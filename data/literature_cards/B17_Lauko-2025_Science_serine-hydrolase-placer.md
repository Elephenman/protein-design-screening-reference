# [B17] 丝氨酸水解酶的从头设计：把筛子从"结构对不对"换成"沿反应坐标的多个态是否预组织"

Lauko A, Pellock SJ †, Anishchenko I, Sumida KH, Juergens D, Ahern W, Jeung J, Shida A, Hunt A, Kalvet I, Norn C, Humphreys IR, Jamieson C, Krishna R, Kipnis Y, Kang AK, Brackenbrough E, Bera AK, Sankaran B, Houk KN, Baker D *（华盛顿大学 Biochem/IPD + UCLA Houk 组）
Science 2025, 388: eadu2454 · DOI 10.1126/science.adu2454 · PMID 39946508 · PMCID PMC12288761（NIHMS 接受稿）
CC BY 4.0 · 全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC12288761/ （前身 bioRxiv 2024.08.30）
† 共同第一作者 · * 通讯作者

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B17**（组：Baker组; 通用方法学; 口径对照） |
| batches 状态 | **FULLTEXT**（`data/literature_cards/batches.tsv` 第 5 批） |
| 本地全文（本卡引句底稿） | `data/interim/baker_lit/ft/serinehydrolase2025.txt`（82,350 B，2026-10-16 抓取，Europe PMC fullTextXML 去标签纯文本；正文表头带 NIHMS 字样，说明取到的是**作者接受稿**而非 Science 排版版） |
| 对照底稿 | `sources/baker.md:224–236`（原卡）、`sources/baker.md:607`（3c 活性位预组织行）、`sources/baker.md:612`（确证行）、`sources/baker.md:646`（酶专用判据段）、`sources/baker.md:662`（QM 角色定位）；本卡在其基础上补：NTF2 前置战役及其否证、round 3 motif 生成失败与两步补救、AF2 三项阈值的完整组合、PLACER 的输入/种子/裁剪口径、DFT 泛函与基组、g−/g+ 与第二对 oxyanion 的因果链、r5–r8 各轮的针对性修补 |
| 证据级别 | **全文级**（本卡所有英文引句可在本地全文逐字命中；见第 9 节） |
| 未取到的部分 | Supplementary/Computational methods 的细节段（CA diffusion 具体做法、过滤脚本、fig. S1 每轮设计数目流程图、fig. S5–S17 逐条数值）、Fig 2B 轮次总表的原始计数。凡涉及这些之处本卡明写"正文未给" |
| 与 CSV 既有字段的差异 | CSV `thresholds` 已记的三条原句核对通过；但 CSV `md_used=否` 需要留证据：本地全文里 **molecular dynamics 一词一次都没出现**（本卡第 9 节给出检索结果）；另外 CSV `round1 129→2 活性(1.6%)` 的 1.6% 在正文里是"10 round 2 designs (5.2%)"同段的"two round 1 designs (1.6%)"，属**占合成基因总数（129）之比**，不是"占 FP 阳性者之比"——引用时别混淆分母 |

## 1. 这篇到底解决什么（一句话+大白话）

**多步催化、需要四个残基原子级摆位的酶，能不能从零设计出来？** 以往酶设计的套路是"给定活性位几何 → 去固定骨架库里找能装下的口袋"（theozyme + 库匹配），这篇先照旧路子做了一轮（NTF2 大库），结果是**只做出活化丝氨酸、做不出转换数**；于是换成 RFdiffusion **围着活性位几何直接长出新骨架**，再解决第二个问题：折叠对了、静态结构像了，**不等于沿整条反应路径每个态都摆得对**。为此他们做了 PLACER（一个随机化的侧链+小分子坐标生成网络），对 apo/结合/TI1/AEI/TI2 五个态各出 50 帧构象系综，用关键氢键形成频率当筛子。最终拿到 k_cat/K_M 最高 4,300 M⁻¹s⁻¹ 的设计丝氨酸水解酶，X 射线与设计模型几乎重合，而且落在天然丝氨酸水解酶从未有过的 5 种折叠上。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **静态自洽性判据在催化任务上根本不够用（本文的主论点）**。他们做这件事的直接动机也写得很明白——**先解释别人为什么失败，再决定加什么判据**："We set out to understand why previously designed serine hydrolases failed to appreciably catalyze ester hydrolysis and hypothesized that modeling each state of the reaction coordinate could be critical for assessing the ability of a design to achieve catalytic turnover"，并且用天然与既有设计各跑一遍系综来坐实这个假设："At each step in the reaction coordinate, the catalytic residues sample the key hydrogen bonds essential for catalysis more often in native than designed serine hydrolases"。结构性困难本身作者也摆明了："Achieving preorganization is especially difficult for multistep reaction mechanisms, because the enzyme must preferentially stabilize multiple transition states and intermediates"，并指出可用的评价工具"existing methods to evaluate design preorganization in silico are limited by low accuracy or computational cost"（作者原话只说到"精度低或算力贵"，未点名具体方法；QM/MM 在本文讨论里是作为他人的互补手段出现的）。 **应对**：造一个便宜的构象系综生成器顶上——PLACER（"PLACER is stochastic, and repeated runs from different random seeds yield an ensemble of models for the predicted region"），把"预组织"变成可数频率："we compute the frequency of formation of key interactions between the catalytic functional groups and reaction intermediates over each step of the reaction"。 **效果（作者口径）**："The value of this approach is evident in the dramatic improvement in experimental success rate upon filtering with PLACER"。而且他们把 r1/r2 特意做成**只有筛子不同**的对照（活性位复杂度相同，都是 Ser-His dyad + 一对主链 oxyanion）："In the first two rounds of design, we built relatively simple active sites consisting of Ser-His dyads with a single oxyanion hole contact from the backbone amide of the serine"，"round 1 designs were filtered with AF2 alone, while round 2 designs that passed the AF2 filter were selected for experimental screening if PLACER ensembles of the apo state indicated the key Ser-His hydrogen bond was formed"。
2. **固定骨架库装不下这套几何——先用实验把自己的第一条路否掉**。前置 NTF2 战役（RosettaMatch + trRosetta 理想化 NTF2 库）做完后："experimental characterization of the resulting designs revealed activated serines but no catalytic turnover on ester substrates, despite a close match between the experimental and designed structures"。 **应对**：不回头调匹配参数，而是**换生成范式**——RFdiffusion 从 motif 向外长出全新骨架；并给出机制层面的解释作为下一步判据："We suspect that an inability to install key catalytic features into NTF2s, such as the backbone oxyanion hole contact common to all serine hydrolases, limited the function of these designs"。→ 这一轮失败的产物直接被回收进第 5 节的 812 设计统一分析里当阴性样本。
3. **AF2 一道筛子几乎不淘汰任何东西，PLACER 一道就淘汰 98.4%**。round 1 只用 AF2，round 2 加了 PLACER  apo 态判据后："Only 1.6% of round 2 designs that passed the AF2 RMSD filter were predicted to be preorganized by PLACER"。 **应对**：把这道极窄的闸口**明写进漏斗**并让实验按闸口取样（"round 2 designs that passed the AF2 filter were selected for experimental screening if PLACER ensembles of the apo state indicated the key Ser-His hydrogen bond was formed"），而不是嫌它太严就放宽。 **代价**：计算通过率被压到 1.6%，等于把成本全部推到"先生成足够多骨架"这一侧。
4. **一次把 triad + 第二个 oxyanion hole 全摆好，反而生成不出可用骨架**。round 3 motif 起初把 Asp/Glu 与第二对 oxyanion 氢键一起写进 motif，结果"backbones produced from these motifs had exceedingly low AF2 success rates, presumably due to the generation of incompatible combinations of backbone conformations"。 **应对**：**把一次性约束拆成两步搜索**——先用简单 substrate-Ser-His motif 生成大量骨架（"we generated 10,000 backbones with RFdiffusion using the simple substrate-Ser-His motifs as input"），再在这些骨架里用 Rosetta 找能容纳 Asp/Glu 的次结构位置，最后同样方式补第二个 oxyanion 残基（"ultimately producing 2238 unique round 3 motifs with Ser-His-Asp/Glu catalytic triads"）。对比：round 1/2 只有 108 个 motif。
5. **做出来了但只转一轮：AEI 水解不掉（这是全文的核心失败模式）**。round 1/2 的进度曲线在约一个酶当量产物后就平了——"The progress curves for these round 1 and 2 designs plateau after approximately one enzyme equivalent of fluorescent product is formed"，并且质谱给出与酰化对应的质量位移，作者据此判定"protein inactivation following formation of the acylated intermediate"。 **应对（四层）**：① **设计端加约束**：round 3 起把催化酸与第二个 oxyanion 供体写进 motif 并要求 apo + AEI 两态都预组织（"we required all catalytic triad and oxyanion hole H-bonds to be highly preorganized in PLACER ensembles of both the apo and AEI states"）；② **判据端沿反应坐标加密**：由 2 态（apo+AEI）扩到 4 态过滤；③ **诊断端做归因**：对 812 个已表征设计跑 PLACER 系综，找出失活的结构原因——"designs that irreversibly acylate switch to the g + rotamer in the AEI"，而 g+ 之所以失能："The g + serine rotamer is catalytically incompetent in these designs because it leads to an acyl group conformation that occludes interaction of the hydrolytic water with histidine"；④ **拿旧数据回溯自检新判据**："Retrospective PLACER analysis of the round 1 designs revealed that the Ser-His H-bonds in the two catalytically active designs were predicted to be among the most preorganized"，而加了闸口的 round 2 一侧："PLACER filtering of round 2 designs on the extent of formation of the key Ser-His H-bond not only increased the fraction of designs exhibiting FP probe labeling and enzymatic activity, but also resulted in higher activities"。
6. **诊断出的结构性根因，然后按根因改设计（不是继续加筛子）**。① 发现第二对 oxyanion 残基会偏向活性构象："The second oxyanion hole contact in serine hydrolases thus not only stabilizes the transition state but likely helps orient intermediates in catalytically productive conformations"；② 发现 r4 系列里活性更高的重设计在 AEI 态更能保住设计的 T99 旋转构象（"r3-win never adopts this rotamer"）；③ 发现设计的 oxyanion 氢键**在羰基平面内**，与天然的**平面外**几何相反——"Analysis of the oxyanion hole geometries in these designs and others in earlier design rounds reveal in-plane hydrogen bonds to the oxygen of the substrate carbonyl"。 **应对③ 具体动作**：去借天然的几何而不是借序列——把 r3-super 的 Gln71 突变为 Asn、按 subtilisin Asn155 的平面外取向摆位，再用 RFdiffusion（RFam）重建周边骨架（"Using the subtilisin oxyanion hole geometry as a guide"），150 个设计中拿到 k_cat 提升 8×/7× 的两条。
7. **修补方向不靠猜，靠"局部重生成"**。r6-momi 之后还想再提活，他们没有做理性突变扫描，而是"we built out the N-terminus to further stabilize the active site but made no changes to the parent backbone or sequence"（固定母体、只扩散新生一段 20–50 aa 的 N 端次结构，1000 轮），结果"Of 65 designs tested, all showed activity"，最佳 r7-momi120 = 4,300 M⁻¹s⁻¹。 **含义**：把"优化"变成"在指定自由度上重新生成 + 同一套闸口复筛"，而不是在序列空间里搜索。
8. **换了个新催化几何（N+1 oxyanion 型），没有历史经验可依**。 **应对**：直接照同一管线跑（"We used the RFdiffusion and LigandMPNN/FastRelax design pipeline to generate 66 designs for this new catalytic site and the larger 4MU-PhAc substrate"），一次成功："The high activity achieved without any prior experimental characterization for this new catalytic site shows that filtering for preorganization across the reaction cycle can yield novel catalysts in one shot"。→ r6-momi 的 k_cat/K_M = 1,240 M⁻¹s⁻¹、k_cat = 0.1 s⁻¹。
9. **判据"过了四态"仍然会失活，作者承认没解决**。"Several experimental results identify areas to address for improved function"开头即举两例：其一 "r5-kent1 inactivates after roughly 10 turnovers"，且质谱显示稳定酰化物种，作者结论："designs that hydrolyze the AEI are still susceptible to inactivation, potentially from off-mechanism acylation events in the active site or acylation-induced conformational changes"；其二侧链 oxyanion 残基突变后效应不一致（三个设计只轻度下降）。 **应对**：只把它们写成"待改进方向"，未回到漏斗里补判据——**这两条本文没有解决**。
10. **动力学上拿到很小的 K_M，但不能当"结合紧"**。r3-win 的 K_M = 2.8 µM 但作者测不到饱和："we were unable to reach saturation of the initial burst phase of the reaction by increasing substrate concentration up to 100 µM"，据此判断真实情形是 K_s ≫ K_M，小 K_M 来自酰化快而非结合紧。 **应对**：换拟合口径——单转换用初速算 k2/K_M，有明显 burst 的用稳态直线段拟合（Methods："In cases where single-turnover activity was observed, initial velocities were used to determine k 2 / K m"）。→ 这一条对我们极重要：**同一个数字在不同机制假设下含义完全不同**。
11. **"新折叠"这件事依赖一个外部阈值，作者自己把边界写进去了**。r3-super 与 r3-win 对全部数据库的 Foldseek 最近 TM-score 是 0.52 与 0.46，而"different fold"的通行 cutoff 是 0.5；作者的措辞是 "at or below the 0.5 cutoff below which structures are considered to have different topological folds"。 **应对**：不解释 0.52 > 0.5 这一事实，改用双重表述（正文一句里同时说"very different from known structures"与"at or below"），并把结论落在"expanding the structural space of this ancient enzyme family"上。→ 本卡第 7 节把这条列为**本文最可疑的判据**。

## 3. 方法与工作流程（可复现顺序）

### 用了哪些方法（工具箱，以及各自承担什么）

- **QM/DFT（化学步建模，不做全局筛选）**：酯过渡态几何由 DFT 定——"The transition state geometry of the substrate ester group was determined by DFT geometry optimization (B3LYP-D3(BJ)/6-31G(d))"，然后"we placed the catalytic sidechains around a QM-optimized transition state"。这是 theozyme 的现代版：QM 只负责给出**目标几何**，不负责给几十万候选打分。
- **骨架生成**：RFdiffusion（围着 motif 的 N/Cα/C 骨架原子从噪声建起），后期局部重生成用 contigs 固定母体 + RFam（能对单个原子/官能团作骨架并同时在序列轴上推理位置）。
- **序列设计**：LigandMPNN ↔ Rosetta FastRelax 三回环（"Following three cycles of LigandMPNN and FastRelax, the structures of the designs were predicted with AlphaFold2"），配合两项干预：活性位 8 Å 内的残基在对数概率上**偏向极性氨基酸**；催化残基固定并全程用 Rosetta enzyme constraints 锁几何。
- **静态自洽性闸口**：AF2 单序列预测（model 4，三个 recycle）→ 全局 Cα RMSD、pLDDT、催化残基 Cα RMSD 三阈值。
- **动态/系综闸口（本文新增）**：PLACER，输入是口袋内蛋白骨架坐标 + 序列 + 小分子连接性（**不给小分子位置**），在随机化侧链与小分子坐标后重建全原子；作者给的训练与精度口径："randomizing the atomic coordinates of sidechains and small molecules within spherical regions with up to 600 heavy atoms"、"In benchmark tests, PLACER predicted regions within native structures with an average RMSD of 1.1 Å"。
- **实验侧**：FP-TAMRA 活性探针标记（在凝胶上读，判"有没有活化丝氨酸"）→ 96 深孔裂解液荧光筛选（4MU-Ac/4MU-Bu，判"有没有酯酶活性"）→ 纯化后动力学（判 acylation vs turnover）→ intact MS（判酰化质量位移）→ X 射线（判设计准确度）→ Foldseek（判折叠新颖性）。**三级实验对应三个化学事件**，这是本文漏斗结构上最值得抄的一点。
- **没有用的方法**：MD 一次没出现（本地全文检索 molecular dynamics = 0 次命中），QM/MM 只在讨论里作为他人方法被提及；作者用 PLACER 明确替代"贵而不准"的预组织评价手段。

### A. 漏斗（每一轮：输入 → 操作 → 判据/阈值 → 输出与实验结局）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与结局 |
|---|---|---|---|---|
| P0 前置战役 | 天然丝氨酸水解酶几何分析 + trRosetta 理想化 NTF2 库 | RosettaMatch 匹配 motif → LigandMPNN + FastRelax → AF2 过滤，并额外要求所有催化氢键在 AF2 预测里形成 | "An additional filter was used requiring that all catalytic hydrogen bonds in the active site be formed in the AlphaFold2 prediction" | 有活化丝氨酸、**无转换数**；该轮样本并入 812 设计统一分析（2.2 条） |
| P1 motif | 天然水解酶晶体（N 型 oxyanion 用 1scn 残基 220–222；N+1 型用 1lns 残基 347–349）+ DFT 过渡态 | 把 Ser stub、His（在 3 残基螺旋/链 stub 上）与底物按几何摆放，只保留能同时与 Ser 和离去基氧形成氢键的构象 | 几何筛（正文未给数值阈值） | "This process resulted in 108 unique motifs for design rounds 1 and 2"；round 3 因约束过强失败后改用两步搜索得 **2238** 个 motif |
| P2 骨架 | motif 的 N/Cα/C + 邻近残基 | RFdiffusion 去噪轨迹向外建骨架，并要求形成底物口袋 | 作者自述 motif 复现精度："average all-atom RMSD ~ 0.1 Å"（正文口径，逐条分布 fig. S1） | 每轮 96 孔固定送测；基因合成送测 **129（r1）/ 192（r2）** 条 |
| P3 序列 | 骨架 + 底物 | LigandMPNN ↔ FastRelax 三轮；催化残基冻结；8 Å 内极性偏向；enzyme constraints 锁氢键 | 约束容差："with tolerances of 0.1 Å for distances and 5° for angles and dihedrals" | 每条骨架出多条序列（r6/r7 局部重生成轮为 "Ten sequences were generated per backbone"） |
| P4 静态闸口 | 设计模型 | AF2 单序列预测 | "Designs were filtered for a global Cα RMSD < 1.5 Å, pLDDT > 75, and catalytic residue Cα RMSD < 1.0 Å"（另注："AF2 was run using model 4 with three recycles"；末轮 N+1 型改用带稀疏 template 的 Initial Guess AF2） | 过筛者进入 PLACER |
| P5 系综闸口 | 过 AF2 的设计 | PLACER 对 **5 个态**（apo、底物结合、TI1、AEI、TI2）各跑 **50 个种子**，统计关键氢键形成频率；r1/r2 被特意做成"活性位复杂度相同、只有筛子不同"的对照 | 裁剪口径："PLACER predictions were done for a spatial crop of 600 atoms closest to the active site"；r1 不过 PLACER；r2 只用 apo 的 Ser-His 氢键；r3 起要求 apo + AEI 两态；r4 起再做 2 态 vs 4 态两套 | r2 只有 1.6% 过 AF2 者被判预组织；r3 的 132 条送测中 111 条 FP 阳性、20 条水解、**2 条（1.5%）多轮转换** |
| P6 湿实验一级 | 裂解液 | FP-TAMRA 标记 + in-gel 荧光 | 是否被亲电探针标记（活化丝氨酸的代理） | r1 3% → r2 17%（5 倍）；r3 84%；两态过滤轮 "We obtained genes encoding 45 two-state filtered designs for experimental characterization" → 38 (84%) 标记；四态轮 10/11 (91%) |
| P7 湿实验二级 | 同上 | 4MU-Ac/4MU-Bu 荧光动力学（96 孔，mScarlet 归一） | 是否显著高于背景（酯酶活性） | r1 2 条（1.6%）、r2 10 条（5.2%）；r3 20 条（18%）；两态轮 9 条（20%）；四态轮 8 条（73%）；r5 的 20 条中 2 条有显著酯酶活性（180 与 1400 M⁻¹s⁻¹） |
| P8 湿实验三级 | 纯化蛋白 | 进度曲线 + Michaelis-Menten + intact MS + 催化残基敲除 | 是否出现 >1 酶当量的持续产物；是否有 burst；质谱是否给出酰化质量位移；突变任一催化残基是否显著降活 | r3-super / r3-win = 22 与 410 M⁻¹s⁻¹；r4 重设计 k_cat 升 15×/17×/9×；r4-dadt1 k_cat/K_M = 3800 M⁻¹s⁻¹ |
| P9 迭代提活 | 已知活性设计（r3-win、r6-momi、r3-super） | 固定母体、局部重生成（N 端 20–50 aa / 按 subtilisin 几何重建 56–91 区段）→ 重跑 P3–P5 | 同一套闸口复筛；r7 轮 65 条全部有活性；r8 轮 150 条中取最活两条 | r7-momi120 = 4,300 M⁻¹s⁻¹（3.5× r6-momi）；r8-superfast / r8-supercool 对 r3-super 分别 k_cat 8×/7×、k_cat/K_M 19×/13× |
| P10 结构确证 | 活性设计 | X 射线 + Foldseek 对全部数据库（TM-align 模式） | 设计与实验的 Cα / 全原子 RMSD；最近邻 TM-score | r3-super 0.8 Å(165 res)/0.38 Å(22 atoms 全原子)、r3-win 0.83 Å(160)/0.86 Å(20)；r4 系列 1.42/0.7/1.2 Å；最近邻 TM-score 0.52 与 0.46 |

### B. 与"90% 类叙述"有关的口径分层（本文自己就是活教材）

同一篇论文里并列着 1.6%、5.2%、18%、84%、91%、"all showed activity"与"all showed activity of 150 中 2 条最活"。差别只在**分母是谁**：过闸口数、合成基因数、FP 阳性数、还是送测数。本卡第 4 节把每个数字的分母写死，就是为了防止跨口径引用。

## 4. 关键数字台账（均可在 `serinehydrolase2025.txt` 逐字搜到）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 1.6% | round 2 过 AF2 RMSD 筛者中被 PLACER 判预组织的比例 | "Only 1.6% of round 2 designs that passed the AF2 RMSD filter were predicted to be preorganized by PLACER" |
| 129 / 192 | round 1 / 2 订购的合成基因数 | "For experimental testing, we obtained synthetic genes encoding 129 and 192 designs for rounds 1 and 2" |
| 3% → 17%（5 倍） | FP 探针标记率从 r1 到 r2 | "The fraction of designs labeled by the FP probe in E. coli lysate increased 5-fold from 3% to 17% from round 1 to round 2" |
| 2 条（1.6%）/ 10 条（5.2%） | r1 / r2 显示出催化活性的设计数（分母＝送测基因数） | "two round 1 designs (1.6%) and 10 round 2 designs (5.2%) showed catalytic activity" |
| 132 / 111（84%）/ 20（18%）/ 2（1.5%） | round 3：送测 / FP 标记 / 水解 4MU / 多轮转换 | "Of 132 round 3 designs, 111 (84%) displayed FP probe labeling, 20 hydrolyzed 4MU substrates (18%), and two designs (1.5%) displayed multiple turnover activity" |
| 45 / 38（84%）/ 9（20%） | 两态（apo+AEI）过滤轮的送测 / 标记 / 活性 | "We obtained genes encoding 45 two-state filtered designs for experimental characterization" |
| 11 / 10（91%）/ 8（73%） | 四态过滤轮的送测 / 标记 / 活性 | "Of the 11 four-state filtered designs tested, 10 (91%) labeled with FP-probe" |
| 22 与 410 M⁻¹s⁻¹；k_cat 0.00137 与 0.00117 s⁻¹；K_M 64 与 2.8 µM | r3-super 与 r3-win 的催化效率（多轮转换） | 正文 round 3 结果段 |
| 15×/17×/9× 与 0.018/0.0197/0.0105 s⁻¹ | r4-win1/r4-win11/r4-win31 对 r3-win 的 k_cat 提升 | "which increases 15-fold in r4-win1" |
| 3800 与 640 M⁻¹s⁻¹ | r4-dadt1 与 r4-wint4 的 k_cat/K_M | "Two of these, r4-dadt1 and r4-wint4 , displayed higher catalytic efficiencies than r3-win" |
| 2/20；180 与 1400 M⁻¹s⁻¹ | r5（round 3 骨架排除 r3-win 后重跑全坐标过滤）的命中与效率 | "and of 20 designs tested, two" 有显著酯酶活性 |
| 66 / 1,240 M⁻¹s⁻¹ / k_cat 0.1 s⁻¹ | N+1 oxyanion 新几何的设计数与最佳效率（r6-momi） | "We used the RFdiffusion and LigandMPNN/FastRelax design pipeline to generate 66 designs for this new catalytic site" |
| 65 / all / 4300 M⁻¹s⁻¹（3.5×） | r7 局部重生成轮的送测 / 有活性 / 最佳（r7-momi120） | "Of 65 designs tested, all showed activity" |
| 150 / 8× 与 7× / 19× 与 13× | r8 oxyanion 几何重构轮的送测与提升 | "Of the 150 designs screened, the two most active designs" |
| **812** | 被 PLACER 系综回溯分析的、已实验表征设计总数（含 NTF2 轮） | "PLACER ensembles of all 812 experimentally characterized designs, categorized as inactive, FP probe labeling, acylation, and catalytic turnover" |
| Ser-His 角 94°（活性）vs 108°（无活性）vs ~125°（PDB 常见） | 几何决定活性的直接证据 | "Ser(Oγ):His(Nε-Cε) bond angles that were more acute (median, all states = 94°)" |
| 56% / 60% / 100% vs 0% | r4-win1/r4-win31/r4-dadt1 在 AEI 态采用设计 T99 构象的比例，r3-win 从不采用 | "while r3-win never adopts this rotamer" |
| AF2 全局 Cα RMSD < 1.5 Å、pLDDT > 75、催化残基 Cα RMSD < 1.0 Å | 静态闸口三阈值 | "Designs were filtered for a global Cα RMSD < 1.5 Å, pLDDT > 75, and catalytic residue Cα RMSD < 1.0 Å" |
| crop 600 atoms、50 seeds × 5 states、model 4 + 3 recycles、约束 0.1 Å/5°、8 Å 极性偏向 | PLACER/AF2/序列设计的全部口径 | 见第 3 节 P3–P5 |
| 1.1 Å（PLACER 基准）、~0.1 Å（motif 复现全原子 RMSD） | 两个工具自身精度 | "In benchmark tests, PLACER predicted regions within native structures with an average RMSD of 1.1" |
| 108 → 2238 | round1-2 与 round3 的 motif 数（两步搜索之后） | "ultimately producing 2238 unique round 3 motifs with Ser-His-Asp/Glu catalytic triads" |
| TM-score 0.52 / 0.46，cutoff 0.5 | 折叠新颖性判据 | "the closest matches found from Foldseek searches against all available databases have TM-scores of 0.52 and 0.46" |
| 对比基准：OE1 210 M⁻¹s⁻¹ 且需 4 轮定向进化、筛 12,000 克隆才到 3190；半胱氨酸体系 3.7 M⁻¹s⁻¹ | 作者用来定位本文优势的他人数字 | "the previously designed esterase OE1 has a k cat / K m = 210 M" |
| 天然对照：乙酰胆碱酯酶 >10⁸ M⁻¹s⁻¹；α-糜蛋白酶 3530、subtilisin 610（pNPA） | 本文设计与天然的差距 | "The designs described here are not as efficient as native serine hydrolases with their cognate substrates" |
| 估计脱酰加速 >10⁸ | 用未催化乙酸乙酯水解速率（2.5–5.0×10⁻¹⁰ s⁻¹）比 r6-momi 脱酰下限 0.076 s⁻¹ | 正文讨论段（该数字是作者估算，非实测） |
| **本文未记录** | 每个闸口的 GPU/CPU 单价与总机时（PLACER 50 seeds×5 态的代价只在 [B19] 讨论） | 正文无 |

## 5. 结论——作者说了什么

1. 用 RFdiffusion 生成骨架 + PLACER 系综过滤，可以从最小活性位描述出发做出**真正的丝氨酸水解酶**（Ser-His-Asp/Glu 三元体 + oxyanion hole，含 AEI 水解这一步）："we combined the generative capabilities of RFdiffusion with a new ensemble generation method to design and filter enzymes starting from minimal active sites"。
2. 实验精度：k_cat/K_M 最高 4.3×10³ M⁻¹s⁻¹（r7-momi120 达 4300），晶体结构与设计模型高度一致（摘要口径 Cα RMSD < 1 Å），活性位全原子 RMSD 低至 0.38 Å（22 原子）。
3. 沿反应坐标的**多态一致性**选择是命中率跃升的原因，并且还能拿到天然家族里没有的 5 种折叠："Selection for structural compatibility across the reaction coordinate enabled identification of new catalysts in low-throughput screens and yielded serine hydrolases in five different folds not previously observed in this enzyme family"。
4. PLACER 的额外价值是机理归因："PLACER revealed pervasive off-target conformational changes in the acyl-enzyme intermediate, providing feedback on design flaws that would go unnoticed when considering only a single state in the catalytic cycle"。
5. 作者自限：与天然酶尚有 4–5 个数量级差距（乙酰胆碱酯酶 >10⁸）；仍有设计在约 10 轮后失活；侧链 oxyanion 的贡献在不同设计里不一致；本文讨论里明确把 QM/MM、定向进化列为**互补**手段而非被替代者。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文是我们项目里"判据该长什么样"的最强范例**：它把筛子从"一个静态结构对不对"换成"沿反应路径若干态是否都能形成若干关键相互作用"。→ 对应我们：UAA 的判据必须按 S0（游离 UTP 起始）/S1（pppUA）/S2（第二枚 ATP vs 环化）分别定义"该态里哪些键必须在"，并且要求同一候选在**所有相关态**都过关；单态通过不得计入。
2. **1.6% 与 84% 同在一篇里，是"同一实验、不同分母"的标准案例**。→ 我们所有对外数字必须写成 `分子/分母（分母是谁）`；"末端 84%"不能当"漏斗端到端能力"引用。这一条正是本调研针对"90% 类叙述"立的反例锚点（CSV `成本/统计` 字段原话）。
3. **QM 的正确用法是"定目标几何"，不是"打分器"**：DFT 只用于过渡态几何（2. 与 P1），一旦用它筛几千候选就会破产。→ 我们的 xTB/DFT 预算应压在 theozyme 级（几十个几何）而不是评价级（几百个候选）。
4. **他们没上 MD，而是造了一个更便宜的随机化网络来近似系综**。→ 对我们：与其在长时 MD 上烧核时，不如先明确"我要的判据其实是若干关键接触在各态的形成频率"，然后找/造一个能以 10⁻² 单价给出该频率的替代物（本项目里即 PLACER 直接调用，单价已在 run.md 记录）。
5. **"局部重生成"比"再筛一遍"更能提活**：r7 固定母体只重生长 N 端就 65/65 有活性，r8 借天然几何重构一个区段就拿 8×。→ 我们的漏斗末端不该只有"排序取前 N"，还该有"指定自由度重新生成 + 复筛"这一档动作。
6. **失败样本被系统性回收成阴性集**（812 设计统一 PLACER 分析，含 NTF2 那轮）——这是把失败变成判据标定材料的具体做法。→ 我们：每一轮的阴性构建体/失活突变体都应进同一张表，而不是只报活性者。
7. **K_M 的解释依赖机制假设**（2.10 条）。→ 我们：任何"亲和力/效率"读数在写出前必须先声明它假定哪一步是限速步，否则同一数字可以被两种相反结论共用。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：绝对效率仍低于天然酶数个数量级；仍有脱酰后失活（r5-kent1）与侧链 oxyanion 贡献不一致两件事未解决；本文用的是已知机制（Ser-His-Asp 三元体），只有几何与折叠是新的。
- 我们读出：① **"五种新折叠"依赖 TM-score 0.5 这个外部阈值，而 r3-super 的最近邻是 0.52**，正文用 at or below 含糊带过——新颖性主张在这一点上是**口径依赖**而非测量依赖；② **判据自身的对照是干净的**（r1 只过 AF2、r2 在 AF2 之后加 PLACER apo 态，两轮活性位复杂度相同），但 **r2→r3 有两件事一起变了**：既加了催化酸与第二对 oxyanion（motif 更复杂），又把过滤从 apo 单态升到 apo+AEI 两态；因此 r3 之后的数字（18% 水解、1.5% 多轮转换）**不能全部记在 PLACER 头上**，本文没有再补一个"复杂度相同、只换过滤态数"的轮次；③ **缺反证臂**：过 AF2 但没被 PLACER 选中的 r2 设计从未下单，所以"被 PLACER 淘汰的 98.4% 里是否真没有好设计"无法判定，判据只被证明是**富集器**而非**必要条件**；④ 每轮固定送测 129–192 条，多轮转换的绝对命中数只有个位数（2 条起步），效率跃升没有置信区间与统计口径（正文未记）；⑤ 812 设计的几何-活性关联是**回顾性**分组统计，作者措辞也只是 were associated with activity，不构成因果证明（他们靠催化残基敲除与后续按几何重设计部分佐证）；⑥ 文中出现**两个 1.6% 且分母不同**（"Only 1.6% of round 2 designs that passed the AF2 RMSD filter"是占过 AF2 者；"two round 1 designs (1.6%)"是占 129 条送测者），引用时极易串味。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **多态预组织闸口的形式**：照 "we required all catalytic triad and oxyanion hole H-bonds to be highly preorganized in PLACER ensembles of both the apo and AEI states" 的写法，把我们的闸口写成"在 S0/S1/S2 各自的系综里，指定氢键/接触的形成频率 > 阈值"；频率口径 = 关键氢键在 50 帧里的出现次数（本文算法层可原样借用：crop 内随机化侧链、多 seed、统计接触频率）。
2. **三级湿实验对应三个化学事件**（FP 标记 = 活化亲核体；底物荧光 = 转化；进度曲线/质谱 = 是否真的 turnover）。→ 我们的等价三级：① 酶+底物能否形成共价/加成物（质谱质量位移）；② 目标产物是否生成（LC-MS/MS 定量）；③ 是否多轮（时间线性 + 酶量稀释检验）。**只有第③级能证明催化**，第①②级只能算"活性位可用"。
3. **口径纪律**：每个百分数带分母；漏斗表里"过闸口数"与"下单数"与"有读数数"分列。
4. **局部重生成作为优化动作**：固定已验证主体、只在指定自由度上再生成（本文 contigs 写法可直接借给 RFdiffusion2/3 调用脚本）。
5. **阴性集回收**：把无活性/失活样本纳入同一判据标定表（本文 812 的做法）。
6. **QM 的正确位置**：theozyme 级几何（少量）而非评价级打分（海量）。

**不可迁移（为什么不能照搬）**

1. **本文的 1.6% / 5.2% / 18% / 84% / 91% 全是"酯水解这一类反应"的数**，底物是小荧光酯、反应是两电子酰基转移，与氨酰-tRNA 合成酶三步化学（含焦磷酸释放、环化竞争）没有映射关系。**禁止**把其中任何数当 UAA 场景的先验概率或成功率引用。
2. **oxyanion hole / Ser-His 氢键这些"关键接触"是本文人工指定的**（来自天然机制知识）；UAA 场景里我们尚无等价的"公认必须接触集"，因此判据必须先由机制推导出接触清单，才能套本文管线——顺序不能反过来。
3. **PLACER 的 1.1 Å 基准精度是在 PDB 蛋白-小分子复合物上测的**，它保证的是"重建口袋原子坐标"的准确度，不是"预测催化能力"的准确度；本文的催化结论来自湿实验，PLACER 只提供排序与归因。不得据此声称"PLACER 能判活性"。
4. **没有 MD、没有速率理论**：本文不产生任何"从构象系综算 kcat"的路径，因此不能用来支持"MD/自由能可以定量预测酶活"这类主张（它支持的只是"系综频率可作为便宜的排序筛"）。

## 9. 溯源与自检

- 引句底稿: data/interim/baker_lit/ft/serinehydrolase2025.txt —— 本卡全部英文引句以此为唯一逐字比对对象（该编号在 `sources_map.json` 里登记的其余底稿只有 `sources/baker.md`）。
- 检索记录（本卡第 0 节 `md_used` 证据）：在该全文的归一化文本里检索字符串 molecular dynamics，**0 次命中**（同一次检索里 MD 相关的其他拼法也未出现）；因此 CSV `是否用MD=否` 有文本级依据，不是推断。
- 对照底稿行号：`sources/baker.md:224–236`；跨论文对照表：`sources/baker.md:607`（3c 活性位预组织：PLACER + QM theozyme 输入）、`sources/baker.md:612`（6 确证）、`sources/baker.md:646`（酶专用判据段，含 1.6% 与 45→38=84%）、`sources/baker.md:662`（QM 角色＝化学步建模）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本/统计`；第 8 节 ↔ `在方法演进链的位置`。
- 本卡自检：`scripts/verify_literature_cards.py --only B17 --no-report`。写卡过程中门禁第一轮判 FAIL 的唯一原因是本卡没有按新版核验器要求声明引句底稿（缺少带路径的 引句底稿 一行）；补上后另有两条被判不逐字的片段，经核对**是第 9 节里用来解释修改过程的说明性英文片段被门禁当作了逐字引句**（它们不是原文），已去掉其直双引号；正文引句本身全部为复制粘贴。复跑结果见对话回报。
- 未取回内容（已在正文相应位置声明）：Supplementary/Computational methods 的 CA diffusion 参数、fig. S1 每轮设计数流程图、fig. S5–S17 逐条数值、PLACER 与 AF2 的算力开销。

<!--CSV回填
work_type=论文
target=4-甲基伞形酮（4MU）酯水解（4MU-Ac/4MU-Bu/4MU-PhAc），丝氨酸水解酶机制：Ser-His-Asp/Glu 催化三元体 + 主链与侧链 oxyanion hole，含 acyl-enzyme intermediate（AEI）水解这一步
backbone_generation=RFdiffusion 围绕活性位 motif 从噪声建骨架（motif 由 DFT 过渡态几何 + 天然水解酶晶体 stub 采样得到；round3 改为两步搜索）；后期用 contigs 固定母体只重生成局部（N 端 20-50 aa / RFam 按 subtilisin 几何重建 56-91 区段）；序列端 LigandMPNN ↔ Rosetta FastRelax 三回环
computational_filters=静态闸口 AF2 单序列预测（model 4，3 recycles）：全局 Cα RMSD、pLDDT、催化残基 Cα RMSD；FastRelax 后 motif 几何复现 + Rosetta 底物形状互补；系综闸口 PLACER（50 seeds × 5 个反应态，600 原子裁剪）统计关键氢键形成频率（r2 用 apo 的 Ser-His 氢键；r3 起 apo+AEI 两态；再做 2 态 vs 4 态两套）；Rosetta enzyme constraints 全程锁催化几何
thresholds=AF2 全局 Cα RMSD<1.5 Å、pLDDT>75、催化残基 Cα RMSD<1.0 Å；enzyme constraints 距离容差 0.1 Å、角度/二面角容差 5°；LigandMPNN 对活性位 8 Å 内残基偏向极性氨基酸；PLACER 裁剪 600 原子、每态 50 个种子、5 个态；motif 复现全原子 RMSD ~0.1 Å；PLACER 自身基准 1.1 Å；DFT = B3LYP-D3(BJ)/6-31G(d)；折叠新颖性用 Foldseek TM-score cutoff 0.5
md_used=否（全文检索 molecular dynamics 零命中；作者用 PLACER 构象系综替代"贵而不准"的预组织评价手段，未把 MD 放进漏斗）
qm_used=是-化学步（仅用于确定底物酯过渡态几何并据此摆放催化侧链：DFT B3LYP-D3(BJ)/6-31G(d)，"placed the catalytic sidechains around a QM-optimized transition state"；QM 不承担候选打分或自由能排序）
experimental_methods=E. coli 表达 → FP-TAMRA 活性探针 in-gel 荧光（活化丝氨酸）→ 96 深孔裂解液 4MU 荧光筛选（酯酶活性）→ 纯化蛋白动力学（初速 k2/K_M、稳态 kcat/K_M）+ intact LC-MS（酰化质量位移）+ 催化残基/二级壳突变对照 → X 射线晶体（6 个结构，PDB 9DED/9DEE/9DEF/9DEG/9DEH/9MRB）→ Foldseek 折叠新颖性
pipeline_counts=NTF2 前置轮：有活化丝氨酸、零转换；r1 129 送测 → 2 活性（1.6%）；r2 192 → 10（5.2%），且过 AF2 者仅 1.6% 过 PLACER；r3 132 → 111 FP（84%）→ 20 水解（18%）→ 2 多轮转换（1.5%）；两态过滤 45 → 38 FP（84%）→ 9 活性（20%）→ 3 条 k_cat 提升；四态过滤 11 → 10 FP（91%）→ 8 活性（73%）→ 2 条效率更高；r5 20 → 2；N+1 新几何 66 → r6-momi；r7 局部重生成 65 → 全部有活性 → 最佳 4300 M⁻¹s⁻¹；r8 150 → 最优 8×/7× k_cat；PLACER 回溯分析总计 812 个已表征设计
hit_rate=端到端 1.6%（r1）→ 5.2%（r2）→ 1.5% 多轮转换（r3）；末端"过全部闸口后送测者"的标记率 84%/91%、活性率 20%/73%、r7 轮 65/65 全部有活性；作者未给统一成功率，也未给置信区间
best_metric=k_cat/K_M = 4300 M⁻¹s⁻¹（r7-momi120；r6-momi 1240 M⁻¹s⁻¹、k_cat 0.1 s⁻¹；r4-dadt1 3800 M⁻¹s⁻¹）；结构最佳：r3-super 活性位全原子 RMSD 0.38 Å（22 原子）、Cα 0.8 Å（165 残基）
cost_or_stat_note=同一篇里 1.6%/5.2%（占送测基因）与 84%/91%/20%/73%（占各闸口通过者）并列——这就是"90% 类数字"的产生机制，引用必须带分母；正文未记录 PLACER 50 seeds×5 态与 AF2 过滤的机时单价；动力学部分未给统计功效或置信区间；对照他人数字：OE1 需 4 轮定向进化筛 12,000 克隆才达 3190 M⁻¹s⁻¹
role_in_timeline=酶设计第一次"零到零"跑通多步机制（含 AEI 水解）并拓出天然家族外的 5 种折叠；杠杆是把漏斗判据从"静态结构自洽"（B09 型 pAE/ipTM）换成"沿反应坐标的构象系综预组织"，同时把 QM 限定在 theozyme 几何、把 MD 排除在筛子之外；其口径分层（端到端 vs 末端）成为本项目反"90% 叙述"的锚点文献
source_pointer=data/interim/baker_lit/ft/serinehydrolase2025.txt；sources/baker.md:224-236、607、612、646、662
CSV回填-->
