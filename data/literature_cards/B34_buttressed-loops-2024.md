# [B34] 给长环加扶壁——用重复蛋白把「设计长环」从不可能变成可批量

Hanlun Jiang, Kevin M. Jude, Kejia Wu, … L. Stewart, K. C. Garcia, D. Baker（华盛顿大学 IPD + 斯坦福；Jude/Garcia 在 Stanford Med）
Nature Chemical Biology 2024, 20:974–980 · DOI 10.1038/s41589-024-01632-2 · PMID 38816644 · PMCID PMC11288887
预印本 bioRxiv 10.1101/2023.08.22.554384（PMCID PMC10473674, PMID 37662224），2023-08-23 上线，2024-05-30 接收 · 开放获取 CC BY 4.0

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B34**（组：Baker组；state=FULLTEXT） |
| 本文底稿 | `data/interim/baker_lit/ft/buttressedloops2024.txt`（68,754 B；PMC11288887 正式版全文，非预印本版；据 `sources/baker.md:685`，这一篇是 46 篇批量缓存之后由内联脚本单独补抓的） |
| 对照底稿 | `sources/baker.md:443–460`（原卡）与 `sources/baker.md:644,659`（MD 进入入选判据的那一次） |
| 证据级别 | **全文级**（本卡全部引句在 §0 那一份本地全文里逐字命中，见第 9 节） |
| 未取到的部分 | Supplementary Table 1、Extended Data Fig. 1–4 的原图数字、Reporting Summary。**正文没有给出参数化骨架生成的模型总数、也没有给逐级过滤后各剩多少**——只有送实验的 102 条。凡涉及中间漏斗规模的地方本卡明写「原文未给数」 |
| 本卡重点 | ① 长环设计以前为什么不行 ② buttressing（扶壁）具体扶什么 ③ 计算判据与阈值（这篇是 Baker 组里判据最「物理」的一篇）④ 结构命中与功能命中各有各的分母，不能合在一起报 ⑤ 作者自己承认的边界 |

## 1. 这篇到底解决什么（大白话）

天然蛋白的功能位点（识别、信号传导、催化）很多是靠**结构化的环**去够底物的，但过去从头设计做不出「好几条听话的长环」，所以计算设计的结合蛋白几乎只会用α螺旋和β链搭界面，形状库被锁死。这篇的思路是：**不要指望一条环自己稳住，而是让它旁边的环和下面的螺旋一起把它「撑」住**（buttressing）——原文的说法是 "by computationally designing repeat proteins with multiple long loops buttressed by loop-loop interactions"。做法是把环做成带β转角的发夹状长环（灵感来自天然蛋白：他们观察到长环 "they frequently contain β turns with strand-like hydrogen bonds flanking the turn residues"，且 "natural proteins often use helix-capping interactions between the sidechain or backbone on the loop residue and the backbone of the helix from which it emanates"），要求环内至少 2 条主链-主链氢键、相邻环之间至少 1 条，再往环上装天冬酰胺/天冬氨酸/谷氨酰胺/组氨酸去形成侧链-主链**双齿氢键**，加上环-螺旋疏水接触与环内脯氨酸倾向。骨架用自建的**参数化重复蛋白生成器**产出（这样每个重复单元的环是同一个构象被复制 n 次，一次扶壁等于 n 次扶壁）。做完的结构叫 RBL（repeat proteins with buttressed loops），再拿它的凹槽去设计重复肽结合体——摘要的说法是 "in which the loops form one side of an extended binding pocket"，得到 nM 级肽结合体。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **长环本身就是设计难点，而且难点在「多」条**。摘要原句把问题定位得很准："organizing multiple structured loops at protein functional sites has been very difficult to achieve by de novo protein design"；正文更具体的因果句是：因为长环区天生柔、又没有成片的骨架氢键，所以结合蛋白设计一直退回到α螺旋/β链骨架（"which has limited the achievable local shape diversity"）。 → **他们做了什么**：不再单点设计一条环，而是换成重复蛋白架构，把同一条环构象传播到每个重复单元（"To install the loops of the same conformation in each unit of repeat proteins, we used the RepeatPropagationMover"），于是环的稳定来自「一整排环互相扶壁」而不是「一条环自稳」。代价：产物形状被限定在超螺旋重复蛋白这一族，不是任意骨架。
2. **老路子精度不够**。用前人片段组装法造α螺旋重复蛋白是可行的，但"we found that they did not provide sufficient control over backbone positions for designing loop buttressing"——扶壁要求环与环、环与螺旋之间的相对几何极其精确，位置漂了就搭不上氢键。 → **他们做了什么**：重写骨架生成器，"we developed a parametric repeat protein generation method that enables precise control over backbone placement"：两根理想螺旋（各 12–28 残基）之间采 6 个刚体自由度，重复单元之间再采 6 个，同一变换反复作用；序列相邻的螺旋之间用基于天然蛋白的 loop lookup 接上 3–6 残基的连接环。代价：阈值是试出来的——"In extensive model-building experiments, we found that to enable the installation of long loops onto these parametrically generated models, the termini of the helices had to be less than 18 Å apart"，另有堆积下限"fewer than 28% of the residues in a buried core"被剔除；原文未给这条路上生成/淘汰了多少模型。
3. **环长有一个窄窗口，窗口外这套办法不成立**。原文写得毫不含糊："We chose these lengths because we found limited structural diversity for loops with lengths less than nine amino acids"，紧接着一句（两句之间无插入编号，但为安全分成两条引）："When the loop length exceeded 14 amino acids, it became significantly more difficult to design buttressing interactions to stabilize the entire loop"。 → **他们做了什么**：把可设计环长锁死在 9–14 残基（摘要原话 "structured loops (9-14 residues) buttressed by extensive hydrogen bonding interactions"），并规定每条环必须采到β转角 + 螺旋帽 motif。代价：**真正的长环/柔顺环本文没有解决**，本文未解决；「酶活性位点要用 14 残基以上的环」这一类需求在这篇里没有答案。
4. **一步 rotamer 装箱常常装不出双齿氢键**。Methods 承认这条会失败："In the case where the one-step packing approach failed to generate any interloop bidentate hydrogen bonds, we used an alternative three-stage scheme to maximize the sampling efficiency of bidentate hydrogen bonds"。 → **他们做了什么**：三级兜底——先按几何判据找伪氢键（"We defined that a pseudo hydrogen bond has a donor-acceptor distance"、角度 >120°），再对环做对称最小化并加谐振距离约束（"we imposed a harmonic distance constraint between each donor and acceptor atoms with a target distance of 2 Å and a s.d. of 0.5 Å"），最后用 Rosetta 打分复核是否真形成。同时主动缩氨基酸字母表："We excluded amino acids with longer side chains (Arg and Lys), as their high entropic cost might diminish the free energy contribution of buttressing"。代价：可用残基被人为收窄到 Asn/Asp/Gln/His 四类，长侧链带来的互补性机会被整段放弃（原文没有量化这一放弃的代价）。
5. **MD 太贵，只配给前 10% 用**。原文："Top 10% scoring structures were further tested by in silico validation methods such as molecular dynamics simulations"，且 MD 与 AlphaFold / RoseTTAFold 是**三选一**的可替换手段（前句里三者并列），MD 协议为 GROMACS 2018.4 + Amber99SB-ILDN、每个模型三条 20 ns 轨迹。 → **他们做了什么**：把便宜且硬的 Rosetta 五项几何/能量过滤放在前面削量，贵的柔性检验放最后；刚性判据取 Cα RMSD < 3 Å。代价：原文**未给 MD 的通过率、未给三选一之间谁更严、也未报有多少设计仅因 MD 失败被淘汰**，所以「MD 在这里到底值多少」无法从本文判定。
6. **晶体长不出来 / 相位解不出，靠改寡聚态救**。RBL7 一开始"design was highly stable and monomeric, with an overall fold validated by SAXS"，但"We obtained crystals that diffracted poorly with the highest resolution at 4.2 Å."。RBL4 那边也有一个坑："Initial attempts using the predicted model were unsuccessful due to clashes." → **他们做了什么**：① 借前人观察"synthetic oligomerization can sometimes assist crystallization"，人为引入疏水二聚界面，重设计出 RBL7_C2_3，最终 3 Å 解出；② RBL4 的分子置换改成只搜单个 helix–loop–helix 重复（76–118 残基）的 8 个拷贝，再 Phenix AutoBuild 重建。代价：拿到的是「为结晶改造过的变体」的结构，不是最初设计；RBL7_C2_3 二聚体 Cα RMSD 2.9 Å 明显差于单体 1.6 Å，末端螺旋偏差最大（"The main discrepancies between the crystal and designed structures were in the terminal helices."）。
7. **重复单元之间的变换（曲率）设计不准，本文没有解决**。单元内部吻合极好，但"The primary discrepancy between the crystal structure and design model is in the inter-repeat transformation"——"the design model is slightly curved (smaller superhelical radius), while the crystal structure is nearly flat (larger superhelical radius)"。 → **他们做了什么**：没有纠正，只在报告口径上把整体 RMSD（1.7 Å）和单元内 RMSD（0.48–0.61 Å）分开列，用单元内数字支撑「环按设计折好」这一条主张。代价：**超螺旋半径/曲率不可预测**，而结合沟的宏观几何恰恰由曲率决定——这对「按靶形定制造型」的后续 binder 设计是直接风险，本文未解决。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **骨架**：自建的**参数化重复蛋白生成器**（Rosetta 2019.01 的 MakeBundleHelix + 用户指定刚体变换 + ConnectChainMover 天然 loop 查询）。选它是因为片段组装法给不了环扶壁需要的骨架位置精度。
- **环构象**：天然 motif 拼装 + **GeneralizedKIC** 运动学闭环；motif 库来自 PISCES 过滤后的 PDB 四残基片段 K-centers 聚类。
- **序列**：Rosetta 组合式序列设计（FastDesign，重复对称约束 4 轮 + 1 轮表面极性化），fa_rep 缓升促核心堆积，环区加轻微脯氨酸倾向。
- **过滤与验证**：Rosetta 五项物理判据（氢键不满足/空洞/总能量/packstat/氢键能）→ 前 10% 进 **MD（GROMACS + Amber99SB-ILDN，Cα RMSD < 3 Å）或 AlphaFold 或 RoseTTAFold（pLDDT > 80 且 Cα RMSD < 3 Å）三选一**。
- **功能化**：Rosetta 界面设计（沿用 Cao 2022 那套蛋白-蛋白设计方法）+ 复合物侧 **AlphaFold PAE_interaction ≤ 15**。
- **实验侧**：E. coli 表达 + IMAC/FPLC、SEC-MALS、变温 CD、SAXS（ALS SIBYLS 12.3.1）、X 射线晶体学（APS 23-ID-B）、split-luciferase（Nano-Glo）初筛、荧光偏倚测 Kd。
- **注意 MD 的定位**：这篇是 Baker 组文献里 MD 唯一一次进入**入选流程**（作为刚性检验，与 AF/RF 并列可替换，不是独立必过关口）；全文没有 QM/自由能微扰。

### 主流程（结构分支）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| S1 骨架生成 | 理想螺旋参数 | 建 H1/H2（各 12–28 残基）组成重复单元 R1；H1→H2 采 6 个刚体自由度；单元间再采 6 自由度并重复同一变换；ConnectChainMover 用 3–6 残基天然 loop 接序列相邻螺旋 | 待接两根螺旋的末端距离上限 **18 Å**（超过即删）；埋藏核心残基比例下限 **28%** | 参数化重复蛋白骨架模型集（**原文未给总数**） |
| S2 motif 库 | PDB | 按 PISCES **90% 最大序列同一性 + 1.6 Å 分辨率截止**筛 PDB，取四残基天然片段做 K-centers 聚类（**最大簇距 0.63 Å**）；螺旋帽库同法 | β转角定义：残基 i 的羰基与 i+3 的氨基之间有主链-主链氢键；只保留满足氢键要求的簇 | **180 个 β转角 motif 簇**（螺旋帽簇数原文未给） |
| S3 单条长环构建 | S1 骨架 + S2 motif | 螺旋帽(4 残基)+β转角(4 残基)+KIC 残基(5–10 残基)随机拼接，非枢纽残基按 Ramachandran 采 Φ/Ψ、ω 固定 180°，GeneralizedKIC 闭环接到下一螺旋 N 端 | 无骨架立体冲突；每个重复单元内**至少 2 条环内主链-主链氢键**；DSSP 判定连续螺旋残基 **>5** 者删（防塌成螺旋）；环长取 **9–14 残基**（<9 构象多样性不足，>14 难以整体扶住） | 候选长环构象集（**原文未给数**） |
| S4 传播 + 挑选 | S3 环构象 | RepeatPropagationMover 把同一构象装进每个重复单元；算三项指标：interloop 主链-主链氢键数、loop motif score（匹配 V/L/I/M/F 天然接触对，取和）、direction score = arccos(a·b/｜a｜｜b｜) | **至少 1 条相邻环之间的主链-主链氢键**；motif 总分须为**负**；direction score 接受区间 **45°–135°**；**至少 5 个残基位于距最近螺旋残基 8 Å 内** | 通过者呈片层状排布的长环骨架，供侧链扶壁安装 |
| S5 双齿氢键预装 | S4 中第 2 个重复单元的环 | 逐残基一步 PackRotamersMover，字母表只给 **Asn/Asp/Gln/His**；排除 Arg/Lys | 装箱残基必须与相邻重复单元主链形成**侧链-主链双齿氢键**，否则退回默认 Ala；一步失败走三级兜底：伪氢键（供体-受体距离 **<3 Å**、氢键角 **>120°**）→ 加谐振约束（目标距离 **2 Å**、标准差 **0.5 Å**）对称最小化 → Rosetta 复核 | 带「已确认扶壁相互作用」的残基类型约束（**原文未给通过数**） |
| S6 全序列设计 | S5 骨架 + 约束 | LayerSelector 分 core/boundary/surface 并指定各层允许氨基酸；FastDesign 在重复对称约束下跑 **4 轮**；随后 **1 轮**只允许 Glu/Gln/Lys/Arg 去掉末端重复单元暴露的疏水残基；fa_rep 缓升；环区轻微 Pro 倾向 | 保持 S5 固定的双齿氢键残基身份不变（残基类型约束） | 设计结构集（**原文未给数**），笛卡尔空间最小化精修 |
| S7 Rosetta 五项过滤 | S6 结构 | 逐条打分过滤 | **埋藏未满足重原子 ≤3**；**空洞分数（按核心残基数归一）≤−0.015**；**总能量/残基 <−2**；**packstat ≥0.5**；**每个环残基氢键能 ≤−1** | 取评分**前 10%** 进入 in silico 验证 |
| S8 in silico 验证（三选一） | S7 的 Top 10% | MD：GROMACS 2018.4 + Amber99SB-ILDN + TIP3P、PME、短程静电与范德华截断 **10 Å**、最陡下降能量最小化、位置约束下 **1 ns** NPT 平衡、Parrinello–Rahman 1 atm、速度重标 **310 K**、每个模型 **3 条 20 ns** 生产轨迹；或 AlphaFold；或 RoseTTAFold | **MD：对设计模型 Cα RMSD < 3 Å**；**AF/RF：pLDDT > 80 且 Cα RMSD < 3 Å**；结构相似度另用 TM-align 与天然 ankyrin 环比较 | **102 条**设计进入表达（即 RBL 全集；中间各级通过数**原文未给**） |
| S9 湿实验表征 | 102 条设计（pET-29b, Lemo21(DE3)，自诱导 37 °C 24 h；Ni-NTA IMAC + FPLC SEC） | 可溶 → SEC-MALS（单分散/单体）→ 变温 CD（25 °C / 95 °C / 回落 25 °C）→ SAXS 对照理论曲线 → 取 2 条结晶 | 成功口径（本文按「性质合格」逐级报，未设单一阈值） | **102 表达 → 77 可溶 → 52 单分散 → 46 单体（SEC-MALS）→ 44 CD 合格且 95 °C 仍部分折叠、回冷信号几乎全回收 → 14 条 SAXS 与模型一致 → 2 条晶体结构**（RBL4 **1.8 Å**；RBL7_C2_3 **3 Å**）；典型单分散热稳定 RBL 产量 **1–6 g l⁻¹** |
| S10 结构验证细节 | RBL4 / RBL7_C2_3 晶体 | 分子置换 + AutoBuild + Coot/Phenix/BUSTER 逐轮精修；复合 omit map（每次省略 **5%** 模型、自 5,000 K 模拟退火） | RBL4 拉氏图 **99.5%** 在 favored 区无离群；RBL7_C2_3 **98.22%** 无离群 | 整体 Cα RMSD **1.7 Å**（RBL4）、二聚体 **2.9 Å**/单体 **1.6 Å**（RBL7_C2_3）；单元内 RMSD **0.48–0.61 Å** |

### 功能分支（把 RBL 变成肽结合体）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| F1 | 已验证 RBL 的延伸沟 | 把 (XYZ) 三肽以聚脯氨酸 II 螺旋构象对接进沟（几何参照 PDB 里天然 ankyrin–肽复合物），刚体扰动多样化姿态 | 目标序列模式：X 为极性残基（与β转角顶相互作用）、Y/Z 为疏水残基（与螺旋及螺旋-环关节作用）；肽为 6 联重复 | 对接姿态集（未给数） |
| F2 | F1 姿态 | Rosetta 同时设计 RBL 与肽的序列以优化结合；对称序列设计沿用 S6 | 沿用 S7 的 Rosetta 物理过滤口径 | 设计候选池 |
| F3 | 设计候选 | 复合物层面 in silico 复测后下单合成、E. coli 表达纯化 | **AlphaFold PAE_interaction ≤ 15** | **34 条**针对 (DLP)₆/(KLP)₆/(DLS)₆ 的结合体设计 |
| F4 | 34 条表达产物 | split-luciferase（小 BiT 融到结合体、大 BiT 融到肽），在 96 孔板里梯度滴定加 Nano-Glo 底物测发光 | 「有清晰结合信号」为阳性（**原文未给信号阈值**） | **7 条**初筛阳性（分母＝34） |
| F5 | 每个肽靶的最强结合体 | 荧光偏倚：N 端四甲基罗丹明标记肽固定 **0.3 nM**，结合体 **4 μM–0.47 pM** 两倍系列稀释，25 °C 孵育 **3 h**，530/590 nm | 结合曲线拟合 Kd；并做交叉结合检验正交性 | **3 个 Kd**：(DLP)₆ 结合体 **1.2 nM**、(KLP)₆ 结合体 **<0.3 nM**、(DLS)₆ 结合体 **2.9 nM** |
| F6 | (DLS)₆ 不被前两条结合体识别 | 在β转角顶端安装 **Gln 介导的双齿氢键**重设计 | 新设计对 (DLS)₆ 的 Kd | 1 条设计达到 **2.9 nM**，但**仍保留对 (DLP)₆ 的亲和力**（正交性未完全达成） |

**这条流程最值得记的骨架**：它把「环能不能折成设计构象」这件事拆成了**几何可行性（S1/S4）→ 氢键存在性（S2/S3/S4/S5）→ 能量学合格性（S6/S7）→ 柔性/自洽性（S8）**四层，且越靠后越贵；功能化只在结构分支过关之后才开始，且功能分支用的是**另一套分母（34）与另一套判据（PAE_interaction ≤ 15）**。

## 4. 关键数字台账（数值 · 含义 · 出处；全部可在 §9 声明的本地全文里搜到）

| 数值 | 含义 | 出处（正文位置/原句片段） |
|---|---|---|
| 9–14 残基 | 可设计结构化长环的长度窗口 | 摘要 "structured loops (9-14 residues) buttressed by extensive hydrogen bonding interactions"；Methods "We chose these lengths because we found limited structural diversity for loops with lengths less than nine amino acids"；"When the loop length exceeded 14 amino acids, it became significantly more difficult to design buttressing interactions to stabilize the entire loop" |
| 12–28 残基 | 参数化骨架里两根理想螺旋的采样长度范围 | Results "systematically sampling the lengths of the helices (from 12 to 28 residues)" |
| 3–6 残基 | 连接序列相邻螺旋的天然 loop 查询长度 | Methods "then connected pairs of sequence-adjacent helices with loops of three to six residues using ConnectChainMover" |
| 6 + 6 | 分别采样的刚体自由度数（螺旋间、重复单元间） | Results "the six rigid-body degrees of freedom between the two helices"；"We next sampled the six rigid-body degrees of freedom between repeat units" |
| 18 Å | 待接螺旋末端最大允许距离（骨架硬阈值） | Methods "we required a maximum distance of 18 Å between the termini"（Results 同义句已在 §2.2 引出） |
| 28% | 埋藏核心残基比例下限 | Results "eliminated poorly packed models with fewer than 28% of the residues in a buried core" |
| 90% / 1.6 Å | motif 库构建时 PDB 的 PISCES 序列同一性与分辨率截止 | Methods "based on 90% maximum sequence identity and a 1.6 Å resolution cutoff from PISCES" |
| 0.63 Å / 180 | K-centers 聚类最大簇距 / 得到的 β转角 motif 簇数 | Methods "maximum cluster distance of 0.63 Å, resulting in 180 motif clusters" |
| 4 残基 / 4 残基 / 5–10 残基 | 拼接片段长度：螺旋帽 motif / β转角 motif / KIC 残基 | Methods "helical capping motifs (four amino acids)"（β转角 motif 同为四残基）；"and KIC residues (five to ten amino acids)" |
| ≥2 / ≥1 | 环内主链-主链氢键下限（单元内）/ 环间主链-主链氢键下限（相邻单元之间） | Results："at least two intraloop backbone-to-backbone hydrogen bonds within each repeat unit"；同句后半 "at least one interloop backbone-to-backbone hydrogen bond" |
| 8 Å / ≥5 残基 | 环与最近螺旋残基的接触要求 | Results "we further filtered the models by requiring at least five residues within 8 Å of the closest helical residues" |
| 45°–135° | direction score 接受角度区间 | Methods "The accepted angles ranged from 45° to 135°" |
| >5 连续螺旋残基 | 用 DSSP 剔除塌成螺旋的环 | Methods "we removed the models predicted to have more than five consecutive helical residues by DSSP" |
| <3 Å / >120° | 伪氢键判据（供体-受体距离 / 氢键角） | Methods "a pseudo hydrogen bond has a donor-acceptor distance <3 Å and a hydrogen bond angle >120°" |
| 2 Å, s.d. 0.5 Å | 最小化阶段对供-受原子加的谐振距离约束 | Methods "we imposed a harmonic distance constraint between each donor and acceptor atoms with a target distance of 2 Å and a s.d. of 0.5 Å" |
| Asn/Asp/Gln/His（排除 Arg/Lys） | 双齿氢键预装可用的氨基酸字母表 | Methods "compatible with forming sidechain-to-backbone bidentate hydrogen bonds—Asn, Asp, Gln or His"；"We excluded amino acids with longer side chains (Arg and Lys), as their high entropic cost might diminish the free energy contribution of buttressing" |
| ≤3 / ≤−0.015 / <−2 / ≥0.5 / ≤−1 | Rosetta 五项设计过滤阈值（埋藏未满足重原子、归一空洞分数、归一总能量、packstat、每个环残基氢键能） | Results "buried unsatisfied heavy atoms (≤3), core residue hole score (≤−0.015), total score per residue (≤−2), packstat (≥0.5) and average hydrogen bond energy per residue (≤−1)" |
| 4 轮 + 1 轮 | FastDesign 对称序列设计轮数 + 末端表面极性化轮数 | Methods "we performed four rounds of sequence design using the FastDesign mover"；"we subsequently performed one round of FastDesign to remove the solvent-exposed hydrophobic residues" |
| Top 10% | Rosetta 过滤后进入 in silico 验证的比例 | Methods "Top 10% scoring structures were further tested" |
| Cα RMSD < 3 Å；pLDDT > 80 | MD 与 AF/RF 的验证阈值（三者为可替换手段，原文三处之间夹参考文献编号，故拆两条引） | Methods "molecular dynamics simulations (Cα RMSD < 3 Å)"；"(PLDDT > 80, Cα RMSD < 3 Å) or RoseTTAFold" |
| 3×20 ns；1 ns 平衡；310 K；1 atm；10 Å 截断 | MD 生产规模与力场设置 | Methods "we launched three 20-ns trajectories under the NPT ensemble for each design model"；"A 1-ns equilibration under the NPT ensemble was subsequently performed with position restraints on the heavy atoms" |
| 102 → 77 → 52 → 46 → 44 → 14 → 2 | 结构分支逐级分母：表达→可溶→单分散→单体→CD 合格→SAXS 验证→晶体结构 | Results："We expressed 102 selected designs"；"In total, 77 of the purified proteins were soluble"；"52 were monodisperse and 46 were monomeric"；"Forty-four of these proteins showed the expected α-helical circular dichroism (CD) spectrum at 25 °C"；"Fourteen designs were further validated by small-angle X-ray scattering (SAXS"；晶体只有 RBL4 与 RBL7_C2_3 两条 |
| ~43% | 102 条里同时满足「正确α螺旋 CD + 95 °C 仍部分折叠 + 回冷几乎全回收」的比例（44/102） | 由上面 Forty-four 那一行算得（**本卡计算，非原文表述**） |
| 1.7 Å / 0.48–0.61 Å | RBL4 晶体对设计模型的整体 Cα RMSD / 各重复单元内 RMSD | Results "the design model is in good agreement with the crystal structure with a Cα root-mean-square deviation (RMSD) of 1.7 Å"；"with repeat unit Cα RMSDs for different repeat units ranging from 0.48 to 0.61 Å" |
| 4.2 Å → 3 Å | RBL7 原始晶体最高分辨率（衍射差）→ 二聚化改造后 RBL7_C2_3 解出分辨率 | Results "We obtained crystals that diffracted poorly with the highest resolution at 4.2 Å"；"we were able to solve the crystal structure at 3 Å resolution" |
| 2.9 Å / 1.6 Å | RBL7_C2_3 对设计模型的 Cα RMSD（跨二聚体 / 跨单体） | Results "with a Cα RMSD over the dimer of 2.9 Å"；"and over the monomer of 1.6 Å" |
| 99.5% / 98.22% | 两个最终模型的拉氏图 favored 区占比（均无离群） | Methods（晶体学段）"The final model included 99.5% of residues in the favored region of the Ramachandran plot with no outliers"；"The final model had 98.22% of residues in the favored regions of the Ramachandran plot with no outliers" |
| 150 mg ml⁻¹ / 119 mg ml⁻¹ | RBL4 / RBL7_C2_3 结晶前浓缩浓度 | Methods "RBL4 was concentrated to 150 mg ml"；"RBL7_C2_3 was concentrated to 119 mg ml"（原文单位为上标形式 mg ml⁻¹） |
| 1–6 g l⁻¹ | 典型单分散热稳定 RBL 的蛋白产量 | Methods "The typical yield of a monodisperse and thermally stable designed RBL is"（其后紧跟原文数值 1-6 g l⁻¹） |
| 34 → 7 → 3 | 功能分支分母：设计的肽结合体数 → split-luciferase 阳性数 → 报出 Kd 的结合体数 | Results "We designed 34 proteins to bind six-repeat peptides"；"seven designs showed clear binding signals"；Fig. 4c,f,i 三条曲线 |
| PAE_interaction ≤ 15 | 肽结合体下单前的复合物 AlphaFold 阈值 | Methods "All the designed complexes were computationally tested by AlphaFold with a cutoff of PAE_interaction ≤15" |
| 1.2 nM / <0.3 nM / 2.9 nM | (DLP)₆ / (KLP)₆ / (DLS)₆ 结合体的 Kd | Results "K d = 1.2 nM and <0.3 nM, respectively"；"The resulting design bound (DLS) 6 with high affinity ( K d = 2.9 nM)" |
| 0.3 nM / 4 μM–0.47 pM / 3 h | 荧光偏倚中肽浓度、结合体浓度跨度、孵育时间 | Methods "The protein concentrations ranged from 4 μM to 0.47 pM"；"the concentration of N-terminal tetramethylrhodamine-labeled peptide was kept at 0.3 nM"；"The samples were incubated for 3 h before measurement" |
| 8FRE / 8FRF | RBL4 与 RBL7_C2_3 的 PDB 登录号 | Data availability "Crystal structures and reflection data have been deposited in the RCSB Protein Data Bank with accession IDs 8FRE (RBL4) and 8FRF (RBL7_C2_3)" |
| 未记录 | 参数化骨架、环构象、S5、S6、S7 各级的绝对条数（正文只给 Top 10% 这个比例） | 正文/Methods 未给出；应位于 Supplementary Table 1，本地未取 |

## 5. 结论——作者说了什么

1. 「设计多条听话的长环」这件事被攻下来了，证据是结构而不是功能：原文把它说成一次阶段性突破——"the crystal structures presented here show that computational protein design has advanced to the point that proteins with multiple ordered long loops can now be designed"。
2. 成功的**关键被明确归到氢键/非极性相互作用网络**："Key to this success was the design of dense networks of hydrogen bonding and nonpolar interactions within and between the loops and between the loops and the underlying secondary structural elements."
3. 设计质量主张：可溶、单分散、折叠、热稳定，且环按设计被扶住——"Crystal structures are in close agreement with the design models, with the loops structured and buttressed as designed."；所有设计出来的环间氢键（β转角处）都在晶体里复现（"All of the designed interloop hydrogen bonds at the β turns of long loops were recapitulated in the crystal structure"）。
4. 比天然 ankyrin 的发夹环更多样、氢键更多："These designed buttressed loops have significantly more diverse structures than the long, hairpin loops in the native ankyrins"（对照见 Extended Data Fig. 1/2，本卡未取到图内数字）。
5. 功能可行性演示：不需要大规模库筛选也能得到 nM 级结合体——"This could enable the design of DARPin-like binders for a wide range of targets without the need for large-scale library selection methods."；肽结合位点每条环贡献一侧，结合模式与序列特异性由设计规定。
6. 展望有两条路（作者自己列的）："There are two primary routes forward for engineering new functions using our designed RBLs"——一是 RBL 走随机库 + 酵母展示筛选（类比 DARPin），二是继续用计算设计扩展到更多靶形；并推测可用于酶设计，把多条环从设计的 TIM barrel 上伸出来彼此支撑以建成催化位点（"multiple loops emanating from designed TIM barrels"）。
7. 作者对当下深度学习方法的边界说得很直白：那些方法"which do not directly address the challenge of designing structured long loops"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的命中率之所以好看，是因为分母被前移到了计算侧，而且前移的量没有登记**。102 是「过了 in silico 验证之后」的数，S1–S8 各级淘汰量只在 Supplementary Table 1（本地未取）。→ 我们看任何一篇 Baker 论文的「43% 折叠合格」时都要问：这是漏斗末端还是中段；本文这一数**不能**当作「设计成功率」引用。
2. **真正的贡献不是某个新打分，而是「换一个能让约束被复制 n 次的骨架架构」**。扶壁的强度来自重复对称：同一条环构象被传播到每个单元，一次几何成功等于 n 次几何成功。→ 对我们：把难满足的判据设计成「天然在多个位点上重复出现」的结构需求，比把它调得更松更有效。
3. **判据是「相互作用存在性」而不是「能量低」**：环内 ≥2 / 环间 ≥1 条主链氢键、必须有双齿氢键、必须有疏水接触、方向角 45°–135°——全是**几何存在性计数**，最后才用 Rosetta 能量项与 MD 兜底。这与 B09 那套「预测自洽性打分」是互补的两类筛子：本管「按要求搭起来」，自洽性管「序列自己会不会折成那样」。
4. **曲率失控是这篇最被低估的坑**。单元内 0.48–0.61 Å、整体 1.7 Å 很好看，但单元**之间**的变换错到「设计微弯 vs 实测近平」。凡功能依赖宏观沟形（本文的结合沟正是宏观形状），这个误差就直接进入结合设计环节，而本文没有为它提供任何判据。
5. **功能分支与结构分支的判据体系不同，且功能侧明显更弱**：结构侧有 5 项物理阈值 + MD/AF/RF，功能侧只有 PAE_interaction ≤ 15 一条，而它的命中率是 34 里 7（初筛阳性，非确证）。→ 一个「设计功能」的漏斗，末端证据其实很薄（三条 Kd）。
6. **MD 在这里是「可选的柔性检查」，不是闸口**，且没有报告它单独淘汰了多少。所以本文**不能**被引用为「MD 能提高设计命中率」的证据——它只能被引用为「MD 可以用来验刚性并与其他两法互换」。

## 7. 局限（作者承认的 + 我们读出的）

**作者自己写出来的**：

- 环长窗口是硬边界：<9 残基构象多样性不足，>14 残基难以整体扶住；也就是说本文没有解决「真正的长环」。
- 深度学习设计方法（RFdiffusion 那一类）不解决结构化长环问题——作者明确把这件事留作本方法的独立价值。
- 结构层面的两处偏差被如实报告：RBL4 的偏差在重复单元间变换（曲率），RBL7_C2_3 的偏差在末端螺旋。
- 环残基的 B 因子确实高于螺旋残基（"B-factors for the loop residues are elevated compared to the helix residues"），作者用电子密度拟合良好来回应，但没有量化「环到底有多刚性」。
- 挽救 (DLS)₆ 的设计同时保留对 (DLP)₆ 的亲和力——正交性没有做干净（Fig. 4i）。
- 结合体全部基于 RBL4 骨架（"were based on RBL4 with the peptides in nearly identical binding modes"），也就是说功能演示没有体现「多种骨架形状」这一本文主打卖点。
- 酶设计（TIM barrel + 环建成催化位点）只写在 Discussion 里作为展望，本文没有任何催化证据。

**我们读出的（推断）**：

- 计算漏斗的中间规模不可审计（正文只给 Top 10% 比例，无绝对数），因此这篇的「结构命中率」在数学上是**末端条件概率**，与 B09 那种「百万分之一」的量级不可直接比较。
- 102 条送测是**人工挑选**（"We expressed 102 selected designs"），挑选规则未在正文声明 → 77/52/46/44 存在选择偏差风险，无法判定判据的真实 ROC。
- 两条结晶结构 = 2/102 的直接构象确证；其余 12 条依赖 SAXS（低分辨率整体形状），其余全部只有 CD/SEC-MALS 这类「折叠且均一」的间接证据。「环按设计折好」这一核心主张的直接证据只有 2 个样本。
- 阈值全部是**经验值**（18 Å、28%、45°–135°、8 Å、0.63 Å、Cα RMSD < 3 Å、PAE_interaction ≤ 15），原文没有给出任何一条的敏感性分析或跨靶稳健性检验。
- 无 QM、无结合自由能计算、无竞争/副反应评估；对「环形成的沟为什么结合这条肽」只有静态结构解释。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **「存在性计数」型判据可以直接搬进我们的漏斗**。我们目前用的都是连续打分（pLDDT、RMSD、xTB 能量），而这篇的主力筛子是「几条氢键、几个接触、角度落在哪个区间」这类**离散计数 + 区间**判据。→ 具体用法：把 UAA 催化位点的要求写成计数式约束（例如 催化残基到拟底物原子的距离约束个数、氧负洞配位数、第三步环化所需残基的可达性），每条都能判真伪、不依赖打分标定；本轮已在 S0/S1/S2 事件判据里采用同型写法。
2. **把「难以同时满足的多个约束」放进一个对称/可复制的结构语境**：一次几何达标在 n 个重复单元上重复达标。→ 对我们：对四聚体/多重复体系（或同一位点在多个构象副本中）用对称设计，可把「一次通过」变成「多次通过」，比放宽阈值更省预算。
3. **贵判据只给前 10%**：便宜的物理计数先削量，MD/结构预测类柔性检验只对末端小集合跑。→ 与我们本轮的 10.6 GPU·h/体系、153.3 s/评价的单价结合：先排单价，再决定谁进 MD。
4. **功能与结构分两套分母、两套判据，各自单独报**（本文 102 与 34 从不合并）。→ 我们的交付也必须把「折得对/可表达」与「催化得对」分母分开写，绝不合并成一个「成功率」。
5. **失败归因写进 Methods 的诚实样本**：一步装箱装不出双齿氢键时的三级兜底、以及明确排除 Arg/Lys 的理由（熵代价）——这种「我们把哪些自由度主动关掉、为什么」的写法应当照搬进我们的 run.md。

**不可迁移（为什么不能照搬）**

1. **PAE_interaction ≤ 15（以及 B09 的 <10）是「会不会按设计结合」的判据，不是「会不会催化 UAA 合成反应」的判据**。本卡绝不把这两个数值写进 UAA 漏斗阈值；DP2R 标准 §2 禁止把 binder 的 pAE/ipTM 阈值当酶活闸口。
2. **102→77→52→46→44 是骨架可表达/可折叠率，与催化能力无关**，更**不能**当作 UAA 设计成功概率的任何一档校准值；我们能引用的只有「方法结构」，不是这些数字。
3. **本文不含 QM、不含自由能、不含竞争副产物评估**，所以它无法为「用 MD/QM 判催化」提供命中率证据；这篇里 MD 只是柔性检验，且没有淘汰率数据。
4. **它的设计对象是可重复、无配体、无化学步骤的纯蛋白骨架**；UAA 合成酶要求三步化学事件（含 S0 游离 UTP 起始、S1 pppUA、S2 第二枚 ATP 与环化竞争）在正确时空发生，这套「几何自洽 = 成功」的等价关系在本族问题上根本不成立。
5. **它一次下单 102 条 + 34 条**的通量前提（合成基因便宜、E. coli 表达 + SEC/CD 便宜）在我们这边不存在——我们的末端是 LC-MS/MS 产物身份，单条成本与信息量结构完全不同，不能按「扩大样本数」的思路照搬其漏斗末端设计。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/buttressedloops2024.txt

- **实际照着写的那一份**：`data/interim/baker_lit/ft/buttressedloops2024.txt`（68,754 B，PMC11288887 正式版全文抽取，已剥标签、HTML 实体解码、破折号/引号归一；本卡全部英文引句逐字复制自该文件）。同一篇另有预印本（bioRxiv/PMC10473674），本卡**未**使用其文本，措辞与数字若有出入以本底稿为准。
- 对照底稿：`sources/baker.md:443–460`（本行原卡，阈值与命中率数字）、`sources/baker.md:5`（MD 唯一进入入选判据的总判断）、`sources/baker.md:644,659`（MD 与 AF/RF 三选一、可替换性的定位）。
- 身份复核：文件头部含 Nat Chem Biol 20:974–980、DOI 10.1038/s41589-024-01632-2、PMID 38816644、PMCID PMC11288887，与 CSV 行 B34 标题一致（按全局规则，取回全文必须复核头部身份，本卡已复核）。
- 未取到的部分：Supplementary Table 1（预计含各级过滤的绝对条数）、Extended Data Fig. 1–4 图内数字、Reporting Summary。凡涉及这些处本卡写「原文未给」或「本卡未取到」。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`；第 5/7 节 ↔ `Kd或活性最好值`。
- 本卡自检命令：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B34 --no-report` → **PASS B34 quotes=94/94，退出码 0**（94 条英文引句全部在第 9 行声明的那一份底稿里逐字命中）。
- 过程中的两次红：① 初稿把 §7 一条引句写成跨句省略号拼接（All the selected binders … were based on RBL4）→ 门禁判未命中，改成原文连续片段 "were based on RBL4 with the peptides in nearly identical binding modes" 后转绿；② §4 台账原以不带引号的 `原句 … 原句` 形式写出处，虽不被门禁核验，但属「跨句拼接」风险，已逐行改为逐字引句（MD/AF/RF 阈值那行因原文三处之间夹参考文献编号 12, 13 / 34，按规定拆成两条）。
- **反向自测**（只在内存里改，不写盘）：把一处真引句里的二聚体 RMSD 从 2.9 Å 篡改为 1.9 Å，核验器立即报出该条未命中（93 条里 1 条 miss）——即「引用造假会被机器抓到」是可执行的，不是声明。
- 本卡**没有**做的事：没有取回任何新的网络内容；没有跑 `--sync-map`；没有改 CSV、`sources/*.md`、样板卡 B09、`scripts/` 下任何文件。§4 里唯一的非原文数字是 ~43%（44/102，本卡计算并已标注）。

<!--CSV回填
work_type=论文
target=带结构化长环（9–14 残基）的α螺旋重复蛋白 RBL；功能分支为六联重复肽 (DLP)₆、(KLP)₆、(DLS)₆ 的结合蛋白
backbone_generation=自建参数化重复蛋白生成器（MakeBundleHelix 建 12–28 残基理想螺旋 + 螺旋间与单元间各 6 个刚体自由度 + ConnectChainMover 3–6 残基天然 loop 连接）；RepeatPropagationMover 把同一环构象传播到每个重复单元；序列走 Rosetta FastDesign 重复对称 4 轮 + 1 轮表面极性化
computational_filters=环内/环间主链-主链氢键计数（≥2 / ≥1）、环-螺旋接触（≥5 残基在 8 Å 内）、direction score 区间 45°–135°、环-螺旋疏水 motif 总分须为负、侧链-主链双齿氢键存在性（字母表 Asn/Asp/Gln/His，排除 Arg/Lys）、Rosetta 五项（埋藏未满足重原子、归一空洞分数、归一总能量、packstat、环残基氢键能）；末端三选一柔性/自洽检验：MD Cα RMSD<3 Å 或 AlphaFold/RoseTTAFold pLDDT>80 且 Cα RMSD<3 Å；功能分支用 AlphaFold PAE_interaction≤15
thresholds=螺旋末端距离≤18 Å；埋藏核心残基≥28%；PISCES 90% 序列同一性 + 1.6 Å 分辨率；K-centers 最大簇距 0.63 Å（180 簇）；环长 9–14 残基；伪氢键 供-受<3 Å 且角>120°；谐振约束目标 2 Å±0.5 Å；Rosetta 过滤 ≤3 / ≤−0.015 / <−2 / ≥0.5 / ≤−1；取 Top 10% 进 in silico 验证；MD/AF/RF：Cα RMSD<3 Å、pLDDT>80；复合物 PAE_interaction≤15
md_used=是（入选流程内的刚性检验：GROMACS 2018.4 + Amber99SB-ILDN + TIP3P，PME、10 Å 截断、1 ns 约束平衡、NPT 310 K/1 atm、每模型 3×20 ns，判据为对设计模型 Cα RMSD<3 Å；与 AlphaFold/RoseTTAFold 三选一、非必过关口；未报 MD 单独淘汰数）
qm_used=否
experimental_methods=E. coli Lemo21(DE3) 自诱导表达 + pET-29b + His-IMAC + FPLC SEC；SEC-MALS 判单分散/单体；变温 CD（25/95/回落 25 °C）；SAXS（ALS SIBYLS 12.3.1）对照理论曲线；X 射线晶体学（RBL4 1.8 Å、RBL7_C2_3 3 Å，PDB 8FRE/8FRF）；split-luciferase 初筛；荧光偏倚测 Kd；TM-align 比环相似度
pipeline_counts=结构分支：参数化骨架与环构象各级绝对条数原文未给（正文仅给 Top 10% 比例）→ 102 条设计表达 → 77 可溶 → 52 单分散 → 46 单体 → 44 CD 合格且热稳定 → 14 SAXS 验证 → 2 晶体结构；功能分支：34 条肽结合体设计 → 7 条 split-luciferase 阳性 → 每靶最强者共 3 条给出 Kd → 1 条挽救设计
hit_rate=结构口径：44/102 ≈ 43% 同时满足正确 CD 谱 + 95 °C 部分折叠 + 回冷回收，77/102 ≈ 75% 可溶；直接构象确证仅 2 条（1.7 Å、单体 1.6 Å，单元内 0.48–0.61 Å）；功能口径：7/34 ≈ 21% 初筛阳性，确证 3 条；作者称设计比天然 ankyrin 环更多样、主链氢键更多（Extended Data 图内数字本卡未取）
best_metric=Kd 1.2 nM（(DLP)₆）、<0.3 nM（(KLP)₆）、2.9 nM（(DLS)₆，挽救设计但仍保留对 (DLP)₆ 的亲和力）；无催化/活性数据（酶设计仅在 Discussion 作展望）
cost_or_stat_note=典型单分散热稳定 RBL 产量 1–6 g l⁻¹；结晶浓缩 150/119 mg ml⁻¹；FP 肽固定 0.3 nM、蛋白 4 μM–0.47 pM 两倍稀释、孵育 3 h；MD 每模型 3×20 ns；拉氏图 favored 占比 99.5%（RBL4）/98.22%（RBL7_C2_3）；本文全部阈值为经验值，未做敏感性分析；漏斗中间规模不可审计（Supplementary Table 1 未取）
role_in_timeline=Baker 组文献里唯一一次把 MD 写进入选流程（作刚性检验、与 AlphaFold/RoseTTAFold 并列可替换）；也是把「结构化长环」重新变成可设计对象的一篇，路线与 2022–2023 主线的自洽性打分漏斗不同：用几何存在性计数（氢键数、接触数、角度区间）＋Rosetta 物理项做筛子，并把骨架换成可复制约束的参数化重复蛋白；其 PAE_interaction≤15 与同期 binder 论文的 pAE<10 属同一族结合判据、口径不同，不能互推也不适用于酶活
source_pointer=data/interim/baker_lit/ft/buttressedloops2024.txt（PMC11288887 正式版全文，68,754 B）；对照 sources/baker.md:443-460, 644, 659；PDB 8FRE/8FRF；代码 github.com/hanlunj/buttressed_loops
CSV回填-->
