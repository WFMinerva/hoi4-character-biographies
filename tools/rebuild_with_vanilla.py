from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

from common import ROOT, find_vanilla_reference, lex_script, load_json, save_json, sha256_bytes

PERSON_CONTAINERS = {
    "country_leader",
    "create_country_leader",
    "add_corps_commander_role",
    "add_field_marshal_role",
    "add_naval_commander_role",
}
ROOT_CONTAINERS = {"country_event", "news_event", "unit_leader_event", "operative_leader_event", "focus"}
BOM = b"\xef\xbb\xbf"

# 机主逐条裁定（2026-11-02）的显式落点：只按“文件 + 旧版行号 + 完整键值”精确命中，
# 仅做插入，不参与任何通用身份/语义推断。除这两条外不得扩充。
APPROVED_EXPLICIT_INSERTS = {
    ("events/GOE_Raj.txt", 4039, "CBIO_RAJ_GOE_muhammad_ali_jinnah_desc"): {
        "container": "country_leader",
        "root": "GOE_RAJ_partition.7",
        "character": "RAJ_GOE_muhammad_ali_jinnah",
        "ideology": "liberalism",
    },
    ("events/GOE_Raj.txt", 4155, "CBIO_RAJ_GOE_jawaharlal_nehru_desc"): {
        "container": "country_leader",
        "root": "GOE_RAJ_partition.12",
        "character": "RAJ_GOE_jawaharlal_nehru",
        "ideology": "liberalism",
    },
}


@dataclass
class Assignment:
    field: str
    anchor: int
    line: int
    value: str
    ancestors: tuple[str, ...]
    root: str | None


@dataclass
class Block:
    container: str
    anchor: int
    line: int
    ancestors: tuple[str, ...]


@dataclass
class Parsed:
    tokens: list
    normalized: list[str]
    normalized_tokens: list
    roots: list[str | None]
    assignments: list[Assignment]
    blocks: list[Block]


def parse_script(text: str, fields: set[str]) -> Parsed:
    tokens = lex_script(text)
    normalized: list[str] = []
    normalized_tokens: list = []
    roots: list[str | None] = []
    assignments: list[Assignment] = []
    blocks: list[Block] = []
    stack: list[str] = []
    root_stack: list[str | None] = []
    root: str | None = None
    i = 0

    def add(token) -> None:
        normalized.append(token.value)
        normalized_tokens.append(token)
        roots.append(root)

    while i < len(tokens):
        token = tokens[i]
        if i + 2 < len(tokens) and tokens[i + 1].value == "=" and tokens[i + 2].value == "{":
            root_stack.append(root)
            stack.append(token.value)
            for part in tokens[i:i + 3]:
                add(part)
            blocks.append(Block(token.value, len(normalized), token.line, tuple(stack)))
            i += 3
            continue
        if token.value == "}":
            closed = stack.pop() if stack else None
            add(token)
            previous_root = root_stack.pop() if root_stack else None
            if closed in ROOT_CONTAINERS:
                root = previous_root
            i += 1
            continue
        if token.value in fields and i + 2 < len(tokens) and tokens[i + 1].value == "=" and tokens[i + 2].value != "{":
            assignments.append(Assignment(token.value, len(normalized), token.line, tokens[i + 2].value, tuple(stack), root))
            i += 3
            continue
        if token.value == "id" and i + 2 < len(tokens) and tokens[i + 1].value == "=" and stack and stack[-1] in ROOT_CONTAINERS:
            root = tokens[i + 2].value
            for part in tokens[i:i + 3]:
                add(part)
            i += 3
            continue
        add(token)
        i += 1
    return Parsed(tokens, normalized, normalized_tokens, roots, assignments, blocks)


def mapping(old: Parsed, new: Parsed) -> dict[int, int]:
    result: dict[int, int] = {}
    matcher = SequenceMatcher(None, old.normalized, new.normalized, autojunk=True)
    for a, b, size in matcher.get_matching_blocks():
        for offset in range(size):
            result[a + offset] = b + offset
    return result


def root_mapping(old: Parsed, new: Parsed, root: str | None) -> tuple[dict[int, int], dict[int, int]] | None:
    if root is None:
        return None
    old_indices = [i for i, value in enumerate(old.roots) if value == root]
    new_indices = [i for i, value in enumerate(new.roots) if value == root]
    if not old_indices or not new_indices:
        return None
    old_values = [old.normalized[i] for i in old_indices]
    new_values = [new.normalized[i] for i in new_indices]
    matcher = SequenceMatcher(None, old_values, new_values, autojunk=False)
    local: dict[int, int] = {}
    for a, b, size in matcher.get_matching_blocks():
        for offset in range(size):
            local[old_indices[a + offset]] = new_indices[b + offset]
    reverse = {new: old for old, new in local.items()}
    return local, reverse


def localisation_keys(donor: Path) -> set[str]:
    pattern = re.compile(r'^\s*([A-Za-z0-9_]+):\d+\s+"', re.M)
    keys: set[str] = set()
    for path in (donor / "localisation").rglob("*.yml"):
        keys.update(pattern.findall(path.read_text(encoding="utf-8-sig")))
    return keys


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_digest(rows: dict[str, str]) -> str:
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def output_bytes(text: str, original: bytes) -> bytes:
    newline = "\r\n" if b"\r\n" in original else "\n"
    text = text.replace("\r\n", "\n").replace("\n", newline)
    data = text.encode("utf-8")
    return (BOM if original.startswith(BOM) else b"") + data


def line_indent(line: str) -> str:
    return line[:len(line) - len(line.lstrip(" \t"))]


def role_identity(text: str, line: int) -> dict[str, str]:
    lines = text.splitlines()
    before = "\n".join(lines[max(0, line - 12):line])
    starts = list(re.finditer(r"(add_country_leader_role|create_country_leader|add_corps_commander_role|add_field_marshal_role|add_naval_commander_role)\s*=\s*\{", before))
    if not starts:
        return {}
    start = starts[-1]
    block = before[start.start():] + "\n" + "\n".join(lines[line - 1:line + 20])
    role = start.group(1)
    fields = ("name", "picture", "ideology") if role == "create_country_leader" else ("character", "ideology")
    result = {}
    for field in fields:
        match = re.search(rf"\b{field}\s*=\s*(\"[^\"]+\"|[^\s#]+)", block)
        if match:
            result[field] = match.group(1)
    return result


def build_expected(rel: str, donor_text: str, vanilla_text: str, fields: set[str], keys: set[str], shared: bool, static_requests: list[dict]):
    donor = parse_script(donor_text, fields)
    vanilla = parse_script(vanilla_text, fields)
    direct = mapping(donor, vanilla)
    root_maps: dict[str | None, tuple[dict[int, int], dict[int, int]] | None] = {}
    replacements: dict[int, str] = {}
    insertions: dict[int, list[str]] = defaultdict(list)
    planned_inserts: set[tuple[str, int, str]] = set()
    overlays: list[dict] = []
    errors: list[str] = []
    targeted_vanilla: set[tuple[str, int]] = set()

    def static_candidate(assignment: Assignment) -> str | None:
        root_lines = [token.line for i, token in enumerate(vanilla.normalized_tokens) if vanilla.roots[i] == assignment.root]
        if not root_lines:
            return None
        vanilla_lines = vanilla_text.splitlines()
        root_text = "\n".join(vanilla_lines[min(root_lines) - 1:max(root_lines)])
        candidates = []
        for body in re.findall(r"promote_character\s*=\s*\{([^}}]*)\}", root_text, re.S):
            character = re.search(r"character\s*=\s*([A-Za-z0-9_]+)", body)
            ideology = re.search(r"ideology\s*=\s*([A-Za-z0-9_]+)", body)
            if character and ideology:
                candidates.append((character.group(1), ideology.group(1)))
        donor_identity = role_identity(donor_text, assignment.line)
        if "character" in donor_identity:
            matched = {character for character, _ in candidates if character == donor_identity["character"]}
        else:
            donor_lines = donor_text.splitlines()
            donor_block = "\n".join(donor_lines[assignment.line - 1:assignment.line + 20])
            donor_ideology = re.search(r"ideology\s*=\s*([A-Za-z0-9_]+)", donor_block)
            matched = {character for character, ideology in candidates if donor_ideology and ideology == donor_ideology.group(1)}
        return matched.pop() if len(matched) == 1 else None

    def append_static(assignment: Assignment, character: str) -> None:
        overlays.append({
            "field": assignment.field,
            "value": assignment.value,
            "person_id": character,
            "container": "promote_character",
            "ancestors": list(assignment.ancestors),
            "root": assignment.root,
            "donor_anchor": assignment.anchor,
            "vanilla_anchor": None,
            "action": "inherit_static",
        })

    def moved_role_candidate(assignment: Assignment):
        donor_lines = donor_text.splitlines()
        before = "\n".join(donor_lines[max(0, assignment.line - 8):assignment.line])
        character = re.search(r"character\s*=\s*([A-Za-z0-9_]+)", before)
        if not character:
            return None
        donor_block = "\n".join(donor_lines[assignment.line - 1:assignment.line + 20])
        ideology = re.search(r"ideology\s*=\s*([A-Za-z0-9_]+)", donor_block)
        traits = re.search(r"traits\s*=\s*\{([^}}]*)\}", donor_block, re.S)
        identity = re.search(r"\bid\s*=\s*(-?\d+)", donor_block)
        vanilla_lines = vanilla_text.splitlines()
        matches = []
        for block in vanilla.blocks:
            if block.container != "country_leader" or len(block.ancestors) < 2 or block.ancestors[-2] != "add_country_leader_role":
                continue
            before_block = "\n".join(vanilla_lines[max(0, block.line - 8):block.line])
            if not re.search(rf"character\s*=\s*{re.escape(character.group(1))}\b", before_block):
                continue
            after_block = "\n".join(vanilla_lines[block.line - 1:block.line + 20])
            block_ideology = re.search(r"ideology\s*=\s*([A-Za-z0-9_]+)", after_block)
            if ideology and block_ideology and ideology.group(1) == block_ideology.group(1):
                block_traits = re.search(r"traits\s*=\s*\{([^}}]*)\}", after_block, re.S)
                block_identity = re.search(r"\bid\s*=\s*(-?\d+)", after_block)
                if traits and (not block_traits or traits.group(1).split() != block_traits.group(1).split()):
                    continue
                if identity and (not block_identity or identity.group(1) != block_identity.group(1)):
                    continue
                matches.append(block)
        return matches[0] if len(matches) == 1 else None

    def create_role_candidate(assignment: Assignment):
        wanted = role_identity(donor_text, assignment.line)
        if not wanted:
            return None
        matches = []
        for block in vanilla.blocks:
            if block.container != "create_country_leader":
                continue
            actual = role_identity(vanilla_text, block.line)
            if all(actual.get(field) == value for field, value in wanted.items()):
                matches.append(block)
        if len(matches) == 1:
            return matches[0]
        same_branch = [b for b in matches if b.ancestors == assignment.ancestors]
        if len(same_branch) == 1:
            return same_branch[0]
        same_root = [b for b in matches if vanilla.roots[b.anchor - 1] == assignment.root]
        return same_root[0] if len(same_root) == 1 else None

    def role_candidate(assignment: Assignment):
        if assignment.ancestors[-1] == "add_country_leader_role":
            return moved_role_candidate(assignment)
        if assignment.ancestors[-1] == "create_country_leader":
            return create_role_candidate(assignment)
        return None

    def containing_block(assignment: Assignment, anchor: int):
        matches = [b for b in vanilla.blocks if b.container == assignment.ancestors[-1] and b.anchor <= anchor]
        return max(matches, key=lambda b: b.anchor) if matches else None

    def candidate_anchor(assignment: Assignment, block) -> int:
        existing = [a for a in vanilla.assignments if a.field == assignment.field and a.ancestors == block.ancestors and a.anchor >= block.anchor]
        if existing:
            return min(existing, key=lambda a: a.anchor).anchor
        return block.anchor

    def identity_mismatch(assignment: Assignment, anchor: int) -> bool:
        if shared:
            return False
        block = containing_block(assignment, anchor)
        if block is None:
            return True
        donor_identity = role_identity(donor_text, assignment.line)
        vanilla_identity = role_identity(vanilla_text, block.line)
        return any(field not in vanilla_identity or vanilla_identity[field] != value for field, value in donor_identity.items())

    explicit_used: set[tuple[str, int, str]] = set()

    def explicit_insert(assignment: Assignment, value: str, spec: dict) -> None:
        explicit_used.add((rel, assignment.line, value))
        donor_line = donor_text.splitlines()[assignment.line - 1]
        if value not in donor_line:
            errors.append(f"{rel}:{assignment.line} 显式裁定行与旧版键值不一致 {assignment.value}")
            return
        candidates = [
            block for block in vanilla.blocks
            if block.container == spec["container"]
            and vanilla.roots[block.anchor - 1] == spec["root"]
            and role_identity(vanilla_text, block.line).get("character") == spec["character"]
            and role_identity(vanilla_text, block.line).get("ideology") == spec["ideology"]
        ]
        if len(candidates) != 1:
            errors.append(f"{rel}:{assignment.line} {assignment.value} 显式裁定目标不唯一或身份不符")
            return
        block = candidates[0]
        if [a for a in vanilla.assignments if a.field == assignment.field and a.ancestors == block.ancestors and a.anchor >= block.anchor]:
            errors.append(f"{rel}:{assignment.line} {assignment.value} 显式裁定目标块已有 {assignment.field}")
            return
        anchor_line = vanilla.normalized_tokens[block.anchor - 1].line
        if block.anchor < len(vanilla.normalized_tokens) and vanilla.normalized_tokens[block.anchor].line == anchor_line:
            errors.append(f"{rel}:{assignment.line} 显式裁定目标为复杂同行块，拒绝插入")
            return
        insertions[anchor_line].append(f"{line_indent(donor_line)}{assignment.field} = {assignment.value}")
        planned_inserts.add((assignment.field, block.anchor, assignment.value))
        overlays.append({
            "field": assignment.field,
            "value": assignment.value,
            "person_id": spec["character"],
            "container": spec["container"],
            "ancestors": list(block.ancestors),
            "root": spec["root"],
            "vanilla_root": vanilla.roots[block.anchor - 1],
            "identity": role_identity(donor_text, assignment.line),
            "donor_anchor": assignment.anchor,
            "vanilla_anchor": block.anchor,
            "action": "insert",
            "explicit_approval": True,
        })

    for assignment in donor.assignments:
        value = assignment.value.strip('"')
        person = assignment.ancestors and assignment.ancestors[-1] in PERSON_CONTAINERS
        if shared:
            target = True
        else:
            target = person and (value in keys or value.startswith("POLITICS_"))
        if not target:
            continue
        spec = APPROVED_EXPLICIT_INSERTS.get((rel, assignment.line, value))
        if spec is not None:
            explicit_insert(assignment, value, spec)
            continue
        if assignment.anchor == 0:
            errors.append(f"{rel}:{assignment.line} 无法确定前置语义锚点")
            continue
        old_anchor = assignment.anchor - 1
        new_anchor = direct.get(old_anchor)
        if new_anchor is not None and assignment.root is not None and vanilla.roots[new_anchor] != assignment.root:
            new_anchor = None
        if new_anchor is not None:
            new_anchor += 1
        else:
            if assignment.root not in root_maps:
                root_maps[assignment.root] = root_mapping(donor, vanilla, assignment.root)
            fallback = root_maps[assignment.root]
            if fallback and old_anchor in fallback[0]:
                new_anchor = fallback[0][old_anchor] + 1
        if new_anchor is None or new_anchor > len(vanilla.normalized_tokens):
            inherited_character = static_candidate(assignment) if not shared else None
            if inherited_character:
                append_static(assignment, inherited_character)
                continue
            moved_role = role_candidate(assignment)
            if moved_role:
                new_anchor = candidate_anchor(assignment, moved_role)
            else:
                errors.append(f"{rel}:{assignment.line} {assignment.value} 无法匹配新版语义块 root={assignment.root}")
                continue

        if identity_mismatch(assignment, new_anchor):
            inherited_character = static_candidate(assignment) if not shared else None
            if inherited_character:
                append_static(assignment, inherited_character)
                continue
            moved_role = role_candidate(assignment)
            if moved_role:
                new_anchor = candidate_anchor(assignment, moved_role)
            if identity_mismatch(assignment, new_anchor):
                errors.append(f"{rel}:{assignment.line} {assignment.value} 人物身份与新版目标块不一致")
                continue

        current = [a for a in vanilla.assignments if a.field == assignment.field and a.anchor == new_anchor]
        if not shared and not current:
            candidate = role_candidate(assignment)
            if candidate:
                new_anchor = candidate_anchor(assignment, candidate)
                current = [a for a in vanilla.assignments if a.field == assignment.field and a.anchor == new_anchor]
        action = "insert"
        if current:
            if len(current) != 1 or current[0].ancestors != assignment.ancestors:
                errors.append(f"{rel}:{assignment.line} {assignment.value} 新版目标块不唯一或层级变化")
                continue
            existing = current[0]
            targeted_vanilla.add((existing.field, existing.anchor))
            if existing.value == assignment.value:
                action = "inherit"
            elif not shared and value not in keys:
                errors.append(f"{rel}:{assignment.line} 非项目键替换未获裁定 {assignment.value} -> {existing.value}")
                continue
            else:
                action = "replace"
                line = vanilla_text.splitlines()[existing.line - 1]
                if not re.match(rf"^\s*{re.escape(assignment.field)}\s*=.*$", line):
                    errors.append(f"{rel}:{assignment.line} 目标为复杂行，拒绝行内替换")
                    continue
                replacements[existing.line] = f"{line_indent(line)}{assignment.field} = {assignment.value}"
        elif not shared and value not in keys:
            inherited_character = static_candidate(assignment)
            if inherited_character:
                append_static(assignment, inherited_character)
                continue
            errors.append(f"{rel}:{assignment.line} 新版缺少非项目键原值，需人工裁定 {assignment.value}")
            continue

        if action == "insert":
            anchor_line = vanilla.normalized_tokens[new_anchor - 1].line
            if new_anchor < len(vanilla.normalized_tokens) and vanilla.normalized_tokens[new_anchor].line == anchor_line:
                errors.append(f"{rel}:{assignment.line} 目标锚点为复杂同行块，拒绝插入")
                continue
            donor_line = donor_text.splitlines()[assignment.line - 1]
            insertions[anchor_line].append(f"{line_indent(donor_line)}{assignment.field} = {assignment.value}")
            planned_inserts.add((assignment.field, new_anchor, assignment.value))
        overlays.append({
            "field": assignment.field,
            "value": assignment.value,
            "person_id": assignment.ancestors[-2] if len(assignment.ancestors) > 1 else None,
            "container": assignment.ancestors[-1] if assignment.ancestors else None,
            "ancestors": list(assignment.ancestors),
            "root": assignment.root,
            "vanilla_root": vanilla.roots[new_anchor - 1] if new_anchor > 0 else None,
            "identity": role_identity(donor_text, assignment.line),
            "donor_anchor": assignment.anchor,
            "vanilla_anchor": new_anchor,
            "action": action,
        })

    for spec_key in APPROVED_EXPLICIT_INSERTS:
        if spec_key[0] == rel and spec_key not in explicit_used:
            errors.append(f"{rel}:{spec_key[1]} 已裁定显式落点未命中 {spec_key[2]}")

    if shared:
        vanilla_lines = vanilla_text.splitlines()
        for request in static_requests:
            character = request["person_id"]
            matches = [b for b in vanilla.blocks if b.container == "country_leader" and character in b.ancestors[:-1]]
            if not matches:
                continue
            if len(matches) != 1:
                errors.append(f"{rel} 静态人物 {character} 的 country_leader 块不唯一")
                continue
            block = matches[0]
            existing = [a for a in vanilla.assignments if a.field == "desc" and a.ancestors == block.ancestors and a.anchor >= block.anchor]
            if existing and existing[0].value != request["value"]:
                errors.append(f"{rel} 静态人物 {character} 已有不同 desc: {existing[0].value}")
                continue
            planned = {(value, anchor) for field, anchor, value in planned_inserts if field == "desc" and anchor == block.anchor}
            if any(value != request["value"] for value, _ in planned):
                errors.append(f"{rel} 静态人物 {character} 已有不同计划 desc: {sorted(planned)}")
                continue
            action = "inherit_static" if (existing or planned) else "insert_static"
            if action == "insert_static":
                indent = line_indent(vanilla_lines[block.line]) if block.line < len(vanilla_lines) else line_indent(vanilla_lines[block.line - 1]) + "\t"
                insertions[block.line].append(f"{indent}desc = {request['value']}")
                planned_inserts.add(("desc", block.anchor, request["value"]))
            overlays.append({
                "field": "desc",
                "value": request["value"],
                "person_id": character,
                "static_character": character,
                "container": "country_leader",
                "ancestors": list(block.ancestors),
                "root": None,
                "donor_anchor": None,
                "vanilla_anchor": block.anchor,
                "action": action,
            })

    if errors:
        return None, overlays, errors

    lines = vanilla_text.splitlines()
    result: list[str] = []
    for number, line in enumerate(lines, 1):
        if number in replacements:
            result.append(replacements[number])
        else:
            result.append(line)
        result.extend(insertions.get(number, []))
    expected = "\n".join(result) + ("\n" if vanilla_text.endswith("\n") else "")
    check = parse_script(expected, fields)
    if check.normalized != vanilla.normalized:
        errors.append(f"{rel} 重建后非叠加token不等于新版")
        return None, overlays, errors
    vanilla_groups = Counter((a.field, a.anchor, a.ancestors) for a in vanilla.assignments)
    for (field, anchor, ancestors), count in Counter((a.field, a.anchor, a.ancestors) for a in check.assignments).items():
        if count > 1 and vanilla_groups[(field, anchor, ancestors)] < count:
            errors.append(f"{rel} 叠加字段重复 anchor={anchor} {field}")
    if errors:
        return None, overlays, errors

    expected_assignments = {(a.field, a.anchor, a.value, a.ancestors) for a in check.assignments}
    for overlay in overlays:
        if overlay["action"] == "inherit_static":
            continue
        wanted = (overlay["field"], overlay["vanilla_anchor"], overlay["value"], tuple(overlay["ancestors"]))
        if wanted not in expected_assignments:
            errors.append(f"{rel} 叠加回读失败 {overlay['value']} anchor={overlay['vanilla_anchor']}")
    for existing in vanilla.assignments:
        if (existing.field, existing.anchor) in targeted_vanilla:
            continue
        wanted = (existing.field, existing.anchor, existing.value, existing.ancestors)
        if wanted not in expected_assignments:
            errors.append(f"{rel} 新版原有字段被改 {existing.field}={existing.value} anchor={existing.anchor}")
    return (expected if not errors else None), overlays, errors


def exception_document(outputs: list[dict]) -> dict:
    exceptions = []
    with tempfile.TemporaryDirectory(prefix="cbio_rebase_exceptions_") as tmp:
        expected_file = Path(tmp) / "expected.txt"
        for row in outputs:
            if not row["rel"].endswith(".txt"):
                continue
            expected_file.write_bytes(row["data"])
            diff = subprocess.run(
                ["git", "diff", "--no-index", "--unified=0", "--no-ext-diff", "--", str(row["target"]), str(expected_file)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
            )
            if diff.returncode not in (0, 1):
                raise RuntimeError(f"生成精确例外失败: {row['rel']}: {diff.stderr}")
            counts: dict[tuple[str, str], int] = defaultdict(int)
            for line in diff.stdout.splitlines():
                if line.startswith(("+++", "---", "@@", "diff --git", "index ", "new file mode", "deleted file mode")):
                    continue
                if not line.startswith(("+", "-")):
                    continue
                direction, content = line[0], line[1:]
                if re.match(r"^\s*desc\s*=", content) or re.match(r"^\s*(?:#.*)?$", content):
                    continue
                counts[(direction, content)] += 1
            if not counts:
                continue
            exact = [{"direction": direction, "line": content, "count": count} for (direction, content), count in sorted(counts.items())]
            exceptions.append({
                "path": row["rel"],
                "reason": "HOI4 1.19.4.1 全量重建：由基线与已验证新版原版预生成，非工作树自我授权",
                "approved_by_user": True,
                "allowed_regex": sorted({re.escape(line) for _, line in counts}),
                "exact_lines": exact,
            })
    return {
        "schema_version": 1,
        "instructions": "默认脚本diff只允许desc赋值。exact_lines由基线与已验证原版预生成，绑定方向、整行和次数；未命中、过期或多余例外均失败。禁止allow_all与宽泛正则。",
        "exceptions": exceptions,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Dry-run HOI4 vanilla rebase; only --apply may write src/")
    parser.add_argument("--donor")
    parser.add_argument("--game-version")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--restore", action="store_true")
    parser.add_argument("--backup-dir", default="build/rebuild-backup")
    parser.add_argument("--manifest", default="audit/allowlists/rebuild_manifest.json")
    args = parser.parse_args()
    if args.apply and args.restore:
        parser.error("--apply 与 --restore 互斥")

    backup_root = ROOT / args.backup_dir
    backup_manifest = backup_root / "manifest.json"
    if args.restore:
        data = load_json(backup_manifest)
        errors = []
        for row in data["files"]:
            target = ROOT / row["target"]
            backup = ROOT / row["backup"]
            if not backup.exists() or file_digest(backup) != row["original_sha256"]:
                errors.append(f"备份缺失或哈希不符，拒绝恢复: {row['backup']}")
            if not target.exists() or file_digest(target) != row["written_sha256"]:
                errors.append(f"目标已变化，拒绝覆盖: {row['target']}")
        for row in data.get("created", []):
            target = ROOT / row["target"]
            if target.exists() and file_digest(target) != row["sha256"]:
                errors.append(f"新建清单已变化，拒绝删除: {row['target']}")
        if errors:
            for error in errors:
                print("ERROR", error)
            raise SystemExit(1)
        for row in data["files"]:
            target = ROOT / row["target"]
            shutil.copy2(ROOT / row["backup"], target)
            if file_digest(target) != row["original_sha256"]:
                raise SystemExit(f"恢复后哈希不符: {row['target']}")
        for row in data.get("created", []):
            target = ROOT / row["target"]
            if target.exists():
                target.unlink()
        print(f"restore: files={len(data['files'])} created={len(data.get('created', []))} OK")
        return

    if not args.donor or not args.game_version:
        parser.error("非 --restore 模式必须提供 --donor 与 --game-version")
    donor = Path(args.donor).resolve()
    vanilla = find_vanilla_reference()
    if not donor.is_dir() or vanilla is None or not vanilla.is_dir():
        parser.error("donor/原版目录无效")
    launcher = load_json(vanilla / "launcher-settings.json")
    if launcher.get("rawVersion") != args.game_version:
        raise SystemExit(f"原版版本不符: expected={args.game_version} actual={launcher.get('rawVersion')}")

    donor_files = {p.relative_to(donor).as_posix(): file_digest(p) for p in donor.rglob("*") if p.is_file()}
    donor_hash = manifest_digest(donor_files)
    keys = localisation_keys(donor)
    full_root = ROOT / "src/full_only"
    shared_root = ROOT / "src/shared"
    full_all = sorted(full_root.rglob("*.txt"))
    shared_all = sorted((shared_root / "common/characters").glob("*.txt"))
    static_requests: list[dict] = []
    full_targets = []
    shared_targets = []
    unchanged = []
    no_project_key_paths = []
    errors: list[str] = []

    for path in full_all:
        rel = path.relative_to(full_root).as_posix()
        donor_text = (donor / rel).read_text(encoding="utf-8-sig")
        vanilla_text = (vanilla / rel).read_text(encoding="utf-8-sig")
        donor_assignments = parse_script(donor_text, {"desc"}).assignments
        if not any(a.ancestors and a.ancestors[-1] in PERSON_CONTAINERS and a.value.strip('"') in keys for a in donor_assignments):
            no_project_key_paths.append(f"src/full_only/{rel}")
        if parse_script(donor_text, {"desc"}).normalized == parse_script(vanilla_text, {"desc"}).normalized:
            unchanged.append({"path": f"src/full_only/{rel}", "sha256": file_digest(path)})
        else:
            full_targets.append((path, rel))
    for path in shared_all:
        rel = path.relative_to(shared_root).as_posix()
        donor_text = (donor / rel).read_text(encoding="utf-8-sig")
        vanilla_text = (vanilla / rel).read_text(encoding="utf-8-sig")
        if rel == "common/characters/PHI.txt" or parse_script(donor_text, {"desc", "name"}).normalized != parse_script(vanilla_text, {"desc", "name"}).normalized:
            shared_targets.append((path, rel))
        else:
            unchanged.append({"path": f"src/shared/{rel}", "sha256": file_digest(path)})

    outputs: list[dict] = []
    for path, rel in full_targets:
        donor_text = (donor / rel).read_text(encoding="utf-8-sig")
        vanilla_text = (vanilla / rel).read_text(encoding="utf-8-sig")
        expected, overlays, file_errors = build_expected(rel, donor_text, vanilla_text, {"desc"}, keys, False, [])
        errors.extend(file_errors)
        static_requests.extend(overlay for overlay in overlays if overlay["action"] == "inherit_static")
        if expected is not None:
            data = output_bytes(expected, path.read_bytes())
            outputs.append({"target": path, "rel": f"src/full_only/{rel}", "data": data, "overlays": overlays, "donor_sha": file_digest(donor / rel), "vanilla_sha": file_digest(vanilla / rel)})
    static_requests = list({(row["person_id"], row["value"]): row for row in static_requests}.values())
    for path, rel in shared_targets:
        donor_text = (donor / rel).read_text(encoding="utf-8-sig")
        vanilla_text = (vanilla / rel).read_text(encoding="utf-8-sig")
        expected, overlays, file_errors = build_expected(rel, donor_text, vanilla_text, {"desc", "name"}, keys, True, static_requests)
        errors.extend(file_errors)
        if expected is not None:
            data = output_bytes(expected, path.read_bytes())
            outputs.append({"target": path, "rel": f"src/shared/{rel}", "data": data, "overlays": overlays, "donor_sha": file_digest(donor / rel), "vanilla_sha": file_digest(vanilla / rel)})

    static_done = {overlay["static_character"] for row in outputs for overlay in row["overlays"] if "static_character" in overlay}
    for request in static_requests:
        if request["person_id"] not in static_done:
            errors.append(f"静态人物继承未落到 shared: {request['person_id']} {request['value']}")

    for rel in [
        "localisation/simp_chinese/zz_v115_8countries_bios_l_simp_chinese.yml",
        "localisation/simp_chinese/zzzz_ger_bio_v86_l_simp_chinese.yml",
    ]:
        target = shared_root / rel
        outputs.append({"target": target, "rel": f"src/shared/{rel}", "data": (donor / rel).read_bytes(), "overlays": [], "donor_sha": file_digest(donor / rel), "vanilla_sha": None})

    if len(full_targets) != 114 or len(shared_targets) != 24 or len(no_project_key_paths) != 79:
        errors.append(f"目标数量变化: full={len(full_targets)} shared={len(shared_targets)} no_project={len(no_project_key_paths)}")
    if errors:
        for error in errors:
            print("ERROR", error)
        print(f"rebuild_dry_run: full={len(full_targets)} shared={len(shared_targets)} outputs={len(outputs)} errors={len(errors)}")
        raise SystemExit(1)

    exceptions = exception_document(outputs)
    save_json(ROOT / "audit/reports/diff_exceptions.json", exceptions)

    manifest = {
        "schema_version": 1,
        "approved_by_user": True,
        "game_version": args.game_version,
        "vanilla_path": str(vanilla),
        "donor_path": str(donor),
        "donor_manifest_sha256": donor_hash,
        "no_project_key_paths": no_project_key_paths,
        "unchanged": unchanged,
        "files": [{
            "path": row["rel"],
            "donor_sha256": row["donor_sha"],
            "vanilla_sha256": row["vanilla_sha"],
            "expected_sha256": sha256_bytes(row["data"]),
            "overlays": row["overlays"],
        } for row in outputs],
    }
    manifest["semantic_manifest_sha256"] = manifest_digest({
        row["path"]: row["expected_sha256"] for row in manifest["files"]
    } | {row["path"]: row["sha256"] for row in unchanged})

    print(f"rebuild_dry_run: full={len(full_targets)} shared={len(shared_targets)} loc=2 unchanged={len(unchanged)} overlays={sum(len(x['overlays']) for x in outputs)} errors=0")
    print(f"donor_manifest_sha256={donor_hash}")
    print(f"semantic_manifest_sha256={manifest['semantic_manifest_sha256']}")
    if not args.apply:
        save_json(ROOT / "audit/reports/rebuild_dry_run.json", manifest)
        print("dry-run only; --apply required to write src/")
        return

    exception_target = ROOT / "audit/allowlists/diff_exceptions.json"
    exception_data = (json.dumps(exceptions, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    outputs.append({"target": exception_target, "rel": "audit/allowlists/diff_exceptions.json", "data": exception_data, "overlays": [], "donor_sha": None, "vanilla_sha": None})

    backup_rows = []
    if backup_root.exists():
        raise SystemExit(f"备份目录已存在，拒绝覆盖: {backup_root}")
    for row in outputs:
        target: Path = row["target"]
        backup = backup_root / row["rel"]
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
        backup_rows.append({
            "target": row["rel"],
            "backup": str(backup.relative_to(ROOT)),
            "original_sha256": file_digest(target),
            "written_sha256": sha256_bytes(row["data"]),
        })
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    manifest_target = ROOT / args.manifest
    created = []
    if manifest_target.exists():
        outputs.append({"target": manifest_target, "rel": args.manifest, "data": manifest_bytes, "overlays": [], "donor_sha": None, "vanilla_sha": None})
    else:
        created = [{"target": args.manifest, "sha256": sha256_bytes(manifest_bytes)}]
    save_json(backup_manifest, {"files": backup_rows, "created": created})
    for row in outputs:
        row["target"].write_bytes(row["data"])
        if file_digest(row["target"]) != sha256_bytes(row["data"]):
            raise SystemExit(f"写入后哈希不符: {row['target']}")
    manifest_target.write_bytes(manifest_bytes)
    if file_digest(manifest_target) != sha256_bytes(manifest_bytes):
        raise SystemExit(f"写入后哈希不符: {args.manifest}")
    print(f"apply: files={len(outputs)} backup={backup_root} manifest={args.manifest}")


if __name__ == "__main__":
    main()
