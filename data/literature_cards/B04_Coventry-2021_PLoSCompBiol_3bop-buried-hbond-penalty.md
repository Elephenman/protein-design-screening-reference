# [B04] 把「埋藏未满足氢键」做成能塞进两两打分表的惩罚项——Rosetta 侧链打包时代补物理项的一次教科书动作

Coventry Brian, Baker David（华盛顿大学 Molecular Engineering & Sciences Institute / Institute for Protein Design / Biochemistry / HHMI）
PLOS Computational Biology 2021, 17(3): e1008061 · DOI 10.1371/journal.pcbi.1008061 · PMID 33684097 · PMCID PMC7971855
开放获取（CC BY 4.0）· 全文链接 https://pmc.ncbi.nlm.nih.gov/articles/PMC7971855/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B04**（组：Baker组；文献类型：方法） |
| 本文取回方式 | Europe PMC `fullTextXML`（HTTP 200，81,545 B，记 `OK ok`），2026-10-20 本地抓取；见 `data/literature_cards/fetch_log.tsv` 的 B04 行 |
| 本地全文 | `data/literature_cards/fulltext/B04_PMC7971855_fullTextXML.xml`（SHA-256 `0ba9a44cd7072026…`）与去标签归一化纯文本 `data/literature_cards/fulltext/B04_PMC7971855_text.txt`（44,739 B / 归一后 44,654 字符，SHA-256 `53a3801e13893975…`） |
| 抓取副产物（有价值的意外） | 这份 fullTextXML **连同行评审记录一起抓下来了**（PLOS 公开 peer review），本卡第 2 节的第 8 条应对直接引这段评审史；`Reviewer #1: The authors have satisfied all of my requests with their review.` 即修订后的复审原句 |
| 对照底稿 | `sources/baker.md` 第 55–66 行（原卡）。本卡补：3BOP 的确切算法（含过饱和修正的取 max 写法）、埋藏区计算的 poly-Leu 预处理与阈值范围、全部对照实验与数字、公开评审记录里的审稿意见与本文对应增补、运行时开销的真实成因（98% 花在字典查找而不是三体计算） |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中；见第 9 节自检） |
| 未取到的部分 | S1 Text、S1 Fig、S2 Fig、S3 Fig 只有正文/图注文字，图内数值与 100/97 个蛋白的逐蛋白分布没有取（在 S1 Data 里）；Table 1 是本文正文里的表，本卡只取图注与表注里能逐字命中的部分。凡依赖未取数据之处，本卡明写「正文未给出具体数值，只有图注描述」 |
| 底稿登记 | `sources_map.json` 的 B04 条目已登记两份全文（`_fullTextXML.xml` 与归一化 `_text.txt`）加 `sources/baker.md`；本卡引句按 §9 声明只与 `_text.txt` 逐字比对（xml 被门禁排除，非可读底稿） |

## 1. 这篇到底解决什么（大白话）

Rosetta 做侧链打包时，为了跑得快，**只会两两相加地算能量**：位置 i 选氨基酸 A、位置 j 选氨基酸 B，两者之间的分数就固定了。但「这个极性原子是不是被埋起来了、有没有氢键把它的氢键需求喂饱」这件事天生不是两两的——它取决于**周围一圈所有邻居**，甚至是三体的：两个 serine 共同喂饱同一个 glutamate 氧，第三个再来就是浪费。于是设计出来的蛋白里经常出现「埋起来了、却没有氢键」的极性原子，这在热力学上是实打实的代价（天然蛋白里几乎看不到这种原子），但打分函数看不见它。

这篇的做法：把「埋藏」这件事**在序列确定之前**用只含亮氨酸的假结构先算好（序列无关，所以可以预算），再把「喂饱 / 过度喂饱」的账**预先摊到 rotamer 对的两两能量项里**，从而让一个本质上三体的 all-or-none 判据，装进两两分解的打分表。结果不是「更好的设计命中」，而是**同一批设计里的埋藏未满足极性原子计数下降**（7 → 5，50th 百分位）与「完全满足所有极子的 dock 从 0 个变成 3 个」。

值得单独记住的是它的**定位**：这是 Rosetta 时代（2021）补物理项的典型动作——同期 [B03] 已经用网络幻觉做全新 fold，[B05] ProteinMPNN（2022）与 [B28] LigandMPNN（2025）之后，这类判据被吸收进神经网络的序列似然与全原子条件化里，而不是继续给能量函数打补丁。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述 + 本文公开评审记录）

1. **核心矛盾：要罚的东西不是两两可加的**。原话："Efficiently representing the energetic cost of unsatisfied hydrogen bonds with a pairwise-decomposable energy term during protein design is challenging since whether or not a group is satisfied depends on all of its neighbors."，并且更早一段就把症结点出来："The most computationally efficient implicit solvent models are pairwise additive, but identifying and penalizing buried unsatisfied polar atoms is challenging using such models as burial is a collective property." **应对**：把「算」和「用」拆开——"We take advantage of the fact that for rotamer-based side chain packing calculations, while the calculated energies must be pairwise-decomposable, the calculations leading to these energies need not be pairwise-decomposable." 三体账目在 Monte Carlo 轨迹开始之前算完，轨迹里只查两两表；代价是这条路线只适用于固定骨架、且所有 rotamer 事先可得的场景："The method is applicable to fixed-backbone packing trajectories and requires that all rotamers are available before the Monte Carlo trajectory begins."
2. **已有的两两溶剂化项是「渐进埋藏」，不是「全有全无」**。作者对 LK / LK-Ball 的批评："Instead of a switching behavior where an atom becomes completely buried and can no longer hydrogen bond with water, the burial is gradual and depends on the local density of nearby atoms."，并进一步指出 "These approaches do not specifically penalize buried unsatisfied polar atoms, but instead attempt to model this effect indirectly through balancing the energies of desolvation and hydrogen bonding."（而 Rosetta 现成的 BuriedUnsatisfiedPolarCalculator 又慢又不兼容打包器："These methods work well on a fixed protein, but they are not amenable to the implicit-solvation pairwise-decomposable sidechain packer of Rosetta"）。 **应对**：不再用「去溶剂化 vs 氢键」平衡间接表达，而是**直接造一个显式惩罚**："We describe a method for explicitly penalizing buried unsatisfied polar atoms during sidechain packing called the 3-Body Oversaturation Penalty (3BOP)."，其形状是氢键数 H 的二次函数（β、σ、ω 三项），于是相对线性模型更贴近全有全无的特征——原句在中间被一组原文引号断开，可核验的后半为 "aspect of buried unsatisfied atoms than linear models such as the LK solvation model."。
3. **最容易踩的坑：重复计数**。作者摘要级解释："This fails when two different amino acids satisfy the same atom; the pairwise nature of the protein design software will double count the satisfaction bonus." **应对**：不做事后判断，而是**提前把过度喂饱的账摊到两个满足者之间**："Here we show that by anticipating the situation where two amino acids satisfy the same polar atom, we can apply a penalty to the two amino acids in advance and assume the polar atom will be there."，并断言 "This scheme correctly penalizes unsatisfied polar atoms and does not fall victim to overcounting."
4. **摊账摊过头：同一序列位点上互斥的 rotamer 被当成同时存在**。原文："A problem occurs with this simple algorithm when multiple B from different rotamers at the same sequence position hbond to the same Q1<->Q2 pair."（本卡不整句引用，因为它跨了脚注编号）；他们判定 "This oversaturation penalty is an error because these B cannot exist at the same time." **应对**：给同一对 rotamer 只保留最坏情况的值——"The solution is to limit the oversaturation penalty to the maximum value one rotamer can generate at each position."，即正文里 Corrected 3BOP Algorithm 的 `max(M[...])` 写法；顺带还给了省内存的等价做法："The memory footprint of M can be greatly reduced if instead of storing a list, one only stores the running max value after iterating over each rotamer R."
5. **「埋藏」本身要先定义，而且定义必须与序列无关**（否则设计前算不了）。 **应对**：把结构先变成假的多聚亮氨酸再量深度："the protein is first mutated to poly Leucine with Chi1 = 240 and Chi2 = 120"，然后 "used to voxelize cartesian space at 0.5Å resolution, determine the molecular surface with a 2.3Å radius sphere, and label each voxel with its depth below the molecular surface"，阈值写成可选项："The burial region is then defined as all voxel XÅ below the molecular surface where X is between 3.5-5.5Å depending on user preference"。**留下的代价（作者自己承认的漏判）**："However, polar atoms just below the surface will not be considered buried."，并且给了一个具体反例（埋在 4.5 Å 面外、却被 Phe 环盖住的骨架羰基），结论是 "Such an oxygen would be buried by explicit solvent or SASA-based measure, but would not be buried by this algorithm."——**这条本文没有解决**，只是说明其性质。
6. **幽灵罚：埋藏原子最终没被选中，罚却已经加在两个 rotamer 之间**。原话："However, a limitation of our approximation is that the oversaturation penalties do not depend on the presence of the buried polar atom rotamer."，并举 Fig 1 的情形说明（Glu rotamer 不在场时 Ser–Ser 之间的罚仍在）。 **应对**：①**量化它**——拿一个天然埋藏氢键网络密集的蛋白来测（"To investigate the extent to which this happens, Outer Membrane Phospholipase A of E. Coli, a natural protein with extensive buried polar networks was repacked with an implementation of 3BOP in Rosetta."），结论是 "As S2A Fig shows, the less strict the threshold for h-bonds, the more the extraneous penalties."，并且 rotamer 越多（加 rotamer 或开设计）越严重；②**给出可操作的缓解**："This problem may be reduced by increasing the stringency of the h-bond-quality threshold or limiting the number of polar rotamers."；③**论证在设计场景里可以忍**——这是本文最像「工程判断」的一段："For designed proteins, there may be several solutions that satisfy a backbone and if one of them is eliminated by an error, there are still several other equally valid solutions, and an almost infinite number of backbones may be attempted."，并明确不对称性："Overall, for design, sins of omission (moving forward with designs containing buried unsats) are more serious than sins of commission (incorrectly eliminating a reasonable design)."。但作者也承认同一件事反过来成立："While the extraneous oversaturation penalties may pose a problem for structure prediction"——即**这套惩罚不适合拿去做结构预测**。
7. **指标只有「计数」，没有任何湿实验**。全文的判据是计算量：埋藏未满足极性原子数、跨界面氢键数、氨基酸恢复错误率；没有任何表达、亲和力或热力学测量。 **应对**：本文没有对此做应对（它把自己定位成能量函数/打分器改造，"This is a PLOS Computational Biology Methods paper."），只给出「相对基线更好」与「比单纯加强氢键更好」的对照："Figs 2A and S1A show that incorporation of 3BOP results in fewer buried unsatisfied polar atoms than simply increasing the hydrogen bond strength."——也就是说**它证明的是「这个项改变了优化方向」，不是「设计出来的蛋白更行」**。
8. **审稿人把上述弱点逐条点出来了，而本文的应对全部留在正文里可查**。第一轮 Reviewer #1 说："The authors don't really tell us what parameters to use for 3BOP and leave out some important details about the experiments that they performed."，要求命名（"It needs a name."，并自己提议 "Three-body oversaturation penalty"），说 "This is a clever approach to a vexing problem, and the authors present some compelling results, but there are a few things that leave the reader unsatisfied."。具体三条改动压力：①对照设计不充分——"A better test would be 1-sided interface design and interrogate the number of buried unsatisfied polar atoms on the side held fixed."、"It seems important to report the number of buried polar atoms that the different score functions create."，还注意到计数下降可能是「少埋极性原子」换来的："It is fascinating and confusing that the median number of buried polar atoms per design could decrease from 5 to 2 while the number of hydrogen bonds only increased by two"；②预计算带来的开销与通用性——"Figure 3B shows that only a tiny fraction of the total design time is consumed on 3BOP; however, 3BOP relies on the pre-calculation of all pairs of rotamer energies ahead of design, and the standard design algorithm in rosetta is to compute pair energies on the fly."；③幽灵罚——"Figure 3A shows a concerning presence of oversaturation penalties between pairs of atoms that are simultaneously hydrogen bonding to the same absent/phantom atom."，并要求 "It seems like there is likely some price that comes with the use of 3BOP, but there's little that the authors present in terms of investigations into what that price would be."。 **他们做了什么**（对照发表版的可见痕迹）：给方法起名 3BOP；在图注里把每个变体的参数写全（"the parameters were β = 5, σ = -5, and ω = 5 for all polar atoms"，无过饱和变体是 "the parameters were β = 5, σ = -5, and ω = 0"，Lys-NZ 另有 β = 15 / σ = -10 的特例）；把「只允许极性残基重新设计天然蛋白」这一能排除「少埋就不罚」漏洞的测试做成 S1 Fig，并同时报告埋藏极性原子总数（S1C，正是审稿人要的那一项）；把幽灵罚做成 S2 Fig（1ILZ 网络 + 97 个蛋白的恢复误差对照）；把开销做成 S3 Fig 的时间分解。修订后复审原句是："The authors have satisfied all of my requests with their review."（2021-02-12 编辑部 provisional accept，2021-03-02 正式接收）。
9. **运行时的真实开销不在算法本身，而在实现**。作者自己拆解：尽管 3BOP 带来了可观的运行时间增加，"only 2% of this runtime is spent calculating the actual 3-body interactions."，而 "98% of the runtime is spent later in dictionary lookups during rotamer-pair energy assignment."，并直接指出可优化点："With better data management, the green bar could be avoided as h-bonds are double calculated here"。**留下的代价**：这一实现缺陷本文没修，只是记账；作者对全篇的收口是自评式的："The 3BOP algorithm is computationally efficient ( S3 Fig ), and in its current form without explicit water atoms, is now widely used in our research group"——「组内广泛使用」不是外部验证。
10. **显式水没有处理**，而埋藏极性饱和恰恰常靠水完成。 **应对**：只给出「可以加」的论证而没有加——"While this paper and the implementation in Rosetta do not consider explicit bound water molecules in crystal structures or from other sources, incorporating these is straightforward."，条件是 "As long as the location of the water molecules is known at pre-compute time, they may simply be modeled as polar atoms that can make hydrogen bonds."。**本文未解决**。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **Rosetta 组合侧链打包 + ref2015 能量函数**：宿主系统。选它因为设计流程就是它；新增项以「伪能量」形式插进两两表，因此**不改动采样器**。
- **poly-Leucine 预处理 + EDTSurf 体素化**：为「埋藏」做一个与氨基酸序列无关、可以在设计前算完的定义。
- **二次型惩罚（β / σ / ω 三系数）**：用 H(H−1)/2 的二次项表达 all-or-none，而不是再去调去溶剂化/静电的函数形式（作者明说旧形式的痛点："Previous approaches have sought to more accurately model the energetics of protein electrostatics, but the final functional forms are intertwined with the rest of the force-field in a way that could not be arbitrarily modified."）。
- **对照手段**：①与「直接把氢键项加强」对比（原文 "As the maximum energy for an h-bond in Rosetta is approximately -2 kcal/mol"，两个加强氢键的对照变体把上限抬到 -7 与 -12 kcal/mol）；②与 ω=0 的「不带过饱和」变体对比；③与 ref2015 裸基线对比。
- **评测集**：de novo 界面（barnase 一侧）与天然蛋白重设计两类，两类都是**计算计数指标**。
- **没有用的方法**：无 MD、无 QM、无自由能微扰、无任何湿实验（表达/结合/热力学）。全文里连一次实验测量都没有。

### A. 算法本身（Materials and Methods 的顺序）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 任意待设计/待打包结构（蛋白骨架） | 先整体突变成多聚亮氨酸（固定 Chi1/Chi2），再用 EDTSurf 体素化求分子表面并给每个体素标深度 | 体素 0.5 Å；探针球半径 2.3 Å；埋藏深度阈值 X 取 3.5–5.5 Å 由用户定（图例用 4.5 Å，Ubiquitin PDB 1UBQ） | 一个与序列无关的「埋藏区」，只算一次；A1 之后所有判定都不依赖氨基酸身份 |
| A2 | 埋藏区 + 全部 rotamer | 找出所有 rotamer 中落在埋藏区里的极性原子 B，为每个 B 累加三项：1-body β、每个能与 B 成氢键的 Q 加 2-body σ、每对同时喂饱 B 的 Q1–Q2 加 2-body ω | β/σ/ω 可按原子类型分别设；Table 1 给了使「偏离理想氢键数 1 个」罚分为 1 的一组系数（例：NH1 目标 1 条：β=1, σ=-1, ω=2；羰基 O 目标 1 或 2：β=1, σ=-1, ω=1；Carboxylate O 目标 2 或 3：β=3, σ=-2, ω=1） | 惩罚形状是氢键数的二次函数 P = β + σ·H + ω·H(H−1)/2；作者说 "The coefficients β, σ, and ω can be modified to give any quadratic relationship between the number of h-bonds and the penalty." |
| A3 | A2 的三项表 | 逐序列位点 n 做**过饱和修正**：同一位点上互斥 rotamer 造成的 ω 不能叠加 | 对每一对 rotamer 只取所有候选 B 生成的 ω 之和的最大值（`max(M[r_Q1<->r_Q2])`）；实现上可只存 running max | 得到最终的两两伪能量表；局部复杂度 "which is O (n 3 ) on the local number of polar rotamers that h-bond at nearby sequence positions; the algorithm is approximating a 3-body interaction." |
| A4 | 两两伪能量表 + rotamer 库 | 交给 Rosetta Monte Carlo 打包/设计（要求所有 rotamer 事先可得、骨架固定） | 本文未给采样步数/轨迹数阈值 | 每个位点一个氨基酸序列（或 repack 后的构象） |

### B. 验证与对照（Results 的顺序）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 40 个 mini-protein（mixed alpha/beta 与 all alpha 两类拓扑）+ barnase | 对接后做 de novo one-sided 界面设计："40 mini-proteins of mixed alpha/beta and all alpha topology were docked against barnase (PDB: 1BRS) using PatchDock"，每个取前 10 个 dock，"Residues within 10Å of the interface were allowed to repack on barnase and to design with all 20 amino acids on the mini-protein."，序列由 ramped-repulsive pack-and-minimize 得到 | 主指标 = 界面埋藏未满足极性原子数；次指标 = 跨界面氢键数；变体：ref2015、ref2015+3BOP（5×、10×）、ref2015+3BOP 无过饱和（ω=0）、ref2015+加强氢键（2.5×、5×） | "Four hundred de novo one-sided interfaces to barnase" 这一批设计；正文给的结果是 "the 50th percentile structure coming from 3BOP + ref2015 had 5 buried unsatisfied polar atoms" 而裸 ref2015 为 7（推荐 setting of 5）；完全满足所有极子的 dock 数 3 vs 0，即 "Some docks fully satisfied all polar atoms on the target; 3BOP + ref2015 generated 3 such docks while ref2015 alone generated none" |
| B2 | 100 个天然蛋白 | 只允许极性残基的整蛋白重设计（防止「干脆不埋极性」这种绕过），参数与 B1 相同 | 指标 = 每蛋白埋藏未满足极性原子数、埋藏极子的氢键数，另报埋藏极性原子总数（S1C，回应审稿人） | 结果是 "resulted in a median of 2 buried unsatisfied polar atoms while ref2015 alone resulted in a median of 5"；同一句里作者自曝混因："one hundred native proteins were redesigned to only allow polar residues" 的设计同时埋藏了更少极性原子，故**计数下降不能直接等同于更好** |
| B3 | Outer Membrane Phospholipase A（1ILZ，天然埋藏氢键网络密集） | 分别用标准 rotamer / 额外 rotamer 做 repack，以及全氨基酸重设计，统计「多余过饱和罚」占比随氢键能量阈值的变化 | S2 图注统一给出的氢键判定阈值（A/B 两个 panel 共用一套参数）："The h-bond threshold was set to -0.75." | 结论为两条：阈值越松假罚越多、rotamer 越多假罚越多；正文只给趋势描述（S2A 具体百分比在 S1 Data，本文正文未给出） |
| B4 | 97 个天然蛋白的氢键网络残基 | 只允许极性氨基酸重设计，比较 ref2015 / +5×3BOP 无过饱和 / +5×3BOP 的氨基酸恢复错误 | Lys-NZ 特例 β=15、σ=-10；同一图注给的氢键阈值 -0.75 | "Ninety-seven native proteins had their h-bond network residues redesigned using only polar amino acids."（恢复误差的分布数值在 S2B 图内，正文未给） |
| B5 | 1ILZ 的一次 packing/design 计算 | 按用途分解 CPU 时间（罚规则应用 / rotamer 间氢键计算 / 原子深度 / 背景打包），并用 pre-computed interaction graph 设置 | 无阈值；纯记账 | "only 2% of this runtime is spent calculating the actual 3-body interactions."；"98% of the runtime is spent later in dictionary lookups during rotamer-pair energy assignment." |

**这套流程的骨架值得单独记住**：先给一个原本「多体、全有全无」的物理直觉**造一个可以塞进两两打分表的代理量**（A1–A3），再用两类独立计算任务（de novo 界面、天然蛋白重设计）＋**两个正交对照**（不带过饱和的变体、单纯加强氢键）证明代理量确实在改变优化方向；对代理量自身的失真（幽灵罚、表面浅层漏判）用「量化 + 给缓解旋钮 + 论证代价不对称」三件套收尾。**全程没有一步是功能实验。**

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 400 个 one-sided 界面（40 mini-protein × top 10 dock） | de novo 界面验证集规模 | "Four hundred de novo one-sided interfaces to barnase" |
| 10 Å / 全 20 种氨基酸 | 界面附近允许 repack/设计的范围 | "Residues within 10Å of the interface were allowed to repack on barnase and to design with all 20 amino acids on the mini-protein." |
| **5 vs 7**（50th 百分位） | 3BOP+ref2015 vs ref2015 的埋藏未满足极性原子数 | "the 50th percentile structure coming from 3BOP + ref2015 had 5 buried unsatisfied polar atoms" |
| **3 vs 0** | 把所有极子完全满足的 dock 数（3BOP vs 裸 ref2015） | "Some docks fully satisfied all polar atoms on the target; 3BOP + ref2015 generated 3 such docks while ref2015 alone generated none" |
| **2 vs 5**（median） | 100 个天然蛋白「只允许极性残基」重设计后的埋藏未满足极子数 | "resulted in a median of 2 buried unsatisfied polar atoms while ref2015 alone resulted in a median of 5" |
| 97 | 氢键网络残基重设计的天然蛋白数 | "Ninety-seven native proteins had their h-bond network residues redesigned using only polar amino acids." |
| β=5, σ=-5, ω=5 / ω=0 | 推荐 5× 变体与「无过饱和」对照的参数 | "the parameters were β = 5, σ = -5, and ω = 5 for all polar atoms" |
| β = 15, σ = -10 | S1/S2 实验中 Lysine-NZ 的特例参数 | 正文与图注（同一段描述 Lys-NZ 用 β = 15、σ = -10） |
| 0.5 Å / 2.3 Å / 3.5–5.5 Å（示例 4.5 Å） | 体素分辨率 / 探针半径 / 埋藏深度阈值 | "The burial region is then defined as all voxel XÅ below the molecular surface where X is between 3.5-5.5Å depending on user preference" |
| Chi1 = 240、Chi2 = 120（poly-Leu） | 埋藏区预处理的假结构 | "the protein is first mutated to poly Leucine with Chi1 = 240 and Chi2 = 120" |
| O(n³) | 摊三体账到两两表的局部复杂度 | "which is O (n 3 ) on the local number of polar rotamers that h-bond at nearby sequence positions" |
| -2 / -7 / -12 kcal/mol | Rosetta 氢键最大能量，与两个「单纯加强氢键」对照 | "As the maximum energy for an h-bond in Rosetta is approximately -2 kcal/mol" |
| −0.75 | 判定「算一条氢键」的能量阈值（S2 用） | "The h-bond threshold was set to -0.75." |
| 2% / 98% | 3BOP 运行时中真三体计算 / rotamer 对能量赋值时的字典查找 | "98% of the runtime is spent later in dictionary lookups during rotamer-pair energy assignment." |
| 5 → 2、氢键只多 2 条 | 审稿人对「计数下降是否来自少埋极性」的质疑 | "It is fascinating and confusing that the median number of buried polar atoms per design could decrease from 5 to 2 while the number of hydrogen bonds only increased by two" |

## 5. 结论——作者说了什么

1. 3BOP 是一个**可两两分解**的埋藏未满足极性原子惩罚，能直接插进现有 Rosetta 侧链打包，不需要改采样器。
2. 加了这一项之后，"We show that inclusion of this term in Rosetta sidechain packing calculations substantially reduces"（摘要收口），且效果优于单纯把氢键项加权。
3. 惩罚是**可定制**的：设计者自己定 β/σ/ω，因此 "Explicit control allows designers to directly penalize buried unsatisfied polar atoms."，并且可以为不同原子类型指定不同理想氢键数。
4. 该实现无显式水；作者认为加入水的做法直接（第 2.10 条），但没有做。
5. 作者的自我限制：多余过饱和罚是真实存在的近似误差，会影响结构预测；对设计则论证代价不对称。本文没有任何湿实验。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **「把不可两两分解的约束预计算后摊进两两打分」是可复用的工程模板**。对我们真正可搬的是这个动作的形状：先找一个**与序列无关、可在设计前算完**的几何/化学量（这里是 poly-Leu 埋藏深度），再把多体判据折成对子表。我们的 UAA 催化位点「预组织 + 竞争副反应位点是否被埋」正属于同类多体量，而现在我们的漏斗里没有任何这样的预处理层。
2. **它同时是一个「代理指标陷阱」的教科书样本**：优化的目标量就是被评价的目标量（埋藏未满足极子数既是惩罚项也是结果指标）。审稿人一眼看穿（少埋极性也能降计数），作者用「只允许极性残基」和「同时报告埋藏极性原子总数」把漏洞收窄，但**没有彻底封住**，因为最强的封法需要湿实验而本文没有。→ 对我们：凡是「筛子的分数」与「验收的分数」是同一个量，必须在卡里明写这条不成立，不能报成 improvement。
3. **「漏放比误杀严重」是本项目该显式表态的东西**。作者用一句不对称性论证为近似误差开脱；我们在 UAA 漏斗上同样存在这种不对称（假阳性候选花一轮湿实验，假阴性候选可能永远是唯一能做的构建体），但我们目前的判据一律写成对称的分数阈值，没有做过一次这样的成本不对称声明。
4. **运行时的账要算到实现层**。98% 时间在字典查找而不是三体计算——这类信息只在作者把时间拆开后才可见。→ 我们的 MD/打分漏斗同样只报了总 GPU·h，从没拆过「真正用于物理计算 vs 数据搬运/IO」的比例。
5. **PLOS 公开评审记录是低成本的高价值证据源**。本文「遇到问题做了什么」几乎全部可以从评审史里直接读出来（要名字 → 取名、要参数 → 图注写全 β/σ/ω、要更公平的对照 → S1/S2、要开销 → S3）。以后遇到 OA 且公开 peer review 的行（PLOS / eLife / Nature 系），值得把评审段落当作方法学证据抓下来。

## 7. 局限与失败（作者的 + 我们读出的）

- **作者自认**：①近似误差（幽灵罚）存在，且对结构预测不友好；②埋藏判据会把贴着表面、实际被大侧链盖住的极性原子漏掉，本文不处理；③不含显式水；④实现里 98% 时间花在字典查找；⑤β/σ/ω 需要使用者自己按场景定（"may be selected on a per-buried-polar-atom basis"），文中 Table 1 只是示例（"The target # Hbonds listed here are for example only and are not necessarily ideal."）。
- **我们读出的**：①**全文零湿实验**，所有结论都是计算计数，因此「埋藏未满足极子减少」与「设计真的更稳/更能结合」之间的链条本文没有闭合，是**被后续工作默认吸收**而不是被证明；②计数下降与埋藏极性原子总数下降同时发生（第 4 节 2 vs 5 那条），作者自己写了混因，读者容易只记住前者；③「现在组内广泛使用」不是外部验证；④没有绝对命中率或成功率——这篇里没有任何「多少个设计成功」的量，把它当「提升命中率的证据」引用属于误用。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **「序列无关的预处理层」这个动作**（DP2R 标准 G1/G2 侧写）：在做任何序列设计/打分之前，先把与序列无关的几何事实（哪些位置是深埋的、催化位点周围的空腔与极性分布）一次性算出来并缓存，后续所有判据引用它。我们现在的埋藏/空腔判断混在逐候选的打分里，重复且不可比。
2. **多体约束摊进两两表**：如果要把「催化三联体三点是否同时到位」这类三体条件接进便宜打分器，本文给的路线是「预算 + 取 max 避免互斥 rotamer 叠加」，而不是一上来就上位自由能方法。这是最便宜的可行替代，且**明确标着自己的误差**。
3. **把「代价不对称」写成判据的一部分**：给每个闸口标注它更怕漏放还是更怕误杀，并据此定阈值方向（我们漏斗目前的阈值全部来自「分布拐点」，没有一处写了不对称偏好）。
4. **给近似误差做专项量化**（本文的 1ILZ 做法）：挑一个**已知该判据会很别扭**的极端样本（对我们：已知的多埋藏极性、且必须靠水或金属配位满足的催化位点），单独统计假罚比例，而不是只在平均分布上展示好处。

**不可迁移（为什么不能照搬）**

1. **它的输出根本不是功能**。这项惩罚降低的是「埋藏未满足极性原子计数」，与「能不能催化 UTP → pppUA / 环化」没有本文层面的任何联系。把 3BOP 当 UAA 酶活判据或先验筛选器是误用；至多作为**结构合理性**的一道弱检查，且必须写成「不计入成功概率」。
2. **它的数字不能当我们的命中率或提升幅度**：7→5、0→3、5→2 都是同一批计算设计的计数变化，样本量小（40×10、100、97），且没有独立实验验证；引用时只许引用方法结构。
3. **它依赖固定骨架 + 事先可得全部 rotamer**（"requires that all rotamers are available before the Monte Carlo trajectory begins"），而我们的路线里骨架本身是生成的（RFdiffusion 类），预处理层的「与序列无关」前提就不成立——直接照搬会失效，需要先决定深度阈值在动态骨架上如何重算。
4. 无 MD/QM 这一点不能反过来被本文用作「不需要 MD/QM」的证据：本文的对象是静态打包打分，从未处理任何化学态或反应坐标。

## 9. 溯源与自检

- 本地纯文本：`data/literature_cards/fulltext/B04_PMC7971855_text.txt`（Europe PMC fullTextXML，剥标签、HTML 实体已解码、破折号/引号归一，未改写内容；SHA-256 `53a3801e13893975…`）。同目录 `_fullTextXML.xml` 为原始件（`0ba9a44cd7072026…`）。

引句底稿: data/literature_cards/fulltext/B04_PMC7971855_text.txt

- 公开评审记录位于同一份全文尾部（PLOS 的 `Decision Letter 0` / `Author response` / `Decision Letter 1` / `Acceptance letter` 段落），本卡第 2.8 条引句即出自其中；作者对第一轮意见的**响应正文没有进入 XML**，只有一个附件名（`Buried Unsat Letter to Reviewer.pdf`），因此第 2.8 条里「他们做了什么」是我用发表版本正文/图注的可见增补逐条对照出来的，不是从回复信里引的。
- 对照底稿行号：`sources/baker.md:55–66`（原卡，摘要级）；同文件 `:636` 把本文归入「Rosetta 时代修补物理打分」的解释线、`:606` 把「埋藏未满足氢键惩罚」列入 3b 物理/化学正交筛。
- CSV 字段映射：本文第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B04 --no-report`（输入：本卡 + `sources_map.json` 登记的 B04 底稿）把卡内所有不含中日韩字符、且被直双引号包住的 ≥20 字符 / ≥12 字母片段，在 §9 声明的那一份全文里逐字查找，任何一条不命中即 FAIL。本卡结果 **PASS B04 quotes=82/82，退出码 0**。首轮有两处不合格：①一处引句截在了省略号处（原文那句中间自带一组引号 all or none，直双引号跨不过去），改成只引可核验的后半段；②把 singular 的 the same sequence position 抄成了复数 positions。两处按全文原样改回后复跑转绿；此后又红过一次——原因是 §9 自检段里用直双引号举了一个「我抄错的片段」作例子，那一行本身被门禁当引句比对（省略号式截断必红），改成中文述句后转绿。B04 只有一份全文通路（Europe PMC），没有 B09 那样的双通路互证，这一点在本卡第 0 节已标明。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 1 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=方法（能量函数/打分器改造，无湿实验）
target=通用序列设计环节（Rosetta 侧链打包/界面设计时埋藏极性原子的氢键饱和），非特定靶点；验证用 barnase 界面 + 100/97 个天然蛋白重设计 + 1ILZ
backbone_generation=不生成骨架；在给定/固定骨架上做 Rosetta 组合侧链打包（de novo 界面用 PatchDock 对接 mini-protein 到 barnase，界面 10 Å 内 repack/设计；天然蛋白做只允许极性残基的重设计）；埋藏区由 poly-Leucine 预处理 + EDTSurf 体素化预先算出
computational_filters=新增可两两分解的「埋藏未满足氢键」惩罚 3BOP：1-body 埋藏罚 β、喂饱加成 σ、过度喂饱罚 ω（对同时喂饱同一极子的两个残基之间加），并按每序列位点取 max 修正互斥 rotamer 叠加；对照变体：不带过饱和（ω=0）、单纯加强氢键（最大能量 −2 → −7 / −12 kcal/mol）、裸 ref2015
thresholds=埋藏深度 X = 3.5–5.5 Å（图例 4.5 Å）；体素 0.5 Å；探针 2.3 Å；推荐 5× 系数 β=5, σ=-5, ω=5（Lys-NZ 用 β=15, σ=-10）；判定一条氢键的能量阈值 -0.75；局部复杂度 O(n³)
md_used=否
qm_used=否
experimental_methods=无（全部为计算评测：界面埋藏未满足极性原子计数、跨界面氢键计数、氨基酸恢复错误率、CPU 时间分解）
pipeline_counts=barnase 一侧 40 个 mini-protein × 前 10 dock → 400 个 de novo one-sided 界面；100 个天然蛋白「只允许极性残基」整蛋白重设计；97 个天然蛋白的氢键网络残基重设计；1ILZ 用于幽灵罚与运行时专项分析
hit_rate=未记录（本文不报命中率/成功率，只报计数分布变化：50th 百分位埋藏未满足极子 7→5；完全满足所有极子的 dock 0→3 个；100 蛋白重设计 median 5→2，且同批设计的埋藏极性原子总数也同时减少）
best_metric=未记录（本文无任何亲和力/表达/热力学测量，Kd 或活性最好值不适用）
cost_or_stat_note=运行时分解：真三体相互作用计算只占 3BOP 引入时间的 2%，98% 花在 rotamer 对能量赋值时的字典查找；埋藏深度因与序列无关可在打包前一次算完
role_in_timeline=Rosetta 时代「补物理项」的代表动作：把多体、all-or-none 的埋藏氢键饱和约束预计算后摊进两两打分表；同一「埋藏极性必须成氢键」判据后被吸收进 ProteinMPNN（[B05]）与 LigandMPNN（[B28]）的序列似然/全原子条件化，之后 Baker 组的界面过滤里它作为 3b 物理化学正交筛继续存在；本文也说明这类修补无法替代「设计会不会成功」的功能判据
source_pointer=data/literature_cards/fulltext/B04_PMC7971855_text.txt（SHA 53a3801e13893975…）+ 同名 _fullTextXML.xml（0ba9a44cd7072026…，含公开评审记录）；sources/baker.md:55-66、:606、:636
CSV回填-->
