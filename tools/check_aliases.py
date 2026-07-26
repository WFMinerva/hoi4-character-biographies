from __future__ import annotations
from collections import defaultdict
import re
from common import ROOT, read_utf8, source_relative

line_re=re.compile(r'^\s*([^#\s][^:]*?):(?:\d+)?\s+"(.*)"\s*(?:#.*)?$')
alias_re=re.compile(r'^\$([^$]+)\$$')
by_lang=defaultdict(dict); places=defaultdict(lambda:defaultdict(list)); errors=[]; aliases=0
for base in (ROOT/'src/shared',ROOT/'src/full_only'):
    for p in base.rglob('*.yml'):
        lines=read_utf8(p).splitlines(); first=next((x.strip() for x in lines if x.strip()),'UNKNOWN:')
        lang=first[:-1] if first.endswith(':') else 'UNKNOWN'
        for no,line in enumerate(lines,1):
            m=line_re.match(line)
            if not m: continue
            key,value=m.groups(); places[lang][key].append((source_relative(p),no))
            by_lang[lang][key]=value
for lang,mapping in by_lang.items():
    graph={}
    for key,value in mapping.items():
        m=alias_re.match(value)
        if m:
            aliases+=1; target=m.group(1); graph[key]=target
            if target.startswith('CBIO_') and target not in mapping:
                errors.append(f'{lang}: CBIO别名目标缺失 {key} -> {target}')
    state={}; trail=[]
    def visit(k):
        state[k]=1; trail.append(k)
        t=graph.get(k)
        if t in graph:
            if state.get(t)==1:
                i=trail.index(t); errors.append(f'{lang}: 别名循环: {" -> ".join(trail[i:]+[t])}')
            elif state.get(t,0)==0: visit(t)
        trail.pop(); state[k]=2
    for k in graph:
        if state.get(k,0)==0: visit(k)
for e in errors: print('ERROR',e)
print(f'aliases: aliases={aliases} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
