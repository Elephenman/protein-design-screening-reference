# 多轮迭代证据台账（仅研究产物，不改任何现有文件）

来源：`data/literature_cards/*.md`（152 行文献 CSV 的精读卡）。产出日期：2026-11-07。
方法：Glob/Grep 定位 + Read 片段读取；每条事实附卡文件名、原句摘录、证据级别与 `引句底稿:` 声明。所有卡均找到，无"卡缺失"。B10 与 C08 是同一张合并卡（同一工作双 CSV 编号），只记一行。
口径约定：每个百分数写明分子读数与分母池；"闸口形分母"=按排名取 top-N 送测，非随机样本；卡 §6 标"以下为推断"的内容单独标注，不算文献结论。

## 一、逐行迭代台账

### B17 — Lauko et al. 2025 Science：de novo 丝氨酸水解酶，PLACER 反应态系综筛子（Baker 组）
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B17_Lauko-2025_Science_serine-hydrolase-placer.md`；引句底稿: `data/interim/baker_lit/ft/serinehydrolase2025.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| P0 | NTF2 固定骨架库 + RosettaMatch + LigandMPNN + AF2（另要求催化氢键全形成） | 正文未给计数 | 有活化丝氨酸、零转换数 | 结构吻合但装不进主链 oxyanion 接触 | 换生成范式：RFdiffusion 围 motif 长新骨架；失败样本回收进 812 设计回溯分析 |
| r1 | RFdiffusion + LigandMPNN，仅 AF2 筛（Ser-His dyad + 1 个主链 oxyanion） | 129 条送测基因 | 2 条酯酶活性（1.6%）；FP 标记 3% | 进度曲线约 1 酶当量后平台：AEI 酰化中间体失活 | r2 加 PLACER apo 态 Ser-His 氢键筛；r1/r2 特意做成活性位复杂度相同、只有筛子不同的对照 |
| r2 | 同上 + PLACER apo 态筛 | 192 条送测基因 | 10 条活性（5.2%）；FP 标记 17%（5 倍） | 仍单周转；过 AF2 者仅 1.6% 被 PLACER 判预组织 | r3 把催化酸 + 第二 oxyanion 写进 motif，并要求 apo+AEI 两态预组织 |
| r3 | triad + 双 oxyanion motif；一次性约束生成失败后改两步搜索（10,000 骨架→2238 motif，r1/r2 仅 108） | 132 条送测 | 111 FP（84%）→20 水解 4MU（18%）→2 多轮转换（1.5%） | 812 设计回溯定位根因：失活设计在 AEI 态转 g+ 旋转异构、酰基挡住水解水 | r4 起按根因重设计 + 筛子从 2 态扩 4 态 |
| r4 | 两态/四态过滤各送一批 + 根因重设计 | 45 / 11 条 | 38 FP→9 活性（20%）；10 FP→8 活性（73%） | 四态筛更富集；重设计保住 T99 活性旋转构象者更活 | 继续按结构根因改（第二 oxyanion 取向） |
| r5 | 根因修补轮 | 20 条 | 2 条显著酯酶活性（180 / 1400 M⁻¹s⁻¹） | r5-kent1 约 10 轮转换后仍失活（作者承认未解决） | r6 换新催化几何验证管线泛化 |
| r6 | N+1 oxyanion 新几何 + 大底物，同一管线无历史数据 | 66 条 | r6-momi 1,240 M⁻¹s⁻¹，一次成功 | 反应全程预组织筛可迁移到新几何 | r7 在母体上局部重生成提活 |
| r7 | 固定母体骨架/序列，只扩散新生 N 端 20–50 aa 次结构 | 65 条 | 65 条全部有活性；最佳 4,300 M⁻¹s⁻¹（3.5×） | 局部重生成 + 同一套闸口复筛有效 | r8 换几何来源继续 |
| r8 | 借 subtilisin Asn155 平面外 oxyanion 几何重建 56–91 区段 | 150 条 | 最优两条对 r3-super k_cat 8×/7×、k_cat/K_M 19×/13× | 设计内氢键在羰基平面内、天然在平面外 | —（末轮） |

- 原句："two round 1 designs (1.6%) and 10 round 2 designs (5.2%) showed catalytic activity"；"Of 132 round 3 designs, 111 (84%) displayed FP probe labeling, 20 hydrolyzed 4MU substrates (18%), and two designs (1.5%) displayed multiple turnover activity"；"Only 1.6% of round 2 designs that passed the AF2 RMSD filter were predicted to be preorganized by PLACER"；"Of 65 designs tested, all showed activity"；"experimental characterization of the resulting designs revealed activated serines but no catalytic turnover on ester substrates, despite a close match between the experimental and designed structures"
- 不能这么用：①三个百分数读数不同（r1/r2=酯酶活性，r3 的 1.5%=多轮转换，同分母下水解是 18%），不能画成一条"成功率上升曲线"；②另一个 1.6% 是 AF2 通过者中 PLACER 通过率，与湿实验命中无关——同篇两个 1.6% 必须分开；③r2→r3 同时改了 motif 复杂度与筛子状态数，提升不能单独归因 PLACER（干净对照只有 r1/r2）；④PLACER 拒绝者从未送测，无反证臂，只证明富集器不证明必要条件；⑤多轮转换绝对命中是个位数，无置信区间。

### B18 — Kim et al. 2026 Nature：de novo 金属水解酶 ZETA，失败归因→theozyme 重写（Baker 组）
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B18_Kim-2026_Nature_metallohydrolase-zeta.md`；引句底稿: `data/interim/baker_lit/ft/metallohydrolase2026.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| R1 | RFdiffusion2 + theozyme（未显式含通用碱） | 96 条（5,120 轨迹过闸后 top-96，闸口形分母） | 86 可溶；5 高于背景；1 条 >10³ M⁻¹s⁻¹（ZETA_1 16,000±2,000） | D67A 突变对 k_cat/K_M 影响小却增强 Zn 结合→怀疑竞争性 Zn 位点；Chai-1 复核 | R2 theozyme 显式写入通用碱 + 换新版 RFdiffusion2（随机初始化、3 倍数据重训） |
| R2 | 新 theozyme + 新 RFdiffusion2，96 条/37 骨架 | 96 条（同为闸口形分母） | 85 可溶；11 活性（3 倍）；5 条 >10⁴；ZETA_2 53,000±5,000 | 活性位几何按设计摆位 | — |
| 否证 | 回溯表达 7 条被 PLACER 过滤掉的 ZETA_1 家族设计 | 7 条（被拒子集，非随机） | "very low or no activity" | 筛子拒绝方向正确 | 给 PLACER 闸口提供反证臂 |

- 原句："Eighty-six out of ninety-six designs were expressed and soluble"；D67A "had little effect on k cat / K M and increased Zn( II )-binding affinity"；"The success rate in the second design campaign was considerably higher than the first campaign"；被拒设计 "very low or no activity"
- 不能这么用：①1/96 vs 11/96 用的是 >10³ M⁻¹s⁻¹ 口径；R1 有 5 条高于背景，放宽口径比值就变——引用必须带活性阈值；②R2 同时改了 theozyme 与生成器版本，归因不干净；③两轮 96 都是排名截断的闸口形分母；④两轮均零定向进化，不是湿实验成熟证据；⑤数值阈值细节在 SI 未取回。

### B10-C08 — Yeh et al. 2023 Nature：de novo 荧光素酶 LuxSit（同一工作、CSV 双编号，只算一条证据）
- 证据级别 / 底稿：全文级 FULLTEXT（Methods 不在本地文本）；卡 `B10-C08_Yeh-2023_Nature_luciferase-dl.md`；引句底稿: `data/interim/baker_lit/ft/luciferase2023.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| R1 | DTZ 底物：4,000 对接→NTF2→1,615 hallucination 骨架→top 50,000 对接→RosettaDesign→4 道物理筛→oligo pool→菌落发光成像 | 7,648 条 oligo pool（菌落成像口径） | 3 条活性（0.039%） | 拿到活性位几何知识：哪些 His/Arg-底物相互作用几何成功 | R2 换 h-CTZ 底物 + pLDDT>92 骨架预筛 + 写入 R1 成功几何 + ProteinMPNN 替换 RosettaDesign |
| R2 | 上述三处同改 | 46 条表达纯化（与 R1 分母口径不同） | 2 条活性（HTZ3-D2/G4，4.3%） | 命中率升但两条活性弱于 LuxSit（约 25%/58% Imax） | 命中后 SSM + NNK 组合成熟 |
| 成熟 | 口袋 SSM→60/96/110 三位点 NNK 全组合 | 组合库（正文未给总数） | A96M 16×、M110V 19×→LuxSit-i >100× 光子通量 | 组合优于单点 | — |

- 原句："Three active designs were identified"；"The success rate increased from 3/7,648 to 2/46 sequences in the second round, probably owing to the knowledge of active-site geometry from the first round and the increased robustness of the ProteinMPNN method of sequence design"
- 不能这么用：①B10 与 C08 不是两条独立证据；②R2 同时改底物、序列方法、几何约束三件事，"probably owing to"是作者推测性归因，不是受控结论；③3/7,648（菌落成像）与 2/46（表达纯化）分母口径不可比，4.3% 不是 0.039% 的 110 倍方法提升；④唯一明写的数值阈值只有 pLDDT>92，其余在 SI；⑤无 LuxSit 晶体结构（AF2 1.35 Å + SSM 一致性替代）。

### B24 — Qian et al. 2026 Nat Commun：SAPP/DMX 平台 + RSV 结合体寡聚化战役
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B24_Qian-2026_NatComms_SAPP-DMX.md`；引句底稿: `data/interim/baker_lit/ft/accelscaling2026.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| C1 | 一条计算漏斗：21,400 RifDock→FastDesign→物理筛→best 5,000 motif→graft | 31,394 条 oligo pool 送合成（这不是三轮，是同一漏斗的三段） | —（计算段无湿读数） | — | 进 YSD |
| C2 | YSD 4 轮分选（1 μM 起 3 倍稀释）→命中者 SSM+组合库 | 31,394 池→分选富集（每轮计数正文未给） | cb13 35 nM；cb4=cb13+7 点突变（成熟轮） | 非共价寡聚体与展示技术不兼容 | 寡聚化改用 SAPP 阵列直测，不再走展示 |
| C3 | 新设计轮：2 binder×27 寡聚化域×N/C 端+4 对照 | 58 构建体（每 binder 各 58） | cb13 组 19/58、cb4 组 33/58 组装达目标寡聚态（SEC 99% CI，表达>0.1 mg/4mL） | 成熟后的 cb4 组装兼容率更高；几何/朝向造成 10–25× 功能差 | 功能验证 |
| C4 | 活病毒中和 | 组装成功的寡聚构建体 | IC50 40/59 pM vs 单体 5.4 nM vs 抗体 MPE8 156 pM | C6/C8 高价无增益 | — |

- 原句："31,394 designs were ordered as an oligo pool (Agilent)"；cb13 "had an affinity of 35 nM for RSV F protein"；"The success rate was higher than for cb13 (33 of 58 constructs assembled to their target oligomeric state)"；"The oligomeric constructs vastly outperform monomeric cb13 with nHALC2_065 and nHALC3_919 having IC50s of 40 and 59 pM respectively, compared to 5.4 nM for their monomeric counterpart"
- 不能这么用：①21,400→5,000→31,394 是一条漏斗不是三轮迭代，真正的"轮"是 YSD 成熟（C2）与寡聚化新设计（C3）；②19/58、33/58 是两个结合域的个案，不是通用寡聚化成功率（卡 §7 明写）；③SEC 判据是尺寸不是形状；④全部读数是静态结合/组装，与催化周转无对应；⑤作者定位 "primarily intended for screening purposes"，有假阴性。

### C23 — Ke et al. 2026 bioRxiv：液滴酶筛标签喂模型→Lib2（预印本，未同行评审）
- 证据级别 / 底稿：全文级 FULLTEXT 但底稿缺 Methods；卡 `C23_Ke-2026_biorxiv_ml-droplet-enzyme-screening.md`；引句底稿: `data/literature_cards/fulltext/C23_PPR1259026_text.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| Lib1 | sdDE-FACS 百万液滴，先宽门后严门多轮分选（轮数/每轮计数只在 Fig 3A，正文不可台账化） | 末端池 343→145 纯化 | "All characterized monomeric designs displayed detectable hydrolytic activity"（入选后比例，非全池命中率） | 既有计算指标单特征无判别力（FDR P<0.05 下） | 用液滴标签训模型（SaProt >10⁵ 变体、GVP-GNN，80/20 回溯拆分） |
| Lib2 | 模型提名→合成纯化验证 | 96 条模型选出的合成候选（不是数千提名库） | 28 活性（29.2%）；较 Lib1 4.9 倍 | 28 条里仅 16 条测得动力学：约 43% 液滴阳性在纯化后掉队 | 三突变体组合空间 >1.9×10⁹，取 top 6 验证 |
| 成熟 | 三突变体 top-6 | 6 条（模型挑选子集） | kcat/KM 2.6–4.8× | — | — |

- 原句："For the initial round, we applied permissive sorting gates to maximize the recovery of potential hits, followed sort rounds were performed under stringent conditions to enrich for highly active designs."；"no feature is individually an effective discriminator"；"we synthesized and purified 96 candidates from Lib2 to identify 28 active designs (29.2%)"；"4.9-fold increase in the rate of active hits compared to that of the previous Lib1"
- 不能这么用：①29.2% 分母=96 条模型选中并合成的候选，不是提名全库；Lib1 绝对命中率正文从未给 n/n（~6% 只能由 4.9× 反推，属推算）；②无前瞻平行对照（Lib2 模型选 vs 随机选未同场比）；③液滴标签混入表达/分泌失败，16/28 动力学掉队说明标签≠纯化后活性，缺口未量化；④80/20 拆分未声明按簇隔离；⑤预印本+缺 Methods，引用须降级声明。

### B26 — Haddox et al. 2026 PLoS Comp Biol：DMS 失败模式→基准加权→能量函数重训
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B26_Haddox-2026_PLoSCompBiol_energy-retrain.md`；引句底稿: `data/interim/baker_lit/ft/energyfunc2026.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| 诊断 | RF 挑 21 个"预测稳定/实测不稳"离群设计→DMS（2 蛋白酶×6 浓度，19/21 重复，338 对照） | ~16,000 单突变（21 个刻意挑选的离群骨架上） | 156 条高稳定化（~1%，Δstability>1.0） | 救援突变指向 clashing 失败模式；直接拟合实验值不泛化 | 改走间接学习：晶体复核（clash 少 ~30%）→该基准权重×10 + 15 参数重拟合 |
| 修正 | beta_jan25 重拟合 + 护栏 | 基准分布 118 项 | KL 0.022→0.018（p=0.002）；界面 0.64→0.67；ΔΔG 持平 | 第二失败模式（设计优于晶体 ~0.1 kcal/mol/residue）只登记未修复 | — |

- 原句："~ 1% of mutations (156 out of ~16,000 mutations tested) were highly stabilizing (Δ stability score > 1.0)"
- 不能这么用：①~1% 分母=21 个刻意挑选的不稳定离群设计上的突变，不是任意蛋白突变空间，读数是蛋白酶抗性稳定性不是功能；②这是"修评分器"的迭代，不是"设计命中率提升"的迭代，没有新一轮设计送测数字；③直接拟合失败→间接学习是被迫转向，说明"有标签就能直接训"不成立；④第二失败模式未解决，作者只登记。

### K30 — Rocklin et al. 2017 Science：>15,000 迷你蛋白设计-实验闭环（摘要级，只能当量级锚点）
- 证据级别 / 底稿：**摘要级降级精读卡，无本地全文**；卡 `K30_Rocklin-2017_Science_massively-parallel-design-synthesis-testing.md`；引句底稿: `sources/cost-benchmarks.md`（§3.3 行 105–109、§五 行 185、§八 gap 8）

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| 多轮（轮数不明） | 设计-实验迭代；>15,000 de novo 迷你蛋白 + 1,000 天然 + 10,000 突变体 + 30,000 阴性对照 | 6%/47% 的分母定义缺失 | 成功率 6%→47%（稳定性代理读数） | 闭环能大幅提命中率 | 具体改了什么评分：摘要未给 |

- 原句："Iteration between design and experiment increased the design success rate from 6% to 47%"
- 不能这么用：卡 §2.4 明列缺失——轮数、每轮送测数、6%/47% 分母定义、成功的二值化口径、改了什么判据，全部不可考。只能引用为"闭环迭代可把命中率提一个量级"的摘要级量级锚点；禁止画轮次曲线、反推分母或当全文级证据。<$0.001/base 是从他文转引的成本数。

### B05 — Dauparas et al. 2022 Science：ProteinMPNN 换序列设计器救援 AF 不溶设计
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B05_Dauparas-2022_Science_ProteinMPNN.md`；引句底稿: `data/interim/baker_lit/ft/proteinmpnn2022.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| r0 | hallucination 骨架 + AF 自生序列 | 150 蛋白尝试（Fig 3A 骨架集 N=129，口径不一卡已标） | 多数不溶，中位可溶产量 9 mg/L | 骨架可设计但序列层失败 | 骨架不动、弃原序列，ProteinMPNN 重设计 |
| r1 | 固定骨架 + ProteinMPNN 新序列 | 96 条 E. coli 表达 | 73 可溶（中位 247 mg/L）；50 SEC 寡聚态正确 | 序列层问题可被换设计器救援 | 同法用于环状寡聚体（Rosetta 40% 可溶/0 正确→MPNN 88%/27.7%）与 Grb2 支架救援 |

- 原句："the AF generated sequences were mostly insoluble (median soluble yield: 9 mg per liter of culture equivalent Figure 3A )"；"we kept the backbones of the original designs fixed but discarded the original sequences and generated new ones using ProteinMPNN"；"of 96 designs produced in E. coli , 73 were expressed solubly (median soluble yield: 247 mg per liter of culture equivalent, Figure 3A ) and 50 had the target monomeric or oligomeric state as assessed by SEC"
- 不能这么用：①150/129/96 三个分母口径不一致（卡已标），73/96 只对 96 条送测子集成立；②只救序列层失败，骨架失败换 MPNN 无用；③纳米颗粒 13/27 骨架一例作者自述总成功率与 Rosetta 相当——收益是人力/时间不是命中率；④NLL 与实验成功的相关是作者提议未验证。

### B12 — Vázquez-Torres et al. 2024 Nature：螺旋肽结合体，结构扩展成熟 + 阈值漂移反面教材
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B12_VazquezTorres-2024_Nature_helical-peptide-binders.md`；引句底稿: `data/interim/baker_lit/ft/helicalpeptide2024.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| r1 | 参数化沟槽骨架直接设计 | 每靶 12 条 | PTH/GCG/NPY 各 3/4/8 结合，但仅 µM 级 | 亲和力不够 | r2 Inpainting 结构扩展 + MPNN 重设计 |
| r2 | 结构扩展 + 序列重设计 | 分支分母 46/96 等（互不可比） | 亲和力提升约 3 个数量级 | 消融：结构扩展是关键；仅对原界面 MPNN 重设计不 measurably 提亲和 | — |

- 原句："Many of the designs bound their targets (3, 4 and 8 out of 12 to PTH, GCG and NPY, respectively) but with only micromolar affinities"；"the structural extension was critical to the improvement in binding affinity"；"Precise metrics cutoffs changed for each design campaign to get to an orderable set, but largely focused on"；"The precise values used for filtering were chosen to reduce the set down to 46 designs"
- 不能这么用：①阈值是预算驱动裁池（"减到 46/96 条可下单"），不是可复现物理判据——这是"阈值漂移"的实锤，各分支 12/66/192/46/96 分母不可横比；②柔性靶路线亲和力丢失是作者诚实阴性，说明该成熟法不普适；③hallucination 对抗序列被 MPNN 救援一例与 B05 同型，不重复计证据。

### B14 — Glugl et al. 2024 Science：partial diffusion 当计算亲和力成熟
- 证据级别 / 底稿：全文级 FULLTEXT（本地无 Methods）；卡 `B14_Glugl-2024_Science_tnfr-free-and-partial-diffusion.md`；引句底稿: `data/interim/baker_lit/ft/tnfr2024.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| r1 | free diffusion 从头设计 | 96 条（排名截断） | 取最佳者进 r2 | mb1 骨架已接近该结合模式理想解 | r2 只挑最佳做 partial diffusion |
| r2 | partial diffusion（每起点 25,000 轨迹、15–25 噪声步） | 25,000 轨迹→pae 分层裁到 32 | mb2 亲和力 +3 个数量级；mb1 提升小 | 4-1BB 关系更远，一轮不够 | 对 4-1BB 再加一轮 partial diffusion 才达 pae_interaction<7 |

- 原句："Improvements were smaller for the more regular TNFR1_mb1 backbone; free diffusion sampling appears to have already found a close-to-ideal solution for this binding mode."；"For the even less related 4-1BB, an additional round of partial diffusion was required to achieve a pae_interaction less than 7"；"no random or experimentally guided optimization was involved other than selecting the best of the 96 first round designs for partial diffusion"
- 不能这么用：①pae 分层（<20→<7.5→<5→<7）是把 25,000 裁到 32 的裁池手段，不是预注册阈值；②"再加一轮"无事先触发判据，属事后决定；③收益依赖 r1 起点质量（mb1 反例）；④无失败候选反证核查。

### B20 — Ahern et al. 2026 Nat Methods：RFdiffusion2/AME——方法版本迭代，不是设计多轮（反面）
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B20_Ahern-2026_NatMethods_rfdiffusion2-ame.md`；引句底稿: `data/interim/baker_lit/ft/rfdiff2_natmeth.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| 基准对比 | 旧法 vs AME 同一 41 个 theozyme 任务 | 41 任务（in silico） | AME 41/41 vs 旧 16/41 自洽通过 | 湿实验另测：4/96、3/96、5/96、11/96 等（96 为闸口形分母） | 无设计轮次迭代；theozyme 扩展假设未检验 |

- 原句（卡 §7 中文）："AME 的'成功'是 in silico 自洽性，不是活性——41/41 与湿实验 4~11/96 之间隔着一道没有量化的鸿沟"
- 不能这么用：41/41 不能当命中率引用；本文是生成器版本对比，不构成"这轮→观察→下轮改"的设计迭代链；训练成本 17 天×24 A100 是方法成本不是筛选成本。

### B22 — Bennett et al. 2025 Nature：RFantibody——回顾性判据升级 + OrthoRep 湿成熟
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B22_Bennett-2025_Nature_rfantibody.md`；引句底稿: `data/interim/baker_lit/ft/antibodyRFdiff.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| r1 | VHH/scFv 设计 + RF2 闸口 | 各库送测（分母见卡） | 命中率 0–2% | RF2 闸口依赖特权信息：hotspot 100%→10% 时 80.3%→52.6% | 回溯加 AF3 ipTM 判据 |
| 回溯 | AF3 ipTM 复核已送测设计 | 已下单 VHH 全体的 9% ipTM>0.6；scFv 库 4% 过 ipTM>0.85 但 5/6 确证命中都过 | AUC 0.86 | 一条 wrong-dock 命中若当初用 AF3 会被错杀 | 提议纳入 ipTM 筛——**未前瞻重测命中率** |
| 成熟 | OrthoRep 定向进化；组合式同表位 CDR 洗牌 | 进化库（正文口径） | 亲和力 ~2 个数量级提升，cryo-EM 确认 pose 不变 | 固定配对洗牌无命中，组合式才救活 | CAR-T 应用失败（未解决） |

- 原句："which range from 0% to 2%"；"Overall, only 9% of our ordered VHH designs have an ipTM > 0.6, suggesting that success rate will be improved by incorporation of an ipTM filter"；"Had AlphaFold3 been used as an initial filter, this design would have been rejected..."
- 不能这么用：①ipTM 升级只有回顾性证据，"将提高成功率"是推测，前瞻命中率未测；②wrong-dock 案例同时证明新筛子会错杀真命中——判据升级有双向代价；③0–2% 是抗体从头设计现状，不能与酶/迷你结合体命中率横比。

### B23 — Sappington et al. 2026 Nat Commun：β 配对氢键互补写进生成条件（前置战役全失败后的救援）
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B23_Sappington-2026_NatComms_beta-pairing.md`；引句底稿: `data/interim/baker_lit/ft/beta_pairing2026.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| 前置 | RFdiffusion+MPNN+AF2 常规管线攻 ALK-3/KIT | 多个战役（失败库已发表） | 零结合体 | 常规管线对 β 配对界面失效 | 把氢键互补（SS/ADJ 张量）写进生成条件 |
| 新法 | 氢键互补条件生成 | 实验库 96–5000 条不等（按 in silico 通过率定预算） | in silico 9.2% vs 旧 0.98%；实验 <1% 强结合富集，绝对命中个位数 | 矛盾 PDGFRa 结构：两条都下单不做裁决 | — |

- 原句："Prior to this study, multiple design campaigns-including campaigns utilizing RFdiffusion, ProteinMPNN, and AlphaFold 2-had failed to yield binders for ALK-3"；"<1% of designs showing strong binding and enrichment"；"In silico and experimental library sizes depended on the in silico filter success rate..."；卡 §7："9.2% 是 in silico 通过率，不是实验命中率"
- 不能这么用：①9.2% 与 <1% 是两个不同世界的数，前者不能当命中率；②库规模由通过率决定→各靶分母互不可比；③绝对命中个位数，<1% 的置信度有限。

### B25 — Dowling et al. 2025 Nature：伪对称纳米笼——判据与目标正交的失败与换读出救援
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B25_Dowling-2025_Nature_pseudosymmetric-nanocages.md`；引句底稿: `data/interim/baker_lit/ft/nanocage_hier2025.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| r1 | 按能量打分预测 96 个破对称突变（>100 REU） | 82 条单突变湿测（预测挑选子集） | 仅 3/82 未组装成笼 | 正向稳定化打分对"破坏组装"目标近乎正交 | 换便宜基因型-表型读出：共组装 + native PAGE |
| r2 | 共组装筛选连接基因型与表型 | 组合库 | AAB/ABB 污染被重新利用为目标产物；意外 71 nm 颗粒→GI9 540 亚基 | 读出便宜且对准目标后路线才走通 | — |

- 原句："The 1WA3 trimer proved remarkably plastic: only 3 out of the 82 single mutants tested did not yield a band corresponding to the assembled I53-50 nanocage"；"Key to our success was having an efficient screen for connecting genotype to phenotype"
- 不能这么用：①3/82 分母=按预测自选的突变子集，不是随机突变库；②卡 §6.1 标"以下为推断"：'正向打分器做负向目标≈正交'是读卡人归纳，不算文献结论（但与 B17 静态 AF2 不够、B20 自洽≠活性同型）；③GI9 是偶然发现，不是可复制的迭代策略。

### B33 — Wu et al. 2023 Nature：超螺旋匹配蛋白-肽对，两轮真实迭代（补充发现）
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B33_Wu-2023_Nature_superhelical-matching.md`；引句底稿: `data/literature_cards/fulltext/B33_PMC10115654_text.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| r1 | 超螺旋匹配设计 | 49 条基因 | 30 单分散可溶；亲和力/特异性低 | 可溶≠好用 | r2 加四条可核查约束：口袋互异、每个非 Pro 特异接触、ddG 对靶最优、丙氨酸扫描除非特异疏水；另加 MC 对接收敛（RMSD<2.0/1.5）与 20-ns MD 氢键保持>80% |
| r2 | 四约束协议重设计 | 54 对 | 42 可溶表达；16 条亲和力与特异性显著高于 r1 | 约束前置有效 | — |

- 原句："Out of 49, 30 were monomeric and soluble"；"We tested 54 second-round designed protein-peptide pairs..."；"Forty-two of the designed proteins were solubly expressed in E. coli , and 16 bound their targets with considerably higher affinity and specificity than in the first round"
- 不能这么用：①逐靶分母在未取回的 Extended Data Table 1；②16/54 的"显著更高"无 Kd 数值阈值；③四条约束同轮齐上，无法单独归因哪条有效。

### B44 — Roy et al. 2023 Nat Commun：整合素迷你结合体，第二轮用第一轮晶体而非模型（补充发现）
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B44_Roy-2023_NatComms_integrin-miniprotein.md`；引句底稿: `data/interim/baker_lit/ft/integrin_miniprot2023.txt`

| 轮 | 这轮做了什么 | 测了多少(分母) | 命中多少(分子+读数) | 观察到什么 | 因此下一轮改了什么 |
|---|---|---|---|---|---|
| r1 | 扫 PDB 找承载 RGD loop 拓扑→理想化拼装→SSM+YSD | 首轮库规模正文未给；SSM 后纯化 9 条 | 9/9 亚纳摩尔；最佳 av6_3 Kd 1.2 nM；拿到晶体 | 晶体 C 螺旋刚体平移 ~3.4 Å：评价改接触图谱（11/13 残基对、3 盐桥全中）而非刚体 RMSD | r2 用**晶体结构**叠靶重采样两个界面环 |
| r2 | 晶体导向环重采样 + SSM 库 YSD（200 pM top5%→100 pM top1%） | 16 条设计送测 + SSM 库 | 富集 5 处界面取代→纯化 9 条全亚纳摩尔；终分子 B6_BP 0.11 nM | 数量递减靠便宜湿实验完成（16→9→4） | αvβ8 支路：200 环模型→AF2 取 9→4/9 优先结合 |

- 原句："We identified two loop regions in the design close to the integrin and sampled a range of lengths and conformations for the two loops, and selected 16 designs with loops predicted to make selective interactions with the integrin for experimental testing"；"Of the 13 interacting pairs of residues present in the cryoEM model, 11 are present in the computational design model, including all three salt bridges."；"Five substitutions at the interface which primarily increase charge complementarity were enriched"
- 不能这么用：①16 条的逐条失败计数正文不可见（卡 §7.7：无法重建混淆矩阵、无法验证 AF2 排序判别力）；②卡 §7 记录五处正文/图注数字打架（同一剂量 43.6/43.62/46.3 三写法等）；③设计侧无可复现阈值（§7.6），只可重做实验不可复算；④摘要 pM 与正文 BLI nM–亚 nM 口径不一致，pM 只在细胞表面滴定。

### B16 — Baryshev et al. 2024 Nat Chem Biol：MP3-seq——边界分类，**不算迭代证据**
- 证据级别 / 底稿：全文级 FULLTEXT；卡 `B16_Baryshev-2024_NatChemBio_mp3seq.md`；引句底稿: `data/interim/baker_lit/ft/mp3seq2024.txt`
- 原句："Initially, we chose 100 designs for testing (DHD1; Fig. 4a ), adding 52 more designs in a second round"
- 不能这么用：正文只说第二批加测 52 条扩大测量规模，未说第二轮设计依据第一轮结果改变了方法或判据——这是"加批次"不是" informed 迭代"，按任务要求明写排除。其价值在测量平台（113,569 PPI 一锅测）与 20% 设计集成功率的口径互认，不在轮次链。

## 二、可复用的迭代模式（从上面台账归纳）

以下为归纳

### 模式 1：换生成器/换范式救援（失败归因在生成端而非筛子端时）
- 触发：失败模式被定位到"生成器装不下所需特征"或"序列层不溶"，且骨架/目标本身可用。
- 支持行：B17 P0→RFdiffusion（NTF2 装不进 oxyanion）；B05 骨架固定换 MPNN（96→73 可溶）；B23 氢键互补写进生成条件（前置战役全零后）。
- 成本量级：B05 仅 96 条基因重订；B17/B23 是整条管线重跑。
- 何时不灵：B05 纳米颗粒例作者自述总成功率与 Rosetta 持平（收益在人力）；B25 证明判据正交时换生成器也没用——先归因再换。

### 模式 2：加严/加密筛子，但先做受控对照与反证臂
- 触发：现有筛子放行太多假阳性（静态自洽≠功能）。
- 支持行：B17 r1/r2 只有筛子不同的干净对照（1.6%→5.2%）+ 812 失败样本回溯标定 + r3 起沿反应坐标加密到 2 态/4 态；B18 回溯表达 7 条被拒设计证伪筛子放行方向。
- 成本量级：B17 每轮 96 孔固定送测（129–192 基因）；B18 反证臂仅 7 条。
- 何时不灵：B22 ipTM 升级只有回顾性证据且会错杀 wrong-dock 真命中；B20 41/41 in silico 与湿实验 4–11/96 的鸿沟未量化——筛子加严必须配湿实验反证，否则只是自我循环。

### 模式 3：把上一轮的结构知识写进下一轮生成约束
- 触发：上一轮拿到命中 + 结构（晶体/ cryo-EM / 成功几何统计），下一轮想提命中率。
- 支持行：B10-C08 R1 成功 His/Arg 几何→R2（3/7,648→2/46，口径不同）；B18 D67A 归因→theozyme 补通用碱（1/96→11/96）；B33 四条可核查约束（54→16 高特异）；B44 用晶体不用模型重采样。
- 成本量级：16–96 条基因/轮。
- 何时不灵：B10-C08 三处同改、作者只说 "probably owing to"——知识迁移要多轮单变量才可归因；B44 无失败计数，约束的判别力不可审计。

### 模式 4：局部重生成/partial diffusion = 计算亲和力成熟
- 触发：已有活性/弱结合母体，想在不推翻母体的前提下提活。
- 支持行：B17 r7 固定母体只再生 N 端（65/65 有活性，4,300 M⁻¹s⁻¹）、r8 借天然几何重建区段（k_cat 8×/7×）；B14 partial diffusion（mb2 +3 个数量级）；B12 Inpainting 结构扩展（~3 个数量级，消融证明扩展是关键、仅换序列无效）。
- 成本量级：B17 每轮 65–150 条基因；B14 每起点 25,000 轨迹（算力侧）。
- 何时不灵：B14 mb1 起点已近理想时收益小；B12 柔性靶路线丢亲和；B14 "再加一轮"无预注册触发判据——须事先定"何时值得再扩散一轮"。

### 模式 5：湿实验突变扫描 + 组合成熟（命中后提活/提亲和）
- 触发：有命中但活性/亲和力距目标差 1–3 个数量级。
- 支持行：B10 SSM→NNK 三位点组合（>100× 光子通量）；B24 SSM→cb4（+7 突变，且组装兼容率 19/58→33/58）；B22 OrthoRep（~2 个数量级，pose 不变）+ 组合式 CDR 洗牌救活固定配对的零命中；B44 YSD 两轮加压分选富集 5 取代（9/9 亚纳摩尔）。
- 成本量级：96 孔单点到组合库/进化库；B44 分选压力 200 pM top5%→100 pM top1% 可照抄。
- 何时不灵：B22 固定配对洗牌无命中（必须组合式）；B17 r5-kent1 成熟后仍 ~10 轮失活——成熟解决不了机制性缺陷，先归因再成熟。

### 模式 6：把实验标签喂回评分器/模型，再开下一库
- 触发：攒到足够带标签的失败+成功样本，且旧指标被证明无判别力。
- 支持行：C23 液滴标签→SaProt/GVP-GNN→Lib2（96 合成→28 活性 29.2%，4.9×）；B26 DMS→clashing 失败模式→基准×10 加权+15 参数重拟合（KL 0.022→0.018）；K30 仅摘要级量级锚点（6%→47%，分母缺失）。
- 成本量级：C23 百万液滴 + >10⁵ 变体标签；B26 ~16,000 突变 DMS。
- 何时不灵：B26 直接拟合实验值不泛化，被迫间接学习；C23 标签混入表达/分泌失败（16/28 纯化后掉队）、无前瞻对照、拆分未按簇声明——喂回前必须先修标签口径，否则模型学的是假目标。

### 模式 7：换便宜且对准目标的读出（判据正交时的唯一解）
- 触发：现有打分/读出与真实目标方向不一致或不可连接基因型。
- 支持行：B25 能量打分预测破对称 3/82 近乎全错→共组装+native PAGE 便宜读出救活；B17 三级湿读出（FP 标记→底物水解→多轮转换）逐级对准化学事件；B44 刚体 RMSD→接触图谱。
- 成本量级：B25 凝胶带读出；B17 96 孔三级。
- 何时不灵：B24 SEC 是尺寸判据不是形状判据，需功能梯度补判——换读出后仍要问"这个读出对准目标了吗"。

### 反模式清单（怎么写"不要这样迭代"）
- 阈值随预算漂移：B12 "cutoffs changed for each design campaign"、减到 46/96 条可下单；B14 pae 分层裁池。阈值要么预注册，要么明写是裁池手段。
- in silico 通过冒充实验命中：B20 41/41 vs 4–11/96；B23 9.2% vs <1%。
- 判据与目标正交：B25 正向打分做负向目标；B17 静态 AF2 对多步催化不够。
- 同轮多改无法归因：B10-C08 三处同改、B18 两处同改、B33 四约束齐上——提升真实但归因是推测。
- 只加批次不改方法：B16 第二轮 52 条，明写不算迭代证据。
- 回顾性升级不前瞻验证：B22 ipTM；且新筛子会错杀真命中（wrong-dock 案例）。