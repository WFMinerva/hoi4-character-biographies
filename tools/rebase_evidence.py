"""Exact Git-to-source approvals for a game-version migration."""
from __future__ import annotations

from collections import Counter
import re
import subprocess

from common import ROOT, lex_script, load_json, sha256_bytes
from rebuild_with_vanilla import parse_script, role_identity

OPERATION = "vanilla_rebase"
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
    """Ignore only person-role descriptions; track shared names by their block."""
    values = [token.value for token in lex_script(data.decode("utf-8-sig"))]
    stack = []
    tokens = []
    names = Counter()
    i = 0
    while i < len(values):
        value = values[i]
        if value == "{":
            block = values[i-2] if i >= 2 and values[i-1] == "=" else "<anonymous>"
            stack.append(block)
        elif value == "}" and stack:
            stack.pop()
        scalar = i+2 < len(values) and values[i+1] == "=" and values[i+2] not in {"{", "}"}
        if scalar:
            bio_desc = value == "desc" and stack and stack[-1] in BIO_ROLES
            name_scope = len(stack) == 2 or (len(stack) == 3 and stack[-1] == "instance")
            character_name = value == "name" and shared and stack[0:1] == ["characters"] and name_scope
            if character_name:
                names[tuple(stack), values[i+2]] += 1
            if bio_desc or character_name:
                i += 3
                continue
        tokens.append(value)
        i += 1
    return tokens, names


def vanilla_semantics_errors(base, path, vanilla, localization_keys):
    current = ROOT / path
    if not current.is_file():
        return removed_biography_errors(base, path, vanilla, localization_keys)
    shared = path.startswith(SCRIPT_PREFIXES[0])
    actual, actual_names = script_contents(current.read_bytes(), shared)
    original, original_names = script_contents(vanilla, shared)
    if actual != original:
        return [f"版本重建存在原版非小传脚本差异: {path}"]
    if not shared or actual_names == original_names:
        return []
    before = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, capture_output=True)
    if before.returncode:
        return [f"无法核对旧版人物显示名: {path}"]
    _, approved_names = script_contents(before.stdout, True)
    invalid_names = [
        (context, name) for (context, name), count in (actual_names-original_names).items()
        if name not in localization_keys or not name or count > approved_names[context, name]
    ]
    original_counts = Counter()
    actual_counts = Counter()
    for (context, _), count in original_names.items():
        original_counts[context] += count
    for (context, _), count in actual_names.items():
        actual_counts[context] += count
    errors = []
    if invalid_names:
        errors.append(f"版本重建出现未经批准的姓名: {path} {invalid_names}")
    if removed := original_counts - actual_counts:
        errors.append(f"版本重建缺少原版人物姓名字段: {path} {dict(removed)}")
    return errors
