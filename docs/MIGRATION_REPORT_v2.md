# Codex长期维护仓库v2升级报告

v2在v1已验证的v130c7双版本源码基础上，补齐了长期经验与日常审计体系。

## 新增

- 工程维护、文本处理、典型故障和人工裁定四类长期文档；
- v130a—v130b机器底库和语义复核资料；
- 国家显示位扫描表、最终入包清单模板；
- 人工裁定结构化JSON；
- `desc`层级、本地化别名、文本残留、差异白名单和原版非小传语义检查；
- 首次基线验证与日常审计分离。

## 入口调整

- 首次迁移：`python tools/verify_initial_baseline.py`。
- 日常维护：`python tools/audit_all.py`或`python tools/audit_worktree.py`。
- 完整版文件发生变化时，必须配置原版目录或原版ZIP供`compare_with_vanilla.py`复核。

## 未改变

- v130c7 MOD源码内容；
- 双版本构建结构；
- 用户已实机确认的稳定状态；
- 任何人物文本和游戏逻辑。
