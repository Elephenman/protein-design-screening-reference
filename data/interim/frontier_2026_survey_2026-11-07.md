# 前沿方法核验调研（2025-06 → 2026-11）
调研日期 2026-11-06/07 · 委托项目 `A:\Data\MD\projects\protein-design-screening-20261016`（蛋白设计筛选参考库，152 篇）
用途：判断库内是否已覆盖 2025–2026 主流前沿方法，并给出可直接抄进工作流模板的**能力边界 + 公开基准数字 + 失败模式**。
本文件只做调研与核验，**未修改项目内任何文件**。

---

## 0. 核验方法与取证级别（先读这段）

**只用这四类一手来源**：① 官方 GitHub 仓库 README（raw 文件直接下载）；② bioRxiv/arXiv 正文全文（HTML/PDF 抓取后本地检索）；③ 出版商/Europe PMC 索引记录（题录 + 摘要）；④ 官方文档站。未使用博客/推文/二手综述作为任何数字的依据。

取证级别标签（每条数字后都带）：
- `FT` = 读了正文全文，数字出现在正文句子里（可复检索，本地缓存见 §10）
- `ABS` = 只读到摘要（bioRxiv/arXiv/出版商摘要页），正文未取到 → 细节不可外推
- `README` = 只到官方仓库 README / 官方文档站，无论文正文

**检索式（可复跑）**：Europe PMC REST `search?query=...`、arXiv API `export.arxiv.org/api/query`、Crossref `api.crossref.org/works?query.bibliographic=`、GitHub Search API + `raw.githubusercontent.com`。
对 §6 的六个"疑似不存在"名称，四个来源**全部返回 0 条**（不是"我没查到"，是接口显式 `hitCount=0 / total=0`）。

**库内已有 vs 本次新发现**（用于回答"哪些值得进模板"）：
库内已覆盖：RFAA[B13]、RFdiffusion2[B20]、RFdiffusion3 预印本[B35]、ProteinMPNN[B05]、LigandMPNN[B28]、RFpeptides[B15]、PLACER 丝氨酸水解酶[B17]、metallohydrolase[B18]、dTERMen[C05]、Kemp 完整计算设计[K63]、催化基序脚手架[K64]、IMUSE[C23]、近红外荧光蛋白[M-K34]、扩散模型综述[K38]、"最后一公里"打分批判[K34]。
**库内没有、本次新确认**：RF3 / AtomWorks / Foundry / RFO；Boltz-1 / Boltz-2（含全部第三方亲和力评测）；Chai-1 / Chai-2；OpenFold3 / OpenBind / ABCFold / AntiConf；ESM3 / ESMC / ESMFold2 / ESM Atlas；AlphaProtein Novo；CaGE；Metal Mer；Multistate enzyme design；RFD3 的 Science 正式版；Latent-X；SeedProteo；epitope excision + agent 设计；Promera；BoltzProt-1。

---

## 1. Baker / RosettaCommons：RF3、RFAA、RFSolo、Foundry 默认组合

### 1.1 Foundry = 2025 之后的官方装配线（回答"RFdiffusion+ProteinMPNN+RF3 是否成默认"）
一手来源：`https://github.com/RosettaCommons/foundry`（README，取于 2026-11-07）`README`
- 原文定位：README 首句即声明 Foundry 覆盖"design (RFD3)、inverse folding (ProteinMPNN)、protein folding (RF3)"三类模型，全部依赖 AtomWorks（`https://github.com/RosettaCommons/atomworks`）做训练与推理的数据层。
- 官方安装/权重：`pip install "rc-foundry[all]"` → `foundry install base-models`（一次装最新 RFD3 + RF3 + MPNN）；官方镜像 `rosettacommons/foundry`（Docker Hub）。
- **默认流程的直接证据**：README 提供 Google Colab "IPD Design Pipeline Tutorial"，标题写明是"a basic design pipeline with **RFD3, MPNN, and RF3**"——即 IPD 自己把这三件套作为对外教的默认链。`README`
- **第四个组件 RFO（RFOptimization）**：README 定义为"RF3 梯度引导序列优化 + **Boltz-2 结构预测** + 外部 ProteinMPNN/LigandMPNN 重设计"。这条很关键：Baker 官方工具链自己已经把第三方 Boltz-2 用作打分/验证环节，不是只用自家 RF3。`README`
- 附带事实：RFdiffusion3NA（核酸版）挂在同一预印本 DOI 的不同版本上（`10.1101/2025.09.18.676967v3`）。`README`

**能证明**：2025-H2 起，Baker/IPD 的公开默认组合确实是 **RFD3(骨架+全原子条件) → MPNN/LigandMPNN(序列) → RF3(复折与置信度)**，且官方承认在打分位引入 Boltz-2。
**不能证明**：不能证明"所有 Baker 组论文都按这个组合做"（各组仍按课题选 Chai-1/AF2/AF3 复折，见库内 B17/B20 用的是 Chai-1）。
**尚缺什么**：缺一份同口径对比"RFD3+MPNN+RF3 vs RFdiffusion1+MPNN+AF2 闸口"的湿实验命中率文献——没有它，模板里只能写"官方默认"，不能写"实测更优"。

### 1.2 RF3（这才是"AF3 类开源权重"）
一手来源：Corley A, Mathis S, Krishna R, et al. **"Accelerating Biomolecular Modeling with AtomWorks and RF3"**, bioRxiv 2025-08-14, DOI `10.1101/2025.08.14.670328` → https://doi.org/10.1101/2025.08.14.670328 （EPMC PPR1068521，正文已读 `FT`）
权重：`http://files.ipd.uw.edu/pub/rf3/rf3_foundry_01_24_latest_remapped.ckpt`（BSD 许可，见 README）；三个检查点：**Latest(01/24)**、**Preprint(01/24)**、**Benchmark(09/21 训练截断，用于同截断对比)**。`README`+`FT`

量化表现（来源 `10.1101/2025.08.14.670328` `FT`；分母 = 自建非冗余测试集，按 40% 序列同一性/CCD 同一性聚类；均为 in silico，无湿实验命中）：
| 指标 | RF3 | AF3 | Boltz | 口径 |
|---|---|---|---|---|
| 定位 | 介于 AF3 与开源 Boltz 之间，"almost all categories" | 最高 | 开源基线 | 正文 §"narrows the gap" `FT` |
| 蛋白-蛋白界面中位 lDDT | 0.607（截断 01/24）/ 0.571（09/21） | — | — | 同测试集 `FT` |
| 蛋白-配体界面中位 lDDT | 0.798 / 0.766 | — | — | `FT` |
| 蛋白-DNA 界面中位 lDDT | 0.523 / 0.415 | — | — | `FT` |
| RNA-only 中位 lDDT | 0.772 / 0.765 | — | — | `FT` |
| 手性中心正确率 | **88%** | **84%** | **76%**（Boltz-2，不加推理引导） | 测试集配体手性中心，按 CCD 聚类取均值，t 检验 `FT` |
| 距离条件收益 | 蛋白-配体界面 0.821 → 0.882 / 0.890；给定模板配体时中位 ligand-only lDDT **0.991** | — | — | `FT` |
成本/吞吐（可直接进模板）：`num_steps` 200→50 精度不降、速度提升 >2×；`early_stopping_plddt_threshold` 默认 0.5，开启后结构产出提升 **10–20×**（作者原话"we see no deterioration in performance with 50 steps"）。`README`

**流程位置**：替换/补强"复合物结构预测 + 复折自洽性验证 + 置信度打分"这一步；AtomWorks 同时是数据/特征层（结构预测、生成式设计、固定骨架序列设计三任务共用）。

**已知失败模式 / 作者自述局限**：
- 无 MSA 时模型会**早停**（只出 `.score`，不出结构文件）——用作批量筛除时，"没结构"不等于"结构差"，模板里必须把 early_stopped 单独建一列。`README`
- 自定义配体若与 CCD 内配体同名，"**the prediction will be catastrophically wrong**"，必须重命名（建议前缀 `L:`）。`README`
- 论文正文中出现的自家设计阈值得抄就抄：`pDE ≤ ln(0.075·length)` + `pLDDT ≥ 0.62` + `pAE ≤ 15`（设计筛选）；蛋白-DNA 复折用 `mean pLDDT > 80` + `mean interface PAE < 10`。`FT`
- 局限：作者明确"AF3 论文未写全训练细节，我们自述的训练流程供复现参考"（附录 A.3.2），即** bitwise 复现 AF3 不成立**，只能"接近"。

### 1.3 RFAA
一手来源：Krishna R, et al. **"Generalized biomolecular modeling and design with RoseTTAFold All-Atom"**, Science 2024, DOI `10.1126/science.adl2528`（库内 **[B13]** 已建卡，PMID 38452047）。仓库 `https://github.com/baker-laboratory/RoseTTAFold-All-Atom`（创建 2023-12-19，最近推送 2026-05-18）。
**结论：RFAA 属于 2024-03 的开源事件，不是 2025-06 的 AF3 类权重发布**；2025 年那一次开源事件的名字是 **RF3 + AtomWorks**（§1.2）与 **RFD3**（§1.4）。你原问题里"2025-06 前后开源的 AF3 类权重"应改写成"RF3，2025-08-14 预印本 + BSD 权重"。
**能证明**：RFAA 已被 RF3 在同架构上取代（Foundry 只列 RF3，不再列 RFAA）。
**不能证明**：RFAA 与 RF3 的同基准数值差（未见任何一手对比表）。
**尚缺什么**：一张 RF3 vs RFAA 的同截断界面 lDDT 对比。

### 1.4 RFSolo —— **未找到该名称的一手来源**
EPMC `ABSTRACT:"RFSolo"` → hitCount 0；arXiv `all:"RFSolo"` → 0 条；GitHub 仓库搜索 → 0；Crossref → 0；且 Foundry 与 RF3 的全部 README/检查点清单里没有该名字。
**处置**：模板里不要出现 RFSolo。若要写"单序列/无 MSA 模式"，RF3 侧的真实说法是 early stopping + `num_steps` 降步；ESMFold2 侧的真实说法是 single-sequence mode（见 §5）。

### 1.5 RFdiffusion3 已见刊（库内 B35 需从"预印本"升级为"已刊"）
一手来源：**Butcher J, Krishna R, Mitra S, Woodbury N, Kim, Brent 等. "Atomic functional site scaffolding in biopolymers with RFdiffusion3." Science 2026, DOI `10.1126/science.aeh2982`, PMID 42879533** → https://doi.org/10.1126/science.aeh2982 `ABS`（Science 订阅墙，正文未取到；预印本正文在库内 B35）
摘要级实测声明：设计 de novo **磷酸三酯酶**（含氨基甲酰化 Lys 配位两个金属离子的复杂活性位）**和** 针对转甲状腺素蛋白（TTR）的 **锌蛋白酶**，"in both cases we obtain active catalysts in **zero shot 96 construct design campaigns**"。`ABS`
**能证明**：全原子约束设计能在 96 个构型的零样本批次里直接拿到活性催化剂（分母=下单 96 孔，非 in silico）。
**不能证明**：具体命中率数值与催化效率数值（摘要未给）。
**尚缺什么**：正文表格（需订阅或找作者）。

---

## 2. Boltz 系列（MIT，权重+训练码全开）

### 2.1 Boltz-1
一手来源：Wohlwend J, Corso G, Passaro S, et al. **"Boltz-1: Democratizing Biomolecular Interaction Modeling"**, bioRxiv 2024-11-19, DOI `10.1101/2024.11.19.624167`（EPMC PPR943186）→ https://doi.org/10.1101/2024.11.19.624167 `FT`
仓库：`https://github.com/jwohlwend/boltz`（README 明写 code+weights **MIT**，可商用）。`README`
定位：第一个"完全开源 + 达到 AF3 级精度"的复折叠模型；新增 **Boltz-steering**（推理期物理势引导），Boltz-1x/2x 即带 steering 的发布版，用于修 hallucination 与非物理预测。`FT`
正文里同时留了一句重要的口径警告：与 AF3 论文数值对比时，"these differences may simply be the result of **reporting mistakes in the current version of the original manuscript from Abramson et al.**"——即 AF3 论文数值本身可能有问题。`FT`

### 2.2 Boltz-2（存在，且是"结构+亲和力"联合模型）
一手来源：Passaro S, Corso G, Wohlwend J, et al. **"Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction"**, bioRxiv 2025-06-14, DOI `10.1101/2025.06.14.659707`（EPMC PPR1039145）→ https://doi.org/10.1101/2025.06.14.659707 `FT`
作者列表：Passaro, Corso, Wohlwend, Reveiz, Thaler, Somnath, Getz, Portnoi, Roy, Stark, Kwabi-Addo, Beaini, Jaakkola, Barzilay（MIT）。

**两个输出头要分清（README 原文定义，模板必须写死）**：`README`
- `affinity_probability_binary` ∈ [0,1]：判"结合/不结合"，用于 **hit discovery（活性物 vs 诱饵）**；
- `affinity_pred_value` = **log10(IC50)，IC50 以 µM 计**：用于 **hit-to-lead / lead optimization 的排序**；两者训练数据与监督不同，不可混用。

亲和力公开基准（数字后标分母口径）：
| 测试集 | Boltz-2 数值 | 对照 | 分母/口径 |
|---|---|---|---|
| FEP+ 4-target 子集 | 平均 **Pearson 0.66** | "outperform all available inexpensive physical methods and ML baselines"；逼近 SOTA FEP，算力快 **>1000×** | in silico 基准，训练集已剔除与 FEP+ 有 ≥90% 同一性的蛋白 `FT` |
| OpenFE 全量 | "approaches the performance of OpenFE"（未给单值） | 开源相对 FEP | in silico `FT` |
| **CASP16 亲和力 track** | "outperforms all top-ranking participants by a clear margin"，零微调、无输入整理 | 盲测竞赛提交方 | **140 个蛋白-配体对 / 2 个靶点**，盲测 `FT` |
| Recursion 8 个内部盲测 assay | **3/8 个 assay Pearson > 0.55，其余 5 个表现有限** | 其他 ML 基线被明显超过 | **真实药化项目**，非公开 `FT` |
| MF-PCBA（hit discovery） | AP 与 EF（K=0.5/1/2/5%）"substantially outperforms docking 与 ML" | docking / ML | 回顾性公开集 `FT` |
| TYK2 虚拟筛选 | 屏幕打分 vs ABFE ΔG **|R| = 0.74**；该靶点蛋白-配体基准上 Pearson R=0.83 | Boltz-ABFE：R=0.95、cMAE 0.42 kcal/mol、偏置 0.92 kcal/mol | **全部为计算验证（ABFE 代理），非湿实验命中** `FT` |
| 结构精度（2024–2025 新提交 PDB 非冗余集） | "matches or moderately improves over Boltz-1；略胜 Chai-1/ProteinX，但**落后 AlphaFold3**"；抗体-抗原明显改善 | AF3/Chai-1/ProteinX/Boltz-1 | in silico `FT` |

**失败模式 / 作者自述局限（§6 Limitations 逐条，`FT`）**：
1. **口袋错→亲和力必然不可信**："If the model fails to identify the correct pocket or inaccurately reconstructs the binding interface … downstream affinity predictions are unlikely to be reliable."
2. **辅因子/离子/水/多聚体伴侣不进亲和力模块**："the affinity module does not explicitly handle such cofactors, including ions, water, or multimeric binding partners."（这条对酶设计工作流是硬约束）
3. **crop size 截断长程相互作用**（正构+别构并存时尤其危险）。
4. **跨 assay 性能方差大**："the performance varies strongly between assays"，作者不知道来源（结构误差？蛋白家族泛化？小分子分布外？）。
5. 系综/MD 不占优：与 AlphaFlow / BioEmu "no significant deviation"。
6. 结构预测相对前代没有大跳（同一训练数据 + 同一架构），"still often fails to capture large conformational changes, such as those induced by binding"。
7. 非物理位形问题在 §2.1 由 Boltz-steering 处理（Boltz-2x 物理性指标显著更好），意味着 **默认 Boltz-2 输出不保证物理合理**。

**独立第三方评测（负面为主，全部一手来源）**
- Wan S, Zhang X, Xue X, Coveney PV. **"On the Reliability of AI Methods in Drug Discovery: Evaluation of Boltz-2 for Structure and Binding Affinity Prediction"**, arXiv 2026-03-02, `https://arxiv.org/abs/2603.05532`；已见刊 **J. Chem. Theory Comput. 2026, DOI `10.1021/acs.jctc.6c01334`, PMID 42579383（PMC13472093，正文已读）** `FT`
  - 分母：**16,780 个化合物（3CLPro）+ 21,702 个（TNKS2）**，对照 = ESMACS 物理自由能（非实验湿测）。
  - 数值：TNKS2 **Pearson r = 0.45 / Spearman ρ = 0.46**；3CLPro **r = 0.24 / ρ = 0.25**；**top-100 精选子集相关系数≈0**（作者：top-100 内预测值方差被压到 <1.0 kcal/mol，小于模型内在不确定度，数学上必然塌相关）。
  - 两个头自相矛盾：亲和力值 vs 结合概率之间 Pearson 仅 **0.21（3CLPro）/ 0.25（TNKS2）**；"almost all compounds are predicted by Boltz-2 to have binding affinities below −4 kcal/mol"（即数值端严重压缩/饱和）。
  - 可复现性很好（两次独立重跑 r = 0.913 / 0.962）——**问题不在噪声，在分辨率**。〔`10.1021/acs.jctc.6c01334` `FT`〕
  - 作者结论原话级：Boltz-2 "offers substantial speed for initial screening, it **lacks the energetic resolution required for lead identification**"。
- **Benchmarking Boltz-2 for Screening of Therapeutic Antibody-Antigen Interactions**, bioRxiv 2026-05-13, DOI `10.64898/2026.05.13.724924` `ABS`
  - 分母：**519 个治疗性单抗**（Thera-SAbDab），每个配对同源抗原 + 一个随机非同源抗原。
  - 数值：Boltz-2 置信度指标判别力 **0.5 < ROC-AUC < 0.60**（"weak, though above chance"）；最强指标是 seed 采样间的 **ipTM-min**；多特征聚合/多变量建模"little to no improvement"；随机采样收益在 **~15–20 个 seed** 之后明显递减；**不喂 MSA 反而略好**（ΔAUROC ≈ +0.027）且省 ~8 s/条。〔`10.64898/2026.05.13.724924` `ABS`〕
  - 结论原话级：通用结构预测模型的现成置信度指标"may be **insufficient** for reliable target-antibody screening"。
- **A Medicinal Chemistry-Centered Evaluation of AlphaFold 3 and Boltz-2 Across Diverse Binding Modalities**, bioRxiv 2026-08-24, DOI `10.64898/2026.08.24.746785` `ABS`
  - 分母：新解的可溶性环氧水解酶共晶结构 + 配套活性数据 + 一个"训练截断之后"的策展集（激酶、别构、共价、PROTAC、分子胶、片段、膜蛋白、RNA 结合、活性悬崖对）。
  - 能用的正向数字：**AF3 minPAE < 0.85 Å 强烈富集正确构象**（可当位姿门阈）。〔`10.64898/2026.08.24.746785` `ABS`〕
  - 关键负面：**"Model confidence scores were not associated with experimental activity"**；Boltz-2 亲和力能抓相对活性趋势、能分辨那对活性悬崖，但跨系列表现不稳。
  - 失败模式：别构、膜蛋白、诱导邻近复合体仍是硬伤；正交位点酶/激酶复合物（含 DFG/αC 态）能还原。
- **Adapting Boltz-2 with limited experimental activity data improves early enrichment in virtual screening**, arXiv 2026-09-21, `https://arxiv.org/abs/2609.24302` `ABS`
  - 分母：8 个 MF-PCBA 靶点，回顾性；微调亲和力头用 40–300 条二值活性标签。
  - 数值：300 条标签时，**top 1% 内活性物数量几何均值 ×1.77，AP ×2.14**（对照=不微调）；只对 top ~10% 候选重打分即可保住大部分收益。〔arXiv `2609.24302` `ABS`〕→ **模板可写成"有 ≥百条本靶标活性数据就微调亲和力头并重排 top 10%"**。
- **On fine-tuning Boltz-2 for protein-protein affinity prediction**, arXiv 2025-12-06, `https://arxiv.org/abs/2512.06592`（MLSB 2025）`ABS`
  - 分母：TCR3d 与 PPB-affinity 两个公开集。
  - 负面结论：结构精度很高，但 **Boltz-2-PPI 在小样本与更大样本两种设定下都输给序列型基线**；结构嵌入与序列嵌入互补。原话："current structure-based representations are **not primed for performant affinity prediction**"（蛋白-蛋白）。
- 工具类：**Boltzina**（arXiv `2508.17555`，docking-guided 虚拟筛选）、**Boltz-ABFE**（arXiv `2508.19385`，无晶体结构的 ABFE）、**BoltzOmics**（`10.1016/j.isci.2026.116797`）、**Biasing Conformational Sampling in AF3/Boltz-2 via Pair Representation Scaling**（`10.1021/acs.jcim.6c02094`）。均 `ABS`。

**流程位置**：Boltz-2 同时替换"复合物结构预测"和"亲和力打分"，并首次给了**分类头**（结合/不结合）供 hit discovery 用。

**三态判定**
- **能证明**：Boltz-2 的亲和力在小分子-蛋白上确实达到"逼近 FEP、快 1000×"的量级（4-target FEP+ Pearson 0.66；CASP16 亲和力 track 140 对盲测超全部参赛方案），并且**系列内相对排序可用**（能分辨活性悬崖对）。
- **不能证明**：不能证明它可以当**绝对门槛**或**跨系列/跨靶标判据**（top-100 相关塌到 ≈0；Recursion 5/8 个内部 assay 表现有限；抗体-抗原方向置信度 AUC 仅 0.5–0.6；PPI 亲和力回归输给序列基线）。TYK2 那条"高亲和力"是 **ABFE 模拟代理**，没有任何湿实验命中。
- **尚缺什么**：缺一个把 Boltz-2 亲和力直接放进**蛋白设计漏斗**（而非小分子 VS）并报告"命中率随阈值变化曲线"的前瞻性一手研究；缺 15-PGDH 那条负面案例的一手 DOI。

---

## 3. Chai 系列

### 3.1 Chai-1（结构预测，**不预测亲和力**）
一手来源：Chai Discovery（Boitreaud, Dent, McPartlon, Meier, Reis, Rogozhnikov 等）。**"Chai-1: Decoding the molecular interactions of life"**, bioRxiv 2024-10，DOI `10.1101/2024.10.10.615955`（EPMC PPR922953）→ https://doi.org/10.1101/2024.10.10.615955 `FT`
仓库：`https://github.com/chaidiscovery/chai-lab`（README，`pip install chai_lab==0.6.1`；权重**非商用**，网页版可商用）`README`
关键量化（分母都写清）：
- 蛋白-蛋白界面：在 **1054 个 PDB 结构 → 4120 个界面 → 聚成 929 个界面簇**的低同源性子集上，DockQ>0.23 成功率 **0.751 vs AF-Multimer 2.3 的 0.677**（Wilcoxon p = 6.24×10⁻¹⁰）；不给模板时 0.743（差异不显著）。`FT`
- 实验约束提示：单条抗体-抗原距离约束（θ ≤ 15 Å）使 DockQ acceptable 比例 **35% → 57%**；给 4 个随机表位残基使成功率"more than doubles"，但高质量预测比例仍然低。`FT`
- 单序列模式（不给 MSA）保留大部分性能，并优于 ESMFold，某些评测下甚至优于带 MSA 的 AF-Multimer2.3。`FT`
- 训练截断 **2021-01-12**（比 AF3/Boltz 早很多，做时间外对比时必须记住）。`FT`
失败模式（一手，第三方独立）：**BepiPocket / DiscoPocket**, Protein Science 2026, DOI `10.1002/pro.70730`, PMID 42489170, PMCID PMC13393073 —— 在 **1628 个抗体-抗原复合体**上，标准 Chai-1 建模的典型失效是"**把抗体放错抗原位置，并反复收敛到同一种冗余结合模式**"；用 BepiPred-3.0（序列）或 DiscoTope-3.0（结构）做表位约束能同时提高**准确率与多样性**。`ABS`（正文未读，摘要含数字）

### 3.2 Chai-2（**是设计模型，不是亲和力模型**）
一手来源 #1：**"Zero-shot antibody design in a 24-well plate"**, bioRxiv 2025-07-05（Date 2025-06-30），DOI `10.1101/2025.07.05.663018`（EPMC PPR1048062）→ https://doi.org/10.1101/2025.07.05.663018.full `FT`（正文已读）
一手来源 #2：**"Drug-like antibody design against challenging targets with atomic precision"**, bioRxiv 2025-11-29, DOI `10.1101/2025.11.29.691346`（EPMC PPR1128296）`ABS`
分母与数字（这是本次最适合进模板的一组，因为分母是"下单量"）：
- 抗体/纳米抗体：**52 个新抗原**（PDB 里原本没有任何已知抗体/纳米抗体结合剂），每靶点 **≤20 条设计**；平均实验命中率 **15.5%**（**VHH 20.0%，scFv 13.7%**）；**26/52（50%）靶点至少拿到 1 条确认结合剂**；作者称较此前 SOTA 提升**两个数量级**，并明确"此前 de novo 抗体设计的实验室成功率**通常 <0.1%**"。`FT`
- 命中判据（可直接抄的阈值）：BLI 信号 **> 背景 + 0.1 nm 且 > 背景的 300%**。`FT`
- 小蛋白（miniprotein）：**5 个靶点**（PD-L1 25 条、IL-7Rα 23、InsulinR 20、TNFα 22、PDGFRβ 21，另每靶点跑原型模型 Chai-1d 20 条），**湿实验成功率 68%**，对每个靶点至少比次优方法好 3×，并给出（据称）首个计算设计出的 TNFα 结合剂；K_D 分布：IL-7Rα/PD-L1/PDGFRβ/InsulinR 达 **皮摩尔级**，TNFα 为低纳摩尔；含一条几乎全 β 的单-digit nM PDGFRβ 结合剂。`FT`
- 周期：从表位到湿实验确认 **< 2 周**；表达用 E. coli 无细胞体系（miniprotein 8 µL/12 h，scFv/VHH 1 mL/3 h），mini 用 Twin-Strep 荧光定量归一、抗体用 Ni 柱 + OD280。`FT`
- 第二篇（`ABS` 级）：全长单抗 **>86% 通过 developability 谱**（与治疗性抗体同级）；实验结构与其 in silico 预测相符；示范 GPCR 激动型抗体与肿瘤新表位选择性抗体。
- 第三方引用数值：BoltzProt-1（§7.6）称 Chai-2 在其所用的 10 靶点子集上"previously reported 6/10"。`ABS`（二手转述，不可当作 Chai 的官方数字）
**作者自述局限（原话结构，`FT`）**：① 所有结合数据都在 **scFv/VHH 格式**上取得；scFv 的亲和力与同一可变区改成的 Fab/全长 IgG **可能不同**，且 scFv 结合不总平移到 Fab；② 为确认打中预期表位，还需要**竞争结合实验 + 实验室三维结构**；③ 交叉反应性（human/cyno）不是靠打同一表位就自动拿到（部分结合剂只绑一种同源物）。
未见 Chai-2 自身发表系统性失败模式清单；本轮也没找到独立的 Chai-2 复现论文（EPMC 检索 0 条独立复现，见 §7.6 的 BoltzProt-1 属竞品对比）。

**"预测结合亲和力能否用于排序/筛选"的证据（针对 Chai）**：Chai-1/Chai-2 都**没有**亲和力头（Chai-1 正文无该功能；Chai-2 是设计模型），所以对 Chai 只能引用它的**置信度/约束提示**用法，不能引用亲和力排序能力。这一条要在模板里写死，防止有人把 Boltz-2 的用法套到 Chai 上。

**三态判定（Chai 系列）**
- **能证明**：Chai-1 的约束提示增益有可复算数字（DockQ acceptable 35%→57%；PP 成功率 0.751 vs AF-Multimer2.3 的 0.677，分母 929 个界面簇）；Chai-2 的湿实验命中率是分母最干净的一条（52 靶点 × ≤20 设计 = 下单量即分母，15.5%、26/52、miniprotein 68%）。
- **不能证明**：不能证明 Chai-2 的 scFv/VHH 命中率可平移到**全长 IgG**（作者自列为局限）；不能证明 Chai 系列有亲和力排序能力（无该头）。
- **尚缺什么**：缺第三方对 Chai-2 的独立复现（本轮 EPMC 检索独立复现 0 条，只有竞品 BoltzProt-1 的转引"6/10"）；缺 Chai 与 RF3/Boltz-2 在同一设计漏斗末端（下单→命中）的同口径对比。

---

## 4. 第三方复现：OpenFold3、ABCFold、AntiConf；"PoseChains" 未找到

### 4.1 OpenFold3（存在，AF3 的开源复现，但只有技术报告 PDF，无 arXiv 论文）
一手来源：`https://github.com/aqlaboratory/openfold-3`（README，取于 2026-11-07）`README`
- 官方定位：**"a biomolecular structure prediction model aiming to be a bitwise reproduction of DeepMind's AlphaFold3"**，AlQuraishi Lab（Columbia）+ OpenFold consortium，**Apache-2.0，学术与商用皆可**。
- 版本与权重命名（模板里要用这套名字）：`OpenFold3-preview`（pip 包 `openfold3`）；**OF3p1** = `of3_ft3_v1.pt`（openfold3 0.3.x）；**OF3p2** = `of3-p2-155k.pt`（openfold3 ≥ 0.4.0，检查点约 2.3 GB）；`>=0.5.0` 默认参数换成 **OpenBind-0**（"forthcoming OpenFold3 architecture"，**训练截断 2025-06**），官方 README 明确建议日常使用 OpenBind-0 而非 OF3p2。
- 技术报告（PDF，未读）：`https://portal.openfold.omsf.io/reports/of3p2_technical_report.pdf`；门户 `https://portal.openfold.omsf.io`（含训练数据、复现 AF3 的 13M MGnify 蒸馏集）。
- **重要一手陷阱**（来自第三方仓库 README，属一手技术文档）：`aqlaboratory/confornets` 记录 **OF3p1 与 OF3p2 检查点互不兼容**，`openfold3==0.3.1` 才能复现某篇论文的数值，且他们声明将重跑基准——即**OpenFold3 的不同参数集之间数值不可横向比较**。`README`

一手评测（OpenFold3 的公开能力边界）：
- **Systematic Evaluation of AlphaFold2 and OpenFold3 on Protein–Peptide Complexes**, bioRxiv 2026-04-21, DOI `10.64898/2026.04.21.720042` `ABS`
  - 分母：**271 个非冗余蛋白-肽复合体**，CAPRI 肽判据，分内在无序(IDR)/结构型(Non-IDR)两子集。
  - 数值/结论：整体成功率与高质量比例上 **AF2 一致优于 OF3**；两者全局折叠精度相当；**AF2 在其训练集里已有的蛋白-肽复合体上表现出记忆效应（memorization）**；对 AF2 最可靠的置信代理是 **pDockQ2、LIS、ipSAE**（PAE 派生指标），而 **OF3 的 PAE 分布大幅削弱了派生分数的判别力**；**蛋白-蛋白的 DockQ 阈值不能直接搬到蛋白-肽**。〔`10.64898/2026.04.21.720042` `ABS`〕
- **The first OpenBind release**, bioRxiv 2026-08-27, DOI `10.64898/2026.08.27.747600` `ABS`
  - 分母：肠道病毒 2A 蛋白酶，**925 个晶体学结合事件 / 699 个化合物 / 601 个化合物的亲和力**——据称最大公开单靶标"结构-亲和力"集。
  - 结论：对接表现强依赖结合口袋构象；**构象难以排序**；结构法亲和力预测仍然难；**用片段筛选阶段的晶体结构微调 OpenFold3-p2，能显著改善后续化合物的位姿预测与虚拟筛选**。→ 模板可写"早期实验结构 → 本靶标微调共折叠模型"这一步。
- **resTrain**（把距离先验注入 distogram，适用 AF2 与 OpenFold3），bioRxiv `10.64898/2026.07.02.736010`；**ConforFlux**（Boltz-2 推理期多构象引导，覆盖 OpenFold3/Protenix），`10.64898/2026.05.16.725138`（默认 500 采样未出现的 inward 态可被采到；per-state 成功率 +3–17 个百分点，代价是 clashscore 上升）。`ABS`

### 4.2 "PoseChains 类"——**未找到该名称的一手来源**
EPMC（TITLE/ABSTRACT）、arXiv（all）、Crossref、GitHub 仓库搜索：四路全部 0。
**处置**：模板里改用真实存在的同类基准名 —— **PoseBusters**（Buttenschoen et al., Chem. Sci. 2024, DOI `10.1039/d3sc04185a`，被 Boltz-2 正文引用为其物理性缺陷依据）、Foldbench（ESMFold2 README 引用）、SAbDab/Thera-SAbDab、MF-PCBA、mdCATH/ATLAS（Boltz-2 的 MD 基准）。

### 4.3 其他第三方（一句话级，均可点）

**三态判定（第三方复现类）**
- **能证明**：OpenFold3 确实是 AF3 的开源 Apache-2.0 复现并有版本体系（OF3p1/OF3p2/OpenBind-0，训练截断 2025-06），且**已被独立评测证明弱于 AF2 于蛋白-肽任务**（271 复合体，成功率与高质量比例一致劣于 AF2）；OpenBind-0 用早期实验结构微调能改善位姿预测与虚拟筛选。
- **不能证明**：不能给出 OpenFold3 vs AF3 vs RF3 的同基准数值差（其技术报告 PDF 本轮未读）；不能证明 OpenFold3 在**设计筛选闸口**上有已发表表现。
- **尚缺什么**：OpenFold3 技术报告（`portal.openfold.omsf.io/reports/of3p2_technical_report.pdf`）的数值表；一份把 OpenFold3/RF3/Boltz-2/Chai-1 放进同一设计漏斗的同口径横评。
- **ABCFold**: Elliott LG, Simpkin AJ, Rigden DJ. *Bioinformatics Advances* 2025, DOI `10.1093/bioadv/vbaf153`, PMID 40708869, PMCID PMC12287924（正文已读）→ 一个输入 JSON 同时驱动 **AF3 / Boltz-1 / Chai-1**，统一链重排、统一排序、可视化**位阻冲突**。仓库 `https://github.com/rigdenlab/ABCFold`。`FT`（工具论文，无新精度数字）
- **AntiConf**: *Briefings in Bioinformatics* 2026, DOI `10.1093/bib/bbag137`, PMID 41903187 —— 抗体-抗原复合物置信度打分新指标（precision-driven）。`ABS`
- Ligo Biosciences 的 AF3 社区复现（Boltz-1 正文引用为 `https://github.com/Ligo-Biosciences/AlphaFold3`）——说明"AF3 复现"至少有两路官方级实现（OpenFold3、Ligo）。`FT`（引自 Boltz-1 参考文献）

---

## 5. ESM3 与统一多模态生成路线

### 5.1 ESM3 本体
一手来源：Hayes T, Rao R, Akin H, Sofroniew W, Oktay K, Lin Z 等。**"Simulating 500 million years of evolution with a language model"**, *Science* 2024, DOI `10.1126/science.ads0018`, PMID 39818825 → https://doi.org/10.1126/science.ads0018 ；预印本正文全文 `10.1101/2024.07.01.600583`（已读）`FT`；仓库 `https://github.com/Biohub/esm`（原 evolutionaryscale/esm，已重定向），ESM3 专页 `_assets/ESM3_README.md`（已读）`README`

**湿实验结果的全部可核数字（这就是你问的"有多少"）**（以下条目均出自预印本正文 `10.1101/2024.07.01.600583` `FT`；结论句另见 Science 摘要 `10.1126/science.ads0018`）：
- 模型规模：最大 98B，训练 **1.07×10²⁴ FLOPs / 27.8 亿蛋白 / 7710 亿 token**；GFP 设计全部用 **ESM3 7B 基础模型、无微调**，生成时禁止解码半胱氨酸。
- **实验 1**：**96 孔板上的 88 条设计**（按序列相似度分桶各取 top），E. coli 表达、485 nm 激发测荧光 → 得到多条与天然 GFP 相似度较高的亮设计，其中 **B8** 与模板 1QY3 序列同一性仅 **36%**，为弱命中（后续复测显示"比天然 GFP 暗 **50×**"）。
- **实验 2**：以 B8 序列为起点做 chain-of-thought 迭代 → 得到多条亮 GFP，最佳 **C10 = esmGFP**。esmGFP：与 *A. victoria* GFP **36% 同一性**、与最近已知荧光蛋白 **58% 同一性**（相对 tagRFP **96 个突变**）；亮度落在天然 GFP 分布内，但**成熟更慢**（0/2/7 天三点测），2 天后达到可比亮度；T65G/Y66G 色基敲除使其荧光回落到背景（证明机制）；与 Anthozoa 类 FP 平均 51.4% 同一性；作者用序列同一性→时间标尺估计"相当于 **5 亿年以上**天然演化距离"。
- **口径必须写清**：这是"**一次功能类别（GFP）的湿实验验证**"，不是命中率统计：设计→下单 88+（实验 2 具体条数在图/附表，摘要与正文主体未给整数），命中=1 条明亮（esmGFP）+若干较近缘的亮设计。**没有** ESM3 的抗体/结合剂湿实验命中数字。
已知局限（一手，第三方）：**"More Structure, Less Accuracy: ESM3's Binding Prediction Paradox"**, bioRxiv `10.1101/2024.12.09.627585` —— 给 ESM3 逐个变体喂不同松弛结构会让结合预测**变差**，喂同一致结构才提升；作者直接"建议谨慎"。`ABS`

### 5.2 是否停更/改名（一手事实，别用记忆）
- 仓库 README 现在的标题是 **"A world model of protein biology: ESMC, ESMFold2, & ESM Atlas"**，并单列一句"For information on using ESM3, see the ESM3 README"（ESM3 文档被降级为 `_assets/ESM3_README.md` 附属页）。开源权重只有 **esm3-sm-open-v1（1.4B）**在 HuggingFace `biohub` 集合里，"Other weights are available when the model is accessed through Biohub"（即 98B/7B 旗舰需走平台）。`README`
- 组织名：**EvolutionaryScale → Biohub**（GitHub 组织与 HF 命名空间均为 `biohub`，文档链接 `biohub.ai`）。这是可核的仓库/平台事实；至于"公司停更/团队迁移"的商业叙事，**我未找到一手来源，模板里只写"ESM3 已被 ESMC + ESMFold2 取代，发布方署名 Biohub"**。
- 后继一手来源：**"Language Modeling Materializes a World Model of Protein Biology"**, bioRxiv 2026-06-03, DOI `10.64898/2026.06.03.729735`（EPMC PPR1245895）`ABS`+`README`
  - ESMFold2（基于 ESMC-6B）在 **Foldbench 的蛋白-蛋白与抗体-抗原复合物 DockQ pass-rate 上超过既有方法**，可单序列模式运行换取"一个数量级"提速；
  - **湿实验**：README 原文"ESMFold2 is validated in the lab across **five therapeutic targets**"，用 ESMFold2 反演（inversion）生成 de novo miniprotein 与 scFv，"with **high hit rates, nanomolar affinities**, target specificity, and functional activity"，并公开从靶序列到排序结合剂的 notebook。**注意：具体命中率数值在 README/摘要里没给，我只拿到定性声明。**
  - ESM Atlas：**68 亿序列 / >11 亿预测结构**，用稀疏自编码器（~16,000 可解释特征）解释 ESMC 表示空间。
- 另有 ESM3 机理分析一手：`10.64898/2026.07.08.737319`（esm3-sm-open-v1 1.4B/48 层的模态融合深度分析：物理模态在第 25–35 层融合、序列最后加入、功能注释模态全程不正交融合；跨 12 物种 5,555 蛋白均在第 35 层达峰）。`ABS`

**流程位置**：ESM3/ESMFold2 属"序列生成 + 结构预测 + 反演设计"三合一路线（统一多模态），与 Baker 的"扩散骨架 + MPNN 反折叠 + 复折"分离式路线竞争同一流程骨架；ESM3 侧目前**没有**亲和力头。

**三态判定（ESM 路线）**
- **能证明**：ESM3 有**真实湿实验功能产物**——esmGFP（与最近已知 FP 58% 同一性、与模板 1QY3 36%、相对 tagRFP 96 个突变、2 天成熟后亮度落入天然 GFP 分布、色基敲除丧失荧光）；实验 1 的分母明确是 96 孔板上的 88 条设计。后继 ESMFold2/ESMC 也已发布并有 5 个治疗靶点的实验室验证声明 + 6.8B 序列/1.1B 结构的 Atlas。
- **不能证明**：不能给出 ESM3 的**命中率数值**（论文只给"哪条亮了"，没给"亮了几条/下单几条"的整数，实验 2 下单条数在附表未取到）；不能证明 ESMFold2 的 binder 命中率高于 Chai-2/Latent-X（README 只写"high hit rates"，无数字）；不能把"公司停更/团队并入 Biohub"当已核验事实——我只核验到仓库/权重/署名从 EvolutionaryScale 迁到 Biohub，且 ESM3 文档降级为附属页、98B/7B 权重不再开放下载。
- **尚缺什么**：实验 2 的设计条数与命中计数（需 Science 附表/补充材料）；ESMFold2 反演设计的命中分母（需读 `10.64898/2026.06.03.729735` 正文）。

---

## 6. 你点名但查无一手来源的方法（明确结论）

| 名称 | 结论 | 检索证据（2026-11-07） |
|---|---|---|
| **DockDesign**（2025，扩散+对接联合做结合体） | **未找到该名称的一手来源** | EPMC TITLE/ABSTRACT 0；arXiv `all:"DockDesign"` 0；Crossref 0；GitHub 仅一个 0 星个人库 `Nikhil-kurmachalam/DiseaseToTarget_Dockdesign`（2026-04-24，无文档、与"扩散+对接联合"无关） |
| **MolGen**（作为蛋白设计方法） | **不存在该用途的方法**；同名工作属**小分子**生成 | GitHub `zjunlp/MolGen`（ICLR 2024, *Domain-Agnostic Molecular Generation with Chemical Feedback*）、`eyalmazuz/MolGen`（2021/22 GFlowNet 3D 分子生成）；EPMC 蛋白设计语境 0 |
| **IG-LLM** | 名称存在但**不同领域**，与蛋白设计无关 | 唯一近名命中为 *Re-Thinking Inverse Graphics With Large Language Models*（arXiv `2404.15228`）与一篇 2026 韩国数字产业期刊文本挖掘文（`10.7838/kjdi.2026.31.2.001`）；蛋白语境 0 |
| **LockMSF** | **未找到该名称的一手来源** | EPMC 0；arXiv 0；Crossref 0；GitHub 0 |
| **PoseChains** | **未找到该名称的一手来源** | 四路 0（见 §4.2） |
| **RFSolo** | **未找到该名称的一手来源** | 四路 0（见 §1.4） |

**能证明**：这 6 个名字在四个独立学术索引里都没有一手论文/仓库。
**不能证明**：不能证明它们不存在于闭源公司内部代号。
**尚缺什么**：若你是在某份二手材料里看到这些名字，需要那则材料的原始出处才谈得上核验；否则模板里出现它们就是把无法核验的代号写成"前沿"。

---

## 7. 从头酶设计 2025–2026：**库里没有**的新方法与新材料（每条给"实测做到什么程度"）

> 库内已有的酶设计行（B17 PLACER 丝氨酸水解酶 / B18 metallohydrolase / B20 RFdiffusion2-AME / K63 Kemp / K64 motif scaffolding / C05 dTERMen / M-K34 近红外 FP / C23 IMUSE）已排除，下面只列增量。

### 7.1 AlphaProtein Novo（AP Novo / APN）——2026-10，**本次最强的一条**
一手来源：**"Designing enzymes for new-to-nature chemistry and non-natural substrates with AlphaProtein Novo"**, bioRxiv 2026-10-01, DOI `10.64898/2026.10.01.756017`（EPMC PPR1334440）→ https://www.biorxiv.org/content/10.64898/2026.10.01.756017v1 （正文已读）`FT`
- 替换步骤：骨架生成（motif scaffolding 扩散）+ **序列系综打分筛选**（新闸口）+ 机制启发式度量（基于 **AF3 预测**）。
- 湿实验与分母：
  - **DEHP 降解（酯酶，非天然底物）**：首轮 **81 条设计**中 4 条高于背景 3 个标准差、1 条裂解液活性 ≥ 对照天然酶 QHH21706.1 的 2%；再两轮后 **新骨架 hit rate 11%、回收骨架 hit rate 39%**（命中定义 = 活性 ≥ QHH 的 2%）；命中分布在 7 个不同结构簇。**对照口径**：近期一次 65 个天然酯酶（其中 16 个预测具 DEHPase 活性）的筛选只找到 **1 条**有活性 DEHPase。`FT`
  - 设计酶 **GDM_DEHP_376** 在含乙腈/变温条件下把 DEHP  hydrolyze 到 MEHP（TTN 曲线），而这些条件会使天然酶变性。`FT`
  - **新-to-nature 卡宾/ nitrene 转移酶（C–H 胺化制哌啶）**：活性命中定义 = 总 C–H 胺化活性 ≥ Tam Pgb wt 的 5%，其中哌啶选择性命中按区域选择性再筛；最佳设计把天然偏向吡咯啶的选择性**反转**。`FT`
  - Kemp  eliminase 与丝氨酸 esterase 两个"模范反应"上给出 state-of-the-art 催化效率（Table 1，含 Michaelis-Menten 参数，需按孔板重读）。`FT`
- 作者明示的方法学要点：**"a key predictor of design success was a novel filtering strategy which evaluates ensembles of sequences derived from the same backbone"**；且明确"各反应 hit rate 定义不同，**不允许跨反应比较**"。`FT`
- 局限：Table 1 里"best design 不一定来自 best facet"（facet=同一套管线参数的子集），即最优值来自子集挑选，分母是自选的。`FT`

### 7.2 CaGE（Baker/IPD 系，2026-10）——RF3 被"再训练成设计条件网络"
一手来源：**"Complex enzyme active site scaffolding by iteratively detuned catalytic guidance"**, bioRxiv 2026-10-02, DOI `10.64898/2026.10.02.756307`（EPMC PPR1335387，正文已读）`FT`
- 替换步骤：**序列生成 + 约束满足的迭代循环**。核心是**把 RF3 训练成可接受 5 类设计条件**（界面热点、相对可及度、氢键供/受体身份、界面类型、**原子对距离**），再用 classifier-free guidance 在多轮设计中**逐步衰减**约束强度（detune），交替"约束引导的结构预测 → LigandMPNN 重设计"；另有免训练的推理期 motif guidance（扩散采样时直接拉原子到目标几何）。
- 湿实验做到什么程度：
  - **非血红素铁设计 A11**：175 残基、以 α-螺旋为主的疏水口袋，His73/His100/Asp102 组成 2-His-1-carboxylate facial triad，Tyr78/Asn130 负责底物定向；产物信号高于背景且 **56% ee**，无酶对照与 H73A/H100A 配位点突变对照均为**外消旋**。`FT`
  - **PLP 依赖的 retro-aldolase CaGE-RA1.0**：完整蛋白质谱显示在 NaBH₄ 处理后出现 **+231 Da** 物种（ apo 21,504 Da → 21,735 Da），与"单个 PLP 经 Schiff 碱形成并被还原"一致；**2.7 Å 晶体结构**与模型骨架 **r.m.s.d. = 0.702 Å**，且如设计般为**单体**（天然 PLP 酶多为寡聚）；四个设计催化位点的替换使产量回落到背景附近。`FT`
  - in silico 基准：CaGE 在一组多样的酶基准（含 PTE、UGDH）上降低中位 motif r.m.s.d.，并让序列在**独立 AF3 预测**下恢复目标活性位。`FT`
- 局限（作者语境）：复杂约束集下"内部一致的设计占比可以极低，以致计算上不可负担"——这正是 CaGE 存在的理由，也说明**单轮生成 + 置信度筛选**在复杂活性位上会失败。`FT`

### 7.3 Metal Mer —— 无定向进化的金属酶选择性
一手来源：**"De novo design of metalloenzymes using Metal Mer"**, bioRxiv 2026-10-13, DOI `10.64898/2026.10.13.758590`（EPMC PPR1344074）`ABS`（正文未取）
- 做到什么程度（摘要级，数字来自作者自己）：**锌依赖氢转移酶**，最佳变体在 **13 个底物**上 **ee > 99%，且不经定向进化**；对含多个羰基的甾体底物，重设计变体区域/非对映选择性 **> 19:1**；**铁催化的烯烃双官能化**"out of the box" 有活性（**10% 收率，70:30 e.r.**），超过此前报道的天然功能类似物。
- 口径：湿实验（产物分析/ee/e.r.），但**没有命中率的总分母**（摘要未给"投了多少条"）→ 模板里写"选择性数字可用，命中率口径未明"。

### 7.4 Multistate enzyme design —— 不再"只对一个过渡态做设计"
一手来源：**"Multistate Enzyme Design Enables Efficient and Stereoselective Multistep Catalysis"**, bioRxiv 2026-09-11, DOI `10.64898/2026.09.11.750617`（PPR1320068）`ABS`
- 做到什么程度：对 de novo **Morita–Baylis–Hillman 酶**，用构象系综沿整条反应坐标优化活性位，最佳变体的**双底物催化效率比单态设计高 >100×**，并在效率与对映选择性上**超过一条经大量定向进化优化的天然/进化酶**；结构+动力学分析显示单态设计会破坏预组织、 destabilize 上游态并把限速步骤推离目标过渡态。
- 模板价值：把"theozyme/单过渡态约束"升级为"多态约束"，且给出一条可写的负面判据——单态优化可能人为制造动力学瓶颈。

### 7.5 Design–Evolution Synergy / 演化后机理解释（两条，正好补库内缺口）
- **"Design-Evolution Synergy Enables New-to-Nature Enzyme Chemistry"**, bioRxiv 2026-10-01, DOI `10.64898/2026.10.01.754751`（PPR1332934）`ABS`：motif scaffolding + 计算重设计 + 定向进化，用工程化 de novo **血红蛋白（haemoprotein）**实现可程序化区域/对映选择性的 **C–H 胺化合成手性哌啶**。
- **"Interplay of stability and dynamics in the optimization of a highly proficient de novo enzyme"**, bioRxiv 2026-05-29, DOI `10.64898/2026.05.29.728685`（PPR1242495）`ABS`：从原始计算设计经**两轮定向进化**到高催化效率；最有价值的负面发现——**"the initial design considered only the transition state but not substrate binding, leading to a dynamic Michaelis complex prior to optimization"**；在活性位入口螺旋引入 Gly/Pro 提高动力学从而提活性；TSA 结合使全蛋白骨架稳定性上升（除该螺旋）。
- **"Evolution promotes transition-state-like conformations with enhanced basicity and electric fields in the substrate complex of a designer enzyme"**, bioRxiv 2026-09-09, DOI `10.64898/2026.09.09.750330`（PPR1317712）`ABS`：**大规模 MD + QM/MM 反应势垒**，对 de novo **Kemp 消 elimase** 的设计版 vs 进化版比较；结论：势垒与质子转移反应能强相关，进化让基态系综富集"反应性构象"（减少到达过渡态所需重组），并出现**负活化热容**。→ 这是库里"[K27] MD 精筛是否更省无公开基准"缺口的**相邻正面材料**：MD 在这里不是筛选闸口，而是"解释设计-进化差距"的手段，模板该这样放它。

### 7.6 面向细胞的 de novo 酶（两条，库内完全没有这类）
- **"A de novo designed enzyme for photo-proximity labeling of E3 ligase neighborhoods in live cells"**, bioRxiv 2026-07-22, DOI `10.64898/2026.07.22.739993`（PPR1284233；作者 Kim/Lin/Nam/Swaney/Krogan/Kim）`ABS` —— 设计酶直接用于活细胞邻近标记。
- **"Computational design of a versatile, zero-radius proximity labeling enzyme"**, bioRxiv 2026-09-24, DOI `10.64898/2026.09.24.754223`（PPR1329554）`ABS` —— "零半径"标记酶（把标记范围压到点接触）。
- **"Engineering a Covalent Linkage into a Dimeric De Novo Enzyme Reveals a Novel Life-Sustaining Mechanism"**, bioRxiv 2025-12-09, DOI `10.64898/2025.12.09.693225`（PPR1232271）`ABS`。
- **CatESO**, *JACS* 2026, DOI `10.1021/jacs.6c14365`, PMID 42915563 `ABS`：可微分的酶序列优化，由"底物感知的 **kcat** 预测"引导——把 kcat 预测放进了优化回路（库内只有 kcat 预测的评测，没有把它当设计目标的）。
- 综述/观点（新增、非重复）：Listov & Fleishman *Curr Opin Struct Biol* 2026 `10.1016/j.sbi.2026.103252`；Lindner/Hardy/Hilvert *Biochemistry* 2026 `10.1021/acs.biochem.6c00356`；MechFind *Nat Commun* 2026 `10.1038/s41467-026-71957-0`（de novo **预测酶机理**，不是设计酶）。

**三态判定（2025–2026 从头酶设计整体）**
- **能证明**：设计酶已进入"可给出选择性数字"的阶段——DEHPase 新骨架 11%/回收骨架 39% 命中（分母=下单条数，命中=活性 ≥ 天然对照 2%）；Metal Mer 的 13 底物 ee > 99% 且不用定向进化；RFD3 在 96 构型零样本批次直接拿活性催化剂；CaGE 有 2.7 Å 晶体（骨架 RMSD 0.702 Å）+ +231 Da PLP 加合 + 突变失活三重证据；Multistate 设计比单态高 >100× 双底物效率。
- **不能证明**：不能证明任何一条达到"工业可用"级别（多数只给单点最佳值、分母自选，且 AP Novo 自己声明 hit rate 定义不可跨反应比较）；不能证明 `ABS` 级几条（Metal Mer / Multistate / Design-Evolution / Boltz-2 抗体基准）的表格内数值——本轮只读到摘要。
- **尚缺什么**：一份把"新骨架 hit rate"统一到同一反应、同一活性定义下的前瞻基准；Metal Mer 与 Multistate 的正文（下单条数、每轮分母、kcat/KM 全表）。

---

## 8. "用亲和力预测模型直接当设计筛选判据"的 2026 公开证据（含负面）

**直接结论**：2026 年这类证据已经相当多，而且**负面/限制型占多数**。逐条（一手，全部可点）：

| 证据 | 判据 | 分母 | 正/负 | 来源 |
|---|---|---|---|---|
| 共折叠置信度**与实验活性无关联** | AF3/Boltz-2 置信度、Boltz-2 亲和力 | 新解 sEH 共晶+配套活性、及截断后策展集（激酶/别构/共价/PROTAC/分子胶/片段/膜蛋白/RNA/活性悬崖） | **负**（但 AF3 **minPAE < 0.85 Å** 可作位姿门；亲和力能抓系列内相对趋势、能分辨悬崖对） | `10.64898/2026.08.24.746785` `ABS` |
| 通用置信度指标**不足以做抗体-抗原筛选** | Boltz-2 置信度（含 ipTM-min 最佳） | **519 条治疗性 mAb** ×（同源/随机非同源抗原） | **负**：ROC-AUC 仅 **0.5–0.6**；多特征/多变量建模"little to no improvement"；采样 ~15–20 seed 后收益递减；不喂 MSA 略好（+0.027 AUROC，省 ~8 s） | `10.64898/2026.05.13.724924` `ABS` |
| 亲和力值 vs 物理自由能：整体弱、**top-100 归零** | Boltz-2 affinity vs ESMACS ΔG | **16,780（3CLPro）/ 21,702（TNKS2）** 化合物 | **负**：r=0.45/ρ=0.46（TNKS2）、r=0.24/ρ=0.25（3CLPro）、top-100 相关≈0；两头互相关仅 0.21/0.25；几乎全部预测 < −4 kcal/mol（压缩） | `10.1021/acs.jctc.6c01334` / arXiv `2603.05532` `FT` |
| **有少量本靶标活性标签就微调亲和力头** | 微调 Boltz-2 affinity head + 重排 top 10% | 8 个 MF-PCBA 靶点回顾集，标签 40–300 | **正**：300 标签时 top1% 活性数 ×1.77、AP ×2.14 | arXiv `2609.24302` `ABS` |
| 结构法**蛋白-蛋白亲和力回归不可靠** | Boltz-2-PPI | TCR3d + PPB-affinity | **负**：小样本与大样本两种设定均逊于序列基线 | arXiv `2512.06592` `ABS` |
| **亲和力/相互作用模型可替代置信度做排序** | 用 BoltzPPI 而非结构置信度排序纳米抗体 | **10 个新靶点**，确认结合剂 | **正**：命中率 **3.3% → 8.0%**；另 10 靶点上 7/10 拿到纳米抗体筛选命中（文献中 Chai-2 为 6/10）；可开发性五项全过 58%（BoltzGen 40%、临床期 VHH 对照 21%） | `10.64898/2026.06.23.733997` `ABS` |
| **共折叠模型的"过滤能力"本身是被承认的短板** | Promera 置信度指标分结合/非结合 | miniprotein + 纳米抗体 | 承认现状："their ability to **filter designed binders** — an essential use case — remains **insufficient**"；并声称其置信度指标更适合过滤、共折叠超过 **OpenFold3-p2 与 Boltz-2** | `10.64898/2026.06.07.729267` `ABS` |
| 亲和力代理做**闭环设计**（计算验证而非湿验证） | Boltz-2 生成 likelihood + affinity 联合打分 | TYK2 虚拟筛选 → 与 Boltz-ABFE 对比 | 中性偏正但**分母是模拟**：屏幕分 vs ABFE **\|R\|=0.74** | `10.1101/2025.06.14.659707` `FT` |
| **ML 亲和力在新骨架探索系列失效**（药化真实项目） | Boltz-2 共折叠 + 亲和力；对照 AEV-PLIG、Vina、HAC | 15-PGDH 四个化合物系列（含一个探索新亚口袋的系列 3） | **负**：系列 3 未预测出任何成员优于母体，而实验活性提升达 **500×**；汇总 Boltz-2 显著低于 FEP+（系统性系列间偏差，辛普森悖论式）；Vina 在多数系列表现相对更好 | 见下方"注" |

**注（最后一条）**：这条我**没有拿到一手正文**，只在二手聚合站见到转述（ebiotrade 对一篇 2026-10 文章的编译）。按你自己定的规矩它只能算线索。**要进模板必须先找到原始 DOI**；我未找到一手来源，故在表里标注为待补。

**关于"配套阈值/Rocket"**：
**能证明**：公开可查的、来自一手论文/README 的阈值确实存在若干条（RF3 的 `pDE ≤ ln(0.075·length)` / `pLDDT ≥ 0.62` / `pAE ≤ 15` / 复折 `pLDDT>80 & iPAE<10`；Chai-2 的 BLI `>+0.1 nm 且 >300% 背景`；AF3 `minPAE < 0.85 Å`；Boltz-2 `affinity_probability_binary` 用于结合/诱饵二分、`affinity_pred_value` = log10 IC50 µM；AP Novo 的"同骨架序列系综"过滤）。
**不能证明**：**不存在任何公开的、跨靶标可复用的"亲和力阈值"**。多个一手来源明确否认阈值可迁移：`10.1021/acs.jctc.6c01334` 写"no universal threshold exists due to the system-dependent nature of the overestimation"；`10.64898/2026.04.21.720042` 写"canonical DockQ threshold cutoffs for protein–protein complexes are **not directly transferable**"。库内 §"3a 自洽性反折叠主闸口"那种"pLDDT>80 / pAE<10"式阈值表，同样只该以"某篇论文在某靶点上的选择"来引用。
**尚缺什么**：所谓 "Rocket"（如果指预注册规程/registry 或一份官方 protocol 文档）——**我在 bioRxiv/arXiv/Crossref/GitHub/EPMC/protocols.io 语境都未检索到这样一个一手对象**；最接近的一手规程是 Foundry 的 Colab "IPD Design Pipeline Tutorial"（流程而非阈值）与库内 [K06] 的 protocols.io 文件。

---

## 9. 给模板的"可直接抄"结论（压缩版，全部带来源号）

1. **默认链**：RFD3 → ProteinMPNN/LigandMPNN → **RF3**（官方教程原话），且官方 RFO 已把 **Boltz-2 接入打分位** — [S1 Foundry README]
2. **RF3 的独门卖点不是精度而是"物理正确性"**：手性中心正确率 88% vs AF3 84% vs Boltz-2 76%（不加引导）— [S2 `10.1101/2025.08.14.670328`]
3. **亲和力头分两个用途，混用即错**：`probability` 管 hit discovery 二分，`log10(IC50, µM)` 管系列内排序 — [S3 Boltz README]
4. **亲和力预测当"设计判据"目前只能做到"系列内相对排序"，不能做绝对门槛**：top-100 相关塌到 ≈0；跨系列 500× 提升看不见 — [S4 `10.1021/acs.jctc.6c01334`]
5. **抗体-抗原方向，通用置信度指标近乎无效**（AUC 0.5–0.6），要筛就得用任务专用模型（BoltzPPI/AntiConf/表位约束）— [S5 `10.64898/2026.05.13.724924`；S6 AntiConf `10.1093/bib/bbag137`；S7 BepiPocket `10.1002/pro.70730`]
6. **命中率数字最漂亮的是 Chai-2 与 Latent-X/SeedProteo 这一代**：Chai-2 抗体 15.5%（VHH 20.0%/scFv 13.7%）、26/52 靶点、miniprotein 68%，每靶 ≤20 条、两周闭环 — [S8 `10.1101/2025.07.05.663018`]
7. **酶设计已经出现"零-shot 96 孔拿到活性催化剂"与"同骨架序列系综是主判据"两条新事实** — [S9 `10.1126/science.aeh2982`；S10 `10.64898/2026.10.01.756017`]
8. **单过渡态约束是被点名的新方法学缺陷**，需升级成多态/系综约束，或用 CaGE 的迭代衰减 — [S11 `10.64898/2026.09.11.750617`；S12 `10.64898/2026.05.29.728685`；S13 `10.64898/2026.10.02.756307`]
9. **MD/QM 的位置**：2026 一手材料里 MD 用来**解释**设计与进化差（QM/MM 势垒、负活化热容），不是当筛子；QM 用在**约束生成**（theozyme/TS 几何、多态） — [S14 `10.64898/2026.09.09.750330`]
10. **模型版本必须写死**：OpenFold3 OF3p1 与 OF3p2 检查点互不兼容、数值不可横比；RF3 有 01/24 与 09/21 两个截断；Chai-1 截断 2021-01-12。模板里凡引用别人的分数，必须同时写模型版本 + 训练截断 — [S1 confornets README；S2；S8 Chai-1]
11. **6 个方法名（DockDesign / MolGen / IG-LLM / LockMSF / PoseChains / RFSolo）没有一手来源，模板禁止出现** — [§6]

---

## 10. 溯源与复现

- 抓取脚本与本地缓存（可作为本次引句的"底稿"）：`A:\AITEMP\frontier_survey_20261106\`
  - 脚本：`arx.py`(arXiv API) `epmc.py`(Europe PMC) `ft.py`(EPMC fullTextXML) `bx.py`(bioRxiv HTML) `pprpdf.py`(EPMC 预印本 PDF) `s2.py`(Semantic Scholar, 本次 429 弃用) `oa.py`(OpenAlex, 本次 429 弃用) `page.py`
  - 正文缓存（本次实际读过全文的）：`txt_10_1101_2025_08_14_670328.txt`(RF3) `txt_10_1101_2024_10_10_615955.txt`(Chai-1) `txt_10_1101_2024_11_19_624167.txt`(Boltz-1) `txt_10_1101_2025_07_05_663018.txt`(Chai-2) `txt_10_1101_2025_09_18_676967.txt`(RFD3 预印本) `txt_10_1101_2024_07_01_600583.txt`(ESM3) `ft_PPR1039145.txt`(Boltz-2) `ft_PMC13472093.txt`(Boltz-2 JCTC 评测) `ft_PMC12287924.txt`(ABCFold) `gh_foundry.md` `fd_models_rf3_README.md` `fd_models_rfo_README.md` `fd_models_rfd3_README.md` `of3.md` `confornets.md` `boltz_readme.md` `chai_readme.md` `es_evolutionaryscale_esm.md` `esm3_readme.md`
- 每条数字后的 `FT`/`ABS`/`README` 已标明取证级别；`ABS` 条目**不得**在模板里扩写方法细节。
- 本轮**未做**的事（诚实边界）：未读 Chai-2 第二篇（`10.1101/2025.11.29.691346`）正文；未读 OpenFold3 技术报告 PDF；未读 Science 版 RFD3 正文（订阅墙）；未读 Metal Mer / Multistate / BoltzProt-1 / Promera / OpenBind / Boltz-2 抗体基准的正文（仅摘要）；未核验 EvolutionaryScale 公司层面的停更/并购叙事；未逐字核验 15-PGDH 那条（缺一手 DOI）。
