from __future__ import annotations
import re
from common import ROOT, read_utf8

# Entry-point integrity: AGENTS.md must carry an explicit path pointer to
# docs/CURRENT_BASELINE.md (the single version authority) and must NOT
# re-embed a version line of its own. Duplicated version snapshots in the
# entry point caused repeated drift, so the audit guards the pointer
# architecture instead of the old snapshot-equality rule.
errors=[]

baseline=read_utf8(ROOT/'docs/CURRENT_BASELINE.md')
agents=read_utf8(ROOT/'AGENTS.md')

m=re.search(r'当前版本：(\S+)',baseline)
if not m:
    errors.append('docs/CURRENT_BASELINE.md缺少“当前版本：”行')
if 'docs/CURRENT_BASELINE.md' not in agents:
    errors.append('AGENTS.md缺少指向 docs/CURRENT_BASELINE.md 的明确路径指针')
if re.search(r'当前版本\s*[:：]\s*[A-Za-z0-9]',agents):
    errors.append('AGENTS.md内嵌了版本行——版本事实只能由 docs/CURRENT_BASELINE.md 持有')

for e in errors: print('ERROR',e)
print(f'snapshot-pointer: baseline_version={m.group(1) if m else "?"} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
