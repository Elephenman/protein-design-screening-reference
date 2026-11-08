# [B24] 把湿实验做成产线——SAPP/DMX：计算漏斗末端"送测与表征"的高通量、低价、标准化方案

Qian J, Milles L, Wicky B, Ragotte R, … Stewart L, Baker D（华盛顿大学 IPD 等）
Nature Communications 2026, 17:9945 · DOI 10.1038/s41467-026-76740-9 · PMID 42754580 · PMCID PMC13586242（CC BY 4.0）
预印本 10.1101/2025.08.05.668824

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B24**（组：Baker组; 通用方法学; 口径对照） |
| 本地全文 | `data/interim/baker_lit/ft/accelscaling2026.txt`（100,997 B，2026-10-16 抓取；batches.tsv 第 7 行，state=FULLTEXT） |
| 对照底稿 | `sources/baker.md` 第 316–327 行（原卡） |
| 登记底稿清单 | `sources_map.json` 键 B24：上述全文 + `sources/baker.md`（.xml 除外）；本卡全部英文引句在全文里逐字命中（门禁 `verify_literature_cards.py --only B24 --no-report`） |
| 证据级别 | **全文级**（引句均可在本地纯文本逐字命中） |
| 未取到的部分 | 补充信息（Supplementary Tables 1–9、Supplementary Figs、SI 里的成本明细计算）、Source Data、Fig 1–4 原始数据点。凡涉及这些处本卡明写"正文未给出" |

## 1. 这篇到底解决什么（大白话）

计算设计（RFdiffusion/ProteinMPNN 一夜生成几十万个候选）已经把湿实验环节甩在后面：一个设计要**克隆→表达→纯化→表征**，传统流程"几条到几十条就要几周"。这篇不提出新打分函数，而是把**下游实验本身重做成产线**：SAPP（半自动蛋白生产）从线性 DNA 片段出发，跳过挑克隆和测序验证，靠负筛选直接转化表达菌株，96 孔板全流程 + 自动 SEC + 自动色谱分析，一天几百个设计、端到端 48 小时、 bench 时间约 6 小时、单设计成本≈"几条 DNA 寡核苷酸"。再配 DMX（条形码解混）把便宜的 oligo pool 转成上千个**序列确证的阵列化克隆**，把基因合成成本再降 5–8 倍。用三个应用证明产线能用：ProteinMPNN 重设计荧光蛋白（一周表征 96 条）、RSV 结合体寡聚化筛选（IC50 打到 pM 级、和单抗 MPE8 同级）、文库→阵列克隆转换。开篇的定性判断："Recent advances in de novo protein design have greatly outpaced standard protein biochemistry workflows, making experimental validation a bottleneck"。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **验证环节是瓶颈，而且贵、慢、不可比**。"Typical workflows are time-, cost-, and labour-intensive, often requiring multiple weeks for testing a few dozen designs, and lack protocol standardization for consistent data collection"；而已有的大规模池式实验虽然通量高，"these assays are usually highly specialized towards measuring one or a few properties (e.g., stability, binding, enzymatic activity), require significant upfront protocol development, and rarely provide information on the manufacturability of individual sequences"。→ **应对**：做"assay-agnostic"的阵列式标准产线，所有设计输出同一组数据（产量/分散度/寡聚态），并写成开放格式数据框供后续机器学习用。**代价**：产线只覆盖"可溶、好表达"的蛋白，作者明写对复杂表达体系蛋白不适用（见第 7 节）。
2. **"必须挑克隆+测序"的教条被主动放弃**。作者指出该步骤 "adds multiple days and high costs to any protocol, and scales poorly, with colony isolation being a bottleneck"，于是用 ccdB 致死基因载体做背景压制（"that is excised and replaced by the design during GGA, ensuring background suppression and thus circumventing the need for colony isolation"），GGA 产物直接转化 BL21(DE3)。→ **应对之二（事后验证代替事前验证）**：回顾性 NGS 929 个反应："sequencing analysis of 929 GGA reactions with insert size below 314 bp showed that 89.3% had a clonal purity ≥ 90%"；再加质谱防"表达偏向"："Since protein expression can further bias polyclonal mixtures due to fitness effects resulting from variants, we performed mass spectrometry analysis of 863 purified proteins to analyze the extent of any possible contamination"，结果 "revealed the expected mass within ± 1 Da for 90% of all products (777/863)"。→ **遗留代价（作者自陈）**："While highly efficient, our protocol may still occasionally yield false negative results, and thus is primarily intended for screening purposes"；且 "the small levels of polyclonality resulting from synthesis error are length-dependent, which can complicate using the protocol for longer proteins"——多克隆纯度证据只统计了插入片段 <314 bp 的反应。
3. **摇瓶表达与化学诱导无法规模化**。96 深孔板 + 自诱导培养基替代振荡瓶/IPTG（"avoiding the need for any intervention between inoculation and harvest"），并记录了搅拌轨道半径对自诱导的影响（"smaller orbital paths appear to negatively impact expression, most likely due to reduced aeration"，Methods 表达段）。→ **应对**：全程板式化——"Keeping all steps in a plate format also eliminates container tracking overhead and reduces single-use plastic waste"。
4. **终点是 SDS-PAGE 胶，信息量太少**。他们判断凝胶不反映蛋白天然性质（寡聚态、分散度），"this two-step approach is also more time-consuming"（先胶筛再放大纯化的两步法）。→ **应对**：把表征与纯化合并——每个样品都直接上制备 SEC + 自动色谱分析（"Chromatograms are automatically analyzed, and the experimental profile for each design (yield, polydispersity, estimated molecular weight, see Supplementary Information) is output to a single open-format file"），并用廉价液体处理机器人自动收峰归一。→ **遗留代价**：瓶颈转移到仪器："the main bottleneck being SEC, with a capacity of ~300 samples per chromatographic instrument per day"。
5. **多聚体与展示技术天然不兼容**："the non-covalent nature of oligomers makes multimeric constructs inherently incompatible with"——想筛 58 种寡聚构型，YSD 做不了。→ **应对**：SAPP 阵列直测，用 SEC 洗脱体积是否在目标寡聚态 99% 置信区间内判"组装对不对"，再直接上功能实验（RSV 中和）。→ **遗留代价**：判据是尺寸而非形状——同分子量不同几何的组装体无法靠 SEC 区分；作者用功能数据（IC50）补这一课。
6. **SAPP 把瓶颈推给了 DNA 合成**："The highly optimized SAPP protocol has shifted the bottleneck of large-scale testing from protein expression/purification to the cost of DNA synthesis"。→ **应对**：DMX——oligo pool（便宜）→ 条形码解混 → 序列确证的阵列克隆，"The DMX pipeline is a 5-day protocol that leverages an isothermal DNA barcoding strategy and long-read sequencing"，"This approach is five and eight times more cost-effective (including reagent and sequencing costs) than ordering 500 and 2000 individual gene fragments, respectively"。→ **遗留代价**："only adding five days to the pipeline"，且回收率 78% 对理论上限 92%（"We successfully recovered 78% of the library variants as clonal, sequence-verified constructs by screening 4608 clones (3x the library complexity), approaching the theoretical maximum recovery rate of 92%"）；小库不划算——"while the polyclonal approach from SAPP is better suited for smaller campaigns (~100–200 designs) where faster turnaround time is desired"。
7. **DMX 内部的三个具体工程难点，各有对策**：(i) 双指数 PCR 条形码通量低——"This step is typically achieved by dual-indexed PCR, which limits throughput and requires large numbers of thermocyclers when processing thousands of samples"——改为恒温 GGA 连接条形码（"we developed an isothermal barcoding strategy based on GGA that ligates barcodes with the GOI directly in bacterial lysate"），组合编码 "Our approach uses four sets of position-specific barcodes comprising 24 unique molecular identifiers (UMIs) each, allowing for >330k wells to be tagged from a single 96-well plate of UMIs (24^4)"；(ii) 短读长测序限制基因长度——"We leverage nanopore long-read sequencing to overcome this limitation, making barcode mapping length-agnostic and enabling pools with longer genes to be demultiplexed"；(iii) pool PCR 扩增偏好——"To reduce biases, amplifications were monitored by real-time PCR using EvaGreen Dye (Biotium), and stopped before plateauing"。→ **代价**：回收率仍受合成错误/偏好制约（作者注明 92% 理论值是"reported by Twist"口径）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **构建与克隆**：定制 Python 反向翻译（DNA Chisel 做密码子优化：自定义 CAI、去重复序列、消 BsaI 位点、抑制起始密码子旁路；经 IDT SciTools Plus API 实时校验可合成性），>1500 bp（eBlock 上限）自动切成两段 one-pot GGA；载体带 ccdB 负筛选，25 个兼容表达载体（His/Strep/Avi/NanoBiT/Halo/MBP/FP 标签）存 Addgene。
- **表达纯化**：96 深孔板自诱导培养基；化学裂解 → 96 孔 Ni-NTA 亲和层析 → 自动进样 SEC（Superdex 75/200，5/150 柱）；OT-2/ECHO 机器人收样归一。
- **表征与分析**：Python 批量色谱分析（280 nm 峰检测、保留体积→分子量标定、浓度积分）→ HDF5 数据框；NGS（Illumina NextSeq2000）算克隆纯度；完整质谱（Agilent G6230B TOF）验质量；分子对接/实验细节另有 SP 荧光板读、SPR、cryo-EM、RSV 活病毒中和。
- **上游计算（RSV 案例）**：Rosetta RIF（rotameric interaction field）+ RifDock（21,400 脚手架库）+ FastDesign + 物理过滤（contact molecular surface、∆∆G、界面埋藏 SASA、形状互补）→ YSD 四组分选 + 位点饱和突变 SSM + 组合突变库；FP 案例用 ProteinMPNN + AF2 六判据过滤。
- **没有用的方法**：MD、QM 全无——本文是实验方法学论文，计算部分只做既有设计协议的搬运与 AF2 过滤。

### A. SAPP 主产线（从序列到表征板）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 设计氨基酸序列清单（FASTA/PDB） | 自动反向翻译 + 密码子/可合成性优化 + 拼接克隆接头；大基因自动切两段 | 默认切分阈值 1500 bp（eBlock 上限），<300 bp 补随机填充序列 | 下单表（电子稿直传 IDT）+ ECHO 移液协议 |
| A2 | 线性 DNA 片段（eBlocks，list price $0.07/bp） | 1 μL GGA（BsaI-HFv2+T4 连接酶）→ 直接转化 BL21(DE3)，不挑克隆、不测序 | ccdB 背景压制；质粒得率判据：50–100 μg 中提够 2000–4000 个 GGA 反应 | "The whole process from linear DNA to inoculated cultures is optimized to take 2 hours for up to 192 reactions"；转化效率 858 ± 443 CFU（N = 12） |
| A3 | 转化孔 | 96 深孔板自诱导培养基，恒温震荡 ≥20 h（1000 rpm、2.5 mm 轨道） | 无 | 4×1 mL 分种/设计 |
| A4 | 培养板 | 离心收菌 → B-PER 化学裂解 → 4×100 μL 并入一板 → Ni-NTA 96 孔（50 μL 树脂/孔）三步洗脱、真空 manifold | "The process is optimized to take 2 hours from cell harvest to starting SEC"（正文方法节表述） | 注射-ready 洗脱液（上样前 0.22 μm 过滤） |
| A5 | 洗脱液 | 自动 SEC 过夜（Superdex 75 或 200，5/150，100 μL 上样、0.65 mL/min） | "15 hours for 192 samples, <5 minutes per sample, see Methods"；仪器日容量 ~300 样 | 96/384 孔收样板 |
| A6 | 色谱图 | Python 批分析：峰检测、洗脱体积→分子量、A280 积分→浓度；生成 OT-2 代码自动归池+归一 | 汇总为单一开放格式数据框（HDF5） | "typical yields: 0.1–0.5 mg at 10–100 μM"（N = 576 直方图，Fig 1e） |
| A7 | 事后质量核验（回顾性） | 929 个 glycerol stock 混合 NGS 算完美匹配比例；863 个纯化蛋白做完整质谱 | "sequencing analysis of 929 GGA reactions with insert size below 314 bp showed that 89.3% had a clonal purity ≥ 90%"；MS 判据 "revealed the expected mass within ± 1 Da for 90% of all products (777/863)" | 产线可信度论证（跳过克隆QC的依据） |
| A8 | 端到端 | 全流程计时与成本口径 | 从线性 DNA 到数据表 | "End-to-end protocol execution takes 48 hours, with ~6 hours spent benchside using standard laboratory equipment"；"Complete end-to-end execution takes 48 hours (excluding commercial DNA synthesis), enabling rapid iteration cycles at a total cost per design equivalent to a few DNA oligos" |

### B. 应用一：ProteinMPNN 重设计荧光蛋白（FP）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | FPbase 的 WT FP 序列 + AF2 预测结构（UniRef30 MSA/HHblits） | MSA 逐位保守性评估；接触发色团残基、高保守残基、核心朝向残基（SASA<2.0 Å², pyrosetta）固定，其余非保守表面残基重设计 | "either 50% or 70% of the most conserved residues were kept fixed during ProteinMPNN sequence"；ProteinMPNN T = 0.01–0.5；AF2 浅 MSA（≤15 序列）复评 | "Overall, sequence identities of designs to WT ranged from 50 to 80% with a Levenshtein distance of up to 50 compared to their respective WT" |
| B2 | 设计池 | AF2 置信度 + 物理量六联过滤 | "Designs were selected based on the following metrics: AF2_plddt_mean > 0.8, AF2_ptm > 0.80, AF2_pae_mean <12.0, AF2_tm_score to WT > 0.7, AF2_tm_rmsd to WT < 1.5, AF2_sap_per_res <0.4" | 选 96 个构建体（含 12 个 WT 对照） |
| B3 | 96 构建体 | SAPP 产线 A1–A6 全流程，一周内拿到全部数据 | 收样后板读荧光（"Following SAPP purification of 88 designs and 12 respective WT controls"… "at a concentration of 20 µM"）；煮沸判据（95 °C 1 h 后 SEC 仍单体） | "In conclusion, using SAPP enabled 96 FP variants with large edit distances to be characterized within a week, providing detailed biochemical information (yield, dispersity, oligomeric state, absorbance and fluorescence) for each design"；部分变体（如 muGFP 源）耐热、光谱红移/Stokes 改变——"these results highlight that native redesign with ProteinMPNN can introduce non-trivial sets of mutations that push the FPs into a sequence space with altered spectral properties" |

### C. 应用二：RSV 寡聚结合体筛选（含上游计算漏斗）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | RSV F（SC-DM）site III / MPE8 表位 | Rosetta RIF 方法生成结合体库：21,400 脚手架 RifDock 对接 → FastDesign 定序列 → 物理过滤 → α-螺旋 motif 提取聚类 → grafting 回灌 → 补 polySer 到 65 aa | "Designs were filtered using contact molecular surface, Rosetta ∆∆G, interface buried solvent accessible surface area, and shape complementarity"；motif 聚类后取 best 5000；"All designs were padded to 65 amino acids with polyserines split evenly at the N and C termini" | "31,394 designs were ordered as an oligo pool (Agilent)"（正文另一处概览口径为 "The top ~31,000 designs were obtained as chip-based synthetic DNA, screened through yeast surface display, and optimized through site saturation mutagenesis"） |
| C2 | 31,394 设计 | YSD 四轮分选（表达→双阳→复分→1 μM 起 3 倍梯度稀释滴定）→ 命中者再下 SSM 库 + 组合库 | 稀释系列起点 1 μM、4 步 3 倍稀释；取"可见信号的最低抗原浓度"档收样测序 | 最优设计 cb13："had an affinity of 35 nM for RSV F protein"；cb4 = cb13 的 7 个点突变变体 |
| C3 | cb13/cb4 + 27 个去 novo 寡聚化结构域 | 每个结构域建 N 端/C 端融合两个入载体 → 58 构建体库（54+4 单体对照）走 SAPP；C2–C8 价数、结合域间距 10–65 Å | 组装正确 = SEC 洗脱体积落在预期寡聚态（分子量标准曲线）99% 置信区间内 | cb13 组：19/58 以中等以上表达（>0.1 mg/4 mL 培养）组装成目标寡聚态；cb4 组更高："The success rate was higher than for cb13 (33 of 58 constructs assembled to their target oligomeric state)"——作者结论 "not all binding/oligomerization domains are mutually compatible" |
| C4 | 组装正确的寡聚体 | 活病毒中和（HEp-2 + RSV A2 mKate，384 孔，3 倍系列稀释）+ SPR（SC-DM 芯片偶联，320 pM 起 6 步 5 倍） | IC50 四参数拟合；至少 3 次独立实验、双复孔 | "The oligomeric constructs vastly outperform monomeric cb13 with nHALC2_065 and nHALC3_919 having IC50s of 40 and 59 pM respectively, compared to 5.4 nM for their monomeric counterpart"；对照 "which targets the same epitope of RSV F and had an IC50 of 156 pM"；同价数不同几何差 25 倍（"nHALC2_065 is ~25-fold more potent than an alternative dimer, nHALC2_067"），N/C 端朝向差 10 倍（59 pM vs 530 pM）；C6/C8 高阶寡聚无改善 |
| C5 | cb13·F 复合物 | cryo-EM（Glacios，4.63 Å）验证设计界面 | 对齐靶标后 binder 全 Cα 比较 | "with 1.9 Å RMSD across all Cα of the binder when aligned on the target"；模型/密度入库 PDB 9YCF、EMD-72769 |

### D. 应用三：DMX（oligo pool → 序列确证的阵列克隆）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| D1 | Twist oligo pool | "we obtained an oligo pool encoding a library of 1500 de novo designed protein with lengths ranging from 275 to 400 bp"；KAPA HiFi 扩增，qPCR 监控提前终止 | 扩增不过平台期（防偏好） | 目的条带胶回收库 |
| D2 | 库 DNA | GGA（BsmBI）入三功能 DMX 载体（入池 BsmBI / 条形码 BsaI / 切出 GOI BsaI，带 ccdB）→ 电转表达株 → 铺板 → 克隆仪挑入 384 低盐板 | CFU 预估后定量挑 2500 菌落/板 | 384 孔菌液库 |
| D3 | 菌液板 | ECHO 4:1 压缩至 1536 孔 → 98 °C 30 min 热裂解 → 恒温 GGA 把 4 组位置条形码（24 UMI/组）连到 GOI → 混合回收 → ONT 纳米孔长读测序 | 编码容量 24⁴ > 330k 孔 | 条形码化混合库 |
| D4 | 测序数据 | 自动生信：basecall→质控过滤→按条形码组合解混→比对参考→生成共识序列→非冗余 pick-list→ECHO 重排阵列 | 判据：序列确证的单克隆 | "We successfully recovered 78% of the library variants as clonal, sequence-verified constructs by screening 4608 clones (3x the library complexity), approaching the theoretical maximum recovery rate of 92%" |
| D5 | 规模决策 | 库大小 vs 挑取量的成本曲线（Supplementary Fig 5 口径） | 大库最优规模："the optimal library size is about 2000 genes, requiring the sampling of about 8000 colonies"（>95% 回收）；小库 500 genes 手动挑 1500 菌落 | 比直接下单基因片段省 5×（500 库）/8×（2000 库）；只加 5 天 |

**流程骨架值得单独记住**：先造一把"尺子"（SAPP 的标准化数据输出），再拿三个互不相同的应用（FP 重设计、寡聚 RSV 中和剂、DMX 文库转换）去踩这把尺子；瓶颈每一环被解决后就显出下一环（克隆→SEC→DNA 成本），作者把每一环的容量数字都写成了可核算的量。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 48 小时 / ~6 小时 bench | 端到端总时长 / 人工操作时间 | "End-to-end protocol execution takes 48 hours, with ~6 hours spent benchside using standard laboratory equipment" |
| 2 小时 / 192 反应 | 线性 DNA→接种培养 | "The whole process from linear DNA to inoculated cultures is optimized to take 2 hours for up to 192 reactions" |
| 15 小时 / 192 样；<5 min/样 | SEC 过夜批量 | "15 hours for 192 samples, <5 minutes per sample, see Methods" |
| ~300 样/天 | 单台色谱仪容量（主瓶颈） | "the main bottleneck being SEC, with a capacity of ~300 samples per chromatographic instrument per day" |
| 0.1–0.5 mg @ 10–100 μM | 典型可溶产量（N=576） | "typical yields: 0.1–0.5 mg at 10–100 μM" |
| 89.3%（929 反应用 NGS，插入 <314 bp） | 克隆纯度 ≥90% 比例 | "sequencing analysis of 929 GGA reactions with insert size below 314 bp showed that 89.3% had a clonal purity ≥ 90%" |
| 777/863（±1 Da） | MS 验证正确质量 | "revealed the expected mass within ± 1 Da for 90% of all products (777/863)" |
| 858 ± 443 CFU（N=12） | 1 μL GGA 直接转化效率 | "transformation efficiency = 858 ± 443 colony-forming units (CFU) (mean ± standard deviation, N = 12)" |
| $0.07/bp；1500 bp 切分；300 bp 填充 | 片段下单单价 / 大基因处理 | "list price $0.07/bp" |
| 6 项 AF2 阈值（>0.8/>0.80/<12.0/>0.7/<1.5/<0.4） | FP 设计过滤 | "Designs were selected based on the following metrics: AF2_plddt_mean > 0.8, AF2_ptm > 0.80, AF2_pae_mean <12.0, AF2_tm_score to WT > 0.7, AF2_tm_rmsd to WT < 1.5, AF2_sap_per_res <0.4" |
| 50–80% 同一性；Levenshtein ≤50 | FP 重设计编辑距离 | "Overall, sequence identities of designs to WT ranged from 50 to 80% with a Levenshtein distance of up to 50 compared to their respective WT" |
| 88+12 样 @ 20 μM | FP 实测批次 | "Following SAPP purification of 88 designs and 12 respective WT controls" |
| 21,400 → 5,000 → 31,394 | RSV 上游漏斗（脚手架→motif→下单库） | "A rotameric interaction field (RIF) was generated against the MPE8 epitope. Next, a library of 21,400 scaffolds was docked against the RIF using RifDock"；"31,394 designs were ordered as an oligo pool (Agilent)" |
| 35 nM；4.63 Å；1.9 Å | cb13 亲和力 / cryo-EM 分辨率 / 界面偏差 | "had an affinity of 35 nM for RSV F protein"；"with 1.9 Å RMSD across all Cα of the binder when aligned on the target" |
| 58 构建体 → 19（cb13）/ 33（cb4） | 寡聚库组装命中 | "The success rate was higher than for cb13 (33 of 58 constructs assembled to their target oligomeric state)" |
| 40 / 59 pM vs 5.4 nM vs 156 pM（MPE8） | 寡聚/单体/抗体对照中和 | "The oligomeric constructs vastly outperform monomeric cb13 with nHALC2_065 and nHALC3_919 having IC50s of 40 and 59 pM respectively, compared to 5.4 nM for their monomeric counterpart"；"which targets the same epitope of RSV F and had an IC50 of 156 pM" |
| 25×；10× | 同价数几何差；N/C 端朝向差 | "nHALC2_065 is ~25-fold more potent than an alternative dimer, nHALC2_067" |
| 1500 设计池（275–400 bp）→ 4608 克隆 → 78%（理论 92%） | DMX 回收率 | "We successfully recovered 78% of the library variants as clonal, sequence-verified constructs by screening 4608 clones (3x the library complexity), approaching the theoretical maximum recovery rate of 92%" |
| 2000 基因 / 8000 菌落 / >95%；500 基因/1500 菌落；5×、8× | DMX 最优规模与省钱倍数 | "the optimal library size is about 2000 genes, requiring the sampling of about 8000 colonies"；"This approach is five and eight times more cost-effective (including reagent and sequencing costs) than ordering 500 and 2000 individual gene fragments, respectively" |
| 24⁴ > 330k 孔 | 组合条形码容量 | "Our approach uses four sets of position-specific barcodes comprising 24 unique molecular identifiers (UMIs) each, allowing for >330k wells to be tagged from a single 96-well plate of UMIs (24^4)" |
| 5 天 | DMX 端到端 | "The DMX pipeline is a 5-day protocol that leverages an isothermal DNA barcoding strategy and long-read sequencing" |
| 数万设计 | 该产线在 IPD 的累计使用 | "These protocols have already been used to experimentally produce and characterize tens of thousands of de novo designed proteins at the Institute for Protein Design" |
| 25 个载体 | 模块化克隆载体套件 | 正文（Methods Cloning / Supplementary Table 1，"the full list of 25 vectors deposited at Addgene" 为原文口径） |

## 5. 结论——作者说了什么

1. SAPP 是"rapid, modular, scalable and cost-effective protocol"，实现每天数百设计的阵列式生产与标准化表征，端到端 48 小时、bench ~6 小时、单设计成本约等于几条 DNA 寡核苷酸，"enabling at least an order of magnitude increase in throughput while reducing wetlab time"。
2. 可以跳过"挑克隆+测序验证"：ccd B 背景压制 + 事后 NGS/MS 统计（89.3% / 90%@±1 Da）足以保证"正确克隆是表达池主成分"；但该协议"primarily intended for screening purposes"，偶发假阴性。
3. FP 案例：96 条大编辑距离序列一周表征完毕，ProteinMPNN 表面重设计能把 FP 推进"光谱性质改变"的序列空间（个别变体耐 95 °C 煮沸仍单体、保留发色团吸收）。
4. RSV 案例：SAPP 快速筛出正确组装的寡聚体，最优二/三聚体 IC50 40–59 pM，与同表位 potent 单抗 MPE8（156 pM）同级或更好；几何（连接子、朝向）造成 10–25 倍功能差；高阶 C6/C8 无益。
5. DMX 案例：oligo pool→序列确证阵列克隆，5 天、回收 78%（上限 92%）、比基因片段省 5–8 倍，适合 ≥500–2000 基因规模；小批量仍用 SAPP 多克隆直筛。
6. 作者展望：标准化+低成本的实验数据流"will contribute to the development of new protein design models informed by experimental data, as well as enabling active learning approaches in protein design"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的真实贡献是"把判据成本写成了可审计的台账"**：每一步给"仪器容量×时间×单价"（SEC ~300/天、$0.07/bp、bench 6h），这正是我们项目缺的口径——任何判据先折算"每个通过闸口的候选花多少钱/多少机时"再决定用不用。
2. **"瓶颈迁移"是动态的**：克隆被消灭后瓶颈变 SEC，SEC 摊薄后变 DNA 合成，DMX 再削 5–8 倍后瓶颈回到"每天能测什么功能"。对我们的镜鉴：漏斗任何一环提速后必须重找瓶颈，不能假设成本结构不变。
3. **放弃事前 QC 的前提是有第二门事后验证**：他们敢跳测序验证，是因为有 NGS 池统计 + 完整质谱兜底，且明确该产物只用于"筛选"而非最终确证。我们若削减某中间验证（如省略中间产物纯化），需要同等地位的"事后第二方法"复核，否则证据链断。
4. **SEC 判组装是"尺寸判据"不是"结构判据"**：99% CI 洗脱体积无法区分同分子量的错误几何；他们用功能梯度（IC50 几何差异 25 倍）补判。对应我们：光谱/色谱的"表观判据"（保留时间/分子量）与"化学身份判据"（MS/MS 碎片）必须分层，不能互相冒充。
5. **他们把"失败样本"也做成标准数据**（每个失败设计同样有 yield/dispersity/SEC 曲线进同一数据框），这为后续训练留了负标签池——与 B09 的"筛子考卷"是同一思路的基建版。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：偶发假阴性，仅供筛选（"While highly efficient, our protocol may still occasionally yield false negative results, and thus is primarily intended for screening purposes"）；多克隆性随长度上升（"the small levels of polyclonality resulting from synthesis error are length-dependent, which can complicate using the protocol for longer proteins"）；产线定位——"The protocol was developed and optimized for wetlab validation of high-yielding proteins such as engineered and designed sequences, and may be less well suited for proteins that require complex expression and purification protocols"；DMX 只加 5 天但小库不经济（"while the polyclonal approach from SAPP is better suited for smaller campaigns (~100–200 designs) where faster turnaround time is desired"）。
- 我们读出：① 克隆纯度/MS 统计建立在"插入 <314 bp、E. coli 可溶表达"的样本空间上，对大蛋白、真膜蛋白、需要翻译后修饰的体系外推未验证；② RSV 漏斗的 19/58、33/58 是两个结合域的个案，不构成"寡聚化成功率"的通用数字；③ 本文所有功能判据（IC50、SEC 区间、煮沸后单体）都是"静态结合/组装"性质，与催化周转无对应；④ 全文无 MD/QM，不能作为任何物理法判据的命中率证据。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **"每候选边际成本 + 仪器日容量"的台账写法**直接搬进我们漏斗预算：把 LC-MS 梯度（样/天）、基因合成（$0.07/bp 类口径）、表达纯化 bench 时间逐项登记，任何判据先过"通过率÷单价"再上产线（与 B09 的效率公式互补：B09 算计算侧，这篇算湿侧）。
2. **板式标准化 + 开放数据框**：我们每个构建体无论成败都应输出同一组数据（表达量、产物峰面积、分步化学事件归类、失活对照信号），存成单一机器可读表——没有这个，未来任何"筛子考卷"都无从训练。
3. **"事后第二方法复核"代替"事前逐一 QC"**：候选数超出确证能力时，可仿其结构——主通道用便宜判据筛选、按统计抽样用正交法（我们是 LC-MS/MS 碎片 + 煮沸/酶失活对照）估假阳/假阴率，并公开该比率。
4. **"瓶颈迁移"检查点**：每轮实验结束记"本轮最大成本项是什么、被消灭后下一个是什么"，防止把上一轮瓶颈当永恒瓶颈。

**不可迁移（为什么不能照搬）**

1. **读出性质不同**：SAPP 的判据（产量、分散度、SEC 寡聚态、荧光、IC50）全部是静态理化/结合性质；目标酶的成败是三步化学事件的周转数与副产物比，LC-MS 产物定量无法用"SEC 99% CI"式的表观判据替代。不得把本文任何判据阈值当酶活闸口。
2. **通量口径不可挪用**："hundreds of designs per day"是表达纯化表征的容量，不是功能确证的容量；我们单轮 LC-MS 确证上限远低（一轮、至多数个构建体），不能拿 19/58、33/58、40 pM、78% 回收等数字为酶设计项目估算任何成功概率。
3. **E. coli 自诱导 + Ni-NTA 管线**不覆盖膜蛋白/需要伴侣或多亚基真核修饰的体系，作者自己限定适用域；我们的目标酶若涉及膜锚定或辅因子装载，不能默认适用。
4. **无计算筛选贡献**：本文的 AF2 六判据只是 FP 案例的入场券，其阈值不来自系统评估实验，不能引它论证我们的闸口选择。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/accelscaling2026.txt

- 本地全文：`data/interim/baker_lit/ft/accelscaling2026.txt`（Europe PMC 通路，2026-10-16 抓取，batches.tsv 第 7 行登记为 B24 唯一全文；另有登记底稿 `sources/baker.md:316–327`）。
- 对照底稿：`sources/baker.md` 第 316–327 行原卡（其"通量与命中率原始数字"段的引句与本卡引句同源）；汇总表 `sources/baker.md:605/606/611/612/622/648/660/666/678` 各处引用 B24。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：所有直双引号英文片段由 `scripts/verify_literature_cards.py`（参数 `--only B24 B25 B26 --no-report`）在本地全文做归一化（实体解码、引号/破折号统一、空白折叠）后的逐字查找；写卡前已用同一 `litcards_text.norm` 对全部候选引句预校验（一处因漏掉冠词 the 而 MISS，已改正；一处煮沸句因误加 and 而 MISS，已改正）。引句在正文（Abstract/Results/Discussion）与 Methods/图注中的位置已在第 4 节逐条标注。内容层面：本文无补充信息（成本明细计算在 SI，本卡未引），第 5/6 节分工已注明。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 2 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（实验方法学/自动化产线）
target=SARS-CoV-2/RSV F 位点III 迷你结合体（cb13/cb4 及其寡聚化库）、ProteinMPNN 重设计荧光蛋白（96 变体）、DMX 1500 设计 oligo pool
backbone_generation=上游沿用 Rosetta RIF/RifDock/FastDesign + YSD/SSM 与 ProteinMPNN+AF2 过滤；本文主体是构建自动化（反向翻译软件+GGA+ccdB 负筛选直转表达株）
computational_filters=FP 案例：AF2 pLDDT/PTM/PAE 均值、与 WT 的 TM-score/tm_rmsd、SAP per residue；无 MD、无 QM
thresholds=AF2_plddt_mean>0.8、AF2_ptm>0.80、AF2_pae_mean<12.0、AF2_tm_score to WT>0.7、AF2_tm_rmsd to WT<1.5、AF2_sap_per_res<0.4；组装判据=SEC 洗脱体积落在目标寡聚态 99% CI；克隆可信度判据=纯度≥90%、MS ±1 Da
md_used=否
qm_used=否
experimental_methods=SAPP（GGA 直转 BL21(DE3)、96 深孔自诱导、Ni-NTA 96 孔、自动 SEC、OT-2/ECHO 收样归一、色谱自动分析→HDF5、NGS/完整质谱回顾验证、板读荧光、SPR、活病毒中和 IC50、cryo-EM 4.63 Å）；DMX（oligo pool→恒温 GGA 组合条形码→ONT 长读→解混重排阵列）
pipeline_counts=RSV：21,400 对接→best 5,000 motif→31,394 设计 oligo pool→YSD+SSM→cb13（35 nM）→58 寡聚构建体→19（cb13 组）/33（cb4 组）组装→IC50 40/59 pM；FP：96 构建体（12 WT）→88+12 实测@20 μM；DMX：1500 设计池→4608 克隆→78% 回收（理论 92%）；2000 基因/8000 菌落→>95%
hit_rate=无统一命中率口径；SAPP 克隆纯度 89.3%（<314 bp）、质量正确 90%（777/863）；寡聚组装 19/58、33/58；作者定位=筛选用途、有假阴性
best_metric=RSV 中和最优 IC50 40 pM（nHALC2_065）与 59 pM（nHALC3_919），对标单抗 MPE8 156 pM；单体 cb13 5.4 nM、界面 cryo-EM 偏差 1.9 Å
cost_or_stat_note=$0.07/bp eBlock；端到端 48 h、bench ~6 h；克隆 2 h/192 反应；SEC 15 h/192 样、<5 min/样、~300 样/天/台；单设计成本≈几条寡核苷酸；DMX 比基因片段省 5×/8×、+5 天；转化效率 858±443 CFU
role_in_timeline=计算闸口（pAE 类，B09/B23）成熟后，把漏斗末端"送测与表征"改造成低价高通量标准产线，使"每周数百设计"的阵列湿实验成为可能，并为主动学习提供标准化失败/成功数据；是 Baker 组"用便宜高通量湿实验替代昂贵计算验证"路线的代表作
source_pointer=data/interim/baker_lit/ft/accelscaling2026.txt（全文）+ sources/baker.md:316-327（底稿）；PDB 9YCF / EMD-72769；代码 https://github.com/bwicky/SAPP_DMX
CSV回填-->
