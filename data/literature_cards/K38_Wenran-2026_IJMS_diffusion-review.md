# [K38] 扩散模型蛋白结构设计的综述——把"生成器之间怎么比"和"验证判据够不够"写成一张对照表

Li Wenran, Cadet Xavier, Medina-Ortiz David, Davari Mehdi D., Sowdhamini Ramanathan, Bessafi Miloud, Damour Cedric, Li Yu, Miranville Alain, de Brevern Alexandre G.\*, Cadet Frederic\*
International Journal of Molecular Sciences 2026, 27(16):7151 · DOI 10.3390/ijms27167151 · PMID 42653156 · PMCID PMC13513569
开放获取（CC BY 4.0）· 文章类型标注为 Review · 代码链接核对日期原文写作 accessed on 27 July 2026

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 第 120 行，编号 **K38**（组：通用方法学; 口径对照；文献类型列=综述） |
| 文献类型 | **综述（Review）**——不是方法论文。作者自述："No new experimental data were generated in this study, as this article is a review of previously published research."（Data Availability 原句），因此**没有自己的实验台账、没有命中率、没有任何数值阈值** |
| 本文取回方式 | Europe PMC 检索（按 DOI）+ fullTextXML 通路，登记于 `data/literature_cards/inventory.json`（`fetch_channel=epmc_search_then_fulltext`） |
| 本地全文 | `fulltext/K38_PMC13513569_fullTextXML.xml`（原始抓取）→ 去标签纯文本 `fulltext/K38_PMC13513569_text.txt`（本卡**唯一**引句底稿） |
| 身份核验 | 底稿开头身份块逐字含 "Diffusion-Based Protein Structure Design: Geometric Modelling, Validation Strategies, and Thermodynamic Challenges"、"10.3390/ijms27167151"、"PMC13513569"、"1 Review" 与 11 位作者署名，确认**这份全文就是 K38 本身**（非引用它的其它论文） |
| 对照底稿 | `sources/cost-benchmarks.md` §3.7（第 135–138 行）与 §六表格行 202、205：那里已核过本篇四句关键论断；本卡所有引句一律以**本地全文**为准，差异记在第 7 节 |
| 证据级别 | **全文级**（本卡全部引句均可在 `fulltext/K38_PMC13513569_text.txt` 里逐字命中；见第 9 节自检） |
| 未取到的部分 | Figure 1/2 与 Figure A1 只有图注文字（图像未取）；Table 1/2/3/A1 是**去标签后的线性文本**，行列结构靠单元格顺序复原，个别行跨列归属需人工判断；补充信息与原文 PDF 未取 |
| 抽取侧风险（写卡时已避） | 该底稿把行内公式拆成 "x 0"、"α ¯ t"、"C α"、"S E ( 3 )" 这类带空格的形式，还残留 "Erratum in" 之类的题录串；本卡凡涉公式与带希腊字母/特殊减号的句子**一律不做英文引号引用**，只做中文转述 |

## 1. 这篇到底解决什么（一句话）

**一句话**：它不提出新模型，而是把"扩散模型造出来的蛋白骨架，凭什么说它算成功"这件事拆成一张**分层判据表**（每个指标"测什么"配一栏"不能确立什么"），并给出这条社区里最硬的一句否证：预测置信度、结构自洽性、novelty/diversity 都**不等于**热力学稳定性、可实验折叠与功能。

它要填的缺口，作者自己写在引言末："Although several reviews have described generative modelling for proteins, the relationships between molecular representation, geometric conditioning, physical consistency, computational validation and experimental evidence are still not fully understood"——即已有综述各说一段，没人把**表示—条件化—物理一致性—计算验证—实验证据**串成一条链。

问题为什么难（作者的出发点，全是原文）：蛋白工程的目标是"找到既满足结构又满足功能、热力学、动力学和可开发性约束的序列"——"The objective of protein engineering is to identify amino-acid sequences that adopt specified three-dimensional structures while satisfying functional, thermodynamic, kinetic and developability constraints"；这是个天生多目标问题，"The inverse problem is inherently multi-objective because sequence, structure, conformational dynamics, stability, molecular recognition, and biological function are strongly interconnected across a complex, high-dimensional energy landscape"；而即便靶折叠已定，"the accessible sequence space grows combinatorially with chain length"，穷举不可行。AlphaFold2 之后大家手里的其实是**预测器**，不是**设计器**，作者把这条界线写成全篇的锚点："However, structure prediction in isolation does not resolve the inverse design problem"，接着定义："Conversely, a design method must generate candidates that satisfy predefined structural, functional or physicochemical constraints"。

声明的三项贡献（原文逐条）："This review makes three key contributions"——① 建立扩散形式与坐标/残基 frame 表示之间的概念框架；② 按任务对代表性方法做批判性比较，重点是条件化机制、评测协议与可得实验证据；③ 把"几何合理性 / 结构自洽 / 预测可设计性 / 热力学稳定性 / 生物功能"这五件事明确区分开。它落给读者的立场是：扩散模型只提供候选生成与约束满足，其余要在更大的工程闭环里补——"Within this framework, diffusion models offer candidate generation and constraint satisfaction capabilities within broader protein engineering workflows"。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **置信度指标被当成稳定性/功能证据——这是全篇的主难点**。现象/原句证据：作者先把 TM-score 与 pLDDT 拆开（"TM-score and pLDDT should not be interpreted equivalently"），随后给出本文最常被转引的那句判决：**"A high pLDDT value indicates that the predictor is confident in the local geometry, but it does not provide direct evidence that the sequence is thermodynamically stable, experimentally foldable, or functionally active"**。同类判决在 Table 3 里被逐条列出（pLDDT 那一行的"What It Does Not Establish"写的是 "Experimentally measured accuracy, thermodynamic stability, expression, foldability or function"）。→ **作者做了什么**：不给新分数，改给**报告规则**——"The following should be reported separately: local geometry; sequence-structure recovery; distributional novelty; and task-specific constraint satisfaction"，并要求一旦设计目标需要物理或功能解释，就必须在计算指标之外补一层："these computational criteria should be supplemented with physically motivated calculations and experimental measurements"。→ **仍留下的代价**：整篇没有一处数值阈值（多少 pLDDT 算够、RMSD 卡在哪），也没有给出"这样分层之后实验成功率变化多少"的任何数字；它只证明了"不该把 A 当 B"，没给出"A 与 B 之间的定量桥"。
2. **循环验证：生成器和评测器同源**。现象/原句证据："Circular validation may also arise when generators and evaluators share related architectures, training data or evolutionary information"，且 "As benchmark outcomes depend on datasets, sampling budgets, evaluators and filtering protocols, meaningful comparisons require the transparent reporting of each component of the evaluation pipeline"——所谓 designability 判定本身就靠"逆折叠 + 独立结构预测复算"这一自洽回路（"The designability of a generated backbone is typically assessed through a self-consistency procedure in which sequences are designed for that backbone and subsequently evaluated using an independent structure-prediction model"）。→ **作者做了什么**：把控制项写成清单——"It is therefore recommended that benchmark protocols report structure-level redundancy filters, temporal splits, evaluator independence, sampling budgets and the number of candidates retained after filtering"，并要求"Interpretation of the results also requires controls for training-data leakage, evaluator dependence and candidate-selection bias"。→ **仍留下的代价**：这是**建议不是执行**——本文没有实现任何一项控制；对 PDB-Struct 的排序结论（"PDB-struct suggests that encoder-decoder methods generally outperform structure-prediction-based methods in terms of refoldability, recovery, and stability metrics"）也是原样转述，没有核查其评测器是否真的独立于被比模型。
3. **实验失败不报，漏斗数字就无法比**。现象/原句证据：作者指出各层实验统计"The proportion of candidates that have been tested through experimentation, and the success rate at each validation stage, are essential for the comparison of generative methods"，紧接着承认现状——"However, these statistics are currently reported inconsistently across studies"。→ **作者做了什么**：把实验验证拆成三层并逐层给出可观测项：先表达/溶解性/单分散（"The preliminary evaluation may encompass recombinant expression, solubility, and monodispersity"），再结构验证（"The validation of structures may be achieved through a variety of methods, including circular dichroism, nuclear magnetic resonance, crystallography, and cryo-electron microscopy"），最后功能层（"Depending on the objective of the design, functional validation may require measurements of binding affinity, specificity, catalytic activity or cellular response"）；总原则是"It is important to distinguish between experimental validation and computational ranking, and this distinction must be reported at several levels"，减员侧的收口是"In order to reduce survivorship bias and publication bias, experimental failures should be reported wherever possible"。→ **仍留下的代价**：**本文未解决**——它自己没有汇入任何失败数据，也没有建立可复用的失败台账；给出的只是"应当报"的规范，各层的实测通过率仍是空的。
4. **学习分布 ≠ 平衡系综，构象多样性被当成热力学结论**。现象/原句证据："A collection of structurally diverse samples should not be automatically interpreted as an equilibrium ensemble, since the generated conformations may lack physically meaningful populations, kinetic connectivity, or transition pathways"；对 Mac-Diff 这类模型写得更直白——"the resulting samples should be interpreted as learned conformational distributions rather than as equilibrium ensembles with physically calibrated populations or kinetic connectivity"；理论层的总结是"Recovering equilibrium populations requires calibrated statistical weights or free-energy differences, whereas kinetic interpretation additionally requires information on state connectivity and transition rates"。→ **作者做了什么**：给出三分布不等价（数据经验分布 / 模型学习分布 / 热力学平衡分布），并把独立验证写成前置条件——**"ensemble-oriented diffusion models must be validated against molecular simulations, experimental observables, or independently estimated free-energy landscapes before thermodynamic or kinetic interpretations can be assigned"**；同时提醒动力学解释还要连通性与跃迁速率（"In order to support the thermodynamic interpretation, it is necessary to associate the sampled states with meaningful statistical weights"）。→ **仍留下的代价**：它列了出路却没定价——同节即承认"Force fields remain approximate, solvent effects may be uncertain, and free-energy calculations are computationally demanding"，并要求"Physics-informed generation should therefore be evaluated empirically rather than assumed to improve every design objective"；全文没有任何一条"经此验证后判断更准"的量化案例。
5. **可开发性/表达失败根本没进训练数据，因此预测器看不见它**。现象/原句证据："A generated sequence or structure may appear computationally designable, yet exhibit poor recombinant expression, limited solubility, aggregation, chemical instability, proteolytic sensitivity, immunogenicity or unsuitable oligomerisation"，作者解释原因——"The properties in question are influenced by environmental and manufacturing conditions that are only weakly represented in most training datasets"；训练集侧同源问题也写明了："Structural databases demonstrate an overrepresentation of proteins that are experimentally tractable, stable and well-ordered, while membrane proteins, intrinsically disordered regions, transient assemblies, alternative conformational states and unsuccessful experimental constructs remain comparatively underrepresented"。→ **作者做了什么**：要求把评价范围从"折叠回收 + 靶活性"扩展到表达量、单分散、长时稳定与下游制备兼容性，并把这类失败列为独立局限（原文用 "An additional limitation pertains to the developability of the protein" 起手），报告侧配套要求"benchmark studies should report the computational cost, software versions, random seeds and candidate-selection procedures alongside structural and functional metrics"。→ **仍留下的代价**：**本文未解决**——没有给出任何可操作的 developability 阈值或面板，只把它列为"需要综合评估"的方向。
6. **复现性本身是难点（软件层，而非生物层）**。现象/原句证据："discrepancies in code accessibility, model weights, licences, hardware, sampling parameters and unpublished filtering procedures have the potential to impede independent replication"；生成本身也贵——"sampling can be computationally expensive, and performance can be sensitive to noise schedules and guidance parameters"。→ **作者做了什么**：把成本与配置写进报告要求（同上第 5 条的 cost/versions/seeds/procedures 清单），并在附录 A 给全 16 个模型的代码链接与训练集规模（"Models mentioned in this review have been implemented as open-source tools"）。→ **仍留下的代价**：Table A1 的数据量列大量写 "-"（即原文没查到），且链接只在 2026-07-27 那一刻核过；本卡不能据此断言任何模型"今天仍可下载/可跑"。
7. **我们采证时遇到的坑（不是作者的难点，但影响这张卡能用哪些句子）**：这篇综述正文的**引文编号错位**——正文把 Mac-Diff 标为 [39]（"Mac-Diff addresses a different application, learning distributions of protein conformations from molecular dynamics trajectories"），把 DiffDock 标为 [38]，而参考文献表里 [38] 才是 Mac-Diff（Wang B 等，Nat. Mach. Intell. 2026）、[39] 是 Protpardelle（Chu A E 等，PNAS 2024）、DiffDock 是 [17]（Corso G 等），附录 Table A1 又用 [38] 指 Mac-Diff。→ **我们做了什么**：本卡凡引用带编号的方法归属，一律以"底稿文字 + 模型名"为准，不用它的编号；数字只录 Table A1 里能在本地底稿逐字命中的那几条，并标注为二手转录。→ **仍留下的代价**：本文未解决（综述无勘误），任何要拿这篇当"某模型用了多少数据"的一手依据的人都得回溯原论文。

## 3. 方法与工作流程（综述的"方法"=它的组织方法；每步：输入 → 操作 → 判据 → 输出规模）

### 它比的是哪些工具（组织用的工具箱，不是它自己跑过的东西）

- **生成器族**：RFdiffusion / RFAA / RFdiffusionAA / RFdiffusion2 / RFdiffusion3（RoseTTAFold 系，含全原子与活性位点条件化）、FrameDiff / FrameDiPT / TDS / VFN-Diff / SMCDiff（残基局部刚体 frame 上的扩散）、Genie / Genie2 / Genie3（取向残基云 + 坐标加噪）、Chroma（用户自定义能量/语义约束）、ProteinGenerator（序列空间扩散、多态设计）、Mac-Diff（构象系综生成）、Protpardelle（全原子联合建模）、AlphaFold3 与 DiffDock（扩散模块但主职是预测/对接）。
- **验证侧工具**：MolProbity（立体化学）、TM-score / RMSD / pLDDT / sequence recovery（结构与置信度）、自洽性 designability（逆折叠 + 独立预测器复算）、novelty（对 PDB 最近邻相似度）、diversity（聚类数/总数）、Melodia（几何/拓扑描述子，作者明说它不是生成模型的基准）、PDB-Struct 与 Scaffold-Lab（统一基准）。
- **物理与实验侧（作者列为"应当补上的独立层"，不是本文用过）**：分子力学、分子动力学、自由能计算、Boltzmann generator 与 Markov state model；实验三层（表达/溶解性/单分散 → CD/NMR/晶体学/冷冻电镜 → 结合/特异性/催化活性/细胞响应）。
- **本文自己完全没有的环节**：无自做生成、无自做筛选、无湿实验、无计算成本测量（Data Availability 原句："No new experimental data were generated in this study"）。

### 工作流程表（照它的章节推进顺序重放，7 步）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | 扩散结构生成方向的公开方法 + 已有生成模型综述 | 不按数学形式排队，改按"分子表示 × 设计目标 × 代表性应用"三轴重排；作者自述动机："The following comparison is organised around practical questions that arise when selecting a method" | 纳入判据=是否直接服务三维结构生成，原句："Sequence-only diffusion, general protein language models, inverse-folding methods and molecular docking approaches are considered only when they contribute directly to structural generation workflows and are not reviewed comprehensively"；**原文未给数值阈值** | Table 2：7 类（backbone generation / motif-guided / programmable / all-atom / interaction prediction / sequence-structure co-design / ensemble generation） |
| W2 | DDPM 离散形式 + 连续时间 score-based SDE | 把两套写法并排推一遍：式 (1)-(13)（前向马尔可夫链、闭式边际、噪声预测参数化、简化训练目标、正反 SDE、probability-flow ODE、denoising score matching），Table 1 统一 16 项记号；附录 B 用 Gram-Schmidt 定义残基局部 frame 与 SO(3)/SE(3)/E(3) 关系 | 几何判据=手性是否守恒，取舍原句："SE(3)-equivariant formulations are therefore commonly used when preserving molecular handedness is required" 与 "E(3)-equivariant formulations may still be useful in appropriate settings, but their relationship to chirality should be stated explicitly"；**原文未给阈值**（注意底稿里同一篇的 SE(3)/E(3) 有时被拆成带空格的 "S E ( 3 )"，本卡只引紧凑写法那几处） | 三族架构对照（Fig 2：RoseTTAFold 表示 / frame 扩散 + IPA / 取向残基云）；Fig 1 是图像类比的加噪-去噪示意 |
| W3 | W1 得到的 7 类 | 逐族写"适用边界 + 条件化机制 + 验证证据类型"，并把每族的验证短板单独标出 | 判据是**证据类型而非数字**：骨架族 "although the generated backbone must generally be followed by sequence design, structure-prediction-based filtering and experimental testing"；FrameDiff 族 "The primary constraint pertains to the reliance of performance comparisons on computational self-consistency, novelty and diversity metrics"；Genie 族 "Nevertheless, a direct comparison with RFdiffusion or FrameDiff remains sensitive to differences in training data, sequence-design procedures, sampling budgets and evaluator choice"；Chroma "the provision of robust user-defined guidance has the potential to modify the sampled distribution"；全原子族 "the success of the application process is contingent on factors such as compatible sequence assignment, efficient side-chain packing, effective protonation-state treatment, and experimental verification of the intended interaction" | §3 正文逐族评述（RFdiffusion 系 / FrameDiff 系 / Genie 系 / Chroma / 特化方法五块）+ Table A1 的 16 行模型清单（任务/输入/输出/训练集/数据量/代码/文献号） |
| W4 | 各模型论文里实际用过的评测工具 | 做成 13 行 × 4 栏的判据表（Metric or Framework / Validation Layer / What It Measures / **What It Does Not Establish**），即每个指标必须同时写出它"不能确立什么" | 关键判决句：MolProbity "These criteria are useful for identifying locally unrealistic conformations, but they do not establish global fold stability, correct oligomerisation, favourable solvation or biological function"、"MolProbity should therefore be interpreted as a stereochemical validation tool, not as a comprehensive measure of physical plausibility"；pLDDT 与 RMSD "RMSD and pLDDT should not be treated as interchangeable"；novelty "Lower nearest-neighbour similarity can indicate greater structural novelty, but the result depends on the database release, chain-length distribution, structural-search method and alignment procedure"；diversity 只给定义（unique clusters / total），**无下限值** | Table 3：13 行、每行一个 Validation Layer 标签（从 Local stereochemistry 一直到 Functional validation，共 13 种）；结论句 "These evaluation criteria constitute a hierarchy rather than a single, composite definition of protein quality" |
| W5 | 两个统一基准 + 一个方法作者自限的案例 | 逐个记覆盖层与缺失层；把 PDB-Struct 的"稳定性"口径写清楚（它其实是数据集级相关，不是单候选判定） | PDB-Struct 侧原句："In PDB-Struct, thermodynamic stability is instead evaluated using experimentally annotated mutagenesis datasets" 与 "For the stability metric, PDB-Struct reports the Spearman correlation between model pseudo-log-likelihood and experimentally measured stability"（正文随后以式 (11) 把这个稳定性分数写成 ρs 形式的 Spearman 相关，操作数就是"伪对数似然 vs 实验稳定性标注"两组量）；Scaffold-Lab 覆盖 "Designability, novelty, diversity, structural quality, motif recovery and computational efficiency under a common protocol"，但同一行明写不确立 "Wet-lab expression, stability, affinity, catalytic activity or biological function"；**两者原文均未给出可用阈值数字** | 一个示范案例：SALAD——"the authors explicitly note that predictor-based designability metrics alone are insufficient and that additional experimental validation remains necessary"，作者点评 "This provides an instructive example that computational ranking should not be interpreted as experimental evidence" |
| W6 | W4/W5 的失效边界 + 统计力学定义 | 三分布不等价论证（经验数据分布 / 学习模型分布 / 热力学平衡分布）→ 给出前置验证条件 → 给出两条补物理的路（生成后再过滤再加权、训练或采样期插可微能量项）→ 要求把候选绑定到明确条件 | 前置条件句见第 2 节第 4 条；条件绑定句："Where possible, candidate structures should be associated with defined temperature, solvent, protonation, ligand and oligomeric conditions, and assessed through observables that can be related to these conditions"；收口："thermodynamics-informed protein design should be formulated as condition-dependent inference rather than generic structural plausibility"；**原文未给阈值** | §5.2 全套建议 + 成本警告句（力场近似、溶剂不确定、自由能计算昂贵） |
| W7 | W3–W6 暴露的报告不一致 | 把"必须公开什么"写成清单，作为比较任何两个生成器的前置条件 | 非数值清单项两组：基准侧 "It is therefore recommended that benchmark protocols report structure-level redundancy filters, temporal splits, evaluator independence, sampling budgets and the number of candidates retained after filtering"；成本侧 "benchmark studies should report the computational cost, software versions, random seeds and candidate-selection procedures alongside structural and functional metrics" | §4 末段 + §5.1 第五类局限；同时给出实验通过率口径 "The proportion of candidates that have been tested through experimentation, and the success rate at each validation stage, are essential for the comparison of generative methods" |

## 4. 关键数字台账（综述没有实验台账，能记的只有它抄来的规模与它自己的结构计数）

| 数值 | 含义 | 出处（原句片段 / 位置） |
|---|---|---|
| 7 类 | Table 2 按"分子表示 × 设计目标"把方法归成的类别数（本卡清点表行） | Table 2 各行类别名：Backbone generation / Motif-guided generation / Programmable generation / All-atom generation / Interaction prediction / Sequence-structure co-design / Ensemble generation |
| 13 行 | Table 3 的"指标/框架 × 不能确立什么"判据表行数（本卡清点） | Table 3 行标签从 "Local stereochemistry" 到 "Functional validation"，共 13 种 Validation Layer |
| 16 行 | Table A1 列出的开源模型条目数（本卡清点；正文另提 Protpardelle 未进表） | "Models mentioned in this review have been implemented as open-source tools" + Table A1 逐行 |
| 13 条公式 / 16 项记号 | §2.1 给出的式 (1)-(13)（DDPM 与 score-based 两套）与 Table 1 记号表 | 正文公式编号 (1)…(13)；Table 1 列 x0…∇x log p(x) |
| 50 条 | 参考文献总数（末条为 Bogatskiy 等，E(3) 等变架构） | 参考文献表末条标题 "Symmetry group equivariant architectures for physics" |
| 121,800 | RFAA（RoseTTAFold All-Atom）训练集 PDB 规模 | Table A1 行 "RFAA sequence structures PDB 121,800" |
| 20,312 backbones | FrameDiff 训练集规模 | Table A1 行 "FrameDiff structures structures PDB 20,312 backbones" |
| 9K clusters | FrameDiPT 训练集规模（RCSB/PDB 聚类） | Table A1 行 "FrameDiPT structures structures; all-atom RCSB; PDB 9K clusters" |
| 4269 | SMCDiff 训练数据规模 | Table A1 行 "SMCDiff motif scaffolds PDB 4269" |
| 195,214 | Genie 训练集（SCOPe）规模 | Table A1 行 "Genie structures structures SCOPe 195,214" |
| 588,570 structures | Genie2 训练集（PDB + AFDB）规模 | Table A1 行 "Genie2 structures structures PDB; AFDB 588,570 structures" |
| 587,479 + 135,745 | Genie3 训练集：AFDB 结构数 + Pinder 复合物数 | Table A1 行 "Genie3 structures structures PDB; AFDB 587,479 AFDB structures + 135,745 Pinder complexes" |
| 619,045 + 1674 MD trajectories | Mac-Diff 训练数据：PDB 结构数 + MD 轨迹数（另含 GPCRmd、ATLAS） | Table A1 行 "Mac-Diff protein sequence protein conformational ensembles PDB; GPCRmd; ATLAS 619,045 PDB structures + 1674 MD trajectories" |
| 28,819 structures | Chroma 训练集规模（PDB/UniProt/PFAM） | Table A1 行 "Chroma sequence structures PDB, UniProt, PFAM 28,819 structures" |
| 41,000,000 structures | AlphaFold3 条目所写训练数据量（**二手转录，本卡未回溯 AF3 原文核实此量纲**） | Table A1 行 "AlphaFold3 sequence; SMILES structures PDB 2021 41,000,000 structures" |
| 6 行写 "-" | Table A1 里 RFDiffusion、RFDiffusion2、RFDiffusion3、Protein Generator、TDS、VFN-Diff 的数据量栏为空（TDS 连数据集名也写 "-"） | Table A1 对应行；"dataset size (when available)" 即作者自述口径 |
| approaching 1000 residues | SALAD 系稀疏去噪模型能生成的蛋白长度量级（作者用来举例"可扩展性"） | "In addition to demonstrating scalable backbone generation for proteins approaching 1000 residues and applications to motif scaffolding, structure editing and multistate design" |
| accessed on 27 July 2026 | Table A1 代码链接的核对日 | "code availability (accessed on 27 July 2026)" |
| 0 条数值阈值 | **全篇没有给出任何判据的数值阈值**（pLDDT/RMSD/TM-score/designability 都只给定义与"不能确立什么"） | 本卡清点底稿全文：除题录号、Table A1 的训练集规模与公式编号外没有别的数字；实测 "%" 出现 0 次，也没有任何 "<数字 / >数字" 型阈值表达式 |
| 0 条命中率 / 0 条成本 | 无任何实验命中率、成功率、GPU/CPU 秒或金额数字；成本只有定性句 | "sampling can be computationally expensive, and performance can be sensitive to noise schedules and guidance parameters"；"free-energy calculations are computationally demanding" |
| 题录 27(16):7151 · PMID 42653156 · PMC13513569 | 本篇自身标识（用于身份核验） | 底稿开头身份块 "10.3390/ijms27167151 ijms-27-07151 1 Review"、"42653156"、"PMC13513569" |

## 5. 结论——作者说了什么

1. **各方法族有明确分工，不存在"扩散 = 好"**："It has been demonstrated that RFdiffusion-derived methods are particularly well-suited to fixed-motif scaffolding, binder generation and, in their all-atom extensions, atom-level active-site and ligand-aware design"；"FrameDiff-based approaches provide a residue-frame formulation for unconditional backbone generation, structural inpainting and conditional sampling"；"By contrast, the Genie family emphasises diverse backbone exploration, multi-motif scaffolding and increasingly all-atom generation"；"Chroma is capable of supporting programmable combinations of geometric and semantic constraints"；"ProteinGenerator is able to couple sequence and structure generation"；"Mac-Diff targets learned conformational heterogeneity as opposed to reconstruction of a physically calibrated equilibrium ensemble"。
2. **跨族比较不能直接采信**："Across these categories, comparative outcomes are found to be strongly dependent on training datasets, sampling budgets, inverse-folding and structure-prediction pipelines, and evaluator choice"；对"用扩散"这件事本身，作者给的评价标准是："the practical value of a method depends less on the presence of diffusion alone than on the correspondence between its molecular representation, conditioning scheme, sampling cost, and intended experimental application"。
3. **第二个趋势是预测架构被复用进生成流程**："A second major trend is the reuse of structure-prediction architectures within generative workflows"（RFdiffusion 借 RoseTTAFold 表示、AlphaFold3 用扩散模块做条件坐标生成），但这"retaining distinct objectives and evaluation requirements"——目标与评测要求仍然不同。
4. **判据必须分层分开报，不得当作自由能/动力学/功能的证据**（全篇收口句）："Consequently, stereochemical quality, structural self-consistency, novelty, diversity and task-specific constraint satisfaction should be reported separately and should not be interpreted as the direct evidence of folding free energy, kinetic accessibility or biological function"。
5. **五条局限是作者的自陈清单**：训练集构成限制泛化（"the composition of training datasets imposes limitations on model generalisation"）、蛋白动力学与固有无序表征不完全、功能设计远比几何生成难（"Functional labels are generally scarcer, more heterogeneous and more condition-dependent than structural data"）、当前架构没有完整编码化学与环境上下文（"Structures produced in residue-frame or Cartesian coordinate space may contain local steric clashes, strained torsions, inadequate side-chain packing, incorrect protonation states, or interactions that are incompatible with the solvent"）、评测协议不够标准（"evaluation protocols remain insufficiently standardised"）；另加一条 developability 与一条复现性（见第 2 节 5、6 条）。
6. **对物理引导不持乐观默认值**："Physics-based guidance has been demonstrated to enhance local geometry, interaction plausibility and the ranking of candidate structures"，但其对折叠稳定性/亲和力/催化活性的影响"contingent upon the accuracy of the physical model and the adequacy of conformational sampling"，因此"Physics-informed generation should therefore be evaluated empirically rather than assumed to improve every design objective"。
7. **闭环态度**："Closed-loop design-build-test-learn workflows have the potential to accelerate protein engineering; however, their reliability will require the establishment of objectives grounded in experimentation, the incorporation of uncertainty awareness in candidate selection, and the ongoing involvement of human oversight"。
8. **展望**："It is anticipated that future studies will yield the greatest insights when task-matched generative models are combined with condition-aware molecular modelling, uncertainty estimation, and experimental measurements of expression, stability, structure and function"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的真正产出是"否证性清单"而不是"新判据"**。Table 3 用 What It Measures / What It Does Not Establish 两栏并排，等于给每个指标配了一句"它能排除什么、不能确立什么"。→ 对我们的漏斗：任何判据（Foldseek 命中、pLDDT、催化残基对齐、序列保守分）在写进标准之前，都应强制补一栏"不许用它证明什么"；只有肯定句的判据不算进过评审。
2. **"三个分布不等价"可以直接平移到我们的证据链**：数据经验分布 ≠ 模型学习分布 ≠ 热力学平衡分布。我们的类比是：底物筛选面板里的**富集/命中分布** ≠ 该酶在生理条件下的**通量分布**——把前者的排序当成后者的定量预测，正是作者点名的同一类越权。结论：任何"候选更可能干活"的表述只允许写成条件相关的推断，不许写成"其周转数为 X"；而"跑了 MD 就得到平衡系综"在本文口径下也不成立——"the resulting samples should be interpreted as learned conformational distributions rather than as equilibrium ensembles with physically calibrated populations or kinetic connectivity"。
3. **作者给的补救路径是"三选一独立验证"（分子模拟 / 实验观测量 / 独立自由能景观），但没有给任何一条的命中率**→ 这篇只能用来**限制**其它卡的结论强度，不能用来支撑"跑 MD 就能确认稳定性"的成本收益估算；那类估算仍需 B09 式"通过率 ÷ 单价"，而本文连单价都没有。
4. **它转述的 PDB-Struct 稳定性口径里藏着我们最容易犯的错**：底稿原句是 "For the stability metric, PDB-Struct reports the Spearman correlation between model pseudo-log-likelihood and experimentally measured stability"——即"稳定性"这一格给的是**数据集级相关系数**，不是"这一个候选稳不稳"的判定；本文自己的 Table 3 也写了 PDB-Struct 那一行不确立 "Direct stability or foldability of an individual newly generated protein"。→ 我们的判定器若只报面板级相关（AUC/Spearman），同样不能写成逐条候选的把握度——除非像第 17 轮那样把逐条后验单独做出来。（注意：这两句是转述他人基准，本文没给相关系数的具体数值。）
5. **综述承认"these statistics are currently reported inconsistently across studies"却没有失败台账**——这与 DP2R 缺"能同时给阳性和阴性打分的考卷"（B09 第 A 段）是同一个缺口的两个视角：他们的社区层面缺失败数据，我们在项目层面也缺带产物标签的阴性集。本篇可作为"标准 G0（真值面板）为什么必要"的**旁证**，不是证据。
6. **它的引文编号错位提醒了一件事**：综述级文献里的"某模型用了多少数据/被谁验证过"属于二手转录（本卡第 4 节所有 Table A1 数字都是这个性质）。凡要从这些数字推论（例如选型、估成本），必须回到原论文；本卡因此**不**据此做任何选型建议。

## 7. 局限与失败（作者的 + 我们读出的 + 与登记底稿的差异）

**作者自承的（第 5 节第 5 条那份"五条局限 + developability + 复现性"清单，另补以下四句原文收口）**

- 比较优势本身没定论："Furthermore, their comparative advantages over autoregressive models, masked language models, flow-matching approaches, and energy-based optimisation remain incompletely established"。
- 现有基准还不够："Although PDB-Struct and Scaffold-Lab represent important steps towards unified assessment, community benchmarks that link computational outputs to experimentally measured properties are still necessary"。
- 系综型模型目前给不出平衡分布："Current ensemble-oriented diffusion models primarily address conformational diversity and do not yet consistently recover equilibrium populations or kinetic networks"。
- 同时优化序列/结构/动力学/功能仍属预期目标："Sequence, structure, dynamics and function may be approached within increasingly unified frameworks; nevertheless, their simultaneous optimisation remains a prospective objective"。

**我们读出的（推断）**

1. **零一手数据**：无自做生成、无湿实验、无成本测量，所以它在证据等级上只能给"限定句"，不能给"支持句"；把它当作"某判据有效"的引用来源是误用。
2. **零数值阈值**：全篇没有一条可执行的判定数值（多少 pLDDT、多大 RMSD、几类 cluster 算够），所有"应当分开报告""应当独立验证"都是规范性表述。凡需要阈值的项目决策，必须另找方法论文（本文不能替代）。
3. **二手数字未回溯**：Table A1 的训练集规模（尤其 "41,000,000 structures" 这一条挂在 AlphaFold3 名下）本卡无法在本地核验，且量纲可疑（结构与序列条目易混）；"dataset size (when available)" 与 6 行 "-" 说明作者也是能查到才写。
4. **引文编号错位**（本卡实际抓到的两处）：正文给 Mac-Diff 标 [39]、给 DiffDock 标 [38]，而底稿参考文献表里 [38] 是 Mac-Diff、[39] 是 Protpardelle、DiffDock 是 [17]，附录 Table A1 又用 [38] 指 Mac-Diff。→ 使用本卡时**不要**引用它的编号。
5. **口径混用**：作者声明只综述"直接服务结构生成"的方法，却把主职是预测的 AlphaFold3 与做小分子姿态的 DiffDock 写进 §3 与 Table A1；这不影响判据结论，但影响"这篇覆盖了多少个扩散设计模型"这种计数的可比性。
6. **它推荐的物理层没有定价**：文中要求用 MD/自由能做独立验证，同时承认自由能计算昂贵、力场近似——但没有给出一次成本或一个命中率，因此对"该不该把 MD 放进漏斗"这个决策，本文只提出义务、不提供可行性证据。

**与登记底稿 `sources/cost-benchmarks.md` §3.7 的逐条对照（不一致处以本地全文为准）**

| 项 | 登记底稿写法 | 本地全文实情 | 处置 |
|---|---|---|---|
| pLDDT 判决句 | 句中夹 markdown 星号包住了 "does not provide direct evidence" 这一小段 | 该句无星号，整句与本地全文逐字一致 | 本卡引无星号版本（见第 2 节第 1 条）；星号会让引句与全文比对产生偏差，故不带 |
| 系综验证句 | 直接从 "ensemble-oriented" 起引 | 该句在全文里以 Thus 起手（"Thus, ensemble-oriented diffusion models must be validated"） | 本卡仍从 ensemble-oriented 起引——它是全文的连续子串，逐字命中，语义不变 |
|  developability 列表 | "poor recombinant expression, limited solubility, aggregation, chemical instability, proteolytic sensitivity, immunogenicity or unsuitable oligomerisation" | 逐字一致，且前接 "A generated sequence or structure may appear computationally designable, yet exhibit" | 本卡按完整句引，补出"看起来可设计却表达差"这个前提 |
| 报告要求 | "呼吁基准报告 computational cost, software versions, random seeds and candidate-selection procedures" | 完整句还带 "alongside structural and functional metrics"，且该句位于 developability/复现性段落末（§5.1），不在 §4 评测节 | 本卡记为 §5.1 出处；语义无冲突 |
| CSV 第 120 行原句列 | 与上述三句一致 | 逐字命中本地全文 | 无需修正 |
| 底稿未收的两句（本篇更硬的限制） | 未记录 | "A collection of structurally diverse samples should not be automatically interpreted as an equilibrium ensemble, since the generated conformations may lack physically meaningful populations, kinetic connectivity, or transition pathways" 与 "Thermodynamic favourability, therefore, does not in itself establish that a molecular state is kinetically accessible or that a designed protein will fold, bind or function on biologically relevant timescales" | 本行直接补录两句原文；其中第一句另见第 2 节第 4 条，第二句（热力学有利 ≠ 动力学可达）此前未在任何底稿登记过 |
| 数值层面 | 底稿没从本篇引任何数字 | 本篇确实也没有可引的阈值/命中率 | 无冲突，但要防下游把 §3.7 相邻行的其它文献数字错挂到本篇 |

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **把"pLDDT 高 ≠ 可表达/可折叠/有功能"当作我们漏斗的否证边界写进标准**：DP2R 里 Foldseek 命中、结构预测 pLDDT、催化残基几何对齐这类指标，一律只能作为**召回与排除**用途，不许写成"该候选具备尿嘧啶/ATP 激活能力的证据"。落地做法＝照 Table 3 的做法给每条判据并排写满 "What It Measures" 与 "What It Does Not Establish" 两栏（该表实为 4 栏 × 13 行），缺后一栏的判据不许进漏斗。
2. **"分层报告清单"直接抄成我们的 run.md / manifest 字段**：本文要求 benchmark 公开 structure-level redundancy filters、temporal splits、evaluator independence、sampling budgets、过滤后候选数、失败实验，以及 computational cost、software versions、random seeds、candidate-selection procedures。我们的真值面板与判定器目前缺三项：**评测器独立性声明、随机种子、失败候选逐条留档**——这三项加进 `--check` 类门禁成本极低，正是它点名的失效来源（幸存者偏差）。
3. **"学习分布 ≠ 平衡系综"→ 我们结论的表述规范**：任何来自 MD 采样/构象聚类的结果，在写成热力学或动力学结论之前，必须像本文那样绑定条件（温度、溶剂、质子化态、配体、寡聚状态），或明确标为"仅构象多样性"。这条能防住我们在第 10 轮之后最容易犯的错：把轨迹多样性当"该位点更稳定"。
4. **实验三层顺序（表达/溶解性/单分散 → 结构验证 → 功能验证）可作为我们湿实验排期的外部对齐**，特别是"先可行性、后结构、最后功能"这一层级；我们的 LC-MS/MS 产物身份属于第三层（功能/化学事件），不能替代前两层，因此**可表达性失败会让功能检测无从解释**——这是本文分层逻辑对我们唯一的实操提醒。
5. **"物理引导需被实证评估，而不是默认改善一切目标"** 这条态度应当成为我们引入 MD/自由能层时的默认预设立场：先在小面板上证明它比不用它更准，再扩用量。

**不可迁移（为什么不能照搬）**

1. **本文没有任何 UAA/酶活判据**。它谈"催化"只到 "catalytic activity" 需要 task-specific assay 这一层："Function-guided generation necessitates task-specific experimental measurements, precluding validation solely through predicted structural compatibility"，没有给出任何催化活性阈值、也没有把催化几何作为验证对象——不能当作"结构自洽即可推酶活"的背书，恰恰相反它是这句话的反证来源。
2. **不能引用它做任何命中率/成功概率校准**：全篇零命中率、零样本量、零成本数字（见第 4 节的两行 0 条）。同样，**不许**把 binder 类论文的 pAE/ipTM 阈值或适配体 FEP 命中率借到这张卡的名下——这张卡连阈值都没有。
3. **不能把"MD/自由能可作独立验证层"当成 MD 对 UAA 酶活有效性的证据**：本文给的是**义务**（不作独立验证就不许写热力学结论），不是**效果**（验证了就更准）；它自己并列了"力场近似、溶剂不确定、自由能计算昂贵"三条折扣。
4. **Table A1 的模型清单/数据量不能当选型依据**：那是二手转录（代码链接只在 2026-07-27 核过，且引文编号有错），选型必须回原论文与仓库实测。
5. **本文的"分层判据表"不等于"面板上的判别力排序"**：它没有在任何真值集上量化过哪条判据更准（这一点 B09 做了）。所以它能约束我们"别越权解释"，不能替我们做判据取舍的量化排序。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K38_PMC13513569_text.txt

- **本卡全部英文引句只照着上面这一份底稿逐字写、逐字核**（同一篇另有 `fulltext/K38_PMC13513569_fullTextXML.xml` 原始抓取件，登记在同编号名下但门禁只读非 .xml 件；两份内容同源，故不再声明第二份引句底稿）。底稿身份块已核对：标题 "Diffusion-Based Protein Structure Design: Geometric Modelling, Validation Strategies, and Thermodynamic Challenges"、DOI "10.3390/ijms27167151"、"PMC13513569"、类型 "1 Review"、署名 11 人（Li Wenran … Cadet Frederic），确认是 K38 本身。
- 对照底稿：`sources/cost-benchmarks.md` §3.7（第 135–138 行，四句已核关键论断）、§六表格行 202（热稳定性不足）与行 205（修饰/二硫键类 developability 失败）；差异逐条记在本卡第 7 节对照表，**凡与本地全文不一致处以本地全文为准**。
- CSV 行映射：`data/protein_design_literature.csv` 第 120 行；本卡 §3/§7 ↔ `计算筛选判据`、`阈值数字`（本篇为"零阈值"）；§4 ↔ `候选数递减`、`成本统计引用`（本篇只有训练集规模）；§8 ↔ `在方法演进链的位置`。
- 本卡数字与计数的可核性：第 4 节 Table A1 各行片段（含 121,800 / 20,312 / 9K / 4269 / 195,214 / 588,570 / 587,479 + 135,745 / 619,045 + 1674 / 28,819 / 41,000,000）在底稿中逐字命中；"7 类 / 13 行 / 16 行 / 6 行写 -" 属**本卡清点表格行数**，不是原文句子，已在含义列注明。
- 已避开的形式：底稿把行内公式与部分符号拆成带空格形态（如 "S E ( 3 )"、"x 0"、"C α"、"α ¯ t"），本卡对这些只作中文转述、不加英文引号；含 U+2026 省略号的跨句拼接一律拆成两条或改取连续子串；引号内不含 markdown 星号（本卡自查确认 0 处）。
- **本卡自检**：`scripts/verify_literature_cards.py`（参数 `--only K38 --no-report`，2026-10-16 本地运行）把卡内所有不含中日韩字符、被直双引号包住、≥20 字符且 ≥12 个字母的片段，在登记的底稿里做逐字查找，任何一条不命中即 FAIL。**最终实测输出：`PASS K38 quotes=122/122`，判定结果 1/1 张卡 PASS、0 行不合格，退出码 0**（122 条含跨节重复出现的同一片段；去重后为 111 条独立片段，全部逐字命中底稿）。未跑 `--sync-map`、未跑不带 `--no-report` 的全量门禁，故未改写 `selfcheck.txt` 与 `rollout_status.tsv`。
- 自查过程中被抓出或改正的四处（说明这道门是真在做事）：① Table A1 的 FrameDiPT 行拼接时漏了 Output 列的 "structures; all-atom"，由写卡中途一次"复刻门禁取句 + 逐字查串"的自查抓到并改正（正式门禁首跑前已修，故门禁输出里没有这条）；② §3 W4 曾写 Table 3 "按 Validation Layer 分 8 层"，属未经点数的估计，已按底稿实测改为 13 行 / 13 个互不重复的层标签；③ §3 W2 曾以为 E(3) 那句被抽成了带空格的写法而不敢加引号，实测底稿里该句是紧凑形式，已改为逐字引用；④ §3 W5 与 §6 第 4 条关于 PDB-Struct 稳定性口径的说法已补上底稿原句 "For the stability metric, PDB-Struct reports the Spearman correlation between model pseudo-log-likelihood and experimentally measured stability"，不再只靠中文转述；抓取通路一项按 `inventory.json` 登记值写为 `fetch_channel=epmc_search_then_fulltext`，未凭猜测填写。
- 清点类断言的核验方式：Table 3 的 13 个 Validation Layer 标签、Table 2 的 7 个类别名、Table A1 的 16 行模型名，均在本卡声明的那一份底稿里逐个字符串命中（0 缺失）；"数据量栏写 - 的 6 行"是按 Table A1 的行结构（Paper/Input/Output/Dataset/Data Size/Code/Ref）解析出 16 行后点出来的，落在 RFDiffusion、RFDiffusion2、RFDiffusion3、Protein Generator、TDS、VFN-Diff——不是凭印象计数；身份块核验用到的题录串 "10.3390/ijms27167151"、"PMC13513569"、"1 Review" 也逐字在底稿开头命中。

<!--CSV回填
work_type=论文（综述 Review；无自建实验台账，作者自述仅综述已发表工作）
target=无特定靶点（综述对象：de novo 骨架、motif 支架、binder 与固有无序蛋白结合体、小分子/辅因子邻近蛋白（digoxigenin、heme、bilin）、活性位点支架、对称组装体、构象系综）
backbone_generation=本文不生成；按分子表示与生成目标归类：RoseTTAFold 系（RFdiffusion / RFAA / RFdiffusionAA / RFdiffusion2 / RFdiffusion3）、残基局部 frame 扩散（FrameDiff / FrameDiPT / TDS / VFN-Diff / SMCDiff）、取向残基云（Genie / Genie2 / Genie3）、可编程约束（Chroma）、序列空间扩散（ProteinGenerator）、系综生成（Mac-Diff）、全原子联合建模（Protpardelle）、AF3（扩散模块用于复合物预测）
computational_filters=MolProbity 立体化学（clash/Ramachandran/rotamer/键几何）；TM-score；RMSD；pLDDT；sequence recovery；自洽性 designability（逆折叠出序列再用独立预测器复算）；novelty（对 PDB 最近邻最高 TM-score）；diversity（unique clusters / total）；基准 PDB-Struct 与 Scaffold-Lab；本文未提出任何新过滤器也未给任何判定阈值
thresholds=原文未给数值阈值；只给报告规范清单（structure-level redundancy filters、temporal splits、evaluator independence、sampling budgets、过滤后候选数、失败实验、computational cost、software versions、random seeds、candidate-selection procedures）
md_used=是（综述层面：把分子力学/MD/自由能计算列为独立验证与再加权层，并规定系综型模型须先经"分子模拟、实验观测量或独立自由能景观"验证才可作热力学或动力学解释；Mac-Diff 以 MD 轨迹为训练数据；本文未自做 MD）
qm_used=否（全文未把 QM/QM-MM 列为设计或验证层；仅附录 B.2 引 E(3) 等变网络在 quantum chemical properties 建模上与 SE(3) 相当，属几何方法学引证）
experimental_methods=综述列举（非本文所做）：recombinant expression、solubility、monodispersity；circular dichroism、NMR、crystallography、cryo-EM；binding affinity、specificity、catalytic activity、cellular response；PDB-Struct 使用实验突变稳定性标注数据集
pipeline_counts=本文无自建流水线；登记二手规模（Table A1）：RFAA 121,800；FrameDiff 20,312 backbones；FrameDiPT 9K clusters；SMCDiff 4269；Genie 195,214（SCOPe）；Genie2 588,570 structures；Genie3 587,479 AFDB + 135,745 Pinder complexes；Mac-Diff 619,045 PDB + 1674 MD trajectories；Chroma 28,819 structures；AlphaFold3 41,000,000 structures；SALAD 生成蛋白长度 approaching 1000 residues；表格规模 Table 2=7 类、Table 3=13 行判据、Table A1=16 行模型
hit_rate=未记录（综述无实验，全文未给出任何实验命中率或成功率数字）
best_metric=未记录（综述无该字段；全篇最接近的定量结论只是转述 PDB-Struct 用 Spearman 相关衡量模型伪对数似然与实验测得的稳定性，未给具体相关系数）
cost_or_stat_note=只有定性成本：sampling can be computationally expensive；free-energy calculations are computationally demanding；代码/权重/许可/硬件/采样参数与未公开过滤流程可阻碍独立复现；全文无 GPU/CPU 秒、无金额、无吞吐数字
role_in_timeline=给"生成器 + 预测器自洽性"这条漏斗提供判据上限声明：把 pLDDT/RMSD/TM-score/designability/novelty/diversity 与热力学稳定性、动力学可达性、生物功能明确切开，并要求基准公开成本/版本/随机种子/筛选流程；在 DP2R 中作"否证边界卡"与报告规范来源，不作数据点
source_pointer=data/literature_cards/fulltext/K38_PMC13513569_text.txt（同编号另登记 fullTextXML.xml）；sources/cost-benchmarks.md §3.7（135-138 行）与 §六（202、205 行）；data/protein_design_literature.csv 第 120 行
CSV回填-->
