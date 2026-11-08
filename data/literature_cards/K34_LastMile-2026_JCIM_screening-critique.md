# [K34] 最后一公里问题：把「漏斗末端该用哪个打分器」做成一次大规模批判性基准

Wang Xiaowen, Hentabli Hamza, Mettu Akhila, Gautam Shubha, Kireev Dmitri（密苏里大学文理学院化学系；通讯 kireev）
J. Chem. Inf. Model. 2026, 66 (10), 5964–5977 · DOI 10.1021/acs.jcim.6c00942 · PMCID PMC13213910
开放获取（CC BY 4.0）· https://doi.org/10.1021/acs.jcim.6c00942 · 代码 https://github.com/kireevlab/Last-mile-physics-based-AI-for-VS

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K34**（组：通用方法学; 口径对照；文献类型 benchmark） |
| 本文取回方式 | inventory 登记 `fetch_channel=epmc_search_then_fulltext`（Europe PMC 检索后取 fullTextXML），本地抓取日期 2026-10-20 |
| 本地全文① | `data/literature_cards/fulltext/K34_PMC13213910_fullTextXML.xml`（192,462 B，门禁不参与比对，`.xml` 被排除） |
| 本地全文②（本卡引句底稿） | `data/literature_cards/fulltext/K34_PMC13213910_text.txt`（82,428 B，去标签单行纯文本；按核验器同一 `norm()` 归一后 82,282 字符） |
| 登记底稿② | `sources/cost-benchmarks.md`（本目录下的先行调研卡片，§二与 §3.6）；本卡数字与其口径一致，见第 4 节 |
| 证据级别 | **全文级**（本卡所有引句均可在上述纯文本里逐字命中；见第 9 节自检） |
| 元数据行给出的题录 | 本地纯文本头部含 PMC13213910、PMID 字段 42095677、DOI、卷期页码 66/10/5964-5977，以及一组 2026 年 3–5 月的日期字段（去标签后只剩裸数字，投稿/修订/接收/在线的顺序无法确定，本卡不据此断言具体日期）；CSV 的 `PMID/PMCID/arXiv` 列登记为 未记录，故本卡把 PMID 视为**底稿元数据，未独立核验** |
| 作者方法学立场（影响解读） | 刻意只用公开软件（GROMACS + 标准 ABFE 协议）与标准化参数，以便非专家直接复用："we deliberately opted for a standardized implementation that could be readily adopted by nonexperts."（他们自述这以牺牲部分算力为代价换取自动化，见第 5.6 条） |
| 未取到的部分 | 补充材料全部（Supplementary Figures S1–S5、Tables S1–S4、Data Sets 1–7）与正文 Figure 1–5 的原图数值：包括**逐复合物计算/实验 BFE 值、逐靶 TPR 全表（S2/S3/S4）、化合物性质分布 PDF（S1）**。凡需要这些数字的地方，本卡明写「正文未给出，仅有正文描述」 |
| 作者方法学立场（影响解读） | 刻意只用公开软件（GROMACS + 标准 ABFE 协议）与标准化参数，以便非专家直接复用："we deliberately opted for a standardized implementation that could be readily adopted by nonexperts."（他们自述这以牺牲部分算力为代价换取自动化，见第 2.6 节） |

## 1. 这篇到底解决什么（大白话 + 一句话）

**一句话**： docking 之后手上那一两百个候选，到底该花钱上哪种打分器——绝对结合自由能（ABFE）、端态法（MM/PBSA、MM/GBSA）还是 AI 打分（7 个模型）——这篇用两个基准集把这件事**逐项量出来**，并给出一个分阶段建议。

**大白话版**： docking 出的命中列表假阳性极高，公开文献里的命中率又因为「失败的筛选没人写论文」而被系统性夸大。作者把漏斗**末端**单独拿出来当考题：末端每化合物成本高几个数量级，错一步整批钱就白花，这就是他们借物流术语说的「最后一公里」难题。他们建了两套互补的基准：一套是**定量的**（PDBbind 里 632 个有实验 Kd/Ki 又有晶体结构的复合物，问「算出来的自由能像不像实验值」），一套是**排序/判别型的**（DUD-E 的 135 个结合体 + 180 个诱饵，问「能不能把真的挑出来」）。结果两条轴上的排名**几乎反过来**：端态法在定量轴上不行、在判别轴上还行；多数 ML 模型在定量轴上好看（因为训练数据重叠）、在判别轴上等于随机。最后他们建议：AI 模型 Boltz-2 当主过滤器削大库，末端再对少数候选上 alchemical ABFE。

**为什么这张卡对我们最要紧**： 这篇的主题不是「某个新判据多好」，而是**「判据在不同口径的基准上会换位子，而且事前无法判断这一枪可信不可信」**——正是我们盲测过不了门时该读的那篇。

## 2. 难点与应对（作者自述，不是我们的推测）

1. **公开发表的筛选命中率本身就是被污染的指标**。作者指出社区只有成功案例可看："these estimates are highly likely to be skewed by survivorship bias, which refers to the reality that unsuccessful screening campaigns are almost never published." → **应对**：不用文献命中率做基准，改锚在 CACHE 盲测（提交 100 个虚拟命中、由组织方统一采购与实验验证）上："Results from CACHE Challenge #1 showed that only 7 of 23 participants identified any experimentally confirmed hits, and in CACHE Challenge #2, this number was only 5 out of 25."（即两个挑战分别只有 23 人中的 7 人、25 人中的 5 人拿到实验确认命中；逐靶细节在补充材料，本卡未取到）
2. **赢家赢在 docking 之外，机制不明**。"it was not the choice of docking algorithm, as most participants, including the winners, relied on widely used software such as AutoDock-GPU, AutoDock Vina, or Glide." 作者把成功归到别处（预筛、增强打分函数、MD 类 ABFE/RBFE 的重度使用）。→ **应对**：把「哪个环节值钱」写成一个可测问题，直接用一套标准化协议把所有候选打分器放在同一口径下重跑，排除软件差异。
3. **末端成本与前面所有步骤差几个数量级，容不得浪费**。"the costs per compound in this final step are orders of magnitude higher than in all previous steps"；且即便一个实验室付得起 100 个化合物的 ABFE（"For a typical VS study, a laboratory could readily afford ABFE calculations for up to 100 compounds."），这 100 个可能一个真的都没有。→ **应对**：不假装能算整库，而是用超几何分布把小基准的结果**投影**到实际场景（N_tot=1000、N_pos=10、n=100），把「该给多少个候选上贵判据」变成有概率语言的问题。
4. **贵判据跑之前无法预判这一枪准不准（这是本文最关键的一次「判据失效」）**。他们系统性试了可前瞻获取的性质——蛋白/配体分子量、配体埋在蛋白里的比例（用邻近蛋白原子数近似）、口袋残基平均亲脂性——结论是分开的高低子集相关性同量级："the ABFE values for all of the split subsets show similar levels of correlation with the experimental data and hence cannot be used as useful criteria to prospectively assess the accuracy of ABFE predictions"。亲和力高低也不行："The difference between these two subsets is insignificant, indicating that tighter binders are not simulated more accurately than weaker binders." → **应对**：本文**没有**给出可用的自评估判据；作者的做法是**放弃这条线**，改为给出「平均而言可靠 + 逐靶分开看」的工程建议。**这是本文未解决的部分，且被作者明确写进正文。**
5. **端态法的「改进」是负改进**。MM/PBSA 与 MM/GBSA 各跑三种模式（不做熵修正、正常模式分析 NMA 修正、相互作用熵 IE 修正），结果是："Overall, none of the methods demonstrated satisfactory performance, and, consistent with earlier evidence, the entropy-corrected methods performed even worse than the original MM/PBSA and MM/GBSA." → **应对**：不把失败的配置藏起来，三种模式全报（Figure 2A–F）；并额外检查端态法是否也受那些性质影响——"The accuracy of both end-state methods appeared unaffected by any of these factors"（即同样无可用于自评估的因子）。
6. **ML 打分器在两个基准上换位子，暴露训练域问题**。多数模型在 PDBbind 上好看（与原文报告相当），在 DUD-E 上等于随机："Because they were never exposed to true nonbinders during training, it is unsurprising that they fail to distinguish binders from decoys in the DUD-E data set." 另有反向案例：TopologyNet 与 Yuel 在他们独立整理的 PDBbind 子集上远低于其自报成绩（"two other methods, TopologyNet and Yuel, show markedly lower performance, with a Pearson correlation slightly exceeding 0.5 compared to approximately 0.75 as reported in the original sources."），作者猜是其训练时把噪声 IC50 当亲和力导致过拟合（"which may be attributed to overfitting to noise caused by the inclusion of noisy IC50 data as a proxy for binding affinity."）。→ **应对**：基准集设计上**强制两轴分离**——定量轴（PDBbind）与判别轴（DUD-E）分别建、分别报；并把「域适用性」列为被前人忽视的问题（"The issue of domain applicability has been largely overlooked in previous studies"）。
7. **贵方法的起点构象只能来自 docking，而 docking 会给出错 pose**。55 个有晶体的活性配体里 43 个 docking pose 与晶体接近，12 个 RMSD > 3 Å。→ **应对**：专门做「同一批配体改用 docking pose 起算 vs 用 X-ray 起算」的回顾对照："Of the 12 alchemical calculations started from divergent docking poses, five showed significant differences (greater than 2 kcal/mol) when compared to those initiated from X-ray structures. Four of these five calculations resulted in weaker predicted affinities, thereby increasing the risk of false negatives."，并把代价量化为一句可核查的估计："one might expect to lose 2 to 5% of active compounds (if any) as false negatives in a typical screening campaign due to incorrect docking poses."
8. **基准集自身的已知偏差无法回避**。DUD-E 的诱饵有时靠简单物化性质就能和活性物分开，且每个靶的活性物化学多样性有限："the DUD-E data set we used for the VS-like benchmark has known limitations and biases, such as decoys that can sometimes be distinguished from actives based on simple physical properties rather than true binding interactions, and limited chemical diversity among active compounds for given targets." → **应对**：明知有偏仍然使用，理由是**可比性优先**（MUV 靶覆盖窄、DEKOIS 2.0 窄、LIT-PCBA 有高通量实验本身的假阳/假阴与干扰），DUD-E 是领域事实上的金标准；这是一个公开承认的取舍，不是被忽略。
9. **各打分器的失败靶点几乎不重合，无法用「换个便宜判据」兜底**。"The analysis revealed very weak correlations among the different methods, suggesting that their failure points are largely method-specific."（正文只给定性结论 + 三个举例靶；完整逐靶矩阵在 Supplementary Tables S2/S3，未取到）→ **应对**：把「方法×靶」的交叉表现作为独立分析层，最终推荐因此只看**唯一在九个靶上都稳的**方法（ABFE）。
10. **小基准不能直接用常规分类指标**。15 活性/20 诱饵的构成让 sensitivity/ROC-AUC 失去现实含义："the small size of our benchmark data sets (15 actives and 20 decoys per target) and the artificially high fraction of active ligands make these standard metrics less representative of a real-world virtual screening setting." → **应对**：弃用 ROC-AUC 作为主指标，改自报 TPR + 随机选取下的精确概率 + 投影到实际场景的可回收活性数（第 3 节 C 段）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **物理侧三种**：(i) alchemical ABFE（绝对结合自由能，GROMACS 实现的标准协议，BAR 估计子）；(ii) MM/PBSA；(iii) MM/GBSA（后两者为端态法，gmx_MMPBSA v1.6.2）。作者对端态法的定位写得很直白："In addition to theoretically rigorous alchemical calculations, we explored the value of two popular empirical simulation-based methods."，并解释为什么必须把它们拉进来对比："While end-state methods require similar computational time per affinity calculation as alchemical ABFE techniques (on the order of hours), they utilize an order of magnitude fewer compute nodes, enabling significantly higher parallelization."
- **AI/ML 侧七个**：GNINA、K DEEP、OnionNet-2、TopologyNet、Yuel、RF-Score-VS、Boltz-2。选择标准是架构多样性 + 已报性能 + 有源码："The seven ML models were selected to represent the diversity of approaches"；且作者点明它们的共同出身："Most of the above methods are trained and tested on subsets of the PDBbind database."
- **QM**：只出现在配体参数化环节（RESP 电荷由 HF/6-31G* 层级 ESP 拟合，Gaussian 16），**不参与打分与排序**——所以本卡 `qm_used` 记为「否（仅力场参数化）」。
- **MD**：整篇的物理判据都建在 MD 轨迹上（AMBER14SB + GAFF、TIP3P、PME、2 fs、5 ns 生产段），故 `md_used` = 是（主筛选器本体，不是事后机理）。
- **没有做的事**：没有湿实验验证新命中（全部为回顾/benchmark 计算）、没有 RBFE、没有把方法部署到真实内部库、没有做自由能微扰之外的增强采样。

### A. 两个基准集怎么建（本文最值得抄的部分：一条定量轴 + 一条判别轴）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | PDBbind v2020 refined 子集（2022-10-26 下载） | 先定「参考集必须同时有结构与定量亲和力」："The primary requirement for the reference affinity data set was the availability of experimentally determined 3D structures and affinity data" | 亲和力须以 Kd/Ki 且关系符为等号记录 | 起点：5,316 复合物 / 4,131 唯一配体 / 1,409 唯一蛋白 |
| A2 | 同上 4,284 唯一配体 | 成药性过滤（RDKit 实现），目的是让基准里的分子像「能当先导」的分子："Since the ultimate goal of this study is to evaluate the potential of BFE predictors in hit finding, we focused exclusively on ligands that could potentially serve as leads in drug discovery projects." | 修订 Lipinski：MW 250–600 Da、cLogP 1–5、HBD ≤5、HBA ≤10、可旋转键 <14；结构过滤：无磷、可离子化基团受限、至少一个环、无长脂肪链、无大稠环、无潜在毒性/高反应基团。原文口径："we retained ligands that satisfy Lipinski's rules, with the exception of molecular weight, which we restricted to the range of 250-600 Da." **注意原文两处口径不一致**：Results 写「排除多于一个可离子化基团」，Methods 写「可离子化基团不超过两个」——本卡按 Methods 的表述记录并在此标注，不做调和 | 削到 1,286 复合物："Overall, the filters reduced the data set to 1,286 protein-ligand complexes." |
| A3 | 1,286 复合物 | 自动蛋白制备（Maestro/Schrödinger 2022-4 加氢、重排键级、补环缺失残基、PROPKA pH 7.0 定质子化）与 Open Babel 配体转换跑一遍，失败的直接剔除 | 无（工程可用性即判据） | 147 个 PDB 文件处理失败 → 1,139 复合物："resulting in a set of 1,139 protein-ligand complexes." |
| A4 | 1,139 | 剔除金属蛋白（标准力场不描述配位） | 力场覆盖度 | 去掉 285 个金属蛋白 |
| A5 | 1,139 减 285 金属蛋白后剩约 854（本卡推算的中间数，原文未直接给该值，只给起止两端） | MD 运行时错误（range-checking、内存类）再剔除，然后进入全判据计算 | 稳定性 | "Some systems failed due to MD runtime errors, such as range-checking violations or memory-related issues." → 最终 632 复合物 / 606 唯一配体："This set was later further reduced to 632 complexes (or 606 unique ligands)." 另有正文并列表述："a data set of 632 protein-ligand complexes involving 206 unique proteins and 606 unique ligands was retained for all benchmark calculations" |
| A6 | 632 复合物 | **给基准集做「分层能力体检」**（关键一步）：统计靶分布、家族分布、化学多样性 | 蛋白超家族：124 个（SUPFAM 定义）；每靶配体数 1–56；≥10 个配体的靶有 9 个；Butina 聚类（ECFP4，Tanimoto 0.5） | "A total of 379 clusters were obtained, with cluster sizes ranging from 1 (263 singletons) to 10 (there are five clusters with more than 5 compounds)." 作者写明为何要挑多配体靶："Targets with high ligand counts are particularly useful for determining whether binding free energies can be more accurately predicted for individual targets compared to the entire data set." |
| A7 | DUD-E（SMILES 于 2024-04-29 下载） | 判别轴基准：作者自陈设计逻辑 "Here, the rationale was to test the benchmarked methods under conditions close to those in virtual screening campaigns."；每靶随机取 200 个化合物做 Glide flexible 对接，按 Glide score 取前 20 作诱饵；活性组用同一流程取前 15 | 靶数必须显著小于 PDBbind 集才付得起 ABFE："the number of targets must be significantly smaller compared to the PDBbind data set." | 沿用前作 10 靶子集（"a DUD-E subset involving 10 structurally diverse targets broadly covering the protein space"），其中 9 个与 PDBbind 交集：ACE, ADRB1, FAK1, GRIK1, HMDH, MCR, PGH2, PRGR, TRYB1；"This data set features a total of 315 ligand complexes"＝"135 binders (15 per target) and 180 decoys (20 per target)." |
| A8 | DUD-E 315 复合物 | 起点构象一律用 docking pose（因为多数没有晶体结构），AutoDock Vina 1.2.0，中心取自相应 X-ray 配体 | 网格 40×40×40 点、间距 0.375 Å、exhaustiveness 8 | "We utilized AutoDock Vina 1.2.0 for molecular docking studies."；有晶体的活性配体 55/135 被另用作 MD 起点，供第 2.7 节的构象敏感性对照 |

**基准集设计的核心逻辑（原文）**："The performance of the benchmarked methods on this second data set would be indicative of how useful they might be in a VS setting."——即：**定量轴回答「数值准不准」，判别轴回答「排序能不能把真的捞上来」，两轴必须分开建，否则会把「相关性好」误读成「能筛东西」。**

### B. 判据怎么算出来的（协议与阈值，全是原文数字）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 632 复合物 + 315 docking 复合物 | MD 前置：AMBER14SB（蛋白）+ GAFF（配体）；立方盒，复合物到边界最小 10 Å；TIP3P 显式水，0.15 M NaCl 中和 | "The system underwent energy minimization using the steepest descent algorithm to resolve steric clashes and unfavorable atomic interactions, terminating when the maximum force reached 2.4 kcal/mol/nm." | "Molecular dynamics (MD) simulations were performed using GROMACS v2022.2 software." |
| B2 | 同上 | 平衡 + 生产 | 100 ps NVT 与 NPT（298 K、1 atm）；生产段 5 ns 无约束，velocity-rescaling 恒温器；步长 2 fs，非键截断 12 Å，长程静电 PME | 轨迹以 RMSD 监控复合物完整性，通过者才进入三种自由能计算："The integrity of ligand-protein complexes during MD simulations was evaluated by monitoring root-mean-square deviations (RMSD). Next, MM/GBSA, MM/PBSA, and FEP calculations were conducted for complexes that passed the integrity checks." |
| B3 | 通过完整性检查的复合物 | ABFE 热力学循环 | 两条耦合路线（水中脱耦配体；溶剂中蛋白-配体脱耦）各 25 个 λ 窗，合计 50 窗；λ 从 0.0 到 1.0，0.1 步长至 0.8、0.05 步长至 1.0；前 12 窗只开 vdW、其余逐步开库仑；软核 sc-alpha 0.5、sc-power 1、sc-sigma 0.3；ΔH/Δλ 每 100 fs 记录；BAR 汇总 | "The number of λ-windows was set to 25, a frequently observed choice across recent publications."；"The complete BFE thermodynamic cycle comprised 50 λ-windows, with MD simulations of 5 ns per window."；"Free energy differences between the alchemical states were estimated using the BAR method." |
| B4 | 77 个复合物（亲和力均匀分布随机抽） | **λ 窗长度定标**（成本-精度拐点），跑 1/5/10/15 ns 四档 | 以 Pearson r 与 Spearman ρ + 散点图判优；结论：10/15 ns 相对 5 ns 增益小："the gain in accuracy for 10 ns and 15 ns windows (over the 5 ns window) is relatively modest given the additional computing power that such calculations would require." | 全文统一用 5 ns："The length of a λ-window was determined by running ABFE simulations with window sizes of 1 ns, 5 ns, 10 ns, and 15 ns on a subset of 77 ligand-protein complexes with uniformly distributed experimental binding affinities randomly pulled from the PDBbind data set."（该 77 子集同时也是定标用的 pilot，r=0.73/ρ=0.70，与全集 r=0.69 有差，见第 4 节） |
| B5 | 同一 77 复合物 | **取向约束做不做**的 A/B（Boresch-Karplus 算法） | 加约束提升相关性："While the application of restraints resulted in improved correlation metrics (with Pearson r increased from 0.73 to 0.77)"；代价："implementing spatial restraints requires additional λ-windows, which increases the computational cost by up to 30%." | 决定**不用**约束跑全集："because the unrestrained setup still achieved a highly respectable correlation of r = 0.73"，并补一条工程理由（自动化难、易在流水线里出错）。→ 注意这是一个**主动放弃精度换可自动化**的取舍，不是能力上限 |
| B6 | 复合物轨迹 | 端态法三种模式 | 5 ns 轨迹取最后 1 ns（1,000 帧）算 BFE；NMA 因太贵只用 20 帧，IE 用满 1,000 帧 | "MD trajectories of 5 ns were used for both MM/PBSA and MM/GBSA."；"The last 1 ns of 5 ns MD trajectories (1,000 snapshots) were used for the BFE calculations."；"The normal-mode analysis was limited to 20 frames due to its high computational cost." |
| B7 | 606 唯一配体 + 206 蛋白 | 七个 ML 模型按各自官方入口跑（KDEEP 走 OpenPlayMolecule 在线、OnionNet-2/TopologyNet/Yuel 走 GitHub/Bitbucket、GNINA 走 Colab 默认打分函数、Boltz-2 走共折叠、RF-Score-VS 走接触计数），全部登记运行日期 | 无判据，纯打分器输出 | "The prepared input files were uploaded to OpenPlayMolecule.org, where KDEEP was run online (on 11/16/2024) to calculate BFE values."；"GNINA docking was run on 1/3/2025 to predict the BFE values by using its default scoring function."；所有计算值打包为 Supplementary Data Set 6/7（**本卡未取到**） |

### C. 「在真实筛选里值多少」怎么折算（本文方法学上最硬的一环）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | 实际场景参数 | 从 CACHE 报告取 docking 主筛真实阳性率，用来设定投影目标 | "the true positive rate of a primary docking screen is approximately 1%." | 由 1% 得："identifying true actives from a 100-compound selection typically requires rescoring at least 1,000 docking hits, which would contain approximately 10 true actives." |
| C2 | 基准内每靶 15 活性 + 20 诱饵 | 用超几何分布算「随机抽 n 个恰好捞到 k 个真活性」的精确概率 P(k)，作为随机基线 | 基准取样设定："In our benchmark setup, N tot = 35 and N pos = 15 per target, and we selected n = 7 ligands to evaluate the success rate."；判据口径："Methods that provide significant predictive value show true-positive rates that are virtually impossible to observe by random chance under this exact distribution." | 实现：scipy.stats.hypergeom 的 pmf（"we used the hypergeometric distribution implemented in Python"）；对每个方法、每个靶都给 P(k) |
| C3 | 同上 | **把小基准的成绩投影到实际场景**：匹配两边累积概率 P(k≥·)，在 N_tot=1000、N_pos=10、n=100 假设下解出可回收活性数 | "Second, we used the hypergeometric distribution to mathematically project these benchmark results onto the more realistic virtual screening scenario" | 输出单位变成「100 个送测名额里能捞回几个真活性」，而不是抽象 AUC |
| C4 | 两轴成绩 | 逐靶一致性检查（哪一靶崩了） | 以「是否低于随机水平」为准（正文用 NTP ≤4 作随机基线附近的说法） | 结果见第 4/5 节；完整矩阵在 Supplementary Table S2–S4（本卡未取到） |

### D. 成本轴（判据强度必须与单价一起报）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| D1 | 自建 Hellbender 集群 | 记录三种层级的单价 | — | ABFE："A full alchemical calculation requires approximately 2 h on a dedicated high-performance GPU on our local Hellbender cluster"；端态法同样约 2 h/个但算力资源少约 50 倍："they consume roughly 50 times fewer computing resources than alchemical methods, allowing for extensive concurrent execution across available nodes."；GNINA/Boltz-2 为分钟级；常规 ML 单次前向、每秒分数个复合物（正文描述，未给逐条数字） |
| D2 | 单价 × 通过率 | 按成本给所有判据分档 | — | "The results of our study intuitively rank BFE predictors according to their computational costs." |
| D3 | 分档结论 | 给出分阶段漏斗 | 未给具体阈值数字（「先 AI 预筛 10^5 量级、再对数百个上 ABFE」，正文只给数量级） | "we recommend a multistage workflow." + 第 5.4 条原文 |

**这套流程的骨架值得单独记住**：先建**两个口径不同**的基准（A 段），再在**同一批轨迹**上把所有打分器跑齐（B 段），最后用**随机基线 + 概率投影**把成绩翻译成实际筛选语言（C 段），并始终与**单价**并列（D 段）。任何一条轴单独拿出来都会给出相反的结论——这正是本文标题里「critical」的意思。

## 4. 关键数字台账（数值 · 含义 · 出处；数字均可在本地全文里搜到）

| 数值 | 含义 | 出处（本卡小节 · 原文位置） |
|---|---|---|
| 5,316 / 4,131 / 1,409（配体侧 4,284） | PDBbind v2020 refined 子集起点（复合物/唯一配体/唯一蛋白） | §3 A1 · Methods「PDBbind Benchmark Set」首句 |
| 1,286 → 1,139 → 632（606 唯一配体） | 基准集三级漏斗：物化过滤 → 自动制备失败 147 个 → 剔 285 金属蛋白 + MD 运行错误 | §3 A2–A5 · Methods 同段 |
| 147 / 285 | 自动制备失败 PDB 数 / 因力场不覆盖而剔除的金属蛋白数 | §3 A3–A4 · Methods |
| 124 / 1–56 / 9 | 蛋白超家族数 / 每靶配体数范围 / 配体数 >10 的靶数 | §3 A6 · Results「Data Sets」 |
| 379 簇（263 单例，最大簇 10，5 个簇 >5） | 基准集化学多样性（Butina，ECFP4，Tanimoto 0.5） | §3 A6 · Results「Data Sets」 |
| 315 = 135 活性 + 180 诱饵（15/20 每靶）；10 靶、9 靶与 PDBbind 交集 | 判别轴基准规模 | §3 A7 · Results + Methods「DUD-E Benchmark Set」 |
| 200 → 20 / 15 | 每靶随机取 200 个对接、按 Glide 取得分前 20 为诱饵、活性取前 15 | §3 A7 · Methods |
| 55 / 43 / 12；RMSD > 3 Å；5 / 12；差异 > 2 kcal/mol；4 变弱、1 成真阴 | docking 起点 vs 晶体起点的敏感性链 | §2.7 · Results「Sensitivity to Starting Coordinates」 |
| 2 – 5% | 因 docking pose 错误而漏掉的真活性估计占比 | §2.7 · Discussion |
| 25 窗/路线，50 窗总计，5 ns/窗；λ 步长 0.1→0.8、0.05→1.0；前 12 窗只开 vdW；sc-alpha 0.5、sc-power 1、sc-sigma 0.3；ΔH/Δλ 每 100 fs | ABFE 协议全部关键参数 | §3 B3 · Methods「Alchemical Free Energy Calculations」 |
| 77；1 / 5 / 10 / 15 ns | λ 窗长度定标子集与四档 | §3 B4 · Results |
| r = 0.73 → 0.77；成本 +最多 30% | 取向约束的增益与其代价（77 复合物 pilot） | §3 B5 · Results |
| r = 0.69 / ρ = 0.68（全集）对比 0.73 / 0.70（77 pilot） | ABFE 定量精度从 pilot 到全集的回落 | 原文 Results「PDBbind Benchmark · Alchemical ABFE Calculations」末段 |
| 0.44 – 0.75（Pearson）/ 0.19 – 0.74（Spearman） | **同一判据在不同靶上的靶内相关性跨度**（≥10 配体的靶） | 原文 Results 同段（intratarget correlations）；本卡 §2.4、§6.2 |
| RMSE 2.30 vs 2.16 kcal/mol | 强结合半区 vs 弱结合半区的误差（差异不显著） | 原文 Results 同段（affinity 依赖检验）；本卡 §2.4 |
| 2（BRD4, WDR5）/ 3（BRD4, MK14, WDR5） | MM/GBSA 与 MM/PBSA 靶内 Pearson >0.5 的靶数（PDBbind 侧） | 原文 Results「End-State Methods」 |
| ~0.5 vs 自报 ~0.75 | TopologyNet、Yuel 在本基准 vs 其原文 | 原文 Results「ML Models」；本卡 §2.6 |
| 0.58（Boltz-2）；0.34/0.52（GNINA）；0.30/0.35（RF-Score-VS） | 三个模型在 PDBbind 定量轴上的 Pearson/Spearman | 原文 Results「ML Models」；本卡 §6.7 |
| TPR 94%（59 个预测阳性为真）；投影后可回收 10/10；只需点 17 个阳性即含全部 10 活性；5 靶 100% + 4 靶 86% | ABFE 在判别轴上的成绩（唯一九靶全稳） | 原文 Results「DUD-E · Alchemical ABFE Calculations」 |
| TPR 70%（MM/GBSA）/ 83%（MM/PBSA）；投影 8/10 与 10/10；MM/PBSA 点 38 个即含全部 10 活性 | 两个端态法判别轴成绩 | 原文 Results「DUD-E · End-State Methods」 |
| MM/GBSA：4 靶 TPR 57%（随机选择概率 43%）、HMDH 14%；MM/PBSA：HMDH 29%、其余 71–100% | 端态法的逐靶塌陷面 | 原文 Results「DUD-E · End-State Methods」（完整表为 Supplementary Table S3，未取到） |
| 早期 ML TPR 20–38%（TopologyNet 20%、随机概率 11%；K DEEP 24%、约 2%；GNINA 38%、P(k)=9.0×10⁻⁰⁴） | 训练于 PDBbind 的 ML 打分器在判别轴 ≈ 随机 | 原文 Results「DUD-E · ML Models」 |
| Boltz-2 81%（P=2.1×10⁻¹¹）/ RF-Score-VS 79%（P=1.6×10⁻¹⁰）；投影各 10/10；崩的靶：Boltz-2 为 HMDH+PGH2，RF-Score-VS 为 GRIK1+HMDH | 两个较新模型的判别轴成绩与各自失分靶 | 原文 Results「DUD-E · ML Models」 |
| 早期四种 ML 投影后仅回收 1–3 / 10；GNINA 5 / 10 但 9 靶里 5 靶差 | 「随机水平」的具体表现 | 原文 Results「DUD-E · ML Models」 |
| N_tot=35, N_pos=15, n=7（每靶）；N=307, pos=135, n=63（合并集）；投影 N=1000, pos=10, n=100 | 超几何检验与投影的全部参数 | §3 C2–C3 · Results + Methods「Hypergeometric Distributions」 |
| ~1% | 真实 docking 主筛阳性率（取自 CACHE 1/2） | §3 C1 · Results |
| ABFE ≈ 2 h/配体（专用 GPU）；端态法 ≈ 2 h 但资源少约 50 倍、节点少一个数量级；GNINA/Boltz-2 分钟级；标准 ML 亚秒级 | 三档成本阶梯（判据分层的依据） | §3 D1 · Discussion |
| 100 vs 1,000 | 一个实验室付得起的 ABFE 数 vs 要让命中列表被富集所需的评价数 | §1 引言段 |
| AMBER14SB / GAFF / RESP（HF/6-31G*，Gaussian 16）/ TIP3P / 0.15 M NaCl / 盒边界 10 Å / 最陡下降至 2.4 kcal/mol/nm / 100 ps NVT+NPT / 298 K / 1 atm / 重原子约束 239 kcal/mol/Å² / 2 fs / 非键 12 Å / PME | MD 与电荷参数化的全套设置 | §3 B1–B2 · Methods「Molecular Dynamics」 |
| GROMACS v2022.2 / gmx_MMPBSA v1.6.2 / AutoDock Vina 1.2.0 / AutoDock Tools 1.5.6 / 网格 40×40×40 点、间距 0.375 Å、exhaustiveness 8 / Maestro 2022-4 + PROPKA pH 7.0 / Open Babel / RDKit / acpype | 软件版本与对接盒设置（可复现清单） | §3 B · Methods 各小节 |
| 2022-10-26 / 2024-04-29 / 2024-11-16 / 11-18 / 11-20 / 11-22 / 2025-01-03 | PDBbind、DUD-E 下载与各 ML 模型运行日期（作者逐条登记） | §3 A、B · Methods |

## 5. 结论——作者说了什么

1. **定位**：这是（据他们所述）第一篇把 ABFE 放进虚拟筛选工作流里做大规模对比评估的工作："we present a large-scale benchmark study, which, to the best of our knowledge, is the first of its kind,"；补一句："This work addresses a gap in the critical assessment of MD-based methods for virtual screening." 以及口径声明："In addition, we compare computationally intensive, physics-based approaches with ML techniques within a standardized benchmark protocol." 他们同时交代了前人为何不够："Prior large-scale efforts exploring the potential of alchemical methods have primarily focused on relative binding free energy (RBFE) calculations to support lead optimization within chemical series" 与 "ABFE evaluations, in contrast, have so far been limited to smaller-scale studies, as summarized in recent reviews."，并点出唯一一篇 VS 式评测的指标缺陷："Only one of those studies specifically tested the performance of the alchemical ABFE approach in a VS-like setting, using small sets of actives and decoys against three targets."
2. **绝对排序结论**：贵判据确实最强且两轴都稳。"the alchemical ABFE method can be confidently recommended for prioritizing compounds in virtual screening, as it demonstrated consistently high performance with true positive rates between 86% and 100% across all targets."；且在靶层面是唯一稳的："The alchemical binding free energy calculation was the only approach that maintained consistently high performance across the entire target panel"。但同一句里立刻给出限制："However, its significant computational cost may render it inaccessible for processing large compound libraries."
3. **最意外的发现是「端态法与 ML 换位子」**："One of the least expected findings was the reversal of roles between the end-state MD-based methods and ML models."，拆开说就是摘要那两句："End-state methods scored well in recognizing actives from decoys in the DUD-E data set but showed little correlation with experimental values in PDBbind." 与 "Most ML models performed well on PDBbind, likely due to training overlap, but failed on DUD-E, except for GNINA and Boltz-2, which demonstrated a degree of generalization comparable to end-state physics-based methods."
4. **工程建议（他们的最后一公里答案）**："we recommend a multistage workflow." 具体是："Overall, a staged approach involving Boltz-2 as a primary filter followed by alchemical ABFE is likely to robustly and cost-efficiently enrich docking-based VS hit lists with true actives."；若非用端态法不可，则 "If end-state methods must be used, then there is a clear preference for MM/PBSA over MM/GBSA."，理由是 MM/GBSA 九个靶里崩了四个："MM/GBSA underperformed on four of nine targets, highlighting the highly variable performance that practitioners might encounter and raising concerns about its reliability."；Boltz-2 的地位："Among the other methods evaluated, the AI model Boltz-2 emerged as a highly efficient alternative, performing comparably to end-state physics-based methods but with excellent consistency across different targets and at a fraction of the computational cost."
5. **对 ML 的判词**："While ML models are not yet ready for widespread deployment"——原因不是模型小，而是训练域："Because they were never exposed to true nonbinders during training, it is unsurprising that they fail to distinguish binders from decoys in the DUD-E data set." 并把「域适用性」点名为被忽视的问题："The issue of domain applicability has been largely overlooked in previous studies"。
6. **约束与参数选择的自辩**：不加取向约束是主动取舍——"because the unrestrained setup still achieved a highly respectable correlation of r = 0.73"；不追求可变窗长也是主动取舍："While some computational resources might have been saved by adopting variable-length λ-windows, we prioritized a more conservative protocol to enable automated, curation-free execution."
7. **作者承认的误差与限制（原话层面）**：误差来源三条："The sources of error include the molecular mechanics force field (which is only an approximation of true quantum interactions), insufficiently fine windows, and undersampling of configuration spaces."；再加 pose 风险："Additionally, incorrect docking poses for certain ligands can lead to erroneous ABFE predictions."；基准偏差："the DUD-E data set we used for the VS-like benchmark has known limitations and biases"；以及一句对前人指标的批评："the reported ROC-AUC values" 来自活性/诱饵等量的数据集，"do not accurately reflect performance in real-world VS campaigns."
8. **作者明确没给出的东西**：没有任何可用的**事前**可信度判据（见第 2.4 条，原文判定为 cannot be used as useful criteria）；没有真实内部库的前瞻实验；没有对新命中做湿实验；没有逐靶完整矩阵进正文（都在补充材料）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **「判据的有效性是基准口径的函数」是本文最重要的一课**。同一批打分器在定量轴与判别轴上的名次几乎互换，说明任何「我们的判据效果好」这句话，如果不先声明是哪条轴，就没有内容。→ 对我们：漏斗里每个判据都必须标注它负责哪条轴（会不会催化 ≠ 结构像不像），并禁止用一条轴的成绩去给另一条轴背书。
2. **贵判据的通过，是「平均通过」而不是「这次通过」**。靶内 r 从 0.44 跨到 0.75，且作者找不到任何事前因子来预测单次计算的可信度——这意味着 ABFE 给出的是一个**期望层面的可靠性**，个体决策仍要靠外部证据（复算、双起点、失活对照）。→ 对我们：把「跑一次 MD/xTB 拿到一个数」当决策依据的做法，本身就缺这一层；我们需要**同一候选的多路独立评价**，而不是更强的单一评价。
3. **他们的漏斗末端有明确的随机基线与概率语言**。每个 TPR 都配了「随机抽也能得到的概率」。→ 对我们：任何盲测结果如果不附随机基线下的 P(k) 或等价置换检验，就无法区分「判据有效」与「面板太好猜」。这正是我们现在缺的口径。
4. **「1% 主筛阳性率 + 1000 里捞 10 个」这个设定，是本文全部结论的隐形前提**。他们从 CACHE 取 1% 这个数，把整个投影锚在实际场景上；如果我们的真实阳性先验不是 1%，就不能直接搬他们的「回收 8/10、10/10」这类换算结果。
5. **失败不共线，所以「串联便宜的判据」不等于稳健**。作者观察到各方法失败点几乎不重合（method-specific），因此他们的推荐是「便宜的 AI 预筛 + 贵的 ABFE 收尾」而不是「多个便宜判据投票」。→ 对我们：**投票式多判据在一个所有判据都会一起崩的靶上毫无用处**；盲测面板必须显式包含「已知难靶层」，专门测这种共线崩塌。
6. **他们的「最后一公里」不是精度问题而是成本问题**。全文最硬的一句话是把成本当排序维度："The results of our study intuitively rank BFE predictors according to their computational costs."——即先问「算得起几个」再问「算得准不准」。→ 这与 B09 的「效率 = 通过率 ÷ 单价」是同一个思想，只是这篇把它做成了三档成本阶梯的可引用版本。
7. **一处内部张力（我们的读法，不是作者的）**：摘要把「在 DUD-E 上有泛化」的例外归给 GNINA 与 Boltz-2，而正文结果给的是 Boltz-2 与 RF-Score-VS（81%/79%）；同时 RF-Score-VS 在 PDBbind 定量轴上是最差的（r = 0.30）。两个轴上极端相反的名次出现在同一个模型身上，说明**要么某一轴的评价口径不足以刻画它，要么其 DUD-E 高分部分来自与训练域无关的捷径**；作者没有对此展开解释（正文只写 RF-Score-VS 在定量轴最弱、在判别轴最好，未调停）。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自陈（可回原文核对）**

- 判别轴规模小、活性比例被人为抬高：每靶仅 15 活性 + 20 诱饵；作者因此弃用 ROC-AUC 类指标，改走超几何投影。他们说得很清楚：在小基准上观察到的假阳性率**低于**真实场景，"In a practical VS setting, where the number of decoys significantly outweighs the number of actives, this overlap may result in a higher false positive rate than observed in our benchmark study."
- 基准集偏差是已知且被接受的：DUD-E 诱饵可被简单物化性质区分、活性化学多样性不足（§2.8 原句）。作者的正当理由是可比性，不是无偏。
- 全部为回顾性评估，没有一次真实前瞻筛选；投影出的「能回收 10/10」是**分布外推**，不是实验观测。
- 定量轴上 ABFE 全集只有 r = 0.69（比 pilot 的 0.73 低），作者专门解释这一下降但没给出可预判的下限；RMSE 约 2.2–2.3 kcal/mol 意味着**单值不可用于精细能量排序**。
- 参数被刻意保守化以换自动化（定长 5 ns 窗、不加约束、统一协议），作者自承这会牺牲一部分可能的精度/算力效率。
- 金属蛋白被整体剔除（285 个）——也就是说，**本文全部结论对「活性位点含金属」的体系不作任何承诺**；这对我们是硬约束（详见第 8 节不可迁移第 4 条）。

**我们读出的额外风险**

1. **「1% 阳性率」是借来的先验，不是他们测的**。整个投影链条的量纲来自 CACHE 报告；若换成他们自己的先验，回收数会整体平移。引用他们的「10/10」必须连这个先验一起引用。
2. **两个基准的靶高度重叠（9/9）**，即判别轴上的靶同时也是定量轴上有标签的靶；同一批蛋白上的两种成绩不能当成「独立验证」。
3. **逐靶矩阵在正文里只有例子（HMDH、GRIK1、PGH2、FAK1、MCR、PRGR、TRYB1、ADRB1）**，完整表在 Supplementary Table S2–S4，本卡未取到；因此「只有 ABFE 九靶全稳」这句话我们**只能在作者断言层面接受**，无法自行复核其边界。
4. **§6.7 那处内部张力（RF-Score-VS 在两个轴上极端相反）作者没有解释**，说明这套双轴指标本身可能仍不足以刻画模型行为；不要把「两轴一致」当成方法学完备的证据。
5. **失败模式的归因是猜测**（训练域、噪声 IC50 过拟合、捷径），本文没有机制实验去证实这些解释。
6. 他们测的是**小分子**结合；催化事件、共价中间体、金属中心、多步反应坐标全部不在覆盖范围。

## 8. 对我们筛漏斗/盲测面板的迁移判断

### 可迁移（直接怎么用在我们的面板上）

1. **面板必须做成两条正交轴，各自出题、各自打分**。这篇用 PDBbind（有实验 Kd/Ki + 晶体结构）测「数值准不准」，用 DUD-E（多数没有结构、只有结合/不结合标签）测「排序能不能捞到真的」，结果两轴名次互换。**我们的对应做法**：
   - 定量轴：一批**已知产物结局**的酶/反应组合（能氨酰化 vs 不能，且有可测的化学计量或产物身份），用来问「我们的判据能不能给出与结局一致的强弱排序」。
   - 判别轴：一批**已知阳性 + 显式构造的阴性**，问「能不能把阳性排在阴性之前」，标签是二值的。
   - 任何判据只许在其中一条轴上获得成绩；**禁止**用结构自洽类的分数去声称催化预测能力。
2. **阴性集（decoy）要按物化性质配对，并且要防「可以被简单性质分开」**。DUD-E 的教训被作者明写（§2.8）：诱饵可被分子量/亲脂性一类性质区分，于是「区分能力」可能压根不是识别结合。→ 我们建阴性对照时必须**匹配**这些可观察性质（链长、Foldseek 相似度、pLDDT、序列复杂度、结构域组成），否则任何便宜判据都能"作弊"，面板会给出虚高成绩。
3. **每格必须带随机基线与精确概率**。他们的口径是：报告 TPR 同时报告「随机抽取观察到该 TPR 的概率」，并预声明「几乎不可能由随机得到」才算有判别价值。**我们的盲测面板照此办理**：每格（判据 × 靶家族 × 层级）给 N_阳 / N_阴 / 抽样数与随机概率（或置换检验 p 值），并预先写下「低于此概率才承认信号」。没有这一行，面板结果不能进漏斗。
4. **分层报告，不许报平均**。他们把靶内相关性从 0.44 到 0.75 的跨度直接摊开，并专门保留多配体靶来问「逐靶是否比全集更准」。**我们的面板分层应为**：候选来源家族 × 化学事件（第一步 游离底物起始 / 第二步 中间体形成 / 第三步 第二底物与副反应竞争）× 判据；每层单独出成绩，且**必须包含一个已知会全崩的难层**，用来测判据共线失效。
5. **判据失败点是否重合，要单独测**。他们发现各方法失败靶几乎不重合（method-specific），因此推荐「便宜 AI 预筛 + 贵 ABFE 收尾」而非多便宜判据投票。→ 我们该做一张**判据 × 候选的失败矩阵**，算两两失败重合度；重合度高就说明「再加一道便宜筛」不带来稳健性，只能再加**异质**判据（不同物理来源）。
6. **单价与通过率并列，形成三档成本阶梯**。他们的分档（亚秒 ML / 分钟级 co-folding / 小时级 MD 类，且端态法与 ABFE 同耗时但资源少约 50 倍）正好是我们需要的表达形式：把我们的判据按 结构类检索/共折叠类比 → MD → 量子化学 排成阶梯，每档标「每个通过闸口的候选花多少核时」，再决定谁有资格做末端判据。这与 B09 的效率口径是同一件事，两者可合并用。
7. **「事前不可预判」要作为面板的一个正式结论来测，而不是当作失败**。他们系统试了可前瞻获取的因子（大小、埋藏度、口袋亲脂性、亲和力高低）并公开判定这些因子**不能**预判单次 ABFE 的可信度。→ 我们应当把「能不能事前知道这一枪可信」作为面板的第 4 个问题独立出成绩；预期结论很可能同样是「不能」，而这是一个**有用的阴性结果**：它把资源从「调判据权重」转向「同候选多路独立评价 + 失活对照」。
8. **构象/起点敏感性单独出一格**。他们用 55 例（43 近 / 12 偏，>3 Å）量化出「因起点错误丢 2–5% 活性」。→ 我们同理：每个花钱判据要标注它的起点依赖（结构预测置信度、构象采样起点），并给「因起点错误而漏掉」的量级估计，而不是默认起点正确。

### 不可迁移（为什么不能照搬）

1. **他们的全部阈值是「小分子结合自由能」的阈值**：50 个 λ 窗、5 ns/窗、BAR、r = 0.69–0.77、TPR 94%、RMSE ≈ 2.2 kcal/mol、网格 40×40×40。这些与「某蛋白能否把底物装上 tRNA 并完成催化」没有任何等价关系，**不得**作为我们的判据阈值或闸口，也不得写进我们的成功判据。（本库口径同样禁止把结合类阈值当酶活闸口。）
2. **「ABFE 九靶 86–100% TPR」「Boltz-2 81%」不能换算成我们的任何命中概率或成功率**。它们是 135 活性/180 诱饵、1% 先验、无湿实验的回顾投影数字，标签是「结合/不结合」的二值标签；我们的结局标签是**多步化学事件 + 竞争副产物**，至今连一条被产物化学确认的天然参照酶都没有。引用时只许引用其**面板结构与统计口径**，不许引用其成绩值。
3. **他们的阳性是「可定义的二值结合」，我们的阳性目前不可定义**。PDBbind/DUD-E 之所以能建，是因为「有实验 Kd」和「已知活性」两套现成标签。我们没有等价标签 → 面板第一步不是选判据，而是**先建立可核验的结局标注**（哪怕来自文献报道级证据），并允许 UNKNOWN / METHOD_FAIL 两态。
4. **金属蛋白被整体排除（285 个）**，而我们要处理的体系里含金属中心/金属依赖催化的情形不少；本文的力场结论对这些体系**不作承诺**，不能拿来支持「MD 判据在我们这类活性位点上可靠」。
5. **QM 在他们的流程里只做配体电荷参数化**，从不参与打分；因此这篇**不能**被引用为「QM/xTB 类方法可作筛选判据」的证据，正反都不行——它没有测过。
6. **他们没有前瞻实验**（第 7 节作者自陈第 3 条），所以这篇不能用来论证「我们的盲测只要面板够大就能替代湿实验」；面板改善的是**期望命中率**，不是证据等级。
7. **「Boltz-2 预筛 + ABFE 收尾」这个具体配方不可照搬**：它依赖「便宜 AI 模型在大库上有可用排序」这一条已被本文限定在 docking 语境的结论。我们的候选生成端（结构预测/检索/生成模型）没有等价的、被双轴检验过的便宜排序器，照搬等于把未知判据放主闸口。

### 一句话的可执行版

把这篇的骨架抄成我们的面板规格：**双轴出题（定量/判别）+ 性质配对的阴性集 + 每格随机基线概率 + 分层（家族 × 化学事件 × 判据，含一个已知全崩层）+ 单价并列的三档成本阶梯 + 独立一格的「事前可预判性」测试（预期为否）+ 起点敏感性一格**；七个格子全部有成绩之前，任何判据不得进入漏斗，任何成绩不得写成「我们的方法有效」。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K34_PMC13213910_text.txt

- **本卡逐字比对用的唯一底稿**：`data/literature_cards/fulltext/K34_PMC13213910_text.txt`（82,428 B，SHA-256 前缀 `78fe6b20f6f710e2…`；Europe PMC fullTextXML 去标签纯文本，按核验器同一 `norm()` 归一后 82,282 字符，全文单行）。同目录另有 XML 原件 `K34_PMC13213910_fullTextXML.xml`（192,462 B，SHA-256 前缀 `be8d9e75d5a8af3b…`），门禁显式排除 `.xml`，故不参与比对，仅作取回凭据。
- **为什么必须声明这一份**：同一篇可能有 Europe PMC 与 NCBI 两套抽取版本，句中夹的参考文献编号位置不同；本卡所有引句照上面这份纯文本逐字复制。该纯文本里有 20 处私有区字符 U+E5F8（标签剥离后残留的连接符）与 4 处软连字符，跨这些字符的句子**一律不引**，改拆成同句内的两段或只取不含该字符的半句（例如端态法/ML 换位子、DUD-E 靶列表两处）。
- **对照底稿**：`sources/cost-benchmarks.md:67`（§二 计算成本表的 FEP/ABFE 行）与 `sources/cost-benchmarks.md:127-133`（§3.6 结合自由能与实验相关性）。本卡相对底稿补齐：基准集的完整构建漏斗（1,286→1,139→632）、分层体检数字（124 超家族 / 379 簇 / 263 单例）、λ 窗协议全部参数、超几何检验与投影的具体 N/K/n、逐靶 TPR 塌陷面、构象敏感性 55/43/12 链条、以及「事前因子不能预判单次 ABFE 可信度」的原文判定句。
- **CSV 字段映射**：本文 §3 ↔ `候选生成方法/计算筛选判据/阈值数字`；§4 ↔ `候选数递减/实验命中率/成本/统计量引用`；§5–§6 ↔ `在方法演进链的位置`；§8 ↔ `计算筛选判据` 的使用边界（不许跨域搬阈值）。CSV 原行的 `md_used=是-主筛选器` 与本卡一致；`qm_used=否` 本卡补了限定（QM 只做配体电荷参数化）。
- **未取到的部分（诚实边界）**：Supplementary Figures S1–S5、Tables S1–S4、Data Sets 1–7 全部未取回。因此本卡第 5.2/7.3 条涉及「唯一九靶全稳」「失败点不重合」的具体逐靶矩阵，属于**作者断言**，本卡无法自行复核；第 4 节凡标注「正文举例」的数字，均来自正文文字而非表格。
- **本卡自检**：`scripts/verify_literature_cards.py --only K34 --no-report`（输入：本目录卡片 + `fulltext/` + `sources_map.json`；参数：`--only K34 --no-report`，不写 selfcheck.txt/rollout_status.tsv 以免覆盖并行代理产物）。该门禁把卡内被直双引号包住、纯英文、≥20 字符且 ≥12 个字母的片段当作逐字引句，在声明底稿里逐字查找，任一条不命中即 FAIL 且退出码 1。本轮结果 **96/96 逐字引句全部命中**，退出码 0；门禁同时统计到 §3 工作流程表 28 行步骤（下限 3）、§2 难点 10 条（下限 2）、十节标题与顺序齐全、`引句底稿` 指向该编号已登记的可读底稿。
- **反向自测（证明这道门真能判红，不是自我声明）**：在同一张卡的内存副本上做三处数字篡改，每次只改一处、复跑门禁的引句提取与逐字查找逻辑（不写任何生产文件）——① 约束增益句里 `from 0.73 to 0.77` 改成 `from 0.74 to 0.77`；② 基准漏斗句 `reduced the data set to 1,286` 改成 `1,386`；③ 推荐句 `true positive rates between 86% and 100%` 改成 `between 76% and 100%`。三处**均被检出**（各产生 1 条 miss，门禁判定为 FAIL），说明「引句造假会被机器抓到」是可执行的事实。
- **写卡过程中的失败与修正**：首轮提取时曾打算跨引文编号连句（原文两处句中夹着剥离后的参考文献标记与私有区字符 U+E5F8），改为按原样分段引用；含 `*`（如力场层级 HF/6-31G 后紧跟星号）的句子一律不引，因为门禁的清洗步骤会剥掉星号导致逐字不命中。

<!--CSV回填
work_type=benchmark（回顾性大规模基准，无新增湿实验）
target=小分子 docking 虚拟筛选漏斗末端的结合自由能预测；定量轴 PDBbind 632 复合物（206 蛋白/606 配体），判别轴 DUD-E 9-10 靶 315 复合物（135 活性+180 诱饵）
backbone_generation=不生成新候选；起点构象来自 AutoDock Vina 1.2.0（网格 40×40×40 点、间距 0.375 Å、exhaustiveness 8），PDBbind 侧用晶体结构，DUD-E 侧用对接 pose；诱饵/活性由 Glide flexible 打分排序选出
computational_filters=alchemical ABFE（GROMACS 标准协议 + BAR）；端态 MM/PBSA 与 MM/GBSA（无熵修正 / NMA / 相互作用熵 IE 三模式）；七个 ML 打分器 GNINA、K DEEP、OnionNet-2、TopologyNet、Yuel、RF-Score-VS、Boltz-2；评价指标为 Pearson/Spearman 相关 + 逐靶 TPR + 超几何随机概率 + 投影到实际筛选场景的可回收活性数
thresholds=ABFE 协议：每条耦合路线 25 个 λ 窗（共 50 窗）、每窗 5 ns、λ 步长 0.1（至 0.8）后 0.05、前 12 窗只开 vdW、软核 sc-alpha 0.5/sc-power 1/sc-sigma 0.3、ΔH/Δλ 每 100 fs 采样、BAR 汇总；定标结论 5 ns 优于 1 ns 而 10/15 ns 增益不划算；取向约束增益 r 0.73→0.77 但成本最多 +30%，故弃用；端态法取末 1 ns 共 1000 帧、NMA 仅 20 帧；基准构建过滤：MW 250-600 Da、cLogP 1-5、HBD≤5、HBA≤10、可旋转键<14、无磷、可离子化基团受限（Results 称排除多于一个、Methods 称不超过两个，原文两处口径不一致）、至少一环、Tanimoto 0.5 聚类；统计判据：每靶 N_tot=35/N_pos=15/n=7 的超几何精确概率 + 合并集 307/135/63 + 投影场景 1000/10/100 与主筛阳性率先验约 1%；构象偏差判据 RMSD>3 Å、能量差阈值 2 kcal/mol。注意：全文没有「通过/淘汰」型闸口阈值，只有评价口径与协议参数
md_used=是（判据本体：ABFE 与两种端态法全部建立在 5 ns MD 轨迹上，不是事后机理解释）
qm_used=否（QM 仅用于配体 RESP 电荷拟合，HF/6-31G* 层级 Gaussian 16，属力场参数化，不参与任何打分或排序）
experimental_methods=无湿实验；使用已有实验标签：PDBbind 的实验 Kd/Ki 与 X-ray 结构、DUD-E 的既有活性/诱饵标注（55/135 活性配体有晶体结构用于构象敏感性回顾）；CACHE Challenge 1/2 的公开盲测命中率（7/23、5/25 出货）用作真实阳性率先验
pipeline_counts=PDBbind 侧：5316 复合物/4284 唯一配体 → 物化与结构过滤后 1286 → 自动制备失败 147 个后 1139 → 剔除 285 金属蛋白 → MD 运行错误再剔 → 最终 632 复合物/606 配体/206 蛋白；DUD-E 侧：每靶随机 200 个对接 → 前 20 为诱饵、前 15 为活性 → 共 315 复合物；定标子集 77；λ 窗定标 1/5/10/15 ns 四档；构象敏感性子集 55（43 接近晶体、12 偏差 >3 Å）
hit_rate=定量轴：ABFE 全集 Pearson 0.69/Spearman 0.68（77 pilot 0.73/0.70，加取向约束 0.77），靶内 Pearson 0.44-0.75、Spearman 0.19-0.74，端态法无满意表现且熵修正后更差（MM/GBSA 仅 2 靶 r>0.5、MM/PBSA 3 靶），Boltz-2 0.58、GNINA 0.34、RF-Score-VS 0.30；判别轴 TPR：ABFE 94%（逐靶 86-100%）、Boltz-2 81%、RF-Score-VS 79%、MM/PBSA 83%、MM/GBSA 70%、GNINA 38%、其余早期 ML 20-38%（约随机）；投影到 N=1000/pos=10/n=100 场景：ABFE、MM/PBSA、Boltz-2、RF-Score-VS 可回收 10/10（ABFE 仅需点 17 个阳性），MM/GBSA 8/10（HMDH 靶 14% 低于随机），GNINA 5/10，早期 ML 1-3/10
best_metric=未记录（本文为判据基准研究，不报告单化合物最优 Kd/活性；只报误差量级：top/bottom 50% 配体 RMSE 2.30 与 2.16 kcal/mol）
cost_or_stat_note=ABFE 约 2 h/配体（专用 GPU，Hellbender 集群）；端态法同约 2 h 但算力资源少约 50 倍、节点数少一个数量级（可大规模并行）；GNINA/Boltz-2 分钟级；常规 ML 单次前向亚秒级；加取向约束需额外 λ 窗、成本最多上升 30%（换 r 0.73→0.77）；结论按成本把判据分档排序；因 docking pose 错误预计损失 2-5% 真活性
role_in_timeline=把「漏斗末端该用哪个判据」从经验断言变成可测问题：首次同时建定量轴与判别轴双基准，证明两类判据名次会随口径互换（端态法能排序不能定量、多数 ML 能拟合不能判别），并给出随机基线加超几何投影的统计语言与「便宜 AI 主筛（Boltz-2）→ 少量候选上 alchemical ABFE」的分阶段建议；同时留下一条硬负面结论——没有任何可前瞻获取的性质因子能预判某一次 ABFE 计算是否可信
source_pointer=data/literature_cards/fulltext/K34_PMC13213910_text.txt（SHA 78fe6b20f6f710e2…，本卡引句底稿）；sources/cost-benchmarks.md:67 与 §3.6（:127-133）；DOI 10.1021/acs.jcim.6c00942；代码 https://github.com/kireevlab/Last-mile-physics-based-AI-for-VS
CSV回填-->
