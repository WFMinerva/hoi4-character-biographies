# Steam工坊上传流程

> 总入口：根目录`AGENTS.md`。本流程依据`F:\steamcmd\STEAMCMD_工坊上传指南.md`整理，该指南已在本机其他HOI4 MOD实测通过。

## 分工

- **Codex负责做到登录前**：构建正式包、解压到独立暂存目录、逐文件哈希核对、生成VDF和changenote、核对物品ID与缩略图路径。
- **必须用户本人做**：使用账号`wendu1991`执行steamcmd命令并输入密码和Steam Guard验证码；密码和验证码不得写入命令、VDF、仓库或记忆。
- **上传后由Codex收尾**：读取`F:\steamcmd\logs\workshop_log.txt`，分别确认两个物品均出现`Upload finished ... : OK`，记录Manifest ID并更新仓库状态。
- AGENTS.md第11节禁令不变：Codex不得自行上传工坊。

## 工坊物品ID

- 兼容版：`3736859636`
- 完整版：`3762643540`

更新已有物品时`publishedfileid`不变，订阅者自动收到更新。VDF采用版本化文件名：

- `F:\steamcmd\hoi4_china_bio_lite_<版本>.vdf`
- `F:\steamcmd\hoi4_china_bio_full_<版本>.vdf`

## 上传三步

### 1. 暂存内容

把MOD内容原样复制到暂存目录，目录名即MOD文件夹名：

```text
F:\steamcmd\workshop_content\<MOD目录名>\
    common\ events\ localisation\ ...(MOD实际内容)
    descriptor.mod
    thumbnail.png
```

上传前用`diff -r`确认暂存目录与`releases/`解压后的发布包逐文件一致。`descriptor.mod`里的`path=`行保留无妨，工坊会忽略。

### 2. 写VDF配置

每个版本一个VDF，放在`F:\steamcmd\`下（参考已有`hoi4_ocnb_workshop.vdf`格式）：

```text
"workshopitem"
{
	"appid"		"394360"
	"publishedfileid"		"<工坊物品ID>"
	"contentfolder"		"F:/steamcmd/workshop_content/<MOD目录名>"
	"previewfile"		"F:/steamcmd/workshop_content/<MOD目录名>/thumbnail.png"
	"changenote"		"<本次更新的变更说明>"
}
```

每次上传前更新`changenote`；changenote按`docs/RELEASE_CHECKLIST.md`“工坊发布文案”节的玩家版口径写。路径统一使用正斜杠，避免反斜杠转义。默认不在VDF中加入`title`或`description`，不修改工坊标题、简介和简介中的版本号；只有用户当次明确要求时才改。

### 3. 执行上传（用户本人操作）

同一账号拥有两个物品。准备完成后优先一次登录连续上传两项：

```powershell
F:\steamcmd\steamcmd.exe +login wendu1991 +workshop_build_item F:\steamcmd\hoi4_china_bio_lite_<版本>.vdf +workshop_build_item F:\steamcmd\hoi4_china_bio_full_<版本>.vdf +quit
```

- 密码和Steam Guard验证码由用户按提示输入。
- 必须看到兼容版`3736859636`和完整版`3762643540`各自的`Upload finished ... : OK`；只出现一个`OK`不算双版本上传完成。
- 若连续命令只执行了一项，使用同一账号单独重跑缺失项；本机通常会复用刚完成的登录验证。
- 最终以`F:\steamcmd\logs\workshop_log.txt`为准，不以终端窗口一闪而过或页面更新时间作为唯一证据。

## 默认文案边界

- 默认只更新文件内容、预览图和changenote。
- 工坊标题、简介、标签和简介版本号一律保持现状，除非用户在当前上传任务中明确要求修改。
- 如果用户明确要求修改简介，以`docs/STEAM_FULL_BBCODE.txt`、`docs/STEAM_LITE_BBCODE.txt`为底稿，修改前先展示精确差异。

## 2026-07-30实测记录

- v130e兼容版：物品`3736859636`，Manifest `5995984417193478401`，日志确认`OK`。
- v130e完整版：物品`3762643540`，Manifest `8131297658874109917`，日志确认`OK`。
- 两个暂存目录与正式ZIP内MOD目录逐文件哈希一致；两份VDF均未包含`title`或`description`。
