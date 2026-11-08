# [B20] Atom-level enzyme active site scaffolding using RFdiffusion2——把「指定序列位置+逆 rotamer 枚举」从酶设计里删掉

Ahern W, Yim J, Tischer D, Salike S, Woodbury SM, Kim D, Kalvet I, Kipnis Y, Coventry B, Altae-Tran HR, Bauer MS, Barzilay R, Jaakkola TS, Krishna R, Baker D（华盛顿大学 IPD；MIT CSAIL）
Nature Methods 2026, 23:96–105（在线 2025-12-03；收稿 2025-04-21，接收 2025-11-04）· DOI 10.1038/s41592-025-02975-x · PMID 41339749 · PMCID PMC12791007
开放获取（CC BY-NC-ND）· 全文 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12791007/ · 代码 https://github.com/RosettaCommons/RFdiffusion2/
（[B18] 金属水解酶是本文的配套实验论文；[B19] PLACER 是其下游打分器。DP2R 直接引用本卡时，以第 3 节闸口表与第 4 节台账为准）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B20**（组：Baker组; 通用方法学; 口径对照） |
| 本文取回方式 | 先行调研缓存（baker_lit，2026-10-16），非本轮 cards/fetch_log 抓取（fetch_log.tsv 无 B20 行）；文本为 PMC XML 抽取纯文本 |
| 登记全文 | `data/interim/baker_lit/ft/rfdiff2_natmeth.txt`（71,273 B；`sources_map.json` 中 B20 唯一登记全文） |
| 对照底稿 | `sources/baker.md` 第 265–279 行（原卡）；注意 `sources/baker.md:642` 行把 [B20] 误挂在 luciferase 语境（该处编号应为 [B10]），以本卡登记的全文为准 |
| 证据级别 | **全文级**（本卡所有英文引号片段均为该全文的逐字子串，经门禁逐字比对） |
| 未取到的部分 | Supplementary Information（Figs 1–17、Tables 1–6、Methods 节 B/D——训练超参与各设计战役细节都在里面）；正文 Methods 明确写 "A detailed description of the methods is provided in the Supplementary Information"。正文里 LaTeX 公式处有 MathJax 残片乱码（第 10–27 行），涉及公式的表述本卡只用文字复述、不引用 |

## 1. 这篇到底解决什么（大白话）

从头设计酶的规范流程是：先用 QM/化学直觉定义"围绕过渡态的一小撮官能团坐标"（theozyme），再让蛋白骨架把这撮坐标包住。旧版 RFdiffusion 只认"骨架级、带序列位置索引"的 motif，所以得先做两步昂贵的预处理：逆 rotamer 采样（从侧链反推骨架该放哪）× 序列位置枚举（组合数 L!/(L−M)! 指数爆炸）。这篇把生成模型升级到原子级（RFdiffusion2）：条件输入就是 theozyme 里那些**没有索引、没有完整残基**的侧链原子（外加配体/金属），rotamer 和序列位置改由模型在每条扩散（flow matching）轨迹里自己推断。效果：(1) 自建 AME 基准上 41 个活性位全部至少做出一条通过一致性检验的脚手架，旧法只有 16/41；(2) 湿实验侧 5 个案例（2 个晶体结构 theozyme + 3 个纯机制假设）各测不超过 96 个设计就都拿到活性酶。配套论文 [B18] 给出其中金属水解酶的完整细节。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **逆 rotamer × 索引枚举是指数级的，做不起**。原文先交代旧法的两步预处理（"Current approaches attempt to overcome this limitation for atom-level active site descriptions by"），再给判词："it is computationally inefficient and does not scale to more complex active sites as the number of"；且旧法每次运行只能押一个组合。→ **应对**：表示层革命——把 motif 残基"原子化 + 去索引"（"This ability to condition on individual atoms rather than entire residues allows us to forgo"；索引同理，"The ability to condition on motifs without specifying their indices enables us to forgo naive index"）。→ **代价**：要重训一个全新网络；且去索引训练有个非平凡的学习事实要靠架构保证——"Without any auxiliary losses,"。
2. **上一代模型训不长（训练不稳定）**。作者自述旧法依赖补丁："When training RFdiffusion and RFDiffusionAA,"，它们靠辅助损失+自条件化才在短训里达标；而去索引原子 motif 任务更难，"we expected that a stable objective would be required"。→ **应对**：整个换目标函数——flow matching（R3 用高斯概率路径、SE(3) 用 FrameFlow 的 Riemannian 形式，去掉 RFdiffusion 的旋转损失近似）；结果是 "With these improvements, RFdiffusion2 trained"，也顺带解除"必须从结构预测权重微调"的架构绑定。→ **代价**：算力账本变大——"We train the final model for 17 days using 24 A100 Nvidia GPUs"；正文没给单次推理单价（在 SI 节 B，未取到）。
3. **flow matching 的"中心化"选择会漏答案**。全局居中会把"脚手架质心–motif 偏移"泄漏给模型，推理时又要求用户预先知道这个偏移（通常不知道）；改成 motif 居中的常见修法也不彻底——"due to the interpolation scheme used in flow matching, the model is able to exactly determine this offset from any partially noised structure"，导致第一步纯噪声时的预测无法在后续步被修正（"In our early experiments with flow matching, we found that the choice of how the ground-truth structures were centered relative to the origin in training substantially affected the quality of inference outputs"）。→ **应对**：发明 stochastic centering——"which first centers the ground-truth structure and adds a small global translation sampled from a three-dimensional Gaussian such that the noised input structures only encode an approximate offset between the motif and scaffold"；推理端给用户一个显式先验接口 ORI 伪原子——"At inference time, users supply a prior belief about the placement of the motif through a special ORI pseudo-atom that specifies the approximate center of mass of the generated structure"。→ **代价**：ORI 放哪成了新的"专家直觉"自由度（[B18] 里 ORI 位置直接决定了底物两端谁埋在口袋、谁露在外面，两代设计结合取向相反）。
4. **旧基准测不到真问题**。RFdiffusion 论文的 5-EC-class 基准用的是"已索引骨架 motif、无配体"："this benchmark does not accurately reflect the"。→ **应对**：自建并开源 AME 基准："We cross-referenced the 958 hand-curated"，"After curation, we found 41 active sites spanning"。→ **代价**：M-CSA 只有残基级标注，原子只能"随机取连通子图"模拟 theozyme——作者自己承认这不等价于真催化位："It is important to note that scaffolding these atoms will not necessarily generate catalytically proficient enzymes, but these cases were extremely helpful in evaluating the ability of the network to perform unindexed atomic motif scaffolding"；且 "The AME benchmark is limited to scaffolding"（PDB 衍生 motif 的可迁移上限）。
5. **结构预测器本身会误判（配体/侧链相互作用）**。评估要复折，但 AF2 对配体体系不理想。→ **应对**：选 Chai-1——"an open-source implementation of AlphaFold3 (ref."；每个设计取 5 个 diffusion 样本降低单次预测方差（Methods 节）。→ **代价**：闸口口径绑在 Chai-1 上，讨论区承认 "The rapid development of open-source biomolecular"——即当前过滤还不是最优。
6. **湿实验端：命中率仍是"几个/96"量级，且离天然酶有差距**。五案例分别得 4/96（逆醛醇）、"several"/48（半胱氨酸水解酶）、3/96 与 5/96（锌水解酶两底物）、11/96（含通用碱第二轮）。→ **应对**：作者没有加实验轮次，而是收口在讨论区并给出归因假设："Despite RFdiffusion2's success in obtaining active enzymes across four reactions, the enzymes designed by RFdiffusion2 are not as active as native enzymes"，"Our theozymes might not be capturing all the"。→ **本文未解决**：theozyme 该扩充哪些相互作用、扩了是否就更好，都没测。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **生成**：RFdiffusion2 = RFAA 架构 + 原子级/无索引 motif 的 in-context conditioning（"atomic and unindexed motifs are provided as"）+ flow matching 目标（"the network is trained from"）。
- **训练数据操作**：PDB（去溶剂/结晶添加剂）；每步重抽 motif 做增强；每条 motif 残基随机 frame 化或原子化（原子化只给重原子随机子图）；配体给随机连通子图并间歇加 RASA 标签（"we sample a random connected"）。
- **序列**：LigandMPNN（骨架+催化侧链+配体坐标条件化）。
- **结构复核**：Chai-1（AF3 开源实现）。
- **对照管线**：RFdiffusion 基线（先逆 rotamer+索引采样转成骨架 motif，"The pipeline samples inverse"）。
- **上游 theozyme**：QM/化学推理（3 个纯机制案例用 DFT 找鞍点；Fig.1a 图注口径：theozyme 是 "generated using quantum chemistry," 的催化基团排布）。
- **没有用的方法**：MD（无）；PLACER 不在本文闸口（那是 [B18] 战役的排序器）。

### A. AME 计算基准线（in silico 漏斗）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | M-CSA 958 个精编活性位 | 与 PARITY 交叉，要求反应物+辅因子全在 PDB 晶体结构中出现 | 全部反应物/辅因子在结构内 | "After curation, we found 41"（EC 1–5 占 M-CSA 96%） |
| A2 | 每个活性位 | M-CSA 残基级标注 → 每残基取随机连通原子子图当 theozyme 蛋白部分；ligand 全构象或 partial | 正文未给子图规模阈值 | 41 个 motif 案例（难度=残基岛数 1–7） |
| A3 | 每个 motif | RFdiffusion2 默认配置采样（ORI 放 motif 质心），100 骨架/案例；每骨架 LigandMPNN 配 8 条序列 | "We evaluate RFdiffusion and"；"We assign eight sequences to" | 4,100 骨架 × 8 序列（每模型） |
| A4 | 序列 | Chai-1 复折（5 个 diffusion 样本） | 成功= (1) 任一序列任一样本上，催化残基全部重原子 RMSD <1.5 Å（按该残基骨架 N, Cα, C 对齐）且 (2) 无配体-clash（两原子距离 <1.5 Å 定义为 clash）——原文："We call a design an in silico" | "We find that RFdiffusion2 finds"；"In 40/41 cases, we find that" |
| A5 | 成功设计 | Foldseek+TM 查新颖性 | TM 分数分布 | "Most designs have low closest"；"Although the motif examples in" |
| A6 | 消融：rotamer/索引三种取法（naive 枚举 vs 模型推断 vs 原生值） | 3/4/5/6 残基岛各选 1 案例 × 每 motif 100 设计 | 各 island 档通过率（Supplementary Table 1，未取到） | "We find the best strategy is to"；"At four residue islands, we" |

### B. 湿实验线（5 个案例 = 4 个反应，正文口径见 §7）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1a | 晶体结构 theozyme ×2（逆醛醇酶四联体来自 PDB 5AN7；半胱氨酸水解酶三联体+氧阴离子洞来自 PDB 1PPN） | 直接考核"只给官能团坐标能不能出活酶"——"For two reactions, we used" | 同上漏斗（A3–A4 思路） | 见 B3 |
| B1b | 纯机制假设 ×3 | "For another three reactions,"；"we perform optimization with" | DFT 鞍点几何（方法细节在 SI 节 B/D，未取到） | Zn 案例细节全部甩给配套论文 [B18] |
| B2 | theozyme | 统一流程："In all five cases, we generate" | 结构预测复折一致性 | 每案例 ≤96 个送测 |
| B3a | 逆醛醇酶 96 设计 | IVTT 表达 + racemic Methodol 半定量活性 | 可检出活性 | "We generated designs scaffolding this theozyme, filtered them and expressed 96 in an in vitro transcription/translation system"；"found four variants that show"；最优 "We purified the most active" |
| B3b | 半胱氨酸水解酶 48 设计 | 同上 + 纯化复测 | 多周转活性 | "Among the 48 designs that were"；"the best design shown exhibited"；"better than previous results" |
| B3c | 锌水解酶 96×2 + 96（第二轮） | 复述 [B18]：4MU-butyrate 与 4MU-phenylacetate 两底物 | >背景 + 锌依赖 | "We obtained 96 designs for each"；best 77 ± 10 与 "The best enzyme for 4MU-phenylacetate had a k cat / K M of 16,000 ± 2,000"；"In a second set of 96 designs"，"the best of which had a k cat /" |
| B4 | 汇总口径 | 与旧方法对比的总宣称 | 案例数=5 | "In all cases, we found functional enzymes when testing less than 96 designed proteins"；摘要口径 "We further design enzymes for" |

**流程骨架**：生成端"原子级条件化 + 推断自由度"取代"枚举自由度"；评估端仍是 B09 式自洽性反折叠闸口，只是把预测器换成会处理配体的 Chai-1、把 RMSD 判据从骨架原子细化到**催化侧链重原子**（<1.5 Å）；实验端固定 ≤96 名额/案例。三层各自独立可查——基准（AME）、消融（残基岛×三种取法）、湿实验（5 案例）。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 958 → 41 | M-CSA 活性位经 PARITY 交叉后保留的 AME 案例数 | "We cross-referenced the 958" |
| EC 29 classes 1–5 | AME 覆盖的酶类别广度 | "After curation, we found 41" |
| 41/41 vs 16/41 | RFdiffusion2 vs RFdiffusion 通过的案例数 | "RFdiffusion2 finds solutions to"（摘要口径 "compared to 16 using previous"） |
| 40/41 | RFdiffusion2 显著优于旧法的案例数 | "In 40/41 cases, we find that" |
| 100 骨架/案例 × 8 序列 × 5 样本 | AME 评估采样规模 | "We evaluate RFdiffusion and"；"We assign eight sequences to" |
| <1.5 Å（两条） | 催化残基重原子 RMSD 闸口；clash 定义 | "the root mean square deviation"；"the design contains no clashes" |
| 7（残基岛） | 旧法与新法的难度分界 | "RFdiffusion2 is able to solve"（Fig.3b 图注）；0 通过出现在四岛 naive（"At four residue islands, we"） |
| TM 0.5–0.6 | 成功设计对最近 PDB 结构的典型 TM 分数 | "Most designs have low closest" |
| 17 天 × 24 A100 | 最终模型训练算力 | "We train the final model for 17" |
| 50%（RASA 提供频率） | 配体原子暴露度条件化的训练配比 | "By providing the RASA of each" |
| 96 → 4；6.34 ± 0.92 | 逆醛醇酶送测数/检出数/最优 k_cat/K_M（M⁻¹s⁻¹） | "We generated designs scaffolding this theozyme, filtered them and expressed 96 in an in vitro transcription/translation system"；"found four variants that show"；"We purified the most active" |
| 48 → several；248 ± 34 | 半胱氨酸水解酶 | "Among the 48 designs that were"；"the best design shown exhibited" |
| 96×2 → 3 与 5；96 → 11 | 锌水解酶两底物 + 第二轮 | "We obtained 96 designs for each"；"In a second set of 96 designs" |
| 77 ± 10；16,000 ± 2,000；53,000 ± 5,000 | 锌案例三档最优（M⁻¹s⁻¹） | "The best enzyme for 4MU-phenylacetate had a k cat / K M of 16,000 ± 2,000"；"the best of which had a k cat /"（77 ± 10 在 [B18] 台账，本文正文口径为 "higher than previously designed"） |
| 5 案例 / <96 每案例 | 总宣称的实验预算上限 | "In all cases, we found functional enzymes when testing less than 96 designed proteins"；"In all five cases, we generate" |

## 5. 结论——作者说了什么

1. RFdiffusion2 不需要指定序列位置、不做逆 rotamer 生成，"designing enzymes directly from"（摘要句），并在 AME 上 41/41 完胜旧法 16/41。
2. 让模型自己推断 rotamer+索引优于枚举、也优于用"原生值"——"even surpassing using the"。
3. 湿实验：三个催化机制、五种案例，各测 <96 条序列即得活性酶；计算端与实验端共同支持"原子级生成建模可直接从反应机制造酶"。
4. 新颖性：AME 成功设计大多与训练集结构显著不同（TM 0.5–0.6）。
5. 作者自限（讨论区）：设计酶活性仍不及天然酶（"the enzymes designed by RFdiffusion2 are not as active as native enzymes"）；theozyme 定义可能不完整；AME 只覆盖 PDB/M-CSA 衍生 motif；多过渡态酶不在基准内；过滤用的结构预测器还会被更新的开源模型改进。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的杠杆是"删预处理"而不是"加算力"**：旧管线的时间花在指数枚举上，新管线把枚举变成模型内的一次联合推断，于是同样 96 个实验名额能装进"更难的 motif"（残基岛数更多、含金属/配体）。→ 对我们：UAA 筛选的设计预算应该花在"让自由度进模型"还是"把自由度展开成网格"上，是个可核算的取舍。
2. **闸口细化到"催化侧链重原子 RMSD <1.5 Å + 无 clash"**——注意这不是通用的 pLDDT/pAE（B09 的 binder 判据在酶上被替换了）。它成立的前提是有明确 motif 可对齐。若我们未来有可信 theozyme 等价物，可照搬"对齐到化学功能基团"的判据形态；但数值阈值 1.5 Å 是针对 Chai-1 误差分布的经验线，不可挪用（换预测器就得重标）。
3. **"fewer than 96 sequences"是选择偏差友好的口径**：96 不是随机样本量，而是漏斗顶端算力的产物（PLACER/复折排名取前 96）。成功率的分母（96）本身是被闸口塑形过的——引用这套数字谈"酶设计命中概率"前，必须先把闸口整套复刻才有意义。我们目前没有这套闸口的输入前提（可信骨架+可信 TS 几何）。
4. **训练不稳定的坦白值得记住**：他们的旧模型"训久了变差"，靠换目标函数解决而不是靠调 LR/更多数据。→ 我们若在长时 MD/xTB 轨迹上观察到"越跑越差"，应优先怀疑目标/度量而不是加大采样。
5. **本文与 [B18] 的分工**是"生成器+基准"与"战役+机理反查"两张卡：任何 DP2R 引用若要谈成功率/活性数字，应引 B18（更细）；谈计算闸口/训练成本，引本篇。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：见 §5.5；另有"湿实验数字给得不齐"——Cys 案例只说 "Among the 48 designs that were"，具体检出数在 Supplementary Fig. 12（未取）。
- 文本自洽问题（审稿人视角，值得警惕）：正文先说 "In all five cases, we generate"，紧接着写 "The specifics of theozyme"，而摘要写 "three distinct catalytic"——三个口径（5 案例/4 反应/3 机制）并存但都对得上账（2 晶体 theozyme + 3 DFT 案例 = 5 案例；逆醛醇/半胱/锌×2 底物 = 4 反应；机制类型 = 3）。引用时务必注明用的是哪个口径。
- 我们读出：① AME 的"成功"是 in silico 自洽性，不是活性——41/41 与湿实验 4~11/96 之间隔着一道没有量化的鸿沟；② 计算闸口的两个 1.5 Å（RMSD 与 clash）用同一数值，正文未解释为何不分开调参；③ 单次推理成本、采样成功率→送测转化漏斗的数字全在 SI，本地不可核验，所以本卡在"候选数递减"上只能给"≤96/案例"这一端点；④ 无 MD、无自由能；QM 只在 theozyme 生成端；⑤ 配套湿实验里锌案例细节在 [B18]，本篇正文对锌部分只有摘要级复述。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么做）**

1. **"自由度进模型 vs 展开成网格"的取舍框架**（§6.1）：DP2R 里对应"枚举催化残基摆放组合"与"用生成/采样隐式覆盖"两种路线；先估组合规模（本文的 10^18 教训）再选路线，并写明选的那条的单价（本文：17 天 × 24 A100 换掉指数枚举）。
2. **闸口形态可借鉴、数值不可挪用**：把"按化学功能基团对齐的原子级 RMSD + clash 检查"作为**判据类别**引入我们未来的 theozyme-等价物评估；但 1.5 Å 阈值绑定 Chai-1 与酶 motif，换场景必须重新标定。引用规则同 [B09] §8：判据先上面板考卷，再进漏斗。
3. **"自建基准 + 开源"的组织方式**：他们把旧基准的缺陷逐条点名（索引化、无配体、案例少），再造 41 案例 AME 并放数据/代码。我们对 UAA 面板（G0/G6）的构建可直接抄这个"先点名旧口径为何测不到真问题"的论证结构。
4. **消融设计**（rotamer/索引 × naive/inferred/native 三取法 × 残基岛难度分层，A6）：便宜、可复现、把"增益来自哪个自由度"拆开——任何 UAA 判据组合都应做这种"逐自由度归还给模型"的消融。

**不可迁移（为什么不能照搬）**

1. **前提缺失**：整套方法的第一步是"有一簇可信的 theozyme 原子坐标"。UAA 合成酶三事件（S0/S1/S2）的过渡态几何在文献里没有经过 DFT+实验双确认的版本（本项目现状：机制假设，非 theozyme 级输入）。没有这个，RFdiffusion2 连输入都给不出——**本文一切数字对"没有 theozyme 的问题"外推值为零参考**。
2. **命中率/活性数字禁止挪用**：41/41、16/41 是 in silico 自洽率；<96→活性酶是已定义机制的 4 个反应的成绩。不得作为 UAA 的任何成功概率（规则 §8 与 DP2R 标准 §2：binder 的 pAE/ipTM、适配体 FEP 命中率、展示库通量都不能当 UAA 酶活判据，同理这篇的 AME/96 名额口径也不能）。
3. **Chai-1 闸口的误差结构不同**：他们验证过 Chai-1 侧链距离分布更接近天然参考才选用；我们若用同一预测器评"未表征天然蛋白+不确定的底物态"，前提（设计构象规整性、TS mimic 化学图）不成立。
4. 无 MD/QM 打分环节：本文不能为"MD/QM 逐候选打分"提供任何命中率背书（QM 只在输入端）。

## 9. 溯源与自检

- 引句底稿: data/interim/baker_lit/ft/rfdiff2_natmeth.txt（本卡全部英文引号片段的逐字比对对象）
- 本地全文：`data/interim/baker_lit/ft/rfdiff2_natmeth.txt`（PMC12791007 XML 抽取纯文本，先行调研缓存；引句在 norm（HTML 实体解码+NFKC+空白折叠）后逐字命中；注意 `<1.5 Å` 在原文里是 `&lt;1.5` 实体、Å 存在 U+00C5/U+212B 两个码点混用，本卡引句按源文件码点原样保留）。
- 对照底稿：`sources/baker.md:265–279`（B20 原卡）。已发现 `sources/baker.md:642` 的 [B20] 编号误挂（该句语境是 luciferase [B10]），回填 CSV 时不要沿用该行的编号映射。
- 关联卡：[B18]（湿实验细节与 PLACER 闸口的真正出处）、[B19]（PLACER 本体）、[B09]（自洽性反折叠闸口的 binder 版前身）。
- CSV 字段映射：本卡第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B20 --no-report` 输出 `PASS B20 quotes=N/N`（PASS 行打印命中数/总数）。正文 MathJax 残片区（L !/( L − M )! 那句）未做引句使用，避免把抽取噪声当原文。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 71 条逐字引句来自许可受限的第三方来源（B20；CC_BY_NC_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文
target=原子级活性位脚手架（AME 41 案例 + 逆醛醇酶/半胱氨酸水解酶/锌金属水解酶 5 个湿实验案例，4 个反应、3 种机制）
backbone_generation=RFdiffusion2：RFAA 架构 + flow matching（R3 高斯路径 + SE3 Riemannian/FrameFlow）+ 原子级/无索引 motif in-context conditioning；从随机权重初始化训练（不再微调自结构预测权重）；配 LigandMPNN 出序列
computational_filters=in silico 成功闸口：Chai-1（AF3 开源实现）复折后催化残基侧链重原子 RMSD（按 N,Cα,C 骨架对齐）；配体-骨架 clash 检查；对照基线=RFdiffusion+逆rotamer/索引枚举管线
thresholds=重原子 RMSD <1.5 Å；clash 定义=两原子 <1.5 Å；每案例 100 骨架 × 8 序列 × 5 Chai-1 样本；AME=41 案例（958 M-CSA 位点经 PARITY 交叉、要求反应物/辅因子齐备）；RASA 标签训练提供率 50%
md_used=否
qm_used=是（theozyme 输入端：Fig.1 口径「quantum chemistry, protein structural analysis and/or chemical reasoning」；3 个纯机制案例用 DFT 找过渡态鞍点；不做逐候选打分）
experimental_methods=IVTT 无细胞表达 + racemic Methodol 半定量活性（逆醛醇）；48 设计筛查+纯化稳态动力学（Cys 水解酶，荧光产物）；锌案例复述配套论文 [B18]（E. coli 表达纯化、4MU 酯荧光动力学）
pipeline_counts=计算：5,120 轨迹→…→96/批 为 [B18] 口径；本文 AME 线：41 案例 ×100 骨架 ×8 序列→至少 1 条过闸/案例（41/41）；湿实验：96→4（逆醛醇）、48→several（Cys）、96→3 与 96→5（锌两底物）、96→11（第二轮）；总宣称：每案例 <96
hit_rate=摘要口径「three distinct catalytic mechanisms...fewer than 96 sequences in each case」全部拿到活性候选；AME in silico 41/41 vs 旧法 16/41、40/41 案例显著占优；naive 枚举在 4 残基岛 0 通过
best_metric=k_cat/K_M = 53,000 ± 5,000 M⁻¹s⁻¹（锌第二轮最优，转引 [B18] 细节）；逆醛醇 6.34 ± 0.92；Cys 248 ± 34；锌 16,000 ± 2,000 与 77 ± 10
cost_or_stat_note=最终模型训练 17 天 × 24 A100；推理单价正文未给（SI 节 B 未取）；成功设计对最近 PDB 的 TM 多在 0.5–0.6；RASA 条件 50% 训练提供率
role_in_timeline=酶设计生成端从「残基/骨架级」降到「原子级、无索引」的一代：删掉逆 rotamer+索引枚举两道预处理，AME 成为社区基准；其湿实验侧与 [B18]（PLACER 闸口+机理反查）互为配套，构成 2025–2026 零优化酶设计的核心三件套
source_pointer=data/interim/baker_lit/ft/rfdiff2_natmeth.txt（PMC12791007 抽取文本，71,273 B）；sources/baker.md:265-279；配套论文 PMC12727532（[B18]）
CSV回填-->
