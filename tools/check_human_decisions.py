from __future__ import annotations
import re
from pathlib import Path
from common import ROOT, load_json, read_utf8

line_re=re.compile(r'^\s*([^#\s][^:]*?):(?:\d+)?\s+"(.*)"\s*(?:#.*)?$')
loc={}; errors=[]
for base in (ROOT/'src/shared',ROOT/'src/full_only'):
    for p in base.rglob('*.yml'):
        for line in read_utf8(p).splitlines():
            m=line_re.match(line)
            if m: loc[m.group(1)]=m.group(2)

def require(cond,msg):
    if not cond: errors.append(msg)

require(loc.get('SHX_fu_zuoyi_desc')=='$CHI_fu_zuoyi_desc$','傅作义顾问别名未保持 SHX_fu_zuoyi_desc -> CHI_fu_zuoyi_desc')
require('CHI_fu_zuoyi_desc' in loc,'傅作义正文主键CHI_fu_zuoyi_desc缺失')
daigo=loc.get('CBIO_JAP_tadashige_daigo_desc','')
require('坤甸事件' in daigo and '1947年10月3日' in daigo and '12月6日' in daigo,'醍醐忠重v130c7人工审定正文疑似被旧稿覆盖')

protected=['EGY - Egypt.txt','ISR - Israel.txt','JOR - Jordan.txt','LEB - Lebanon.txt','LIB - Liberia.txt','PAL - Palestine.txt','SYR - Syria.txt']
for name in protected:
    require((ROOT/'src/full_only/history/countries'/name).exists(),f'受保护运行时领袖文件缺失: {name}')

pu_ref=0
for p in (ROOT/'src/full_only').rglob('*.txt'):
    pu_ref+=read_utf8(p).count('desc = MAN_aisin_gioro_puyi_desc')
require(pu_ref>=1,'完整版溥仪动态身份desc补挂缺失')

decisions=load_json(ROOT/'workbench/decisions/human_decisions.json')

# Parity: every actionable item in the machine-readable ledger must also
# appear in the human-readable ledger docs/HUMAN_DECISIONS.md.
md_path=ROOT/'docs/HUMAN_DECISIONS.md'
md=read_utf8(md_path) if md_path.exists() else ''
require(md_path.exists(),'docs/HUMAN_DECISIONS.md缺失')
for ent in decisions.get('entities',[]):
    for key in ent.get('keys',[]):
        require(key in md,f'裁定台账md未提及实体key: {key} ({ent.get("entity")})')
for group in decisions.get('protected_files',[]):
    for path in group.get('paths',[]):
        tag=Path(path).name.split(' ')[0]
        require(tag in md,f'裁定台账md未提及保护文件: {path}')

for tag,keys in decisions.get('placeholder_name_restores',{}).items():
    if tag=='decision': continue
    for key in keys:
        value=loc.get(key)
        require(value is not None,f'占位姓名恢复key缺失: {key}')
        if value is not None:
            require(not re.search(r'[\u4e00-\u9fff]',value),f'占位人物又显示中文名: {key}={value}')

for e in errors: print('ERROR',e)
print(f'human_decisions: protected_files={len(protected)} placeholder_keys={sum(len(v) for k,v in decisions.get("placeholder_name_restores",{}).items() if isinstance(v,list))} puyi_dynamic_desc_refs={pu_ref} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
