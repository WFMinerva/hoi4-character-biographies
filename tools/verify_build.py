from __future__ import annotations
import argparse, zipfile, hashlib, json
from pathlib import Path
from common import ROOT, load_json
from build_release import rewrite_descriptor

TARGETS={
 'lite':('china_bio_lite_v130e.zip','lite_manifest.json'),
 'full':('china_bio_v130e.zip','full_manifest.json')
}

def manifest_zip(p:Path):
    rows={}
    with zipfile.ZipFile(p) as z:
        for i in z.infolist():
            if i.is_dir(): continue
            parts=i.filename.split('/')
            rel='__outer__/'+i.filename if len(parts)==1 else '/'.join(parts[1:])
            data=z.read(i)
            if rel in rows: raise ValueError(f'duplicate normalized ZIP path: {rel}')
            rows[rel]=(len(data),hashlib.sha256(data).hexdigest())
    return rows

def source_manifest(target:str,version:str):
    rows={}
    sources=[ROOT/'src/shared']
    if target=='full': sources.append(ROOT/'src/full_only')
    for source in sources:
        for p in source.rglob('*'):
            if p.is_file() and p.name!='AGENTS.md':
                data=p.read_bytes()
                rows[p.relative_to(source).as_posix()]=(len(data),hashlib.sha256(data).hexdigest())
    stem='china_bio_lite' if target=='lite' else 'china_bio'
    name=f'{stem}_{version}'
    for filename in ('descriptor.mod','outer.mod'):
        data=rewrite_descriptor((ROOT/f'packaging/{target}'/filename).read_bytes(),name,name)
        rel='descriptor.mod' if filename=='descriptor.mod' else f'__outer__/{name}.mod'
        rows[rel]=(len(data),hashlib.sha256(data).hexdigest())
    return rows

def semantic_manifest_check(path:Path):
    data=path.read_bytes()
    document=json.loads(data)
    files=document['files']; unchanged=document['unchanged']
    rows={r['path']:r['expected_sha256'] for r in files}|{r['path']:r['sha256'] for r in unchanged}
    payload=json.dumps(rows,sort_keys=True,separators=(',',':')).encode('utf-8')
    if hashlib.sha256(payload).hexdigest()!=document['semantic_manifest_sha256']:
        raise ValueError('semantic_manifest_sha256与清单内容不符')
    for row in files:
        source=ROOT/row['path']
        if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest()!=row['expected_sha256']:
            raise ValueError(f"语义清单与当前源码不符: {row['path']}")
    for row in unchanged:
        source=ROOT/row['path']
        if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError(f"不动文件与语义清单不符: {row['path']}")
    return hashlib.sha256(data).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--version')
    ap.add_argument('--semantic-manifest',type=Path)
    args=ap.parse_args()
    errors=[]
    if args.semantic_manifest:
        try:
            digest=semantic_manifest_check(args.semantic_manifest)
            print(f'semantic manifest: {args.semantic_manifest} sha256={digest}; bound to current sources')
        except (OSError,UnicodeDecodeError,json.JSONDecodeError,KeyError,TypeError,ValueError) as e:
            errors.append(f'semantic manifest: {e}')
    for target,(baseline_zip,mname) in TARGETS.items():
        if args.version is not None:
            stem='china_bio_lite' if target=='lite' else 'china_bio'
            zipname=f'{stem}_{args.version}.zip'
            exp=source_manifest(target,args.version)
            source='current sources'
        else:
            zipname=baseline_zip
            expected=load_json(ROOT/'audit/baselines'/mname)
            exp={r['path']:(r['size'],r['sha256']) for r in expected['files']}
            source='baseline'
        p=ROOT/'releases'/zipname
        try:
            got=manifest_zip(p)
        except (OSError,zipfile.BadZipFile,ValueError) as e:
            errors.append(f'{target}: {e}')
            continue
        if exp!=got:
            missing=sorted(set(exp)-set(got)); extra=sorted(set(got)-set(exp)); changed=sorted(k for k in set(exp)&set(got) if exp[k]!=got[k])
            errors.append(f'{target}: missing={missing[:10]} extra={extra[:10]} changed={changed[:10]}')
        else:
            print(f'{target}: normalized content exactly matches {source} ({len(got)} files)')
    for e in errors: print('ERROR',e)
    return 1 if errors else 0

if __name__=='__main__':
    raise SystemExit(main())
