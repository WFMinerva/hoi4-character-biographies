# -*- coding: utf-8 -*-
"""v130d 档1疑似真人漏写（中国相关TAG+日本，191条）人工裁定表生成。
只读 src/ audit/ workbench/decisions 与既有对账 CSV；产出到 workbench/import_lists/。
"""
from __future__ import annotations
import sys, re, json, csv, difflib
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from common import iter_desc_assignments, read_utf8  # noqa: E402

STATIC_ROLES = {"country_leader", "advisor", "corps_commander", "field_marshal", "navy_leader", "scientist"}
CJK_RE = re.compile(r"[一-鿿]")

# ---------- 当前源码覆盖（与 v130d_reconcile 同口径） ----------
cov = defaultdict(list)
char_level = defaultdict(list)
for base in (ROOT / "src/shared", ROOT / "src/full_only"):
    for p in sorted(base.rglob("*.txt")):
        try:
            text = read_utf8(p)
        except UnicodeDecodeError:
            continue
        for line, value, stack in iter_desc_assignments(text):
            if "characters" not in stack:
                continue
            idx = stack.index("characters")
            if idx + 1 >= len(stack):
                continue
            ck = stack[idx + 1]
            role = None
            for tok in stack[idx + 2:]:
                if tok in STATIC_ROLES:
                    role = tok
                    break
            if role is None:
                char_level[ck].append(value)
            else:
                cov[(ck, role)].append(value)

LOC_RE = re.compile(r'^\s*([A-Za-z0-9_.\-]+):(\d+)?\s*"(.*)"\s*$')
loc = {}
for locdir in (ROOT / "src/shared/localisation/simp_chinese",
               ROOT / "src/shared/localisation/replace/simp_chinese"):
    for p in sorted(locdir.rglob("*.yml")):
        for ln in read_utf8(p).splitlines():
            m = LOC_RE.match(ln)
            if m:
                loc[m.group(1)] = m.group(3)

ALIAS_RE = re.compile(r"^\$([A-Za-z0-9_.\-]+)\$$")
def resolve(key, depth=0):
    """-> (有正文?, 终端key, 是否经别名)"""
    if key not in loc or depth > 5:
        return (False, key, False)
    v = loc[key].strip()
    m = ALIAS_RE.match(v)
    if m:
        ok, end, _ = resolve(m.group(1), depth + 1)
        return (ok, end, True)
    return (len(v) > 0, key, False)

# 已覆盖人物 key 集合（任一身份有有效 desc）
covered = {}
for (ck, role), vals in cov.items():
    for v in vals:
        ok, end, via = resolve(v)
        if ok:
            covered.setdefault(ck, (v, end, via))
for ck, vals in char_level.items():
    for v in vals:
        ok, end, via = resolve(v)
        if ok:
            covered.setdefault(ck, (v, end, via))

# ---------- 占位家族命名模式 ----------
SURNAMES = {"li","liu","zhang","wang","chen","zhao","sun","ma","huang","zhou","wu","xu","zhu",
            "guo","he","luo","han","lin","deng","liang","song","tang","feng","yu","dong","xiao",
            "cheng","cao","yuan","fu","shen","zeng","peng","lu","su","jiang","cai","jia","ding",
            "wei","xue","yan","duan","lei","hou","long","shi","tao","gu","shao","wan","qian",
            "dai","xia","hsia","kwong","hsia","mao","liao","kong","tan","yang","zhu","min","qu"}
PY_SYL = re.compile(r"^(zh|ch|sh|hs|kw|ts|tz|[bpmfdtnlgkhjqxrzcsyw])?[a-zü]{1,6}$")
def placeholder_family(key: str, disp: str) -> bool:
    """与已裁定36个占位人物同族的拉丁拼音通用名：TAG_后2-3个拼音音节、含常见姓、无连字符。"""
    if CJK_RE.search(disp) or "-" in disp:
        return False
    toks = key.split("_", 1)[1].split("_") if "_" in key else []
    if not (2 <= len(toks) <= 3):
        return False
    if not all(PY_SYL.match(t) for t in toks):
        return False
    return toks[0] in SURNAMES or any(t in SURNAMES for t in toks)

# ---------- 读取对账 CSV 的档1疑似行 ----------
rows = list(csv.DictReader(open(ROOT / "workbench/import_lists/v130d_static_gap_reconciliation.csv", encoding="utf-8-sig")))
t1 = [r for r in rows if r["当前分类"] == "疑似真人漏写" and r["优先级档"] == "1"]
assert len(t1) == 191, len(t1)

# ---------- 逐条机器初判 ----------
def suffix(key):
    return key.split("_", 1)[1] if "_" in key else key

def find_similar_covered(key):
    """仅接受两种高置信匹配，宁缺毋滥：
    a) 跨 TAG 同后缀精确匹配（如 SHX_fu_zuoyi → CHI_fu_zuoyi；但跨TAG同后缀也可能是同名不同人，依据中须提示）；
    b) 前缀/改名关系（如 URG_alfredo_baldomir → URG_alfredo_baldomir_ferrari）。
    返回 (key, 方式) 或 None。"""
    s = suffix(key)
    for ck in covered:
        if ck == key:
            continue
        if suffix(ck) == s:
            return (ck, "跨TAG同后缀" if ck.split("_", 1)[0] != key.split("_", 1)[0] else "同后缀")
    best = None
    for ck in covered:
        if ck == key:
            continue
        if ck.startswith(key + "_") or key.startswith(ck + "_"):
            if best is None or len(ck) < len(best):
                best = ck
    if best:
        return (best, "前缀/改名")
    return None

out = []
for r in t1:
    key, tag, role = r["人物key"], r["国家Tag"], r["身份代码"]
    # 当前显示名：MOD 本地化优先，否则底账原版简中名
    if key in loc and not ALIAS_RE.match(loc[key].strip()):
        disp, src = loc[key], "MOD本地化"
    else:
        disp, src = r["简中显示名"], "原版简中底账"
    name_type = "中文名" if CJK_RE.search(disp) else "拉丁名"

    notes = []
    # 同键其他身份已有正文？
    if key in covered:
        dkey, end, via = covered[key]
        chain = f"{dkey}→{end}" if via else dkey
        notes.append(f"同键其他身份已挂有效desc（{chain}，正文已存在），仅本身份未挂")
    # 类似正文键？（同键命名规律的 desc 正文是否已存在于本地化）
    for cand in (f"{key}_desc", f"CBIO_{key}_desc"):
        if cand in loc:
            ok, end, via = resolve(cand)
            if ok:
                chain = f"{cand}→{end}" if via else cand
                notes.append(f"本地化中已存在可用正文键 {chain}")
            break

    if placeholder_family(key, disp):
        verdict = "疑似占位"
        basis = "拉丁拼音通用名，命名模式与已裁定36个占位人物同族"
    elif src == "MOD本地化" and name_type == "拉丁名":
        # 已进入MOD名称覆盖白名单恢复拉丁名，但不满足占位家族模式（如有连字符）——保守归为真人候选
        verdict = "疑似真人"
        basis = "有拉丁显示名且身份重要；注意：MOD名称覆盖白名单已将其恢复拉丁名（此前批次按未核实人物处理过名字），需人工核对是否真人"
    else:
        sim = find_similar_covered(key)
        if sim:
            sk, how = sim
            dkey, end, via = covered[sk]
            verdict = "疑似key改名"
            basis = f"当前源码存在已覆盖人物 {sk}（desc={dkey}，匹配方式：{how}），疑为同一人跨TAG或改名"
            if how == "跨TAG同后缀":
                basis += "；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份"
        else:
            verdict = "疑似真人"
            basis = "有中文显示名" if name_type == "中文名" else "有拉丁显示名且身份重要"
    if verdict == "疑似占位" and src == "MOD本地化":
        basis += "；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理）"
    if notes:
        basis += "；" + "；".join(notes)

    out.append({
        "底账序号": r["序号"], "TAG": tag, "人物key": key, "身份角色": role,
        "身份路径": r["身份路径"], "同类序号": r["同类序号"], "顾问槽位": r["顾问槽位"],
        "当前显示名": disp, "名类型": name_type, "显示名来源": src,
        "机器初判": verdict, "初判依据": basis, "人工裁定": "",
    })

TAG_ORDER = ["CHI", "PRC", "GXC", "MAN", "MEN", "SHX", "SIK", "XSM", "YUN", "JAP"]
ROLE_RANK = {"country_leader": 0, "field_marshal": 1, "corps_commander": 2, "navy_leader": 3, "advisor": 4}
out.sort(key=lambda x: (TAG_ORDER.index(x["TAG"]) if x["TAG"] in TAG_ORDER else 99,
                        ROLE_RANK.get(x["身份角色"], 9), x["人物key"]))
for i, o in enumerate(out, 1):
    o2 = {"序号": i}
    o2.update(o)
    out[i - 1] = o2

stats = Counter(o["机器初判"] for o in out)
bio_exists = sum(1 for o in out if "本地化中已存在可用正文键" in o["初判依据"])
same_key = sum(1 for o in out if "同键其他身份已挂有效desc" in o["初判依据"])
print("初判分布:", dict(stats))
print("其中：本地化已有可用正文键", bio_exists, "；同键其他身份已覆盖", same_key)
per_tag = Counter((o["TAG"], o["机器初判"]) for o in out)
for k, v in sorted(per_tag.items()):
    print(k, v)

csvp = ROOT / "workbench/import_lists/v130d_tier1_ruling_sheet.csv"
with csvp.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)
print("CSV ->", csvp)

# ---------- Markdown 可读版 ----------
def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")

md = []
md.append("# v130d 档1疑似漏写人工裁定表（中国相关TAG + 日本，191条）")
md.append("")
md.append("> **声明：本表\"机器初判\"仅供参考，不构成确认结论；最终以人工裁定为准。裁定结果经用户确认后，由维护流程登记进 `workbench/decisions/human_decisions.json`。**")
md.append("")
md.append("来源：`v130d_static_gap_reconciliation.csv` 中 557 条\"疑似真人漏写\"的优先级档1部分（CHI/PRC/GXC/MAN/MEN/SHX/SIK/XSM/YUN/JAP）。生成脚本：`workbench/v130d_tier1_ruling.py`。配套 CSV：`v130d_tier1_ruling_sheet.csv`（列更全，含底账序号、顾问槽位）。")
md.append("")
md.append("## 使用说明")
md.append("")
md.append("- 在每条末尾的**裁定栏**填写四选一：`写传` / `占位去汉化` / `已覆盖-键改名` / `不写-其他`（可加简短备注）。")
md.append("- **191 条中 177 条本地化里已有现成正文键**（依据列注明\"本地化中已存在可用正文键\"）：这些通常**不需要新写正文**，裁定的实质是\"是否把已有正文挂到该身份\"或\"不写\"。真正没有任何现成正文的仅 14 条（全部为拉丁显示名的 GXC/SIK/XSM/YUN 通用名人物）。")
md.append("- 机器初判三类的含义：")
md.append("  - `疑似占位`：拉丁拼音通用名，命名模式与已裁定 36 个占位人物同族，且 MOD 名称覆盖白名单已恢复其拉丁名；候选处理方式是\"占位去汉化\"而非写传。")
md.append("  - `疑似key改名`：当前源码存在同后缀跨 TAG 或前缀/改名关系的已覆盖人物；**跨 TAG 同后缀也可能是同名不同人**（典型：陈仪 CHI_chen_yi / 陈毅 PRC_chen_yi），裁定前必须核对人物身份。")
md.append("  - `疑似真人`：其余，多为有中文显示名的顾问身份。")
md.append("- 排序：按 TAG 分组（CHI、PRC、GXC、MAN、MEN、SHX、SIK、XSM、YUN、JAP），组内按身份重要度（country_leader > field_marshal > corps_commander > navy_leader > advisor）再按人物 key 字母序。")
md.append("- 同一人物多条 instance/同类序号行不合并（与底账口径一致）；裁定可逐行打勾，也可对同一人批量同判。")
md.append("")
md.append("## 机器初判统计")
md.append("")
md.append("| 机器初判 | 条数 |")
md.append("|---|---|")
for k in ("疑似真人", "疑似占位", "疑似key改名"):
    md.append(f"| {k} | {stats.get(k, 0)} |")
md.append(f"| 合计 | {sum(stats.values())} |")
md.append("")
md.append(f"补充信号：本地化已有现成正文键 {sum(1 for o in out if '本地化中已存在可用正文键' in o['初判依据'])} 条；同键其他身份已覆盖（正文已存在，仅本身份未挂）{sum(1 for o in out if '同键其他身份已挂有效desc' in o['初判依据'])} 条。")
md.append("")
md.append("## 裁定表")
md.append("")
cur_tag = None
for o in out:
    if o["TAG"] != cur_tag:
        cur_tag = o["TAG"]
        md.append(f"### {cur_tag}")
        md.append("")
        md.append("| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |")
        md.append("|---|---|---|---|---|---|---|---|")
    role = o["身份角色"] + (f"/{o['顾问槽位']}" if o["顾问槽位"] else "")
    path = o["身份路径"] + (f"#{o['同类序号']}" if o["同类序号"] not in ("1", 1) else "")
    md.append("| " + " | ".join([
        str(o["序号"]), f"`{o['人物key']}`", role, path,
        f"{esc(o['当前显示名'])}（{o['名类型']}）", o["机器初判"], esc(o["初判依据"]), "",
    ]) + " |")
    nxt = out[out.index(o) + 1] if out.index(o) + 1 < len(out) else None
    if nxt is None or nxt["TAG"] != cur_tag:
        md.append("")
mdp = ROOT / "workbench/import_lists/v130d_tier1_ruling_sheet.md"
mdp.write_text("\n".join(md) + "\n", encoding="utf-8")
print("MD ->", mdp)

# 需要特别注意的条目：拉丁名但被判疑似真人 / 占位家族边界
print("--- 边界条目 ---")
for o in out:
    if o["名类型"] == "拉丁名" and o["机器初判"] != "疑似占位":
        print("拉丁名非占位初判:", o["TAG"], o["人物key"], o["当前显示名"], o["机器初判"])
(ROOT / "workbench/import_lists/_v130d_tier1_ruling_stats.json").write_text(
    json.dumps({"stats": dict(stats), "per_tag": {f"{a}|{b}": n for (a, b), n in sorted(per_tag.items())}},
               ensure_ascii=False, indent=2), encoding="utf-8")
