from __future__ import annotations
import hashlib
from common import ROOT, load_json

errors=[]
for target in ('lite','full'):
    expected=load_json(ROOT/f'audit/baselines/{target}_manifest.json')
    exp={r['path']:r['sha256'] for r in expected['files'] if r['path']!='descriptor.mod' and not r['path'].startswith('__outer__/')}
    got={}
    for base in [ROOT/'src/shared'] + ([ROOT/'src/full_only'] if target=='full' else []):
        for p in base.rglob('*'):
            if p.is_file() and p.name!='AGENTS.md':
                rel=p.relative_to(base).as_posix()
                got[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
    if exp!=got:
        missing=sorted(set(exp)-set(got)); extra=sorted(set(got)-set(exp)); changed=sorted(k for k in set(exp)&set(got) if exp[k]!=got[k])
        errors.append(f'{target}: missing={missing[:10]} extra={extra[:10]} changed={changed[:10]}')
    else:
        print(f'{target}: source content matches v130e baseline ({len(got)} mod files)')
for e in errors: print('ERROR',e)
raise SystemExit(1 if errors else 0)
