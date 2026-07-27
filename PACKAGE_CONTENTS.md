# 仓库内容索引

> 总入口：根目录`AGENTS.md`（状态快照、待办、目录地图、推荐阅读顺序）。本文件仅作快速索引。

## 核心源码

- `src/shared/`：两版本共同源码（先读`src/shared/AGENTS.md`）
- `src/full_only/`：完整版动态路径覆盖（高风险，先读`src/full_only/AGENTS.md`）
- `packaging/`：两版本包元数据

## 活跃文档（docs/）

- `docs/CURRENT_BASELINE.md`：当前版本基准
- `docs/HUMAN_DECISIONS.md`：人工裁定台账
- `docs/CODEX_WORKFLOW.md`、`docs/RELEASE_CHECKLIST.md`：流程与发布闸门
- `docs/ENGINEERING_PLAYBOOK.md`、`docs/TEXT_PROCESSING_PLAYBOOK.md`：两本经验手册
- `docs/INCIDENTS_AND_SOLUTIONS.md`、`docs/KNOWN_RISKS.md`：故障与风险
- `docs/LOCAL_REPOSITORY_GUIDE.md`、`docs/AUDIT_DATA_GUIDE.md`：环境与底库
- `docs/WORKSHOP_UPLOAD.md`：工坊上传流程
- `docs/STEAM_FULL_BBCODE.txt`、`docs/STEAM_LITE_BBCODE.txt`：工坊页面文案

历史文档已归档至`docs/archive/`（含旧常驻规范`PROJECT_RULES_FULL.md`），仅供追溯。

## 审计与台账

- `audit/data/`：v130a—v130b历史机器底库
- `audit/baselines/`：v130d基线manifest（机器生成）
- `audit/allowlists/`：高风险差异例外
- `workbench/decisions/`：结构化人工裁定
- `workbench/templates/`：国家扫描和最终入包清单模板

## 工具

- 首次迁移：`tools/verify_initial_baseline.py`
- 日常审计：`tools/audit_all.py`
- 构建：`tools/build_release.py`
- 基线包校验：`tools/verify_build.py`
- 原版语义比对：`tools/compare_with_vanilla.py`
