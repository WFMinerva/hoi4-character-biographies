# -*- coding: utf-8 -*-
"""v130d 静态身份覆盖对账：v130a-2 全量表(6421行) × 当前 src 覆盖 × 人工裁定。
只读 src/ audit/ docs/ reference/ workbench/decisions；产出到 workbench/import_lists/。
"""
from __future__ import annotations
import sys, re, json, csv
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from common import iter_desc_assignments, read_utf8  # noqa: E402
import openpyxl  # noqa: E402

STATIC_ROLES = {"country_leader", "advisor", "corps_commander", "field_marshal", "navy_leader", "scientist"}

# ---------- 1. 读取 v130a-2 全量表 ----------
wb = openpyxl.load_workbook(ROOT / "audit/data/v130a-2_静态身份全量表.xlsx", read_only=True)
ws = wb["静态身份全量表"]
raw = list(ws.iter_rows(values_only=True))
COLS = list(raw[2])
rows = [dict(zip(COLS, r)) for r in raw[3:]]
assert len(rows) == 6421, len(rows)

# ---------- 2. 当前源码：characters 树内 desc 引用 ----------
# cov[(char_key, role)] = [(file, line, desc_key), ...] 按文件+行号排序
cov = defaultdict(list)
char_level_desc = defaultdict(list)  # char_key -> [desc_key] 直接挂在人物顶层的 desc
desc_refs_total = 0
char_files = set()
for base in (ROOT / "src/shared", ROOT / "src/full_only"):
    for p in sorted(base.rglob("*.txt")):
        try:
            text = read_utf8(p)
        except UnicodeDecodeError:
            continue
        rel = p.relative_to(ROOT).as_posix()
        for line, value, stack in iter_desc_assignments(text):
            if "characters" not in stack:
                continue
            idx = stack.index("characters")
            if idx + 1 >= len(stack):
                continue
            char_key = stack[idx + 1]
            # 允许 instance/allowed 等包装块：在人物块之下寻找第一个已知身份角色
            role = None
            for tok in stack[idx + 2:]:
                if tok in STATIC_ROLES:
                    role = tok
                    break
            desc_refs_total += 1
            char_files.add(rel)
            if role is None:
                char_level_desc[char_key].append((rel, line, value))
            else:
                cov[(char_key, role)].append((rel, line, value))
for k in cov:
    cov[k].sort()

# ---------- 3. 当前源码：简中本地化键（普通 + replace） ----------
LOC_RE = re.compile(r'^\s*([A-Za-z0-9_.\-]+):(\d+)?\s*"(.*)"\s*$')
loc_values = {}   # key -> raw value（后读覆盖先读；replace 目录后读）
loc_files = 0
for locdir in (ROOT / "src/shared/localisation/simp_chinese",
               ROOT / "src/shared/localisation/replace/simp_chinese"):
    for p in sorted(locdir.rglob("*.yml")):
        loc_files += 1
        for ln in read_utf8(p).splitlines():
            m = LOC_RE.match(ln)
            if m:
                loc_values[m.group(1)] = m.group(3)

ALIAS_RE = re.compile(r"^\$([A-Za-z0-9_.\-]+)\$$")
def resolve_text(key, depth=0):
    """返回 (是否有正文, 解析链)。别名 $KEY$ 指向主键算覆盖。"""
    if key not in loc_values or depth > 5:
        return (False, key)
    v = loc_values[key].strip()
    m = ALIAS_RE.match(v)
    if m:
        ok, chain = resolve_text(m.group(1), depth + 1)
        return (ok, f"{key}->{chain}")
    return (len(v) > 0, key)

alias_keys = sum(1 for v in loc_values.values() if ALIAS_RE.match(v.strip()))

# ---------- 4. 人工裁定 ----------
hd = json.loads((ROOT / "workbench/decisions/human_decisions.json").read_text(encoding="utf-8"))
placeholder = set()
for tag, lst in hd["placeholder_name_restores"].items():
    if isinstance(lst, list):
        placeholder.update(lst)
human_exceptions = set()  # 已裁定的真人例外（科学家/C类不适用，仅记录）
for e in hd.get("entities", []):
    human_exceptions.update(e.get("keys", []))

# ---------- 5. 逐条对账 ----------
CJK_RE = re.compile(r"[一-鿿]")
TIER1 = {"CHI","PRC","SHX","SIK","YUN","MEN","MAN","XSM","TIB","GXC","JAP"}
TIER2 = {"SOV","GER","ENG","USA","ITA","FRA"}
ROLE_RANK = {"country_leader":0,"field_marshal":1,"corps_commander":2,"navy_leader":3,"advisor":4,"scientist":5}

def cur_coverage(r):
    """返回 (是否覆盖, 当前desc键, 解析链/原因)"""
    ck, role, k = r["人物key"], r["身份代码"], r["同类序号"] or 1
    cands = list(cov.get((ck, role), []))
    for f, ln, v in char_level_desc.get(ck, []):
        cands.append((f, ln, v))
    if not cands:
        return (False, "", "当前源码该人物+身份无desc")
    pick = cands[min(k - 1, len(cands) - 1)]
    ok, chain = resolve_text(pick[2])
    if ok:
        return (True, pick[2], chain)
    return (False, pick[2], f"desc已挂但简中正文缺失: {chain}")

results = []
for r in rows:
    covered, desc_key, note = cur_coverage(r)
    ck, role, tag = r["人物key"], r["身份代码"], r["国家Tag"]
    disp = r["简中显示名"] or ""
    has_cjk = bool(CJK_RE.search(disp))
    named = disp != ck  # 有独立显示名（非裸key）
    important = role in ("country_leader", "field_marshal", "corps_commander", "navy_leader")
    evid = []
    if has_cjk: evid.append("有中文显示名")
    if named and not has_cjk: evid.append("有拉丁显示名")
    if important: evid.append(f"重要身份({role})")
    if covered:
        cat, basis = "已覆盖", f"当前desc={desc_key}; 正文链={note}"
    elif ck in placeholder:
        cat, basis = "已裁定不写-占位", "命中 human_decisions.json placeholder_name_restores（占位不写，恢复拉丁原名）"
    elif role == "scientist":
        cat, basis = "已裁定不写-科学家", "项目规则：科学家默认不写；无人工例外记录"
    else:
        # C类非领袖：v130a-2 底账与 v130a-1d 均无逐条机器分类支撑，不使用该类别
        if has_cjk or (important and named):
            cat = "疑似真人漏写"
            basis = "机器候选，佐证: " + ("; ".join(evid) if evid else "无")
        else:
            cat = "待人工裁定"
            basis = "无明确佐证（疑为C类/generic/备用身份，无机器分类支撑，需人工判断）"
    tier = 1 if tag in TIER1 else (2 if tag in TIER2 else 3)
    results.append({
        "序号": r["序号"], "国家Tag": tag, "人物key": ck, "简中显示名": disp,
        "身份代码": role, "身份路径": r["身份路径"], "同类序号": r["同类序号"],
        "意识形态": r["意识形态"] or "", "顾问槽位": r["顾问槽位"] or "",
        "v130a状态": r["精简版状态"], "当前分类": cat,
        "当前desc": desc_key, "分类依据": basis,
        "优先级档": tier, "角色优先级": ROLE_RANK.get(role, 9),
        "原版角色文件": r["原版角色文件"] or "",
    })

CAT_ORDER = {"疑似真人漏写":0,"待人工裁定":1,"已裁定不写-占位":2,"已裁定不写-科学家":3,"已裁定不写-C类非领袖":4,"已覆盖":5}
results.sort(key=lambda x: (CAT_ORDER[x["当前分类"]], x["优先级档"], x["角色优先级"], x["国家Tag"], x["人物key"]))

# ---------- 6. 统计 ----------
stats = Counter(x["当前分类"] for x in results)
gap = [x for x in results if x["当前分类"] != "已覆盖"]
gap_sus = [x for x in gap if x["当前分类"] == "疑似真人漏写"]
sus_tier = Counter(x["优先级档"] for x in gap_sus)
sus_role = Counter(x["身份代码"] for x in gap_sus)
sus_tag = Counter(x["国家Tag"] for x in gap_sus)
# 与 v130a 对比：当时两类非有效行现在的去向
trans = Counter((x["v130a状态"], x["当前分类"]) for x in results)
# 当前 desc 引用有效性自检
all_desc_keys = {v for lst in cov.values() for _,_,v in lst} | {v for lst in char_level_desc.values() for _,_,v in lst}
bad_desc = [k for k in sorted(all_desc_keys) if not resolve_text(k)[0]]

summary = {
    "rows": len(results),
    "stats": dict(stats),
    "gap_total": len(gap),
    "suspected_real_missing": len(gap_sus),
    "suspected_by_tier": {str(k): v for k, v in sorted(sus_tier.items())},
    "suspected_by_role": dict(sus_role.most_common()),
    "suspected_top_tags": dict(sus_tag.most_common(15)),
    "transition_from_v130a": {f"{a} -> {b}": n for (a, b), n in sorted(trans.items())},
    "current_char_desc_refs": desc_refs_total,
    "current_char_desc_keys": len(all_desc_keys),
    "current_char_files_with_desc": len(char_files),
    "loc_files": loc_files,
    "loc_keys": len(loc_values),
    "loc_alias_keys": alias_keys,
    "desc_keys_missing_loc": bad_desc,
    "placeholder_keys": len(placeholder),
}
(ROOT / "workbench/import_lists/_v130d_reconcile_summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------- 7. CSV ----------
out = ROOT / "workbench/import_lists/v130d_static_gap_reconciliation.csv"
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    w.writeheader()
    w.writerows(results)

print(json.dumps(summary, ensure_ascii=False, indent=2))
print("CSV ->", out)
