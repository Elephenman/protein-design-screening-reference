# [B05] ProteinMPNN——把"出序列"从算力黑洞变成 1 秒一步，并用似然值给候选排序

Dauparas J, Anishchenko I, Bennett N, Bai H, Ragotte R, Milles L, Wicky B, Courbet A, de Haas R, Bethel N, Leung P, Huddy T, Pellock S, Tischer D, Chan F, Koepnick B, Nguyen H, Kang A, Sankaran B, Bera A, King N, Baker D（UW-IPD / HHMI / Wageningen / LBNL）
Science 2022, 378:49-56 · DOI 10.1126/science.add2187 · PMID 36108050 · PMCID PMC9997061
开放获取（CC BY 4.0，HHMI author manuscript）· 全文链接 https://pmc.ncbi.nlm.nih.gov/articles/PMC9997061/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B05**（组：Baker组; 通用方法学） |
| 本文取回方式 | Europe PMC `fullTextXML`（PMC9997061，author manuscript 版），2026-10-16 本地抓取 |
| 本地全文 | `data/interim/baker_lit/ft/proteinmpnn2022.txt`（46,876 B；标签剥离后 46,673 字符） |
| 对照底稿 | `sources/baker.md` 第 68–79 行（原卡）与 `sources/baker.md:604`（序列设计环节对照表）、`sources/baker.md:638`（"为什么做这一步"记录） |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中；见第 9 节自检） |
| 未取到的部分 | Supplementary Methods、Figure S1–S3、Table S1（本地全文只有正文 + 图注 + Table 1 的表格文字）。本卡的训练超参、温度扫描细节、以及"NLL 阈值/排序取前多少条"等只能写正文里出现过的；正文未给的地方明写"原文未给阈值" |

## 1. 这篇到底解决什么（大白话）

设计蛋白的分工原本是"骨架由某种生成法给，序列由 Rosetta 的组合侧链打包给"。后者有两个致命成本：**慢**（100 残基要 4.3 分钟，还要人反复调限制条件）和**挑界面**（同一个骨架，Rosetta 出的序列经常不折、或折成错的寡聚态）。这篇做的事：把"给定骨架 → 出序列"这个**反折叠问题**交给一个消息传递网络，输入只是骨架原子坐标的几何量（N/Ca/C/O/虚拟 Cb 之间的距离、帧朝向、二面角），输出每位置氨基酸分布，自回归地按随机顺序解码。三件事一次交付：① 天然骨架上的序列回收率从 Rosetta 的 32.9% 提到 52.4%，算力只花 1.2 秒/100 残基；② 通过**随机解码顺序 + logits 耦合**，同一个模型能做均聚/异聚、对称位点绑定、重复蛋白、甚至"多态设计"（一条序列要同时编码两个构象）；③ 最重要的——**把别人失败的设计救活**：AF 幻觉出来的骨架配 AF 自己的序列大多不溶，换成 MPNN 序列后可溶表达 73/96；Rosetta 设计的环寡聚体 0/若干条寡聚态正确，MPNN 重设序列后 27.7% 正确。附带给出一个可直接用于漏斗的**排序量**：模型给的序列平均对数概率（NLL）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **物理方法的目标与实际优化对象不一致，导致必须人工定制**（这是全文最有价值的"归因"段）：作者指出真正想要的是"序列的最低能态是目标结构"，但这算不动——"This is, however, computationally intractable as it requires computing energies over all possible structures, including unwanted oligomeric and aggregated states"，于是 Rosetta 实际做的是代理问题："instead Rosetta and other approaches as a proxy carry out a search for the lowest energy sequence for a given backbone structure, and structure prediction calculations are required in a second step to confirm that there are no other structures in which the sequence has still lower energy"。后果是："Because of the lack of concordance between the actual design objective and what is being explicitly optimized, considerable customization can be required to generate sequences which actually fold"，并且举了一个具体的模糊地带："for example in Rosetta design calculations hydrophobic amino acids are often restricted on the protein surface as they can stabilize undesired multimeric states, and at the boundary region between the protein surface and core there can be considerable ambiguity about the extent to which such restrictions should be applied"。
   **应对**：不再优化能量，而是**直接训练"给定骨架最可能的氨基酸"**——"While deep learning methods lack the physical transparency of methods like Rosetta, they are trained directly to find the most probable amino acid for a protein backbone given all the examples in the PDB, and hence such ambiguities do not arise, making sequence design more robust and less dependent on the judgement of a human expert."
   **留下的代价**：作者自己承认换来的是可解释性——"While deep learning methods lack the physical transparency of methods like Rosetta"；且这套好处建立在 PDB 分布之上，对 PDB 里没有的几何（见第 6 条）没有保证。
2. **老指标的判别力与设计目标脱钩**。"While recent protein sequence design approaches have focused on maximizing native sequence recovery, this is not necessarily optimal for actual protein design applications."，作者进一步拆掉自己的指标："In silico metrics such as native sequence recovery are very sensitive to crystallographic resolution"、"and may not correlate with proper folding (even a single residue substitution, while causing little change in overall sequence recovery, can block folding)"。
   **应对**：① 换评估口径——用 **AF 单序列预测能不能复现骨架**（lDDT-Ca 95/90 计数）当 in silico 成功；② 最终判据交回湿实验："in the same way that language translation accuracy must ultimately be evaluated by human users, the ultimate test of sequence design methods is experimental characterization"。
   **留下的代价**：AF 单序列预测本身在天然序列上就偏弱（"generally produce much poorer structures when provided only with a single sequence"），用它当"成功"定义会把 AF 的偏好混进结论。
3. **完美骨架上训练出的模型，用到预测结构上就退化**——真正的设计输入是模型骨架，不是晶体骨架。现象：模型在 perfect backbones 上回收率最高，但"the average sequence recovery for perfect backbones decreases with increasing amounts of noise added during training"，看起来像"加噪声是纯损失"。
   **应对**：**故意在训练时加高斯噪声**（std=0.02 Å 起步，另训 0.3 Å 档），并给出机理猜想："Crystallographic refinement may impart some memory of amino acid identity in the backbone coordinates which is recovered by the model trained on perfect backbones but not present in predicted structures; since the goal is to identify optimal sequences given the overall backbone context the more robust model is preferable." 实测收益是噪声模型在 AF 模型上回收率更高，且"0.3 Å 噪声档让 AF 预测落在 lDDT-Ca 95/90 的序列数增至 2–3 倍"。
   **留下的代价**：**没有单一最优模型**——图注把这件事写成一对取舍："For higher accuracy predictions (circles) smaller amounts of noise are optimal (1.0 corresponds to 1.8% success rate), while to maximize prediction success at a lower accuracy cutoff (squares), models trained with more noise are better (1.0 corresponds to 6.7% success rate)"，即"要多而稳"就用高噪声模型，"要准"就用低噪声模型；本文没有给出按任务选噪声档的规则。
4. **对称/多链/重复结构不是单链问题，但当时只有单链模型**。前作局限："However, the methods described thus far are limited in their applicability to the wide range of current protein design challenges, and have not been extensively validated experimentally."
   **应对**（三步架构改造）：① 随机解码顺序——"we replaced the fixed N to C terminal decoding order with an order agnostic autoregressive model in which the decoding order is randomly sampled from the set of all possible permutations"，顺带让"固定中间序列"变得可能："Order agnostic decoding enables design in cases where, for example, the middle of the protein sequence is fixed and the rest needs to be designed, as in protein binder design where the target sequence is known"；② 多链等变性——保留 ±32 的链内相对位置编码，另加一个"同一链/不同链"的二值特征；③ **耦合位置**=先对绑定位置的两侧分别出 logits 再合并成一个分布采样；多态设计则"Multi-state protein sequence design to generate a single sequence that encodes two or more desired states can be achieved by predicting logits for each state and then averaging"，更一般地"more generally a linear combination of predicted logits with some positive and negative coefficients can be used to upweight, or downweight specific backbone states to achieve explicit positive-negative sequence design"。
   **留下的代价**：耦合让回收率的可解释性变差——"Because of the non-local context, sequence recovery is no longer a monotonic function of the average Cb neighbor distance"；且正负权重做多态设计这一段在本文**只有能力声明，没有实验结果**（正文没给出用这条路设计出的开关）。
5. **AF 幻觉出的全新骨架，配它自己的序列大多不溶**（最贵的坑，也是最直接的证据）："However, we found that the AF generated sequences were mostly insoluble (median soluble yield: 9 mg per liter of culture equivalent Figure 3A )"（他们先试了 150 个蛋白）。
   **应对**：把"骨架"与"序列"这两个失败源切开——"In each case, we attempted to rescue previous failed designs with sequences generated using Rosetta or AlphaFold-we kept the backbones of the original designs fixed but discarded the original sequences and generated new ones using ProteinMPNN." 同一批骨架换序列后："The success rate was far higher: of 96 designs produced in E. coli , 73 were expressed solubly (median soluble yield: 247 mg per liter of culture equivalent, Figure 3A ) and 50 had the target monomeric or oligomeric state as assessed by SEC"。
   **留下的代价**：这个"分诊法"只能救序列问题；骨架本身错（如第 7 条的错寡聚态倾向）不在本文射程内，作者也没量化"多少比例的设计是序列问题"。
6. **Rosetta 在对称组装体上不是"成功率低"而是"全军覆没"**："For the Rosetta designed set, 40% were soluble and none had the correct oligomeric state confirmed by SEC-MALS."
   **应对**：把环对称 + 内部重复**同时**绑定（within 与 between chains 一起 tie），并用同一套模型重出序列；结果："For the ProteinMPNN designed set, 88% were soluble and 27.7% had the correct oligomeric state."
   **留下的代价**：27.7% 仍然意味着四分之三不对；本文的补救手段仍然是"同一骨架出多条序列 + 排序"，没有从原理上保证寡聚态。
7. **纳米颗粒的旧流程要靠人周级干预**："We started with a set of previously described protein backbones for two-component tetrahedral designs generated using a compute- and effort-intensive procedure that involved Rosetta sequence design followed by more than a week of manual intervention to eliminate unwanted substitutions"。
   **应对**：全自动出序列并**直接下单，不做人肉修序列**："We used ProteinMPNN to design 76 sequences spanning 27 of these tetrahedral nanoparticle backbones, tying identities at equivalent positions in the 12 copies of each subunit in the assemblies, and ordered plasmids encoding them without further intervention."；结果："We found upon expression in E. coli and purification by SEC that 13 designs formed assemblies with the expected MW (~1 MDa)"，且"Although a similar overall success rate was obtained using Rosetta in the original study, several new tetrahedral assemblies were successfully generated using ProteinMPNN that had failed using Rosetta."
   **留下的代价**：作者明说总体成功率与旧法相当——收益是**人力与时间**，不是命中率；这一点很容易被后续引用者读成"命中率提高"。
8. **一个 Rosetta 完全做不动的功能设计（富脯氨酸 motif 支架）**。原文解释为什么难："the design problem is challenging as very few native proteins have proline rich secondary structure elements that closely interact with the core of the protein"，且原设计确实失败："but sequences designed for these backbones did not fold to structures binding Grb2 when expressed in E. coli"。
   **应对**：同骨架换 MPNN 序列 → "Biolayer interferometry experiments showed strong binding to the Grb2 SH3 domain"，且信号高于游离肽（"with considerably higher signal than the free proline rich peptide"）；再用**定向破坏**证明是设计位点在起作用："point mutations predicted to disrupt the design completely eliminated the binding signal"，结论句"Thus ProteinMPNN can generate sequences for challenging protein design problems even when traditional RosettaDesign fails."
   **留下的代价**：机制解释靠两个 Asn→Asp 的负对照，属于"打断即证"，没有亲和力定量比较（正文未给 Kd）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **模型本体**：message passing neural network，3 encoder + 3 decoder、128 hidden dims，自回归出序列；输入是骨架几何量（N、Ca、C、O 与由骨架原子外推的虚拟 Cb 之间距离、Ca-Ca-Ca 相对帧朝向/旋转、骨架二面角）。**选它的理由**（作者原话）："locally connected graph neural networks can be used to model the structure to sequence mapping problem because protein backbones provide a notion of local neighborhoods which primarily determine sequence identities"。
- **对照基线**：Rosetta fixed backbone combinatorial design（"one round of the PackRotamersMover"，default options，beta_nov16 score function）。
- **评估器**：① native sequence recovery（按埋藏度分档）；② **单序列 AlphaFold** 复现骨架的程度（lDDT-Ca ≥ 90/95 计数）；③ 实验：E. coli 可溶产量（SEC 积分面积折算 mg/L）、SEC/SEC-MALS 寡聚态、CD 热稳定性、X 射线/cryoEM/negative stain EM、BLI。
- **漏斗用的排序量**：序列平均对数概率（NLL）+ 采样温度（控多样性）。
- **没有用的方法**：MD、QM、自由能微扰；也没有 Rosetta 能量重打分做闸口（这一点与 [B09] 的"AF2 界面 pAE"是两条独立路线，本文只给序列侧）。

### 工作流（正文可复现顺序；实验救援部分是本文的真正落点）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 | 前作 MPNN（3 enc/3 dec、128 dims、N→C 顺序解码） | 加输入特征：N/Ca/C/O/虚拟 Cb 间距离 | 以 held-out 序列回收率定优劣（Table 1） | 回收率 41.2%（baseline）→ 49.0%（experiment 1）；参数量 1.381 mln → 1.430 mln |
| 2 | 同一模型 | 在 encoder 里加 edge updates（experiment 2）；再与 1 合并（experiment 3） | 同上 | 43.1%（实验 2）→ 50.5%（实验 3，1.678 mln 参数）；作者结论："interatomic distances evidently provide a better inductive bias to capture interactions between residues than dihedral angles or N-Ca-C frame orientations" |
| 3 | 合并后的模型 | 扫邻域规模：16/24/32/48/64 最近 Ca 邻居 | 性能饱和点 | "we experimented with 16, 24, 32, 48, and 64 nearest Ca neighbor neural networks"，"performance saturated at 32-48 neighbors" |
| 4 | 同上 | 把固定 N→C 解码换成**顺序无关自回归**（每步随机采样一个排列） | 回收率 + 能不能固定任意子集 | 50.8%（experiment 4）；能力上支持 binder 设计里"靶序列已知、只设计其余部分" |
| 5 | 顺序无关模型 | 加多链等变特征：链内相对位置编码封顶 ±32 残基 + "同链/异链"二值特征；对称位点用 logits 平均耦合 | 均聚体上比较三种做法 | "unconstrained design without symmetry, averaged probabilities, and averaged logits resulted in 52%, 53%, and 55% median sequence recoveries respectively"（取 logits 平均） |
| 6 | 同上 | 训练集清洗与去冗余 | **分辨率 <3.5 Å、链总残基 <10,000、X-ray 或 cryoEM**；**mmseqs2 在 30% 序列一致性阈值聚类** | 25,361 个聚类（PDB 截至 Aug 02, 2021）；早期单体训练/验证用 19.7k 高分辨率单链结构，按 CATH 划分 |
| 7 | 定稿模型 | 与 Rosetta 正面对拍：同一批骨架各出序列 | 回收率 + 算力 | "For a test set of 402 monomer backbones we redesigned sequences using Rosetta fixed backbone combinatorial sequence design"；"Although requiring only a small fraction of the compute time (1.2 seconds versus 4.3 minutes for 100 residues), ProteinMPNN had a much higher overall native sequence recovery (52.4% vs 32.9%)" |
| 8 | 定稿模型 | 按体系类型分层验证 | 三类测试集 | "We evaluated ProteinMPNN on a test set of 690 monomers, 732 homomers (with less than 2000 residues), and 98 heteromers."；中位回收率 52%/55%/51%；埋藏度分层："sequence recovery correlated closely with residue burial ranging from 90-95% in the deep core to 35% on the surface" |
| 9 | 定稿模型 | **训练时加高斯坐标噪声**（std=0.02 Å 与更大档） | 判据换成"在 AF 模型骨架上的回收率 + AF 单序列能否复现（lDDT-Ca 90/95）"，而非晶体骨架回收率 | "We found that training models on backbones to which Gaussian noise"（正文紧接 std=0.02Å）"had been added improved sequence recovery on confident protein structure models generated by AlphaFold (average pLDDT>80.0) from UniRef50"；"noise generated 2-3 times more sequences with AlphaFold predictions within lDDT-Ca"（正文此处在 0.3Å 之后，紧接 of 95.0 and 90.0 of the true structures than unnoised or slightly noised models） |
| 10 | 噪声档模型 | 推理温度扫描：高温多采、低温求准 | 序列多样性 vs 平均回收率 | "We found that the diversity of sequences generated by MPNN could be considerably increased, with only a very small decrease in average sequence recovery, by carrying out inference at higher temperatures" |
| 11 | 每骨架的批量序列 | **用模型似然排序，把"该送哪几十条"变成可算的操作** | 排序量＝序列给定结构下的平均对数概率；**正文未给"取前 N 条/阈值"的数字** | "We also found that a measure of sequence quality derived from the ProteinMPNN, the averaged log probability of the sequence given the structure, correlated strongly with native sequence recovery over a range of temperatures"，"enabling rapid ranking of sequences for selection for experimental characterization." |
| 12 | 此前失败的 AF 幻觉骨架（Fig 3A 图注口径 N=129；正文另记尝试表达 150 个蛋白，两个数口径不完全一致，本卡如实并列） | 分诊实验：骨架不动、只换序列 | 可溶产量（SEC 积分面积）、SEC 峰位是否为目标寡聚态 | 先用 AF 自序试 150 个蛋白→"the AF generated sequences were mostly insoluble (median soluble yield: 9 mg per liter of culture equivalent Figure 3A )"；换 MPNN 后→"of 96 designs produced in E. coli , 73 were expressed solubly (median soluble yield: 247 mg per liter of culture equivalent, Figure 3A ) and 50 had the target monomeric or oligomeric state as assessed by SEC"；热稳定性："Many of the proteins were highly thermo-stable, with secondary structure being maintained up to 95 °C" |
| 13 | 其中一个单体设计 | 结构确认（X 射线） | 与设计骨架的偏差、与 PDB/UniRef 的相似度（说明"不是抄来的 fold"） | 8CYK："and is close to the design target backbone"（正文此处括号为 2.35 Å over 130 residues）；"The alpha-beta protein structure contains 5 beta strands and 4 alpha helices"；图注给相似度口径："(E-value=2.8 against UniRef100 using HHblits, TM-score=0.56 against PDB)" |
| 14 | Rosetta 的重复蛋白设计（DHR82）与 C5/C6 环寡聚体 | 重复单元内 + 链间同时 tie；重出序列 | SEC/SEC-MALS 寡聚态；图注给重复蛋白例子的偏差 | "We found that many previously suboptimal Rosetta designs of repeat protein structures could be rescued by ProteinMPNN redesign"；Rosetta 集"40% were soluble and none had the correct oligomeric state confirmed by SEC-MALS"→MPNN 集"88% were soluble and 27.7% had the correct oligomeric state"；重复蛋白图注："ProteinMPNN rescue of Rosetta design made from a perfectly repeating structural and sequence unit (DHR82)"（同一图注给偏差 ~1.2Å error over 232 residues） |
| 15 | 两组分四面体纳米颗粒骨架（27 个） | 每个亚基 12  copies 的等价位置 tie；自动出 76 条序列，不做人工修正，直接下单 | SEC 是否给出预期 MW（~1 MDa）；晶体比对 | 13 个组装成功；"the crystal structure (grey) is very nearly identical to the design model (green/purple)"（同一句后半给 backbone RMSD of 1.2 Å over two complete asymmetric units） |
| 16 | Grb2 SH3 识别的富脯氨酸支架（RIFDOCK 对接 + Rosetta remodel 建 loop + Rosetta layer design） | 同骨架换 MPNN 序列 | BLI 结合信号（对比 Rosetta 设计与游离肽）；再用预测破坏位点的点突变做负对照 | "but sequences designed for these backbones did not fold to structures binding Grb2 when expressed in E. coli" → "Biolayer interferometry experiments showed strong binding to the Grb2 SH3 domain" → "point mutations predicted to disrupt the design completely eliminated the binding signal" |
| 17 | 交付 | 部署与口径固化 | 全流程自动化 | "Sequence generation with MPNN is fully automated and requires only ~1 second per backbone, vastly streamlining the design process compared to the earlier Rosetta-based procedure."；"ProteinMPNN solves sequence design problems in a small fraction of the time (1.2 sec vs 258.8 sec on a single CPU for a 100 residue protein)" |

**这套流程的骨架值得单独记住**：它把设计流水线切成**"骨架对不对"与"序列对不对"两个可分诊的问题**（步骤 12 的 kept backbones fixed / discarded sequences），并且给"送测哪几十条"一个免费的排序量（步骤 11 的 NLL）。[B09] 后来算的 efficiency（通过率÷单价）就是在这个单价上做的。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 52.4% vs 32.9% | 天然骨架上的序列回收率：MPNN vs Rosetta | "ProteinMPNN had a much higher overall native sequence recovery (52.4% vs 32.9%)" |
| 1.2 seconds vs 4.3 minutes | 100 残基出序列的算力（MPNN vs Rosetta） | "Although requiring only a small fraction of the compute time (1.2 seconds versus 4.3 minutes for 100 residues)" |
| 1.2 sec vs 258.8 sec | 同一件事的另一种口径（单 CPU，100 残基） | "(1.2 sec vs 258.8 sec on a single CPU for a 100 residue protein)" |
| ~1 second / backbone | 全流程自动化后的单价 | "requires only ~1 second per backbone" |
| 41.2% / 49.0% / 43.1% / 50.5% / 50.8% | 消融链：baseline / 加距离特征 / 加 edge updates / 合并 / 随机解码 | "This resulted in a sequence recovery increase from 41.2% (baseline model) to 49.0% (experiment 1)" |
| 1.381 mln → 1.678 mln | 参数量随消融增长 | Table 1（"Baseline model None 1.381 mln"… "Experiment 3 Combine 1 and 2 1.678 mln"） |
| 32–48 neighbors | 几何邻域饱和点 | "performance saturated at 32-48 neighbors" |
| ±32 residues | 链内相对位置编码封顶 | "we kept the per chain relative positional encoding capped at" |
| <3.5 Å / <10,000 residues / Aug 02, 2021 | 训练集筛选条件 | "We trained ProteinMPNN on protein assemblies in the PDB (as of Aug 02, 2021)"（同句给出筛选口径：X-ray crystallography or cryoEM to better than 3.5Å resolution and with less than 10,000 residues） |
| 30% 一致性 / 25,361 clusters | 去冗余聚类阈值与结果 | "Sequences were clustered at 30% sequence identity cutoff using mmseqs2"，"resulting in 25,361 clusters" |
| 402 / 690 / 732 / 98 | 对拍单体集 / 三类体系测试集规模 | "For a test set of 402 monomer backbones" |
| 52% / 55% / 51% | monomer / homomer / heteromer 中位回收率 | "The median overall sequences recoveries were 52% for monomers, 55% for homomers, and 51% for heteromers" |
| 90–95% → 35% | 回收率随埋藏度（深核→表面） | "sequence recovery correlated closely with residue burial ranging from 90-95% in the deep core to 35% on the surface" |
| 52% / 53% / 55% | 无约束 / 概率平均 / logits 平均（均聚体） | "unconstrained design without symmetry, averaged probabilities, and averaged logits resulted in 52%, 53%, and 55% median sequence recoveries respectively" |
| std=0.02 Å、0.3 Å | 训练噪声档 | "We found that training models on backbones to which Gaussian noise" + "had been added improved sequence recovery" |
| pLDDT>80.0（UniRef50 AF 模型）；lDDT-Ca 95.0/90.0 | 噪声模型的评估口径；0.3 Å 档收益 2–3 倍 | "improved sequence recovery on confident protein structure models generated by AlphaFold (average pLDDT>80.0) from UniRef50" |
| 1.8% 与 6.7% | 噪声档 1.0 在高准/低准两种 cutoff 下的 AF 成功率（取舍证据） | 图注 "For higher accuracy predictions (circles) smaller amounts of noise are optimal (1.0 corresponds to 1.8% success rate)" |
| 396 / 150 / 129 / 96 / 73 / 50 | 重设计的天然结构数 / 先试的 AF 自序蛋白数 / Fig3A 骨架集 / MPNN 实测数 / 可溶数 / 目标态数 | "we attempted to express 150 proteins in E. coli"；"The success rate was far higher: of 96 designs produced in E. coli , 73 were expressed solubly" |
| 9 mg/L → 247 mg/L | 中位可溶产量（AF 自序 → MPNN 序列） | "(median soluble yield: 9 mg per liter of culture equivalent Figure 3A )" |
| 95 °C | 二级结构保持温度上限（多个设计） | "with secondary structure being maintained up to 95 °C" |
| 2.35 Å / 130 residues；TM-score 0.56；E-value 2.8 | 单体设计的晶体一致性与其"非天然性" | "and is close to the design target backbone"（正文此处括号为 2.35 Å over 130 residues）；"(E-value=2.8 against UniRef100 using HHblits, TM-score=0.56 against PDB)" |
| 40% / 0% → 88% / 27.7% | C5/C6 环寡聚体：Rosetta 序列 vs MPNN 序列（可溶 / 寡聚态正确） | "For the Rosetta designed set, 40% were soluble and none had the correct oligomeric state confirmed by SEC-MALS." |
| 76 序列 / 27 骨架 / 12 copies / 13 个 ~1 MDa 组装 / 1.2 Å | 四面体纳米颗粒救援规模与结构一致性 | "We used ProteinMPNN to design 76 sequences spanning 27 of these tetrahedral nanoparticle backbones" |
| >1 week 人工干预 | 旧纳米颗粒流程的人力成本（本文的对照基线） | "followed by more than a week of manual intervention to eliminate unwanted substitutions" |
| 3,000 backbones（NTF2 集） | Rosetta 设计的 NTF2 fold 骨架规模，MPNN 重设后 AF 单序列成功率显著改善 | "ProteinMPNN redesign of previous Rosetta designed NTF2 fold proteins (3,000 backbones in total)" |

## 5. 结论——作者说了什么

1. 一句话总括（结论段）："ProteinMPNN solves sequence design problems in a small fraction of the time (1.2 sec vs 258.8 sec on a single CPU for a 100 residue protein) required for physically based approaches such as Rosetta, which carry out large scale sidechain packing calculations, achieves much higher protein sequence recovery on native backbones (52.4% vs 32.9%), and most importantly, rescues previously failed designs made using Rosetta or AlphaFold for protein monomers, assemblies, and protein-protein interfaces"。
2. 通用性来自架构改造（顺序无关解码 + 位置耦合），因此"单体、环寡聚体、纳米颗粒、界面"一套模型通吃；并且"Unlike Rosetta and other physically based methods, ProteinMPNN requires no expert customization for specific design challenges, and it should thus make protein design more broadly accessible."
3. 评估哲学：作者明确不接受只用 in silico 指标下结论——"in the same way that language translation accuracy must ultimately be evaluated by human users, the ultimate test of sequence design methods is experimental characterization"。
4. 组织层面的自我宣告："The high rate of experimental design success of ProteinMPNN, together with the high compute efficiency, applicability to almost any protein sequence design problem, and lack of requirement for customization has made it the standard approach for protein sequence design at the Institute for Protein Design"。
5. 展望与自限：作者认为 MPNN 序列对天然骨架"预测折叠得更自信更准"，因此可能可用于提升重组天然蛋白的表达与稳定性，但限定"residues required for function would clearly have to be kept fixed"；当时尚未做蛋白-核酸与蛋白-小分子（"We are currently extending ProteinMPNN to protein-nucleic acid design and protein-small molecule design"）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文真正的漏斗贡献不是"更好的序列"，而是"免费的排序量"**。NLL 是模型白送的，不需要额外计算；但它的相关对象是 **native sequence recovery**，不是实验成功率（正文只声称前者）。→ 对我们：任何"从模型内部取一个分数当筛子"的做法，都必须先自问"它相关的是哪个标签"，否则就是拿代理指标做终局判据（与 [B09] 第 2.3 条"生成阶段用过的指标不能当筛子"是同一类错误）。
2. **"骨架不动、只换序列"是本文最可复用的实验设计**。它把一次失败变成可分诊的两类（几何错 vs 序列错），因此"救援率"本身成了诊断工具。→ 对我们：候选失败时应先做"只换一侧"的最小对照（例如保持催化残基排布不动、只重做 loop/表面；或反过来），而不是整条重建。
3. **"没有单一最优噪声档"提示了评估口径决定选型**。同一模型族，按"高准"和"高通过率"会选出不同的模型。→ 对我们：判据必须先写清"我们优化的是单条候选的正确率，还是每批候选的通过数"，两个口径下的最优配置通常不同。
4. **纳米颗粒那条是"省人力不省命中率"**（作者自述总体成功率与 Rosetta 相当）。→ 对我们：引用本文时不许把"救援成功"读成"命中率提升 X%"；它的量化收益在时间/人工，命中率收益集中在特定体系（环寡聚体、SH3 支架）。
5. **本文完全没有 MD/QM，也没有催化层评估**。它的能力边界是"给定几何，出序列"，对"这条序列能不能催化一个反应"不提供判据——催化相关的所有断言都得靠功能残基被固定（作者只在展望里提了"功能残基要 fixed"这一句）。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：① 缺物理透明性（"lack the physical transparency of methods like Rosetta"）；② in silico 回收率对分辨率敏感、且可能与能否折叠无关（单点突变即可阻断折叠）；③ 噪声模型的取舍未解决（按 cutoff 选档）；④ 蛋白-核酸/小分子当时未覆盖。
- 我们读出：① **实验样本量小**：96/27/21/13 这一量级，27.7%、88% 之类比例的置信区间很宽，不能当"预测能力"；② **NLL 与实验结局的关系没有直接测**（正文只与回收率相关，图注 S3A），"用似然排序送前几十条"在本篇是**提议**而非验证；③ 救援实验都保留了原骨架，因此**无法回答"骨架生成器本身的失败率"**；④ 训练集是 PDB 装配体（3.5 Å、30% 聚类），对 PDB 罕见几何（富脯氨酸核心、非天然 fold）的可靠性由作者自己标注为"very few native proteins"，属于分布外；⑤ 正负 logits 的"多态设计"能力在本文**无实验结果**，与 [B01] 的三态开关没有形成闭环。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **"骨架固定、只换序列"的分诊协议**（第 2 节第 5 条）：候选酶若一轮失败，第一批补救应是**保留催化几何、只重设计外围/loop 序列**，并记录"换序列能救回多少"——这直接给出我们最缺的量：**序列问题 vs 几何问题的占比**。本库判据里可作为 G6（失败归因）的执行动作。
2. **免费排序量 + 批量小送测**（步骤 10/11）：每骨架出多条（高温增多样性），用一个模型内部分数排序，只送最前若干条。→ 我们的版本：每候选骨架用现有序列模型出 N 条变体、按似然排序，把预算压到"一轮、最多四个构建体"上（注意：这里的 N 与阈值本文未给，我们要自己标定）。
3. **算力单价必须与命中率一起报**（1.2 s vs 4.3 min、~1 s/骨架、>1 周人工）：任何新判据先给"每个通过闸口的候选花多少 CPU·s"，再决定上线。
4. **"指标与目标不一致"的自检**（第 2 节第 1 条）：把 Rosetta 式的代理优化对照到我们身上——我们的代理量（结构自洽、序列保守、能量项）与"三步化学事件是否发生"之间同样存在"缺乏一致性"的风险，必须显式列出代理量与终局量的差距，并在真值面板上量一遍。
5. **按任务分档选模型**（噪声档取舍）：我们若要"多而稳的候选"与"单条最像的候选"，应分别配置，不许用一个口径。

**不可迁移（为什么不能照搬）**

1. **序列回收率/对数似然不是酶活判据**。52.4%、NLL、AF 单序列 lDDT 全部是"序列是否编码这个骨架"的量，**与催化效率、底物选择性、竞争副产物无关**；本库判据 §2 明禁把此类阈值当酶活闸口。把 MPNN 分数当"能不能装酶设计"的分数是错的。
2. **96→73→50、88%/27.7% 不能当我们的成功概率**。它们是单体/组装体/binder 骨架上的**折叠与寡聚态**结果，分母极小、且样本是高度规整的人工骨架；天然参照酶的分布外情形本文没测。引用时只许引方法结构（分诊、排序、单价）。
3. **"residues required for function would clearly have to be kept fixed"是本文对催化位点的全部陈述**——它不是协议、没有精度指标、没有实验。想据此声称"锁住催化残基重设计其余部分可行"属于外推，需要自己的对照实验。
4. **本文没有 MD/QM/过渡态**，不能为"用 MD/QM 判催化"提供任何命中率背书（本文亦无任何化学选择性指标）。

## 9. 溯源与自检

- 本地纯文本：`data/interim/baker_lit/ft/proteinmpnn2022.txt`（Europe PMC `fullTextXML` → 标签剥离 → `litcards_text.norm` 归一化，未改写内容）。
- 引句底稿: data/interim/baker_lit/ft/proteinmpnn2022.txt
- 对照底稿行号：`sources/baker.md:68–79`（原卡，含 96/73/50、52.4%/32.9%、1.2 s/4.3 min 的原始摘录）、`sources/baker.md:604`（序列设计工具对照行）、`sources/baker.md:638`（做这一步的原因）。
- 原文指针：Table 1 在本地全文尾部以文字形式保留（"Baseline model None 1.381 mln 41.2/ 40.1 6.51/ 6.77 41.4/ 41.4" 等行），本卡消融数字取自该处；结构条目 8CYK 与图注口径（"2.35 RMSD over 130 residues"、"E-value=2.8 against UniRef100 using HHblits, TM-score=0.56 against PDB"）取自 Fig. 3 图注。
- 代码可得性（正文口径）："ProteinMPNN code is available at https://github.com/dauparas/ProteinMPNN"。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only B05 --no-report`（输入：本目录卡片 + 本编号登记的全文与底稿）；引句逐字比对结果见本次回报。
- 诚实声明：正文（作者手稿版）**没有 Methods 段落**（训练细节在 Supp Methods，本地未取得），故本卡第 3 节的"判据/阈值"列里凡涉及超参、采样温度数值、NLL 取前多少条的地方一律写"正文未给/原文未给阈值"，未做补全猜测。

<!--CSV回填
work_type=方法（deep learning 反折叠序列设计 + 跨体系架构扩展 + 失败设计救援的实验验证）
target=单体、均/异聚对称组装体、重复蛋白、C5/C6 环寡聚体、两组分四面体纳米颗粒（~1 MDa）、蛋白-蛋白界面与靶标结合体（Grb2 SH3 识别的富脯氨酸支架）；此前用 Rosetta 或 AlphaFold 设计失败的同批骨架
backbone_generation=本文不生成骨架；骨架沿用外部来源（AF/网络幻觉骨架、Rosetta 参数化束、已发表纳米颗粒骨架、RIFDOCK+Rosetta remodel 的 SH3 支架），由 ProteinMPNN 从骨架原子坐标（N/Ca/C/O/虚拟 Cb 距离、相对帧朝向、二面角）自回归出序列；顺序无关解码支持固定任意子集（如已知的靶序列），对称/重复/多链位置用 logits 平均耦合，多态设计用 logits 线性组合（正负权重，本文未做实验）
computational_filters=模型给出的序列平均对数概率（NLL，给定结构下的序列似然）用于批量排序送测；in silico 评估用 native sequence recovery（按埋藏度分档）与单序列 AlphaFold 复现骨架程度（lDDT-Ca 90/95 计数）；训练集筛选为分辨率/链长/聚类去冗余（物理能量项不作为闸口）
thresholds=训练集 <3.5 Å 分辨率、<10,000 残基、mmseqs2 30% 一致性聚类（25,361 簇）；邻域 32-48 最近 Ca 饱和；相对位置编码 ±32；训练噪声 std=0.02 Å 与 0.3 Å 档；评估用 AF 模型 average pLDDT>80.0、lDDT-Ca 95.0/90.0；NLL 排序的"取前 N 条"阈值=未记录（正文未给）；采样温度数值阈值=未记录（正文只给趋势）
md_used=否
qm_used=否
experimental_methods=E. coli 表达（合成基因/质粒）、Ni-NTA 纯化 + SEC 积分面积折算可溶产量（mg/L 培养等价）、SEC/SEC-MALS 定寡聚态、CD 波长扫描与热融化（至 95 °C）、X 射线晶体学（8CYK 单体、四面体颗粒）、cryoEM 与 negative stain EM 类平均、BLI（Grb2 SH3 结合 + 预测破坏点位突变负对照）
pipeline_counts=AF 幻觉骨架集 N=129：先用 AF 自序试表达 150 个蛋白（大多不溶，中位 9 mg/L）→ 同批骨架换 MPNN 序列下单 96 个设计 → 73 个可溶表达（中位 247 mg/L）→ 50 个为目标单体/寡聚态（SEC）；C5/C6 环寡聚体：Rosetta 序列 40% 可溶且 0 条寡聚态正确 → MPNN 序列 88% 可溶、27.7% 寡聚态正确；四面体颗粒：76 条序列覆盖 27 个骨架（每亚基 12 copies 耦合）→ 13 个形成预期 ~1 MDa 组装；in silico 集：402 单体对拍、690 monomers/732 homomers/98 heteromers 分层测试、396 个天然结构全重设计、NTF2 旧设计 3,000 骨架重设
hit_rate=天然骨架回收率 52.4%（MPNN）vs 32.9%（Rosetta）；救援实验成功率：AF 骨架集 73/96 可溶（76%）、50/96 目标寡聚态（52%）；环寡聚体 27.7% 寡聚态正确（对照 Rosetta 0%）；纳米颗粒 13/27 骨架成功组装（作者明说总体成功率与 Rosetta 原研究相当，收益在自动化与免人工干预）
best_metric=未记录（本文核心指标是可溶产量而非 Kd/活性：中位可溶产量 247 mg/L 培养等价（MPNN）vs 9 mg/L（AF 自序）；SH3 支架只给 BLI 信号"strong binding"与高于游离肽，未报 Kd；晶体一致性 2.35 Å/130 残基（8CYK）、颗粒界面 1.2 Å/两个完整不对称单元）
cost_or_stat_note=1.2 秒 vs 4.3 分钟（100 残基，出序列）；结论段另一口径 1.2 sec vs 258.8 sec（单 CPU、100 残基）；全自动 ~1 秒/骨架；旧纳米颗粒流程含 Rosetta 设计后 >1 周人工修正；模型参数 1.381→1.678 mln；样本量偏小（96/27/13），比例类结论的置信区间宽
role_in_timeline=解决 Rosetta 序列端的两个瓶颈——算力（约 200 倍加速）与界面/组装体失败率（直接救活此前 Rosetta 与 AF 自序的失败设计）；把"同骨架批量出序列 → 用模型似然排序 → 只送前几十条"变成 IPD 的标准动作（作者自述已成为组内默认序列方法），其 ~1 秒单价正是 [B09] efficiency 指标里"吞吐"那一侧、也是 ProteinMPNN-FR 加速 AF2 过滤漏斗的前提；对催化/功能位点只留了一句"功能残基需固定"的展望，未给协议
source_pointer=data/interim/baker_lit/ft/proteinmpnn2022.txt（Europe PMC PMC9997061 fullTextXML，2026-10-16 抓取）；sources/baker.md:68-79、604、638；代码 https://github.com/dauparas/ProteinMPNN；结构条目 PDB 8CYK
CSV回填-->
