# 工程维护手册

> 总入口：根目录`AGENTS.md`；当前版本状态以`docs/CURRENT_BASELINE.md`为准。

本文件把项目过去实际踩过的技术坑整理为Codex可执行的工程规则。它补充`AGENTS.md`，不替代当前基准卡。

## 1. 源码与版本模型

- `src/shared/`是两个版本唯一的共同源码。
- `src/full_only/`只保存完整版为动态人物显示而必须覆盖的原版文件。
- 兼容版构建：`shared + packaging/lite`。
- 完整版构建：`shared + full_only + packaging/full`。
- 禁止同时维护两棵完整MOD目录；任何共同文本只维护一份。
- `baseline_inputs/`只用于首次迁移等价验证，不是日常编辑对象。

## 2. 静态身份显示

常见静态身份位于`common/characters`：

- `country_leader`
- `advisor`
- `corps_commander`
- `field_marshal`
- `navy_leader`

人物小传必须写在实际身份块中。注意两类例外：顾问/理论家/部长界面不读身份块`desc`，改读`<idea_token>_desc`（见第4节）；动态新增身份不自动继承静态身份`desc`（见第3节）。多身份应优先共用一个正文主键，通过别名避免维护两套文字。

标准例：

```txt
country_leader = {
    ideology = conservatism
    desc = CBIO_TAG_person_desc
}
```

## 3. 动态身份与运行时新建人物

必须检查的动态命令包括但不限于：

- `add_country_leader_role`
- `add_corps_commander_role`
- `add_field_marshal_role`
- `add_navy_leader_role`
- `add_advisor_role`
- `promote_character`
- `create_country_leader`
- `create_corps_commander`
- `create_field_marshal`
- `create_navy_leader`
- `recruit_character`、`retire_character`
- `set_country_leader`、`remove_country_leader_role`

`add_country_leader_role`的`desc`必须进入其内部`country_leader = {}`块，不能放在命令顶层：

```txt
add_country_leader_role = {
    character = TAG_person
    country_leader = {
        ideology = conservatism
        desc = CBIO_TAG_person_desc
    }
}
```

军官动态角色通常直接把`desc`放在`add_corps_commander_role`等命令块内。运行时`create_*`命令的`desc`通常直接位于创建块内。

通过国策或事件**移除旧身份再新增另一身份**的，新增身份必须单独检查`desc`，不能因原始身份已有`desc`就判定动态路径已覆盖。

## 4. 显示路径全景

人物小传在游戏里有三类显示入口，机制不同，排查和补挂方式也不同：

1. **领袖/将领身份块**：界面读取身份块内的`desc = KEY`。静态身份在`common/characters`，动态身份沿第3节命令块补挂。
2. **顾问/理论家/部长**：界面**不读人物身份块的`desc`**，而是自动读取`idea_token = xxx`对应的本地化键`xxx_desc`。因此：
   - 同一人兼任顾问时，只补人物主键`CBIO_xxx_desc`不够，顾问界面仍为空；必须为`idea_token`对应的`xxx_desc`建立本地化，通常用别名复用主键：`xxx_desc:0 "$CBIO_xxx_desc$"`。
   - 反向也成立：顾问身份没有显式`desc`不等于无小传——`<idea_token>_desc`可能已存在。v130d档1复核（2026-07）曾把124名此类人物误判为"未挂"，后全部确认为误报。判定顾问覆盖状态时必须检查`idea_token`的`_desc`键。
   - 边界：禁止修改`idea_token`字段本身（AGENTS.md第6节），但允许新增或替换`<token>_desc`本地化键。
3. **旧式/动态领袖的`POLITICS_*_DESC`**：部分旧式领袖和`create_country_leader`创建的运行时领袖使用`POLITICS_xxx_DESC`政治简介键。`create_country_leader`可以在`history/countries`、国策或事件中直接创建领袖，**该人物未必存在于`common/characters`**，只扫characters文件必漏。EGY等七文件保护的18个运行时领袖即属此类。

本地化覆盖顺序：`localisation/replace/`下的文件在原版本地化之后加载，用于覆盖原版同名key。本项目`cbio_replace_*`系列文件即用于替换原版人物短简介。规则：覆盖原版key必须用replace目录明确替换；不得靠普通yml里的同名key"掩盖"旧定义，重复key必须只留一处有效定义。

## 5. “某人不显示”排查顺序

用户报告"某人没有小传"时，不得直接判"缺正文"。按顺序排查：

1. 查机器底账和人工裁定：该人物是否已裁定不写（占位、C类非领袖、科学家）；
2. 查本地化：正文主键是否存在，有无同名key冲突或被原版短文本覆盖；
3. 查静态身份块：对应身份块内是否有`desc`、层级是否正确；
4. 查顾问路径：若为顾问/理论家/部长，检查`idea_token`的`_desc`键；
5. 查动态路径：沿`add_*_role`/`create_*`/`promote_character`实际执行路径检查动态身份块的`desc`；经"移除旧身份再新增身份"的，新增身份单独检查；
6. 查`create_country_leader`：该领袖是否由history/国策/事件直接创建、使用`POLITICS_*_DESC`键；
7. 查同人跨key：是否已有正文主键但该入口未同步别名；
8. 以上全部排除后，才判定为确需补写的缺口，并按机器候选→人工裁定流程处理。

另外：人物脚本解析不能假设缩进规整（张闻天角色块曾因缩进不规则被脚本漏抓）。扫描脚本必须配不匹配兜底清单，疑似漏抓时人工复核。

## 6. 完整版覆盖文件重建原则

完整版覆盖原版事件、国策、决议、`on_actions`、`scripted_effects`和国家历史文件。出现以下任一情形，先做版本兼容审计再入包：用户提到P社更新；玩家反馈MOD与原版行为不一致；拿到新版原版文件；MOD覆盖了原版脚本（完整版恒定满足）；原版更新日志涉及已覆盖文件。

游戏版本更新时：

1. 以新版本原版文件为底稿；
2. 从当前MOD中提取已批准的`desc`注入；
3. 将注入精确迁移到新原版对应语义块；
4. 比较去除所有`desc`赋值后的脚本token；
5. 非`desc`语义必须与新原版一致；
6. 重新进行代表性动态路线实机测试。

禁止直接把旧版完整覆盖文件复制到新游戏版本。过去事件不触发、国策停滞等问题，本质上就是旧原版全文覆盖新原版逻辑。

覆盖文件按四分类处理：

- A类（确有动态小传功能）：按上述步骤重新注入；
- B类（功能已不再需要）：优先删除覆盖让原版生效，避免回退原版逻辑；
- C类（仍需保留）：保留并复核`desc`值语义；
- D类（仅历史包袱、无小传语义）：考虑删除，减少未来冲突面。

删除判断与"EGY等七文件保留"不矛盾：标准都是逐文件`desc`值语义复核。把有效覆盖误判为冗余已有前科（见`docs/INCIDENTS_AND_SOLUTIONS.md`第2条）。

## 7. “文件看似相同”不等于可以删除

以下变化虽然不增加`desc`行数，但承担真实功能：

```txt
desc = ""  ->  desc = CBIO_TAG_person_desc
```

或：

```txt
desc = POLITICS_OLD_DESC  ->  desc = CBIO_TAG_person_desc
```

因此冗余判断必须比较`desc`的值和引用正文，不能只看行数净增。EGY、ISR、JOR、LEB、LIB、PAL、SYR七个国家历史文件保护18个运行时领袖小传，未经重新语义复核不得删除。

## 8. 别名与单一正文源

同一真人跨国家Tag、跨身份、跨显示入口时，应建立单一正文源。例如：

```yml
CHI_fu_zuoyi_desc:0 "……"
SHX_fu_zuoyi_desc:0 "$CHI_fu_zuoyi_desc$"
```

维护时只改主键。别名必须无循环、目标存在、不得把人工审定正文反向覆盖为旧短文。

## 9. 编码与换行

- 本地化YML：UTF-8 BOM。
- 普通脚本TXT：保持原文件编码，项目当前规范为UTF-8无BOM。
- 不得由编辑器造成整文件换行变化。
- 不得出现UTF-16、零宽字符、NUL、混合换行。
- 本地化正文必须物理单行；内部引号使用HOI4当前文件既有转义风格。

## 10. 日志解释

日志必须与本轮diff和MOD本体一起判断：

- `text.log`：缺失本地化、非法键、解析异常的主要证据。
- `error.log`：脚本语法、无效scope、无效token等主要证据。
- `game.log`：事件、国策、决议与动态路径执行线索。
- `setup.log`：加载顺序、文件覆盖和初始化线索。

日志中存在原版噪声不等于MOD有错；但本轮新增且与修改文件、key或路径对应的报错必须处理。

`error.log`自检关键词：`Unexpected token`、`Invalid effect`、`Unknown effect-type`、`Malformed token`、`Invalid Decision ID`、`missing localization`、`duplicate loc key`。

`text.log`为空只说明本地化层面无报错，不等于"日志无报错"；结论必须写清是哪个日志为空。

控制台/debug归因：用控制台或debug decision强制触发测试动态路径时，`error.log`可能出现原版运行时提示（`create_unit`位置失败、state/controller条件不满足、AI脚本失败、强制触发下事件链状态不足等）。归因四步：不开MOD是否也报→报错块是否含CBIO注入内容→是否debug强制触发→与小传无关则记为观察项。**不得为了让error.log绝对为空而修改原版玩法。**

## 11. Git任务边界

- 一个问题一个分支。
- 修改前先只读扫描。
- 修改后必须查看`git diff --stat`和完整diff。
- 默认脚本修改只允许`desc`赋值；其他脚本语义变化必须写入有理由、有范围的临时例外清单，并由用户批准。
- 不允许`git reset --hard`、`git clean -fd`或覆盖未提交用户文件。

## 12. 测试状态

状态必须分开记录：

- 文件确认；
- 静态审计通过；
- 测试包已构建；
- 截图确认；
- 日志确认；
- 试玩确认；
- 用户人工确认；
- 稳定基准。

Codex不能把静态审计通过写成“稳定版”。
