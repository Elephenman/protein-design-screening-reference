# [K50] Siegel 2010 Diels-Alderase：QM/theozyme 进入设计漏斗的正规形态（降级卡：摘要级，未获正文）

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 第 132 行，编号 **K50**（组：通用方法学; 口径对照；`证据级别` 列原文即写 摘要级） |
| 题目 | Computational Design of an Enzyme Catalyst for a Stereoselective Bimolecular Diels-Alder Reaction |
| 作者 | Siegel JB, Zanghellini A, … Hilvert D, Gelb MH, Stoddard BL, Houk KN, Michael FE, Baker D（跨 Baker/Hilvert/Houk 三组联合） |
| 出处 | Science, 2010 · DOI 10.1126/science.1190239（✅Crossref 核验）· PMID/PMCID 未记录（CSV 行原值） |
| 正文取回状态 | ⛔ **未获正文**。曾按 PMC3241958 尝试 EPMC fullTextXML，多次 HTTP 500 失败（`fetch_log.tsv:100`、`:148`、`:186`，注记 ncbi_efetch 0 无 PMCID 可走 NCBI、biorxiv_full 0 非预印本）。**无一次下载成功，不存在挂错行/隔离事件**；`inventory.json` K50 项 local=[]、has_fulltext=false |
| 登记底稿 | `sources_map.json` K50 项登记两份：`sources/baker.md` 与 `sources/cost-benchmarks.md`。**本卡引句底稿只声明一份：`sources/baker.md`**（第 594 行经典锚点段为主，第 273/662 行 theozyme 惯例转引为辅）；cost-benchmarks §四 的数字仅作口径对照、不作引句 |
| 证据级别 | **摘要级 / 未获正文**（与 CSV 行一致）；本文在项目中的身份是「QM/theozyme 溯源锚点」，非独立战役记录 |
| 未取到的部分 | 建库规模、送测/命中数字、活性与选择性最好值、MD/QM 细节流程——CSV 行 候选生成方法/候选数递减/实验命中率/Kd 各栏原值即 未记录 |

## 1. 这篇解决什么（一句话）

**一句话（到 CSV 与底稿粒度）**：用 QM 把一个**立体选择性双分子 Diels-Alder 反应**的过渡态几何与催化基团排布定下来（theozyme），再交给 Rosetta 建库/设计酶催化剂——它回答了「QM 在设计漏斗里应该站哪个位置」：**定化学几何，不做候选排序**。

底稿对该文的全部直接记录在 `sources/baker.md:594`（附：非 Baker 组对照之后的经典锚点行）：该文作为 [B17] 参考文献原文出现在 Baker 侧正文引注中；其 **QM 角色**＝用 QM 给出过渡态几何与催化基团排布；属「化学步建模」，不是全局筛选器。CSV 行 在方法演进链的位置 同：是 Baker 侧 [B17] 引注的 theozyme 溯源锚点。

## 2. 难点，以及遇到问题时作者做了什么（依据登记底稿；作者自述部分未获正文，无法核验）

> 2010 原文细节本卡不可核验；「作者做了什么」凡超出底稿者一律写未记录，不补脑。

1. **QM 贵，不可能对成千上万候选做排序。** 现象/证据：CSV 行 成本/统计量 引用栏记 QM（Houk 组过渡态几何/能量）只作用于十几个原子的反应中心；口径对照底稿 `sources/cost-benchmarks.md:161` 同记「QM 只作用于**十几个原子的反应中心**」（该句仅作对照，不作本卡引句）。→ 作者做了什么（可核形态，底稿 `:594`）：QM 只产 theozyme 几何与催化基团排布，其后交 Rosetta 建库/设计——分工写死，QM 不进排序层。→ 仍留下的代价：theozyme 到蛋白之间的建库规模、命中率本卡全部未记录（本次未取正文）。

2. **双分子 Diels-Alder 的立体选择性靠静态几何约束未必够。** 现象/证据：CSV 行把该文归口「QM 进入设计漏斗的正规形态：定过渡态几何与催化基团排布，不做候选排序」；作者侧后续取舍底稿未记。→ 作者做了什么：**本文未解决（就本卡可见证据而言）**——底稿未转录作者对活性/选择性不达标时做了什么（无定向进化、迭代重设计的记录）。→ 代价：本文只能支撑「QM 的位置」这一结构性论断，不能支撑任何效果量论断。

3. **取证困难（我们的）：无正文 + 双底稿口径分离。** 曾按 PMC3241958 抓取三次均 HTTP 500（`fetch_log.tsv:100`、`:148`、`:186`），换 NCBI/bioRxiv 通道亦无路（同注记）；`sources/baker.md` 底稿内部该文题名出现**两种拼写**（标题级 Diels-Alderase 与引注级 Diels-Alder，见第 4 节两条引句），系转录 [B17] 参考文献列表与原锚点句之别。→ 处置：引句底稿只声明 `sources/baker.md` 一份并在 §9 写明 cost-benchmarks 不作引句来源；题名差异照实登记，不择一「修正」。

## 3. 取证方法与工作流程（非实验流程——本文未获正文，按取证工作流登记；每步：输入 → 操作 → 判据/阈值 → 输出规模）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | CSV 行 K50（Siegel 2010，DOI ✅） | 在 `sources/baker.md` 定位锚点段（第 594 行）与 theozyme 惯例段（第 273、662 行） | 只取底稿原句；正文级细节一律写 未记录（本次未取正文） | 锚点段 1 + 转引句 1 |
| S2 | 锚点句 | 与 `sources/cost-benchmarks.md:161` theozyme 行交叉对照（QM 作用范围=十几个原子反应中心） | 判据：交叉口径只进台账并标注「对照底稿，未作引句」 | QM 角色定位 1 条 |
| S3 | QM 角色定位 | 登记为 [B17]/[B18]/[B20] 谱系的上游锚点（Baker 侧正文引注关系，`:594`） | 原文未给阈值（本次未取正文；全链无阈值记录） | 谱系边 1 条（K50 → Baker 酶线） |

**工具箱**：就 K50 本身，底稿可核的只有 CSV 行 计算筛选判据 一栏：QM theozyme 几何 → Rosetta 建库/设计；是否用MD=否、是否用QM=是-化学步（CSV 行原值）。2010 原文的协议名/参数未记录。

## 4. 关键数字台账（引句全部能在 `sources/baker.md` 里搜到；对照值已标注来源）

| 数值/条目 | 含义 | 出处 |
|---|---|---|
| "Computational design of an enzyme catalyst for a stereoselective bimolecular Diels-Alderase reaction" | 底稿锚点段的题名写法（带 -erase） | `sources/baker.md:594` |
| "Houk KN, Michael FE, Baker D," | 该文以 [B17] 参考文献身份出现时的题名写法（不带 -erase）；两种拼写的差异照实登记 | `sources/baker.md:594` |
| "De novo enzyme design starts from a configuration of catalytic groups around the reaction" | theozyme 惯例的定义句（**[B20] 原文引句经底稿转录**，用于登记 K50 所锚定的惯例，非 Siegel 2010 原文） | `sources/baker.md:273`、`:662` |
| 十几个原子 | QM 作用范围（反应中心） | `sources/cost-benchmarks.md:161`（口径对照底稿，本卡未从其取引句）；CSV 行成本栏同义 |
| 2010；DOI 10.1126/science.1190239 ✅ | 年份与 DOI 核验状态 | CSV 行；`sources/baker.md:594` |
| 未记录 | 建库规模、命中率、活性/选择性最好值 | CSV K50 行各栏原值 |

## 5. 作者说了什么（本卡层：只有底稿转录）

1. 就 Siegel 2010 本身：底稿**未转录其任何正文原句**——本卡不冒领作者声明。
2. 底稿可核的只是 Baker 侧笔记的归属判断：该文的 QM 角色＝给出过渡态几何与催化基团排布，属化学步建模、不是全局筛选器（`:594`）；并作为 [B17] 的参考文献出现在 Baker 侧正文引注中。
3. 作者自述局限：未获正文，无法核验；活性数字与后续优化路线本卡全部不写。

## 6. 我们读出了什么（以下为推断，非作者原文）

1. **它是「QM 站几何位、不站排序位」这条项目纪律的溯源锚**：Baker 酶线 [B17]/[B18]/[B20] 的 DFT/theozyme 用法（`:662` 逐条引注）都能经 `:594` 的引注关系追到这条 2010 谱系——本项目把 QM 限定为「定过渡态几何与催化基团排布」不是自定规矩，是继承正规形态。
2. **成本分工是这篇文章给我们的最可用结论**：QM 预算花在十几个原子的反应中心，换来生成模型的硬约束输入；把同样的钱花在候选排序上则整条漏斗跑不动（与 `:664` 的「没有一例把 QM 用于成千上万候选的排序——原因与 MD 相同：单分子成本」互证）。
3. **不要向本文要数字**：降级+锚点双重身份决定它只回答「位置」问题。把握度：对「QM 角色定位」高（两处底稿一致）；对「2010 实验成绩」零。

## 7. 局限

- 摘要级/未获正文：方法参数、递减、命中、最好值全部未记录。
- 底稿题名两写法不一致（Diels-Alderase / Diels-Alder）——转录层级差异，未对 2010 原文核实前不判谁对谁错。
- 抓取通道对 PMC3241958 持续 500，非权威阴性；换正确 PMCID/出版社通道后应重取补登。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**：
1. **「QM 定几何 → 生成/设计器消化」的两段式**：我们的机制层候选同样应把 xTB/DFT 预算限定在反应中心簇的过渡态几何（产出是距离/角度约束），再让结构模型按约束搭架——这条分工形态可直接引用本锚点做文献根据。
2. **成本口径的引用方式**：「QM 只作用十几个原子」是**角色声明**不是报价；我们引用时同样只引角色，不引任何美元/机时数（那些在 K 系列价目卡）。

**不可迁移（为什么不能照搬）**：
1. Siegel 2010 的活性/选择性数字本卡不存在——**不得**被引为任何酶设计成功概率、Kcat/KM 先验或校准值。
2. DA 反应的 theozyme 几何不能平移到酶设计活化化学（反应坐标、底物几何完全不同）；迁移的只有「流程位置」，没有参数。
3. 禁止把本文写成「QM 能提高筛选命中率」的支持证据——底稿明记 QM 不做排序（`:594`、`:664`），引用反了就是错引。

## 9. 溯源与自检

引句底稿: sources/baker.md

- **本卡是降级卡**：K50 未获正文（`fetch_log.tsv:100`、`:148`、`:186` 记 PMC3241958 抓取 HTTP 500；NCBI/预印本通道无路）。从未成功下载全文，**不存在挂错行/隔离事件**。本行虽有双登记底稿，本卡**只声明 `sources/baker.md` 一份**作引句来源；`sources/cost-benchmarks.md` 的口径句仅入台账并标注对照。降级卡引句规则（≥2 条、逐字命中声明底稿）；本卡共 3 条逐字引句，全部命中 `sources/baker.md`（第 594 行两条、第 273 行一条；第 3 条已显式标注为 [B20] 原文经底稿转录，不是 Siegel 2010 正文）。
- **登记底稿核对**：`sources_map.json` K50 项登记 `sources/baker.md` + `sources/cost-benchmarks.md`（均实存）。对照行号：`sources/baker.md:594`（经典锚点段）、`:273`/`:662`（theozyme 惯例）、`:664`（QM 成本论断）；`sources/cost-benchmarks.md:161`（对照）。CSV 行：`data/protein_design_literature.csv:132`（证据级别=摘要级）。
- **门禁自检**：命令 `cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K50" --no-report`。本卡未改 CSV、`sources/*.md`、样板卡、`scripts/`，未做网络抓取。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 2 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（降级卡：摘要级，未获正文；经典锚点/口径对照条目）
target=Diels-Alderase（立体选择性双分子 Diels-Alder 反应）的设计催化剂
backbone_generation=未记录（CSV 行原值；本次未取正文）
computational_filters=QM theozyme 几何 → Rosetta 建库/设计
thresholds=未记录（原文未给阈值；本次未取正文）
md_used=否（CSV 行原值）
qm_used=是-化学步（QM 给出过渡态几何与催化基团排布，不做候选排序；sources/baker.md:594）
experimental_methods=酶活测定 + 立体选择性（CSV 行原值；方法与参数细节未记录）
pipeline_counts=未记录（未获正文）
hit_rate=未记录（不得引用为成功率或先验）
best_metric=未记录
cost_or_stat_note=QM（Houk 组过渡态几何/能量）只作用于十几个原子的反应中心（口径对照 sources/cost-benchmarks.md:161，本卡未从其取引句）；这是角色声明不是报价
role_in_timeline=QM 进入设计漏斗的正规形态：定过渡态几何与催化基团排布，不做候选排序；是 Baker 侧 [B17] 引注的 theozyme 溯源锚点
source_pointer=sources/baker.md:594（经典锚点段）、:273/:662（theozyme 惯例转引）、:664（QM 成本论断）；sources/cost-benchmarks.md:161（仅对照）；DOI 10.1126/science.1190239 ✅Crossref
CSV回填-->
