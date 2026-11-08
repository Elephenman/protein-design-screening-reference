# [B01] 用 Rosetta 物理设计把"别构开关"做成可编程零件——LOCKR（Cage–Latch–Key）三态热力学设计

Langan R, Boyken S, Ng A, Samson J, Dods G, Westbrook A, Nguyen T, Lajoie M, Chen Z, Berger S, Mulligan V, Dueber J, Novak W, El-Samad H, Baker D（UW-IPD / UCSF / UC Berkeley / Wabash College）
Nature 2019, 572:205-210 · DOI 10.1038/s41586-019-1432-8 · PMID 31341284 · PMCID PMC6733528
开放获取（HHMI author manuscript）· 全文链接 https://pmc.ncbi.nlm.nih.gov/articles/PMC6733528/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B01**（组：Baker组） |
| 本文取回方式 | Europe PMC `fullTextXML`（PMC6733528，author manuscript 版），2026-10-16 本地抓取 |
| 本地全文 | `data/interim/baker_lit/ft/switches2019.txt`（67,680 B；标签剥离后 67,237 字符） |
| 对照底稿 | `sources/baker.md` 第 13–25 行（原卡），本卡在其基础上补：三态模型的阈值语义、HBnet 正交化协议、toehold 调参系列、nesLOCKR 聚集伪影、HEK293T 非对称改造、代码与质粒存档号 |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中；见第 9 节自检） |
| 未取到的部分 | Supplementary Information 与 Supplementary Tables 1/4/5/6（本地全文里只剩 `Supplementary Material 1 6 7 8 9 10 11 12 13 2 3 4 5` 一行占位）。**正文多次把设计阈值与筛除判据推给 SI（原文写法是 see Supplementary Information），因此本卡第 3 节的判据列只能给"正文明写的"那部分，其余标"原文未在正文给阈值"** |

## 1. 这篇到底解决什么（大白话）

以前的 de novo 设计做的是"折成一个稳定形状"，靠的是把目标态能量压得越低越好。这篇要做的是**反方向的事**：让一个蛋白在**两个状态之间**待得住——一个"关"（Latch 自己贴在 Cage 上）、一个"开"（外加的 Key 把 Latch 挤下来，让 Latch 上的功能肽去干活），而且两个态的自由能差必须**小到能被外加的 Key 拨动**，又不能小到 spontaneous 漏开。作者的做法是：不去造别构远程调控（难），而是把竞争放到**同一个结合位点**上（分子内 Latch 贴 Cage vs 分子间 Key 贴 Cage），这样两个态的相互作用残基几乎相同，自由能差就变成可算、可调的量。然后给这套骨架装三种"货物"：凋亡肽 Bim（体外结合）、cODC 降解子（酵母/HEK293T 里控蛋白量）、NES（酵母里控核质分布），并用**埋藏氢键网络（HBnet）换一套供受体**做出互不识别的正交对。它是 Rosetta 物理能量时代"功能设计"的天花板样本，也是本 CSV 里"设计成本与判据全靠人工热力学调参"的锚点。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **"多态都要低能"与物理设计的根本目标相反**。原文把困难写实了：蛋白开关设计之所以难，"as it requires explicit design of multiple states with comparable free energies"，并且"Designing proteins that can switch conformations is more challenging,"——此前"a method for the de novo design of modular,"。
   **应对**：把问题**降维成同位点竞争**——"programming free energy differences between two states is more straightforward in a system governed"，并挑一个本身已被证明可稳定设计的框架（五螺旋 cage）而不是新造骨架。
   **留下的代价**：整个系统被三个解离常数（K_open、K_LT、K_CK）支配，**任何一个货物换进去都要重新热力学调一遍**；作者没有给出可自动筛选"哪些设计是开关"的计算判据（正文只说设计参数与筛选见 SI）。
2. **"关不严"是第一代设计的实际死因**（Extended Data Fig 3d 图注直说）："Early versions of the switch, with aBcl2 and pBim did not efficiently cage Bcl2 binding in the off state." 紧接着"They also only weakly bound the Key leading to small dynamic range."——即关态漏、开态弱，两头都不行。
   **应对（三条并行改协议）**：① 加长界面以扩大可调范围，"we expanded the available interaction surface area for the Cage:Latch and Cage:Key interactions by"，理由是"taking advantage of the modular nature of parametric de novo helical bundles"；② 弱化 Latch 自身（见第 4 条 serine 突变与 toehold）；③ 重新选择 graft 的**螺旋相位（register）**，把 Bcl2 结合残基埋进 Cage-Latch 界面而不是暴露在外（图注对比了 "a well caged graft where important binding residues are caged" 与 "a poor graft where Bcl2 binding residues are"）。
   **留下的代价**：这些应对全是**逐个设计体试出来的**（Extended Data 3/5/6/8 一整片剂量响应矩阵），不是筛子；正文没有"N 个设计里淘汰多少个"的分母。
3. **分子内 Latch 天然打不过？反过来说，Key 打不过 Latch**。作者用一条物理不等式解释为什么六螺旋（含 cis-Latch）框架不结合外加 GFP-Key：如果界面相同、linker 不受力，"the intramolecular interaction should outcompete"。实测正是"The five-helix framework,"。
   **应对**：不去加强 Key，而是**削弱 Latch**——"To enable the Key to outcompete the Latch,"，具体是双 serine 突变："A Cage-Latch framework with two serine"，机理推测为"the two serines likely weaken the Cage-Latch"。
   **留下的代价**：削弱是有账要还的——同一句里作者承认改造后"the guanidine hydrochloride denaturation midpoint"，即**开关的可调性是用稳定性换来的**（他们靠 cage 本身hyperstable，能在 5 M 变性剂下保持折叠来吸收这个损失）。
4. **同一功能要能被不同 Key 独立打开（正交性）**。这是活细胞多路调控的硬需求："To enable independent caging and specific"。**应对**：用 HBnet 换供受体对（核心思路句："we chose to design interfaces containing buried"）。**代价**：正交性不是设计出来的、是**测出来的**——只有 a 与 c 组成正交对，b 这一路在降解子实验里直接不出活（"degronLOCKR a and degronLOCKR c were strongly" 而正文注明 "LOCKR b did not activate"），且 Key b 对 Switch a/c 都有弱串扰。
5. **体内读数会碰上"假信号"**。nesLOCKR 实验里出现 YFP 胞质颗粒："punctae of YFP fluorescence is observed when both YFP-nesSwitch a and Key-BFP are expressed in the cytosol, which we assume is due to aggregation of the nesSwitch a"——注意措辞是 we assume，作者没有做抗聚集验证；同时他们还发现 Key 上带强 NLS 时结果与不带 NLS 一致，据此论证 uncaging 不依赖 Key 的定位。
   **应对**：加**双读数**（YFP 定位 + HTA2-RFP 核标记）与 Key 荧光作为表达对照，把"Key 没表达"与"开关没开"分开；正文另有一句支撑："Key fluorescence was independent of degronSwitch"，用以排除 Key 被一起降解。
   **留下的代价**：聚集这一解释停留在我方推测级别，正文未给去除聚集的方案。
6. **哺乳细胞里对称设计动态范围不够**。**应对**：重做成非对称 cage 并扫 toehold 长度——"A redesigned asymmetric degronSwitch a with an"，最终"triggered a 11-fold reduction in mean RFP"；图注给出比较口径"Asymmetric cage with a t8 toehold demonstrates"。
   **留下的代价**：酵母里最好的是 12-aa toehold，HEK293T 里最好的是 t8 非对称——**同一个 Switch 的最优参数跨细胞系迁移失败**，只能逐个重调（Extended Data 5d/8）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **骨架生成**：Rosetta 物理设计；起点是已发表的氢键网络介导的螺旋束三聚体（正文写法是 "a designed homo-trimer of"），用设计的短无序 loop 把亚基连成单体框架（五螺旋=Cage，六螺旋=Cage+Latch）。**选它的理由**：螺旋界面"are dominated by sidechain-sidechain interactions, which can be more readily tuned than the backbone hydrogen-bonding interactions between β-strands"——可调范围宽。
- **特异性来源**：埋藏氢键网络（HBnet），换供受体即换特异性，用于做正交对。
- **理论层（本文真正的"筛子"）**：**三态结合平衡模型**，K_open（Latch 从 Cage 解离）、K_LT（Latch 结合 Target）、K_CK（Cage 结合 Key）；作者先做数值解再做设计（Fig 1b 给不同 K_LT 与 K_open 下的响应曲线族）。
- **序列/突变层**：Latch 上 serine 取代调 K_open；helix 加长（5/9/18 残基）与 toehold 长度调 K_CK 与动态范围；graft register 决定关态是否漏。
- **实验层**：SEC、CD、GdmCl 变性曲线、SAXS（含 FoXS 拟合设计模型）、GFP pull-down 96 孔荧光、BLI（Octet RED96、SA 传感器、1:1 拟合）、酵母双诱导（E2/Pg 滴度矩阵）+ 流式、自动化连续培养测动力学、HEK293T 慢病毒转导 + 流式、共聚焦/荧光成像。
- **没有用的方法**：MD、QM、结构预测网络自洽性判据（2019 年还没有这套）、也没有展示库 + NGS 的大规模计算筛除。设计淘汰标准在 SI，正文不含阈值。

### 工作流（正文可复现顺序）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 | 目标：让某功能肽"只在加 Key 时可用" | 用三态模型先算清什么参数区间是开关，再动手设计 | 正文明写了两条失效边界："the system binds Target in the presence of little to no Key and the fold induction by Key is low"（Latch-Cage 太弱→关不住）与"the system only partially binds Target even at high Key concentrations"（Latch-Cage 太强→开不满）；且"The Latch-Cage interaction affinity that gives optimal switching" 是 K_LT 的函数 | 得到"K_LT 定 K_open 目标"的设计准则（Fig 1b；K_LT 取 1 nM 与 50 nM 两栏，K_open 从 0.1 到 1e-9 五档，K_CK 固定 1 nM） |
| 2 | 5L6HC3_1 三聚体 | Rosetta 设计 loop 把三聚体连成单体五螺旋/六螺旋框架 | 正文未给计算阈值；验收用实验：单体性（SEC）、折叠性（CD、GdmCl）、结构一致（SAXS 拟合） | 两个框架；两者"expressed in E. coli were"、"remain folded up to 5 M guanidine hydrochloride"；SAXS 与起始三聚体类似，五螺旋偏差最大（作者归因"the loss of a helix"） |
| 3 | 五/六螺旋框架 | GFP pull-down 检验分子间 Key 能否结合 | 六螺旋必须不结合（对照），五螺旋必须结合 | 结论句："The five-helix framework,"（n=3 技术重复） |
| 4 | 五螺旋 Cage + Latch | 在 Latch 上引入弱化突变（V223S/I238S），必要时给 Key 造 toehold | 判据是"Key 结合强度≈无 Latch 的截短 Cage" | "A Cage-Latch framework with two"；代价是稳定性下降（见第 2 节第 3 条） |
| 5 | 已调好的 base LOCKR | 把功能肽装进 Latch：选三种 Bcl2 结合肽、采样不同 helical register，使 Bcl2 结合残基被埋进 Cage-Latch 界面 | 埋藏准则（原文）："optimizing for the burial of"；肽的选择准则："were chosen to sample a range" | 采样 3 条肽 × 多个 register；aBcl2/pBim 早期版本失败，全长按 18 残基加长后"fully off in the absence of Key" |
| 6 | 加长版 Switch + 全/截短 Key | 定"最强诱导"组合，并做剂量响应 | 正文给的实测值："Strongest inducible binding was observed with a Latch truncated by 9 residues and a full-length Key"；"the Key buries more surface" | "Addition of Key activated"；BLI 拟合出 EC50："a 40-residue Key produces no"、"and the full-length 58 residue" |
| 7 | 同一 Switch 对不同亲和 Target | 用 Bcl2/BclB/Bak 三个 K_LT 检验模型预测 | 先测非笼 Bim 对三者的 K_d（0.17 nM、20 nM、4.2 μM），再看激活所需 Key 浓度是否随 K_LT 上移 | 与模型一致："activation of BclB binding"；作者总结"The equilibria involved in" |
| 8 | base LOCKR 界面 | 换 HBnet（不同氢键供受体排布）做正交对 | 验收口径："each Switch is activated only" | "Designs BimLOCKR b and BimLOCKR"（正交对 a/c 成立；b 在细胞实验里不出活） |
| 9 | 关态货物换成 cODC 降解子 | 三种 cODC 变体（野生型 / 去掉 destabilizing proline / 仅中心二肽 CA）× toehold 长度扫描，在酵母双诱导系统里表达 YFP-Switch 与 Key-BFP | 验收=动态范围最大者；正文写法："We optimized the amount of" | "and found the Switch with"（degronSwitch a）；短 Key（43 aa）需更高 Key 浓度才到顶："but a higher Key concentration" |
| 10 | degronSwitch a | 用自动化连续培养 + 流式测激活动力学 | 稳态判据：作者读数"reaching a new steady-state in" | 折算降解半衰期："we estimate a 24 minute half-life for activated degronSwitch a"，与前报 cODC 的 11–30 分钟同量级 |
| 11 | 同一细胞共表达 two degronLOCKRs | YFP-degronSwitch a + RFP-degronSwitch c _constitutively_ 表达，分别滴 Key a / Key c | 正交判据：只有对应 Key 能降对应货物 | "Expression of Key a led to"（Key c 反之） |
| 12 | 移植到哺乳细胞 | HEK293T 慢病毒转导表达 RFP-degronSwitch + Key-BFP；对称版不够用，改非对称 cage 再扫 toehold | 判据=11 倍荧光下降与最大动态范围 | "A redesigned asymmetric degronSwitch a with an 8-residue toehold"，"triggered a 11-fold reduction" |
| 13 | degronLOCKR 接到转录机器 | 分别笼住合成转录因子 synTF-RFP 与 dCas9-VP64，用 YFP 报告基因读转录输出 | 报告口径：转录因子本体（RFP）与下游输出（YFP）同时报 | synTF："Key induction triggered a 61%"；dCas9："A 78% reduction of RFP and 41%" |
| 14 | 换第三类货物：NES | 把核输出序列按同一策略笼进 Latch，融合 YFP-NLS-nesSwitch a，核标记 HTA2-RFP | 定位判据（图像 + 转录输出） | "the YFP fluorescence becomes"；核内转录因子版本："induction of Key caused a 33%"；同时暴露聚集伪影（第 2 节第 5 条） |
| 15 | 结构一致性核对 | SAXS 与设计模型比对；**注意为对齐实测序列，先补建模标签** | "The hexahistidine tags and"；构象柔性处理："100 independent models were" | FoXS chi 值列于 Extended Data Fig 1c |
| 16 | BLI 定量 | Bcl2-biotin 上样 SA 传感器，梯度 Key/梯度 Switch 结合 | 上样阈值："Biotinylated Bcl2 was loaded"；拟合模型："Kinetic constants and response" | 全文 BLI 数据的主来源（Fig 2、Extended Data 2/4） |

**这套流程的骨架值得单独记住**：先**写一个能把失败模式画成曲线的解析模型**（步骤 1，K_open/K_LT/K_CK），再用模型指示"往哪个方向调参数"（步骤 4/5/6/9），最后**每个新货物/新细胞系都重跑一遍调参矩阵**。它是"模型驱动 + 人工调参"的极端样本——没有任何自动判据把设计批量削掉。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 40-fold（over forty-fold） | Key 诱导的最大激活倍数（体外 Bim-Bcl2） | "Addition of Key activated" |
| 230 +/− 58 nM | 45-aa Key 激活 BimLOCKR 的 EC50 | "a 45-residue Key activates with" |
| 27.0 +/− 2.8 nM | 58-aa 全长 Key 的 EC50（40-aa Key 无激活） | "and the full-length 58 residue" |
| 0.17 nM / 20 nM / 4.2 μM | 非笼 Bim 对 Bcl2 / BclB / Bak 的 K_d（决定 K_LT 跨度） | "Bcl2, BclB, and Bak bind" |
| 22-fold / 8-fold | BimLOCKR b / c 与各自 Key 的激活倍数 | "Designs BimLOCKR b and BimLOCKR" |
| 5 μM | 正交性检验所用 Key 浓度上限 | "each Switch is activated only" |
| 5-, 9-, 18-residues | Cage/Latch/Key 加长档位（扩大界面、调 K_CK） | "lengthening the helices in the" |
| 12-residue（酵母） / 8-residue t8（HEK293T） | 各自最优 toehold 长度 | "found the Switch with proline" |
| ~3 hours / 24 minute / 11–30 分钟 | 激活后达新稳态时间 / 估的半衰期 / 文献 cODC 半衰期 | "reaching a new steady-state in" |
| 11-fold | HEK293T 中 RFP 荧光下降倍数 | "triggered a 11-fold reduction" |
| 61% / 82% | synTF（RFP）与下游 YFP 下降 | "Key induction triggered a 61%" |
| 78% / 41% | dCas9-VP64（RFP）与下游 YFP 下降 | "A 78% reduction of RFP and 41%" |
| 33% | nesLOCKR 控制的 YFP 下降 | "induction of Key caused a 33%" |
| 5 M | GdmCl 耐受（cage 骨架 hyperstable 的量化） | "remain folded up to 5 M guanidine hydrochloride" |
| V223S/I238S | 使 Key 能与 Latch 竞争的双 serine 突变 | "A Cage-Latch framework with two" |
| 100 个模型 | Rosetta Remodel 采样数（SAXS 拟合前补标签） | "100 independent models were" |
| 0.5 nm | BLI 生物素上样阈值 | "loaded onto the SA tips to a" |
| 3 条 Bim 肽 / 3 种 cODC 变体 | 每次"装货物"实际采样的组合数 | "Three Bcl2 binding peptides" ; "was used to embed three variants of cODC into Switch a" |
| 未记录 | 设计→下单→命中的漏斗分母（正文无统一口径） | 见第 9 节；SI 未取得 |

## 5. 结论——作者说了什么

1. 做出了可切换的全新蛋白系统：正文明说这是里程碑式推进——"The design of switchable"，能力口径是"We describe orthogonal Cage-Key"。
2. 三态模型**在活细胞里也成立**：作者用短/长 Key 的剂量响应差异论证"suggesting the Fig 1a model"。
3. HBnet 是达到特异性的关键手段：正文写法"illustrating the power of the"。
4. 相对天然蛋白改造的优势在**通用与可调**：作者主张"A number of proteins, including"但"Strategies that rely on repurposing natural proteins have modularity and tunability limited by the evolved functions and ligands of these existing proteins, whereas altering the affinities of LOCKR components is tunable based on simple design principles that are generally irrespective of the functional modality or application"。
5. 作者自认的边界（第 2 节汇总）：LOCKR b 在细胞里不出活；nesLOCKR 有聚集体无法解释；最优 toehold 因细胞系而变；稳定性被 Latch 削弱牺牲；设计阈值与筛除判据放在 SI，正文不提供可复用数字。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文的"计算筛子"其实是热力学不等式，不是打分函数**。他们能把"关不住/开不满"写成 K_open 与 K_LT 的函数曲线族，再反过来定设计目标——这比任何单点能量打分更接近"可执行的设计规格"。→ 对我们：酶设计筛选也应该有一个这样的**事件平衡式**（分步化学事件相对自由能与竞争副产物通量），而不是只堆 pLDDT/能量项。
2. **"可调性用稳定性换"是本类设计的通用代价**。serine 弱化 Latch 与 toehold 都在牺牲折叠自由能，他们靠骨架本身极端稳定（5 M GdmCl）扛住。→ 对我们：如果为了催化几何而牺牲可溶性/稳定性，就必须先确认底架有足够"稳定预算"可以花，否则改造一定以表达量崩掉收场。
3. **每个货物/每个细胞系都要重跑调参矩阵**（12-aa vs t8、a/c 正交但 b 死）。这说明他们的"平台化"只在**骨架层**成立，**功能层没有外推性**。→ 对我们：不要指望"一个判据在所有酶构建体上通用"，一轮实验的构建体数量预算要按功能类别分开算。
4. **正文没有漏斗分母这件事本身是信息**：2019 年的功能设计根本没把"设计多少个、淘汰多少"当作报告对象，命中率口径来自后来的深度学习论文回溯（本 CSV 的 [B06]/[B09]/[B05] 才开始量化）。→ 对我们：跨时代比"命中率"时必须先对齐口径，不能拿 LOCKR 的"40-fold 激活"和别人的"96→73→50"放同一张表。
5. **失败模式被作者明确归到"off-state 漏"与"dynamic range 小"两类**，且应对都是**结构尺寸层面（界面面积/toehold）**，不是能量权重层面。这与 [B09] 的 Type I/II 分型是同一思维的早期版本：先分型，再决定改哪一层。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者层面：无统一命中率分母；正交性靠逐个细胞实验确认（LOCKR b 失败）；聚集伪影仅"we assume"；稳定性与开关性的取舍没有理论上限；SI 阈值未进入正文，本文外部读者无法复算设计筛选。
- 我们读出：① 模型只覆盖三条平衡常数，**没有覆盖 Latch 的折叠态-未折叠态分布、也没有覆盖细胞内拥挤/降解通路**，dCas9 一路 RFP 降 78% 但 YFP 只降 41% 就是下游非线性的直接证据；② 激活倍数（40-fold、11-fold）与"设计质量"不是同一件事，它衡量的是**开关动态范围**，对全新靶点没有可迁移的通过阈值；③ 本文完全没有结构预测自洽性判据（2019），因此它不能为"AF2/pAE 类闸口"提供任何证据。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **"先写平衡式再设计"的组织方式**（对应本库判据 G0/G6 的"判据必须能说清它对应哪个物理量"）：把底物装载拆成可写的竞争性平衡（氨酰化 vs 脱笼 / 正确 tRNA vs 游离底物 / 单掺 vs 二掺），先算清"哪一段自由能差会让系统漏"，再去设计，而不是先造一大批再看结果。
2. **同位点竞争优于远程别构**——迁移含义：如果我们想给目标酶做"可开关"版本，应当设计**同一结合位点上的分子内/分子间竞争**（例如把催化残基所在的 loop 用可置换肽卡住），而不是指望远端突变诱导别构。
3. **"稳定预算"的概念**：本文靠 hyperstable cage 吸收削弱代价。→ 我们选天然参照酶做骨架时，应先量它的可溶/热稳定余量（Tm、SEC 单体比例），余量不足的骨架直接不进功能改造队列。
4. **失败分型（关不住 / 开不满 / 串扰）**：把候选标注成"漏（无产物背景）/ 不响应（无增量）/ 不特异（错配 tRNA 也认）"，与分步化学事件事件对应，允许写 UNKNOWN 与 METHOD_FAIL。

**不可迁移（为什么不能照搬）**

1. **40-fold、11-fold、EC50 230 nM 这些数字是"开关动态范围/亲和力"，不是"酶活"**。它们不能当目标酶的通过阈值，更不能折算成命中率（本库判据 §2 明禁借 binder/开关类阈值当酶活闸口）。
2. **LOCKR 的成功判据几乎全在湿实验层**（BLI/流式），正文没有计算筛除阈值，因此本文**不能为"计算漏斗该用哪个判据"提供任何定量答案**——它恰恰是后来深度学习论文要解决的"人工筛选成本高"的那个对象。
3. **三条平衡常数的模型不能移植到催化**：底物装载是化学步骤（过渡态、竞争亲核体），需要的是能垒与选择性，结合平衡模型没有这个自由度；想用类似平衡式，必须自己加化学事件项，且不能声称本文支持。
4. **哺乳/酵母内的调控读数（荧光下降%）与我们的产物化学读数（LC-MS/MS 掺入量）不同量纲**，不能相互标定。

## 9. 溯源与自检

- 本地纯文本：`data/interim/baker_lit/ft/switches2019.txt`（Europe PMC fullTextXML → 标签剥离 → `litcards_text.norm` 归一化，未改写内容）。
- 引句底稿: data/interim/baker_lit/ft/switches2019.txt
- 对照底稿行号：`sources/baker.md:13–25`；相关汇总表：`sources/baker.md:633`（Rosetta 静态打分 + MD 回顾性诊断对照段）、`sources/baker.md:672`（已记录"B01 漏斗分母正文未检索到"的缺口 1）。
- 引文原始指针（正文级）：摘要句 "We describe orthogonal Cage-Key"（PubMed 31341284）；方法代码 "Python scripts, bash scripts,"（正文 Code Availability）；质粒存档 Addgene 127416–127424、127200–127206、127246。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据`；第 4 节 ↔ `阈值数字/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only B01 --no-report` 把卡内所有不含中日韩字符、且被直双引号包住的 ≥20 字符片段，在本编号登记的全文与底稿里做逐字查找；结果见本次回报与 `data/literature_cards/rollout_status.tsv`（`--no-report` 模式下不落盘，打印行）。
- 诚实声明：`阈值数字=未记录` 的原因不是没读，而是正文本身把设计筛除判据放在未取得、不可解析的 Supplementary Information；本卡没有为补齐空格而编造阈值。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 69 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（de novo 别构蛋白开关的功能设计，方法学 + 合成生物学应用）
target=LOCKR 三态开关（Cage-Latch-Key）；货物依次为 Bim 凋亡肽（体外 Bcl2/BclB/Bak 结合）、cODC 降解子（酵母与 HEK293T 控蛋白量，含 synTF 与 dCas9-VP64 转录输出）、NES（酵母核质分布）
backbone_generation=Rosetta 物理设计：以 HBnet 介导的螺旋束三聚体 5L6HC3_1 为起点，设计短无序 loop 连成五螺旋 Cage / 六螺旋 Cage+Latch 单体框架；Ligand 层用 helix 加长（5/9/18 残基）、Latch 双 serine 突变（V223S/I238S）、graft register 采样与 toehold 长度调节三个平衡常数
computational_filters=三态结合平衡模型 K_open（Latch 从 Cage 解离）/ K_LT（Latch 结合 Target）/ K_CK（Cage 结合 Key）的数值解定设计目标；界面与特异性由埋藏氢键网络（HBnet，换供受体即换正交对）控制；正文未见自动能量筛除判据，具体筛除与阈值指向 Supplementary Information
thresholds=正文给出的实测数值：EC50 230 +/- 58 nM（45-aa Key）、27.0 +/- 2.8 nM（58-aa Key）、40-aa Key 无激活、正交性检验浓度上限 5 μM、BLI 上样阈值 0.5 nm、1:1 拟合模型、骨架耐受 5 M 盐酸胍；设计-筛除阈值=未记录（正文明写 see Supplementary Information，SI 本地未取得）
md_used=否
qm_used=否
experimental_methods=SEC、CD 波长扫描与 GdmCl 化学变性（拟合 ΔG 折叠）、SAXS + FoXS 比对设计模型（Rosetta Remodel 补 His 标签后 100 模型聚类取中心）、His 板 GFP pull-down、BLI（Octet RED96、SA 传感器、梯度 Key 剂量响应）、酵母双诱导（E2/Pg）+ 流式 + 自动化连续培养测动力学、HEK293T 慢病毒转导 + 流式、荧光显微（NES 定位）
pipeline_counts=未记录（正文无"设计 N / 下单 M / 命中 K"统一口径；已明确的实验采样规模为 3 条 Bcl2 结合肽 × 多 register、3 种 cODC 变体 × toehold 9/12/16 aa、对称与非对称 cage × t 长度两档、21 个设计中的功能验证按图计）
hit_rate=未记录（本文按"能否开关 + 正交"逐条判定，不报比例；给出的量级是功能读数：体外 40-fold 激活、b/c 亚基 22-fold 与 8-fold、HEK293T 11-fold 降解、酵母转录输出 82%/41%/33% 下降、dCas9 RFP 降 78%）
best_metric=未记录（无 Kd 或活性最优值的统一表；正文最好功能值=体外 Key 诱导 Bim-Bcl2 结合激活 over forty-fold，EC50 最低 27.0 +/- 2.8 nM（58-aa Key））
cost_or_stat_note=成本主要在人工热力学调参与剂量响应矩阵（Extended Data 3/5/6/8），本文未报 CPU/GPU 时长；每个货物与每个细胞系需重扫 toehold 与界面长度（酵母最优 12-aa，HEK293T 最优 t8 非对称）
role_in_timeline=2019 年"物理能量函数 + HBnet 多态设计"的终点样本：证明 Rosetta 时代能做出可编排的多态功能零件，但其筛选全靠人工调参、正文无漏斗分母与自动判据——正是 [B06]/[B09] 深度学习漏斗要解决的"筛选成本"对象；HBnet 与三态模型至今仍是人工设计别构/可控体系的参考做法
source_pointer=data/interim/baker_lit/ft/switches2019.txt（Europe PMC PMC6733528 fullTextXML，2026-10-16 抓取）；sources/baker.md:13-25；缺口记录 sources/baker.md:672；PubMed 31341284；Addgene 127416-127424 / 127200-127206 / 127246
CSV回填-->
