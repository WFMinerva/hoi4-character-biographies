from __future__ import annotations
from collections import Counter
from common import ROOT, iter_source_files, load_json, source_relative

BOM=b"\xef\xbb\xbf"
BINARY_SUFFIXES={'.png','.jpg','.jpeg','.gif','.dds','.tga','.zip','.xlsx','.xls'}
errors=[]; warnings=[]; counts=Counter()
baseline_path=ROOT/'audit/baselines/encoding_baseline.json'
baseline={r['path']:r for r in load_json(baseline_path)['files']} if baseline_path.exists() else {}

for p in iter_source_files():
    rel=source_relative(p); data=p.read_bytes(); suffix=p.suffix.lower()
    if suffix in BINARY_SUFFIXES:
        counts['binary']+=1; continue
    if data.startswith((b"\xff\xfe",b"\xfe\xff")):
        errors.append(f'UTF-16禁止: {rel}'); continue
    if b'\x00' in data:
        errors.append(f'NUL字符: {rel}')
    try:
        text=data.decode('utf-8-sig')
    except UnicodeDecodeError as e:
        errors.append(f'UTF-8解码失败: {rel}: {e}'); continue
    if any(ch in text for ch in ('\u200b','\u200c','\u200d','\ufeff')):
        # Leading BOM is consumed by utf-8-sig; remaining FEFF is embedded.
        errors.append(f'零宽或嵌入BOM字符: {rel}')
    has_bom=data.startswith(BOM)
    if suffix=='.yml' and '/localisation/' in '/'+rel:
        if not has_bom: errors.append(f'本地化YML缺少UTF-8 BOM: {rel}')
    elif rel in baseline:
        expected=bool(baseline[rel]['utf8_bom'])
        if has_bom!=expected:
            errors.append(f'BOM状态偏离v130c7基线: {rel}: expected={expected} got={has_bom}')
    elif suffix in {'.txt','.mod'} and has_bom:
        warnings.append(f'新脚本文件带BOM，请确认有意为之: {rel}')
    crlf=data.count(b'\r\n'); lf=data.count(b'\n'); lone_lf=lf-crlf
    if crlf and lone_lf:
        errors.append(f'混合换行: {rel}')
    style='crlf' if crlf else 'lf'
    if rel in baseline and baseline[rel].get('line_ending') not in (None,'none',style):
        errors.append(f'换行风格偏离v130e基线: {rel}: expected={baseline[rel]["line_ending"]} got={style}')
    counts[suffix or '<none>']+=1
for x in warnings: print('WARN',x)
for x in errors: print('ERROR',x)
print(f'encoding: checked={sum(counts.values())} errors={len(errors)} warnings={len(warnings)}')
raise SystemExit(1 if errors else 0)
