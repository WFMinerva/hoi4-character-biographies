# 档1疑似真人复核表（124名唯一人物）——已关闭：全量已覆盖

**2026-07-27 复核结论（用户指出后二次核实）：本表"未挂"判定为机器误报，124 人全部已有游戏内显示路径，无需任何补挂。**

- 误判原因：底账只检查身份块内显式 `desc =`，未计入顾问/理论家/部长界面自动读取 `<idea_token>_desc` 本地化的路径（见 docs/archive/PROJECT_RULES_FULL.md 第24.5节，历史参考）。
- 二次核实方法：对 124 名唯一人物逐一检查其全部 idea_token 对应的 `_desc` 本地化键及显式 desc 引用，123 人脚本验证通过，张闻天（PRC_zhang_wentian_desc 存在）手动确认。
- 此结果与 v130d"有现成正文键维持现状、不批量挂接"裁定一致：那些键本就通过 idea_token 路径生效。

以下为原始生成数据，仅留档，不作为工作清单。

---

~~说明：本表由 v130d_tier1_ruling_sheet.csv 疑似真人 162 行按人物去重生成（同一人物多个未挂身份合并）。~~

- 全部人物在本地化中已有现成正文键。
- v130d 已裁定：有现成正文键的维持现状、不批量挂接（docs/HUMAN_DECISIONS.md）。
- 溥仪理论家、蒋有芬两行已在 v130d 修复，下表标注。

| TAG | 显示名 | 人物key | 未挂身份 | 现成正文键 |
|---|---|---|---|---|
| PRC | 博古 | PRC_bo_gu | political_advisor | — |
| PRC | 薄一波 | PRC_bo_yibo | political_advisor | — |
| PRC | 蔡畅 | PRC_cai_chang | political_advisor | — |
| PRC | 常乾坤 | PRC_chang_qiankun | air_chief | — |
| PRC | 陈昌浩 | PRC_chen_changhao | political_advisor | — |
| PRC | 陈赓 | PRC_chen_geng | high_command | — |
| PRC | 陈少敏 | PRC_chen_shaomin | political_advisor | — |
| PRC | 陈潭秋 | PRC_chen_tanqiu | political_advisor | — |
| PRC | 陈毅 | PRC_chen_yi | high_command | — |
| PRC | 陈云 | PRC_chen_yun | political_advisor | — |
| PRC | 楚青 | PRC_chu_qing | high_command | — |
| PRC | 邓发 | PRC_deng_fa | political_advisor | — |
| PRC | 邓小平 | PRC_deng_xiaoping | political_advisor | — |
| PRC | 邓颖超 | PRC_deng_yingchao | political_advisor | — |
| PRC | 邓子恢 | PRC_deng_zihiu | political_advisor | — |
| PRC | 董必武 | PRC_dong_biwu | political_advisor | — |
| PRC | 方子翼 | PRC_fang_zeyi | air_chief | — |
| PRC | 高岗 | PRC_gao_gang | political_advisor、air_chief | — |
| PRC | 高秋 | PRC_gao_qiu | navy_chief | — |
| PRC | 贺诚 | PRC_he_cheng | high_command | — |
| PRC | 吴运铎 | PRC_he_yuandang | political_advisor | — |
| PRC | 夏天 | PRC_hsia_tian | theorist | — |
| PRC | 康生 | PRC_kang_sheng | political_advisor | — |
| PRC | 李立三 | PRC_li_lisan | political_advisor | — |
| PRC | 李先念 | PRC_li_xiannian | high_command | — |
| PRC | 李贞 | PRC_li_zhen | political_advisor | — |
| PRC | 梁深 | PRC_liang_shen | high_command | — |
| PRC | 林伯渠 | PRC_lin_bojiu | political_advisor | — |
| PRC | 林伯渠 | PRC_lin_boqu | political_advisor | — |
| PRC | 刘伯承 | PRC_liu_bocheng | theorist | — |
| PRC | 刘少奇 | PRC_liu_shaoqi | political_advisor | — |
| PRC | 刘亚楼 | PRC_liu_yalou | air_chief | — |
| PRC | 刘玉堤 | PRC_liu_yuti | air_chief | — |
| PRC | 罗瑞卿 | PRC_luo_ruiqing | political_advisor | — |
| PRC | 罗舜初 | PRC_luo_shunchu | navy_chief | — |
| PRC | 马进 | PRC_ma_jin | army_chief | — |
| PRC | 毛泽东 | PRC_mao_zedong | political_advisor、theorist | — |
| PRC | 毛泽民 | PRC_mao_zemin | political_advisor | — |
| PRC | 聂荣臻 | PRC_nie_rongzhen | high_command | — |
| PRC | 李德 | PRC_otto_braun | army_chief | — |
| PRC | 帕维尔·米夫 | PRC_pavel_mif | political_advisor | — |
| PRC | 任弼时 | PRC_ren_bishi | political_advisor | — |
| PRC | 邵式平 | PRC_shao_shiping | political_advisor | — |
| PRC | 粟裕 | PRC_su_yu | army_chief | — |
| PRC | 王稼祥 | PRC_wang_jiaxiang | political_advisor | — |
| PRC | 王明 | PRC_wang_ming | political_advisor | — |
| PRC | 王实味 | PRC_wang_shiwei | political_advisor | — |
| PRC | 吴晗 | PRC_wu_han | political_advisor | — |
| PRC | 吴玉章 | PRC_wu_yuzhang | political_advisor | — |
| PRC | 谢觉哉 | PRC_xie_juezai | political_advisor | — |
| PRC | 徐特立 | PRC_xu_teli | political_advisor | — |
| PRC | 徐向前 | PRC_xu_xiangqian | high_command | — |
| PRC | 杨尚昆 | PRC_yang_shangkun | high_command | — |
| PRC | 杨志成 | PRC_yang_zhicheng | high_command | — |
| PRC | 叶剑英 | PRC_ye_jianying | high_command | — |
| PRC | 张伟 | PRC_zhang_wei | theorist | — |
| PRC | 张闻天 | PRC_zhang_wentian | political_advisor | — |
| PRC | 周恩来 | PRC_zhou_enlai | political_advisor | — |
| PRC | 朱德 | PRC_zhu_de | army_chief | — |
| PRC | 左权 | PRC_zuo_quan | high_command | — |
| CHI | 薄一波 | CHI_bo_yibo | theorist | — |
| CHI | 陈策 | CHI_chan_chak | navy_chief | — |
| CHI | 张嘉璈 | CHI_chang_kia_ngau | political_advisor | — |
| CHI | 陈璧君 | CHI_chen_bijun | political_advisor | — |
| CHI | 陈诚 | CHI_chen_cheng | high_command | — |
| CHI | 陈公博 | CHI_chen_gongbo | political_advisor | — |
| CHI | 陈果夫 | CHI_chen_guofu | political_advisor | — |
| CHI | 陈立夫 | CHI_chen_lifu | political_advisor | — |
| CHI | 陈庆云 | CHI_chen_qingyun | theorist | — |
| CHI | 陈绍宽 | CHI_chen_shaokuan | navy_chief | — |
| CHI | 蒋经国 | CHI_chiang_ching_kuo | political_advisor | — |
| CHI | 褚民谊 | CHI_chu_minying | political_advisor | — |
| CHI | 戴季陶 | CHI_dai_jitao | political_advisor | — |
| CHI | 戴笠 | CHI_dai_li | political_advisor | — |
| CHI | 杜月笙 | CHI_du_yuesheng | political_advisor | — |
| CHI | 方子翼 | CHI_fang_zeyi | theorist | — |
| CHI | 高志航 | CHI_gao_zhihang | high_command | — |
| CHI | 高宗武 | CHI_gao_zongwu | political_advisor | — |
| CHI | 桂永清 | CHI_gui_yongqing | high_command | — |
| CHI | 孔祥熙 | CHI_h_h_kung | political_advisor | — |
| CHI | 何应钦 | CHI_he_yingqin | army_chief | — |
| CHI | 徐焕昇 | CHI_hsu_huang_sheng | high_command | — |
| CHI | 胡汉民 | CHI_hu_hanmin | political_advisor | — |
| CHI | 黄金荣 | CHI_huang_jinrong | political_advisor | — |
| CHI | 黄琪翔 | CHI_huang_qixiang | army_chief | — |
| CHI | 黄兴 | CHI_huang_shen | theorist | — |
| CHI | 蒋百里 | CHI_jiang_baili | theorist | — |
| CHI | 居正 | CHI_ju_zheng | political_advisor | — |
| CHI | 邝江 | CHI_kwong_jiang | political_advisor | — |
| CHI | 李璜 | CHI_li_huang | political_advisor | — |
| CHI | 梁漱溟 | CHI_liang_shuming | political_advisor | — |
| CHI | 林森 | CHI_lin_sen | political_advisor | — |
| CHI | 毛人凤 | CHI_mao_renfeng | political_advisor | — |
| CHI | 梅思平 | CHI_mei_siping | political_advisor | — |
| CHI | 沈鸿烈 | CHI_shen_honglie | theorist | — |
| CHI | 沈钧儒 | CHI_shen_junru | political_advisor | — |
| CHI | 史良 | CHI_shi_liang | political_advisor | — |
| CHI | 宋美龄 | CHI_soong_mei_ling | political_advisor | — |
| CHI | 孙科 | CHI_sun_fo | political_advisor | — |
| CHI | 孙立人 | CHI_sun_li_jen | high_command | — |
| CHI | 西麦翁·杜润臣 | CHI_symeon_du | political_advisor | — |
| CHI | 宋子文 | CHI_t_v_soong | political_advisor | — |
| CHI | 陶行知 | CHI_tao_xingzhi | political_advisor | — |
| CHI | 滕杰 | CHI_teng_chie | army_chief | — |
| CHI | 王宠惠 | CHI_wang_chonghui | political_advisor | — |
| CHI | 翁文灏 | CHI_weng_wenhao | political_advisor | — |
| CHI | 萧毅肃 | CHI_xiao_yisu | high_command | — |
| CHI | 晏阳初 | CHI_y_c_james_yen | political_advisor | — |
| CHI | 张群 | CHI_zhang_qun | political_advisor | — |
| CHI | 张治中 | CHI_zhang_zhizhong | high_command | — |
| CHI | 周佛海 | CHI_zhou_fohai | political_advisor | — |
| CHI | 朱家骅 | CHI_zhu_jiahua | political_advisor | — |
| CHI | 邹鲁 | CHI_zou_lu | political_advisor | — |
| CHI | 邹韬奋 | CHI_zou_taofen | political_advisor | — |
| MAN | 爱新觉罗·溥仪（已修复） | MAN_aisin_gioro_puyi | theorist | — |
| MAN | 丁鉴修 | MAN_ding_jianxiu | political_advisor | — |
| MAN | 孙其昌 | MAN_sun_qichang | political_advisor | — |
| MAN | 张景惠 | MAN_zhang_jinghui | political_advisor | — |
| GXC | 陈济棠 | GXC_chen_jitang | field_marshal、army_chief | — |
| GXC | 李宗仁 | GXC_li_zongren | political_advisor | — |
| MEN | 金永昌 | MEN_chin_yung_chang | political_advisor | — |
| SHX | 阎锡山 | SHX_yan_xishan | army_chief | — |
| SIK | Chiang Yu-fen（已修复） | SIK_chiang_yufen | corps_commander | — |
| XSM | 马步芳 | XSM_ma_bufang | army_chief | — |
