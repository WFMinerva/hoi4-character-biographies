# 钢四人物小传 MOD
# v130c6 晋系傅作义、蒙疆与满洲国姓名及动态路径专项交接单

## 一、当前稳定基准

本串结束时，用户已完成实机测试并明确反馈：

> 测试通过

因此，以下两个版本正式视为当前稳定基准。后续所有整合、修复、审计和打包必须以它们为底稿，不得回退到 v130c5、v130c4 或更早版本。

### 完整版稳定基准

`（完整版测试版）china_bio_v130c6_Fu_Zuoyi_MAN_hotfix_test.zip`

### 兼容版稳定基准

`（兼容版测试版）china_bio_lite_v130c6_Fu_Zuoyi_MAN_hotfix_test.zip`

---

## 二、本串处理范围

本串主要处理中国地方势力及相关政权中的三类问题：

1. 无小传的占位角色仍显示中文名；
2. 同一真人在不同身份中，小传正文没有复用；
3. 动态新增身份存在漏挂 `desc` 的情况。

涉及范围：

- 晋系 `SHX`；
- 新疆 `SIK`；
- 云南 `YUN`；
- 蒙疆 `MEN`；
- 满洲国 `MAN`；
- 傅作义跨 `CHI / SHX` 身份正文复用。

---

## 三、已完成事项

### 1. SHX、SIK、YUN 占位角色原名恢复

专项审计统计出：

- SHX：16个全无显示小传角色；
- SIK：17个；
- YUN：15个；
- 合计48个。

用户最终裁定：

- 除傅作义外，其余47个均为占位角色；
- 占位角色不写人物小传；
- 凡仍显示中文名者，统一恢复原版英文／原名；
- 傅作义为唯一真人例外。

执行结果：

- SIK 17个、YUN 15个在 v130c3 中已经完成英文／原名恢复；
- SHX 新增恢复15个占位角色；
- 傅作义保留中文名。

阶段版本：

`v130c4_SHX_placeholder_name_cleanup_test`

---

### 2. 蒙疆 MEN 静态占位角色姓名清理

对蒙疆进行静态人物、动态身份、运行时路径和姓名本地化专项检查后确认：

#### 真实动态人物

- `MEN_prince_demchugdongrub` 德穆楚克栋鲁普；
- `MEN_jodbajab` 卓特巴扎普。

两人合计存在7条动态国家领袖路径。

完整版中：

- `events/SEA_Japan.txt`
- `history/countries/MEN - Mengkukuo.txt`

已经存在对应动态 `desc`，不得进入占位角色清理。

兼容版中：

- 不覆盖事件和 `history`；
- 两人的动态身份小传属于结构性例外；
- 不为修补该问题而破坏兼容版边界。

#### 静态无小传角色

确认11名静态角色有中文名但没有有效小传，统一恢复英文／原名：

- `MEN_sonin_xiangying`
- `MEN_zhao_zhanshan`
- `MEN_songgotu_shangzhi`
- `MEN_hesehn_tiemei`
- `MEN_guan_xingde`
- `MEN_deng_linge`
- `MEN_hung_zhehuang`
- `MEN_yonimitsu_kasahara`
- `MEN_nalan_kang_an`
- `MEN_songgotu_zhanshan`
- `MEN_megata_toshiro`

这些角色不写人物小传。

阶段版本：

`v130c5_MEN_placeholder_name_cleanup_test`

用户随后测试通过。

---

### 3. 晋系政治顾问傅作义小传修复

发现：

- CHI 陆军将领傅作义已有正文：`CHI_fu_zuoyi_desc`
- SHX 政治顾问傅作义使用：`idea_token = SHX_fu_zuoyi`
- 但缺少：`SHX_fu_zuoyi_desc`

最终处理方式：

```text
SHX_fu_zuoyi_desc:0 "$CHI_fu_zuoyi_desc$"
```

即：

- 不复制正文；
- 不产生两套傅作义文本；
- SHX 政治顾问与 CHI 陆军将领共用同一正文源；
- 后续如修改傅作义正文，只需维护 `CHI_fu_zuoyi_desc`。

该修复同时写入完整版和兼容版。

---

### 4. 满洲国 MAN 静态占位角色姓名清理

确认10名满洲国静态角色有中文名但无有效人物小传，统一恢复原版英文／原名：

- `MAN_changlin_linge`
- `MAN_hung_zhehuang`
- `MAN_xian_yuan`
- `MAN_deng_linge`
- `MAN_guan_xingde`
- `MAN_yin_zuoqian`
- `MAN_yonimitsu_kasahara`
- `MAN_hesehn_tiemei`
- `MAN_megata_toshiro`
- `MAN_songgotu_zhanshan`

这些角色不写人物小传。

---

### 5. 满洲国动态路径复核与溥仪漏挂修复

对满洲国动态人物路径进行复核后确认：

- `MAN_aisin_gioro_puyi`
- `MAN_pujie`
- `MAN_aisin_gioro_xiqia`
- `MAN_jonjurjab`

其中溥杰、熙洽、正珠尔扎布现有动态 `desc` 保持不变。

在：

`common/national_focus/manchukuo_TSR.txt`

的：

`MAN_tsr_chinese_leadership`

路径中，溥仪通过：

```text
add_field_marshal_role
```

获得陆军元帅身份，但原先没有 `desc`。

完整版新增：

```text
desc = MAN_aisin_gioro_puyi_desc
```

修复边界严格限定为：

- 仅增加1行 `desc`；
- 不改 `skill`；
- 不改 `traits`；
- 不改触发条件；
- 不改国策逻辑；
- 不改人物上台机制；
- 不改 AI。

兼容版不覆盖 `national_focus`，因此该动态元帅身份仍属于结构性例外。

---

## 四、最终稳定版内容

v130c6 在 v130c5 基础上新增：

1. SHX 政治顾问傅作义 `desc` 别名；
2. MAN 10名占位角色英文／原名恢复；
3. 完整版溥仪 TSR 动态陆军元帅 `desc` 补挂。

用户已实机确认：

> 测试通过

因此 v130c6 正式替代 v130c5，成为当前稳定基准。

---

## 五、本串生成文件

### 当前稳定包

- `（完整版测试版）china_bio_v130c6_Fu_Zuoyi_MAN_hotfix_test.zip`
- `（兼容版测试版）china_bio_lite_v130c6_Fu_Zuoyi_MAN_hotfix_test.zip`

### v130c6 审计文件

- `v130c6_傅作义顾问与满洲国占位及动态路径_修包审计.xlsx`
- `v130c6_傅作义顾问与满洲国专项修复_构建审计报告.txt`
- `v130c6_傅作义与满洲国专项_SHA256.txt`

### 前序阶段文件

- `v130c4_SHX_SIK_YUN_占位角色原名恢复_最终裁定与修包审计.xlsx`
- `v130c5_MEN_11名占位角色原名恢复与动态人物保护_修包审计.xlsx`

---

## 六、已确认技术规则

### 1. 占位角色处理

对于无有效人物小传、无可信真人依据，并经用户确认属于占位角色者：

- 不写人物小传；
- 不保留中文名；
- 恢复原版英文／原名。

---

### 2. 真人多身份处理

同一真人存在多个身份时：

- 优先复用同一正文源；
- 不复制生成多套正文；
- 顾问可通过 `idea_token_desc` 或对应 `desc` key 指向主正文；
- 修改正文时只维护一个源 key。

傅作义为标准案例：

```text
SHX_fu_zuoyi_desc -> CHI_fu_zuoyi_desc
```

---

### 3. 动态身份处理

静态身份已有 `desc`，不代表动态新增身份自动继承。

必须逐路径检查：

- `add_country_leader_role`
- `add_corps_commander_role`
- `add_field_marshal_role`
- `add_navy_leader_role`
- `create_country_leader`
- 其他运行时新增人物身份命令

完整版可在动态创建块中精确补 `desc`。

兼容版原则上不为单个动态缺口覆盖：

- `events`
- `history`
- `national_focus`
- `decisions`
- `scripted_effects`

这类问题应登记为结构性例外。

---

### 4. 修改边界

后续同类修复必须继续坚持：

- 只改姓名显示和 `desc`；
- 不改人物属性；
- 不改 `traits`；
- 不改 `ideology`；
- 不改顾问费用；
- 不改国策逻辑；
- 不改事件触发；
- 不改 AI；
- 不改原版玩法机制。

---

## 七、测试口径

固定只测试：

- 1936剧本；
- 1939剧本。

建议回归项目：

1. 国家领袖悬停；
2. 政治顾问悬停；
3. 陆军将领和陆军元帅悬停；
4. 动态上台领袖；
5. 动态新增军职；
6. 占位角色姓名是否恢复英文／原名；
7. `error.log`；
8. `text.log`。

v130c6 已由用户实机确认通过。

---

## 八、下一步建议

中国地方势力与相关政权的这一轮姓名清理和动态路径修复已基本收尾。

下一串建议选择新的国家或政权，继续采用相同流程：

1. 扫描静态人物与身份；
2. 扫描动态新增身份；
3. 找出“中文名但无小传”角色；
4. 区分真人、动态真人与占位角色；
5. 真人保留中文名并写小传；
6. 占位角色恢复英文／原名；
7. 完整版补动态 `desc`；
8. 兼容版登记结构性例外；
9. 生成双版本测试包；
10. 实机测试后再升级稳定基准。

当前不应重复处理：

- SHX；
- SIK；
- YUN；
- MEN；
- MAN；
- 傅作义跨身份正文问题；
- 溥仪 TSR 动态陆军元帅漏挂。

除非新日志、截图或实机测试证明问题复发。
