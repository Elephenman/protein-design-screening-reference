# Baker 组：计算筛选漏斗与实验命中率（调研于 2026-10-16）

调研对象：University of Washington / HHMI / Institute for Protein Design（Institute for Protein Design, UW）David Baker 实验室及其合作者 2019–2026 年 de novo 蛋白设计工作。
证据级别说明：除特别标注"仅摘要级"外，所有数字均来自我用 Europe PMC REST `fullTextXML` 实际抓取的正文全文（本地缓存见 `..\data\interim\baker_lit\ft\`），每个 DOI 均已用 Crossref `/works/<doi>` 逐条核验（核验输出：`..\data\interim\baker_lit\verify.out`）。
核心问题回答（一句话）：Baker 组送湿实验前的筛选依据**不是** MD、也**不是** QM，而是"自洽性反折叠（AF2/RF 的 pLDDT / pAE_interaction / pTM / RMSD）＋ 序列模型似然（ProteinMPNN / LigandMPNN）＋ Rosetta 物理项（ddG / CMS / SAP）"这一套**计算漏斗**，再叠加**廉价高通量湿实验（酵母表面展示 + FACS + NGS、MP3-seq、SAPP 半自动表达纯化）**；QM 只出现在酶的过渡态（theozyme）与发色团光化学，MD 主要做事后机理解释，唯一一次成为闸口是 2024 年 buttressed-loop 重复蛋白论文（GROMACS 刚性检验，且与 AF/RF 并列可替换，见 [B34]），2019 年曾做过"MD+ML 可当筛选器"的探索（[B02]），2025 年 PLACER 论文明确以成本否弃它当主筛选器（[B19]）。

---

## 一、逐篇文献卡片

> 年标说明：Nature 系刊物常出现 **Crossref issued 年（在线发表年）≠ 卷期印刷年**（例如 10.1038/s41586-025-09721-5 的 Crossref issued=2025 而 EPMC pubYear=2026、卷 649；10.1038/s41592-025-02975-x issued=2025、卷 23；10.1038/s41586-024-08360-6 issued=2024、EPMC=2025、卷 638）。卡片里两处年份都按"在线年 / 刊期年"如实标注，卷页一律取自 Crossref 核验结果，不做推断。

### [B01] De novo design of bioactive protein switches
- 作者/单位: Langan R, Boyken S, Ng A, … Baker D（UF / UW-IPD）
- Nature, 2019, 572:205-210
- DOI: 10.1038/s41586-019-1432-8 ✅（Crossref 核验）  PMID 31341284 / PMCID PMC6733528
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC6733528/
- 设计对象/靶点: LOCKR（Cage–Latch–Key）别构开关，负载降解子/nuclear export 序列，用于哺乳细胞与酵母内源功能调控
- 候选生成方法: Rosetta 物理设计（五螺旋 Cage + Latch 界面 + Key 肽）
- 计算筛选器: 界面含 **buried hydrogen bond networks**（HBnet）用于调节 Cage–Latch 与 Cage–Key 相对亲和力；原文："we chose to design interfaces containing buried hydrogen bond networks; as in DNA base-pairing, specificity can be altered by minor changes to hydrogen bond donors and acceptors"（全文）；三态自由能模型（K_open / K_LT / K_CK）用于选择可调范围内的设计
- MD 使用: 否（全文仅提到磁搅拌培养管，无 MD）
- QM 使用: 否
- 实验验证方法与通量: 体外结合 + 酵母/HEK293T 报告基因；中低通量
- **命中率原始数字**: 原文摘要级证据："We describe orthogonal cage-key systems that function in vitro, in yeast and in mammalian cells with up to 40-fold activation of function by Key"（https://pubmed.ncbi.nlm.nih.gov/31341284/）。具体"设计 N 个/筛 M 个"的分母我未从正文提取到统一口径（见第五节缺口 1）
- 时间线位置: 2019 年的"物理能量函数 + HBnet 多态设计"终点；是 Rosetta 时代的最后一代复杂功能设计，其成本（大量人工筛选）正是后来深度学习要解决的瓶颈

### [B02] Improving the Efficiency of Ligand-Binding Protein Design with Molecular Dynamics Simulations
- 作者/单位: Barros E, Schiffer J, Vorobieva A, Dou J, **Baker D**, Amaro R（UCSD Amaro lab + UW-IPD）
- J. Chem. Theory Comput., 2019, 15:5703-5715
- DOI: 10.1021/acs.jctc.9b00483 ✅  PMID 31442033 / PMCID PMC7532806
- 链接: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7532806/（Europe PMC fullTextXML 返回 HTTP 500，故本卡片为**摘要级 + Crossref 元数据**）
- 设计对象/靶点: 配体结合蛋白（两种 fold、跨不同亲和力的 37 个设计变体）
- 候选生成方法: Rosetta 配体结合位点设计（既有 Baker 管线）
- 计算筛选器: 显式溶剂全原子 MD 轨迹特征 + 机器学习分类器
- MD 使用: **是，且是唯一一次把 MD 当潜在筛选器**——"Simulations ranging from 500 to 1000 ns per replicate were conducted on 37 designed protein variants … resulting in more than 180 μs of combined sampling"；"we demonstrate that the application of machine learning approaches built upon the output from the simulations can help discriminate between successful and failed binders, such that MD could act as a screening step in protein design, resulting in a more efficient process"（摘要，https://pubmed.ncbi.nlm.nih.gov/31442033/）；性质是**回顾性诊断**（"retrospective insights into the properties affecting ligand affinity"），并指出 entropic 成分对亲和力重要、而设计协议常用的经验模型难以纳入
- QM 使用: 否
- 实验验证方法与通量: 复用已有设计体的结合/稳定性测定，无新展示库
- 命中率原始数字: 37 个设计变体、>180 μs 累计采样（上引）；未报告新的湿实验命中率
- 时间线位置: 这是"MD 能否成为漏斗一环"的直接实验。**结论是否定的**：37 个体系 × 180 μs 的量级远不能覆盖 10^4–10^5 数量级的候选，2025 年 PLACER 论文（[B19]）明确以此为理由放弃 MD 改用生成式构象系综

### [B03] De novo protein design by deep network hallucination
- 作者/单位: Anishchenko I, Pellock S, … Baker D（UW-IPD）
- Nature, 2021, 600:547-552
- DOI: 10.1038/s41586-021-04184-w ✅  PMID 34853475 / PMCID PMC9293396
- 链接: https://pubmed.ncbi.nlm.nih.gov/34853475/（Europe PMC fullTextXML 亦 HTTP 500，本卡片**摘要级**）
- 设计对象/靶点: 全新小蛋白单体（序列与训练集中天然蛋白无关）
- 候选生成方法: 随机序列 → trRosetta 距离图 → 序列空间 Monte Carlo 最大化"幻觉对比度"（KL 散度）
- 计算筛选器: 网络预测的 distance map 置信度（后续版本即 pLDDT 型自洽判据）
- MD 使用: 否
- QM 使用: 否
- 实验验证方法与通量: E. coli 表达 + SEC + CD，X 射线/NMR 解析结构
- **命中率原始数字（摘要原文）**: "We obtained synthetic genes encoding **129** of the network-'hallucinated' sequences, and expressed and purified the proteins in Escherichia coli; **27** of the proteins yielded monodisperse species with circular dichroism spectra consistent with the hallucinated structures. We determined the three-dimensional structures of three … closely matched the hallucinated models."（https://pubmed.ncbi.nlm.nih.gov/34853475/）→ 送测 129、成功 27 ≈ **21%**
- 时间线位置: 把"筛选器"从物理能量函数换成**结构预测网络本身**的第一步；瓶颈是只能设计到 ~100 aa（[B08] 明确说 "in silico success rates rapidly deteriorate beyond this length"），且生成的是网络"记忆"内的 fold，骨架多样性受限 → 直接催生 diffusion 生成模型

### [B04] Protein sequence optimization with a pairwise decomposable penalty for buried unsatisfied hydrogen bonds
- 作者/单位: Coventry B, Baker D（UW-IPD）
- PLOS Computational Biology, 2021, 17(3): e1008061
- DOI: 10.1371/journal.pcbi.1008061 ✅  PMID 33684097 / PMCID PMC7971855
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC7971855/
- 设计对象/靶点: 通用序列设计环节（非特定靶点）
- 候选生成方法: Rosetta 组合侧链打包
- 计算筛选器: 新增**可两两分解的"埋藏未满足氢键"惩罚项**，可直接进入 combinatorial packing 打分
- MD: 否 / QM: 否（但该项的物理动机来自对天然蛋白中 buried unsatisfied polar group 罕见性的统计，非量子化学）
- 实验验证: 无新湿实验，属于能量函数/打分器改造
- 关键原文: "We show that inclusion of this term in Rosetta sidechain packing calculations substantially reduces the number of buried unsatisfied polar groups."（摘要）
- 时间线位置: Rosetta 时代"补物理项"的典型动作。同类上游锚点：Maguire J, Boyken S, Baker D, Kuhlman B, "Rapid Sampling of Hydrogen Bond Networks for Computational Protein Design", JCTC 2018, DOI 10.1021/acs.jctc.8b00033 ✅ (PMC5940506)；再早是 Boyken 2016 Science HBnet（DOI 10.1126/science.aad8865 ✅）。这一"埋藏极性必须成氢键"的判据后来被吸收进 ProteinMPNN/LigandMPNN 的序列似然与全原子打分中

### [B05] Robust deep learning–based protein sequence design using ProteinMPNN
- 作者/单位: Dauparas J, Anishchenko I, Bennett N, … Baker D（UW-IPD + Milner）
- Science, 2022, 378:49-56
- DOI: 10.1126/science.add2187 ✅  PMID 36108050 / PMCID PMC9997061
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC9997061/
- 设计对象/靶点: 单体、均/异聚组装体、蛋白-蛋白界面、 Previously failed Rosetta/AF2 设计
- 候选生成方法: 给定骨架 → MPNN 反折叠出序列（每骨架通常采 8 条）
- 计算筛选器: **序列对数似然（NLL / 平均 log probability）排序** —— "a measure of sequence quality derived from the ProteinMPNN, the averaged log probability of the sequence given the structure, correlated strongly with native sequence recovery over a range of temperatures, enabling rapid ranking of sequences for selection for experimental characterization"（全文 Results/Methods）
- MD: 否 / QM: 否
- 实验验证方法与通量: E. coli 表达 + SEC + CD + X 射线；96 个设计一批
- **命中率原始数字（全文）**："The success rate was far higher: of **96** designs produced in E. coli, **73** were expressed solubly (median soluble yield: 247 mg per liter of culture equivalent) and **50** had the target monomeric or oligomeric state as assessed by SEC"（→ 可溶表达 76%、目标态 52%）；"On native protein backbones, ProteinMPNN has a sequence recovery of **52.4%**, compared to **32.9%** for Rosetta"；"requiring only a small fraction of the compute time (**1.2 seconds versus 4.3 minutes** for 100 residues)"
- 时间线位置: 解决 Rosetta 序列设计**算力**瓶颈（200× 加速）与**界面/组装体失败率**瓶颈（直接救活此前 Rosetta 失败的设计）。它使"同一骨架批量出几百条序列 → 用似然排序 → 只送前几十条"成为标准动作

### [B06] Design of protein-binding proteins from the target structure alone
- 作者/单位: Cao L, Coventry B, Goreshnik I, … Baker D（UW-IPD 等 35 人）
- Nature, 2022, 605:551-560
- DOI: 10.1038/s41586-022-04654-9 ✅  PMID 35332283 / PMCID PMC9117152
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC9117152/
- 设计对象/靶点: 13 个靶点表面（12 个天然蛋白，含 HA、EGFR×2、PDGFR、IR、IGF1R、TIE2、IL-7Rα、CD3δ、TGFβ、VirB8）
- 候选生成方法: 全骨架 de novo（RIFdock 对接 + Rosetta 界面设计 + 片段组装 20-mer 螺旋束文库）
- 计算筛选器: **Rosetta ddG + contact molecular surface (CMS)** 为主判据；另有"快速预筛轨迹"预测每个设计能否通过阈值（sigmoid 拟合通过率）；"the designs observed experimentally to bind their targets tended to have stronger predicted binding energy and larger contact molecular surfaces"
- MD: 否 / QM: 否
- 实验验证方法与通量: **酵母表面展示 + 多轮 FACS + 深度测序**（pooled 设计库），再对富集设计做 SSM（site saturation mutagenesis）结合指纹与组合突变库；"Combinatorial libraries were purchased as Integrated DNA Technologies ultramers, with the final DNA diversity ranging from **1 × 10^6 to 1 × 10^7**"；"the libraries were sorted … collecting only the **top 0.1%** of the binding population"
- **命中率原始数字（全文）**："Using the above protocol, we designed **15,000–100,000 binders for each of the 13 target sites**"；"Experimental data on **nearly half a million computational designs** and hundreds of thousands of point mutants…"；"CPU time requirements to produce 100,000 designed binders to be tested experimentally were typically around **100,000 CPU hours** (usually **at least ten times as many binders were computationally designed than were ordered**)"；"For some (FGFR2 and PDGFR), **hundreds** of binders were generated, whereas for others (TIE2 and CD3δ), **fewer than 10 binders were obtained from libraries of 100,000 designs**"（→ 约 10^-4 量级命中率）；"Only a small fraction of designs bind, and in almost all cases, the best of these require additional substitutions to achieve high-affinity binding"；结合功能验证："most (9 out of 13) were stable at 95 °C"；VirB8 结合体 510 pM
- 时间线位置: 这是"**用昂贵计算 + 更贵湿实验硬堆通量**"的极限样本，也是后续所有漏斗论文的基准数据集（[B09] 就是拿它的 ~100 万条实验标注训练/评估筛选器）。它暴露的瓶颈——每靶点十万级设计、千分之一以下命中、必须再进化亲和力——正是 RFdiffusion + AF2 过滤要打的靶

### [B07] Sampling of structure and sequence space of small protein folds
- 作者/单位: Linsky T, Noble K, Tobin A, Crow R, Carter L, Urbauer J, **Baker D**, Strauch E（UW/OSU）
- Nature Communications, 2022, 13:7151
- DOI: 10.1038/s41467-022-34937-8 ✅  PMID 36418330 / PMCID PMC9684540
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC9684540/
- 设计对象/靶点: 8 种小蛋白 fold 的形状多样性采样（含 thioredoxin 最小化）
- 候选生成方法: Rosetta 蓝图/fragment 组装 + 序列设计
- 计算筛选器: Rosetta 能量、埋藏极性/堆积质量类判据（物理打分主导）
- MD: 仅出现在参考文献（PDBMD2CD），正文未用 MD 筛选 / QM: 否
- 实验验证: E. coli 高通量表达 + SEC/CD 稳定性测定
- **命中率原始数字（摘要）**："We designed and evaluated stability of about **30,000** de novo protein designs of eight different folds. Among these designs, about **6,200 stable proteins were identified**"（→ **≈20.7%** 计算通过→实验稳定的对照率）
- 时间线位置: 提供"纯 Rosetta 时代 fold/稳定性设计 ~20% 命中、三万数量级投入"的量化锚点，与 [B05] 的 96→73→50 一起构成分母基线

### [B08] De novo design of protein structure and function with RFdiffusion
- 作者/单位: Watson J, Juergens D, Bennett N, Trippe B, … Baker D（UW-IPD）
- Nature, 2023, 620:1089-1100
- DOI: 10.1038/s41586-023-06415-8 ✅  PMID 37433327 / PMCID PMC10468394
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC10468394/
- 设计对象/靶点: 全新 fold（TIM barrel、NTF2）、对称组装体、Ni²⁺ 金属位、5 个蛋白靶点结合体（Influenza A H1 HA、IL-7Rα、InsR、PD-L1、TrkA）+ MDM2 螺旋肽结合体
- 候选生成方法: RFdiffusion（在 RoseTTAFold 权重上微调的扩散模型）生成骨架 → ProteinMPNN 设计序列（"typically sampling eight sequences per design"）
- 计算筛选器: **AF2 自洽性**（复合物 + 单体），原文："Designs were filtered by AF2 confidence in the interface and monomer structure, and **95 were selected for each target** for experimental characterization"；in silico 成功定义："the proportion of designs for which AF2 yields a prediction from a single sequence that has **mean pLDDT > 80 and backbone r.m.s.d. < 2 Å**（到设计模型）"，并对参考 fold 加 TM-score 判据；界面侧另用 AF2 界面 pAE（呼应 [B09]）
- MD 使用: 否 / QM 使用: 否（Ni 位用理想配位几何，未做量子化学）
- 实验验证方法与通量: **E. coli 表达 + 单点 BLI（10 μM）**，每个靶点只测 <100 个设计——刻意不走展示库
- **命中率原始数字（全文）**："The overall experimental success rate, defined as binding at or above 50% of the maximal response for the positive control, was **19%**"；"e, Out of **95** designs, **55** showed binding to MDM2 (more than 50% of maximum response)"；金属酶模拟："We expressed and purified **44** designs … **37** had SEC chromatograms consistent with the intended oligomeric state … Of the designs, **36** were tested for Ni²⁺ coordination by ITC, and **18** were found to bind Ni²⁺ with dissociation constants ranging from low nanomolar to low micromolar"；对比前代："For IL-7Rα, InsR, PD-L1 and TrkA, RFdiffusion has success rates roughly **two orders of magnitude higher** than the original design campaigns. We attribute one order of magnitude to RFdiffusion, and the second to filtering with AF2 (estimated success rates for previous campaigns if AF2 filtering had been used: HA, 0%; IL-7Rα, 2.2%; InsR, 5.5%; PD-L1, 3.7%; TrkA, 1.5%)"；"Binders were identified for all five targets, with **fewer than 100 designs tested per target compared to thousands in previous studies**"；in silico："In silico success rates were **42.5 and 54.1%** for TIM barrels and NTF2 folds"；"high-affinity binders can be identified from dozens of designs, in many cases **eliminating the requirement for slow and expensive high-throughput screening**"
- 时间线位置: 分水岭。生成端解决"骨架多样性/界面形状互补"，筛选端解决"物理打分判不出会折叠的结合体"；成本结构从"十万设计 + 展示库"变成"约百设计 + 96 孔 BLI"

### [B09] Improving de novo protein binder design with deep learning
- 作者/单位: Bennett N, Coventry B, Goreshnik I, Huang B, … Baker D（UW-IPD）
- Nature Communications, 2023, 14:2625
- DOI: 10.1038/s41467-023-38328-5 ✅  PMID 37149653 / PMCID PMC10163288
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC10163288/
- 设计对象/靶点: LTK、ALK、IL-2Rα site1/site2、IL-10Rα（4 个新靶 + 10 靶回顾集）
- 候选生成方法: Rosetta 设计协议（Cao 2022 管线）出骨架，Rosetta LayerDesign 或 ProteinMPNN 出序列，AF2/RF2 复测
- 计算筛选器: **pAE_interaction < 10 + 复合物 Cα RMSD < 5 Å**（AF2/RF2 界面预测对齐误差），辅以 target_delta_sap、ddG、contact_patch、contact_molecular_surface
- MD: 否 / QM: 否
- 实验验证方法与通量: 合成基因 → 酵母表面展示（先 1 μM + avidity 分选，再递减浓度分选）→ 可溶表达 + BLI/SPR
- **命中率原始数字（全文）**：回顾集 "the set of **~1 million** experimentally characterized designs for 10 different targets described in Cao et al."；"**15,000–100,000 designs were experimentally tested for each target, and the number of actual binders ranged from 1 to 584**"；前瞻："we generated computational libraries of **~2 million designs for each target** and filtered these down to **~20,000 designs** to be experimentally tested for each target: ~15,000 designs using the physically based filters of Cao et al. and ~**5000** designs with **AF2 pAE_interaction <10**"；"Synthetic genes were obtained for the **~80,000** designs"；"increases design success rates nearly **10-fold**"；"Physically based filtering yielded successful binders for two targets (LTK, IL-2Rα site1); for these the AF2-filtered libraries had **8- and 30-fold higher** success rates"；"the AF2 filter is computationally expensive (~**30 GPU-seconds per design**) and only **~2.3%** of designs pass"；最终池规模 "pools of sizes 9 K (Rosetta-Rosetta), 2 K (Rosetta-AF2), and 2 K (ProteinMPNN-AF2)"；自我限制："success rates among the targets remain **low (<1%)** and no binders were identified to Site 2 of IL2 receptor-ɑ"
- 时间线位置: 把 [B06] 的近百万条湿实验标注变成『筛选器训练/评估集』，第一次给出『漏斗该用哪个判据』的定量答案，并把失败归因结构化（Type I / Type II）；其结论（AF2/RF2 界面 pAE_interaction 是最强判据、阈值 10）直接成为 [B08] 之后所有 binder 论文的默认闸口，其暴露的成本（30 GPU-秒/设计、仅 2.3% 通过）则催生 [B05]/[B28] 的序列端加速。
- 失败机理分类（该文最有价值的概念）：**Type I 失败 = 设计态与 AF2/RF2 复测结构不一致（根本没折成/没结合构象）**；**Type II 失败 = 折叠与结合模式都对、但亲和力不够**，"Type II errors are primarily responsible for the low success rates of Cao et al."。→ 明确回答了"为什么会失败"

### [B10] De novo design of luciferases using deep learning
- 作者/单位: Yeh A, Norn C, Kipnis Y, Tischer D, Pellock S, … Baker D（UW-IPD）
- Nature, 2023, 614:774-780
- DOI: 10.1038/s41586-023-05696-3 ✅  PMID 36813896 / PMCID PMC9946828
- 设计对象/靶点: 能催化 DTZ/CTZ 发光的全新 luciferase（新反应、新骨架）
- 候选生成方法: NTF2 超家族库 hallucination + family-wide hallucination 生成 1,615 scaffold → 序列设计（Rosetta / 后期 ProteinMPNN）
- 计算筛选器: 配体结合能（Rosetta ddG）、**蛋白-配体氢键**、shape complementarity、contact molecular surface；第二轮加入 **AF2 pLDDT > 92** + Cα RMSD + CMS + Rosetta 能量
- MD 使用: **是，但仅做事后机理**——"We used a combination of density functional theory (DFT) calculations and molecular dynamics (MD) simulations to investigate the basis for LuxSit activity in more detail"（Extended Data，非筛选环节）
- QM 使用: **是，用于化学步**——"Density functional theory calculation suggested that the formation of an anionic state is the essential electron source for the activation of triplet oxygen (³O₂)"；"The free-energy profile calculated by density functional theory shows triplet oxygen can react directly with the anionic species of DTZ (Int1) through the reactant complex Int2 and TS1. The dioxetane intermediate Int3 then cleaves in an open shell singlet transition state OSS TS2…"；设计逻辑本身仍是 theozyme/transition-state 匹配："Computational enzyme design generally starts from an ideal active site or theozyme consisting of protein functional groups surrounding the reaction transition state"
- 实验验证方法与通量: 池式寡核苷酸文库 + 荧光素酶发光筛选（第一轮），第二轮 E. coli 表达 46 个
- **命中率原始数字（全文）**："After sequence optimization, the designs were filtered … and **7,648** designs were selected and ordered as pooled oligos for experimental screening" → 第一轮 **3/7,648**；"After filtering on the basis of the AlphaFold2-predicted pLDDT, Cα RMSD, contact molecular surface and Rosetta-computed binding energies, we selected and experimentally expressed **46** designs in E. coli" → 第二轮 **2/46**；原文自评："The success rate increased from **3/7,648 to 2/46** sequences in the second round, probably owing to the knowledge of active-site geometry from the first round and the increased robustness of the ProteinMPNN method"；最终 LuxSit-i "has higher activity than any previous de-novo-designed enzyme, with a k_cat/K_m (10⁶ M⁻¹ s⁻¹) in the range of native luciferases"
- 时间线位置: 深度学习进入**功能（催化）设计**的开端；同时暴露旧范式代价（7,648 送测才中 3 个）→ 直接引出"需要能筛'活性位预组织'的便宜打分器"，即 PLACER / [B18][B19][B21]

### [B11] De novo design of small beta barrel proteins
- 作者/单位: Kim D, Jensen D, Feldman D, … Baker D（UW-IPD）
- PNAS, 2023, 120: e2207974120
- DOI: 10.1073/pnas.2207974120 ✅  PMID 36897987 / PMCID PMC10089152
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC10089152/
- 设计对象/靶点: SH3、OB、以及 5/6 链 up-and-down β barrel（b5、b6）等 <70 aa 小 β 桶
- 候选生成方法: Rosetta fold-assembly/蓝图 vs 深度学习骨架生成（hallucination/RF 类）+ Rosetta 序列设计
- 计算筛选器: 折叠匹配、β 配对/β-bulge、聚集倾向；DL backbone + Rosetta sequence 组合
- MD: 否 / QM: 否
- 实验验证: E. coli 表达 + Ni 柱纯化 + SEC + far-UV CD + ¹H-¹⁵N HSQC NMR
- **命中率原始数字（全文）**："**72 out of 80** designs expressed, **43** were soluble, and **19** and **9** appeared to be monomers and dimers by size exclusion chromatography"；"**Eleven** monomers and **five** dimers had far-UV CD spectra suggesting folded structures, and **11** designs had close to the expected number of well-dispersed sharp peaks from ¹H-¹⁵N HSQC"；失败模式："Indeed, **74 percent** of the soluble experimentally characterized designs were oligomers, and **40 percent** of the expressed designs aggregated"；结论："Using deep learning for backbone generation and Rosetta for sequence design yielded higher design success rates and increased structural diversity than Rosetta alone"
- 时间线位置: 说明漏斗失败原因的另一种维度——不是打分不准，而是**β 边缘聚集/寡聚**这类设计目标之外的路径；"表达→可溶→正确寡聚态→折好的谱学证据"的四段漏斗在此被完整量化（80→72→43→28 单体/二聚体→16 CD 折叠）

### [B12] De novo design of high-affinity binders of bioactive helical peptides
- 作者/单位: Vázquez Torres S, Leung P, Venkatesh P, Lutz I, … Baker D（UW-IPD；Nat 2024, 626:435-442）
- DOI: 10.1038/s41586-023-06953-1 ✅（Crossref 年标 2023 在线/2024 刊期）  PMID 38109936 / PMCID PMC10849960
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC10849960/
- 设计对象/靶点: PTH、GCG、NPY、Bid 等 α-螺旋肽（含 PPII/无序起始信息）
- 候选生成方法: Rosetta 18,000 螺旋束文库筛选 + hallucination 序列空间 Monte Carlo + RFdiffusion / RF joint inpainting，序列由 ProteinMPNN 设计，AF2 with initial guess 复测
- 计算筛选器（明确阈值，全文原文）: "Both rounds had gate filters of **interface pAE < 10, mean pLDDT > 92, pTM > 0.8 and RMSD to input backbone < 1.75 Å**"；"Precise metrics cutoffs changed for each design campaign to get to an orderable set, but largely focused on **pAE (<10), pLDDT (>80) and Rosetta ddG (<−40)**"；另加 membrane-insertion potential、contact_molecular_surface、monomer pAE；"Sixty-four sequences were designed per backbone … filtered on the basis of AF2 pLDDT, pTM, RMSD to the design model, RMSD of the monomer … and Rosetta ddG. The precise values used for filtering were chosen **to reduce the set down to 46 designs**" / "to reduce the set down to **96 designs for each target**"
- MD: 否（唯一一句相关：承认传统方法需要 "extensive full-atom calculations … using molecular dynamics simulation or Rosetta full-atom relaxation"，而 DL 方法绕开它）/ QM: 否
- 实验验证: 酵母表面展示 + BLI；NanoBiT split-luciferase 结合/生物传感
- **命中率原始数字（全文）**："Out of **192** designs tested, **44** showed binding against PTH in initial yeast display screening"；"Initial screening with yeast surface display revealed quite high binding success rates, with **25 out of 96** designs binding GCG, and **20 out of 96** binding NPY at 10 nM peptide concentration"；hallucination 支路："We experimentally tested **46** of the Hallucinated designs"；螺旋肽模板预筛："12 designs for each target … 3, 4 and 8 out of 12 to PTH, GCG and NPY, respectively, but with only **micromolar** affinities"；结构改进量化："the average contact molecular surface for the partially diffused GCG binders and NPY increased by **33% and 29%** … and the Rosetta ddG improved by **29% and 21%**"
- 时间线位置: 把 [B08]/[B09] 的漏斗标准化成**多闸口 (gate) + 目标池规模反推阈值**的工程实践（阈值不是物理意义，而是"把集合削到可下单的 46/96 个"）

### [B13] Generalized biomolecular modeling and design with RoseTTAFold All-Atom
- 作者/单位: Krishna R, Wang J, Ahern W, … Baker D（UW-IPD）
- Science, 2024, 384: eadl2528
- DOI: 10.1126/science.adl2528 ✅  PMID 38452047（无 PMC，本卡片**仅摘要级**）
- 链接: https://www.science.org/doi/10.1126/science.adl2528
- 设计对象/靶点: digoxigenin（地高辛）、heme、bilin 等小分子/辅因子结合蛋白
- 候选生成方法: RFAA 建模 + **RFdiffusionAA**（全原子扩散，围绕小分子生成蛋白）
- 计算筛选器: 全原子（非残基级）复合物置信度，取代"只表示蛋白"的 AF2 自洽
- MD: 否 / QM: 否（摘要层面）
- 实验验证: X 射线晶体学 + 结合测定
- 关键原文（摘要）: "Starting from random distributions of amino acid residues surrounding target small molecules, we designed and experimentally validated, through crystallography and binding measurements, proteins that bind the cardiac disease therapeutic digoxigenin, the enzymatic cofactor heme, and the light-harvesting molecule bilin"（https://pubmed.ncbi.nlm.nih.gov/38452047/）；未给出 N/M/命中率数字（见缺口 2）
- 时间线位置: 全原子化转折的方法学底座。此前 AF2/RF2 无法评估金属、辅因子、共价修饰，导致小分子/酶设计的"筛选器失效"；RFAA→LigandMPNN→RFdiffusion2/3 把漏斗延伸到原子层

### [B14] Target-conditioned diffusion generates potent TNFR superfamily antagonists and agonists
- 作者/单位: Glögl M, Krishnakumar A, Ragotte R, … Baker D（UW-IPD + Harvard）
- Science, 2024, 386:1154-1161
- DOI: 10.1126/science.adp1779 ✅  PMID 39636970 / PMCID PMC12416549
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12416549/
- 设计对象/靶点: TNFR1、TNFR2、4-1BB、OX40（TNFR 超家族，拮抗与激动，含寡聚态依赖性）
- 候选生成方法: 自由扩散（free diffusion）+ **partial diffusion（从中间时间步重采样）**做局部优化
- 计算筛选器: "the predicted structure was already close to the final structure at around **timestep 120 out of 200**"；"We generated **25,000 partially diffused backbones** around each starting structure, and following ProteinMPNN, the **32 designs for each starting structure** which AF2 most confidently predicted bound TNFR1 in the designed binding mode (**pae_interaction < 5**) were selected"；主闸口 "**interface pae < 7.5** 且 **pLDDT > 85**"
- MD: 否 / QM: 否
- 实验验证: E. coli / 昆虫细胞表达 + BLI + 细胞报告基因（agonism/antagonism）
- **命中率原始数字（全文）**："Most (**94 out of 96**) of the designs were expressed at high levels, and **30% (28 out of the 94 expressed designs)** bound TNFR1"；"For TNFR2, **1323** designs had AF2 complex predictions with pae_interaction <7.5—a substantially higher success rate than achieved by free diffusion on TNFR1"；"For TNFR2, **32%** of the designs bound with high specificity; the highest affinity design had a K_D of **198 pM**"；"For 4–1BB … the experimental success rate was still high, with **22 out of 48** tested designs binding specifically, with the highest affinity of **44 nM**"；方法学自评："The number of sequences tested (96 free diffusion and 96 partial diffusion designs for TNFR1, and 48 partial diffusion designs for TNFR2, OX40, and 4–1BB) is **far fewer than in previous studies in which libraries of tens of thousands of designs were screened using yeast display**, and no random or experimentally guided optimization was involved"
- 时间线位置: 把漏斗从"生成-筛选"升级为"**生成-筛选-再生成（partial diffusion 作为廉价局部优化器）**"；4 靶点、总送测 <350 序列即拿到 pM 级激动/拮抗剂，是"Baker 组自己报告的实验成功率"里最漂亮的一组（30%/32%/46%）

### [B15] Accurate de novo design of high-affinity protein-binding macrocycles using deep learning（RFpeptides）
- 作者/单位: Rettie S, Juergens D, Adebomi V, … Baker D（UW-IPD + ChromaDex/其他）
- Nature Chemical Biology, 2025, 21:1948-1956
- DOI: 10.1038/s41589-025-01929-w ✅  PMID 40542165 / PMCID PMC12643943
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12643943/
- 设计对象/靶点: MCL1、MDM2、GABARAP、Rhombotarget A（RbtA）
- 候选生成方法: RFpeptides（环肽扩散）生成 10,000–20,000 骨架（16–18 aa）+ ProteinMPNN/Rosetta Relax 迭代出序列（每条骨架 4–8 序列）
- 计算筛选器（阈值齐全）: **AfCycDesign** iPAE（"<0.13" / "<0.3" / "<0.4" 三档按靶点调）+ **Rosetta ddG（<−30 或 <−50 kcal/mol）+ SAP < 35 + CMS > 300 Å²**；t-SNE/TM-score 结构聚类去冗余
- MD: 否 / QM: 否
- 实验验证: 化学合成（HPLC 纯度 >90%）+ SPR 单周期动力学 + AlphaScreen + X 射线共晶
- **命中率原始数字（全文）**："We generated **10,000** macrocycle backbones … designed four amino acid sequences for each" → "After strictly filtering … we selected **27** designs for synthesis"；MDM2："**20,000** backbones … Of the resulting **80,000** design models, we selected **335** macrocyclic designs on the basis of AfCycDesign (iPAE < 0.13) and Rosetta (ddG < −30 kcal mol⁻¹, SAP < 35 and CMS > 300 Å²)"；关键的成本动作："**Instead of trying to synthesize and characterize all 335 cyclic peptides (which would have required substantial time and experimental resources), we clustered the 335 designs into 80 different clusters** … and selected representative designs from diverse clusters" → 各靶点 "we identified **17** designs with iPAE < 0.3, ddG < −50 …; We selected **11** top-ranked designs by ddG"；"We successfully synthesized **six** designs … tested them for binding to GABARAP"；结果："We tested **20 or fewer** designed macrocycles against each of four diverse proteins and obtained binders with medium to high affinity against all targets … a high-affinity binder (K_d < 10 nM) [to RbtA]"；自评："Despite testing fewer than 20 designed candidates per target (in contrast to **trillions of peptides tested in traditional library-based approaches**), we achieved high-affinity binders for two targets without requiring any further experimental optimization; to our knowledge, this is a considerably higher success rate than achieved with any previous method"
- 时间线位置: 首次把漏斗套到**化学合成**（而非生物表达）候选上，成本约束从"表达通量"变成"合成通量"，于是新增**结构聚类去冗余**这一层（用 80 个代表代替 335 个下单）

### [B16] Massively parallel measurement of protein–protein interactions by sequencing using MP3-seq
- 作者/单位: Baryshev A, La Fleur A, Groves B, Michel C, **Baker D**, Ljubetič A, Seelig G（UW-IPD + UCSD）
- Nature Chemical Biology, 2024, 20:1514-1523
- DOI: 10.1038/s41589-024-01718-x ✅  PMID 39192093 / PMCID PMC11511666
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC11511666/
- 设计对象/靶点: 设计的 coiled-coil（1×1、2×2、1×2）异二聚体、Bcl-2 家族设计抑制剂、PUMA 肽、以及天然 PPI
- 候选生成方法: 既有设计体（本论文卖点是**测**不是设计）
- 计算筛选器: 条形码配对富集倍数（LFC）+ 多重检验校正（P_adj ≤ 0.05）；另用 AF-M（AF2 多链）iPTM 作为计算对照
- MD: 否 / QM: 否
- 实验验证方法与通量: 重编程酵母双杂交（Y2H）+ 条形码 + NGS
- **通量/命中率原始数字（全文）**："**MP3-seq can measure over 100,000 PPIs in a single experiment**"；"We show that MP3-seq is highly quantitative and scales to over 100,000 interactions"；设计侧对照："**Every design set had an approximately 20% success rate in the largest screen, consistent with past 22% success rates for α-helical bundles**"；验证集规模："we screened **144** pairwise interactions between six orthogonal 1×1s"；"six homologous proteins from the Bcl-2 family … and **nine de novo designed inhibitors**"
- 时间线位置: 把"每个设计的 Kd/特异性"变成 **~10⁵ 对/实验** 的可测序数据 → 既是廉价筛选器，也是回头训练/校正打分函数（[B27]）的数据引擎

### [B17] Computational design of serine hydrolases
- 作者/单位: Lauko A, Pellock S, Sumida K, Anishchenko I, Ahern W, … Baker D（UW-IPD + UCSF/其他）
- Science, 2025, 388: eadu2454
- DOI: 10.1126/science.adu2454 ✅  PMID 39946508 / PMCID PMC12288761
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12288761/
- 设计对象/靶点: 4-甲基伞形酮（4MU）酯水解，Ser-His-Asp/Glu 催化三元体（含 acyl-enzyme intermediate, AEI）
- 候选生成方法: RFdiffusion 骨架（围绕催化几何）+ LigandMPNN/FastRelax 序列 + 迭代 redesign（round 1→8）
- 计算筛选器: 第一轮只用 **AF2（RMSD/置信度 + 要求所有催化氢键在 AF2 预测中形成）**；第二轮起用 **PLACER 系综**判"预组织"："round 2 designs that passed the AF2 filter were selected for experimental screening if PLACER ensembles of the apo state indicated the key Ser-His hydrogen bond was formed"；再后按反应坐标 2 态/4 态过滤
- MD 使用: **不作为筛选器，被显式否弃**（方法学理由见 [B19]）
- QM 使用: **是，用于化学步**："To generate active site motifs, we placed the catalytic sidechains around a **QM-optimized transition state** (see Computational methods)"
- 实验验证: E. coli 表达 + FP（fluorophosphonate）探针标记 + 酯酶/酰胺酶动力学（kcat/KM）+ X 射线晶体
- **命中率原始数字（全文）**："**Only 1.6%** of round 2 designs that passed the AF2 RMSD filter were predicted to be preorganized by PLACER"；"We obtained genes encoding **45** two-state filtered designs … and found **38 (84%)** labeled with FP-probe"；"Of the **11** four-state filtered designs tested, **10 (91%)** labeled with FP-probe"；"of **20** designs tested, **two** displayed significant esterase activity, with catalytic efficiencies of 180 and 1400 M⁻¹ s⁻¹"；"Of **65** designs tested, **all** showed activity, and one design, r7-momi120, displayed a catalytic efficiency of 4300 M⁻¹ s⁻¹"；"Of the **150** designs screened, the two most active … showed 8-fold and 7-fold improvements in k_cat over the parent design r3-super (k_cat = 0.00137 s⁻¹)"；总规模："PLACER ensembles of all **812** experimentally characterized designs, categorized as inactive, FP probe labeling, acylation, and catalytic turnover"
- 时间线位置: 酶设计第一次"零到零"跑通（多步机制 + AEI 水解），关键杠杆是把筛选判据从"静态结构一致"换成"**沿反应坐标的构象系综预组织**"

### [B18] Computational design of metallohydrolases
- 作者/单位: Kim D, Woodbury S, Ahern W, … Baker D（UW-IPD）
- Nature, 649:246-253（Crossref issued=2025，EPMC pubYear=2026）
- DOI: 10.1038/s41586-025-09746-w ✅  PMID 41339547 / PMCID PMC12727532
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12727532/
- 设计对象/靶点: Zn(II)-氢亲核攻击羧酸酯（4MU-PA 等）水解酶 ZETA_1–4
- 候选生成方法: **RFdiffusion2** 围绕 theozyme 生成骨架 + ProteinMPNN/LigandMPNN + FastRelax
- 计算筛选器: 硬性活性位几何约束（要求 Glu/Asp/His 可作为通用碱活化水、稳定过渡态氧阴离子的侧链氢键、AF2 折成目标结构），再按 **PLACER** 预组织度排序；每轮**固定送测 96 个**
- MD: 否 / **QM: 是（核心输入）**——"We began by using **density functional theory (DFT)** to identify the transition-state geometry of the rate-determining Zn(II)-OH nucleophilic attack on the substrate ester. These calculations provide the coordinates of the three Zn(II)-binding imidazole rings, the metal, and the transition state"；"we designed zinc metallohydrolases starting from **quantum chemistry-derived active site geometries**"
- 实验验证: 表达纯化 + 水解动力学（kcat/KM）+ 金属结合表征
- **命中率原始数字（全文）**："From an initial set of **96** designs tested experimentally, the most active has a catalytic efficiency (k_cat/K_M) of **16,000 M⁻¹ s⁻¹**"；"The success rate in the second design campaign was considerably higher than the first campaign (**11 out of 96** versus **1 out of 96** designs with k_cat/K_M greater than 10³ M⁻¹ s⁻¹)"；"**Seven** designs based on the same ZETA_1 backbone family were initially filtered out during the design selection phase, as they had **suboptimal PLACER metrics**; we retrospectively expressed and purified these designs and found that they had **very low or no activity**, further highlighting the utility of PLACER ensemble calculations"；zero-shot 论断："The zero-shot design of an enzyme (ZETA_1) with a k_cat/K_M greater than 10⁴ M⁻¹ s⁻¹ — **the top-ranked in silico design out of a total of 96 tested straight from the computer, with no experimental optimization**"；"The robustness … is demonstrated by the zero-shot design of 3 additional enzymes from a new set of **96** designs tested straight from the computer: ZETA_2 and ZETA_3 (>10⁴ M⁻¹ s⁻¹), and ZETA_4 (>10³ M⁻¹ s⁻¹)"
- 时间线位置: 漏斗第一次**不需要实验优化轮**——计算排名第一的设计即达标。这是"筛选依据"的终极目标态；其判据不是 MD/QM 全局打分，而是"QM 定 theozyme + PLACER 定预组织 + 96 个送测名额"

### [B19] Modeling protein–small molecule conformational ensembles with PLACER
- 作者/单位: Anishchenko I, Kipnis Y, Kalvet I, Zhou G, Krishna R, Pellock S, Lauko A, Lee G, … Dauparas J, … Baker D（UW-IPD）
- PNAS, 2025, 122: e2427161122
- DOI: 10.1073/pnas.2427161122 ✅  PMID 41187076 / PMCID PMC12625923
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12625923/
- 设计对象/靶点: 小分子 dock 与酶活性位预组织评估（含 retro-aldolase）
- 候选生成方法: 图神经网络 PLACER，原子级表示、随机噪声初始化 → 生成**构象系综**
- 计算筛选器（定位）: PLACER 取代静态打分做"**活性位点准确度 + 预组织度**"筛选；配体内部结构/朝向从输入中抹去以避免"记忆答案"
- **MD 判定原文（本调研最关键的一条）**："**The most general way to evaluate such preorganization is molecular dynamics simulations (27,28), but as sidechain reconfiguration can occur on the microsecond time scale, such simulations are computationally expensive and cannot be applied to large numbers of designs**"；"We reasoned that PLACER could enable assessment … by generating ensembles … **much more rapidly than molecular dynamics simulations** and without the limitations of the Rotamer Boltzmann method"
- QM 使用: 否（PLACER 本身是 ML，不显式含 QM；QM 只在 theozyme 上游）
- 实验验证: 干验（Astex 非天然系 docking 成功率，ligand RMSD <1 Å / <2 Å 两档）＋ 湿实验酶
- **可量化结果（全文）**: "we obtain a preorganized retroaldolase with a k_cat/K_M of **11,000 M⁻¹ min⁻¹**, considerably higher than any pre–deep learning design for this reaction"；"using PLACER to assess the accuracy and preorganization of the designed active sites **results in higher success rates and higher activities**"
- 时间线位置: 明确回答"为什么 Baker 组不用 MD 做主筛选器"——成本；并用便宜的随机生成网络近似 MD 想回答的构象系综问题

### [B20] Atom-level enzyme active site scaffolding using RFdiffusion2
- 作者/单位: Ahern W, Yim J, Tischer D, Salike S, … Baker D（UW-IPD）
- Nature Methods, 23:96-105（Crossref issued=2025，EPMC 归入 2026 卷期）
- DOI: 10.1038/s41592-025-02975-x ✅  PMID 41339749 / PMCID PMC12791007
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12791007/
- 设计对象/靶点: 41 个 AME 基准活性位（含 Methodol retroaldolase、Zn 水解位）
- 候选生成方法: RFdiffusion2（原子级 motif scaffolding，支持 unindexed motif、配体构象自动采样）+ LigandMPNN 拟合序列 + Chai-1/AF2 复折
- 计算筛选器: "For each case, we generated **100 backbones**, fit **eight sequences** to them with LigandMPNN and then **refolded them with Chai-1** … After applying final quality filters … we found **41 cases** that satisfy all the criteria"；实验侧"filter them with structure prediction models to select designs for experimental validation"
- MD 使用: 否（仅引 MDTraj 作为参考文献）/ QM: **是，theozyme 来源**——"De novo enzyme design starts from a configuration of catalytic groups around the reaction transition state(s) (a theozyme) generated using **quantum chemistry**, protein structural analysis and/or chemical reasoning"
- 实验验证: 无细胞（IVTT）表达 + 半定量/定量活性测定
- **命中率原始数字（全文）**: "RFdiffusion2 samples at least one scaffold passing the success filters for **41/41** cases while RFdiffusion achieves **16/41**"（in silico）；"We generated designs scaffolding this theozyme, filtered them and expressed **96** in an in vitro transcription/translation system. We tested activity … using racemic Methodol … and found **four** variants that show detectable levels of retroaldolase activity"；"Among the **48** designs that were screened experimentally, several displayed detectable activity"；"In a second set of **96** designs tested including a general base to activate the water, we identified **11 functional enzymes**, the best of which had a k_cat/K_M of **53,000 ± 5,000 M⁻¹ s⁻¹**"
- 时间线位置: 从"残基级"降到"**原子级**"约束后，同一批 96 名额的实验命中率从 4/96 提升到 11/96（同一方法两代之间的量化对比），并解释 2024–2026 全原子化的动机：旧版要求指定侧链+骨架二面角，采样代价高、命中率低

### [B21] Diffusing protein binders to intrinsically disordered proteins
- 作者/单位: Liu C, Wu K, Choi H, … Watson J, … Baker D（UW-IPD）
- Nature, 2025, 644:809-817
- DOI: 10.1038/s41586-025-09248-9 ✅  PMID 40739343 / PMCID PMC12367549
- 设计对象/靶点: 非结构化/短肽靶：amylin、CP（carmine peptide? 具体为 IDP 片段）、VP48、ARATH/FUS 衍生、G3BP1 RBD、p53 类
- 候选生成方法: 部分扩散 + 二级结构指定（strand/helix specification）+ sequence-input diffusion
- 计算筛选器: "**pAE_interaction < 10, pLDDT > 90**"；再加 AF2 monomer pLDDT、RMSD to design model、contact_molecular_surface、**ddG**、SAP、氢键数；"Specific filtering criteria were carefully selected **to narrow down the set to 48–96 designs for each target**"
- MD: 否（文中 microfluidics/droplet 是成像实验，非 MD）/ QM: 否
- 实验验证: E. coli/昆虫细胞表达 + BLI
- **命中率原始数字（全文，逐靶）**：amylin "We tested **96** designs … binding affinities ranging from **100 nM to 454 nM**"；CP "**Six out of 95** designs bind to CP with better than 100 nM; the highest affinity binder (CP-35) had a K_d of **28 nM**"；VP48 "Of the **95** designs tested, the best binder with an affinity of **750 nM**"；sequence-input "using sequence input diffusion, **2 of 41** tested designs showed binding at approximately **450 nM** by BLI"；**"**Of **94** designs tested, **3** showed binding, with the top design having an affinity of **520 nM** and thermostability up to 95 °C"；G3BP1 "**Five out of 78** designs bound to G3BP1_RBD, with the tightest having a binding affinity at **17 nM**"；另一靶 "Of **48** designs tested, the tightest, PRI28, had a binding affinity of **14 nM**"；筛选逻辑改善的量化："only the **23** strand-containing designs had AF2 pAE_interaction < 10 and pLDDT_binder > 90 … we specified the secondary structure as a strand which **increased the fraction of designs passing the filters more than 50-fold**（23 → 1,192 successes）"
- 时间线位置: 展示漏斗的"**靶点依赖性**"——IDP/柔性表位即便全套过滤，命中率仍掉到 3/94、5/78 这个量级，且亲和力上限停在数百 nM。这类靶点是当前漏斗仍不奏效的边界

### [B22] Atomically accurate de novo design of antibodies with RFdiffusion
- 作者/单位: Bennett N, Watson J, Ragotte R, Borst A, … Baker D（UW-IPD）
- Nature, 649:183-193（Crossref issued=2025，EPMC pubYear=2026；预印本 10.1101/2024.03.14.585103 ✅）
- DOI: 10.1038/s41586-025-09721-5 ✅  PMID 41193805 / PMCID PMC12727541
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12727541/
- 设计对象/靶点: RSV site I/site III、SARS-CoV-2 RBD、Influenza HA、C. difficile TcdB、IL-7Rα、PHOX2B-pMHC
- 候选生成方法: **fine-tuned RFdiffusion2** 设计 VHH / scFv / 全 Ig；scFv 通过 H/L 组合文库（TM-score 聚类阈值对齐 yeast 转化效率 10⁷）组装
- 计算筛选器: 因为 **AF2 不能预测抗体-抗原**，改用自微调 **RoseTTAFold2**（RMSD < 2 Å to design model, **pAE < 10**）；正交用 **Rosetta ddG + SAP**；事后复盘 **AlphaFold3 ipTM**（AUC = 0.86）
- MD: 否 / QM: 否
- 实验验证: 高通量**酵母表面展示**（9,000 设计/靶）与低通量 **E. coli 表达 + SPR**（95 设计/靶）双轨 + cryo-EM
- **命中率原始数字（全文）**："Designs were screened either at high-throughput by yeast surface display (**9,000 designs per target**; RSV sites I and III, RBD and influenza haemagglutinin) or at lower-throughput with E. coli expression and single-concentration SPR (**95 designs per target**; TcdB, IL-7Rα and influenza haemagglutinin)"；"**success rates against each target … range from 0% to 2%**"；"Nine thousand designed VHHs were screened against RSV site III … and influenza haemagglutinin"；"the highest affinity [HA] binder had a K_d of **78 nM**"；"after soluble expression, SPR confirmed an affinity of **5.5 μM** to the target for design VHH_RBD_D4"；漏斗改进空间自评："We found that the AlphaFold3 interface predicted template modelling (ipTM) score … **is predictive of binding success (area under the curve = 0.86)** … Overall, **only 9% of our ordered VHH designs have an ipTM > 0.6**, suggesting that success rate will be improved by incorporation of an ipTM filter"；"the filtering power of this [fine-tuned RF2] model is limited (at least with the settings used; providing 100% of interface 'hotspots'). This probably accounts for the low experimental success rates and the inaccurate SARS-CoV-2 design"；scFv 侧 "Only **4%** of the initial design library has ipTM > 0.85, whereas **5 out of the 6** experimentally confirmed designs pass this threshold"；亲和力成熟："initial computational designs exhibit modest affinity (tens to hundreds of nanomolar K_d); affinity maturation using **OrthoRep** enables production of single-digit nanomolar binders"（摘要，https://pubmed.ncbi.nlm.nih.gov/41193805/）
- 时间线位置: 深度学习漏斗的**失效边界 + 修补方向**：当自洽性判据（AF2）对某类分子（抗体）失灵时，命中率塌回 0–2%、需要展示库+误差校正（OrthoRep）来补，且作者给出下一步判据（AF3 ipTM>0.6/0.85）

### [B23] Improved protein binder design using β-pairing targeted RFdiffusion
- 作者/单位: Sappington I, Toul M, Lee D, Robinson S, Goreshnik I, … Baker D（UW-IPD）
- Nature Communications, 2026, 17:1101
- DOI: 10.1038/s41467-025-67866-3 ✅  PMID 41519838 / PMCID PMC12852815
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12852815/
- 设计对象/靶点: KIT、PDGFRα、ALK-2、ALK-3、FCRL5、NRP1、α-CTX（暴露 β 边缘链位点）
- 候选生成方法: β-strand-interface conditioned RFdiffusion + ProteinMPNN
- 计算筛选器（阈值成套，最完整一条）: "obtained minimum values of **pAE_interaction < 10, pLDDT > 85, ΔΔG < −30**, a variable ROG filter adjusted for binder size (length/4.5 = ROG), and **SAP < 45**"；"Structurally diverse designs with high AlphaFold 2 confidence (interface **pAE < 8 and pLDDT > 85**) designs were selected for experimental screening by yeast surface display"
- MD: 否 / QM: 否
- 实验验证: 酵母表面展示库 + AKTA FPLC 96 孔自动 SEC + BLI + 功能细胞实验（lentivirus/CHO 稳定株）
- **命中率原始数字（全文）**: "These filters were used for in silico selection of top binder designs from **hundreds of thousands of sequences**, resulting in libraries ranging in size from **96 to 5000** that were screened experimentally"；"**over 9.2%** of β-strand interface conditioned designs meeting reasonable quality metrics, in contrast to **0.98% success rates** by RFdiffusion conditioned on target hotspots alone"；"less than **1%** of designs showing strong binding and enrichment" for hard targets；"The best binder to FCRL5, with a **82 nM K_d**, was obtained from a yeast display library of **4841** designs. For KIT, a **65 nM** binder (KITbp) was identified from a yeast surface library screening of **1298** designs"；"They were enriched from **5427** and **189** member design libraries … without any further experimental sequence optimization"；pM–mid nM affinity；氢键设计准确度："The majority of these hydrogen bonds were predicted accurately in our design model (**16 out of 21**)"
- 时间线位置: 漏斗参数化——"in silico 通过率"直接决定"下单库规模"（96↔5000），并显式按靶点表面凹凸/疏水性（SAP）预估难度来分配预算

### [B24] Accelerating protein design by scaling experimental characterization（SAPP / DMX）
- 作者/单位: Qian J, Milles L, Wicky B, Ragotte R, Motmaen A, Borst A, … Coventry B, … Baker D（UW-IPD）
- Nature Communications, 2026, 17:9945（预印本 10.1101/2025.08.05.668824）
- DOI: 10.1038/s41467-026-76740-9 ✅  PMID 42754580 / PMCID PMC13586242
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC13586242/
- 设计对象/靶点: SARS-CoV-2 RBD 迷你结合体（cb13/cb4）、荧光蛋白设计体、寡聚融合体
- 候选生成方法: RFdiffusion/ProteinMPNN（"either 50% or 70% of the most conserved residues were kept fixed during ProteinMPNN sequence redesign"）+ 自动反向翻译
- 计算筛选器（AF2 全套阈值，原文）: "AF2_plddt_mean > **0.8**, AF2_ptm > **0.80**, AF2_pae_mean < **12.0**, AF2_tm_score to WT > **0.7**, AF2_tm_rmsd to WT < **1.5**, AF2_sap_per_res < **0.4**"
- MD: 否 / QM: 否
- 实验验证方法与通量（这是 Q4 的主力论文）: **Semi-Automated Protein Production (SAPP)** + DMX 条形码解混 + 96/384 孔 + 自动 SEC
- **通量与命中率原始数字（全文）**: "SAPP is a rapid, modular, scalable and cost-effective protocol, enabling up to milligram-scale protein production and standardized characterization — including yield, dispersity, and oligomeric state — of **hundreds of designs per day, at the cost-equivalent of a few DNA oligos per construct**"；"The whole process from linear DNA to inoculated cultures is optimized to take **2 hours for up to 192 reactions**"；"SEC, which is run overnight (**15 hours for 192 samples**, <5 minutes per sample)"；"the main bottleneck being SEC, with a capacity of **~300 samples per chromatographic instrument per day**"；"enabling at least an **order of magnitude increase in throughput** while reducing wetlab time"；文库回收率："We successfully recovered **78%** of the library variants as clonal, sequence-verified constructs by screening **4608** clones (3× the library complexity), approaching the theoretical maximum recovery rate of **92%**"；解混最优规模："For large demultiplexing campaigns, the optimal library size is about **2000 genes**, requiring the sampling of about **8000 colonies** (20 × 384 well plates) to achieve >95% recovery"；一次实测："Following SAPP purification of **88 designs** and 12 respective WT controls … tested for their fluorescence properties … at a concentration of 20 µM"；寡聚体兼容："The success rate was higher than for cb13 (**33 of 58** constructs assembled to their target oligomeric state)"；上游计算→合成规模："The **top ~31,000 designs** were obtained as chip-based synthetic DNA, screened through yeast surface display, and optimized through site saturation mutagenesis"；YSD 局限："the non-covalent nature of oligomers makes multimeric constructs inherently incompatible with display technologies such as yeast surface display"
- 时间线位置: 漏斗的最后一环不再靠更好的打分函数，而靠**把湿实验本身变成高通量、低价、标准化产线**（每天数百设计，单价≈几条寡核苷酸）

### [B25] Hierarchical design of pseudosymmetric protein nanocages
- 作者/单位: Dowling Q, Park Y, Fries C, … Wargacki A, Hsia Y, … Baker D 等（UW-IPD）
- Nature, 638:553-561（Crossref issued=2024，EPMC pubYear=2025）
- DOI: 10.1038/s41586-024-08360-6 ✅  PMID 39695230 / PMCID PMC11821544
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC11821544/
- 设计对象/靶点: 准对称（pseudosymmetric）I53-50 型杂多聚体纳米笼，540 亚基级颗粒 GI4-F7 / GI9-F7
- 候选生成方法: Rosetta 突变扫描（对称破坏突变）+ 组合突变 + ProteinMPNN
- 计算筛选器: **ddG 与 total score 相对野生型的归一化升降**（式 1/式 2）："Ideal mutant pairs were those where one or both single mutations **increased the energy** of the trimer relative to the wild type (normalized scores > 0) while the double mutation had **no effect or stabilized** the trimer (normalized scores ≤ 0)"
- MD: 否 / QM: 否
- 实验验证: E. coli 裂解液组装筛选（native PAGE）+ 质谱 + cryo-EM
- **命中率原始数字（全文）**: "The 1WA3 trimer proved remarkably plastic: **only 3 out of the 82 single mutants** tested did not yield a band corresponding to the assembled I53-50 nanocage"；"Ninety-six unique individual mutations increased the predicted homotrimerization energy (ddG) or Rosetta score by more than 100 Rosetta energy units"；失败解释（作者自陈）："Although this choice contributed to the successful expression of a large number of mutants, it also led to the **low success rate of symmetry-breaking mutations**: 1WA3 proved remarkably resilient to mutations intended to disrupt the homotrimer"；结构精度："the diameter of GI4-F7 observed by cryo-EM is within **2%** of the design model"；GI9-F7 "deviates from the design model by only **11.5 Å Cα r.m.s.d. across all 540 subunits, 1.6% of the nanocage diameter**"
- 时间线位置: 展示漏斗的另一种失败类型——**物理打分"太保守"（ddG 判为破坏的设计大多仍能折叠/仍能组装）**，即判据与目标"不对称性"错位；作者明确把希望寄托于结构预测与设计成功率的持续提高

### [B26] Using experimental results of protein design to guide biomolecular energy-function development
- 作者/单位: Haddox H, Rocklin G, Motta F, Strickland D, Halabiya S, Cordray C, Park H, Klavins E, **Baker D**, DiMaio F（UW-IPD）
- PLOS Computational Biology, 2026, 22: e1014215
- DOI: 10.1371/journal.pcbi.1014215 ✅  PMID 42018576 / PMCID PMC13124059
- 链接: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014215
- 设计对象/靶点: 用 Rosetta 设计的小型蛋白（miniprotein）稳定性/折叠失败案例
- 候选生成方法: Rosetta（beta_nov16）设计 + FastRelax
- 计算筛选器（研究对象本身）: Rosetta ddG / total score 的"clashing bias"
- MD: 否（用 DMS 实验数据回归能量参数）/ QM: 否
- 实验验证方法与通量: **深度突变扫描（DMS）21 个库**、约 16,000 个突变、"biological replicates … for 19 of the 21 outlier designs"
- **命中率原始数字（全文）**: "Across all outlier designs, **~1% of mutations (156 out of ~16,000 mutations tested) were highly stabilizing (Δ stability score > 1.0)**"；"As described in the Methods, the **21 DMS libraries** were ordered and tested as part of two larger libraries"；重训练效果："**Retraining Rosetta using high-quality benchmarks largely eliminated the clashing bias**"；界面预测基准 "used in training, but we tested the energy functions using a set of **59 structures** withheld from training"、验证集 "**62 crystal structures**"；质量控制阈值 "differed by >0.1 energy units per residue" 等
- 时间线位置: 闭环的最后一块：**用湿实验失败数据回炉校正物理打分器**（而不是再加一层 MD/QM）。这就是"降低实验成本"的长期策略之一

### [B27] Computational design of sequence-specific DNA-binding proteins
- 作者/单位: Glasscock C, Pecoraro R, McHugh R, … Haddox H, … Baker D（UW-IPD）
- Nature Structural & Molecular Biology, 2025, 32:2252-2261
- DOI: 10.1038/s41594-025-01669-4 ✅  PMID 40940539 / PMCID PMC12618268
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12618268/
- 设计对象/靶点: 序列特异性 DNA（HTH 型人造 DNA 结合蛋白，DBP）
- 候选生成方法: 自建 scaffold 库（AF2 预测天然 HTH）+ motif grafting + loop inpainting + Rosetta/LigandMPNN 序列设计
- 计算筛选器: AF2 **pLDDT** + 与已知 HTH 结构 **TMscore**；DNA 相互作用过滤器（识别螺旋与碱基的多重有利接触）；多轮筛选（识别螺旋提取→聚类→回贴→再设计）
- MD: 否（2 处提及均为参考文献/无筛选作用）/ QM: 否
- 实验验证: 酵母表面展示 + FACS 分选
- **规模原始数字（全文）**: "We generated at least **10,000 designs for each DNA target that passed all the structural and DNA interaction filters**"；"In the first set, we generated **21,488** designs using Rosetta-based sequence design, the motif grafting strategy and our custom scaffold library of AF2-predicted native DNA-binding domains"；"In the second design set, we generated **12,273** designs against the same DNA sequences with the **LigandMPNN** sequence design strategy and the motif grafting approach for backbone resampling"；分选后命中数未在正文给出统一百分比（见缺口 9）
- 时间线位置: 把漏斗推广到**非蛋白靶（核酸）**；同时显示 LigandMPNN（原子环境条件化序列设计）在真实项目里替换 Rosetta LayerDesign 的量化路径

### [B28] Atomic context-conditioned protein sequence design using LigandMPNN
- 作者/单位: Dauparas J, Lee G, Pecoraro R, An L, Anishchenko I, Glasscock C, Baker D（UW-IPD）
- Nature Methods, 2025, 22:717-723
- DOI: 10.1038/s41592-025-02626-1 ✅  PMID 40155723 / PMCID PMC11978504
- 链接: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11978504/
- 设计对象/靶点: 小分子结合/传感蛋白、DNA 结合蛋白、金属位
- 候选生成方法: LigandMPNN（显式建模非蛋白原子，同时输出侧构象）
- 计算筛选器: 序列-骨架-配体联合似然 + 侧链构象可评估性
- MD: 否 / QM: 否
- 实验验证与命中率（摘要，本卡片为**摘要级**，未抓取全文）: "LigandMPNN significantly outperforms Rosetta and ProteinMPNN on native backbone sequence recovery for residues interacting with **small molecules (63.3% versus 50.4% and 50.5%)**, **nucleotides (50.5% versus 35.2% and 34.0%)** and **metals (77.5% versus 36.0% and 40.6%)**"；"LigandMPNN has been used to design **over 100 experimentally validated** small-molecule and DNA-binding proteins with high affinity and high structural accuracy (as indicated by **four X-ray crystal structures**), and **redesign of Rosetta small-molecule binder designs has increased binding affinity by as much as 100-fold**"（https://pubmed.ncbi.nlm.nih.gov/40155723/）
- 时间线位置: 序列端的"全原子化"。与 [B29] 的**回溯性证据**互相印证：Baker 组自己的小分子结合体论文（[B10]、[B33]）里"用 LigandMPNN/ProteinMPNN 重设计 Rosetta 设计"能把亲和力提高 100 倍，这就是"为什么换序列设计器"的成本理由

### [B29] Computational design of soluble and functional membrane protein analogues
- 作者/单位: Goverde C, Pacesa M, Goldbach N, … Rosset S, … Baker D 等（UW-IPD + ETH Zürich）
- Nature, 2024, 631:449-458
- DOI: 10.1038/s41586-024-07601-y ✅  PMID 38898281 / PMCID PMC11236705
- 设计对象/靶点: 膜蛋白拓扑的可溶模拟物（含功能位点富集）
- 候选生成方法: ProteinMPNN 序列设计 + 拓扑蓝图
- 计算筛选器（原文阈值）: "the structures of all resulting sequences are repredicted with AF2 and filtered on the basis of their structural similarity to the target topology (**TM score > 0.8**), confidence scores (**pLDDT > 80**) and sequence novelty relative to naturally occurring sequences (**e-value > 0.1**)"
- MD: 否 / QM: 否
- 实验验证: 表达纯化 + SEC + 热稳定性
- **命中率原始数字（全文）**: "We selected **19** designs for experimental characterization on the basis of AF2 confidence scores and sequence diversity"；"We experimentally characterized **25** designs, of which **six** were found to be folded and monomeric in solution while exhibiting high thermal stability"（≈24%）；"We experimentally assessed **25** designs, **five** of which were monomeric, folded and highly thermostable in solution"（≈20%）
- 时间线位置: 拓扑复杂度上限被打开时，命中率反而回落到 ~20%，与 [B08] 的 19% 一致——**漏斗效率天花板主要由任务难度决定**，不是打分器数量

### [B30] Rapid and automated design of two-component protein nanomaterials using ProteinMPNN
- 作者/单位: de Haas R, Brunette N, Goodson A, Dauparas J, … Bera A, … Baker D（UW-IPD）
- PNAS, 2024, 121: e2314646121
- DOI: 10.1073/pnas.2314646121 ✅  PMID 38502697 / PMCID PMC10990136
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC10990136/
- 设计对象/靶点: 双组分蛋白纳米材料（T33 型 icosahedral cage）全自动重设计
- 候选生成方法: Rosetta SymDofMover 微扰 + **ProteinMPNN**（无人工干预）
- 计算筛选器: shape complementarity 排序 + 阈值过滤："We selected a maximum of three variants of each original design … resulting in a total of **76 designs that passed our filter cut-offs** … without any manual intervention"
- MD: 否 / QM: 否
- 实验验证: 双顺反子质粒 + 2 mL E. coli 培养 + native PAGE 组装筛选
- **命中率原始数字（全文）**: "In the original publication, **four of the 27** previously designed complexes successfully adopted the target architecture"；"ProteinMPNN had a similar success rate to Rosetta, yielding **13 new experimentally confirmed assemblies**, but required **orders of magnitude less computation** and no manual refinement"
- 时间线位置: "同样的命中率、1/1000 算力、零人工"——这是算力成本而非判据成本的改进，解释了为什么 ProteinMPNN 会被无条件采纳

### [B31] Small-molecule binding and sensing with a designed protein family
- 作者/单位: Lee G, Pellock S, Norn C, Tischer D, Dauparas J, Anishchenko I, … Baker D（UW-IPD）
- Nature Communications, 2026, 17（文章号见 DOI）
- DOI: 10.1038/s41467-026-70953-8 ✅  PMID 41904144 / PMCID PMC13194776
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC13194776/
- 设计对象/靶点: 6 个小分子（HCY/皮质醇类、ROC、WRF、APX、IRI、OHP）
- 候选生成方法: RIFdock + 3 螺旋束/迷你蛋白库 + Rosetta FastDesign + ProteinMPNN/LigandMPNN
- 计算筛选器: AF2 复合物置信度 + Rosetta 界面项（同一族多靶点复用）
- MD: 否 / QM: 否
- 实验验证: 表达 + 结合测定 + 生物传感
- **规模与自评原始数字（全文）**: "After filtering, we obtained oligonucleotides encoding the binders for experimental characterization, including **630 for HCY, 1661 for ROC, 16,276 for WRF, 9024 for APX, 19,390 for IRI, and 7573 for OHP** (two approaches combined when applied)"；"Nevertheless, the **success rate of high-affinity binder designs in our approach was lower than alternative methods utilizing the four-helical bundles**, and this highlights the need to develop methods capable of designing scaffolds to accommodate a broader range of targets and accurately predicting binding prior to experimental validation"
- 时间线位置: 小分子方向仍需"万级下单"，与蛋白-蛋白方向的"百级下单"形成对照——漏斗对**小分子/柔性表位**仍不充分有效

### [B32] Design of high-affinity binders to immune modulating receptors for cancer immunotherapy
- 作者/单位: Yang W, Hicks D, Ghosh A, … Coventry B, … Baker D（UW-IPD + 其他）
- Nature Communications, 2025, 17
- DOI: 10.1038/s41467-025-57192-z ✅  PMID 40011465 / PMCID PMC11865580
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC11865580/
- 设计对象/靶点: CTLA-4、PD-L1、TGFβRII 等免疫检查点（5HCS 螺旋支架 + 迷你蛋白）
- 候选生成方法: 5HCS（five-helical bundle）组合支架库 + Rosetta LayerDesign + ProteinMPNN 界面重采样
- 计算筛选器（原文阈值）: "filtered by the AlphaFold2 with a mean pLDDT cutoff of **80** and AccNet with a mean pLDDT cutoff of **0.8**"；"filtered by **ddG (less than −40)**, contact molecular surface (**larger than 400**), and **pAE (less than 10)** from AlphaFold2 initial guess"；"delta ddG predicted by AlphaFold2 initial guess"
- MD: 否 / QM: 否
- 实验验证: 酵母展示 + FACS + SSM 结合指纹 + 细胞功能报告基因（Jurkat 荧光素酶）+ E. coli 表达 + BLI
- **规模与命中率原始数字（全文）**: "We tested in parallel **67** 5HCS based designs and **4310** designs based on the globular scaffolds used by Cao et al."；"Finally, **67 and 4310** designs … passed the filters and were tested experimentally"；另一靶 "Finally, **4600** designs from 5HCS passed the filters and were tested experimentally"；另一轮 "Finally, **96** designs from 5HCS libraries passed the filters and were tested experimentally"；亲和力成熟路径："combining the most enriched substitutions from the **SSM heatmap** … following yeast display selection, we expressed **four** of the best binders in E. coli"
- 时间线位置: 展示了"**计算筛 → 67/4310 下单 → SSM 热图 → 组合突变库 → 亲和成熟**"的标准三段式，即"设计端只负责命中，亲和力靠便宜展示端优化"

### [B33] De novo design of modular peptide-binding proteins by superhelical matching
- 作者/单位: Wu K, Bai H, Chang Y, … Baker D（UW-IPD）
- Nature, 2023, 616:581-589
- DOI: 10.1038/s41586-023-05909-9 ✅  PMID 37020023 / PMCID PMC10115654
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC10115654/
- 设计对象/靶点: 短肽模体（含 phospho-肽）的可模块化肽结合支架
- 候选生成方法: superhelical matching（超螺旋匹配）生成支架 + 序列设计（本卡片仅元数据 + 摘要级，**未逐段核对方法细节与命中率**）
- 计算筛选器: 未核对（⚠️ 不做无证据推断）
- MD 使用: 未核对 / QM 使用: 未核对
- 实验验证方法与通量: 仅摘要级（本卡片未抓取正文方法段，故不填写未经核实的通量与命中率）
- 时间线位置: 螺旋支架路线的代表；[B32] 的 5HCS 文库、[B28] 提到的"四螺旋束命中率更高"均溯源至此系工作

### [B34] De novo design of buttressed loops for sculpting protein functions
- 作者/单位: Jiang H, Jude K, Wu K, Fallas J, Ueda G, Brunette T, Hicks D, Pyles H, Yang A, Carter L, … Baker D（UW-IPD + Scripps）
- Nature Chemical Biology, 2024, 20:974-980
- DOI: 10.1038/s41589-024-01632-2 ✅  PMID 38816644 / PMCID PMC11288887
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC11288887/
- 设计对象/靶点: 带长环的重复蛋白（RBL, repeat proteins with buttressed loops）+ 六联重复肽（(DLP)₆、(KLP)₆、(DLS)₆）结合体
- 候选生成方法: 系统采样两理想螺旋长度（12–28 aa）与六个刚体自由度 → 支架库 → 序列设计
- 计算筛选器（阈值最"物理"的一篇，全文原文）: "filtered in Rosetta by the number of **buried unsatisfied heavy atoms (≤3)**, core residue **hole score (≤−0.015)**, **total score per residue (<−2)**, **packstat (≥0.5)** and average **hydrogen bond energy per residue (≤−1)** in the buttressed long loops"；骨架侧要求"fewer than **28%** of the residues in a buried core"被剔除、 termini distance ≤18 Å、"at least five residues within **8 Å** of the closest helical residues"；复合物侧"**PAE_interaction ≤ 15**"
- **MD 使用: 是（本调研中唯一一次 MD 进入入选判据）** —— "The rigidity of the design models was evaluated using **molecular dynamics simulations** and the extent to which the designed sequence encodes the structure by AlphaFold"；"Top 10% scoring structures were further tested by in silico validation methods such as **molecular dynamics simulations (Cα RMSD < 3 Å)**, **AlphaFold (pLDDT > 80, Cα RMSD < 3 Å)** or **RoseTTAFold (pLDDT > 80, Cα RMSD < 3 Å)**"；软件/力场："We performed molecular dynamics simulations using **GROMACS (2018.4)** with the **Amber99SB-ILDN** force field"。注意其定位：MD 只是三种可互换的 in silico 验证手段之一（用于刚性，而非亲和力）
- QM 使用: 否
- 实验验证: E. coli 表达 + His 柱 + SEC-MALS + CD（含 95 °C 可逆性）+ 荧光偏振
- **命中率原始数字（全文）**: "We expressed **102** selected designs (which we call repeat proteins with buttressed loops (RBLs)) in Escherichia coli"；"**52** were monodisperse and **46** were monomeric, as indicated by multi-angle light scattering coupled with size-exclusion chromatography (SEC–MALS)"；"**Forty-four** of these proteins showed the expected α-helical circular dichroism (CD) spectrum at 25 °C, remained at least partially folded at 95 °C and recovered nearly all the CD signal when cooled"（→ 102 送测中 44 ≈ **43%** 折好且热稳定）；成本指标："The typical yield of a monodisperse and thermally stable designed RBL is **1–6 g l⁻¹**"；肽结合分支："We designed **34** proteins to bind six-repeat peptides …, screened them in silico based on protein–protein interaction design filters including AlphaFold structure recapitulation, obtained synthetic genes encoding the designs and purified the proteins from E. coli"
- 时间线位置: 全原子局部设计（长环）的能力扩展；同时也是"MD 到底有没有进过闸口"这一问题的唯一肯定答案——但它是以"刚性检查"的身份、与 AF/RF 平行可选，而不是像 Rosetta ddG 那样的必过关口。

### [B35] De novo Design of All-atom Biomolecular Interactions with RFdiffusion3
- 作者/单位: Butcher J, Krishna R, Mitra R, … **Baker D**（23 人，UW-IPD）
- bioRxiv 预印本, 2025-09-18（DOI 10.1101/2025.09.18.676967 ✅ Crossref 核验；未见刊期记录）
- DOI: 10.1101/2025.09.18.676967 ✅（Crossref 核验，23 人，has_baker=True；未核验正式刊期 ⚠️）  PMID: 无（预印本，PubMed 未收录）
- 链接: https://www.biorxiv.org/content/10.1101/2025.09.18.676967v1
- 设计对象/靶点: DNA 结合蛋白、半胱氨酸水解酶（cysteine hydrolases）等全原子相互作用
- 候选生成方法: RFdiffusion3（单一全原子扩散模型同时生成骨架+序列+非蛋白组分）
- 计算筛选器: 预印本摘要未列阈值（仅摘要级）
- MD: 否 / QM: 否（均为摘要 + bioRxiv 页面级判断，未见判据细节）
- 实验验证方法与通量: 摘要级——bioRxiv 摘要页未给下单数/命中率，仅『designing and experimentally characterizing DNA binding proteins and cysteine hydrolases』
- **可引用原文数字（摘要）**: "RFdiffusion3 achieves improved performance compared to prior approaches on a range in silico benchmarks **with one tenth the computational cost**" 并 "designing and experimentally characterizing DNA binding proteins and cysteine hydrolases"
- 配套工作：同期另有 "De novo design of cysteine proteases"（Choi H, Bauer M, Coventry B, … Baker D；23 人，has_baker=True），bioRxiv DOI 10.1101/2025.11.21.689808 ✅（Crossref 核验，未核验正文数字）；以及 "RFOptimization: Guiding Design Optimization with All-Atom Structure Prediction"（Zhang O, Wang J, Thompson T, You Z, Song Z, DiMaio F, **Baker D**），bioRxiv DOI 10.64898/2026.09.04.749184 ✅（Crossref 核验；7 人）。这三项构成 2025–2026 的"one-shot 全原子/优化"前沿，但**尚无同行评审的实验命中率数字可引**（见缺口 3）
- 时间线位置: 把"生成"与"筛选"合并进同一个全原子模型（10× 算力下降），目标是取消 AF2-refold 这一最贵的闸口

### [B36] The past, present and future of de novo protein design（Baker 组 2026 立场综述）
- 作者/单位: Yang W, Wang S, Lee G, Zhang J, Courbet A, Juergens D, Wang X, Schlichthaerle T, Abedi M, Ragotte R, … Baker D（24 人）
- Nature, 2026, 652:1139-1152
- DOI: 10.1038/s41586-026-10328-7 ✅  PMID 42056544（无 PMC，**摘要级**）
- 链接: https://pubmed.ncbi.nlm.nih.gov/42056544/
- 设计对象/靶点: 不适用（综述，覆盖 fold / 组装体 / 蛋白结合体 / 酶 / 多态开关全谱）
- 候选生成方法与计算筛选器: 不适用（综述；正文未抓取，本报告仅使用摘要）
- MD / QM 角色: 摘要未提及，不作为证据
- 实验验证方法与通量: 不适用（综述）
- 关键原文（摘要）: "While there is still room for improvement in **success rates and activities**, the long-standing challenges of designing new protein structures, assemblies and protein binders are **close to being solved**. The key current questions in these areas are not how to design, but what to design, and open-source design methodology such as **RFdiffusion and ProteinMPNN together with protein structure prediction tools** enable biochemists and molecular biologists to broadly explore possible applications"；"Current challenges for methods development include **design of catalysts for reactions with high energy barriers** and, more generally, design of switches and nanomachines…"
- 时间线位置: Baker 组对"**漏斗已经够用**"的官方判断——即蛋白 fold/组装体/蛋白-蛋白结合体三类任务的筛选问题被视为基本解决；剩余未解的是高活化能反应催化、多态开关/纳米机器

### [B37] Incorporation of sensing modalities into de novo designed fluorescence-activating proteins
- 作者/单位: Klima J, Doyle L, Lee J, Rappleye M, Gagnon L, Lee M, Barros E, Vorobieva A, Dou J, Bremner S, … Baker D（UW-IPD）
- Nature Communications, 2021, 12:856
- DOI: 10.1038/s41467-020-18911-w ✅  PMID 33558528 / PMCID PMC7870846
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC7870846/
- 设计对象/靶点: 全新荧光激活蛋白（FAP，结合 DFHBI/DFHO 生色团），并加装 Ca²⁺ 感应/别构模态
- 候选生成方法: RosettaRemodel 自定义 β-桶 loop 片段库（b11、b32 支架）+ EF-hand 嫁接 + 组合链接肽采样
- 计算筛选器: 环闭合成功的骨架 + 生色团界面极性/氢键设计 + 堆积质量（Rosetta 物理项）
- **MD 使用: 是，但为事后机理解释**——"Molecular dynamics (MD) simulations starting from the X-ray crystal structure coordinates of EF1p2_mFAP2b in four conditions (apo, Ca²⁺-bound, DFHBI-bound and with both Ca²⁺ and DFHBI) suggest Ca²⁺ binding to loop7 shifts the free energy landscape towards the holo (fluorescently active) conformation even in the absence of DFHBI"；Methods："Chain B of the refined EF1p2_mFAP2b–DFHBI–Ca²⁺ co-crystal structure (PDB 6OHH) was used as the starting point for MD"
- **QM 使用: 是，但只用于生色团参数化/光化学**——"The DFHBI ligand was parametrized using Antechamber and the generalized Amber Force Field (GAFF), with geometry optimization performed with Gaussian 09"
- 实验验证方法与通量: 库筛选（多轮）+ 荧光滴定（8 个技术重复）+ 心肌细胞/活细胞成像
- **规模与命中率原始数字（全文）**: "from which **2226** designs with successfully closed loops were generated"；"we used Rosetta to de novo design **59** extensions of β-barrel loops 1, 3 and 7, and screened them for fluorescence after labeling with DFHBI"；"We identified **five** extended loop7 variants that maintain the β-barrel fold and are compatible with DFHBI binding"；亲和力基线："mFAP2 was chosen for optimization because it has the highest absolute fluorescence quantum yield (ϕc of **2.1%**) and highest affinity (**K_d of ~180 nM**) for the phenolate form of DFHBI"
- 时间线位置: 2019–2021 期"物理设计 + 生色团"的功能化尝试；也是 MD/QM 同时出现但均不在闸口的典型样本（且作者 [B02] 即本篇共同作者 Barros 的 MD 筛选探索同年）

### [B38] Local structural flexibility drives oligomorphism in computationally designed protein assemblies
- 作者/单位: Khmelinskaia A, Bethel N, Fatehi F, Mallik B, Antanasijevic A, Borst A, Lai S, Chim H, Wang J, Miranda M, … Baker D（UW-IPD）
- Nature Structural & Molecular Biology, 2025, 32:1050-1060（预印本 10.1101/2023.10.18.562842）
- DOI: 10.1038/s41594-025-01490-z ✅  PMID 40011747 / PMCID PMC12170342
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC12170342/
- 设计对象/靶点: 设计蛋白组装体的"寡聚多型"（同一组件形成多种邻近架构）
- 候选生成方法: Rosetta/ProteinMPNN 界面设计（既有 I32-10 等组装体）
- 计算筛选器: 静态设计模型 + cryo-EM 密度刚体拟合（不是 MD 筛）
- **MD 使用: 是，纯机制用途**——"Structural modeling and **molecular dynamics simulations** indicate that constrained flexibility within the subunits of each assembly promotes a defined range of architectures rather than nonspecific aggregation"；"To identify inherent structural fluctuations, we performed **molecular dynamics simulations for each trimeric and dimeric building block as well as the interfaces formed between them**"；"it should be possible to reconstruct each of the observed assemblies using a small number of structural snapshots from the **molecular dynamics trajectories**"
- QM 使用: 否
- 实验验证: cryo-EM（cisTEM/CryoSPARC 的 C1 ab initio 重建）+ DLS/SEC
- 命中率数字: 本论文不报告设计命中率（研究对象是已建成组装体的柔性），**无 N→M→K 计数**
- 时间线位置: 说明 MD 在 Baker 组 2025 年的真实用途——**解释"为什么设计体聚成两种而非一种"**，而不是"挑哪个送去表达"

### [B39] Exploiting conformational dynamics to modulate the function of designed proteins
- 作者/单位: Rennella E, Sahtoe D, **Baker D**, Kay L（UW-IPD + Toronto）
- PNAS, 2023, 120: e2303149120
- DOI: 10.1073/pnas.2303149120 ✅  PMID 37094170 / PMCID PMC10161014
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC10161014/
- 设计对象/靶点: C34（设计 α/β 蛋白，捕获 β-strand/发夹，用于聚集病相关分子隔离）
- 候选生成方法: 既有设计体 + 定点突变稳定单构象
- 计算筛选器: 无（用 NMR 弛豫色散"看见"激发态）
- **MD 使用: 仅辅助**——原文相关表述："minimum energy **molecular dynamics** trajectories on energy landscapes could provide critical insights into the conformers that must be considered"（展望性质，非入选判据）
- QM 使用: 否
- 实验验证: NMR（对"不可见"低丰度构象的探测）+ 突变体亲和力测定
- 关键结论原文: "establishing that it interconverts between a pair of distinct conformers that **compete with binding of the cognate peptide**"；"these **attenuate the affinity**"（→ 失败原因是静态设计模型看不见的激发态）
- 时间线位置: 给出 Baker 组对"漏斗为什么仍有 Type II 式失败"的物理答案（低能激发态与结合态竞争），并明确主张用 NMR（不是 MD/QM）来改进设计流程

### [B40] De novo design of proteins housing excitonically coupled chlorophyll special pairs
- 作者/单位: Ennist N, Wang S, Kennedy M, Curti M, Sutherland G, Vasilev C, Redler R, Maffeis V, Shareef S, Sica A, … Baker D（UW-IPD + ASU/其他）
- Nature Chemical Biology, 2024, 20:906-915（预印本 10.21203/rs.3.rs-2736786/v1）
- DOI: 10.1038/s41589-024-01626-0 ✅  PMID 38831036 / PMCID PMC11213709
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC11213709/
- 设计对象/靶点: 容纳叶绿素特殊对（excitonic coupling）的人工光合能量转移蛋白
- 候选生成方法: 全原子/配体约束的 de novo 设计（RFAA 系工具链）
- 计算筛选器: 色素几何/间距约束 + 模型置信度
- **MD 使用: 是，用于光谱建模与参数化**——"All molecular dynamics simulations were performed with **Amber18**"；"we used the **MCPB.py** module of Amber [for chromophore (ZnPPaM) force field parameters]"；"the protocol consists of nine sequential energy minimizations and short molecular dynamics runs, which sum to 4,000 steps of minimization and 40,000 molecular dynamics steps (totaling 30 ps), followed by a final molecular dynamics equilibration (500,000 steps, 1,000 ps)"
- **QM 使用: 是（激发态光化学，设计目标本身要求）**——"Absorbance, fluorescence and circular dichroism measurements along with **time-dependent density functional theory calculations** suggest that the chlorophyll molecules in our special pair proteins are also excitonically coupled"；"excitonic splitting … induced by an interpigment coupling of **241 cm⁻¹ as estimated by density functional theory**"；"Quantum mechanical geometry optimization and ESP calculations were performed using **Gaussian 16 (rev B.01) at the B3LYP/6-31G\*** level"
- 实验验证: 吸收/荧光/CD 光谱 + 结构解析
- 命中率数字: 本论文正文未给统一的"设计→表达→命中"计数（属功能光谱验证型工作）
- 时间线位置: QM 在这里不是筛掉候选的工具，而是**定义成功标准的工具**（激发耦合需要 QM 才能算）——与酶过渡态情形同构

### [B41] Four-component protein nanocages designed by programmed symmetry breaking
- 作者/单位: Lee S, Kibler R, Ahn G, Hsia Y, Borst A, Philomin A, Kennedy M, Huang B, Stoddard B, **Baker D**（UW-IPD）
- Nature, 638:546-552（Crossref issued=2024，EPMC pubYear=2025）
- DOI: 10.1038/s41586-024-07814-1 ✅  PMID 39695226 / PMCID PMC11821509
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC11821509/
- 设计对象/靶点: T=4 四组分蛋白纳米笼（四面体/八面体/二十面体）
- 候选生成方法: BGL17_A32 同源三聚体为 host/guest（7 个带臂 + 4 个无臂界面）→ RPXdock 采样 C3 轴位移 → 层级化 crown 设计
- 计算筛选器（AF2 正/负双判据）: "We selected designs for which **AF2 predicted the ch_A–ch_B interface with RMSD < 2 Å and did not predict the ch_A–ch_A or ch_B–ch_B homodimer interfaces to form**"；"Designs were filtered based on the formation of the designed interface, and **lack of formation of the self interfaces**, in AF2 predictions"
- MD: 否 / QM: 否
- 实验验证: E. coli 分别表达各链 + SEC + negative-stain EM（Talos L120C；300 kV Krios 自动采集）+ DLS 稳定性
- **规模原始数字（全文）**: "We obtained genes encoding **19** sets of crowns that passed these filters (crown C3-1 … C5-7)"；"We experimentally tested **14** sets of T=4 cage designs (Tet T=4-1 … Ico T=4-5) that passed the AF2 filters"
- 时间线位置: 与 [B25] 同期，展示漏斗在"多组分不对称组装"上的新判据形态——**同时要求"该成的界面成"与"不该成的界面不成"**（负向筛选），这是纯物理打分难以表达的

### [B42] Designed endocytosis-inducing proteins degrade targets and amplify signals
- 作者/单位: Huang B, Abedi M, Ahn G, Coventry B, Sappington I, Tang C, … Schlichthaerle T, … Baker D（UW-IPD；45 人）
- Nature, 638:796-804（Crossref issued=2024，EPMC pubYear=2025）
- DOI: 10.1038/s41586-024-07948-2 ✅  PMID 39322662 / PMCID PMC11839401
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC11839401/
- 设计对象/靶点: 诱导内吞的受体结合体（IGF2R、ASGPR、EGFR 等）与 EndoTag/pLYTAC
- 候选生成方法: RFdiffusion 迷你结合体 + 螺旋模体提取/ grafting 迭代
- 计算筛选器: **AF2 复合物自洽**（"designs for which AlphaFold2 predictions matched the intended structures"）
- MD: 否 / QM: 否
- 实验验证方法与通量: 酵母表面展示 + FACS + 扩增子测序；HeLa 磷酸化流式；ATZ 融合 PD-L1 清除
- **命中率原始数字（全文）**: "We tested **170** designs for which AlphaFold2 predictions matched the intended structures for binding to both IGF2R domains, and expressed **eight** designs that interacted with both domains in E. coli"；"We used yeast display for **2,689** designs that were predicted to bind ASGPR by AlphaFold2 followed fluorescence-activated cell sorting (FACS) and next-generation sequencing to reveal **four** highly enriched designs"；迭代优化侧："Helical motifs were extracted, and **3,000** designs were selected, grafted and subjected to further design"
- 时间线位置: 展示了当"功能"比"结合"要求更高（要触发内吞）时命中率再次跌至 8/170、4/2689——**漏斗命中率与下游功能复杂度成反比**，这是 Q5 的负面对照

### [B43] De novo designed proteins neutralize lethal snake venom toxins
- 作者/单位: Vázquez Torres S, Benard Valle M, Mackessy S, … Sappington I, Overath M, … Baker D（UW-IPD + Liverpool School of Tropical Medicine 等 33 人）
- Nature, 2025, 639:225-231（Research Square 预印本 2024-05-17，见全文 'Previous version available' 声明）
- DOI: 10.1038/s41586-024-08393-x ✅  PMID 39814879 / PMCID PMC11882462
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC11882462/
- 设计对象/靶点: 3FTx 家族（短链/长链 α-神经毒素、细胞毒素），目标做"泛蛇毒中和剂"
- 候选生成方法: RFdiffusion/ProteinMPNN 类深度学习设计 + partial diffusion 界面再优化
- 计算筛选器: AF2/设计模型自洽（正文以"limited experimental screening"强调不用大库）
- MD: 否 / QM: 否
- 实验验证方法与通量: 酵母表面展示 + BLI/SPR + SEC + 热稳定性 + 细胞活力发光中和实验 + 小鼠保护实验
- **命中率原始数字（全文）**："Synthetic genes encoding **44** designs targeting ScNtx were screened via yeast surface display, and **one** candidate was identified to bind ScNtx with a dissociation constant (K_d) of **842 nM**, as confirmed by bio-layer interferometry (BLI)"；"Following partial diffusion optimization, **11 of 78** designs had higher affinity than the initial hit"；"Partial diffusion optimization of the binding interface generated **38** designs"；"A total of **55** protein designs were recombinantly expressed using Escherichia coli, and following SEC purification, **18** designs with monomeric populations were tested in a luminescent cell viability assay"；最高亲和力 "LNG, had a K_d of **1.9 nM**, as measured by SPR"；细胞毒素分支 "a disulfide bond was introduced … yielding a candidate (CYTX_B10) with improved thermal stability (**T_m = 70.3 °C**) and monomeric profile during SEC, but a slightly weaker K_d of **740 nM**"；成本定位："More generally, our in silico design approach avoids animal immunization and/or construction and several rounds of selection and/or screening of large libraries, providing a **low-cost methodology** for the rapid development of toxin binders"；摘要级结论："With **limited experimental screening**, we obtained protein designs with remarkable thermal stability, high binding affinity and near-atomic-level agreement with the computational models. The designed proteins effectively neutralized all three 3FTx subfamilies in vitro and protected mice from a lethal neurotoxin challenge"
- 时间线位置: "设计→有限筛选→体内有效"的治疗学验证终点样本；也说明 nM 级首轮命中（1/44）仍需 partial diffusion 第二轮（11/78）才做到 pM–低 nM

### [B44] De novo design of highly selective miniprotein inhibitors of integrins αvβ6 and αvβ8
- 作者/单位: Roy A, Shi L, Chang A, Dong X, … Cherf G, … Baker D（UW-IPD + Genentech 等 40 人）
- Nature Communications, 2023, 14:5660
- DOI: 10.1038/s41467-023-41272-z ✅  PMID 37704610 / PMCID PMC10500007
- 链接: https://pmc.ncbi.nlm.nih.gov/articles/PMC10500007/
- 设计对象/靶点: αvβ6 / αvβ8 整合素（RGD 型 L-TGF-β 肽构象模拟），选择性抑制 TGF-β 激活
- 候选生成方法: 以 4UM9/6OM2 复合物结构为模板 → in silico 扫 PDB 找能容纳 8 残基 extended turn 的拓扑 → RosettaRemodel 生成 **200** 个不同长度/构象的 β-loop 模型 → 迷你蛋白支架
- 计算筛选器: 拓扑匹配 + 界面设计打分（正文以结构域筛选为主，未给统一阈值）
- MD: 否 / QM: 否
- 实验验证方法与通量: **蛋白酶切割富集 + 酵母表面展示**（先用 4 μM 胰蛋白酶 + 0.8 μM 糜蛋白酶 45 s、200 pM 生物素化 αvβ6 取 top 5%；第二轮 100 pM 取 top 1%）+ BLI + CAGA 报告细胞 IC₅₀ + Expi293F 800 mL 整合素制备 + 荧光体内成像
- **命中率原始数字（全文）**："We expressed and purified **9** enriched variants and measured binding for αvβ6 integrin using BLI; **all had subnanomolar binding affinity**（the original av6_3 binds to αvβ6 with a K_d of **1.2 (±0.006) nM**）"；"Four out of 9 designs showed preferential binding to αvβ8 with B8_BP_dslf showing the highest affinity and selectivity"；选择性量化："B6_BP binds αvβ6 with … K_d of **0.11 (±0.09)** and **580 (±40) nM** [αvβ8], respectively"；"B6B8_BP … binds to αvβ6 and αvβ8 with a K_d of **1.7 (±0.2)** and **7.3 (±1.2) nM**"；"B6B8_BP lacking the A39K mutation binds to αvβ8 with a K_d of ~7.3 nM whereas B6_BP containing the A39K mutation binds to αvβ8 > 500 nM"；功能："selectively inhibited αvβ6-mediated TGF-β activation (**IC₅₀ 32.8 ± 3.4 nM**)"
- 时间线位置: 展示"**蛋白酶切割 = 构象/折叠筛选**"这一廉价正交判据（只有折成目标 turn 的设计才抗切割），与 [B24] 的 SAPP/SEC-MALS 同属"用便宜实验替代贵的计算"

### [附：非 Baker 组对照，用于界定 MD/QM 归属]
- Listov D, Vos E, … **Fleishman S**（Weizmann；无 Baker），"Complete computational design of high-efficiency Kemp elimination enzymes", Nature 2025, 643:1421-1427, DOI 10.1038/s41586-025-09136-2 ✅, PMID 40533551, PMC12310539。⚠️ **作者列表经 Crossref 核验为 9 人、has_baker=False**，不得算作 Baker 组工作；其内部有 MD 与 QM 相关内容（本地全文 MD 命中 28 句、QM 29 句），可作为"MD/QM 在酶设计里能做到什么"的外部参照。
- Braun M, … **Hilvert D**（ETH Zürich），"Computational enzyme design by catalytic motif scaffolding", Nature 2025, 649:237-245, DOI 10.1038/s41586-025-09747-9 ✅, PMID 41339546, PMC12727513。同样 **has_baker=False**。
- 经典锚点（Baker + Hilvert + Houk 联合，供 QM/theozyme 溯源）：Siegel JB, Zanghellini A, Lovick HM, Kiss G, Lambert AR, … Hilvert D, Gelb MH, Stoddard BL, Houk KN, Michael FE, **Baker D**, "Computational design of an enzyme catalyst for a stereoselective bimolecular Diels-Alderase reaction"（该文作为 [B17] 参考文献原文出现在 Baker 侧正文引注中："…Houk KN, Michael FE, Baker D, Computational design of an enzyme catalyst for a stereoselective bimolecular Diels-Alder reaction"）。该锚点的 **QM 角色**＝用 QM 给出过渡态几何与催化基团排布；属"化学步建模"，不是全局筛选器。

---

## 二、漏斗级联总结

| 阶段 | 工具/论文 | 判据（含阈值） | 进入规模 → 剩余规模 | 出处 |
|---|---|---|---|---|
| 0 靶点/表位定义 | 冷冻结构/AF2 模型 + hotspot 指定 | 提供 interface hotspots（RFdiffusion binder 微调模型） | 1 靶点 | [B08] |
| 1 骨架生成 | Rosetta RIFdock+片段组装 / hallucination / **RFdiffusion** / RFdiffusion2(原子级) / RFpeptides / RFAA | 结构合理性、ROG（length/4.5）、二硫/拓扑约束 | 10⁵–10⁶ CPU-h → 10⁴–10⁶ 骨架 | [B03][B06][B08][B20] |
| 2 序列设计 | Rosetta LayerDesign/FastDesign → **ProteinMPNN**(1.2 s vs 4.3 min) → **LigandMPNN**(原子环境) | 平均 log-likelihood(NLL) 排序；每骨架 4–8 条 | 每骨架 8 条序列 | [B05][B27][B28] |
| 3a 自洽性反折叠（主闸口） | AF2 / AF2-with-initial-guess / fine-tuned RF2 / Chai-1 / AfCycDesign(环肽) | **mean pLDDT>80（严时>85/>90/>92）**、**pAE_interaction<10（严时<8/<7.5/<5）**、**pTM>0.8**、**RMSD to design<1.75–2 Å**、TM score to reference>0.5–0.7、AF3 **ipTM>0.6/0.85**（回顾） | **通过率 ~2.3%**（AF2 pAE<10）→ 削到"可下单池" | [B08][B09][B12][B22][B23][B24] |
| 3b 物理/化学项（正交二次筛） | Rosetta | **ddG/ΔΔG < −30 ~ −40 kcal/mol**、**CMS > 300–400 Å²**、**SAP < 35–45**、埋藏未满足氢键惩罚、holes、membrane-insertion potential、e-value>0.1（新颖度） | 数百千 → 46–96 个/靶（或 96–5000 展示库） | [B04][B12][B15][B23][B24][B29] |
| 3c 酶专用：活性位预组织 | **PLACER**（构象系综）+ QM/DFT 的 theozyme 输入 | apo/AEI/多态均要求关键 Ser-His 氢键、oxyanion hole H 键形成；"1.6% of AF2-passing designs predicted preorganized" | 96/批 固定送测；DFT→theozyme→RFdiffusion2 | [B17][B18][B19][B20] |
| 3d（罕见）刚性校验 | GROMACS 2018.4 + Amber99SB-ILDN MD（仅 [B34] 一次，与 AlphaFold/RoseTTAFold 三选一） | Cα RMSD < 3 Å（AF/RF 还加 pLDDT > 80） | Top 10% 打分结构 → 102 表达 | [B34] |
| 4 计算局部优化 | partial diffusion（timestep ~120/200 重采样）、SSM 热图、OrthoRep、聚类去冗余（335→80 cluster） | 每起始结构 25,000 重采样 → 32 条最自信 | 削减合成/表达预算 | [B14][B15][B22][B32] |
| 5a 高通量湿筛（贵→便宜替换） | **酵母表面展示 + FACS + NGS**（10⁶–10⁷ DNA 多样性）、**MP3-seq**（>10⁵ 对/实验）、proteolysis/chymotrypsin 富集筛选 | SC₅₀、top 0.1%/1%/5% 收集频率、LFC 与 P_adj≤0.05 | 10⁴–10⁵ 设计 → 数十命中 | [B06][B12][B16][B23][B32] |
| 5b 中/低通量直测（省掉展示） | **E. coli/昆虫细胞 96 孔表达 + 单点 BLI(10 μM)/SPR**；**SAPP**（数百设计/天，192 反应/2 h，SEC ~300/天） | 表达量、SEC 单体/目标寡聚态、CD、DSF(Tm)、BLI ≥50% 阳性对照响应 | **46–170 个/靶** | [B05][B08][B14][B21][B24] |
| 6 确证 | X 射线/cryo-EM（与设计模型比对）、ITC、NMR HSQC、FP 探针标记、细胞功能报告基因 | 直径偏差 <2%、Cα RMSD 11.5 Å/540 亚基、4 个 X 射线结构 | 数个 | [B08][B11][B17][B22][B25][B28] |
| 7 反馈回炉 | DMS + 能量函数再训练（beta_jan25 去 clashing bias）、失败分型（Type I/II） | Δstability>1.0；156/16,000 突变 (~1%) | 新打分器 | [B09][B26] |

**成本与命中率的总账（可直接引用的三组最硬数字）**
1. Rosetta + 展示库时代：15,000–100,000 设计/靶点、~50 万设计被实验表征，困难靶点（TIE2、CD3δ）**<10 个结合体 / 100,000 库**；100,000 CPU 小时产 100,000 候选（[B06]）。
2. RFdiffusion + AF2 过滤时代：**每靶点仅 95 个设计、实验成功率 19%**，比旧战役高约两个数量级（作者把这 100× 拆成 10× 归 RFdiffusion、10× 归 AF2 过滤）（[B08]）。
3. 2024–2025 时代：TNFR 家族 **96 设计 → 28/94 结合（30%），K_D 198 pM**（[B14]）；金属水解酶 **96 设计 → 11/96 具 >10³ M⁻¹s⁻¹ 活性、零-shot 最优 >10⁴ M⁻¹s⁻¹**（[B18]）；抗体/VHH 仍只有 **0–2%**（[B22]）。

**实验侧"低成本高通量"如何替代昂贵验证（对应问题 4，逐条出处）**
- **酵母表面展示 + 多轮 FACS + NGS**（把 10⁴–10⁵ 设计的结合信息压成测序计数）：[B06] DNA 多样性 1×10⁶–1×10⁷、每轮只取 top 0.1%，并用 SC₅₀（50% 分选浓度）作为亲和力代理排序；[B22] 每靶点 9,000 设计；[B23] 每靶点库规模 96–5,000、从"数十万序列"削到库；[B32] 并行测 67 vs 4,310 设计、再对命中做 SSM 全饱和突变热图与组合突变库；[B42] 2,689 设计 → FACS + NGS → 4 个高度富集设计。
- **不依赖展示的"直接测"**：[B08]/[B14] 用 E. coli/昆虫细胞 96 孔表达 + 单点 BLI（10 μM，判据 = ≥50% 阳性对照响应），刻意省掉展示库；[B24] SAPP 把这条路做成产线（192 反应/2 h、SEC 15 h/192 样、~300 样/天/台、单设计成本≈"几条 DNA 寡核苷酸"、每天数百设计）；[B20] 用无细胞 IVTT（96 个/批）直接把酶送测。
- **条形码并行 PPI 测定**：[B16] MP3-seq（重编程酵母双杂交 + 条形码配对 + NGS），"scales to over 100,000 interactions"，一次实验覆盖 2×2/1×2 设计异二聚体全部配对，并用 LFC + P_adj≤0.05 作定量判据。
- **亲和力成熟的廉价化（用误差校正文库替代从头再设计）**：[B22] OrthoRep 连续超突变把几十–几百 nM 推到个位数 nM 且保持表位选择性；[B32] SSM→组合库→递减浓度分选；[B06] 同样走 SSM + 5–15 个组合突变。
- **Kd 分布（各篇报告的实测范围，用于判断"多少算力换多少亲和力"）**：pM 级 198 pM（TNFR2，[B14]）、510 pM（VirB8，[B06]）；低 nM 级 1.2 nM（αvβ6，[B44]）、1.9 nM（蛇毒 3FTx，[B43]）；中 nM 级 14–82 nM（[B21] PRI28 14 nM、[B23] KITbp 65 nM / FCRL5bp 82 nM、[B22] HA 78 nM）；数百 nM 级（IDP/柔性表位：28–750 nM，[B21]；蛇毒首轮命中 842 nM，[B43]）。
- 注：**卡片编号按加入顺序而非年份**（B37–B44 是补齐 MD/QM 证据与高通量证据后追加的），时间顺序请看第三节。

---

## 三、方法演进时间线（2019 → 2026，筛选逻辑为什么改）

- **2019｜多态开关 + MD 诊断**
  [B01] LOCKR 用 HBnet + 三态自由能模型设计别构开关；[B02]（Barros/Baker/Amaro, JCTC 2019）用 500–1000 ns × 37 设计（>180 μs）做**回顾性失败诊断**，并提出 MD+ML "could act as a screening step"。**为什么**：Rosetta 静态打分会给出"预测成功但实验低亲和"的结果，怀疑熵项缺失。
- **2020｜口袋枚举 / 对称域融合**（背景锚点：PNAS 2020 口袋枚举 10.1073/pnas.2005412117、PNAS 2020 lanthanide TIM barrel 10.1073/pnas.2008535117）——继续加物理约束，不改判据形态。
- **2021｜判据第一次换轨：网络即目标函数**
  [B03] hallucination：129 送测 → 27 成功（~21%）。**为什么**：Rosetta 无法为全新 fold 提供可靠的"会不会折"判据；结构预测网络的置信度是天然更好的判据。同期 [B04] 把"埋藏未满足氢键"做成可两两分解的惩罚项，说明当时仍在修补物理打分。
- **2022｜序列端算力革命 + 湿筛极限**
  [B05] ProteinMPNN：1.2 s vs 4.3 min、回收率 52.4% vs 32.9%、96→73 可溶→50 目标态；NLL 用于排序。**为什么**：要把"每骨架 8 条序列 × 十万骨架"变成可行计算，并让界面/组装体设计不再依赖人工微调。
  [B06] Cao：10⁴–10⁵ 设计/靶 + 10⁶–10⁷ 展示库 + NGS，~5×10⁵ 条实验标注。**为什么**：这是唯一能把"ddG/CMS 哪个指标真正预测结合"回答清楚的代价——也暴露了"每战役十万级"不可持续。
  [B07] Linsky/Strauch：30,000 设计 → 6,200 稳定（~21%）。
- **2023｜生成端革命 + 自洽性筛选标准化**
  [B08] RFdiffusion：**95 设计/靶 → 19%**，两个数量级提升；[B09]：把 AF2/RF2 的 **pAE_interaction<10** 定为闸口，明确 **仅 ~2.3% 通过、30 GPU-秒/设计**、10× 提升、并给出 Type I/II 失败分型；[B10] 荧光素酶：7,648→3 → 改 ProteinMPNN+AF2 后 46→2；[B12] 螺旋肽：18,000 骨架库 + "pAE<10, pLDDT>92, pTM>0.8, RMSD<1.75 Å, ddG<−40" 成套闸口；[B20] luciferase 之外的 [B11] 小 β 桶（80→72→43→28→16）给出折叠漏斗各段比例。**为什么**：生成模型解决了"有没有好的骨架/界面形状互补"，于是瓶颈整体迁移到"能否便宜地预测一个复合物会不会按设计结合"。
- **2024｜全原子化 + 新模态 + 判据失灵暴露**
  [B13] RFAA（小分子/金属/共价修饰进模型）；[B28] LigandMPNN（原子环境条件化序列设计，分子交互残基回收率 63.3% vs 50.4/50.5）；[B15] 环肽（AfCycDesign + ddG/SAP/CMS，335→80 聚类以省合成预算）；[B14] TNFR partial diffusion（把"筛选"与"再优化"合并）；[B32] 免疫检查点（67 vs 4310 双轨）；[B16] MP3-seq（>10⁵ PPI/实验，设计集 ~20% 成功）；[B22] 抗体设计首次尝试，**AF2 失灵 → 命中率 0–2%**，作者转而微调 RF2 并事后指出 AF3 ipTM>0.6/0.85 才是该用的闸口。**为什么**：模态一旦超出"纯蛋白"（抗体 CDR、配体、核酸、金属），自洽性判据失效，就退回"展示库 + 亲和力成熟"，这就是为什么抗体方向没有复现 19%。同年 [B34]（buttressed loops）出现本调研中**唯一一次 MD 进入入选判据**（GROMACS/Amber99SB-ILDN，Cα RMSD<3 Å，与 AlphaFold/RoseTTAFold 三选一，验刚性），[B42]（EndoTag）则显示当目标从"结合"升级为"触发内吞"时命中率跌到 8/170 与 4/2689。
- **2025｜酶设计年 + 湿实验产线化**
  [B17] 丝氨酸水解酶（PLACER 预组织筛选，1.6% 通过、45→38=84%、812 个设计全谱系分析）；[B19] PLACER 论文**明确以成本否弃 MD 作为筛选器**；[B18]（在线）金属水解酶 **DFT theozyme → RFdiffusion2 → 96 送测 → 11/96**、零-shot >10⁴ M⁻¹s⁻¹；[B20] RFdiffusion2 原子级 motif scaffolding（41/41 vs 16/41；96→4 与 96→11）；[B21] IDP 结合体（阈值 pAE<10/pLDDT>90；二级结构指定使通过率 ×50，命中率 3/94、5/78）；[B27] DNA 结合蛋白（21,488 + 12,273 设计、≥10,000 通过全过滤/靶）；[B35] RFdiffusion3 预印本（全原子 one-shot，**算力 1/10**）。**为什么**：催化设计要求"沿反应坐标的多个态都对"，静态自洽性判据不够 → 需要便宜的系综判据（PLACER）与原子级生成（RFdiffusion2/3）。
- **2026｜漏斗工程化 + 数据回炉 + 官方收官判断**
  [B23] β-pairing（按 in silico 通过率反推下单库规模 96–5000，pM–mid nM）；[B24] SAPP（数百设计/天、单设计成本≈几条寡核苷酸、SEC 为唯一瓶颈 ~300/天）；[B26] 用 21 个 DMS 库/16,000 突变重训 Rosetta 消除 clashing bias；[B25]/[B41] 准对称纳米笼与四组分笼（cryo-EM 与设计偏差 2%；四组分笼的 AF2 判据同时要求"该成的界面成、不该成的界面不成"）；[B36] Baker 组综述宣布 fold/组装体/蛋白-蛋白结合体"close to being solved"，把未解问题定位为"高活化能反应催化 + 开关/纳米机器"。

---

## 四、MD / QM 的真实角色判定

**判定（高置信，基于本地缓存 46 篇全文（44 篇 Baker 署名 + 2 篇非 Baker 对照）的逐句检索，脚本 `mdqm.py` + 关键词复核，输出 `mdqm.out`）：**

1. **MD 不是主筛选器；它的两个真实身份是"事后机理顾问"和（极少数情况下）"可选的刚性校验闸口"。**
   证据：在 Baker 署名全文里，MD 相关句子绝大多数落在 Methods/讨论的机制分析（[B10] "We used a combination of DFT calculations and MD simulations to investigate the basis for LuxSit activity"；[B37] FAP：EF1p2_mFAP2b 在 apo/Ca²⁺/DFHBI/双配体四种条件下 MD，说明 Ca²⁺ 结合把自由能面推向荧光态；[B38] oligomorphism：对每个三聚/二聚组件及其界面跑 MD，再用轨迹快照重建观察到的多种架构；[B39] conformational dynamics（Kay/Baker, PNAS 2023）用 NMR 而非 MD 抓激发态）；
   最直白的判据来自 Baker 组自己的 PLACER 论文：**"The most general way to evaluate such preorganization is molecular dynamics simulations, but … such simulations are computationally expensive and cannot be applied to large numbers of designs"**（[B19]）——这句是本调研对"为什么不用 MD 筛"的一手答案。
   **唯一的肯定反例（需如实记录）**：[B34] buttressed-loop 重复蛋白（Nat Chem Biol 2024）把 MD 写进了入选流程——"Top 10% scoring structures were further tested by in silico validation methods such as **molecular dynamics simulations (Cα RMSD < 3 Å)**, AlphaFold (pLDDT > 80, Cα RMSD < 3 Å) or RoseTTAFold (pLDDT > 80, Cα RMSD < 3 Å)"；"We performed molecular dynamics simulations using **GROMACS (2018.4)** with the **Amber99SB-ILDN** force field"，用途是"rigidity of the design models was evaluated"（刚性/构象漂移），且与 AF/RF 属**三选一的可互换手段**，不是必过关口。
   另一次把 MD 推向"筛选步骤"的是 2019 年 JCTC（[B02]，37 个设计、>180 μs），其结论是"MD could act as a screening step"；但此后 Baker 组的 binder/enzyme 战役里没有任何一篇把显式溶剂 MD、MM/PBSA、MM/GBSA、FEP/TI 或 metadynamics 作为入选判据（逐关键词检索命中数：**MM/PBSA·MM/GBSA = 0；free energy perturbation/TI/alchemical = 0；metadynamics/umbrella = 0；GROMACS/OpenMM/NAMD = 仅 [B34] 的 GROMACS + [B29] 的 Namdinator（晶体学工具，非 MD）**；OPLS 仅在 [B26] 参考文献标题与两篇**非 Baker** 对照论文（kemp2025 的 EVB/OPLS-AA、motifscaffold2026 的 GROMACS）中出现）。
2. **QM 只在"化学步"出现，且是设计输入而非筛选器。** 具体形态只有两种：
   (a) 用 **DFT 定过渡态/theozyme 几何**作为生成模型的输入——[B18] "starting from **quantum chemistry**-derived active site geometries"、"We began by using **DFT** to identify the transition-state geometry…"；[B17] "placed the catalytic sidechains around a **QM-optimized transition state**"；[B20] "theozyme … generated using **quantum chemistry**, protein structural analysis and/or chemical reasoning"；[B10] 的 DFT 反应自由能剖面（Int1/TS1/Int3/OSS-TS2）。
   (b) 用 **TD-DFT/QM 处理光物理与发色团**——[B40] 叶绿素特殊对（"time-dependent density functional theory calculations … excitonically coupled"、B3LYP/6-31G* 几何优化、PigmentHunter 光谱模拟、Amber18 + 短 MD 做力场参数）；[B37] FAP 的 DFHBI 用 Gaussian 几何优化 + GAFF 参数化。
   没有一例把 QM 用于成千上万候选的排序——原因与 MD 相同：单分子成本。
3. **真正的"入选判据"三件套**：AF2/RF（或 AF3 ipTM）自洽性阈值 + ProteinMPNN/LigandMPNN 序列似然 + Rosetta 界面物理项（ddG、CMS、SAP）；酶加 PLACER 预组织；小分子/全原子任务加 RFAA/RFdiffusion2 级原子约束。MD/QM 的位置是"**在闸口之间解释与提供约束**"，不是"闸口本身"。
4. **当自洽性判据失效时（抗体、IDP、小分子），Baker 组的应对不是加 MD/QM，而是加便宜的高通量湿实验**：酵母展示 + FACS + NGS（[B06][B22][B23][B32]）、MP3-seq（[B16]）、SAPP（[B24]）、OrthoRep/SSM 亲和成熟（[B22][B32]）。这正是问题"实验侧低成本高通量筛选如何替代昂贵验证"的答案。

---

## 五、未能核实的问题清单

1. **2019 篇（[B01]）漏斗分母**：正文里未检索到统一口径的"设计 N 个 / 筛 M 个 / 命中 K 个"计数（LOCKR 系列按 Cage–Key 组合分别报告，且部分数据在 Supplementary）。要判定"Rosetta 时代多态开关设计的具体命中率"，需要补充读取其 Supplementary/Methods 表格（本次未获取到可解析的 SI 文件）。
2. **[B13] RFAA（Science 2024）与 [B28] LigandMPNN 的送测→命中分母**：Europe PMC 无 PMC 全文（RFAA）或我只取到摘要（LigandMPNN 用摘要中"over 100 experimentally validated…four X-ray crystal structures"）。缺观察：正文 Methods 中每靶点的 96/几十名额与命中率。若能取得 SI/正文 PDF，可确认"全原子路线把命中率从 X 提到 Y"的具体数字。
3. **RFdiffusion3（[B35]）与"半胱氨酸蛋白酶/ RFOptimization"（2025–2026 预印本）尚无同行评审的命中率数字**。当前只核到"one tenth the computational cost"这一 in silico 论断（预印本摘要，bioRxiv 页面抓取）。判定"全原子 one-shot 是否真的取消 AF2-refold 闸口并提升实验命中率"需要其正式发表版的实验表格。
4. **"2024 HydrogenBonds"这一具体模型名**：按题名/全文检索（`"HydrogenBonds"`、`"MPNN-HB"`、`TITLE:hydrogen AND AUTH:"Baker D"`）**未找到对应的 Baker 2024 论文**。实际可核的氢键设计谱系是 Boyken 2016 Science（10.1126/science.aad8865 ✅）、Maguire/Baker/Kuhlman 2018 JCTC（10.1021/acs.jctc.8b00033 ✅）、Coventry & Baker 2021 PLoS CB（10.1371/journal.pcbi.1008061 ✅）。需要用户提供该名称出处才能进一步核对。
5. **"Baker lab picobodies" 论文不存在/无法核实**：Europe PMC 以 `TITLE:"picobody"`、`picobody` 检索仅命中非 Baker 的牛源超长 CDR-H3 综述（10.1016/j.biotechadv.2023.108120，作者 Passon 等，与 Baker 无关）。因此"Baker 组 2024 picobody 工作（RFdiffusion + 酵母展示，pM 级）"**未能核实**，本调研不把它计入 Baker 漏斗证据。要判定需给出具体 DOI 或作者。
6. **RFantibody（IgG Fc 结合域/抗体设计 Science 类工作）**：以题名"Programmable de novo design of IgG Fc-binding domains"与 `AUTH:"Raman" AND AUTH:"Baker D" AND "Fc"` 检索**均无命中**；Crossref 只返回 2012 生物物理期刊会议摘要与 2007 Nature 旧文。因此该项**未能核实**，未写入卡片。
7. **Baker 组"自动化/自驱动实验室"闭环论文（若存在，例如以设计-构建-测试自动化机器人为主体、报告数百设计/周与成功率的 Nature/Nat Methods 论文）**：我检索到的只有 [B24] SAPP（半自动、人工不缺席）与 "High-Throughput De Novo Protein Design Yields Novel Immunomodulatory Agonists"（bioRxiv 10.1101/2025.10.12.681920，Abedi/Coventry/Krishnakumar 等，未获全文，无命中率数字）。判定"是否存在完全闭环（无人决策）的设计-合成-测试流水线并给出量化成功率"缺少可核正文。
8. **用户点名的判据（MM/PBSA、MM-PSA、OPLS/隐式溶剂、RoseTTAFire、FEP+、metadynamics）在已刊 Baker 论文中基本不存在**：对 46 篇缓存全文逐关键词检索（脚本 `mdqm.py` + 二次复核脚本，命中明细见本报告第四节第 1 条）：MM/PBSA·MM/GBSA、free energy perturbation/TI/alchemical、metadynamics/umbrella sampling、RoseTTAFire、MMPSA 均**零命中**；GROMACS 仅命中 [B34]（作为可选刚性校验），NAMD 命中是 Namdinator（晶体学，非 MD），OPLS 命中是参考文献标题与非 Baker 对照论文。**尚缺的观察**：若这些判据确实在 Baker 内部工作流中使用，只能来自 IPD 内部 run 记录、GitHub issue/工具链文档或未刊 SI，本次未获取；因此"这些判据是否曾在未发表流程里出现"这一问题**当前无法判定**，只能判定"它们没有出现在已刊论文的入选判据里"。
9. **每个漏斗阈值的"来源可信度"**：多数论文对阈值写作"per-campaign 调整"（如 [B12] "Precise metrics cutoffs changed for each design campaign to get to an orderable set"、[B23] "cutoff values … varied somewhat for each target protein"）。因此"固定通用阈值"其实是各篇挑出来的可达标值，真实判据是"把集合削到可下单规模"。要精确复现需各篇 Supplementary Table（如 [B23] 的 Supplementary Table 1 记录了逐靶库规模与阈值），本次仅拿到正文。

---

### 附：本次调研的可复现路径（便于后续核对）
- 抓取/检索脚本：`..\data\interim\baker_lit\lit.py`（Europe PMC search + fullTextXML、Crossref works、PubMed）、`dlall.py`（两批共 46 篇全文缓存到 `ft/`，另 2 篇经内联脚本补抓 buttressed loops 与 four-component cages）、`mdqm.py`（MD/QM 逐句分类，输出 `mdqm.out`）、`verify.py`（共 53 条 DOI 的 Crossref 逐条核验，输出 `verify.out`；本报告内出现的 60 个 DOI 中，除期刊内文引用的第三方文献外全部已核验 ✅）。
- Europe PMC 全文接口示例：`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10468394/fullTextXML`（HTTP 200）。
- DOI 核验示例：`https://api.crossref.org/works/10.1038/s41586-025-09746-w` → `{"has_baker": true, "vol": "649", "page": "246-253"}`。
- 两条 Europe PMC fullTextXML 返回 HTTP 500（PMC7532806、PMC9293396），已改用 PubMed 摘要并标注"摘要级"。
