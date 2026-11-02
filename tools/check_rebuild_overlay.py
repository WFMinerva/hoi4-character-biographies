from __future__ import annotations

from collections import Counter
from pathlib import Path

from common import ROOT, find_vanilla_reference, load_json
from rebuild_with_vanilla import PERSON_CONTAINERS, file_digest, localisation_keys, manifest_digest, parse_script, role_identity

MANIFEST = ROOT / "audit/allowlists/rebuild_manifest.json"
if not MANIFEST.exists():
    print("rebuild_overlay: SKIP（无重建manifest）")
    raise SystemExit(0)

m = load_json(MANIFEST)
errors: list[str] = []
vanilla = find_vanilla_reference()
donor = Path(m["donor_path"])
if vanilla is None:
    errors.append("未配置原版路径")
else:
    launcher = load_json(vanilla / "launcher-settings.json")
    if launcher.get("rawVersion") != m["game_version"]:
        errors.append(f"原版版本不符: {launcher.get('rawVersion')} != {m['game_version']}")
if not donor.is_dir():
    errors.append(f"donor目录不存在: {donor}")
else:
    donor_files = {p.relative_to(donor).as_posix(): file_digest(p) for p in donor.rglob("*") if p.is_file()}
    if manifest_digest(donor_files) != m["donor_manifest_sha256"]:
        errors.append("donor清单哈希已变化")

expected_hash = m["semantic_manifest_sha256"]
actual_semantic = manifest_digest(
    {row["path"]: row["expected_sha256"] for row in m["files"]}
    | {row["path"]: row["sha256"] for row in m["unchanged"]}
)
if actual_semantic != expected_hash:
    errors.append("semantic_manifest_sha256与清单内容不符")

for row in m["files"]:
    path = ROOT / row["path"]
    if not path.exists():
        errors.append(f"缺少目标文件: {row['path']}")
    elif file_digest(path) != row["expected_sha256"]:
        errors.append(f"目标哈希不符: {row['path']}")
for row in m["unchanged"]:
    path = ROOT / row["path"]
    if not path.exists():
        errors.append(f"不动文件被删除: {row['path']}")
    elif file_digest(path) != row["sha256"]:
        errors.append(f"不动文件哈希变化: {row['path']}")

full_paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / "src/full_only").rglob("*.txt")}
shared_paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / "src/shared/common/characters").glob("*.txt")}
manifest_full = {row["path"] for row in m["files"] + m["unchanged"] if row["path"].startswith("src/full_only/")}
manifest_shared = {row["path"] for row in m["files"] + m["unchanged"] if row["path"].startswith("src/shared/common/characters/")}
if full_paths != manifest_full:
    errors.append(f"full_only路径集合变化: missing={sorted(manifest_full - full_paths)} extra={sorted(full_paths - manifest_full)}")
if shared_paths != manifest_shared:
    errors.append(f"shared人物路径集合变化: missing={sorted(manifest_shared - shared_paths)} extra={sorted(shared_paths - manifest_shared)}")

keys = localisation_keys(donor) if donor.is_dir() else set()
project_count = 0
nonproject_count = 0
protected_count = 0
protected = {"EGY", "ISR", "JOR", "LEB", "LIB", "PAL", "SYR"}

for row in m["files"] + m["unchanged"]:
    rel = row["path"]
    if not rel.endswith(".txt") or not (rel.startswith("src/full_only/") or rel.startswith("src/shared/common/characters/")):
        continue
    source = ROOT / rel
    shared = rel.startswith("src/shared/")
    fields = {"desc", "name"} if shared else {"desc"}
    if vanilla is None:
        continue
    vanilla_rel = rel.removeprefix("src/full_only/").removeprefix("src/shared/")
    vanilla_file = vanilla / vanilla_rel
    if not vanilla_file.exists():
        errors.append(f"原版缺少同路径文件: {rel}")
        continue
    parsed = parse_script(source.read_text(encoding="utf-8-sig"), fields)
    original = parse_script(vanilla_file.read_text(encoding="utf-8-sig"), fields)
    if parsed.normalized != original.normalized:
        errors.append(f"去除叠加字段后仍与原版不同: {rel}")
    if rel.startswith("src/full_only/"):
        for assignment in parsed.assignments:
            if not assignment.ancestors or assignment.ancestors[-1] not in PERSON_CONTAINERS:
                continue
            value = assignment.value.strip('"')
            if value in keys:
                project_count += 1
            elif value.startswith("POLITICS_"):
                nonproject_count += 1
            if any(f"/{tag} - " in rel for tag in protected):
                protected_count += 1

for row in m["files"]:
    if not row["path"].endswith(".txt"):
        continue
    source = ROOT / row["path"]
    if not source.exists():
        continue
    shared = row["path"].startswith("src/shared/")
    parsed = parse_script(source.read_text(encoding="utf-8-sig"), {"desc", "name"} if shared else {"desc"})
    source_text = source.read_text(encoding="utf-8-sig")
    assignments = {(a.field, a.anchor, a.value, a.ancestors) for a in parsed.assignments}
    for overlay in row["overlays"]:
        if overlay["vanilla_anchor"] is None:
            continue
        wanted = (overlay["field"], overlay["vanilla_anchor"], overlay["value"], tuple(overlay["ancestors"]))
        if wanted not in assignments:
            errors.append(f"人物叠加回读失败: {row['path']} {overlay['value']} anchor={overlay['vanilla_anchor']}")
        if not shared:
            if not overlay.get("identity"):
                errors.append(f"人物叠加缺少身份证据: {row['path']} {overlay['value']}")
                continue
            blocks = [b for b in parsed.blocks if b.anchor <= overlay["vanilla_anchor"] and b.container == overlay["container"]]
            if not blocks:
                errors.append(f"人物身份块无法唯一回读: {row['path']} {overlay['value']}")
            else:
                block = max(blocks, key=lambda b: b.anchor)
                actual = role_identity(source_text, block.line)
                for field, expected in overlay["identity"].items():
                    if actual.get(field) != expected:
                        errors.append(f"人物身份错挂: {row['path']} {overlay['value']} {field}: {actual.get(field)} != {expected}")

if project_count != 821:
    errors.append(f"项目键人物desc数量不符: {project_count} != 821")
if nonproject_count != 56:
    errors.append(f"完整版非项目键动态desc数量不符: {nonproject_count} != 56")
if protected_count != 18:
    errors.append(f"七国动态人物desc数量不符: {protected_count} != 18")
if len(m.get("no_project_key_paths", [])) != 79 or any((ROOT / p).suffix != ".txt" or not (ROOT / p).exists() for p in m.get("no_project_key_paths", [])):
    errors.append("79个无项目键路径未完整保留")

special = [
    ("src/full_only/events/NSB_Poland.txt", "CBIO_POL_karl_albrecht_desc", 1),
    ("src/full_only/events/SEA_Japan.txt", "CBIO_PHI_jose_laurel_desc", 8),
    ("src/shared/common/characters/PHI.txt", "CBIO_PHI_jose_laurel_desc", 1),
]
for rel, value, expected in special:
    parsed = parse_script((ROOT / rel).read_text(encoding="utf-8-sig"), {"desc"})
    got = sum(a.value == value for a in parsed.assignments)
    if got != expected:
        errors.append(f"v130f专项数量不符: {rel} {value} {got} != {expected}")

spr = parse_script((ROOT / "src/shared/common/characters/SPR.txt").read_text(encoding="utf-8-sig"), {"desc"})
static_anarchist = [a for a in spr.assignments if a.value == '"POLITICS_ANARCHIST_COMMUNE_DESC"' and a.ancestors[-2:-1] == ("SPR_anarchist_commune",)]
if len(static_anarchist) != 1:
    errors.append(f"SPR_anarchist_commune静态desc数量不符: {len(static_anarchist)}")

goe_path = ROOT / "src/full_only/events/GOE_Raj.txt"
goe_text = goe_path.read_text(encoding="utf-8-sig")
goe = parse_script(goe_text, {"desc"})


def goe_desc_blocks(value: str):
    rows = []
    for assignment in goe.assignments:
        if assignment.value.strip('"') != value:
            continue
        blocks = [b for b in goe.blocks if b.container == "country_leader" and b.anchor <= assignment.anchor]
        if not blocks:
            continue
        block = max(blocks, key=lambda b: b.anchor)
        rows.append((goe.roots[block.anchor - 1], role_identity(goe_text, block.line)))
    return rows


nehru = goe_desc_blocks("CBIO_RAJ_GOE_jawaharlal_nehru_desc")
nehru_12 = [row for row in nehru if row[0] == "GOE_RAJ_partition.12"]
if len(nehru_12) != 1 or nehru_12[0][1].get("character") != "RAJ_GOE_jawaharlal_nehru":
    errors.append(f"尼赫鲁小传未唯一挂在 .12: {nehru_12}")
if any(root == "GOE_RAJ_partition.9" for root, _ in nehru):
    errors.append("旧事件 .9 被写入尼赫鲁小传")
jinnah = [row for row in goe_desc_blocks("CBIO_RAJ_GOE_muhammad_ali_jinnah_desc") if row[0] == "GOE_RAJ_partition.7"]
if len(jinnah) != 1 or jinnah[0][1].get("character") != "RAJ_GOE_muhammad_ali_jinnah":
    errors.append(f"真纳小传未唯一挂在自己的 .7 领袖块: {jinnah}")
mountbatten = [row for row in goe_desc_blocks("CBIO_RAJ_louis_mountbatten_desc") if row[0] == "GOE_RAJ_partition.7"]
if len(mountbatten) != 1 or mountbatten[0][1].get("character") != "RAJ_louis_mountbatten":
    errors.append(f"蒙巴顿小传未唯一挂在自己的 .7 领袖块: {mountbatten}")
gandhi_dynamic = [row for row in goe_desc_blocks("CBIO_RAJ_mahatma_mohandas_gandhi_desc") if row[0] == "GOE_RAJ_partition.7"]
if gandhi_dynamic:
    errors.append(f"甘地在完整版 .7 不应再写动态 desc: {gandhi_dynamic}")
shared_raj = parse_script((ROOT / "src/shared/common/characters/RAJ.txt").read_text(encoding="utf-8-sig"), {"desc", "name"})
shared_gandhi = [
    a for a in shared_raj.assignments
    if a.value.strip('"') == "CBIO_RAJ_mahatma_mohandas_gandhi_desc"
    and a.ancestors[-1] == "country_leader"
    and "RAJ_mahatma_mohandas_gandhi" in a.ancestors
]
if len(shared_gandhi) != 1:
    errors.append(f"甘地共享静态小传数量不符: {len(shared_gandhi)}")

for error in errors:
    print("ERROR", error)
print(f"rebuild_overlay: full_files={len(full_paths)} shared_characters={len(shared_paths)} project_desc={project_count} nonproject_desc={nonproject_count} protected={protected_count} errors={len(errors)}")
raise SystemExit(1 if errors else 0)
