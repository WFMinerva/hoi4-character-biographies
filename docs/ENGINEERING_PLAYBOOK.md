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

人物小传必须写在实际身份块中。人物已有一个身份的正文，不等于其他身份一定自动显示。多身份应优先共用一个正文主键，通过别名避免维护两套文字。

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
- `promote_character`
- `create_country_leader`
- `create_corps_commander`
- `create_field_marshal`
- `create_navy_leader`

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

## 4. 完整版覆盖文件重建原则

完整版覆盖原版事件、国策、决议、`on_actions`、`scripted_effects`和国家历史文件。游戏版本更新时：

1. 以新版本原版文件为底稿；
2. 从当前MOD中提取已批准的`desc`注入；
3. 将注入精确迁移到新原版对应语义块；
4. 比较去除所有`desc`赋值后的脚本token；
5. 非`desc`语义必须与新原版一致；
6. 重新进行代表性动态路线实机测试。

禁止直接把旧版完整覆盖文件复制到新游戏版本。过去事件不触发、国策停滞等问题，本质上就是旧原版全文覆盖新原版逻辑。

## 5. “文件看似相同”不等于可以删除

以下变化虽然不增加`desc`行数，但承担真实功能：

```txt
desc = ""  ->  desc = CBIO_TAG_person_desc
```

或：

```txt
desc = POLITICS_OLD_DESC  ->  desc = CBIO_TAG_person_desc
```

因此冗余判断必须比较`desc`的值和引用正文，不能只看行数净增。EGY、ISR、JOR、LEB、LIB、PAL、SYR七个国家历史文件保护18个运行时领袖小传，未经重新语义复核不得删除。

## 6. 别名与单一正文源

同一真人跨国家Tag、跨身份、跨显示入口时，应建立单一正文源。例如：

```yml
CHI_fu_zuoyi_desc:0 "……"
SHX_fu_zuoyi_desc:0 "$CHI_fu_zuoyi_desc$"
```

维护时只改主键。别名必须无循环、目标存在、不得把人工审定正文反向覆盖为旧短文。

## 7. 编码与换行

- 本地化YML：UTF-8 BOM。
- 普通脚本TXT：保持原文件编码，项目当前规范为UTF-8无BOM。
- 不得由编辑器造成整文件换行变化。
- 不得出现UTF-16、零宽字符、NUL、混合换行。
- 本地化正文必须物理单行；内部引号使用HOI4当前文件既有转义风格。

## 8. 日志解释

日志必须与本轮diff和MOD本体一起判断：

- `text.log`：缺失本地化、非法键、解析异常的主要证据。
- `error.log`：脚本语法、无效scope、无效token等主要证据。
- `game.log`：事件、国策、决议与动态路径执行线索。
- `setup.log`：加载顺序、文件覆盖和初始化线索。

日志中存在原版噪声不等于MOD有错；但本轮新增且与修改文件、key或路径对应的报错必须处理。

## 9. Git任务边界

- 一个问题一个分支。
- 修改前先只读扫描。
- 修改后必须查看`git diff --stat`和完整diff。
- 默认脚本修改只允许`desc`赋值；其他脚本语义变化必须写入有理由、有范围的临时例外清单，并由用户批准。
- 不允许`git reset --hard`、`git clean -fd`或覆盖未提交用户文件。

## 10. 测试状态

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
