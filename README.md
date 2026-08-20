# Hearts of Iron IV Character Biographies

[![Steam Workshop](https://img.shields.io/badge/Steam-Workshop-1b2838?logo=steam&logoColor=white)](https://steamcommunity.com/sharedfiles/filedetails/?id=3736859636)

> 维护者请跳至文末「开发者入口」；仓库维护规则以中文文档为准。

A historical biography expansion mod for **Hearts of Iron IV**.

This project adds detailed historical biographies to characters that appear throughout the game, including national leaders, political advisors, army commanders, naval commanders, and other historically significant figures.

By hovering over a character portrait in the game, players can read a short biography and better understand who these people were and their historical background.

---

## Features

### Historical Character Biographies

The mod restores historical context behind the names shown in Hearts of Iron IV.

Instead of only displaying a portrait and name, characters now have:

- Historical identity
- Birth and death information where available
- Political career
- Military experience
- Historical background

The goal is not to rewrite history, but to provide additional context while preserving the original game experience.

---

## Editions

The project provides different editions according to player requirements.

### Compatibility Edition

A lighter version focused on:

- Better compatibility with other mods
- Minimal changes to original game files
- Stable long-term maintenance

### Full Edition

A broader coverage version focused on:

- More complete character coverage
- Wider historical restoration
- Maximum immersion for vanilla campaigns

---

## Design Principles

This project follows several principles:

- Do not change vanilla gameplay balance
- Do not alter country AI behavior
- Do not change national focus trees, events, or political systems
- Avoid unnecessary interference with original game mechanics
- Use historical sources whenever possible

The purpose is to enrich historical immersion, not replace the original game design.

---

## Sources

Biographical texts are compiled from publicly available historical references, including:

- Wikipedia and related historical databases
- Public biographies
- Historical reference materials

Important historical figures are checked carefully before inclusion.

---

## Compatibility

Designed primarily for:

- Hearts of Iron IV 1.19.x
- Vanilla-focused gameplay

The mod is tested in-game before stable releases.

---

## Author

Created by **HAPPYADONG**

Steam Workshop:

https://steamcommunity.com/profiles/76561198024627348

---

## Related Projects

Other Hearts of Iron IV projects:

- One-Click Navy Builder
- One-Click Sandbox Start

---

## For Maintainers / 开发者入口（中文）

本仓库的维护流程、事实源与红线以中文文档为准。新接手请按以下读链顺序阅读：

1. 根目录 [`AGENTS.md`](./AGENTS.md)——总入口：状态快照、待办、目录地图（哪个目录能改）、强制规则、推荐阅读顺序。
2. [`docs/CURRENT_BASELINE.md`](./docs/CURRENT_BASELINE.md)——稳定版本与发布物唯一裁决点。
3. [`docs/HUMAN_DECISIONS.md`](./docs/HUMAN_DECISIONS.md)——已确认的人工裁定与长期例外。
4. [`docs/maintenance/维护与重构标准流程_适配版.md`](./docs/maintenance/维护与重构标准流程_适配版.md)——动手前的三级流程（A/B/C）与三扇门。
5. [`docs/maintenance/开发状态快照与交接.md`](./docs/maintenance/开发状态快照与交接.md)——开发串与机器环境交接（环境表、变更记录、开场命令）。
6. 按任务选读：工程/文本/故障/风险手册、发布闸门（见 `AGENTS.md` 第 0.4 节完整读链）。

### 快速上手

```powershell
git clone https://github.com/WFMinerva/hoi4-character-biographies.git
cd hoi4-character-biographies
# 日常维护：先跑审计留底
python tools/audit_all.py
```

- 涉及 `src/full_only/` 改动前，先按 [`reference/README.md`](./reference/README.md) 配置本机 HOI4 原版参考（`reference/vanilla_path.json`）。
- 发布构建与工坊上传纪律见 [`docs/RELEASE_CHECKLIST.md`](./docs/RELEASE_CHECKLIST.md) 与 [`docs/WORKSHOP_UPLOAD.md`](./docs/WORKSHOP_UPLOAD.md)。

### 目录速览

| 路径 | 用途 |
| --- | --- |
| `src/shared/` | 两版本共同 MOD 源码（兼容版=`shared`） |
| `src/full_only/` | 完整版动态路径覆盖（完整版=`shared+full_only`） |
| `packaging/` | 两版本包元数据（descriptor/outer.mod） |
| `tools/` | 审计/构建/校验脚本（先读 `tools/AGENTS.md`） |
| `audit/` | 机器底库、基线 manifest、例外登记、报告 |
| `workbench/` | 人工工作台：待审/审定正文、裁定台账、对账底账、任务卡 |
| `docs/scaffold/` | 孵化脚手架：可迁移方法论与任务卡机制 |
| `docs/archive/` | 历史文档（只读追溯，不覆盖现行规则） |

### 开新任务

新任务（新人物批次/新游戏版本/新接手）按任务卡机制开工：读 [`docs/scaffold/任务卡机制说明.md`](./docs/scaffold/任务卡机制说明.md)，复制 [`workbench/templates/任务卡模板.md`](./workbench/templates/任务卡模板.md) 为 `workbench/cards/<NNN>_<任务名>.md`。

> 提交与推送纪律：未经机主确认不 git commit；推送仅凭机主「推送」二字。
