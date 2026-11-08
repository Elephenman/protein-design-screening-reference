# [B16] MP3-seq：把"谁跟谁结合、结合多强"变成测序读数——一次实验 ~10⁵ 对，用来给设计库判活并反过来考结构预测

Baryshev A, La Fleur A †, Groves B, Michel C, Baker D, Ljubetič A, Seelig G（华盛顿大学 EE/Allen School/Biochem/IPD + 斯洛文尼亚国家化学所）
Nature Chemical Biology 2024, 20:1514–1523 · DOI 10.1038/s41589-024-01718-x · PMID 39192093 · PMCID PMC11511666
CC BY-NC-ND 4.0 · 全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC11511666/ （前身 bioRxiv 2023.08.16 预印本）
† 共同第一作者

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B16**（组：Baker组; 通用方法学; 口径对照） |
| batches 状态 | **FULLTEXT**（`data/literature_cards/batches.tsv` 第 5 批） |
| 本地全文（本卡引句底稿） | `data/interim/baker_lit/ft/mp3seq2024.txt`（62,973 B，2026-10-16 抓取，Europe PMC fullTextXML 去标签纯文本）；登记表 `sources_map.json["B16"]` 只有这一份 + `sources/baker.md` |
| 对照底稿 | `sources/baker.md:211–222`（原卡）与 `sources/baker.md:610`（5a 高通量湿筛行）、`sources/baker.md:623`（条形码并行 PPI 行）；本卡在其基础上补：Autotune 的适用范围与死角、两种融合序/pseudoreplicate 口径、DESeq2 与最低读数过滤的取舍、弱相互作用的判读、DUET 图算法与保守削减、AF-M/iCipa/回归模型的三种训练-测试拆分 |
| 证据级别 | **全文级**（本卡所有英文引句可在本地全文逐字命中；见第 9 节） |
| 未取到的部分 | Supplementary Methods（Autotune 公式、DUET 打分函数细节、建模超参、片段/载体清单）、Supplementary Figs 1–14 与 Tables 2–5 的逐条数值。凡涉及这些的地方本卡明写"正文未给阈值/数值" |
| 与 CSV 既有字段的差异 | CSV `阈值数字=P_adj ≤ 0.05`：正文里 **0.05 只出现在图 2 网络图的展示口径**，而"设计成功"的判定用的是 **P_adj ≤ 0.01 且 P-LFC ≥ 4**（结果段原句见第 3 节 S6）；CSV 需补这条。其余字段与正文一致 |

## 1. 这篇到底解决什么（一句话+大白话）

**这不是设计论文，是"测量"论文。** Baker 组与 Seelig 组要解决的问题是：设计完一大批异二聚体（coiled-coil 1×1、四螺旋束 2×2、三螺旋 1×2）之后，**没人能快速知道每一对到底结不结、有多强、有没有偷偷跟别人结**。已有的办法要么要纯化蛋白（质谱/蛋白芯片），要么只能"少数几个 vs 一大库"（酵母/噬菌体展示），要么要建 E. coli 库 + 酵母交配。这篇把酵母双杂交（Y2H）改造成：所有需要的元件（两个蛋白 + 两个条形码 + DBD/AD + 选择标记）在**一个质粒**上、在**酵母里直接同源重组装配**，靠 His 营养缺陷选择把"结合"变成"长得快"，再测条形码对的读数变化算富集。于是**一次实验能测 >10⁵ 对相互作用**，还能把结果当标签去训模型。作者同时诚实给出结论：结构预测模型（AF-M）可以当预筛，但**定量排序仍然必须做实验**。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **Y2H 规模化卡在建库流程上**（要 E. coli 建库、要酵母交配、要把两个库分别转进 MATα/MATa）。 **应对**：把两两组合编码到单个质粒上，用同源重组在酵母内一次装好——原文："A plasmid library is constructed directly through homologous recombination in yeast to measure all"，并明确收益："Our workflow bypasses the need for plasmid cloning in E ."。同时用 CEN 序列保证拷贝数≈1，把"细胞长得好"与"条形码读数"锁成一件事："the CEN sequence ensures each yeast cell (and any subsequent daughter cells) will contain"。
2. **自激活（autoactivation）——Y2H 的经典假阳性**：某个蛋白不管跟谁都让酵母长。作者给的定义："autoactivation is an error mode in Y2H experiments where high enrichment is observed for a protein"。 **应对**：先做非选择培养（His preselection）当基线（并核实"His preselection barcode counts remained steady over time"），再在分析里检测自激活体、用**反方向融合序**的数值补回去（Autotune）："Next, we detect autoactivators and replace their His postselection values with values calculated"。 **留下的代价（作者明写）**："If an autoactivator is found,"；未来方向是改选择方案从实验上消灭自激活体（"The MP3-seq workflow could be further generalized"），本文没做。
3. **融合方向本身会改变蛋白的表达/折叠**，同一对蛋白可能因为谁接 AD 谁接 DBD 而测出不同结果。 **应对**：所有蛋白两种序都测——"The expression or folding of some proteins may be"；需要把两序合成一个可比较的数时，把两序当**两个 pseudoreplicate**丢进 DESeq2 得 P-LFC："We treat each fusion order as an independent set"。
4. **同源二聚体（A:A）在装配端天生吃亏**：**"Homodimer plasmid assembly was less efficient in"**，作者判断原因："This phenomenon is likely because of increased"。 **应对**：不重做实验，先确认覆盖度够就纳入分析（"but coverage was sufficient for inclusion in the"）；并系统性试了不同的**最低读数过滤阈值**："We explored using minimum read count filtering at"（NICP 系列上过滤确实改善了相关，尤其 Spearman rho）。→ 结论是过滤对定量结论影响小，但**缺读数仍会永久缺数据**，这一点他们在 DUET 一节还要专门做置换检验去排查。
5. **重复之间的测序深度/选择时长不一样，直接平均富集值会串味**。 **应对**：改用 DESeq2 的差分富集框架——"DESeq2 calculates differential enrichment across"，用 LFC + P_adj 当判据，而不是平均 enrichment。
6. **弱相互作用反而被"统计化"处理后变差**（DESeq2 是为大效应设计的）。 **应对**：单独拿最弱的 5 对比较两种口径，发现原始富集更好排序："Enrichments had a slightly better ability to order weak interactions than P-LFCs, suggesting that a non-DeSeq2 analysis may be better suited for the high-throughput study of weak PPIs"。→ 这是一处**主动承认"我的主判据在弱信号上不占优"**的写法。
7. **第一版条形码位置可能干扰 mRNA 稳定性**（放在 3′UTR、终止子上游），等于探针本身影响被测物。 **应对**：换第二版（条形码移到终止子下游），并用重复间相关性检验两版数据是否可比："the inter-replicate correlations suggested"；同时限定可比范围（Bcl-2 那一轮第一重复用的是 v1）。
8. **正交性拿不到：全对全里绝大多数强信号是"预期外"的配对**。在包含 DHD0–DHD2 + mALb 的最大一轮里："only 33 of 914 total PPIs with P adj ≤ 0.01 and P-LFC ≥ 4 were on target"。 **应对**：不去改设计，而是**把问题改成图论问题**——用显著正 P-LFC 建加权无向图，"This approach allowed us to rephrase the problem as finding a graph of degree one vertices without self-edges, which maximizes the sum of the remaining edges"，再用自写的贪心删边算法 DUET（每轮删一个顶点及其边）抽潜在正交子集："This scoring function was used in a greedy graph reduction method, Deleting Undirected Edges Thoughtfully (DUET)"。其中"正交间隙"沿用文献定义："The orthogonality gap is defined as the"。
9. **DUET 的结果只有在"把不显著的相互作用都当成不存在"时才叫正交**——这个前提可能不成立。 **应对**：再加一层保守削减（把 DUET 对的 P-LFC 低于该蛋白最高非 DUET 配对 P-LFC 的先删，再逐个删掉非 DUET 信号最大的对），削减到一半规模后仍保住与 NICP/Bcl-2 可比的正交间隙（"we removed interactions with protomers for which the DUET pair P-LFC was lower than the highest non-DUET pair P-LFC"）。
10. **怀疑 DUET 偏心"缺数据"的蛋白**（缺数据 = 图上边少 = 更容易被留下）。 **应对**：做置换检验，比较 DUET 结果与随机同规模蛋白集的缺失相互作用数，结论："We did not find that DUET results had a significantly higher number of missing interactions"。→ 这是本文里最干净的一次"对自己的算法做一次反自证"。
11. **AF-M 的单一误差指标不够用**：最好的单项也只是界面 iPTM——"The best-performing metric was the interface"，而专用序列模型更强："we found that a sequence-based predictor (iCipa)"；对 2×2 体系，AF-M 也只抓住部分规律："Heterodimeric interactions had"。 **应对**：把 AF 误差项 + Rosetta 物理项拼起来训 ridge 回归/分类："Rosetta was used to collect"，并用层次聚类先去共线性（"Agglomerative hierarchical"）。结果在填补缺失相互作用的任务上追平 iCipa（见 2.12 的代价）。
12. **但换蛋白族就崩**——这是本文最重要的负结果。作者用两种拆分（留出一批**相互作用** vs 留出一整批**蛋白**）分别考核：留出蛋白的任务上"回归模型全部大幅掉分"——"All regression models dropped"；跨族迁移更糟："the models performed worse than"；连 AF-M 自己也只抓住部分规律："Heterodimeric interactions had"。 **应对（=结论而非补救）**：明确把方法定位让给实验——"high-throughput experimental"；同时把卖点改成**便宜**："the LFC predictor can be"（对比 iCipa 用了 8,000+ 对手工调过的能量项）。

## 3. 方法与工作流程（可复现顺序）

### 用了哪些方法（工具箱与用途）

- **湿实验核心**：重编程的酵母双杂交（Zif268 Cys(2)His(2) 锌指作 DBD + 其启动子驱动生长必需酶 His3；VP16 作 AD）+ **条形码对**（每个蛋白一个条形码，蛋白与条形码在同一片段上、中间夹终止子 Tsynth23/Tsynth27）+ 条形码扩增子的高通量测序读数（分析端从 bcl2fastq 起，原始数据存 GEO GSE271790）。选择压力可用 **3-AT**（His3 竞争性抑制剂）浓度梯度调节严格度。
- **分析链**：bcl2fastq → cutadapt 切条形码区 → Starcode 聚类计数条形码对 → 富集 E（含每条件最小检出值当伪计数）→ Autotune 去自激活 → DESeq2 出 LFC / P-LFC 与 Hochberg 校正 P_adj。
- **下游算法**：DUET（贪心删边取 1-正则子图）+ 保守二次削减 + 置换检验。
- **计算对照侧**：AF2 与三版 AF-Multimer 预测复合体，取 iPTM/PAE/pLDDT 类误差项；Rosetta 取物理能量项；ridge 回归（LFC 预测器）与 logistic ridge（结合/不结合分类）；iCipa 作族专用基线。
- **没有用的方法**：MD、QM/电子结构、自由能微扰；本文也不测 Kd（Kd 全部来自他人的 BLI/luciferase/stopped-flow 数据，只用来做相关性核对）。

### A. 建库—选择—读出—判据（每一步：输入 → 操作 → 判据/阈值 → 输出规模）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | Twist 订购的基因片段（linker + 蛋白 CDS + 终止子 + PCR handle + 条形码 + insulation）+ 含 CEN/TRP1/DBD/AD 的载体骨架 | 电转进 Y777（MATa）单菌一步完成全部两两组合的质粒装配 | 正文未给转化/覆盖度阈值（细节在 Supplementary Methods） | 一个池子里同时装出全部配对；1×1 验证轮为"24 片段池、12 个蛋白各配 AD 或 DBD"，共 **144** 对 |
| S2 | 装配后的酵母 | Trp− 媒体延长培养（维持质粒）→ 取一份冻存 = **His preselection** | "the CEN sequence ensures each"（拷贝数≈1 是读数可解释的前提） | 预选择群体 |
| S3 | 预选择群体 | His− 媒体选择生长（可加不同浓度 3-AT 调严格度）= **His postselection** | 3-AT 为 His3 竞争性抑制剂；正文未给具体浓度数值（在补充图 2b–d） | 后选择群体 |
| S4 | 两份群体的质粒 | 提取 → 扩增条形码区 → 测序 → bcl2fastq / cutadapt / Starcode 计数条形码对 | 富集 E = 库规模归一读数比 + 每条件最小检出值伪计数；最低读数阈值另做敏感性测试 | 原始条形码对计数表 |
| S5 | 计数表 | 检测自激活体 → Autotune 用反融合序数值回填 → 多重复用 DESeq2 合并出 LFC；两融合序合并出 P-LFC | Hochberg 校正的 Wald 检验 **P_adj**；正文图示网络用 P_adj ≤ 0.05（图 2d,e） | LFC / P-LFC / P_adj 矩阵 |
| S6 | 显著性矩阵 | 判定"设计成功" | 结果段口径：**P_adj ≤ 0.01 且 P-LFC ≥ 4**（"we defined a 'success' as any PPI with P adj ≤ 0.01 and P-LFC ≥ 4"） | 每个设计集的成功数与成功率 |
| S7 | 显著正 P-LFC 边集 | 建加权无向图 → DUET 贪心删边到 1-正则图 → 按正交间隙做保守削减 → 置换检验查缺数据偏置 | 打分函数奖励正交边/超过目标正交间隙的边、惩罚非正交边（α = 0.01）；削减规则见 2.9 | 全 DHD 集：1,562 条边/270 顶点 → **36** 个 DUET 对；其中 on-target 仅 4 对 |

### B. 用 MP3-seq 回答的三个实质问题

| # | 问题 | 操作 | 关键数字（正文） | 结论口径 |
|---|---|---|---|---|
| Q1 定量性 | 与既有 Kd/激活值对不对得上 | 与 NICP 的 HEK293T luciferase 数据、AN/BN 截短体的 BLI Kd、Bcl-2 家族 BLI、PUMA-Mcl-1 stopped-flow 分别做相关 | r² = 0.74（n = 141 PPIs）；r² = 0.94（跨越约三个数量级的 Kd）；Bcl-2 r² = 0.61（n = 43）；PUMA r² = 0.66（n = 13） | "highly quantitative"（摘要口径），非绝对定量 |
| Q2 规模 | 一次能测多少对 | 全 DHD 集 + Bcl-2 家族同池的全对全 | **337 × 337 = 113,569** 相互作用（两轮重复）；DHD1 初始 100 条设计 + 第二轮 52 条 + 35 对衍生体 + 9 条既往 2×2 对照 | "MP3-seq can measure over 100,000 PPIs in a single experiment" |
| Q3 设计集成活率 | 设计库到底多少能用 | 按 S6 判据数成功率 | "Every design set had an approximately 20% success rate in the largest screen," | 20% 与文献 22% 一致 → 本文的测量口径与既往实验口径可互认 |
| Q4 设计规律 | 长度与 HB-net 数怎么决定正交 | 拿母体 mALb8 做截短体（T1/T2）与 HB-net 替换（R1/R2/R12 × 大/小疏水）系列全测 | 截两turn直接不结；可推出 2×2 最短可用长度 = **3.5 heptads**；需要 **≥2 个 HB-net 错配**才挡住结合；单纯换疏水残基大小不足以给正交性 | 用一次高通量数据把"最小设计要件"量化出来（"we found that at least two"） |
| Q5 计算能不能替实验 | AF2/AF-M + 物理项训 LFC 预测器 | 三种拆分：留出相互作用、留出蛋白、跨族迁移；对照 iPTM 与 iCipa | 测试集 n = 14（1×1）/n = 19（mALb8）；iCipa 训练用 >8,000 对；本方法数据量约**百分之一** | 预筛可用，定量排序不可用（"high-throughput experimental"） |

**这套流程的骨架值得单独记住**：先造一个**能同时给阳性和阴性打分的廉价读数**（一次 10⁵ 对，成本≈一次建库 + 一次测序），再用它去 (a) 数设计集成功率、(b) 抽可用子集、(c) 反过来给结构预测模型定分。这正是我们项目缺的那一层——**B09 的"筛子考卷"是别人历史数据的整理，本文是主动制造考卷的仪器**。

## 4. 关键数字台账（均可在 `mp3seq2024.txt` 逐字搜到）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| >100,000 对 / 单次实验 | 通量上限（本文卖点） | "MP3-seq can measure over 100,000 PPIs in a single experiment" |
| 337 × 337 = 113,569 | 最大一轮全对全规模（2 重复） | "resulting in a matrix of 337 ×"（数值在该句中） |
| 144 对 / 6 个正交 1×1 / 5 重复 | 第一支验证集 | "we screened 144 pairwise" |
| r² = 0.74（n=141） | 与 HEK293T luciferase 激活值相关 | "we correlated MP3-seq LFCs with" |
| r² = 0.94，跨 ~3 个数量级 Kd | 与截短体系列 Kd 定量一致 | "The MP3-seq P-LFCs correlated" |
| 28 个蛋白 | 第二支 1×1 全对全（NICP + N/P 变体） | "In a separate all-by-all" |
| 6 个 Bcl-2 同源体 × 9 条设计抑制剂；2 重复 | 球蛋白验证 | "six homologous proteins from the Bcl-2 family"、"nine de novo designed inhibitors of said homologs" |
| r² = 0.61（BLI，n=43）；11 条 BLI 未检出 vs 43 条检出，单侧 t 检验 t = 4.51, P = 1.858×10⁻⁵ | MP3-seq 能区分"BLI 检不出"的弱对 | "found that the mean MP3-seq" |
| Alpha-seq 对照：batched r² = 0.45 / paired r² = 0.61；batched 的 t = 1.36, P = 0.0904 不显著 | 与另一条高通量路线交叉验证 | "Pairwise Alpha-seq also had a" |
| r² = 0.66（n=13） | PUMA 无序肽-Mcl-1 与 stopped-flow Kd | "We found a good correlation" |
| 100 + 52 + 35 对 + 9 对照 | DHD 设计集构成（DHD1/DHD2/DHD0/mALb） | "Initially, we chose 100 designs" |
| ≈20%（既往 α 螺旋束 22%） | 最大筛里每个设计集的成功率 | "Every design set had an approximately 20% success rate in the largest screen" |
| **P_adj ≤ 0.01 且 P-LFC ≥ 4** | 本文"成功"的定义 | 结果段定义句（S6） |
| 33 / 914 | 强信号里 on-target 的份额（正交性灾难） | "only 33 of 914 total PPIs with" |
| 2,001 边/202 顶点 → 18 对；279/85 → 11；1,562/270 → 36；on-target 2/2/4 | DUET 削减结果 | "we went from 2,001 edges" |
| 3.5 heptads；≥2 个 HB-net 错配 | 从数据反推的 2×2 设计最小要件 | "We showed that the minimum" |
| AF-M v2/v3 > AF2 与 v1；iCipa > 任何单一 AF 指标；测试集 n=14 / n=19；iCipa 训练 >8,000 对；数据量百分之一 | 计算侧的排序与代价 | "While iCipa was trained on over" |
| 5 种融合序/重复设计、3–5 个重复 | 每轮的重复数（正文散述） | "All MP3-seq values were calculated from five biological replicates"（图 2b 图注；该句后半说明其余轮次以图中标注给出重复数） |
| **本文未记录** | 单实验测序成本金额、GPU/机时（建模部分未给算力） | 正文无 |

## 5. 结论——作者说了什么

1. MP3-seq 易用、可扩展、高度定量："We show that MP3-seq is highly quantitative and scales to over 100,000 interactions"（摘要），并在四组既有体系上拿到定量一致（Q1）。
2. 它能一次性覆盖设计库的全对全相互作用矩阵，从而**事后**抽正交子集，也能反推设计最小要件（3.5 heptads、≥2 HB-net 错配）。
3. 计算侧：AF-M 类指标可以做**预筛**（iPTM 最好的单一指标；组合 AF + Rosetta 项的回归能追平 iCipa，且只需约百分之一的数据量），但 **"experimentally measuring"**（摘要原句）。
4. 关于设计集本身：约 20% 成功率与既往 α-螺旋束 22% 一致，作者把它当作"测量口径与历史口径互认"的证据，而不是设计突破。
5. 作者自列待办：从实验端消灭自激活体、接 Stable-seq/蛋白酶试验以确认"测到阴性不是表达或折叠问题"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文的价值对我们不在"又一个筛选判据"，而在"标签生成器"**：一次实验就把 N×N 变成带 P_adj 的二值/连续标签。→ 我们的酶设计项目没有这一层，所以任何判据都只能机制论证（对照 B09 的 A 段需要百万级历史标签）；MP3-seq 式的**廉价批量结局标签**是我们可以争取的最短路径（哪怕规模只有 4 个构建体 × 突变体 × 底物条件的矩阵，也足够把"判据考卷"从 0 变成有）。
2. **他们把"测量的自身误差"当成一等公民处理**：Autotune、双融合序、最低读数敏感性、弱相互作用换口径、置换检验查算法偏置——每一条都是"先怀疑仪器，再解释生物学"。→ 对应我们：LC-MS/MS 产物定量应先做同类自检（同位素内标、空白基质、低浓度排序能力），**否则漏斗判据会把仪器误差当成化学信号**。
3. **"判据换成能区分弱信号的那一套"是他们做过的显式动作**（2.6 条），而我们的漏斗目前只有强/弱二值口径。→ 建议：在低 SNR 区（痕量产物）改用未校正的原始峰面积排序，把 DESeq2 式的显著性检验留给高 SNR 区。
4. **正交性的教训可直接搬**：全对全里强信号 914 条只有 33 条是设计意图（≈3.6%）。→ 我们做"特异装载酶设计 vs 装载天然氨基酸/竞争性副反应"时，**默认应为"预期外事件占多数"**，漏斗必须包含非预期通道检测，而不是只验证预期通道。
5. **负结果的写法值得学**：他们没有把 AF-M 组合模型吹成替代实验，而是给出"两种任务拆分，一种能一种不能"（2.12 条）。→ 我们报告 PLACER/MD/QM 判据时也应固定给"填补缺口"与"新蛋白零样本"两种拆分，只允许前者支持上线。
6. "约百分之一数据量就能自动造出追平族专用模型的预测器"这句话，如果成立，对我们是**最经济的一条路**：先用少量批量湿实验标签训便宜线性模型，再决定是否上长时 MD。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：自激活使同源二聚体不可判（2.2 条）；弱相互作用下 P-LFC 不如原始富集（2.6 条）；v1 条形码位置可能影响 mRNA 稳定性（2.7 条）；DUET 的正交性建立在"不显著即不结合"这一未必成立的假设上（2.9 条）；留出蛋白任务上回归模型全线崩（2.12 条）；测的是细胞内表观结合，与纯化蛋白 Kd 的差别来自表达环境（正文以"MP3-seq interactions are measured with proteins expressed in yeast, while biolayer interferometry uses purified proteins"解释与文献的偏差）。
- 我们读出：① **"20% 成功率"是本文自己的判据（P_adj ≤ 0.01 且 P-LFC ≥ 4）下的数**，与既往 22% 的"一致"只是量级巧合，不能当独立验证；② 本文不产出任何亲和力绝对值（无 Kd 表），所有定量都是与他人数据的相关性；③ 全对全矩阵里的 113,569 是**理论配对数**，不是实测对数（存在缺失读数，正文用灰色 × 标注缺失），所以"一次测 10⁵ 对"应当读作上限而非产出；④ 补充方法（Autotune 公式、DUET 打分函数、建模超参）未取回，本文的判据无法严格复现；⑤ 全文无 MD/QM，不能为能量学主张提供依据。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **"条形码/可读标签 + 富集倍数 + 多重检验校正"这套统计口径**可整体搬到我们的产物分辨：只要某个读数（例如质谱峰面积比、或可测序的报告条形码）能把"发生了正确化学反应"变成可计数的量，就照本文格式报 **LFC + P_adj（并附最低读数敏感性测试）**，不要只报"有/无"。
2. **两种任务拆分必须同时报**（填补缺失 vs 留出全新对象）：任何"我们的打分函数能预测活性"的结论，只有留出蛋白/留出酶的拆分也算过才允许写进漏斗依据（本文正是靠这条把自己的模型限成"预筛"）。
3. **双方向/双对照测同一个对**：同一反应应在两个正交设置（如不同底物浓度、加/不加竞争天然氨基酸）各测一次，再合并——照本文"两种融合序"的处理，避免"读数差异来自标签位置而非被测物"。
4. **把"仪器假阳性"当独立难点处理**（Autotune 类比）：酶设计场景的等价物是"底物/产物自发荧光或背景峰"造成的假信号，必须在漏斗里显式设一道回填/剔除规则，并写清剔除不了的死角（本文承认同源二聚体救不回来）。
5. **用批量测量反推"最小设计要件"**（3.5 heptads / ≥2 HB-net 错配）：这是把高通量数据转成设计规则的范式；我们做分步化学事件事件归因时，目标也是从一批测量里给出"最少需要哪些催化元件"的规则，而不是逐个描述。

**不可迁移（为什么不能照搬）**

1. **Y2H 的读出是"两个蛋白在酵母核里是否形成转录因子"**，与氨基酸化反应没有任何映射。LFC/P_adj ≤ 0.01/20% 这些数字**不得**引用为底物装载效率或酶活性的判据或先验概率。
2. **本文的 10⁵ 通量建立在可复制质粒 + 可生长选择上**；我们的产物化学不能"选择生长"，一次反应不能自我扩增，通量天花板由 LC-MS/MS 或显色读数决定，**不能承诺"一次一万个反应"**，也不能据此估算成本曲线。
3. **iPTM/AF-M 在这里只被证明"可当预筛"**，且作者明写不能定量排序。因此不能把 AF-M 类指标当成催化判据引用，更不能引用来支持"结构预测可判酶活"。
4. 本文不产生 Kd 也不产生 kcat/KM，与 [B17] 的活性判据之间没有可比性；两篇的"成功率"口径互不可换。

## 9. 溯源与自检

- 引句底稿: data/interim/baker_lit/ft/mp3seq2024.txt —— 本卡全部英文引句以此为唯一逐字比对对象（该编号在 `sources_map.json` 里登记的其余底稿只有 `sources/baker.md`）。
- 对照底稿行号：`sources/baker.md:211–222`；跨论文对照表：`sources/baker.md:610`（5a 高通量湿筛行，SC₅₀/LFC/P_adj ≤ 0.05 口径）、`sources/baker.md:623`（条形码并行 PPI 测定行）、`sources/baker.md:644`（自洽性判据失效时改加便宜高通量湿实验的总判断）。
- CSV 字段映射：第 3 节 ↔ `计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率`；第 8 节 ↔ `在方法演进链的位置`；CSV 的 `阈值数字` 需按第 0 节差异说明补记 P_adj ≤ 0.01 + P-LFC ≥ 4。
- 本卡自检：`scripts/verify_literature_cards.py --only B16 --no-report`（参数 --no-report，避免覆盖他人产物）。写卡过程中就地修掉四处不逐字草稿：一处把原文 physics-based metrics 误写成 terms、一处把图注里 except for those labeled 之前漏掉的 for 连写、一处把原文小写开头的 found that the mean… 加了主语 we、一处把两处仅作说明用的省略号式英文片段去掉直双引号以免被门禁当逐字引句。均按门禁报错改正后复跑。
- 不可复现之处（已声明）：Autotune 公式、DUET 打分函数与建模超参都在 Supplementary Methods，本卡第 3 节的 S5/S7 相应格子只写"正文未给阈值"。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 44 条逐字引句来自许可受限的第三方来源（B01、B16；CC_BY_NC_ND、PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=方法
target=设计型异二聚体（NICP 1×1 系列、四螺旋束 2×2 与三螺旋 1×2、mALb8 及其截短/HB-net 变体）、Bcl-2 家族 6 个同源体 × 9 条设计抑制剂、PUMA 肽-Mcl-1，以及天然 PPI（本文卖点是测量而非设计）
backbone_generation=沿用既有设计体（Cao/Boyken/Chen 等），本文不生成新骨架；计算侧只做 AF2/AF-Multimer(v1-v3) 复合体预测 + Rosetta 物理项取数
computational_filters=条形码配对富集倍数 LFC 与 pseudoreplicate P-LFC + DESeq2 的 Hochberg 校正 Wald 检验 P_adj；自激活体检测与 Autotune 回填；最低读数过滤敏感性测试；下游 DUET 贪心删边抽正交子集；计算对照用 AF-M 误差项（iPTM 最佳）+ Rosetta 能量项训 ridge 回归/logistic 分类，基线 iCipa
thresholds=设计成功 P_adj ≤ 0.01 且 P-LFC ≥ 4；网络图展示口径 P_adj ≤ 0.05；DUET 建图显著性 α = 0.01；正交间隙定义为最弱 on-target 与最强 off-target 之差（正文未给数值阈值）
md_used=否
qm_used=否
experimental_methods=重编程酵母双杂交（Zif268-DBD + VP16-AD，His3 作生长必需报告基因，3-AT 调严格度）+ 条形码配对 + 一代/二代测序读数；与文献 BLI、luciferase、stopped-flow、Alpha-seq 数据做相关验证
pipeline_counts=单次全对全 337 × 337 = 113,569 对（理论上限，实测存在缺失读数）；1×1 验证轮 144 对（6 个正交 1×1，5 个重复）；28 蛋白全对全一轮；Bcl-2 6×9 两轮；DHD 集 100 + 52 + 35 对 + 9 对照；DUET 1,562 边/270 顶点 → 36 对（on-target 4）
hit_rate=每个设计集在最大筛里约 20% 成功（与既往 α-螺旋束 22% 一致）；最大全对全里强信号 914 对中仅 33 对为设计意图（约 3.6%）；跨族/留出蛋白任务上计算模型全线失效，作者结论是实验测量仍不可省
best_metric=未记录（本文只给富集倍数与相关性 r² = 0.74/0.94/0.61/0.66，不产出 Kd 或催化效率）
cost_or_stat_note=通量 >10⁵ 对/次实验（成本≈一次酵母装配 + 一次测序）；正文未给金额与测序成本、未给建模算力；"预测器可在约百分之一数据量上自动训练"是其主打性价比口径；本文未记录统计功效计算
role_in_timeline=把"每个设计的结合与特异性"从逐个 BLI/SPR 变成 ~10⁵ 对/实验的可测序标签：既是廉价筛选器，也是回头训练与校正打分函数的数据引擎；在自洽性判据（B09 型）失效的模态上，本文代表 Baker 组"用便宜的高通量湿实验替代昂贵验证"那条应对路线
source_pointer=data/interim/baker_lit/ft/mp3seq2024.txt；sources/baker.md:211-222、610、623、644
CSV回填-->
