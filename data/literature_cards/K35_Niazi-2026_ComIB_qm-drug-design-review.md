# [K35] 量子力学在药物设计中的应用——综述：QM 分层、校准基准与失效边界

Niazi S. K.（University of Illinois Chicago, College of Pharmacy，单一作者）
Communicative & Integrative Biology 2026 · DOI 10.1080/19420889.2025.2603140 · PMC12721093 · PMID 41438190
开放获取（CC BY 4.0）· Received 2025 Sep 28; Accepted 2025 Dec 8 · Taylor & Francis

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K35**（组：通用方法学; 口径对照） |
| 本文取回方式 | PMC/Europe PMC `fullTextXML`（`data/literature_cards/batches.tsv` 第 73 行，fetch_status=OK） |
| 本地全文 | `data/literature_cards/fulltext/K35_PMC12721093_fullTextXML.xml`（原始）＋ `data/literature_cards/fulltext/K35_PMC12721093_text.txt`（去标签纯文本，61,124 B，**本卡唯一引句底稿**） |
| 对照底稿 | `sources/cost-benchmarks.md` 第 131 行（已把 Table 4/Table 6/Fig 1 关键数摘为对照行，并标注为“作者估算”） |
| 证据级别 | **全文级**（本卡全部引句可在登记底稿逐字命中，见第 9 节） |
| 本文性质 | **综述，无原创计算、无原创湿实验**；所有性能数字是对 156 篇原始文献＋42 篇综述的转述/表格化，本卡凡引用数字处均注明“综述口径” |
| 未取到的部分 | Figure 1/2 原图、各被引文献的原始数据与计算细节。Table 1/3/4/5/6 只能核验“综述里写了什么”，**不能**核验原研究本身 |

## 1. 这篇到底解决什么（一句话与大白话）

**一句话**：它不给新算法、不给新实验，只回答一个工程问题——**QM 在药物设计流水线的哪一步、对哪类体系才值得进，用什么级别算，精度拿哪些公开基准校准，以及作者自己划出的失效边界在哪里**。

大白话：经典力场（固定电荷）算结合自由能会系统性地漏掉极化、电荷转移、共价反应这三类电子效应，误差能到 2-3 kcal/mol；全量上 QM 又贵得算不动。这篇综述把 2020–2025 的证据整理成一个**分层应答体系**：小分子用 DFT（r2SCAN-D4）、酶活性位点/金属中心用 QM/MM（QM 区 100–300 原子）、大体系采样用机器学习力场（MLFF）、自由能量化用 QM 校正的 FEP；每一档的精度都挂在一个公开基准上（GMTKN55 校准泛函、S66×8/L7 校准色散校正、SAMPL6/SAMPL8 校准 pKa 与主客体结合、四类靶点的社区回顾研究校准 RBFE）。作者的总结心是“定向应用而非全面替换”："Quantum mechanical enhancements provide substantial benefits for specific challenging cases rather than universal improvements across all drug discovery applications."

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

> 说明：本文是综述，这里的“他们”= 作者综述并转述的各领域团队＋作者本人的处置。每条给：难点 → 现象/证据（尽量原句）→ **应对** → 应对后仍留下的代价。

1. **经典力场系统性漏掉电子效应，这是 QM 进场的第一动机**。现象："these methods systematically underestimate or neglect critical physical phenomena that often determine binding specificity and affinity with deviations exceeding 2-3 kcal/mol"。→ **应对**：不做全量替换，改为按“四类升级判据”定向进 QM（金属中心、电荷变化、共价键、极化主导；Fig 2 的四个菱形决策点），并给出分层工具箱（第 3 节 A 表）。→ 代价：作者明说收益只属于“specific challenging cases”，对普通体系 QM 无增益，升级判据本身**只有定性清单、无定量触发阈值**。
2. **QM 的规模/成本墙**。现象：DFT 是 O(N³) 标度，"While QM/MM methods can handle systems of up to 10,000 atoms, realistic membrane environments often require 100,000 atoms or more, pushing beyond practical limits."；纯 QM 上限 ~500 原子（Table 4）。→ **应对**：(a) 多层展开——ONIOM 类分层 "These strategies typically reduce computational costs by 10-50× compared to complete DFT calculations while maintaining chemical accuracy in the region of interest"；(b) QM 区取小但取全："For enzymatic reactions, this region typically includes the substrate, cofactors, and first-shell coordinating residues, often requiring 100-300 atoms for adequate chemical completeness."；(c) 嵌入方案分档（点电荷嵌入便宜 vs 极化嵌入贵）；(d) 基础设施（MiMiC 线性扩展上千核、"GPU-accelerated implementations achieve 2-5× performance improvements for typical protein-ligand systems using semiempirical QM methods."）；(e) MLFF 用经典成本换 ab initio 精度。→ 代价：作者把 scalability 列为三大未解限制之首（原句 "First, computational scalability remains problematic"），膜类体系被明示在能力边界外。
3. **QM/MM 边界是化学上不自然的切割**。现象：Table 1 对 QM/MM(DFT) 自认 "Complex boundary definitions; method-dependent accuracy"（典型精度 1.0-2.5 kcal/mol）。→ **应对**：给出边界规则——QM 区必须完整包住反应体系，"without artificial truncation of conjugated systems or hydrogen-bonding networks"，且 "Link atom approaches at QM/MM boundaries must preserve local chemistry while avoiding spurious interactions"；嵌入按精度需求选档："Point-charge embedding often offers adequate accuracy for many applications at substantially reduced cost, particularly when combined with appropriate boundary treatments"。→ 代价：规则是定性的，综述未给“边界误差多大、怎么验收”的量化协议。
4. **质子化/互变异构微观状态是隐形炸弹——宏观看对、微观全错**。现象（SAMPL6 盲测）："with over 40% of individual sites misassigned by more than 1 pKa unit"，而宏观 pKa 的 MUE 只有约 0.7 个单位。→ **应对**：microstate-aware 的 QM/MM FEP＋Boltzmann 加权。CDK2 案例：固定质子态的经典 RBFE 失败，"with calculated binding affinity differences exhibiting a poor correlation (R 2 = 0.3) with experimental IC 5 0 values"；纳入全部相关微观态后 "When all relevant microstates were included with proper Boltzmann weighting, calculated ΔΔG values improved substantially (R 2 = 0.8), with mean unsigned errors decreasing from 1.6 to 0.7 kcal/mol"；另用量子描述符＋可解释神经网络把位点 pKa 压到 <0.5 个单位（BCL:pKa 0.4–0.6）。→ 代价：微态枚举与权重本身仍靠人做，综述未给自动化判定流程。
5. **MLFF 在训练域外脆断**。现象："Machine-learned quantum potentials achieve impressive accuracy within training domains but often fail when applied to novel scaffolds."（作者列为第二大限制）；"Performance typically degrades significantly when applied to chemical motifs that are not represented in the training data."→ **应对**：混合方案——"Hybrid approaches that combine machine-learnt short-range interactions with classical long-range electrostatics offer a pragmatic solution for large biomolecular systems"；训练数据本身也分层报价（ANI-2x 用 9.6M DFT 计算，NequIP 只要 1–10K、sGDML 100–1K 构型）。→ 代价：作者原话 "though systematic validation remains ongoing"——**外推可靠性问题本文未解决**。
6. **不确定性与可复现性撑不起监管级判定**。现象：作者把 UQ 列为第三大限制："Third, uncertainty quantification remains inadequate for pharmaceutical decision-making."→ **应对**：Good Computational Practice（GCP）框架——多独立计算、系综不确定度、全参数文档（软件版本、泛函、基组、色散校正、收敛判据、质子化态），并引用多站点验证："Multi-site validation studies have shown that implementing GCP principles reduces irreproducibility rates from 40% to below 10%"；监管侧对接 FDA MIDD 与 EMA 资质路径，先例是 PBPK（"with over 200 FDA submissions incorporating PBPK modeling since 2008"）。→ 代价：该 40%→10% 的出处 [54] 是 EFPIA MID3 建模实践论文而非量子计算研究（见第 7 节），且作者承认针对量子方法的监管指南仍缺。
7. **量子计算叙事的现实落差**。现象："practical quantum computing applications in drug discovery remain largely aspirational"；NISQ 门错误率 "Current noisy intermediate-scale quantum devices exhibit error rates of 10 -3 to 10 -4 per gate operation, while quantum chemistry applications require error rates below 10 -6 for reliable results"（抽取文本原样）。→ **应对**：收缩到混合策略——近期只对 5–10 原子活性位点片段做强相关模拟；给出的资源底数是 100–200 个逻辑量子比特＋10⁻⁶ 错误率；时间表 "Expert assessments predict that fault-tolerant quantum computers capable of solving problems related to drug-sized molecules will be available at least 5-15 y in the future, with some estimates extending to 20 y or more."→ 代价：等于承认**当前**量子计算对本领域贡献近零；未来收益全部押注在经典侧量子化学的渐进改进（"Future progress will probably come from small changes to hybrid methods rather than big changes."）。

## 3. 方法与工作流程（QM 分层：哪些体系用什么级别、精度靠什么基准校准）

### A. 方法分层总表（综述 Table 1 / Table 4 转述；MUE=平均无符号误差）

| 层级 | 适用体系 | 系统规模上限 | 精度（综述口径 MUE） | 时间成本 | 该档精度的校准来源 |
|---|---|---|---|---|---|
| Classical Docking | 初筛 | 无上限 | 2.5-3.5 kcal/mol | 分钟级 | Table 4（综述自列，未挂单一基准） |
| MM/PBSA | 打分复核 | ~100,000 原子 | 1.5-2.5 kcal/mol | 小时级 | 同上 |
| Classical FEP | SAR 排序 | ~50,000 原子 | 0.9-1.5 kcal/mol | 天级 | 回顾大样本 "optimized relative binding free energy protocols achieve mean unsigned errors of 0.8-1.2 kcal/mol"；FEP+ 单点："RBFE accuracy of 0.9 kcal/mol with a mean unsigned error for well-converged calculations using the FEP+ protocol with the OPLS3e force field" |
| QM-corrected FEP | 电荷变化/难变换 | ~10,000 原子 | 0.5-1.0 kcal/mol | 天—周 | Table 4；带电微扰元分析 "Charge-changing perturbations benefit substantially from QM/MM treatment, with meta-analysis showing accuracy improvements of 0.5-1.0 kcal/mol when QM/MM corrections are applied" |
| QM/MM（DFT/HF） | 酶活性位点、金属中心、共价反应 | ~10,000 原子总、QM 区 100–300 原子 | 1.0-2.5（HF 基 2.0-3.5）kcal/mol | 天级（Table 4 列 0.8-1.8） | 酶反应能垒基准 [14]；蛋白-配质相互作用 [15]（综述脚注口径） |
| 纯 QM（DFT/HF） | ≤500 原子小分子、方法学验证 | ~500 原子 | DFT 0.5-2.0；HF 仅几何 | 小时—天 | GMTKN55："Systematic benchmarking against the GMTKN55 database reveals that r 2 SCAN-D4 achieves mean absolute deviations of below 2 kcal/mol for thermochemistry and sub-kcal/mol accuracy for noncovalent interactions"；色散：D4 在 S66×8/L7 上 MAE <0.3 kcal/mol |
| 半经验（PM6/PM7、GFN2-xTB、DFTB3） | 大通量初筛、MD 内嵌 | 数千—万原子 | PM6 生成热 4-6；xTB 构象能 3-5 kcal/mol、键长 0.1-0.2 Å；DFTB3 结合能 2-4 kcal/mol | 远低于 DFT | 各自参数化基准（综述转述） |
| FMO（DFT/HF） | 蛋白-蛋白界面逐残基分解 | 数千原子 | 1.5-3.0（HF 基 2.5-4.0）kcal/mol | 天级 | 综述 Table 1 脚注 [15] |
| MLFF（ANI-2x/NequIP/MACE/sGDML） | 构象采样、MD 加速 | 视架构 | ANI-2x 构象能 <1 kcal/mol | 较 ab initio 快 10⁴–10⁶× | 各自训练/测试集（综述 Table 5） |

双杂化泛函（revDSD-PBEP86-D4、ωPr2SCAN50-D4）为高精度档：金属蛋白活性位点与有机金属骨架的能垒误差 "with barrier height errors typically below 1 kcal/mol"。

### B. 精度靠什么校准（综述点名的基准体系）

- **泛函级**：GMTKN55（热化学/非共价）、S66×8 与 L7（色散校正 D4）；
- **盲测级**：SAMPL6 pKa 挑战（宏/微观质子化态）、SAMPL8 主客体（极化效应，AMOEBA 对 cucurbituril 体系 ABFE "with mean unsigned errors approaching 1.0 kcal/mol"）；
- **产业回顾级**：Table 3 四类靶点——激酶 219 个变换（经典 0.9±0.1，QM 增强金属位 0.5±0.1）、GPCR 156（1.1±0.2→0.9±0.2）、蛋白酶 89（0.8±0.1，共价 0.2±0.1）、离子通道 67（1.2±0.2→0.9±0.2）；QM 增强收益 +0.2 到 +0.6 kcal/mol，共价键类最大（+0.6）；
- **组合验收线**：Fig 1 的最优性能区 "The grey-shaded region indicates the optimal performance zone (<1.0 kcal/mol error, <1,000 GPU hours)."

### C. 工作流程（Fig 2 四阶段＋菱形升级判据；每步：输入 → 操作 → 判据/阈值 → 输出）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | 靶点与结合位点结构 | 体系分诊：判断命中哪类“经典力场系统性失效”场景（Fig 2 四个菱形决策点：金属中心、电荷变化、共价键、极化效应）；质子化态/微态枚举 | 定性判据清单，**原文未给分诊阈值**（无“误差超过 X 才升级”的定量线） | 走经典分支或量子分支；微态集合 |
| W2 | 分诊结果 | 按 A 表选层级：小分子→r2SCAN-D4；酶/金属→QM/MM（QM 区 100–300 原子）；界面分解→FMO；采样→MLFF | 目标精度线 <1.0 kcal/mol；成本线 <1,000 GPU-hours（Fig 1 最优区） | 计算方法与软件选型（CP2K-GROMACS/MiMiC/ORCA/ChemShell，Table 2） |
| W3 | QM/MM 体系草案 | 边界与嵌入设置：QM 区完整包含底物/辅因子/第一壳层配位残基，link atom 保化学、避免伪相互作用；点电荷嵌入（便宜）vs 极化嵌入（贵但准） | 化学完备性规则（定性）；原文未给边界验收阈值 | 可运行的 QM/MM 模型；GPU 加速 2-5× |
| W4 | 就绪的自由能任务 | FEP/TIG3/REST2/OneOPES-ABFE、自适应 λ 调度、收敛检测；电荷变化用 separated topology RBFE | 收敛判据由协议自动调度；增强采样 "improving convergence rates by 2-3× compared to standard protocols" | ΔG/ΔΔG 数值＋不确定度；量级示例 4200 GPU-hours（QM 增强 RBFE，A100） |
| W5 | 计算结果 | GCP 验收：多独立计算、系综不确定度、全参数文档（软件版本/泛函/基组/色散校正/收敛判据/质子化态）；对照 B 节基准定位 | 不可复现率控制线：实施 GCP 后 "reduces irreproducibility rates from 40% to below 10%" | 可进决策（及监管）的报告；未过验收 = 不许用 |

**分层逻辑一句话**：先用 W1 的定性判据把体系分流，再用 W2 的双阈值（精度 <1.0 kcal/mol × 成本 <1,000 GPU-hours）选层级，最后用 B 节的外部基准而不是内部自洽来校准——校准对象始终是“方法在该类化学事件上的历史误差”，不是单次计算结果。

## 4. 关键数字台账（全部为综述转述口径；数值可在底稿中搜到，第 9 节逐字命中）

| 数值 | 含义 | 出处（章节/原句片段） |
|---|---|---|
| 156 篇原始研究 + 42 篇综述；检索 PubMed/WoS/arXiv，2020-01 至 2025-01 | 综述语料与检索窗 | 摘要 "We critically evaluate 156 primary research articles and 42 review papers" |
| 2-3 kcal/mol | 经典力场系统性偏差的量级 | §1 Introduction |
| 0.8-1.2 kcal/mol | 优化后 RBFE 协议社区回顾 MUE | §1、§4.1 两处 |
| <1.0 kcal/mol × <1,000 GPU-hours | Fig 1 最优性能区双阈值 | 图注 |
| ~500 原子 / 0.5-2.0 kcal/mol | 纯 DFT 体系上限与精度（GMTKN55 脚注） | Table 1、Table 4 |
| ~100 原子；仅几何 | HF 上限（无电子相关，不给能量精度） | Table 1 |
| ~10,000 原子总、QM 区 ~200 原子 / 1.0-2.5 kcal/mol | QM/MM(DFT) 规模与精度；HF 基 2.0-3.5 | Table 1 |
| 100-300 原子 | 酶反应 QM 区推荐规模 | §3.1 |
| 10-50× | ONIOM 分层相对全 DFT 的省费倍率 | §2.2 末 |
| <2 kcal/mol（热化学）/ sub-kcal（非共价）| r2SCAN-D4 对 GMTKN55 | §2.1 |
| <0.3 kcal/mol | D4 色散校正对 S66×8/L7 | §2.1 |
| <1 kcal/mol | 双杂化泛函能垒误差（金属位） | §2.1 |
| 4-6 / 3-5 kcal/mol；0.1-0.2 Å；2-4 kcal/mol | PM6 生成热 / GFN2-xTB 构象能·键长 / DFTB3 结合能 | §2.2 |
| 1.5-3.0 / 2.5-4.0 kcal/mol | FMO-DFT / FMO-HF 精度 | Table 1 |
| 2-5× | 半经验 QM 的 GPU 加速倍率 | §3.1 |
| 2-3 kcal/mol | 激酶 Mg²⁺/Mn²⁺ 金属配位几何对亲和力的影响 | §3.2 |
| 12-18 kcal/mol | SARS-CoV-2 Mpro 共价键形成活化能垒（QM/MM，两处一致） | §3.2、§9.2 |
| 2-4 个单位 | 蛋白环境相对溶液的 pKa 偏移 | §3.2 |
| Docking 2.5-3.5（分钟）→ MM/PBSA 1.5-2.5（小时, ~100,000 原子）→ 经典 FEP 0.9-1.5（天, ~50,000 原子）→ QM 校正 FEP 0.5-1.0（天—周, ~10,000 原子）→ QM/MM 0.8-1.8（天）→ 纯 QM 0.5-1.5（小时—天, ~500 原子）→ FMO 1.0-2.0（天） | Table 4 全档：精度-规模-成本三联 | §4.1 Table 4 |
| 激酶 219 / GPCR 156 / 蛋白酶 89 / 离子通道 67 个变换；QM 增强收益 +0.4 / +0.2 / +0.6 / +0.3 kcal/mol；蛋白酶共价档 MUE 0.2±0.1 | Table 3 社区基准四行 | §4.1 |
| 0.9 kcal/mol；FEP+ 协议、OPLS3e 力场 | 工业大样本单点基准（Schindler） | §4.1 |
| 1.0-1.5 kcal/mol | ABFE 对实验的当前精度 | §4.1 |
| 2-3× | OneOPES-ABFE 收敛率提升 | §4.2 |
| 9.6M DFT 训练 / <1 kcal/mol / 加速 >10⁶×；NequIP 1-10K、MACE 2-10K、sGDML 100-1K 构型 | MLFF 训练量-精度-速度 | §5.1、Table 5 |
| ~0.7 pKa 单位（宏观 MUE）；>40% 位点错派 >1 单位 | SAMPL6 盲测 | §6.1 |
| <0.5；0.4-0.6 pKa 单位 | 量子描述符 NN / BCL:pKa 微观 pKa | §6.2 |
| R² 0.3→0.8；MUE 1.6→0.7 kcal/mol | CDK2 微态感知前后对比 | §6.3、§9.3 |
| 70-80% | WaterMap 识别可置换高能动水的准确率 | §7.1 |
| ~1.0 kcal/mol | AMOEBA 对 SAMPL8 cucurbituril ABFE | §9.1 |
| 4200 GPU-hours → 1512 kWh → 605 kg CO₂eq（可再生 76 / 煤电 1210）；美国电网 0.4 kg/kWh | 一次 QM 增强 RBFE 的碳核算示例 | §8.1 |
| 经典 RBFE 500 GPU-h/72 kg；QM 校正 2000/288；QM/MM ABFE 5000/720；MLFF 训练 10000/1440（美国电网 CO₂ kg） | Table 6 四行 | §8.1 |
| 20-50% | 编译/优化实现相对朴素实现的省算力 | §8.2 |
| 40% → <10% | 实施 GCP 后不可复现率 | §10.2 |
| 10⁻³–10⁻⁴ vs <10⁻⁶ 每门错误率；100-200 逻辑量子比特；5-10 原子片段；5-15 年（保守到 20+ 年） | NISQ 现状 vs 化学需求 | §11.1、§11.2 |
| $100-300 million | 每避免一次后期失败的节省（作者估算，无出处挂账） | §16.1 |
| 89% | nirmatrelvir 临床住院风险降低 | §9.2 |
| 2-3 年 / 5-7 年 / 7-10 年 | 三阶段渗透路线图 | §16.4 |
| 500+ 蛋白-配体体系；0.4-0.6 kcal/mol | Highlights 口径的基准覆盖与共价/金属/电荷类的增益 | Article highlights |

## 5. 结论——作者说了什么

1. QM 已从特例研究工具变成计算药物发现的实用组件，但 **"The most significant impact lies in targeted application to challenging problems where classical methods systematically fail."** ——价值在定向使用，不在全面替换。
2. 投资回报最高的是三类体系：含金属、共价修饰、极化主导（摘要原句 "targeted applications to metal-containing systems, covalent modifications, and polarization-dominated interactions yield the highest return on computational investment"）。
3. 精度已跨过可用线：RBFE 0.8–1.2、QM 校正档 0.5–1.0 kcal/mol；最优区双阈值 <1.0 kcal/mol × <1,000 GPU-hours；QM/MM  corrections 在难点变换上再提高 0.4–0.6 kcal/mol（Highlights）。
4. 三大技术限制被作者明列：规模（O(N³)、膜体系出界）、MLFF 训练域外脆断、不确定量化的缺失（第 2 节 2/5/6 条）。
5. 路线图：近期 2–3 年量子方法成为金属位点/共价抑制剂/电荷变化变换的标准做法；5–7 年 MLFF 成熟替代经典力场；7–10 年自动量子增强流程成为先导优化标配；真容错量子机至少 5–15 年。
6. 整合的形态要求："Successful integration requires treating quantum methods as engineering tools with appropriate validation protocols, uncertainty quantification, and cost-effectiveness analysis."
7. 失效边界（作者明写）："extending method applicability beyond well-validated chemical space" 仍是关键挑战；量子计算近期 "largely aspirational"；未来进展 "Future progress will probably come from small changes to hybrid methods rather than big changes."

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. 这篇的真正产物是**资格清单＋校准台账**，不是性能证明。它把 QM 进不进判定链的问题从“准不准”改写成“**化学事件是否命中金属/共价/电荷变化/极化四类经典力场系统性失效场景**”——命中才谈升级，未命中升级就是烧 GPU。我们的目标反应簇（亲核取代/磷酰转移/共价中间体）**命中其中两格**，这给“QM/MM 有理由被考虑”提供了方法选型依据；但它**不提供**任何“考虑了就能判对”的概率。
2. 校准链条的参照系对我们不存在：GMTKN55/SAMPL 之所以能用，是因为基准集上有**阴阳性同域的实测真值**。我们至今没有一条被产物化学确认的天然参照酶（B09 卡同结论），所以我们的 QM/MM 数值暂时只能校准到“几何/电荷合理性＋竞争假设间排序”，校准不到“判定精度”。
3. 双阈值（<1.0 kcal/mol × <1,000 GPU-hours）是**综述自设的验收线**，Fig 1 是示意图不是散点实测。它对我们的意义是给“判定权分级”提供了可借用的形状：未达任一阈的方法只配证据权，达双阈且**有独立真值集**才配判定权——第三格（独立真值集）是这篇替我们暴露出来、但它自己没强调的必备条件。
4. SAMPL6 的 40% 微观态错派是一记前置警告：**质子化/互变异构态没钉死之前，任何 QM/MM 能垒数值都是未定义问题的答案**。我们体系里催化残基微态若只能猜，QM/MM 的正确出场方式是“微态敏感性扫描＋区间报告”，不是单值。
5. 作者的三阶段路线图（2–3 年金属/共价/电荷标准用 → 5–7 年 MLFF 换力场 → 7–10 年全自动）暗示：本文级别的综述也在等工程化。对项目的含义是把 QM/MM 当**低频、高单价、需要人工设置与验收的判据**来排预算（示例单价：一次 QM 增强 RBFE 4200 GPU-hours），别按“流水线默认件”规划。

## 7. 局限与失败（作者的 + 我们读出的）

**作者明写的失效边界**
- 适用性不越“已验证化学空间”："extending method applicability beyond well-validated chemical space" 列为关键挑战（§15）；
- 规模：QM/MM ~10,000 原子，膜环境 100,000+ 原子出界；纯 QM ~500 原子；
- MLFF 训练域外脆断，"systematic validation remains ongoing"；
- 不确定量化的缺失本身被列为制药决策的未解限制（第 2 节 6 条）；
- 量子计算近期无贡献（largely aspirational），5–15+ 年；
- 作者承认产业落地障碍不是技术而是监管标准化缺失与专才稀缺（§16.1）。

**我们读出的（本卡必须留档的可疑处）**
1. **单一作者综述、无原创计算**：全部表格数字是转述/估算，可核验上限只到“这篇综述写了这个数”，不到“这个数被谁在什么条件下测出”。`sources/cost-benchmarks.md:131` 摘取时同样标注为“作者估算”。
2. **疑似引用错位三处**（按文末参考文献表核对）：CDK2 微态案例的定量前后对比（R² 0.3→0.8、MUE 1.6→0.7）挂到 [47]，而 [47] 是 2008 年 factor Xa 活性位点水的论文；BCL:pKa 的 0.4–0.6 pKa 单位挂到 [46]（一篇泛论计算药物发现的综述）；GCP 的 40%→<10% 不可复现率挂到 [54]（EFPIA MID3 实践文件，非量子方法可复现性研究）。**这三条恰好是全篇“QM 带来跃升”最依赖的量化论据。**
3. **nirmatrelvir 案例是回溯叙事**：QM/MM 能垒（12–18 kcal/mol）与临床 89% 并置，暗示因果；实际是“设计成功之后用 QM/MM 解释”，综述把它写成 validating the computational design strategy——单案例、非对照。
4. 检索窗写 January 2020-January 2025 但正文称覆盖 2020 to 2025，纳入/排除标准除库名外未给，156/42 的计数不可复现。
5. 利益声明：作者自述为 FDA/EMA/MHRA 顾问（Disclosure statement），与 §14 监管乐观叙事同源，需在引用其监管结论时降一档置信。

## 8. 对我们项目 QM/MM 进判定链的迁移判断

**可迁移（怎么用）——“我们的 QM/MM 该在什么条件下才有资格进判定链”**

1. **资格判据一：化学事件命中性**。只有当被判定问题属于共价键形成/断裂、电荷变化、金属中心或极化主导时，QM/MM 才有入场理由（Fig 2 四菱形）。我们 S1/S2 的磷酰转移与共价中间体属于“共价＋电荷变化”双命中，这是引用本文能支持的**唯一强度的结论**：方法选型合理。
2. **资格判据二：先校准、后判定**。本文每一档精度都挂在外部真值基准（GMTKN55/SAMPL/产业回顾集）上。对应动作：我们的 QM/MM 判据必须先在一套**独立几何/能量参照**上验收（已审计的 271 原子簇、参考酶晶体几何等），在拿出不优于参照物的误差报告之前，只许给证据权/排序权，不给否决权。
3. **资格判据三：规模与边界合规**。QM 区按 100–300 原子、共轭与氢键网不截断、link atom 规则设置；总体系超出 ~10,000 原子量级或需要膜环境时，直接承认本文口径下 QM/MM 不具备可行性（我们若走大复合物路线，QM/MM 就不是候选工具）。
4. **资格判据四：微态前置**。SAMPL6 结果要求：催化残基质子化/互变状态先用 pKa 手段约束或显式扫描，QM/MM 报告带微态权重或带敏感性区间——单值能垒在微态未定时不进判定链。
5. **成本口径**：判定链排预算用本文示例量级（QM 校正/增强档：天级、千 GPU-hours 级，4200 GPU-hours 一例），结合我们实测单价（xTB 271 原子 153.3 s/评价）报“每个进判定链的候选花多少核时”。
6. **验收文档模板**（GCP 可借用）：软件版本、泛函/基组/色散校正、收敛判据、体系制备（质子化态）、不确定度（系综）——缺任一项的结果按本文标准不可复现，不进链。

**不可迁移（为什么不能照搬）**

1. **不许把本文任何 MUE/增益数字当我们的期望误差或成功概率**：0.8–1.2、0.5–1.0、+0.4–0.6 kcal/mol 全部来自别人体系、别人数据集的综述转述，其中三条关键量化还疑似引用错位（第 7 节）。“QM/MM corrections improving binding affinity predictions by 0.4-0.6 kcal/mol in these challenging cases”是别人化学空间的读数。
2. **nirmatrelvir/SARS-CoV-2 Mpro 案例不能迁移为“QM/MM 能提高设计成功率”**：那是单例回溯叙事，没有对照；我们的目标连正向标签都没有，无法构成同类论证。
3. **RBFE/FEP 精度阶梯不覆盖酶催化转化**：本文的“clinically relevant accuracy”线是给结合亲和力定的，不是给反应能垒定的；酶能垒档 QM/MM 的综述口径只有 Table 1 的 [14] 脚注一类，且 Table 1 自认 method-dependent accuracy。**不许**用结合自由能的 <1.0 kcal/mol 线来宣称我们 QM/MM 能垒判定“达标”。
4. **监管章节（FDA MIDD/EMA）不构成我们产物的合规范式**：那是针对 PK/PD 模型的路径（且 PBPK 先例是 2008 年起的统计），与酶功能判定无关。
5. **MLFF 替代力场的路线图不许写进我们的本轮计划**：作者自己承认外推脆、验证 ongoing；我们无训练数据域，直接排除。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K35_PMC12721093_text.txt

- 本地纯文本：`data/literature_cards/fulltext/K35_PMC12721093_text.txt`（由 `K35_PMC12721093_fullTextXML.xml` 经 `scripts/litcards_text.py` 同一 norm 管道去标签生成；61,124 B，单行）。本卡全部直双号引句均从**这一份**复制；同一论文只有这一种抽取版本入库，无 Europe PMC/NCBI 双版本歧义。
- 对照底稿：`sources/cost-benchmarks.md:131`（Table 4/6 与最优区数字的先行摘录，标“作者估算”；本卡数字与其互洽，出处均另指全文）。
- CSV 字段映射：第 3 节 ↔ `计算筛选判据/阈值数字`；第 4 节 ↔ `成本/统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only "K35" --no-report` 逐字比对全部引句于登记底稿；引句在写卡前先经同一 `norm()` 管道逐条预核验，结果见交付回报。第 4 节数字全部可在底稿文本中检索到（含抽取噪声形态如 r 2 SCAN、10 -3、IC 5 0，原样保留）。
- 引用错位三处（第 7 节）系按文末参考文献表 [46][47][54] 条目与正文主张交叉比对得出，属卡内推断，不改动引句本身。

<!--CSV回填
work_type=综述（单一作者，无原创计算/湿实验；覆盖 156 篇原始研究＋42 篇综述，检索窗 2020-01—2025-01）
target=无自有靶点；综述对象为蛋白-配体体系（激酶/GPCR/蛋白酶/离子通道）、SARS-CoV-2 Mpro（共价）、CDK2（微态）、SAMPL 主客体
backbone_generation=不适用（方法选型综述：按化学事件在 DFT/半经验/QM/MM/FMO/MLFF/FEP 档位间分层）
computational_filters=Fig 2 四个升级决策点：金属中心、电荷变化、共价键、极化效应；GCP 验收（文档+系综不确定度）
thresholds=最优区 <1.0 kcal/mol × <1,000 GPU-hours；QM/MM 总体系 ~10,000 原子、QM 区 100-300 原子；纯 QM ~500 原子；RBFE MUE 0.8-1.2；ABFE 1.0-1.5；分诊本身原文未给定量阈值
md_used=是（综述口径：转述 QM/MM-MD、增强采样 OneOPES/REST2、WaterMap/GIST  hydration 等 MD 用途；非自有 MD）
qm_used=是（综述口径：全文即 DFT/QM/MM/半经验/FMO/MLFF/量子校正 FEP 的应用分层与校准基准；非自有计算）
experimental_methods=无原创实验；转引 SAMPL6/SAMPL8 盲测、NMR pKa 指认、nirmatrelvir 临床试验（89% 住院风险降低）
pipeline_counts=综述语料 156 原始＋42 综述；Table 3 基准 219/156/89/67 变换；Highlights 称 500+ 蛋白-配体体系社区基准
hit_rate=未记录（综述无自有命中率；仅档位化增益：QM 增强 +0.2 至 +0.6 kcal/mol，共价档最大）
best_metric=共价蛋白酶 QM 增强 RBFE MUE 0.2±0.1 kcal/mol（Table 3）；CDK2 微态感知后 MUE 0.7 kcal/mol/R²=0.8（综述转述，引用疑错位）
cost_or_stat_note=Table 4 阶梯：Docking 2.5-3.5 分钟级→经典 FEP 0.9-1.5 天级(~5×10⁴ 原子)→QM 校正 FEP 0.5-1.0 天—周(~10⁴)→纯 QM 0.5-1.5 小时—天(~500 原子)；示例 QM 增强 RBFE 4200 GPU-h→1512 kWh→605 kg CO2eq；ONIOM 省 10-50×；GPU 加速 2-5×；避免一次后期失败估省 $100-300M（作者估算）
role_in_timeline=口径对照位：给出“QM 何时才有资格进判定链”的资格清单（事件命中/外部基准校准/规模边界/微态前置/成本验收），并明写失效边界（非普适增益、膜体系出界、MLFF 域外脆断、UQ 不足、量子计算 5-15+ 年）；为我们的 QM/MM 判定权分级提供方法学依据而非概率背书
source_pointer=data/literature_cards/fulltext/K35_PMC12721093_text.txt（引句底稿）＋ K35_PMC12721093_fullTextXML.xml；sources/cost-benchmarks.md:131
CSV回填-->
