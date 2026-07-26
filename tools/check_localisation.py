from __future__ import annotations
from pathlib import Path
import re, collections
from common import ROOT

key_re=re.compile(r'^\s*([^#\s][^:]*?):(?:\d+)?\s+"')
cbio_ref_re=re.compile(r'\bdesc\s*=\s*(CBIO_[A-Za-z0-9_.-]+)')
# A localisation key may legitimately exist once per language. Duplicates are checked inside the same language only.
keys_by_language=collections.defaultdict(lambda: collections.defaultdict(list))
all_keys=set()
errors=[]
loc_files=[]
for base in (ROOT/'src/shared', ROOT/'src/full_only'):
    for p in base.rglob('*.yml'):
        loc_files.append(p)
        text=p.read_text(encoding='utf-8-sig')
        lines=text.splitlines()
        first=next((x.strip() for x in lines if x.strip()),'')
        if not first.startswith('l_') or not first.endswith(':'):
            errors.append(f'语言头异常: {p.relative_to(ROOT)}: {first!r}')
            language='UNKNOWN'
        else:
            language=first[:-1]
        for no,line in enumerate(lines,1):
            m=key_re.match(line)
            if m:
                key=m.group(1)
                keys_by_language[language][key].append((p.relative_to(ROOT).as_posix(),no))
                all_keys.add(key)
            elif line.strip() and not line.lstrip().startswith('#') and not line.strip().startswith('l_'):
                errors.append(f'非法本地化行: {p.relative_to(ROOT)}:{no}: {line[:100]}')

for language,mapping in keys_by_language.items():
    for k,places in mapping.items():
        if len(places)>1:
            errors.append(f'{language}重复key {k}: {places}')

# This repository intentionally does not contain all vanilla localisation.
# Only CBIO-owned desc references are required to resolve inside the mod.
refs=[]
for base in (ROOT/'src/shared',ROOT/'src/full_only'):
    for p in base.rglob('*.txt'):
        try: text=p.read_text(encoding='utf-8-sig')
        except UnicodeDecodeError: continue
        for m in cbio_ref_re.finditer(text):
            refs.append((m.group(1),p.relative_to(ROOT).as_posix()))
missing=collections.defaultdict(list)
for key,path in refs:
    if key not in all_keys:
        missing[key].append(path)
for key,paths in missing.items():
    errors.append(f'CBIO desc引用缺少MOD本地化 {key}: {sorted(set(paths))[:5]}')

for e in errors: print('ERROR',e)
print(f'localisation: files={len(loc_files)} languages={len(keys_by_language)} keys={len(all_keys)} cbio_desc_refs={len(refs)} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
