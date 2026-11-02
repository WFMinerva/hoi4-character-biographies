# Changelog

## v130g（HOI4 1.19.4.1 全量重建，2026-11-02）

- 任务分支 `fix/hoi4-1.19.4.1-rebase`（比较基线 `4508aee`），机主授权提交并合并 `main`；**尚未上传工坊、尚未更新稳定基准**。
- 重建口径：以 HOI4 1.19.4.1 原版为底、以工坊 v130f 为人物叠加来源，重建 `src/` 140 个文件；完整版 206 个覆盖路径全部保留，`shared` 167 个人物文件全部核验（23 个漂移文件重建）。剔除获批 `desc`/姓名后，全部 TXT 与原版 token 零差异。
- 项目键人物 `desc` 821（较 v130e 的 822 减少 1：甘地改由 shared 静态 `desc` 继承）、非项目键动态 `desc` 56、七国保护 18，`check_rebuild_overlay.py errors=0`。
- 保留工坊 v130f 的 5 个已发布实质变化：`PHI` Laurel 顾问 `desc`、`NSB_Poland` Karl Albrecht、`SEA_Japan` Laurel 8 处、两份本地化正文修正（Karl Albrecht、Franz Ritter von Epp）。
- 修复 v130g-test1 暴露的 `GOE_Raj` 分治链错挂：真纳/蒙巴顿 `desc` 归位到各自 `.7` 块；尼赫鲁迁到新版 `.12`；甘地改为继承 shared 静态 `desc`；旧 `.9` 不写任何人。
- 新增工具：`rebuild_with_vanilla.py`（dry-run 优先、`--apply` 才写、`--restore` 逐文件哈希恢复）、`check_rebuild_overlay.py`、`check_rebuild_whitespace.py`；扩展 `verify_build.py`（支持测试/正式版本）、`check_diff_whitelist.py`（精确例外）、`self_test.py`（23 例）。
- 日志判读：按机主 2026-11-02 白名单裁定入库 89 条（A 组 41 + B 组 24 + 兼容版行号变体 10 + `GOE_Persia` 9 + 既有 5），逐条标注「仅适用 HOI4 1.19.4.1」；复跑 `check_logs_cbio` 1936/1939/交互及兼容版两轮全部 PASS。
- 证据分级：静态确认（`audit_all.py --require-vanilla --base 4508aee` 全绿；独立复检 PASS，含 `GOE_Raj` 分治链逐项）；实机确认（AI 代跑 1936/1939/交互，16 截图 + 7 组脱敏日志，归档 `docs/testing/v130g-test2/`）；**用户确认：待机主工坊上传前确认，尚未完成**。
- 正式包（`releases/`）：完整版 `china_bio_v130g.zip` SHA-256 `3bac28fd939da16f539172bd92adf9175ef189c714371fc1df731605ed205afa`；兼容版 `china_bio_lite_v130g.zip` SHA-256 `52de98ce748abd00d0e1d19f6415169776e159299a8125875647b3fa01f53edc`；两包均经 `verify_build.py --version v130g` 与语义 manifest（字节 `9b10f30e…`，语义 `af8cc612…`）逐字节核对。
- 未做：自然焦点链全量实机回归、P0/P1 全人物矩阵、B 组无 MOD 等时长对照（机主裁定不做）。

## v130e-stable

- 核实原版`GER_victoria`为威廉二世独女维多利亚·路易丝（1892—1980）；旧正文误写为威廉二世之妹维多利亚公主（1866—1929）。
- `CBIO_GER_victoria_desc`已替换为用户逐字审定正文；主键、角色、事件、国策、特质和继位逻辑均未改变。
- 全量静态审计通过；本次正文未触发超长警告。
- 用户实机确认完整版1936德国女皇动态上台路径正常，人物上台后显示修订小传。
- 兼容版包含修订正文，但不覆盖该动态事件，因而不负责此路径的小传显示。
- 2026-07-30已上传Steam工坊：兼容版物品`3736859636`（Manifest `5995984417193478401`），完整版物品`3762643540`（Manifest `8131297658874109917`）。

## 审计闭环收尾（2026-07-28，非MOD内容变更）

- 修正`docs/HUMAN_DECISIONS.md`中仍把v130c7称为当前稳定基准的过期表述；活跃构建示例改为`<下一版本>`占位符。
- `check_snapshot.py`从版本前缀匹配改为精确接受`当前版本`或`当前版本-stable`，防止相似版本号蒙混过关。
- 人类/机器裁定台账改为双向核对条目编号和状态，并补录原先只存在于人类文档的3条长期裁定。
- `self_test.py`为Git差异白名单和原版语义比较器构造合成依赖，金丝雀覆盖全部日常检查器。
- MOD源码、构建产物与发布包内容零变化。

## 审计体系加固（2026-07-27，非MOD内容变更）

- 新增`tools/self_test.py`：金丝雀测试，经`CBIO_ROOT`把检查器重定向到合成fixture，验证9个用例（干净通过+注入故障必拦截）；`check_diff_whitelist`/`compare_with_vanilla`因依赖git历史和原版文件不在范围内。
- `check_human_decisions.py`新增台账parity检查：`human_decisions.json`的实体key与保护文件必须出现在`docs/HUMAN_DECISIONS.md`。
- 新增`tools/check_snapshot.py`：`AGENTS.md`快照版本与日期必须与基准卡一致，已接入日常审计。
- `audit_worktree.py`新增`--skip-vanilla`（仅供CI）；新增`.github/workflows/audit.yml`：push/PR时先跑self_test再跑日常审计。
- MOD源码零变化。

## 项目管理手册（2026-07-27，非MOD内容变更）

- 新增`docs/PROJECT_MANAGEMENT_PLAYBOOK.md`：可迁移的AI协作项目管理方法论，含新项目引导词、十条核心原则、仓库骨架模板和AGENTS.md填空骨架。

## 经验回填（2026-07-27，非MOD内容变更）

- 旧规范`docs/archive/PROJECT_RULES_FULL.md`差距核对：12条仍有效规则回填活跃文档——idea_token顾问显示路径、`POLITICS_*_DESC`路径、动态命令清单补全、"某人不显示"排查顺序、replace覆盖机制、版本兼容触发条件与覆盖四分类、日志关键词与debug归因、动态路径双重验证与P0—P3分级、写作素材细则、工坊文案双轨口径、核心UI本地化禁令（均进ENGINEERING/TEXT/RELEASE/KNOWN_RISKS对应章节）。
- 两个会话导出（2026-07-26/27）挖掘回填：部署后Codex自查日志分工、mod目录部署步骤、工坊上传SOP（新建`docs/WORKSHOP_UPLOAD.md`，含两个publishedfileid）、编辑工具丢BOM故障（INCIDENTS第11条）、difflib人名误配禁令、档3/待裁定区口径警告。
- `AGENTS.md`待办新增：v130d工坊上传；对账收尾加口径警告。
- MOD源码、构建产物与发布包内容零变化。

## 仓库整理（2026-07-27，非MOD内容变更）

- 根`AGENTS.md`升级为总入口：新增状态快照、当前待办、目录地图和推荐阅读顺序，原11节强制规则保留。
- 7份历史文档（两份HANDOFF、v130c7测试清单、迁移/验证报告3份、旧常驻规范PROJECT_RULES_FULL）归档至`docs/archive/`，原文未改。
- 两个v130c7工坊封面测试包移至`releases/archive/`。
- 活跃docs统一加入口指引行；新增`workbench/README.md`、`docs/archive/README.md`；`PACKAGE_CONTENTS.md`重写为快速索引。
- MOD源码、构建产物与发布包内容零变化。

## v130d-stable

- 傅作义 SHX 政治顾问身份块补挂`SHX_fu_zuoyi_desc`（别名复用主键）。
- 溥仪 MAN 理论家顾问身份块补挂`MAN_aisin_gioro_puyi_desc`（复用主键）。
- 完成6421条静态身份覆盖对账与档1裁定表（workbench）。
- 蒋有芬（SIK）、韩乙奴（XSM）经史料核实为真人并恢复中文名，小传经用户审定入包。
- 用户实机确认通过（1936剧本显示正常，error.log零报错），转为稳定基准。

## Codex维护仓库v2

- 保持v130c7双版本MOD源码不变。
- 加入v130a—v130b静态身份、动态路径、本地化与哈希审计底库。
- 加入国家显示位扫描表和最终入包清单模板。
- 增加工程维护、文本处理、典型故障和人工裁定手册。
- 把首次基线等价验证与日常审计分离。
- 增加diff白名单、`desc`层级、别名、文本残留及原版非小传语义检查。

## v130c7-stable

- 导入用户实机确认通过的v130c7双版本源码。
- 保留醍醐忠重修订、36名占位人物姓名去汉化、傅作义顾问正文复用与完整版溥仪动态元帅修复。
- 建立`shared + full_only`源码模型；未改变任何MOD文件内容。
