# Codex日常维护流程

> 本文是 `docs/maintenance/维护与重构标准流程_适配版.md` 的「判级后执行附录」：动手前先读该流程判级（A/B/C）并过对应门（需求对齐/方案拍板/提交确认），本文第 1–7 节命令照常执行。

> 总入口：根目录`AGENTS.md`；当前版本状态以`docs/CURRENT_BASELINE.md`为准。

## 1. 任务开始

```powershell
git switch main
git status --short
git switch -c fix/任务英文短名
```

第一条指令：

```text
读取AGENTS.md、docs/CURRENT_BASELINE.md、docs/HUMAN_DECISIONS.md，
以及与本任务有关的工程或文本经验手册。

本轮先只读扫描，不修改文件。
列出：确认事实、推测、问题证据、涉及文件、最小修复方案、允许diff、需要的原版比对和游戏测试。
机器底库中的候选不得直接视为确认BUG。
```

## 2. 修改前

- 查看`git status --short`；
- 确认任务分支；
- 确认没有未提交用户改动；
- 若修改`full_only`，先配置原版参考；
- 若需要非`desc`脚本改动，先得到用户批准并登记精确例外。

## 3. 执行修改

```text
只修改刚才列出的文件。
禁止顺手修复、批量格式化和改换行。
修改后运行python tools/audit_all.py并展示git diff。
不要声明稳定，不要上传工坊。
```

## 4. 审计

```powershell
python tools/audit_all.py
```

该入口检查：

- 编码、BOM、换行和隐藏字符；
- 本地化语法、重复key和缺失正文；
- 别名缺失与循环；
- 审稿残留和空正文；
- 人工裁定落实及台账md/json一致性；
- `AGENTS.md`快照与基准卡版本一致性；
- 脚本括号和引号；
- `desc`层级语义；
- 当前Git差异白名单；
- 完整版去除`desc`后与原版脚本语义一致。

改动`tools/`下任何检查器后，先运行`python tools/self_test.py`（金丝雀测试）再跑审计。

`verify_initial_baseline.py`只用于首次迁移，不属于日常审计。

## 5. 构建与验证

```powershell
python tools/build_release.py --version <下一版本>-test
```

构建输出在`releases/`，不提交Git。

实机测试前把构建结果部署到游戏mod目录：`<游戏用户目录>\mod\`（路径以《开发状态快照与交接》1.1 为准）。开发期目录名加`_dev`后缀与正式版区分；转正后删除dev目录。

## 6. 实机测试

分别测试两个版本的1936和1939剧本，检查目标人物、动态路径、无关原版流程以及：

- `error.log`
- `text.log`
- `game.log`
- `setup.log`

日志位于`<游戏用户目录>\logs\`（路径以《开发状态快照与交接》1.1 为准）。部署后由Codex先自查日志再向用户汇报，不要让用户转发日志。日志解释和原版噪声归因见`docs/ENGINEERING_PLAYBOOK.md`第10节。

## 7. 稳定化

只有用户明确确认后：

```powershell
git add .
git commit -m "fix: ..."
git switch main
git merge --no-ff fix/...
git tag <下一版本>-stable
```

随后更新`docs/CURRENT_BASELINE.md`、`CHANGELOG.md`和必要的人工裁定台账。
