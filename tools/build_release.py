from __future__ import annotations
import argparse, shutil, zipfile, hashlib, json, re
from pathlib import Path
from common import ROOT, find_vanilla_reference, iter_source_files, load_json

def documented_version() -> str:
    path = ROOT / "docs/CURRENT_BASELINE.md"
    version = re.search(r"^\s*- 当前版本：(\S+)", path.read_text(encoding="utf-8-sig"), re.M)
    if not version or not re.fullmatch(r"v[0-9]+[a-z0-9]*", version[1]):
        raise ValueError("基准卡缺少有效当前版本")
    return version[1]


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
    stem = "china_bio_lite" if target == "lite" else "china_bio"
    if not version:
        raise ValueError("--version 必填，除非使用 --baseline")
    root_name = f"{stem}_{version}"
    outer_name = f"{root_name}.mod"
    build_root=ROOT/'build'/target
    if build_root.exists(): shutil.rmtree(build_root)
    mod_root=build_root/root_name
    mod_root.mkdir(parents=True)
    copy_tree(ROOT/'src/shared',mod_root)
    if target=='full': copy_tree(ROOT/'src/full_only',mod_root)
    desc=(ROOT/f'packaging/{target}/descriptor.mod').read_bytes()
    outer=(ROOT/f'packaging/{target}/outer.mod').read_bytes()
    if not baseline:
        desc=rewrite_descriptor(desc,root_name,root_name)
        outer=rewrite_descriptor(outer,root_name,root_name)
    (mod_root/'descriptor.mod').write_bytes(desc)
    (build_root/outer_name).write_bytes(outer)
    releases=ROOT/'releases'; releases.mkdir(exist_ok=True)
    zip_name=root_name+'.zip'
    zip_path=releases/zip_name
    if zip_path.exists(): zip_path.unlink()
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(build_root.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(build_root).as_posix())
    digest=hashlib.sha256(zip_path.read_bytes()).hexdigest()
    print(f'{target}: {zip_path} sha256={digest}')
    return zip_path, digest, root_name, outer_name

def write_baseline_manifest(target:str,root_name:str,outer_name:str,zip_path:Path)->dict:
    rows=[]
    with zipfile.ZipFile(zip_path) as z:
        for i in sorted(z.infolist(),key=lambda x:x.filename):
            if i.is_dir(): continue
            parts=i.filename.split('/')
            rel='__outer__/'+i.filename if len(parts)==1 else '/'.join(parts[1:])
            data=z.read(i)
            rows.append({'path':rel,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    manifest={'root':root_name,'outer_mod':outer_name,'file_count':len(rows),'files':rows}
    out=ROOT/'audit'/'baselines'/f'{target}_manifest.json'
    out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'{target}: manifest -> {out} ({len(rows)} files)')
    return manifest

def write_baseline_summary(version: str, infos: dict, game_version: str):
    lite=infos['lite']; full=infos['full']
    lp={f['path']:f['sha256'] for f in lite['manifest']['files']}
    fp={f['path']:f['sha256'] for f in full['manifest']['files']}
    common=sorted(set(lp)&set(fp)); diff=[p for p in common if lp[p]!=fp[p]]
    lite_only=sorted(set(lp)-set(fp)); full_only=sorted(set(fp)-set(lp))
    summary={
     'baseline':version,
     'game_version':game_version,
     'normalized_comparison':{
       'common_paths':len(common),
       'same_content_paths':len(common)-len(diff),
       'different_common_paths':diff,
       'lite_only_paths':lite_only,
       'full_only_paths_count':len(full_only),
       'full_only_mod_files_count':len([p for p in full_only if not p.startswith('__outer__/')]),
     },
     'lite_zip':{'filename':lite['zip'].name,'sha256':lite['digest'],'root':lite['manifest']['root'],'files':lite['manifest']['file_count']},
     'full_zip':{'filename':full['zip'].name,'sha256':full['digest'],'root':full['manifest']['root'],'files':full['manifest']['file_count']},
    }
    out=ROOT/'audit'/'baselines'/'baseline_summary.json'
    out.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'baseline summary -> {out}')

def write_encoding_baseline(version: str) -> None:
    rows = []
    for p in sorted(iter_source_files(), key=lambda p: ("shared" not in p.relative_to(ROOT).parts[:2], p)):
        if p.suffix.lower() not in {".txt", ".yml"}:
            continue
        data = p.read_bytes()
        style = "crlf" if b"\r\n" in data else "lf" if b"\n" in data else "none"
        rows.append({
            "path": p.relative_to(ROOT).as_posix(),
            "utf8_bom": data.startswith(b"\xef\xbb\xbf"),
            "line_ending": style,
        })
    path = ROOT / "audit/baselines/encoding_baseline.json"
    path.write_text(json.dumps({"baseline": f"{version}-stable", "files": rows},
                               ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline',action='store_true')
    ap.add_argument('--version')
    ap.add_argument('--targets',default='lite,full')
    args=ap.parse_args()
    targets = [t.strip() for t in args.targets.split(",") if t.strip()]
    version = args.version
    if args.baseline:
        if len(targets) != 2 or set(targets) != {"lite", "full"}:
            ap.error("--baseline 必须同时构建 lite 与 full")
        if args.version is not None:
            ap.error("--baseline 从基准卡读取版本，无需 --version")
        version = documented_version()
        reference = find_vanilla_reference()
        if reference is None or not (reference / "launcher-settings.json").is_file():
            ap.error("--baseline 需要已核实的原版安装目录及游戏版本")
        game_version = load_json(reference / "launcher-settings.json")["rawVersion"]
        major, minor, *_ = game_version.split(".")
        metadata = {f'supported_version="{major}.{minor}.*"'}
        for target in targets:
            stem = "china_bio_lite" if target == "lite" else "china_bio"
            root_name = f"{stem}_{version}"
            expected = metadata | {f'name="{root_name}"', f'path="mod/{root_name}"'}
            for filename in ("descriptor.mod", "outer.mod"):
                path = ROOT / "packaging" / target / filename
                if not expected <= set(path.read_text(encoding="utf-8-sig").splitlines()):
                    ap.error(f"基准打包元数据不匹配: {path}")
    if not version:
        ap.error("--version 必填，除非使用 --baseline")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]*", version):
        ap.error("无效版本名")
    infos = {}
    for target in targets:
        if target not in {"lite", "full"}:
            ap.error(f"未知构建目标: {target}")
        zip_path, digest, root_name, outer_name = build(target,version,args.baseline)
        if args.baseline:
            manifest=write_baseline_manifest(target,root_name,outer_name,zip_path)
            infos[target]={"zip":zip_path,"digest":digest,"manifest":manifest}
    if args.baseline:
        write_baseline_summary(version, infos, game_version)
        write_encoding_baseline(version)


if __name__=='__main__': main()
