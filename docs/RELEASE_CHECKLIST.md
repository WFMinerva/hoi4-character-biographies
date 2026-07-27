# 发布闸门

> 总入口：根目录`AGENTS.md`；当前版本状态以`docs/CURRENT_BASELINE.md`为准。

## 静态检查

- [ ] `python tools/audit_all.py`全部通过
- [ ] 本地化YML编码、语言头、重复key检查通过
- [ ] 别名无缺失目标、无循环
- [ ] 所有新增`desc`引用均有正文
- [ ] `desc`处于正确身份或动态命令层级
- [ ] 脚本大括号和引号检查通过
- [ ] `git diff --stat`与任务范围一致
- [ ] 无批量格式化、换行、BOM或编码噪声
- [ ] 无未批准的`ideology`、`traits`、触发条件或效果修改
- [ ] 若`full_only`变化：去除`desc`后与原版脚本token完全一致

## 构建检查

- [ ] 兼容版只由`shared`构建
- [ ] 完整版由`shared + full_only`构建
- [ ] `.mod`与`descriptor.mod`路径一致
- [ ] 无日志、表格、审计底库、缓存、旧ZIP混入MOD包
- [ ] 生成SHA-256和文件清单

## 游戏测试

- [ ] 兼容版1936可进入
- [ ] 兼容版1939可进入
- [ ] 完整版1936可进入
- [ ] 完整版1939可进入
- [ ] 本轮目标功能正常
- [ ] `error.log`无新增相关报错
- [ ] `text.log`无新增缺失本地化
- [ ] `game.log`和`setup.log`无相关异常
- [ ] 无关原版事件、国策、决议和动态流程未受影响
- [ ] 动态路径双重验证：目标人物按原版逻辑正常上台/获得身份，**且**上台后悬浮显示小传；错误人物上台但有小传不算通过

测试优先级：P0本轮改过的路径必测；P1历史问题路径回归；P2新增`<idea_token>_desc`顾问路径抽测；P3纯静态`desc`补挂抽测。

## 工坊发布文案

- 玩家版（changenote、工坊更新说明）：写新增国家/人物、玩家可感知的修复、是否建议重新订阅；不写脚本路径、key名和debug过程。
- 开发版（CHANGELOG、提交说明）：写数量、文件和证据分级；未经用户确认不得写"人工确认完成"。
- 工坊页面固定说明含"Made in a Chinese-language environment; not tested in English"。
- 上传流程见`docs/WORKSHOP_UPLOAD.md`；页面简介文案见`docs/STEAM_FULL_BBCODE.txt`、`docs/STEAM_LITE_BBCODE.txt`。

## 状态

Codex只能写“静态检查通过”或“测试包已生成”。只有用户实机确认后，才能写“稳定版”。
