# 钢四人物小传MOD：总入口与强制维护规则

本文件是仓库总入口。任何接手者先读本文件的快照、待办、目录地图和阅读顺序，再按任务深入对应文档。

## 0.1 当前状态快照（2026-08-20）

> 时效提醒：本节负责当前工作状态和待办，可能过期。稳定版本和发布物以`docs/CURRENT_BASELINE.md`为准，语义裁定以人工裁定台账为准；先核对`git log`/`git status`，冲突时标记为“待验证”并更新对应事实源，不得让历史文档反向覆盖。

- 当前版本：v130e-stable（兼容版`china_bio_lite_v130e.zip` + 完整版`china_bio_v130e.zip`），用户实机确认德国女皇线在完整版1936剧本中正常上台并显示审定小传，是当前稳定基准；2026-07-30已上传Steam工坊（兼容版物品`3736859636`，完整版物品`3762643540`）。
- 游戏版本口径：HOI4 1.19.x（原版参考已配置于`reference/vanilla_path.json`，指向1.19.2）。
- 测试口径：1936、1939剧本。
- v130d相对v130c7的变更：傅作义SHX顾问/溥仪MAN理论家补挂desc别名；蒋有芬（SIK）、韩乙奴（XSM）核实为真人，恢复中文名并入审定小传；完成6421条静态身份覆盖对账（档1已结案）。
- v130e相对v130d的变更：德国女皇线`GER_victoria`已确认是威廉二世独女维多利亚·路易丝，旧正文误写为威廉二世之妹；修订正文已于2026-07-30经用户逐字审定，并在完整版1936剧本动态上台路径中实机确认显示正常。兼容版仅包含正文，不覆盖该动态事件，因此不负责此路径的小传显示。
- 工作区状态：档1复核结论已提交（档1全部结案）；`workbench/pending_text/`为空，无待审正文。
- 2026-08-20 维护者换机接手（Codex 维护机 → 本机）：落地文档体系——新增`docs/maintenance/`（三级流程、开发交接快照、机主开工手册）与`docs/testing/`（实机归档、黄金存档制度）及配套`tools/check_logs_cbio.py`；MOD 源码零变化。详见`docs/maintenance/开发状态快照与交接.md`。

### 0.1.1 事实源职责与证据等级

- 根 `AGENTS.md`：当前工作状态、待办、范围和授权边界。
- `docs/CURRENT_BASELINE.md`：稳定版本、双包文件名、哈希、文件数和转正条件。
- `docs/HUMAN_DECISIONS.md` + `workbench/decisions/human_decisions.json`：已确认语义裁定和长期例外。
- `docs/archive/`、机器底库、历史报告：只提供历史或候选证据，不得覆盖前三者。
- 结论必须区分：**文件确认**、**静态确认**、**日志确认**、**实机确认**、**用户确认**、**稳定基准**、**已接受限制**、**未覆盖**和**待验证**。低等级证据不能替代高等级证据；机器候选尤其不能直接升级为确认 BUG。

## 0.2 当前待办（按优先级）

1. 静态身份对账收尾（未排期，需用户发起）：档3共364条、待裁定区1579条尚未裁定，底账见`workbench/import_lists/`。**口径警告**：底账未计入顾问`<idea_token>_desc`自动显示路径（档1曾因此全部误报），推进前必须先按该路径重新核，见`docs/ENGINEERING_PLAYBOOK.md`第4节。
2. HOI4发布新游戏版本时：以新原版文件为底重建`src/full_only/`全部覆盖（规则见第9节、`docs/KNOWN_RISKS.md`第1条），并重新跑全量审计。
3. 兼容版1939剧本动态领袖缺口（毛泽东NCNS线、德王、乔巴山）：已裁定不修复，仅登记，见`docs/KNOWN_RISKS.md`第9条。

## 0.3 目录地图

| 路径 | 用途 | 能不能动 |
| --- | --- | --- |
| `src/shared/` | 两版本共同MOD源码（255文件） | 受第5/6节约束，改动须过审计；先读`src/shared/AGENTS.md` |
| `src/full_only/` | 完整版动态路径覆盖（207文件） | 高风险，先读`src/full_only/AGENTS.md`和第9节 |
| `packaging/lite/`、`packaging/full/` | 两版本包元数据（descriptor/outer.mod） | 版本号变更时才动 |
| `tools/` | 审计/构建/校验脚本 | 可维护，先读`tools/AGENTS.md`；默认只读、不得静默改src |
| `audit/baselines/` | v130e基线manifest与编码基线 | 机器生成，只由`build_release.py --baseline`重建 |
| `audit/allowlists/` | 非desc差异临时例外登记 | 按第6节流程逐任务登记 |
| `audit/data/` | v130a—v130b历史机器底库（约37MB） | 只读参考资料，不得当作确认BUG |
| `audit/reports/` | 审计报告输出目录 | 工具写入 |
| `workbench/` | 人工工作台（待审/审定正文、裁定、对账底账） | 日常工作区，见`workbench/README.md` |
| `docs/` | 活跃指引文档 | 可维护，保持第0.4节阅读链有效 |
| `docs/archive/` | 历史文档（2026-07-27归档） | 只读追溯，不得反向覆盖现行规则 |
| `docs/maintenance/` | 三级流程、开发交接快照、机主开工手册 | 可维护，先读《维护与重构标准流程_适配版》 |
| `docs/testing/` | 实机回归归档与黄金存档制度 | 按制度写入 |
| `build/` | 构建暂存（工具输出） | 工具写入，勿手改 |
| `releases/` | 当前发布包（v130e双zip） | 只由`build_release.py`产出；`releases/archive/`为旧测试包 |
| `baseline_inputs/` | 历史原始包与封面素材 | 只读 |
| `reference/` | 原版游戏路径配置 | 只改`vanilla_path.json`指向本机安装路径 |
| `.git/` | Git仓库 | 禁止`reset --hard`/`clean -fd`等破坏性操作 |

## 0.4 推荐阅读顺序（AI接手后）

1. 本文件（总入口+全部强制规则）。
2. `docs/CURRENT_BASELINE.md`——版本状态唯一裁决点。
3. `docs/HUMAN_DECISIONS.md` + `workbench/decisions/human_decisions.json`——人工裁定台账。
4. `docs/maintenance/维护与重构标准流程_适配版.md`——三级流程与三扇门；判级后按`docs/CODEX_WORKFLOW.md`执行。`docs/RELEASE_CHECKLIST.md`——发布闸门；发布上传时另读`docs/WORKSHOP_UPLOAD.md`。
5. `docs/KNOWN_RISKS.md` + `docs/INCIDENTS_AND_SOLUTIONS.md`——风险边界与典型故障。
6. 按任务选读：`docs/ENGINEERING_PLAYBOOK.md`（工程）、`docs/TEXT_PROCESSING_PLAYBOOK.md`（文本）、`docs/LOCAL_REPOSITORY_GUIDE.md`（环境/初始化）、`docs/AUDIT_DATA_GUIDE.md`（底库用法）。
7. 进入`src/shared/`、`src/full_only/`、`tools/`前，先读各目录下的`AGENTS.md`。
8. 只有追溯历史时才读`docs/archive/`（其中PROJECT_RULES_FULL为对话串时代旧规范，与现行体系平行，仅供参考）。

## 1. 项目定位

本项目是纯人物小传MOD。核心功能仅为国家领袖、顾问、陆军将领、海军将领等人物补充悬浮简介。

除非用户明确要求，禁止恢复或加入：地区介绍事件、功德林或接收将领玩法、战争/投降/议和沉浸文本、额外决议、AI或玩法机制修改。默认测试剧本只处理1936和1939。

## 2. 每次任务开始必须执行

1. 阅读`docs/CURRENT_BASELINE.md`、`docs/HUMAN_DECISIONS.md`以及与任务相关的经验文档。
2. 执行`git status --short`，不得覆盖未提交的用户改动。
3. 先做只读扫描，列出已确认事实、推测、涉及文件、最小方案、允许diff和测试项目。
4. 先按`docs/maintenance/维护与重构标准流程_适配版.md`判级（A/B/C）并走对应门；三扇门（需求对齐/方案拍板/提交确认）必须等机主拍板；推送仅凭「推送」二字。
5. 未获得明确修改指令前不得写入源码。
6. 任务范围明确时不得顺手修复其他问题。
7. 机器底库只用于找候选，不得把机器候选直接写成确认BUG。

## 3. 来源优先级

1. 用户在当前任务中的明确指令和人工审定文本；
2. `workbench/decisions/human_decisions.json`和`docs/HUMAN_DECISIONS.md`；
3. `docs/CURRENT_BASELINE.md`；
4. `workbench/approved_text/`；
5. 当前Git稳定源码；
6. `docs/archive/PROJECT_RULES_FULL.md`（历史参考）及各活跃经验手册；
7. `audit/data/`机器底库和历史交接资料。

旧包、旧表或旧报告不得覆盖当前稳定基准。历史文档中的“测试版”状态不得覆盖用户后续实机确认。

## 4. 源码模型

- `src/shared/`：完整版和兼容版共同来源；
- `src/full_only/`：仅完整版需要的动态人物路径覆盖；
- `packaging/lite/`、`packaging/full/`：两个版本各自包元数据；
- 兼容版=`shared`；完整版=`shared + full_only`。

禁止维护两套重复的完整源码。禁止把`full_only`整棵复制进兼容版。

## 5. 默认允许的修改

仅在任务明确要求时允许：

- 新增或替换人物身份块内的`desc`引用；
- 新增或替换人物小传本地化正文；
- 必要的`idea_token_desc`或`POLITICS_*_DESC`别名；
- 用户批准的人物姓名显示修正；
- 为当前游戏版本重建完整版动态路径覆盖，并保持非小传语义与原版一致；
- 维护审计、构建和报告工具。

## 6. 默认禁止的修改

未经用户明确批准，不得修改：

- `ideology`、`traits`、技能、费用、头像、角色ID、`idea_token`；
- `allowed`、`available`、`visible`、`trigger`、`ai_will_do`；
- 国策、事件、决议、on_action、scripted_effect的原版效果或顺序；
- 国家历史、招募、晋升、选举、政变和动态上台逻辑；
- 与当前任务无关的文件；
- 原版参考目录；
- Git历史或用户未提交改动。

禁止批量格式化、批量重排、批量改换行、批量改编码。禁止使用`git reset --hard`、`git clean -fd`等破坏性命令。

非`desc`脚本变化必须得到用户明确批准，并临时登记到`audit/allowlists/diff_exceptions.json`，写明文件、理由和允许正则。不得用宽泛例外掩盖整文件差异。

## 7. 人物文本规则

- 人物小传原则上为单段；
- 以公开史料为主，重要人物核验生卒年月、职务和关键事件；
- 资料不足、同名混淆或身份存疑时保守处理；
- C类非领袖原则上不写；科学家默认不写；
- 不神化，不洗白，不以情绪化评价替代事实；
- 同一人物优先建立单一正文主键，其他身份用别名复用；
- 人工审定文本优先于AI文本；AI生成正文不得未经人工批准进入发布源码。

## 8. 编码和本地化

- `localisation/**/*.yml`保持UTF-8 BOM及正确语言头；
- 现有脚本必须保持v130c7基线的BOM和换行状态；新普通脚本默认UTF-8无BOM；
- 不得产生重复key、非法YML行、空正文、失效别名或别名循环；
- 新增`desc`引用必须有对应正文；
- 正文不要使用物理多行或残留审稿标记。

## 9. 完整版高风险规则

修改`src/full_only/`前必须：

1. 配置`reference/vanilla_path.json`或环境变量`HOI4_VANILLA_PATH`；
2. 与当前原版参考文件比对；
3. 证明该覆盖确有动态人物小传功能；
4. 以当前原版文件为底重新注入；
5. 除批准的`desc`外，去除`desc`后的原版脚本token必须完全一致；
6. 展示完整diff并运行全部审计。

EGY、ISR、JOR、LEB、LIB、PAL、SYR七个`history/countries`文件保护18个运行时领袖小传，未经重新语义审计不得删除。

## 10. 审计入口

首次迁移或怀疑基线损坏时：

```text
python tools/verify_initial_baseline.py
python tools/build_release.py --baseline
python tools/verify_build.py
```

日常修改后：

```text
python tools/audit_all.py
```

日常审计不得要求源码永远与v130c7相同；它检查的是当前差异是否合法。完整版发生变化但没有原版参考时，审计必须失败。

## 11. 状态和发布

Codex可以表述：文件确认、静态检查通过、测试包已生成、日志发现问题。Codex不得自行声明“稳定版”或“正式修复”。只有用户完成游戏内测试并明确确认后，才允许更新稳定基准、合并`main`和创建`*-stable`标签。

不得自行上传Steam工坊、发布远程仓库、发送邮件或删除旧稳定包。发布包中不得混入日志、存档、Excel、缓存、历史ZIP、审计底库或工作台文件。
