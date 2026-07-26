# v130c7 → Codex本地维护仓库迁移报告

## 1. 输入文件

- `（兼容版测试版）china_bio_lite_v130c7_Daigo_cover_test.zip`
  - 原始SHA-256：`6d037cb0234393ef2113e123f7b56de8416c6fcb2b98735945846a92276e7073`
- `（完整版测试版）china_bio_v130c7_Daigo_cover_test.zip`
  - 原始SHA-256：`48aa90e76ff0da87c4e1acd334443d910159556ee8e471ac24bf4d93b784b99c`

原交接单制作时仍标记为测试版；用户在后续项目对话中完成实机验证并将v130c7作为稳定基准。本仓库保留原交接单，同时在`CURRENT_BASELINE.md`记录后续有效状态。

## 2. 双版本拆分结果

规范化内部路径后：

- 兼容版文件：256；
- 完整版文件：462；
- 共同路径：255；
- 共同路径内容完全一致：254；
- 共同路径唯一差异：`descriptor.mod`；
- 完整版额外MOD内容文件：206；
- 两个包各自另有一个外层`.mod`文件。

因此源码被无损拆分为：

```text
兼容版 = src/shared + packaging/lite
完整版 = src/shared + src/full_only + packaging/full
```

初始化导入：

- `src/shared`：254个MOD文件；
- `src/full_only`：206个MOD文件。

## 3. 审计结果

已执行：

```text
python tools/audit_all.py
```

结果：

- 兼容版源码与基准254个MOD文件逐文件SHA-256一致；
- 完整版源码与基准460个MOD文件逐文件SHA-256一致；
- 本地化编码检查通过；
- 86个本地化文件、2种语言、7388个去重键检查通过；
- 4570处CBIO desc引用均可解析；
- 373个脚本TXT大括号与引号检查通过。

`thumbnail.png`被识别为二进制文件并产生预期警告，不是错误。

## 4. 重建验证

已执行：

```text
python tools/build_release.py --baseline
python tools/verify_build.py
```

结果：

- 兼容版重建包256个规范化文件与原始包逐文件大小、SHA-256完全一致；
- 完整版重建包462个规范化文件与原始包逐文件大小、SHA-256完全一致。

重建ZIP整体SHA-256与原始ZIP不同，原因是ZIP容器元数据、时间戳或压缩条目元数据不同。该差异不代表MOD内容变化；验证程序以包内规范化路径和文件SHA-256为准。

## 5. 本仓库没有做的事

- 没有修改任何人物正文；
- 没有修改任何角色、事件、国策、决议或国家历史逻辑；
- 没有更新MOD版本号或工坊内容；
- 没有把原版游戏文件放入仓库；
- 没有建立远程仓库或上传GitHub；
- 没有替用户再次进行游戏实机测试。

## 6. 下一步

在Windows本地解压后运行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\init_repo.ps1
```

然后用Codex打开仓库根目录。首次任务应选择一个极小且可验证的维护任务，用于验证“只读扫描—最小修改—静态审计—构建—实机测试—稳定tag”整条流程。
