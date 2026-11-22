"""Exact Git-to-source approvals for a game-version migration."""
from __future__ import annotations

from collections import Counter, defaultdict
import re
import subprocess

from common import ROOT, lex_script, load_json, sha256_bytes
from rebuild_with_vanilla import parse_script, role_identity

OPERATION = "vanilla_rebase"
NAME_CHANGE = "name_change"
SCRIPT_PREFIXES = ("src/shared/common/characters/", "src/full_only/")
TRANSITION = re.compile(r"\^(?:[0-9a-f]{64}|missing) -> (?:[0-9a-f]{64}|missing)\$")
BIO_ROLES = {
    "advisor", "country_leader", "corps_commander", "field_marshal", "navy_leader", "scientist",
    "create_country_leader", "create_corps_commander", "create_field_marshal", "create_navy_leader",
    "add_corps_commander_role", "add_field_marshal_role", "add_naval_commander_role", "add_navy_leader_role",
}
SHA256 = re.compile(r"[0-9a-f]{64}")
ALLOWLIST = ROOT / "audit/allowlists/diff_exceptions.json"


def rebase_version(document):
    version = document.get("game_version")
    if version is None:
        return None
    if (not isinstance(version, str) or not re.fullmatch(r"\d+(?:\.\d+){3}", version)
            or not any(entry.get("operation") == OPERATION for entry in document.get("exceptions", []))):
        raise ValueError("版本重建必须登记四段原版版本和精确例外")
    return version


def load_rebase_document():
    return load_json(ALLOWLIST) if ALLOWLIST.is_file() else {}


def baseline_game_version():
    summary = ROOT / "audit/baselines/baseline_summary.json"
    return load_json(summary).get("game_version") if summary.is_file() else None


def validated_rebases(base, changed, exceptions):
    """Return exact approved paths and report missing or altered evidence."""
    verified = {}
    errors = []
    entries_by_path = {}
    for entry in exceptions:
        if entry.get("operation") == OPERATION:
            entries_by_path.setdefault(entry.get("path", ""), []).append(entry)
    for path, entries in sorted(entries_by_path.items()):
        if path not in changed:
            errors.append(f"版本重建例外未命中: {path}")
            continue
        entry = entries[0]
        patterns = entry.get("allowed_regex", [])
        if (len(entries) != 1 or not path.startswith(SCRIPT_PREFIXES) or not path.endswith(".txt")
                or any(char in path for char in "*?[")
                or entry.get("approved_by_user") is not True or not str(entry.get("reason", "")).strip()
                or not isinstance(patterns, list) or len(patterns) != 1
                or not isinstance(patterns[0], str) or not TRANSITION.fullmatch(patterns[0])
                or not SHA256.fullmatch(str(entry.get("vanilla_sha256", "")))):
            errors.append(f"版本重建批准必须是唯一文件及精确SHA256转移: {path}")
            continue
        baseline = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT,
                                  capture_output=True)
        if baseline.returncode and not patterns[0].startswith("^missing -> "):
            errors.append(f"读取版本重建Git底稿失败: {path}")
            continue
        before = sha256_bytes(baseline.stdout) if baseline.returncode == 0 else "missing"
        current = ROOT / path
        after = sha256_bytes(current.read_bytes()) if current.is_file() else "missing"
        if not re.fullmatch(patterns[0], f"{before} -> {after}"):
            errors.append(f"版本重建文件内容与批准SHA256转移不符: {path}")
            continue
        verified[path] = entry["vanilla_sha256"]
    return verified, errors


def removed_biography_errors(base, path, vanilla, localization_keys):
    before = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, check=True, capture_output=True)

    def entries(data):
        text = data.decode("utf-8-sig")
        parsed = parse_script(text, {"desc"})
        result = Counter()
        for assignment in parsed.assignments:
            if not assignment.ancestors or assignment.ancestors[-1] not in BIO_ROLES:
                continue
            value = assignment.value.strip('"')
            if value not in localization_keys and not value.startswith(("CBIO_", "POLITICS_")):
                continue
            role = max(
                (b for b in parsed.blocks if b.ancestors == assignment.ancestors and b.anchor <= assignment.anchor),
                key=lambda b: b.anchor,
            )
            identity = tuple(sorted(role_identity(text, role.line).items()))
            result[(assignment.root, assignment.ancestors, identity, value)] += 1
        return result

    lost = entries(before.stdout) - entries(vanilla)
    if lost:
        return [f"撤下覆盖会丢失原版未保留的小传: {path}: {list(lost.items())}"]
    return []


def script_contents(data, shared):
    """Keep non-biography tokens and locate names by character and block occurrence."""
    values = [token.value for token in lex_script(data.decode("utf-8-sig"))]
    address = []
    siblings = [Counter()]
    tokens = []
    names = defaultdict(list)
    i = 0
    while i < len(values):
        value = values[i]
        if value == "{":
            block = values[i-2] if i >= 2 and values[i-1] == "=" else "<anonymous>"
            address.append((block, siblings[-1][block]))
            siblings[-1][block] += 1
            siblings.append(Counter())
        elif value == "}" and address:
            address.pop()
            siblings.pop()
        scalar = i+2 < len(values) and values[i+1] == "=" and values[i+2] not in {"{", "}"}
        if scalar and address:
            bio_desc = value == "desc" and address[-1][0] in BIO_ROLES
            name_scope = len(address) == 2 or (len(address) == 3 and address[-1][0] == "instance")
            character_name = value == "name" and shared and address[0][0] == "characters" and name_scope
            if character_name:
                names[tuple(address)].append(values[i+2])
            if bio_desc or character_name:
                i += 3
                continue
        tokens.append(value)
        i += 1
    return tokens, dict(names)


def approved_name_change(entries, address, before, after):
    expected_address = [list(block) for block in address]
    matches = [entry for entry in entries if entry.get("address") == expected_address]
    if len(matches) != 1:
        return False
    entry = matches[0]
    reason = entry.get("reason")
    return (
        entry.get("approved_by_user") is True
        and isinstance(reason, str) and bool(reason.strip())
        and all(type(block[1]) is int for block in entry["address"])
        and entry.get("old_names") == before
        and entry.get("new_names") == after
    )


def vanilla_semantics_errors(base, path, vanilla, localization_keys, *, changed, name_changes=()):
    current = ROOT / path
    if not current.is_file():
        return removed_biography_errors(base, path, vanilla, localization_keys)
    shared = path.startswith(SCRIPT_PREFIXES[0])
    actual, actual_names = script_contents(current.read_bytes(), shared)
    original, original_names = script_contents(vanilla, shared)
    if actual != original:
        return [f"版本重建存在原版非小传脚本差异: {path}"]
    if not shared:
        return []

    before_names = actual_names
    if changed:
        before = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, capture_output=True)
        if before.returncode != 0:
            tree = subprocess.run(["git", "ls-tree", base, "--", path], cwd=ROOT, capture_output=True)
            if tree.returncode != 0 or tree.stdout:
                return [f"无法读取 Git 基准中的人物显示名: {path}"]
            before_names = original_names
        else:
            _, before_names = script_contents(before.stdout, True)
    errors = []
    for address in sorted(actual_names.keys() | original_names.keys() | before_names.keys()):
        current_names = actual_names.get(address, [])
        vanilla_names = original_names.get(address, [])
        stable_names = before_names.get(address, [])
        block = " > ".join(f"{key}[{ordinal}]" for key, ordinal in address)
        if len(current_names) < len(vanilla_names):
            errors.append(f"缺少原版人物姓名字段: {path} {block}")
        if current_names != stable_names and not approved_name_change(name_changes, address, stable_names, current_names):
            errors.append(f"人物实例姓名变更缺少同一块的精确批准: {path} {block} {stable_names!r} -> {current_names!r}")
        if unresolved := set(Counter(current_names) - Counter(vanilla_names)) - localization_keys:
            errors.append(f"人物实例姓名缺少本地化: {path} {block} {sorted(unresolved)!r}")
    return errors
