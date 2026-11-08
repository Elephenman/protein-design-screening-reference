# [K42] Scaffold-Lab：把 7 种骨架生成器塞进同一条复折叠流水线横评——统一判据怎么定、哪些"更好"其实分母不可比

Zheng Zhuoqi, Zhang Bo, Zhong Bozitao, Yu Jinyu, Liu Kexin, Li Zhengxin, Zhu Junjie, Wei Ting*, Chen Hai-Feng*（上海交通大学 生命科学学院 微生物代谢国家重点实验室）
PLoS Computational Biology 2026, 22(5): e1014290 · DOI 10.1371/journal.pcbi.1014290 · PMID 42172287 · PMCID PMC13225634 · 编辑 Gaetano Montelione（RPI）
开放获取（CC BY 4.0）· https://doi.org/10.1371/journal.pcbi.1014290 · 代码 https://github.com/Immortals-33/Scaffold-Lab · 骨架数据 https://zenodo.org/records/20080699

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K42**（组：通用方法学；`文献类型=benchmark`；CSV 原行除 DOI 与题录外全部为"未记录"，本卡是首次全文级填充） |
| batches.tsv | 第 78 行，`state=FULLTEXT`，`fulltexts=data/literature_cards/fulltext/K42_PMC13225634_text.txt`，`records=sources/cost-benchmarks.md` |
| 本地全文① | `fulltext/K42_PMC13225634_fullTextXML.xml`（267,564 B，2026-10-20 抓取） |
| 本地全文② | `fulltext/K42_PMC13225634_text.txt`（104,669 B，去标签纯文本）——**本卡全部引句的唯一底稿** |
| 对照底稿 | `sources/cost-benchmarks.md:149`（原为一句题录级摘要，本卡在其基础上补齐判据、阈值、分母口径与排名机制） |
| 证据级别 | **全文级**（本卡所有英文引句均可在 `K42_PMC13225634_text.txt` 里逐字命中；见第 9 节） |
| 额外可引内容 | 这份抽取文本把 **PLOS 审稿意见全文**（Reviewer #1/#2/#3 + Decision Letter）一并收录在正文之后，故本卡第 7 节里"审稿人质疑"的引句同样是逐字命中的原文 |
| 未取到的部分 | **S1 File（DOCX）本地没有**：S1–S16 图、S1 Table（24 个 case 的 motif 定义与总长）、S2 Table（novelty 惩罚显著性明细）、S3 Table（RA95.5-8F 五种方法成功率）。因此凡涉及这三张表的数字，本卡只引正文里出现的转述句，不编造表内数值；作者对审稿人的回复也在附件 `Response to Reviewers.docx` 里，本地未获取。正文 Table 3 的 Efficiency 列**单位在正文未标注**（正文只说平均时间、量级为分钟级） |

## 1. 这篇到底解决什么（一句话）

它解决的不是"哪个生成器更强"，而是**"各家报的数字根本没法比"这件事本身**：论文指出 "differences in the definition and thresholds of evaluation limit effective comparisons"，并说 "there is no standardized evaluation suite for assessing methods from scratch"，于是搭了一个叫 Scaffold-Lab 的**统一评测框架**——两类任务（无条件生成：给定长度 50–1000 残基；条件生成：motif-scaffolding）、四类定量指标（designability / novelty / diversity / efficiency，用于排名）加一组结构性质描述（二级结构、Rg、MolProbity），并且**把所有方法的评估都塞进同一条复折叠流水线**（骨架 → ProteinMPNN 出 10 条序列 → ESMFold 单序列复预测 → 算 sc-TM/sc-RMSD），最后用 TOPSIS + CRITIC 把多维指标压成一个可排名的 Ci 值，对 7 种代表方法（Genie、FrameDiff、RFdiffusion、TDS、GPDL、FrameFlow、Chroma）出排名。作者自己给这项工作的定位是 "experimental validation lags far behind computational generation in throughput"，所以要用 "in silico evaluation pipeline" 替湿实验做初步取舍。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **难点：同一件事各家定义不同，比了等于没比。** 现象/证据：Introduction 直说 "there has been a lack in standardized evaluation framework to accurately assess diverse methods, nor is there a comprehensive analysis of their practical applications"，并且 "differences in the definition and thresholds of evaluation limit effective comparisons"。
   **他们做了什么**：把判据全部重写成自己的口径并固定一条流水线（统一序列设计器 ProteinMPNN、统一预测器 ESMFold、统一 N=3 的 Top-N 策略、统一 Foldseek 的 TM 0.5 聚类阈值），再按长度分组排名。
   **应对后仍留下的代价**：两类任务用了**不同的成功阈值**——无条件生成用 "We use the success definition of sc-TM > 0.5 for unconditional generation (protein length ranges from 50 to 1000)"，motif-scaffolding 换成 "For evaluation on motif-scaffolding, we use sc-RMSD < 2.0 Å since designed proteins here are typically under 150 residues, providing a more rigorous test of method performance"。于是**跨任务的成功率数字不可比**（一个偏松、一个偏严），论文里两处成功率被并列叙述却不同尺。
2. **难点：只看最优序列会把骨架质量误判。** 现象：常规做法是取 best sequence 的自洽性，"While current methods typically consider the best sequence for evaluating designability, we propose that the number of sequences that fold into a generated structures also reflects the robustness and fitness of backbones"（能容纳多条序列的骨架更耐突变、更热力学稳定，而这两点正是湿实验挑选时真正在意的）。
   **应对**：自定义 Top N strategy，对前 3 条序列的 sc-TM（或 sc-RMSD）取均值再判阈值，并同时报 best 口径作对照（"Here we chose N = 3 for evaluation"）。
   **代价**：口径一改，与历史文献的同类数字立刻不可互换；而 N=3 本身是新引入的自由度，他们未对 N 做敏感性。
3. **难点：方法能跑的长度不齐，覆盖矩阵是残缺的。** 证据即 Table 2 原样："Short 50, 100 Genie, FrameFlow, FrameDiff, Chroma, RFdiffusion Medium 200, 300, 400, 500 FrameDiff, Chroma, RFdiffusion Long 600, 800, 1000 Chroma, RFdiffusion"——**长蛋白组只有 2 个方法可比**，中组 3 个；摘要说 "We thoroughly evaluated seven representative methods, providing a detailed analysis of their performance and utilities"，而作者概述自己写的是 "We evaluated five and four methods in terms of unconditional generation and motif-scaffolding both qualitatively and quantitatively"（五个跑无条件、四个跑条件）。
   **应对**：不跨组比原始值，改为**在每个长度组内单独算 TOPSIS 的 Ci**，再对该组内各长度取均值排名。
   **代价**：分组内比规避了"没测的项"，但组与组之间的 Ci **不可比**（权重由组内数据反推，参与池不同）；结论里"长蛋白 RFdiffusion 最好"实质是 2 选 1。
4. **难点：新颖度和"能不能折"混在一起，novelty 高分可能是废骨架。** 现象：他们观察到 "some generated backbones, although novel, were undesignable"。
   **应对**：给 novelty 加设计性惩罚项（平均 sc-TM < 0.5 时按与 0.5 的差额扣分），并明写 "A higher w imposes a more stringent penalty on backbones with less designability"，全文固定 "We set n = 3 and w = 1 throughout our experiments"；再用是否加惩罚做配对比较，得到 "The results indicate significant differences in some groups with p-values < 0.001"。
   **代价**：惩罚强度 w 与 n 是**拍定的常数，未做敏感性**；审稿人直接质疑显著性与图面不符——"It appears contradictory that the distributions for Medium RFDiffusion with and without penalty look nearly the same, but have p < 0.001, while for Medium FrameDiff the distributions look different but are not statistically different"（这是本地全文里收录的审稿意见原文）。作者本人的收口是承认 novelty 判别力弱："our analysis suggests that designability should be partially considered when calculating novelty"。
5. **难点：评估器本身有偏，横评比的是"模型合不合得来"。** 现象：整条流水线的分数来自 ProteinMPNN + ESMFold，而非实验。
   **应对**：三处补丁——(a) 换序列设计器做对照，因为 "ProteinMPNN outperformed ESM-IF1 in terms of refolding ability, thereby maximizing the potential of different protein backbone generation methods"（挑更强的设计器，尽量不把骨架的失败算到设计器头上）；(b) 换折叠预测器做一致性对照，S2 Fig 用 "a total number of 900 sequences predicted by ESMFold, AlphaFold2 (without MSA) and OmegaFold"，称三者相关性强；(c) 顺带算了 ESMFold pLDDT/pAE 与 sc-TM 的相关（S15 Fig）。选 ESMFold 的理由是 "We chose ESMFold as the standard refolding predictor due to its speed and competitive performance on long proteins"。
   **代价**：这些只是**相关性检查，不是效度检查**——没有任何湿实验结局用来验证"sc-TM 高"是否等价于"能表达能折叠"；生成器与 ProteinMPNN/ESMFold 共享 PDB 训练分布这层循环性，本文未处理（见第 7 节）。
6. **难点：条件生成任务各家协议不同，连"总分母"都不一样。** 证据（S1 Table 说明原文）：基准集沿用 RFdiffusion 的 24 case，"We basically followed the benchmark set collected by RFdiffusion except 6VW1 since it is a complex generation task which TDS was not capable to perform"；对各家设置 "For the other three method, we followed their original experimental settings except fixing the types of amino acids of all motif positions without redesign"，其后果是 "The different experimental settings resulted in different sets of total lengths"，因为 "TDS and GPDL generated proteins with mostly fixed lengths" 而 RFdiffusion/Chroma 可在长度区间内随机采样。
   **应对**：把差异如实登记（哪些是 motif 输入、哪些是随机采样的 scaffold 长度），并强调 "Note that the differences between lengths of fixed or random lie on the scaffold parts, where all method were input with the same motifs from real protein structures"。
   **代价**：**同一 case 上各家交付的总长不同**，等于各法在自己选的难度上得分；而且为迁就最弱的方法把 6VW1 从基准里删掉，这是"基准被被评对象的可用性反向裁剪"。
7. **难点：全部方法都偏向规整二级结构，对功能相关的 loop/无序区几乎不产。** 现象：SSE 偏好稳定到最长——"this preference for structured proteins remain consistent even as protein length increases up to 1000 residues"，作者归因 "This is probably due to the imbalanced training set where loop-abundant structures only account for a small subset of training data"；Rg 侧 "Chroma was the only exception as it generates more stretched backbones, particularly for longer proteins"。
   **应对**：只做了描述与归因，并指出这类区域 "These regions are typically studied through molecular dynamics (MD) simulation" 或构象采样，而它们 "which are often excluded from most training sets of protein backbone generation methods"。
   **代价**：**本文未解决**——他们没有引入 MD/系综来评这些区域，也没把 loop 产出率纳入排名指标；对需要环区参与催化或识别的应用，这套评测没有判别力（对我们的酶位点需求正对着）。审稿人还指出他们把"有序非规则结构"与"内在无序区"混为一谈（第 7 节）。
8. **难点：酶活性位点这种最小输入的条件任务，常规方法全军覆没，没法比较。** 现象："We found the base versions for all four methods failed to produce a single solution for the active site of retro-aldolase, highlighting the difficulty of scaffolding the motifs containing multiple discontinuous residues"。
   **应对**：额外引入用活性位点微调并对底物施加外电势的版本（他们称作 "RFdiffusion-enzyme"），得到 "we found RFdiffusion-enzyme succeeded 20 out of 100, which is a considerable success rate for such a challenging task"，据此结论 "This highlights the importance for the minimalist site fine-tuning and the external information from the substrate"。
   **代价**：这组"0/100 vs 20/100"**信息预算不等价**（微调权重 + 底物模板势都是额外输入），20/100 不能读成"该方法自身能力"；且单 case、无重复、无置信区间，明细在本地缺失的 S3 Table 里。

## 3. 方法与工作流程（统一判据 + 基准怎么建；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么是它）

- **被评对象（7 种骨架生成器，Table 1）**：Genie（IPA + SE(3) 扩散，Cα-only）、FrameDiff（SE(3) 流形扩散）、RFdiffusion（扩散 + 预训练 RoseTTAFold）、TDS（粒子滤波做条件采样）、GPDL（ESMFold + 约束式 hallucination/inpainting）、FrameFlow（用 flow-matching 替换扩散的去噪打分匹配）、Chroma（扩散 + GNN，同时出结构与序列）。任务归属：无条件 5 家、条件 4 家，RFdiffusion 与 FrameFlow、Chroma 两类都做。
- **统一评估器（本文的真正主角）**：一条**复折叠（refolding）流水线**——固定用 ProteinMPNN 出序列、固定用 ESMFold 做单序列结构预测，再算自洽性指标。Fig 1 图注写得很清楚："Each of the generated backbone was evaluated with a refolding pipeline. We generated 100 backbones with 10 sequences for each backbone to be evaluated"。
- **四类定量指标（用来排名）**：designability、novelty、diversity、efficiency；正文原话 "The first four categories are quantitative that were used for ranking different methods"，并承认这些是 "While most of the these are in silico metrics, they serve as valuable proxies for high-throughput in vitro experiments"。
- **一组描述性结构指标（不排名）**：DSSP 二级结构组成、半径 of gyration（Rg）对照经验回归、MolProbity 的 clash score 与 bad bonds/bad angles。
- **排名算法**：TOPSIS 做多准则决策 + CRITIC 客观定权——"For the ranking of different methods, we used the widely recognized Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)"，权重 "objective, like the CRiteria Importance Through Intercriteria Correlation (CRITIC)"；Ci 越大越好："C i denotes the calculated relative nearness value of TOPSIS results, where higher indicates better performances"。
- **动态阈值（消除主观阈值）**：把 sc-TM（或 sc-RMSD）的判定阈值当自变量扫，取 AUC —— "A method with a higher AUC value indicates better performance, regardless of the subjective definition of designability"，扫描步长 "We take the step of sc-TM as 0.01 during the calculation"。
- **没有用的方法**：湿实验表达/结合/活性测定（全文零实验）、MD 生产运行（只在讨论里提到 loop 区通常用 MD 研究）、QM/自由能。这是一篇**纯计算基准**。

### A. 无条件生成主流程

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | 7 种公开方法（Table 1） | 按官方实现/可用性分派任务与长度档 | 判据＝该方法是否支持该任务/长度（原文未给数值阈值） | 无条件 5 法（Genie/FrameDiff/FrameFlow/Chroma/RFdiffusion）、条件 4 法（RFdiffusion/TDS/GPDL/Chroma）+ FrameFlow；长档仅 Chroma 与 RFdiffusion |
| W2 | 长度档 50/100（短）、200/300/400/500（中）、600/800/1000（长） | 每法在每个长度生成固定数量骨架 | 原文未给采样参数阈值（温度/步数按其原设置） | "we generated 100 backbones at each unique evaluated length for each method"（9 个唯一长度） |
| W3 | 每条骨架 | ProteinMPNN 设计序列（全程不换设计器） | 无阈值；S1 Fig 里用 sc-TM 高低证明选 ProteinMPNN 而非 ESM-IF1 | "We generated 100 backbones with 10 sequences for each backbone to be evaluated" ⇒ 每长度 1,000 条序列；对照实验规模 "9 (number of unique lengths) × 20 = 180 unique backbones and 180 × 10 = 1800 designed sequences" |
| W4 | 序列 | ESMFold 单序列复预测（无 MSA） | 无阈值 | 每条骨架 10 个复折叠结构；预测器一致性对照 "a total number of 900 sequences predicted by ESMFold, AlphaFold2 (without MSA) and OmegaFold" |
| W5a | 骨架 vs 复折叠结构 | 算 sc-TM（TM-score），判 designable | "where a protein backbone is considered as designable if the refolded structures and the original backbones shares a TM-score" > 0.5 | 成功率口径：**"Success rate is defined by the number of backbones passing the sc-TM threshold divided by the total number of backbones within each group"**（分母＝该法该组生成的骨架数 100） |
| W5b | 同上 | 口径改为 Top-N：取前 3 条序列的 sc-TM 均值再判 0.5 | sc-TM>0.5；"Here we chose N = 3 for evaluation"；同时保留 best 口径作对照 | Fig 2A/2B 实数：短中档 "For proteins with 300 or less residues, all the tested methods performed strongly, with success rates around or exceeding 80%"，长档 "falling below 30% for proteins with 800 or more residues"；拐点 "A notable turning point was observed at protein lengths of around 300 residues" |
| W5c | 各阈值下的成功率曲线 | 动态阈值 AUC（步长 0.01，SciPy 积分） | AUC 越大越好，与主观阈值无关 | RFdiffusion 在高要求端仍站得住："as it maintains success rates of around 70% and 50% for short and medium-length proteins, respectively" |
| W6 | 骨架 | Foldseek 对整库 PDB 搜索，取最高 TM = pdb-TM；再按设计性加惩罚得 novelty score | 惩罚：均值 sc-TM<0.5 时补 (0.5 − w·均值)；"We set n = 3 and w = 1 throughout our experiments" | 结果 "the pdb-TM values predominantly range between 0.6 and 0.7, with no significant trends observed across the different methods or length categories" |
| W7 | 同一长度组的全部骨架 | Foldseek-Cluster 聚类，算 unique clusters / total | 聚类阈值：TM-score 0.5；"Diversity is defined as the number of unique clusters divided by the total number of proteins within each group using Foldseek-Cluster"；S16 Fig 另做 0.4/0.6 敏感性 | 随长度上升： "diversity tended to increase with protein length, potentially due to the distinctive levels of redundancy in the training set at different lengths" |
| W8 | 同一批生成任务 | 记平均每条骨架耗时（100 条） | "All tests were conducted under identical hardware resources"；判据＝时间越短越好（效率列方向 ↓） | Table 3 效率跨 3 个数量级：FrameFlow 0.11（长 50）→ Genie 8.08（长 100）→ RFdiffusion 54.43（长 1000）；正文 "the processing speeds of the current methods are still in the range of several minutes"（**单位正文未标注**） |
| W9 | 原始骨架（不复折叠） | DSSP 二级结构、Rg 对照经验回归、MolProbity（clash / bad bonds / bad angles） | 期望值来自晶体结构基准：bad bonds 0%、bad angles 0.1% | 实测 "far beyond the expected threshold of 0% for bad bonds and 0.1% for bad angles, respectively"，其余方法分布在 0%–20%；clash 侧 "with the exception of RFdiffusion obtaining a significantly lower clash score than different methods" |
| W10 | W5–W8 的四类指标均值 | 按长度组分别跑 TOPSIS + CRITIC 得 Ci，再对组内长度取均值排名 | 指标方向：Designability ↑、Novelty ↓、Diversity ↑、Efficiency ↓ | Table 3：短组第 1 FrameFlow（Ci 均值 0.517）、第 2 Genie 0.464、第 5 RFdiffusion 0.238；中组第 1 RFdiffusion 0.531；长组只有 Chroma/RFdiffusion（0.354 vs 0.406） |

### B. motif-scaffolding 与酶位点扩展

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| M1 | 4 家条件方法 | 沿用 RFdiffusion 的 case 集（剔除 6VW1） | "we adopted the 24-cases benchmark set from RFdiffusion" | 24 case × 每 case 100 骨架： "we generated 100 backbones for each of the 24 benchmark cases of different methods" |
| M2 | 各家原协议 + motif 残基类型固定不重设计 | 生成后走同一条复折叠流水线 | 整体判据 sc-RMSD<2.0 Å（或 sc-TM>0.5）+ motif 保持判据：**"The success threshold is defined as refolded sc-TM of the whole structure > 0.5 and motif-RMSD < 1.0 Å"**（S13 Fig） | 结论 "All methods exhibited high variance in their distribution, implicating that their performances varied significantly across different tasks"；RFdiffusion 均值成功率约 40%（原句排版为 "demonstrated strong efficacy achieving an average success rate of approximately 40%, while GPDL and TDS generated considerably diverse backbones"） |
| M3 | 每个 case 的设计 | 按"骨架是否 designable × motif 是否保住"做四分类 | "we analyzed the outcomes of each motif-scaffolding task by grouping them into four categories"（overall success / motif failure / scaffold failure / overall failure） | "motif failure dominated the failed cases followed by overall failure"，且 "scaffold failure accounted for a minimal fraction of failed cases" ⇒ 作者判定 "meeting the overall designability is necessary, but not sufficient, for a successful design" |
| M4 | case 难度差异 | 逐 case 拆开看成功率与多样性，而不是只报均值 | 原文未给难度阈值 | 好例 2KL8（"the motif of 2KL8 has far more residues than its scaffold, allowing models to sculpt a small scaffold region more easily"）、分化例 7MRX_60（"showed divergent performances across different methods"）、困难例 4JHW；归因 "The varying performance like results from differences in the secondary structures and topologies of certain motifs, as well as the length scopes of motifs and scaffolds for different cases" |
| M5 | 酶活性位点 RA95.5-8F（人工 retro-aldolase） | 追加 5 种方法（4 个基础版 + RFdiffusion-enzyme）做最小输入条件生成 | 原文未给阈值；每法 100 骨架："100 backbones was generated and evaluated for each method" | 基础版 0/100（"We found the base versions for all four methods failed to produce a single solution for the active site of retro-aldolase"），RFdiffusion-enzyme 20/100；明细在未获取的 S3 Table |

### C. 这篇评测设计的骨架（一句话记住）

**先用一套固定的"设计器 + 预测器 + Top-N + 动态阈值"把不同来源拉到同一条流水线里，再按长度/难度分层，最后用 TOPSIS+CRITIC 合成一个组内 Ci。** 它的价值在协议形式（可借），它的风险也全在协议形式（分母、覆盖矩阵、权重来源；见第 6、7 节）。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（正文位置/原句片段） |
|---|---|---|
| 7 种方法 | 参评骨架生成器（Genie/FrameDiff/RFdiffusion/TDS/GPDL/FrameFlow/Chroma） | Table 1；摘要 "We thoroughly evaluated seven representative methods" |
| 5 法（无条件）/ 4 法（条件） | 两类任务各自实际覆盖的方法数 | Author summary "We evaluated five and four methods in terms of unconditional generation and motif-scaffolding" |
| 长度档 50–1000，9 个唯一长度 | 无条件生成的评测长度 | Table 2；S1 Fig "9 (number of unique lengths) × 20 = 180 unique backbones" |
| 100 骨架 / 每法每长度；10 序列 / 每骨架 | 评测样本量（即所有成功率的分母） | Fig 1 图注；Methods "We generated 100 backbones with 10 sequences for each backbone to be evaluated" |
| sc-TM > 0.5 | designability 判据（无条件生成，Top-3 口径） | Methods "We use the success definition of sc-TM > 0.5 for unconditional generation (protein length ranges from 50 to 1000)" |
| sc-RMSD < 2.0 Å | designability 判据（motif-scaffolding；骨架 <150 残基） | Methods "For evaluation on motif-scaffolding, we use sc-RMSD < 2.0 Å since designed proteins here are typically under 150 residues" |
| motif-RMSD < 1.0 Å | motif 是否被保住的判据（与整体判据并联） | S13 Fig 说明 |
| N = 3；n = 3, w = 1 | Top-N 序列数；novelty 惩罚的取样数与惩罚强度 | Methods "Here we chose N = 3 for evaluation"；"We set n = 3 and w = 1 throughout our experiments" |
| 聚类 TM 阈值 0.5（另做 0.4/0.6） | diversity 的聚类口径 | Methods "We used a clustering TM-Score threshold of 0.5 based on the aforementioned consensus"；S16 Fig |
| AUC 步长 0.01（sc-TM）/ 0.1 Å（sc-RMSD） | 动态阈值扫描粒度 | Fig 2C 图注与 S7 Fig |
| 拐点 ~300 残基；≤300 时 ≥~80%；≥800 时 <30% | 设计性随长度的崩塌位置与两端水平 | Results "A notable turning point was observed at protein lengths of around 300 residues"（原句见第 3 节 W5b 两条引句） |
| ~70% / ~50% | 阈值收紧后 RFdiffusion 在短/中档仍保住的通过率 | "as it maintains success rates of around 70% and 50% for short and medium-length proteins, respectively" |
| pdb-TM 0.6–0.7 | 新颖度分布（与 PDB 最相近结构的 TM） | "the pdb-TM values predominantly range between 0.6 and 0.7, with no significant trends observed across the different methods or length categories" |
| α-螺旋 >50% | 生成库的二级结构偏置 | Results "with a α -helices comprising more than 50% of the structures in most cases"（该句含排版空格，本卡不作为引句） |
| bad bonds/angles 0%–20% vs 期望 0% / 0.1% | 局部几何合格率（MolProbity） | "far beyond the expected threshold of 0% for bad bonds and 0.1% for bad angles, respectively" |
| 效率跨 0.11 → 54.43（单位正文未标） | Table 3 Efficiency（↓）列的极差：FrameFlow@50 最快，RFdiffusion@1000 最慢 | Table 3；正文 "the processing speeds of the current methods are still in the range of several minutes" |
| Ci：短组 FrameFlow 0.517 第 1 / Genie 0.464 第 2 / Chroma 0.403 / FrameDiff 0.365 / RFdiffusion 0.238 第 5 | 短蛋白综合排名（**注意 RFdiffusion 在短组垫底**） | Table 3 |
| Ci：中组 RFdiffusion 0.531 第 1、FrameDiff 0.399 第 2、Chroma 0.296 第 3；长组 RFdiffusion 0.406 第 1、Chroma 0.354 第 2（长组仅 2 法） | 中/长档综合排名 | Table 3 |
| 24 个 case × 100 骨架 | motif-scaffolding 基准规模 | "we adopted the 24-cases benchmark set from RFdiffusion"；Fig 1 图注 |
| ~40% | RFdiffusion 在 24 case 上的平均设计性成功率（sc-RMSD 口径，非实验） | "demonstrated strong efficacy achieving an average success rate of approximately 40%" |
| 0/100（4 法）与 20/100（RFdiffusion-enzyme） | RA95.5-8F retro-aldolase 活性位点案例的复折叠成功率 | "We found the base versions for all four methods failed to produce a single solution for the active site of retro-aldolase"；"we found RFdiffusion-enzyme succeeded 20 out of 100" |
| 180 骨架 / 1800 序列；900 序列 | 两处评估器敏感性对照的规模 | S1 Fig（ProteinMPNN vs ESM-IF1）；S2 Fig（ESMFold vs AF2-noMSA vs OmegaFold） |
| p < 0.001（部分组） | novelty 加/不加惩罚的 Mann-Whitney U 检验 | "The results indicate significant differences in some groups with p-values < 0.001"；具体 6.11e-8 等数值在抽取文本里被排成 "6 . 1 1 × 1 0 - 8"，故不作引句，明细在缺失的 S2 Table |

## 5. 结论——作者说了什么

1. **两个瓶颈**：摘要原句 "generating long proteins for unconditional generation and accurately reconstructing motifs are key bottlenecks for most methods"。
2. **无条件生成整体可用，但有长度墙**：≤300 残基各家都强（≥80%），越过 300 快速下滑，≥800 掉到 30% 以下；短蛋白上 "FrameFlow , Genie and FrameDiff generated short proteins that were almost entirely designable, while RFdiffusion demonstrated the most consistent performance across all lengths"。
3. **综合排名没有全能冠军**："We found FrameFlow and Genie performing the best on short proteins and RFdiffusion showing outstanding performance for long proteins"，并且 "no single method consistently performed the best or worst across all groups, indicting that each method excels in different scenarios"，因此实践建议是 "we recommend a flexible and personalized selection of methods in practical applications, tailored to achieve the most optimal performance for specific circumstances"。
4. **RFdiffusion 的优势被归因于预训练折叠模型**："We argue that the outstanding performance of RFdiffusion largely benefits from its integration with the pre-trained structure prediction model RoseTTAFold"（作者用 argue/hypothesize 措辞，非实验证明）。
5. **新颖度不该再被单独强调**：讨论区 "While novelty has been overemphasized in prior studies, its practical relevance to biological applications appears limited, as methods showed minimal disparities in this regard"；并主张计算 novelty 时应部分考虑设计性。
6. **条件生成的失败主要栽在 motif 重建，而不是骨架整体不可折**：四分类显示 motif failure 占主导、scaffold failure 极少 ⇒ "meeting the overall designability is necessary, but not sufficient, for a successful design"，他们进一步外推 "designing a physically plausible protein structure is more crucial than simply meeting certain conditions"，并给出方法论建议 "extending a well-established unconditional generation model to conditional generation is more efficient than developing a conditional generation model from scratch"。
7. **全体方法偏向规整、螺旋富集、偏紧的球状结构**，loop/IDP 产出弱；局部几何合格率普遍不达标（bad bonds/angles 远超 0% / 0.1% 的晶体基准）。
8. **效率仍是分钟级**，与秒级的序列设计方法有量级差；作者说改进推理速度是该领域重要方向。
9. **酶活性位点这个最小输入任务**：4 种基础方法 0/100，加了活性位点微调 + 底物外电势的 RFdiffusion-enzyme 20/100；作者把这解读为微调与外源信息的重要性。
10. **作者自限**：这套评测全是计算侧的（"Although our evaluations were conducted in silico"），其定位是 "This framework can identify designable scaffolds, facilitating high-throughput filtering for downstream in vitro experiments"；复合物/动态骨架生成 "methods focusing on generating protein complexes or dynamic backbones critical for the design of enzymes of allosteric proteins are still in an early stage of development"。审稿人的定性是 "Although the study is not as comprehensive as one might like, it does provide a significant and valuable effort in this direction"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的可迁移资产是"评测协议"，不是那张排名表。** CRITIC 是"客观定权"，权重由当次参与数据自身的方差与指标间相关性推出；TOPSIS 的 Ci 是"到组内理想解的距离"。两者合起来的直接后果是：**换掉参与池里任意一个方法、任意一个长度、或任意一个指标方向，Ci 与名次就会重算**。他们从没做 leave-one-out 或权重敏感性，所以第 5 节的排名只能读成"这一次这个池子里的相对位置"，不能读成方法能力的绝对刻度。
2. **"看起来更好"里有七处分母不可比，本卡逐条列出（这才是精读这篇的真正收获）**：
   - (a) **长档只有 2 个方法**（Table 2 的覆盖矩阵），"RFdiffusion 长蛋白第一"实际是二选一的胜出；而它自己在长档的 designability 是 0.654→0.465→0.384（600/800/1000）持续下滑，第 1 名与"能用"是两件事。
   - (b) **成功率的分子分母都是"该方法在该长度生成的 100 条骨架"**（他们定义得很干净："Success rate is defined by the number of backbones passing the sc-TM threshold divided by the total number of backbones within each group"），但**骨架长度本身由各家协议决定**（条件任务里 "TDS and GPDL generated proteins with mostly fixed lengths"，RFdiffusion/Chroma 随机采样，作者也承认 "The different experimental settings resulted in different sets of total lengths"）。于是同一 case 上各家面对不同难度，通过率不共享同一个分母池。
   - (c) **两个任务用两套阈值**（无条件 sc-TM>0.5、条件 sc-RMSD<2.0 Å + motif-RMSD<1.0 Å），他们又同时报 best 与 Top-3；历史文献多用 best-sequence。跨论文的"通过率"若要并表，必须先声明用的是哪一口径，否则数字看着矛盾（他们自己的 S4 Fig 就说 sc-RMSD 口径下"长档几乎没有可设计骨架"）。
   - (d) **diversity = unique clusters / total 会随长度机械上升**（作者原话承认 "diversity tended to increase with protein length, potentially due to the distinctive levels of redundancy in the training set at different lengths"），而且它和 designability 反向：FrameFlow designability 最高却 "FrameFlow had the lowest diversity compared with other methods"。**高 diversity 既可能代表"可用拓扑多"，也可能只代表"生成的东西散、失败模式杂"**，本文没有把这两种解释分开。
   - (e) **efficiency 没有按产物内容归一**：Genie 只出 Cα（作者因此把它排除出 SSE 分析："Genie was excluded from this test as it solely generates C α -only backbones"），Chroma 同时出侧链与序列（"Chroma has an internal sequence design module which is capable of generating backbones with sidechain atoms, which might contribute to its high clash scores"），AF2 类还要 MSA。把"每条骨架平均耗时"直接排进 TOPSIS，等于是**拿不等质的产物比单价**。
   - (f) **结构合格性指标对 Cα-only 表示并不成立**（没有侧链就没有 clash/bond 概念），所以 validity 这一维各家可比性不齐，却被用来支持"哪个方法更物理"的叙述。
   - (g) **novelty 的惩罚常数 w=1、n=3 未做敏感性**，而结论"新颖度与设计此消彼长、过去被过度强调"就建立在这个自设项上；审稿人对同一张图（Fig 2F）的显著性提出了直接质疑。
3. **评估器与生成器同源，是这套框架没处理的循环。** 生成器在 PDB 上训练，ProteinMPNN/ESMFold 也在 PDB（及其预测结构）上训练，于是 sc-TM 高更像"与 PDB 分布 + PMPNN 可解性一致"，而不是"能表达能折叠"。作者自己给的偏置证据其实指向同一件事（训练集把 loop 富集结构排除了，于是所有方法一起偏螺旋、Rg 偏紧）。**他们做了敏感性对照（换设计器、换预测器），但没有做一次外部效度检验**（哪怕拿一小批已有湿实验结果的设计集，看 sc-TM 口径能否复现实验命中）——这正好是 B09 做过的事。所以本文能排"模型间一致性"，**不能校准真实命中率**。
4. **最有价值的一条结论其实是负结果**：条件化任务里 motif failure 主导、scaffold failure 极少 —— 说明"**整体结构合理**"是门槛而不是加分项，而现有方法普遍在"满足指定子结构"上失败。对我们这种"位点几何必须对"的任务，这条比任何排名都直接。
5. **RFdiffusion-enzyme 的 20/100 不是方法能力，是"多给了信息"的收益**（微调 + 底物外电势）。正确的读法是：**条件任务的瓶颈在条件表达得够不够，而不是生成器本身**——这与第 4 条互相印证。
6. 与 B09 对照，两篇是同一件事的两个层级：B09 有"带结局标签的百万条历史实验"，所以能回答"**哪个筛子真的能预判实验**"；K42 没有实验标签，只能回答"**哪个生成器在统一模型口径下更自洽**"。**引用时必须分清这两类结论的强度**：前者是效度，后者是一致性。

## 7. 局限与失败（作者的 + 我们读出的 + 审稿人当场指出的）

**作者自己承认的**
- 全程计算侧，无湿实验：见第 5.10 条引句；框架的用处被限定为 "This framework can identify designable scaffolds, facilitating high-throughput filtering for downstream in vitro experiments"。
- 覆盖任务窄：只评 backbone，不含序列-结构联合设计、全原子生成、复合物与动态骨架——"methods focusing on generating protein complexes or dynamic backbones critical for the design of enzymes of allosteric proteins are still in an early stage of development"；他们也承认表示方式（Cα / frame / all-atom）本身就是差异来源。
- 偏置未修：螺旋富集、Rg 偏紧、loop/IDP 几乎不产，被归因于训练集，但本文没有对策。
- 单个案例（RA95.5-8F）说明不了酶设计能力，且明细表在补充材料。

**审稿意见直接命中的三条（这些句子在本地全文里，属原文）**
- 统计与图面矛盾："It appears contradictory that the distributions for Medium RFDiffusion with and without penalty look nearly the same, but have p < 0.001, while for Medium FrameDiff the distributions look different but are not statistically different"。
- 概念混用：审稿人指出"有序非规则结构"与"内在无序区"被当作同义词使用（"These are treated as synonymous, which they are not"）——这直接关系到"本文对 loop 的结论是否成立"。
- 覆盖面不足与补充材料缺字：Reviewer #1 说 "On pg. 4 of SI it appears that some text might be missing"；Reviewer #3 的总评为 "Although the study is not as comprehensive as one might like, it does provide a significant and valuable effort in this direction"，并希望条件化设计再做更多参数探索（"It seems that exploring strengths and weaknesses of different methods and their parameter choices in conditional design is a tremendous value of Scaffold-Lab"）。

**我们读出的（与第 6 节对应，此处只列"后果"）**
1. **外部效度缺失**：没有一条湿实验结局参与评分，因此"通过率"无法换算成"实验命中率"；这篇不能为任何"某法实验成功率 X%"提供依据。
2. **可比性未闭合**：长度覆盖矩阵残缺（长档 2 法）、条件任务各家总长不同、效率未按产物内容归一、validity 指标对 Cα-only 方法不适用——四条叠在同一个 TOPSIS 分数里，等于把不可比项直接相加。
3. **口径自由度未做敏感性**：N=3、w=1、聚类 TM 0.5（S16 只对 diversity 做了 0.4/0.6）、AUC 步长 0.01；排名对这些常数的稳健性没有报告。
4. **本地不可核验的部分**：S1–S16 图与 S1–S3 表（含 24 case 定义、显著性明细、RA95.5-8F 各法成功率）与作者回复信均未获取；Table 3 Efficiency 的单位正文未标注，本卡只报数值不报单位。
5. **本文没有 MD**：只在讨论里提到 loop/IDP 通常用 MD 或构象采样研究——不许把这篇当"MD 判据有效/无效"的证据。

## 8. 迁移判断：我们若要比较多种候选来源，这套评测该怎么设计

**可迁移（直接怎么用在我们的漏斗上）**

1. **把"下游评估器"固定下来，让被比的只剩来源本身。** 他们的做法是全程 "was used as the sequence designer throughout the pipeline, as it has been widely utilized and validated by wet-lab experiments" + "We chose ESMFold as the standard refolding predictor due to its speed and competitive performance on long proteins"。对应到我们的多来源候选（Foldseek 命中的天然聚合酶 / 结构通道生成的骨架 / 序列 motif 检索 / 既有突变体库）：统一同一个逆折工具、同一个预测器、同一版本，写进 `run.md`；否则"来源 A 比 B 好"可能只是"评估器偏爱 A 的分布"。
2. **做一次评估器敏感性对照，哪怕只做相关性。** 他们至少换了设计器（ProteinMPNN vs ESM-IF1，180 骨架/1800 序列）和预测器（ESMFold vs AF2-noMSA vs OmegaFold，900 序列）。我们要照抄这个动作：同一批候选用两套逆折/两套几何判据各跑一遍，报告秩相关；不一致就把结论降级为"评估器依赖"。
3. **分母必须钉死成同一个数。** 他们每个来源在每个长度都是 100 条骨架 × 10 条序列，且明确 "Success rate is defined by the number of backbones passing the sc-TM threshold divided by the total number of backbones within each group"。我们过去踩的正是这点：不同来源的召回规模差 2 个数量级，通过率当然不可比。规定：**每来源同一 N（按最小来源定，宁可下采样），并报通过数/该来源总数**；下采样要记随机种子。
4. **分层比较，不报混合总分。** 他们按 short/medium/long 分开排名，正因为 designability 对长度极端敏感（≤300 时 ≥80%、≥800 时 <30%）。我们的候选来源要按**事件层（第一步 游离底物起始 / 第二步 中间体形成 / 第三步 第二底物 vs 副反应竞争）**或按 fold class 分层，同层内才谈高低；混合总分会被来源构成比主导。
5. **阈值当自变量扫，报 AUC 而不是单点。** 这条直接治"各来源用对自己有利的阈值"：把判据阈值从松到紧扫一遍（他们用 0.01 步长），看排序是否随阈值翻转；**排序随阈值翻转 = 结论不成立**，只能报"在 X 阈值区间内 A 优于 B"。
6. **双口径并报**（best vs Top-k）：他们同时报 best 与 Top-3，用来区分"勉强能过一条序列"与"结构真的稳健"。我们的候选也应并报"最好一次读数"和"前 k 次读数均值"（k 预先固定、不许事后挑）。
7. **单价与通过率并列，且必须归一化。** 他们把 efficiency 纳入排名（同硬件、每骨架平均时间："All tests were conducted under identical hardware resources"），但**没按产物内容归一**——我们要修这一点：核时按"每通过 1 个候选来源的闸口需要多少 GPU·h"计，并把长度/是否含侧链/是否需 MSA 写进分母。已实测单价（MD 156.6 ns/day、新体系 10.6 GPU·h、xTB 271 原子 153.3 s/评价）继续沿用。
8. **失败分型优先于名次。** 他们的四分类（overall success / motif failure / scaffold failure / overall failure）把"该改进哪一环"变成可执行问题。我们对应建三类失败：折叠/整体结构不成立、催化几何不满足约束（theozyme 距离/角度/预组织）、满足约束但被竞争路径吃掉；并允许 UNKNOWN 与 METHOD_FAIL 两个状态（不许把方法失败算成候选失败，这条是我们已经踩过的坑）。
9. **基准集不许被"最弱的被评者"反向裁剪。** 他们为了 TDS 不能做复合物而删掉 6VW1（"We basically followed the benchmark set collected by RFdiffusion except 6VW1 since it is a complex generation task which TDS was not capable to perform"）。我们若要比较多种来源，**基准集合必须固定且与来源无关**；某来源跑不动的项要保留并标 METHOD_FAIL，而不是从面板里删掉。
10. **复合分数的权重必须预注册 + 做留一敏感性。** TOPSIS/CRITIC 形式可以借（多维指标压一个数确实便于沟通），但必须先写权重与方向、再算，且额外报"去掉任一来源/指标后的名次变化"。这一步他们没做，是这篇最容易被后续引用误读的地方。

**不可迁移（为什么不能照搬）**

1. **判据本身与催化无关。** sc-TM>0.5 / sc-RMSD<2.0 Å / motif-RMSD<1.0 Å 测的是"一条序列能否折回给定骨架"和"指定残基是否留在原位"，**不测距离-角度几何、不测质子转移能垒、不测产物选择性**。目标酶的成功要的是三步化学事件与竞争副产物，结构自洽既不必要也不充分。本库判据总纲明令不许把 binder/折叠类阈值当酶活闸口，本文的阈值同样不许。
2. **数字不许当我们的概率。** 全文没有一次湿实验；20/100 与 0/100 都是 ESMFold 复折叠口径，且 RFdiffusion-enzyme 额外使用了活性位点微调与底物外电势。**不许**由此写"某法对目标酶设计成功率约 20%"或"骨架生成对酶活通过率 X%"（这是硬规则，也是本文最容易被误引的一句）。
3. **它评的是 backbone 层，我们要的是构象系综与动态。** 本文对 loop/无序区明确失能（作者归因训练集，审稿人指出概念混用），而我们的位点预组织恰恰依赖柔性区；这类问题该用系综/自由能判据（本文没有，也不提供命中率）。本文的 MD 只出现在讨论段的引用里，没有任何 MD 结果。
4. **它的"考卷"没有真值标签，所以不能替代我们该建的 B09 式面板。** 我们的评测最终目标是"判据能否预判实验"，需要已知产物/已知阳性的分层面板；K42 只能作为**协议形式模板**（固定评估器、同 N、分层、双口径、扫阈值、单价并列、失败分型），不能作为**判据效度**的证据。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K42_PMC13225634_text.txt

- **只对照这一份底稿**：`fulltext/K42_PMC13225634_text.txt`（由同目录 `K42_PMC13225634_fullTextXML.xml` 去标签、HTML 实体解码得到；本卡所有英文引句都是从这份纯文本复制粘贴，含原文的排版特征如 "FrameFlow ," 前的空格、"indicting"、"RFdiffu sion" 这类抽取产生的空格——凡是需要跨过这类空格/公式排版的句子，本卡改为不用作引句或直接不用）。同一篇论文若存在 NCBI 抽取版本，夹注编号位置不同，故以本行声明的这份为准。
- 登记底稿（`data/literature_cards/sources_map.json` 的 K42 项）：`K42_PMC13225634_fullTextXML.xml`、`K42_PMC13225634_text.txt`、`sources/cost-benchmarks.md`；对照行号 **`sources/cost-benchmarks.md:149`**（§3.9 内的一条题录级条目，本卡把它填成了全文级）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `阈值数字/候选数递减/成本统计`；第 6、7 节 ↔ `实验命中率/成本统计`（本文的实验命中率这一格只能是"无湿实验"）；第 8 节 ↔ `在方法演进链的位置`。
- 本地未获取、因此本卡未据其下结论的内容：S1 File（S1–S16 图、S1–S3 表）、`Response to Reviewers.docx`、主图 Fig 2–5 的原图数值。凡涉及这些的表述，本卡只引正文/图注里出现过的句子。
- 本卡自检：`scripts/verify_literature_cards.py --only K42 --no-report` 把卡内所有被直双引号包住、不含中日韩字符、≥20 字符且≥12 个字母的片段，在该底稿里做 NFC 归一 + 空白折叠后的逐字查找；本轮结果见该命令输出（引句全部命中才交回）。
- 未核验的部分：引句只证明"原文确实这么说"，不证明"原文这么说是对的"。第 6、8 节里关于分母不可比、循环性、权重敏感性的判断是本卡推断，其成立依赖于第 3、4 节记录的协议细节；若要用于实际评测设计，需按第 8.10 条在我们自己的面板上重跑一次留一敏感性。

<!--CSV回填
work_type=论文（纯计算基准/评测框架，无湿实验）
target=7 种蛋白骨架生成方法的横向评测：无条件生成（50–1000 残基，9 个长度档）+ motif-scaffolding（RFdiffusion 24-case 基准）+ 追加 RA95.5-8F 人工 retro-aldolase 活性位点案例
backbone_generation=不自己造生成器；直接调用参评方法：Genie、FrameDiff、RFdiffusion、TDS、GPDL、FrameFlow、Chroma（另加活性位点微调版 RFdiffusion-enzyme）；序列统一由 ProteinMPNN 出、结构统一由 ESMFold 单序列复预测
computational_filters=designability（sc-TM 自洽 / sc-RMSD 自洽 + Top-N 策略）、novelty（Foldseek 搜 PDB 的 pdb-TM，再按低设计性加惩罚）、diversity（Foldseek-Cluster 唯一簇数/总数）、efficiency（同硬件每条骨架平均耗时）、结构性质（DSSP 二级结构、Rg 对照经验回归、MolProbity clash/bad bonds/bad angles）；综合排名用 TOPSIS + CRITIC 客观定权得 Ci
thresholds=无条件生成 sc-TM>0.5；motif-scaffolding sc-RMSD<2.0 Å 且 motif-RMSD<1.0 Å；Top-N 取 N=3；novelty 惩罚 n=3、w=1；聚类 TM 阈值 0.5（敏感性 0.4/0.6）；动态阈值 AUC 步长 sc-TM 0.01、sc-RMSD 0.1 Å；MolProbity 期望 bad bonds 0%、bad angles 0.1%
md_used=否（仅讨论段引用 MD 作为研究 loop/IDP 的常规手段，本文无任何 MD 运行或结果）
qm_used=否
experimental_methods=无湿实验；全部为 in silico 复折叠评测（ProteinMPNN 设计 + ESMFold 预测 + TM-score/RMSD/Foldseek/MolProbity 计算），实验类指标一律缺失
pipeline_counts=无条件：每法每长度 100 骨架 × 10 序列（9 个长度档；短组 5 法、中组 3 法、长组仅 Chroma+RFdiffusion）；条件：4 法 × 24 case × 100 骨架；酶位点案例 5 法 × 100 骨架；敏感性对照 180 骨架/1800 序列（换设计器）与 900 序列（换预测器）
hit_rate=无实验命中率。计算口径通过率：≤300 残基各法约≥80%，≥800 残基<30%；阈值收紧后 RFdiffusion 短/中档仍约 70%/50%；24-case motif-scaffolding RFdiffusion 平均约 40%；RA95.5-8F 位点 4 种基础方法 0/100、RFdiffusion-enzyme 20/100（均为 ESMFold 复折叠口径，非活性命中）
best_metric=未记录（本文无任何结合/催化实测指标，只有 sc-TM 0.956（RFdiffusion@长100 均值口径见 Table 3）、Ci 最高 0.531 等计算读数，不存在 Kd 或活性值）
cost_or_stat_note=效率横评：同硬件、每骨架平均生成耗时跨约 3 个数量级（Table 3 中 0.11 至 54.43，正文未标单位，正文称方法速度为分钟级）；综合排名 Ci 短组 FrameFlow 0.517 第 1、RFdiffusion 0.238 第 5，长组仅 2 法参评；novelty 加/减惩罚的 Mann-Whitney U 检验部分组 p<0.001（明细在缺失的 S2 Table），审稿人指其与图面矛盾
role_in_timeline=继 RFdiffusion/FrameFlow/Chroma 等单方法论文之后出现的骨架生成"统一评测层"文献：把各家自定义的 designability/novelty/diversity/efficiency 拉进同一条 ProteinMPNN+ESMFold 复折叠流水线，加 Top-N 与动态阈值 AUC，再用 TOPSIS+CRITIC 出分长度档排名；结论是"无全能冠军、瓶颈在长蛋白设计性与 motif 重建"，但全程无湿实验标签，故属于"模型间一致性排序"，与 B09（用百万级带结局实验数据考核筛子）构成互补的两级证据强度
source_pointer=data/literature_cards/fulltext/K42_PMC13225634_text.txt（同源 fullTextXML 267,564 B，2026-10-20 抓取）；对照底稿 sources/cost-benchmarks.md:149；CSV 行 K42；代码 https://github.com/Immortals-33/Scaffold-Lab，骨架数据 https://zenodo.org/records/20080699
CSV回填-->
