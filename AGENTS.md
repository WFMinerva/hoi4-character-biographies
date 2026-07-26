# 钢四人物小传MOD：Codex强制维护规则

## 1. 项目定位

本项目是纯人物小传MOD。核心功能仅为国家领袖、顾问、陆军将领、海军将领等人物补充悬浮简介。

除非用户明确要求，禁止恢复或加入：地区介绍事件、功德林或接收将领玩法、战争/投降/议和沉浸文本、额外决议、AI或玩法机制修改。默认测试剧本只处理1936和1939。

## 2. 每次任务开始必须执行

1. 阅读`docs/CURRENT_BASELINE.md`、`docs/HUMAN_DECISIONS.md`以及与任务相关的经验文档。
2. 执行`git status --short`，不得覆盖未提交的用户改动。
3. 先做只读扫描，列出已确认事实、推测、涉及文件、最小方案、允许diff和测试项目。
4. 未获得明确修改指令前不得写入源码。
5. 任务范围明确时不得顺手修复其他问题。
6. 机器底库只用于找候选，不得把机器候选直接写成确认BUG。

## 3. 来源优先级

1. 用户在当前任务中的明确指令和人工审定文本；
2. `workbench/decisions/human_decisions.json`和`docs/HUMAN_DECISIONS.md`；
3. `docs/CURRENT_BASELINE.md`；
4. `workbench/approved_text/`；
5. 当前Git稳定源码；
6. `docs/PROJECT_RULES_FULL.md`及各经验手册；
7. `audit/data/`机器底库和历史交接资料。

旧包、旧表或旧报告不得覆盖当前稳定基准。历史文档中的“测试版”状态不得覆盖用户后续实机确认。

## 4. 源码模型

- `src/shared/`：完整版和兼容版共同来源；
- `src/full_only/`：仅完整版需要的动态人物路径覆盖；
- `packaging/lite/`、`packaging/full/`：两个版本各自包元数据；
- 兼容版=`shared`；完整版=`shared + full_only`。

禁止维护两套重复的完整源码。禁止把`full_only`整棵复制进兼容版。

## 5. 默认允许的修改

仅在任务明确要求时允许：

- 新增或替换人物身份块内的`desc`引用；
- 新增或替换人物小传本地化正文；
- 必要的`idea_token_desc`或`POLITICS_*_DESC`别名；
- 用户批准的人物姓名显示修正；
- 为当前游戏版本重建完整版动态路径覆盖，并保持非小传语义与原版一致；
- 维护审计、构建和报告工具。

## 6. 默认禁止的修改

未经用户明确批准，不得修改：

- `ideology`、`traits`、技能、费用、头像、角色ID、`idea_token`；
- `allowed`、`available`、`visible`、`trigger`、`ai_will_do`；
- 国策、事件、决议、on_action、scripted_effect的原版效果或顺序；
- 国家历史、招募、晋升、选举、政变和动态上台逻辑；
- 与当前任务无关的文件；
- 原版参考目录；
- Git历史或用户未提交改动。

禁止批量格式化、批量重排、批量改换行、批量改编码。禁止使用`git reset --hard`、`git clean -fd`等破坏性命令。

非`desc`脚本变化必须得到用户明确批准，并临时登记到`audit/allowlists/diff_exceptions.json`，写明文件、理由和允许正则。不得用宽泛例外掩盖整文件差异。

## 7. 人物文本规则

- 人物小传原则上为单段；
- 以公开史料为主，重要人物核验生卒年月、职务和关键事件；
- 资料不足、同名混淆或身份存疑时保守处理；
- C类非领袖原则上不写；科学家默认不写；
- 不神化，不洗白，不以情绪化评价替代事实；
- 同一人物优先建立单一正文主键，其他身份用别名复用；
- 人工审定文本优先于AI文本；AI生成正文不得未经人工批准进入发布源码。

## 8. 编码和本地化

- `localisation/**/*.yml`保持UTF-8 BOM及正确语言头；
- 现有脚本必须保持v130c7基线的BOM和换行状态；新普通脚本默认UTF-8无BOM；
- 不得产生重复key、非法YML行、空正文、失效别名或别名循环；
- 新增`desc`引用必须有对应正文；
- 正文不要使用物理多行或残留审稿标记。

## 9. 完整版高风险规则

修改`src/full_only/`前必须：

1. 配置`reference/vanilla_path.json`或环境变量`HOI4_VANILLA_PATH`；
2. 与当前原版参考文件比对；
3. 证明该覆盖确有动态人物小传功能；
4. 以当前原版文件为底重新注入；
5. 除批准的`desc`外，去除`desc`后的原版脚本token必须完全一致；
6. 展示完整diff并运行全部审计。

EGY、ISR、JOR、LEB、LIB、PAL、SYR七个`history/countries`文件保护18个运行时领袖小传，未经重新语义审计不得删除。

## 10. 审计入口

首次迁移或怀疑基线损坏时：

```text
python tools/verify_initial_baseline.py
python tools/build_release.py --baseline
python tools/verify_build.py
```

日常修改后：

```text
python tools/audit_all.py
```

日常审计不得要求源码永远与v130c7相同；它检查的是当前差异是否合法。完整版发生变化但没有原版参考时，审计必须失败。

## 11. 状态和发布

Codex可以表述：文件确认、静态检查通过、测试包已生成、日志发现问题。Codex不得自行声明“稳定版”或“正式修复”。只有用户完成游戏内测试并明确确认后，才允许更新稳定基准、合并`main`和创建`*-stable`标签。

不得自行上传Steam工坊、发布远程仓库、发送邮件或删除旧稳定包。发布包中不得混入日志、存档、Excel、缓存、历史ZIP、审计底库或工作台文件。
