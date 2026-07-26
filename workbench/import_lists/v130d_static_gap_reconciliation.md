# v130d 静态身份覆盖对账报告

生成时间：2026-07-26。对账脚本：`workbench/v130d_reconcile.py`（只读 `src/`、`audit/`、`docs/`、`workbench/decisions/`，不修改任何源码）。
明细表：`workbench/import_lists/v130d_static_gap_reconciliation.csv`（6421 行，UTF-8 BOM）。
机器汇总：`workbench/import_lists/_v130d_reconcile_summary.json`。

> **行动纪律：本报告所有"疑似真人漏写""待人工裁定"均为机器候选，不是确认结论，更不是确认 BUG。任何条目必须经人工裁定（真人 / C类 / 占位 / 备用身份 / 是否实际显示）后才可动笔或入包。**

## 1. 对账口径

- **底账**：`audit/data/v130a-2_静态身份全量表.xlsx` 主表 6421 条静态身份实例（人物 × 身份类型 × direct/instance 路径），基准为 HOI4 v1.19.2 原版 + v129o 精简版 + v129n 完整版。
- **当前覆盖来源**（脚本实测）：
  - `src/shared` + `src/full_only` 全部 `.txt` 中 characters 树内的 `desc` 引用，解析逻辑复用 `tools/common.py` 的 `iter_desc_assignments`（与 `tools/check_desc_semantics.py` 同一解析器），共 4205 条引用、3216 个去重 desc 键、167 个角色文件；`full_only` 中无 characters 树内 desc（其增量全在动态脚本，与 v130a 结论一致）。
  - 简中本地化：`src/shared/localisation/simp_chinese/` 与 `replace/simp_chinese/` 共 83 个 yml、7388 个键，其中 720 个为 `$主键$` 形式别名键；别名递归解析到主键，主键有正文即算覆盖。
  - 自检：3216 个 characters 树内 desc 键全部能解析到非空简中正文（缺失数 0），与"当前审计口径 desc 引用全部有效"一致。
- **覆盖判定粒度**：人物 key × 身份代码。同类序号 k 对齐到当前 MOD 文件内该人物该身份第 k 个带 desc 的角色块（与底账"同类序号按文件顺序"的定义一致）；直接挂在人物顶层的 desc 视为覆盖该人物全部身份。允许 `instance` 包装块（如 `has_dlc` 条件块）内的身份角色被正确识别。
- **逐条分类规则**（保守，拿不准一律进"待人工裁定"）：
  - `已覆盖`：当前有有效 desc 且键有正文（含别名复用）。
  - `已裁定不写-占位`：人物 key 命中 `workbench/decisions/human_decisions.json` 的 36 个占位键（SHX 15 + MEN 11 + MAN 10；不写小传、恢复拉丁原名）。
  - `已裁定不写-科学家`：身份代码为 scientist 且无人工例外（当前无任何科学家例外记录）。
  - `已裁定不写-C类非领袖`：**本轮 0 条**。v130a-2 底账与 v130a-1d（JSON/XLSX）均无逐条 C 类机器分类，按任务约定无底账支撑则不使用此类别。
  - `疑似真人漏写`：未覆盖、不属以上类别，且有佐证——有中文显示名，或（有拉丁显示名 且 身份为 country_leader/field_marshal/corps_commander/navy_leader 重要身份）。
  - `待人工裁定`：其余未覆盖（显示名即裸 key、疑为 generic/C类/备用身份，但无机器分类支撑）。
- **优先级排序**：TAG 分档——档1 中国相关（CHI/PRC/SHX/SIK/YUN/MEN/MAN/XSM/TIB/GXC）+ 日本（JAP），档2 苏德英美意法（SOV/GER/ENG/USA/ITA/FRA），档3 其余；档内按角色 country_leader > field_marshal > corps_commander > navy_leader > advisor 排序。

## 2. 分类统计（全部为脚本实测数字）

| 当前分类 | 行数 | 占 6421 |
|---|---|---|
| 已覆盖 | 4205 | 65.5% |
| 已裁定不写-占位 | 37（涉及 36 个 key，1 个 key 有两条身份） | 0.6% |
| 已裁定不写-科学家 | 43 | 0.7% |
| 已裁定不写-C类非领袖 | 0（无底账支撑，见口径） | 0% |
| 疑似真人漏写 | 557 | 8.7% |
| 待人工裁定 | 1579 | 24.6% |
| **缺口合计（非"已覆盖"）** | **2216** | 34.5% |

按身份类型交叉：

| 身份 | 总数 | 已覆盖 | 占位 | 科学家 | 疑似真人漏写 | 待人工裁定 |
|---|---|---|---|---|---|---|
| country_leader | 774 | 660 | 7 | 0 | 107 | 0 |
| field_marshal | 135 | 131 | 0 | 0 | 4 | 0 |
| corps_commander | 785 | 752 | 0 | 0 | 19 | 14 |
| navy_leader | 165 | 153 | 0 | 0 | 10 | 2 |
| advisor | 4459 | 2449 | 30 | 0 | 417 | 1563 |
| scientist | 103 | 60 | 0 | 43 | 0 | 0 |

## 3. 与 v130a 摘要的差异解释

v130a 时点：有效 4193 / 身份存在但无desc 1115 / 身份未覆盖 1113 / desc缺本地化 0。本轮转移矩阵（实测）：

| v130a 状态 | → 已覆盖 | → 占位 | → 科学家 | → 疑似真人漏写 | → 待人工裁定 |
|---|---|---|---|---|---|
| 有效 (4193) | 4193 | 0 | 0 | 0 | 0 |
| 身份存在但无desc (1115) | 12 | 37 | 43 | 518 | 505 |
| 身份未覆盖 (1113) | 0 | 0 | 0 | 39 | 1074 |

要点：

- **零回归**：v130a 时 4193 条有效身份当前全部仍为已覆盖。
- **v130c1—c7 后静态侧新增覆盖仅 12 条**（PRC/CHI 顾问与将领等）。这不与"c 批次新增大量正文"矛盾：c 批次正文主要落在①既有 desc 键的正文补齐与改写、②别名键复用（当前 720 个别名键）、③完整版动态脚本路径（不在本静态表统计单位内）、④占位人物姓名去汉化。静态角色文件集合仍为 167 个，与 v129o 相同，因此"身份未覆盖"的 1113 条无一转为覆盖——它们对应的国家/人物文件本来就没有新增。
- 1113 条"身份未覆盖"当前去向：39 条疑似真人漏写 + 1074 条待人工裁定，仍全部属于覆盖范围外待办，不是稳定版回归。

## 4. 疑似真人漏写：数量与地区分布（机器候选，共 557 条）

优先级档分布：档1（中国相关+日本）191 条，档2（苏德英美意法）2 条，档3（其余）364 条。

档1 TAG 分布：PRC 86、CHI 80、GXC 6、XSM 5、SIK 4、MAN 4、YUN 3、SHX 2、MEN 1、JAP 0。
档2 仅 2 条：ENG `ENG_horatio_dundas`（country_leader）、ITA `ITA_grand_council`（country_leader）。
档3 主要 TAG：PHI 47、URG 39、SWE 26、ICE 22、PER 18、SPR 16、IRQ 12、SWI 11、AFG 11、MON 10、BUL 10、CHL 8、SAF 8 等。

角色分布：advisor 417、country_leader 107、corps_commander 19、navy_leader 10、field_marshal 4。

示例（CSV 中按优先级排序，此处为前排样例）：

- 档1 领袖类：`GXC_li_ting`（Li Ting）、`GXC_liu_peng`（Liu Peng）、`SIK_kwong_jin`（Kwong Jin）、`XSM_hsia_jin`（Hsia Jin）、`YUN_cheng_peng`（Cheng Peng）等——**注意这一批与已裁定的 36 个占位人物命名模式高度相似（拉丁拼音通用名），很可能是同族 generic/C类人物，占位裁定的扩候选，必须人工核实**。
- 档1 有中文名的真实人物候选：`CHI_chen_cheng`（陈诚）、`CHI_bai_chongxi`（白崇禧）等的 advisor 身份（其领袖/将领身份已覆盖，仅顾问身份未挂 desc）。
- 档3 有中文名候选：`ALB_eqrem_belishi`（埃奇雷姆·贝利希，country_leader）、`BOL_severino_ruiztagle`（塞韦里诺·鲁伊斯-塔格莱，country_leader）、`CHL_domingo_blanco`（多明戈·布兰科，country_leader）等。

## 5. 探查 xlsx 时的重要口径注意事项

1. **统计单位是"人物 × 身份 × direct/instance 路径"**，不是人物。6421 行中 1096 行为 instance 路径（DLC/条件化实例），底账字段说明明确"不要合并不同 instance 行"。同一个人物可占多行（如 `URG_alfredo_baldomir` 的 advisor 有 instance[1]/instance[2] 两行）。
2. **"原版desc"列 6421 行全部为空**（v1.19.2 原版这些身份均未挂 desc）。因此任务设想中的"有原版 POLITICS_*_DESC 引用"佐证在底账里不存在，本轮"疑似"佐证只用了中文名/拉丁名/重要身份三项。
3. **同类序号按文件顺序**，同一人物同一身份最多 4 个同类块（多意识形态领袖）。本对账按同序对齐 MOD 文件内第 k 个带 desc 角色块；若人工裁定要精确到意识形态，需回看源文件行号（CSV 保留了原版角色文件列）。
4. **精简版与完整版静态身份覆盖完全一致**（两列状态逐行相同），完整版增量全在动态脚本路径；静态缺口只需修一次。
5. **底账"项目口径"列只有两种取值**：纳入身份审计（6318）/ 科学家默认不写小传（103）。底账和 v130a-1d 均不含逐条"真人/C类"机器分类——C类判断本来就是人工工作台职责，这就是"已裁定不写-C类非领袖"本轮为 0 条的原因。
6. **底账状态列是机器判定**，其字段说明与审计备注自带免责："身份未覆盖属于覆盖范围外待办，不直接视为稳定版 BUG"、"身份存在但无desc 必须人工分类后再修"。本报告沿用同一纪律。
7. **MOD 人物 key 可能与原版 key 不同**：例如原版 `URG_alfredo_baldomir`（advisor 行）在 MOD 中对应人物定义为 `URG_alfredo_baldomir_ferrari`（已有正文 `CBIO_URG_alfredo_baldomir_ferrari_desc`）。按 key 严格对齐会把这类记为缺口；保守起见仍列入"疑似真人漏写"，人工裁定时应优先排查 key 改名/身份归属，避免重复写传。
8. 43 条科学家未覆盖行在 v130a 备注中即标注"按当前项目规则默认不作为人物小传缺口"，与"科学家默认不写"裁定一致；另有 60 条科学家身份在 v130a 前就已挂有效 desc，保持不动。

## 6. 产出文件

- `workbench/import_lists/v130d_static_gap_reconciliation.csv`——6421 行逐条明细：分类、依据、当前 desc 键、优先级档、角色优先级，按（分类 → 档 → 角色 → TAG → key）排序。
- `workbench/import_lists/_v130d_reconcile_summary.json`——机器汇总指标（本报告全部数字的来源）。
- `workbench/v130d_reconcile.py`——可重跑的对账脚本。

**再次声明：以上"疑似真人漏写"与"待人工裁定"共 2136 条均为机器候选清单，任何条目在人工裁定前不得写成确认 BUG、不得直接注入 desc。**
