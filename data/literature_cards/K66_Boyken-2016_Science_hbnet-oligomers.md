# [K66] Boyken 2016：埋藏氢键网络（HBnet）正交界面设计策略——判据谱系起点（降级卡：摘要级，底稿信息稀薄）

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 第 148 行，编号 **K66**（组：通用方法学；`证据级别` 列原文即写 摘要级） |
| 题目 | De novo design of protein homo-oligomers with modular hydrogen-bond network–mediated specificity |
| 作者 | Boyken SE 等——CSV 行原注：笔记原句只到『Boyken 2016 Science HBnet』，作者列表未展开 |
| 出处 | Science, 2016 · DOI 10.1126/science.aad8865（✅Crossref 核验）· PMID/PMCID 未记录 |
| 正文取回状态 | ⛔ **未获正文**。曾尝试按 PMC 号抓 EPMC fullTextXML，两次均 HTTP 500 失败（`fetch_log.tsv:108`、`:156`）；后续按 DOI 重检索遇 SSL UNEXPECTED_EOF（`fetch_log.tsv:193`）。**无一次下载成功，故无挂错行/隔离事件**；`inventory.json` K66 项 local=[]、has_fulltext=false |
| 登记底稿（本卡唯一引句来源） | `sources/baker.md`：第 66 行（[B04] 段谱系锚点句）、第 675 行（§五 缺口 4 可核谱系）、第 20 行（[B01] 段对 HBnet 用法的**全文自述转引**，非 Boyken 原文） |
| 证据级别 | **摘要级 / 未获正文**（与 CSV 行一致）。**底稿信息稀薄是本文的实情**：谱系一句 + DOI 核验 + 缺口 4 检索记录，其余全为未记录 |
| 未取到的部分 | 方法、工作流程、设计库/送测分母、命中率、实验手段、MD/QM——CSV 行 候选生成方法/候选数递减/实验命中率/Kd 等栏原值即 未记录。本卡一律写 未记录（本次未取正文），不以谱系下游（B01/B04）细节冒充 Boyken 2016 本身 |

## 1. 这篇解决什么（一句话）

**一句话（仅到 CSV 与底稿粒度）**：把**埋藏在蛋白界面内部的氢键网络（HBnet）**当作正交界面的设计策略，用于蛋白同源寡聚体的特异性控制——本项目登记它是 **HBnet 判据谱系的起点**，早于 Rosetta 时代的 [B01] LOCKR（CSV 行 在方法演进链的位置 原句）。

底稿对该文的全部直接记录止于 `sources/baker.md:66`：「再早是 Boyken 2016 Science HBnet（DOI 10.1126/science.aad8865 ✅）」，以及 `:675` 缺口 4 把它列为可核氢键设计谱系的第一环（Boyken 2016 → Maguire 2018 → Coventry 2021）。**稀薄就照实写稀薄：本卡不给出任何方法级细节。**

## 2. 难点，以及遇到问题时作者做了什么（依据登记底稿；作者自述部分未获正文，无法核验）

> 按降级卡规则：K66 的「作者做了什么」在底稿层不可核验，凡不可核处明写；可核的是**谱系下游如何继承这一判据**（转引，已点名出处）。

1. **（作者的、谱系级）埋藏极性基团在疏水界面里若不满足氢键，界面就不可设计。** 现象/证据：底稿 `:66` 记这一「埋藏极性必须成氢键」的判据后来被吸收进 ProteinMPNN/LigandMPNN 的序列似然与全原子打分。→ 作者做了什么：**Boyken 2016 本文未解决核验**（未获正文，作者侧操作无法登记）；可核的是下游继承——[B01] LOCKR 全文自述（转引，非 Boyken 原文）："we chose to design interfaces containing buried hydrogen bond networks;"（`sources/baker.md:20`），即把 HBnet 当可微调特异性的正交模块。→ 代价：起点论文自身的设计流程、通过率全部未记录。

2. **（取证级）K66 在 Baker 笔记里的存在感只有一句谱系句，行内容易被下游细节污染。** 现象/证据：CSV 行第一作者字段只能写到『Boyken 2016 Science HBnet』；实验手段/递减/命中率全部 未记录。→ 我们做了什么：本卡把 [B01]、[B04]、Maguire 2018 的每一条转引都**显式标注不是 Boyken 原文**；§3 只登记取证工作流而非实验流程（避免为凑步骤编造实验）。→ 仍留下的代价：想判定 HBnet 起点论文的实际效果，必须取回 2016 正文/SI——当前抓取通道 500/SSL 失败，缺口未闭合。

3. **（谱系核对）用户点名的 2024 年 HydrogenBonds 模型名查无此文。** 现象/证据：底稿缺口 4（`:675`）记按题名/全文检索未找到对应 Baker 2024 论文。→ 做了什么：改以可核谱系登记——Boyken 2016 Science（DOI ✅）、Maguire/Boyken/Baker/Kuhlman 2018 JCTC（10.1021/acs.jctc.8b00033 ✅，PMC5940506）、Coventry & Baker 2021 PLoS CB（10.1371/journal.pcbi.1008061 ✅），并要求用户提供名称出处再核。→ 代价：若该名称确有所指，K66 的谱系位置可能要改。

## 3. 取证方法与工作流程（本行无可登记实验流程，按取证工作流写；每步：输入 → 操作 → 判据/阈值 → 输出规模）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | CSV 行 K66（Boyken 2016，DOI ✅） | 在 `sources/baker.md` 定位全部相关段落（第 66、675 行；关联段 20、56–66） | 只取底稿原句登记，缺口一律写 未记录（本次未取正文） | 谱系锚点句 1 条 + 可核链 3 环 |
| S2 | 谱系锚点句 | 用下游 [B01]/[B04] 段落核 HBnet 判据的继承形态 | 判据：下游细节只作转引、不回写 K66 属性 | 用法形态 1 条（base-pairing 式微调，转引标注） |
| S3 | 继承形态 | 登记判据吸收去向（ProteinMPNN/LigandMPNN 序列似然与全原子打分） | 原文未给阈值（本次未取正文；全链均无阈值记录） | 谱系终点 1 条（`:66` 末句） |

**工具箱**：就 K66 本身，底稿未记任何工具名——本卡不填。就谱系（供定位用）：Rosetta 组合侧链打包 + 埋藏未满足氢键惩罚项（[B04]，`:61–62`）；HBnet 界面设计（[B01] 转引，`:20`）。

## 4. 关键数字台账（全部能在登记底稿 `sources/baker.md` 里搜到）

| 数值/条目 | 含义 | 出处 |
|---|---|---|
| "Boyken 2016 Science HBnet" | 底稿对该文的唯一直接锚点句片段 | `sources/baker.md:66` |
| "Rapid Sampling of Hydrogen Bond Networks for Computational Protein Design" | 谱系第二环 Maguire 2018 JCTC 的题目（**非 Boyken 2016 本身**） | `sources/baker.md:66` |
| "we chose to design interfaces containing buried hydrogen bond networks;" | [B01] LOCKR 全文对 HBnet 用法的自述（**转引，非 Boyken 原文**） | `sources/baker.md:20` |
| 2016；DOI 10.1126/science.aad8865 ✅ | K66 的年份与 DOI 核验状态 | CSV 行；`sources/baker.md:66`、`:675` |
| 10.1021/acs.jctc.8b00033 ✅（PMC5940506）；10.1371/journal.pcbi.1008061 ✅ | 可核谱系其余两环（Maguire 2018；Coventry 2021） | `sources/baker.md:66`、`:675` |
| 未记录 | 设计库/送测/命中/实验手段/MD-QM 全部 | CSV K66 行各栏原值；底稿无对应记录 |

## 5. 作者说了什么

**就 Boyken 2016 本身：底稿未转录任何作者自述**——一句谱系锚点句加 DOI 核验就是全部。本卡没有可登记的作者声明层级，也不从 [B01]/[B04] 的自述反推 K66 的声明。CSV 行 出处指针 的原句同样止于「sources/baker.md [B04] 再早是 Boyken 2016 Science HBnet（DOI 10.1126/science.aad8865 ✅）」。

## 6. 我们读出了什么（以下为推断，非作者原文）

1. **HBnet 是「用埋藏极性做正交性」这条设计哲学的起点**：DNA base-pairing 式的供受体微调思路（经 [B01] 转引可见其形态）后来被吸收为通用打分项——一个具体界面策略变成了序列设计器的先验。判据谱系的研究价值高于一场战役的价值。
2. **对本项目最可操作的读法**：任何设计要求里出现埋藏极性（氢键、配位、催化侧链排布）时，「极性必须有归宿」应作为可判的定性检查项——这正是我们界面/活性位设计里少掉的一类负约束。
3. **稀薄行就该长这样**：K66 卡的意义在于诚实标注哪些是起点论文可核的、哪些是下游转引的；把转引写成原文是这类卡最容易犯的错。把握度：对「底稿稀薄」高；对「2016 正文里有什么」零。

## 7. 局限

- 降级 + 稀薄：方法/工作流/数字全缺；作者字段不完整（只到 Boyken SE 等）。
- 抓取通道对 Science 2016 老文失败（HTTP 500 / SSL），非「权威阴性」——换通道（如正确 PMCID 路线）后应重取。
- 无挂错行事件，但也意味着连「疑似全文」都不存在。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**：
1. 「埋藏极性必须有氢键归宿」作为**定性负约束**进入我们的界面/活性位设计检查表：设计位点里裸露的供受体若无配对对象，即视为设计缺陷信号（不依赖任何数值阈值）。
2. 「模块化供受体编辑调特异性」的形态可借鉴到催化位点：若要区分两枚相似底物/两态竞争，改氢键供受体组合比改形状互补更可控——这是我们该记的**做法**，不是数字。

**不可迁移（为什么不能照搬）**：
1. 本文无任何命中率/阈值可引；寡聚体界面特异性的成敗判据与酶活判据不同量纲，禁止互抄（本库判据 §2）。
2. HBnet 惩罚已被吸收进序列模型/打分器这件事，不能反过来当作「我们的序列设计器已覆盖该判据」的免检理由——吸收程度未核。

## 9. 溯源与自检

引句底稿: sources/baker.md

- **本卡是降级卡**：K66 未获正文（抓取两次 HTTP 500 + 一次 SSL 失败，`fetch_log.tsv:108`、`:156`、`:193`；`inventory.json` local=[]）。与 B13/B36 不同，**本文从未成功下载过全文，不存在挂错行隔离事件**。降级卡引句规则（≥2 条、逐字命中登记底稿）；本卡共 3 条逐字引句，全部命中 `sources/baker.md`（第 66 行两条、第 20 行一条；后者已在卡内多处显式标注为 [B01] 转引而非 Boyken 原文）。
- **登记底稿核对**：`sources_map.json` K66 项只登记 `sources/baker.md`（实存）。对照行号：`:66`（[B04] 段谱系句）、`:675`（缺口 4）、`:20`（[B01] 段转引）。CSV 行：`data/protein_design_literature.csv:148`（证据级别=摘要级）。
- **门禁自检**：命令 `cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K66" --no-report`。本卡未改 CSV、`sources/*.md`、样板卡、`scripts/`，未做网络抓取。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 2 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（降级卡：摘要级，未获正文；底稿信息稀薄）
target=埋藏氢键网络（HBnet）作为正交界面设计策略；蛋白同源寡聚体的特异性
backbone_generation=未记录（本次未取正文；底稿未记该方法细节）
computational_filters=HBnet 设计（谱系形态经 [B01]/[B04] 转引可核；Boyken 2016 本文判据细节未记录）
thresholds=未记录（原文未给阈值；本次未取正文）
md_used=未记录（CSV 行原值；无正文无从判定）
qm_used=否（CSV 行原值；底稿未见 QM 记录）
experimental_methods=未记录（本次未取正文）
pipeline_counts=未记录（底稿只记谱系锚点句）
hit_rate=未记录（禁止引用为成功率）
best_metric=未记录
cost_or_stat_note=Baker 笔记仅记为再早的 HBnet 锚点（DOI 已核验），未记命中率/实验数字；缺口 4：2024 年 HydrogenBonds 模型名未检索到，可核谱系为 Boyken 2016 → Maguire 2018（K65）→ Coventry 2021（B04）
role_in_timeline=HBnet 判据谱系起点，早于 Rosetta 时代的 [B01] LOCKR；该判据后被吸收进 ProteinMPNN/LigandMPNN 序列似然与全原子打分
source_pointer=sources/baker.md:66（[B04] 段谱系句）、:675（缺口 4 可核谱系）、:20（[B01] 段 HBnet 用法，转引非 Boyken 原文）；DOI 10.1126/science.aad8865 ✅Crossref
CSV回填-->
