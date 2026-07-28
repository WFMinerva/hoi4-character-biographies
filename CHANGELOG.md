# Changelog

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
