# [B07] FoldArchitect：把"选一个 fold、扫它所有形状"做成可并行流水线——3 万设计 / 6 千稳定 / 一个跨 fold 稳定性分类器

Linsky T, Noble K, Tobin A, Crow R, Carter L, Urbauer J, Baker D, Strauch E（UW-IPD / U Georgia / OSU）
Nature Communications 2022, 13:7151 · DOI 10.1038/s41467-022-34937-8 · PMID 36418330 · PMCID PMC9684540
开放获取（CC BY 4.0，期刊版）· 全文链接 https://pmc.ncbi.nlm.nih.gov/articles/PMC9684540/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B07**（组：Baker组） |
| 本文取回方式 | Europe PMC `fullTextXML`（PMC9684540，Nature Communications 期刊版），2026-10-16 本地抓取 |
| 本地全文 | `data/interim/baker_lit/ft/smallfolds2022.txt`（67,537 B；标签剥离后 66,886 字符） |
| 对照底稿 | `sources/baker.md` 第 94–105 行（原卡）、`sources/baker.md:640`（30,000→6,200 的漏斗对照行） |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中；见第 9 节自检） |
| 未取到的部分 | Supplementary Methods/figures/tables（含全部打分项清单 "All score terms for filtering and evaluating designs are summarized in the SI"、fold-description XML、Supplementary Fig 8/9 的稳定性分数分布）。本卡凡涉及**具体筛除打分项与阈值**的地方一律标"正文未给/在 SI"；fold 级成功率的逐 fold 数字在图（Fig 2d/e）里，正文只给相对高低 |

## 1. 这篇到底解决什么（大白话）

在此之前，Rosetta 的骨架设计是"蓝图（blueprint）驱动"的：一个 fold 一个固定的 ABEGO 序列文件，想改一根螺旋的长度、挪一下 strand 的 register、加一个 bulge，就得**重画蓝图 + 专家重排折叠轨迹**。这篇把"蓝图"换成"fold 级的参数化描述"（XML）：**在折叠轨迹里面动态改变**二级结构长度、loop 类型、register shift、bulge、距离约束，一段一段把整条链拼起来；然后利用当时已有的湿实验能力（一条寡核苷酸装一个基因、酵母表面展示 + 蛋白酶消化 + FACS + NGS）**把两万个设计一次性测稳定**。产出三件东西：① 8 种 fold（含两种自然界没有的 F2/F4）的形状多样性数据集；② 从中提炼的折叠规则（螺旋-螺旋 loop 连接规则、strand-helix-strand 的右手性几何限制），并**把规则回灌进设计平台**；③ 一个跨 fold 训练的 Random Forest 稳定性预测器（110 个特征，在别人的数据集上 AUC ~0.83）。它是"纯 Rosetta 物理打分 + 展示库通量"这条路线的量化锚点：**约 3 万个设计 → 约 6,200 个稳定蛋白（~21%）**。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **旧蓝图基础设施不能规模化，也不能采样形状**。原文诊断："This approach is computationally intensive and has limited scalability for larger proteins because determining the ABEGO sequence needed to fold a viable backbone requires expert intervention and multiple manually defined steps."，并且"Sampling the shape space using these methods is challenging because variations within any secondary structure lengths or loop connections require a new trajectory and blueprint file, and often require concerted and context-dependent changes to multiple secondary structures"。
   **应对**：把 fold 描述参数化（XML）+ 轨迹内动态改参——"We addressed these limitations by creating a definition for a fold with parameters that can be altered during a trajectory"，并让非程序员也能改："The RosettaScripts XML scheme allows modification of the design strategy without programming knowledge."
   **留下的代价**：仍然靠 PDB 片段插入折叠，作者明写长度可扩展性差（见第 3 条）；且**设计的形状空间被上游的合成/展示能力框住**（见第 2 条），不是完全自由的采样。
2. **湿实验侧的长度上限反过来决定了能设计什么**。作者直接把射程写清："For a 230 nt oligomer, the maximum length is ~64 amino acids, given that the end parts of the DNA fragments are used for homologous recombination into the yeast surface vector. This roughly allows up to about six independent secondary structure elements (meaning sheet or helix) per fold with loop connectors and their variations"。
   **应对**：不是想办法突破，而是**按实验预算挑题**——8 种 fold 全在小尺寸区间（3H/4H/coil/beta-grasp/ferredoxin/thioredoxin/F2/F4）。
   **留下的代价**：这条上限使本文结论只覆盖"小蛋白"，作者自己把它列为前提而非结果；对更大 fold 的规则是否成立，本文没有数据。
3. **de novo 从伸展链折叠的算法随长度急剧变差**，作者给了具体失败机理："One complication with the de novo extended chain folding of backbones is that it scales poorly with length; a single missing hydrogen bond in a backbone can lead to incorrect secondary structure and failure of filters."，并量化："a complete 40-50 amino acid long miniprotein fold might require thousands of trajectories from an extended chain to find one that is correctly folded"。
   **应对**：分治 + 扰动器——"we developed an algorithm (DivideAndConqueror) that identifies subsegments of a full-length backbone that can be folded individually and generates a strategy to build the backbone incrementally, piece-by-piece"；失败时不是重跑同一件事，而是让 Perturber 换参数："if the model fails the filters, the Perturber instructs the architects to permute the parameters of the subsegment (e.g. secondary structure lengths, register shift, phi and psi angles, loop connectivity) and another folding attempt is made"。
   **留下的代价**：作者承认以前这活儿靠人："This has been addressed in previous work with single folds through extensive intervention by an expert."；本文把专家经验搬进代码，但**每 fold 仍要人工调距离约束默认值**（8 Å 起步，beta-grasp 改到 9 Å）。
4. **稳定性读数本身可能是假阳性——单蛋白酶不够**。最典型的案例是他们故意留的对照 ThioFL24："It showed a high trypsin stability score, but a negative score for chymotrypsin, indicating it should be unfolded."
   **应对**：① **双蛋白酶并行**（trypsin 与 chymotrypsin 各自 5 档浓度），结论句写得毫不含糊："This demonstrates that using two proteases is essential for this high-throughput screen."；② 用约 2300 条随机序列定"稳定性阈值"；③ 加内参阶梯："This ladder allows adjustment for the activity of each enzyme batch."；④ 多做筛选轮次与重复："Additional selections and duplicates were also performed compared to the previously published method to improve accuracy"。
   **留下的代价**：EC50 是**抗蛋白酶性**，不是折叠自由能；作者只引用前人的相关关系（"A direct correlation between the EC50 values of digested protein variants with their free energy was previously established"）来代理，本文没有重新标定这条代理关系；稳定性分数 >0.5 这个"成功线"沿用了前人方法口径。
5. **设计的 fold 在溶液里做成二聚/交换二聚体，与设计态不符**（这是本文"没解决"的一块）。现象："While all-alpha-helical folds were dominantly monomeric, more dimer and aggregate formation was observed for folds containing beta-strands."、"All F2 and F4 designs characterized appeared to be largely in a dimeric conformation with only little of the protein found in the monomer fraction"，并且"Dimeric and monomeric fractions are not in equilibrium as they remain in the same state even after several days"。
   **应对**：① 不假装成功，改测优势态——"Because the monomeric version of F4M_256 was misfolded, we examined its dominant dimer fraction."；② 给出机制猜想并指出设计方法的盲区："This suggests a mechanism at work that is not captured by our design method; it is possible that the lack of interconnectedness in these folds enables the fold to become a swapped dimer."；③ 提出修正方向但**不在本文执行**："Folds that have a direct linear connectivity of their secondary structure elements, such as F2 and F4, may require further optimization through disulfide connections or, perhaps, negative design that discriminates against a swapped dimeric conformation."；④ 对无法解释的部分明写"Further investigation would be needed to prove these assumptions."
   **留下的代价**：**寡聚态不是设计出来的**；作者的兜底说法是"Although the oligomeric state was not as designed, our pipeline was readily able to produce models for these folds that are stable against proteolysis and are folded."——即"稳定且有结构"，但**不是设计的对象本身**。这对任何想借用这批 scaffold 做结合蛋白的人是硬约束。
6. **极小 ferredoxin 之前做不出来**。"Previous attempts to design very small versions of the ferredoxin fold have failed, resulting in unfolded proteins"。
   **应对**：穷举二级结构长度与 register："We extensively sampled secondary structure lengths and registers for the ferredoxin fold and found that there are indeed geometric limitations"，并把原因归到右手性 motif（"likely due to the inherent requirement of right-handed strand-helix-strand motifs"），最终"我们做出了小至 55 个氨基酸的稳定变体"。
   **留下的代价**：几何限制是**事后发现的边界**，不是一个可预测的判据——本文没有给出"多大的 ferredoxin 一定折不出来"的定量规则。
7. **AF2 单序列预测能不能当预筛子？作者试过但不敢用**。实测："The topologies of all folds were predicted as modeled"（正文给偏差区间 0.4–3 Å），但"except for Thio_330 and bG-518.1"，且错法很有教学意义："For the thioredoxin, the last beta-strand was predicted to be part of the previous helix, whereas the beta grasp fold was predicted to have a strand swap of the last two strands."
   **应对（其实是"不应对"）**：只把 AF2 当**描述性核对**，明确拒绝把它的参数当筛子——"However, parameters for this should be carefully assessed in more detail and experimentally validated to identify ideal thresholds." **本文未解决**：他们提出了"可以用 AF2 预选"的可能性，但没有给出阈值，也没有回测命中率。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **骨架生成（本文主角）**：自研 **FoldArchitect（FoldArchitectMover）**，跑在 RosettaScripts 里，四个可插拔模块：`Architect`（把 fold 描述变成逐残基指令）、`PoseFolder`（按指令做片段插入折叠）、`Filter`（任意 Rosetta filter 判该段是否折对）、`Perturber`（没过 filter 就改参数重来）。**为什么选它**：作者认为只有物理方法能系统扫形状——"Rosetta-based computational methods for de novo design of monomeric proteins can systematically sample this space"，而生成式/ML 方法"are not designed to systematically probe the shape space of a given fold in a controlled manner"。
- **回灌的折叠规则**：来自 ferredoxin 设计的既有规则 + 本文新识别的**螺旋-螺旋 loop 连接规则**；loop 构象不是穷举而是"只采样以前发现的连接类型"。
- **序列设计**：两条 Rosetta 协议——① 按溶剂可及性选氨基酸子集采样 rotamer，从低排斥项起、逐步加大排斥（先找好相互作用、再解 clash）；② **pair-motifs** 先铺核心再走①，既省算力又提高 3H 成功率。
- **实验通量**：酵母表面展示 + **蛋白酶滴度（trypsin/chymotrypsin 各 5 档）+ FACS + NGS**，用概率模型拟合每序列 EC50 并折算 stability score；negative control = 随机序列池；内参 = 5 条已知稳定性跨度的蛋白（ladder）。
- **单点验证**：E. coli 表达 + SEC/SEC 单体峰 + CD（25/95 °C 与回冷、熔解曲线）+ PDBMD2CD 预测谱比对 + 1H NMR（4 条）+ 热稳定性（8 条）+ ColabFold 单序列预测 + 同位素标记 NMR 解结构（ThioM_802）。
- **机器学习**：Random Forest（110 个序列/结构特征，500 棵树，fivefold CV + bootstrap/OOB），并做 **leave-one-fold-out** 的抗偏置验证。
- **没有用的方法**：MD、QM；正文里 MD 这个词只在参考文献 16 的标题里出现（PDBMD2CD，CD 谱预测工具，工具名含 MD-generated），不是本文的筛选环节。AF2 也未被用作筛子（见第 2 节第 7 条）。

### A. 计算侧：从 fold 描述到下单清单

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 用户 fold 描述（XML：SS 长度范围、loop 长度范围、约束施加方式、register shift、bulge） | FoldArchitect 读入并把 fold 切成**段**（两个二级结构元素 + 一个 loop 连接），逐段折叠并验证 | "the FoldArchitect reads a fold definition and divides the fold into segments (two secondary structure elements with a loop connector) that are folded and validated incrementally." | 8 种 fold：3H、4H、coil、beta-grasp、ferredoxin、thioredoxin、以及自然界没有的 F2、F4 |
| A2 | 每段 | 用 PDB 里按 ABEGO 序列挑出的结构化片段，插入 poly-valine 伸展链中折叠；轨迹内动态变 SS 长度与 loop 类型 | 由 Filter 判（**具体 filter 清单与打分项在 SI**）；正文只给了两类硬性检查：主链 omega/rama 角"Backbone constructs representing the complete fold were stringently filtered for the omega and rama angles before designing their sequence." | 同一 fold 得到一批多样骨架（"This results in a diverse set of backbones for a given fold"） |
| A3 | 整链折叠难（长度相关） | DivideAndConqueror 找出**可独立折叠且含完整配对**的最小子段，增量拼装 | 过 filter 就"锁住这段继续下一段"；不过就换参数 | 例：ββαβ 先折 ββ（含配对），再加 α（含与已折链的配对），最后 β |
| A4 | β-链类 fold | 加**松弛距离约束**偏置出"成形的 sheet"；BetaSheetArchitect 自动生成相邻 strand 配对并允许指定平行/反平行 | 约束函数："Distance constraints were coupled to a simple harmonic or a bounded harmonic function with a loose standard deviation of"（正文此处数值为 2 Å）；默认跨距"After measuring distances between helices and sheets of a few example beta-grasps and ferredoxin folds, we chose 8"（正文此处为 8 Å）"as the default starting value for sheet and helix distances" | 需按 fold 微调："Adjustments were made depending on the output for a given fold and distances were increased or decreased."；beta-grasp 中一处改成 9 Å（正文原句含 "was adjusted to 9"） |
| A5 | 螺旋 | Helix "kink" filter 限制弯曲 | "This filter monitors the curvature of helices and allows to restrict them."（正文给出的口径：仅允许 **less than 15°** 的弯曲） | 弯曲超限的骨架被拒 |
| A6 | sheet 合法性 | BetaSheetArchitect 只建"合法 sheet" | "The architect will only attempt to build valid sheets, those where the fully built sheet has no unpaired residues." | 剔除悬空 strand 的骨架 |
| A7 | loop 连接 | 不穷举所有 loop，只采样以前发现的 αβ/βα/ββ 连接类型，并加入本文新得的**螺旋-螺旋连接规则** | "In addition, our study identified rules for the connection of helical elements, which we also incorporated."，且"connections as previously discovered were sampled"；可扩展："As more principles are identified, they can be readily added." | 规则回灌进平台，后续设计步可直接调用 |
| A8 | 通过折叠的骨架 | 两路序列设计：① 按溶剂暴露选氨基酸集 + 递增排斥项；② pair-motif 先铺核心后走① | ②的动机与效果："this also reduced the compute time for the sequence design steps"、"Further, it substantially improved the rate of successful designs for 3-helical bundles"；①的机理句："As this scoring term increases, clashes are relieved while the strongest interactions typically remain intact." | 每个 fold 得到一批"骨架+序列"设计体（作者定位："Each design has a unique three-dimensional conformation and a unique sequence predicted to be near-optimal for that conformation"） |
| A9 | 全部设计体 | 按 filter 项 + 计算能量选设计（送测集合的选取） | **正文未给阈值**（原文："We selected designs for each topology and sequence design protocol based on a set of filter terms and their computed energies"，并指向 Methods/SI："All score terms for filtering and evaluating designs are summarized in the SI."） | "For each fold, 2000-12,000 finished design models were generated and scored."；总规模约 30,000（摘要口径）→ 实验测得 31,500 条序列（含随机对照） |

### B. 实验侧：一次性把两万个设计测完

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 选中的设计序列 | DNAworks2.0 按 ecoli2 密码子反译成 DNA；向 Agilent 下单**单池寡核苷酸** | 长度约束：基因 <230 bp 需补扩增序列（正文："For genes shorter than 230 base pairs, additional amplification sequences were added as previously reported"） | "Oligo libraries encoding designs and control sequences were purchased from Agilent Technologies as part of a 27,000-oligonucleotide pool." |
| B2 | 寡核苷酸池 | qPCR 扩增（刻意**欠扩增**）→ 胶回收 → 再 qPCR 扩增到够量 | "Amplification was performed using a qPCR (BioRad) to avoid overamplification. The number of cycles was chosen based on a test qPCR run to terminate the reaction at 50% maximum yield." | 得到可转化的插入片段 |
| B3 | 插入片段 + pETCON3 | 同源重组进酵母 EBY100（线性化载体 NdeI/XhoI 切） | 投料 1–2 µg insert + 1 µg 线性化载体；两侧各 40 bp 同源臂："The amplified libraries included 40 bp segments on either end to enable homologous recombination with the pETCON vector." | 展示文库（含约 2300 条随机序列负对照） |
| B4 | 展示文库 | 30 °C SGCAA 诱导 16–18 h；细胞归一到 O.D. 1（12–15 Mio cells），消化时 O.D. 2；trypsin 用 PBS、chymotrypsin 用 TBS+CaCl₂；**每管一档蛋白酶浓度**，5 min 后用 1% BSA 冷缓冲淬灭；抗 c-Myc-FITC 标记 | **五档浓度**："The library was assayed at five protease concentrations over sequential selection rounds"（正文数值：trypsin 0.07/0.21/0.64/1.93/5.78 µM；chymotrypsin 0.08/0.25/0.74/2.22/6.67 µM）；未切才有荧光："Unfolded proteins are cleaved and, thereby, will not be fluorescently labeled." | 每档得到"未切"细胞群 |
| B5 | 标记后的细胞 | FACS（Sony SH800，Ultra Purity 设置）：FSC/SSC 圈主群 → FSC-W/H 分单个与分裂细胞 → 单维荧光门；**每天按当次条件微调门** | "Small adjustments were made to this gate based on daily conditions to maximize the separation between the major displaying and non-displaying populations."；每个条件约 10 million cells；并记录**消化前过阈比例**用于归一 | 分选池（每蛋白酶 × 每浓度） |
| B6 | 各池 | 提质粒（Exo1 + Lambda 外切酶处理）→ 加 Illumina 接头与 6 bp 池特异 barcode → 混池上机（NextSeq）；reads 用 PEAR 配对 | 计数三条硬规则："Reads were considered counts for a particular ordered sequence if the read"（后接 (1)(2)(3)）——即上游必须含完整 NdeI 位点、下游含完整 XhoI 位点、且翻译后与订购序列逐氨基酸一致 | 每池每序列的 counts |
| B7 | counts 矩阵 | 沿用前人概率模型拟合 EC50（不改动代码，直接取仓库脚本） | "It assumes that proteolysis (i.e., any cleavage that results in detachment of the epitope tag) follows pseudo-first-order kinetics, with a rate constant specific to each sequence."；"Scripts were used precisely as previously reported without modification" | "Using the counts obtained through sequencing, we fit EC50 values for over 31,180 sequences (including control sequences) for both proteases and calculated a stability score for each" |
| B8 | 全部 EC50 | 定"稳定"线并做 fold 间比较 | 成功口径（Fig 2 图注）："The number of designs from each fold with indicated stability score or higher was used to compute" the per-fold success rate，正文用的分档线是 **stability score > 0.5**；随机序列池定阈值，5 蛋白 ladder 校酶批 | 摘要口径结果："We designed and evaluated stability of about 30,000 de novo protein designs of eight different folds."，"Among these designs, about 6,200 stable proteins were identified"（≈21%） |
| B9 | 各 fold 相对表现 | 按 fold 读成功率差异并给解释 | 定性结论："Three helical bundles generally showed the highest success rate; this is consistent with the previous report"；最低的是"thioredoxin and the super helical-coiled four helical bundles (coil) had the lowest."；机理猜测"For the 4H and coil designs, it is possible that fewer secondary structure contacts, a smaller core, and an additional loop compared to the 3H designs may decrease the margin for error." | 逐 fold 数值在 Fig 2d/e（本地全文无表） |
| B10 | 形状多样性 | 对稳定 vs 不稳定设计比较 SS 间距离、register shift、外周 strand 二面角（sheet 曲率）、相邻 SS 二面角、螺旋间距、螺旋夹角（给定 loop 的 phi/psi） | 无阈值；这是**描述性对照**："We compared distances between secondary structure elements, register shifts, dihedral of the outer beta-strands to describe the curva"（后半接 ture of the sheets …） | 结论：每个 fold 都有局部可塑性，验证已有规则并**导出新规则**（Fig 2、Supplementary Figs 14–18） |
| B11 | 抽 21 条代表设计 | 逐个表达纯化验证高通量读数（不是重新筛选，是抽查校准） | "We randomly picked 21 designs with different topologies and stability scores for detailed characterization"；"Of these, 19 proteins expressed in E. coli which were then analyzed via size exclusion chromatography (SEC) to monitor the presence of aggregate, dimer, or monomeric conformations." | 二级结构："we measured their circular dichroism (CD) spectra to assess their secondary structure formation and found all but two folded"；与 PDBMD2CD 预测谱比对"we found that 15/19 were similar to the predictions, despite the limitations of these type of predictions"；例外："The exceptions were bGM_166, bGM_649.2, and F4M_256, which are likely misfolded, and ThioFL24, which we expected to be unfolded due to its low stability score" |
| B12 | B11 的样品 | 1H NMR 判"有没有真三级结构"；CD 熔解判热稳；ColabFold 单序列预测核对拓扑 | NMR 覆盖 4 条设计；热稳覆盖 8 条；AF2 偏差区间 0.4–3 Å | "The topologies of all folds were predicted as modeled"，"except for Thio_330 and bG-518.1"；对 AF2 作筛子的态度见第 2 节第 7 条 |
| B13 | 最小化 thioredoxin 设计 ThioM_802 | 13C/15N 标记 + 全套三共振/NOESY 指派，CYANA 定距离约束、TALOS-N 给二面角约束、CNS 模拟退火出 100 个初始结构，**取能量最低 20 个作最终系综** | 与设计模型的一致性：top structure RMSD 1.9 Å（C-alpha），β-链部分 1.1 Å | "The NMR ensemble agrees with the designed model with the top structure having an RMSD of 1.9"（此处接 Å，based on C-alpha atoms）"compared to the model; deviations are mostly from the last helix."，结论"making this the first accurately de novo designed thioredoxin fold"（PDB 7LDF，BMRB 30844） |

### C. 数据回流：稳定性分类器

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | 稳定/不稳定标签（31,180+ 条）× 8 fold | 提 110 个序列与结构特征，其中新加**残基相互作用网络与枢纽残基能量贡献**类特征 | 训练用 fivefold 交叉验证；Random Forest，500 棵树，gini 判据，允许 bootstrap 并以 out-of-bag 估计泛化精度 | "Compared to previously described physical and statistical features for stability, we evaluated additional features describing residue interaction networks and energetic contributions of individual amino acids within tightly connected hubs of residues, resulting in a total of 110 sequence- and structure-based features." |
| C2 | 同上 | 找最有信息量的特征 | 排序结论 | 新特征里最强的是最连接残基的整体能量贡献；总体上"As previously seen"（后接引文编号）"correct local geometry as measured through alignment with short structural fragments"（后接 Supplementary 编号）是第一位预测量，"followed by the number of hydrophobic residues within the protein core" |
| C3 | 8 个 fold | **留一 fold 验证**（一次藏一个 fold，用其余 fold 训练后预测被藏的 fold） | 目的写在图注："To avoid potential bias, we compared the ROC of predicting stabilities for any protein within the whole set vs. a ROC of the different folds or all combined (mix) after training on the other folds within the set." | 能预测未见过的 fold（Fig 5c、Supplementary Figs 21–23） |
| C4 | Rocklin 等前人的小 fold 数据 | 外部集回测 | 指标 AUC | "and observed a predictive power of an AUC of around 0.83 using our single classifier" |
| C5 | 与前作的差别 | 一句话定位 | — | "Unlike previous studies, by using our larger and more diverse fold data set and descriptive features, we were able to train a model on multiple folds, instead of one fold at a time"（后接引文编号） |

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| ~30,000 → ~6,200（≈21%） | 8 种 fold 的设计数 → 实验判定稳定蛋白数 | "We designed and evaluated stability of about 30,000 de novo protein designs of eight different folds." |
| 31,500 / ~2300 | 实际表征的序列数 / 随机序列负对照数 | "We experimentally characterized 31,500 sequences reflecting these eight folds using yeast surface display, including about 2300 randomized sequences as negative controls." |
| 31,180 | 拟合出 EC50 并算稳定性分的序列数（含对照） | "Using the counts obtained through sequencing, we fit EC50 values for over 31,180 sequences (including control sequences) for both proteases and calculated a stability score for each" |
| 2000–12,000 | 每个 fold 生成并打分的完成设计模型数 | "For each fold, 2000-12,000 finished design models were generated and scored."（原文为 2000–12,000） |
| stability score > 0.5 | 本文"成功"的口径（按 fold 算成功率的分数线） | "The number of designs from each fold with indicated stability score or higher was used to compute"（Fig 2d 图注；正文用 >0.5 分档） |
| 230 nt / ~64 aa / 约 6 个 SS 元素 | 单条寡核苷酸决定的设计尺寸上限 | "For a 230 nt oligomer, the maximum length is ~64 amino acids, given that the end parts of the DNA fragments are used for homologous recombination into the yeast surface vector." |
| 27,000 | 下单的寡核苷酸池规模 | "as part of a 27,000-oligonucleotide pool" |
| 50% maximum yield | qPCR 循环数截止（防过扩增） | "The number of cycles was chosen based on a test qPCR run to terminate the reaction at 50% maximum yield." |
| 40 bp | 与 pETCON 重组的同源臂长度 | "The amplified libraries included 40 bp segments on either end to enable homologous recombination with the pETCON vector." |
| 5 档蛋白酶浓度 | trypsin 与 chymotrypsin 各做 5 个浓度 | "The library was assayed at five protease concentrations over sequential selection rounds" |
| 10 million cells / 条件 | 每个浓度分选的细胞量 | "Generally, about 10 million cells were sorted for each protease concentration including the control." |
| 5 条 ladder 蛋白 | 校正酶批活性的内参 | "we added five proteins"（Fig 2c）"spanning a wide range of previously measured stability scores"；"This ladder allows adjustment for the activity of each enzyme batch." |
| 21 → 19 → all but two / 15/19 | 抽查设计数 → E. coli 表达数 → CD 折叠数 → 与预测 CD 谱相符数 | "We randomly picked 21 designs with different topologies and stability scores for detailed characterization" |
| 0.4–3 Å | ColabFold 单序列预测与设计模型的拓扑偏差区间（两个例外：Thio_330、bG-518.1） | "The topologies of all folds were predicted as modeled"（正文此处写 within 0.4–3 Å），"except for Thio_330 and bG-518.1" |
| 1.9 Å / 1.1 Å | ThioM_802 的 NMR 系综 vs 设计模型（C-alpha；仅 β-链部分） | "The NMR ensemble agrees with the designed model with the top structure having an RMSD of 1.9" |
| 110 / 500 / fivefold | Random Forest 特征数 / 树数 / 交叉验证折数 | "resulting in a total of 110 sequence- and structure-based features." |
| AUC ≈ 0.83 | 单个分类器在 Rocklin 等外部小 fold 集上的预测力 | "and observed a predictive power of an AUC of around 0.83 using our single classifier" |
| 2 Å / 8 Å / 9 Å / <15° | 距离约束的标准差 / sheet-与-helix 距离默认值 / beta-grasp 的调值 / 螺旋弯曲上限 | "Distance constraints were coupled to a simple harmonic or a bounded harmonic function with a loose standard deviation of"（数值 2 Å） |
| 55 aa | 做出来且稳定的小 ferredoxin 变体长度下限 | "We were able to design small and stable variations of this fold as small as 55 amino acids in length" |
| 40–50 aa / thousands of trajectories | 从伸展链折叠一个 mini 蛋白需要的轨迹量级 | "a complete 40-50 amino acid long miniprotein fold might require thousands of trajectories from an extended chain to find one that is correctly folded" |
| 100 → 20 | CNS 模拟退火产生 100 个初始结构，取能量最低 20 个为最终系综 | "These structural restraints were used to calculate a set of 100 initial structures starting from an extended structure" |
| PDB 7LDF / BMRB 30844 | 最小化 thioredoxin 的溶液结构与化学位移存档 | "Chemical shifts, structural restraints, and atomic coordinates have been deposited in the BMRB (entry 30844) and the PDB (PDB ID 7LDF)." |

## 5. 结论——作者说了什么

1. 平台成立："we developed and experimentally validated a computational platform that can design a wide variety of small protein folds while sampling shape diversity"，并且"Nature only samples a small fraction of the sequence space that can fold into stable proteins."（→ 主动采样形状空间是有价值的事）。
2. 数量与规则：约 30,000 设计得到约 6,200 个稳定蛋白；"Obtained data revealed protein folding rules for structural features such as helix-connecting loops."；新规则被写回算法："We also extracted additional rules for protein design, such as loop connectors for helical elements, which we in turn incorporated into the design algorithm and can be readily accessed in any Rosetta design step."
3. 里程碑式的一个 fold："Among these designs, about 6,200 stable proteins were identified, including some predicted to have a first-of-its-kind minimalized thioredoxin fold."，并以 NMR 结构坐实："making this the first accurately de novo designed thioredoxin fold"。
4. 稳定性可预测："We developed an accurate classifier to predict the stability of our designed proteins."，且这个数据集的价值超出本文："Beyond serving as a resource for protein engineering, this massive and diverse dataset also provides training data for machine learning."
5. 作者自认的边界（明写在文中）：寡聚态没按设计实现（F2/F4 二聚、"Further investigation would be needed to prove these assumptions."）；AF2 参数不能当筛子（"However, parameters for this should be carefully assessed in more detail and experimentally validated to identify ideal thresholds."）；设计规模被 230 nt 合成上限框住；筛除打分项与阈值只存在于 SI。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文的漏斗是"计算只做形状可行性，实验只做稳定性二分"**，中间没有任何"会不会结合/会不会催化"的判据。21% 这个数是**形状可行 × 蛋白酶抗性**的通过率，不是功能命中率。→ 对我们：把这类"稳定率"引为我们筛选的"预期成功率"是范畴错误；它能给的只是"物理设计 + 展示通量"这条路线的**分母量级**。
2. **"实验上限决定设计射程"是很少被写出来的诚实**。作者把 230 nt→~64 aa→最多 6 个 SS 元素当作设计前提。→ 对我们：酶设计项目里同样要先写清"我们一轮能测多少构建体、能测多长的蛋白"，再倒推候选生成器的复杂度上限，而不是先生成再想办法测。
3. **两个蛋白酶 + 随机序列定阈 + ladder 校批 = 一个"可跨批次比较"的量表工程**。这是他们能让 31,180 条序列可比的全部手段，且他们仍承认 EC50 只是 ΔG 的代理（引用前人相关性，本文未重新标定）。→ 对我们：LC-MS/MS 读数必须带**内参梯度**（已知转化率的标准曲线）与**阴性对照池**，否则跨天数据不可比，而"跨天不可比"正是我们单轮小样本最容易被否掉的地方。
4. **他们把失败（二聚/交换二聚）转化为下一代设计规则**（二硫键交联、针对 swapped dimer 的 negative design），而不是删掉这批数据。→ 对我们：把"寡聚/聚集态错误"明确记成一类可命名的失败（与分步化学事件并列的"构建体层面失败"），并在下一轮设计里显式负设计，比事后解释更有产出。
5. **分类器的最强特征是"局部几何 fragment alignment"，即 Rosetta 已在用的信息**。也就是说，ML 没有发现新物理，只是把物理量与非线性关系拟合成一把尺。→ 对我们：若用 ML 做催化可行性预测，必须先想清楚"我们的特征里有没有 Rosetta/结构比对之外的新信息"，否则模型只是把已有判据重新包装。
6. **作者自己拒绝把 AF2 当筛子**（缺阈值 + 有反例）。这与 [B09] 把 AF2 用作闸口形成时间线对照：AF2 可用是在 binder 任务上、有了百万级标注之后才被证明的；在"fold 稳定性"任务上他们选择不用。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：① 寡聚态偏离设计（F2/F4 主要为二聚体、含交换二聚可能）；② AF2 单序列预测有实质错例（Thio_330、bG-518.1），且未给可用于预筛的参数；③ 稳定性来自抗蛋白酶性而非热力学 ΔG，本文未重新标定；④ 筛除打分项与阈值全在 SI；⑤ 设计长度被合成/展示上限锁死在小蛋白。
- 我们读出：① **~21% 的分母不是"设计成功率"**：31,500 条序列里含约 2300 条随机对照，"稳定"线 0.5 沿用前人方法学口径，且 EC50 拟合依赖"配对 reads 必须匹配订购序列"这类计数规则——任何一步偏置都会平移整条分数；② 抽查只有 **21 条**（19 表达、15/19 谱相符、2 条 CD 未折），用它来"验证高通量屏"的统计力量极弱；③ 分类器是**同一批数据自证**：leave-one-fold-out 能防 fold 泄漏，但标签仍是 protease EC50，"predict stability"的稳定性不是独立测定的；外部 AUC 0.83 只在 Rocklin 一个集上给；④ 本文没有任何功能读出（无结合、无催化），因此它证明的是"能稳定地做出形状"，不是"能做出功能"——作者对此的说法是提供做功能的基础（"The methods and the wide range of protein shapes provide a basis for designing new protein functions without compromising stability."）；⑤ MD/QM 全程缺席，机理层面的解释（右手性 strand-helix-strand 限制、swapped dimer）都是几何/结构推断。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **把"发现的规则回灌进设计器"这一动作**（第 5 节第 2 条）：我们每轮湿实验后应产出**可执行的规则条目**（如"某类 loop 长度下催化残基几何必崩"），并写回候选生成器的约束里，而不是只写进讨论文字。本库判据里可作为 G7（规则闭环）的执行范式。
2. **实验预算先定设计射程**（230 nt → ~64 aa → ≤6 SS）：我们在下单前先固定"一轮能测多少个构建体、多长的酶、能测哪种读数"，再倒推候选生成规模与过滤层级；这是把漏斗设计变成**约束满足问题**的范例。
3. **量表工程三件套（阴性对照池 + 内参梯度 + 双读数）**：本文用随机序列定阈值、5 蛋白 ladder 校酶批、trypsin/chymotrypsin 交叉验证，并给出真实反例（ThioFL24）。→ 我们的 LC-MS/MS 面板必须有：无酶/无 ATP/死催化位点对照（定"背景阈值"）、已知转化率梯度蛋白（跨天校正）、**两个正交读数**（如产物定量 + 未掺入底物消耗），单读数一律不判"稳定/有活性"。
4. **抽查式校准（21 条）值得抄，但要放大**：他们的抽查是为了验证高通量读数可信，而不是为了发现新事实。→ 我们对主筛读数（如荧光/生长 rescue）应做小样本 LC-MS/MS 反查，并**预先声明要反查几条、按什么分层抽**（不同 fold/不同分数段），否则反查会挑到好做的。
5. **失败要命名并给出修正方案**（swapped dimer → 二硫交联 / negative design）。→ 对我们：把聚集、错寡聚、无表达这类失败各自命名，并写出对应的负设计手段，供下一轮直接引用。

**不可迁移（为什么不能照搬）**

1. **20.7%（6,200/30,000）不是我们的预期命中率，也不能折算**。它是"小蛋白形状可行性 × 抗蛋白酶性"的通过率，**完全不含催化信息**；目标酶要的是三步化学事件与竞争性副产物控制（分步化学事件），本文一个都没测。本库判据 §2 明禁把这类通量/稳定率当酶活概率。
2. **stability score > 0.5 / EC50 阈值不是酶活阈值**，而且它的前身是 protease 抗性与 ΔG 的相关性（作者只引用、未重标定）。我们若照抄"两档蛋白酶 + 阈值"，读的是折叠稳健性，不是活性。
3. **27,000 条寡核苷酸池 + FACS + NGS 的通量在产物化学上不存在**。本文的漏斗末端是"几万个序列一次测"，我们末端是"一轮、最多几个构建体的 LC-MS/MS"——**样本数换不了**，只能在信息量（机制多样性 + 失活对照）上补。
4. **本文没有 MD/QM**，不能为"用 MD/QM 判催化"提供任何参照；它甚至明确拒绝用 AF2 做预筛。想用它的 scaffold 库，需要自己补功能层证据。
5. **Random Forest 的特征体系不能直接搬**：110 个特征围绕"是否稳定"构造，其中最强项是局部几何 fragment alignment；这些特征对"是否催化酶设计"没有已知相关性，必须重新做特征-标签配对验证才有资格进漏斗。

## 9. 溯源与自检

- 本地纯文本：`data/interim/baker_lit/ft/smallfolds2022.txt`（Europe PMC `fullTextXML`，期刊版 → 标签剥离 → `litcards_text.norm` 归一化，未改写内容）。
- 引句底稿: data/interim/baker_lit/ft/smallfolds2022.txt
- 对照底稿行号：`sources/baker.md:94–105`（原卡；其中"候选生成=蓝图/片段组装""约 30,000→约 6,200"两处已核对）、`sources/baker.md:640`（B07 的 21% 分母锚点行）。
- **对原卡的一处更正**：`sources/baker.md` 与 CSV 把实验手段记作"E. coli 高通量表达 + SEC/CD"，正文实际是**酵母表面展示 + 双蛋白酶滴度 + FACS + NGS 为主筛（31,500 条）**，E. coli 表达 + SEC/CD/NMR 只是 21 条设计的抽查验证。本卡按正文改写，CSV 回填块里两处都写明。
- 原文指针：代码 "https://github.com/strauchlab/scaffold_design"（Methods："our protocol has been deposited on github"）；EC50 拟合脚本 "https://github.com/asford/protease_experimental_analysis"；结构存档 PDB 7LDF、BMRB 30844；序列计数与筛选流程细节在 experiments.csv 与 SI。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only B07 --no-report`（引句全部与本节声明的引句底稿逐字比对）；结果见本次回报。
- 诚实声明：本卡没有把 Fig 2d/e 的逐 fold 成功率编成数字（本地全文只有图，无表）；也没有把 SI 里的打分项清单当作已知项——凡此皆标"正文未给/在 SI"。

<!--CSV回填
work_type=论文（小蛋白 fold 的形状/序列空间大规模采样平台 + 蛋白酶高通量稳定性屏 + 跨 fold 稳定性分类器）
target=8 种小蛋白 fold 的形状多样性：三螺旋束 3H、四螺旋束 4H、超螺旋 coil、beta-grasp、ferredoxin、thioredoxin（含最小化变体），以及两种自然界未见的 αβββα（F2）与 βααβββ（F4）
backbone_generation=自研 FoldArchitect（RosettaScripts 内的 FoldArchitectMover）：读 fold 级 XML 描述（SS 与 loop 长度范围、距离约束方式、register shift、beta bulge），用 DivideAndConqueror 把整链拆成含完整配对的最小子段增量折叠，ABEGO 约束下的 PDB 片段插入 poly-valine 伸展链，未过 filter 时由 Perturber 改变子段参数重试；序列设计走两条 Rosetta 协议（按溶剂暴露选 rotamer 子集 + 递增排斥项；或先用 pair-motif 铺核心再做同样 rotamer 设计）
computational_filters=骨架侧：Rosetta filter（omega/rama 角严格过滤、Helix kink 弯曲限制、BetaSheetArchitect 只允许无悬空残基的合法 sheet、松弛/有界调和距离约束偏置成形 sheet）；序列侧：一组 filter 项 + 计算能量选设计（完整打分项清单在 SI，正文未给阈值）；实验侧：trypsin 与 chymotrypsin 双蛋白酶 EC50 → stability score，随机序列池定稳定阈值、5 条已知稳定蛋白做批次内参；后期 Random Forest（110 特征，leave-one-fold-out 验证）
thresholds=距离约束 std 2 Å、sheet/helix 间距默认 8 Å（beta-grasp 一处调至 9 Å）、螺旋弯曲 <15°、每 fold 生成并打分 2000–12,000 条设计、成功口径 stability score > 0.5（Fig 2d/e 分档）、五档蛋白酶浓度（trypsin 0.07/0.21/0.64/1.93/5.78 µM；chymotrypsin 0.08/0.25/0.74/2.22/6.67 µM）、qPCR 终止于 50% 最大产量、Random Forest 500 棵树 + fivefold 交叉验证 + bootstrap/OOB；设计筛除的能量/打分阈值=未记录（正文明写 All score terms for filtering and evaluating designs are summarized in the SI）
md_used=否（全文里 MD 仅出现在参考文献 16 的标题中；PDBMD2CD 是从结构预测 CD 谱的工具，本文未做任何动力学筛选）
qm_used=否
experimental_methods=DNAworks2.0 反译（ecoli2 密码子）→ Agilent 27,000 寡核苷酸池 → qPCR 欠扩增 + 胶回收 → 40 bp 同源臂重组进 EBY100 的 pETCON3 酵母展示 → 诱导 16–18 h（30 ℃ SGCAA）→ 双蛋白酶浓度滴度消化（5 min 后 1% BSA 淬灭）→ 抗 c-Myc-FITC 标记 → Sony SH800 FACS 分"未切"细胞（每条件约 10 million cells，并记录消化前过阈比例）→ 条形码化 NGS（reads 须含 NdeI/XhoI 完整位点且逐氨基酸匹配）→ 概率模型（拟一级动力学，MAP 估计）算 EC50 与 stability score → 21 条设计做 E. coli 表达 + SEC/SEC-MALS + CD（25/95 ℃ 与熔解曲线）+ PDBMD2CD 预测比对 + 1H NMR（4 条）+ ColabFold 单序列预测 + 同位素标记多维 NMR 解结构（ThioM_802，CNS 100 初结构取最低能 20）
pipeline_counts=每 fold 2,000–12,000 完成打分模型 → 摘要口径约 30,000 设计（8 fold）→ 实验表征 31,500 条序列（含约 2300 条随机负对照）→ 拟合出 EC50/稳定性分 >31,180 条 → 约 6,200 个稳定蛋白（≈21%）；抽查层：21 条设计 → 19 条在 E. coli 表达 → CD 除 2 条外均折叠、15/19 与预测谱相符 → 4 条 NMR 证实三级结构、8 条测热稳
hit_rate=按 stability score 分档的 fold 级成功率：三螺旋束最高（与前报一致），thioredoxin 与 coil 最低；总体约 6,200/30,000 ≈ 21%（这是"抗蛋白酶稳定率"，非功能/结合/催化命中率；逐 fold 数值在 Fig 2d/e，本地全文无表）；稳定性分类器 AUC ≈ 0.83（在 Rocklin 等外部小 fold 集上，单一模型跨 fold）
best_metric=未记录（本文目标是稳定性而非亲和力或活性，无 Kd/kcat 类指标；结构精度最好值为最小化 thioredoxin ThioM_802 的 NMR 系综与设计模型一致性：top structure RMSD 1.9 Å（C-alpha），β-链部分 1.1 Å；PDB 7LDF / BMRB 30844）
cost_or_stat_note=算力：40–50 残基 mini 蛋白从伸展链折叠"可能需要数千条轨迹"才能出一条正确折叠的；旧蓝图法需专家多步手工干预（本文用 DivideAndConqueror+Perturber 自动化）；通量：27,000 条寡核苷酸一池、五档蛋白酶 × 两种蛋白酶、每条件约 10 million 细胞分选；设计长度受 230 nt 单链上限约束（~64 aa、约 6 个二级结构元素）
role_in_timeline=纯 Rosetta 物理打分时代"功能前置基础设施"的量化锚点：把 blueprint 驱动换成 fold 参数化 + 轨迹内形状采样，给出 ~20% 稳定率与三万量级投入的分母基线（与 [B05] 的 96→73→50 并列构成分母参照）；同时留下两个被后续深度学习路线接手的缺口——(a) 物理筛除阈值不透明（在 SI）、(b) AF2 单序列预筛"能用但阈值未定"（作者明确拒绝当闸口，[B09] 才在 binder 任务上把 AF2 判据量化）；其 scaffold 数据集与折叠规则（螺旋-螺旋 loop 连接、右手性 strand-helix-strand 限制）成为后续最小化设计、结合蛋白 scaffold 与稳定性预测模型的训练资源
source_pointer=data/interim/baker_lit/ft/smallfolds2022.txt（Europe PMC PMC9684540 fullTextXML，2026-10-16 抓取）；sources/baker.md:94-105、640；代码 github.com/strauchlab/scaffold_design；EC50 脚本 github.com/asford/protease_experimental_analysis；PDB 7LDF；BMRB 30844
CSV回填-->
