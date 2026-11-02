# v130g-test2 实机回归归档（2026-11-02）

> 本轮由 AI 在本机执行 GUI 自动化代跑（机主 2026-11-02 明确授权），用于验证 GOE_Raj 分治链小传显示与日志回归。
> 游戏：HOI4 1.19.4.1（`code_revisions.log`：`game_hash_short=99a5ee557`，Operation Postern v1.19.4.1.99a5）。
> 测试包：`china_bio_v130g-test2.zip`（完整版）sha256 `aaeecef80a283c83f8de251ec105ef5b4f05e1c533f447783436415ddbaf224f`；`china_bio_lite_v130g-test2.zip`（兼容版）sha256 `78fcf715061ad9d22958394b81a1ab5ae9cca1fae5fc142926df3cda9d27c544`。
> 部署：本机 `Documents/Paradox Interactive/Hearts of Iron IV/mod/china_bio[_lite]_v130g-test2/`；每轮只启用一个版本；未改工坊包。

## 一、结论摘要

- **GOE_Raj 分治链人物小传显示：通过（实机确认）**。
  - 完整版 1936/1939：真纳、蒙巴顿各自只见自己的小传；尼赫鲁只由新版 `.12` 上台并显示自己的小传；旧 `.9` 事件（联合王国准备介入）不改变领袖、无尼赫鲁小传；甘地由 shared 静态 desc 显示。
  - 兼容版 1936/1939：可进入游戏，无小传相关报错。
- **日志对比：通过（归因）**。
  - 完整版/兼容版 1936 开局 `error.log` 均为 0 字节（无 MOD 同场景也是 0）。
  - 完整版/兼容版 1939 开局 `error.log` 均为 44 行；忽略行号后与**无 MOD 同场景**的错误多重集**完全一致**（差异 0），说明 1939 开局的 41 类签名全部是原版 1.19.4.1 既有噪声，不是本 MOD 引入。
  - 旧包调查基线（`build/runtime-baseline-20261101/error.log`，64 行/60 类签名）中的错误在 v130g-test2 中**全部消失（60/60）**。
- **白名单判定**：初判 1936 clean 轮 `PASS`；1939 clean 轮 `FAIL`（41 类原版新签名）、交互轮 `FAIL`（另 33 类时间推进期原版 AI/事件签名）——当时未擅自扩白名单，另出审定提案 `audit/reports/cbio_whitelist_proposal_v130g-test2.md`。机主 2026-11-02 裁定后已入库 89 条并复跑：**1936/1939/交互三轮全部 PASS**（含兼容版两轮），执行记录 `audit/reports/cbio_whitelist_ruling_execution_v130g-test2.md`。

## 二、实机矩阵（每轮只启用一个版本）

| 轮次 | 版本 | 剧本/入口 | 关键操作 | 结果 |
| --- | --- | --- | --- | --- |
| full-1936 | 完整版 | 1936 / `-start_tag=RAJ` | 政治界面悬停领袖；控制台 `event GOE_RAJ_partition.7` 选真纳/蒙巴顿/甘地；`event .12` 选尼赫鲁；`event .9` 负向 | 通过 |
| full-1939 | 完整版 | 1939 / 菜单选英国属印度 | 同上（1939 下 `.7` 的真纳选项需先补 `RAJ_a_secular_state` 焦点，已用控制台补齐） | 通过 |
| lite-1936 | 兼容版 | 1936 / `-start_tag=RAJ` | 进入游戏截屏 | 通过（无动态分治链验收项） |
| lite-1939 | 兼容版 | 1939 / 菜单选英国属印度 | 进入游戏截屏 | 通过 |

> 说明：本轮为合成复现，使用控制台补齐政治条件（`eval_effect set_politics = { ruling_party = democratic ... }`、`eval_effect complete_national_focus = RAJ_a_secular_state`）。正常游玩路径由焦点链自然满足；控制台仅用于让 `.7/.12` 在当前 1936/1939 存档内可复现。
> 说明：重复触发 `.7` 的甘地选项会产生 `add_country_leader_trait - Country leader already has trait` 告警（2 类），属**测试方法产物**，不是正常游玩路径会出现的 MOD 错误；已从 clean 轮日志中剥离（clean 轮未触发事件）。

## 三、证据

- 截图（16 张）：`screenshots/`；清单见 `清单.md`。
- 日志（7 组，已脱敏）：`logs/full-1936-clean/`、`logs/full-1939-clean/`、`logs/full-1939-interactive/`、`logs/nomod-1936/`、`logs/nomod-1939/`、`logs/lite-1936/`、`logs/lite-1939/`；每组含 `error.log`/`game.log`/`setup.log`/`text.log`/`code_revisions.log`/`system.log`。
- 机器判定：
  - `audit/reports/cbio_v130g-test2_1936.json` → **PASS**
  - `audit/reports/cbio_v130g-test2_1939.json` → **FAIL（41 类原版噪声未入库）**
  - `audit/reports/cbio_v130g-test2.json` → **FAIL（交互轮，74 类未入库；其中 41 类为原版开局噪声、33 类为时间推进期原版 AI/事件噪声）**
  - 日志归因对照：`audit/reports/runtime_log_compare.txt`
  - 白名单审定提案：`audit/reports/cbio_whitelist_proposal_v130g-test2.md`
- `SHA256SUMS.txt`：本归档内全部文件哈希。

## 四、残余风险 / 待机主裁定

1. `tools/cbio_log_whitelist.json` 已于 2026-11-02 按机主裁定更新（89 条，全部标注仅适用 HOI4 1.19.4.1），三轮复跑 PASS；游戏升级后这些条目必须重新判定。
2. 兼容版 1939 动态领袖既有缺口（毛泽东 NCNS、德王、乔巴山）属已接受限制，本轮未新增。
3. 本轮 AI 代跑使用控制台合成前置条件与固定套路点击；未覆盖完整焦点链自然推进、全部 P0/P1 人物与长时间运行，正式放行仍应以机主完整实机回归为准。

## 五、环境恢复

- 每轮结束均关闭游戏；测试后 `dlc_load.json` 已恢复为原值 `{"enabled_mods":["mod/ugc_3762643540.mod"],"disabled_dlcs":[]}`。
- 本地测试包保留在 `Documents/.../mod/` 便于机主复跑；未改动工坊 `ugc_3762643540`；未提交、未推送、未上传。

## 六、白名单入库与正式包（2026-11-02 追加）

- 机主裁定：A 组 41 类入库；B 组按来源分流（19 条引擎/AI 无来源文件 + 5 条来源 `history/units/` 入库；9 条 `events/GOE_Persia.txt` 单独列出后按选项 A 入库）；另补 10 条兼容版行号变体。白名单共 89 条，逐条 `version:"1.19.4.1"`。
- 复跑结果（`audit/reports/cbio_v130g_test2c_*.json`）：完整版 1936/1939/交互 PASS，兼容版 1936/1939 PASS。
- 正式包（替代 test2 测试包，版本号 `v130g`）：`china_bio_v130g.zip` SHA-256 `3bac28fd939da16f539172bd92adf9175ef189c714371fc1df731605ed205afa`；`china_bio_lite_v130g.zip` SHA-256 `52de98ce748abd00d0e1d19f6415169776e159299a8125875647b3fa01f53edc`；`verify_build.py --version v130g` 逐字节通过。
- v130g-test2 测试包与 v130g-test1 一律作废，不得部署或上传。
