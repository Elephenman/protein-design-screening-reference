# [K65] 氢键网络的快速采样（MC HBNet）——把关键相互作用前置成生成空间的硬约束，再事后过滤

Maguire Jack B.（UNC Chapel Hill）, Boyken Scott E.（UW IPD）, Baker David（UW IPD/HHMI）, Kuhlman Brian*（UNC）
J. Chem. Theory Comput. 2018, 14(5): 2751–2760 · DOI 10.1021/acs.jctc.8b00033 · PMID 29652499 · PMCID PMC5940506（NIHMS961206 作者手稿版）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K65**（组：通用方法学；CSV 证据级别登记为"摘要级"，本卡按 FULLTEXT 状态写到全文级） |
| 本文取回方式 | Europe PMC fullTextXML（inventory 记录 fetch_channel=epmc_fulltext；batches.tsv 记 NCBI efetch 兜底成功），本地抽取共 48,461 字符、单行（norm 折叠空白） |
| 本地全文 | `fulltext/K65_PMC5940506_fullTextXML.xml` 与去标签纯文本 `fulltext/K65_PMC5940506_text.txt`（门禁只拿 §9 声明的那份逐字比对） |
| 对照底稿 | `sources/baker.md:66`——[B04] 条目把本文列为"埋藏极性必须成氢键"判据演进链的上游锚点：Boyken 2016 Science、本文 2018、Coventry & Baker 2021（B04，两两分解惩罚项）、后被吸收进 ProteinMPNN/LigandMPNN 序列似然 |
| 证据级别 | **全文级**（本卡所有引句在 §9 声明底稿里逐字命中；见第 9 节自检） |
| 版本注意 | 本地版是 **NIHMS 作者手稿**（非出版社排版版）；文头还登记了一条 2018-09-17 的 Correction（JCTC, PMID 30221938），更正内容本地未取回——凡涉及可能被更正的数值，本卡只保证与本地底稿逐字一致 |
| 未取到的部分 | 补充材料 Figure S1 与 Table S1–S8 的原图数值、Table 1 之外的采样级别实现细节。凡引这些处本卡明写"正文未给出数字，仅有正文描述" |

## 1. 这篇到底解决什么（大白话）

蛋白设计里有一类需求：让指定位置上的一组氨基酸**恰好互相成氢键、且不留任何埋藏却没有氢键伙伴的极性基团**——作者把这种性质定义为"closed network"（封闭网络）。这种网络整体是合作性的：只有全部埋藏极性都被满足，网络才在能量上划得来，所以不能像普通相互作用那样一项一项加进打分函数。Boyken 2016 的 HBNet 用**穷举**在固定骨架上枚举给定 rotamer 库里所有可能的封闭网络，并在对称卷曲螺旋上拿过实验验证；但它扩不动——稍大的非对称界面或蛋白内部就几小时、几周跑不完。这篇给出 **MC HBNet**：先把"哪些位置换成哪些氨基酸、用哪个侧链构象能成氢键"预先编译成一张图（节点=rotamer，边=一条能量低于 -0.5 REU 的氢键），再用蒙特卡洛轨迹在图上随机生长网络，**只有零重原子埋藏未满足（heavy unsat = 0）的网络才作为结果登记**。验证全部是计算对计算：2776 条天然界面网络的可恢复率、四个设计场景与四个对称复跑案例的耗时/网络数/Saturation/内存。**本文没有新的湿实验**，它的"命中"口径是：复现此前已被晶体结构验证的设计，并在旧方法失败的大界面场景里产出可行的氢键网络。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **难点：目标本身不可两两分解——氢键网络是"全满足才成立"的合作性结构**。作者开篇定性："One key feature of hydrogen bond networks that makes them difficult to rationally engineer is that they are highly cooperative and are not energetically favorable until the hydrogen bonding potential has been satisfied for all buried polar groups in the network."，而主流打分框架帮不上忙："Existing computational methods for protein design are ill-equipped for creating these highly cooperative networks because they rely on energy functions and sampling strategies that are focused on pairwise interactions."。物理锚点：埋藏一个没有氢键伙伴的供体/受体代价极高——原文估计数值 5-6 kcal/mol（该句在原文里内嵌一个 ASCII 双引号括注与引文编号 21，本卡只引编号前片段："the energetic cost of burying a hydrogen-bond donor or acceptor that does not have a hydrogen bond partner"，并附下句片段 "which is comparable to the total free energy of unfolding for some proteins"）。 **他们做了什么**：不改能量函数权重，而是换范式——把"满足性"变成**生成空间上的硬约束**："To enable the design of complex hydrogen bond networks, we have developed a new sampling protocol in the molecular modeling program Rosetta that explicitly searches for sets of amino acid mutations that can form self-contained hydrogen bond networks."；形式化定义是图语言："A hydrogen bond network can be defined as a set of nodes that form a connected component in the HbondGraph without having any two nodes that represent rotamers that clash or occupy the same residue position."，验收标准只有一条：封闭（每个埋藏极性都有伙伴，"every buried polar group has a hydrogen bond partner"）。 **留下的代价**：满足只是静态几何判据，网络周围尚空——原文自述输出时要 "Constraints are turned on to ensure that the hydrogen bonds of the network are maintained during downstream design"，即本方法只交付"被约束保护的网络"，周围 packing 全押给下游（本文未做）。
2. **难点：穷举枚举扩不动，旧 HBNet 在真实设计规模上直接超时**。"Since these initial results, we have begun to apply HBNet to other design problems and we have found that is scales poorly to larger systems, especially cases where symmetry cannot be used to reduce search space."（原文语法错误保留）以及："For larger rotamer libraries or larger numbers of residue positions, we observe that the exhaustive search employed by HBNet often does not complete after several hours, which precludes its use in design pipelines that also involve backbone sampling and docking."——旧法本质是穷举："To maximize the number of potential networks that are identified for a given backbone conformation and set of residues, HBNet enumerates through all possible closed networks that can be created with a given rotamer library."。 **他们做了什么**：把穷举换成**蒙特卡洛图上生长**："Here, we introduce a new Monte Carlo-based algorithm (MC HBNet) that makes it possible to rapidly sample and design viable hydrogen bond networks for larger design problems."；基准里明说旧法慢到什么程度——"HBNet's tendency to take weeks to run if given too large of a design scenario"，并因此设 24 小时限。 **留下的代价**：随机生长不完备（见第 6 条）。
3. **难点：氢键对几何极端敏感，rotamer 库太粗会漏掉真网络；但把库加大又会让穷举爆炸**——速度与覆盖率是一对矛盾。原文："One of the limitations of the previously developed HBNet protocol is that it becomes dramatically slower (see below for case examples) when a larger rotamer library (i.e. more chi torsion angle sampling) is used during the design process."。 **他们做了什么**：引入 extra chi 采样档位（Table 1：Ø、χ1、χ1χ2、χ1χ2χ3、χ1χ2χ3χ4，每档对相应 chi 角 ±1 标准差加密），并用 2776 条天然界面网络量化收益——"Sampling level χ 1 χ 2 can sample more than three times the fraction of native networks than can be sampled with no extra chi sampling (Ø)."；MC 的关键卖点恰是能消化更细的库："Because MC HBNet can be used with a finer degree of side chain sampling than HBNet, we also show that it can find more favorable networks than HBNet in substantially shorter runtimes."。 **留下的代价**：恢复率是"能否同时采样到"的能力上限，不是概率保证；细库下的假阳性网络（几何上能成键但实际不会随设计折叠出现）本文没有量化。
4. **难点：骨架冻结假设与设计管线冲突**。协议全程固定骨架："The protein backbone is held fixed throughout the protocol and sidechain conformations are sampled using a backbone-dependent rotamer library"；但作者自己测出网络对骨架微扰敏感——"backbone perturbations of as little as ~0.1 RMSD can affect the networks that can captured"（原文缺 be，保留）。 **他们做了什么**：用 Rosetta Backrub 骨架集做了演示（Figure S1，正文只有描述、无数字），表明 extra chi 采样能补偿一部分骨架扰动；管线层面给出算力再分配方案："the computational savings afforded by MC HBNet can be reallocated to employ more computationally expensive protocols (e.g. flexible backbone methods) during downstream design to optimize the remaining interface positions that surround the network"。 **留下的代价**：本文未解决——柔性骨架与网络搜索的联合采样只是展望，没有基准与实验。
5. **难点：埋藏性判定本身困难——设计态网络周围是空腔**。"Determining which polar atoms in the networks are buried versus solvent-exposed is challenging because the space around the hydrogen bond networks is often not yet designed, leaving large voids."。 **他们做了什么**：放弃旧 HBNet 的"增大探针半径的 SASA"算法，改为**位置级预计算**："burial is precomputed by classifying each residue position as buried or not based on the number of neighboring residue positions that fall within a cone around the vector between its C α and C β atoms"，作者说明这样更快、且对同一骨架与序列/侧链构象无关地一致。 **留下的代价**：粗分类意味着"埋藏"判定与真实堆积环境脱钩，未满足判据的假阳/假阴率没有对照（本文未给阈值之外的验证）。
6. **难点：换随机搜索就得回答"为什么不完备的搜索反而更好"**。他们给出的机理解释是本卡认为最有价值的一段："In short, HBNet is a complete search of an incomplete sample space while MC HBNet is an incomplete search of a more complete sample space, and the latter appears to be a more effective strategy."，并且作者诚实标注这反直觉："This result is not expected to be true when comparing any stochastic protocol with its exhaustive counterpart."。机制差异在登记规则："HBNet only stores networks that have grown to completion"（片段），而 "MC HBNet can register satisfied subnetworks as results and continue to grow from them, while HBNet does not by default."。 **他们做了什么**：给 MC 加轨迹数旋钮并实测——对称案例 "MC HBNet benefits noticeably by increasing the number of Monte Carlo trajectories from the default of 10 4 to 10 5 for these symmetric cases."。 **留下的代价**：本文未解决——没有收敛判据，"轨迹数够不够"只能逐案例用复现旧设计来事后判断。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **Rosetta 内的新采样协议 MC HBNet**（本文主角）：新数据结构 HbondGraph + 蒙特卡洛轨迹生长。
- **backbone-dependent rotamer library**（Dunbrack 2011）+ 用户可选的 extra chi 加密档（Table 1，每档对相应 chi 角加 ±1 标准差样本）。
- **Rosetta 标准氢键势**（距离+方向，O'Meara 2015/Kortemme 2003 一脉）做边的判据；**ref2015 打分函数**只在天然恢复基准里用来算天然氢键能量；**完整 Rosetta 能量函数**只用于并列时的 HBNet Score 排序。
- **Pisces** 网络服务器建天然界面结构库；**Backrub** 骨架集仅作 Figure S1 敏感性演示。
- **没有用的方法**：MD、QM、深度学习、湿实验——本文全程是"计算对计算"的算法论文。

### 主协议 + 基准的分步流程（阈值全部取原文数字）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 建图 | 输入结构（骨架固定）+ 用户定义的可设计位点集合与每位点允许的氨基酸类型 | 枚举位点对："All residue pairs within a user-defined set of packable positions are enumerated."，每位点按 rotamer 库（可选 extra chi 档 Ø…χ1χ2χ3χ4）展开为节点，逐对测氢键："Hydrogen bonds are detected using Rosetta's standard hydrogen bonding potential, which depends on the distance and relative orientation of the donor and acceptor groups" | "Hydrogen bonds typically score between -0.5 and -1.5 Rosetta Energy Units (REU)." 且 "For most of this work, we only consider interactions with an energy less than -0.5 as a hydrogen bond." | HbondGraph：节点=rotamer（含位点冲突/位阻不相容表），边=氢键（边上存供体/受体/氢原子索引） |
| 2 剥离背景满足 | 图上各节点的侧链极性原子清单 | 剔除已被背景满足的原子（溶剂暴露、或与固定的主链/非设计侧链成键）："MC HBNet strips this atom information for polar atoms that are already satisfied by the background" | 剩余即"必须被网络自身满足"的原子；追踪对象定义为："For each network, MC HBNet tracks satisfaction by storing a list of all heavy (non-hydrogen) polar atoms that are buried and not satisfied"（即 heavy unsat 表） | 每条种子的 ad hoc 验收清单（原子数原文未给） |
| 3 MC 生长 | HbondGraph + 起始准则（可选，如 HBNetStapleInterface："which searches for networks that span across a protein-protein interface"） | "The MC HBNet sampling protocol is composed of a user-defined number of trajectories."；"Seed edges can be selected based on predefined starting criteria."，从种子边随机起，"networks are grown stochastically by adding adjacent edges that lead to compatible nodes"，选择概率："The relative probability of selecting a candidate to be added to the network is proportional to the number of its compatible children plus one."；"Efficiency is improved by restricting sampling to only start at seed edges relevant to the task at hand." | 有 heavy unsat 时聚焦："If the network has any heavy unsats at any point within a trajectory, the MC HBNet sampling protocol will shift its focus to only consider candidate nodes whose addition would result in the satisfaction of a heavy unsat."；登记条件："One candidate is stochastically selected to be added to the network and the network is registered as a result if it is determined to be absent of heavy unsats." 默认 10^4 条轨迹（对称基准用 10^3–10^6） | 原始封闭网络集合（数量随体系；3U3B 单体案例"几分钟数千条"，其余案例正文未给总数） |
| 4 事后过滤 | 全部轨迹产物 | 序列冗余去重 + 硬性剔除 + 可选自定义剔除 | "Networks are filtered and sorted, eliminating those that are redundant in primary amino acid sequence past a user defined threshold."；"Networks that contains at least one heavy (non-hydrogen) buried polar atom that is not either donating or accepting in a hydrogen bond are also eliminated."；羟基豁免单边："Hydroxyl groups are only required to either donate or accept, but not both, to be considered satisfied"；"Users can also eliminate networks based on a custom criterion (e.g. minimum number of residues in the network, or number of intermolecular hydrogen bonds)."（去重相似度的具体数值原文未给阈值） | 存活网络集（规模原文未给） |
| 5 排序与输出 | 存活网络集 | 三级排序 + 落回结构 | 第一级埋藏未满足极性氢原子数（允许存在但罚分）："Buried polar hydrogen atoms that do not participate in hydrogen bonds are allowed but incur a penalty during sorting."；"The remaining hydrogen bond networks are sorted and ranked first by the number of buried unsatisfied polar hydrogen atoms (Num_Unsat_Hpol), then Saturation, then HBNet Score:"；饱和度定义："We define saturation as the fraction of total hydrogen bonding capacity (given the polar atoms that comprise the network) that is met by the actual hydrogen bonds of the network."，满分 1.0，"Saturation values can potentially be larger than 1.0 in the case of a hydroxyl participating in 3 hydrogen bonds or the case of bifurcated hydrogen bonds."；"HBNet Score is the difference in energy between the background structure with and without the network residues placed, normalized by the number of residues in the network."，背景=丙氨酸化基底："which is the input structure with all packable residues mutated to alanine (except for any existing Gly, Pro, or disulfides, which are kept)" | 按排名逐个把网络放到输入结构上输出；"Once the output structures are returned, any other part of Rosetta can be called to perform further design and analysis, or the structures can be output to disk."；同构网可合并："Users can also opt to combine compatible networks together on the same output structure." |
| 6 天然恢复基准 | PDB 经 Pisces 修剪（"Sequence percentage identity ≤ 60; Resolution ≤ 2.0 Å; R-factor ≤ 0.3, Sequence Length 40 - 10000"），且 "This library was pruned to only include structures that contain at least one protein-protein interface." | 用 HBNet 只考虑天然 rotamer 枚举网络："HBNet was used to generate a list of unique native hydrogen bond networks within this pruned library by considering only native rotamers in each structure."；再按低分辨侧链剔除："removes networks that were comprised of at least one sidechain that had a heavy atom with a B factor greater than 40"（单位 Å²） | 恢复判据双阈值："For every network in this list, we identified every hydrogen bond that had an energy ≤ -0.5 Rosetta Energy Units (REU) using Rosetta's ref2015 score function."，重建时要求 "every native hydrogen bond with an energy ≤ -0.5 REU was simultaneously present with an energy ≤ -0.4 REU"；"If all of the hydrogen bonds in the network could be simultaneously sampled, the network was deemed to be recovered." | "2776 networks met these criteria and made the final list."；结论：χ1χ2 档恢复分数倍于 Ø（见上引 3× 句） |
| 7 四个设计场景对照 | 1YRK 界面（40 可打包位点）、1DPJ（121）、1GK9（342）、3U3B 链 A 螺旋束单体（23 个埋藏位点）；场景口径："all residue positions of the first chain were designed and all positions on the other chain were set to repack only"；"In all cases, all polar amino acid types were considered at designable residue positions" | HBNet 与 MC HBNet 各跑 {Ø, χ1, χ1χ2}，MC 轨迹数 10^3/10^4/10^5/10^6；记录 CPU 时间、峰值内存、top10 网络的统计量 | 超时上限："Due to the ability for most runs to finish within a few hours and HBNet's tendency to take weeks to run if given too large of a design scenario, we declared a 24-hour runtime limit." | "Many HBNet runs were not able to finish within 24 hours (denoted by asterisk in Figure 5 ) while every MC HBNet run took less than 1 CPU hour."；单体案例："HBNet failed to finish exploring the sample space of the small helical monomer design case within our 24-hour time limit, even at the smallest extra chi sampling level, but MC HBNet was able to find thousands of hydrogen bond networks within minutes."；质量侧："All of the top networks reported had 0 unsatisfied polar atoms (which is the first metric used to sort results), meaning that Saturation was the primary determinant in the ranking of the networks and assessing network quality." |
| 8 对称复跑 + 591 例聚合 | 先前实验验证的 4 个对称设计（5J0K/5J10 同源二聚、5J0H/5IZS 同源三聚）；另有 591 个单侧界面案例（含前述 3 个界面）只跑 Ø 档 | 对称案例按原协议加更严过滤器复跑："Unlike with the Monte Carlo-motivating benchmarks, we defined stricter filters to the designed networks in order to match the original protocol used to create these designs"，比较口径："We compared the two protocols by the number of networks that meet these strict design criteria."；591 例："Additionally, this benchmark was run using sampling level Ø on 591 one-sided interface design cases including the 3 mentioned previously."，且 "The only metrics we tracked were the runtimes for HBNet and MC HBNet (using 10 4 trajectories)." | 对称案例豁免 24h 上限（此前已被证明能在合理时间跑完） | MC 复现先前验证的网络且随时间找到更多（"MC HBNet still outperforms HBNet for the symmetric homo-oligomers when comparing CPU time for a given chi sampling level, however the difference is milder than with the asymmetric interfaces."）；591 例："Not only are most points above the line, but the distance from the line increases as the problem size grows, demonstrating that MC HBNet is faster than HBNet and better equipped to handle large design cases."；早退机制另省约 40%："This check reduces MC HBNet's runtime by approximately 40% by creating fewer false positives that need to be filtered out by a more computationally expensive satisfaction check that occurs at the end of the protocol, before networks are output." |

**流程骨架值得单独记住**：生成阶段的唯一硬约束是"封闭"（heavy unsat = 0），其余全部降级为事后过滤与三级排序；而"封闭"这个约束之所以可能，是因为它被**预先编译进图结构**（边只连"能成氢键且不打架"的 rotamer 对），搜索时只走合法路径——这与 B09 的"事后用 AF2 打分当筛子"是互补的两路：**一个在生成端把物理要求变成可达性，一个在评估端用预测器做判别**。

## 4. 关键数字台账（数值 · 含义 · 出处；全部可在本地全文搜到）

| 数值 | 含义 | 出处（全文位置） |
|---|---|---|
| 5-6 kcal/mol | 埋藏一个无氢键伙伴的供体/受体的估计能量代价（引自文献 21 的估计，非本文测量） | Introduction 第 2 段 |
| -0.5 ~ -1.5 REU | Rosetta 标准氢键势下氢键的典型得分区间 | Methods 第 1 段 |
| 能量 < -0.5 REU | 建图时的成边判据（本文主工况） | Methods 第 1 段 |
| 额外 chi 采样 ±1 标准差 | Table 1 各档（Ø、χ1、χ1χ2、χ1χ2χ3、χ1χ2χ3χ4）的加密幅度 | Table 1 及其脚注 |
| ≤ -0.5 REU → ≤ -0.4 REU | 天然恢复判据：原网络每条氢键须被同时重建且允许 0.1 REU 松弛 | Benchmarks, Native Network Recovery 段 |
| 2776 | 进入恢复基准的天然界面氢键网络数 | Benchmarks, Native Network Recovery 段 |
| B factor > 40 Å² | 剔除含低分辨侧链的网络 | Benchmarks, Native Network Recovery 段 |
| ≤60% 序列同一性 / ≤2.0 Å / R-factor ≤0.3 / 长度 40–10000 | Pisces 建库修剪四条件 | Benchmarks, Native Network Recovery 段 |
| 40 / 121 / 342 | 小/中/大界面单侧设计的可打包位点数（1YRK / 1DPJ / 1GK9） | Benchmarks, Network Design Benchmarks 段 |
| 23 | 螺旋束单体案例（3U3B 链 A）的埋藏设计位点数 | 同上 |
| 591 | Ø 档聚合运行时间基准的单侧界面案例数（只记时间） | Benchmarks 末段 |
| 10^4（默认）；10^3–10^6 | MC 轨迹数：默认与对称基准测试档位 | Methods MC Traversal 段 / Benchmarks |
| 24 小时 | HBNet vs MC 基准的超时上限（对称复跑豁免） | Benchmarks 末段；Results New Design Cases 段 |
| < 1 CPU hour | 四个新场景中每一次 MC HBNet 运行的耗时上界 | Results, New Design Cases 段 |
| less than a minute（一般情形） | MC 对多数界面尺寸的典型完成时间 | Conclusions 段 |
| 约 40% | 未满足即终止+不登记 heavy unsat 带来的运行时间节省 | Methods MC Traversal 段 |
| 3 倍以上 | χ1χ2 档相对 Ø 档的天然网络恢复分数倍 | Results, Benefits of Extra Chi Sampling 段 |
| ~0.1 RMSD | 足以改变可捕获网络集合的骨架微扰幅度 | 同上段（Figure S1，正文未给数字细节） |
| 1.0（可超过） | Saturation 满值定义；羟基三键/双分支氢键时可 >1.0 | Methods, Ranking Results 段 |
| 0 | 四个新场景 top10 网络的重原子未满足数（全体） | Results, New Design Cases 段 |
| 10^4 → 10^5 | 对称复跑案例轨迹数的有效提升 | Results, Symmetric Homo-Oligomer Benchmarks 段 |
| Xeon E5-2680 v4 @ 2.40GHz（Longleaf 集群） | 基准硬件 | Benchmarks 末段 |
| 2751–2760；2018-09-17 Correction | 卷期页码（文头块）；投稿后更正声明（PMID 30221938，内容未取回） | 文头元数据 |

## 5. 结论——作者说了什么

1. **速度与质量双改进**："MC HBNet is able to sample hydrogen bond networks faster and more effectively than HBNet."，且能吃下更大的 rotamer 库："We show that MC HBNet is able to recapitulate the networks of native protein-protein interfaces, and that it can be robustly used with large rotamer libraries."
2. **复现与扩展**："The sampling protocol we describe here not only recapitulates previously validated designs with performance improvements, but also yields viable hydrogen bond networks for cases where the previous method fails, such as the design of large, asymmetric interfaces relevant to engineering protein-based therapeutics."——注意实验验证的归属："The protocol builds on a recently developed method in Rosetta for designing hydrogen bond networks that has been experimentally validated for small symmetric systems, but was not extensible to many larger protein structures and complexes."（湿实验证据属于前作 Boyken 2016，不属于本文）。
3. **框架无关性主张**："We have implemented MC HBNet within the Rosetta modeling package, but the sampling strategy, data structures, and network selection criteria described here are general, and could be straight forwardly implemented within other computational frameworks."
4. **定位是多阶段管线的快速前置件**："One of our primary motivations for developing MC HBNet was to create a robust protocol that could be used as part of a larger pipeline aimed at de novo interface design."，理由："When designing new protein-protein interactions it is generally not clear a priori what will be the most favorable way to dock the proteins against each other."，"It is important that the sequence search be rapid and reliably produce low energy solutions so that many alternative docked positions can be sampled."
5. **展望**："These improvements will allow explicit hydrogen bond network design to be incorporated into more complex, multi-stage protocols such as de novo interface design and enzyme design, and are general strategies that can be readily incorporated into modeling packages other than Rosetta."；"In addition to interface design, this type of protocol should prove useful for designing ligand binding sites and catalytic sites that require hydrogen bond networks to stabilize the ligand or transition state."——酶/过渡态只是展望级表述，本文无任何酶设计实例。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文真正的贡献是把"合作性"编译进搜索空间**：判据不再靠能量函数事后相加，而是靠图结构保证——边只连接"能成氢键且互不打架"的 rotamer 对，生长只走合法路径。这是"生成端可达性"与 B09 那条"评估端预测器"路线的互补：前者不需要打分器对多体效应外推，后者不需要改生成器。
2. **"命中"口径必须盯死**：本文没有任何湿实验，其"成功"= 复现 4 个旧实验验证设计 + 天然网络可恢复 + 比旧法快。引用它时只能引用**判据结构与工程折中**，绝不能把它的"top10 网络 0 unsat"当成"设计会折叠/会工作"的概率证据。
3. **过滤器的分层是一条可直接抄的工程原则**：重原子埋藏未满足=硬剔除；氢原子埋藏未满足=保留但罚分；羟基=单边满足即豁免。对应到我们的漏斗：**化学事件不可缺的相互作用进硬闸，只起稳定作用降级为排序项**——两者混在一个总分里是最常见的判据污染。
4. **"天然恢复率"是给判据本身做的阳性包含门**：先用 2776 条已知网络证明"我的采样表示得出现实"，再谈设计。任何我们的化学事件约束工具都欠这一步（我们 A5 轴盲测 AUROC 0.25 就是缺这道门的后果）。
5. **硬约束是一条会被"消化"的中间路线**：同一判据后来被 B04 改造成可两两分解的惩罚项（塞进组合打包打分），再被吸收进 ProteinMPNN/LigandMPNN 的序列似然（见 sources/baker.md:66）——说明"专用采样器"的长期归宿是并入通用打分/生成器；我们选前置硬约束时应预留"以后能不能变成打分项"的退路。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自述的失败模式/局限**

1. 旧法（HBNet）在非界面、大搜索空间场景的失败："The sample space of all possible hydrogen bond networks grows dramatically when the requirement of crossing an interface is removed."，"Our experience in using HBNet for non-interface designs has often resulted in unreasonably long runtimes"，而且调参负担转嫁给用户："This issue can be partially alleviated by manipulating user-defined options, but it is not always obvious to the user how to implement this effectively."
2. MC 是不完备搜索：没有收敛判据，轨迹数靠试——"MC HBNet benefits noticeably by increasing the number of Monte Carlo trajectories from the default of 10 4 to 10 5 for these symmetric cases."（默认值在他们的对称案例上不够好）。
3. 骨架刚性代价：网络捕获对 ~0.1 RMSD 的骨架微扰敏感（§2.4 已引），柔性骨架整合只是展望。
4. 基准的度量不完整：591 例聚合基准 "The only metrics we tracked were the runtimes for HBNet and MC HBNet (using 10 4 trajectories)."——只比了时间，没比质量；质量结论只建立在 4+4 个案例上。
5. 本文无湿实验：实验背书全部来自旧论文的小对称体系（§5.2 所引），大界面/蛋白内部的新网络**送没送测？本文根本没送测**——"送测与命中"在这篇里的全部含义是计算基准上的复现与恢复。
6. 版本风险：本地为 NIHMS 作者手稿，文头登记了 2018-09-17 的 Correction（PMID 30221938），更正内容未取回，无法排除个别数值在正式版被修正。

**我们读出的**

1. 阈值全是工程约定，无敏感性分析：-0.5 REU 成边、-0.4 REU 恢复容差、B factor 40、羟基单边豁免——原文均未给"换成别的数结论怎么变"。
2. 排序的现实承重是软量：四个新场景里 "All of the top networks reported had 0 unsatisfied polar atoms (which is the first metric used to sort results), meaning that Saturation was the primary determinant in the ranking of the networks and assessing network quality."——第一级硬判据全部打平，网络好坏实际由 Saturation（几何饱和度）决定，而它与可折叠性/可表达性无直接证据链。
3. "封闭"预设了可设计位点集合已知；位点集合本身未知的问题（我们的情形）本文不解决。

## 8. 对 UAA 筛选（S0/S1/S2 化学事件）的迁移判断

**核心问题：这种"把关键相互作用前置成硬约束"的思路能不能搬给我们的 S0/S1/S2？——能搬的是它的形式化方法和验证次序，不能搬的是它的数值判据和对"封闭"的充分性假设。**

**可迁移（怎么用）**

1. **事件的同时满足性可以"编译"成生成端硬约束**。HBNet 线的形式化是：不打分，而是只允许"每个埋藏极性都有氢键伙伴"的组合被生成（封闭网络），搜索空间预先被图结构裁剪。对 S0/S1/S2 的对应做法：把每个化学事件拆成必须**同时**成立的几何要件集合（例如 S1 的 pppUA 形成要求亲核原子—αP 距离/角度、离去基团稳定基、口袋内埋藏极性中和这几项同真），在序列×rotamer 生成阶段就只产出全要件闭合的组合，不闭合的组合根本不进漏斗——这与 B09 的事后 AF2 判别是互补位置：**一个管"可达"，一个管"可信"**。
2. **三级过滤器分层**（§6.3）：不可缺要件=硬剔除（对应 heavy unsat），有害但非致命=罚分保留（对应 buried 氢原子未满足），物理上正当的单边豁免=明确列出（对应羟基只需捐或受）。我们给 S0/S1/S2 定约束时必须先把每件事分进这三档，混进一个加权总分就是判据污染。
3. **判据先过"阳性包含"考卷再上岗**：本文用 2776 条天然界面网络测"我的采样表示得出现实吗"（双阈值 -0.5/-0.4 REU 的恢复判据）。对应动作：任何化学事件约束在用于筛选候选前，先在"公认做过该事件的已知结构"面板上测恢复率；恢复不了就改约束或改采样粒度，而不是先去筛候选。我们 A5 轴盲测低于随机的教训，正是缺这道门的代价。
4. **复跑旧成功设计当回归测试**：对称复跑 4 例（5J0K/5J10/5J0H/5IZS）的作用是"改动协议后仍能复现已知阳性"。我们应固定一组"事件已知为正"的案例（如参考酶的已知活性构象），每次改判据/改环境后先跑它们。
5. **前置硬约束的价值以管线吞吐计**：MC 把"周级"降到"分钟级～1 CPU 小时"（§3 表 7/8 行）不是为了省时间本身，而是让"多对接姿态 × 快序列搜索"成为可能。我们若加事件约束这道闸，也要按"每放行 1 个通过闸口的候选花多少核时"报效率（B09 卡同款原则），否则前置约束挤掉探索多样性就是亏的。

**不可迁移（为什么不能照搬）**

1. **数值判据零对应**：-0.5/-0.4 REU 是 Rosetta 氢键势的经验阈值，5-6 kcal/mol 是他人文献的估计——我们的栈里没有同一把尺子；埋藏性定义（cone 计数）也是为界面/核心设计的。把这些数字搬来当 S0/S1/S2 阈值属于无依据移植（与"binder 的 pAE/ipTM 阈值不得当酶活判据"同一条禁令）。
2. **"封闭"不蕴含"会反应"**：氢键闭合是静态几何满足，化学事件涉及断键/成键与质子转移；作者自己只把酶/过渡态写成展望（"should prove useful"），全文无一个酶设计实例。前置约束至多给出"几何上未被排除"的候选，判定仍需 QM 一维剖面（我们已冻结的 P4 xTB 路线）与湿实验，不能以闭合率替代反应可行性。
3. **骨架刚性假设对酶活性位点更不利**：催化位点常要诱导契合，本文实测 ~0.1 RMSD 微扰就改变可捕获网络集；界面案例尚且如此，口袋案例只会更糟，而"骨架柔性 × 网络搜索"的联合方法本文未解决。我们若要前置硬约束，必须自带骨架集（多构象）而不是单一晶体/模型构象。
4. **不许引用任何"命中率"**：这篇没有实验命中率；任何"S0/S1/S2 前置约束后成功率 X%"的说法都没有本文（或本卡）来源，禁止出现。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K65_PMC5940506_text.txt

- 本地纯文本：Europe PMC fullTextXML（NCBI efetch 兜底记录见 batches.tsv）去标签、实体解码、空白折叠后的单行文本（48,461 字符），与同目录 `K65_PMC5940506_fullTextXML.xml` 同源；门禁只拿上面声明的这一份逐字比对全部引句。本地版为 NIHMS 作者手稿，含 2018-09-17 Correction 的登记行但无更正内容（见 §0、§7）。
- 对照底稿：`sources/baker.md:66`（[B04] 条目的上游锚点行，判据演进链 Boyken 2016 → 本文 → Coventry & Baker 2021 → MPNN 序列似然）；CSV K65 行（编号、DOI 10.1021/acs.jctc.8b00033、PMCID PMC5940506，Crossref 已核验）。
- CSV 字段映射：本文第 3 节 ↔ 计算筛选判据/阈值数字；第 4 节 ↔ 成本/统计；第 7、8 节 ↔ 在方法演进链的位置。
- 引句纪律执行情况：全部引句从底稿复制粘贴；两处原文句中内嵌引文编号（5-6 kcal/mol 句带编号 21；HBNetStapleInterface 句带编号 26）与一处带 Figure 引用的句子，均按规则只截取编号前/后片段或拆分为独立引句；文头另登记一条更正声明（PMID 30221938），本卡未引用其内容。
- **本卡自检**：`scripts/verify_literature_cards.py --only K65 --no-report` 的结果见该命令输出与下方门禁记录。

<!--CSV回填
work_type=论文（方法学：MC HBNet 采样协议，全文无新湿实验）
target=蛋白-蛋白界面与蛋白内部的埋藏氢键网络设计；基准为 1YRK/1DPJ/1GK9 单侧界面、3U3B 单体核心、对称复跑 5J0K/5J10/5J0H/5IZS、591 例聚合计时
backbone_generation=不生成骨架：输入实验/设计骨架且全程固定，只在给定骨架上采样 序列×rotamer（backbone-dependent 库 + extra chi ±1σ 档 Ø…χ1χ2χ3χ4）
computational_filters=封闭网络硬约束（埋藏重极性原子未满足数=0 才登记）；HbondGraph 边判据=氢键能量<-0.5 REU；事后过滤：序列冗余去重、埋藏重极性未供未受即删、羟基单边豁免、自定义准则；排序=Num_Unsat_Hpol→Saturation→HBNet Score（丙氨酸背景上的全能量差/残基数）
thresholds=成边 <-0.5 REU（典型 -0.5~-1.5 REU）；天然恢复 ≤-0.5 REU 须重建至 ≤-0.4 REU；B factor>40 Å² 剔除；Pisces ≤60% id/≤2.0 Å/R≤0.3/长度40-10000；默认 10^4 轨迹（测 10^3-10^6）；24 小时超时上限；Saturation 满值 1.0
md_used=否（Backrub 骨架集仅用于 Figure S1 的敏感性演示，非动力学模拟）
qm_used=否（5-6 kcal/mol 埋藏未满足代价为引文估计，非量子化学计算）
experimental_methods=本文无新湿实验；验证=2776 条天然界面网络恢复基准 + HBNet/MC 耗时·内存·Saturation 对照 + 复跑 4 个此前已被晶体结构验证的对称 HBNet 设计（Boyken 2016 Science）
pipeline_counts=Pisces 修剪→含界面结构→2776 条天然网络；4 设计场景（40/121/342/23 可打包位点）×{Ø,χ1,χ1χ2}×轨迹 10^3-10^6；591 例 Ø 档计时基准；输出网络总数原文未给
hit_rate=无实验命中率（纯计算基准）；χ1χ2 档天然网络恢复分数倍于 Ø（>3×）；四个新场景 top10 网络 heavy unsat 全为 0；对称案例 MC 复现先前验证的网络
best_metric=未记录（本文无结合/表达/活性度量；计算侧最优读数=MC 全部运行 <1 CPU 小时 vs HBNet 多数 24 小时超时，界面采样一般 <1 分钟）
cost_or_stat_note=Longleaf 集群 Xeon E5-2680 v4 @2.40GHz；未满足即早退省约 40% 运行时间；MC 内存占用略低于 HBNet；对称案例默认 10^4 轨迹不足、10^5 才明显改善
role_in_timeline=HBnet 判据演进链的中段：Boyken 2016 Science（HBNet 穷举+对称体系实验验证）→ 本文 2018（MC HBNet 解决规模化，使埋藏氢键网络约束可嵌入 de novo 界面/酶设计多阶段管线）→ Coventry & Baker 2021（B04，把同一要求改造成可两两分解惩罚项）→ 吸收进 ProteinMPNN/LigandMPNN 序列似然（sources/baker.md:66）
source_pointer=data/literature_cards/fulltext/K65_PMC5940506_text.txt（声明底稿）+ 同目录 fullTextXML.xml；sources/baker.md:66；DOI 10.1021/acs.jctc.8b00033
CSV回填-->
