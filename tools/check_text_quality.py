from __future__ import annotations
import re
from common import ROOT, read_utf8, source_relative

line_re=re.compile(r'^\s*([^#\s][^:]*?):(?:\d+)?\s+"(.*)"\s*(?:#.*)?$')
residue_patterns=[
    (re.compile(r'(^|[：:])\s*自检\s*'), '自检残留'),
    (re.compile(r'§[Y!GRTB]'), '审稿/颜色标记'),
    (re.compile(r'```|---option'), 'Markdown或写作块残留'),
    (re.compile(r'^(资料来源|参考资料|Sources?|Source)\s*[：:]'), '来源说明残留'),
]
errors=[]; warnings=[]; bios=0
for base in (ROOT/'src/shared',ROOT/'src/full_only'):
    for p in base.rglob('*.yml'):
        for no,line in enumerate(read_utf8(p).splitlines(),1):
            m=line_re.match(line)
            if not m: continue
            key,value=m.groups()
            if value=='': errors.append(f'空本地化正文: {source_relative(p)}:{no}: {key}')
            if not key.endswith('_desc'): continue
            if value.startswith('$') and value.endswith('$'): continue
            bios+=1
            for rx,label in residue_patterns:
                if rx.search(value): errors.append(f'{label}: {source_relative(p)}:{no}: {key}')
            if '\n' in value or '\r' in value:
                errors.append(f'正文包含转义换行: {source_relative(p)}:{no}: {key}')
            if len(value)>500:
                warnings.append(f'正文超过500字符，需人工确认: {key} len={len(value)} ({source_relative(p)}:{no})')
for x in warnings[:10]: print('WARN',x)
if len(warnings)>10: print(f'WARN ... 另有{len(warnings)-10}条历史长文，仅提示不阻断')
for e in errors: print('ERROR',e)
print(f'text_quality: biographies={bios} errors={len(errors)} warnings={len(warnings)}')
raise SystemExit(1 if errors else 0)
