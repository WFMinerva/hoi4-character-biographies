# 已确认的人工裁定与长期例外

> 总入口：根目录`AGENTS.md`；当前版本状态以`docs/CURRENT_BASELINE.md`为准。

本文件只记录已明确确认、会影响后续自动判断的裁定。新的裁定应同时更新`workbench/decisions/human_decisions.json`，并保留对应的`ledger`标记；审计会双向核对条目编号和状态。

## 长期项目裁定

1. 主线是纯人物小传，不主动恢复地区事件、接收将领、战争文本或其他玩法。 <!-- ledger:rule:project_pure_bio status=confirmed -->
2. 默认测试1936和1939剧本。 <!-- ledger:rule:scenarios status=confirmed -->
3. C类非领袖原则上不写；科学家默认不写。 <!-- ledger:rule:class_c_nonleader status=confirmed --><!-- ledger:rule:scientists status=confirmed -->
4. AI或外部写手正文必须经人工审核后才能入包。 <!-- ledger:rule:ai_text_review status=confirmed -->
5. 完整版聚焦动态显示覆盖；兼容版不为运行时人物覆盖原版国策、事件、决议和国家历史。 <!-- ledger:rule:edition_scope status=confirmed -->
6. 完整版和兼容版不能同时启用。 <!-- ledger:rule:editions_mutually_exclusive status=confirmed -->
7. 统一GUI Tooltip方案已终止，不再作为主线。 <!-- ledger:rule:gui_tooltip_route status=closed -->
8. 正文超过500字符不视为问题，`check_text_quality`的超字数警告仅提示、不需要精简或整改。 <!-- ledger:rule:long_bio_warning status=confirmed -->

## v130c6—v130c7专项裁定

### 傅作义

- 真人，不属于占位人物。
- 中国陆军将领正文主键：`CHI_fu_zuoyi_desc`。
- 晋系政治顾问通过`SHX_fu_zuoyi_desc`别名复用主键。
- 后续修改傅作义只维护主键，不建立第二套正文。 <!-- ledger:entity:fu_zuoyi status=confirmed -->

### 晋系、蒙疆、满洲国占位角色

- 已裁定的一批占位非领袖不写小传。
- 原版简中误导性中文名恢复拉丁字母原名。
- 傅作义是该批次真人例外，保留中文名和正文。

### 溥仪

- 静态正文主键：`MAN_aisin_gioro_puyi_desc`。
- 完整版动态元帅或动态角色路径必须复用该正文。
- 不改变人物技能、特质、国策和上台逻辑。 <!-- ledger:entity:aisin_gioro_puyi status=confirmed -->

### 醍醐忠重

- 当前人工审定正文主键：`CBIO_JAP_tadashige_daigo_desc`。
- 当前正文明确记载坤甸事件、指挥责任、战后审判和处决，不得被旧版短文覆盖。 <!-- ledger:entity:tadashige_daigo status=confirmed -->

## v130d专项裁定（档1静态身份对账）

### 档1范围裁定

- 档1疑似漏写共191条。其中177条已有现成正文键：用户明确不逐条审查，维持现状，不批量挂接。
- 14条无现成正文条目中，12条拉丁通用名维持现状（拉丁名、不写传、不扩充占位裁定）。
- 其余2条经用户提供的史料线索核实为真人，进入写传流程（见下）。

### Chiang Yu-fen（SIK）→ 蒋有芬

- 真人，中文名蒋有芬：《新疆百科》《新疆历史》有专条，原版官方简中同此写法。
- 生平：辽宁人，东北抗日义勇军将领，1933年假道苏联入疆；1937年任喀什警备司令部参谋长、代理司令，平定麻木提叛乱、追击马虎山第一旅；后任喀什区行政长；1941年任阿山军区总指挥；1942年在阴谋暴动案中被捕，结局无可靠记载不写。
- 已从拉丁名白名单移除、恢复中文名；正文已经用户审定入包，主键`SIK_chiang_yufen_desc`。 <!-- ledger:entity:chiang_yu_fen status=confirmed -->

### Han Yimu（XSM）→ 韩乙奴

- 真人，中文名韩乙奴：原版官方简中同此写法，查加沟战斗有多条中文史料（县志口径、烈士名录、马继援密信研究）佐证。
- 生平：青海循化撒拉族，马步芳部下；1949年12月13日与韩有福残部在循化查加沟暴乱，杀害解放军干部战士98人，三日后被清剿溃散。
- 英文维基称军官、中文来源称保长/县长，职务记载不一致，正文不坐实职务；1958年结局仅见自媒体，不采用。
- 用户曾提供的西南剿匪条目线索经全文核对不成立，不得以该战役为据。
- 已从拉丁名白名单移除、恢复中文名；正文已经用户审定入包，主键`XSM_han_yimu_desc`。 <!-- ledger:entity:han_yimu status=confirmed -->

### 傅作义、溥仪身份补挂

- 傅作义：SHX政治顾问身份块已补挂`SHX_fu_zuoyi_desc`（别名复用主键，原裁定不变）。
- 溥仪：MAN理论家顾问身份块已补挂`MAN_aisin_gioro_puyi_desc`（复用主键，原裁定不变）。

### 七个国家历史文件

- EGY、ISR、JOR、LEB、LIB、PAL、SYR全部保留。
- 它们保护18个运行时创建领袖的小传。 <!-- ledger:protected:group_1 status=confirmed -->
- 除非基于新游戏版本重新完成逐文件语义审计，不得列入自动删除或减负候选。

## 2026-07-30维多利亚·路易丝身份修订

### Viktoria Luise（GER）

- 原版角色`GER_victoria`的头像资产、事件文本和女皇继位路径均指向维多利亚·路易丝（1892—1980），即威廉二世的独女；旧正文误写为威廉二世之妹维多利亚公主（1866—1929），属于同名皇室人物身份错配。
- 正文主键保持`CBIO_GER_victoria_desc`不变；只替换正文，不改角色、事件、国策、特质或继位逻辑。
- 2026年7月30日用户已逐字审定修订正文；正文记载其婚姻、退位后的居所、署名回忆录的代笔争议，以及威斯巴登市历史专家委员会对其粉饰纳粹时期经历的结论。 <!-- ledger:entity:viktoria_luise status=confirmed -->

## 状态裁定

- v130c7在原交接单中仍称测试版，是因为交接单早于实机确认。
- 用户后续已实机确认并上传工坊，`v130c7-stable`成为当时的稳定基准；当前稳定基准已更新为`v130g-stable`（2026-11-02，见`docs/CURRENT_BASELINE.md`）。
- 历史文档不得反向覆盖该状态。

<!-- ledger:placeholder:placeholder_name_restores status=confirmed -->
