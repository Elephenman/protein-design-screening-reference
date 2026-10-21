# [K33] 表观功能分数不等于功能本身：把「DMS 分数能替功能说到什么程度」量化成随读出类型变化的相关系数

Gerasimavicius Lukas, Livesey Benjamin J, Marsh Joseph A（MRC Human Genetics Unit, Institute of Genetics & Cancer, University of Edinburgh；通讯 Joseph A. Marsh）
Protein Science 2023, 32(7): e4688 · DOI 10.1002/pro.4688 · PMCID PMC10273344 · PMID 37243972（后两者来自底稿头部元数据行）
开放获取（CC BY 4.0）· https://doi.org/10.1002/pro.4688 · 数据仓库 https://www.doi.org/10.17605/OSF.IO/ZTV8A · Review Editor: Nir Ben-Tal

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K33**（组：通用方法学; 口径对照；文献类型 benchmark） |
| 本文取回方式 | inventory 登记 `fetch_channel=epmc_search_then_fulltext`（Europe PMC 检索后取 fullTextXML），本地抓取日期 2026-10-20 |
| 本地全文① | `data/literature_cards/fulltext/K33_PMC10273344_fullTextXML.xml`（159,507 B，SHA-256 前缀 `b12d98f239095640`；门禁显式排除 `.xml`，仅作取回凭据） |
| 本地全文②（本卡引句底稿） | `data/literature_cards/fulltext/K33_PMC10273344_text.txt`（74,368 B，SHA-256 前缀 `891544b57dd80f4f`；去标签单行纯文本，按核验器同一 `norm()` 归一后 73,865 字符） |
| 登记底稿③ | `sources/cost-benchmarks.md:121-125`（§3.5「物理 ΔΔG 判据对实验功能分的预测力其实很弱」），本卡数字与该段口径一致并补齐读出分层（见第 4/8 节） |
| 证据级别 | **全文级**（本卡所有引句均可在上述纯文本里逐字命中；见第 9 节自检） |
| 底稿元数据给的题录 | 头部一行含 `Protein Science`、`PMC10273344`、`37243972`、`10.1002/pro.4688`、卷期页 `32 7 e4688`、投稿/修回/接收日期（2023-02-03 / 2023-04-19 / 2023-05-24）。CSV 的 `PMID/PMCID/arXiv` 列登记为 未记录，故本卡把 PMID/PMCID 视为**底稿自带元数据，未独立核验**；只有 DOI 被 Crossref 核过（CSV `核验状态=✅Crossref核验`） |
| 未取到的部分 | 补充材料全部（Table S1 = 49 个数据集与基因清单及各自 MaveDB/文献编号、Table S3 = 五类读出的逐数据集归类、Figure S1 = VEP 相关矩阵、Figure S2 = 含 VEP 的完整排名）；正文 Figure 1/2/5/6 的原始数值只以热图与误差棒形式给出，**逐数据集 rho、逐数据集变体数、每组数据集条数均未以文本给出**。凡需要这些数字的地方本卡明写「正文未给出，仅有正文描述」 |
| 本文性质（影响解读） | **不是设计论文，也不是实验论文**：不生成任何新蛋白候选、不做湿实验，只把「9 个结构基稳定性预测器的分数」与「49 个已发表 DMS 数据集的实验功能分」两两求相关。全文没有 MD、没有 QM（ENCoM 用的是正则模态/正常模式分析，不是轨迹采样） |

## 1. 这篇到底解决什么（大白话 + 一句话）

**一句话**：高通量突变扫描（DMS）给每个突变打一个「表观功能分」，但这个分数是**某种读出的产物**（活得快不快 / 蛋白还剩多少 / 还结不结合 / 电流多大），不是「功能」本身。这篇用 17 万条单点错义变体，把「这个表观分能替功能说到什么程度」量成一组相关系数，并证明**系数的高低主要由读出类型决定，而不是由算法决定**。

**大白话版**：作者手上有一把物理尺（ΔΔG：这个突变让蛋白更稳还是更不稳，9 种工具算）和一堆实验分数（DMS：某个突变让细胞/蛋白在某项测定里表现如何，49 套测定）。他们做三件事：
1. **尺和尺先互量**——9 个预测器两两相关性平均只有 0.49（去掉最怪的 ENCoM 后 0.60），说明这些「物理分」彼此都不算一致；
2. **尺量实验分**——把每个预测器和每个 DMS 数据集求 Spearman 相关，结果整体很低：平均 **0.26（ΔΔG）/ 0.28（|ΔΔG|）**，最强的 FoldX 与 Rosetta 在bla(a)/bla(b) 也只有 0.66–0.68；
3. **按读出分组**——这一步才是本文真正的产品：**丰度/降解类读出（VAMP-seq、荧光融合定量）相关最高，病毒复制类最差，竞争性生长类逐基因忽高忽低**，而且「相关性的高低主要来自数据集之间，而不是预测器之间」。

**它为什么在我们的口径对照链上（CSV 组名 口径对照）**：这张卡给的不是「某判据能用」，而是一条**否定性的量级依据**——物理分数与实验功能分的对应关系天生只有 0.2–0.4 量级，且**同一基因换一种读出就会换一套排序**。这正是我们「只有一轮湿实验、四个构建体名额」时选读出的判据来源：选一个**只对应一件事**的读出当主判据，把**混着好几件事**的读出降级为旁证。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **同一个基因的 DMS 分数本身就不自洽——这是「表观分能否代表功能」的第一道漏洞**。不同组对同一基因做的实验给出的变体效应值会因条件与读出不同而漂移：原文给出的量级是 "they generally show moderate to high Spearman's correlations, averaging at around 0.66, suggesting that they represent a sufficiently robust approach to benchmark variant effect prediction performance"。→ **他们做了什么**：(i) 不合并同基因数据集，改用字母加括号把它们分开登记（"In this work, for cases where a single gene has multiple associated DMS datasets, we identify the datasets alphabetically, surrounded by parentheses"），于是 bla(a)/bla(b)/bla(d) 是三个独立考点；(ii) 把「同基因两套实验平均只到 0.66」当作**噪声上限**引用（来自前作 Livesey & Marsh 2020），而不是把它当失败。 **留下的代价**：既然实验彼此上限 ~0.66，任何「预测器 vs 实验 = 0.3」这类读数都同时被实验侧噪声打折，本文无法把「判据不准」与「读出本身不稳」分离。
2. **多条件数据集只能选一条，条件选择是判断性的**。很多 DMS 实验在不同药物浓度/温度/表达背景下各测了一遍。→ **他们做了什么**：定一条选取规则并写进正文："For the additional DMS experiments that contained fitness values from assays under multiple conditions, we selected the option most representative of native‐like conditions"，且解释什么叫 native-like（不给额外处理，只给测定本身要求的条件）。 **留下的代价**：「最像天然条件」由作者主观判定，正文未给出逐数据集选了哪一条（在 Table S1/S3，本卡未取到）。
3. **预测器要结构，但结构对不上变体位点**。DMS 变体按 UniProt 编号，PDB 结构经常缺链、缺残基、是 NMR 集、或压根没人解过。→ **他们做了什么**：一套写明的映射优先级——"choosing the first biological assembly for each structure as representative of the biologically relevant quaternary structure"、"Structures with best resolution followed by largest biological assembly were prioritized for mapping in the case of multiple available structures for a residue"、多占位只取第一条、NMR 取第一帧；为扩大覆盖把跨物种结构也放进来（"Protein chains with more than 90% sequence identity to a human protein over a region of at least 50 amino acid residues were considered"，并且 "Including nonhuman structures with this approach allowed us to substantially increase the size of our dataset"）；仍然映射不上的走 AlphaFold2（"Variants that could not be mapped to PDB structures were evaluated on AlphaFold2 models"），并引前作为模型结构可用作 FoldX 输入背书："It has been recently demonstrated that accurate stability predictions can also be delivered using modeled protein structures, with AlphaFold2 providing suitable inputs for FoldX even for proteins without homologs in the training set"。 **留下的代价**：模型结构没有复合物语境（AFDB 是单体），所以「用完整生物组装体」这条本文最重要的增益，恰恰在 AF2 兜底的那部分变体上拿不到；本文没有量化这一损失。
4. **各预测器覆盖的变体集合不齐，直接算平均会把缺数据的方法判死**。"Some predictions for certain datasets or variants could not be completed due to software or webserver errors"（INPS3D/mCSM/DynaMut2/PoPMuSiC 全靠网页服务器爬取）。→ **他们做了什么**：两招——相关只在两个方法都有值的**共同子集**上算（"The advantage of this ranking strategy is that it accounts for the fact that not all methods successfully made predictions for all mutations in all proteins"），排名得分再除以该方法的**成功比较次数**归一（"This normalization also gives a chance for predictors with a few missing DMS datasets not to fall behind in the scoring scheme due to undersampling issues"）。 **留下的代价**：不同方法的 rho 分母不同，横向数值不完全可比；正文未给每个方法实际参与的比较条数。
5. **ΔΔG 的符号都靠不住——工具经常把增减方向算反**。作者带着前一轮经验进来：把强稳定化变异也当作有害来算（用 |ΔΔG|）能提升疾病判别，"considering strongly stabilizing variants as deleterious through use of |ΔΔG| improves the disease identification performance of most stability predictors, likely due to stability predictors sometimes mispredicting the sign of the ΔΔG"。→ **他们做了什么**：两套口径全程并排跑（ΔΔG 与 |ΔΔG|），且明确写出方向对齐约定："Both the predictor and DMS score directions were adjusted for consistency"。 **应对结果是一条反直觉结论（他们如实报了）**：在 DMS 排序任务上换绝对值几乎不改变名次（"Using either ΔΔG or |ΔΔG| values results in very similar rankings overall"），而在丰度型子集上反而是**带符号的原始值更好**。代价：同一批工具在「致病/良性分类」与「功能分排序」两种任务上需要不同口径，本文没有给出该在什么时候用哪一个的判据。
6. **相关系数天然有上限，不能把低相关直接读成「工具烂」**。→ **他们做了什么**：把上限写进正文而不是留给读者猜——"even direct experimental thermostability values and computational predictions are often shown to only correlate on the order of ~0.5, with some works showing that the practical upper bound for such comparisons can only reach ~0.8 due to experimental data quality"，并拿第三方同口径结果对齐："This is in‐line with the recent observations from Høie et al. showing an average Spearman's correlation value of 0.25 between Rosetta ΔΔG and a number of DMS datasets"。 **留下的代价**：这些上限来自文献而非本文实测，本文自己的上限数字（0.66 同基因一致性）与文献上限（~0.8）之间没有解释。
7. **一批体系怎么算都低相关（这是本文最主要的一次「判据失效」，而且作者给出了机制解释）**。CALM1、TARDBP、SRC 的相关性系统偏低："This is likely to contribute to the low correlations observed for CALM1, TARDBP and SRC datasets, which are known to also be associated with non‐loss‐of‐function disease mechanisms"；他们前作的机制结论在引言里就铺好了："Other types of assays, such as general competitive growth experiments, are potentially sensitive to non‐destabilizing but damaging mutations, such as those associated with gain‐of‐function or dominant‐negative effects"。同一个 bla 靶换一次实验（bla(d)）最好也只有 0.44。→ **他们做了什么**：不清洗这些靶、不给它们开后门，而是**把「读出与机制是否对应」提出来当正式问题**（第 8 节那一组分组分析），并明确把低相关归到机制而非工具缺陷。 **本文未解决**：没有任何补救——既没有为显性负/获得功能机制设计新打分，也没有给「这一批低相关数据集能否用别的读出重测」的方案。
8. **结合类读出普遍算不准，查下去发现是结构里根本没有被测的那个配对体**。→ **他们做了什么**：逐个查结构覆盖度，"structures for HRAS (PDB IDs: 2CE2 and 6P0Z ) and PSD95 (PDB ID: 6QJL ) did not contain the binding partners relevant for the specific DMS assays, or were monomeric, explaining the inability of stability predictors to reflect intermolecular interactions"，而结构对得上的 GAL4（3COQ，二聚体+DNA）与 BRCA1(a)（BRCA1-BARD1 异源二聚体）就明显上升（原文该句以 For example 起头，故小写）："both FoldX and Rosetta showed marked increases in correlation with GAL4 DMS values"、"as opposed to just the monomeric subunit in isolation"。 **本文未解决，作者明写**："More suitable complex structures were not currently available in the PDB"——即这条改进被数据库覆盖度卡住，不是被方法卡住；并且整体仍有 "Curiously, half of the binding‐based assays do not show good agreement even with FoldX or Rosetta, which are able to evaluate interactions in complex structures, or show a marked improvement between predictions derived on monomeric structures vs fullest available structure"。
9. **组内均值会被个别数据集主导**。activity 组看着不错，作者自己拆了台："Activity‐based assays show good agreement mostly due to high correlations on the GFP datasets, which are bound to be more representative of loss‐of‐function mechanism mutations"。→ **他们做了什么**：按组给均值 + 误差棒（"Error bars denote the 95% confidence interval, found by using the Fisher z transform of the correlation"），并额外只取丰度型子集重跑一遍排名（Figure 6），让「哪个结论依赖哪个子集」可见。 **留下的代价**：分组样本量在正文未给（Table S3 未取回），读者无法自行判断每组均值被几个数据集撑着。
10. **单一工具都太弱，于是做集成**。意外发现：把 FoldX 与 Rosetta 直接取平均就明显变强，"combining complex‐based scores from the two tools produces a superior predictor, with the Foldetta_comp ensemble coming out ahead by ~0.15 points in the ranking"，而且这与那些多特征方法的失败形成对比——"the ensemble score correlates better with DMS data, matching the performance of VEPs and even substantially outperforming them when only ranking methods on abundance‐based datasets"。→ **他们做了什么**：不做训练、不加权重，只做**单位对齐后的算术平均**（Rosetta 要先换算："As Rosetta predictions are initially produced in REUs (Rosetta Energy Units), they need to be divided by a scaling factor of 2.94"；绝对值情形先取众数再合）。 **本文未解决**：为什么 DynaMut2/DDGun3D/INPS3D 这类内部已经在做组合的方法反而不灵，作者只给猜想（"perhaps with a specific emphasis on methodologies based on empirical potentials that approximate physics terms"），没有实验分辨。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **实验侧分数（不是他们做的）**：49 个已发表 DMS/MAVE 数据集、39 个唯一靶、170,940 个单点错义变体。读出五花八门，作者逐类点名：人基因在酵母里互补原生基因的竞争性生长（最常见那一类）、"VAMP‐seq is another methodology, which interrogates the abundance of GFP‐fused variant proteins and thus also their stability"、毒性测定、双杂交/噬菌体展示的结合强度变化、以及靶专用活性测定（原文举例："patch‐clamp assessment of cell currents for KCNQ4 potassium channel variants"）。数据集来源是前两轮 VEP 基准 + MaveDB 新入库数据。
- **被测的判据（本文主角，9 个结构基稳定性预测器）**："We tested nine stability predictors, seven of which we have previously also explored for their ability to distinguish between pathogenic and putatively benign human variants" — FoldX 5.0、Rosetta（Cartesian ΔΔG）、ENCoM（正常模式分析）、DDGun3D（无训练）、INPS3D、mCSM、DynaMut2、PoPMuSiC、RaSP（序列输入的神经网络）。其中只有三个能直接吃复合物结构："FoldX, ENCoM and Rosetta were also evaluated in terms of full protein complex structures, if they were available"。
- **对照判据（另一条口径）**：7 个变异效应预测器 VEP —— 两个替换矩阵（BLOSUM62、Grantham）作基线，SIFT、PROVEAN、SNAP2、DeepSequence、EVcouplings。选型理由写得很直白："Many of our DMS dataset genes are not of human origin, and many VEPs are not designed to produce predictions for nonhuman proteins" → "We thus picked a small selection of methodologically diverse methods that had produced a sufficient number of predictions for most DMS datasets"。
- **共识分（本文提出的东西）**：Foldetta = "The Foldetta stability score was derived as a mean of FoldX and scaled Rosetta predictions for each variant"，绝对值情形先取众数再合。
- **统计口径**：全成对 Spearman 相关（完整观测）、方向统一约定、成对投票排名 + 二项 95% 置信区间 + Fisher z 误差棒。
- **本文没有的东西（重要）**：没有 MD（ENCoM 是正则模态分析，不是轨迹采样）、没有 QM、没有新湿实验、没有从头设计、没有前瞻验证、**也没有任何通过/淘汰型阈值**（全文只给相关系数与协议参数）。

### A. 数据集与结构的准备（把实验分数变成可比的对象）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 前作 VEP 基准的数据集 + MaveDB 新数据集 | 汇总、去重、按基因登记；同一基因多套实验用字母区分 | 选取规则："For the additional DMS experiments that contained fitness values from assays under multiple conditions, we selected the option most representative of native‐like conditions" | "For this study, we gathered 49 different DMS datasets for 39 unique protein targets"；"In this work, for cases where a single gene has multiple associated DMS datasets, we identify the datasets alphabetically, surrounded by parentheses"（完整清单在 Table S1，**本卡未取到**） |
| A2 | 每个数据集的变体（UniProt 编号） | 建「结构变异映射表」：PDB 优先，取首生物组装体 | "Protein chains with more than 90% sequence identity to a human protein over a region of at least 50 amino acid residues were considered"；非人结构只有当该残基及邻近残基与人野生型一致才允许映射；多结构并存时 "Structures with best resolution followed by largest biological assembly were prioritized for mapping in the case of multiple available structures for a residue"；多占位取第一条、PDB 缺失残基不考、"For NMR ensembles the first frame was chosen" | 覆盖度提升："Including nonhuman structures with this approach allowed us to substantially increase the size of our dataset"（逐靶覆盖条数未给） |
| A3 | 映射不到 PDB 的变体 | 走 AlphaFold2 模型兜底 | "Variants that could not be mapped to PDB structures were evaluated on AlphaFold2 models"；按 UniProt 序列位置映射 | AF2 模型下载日期与入口："AlphaFold models were accessed and downloaded on July 27, 2021" |
| A4 | 170,940 个变体 × 9 个预测器 | 逐工具跑分；单体输入，FoldX/Rosetta/ENCoM 另跑复合物输入 | 无阈值；工程可用性即门槛（服务器/软件报错者记为缺失） | 全集规模："we compare the predictions of 9 protein stability‐based tools against mutant protein fitness values from 49 independent DMS datasets, covering 170,940 unique single amino acid variants"；缺失量："Some predictions for certain datasets or variants could not be completed due to software or webserver errors" |

### B. 预测器实际怎么跑的（Methods 4.2 的参数逐条抄）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | PDB/AF2 结构 | FoldX 5.0 | "FoldX 5.0 was run using default parameters as previously described"；先过 RepairPDB（该句在原文里带函数名的引号，本卡不作引句），再算 ΔΔG；单体与复合物两种输入都跑 | 全部变体 |
| B2 | 同一批结构 | Rosetta Cartesian ΔΔG | "The Cartesian ΔΔG application from Rosetta suite (Linux build 2021.16.61629) was run based on the protocol laid out in Park et al. ( 2016 ), while using the Ref2015 scoring function"；按协议做 relaxation | "Results from three prediction iterations were averaged and ΔΔG values were derived by taking the difference between the wild‐type and mutant values for each individual run" |
| B3 | 含非标准残基的复合物 | 手工改造后再跑 Rosetta | 二硫键可识别 | "For complex evaluation, PDB structures 4JZW and 4JZZ were modified to introduce cysteines instead of some nonstandard residues for Rosetta to recognize the disulfide bonds" |
| B4 | ENCoM / DDGun3D | 本地源码跑 | ENCoM 单体与复合物各跑一遍（两个独立实例）；DDGun 用 3D 协议 | "DDGun (Montanucci et al., 2022 ) source code was downloaded" |
| B5 | 序列 | RaSP 走改过的 Google Colab notebook；INPS3D、mCSM、DynaMut2、PoPMuSiC 走网页服务器（Python 3.8.8 + RoboBrowser / Selenium） | 原文注明部分预测因此失败 | "RaSP (Blaabjerg et al., 2023 ) was run on a modified Google Colab notebook" |
| B6 | FoldX + Rosetta 两套分 | 合成 Foldetta | 单位先对齐："As Rosetta predictions are initially produced in REUs (Rosetta Energy Units), they need to be divided by a scaling factor of 2.94"；绝对值情形先取 FoldX 与 Rosetta 的众数再合 | 逐变体一个共识分 |
| B7 | VEP 分数 | 沿用前作已算好的 VEP 值；新数据集用同一管线补算 | 有 dbNSFP 4.0 就取现成的；SNAP2 走网页、EVcouplings / SIFT / DeepSequence 本地跑 | 7 个 VEP 的逐变体分 |

### C. 评价与归因（本文真正的产出）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | 9 个预测器的全量分 | **先量尺和尺**：预测器两两 Spearman，ΔΔG 与 \|ΔΔG\| 两个口径（Figure 1） | 排除同一预测器单体 vs 复合物、以及 DynaMut2 与其成分 mCSM 的相关 | "Without taking the high correlation between monomeric vs complex predictions for the same predictor into account, or DynaMut2 and its methodological component mCSM, we see that, overall, most of the predictors also show fairly good agreement with each other, with the average absolute Spearman's rho value for ΔΔG at 0.49, rising to 0.60 if we exclude ENCoM"；两个极端："ENCoM predictions stand out as the most unrelated to any other predictor, with the highest correlation for ΔΔG being with DDGun3D at 0.23"、"The highest correlations of 0.76 were observed between DDGun3D and INPS3D, as well as 0.75 between RaSP and Rosetta" |
| C2 | 预测器分 × 49 个数据集 | **再量尺和实验**：逐（预测器, 数据集）对算 Spearman，只用共同观测子集；方向统一到「越大越有害」 | "Both the predictor and DMS score directions were adjusted for consistency"；绝对值口径并行跑 | 图 2 热图（逐格数值未取到）；总均值见下面 prose 原句（平均只有 0.26 / 0.28） |
| C3 | 同上 | 排名：每对预测器在每个数据集上比大小 | "Each predictor would be given a point for demonstrating a higher Spearman's rho value for a DMS set against another prediction tool, or both would get half a point for a tie"；"The correlation values were rounded to two digits after the decimal point and were compared only if neither predictor was completely missing data for a given DMS dataset"；"This normalization also gives a chance for predictors with a few missing DMS datasets not to fall behind in the scoring scheme due to undersampling issues" | Figure 4；"Error bars denote the 95% confidence interval of a binomial test"；两条结论原句见下面 prose（名次几乎不变、Foldetta_comp 领先约 0.15 点）；垫底 "the four methods that show the least correspondence with DMS rankings are DynaMut2, mCSM, ENCoM for complexes and ENCoM for monomers" |
| C4 | 加入 VEP 后重排 | 同一投票口径下把 7 个 VEP 一起排 | 同上 | "Figure S1 shows that, compared to stability predictors, VEP correlations are considerably higher and more consistent across the different gene datasets"；"They achieve average Spearman's correlations of 0.36, and 0.42 if we exclude the BLOSUM62 and Grantham substitution matrices"（对比稳定性分的 ~0.26）；"FoldX and Rosetta outperform the substitution matrices and SIFT, but cannot perform as well as modern VEPs for predicting functional scores from DMS experiments"；"the combined Foldetta score shows substantial capacity to accurately reflect the relative functional impacts of variants, comparable to the top tested VEPs-EVcouplings and SNAP2"（Figure S2 未取到） |
| C5 | 49 个数据集 | **按读出类型分五组**，逐组算均值（Figure 5） | 分组依据与归类表在 Table S3（未取到）："we classified the DMS datasets broadly into five groups, as outlined in Table S3 , depending on the phenotype assaying approach"；组定义原文："Abundance‐based assays represent experiments that make use of VAMP‐seq and other fluorescent‐tagging approaches that can quantify protein expression and stability in cells, being able to directly assess whether variants lead to a loss‐of‐function through degradation"、"Growth experiments involve mutant competition or antibiotic survival and are able to characterize functional effects from multiple molecular mechanisms"、"The activity assay category includes target‐specific experimental setups more directly measuring the functional mutant effects, and not just through the proxy of growth or protein stability"；病毒复制组单列 | "The trend clearly demonstrates that stability predictors best reflect functional scores from abundance‐based DMS datasets, both in the case of only the best methods, as well as for all predictors, while viral replication datasets show the worst agreement"；误差棒口径："Error bars denote the 95% confidence interval, found by using the Fisher z transform of the correlation"；"Only raw ΔΔG values from stability predictors were used in the comparison" |
| C6 | 读出侧的失败案例 | 逐个查结合类数据集的结构覆盖，定位「低相关是结构缺配对体」还是「方法不行」 | 以「复合物里有没有被测的那个对象」为判据 | 反面："structures for HRAS (PDB IDs: 2CE2 and 6P0Z ) and PSD95 (PDB ID: 6QJL ) did not contain the binding partners relevant for the specific DMS assays, or were monomeric, explaining the inability of stability predictors to reflect intermolecular interactions"；正面："The GAL4 structure (PDB ID: 3COQ ) contains a transcription factor dimer that is bound to a DNA duplex, allowing us to evaluate variant effects both on dimerization and DNA recognition"、"The BRCA1(a) dataset was derived from an assay interrogating BRCA1‐BARD1 heterodimer interactions, which are represented in the structural data (PDB IDs: 7JZV and 1JM7 )"；上限 "More suitable complex structures were not currently available in the PDB" |
| C7 | 只取丰度型读出 | 在「最适合失活预测」的子集上重跑排名，把 VEP 一起拉进来（Figure 6） | 子集定义：VAMP-seq 与其他荧光法 + 该子集上只用原始 ΔΔG；"In our comparison we also included VEPs to see how stability predictors compare on DMS datasets that are best suited for loss‐of‐function prediction" | "Figure 6 shows a considerably steeper rank distribution, strongly establishing the combined Foldetta score not only as the approach most reflective of functional assay scores among stability‐based methods, but also as the overall best predictor, significantly outperforming all VEPs in the case when predictions from complex structures are used against abundance‐based DMS scores"；子集内数据集条数正文未给（未记录） |
| C8 | GAL4 单案例 | 结构级可视化：把 DMS 分与 FoldX 分做秩归一后逐位点比较 | 两列都归一到 0-1；取绝对值形式（相关更好）；剔除方向相反的变异："any variants that were indicated to increase the functional outcome of the DMS assay were removed to focus on the loss‐of‐function aspect of the predictions"；正 delta = FoldX 低估功能效应，负 delta = 高估，接近 0 = 一致 | Figure 3；"The DMS dataset for GAL4 contains variant enrichment scores from a yeast two‐hybrid experiment"；"GAL4 variants used for the analyses were mapped to PDB structure 3COQ, containing a GAL4 dimer and a DNA double‐strand"；逐位点取中位数（图注口径） |

### C-补. 上表里被拆出来的两句原话（含绝对值符号，为避免表格断列单独成行）

- 总均值： "the overall correlations tend to be fairly low, with the average rho values throughout the benchmark at 0.26 and 0.28 for ΔΔG and |ΔΔG|, respectively"
- 名次稳定性： "Using either ΔΔG or |ΔΔG| values results in very similar rankings overall"；共识分增益： "combining complex‐based scores from the two tools produces a superior predictor, with the Foldetta_comp ensemble coming out ahead by ~0.15 points in the ranking"

**这套流程的骨架值得单独记住（三步走的顺序本身是产品）**：C1 **先量判据之间的一致性**（0.49），确认这些分数不是同一个东西 → C2/C3 **再量判据对实验分的一致性**（0.26，FoldX/Rosetta/Foldetta 最高）→ C5–C7 **最后把「实验分」本身拆开**，按读出类型分组、把某一类单独重跑（发现排序可以整体翻转）。**第 2 步和第 3 步的顺序不能颠倒**：先算总平均只会得到「物理判据都很差」这个错误结论；按读出分组之后才看得见「在丰度型读出的物理判据上，它其实超过所有专用预测器」。

## 4. 关键数字台账（数值 · 含义 · 出处；数值均可在本地全文里搜到）

| 数值 | 含义 | 出处（本卡小节 · 原文位置） |
|---|---|---|
| 49 / 39 / 170,940 / 9 | DMS 数据集数 / 唯一靶数 / 唯一单点错义变体数 / 稳定性预测器数 | §1、§3 A1、A4 · Abstract 与 Results 2.1 |
| 一个基因多套实验 | 「表观分数依赖读出」的最小内部证据：bla 靶至少有 (a)(b)(d) 三套、BRCA1 至少 (a)(b) 两套；逐靶数据集数在 Table S1，**正文未给计数** | §2.1、§5.1 · Results 2.1–2.2 |
| 0.66 | **同一基因的两套 DMS 实验之间**的 Spearman 平均值（读出侧噪声/口径漂移的尺度） | §2.1 · Results 2.1（引 Livesey & Marsh 2020） |
| 0.49 → 0.60 | 9 个预测器**两两一致**的平均 \|rho\|（ΔΔG 口径）；去掉 ENCoM 后升到 0.60 | §3 C1 · Results 2.1 + Figure 1 |
| 0.23 | ENCoM 与任何其他预测器的**最高**相关（对象是 DDGun3D）——它是全局最不合群的尺 | §3 C1 · Figure 1 图注段 |
| 0.76 / 0.75 | DDGun3D–INPS3D 最高成对相关 / RaSP–Rosetta 成对相关（后者的原因：RaSP 是用 Rosetta 输出训练的） | §3 C1 · Results 2.1 |
| 0.26 / 0.28 | **稳定性分与 DMS 功能分的平均 Spearman**（分别用 ΔΔG 与 \|ΔΔG\|）——本文最重要的那个「很低」 | §3 C-补 · Results 2.2 |
| 0.25 | 第三方（Høie et al. 2022）Rosetta ΔΔG 与若干 DMS 数据集的平均 Spearman，作者用来对齐自己的量级 | §2.6 · Results 2.2 |
| ~0.5 与 ~0.8 | 直接实验热稳定性数据与计算预测之间通常只到 ~0.5；文献给出的实践上限 ~0.8（受实验数据质量限制） | §2.6 · Results 2.2 |
| 0.57 | 单靶最好案例之一：NUDT15（引 Cagiada et al. 2021） | §5 · Results 2.2 |
| 0.66–0.68 | 本基准**全局最高**相关：FoldX 与 Rosetta 在 E. coli β-内酰胺酶 bla(a)/bla(b) 抗生素抗性数据集上的区间 | §5.1 · Results 2.2 |
| 0.44 | 同一个 bla 靶的另一套实验 bla(d) 的最好相关（换读出即换结论的直接证据） | §2.7、§5.1 · Results 2.2 |
| 0.61 | Rosetta 复合物 ΔΔG 与 UBI4(b)（FACS 丰度类读出）的相关 | §5.1 · Results 2.2 |
| 0.53 | 其余基因里第二梯队数据集能达到的最高 rho（ΔΔG 与 \|ΔΔG\| 两个口径都是） | §5.1 · Results 2.2 |
| 0.36 | ENCoM 从「带符号」换到「绝对值」口径时 rho 的最大提升幅度（说明它系统性把变异预测成稳定化） | §2.5 · Results 2.2 |
| 0.36 / 0.42 | **VEP 组**对 DMS 的平均 Spearman；0.42 是剔除 BLOSUM62 与 Grantham 两个替换矩阵后的均值 | §3 C4 · Results 2.3 |
| ~0.15 | Foldetta_comp（复合物口径共识分）相对最好单工具的排名得分领先量（单位是投票排名点，不是 rho） | §3 C3 · Results 2.3 + Figure 4 |
| 5 组 | 读出类型分组数：丰度 / 生长 / 结合 / 活性 / 病毒复制 | §3 C5 · Results 2.4 + Table S3（未取到） |
| 90% / ≥50 残基 | 跨物种结构映射门槛：与人蛋白 >90% 一致性、且比对区域至少 50 个氨基酸 | §3 A2 · Methods 4.1 |
| 2.94 | Rosetta REU → kcal/mol 的换算因子（Foldetta 之前必须做） | §3 B6 · Methods 4.2（取自 Park et al. 2016） |
| 2021.16.61629 / Ref2015 / 3 次迭代取平均 | Rosetta Cartesian ΔΔG 的构建号、打分函数与重复数 | §3 B2 · Methods 4.2 |
| 两位小数 / 平局各半分 / 除以成功比较次数 | 投票排名的三条统计细则（决定名次可复现性） | §3 C3 · Methods 4.3 |
| July 27, 2021 | AlphaFold 模型取用日期（作者登记的兜底输入版本） | §3 A3 · Methods 4.1 |
| PDB 号 3COQ / 7JZV / 1JM7 / 2CE2 / 6P0Z / 6QJL / 4JZW / 4JZZ | 分别对应：GAL4 二聚体+DNA（相关上升）、BRCA1-BARD1（相关上升）、HRAS 与 PSD95（**缺被测配对体，导致低相关**）、Rosetta 复合物计算中被手工换成半胱氨酸的两个结构 | §3 C6、B3 · Results 2.4 + Methods 4.2 |
| 0（本文无） | 全文不含分子动力学、不含量子化学、不含任何通过/淘汰型阈值、不含前瞻湿实验 | §3 工具箱末条、§7 |

## 5. 结论——作者说了什么

1. **谁最能替功能分说话**：FoldX 与 Rosetta 最强，且这与它们此前在「致病 vs 良性」分类任务上的顶尖表现一致；"Rosetta and FoldX stability predictions for the E. coli beta lactamase (bla) antibiotic resistance DMS datasets bla(a) and bla(b) produced the highest observed correlations in this benchmark, ranging between 0.66 and 0.68, while the best correlation for bla(d), a different antibiotic resistance experiment, was only 0.44"；此外 "Rosetta complex ΔΔG values also appear to correlate well (0.61) with dataset UBI4(b), based on a FACS assay that relates well to stability"、"The next best correlating datasets for other genes had Spearman's rho values of up to 0.53, across both ΔΔG and |ΔΔG|"。
2. **整体对应度就是低**，而且低得可以第三方对齐："the overall correlations tend to be fairly low, with the average rho values throughout the benchmark at 0.26 and 0.28 for ΔΔG and |ΔΔG|, respectively"、"This is in‐line with the recent observations from Høie et al. showing an average Spearman's correlation value of 0.25 between Rosetta ΔΔG and a number of DMS datasets"。上限口径也被写死："even direct experimental thermostability values and computational predictions are often shown to only correlate on the order of ~0.5, with some works showing that the practical upper bound for such comparisons can only reach ~0.8 due to experimental data quality"。
3. **整体异质性主要来自数据集而不是工具**："We have observed that the highest heterogeneity in correlation values arises not between different predictors, but across DMS datasets"（图注同义句："Stability predictor scores can correlate highly with scores from DMS experiments, but performance is highly heterogenous"）。
4. **用复合物结构（把分子间相互作用算进去）会明显改善**："we also explored how taking into account intermolecular interactions, by using complex structures, impacts variant stability prediction, and in turn the evaluation of functional effects"；正面案例是 GAL4：原句以 For example 起头，本卡按底稿小写照引 "both FoldX and Rosetta showed marked increases in correlation with GAL4 DMS values"、"as opposed to just the monomeric subunit in isolation"，图注解释为什么："showing that hotspots of highest functional variant impact appear not only at the protein dimer interface, but also at interaction sites with DNA"。
5. **共识分 Foldetta 更强**："combining complex‐based scores from the two tools produces a superior predictor, with the Foldetta_comp ensemble coming out ahead by ~0.15 points in the ranking"；与 VEP 同台时 "the combined Foldetta score shows substantial capacity to accurately reflect the relative functional impacts of variants, comparable to the top tested VEPs-EVcouplings and SNAP2"。作者特意把这归为「无训练集成」的价值："but demonstrates the utility of even simple untrained ensembling when combining the right inputs"。
6. **读出类型决定一切（本文的主结论）**："predicted stability effects show consistently higher correlations with certain DMS experimental phenotypes, particularly those based upon protein abundance"；分组实测："The trend clearly demonstrates that stability predictors best reflect functional scores from abundance‐based DMS datasets, both in the case of only the best methods, as well as for all predictors, while viral replication datasets show the worst agreement"；生长类："Competitive growth assays, which are a popular generalized approach, appear to show mixed agreement on a per‐gene level, but are not well correlated with changes to stability overall"；结合类一半不灵："Curiously, half of the binding‐based assays do not show good agreement even with FoldX or Rosetta, which are able to evaluate interactions in complex structures, or show a marked improvement between predictions derived on monomeric structures vs fullest available structure"。
7. **在丰度型子集上，物理稳定性判据反超所有被测 VEP**："strongly establishing the combined Foldetta score not only as the approach most reflective of functional assay scores among stability‐based methods, but also as the overall best predictor, significantly outperforming all VEPs in the case when predictions from complex structures are used against abundance‐based DMS scores"；同时作者保留方向性口径的价值："they offer a clear advantage over VEPs in terms of interpretability of mechanistic effects, especially in this case where we see that raw stability predictions correlate better than absolute values with functional DMS scores"。
8. **作者自己给结论设的边界（原话层面，必须一起引用）**：(i) 排名好 ≠ ΔΔG 算得准："stability predictors are not designed for disease variant identification, and their training and design is aimed at reproducing realistic ΔΔG values that reflect experimental thermostability changes, and not at ranking functional impacts"；(ii) 全局上 VEP 仍更好用："FoldX and Rosetta outperform the substitution matrices and SIFT, but cannot perform as well as modern VEPs for predicting functional scores from DMS experiments"；(iii) 非失活机制测不到："In these cases, both stability predictors and abundance‐based DMS experiments will be less likely to accurately reflect the biologically important impacts of variants"，而且 "not all loss‐of‐function missense mutations will be due to protein destabilization: for example, they may impact functionally important sites or perturb protein allostery"、"Moreover, gain‐of‐function and dominant‐negative mechanisms are also common pathogenic mechanisms"；(iv) 多功能蛋白必须多读出："In the case of proteins with multiple functions or disease mechanisms, multiple different assays would be required to gleam the full scope of a variant"；(v) 竞争性生长虽然覆盖最广但会丢归因："although, the delineation of what molecular mechanism might be responsible for the increase or reduction in fitness is lost"；(vi) DMS 自身的通用缺陷与成本："Other general issues with DMS data are that it can be noisy, restricted to a small set of experimental conditions, and also removed from the original cellular context"、"Due to these limitations, as well as the enormous resource cost of most current DMS methodologies, they are unlikely to replace computational prediction tools as the main avenue to fully understanding functional effects of missense mutations in the near future"；(vii) 他们指出的下一步是换读出而非换算法："cDNA display proteolysis, was recently shown to be capable of assessing functional variant effects on protein thermodynamic stability at tremendous scale and speed"，但立刻限定 "While limited to a stability phenotype, such a DMS approach also presents a valuable opportunity"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **「选哪个读出」是比「选哪个算法」更高阶的决策，而且这篇把它量化了**。作者只说了异质性来自数据集（第 5.3 条），我们读出的是它的工程含义：如果同一个基因换一套读出就能把 rho 从 0.66 打到 0.44（bla 案例），那么「我们的候选分数与某个实验读数一致」这句话，必须先声明是哪套读数，否则它不带信息。→ 对我们：任何「湿实验支持我们的判据」的结论都要写成「判据 × 读出类型 × 结局」三元组，不许写成「判据 ↔ 功能」。
2. **表观功能分是机制的混合物，所以它天生不能归因**。竞争性生长把折叠、表达、降解、相互作用、毒性、代谢负担压进同一个适应度数；作者的上半句（覆盖最广）与下半句（归因丢失）其实给出了一个我们该照抄的取舍框架：**要广度就丢归因，要归因就丢广度**。→ 我们一轮只做四个构建体，买不起广度，只能买归因，所以主读出必须是「一个数只对应一个化学事件」的那种。
3. **0.26 这个量级应当变成我们的默认预期，而不是我们的失败证据**。若某便宜判据与湿实验结局的 Spearman 落在 0.2–0.4，这在同类「物理分 vs 实验功能分」比较里是正常水平（本文 0.26、Høie 0.25）；反之若有人报 0.6 以上，第一反应应该是问「是不是只看了丰度型读出」——本文里唯一能让物理分反超专用 VEP 的场景，恰恰是被挑出来的丰度子集（第 5.7 条）。这是**子集选择能造出多大奇迹**的样本。
4. **「同一物种同一基因的两套实验只到 0.66」应折算进我们自己的复现预算**。我们计划用重复构建体来「验证」结果，但这篇给的经验上限说明：两套都有效、但都只测自己那件事的读数，本来就不会完全一致；若两次读数彼此不一致，**先假设是读出定义不同，而不是其中之一做错**。
5. **Foldetta 的真正启示是给「无标签时的集成」找到了便宜做法**：它不用训练、不用权重，只要单位换算 + 算术平均（+0.15 排名点）。→ 我们现在**没有任何结局标签**（DP2R 口径：至今无一条被产物化学确认的天然 UAA 合成酶），所以「加权集成/学习式集成」这条路根本没有地基；能立刻抄的只有这种**秩/均值式无训练共识**。同时注意它的边界：Foldetta 只在同类物理来源（经验势家族 FoldX + Rosetta）之间有效，把两个不相关的量（例如几何分数与序列保守度）平均起来本文没测过，不保证有效。
6. **|ΔΔG| 与 ΔΔG 的口径翻转（第 2.5 条）说明「分数该不该带方向」也是读出的函数**。在分类任务上取绝对值更好，在丰度型排序上带符号更好。→ 我们的判据（例如 MD/xTB 垒高、几何偏差）在设计漏斗闸口时，「用带符号的量还是用幅度」不该一次定死，应当在小面板上两条口径都跑，再按结局类型决定；并且要把「这个判据的方向在物理上对应哪一步化学事件」写进判据定义（DP2R 的 G0/G6 类要求）。
7. **本文是「判据审计」的一个范式：判据本身不是产品，审计口径才是产品**。全文没有任何阈值、没有任何被推荐的绝对分数，产出的是「哪种读出下谁更相关、以及整体有多不相关」。→ 对我们：在结局标签稀缺的现在，**能对判据做的事只有这种审计型结论**，不要指望从这篇文章里借到任何可用的分数门槛。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自陈（可回原文核对）**

- 排名的含义被限死：判据在「替功能分排序」上排第一，不代表它把 ΔΔG 本身算准了（第 5.8(i) 条原句）。
- 全局打不过 VEP：稳定性分平均 0.26 vs VEP 0.36/0.42；Foldetta 只是「追平」EVcouplings/SNAP2，反超只发生在丰度子集（§5.5–5.7）。
- 非失活机制是结构性盲区：显性负与获得功能变异在结构上温和，稳定性分与丰度型读出**双双**测不到（"In these cases, both stability predictors and abundance‐based DMS experiments will be less likely to accurately reflect the biologically important impacts of variants"），且 LOF 里也有一大类不是降解造成的（"not all loss‐of‐function missense mutations will be due to protein destabilization: for example, they may impact functionally important sites or perturb protein allostery"）。
- 复合物结构受 PDB 覆盖度卡死："More suitable complex structures were not currently available in the PDB" —— 结合类读出有一半就是因此拿不到增益（§2.8）。
- 分组均值受个别数据集主导（activity 组几乎全靠 GFP 数据集）；DMS 数据本身"can be noisy, restricted to a small set of experimental conditions, and also removed from the original cellular context"。
- 本文对疾病变异识别的实际可用性留了明确的保留："While this current generation of stability predictors are not likely to be particularly useful in the direct identification of pathogenic variants on the proteome scale, compared to state‐of‐the‐art VEPs, they offer a clear advantage over VEPs in terms of interpretability of mechanistic effects" —— 也就是说，作者卖的是**可解释性**，不是**准确率**。

**我们读出的额外风险**

1. **全文没有一次前瞻实验，也没有一次自做的湿实验**。所有数字都是从别人的数据集里重算的，49 个数据集的测序深度、突变覆盖率、重复数在正文一概未给（Table S1 未取回）。因此「平均 0.26」这个头条数，我们**无法自行复核它的分母构成**，只能在作者断言层面接受。
2. **Figure 1/2/5/6 的数值只以热图与柱状+误差棒呈现**，正文只报作者点名的极值（0.66–0.68、0.44、0.61、0.53、0.57、~0.15）。我们看不到分布形状，也就看不到「FoldX/Rosetta 的高相关是不是由少数靶撑着」——而作者自己已经承认 activity 组正是这种情形，所以同类偏倚在别处不能排除。
3. **丰度子集（Figure 6）的数据集条数正文未给**。那句最强的结论（Foldetta 超过所有 VEP）建立在一个规模未知的子集上；引用这句话必须连「子集未定量」一起说。
4. **0.66（同基因两套实验）是转引前作的数**，不是本文独立测的；本文只是拿它当「DMS 够用」的论证。若有人想引用「DMS 之间的复现上限」，出处应回到 Livesey & Marsh 2020，而不是这张卡。
5. **相关系数回答的是排序，不回答可分性**。漏斗需要的是「这个候选过不过」，而 rho 高不代表两个类群之间存在可分间隔；本文全程没做 ROC/AUC、没给任何分类指标。→ 把这篇当「某判据可用」的证据是错误的用法，它顶多支持「某判据在某类读出上排序有信号」。
6. **AF2 兜底与复合物增益互斥**（§2.3 代价的推论）：单体 AF2 模型没有相互作用语境，于是「复合物输入更强」这条结论在最需要它的新蛋白/无结构蛋白上恰好失效。本文没有量化这个失效面。
7. **稳定性这一维被过度代表**：本文全部判据都是「扰动稳定性」这一个物理量，全部对照都围绕它。对催化几何、预组织、底物选择性、竞争副反应，它没有任何证据——正反都不能引。

## 8. 对 UAA 筛选的迁移判断（重点：只有一轮湿实验时，主读出选哪种、哪种只能当旁证）

我们的约束条件先说清楚：一轮、最多四个构建体，结局要靠产物化学（LC-MS/MS 判产物身份与量），且**至今没有一条被产物化学确认的天然 UAA 合成酶**，即没有任何结局标签。这篇的价值恰好在这个约束下才显出来：它不给阈值，它给的是**「哪一类读出值得押、哪一类只能作旁证」的可引用量级证据**。

### 8.1 该选作主读出：单一机制型（丰度/产物型）读出 —— 对应我们的「产物身份 + 定量」

- **证据**：本文最强的一条规律就是「读出只对应一件事时，物理分数与它最对得上」——"Realistically, we can expect that assays that evaluate phenotypes such as protein abundance or complex formation, should show the best agreement with stability predictions, as they are well suited to detect destabilizing loss‐of‐function molecular mechanisms"，实测亦如此："The trend clearly demonstrates that stability predictors best reflect functional scores from abundance‐based DMS datasets, both in the case of only the best methods, as well as for all predictors, while viral replication datasets show the worst agreement"；这类读出的定义是「能直接判定点突变是否通过降解导致功能丢失」："Abundance‐based assays represent experiments that make use of VAMP‐seq and other fluorescent‐tagging approaches that can quantify protein expression and stability in cells, being able to directly assess whether variants lead to a loss‐of‐function through degradation"（以及 "VAMP‐seq is another methodology, which interrogates the abundance of GFP‐fused variant proteins and thus also their stability"）。
- **我们的等价物（怎么用）**：一轮的四个名额全部押在**能直接把化学事件读出为产物分子**的那一类测定上——LC-MS/MS 判 S1（pppUA 之类中间体）与 S2（终产物）的**身份 + 量**，并同批测竞争副产物（S0 游离 UTP 起始路径与错误底物路径）。它是「丰度型读出」在酶学里的对应物：**一个数对应一个事件，低分可以归因到具体那一步**。
- **必须一起做的两件事（照抄这篇的两个教训）**：① **语境要齐**（否则重演结合类读出的失败）：作者发现低相关的原因是复合物里根本没有被测的配对体——"structures for HRAS (PDB IDs: 2CE2 and 6P0Z ) and PSD95 (PDB ID: 6QJL ) did not contain the binding partners relevant for the specific DMS assays, or were monomeric"。→ 我们的测定体系必须**含全部共底物与辅因子**（正确 tRNA、氨基酸/UTP、ATP、镁离子等）并能分离各产物；只测单一底物消耗 = 拿单体结构判界面。② **配失活/阴性对照**：本文能定位「是结构缺配对体而非方法不行」，靠的正是有可比的另一套语境；我们需要同轮放一个已知失活背景（催化残基突变体）作方向锚。

### 8.2 只能作旁证：多机制混合型读出（生长/富集/存活/展示分选）

- **证据**：混合型读出的定义就是「一把尺量所有机制」——"Growth experiments involve mutant competition or antibiotic survival and are able to characterize functional effects from multiple molecular mechanisms"；实测后果是排序不稳定："Competitive growth assays, which are a popular generalized approach, appear to show mixed agreement on a per‐gene level, but are not well correlated with changes to stability overall"；同一个 bla 靶换一套**同一大类**的抗性/生长实验（原文称 bla(d) 为 a different antibiotic resistance experiment），最好相关就从 0.66–0.68 掉到 0.44；最系统性的失效是机制不在失活轴上的那批靶："This is likely to contribute to the low correlations observed for CALM1, TARDBP and SRC datasets, which are known to also be associated with non‐loss‐of‐function disease mechanisms"。作者同时给出取舍的原话："although, the delineation of what molecular mechanism might be responsible for the increase or reduction in fitness is lost"。
- **我们的用法（降级，不作准入判据）**：酵母/大肠杆菌生长 rescue、展示库分选富集倍数、细胞存活、"表达可溶但不聚集"这类结果，在本篇的证据结构里都属于「混机制读出」：它们能**排除**一些解释（这个构建体整体没死、蛋白表达得出来），但**不能支持**「这一步化学事件发生了、且发生对了」。→ 允许写进记录的口径只有两条：(i) 作为**可行性/毒性排除**（阴性时有信息量：不表达/不长 → 无法判定催化）；(ii) 作为**旁证一致性检查**（与产物型结果同向时提高整体可信度，不同向时优先信产物型）。**禁止**把它们单独作为「候选有 UAA 活性」的证据进漏斗。
- **另一类必须降级为旁证的：只证明「折得对/稳得住」的结构性读出**（nanoDSF 的 Tm、SEC 单体率、pLDDT 类）。它们的机制对应物就是本文的丰度型读出——测的是降解/稳定性，不是催化。作者连丰度型都只肯说它「适合检测 destabilizing LOF」，从未说它能判功能位点：而本文自己也限定 "not all loss‐of‐function missense mutations will be due to protein destabilization: for example, they may impact functionally important sites or perturb protein allostery"。→ 结构性读出对我们同样只作旁证。

### 8.3 可迁移的做法（不需要借用任何数字）

1. **押归因、不押广度**（本篇的核心取舍）：一轮预算下选「一个数只对应一个化学事件」的读出；广覆盖的混合型读出留到以后。作者的对照句式可复用于我们的记录模板：每个读数注明「它低分能排除什么、高分能支持什么」，写不出来的读数不进主判据。
2. **主读出必须自带可比的第二语境**（配对体/失活背景）——这是 HRAS/PSD95 与 GAL4/BRCA1(a) 两组案例给我们的直接操作要求。
3. **无标签时用无训练共识分**：Foldetta = 单位对齐 + 算术平均就领先最好单工具 ~0.15 排名点（"combining complex‐based scores from the two tools produces a superior predictor, with the Foldetta_comp ensemble coming out ahead by ~0.15 points in the ranking"、"but demonstrates the utility of even simple untrained ensembling when combining the right inputs"）。→ 我们的两个物理来源不同的便宜判据（如几何类 + 能量类）可以先做**秩平均共识**再排序，不需要标签；但只许在同类物理来源之间做（本文只在经验势家族内部验证过）。
4. **覆盖不齐时用共同子集比较 + 按成功比较次数归一**（§2.4 的三招）：我们各判据对候选的覆盖度不一致（MD 只跑得起少量原子簇、xTB 只跑一维剖面），任何「判据 A 比 B 好」的比较必须限定在两者都有值的候选上并明说分母。
5. **相关量级写进先验**：判据 vs 湿实验结局的 Spearman 落在 0.2–0.4 是本领域的正常水平（0.26/0.25 两个外部锚），别把它当失败；同理别把 0.6+ 当能力，先问是不是挑了单一机制型读出。
6. **分组报告、不许报总平均**（这篇自己就是靠分组才翻出结论的）：我们的面板按 S0/S1/S2 × 读出类型 × 判据分层，各层单独出数，并保留一层「已知会全崩」的阴性层。
7. **把「上限」写进结论**：同基因两套实验只到 0.66、物理-实验比较实践上限 ~0.8 —— 引用我们的任何复现一致性时，应连同这两个尺度一起给，避免把「两个读数不一致」直接读成「其中一个是错的」。

### 8.4 不可迁移（为什么不能照搬）

1. **一个数字都不许搬**：0.26 / 0.66 / 0.15 / 0.61 / 0.53 / 2.94 全部是「错义变体效应排序」语境的量，标签是群体适应度或蛋白丰度；我们的结局是**多步化学事件 + 竞争副产物分支**，二值性与连续性与他们都不一样。特别是 Foldetta 的 ~0.15 排名点（投票排名单位，不是 rho）——**不得**换算成我们的判据增益或命中率。
2. **「丰度型读出最相关」不能被读成「表达量高就等于有活性」**：那正是本文反面教材的位置（结构温和但功能受损的机制一大把，见 §5.8(iii)）。DP2R 口径禁止把表达/稳定性一致当酶活闸口，本文也**只支持**「丰度型读出与稳定性类判据彼此最对得上」这一条窄结论，不支持任何催化主张。
3. **"Foldetta 超过所有 VEP" 是丰度子集上的结论，子集条数正文未给**（§7 我们读出第 3 条），引用这句话必须连这个边界一起说，否则就是把子集选择当成能力。
4. **本文没有 MD、没有 QM、没有酶、没有催化读出**（§3 工具箱末条），因此它**不能**为「用 MD/xTB 判催化是否可行/可靠」提供任何正面或负面证据；它能提供的只是「物理类分数与实验功能分的相关性典型量级」这一条外部参照。
5. **相关性口径 ≠ 闸口口径**（§7 我们读出第 5 条）：全文没有任何通过/淘汰阈值，所以这篇不能出现在我们的阈值表里，只能出现在「读出选择依据」与「判据审计口径」两处。
6. **他们能审计判据是因为有 49 套现成实验分**；我们一个都没有（一轮四个构建体 ≈ n 极小）。所以这篇的 **A 段式审计**（先有结局标签再评判据）我们暂时复制不了，只能借用它的**结论层**（押归因型读出、混合型降旁证、无标签用秩共识、共同子集比较）。
7. **cDNA display proteolysis 那条建议不可照搬**：作者自己限定它 "While limited to a stability phenotype" —— 只测稳定性表型，正是我们要避免的单一维度；对我们它至多是「旁证层」里最便宜的表达/稳定性选项，不是主读出。

### 一句话的可执行版

**主读出 = 能判产物身份与量、且体系含全部共底物 + 失活背景的那一个（把四个名额全押上去）；生长 rescue、展示富集、表达量/Tm/单体率这类混机制或纯结构型读数一律登记为旁证与排除性证据，不作准入判据；任何判据与湿实验读数的一致程度按 0.2–0.4 为先验正常区间，超过 0.6 先自查是不是只看了单一机制型读出。**

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K33_PMC10273344_text.txt

- **本卡逐字比对用的唯一底稿**：`data/literature_cards/fulltext/K33_PMC10273344_text.txt`（74,368 B，SHA-256 前缀 `891544b57dd80f4f`；Europe PMC fullTextXML 去标签纯文本，按核验器同一 `norm()` 归一后 73,865 字符，**全文单行、无换行符**）。同目录另有 XML 原件 `K33_PMC10273344_fullTextXML.xml`（159,507 B，SHA-256 前缀 `b12d98f239095640`），门禁显式排除 `.xml`，故不参与比对，仅作取回凭据。
- **为什么必须声明这一份**：同一篇可能有 Europe PMC 与 NCBI 两套抽取版本，句中夹的参考文献编号位置不同。本底稿的特征（实测统计）：含 **198 处 U+2010 HYPHEN**（abundance‐based、loss‐of‐function、VAMP‐seq、per‐gene、native‐like、DNA‐bound 这类词内部用的都不是普通连字符）、90 处 Δ、以及标签剥离留下的空格（如 "Table S3 ," 与 "(PDB IDs: 7JZV and 1JM7 )"）。本卡所有引句按这份底稿**逐字符复制**，含 U+2010 与这些空格；大小写也照底稿（例如 For example 起头那句在本卡保持小写 both）。跨句拼接一处未做：`the R "psych" ... "corrplot"` 那句因内部含直双引号，本卡改为中文转述不作引句；含 `|ΔΔG|` 的两条引句移出表格单独成行，避免 markdown 表格断列时被误改。
- **对照底稿**：`sources/cost-benchmarks.md:121-125`（§3.5）。该段已核过的三个数（0.26/0.28、Rosetta 0.25、同基因 0.66、Foldetta +0.15、预测器两两 0.49）与本卡一致；本卡相对底稿补齐的是：49/39/170,940 的规模口径、五类读出的原文定义与分组实测结论（Fig 5/6）、FoldX/Rosetta 具体极值（0.66–0.68 / 0.44 / 0.61 / 0.53 / 0.57）、复合物增益的正反两组 PDB 案例、全部协议参数（Rosetta 构建号与 Ref2015、3 次迭代、REU/2.94、RepairPDB、>90% 与 ≥50 残基映射门槛、AF2 取用于 2021-07-27）、以及投票排名的统计细则（两位小数、平局半分、按成功比较次数归一、二项/Fisher z 置信区间）。
- **CSV 字段映射**：本卡 §3 ↔ `计算筛选判据/候选生成方法/阈值数字`；§4 ↔ `候选数递减/实验命中率/成本/统计量引用`；§5–§6 ↔ `在方法演进链的位置`；§8 ↔ 这些数字的使用边界（不许跨域搬阈值、不许把相关系数当命中率）。CSV 原行 `是否用MD=否`、`是否用QM=否` 与本卡一致（并补限定：ENCoM 是正常模式分析，不是 MD）；原行 `候选生成方法=未记录`、`阈值数字=未记录` 本卡同样记为未记录（本文不生成候选、不设闸口阈值）。
- **未取到的部分（诚实边界）**：Table S1（49 个数据集与基因清单、逐数据集变体数与出处）、Table S3（逐数据集的读出分组归类）、Figure S1/S2（VEP 相关矩阵与含 VEP 的完整排名）、Figure 1/2/5/6 的逐格原始数值。因此本卡 §5.7 那句最强结论（Foldetta 在丰度子集上超过所有 VEP）与 §4 的分组趋势，属于**作者断言 + 底稿可查的文字**，其分母构成本卡无法自行复核；已在 §7 明示。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only K33 --no-report`（输入：本目录卡片 + `fulltext/` + `sources_map.json`；参数：`--only K33 --no-report`，不写 selfcheck.txt/rollout_status.tsv 以免覆盖并行代理产物）。门禁把卡内被直双引号包住、不含中日韩字符、≥20 字符且 ≥12 个字母的片段当作逐字引句，在声明底稿里逐字查找，任一条不命中即 FAIL、退出码 1。**本轮结果：PASS K33 quotes=138/138，退出码 0**（卡内 138 次逐字引句出现，去重后 **100 条**不同引句）。写卡之前先用同一 `norm()` 对 51 + 49 共 100 个**候选**片段做过预核验（临时脚本放在 `A:\AITEMP`，交付后删除），其中 2 条因**句首大小写**不符被当场拒（For example 起头那句被我误写成大写 Both / This），说明这道门是逐字符工作、不是近似匹配；另有 1 条是我在正文里手工重打时把 U+2010 打成了 ASCII 连字符，第一次跑门禁即 FAIL（1 条未命中），按底稿字符改正后复跑转绿。
- **反向自测（证明这道门真能判红，本会话实测，只在内存里改字符串、不写任何生产文件）**：对本卡三条真引句各做单点扰动，扰动后全部不再命中底稿——① 把 0.26 and 0.28 那句里的 `0.26` 改成 `0.27` ⇒ 不命中；② 把 both FoldX and Rosetta showed… 的句首 `both` 改成 `Both` ⇒ 不命中；③ 把 VAMP-seq is another methodology… 里所有 U+2010 换成 ASCII 连字符 ⇒ 不命中。原句三条均命中。也就是说「引用造假或抄错一个字符会被机器抓到」是可执行的结论，不是声明。

<!--CSV回填
work_type=benchmark（回顾性相关性基准：只重算已发表 DMS 数据与既有预测器的分数；无新湿实验、无蛋白设计、无前瞻验证）
target=39 个唯一蛋白靶 / 49 个 DMS 数据集 / 170,940 个单点错义变体（人源为主，含酵母、细菌与病毒蛋白；正文点名体系：bla 抗生素抗性、GAL4 双杂交+DNA、BRCA1(a) BRCA1-BARD1、UBI4(b) FACS、NUDT15、PTEN(a)、TPMT、CYPC9(a)、CALM1、TARDBP、SRC、P53、PSD95、HRAS、KCNQ4 膜片钳、HSP82、PAB1）
backbone_generation=未记录（本文不生成任何新骨架或新序列候选；只做变体→结构映射：PDB 首生物组装体优先，跨物种链需与人蛋白 >90% 一致且比对区 ≥50 残基，映射不到者用 AlphaFold2 模型（2021-07-27 取用））
computational_filters=9 个结构基稳定性预测器 FoldX 5.0、Rosetta Cartesian ΔΔG（Ref2015）、ENCoM（正常模式分析）、DDGun3D、INPS3D、mCSM、DynaMut2、PoPMuSiC、RaSP；FoldX/Rosetta/ENCoM 另跑复合物（含 DNA）输入；对照侧 7 个 VEP BLOSUM62、Grantham、SIFT、PROVEAN、SNAP2、DeepSequence、EVcouplings；提出的共识分 Foldetta=FoldX 与换算后 Rosetta 的均值；评价指标只有 Spearman rho + 成对投票排名（平局各半分、按成功比较次数归一、二项 95% CI）+ Fisher z 误差棒
thresholds=全文没有通过/淘汰型闸口阈值（本文是相关性基准）；可复现的协议参数：跨物种映射 >90% 序列一致且 ≥50 残基、Rosetta REU→kcal/mol 除以 2.94、Rosetta 3 次迭代取平均、相关值四舍五入到两位小数后才比较、平局各记半分、排名得分除以成功比较次数、FoldX 先 RepairPDB、结构优先级=分辨率最优后取最大生物组装体、NMR 取第一帧、丰度子集可视化时两列分数秩归一到 0-1 并剔除方向相反变异
md_used=否（全文无分子动力学；ENCoM 用的是正则模态/正常模式分析，不是轨迹采样）
qm_used=否（全文不含量子化学计算）
experimental_methods=无湿实验；全部复用已发表 DMS/MAVE 读出并按表型归五组：酵母内人基因互补的竞争性生长适应度（最常见）、VAMP-seq 与其他荧光法测蛋白丰度、毒性测定、双杂交/噬菌体展示的结合强度、靶专用活性测定（KCNQ4 膜片钳电流等）、病毒复制测定；数据源为前两轮 VEP 基准 + MaveDB；数据仓库 doi 10.17605/OSF.IO/ZTV8A
pipeline_counts=49 个 DMS 数据集 / 39 个靶 / 170,940 个变体 → 9 个稳定性预测器（FoldX、Rosetta、ENCoM 各再跑复合物口径）→ 逐（预测器 × 数据集）Spearman → 成对投票排名（含 Foldetta 与 VEP 两轮扩展）→ 按 5 类读出分组重算 → 只取丰度型子集重排；逐数据集变体数与每组数据集条数正文未给（Table S1/S3 未取回）
hit_rate=不适用（本文不测命中率）；替代口径为相关系数：稳定性分与 DMS 功能分平均 rho 0.26（ΔΔG）/0.28（绝对值口径）；FoldX 与 Rosetta 最高，在 bla(a)/bla(b) 达 0.66-0.68，同一靶换 bla(d) 仅 0.44；UBI4(b) 0.61；其余基因最高 0.53；NUDT15 文献案例 0.57；VEP 平均 0.36（剔除替换矩阵 0.42）高于稳定性分；Foldetta_comp 在投票排名上领先最好单工具约 0.15 点，且只在丰度型子集上超过全部 VEP
best_metric=未记录（本文无 Kd 或催化活性值；最接近最好成绩的是判据-实验相关上限类数字：FoldX/Rosetta 对 bla(a)/bla(b) 的 Spearman 0.66-0.68，同基因两套 DMS 彼此平均只到 0.66，物理-实验比较的实践上限约 0.8）
cost_or_stat_note=预测器两两平均绝对 rho 0.49（剔除 ENCoM 后 0.60）；ENCoM 与任何其他工具最高仅 0.23（对 DDGun3D）；DDGun3D-INPS3D 0.76、RaSP-Rosetta 0.75（后者因 RaSP 用 Rosetta 输出训练）；ENCoM 改用绝对值口径 rho 最多提升 0.36；外部同口径锚点 Høie 等 Rosetta 对 DMS 平均 0.25；直接实验热稳定性与预测仅约 0.5、实践上限约 0.8；计算成本本文未报（全部工具为秒-分钟级打分器）
role_in_timeline=关键否定性定量证据（口径对照）：第一，不要用单一 ΔΔG 阈值当准入判据——物理分与实验功能分的相关平均只有 0.26；第二，相关性高低主要由读出类型决定而非算法决定，丰度/降解型最高、病毒复制型最低、竞争性生长型逐基因漂移，故同一表观分在不同测定里不可互换；第三，无训练简单共识（Foldetta）即可追平专用 VEP，给无结局标签的场景一条可抄路径；第四，为「只有一轮湿实验该选哪种读出」提供直接依据：押单一机制型（产物身份/定量）读出，把混机制型（生长 rescue、展示富集、表达量/Tm）降为旁证与排除性证据
source_pointer=data/literature_cards/fulltext/K33_PMC10273344_text.txt（SHA 891544b57dd80f4f…，本卡引句底稿）+ K33_PMC10273344_fullTextXML.xml（SHA b12d98f239095640…）；sources/cost-benchmarks.md:121-125（§3.5）；DOI 10.1002/pro.4688；数据 https://www.doi.org/10.17605/OSF.IO/ZTV8A
CSV回填-->
