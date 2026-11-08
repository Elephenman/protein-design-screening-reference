# [Z09] FEPaML：ML 粗筛 + alchemical FEP 精排的分层筛选器说明书——降级精读卡

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **Z09**（组：周如鸿组） |
| 卡片状态 | **DEGRADED（降级卡）**：本卡唯一取证底稿为 `sources/zhou.md` 的 [Z09] 段落（第 121–127 行）；底稿第 124 行原记“全文在 PMC 未核验，摘要级” |
| 文献 | Brief Bioinform, 2025 · DOI 10.1093/bib/bbaf254（Crossref 核验 ✅）· PMID 40635188 |
| 另注（如实记录） | 清单（inventory）为本号另登记了一份 Europe PMC 缓存 `data/interim/claim_lit/PMC12240735.xml`（标题与本文一致）；门禁只拿非 XML 底稿逐字比对引句，本卡未读取、未核验该缓存内容，引句一律以 `sources/zhou.md` 为准 |
| 证据级别 | 摘要级（照 CSV 行 20 列；作者自述细节未经正文核验） |
| 本卡性质 | 分层筛选器的“说明书”条目：只记底稿确实写下的两阶段逻辑，量级词（万级/百级）保留底稿原文口径，具体阈值一律写“原文未给阈值（本次未取正文）” |

## 1. 这篇解决什么（一句话）

在新抗原疫苗的 mimotope（模拟表位）筛选里，把“海量分类交给 ML、比亲代更强的定量排序交给 FEP”这一分层逻辑显式写成方法：ML 粗筛万级 → FEP（alchemical）精排 top 百级（底稿口径）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（据底稿记录；作者自述部分未获正文，无法核验）

1. **ML 分类器回答不了“比亲代更强”**。底稿转引原文："ML models facilitate high-throughput screening"（后接省略）"but struggle to distinguish mimotopes from original neoantigens"——高通量分类与“相对亲代增强”判别是两回事。 → **作者做了什么**：在 ML 之后加一级 alchemical 自由能计算，用定量结合自由能差做精排（底稿将其概括为“ML 粗筛万级 → FEP 精排 top 百级”的两阶段漏斗）。 **代价**：两级衔接点（ML 送多少条进 FEP、按什么分数截断）摘要层不可见，原文未给阈值（本次未取正文）。
2. **FEP 定量但算不起全量**。底稿转引原文："in contrast, alchemical methods such as FEP provide quantitative binding free-energy differences"（后接省略）"but are computationally intensive"。 → **作者做了什么**：不让 FEP 直面海量候选，只把它用在 ML 粗筛后的 top 百级——用分层消化成本。 **代价**：精排窗口时长、λ 方案、ΔΔG 判据数值底稿均未记，无法复现。
3. **本文未解决（据底稿记录）**：第 127 行记“计算评估为主，无合成端数字（摘要级）”——ML→FEP 漏斗排出来的 mimotope 是否真的结合/免疫原性更强，底稿没有任何实验闭环记录；两级判据不一致时怎么仲裁亦未记。
4. **无 OA 正文的取证困难与处置（我们侧）**：底稿当时未核验 PMC 全文，本卡沿用摘要级口径。处置：引句全部逐字取 `sources/zhou.md` [Z09] 段；“万级/百级”只作为底稿记的量级表述引用，不写成实数；不借用同组 Z01/Z03/Z04 的 FEP 窗口与阈值来“补全”本文流程。

## 3. 方法与工作流程（只写底稿记下的部分）

**工具箱（底稿记录）**：ML 结合/不结合分类模型（海量侧）；alchemical FEP（定量 ΔΔG 精排侧）。QM：否（底稿记录）。MD 在 CSV 记为“是-主筛选器”（FEP 属同类自由能体系）；底稿未记 MD 体系细节。FEPaML 是底稿给的条目别名。

**工作流（输入 → 操作 → 判据/阈值 → 输出规模）**：

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 | neoantigen 与其 mimotope 候选空间 | ML 模型做海量“结合/不结合”分类 | 底稿未记分类模型与截断分数（本次未取正文） | 粗筛通过集（底稿量级表述：万级） |
| 2 | ML 粗筛 top 集 | alchemical FEP 定量结合自由能差，对“相对亲代 neoantigen 是否增强”精排 | 方向判据=定量 ΔΔG；原文未给阈值（本次未取正文） | 精排集（底稿量级表述：top 百级） |
| 3 | 精排结果 | 输出 mimotope 排序供疫苗设计选用 | 底稿未记最终选取规则 | 计算评估为主；无合成端数字（摘要级） |

## 4. 关键数字台账（全部出自底稿 `sources/zhou.md`，摘要级）

| 数值 | 含义 | 出处 |
|---|---|---|
| 万级 | ML 粗筛面对的量级（底稿概括，非实数） | [Z09] 定位行 |
| top 百级 | 进入 FEP 精排的规模（底稿概括，非实数） | [Z09] 定位行 |
| 2 级 | 漏斗层级（ML 粗筛 + FEP 精排） | [Z09] 定位行 |
| ΔΔG 阈值 / FEP 窗口 / 模型参数 | 未记录——原文未给阈值（本次未取正文） | [Z09] 全段 |
| 实验数 | 未记录（计算评估为主，无合成端数字） | [Z09] 命中率行 |

## 5. 作者说了什么（据底稿，只转述摘要层面明确的话）

作者的自述框架（底稿原文转引，两句之间原文以省略号衔接，故拆条引用）："ML models facilitate high-throughput screening"；"but struggle to distinguish mimotopes from original neoantigens"；"in contrast, alchemical methods such as FEP provide quantitative binding free-energy differences"；"but are computationally intensive"。除这一角色分工陈述外，底稿未记录作者给出任何实数阈值、命中率或实验结果。

## 6. 我们读出了什么（以下为推断，非作者原文）

- 我们把这篇读作该组标准漏斗逻辑第一次被**显式成文**为“分工说明书”：ML 管召回、自由能管定量序。底稿演进链行也是这个口径（“组内标准漏斗的显式表述”）。对我们的启示是把粗筛/精排的**职责边界**写进判据文档，而不是给每级凑阈值数字——这是形态层面的可借鉴点。
- “比亲代更强”是一类我们同样会遇到的问题（在失活/弱活背景上找回活性），其共同陷阱是让分类器回答回归问题；此为一般方法学推断，不由本文实验证明（本文无实验）。

## 7. 局限

- 摘要级：两级漏斗的截断分数、FEP 参数、送测规模全不可见，“万级/百级”只是底稿概括词。
- 无实验闭环记录：排序质量未由任何合成/结合数据确认。
- 分类问题（mimotope vs neoantigen）与我们的催化问题跨域，判据内容不可搬。

## 8. 迁移到我们的筛选／判定工作流

**可迁移（怎么用）**
1. 分层职责表述：便宜模型只做召回，定量层级只做小规模精排——直接对应我们“序列/结构粗筛 → MD/机制精排”的预算分配写法。
2. “分类器分不清比亲代更强”这条教训可用于 our funnel 的判据评审：任何用召回模型回答序问题的环节都要标记为不合格据。

**不可迁移（为什么不能照搬）**
1. FEP 的 ΔΔG 是**结合自由能差**，不是过渡态能垒或产物生成量，禁止当酶活判据（本库口径）。
2. “万级→百级”不得引用为命中率或压缩比实数（底稿概括词，非测量）。
3. 本文无湿实验，不能作为“ML+FEP 漏斗能出真阳性”的证据来源。

## 9. 溯源与自检

引句底稿: sources/zhou.md

- 唯一取证底稿：`sources/zhou.md` [Z09] 段落（第 121–127 行）；链接 https://doi.org/10.1093/bib/bbaf254 ；底稿自记“全文在 PMC 未核验，摘要级”。
- 标题与署名（"A free energy perturbation-assisted machine learning strategy"、"for mimotope screening in neoantigen-based vaccine design"、"Qinglu Zhong, Kevin C. Chan, Lei Fu"、"Brief Bioinform, 2025"）逐字取自该段（标题为避跨省略号拆作两条）。
- Europe PMC 缓存 `data/interim/claim_lit/PMC12240735.xml` 虽登记于清单，但门禁比对不用 XML，本卡亦未据其声称任何正文细节。
- 全卡引句避开含 `**` 片段；门禁：`scripts/verify_literature_cards.py --only Z09 --no-report`。

<!--CSV回填
work_type=方法
target=neoantigen 疫苗中 mimotope（模拟表位）筛选的分层筛选器设计
backbone_generation=ML 模型做海量结合/不结合分类（候选来自 mimotope 空间；底稿未记生成细节）
computational_filters=两阶段漏斗：ML 粗筛（底稿量级：万级）→ FEP（alchemical）精排定量 ΔΔG（底稿量级：top 百级）
thresholds=未记录（原文未给阈值，本次未取正文；截断分数与 ΔΔG 判据底稿均未记）
md_used=是-主筛选器（alchemical FEP 精排属自由能体系；MD 细节底稿未记）
qm_used=否
experimental_methods=无合成端实验记录（计算评估为主，摘要级）
pipeline_counts=未记录（底稿仅有“万级→top 百级”量级概括，非实数）
hit_rate=未记录（无实验数据；底稿原记“未获正文”）
best_metric=未记录（摘要级无 Kd/ΔΔG 数值）
cost_or_stat_note=FEP 定量但 computationally intensive 为作者自述口径；分层设计即成本对策；正文未核验（摘要级）
role_in_timeline=筛选器的分层设计说明书：ML 高通量但分不清比亲代更强的 mimotope，alchemical FEP 定量但算力贵——组内标准漏斗逻辑的显式表述
source_pointer=sources/zhou.md [Z09] 段落（第 121–127 行）；https://doi.org/10.1093/bib/bbaf254；PMID 40635188
CSV回填-->
