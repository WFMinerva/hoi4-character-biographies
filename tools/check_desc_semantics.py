from __future__ import annotations
from common import ROOT, iter_desc_assignments, read_utf8, source_relative

STATIC_ROLES={'country_leader','advisor','corps_commander','field_marshal','navy_leader','scientist'}
DYNAMIC_DIRECT={'add_corps_commander_role','add_field_marshal_role','add_navy_leader_role'}
CREATE_DIRECT={'create_country_leader','create_corps_commander','create_field_marshal','create_navy_leader'}
errors=[]; checked=0; relevant=0

for base in (ROOT/'src/shared',ROOT/'src/full_only'):
    for p in base.rglob('*.txt'):
        try: text=read_utf8(p)
        except UnicodeDecodeError: continue
        checked+=1
        for line,value,stack in iter_desc_assignments(text):
            relevant_context=False; valid=True; reason=''
            if 'characters' in stack:
                relevant_context=True
                if not any(role in stack for role in STATIC_ROLES):
                    valid=False; reason='characters树内desc不在已知身份块中（可能插入了注释身份或人物顶层）'
            if 'add_country_leader_role' in stack:
                relevant_context=True
                idx=len(stack)-1-stack[::-1].index('add_country_leader_role')
                if 'country_leader' not in stack[idx+1:]:
                    valid=False; reason='add_country_leader_role的desc必须位于内部country_leader块'
            for cmd in DYNAMIC_DIRECT|CREATE_DIRECT:
                if cmd in stack:
                    relevant_context=True
            if relevant_context:
                relevant+=1
                if not valid:
                    errors.append(f'{source_relative(p)}:{line}: {reason}; value={value}; path={" > ".join(stack[-8:])}')
for e in errors: print('ERROR',e)
print(f'desc_semantics: files={checked} relevant_desc={relevant} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
