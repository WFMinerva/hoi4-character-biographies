# 钢四人物小传MOD：总入口与强制维护规则

本文件是仓库总入口：项目定位、任务路由、安全红线、关键目录与权威文档指针。本文件不保存当前版本、待办、机器环境或历史记录——版本以 `docs/CURRENT_BASELINE.md` 为准，当前状态以 Git 与当前对话为准。

## 1. 权威文档指针（事实只在一处维护）

| 你要找什么 | 唯一权威 |
| --- | --- |
| 稳定版本、发布物、哈希、转正条件 | `docs/CURRENT_BASELINE.md` |
| 人工语义裁定与长期例外 | `docs/HUMAN_DECISIONS.md` + `workbench/decisions/human_decisions.json` |
| 任务分类与执行流程 | `docs/maintenance/维护与重构标准流程_适配版.md` |
| 机主交互与只有机主能做的事 | `docs/maintenance/机主开工手册.md` |
| 高风险边界 | `docs/KNOWN_RISKS.md` |
| 故障史与防复发 | `docs/INCIDENTS_AND_SOLUTIONS.md` |
| 发布闸门 / 工坊上传 | `docs/RELEASE_CHECKLIST.md` / `docs/WORKSHOP_UPLOAD.md` |
| 工程 / 文本 / 环境 / 底库手册 | `docs/ENGINEERING_PLAYBOOK.md`、`docs/TEXT_PROCESSING_PLAYBOOK.md`、`docs/LOCAL_REPOSITORY_GUIDE.md`、`docs/AUDIT_DATA_GUIDE.md`（按任务选读） |
| 高风险任务卡机制 | `docs/scaffold/任务卡机制说明.md` |
| 实机证据制度 | `docs/testing/`（仅发布、稳定版转正与高风险回归要求完整归档） |
| 历史文档 | `docs/archive/`（只读追溯，不得反向覆盖现行规则） |

机器环境（Python、游戏路径、steamcmd、模型配置）以本机运行时识别为准，不写入共享文档。

## 2. 项目定位

本项目是纯人物小传MOD。核心功能仅为国家领袖、顾问、陆军将领、海军将领等人物补充悬浮简介。

除非用户明确要求，禁止恢复或加入：地区介绍事件、功德林或接收将领玩法、战争/投降/议和沉浸文本、额外决议、AI或玩法机制修改。默认测试剧本只处理1936和1939。

## 3. 任务路由（自然语言开工，按类执行）

接到任务先 `git status --short`（不得覆盖未提交的用户改动），再按类执行——细则见 `docs/maintenance/维护与重构标准流程_适配版.md`：

- **普通讨论 / 只读检查**：直接处理，不建卡、不落盘、不跑审计。
- **小型、可逆、范围清楚的变更**：不建卡、不强制独立模型复验；先只读扫描（列出确认事实、推测、涉及文件、最小方案、允许 diff 与所需测试）；验证按实际风险选择（见第 12 节）；展示 diff，机主明确确认后提交。
- **高风险变更**（命中任一：`src/full_only/`、游戏逻辑或身份语义、史实来源存疑、批量正文、双版本结构、基准卡或人工裁定台账、稳定版转正、发布与工坊上传）：需求门 / 方案门 / 完整验证 / 提交前独立复验**必须执行**；任务卡仅在需要跨对话、跨多步骤推进或确有复杂决策需要持久交接时使用（见 `docs/scaffold/任务卡机制说明.md`）。

已核实来源且经机主逐字批准的单篇小传或别名维护按小型变更处理，不自动升级高风险；人工批准与内容审计不省。

任何情况下：机器扫描结果只是候选，不是确认 BUG；未获得明确修改指令前不得写入源码；任务范围明确时不得顺手修复其他问题。

## 4. 关键目录

| 路径 | 用途 | 能不能动 |
| --- | --- | --- |
| `src/shared/` | 两版本共同MOD源码 | 受第7/8节约束，改动须过审计；先读`src/shared/AGENTS.md` |
| `src/full_only/` | 完整版动态路径覆盖 | 高风险，先读`src/full_only/AGENTS.md`和第11节 |
| `packaging/lite/`、`packaging/full/` | 两版本包元数据（descriptor/outer.mod） | 版本号变更时才动 |
| `tools/` | 审计/构建/校验脚本 | 可维护，先读`tools/AGENTS.md`；默认只读、不得静默改src |
| `audit/baselines/` | 当前基线manifest与编码基线 | 机器生成，只由`build_release.py --baseline`重建 |
| `audit/allowlists/` | 非desc差异临时例外登记 | 按第8节流程逐任务登记 |
| `audit/data/` | 历史机器底库 | 只读参考资料，不得当作确认BUG |
| `audit/reports/` | 审计报告输出目录 | 工具写入 |
| `workbench/` | 人工工作台（待审/审定正文、裁定、对账底账） | 日常工作区，见`workbench/README.md`；`workbench/cards/`为高风险任务卡存放区 |
| `docs/` | 活跃指引文档 | 可维护；`docs/scaffold/`为孵化脚手架层（可迁移方法论+任务卡机制） |
| `docs/archive/` | 历史文档 | 只读追溯，不得反向覆盖现行规则 |
| `docs/maintenance/` | 维护流程、机主手册 | 可维护 |
| `docs/testing/` | 实机回归归档与黄金存档制度 | 按制度写入 |
| `build/` | 构建暂存（工具输出） | 工具写入，勿手改 |
| `releases/` | 当前发布包 | 只由`build_release.py`产出；`releases/archive/`为旧测试包 |
| `baseline_inputs/` | 历史原始包与封面素材 | 只读 |
| `reference/` | 原版游戏路径配置 | 只改`vanilla_path.json`指向本机安装路径 |
| `.git/` | Git仓库 | 禁止`reset --hard`/`clean -fd`等破坏性操作 |

进入 `src/shared/`、`src/full_only/`、`tools/` 前，先读各目录下的 `AGENTS.md`。

## 5. 来源优先级

1. 用户在当前任务中的明确指令和人工审定文本；
2. `workbench/decisions/human_decisions.json`和`docs/HUMAN_DECISIONS.md`；
3. `docs/CURRENT_BASELINE.md`；
4. `workbench/approved_text/`；
5. 当前Git稳定源码；
6. `docs/archive/PROJECT_RULES_FULL.md`（历史参考）及各活跃经验手册；
7. `audit/data/`机器底库和历史交接资料。

旧包、旧表或旧报告不得覆盖当前稳定基准。历史文档中的"测试版"状态不得覆盖用户后续实机确认。

## 6. 源码模型

- `src/shared/`：完整版和兼容版共同来源；
- `src/full_only/`：仅完整版需要的动态人物路径覆盖；
- `packaging/lite/`、`packaging/full/`：两个版本各自包元数据；
- 兼容版=`shared`；完整版=`shared + full_only`。

禁止维护两套重复的完整源码。禁止把`full_only`整棵复制进兼容版。

## 7. 默认允许的修改

仅在任务明确要求时允许：

- 新增或替换人物身份块内的`desc`引用；
- 新增或替换人物小传本地化正文；
- 必要的`idea_token_desc`或`POLITICS_*_DESC`别名；
- 用户批准的人物姓名显示修正；
- 为当前游戏版本重建完整版动态路径覆盖，并保持非小传语义与原版一致；
- 维护审计、构建和报告工具。

## 8. 默认禁止的修改

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

## 9. 人物文本规则

- 人物小传原则上为单段；
- 以公开史料为主，重要人物核验生卒年月、职务和关键事件；
- 资料不足、同名混淆或身份存疑时保守处理；
- C类非领袖原则上不写；科学家默认不写；
- 不神化，不洗白，不以情绪化评价替代事实；
- 同一人物优先建立单一正文主键，其他身份用别名复用；
- 人工审定文本优先于AI文本；AI生成正文不得未经人工批准进入发布源码。

## 10. 编码和本地化

- `localisation/**/*.yml`保持UTF-8 BOM及正确语言头；
- 现有脚本必须保持既有基线的BOM和换行状态；新普通脚本默认UTF-8无BOM；
- 不得产生重复key、非法YML行、空正文、失效别名或别名循环；
- 新增`desc`引用必须有对应正文；
- 正文不要使用物理多行或残留审稿标记。

## 11. 完整版高风险规则

修改`src/full_only/`前必须：

1. 配置`reference/vanilla_path.json`或环境变量`HOI4_VANILLA_PATH`；
2. 与当前原版参考文件比对；
3. 证明该覆盖确有动态人物小传功能；
4. 以当前原版文件为底重新注入；
5. 除批准的`desc`外，去除`desc`后的原版脚本token必须完全一致；
6. 展示完整diff并运行全部审计。

EGY、ISR、JOR、LEB、LIB、PAL、SYR七个`history/countries`文件保护18个运行时领袖小传，未经重新语义审计不得删除。

## 12. 审计入口

首次迁移或怀疑基线损坏时：

```text
python tools/verify_initial_baseline.py
python tools/build_release.py --baseline
python tools/verify_build.py
```

日常验证按风险匹配：

- `src/`内容改动：`python tools/audit_all.py`；
- 检查器改动（`tools/check_*.py`、`common.py`、`self_test.py`）：先`python tools/self_test.py`再跑相关审计；
- 纯文档改动：`git diff --check`与相关链接/指针检查；只改`AGENTS.md`时加跑`python tools/check_snapshot.py`（它校验入口指针），不强制完整 audit；
- 改动`docs/CURRENT_BASELINE.md`、`docs/HUMAN_DECISIONS.md`及其JSON台账属高风险：跑相关专项检查与`python tools/audit_all.py`。

日常审计不得要求源码永远与旧基线相同；它检查的是当前差异是否合法。完整版发生变化但没有原版参考时，审计必须失败。

## 13. 表述纪律：证据分级

结论必须区分：**文件确认**、**静态确认**、**日志确认**、**实机确认**、**用户确认**、**稳定基准**、**已接受限制**、**未覆盖**和**待验证**。低等级证据不能替代高等级证据；机器候选尤其不能直接升级为确认 BUG。

## 14. 状态和发布

AI可以表述：文件确认、静态检查通过、测试包已生成、日志发现问题。AI不得自行声明"稳定版"或"正式修复"。只有用户完成游戏内测试并明确确认后，才允许更新稳定基准、合并`main`和创建`*-stable`标签。

提交、合并、标签与发布均须机主明确授权；推送涉及外部写入，必须机主明确说出「推送」，不得从"确认""照批""按推荐"推断。不得自行上传Steam工坊、发布远程仓库、发送邮件或删除旧稳定包。发布包中不得混入日志、存档、Excel、缓存、历史ZIP、审计底库或工作台文件。
