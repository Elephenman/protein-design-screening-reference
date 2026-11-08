# [B23] 把氢键配对写进生成条件——β-pairing RFdiffusion 拿下「亲水表面 + 以前做不成的靶」

Sappington I, Toul M, Lee D S, Robinson S A, Goreshnik I, … Watson J L, … Banik S M, Baker D（华盛顿大学 IPD + Ghent + Pitt + DTU + Stanford）
Nature Communications 2026, 17:1101 · DOI 10.1038/s41467-025-67866-3 · PMID 41519838 · PMCID PMC12852815
开放获取（CC BY 4.0，投稿后已更正许可）· 收稿 2024-12-20 / 接收 2025-12-10 · https://pmc.ncbi.nlm.nih.gov/articles/PMC12852815/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B23**（组：Baker组; 通用方法学; 口径对照） |
| 本地全文①（本卡引句担保） | `data/interim/baker_lit/ft/beta_pairing2026.txt`（90,275 B，SHA-256 `22446c05ea67c991…`，2026-10-16 抓取，Europe PMC 通道，标签剥离 + `scripts/litcards_text.py` 归一化） |
| 本地全文②（同文 JATS XML，独立通路） | `data/interim/claim_lit/PMC12852815.xml`（179,370 B，SHA-256 `f74a77b88c95cb1a…`，URL 记于 `inventory.json`）。门禁按规则不核验 `.xml`，但本卡用 `scripts/litcards_text.py` 的 `to_text()` 去标签后比过：**39/39 条逐字引句在①与②两份本地全文里同时命中** |
| 对照底稿 | `sources/baker.md:303-314`（原卡）；本卡在其基础上补：接口条件张量的构造规则（L 与 T 的对应）、in silico 基准的样本量（500 骨架 × 10 序列）、组合扩散/序列再采样的位置、YSD 分选策略（with/without-avidity 与 SC50）、结晶数据病理与 STARANISO 处理、SPR 拟合的排除项与 α-CTXbp 的特例模型 |
| 证据级别 | **全文级**（引句逐字命中本地全文；见第 9 节门禁结果） |
| 未取到的部分 | Supplementary Figures 1-9 与 **Supplementary Table 1（逐靶库规模与逐靶阈值的精确值）**、Supplementary Table 2（晶体学数据与内化实验细节）。凡涉及逐靶精确 cut-off 的地方本卡只给正文明写的「最低值」 |

## 1. 这篇到底解决什么（大白话）

想做出「贴在一块很亲水的表面上」的结合体很难：靶子边缘 β-strand 上排着一串裸露的氢键给体/受体，设计端必须**逐个原子把它们配平**，否则脱水代价付不起。传统 RFdiffusion 擅长「形状互补」，不擅长「氢键供受体一一对齐」；前深学习时代的 Rosetta 链配对法又跟不上真实 β-strand 的各种非规范几何（扭曲、鼓包、错位）。这篇的做法是：**把「binder 的某一段要和靶子的某条边缘链形成链配对」这件事写成二级结构 + block-adjacency 条件张量，直接喂给 RFdiffusion 的去噪过程**——只指定二级结构与接触关系，不指定三维坐标，于是链的扭曲/鼓包由模型自己去贴合。结果是七个含边缘 β-strand 的治疗相关靶（KIT、PDGFRa、ALK-2、ALK-3、FCRL5、NRP1、α-CTX）都拿到 pM–中 nM 的结合体，其中 **ALK-3 和 KIT 此前多次设计 campaign 全失败**；KITbp:KIT 的共晶结构与设计模型几乎一致，界面有 21 条氢键。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **痛点是「亲水表面补不平」，不是「形状对不上」**。原文：**"design of high affinity binders to hydrophilic regions of a target surface remains challenging since the exposed hydrogen bond donors and acceptors must be complemented with precisely positioned acceptors and donors on the designed binder to compensate for the loss of interactions with water"**，并且 **"these solutions do not always provide detailed complementarity of hydrogen bonding donors and acceptors"**（两句之间夹引文编号 7，故分开引）。→ **他们做了什么**：把氢键配平从「筛出来」改成「生成时指定」——用 SS/ADJ 条件张量声明 binder 有 L 个连续残基与靶链 T 形成链配对（**"Given the length of the designed interacting β-strand (L) and the identity of the target β-strand to be bound (T), RFdiffusion generates binders assigning a random set of L consecutive binder residues to form a β-strand pair with the target strand T"**），其余残基不给约束。
2. **Rosetta 时代的链配对法不够通用**：**"but this approach has limited ability to match the diversity of edge β-strand geometries"**。→ **应对**：让扩散模型自己吸收几何（不指定坐标），正文的立论就是 **"A generalizable deep learning method for designing β-strand pairing based binders to complement arbitrary target β-strand twists"**（后半句是 bends、bulges 等列举，中间夹引文编号，故只引前半）。
3. **两个靶此前彻底做不成，而且失败数据是公开的**：**"Prior to this study, multiple design campaigns-including campaigns utilizing RFdiffusion, ProteinMPNN, and AlphaFold 2-had failed to yield binders for ALK-3"**，另有 **"previous attempts to de novo design binders against KIT had failed"**（前半句为 As in the case of ALK-3）。→ **应对**：① 对 ALK-2/ALK-3，先做结构比较，发现两者边缘链上有五个连续残基骨架几乎重合（**"The ALK-2 and ALK-3 ectodomains have 30% sequence identity and high structural similarity"**，且这五条残基的骨架 RMSD 为 0.07），但每条链被 N-terminal coil 部分遮挡，于是**只指定未被遮挡的那五个残基**做配对（**"We conditioned RFdiffusion on generating β-strand pairings to these five edge β-strand residues that were not occluded by the N-terminal coil"**）；② 把失败的库文件随论文公布（Data availability 里的 `alk3_kit_failed_libraries.zip`）。**代价**：这两个靶在展示筛选里仍最难，**"with less than 1% of designs showing strong binding and enrichment"**。
4. **FCRL5 连一个实验结构都没有**：**"Because no experimentally determined structure exists for FCRL5, we designed binders against the AlphaFold 2 model"**。→ 应对：直接用 AF2 模型当靶输入，并把它和 KIT/PDGFRa 的 PDB 结构并列做同一套流程；结果 FCRL5bp 82 nM。
5. **PDGFRa 两个来源的靶结构互相矛盾**：**"Despite significant disagreement between the cryo-EM structure and the AlphaFold 2 model regarding the conformation of the target domain 2 Ig fold, design against both conformations yielded high-affinity binders"**。→ 应对：**不裁决，两条都下单**，分别得到 PDGFRabp-7LBF 与 PDGFRabp-AF2model，并补一句机理解释作为「为什么两个都能成」：**"The binders may selectively induce the cognate PDGFRa conformation upon binding, as their design model conformations are not cross-compatible"**。
6. **β 条件化并非在所有靶上都更好**。PDGFRa 那个位点是例外：**"the PDGFRa target site, which was likely more amenable to helical bundle binder design success due to its flat, hydrophobic surface"**。→ 应对：不强行统一路线，helical 与 strand 两类设计都放进过滤，按 in silico 通过率与实验命中数分配预算，并明写该位点更适合螺旋束。
7. **共享同一套链配对机制，怕特异性塌掉**（所有 binder 都用 β-strand 贴 β-strand）。→ **应对**：做 all-by-all SPR（同一批浓度梯度扫所有 binder × 所有靶），结论 **0 例显著脱靶（"There was no evidence for off-target binding of the ALK-2, ALK-3, KIT, and PDGFRa binding proteins to related family members"**，仅在 1.5 μM/200 nM 两档比较响应）。给出的解释是：**"the binders for each structurally similar target pair (i.e., ALK-2 and ALK-3, KIT and PDGFRa, FCRL5 and NRP1), were designed with different β-strand pairing hydrogen bonding arrays"**，且除 ALK-3bp 外每个 binder 还额外做了 α-helical 接触；并补一条反向验证：SCF 饱和浓度使 KIT 文库的分选计数下降 99%，说明口袋占用可被天然配体竞争。
8. **暴露的边缘链会带来聚集风险（设计端自己造了一个「粘性面」）**。→ **应对**：拿 SEC 与 CD 热熔做体检而不是靠预测，**"No obvious trends were observed between the size of the edge β-strand interface and aggregation propensity of the binders"**，并给出一个具体反例式证据：**"ALK-3bp was stable and monomeric up to 95"**（后接 °C 与「despite having four exposed edge β-strands」，中间夹单位故不合并）。作者的收口解释是自然界的非规范几何本身就抑制错配：**"very high binding specificity and the lack of significant aggregation of our designs despite the availability of edge β-strands for intermolecular interactions supports the conjecture that non-canonical β strand geometries suppress off target pairing"**。此外用 AF2 单体预测解释 KITbp 为什么不粘：**"Alphafold 2 prediction of the monomeric KITbp without KIT target places the β-strand pairing residues in a coil conformation"**（去掉靶子后那条链自发卷成 coil，遮蔽疏水核心与氢键原子）。
9. **晶体数据有病理**：各向异性 + 平移性非晶体学对称。**"severe data pathologies, including strong anisotropy and translational noncrystallographic symmetry, were revealed"** → **应对**：椭圆截断并用 STARANISO 服务器校正后再精修（**"the data were elliptically-truncated and corrected using the STARANISO"**），最后仍拿到 2.8 Å、与设计模型 1.9 Å 全原子 RMSD。
10. **SPR 高端浓度不可信**：**"10 μM data was excluded from the fit due to non-ideal solution behaviour"**（Fig 2c 图注另给一句：signal aberrations at this high binder concentration）；α-CTXbp 因双相结合改用非均相动力学模型。→ 应对：**先声明排除项再拟合**，而不是硬套 1:1 Langmuir。
11. **下单预算怎么定？** 展示库规模跨两个数量级（96 到 5,000）。→ **应对**：**把 in silico 通过率当作预算变量**：**"In silico and experimental library sizes depended on the in silico filter success rate, and the perceived difficulty of designing a binder interface based on target surface concavity, target surface hydrophobicity measured by SAP, and known previous experimental challenges (as for ALK-2, ALK-3, KIT, unpublished data)"**，并明确 **"resulting in libraries ranging in size from 96 to 5000 that were screened experimentally"**。事后复盘：NRP1 与 α-CTX 用 96 孔规模就出命中（**"Binders for α-CTX (originally introduced by Vazques-Torres, et. al.) and NRP1 (1.9 nM and 101 nM, respectively) were obtained by testing the 96 designs based solely on in silico metrics"**）。
12. **三个靶的功能读出做不了**。→ **应对（其实是承认边界）**：**"ALK-2bp, ALK-3bp, and NRP1bp could not be tested for functional agonism in a straightforward manner, as the native ligands for ALK-2 and ALK-3 promiscuously activate signaling with other BMP receptors and NRP1 acts as a cofactor in signaling for various RTKs"**。本文未解决该三项的功能层证据（α-CTXbp 的中和小鼠实验交给配套研究）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **生成端（本文的创新点）**：RFdiffusion 的 **interface conditioning**——除单体二级结构条件外，额外构造 N×N block-adjacency 中的「binder 残基 ↔ 靶残基」接触块，声明「这 L 个连续 binder 残基 = strand，且与靶链 T 配对」。**不给三维坐标**，所以扭曲/鼓包由模型自己拟合。作者说明该条件的信息**在轨迹极早期就被吸收**：**"This information influences the denoising in very early trajectory timesteps (t), with the tertiary fold determined within 5 timesteps and the final output at t = 50"**。
- **序列端**：ProteinMPNN，每个骨架 10 条序列（基准实验里）。
- **过滤端**：AF2 **initial guess**（复合物，取 interface pAE 与 binder pLDDT）+ AF2 单体 pLDDT + Rosetta FastRelax 的 ΔΔG + radius of gyration（ROG）+ SAP；必要时走 **iterative partial RFdiffusion + ProteinMPNN cycling** 做 in silico 局部优化。
- **文库端**：DNAworks2.0 反向翻译做 10⁴ 规模 DNA 库 → pETcon3 酵母表面展示 → with-avidity 起手 + without-avidity 递减浓度 → NGS 算 **SC50**（沿用 Cao 等的口径）；库内先按序列相似度/RMSD 聚类做**等比例抽样**。
- **确证端**：E. coli 表达 + AKTA FPLC 96 孔自动 SEC；CD 全谱 + 217 nm 热熔定 Tm；SPR（Biacore 8K，生物素 CAPture 芯片捕获受体）；KIT D1-3 由 HEK293 瞬转 + Endo Hf 去糖后结晶；FCRL5bp 内化与 FCRL5bp-EGFRbp 融合降解 EGFR；PDGFRabp-7LBF 在 CHO-PDGFRα 里阻断 PDGF-AA 的 Erk/Akt 磷酸化。
- **没有用的方法**：MD、QM、自由能微扰。

### A. in silico 基准（先证明「条件化」本身值不值）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 7 个靶的 8 个位点（PDGFRa 因预测结构多变取 2 个位点） | 两条路并行：**"Following the generation of 500 scaffolds using each diffusion approach, ten candidate binder sequences were generated for each scaffold by ProteinMPNN"**，再用 AF2 initial guess + Rosetta FastRelax 评估 | 「reasonable quality metrics」= pAE interaction <10、pLDDT >85、ΔΔG < -30（见 B3 的最低值口径） | **"over 9.2% of β-strand interface conditioned designs meeting reasonable quality metrics, in contrast to 0.98% success rates by RFdiffusion conditioned on target hotspots alone"**；且 **"β-strand interface conditioning yielded in silico design successes for all targets, whereas hotspot conditioning alone did not yield any in silico successes for two targets (ALK-3 and FCRL5)"** |
| A2 | 同一批骨架 | 折叠质量与结构空间分布 | 球半径判据（ROG，按 binder 长度调整）；all-by-all TM-score + t-SNE | **"88.7% of output scaffolds meeting radius of gyration criteria and only 25.5% of designs from the other methods meeting the same criteria"**；两条路占据不同结构空间，β 路线 β-sheet 比例升高、α-束输出减少 |

### B. 生产级设计-下单流程（每靶）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 靶结构来源：PDB（KIT 2E9W、NRP1 2QQI、PDGFRa 7LBF）或 AF2 模型（ALK-2、ALK-3、FCRL5、PDGFRa 另一构象） | 先看表面疏水与边缘链暴露度，决定用哪条链、指定哪些残基 | 未给数值阈值（定性：可及性与凹凸度、SAP） | 选定 7 靶 8 位点 |
| B2 | 位点 + 目标边缘链 | 用脚本生成接口条件张量；RFdiffusion 同时跑 hotspot 路与 β 条件路 | 条件规则：链配对段长度 = 靶边缘链长度 | **"Five to ten thousand binder backbone scaffolds complementing these sites were generated by standard RFDiffusion design with hotspot conditioning as well as β-strand interface conditioning"** |
| B3 | 骨架 → ProteinMPNN 序列（数十万条） | AF2 initial guess + AF2 单体 + Rosetta ΔΔG + ROG + SAP 过滤；必要时迭代 partial diffusion 再 MPNN | **"The cutoff values for these metrics varied somewhat for each target protein, but obtained minimum values of pAE interaction <10, pLDDT >85, ΔΔG < -30, a variable ROG filter adjusted for binder size length/4.5 = ROG, and SAP < 45"**；严格档：**"Structurally diverse designs with high AlphaFold 2 confidence (interface pAE <8 and pLDDT > 85) designs were selected for experimental screening by yeast surface display"** | 数十万序列 → 库规模 96–5,000（**"resulting in libraries ranging in size from 96 to 5000 that were screened experimentally"**） |
| B4 | 过滤后设计集 | 按序列相似度/RMSD 聚类，保证每个簇在最终库里等比例出现 | 无阈值（多样性约束） | 下单库（多样性受控） |
| B5 | DNA 库（10⁴ 规模，反向翻译按酵母密码子频率） | pETcon3 转化 EBY100 → with-avidity 起手排除弱结合 → 多轮 without-avidity 递减浓度 → NGS → SC50 | SC50（Cao 口径）；ALK-2/ALK-3 上强结合富集的比例 **"with less than 1% of designs showing strong binding and enrichment"** | 富集命中：FCRL5 从 **4841** 库、KIT 从 **1298** 库、PDGFRa 从 **5427** 与 **189** 库、NRP1 与 α-CTX 从 **96** 孔规模 |
| B6 | 最富集（表达量 + 亲和）设计 | E. coli 500 mL 自诱导表达 → Ni-NTA → SEC（96 孔自动 FPLC）→ CD 全谱与热熔 | Tm 判定规则：**"For designs retained more than half of the mean residue ellipticity values, Tm values are reported as greater than 95"**（后接 °C，故只引前半）；单体性看 SEC 峰 | 可溶、单体、耐热（Tm 记录：ALK-2bp 81.2、KITbp 63.2、α-CTXbp 95、PDGFRabp-AF2model 95、NRP1bp 77.2、PDGFRabp-7LBF 71.1 °C，FCRL5bp >95 °C） |
| B7 | 纯化蛋白 | SPR 动力学（Biacore 8K，单周期，6 档 7 倍稀释 600 pM–10 μM） | 1:1 Langmuir 全局拟合；高端点剔除：**"Fits for K d determination (green) excluded the 10 μM data excluded due to signal aberrations at this high binder concentration"**；α-CTXbp 例外用非均相模型 | Kd：PDGFRabp-7LBF **137 pM**、ALK-3bp **528 pM**、α-CTXbp **1.9 nM**、NRP1bp **101 nM**、PDGFRabp-AF2model **4 nM**、KITbp **65 nM**、FCRL5bp **82 nM**、ALK-2bp **96 nM** |
| B8 | 全部 binder × 全部靶 | all-by-all SPR | 以「相对自身最大响应」归一比较脱靶信号 | 无显著脱靶；同家族之间（ALK-2/ALK-3、KIT/PDGFRa）也不交叉 |

### C. 结构确证与生物学读出

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | KIT D1-3（HEK293 瞬转 + Endo Hf 去糖）+ KITbp（3 倍摩尔过量） | 坐滴蒸气扩散结晶（BCS-Screen，G11 条件），P13/PETRA III 收集 | 分辨率与 RMSD；数据病理需校正 | **2.8 Å**；全原子 RMSD 1.9 Å，binder 全原子 2.0 Å、骨架 0.98 Å；PDB 9H71 |
| C2 | 复合物界面 | HBPLUS 数氢键 + DSSP 判链配对与平行/反平行 + SASA 极性比例 | 「设计是否被复现」= 预测氢键命中数 | **21** 条界面氢键（多于以往设计与多数同尺寸天然界面）；其中 **16 out of 21** 被设计模型正确预测；链配对 8 个残基贡献 9 条；界面 1164 Å²，链配对面 291 Å²（65% 极性）vs 其余 873 Å²（45% 极性） |
| C3 | KITbp | Foldseek 比对整个 PDB | 有无显著已知折叠匹配 | 无显著匹配；天然蛋白里找不到孤立 β-strand 的先例（仅在复合物界面中由 loop 延伸成链） |
| C4 | KITbp 单体 | AF2 只预测 binder（无靶） | 链配对残基的构象 | 预测为 coil，遮蔽疏水核心与界面氢键原子 → 提出「结合诱导链形成」解释 |
| C5 | FCRL5bp | pHrodo DeepRed 标记 + 活细胞成像（Dox 诱导 FCRL5 表达） | 红/绿重叠信号随 FCRL5 表达量与时间 | 18 h 达稳态内化，与 FCRL5 表达水平相关 |
| C6 | FCRL5bp-EGFRbp 融合（两种末端方向） | HeLa-FCRL5 里做 EGFR 内吞降解（50 nM，与 EGF 对照） | 依赖 Dox 诱导的 FCRL5 表达 | Western 与流式均显示 EGFR 降解，与天然 EGF 通路可比 |
| C7 | PDGFRabp-7LBF | CHO-PDGFRα 中阻断 PDGF-AA 诱导的磷酸化 | IC50 | Erk **19.6 nM**、Akt **38.25 nM**；重复四次结果相似 |

**这套流程的骨架值得单独记住**：先做一次**便宜的 in silico A/B 实验**（同一批靶、两条生成路线、同口径打分）来证明「改生成条件」值不值，再按 **A 段的通过率**反推 B 段该下多大的库，最后把「结构对不对」交给晶体学而不是交给打分器。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处 |
|---|---|---|
| 9.2% vs 0.98% | β 条件化 vs 仅 hotspot 条件的 in silico 通过比例 | A1 段（Fig 1c 相应正文） |
| 500 骨架 × 10 序列 | 基准实验样本量 | Methods「In silico comparison」 |
| 88.7% vs 25.5% | 两类骨架满足 ROG（球半径/紧凑度）判据的比例 | A1 段 + Supplementary Fig 3 |
| 5 个 timestep | 接口条件对去噪轨迹的作用窗口（三级结构在 5 步内定形，输出 t=50） | Fig 1b 图注 |
| 5,000–10,000 / 路 / 靶 | 生产级骨架生成规模 | Methods「Production scale computational protein design workflow」 |
| pAE interaction<10、pLDDT>85、ΔΔG<-30、ROG=length/4.5、SAP<45 | 各过滤项的「最低值」口径（逐靶另调） | Methods 同上 |
| interface pAE<8 且 pLDDT>85 | 送展示前的严格档 | Fig 2 前正文 |
| 数十万序列 → 96–5,000 | 计算过滤把序列空间削成可下单库 | Methods 同上 |
| 10⁴ | 每靶 DNA 库规模（反向翻译、按酵母密码子频率） | Methods「DNA library preparation」 |
| <1% | ALK-2/ALK-3 展示库里强结合富集的比例 | ALK 段正文 |
| 4841 / 1298 / 5427 / 189 / 96 | 各靶实际下单库规模（FCRL5 / KIT / PDGFRa-7LBF / PDGFRa-AF2 / NRP1 与 α-CTX） | 各靶结果段 |
| 137 pM、528 pM、1.9 nM、4 nM、96 nM、101 nM、82 nM、65 nM | 逐靶最优 Kd（PDGFRabp-7LBF、ALK-3bp、α-CTXbp、PDGFRabp-AF2model、ALK-2bp、NRP1bp、FCRL5bp、KITbp） | B7 汇总 |
| 600 pM–10 μM、7 倍稀释、单周期 6 档 | SPR 浓度阶梯与拟合设定（10 μM 点被剔除） | Methods「Surface plasmon resonance」 + Fig 2c 图注 |
| 81.2 / 63.2 / 95 / 95 / 77.2 / 71.1 °C，>95 °C | 各 binder 的 CD Tm（ALK-2bp、KITbp、α-CTXbp、PDGFRabp-AF2model、NRP1bp、PDGFRabp-7LBF；FCRL5bp >95） | 「Stability of binders」段 |
| 2.8 Å；1.9 / 2.0 / 0.98 Å | KITbp:KIT 晶体分辨率与全原子/骨架 RMSD | 「KITbp:KIT complex structure」段 |
| 21；16 out of 21；9 | 界面氢键总数 / 被设计模型预测中的数量 / 链配对 8 残基贡献数 | 同上 + HBPLUS 计算段 |
| 1164 Å²；291 Å²；873 Å²；65% vs 45% | 界面总 SASA / 链配对残基 / 其余残基 / 两者极性原子占比 | 同上 |
| 30%；RMSD 0.07 | ALK-2 与 ALK-3 胞外域序列同一性 / 五个边缘残基骨架重合度 | ALK 段 |
| 99% | 60 μM SCF 使 KIT 展示文库分选计数下降幅度 | 同上 |
| 19.6 nM；38.25 nM | PDGFRabp-7LBF 阻断 PDGF-AA 的 Erk / Akt IC50 | 「Biological functionality」段 |
| 50 nM；18 h | 内化/降解实验用量与达稳态时间 | Fig 5 图注 |
| 7 靶（除 α-CTX 均为癌症治疗靶点） | 靶集合的治疗相关性 | Introduction |

## 5. 结论——作者说了什么

1. **RFdiffusion 可以被条件化成「生成几何匹配的扩展 β-sheet 并配平靶上极性基团」**，且不需要指定三维坐标。
2. 相比 hotspot 条件，β-pairing 条件在**同一批靶上把 in silico 通过率提高约一个数量级**（9.2% vs 0.98%），并且**为 hotspot 完全失败的 ALK-3、FCRL5 产出了 in silico 成功**。
3. 实验端在 7 个边缘链靶上拿到 **pM–中 nM** 亲和力与更高命中率；KITbp:KIT 共晶几乎等于设计模型（1.9 Å 全原子、界面氢键 16/21 被预测中）。
4. **共享链配对机制不等于失去特异性**：作者把特异性归因于「每对相似靶用了不同的链配对氢键阵列 + 额外非链配对接触」，并支持 Richardsons 关于「非规范边缘链几何抑制错配」的推测。
5. 结合体稳定且单体：即使带四个暴露边缘链的 ALK-3bp 仍 95 °C 单体。
6. 方法把可及的靶表面扩展到「Ig fold 与 β-sheet 富集的胞外域」这类常见治疗靶。
7. 作者自限：这些结合体「未必能直接当药」，亲和力、稳定性、药代、种属交叉、寡聚化、蛋白酶稳定性都还需再优化；ALK-2/ALK-3/NRP1 的功能读出没有干净体系。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **他们的跃升来自「把最难补的相互作用写进生成条件」，而不是「把判据调得更准」**。A 段只换了生成路线、打分口径没变，通过率就差 10 倍。→ 对我们：若某类化学约束（比如两个金属的同时配位、或 3′-OH 对 α-磷酸的进攻取向）是可写成条件的，就该写进生成端，而不是留着让筛子事后找。
2. **接口条件的作用窗口极早（5 步定三级结构）**——说明这类约束的成本很低（只影响轨迹早期），这与「后处理罚函数」完全不同。→ 我们的几何约束也应尽量放在采样早期，而不是放在评分端反复重算。
3. **「通过率决定下单规模」是本文最可直接搬走的工程规则**：同口径跑一小批 in silico A/B（500×10 的量级），拿到通过率，再按预算反推 96 还是 5,000。这条不依赖任何具体判据的物理含义。
4. **面对相互矛盾的结构证据（PDGFRa 两种构象），他们选择「不裁决、都下单」**，用实验命中来消解歧义——这是把计算争议转成预算问题。我们手上若有 apo/holo 或金属态争议，同样可以用「两条都进池、共用一次读出」代替先做更贵的判定。
5. **失败数据被公开为资产**（ALK-3/KIT 失败库随文发布）。→ 我们要建真值面板时，负例库应当作正式交付物，而不是留在 log 里。
6. **「特异性」的证据是设计出来的对照，不是算出来的分数**：all-by-all SPR + 天然配体竞争 + 同家族交叉检验。对应我们：任何「选择性」主张都必须自带交叉底物/竞争副产物的对照，而不是靠单一位点打分。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：ALK-2/ALK-3/NRP1 无直接功能读出；结合体治疗可行性尚远；逐靶阈值「varied somewhat」，精确值在 Supplementary Table 1（本次未取）；FCRL5 依赖 AF2 模型（无实验结构）。
- 我们读出：① **9.2% 是 in silico 通过率，不是实验命中率**；实验侧最硬的比例是「<1% 强结合富集」与「96 孔里出 1 条」。② 每条路线只测一次基准（500 骨架），**两臂差 10 倍但绝对命中数都是个位数**，置信区间很宽。③ 「特异性来自不同的氢键阵列」是**事后解释**，本文没有做「随机重排条件化残基」之类的机制检验。④ α-CTXbp 的 SPR 用非均相模型，说明该复合物不是简单 1:1；10 μM 点被剔除，说明高浓度端行为已偏离模型。⑤ 全文无 MD/QM/自由能，对「氢键配平的脱水代价」没有能量学计算，只有结构计数——这与「预组织/系综」类判据是互补而非等价关系。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **「通过率 → 下单规模」的预算公式**（G8 成本门）：任何新条件/新判据先用一次小规模同口径 A/B（固定生成样本量、固定打分链）得到通过率，再由「每候选下单成本」反推库规模上限，并允许缩到 96 孔级；写进 run.md 的公式应显式包含「按目标表面难度（凹凸度/亲水性/历史失败记录）上调预算」这一项。
2. **把最难的化学约束写成生成条件**：与 [B20] 的原子级 motif scaffolding 同向。对我们，「底物取向 + 两金属配位 + 进攻原子距离」若可表达为残基/原子的接触与二级结构约束，就应在生成端指定，而不是留给事后打分。
3. **矛盾输入不裁决、并行下单**：对 apo/holo、不同金属态、不同寡聚态争议，用「两版都进池 + 共用一次读出」替代先做昂贵的机制判定，并在结果里注明两版设计是否互不兼容（他们正是用「互不兼容」推出结合诱导构象）。
4. **特异性靠交叉矩阵而非单点分数**：任何「这个酶只做我们要的反应」的断言，必须配 all-by-all 式的交叉底物/竞争副产物读出。我们的分步化学事件失败分型可以套这个思路：一个阳性之外，还要看「不该发生的邻近反应有没有发生」。
5. **把失败集当交付物**：负例库（序列/模型/参数）随结果发布，作为下一轮判据的标定集（对应 G0 真值面板）。
6. **结构体检放在实验侧**：SEC 单体性与 CD 热熔这类「便宜但不给功能」的检查，适合当漏斗中段的「能不能进下一层」闸门；我们对应的是可溶表达 + 蛋白完整性检查，不要指望它预测活性。

**不可迁移（为什么不能照搬）**

1. **pAE interaction<10、pLDDT>85、ΔΔG<-30、SAP<45、ROG=length/4.5 是「结合界面自洽 + 可溶」的判据**，量的是静态界面；目标酶要判断的是三步化学事件与连接选择性，本库判据 §2 明令禁止把 binder 的 pAE/ipTM 阈值当酶活闸口。
2. **9.2% / 0.98% 与「<1% 强结合富集」都是结合读出下的数字**，且绝对命中是个位数；**不得**换算成我们对酶设计的任何成功概率，也不得用来校准「某法对酶设计成功率 X%」。
3. **10⁴ 规模的酵母展示 + SC50** 在产物化学上不存在：我们不能把「摊大库」当成同等解法，漏斗末端仍要走信息量最大化（机制多样性 + 失活对照 + 竞争副产物定量）。
4. **「用几何条件保证氢键配平」不能推成「催化能垒下降」**：本文的氢键计数是界面结合氢键，不是沿反应坐标的过渡态稳定化；后者需要系综/QM 层证据（本文完全没有）。
5. **本文的靶是「被结合的受体位点」**，其成功标准是亲和力与阻断活性；我们若要引用它的「pM–nM」量级，只能引作「binder 侧的可达上限」，不可引作酶改造侧的期望值。

## 9. 溯源与自检

- 引句底稿: data/interim/baker_lit/ft/beta_pairing2026.txt
- 两通路互证：39/39 条引句在①（txt）与②（JATS XML，`to_text()` 去标签）里同时命中。
- 本地全文：`data/interim/baker_lit/ft/beta_pairing2026.txt`（SHA-256 `22446c05ea67c991…`）；同文 JATS XML `data/interim/claim_lit/PMC12852815.xml`（SHA-256 `f74a77b88c95cb1a…`，门禁不核验 xml，本卡引句未在其上担保）。
- 对照底稿行号：`sources/baker.md:303-314`；汇总表相关行：`sources/baker.md:605`（3a 自洽闸口）、`606`（3b 物理项，46–96 个/靶的下采样规模）、`610`（5a 展示库通量）、`648`（按 in silico 通过率反推下单库规模）、`680`（阈值 per-campaign 调整、需 Supplementary Table）。
- 代码与数据指针（原文）：`https://files.ipd.uw.edu/pub/strand_pairing_binders_2025/`（含 `interface_tensors.zip`、`anaysis_scripts.zip`、`facs_data.zip`、`experimentally_tested_design_pdbs.zip`、**`alk3_kit_failed_libraries.zip`**）；RFdiffusion GitHub；AF2 initial-guess 脚本 Zenodo；PDB 9H71（本文）与 9BK6（α-CTXbp 配套研究）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检命令**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B21 B22 B23 --no-report`。结果见回报。

<!--CSV回填
work_type=论文
target=边缘 β-strand 位点：KIT、PDGFRα（7LBF 构象与 AF2 模型两版）、ALK-2、ALK-3、FCRL5、NRP1、α-CTX（共 7 靶 8 位点）
backbone_generation=β-strand interface conditioned RFdiffusion：在二级结构 + block-adjacency 张量里声明「binder 的 L 个连续残基为 strand 且与靶边缘链 T 接触」，不指定三维坐标；对照路为 hotspot 条件 RFdiffusion；辅以迭代 partial RFdiffusion + ProteinMPNN 循环做 in silico 局部优化；序列端 ProteinMPNN（每骨架 10 条）
computational_filters=AF2 initial guess 复合物 interface pAE + binder pLDDT、AF2 单体 pLDDT、Rosetta FastRelax ΔΔG、radius of gyration(ROG)、SAP；展示侧 SC50（Cao 口径）；结构侧 HBPLUS 氢键计数、DSSP 链配对取向、SASA 极性占比、Foldseek 新颖度
thresholds=最低值口径 pAE interaction<10、pLDDT>85、ΔΔG<-30、ROG=length/4.5、SAP<45（作者明写逐靶变动，精确值在 Supplementary Table 1）；送展示前严格档 interface pAE<8 且 pLDDT>85；β 条件化 vs hotspot 的 in silico 通过率为 9.2% vs 0.98%；ROG 合格率 88.7% vs 25.5%
md_used=否
qm_used=否
experimental_methods=10⁴ 规模 DNA 库（DNAworks2.0 反向翻译）→ pETcon3/EBY100 酵母表面展示（with-avidity 起手 + without-avidity 递减浓度）→ NGS 算 SC50 → E. coli 500 mL 表达 + Ni-NTA + AKTA FPLC 96 孔自动 SEC → CD 全谱与 217 nm 热熔定 Tm → Biacore 8K SPR 单周期动力学（600 pM–10 μM，7 倍稀释；10 μM 点剔除；α-CTXbp 用非均相模型）→ all-by-all 特异性 SPR → KIT D1-3(HEK293+Endo Hf) 共晶 X 射线 2.8 Å → FCRL5bp 内化与 FCRL5bp-EGFRbp 融合降解 EGFR（HeLa-FCRL5）→ CHO-PDGFRα 中 PDGF-AA 磷酸化阻断（Erk/Akt Western + Jess）
pipeline_counts=每靶 5,000–10,000 骨架（两条路线）× 10 序列（数十万序列）→ 计算过滤后 96–5,000 的下单库（NRP1/α-CTX 各 96；KIT 1298；FCRL5 4841；PDGFRa 5427 与 189）→ 7 靶各得 1–2 条最优 binder；ALK-2/ALK-3 展示库强结合富集 <1%
hit_rate=β 条件化 in silico 通过 9.2% vs hotspot 0.98%（约一个数量级），且 hotspot 路在 ALK-3 与 FCRL5 上 0 个 in silico 成功；实验侧 ALK-2/ALK-3 富集 <1%；困难靶（ALK-3、KIT）此前多次 campaign 全失败（失败库随文公布），本文各出 1 条 pM/nM 级 binder；作者未给跨靶平均实验命中率
best_metric=Kd：PDGFRabp-7LBF 137 pM、ALK-3bp 528 pM、α-CTXbp 1.9 nM、PDGFRabp-AF2model 4 nM、ALK-2bp 96 nM、NRP1bp 101 nM、FCRL5bp 82 nM、KITbp 65 nM；功能：PDGFRabp-7LBF 阻断 PDGF-AA 的 Erk IC50 19.6 nM、Akt IC50 38.25 nM；结构：KITbp:KIT 2.8 Å，全原子 RMSD 1.9 Å，界面 21 条氢键中 16 条被设计模型预测
cost_or_stat_note=未记录（正文无 GPU/CPU 时间与每候选成本数字）；可核对的规模口径：500 骨架 × 10 序列的 in silico A/B、5,000–10,000 骨架/靶/路线、96–5,000 下单库、10⁴ DNA 库、SPR 六档浓度；晶体学需椭圆截断 + STARANISO 校正各向异性与平移性 NCS；α-CTXbp 需非均相动力学模型
role_in_timeline=把 [B08]/[B09]/[B20] 的「自洽性闸口 + 原子级约束」推进为「把界面氢键配对直接写进生成条件」：在同一批困难靶（ALK-3、KIT）上第一次拿到 pM/nM 结合体，并把漏斗参数化——用 in silico 通过率和靶表面难度（凹凸度、SAP、既往失败记录）显式决定下单库规模（96↔5000），是「判据之外、生成端改条件」这一路线的代表案例
source_pointer=data/interim/baker_lit/ft/beta_pairing2026.txt（SHA 22446c05ea67c991…）+ data/interim/claim_lit/PMC12852815.xml（SHA f74a77b88c95cb1a…，门禁不核验）；sources/baker.md:303-314
CSV回填-->
