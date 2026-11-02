# 工具规则

审计工具默认只读，输出只能进入`audit/reports/`、`build/`或`releases/`。任何自动修复必须要求显式`--apply`参数。失败必须返回非零退出码，不得静默修改`src/`。

## 入口边界

- `verify_initial_baseline.py`：只用于首次迁移或基线损坏调查，不得放回日常审计入口。
- `audit_all.py` / `audit_worktree.py`：日常维护入口，检查当前差异是否合法。`--skip-vanilla`跳过原版比对（仅供CI等无游戏文件环境使用，本地日常审计不得使用）。
- `self_test.py`：审计工具的金丝雀测试。用`CBIO_ROOT`环境变量把各检查器重定向到合成fixture，验证每个检查器对干净树通过、对注入故障拦截。改动任何`check_*.py`或`common.py`后必须运行。
- `check_snapshot.py`：校验`AGENTS.md`含指向`docs/CURRENT_BASELINE.md`的明确路径指针，且未内嵌版本行（版本事实单一事实源为基准卡）。
- `compare_with_vanilla.py`：只读比较完整版与原版，必须忽略`desc`赋值但保留其他全部脚本token。
- `build_release.py`：只从`src/`与`packaging/`构建，不得把`audit/`、`docs/`、`workbench/`、日志或历史ZIP装入MOD。
- `check_logs_cbio.py`：实机日志判读工具（非审计门禁检查器，不接入`audit_all.py`；输出仅`audit/reports/`；金丝雀用例见`self_test.py`）。

## 开发要求

- 新检查器必须能在当前稳定基线上通过。
- 必须为误报和漏报分别设计测试（在`self_test.py`登记金丝雀用例）。
- 不得以简单全文件字符串替换实现高风险脚本修复。
- 对Git差异的检查必须包含未跟踪的`src/`文件。
- 对原版语义的检查不得仅比较行数、哈希或去空白文本。
