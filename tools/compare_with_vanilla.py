from __future__ import annotations
import argparse
from pathlib import Path
import zipfile
from common import ROOT, changed_source_paths, find_vanilla_reference, normalize_script_without_desc, read_utf8

ap=argparse.ArgumentParser(); ap.add_argument('--require',action='store_true'); ap.add_argument('--base'); args=ap.parse_args()
changed=changed_source_paths(args.base)
full_changed=any(p.startswith('src/full_only/') for p in changed)
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

def read_vanilla(rel):
    if z:
        if rel not in names: return None
        return z.read(rel).decode('utf-8-sig')
    p=ref/rel
    if not p.exists(): return None
    return p.read_text(encoding='utf-8-sig')

for p in (ROOT/'src/full_only').rglob('*'):
    if not p.is_file() or p.name=='AGENTS.md' or p.suffix.lower()!='.txt': continue
    rel=p.relative_to(ROOT/'src/full_only').as_posix(); vanilla=read_vanilla(rel)
    if vanilla is None:
        errors.append(f'原版缺少对应文件: {rel}'); continue
    checked+=1
    mod_tokens=normalize_script_without_desc(read_utf8(p)); vanilla_tokens=normalize_script_without_desc(vanilla)
    if mod_tokens!=vanilla_tokens:
        j=next((i for i,(a,b) in enumerate(zip(mod_tokens,vanilla_tokens)) if a!=b),min(len(mod_tokens),len(vanilla_tokens)))
        errors.append(f'去除desc后仍有原版语义差异: {rel} token={j} mod={mod_tokens[j:j+8]} vanilla={vanilla_tokens[j:j+8]}')
if z: z.close()
for e in errors: print('ERROR',e)
print(f'vanilla_compare: reference={ref} checked={checked} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
