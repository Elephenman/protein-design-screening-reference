# [B19] Modeling protein–small molecule conformational ensembles with PLACER——用便宜的随机生成网络替代 MD 去看"活性位预组织"

Anishchenko I, Kipnis Y, Kalvet I, Zhou G, Krishna R, Pellock SJ, Lauko A, Lee G, An L, Dauparas J, DiMaio F, Baker D（华盛顿大学 IPD；HHMI）
PNAS 2025, 122: e2427161122 · DOI 10.1073/pnas.2427161122 · PMID 41187076 · PMCID PMC12625923
收稿 2025-01-03，接收 2025-09-22 · 开放获取（CC BY）· 全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC12625923/
（PLACER 在 [B18] 里作为活性位预组织闸口使用；[B18] 正文对 PLACER 的机制转述可与本卡 §3 工具箱互相印证）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B19**（组：Baker组; 通用方法学; 口径对照） |
| 本文取回方式 | 先行调研缓存（baker_lit，2026-10-16），非本轮 cards/fetch_log 抓取（fetch_log.tsv 无 B19 行）；文本为 PMC XML 抽取纯文本 |
| 登记全文 | `data/interim/baker_lit/ft/placer2025.txt`（57,491 B；`sources_map.json` 中 B19 唯一登记全文） |
| 对照底稿 | `sources/baker.md` 第 251–263 行（原卡；`sources/baker.md:5,39,658` 的"MD 被成本否弃"论断即以本文为一手依据） |
| 证据级别 | **全文级**（本卡所有英文引号片段均为该全文的逐字子串，经门禁逐字比对） |
| 未取到的部分 | SI Appendix（训练超参、设计流程 section 1–5 细节、Table S3/S5）、Fig 1–4 原图数值。涉及处本卡明写"正文未给阈值" |

## 1. 这篇到底解决什么（大白话）

要评一个设计酶"会不会成"，关键不是骨架折对没有，而是**活性位在没结合底物时是否已经把催化侧链和底物通道摆好了**（预组织）。评预组织的"最正规"办法是 MD，但侧链重排发生在微秒尺度，几万条设计跑不起。这篇训了一个纯原子表示的图网络 PLACER：**输入骨架坐标 + 化学图（原子种类与成键），把配体和侧链坐标整个打乱再生回来**，重复多次就得到一个构象系综——用一次几百次的廉价采样近似 MD 想回答的"这里有多少种摆法、是不是钉死了"。同时给出每原子不确定度并合成 pRMSD，可用于排序。论文先在 CSD/PDB 上证明它建小分子与 dock 的能力（Astex、PoseBusters 基准，对比 Vina/GOLD/AF3），再回顾性证明它能"看出"RA95 系列进化前后预组织的差异，最后前瞻：从 17,810 个骨架设计池里按 PLACER 指标选 320 个走 IVTT 半定量测活，纯化复测 24 个，得到 cnRA-50（k_cat/K_M = 11,000 M⁻¹min⁻¹，比前深度学习时代该反应的任何计算设计高）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **MD 当筛选器在成本上不可行——这是全文的立论起点，也是本调研"为什么不用 MD 筛"的一手答案**。原文："most general way to evaluate such preorganization is molecular dynamics simulations ( 27 , 28 ), but as sidechain reconfiguration can occur on the microsecond time scale, such simulations are computationally expensive and cannot be applied to large numbers of designs"。**应对**：造 PLACER——"generating ensembles of models of small molecules and interacting sidechain placements much more rapidly than molecular dynamics simulations and without the limitations of the Rotamer Boltzmann method"。**代价**：PLACER 系综没有时间轴，给不出轨迹/路径/自由能，只给"摆法的分布+每原子不确定度"；它也不预测骨架（作者明说 "Unlike AF3, RF All-Atom, and other protein structure prediction methods, PLACER does not predict protein backbone structure"），所以必须搭配会折骨架的上游工具。
2. **既有的近似预组织方法卡在"单侧链独立"假设上**："Approximate discrete methods such as the Rosetta Rotamer Boltzmann method ( 29 ) estimate preorganization at the individual sidechain level, but are limited by the rotamer approximation and the inability to model coupled and concerted movements of side chains and small molecules"。**应对**：把侧链与配体放进**同一个原子图里联合随机化再生**（配体+周围 600 原子球内全部侧链一起重摆，见 [B18] 对该机制的转述），耦合运动因此进入系综。**代价**：物理能量项没了——高精度 docking 档（<1 Å）反而输给物理法（41.8% vs. 51.6%），要靠"PLACER 采样 + GALigandDock 物理极小化重打分"补 +7.3% 才追回来。
3. **网络架构在 PDB 上试错太贵**："considerably reduced the architecture exploration time (PLACER training on the PDB until convergence takes ×10 longer)"——**应对**：先拿 CSD 小分子晶体结构当"架构试验田"（226,684/7,116 训练验证），并做成套消融："Reducing the number of iterations to two or replacing the FAPE loss with a combination of coordinate and distance RMSD losses both result in predictions of substantially lower quality"；"Performance also degraded when the 2D inputs did not include the bond separation feature (an integer counting the number of covalent bonds between any two atoms in the chemical graph) but only included a binary feature flagging that the two atoms are immediately connected by a bond"。分两阶段训：先 4 个迭代块只用 FAPE，再扩到 8 块并加键合几何项。**代价**：CSD 阶段"confidence heads were omitted"，置信头能力是 PDB 阶段才具备的。
4. **模型可能背答案（数据泄漏/输入泄漏）**：两类防线。①训练集侧：与 Astex 测试集蛋白同一性 ≥30% 或配体 Tanimoto ≥80% 的条目剔除（"A PDB structure was discarded if any of its protein chains had ≥30% sequence identity to any of the protein chains in the test set"）；并在结果侧检查"Astex benchmark performance showed no significant decline when ligands with Tanimoto similarity ≥ 0.5 to the training set were excluded, indicating that data leakage is not substantial"。②输入侧：故意抹掉配体内部结构——"ensuring that neither the internal structure of the ligand nor its orientation in the pocket were inferrable from the inputs to the network"。**代价**：PoseBusters 上只有 118/428 复合物不在训练集内（其中 59 个 TC≤0.7 是更难子集），泛化证据仍然薄。
5. **IVTT 半定量给不了真 k_cat/K_M**："It should be noted that in this format of the experiment, concentration of the soluble protein remains unknown, and therefore, activity level should be treated as apparent activity defined as a product of the amount of soluble protein and intrinsic activity of each variant"。**应对**：每批 90 设计 + 6 个已知活性的对照蛋白（"Genes of several control proteins with a range of activities previously determined in purified form were included with each batch of tested designs to assist in ranking activity of the new variants"）做批间标尺；前 24 个表观活性最高者再走 E. coli 纯化 + 稳态动力学。**代价**：PLACER-活性相关分析建在这 320 个的表观活性口径上，IVTT 数值与纯化酶数值不可直接混算。
6. **PLACER 指标多、不知道该看哪几个**：**应对**——"To identify a smaller subset of PLACER metrics, we trained a simple logistic regression model to classify designs as active or inactive on a set of designs characterized in the preliminary experiment performed to identify the focus theozyme configuration"，即用**早期预实验的少量带标签设计**给指标降维。**代价**：这一步的前提是"已经有一小批测过的设计"——正是我们项目没有的东西（对照 [B09] §6.1 的 A 段缺失）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **本体**：PLACER（protein-ligand atomistic conformational ensemble resolver）——节点=重原子（"nodes representing individual heavy atoms (hydrogen atoms are not modeled to reduce computation cost) and edges representing chemical bonds between atoms"）；RF 式三轨架构 + SE3-Transformer；"For every atom, the 32 closest neighbors are picked in equal proportions based on both spatial proximity and proximity in the chemical graph"；"The fully trained network consists of eight iteration blocks with shared weights"；损失为 all-atom FAPE（"The primary structure loss is all-atom frame-aligned point error FAPE allatom , which is an extension of the original FAPE from ref. 9 to arbitrary molecules"）+ 每原子不确定度头（"These predicted deviations can then be combined over a subset of atoms of interest (e.g., a small molecule) to give the predicted RMSD"）。
- **上游**（用于酶设计应用线）：RFjoint2 出 NTF2 骨架库；XML-Matcher（RosettaMatch 系）放催化四联体；LigandMPNN 在底物存在下出序列；AF2 单序列模式复折。
- **对照基准**：Astex 非天然构象 docking 集（vs. Vina、GOLD、GalaxyDock、Rosetta GALigandDock）、PoseBusters（vs. AlphaFold3、RF All-Atom）。
- **湿实验**：IVTT（eBlocks 线性 DNA + PurExpress）半定量；E. coli 表达、IMAC+SEC 纯化、Michaelis–Menten。
- **没有用的方法**：MD（明确否弃为筛选器，见 §2.1）；QM 只做了一处提及——GEOM-DRUGS 是半经验 QM 算的（且那是**别人的**扩散模型训练集），本文自身不做 QM 计算。

### A. 网络构建线

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | CSD v5.43 小分子晶体结构 | 架构/超参试验田：从化学结构+随机初始坐标预测晶体构象 | R-factor 7.5% 且更好、无 disorder、非聚合物/有机金属、3–80 重原子、Open Babel 可解析；75% Tanimoto 切分 | 训练 226,684 / 验证 7,116；两阶段：4 块+FAPE → 8 块+键合几何损失 |
| A2 | PDB（2023-01-12 前、分辨率 <2.5 Å） | 化学图化（Chemical Component Dictionary 解析；仅去水）；训练时裁剪 ≤600 重原子、按 蛋白:NA:小分子:金属 = 1:1:5:1 选中心 | 质量过滤："These filters reduced the size of the set by 33% from 200,713 to 135,172"（≥10% 未解析原子、≥20 非标准残基剔除）；防泄漏剔除见 §2.4 | 最终 "The remaining 119,916 PDB structures were randomly split into training (112,828) and validation (7,090) sets such that none of the protein chains in the two sets share >30% sequence identity" |
| A3 | 裁剪后的结构 | 输入腐蚀：骨架原子固定仅加 "are kept fixed with only a minor Gaussian noise ( σ = 0.1 Å) added to the atom coordinates"；其余非骨架原子按连通分量塌缩后加 σ = 1.5 Å 高斯噪声 | 腐蚀集=裁剪中心 8-hop 邻域 + 全部非骨架原子 | 训练任务：从腐蚀态再生全部原子坐标 |
| A4 | 训好的网络 | docking 评估（Astex）："PLACER was run on each protein–ligand pair, generating 1,000 models" | 三档置信指标排序 (pRMSD, pLDDT, pLDDT-pDE)，取最高置信模型的 RMSD 定成败（<1 Å / <2 Å） | 65 靶 × 1,112 非天然结构对；结果：82.4% (<2 Å) 胜 GALigandDock 73.6%，41.8% (<1 Å) 负于 51.6%；物理极小化后 "gives +7.3% increase in docking success rate at <1 Å" |
| A5 | 同上 | PoseBusters 对比：只预测配体朝向（骨架已知） | 428 复合物、每复合体 100 模型；<1 Å / <2 Å | "On the 118 complexes absent from PLACER's training and validation sets, PLACER achieved 84% success at <2 Å RMSD, better than AlphaFold3 (77%) and RF All-Atom (38%)"；"At the stricter <1 Å threshold, however, AlphaFold3 remained superior (58% vs. 51%)" |

### B. 酶设计应用线（回顾 → 前瞻）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | RA95 系列已发表设计+进化中间体（有高分辨晶体结构） | 对每个反应中间体（5 态，含赖氨酸共价加合物）跑 PLACER 系综："For every retro-aldolase intermediate shown in Fig. 4 A , we ran PLACER 50 times and analyzed the structural diversity of the active site lysine (and covalent adducts of this lysine) through the mean predicted RMSD ( p RMSD ) calculated over side chain atoms and excluding backbone N, Cα, C, O" | pRMSD 均值（仅侧链原子，排除骨架） | 结论："PLACER generated ensembles are highly varied for the lower activity initial computational designs, indicating a lack of preorganization, and become increasingly well ordered for the more active evolved versions" → "This suggests that lack of preorganization was a major shortcoming of early enzyme design efforts" |
| B2 | 机制假设（进化来的催化四联体，源自 RA95.5-8F） | 前瞻造库：10,000 NTF2 骨架 → 放四联体 → LigandMPNN（底物在场）→ AF2 单序列复折 | "Structurally diverse set of 10,000 backbones in NTF2 fold was generated using RF joint inpainting (RFjoint2)"；折叠闸 "AF2 models with lDDT higher than 85 formed a pool of designs subjected to in silico selection strategies including or skipping PLACER-assisted selection" | 设计池 17,810 变体（"picking the most promising designs from the same pool of 17,810 variants"） |
| B3 | 17,810 池 | PLACER 打分：50 模型系综的几何+不确定度指标；用早期预实验标签的 logistic regression 精简指标 | "The obtained metrics included distances between polar atoms of the theozyme side chains and uncertainty (pRMSD) in polar atom positions computed over the ensemble of 50 models"（正文未给 cut-off 数值） | 选出 320 个设计 |
| B4 | 320 设计 | IVTT 半定量测活（Methodol 底物，apparent activity） | 每批 90 设计 + 6 对照；正文未给"活性线"数值 | "The activities of the 320 designs were first evaluated in an in vitro transcription translation system (IVTT), enabling rapid identification of promising variants without the need for protein purification" |
| B5 | IVTT 表观活性前列者 | E. coli 表达、IMAC+SEC 纯化、底物浓度梯度稳态动力学；同时把 PLACER 指标与活性做相关 | "we cloned, expressed in E. coli , purified by IMAC (Ni-NTA) and size-exclusion chromatography, and determined Michaelis–Menten parameters for 24 designs with the highest apparent activities" | 24 个定量值；"The most active design, cnRA-50, displayed one of the highest preorganization levels according to PLACER and had a k cat / K M of 11,000"（M⁻¹min⁻¹，摘要口径 "considerably higher than any pre"–deep learning design for this reaction） |

**流程骨架**：方法学（A 线）与用途（B 线）分开验证——先拿晶体结构基准证明"摆得准"（Astex/PoseBusters），再拿已知答案的旧设计系列证明"看得出预组织梯度"（RA95 回顾），最后才前瞻使用（NTF2 新设计）。这条"能力→梯度→前瞻"的三级台阶是我们可以照搬的评估顺序。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 226,684 / 7,116 | CSD 阶段训练/验证例数 | "The training and validation datasets consisted of 226,684 and 7,116 examples of organic nonpolymeric small molecules" |
| 200,713 → 135,172（-33%）→ 119,916 | PDB 过滤漏斗（≤2.5 Å 起点→质量过滤→防泄漏） | "These filters reduced the size of the set by 33% from 200,713 to 135,172"；"The remaining 119,916 PDB structures" |
| 112,828 / 7,090 | PDB 阶段训练/验证 | 上行同句 "training (112,828) and validation (7,090) sets" |
| 600 重原子 / σ=0.1 Å / σ=1.5 Å | 训练裁剪上限 / 骨架微噪 / 非骨架腐蚀噪声 | "During training, the input structures were cropped to at most 600 heavy atoms and centered around a randomly selected atom"；"are kept fixed with only a minor Gaussian noise ( σ = 0.1 Å) added to the atom coordinates" |
| 32 近邻 / 8 迭代块 / 1:1:5:1 | 邻居图规模 / 网络深度 / 裁剪中心类别抽样比 | "For every atom, the 32 closest neighbors are picked in equal proportions based on both spatial proximity and proximity in the chemical graph"；"The fully trained network consists of eight iteration blocks with shared weights"；"then randomly choose one of these classes with ratios 1:1:5:1" |
| 82.4% vs 73.6% / 41.8% vs 51.6% | Astex 两档：PLACER vs Rosetta GALigandDock | "PLACER performance is higher in the lower accuracy regime (% of complexes with ligand RMSD < 2 Å, 82.4% vs. 73.6%), but is behind in the high-accuracy regime (RMSD < 1 Å, 41.8% vs. 51.6%)" |
| +7.3% | PLACER dock 经 GALigandDock 物理极小化重打分在 <1 Å 档的增益 | "gives +7.3% increase in docking success rate at <1 Å and no notable change at <2 Å" |
| 65 靶 / 1,112 对 / 1,000 模型 | Astex 非天然集规模与每对采样数 | "we used a standard test set of 65 drug targets from the Astex non-native set"；"totaling to 1,112 non-native structures over the 65 targets"；"PLACER was run on each protein–ligand pair, generating 1,000 models" |
| 428 / 118 / 59 / 100 模型 | PoseBusters 全集 / 不在训练集的复合物 / 其中 TC≤0.7 难子集 / 每复合体采样 | "This benchmark consists of 428 protein–ligand complexes from the PDB"；"Of the 118 PoseBusters complexes absent from the PLACER training and validation sets, 59 contained ligands with TC ≤ 0.7 forming a more challenging benchmark subset"；"For each complex, PLACER generated 100 models" |
| 84% / 77% / 38%（<2 Å）；51% / 58%（<1 Å） | PoseBusters 118 子集上 PLACER vs AF3 vs RFAA | "PLACER achieved 84% success at <2 Å RMSD, better than AlphaFold3 (77%) and RF All-Atom (38%)"；"At the stricter <1 Å threshold, however, AlphaFold3 remained superior (58% vs. 51%)" |
| 0.5 Å / 30° | 氢键能量敏感的位置/角度偏差量级（为什么要求高） | "As 0.5 Å deviations in distance and 30-degree deviations in angle can have large effects on hydrogen bonding energies, the level of accuracy in positioning required is quite high" |
| 10,000 → 17,810 → 320 → 90+6/批 → 24 → 1 | 前瞻设计漏斗：NTF2 骨架 → lDDT>85 池 → PLACER 选人 → IVTT 批次 → 纯化定量 → 最优 cnRA-50 | "Structurally diverse set of 10,000 backbones in NTF2 fold was generated using RF joint inpainting (RFjoint2)"；"AF2 models with lDDT higher than 85 formed a pool of designs"；"The activities of the 320 designs were first evaluated in an in vitro transcription translation system (IVTT)"；"Typically, a batch of 90 designs and 6 controls were used to evaluate performance of a particular computational workflow"；"determined Michaelis–Menten parameters for 24 designs with the highest apparent activities" |
| 11,000 M⁻¹min⁻¹ | cnRA-50 的 k_cat/K_M（注意单位是每分钟） | "The most active design, cnRA-50, displayed one of the highest preorganization levels according to PLACER and had a k cat / K M of 11,000" |
| 50 次/设计；5 个反应中间体 | RA95 回顾与前瞻共用的系综规模 | "we ran PLACER 50 times and analyzed the structural diversity of the active site lysine" |

## 5. 结论——作者说了什么

1. PLACER 能从"骨架坐标+化学图"出发准确重建小分子/配体/侧链的三维排布，系综生成快而随机，适合描构象景观："PLACER ensemble generation provides a rapid means to map protein–small molecule conformational landscapes in ligand docking and to assess the accuracy and preorganization of designed active sites, which can substantially increase the success of enzyme design efforts"。
2. Docking 上"中精度档领先、高精度档落后"，且网络没专门训过非天然 docking（见 A4/A5 数字）。
3. 在酶设计里，"using PLACER to assess the accuracy and preorganization of the designed active sites results in higher success rates and higher activities"；前瞻得到 "a preorganized retroaldolase with a k cat / K M of 11,000" M⁻¹min⁻¹，"considerably higher than any pre"–deep-learning 设计。
4. 早期酶设计的核心短板被确认为预组织不足："This suggests that lack of preorganization was a major shortcoming of early enzyme design efforts"，并与更贵的 MD 研究结论一致（正文以括号引用说明）。
5. 定位声明：PLACER 不预测骨架，所以比 AF3/RFAA 快，但用途是评估/细化而非从头结构预测。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **MD 被否弃的理由是"通量 × 单价"，不是"不准"**。作者没有说 MD 结论错，而是说"cannot be applied to large numbers of designs"。→ 我们的正确读法：MD 该出现在漏斗末端少数候选的机理复核，不该出现在亿级筛选里；这与 [B09] §6.4 的"单价×通过率"账一致。
2. **"廉价系综近似"是可复制的品类**：核心是把 MD 的问题改写为"多次独立随机初始化再生 + 分布统计"，牺牲时间维度换 3 个数量级通量。酶设计场景若要做类似代理（比如活性位通道水/底物取向的分布），必须先确认**输入端**（骨架+化学图）我们能可靠给出，否则系综没有意义。
3. **他们对"打分器可信度"的三级验证顺序值得抄**：晶体基准（摆得准）→ 已知活性梯度的旧设计（分得出好坏序）→ 前瞻（真提升）。我们评估任何催化判据时同样应在旧文献真值面板上先看"梯度"，再看"前瞻"。
4. **logistic regression 需要带标签的早期实验**（§2.6）——又一次指向同一缺口：没有标签集，判据组合就只能靠机制先验而非拟合权重。
5. **单位陷阱**：本文酶活性用 M⁻¹min⁻¹，[B18]/[B20] 用 M⁻¹s⁻¹；跨文对比若忽略单位会差 60 倍。台账与 CSV 回填已分别注明。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：高精度档（<1 Å）不如物理法（41.8% vs 51.6%；AF3 58%）；PLACER 不预测骨架；训练时氢原子不显式建模；GEOM-DRUGS 那类"半经验 QM 训练集"路线不是他们的（引用对比语境）。
- 我们读出：① IVTT 口径只能排序不能定量，320→24 的漏斗里"PLACER 与活性相关"的证据实际建在表观活性上；② 前瞻只有 retro-aldolase 一个反应，"results in higher success rates" 的跨文佐证来自 [B17][B18]（正文引用），本文自己没做双臂对照（同一池子一半用 PLACER 选、一半不用——B2 行显示"including or skipping"两条选择策略并存，但正文没给两臂命中率对比数字，仅在补充里，本地未取）；③ pRMSD 是经验置信量，正文没给"pRMSD 多小算预组织好"的绝对阈值；④ 专利与商业化信息（"A provisional patent (Application No. 63/535,404) covering the PLACER network (formerly known as ChemNet) presented in this paper has been filed by the University of Washington"）提示代码可用范围需按仓库许可核对。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么做）**

1. **"用 MD 的理由和不用的理由"都要写进判据文档**：本文提供了本调研唯一的一手原文（§2.1）。我们的本库口径：MD 只做末端机理复核（少数候选、带可证伪问题），不做漏斗闸口；闸口若需要"分布/预组织"信息，走廉价系综路线而不是长时 MD。
2. **三级验证顺序**（晶体基准→已知梯度→前瞻）直接搬到我们判据的验收流程：任何酶设计打分器先在"文献已知做过/已知失败"的面板上验梯度（对应 [B09] 的 A 段思想），再上前瞻。
3. **"输入泄漏防线"**：设计评估器时必须把答案从输入里抹掉（本文连配体内部几何与朝向都要塌缩重加噪声）。我们评"催化位是否合理"的判据时，凡生成/召回阶段用过的信息（Foldseek 命中、已知 Asn 位点）不得再进打分输入。
4. **批内对照标尺**（90+6 的做法）：湿实验通量极小的我们更需要——每轮实验带已知行为对照构建体，把"批间可比"写进流程。

**不可迁移（为什么不能照搬）**

1. **PLACER 的输入前提我们不满足**：它要求给定可靠骨架坐标 + 完整化学图。候选酶的底物/过渡态结合态本身是待验证假设，拿"假设的结合态"去算预组织系综是自证（违反 §8-3 精神）。
2. **docking 成功率数字（82.4%/84% 等）不能当我们的概率**：那是"已知口袋摆已知配体"的问题；我们的问题是"该不该有这个口袋/这条链"，且 bing binder 类阈值（pAE 等）与本卡无任何换算关系（本库判据 §2）。
3. **11,000 M⁻¹min⁻¹ 是 retro-aldolase 的成绩**，与酶设计成键化学无机制通路对应；引用只许引用方法结构（系综、pRMSD、双档判据），不许引用活性数字做目标设定。

## 9. 溯源与自检

- 引句底稿: data/interim/baker_lit/ft/placer2025.txt（本卡全部英文引号片段的逐字比对对象）
- 本地全文：`data/interim/baker_lit/ft/placer2025.txt`（PMC12625923 XML 抽取纯文本，先行调研缓存；引句在 norm（实体解码+NFKC+空白折叠）后逐字命中）。
- 对照底稿：`sources/baker.md:251–263`（B19 原卡）；`sources/baker.md:5,39,658`（"2025 年 PLACER 论文明确以成本否弃它当主筛选器"与 MD 原文引用行）。
- 关联卡：[B18]（PLACER 作闸口的实战）、[B20]（上游生成器）、[B09]（A 段"筛子考卷"思想同源）。
- CSV 字段映射：本卡第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B19 --no-report` 输出 `PASS B19 quotes=N/N`。注意本卡把原文 "computationally expensive and cannot be applied to large numbers of designs" 一类跨括号引文编号的句子按原文连写摘录（norm 后逐字命中），未做跨句拼接；"×10 longer" 等含特殊符号处为复制原文。

<!--CSV回填
work_type=论文
target=蛋白-小分子复合物构象系综（配体 docking、金属/非标准残基、蛋白-DNA 界面侧链）；应用线为 retro-aldolase（NTF2 折叠）设计与预组织评估
backbone_generation=本文不生成骨架（输入端）：应用线用 RFjoint2 出 10,000 NTF2 骨架 + XML-Matcher 放催化四联体 + LigandMPNN 出序列 + AF2 单序列复折
computational_filters=PLACER 系综：pRMSD（逐原子不确定度合成）、催化侧链-配体几何距离、构象分布宽度；dock 排序用 pRMSD/pLDDT/pLDDT-pDE；可选 GALigandDock 物理极小化重打分
thresholds=折叠闸 lDDT>85（AF2 单序列模式，model ptm、3 recycles）；docking 双档 ligand RMSD<1 Å/<2 Å；防泄漏 ≥30% 序列同一性、Tanimoto ≥80%（Astex 检查另用 ≥0.5）；PLACER 预组织绝对阈值正文未给（SI 未取）
md_used=否（且是本文立论依据：MD 太贵不能当大规模筛选器，原句见 §2.1；MD 仅作为对照组引用）
qm_used=否（自身不做 QM；仅在综述对比中提到 GEOM-DRUGS 训练集来自半经验 QM）
experimental_methods=IVTT（eBlocks+PurExpress）半定量表观活性（90 设计+6 对照/批）；E. coli 表达、IMAC+SEC 纯化、Methodol 底物浓度梯度 Michaelis–Menten
pipeline_counts=训练：200,713→135,172→119,916（112,828 训练/7,090 验证）；基准：Astex 1,112 对×1,000 模型、PoseBusters 428×100 模型；应用线：10,000 骨架→17,810（lDDT>85）→320（PLACER+logistic regression 选人）→IVTT→24 纯化定量→cnRA-50
hit_rate=docking：Astex 82.4%(<2 Å)/41.8%(<1 Å)；PoseBusters 118 子集 84%(<2 Å)/51%(<1 Å)；酶侧正文未给 320 中活性数（IVTT 口径），以最优设计产出为结论
best_metric=cnRA-50 k_cat/K_M = 11,000 M⁻¹ min⁻¹（注意单位分钟制；优于前深度学习时代该反应所有计算设计）
cost_or_stat_note=架构试验放 CSD 因 PDB 收敛慢约 10 倍；PLACER 不预测骨架故远快于 AF2/AF3/RF；网络 8 共享迭代块、原子级图、氢不建模；大学临时专利申请（原代码名 ChemNet）
role_in_timeline=把"预组织"从 MD 的奢侈品变成每次几十条采样的廉价闸口：上游接 [B20] 的原子级生成，下游被 [B18] 用作 96 名额的排序器；同时给本调研提供"为什么 Baker 组主漏斗不用 MD"的原文依据
source_pointer=data/interim/baker_lit/ft/placer2025.txt（PMC12625923 抽取文本，57,491 B）；sources/baker.md:251-263
CSV回填-->
