# 周如鸿团队：MD/自由能筛选与实验命中率（调研于 2026-10-16）

> 成功测试（开工前定义）：本文件收录 ≥10 篇周如鸿（Ruhong Zhou，浙大定量生物中心/IQB）论文卡片，每个 DOI/PMID 均经 PubMed E-utilities / Europe PMC REST / Crossref API 实际调用核验（标题+作者+单位），并给出"90%+ 成功率"的可查证性判定（找到出处或明确声明未找到）。→ 判定见第四节。
>
> 检索途径：PubMed `zhou,ruhong[Author] AND 2019:2026[dp]`（164 篇，全部拉取摘要并按设计关键词筛选）；Europe PMC 全文/摘要检索（多次）；Crossref DOI 核对；bioRxiv/Europe PMC 预印本；PMC OA 全文 XML 5 篇精读。所有"✅核验"= 由上述 API 返回记录直接核对标题与作者。

## 〇、作者身份消歧说明（同名风险如何处理）

- 目标人物：Ruhong Zhou（周如鸿），浙大求是讲席教授，2020 年全职回国前为 IBM Watson 软物质科学系主任。其论文单位以 "Institute of Quantitative Biology (IQB), College of Life Sciences / School of Physics, Zhejiang University" 为主，通讯/资深作者位置。PubMed 作者索引 `Zhou, Ruhong[Author]`（2019–2026 命中 164 篇）+ 单位字段逐条核对。Europe PMC 记录中其 ORCID 出现为 `0000-0001-8624-5xx` 尾注（PNAS 2020 条目），未逐条落盘。
- 已剔除的同名/误匹配实例（均经作者列表核对）：
  1. **Zhou Rui**（Sunchon National Univ, 韩国，地衣代谢物/HIF-1α，PMID 42802108）——Europe PMC `AUTH:"Zhou R" AND "de novo protein"` 首条即此误配，剔除。
  2. **PNAS 2019 bithionol 抗 MRSA 持留菌论文**（PMID 31358625）——Europe PMC 全文检索命中"Ruhong Zhou"字样（引文），作者列表 Kim W…Mylonakis E 中无周如鸿，剔除。
  3. **ACS Nano 2020 "Distal Polybasic Cleavage Sites enhance Spike–ACE2 binding"**（10.1021/acsnano.0c04798）——作者为 Qiao Baofu & Olvera de la Cruz（Northwestern），非周组，剔除。
  4. **RaptGen**（Commun Biol 2022，PMID 38177576）——作者 Iwano/Hamada（东京工大），非周组，剔除。
  5. **TIP4P-D 水模型**：Europe PMC `"Ruhong Zhou" AND "TIP4P-D"` = **0 篇**；TIP4P-D 原始方法论文为 JCTC 2019 `10.1021/acs.jctc.8b01123`（Uppsala/van der Spoel 一系），周如鸿既非发明者、检索亦未见署名应用。**用户背景中"TIP4P-D"一条与周如鸿无直接文献关联**（他组的水模型工作是 CHARMM/IBM 大规模显式溶剂模拟体系本身）。
- **曹龙兴（Longxing Cao）× 周如鸿：PubMed `"Cao Longxing"[Author] AND "Zhou Ruhong"[Author]` = 0；Europe PMC `"Longxing Cao" AND "Ruhong Zhou"` = 0。两人没有发现任何合作论文。**曹龙兴为 Baker 组博后（2017–2021）→ 西湖大学独立 PI（2021–），其 de novo 大蛋白/跨膜蛋白/binder 库式设计与 Baker 管线同脉；与周如鸿仅在学术会议层面同场（如中国生物化学与分子生物学会 2026 全国大会"专题5 生物大分子设计"，曹龙兴报告 "Exploring De Novo Protein Design through Physics-Based Modeling and Deep Learning"）。讲座中"周如鸿团队的 de novo 设计"更可能指周组自己的**适配体/抗原肽/抗体的计算亲和力成熟型设计**（见下），而非 Baker 式骨架从头设计。

## 一、逐篇文献卡片

### [Z01] In silico design and validation of high-affinity RNA aptamers for SARS-CoV-2 comparable to neutralizing antibodies（CAAMO 框架）
- 作者: Yanqing Yang, Lei Qiao, Yangwei Jiang, Zhiye Wang, Dong Zhang, Damiano Buratto, Liquan Huang, **Ruhong Zhou**（周如鸿为末位资深作者；通讯作者归属未从 XML 抓到，标"未核"）/ 单位: 浙江大学生命科学学院定量生物研究所 + 植物环境韧性国家重点实验室（黄 Liquan 实验端）
- 期刊, 年: eLife, 2026（在线 2026）
- DOI: 10.7554/eLife.107785 ✅（Europe PMC EXT_ID 核验）  PMID: 42446520 / PMCID: PMC13368180（全文 OA，已精读）
- 链接: https://doi.org/10.7554/eLife.107785
- 设计对象 + 实验验证: SARS-CoV-2 RBD 靶向 RNA 适配体（起点为 SELEX 得到的 Ta 序列）；**自足闭环**（计算端浙大 IQB + 实验端浙大生命科学学院）。
- 候选生成: RNA 二级结构（Mfold）→ SimRNA 等 3D 构象系综（25 个代表构象）→ 4×25×10 = **1000 个对接复合体池** → 聚类（0.2 nm RMSD cutoff）→ **6 个候选结合模式**。
- **MD/自由能筛选器**: ①各模式 100 ns MD 精修 + **MM/GBSA**（gmx_MMPBSA，末 300 ns 抽 600 帧）+ SMD 拉膜动力学；判据：构象01 ΔG = **−142.93 ± 7.65 kcal/mol**，其余五个 **> −120 kcal/mol**（相差 ~20 kcal/mol 量级即入选）；②界面突变全扫描 → Mfold 二级结构相似性 **BP similarity > 0.9 才允许进 FEP**；③**FEP（alchemical，5 次独立重复）ΔΔG<0 的设计突变送合成**；④对 SARS-CoV-2 变体用 **FEP/HREX**（Hamiltonian 副本交换）预测逃逸（5 Å 内残基参与微扰）。
- QM 使用: 否（经典力场）。
- 实验验证手段: EMSA（半定量 ΔΔG_exp）、荧光结合、ITC 类结合曲线（Prism 拟合 Kd）。
- **命中率原始数字（原文）**: "Notably, the success rate of the in silico design via the CAAMO framework is very promising, with **five out of the six (~83%)** computationally designed candidate aptamers experimentally confirmed to have improved binding affinities."；"the designed aptamer Ta G34C … **Kd = 33.x nM**，较 WT Ta **Kd = 110.x nM** 提升约 3.3 倍；其余四条约 2 倍提升（Kd ≈ 55 nM）"（PMC13368180 全文，Figure 4–5）。
- 演进链位置: 2024–2026 "AI+物理混合、多阶段漏斗"阶段的旗舰（DL 只做结构预测，筛选全部押在 MM/GBSA + FEP 上）。

### [Z02] In silico design and validation of high-affinity RNA aptamers targeting epithelial cellular adhesion molecule dimers
- 作者: David R. Bell, Jeffrey K. Weber, Wang Yin, Tien Huynh, Wei Duan（Deakin 医学院，实验端）, **Ruhong Zhou** / 单位: 浙江大学定量生物中心 + IBM Watson（2020 过渡期双单位）
- 期刊, 年: PNAS, 2020, 117(15)
- DOI: 10.1073/pnas.1913242117 ✅（Europe PMC + PubMed 双核）  PMID: 32234785（PMCID PMC7165443 在库但无 OA 全文 → **仅摘要级证据**）
- 链接: https://doi.org/10.1073/pnas.1913242117
- 设计对象 + 实验验证: EpCAM 靶向 RNA 适配体优化；模拟+合作实验闭环。
- 候选生成: 基于专利纳米摩尔适配体 EP23 的结构预测 → 结合模式判定 → 合理突变优化。
- **MD/自由能筛选器**: 摘要原文："predicts their binding modes and then optimizes them for EpCAM with **molecular dynamics simulations, docking, and free energy calculations**"（具体阈值摘要不可见，未核验到数字）。
- QM: 否。
- 实验验证手段: **ITC**（确认设计适配体亲和力优于 EP23）；native 结合实验证明 EpCAM 二体才是表位。
- 命中率: 摘要称"developed **two optimal** EpCAM aptamers"且"experiments further confirm…exhibit enhanced affinity"→ 合成端 2/2 阳性（**仅摘要级**）。
- 演进链位置: IBM→浙大过渡期第一篇"设计+实验"闭环论文，方法模板（docking+MD+FE→合成）沿用至 Z01。

### [Z03] Multi-strategy embedded framework for neoantigen vaccine maturation（NEOM）
- 作者: Kevin C. Chan, Ruofan Jin, Yuxuan Yang, Lei Fu, **Ruhong Zhou** / 单位: 浙大物理学院/生命科学学院/IQB + 上海高等研究院
- 期刊, 年: Scientific Reports, 2026, 16
- DOI: 10.1038/s41598-025-34618-8 ✅  PMID: 41554915 / PMCID: PMC12865018（OA，已精读全文）
- 链接: https://doi.org/10.1038/s41598-025-34618-8
- 设计对象 + 实验验证: HLA-A*02:01 呈递的肿瘤抗原肽（起点 GAD65 VMN 等）亲和力成熟；**自足闭环**。
- 候选生成: 理论肽空间 >**10^9** → 自适应 MCMC（policy/structure/evaluation/selection 四模块迭代；structure 模块用 **PANDORA** 建 3D pHLA）扩展肽池 → filter 模块用 **NetMHC 4.0（强结合阈值 0.5、弱结合 2，percentile rank）+ Consensus + EpiScan** 三模型投票排序。
- **MD/自由能筛选器**: ①100 ns 全原子 MD 稳定性判据：肽骨架 RMSD、P2 锚定残基 RMSD、埋没表面积（Buried-SA）；原文："This metric alone yields an average **success rate of around 80%**… more rigorous criteria（加 2nd-Res RMSD/BSA）… 仍保持 **~40%**"（此处指与实验稳定结合的符合率）；②进入 FEP 前的硬门槛："final structure was chosen based on RMSD analysis, confirming structural stability (**<0.5 nm**) for **over 200 ns**"；③**FEP**：30 个 λ 窗口 × 600 ps = 18 ns/次，≥3 副本，结合+游离两态 **≥108 ns/突变**；production MD 500 ns（10 ns 平衡，NAMD、PME、CHARMM 体系）。
- QM: 否。
- 实验验证手段: 肽合成（生工生物）→ **MHC-I 四聚体肽交换实验 + 流式细胞术**（Q1/交换效率，野生型 VMN 交换率 ~86% 作参照）。
- **命中率原始数字（原文）**: "we narrowed **38** initial candidates to **six** with favorable binding affinities, of which **five were validated** by MHC tetramer exchange and flow cytometry assays"（38→6（FEP）→实验 6 条中 5 条阳性，**5/6 ≈ 83%**，除 pep4 外全部优于 WT 交换效率）。
- 演进链位置: 2025–2026 生成式（MCMC）+ 物理精筛（FEP）两阶段漏斗的代表；给出全组少见的**逐级递减候选数字**。

### [Z04] A mutagenesis study of autoantigen optimization for potential T1D vaccine design
- 作者: Yi Song, David R. Bell, Rizwan Ahmed, Kevin C. Chan, Sangyun Lee, Abdel Rahim A. Hamad, **Ruhong Zhou**（实验端: 明尼苏大学 Gregersen 一系，T1D 免疫）
- 期刊, 年: PNAS, 2023, 120(15)
- DOI: 10.1073/pnas.2214430120 ✅  PMID: 37040399 / PMCID: PMC10120010（OA，已精读全文）
- 链接: https://doi.org/10.1073/pnas.2214430120
- 设计对象 + 实验验证: HLA-DQ8–X-idiotype–TCR 自身抗原复合物（1 型糖尿病疫苗抗原）；模拟+合作实验闭环。
- 候选生成: 锚定残基 p1/p4/p6/p9 + 高接触面 p7 的全点突变穷举（SI Table S1）→ 点突变不乐观后转**双突变与换位突变（swap mutations）**。
- **MD/自由能筛选器**: ①500 ns MD（310 K，NAMD2，CHARMM36）；入选结构须 RMSD 稳定（**<0.5 nm 持续 300+ ns**）；②初筛 **FEP 34 λ 窗口 × ≥200 ps = 6.8 ns/突变**（soft-core）；③有希望的突变复算 **≥34 ns × 5 副本 × 2 态 = ≥340 ns/突变**；④ΔΔG<0 判"增强"。原文承认"the low success rate of point mutations"（单点突变命中低）→ 这是转向双/换位突变的设计动因。
- QM: 否。
- 实验验证手段: CFSE/细胞增殖实验 + 流式（CD69 活化）+ HLA-DQ8 稳定 tetramer 类检测。
- **命中率原始数字（原文）**: "revealing that **all designed antigens increased CD69 activation** and **four out of seven**"（功能读出 4/7≈57%，活化标记 7/7；且原文明确说预测与实验的相关系数"though low…sufficient to identify enhanced and reduced binders"）。
- 演进链位置: 2021–2023"纯 FEP 物理筛选"阶段核心论文；也是"送合成 N 很小、逐条回看 ΔΔG 符号正确率"模式的样本。

### [Z05] Mutagenesis-based optimal design of plant peptide phytosulfokine for enhanced biological activity
- 作者: Rui Ye, Chen Xu, Zhong-Jie Ding, Shao-Jian Zheng, Siewert-Jan Marrink（格罗宁根）, Dong Zhang, **Ruhong Zhou**（实验端: 浙大黄 Liquan 植物肽激素实验室）
- 期刊, 年: Comput Struct Biotechnol J, 2025, 27:1869-…（卷页未逐字核验，DOI 为准）
- DOI: 10.1016/j.csbj.2025.03.029 ✅  PMID: 40230409 / PMCID: PMC11994915（OA，已精读全文）
- 链接: https://doi.org/10.1016/j.csbj.2025.03.029
- 设计对象 + 实验验证: 植物五肽激素 PSK（二硫酸酪氨酸修饰肽）类似物设计；**自足闭环**。
- 候选生成: PSK–AtPSKR1^LRR 复合物建模 → 丙氨酸扫描 + 去硫酸扫描（FEP）→ 选 Q5 位为可突变热点 → 设计 PSK Q5A、PSK Q5K。
- **MD/自由能筛选器**: ①MD：WT 复合物 1000 ns × 3 副本、单突变体系 700 ns × 3（GROMACS 体系、TIP3P、PME、1.2 nm 截断、RMSD 均值 ~2.5 Å 判稳定、接触概率取末 100 ns）；②**FEP**：18.4 ns/次 × 6 副本 × 结合/游离两态 = **220.8 ns/突变**；先拿 DcPSKR^LRR 体系与 ITC 实验 ΔΔG 对标校准（"good agreement between experimental measurements and FEP calculations"），再用于 AtPSKR1 体系；关键数字：PSK sY1A ΔΔG = **+4.87 ± 1.16 kcal/mol**、sY3A **+4.60 ± 1.34**（去硫酸 sY1Y +1.24、sY3Y +1.07）→ 判"硫酸酪不可动"；Q5 位耐受 → 突变增强方向（Table 3，ΔΔG<0）入选合成。
- QM: 否（硫酸酪氨酸用现成力场参数）。
- 实验验证手段: 合成肽 + 拟南芥/油菜根growth 促进实验（100/200 nM 处理）+ PSKR1-BAK1 互作检测。
- **命中率原始数字（原文）**: "**two designed PSK analogs (PSK Q5A and PSK Q5K) … detectably increase the root growth promotion, consistent with the FEP calculations**"（合成 2/2 阳性；样本量极小）。
- 演进链位置: 展示"先用另一物种受体复合物对 FEP 做**定量校准**，再拿 ΔΔG 阈值当筛选器"的最完整方法学细节。

### [Z06] Physical insights guided rational design of anti-EGFR antibody to reverse the acquired resistance
- 作者: Mingjiao Zhang, Yaqi Fu, Teng Xie, Zaixing Yang, Dong Zhang, **Ruhong Zhou** / 单位: 浙大 IQB
- 期刊, 年: Int J Biol Macromol, 2025
- DOI: 10.1016/j.ijbiomac.2025.141304 ✅  PMID: 39986495（**无 OA 全文 → 仅摘要级证据**）
- 链接: https://doi.org/10.1016/j.ijbiomac.2025.141304
- 设计对象 + 实验验证: 西妥昔单抗（Cetuximab）CDR 突变体，对抗 EGFR K489E/I491M 耐药突变；模拟+合作实验。
- 候选生成: 系统梳理 EGFR 胞外区逃逸突变 → MD 静电学分析定位界面电荷失配 → 针对性设计 2 条变体（静电补偿 + 空间位阻调整）。
- **MD/自由能筛选器**: 摘要原文："Through **molecular dynamics simulations and free energy perturbation calculations**, we discovered that most resistant mutations primarily alter the **electrostatic properties** of the binding interface"；设计变体须 FEP 预测亲和力回升。具体 ns/阈值数字摘要不可见（未核验）。
- QM: 否。
- 实验验证手段: **SPR** 结合 + HEK-293T Western blot 磷酸化抑制。
- 命中率: "the **two designed Ctx variants exhibit improved binding affinity** to the corresponding EGFR mutants compared with wild-type Ctx"→ SPR **2/2 成功**，其中 CtxD103R 功能验证 1/1（**仅摘要级**）。
- 演进链位置: "MD 出机理解剖（静电失配）→ 按机理设计 1:1 对应突变体"的高置信打法，样本小但方向由物理洞察锁定，是成功率的主要来源。

### [Z07] ANUBI: A Platform for Affinity Optimization of Proteins and Peptides in Drug Design
- 作者: Damiano Buratto, Wanding Wang, Xinyi Zhang, Qiujie Zhu, Jia Meng, Daniel J. Rigden, **Ruhong Zhou**, Francesco Zonta（CNR 那不勒斯）
- 期刊, 年: J Chem Theory Comput, 2026（预印本 bioRxiv 2025.10.20.683353，✅ Europe PMC PPR 核验）
- DOI: 10.1021/acs.jctc.5c01640 ✅  PMID: 41401395（出版商全文付费 → 摘要级 + 预印本页面信息）
- 链接: https://doi.org/10.1021/acs.jctc.5c01640
- 设计对象 + 实验验证: 通用蛋白/多肽亲和力成熟自动化平台（演示体系含抗体-肽）。**未见湿实验**（预印本页面与摘要均无合成/结合实验描述）。
- 候选生成: 用户输入复合物模型 → **Monte Carlo 定点突变系统扫描**选定区域，按结合自由能差保留有利突变（"generating dozens of…"）。
- **MD/自由能筛选器**: MC + **MM/PBSA 类端点法**批量打分；WebFetch 预印本页要点："dozens of optimized variants in 20 days on a single GPU, **affinity gains ~20 kcal/mol**（累计 MM 能量改善）"（页面转述，全文未核验，谨慎引用）。
- QM: 否。
- 命中率: 无实验数据可报。
- 演进链位置: 2025–2026 把组内 FEP/MM-GBSA 打分**产品化/软件化**的一步（供下游"送去合成"前的大规模粗筛）。

### [Z08] Assessing Computational Strategies for the Evaluation of Antibody Binding Affinities
- 作者: Ida Autiero, Damiano Buratto, Fengyi Guo, Wanding Wang, Malay Ranjan Biswal, Kevin C. Chan, **Ruhong Zhou**, Francesco Zonta
- 期刊, 年: J Chem Theory Comput, 2025
- DOI: 10.1021/acs.jctc.5c01231 ✅  PMID: 41129205（摘要级；另有预印本 10.1101/2025.09.25.678535 ✅）
- 链接: https://doi.org/10.1021/acs.jctc.5c01231
- 设计对象 + 实验验证: 方法校准论文——针对 CXCR2 N 端肽的抗体 panel，比较多种计算亲和力算法与实验亲和力的一致性。
- **MD/自由能筛选器身份之争（原文）**: "we find that **equilibrium MM/PBSA (MMPBSA) calculations yield better agreement with experimental binding affinities than nonequilibrium potential-of-mean-force (PMF) evaluations**, underscoring the system-dependent performance of these methods"——即该组在"筛选器该用哪个"上给出的实证裁决：**平衡态 MM-PBSA > 非平衡 SMD-PMF**（在其抗体-肽体系）。
- QM: 否。
- 命中率: 不报命中率，报相关性/排序一致度（全文付费未核验具体 R²）。
- 演进链位置: 给 Z01/Z07 的 MM/GBSA–FEP 组合提供"为什么可信"的方法学底座。

### [Z09] A free energy perturbation-assisted machine learning strategy for mimotope screening in neoantigen-based vaccine design（FEPaML）
- 作者: Qinglu Zhong, Kevin C. Chan, Lei Fu, **Ruhong Zhou** / 浙大 IQB
- 期刊, 年: Brief Bioinform, 2025
- DOI: 10.1093/bib/bbaf254 ✅  PMID: 40635188（全文在 PMC 未核验，摘要级）
- 链接: https://doi.org/10.1093/bib/bbaf254
- 定位: **筛选器的分层设计说明书**——ML 模型负责海量"结合/不结合"分类，但对"比亲代更强的 mimotope"分辨不足；FEP（alchemical）负责定量 ΔΔG 精排。原文："ML models facilitate high-throughput screening… but struggle to distinguish mimotopes from original neoantigens; in contrast, alchemical methods such as FEP provide quantitative binding free-energy differences… but are computationally intensive" → **ML 粗筛万级 → FEP 精排 top 百级**的两阶段逻辑（组内标准漏斗的显式表述）。
- 命中率: 计算评估为主，无合成端数字（摘要级）。

### [Z10] Integrating Physics-Based Simulations with Data-Driven Deep Learning Represents a Robust Strategy for Developing Inhibitors Targeting the Main Protease（Deep-CovBoost）
- 作者: Yanqing Yang, Yangwei Jiang, Dong Zhang, Leili Zhang, **Ruhong Zhou**（张 Leili 为合作者，IBM 时代深度学习侧）
- 期刊, 年: J Chem Inf Model, 2025
- DOI: 10.1021/acs.jcim.5c01307 ✅  PMID: 40767530（**仅摘要级证据**，未见 OA 全文）
- 设计对象: 冠状病毒主蛋白酶（Mpro）非共价抑制剂优化（分子层面，非蛋白大分子）。
- 筛选器: 深度学习生成/优先级排序类似物 → **FEP + MD 严格验证**；输出 I3C-1、I3C-2、I3C-35 等"增强结合（利用 S4/S5 亚口袋）"候选。摘要未提合成/酶活实验 → 保守判定为**计算验证级**（若全文有湿实验，此处判为待核）。
- QM: 摘要未提。
- 演进链位置: "AI+MD"混合（DL 生成 + 物理精筛）在小分子侧的同构体现。

### [Z11] In Silico Design of High-Affinity gp100 Antigenic Mimotopes for Targeting Melanoma
- 作者: Rui Ye, Yuxuan Yang, Kevin C. Chan, Dong Zhang, **Ruhong Zhou**
- 期刊, 年: J Phys Chem B, 2025
- DOI: 10.1021/acs.jpcb.5c01507 ✅  PMID: 40692510（**纯计算**，摘要级）
- 筛选器: 全原子 MD + **FEP** 对 gp100_280-288(288V) 做 in silico 突变扫描；双重判据——既要看 **peptide–HLA ΔΔG 降低**、又要 **TCR–pHLA ΔΔG 不劣化**（E3I/E3L 双双通过；E3A/E3V 因 HLA 口袋填充不足致肽 4-6 位扭曲而被拒）。给出"自由能之外必须有结构解释"的组内惯例（"dynamic pocket"概念同源见 Z12）。
- 命中率: 无实验送检数字（论文本身不声称闭环）。

### [Z12] In silico design of high-affinity antigenic peptides for HLA-B44
- 作者: Mei Feng（兰州大学-浙大联培）, Kevin C. Chan, Qinglu Zhong, **Ruhong Zhou**
- 期刊, 年: Int J Biol Macromol, 2024
- DOI: 10.1016/j.ijbiomac.2024.131356 ✅  PMID: 38574928（**仅摘要级**）
- 筛选器: MD + FEP 突变设计 → "Enhancement in binding affinities compared to the wild-type was found in **three out of five**"——注意这是**计算端 FEP 的预测分布**（3/5 判增强），非湿实验命中率。
- 机制输出: p6-Arg/p7-Lys 引发 groove "induced-fit" 构象迁移；提出 HLA "dynamic pocket"。
- 演进链位置: 纯物理筛选产线的"计算命中率"参照。

### [Z13] Design of TCR-mimicking binders for pHLA with high potency（预印本）
- 作者: Teng Xie, Yaqi Fu, Sha Gong, Damiano Buratto, **Ruhong Zhou**
- 年份/来源: bioRxiv 2025.10.03.680404 ✅（Europe PMC PPR 核验；截至调研未见期刊接收记录）
- 链接: https://doi.org/10.1101/2025.10.03.680404
- 设计对象: p53 R175H–HLA-A*02:01 与 KRAS G12V–HLA-A*03:01 的高选择性结合蛋白/肽（TCR 模拟物）。
- 筛选器（摘要原文）: "**molecular-dynamics–guided electrostatic filtering** yielded **nanomolar binders with >10-fold selectivity** over wild type"；无静电线索的体系改用 **MPNN（消息传递网络）优化**；"When reapplied to p53 R175H, these strategies improved **success rates from 2/5 to 5/5**, with most candidates exhibiting minimal or no binding to the wild-type complex"。
- 命中率: **5/5（100%）**——注意为预印本自述（"success rates"应指 SPR/结合验证，全文未核）；这是全部公开材料中最接近"90%+ 成功率"的数字，但样本仅 5 个。
- QM: 未提。

### [Z14] De Novo Evolution of an Antibody-Mimicking Multivalent Aptamer via a DNA Framework
- 作者: Linlin Tang, …, Chaoyong Yang, Teng Xie, Dong Zhang, **Ruhong Zhou**, Yanling Song, Jie Song（上海交大 杨正/田博之/宋杰一系为实验主导）
- 期刊, 年: Small Methods, 2023
- DOI: 10.1002/smtd.202300327 ✅  PMID: 37086150（摘要级）
- 定位: 实验端 DNA 框架文库 SELEX"**从头进化**"多价适配体（Amap）+ 周组"molecular modeling"（结合模式与多价协同的解释性模拟）+ 磁镊单分子验证。属于"实验筛选为主、计算解释为辅"的合作论文——与周组主线的"计算筛选→小批量合成"方向相反，说明其闭环并非所有"design"论文都跑通。
- 命中率/90%: 不适用（计算端不做准入判据）。

### [Z15] Dynamics-Based Peptide-MHC Binding Optimization by a Convolutional Variational Autoencoder: CASTELO
- 作者: David R. Bell, Giacomo Domeniconi, Chih-Chieh Yang, **Ruhong Zhou**, Leili Zhang, Guojing Cong（IBM Research）
- 期刊, 年: J Chem Theory Comput, 2021
- DOI: 10.1021/acs.jctc.1c00870 ✅  PMID: 34793168（摘要级）
- 定位: **IBM 时代的"AI+MD"雏形**：在 4 抗原×4 HLA 血清型共 **48 个体系的 MD 轨迹**上训练卷积变分自编码器（CVAE），输出逐残基结合贡献并生成更高 HLA-II 亲和力的设计抗原；"ML-MD predictions **agree well with experimental binding results** and FEP-predicted affinities"（实验数据来自合作者，设计端纯计算）。
- 演进链位置: 深度学习进入筛选器的最早组内节点（2021），2025–2026 被 FEPaML/NEOM/Deep-CovBoost 制度化。

### [Z16] QM（量子力学）使用取证——汇总卡片（3 篇代表 + 结论）
- **[✅] Development of a polarizable force field for proteins via ab initio quantum chemistry** — Kaminski, Stern, Berne, Friesner, …**Ruhong Zhou**, Halgren; J Comput Chem 2002, DOI 10.1002/jcc.10125（PubMed 核验作者）。QM 用途：**从头算数据拟合蛋白质极化力场参数**（气相二肽多体效应 RMSD 0.22 kcal/mol 级）。
- **[✅] Amino acid analogues bind to carbon nanotube via π–π interactions: comparison of MM and QM calculations** — Z. Yang, …**Ruhong Zhou**; J Chem Phys 2012, DOI 10.1063/1.3675486。QM 用途：**DFTB-D 校准 CNT–芳香残基 π–π 作用**，为纳米-蛋白界面力场背书。
- **[✅] The ground state and electronic structure of Gd@C82: first principle density functionals** — X. Dai, …**Ruhong Zhou**; J Chem Phys 2014, DOI 10.1063/1.4904389。QM 用途：**DFT 函数选择验证金属富勒烯电子结构**（对应其 Gd@C82(OH)22 纳米酶模拟的力场前置工作）。
- **结论**: 周组对 QM 的使用集中于**力场参数化与纳米材料电子结构**（哥伦比亚/IBM 时期），2019–2026 的设计-筛选管线（Z01–Z13）中**没有一篇用 DFT/QM/MM 作为候选准入判据**；筛选器全部是 MM/GBSA、MM/PBSA、FEP(alchemical)、FEP/HREX、SMD-PMF（后者在 Z08 被其自有数据否决）与 MD 稳定性度量（RMSD/BSA/接触数）。质子转移/酶催化类 QM/MM 工作未见。

## 二、筛选级联总结表（周组"设计→送合成"漏斗）

| 阶段 | 工具/判据 | 具体阈值（原文出处） | 剩余规模 | 出处 |
|---|---|---|---|---|
| 0. 空间定义 | 理论序列空间 | pHLA 肽空间 >10⁹；适配体突变空间=界面残基全扫描 | 10⁹+ | Z03, Z01 |
| 1. 生成/穷举 | MCMC 进化（NEOM）、对接系综（CAAMO 4×25×10=1000 pose）、全点突变扫描（T1D p1/4/6/7/9）、DL 生成（Z10/Z13 MPNN） | NetMHC4.0 strong<0.5 / weak<2 percentile；BP similarity **>0.9** 才准进 FEP | 数百–数千 | Z01/03/04/10/13 |
| 2. MD 稳定性预筛 | 全原子显式溶剂 MD + RMSD/锚残基RMSD/Buried-SA/接触概率 | **RMSD<0.5 nm 持续 200 ns（NEOM）/ 300 ns（T1D）**；单用骨架 RMSD 符合率 ~80%，加严 ~40%（NEOM 自述）；轨迹 100–1000 ns × 3–6 副本 | 数十 | Z01/03/04/05 |
| 3. 自由能精排（准入层） | **FEP（alchemical，soft-core，NAMD/组内自有代码）为主；MM/GBSA(gmx_MMPBSA) 做模式判别与大批量打分** | FEP 收敛要求：30–34 λ 窗 × 200–600 ps/窗，**≥3–6 副本 × 结合/游离两态 = 108–340 ns/突变**；判据 **ΔΔG < 0**（相对亲代）；构象选择用 ΔG 差 ≥ ~20 kcal/mol（CAAMO −142.9 vs >−120）；PSK 体系先与 ITC 对标验证 FEP 精度 | 6–40 | Z01/03/04/05/07/09 |
| 4. 机理一票否决 | 静电/结构可解释性 | "仅 ΔΔG 好但结构机制不通（E3A/E3V 肽扭曲）则不推"；抗体设计走"静电失配→定点电荷补偿" | 2–6 | Z06/11/12 |
| 5. 湿实验终审 | 合成 + SPR/EMSA/ITC/四聚体交换/细胞实验 | 报告 N 个合成、Kd/功能提升倍数 | 5–7 条 | 全部闭环论文 |

**送合成→成功对照表**（"成功率"的公开全部样本）：
| 论文 | 合成/测试数 | 成功数 | 成功率 | 实验类型 |
|---|---|---|---|---|
| CAAMO eLife 2026 | 6 | 5 | **~83%（原文自报）** | EMSA/结合曲线（Kd 110→33 nM） |
| NEOM Sci Rep 2026 | 6 | 5 | 83% | MHC 四聚体交换+流式 |
| EpCAM aptamer PNAS 2020 | 2 | 2 | 100%（摘要级） | ITC |
| PSK CSBJ 2025 | 2 | 2 | 100% | 拟南芥/油菜根生长 |
| 抗 EGFR Ctx IJB 2025 | 2 | 2 | 100%（摘要级） | SPR；功能 1/1 WB |
| T1D PNAS 2023 | 7 | 4（增殖）/7（CD69） | 57%/100% | 细胞实验 |
| TCR-mimic 预印本 2025 | 5 | 5 | 100%（自报） | 结合验证（全文未核） |
| HLA-B44 IJB 2024 | 5（计算） | 3 | 60%（纯计算，未送湿） | — |
| ANUBI JCTC 2026 | 0 | — | 无实验 | 平台论文 |

## 三、方法演进时间线

- **1998–2019（哥大/IBM 时期，纯机制）**：Blue Gene 大规模 MD 蛋白质折叠/去溶剂化（Science 2004、Nature 2005）、Aβ 与淀粉样、水模型对界面疏水效应的影响；QM 只做力场参数化（Z16）。设计含义仅体现在"Gd@C82 纳米酶机理 → implication for de novo design"这类**面向纳米酶理性设计的机制启示**（JACS 2011，无合成闭环）。筛选逻辑此时不存在——没有"设计-验证"任务。
- **2020–2022（闭环起点）**：PNAS 2020 EpCAM 适配体（Bell/Zhou）确立模板：**docking + MD + 自由能计算 → 2 条送合成 → ITC 确认**。同组小分子侧（MRSA 膜活性、C3N 吸附蛋白）是合作机制研究。CASTELO（Z15, 2021）首次把 CVAE 训练在 48 条 MD 轨迹上，AI 进入打分环节但只作辅助。
- **2023–2024（纯物理 FEP 主导 + 暴露痛点）**：PNAS 2023 T1D（Z04）：单点突变 FEP"success rate 低"→ 被迫上双突变/换位突变；送 7 回 4。HLA-B44（Z12）纯计算端 3/5。此阶段筛选器 = FEP + 长时间 MD 稳定性硬门槛（<0.5 nm 300 ns），瓶颈是算力（每突变 ≥340 ns）与 FEP 精度（力场参数误差致 ΔΔG 量级偏大，CAAMO 审稿意见亦承认）。
- **2025–2026（分层混合漏斗成体系）**：①MM/GBSA-MC 粗筛产品化（ANUBI Z07）；②ML 粗筛 + FEP 精排显式化（FEPaML Z09、NEOM Z03、Deep-CovBoost Z10）；③筛选器本身的可靠性实证（Z08：平衡 MM-PBSA 优于非平衡 PMF）；④二级结构保持性（Mfold BP>0.9）等"正交过滤器"加入准入链（Z01 原文明说"custom loss 与过滤器保持正交以降低假阳性"）；⑤MPNN+MD 静电过滤（Z13）。实验端全部为**个位数送样、高命中（5/6、5/5、2/2）**。
- **动因**：从"广撒网预测"转向"漏斗收口 + 机理一票否决"，因为湿实验（SPR/EMSA/合成）贵而慢，FEP 贵但可信度已被自有对照集校准；把 DL 定位为"生成候选/降低 FEP 前置浪费"，把 FEP 定位为"唯一准入判据"，把结构机理分析定位为"否决权"。

## 四、关于"90%+ 成功率"的可查证性判定

**结论：未在公开文献中找到"周如鸿团队设计蛋白成功率 90%+"这一声明的原始出处。**（截至 2026-10-16，检索了 PubMed/Europe PMC 全部 2019–2026 设计类摘要、5 篇 OA 全文、bioRxiv 预印本、中文新闻与讲座报道；无任何一篇论文或新闻稿出现 "90%"/"九成" 的成功率表述。）

最接近的公开数字（即讲座口径的可能来源）：
1. **CAAMO（eLife 2026）自报 ~83%**（6 设计 5 确认），原文用词即 "success rate … (~83%)"——样本小、且限定"结合亲和力提升"这一宽松判据；
2. **NEOM 2026** 6 投 5 回（83%）；
3. **TCR-mimic 预印本 2025** 明示 "improved success rates from 2/5 to **5/5**"（100%，5 个样本，未同行评审）；
4. EpCAM（2/2）、PSK（2/2）、抗 EGFR Ctx（2/2 SPR）——**多个 2–6 样本的末级验证都在 80–100%**，把这几件事加总（约 15 投 13 中 ≈ 87%）就得到"接近九成"的印象值；这很可能就是讲座"90% 以上"的实证底色，但**没有任何一篇论文做过这种汇总声明**。
5. 注意区分口径：周组公开工作几乎全是**以已知结合骨架（SELEX 适配体/天然抗原肽/抗体 CDR）为起点的计算亲和力成熟/理性突变设计**，不是 Baker 式"10⁴–10⁵ 骨架库 de novo binder 设计后测 20–50%"的口径。若讲座说的是"de novo 设计成功率 90%"，在公开文献中**既无数字也无对应实验体量**；90% 只能成立于"送合成的最后 2–7 个候选"这种漏斗末端的定义。

**要定论需要什么证据**：周组（或其浙大/公司合作方的非公开管线）一次设计 campaign 的完整账目——候选池→MD/FEP 精筛→合成 M 条→阳性 N 条的 N/M 原始记录（讲座幻灯片数据页、实验室内部报告或专利实施例），或期刊论文中出现自报的汇总成功率。目前公开材料不具备。

## 五、未能核实的问题清单

1. CAAMO/NEOM 各论文的**共同通讯作者归属**（eLife XML 未含 AuthorNotes；按惯例末位 Zhou R 与 Huang L 推断，未证实）。
2. 付费全文细节：Z06（anti-EGFR）FEP 具体窗口时长与阈值、Z08 各方法相关系数数值、Z10 Deep-CovBoost 是否真有湿实验、Z13 实验验证方式（SPR/BLI）与 5/5 的分母定义。
3. "90%"讲座数字若来自**未发表/商业管线**（周如鸿挂名或合作的企业项目），公开网络不可达，无法排除。
4. 周组**专利**（Zhou 名下 30+ 国际专利，含 EP23 相关）中是否记载更高送检成功率——需 USPTO/智慧芽逐件核对，未在本次完成。
5. 周如鸿是否有 Baker 式**全 de novo 大蛋白骨架设计 + 实验闭环**论文：多轮关键词（Rosetta / RFdiffusion / scaffolding / miniprotein / 曹龙兴 / 卢培龙）交叉检索均无——**现存证据只支持"基于物理的亲和力成熟与小库设计"**；此点与讲座措辞的落差本身值得向讲者确认。
6. SARS-CoV-2 spike 方向：周组公开工作为 RBD 适配体（Z01）与糖基化/受体机制类纯模拟研究；未发现周组"设计结合蛋白中和 SARS-CoV-2"的论文（该叙事在媒体上多归属 Baker 组 miniprotein，曹龙兴一作 Science 2020——再次确认周、曹无合著）。
7. MD 轨迹聚类/水介导界面分析等是否设过显式数值阈值：全文中只见 RMSD、BSA、接触概率（末 100 ns）等描述性判据，**无"ΔG < 某固定值即送合成"的全局阈值**——准入判据始终是"相对亲代 ΔΔG<0 + 结构机理可解释"。

> **引用预算截短（2026-11-08，公开仓库口径）**：本底稿有 2 条逐字引句被截短（来源编号：Z04、Z12；许可类别：CC_BY_NC_ND、UNKNOWN），按 `deliverables/protein_design_license_audit.csv` 的逐份许可判定，单条引句截到 ≤100 字符；其中 1 条截短后仍**逐字命中同一份来源全文**，其余 1 条为**原句的前缀**（本地无全文或原句是我们自己的转写，只减不增、不新增第三方内容）。逐条改动账见 `deliverables/quote_budget_notes_ledger.csv`。
