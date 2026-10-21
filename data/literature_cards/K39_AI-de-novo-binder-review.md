# [K39] AI-Driven De Novo Binder Design: From Structure Prediction to Closed-Loop Optimization（方法学综述 · 命中率与分母口径汇总卡）

Li Xinhao, Fan Zeyu, Yang Jiaping, Jiang Ruoyu, Cao Fangyu, Li Jinqian, Xie Dan, Meng Xuanlin, Sun Mingjuan, Wang Lianghua（海军军医大学生物化学与分子生物学系）
Comput Struct Biotechnol J 2026（CSBJ, Vol 35, 0070）· DOI 10.34133/csbj.0070 · PMID 42052042 · PMCID PMC13113996
开放获取（CC BY 4.0）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K39**（组：通用方法学; 口径对照） |
| 本地全文 | `data/literature_cards/fulltext/K39_PMC13113996_text.txt`（去标签纯文本，抽取版 Europe PMC/NCBI fullTextXML） |
| 登记底稿 | 全文 text.txt + fullTextXML.xml（门禁只比对 text.txt）+ `sources/cost-benchmarks.md` |
| 证据级别 | **全文级**（本卡全部引句均可在该 text.txt 里逐字命中，见第 9 节） |
| 文体 | **综述（review）**，不是单篇一手实验论文：它汇总别人报告的命中率，本卡的重点是"它转述了哪些命中率数字、每个数字的分母是什么口径" |
| 未取到的部分 | 正文未附各引用文献的原始实验明细；凡"1%–10%""1%–2%"等区间均为综述作者对多篇文献的**归纳转述**，非本文自测；本卡不把这些当成一手数据 |

## 1. 这篇到底解决什么（一句话）

它把"AI 从头设计结合蛋白"整理成一条**标准化技术栈**（结构预测 → 扩散生成骨架 → 逆折叠出序列 → 计算置信度筛选 → 高通量湿实验反馈闭环），并且专门汇总了这条栈**目前的命中率区间**、指出这些命中率**分母口径不统一、跨实验室不可直接比较**——这正是本卡（口径对照）要用的核心价值。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **筛选漏斗末端极窄，命中率的"分母"天然被压小**。原文（L231）："it is common to obtain thousands to tens of thousands of candidate binders, while experimental capacity typically allows validation of only tens to hundreds"。→ 现象：计算能造 10³–10⁴ 条，湿实验只测得起 10¹–10² 条。**应对**：不追求"测完全部"，而是把目标改成"控假阳 + 稳定排序"，并推荐只把一小撮拿去高精度验证（L298）："selecting a strategic subset of candidates (e.g., 10 to 50 top hits, supplemented with random edge cases for model calibration)"。**代价**：随机边缘样本之外，大量设计从未被实验触碰，任何"命中率"都只在这个被截断的末端池上算，天然高估或口径漂移。
2. **即便过完全部计算筛，假阳率仍高**。原文（L260）："Even with these stringent in silico filters, designers should expect substantial false-positive rates"，随后给出区间（见第 4 节）。**应对**：明说计算分只"富集"不"保证"（L260）："computational scores enrich for success rather than guarantee it"；加正交立体化学检查（PoseBusters 类）与 MD 兜底。**代价**：没有给出"该把阈值定多严才能让末端命中率≥X"的定量映射，阈值（pLDDT>85 / ipTM>0.8 等）是按文献惯例给的，不是本文标定。
3. **静态建模对柔性/诱导拟合靶会给出"高置信却机理错"的构象**。原文（L324）："static modeling can yield high-confidence yet mechanistically incorrect poses"；且（L323）："Current generation and complex-prediction pipelines are still largely built around single-structure snapshots"。**应对**：建议对小子集叠加靶向 MD / 加速采样、把动态稳定性代理嵌入漏斗（L326）。**本文未解决**：作者把这列为"future direction"，综述本身没给柔性靶的实测命中率。
4. **训练数据偏差 + 各实验室口径不一致，让报告的"成功"不可比**。原文（L339）："Differences in targets, constraints, thresholds, and experimental conditions across laboratories can make reported successes appear incomparable"；数据侧（L235）："their absolute calibration is limited by training data biases, label noise, and distribution shift"。**应对**：给出 benchmarking playbook（L127）要求统一报告口径（见第 4 节）。**代价**：这是**倡议**，不是已落地的标准；文中转述的 1%–10% / 1%–2% 本身仍是不同分母混在一起得到的区间。

## 3. 方法与工作流程（综述归纳的标准化栈）

### 用了哪些方法（工具箱，均为综述转述的代表性工具）

- **骨架/界面生成**：RFdiffusion（含 All-Atom / RFdiffusion3）、Chroma、FrameDiff（motif scaffolding / inpainting）；网络 hallucination 与联合 co-folding 两条并行范式。
- **序列设计与回环**：ProteinMPNN、LigandMPNN、PiFold、SaProt、ESM-IF（逆折叠与结构感知语言模型）；侧链堆积与 constrained relax 用 Rosetta。
- **结构预测/置信度闸口**：AF2 / AF3 / ESMFold / Boltz-2（Boltz-2 内建亲和力预测打分）；BindCraft 把"生成 + 基于可微置信信号的筛选"自动化成 one-shot 管线。
- **物理与特异性侧**：Rosetta 界面能量、ScanNet / DeepRank-GNN 界面打分、negative design 与 cross-docking 抗脱靶、末端可选 MD 稳定性检查。
- **湿实验反馈**：phage / yeast display 高通量富集 + 深测序、DMS（深度突变扫描）、SPR / BLI / ITC 定量动力学、X-ray / cryo-EM / NMR 机理确证。
- **本综述不含**：本文不做一手 MD/QM 计算（MD 仅作为"末端可选稳定性检查 / 诱导拟合策略"被转述提及）。

### 标准化四段工作流（作者归纳；每步：输入 → 操作 → 判据/阈值 → 输出规模）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 几何生成 | 靶表位 / 结构约束 | 扩散模型（RFdiffusion 等）在表位周围生成几何互补骨架，多随机种子采样 + 聚类保多样性 | 综述未给统一生成阈值 | "thousands to tens of thousands of candidate binders"（进入下游的候选量级，L231） |
| 2 序列设计 | 固定骨架（+ 表位/配体几何约束） | 逆折叠（ProteinMPNN / ESM-IF）为骨架配序列，产多样板而非单条最优；物理/全原子回环去冲突 | 综述未给序列层阈值；"the practical success rate is often determined by whether that backbone can be turned into a real molecule"（可表达/可纯/稳定/保留界面化学，L190） | 每骨架多条序列候选，汇入自洽性检验 |
| 3 结构自洽筛选 | 序列候选 | 结构预测器（AF2/ESMFold 等）反折回结构、对齐回设计做 self-consistency + consensus/ensemble 过滤 | 置信度阈（L257）："demanding monomer pLDDT > 85, interface PAE < 5 Å, and ipTM > 0.8" | 削到可下单集合，仍达 10³–10⁴ |
| 4 排序 + 闭环实验 | 通过筛选的设计 | 物理指标（Rosetta 界面能）+ negative design 精排，选高分子集 + 随机边缘样本送高精度正交验证 | 建议子集规模（L298）："10 to 50 top hits, supplemented with random edge cases" | 湿实验只测得起 "only tens to hundreds"（L231） |

**命中率层（本文档最关键）**：四段走完后的实验命中率，综述给两处口径不同的数字——(a) 全局经验区间（L260）："typical experimental hit rates for de novo binders currently range from 1% to 10%, occasionally reaching up to 20% for highly favorable targets"；(b) 表位聚焦 miniprotein 案例（L304）："initial computational screens for these targets yielded experimental hit rates of roughly 1% to 2% from tens of thousands of candidates"，再经酵母展示成熟到 "often reaching K D values of 1 to 100 pM"。**两处 1% 的分母不同**（详见第 8 节）。

## 4. 关键数字台账（数值 · 含义 · 出处）

| 数值 | 含义 | 出处（原句片段，L=第 9 节底稿内句序） |
|---|---|---|
| 1% – 10%（偶达 20%） | de novo 结合蛋白"典型实验命中率"经验区间 | L260 "typical experimental hit rates for de novo binders currently range from 1% to 10%, occasionally reaching up to 20%" |
| 1% – 2% | 表位聚焦 miniprotein 靶的初始命中率（案例转述） | L304 "roughly 1% to 2% from tens of thousands of candidates" |
| thousands – tens of thousands | 进入实验前的计算候选量级 | L231 "thousands to tens of thousands of candidate binders" |
| tens – hundreds | 湿实验实际能验证的量级（末端分母） | L231 "validation of only tens to hundreds" |
| 10 to 50 top hits（+ 随机边缘样本） | 建议送去高精度正交验证（SPR/BLI/ITC）的子集 | L298 |
| monomer pLDDT > 85；interface PAE < 5 Å；ipTM > 0.8 | 结构自洽筛选置信度阈 | L257 |
| 1 to 100 pM | 成熟后的亲和力 K_D 区间（案例） | L304 |
| ≈30% | 训练/测试边界处建议的序列同一性上限（防泄漏） | L125 "capping sequence identity below approximately 30%" |
| 10^9 – 10^11 variants | 传统展示库规模（对照 AI 栈要绕过的瓶颈） | L25 |
| 100 pM | 命中率与 pM 亲和力绑定在同一句话（勿据此把命中率当亲和力概率） | L304 |

## 5. 结论——作者说了什么

1. AI 从头设计已收敛成"几何生成 → 序列设计 → 结构筛选 → 实验闭环"的标准栈。
2. **计算分只富集、不保证**成功；过完全部 in silico 筛后，典型实验命中率仍只有 **1%–10%（个别靶到 20%）**。
3. 全流程真正的瓶颈是**漏斗末端**：计算能出 10³–10⁴ 条、实验只测得起 10¹–10² 条。
4. 柔性/诱导拟合靶、数据偏差、跨实验室口径不一是当前主要局限。
5. 因此作者呼吁统一 benchmarking：报告"数据集大小、计算筛选阈值、置信度指标、实验验证计数、估计假阳率"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的价值不在"给了一个命中率"，而在"暴露了命中率口径混乱"**。它自己在同一段落里就用两种分母报 1%（末端实测池 vs 几万候选池），正说明"de novo 命中率 1%–10%"这类数字脱离分母就没有可比性。
2. "1%–10%"是**跨文献归纳区间**，不是某一次实验的结果；引用它等于引用一个元统计（meta-statement），不能当作"我们这条管线预计命中率"的校准。
3. playbook（L127）要求的报告项，恰好是我们项目缺的字段：分母（生成/实测各多少）、阈值、置信度指标、假阳估计——这套口径可以直接搬到我们 UAA 漏斗的产出登记里。
4. 末端"tens–hundreds"与信息量最大的"10–50 top hits + 随机边缘样本"这一设计，对应我们"末端不是样本数最大化、而是信息量最大化"的既有判断。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：静态单构象建模对柔性靶给出高置信错构象；数据分布偏差 + 标签噪声限制绝对标定；缺统一 ImageNet 式基准。
- 我们读出：① 综述不产一手数据，所有命中率都是转述，无法核对每篇的分母/阈值细节；② "1%–2% 从 tens of thousands candidates"与"1%–10% 典型"是两套口径，若不加标注并列引用会自相矛盾；③ pLDDT>85 / ipTM>0.8 是给 binder 结合用的阈值，与催化活性无关；④ 文中 K_D 1–100 pM 是**成熟后**（酵母展示优化后）的值，不是初始设计命中率对应的亲和力。

## 8. 对 UAA 筛选的迁移判断：**引用这些命中率时必须怎么标注分母口径**

**核心教训**：同一句"命中率 1%"在这篇里有两种分母。我们以后凡是转引本综述（或任何文献）的命中率，必须**在数字旁边显式写出三层口径**，缺一层就视为不可引用：

1. **写清是哪一端的分母**——本卡两处示范：
   - L260 的 "1% to 10%" 分母 = **通过全部 in silico 筛之后、实际送去实验的末端池**（tens–hundreds 量级），**不是**生成总量。引用时标注："末端实测分母（post-filter tested pool）"。
   - L304 的 "1% to 2%" 分母 = **"tens of thousands of candidates"**（近全池 / 大规模合成测试），与上者不同量级、不同口径。引用时标注："全池/大规模合成测试分母"。
   - **禁止**把 1%–10% 与 1%–2% 并排当作同一指标的两个精度；它们是两种分母下的两种读数。
2. **写清分子是什么事件**——这里分子 = "实验测到结合（binding hit）"，二值结合/不结合，**不是催化成功**。UAA 的分子必须是"产物化学确认的活性"，二者不可互换。
3. **写清这是转述归纳值、非一手实测**——本卡命中标注为"综述归纳区间（review-level meta-statistic）"，并保留出处句序（L260 / L304）以便回溯。

**可迁移（怎么做）**
- 把 playbook 的 5 项报告口径（数据集大小 / 计算筛选阈值 / 置信度指标 / 实验验证计数 / 估计假阳率）作为我们 UAA 漏斗**每张命中率表的强制列**：任何命中率都要带"生成数→过滤数→实测数→命中数"四个分母。
- 借"末端只测 tens–hundreds、优先 10–50 top hits + 随机边缘样本"的组织方式：我们末端实验容量更小，更要把随机边缘样本（阴性对照）纳入，才能算真 ROC，而不是只测高分。

**不可迁移（为什么不能照搬）**
1. **1%–10% / 1%–2% 是 binder 结合命中率，绝不能当 UAA 酶活命中率先验或校准**。DP2R 标准明禁把 binder 的 pAE/ipTM/pLDDT 阈值当催化闸口；命中率数字同理不可跨域搬运。
2. **pLDDT>85 / interface PAE<5 Å / ipTM>0.8 是"会不会按设计结合"的阈值**，结构自洽对"会不会催化三步化学事件"既不必要也不充分；不得写进我们的漏斗判据。
3. **K_D 1–100 pM 是展示成熟后的亲和力**，不能反推"某法对 UAA 能到 pM"。本卡严禁编造"某法对 UAA 成功率 X%"。
4. 这篇不含一手 MD/QM，**不能为"用 MD/QM 判催化"提供命中率背书**。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K39_PMC13113996_text.txt

- 本地纯文本：`fulltext/K39_PMC13113996_text.txt`（Europe PMC/NCBI fullTextXML 去标签、HTML 实体已解码、空白折叠；未改写内容）。
- 句序锚点（L#）指底稿按句号切分后的第 # 句，便于回溯；引句均为逐字复制。
- CSV 字段映射：第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/实验命中率/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only K39 --no-report` 把卡内所有不含中日韩字符、被直双引号包住、≥20 字符且≥12 字母的片段，在该底稿里做逐字查找；全部命中才 PASS。

<!--CSV回填
work_type=论文（综述 review，非一手实验）
target=蛋白-蛋白界面 / 非抗体支架（DARPin、affibody、monobody、miniprotein）；难靶举 GPCR、离子通道、柔性信号蛋白；案例含 SARS-CoV-2 RBD、整合素 αvβ6 vs αvβ8
backbone_generation=RFdiffusion（All-Atom/RFdiffusion3）/Chroma/FrameDiff 扩散生成骨架 + 网络 hallucination / 联合 co-folding；序列走 ProteinMPNN/LigandMPNN/PiFold/SaProt/ESM-IF 逆折叠，Rosetta 侧链堆积与 constrained relax；BindCraft 做 one-shot 生成+可微置信筛选
computational_filters=AF2/AF3/ESMFold/Boltz-2 结构自洽与 ensemble 过滤（反折回设计比对 Cα/pLDDT/PAE/ipTM）；Rosetta 界面能与 ScanNet/DeepRank-GNN 界面打分；negative design 与 cross-docking 抗脱靶；末端可选 MD 稳定性检查；PoseBusters 类立体化学检查
thresholds=monomer pLDDT>85；interface PAE<5 Å；ipTM>0.8；训练/测试序列同一性上限≈30%（综述转述，非本文标定）
md_used=是（综述层面：作为诱导拟合/柔性靶的末端可选稳定性校验策略被转述提及，本文未自做 MD 实验）
qm_used=否
experimental_methods=phage/yeast display 高通量富集 + 深测序、DMS、SPR/BLI/ITC 定量动力学与 K_D、X-ray/cryo-EM/NMR 机理确证（均为综述转述别人的实验）
pipeline_counts=计算候选 thousands–tens of thousands（10^3–10^4）→ 湿实验只能验证 tens–hundreds（10^1–10^2）→ 建议高精度正交验证子集 10–50 top hits + 随机边缘样本；传统展示库对照规模 10^9–10^11 variants
hit_rate=综述归纳区间：典型实验命中率 1%–10%，个别有利靶达 20%（分母=过完 in silico 筛后的末端实测池）；表位聚焦 miniprotein 案例初始命中率约 1%–2%（分母=tens of thousands of candidates 近全池）——两种口径分母不同，引用必须标注
best_metric=成熟后亲和力 K_D 1–100 pM（经酵母展示优化，非初始设计命中对应值）
cost_or_stat_note=综述不产一手数据：所有命中率为跨文献归纳值；作者呼吁统一报告口径（数据集大小/筛选阈值/置信度指标/实验验证计数/估计假阳率），并承认各实验室口径不一致使"成功"不可比
role_in_timeline=把 RFdiffusion→ProteinMPNN→AF 置信度→BindCraft one-shot→DBTL 闭环整理成标准技术栈的方法学综述，同时给出 de novo binder 命中率经验区间与 benchmarking playbook，供口径对照（本卡用作"命中率分母口径"参考）
source_pointer=data/literature_cards/fulltext/K39_PMC13113996_text.txt（DOI 10.34133/csbj.0070, PMC13113996）+ sources/cost-benchmarks.md
CSV回填-->
