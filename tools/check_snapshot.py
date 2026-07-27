from __future__ import annotations
import re
from common import ROOT, read_utf8

# Snapshot consistency: the static snapshot in AGENTS.md must carry a date
# and the same version as docs/CURRENT_BASELINE.md, so a stale entry point
# is caught by the daily audit instead of misleading the next session.
errors=[]

baseline=read_utf8(ROOT/'docs/CURRENT_BASELINE.md')
agents=read_utf8(ROOT/'AGENTS.md')

m=re.search(r'当前版本：(\S+)',baseline)
if not m:
    errors.append('docs/CURRENT_BASELINE.md缺少“当前版本：”行')
snap=re.search(r'## 0\.1.*?(?=\n## )',agents,re.S)
if not snap:
    errors.append('AGENTS.md缺少“## 0.1”状态快照节')
if m and snap:
    version=m.group(1)
    section=snap.group(0)
    sm=re.search(r'当前版本：([A-Za-z0-9._-]+)',section)
    if not sm:
        errors.append('AGENTS.md快照缺少“当前版本：”行')
    elif not sm.group(1).startswith(version):
        errors.append(f'AGENTS.md快照版本与基准卡不一致: 基准卡={version} 快照={sm.group(1)}')
    if not re.search(r'\d{4}-\d{2}-\d{2}',section):
        errors.append('AGENTS.md快照缺少日期（YYYY-MM-DD）')

for e in errors: print('ERROR',e)
print(f'snapshot: version={m.group(1) if m else "?"} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
