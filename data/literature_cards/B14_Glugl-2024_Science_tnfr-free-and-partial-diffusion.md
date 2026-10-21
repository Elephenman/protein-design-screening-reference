# [B14] 用"自由扩散 + 部分扩散"打平表面靶——把亲和力成熟做成一次可重复的重采样

Glögl M, Krishnakumar A, Ragotte R J, Goreshnik I, Coventry B, Bera A K, … Baker D（华盛顿大学 IPD）
Science 2024, 386:1154-1161 · DOI 10.1126/science.adp1779 · PMID 39636970 · PMCID PMC12416549
开放获取（CC BY 4.0）· 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12416549/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B14**（组：Baker组; 通用方法学；标题 Target-conditioned diffusion generates potent TNFR superfamily antagonists and agonists） |
| 本文取回方式 | 2026-10-16 本地抓取（先行调研缓存通路） |
| 本地全文①（本次唯一登记全文） | `data/interim/baker_lit/ft/tnfr2024.txt`（40,111 B，Europe PMC 记录派生的去标签纯文本） |
| 登记底稿 | `sources/baker.md` 第 185–196 行（原卡；其引文写法与全文有一处差异：底稿写 `K_D`，全文实际写作 `K D`（上标 D 被剥离）） |
| 证据级别 | **全文级**（本卡所有英文引句均在该本地纯文本里逐字命中；见第 9 节门禁自检） |
| 未取到的部分 | 本文件只有正文与图注，**没有 Methods 章节**（正文只列 Supplement Table S1/S2/S4）；Fig 1–4 原图数值、SSM 深原始表、Table S4 的 24 个寡聚化结构域清单均未获。凡涉这些处本卡明写"正文/图注未给出" |
| 特别注意 | 抓取文本里 `&lt;`/`&gt;` 为未解码实体（门禁按归一化后的 `<`/`>` 比对）；本卡凡涉及阈值数字优先写成不带尖括号的原文表述 |

## 1. 这篇到底解决什么（大白话）

此前的 de novo 结合蛋白设计（[B03] hallucination、[B06] Rosetta 对接、[B09] 深度学习过滤、[B08] RFdiffusion）在**有凹槽、有疏水斑点的靶面**上好使，但对**平坦、极性、几乎没有疏水口袋**的靶面（TNFR1 是代表）反复失败；而 RFdiffusion 原作只用"65 残基理想螺旋"这类小脚手架引导扩散，不加引导时又只能长出三四个螺旋的简单束。这篇做三件事：① 不加脚手架、直接把上百个残基的高斯噪声云摆在天然配体界面上做**自由扩散**，让模型自己长出贴合平坦靶面的形状；② 用**部分扩散**（把已有结构只加噪 15–25 步再去噪）当成"局部优化器"，一举把亲和力从 nM 推到 <10 pM，并且把同一条设计**改靶**到 TNFR2 / OX40 / 4-1BB；③ 把拿到的单体结合体嫁接到环状寡聚体上，做出 4-1BB 与 OX40 的**超激动剂**，从而在同一批零件里同时交付拮抗剂与激动剂。它的关键工程含义是：**"生成 → 筛选 → 再生成"闭环可以完全在计算里做**，湿实验下单量被压到每靶几十个。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **前代方法在这个靶面上是"已知失败"的，而且失败被当作立项依据**。作者开篇就写 "**design efforts have failed for the tumor necrosis factor receptor 1 (TNFR1) and other protein targets with relatively flat and polar surfaces**"，并在结果第一段直说 "**multiple attempts to generate binders to TNFR and other family members using the approach of Cao et al."**；连"照 [B09]/[B08] 的做法"也不行——"**using guidance from 65 aa scaffold libraries or limited to chains less than 65 residues but also had little success**"。→ **他们做了什么**：不再调原协议的权重或阈值，而是**撤掉脚手架这一约束**（"without any guidance from pre-existing scaffolds"），并把生成端的自由度提到 120 个残基的高斯云。→ **代价**：牺牲了"短、规整、易折叠"这一先验，设计变长变不规整，必须回头用表达量来验证能不能生产。
2. **平坦靶的真正难点是疏水残太少且彼此太远**。原文量化了：**"On TNFR, the few surface hydrophobic residues are separated by distances of up to 28 Å"**，并判定 **"too small for 65 residue proteins to simultaneously engage"**（同一句里 65 残基这条正是上一代的链长上限）。→ **他们做了什么**：把随机高斯残基云**摆在天然配体（TNF）界面上**，并让扩散**偏向与这些分散的疏水残基形成接触**（"RFdiffusion was biased to form contacts with these dispersed hydrophobic residues"）。→ **代价**：界面变大也意味着折叠风险变大，他们用 96 条设计的实测表达率来兜底：**"90 of 96 designs expressed well and were primarily monomeric"**。
3. **"界面太大、亲和力太低"这一物理天花板他们没打算靠运气解决，而是换了工具**。原文写得很直白：为了进一步压低亲和力，他们**放弃**了当时通行的做法——"**rather than combining beneficial substitutions from the SSM libraries, which requires considerable experimental screening**"——改用部分扩散，即对骨架"**noise is added (second panel), and then RFdiffusion is used to remove the noise, which results in a similar but better fitting model**"（图注原句，加了 15–25 步噪声、50 步即完全随机）。→ **他们做了什么**：把亲和力成熟变成**重采样**问题，每个起点跑 25,000 条轨迹，再用 AF2 置信度反选。→ **代价**：这条路的收益**不均匀**——TNFR1_mb2 提高三个数量级，但更规整的 TNFR1_mb1 **"Improvements were smaller for the more regular TNFR1_mb1 backbone; free diffusion sampling appears to have already found a close-to-ideal solution for this binding mode."**，也就是说"局部优化器"只对**尚未收敛到最优的起点**有效。
4. **改靶到亲缘关系更远的受体时，一轮部分扩散不够**。作者记录："**For the even less related 4-1BB, an additional round of partial diffusion was required to achieve a pae_interaction less than 7**"。→ **他们做了什么**：把部分扩散**当作可迭代的一级操作**（而不是"一次算完"），并改用逐靶分开报成功率；TNFR2 那条路径甚至出现 **"a substantially higher success rate than achieved by free diffusion on TNFR1"**。→ **代价**：文中没有解释"什么时候该再加一轮"的判据，只给了结果；"额外一轮"是**事后**决定的，不是事前预测的。
5. **结构预测判据（AF2 pae_interaction）在他们自己手里也出现过方向性错误**：图注给出实测对照——两个 TNFR1 结合体的 AF2/RF2 复合物预测与设计结构一致性很好（**"pAE interface of 5.1 and 4.1, CA RMSD to design of 0.6 and 1.0 Å for designs TNFR1_mb1 and TNFR1_mb2 respectively, using AlphaFold2-multimer model 1"**），并用 SSM 指纹做**第二条独立证据**："**the close agreement of the site saturation mutagenesis (SSM) footprints with the design model interfaces**"，且 SSM 的熵分布应当"核心与界面低熵、远端高熵"（**"Positions that were strongly conserved (low entropy, blue) were in the core and at the binding interface"**）。→ **他们做了什么**：不靠单一预测分数下结论，而是**用全位置逐残基置换的实测指纹**去反证模型界面。→ **代价**：SSM 只覆盖"设计出来的结合体"这类命中，全文没写对失败候选做同等验证。
6. **拮抗剂与激动剂是同一批零件，但需要额外的生物学难题**：作者点明 TNFR1 通路长期只能打配体的原因——"antibodies targeting TNFR1"**"owing to their bivalency, can activate, rather than suppress"**（两句之间原文插了参考文献编号，本卡拆成两条引句）。→ **他们做了什么**：用**单价单体**做拮抗（"We investigated if our (monomeric) designs could inhibit TNF"），再用**把同一单体嫁接到环状寡聚体**去做激动，一次覆盖两个治疗方向；激动侧的实测规律是**"valency was the strongest determinant of signal strength, with no signal for C1-C3, a consistent but low signal for C4, and a higher signal for C5 and C6"**。→ **代价（作者自留）**：机制仍未闭合——"**it remains to be determined how bringing in just one more subunit (in the C4 case) leads to agonism**"。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **生成端**：RFdiffusion **自由扩散**（从高斯残基云开始，不加任何脚手架）；**部分扩散**（把已有骨架加噪 15–25 步后去噪，50 步即完全随机）——同一模型充当"生成器"与"局部优化器"两种角色。
- **序列端**：ProteinMPNN（对复合物设计，同时兼顾折叠与结合）。
- **评估端（计算闸口）**：AF2 复合物预测的**界面 pAE（pae_interaction）** + **pLDDT** + 复合物 Cα RMSD 到设计模型；TNFR1 主实验闸口写作 interface pae < 7.5 与 pLDDT > 85（图内数值），后续池子按 pae_interaction < 5（选 32 条）与 < 7.5（TNFR2 计 1323 条）分层。
- **评估端（实验闸口）**：E. coli 表达 + SEC 单体判定 → **SPR** 定量 KD → **SSM**（全位置 ×20 氨基酸 + 深测序）做界面指纹 → X 射线晶体学确证 → HEK293 报告基因（AP-1/NF-κB/SEAP）测拮抗 IC50 → 与寡聚化结构域融合的荧光素酶报告测激动 EC50/Emax → 可开发性三件套（95 °C 热处理、鼠血清孵育、HIC、敲除细胞系 off-target）。
- **没有用的方法**：MD、QM、自由能微扰——全文不含这些；机理层面的解释靠晶体结构与 SSM 指纹，不靠模拟。

### A. 拮抗剂主线（TNFR1，Fig 1–2）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | TNFR1 结构（PDB 6KP8）+ 天然配体 TNF 界面 | 摆**高斯残基云**（至 120 残基）于 TNF 界面，跑 RFdiffusion 自由扩散，偏向与分散疏水残基形成接触 | 正文未给数值阈值 | 一批"**quite different from those in previous campaigns, but complementary in shape to TNFR1**"的骨架 |
| A2 | A1 骨架 | ProteinMPNN 复合物序列设计 → AF2 预测复合物 | **"a low predicted aligned error (pae) in the interface region"**（图注写 pae_interaction <20）用于继续采样 | 采样邻域 |
| A3 | AF2 判为有希望的复合物 | 从**同一条扩散轨迹的更早时间步**再抽骨架（图注：**"the predicted structure was already close to the final structure at around timestep 120 out of 200"**） | 无 | 扩样（正文未给条数） |
| A4 | A3 全集 | 选送测集合 | **interface pae < 7.5** 且 **pLDDT > 85**（正文原句用实体编码尖括号） | **96 条**送测设计（合成基因） |
| A5 | 96 条 | E. coli 表达 + SEC | 表达良好且主要为单体 | **"90 of 96 designs expressed well and were primarily monomeric"** |
| A6 | 表达合格者 | SPR 测 TNFR1 结合 | 有 KD | **"Six of the designs bound to TNFR1 in surface plasmon resonance (SPR) experiments"**；TNFR1_mb1 29 nM、TNFR1_mb2 24.5 nM；"**Both designs were highly specific, with no detectable binding to TNFR2.**" |
| A7 | 命中设计 | 全位置饱和突变库 + 深测序（SSM） | 界面/核心应低熵，远端高熵 | **"4047 substitutions in total"** |
| A8 | 命中设计 | 晶体学 + AF2/RF2 复合物预测回算 | 界面 pAE 与 Cα RMSD | **"pAE interface of 5.1 and 4.1, CA RMSD to design of 0.6 and 1.0 Å"**（用 AF2-multimer model 1） |
| A9 | TNFR1_mb1/2/3 三个起点 | **部分扩散**：加噪 15–25 步再去噪（50 步 = 完全随机） | **pae_interaction < 5**（图注：**"noise is added (second panel), and then RFdiffusion is used to remove the noise, which results in a similar but better fitting model"**） | **"We generated 25,000 partially diffused backbones around each starting structure"**，每起点取 AF2 最确信的 **32 条**送测；新骨架 RMSD 到母体 0.58–4.96 Å |
| A10 | A9 送测池 | 表达 + SPR | 表达率 / 结合率 | 96 条中 **94 条高表达**，**30%（28/94）结合 TNFR1** |
| A11 | 部分扩散产物 | 亲和力与机理归因 | KD 数量级 | TNFR1_mb2 → **<10 pM**（三数量级提升），归因于 **"an additional interface and an overall better fit to the binding cleft"**；mb1 提升小（"Improvements were smaller for the more regular TNFR1_mb1 backbone"）；mb3 从 µM 段 → 20 nM |
| A12 | 最优变体（TNFR1_mb2_pd1） | 功能与可开发性验证 | — | **IC50 = 106 pM**；95 °C/30 min 与鼠血清 2 h 后保留功能；HIC 相对阿达木/依那西普未见明显疏水；敲除细胞系 up to 100 nM 无脱靶 |

### B. 改靶与激动剂支线（Fig 3–4）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | TNFR1_mb1/2/3 三个结合体 | 把 TNFR2 / OX40 / 4-1BB **叠加到 TNFR1 位置**，各跑"加噪 → RFdiffusion 去噪 → ProteinMPNN" | **pae_interaction < 7.5**（4-1BB 需 **<7**，且"an additional round of partial diffusion was required"） | 每组合 **25,000** 条轨迹；TNFR2 有 **"1323 designs had AF2 complex predictions with pae_interaction <7.5"** |
| B2 | B1 的筛后池 | 每受体取设计做 E. coli 表达 + SPR | 结合 + 家族内特异性 | 每受体 **48 条**实测；TNFR2 结合率 **32%**、最优 **K D of 198 pM**（对家族其他成员无亲和力）；OX40 得 **K D of 30 nM**；4-1BB **"with 22 out of 48 tested designs binding specifically to their target, with the highest affinity of 44 nM"** |
| B3 | TNFR2 最优变体 TNFR2_mb1 | X 射线晶体学 | 与设计模型比较 | **"nearly identical over the designed binder (C-alpha RMSD 0.52Å"**（此句正文未加空格，本卡按原文照录）；PDB 9CU8 |
| B4 | 4-1BB_mb2 / OX40_mb1 | 融合到设计好的环状寡聚化结构域（N 端或 C 端，24 种结构域各一套），做化学计量与几何扫描 | 报告基因信号；以天然配体（OX40）或配体+抗体（4-1BB）为对照基线 | **44 个寡聚体**测信号；4-1BB：C1–C3 无信号、C4 低、**C5/C6 更高，最强为 C6**；OX40：单体/二体无信号，**三/四/五价有效**（"Monomeric and dimeric binder constructs did not signal, whereas oligomeric constructs with three, four, or five binding modules efficiently activated signaling"） |
| B5 | 44 组数据 | 归因 | 变量重要性 | **"valency was the strongest determinant of signal strength, with no signal for C1-C3, a consistent but low signal for C4, and a higher signal for C5 and C6"**；除价数外几何也起作用（距离过大或与受体碰撞/穿膜者低信号）；融合规模：**"Binders 4-1BB_mb2 and OX40_mb1 were fused N- or C-terminal to 24 oligomerization domains each"** |

**这套流程里最值得单独记住的一条**：**"no random or experimentally guided optimization was involved other than selecting the best of the 96 first round designs for partial diffusion"** ——他们把"亲和力成熟"这件事从湿实验搬进了计算，于是漏斗末端不再是"筛得更多"，而是"再生成得更准"。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 28 Å | TNFR 上少数疏水残基间的最大距离 | "the few surface hydrophobic residues are separated by distances of up to 28 Å" |
| 120 残基 | 高斯残基云的上限链长 | "random Gaussian residue clouds of up to 120 residues were placed at the native ligand (TNF) interface" |
| timestep 120 / 200 | 结构已接近终态的轨迹步（用于抽邻域骨架） | "close to the final structure at around timestep 120 out of 200" |
| 96 → 90 → 6 → 2 | 送测 → 良好表达且单体 → SPR 有结合 → 高亲和主力 | "90 of 96 designs expressed well and were primarily monomeric"；"Six of the designs bound to TNFR1 in surface plasmon resonance (SPR) experiments" |
| 29 nM / 24.5 nM | TNFR1_mb1 / mb2 的 KD | "with designs TNFR1_mb1 and TNFR1_mb2 having K D s of 29 nM and 24.5 nM respectively" |
| 795 Å 2 / 490 Å 2 | mb2 的接触分子表面 vs 以往扩散设计平均 | "a very high contact molecular surface (CMS) for TNFR of 795 Å 2" |
| 897 Å 2 | mb1 的接触分子表面 | "a similarly high CMS of 897 Å 2" |
| 4047 | SSM 单点置换总数 | "every amino acid substitution at every position one at a time (4047 substitutions in total)" |
| 5.1 / 4.1；0.6 / 1.0 Å | 两设计的界面 pAE 与到设计模型 Cα RMSD | "pAE interface of 5.1 and 4.1, CA RMSD to design of 0.6 and 1.0 Å" |
| 15–25 步 / 50 步 | 部分扩散的加噪幅度（50 步 = 完全随机） | "backbones were partially noised (over 15 – 25 steps; 50 steps yield a completely random distribution)" |
| 0.58–4.96 Å | 部分扩散新骨架与母体相似但不同 | "yielded new backbones resembling but distinct from the original designs" |
| 25,000 / 起点；32 条 / 起点 | 部分扩散采样量与送测量 | "We generated 25,000 partially diffused backbones around each starting structure"；"the 32 designs for each starting structure" |
| 96 → 94 → 28（30%） | 部分扩散送测 → 高表达 → 结合 TNFR1 | "Most (94 out of 96) of the designs were expressed at high levels, and 30% (28 out of the 94 expressed designs) bound TNFR1" |
| 19 pM | 天然 TNF-α 三聚体结合 TNFR1 的亲和力（对标基准） | "binds TNFR1 with high (19 pM) affinity" |
| <10 pM / 20 nM | 部分扩散后 TNFR1_mb2（mb2_pd1）与 mb3 的 KD | "increased from weak binding in the uM range to 20 nM" |
| 106 pM | 最佳拮抗剂的细胞 IC50 | "with an IC50 for the best design at 106 pM" |
| 1323；48 / 靶；32%；198 pM；30 nM；22/48；44 nM | 改靶支线：计算通过量、送测量与实验命中 | "For TNFR2, 1323 designs had AF2 complex predictions with pae_interaction <7.5"；"For each of the receptors, 48 designs were experimentally characterized"；"the highest affinity design had a K D of 198 pM to TNFR2"；"yielded an OX40 binder with a K D of 30 nM"；"the highest affinity of 44 nM" |
| 0.52 Å | TNFR2_mb1–TNFR2 复合物结合体的 Cα RMSD | "nearly identical over the designed binder (C-alpha RMSD 0.52Å" |
| 44 个寡聚体；24 种结构域 | 激动剂几何/价数扫描规模 | "Over a set of 44 oligomers"；"Binders 4-1BB_mb2 and OX40_mb1 were fused N- or C-terminal to 24 oligomerization domains each" |
| 107 残基 | 拮抗剂尺寸（界面却大于天然界面） | "even larger than the native interface despite being only 107 amino acids" |
| 96 + 96 + 48 | 全流程实测序列总数口径 | "The number of sequences tested (96 free diffusion and 96 partial diffusion designs for TNFR1, and 48 partial diffusion designs for TNFR2, OX40, and 4-1BB)" |
| 680 pM / 10–100 nM | 抗体的对照亲和力区间（二价 vs 单体形式） | "have affinities of up to 680 pM"；"whereas monomeric Fabs, scFvs, and nanobodies are in the range of 10-100 nM" |
| 10,000 倍 | off-target 试验浓度相对 KD 的倍数 | "up to 100 nM, 10,000 fold higher than the K D" |

## 5. 结论——作者说了什么

1. 对**平坦极性表面**这类"前代失败靶"，不加脚手架的自由扩散能生成**形状匹配、界面巨大**的结合体（TNFR1 两条，nM 级，家族内特异）。
2. **部分扩散**同时干了两件事：把亲和力推到 **<10 pM**（约三个数量级），以及**把结合体改靶到同家族其他成员**（TNFR2 198 pM、OX40 30 nM、4-1BB 44 nM）。
3. 单价、高特异、超稳定的单体结合体可直接做**拮抗剂**（IC50 106 pM），嫁接到环状寡聚体后同一零件变**超激动剂**；**"the substantially higher Emax of the best OX40 and 4-1BB synthetic agonists compared to the native ligand in the OX40 case and antibody-ligand assemblies in the 4-1BB case"**（两句之间原文插了参考文献编号，本卡拆条）。
4. 全流程只测 **96 + 96 + 48 条**序列，作者自己据此主张通量范式变化：**"The ability to design high-affinity and specificity antagonists and agonists for pharmacologically important targets in silico presages a coming era in protein design in which binders are made by computation rather than immunization or random screening approaches."**
5. 作者也承认遗留问题：4-1BB 的 C4 单亚基增益机制未定（见第 2.6 条）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **"局部优化器"的收益取决于起点离最优有多远**（第 2.3 条：mb1 提升小、mb2 提升三个数量级）。→ 对我们：判断"再跑一轮重采样值不值"，不能看它平均能提多少，而要看**当前候选离其约束最优还有多远**——我们手上最接近"能折叠但催化几何不对"的候选，才配得上一轮重采样。
2. **他们把"改靶"当成重采样的副产品，而不是新漏斗**。家族内改靶之所以便宜，是因为**折叠先验不用重学**（同一批骨架挪到新受体上加噪重采样即可），且作者给出反直觉观察：TNFR2 的通过数**比 TNFR1 的自由扩散更容易**（"a substantially higher success rate"）。→ 对我们：把同一条设计挪到不同 UAA/不同反应构型时，"改构型"的成本可能远低于"从零生成"，值得单列一类而不是并进主漏斗。
3. **第二条独立证据（SSM 全位置指纹）是他们敢只测几十条的底气**。全文没有 MD，验证靠"预测 + 逐残基实测指纹 + 晶体结构"三件事互相印证。→ 对我们：单浓度结合读数或单一预测分数都不构成证据；必须有一条**与预测不共线**的实测信息（本轮的等价物是 LC-MS/MS 产物身份，而不是活性高低）。
4. **"生成 → 筛选 → 再生成"闭环里，筛选器用的是 AF2 pae_interaction 的连续分层（<20 → <7.5 → <5 → <7）**，而不是一个物理常数。这些数字的真实作用是**"把池子削到可下单的量级"**（25,000 → 32）。→ 我们读：阈值应当报告为"削池工具"，不得当催化判据引用（DP2R 标准 §2 禁止把 binder 的 pAE/ipTM 阈值当酶活闸口）。
5. **他们的失败经验被写成了生物学结论**（C4 机制未明、mb1 已近最优）。全文对自己的"哪些靶能做成、为什么"没有给出可预测规则，作者自己把 C4 机理留白——**"it remains to be determined how bringing in just one more subunit (in the C4 case) leads to agonism"**；本文只补上了**工程**（重采样）与**读出**（寡聚几何）。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者自陈：① 更规整的 mb1 从部分扩散获益有限（起点已近最优）；② 4-1BB 需**额外一轮**才达 pae_interaction < 7，且 C4 只多一个亚基就产生激动的原因**未确定**；③ 激动侧只有报告基因读数，全文未给治疗端数据；④ 本文**无 Methods 章节可核对**（本地全文只有正文 + 图注，Table S4 与寡聚化域清单在补充材料里，本卡未获）。
- 我们读出：① 全文没有对**失败候选**做任何实验反证，SSM 只覆盖设计命中体，因此"界面确实如设计"是命中侧的选择结果；② 每靶 48 条、家族内改靶的"成功率"分母极小（22/48、32%），不该外推成"改靶通例的成功率"；③ 亲和力与功能的量级来自 SPR/报告基因单点或曲线拟合，**没有竞争结合的绝对化学计量**（部分扩散后界面变大，寡聚化后又是多价体系，单价 KD 与治疗读数不同层）；④ 判据是 pae_interaction/pLDDT 的**经验拐点**，全文未给 ROC 或阳性/阴性对照校准；⑤ 无 MD/QM，机理层的"形状互补更好"来自晶体结构与 SSM，而不是能量学。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"部分扩散 = 廉价局部优化器"这一组织方式**：对已有候选（如我们已锁定催化 Asn 但几何未调的变体）做"小步重采样 + 复测"，把它当作独立于主生成漏斗的一级操作；同时**沿用他们的报告口径**——同时报"提升幅度"与"起点离最优的距离"（mb1 几乎不涨）来解释为什么不同候选收益差三个数量级。
2. **"再加一轮"作为应对手段**：当一个构型/靶变体在现有轮次里达不到可下单池规模时，先加一轮局部优化再决定放弃；但要像他们一样**把加轮次的判据写出来**（本文没写清，我们应当补写，例如"第二轮仍无候选进入前 K 名即放弃该变体"）。
3. **第二条独立实测证据（SSM 式指纹）**：对我们就是"每个进入终池的候选，除活性/产物读数外，还要一条**与预测不共线**的位置级证据"（如定点失活突变 + 产物化学确证）。这一条比任何分数都更接近"能判定"。
4. **同一批零件交付拮抗/激动双向功能**：对应我们"同一批酶变体交付不同选择性读数（正向反应 vs 竞争副反应）"的设计——一次下单、两个方向的读出，比单方向多测几倍候选更省。
5. **可开发性三件套（热/血清/HIC/off-target）作为终池筛**：我们的等价物是"表达可溶 + 游离 UTP 不依赖 + 第二枚 ATP 竞争下的副产物谱"，都是"能不能被用"的判据，与"好不好"分开。

**不可迁移（为什么不能照搬）**

1. **pae_interaction < 7.5 / < 5、pLDDT > 85 判的是"会不会按设计结合"**，不涉及任何化学步骤。UAA 合成酶的成功要判 S0（游离 UTP 起始）/S1（pppUA）/S2（第二枚 ATP vs 环化竞争）三个化学事件与副产物，结构自洽**既不必要也不充分**；DP2R 标准 §2 明令禁止把 binder 的 pAE/ipTM 阈值当酶活闸口。
2. **"25,000 → 32 → 28/94 结合"这类比例不能转成我们的命中概率**。他们的标签是二值结合/不结合、分母是几十条、绝对 KD 在 pM–nM；我们的标签需要产物化学确证，至今**没有一条被产物化学确认的天然 UAA 合成酶**做分母。引用时只许引用**工作流结构**（生成→筛→再生成、双证据），不许引用**命中率数字**（30%、32%、46%）做校准。
3. **寡聚价数—信号强度规律不能搬到酶活**。他们的激动剂效应来自受体簇集（几何与化学计量问题）；UAA 酶活是位点内化学步骤，多价呈现不会改变催化势垒，反而可能引入相邻位点串扰。
4. **他们"完全不做 MD/QM"不能当作"不需要机理层证据"的依据**。本文的机理主张全部由晶体结构 + SSM 指纹支撑；我们若主张催化可行性，缺少等价的高分辨结构/产物化学证据时不能借它的"无模拟也成立"作挡箭牌。

## 9. 溯源与自检

- 唯一登记全文：`data/interim/baker_lit/ft/tnfr2024.txt`（40,111 B，去标签纯文本；`&lt;`/`&gt;` 实体未解码，门禁比对时按 `scripts/litcards_text.py` 的 `norm()` 归一化后再比）。
- 引句底稿: data/interim/baker_lit/ft/tnfr2024.txt
- 登记底稿：`sources/baker.md:185–196`（原卡；本卡在两处修正其写法：① 底稿把 KD 写作 `K_D`，全文实际为 `K D`；② 底稿把主闸口并写为 "interface pae < 7.5 且 pLDDT > 85"，全文原句用未解码实体 `&lt; 7.5` / `&gt;85`，本卡因此未把该句作为英文引句使用）。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：由 `scripts/verify_literature_cards.py --only B14 --no-report` 执行——把卡内所有"直双引号包住、不含中日韩字符、≥20 字符且 ≥12 个字母"的片段，在该编号登记的**每一份**本地全文里做逐字命中检查；任一条不命中即 FAIL。本卡不引用任何带未解码实体的句子，以避免比对歧义。

<!--CSV回填
work_type=论文
target=TNFR1、TNFR2、OX40、4-1BB（TNFR 超家族；平坦极性表面；同时做拮抗剂与寡聚化超激动剂）
backbone_generation=RFdiffusion 自由扩散（无脚手架，高斯残基云至 120 残基，摆在天然配体 TNF 界面上并偏向分散疏水残基）+ partial diffusion 局部重采样（加噪 15–25 步后去噪）；序列由 ProteinMPNN 复合物设计；改靶靠把已有结合体叠加到新受体后再做 25,000 条/组合的重采样轨迹
computational_filters=AF2 复合物的界面 pAE（pae_interaction）；pLDDT；复合物 Cα RMSD 到设计模型；从同一扩散轨迹更早时间步（约 120/200 步）抽取邻域骨架扩样；SSM 全位置熵指纹与晶体结构作为独立于预测的第二条证据
thresholds=送测闸口 interface pae < 7.5 且 pLDDT > 85（全文用未解码实体 &lt;7.5 / &gt;85，故本卡未作逐字引句）；扩样用 pae_interaction <20；部分扩散选池 pae_interaction <5（每起点 32 条）；改靶 TNFR2/4-1BB 通过线 pae_interaction <7.5 与 <7；加噪幅度 15–25 步（50 步即完全随机）；抽邻域骨架的时间步约 120/200
md_used=否（全文不含 MD；机理层解释靠晶体结构与 SSM 指纹）
qm_used=否（全文不含 QM/自由能计算）
experimental_methods=E. coli 表达 + SEC 单体判定 → SPR 测 KD → 全位置饱和突变库（SSM）+ 深测序做界面指纹 → X 射线晶体学（TNFR2_mb1–TNFR2，PDB 9CU8）→ HEK293 TNF-α AP-1/NF-κB/SEAP 报告测拮抗 IC50 → 与 24 种环状寡聚化结构域融合（N/C 端）在荧光素酶报告细胞系测激动 EC50/Emax → 可开发性：95 °C/30 min、鼠血清 2 h、HIC、TNFR1 敲除细胞系 off-target
pipeline_counts=自由扩散：200 步轨迹抽样 → 96 条送测 → 90 条良好表达且单体 → 6 条 SPR 结合 → 2–3 条主力；部分扩散：每起点 25,000 条骨架 → 32 条送测/起点 → 94 条高表达 → 28 条结合；改靶：每组合 25,000 条轨迹 → TNFR2 计算通过 1323 条 → 每受体 48 条实测；激动剂：44 个寡聚体（每结合体融合 24 种寡聚化域）；全流程实测序列 96+96+48 条
hit_rate=自由扩散 6/96 SPR 结合；部分扩散 30%（28/94 已表达设计）结合 TNFR1；改靶 TNFR2 32%（最优 K D of 198 pM）、4-1BB 22/48（最高 44 nM）、OX40 得 30 nM；作者强调这些通量远低于以往 tens of thousands 级展示库；未给跨靶汇总成功率，也未做 ROC 校准
best_metric=拮抗侧 TNFR1_mb2_pd1 KD <10 pM（部分扩散带来三数量级提升）与细胞 IC50 106 pM；改靶侧 TNFR2 K D of 198 pM、OX40 K D of 30 nM、4-1BB 44 nM；对照基准：天然 TNF-α 19 pM，抗体二价最高 680 pM、单体 Fab/scFv/纳米抗体 10-100 nM
cost_or_stat_note=正文未给 CPU/GPU 单价（Methods 章节未包含在本地全文中）；计算侧唯一显式规模是每起点/每组合 25,000 条扩散轨迹与每靶 32–48 条送测；实验侧强调序列下单总量仅 96+96+48，且无展示库分选；SSM 为 4047 个单点置换
role_in_timeline=把 [B08] 的 RFdiffusion 生成端从"短链/理想脚手架"放开到自由扩散，从而打进 [B06]/[B09] 时代反复失败的平坦极性靶；同时把 [B09] 的"生成后筛选"漏斗升级为"生成 → 筛选 → 再生成（partial diffusion 当廉价局部优化器）"，使亲和力成熟与家族内改靶都在计算里完成；与 [B12] 共同确立 partial diffusion 作为 binder 领域的标准局部优化步骤；实验下单量由十万级压到百级
source_pointer=data/interim/baker_lit/ft/tnfr2024.txt（唯一登记全文，40,111 B）+ sources/baker.md:185-196
CSV回填-->
