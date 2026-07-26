from __future__ import annotations
import argparse
import subprocess
import sys
from common import ROOT

ap=argparse.ArgumentParser(); ap.add_argument('--base'); ap.add_argument('--require-vanilla',action='store_true'); args=ap.parse_args()
checks=[
 ('check_encoding.py',[]),
 ('check_localisation.py',[]),
 ('check_aliases.py',[]),
 ('check_text_quality.py',[]),
 ('check_human_decisions.py',[]),
 ('check_script_structure.py',[]),
 ('check_desc_semantics.py',[]),
 ('check_diff_whitelist.py',(['--base',args.base] if args.base else [])),
 ('compare_with_vanilla.py',(['--base',args.base] if args.base else [])+(['--require'] if args.require_vanilla else [])),
]
failed=[]
for script,extra in checks:
    print(f'\n=== {script} ===')
    r=subprocess.run([sys.executable,str(ROOT/'tools'/script),*extra],cwd=ROOT)
    if r.returncode!=0: failed.append(script)
print('\n=== DAILY AUDIT SUMMARY ===')
if failed:
    print('FAILED:',', '.join(failed)); raise SystemExit(1)
print('ALL DAILY STATIC CHECKS PASSED')
