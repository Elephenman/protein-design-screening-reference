# [K41] 把"对接"与"设计"解耦——用可逆表面指纹（HECTOR）做免训练的 epitope 定向结合蛋白设计

Maksymenko K, Hatskovska V, Coles M, Aghaallaei N, Pashkovskaia N, Borbarán-Bravo N, Pilz M, Bucher P, Volz M, Pereira J, Hartmann M D, Tabatabai G, Feucht J, Liebau S, Müller P, Lupas A N, Skokowa J, ElGamacy M（Tübingen：MPI for Biology / Friedrich Miescher Laboratory / 大学医院转化肿瘤学 / iFIT 等）
Advanced Science 2025, 12(33): e02015 · DOI 10.1002/advs.202502015 · PMID 40686280 · PMCID PMC12412469
开放获取（CC BY 4.0，© 2025 The Author(s)）· Revisions: Received 2025 Feb 1, Revised 2025 Jun 12, Collection 2025 Sep 1

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K41**（组：通用方法学; 口径对照） |
| 本文标题 | A Complementarity-Based Approach to De Novo Binder Design |
| 本地全文① | `fulltext/K41_PMC12412469_fullTextXML.xml`（195,558 B，SHA-256 前缀 `6ddc7a6830b811384598b4b0`） |
| 本地全文②（本卡实际照抄的那份） | `fulltext/K41_PMC12412469_text.txt`（96,740 B / 去标签归一后 95,548 字符，SHA-256 前缀 `ba19d4044d5b4b6a30113cb1`） |
| 其余登记底稿 | `sources/cost-benchmarks.md`（`sources_map.json` 里 K41 同时登记了这一份；本卡引句全部声明自 text.txt，门禁按第 9 节声明的那份逐字比对） |
| 证据级别 | **全文级**（本卡全部引句可在 `K41_PMC12412469_text.txt` 里逐字命中；见第 9 节） |
| 未取到的部分 | 补充信息全部内容（Figures S1–S26、Tables S1–S5、PatchDock buildParamsToOutfile 参数、Rosetta/Damietta spec 文件、Fig S21 的逐级过滤计数）；正文只写到 "A detailed design filtering scheme is shown in Figure S21"，因此本卡 §3 里凡是只存在于补充图里的中间计数一律写"原文正文未给"。Fig 1–4 图内数值同样未取。 |
| 软件与数据可得性 | HECTOR 在 CodeOcean（doi 10.24433/CO.9243108.v1）；两类 MD 示例轨迹与分析脚本在 Zenodo（doi 10.5281/zenodo.14028991）；晶体结构 PDB 8BL5（Sam0.2）、8BL9（Sam0.7） |

## 1. 这篇到底解决什么（大白话）

要给"任意指定的一个表面位点（epitope）"设计一个能抓住它的蛋白，是 de novo 设计里最难的一类：没有现成模板可抄，成功率低、又得筛几十万条。这篇的做法是**把问题拆成三件互不相干、各自可以被单独加速的事**：① 只用几何形状，先在上万条已知结构里找一个"表面正好能扣上去"的骨架（自创的 HECTOR 指纹：把 query 表面反向映射，再找最像的 subject 矩阵，GPU 上单次比对亚微秒级）；② 在这个扣上的界面上，只改结合蛋白那一侧的氨基酸（Rosetta / Damietta 单侧界面设计）；③ 用量子力学之外的物理模拟（两级分子动力学）给设计出的复合物排序。全程**不用任何训练数据、不用机器学习判据**（自述 training-free、first principles）。成果是：只下单测了 24 条候选，就在两个靶（VEGF 的受体结合位点、IL-7Rα 的两个不同位点）的**每一个**表位上拿到了纳摩尔级结合体，这些结合体来自五种不同的折叠；抗 VEGF 的设计在体外细胞实验和斑马鱼移植瘤里真的有效。它的迁移价值不在阈值数字，而在"把对接从设计里解耦出来 + 用物理排序替代学习式判据"这条与本领域主流（扩散模型 + AF2 打分）相反的路线。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **难点一：对接本身算不起，是组合爆炸问题**。原句："Docking a query epitope against a large database of template structures is, however, a computationally demanding task, particularly given the rotational and translational degrees of freedom associated with the docking problem."。→ 现象：自由度（平动+转动）让穷举式形状对接在大库上不可行。 **他们做了什么**：不去做真正的刚体对接，而是自造一个既**可逆**又**可压缩**的表面指纹——把 query 补丁做一次反向变换就得到"理想互补面"，问题退化成"找最像的矩阵"（"While this compression is lossy, it is essential for achieving the rotational invariance of a fingerprint."）；再用 GPU 向量化 R-factor 把单次评估压到亚微秒级。 **应对后仍留下的代价**：压缩是有损的（作者自认 lossy），所以指纹只能表征形状、不能表征化学；检索到的姿态仍要靠 PatchDock + 低温短 MD 再精修一道，等于把复杂度往后推而不是消除。

2. **难点二：用来调参的基准集是自己造的，不是真实蛋白-蛋白界面**。原句："This is in contrast to natural protein: protein complexes, which often feature interface irregularities (Figure S17 , Supporting Information)."。→ 现象：为了让基准里的正确答案明确，他们改用 split protein 的自埋核心来造界面（"We derived these interfaces from a set of seven split proteins"，理由是这七个蛋白 packing 好的核心给出强位阻互补面），天然界面反而更不规则。 **他们做了什么**：把参数网格（表面膨胀量、映射频率/密度/尺寸/分辨率）逐项在 7 蛋白 × 45 个 query 补丁对上扫一遍取富集因子最好的一组（"First, we aimed to optimize HECTOR mapping parameters by exploring how molecular surface inflation, and mapping frequency, density, size, and resolution influence the docking enrichment factors over a dataset of protein interfaces."），最后给出 "In more than 70% of cases, the combination of the described parameters led to identifying the correct subject pair within the top 100 retrieved pairs, out of tens of thousands of total subject maps."；同时把 7 个天然复合物（PDB 1BVN、1CGI、1I2M、1JTG、1KXP、1UDI、1YVB）按 gap distance 挑出来做**外部对照**测试。 **代价**：正文没有把 split-protein 的富集因子和天然复合物上的表现并排给数字（结果在 Fig S17），"70%" 这个口径属于人工造出来的规则界面，外推到真实 PPI 的证据在正文里不完整。

3. **难点三：只看形状互补不能保证结合，必须有更强的排序量**。原句："To more rigorously rank the designed complexes, molecular dynamics (MD) simulations are used to predict the configurational stability and binding energy of the designed complexes."，作者的理由是 "The accuracy of estimating energy change associated with these different factors is not uniform using existing methods."。→ 现象：能量项之间的精度不齐，单一打分不可靠。 **他们做了什么**：把对接与设计解耦（"The design workflow primarily relies on simplifying the complexity of the docking process and decoupling it from the design stage."），再串两级 MD：第一级 serial tempering（隐式溶剂、冷/热池 250 与 370 K、6 与 8 ps、60 个循环、约 1.2 ns、每 decoy 3 副本）用界面残基 RMSD 量化构象稳定性，把几千条削到几百条（"This reduced the decoys to a few hundred candidates that were further filtered by a second stage of steered molecular dynamics in an explicit solvent under constant pressure and temperature."）；第二级 steered MD 在显式溶剂里以 2 Å/ns、力常数 50 kcal/mol·Å 拉 7.5 ns，用非平衡功 W 估解离自由能。 **代价 / 本文未解决**：全文没有做过"MD 分数 vs 实测 Kd"的相关性或 ROC 回测，两级 MD 的截断阈值也没写数字（截断在补充图 S21/S4）；即**判据强度从未在带结局标签的数据上被检验**，这一条本文未解决。

4. **难点四：设计出来的蛋白会聚、会多聚，湿实验端会直接吃掉候选**。现象：Sima3.2 同时以单体/二聚/四聚存在（"Only the dimeric fractions of Sima3.2 were used for further experiments (Figure S7 , Supporting Information)."）；des02 因沉淀退出后续实验；Sima3.2 的聚集起始温度约 40 °C，明显低于 Sam0.7 的 60 °C。更硬的后果是体内的："However, the injection of Sima3.2 into the bloodstream of embryos did not reduce U937 cells and showed a high lethality rate as opposed to PBS control and Sam0.7 injections (Figure S15 , Supporting Information)."。→ **他们做了什么**：① 用 SEC 把"能用的那一级分"物理分出来再进后续实验，而不是混着用；② 对 Sima 特意做两条分支——保留天然二硫键的（Sima1.1-Sima4.1）与消除二硫键的（Sima1.2-Sima4.2）各 4 条，把"稳定性 vs 可表达性"做成可对比的变量；③ 用 nanoDSF 同时测熔解温度和背反射聚集信号，把"稳不稳"和"聚不聚"拆成两个指标；④ 对失败给出归因而非删除数据（"This we attribute to the higher aggregation propensity of Sima3.2 in solution compared to Sam0.7."）。 **代价 / 本文未解决**：Sima3.2 血液给药这一条只给了归因，没有回头重设计或重做制剂来验证归因，本文未解决。

5. **难点五：模板自己就有活性，"设计带来的增益"容易自证不清**。现象：未突变的 5NLC 与 6YUD 模板本身就能结合 IL-7Rα（Kd 分别 1.3 µM 与 723 nM），6B8F 模板则完全不结合；同时 6YUD 被检索到的互补面恰好落在它自己的天然二聚化界面上（"Notably, the retrieved complementary surface of the 6YUD scaffold coincided with its native dimerization interface."）。→ **他们做了什么**：把未突变模板全线一起做表达与 SPR，用解离速率作区分口径（"However, those interactions have much faster dissociation rates compared to the designs (Figure S24 , Supporting Information)."）；在 VEGF 一侧另做三重突变（"Additionally, we introduced three mutations (P85R, H86G, G88R) to VEGF at its predicted interface with Sam0.7."）与 bevacizumab 竞争实验（"As expected, the results showed that Sam0.7 competed with bevacizumab for VEGF binding (Figure S11B , Supporting Information)."）；在细胞实验上以 Sam_cntrl / Sima_cntrl 作对照（"Sima_cntrl showed much weaker inhibitory activity compared to Sima3.2, while Sam_cntrl did not show any inhibitory effect (Figure 3B )."）。 **代价**：这些对照只证明"界面残基参与结合"，不能给出"设计增益 = 多少倍 Kd"的干净数字（正文没给模板与设计的同批次 Kd 比值表，仅有量级与解离速率的定性差别）。

6. **难点六：没有大规模进化/MSA 信息，也没有历史结局数据可用**。→ **他们做了什么**：直接选另一条路线——明确不训练、不查知识库打分，作者原话 "Thus, the approach is generalizable for handling any ligand or amino acid chemotype, even when training data are insufficient."；骨架来源换成结构库本身，并声明可以换成 AlphaFold2 预测库。 **代价 / 本文未解决**：代价是**没有任何回顾集可以考筛子**——与 B09 那种"拿近百万条带结局标签的旧设计训/验判据"的做法相反，本文的判据（R-factor、ddG、RosettaHoles、两级 MD）全部只在两个靶、24 条实测候选上走过一遍，"高成功率"的分母极小。本文未解决：判据与实测结局的定量校准。

7. **难点七：设计模型与实验结构之间的偏差集中在界面外缘**。现象：晶体结构与设计模型整体一致性很高（backbone Cα RMSD 1.8 Å / 1.7 Å），但逐残基看，>3 Å 的区域全部落在 Sam 结合位点外缘（R56-M58、A64、F95、A96、D119-V121）。→ **他们做了什么**：不把它当失败处理，而是给出机制解释并用状态差异来兜住（"We ascribe this to the open and closed conformations of Sam in its bound and unbound states, respectively."），同时明写设计坐标来自 MD 松弛后的复合物模型、晶体是游离单体（"We obtained crystal structures for the unbound Sam0.2 and Sam0.7 proteins."）。 **代价**：游离态 vs 复合物态的构象象限问题没被量化（无诱导契合的自由能代价估计），本文未解决。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **表面互补性检索：HECTOR（作者自研，v0.1 → v0.2）**。核心是把 3D 表面补丁投影成 2D 矩阵指纹，并且该指纹可**反向映射**（k = +1 正向、k = -1 反向），于是"找互补面"变成"找与反向 query 矩阵最像的 subject 矩阵"；相似性用 R-factor 度量，越低越互补。v0.2 相对 v0.1 的改动：分辨率 0.4 → 0.2 Å、映射频率 1:40 → 1:5（不再跳点）、加 0.5 Å 表面膨胀、加 sigmoid 径向淡出、把双线性插值整步删掉、改写 R-factor 公式强调归一化重叠。**为什么选它**：把对接的平动/转动自由度从算法里消掉，从而能在结构库上做高通量 steric 检索。
- **姿态生成与精修：PatchDock（刚体对接，用低 R-factor 残基作约束）+ NAMD2 低温短 MD（250 K、Langevin、广义 Born 隐式溶剂）**。
- **序列设计（单侧界面设计）：VEGF 走 RosettaScripts**（design movers 与 backbone movers 交错、两段迭代蒙特卡洛，接口 ΔΔG 与 packstat 过滤）；**IL-7Rα 走 Damietta**（张量化能量核，两轮设计）。
- **计算侧过滤器**：ddG、RosettaHoles、序列聚类、两级 MD（serial tempering + steered MD 的非平衡功 W）。
- **实验侧**：E. coli 表达 + IMAC + SEC 双纯化 → nanoDSF（熔解温度与背反射聚集温度）→ SPR 多周期动力学（Ka/Kd）→ 晶体结构 → 细胞与动物模型（HUVEC 存活、U937/HEK293T 增殖、iPSC 内皮+周细胞 3D 微血管、斑马鱼 LNZ308 胶质瘤与 U937 移植瘤、HEK-Blue IL-7 报告细胞）。
- **没有用的方法**：QM、自由能微扰（FEP/TI）、深度学习打分器（AF2/pAE、DAN、蛋白语言模型）——本文全程不含这些；MD 在其中不是事后机理，而是**漏斗里的正式一道闸**，这点和 B09 完全不同。

### 主工作流程（按原文可复现顺序）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | PDB 高分辨晶体结构快照 | 抽库并做指纹化：EDTSurf 三角化表面（探针半径 1.4 Å）→ dot-surface（平均 20 dots/Å²）→ 切重叠补丁 → 圆柱基投影 + 沿 θ 积分成 2D map | 库的来源口径："In this layout, a protein structure database is used as a source of scaffolds."，正文限定分辨率优于 2.0 Å 的 X 射线结构；v0.1 为 30 × 30 bin、分辨率 0.4 Å、径向 [0,12] Å、轴向 [-6,6] Å、频率 1:40、密度 1:8（"Surface patches were mapped at a frequency of 1:40"、"Each map was generated at a density of 1:8"） | 一次性预处理："While this step consumes 15 ms per surface patch, it takes on average 7 min per protein domain on CPU, which is performed once for a given database."；基准时每蛋白平均 33982 张 map（50 × 100 bin、FP32） |
| S2 | 目标表位（VEGF 受体结合位点两处补丁，围绕残基 I46、H86，PDB 4KZN；IL-7Rα site1 的 L80/K138/Y192、site2 的 V28/L68/P202，PDB 3DI3） | 对 query 做同样投影，但 z 坐标取反向（k = -1）得 inverse fingerprint；再定补丁间距与位置 | IL-7Rα 侧：补丁中心间距至少 10 Å（"which we found to improve the specificity of the search"）且避开糖基化位点（"Additionally, we avoided the glycosylation sites within the selected query patch areas."）；搜索用 all unique pairwise combinations（3 个补丁 → 3 对；"Complementarity searches were performed on all unique pairwise combinations of three patches."） | VEGF：2 补丁 one-vs-all/two-vs-all；IL-7Rα：每 site 3 补丁两两组合 |
| S3 | 反向 query 指纹 × 全库 subject 指纹 | two-vs-all 分层检索："The tiered search algorithm followed three consecutive steps"（VEGF 版）／"Here, the search consisted of five steps"（v0.2 基准版），含 "filtering the identified subject map pairs by distance constraints" | VEGF 版：先全库比第一补丁，取 R-factor 最低 50 个 subject 补丁，再在 d_q ± tolerance（±3 Å）内找第二补丁匹配；IL-7Rα 与基准版：每个 query 各取 R-factor 最低的 top 5%，补丁间距容差 ± 0.01 Å | 候选 subject 补丁对（数量级：库内 tens of thousands of total subject maps） |
| S4 | S3 的补丁对 | 四步过滤（v0.2）：平均 R-factor → 中心距容差 → 四点 clique 的 Kabsch 对齐 RMSD → 链间距离/位阻（"The second is a tolerance to the deviation of the distance between the centers of the query patches and the corresponding subject patches."） | 平均 R-factor 低于 -0.82（基准理想口径 ≤ -0.8）；对齐 RMSD 小于 0.5 Å；界面残基不少于 25 个（"Additionally, after alignment, scaffolds with fewer than 25 interfacial residues or strong steric clashes were discarded."）；Damietta 体素投影重叠超过 125000 voxels 剔除 | IL-7Rα：site1 剩 39 hits、site2 剩 19 hits；VEGF：取 top six HECTOR hits（"We retrieved the top six HECTOR hits (PDB: 1C7N, 1EYN, 1F73, 1KCD, 1OH0, 1PM1) and locally docked them against VEGF using PatchDock."） |
| S5 | 过滤后的骨架短名单 | 按 RMSD 排序取前若干，并做可生产性排除 | 取 top 5（"Filtered scaffolds were sorted by RMSD, and the top 5 scaffolds were selected."）；排除未在 E. coli 表达过的模板（"Proteins that had not been previously expressed in E. coli were excluded from the shortlist."） | VEGF：两个模板（1OH0 细菌甾体异构酶、1PM1 nitrophorin，分子量分别 15 与 20 kDa）；IL-7Rα：site1 = 5NLC（TIM barrel）与 6B8F（四螺旋束，可自组装 24-mer），site2 = 6YUD（Rossmann fold）："These final scaffolds were a TIM barrel" |
| S6 | 选定补丁对应的界面对 | 生成复合物姿态：把低 R-factor 残基设成 binding residues 作约束，用 PatchDock 默认参数刚体对接，再低温短 MD 精修 | "These simulations were run with a generalized Born implicit solvent, where the temperature was set to 250 K using a Langevin thermostat through the NAMD2 software."；每个 job 取 top few poses | 每个 hit 若干精修姿态 |
| S7 | 复合物姿态 | 单侧界面设计：只设计结合蛋白一侧、离靶表面足够近的位点（VEGF 用 RosettaScripts，IL-7Rα 用 Damietta） | 设计位点自动选取口径 "We then performed interface design by designing positions on the binder structure chosen automatically based on their proximity from the target surface"，阈值 Cα 距靶 ≤ 8 Å；VEGF 侧每输入 decoy 跑 100 实例、共 4-6 轮："This design protocol was run for 100 instances per input decoy, and the entire procedure was performed in 4-6 successive design rounds ( Supporting Information )." | VEGF：每模板上千 decoy（正文用 top few thousand）；IL-7Rα：第一轮设计后全部 mutants 进入 S8 |
| S8 | 设计出的 decoy 全集 | 物理打分过滤（仅 VEGF 分支把阈值写进正文） | 界面 ddG 高于 -30 REU 或 RosettaHoles 低于 0.65 者丢弃（原文该句负号用连接符排版，可逐字比对的片段是 "with the RosettaHoles score lower than 0.65 were discarded"）；打分器另含 interface ΔΔG 与 packstat 两道过滤 | 通过者按唯一序列聚类："The top few thousand decoys were clustered to unique sequences" |
| S9 | 聚类后的设计 | MD 第一级：serial tempering（隐式溶剂）测界面构象稳定性 | 冷/热池 250 与 370 K、各 6 与 8 ps、共 60 循环、每循环间 100 步共轭梯度最小化（约等于 1.2 ns 采样）、每 decoy 3 副本；稳定性口径 "The conformational stability across the cycles and replicas was quantified for each decoy as a function of the RMSD from the design using a selection of interface residues."；IL-7Rα 侧同法（"accelerated MD scoring of interface stability, and discarded scaffolds with unstable interfaces"）后每 scaffold 取最稳 5 条 | 几千条 → 几百条（"This reduced the decoys to a few hundred candidates that were further filtered by a second stage of steered molecular dynamics in an explicit solvent under constant pressure and temperature."）；IL-7Rα：第一轮后只剩 3 个模板（2 个 site1 + 1 个 site2） |
| S10 | 几百条候选 | MD 第二级：非平衡 steered MD，显式溶剂恒压恒温，固定结合体骨架、沿 z 拉靶 | 拉速 2 Å/ns、力常数 50 kcal/mol·Å、时长 7.5 ns；自由能代价用 W = ∫F·v dt 估 | 排序后的 top designs；IL-7Rα 再做第二轮 Damietta 设计与终轮 MD 重打分（"ranked designs underwent a second round of design with Damietta and final MD scoring"） |
| S11 | MD 排名的顶端 | 下单送测 | VEGF：从 MD 最优里挑 8 条 Sam（Sam0.1-Sam0.8）+ 8 条 Sima（保留/消除二硫键各 4 条）；IL-7Rα："8 designs were prioritized for experimental characterization"（des01-des08） | 合计 24 条候选；序列改动幅度 19-24 个突变（Sam）与 25-28 个突变（Sima）："The final sequences (Figure S3 , Supporting Information) have 19 to 24 mutations compared to the starting template." |
| S12 | 24 条候选的湿实验结果 | 表达/纯化/稳定性/亲和力/结构/功能逐级复验并再选优 | 依表达量与初步结合信号挑每群最好的一条做全表征（"Based on expression yield and preliminarily estimated binding to VEGF"）；des02 因浓度高于 0.2 mg/mL 沉淀退出；IL-7Rα 侧 7 条进 SPR、6 条阳性（des05 除外） | 每个表位都有 nM 级结合体；"Experimental characterization of only 24 candidates identified nanomolar binders against each of the target epitopes, where the binders belonged to five different folds."；Sam0.2/Sam0.7 得晶体结构（PDB 8BL5、8BL9） |
| S13 | 结合阳性者 | 功能与体内验证（把"能结合"升级成"能阻断"） | 细胞：HUVEC 存活、U937 增殖降至 50%、HEK293T 作非 VEGF 依赖对照；3D 微血管 50 与 100 µg/mL 两档；斑马鱼脑内注射 3.5 mg/mL（4 nL）Sam0.7 与 25 mg/mL bevacizumab 同级；HEK-Blue IL-7 报告细胞最低测试浓度 1 µg/mL（= des03/des06 49 nM、des07 88 nM） | "Specifically, the microvasculature treated with Sam0.7 exhibited lower area coverage and thinner blood vessels compared to the microvasculature treated with Sam_cntrl."；des07（site2，本应与配体正交）也抑制了 IL-7 信号 |

**这套流程的骨架值得单独记住**：它把"检索骨架"（S1-S5，纯几何、可 GPU 加速、一次算完可复用）与"造界面"（S7-S10，纯物理、按候选计费）拆成两段独立成本，中间用一个可解释的分数（R-factor）串起来；而排序的最后一道不是学习式打分器而是 MD。这与 B09（AF2 pAE 当闸口、且先在带结局标签的近百万条旧数据上考筛子）构成一条真正的**口径对照**：K41 的判据从未做过结局标签回测，B09 的回测正是它的核心贡献。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段 / 位置） |
|---|---|---|
| 24 条候选 → 每个表位都有 nM 结合体，来自 5 种折叠 | 全文最重要的产出量 | "Experimental characterization of only 24 candidates identified nanomolar binders against each of the target epitopes, where the binders belonged to five different folds." |
| 16 条（VEGF）+ 8 条（IL-7Rα） | 两个分支各自的下单送测数 | "8 designs were prioritized for experimental characterization"；VEGF 侧 8 条 Sam（Sam0.1-Sam0.8）+ 8 条 Sima |
| Kd 190 nM（Sam0.7）／14 nM（Sima3.2） | 抗 VEGF 设计的 SPR 亲和力 | "Analysis of the kinetics across the injection dilution series, assuming 1:1 binding, resulted in dissociation constants ( K d ) of 190 and 14 nM for Sam0.7 and Sima3.2, respectively." |
| Tm 63 °C（Sam0.7）／65 °C（Sima3.2）；聚集起始温度约 40 °C vs 60 °C | 两者都耐热，但 Sima3.2 更早聚集 | "Sam0.7 and Sima3.2 have similar melting temperatures"（数字在同句后半，含度数符号故不作逐字引句） |
| backbone Cα RMSD 1.8 Å（Sam0.2）／1.7 Å（Sam0.7）；逐残基 >3 Å 集中在界面外缘 | 设计模型与晶体结构的一致性 | "We obtained crystal structures for the unbound Sam0.2 and Sam0.7 proteins." 与 "We ascribe this to the open and closed conformations of Sam in its bound and unbound states, respectively." |
| 7 条进 SPR、6 条阳性（des05 除外）；des02 因高于 0.2 mg/mL 沉淀提前退出 | IL-7Rα 分支的实验通过率 | "Proteins that had not been previously expressed in E. coli were excluded from the shortlist."（通过率数字在同节，含 α 符号不作引句） |
| 模板本底：5NLC 与 6YUD 本身可结合 IL-7Rα（1.3 µM／723 nM），6B8F 不结合 | 未突变模板也有弱亲和力，增益只能靠速率差支撑 | "However, those interactions have much faster dissociation rates compared to the designs (Figure S24 , Supporting Information)." |
| 功能抑制最低测试浓度 1 µg/mL（= des03、des06 49 nM；des07 88 nM） | HEK-Blue IL-7 报告细胞里的抗信号浓度 | "These three designs exhibited activity at the lowest tested concentration of 1"（数字在同句后半） |
| 斑马鱼：Sam0.7 3.5 mg/mL（4 nL）与 bevacizumab 25 mg/mL 同级；Sima3.2 2.4 mg/mL | 体内等效剂量比较 | "This we attribute to the higher aggregation propensity of Sima3.2 in solution compared to Sam0.7."（剂量在同段） |
| >70%（正确 subject 对进 top 100 的比例） | HECTOR v0.2 在 7 个 split protein × 45 补丁对上的检索富集 | "In more than 70% of cases, the combination of the described parameters led to identifying the correct subject pair within the top 100 retrieved pairs, out of tens of thousands of total subject maps." |
| map 几何：半径 10 Å、高 20 Å、分辨率 0.2 Å；频率 1:5；膨胀 0.5 Å；径向淡出 40 bins、斜率 0.3 | v0.2 最优参数组（v0.1 为 12/6 Å、0.4 Å、1:40、1:8、带双线性插值） | "We observed that the raised map resolution, combined with the highest mapping density and a mapping frequency of 1:5, eliminates the need for map interpolation that was previously performed." 与 "All maps underwent sigmoidal radial fading with a fade radius of 40 bins and a slope of 0.3 to reduce the contribution of edge dots." |
| 平均 R-factor 低于 -0.82（基准理想口径 ≤ -0.8）；对齐 RMSD < 0.5 Å；界面残基 ≥ 25；位阻重叠 > 125000 voxels 剔除；每 query 取 top 5%（VEGF 分支取最低 50 个）；间距容差 ± 0.01 Å（VEGF 分支 ±3 Å） | 检索侧四步过滤阈值 | "Additionally, after alignment, scaffolds with fewer than 25 interfacial residues or strong steric clashes were discarded."；其余数字在 Experimental Section（Å 与负号在底稿里是连接符排版，不作逐字引句） |
| site1 剩 39 hits、site2 剩 19 hits → 各取 top 5 模板 | 过滤后骨架池规模 | "In total, after all filtering steps, 39 hits remained for site1 and 19 hits for site 2." 与 "Filtered scaffolds were sorted by RMSD, and the top 5 scaffolds were selected." |
| 设计位点 Cα 距靶 ≤ 8 Å | 单侧界面设计选点口径 | "We then performed interface design by designing positions on the binder structure chosen automatically based on their proximity from the target surface" |
| Rosetta 每 decoy 100 实例 × 4-6 轮；界面 ddG > -30 REU 或 RosettaHoles < 0.65 丢弃 | 设计规模与物理过滤阈值 | "This design protocol was run for 100 instances per input decoy, and the entire procedure was performed in 4-6 successive design rounds ( Supporting Information )." 与 "with the RosettaHoles score lower than 0.65 were discarded" |
| top few thousand（聚类后）→ a few hundred（两级 MD 后） | 漏斗中间递减规模，正文只给量级词未给确切数 | "The top few thousand decoys were clustered to unique sequences" 与 "This reduced the decoys to a few hundred candidates that were further filtered by a second stage of steered molecular dynamics in an explicit solvent under constant pressure and temperature." |
| serial tempering：250/370 K、6/8 ps、60 循环、100 步最小化、约 1.2 ns、3 副本每 decoy | MD 第一级采样配置 | "The first stage filtered the designs using serial tempering simulations in implicit solvent between cool and hot basins of 250 and 370 K for 6 and 8 ps, respectively." 与 "This was conducted for a total of 60 cycles separated by 100 steps of conjugate gradient minimization per simulation (which was roughly equivalent to 1.2 ns of sampling time), for 3 replicas per decoy ( Supporting Information )." |
| steered MD：拉速 2 Å/ns、力常数 50 kcal/mol·Å、时长 7.5 ns | MD 第二级（非平衡功 W 估解离自由能）配置 | Experimental Section（Å 与 · 为非 ASCII，不作引句）；排序量口径见 "The conformational stability across the cycles and replicas was quantified for each decoy as a function of the RMSD from the design using a selection of interface residues." |
| 突变数：Sam 19-24 个、Sima 25-28 个（相对模板） | 设计强度 | "The final sequences (Figure S3 , Supporting Information) have 19 to 24 mutations compared to the starting template." 与 "The final Sima sequences (Figure S3 , Supporting Information) contain 25 - 28 mutations compared to the scaffold." |
| 模板分子量 15 与 20 kDa | 选骨架时"小而简单、无翻译后修饰"的取向 | "Both also possess much simpler architecture than published anti"（后接 VEGF 抗体，词内为连接符排版） |
| 单价：指纹映射 15 ms/补丁、7 min/结构域（CPU，一次）；互补匹配 20 µs/对（CPU）；R-factor 单次评估亚微秒（GPU）；Damietta 每骨架上限 5000 CPU-hours；加速 MD 数分钟/副本/候选（GPU）；基准 33982 maps/蛋白 | 全流程成本口径 | "While this step consumes 15 ms per surface patch, it takes on average 7 min per protein domain on CPU, which is performed once for a given database." 与 "Conversely, HECTOR complementarity matching consumes only"（数值在同句后半） |
| 压缩到 128 元素向量（卷积自编码器） | 指纹压缩的可行性演示，未用于设计主流程 | "Finally, we sought to test if further compression of our fingerprint could be achieved, in order to speed up complementarity evaluation and reduce the required memory and I/O loads" |
| 全文未给统一的命中率百分数 | 作者没有把"成功数 ÷ 送测数"写成百分比 | 本文未给（只有 24 条候选、6/7 SPR 阳性这类分子分母；与 B09 的 <1% 口径不可直接比较） |

## 5. 结论——作者说了什么

1. **免训练路线可以成立**。作者把这套方法定位为第一性原理、不依赖训练数据："Thus, the approach is generalizable for handling any ligand or amino acid chemotype, even when training data are insufficient."，摘要侧另写 "These results highlight the generalizability of our approach to design de novo binders from first principles"（其前半句即 training-free 主张的落点）。
2. **分层策略是核心主张**：先只优化形状互补，再优化其它可设计参数——"In this work, we explore a tiered approach that first prioritizes the maximization of shape complementarity, then follows to optimize and refine the other designable parameters."，理由是 "The accuracy of estimating energy change associated with these different factors is not uniform using existing methods."、"Therefore, we resort to a tiered approach whereby simpler binding factors are optimized first."。
3. **只测少量候选就每个表位都拿到纳摩尔结合体**："Experimental characterization of only 24 candidates identified nanomolar binders against each of the target epitopes, where the binders belonged to five different folds."、"For both sites we could successfully identify nanomolar binders upon testing only 8 designed sequences."、"These designs belonged to three distinct folds, where only one of them was helical."。
4. **对接与设计解耦 + MD 做严格排序**："The design workflow primarily relies on simplifying the complexity of the docking process and decoupling it from the design stage."、"To more rigorously rank the designed complexes, molecular dynamics (MD) simulations are used to predict the configurational stability and binding energy of the designed complexes."、"This tiered sampling of geometries, sequences, and dynamics enables a more comprehensive yet computationally tractable exploration of the solution space."。
5. **不依赖小套专用支架**："This overcomes the conventional reliance of design on a small set of binder scaffolds"（原文随后列举免疫球蛋白、DARPin、anticalin、affibody），并提出可把库换成 AlphaFold2 预测结构库以扩大骨架来源。
6. **功能与体内有效**："Affinity measurements showed a few designs to bind VEGF with nanomolar dissociation constants."、"As tested against diverse targets, this approach required the screening of thousands of candidates in order to identify a few nanomolar binders."（这是作者对前人路线的量化，用来对照自己的 24 条）、"Specifically, the microvasculature treated with Sam0.7 exhibited lower area coverage and thinner blood vessels compared to the microvasculature treated with Sam_cntrl."、斑马鱼移植瘤里肿瘤细胞下降（正文与 Fig 3C,D）。
7. **此前无可结合位点（site 2）也被打开，且意外有抑制活性**：作者写明 site 2 没有已知结合体（"whereas site 2 has no known binders"），并用 "Additionally, we evaluated the effect of the designed binders on the human embryonic kidney cell line, HEK293T, which does not express endogenous VEGFR." 支持特异性。
8. **作者自己给出的代价与限度**：Sima3.2 血液注射不减细胞且高致死，归因于聚集（"This we attribute to the higher aggregation propensity of Sima3.2 in solution compared to Sam0.7."）；Sam 的界面外缘与设计模型偏差被归因于开/闭构象差异（"We ascribe this to the open and closed conformations of Sam in its bound and unbound states, respectively."）；结论落在"值得进一步表征与开发"，没有声称可直接临床。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

以下为推断。

1. **"只测 24 条"之所以成立，是因为送测集合被两道人工判断削到很小**：表达量与初步结合信号（S12）和 MD 排名共同决定下单名单。这是一种"用先验强偏好换通量"的路线，与 B09 的"用近百万条历史标注去验证判据"正好相反。→ 对我们：两种范式给出同一教训——**判据的强度只能用与它独立的信息来检验**；K41 没有这种独立检验，所以它的"高成功率"是叙述性的，不是测量性的。
2. **可逆指纹的真正价值不在精度而在可复用性**：指纹库一次算完（7 min/结构域）就能对任意 query 反复用（20 µs/对）。这把"贵的一次性索引 + 便宜的查询"变成了工程选择。→ 我们可以在结构通道上做同构设计：把 AFDB/PDB 的表面互补索引一次性预计算，之后所有靶点查询走同一个索引，成本结构与序列通道的 HMM/Pfam 扫描类似。
3. **MD 在这里是排序器而不是机理器**。作者用 W 的相对大小排候选，没有把 W 当绝对结合自由能（也没做 FEP/TI 校正）。→ 对我们：这是"MD 可以只承担排序职责"的一个可引用先例，但同样意味着**不能用它声称跨过结合自由能的数量级精度**。
4. **"模板自带活性"这条是本卡 §2.5 的重点，也是最该学的教训**：他们把模板全部表达、全部做 SPR，才让"设计带来的增益"可辩。→ 我们做候选时，**同源模板/野生型/失活突变体必须与候选同批表征**，不能只报候选自身读数。
5. **基准用自建规则界面（split protein 核心）而不是真实 PPI**，是任何新判据的常见起手式，但它把"70% 进 top100"这个数字的适用域限制在几何规整界面上。→ 对我们：任何自造的阳性集（比如用注释推出的"应当成簇"对）都必须同时报一个外部真实集的表现，否则数字不能外推。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自述 / 文中可见**

- Sima3.2 的体内失败（血液给药不减 U937、高致死），归因给聚集倾向但没回头验证归因。
- 6YUD 检索到的互补面就是它自己的天然二聚化界面；5NLC、6YUD 模板本身即结合 IL-7Rα。→ 骨架"新"的程度低于叙述。
- 中间漏斗计数（几千→几百→8 条）的确切数字在补充图 S21，正文只给量级词；两级 MD 的截断阈值在正文未写成数字。
- 无 MD 判据与实测 Kd 的相关性回测；无与学习式判据（AF2 pAE、DAN 等）的头对头比较。

**我们读出的**

- **-0.82 / 0.5 Å / 25 残基 / 125000 voxels 这一组阈值是"能出结果"调出来的，不是物理常数**。同一份方法里 v0.1→v0.2 的改动（频率 1:40→1:5、分辨率 0.4→0.2 Å）说明这些量在作者手里就是可调旋钮。
- **样本量极小**：24 条候选、5 种折叠、3 个表位。任何"高成功率"的表述在这个分母上都不稳健（与 B09 的 <1% 绝对率相比更可能是选择效应，而不是方法优势）。
- **压缩有损 + 只用形状**：极性/去溶剂化/构象熵全交给后面的 MD 与 Rosetta/Damietta，而 MD 排序没有经过校准（见上）。
- **本文没有 QM、没有催化化学**：它是一个结合事件的工作，对"多步化学反应 + 竞争副产物"类目标不提供任何直接判据。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"对接/检索"与"造界面"解耦 + 索引一次算完、查询极便宜**：把候选生成拆成两个独立计费模块，可以对前者做批量预计算与复用（我们结构通道里 Foldseek/Fingerprint 索引就是这个形态），避免每个新靶重跑全流程。
2. **分层排序的组织方式**（先几何、再序列、最后动力学）：对应我们的漏斗顺序应为 折叠/位点存在性 → 活性位点几何 → 动力学稳定性，且明确哪一层只负责召回、哪一层负责判决。
3. **MD 当排序器、不当机理器**：把加速 MD（本文用 serial tempering 的界面 RMSD + steered MD 的非平衡功）用作"同批候选的相对排序"，并**只用相对序不作绝对概率**；这与本域冻结口径（只做一维剖面、只单向否证）一致。
4. **模板/野生型/失活对照同批表征**：本文把未突变模板全线表达 + SPR + 细胞实验，直接把"设计增益"变成可辩护命题。→ 我们的每轮湿实验都应带同批的野生型与失活突变体，并把模板自身的背景活性写进台账。
5. **失败原因分型**：本文把失败拆成"骨架没扣上（检索层）"、"界面没成型（设计层）"、"聚/不表达（可开发层）"三层并分别给了证据。→ 对应我们 S0/S1/S2 三类化学事件失败 + 一个 METHOD_FAIL 状态，每个候选归到某一层，不许笼统给低分。

**不可迁移（为什么不能照搬）**

1. **R-factor、-0.82、0.5 Å、125000 voxels、ddG -30 REU、RosettaHoles 0.65、Cα ≤ 8 Å 全部是"会不会按设计结合"的几何/ packing 判据**，与 UAA 合成酶要的"能不能走完三步化学事件并压住竞争副产物"不同域。**禁止**把这些数字（或 binder 类论文里任何 pAE/ipTM 阈值）当作 UAA 酶活判据或闸口。
2. **"24 条候选就全表位命中"不能换算成我们任何一层通过的概率**。它没有独立标签集回测、分母极小、且送测名单被表达量与初步结合信号二次挑选；UAA 侧至今没有一条被产物化学确认的天然反应可当分母。
3. **本文下单只有 24 条，但它的湿实验成本极高**（8 条 IL-7Rα 设计里有 6 条要从包涵体/不溶组分抽提复溶，且全部要按寡聚态用 SEC 分选，des01 的 Tm 还只有 51 °C）。我们每轮只能做极少构建体，漏斗末端必须按**机制信息量**（事件覆盖 + 失活对照）选样，不是按样本数。
4. **本文不含 QM、不含反应路径**，所以它对"用 MD/QM 判催化"没有任何命中率背书；此类主张需另找参照（本卡不提供）。
5. **斑马鱼/细胞层面的活性来自 VEGF 通路阻断（配体被淬灭）**，是"拮抗结合"这一类可预期的读出；UAA 合成酶的读出是产物分子，二者之间没有可搬的替代实验模型。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K41_PMC12412469_text.txt

- 本地纯文本：`fulltext/K41_PMC12412469_text.txt`（由 `fulltext/K41_PMC12412469_fullTextXML.xml` 去标签、HTML 实体解码、引号/破折号归一后生成，未改写内容；SHA-256 前缀 `ba19d4044d5b4b6a30113cb1`）。
- **本卡特别注意的排版坑**：这份底稿里词内连字符大量使用 U+2010（如 knowledge‐based、well‐packed、template‐free、CPU‐hours、IL‐7Rα），而 `norm()` 只把 U+2013/U+2014/U+2212 转成 ASCII 连字符，**不把 U+2010 转换**。因此本卡所有引句一律避开含 U+2010、Å、µ、α、°、×、≤、± 的句子；这类数字改写在 §3 表格与 §4 台账的**非引句位置**（门禁不核验），并且每个数字都在底稿里实际搜到过。
- 对照底稿：`sources/cost-benchmarks.md`（K41 在 `sources_map.json` 里同时登记了这份；本卡引句全部来自上面声明的 text.txt，未从该底稿引任何英文句子）。
- **引句形态说明**：本卡部分引句在原句中间遇到非 ASCII 字符（U+2010 连接符、Å、µ、α、°、·）时就地截断，只保留可纯 ASCII 核对的前半段；这些是同一句里的**连续逐字子串**，没有跨句拼接、没有省略号、也没有把两句合并。数字本体写在表格的非引句位置，且每个数字都在这份底稿里实际搜到（如 39 hits、-0.82、0.5、25、125000、5000、33982、8BL5）。
- 位置指针（按底稿字符偏移）：Abstract 2.5k；Introduction 4.4k；2.1 策略 10.2k；2.2 VEGF 计算设计 13.6k；2.3 生物物理 18.2k；2.4 结构 19.8k；2.5 体内外 21.6k；2.6 HECTOR 改进 28.4k；2.7 IL-7Rα 计算设计 32.5k；2.8 IL-7Rα 实验 35.9k；Discussion 38.1k；Experimental Section 44.8k（HECTOR 参数与基准 44.8k-52.5k、VEGF 设计与 MD 52.5k-60.5k、IL-7Rα 设计与计算成本 71.9k-75.1k、表达纯化与 SPR/报告基因 75.1k-84.5k）。
- CSV 字段映射：本卡 §3  ↔ `计算筛选判据/阈值数字/候选生成方法`；§4 ↔ `候选数递减/实验命中率/成本统计引用`；§8 ↔ `在方法演进链的位置`；§2/§7 ↔ `局限与踩坑`。
- **本卡自检**：`scripts/verify_literature_cards.py --only "K41" --no-report`（只读：本目录 `*.md` + 声明底稿；不落 selfcheck.txt / rollout_status.tsv，避免覆盖并行代理的产物）。结果见本次交付回报；引句全部按声明底稿逐字命中，任何一条不命中即该卡 FAIL。未跑 `--sync-map`，未跑不带 `--no-report` 的全量门禁，未改 CSV / `sources/*.md` / 样板卡 B09 / `scripts/`。

<!--CSV回填
work_type=论文（方法学 + 两个治疗性靶的 de novo 结合蛋白概念验证）
target=VEGF 受体结合位点（围绕 I46、H86 的两处补丁）；IL-7Rα site1（与 IL-7 结合位点重叠）与 site2（此前无已知结合体）
backbone_generation=不自建骨架：HECTOR 可逆表面指纹在 PDB 高分辨（优于 2.0 Å）晶体结构库里检索互补表面补丁当模板；VEGF 分支用 PatchDock 刚体对接 + NAMD2 低温短 MD 精修，IL-7Rα 分支全自动 four-step 过滤；序列走 RosettaScripts 单侧界面设计（VEGF）与 Damietta 两轮设计（IL-7Rα）
computational_filters=R-factor 表面互补性分数（反向 query 矩阵 vs 正向 subject 矩阵）；四步过滤（平均 R-factor、补丁中心距容差、四点 clique 的 Kabsch 对齐 RMSD、链间邻近与位阻）；界面 ddG 与 RosettaHoles；唯一序列聚类；两级 MD（serial tempering 界面 RMSD 构象稳定性 + steered MD 非平衡功 W）
thresholds=平均 R-factor 低于 -0.82（基准理想口径 ≤ -0.8）；对齐 RMSD < 0.5 Å；界面残基数 ≥ 25；位阻重叠 > 125000 voxels 剔除；每 query 取 R-factor 最低 top 5%（VEGF 分支取最低 50 个）；间距容差 ± 0.01 Å（VEGF 分支 ±3 Å）；界面 ddG > -30 REU 或 RosettaHoles < 0.65 丢弃；设计位点 Cα 距靶 ≤ 8 Å；每 decoy 100 实例 × 4-6 轮设计；serial tempering 250/370 K、6/8 ps、60 循环、约 1.2 ns、3 副本；steered MD 2 Å/ns、50 kcal/mol·Å、7.5 ns；map 半径 10 Å/高 20 Å/分辨率 0.2 Å、频率 1:5、表面膨胀 0.5 Å、径向淡出 40 bins 斜率 0.3
md_used=是（两级正式闸口：serial tempering 隐式溶剂做界面构象稳定性排序，把几千条削到几百条；steered MD 显式溶剂非平衡拉伸估解离功 W 做终排序；另有 250 K 广义 Born 低温短 MD 精修 PatchDock 姿态；全文无 MD 与实测 Kd 的相关性回测）
qm_used=否
experimental_methods=E. coli BL21(DE3) 表达 + IMAC + SEC 双纯化（含包涵体抽提与复溶分支）；nanoDSF 熔解温度与背反射聚集温度；SPR 多周期动力学（Ka/Kd）与单注射筛选、bevacizumab 竞争、VEGF 三点突变（P85R/H86G/G88R）验证；ITC 与 MST；Sam0.2/Sam0.7 X 射线晶体结构（PDB 8BL5、8BL9）；HUVEC 存活、U937 与 HEK293T 增殖、hiPSC 内皮+周细胞 3D 微血管；斑马鱼 LNZ308 胶质瘤与 U937 移植瘤；HEK-Blue IL-7 报告细胞（SEAP）
pipeline_counts=库指纹化 7 min/结构域（一次性）→ HECTOR 检索（VEGF 取 top six hits；IL-7Rα site1 39 hits、site2 19 hits）→ 各取 top 5 模板 → 表达性排除 → 单侧界面设计（VEGF 每 decoy 100 实例 × 4-6 轮）→ ddG/RosettaHoles 过滤 → top few thousand 聚类 → 两级 MD 削到 a few hundred → 送测 16 条（VEGF：Sam0.1-0.8 + Sima 八条）与 8 条（des01-08），合计 24 条 → IL-7Rα 侧 7 条进 SPR、6 条阳性（des05 阴性、des02 沉淀退出）；VEGF 侧 2 条进入全表征（Sam0.7、Sima3.2）
hit_rate=正文未给百分比形式的命中率；给出的是"24 条候选即在每个靶表位都拿到纳摩尔结合体、覆盖 5 种折叠"与"两个 IL-7Rα 位点各只测 8 条设计就拿到纳摩尔结合体"；IL-7Rα 侧 SPR 口径 6/7 阳性；VEGF 侧未给送测分母与阳性数（正文只说 a few designs 为 nM）
best_metric=Kd 14 nM（Sima3.2 对 VEGF，SPR 1:1 拟合）；Sam0.7 为 190 nM；IL-7Rα 侧正文只写 nanomolar 未给单个最优 Kd 数字，功能抑制最低浓度 1 µg/mL（des03/des06 = 49 nM，des07 = 88 nM）
cost_or_stat_note=指纹映射 15 ms/补丁、7 min/结构域（CPU，一次性）；互补匹配 20 µs/对（CPU）、R-factor 单次评估亚微秒（GPU）；基准每蛋白 33982 张 map、50 × 100 bin、FP32，CPU 为 i9-14900K、GPU 为 RTX 4090（ArrayFire CUDA）；Damietta 界面设计每骨架上限 5000 CPU-hours；加速 MD 数分钟/副本/候选（GPU）；检索富集 >70% 正确对进 top 100（7 个 split protein × 45 补丁对基准）；HECTOR 在 CodeOcean、MD 轨迹与脚本在 Zenodo（doi 10.5281/zenodo.14028991）
role_in_timeline=与本领域主流（Rosetta 界面设计 → 扩散模型 + ProteinMPNN + AF2 pAE 打分）相反的 training-free 分支：把形状互补对接做成可 GPU 加速、可独立于设计阶段的检索模块，用两级 MD 取代学习式判据；同时提出把骨架库从 PDB 换成 AlphaFold2 预测库；与 B09 构成判据口径对照——B09 用带结局标签的近百万条旧数据考筛子，本文判据从未做同类回测，只靠 24 条前瞻候选支撑结论
source_pointer=data/literature_cards/fulltext/K41_PMC12412469_text.txt（SHA-256 前缀 ba19d4044d5b4b6a…，96,740 B）+ 同目录 K41_PMC12412469_fullTextXML.xml；DOI 10.1002/advs.202502015、PMCID PMC12412469、PMID 40686280；登记底稿 sources/cost-benchmarks.md
CSV回填-->
