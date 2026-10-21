# [B08] RFdiffusion——把折叠网络反过来当生成器用，一个模型覆盖折叠/对称/位点/金属位/结合体五类设计（Baker 组，Nature 2023）

Watson J L, Juergens D, Bennett N R, Trippe B L, Yim J, Eisenach H E, Ahern W, Borst A J, Ragotte R J, Milles L F, … Baek M, Baker D（华盛顿大学 IPD + MIT + Columbia + Cambridge + ENS）
Nature 2023, 620:1089–1100 · DOI 10.1038/s41586-023-06415-8 · PMID 37433327 · PMCID PMC10468394
开放获取（CC BY 4.0）· 全文链接 https://pmc.ncbi.nlm.nih.gov/articles/PMC10468394/ · 代码 https://github.com/RosettaCommons/RFdiffusion

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B08**（组：Baker组; 通用方法学; 口径对照） |
| 本文取回方式 | Europe PMC fullTextXML：`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10468394/fullTextXML`（`data/literature_cards/inventory.json` 中 B08 的 `fetch_channel=epmc_fulltext`） |
| 本地全文 | `data/interim/baker_lit/ft/rfdiffusion2023.txt`（93,810 B，去标签纯文本，SHA-256 `2aa635bf84a95987…`，文件 mtime 2026-10-16 19:16）；登记于 `data/literature_cards/sources_map.json` 的 B08 项（另一登记底稿 `sources/baker.md`） |
| 对照底稿 | `sources/baker.md` 第 107–118 行（原卡）。本卡在其基础上补：训练/推断机制细节（去噪表示、m.s.e. loss、self-conditioning、200 步与早停/步长消融）、三套 in silico 成功判据的**不同口径**、25 题 benchmark 的构成与对照方法、对称设计的接触外部势、金属位 H52A 失活对照、MDM2 一批的**正文 96 / 图注 95 不一致**、noise scale 与多样性的权衡 |
| 证据级别 | **全文级**（本卡所有英文引句均可在本地全文里逐字命中；见第 9 节自检） |
| 未取到的部分 | 这份本地文本只含**正文 + 主图/扩展图图注**：独立的 Methods 章节、Supplementary Methods、Supplementary Table 1/9/10 的内容、Extended Data Table 1 的数值、原图与 Source Data 都不在其中。凡涉及微调数据量、训练超参、外部势的具体函数形式、SEC/CD 原始曲线的地方，本卡明写"正文未给出，只指向 Supplementary Methods"（正文与图注里出现的 Supplementary Methods 指针共 10+ 处，例如 "see Supplementary Methods 4.4"）。 |

## 1. 这篇到底解决什么（大白话）

在此之前，深度学习做蛋白设计是**一个问题配一个方法**：想生成新折叠用 Hallucination（在序列空间做 Monte Carlo/梯度搜索，慢、只能到约 100 残基），想在已有骨架里补一段用 RF joint Inpainting（单步、确定性，起点信息给少了就崩，且对同一问题只能给出很有限的多样性），想做结合蛋白还是靠 Rosetta 物理打分（要预先指定一批 scaffold 骨架，界面形状互补受限，命中率低到每靶要筛上千到几万条）。这篇做的事：把已经会折叠蛋白的 RoseTTAFold 网络**改造成去噪生成器**——训练时给它加了噪声的骨架让它还原，推理时从纯随机噪声一步步"还原"出一个从未存在过的骨架；再用不同的输入条件把同一个模型指向不同任务（不给条件=新折叠；给二级结构/block adjacency=指定 fold；给点群对称=对称寡聚体；给界面热点残基=定点结合体；给 motif 三维坐标=功能位点支架；再加外部势=把底物体积隐式挤出口袋）。骨架出来后用 ProteinMPNN 出序列、AF2 单序列复折做计算闸口，湿实验端刻意**不走展示库**：每靶只表达不到一百个设计，用单点 BLI 判阳。结果是把结合体的实验成功率抬到 19%（作者称比他们旧 Rosetta 战役高约两个数量级），并拿下一个 2.9 Å 的冷冻电镜结构证明设计模型和真实结构几乎重合（binder 单体偏差 0.6 Å）。

一句话：**它把"设计"从"在既有骨架库里搜索"变成"按规格直接生成"，并且第一次让一个模型同时覆盖五类设计问题。**

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **蛋白扩散模型此前做不成，因为分布学不出来**。作者开篇就把前史写成失败案例："Diffusion models 10 , 11 have had considerable success in image and language generative modelling but limited success when applied to protein modelling, probably due to the complexity of protein backbone geometry and sequence–structure relationships"。 → **他们做了什么**：不从零训，而是把已会折叠的 RoseTTAFold 权重**微调**成去噪网络，并采用 RF 的残基 frame 表示（每残基一个 Cα 坐标 + N-Cα-C 刚性朝向），平移用 3D 高斯噪声、朝向用旋转矩阵流形上的布朗运动加噪（"We generate training inputs by noising structures sampled from the Protein Data Bank (PDB) for up to 200 steps"）。这个选择被消融实验钉死："Fine-tuning RFdiffusion from pretrained RF weights was far more successful than training for an equivalent length of time from untrained weights"，图注更直白："Without pre-training (at least when trained with equivalent compute), RFdiffusion outputs bear little resemblance to proteins"（等价算力下无预训练的 in silico 成功率为零，两比例 z 检验 z=23.0、p=3.1e-117）。 → **代价**：模型能力被绑死在 RF 权重和 PDB 分布上；"probably due to the complexity of protein backbone geometry" 只是作者的猜测，机制没有被证明。
2. **轨迹前一步信息被丢掉，输出没有核心堆积**。canonical 扩散每步预测彼此独立。 → **他们做了什么**：借 AF2/RF 的 recycling 思路引入 self-conditioning，让模型看见上一步的去噪预测（图注把它当 template 输入）；实测 "Self-conditioning within RFdiffusion notably improved performance on in silico benchmarks encompassing both conditional and unconditional protein design tasks"，失败形态也被刻画："Without self-conditioning, outputs show characteristic protein secondary structures, but lack core-packing and ideality"。 → **代价**：他们只说轨迹连贯性提升 "may, at least in part, explain these performance increases"——归因是假设而非结论。
3. **用结构预测原本的 FAPE loss 训生成器，无条件生成会崩**。 → **他们做了什么**：换成对 frame 的 m.s.e. loss，理由是它不平移不变、因此强制了步与步之间全局坐标系连续："unlike FAPE, m.s.e. loss is not invariant to the global reference frame and therefore promotes continuity of the global coordinate frame between timesteps"；图注给结论："The MSE loss is not invariant to the global coordinate frame, unlike FAPE loss, and is required for good performance at unconditional generation"。 → **代价（他们自己把这个判据的普适性削掉了）**：一旦有 motif 锚定坐标系，换 loss 就不重要了——"For motif scaffolding problems, where the ‘motif’ provides a means to align the global coordinate frame between timesteps, FAPE loss performs approximately as well as MSE loss"。即这是**工程 trick，不是物理定律**。
4. **单步确定性补全（RF joint Inpainting）既给不出多样性也接不了极简 specification**。原文自陈前作局限："the approach fails on minimalist site descriptions that do not sufficiently constrain the overall fold" 且 "because it is deterministic, can produce only a limited diversity of designs for a given problem"。 → **他们做了什么**：把问题改成多轨迹生成——"because the starting point is random noise, each denoising trajectory yields a different solution"，靠反复去噪逐步长结构，所以几乎不需要起点结构信息。 → **代价**：推理要跑很多步（默认 200），单条设计成本远高于单步补全；于是才有了第 2.9 条的加速与取舍。
5. **对称组装体：模型没在对称数据上训练过，而高阶对称在 PDB 里又稀少**。他们先承认对手方法在这里直接失败："this approach fails for higher-order dihedral, tetrahedral, octahedral and icosahedral symmetries, probably in part because of the much lower representation of such structures in the PDB"。 → **他们做了什么**（三招同时上）：①推理端按指定点群把单体随机 frame 复制 n−1 份再整体去噪（"we generate random starting residue frames for a single monomer subunit as in the unconditional generation case, and then generate n − 1 copies of this starting point arranged with the specified point group symmetry"）；②每步显式重新对称化，实测对结构影响很小（"we explicitly resymmetrize at each step but this changes the structures only slightly"）；③加链间/链内接触外部势——"particularly when guided by an auxiliary inter- and intrachain contact potential"；④对八面体/二十面体只显式建模能生成整体的最小子集以压显存（"For octahedral and icosahedral architectures, we explicitly model only the smallest subset of monomers required to generate the full assembly"）。最终结果："Despite not being trained on symmetric inputs, RFdiffusion is able to generate symmetric oligomers with high in silico success rates"。 → **代价**：小于 nsEM 分辨能力的组装体拿不到结构级证据——"Although the D2 dihedrals are too small for nsEM"，D2 那一类只有 SEC 分子量这一条弱证据。
6. **超过 400 残基的设计，AF2/ESMFold 的单序列预测本身就不可信，等于闸口失效**。原文明写："RFdiffusion generates plausible structures for even very large proteins, but these are difficult to validate in silico as they are probably generally beyond the single sequence prediction capabilities of AF2 and ESMFold"（扩展图注同样把高置信区间划在约 400 aa 以内）。 → **他们做了什么**：把验证从计算侧搬到结构侧——对大组装体用 negative stain EM 的 2D class averages 与 3D reconstruction 比对设计模型（"with 350 residue subunits (1,050 residues in total) suggests that the actual structure is very close to the design"），并用 SEC 校准曲线给出置信区间的定量口径；同时对折叠条件设计补 ESMFold 作为 AF2 的**正交**置信度（口径：pLDDT>80）。 → **代价**：通量骤降（电镜是逐颗粒的），且这类确证只在少数个例上做成；C3/C5/C6/D3/D4/二十面体的确证样本各是 1 个级别。
7. **要设计酶位点，但当时的网络不能显式建模小分子/底物**。作者直说："Although RFdiffusion is unable to explicitly model bound small molecules at present"。 → **他们做了什么**：不解决建模问题，而是**绕过去**——加一个既有排斥场又有吸引场的外部势，把底物体积隐式挤出来（"the substrate can be implicitly modelled using an external potential to guide the generation of ‘pockets’ around the active site"），并把失败拆成两个能数的模式："designs often fall into two failure modes: (1) no pocket, and (2) clashes with the substrate"；加势后催化三残基主要落在部分埋藏、形状互补的凹口袋里。判据也定成可搜的硬数：clash = 底物 3 Å 内有骨架 Cα，pocket = 无 clash 且 3–8 Å 内有超过 16 个 Cα。 → **代价（他们自陈的）**：这套定义只看骨架不看侧链——"Note that the potential and clash definition pertain only to backbone Cα atoms, and do not currently include sidechain atoms"；且这条线全程停在 in silico，**没有任何酶活数字**，势的函数形式与参数也只写"详见 Supplementary Methods 4.4"。
8. **结合体一侧的老瓶颈：物理法要预置骨架库、每靶要筛几千到几万条**。原文对前作的判词："However, experimental success rates were low, still requiring many thousands of designs to be screened for each design campaign 12 , and the approach relied on prespecifying a particular set of protein scaffolds as the basis for the designs, inherently limiting the diversity and shape complementarity of possible solutions"，并补一句当时状态："To our knowledge, no deep-learning method has yet demonstrated experimental general success in designing completely de novo binders"。 → **他们做了什么**：①在靶的上下文里直接生成 binder，并微调复合物模型 + 输入界面热点残基来做定点结合；②接受"筛选端已被 [B09] 换成 AF2 置信度"这一事实，直接沿用："Designs were filtered by AF2 confidence in the interface and monomer structure 26 , and 95 were selected for each target for experimental characterization"；③试过再插一道 Rosetta FastRelax 回环，**发现没用就砍掉**："In line with current best practice 26 , we tested using Rosetta FastRelax 58 before designing the sequence with ProteinMPNN, but found that this did not systematically improve designs"；④放弃展示库，改 E. coli 小批量表达 + 单点 BLI。 → **代价**：19% 这个成功率被作者标注为保守下界（"this is a conservative estimate as some designs that showed binding had insufficient material to permit screening at 10 μM"），图注里还专门用色相标出那些**没测到 10 μM、可能是假阴**的设计；特异性只做到同位竞争，"further work is required to fully characterize proteome-wide specificity"。
9. **提高成功率的手段和这篇的卖点是冲突的**。把推理时噪声尺度调小能提成功率："Reducing the noise scale improves the in silico design success rates"，benchmark 上也有 17/23 题如此（"In 17 out of 23 of the problems, RFdiffusion-generated successful solutions with higher in silico success rates when noise was not added during the reverse diffusion trajectories"）——但作者紧接着写明这是交易："This comes at the expense of diversity, with the number of unique clusters at a TM-score cutoff of 0.6 reduced when noise is reduced"。同样，200 步可以砍到 15 步或提前停在 50–75 步来省钱，但难问题（无条件 300 aa）必须取中间值："For harder problems (e.g. unconditional 300 amino acids), one must strike an intermediate number of total timesteps (e.g., T = 50) for optimal compute efficiency"。 → **应对方式**：把噪声尺度与步数当成**按问题难度显式调的旋钮**，并声明主文其余分析统一用 200 步（"Note that for all other analyses in the paper, 200 inference steps were used, in line with how RFdiffusion is trained"）以便比较。 → **代价**：论文报的很多 in silico 成功率是在调低噪声/加势的**最优旋钮位**上取得的，与"多样性/新颖度"不能同时最大化。
10. **本文未解决的一处：同一批设计的实验分母在正文与图注里不一致**。MDM2 那一批，正文写"generate 96 designs scaffolding this helix"、"out of the 96 designs, 55 showed some detectable binding at 10 μM"，而 Fig. 4e 图注写"Out of 95 designs, 55 showed binding to MDM2 (more than 50% of maximum response)"。分子 55 一致、分母 96 与 95 不一致，**正文与图注都没有解释**。本卡按"本文未解决"处理，台账里两个数都记。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么是它）

- **生成器：RFdiffusion**。RoseTTAFold（更新版权重）微调成的去噪扩散模型，工作在残基 frame 表示上（"using the RF frame representation that comprises a Cα coordinate and N-Cα-C rigid orientation for each residue"），训练目标是 frame 预测与真结构之间的 m.s.e.（不做对齐），推理默认 200 步反向扩散。条件通道共 5 类：无（新折叠）／二级结构 + block adjacency（指定 fold）／点群对称 + 链数（对称寡聚体）／界面热点残基（定点 binder）／motif 三维坐标（功能位点支架，含侧链，训练与推理都输入：'we input motifs as 3D coordinates (including sequence and sidechains) both during conditional training and inference, and build scaffolds that hold the motif atomic coordinates in place'）。
- **外部势（只在需要时加）**：链间接触势（把链推到一起）、链内接触势（让链更球状）用于对称设计；底物隐式势（排斥 + 吸引场）用于口袋生成。它们在轨迹上作用于坐标，不改模型权重。
- **序列设计：ProteinMPNN**，"typically sampling eight sequences per design in line with previous work"；对称寡聚体那批的 in silico 口径注明是每个骨架采 16 条序列；消融图注里单体分析用 best of 8。他们试过结构+序列同时生成，实测够用就没继续（"but given the excellent performance of combining ProteinMPNN with the diffusion of structure alone, we did not extensively explore this possibility"）。
- **计算闸口：AF2 单序列复折（+ ESMFold 正交）**，取 mean pAE / mean pLDDT / 设计-预测 backbone r.m.s.d. / 界面 pAE，新颖度用 TM-score 到 PDB。**注意本文的 in silico 成功判据不是一套，而是按任务线各有一套**（见下表 W4/W5/W6/W7/W8/W11），这是引用这篇时必须指名口径的原因。
- **实验侧**：E. coli 可溶表达 + SEC（用校准曲线给 95%/99% 置信区间）+ CD 谱与熔曲线（热稳定性到 95 °C）+ nsEM/cryo-EM（2D class averages、3D reconstruction）+ 单点 BLI（10 μM，阳性对照响应的 50% 为判阳线）+ BLI 滴定投 K_D + ITC（金属位，含 H52A 失活对照）+ 竞争 BLI（位点特异性）。
- **没有用的方法**：MD、QM/电子结构、自由能微扰、酵母/噬菌体展示库。Ni²⁺ 位只给理想配位几何与实测 K_D，没有任何量子化学配位能计算；binder 完全绕开展示库。

### 主工作流（生成 → 出序列 → 计算闸口 → 湿实验 → 结构确证）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | PDB 实验结构 | 训练：对 Cα 加 3D 高斯平移噪声、对残基朝向加流形布朗旋转噪声，最多 200 步；以 m.s.e.（非 FAPE）为损失做微调；可选 self-conditioning | 无实验阈值（200 步为训练设定） | 去噪生成模型（含针对 fold／复合物／最小位点 specification 的多个微调版本） |
| W2 | 随机残基 frame（或指定条件） | 反向扩散采样；推理步数可 200 → 砍到 15 步或早停 50–75；噪声尺度可乘 0.5 或 0 | 无生成期阈值；效率口径按 in silico 成功率/单位算力 | 单体 100–600 aa；例：100 aa 在 NVIDIA A4000 上 15 步约 11 s、in silico 成功率 >60%（对照：RF Hallucination 同样 100 残基约 8.5 min） |
| W3 | W2 的骨架 | ProteinMPNN 出序列 | 无阈值 | 常规 8 条序列/骨架；对称寡聚体口径为 16 条/骨架 |
| W4 | 序列 → AF2（ESMFold 作正交） | 单序列复折，与设计模型比 | mean pAE < 5；全局 backbone r.m.s.d. < 2 Å；被支架位点 backbone r.m.s.d. < 1 Å | 论文所有 in silico benchmark 的统一口径；作者称该口径与实验成功相关 |
| W5 | 指定 fold 的 1D/2D 输入（二级结构 + block adjacency） | fold-conditioned 微调模型生成 | W4 指标 + TM-score vs 参考 fold > 0.5（TIM 对 6WVS、NTF2 对 1GY6）；ESMFold 侧用 pLDDT > 80 | in silico 成功率：TIM barrel 42.5%、NTF2 54.1% |
| W6 | 点群对称 + 链数 n + 单体长度 | 单体随机 frame 复制 n−1 份、整体去噪、每步 resymmetrize、加链间/链内接触势 | mean pLDDT > 80 且整个寡聚体 backbone r.m.s.d.（AF2 vs 设计）< 2 Å | C3–C12（含 C5/C6/C8/C10/C12）、D2/D3/D4、12 链四面体 HE0964；48 个二十面体进入验证；八面体/二十面体只建模最小子集；608 个设计进入 SEC |
| W7 | 25 个 motif-scaffolding 题（取自 6 篇近作，Supplementary Table 9） | 每题生成 100 个设计，输入 motif 三维坐标；对比 Hallucination 与 RF joint Inpainting | design r.m.s.d. < 2 Å、native motif r.m.s.d. < 1 Å、pAE < 5 | RFdiffusion 解 23/25（Hallucination 15、Inpainting 19）；所解 23 题中 19 题成功率高于两个对手 |
| W8 | 催化位点 + 底物（EC1–5、逆醛醇酶三残基） | 加底物隐式外部势生成；先过严格 in silico 口径再统计口袋 | clash：底物 3 Å 内有骨架 Cα；pocket：无 clash 且 3–8 Å 内 > 16 个 Cα | 加势与不加势两组 n = 71/51；EC2–EC5 各位点均产出 in silico 成功设计（设计侧 backbone 偏差 0.78–0.93 Å、pAE 3.3–4.6） |
| W9 | p53 螺旋 + MDM2 | 复合物微调模型在有靶的情况下支架 p53 螺旋，让额外界面接触自由长出 | 单点 BLI 10 μM，响应 ≥ 50% 最大阳性对照 | 生成 96 个（Fig. 4e 图注口径 95）；55 个检出结合，其中 32 个为单体；最佳 K_D 0.5 与 0.7 nM（天然 p53 肽 600 nM） |
| W10 | 方形平面 4×His 理想配位几何 + C4 对称 | 对称 + motif 双条件生成 Ni²⁺ 结合四聚体 | AF2 backbone r.m.s.d. < 1.0 Å 且组氨酸几何近理想 | 44 表达 → 37 个 SEC 与目标寡聚态相符 → 36 个做 ITC → 18 个结合 Ni²⁺（K_D 低 nM 到低 μM；NiB1.17 K_D < 20 nM、计量比 1:4）；H52A 在 17/17 例中消除或显著削弱结合 |
| W11 | 5 个靶（H1 HA、IL-7Rα、InsR、PD-L1、TrkA）+ 界面热点残基 | 复合物微调模型在靶上下文中直接生成 binder；可同时条件 fold 信息 | AF2 界面与单体置信度筛（沿用 [B09] 口径：monomer pLDDT > 80、interaction pAE < 10、monomer vs 设计 r.m.s.d. < 1 Å） | 每靶筛后**选 95 个**送测（合计约 475）；FastRelax 回环经实测无系统提升而被去掉 |
| W12 | W11 送测集合 | E. coli 表达纯化 + 单点 BLI（10 μM） | 响应 ≥ 50% 阳性对照记为结合 | 5/5 靶都有结合体；总体实验成功率 **19%**；对 4 个靶比原 Rosetta 战役高约两个数量级；HA 与 IL-7Rα 最佳约 30 nM（无再优化） |
| W13 | 命中的 binder / 寡聚体 | nsEM 与 cryo-EM 结构确证；SEC 校准曲线统计 | 2D class averages / 3D reconstruction 与设计模型一致；复合物分辨率 | HA/HA_20 复合物 2.9 Å map，复合物 r.m.s.d. 0.63 Å、binder 单体 0.6 Å；C3(350 aa×3)、C5/C6(>750 aa)、D3/D4、二十面体 HE0902（15 nm）各获电镜证据 |
| W14 | 命中 binder 与金属位设计 | 正交/机理性对照：竞争 BLI、位点突变、溶解态复核 | 与已验证阳性对照竞争同一位点；H52A 丧失结合但仍可溶且寡聚态不变 | 6/6 高亲和 IL-7Rα binder 竞争成功；20 个 H52A 突变体保持可溶与目标寡聚态（其中 18 个的野生型确定结合镍） |

**这套流程的组织方式值得单独记住**：一条**统一生成通道**（W1–W3）+ **按任务分别定义的 in silico 闸口**（W4–W8、W11 阈值各不相同）+ **末端小批量湿实验**（W9/W10/W12，每批 <100 个）+ **结构级确证回灌**（W13/W14）。它的省法不在"算得快"（200 步不便宜，靠步长与早停换），而在**把送测数从千/万压到几十**。


## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 200 步 | 训练加噪与默认推理步数 | "We generate training inputs by noising structures sampled from the Protein Data Bank (PDB) for up to 200 steps" |
| 8 / 16 条 | 每个骨架 ProteinMPNN 采样序列数（单体常规 / 对称寡聚体口径） | "typically sampling eight sequences per design in line with previous work"；"Note that 16 sequences per RFdiffusion design were sampled" |
| pAE<5 + 2 Å + 1 Å | 主文统一 in silico 成功口径 | "define an in silico ‘success’ as an RFdiffusion output for which the AF2 structure predicted from a single sequence is (1) of high confidence (mean predicted aligned error (pAE), less than five), (2) globally within a 2 Å backbone root mean-squared deviation (r.m.s.d.) of the designed structure and (3) within 1 Å backbone r.m.s.d. on any scaffolded functional site" |
| ~400 aa / 600 aa | AF2 单序列高置信的范围上限 / 可生成长度 | "with high confidence ( A ) for proteins up to approximately 400 amino acids in length"；"RFdiffusion readily generates diverse unconditional designs up to 600 residues in length" |
| 11 s vs 8.5 min | 100 残基骨架生成耗时（RFdiffusion vs RF Hallucination） | "a 100-residue protein can be generated in as little as 11 s on an NVIDIA RTX A4000 Graphical Processing Unit, in contrast to RF Hallucination, which takes around 8.5 min" |
| 15 步、~11 s、>60% | 缩短轨迹后的吞吐与 in silico 成功率（100 aa） | "for example, on an NVIDIA A4000 GPU, 100 amino acid designs can be generated with 15 steps, in ~11s, with an in silico success rate of over 60%" |
| T=50（可早停 50–75） | 难问题的最优推理步数折中 | "For harder problems (e.g. unconditional 300 amino acids), one must strike an intermediate number of total timesteps (e.g., T = 50) for optimal compute efficiency" |
| 42.5% / 54.1% | TIM barrel / NTF2 的 fold-conditioned in silico 成功率 | "In silico success rates were 42.5 and 54.1% for TIM barrels and NTF2 folds, respectively" |
| 18 → 9 | 无条件设计送测数 → 表达数（4 个 200 aa + 14 个 300 aa） | "9/18 designs expressed, with a major peak at the expected elution volume" |
| 11 → 10 → 8 | TIM 设计纯化 → 可溶单体 → CD 可分析 | "11 TIM barrel designs were purified alongside the 6WVS positive control"；"Ten of these express and elute predominantly as monomers"；"Eight designs expressed sufficiently for analysis by circular dichroism" |
| 95 °C | CD 熔曲线仍保持折叠（热稳定性） | "In all cases, proteins remain well folded even at 95 °C" |
| 608 → ≥87 / 126 | 对称设计送 SEC → 寡聚态与设计相符（95% / 99% 置信区间） | "We selected 608 designs for experimental characterization and found using size-exclusion chromatography (SEC) that at least 87 had oligomerization states closely consistent with the design models"；"within the 95% confidence interval, 126 designs within the 99% confidence interval, as determined by SEC calibration curves" |
| 38 / 7 / 3 | D2 / D3 / D4 中分子量符合设计的个数 | "SEC characterization indicated that 38 D2, seven D3 and three D4 designs had the expected molecular weights" |
| 48 → 1 | 二十面体送验证数 → nsEM 均一颗粒数（HE0902，15 nm） | "Forty-eight icosahedra were selected for experimental validation, and one, HE0902, a 15 nm (diameter) highly porous assembly" |
| 0.47 / 0.43；median 0.72 / 0.50 | C8、C10 桶状组装到 PDB 的最近 TM align；单体 vs 整体对 PDB 的 TM-score 中位 | "closest TM align in PDB 6BRP , 0.47, and PDB 6BRO , 0.43, respectively"；"While the monomers (typically 60–100 AA) show reasonable alignment to the PDB (median 0.72), the whole oligomeric assemblies showed little resemblance to the PDB (median 0.50)" |
| 25 题 → 23 / 15 / 19 | benchmark 解题数：RFdiffusion / Hallucination / RF joint Inpainting | "RFdiffusion solves 23 of the 25 benchmark problems, compared to 15 for Hallucination and 19 for RF joint Inpainting" |
| 100 设计/题 | benchmark 每题采样量（无预先调参） | "One hundred designs were generated per problem, with no previous optimization on the benchmark set" |
| 96（正文）与 95（图注）→ 55 → 32 | MDM2 一批：生成/送测 → 检出结合 → 其中单体 | "The overall success rate was quite high: out of the 96 designs, 55 showed some detectable binding at 10 μM"；"Out of 95 designs, 55 showed binding to MDM2 (more than 50% of maximum response)"；"Thirty-two of these were monomeric" |
| 0.5 / 0.7 nM vs 600 nM | 两个 MDM2 支架结合体 K_D 与天然 p53 肽亲和力 | "p53_design_89, 0.7 nM; p53_design_53, 0.5 nM"；"three orders of magnitude higher affinity than the reported 600 nM affinity of the p53 peptide alone" |
| 44 → 37 → 36 → 18 | Ni²⁺ 金属位漏斗：表达 → SEC 相符 → 测 ITC → 结合镍 | "We expressed and purified 44 designs in Escherichia coli , and found that 37 had SEC chromatograms consistent with the intended oligomeric state"；"Of the designs, 36 were tested for Ni 2+ coordination by isothermal titration calorimetry, and 18 were found to bind Ni 2+ with dissociation constants ranging from low nanomolar to low micromolar" |
| <20 nM，1:4 | NiB1.17 的 K_D 与设计计量比（金属:单体） | "Isothermal titration calorimetry binding isotherm of design NiB1.17 (blue) indicates a dissociation constant less than 20 nM at a metal:monomer stoichiometry of 1:4" |
| 17/17 | H52A 单点突变消除或显著削弱结合的表达成功例数 | "we mutated this residue to alanine, which abolished or notably reduced binding in 17 out of 17 cases with successful expression" |
| 95 / 靶 | binder 战役筛后送测数 | "Designs were filtered by AF2 confidence in the interface and monomer structure 26 , and 95 were selected for each target for experimental characterization" |
| **19%** | binder 总体实验成功率（单点 BLI 判据） | "The overall experimental success rate, defined as binding at or above 50% of the maximal response for the positive control, was 19%" |
| 约 2 个数量级 | 相对同靶旧 Rosetta 战役的提升 | "an increase of roughly two orders of magnitude over our previous Rosetta-based method on the same targets" |
| 1 个数量级 + 1 个数量级 | 提升的归因拆分（生成端 / AF2 过滤端） | "We attribute one order of magnitude to RFdiffusion, and the second to filtering with AF2" |
| 0% / 2.2% / 5.5% / 3.7% / 1.5% | 旧战役**若**用 AF2 过滤的事后估算成功率（HA / IL-7Rα / InsR / PD-L1 / TrkA） | "estimated success rates for previous campaigns if AF2 filtering had been used: HA, 0%; IL-7Rα, 2.2%; InsR, 5.5%; PD-L1, 3.7%; TrkA, 1.5%" |
| <100 vs thousands | 每靶实测数与前作量级对比 | "Binders were identified for all five targets, with fewer than 100 designs tested per target compared to thousands in previous studies" |
| ~30 nM / 28 nM | HA 与 IL-7Rα 最佳亲和力（正文口径）；HA_20 的 K_D（图注口径） | "Full BLI titrations for a subset of the designs showed nanomolar affinities with no further experimental optimization, including HA and IL-7Rɑ binders with affinities of roughly 30 nM"；"The highest affinity HA binder, HA_20, binds with a K D of 28 nM" |
| 6/6 | 高亲和 IL-7Rα 结合体与阳性对照竞争同一位点 | "six of the highest affinity IL-7Rɑ binders were assessed by means of competition BLI, and all six competed for binding with a structurally validated positive control binding to the same site" |
| 2.9 Å / 0.63 Å / 0.6 Å | HA/HA_20 复合物 cryo-EM 分辨率 / 复合物对设计模型偏差 / binder 单体偏差 | "A final non-uniform 3D refinement reconstruction with C3 symmetry yielded a 2.9 Å map of the HA/ HA_20 protein–protein complex"；"r.m.s.d. to RFdiffusion design, 0.63 Å; yellow, influenza HA"；"Over the binder alone, the experimental structure deviates from the RFdiffusion design by only 0.6 Å" |
| 0.6 Å / 2.9 Å | AHB2 三聚体支架的 AF2 复现（不对称单元 / C3 整体） | "AF2 predictions (right) recapitulate the AHB2 structure with 0.6 Å r.m.s.d. over the assymetric unit and 2.9 Å r.m.s.d. over the C3 assembly" |
| n = 71/51；3 Å；16 个 Cα | 口袋统计的两组样本量与 clash/pocket 定义 | "Two-proportion z-test: n = 71/51 +/− potential; clashes z = −2.05, p = 0.02 , pocket z = −2.27, p = 0.01" |
| p = 1.9e-5（n=100/条件） | 接触外部势提升对称设计 in silico 成功率的检验 | "Using these potentials dramatically improves in silico success" |

## 5. 结论——作者说了什么

1. 把 RoseTTAFold 微调成去噪网络就得到通用的蛋白骨架生成器，覆盖无条件设计、fold 限定设计、binder 设计、对称寡聚体、酶活位点支架与对称 motif 支架："by fine-tuning the RoseTTAFold structure prediction network on protein structure denoising tasks, we obtain a generative model of protein backbones"。
2. 无条件设计可做到 600 残基、被 AF2/ESMFold 高置信复折，测试的无条件设计约一半可溶表达且极耐温："Half of our tested unconditional designs express in a soluble way, and have circular dichroism spectra consistent with the design models and high thermostability"。
3. 对称架构：任意点群都能生成，电镜确证结构与设计模型非常接近，且许多整体与已知寡聚体几乎没有全局相似性："Electron microscopy confirmed that the structures of these oligomers are very similar to the design models, which in many cases show little global similarity to known protein oligomers"；这是相对 Hallucination 的能力扩张："RFdiffusion enables generation of higher-order architectures with any desired symmetry, unlike Hallucination methods, which have so far been limited to cyclic symmetries"。
4. motif 支架：25 题 benchmark 解 23 题、多数题成功率更高，且不需要调超参或加外部势（"The excellent performance of RFdiffusion required no hyperparameter tuning or external potentials; this contrasts with Hallucination, for which problem-specific optimization can be required"）；MDM2 一支拿到比天然肽高三个数量级的亲和力，作者用它论证 motif 支架的稳健性。
5. 金属位：侧链原子级定位带来可预测的配位化学（H52A 消除结合），配比与设计一致（1:4）。
6. binder：五靶全出结合体、总体 19%、比旧 Rosetta 战役高约两个数量级（他们把提升拆成生成一乘 + AF2 过滤一乘），并认为从此不再需要高通量筛选："high-affinity binders can be identified from dozens of designs, in many cases eliminating the requirement for slow and expensive high-throughput screening"；作者把这套能力定性为"按最小分子规格生成"："In a manner reminiscent of the generation of images from text prompts, RFdiffusion makes possible, with minimal specialist knowledge, the generation of functional proteins from minimal molecular specifications"。
7. 作者自陈的边界：binder 的高成功率至少只针对此处做的非极性位点（"at least for the non-polar sites targeted here"、"further studies will be required to assess success rates on more polar target sites and sites without native binding partners"）；配体尚不能显式建模（"Although RFdiffusion is unable to explicitly model bound small molecules at present"）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

以下为推断。

1. **这篇真正的跃迁在分母，不在分子**。19% 之所以是突破，不是因为判据更准，而是送测数从"每靶数千到十万"掉到"每靶 95"——预算从**样本量**挪到了**先验质量（生成 + 闸口）**。→ 对我们：没有展示库通量的产物化学里，唯一能复制的就是这条，即提高每个送测个体的机制信息量而不是数量。
2. **提升被显式拆成两乘，第二乘来自 [B09] 的 AF2 过滤**。即 RFdiffusion 单独贡献的是骨架分布多样性与界面形状互补，不是判别能力。反读：只换召回端（换候选来源）而不建立等价判别端，就不会拿到这个量级的收益。
3. **生成端与判别端同源，是这套体系的结构性风险**。生成用 RF 权重微调，验证用 AF2 单序列复折——同一族网络给自己打分；作者用 SEC/EM/BLI/ITC 与突变对照做外部对冲，但 benchmark（W7）与口袋（W8）两条线几乎全靠这族网络自证，而这两条恰恰最像"酶设计"。→ 对我们：任何以预测器为闸口的设计，必须指定至少一个**物理来源不同**的终判据（我们的 LC-MS/MS 产物身份 + 失活对照）。
4. **他们面对能力缺口的策略是绕过去 + 把失败可数化**：不能建模底物 → 外部势 + clash/pocket 计数；不能电镜看小颗粒 → 退回 SEC 分子量；FastRelax 无提升 → 直接砍。这套"降级 + 失败分型"是本文最难复制也最该复制的部分。
5. **台账本身有裂缝**（同一批 96 与 95 并存），说明即便 Baker 组，正文与图注口径也会飘；引用他们的数字必须指名出处，我们自己交付要按"每行可追到产生它的脚本与参数"要求。
6. **两数量级里含一次事后估算**。0%/2.2%/5.5%/3.7%/1.5% 是"假如旧战役用过 AF2 过滤"的重分析而非平行实测；用它支撑"AF2 过滤值一乘"的证据强度低于 [B09] 的前瞻分臂。只许迁移其拆分思路，不许把这些百分数当实测。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自陈**
- 配体/小分子不能显式建模（第 2.7 条），酶位点这条线因此只到几何 + 口袋统计，**全文没有任何催化速率、转化率或酶活数字**；逆醛醇酶一支只做 in silico 演示（"As a demonstration, we scaffold a retroaldolase active site triad while implicitly modelling the reaction substrate"），活性验证不在本文。
- 单序列结构预测能力有上限，超大蛋白无法在计算侧验证（第 2.6 条）；D2 等小组装体只能靠 SEC 分子量弱确证。
- 19% 被标为保守估计，因为部分显示结合的设计因材料不足没在 10 μM 测到（可能是假阴，图注用色相另行标注）；特异性只做到同位竞争，"further work is required to fully characterize proteome-wide specificity"。
- binder 高成功率限定于本次的非极性界面；更极性位点、以及无天然结合伙伴的位点成功率未知。
- 关键增益都带"换个场景不一定成立"的自陈：m.s.e. 只在无锚定时必要、self-conditioning 的机理只是猜测、降噪声尺度换来的成功率以牺牲多样性为代价（第 2.3、2.2、2.9 条）。
- 他们承认在难题上仍会失败："In silico success rates on the problems are correlated between the methods, and RFdiffusion can still struggle on challenging problems in which all methods have low success"。

**我们读出**
- 生成端与判别端同源（同一 RF/AF2 家族），benchmark 与口袋两条线缺独立物理验证，存在自我确认闭环；这是全文最结构性的方法学风险。
- 正文与图注的 MDM2 分母不一致（96 / 95），说明其数字台账未经交叉核对；引用时必须并列两值。
- 与旧战役的对比是**跨战役历史数据 + 事后重分析**，不是同批随机对照；"两个数量级"的可比性弱于 [B09] 的前瞻分臂实验。
- 全文无 MD、无 QM、无自由能计算：本篇不能为"用 MD/QM 判催化"提供任何证据或命中率。
- 本地文本不含 Methods 与 Supplementary Methods，大量协议参数（微调数据量、势函数形式与参数、SEC/CD 与 BLI 的具体条件）无法从这份文本核验；本卡只在有引句处写具体数值，其余明写"正文未给出，指向 Supplementary Methods"。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **把送测预算从数量换成每个个体的机制信息量**：他们靠生成端 + 单一强闸口把每靶压到 95 个，再用结构级确证与失活对照榨取信息。我们一轮最多四个构建体的处境与此同构：每个构建体绑定一个可判伪的机制假设（S0 游离 UTP 起始 / S1 pppUA / S2 第二枚 ATP 与环化竞争），并各配失活对照，而不是加平行重复。
2. **失败可数化的拆法**（第 2.7 条）：把"不成"拆成两类能用几何数出来的模式，再给硬判据（距离阈值 + 计数阈值）。对应我们：把候选失败拆成"底物袋不存在或被侧链堵死"与"催化残基几何错位"两类，各自给可搜的几何判据（theozyme 距离/取向偏差、埋藏度、底物可及的 Cα 计数），并允许 UNKNOWN 与 METHOD_FAIL 两种状态。
3. **能力缺口用代理绕开，但必须声明代理只覆盖到哪一层**：他们明写外部势与 clash 定义只看骨架 Cα、不含侧链。我们同理：用骨架/侧链几何代理催化可行性时，必须显式声明这不涵盖电子结构与过渡态，绝不报成活性判据。
4. **每道闸口都要有一次上它 vs 不上它的实测**（他们这样处理 FastRelax，结果弃用）；不能因惯例保留步骤。配合 [B09] 的"通过率 ÷ 单价"口径决定跑不跑。
5. **正交验证器分层**：AF2 之外再上 ESMFold（不同架构与训练），计算之外再上 SEC/EM/ITC/BLI。我们对应：结构检索与预测之外必须有化学侧终判据（LC-MS/MS 产物身份 + 非天然底物阴性 + 竞争/失活对照）。
6. **报告里显式拆分归因**：他们把两乘提升拆成生成端与筛选端。我们每个改进也要标明这一乘来自召回、那一乘来自判别，否则无法决定下一步预算投向哪一环。

**不可迁移（为什么不能照搬）**

1. **pLDDT>80、interaction pAE<10、backbone r.m.s.d. 1–2 Å 一律不得当 UAA 酶活判据或成功概率**。它们是"会不会折成设计构象、会不会按设计界面结合"的静态结构自洽判据；UAA 合成酶要判的是三个化学事件是否按序发生、有无副产物竞争，结构自洽既不必要也不充分。项目 DP2R 口径规范明确禁止把 binder 的 pAE/ipTM 阈值搬作酶活闸口，本卡按此执行。
2. **19%、约两个数量级、0.5/28 nM 这些数字不能搬来校准我们的期望**。其分母是"每靶 95 个 binder + 二值 BLI 判阳"，判据里没有化学转化维度；19% 还是作者自称的保守下界，跨战役对照为事后重分析。本卡只迁移**流程结构**，不迁移**命中率数字**。
3. **"扩散模型已经能设计酶"这句话在本篇没有证据**。催化位点这条线全文停在 in silico 与口袋统计，无一条活性数据；把 B08 当酶设计可行性依据属于过度引用（带活性的 theozyme/酶设计一线见本目录 [B20]，需另读卡）。
4. **他们的通量优势建立在结合读出上**（96 孔 BLI 单次判阳）；UAA 产物鉴定要 LC-MS/MS，单样时间、假阳结构、样品量限制都不同，"每靶 95 个"的规模直觉不可照搬。
5. **本文无 MD/QM/自由能**，故不能为"用 MD 或 QM 判催化可行"提供命中率背书；该类主张的参照物不在这篇里。
6. **Ni²⁺ 那条线不是催化**：方形平面几何 + ITC 结合常数只证明"设计位点真的结合了金属"，与我们要的多步化学转化不同层次，不能拿 18/36 或 K_D<20 nM 当"设计金属酶位点的成功率"引用。

## 9. 溯源与自检

- **本卡实际照着写的那一份全文**（唯一比对底稿，非 Europe PMC/NCBI 双版本混用）：
  引句底稿: data/interim/baker_lit/ft/rfdiffusion2023.txt
  该文件 93,810 B，去标签纯文本，SHA-256 `2aa635bf84a95987…`；由 Europe PMC `fullTextXML`（PMC10468394）于 2026-10-16 抓取，`inventory.json` 中 B08 记 `fetch_channel=epmc_fulltext`。归一化与门禁共用 `scripts/litcards_text.norm`（实体解码、引号/破折号统一、空白折叠）。
- **登记底稿**：`sources/baker.md` 第 107–118 行（原卡）。本卡是其超集，新增：训练/推断机制细节（frame 表示、m.s.e. loss、self-conditioning、200 步与早停/步长消融）、**三套以上互不相同的 in silico 成功口径**、25 题 benchmark 的构成与对照、对称与口袋两条线的外部势、H52A/竞争 BLI 对照、MDM2 的 96-vs-95 口径裂缝、噪声尺度-多样性权衡。
- **口径来源的另一篇**：本文 binder 闸口直接沿用 [B09]（正文标号 26），见 `data/literature_cards/B09_Bennett-2023_NatComms_af2-filter.md`。
- **CSV 字段映射**：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **自检过程**：卡片落盘前，候选引句分五批（共 183 条）用 `A:\AITEMP\b08_check.py`（import 门禁同一 `norm`）逐字预核验，179 条命中；4 条因抄写走样（漏主语、use/used、首字母大小写）在写入前剔除或改正。写入后用 `A:\AITEMP\b08_cardcheck.py` 以门禁同一抽取规则整卡复核：**105 条英文引句，MISS 0**。
- **门禁实测输出**：`PASS B08 quotes=105/105`（命令 `cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B08 --no-report`，退出码 0）。首次运行曾因 §9 未写引句底稿声明行而 FAIL，补上该行后复跑通过。未跑 `--sync-map`，未跑不带 `--no-report` 的全量门禁；未改 CSV、`sources/*.md`、样板卡 B09 与 `scripts/` 下任何文件。
- **本卡不能核验的部分**：这份本地文本没有独立 Methods 章节与 Supplementary Methods/Tables、没有 Extended Data Table 1 的数值、没有原图；且本卡只有**一条**取回通路（不同于 B09 的双通路互证），无法做跨通路交叉验证，此差异如实记录，不称"双通路互证"。

<!--CSV回填
work_type=论文
target=全新折叠单体（TIM barrel、NTF2）、C/D/四面体/八面体/二十面体对称寡聚体、Ni²⁺ 方形平面金属位、p53 螺旋-MDM2 肽支架、SARS-CoV-2 spike 的 AHB2 三聚体、EC1-5 酶活位点、5 个蛋白靶点结合体（H1 HA、IL-7Rα、InsR、PD-L1、TrkA）
backbone_generation=RFdiffusion：RoseTTAFold（更新版）权重微调的去噪扩散模型，残基 frame 表示（Cα + N-Cα-C 朝向）、m.s.e. 损失、self-conditioning、默认 200 步反向；条件通道＝无／二级结构+block adjacency／点群对称（单体随机 frame 复制 n-1 份 + 每步重对称化 + 链间链内接触势）／界面热点残基（复合物微调模型）／motif 三维坐标（含侧链）／底物隐式外部势 → 序列由 ProteinMPNN 出（常规 8 条/骨架，对称口径 16 条/骨架）
computational_filters=AF2 单序列复折一致性：mean pAE、mean pLDDT、设计-预测 backbone r.m.s.d.、被支架 motif 的 backbone 与全原子 r.m.s.d.、界面 interaction pAE（沿用 [B09] 口径）；ESMFold 作正交置信度；TM-score 到 PDB 做新颖度与 fold 命中；口袋几何计数（clash 与 pocket）；物理打分未进最终流程（Rosetta FastRelax 实测无系统提升后弃用）
thresholds=统一 in silico 口径 mean pAE<5 + 全局 backbone r.m.s.d.<2 Å + 位点 r.m.s.d.<1 Å；对称口径 mean pLDDT>80 + 寡聚体 backbone r.m.s.d.<2 Å；binder 口径 monomer pLDDT>80 + interaction pAE<10 + monomer vs 设计 r.m.s.d.<1 Å；benchmark 口径 design<2 Å + motif<1 Å + pAE<5；口袋口径 clash=底物 3 Å 内有骨架 Cα、pocket=无 clash 且 3-8 Å 内>16 个 Cα；fold 命中 TM-score>0.5；实验阳性=单点 BLI 10 μM 响应≥50% 阳性对照；推理默认 200 步（可 15 步或早停 T=50-75，难问题取 T=50）
md_used=否
qm_used=否（Ni²⁺ 位只给理想配位几何，配位与亲和力靠 ITC 实测，全文无电子结构计算、无自由能微扰）
experimental_methods=E. coli 可溶表达 + SEC（用校准曲线给 95%/99% 置信区间）+ CD 谱与熔曲线（至 95 °C）+ nsEM 2D class averages 与 3D reconstruction + cryo-EM（HA/HA_20 复合物 2.9 Å）+ 单点 BLI 10 μM + BLI 滴定投 K_D + ITC（含 H52A 失活对照）+ 竞争 BLI；刻意不用酵母/噬菌体展示库
pipeline_counts=无条件：18 送测 → 9 表达。TIM：11 纯化 → 10 可溶单体 → 8 够 CD。对称：608 送 SEC → ≥87 相符（95% CI）/126（99% CI）；另有 38 D2 / 7 D3 / 3 D4；48 个二十面体 → 1 个均一颗粒（HE0902）。MDM2：96（正文）或 95（图注）→ 55 检出结合 → 32 单体。Ni：44 表达 → 37 SEC 相符 → 36 测 ITC → 18 结合镍 → H52A 17/17 消除或削弱。binder：每靶 AF2 筛后选 95 → 5 靶全出结合体（合计送测约 475）。benchmark：25 题 × 每题 100 设计
hit_rate=binder 总体实验成功率 19%（作者称保守，含未测到 10 μM 的假阴风险）；相对同靶旧 Rosetta 战役约两个数量级提升，自析为生成端一乘 + AF2 过滤一乘；MDM2 55/96；Ni 18/36；in silico：TIM 42.5%、NTF2 54.1%、benchmark 解 23/25 题（Hallucination 15、RF joint Inpainting 19）；全文无酶活命中率
best_metric=HA_20 K_D 28 nM（Fig. 6d 图注）与 HA/IL-7Rα 约 30 nM（正文口径）；MDM2 支架结合体 0.5 与 0.7 nM（天然 p53 肽 600 nM）；NiB1.17 K_D<20 nM（金属:单体 1:4）；结构精度 cryo-EM 2.9 Å、复合物 0.63 Å、binder 单体 0.6 Å
cost_or_stat_note=100 残基骨架 15 步约 11 s（NVIDIA A4000，in silico 成功率 >60%），对照 RF Hallucination 约 8.5 min；训练与默认推理 200 步；每靶仅送测 <100（旧法数千到十万）；benchmark 每题 100 设计；口袋统计两组 n=71/51；消融以两比例 z 检验报告（n=400 或 800 设计/条件，如 z=9.5、p=1.6e-21 与 z=23.0、p=3.1e-117）；降噪声尺度提成功率但按 TM-score 0.6 聚类口径损失多样性
role_in_timeline=分水岭：生成端从"在既有骨架库里搜索/预设 scaffold 库"转为"按规格直接生成"，一个模型覆盖折叠/对称/motif 支架/金属位/binder 五类任务；筛选端普及并固化 [B09] 的 AF2 置信度闸口（pLDDT>80、interaction pAE<10）；湿实验成本结构从"十万设计 + 展示库"变成"约百设计 + 96 孔 BLI"；其遗留的"不能显式建模配体"缺口由后续全原子/配体版扩散（本目录 [B18]/[B20] 一线）接手
source_pointer=data/interim/baker_lit/ft/rfdiffusion2023.txt（93,810 B，SHA-256 2aa635bf84a95987…，Europe PMC fullTextXML of PMC10468394，2026-10-16 抓取）+ sources/baker.md:107-118
CSV回填-->
