# [K64] Riff-Diff：先把催化 motif（理想活性位点阵列）定死，再为它反向造骨架——一篇"motif 优先"的 one-shot 酶设计全文

Braun M, Tripp A, Chakatok M, Kaltenbrunner S, Fischer C, Stoll D, Bijelic A, … Oberdorfer G（奥地利 Graz 理工大学生物化学所；通讯 Oberdorfer/Hall）
Nature 2025, 649(8095):237–245 · DOI 10.1038/s41586-025-09747-9 · PMID 41339546 · PMCID PMC12727513
开放获取（CC BY 4.0）· 全文链接 https://doi.org/10.1038/s41586-025-09747-9 · 代码 https://github.com/mabr3112/riff_diff_protflow

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K64**（组：通用方法学；CSV 现记 has_baker=False） |
| 论文全称 | rotamer inverted fragment finder–diffusion，简称 **Riff-Diff**（"Here we present rotamer inverted fragment finder-diffusion (Riff-Diff), a hybrid machine learning and atomistic modelling strategy for scaffolding catalytic arrays in de novo proteins"） |
| 本地全文 | `data/interim/baker_lit/ft/motifscaffold2026.txt`（82,645 字符 / 148 行；Europe PMC fullTextXML 抽取后去标签纯文本，抓取通道见 `inventory.json` 的 `fetch_url` = https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12727513/fullTextXML）。**身份块已复核**（防抓取挂错行）：文件第 1 行的头部字段为 `Nature Nature PMC12727513 12727513 12727513 41339546 10.1038/s41586-025-09747-9 Computational enzyme design by catalytic motif scaffolding Braun Markus`，PMCID / PMID / DOI / 标题 / 第一作者与 CSV 与 `inventory.json` **四项一致**，故本卡引句确实来自本文正文。本卡全部引句按 `AGENT_RULES` 归一化口径与该文件逐字比对（见第 9 节） |
| 登记底稿 | `sources_map.json` 的 K64 三项：上述全文 .txt + `sources/baker.md` + `sources/cost-benchmarks.md`。**门禁只与"引句底稿"那一行声明的文件逐字比对** |
| 证据级别 | **全文级**（正文 + Methods 在本地；补充信息 Supplementary Methods/Tables/Figs **不在本地**，涉及处本卡明写"仅在正文提及、数值在补充材料"） |
| 未取到的部分 | Supplementary Methods（含通道占位螺旋的自定义辅助势细节、MBH 两组设计的完整协议）、Supplementary Figs 1–18、Supplementary Tables 1–8、Extended Data Table 1 的晶体学参数表体、Fig 1c 流程图原图。凡引用这些处均标"正文未给出该数字，仅有正文描述" |
| ⚠ 与登记元信息不符（已核验，不改 CSV） | 本地全文的作者表是 **Braun M, Tripp A, Chakatok M, Kaltenbrunner S, Fischer C, Stoll D, Bijelic A, Elaily W, Totaro M G, Moser M, Hoch S Y, Lechner H, Rossi F, Aleotti M, Hall M, Oberdorfer G**，单位是 **Graz University of Technology（奥地利 Graz 生物化学所）**，通讯为 Oberdorfer/Hall；`sources/baker.md:593` 与 CSV `第一或通讯作者` 字段写的 "Braun M, … **Hilvert D**（ETH Zürich）" **与本地全文作者表不符**（Hilvert 不是本文作者；推测误记来源：本文所用的两套催化阵列都取自 Hilvert 实验室的工作——retro-aldol 四元组 RA95.5-8F（ref 5 Obexer 2014，PDB 5AN7）与 MBH 的 BH32.14 / BH1.8（ref 4、30），此点为解释性推断）。CSV 里 `是否用QM=是-化学步` 也与全文不符：正文与 Methods 里没有 QM/DFT 计算，QM 只出现在参考文献 41（De Raffele 等的 QM/MM 研究）。本卡按全文实况写。 |
| 本篇为什么对我们关键 | 这是本项目里**唯一一篇严格"先定催化 motif、再反向造骨架"**并给出成套湿实验结局的 Nature 全文：motif 定义方式、送测数（36 + 63 = 99 条序列）、命中率（91% / 94% / 93.3% 有活性，7/35 达到 kcat>10⁻³ s⁻¹）、以及作者自陈的失败模式（活性预测近乎不可能、RMSD 判据失效、MD 判据不相关）都在正文里。 |

## 1. 这篇到底解决什么（一句话 / 大白话）

**一句话**：他们把"已知高活性酶的活性位点侧链（sidechain）阵列"（催化四元组 / His-Glu-Arg 三元组 / 单个 Glu）当成**不可移动的输入**，先用 rotamer 反演 + 螺旋片段拼装把它变成一组物理上可行的"人工 motif"，再让 RFdiffusion **围着它长出一整条全新骨架和结合口袋**，最后**只送测不到 100 条序列**就拿到 kcat 达到 10⁻² s⁻¹ 量级（比既往 one-shot 设计快几个数量级、甚至超过跑完 8 轮定向进化筛了 13,590 个克隆得到的 BH32.8）的酶。

**大白话**：以往 de novo 酶设计的顺序是"先找/造一个空腔，再往空腔里摆催化基团"，摆不准就白做；这篇把顺序**倒过来**——催化基团的空间排布先钉死，骨架是为这套给定的排布量身生成的。作者要解决的痛点是他们自己在开篇点名的："the current paradigm for generating efficient biocatalysts is to compensate for low initial efficiencies with high-throughput screening and directed evolution"，而对"自然界不存在、也没法用高通量筛选"的反应（例如 MBH 反应），这条路走不通，所以要做 one-shot。

**它同时给出一份"筛子考卷"**：6 个设计拿到原子分辨率晶体结构 + 35 个设计的折叠性/活性/稳定性 + 30 条 RAD 与 2 条 MBH 的稳态动力学参数，用来回答"哪些计算判据真的能预测活性"。结论对判据很不留情面——"This was highlighted by the negligible correlation between predicted enzyme rankings and actual activity in this and previous studies"（第 2、7 节展开）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **难点：把催化阵列直接"倒"进骨架，做出来的 motif 本身就不物理**。
   现象/证据（原句）："This arbitrary arrangement of fragments can result in physically implausible motifs and low scaffolding success rates."
   **他们做了什么**：不硬拼，而是写了一个 motif 库生成脚本——把催化阵列的 rotamer **反演**（固定官能团、让骨架原子去动），再按片段骨架的 phi-psi 相容性挑 rotamer，然后穷举互不位阻的片段组合并按 rotamer 概率 + PDB 出现频率排序："The script starts by inverting rotamers of the catalytic array, which fixes the functional groups in space and varies the position of their backbone atoms"、"Non-clashing assemblies are ranked according to the rotamer probabilities of the individual active site residues and by their abundance in the Protein Data Bank (PDB)"。
   代价：最终只有少数 motif 可用——RAD 系列 36 条序列只来自 **8 个 unique artificial motifs**（"The final selection consisted of 36 sequences derived from 12 unique backbones generated from 8 unique artificial motifs, named RAD1-36"）；库里到底生成/剔除了多少 motif，**正文未给数字**（在 Supplementary Table 1 与 Supplementary Methods，本地无）。

2. **难点：RFdiffusion 自带的配体辅助势造不出"能埋住底物"的口袋**。
   现象/证据：他们先从 PDBbind 建了个"天然酶埋藏度"基线——"In this dataset, an average of 7.1 α-carbons were within 8 Å of the substrate, normalized by the number of ligand-heavy atoms"；拿这个尺子量 RFdiffusion 的产物，得到的是失败结论："The RFdiffusion substrate auxiliary potential decreased the number of clashes between ligand and backbone but failed to promote the formation of well-defined substrate binding pockets."（即"少 clash"和"能埋底物"之间只是一条 trade-off 曲线）
   **他们做了什么**：换一个结构化的做法——往 motif 的口袋位置插一根 α 螺旋当"进液通道占位螺旋"，再用自定义辅助势把去噪轨迹的 centre 钉在这根螺旋上、并约束所有骨架原子到该中心的距离："To circumvent the trade-off, we implemented a novel approach to enforce pockets during diffusion by adding an α-helix as an entry-channel placeholder to each artificial motif at the position of the binding pocket"、"A custom auxiliary potential then places the centre of the denoising trajectory on the helix and enforces a distance constraint of all backbone atoms to this centre"；扩散完再把这根螺旋删掉留空口袋。
   代价：辅助势的具体实现与权重在 Supplementary Methods（本地无）；正文没给"多少比例的扩散产物因口袋不合格被丢"的数字。

3. **难点：扩散出的骨架与 motif 几何会漂移，序列设计又不认 motif**。
   **他们做了什么**：把"预测结构反过来当下一轮序列设计的输入"做成迭代精修环——LigandMPNN 上序列 → FastRelax 以人工 motif 坐标为约束同时修骨架与活性位点取向 → 精修模型再喂回 LigandMPNN → ESMFold 预测结构 → 高分的进下一轮："Each cycle begins with LigandMPNN 36 threading sequences onto the backbones"、"The highest-scoring designs continue into the next refinement cycle"；之后再用 Rosetta CoupledMoves 精修配体-口袋相互作用（"we utilize the Rosetta CoupledMoves protocol 39 to refine ligand interactions with the binding pocket"）。
   代价：**几轮迭代、每轮留多少条，正文没有给数字**；只说末轮用 AlphaFold2 预测并按"结构质量 + 活性位点定位"的组合指标排序（"In the final evaluation step, these sequences are predicted with AlphaFold2 and ranked with a combination of metrics for structure quality and active site positioning"）。

4. **难点：末轮排序该用哪个判据——他们最后用的是 sidechain RMSD，而且这个判据后来被自己的数据证伪**。
   现象/证据（挑设计依据的原句）："To select designs for experimental testing, we ranked the pool of designed enzymes predominantly by the sidechain RMSD of the catalytic tetrad."，再加一道人工把关："After additional manual inspection, we excluded designs for which the binding pocket appeared inaccessible to the substrate."
   **他们做了什么（事后）**：承认这是错的排序量——"RMSD is a popular metric for measuring how closely a designed active site aligns with the intended catalytic array, but it is agnostic to the geometric constraints of catalytic interactions."、"This could explain the discrepancy between the low RMSD in the active site of RAD13 and low catalytic activity and general poor predictiveness of sidechain RMSD for activity."
   代价：**正文里没有一个数值阈值**（pLDDT/RMSD/Rosetta energy 的分布只在 Supplementary Fig. 1；主文唯一的数值门槛是实验侧的 FoXS χ²<5，见第 3 节 S7）。"口袋对底物是否可达"这一条靠人眼看，不可复现。

5. **难点：motif 摆得"近原子精度"，酶却不干活**——这是本文最硬的一次自我否定。
   现象/证据：RAD13 与 RAD17 的晶体结构里催化残基与模型几乎重合（"The catalytic residues of RAD13 and RAD17 adopted the correct conformation with heavy-atom sidechain RMSD values of 0.42 Å and 1.09 Å to the design model and 0.89 Å and 1.2 Å to the catalytic geometry, respectively"），但"Despite the near-atomic precision with which the tetrad was reproduced, RAD13 and RAD17 were more than 10 5 -fold slower than RA95.5-8F."
   **他们做了什么**：不掩盖，改问"还有什么变量"：① 查构象异质性（RAD36 的催化 Lys 三种密度、RAD32 的 Tyr120 走岔路、MBH2 的 Trp140 翻面把入口撑宽并废掉设计好的 π-π 堆叠）——"In the active site of RAD36, we observed density for three distinct conformations of the catalytic lysine."；② 上 MD 量化柔性——"To evaluate the active site dynamics of our designs relative to RA95.5-8F, we computed 20 replicates of 20 ns apo-state molecular dynamics trajectories and used root mean square fluctuation as a metric to estimate sidechain flexibility"；③ MD 也不灵，就换 AF3 复合物预测造复合指标："Notably, an active site metric derived from these features exhibited a Spearman ρ of -0.64 with measured catalytic rates"、"outperforming apo-state metrics such as sidechain RMSD"。
   代价（关键）：MD 那一层是**阴性结果**——"However, neither of the calculated metrics from the molecular dynamics simulations correlated with activity, suggesting that the difference between designs might be linked to other factors."；AF3 复合指标 ρ=-0.64 是在**同一批 30 多条设计上算的相关性**，作者没有留出独立测试集。

6. **难点：催化阵列需要的不只是一个静态几何，而是"随反应步骤改变的构象系综"，现有工具控不了**。
   现象/证据：BH32.14 阵列里的 Arg 要稳定三个不同位置的负电、必须换 rotamer；他们明写做不到指定这种柔性——"Conversely, for the catalytic array of BH32.14, we could not specify the required flexibility of the catalytic arginine relative to the remaining catalytic residues."
   **他们做了什么**：本文层面只是把它列为开放问题，并把出路指向"显式建模构象动力学的低成本工具"："Replicating the precise control of natural enzymes over the dynamic behaviour of their active sites may hinge on the integration of computationally efficient tools that model conformational dynamics explicitly." ——**本文未解决**。

7. **难点：动力学参数本身会被测法低估（湿实验侧的坑）**。
   现象/证据："Notably, the pH rate profiles of RAD35 and RAD29 revealed that their kinetic parameters were determined below their pH optimum, leading to underestimated kinetic parameters."，而表观 pKa1 落在 7.0–9.0、明显高于原始四元组的 6.2。
   **他们做了什么**：补做 384 孔板 pH 速率曲线（pH 4.6–10.6、0.4 一步）、做 K→A / Y→F 突变体验证四元组真的在参与催化（N110A、Y180F 分别降约 2×、20×）；代价是本文给出的 kcat/KM 是"下限"，与 RA95.5-8F 的对比不能当定量结论用。

8. **难点：新反应没有现成的高活性阵列可拿**。
   现象/证据：他们把高活性归因于"用的是从高效酶里取出的催化阵列"——"For novel reactions, these catalytic arrays will need to be constructed from scratch-a challenge that requires a robust mechanistic understanding of how functional groups confer catalytic effects."
   **他们做了什么 / 代价**：本文只做"given array"这一半，theozyme/阵列从头推导这一步**本文未解决**（这正把我们项目的难点原样留在他们方法的上游）。

## 3. 方法与工作流程（catalytic motif 怎么定义、骨架怎么筛、每步输入→操作→判据/阈值→输出规模）

### 3.0 catalytic motif 到底是怎么"定义"出来的（本文最值得抄的一段）

输入不是序列、不是口袋、不是折叠，而是**一组 sidechain 官能团的空间坐标**（作者称 catalytic array）：

- 体系一（retro-aldol）：来自人工进化酶 RA95.5-8F 的**催化四元组**（PDB: 5AN7），"which catalyses the retro-aldol cleavage of ( R )-methodol ( 1 ) to 6-methoxy-2-naphthaldehyde ( 2 ) and acetone"，选它的理由是"产物 2 可以荧光读、四元组被研究得很透"："The product 2 of the reaction can be screened fluorescently and the tetrad is well-studied, providing a robust framework to assess de novo design performance"。
- 体系二（MBH，非天然反应）：两套**从定向进化产物里抠出来的阵列**——BH32.14（His23 亲核 + Glu46 氢键 + Arg124 稳定三个氧阴离子，"The first is the active site of BH32.14, an enzyme that emerged after 14 rounds of directed evolution 4 ."）与 BH1.8（预测 pKa 8.1 的 Glu26 介导限速质子转移，且亲核体是非天然氨基酸 Nδ-methylhistidine）。

定义步骤（正文原句，逐步）：

| 步骤 | 操作 | 原句依据 |
|---|---|---|
| D1 | 把阵列里**每个氨基酸嵌进一段螺旋片段**，而不是裸 sidechain | "First, each amino acid of the input array is embedded into a helical fragment." |
| D2 | 每个氨基酸的 rotamer 要**与该片段骨架相容**，保证"偏好催化 rotamer"的能量代价最小 | "The rotamers of each amino acid are selected for compatibility with the fragment backbone to ensure a minimal energetic penalty is associated with the preferential catalytic rotamer" |
| D3 | 这些片段的组合就叫 artificial motif | "We call the combination of the individual fragments an artificial motif." |
| D4 | **rotamer 反演**：钉死官能团坐标、让骨架原子去适应它（这正是"motif 优先"的技术含义） | "The script starts by inverting rotamers of the catalytic array, which fixes the functional groups in space and varies the position of their backbone atoms" |
| D5 | 片段组合做**互不位阻穷举**，再按 rotamer 概率 + PDB 丰度排序，存成 motif 库 | "Non-clashing assemblies are ranked according to the rotamer probabilities of the individual active site residues and by their abundance in the Protein Data Bank (PDB)."、"This library is then used as input to RFdiffusion to scaffold enzyme backbones." |

### 3.1 工作流程表（每步：输入 → 操作 → 判据 / 阈值 → 输出与规模）

| # | 输入 | 操作 | 判据 / 阈值（**必须是原文数字，没有就写明**） | 输出与规模 |
|---|---|---|---|---|
| S1 | 给定催化阵列（四元组 / BH32.14 / BH1.8 三套） | D1–D5：螺旋片段化 + rotamer 反演 + 非位阻穷举 + 排序 → artificial motif library | 判据＝片段相容性 + 无位阻 + rotamer 概率 + PDB 丰度；**原文未给数值阈值** | motif 库；RAD 线最终只用到 **8 个 unique artificial motifs**（库内生成/淘汰总数正文未给） |
| S2 | 库中挑出的 motif + 底物坐标 | RFdiffusion 从头扩散骨架 | "The RFdiffusion substrate auxiliary potential decreased the number of clashes between ligand and backbone but failed to promote the formation of well-defined substrate binding pockets." ⇒ 默认辅助势**不够**，被弃用 | 扩散骨架（正文未给扩散条数） |
| S3 | motif + 通道占位螺旋 | 加一根 α 螺旋作 entry-channel placeholder，自定义辅助势把去噪轨迹中心钉在螺旋上并约束所有骨架原子到该中心距离；扩散后删螺旋 | 目标口径＝复现天然酶埋藏度：**平均 7.1 个 α-carbons 在底物 8 Å 内**（按配体重原子数归一，PDBbind 统计）；"A custom auxiliary potential then places the centre of the denoising trajectory on the helix and enforces a distance constraint of all backbone atoms to this centre" | 带空口袋的骨架（正文未给通过条数） |
| S4 | 骨架 + motif 坐标 | 迭代精修环：LigandMPNN 上序列 → FastRelax（以 motif 坐标为约束修骨架与活性位点）→ 回喂 LigandMPNN → ESMFold 预测 → 高分进下一轮 | "The highest-scoring designs continue into the next refinement cycle."；**分数定义与轮数、每轮留存量正文未给（在 Supplementary Methods）** | 精修后的骨架-序列对；RAD 线 **12 个 unique backbones** |
| S5 | 精修骨架 | Rosetta CoupledMoves 精修配体-口袋作用（或改用 LigandMPNN 出终序列） | "we utilize the Rosetta CoupledMoves protocol 39 to refine ligand interactions with the binding pocket."；无阈值 | 候选序列池（正文未给池规模） |
| S6 | 候选序列池 | **末轮评估**：AlphaFold2 单序列预测，按"结构质量 + 活性位点定位"组合指标排序；再主要按**催化四元组 sidechain RMSD** 排名；最后人工检查剔除"口袋对底物不可达"的 | "In the final evaluation step, these sequences are predicted with AlphaFold2 and ranked with a combination of metrics for structure quality and active site positioning."、"To select designs for experimental testing, we ranked the pool of designed enzymes predominantly by the sidechain RMSD of the catalytic tetrad."、"After additional manual inspection, we excluded designs for which the binding pocket appeared inaccessible to the substrate." ⇒ **RMSD 无 cutoff，原文未给阈值**；pLDDT/RMSD/Rosetta energy 分布见 Supplementary Fig. 1（本地无） | **RAD：36 条序列（12 骨架 / 8 motif）**；**MBH：18 条（BH32.14，14 骨架）+ 45 条（BH1.8，23 骨架）= 63 条** |
| S7 | 36 / 63 条设计序列 | 先证"新"：FoldSeek 对 PDB、BLAST 对非冗余序列库 | "The backbones adopted novel folds, having an average maximum TM-score of 0.49 when searched with FoldSeek 42 against the PDB." ⇒ 平均最大 TM-score **0.49**（作者报告的量，**不是 cutoff**）；"no similar sequences could be found for any of the 36 sequences" | 36 条全为新 fold/新序列 |
| S8 | 合成基因（IDT / GenScript） | Golden Gate 入 His-tag + TEV 载体 → E. coli BL21(DE3) STAR → 96 孔培养 + 24 孔自诱导（**每样 2 个重复**）→ Ni-NTA 磁珠 96 孔板纯化（OT-2 移液机器人）→ Bradford + SDS-PAGE | 判据：可溶表达；有正/负/无菌对照 | "The set of 36 designed retro-aldolases was ordered as synthetic genes, of which 35 could be cloned." ⇒ **36 下单 → 35 克隆成功** |
| S9 | 35 条粗提 | 初筛活性：跟着产物 2 的荧光（Ex 330 / Em 452 nm），29 °C、pH 7.4、200 µl、96 孔 | 判据＝高于 negative control；**未给数值 cutoff** | "all 35 designs expressed soluble and 32 (91%) designs exhibited activity towards racemic methodol ( rac -methodol) above the negative control." ⇒ **可溶 35/35，有活性 32/35 = 91%** |
| S10 | 35 条纯化酶 | 折叠性三件套：SEC + intact MS + CD；再加 SAXS（Kratky 图、Rg、FoXS 拟合 χ²） | 折叠判据（原文唯一硬阈值）："Twenty-nine out of 35 designed retro-aldolases were correctly folded according to SAXS (FoXS χ 2 <5)." ⇒ **FoXS χ² < 5** | **29/35 判为正确折叠**；SEC 全部单分散、CD 全部 α 螺旋 |
| S11 | 32 条有活性者 | 稳态动力学：8 个 1:1 稀释系列，rac-methodol 1 mM → 0.0078 mM，SciPy 拟合 kcat/KM | 判据（分析线，非筛选线）："Seven designs exhibited k cat > 10 -3 s -1 (yellow bar)." ⇒ **kcat > 10⁻³ s⁻¹** | **30/35 拿到 Michaelis–Menten 参数**；**7 条跨过 10⁻³ s⁻¹**；另有 "For 22 designs, the catalytic rate (<10 -3 s -1 ) falls within the range achievable by an isolated lysine in a hydrophobic pocket"（即 22 条≈只有一个 Lys 在干活） |
| S12 | 命中者 | 机理归因：位点定向突变（K→A、N→A、Y→F）+ pH 速率曲线（pH 4.6–10.6，0.4 一步，双 pKa 拟合）+ 立体选择性（手性 HPLC）+ turnover | 以"突变后活性下降倍数"为判据；**无 cutoff** | 20 个设计有 GdnHCl 变性中点（2.5–>6.5 M）；RAD29/RAD35 kcat 3.1–3.6×10⁻² s⁻¹；turnover 1,000 / 895；E-value 4 / >200 |
| S13 | MBH 63 条 | 终点法筛选：**酶 100 µM**、2-cyclohexenone 25 mM + 4-nitrobenzaldehyde 5 mM、40 °C、8 h、HPLC；背景对照用溶菌酶 | 判据＝产物高于 background（lysozyme 线）并超过 imidazole / DMAP 小分子催化剂 | "Endpoint assays showed that 17 of the designs based on BH32.14 (94%) and 42 of the designs based on BH1.8 (93.3%) displayed product formation above background level" ⇒ **17/18 = 94%、42/45 = 93.3%** |
| S14 | MBH 高转化者 | 动力学：MBH48（60 µM 酶）/MBH18（90 µM 酶）对两个底物分别滴定 | 无 cutoff | MBH18 kcat 7.7×10⁻³ min⁻¹（≈BH32 的 3.5 倍）；MBH48 kcat 0.025 min⁻¹（≈BH32.8 的 1.5 倍，BH32.8 是筛了 13,590 克隆/8 轮进化得来的），但比 BH1.8 23H 低 45 倍 |
| S15 | 4 个 RAD + 2 个 MBH 设计 | 晶体结构解析（1.13 Å 等，PDB 9GBT/9FW5/9FW7/9FWA/9QDP/9R7F）与模型比对 | 判据＝Cα/sidechain RMSD（**事后验证，不是筛选闸口**） | 骨架 Cα RMSD 0.68–1.2 Å；MBH2 0.53 Å、MBH48 0.78 Å；RAD13 sidechain 0.42 Å 却慢 10⁵ 倍 |
| S16 |  apo 结构 | **MD 系综**：GROMACS 2023.4 / amber99sb-ildn / SPC-E / 150 mM NaCl，1.0 nm 盒边距，先 50 ns 确认平衡，再 **20 条 20 ns 重复** apo 轨迹；RMSF + 氢键距离偏差 + 叠合后官能团距离偏差 | 判据＝这些指标能否与活性相关 ⇒ **失败**："However, neither of the calculated metrics from the molecular dynamics simulations correlated with activity, suggesting that the difference between designs might be linked to other factors." | 观测到"五个设计的催化 Lys 漂出活性位点"："In five designs, the catalytic lysine even drifted from the active site into a non-catalytic state." |
| S17 | 设计模型 + 底物/中间体 | **AlphaFold3 复合物建模**：预测与 (R)-methodol 的复合物、以及共价连在 Lys 上的半胺醛中间体；造复合指标（四元组到中间体羟基的作用距离 + 底物羰基定位） | 与实测 kcat 比较；k_uncat 取 "A value of 3.9 × 10 -7 min -1 was used for k uncat (uncatalysed rate constant) 22 ." | "Notably, an active site metric derived from these features exhibited a Spearman ρ of -0.64 with measured catalytic rates"、"outperforming apo-state metrics such as sidechain RMSD"（同一批设计上的相关性，无独立留出集） |

**送测数与命中率总账（这是这篇对我们最有用的两个数）**：下单 99 条序列（36 RAD + 63 MBH），**正文自述口径**："The designed enzymes exceed the activities achieved by previous design campaigns and rival those subjected to several rounds of directed evolution 4 , 22 , 31 , while screening as few as 35 sequences in one instance and fewer than 100 overall." 即"单次最少 35 条、全部不到 100 条"。命中口径分三级：**有活性**（32/35 = 91%、17/18 = 94%、42/45 = 93.3%）→ **真的用了整个 motif**（22 条落回"孤立 Lys"水平 ⇒ 只有 7 条超出）→ **高活性**（RAD29/RAD35，MBH48/MBH18）。

## 4. 关键数字台账（数值 · 含义 · 出处）

| 数值 | 含义 | 出处（本地全文里的原句片段 / 位置） |
|---|---|---|
| 8 · 12 · 36 | retro-aldol 线：unique artificial motifs → unique backbones → 送测序列（RAD1–36） | "The final selection consisted of 36 sequences derived from 12 unique backbones generated from 8 unique artificial motifs, named RAD1-36" |
| 18（14 骨架）+ 45（23 骨架）= 63 | MBH 线两个阵列各自的送测序列与骨架数 | "selected 18 sequences (MBH1-18) derived from 14 unique backbones based on the active site array of BH32.14"、"45 sequences (MBH19-63, 23 unique backbones) based on the active site of BH1.8" |
| 36 → 35 | 下单合成基因 → 克隆成功 | "The set of 36 designed retro-aldolases was ordered as synthetic genes, of which 35 could be cloned." |
| 35/35 可溶 | 初筛表达 | "all 35 designs expressed soluble" |
| 32（91%） | 初筛活性高于 negative control | "32 (91%) designs exhibited activity towards racemic methodol ( rac -methodol) above the negative control." |
| 29/35，**FoXS χ² < 5** | SAXS 判为正确折叠（**正文唯一的数值阈值**） | "Twenty-nine out of 35 designed retro-aldolases were correctly folded according to SAXS (FoXS χ 2 <5)." |
| 30/35 | 拿到 Michaelis–Menten 参数的设计数 | "Next, we determined Michaelis-Menten parameters for 30 of the 35 produced retro-aldolases" |
| 7，**kcat > 10⁻³ s⁻¹** | 跨过"活性明显高于孤立 Lys 水平"的设计数 | "Seven designs exhibited k cat > 10 -3 s -1 (yellow bar)." |
| 22（< 10⁻³ s⁻¹） | 速率落在"疏水口袋里一个孤立赖氨酸"区间内 ⇒ 四元组没协同起来 | "For 22 designs, the catalytic rate (<10 -3 s -1 ) falls within the range achievable by an isolated lysine in a hydrophobic pocket" |
| RAD35 3.6×10⁻² s⁻¹ / RAD29 3.1×10⁻² s⁻¹ | 最高 kcat | "They catalysed the cleavage of rac- methodol with k cat (catalytic rate constant) values of 3.6 × 10 -2 s -1 and 3.1 × 10 -2 s -1 , respectively" |
| ~5×10⁶ 倍 | 相对非催化反应的速率加速 | "a roughly 5 × 10 6 -fold rate acceleration over the uncatalysed reaction." |
| KM ≈ 100 µM、290 M⁻¹s⁻¹（vs RA95.5-5 320 M⁻¹s⁻¹） | RAD29 的亲和力与催化效率 | "With a Michaelis constant ( K m ) of around 100 µM, its catalytic efficiency of 290 M -1 s -1 approaches that of the extensively evolved RA95.5-5" |
| 1.1×10⁻² s⁻¹ | 被超过的参照：催化抗体 38C2 | "surpassing, for example, the activity of the evolved catalytic antibody 38C2 (refs. 44 , 45 ) ( k cat = 1.1 × 10 −2  s −1 )"（正文原样，减号为 U+2212） |
| 全部可测设计 >90 °C 仍折叠（仅 RAD23 例外）；20/33 的 GdnHCl 中点 2.5 → >6.5 M | 热/化学稳定性 | "CD melting curves confirmed that all but one of the designed retro-aldolases remained folded above 90 °C"、"Twenty out of 33 enzymes displayed cooperative unfolding with midpoints of denaturation ranging from 2.5 M to more than 6.5 M GdnHCl" |
| Pearson's R = 0.8（P < 0.05 相关） | 用计算指标（AF2 平均 pLDDT、Rosetta total score、core atomic density、SAP）线性回归预测化学变性中点 | "Using these metrics, we built a simple linear regression model that predicted chemical denaturation midpoints with a Pearson's R of 0.8" |
| 1,000 / 895 turnovers（48 h） | RAD29 / RAD35 的周转数 | "Determination of the turnover number of RAD29 and RAD35 resulted in 1,000 and 895 turnovers after reacting for 48 h in the retro-aldol direction" |
| E-value 4（60% ee）/ >200（99% ee） | RAD29 / RAD35 的立体选择性 | "Whereas RAD29 was modestly stereoselective with an E-value of 4 towards the formation of ( R )-methodol (60% enantiomeric excess), RAD35 displayed exquisite ( R )-stereoselectivity and an E-value of over 200 towards ( R )-methodol (99% enantiomeric excess" |
| 70% / 47.5% 转化；余 (S)-1 的 ee 77% / 88% | 动力学拆分实测 | "Under optimized reaction conditions, RAD29 and RAD35 converted 70% and 47.5% of the racemic substrate" |
| 平均最大 TM-score 0.49（FoldSeek）；BLAST 无相似序列 | 骨架与序列的全新性（报告值，非 cutoff） | "having an average maximum TM-score of 0.49 when searched with FoldSeek 42 against the PDB." |
| 骨架 Cα RMSD 0.68–1.2 Å；RAD13 sidechain 0.42 Å、RAD17 1.09 Å（对模型）；0.89 Å / 1.2 Å（对催化几何） | 晶体结构与设计的吻合度（**高精度却不快**） | "The crystal structures agree with the design models, having backbone C α RMSD values between 0.68 Å and 1.2 Å"、"The catalytic residues of RAD13 and RAD17 adopted the correct conformation with heavy-atom sidechain RMSD values of 0.42 Å and 1.09 Å to the design model and 0.89 Å and 1.2 Å to the catalytic geometry, respectively" |
| RAD13 3.8×10⁻⁵ s⁻¹、RAD32 1.1×10⁻² s⁻¹、RAD36 6.2×10⁻⁵ s⁻¹；RAD17 kcat 未测；比 RA95.5-8F 慢 >10⁵ 倍 | 四个结晶设计的活性跨度（同 motif、不同骨架） | "We obtained crystal structures of the four designs: RAD13 ( k cat = 3.8 × 10 −5 s −1 ), RAD17 ( k cat not determined), RAD32 ( k cat = 1.1 × 10 −2 s −1 ), and RAD36 ( k cat = 6.2 × 10 −5 s −1 )"、"RAD13 and RAD17 were more than 10 5 -fold slower than RA95.5-8F" |
| 20 × 20 ns apo 重复轨迹（另有前置 50 ns 平衡确认）；GROMACS 2023.4、amber99sb-ildn、SPC/E、150 mM NaCl、1.0 nm 盒边距；MDAnalysis 2.8.0 | MD 的规模与设置（**事后机理分析，未进筛选闸口**） | "Molecular dynamics simulations were performed using GROMACS 65 version 2023.4."、"we computed 20 replicates of 20 ns apo-state molecular dynamics trajectories and used root mean square fluctuation as a metric to estimate sidechain flexibility"、"Prior to the 20 ns replicate simulations, individual 50 ns simulations were run to confirm proper equilibration." |
| MD 指标与活性：**无相关**（作者明说） | MD 作为活性判据的失败结果 | "However, neither of the calculated metrics from the molecular dynamics simulations correlated with activity" |
| 5 个设计：催化 Lys 漂出活性位点 | 柔性导致失活的直接观测 | "In five designs, the catalytic lysine even drifted from the active site into a non-catalytic state." |
| Spearman ρ = −0.64（AF3 复合指标 vs 实测 kcat）；k_uncat 取 3.9×10⁻⁷ min⁻¹ | 目前他们手上最强的活性预测量（同一批设计的相关，非独立验证） | "Notably, an active site metric derived from these features exhibited a Spearman ρ of -0.64 with measured catalytic rates"、"A value of 3.9 × 10 -7 min -1 was used for k uncat (uncatalysed rate constant) 22 ." |
| 17/18（94%）、42/45（93.3%） | MBH 两组设计高于 background 的比例 | "Endpoint assays showed that 17 of the designs based on BH32.14 (94%) and 42 of the designs based on BH1.8 (93.3%) displayed product formation above background level" |
| MBH18 7.7×10⁻³ min⁻¹（≈BH32 的 3.5×）；MBH48 0.025 min⁻¹（=1.5× BH32.8；仍比 BH1.8 23H 低 45×） | MBH 线的最好活性与对照 | "MBH18 displays a k cat of 7.7 × 10 -3 min -1 , making it around 3.5-fold more active than BH32 ( k cat of 2.2 × 10 -3 min -1 ), the computationally designed starting point for directed evolution."、"With a k cat of 0.025 min -1 , MBH48 activity is 1.5 times higher than in BH32.8 ( k cat of 0.0168 min -1 ), a variant that emerged after screening 13,590 clones in 8 rounds of directed evolution"、"However, it remains 45-fold less active than BH1.8 23H ( k cat of 1.13 min -1 )" |
| 13,590 克隆 / 8 轮；BH32.14 = 14 轮 | 被"99 条送测"击败的定向进化通量 | "a variant that emerged after screening 13,590 clones in 8 rounds of directed evolution"、"an enzyme that emerged after 14 rounds of directed evolution 4" |
| MBH2 0.53 Å（1.13 Å 分辨率）、MBH48 0.78 Å / sidechain 1.07 Å；Trp140 翻面（除 Trp140 外 sidechain 0.54 Å）、Arg92 双构象 | 结构验证与 MBH 的失败样本 | "Experimental structure determination resulted in a 1.13 Å resolution crystal structure for MBH2, one of the designs displaying the lowest conversion."、"The catalytic sidechains superimpose well with the catalytic geometry except for Trp140, which adopts a flipped conformation (sidechain RMSD 0.54 Å excluding Trp140"、"the desired catalytic geometry was reproduced with a sidechain RMSD of 1.07 Å" |
| 表观 pKa1 7.0–9.0（原始四元组 6.2） | 微环境把 Lys pKa 推高 ⇒ 测得动力学偏低 | "We determined the pH rate dependency for several RAD designs and found a range of apparent p K a 1 values between 7.0 and 9.0"、"Notably, the pH rate profiles of RAD35 and RAD29 revealed that their kinetic parameters were determined below their pH optimum, leading to underestimated kinetic parameters." |
| 7.1 个 α-carbons / 8 Å | 天然酶底物埋藏度基线（口袋设计的靶口径） | "In this dataset, an average of 7.1 α-carbons were within 8 Å of the substrate, normalized by the number of ligand-heavy atoms." |
| 35 条 / <100 条 | 作者自报的总送测量级 | "while screening as few as 35 sequences in one instance and fewer than 100 overall." |
| **无** | 本文**没有**给出：GPU/CPU 机时、每条设计的生成成本、motif 库规模、扩散采样条数、各轮淘汰率 | 正文与 Methods 全文未出现相关数字（算力成本、通过率漏斗比例均未记录） |

## 5. 结论——作者说了什么

1. **方法主张**：给定一套催化阵列，Riff-Diff 能 one-shot 造出两类反应（retro-aldol、MBH）的酶——"In one shot, Riff-Diff designed enzymes to catalyse (retro-)aldol and MBH reactions starting from catalytic arrays as inputs."，且"我们的设计超过以往设计campaign的活性、可与跑过多轮定向进化的变体匹敌"：见 "while screening as few as 35 sequences in one instance and fewer than 100 overall."
2. **免掉了"设计—实验"迭代**："The ability of Riff-Diff to design enzymes without experiment-design cycles constitutes a significant advance towards minimizing laborious high-throughput screens."
3. **结构精度**："High-resolution structures of six of the designs revealed near-atomic active site design precision."，并且稳定性符合 de novo 骨架的常规水平："Our study demonstrated that Riff-Diff can design enantioselective enzymes with thermal stabilities of typical de novo scaffolds."
4. **普适性主张（有条件的）**："The design strategy can, in principle, be applied to any catalytically competent amino acid array."——注意这句的前提是"催化阵列本身已经 competent"，作者在末段亲口承认这个前提是新反应的瓶颈："For novel reactions, these catalytic arrays will need to be constructed from scratch-a challenge that requires a robust mechanistic understanding of how functional groups confer catalytic effects."
5. **作者自己给出的最重要负面结论**（三条，都是他们写进 Discussion 的）：
   - 活性预测仍未解决："A critical challenge that remains in one-shot enzyme design is the accurate prediction of enzymatic activity before experimentation."、"This was highlighted by the negligible correlation between predicted enzyme rankings and actual activity in this and previous studies"
   - 静态几何判据（RMSD）本身有问题："One is the use of metrics for structural similarity, such as RMSD, to rank and optimize designed enzymes."、"RMSD is a popular metric for measuring how closely a designed active site aligns with the intended catalytic array, but it is agnostic to the geometric constraints of catalytic interactions."
   - motif 摆准 ≠ 有活性："This indicates that precise positioning of catalytic sidechains is by itself not sufficient to design efficient biocatalysts, even when scaffolding catalytic arrays that are derived from highly active enzymes."
   - 外加两条"本文未解决"：柔性无法被指定（"Conversely, for the catalytic array of BH32.14, we could not specify the required flexibility of the catalytic arginine relative to the remaining catalytic residues."）、MD 指标与活性不相关（"However, neither of the calculated metrics from the molecular dynamics simulations correlated with activity, suggesting that the difference between designs might be linked to other factors."）。
6. **他们把这套数据定位成"考卷"而非"终点"**："The datasets generated in this study enabled us to detail reasons for higher and lower catalytic proficiencies and are an ideal test set to benchmark models of catalytic activity."
7. 高活性的来源他们归给一件事——用的是**从高效酶里取出的阵列**："an essential factor that contributed to the high activity of our enzymes was the use of catalytic arrays extracted from efficient enzymes."

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

以下为推断。

1. **"motif 优先"确实把送测数压了两个数量级**（99 条 vs 定向进化的 13,590 克隆），但它压的是**骨架搜索空间**，不是**化学判据空间**：命中率 91–94% 的"有活性"里，只有 7/35 真正超出"孤立赖氨酸"的水平。也就是说 motif scaffolding 解决的是"摆得准"，**没解决"摆准了就快"**。对我们："先定理想活性位点再找骨架"这一半是可借的；借来的那半不能承诺高命中率。
2. **"有活性"这个口径在他们那里也是软的**：32/35 = 91% 说的是高于 negative control，而 22 条的 kcat 落回"一个 Lys 自己就能做到"的区间。→ 我们的漏斗必须把"检出产物"与"指定 motif 真的参与"分成两级标签（对应分步化学事件归因），否则 91% 这种数字会被当成成功概率误读。
3. **他们试过 MD、并且 MD 判据输了**：20×20 ns apo 轨迹的 RMSF 与距离偏差**与活性不相关**；赢的是 **AF3 复合物/中间体几何**（ρ=−0.64）。这提示：对"沿反应坐标排布官能团"这件事，**含底物/中间体的复合态建模**比 apo 系综统计更能提前区分——但 ρ=−0.64 是在**同一批设计里算的相关**，没有留出集，我们不能把它当已验证的预测力，只能当"值得在我们体系里做独立验证的候选判据"。
4. **他们没算成本**：全文没有机时/GPU、没有 motif 库规模、没有各轮淘汰率。所以"one-shot 省掉了高通量筛选"省的是**湿实验通量**，计算侧代价不明——我们不能据此声称 motif scaffolding 在算力上便宜。
5. **可迁移性最强的其实是一句自陈的失败**：RAD13 侧链 RMSD 0.42 Å 却慢 10⁵ 倍。这条对我们最有价值，因为它把"结构自洽性 = 功能"的等式在**酶**（不是 binder）上打断了——和 B09 那篇 binder 论文里"pAE 高≠界面成"是同一类 Type II 问题，但这里是 Type II 的化学版：几何全对、动态与质子化不对。
6. **作者的"给定阵列"前提，恰是我们的缺口**：他们不需要设计 motif，我们要（UTP 磷酸化起始 / 中间体 / 竞争副产物这些事件该由哪些官能团、什么几何来承担）。所以这篇的结论对我们**不构成成功概率证据**，只构成"motif 一旦定错，后面全白跑"的风险证据。

## 7. 局限与失败（作者自述的失败模式 + 我们读出的）

**作者自陈（可直接引原文）**

1. 活性不能在实验前预测："A critical challenge that remains in one-shot enzyme design is the accurate prediction of enzymatic activity before experimentation."；排序用的 RMSD 类指标对催化相互作用"不可知"："RMSD is a popular metric for measuring how closely a designed active site aligns with the intended catalytic array, but it is agnostic to the geometric constraints of catalytic interactions."
2. apo 态复现不出来活性："Such precision might explain the high catalytic activity, however, our results show that high activity cannot be inferred from precise reproduction of the apo-state alone."
3. MD 判据全军覆没（作者写成一句话就带过）："However, neither of the calculated metrics from the molecular dynamics simulations correlated with activity"。
4. 柔性无法设计：见第 5.5 条 BH32.14 的 Arg；他们的结构性结论也只有两个 MBH 晶体支撑："Gaining a deeper understanding of the rate enhancement of the MBH reaction will require more than the two crystal structures presented here."
5. 阵列来源受限：本文全部用"已知高效酶的阵列"，新反应要自己造阵列（第 5.4 条）。
6. 测量本身的偏差：pH 最优之下的问题导致 kcat、KM 被低估（"leading to underestimated kinetic parameters"）；RAD17 的 kcat 干脆没测出来（"RAD17 ( k cat not determined)"）。
7. 副反应未被消除：MBH18 有明显竞争 aldol 副产物（"A considerable amount of side product formation-a competing aldol reaction product according to similar previously reported high-performance liquid chromatography retention times"）；也就是说他们只证明了"生成产物"，没证明"化学/区域选择性达意"。

**我们读出的（推断）**

- **送测数太小，命中率的分母经不起复算**：36 下单 / 35 克隆 / 7 高活性；MBH 63 条里只有 2 条做了动力学。"94%/93.3%" 这类数字是**有产物**的口径，不是"有用酶"的口径。
- **计算漏斗的关键比例根本没披露**：motif 库多大、扩散多少条、每轮精修留多少、最终从多少条里挑 36——正文全无（在 Supplementary，本地无）。所以这篇**只能借协议结构，不能借漏斗通过率**。
- **AF3 复合指标 ρ=−0.64 无独立验证集**，且 k_uncat 是文献常数 3.9×10⁻⁷ min⁻¹，指标里含一个外部假设值。
- **人工把关进了漏斗**（"we excluded designs for which the binding pocket appeared inaccessible to the substrate"），意味着这条管线**不是全自动可复现**，"Riff-Diff requires only minimal user input to generate sequences that scaffold a given catalytic array." 这句自述与 S6 步的人工判断存在张力。
- **没有第二家复现**：本文是自报结果，无同行独立复算；我们引用时只引用方法结构与失败分型，不引用命中率做校准。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **"motif 先定、骨架后找"的完整工程实现**：把催化基团坐标当不可动约束、用 rotamer 反演把它变物理可行（第 3.0 节 D1–D5），再用占位螺旋强制成口袋（S3）。→ 我们若为酶设计相关反应定下理想活性位点（例如稳定中间体 / 第二枚 ATP 的磷酸负电荷的胍基+His 排布），可以直接按 D1–D5 生成 motif 库、按 S2–S6 长骨架；这条路径与我们"催化基团排布优先"的思路同构。
2. **"埋藏度基线"这种做法要抄**：他们先用 PDBbind 统计出天然酶的平均埋藏度（7.1 个 α-carbons / 8 Å），把它变成口袋设计的靶口径，再据此发现 RFdiffusion 默认辅助势的不足。→ 对应我们：给"底物/中间体被埋住的程度"定一个来自已知酶的可复算基线，作为口袋合格性的**定义性**判据，而不是拍脑袋。
3. **失败归因的分层口径**：可溶（35/35）→ 折叠（29/35，FoXS χ²<5）→ 有产物（32/35）→ motif 真参与（仅 7/35 超孤立 Lys 水平）→ 高活性（2 条）。→ 我们的漏斗也应做这种**同一批候选上的多级标签**，其中"motif 真参与"这一级必须靠突变体失活（K→A 等）来定，我们项目里的等价物就是"催化残基点突变后产物信号消失"。
4. **"含底物/中间体的复合态建模"优先于 apo 几何**：他们唯一与活性相关的计算量是 AF3 复合物导出的复合指标。→ 我们的判据应围绕"共价中间体/过渡态几何"来建，而不是 apo 结构的 pLDDT/RMSD；MD 可留作机理叙述，但按他们的实测，**apo 系综指标当筛子是被证伪过的**。
5. **把负面结果写进论文的做法**：他们把"MD 不相关""RMSD 不可靠"直接写进 Discussion 并给出反例（RAD13）。→ 我们的 run.md / 卡片也应把阴性判据登记为"已排除项"，避免后续重复投入（本项目已有 MD 156.6 ns/day、10.6 GPU·h/体系、xTB 153.3 s/评价的实测单价，可直接用"单价 ÷ 通过率"决定是否继续把 MD 当筛子）。

**不可迁移（为什么不能照搬）**

1. **他们的 91%/94% 命中率不能当成我们的成功概率**。那批阵列取自被 14 轮进化打磨过的酶，反应（retro-aldol、MBH）有荧光/HPLC 可读、底物毫克级可得；我们面对的是"至今没有任何一条被产物化学确认的天然参照酶"，**连真值面板都没有**。引用时只许引用方法结构，不许引用数字。
2. **他们的"阈值"对我们没有约束力**：FoXS χ²<5 是**折叠性 QC**、kcat>10⁻³ s⁻¹ 是**事后分析线**，两者都不是设计阶段的活性判据；原文的计算排序（sidechain RMSD）连 cutoff 都没给。→ 不许把这两个数字搬进我们的漏斗当阈值，也不许把"TM-score 0.49"当新颖性阈值（那是报告值不是 cutoff）。
3. **反应机理不同层**：retro-aldol 靠 Lys 共价催化 + 氢键网络，是**单共价中间体**；酶设计相关要处理分步化学事件多步磷酸转移与环化竞争，涉及多价阴离子与质子转移顺序，"埋藏度 + 一个共价中间体几何"这套复合指标不足以覆盖。他们的 ρ=−0.64 只在一维活性上成立，我们目标是**多事件归属**，不是单一 kcat 排序。
4. **非天然氨基酸依赖**：BH1.8 阵列的核心亲核体是 Nδ-methylhistidine（非天然氨基酸），他们用普通 His 替换后的对照 BH1.8 23H 才作为比较基准，且新设计仍差 45 倍。→ 提醒我们：**若 motif 本身含非天然残基或特殊质子化态，motif scaffolding 会整体降级**，这正是我们体系里 ATP/UTP 结合位点电荷态的类比风险。
5. **本文不含 QM**，所以它**不能**为"用 QM/自由能判催化步"提供任何命中率背书（正文与 Methods 只有 MD，QM 仅出现在参考文献里）；那类主张需另找参照（本项目里可参照 Listov/Fleishman 2025 一类含 QM 的外部对照，非本卡范围）。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/motifscaffold2026.txt

- **本卡实际照着写的那一份**：`data/interim/baker_lit/ft/motifscaffold2026.txt`（Europe PMC `fullTextXML`（PMC12727513）去标签纯文本，82,645 字符）。本卡所有英文引号片段都是从这一份里复制的连续文本，**逐字比对只针对这一份**；同一论文的其它抽取版本（若存在）在句子中间夹的参考文献编号可能不同，本卡不与之比对。
- 归一化口径与门禁一致：`scripts/litcards_text.py` 的 `norm()`（实体解码、弯引号/破折号/减号 U+2212 统一、`ɑ→a`、空白折叠），本卡引号内的 `χ 2 <5`、`10 -3 s -1`、`C α RMSD`、`π-π-stacking` 等写法即为该函数处理后的原样。
- 对照底稿：`sources/baker.md:593`（该行为本篇在 Baker 侧调研里的唯一一条登记，标题/DOI/PMID/PMCID 与本地全文一致；**其作者归属记为 Hilvert D（ETH Zürich），与本地全文作者表（末位 Oberdorfer G，Graz University of Technology）不符**，本卡按全文实况写，未改动 `sources/*.md`）。`sources/cost-benchmarks.md` 里**未检索到本篇条目**（grep 关键词 K64 / Braun / Oberdorfer / motif scaffolding 均无本篇命中），故该登记底稿对本卡无补充信息。
- CSV 现值与全文不符之处（已核验，本卡未改 CSV，供回填时人工决断）：① `第一或通讯作者` 记为 Hilvert → 应为 Braun M / Tripp A（共同一作）与通讯 Oberdorfer G（Graz TU）；② `是否用QM=是-化学步` → 正文与 Methods 无 QM/DFT，QM 仅见于参考文献 41（De Raffele 等的 QM/MM 研究），应记为否；③ `阈值数字=未记录`、`候选数递减=未记录`、`实验命中率=未记录`、`Kd或活性最好值=未记录` → 全文均可补齐，本卡第 3、4 节已给出。
- 字段映射：本卡第 3 节 ↔ CSV `候选生成方法 / 计算筛选判据 / 阈值数字`；第 4 节 ↔ `候选数递减 / 实验命中率 / Kd或活性最好值 / 成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- 未取到因而**没有**写成结论的部分：Supplementary Methods（辅助势实现、MBH 设计协议）、Supplementary Fig. 1（AF2 pLDDT / active site RMSD / Rosetta energy 分布，即"计算筛子到底用在哪一档"的原始数字）、Supplementary Figs. 2/5/7/12（逐条设计转化率与动力学的图）、Supplementary Tables 1/4/6/7/8（序列与参数全表）、Extended Data Table 1（晶体学条件）、Fig 1c 流程原图。凡涉及"库规模 / 各轮淘汰数 / 成本"的问题，本卡一律写"原文未给"，未做外推。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K64" --no-report` 判 `PASS K64 quotes=<见交付回报>`，退出码 0。门禁逐条校验：十节齐全且顺序正确、§3 工作流程表 ≥3 步、§2 难点 ≥2 条、每条引号内纯英文片段在该编号登记底稿里逐字命中、证据级别与全文可得性一致。写卡过程中本地预检曾抓到 2 条 MISS（一处把中文术语误写成英文引号片段 binding pocket accessible、一处把句首 We 抄成小写 we），已改正后复跑。
- **本篇最可疑的一条判据/结论（人读复核点）**：他们用 sidechain RMSD 作为挑设计的主判据（第 3 节 S6），而自己的晶体数据（RAD13 0.42 Å 却慢 10⁵ 倍）证明该判据与活性无关；文中并未因此停用该判据，只在 Discussion 承认为局限——**"排序判据已知失效仍继续用"** 是本卡最需要人工复核的方法学问题。

<!--CSV回填
work_type=论文
target=催化 motif（catalytic array）支架化的 de novo 酶设计：retro-aldol 四元组（RA95.5-8F，PDB 5AN7）与 MBH 反应（BH32.14、BH1.8 两套进化活性位点，非天然反应）
backbone_generation=Riff-Diff：每个催化残基嵌入螺旋片段并选骨架相容 rotamer → rotamer 反演固定官能团坐标 + 非位阻片段组合穷举并按 rotamer 概率与 PDB 丰度排序成 artificial motif 库 → RFdiffusion 扩散骨架（配 entry-channel 占位 α 螺旋 + 自定义辅助势约束骨架原子到螺旋中心的距离，扩散后删螺旋留口袋）→ LigandMPNN/FastRelax/ESMFold 迭代精修（以 motif 坐标为约束）→ Rosetta CoupledMoves 精修配体作用或 LigandMPNN 出终序列
computational_filters=末轮 AlphaFold2 单序列预测 + 结构质量与活性位点定位组合指标（pLDDT、active site RMSD、Rosetta energy，分布仅在 Supplementary Fig. 1）；主排序判据＝催化四元组 sidechain RMSD；人工检查剔除口袋对底物不可达者；新颖性核查 FoldSeek 对 PDB 与 protein-protein BLAST；事后判据＝AF3 酶-底物/半胺醛中间体复合物导出的复合活性位点指标、apo 态 MD 的 RMSF 与氢键/官能团距离偏差（后者与活性无相关）、以及用于稳定性回归的 pLDDT/Rosetta total score/core atomic density/SAP
thresholds=正文唯一数值阈值是实验侧折叠判据 FoXS χ2<5（29/35 判为正确折叠）；活性分析线 kcat>10-3 s-1（7 条跨过，22 条落在孤立 Lys 区间）；计算排序（sidechain RMSD、pLDDT、Rosetta energy、口袋可达性）原文未给 cutoff；口袋埋藏度口径＝平均 7.1 个 α-carbons 在底物 8 Å 内（PDBbind 统计）；FoldSeek 平均最大 TM-score 0.49（报告值非阈值）
md_used=是（事后机理：GROMACS 2023.4/amber99sb-ildn/SPC-E/150 mM NaCl，先 50 ns 确认平衡再 20×20 ns apo 重复轨迹，算 RMSF 与氢键/官能团距离偏差；作者自述这些指标与活性不相关，未进入筛选闸口）
qm_used=否（正文与 Methods 无 QM/DFT 计算；QM 仅出现在参考文献 41 的 QM/MM 研究；CSV 现值"是-化学步"与本地全文不符）
experimental_methods=合成基因→Golden Gate 入 His-tag/TEV 载体→E. coli BL21(DE3) STAR 96 孔+24 孔自诱导（双重复）→Ni-NTA 磁珠 96 孔板自动化纯化→初筛荧光（Ex330/Em452，产物 2）→SEC+intact MS+CD+SAXS（FoXS χ2）→Michaelis-Menten（SciPy 拟合）→位点定向突变（K→A/N→A/Y→F）→pH 速率曲线（pH 4.6–10.6，双 pKa 拟合）→手性 HPLC（ee、E-value、动力学拆分）→turnover 实验→MBH 终点法 HPLC（lysozyme 作背景对照，imidazole/DMAP 作小分子对照）→X 射线晶体学（6 个结构：9GBT/9FW5/9FW7/9FWA/9QDP/9R7F，最高 1.13 Å）
pipeline_counts=retro-aldol：8 个 artificial motifs → 12 个 unique backbones → 36 条序列下单 → 35 克隆成功 → 35/35 可溶 → 32/35（91%）初筛高于负对照 → 29/35（FoXS χ2<5）折叠 → 30/35 得动力学参数 → 7/35 超 kcat 10-3 s-1 → 2 条高活性（RAD29/RAD35）→ 4 条得晶体结构；MBH：18 条（14 骨架，BH32.14）+ 45 条（23 骨架，BH1.8）= 63 条 → 17/18（94%）与 42/45（93.3%）高于背景 → 2 条做动力学（MBH18/MBH48）→ 2 条得晶体结构；motif 库规模、扩散采样条数与各轮精修留存量正文未给
hit_rate=按"有产物"口径：91%（32/35）、94%（17/18）、93.3%（42/45），总送测 99 条（作者自述 as few as 35 sequences in one instance and fewer than 100 overall）；按"motif 真参与且高活性"口径仅约 7/35（20%）与 2/63；对照：MBH48 的 kcat 是 BH32.8（筛 13,590 克隆 / 8 轮进化）的 1.5 倍，仍比 BH1.8 23H 低 45 倍
best_metric=retro-aldol：RAD35 kcat 3.6×10-2 s-1、RAD29 3.1×10-2 s-1（KM 约 100 µM、催化效率 290 M-1 s-1，约为高度进化的 RA95.5-5 的 320 M-1 s-1 的 90%），相对非催化反应加速约 5×106 倍，turnover 895–1,000（48 h），RAD35 E-value >200（99% ee），全部但 1 条设计 >90 °C 保持折叠、GdnHCl 中点 2.5 至 >6.5 M；MBH：MBH48 kcat 0.025 min-1、MBH18 7.7×10-3 min-1（侧产物明显）；计算侧最佳活性预测量＝AF3 复合指标与实测 kcat 的 Spearman ρ=-0.64
cost_or_stat_note=全文未记录任何算力/机时/成本（无 GPU·h、无每条设计生成时间）；未记录 motif 库规模与漏斗各级淘汰比例；稳定性回归 Pearson R=0.8（P<0.05 相关指标：AF2 平均 pLDDT、Rosetta total score、core atomic density、SAP）；MD 规模 20×20 ns + 前置 50 ns，结果与活性无相关（作者自述 negligible correlation between predicted enzyme rankings and actual activity）；RAD17 的 kcat 未测定；RAD29/RAD35 动力学参数因在 pH 最优之下测得而被低估（表观 pKa1 7.0–9.0，原始四元组 6.2）
role_in_timeline=外部对照（非 Baker 组）：这是全项目里唯一一篇严格"催化 motif/理想活性位点先定死 → 反向造骨架与口袋"并给出成套湿实验结局的 Nature 全文。它把 motif scaffolding 的通量优势做实（99 条送测即拿到与 8–14 轮定向进化相当的活性），同时用自身数据证伪了两件事——静态 sidechain RMSD 排不出活性、apo 态 MD 指标与活性不相关；唯一与活性相关的计算量是含底物/共价中间体的 AF3 复合物几何（ρ=-0.64，无独立留出集）。对本项目的定位：支持"motif 优先"的生成路径，不支持"结构自洽性可预测酶活"
source_pointer=data/interim/baker_lit/ft/motifscaffold2026.txt（Europe PMC fullTextXML，PMC12727513，PMID 41339546，DOI 10.1038/s41586-025-09747-9）；登记底稿 sources/baker.md:593（作者归属有误，已在本卡第 0/9 节标注）、sources/cost-benchmarks.md（无本篇条目）；代码 https://github.com/mabr3112/riff_diff_protflow；数据 Zenodo 10.5281/zenodo.15979364 与 10.5281/zenodo.15494858
CSV回填-->
