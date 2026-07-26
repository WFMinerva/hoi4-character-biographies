from __future__ import annotations
import zipfile, hashlib, json
from pathlib import Path
from common import ROOT, load_json

TARGETS={
 'lite':('china_bio_lite_v130c7_Daigo_cover_test.zip','lite_manifest.json'),
 'full':('china_bio_v130c7_Daigo_cover_test.zip','full_manifest.json')
}

def manifest_zip(p:Path):
    rows={}
    with zipfile.ZipFile(p) as z:
        for i in z.infolist():
            if i.is_dir(): continue
            parts=i.filename.split('/')
            rel='__outer__/'+i.filename if len(parts)==1 else '/'.join(parts[1:])
            data=z.read(i)
            rows[rel]=(len(data),hashlib.sha256(data).hexdigest())
    return rows

errors=[]
for target,(zipname,mname) in TARGETS.items():
    p=ROOT/'releases'/zipname
    expected=load_json(ROOT/'audit/baselines'/mname)
    exp={r['path']:(r['size'],r['sha256']) for r in expected['files']}
    got=manifest_zip(p)
    if exp!=got:
        missing=sorted(set(exp)-set(got)); extra=sorted(set(got)-set(exp)); changed=sorted(k for k in set(exp)&set(got) if exp[k]!=got[k])
        errors.append(f'{target}: missing={missing[:10]} extra={extra[:10]} changed={changed[:10]}')
    else:
        print(f'{target}: normalized content exactly matches baseline ({len(got)} files)')
for e in errors: print('ERROR',e)
raise SystemExit(1 if errors else 0)
