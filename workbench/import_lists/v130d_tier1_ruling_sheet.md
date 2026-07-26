# v130d 档1疑似漏写人工裁定表（中国相关TAG + 日本，191条）

> **声明：本表"机器初判"仅供参考，不构成确认结论；最终以人工裁定为准。裁定结果经用户确认后，由维护流程登记进 `workbench/decisions/human_decisions.json`。**

来源：`v130d_static_gap_reconciliation.csv` 中 557 条"疑似真人漏写"的优先级档1部分（CHI/PRC/GXC/MAN/MEN/SHX/SIK/XSM/YUN/JAP）。生成脚本：`workbench/v130d_tier1_ruling.py`。配套 CSV：`v130d_tier1_ruling_sheet.csv`（列更全，含底账序号、顾问槽位）。

## 使用说明

- 在每条末尾的**裁定栏**填写四选一：`写传` / `占位去汉化` / `已覆盖-键改名` / `不写-其他`（可加简短备注）。
- **191 条中 177 条本地化里已有现成正文键**（依据列注明"本地化中已存在可用正文键"）：这些通常**不需要新写正文**，裁定的实质是"是否把已有正文挂到该身份"或"不写"。真正没有任何现成正文的仅 14 条（全部为拉丁显示名的 GXC/SIK/XSM/YUN 通用名人物）。
- 机器初判三类的含义：
  - `疑似占位`：拉丁拼音通用名，命名模式与已裁定 36 个占位人物同族，且 MOD 名称覆盖白名单已恢复其拉丁名；候选处理方式是"占位去汉化"而非写传。
  - `疑似key改名`：当前源码存在同后缀跨 TAG 或前缀/改名关系的已覆盖人物；**跨 TAG 同后缀也可能是同名不同人**（典型：陈仪 CHI_chen_yi / 陈毅 PRC_chen_yi），裁定前必须核对人物身份。
  - `疑似真人`：其余，多为有中文显示名的顾问身份。
- 排序：按 TAG 分组（CHI、PRC、GXC、MAN、MEN、SHX、SIK、XSM、YUN、JAP），组内按身份重要度（country_leader > field_marshal > corps_commander > navy_leader > advisor）再按人物 key 字母序。
- 同一人物多条 instance/同类序号行不合并（与底账口径一致）；裁定可逐行打勾，也可对同一人批量同判。

## 机器初判统计

| 机器初判 | 条数 |
|---|---|
| 疑似真人 | 162 |
| 疑似占位 | 13 |
| 疑似key改名 | 16 |
| 合计 | 191 |

补充信号：本地化已有现成正文键 177 条；同键其他身份已覆盖（正文已存在，仅本身份未挂）54 条。

## 裁定表

### CHI

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 1 | `CHI_alexander_von_falkenhausen` | advisor/army_chief | instance[1] | 亚历山大·冯·法肯豪森（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 GER_alexander_von_falkenhausen（desc=CBIO_GER_alexander_von_falkenhausen_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；同键其他身份已挂有效desc（CHI_alexander_von_falkenhausen_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_alexander_von_falkenhausen_desc |  |
| 2 | `CHI_alexander_von_falkenhausen` | advisor/army_chief | instance[2] | 亚历山大·冯·法肯豪森（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 GER_alexander_von_falkenhausen（desc=CBIO_GER_alexander_von_falkenhausen_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；同键其他身份已挂有效desc（CHI_alexander_von_falkenhausen_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_alexander_von_falkenhausen_desc |  |
| 3 | `CHI_bai_chongxi` | advisor/navy_chief | direct | 白崇禧（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 GXC_bai_chongxi（desc=CHI_bai_chongxi_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_bai_chongxi_desc |  |
| 4 | `CHI_bo_yibo` | advisor/theorist | direct | 薄一波（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_bo_yibo_desc |  |
| 5 | `CHI_chan_chak` | advisor/navy_chief | direct | 陈策（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_chan_chak_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_chan_chak_desc |  |
| 6 | `CHI_chang_kia_ngau` | advisor/political_advisor | direct | 张嘉璈（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chang_kia_ngau_desc |  |
| 7 | `CHI_chen_bijun` | advisor/political_advisor | direct | 陈璧君（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chen_bijun_desc |  |
| 8 | `CHI_chen_cheng` | advisor/high_command | instance[1] | 陈诚（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_chen_cheng_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_chen_cheng_desc |  |
| 9 | `CHI_chen_cheng` | advisor/high_command | instance[2] | 陈诚（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_chen_cheng_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_chen_cheng_desc |  |
| 10 | `CHI_chen_gongbo` | advisor/political_advisor | direct | 陈公博（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chen_gongbo_desc |  |
| 11 | `CHI_chen_guofu` | advisor/political_advisor | instance[1] | 陈果夫（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chen_guofu_desc |  |
| 12 | `CHI_chen_guofu` | advisor/political_advisor | instance[2] | 陈果夫（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chen_guofu_desc |  |
| 13 | `CHI_chen_jitang` | advisor/army_chief | direct | 陈济棠（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 GXC_chen_jitang（desc=GXC_chen_jitang_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_chen_jitang_desc |  |
| 14 | `CHI_chen_lifu` | advisor/political_advisor | direct | 陈立夫（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chen_lifu_desc |  |
| 15 | `CHI_chen_qingyun` | advisor/theorist | direct | 陈庆云（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chen_qingyun_desc |  |
| 16 | `CHI_chen_shaokuan` | advisor/navy_chief | instance[1] | 陈绍宽（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_chen_shaokuan_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_chen_shaokuan_desc |  |
| 17 | `CHI_chen_shaokuan` | advisor/navy_chief | instance[2] | 陈绍宽（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_chen_shaokuan_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_chen_shaokuan_desc |  |
| 18 | `CHI_chen_yi` | advisor/political_advisor | direct | 陈仪（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 PRC_chen_yi（desc=PRC_chen_yi_commander_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_chen_yi_desc |  |
| 19 | `CHI_chiang_ching_kuo` | advisor/political_advisor | instance[1] | 蒋经国（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chiang_ching_kuo_desc |  |
| 20 | `CHI_chiang_ching_kuo` | advisor/political_advisor | instance[2] | 蒋经国（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chiang_ching_kuo_desc |  |
| 21 | `CHI_chu_minying` | advisor/political_advisor | direct | 褚民谊（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_chu_minying_desc |  |
| 22 | `CHI_claire_lee_chennault` | advisor/air_chief | instance[1] | 克莱尔·李·陈纳德（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 USA_claire_lee_chennault（desc=CBIO_USA_claire_lee_chennault_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_claire_lee_chennault_desc |  |
| 23 | `CHI_claire_lee_chennault` | advisor/theorist | instance[1]#2 | 克莱尔·李·陈纳德（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 USA_claire_lee_chennault（desc=CBIO_USA_claire_lee_chennault_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_claire_lee_chennault_desc |  |
| 24 | `CHI_claire_lee_chennault` | advisor/air_chief | instance[2] | 克莱尔·李·陈纳德（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 USA_claire_lee_chennault（desc=CBIO_USA_claire_lee_chennault_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_claire_lee_chennault_desc |  |
| 25 | `CHI_claire_lee_chennault` | advisor/theorist | instance[2]#2 | 克莱尔·李·陈纳德（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 USA_claire_lee_chennault（desc=CBIO_USA_claire_lee_chennault_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_claire_lee_chennault_desc |  |
| 26 | `CHI_dai_jitao` | advisor/political_advisor | direct | 戴季陶（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_dai_jitao_desc |  |
| 27 | `CHI_dai_li` | advisor/political_advisor | instance[1] | 戴笠（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_dai_li_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_dai_li_desc |  |
| 28 | `CHI_dai_li` | advisor/political_advisor | instance[2] | 戴笠（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_dai_li_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_dai_li_desc |  |
| 29 | `CHI_dai_li` | advisor/political_advisor | instance[3] | 戴笠（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_dai_li_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_dai_li_desc |  |
| 30 | `CHI_dai_li` | advisor/political_advisor | instance[4] | 戴笠（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_dai_li_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_dai_li_desc |  |
| 31 | `CHI_du_yuesheng` | advisor/political_advisor | direct | 杜月笙（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_du_yuesheng_desc |  |
| 32 | `CHI_fang_zeyi` | advisor/theorist | direct | 方子翼（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_fang_zeyi_desc |  |
| 33 | `CHI_gao_zhihang` | advisor/high_command | direct | 高志航（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_gao_zhihang_desc |  |
| 34 | `CHI_gao_zongwu` | advisor/political_advisor | direct | 高宗武（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_gao_zongwu_desc |  |
| 35 | `CHI_gui_yongqing` | advisor/high_command | direct | 桂永清（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_gui_yongqing_desc |  |
| 36 | `CHI_h_h_kung` | advisor/political_advisor | instance[1] | 孔祥熙（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_h_h_kung_desc |  |
| 37 | `CHI_h_h_kung` | advisor/political_advisor | instance[2] | 孔祥熙（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_h_h_kung_desc |  |
| 38 | `CHI_he_yingqin` | advisor/army_chief | direct | 何应钦（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_he_yingqin_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_he_yingqin_desc |  |
| 39 | `CHI_hsu_huang_sheng` | advisor/high_command | direct | 徐焕昇（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_hsu_huang_sheng_desc |  |
| 40 | `CHI_hu_hanmin` | advisor/political_advisor | direct | 胡汉民（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_hu_hanmin_desc |  |
| 41 | `CHI_huang_jinrong` | advisor/political_advisor | direct | 黄金荣（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_huang_jinrong_desc |  |
| 42 | `CHI_huang_qixiang` | advisor/army_chief | direct | 黄琪翔（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_huang_qixiang_desc |  |
| 43 | `CHI_huang_shen` | advisor/theorist | direct | 黄兴（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_huang_shen_desc |  |
| 44 | `CHI_jiang_baili` | advisor/theorist | direct | 蒋百里（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_jiang_baili_desc |  |
| 45 | `CHI_ju_zheng` | advisor/political_advisor | direct | 居正（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_ju_zheng_desc |  |
| 46 | `CHI_kwong_jiang` | advisor/political_advisor | instance[1] | 邝江（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_kwong_jiang_desc |  |
| 47 | `CHI_kwong_jiang` | advisor/political_advisor | instance[2] | 邝江（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_kwong_jiang_desc |  |
| 48 | `CHI_li_huang` | advisor/political_advisor | direct | 李璜（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_li_huang_desc |  |
| 49 | `CHI_li_zongren` | advisor/army_chief | direct | 李宗仁（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 GXC_li_zongren（desc=GXC_li_zongren_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_li_zongren_desc |  |
| 50 | `CHI_liang_shuming` | advisor/political_advisor | direct | 梁漱溟（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_liang_shuming_desc |  |
| 51 | `CHI_lin_sen` | advisor/political_advisor | instance[1] | 林森（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_lin_sen_desc |  |
| 52 | `CHI_lin_sen` | advisor/political_advisor | instance[2] | 林森（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_lin_sen_desc |  |
| 53 | `CHI_mao_renfeng` | advisor/political_advisor | direct | 毛人凤（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_mao_renfeng_desc |  |
| 54 | `CHI_mei_siping` | advisor/political_advisor | direct | 梅思平（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_mei_siping_desc |  |
| 55 | `CHI_shen_honglie` | advisor/theorist | direct | 沈鸿烈（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_shen_honglie_desc |  |
| 56 | `CHI_shen_junru` | advisor/political_advisor | direct | 沈钧儒（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_shen_junru_desc |  |
| 57 | `CHI_shi_liang` | advisor/political_advisor | direct | 史良（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_shi_liang_desc |  |
| 58 | `CHI_soong_mei_ling` | advisor/political_advisor | instance[1] | 宋美龄（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_soong_mei_ling_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_soong_mei_ling_desc |  |
| 59 | `CHI_soong_mei_ling` | advisor/political_advisor | instance[2] | 宋美龄（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_soong_mei_ling_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_soong_mei_ling_desc |  |
| 60 | `CHI_sun_fo` | advisor/political_advisor | direct | 孙科（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_sun_fo_desc |  |
| 61 | `CHI_sun_li_jen` | advisor/high_command | instance[1] | 孙立人（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_sun_li_jen_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_sun_li_jen_desc |  |
| 62 | `CHI_symeon_du` | advisor/political_advisor | direct | 西麦翁·杜润臣（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_symeon_du_desc |  |
| 63 | `CHI_t_v_soong` | advisor/political_advisor | instance[1] | 宋子文（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_t_v_soong_desc |  |
| 64 | `CHI_t_v_soong` | advisor/political_advisor | instance[2] | 宋子文（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_t_v_soong_desc |  |
| 65 | `CHI_tao_xingzhi` | advisor/political_advisor | direct | 陶行知（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_tao_xingzhi_desc |  |
| 66 | `CHI_teng_chie` | advisor/army_chief | direct | 滕杰（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_teng_chie_desc |  |
| 67 | `CHI_wang_chonghui` | advisor/political_advisor | direct | 王宠惠（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_wang_chonghui_desc |  |
| 68 | `CHI_wang_shuming` | advisor/air_chief | direct | 王叔铭（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 GXC_wang_shuming（desc=CHI_wang_shuming_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_wang_shuming_desc |  |
| 69 | `CHI_weng_wenhao` | advisor/political_advisor | instance[1] | 翁文灏（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（CHI_weng_wenhao_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 CHI_weng_wenhao_desc |  |
| 70 | `CHI_xiao_yisu` | advisor/high_command | instance[1] | 萧毅肃（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_xiao_yisu_desc |  |
| 71 | `CHI_xiao_yisu` | advisor/high_command | instance[2] | 萧毅肃（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_xiao_yisu_desc |  |
| 72 | `CHI_y_c_james_yen` | advisor/political_advisor | direct | 晏阳初（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_y_c_james_yen_desc |  |
| 73 | `CHI_yu_hanmou` | advisor/high_command | direct | 余汉谋（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 GND_yu_hanmou（desc=GND_yu_hanmou_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_yu_hanmou_desc |  |
| 74 | `CHI_zhang_qun` | advisor/political_advisor | direct | 张群（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_zhang_qun_desc |  |
| 75 | `CHI_zhang_zhizhong` | advisor/high_command | direct | 张治中（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_zhang_zhizhong_desc |  |
| 76 | `CHI_zhou_fohai` | advisor/political_advisor | direct | 周佛海（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_zhou_fohai_desc |  |
| 77 | `CHI_zhu_de` | advisor/army_chief | direct | 朱德（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 PRC_zhu_de（desc=PRC_zhu_de_commander_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 CHI_zhu_de_desc |  |
| 78 | `CHI_zhu_jiahua` | advisor/political_advisor | direct | 朱家骅（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_zhu_jiahua_desc |  |
| 79 | `CHI_zou_lu` | advisor/political_advisor | direct | 邹鲁（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_zou_lu_desc |  |
| 80 | `CHI_zou_taofen` | advisor/political_advisor | direct | 邹韬奋（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 CHI_zou_taofen_desc |  |

### PRC

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 81 | `PRC_bo_gu` | advisor/political_advisor | direct | 博古（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_bo_gu_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_bo_gu_desc |  |
| 82 | `PRC_bo_yibo` | advisor/political_advisor | instance[1] | 薄一波（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_bo_yibo_desc |  |
| 83 | `PRC_bo_yibo` | advisor/political_advisor | instance[2] | 薄一波（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_bo_yibo_desc |  |
| 84 | `PRC_cai_chang` | advisor/political_advisor | direct | 蔡畅（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_cai_chang_desc |  |
| 85 | `PRC_chang_qiankun` | advisor/air_chief | direct | 常乾坤（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_chang_qiankun_desc |  |
| 86 | `PRC_chen_changhao` | advisor/political_advisor | direct | 陈昌浩（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_chen_changhao_desc |  |
| 87 | `PRC_chen_geng` | advisor/high_command | instance[1] | 陈赓（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_chen_geng_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_chen_geng_desc |  |
| 88 | `PRC_chen_geng` | advisor/high_command | instance[2] | 陈赓（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_chen_geng_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_chen_geng_desc |  |
| 89 | `PRC_chen_shaomin` | advisor/political_advisor | direct | 陈少敏（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_chen_shaomin_desc |  |
| 90 | `PRC_chen_tanqiu` | advisor/political_advisor | instance[1] | 陈潭秋（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_chen_tanqiu_desc |  |
| 91 | `PRC_chen_tanqiu` | advisor/political_advisor | instance[2] | 陈潭秋（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_chen_tanqiu_desc |  |
| 92 | `PRC_chen_yi` | advisor/high_command | instance[1] | 陈毅（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_chen_yi_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_chen_yi_desc |  |
| 93 | `PRC_chen_yi` | advisor/high_command | instance[2] | 陈毅（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_chen_yi_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_chen_yi_desc |  |
| 94 | `PRC_chen_yun` | advisor/political_advisor | instance[1] | 陈云（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_chen_yun_desc |  |
| 95 | `PRC_chen_yun` | advisor/political_advisor | instance[2] | 陈云（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_chen_yun_desc |  |
| 96 | `PRC_chu_qing` | advisor/high_command | direct | 楚青（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_chu_qing_desc |  |
| 97 | `PRC_deng_fa` | advisor/political_advisor | instance[1] | 邓发（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_deng_fa_desc |  |
| 98 | `PRC_deng_fa` | advisor/political_advisor | instance[2] | 邓发（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_deng_fa_desc |  |
| 99 | `PRC_deng_xiaoping` | advisor/political_advisor | instance[1] | 邓小平（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_deng_xiaoping_desc |  |
| 100 | `PRC_deng_xiaoping` | advisor/political_advisor | instance[2] | 邓小平（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_deng_xiaoping_desc |  |
| 101 | `PRC_deng_yingchao` | advisor/political_advisor | direct | 邓颖超（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_deng_yingchao_desc |  |
| 102 | `PRC_deng_zihiu` | advisor/political_advisor | direct | 邓子恢（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_deng_zihiu_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_deng_zihiu_desc |  |
| 103 | `PRC_dong_biwu` | advisor/political_advisor | instance[1] | 董必武（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_dong_biwu_desc |  |
| 104 | `PRC_dong_biwu` | advisor/political_advisor | instance[2] | 董必武（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_dong_biwu_desc |  |
| 105 | `PRC_fang_zeyi` | advisor/air_chief | direct | 方子翼（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_fang_zeyi_desc |  |
| 106 | `PRC_gao_gang` | advisor/political_advisor | instance[1] | 高岗（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_gao_gang_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_gao_gang_desc |  |
| 107 | `PRC_gao_gang` | advisor/air_chief | instance[2] | 高岗（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_gao_gang_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_gao_gang_desc |  |
| 108 | `PRC_gao_qiu` | advisor/navy_chief | direct | 高秋（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_gao_qiu_desc |  |
| 109 | `PRC_he_cheng` | advisor/high_command | direct | 贺诚（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_he_cheng_desc |  |
| 110 | `PRC_he_yuandang` | advisor/political_advisor | direct | 吴运铎（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_he_yuandang_desc |  |
| 111 | `PRC_hsia_tian` | advisor/theorist | direct | 夏天（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_hsia_tian_desc |  |
| 112 | `PRC_kang_sheng` | advisor/political_advisor | instance[1] | 康生（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_kang_sheng_desc |  |
| 113 | `PRC_kang_sheng` | advisor/political_advisor | instance[2] | 康生（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_kang_sheng_desc |  |
| 114 | `PRC_kang_sheng` | advisor/political_advisor | instance[3] | 康生（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_kang_sheng_desc |  |
| 115 | `PRC_li_lisan` | advisor/political_advisor | direct | 李立三（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_li_lisan_desc |  |
| 116 | `PRC_li_xiannian` | advisor/high_command | direct | 李先念（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_li_xiannian_desc |  |
| 117 | `PRC_li_zhen` | advisor/political_advisor | direct | 李贞（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_li_zhen_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_li_zhen_desc |  |
| 118 | `PRC_liang_shen` | advisor/high_command | direct | 梁深（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_liang_shen_desc |  |
| 119 | `PRC_lin_bojiu` | advisor/political_advisor | direct | 林伯渠（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_lin_bojiu_desc |  |
| 120 | `PRC_lin_boqu` | advisor/political_advisor | direct | 林伯渠（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_lin_boqu_desc |  |
| 121 | `PRC_liu_bocheng` | advisor/theorist | instance[1] | 刘伯承（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_liu_bocheng_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_liu_bocheng_desc |  |
| 122 | `PRC_liu_bocheng` | advisor/theorist | instance[2] | 刘伯承（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_liu_bocheng_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_liu_bocheng_desc |  |
| 123 | `PRC_liu_shaoqi` | advisor/political_advisor | instance[1] | 刘少奇（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_liu_shaoqi_desc |  |
| 124 | `PRC_liu_shaoqi` | advisor/political_advisor | instance[2] | 刘少奇（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_liu_shaoqi_desc |  |
| 125 | `PRC_liu_yalou` | advisor/air_chief | direct | 刘亚楼（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_liu_yalou_desc |  |
| 126 | `PRC_liu_yuti` | advisor/air_chief | direct | 刘玉堤（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_liu_yuti_desc |  |
| 127 | `PRC_luo_ruiqing` | advisor/political_advisor | instance[2] | 罗瑞卿（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_luo_ruiqing_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_luo_ruiqing_desc |  |
| 128 | `PRC_luo_shunchu` | advisor/navy_chief | direct | 罗舜初（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_luo_shunchu_desc |  |
| 129 | `PRC_ma_jin` | advisor/army_chief | direct | 马进（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_ma_jin_desc |  |
| 130 | `PRC_mao_zedong` | advisor/political_advisor | instance[1] | 毛泽东（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_mao_zedong_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_mao_zedong_desc |  |
| 131 | `PRC_mao_zedong` | advisor/theorist | instance[1]#2 | 毛泽东（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_mao_zedong_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_mao_zedong_desc |  |
| 132 | `PRC_mao_zemin` | advisor/political_advisor | direct | 毛泽民（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_mao_zemin_desc |  |
| 133 | `PRC_nie_rongzhen` | advisor/high_command | instance[1] | 聂荣臻（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_nie_rongzhen_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_nie_rongzhen_desc |  |
| 134 | `PRC_nie_rongzhen` | advisor/high_command | instance[2] | 聂荣臻（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_nie_rongzhen_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_nie_rongzhen_desc |  |
| 135 | `PRC_otto_braun` | advisor/army_chief | instance[1] | 李德（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_otto_braun_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_otto_braun_desc |  |
| 136 | `PRC_otto_braun` | advisor/army_chief | instance[2] | 李德（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_otto_braun_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_otto_braun_desc |  |
| 137 | `PRC_pavel_mif` | advisor/political_advisor | direct | 帕维尔·米夫（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_pavel_mif_desc |  |
| 138 | `PRC_ren_bishi` | advisor/political_advisor | direct | 任弼时（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_ren_bishi_desc |  |
| 139 | `PRC_shao_shiping` | advisor/political_advisor | direct | 邵式平（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_shao_shiping_desc |  |
| 140 | `PRC_su_yu` | advisor/army_chief | instance[1] | 粟裕（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_su_yu_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_su_yu_desc |  |
| 141 | `PRC_su_yu` | advisor/army_chief | instance[2] | 粟裕（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_su_yu_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_su_yu_desc |  |
| 142 | `PRC_wang_jiaxiang` | advisor/political_advisor | direct | 王稼祥（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_wang_jiaxiang_desc |  |
| 143 | `PRC_wang_ming` | advisor/political_advisor | direct | 王明（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_wang_ming_desc |  |
| 144 | `PRC_wang_shiwei` | advisor/political_advisor | direct | 王实味（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_wang_shiwei_desc |  |
| 145 | `PRC_wu_han` | advisor/political_advisor | direct | 吴晗（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_wu_han_desc |  |
| 146 | `PRC_wu_yuzhang` | advisor/political_advisor | direct | 吴玉章（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_wu_yuzhang_desc |  |
| 147 | `PRC_xie_juezai` | advisor/political_advisor | direct | 谢觉哉（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_xie_juezai_desc |  |
| 148 | `PRC_xu_teli` | advisor/political_advisor | direct | 徐特立（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_xu_teli_desc |  |
| 149 | `PRC_xu_xiangqian` | advisor/high_command | instance[1] | 徐向前（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_xu_xiangqian_desc |  |
| 150 | `PRC_xu_xiangqian` | advisor/high_command | instance[2] | 徐向前（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_xu_xiangqian_desc |  |
| 151 | `PRC_yang_shangkun` | advisor/high_command | direct | 杨尚昆（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_yang_shangkun_desc |  |
| 152 | `PRC_yang_zhicheng` | advisor/high_command | direct | 杨志成（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_yang_zhicheng_desc |  |
| 153 | `PRC_ye_jianying` | advisor/high_command | instance[1] | 叶剑英（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_ye_jianying_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_ye_jianying_desc |  |
| 154 | `PRC_ye_jianying` | advisor/high_command | instance[2] | 叶剑英（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_ye_jianying_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_ye_jianying_desc |  |
| 155 | `PRC_ye_jianying` | advisor/high_command | instance[3] | 叶剑英（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_ye_jianying_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_ye_jianying_desc |  |
| 156 | `PRC_zhang_guotao` | advisor/theorist | direct | 张国焘（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 CHI_zhang_guotao（desc=CHI_zhang_guotao_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；同键其他身份已挂有效desc（PRC_zhang_guotao_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_zhang_guotao_desc |  |
| 157 | `PRC_zhang_guotao` | advisor/political_advisor | direct#2 | 张国焘（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 CHI_zhang_guotao（desc=CHI_zhang_guotao_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；同键其他身份已挂有效desc（PRC_zhang_guotao_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_zhang_guotao_desc |  |
| 158 | `PRC_zhang_wei` | advisor/theorist | direct | 张伟（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_zhang_wei_desc |  |
| 159 | `PRC_zhang_wentian` | advisor/political_advisor | direct | 张闻天（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_zhang_wentian_leader_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_zhang_wentian_desc |  |
| 160 | `PRC_zhou_enlai` | advisor/political_advisor | instance[1] | 周恩来（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_zhou_enlai_desc |  |
| 161 | `PRC_zhou_enlai` | advisor/political_advisor | instance[2] | 周恩来（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_zhou_enlai_desc |  |
| 162 | `PRC_zhou_enlai` | advisor/political_advisor | instance[3] | 周恩来（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 PRC_zhou_enlai_desc |  |
| 163 | `PRC_zhu_de` | advisor/army_chief | instance[1] | 朱德（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_zhu_de_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_zhu_de_desc |  |
| 164 | `PRC_zhu_de` | advisor/army_chief | instance[2] | 朱德（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_zhu_de_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_zhu_de_desc |  |
| 165 | `PRC_zuo_quan` | advisor/high_command | instance[1] | 左权（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_zuo_quan_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_zuo_quan_desc |  |
| 166 | `PRC_zuo_quan` | advisor/high_command | instance[2] | 左权（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（PRC_zuo_quan_commander_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 PRC_zuo_quan_desc |  |

### GXC

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 167 | `GXC_li_ting` | country_leader | direct | Li Ting（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 168 | `GXC_liu_peng` | country_leader | direct | Liu Peng（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 169 | `GXC_zhang_lu` | country_leader | direct | Zhang Lü（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 170 | `GXC_chen_jitang` | field_marshal | instance[2] | 陈济棠（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（GXC_chen_jitang_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 GXC_chen_jitang_desc |  |
| 171 | `GXC_chen_jitang` | advisor/army_chief | instance[1] | 陈济棠（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（GXC_chen_jitang_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 GXC_chen_jitang_desc |  |
| 172 | `GXC_li_zongren` | advisor/political_advisor | direct | 李宗仁（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（GXC_li_zongren_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 GXC_li_zongren_desc |  |

### MAN

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 173 | `MAN_aisin_gioro_puyi` | advisor/theorist | direct | 爱新觉罗·溥仪（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（MAN_aisin_gioro_puyi_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 MAN_aisin_gioro_puyi_desc |  |
| 174 | `MAN_ding_jianxiu` | advisor/political_advisor | direct | 丁鉴修（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 MAN_ding_jianxiu_desc |  |
| 175 | `MAN_sun_qichang` | advisor/political_advisor | direct | 孙其昌（中文名） | 疑似真人 | 有中文显示名；本地化中已存在可用正文键 MAN_sun_qichang_desc |  |
| 176 | `MAN_zhang_jinghui` | advisor/political_advisor | direct | 张景惠（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（MAN_zhang_jinghui_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 MAN_zhang_jinghui_desc |  |

### MEN

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 177 | `MEN_chin_yung_chang` | advisor/political_advisor | direct | 金永昌（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（MEN_chin_yung_chang_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 MEN_chin_yung_chang_desc |  |

### SHX

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 178 | `SHX_fu_zuoyi` | advisor/political_advisor | direct | 傅作义（中文名） | 疑似key改名 | 当前源码存在已覆盖人物 CHI_fu_zuoyi（desc=CHI_fu_zuoyi_desc，匹配方式：跨TAG同后缀），疑为同一人跨TAG或改名；注意跨TAG同后缀也可能是同名不同人（典型如陈仪CHI/陈毅PRC），需核对人物身份；本地化中已存在可用正文键 SHX_fu_zuoyi_desc→CHI_fu_zuoyi_desc |  |
| 179 | `SHX_yan_xishan` | advisor/army_chief | direct | 阎锡山（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（SHX_yan_xishan_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 SHX_yan_xishan_desc |  |

### SIK

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 180 | `SIK_kwong_jin` | country_leader | direct | Kwong Jin（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 181 | `SIK_liang_jiang` | country_leader | direct | Liang Jiang（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 182 | `SIK_luo_wei` | country_leader | direct | Luo Wei（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 183 | `SIK_chiang_yufen` | corps_commander | direct | Chiang Yu-fen（拉丁名） | 疑似真人 | 有拉丁显示名且身份重要；注意：MOD名称覆盖白名单已将其恢复拉丁名（此前批次按未核实人物处理过名字），需人工核对是否真人 |  |

### XSM

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 184 | `XSM_hsia_jin` | country_leader | direct | Hsia Jin（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 185 | `XSM_hsia_sun` | country_leader | direct | Hsia Sun（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 186 | `XSM_mao_sun` | country_leader | direct | Mao Sun（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 187 | `XSM_han_yimu` | corps_commander | direct | Han Yimu（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 188 | `XSM_ma_bufang` | advisor/army_chief | direct | 马步芳（中文名） | 疑似真人 | 有中文显示名；同键其他身份已挂有效desc（XSM_ma_bufang_desc，正文已存在），仅本身份未挂；本地化中已存在可用正文键 XSM_ma_bufang_desc |  |

### YUN

| 序号 | 人物key | 身份 | 路径 | 显示名（类型） | 机器初判 | 初判依据 | 裁定 |
|---|---|---|---|---|---|---|---|
| 189 | `YUN_cheng_peng` | country_leader | direct | Cheng Peng（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 190 | `YUN_hsia_wu` | country_leader | direct | Hsia Wu（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |
| 191 | `YUN_mao_dong` | country_leader | direct | Mao Dong（拉丁名） | 疑似占位 | 拉丁拼音通用名，命名模式与已裁定36个占位人物同族；MOD名称覆盖白名单已将其恢复拉丁名（佐证同族处理） |  |

