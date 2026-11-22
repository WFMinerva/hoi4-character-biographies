from __future__ import annotations
from common import ROOT, lex_script


def instance_order_errors(text, path):
    tokens = lex_script(text)
    errors = []
    for index, token in enumerate(tokens):
        if token.quoted or token.value != "instance":
            continue
        tail = tokens[index + 1:index + 5]
        if tuple(t.value for t in tail[:2]) != ("=", "{"):
            continue
        if len(tail) != 4 or tail[2].quoted or tuple(t.value for t in tail[2:]) != ("allowed", "="):
            errors.append(f"人物定义的 instance 必须先写 allowed: {path}:{token.line}")
    return errors

errors=[]
checked=0
for base in (ROOT/'src/shared',ROOT/'src/full_only'):
    for p in base.rglob('*.txt'):
        try: text=p.read_text(encoding='utf-8-sig')
        except UnicodeDecodeError: continue
        checked+=1
        depth=0
        in_quote=False
        escaped=False
        line_no=1
        i=0
        while i < len(text):
            ch=text[i]
            if ch=='\n':
                line_no+=1
                i+=1
                continue
            if escaped:
                escaped=False
                i+=1
                continue
            if in_quote and ch=='\\':
                escaped=True
                i+=1
                continue
            if ch=='"':
                in_quote=not in_quote
                i+=1
                continue
            if not in_quote and ch=='#':
                # Skip comment through end of line.
                j=text.find('\n',i)
                if j==-1:
                    break
                i=j
                continue
            if not in_quote:
                if ch=='{':
                    depth+=1
                elif ch=='}':
                    depth-=1
                    if depth<0:
                        errors.append(f'多余右括号: {p.relative_to(ROOT)}:{line_no}')
                        depth=0
            i+=1
        if in_quote:
            errors.append(f'字符串引号未闭合: {p.relative_to(ROOT)}')
        if depth!=0:
            errors.append(f'大括号不平衡({depth}): {p.relative_to(ROOT)}')
        if p.relative_to(base).parts[:2] == ("common", "characters"):
            errors.extend(instance_order_errors(text, p.relative_to(ROOT)))
for e in errors: print('ERROR',e)
print(f'structure: checked={checked} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
