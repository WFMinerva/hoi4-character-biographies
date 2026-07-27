# workbench：人工工作台

> 总入口：根目录`AGENTS.md`。本目录是人工审核与裁定的日常工作区，内容不进发布包。

## 子目录

- `pending_text/`：待人工审定的正文草稿。**当前为空**（无在审稿件）。
- `approved_text/`：已人工审定、可入包的正文。历史审定稿留档备查（如`v130d_chiang_yufen_han_yimu_draft.md`，已入包）。
- `decisions/human_decisions.json`：结构化人工裁定（活文件），与`docs/HUMAN_DECISIONS.md`同步维护。
- `import_lists/`：v130d静态身份对账底账与裁定表（6421行分类底账、档1裁定表、档1真人复核表——**档1已结案**）。档3（364条）与待裁定区（1579条）尚未处理。
- `templates/`：国家显示位扫描表、最终入包清单模板（xlsx）。
- `test_results/`：实机测试结果留存。**当前为空**。

## 一次性脚本

- `v130d_reconcile.py`：v130a-2全量表 × 当前源码覆盖 × human_decisions 三方对账，产出6421行分类底账。
- `v130d_tier1_ruling.py`：依赖前者产出，生成档1裁定表（带机器初判）。

两者均为v130d一次性对账脚本，已完成使命；可复跑但不属于日常工具链（日常审计走`tools/audit_all.py`）。
