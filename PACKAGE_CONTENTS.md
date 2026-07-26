# 仓库内容索引

## 核心源码

- `src/shared/`
- `src/full_only/`
- `packaging/`

## 长期经验

- `docs/PROJECT_RULES_FULL.md`
- `docs/ENGINEERING_PLAYBOOK.md`
- `docs/TEXT_PROCESSING_PLAYBOOK.md`
- `docs/INCIDENTS_AND_SOLUTIONS.md`
- `docs/HUMAN_DECISIONS.md`

## 审计与台账

- `audit/data/`：v130a—v130b历史机器底库
- `audit/allowlists/`：高风险差异例外
- `workbench/decisions/`：结构化人工裁定
- `workbench/templates/`：国家扫描和最终入包清单模板

## 工具

- 首次迁移：`tools/verify_initial_baseline.py`
- 日常审计：`tools/audit_all.py`
- 构建：`tools/build_release.py`
- 基线包校验：`tools/verify_build.py`
- 原版语义比对：`tools/compare_with_vanilla.py`
