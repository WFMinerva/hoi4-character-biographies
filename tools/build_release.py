from __future__ import annotations
import argparse, shutil, zipfile, hashlib, json, re
from pathlib import Path
from common import ROOT

BASELINE={
 'lite': {'root':'china_bio_lite_v130e','outer':'china_bio_lite_v130e.mod'},
 'full': {'root':'china_bio_v130e','outer':'china_bio_v130e.mod'},
}

def copy_tree(src:Path,dst:Path):
    for p in src.rglob('*'):
        if p.is_file() and p.name!='AGENTS.md':
            q=dst/p.relative_to(src)
            q.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,q)

def rewrite_descriptor(data:bytes,name:str,root_name:str)->bytes:
    text=data.decode('utf-8-sig')
    text=re.sub(r'^name="[^"]*"',f'name="{name}"',text,flags=re.M)
    text=re.sub(r'^path="mod/[^"]*"',f'path="mod/{root_name}"',text,flags=re.M)
    return text.encode('utf-8')

def build(target:str,version:str|None,baseline:bool):
    meta=BASELINE[target]
    if baseline:
        root_name=meta['root']; outer_name=meta['outer']; display=root_name
    else:
        if not version: raise ValueError('--version必填，除非使用--baseline')
        stem='china_bio_lite' if target=='lite' else 'china_bio'
        root_name=f'{stem}_{version}'
        outer_name=f'{root_name}.mod'
        display=root_name
    build_root=ROOT/'build'/target
    if build_root.exists(): shutil.rmtree(build_root)
    mod_root=build_root/root_name
    mod_root.mkdir(parents=True)
    copy_tree(ROOT/'src/shared',mod_root)
    if target=='full': copy_tree(ROOT/'src/full_only',mod_root)
    desc=(ROOT/f'packaging/{target}/descriptor.mod').read_bytes()
    outer=(ROOT/f'packaging/{target}/outer.mod').read_bytes()
    if not baseline:
        desc=rewrite_descriptor(desc,display,root_name)
        outer=rewrite_descriptor(outer,display,root_name)
    (mod_root/'descriptor.mod').write_bytes(desc)
    (build_root/outer_name).write_bytes(outer)
    releases=ROOT/'releases'; releases.mkdir(exist_ok=True)
    zip_name=(meta['root'] if baseline else root_name)+'.zip'
    zip_path=releases/zip_name
    if zip_path.exists(): zip_path.unlink()
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(build_root.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(build_root).as_posix())
    digest=hashlib.sha256(zip_path.read_bytes()).hexdigest()
    print(f'{target}: {zip_path} sha256={digest}')
    return zip_path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline',action='store_true')
    ap.add_argument('--version')
    ap.add_argument('--targets',default='lite,full')
    args=ap.parse_args()
    for t in args.targets.split(','):
        t=t.strip()
        if t: build(t,args.version,args.baseline)
if __name__=='__main__': main()
