from __future__ import annotations
import argparse
import subprocess
import sys
from common import ROOT, load_json
from rebase_evidence import load_rebase_document, rebase_version

ap=argparse.ArgumentParser(); ap.add_argument('--base'); ap.add_argument('--require-vanilla',action='store_true'); ap.add_argument('--skip-vanilla',action='store_true'); args=ap.parse_args()
checks=[
 ('check_encoding.py',[]),
 ('check_localisation.py',[]),
 ('check_aliases.py',[]),
 ('check_text_quality.py',[]),
 ('check_human_decisions.py',[]),
 ('check_snapshot.py',[]),
 ('check_script_structure.py',[]),
 ('check_desc_semantics.py',[]),
 ('check_diff_whitelist.py',(['--base',args.base] if args.base else [])),
]
if not args.skip_vanilla:
    # 以下检查器依赖原版参考（CI 无游戏文件，--skip-vanilla 时整体跳过）
    checks.append(('check_rebuild_whitespace.py',(['--base',args.base] if args.base else [])))
    checks.append(('compare_with_vanilla.py',(['--base',args.base] if args.base else [])+(['--require'] if args.require_vanilla else [])))
    manifest = ROOT / "audit/allowlists/rebuild_manifest.json"
    version = rebase_version(load_rebase_document())
    historical_version = load_json(manifest)["game_version"] if manifest.is_file() else None
    if version and historical_version and version != historical_version:
        print(f"重建快照 {historical_version} 适用于旧版本，本轮由原版比对验证 {version} 候选。", flush=True)
    else:
        checks.append(('check_rebuild_overlay.py',[]))
failed=[]
for script,extra in checks:
    print(f'\n=== {script} ===')
    r=subprocess.run([sys.executable,str(ROOT/'tools'/script),*extra],cwd=ROOT)
    if r.returncode!=0: failed.append(script)
print('\n=== DAILY AUDIT SUMMARY ===')
if failed:
    print('FAILED:',', '.join(failed)); raise SystemExit(1)
print('ALL DAILY STATIC CHECKS PASSED')
