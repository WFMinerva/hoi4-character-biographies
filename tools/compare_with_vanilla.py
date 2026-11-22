from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import zipfile
from common import (ROOT, changed_source_paths, find_vanilla_reference,
                    normalize_script_without_desc, read_utf8, resolve_diff_base, sha256_bytes)
from rebase_evidence import baseline_game_version, load_rebase_document, rebase_version, validated_rebases, vanilla_semantics_errors

ap=argparse.ArgumentParser(); ap.add_argument('--require',action='store_true'); ap.add_argument('--base'); args=ap.parse_args()
changed=changed_source_paths(args.base)
full_changed=any(p.startswith(('src/full_only/', 'src/shared/common/characters/')) for p in changed)
ref=find_vanilla_reference()
if ref is None:
    if args.require or full_changed:
        print('ERROR 完整版源码已变化，但未配置原版参考。复制reference/vanilla_path.example.json为vanilla_path.json，或设置HOI4_VANILLA_PATH。')
        raise SystemExit(1)
    print('vanilla_compare: SKIP（full_only未变化且未配置原版参考）')
    raise SystemExit(0)

errors=[]; checked=0
z=None
if ref.is_file():
    try: z=zipfile.ZipFile(ref)
    except zipfile.BadZipFile:
        print(f'ERROR 原版参考不是有效ZIP: {ref}'); raise SystemExit(1)
    names=set(z.namelist())

def read_vanilla_bytes(rel):
    if z:
        return z.read(rel) if rel in names else None
    p=ref/rel
    return p.read_bytes() if p.is_file() else None

document = load_rebase_document()
version = rebase_version(document) or baseline_game_version()
base = resolve_diff_base(args.base)
rebases, rebase_errors = validated_rebases(base, changed, document.get("exceptions", []))
errors.extend(rebase_errors)
localization_keys = set()
if version or rebases:
    for loc in (ROOT / "src/shared/localisation").rglob("*.yml"):
        localization_keys.update(re.findall(r'^\s+([^\s:#]+):\d*\s+"', read_utf8(loc), re.M))
if version:
    launcher = read_vanilla_bytes("launcher-settings.json")
    actual = json.loads(launcher.decode("utf-8-sig")).get("rawVersion") if launcher else None
    if actual != version:
        errors.append(f"版本重建原版版本不符: {actual} != {version}")
    major, minor, *_ = version.split(".")
    expected_support = f'supported_version="{major}.{minor}.*"'
    for target in ("lite", "full"):
        for filename in ("descriptor.mod", "outer.mod"):
            metadata = ROOT / "packaging" / target / filename
            if not metadata.is_file() or expected_support not in read_utf8(metadata).splitlines():
                errors.append(f"打包声明与重建版本不符: {metadata.relative_to(ROOT)}")

for source, expected_vanilla in sorted(rebases.items()):
    rel = source.split("/", 2)[2]
    vanilla = read_vanilla_bytes(rel)
    if vanilla is None or sha256_bytes(vanilla) != expected_vanilla:
        errors.append(f'版本重建原版SHA256不同或缺少参考: {rel}')
    else:
        errors.extend(vanilla_semantics_errors(base, source, vanilla, localization_keys))
        checked += (ROOT / source).is_file()

scripts = list((ROOT / "src/full_only").rglob("*.txt"))
if version:
    scripts.extend((ROOT / "src/shared/common/characters").glob("*.txt"))
for p in scripts:
    if not p.is_file() or p.name=='AGENTS.md' or p.suffix.lower()!='.txt': continue
    source = p.relative_to(ROOT).as_posix()
    if source in rebases: continue
    rel=source.split("/", 2)[2]; vanilla=read_vanilla_bytes(rel)
    if vanilla is None:
        errors.append(f'原版缺少对应文件: {rel}'); continue
    checked+=1
    if version:
        errors.extend(vanilla_semantics_errors(base, source, vanilla, localization_keys))
        continue
    mod_tokens=normalize_script_without_desc(read_utf8(p)); vanilla_tokens=normalize_script_without_desc(vanilla.decode('utf-8-sig'))
    if mod_tokens!=vanilla_tokens:
        j=next((i for i,(a,b) in enumerate(zip(mod_tokens,vanilla_tokens)) if a!=b),min(len(mod_tokens),len(vanilla_tokens)))
        errors.append(f'去除desc后仍有原版语义差异: {rel} token={j} mod={mod_tokens[j:j+8]} vanilla={vanilla_tokens[j:j+8]}')
if z: z.close()
for e in errors: print('ERROR',e)
print(f'vanilla_compare: reference={ref} checked={checked} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
