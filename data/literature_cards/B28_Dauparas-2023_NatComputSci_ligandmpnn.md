# [B28] Atomic context-conditioned protein sequence design using LigandMPNN

Dauparas J, Lee G R, Pecoraro R, An L, Anishchenko I, Glasscock C, Baker D（华盛顿大学 IPD）
Nature Methods 2025, 22:717-723 · DOI 10.1038/s41592-025-02626-1 · PMID 40155723 · PMCID PMC11978504
收稿 2023-12-02，接受 2025-02-10，在线 2025-03-28 · 开放获取（CC BY 4.0）
（注：本文件名 slug 沿用早期登记的 2023 Nat Comput Sci 预印本命名；CSV 行 B28 与实际全文均为 Nature Methods 2025 正式版本体，按门禁要求不改名。）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B28**（组：Baker 组） |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory 记录 fetch_channel=epmc_fulltext，URL https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11978504/fullTextXML） |
| 本地全文 | `fulltext/B28_PMC11978504_fullTextXML.xml`（SHA-256 7e33fb90a1f61701…）→ 去标签纯文本 `fulltext/B28_PMC11978504_text.txt`（SHA-256 d12229cb63d27fd0…） |
| 对照底稿 | `sources/baker.md` 的 [B28] 摘要级卡片（登记时未抓全文；本卡已升级为全文级，摘要原句已在正文逐句核对） |
| 证据级别 | **全文级**（本卡全部引句可在 `B28_PMC11978504_text.txt` 里逐字命中；见第 9 节自检） |
| 未取到的部分 | Supplementary Figs 1-5、Source Data、Reporting Summary；参考文献 3-5（Huang 2024、Costello 2024、Rollauer 2024 等）的湿实验协议与逐靶命中率数字不在本文全文里，本卡凡引用处均明写"转引自 ref. 3-5" |

## 1. 这篇到底解决什么（大白话）

给蛋白质设计里的"第二步"换一个更好的工具：手里已经有骨架结构和一个**非蛋白配体**（小分子、核酸、金属离子）的三维位置，怎么自动写出能围绕这个配体形成结合口袋的氨基酸序列。此前深度学习序列设计（ProteinMPNN）只认蛋白骨架坐标，物理法（Rosetta）要为新配体手工写力场参数。LigandMPNN 把配体原子直接喂进图网络，顺带输出侧链构象和置信度。结果分两层：计算层是"贴着配体的残基还原天然序列"的回收率大幅领先（金属位 77.5% vs 36.0%/40.6%）；湿实验层是拿它**重设计** Rosetta 以前做失败的结合体，救回了不结合的 rocuronium 设计、把 cholic acid 结合体亲和力提高 100 倍（后者出自 ref. 4），外加转引 refs 3-5 的 >100 个实验验证界面与 5 个共结晶结构。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **现有深度学习方法压根不建模非蛋白原子**。现象/证据："current state-of-the-art deep-learning-based sequence design methods are unable to model nonprotein atoms and molecules"；具体到 ProteinMPNN："ProteinMPNN explicitly considers only protein backbone coordinates while ignoring any other atomic context, which is critical for designing enzymes, nucleic-acid-binding proteins, sensors and all other protein functions involving interactions with nonprotein atoms"。→ **应对**：在 ProteinMPNN 骨架图之外加两张图（配体内全连接图 + 蛋白-配体图）和两个额外编码器层，用物理直觉（范德华/静电是短程力，"within ~10 Å"）只取每个残基最近的 25 个配体原子："We obtained the best performance by selecting for the protein-ligand and individual residue intraligand graphs the 25 closest ligand atoms based on protein virtual Cβ and ligand atom distances"。代价：参数量 1.66M→2.62M，单序列耗时 0.6 s→0.9 s/100 残基，仍属轻量。
2. **训练数据里"蛋白-配体复合物"很少，能不能外推没底**。作者原话："At the outset, we were unsure whether the accuracy of ProteinMPNN could extend to protein-ligand systems given the small amount of available training data"。→ **应对**：先用逐蛋白回收率对比证明"对绝大多数配体数据够用"（"our results suggest that, for the vast majority of ligands, there are sufficient data"），再拿外推到训练分布外的成功案例背书——rocuronium 复合物不在训练集："there were no rocuronium-binding protein complex structures in the PDB training set"，而最接近的 PDB 胆酸结合体结构 "the cholic-acid-binding protein in the PDB that is closest to our cholic-acid-binding design (PDB: 6JY3 ) has a quite different structure (template modeling score 0.59) with a totally different ligand-binding location"。残留代价：对含稀有元素（如汞、铂类）的化合物仍不放心，"we suggest some care in using LigandMPNN for designing binders to compounds containing elements occurring rarely or not at all in the PDB"，且 "in the latter case it is necessary to map to the most closely occurring element"；低数据区怎么办，作者只给方向——"Hybridization of the physically based and deep-learning-based approaches may provide a better solution to the amino-acid and sidechain optimization problems in the low-data regime"——**本文未解决**。
3. **模型可能从局部几何"读出"天然序列（晶体记忆），而不是真学到配体-侧链关系**。→ **应对**：训练时对蛋白与配体坐标加高斯噪声去模糊细节："Protein and context atoms were noised by adding 0.1 Å standard deviation Gaussian noise to avoid protein backbone memorization 28"；消融显示噪声量直接改变成绩，"Training with 0.05 Å and 0.2 Å noise instead increased and decreased sequence recovery by about 2%, respectively"，并立了比较口径："when comparing performance across methods, similar levels of noising must be used"。代价：0.1 Å 是折中值，跨论文对比必须复刻这一设定才公平。
4. **侧链打包：chi3/chi4 预测基本失败**。现象/证据（图注与正文）：chi1 已经领先——"The median chi1 fraction (within 10° from crystal packing) near small molecules was 76.0% for Rosetta, 83.3% for LigandMPNN-wo and 86.1% for LigandMPNN"——但末端二面角崩塌："All the models struggle to predict chi3 and chi4 angles correctly"（小分子集 LigandMPNN 加权 chi1-chi4 为 84.0%/64.0%/28.3%/18.7%）。→ **应对**：本文没有修复它，只是如实报告并用"配位预组织"解释——去掉配体上下文（LigandMPNN-wo）chi1 只降约 3 个点，"most of the information about sidechain packing is coming from the protein context rather than from the ligand context, consistent with binding site preorganization"。**chi3/chi4 问题本文未解决**。
5. **Rosetta 时代留下的弱结合/不结合设计能不能救**。现象：为 rocuronium（此前完全测不到结合）和 cholic acid（结合极弱）做的 Rosetta 设计失败。→ **应对**：骨架和配体坐标不动、只用 LigandMPNN 重出序列，"LigandMPNN was used to generate sequences around the ligands using the backbone and ligand coordinates as input; these retain and/or introduce new sidechain-ligand hydrogen bonding interactions"，湿实验复测（酵母流式 + 荧光偏振）确认救回结合或提高亲和力，cholic acid 案例（转引 ref. 4）"starting from the crystal structure of a previously designed complex, LigandMPNN increased binding affinity 100-fold"。代价：主文只给了两个配体、每组 3（LigandMPNN）/2（Rosetta）次重复测量的证据规模，不是系统命中率。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **消息传递神经网络（MPNN）序列设计**：沿用 ProteinMPNN 架构（自回归编码器-解码器、随机解码序、21 类氨基酸 softmax + 温度采样），为的是把改动限定在"输入端加原子上下文"，从而能干净归因（对比训练数据完全相同的 ProteinMPNN 重训版，"For fair comparison, we retrained ProteinMPNN on the same training dataset of PDB biounits as LigandMPNN"）。
- **三张图**：蛋白图（残基节点 + N/Cα/C/O/虚拟Cβ 的 25 个成对距离）、配体内图（元素 one-hot 节点 + RBF 距离边）、蛋白-配体图（残基-最近配体原子距离与角度 sin/cos 特征）。加两个 protein-ligand 编码器层专司跨图消息传递。
- **侧链打包网络（同架构）**：序列定下后预测 chi1-chi4，"The model predicts a mixture (three components) of circular normal distributions for the torsion angles (chi1, chi2, chi3 and chi4)"，附 log-probability 置信度——这是"设计完先在线上看口袋合不合理"的抓手。
- **训练增广**："We augmented the training dataset by randomly selecting a small fraction of protein residues (2-4%) and using their sidechain atoms as context ligand atoms"——增广本身不提分（Supplementary Fig. 1b），但换来了第二能力："training in this way also enables the direct input of sidechain atom coordinates to LigandMPNN to stabilize functional sites of interest"（把想固定的功能位侧链当输入冻住）。
- **对照组与评测口径**：Rosetta（genpot；蛋白-DNA 专用能量函数；金属专用参数）、重训 ProteinMPNN；指标=贴配体残基天然序列回收率 + chi 角回收率；湿实验=酵母表面展示流式、荧光偏振（FP）、X 射线共结晶（多为转引 refs 3-5）。
- **没有用的方法**：MD、QM、结合自由能计算，全文不涉及。

### 工作流程表

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 | PDB 装配体（截至 2022-12-16） | 按分辨率/长度过滤后取复合物，mmseqs2 按序列聚类切分训练/测试集 | "LigandMPNN was trained on protein assemblies in the Protein Data Bank (PDB; as of 16 December 2022) determined by X-ray crystallography or cryo-electron microscopy to better than 3.5 Å resolution and with a total length of less than 6,000 residues"；切分 "The train-test split was based on protein sequences clustered at a 30% sequence identity cutoff"；配体侧剔 ["HOH","NA","CL","K","BR"] | 留出测试集："We evaluated LigandMPNN sequence design performance on a test set of 317 protein structures containing small molecules, 74 with nucleic acids and 83 with a transition metal" |
| 2 | 过滤后的 PDB 生物装配体（蛋白+配体坐标） | 三图特征化（每残基取最近 25 个配体原子）→ Adam 优化、categorical cross entropy，单卡 A100 训练序列设计模型 | 分辨率 3.5 Å、长度 <6,000 残基、30% identity 切分、输入噪声 0.1 Å、"Models were trained with a batch size of 6,000 tokens, automatic mixed precision and gradient checkpointing on a single NVIDIA A100 graphics processing unit for 300,000 optimizer steps" | LigandMPNN 2.62M 参数（ProteinMPNN 1.66M）；推理 0.9 s/100 残基/单 CPU |
| 3 | 同一训练框架 | 追加训练侧链打包网络（输入 backbone+配体+序列，输出 chi 角混合分布）；推理时温度 T 采样序列："During the inference, we sample from these probabilities with some temperate ( T )" | 每蛋白设计 10 条序列（正文评测口径）；采样温度数值阈值原文未给（正文只写"with some temperate ( T )"，未给具体 T） | 序列 + 每条序列的侧链构象与逐残基置信度（0-100） |
| 4 | 测试集 317/74/83 蛋白（天然骨架+配体） | in silico 基准：贴配体残基算天然序列回收率、chi1-chi4 回收率，与 Rosetta/ProteinMPNN/LigandMPNN-wo 对比 | 残基定义："We determined the native amino-acid residue sequence recovery for positions close to the ligand (with sidechain atoms within 5.0 Å of any nonprotein atoms)"；chi1 容差 10° | 回收率中位数：小分子 "The median sequence recoveries (ten designed sequences per protein) near small molecules were 50.4% for Rosetta using the genpot energy function 18 , 50.4% for ProteinMPNN and 63.3% for LigandMPNN"；核酸/金属 "For residues near nucleotides, median sequence recoveries were 35.2% for Rosetta 2 (using an energy function optimized for protein-DNA interfaces), 34.0% for ProteinMPNN and 50.5% for LigandMPNN, and for residues near metals, 36.0% for Rosetta 41 , 40.6% for ProteinMPNN and 77.5% for LigandMPNN"。**注意：这一步全部是计算指标，不含任何结合/催化功能测量** |
| 5 | 消融与增广变体（少/多噪声、去配体图、去元素类型、仅侧链上下文、变 25 原子数） | 逐项改变超参数/特征复跑第 4 步 | 原文给的效应量：噪声消融 "Ablating the protein-ligand and ligand graphs led to a 3% decrease in sequence recovery"（此为图消融）；元素特征 "a model trained without chemical element types as input features had much lower sequence recovery near metals"（8% difference，Supplementary Fig. 1d） | 结论：配体图贡献集中在金属位；细节在 Supplementary Fig. 1（本地未取） |
| 6 | Rosetta 旧设计中弱结合/不结合的 rocuronium 与 cholic acid 骨架（含配体坐标） | LigandMPNN 只重出序列（骨架不动），侧链-配体氢键保留或新增，然后湿实验复测 | 湿实验判据：酵母流式 "flow cytometry of yeast is shown, with the designs following incubation with 1 μM biotinylated rocuronium and streptavidin phycoerythrin"；FP 测 cholic acid-FITC；重复数 "The error bars show the mean and standard deviations for three LigandMPNN and two Rosetta measurements" | rocuronium 救回结合、cholic acid 提亲和力（Fig. 4）；ref. 4 案例 "starting from the crystal structure of a previously designed complex, LigandMPNN increased binding affinity 100-fold" |
| 7 | 外部研究（refs 3-5）把 LigandMPNN 当序列端 | 转引验证：小分子/DNA 结合蛋白设计与共结晶 | 成功口径=结合实验阳性 + 晶体结构与模型接近 | "In these studies, LigandMPNN was either used as a drop-in replacement for Rosetta sequence design retaining the backbone relaxation of RosettaFastDesign 38 , 42 , or used independently without backbone relaxation"；"more than 100 protein-DNA binding interfaces and protein-small-molecule binding interfaces designed using LigandMPNN have been experimentally demonstrated to bind to their targets"；"5 co-crystal structures have been solved that in each case are very close to the computational design models"（含 DNA 结合体 8TAC："The crystal structure of a DNA-binding protein designed with LigandMPNN recapitulated the design model closely"） |

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 63.3% / 50.4% / 50.4% | 小分子旁序列回收率中位数（LigandMPNN / Rosetta-genpot / ProteinMPNN） | 摘要给 "63.3% versus 50.4% and 50.5%"，正文两处 ProteinMPNN 为 50.4%——摘要与正文有一处 0.1-0.5 个点的出入，本卡两处都记 |
| 50.5% / 35.2% / 34.0% | 核酸旁序列回收率（LigandMPNN / Rosetta / ProteinMPNN） | Results 第二段 |
| 77.5% / 36.0% / 40.6% | 金属旁序列回收率（LigandMPNN / Rosetta / ProteinMPNN） | 摘要 "(77.5% versus 36.0% and 40.6%)" |
| 317 / 74 / 83 | 测试集蛋白数（含小分子/核酸/过渡金属） | Methods 与 Fig. 2 图注 |
| 3.5 Å / <6,000 残基 / 30% identity | 训练集过滤与训练-测试切分阈值 | Results 与 Methods |
| 0.1 Å；0.05/0.2 Å → ±~2% | 输入高斯噪声基线；改噪声对回收率的效应 | Results（ablation 段） |
| 25 原子 / ~10 Å | 每残基输入的近邻配体原子数；相互作用短程假设 | Results |
| 2.62M vs 1.66M；0.9 s vs 0.6 s | 参数量、100 残基单 CPU 推理耗时（LigandMPNN vs ProteinMPNN） | Results |
| 6,000 tokens / 300,000 步 / 1×A100 | 训练批次、优化步数与算力 | Methods |
| 2-4% | 侧链原子作上下文增广比例（不提分，但解锁功能位冻结输入） | Results |
| 86.1% / 83.3% / 76.0% | 小分子旁 chi1 回收率（LigandMPNN / LigandMPNN-wo / Rosetta） | Results |
| 84.0/64.0/28.3/18.7% | LigandMPNN 小分子集 chi1-chi4 加权回收率（Rosetta 74.5/50.5/24.1/8.1%） | Results；chi3/4 两者都差 |
| 3%；8% | 去蛋白-配体/配体图的回收率损失；去元素类型输入在金属旁的损失 | Results |
| 1 μM；3 / 2 次 | 流式所用生物素化 rocuronium 浓度；LigandMPNN/Rosetta 测量重复数 | Fig. 4 图注 |
| 100-fold | cholic acid 重设计亲和力提升（转引 ref. 4，起点是其晶体结构） | Results 第 4 段 |
| >100 / 5 个 / 4 个 | 实验验证结合界面总数（转引 refs 3-5）；共结晶结构数（正文）vs 摘要"four X-ray crystal structures"（差 1，正文含 DNA 蛋白 8TAC） | Discussion 与摘要对照 |
| ~250 倍 | 相对 Rosetta 的速度（绕开侧链身份蒙特卡洛优化） | Discussion |
| TM-score 0.59 | 6JY3 与胆酸设计骨架的差异（训练分布外泛化的证据） | Results |
| 10 条/蛋白 | in silico 评测与图注口径；推理温度 T 的具体数值全文未给 | Results 与 Methods |

## 5. 结论——作者说了什么

**in silico 层（计算指标，不是功能证据）**
1. 贴配体残基的天然序列回收率 LigandMPNN 显著高于 Rosetta 与 ProteinMPNN（小分子 63.3% vs ~50%；核酸 50.5% vs 34-35%；金属 77.5% vs 36-41%），且对绝大多数测试蛋白都更高；预测置信度与实际回收率相关。
2. 侧链打包：chi1/chi2 优于 Rosetta，但 "All the models struggle to predict chi3 and chi4 angles correctly"；LigandMPNN-wo 与完整版差距小，说明打包信息主要来自蛋白上下文（配位位点预组织）。
3. 比物理法快 ~250 倍、无需为新配体写参数。

**湿实验层（功能证据）**
4. 序列重设计能救回 Rosetta 弱/不结合设计（rocuronium 流式阳性、cholic acid FP 提升），ref. 4 里亲和力提升 100 倍。
5. 转引 refs 3-5：>100 个配体结合界面实验验证、5 个共结晶结构接近设计模型（DNA 结合体 8TAC 等），"This extensive biochemical and structural validation provides strong support for the power of the approach"。
6. 作者自限：稀有元素配体慎用；低数据区留给物理+DL 混合方案（本文未做）。**注意：全文没有给出任何"每个靶点设计 N 条测多少、中多少"的湿实验命中率**——回收率、chi 角都是 in silico 量，100 倍与 >100 验证是结合量，二者在本文中从未与"酶活"接触。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **两层证据强度完全不对称**：in silico 层有 317/74/83 蛋白的统计分布；湿实验层主文只有 2 个配体的 rescue 案例（重复 3/2 次），其余 >100 验证与 5 个结构全部转引自 refs 3-5，本文自己的表格给不出"送测序列数→命中数"的分母。所以引用本文时只能引"方法+案例"，不能引任何"命中率"。
2. **摘要与正文有两处数字不一致**（ProteinMPNN 小分子回收率 50.5% vs 50.4%；"four X-ray crystal structures" vs 正文 5 个 co-crystal），是出版过程中版本修订的残留——引用哪个都行但必须注明出处层级，这是"账面先于实测"式小坑的文献实例。
3. **温度采样无阈值**：正文只写 "with some temperate ( T )" 不给数值，意味着序列多样性/采样强度这一关键旋钮在本文口径下不可复现，实际复现要用 GitHub 代码默认值。
4. **"重设计救活旧骨架"是本文最有工程价值的结论**：骨架生成失败的代价可以用几乎免费的序列重采样（0.9 s/条级）来补救，这改变的是漏斗里"骨架 vs 序列"的责任划分，而不是绝对成功率。
5. 配体旁回收率高 ≠ 会结合：作者自己用 LigandMPNN-wo 的实验说明侧链打包主要靠蛋白上下文；同理，"贴着底物类似物的残基还原天然序列"也不能推断口袋功能。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：稀有/缺席元素化合物需映射到最接近元素、建议慎用；低数据区要物理法混合（未做）；chi3/chi4 预测失败；金属位之外的配体图贡献有限。
- 我们读出：①主文实验证据规模小（2 个 rescue 案例），泛化叙事依赖转引文献；②没有任何逐靶湿实验命中率/假阳性率，>100 是跨文献累计数，不能当单一漏斗的期望值；③评测协议（5.0 Å 定义、10 条/蛋白、0.1 Å 噪声、30% 切分）全是作者自定口径，跨论文对比需严格复刻；④Supplementary 未取，消融细节（25 原子数、层数、隐维）不可全量核验；⑤训练数据截至 2022-12-16，之后的冷冻电镜-配体结构未进模型；⑥全文无 MD/QM，对"结合后构象动力学/催化"不提供任何证据。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么做）**

1. **原子上下文序列设计这一步直接可用**：给定目标底物（或底物类似物）在候选活性位点的三维占位，用 LigandMPNN 出围绕底物的序列（10 条/骨架级成本，0.9 s/100 残基/单 CPU），比物理法便宜几个数量级，适合当漏斗的序列端量产器。
2. **失败候选的"零成本重审"**：对已判定不活/不结合的旧骨架，保持骨架与配体坐标冻结其催化关键侧链（2-4% 增广解锁的功能位输入能力），重出序列再测——这正是本文 rocuronium rescue 的操作。
3. **侧链构象 + 置信度当"结构假说生成器"**：把 chi1 与逐残基概率喂给后续 MD/QM 的起点搭建，减少盲采样；但只当先验，不当判据。
4. **比较口径纪律**：任何"我们的筛子 vs LigandMPNN 类工具"的对比必须同噪声水平、同数据切分——本文 "when comparing performance across methods, similar levels of noising must be used" 是方法学教训。

**不可迁移（为什么不能照搬）**

1. **配体旁序列回收率不是酶活判据**。回收率衡量的是"复现天然蛋白在该位点的氨基酸"，天然蛋白自身的催化效率本文从未测量；把它当酶活性阈值（或据此设通过率）没有依据，本库口径同样禁止把结构一致性分数当催化判据。
2. **"100-fold" 是结合亲和力（cholic acid binder，ITC/FP 量纲），不是催化提升**；把它写成"对酶活可提高 X 倍"属于跨量纲挪用，禁止。
3. **>100 实验验证与 5 个共结晶是结合/传感蛋白的证据，不是酶的**：本文全部湿实验对象无一个是催化剂，目标酶需要三步化学事件与竞争副反应的产物化学证据，本文不提供任何此类判据或命中率参照。
4. 本文无 MD/QM、无反应坐标、无过渡态建模，不能为机制层（键合距离/角度、自由能）主张引用它。
5. 训练集里不存在任何酶-底物复合物结构，对酶口袋而言模型处于分布外区——恰是作者自警的"低数据区"，只能按案例级先验使用，不能给概率。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/B28_PMC11978504_text.txt

- 本地纯文本由 Europe PMC fullTextXML 去标签生成（`litcards_text.norm` 同一实现：实体解码、弯引号/破折号统一、空白折叠）；本卡全部引句按该 norm 后的文本逐字复制（含 "function 18 , 50.4%" 这类参考文献编号留下的空格形态），不跨句拼接、不用省略号。
- 对照底稿：`sources/baker.md` [B28]（原为摘要级登记，摘要两句数字 63.3/50.4/50.5 与 77.5/36.0/40.6 已在正文核对，与正文 50.4/50.4 的差异记在第 4、6 节）。
- CSV 字段映射：第 3 节 ↔ 候选生成方法/计算筛选判据/阈值数字；第 4 节 ↔ 候选数递减/成本统计；第 5 节 ↔ 实验命中率（本文无，填未记录）；第 8 节 ↔ 在方法演进链的位置。
- **本卡自检**：`scripts/verify_literature_cards.py --only B28 --no-report` 逐字核验本卡全部引句；结果见本节末运行记录。未核验项：Supplementary 里的消融数字、refs 3-5 的原始实验细节（不在本底稿，卡内不引）。

<!--CSV回填
work_type=论文
target=小分子结合/传感蛋白、DNA 结合蛋白、金属结合位（固定骨架+配体坐标条件下的序列设计步骤）
backbone_generation=本文不生成骨架；骨架来自 Rosetta/RFdiffusion 设计与 PDB 天然结构，LigandMPNN 在固定骨架+非蛋白原子上下文上出序列与侧链构象（ProteinMPNN 架构 + 配体图/蛋白-配体图 + 两个额外编码层）
computational_filters=贴配体残基（侧链原子距非蛋白原子 ≤5.0 Å）天然序列回收率；chi1 角 10° 容差回收率；模型预测置信度（与回收率相关）；消融（噪声量、图/元素特征增删）对照
thresholds=训练集 better than 3.5 Å、<6,000 残基、30% 序列 identity 切分；输入噪声 0.1 Å；每残基 25 个近邻配体原子；~10 Å 短程假设；侧链增广 2-4%；评测 10 条序列/蛋白；采样温度原文未给数值阈值
md_used=否
qm_used=否
experimental_methods=主文：酵母表面展示+流式细胞术（1 μM 生物素化 rocuronium + 链霉亲和素-PE）、荧光偏振（cholic acid-FITC）、误差棒 n=3/2；转引 refs 3-5：结合测定与 X 射线共结晶（5 个结构，含 8TAC）
pipeline_counts=测试集 317 小分子 / 74 核酸 / 83 金属蛋白（每蛋白 10 序列）；主文湿实验 2 个配体 rescue；跨文献累计 >100 实验验证结合界面、5 个共结晶结构
hit_rate=未记录（全文未给逐靶湿实验命中率分母；回收率是 in silico 指标不可当命中率引用）
best_metric=结合亲和力提升 100-fold（cholic acid，转引 ref. 4，起点为其复合物晶体结构）；摘要级"high affinity"无统一 Kd 数值
cost_or_stat_note=推理 0.9 s/100 残基/单 CPU（ProteinMPNN 0.6 s）；比 Rosetta 快 ~250 倍；训练单张 A100、batch 6,000 tokens、300,000 优化步；参数 2.62M（vs 1.66M）
role_in_timeline=把序列设计端的条件从"仅骨架"升级到"全原子上下文"（骨架→序列两步分工的序列步换代）；为 Baker 组 2024 小分子结合体/传感器系列（refs 3-5）提供默认序列设计器；其 rescue 实验为"失败骨架换序列器重出"提供回溯性证据，与 [B10]/[B33] 的换设计器收益互证
source_pointer=data/literature_cards/fulltext/B28_PMC11978504_text.txt（SHA d12229cb63d27fd0…，Europe PMC fullTextXML）+ sources/baker.md [B28] 摘要卡
CSV回填-->
