# [C23] IMUSE——先花通量把标签造出来，再让训出来的模型当筛选器

Yitao Ke†, Yanzhe Zhang†, Minchao Fang, Jingyang Zhao, Hongli Zhu, Zehui Xu, Longxing Cao（通讯；† 共一）
bioRxiv 预印本 2026-06-23 · DOI 10.64898/2026.06.23.733994 · Europe PMC PPR1259026 · 西湖生命科学研究院（预印本，未经同行评议）
全文链接 https://www.biorxiv.org/content/10.64898/2026.06.23.733994v1

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C23**（组：曹龙兴组） |
| 题名 | Integrating Machine-learning and Ultra-high-throughput Screening for Enzyme spaces exploration（策略简称 **IMUSE**） |
| 作者 | Yitao Ke、Yanzhe Zhang（原文脚注：这两位是共一）、Minchao Fang、Jingyang Zhao、Hongli Zhu、Zehui Xu、**Longxing Cao（末位通讯，caolongxing{at}westlake.edu.cn）** |
| 单位 | State Key Laboratory of Gene Expression, School of Life Sciences, Westlake University；Artificial Intelligence Drug Design Core Laboratory, Westlake Laboratory of Life Sciences and Biomedicine；School of Engineering, Westlake University（Zhao J） |
| 出处 | bioRxiv 预印本 2026-06-23，DOI 10.64898/2026.06.23.733994，Europe PMC 记录 PPR1259026。**未经同行评议** |
| 本文取回方式 | bioRxiv 全文页（batches.tsv: fetch_status=OK, fallback_ok[biorxiv_full]），2026-10-20 本地抓取 |
| 本地全文 | `fulltext/C23_PPR1259026_fullTextXML.xml`（327,325 B）→ 标签剥离纯文本 `fulltext/C23_PPR1259026_text.txt`（65,006 B，本卡引句底稿） |
| **底稿覆盖范围（重要）** | 本底稿含 Abstract / Introduction / Results（含 Fig 1–5 完整图注）/ Discussion / Footnotes / References + 网页导航文字，**不含 Materials & Methods 段**。凡协议级参数（芯片通道尺寸与流速、DE 配方、测序深度、模型超参、QM 泛函/基组）本卡一律写「本底稿未含 Methods」，不猜 |
| 对照底稿 | `sources/cao.md:366–380`（原卡）；`sources/cao.md:422`（筛选级联总结表 C23 行）、`:461`（QM 角色判定）、`:477`（未核实清单第 7 条，正是本卡的命中率分母问题） |
| 证据级别 | **全文级**（本卡引句均可在本地纯文本逐字命中；但「全文」如上，不含 Methods，故阈值多数只能写「原文未给阈值」） |
| 未取到的部分 | Fig 3A 右侧「每轮分选后 NGS 回收的唯一设计数」只存在于图内，正文未复述；Fig 2F/G 标定曲线数值、Supplementary fig S1–S28、table S2/S3/S5（全部动力学常数）均不在本地。凡涉及处本卡明写「正文未给出」 |

## 1. 这篇到底解决什么（大白话）

de novo 设计酶卡在的不是「折不折得起来」，而是**造出来一大堆之后没人能事前判断哪个有催化活性**。这些序列没有自然同源物，等于没有进化信息可借力；作者先把自己的前作路线（也就是 B09 那套为 binder 打磨出来的物理/DL 打分）判了死刑：Lib1 的回顾分析显示传统指标与实测活性无显著相关。

于是这篇换了问题：不去找更聪明的先验判据，而是**自己造数据集**。三步：① 用物理生成器产设计（QM 算底物过渡态 → theozyme → RIF 采样配位几何 → Monte Carlo 片段装配骨架 → Rosetta/ProteinMPNN 出序列）；② 用自建的微流控平台（sdDE-FACS：一个 E. coli 细胞 + 锌离子 + 荧光底物 FDBz 共包封在一个双乳液滴里）把「这个设计有没有活性」变成一次能并行读几百万个的荧光信号，分几轮 FACS 分选后用 NGS 数每轮回收了哪些设计；③ 把「被回收」当正类、「被丢弃」当负类，训练两个模型（一个管同一骨架内的突变排序，一个管跨结构的活性判别），**由训练出来的模型去挑下一批要花钱合成和纯化的候选**。

结果：模型挑出的 96 个 Lib2 候选中 28 个有活性（29.2%），作者称比上一代 Lib1 高约 4.9 倍；这 28 个里 16 个能给出可测的亲和力与催化参数。序列空间那边，模型提名三元突变（理论组合 >1.9×10⁹），只测了 6 个，拿到 2.6–4.8 倍 kcat/KM 提升。

一句话：**它把「漏斗该用哪个判据」这个问题，替换成了「先花通量把判据训出来」**——这正是我们关心的「功能数据怎么回灌筛选器」的一条完整实证路径。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **先验判据在 de novo 酶上集体失效**（全文立论起点，也是我们最该抄的一句话）。
   - 现象/证据：Results 里 "Collectively, deep-sequencing analysis of the sorted populations identified a weak enrichment of"；Fig 3B 图注更直接 "These features show a statistically significance (FDR-adjusted P < 0.05,"；到 Lib2 一节又复述一次 "Previous retrospective analysis of Lib1 dataset revealed that none of the conventional metrics"。
   - **他们做了什么**：不继续调权重、不换指标，直接放弃「用通用判据排序」这条路线，改成造数据 + 训本地模型："This failure of general scoring functions motivated us to develop a data-driven approach tailored"
   - 应对后仍留下的代价：判据从此**只在这个体系（锌水解 + FDBz + 这一套生成器）内成立**，模型可解释性弱，且其天花板被上游液滴标签的质量锁死（见第 7 节）。
2. **功能验证通量是硬瓶颈**：设计一次能生成几十万上百万，逐个纯化测动力学完全做不到。
   - 现象/证据："To overcome the bottleneck of functional"，通量口径 "This approach enabled the screening of millions of droplets within a single experimental run." 与 "for functional screening at a throughput of thousands of droplets per second"。
   - **他们做了什么**：把 genotype 与 phenotype 绑在同一个液滴里（单细胞 + ZnSO₄ + FDBz 共包封），FACS 按荧光门分选，分选池做 NGS 计数，从而「几百万个设计各有一次有无活性的读数」。
   - 代价：读数是**荧光是否过门**，不是 kcat/KM。本底稿没有报告液滴检出的假阳/假阴率，只用标定实验论证敏感性（"capable of detecting <1nM fluorescent probe (5"）。
3. **既有双乳液滴体系要额外加裂解剂，胞质蛋白背景会混淆活性判别**。
   - 现象/证据 + 应对：作者明写顾虑后直接改造表达系统 —— "This strategy compartmentalizes de novo enzymes"（阿拉伯糖诱导 + OmpA 信号肽的周质表达通路），并用 EGFP 做定位与泄漏对照："Prolonged incubation in buffer is confirmed no"。
   - 代价：筛选前提变成「这个设计必须能表达并分泌到周质」。本底稿未见把「表达/定位失败」与「折叠对但没有催化」拆开的对照数据，所以阴性标签里两类混在一起（详见第 7 节）。
4. **双乳液滴和商用 FACS 喷嘴天生不兼容**（尺寸分散→流不稳定→堵喷嘴）。
   - 现象/证据："Our chip-design ensures that the DE droplets"。
   - **他们做了什么**：设计双 flow-focusing 几何的芯片（内水相入口用两条加宽通道降低细胞引起的流扰动），系统优化油/水流速做单分散，并用 100 µm 喷嘴 + 共聚焦确认液滴在整个分选过程保持完整。
   - 代价：通量上限被喷嘴直径与单分散性钳住；正文只给 thousands of droplets per second 这个量级，未给实际运行速率与理论上限的差距。
5. **首轮门限设严了会漏掉弱活性设计**（漏斗第一刀就砍掉 wanted 的样本）。
   - 现象/证据："For the initial round, we applied permissive"
   - **他们做了什么**：分多轮、在不同底物浓度下设门（Fig 3A 图注 "Periplasmic-expressed active designs in E." + "coli are enriched during several rounds of"），第一轮保召回、后续轮做富集；判活阈值最终落在群体频率上 —— "The population fraction of each of the final"
   - 代价：**筛了几轮、每轮削掉多少，正文没有数字**。图注只说每轮回收的唯一设计数标在图 3A 右侧："The total number of unique designs identified in"（本地底稿无图值）。文本能确认的末端分母只有 final enriched pool 343 与其中纯化的 145。
6. **突变体里的动力学权衡：kcat 与 KM 一起涨，效率不涨**。
   - 现象/证据："However, these distal mutations"
   - **他们做了什么**：三处同时改 —— 换输入表征（"we fine-tuned the structure-aware protein"，粗结构 token 由 Foldseek 从 3-4/30-3 代表性骨架抽出后与突变序列拼接）、换损失（"By complementing the default"）、专门去提名**高阶突变**而不是叠加单点（"and selected the top six variants for"）。
   - 代价：验证集只有 6 个变体；与 MULTI-evolve 的对比（5–7 个加成突变换 1.5–5.8 倍 kcat/KM）是跨论文口径对比，不是同库同底物的同期对照。
7. **高通量数据里正负样本极度不平衡 + Lib1 回收率低**。
   - 现象/证据："To counteract class imbalance"；结构模型一节承认 "In consideration of the low"
   - **他们做了什么**：定制 batching +  supervised contrastive loss；用 80/20 回顾式基准配 Precision@n%、Enrichment@n%、Recall@n% 这套与分母无关的指标；再做消融找关键特征（"Encouraged by this success in"）。
   - 应对后仍留下的：本底稿未说明 80/20 是否按骨架/序列聚类切分，因此无法排除同族设计同时进训练与测试（我们读出，第 6.3 条）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **生成端（物理-based，不是扩散模型）**：量子化学算底物**过渡态**几何 → theozyme（Zn 的三个可用配位位点全部 His 几何与 rotamer 系统枚举，存成 coordination RIF table；留一个配位位点给水活化）→ RIF 搜索与过渡态有利的氨基酸相互作用 → 扰动 TS 与配位 His 的相对位姿做 thorough sampling → **Monte Carlo 片段装配（ProBuilder）自下而上搭骨架** → **Rosetta + ProteinMPNN** 序列优化。选它的原因（按原文表述）：要的是**结构多样性超出天然折叠**，而不是复刻某个天然家族（"There are only two representative Zn-His 3 coordination folds in native protein."）。
- **计算评估端（本篇证明它不够用）**：三个配组 His 齐全 + 有利 TS 作用做硬筛；Rosetta 能量指标排序；AF2 评预组织与稳定性；AF2/AF3 的 design-vs-prediction 对齐 = in-silico success；ESM2 / qTM / Foldseek 只用来**证明多样性**，不当闸口。
- **新的筛选端（本篇真正的贡献）**：**sdDE-FACS** —— 单细胞 + ZnSO₄ + FDBz 共包封的双乳液滴，周质表达避免裂解与胞质背景，FACS 多轮分选，NGS 数每轮回收的唯一设计。
- **模型端两个**：① 序列空间用 **SaProt**（结构 token 来自 Foldseek）微调，配 supervised contrastive loss + 定制 batching，输出排序去提名三元突变；② 结构空间用 **GVP-GNN**（ESM2 序列 embedding + AF3 残基级 pLDDT 作节点特征 + 3D 坐标经径向基函数编码 + 针对锌配位环境的专用 attention），二分类头输出 True/False 再转排序分，用来**替人挑要合成纯化的候选**。
- **实验复验端**：纯化 + Michaelis-Menten（KM、kcat、kcat/KM、kcat/kuncat、-log Ktx）；代表性设计做 X 射线共结晶验证构象与活性位点。
- **没有用的方法**：本底稿内**没有**显式溶剂 MD、没有自由能微扰/MM-PBSA/metadynamics；QM 只出现在过渡态几何那一步。

### 工作流程表（生成 → 通量 → 标签 → 回灌 → 前瞻）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| G1 | 目标反应（锌依赖酯水解） | 用量子化学算底物**过渡态**几何，作为 theozyme 中心 | 本底稿未含 Methods，未给泛函/基组与数值判据 | 一套 TS 坐标 |
| G2 | TS + Zn 离子 | 系统枚举 Zn 三个可用配位位点的全部 His 配位几何与 rotamer，存 coordination RIF table；第四配位位点留给水活化 | 原文未给阈值（枚举即全采） | 覆盖组合几何的 RIF 表 |
| G3 | TS 几何 | RIF-based 搜索与过渡态有利相互作用的所有氨基酸 | 原文未给数值阈值 | TS 稳定残基集合 |
| G4 | G2+G3 | 扰动 TS 与配位 His 的空间关系，thorough sampling of theozyme configurations | 原文未给阈值 | 一批 theozyme 构型 |
| G5 | theozyme 构型 | Monte Carlo 片段装配（ProBuilder）自下而上搭骨架，同时容纳三个配位 His 与 TS 稳定残基 | 能量改进方向择优（原文未给数值阈值） | 结构多样的设计骨架（Fig 2B 的 UMAP 云） |
| G6 | 设计骨架 | **第一道硬闸**："Structures featuring all three" | 三个配位 His 必须齐全 + 存在有利 TS 作用（**二值条件，非连续阈值**） | 进入序列优化的设计子集（正文未给数量） |
| G7 | 优化后设计 | 排序 + 结构复评："Top candidate designs were" | Rosetta 能量指标；AF2 预组织/稳定性（原文未给数值阈值） | Top candidate 设计（正文未给规模） |
| G8 | 设计 vs AF2/AF3 预测 | in-silico success 判据：见 Fig 2 图注 "Designs are evaluated by" | **align to a sufficient degree —— 原文只这么写，没有 RMSD/PAE 数字** | 通过的设计进入合成清单 |
| G9 | 通过的设计 | 把设计片段基因合成成 oligo 库，再拼接成全长基因，转化 E. coli | 无 | 实物库（正文未给克隆数） |
| W1 | 表达菌 + ZnSO₄ + FDBz | 双 flow-focusing 芯片生成单分散 W/O/W 双乳液滴，单细胞与底物共包封 | 液滴需明显小于喷嘴直径；单分散性（CV 在图 2D） | "This approach enabled the" |
| W2 | 液滴群 | FACS 分选：**首轮宽门保召回，后续轮收紧做富集**，多轮在不同底物浓度下进行 | "For the initial round, we" | 通量 "for functional screening at a"；检出下限 "capable of detecting <1nM" |
| W3 | 各轮分选池 | 深度测序计数 | 存活设计定义：population fraction > 0.0004 **或**在最后一轮被富集 | 每轮唯一设计数**只标在 Fig 3A 右侧，正文未复述**（"The total number of unique"）；final enriched pool = 343 个唯一设计 |
| W4 | 343 的富集池 | 挑 145 个唯一序列做纯化 + 动力学表征 | 判据 = 可纯化且为单体 | "To validate the screening"；"All characterized monomeric"；kcat/kuncat "ranging from 10 2 - to over 10"；最优变体 3-4 的催化效率 ~1.6×10⁸ M⁻¹，"which is comparable to a series" |
| L1 | Lib1 的回收 vs 丢弃 | 把液滴分选的群体频率直接固化成**训练标签** | 正类 = 富集/存活设计，负类 = 被丢弃设计："The positive designs and" | "we adopted the broad genotype-phenotype data from the first-generation library (Lib1), establishing the first structural-level dataset of de novo enzyme-substrate complexes reported to date." |
| L2 | 同一批 Lib1 数据 | 先做「筛子考卷」：比较存活与丢弃的设计在各计算指标上的分布 | "These features show a statistically significance (FDR-adjusted P < 0.05, Mann-Whitney U test with Benjamini-Hochberg correction) between the final surviving designs (active) and discarded designs (inactive), but no feature is individually an effective discriminator." | 结论：指标只能当**特征**不能当**闸口**；最强物理特征是 "the most dominant physical"，其余主导特征是 AF3 相关 |
| M1 | 3-4 / 30-3 两个活性设计 | error prone PCR 建突变库 → 同一套 sdDE-FACS 筛 → NGS | 覆盖单点到三元突变 | "This generated comprehensive" |
| M2 | 上述密集突变数据 | 微调 SaProt（Foldseek 结构 token + 突变序列拼接），交叉熵 + supervised contrastive loss，定制 batching | 回顾基准 80/20 切分；指标 Precision@n% / Enrichment@n% / Recall@n% | "By effectively prioritizing"（且优于只用序列的 ESM-2） |
| M3 | 训好的序列模型 | 直接提名三元突变空间 | 取模型排序 top 6 | 三元空间理论组合 > 1.9×10⁹（正文：sample the triple mutants (representing > 1.9×10 9 theoretical combinations)）；"and selected the top six"；结果 "achieving 2.6- to 4.8-fold over" |
| M4 | Lib1 结构级数据集 | 建活性预测器："we developed a geometric deep" | 二分类头 True/False → 排序分；80/20 回顾基准；测试集分离显著性 P(MWU) < 0.0001、P(KS) < 0.0001（Fig 5C 图注） | "This model was able to enrich" |
| F1 | 更新到 Lib1 全量后的预测器 | 用同一物理生成器造第二代库 Lib2，再按模型 + Lib1 关键特征挑候选 | "We then ranked the designs" | "This procedure nominated" |
| F2 | 模型挑出的候选 | **实际下单**：合成 + 纯化 | 活性判定用纯化酶的荧光底物测定与动力学 | "we synthesized and purified 96 candidates from Lib2 to identify 28 active designs (29.2%)"，"4.9-fold increase in the rate of active hits compared to that of the previous Lib1" |
| F3 | 28 个活性设计 | 逐个做结合与催化定量 | 可测 KM 与催化 | "exhibited measurable binding affinity and catalytic activity toward the substrate"，16/28（~57%）；对照句 "which stands in contrast to the" |
| F4 | 模型选中的设计 | 与 Lib1 最优、天然酶比催化效率 | -log Ktx 口径（天然酶参照取自 ref 47，CYC/CAN） | "exceeding the most active"（两个设计达到该水平） |
| V1 | 代表性设计 2-8、11-7 | X 射线共结晶，与设计模型叠合 | Cα RMSD 越低越好 | "The solved structures exhibited"（正文另给数值：2-8 为 0.76 Å、11-7 为 1.06 Å，均按 120 个残基计算） |

### 通量分母（本篇最容易写错的地方，逐条钉死）

1. **筛池层面**：文本只给量级 —— millions of droplets / 单次运行、thousands of droplets / 秒。**Lib1 生成了多少条设计、合成了多少条基因，正文没有给数字**（本底稿未含 Methods，也没有 n= 的库容量）。
2. **轮次层面**：正文说 several rounds of selection at different substrate concentrations（首轮宽、后续严），但**轮数的具体数字与每轮剩余唯一设计数只在 Fig 3A 图内**，文本不可台账化；因此本卡不许写「每轮削掉 X%」。
3. **末端分母**：能被文本确认的只有 343（final enriched pool 的唯一设计数）→ 145（实际纯化表征数）→ 其中「所有表征的单体设计都有可检出活性」。**这是选择之后的比例，不是全池命中率**，引用时严禁写成「Lib1 命中率 100%」。
4. **Lib2 命中率 29.2% 的分母 = 由模型 + Lib1 关键特征精挑、且真实合成纯化的 96 个候选**，不是 Lib2 提名池（thousands）也不是生成全集。与之对比的 Lib1 侧 ~6% **正文没有以 n/n 形式给出**，只能由 29.2% ÷ 4.9 反推 —— 这一点与 `sources/cao.md:477` 的未核实记录一致。
5. **标签来源**：训练标签来自 **W2/W3（液滴荧光过门 + NGS 群体频率，阈值 0.0004 或末轮富集）**，**不是** W4/F2 的纯化动力学；纯化与结晶只用于验证与机制解释。模型学到的「活性」= 液滴里荧光过门，二者之间的缺口在正文里没有单独量化（本卡第 7 节）。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| millions of droplets / 单次运行；thousands 滴 / 秒 | sdDE-FACS 通量 | "This approach enabled the" |
| <1 nM 荧光探针；10 nM–1 μM 可与背景区分；5 个数量级动态范围 | 液滴检出灵敏度标定 | "capable of detecting <1nM" |
| 首轮 permissive、后续 stringent；several rounds at different substrate concentrations | 分选轮次策略（**轮数无数字**） | "For the initial round, we" |
| population fraction > 0.0004 或末轮富集 | 「存活设计」的定义阈值（也是标签正类口径） | "The population fraction of each" |
| 343 → 145 | Lib1 最终富集池唯一设计数 → 实际纯化表征数 | "To validate the screening" |
| 145 中单体设计 100% 有可检出活性 | **选择后**的阳性率（不是全池命中率） | "All characterized monomeric" |
| kcat/kuncat = 10² 至 >10⁴ | Lib1 酶的加速倍数区间 | "ranging from 10 2 - to over 10" |
| ~1.6×10⁸ M⁻¹（变体 3-4） | Lib1 最优催化效率 | 正文："the top-performing variant," |
| N = 145；只有 2 个代表性 Zn-His₃ 天然折叠 | qTM 结构分布比对的两端 | "There are only two representative Zn-His 3 coordination folds in native protein." |
| Cα RMSD 0.76 Å（2-8）/ 1.06 Å（11-7），按 120 残基 | 结晶结构对设计模型的验证 | "The solved structures exhibited" |
| >10⁵ 个变体 | 3-4 与 30-3 两个家族的合成适应度景观规模（单→三突变） | "This generated comprehensive" |
| >1.9×10⁹ | 三元突变理论组合空间 | 正文："sample the triple mutants" |
| top 6 | 序列模型实际下单验证的三元变体数 | "and selected the top six" |
| 2.6–4.8 倍（vs 野生型）；2.1–4.8 倍（vs 此前最佳突变体） | 三元突变体 kcat/KM 提升 | "achieving 2.6- to 4.8-fold over" |
| >50 倍 | 序列模型在 top-50 相对随机抽样的富集 | "By effectively prioritizing" |
| 80/20 | 两处回顾式基准的训练/测试切分（序列模型、结构活性预测器） | "In consideration of the low" |
| >2 倍 | 结构活性预测器 top-50 相对随机抽 Lib1 的富集；并优于 Clipzyme | "This model was able to enrich" |
| P < 0.05（FDR 校正，Mann-Whitney + Benjamini-Hochberg）；但无单特征可有效判别 | 「先验指标失效」的统计口径 | "These features show a statistically significance (FDR-adjusted P < 0.05, Mann-Whitney U test with Benjamini-Hochberg correction) between the final surviving designs (active) and discarded designs (inactive), but no feature is individually an effective discriminator." |
| P(MWU) < 0.0001；P(KS) < 0.0001 | 活性预测器在测试集上分开「液滴回收」与「其他」设计 | Fig 5C 图注（正文句："The generalizability of IMUSE"） |
| thousands | 模型为 Lib2 提名的设计量级 | "This procedure nominated" |
| **96 → 28 → 16** | Lib2 合成并纯化的候选数 → 活性设计数（29.2%）→ 其中可测结合与催化数（~57%） | "we synthesized and purified 96 candidates from Lib2 to identify 28 active designs (29.2%)" |
| ~4.9 倍 | Lib2 相对 Lib1 活性命中率提升（**Lib1 侧的绝对率正文未给**，只能由 29.2%/4.9≈6% 反推） | "4.9-fold increase in the rate of active hits compared to that of the previous Lib1" |
| 40% | 作者口中 Lib1 的「可测动力学」比例基线（分母未在正文定义） | "which stands in contrast to the" |
| 5–7 个加成突变 → 1.5–5.8 倍 kcat/KM | 对照方法 MULTI-evolve 的口径（跨论文对比，非同库对照） | 正文："Notably, IMUSE achieved higher" |
| ~5 倍 / ~30% | 摘要给的两个 headline（三元突变活性提升、第二代设计成功率） | "IMUSE identified synergistic" |

## 5. 结论——作者说了什么

1. **通量可以替代进化史**："By screening millions of"；并把这套数据定义为对自然进化数据密度的模拟："This strategy emulates the"
2. **模型能有效指导序列与结构两个空间的探索**："These models effectively guide"（摘要句），落地证据是 top-50 富集 >50 倍（序列）与 >2 倍（结构）、以及 Lib2 的 28/96。
3. **成功率被抬高约 4.9 倍到 ~30%**：摘要口径 "IMUSE identified synergistic"
4. **三元突变能打破 kcat/KM 的耦合约束**（作者称 synergistic / long-range epistasis），并声称采样效率优于 MULTI-evolve。
5. **平台可外推到别的反应类型**："The combination of de novo"。
6. **作者自己承认先验指标不行**："Collectively, deep-sequencing"；并承认 de novo 酶「结构稳定、机理上讲得通」这一优点恰恰让基于天然数据的模型无法判别："Furthermore, these de novo"
7. 作者对通量成果的定性："Ultimately, this platform"

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的「筛选器」不是那个 GNN，而是「通量 + 标签」这个组合**。模型只是在 Lib1 内部把 top-50 富集提到 >2 倍；它学到的概念边界由液滴荧光门（0.0004 群体频率）定义，而不是由化学定义。→ 对我们：**先问「我们的标签来自哪一次读数」，再问「模型多准」**；标签定义决定模型上限。
2. **两个提升数不同分母，不许相加或混用**。29.2% 的分母是「模型精挑 + 真实合成纯化的 96」，>2 倍富集的分母是 Lib1 全库随机抽样，5 倍/2.6–4.8 倍的分母是 6 个变体的湿实验。摘要把三者压成一句（>4.9-fold、~30%、~5-fold），阅读时容易误当成同一个漏斗的同一个率。
3. **4.9 倍这个对比缺少同期对照**。Lib1 与 Lib2 是不同生成批次、不同结构分布（Fig 5D 明说两个库的物理特征 marked differences），正文没有「用旧的物理指标同样挑 96 个」的前瞻平行组；而 Lib1 的绝对命中率（~6%）在正文里根本没有以 n/n 形式出现，只能反推。→ 我们引用时只许引用「换了筛选器之后末端命中率变好」这个**方向**，不许引用 4.9 倍当作可迁移的量。
4. **标签泄漏风险无法排除**：做「筛子考卷」的特征分析（L2）与训练标签（L1）来自同一批回收/丢弃数据，再用 80/20 随机切分做回顾基准；本底稿未说明切分是否按骨架聚类。若同族设计同时进训练与测试，P(MWU)<0.0001 与 top-50 富集都会偏高。
5. **他们的成功路径对我们最有用的一点，是把「判据失效」做成了一句可引用的、带统计口径的结论**（FDR 0.05 + 但无单特征有效）。我们目前缺的正是这种「把某条判据在真值面板上判死」的写法。
6. **从 filter 降级为 feature 是关键角色转换**：Rg、AF3 pLDDT、ddG 这些量没有被丢掉，而是从「一票否决」改成「喂给模型的节点/图特征」。对我们：Foldseek 命中、pLDDT、催化位点几何更适合作为特征而非闸口 —— 但前提是先有一个能训它的数据集。

## 7. 局限与失败（作者的 + 我们读出的）

**作者承认的**：先验指标无判别力（第 5.6 条）；distal 突变解不开动力学耦合（第 2.6 条原句）；Lib1 回收比例低到必须专门解释切分策略；no feature is individually an effective discriminator。

**我们读出的（每条给证据位置）**：

1. **「全文级」但底稿没有 Methods**：芯片几何与流速、DE 配方、NGS 深度、QM 泛函、SaProt/GVP-GNN 的架构与超参全部缺失 → 本篇**不可复现**，我们只能借用它的口径纪律，不能声称复算。
2. **通量分母链断在图里**：每轮唯一设计数只在 Fig 3A（"The total number of unique"），轮数也只有定性描述。因此「筛几轮、每轮削掉多少」在文本层面不可台账化 —— 这不是我们的疏漏，是底稿的物理边界。
3. **末端小分母极易被误读为全池命中率**：145 个表征的单体设计 100% 有活性，是「先按荧光富集、再按群体频率选 145」之后的结果；Lib1 的库容量与全池阳性率在正文里没有数字。任何把这句转述成「设计出来 100% 有活性」的写法都是错的。
4. **液滴阳性 ≠ 纯化活性，缺口未被量化**：28 个活性设计里只有 16 个能给出可测 KM 与催化，即**约 43% 的阳性在复验阶段掉队**；正文把解释放在 fig S24–S27（本地缺失），没有对这一缺口做机制分析。由于训练标签正是液滴读数，这个缺口会直接进模型。
5. **阴性标签里混着「表达/分泌失败」**：周质分泌是筛选前提（第 2.3 条），本底稿未见把不表达、不分泌与「折叠对但无催化」分开的对照；模型很可能先学会了「会不会分泌到周质」。
6. **单一化学体系**：一个金属（Zn）、一个反应（酯水解）、一个底物（FDBz）。「平台可扩展到其他反应」是作者的展望而非结果（"it could be extended to either"）。
7. **对照方法口径不齐**：与 MULTI-evolve 的优劣比较用的是对方论文的倍数区间，不是同一库同一底物重测。
8. **预印本，未经同行评议**；所有数字待正式版核对。
9. **40% 这个 Lib1 基线的分母在正文里未定义**（只写 typically observed），与 16/28 的对比口径不清 —— 与 `sources/cao.md:477` 的未核实条目一致，本卡沿用该保留意见。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **把「标签源」与「下单验证」明确分成两级**：他们让百万级液滴读数负责造标签（L1），让 96 个纯化候选负责下结论（F2）。对应我们：先建一层尽可能便宜的**反应级读出**（哪怕是 96 孔/微孔级的产物检测）专门产标签，再让模型挑一小批上 LC-MS/MS 做产物身份确证。两级之间的富集比（enrichment）才是模型的成绩单。
2. **用「存活 vs 丢弃」的分布检验把判据判死或判活**：他们在自己的真值面板上跑 Mann-Whitney + Benjamini-Hochberg，得到「组间显著但无单特征可有效判别」这句结论。我们照做：把 S0/S1/S2 三种结局做成真值面板，对每个既有判据（Foldseek 命中、pLDDT、催化位点几何、界面/活性位点物理量）报同一套检验，判据不上考卷不许进漏斗。这比继续调阈值有用。
3. **命中率必须分层报口径，并同时给一个与分母无关的量**：他们除 28/96 之外还给了 top-50 富集 >2 倍 vs 随机抽样。我们任何筛选器都要同时报：① 全池/提名池分母的绝对率；② 末端实测分母的绝对率；③ 相对随机抽样的 enrichment。**只报②或只报③都算不合格**。
4. **负样本也是通量的产物**：sdDE 的价值一半在「几百万个没被选中的设计也留下了频率信息」。对应我们既有交付规则（检索类交付每层一个 sheet、含失败与 UNKNOWN/METHOD_FAIL 状态），要把未通过候选的读数一并归档，否则训不出负类。
5. **只训排序、不训绝对值**：他们的分类头输出 True/False 再转 ranking score，突变端也只用 Precision/Enrichment/Recall@n%。标签噪声大时这是正确取舍，我们 likewise 不给模型加「预测 kcat」这种它没有标签可学的目标。

**不可迁移（为什么不能照搬）**

1. **FDBz 那套原位荧光化学在 UAA 反应上不存在**。FDBz 一步水解直接释放荧光素，才能把「一个液滴 = 一个设计 = 一次活性读数」成立。UAA 合成酶/氨酰化的读出需要核酸与产物身份（氨酰化 tRNA、ppuUA 类产物），没有等价的「底物自身变荧光」通路 —— 所以**百万液滴通量这一步在我们这里没有化学前提**，照搬会得到一池假阴性。任何「我们也上微流控百万通量」的计划必须先回答：单个微滴里靠什么信号区分产物与底物。
2. **29.2% / 4.9 倍 / >2 倍富集不许当作 UAA 的成功概率引用**。它们是「Zn + FDBz + 这一套物理生成器」的数，且分母是模型精挑的 96。按 DP2R 口径：既不许把 binder 的 pAE/ipTM 阈值当 UAA 酶活闸口，也不许把酶液滴筛选的命中率当我们的先验成功概率。
3. **他们的「活性」标签不能等价于我们的「有产物」**。液滴荧光过门混入了表达/分泌成败；我们的对应读数会混入可溶表达、非特异水解与背景转化。若不在标签层加表达对照（融合报告或 WB/质谱肽段计数），训出来的筛选器会先学会「会不会表达」。
4. **本底稿无 Methods → 架构与阈值不可复现**，因此这条线对我们只能作为**方法论与口径的参照**（design-test-learn 闭环、标签源分层、enrichment 报告法），不能作为「已被证明有效的具体模型结构」来引用。
5. **QM 在这里只做过渡态几何（theozyme 输入），不做反应能垒评价**；全文无 MD、无自由能微扰。所以本文**不能**为「用 QM/MD 判催化」提供命中率背书 —— 它给的恰好是相反方向的证据：先验物理指标在这个体系里被证明无效，末端答案是湿实验通量。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/C23_PPR1259026_text.txt

- 本地纯文本：`fulltext/C23_PPR1259026_text.txt`（bioRxiv 全文页 → fullTextXML 标签剥离、HTML 实体解码、空白折叠，未改写内容；同源 XML `fulltext/C23_PPR1259026_fullTextXML.xml` 仅用于溯源，不参与逐字比对）。
- 对照底稿：`sources/cao.md:366–380`（原卡，含同一批关键引句）、`:422`（筛选级联总结表 C23 行）、`:438`（物理分数失效→神经网络置信度这条逻辑链）、`:461`（QM 角色判定）、`:477`（未核实清单第 7 条：Lib1 绝对投测数与 40% 的分母）。
- CSV 字段映射：本文第 3 节 ↔ 计算筛选判据/阈值数字/候选生成方法；第 4 节 ↔ 候选数递减/实验命中率/成本统计引用；第 8 节 ↔ 在方法演进链的位置。
- **本卡自检**：由门禁脚本以 --only C23 --no-report 执行（编号里含空格或分号时参数需加引号；本编号不需要）。（该脚本把卡内所有不含中日韩字符、被直双引号包住、≥20 字符且 ≥12 个字母的片段，在声明的底稿里逐字查找；任一条不命中即 FAIL）。引句只取自本底稿，跨参考文献编号与图注断句处一律拆成两条；术语与状态名不加英文引号；底稿中 ∼、µ、α 等特殊字符若落在引句边界则改在引号外转述，避免抄写差异造成假红。
- **本底稿的边界（复核时请注意）**：正文只到 Discussion 与 References，无 Methods 段；Fig 内数值（尤其 Fig 3A 每轮唯一设计数、Fig 2F/G 标定曲线）与全部 Supplementary/table 不在本地。凡本卡写「正文未给出」处，复核者不应在正文里找到它。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 76 条逐字引句来自许可受限的第三方来源（C23；CC_BY_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（bioRxiv 预印本，2026-06-23，DOI 10.64898/2026.06.23.733994，未经同行评议）
target=de novo 锌水解酶（Zn-His3 配位）催化合成荧光底物 FDBz 的酯水解；两代库 Lib1 与 Lib2；派生的 3-4 与 30-3 两个家族的突变体库
backbone_generation=物理-based 生成（非扩散模型）：量子化学算底物过渡态几何 → theozyme（枚举 Zn 三配位位点的 His 几何与 rotamer 存 RIF 表 + RIF 搜过渡态稳定作用 + 扰动采样）→ Monte Carlo 片段装配（ProBuilder）自下而上建骨架 → Rosetta 与 ProteinMPNN 序列优化；Lib2 沿用同一生成器
computational_filters=结构硬筛（三个配组 His 必须齐全 + 存在有利的过渡态相互作用）；Rosetta 能量指标排序；AF2 评预组织与结构稳定性；AF2/AF3 的 design-vs-prediction 对齐 = in-silico success；ESM2/qTM/Foldseek 仅用于多样性核查不当闸口；最终筛选器换成数据驱动的功能预测器（SaProt 微调 + Foldseek 结构 token 做突变排序；GVP-GNN 融合 ESM2 embedding + AF3 残基级 pLDDT + 3D 坐标径向基图 + 锌配位专用 attention，二分类头转排序分做活性判别）
thresholds=标签/存活定义：population fraction > 0.0004 或在最后一轮被富集；判据失效检验：FDR-adjusted P < 0.05（Mann-Whitney U + Benjamini-Hochberg）且无单特征可有效判别；活性预测器测试集分离：P(MWU) < 0.0001 与 P(KS) < 0.0001；两处基准均为 80/20 训练/测试切分；theozyme 采样、His 齐全、Rosetta 排序与 in-silico success 原文均未给连续型数值阈值（只写 align to a sufficient degree）
md_used=否（本地底稿无显式溶剂 MD、无自由能微扰/MM-PBSA/metadynamics；结构验证靠 AF2/AF3 预测与 X 射线结晶）
qm_used=是（仅用于计算底物过渡态几何，作为 theozyme 构建的输入；不做反应能垒筛选或排序）
experimental_methods=oligo 库合成片段基因并拼接全长基因 → E. coli 周质表达（阿拉伯糖诱导 + OmpA 信号肽，EGFP 做定位与泄漏对照）→ 单细胞与 ZnSO4 及 FDBz 共包封成单分散双乳液滴 → sdDE-FACS 多轮分选（首轮宽门保召回、后续收紧富集、不同底物浓度）→ 分选池深度测序 → 145 个设计纯化与 Michaelis-Menten 动力学 → 代表性设计 X 射线共结晶 → error prone PCR 突变库 + 同一液滴平台筛选
pipeline_counts=通量口径：millions 个液滴/单次运行、thousands 滴/秒、检出下限 <1nM 荧光探针（5 个数量级动态范围）；Lib1 多轮分选后 final enriched pool 343 个唯一设计 → 选 145 个纯化表征（每轮回收唯一设计数只在 Fig 3A 图内，正文未复述，故轮数与每轮削减量在文本层面不可台账化）；序列空间 2 个家族映射 >10^5 个变体（单到三突变）→ 三元空间 >1.9×10^9 组合中取 top 6 下单；结构空间由模型为 Lib2 提名 thousands 个设计 → 实际合成并纯化 96 个候选
hit_rate=分母口径逐条钉死：Lib2 为 28/96 = 29.2%（分母 = 模型精挑且真实合成纯化的 96，不是 Lib2 提名池 thousands，也不是生成全集）；同批 16/28 约 57% 给出可测结合与催化；Lib1 的绝对命中率正文未以 n/n 给出，约 6% 只能由 29.2%/4.9 反推，故 4.9 倍是相对上一代库（不同批次、不同结构分布）而非同期前瞻对照；Lib1 表征池分母为 145（343 富集池的子集），其中单体设计 100% 可检出活性属选择后比例，严禁写成全池命中率；模型自身贡献另用以分母无关的富集口径表达：结构活性预测器 top-50 富集 >2 倍（vs 随机抽 Lib1）、序列模型 top-50 富集 >50 倍（vs 随机抽样）
best_metric=正文级：变体 3-4 对 FDBz 的催化效率约 1.6×10^8 M^-1（速率提升约 10^4 倍），Lib1 全体 kcat/kuncat 跨 10^2 至 >10^4；三元突变体 kcat/KM 提升 2.6 至 4.8 倍（vs 野生型）、超过此前最佳突变体 2.1 至 4.8 倍；Lib2 两个模型选中设计的 -logKtx 超过 Lib1 最优且可与天然酶（cyclophilin、carbonic anhydrase 参照）相当；KM 与 kcat 的逐条数值在 table S3，本地未取
cost_or_stat_note=通量侧只给量级（millions 液滴/run、thousands 滴/秒、100 µm 喷嘴、5 个数量级动态范围），无成本数字；昂贵末端为 96 个候选（Lib2）与 145 个纯化表征（Lib1）的合成/表达/纯化/动力学与 2 个结晶结构；芯片参数、测序深度、GPU 时数等因本地底稿不含 Materials & Methods 而未记录（原因：底稿正文止于 Discussion 与参考文献）
role_in_timeline=筛选逻辑的第三次转向：先验物理与 DL 指标对 de novo 酶失效（作者以 FDR 检验明言 conventional metrics 与实验活性无显著相关）→ 自建 sdDE-FACS 把功能读出做成百万级通量 → 用回收/丢弃的液滴标签训练合成适应度景观（SaProt 突变排序 + GVP-GNN 活性预测）→ 由模型决定下一批 96 个投测，末端命中率 约6% → 29.2%；这是曹组从 binder 漏斗（C02/B09 的 ddG 与 pAE_interaction）转向「用通量造筛子」的一环，也是其论文中唯一以数据闭环取代先验判据的实证
source_pointer=data/literature_cards/fulltext/C23_PPR1259026_text.txt（引句底稿，65,006 B；同目录 fullTextXML 327,325 B 为同源件）；sources/cao.md:366-380 原卡、:422 级联表 C23 行、:461 QM 判定、:477 未核实清单
CSV回填-->
