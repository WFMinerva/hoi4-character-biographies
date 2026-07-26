from __future__ import annotations
import argparse
import fnmatch
from pathlib import Path
import re
from common import ROOT, changed_source_paths, git_available, load_json, resolve_diff_base, run_git

FORBIDDEN=re.compile(r'\b(ideology|traits?|skill|attack_skill|defense_skill|planning_skill|logistics_skill|cost|allowed|available|visible|trigger|ai_will_do|complete_effect|hidden_effect|immediate|option|add_political_power|set_country_leader_ideology|recruit_character|promote_character)\b\s*=')
DESC_ONLY=re.compile(r'^\s*desc\s*=')
COMMENT_OR_BLANK=re.compile(r'^\s*(?:#.*)?$')

def load_exceptions():
    p=ROOT/'audit/allowlists/diff_exceptions.json'
    return load_json(p).get('exceptions',[]) if p.exists() else []

def permitted(path,line,exceptions):
    for ex in exceptions:
        if not ex.get('approved_by_user',False): continue
        if fnmatch.fnmatch(path,ex.get('path','')):
            patterns=ex.get('allowed_regex',[])
            if ex.get('allow_all') or any(re.search(rx,line) for rx in patterns): return True
    return False

def check_semantic_line(path,line,exceptions,errors,prefix=''):
    if path.endswith(('.yml','.png')): return
    if COMMENT_OR_BLANK.match(line) or DESC_ONLY.match(line): return
    if permitted(path,line,exceptions): return
    if FORBIDDEN.search(line): errors.append(f'{prefix}禁止字段变化: {path}: {line[:180]}')
    else: errors.append(f'{prefix}脚本非desc变化未获批准: {path}: {line[:180]}')

ap=argparse.ArgumentParser(); ap.add_argument('--base'); args=ap.parse_args()
if not git_available():
    print('diff_whitelist: SKIP（尚未初始化Git；首次迁移请运行verify_initial_baseline.py）')
    raise SystemExit(0)
base=resolve_diff_base(args.base); errors=[]; exceptions=load_exceptions(); changed=set(changed_source_paths(args.base))
cp=run_git(['diff','--unified=0','--no-ext-diff',base,'--','src'])
current=''
for raw in cp.stdout.splitlines():
    if raw.startswith('+++ b/'):
        current=raw[6:]; continue
    if raw.startswith('--- ') or raw.startswith('@@') or raw.startswith('diff --git') or raw.startswith('index ') or raw.startswith('new file mode') or raw.startswith('deleted file mode'): continue
    if not current or not raw.startswith(('+','-')): continue
    check_semantic_line(current,raw[1:],exceptions,errors)
tracked_diff=set(x.strip() for x in run_git(['diff','--name-only',base,'--','src']).stdout.splitlines() if x.strip())
for path in sorted(changed-tracked_diff):
    p=ROOT/path
    if not p.exists() or p.is_dir() or path.endswith(('.yml','.png')): continue
    try: lines=p.read_text(encoding='utf-8-sig').splitlines()
    except UnicodeDecodeError:
        errors.append(f'未跟踪源码无法按UTF-8检查: {path}'); continue
    for line in lines:
        check_semantic_line(path,line,exceptions,errors,prefix='未跟踪文件：')
for e in errors: print('ERROR',e)
print(f'diff_whitelist: base={base} changed_files={len(changed)} errors={len(errors)}')
raise SystemExit(1 if errors else 0)
