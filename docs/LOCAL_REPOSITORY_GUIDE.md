# 钢四人物小传：本地仓库环境与初始化

> 总入口：根目录`AGENTS.md`；当前版本状态以`docs/CURRENT_BASELINE.md`为准。本机环境（Python/Git/游戏路径/steamcmd）以 `docs/maintenance/开发状态快照与交接.md` 1.1 表为唯一口径，本文只讲仓库初始化与日常命令。

本仓库由用户实机确认的v130c7双版本包初始化，并在v2中补齐项目经验、机器审计底库和日常发布闸门。

## 源码模型

- `src/shared/`：完整版与兼容版共同文件，共255个MOD文件。
- `src/full_only/`：仅完整版需要的动态人物路径覆盖，共207个MOD文件。
- `packaging/`：两个版本各自的`descriptor.mod`和外层`.mod`模板。
- `audit/data/`：v130a—v130b历史机器底库和语义复核资料。
- `workbench/templates/`：任务卡与扫描/入包清单模板。
- `workbench/cards/`：任务卡存放区（机制见`docs/scaffold/任务卡机制说明.md`）。
- `workbench/decisions/`：结构化人工裁定。

兼容版=`shared`；完整版=`shared + full_only`。

## 第一次使用

解压后在PowerShell进入本目录：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\init_repo.ps1
```

初始化脚本会：

1. 验证源码与v130c7原包逐文件等价；
2. 运行日常静态检查；
3. 重建两个基线包并逐文件校验；
4. 初始化Git、提交基线并创建`v130c7-stable`标签。

## 配置原版参考

复制：

```text
reference/vanilla_path.example.json
```

为：

```text
reference/vanilla_path.json
```

把路径改为本机HOI4 v1.19.2原版目录或ZIP。也可以设置环境变量：

```powershell
$env:HOI4_VANILLA_PATH="<本机HOI4原版目录或ZIP>"
```

只要`src/full_only/`发生变化，日常审计就会要求原版参考，并验证去除`desc`后全部脚本语义与原版一致。

## 日常维护

```powershell
git switch main
git status --short
git switch -c fix/任务英文短名
```

先让AI只读扫描。人工批准后修改，然后执行：

```powershell
python tools/audit_all.py
python tools/build_release.py --version <下一版本>-test
```

实机测试通过并由用户明确确认后，才能合并`main`和创建稳定标签。

## 文档入口

总入口为根目录`AGENTS.md`（含状态快照、待办、目录地图和推荐阅读顺序）。活跃文档：

- `docs/CURRENT_BASELINE.md`：当前版本基准；
- `docs/HUMAN_DECISIONS.md`：人工裁定；
- `docs/CODEX_WORKFLOW.md`：日常维护流程；
- `docs/ENGINEERING_PLAYBOOK.md`：代码和脚本经验；
- `docs/TEXT_PROCESSING_PLAYBOOK.md`：人物文本写作与清洗经验；
- `docs/INCIDENTS_AND_SOLUTIONS.md`：已遇故障、原因和防复发措施；
- `docs/KNOWN_RISKS.md`：高风险边界速查；
- `docs/AUDIT_DATA_GUIDE.md`：机器底库使用方法。

历史文档（对话串时代交接单、迁移报告、旧常驻规范等）已归档至`docs/archive/`，仅供追溯。
