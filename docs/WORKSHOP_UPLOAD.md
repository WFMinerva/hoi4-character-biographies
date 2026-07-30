# Steam工坊上传流程

> 总入口：根目录`AGENTS.md`。本流程依据`F:\steamcmd\STEAMCMD_工坊上传指南.md`整理，该指南已在本机其他HOI4 MOD实测通过。

## 分工

- **Codex可以做**：暂存内容、`diff -r`核对、起草VDF和changenote。
- **必须用户本人做**：执行steamcmd命令（密码和Steam Guard验证码不经Codex）；工坊页面的标题、简介、标签只能在网页手动修改。
- AGENTS.md第11节禁令不变：Codex不得自行上传工坊。

## 工坊物品ID

- 兼容版：`3736859636`
- 完整版：`3762643540`

更新已有物品时`publishedfileid`不变，订阅者自动收到更新。本MOD的VDF尚未建立（`F:\steamcmd\`下现有VDF属于其他MOD），首次上传需新建。

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
	"contentfolder"		"F:\steamcmd\workshop_content\<MOD目录名>"
	"previewfile"		"F:\steamcmd\workshop_content\<MOD目录名>\thumbnail.png"
	"changenote"		"<本次更新的变更说明>"
}
```

每次上传前更新`changenote`；changenote按`docs/RELEASE_CHECKLIST.md"工坊发布文案"节的玩家版口径写。

### 3. 执行上传（用户本人操作）

```text
F:\steamcmd\steamcmd.exe +login <Steam用户名> +workshop_build_item F:\steamcmd\<项目>.vdf +quit
```

- 账号名直接写，不加尖括号；密码和Steam Guard验证码按提示输入。
- 成功标志：`Upload finished for workshop item <ID> : OK`。
- 可查看`F:\steamcmd\logs\workshop_log.txt`确认结果。

## 上传前后的文案同步

- steamcmd只更新文件内容、预览图和changenote；页面标题、简介、标签需在网页手动编辑。
- 页面简介以`docs/STEAM_FULL_BBCODE.txt`、`docs/STEAM_LITE_BBCODE.txt`为底稿，改动后两边同步。
- v130e上传时：兼容版页面描述应点名1939剧本动态领袖缺口（毛泽东NCNS线、德王、乔巴山），见`docs/KNOWN_RISKS.md`第9条。
