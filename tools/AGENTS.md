# 工具规则

审计工具默认只读，输出只能进入`audit/reports/`、`build/`或`releases/`。任何自动修复必须要求显式`--apply`参数。失败必须返回非零退出码，不得静默修改`src/`。

## 入口边界

- `verify_initial_baseline.py`：只用于首次迁移或基线损坏调查，不得放回日常审计入口。
- `audit_all.py` / `audit_worktree.py`：日常维护入口，检查当前差异是否合法。
- `compare_with_vanilla.py`：只读比较完整版与原版，必须忽略`desc`赋值但保留其他全部脚本token。
- `build_release.py`：只从`src/`与`packaging/`构建，不得把`audit/`、`docs/`、`workbench/`、日志或历史ZIP装入MOD。

## 开发要求

- 新检查器必须能在v130c7稳定基线上通过。
- 必须为误报和漏报分别设计测试。
- 不得以简单全文件字符串替换实现高风险脚本修复。
- 对Git差异的检查必须包含未跟踪的`src/`文件。
- 对原版语义的检查不得仅比较行数、哈希或去空白文本。
