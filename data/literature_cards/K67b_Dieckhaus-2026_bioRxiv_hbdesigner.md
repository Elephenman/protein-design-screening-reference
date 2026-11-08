# [K67b] HBDesigner：把埋藏氢键网络设计变成"可学习的模块"（深度学习采样 + 原子能量打分）

Dieckhaus H, Harvey BT, Mulikova T, Horenstein JT, Nicely NI, Randolph NZ, Kuhlman B（UNC Chapel Hill，通讯 bkuhlman@email.unc.edu）
bioRxiv 预印本（2026-06-08 挂出）· DOI 10.64898/2026.06.08.730848 · PMID 42327288 · PMCID PMC13277954（本卡通读 .2 版）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K67b**（组：通用方法学） |
| 条目类型 | **论文级手稿，但为预印本**：本地全文身份块标 `is-preprint yes`、`is-journal-matter no`、`is-manuscript no`、`status released`、`is-retracted no` |
| 版本与日期（以文件头身份块为准） | PMC13277954.1 = 2026-06-11；**PMC13277954.2 = 2026-09-30（本卡通读这一版）**；bioRxiv DOI 后缀 2026.06.08.730848（挂出 2026-06-08）；PMCID 收录时间戳 2026-10-03 |
| 同行评议状态 | **未见同行评议正文**：全文无期刊卷期页码、无收稿/审稿/编辑日期、无勘误记录； venue 仍为 bioRxiv（Cold Spring Harbor Laboratory Preprints）。凡本卡引用的命中率、阈值，性质都是**预印本自述**，不是同行评议结论 |
| DOI 核对 | 文件头身份块 DOI = `10.64898/2026.06.08.730848`，与 CSV 原登记值一致（任务卡提示的 …730843 未在本地全文任何位置出现，判定为笔误而非 DOI 变更） |
| 本地全文（唯一引句底稿） | `data/literature_cards/fulltext/K67b_PMC13277954_text.txt`（由同目录 `K67b_PMC13277954_fullTextXML.xml` 抽出的纯文本，94,787 字符，单行） |
| 证据级别 | **全文级（读的是 OA 预印本正文 PMC13277954.2，本卡 66 条英文引句全部逐字命中上面那份 txt）**；CSV 行原登记为题录级（本次经 PubMed/Crossref 核对，未读正文），本卡把 evidence 相关字段改为实读值。因**未见同行评议正文**，引用强度按"预印本自述"打折 |
| 未取到的部分 | Supplementary 1–3（含 Supplementary Table 1 输入特征表、Table 2 采样参数、Table 3 晶体学 refinement 统计）、Extended Data Fig 1–11 的原图数值、Zenodo 数据集与脚本、PDB 13JM/13FC/35SL/35SB 的坐标。凡涉及这些，本卡明写"仅在正文图注/正文描述里出现" |
| CSV 原登记与本卡的差 | 原行 `计算筛选判据/阈值/MD/QM/实验手段/候选数递减/命中率/Kd` 全为"未记录"（题录级）；本卡第 3、4、9 节把这些填成实读值 |

## 1. 这篇到底解决什么（一句话）

**把"在设计好的骨架里放一张连通的埋藏氢键网络（HBnet）"这件事，从 Rosetta 的物理采样（HBNet / MC HBNet）搬到一个可学习的生成模型上**：用图神经网络自回归地同时预测"哪些残基进网络 + 它们是什么氨基酸"，再用第二个网络预测侧链 chi 角，最后用 PyRosetta 做原子级能量最小化、打分与排序；作者用它做了三件实验（极性核心的 de novo 单体、高极性界面的均二聚体、给同族异二聚体装上配对特异性），并把氢键判据（saturation、BUHs/BUPHs、HBNet Score）与 AF3 自洽性回收串成一条可下单的漏斗。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **通用序列模型（ProteinMPNN 一类）没有原子能量函数，压根无法显式优化氢键几何。** 现象：作者点明 "these and other DL design tools lack the atomistic energy function necessary to explicitly score"，因此这些工具 "cannot be readily adapted to design H-bond networks with high connectivity or specific amino acid"（该句紧跟在上一句之后，中间无引文号）。 **应对**：不做端到端纯 DL，而做成**三段混合**——DL 负责快速采样（"The third step, the scoring module ( Fig."），把"生成快"和"判据物理"分开。 **代价**：网络必须靠 PyRosetta 事后收拾——"postprocessing with the Rosetta MinMover was essential to avoid clashing and disfavored Rosetta energy scores"，即 DL 直接吐出的构象本身不合格。
2. **MC HBNet 的两个已知缺陷：固定 rotamer 库 + 长柔性侧链难建模。** 原句："While effective, MC HBNet suffers from a few limitations," **应对**：packing model 直接回归侧链 chi 角（正弦/余弦）并用理想键长键角重建，再加 3 轮 recycling；实测在"无周围序列上下文"的复包测试里 rotamer recovery 更高、RMSD 更低。 **代价**：模型仍用 "HBDesigner uses idealized sidechain bond lengths and angles, which may limit its ability to sample realistic network geometry."，且不采样骨架（作者明写 "HBDesigner might benefit from allowing for backbone flexibility during sampling"）。
3. **越极性越难成——这是本文最难看的一条自损数据。** 现象（单体）：Helical bundles had the highest expression success rate (9 of 11 designs), while mixed α/β folds were moderately successful (2 of 4), and all β-sheet-rich designs (0 of 4) failed，且 "While designs with the highest bpSA% were the least likely to express well,"（两句之间夹了图注引用，本卡拆成两条引）。现象（均二聚体）：作者专门做了极性分位对照 "we observed lower dimerization success rates for"。 **应对**：①不追求大网络——先在流水线早期只放 3–4 残基种子，"This behavior enabled us to design large (6+"；②失败归因不硬套在极性上："most of the failed designs were those with"（作者接着承认 "It is therefore possible these designs may have"）。 **代价**：混淆未消除——折叠类型与极性没有解耦（没有同折叠类型的极性对照），这条"极性拖累成功率"仍是相关而非因果。
4. **网络越大越"折不回来"（AF3 回收率随网络尺寸崩塌）。** 原句：scaffold recovery decreased sharply with increasing network size, as over 70% of monomer scaffolds could accommodate a 2-residue network in the core, compared to less than 4% for 6-residue networks。 **应对**：①大网络用低噪声设计模型 + 更多采样（"Large networks required more samples to find sufficient high-quality networks, at the cost of slightly increased runtime."）；②把网络拆小、靠 ProteinMPNN 延长（见第 3 条）；③界面侧改用"非对称网络 + 对称复制"覆盖大界面："We used symmetry constraints (flag --symm_chains" **代价**：可设计的网络上限被锁死在小尺寸；跨界面网络天生比核心网络难回收（同一句里 "networks designed across heterodimer interfaces"）。
5. **ipTM 能判"配对特异性"，判不了"结合强弱"——漏斗末端判据失效。** 现象："while the on-target ipTM is nearly identical for"（该句前面夹有 "However,"）。 **应对**：把 ipTM 的用法从"结合概率"改成**差值**（ΔipTM = 正确配对 − 错配），并用它做二级筛选：先要 on-target ≥0.75（两套序列都要），再要 MPNN 的 off-target ≥0.75 而 HBDesigner 的 ≤0.50，最后用单体 pLDDT 与同源二聚 ipTM 罚分挑 family。作者自己收口："In this one limited example, AF3 ipTM served as a useful specificity screening tool but was unable to distinguish between weak and strong binders." **代价**：亲和力靠 ELISA 事后才知道；HBDesigner 系列换特异性赔上活性（"The HBDesigner heterodimers, on the other hand, had significantly improved specificity for their intended design partners, at the cost of diminished on-target affinity"），且只有 6 个异二聚体进实验。
6. **意外现象：JH1 在晶体里发生 domain swap（结构对了但组装方式没照设计）。** 现象：晶体里 "Under crystallization conditions,"。 **应对**：把意外当成可诊断信号——发现 AF3 在"按二聚体输入"时**正确预测出了这次 domain swap**，据此提出 loop1 应变假说，然后用 RFdiffusion motif scaffolding 重设计 loop（3–12 残基），按"单体 pLDDT 高 + 二聚体 ipTM 低"排序，得到 "with a reduced dimer ipTM of 0.25 compared to"，且极性核心保持完整。 **代价**：本文没重新结晶验证新变体；作者只把这条写成通用建议 "Future design efforts might benefit from the"
7. **未显式建模水，结构水里插进设计网络。** 现象："structural water intrusions into our designed"（JH1 与 S2B；JH1 里 "One interaction in the crystal structure that is"）。 **应对**：部分靠隐式指标兜住（saturation、BUHs），作者在讨论里承认 "This indicates that water can play an important" **本文未解决**：显式水没有进模型，也没有把水纳入筛选判据；S4A 的网络在四个同源二聚体里出现多种替代构象，同样没有被回收成单一设计态。
8. **特异性分析的统计功效不足，作者主动交底。** 原句："due to the small sample size of this analysis"。 **应对**：把结论降级为趋势（13/19 family 更优，而非"更大更相似的界面更好做"这类机制断言）。 **本文未解决**：没有扩充 family 数，n=19 的 ΔipTM–结构特征回归留在"低功效"状态。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 3a. 方法工具箱（用了什么、为什么用它）

- **HBDesigner 本体（新，本文主角）**：固定骨架、三段式。作者原话："we formulated HBDesigner as a three-step procedure"，接着 "The first two steps use graph"，然后 "The design model ( Fig. 1A ," 与序列模型的区别写得很直白："This sparse, network-based"
- **设计模型**：MPNN，残基为节点、按 Cβ-Cβ 距离连 30 个最近邻，骨架几何编码成节点/边特征（N、C、O、Cα、虚拟 Cβ 的两两距离各 16 个 RBF，0–20 Å；相对序列间距 ±32 残基），3 层消息传递；两个输出头：该残基是否进网络（二值）+ 网络残基的氨基酸身份（多类）。参数量 "The design model includes 1.27M"
- **侧链堆积模型（packing model）**：同架构但不接受条件信息，3 轮 recycling，回归 chi 角正余弦后用理想键长键角重建侧链；裁剪规则 "input proteins are cropped to"；损失含 mse/msd/clash/orient 四项（clash 重叠容忍 tol 1.5 Å），权重 w_mse=w_msd=1.0、w_clash=w_orient=0.2、w_norm=0.1。参数量 "The packing model includes"
- **打分/排序模块（物理侧）**：PyRosetta REF2015 + MinMover（"The MinMover class is used with"，只放开网络残基侧链），按 MC HBNet 论文的指标打分：BUHs、BUPHs、saturation、HBNet Score。
- **条件化三条通道**：序列条件（指定氨基酸组成，推理时是硬约束）、虚拟 guide atom（指定网络质心，灵感来自 RFdiffusion2 的 ORI token，默认软约束，可给半径转硬约束）、锚点残基（保证入网，实现"单侧界面设计/网络延长"）。
- **下游序列设计**：LigandMPNN 把 HBDesigner 网络当序列+结构上下文（`--ligandmpnn_use_side_chain_context`），均二聚体用 `--homo_oligomer` 与 `--symm_chains A,B`。
- **骨架生成**：RFdiffusion（无条件 / fold-conditioning / monomer_ROG / monomer_contact / C2 对称 + olig_contacts 0.4/0.2 / partial diffusion partial_T=5）、RFDiffusion motif scaffolding（JH1 loop1 重设计）。
- **结构预测与验证**：AlphaFold3 高通量自折（"We then refolded all sequences"）；PLACER（固定骨架去噪模型，50 个样本）；Boltz-2、ESMFold2、Chai-1 三个"不参与挑选"的独立预测器；STRIDE 二级结构；Rosetta LayerSelector / InterfaceAnalyzer / InterGroupInterfaceByVectorSelector。
- **对照方法**：ProteinMPNN、带埋藏极性偏置的 b-ProteinMPNN（"we add a constant bias favoring"，偏置强度 "This resulted in bias terms of"）、Rosetta MC HBNet（"-ex1 -ex2"，"10,000 Monte Carlo samples were"）、PIPPack、Rosetta PackRotamersMover。
- **实验侧**：E. coli（BL21(DE3)）表达 + Ni 纯化（均二聚体带 MBP 融合便于检测）、圆二色 CD 谱与 5→95 °C 熔解、质量光度计（mass photometry，50 nM/100 nM 判聚合态）、SEC、X 射线晶体学（SER CAT 22-ID-D，AF3 预测做分子替换）、生物素化 + ELISA 结合曲线（n=3）。
- **没有用的方法**：MD、QM/自由能微扰、显式溶剂——本文全程无轨迹、无自由能计算；氢键靠 REF2015 能量项 + 几何判据，水只作为"事后出现在晶体里"的角色。

### 3b. 工作流程（六段，逐步）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| 1 训练集构建 | PDB 2021-08 快照（ProteinMPNN 数据集改版，去配体/溶剂/辅因子） | 侧链拆 chi 角后用理想键长键角重建 → PyRosetta 加/优化极性氢 → REF2015 算 sidechain-sidechain 氢键 → 建图取连通分量 | "Biological assemblies solved by"；"H-bond networks were identified"；"To avoid transient surface"；按 30% 序列同一性分簇切 train/val/test | "This resulted in 19,916/1,209/1,247 clusters assigned to the training/validation/test sets, respectively, containing 84,388/4,003/3,872 chains with 1,767,365/98,078/84,019 H-bond networks."（>1.7M 网络） |
| 2 训练 | 上表的簇；每条样本随机取一个 assembly + 一个网络，非网络残基的序列与侧链坐标先清掉 | 设计模型 + 堆积模型并行训练 | "We train both the design and"；Adam + Noam，warmup 4,000 步；设计模型骨架加 σ=0.2 Å 高斯噪声、堆积模型 σ=0.02 Å；guide atom 50% 概率采样、完整/部分序列条件各 10%；w_pos=w_seq=1、γ=2；recycle 数 r ∈ {0,1,2,3} | 两个模型：设计 1.27M 参数（A100 10 小时）、堆积 1.21M 参数（A100 ~40 小时） |
| 3 推理（放网络） | 任意输入骨架（native 或 de novo）+ 可选条件信息 | 设计模型反复采样 → 裁剪 → 堆积模型出侧链 → PyRosetta 最小化并按指标排序 | "the design model is repeatedly"；"Any predictions that fail to"；默认返回阈值 "By default, we follow the MC"，按此顺序排序取 top K | 单体核心每骨架 top 5（网络尺寸 2–6）；界面每骨架 top 15；heterodimer 特异性测试每骨架最多 2,000 样本取 top 30；"total runtime for HBDesigner is" |
| 4 计算对照（refolding benchmark） | 三套骨架：532 个 native 单体域（"We obtained 532 native monomeric domains of 50-200 residues from the HBDesigner test set by randomly sampling one representative from each qualifying sequence cluster."）、726 个 de novo 单体（80–120 残基）、690 个 de novo 异二聚体（200–300 总残基） | 三条序列路线（HBDesigner→LigandMPNN / ProteinMPNN / b-ProteinMPNN）→ AF3 自折 → PyRosetta 最小化 → 统计极性与埋藏氢键 | 骨架预筛："The de novo heterodimers were"（此处纯文本抽取把不等号抽成了残缺符号，原文写作 500Å δ ΔSASA δ 2000Å，按上下文读作 500–2000 Å² 的界面面积窗口）、STRIDE ≥50% helix/sheet 且 ≥10% turn/coil、单体 ≥12% 残基判为 Core；折回判据 "All successfully refolded"；回收判据 "we consider a scaffold successfully recovered if any of the 20 designed sequences (4 per network) is well-folded"（且全部设计氢键以 RMSD_net ≤ 1.5 Å 复现） | Fig 2 图注给的样本量：极性组成 n=525、复包测试 n=1,011、native 单体 n=642、ProteinMPNN 设计 n=629、核心网络回收测试 n=726、界面 n=690、特异性测试 190 正确配对 vs 1,710 错配；Table 1：单体 HBDesigner "HBDesigner 7.6 ± 0.6 8.9 0.69 79 45 MC HBNet 5.5 ± 1.9 13.5 0.65 76 51"，异二聚体 "HBDesigner 9.3 ± 0.7 11.2 0.72 0.59 32 MC HBNet 28 ± 6 7.7 0.69 0.58 29"（MC HBNet* 更严 MoveMap 时降到 22%） |
| 5a 单体实验漏斗 | RFdiffusion 出 4 组各 1,000 个 80–120 残基骨架 | HBDesigner 放 3–4 残基网络（无条件采样，最小埋藏 4.0 加权侧链邻居、至少 1 个核心残基）→ LigandMPNN 每网络 4 条序列 → AF3 → PyRosetta → BUH/极性 → PLACER | "This produced a total of 16,202"；"First, we filtered for highly"；再要求全部预测氢键回收且 RMSD_net ≤ 1.0 Å → "This left 3,245 high-quality"；"We generated an ensemble of 50" | 544 → 271 → "From these, we selected 19" → 11 个表达良好/稳定/折叠正确（末端 11/19 ≈ 58%，**该百分数为本卡换算，原文未给**） |
| 5b 均二聚体实验漏斗 | RFdiffusion C2 对称骨架（60–120 残基/链，olig_contacts 链内 0.4 / 链间 0.2；骨架尺寸在 Results 与 Methods 两处口径不一致，见 §7.8） | HBDesigner 设计跨界面 2/3/4 残基网络 → 对称复制 → LigandMPNN 每网络 5 条（温度 0.1）→ AF3 → PyRosetta → 网络完整回收 | "We ran HBDesigner to design"；"We used symmetry constraints"；"All successfully refolded"；多网络拼接时 "combined networks were rejected" | 首轮 22 个表达：全部表达良好，15 个在 50 nM 下主要为二聚体；次轮（多网络）9 个：3 个主要二聚、3 个主要单体、3 个平衡；3 个解析晶体结构（S2B 1.80 Å、S3G 1.79 Å、S4A 1.83 Å） |
| 6 特异性实验漏斗 | 19 个既有 de novo 异二聚体（ipTM > 0.8、pTM > 0.7） | 每 seed 用 partial RFdiffusion 生成 10 个近似骨架（TM>0.9）→ 两套序列（HBDesigner 4 残基网络 + LigandMPNN / 仅 LigandMPNN）→ AF3 交叉折叠算 ipTM → 挑"MPNN 花、HBDesigner 专一"的 family → 表达 + 生物素化 ELISA | "Within each family, we first"；"looking for pairs of backbones"；"Any subunit with monomer pLDDT" | 190 个骨架 → 19 个 family（190 正确配对 + 1,710 错配的 ipTM 分布）→ 选出 6 个同族异二聚体进 ELISA（n=3 曲线）；最好设计 HBDes3 = 110 nM 靶内亲和力 + 对靶外 100 倍特异性 |
| 7 结构验证（不参与下单） | 生化上验证过的 11 个单体 + 18 个均二聚体 | 三个**未用于筛选**的独立预测器（Boltz-2 / ESMFold2 / Chai-1）+ PLACER 50 样本 → TM/RMSD 对齐设计模型 | "None of the other three tools"；判据见结果：median TM > 0.95（单体）、> 0.97（均二聚体）、median RMSD_net 0.26 / 0.34 Å、median pLDDT 0.97 / 0.98 | 单体侧另有一条"表达但不结晶"的补救线：n=10 全部走计算验证 |

## 4. 关键数字台账（数值 · 含义 · 出处；数字均可在本地全文里搜到）

| 数值 | 含义 | 出处（本节末给出定位方式） |
|---|---|---|
| 1,767,365 / 98,078 / 84,019 | 训练/验证/测试集的 H-bond 网络数（>1.7M） | Methods Dataset curation；摘要式表述 over 1.7 million |
| 19,916 / 1,209 / 1,247 簇；84,388 / 4,003 / 3,872 链 | 30% 序列同一性分簇后的三集划分 | 同上 |
| ≤3.5 Å；10–10,000 残基；≥25% resolved | 入训 assembly 的解析门槛 | Methods：resolution ≤ 3.5 Å and 10-10,000 total residues with ≥25% of residues resolved |
| 网络 2–6 残基；≥50% 残基埋藏；>4.0 加权侧链邻居 | 网络定义与埋藏门槛（LayerSelector） | Methods：those with 2-6 residues were retained |
| 1.27M 参数 / 10 小时 A100；1.21M 参数 / ~40 小时 A100 | 设计模型 / 堆积模型规模与训练成本 | Methods：can be trained in 10 hours on an A100 GPU |
| 200,000 优化步；batch 10,000 tokens；warmup 4,000 | 训练超参 | Methods Training procedure |
| 每骨架 100–1,000 次采样；top 5（单体/界面 top 15；特异性测试最多 2,000 样本取 top 30） | 推理采样与保留数 | Methods HBDesigner inference / Refolding benchmark |
| ≤0 BUHs；≤5 BUPHs；≥0.5 saturation；≤0 REU HBNet Score | 默认网络返回四道硬阈值 | Methods HBDesigner inference |
| 7.6 ± 0.6 s vs 5.5 ± 1.9 s（单体）；9.3 ± 0.7 s vs 28 ± 6 s（异二聚体） | HBDesigner vs MC HBNet 每骨架用时 | Table 1 |
| 8.9 vs 13.5（找到网络数）；0.69 vs 0.65、0.72 vs 0.69（Top-5 saturation）；79 vs 76（AF3 pLDDT）；45% vs 51%（scaffold recovery，单体）；32% vs 29%（异二聚体）；0.59 vs 0.58（AF3 ipTM） | 与 MC HBNet 的逐项对比（核心互有胜负、界面 HBDesigner 全面略优） | Table 1 |
| 34% → 77%（序列条件下的天然氨基酸回收）；14% → 43%（guide atom 下的位置回收） | 条件化的作用量 | Results：conditioning on the native network sequence |
| >70%（2 残基核心网络）→ <4%（6 残基） | 网络尺寸对可回收性的悬崖 | Results：scaffold recovery decreased sharply with increasing network size |
| 29%（MetalPDB）/ 39%（AME） | top-10 内二级壳层相互作用回收率 | Results + Methods（500 样本、锚点条件） |
| 0.90 / 0.73 → 0.88 / 0.51 | 正确配对 / 错配的中位 ipTM（仅 MPNN → 加 HBDesigner） | Results：the correctly paired dimers received high ipTM scores |
| 13/19 family | HBDesigner 的 ΔipTM 优于 MPNN 的 family 数 | Results（Extended Data Fig. 5A） |
| 19 → 11；9/11、2/4、0/4 | 单体：送测数→成功数；按折叠类型拆分 | Results：We selected 19 designs；Helical bundles had the highest expression success rate |
| >95 °C（12 个纯化设计里的 7 个） | 高极性核心仍可超稳定 | Results：seven of the twelve purified designs were folded up to |
| 16,202 网络 / 64,808 序列 → 30,572 → 3,245 → 544 → 271 → 19 → 11 | 单体计算漏斗逐级递减（原文逐段给出） | Methods Computational design of de novo monomers |
| 判据链 pLDDT ≥ 80 且 RMSD Cα ≤ 1.0 Å；RMSD_net ≤ 1.0 Å；BUHs <5 且核心极性 >28%；PLACER 50 样本、氢键回收 ≥80%、RMSD_net ≤ 0.5 Å | 单体漏斗的四道筛选 | 同上 |
| 22 表达 / 15 主要二聚（50 nM，MP）；3 混合 / 1 高质量峰；次轮 9 → 3/3/3 | 均二聚体实验规模与 MP 读数 | Results：All 22 designs expressed well |
| 33%（上半极性 5/15）vs 81%（下半 13/16） | 界面极性分位与二聚成功率 | Discussion：we observed lower dimerization success rates |
| S2B 1.80 Å（RMSD Cα 1.74 / net 1.88）；S3G 1.79 Å（0.83 / 0.22）；S4A 1.83 Å（0.66 / 1.03）；JH1 2.1 Å（0.93 / 0.53） | 四个晶体结构的对齐质量 | Results（PDB 35SL / 13FC / 35SB / 13JM） |
| 0.89 → 0.25 | JH1 loop1 重设计后的二聚体 ipTM | Results：with a reduced dimer ipTM of 0.25 compared to 0.89 for JH1 |
| 190 正确配对 vs 1,710 错配；19 骨架 × 10 近似骨架（partial_T = 5，TM>0.9） | 计算特异性测试规模 | Methods Computational binding specificity test |
| 6 个同族异二聚体；HBDes3 = 110 nM、100 倍特异性 | 特异性实验末端读数 | Results：Our best-performing design, HBDes3 |
| on-target ipTM 0.90–0.91（HBDes）vs 0.91–0.93（MPNN），但实测结合差 10–100 倍 | 判据与实验脱钩的直接证据 | Discussion：the on-target ipTM is nearly identical |
| TM>0.95、序列同一性>60% | HBDes 与 MPNN 两套设计的相似程度 | Discussion：Our results support this premise |
| median TM > 0.95（单体）/ > 0.97（均二聚体）；PLACER median RMSD 0.26 / 0.34 Å，median pLDDT 0.97 / 0.98 | 三个独立预测器 + PLACER 的正交验证 | Results（Extended Data Fig. 8） |
| n=642 native 单体 / n=629 MPNN 设计 / n=47 native 螺旋型强制二聚体（自 122 条筛得）/ n=92 MPNN 界面 / n=31 本文界面设计 / n=525、n=1,011 | 各图的比较分母 | Fig. 2、Fig. 4 图注 + Methods |

## 5. 作者说了什么（只写作者的主张）

1. **方法学主张**：DL 采样 + 原子能量打分结合起来的固定骨架网络设计器，在把连通 H-bond 网络装到骨架上这件事上超过现有工具；在 >2000 条 native/de novo 骨架的 in silico 基准上比 ProteinMPNN 更可靠地产出埋藏氢键网络，速度与可设计性不低于 MC HBNet。
2. **实验主张（三条线）**：①做出带极性核心的 de novo 单体（19 送测、11 成功，其中一个解析到 2.1 Å 晶体结构，网络侧链 RMSD_net 0.53 Å）；②做出界面高度极化的强制均二聚体（22 条全表达、15 条主要二聚，三个晶体结构）；③在同族高度相似的异二聚体里装上配对特异性——"prior design tools fail to do so"（摘要原话），MPNN 设计彼此混绑，HBDesigner 设计特异性提升约 100 倍、代价是靶内亲和力下降。
3. **概念主张**：埋藏氢键网络设计在现代工具下是 tractable 的（"design of buried H-bond networks is tractable with modern protein design tools"），且"提高核心极性并不必然牺牲超稳定性"（7 个设计 >95 °C 却保持天然级别的核心极性）。
4. **作者自陈的限制**：不能以特定原子 motif 为条件（pH 敏感网络做不了）、不建模配体、不采样骨架柔性、用理想化键长键角、不显式建模水；ipTM 只当特异性筛子、不能区分强弱结合；特异性趋势分析 n=19、统计功效低。
5. **作者没有主张的东西（要点）**：没有报"端到端命中率"、没有和任何 binder 靶点成功率比较、没有声称 HBDesigner 能提高结合体实验成功率、没有做任何 MD/自由能计算、没有声称对催化位点做设计（二级壳层回收只是初步实验，Extended Data Fig. 4）。

## 6. 我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的贡献是"把判据搬进生成器"，不是"提高命中率"**。HBDesigner 的卖点在于：设计阶段就以 saturation / BUHs / BUPHs / HBNet Score 这些**物理可解释的结构判据**为优化目标，因此它送进下游的序列天生带着可核验的几何约束。→ 对我们（酶设计筛选）：这提示一条与我们目前做法相反的路——**判据应当尽可能前移到生成端**，而不是全压在末端打分；但我们的"催化判据"（供体对齐、金属位、闭环几何）能不能像 HBnet 那样写成可微/可采样的显式目标，仍是未验证的前提。把握度：中等（机制类比，不是数据支持）。
2. **"末端成功率 58%（11/19）"这类数字不能当概率引用**。它的分母是**已经过 5 道计算筛 + 人工目视挑选**之后的 19 条，且 271→19 这一段是"based on visual inspection"（无自动化判据），漏斗端到端是 64,808 → 11（≈0.017%）。→ 教训：作者诚实给了逐级数字，反而让"11/19"这种末端读数失去意义。我们做漏斗时**必须同时印末端比例与端到端比例**，且目视挑选那一环要写明不可复现。
3. **AF3/PLACER 的"自洽"是必要不充分的**。本文最干净的一条内部反证：on-target ipTM 几乎一样（0.90–0.91 vs 0.91–0.93），实测结合却差 10–100 倍。→ 对我们的含义：任何"结构预测自洽 + 能量指标"的组合，只能筛掉**明显不折**的候选，不能承诺功能；我们的产物化学（LC-MS/MS 定产物身份）这一层无法被计算替代。把握度：高（这是文内直接观测）。
4. **"隐式物理指标 + 事后最小化"是可以抄的工程形态**。HBDesigner 不用 MD、不用显式水，却靠 MinMover + REF2015 收拾 DL 的产物，并用 MinMover 前后是否 clash 判"必需"。→ 对应我们：把 xTB/单点能量当成**廉价的后处理闸**而不是主引擎，与本项目"MD 单价过高（10.6 GPU·h/体系）"的现实吻合。这是流程形状的可迁移，不是阈值可迁移。
5. **失败被拆成可命名的两种**：本文的失败轴至少有三条独立线——折叠类型（β-rich 全灭）、极性程度（上半 vs 下半）、组装态（domain swap / 多聚）。作者没有做交叉对照，所以三条线彼此混淆。→ 我们应把候选失败标注到**具体化学事件**（游离底物起始 / 中间体 / 第二底物与副反应竞争），并保证正负样本在同一轴上可分，否则又得到"相关不是因果"。
6. **预印本身份本身就是风险**：所有阈值（≤0 BUHs、≥0.5 saturation、pLDDT ≥ 80 等）都未经同行评议稳定化，GitHub/Zenodo 代码虽公开，但**没有第三方复现**。→ 我们引用它只能作为"有人在这样做、这样做有道理"的旁证，不能作为"这样做有效"的结论。

## 7. 局限（作者的 + 我们读出的）

- **作者自陈**（第 5.4 条已列）：不能原子 motif 条件化、不建模配体、无骨架柔性、理想化键长键角、不显式建模水；ipTM 判不了亲和力强弱；n=19 特异性趋势低功效。
- **我们读出的**：
  1. **末端分母极小**：单体 19→11、均二聚体 22→15（其中首轮）+ 9→3（次轮）、异二聚体 6 条进 ELISA、晶体结构只有 4 个（1 个单体 + 3 个均二聚体）。任何"成功率"都是个位数除法。
  2. **成功判据本身偏松/异构**：单体成功 = 表达良好 + CD 稳定 + 折叠曲线与设计一致，**没有热力学参数、没有功能读数**；均二聚体成功 = ">50% dimeric by mass photometry"（图注口径），是组装态而非结合态；特异性成功 = 靶外 Kd 比靶内差 100 倍，是**比值口径**。三类"成功"互不可比。
  3. **计算漏斗里有人工环节**：271 → 19 靠 visual inspection（network quality/centrality + structural diversity），这一段不可自动复现，会污染"漏斗通过率"的解释。
  4. **极性—折叠类型混淆未解耦**：最高 bpSA% 的设计同时最 β-rich，0/4 全灭，因此"极性导致失败"无法与"β 折叠难表达"分离（作者自己承认可能是聚集而非极性）。
  5. **对照实现的公平性存疑**：b-ProteinMPNN 的偏置强度是**由作者调到与 HBDesigner 极性水平对齐**的（bias 1.5/1.0/0.5），这是"对齐极性产出量"而非"对齐优化目标"的对照；MC HBNet 也由作者重新配置参数以尽量 match HBDesigner（网络尺寸、最小埋藏、核心残基数、排序标准都手动对齐，-ex1 -ex2、每骨架 10,000 Monte Carlo 样本）。同一条 MoveMap 敏感性在 Table 1 里能直接看到：异二聚体那一栏的 * 变体（只允许界面残基被设计）把找到网络数从 7.7 压到 5.2、回收率从 29% 压到 22%，说明这类"闸口读数"对可设计区域定义非常敏感。
  6. **无 MD、无 QM、无自由能、无显式溶剂**：本文不能为任何"用轨迹/自由能判催化"的路线提供命中率证据。
  7. **预印本 + 未见同行评议正文**；补充表（采样参数 Supplementary Table 2、晶体学统计 Supplementary Table 3）未取回，本卡涉及它们的读数只能到正文/图注级。
  8. **正文内部有一处规模口径不一致（本卡按两处分别照录，不取平均）**：Results 段写 "we generated de novo homodimer"，Methods 段写的是 "We generated de novo homodimer"（C2 对称下两条链合计最多 240 残基）。两者不能同时成立，读者无法判断均二聚体骨架的真实尺寸区间；同理，Table 1 的单体栏 HBDesigner 在"找到网络数 8.9 vs 13.5、scaffold recovery 45% vs 51%、用时 7.6 s vs 5.5 s"三项上**输给** MC HBNet，而摘要写的是 outperforms existing tools in designing connected H-bond networks onto protein scaffolds——增益实际集中在**界面/异二聚体**那一栏（0.72 vs 0.69、32% vs 29%、9.3 s vs 28 s）。引用本文时要把"哪一栏赢"写清楚，不能整篇当成"胜过 MC HBNet"。

## 8. 迁移到我们的筛选／判定工作流

**可迁移（怎么用）**

1. **"埋藏不可满足极性"这一类可命名的小指标可以搬成候选描述符**：BUHs / BUPHs / saturation 是纯几何计数，我们的候选酶位点同样可以算"埋藏但未满足的极性原子数"（用现有 PyRosetta/REF2015 或 xTB 单点 + 几何判据），作为**负向排除项**（明显埋了不饱和极性 ⇒ 该位点不可能那样结合底物），而不是作为酶活预测器。用法限定为"排除"，符合单向否证的定位（与本轮 P1 的 BcCdnD clade D 只 26.88% 同源这种"单向证据"同构）。
2. **"生成端放种子 + 下游模型延长"的两段结构**：本文先放 3–4 残基种子、让 LigandMPNN/ProteinMPNN 延长到 6+ 残基。→ 对应我们：召回端只放**最强机制约束**（双供体几何、Pfam 成员制），把细节交给下游打分，避免"约束越全越召回不到"的坑（本轮 A5 的教训：盲口径只有 B_FOLD+B_SITE 时 AUROC 0.2527）。
3. **"三个独立预测器不参与挑选"的验证纪律**："None of the other three tools" → 我们的对应做法：**任何用于下单的判据不能同时充当验证判据**（同 271 候选里 p 全靠 palm_ge1 一格的膨胀读数）。要把 Foldseek/pLDDT 之类既当召回又当支持的用法，改成一端冻结、另一端留出。
4. **"通过率 ÷ 单价"仍要一起报**：本文给了 7.6±0.6 s/骨架 这种可直接进预算的单价；我们已有 MD 10.6 GPU·h/体系、xTB 63.3 s/单点（225 原子）的实测单价，任何新判据上线前必须先给单价。

**不可迁移（为什么不能照搬）**

1. **≤0 BUHs、≥0.5 saturation、≤0 REU HBNet Score、pLDDT ≥ 80、RMSD_net ≤ 1.5 Å 全部是"会不会按设计折成/连成这张氢键网"的判据，与"会不会催化酶设计与 tRNA 的反应"无关**。把任何一个数值搬进我们的漏斗当门槛，都是把 binder/折叠判据当酶活判据——本项目判定标准明确禁止（本库判据 §2）。
2. **11/19、15/22、5/15 vs 13/16、"100 倍特异性"这些命中率/比值，不得写成"某法对酶设计成功率 X%"**。分母是人工挑过的个位数候选，且是预印本自述；引用时只许引用**方法结构**与**失败分型思路**。
3. **本文的"实验验证"没有一条是产物化学**：CD/SEC/MP/ELISA/晶体学全部是**结构与组装态**证据。我们的成功判据必须落在"产物身份 + 副产物"上，二者证据类型不同，不能类比成"他们也做到了实验验证"。
4. **无 MD/QM**，所以本文对"用构象动力学或反应能垒判功能"既不提供正面证据也不提供反面证据；引用它来支持或否定该路线都是无效引用（本文无此内容）。
5. **极性提升可溶性/特异性的收益不针对我们的目标**：酶设计筛选的目标不是"让界面更极性/更可溶"，而是"找到能成键的位点排布"。搬"装极性网络"这一动作会直接把问题换掉。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K67b_PMC13277954_text.txt

- **唯一底稿**：`data/literature_cards/fulltext/K67b_PMC13277954_text.txt`（由同目录 `K67b_PMC13277954_fullTextXML.xml` 经 `scripts/litcards_text.py` 的 strip_tags + norm 得到的纯文本，94,787 字符，单行；正文含 2026-09-30 的 .2 版）。本卡 **66 条**英文引句（去重 64 条）全部只声明这一份底稿（同一论文若另有 NCBI/Europe PMC 抽取版本，本卡不使用、不引用）。
- **未使用的可引材料**：Supplementary 1–3、Extended Data 图注原值、Zenodo 数据与脚本、PDB 坐标——本卡没有这些，涉及处一律写"正文/图注口径"。
- 身份核对：文件头身份块给出 PMC13277954、PMC13277954.1（2026-06-11）、PMC13277954.2（2026-09-30）、PMID 42327288、DOI 10.64898/2026.06.08.730848、is-preprint yes、is-journal-matter no、is-retracted no——**与 CSV 行 K67b 的 DOI/PMID 一致**（任务卡提示的 …730843 未在全文出现）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K67b" --no-report` —— 结果见本次回报；引句命中情况以该脚本输出为准（脚本把卡内所有不含中日韩、被直双引号包住、≥20 字符、≥12 字母的片段，在这份底稿里逐字查找）。
- 已知门禁状态：`data/literature_cards/inventory.json` 与 `sources_map.json` 现已把本行两条本地件（`K67b_PMC13277954_fullTextXML.xml`、`K67b_PMC13277954_text.txt`）登记为可读底稿（`has_fulltext: true`）；核验器只把非 `.xml` 的那份当逐字比对基准，与上面声明的引句底稿一致。本卡未运行 `--sync-map`（登记由用户侧完成）。
- 与 CSV 待回填的差：CSV 行的 `计算筛选判据 / 阈值数字 / 是否用MD / 是否用QM / 实验验证手段 / 候选数递减 / 实验命中率 / Kd或活性最好值 / 证据级别` 九格原为"未记录/题录级"，本卡 §9 回填块已给出实读值，等统一回写。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 56 条逐字引句来自许可受限的第三方来源（K67b；CC_BY_NC_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（预印本，bioRxiv，未经同行评议；本地为 PMC 收录的预印本版全文 PMC13277954.2，2026-09-30）
target=埋藏氢键网络（HBnet）的深度学习设计：极性核心 de novo 单体、高极性界面强制均二聚体、同族异二聚体的配对特异性
backbone_generation=RFdiffusion（无条件 / fold-conditioning / monomer_ROG / monomer_contact / C2 对称 + olig_contacts 0.4:0.2 / partial diffusion partial_T=5）出固定骨架；HBDesigner 在骨架上放 2–6 残基氢键网络（设计模型 + 堆积模型）；LigandMPNN 出其余序列（网络作序列与结构上下文，--symm_chains A,B、--homo_oligomer）；JH1 loop1 用 RFDiffusion motif scaffolding 重设计
computational_filters=氢键网络指标（sidechain-sidechain 氢键图、connected-component 判定、saturation、BUHs、BUPHs、HBNet Score）；PyRosetta REF2015 最小化与打分（MinMover）；堆积质量 rotamer recovery（±10°）与 RMSD；AF3 自折自洽（pLDDT / ipTM / RMSD Cα / RMSD_net）；PLACER 侧链去噪验证；Boltz-2 / ESMFold2 / Chai-1 三个不参与挑选的独立预测器；STRIDE 二级结构；Rosetta LayerSelector 埋藏与 InterfaceAnalyzer 界面面积；ΔipTM（正确配对 − 错配）作特异性代理
thresholds=网络返回默认 ≤0 BUHs、≤5 BUPHs、≥0.5 saturation、≤0 REU HBNet Score；训练入组 ≤3.5 Å、10–10,000 残基、≥25% resolved、网络 2–6 残基、≥50% 残基埋藏（>4.0 加权侧链邻居）；骨架预筛 STRIDE ≥50% helix/sheet 且 ≥10% turn/coil、单体 ≥12% Core、界面 500–2000 Å² ΔSASA；refolding 判据 pLDDT ≥ 80 或 ipTM ≥ 0.7 且 RMSD Cα ≤ 2.0 Å；scaffold recovery 需 RMSD_net ≤ 1.5 Å；单体漏斗 pLDDT ≥ 80 且 RMSD Cα ≤ 1.0 Å、RMSD_net ≤ 1.0 Å、BUHs <5、核心极性 >28%、PLACER 50 样本且氢键回收 ≥80% 且 RMSD_net ≤ 0.5 Å；均二聚体漏斗 average pLDDT ≥ 80、ipTM ≥ 0.8、RMSD Cα ≤ 2 Å；特异性筛选 on-target ipTM ≥ 0.75、off-target ≥ 0.75（MPNN）配 ≤ 0.50（HBDesigner）、单体 pLDDT < 80 或同源二聚 ipTM > 0.5 罚分；埋藏下限单体 4.0、界面 3.0 加权侧链邻居；成功判据 CD 光谱/熔解与设计折叠一致、质量光度计 >50% 二聚、ELISA 靶内靶外比值
md_used=否（全文无分子动力学、无轨迹、无自由能计算；仅静态几何 + REF2015 能量最小化）
qm_used=否（无量子化学；侧链用理想化键长键角重建，能量项来自 Rosetta 经验力场）
experimental_methods=E. coli BL21(DE3) 表达（均二聚体带 MBP 融合）+ Ni 纯化；圆二色 CD 光谱与 5→95 °C 熔解；SEC 单体-二聚平衡；质量光度计（Refeyn OneMP，50 nM 判二聚比例）；X 射线晶体学（13JM 2.1 Å、35SL 1.80 Å、13FC 1.79 Å、35SB 1.83 Å，AF3 预测做分子替换）；生物素化 + ELISA 结合曲线（n=3）
pipeline_counts=训练网络 1,767,365（test 84,019）；refolding 基准 532 native 单体 + 726 de novo 单体 + 690 de novo 异二聚体；单体计算漏斗 4×1,000 骨架 → 16,202 网络 / 64,808 序列 → 30,572 → 3,245 → 544 → 271 → 目视选 19 → 成功 11；均二聚体首轮表达 22 → 主要二聚 15，次轮 9 → 3 二聚 / 3 单体 / 3 平衡；特异性测试 19 骨架 × 10 = 190 条（190 正确配对 + 1,710 错配）→ 选 6 个同族异二聚体进 ELISA；晶体结构共 4 个
hit_rate=末端口径：单体 11/19（按折叠拆：螺旋束 9/11、混合 α/β 2/4、β-rich 0/4）；均二聚体 15/22（首轮 MP 口径）+ 次轮 3/9；界面极性分位对照 33%（5/15）vs 81%（13/16）；特异性 110 nM 靶内 + 100 倍靶外（HBDes3，6 条设计内最好）；端到端单体口径 11/64,808 ≈ 0.02%（原文未如此表述，由本卡按原文逐级数字相除）；网络尺寸效应：核心 2 残基网络 >70% 骨架可回收、6 残基 <4%
best_metric=单体 JH1 晶体网络侧链 RMSD_net 0.53 Å（Cα 0.93 Å，2.1 Å 分辨率）、7 个设计 >95 °C 仍折叠；均二聚体 S3G RMSD_net 0.22 Å（Cα 0.83 Å，1.79 Å）；异二聚体 HBDes3 靶内 Kd 110 nM、对靶外 100 倍特异性（ELISA）；计算侧 HBDesigner 单体 Top-5 saturation 0.69、AF3 pLDDT 79、scaffold recovery 45%，异二聚体 ipTM 0.59、回收 32%
cost_or_stat_note=HBDesigner 每骨架 7.6 ± 0.6 s（单体）/ 9.3 ± 0.7 s（异二聚体），MC HBNet 5.5 ± 1.9 s / 28 ± 6 s；推理每骨架采样 100–1,000 网络（特异性测试每骨架最多 2,000 取 top 30）、MC HBNet 对照每骨架 10,000 Monte Carlo 样本；模型 1.27M / 1.21M 参数，A100 上分别 10 小时 / ~40 小时；本行为预印本、无第三方复现；CSV 原登记 cost 字段"替代被撤销的误引条目"仍成立，与本文内容无关
role_in_timeline=氢键判据从物理采样（Rosetta HBNet → MC HBNet，10.1021/acs.jctc.8b00033）走向可学习模型的当前节点：把 saturation / BUHs / HBNet Score 这类原子级判据前移进生成模型，并与 RFdiffusion + LigandMPNN + AF3 自洽性闸口串成一条"网络优先、序列其次"的固定骨架设计流水线；同时给出一处判据失效的实测证据（ipTM 能判配对特异性、判不了结合强弱）
source_pointer=data/literature_cards/fulltext/K67b_PMC13277954_text.txt（PMC13277954.2，2026-09-30 版，本卡通读的这份）；本次已取到 OA 预印本全文（PMID 42327288 + DOI 10.64898/2026.06.08.730848），原 CSV 行记录为题录级（本次经 PubMed/Crossref 核对，未读正文），K67b 的 evidence 相关字段应按本卡第 3、4 节改为实读值；代码 https://github.com/RosettaCommons/HBDesigner、数据 Zenodo（见全文 Data and Software Availability）
CSV回填-->
