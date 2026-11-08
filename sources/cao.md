# 曹龙兴（西湖大学/Baker 组）：设计筛选漏斗与实验命中率（调研于 2026-10-16）

> **成功测试（开工前定义）**：本文件收录 ≥10 篇曹龙兴 de novo 蛋白设计论文卡片；每个 DOI/PMID/PMCID 均由 Crossref API、Europe PMC REST、PubMed E-utilities 或 bioRxiv 全文页**实际调用核验**（标题+作者序列+期刊年份一致），命中率数字必须来自读到的原文短句并附 URL；与周如鸿（Ruhong Zhou）的合著关系用 ≥5 条查询串实证给出"有/无"结论。→ 结论见 §〇 与 §二。
> **证据等级说明**：标注 ✅全文 = 读到论文正文原句；⚠️仅摘要级 = 只有摘要/预印本摘要；⛔二级来源 = 中文科普/新闻稿转述，未核对到论文正文（Science/Nat Chem/Nat BME 三篇无开放获取全文）。
> 本文所有 DOI 均来自 API 返回，未使用记忆推断；作者位次来自 Crossref `author` 字段（1-based）。

---

## 〇、身份与合作关系核查

**身份（✅ 官方主页 + 会议简介互证）**
- 曹龙兴，1990 年生，山东巨野。2008–2012 山东大学生命科学学院学士；2012–2017 **中国科学院分子细胞科学卓越创新中心（原上海生物化学与细胞生物学研究所，SIBCB）**博士，做细胞表面受体的冷冻电镜结构；2017–2021 **华盛顿大学蛋白质设计研究所（IPD, Univ. of Washington）**博士后（David Baker）；2021-08 起西湖大学生命科学学院研究员/助理教授（独立 PI），并挂名"西湖人工智能药物设计核心实验室"（AI Drug Design Core Lab）。
  - 来源：https://www.westlake.edu.cn/faculty/longxing-cao.html （"2012-2017 年在中国科学院生物化学与细胞生物学研究所攻读博士学位…2017-2021 年在华盛顿大学蛋白质设计研究所进行博士后研究…2021 年 8 月全职加入西湖大学"）
  - 博士期间论文的单位行（Europe PMC core 记录，PMID 31116791 / 29079480）："State Key Laboratory of Molecular Biology, National Center for Protein Science Shanghai,"。
  - **博士导师（推断，非官方声明）**：其博士期两篇一作/共一论文末位作者均为 **He Y（何永盛）**：Cao L\*, Yu B\*, …, Baker D, **He Y**. PLoS Pathog 2019（✅ 10.1371/journal.ppat.1007759）；Dong Y\*, **Cao L\***, Tang H, Shi X, **He Y**. J Mol Biol 2017（⚠️仅摘要级，10.1016/j.jmb.2017.10.019）。信心：中高（仅凭作者位次推断，未见官方"师从"表述）。
  - **曹龙兴 ORCID = 0000-0003-4002-3648**（来源：Crossref `https://api.crossref.org/works/10.1126/science.ady6017` 的 author.ORCID 字段，已核对与 Science 2026 作者列表匹配）。

**与周如鸿（Ruhong Zhou，浙江大学）是否存在合著论文 —— 结论：未发现任何合著记录（实证）。**
| # | 查询串（实际执行） | 端点 | 返回条数 |
|---|---|---|---|
| 1 | `db=pubmed&term=Cao Longxing[Author] AND Zhou Ruhong[Author]` | PubMed E-utilities esearch | **count = 0**（`warninglist.outputmessages: "No items found."`） |
| 2 | `"Longxing Cao" AND "Ruhong Zhou"` | Europe PMC /search (resultType=core) | **hitCount = 0** |
| 3 | `AUTH:"Longxing Cao" AND AUTH:"Ruhong Zhou"` | Europe PMC | **hitCount = 0** |
| 4 | `AUTH:"Longxing Cao" AND AUTH:"Zhou Ruhong"` / `AUTH:"Cao Longxing" AND AUTH:"Zhou Ruhong"` | Europe PMC | **hitCount = 0** / **0** |
| 5 | `AUTH_ID:"0000-0003-4002-3648" AND AUTH:"Ruhong Zhou"` | Europe PMC | **hitCount = 0** |
| 6 | `AUTH:"Longxing Cao"`（全量翻页取回 69 条，逐条取 authorList） | Europe PMC | 69 条；其中作者串含任何 "Zhou" 的仅 5 条，合作者分别为 **Zhou Q / Zhou X / Zhou T / Zhou F**，**无一条为 Zhou Ruhong** |

即：曹龙兴的 69 条 Europe PMC 记录（含 20 条预印本）里没有周如鸿；曹也从未在浙江大学挂单位（其论文单位为 SIBCB/CAS → University of Washington → Westlake University）。**"曹龙兴曾在浙大/周如鸿组读博"的说法不成立**；读博单位是中科院分子细胞科学卓越创新中心。两人唯一的公开交集是同一学术会议的同一分会场（中国生物化学与分子生物学会 2026 全国学术大会"专题5 生物大分子设计"，召集人周丛照、卢培龙；曹龙兴为受邀报告人，https://m.sohu.com/a/1087439116_121119508/）——会议同场 ≠ 合作。

**"90%+ 设计成功率"的核查结果**：在曹龙兴 2019–2026 全部可获取的正文/预印本中，**没有出现任何 "90%"/"100%" 口径的设计成功率声明**（对 24 份全文做 `9[0-9]%|100%` 扫描，命中的只有"序列 100% 一致"、"溶出率/回收率"、"90% 抑制率阈值"等，见 §五）。最接近的高比例数字是**漏斗末端的小样本集**：HalluDesign 预印本 13/16 = 81.3%（de novo FGFR2 binder）、12/16 = 75%（PD-L1 拯救实验），IMUSE 预印本 16/28 = 57%（已判定活性候选中具可测动力学者）。口径差异是"90%+"传闻的关键：**"送合成的最后 16 个候选"的命中率 ≠ 整条管线的设计成功率**（后者在其正文中为 0.04%–5%）。

---

## 一、逐篇文献卡片

### [C01] De novo design of picomolar SARS-CoV-2 miniprotein inhibitors
- 作者/单位/角色：**Cao L 为第一作者**（15 人中的第 1 位；末位 Baker D）；University of Washington, Institute for Protein Design + Seattle Children's + Univ. of Wisconsin。**博后期间（2020）**。
- 期刊, 年: **Science 370:426–431, 2020** | DOI: **10.1126/science.abd9909** ✅(Crossref+PubMed) | PMID 32907861 / PMCID PMC7857403（CC-BY 开放获取）/ 预印本 bioRxiv 10.1101/2020.08.03.234914 | 链接 https://www.science.org/doi/10.1126/science.abd9909
- 设计对象: SARS-CoV-2 Spike RBD 的结合蛋白（LCB/AHB 系列 minibinder，56–65 残基）。
- 候选生成: 两条路线 —（1）把 ACE2 结合螺旋嵌入设计骨架（approach 1）；（2）**RIF（rotamer interaction field）docking** 大规模对接自有 miniprotein 骨架库 + Rosetta 序列设计（approach 2）。
- 计算筛选器: Rosetta ddG / 打包与形状互补指标；骨架库本身来自"结构度量可预测折叠"的预筛（承 C05 的 84,690 条骨架库）。原文未给单一数字阈值（阈值体系见 C04）。
- MD 使用: **未使用**。 QM 使用: **未使用**。
- 实验验证方法与通量: **酵母表面展示 + FACS 多轮分选 + 深度测序（NGS）**；随后 E. coli 表达、BLI（Octet）、CD 热熔、cryo-EM、活病毒中和（Vero E6, FFU 空斑）。
- **命中率原始数字（✅全文，https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7857403/fullTextXML）**：
  - "Deep sequencing identified **three** ACE2 helix scaffolded designs ("approach 1"), and **105** de novo interface designs ("approach 2") that were enriched after fluorescence-activated cell sorting (FACS) for RBD binding."
  - "All three ACE2-scaffolded designs and **12 of the de novo designs** were expressed in Escherichia coli and purified." → 表达 12/105 = **11.4%**
  - "One of the ACE2-scaffolded designs and **11 of the 12 de novo designs were soluble and bound RBD** with affinities ranging from 100 nM to 2 μM in biolayer interferometry" → 结合率 **11/12 = 91.7%（表达后）**，绝对值 **11/105 = 10.5%**
  - "For **50** of the minibinders made by using approach 2 … we generated site saturation mutagenesis libraries (SSMs)"；"residues at the binding interface and protein core were largely conserved for **40 out of the 50** approach 2 minibinders"
  - 摘要级："**Ten designs bound the RBD, with affinities ranging from 100 picomolar to 10 nanomolar**, and blocked SARS-CoV-2 infection of Vero E6 cells with median inhibitory concentration (IC50) values between 24 picomolar and 35 nanomolar."；LCB1/LCB3 中和 IC50 = 23.54 / 48.1 pM（"as low as 11 pM"）。
  - 结构验证："backbone Cα root mean square deviation of **1.27 and 1.9 Å** for LCB1 and LCB3"（cryo-EM vs 设计模型）。
- 演进链位置: 物理打分（Rosetta/RIF）时代的天花板；其结论"主要瓶颈不在设计形状/化学互补的界面，而在**识别最好的候选**（recognizing the best candidates）"直接驱动了他后来做生成模型与预筛判据。

### [C02] Design of protein-binding proteins from the target structure alone
- 作者/单位/角色：**Cao L 为第一作者**（35 人中第 1；末位 Baker D，含 Garcia K.C.）。**博后期间完成，2022 年发表**；预印本 Cao L, Coventry B, Goreshnik I, Huang B, Park JS, Jude KM, et al. "Robust de novo design of protein binding proteins from target structural information alone", bioRxiv 2021, **10.1101/2021.09.04.459002**（✅ EPMC PPR391052）。
- 期刊, 年: **Nature 605(7910):551–560, 2022**（卷期页码经 Europe PMC core 记录核验） | DOI: **10.1038/s41586-022-04654-9** ✅ | PMID 35332283 / PMCID PMC9117152 | https://www.nature.com/articles/s41586-022-04654-9
- 设计对象: 12 个天然蛋白的 **13–14 个表位**（HA/H3、EGFR(D1、DIII)、PDGFR、IR、IGF1R、TIE2、IL-7Rα、CD3δ、TGFβ、VirB8、TrkA、FGFR2），50–65 残基 minibinder。
- 候选生成: PatchDock → **RifDock**（RIF 哈希）→ 重采样 → Rosetta FastDesign；骨架来自 84,690 条预筛 miniprotein 库。
- 计算筛选器（名字+阈值数字，✅全文）:
  - "CPU time requirements to produce **100,000** designed binders to be tested experimentally were typically around **100,000 CPU hours** (usually **at least ten times as many binders were computationally designed than were ordered**)." → 计算设计：送测序列 ≈ **10:1** 漏斗
  - 判据集合："Computational metrics of the final design models were calculated using Rosetta, which includes **ddG, shape complementarity and interface buried SASA, contact molecular surface**, among others, for design selection."
  - 预筛器 "the Predictor"：为消除对接与全设计之间的"速度严重失配"（"A severe speed mismatch existed between the docking methods … and the subsequent full sequence design step"），用**只含疏水氨基酸、简化能量函数**的 Rosetta 快速打包评估，"sped up the design time by **more than tenfold** while retaining a strong correlation with results after full sequence design"；对每个 filter 设 goal threshold，再用 sigmoid 拟合"通过该 filter 的概率"（"the probability that each predicted design passes each filter can be calculated (sigmoids are fitted to smooth the distribution)"）。
  - 聚类阈值："Those motifs within a threshold similar score (**default of 0.7**) from the current cluster centre were removed…"
  - 聚类后按 per-position weighted Rosetta binding energy 取每个簇最优 motif。
- MD 使用: **未使用**。 QM 使用: **未使用**。
- 实验验证方法与通量: 酵母展示文库 + 多轮 FACS（先 with-avidity 后 without-avidity）+ **NGS 定量 SC50**（"the midpoint concentration (SC50) in the binding transitions for each design in the library"）；组合突变库（SSM → 点突变组合）做亲和力成熟；E. coli 表达、BLI、CD、X 射线/cryo-EM。文库分选时"collecting only the **top 0.1%** of the binding population"。
- **命中率原始数字（✅全文，https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9117152/fullTextXML）**：
  - "Using the above protocol, **we designed 15,000–100,000 binders for each of the 13 target sites** on the 12 native proteins"
  - "**For some (FGFR2 and PDGFR), hundreds of binders were generated, whereas for others (TIE2 and CD3δ), fewer than 10 binders were obtained from libraries of 100,000 designs**（Extended Data Table 1）." → 单靶点实验命中率 **<0.01%（TIE2/CD3δ）到 ~0.3%（数百/100,000）**
  - "**Design success rates varied considerably between the different targets.**"；"**Only a small fraction of designs bind**, and in almost all cases, the best of these require additional substitutions to achieve high-affinity binding."
  - 数据集规模："the large dataset (**810,000 binder designs and 240,000 single mutants**) generated in this study"
  - 骨架库层面："A total of **84,690** scaffolds spanning 5 different topologies … were encoded in large oligonucleotide arrays, and **34,507** of these were found to be stable using a high-throughput proteolysis-based protein stability assay." → 骨架折叠率 **40.7%**
  - 结构准确度："Nine out of the 13 designs retained more than half of the mean residue ellipticity values, which indicated that the Tm values are **greater than 95 °C**."；LCB1/LCB3 cryo-EM vs 设计"Cα r.m.s.d."接近原子级。
  - 侧链精度的物理上限（原文对"设计-结合"概率的估计）："if the Cα RMSD of the displayed sidechains deviates from the known-good conformation by **0.5 Å**, that there would be a **15% chance of binding** due to the intrinsic accuracy of sidechains required for binding."
- 演进链位置: 这是他"只用靶结构、不需热点先验"的 binder 通用方法（后来他西湖组所有 binder 工作、以及 CAR-T/降解子应用都建立在这条 RIF+Rosetta 管线之上）；同时暴露了物理打分时代的核心局限 → 转向深度学习生成（C15–C17）。

### [C03] De novo design of modular and tunable protein biosensors
- 作者/单位/角色: Quijano-Rubio A¹, Yeh HW, Park J, Lee H, Langan RA, Boyken SE, Lajoie MJ, **Cao L（第 8 位）**, Chow CM, …, Oh BH, Baker D（末位）。**博后期间（2021）**，UW-IPD + 首尔国立大学。
- 期刊, 年: **Nature 591(7850):482–487, 2021** | DOI: **10.1038/s41586-021-03258-z** ✅ | PMID 33503651 / PMCID PMC8074680 | 预印本 10.1101/2020.07.18.206946（✅ EPMC PPR189983）
- 设计对象: 别构蛋白开关/lucKey–lucCage–latch 体系（生物素、BCL-2、IgG1-Fc、HER2、BoNT B、cTnI、HBV、SARS-CoV-2 RBD/S/M/N）。
- 候选生成: DHR 骨架（lucCage/lucKey）+ Rosetta 界面设计 + 热力学耦合模型（ΔG_open、ΔG_CK、ΔG_LT）。
- 计算筛选器: 以**自由能不等式**作为设计判据（✅全文）："the binding free energy of lucKey to lucCage (ΔG_CK) is insufficient to overcome the free energy"。无 pLDDT/ipTM 类阈值（早于该体系）。
- MD 使用: 未见（⛔全文检索无 MD 关键词）。 QM 使用: 未见。
- 实验验证: BLI（OTK 生物传感器层）、发光重建读数（solution readout）、酵母展示 E. coli 表达。
- **命中率原始数字（✅全文，NCBI PMC efetch db=pmc&id=8074680）**：
  - "**Of 13 candidates tested**, the best, which we refer to as lucCageRBD,"
  - "**The best of 8 designs tested**,"
  - 即"每类 8–13 个候选中取最优"的漏斗末端口径；未给整库命中率。
- 演进链位置: 从"静态结合"转向"**多态/可切换**"体系的关键一步；西湖组的光控（C16）、小分子调控寡聚体（C17）与配体诱导折叠/重组传感器（C23）都是这条线。

### [C04] Ultrapotent miniproteins targeting the SARS-CoV-2 receptor-binding domain protect against infection and disease
- 作者/单位/角色: Case JB, Chen RE, **Cao L（第 3 位）**, Ying B, Winkler ES, …, Baker D, Diamond MS。**博后期间（2021）**。
- 期刊, 年: **Cell Host & Microbe 29(7):1151–1161.e5, 2021** | DOI: **10.1016/j.chom.2021.06.008** ✅ | PMID 34192518 / PMCID PMC8221914 | 预印本 10.1101/2021.03.01.433110（✅ PPR290232）
- 设计对象: LCB1–LCB3 及 LCB1-Fc 融合体（RBD 中和）。
- 候选生成/筛选器: 同 C01（RIF docking + Rosetta），加上 Fc 融合改善 avidity。
- MD/QM: 均未使用（⛔全文无相关关键词）。
- 实验验证: 假病毒/活病毒中和、小鼠感染模型（非转基因 129S2 N501Y 适应株）、BLI、结构。
- **命中率原始数字（✅全文）**: 设计侧无新漏斗数字（继承 C01 的 105→12→11），主要贡献是体内效力："we tested the efficacy of LCB1-Fc in a non-transgenic 129S2 mouse model of SARS-CoV-2 infection…"。
- 演进链位置: 从"计算命中"走到"体内有效"，是 binder 平台的转化验证。

### [C05] Large-scale design and refinement of stable proteins using sequence-only models
- 作者/单位/角色: Singer JM, Novotney S, Strickland D, Haddox HK, Leiby N, Rocklin GJ, Chow CM, Roy A, Bera AK, Motta FC, **Cao L（第 11 位）**, Strauch EM, …, Baker D, Klavins E（24 人）。
- 期刊, 年: **PLOS ONE 17(3):e0265020, 2022** | DOI: **10.1371/journal.pone.0265020** ✅ | PMID 35286324 / PMCID PMC8920274 | 预印本 10.1101/2021.03.12.435185（✅ PPR296827）
- 设计对象: 大规模 mini-protein 稳定性库（Rosetta / dTERMen 设计）。
- 计算筛选器: **仅用序列**的卷积模型（sequence-only "EM" 模型）预测折叠/稳定，用于给设计打分。
- MD 使用: 未使用。 QM 使用: 仅 "Ab initio Rosetta predictions"（Rosetta 能量，非量子化学）。
- 实验验证方法与通量: **酵母展示蛋白酶解滴定 + FACS + NGS 的稳定性的高通过量检测**（Corpus A/B/C，BIOFAB 微流控辅助）。
- **命中率原始数字（✅全文，https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8920274/fullTextXML）**：
  - "We used this combination of the existing assay and software-based automation to evaluate the stability of **up to 100,000 proteins in a single experiment**."
  - "This model was trained on a corpus of **107,948 proteins** ("Corpus A") designed by experts using Rosetta or dTERMen software"
  - "We selected **1000 GM designs** with the highest agreement between the input secondary structure and the Reverse GM's predicted secondary structure … These 1000 designs were assayed for stability as part of Corpus B."
  - "Of the **993 designs that expressed at a detectable level**, **275** had a maximum identity less than 95% and **47 of these 275 (17%)** had an empirical stability score greater than 1.0 (classified as "stable")."
  - "guided substitutions increased stability score **4138 out of 5850 times (70.7%)**"；"Random substitutions … decreased stability score **2731 out of 4798 times (56.9%)**"
  - dTERMen 对照组："**less than 1% of designs** achieved stability scores greater than 1."
- 演进链位置: 建立"**便宜的通量代替昂贵的判定**"的方法论底座；他后续所有 binder 工作的骨架可折叠性预筛都靠这套 assay（见 C02 的 34,507/84,690）。

### [C06] Multivalent designed proteins neutralize SARS-CoV-2 variants of concern and confer protection against infection
- 作者/单位/角色: Hunt AC, Case JB, Park Y, **Cao L（第 4 位）**, Wu K, Walls AC, …, Veesler D, Jewett MC, Baker D（47 人）。**博后末期/西湖初（2022）**。
- 期刊, 年: **Science Translational Medicine 14(646):eabn1252, 2022** | DOI: **10.1126/scitranslmed.abn1252** ✅ | PMID 35412328 / PMCID PMC9258422 | 预印本 10.1101/2021.07.07.451375（✅ PPR366958）
- 设计对象: LCB 系列 minibinder 的二价/三价组装（MON/FUS/TRI 系列）+ BRET 传感器。
- 候选生成: 连接子长度 × 寡聚化结构域的组合设计（LCB1/2/3 组合）。
- 计算筛选器: 界面 Rosetta 指标 + 结合态几何（"the distances between the termini of the domains when bound to the "open" and "closed" states of the RBD"）→ 以几何约束确定 linker 长度范围。
- MD/QM: 均未使用。
- 实验验证方法与通量: **无细胞表达（CFPS）+ 发光/结合读数的高通量初筛**，再 E. coli/昆虫细胞表达、BLI/SPR、假病毒与活病毒中和、escape 突变、肾类器官。
- **命中率原始数字（✅全文，https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9258422/fullTextXML）**：
  - "**We designed and screened more than 100 different homotrimeric minibinders**, with varied linker lengths and homotrimerization domains, **using the CFPS workflow**."
  - "**We screened more than 100 different fusions using the CFPS workflow**, evaluating different minibinder orderings and a range of linker compositions and lengths…"
  - "**In total, we tested eleven different oligomerization domains and found that nine of these domains yielded at least one design with a linker length that improved dissociation rates** on par with the top binders." → **9/11 = 81.8%（按结构域层面）**
  - "This is a marked improvement, **more than four orders of magnitude for the TRI2 proteins**, over the dissociation rate constants of the corresponding monomeric minibinders"；"the TRI2 proteins potently neutralized the B.1.1.529 variant whereas many clinical mAbs … do not"。
- 演进链位置: 展示"**多价化 = 用组装换亲和力**"的补救策略，等于给低命中率的一价设计提供第二级筛选/放大通道。

### [C07] Isoform-specific inhibition of FGFR signaling achieved by a de-novo-designed mini-protein
- 作者/单位/角色: Park JS, Choi J, **Cao L（第 3 位）**, Mohanty J, …, Schlessinger J, Lee S（9 人）。
- 期刊, 年: **Cell Reports 41(4):111545, 2022** | DOI: **10.1016/j.celrep.2022.111545** ✅ | PMID 36288716
- 设计对象: FGFR4-D3 的 minibinder mb7（源自 C02 管线），改造出对 FGFR **c-IIIc/c-IVc 异构体**的选择性。
- 候选生成: C02 的 RIF/Rosetta 设计 + 基于共晶结构的理性点突变（"we designed a variant of mb7 that contains two amino acid substitutions, **K48T/K49H** (mb7TH)"）。
- 计算筛选器: 晶体结构界面分析 + Rosetta 突变效应评估（同 C02 的 ddG/CMS 体系）。
- MD/QM: 均未使用。
- 实验验证: 蛋白纯化、BLI/SPR 动力学（Table S1）、细胞信号、结晶（Cα RMSD 0.924 Å）。
- **命中率原始数字（⛔仅摘要+方法级；正文给出的定量内容为亲和力/动力学而非漏斗计数）**: "Overall structures of FGFR4 D3:mb7 complex crystallized in these two conditions are similar to each other, with **Cα RMSD of 0.924 Å**."
- 演进链位置: 说明"设计命中后如何用**极小成本的两点突变**换取异构体选择性"——设计-再造循环。

### [C08] De novo design of luciferases using deep learning
- 作者/单位/角色: Yeh AHW, Norn C, Kipnis Y, Tischer D, …, **Cao L（第 12 位）**, …, Houk KN（K. N. Houk，量子化学家）, Baker D（18 人）。**西湖PI 身份时期的 Baker 组合作**。
- 期刊, 年: **Nature 614(7949):774–780, 2023** | DOI: **10.1038/s41586-023-05696-3** ✅ | PMID 36813896 / PMCID PMC9946828
- 设计对象: 催化二苯基噁哒嗪（DTZ）/h-CTZ 氧化化学发光的**全新荧光素酶（酶）**：LuxSit（117 残基, 13.9 kDa）、LuxSit-i、HTZ3-D2/G4。
- 候选生成: **"family-wide hallucination"**（trRosetta 幻觉 + MCMC 序列-结构采样，生成 NTF2-like 超家族理想化骨架 **1,615 条**）→ RIF  docking 配体 → PSSM-biased Rosetta 序列设计。
- 计算筛选器（✅原文）: "After sequence optimization, the designs were filtered on the basis of **ligand-binding energy, protein–ligand hydrogen bonds, shape complementarity and contact molecular surface**, and **7,648 designs were selected and ordered** as pooled oligos for experimental screening."；第二轮"we created an additional set of NTF2 superfamily scaffolds with matching pocket shapes and high model confidence (**AlphaFold2-predicted pLDDT > 92**)"；"After filtering on the basis of the **AlphaFold2-predicted pLDDT, Cα RMSD, contact molecular surface and Rosetta-computed binding energies**, we selected and experimentally expressed **46 designs** in E. coli"。
- **MD 使用: ✅明确使用** — "We used a combination of **density functional theory (DFT) calculations and molecular dynamics (MD) simulations** to investigate the basis for LuxSit activity…"；"the distances between His98 to O1 … and Arg65 to N1 … of the substrate were plotted throughout **500 ns MD simulations**"；图题"**Free-energy profile of DTZ chemiluminescence and MD simulations** of proposed protein–intermediate complexes"；"50-fold selectivity for DTZ over bis-CTZ … **MD simulations suggest** that this arises from greater transition-state shape complementarity"。
- **QM 使用: ✅明确使用** — "**Both quantum chemistry calculations and experimental data suggest** that the chemiluminescent reaction proceeds through an **anionic species** …"；"**Density functional theory (DFT) calculation suggested** that the formation of an anionic state is the essential electron source for the activation of triplet oxygen (³O₂)"（Houk 组参与）。
- 实验验证方法与通量: **寡核苷酸池组装基因 + E. coli 96 孔表达 + 菌落水平化学发光成像直接筛活**（"A colony-based screening method was used to directly image active luciferase colonies from the library"）；随后位点饱和突变库（SSM）活性图谱、CD、cryo-EM/晶体学。
- **命中率原始数字（✅全文，https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9946828/fullTextXML）**：
  - 第一轮："**Three active designs were identified**; we refer to the most active of these as LuxSit" → **3 / 7,648 = 0.039%**
  - 第二轮："identified **2** (HTZ3-D2 and HTZ3-G4) that had luciferase activity with the h-CTZ luciferin substrate" → **2 / 46 = 4.3%**
  - 原文自述漏斗对比："**The success rate increased from 3/7,648 to 2/46 sequences in the second round**, probably owing to the knowledge of active-site geometry from the first round and the increased robustness of the **ProteinMPNN** method of sequence design."
  - 催化效率："k_cat/K_m = 10⁶ M⁻¹ s⁻¹"；"a melting temperature higher than 95 °C"。
- 演进链位置: **酶设计 = 他工作中唯一有 MD+QM 闭环的类别**（QM 定过渡态/阴离子机理，MD 验证活性位点动力学与选择性）；同时给出"从 0.04% 到 4.3%"的量化迭代收益，是他反复强调"迭代设计-构建-测试"的实证。

### [C09] Top-down design of protein architectures with reinforcement learning
- 作者/单位/角色: Lutz ID, Wang S, Norn C, Courbet A, …, **Cao L（第 8 位）**, …, Ruohola-Baker H, Baker D（20 人）。
- 期刊, 年: **Science 380(6642):266–273, 2023** | DOI: **10.1126/science.adf6591** ✅ | PMID 37079676 | 预印本 10.1101/2022.09.25.509419（✅ PPR550401）
- 设计对象: 用 RL 从"自上而下"设计大尺度蛋白组装体/拓扑（Corona-like 库扩展）。
- 计算筛选器: RL reward 内置可设计性/几何度量（⚠️仅摘要级证据；正文未获取）。
- MD/QM: 未见证据（⚠️仅摘要级）。
- 实验验证: 高通量酵母展示稳定性/结合读数（同 C05 体系）（⚠️摘要级）。
- **命中率原始数字**: ⚠️仅摘要级——正文未开放，未提取到计数；不编造。
- 演进链位置: 生成模型从"骨架库检索"进入"强化学习/参数化生成"，为他自研 Proteus（C16）铺路。

### [C10] Modulation of FGF pathway signaling and vascular differentiation using designed oligomeric assemblies
- 作者/单位/角色: Edman NI, Phal A, Redler RL, Schlichthaerle T, …, **Cao L（第 20 位 / 40 人）**, …, Ruohola-Baker H, Baker D。
- 期刊, 年: **Cell 187(14):3726–3740.e43, 2024** | DOI: **10.1016/j.cell.2024.05.025** ✅ | PMID 38861993 | 预印本 10.1101/2023.03.14.532666（✅ PPR630731）
- 设计对象: **大蛋白/高阶寡聚体**（C4–C8 星形组装体，DHR 重复蛋白模块 + FGFR 结合模块 mb），用于价态/几何依赖的信号调控与人-小鼠血管共培养。
- 候选生成: DHR 重复单元模块化扩展 → 对称对接（C4–C8），另一套用 1526 条 **5HCS**（5-螺旋凹面）库做 C2 对接。
- 计算筛选器（✅全文，NCBI PMC efetch db=pmc&id=11246234）: "**ΔΔG < 0**（favorable）、**shape complementarity sc > 0.65**、界面**未满足氢键 < 2 个**"。
- MD/QM: 均未使用（全文无 MD/QM 关键词）。
- 实验验证方法与通量: 合成基因 → E. coli 表达 → IMAC → **SEC 单分散判定 → SAXS + SEC-MALS 判定正确寡聚态 → cryo-EM/SPr、细胞与类器官功能**。
- **命中率原始数字（✅全文，逐级）**：
  - "A total of **109 designs** were selected for structural characterization: 15 tetramers, 16 pentamers, 24 hexamers, 24 heptamers, and 30 octamers."
  - "Design characterization: Synthetic genes encoding the 109 designs of symmetry C4 or higher were synthesized, expressed as protein in Escherichia coli, and purified…"
  - "**Of the 60 designs that were soluble, 28 had single monodisperse peaks on size exclusion chromatography (SEC).** **Of these, ten designs were found to have a single oligomeric state by both SAXS and SEC-MALS.**"
    → **可表达/可溶 60/109 = 55.0%**；**单分散 28/60 = 46.7%（占投测 25.7%）**；**正确组装 10/109 = 9.2%**
  - 另一路径："from **3747 C2 oligomers**, **14 designs** were selected for further analysis … **From the 14 C2 designs, three (C2-58, C2-CDX, C2-Y2D)** had soluble expression, were confirmed as a monodisperse peak on SEC and had a correctly assembled oligomeric state" → **3/14 = 21.4%**
  - 结构偏差："Both the C6-79 and C8-71 cryo-EM models align well with the corresponding design models, with pairwise **RMSDs of 2.85 Å and 1.79 Å**"；"the highest success rate was achieved with the DHR71 building block … design model was closer to the crystal structure (**0.67 Å RMSD**)"。
- 演进链位置: 他参与的"**大蛋白/高级结构从头设计**"代表作——瓶颈从"会不会折"变成"**装配对不对（价态、几何）**"，判据因此增加 SAXS/SEC-MALS 这类低通量但一锤定音的物理测量。

### [C11] Designed endocytosis-inducing proteins degrade targets and amplify signals（DICE）
- 作者/单位/角色: Huang B, Abedi M, Ahn G, Coventry B, …, **Cao L（第 36 位 / 45 人）**, …, Roybal KT, Bernardes GJL, Bertozzi CR, Baker D。
- 期刊, 年: **Nature 638(8051):796–804**（2024-09-25 在线，正式卷期 2025-02；Europe PMC 记为 2025） | DOI: **10.1038/s41586-024-07948-2** ✅ | PMID 39322662 / PMCID PMC11839401 | 预印本 10.1101/2023.08.19.553321（✅ PPR705400）
- 设计对象: 诱导内吞/降解膜蛋白并放大信号的合成受体（Sortilin→PD-L1、IgG、B7-H3 等），"EndoTag"系列。
- 候选生成: Rosetta binder 设计（承 C02）+ **MotifGraft** 嫁接 + **ProteinMPNN** 序列生成 + 重新采样。
- 计算筛选器（✅全文，名字+阈值）：
  - "21,000 binders were generated to each of 2 sites on the sortilin"（初筛规模）；"**Helical motifs were extracted, and 3,000 designs were selected**, grafted and subjected to further design."
  - "**After 2,000 sequences were generated for each ProteinMPNN input**, designs were filtered by predicted Rosetta ddG."
  - "**Designs with ddG metrics less than −40 and spatial aggregation propensity scores less than 35** were selected for expression and experimental assays."
  - "**Designs with pae_interaction < 10 and relaxed_ddG < −40** were selected for resampling with another round of protein-MPNN prediction followed by Rosetta Fastrelax."
  - "**The designs with poor monomer plddt (plddt < 85) were dropped.**"；最终"filtered with exposed hydrophobicity (sap_score) and optimized with a **net-charge of −7**"；"filtered based on geometrical restraints, **CST-score < 5**"。
- MD/QM: 均未使用（全文无 MD/QM 证据）。
- 实验验证: E. coli/昆虫细胞表达、BLI、流式内吞/降解读数、Jurkat、小鼠药代与肿瘤模型、质谱（FDR < 1%）。
- **命中率原始数字（✅全文）**：
  - "**We tested 170 designs** for which AlphaFold2 predictions matched the intended structures for binding to both IGF2R domains, and **expressed eight designs that interacted with both domains in E. coli**" → **8/170 = 4.7%**
  - 功能端："the highest affinity design (Sort_EndoTag) had a dissociation constant (K_D) for Sortilin of **21 nM**"；"**77% of the PD-L1** in the cells was eliminated after 48 h"；"**depletion of 70% of the IgG**"。
- 演进链位置: 阈值体系成型的标志——**ddG < −40 + SAP < 35 + pAE_int < 10 + pLDDT ≥ 85 + 净电荷 −7**，即"物理打分 + AF2 置信度"双闸；但送实验仍只拿到个位数百分比命中。

### [C12] Targeting overexpressed antigens in glioblastoma via CAR T cells with computationally designed high-affinity protein binders
- 作者/单位/角色: Xia Z, Jin Q, Long Z, He Y, Liu F, Sun C, Liao J, Wang C, Wang C, Zheng J, Zhao W, Zhang T, Rich JN, Zhang Y, **Cao L（第 15 位，通讯）**, **Xie Q（谢琦，末位通讯）**；单位含 Westlake Laboratory of Life Sciences and Biomedicine / 西湖大学。**独立 PI 时期（2024）**。
- 期刊, 年: **Nature Biomedical Engineering 8(12):1634–1650, 2024**（2024-10-17 在线）| DOI: **10.1038/s41551-024-01258-8** ✅（Crossref）| PMID 39420062；另有 Publisher Correction DOI **10.1038/s41551-024-01338-9** ✅ (PMID 39663402)
- 设计对象: 靶向 **EGFR** 与 **CD276(B7-H3)** 的高亲和力 de novo binder，作为 CAR 胞外域（DNDB-CAR）。
- 候选生成: 曹龙兴自建组的 binder 管线（RIF/Rosetta 系 + 深度学生成；⛔具体版本未从正文确认）。
- 计算筛选器: ⛔**未获得正文级证据**（无 OA 全文；仅摘要级）。
- MD/QM: 未见证据（⚠️仅摘要级）。
- 实验验证: T 细胞增殖/细胞因子/耗竭、体外与颅内移植瘤模型、bulk + **single-cell 转录组**（解释 CAR 表面表达与抗降解优势）；已启动 CD276 binder CAR-T 研究者发起临床（IIT）。
- **命中率原始数字**: ⚠️**仅摘要级**（摘要不含漏斗计数）。摘要原句（https://europepmc.org/article/MED/39420062）："…the designed binders on CAR T cells promoted the proliferation of the cells, the secretion of cytotoxic cytokines and their resistance to cell exhaustion, and improved antitumour performance in vitro and in vivo."
  - 二级来源（西湖实验室/谢琦组新闻，https://news.bioon.com/article/e5fd84e84488.html、https://new.qq.com/rain/a/20241101A013FS00）亦**未给设计→实验漏斗计数**，故此处不填数字，列为未核实项。
- 演进链位置: 他组**转化最深的一条**（进入 IIT）——筛选逻辑在此不再是"找结合"，而是"**结合 + CAR 表面表达 + 抗降解**"三个属性联合。

### [C13] Accurate de novo design of heterochiral protein–protein interactions
- 作者/单位/角色: Sun K, Li S, Zheng B, Zhu Y, …, **Cao L（第 14 位 / 17 人）**, Liu L, **Lu P（卢培龙，末位通讯）**。**西湖组间合作（2024）**。
- 期刊, 年: **Cell Research 34(12):846–858, 2024** | DOI: **10.1038/s41422-024-01014-2** ✅ | PMID 39143121 / PMCID PMC11614891
- 设计对象: 用 L 型蛋白设计 **D-蛋白**的结合物（及反向），靶 D-TrkA、D-IL-6、D-Pep-1。
- 候选生成: Rosetta 界面设计 + **MotifGraft** 采样（"more backbone geometries and interface compositions … were sampled by using the MotifGraft algorithm for optimal binding"）。
- 计算筛选器: 承 Baker 管线指标（⛔阈值数字未在该文正文出现）。
- MD/QM: 均未使用。
- 实验验证: 寡核苷酸池合成 → 酵母展示 → 多轮磁珠/FACS（BD Melody）→ NGS；化学合成 D-肽/D-蛋白、CD、MST、SPR、蛋白酶抗性与 TF-1/HEK 细胞功能。
- **命中率原始数字（✅全文）**：
  - "For the d-Pep-1 pool, after sorting against d-Pep-1 at concentrations of **100 nM and 10 nM**, we identified **140** and **11** diverse sequences, respectively."
  - "**Two binders were successfully identified** from these libraries, namely l-57445-evo d-TrkA and l-25367-evo d-IL-6."
  - "The d-protein binders were **hyper-stable** in the thermo-melting experiments: the CD spectra at 95 °C are very close to those at 25 °C"；"All l-protein binders were completely digested by trypsin or pepsin after 6 h … while all d-protein binders remained intact even after a 20-h incubation."
  - 分选群体阈值："with a population fraction larger than **0.05%** in the last round of selection"。
- 演进链位置: 显示其漏斗**对映体无关**（同一套 RIF/Rosetta + 酵母展示判据可用于镜像体系）。

### [C14] Design of high-affinity binders to immune modulating receptors for cancer immunotherapy
- 作者/单位/角色: Yang W, Hicks DR, Ghosh A, Schwartze TA, Coventry B, Goreshnik I, …, **Cao L（第 16 位 / 28 人）**, …, Hinck CS, Hinck AP, Baker D（末位通讯）。
- 期刊, 年: **Nature Communications 16(1):2001, 2025** | DOI: **10.1038/s41467-025-57192-z** ✅ | PMID 40011465 / PMCID PMC11865580 | 预印本 **10.1101/2024.05.01.592114**（✅ EPMC PPR847282，Baker D 列首位署名顺序为仓库记录所致）
- 设计对象: **TGFβRII、CTLA-4、PD-L1**（以**凸面**表位为主）的高亲和力结合蛋白，含六聚体 avidity 版本。
- 候选生成: 自建 **5HCS 凹面 5-螺旋支架库**（"The selected **7476** scaffolds, referred to as 5HCS (5 helix concave scaffolds), exhibit a wide range of curvatures"；<120 aa）+ RIF docking（引用 Cao et al. 即 C02）+ Rosetta 设计 → 虚拟优化 + 组合库。
- 计算筛选器（✅全文，阈值齐全）：
  - "**The designs were later filtered by ddG (less than −40), contact molecular surface (larger than 400), and pAE (less than 10)** from AlphaFold2 initial guess."
  - "**The designed scaffolds were later filtered by the AlphaFold2 with a mean pLDDT cutoff of 80** and **AccNet with a mean pLDDT cutoff of 0.**"（DeepAccNet 截断值；正文该句在 XML 中被截，数字以 0.x 表示）
  - "We evaluated the **curvatures** of the three interfacial helices and **filtered out those with convex surfaces**."（几何准入：支架必须凹）；"Docked poses of the 5HCS library were filtered by **binding orientation**."；"filtered by interfacial profiles, including the length of each partner's and **delta SASA**"；"RANSAC was used to fit spherical surfaces … **threshold of 1 Å**, max iteration 100k"（曲率量化）。
  - 组合库分选："The combinatorial libraries were enriched at a medium concentration of target for two rounds by collecting the **top 10%** of the binding population."
- MD/QM: 均未使用（全文无 MD/QM 关键词；界面描述为"reducing solvation-free energy"这类概念性表述，非计算）。
- 实验验证方法与通量: **oligo 池编码 → 酵母展示 → FACS 多轮 + NGS（SC50）** → 命中克隆 100% 序列一致确认 → E. coli 包涵体复性/SEC → BLI/ITC → 晶体学/共晶 → CTLA-4 封闭 Bioassay（Jurkat 报告基因）与 TGFβ 通路功能。
- **命中率原始数字（✅全文）**：
  - "**FACS of yeast libraries displaying the designs identified six CTLA-4 binders** which match the designs with 100% sequence identity."
  - "**Two PD-L1 binders were obtained from a set of 96 designs.**" → **2/96 = 2.1%（送测层面）**
  - 亲和力："achieving **low nanomolar to picomolar affinities** … following experimental optimization"；"5HCS_CTLA4_1 … is expressed at high levels, very stable and has an **affinity of 646 pM**"；CTLA-4 功能 "**EC50 of 53.3 nM**"。
  - 结构精度："The crystal structure of 5HCS_CTLA4_1 in complex with CTLA-4 closely agrees with the design model, with a **very low rmsd**"（正文数值）；5HCS_PDL1_1 同样"superimposes … with a rmsd of …"。
- 演进链位置: 解决"**凸面表位无形状互补**"瓶颈（用互补凹面支架代替 miniprotein），是他作为参与者的"Baker 免疫治疗 binder 库"代表作；漏斗仍是"96 投 2 中"级别。

### [C15] De novo design of light-responsive protein–protein interactions enables reversible formation of protein assemblies
- 作者/单位/角色: Yu B, Liu J, Cui Z, Wang C, Chen P, Wang C, Zhang Y, Zhu X, Zhang Z, Li S, Pan J, Xie M（解明岐）, Shen H, **Cao L（第 14 位 = 末位通讯）**。**独立 PI 时期（2025）**。
- 期刊, 年: **Nature Chemistry 17(12):1910–1919, 2025**（在线 2025-08-28） | DOI: **10.1038/s41557-025-01929-2** ✅ | PMID 40877575
- 设计对象: 光响应蛋白-蛋白相互作用——**非天然氨基酸苯基偶氮丙氨酸（AzoF）**调控的环状同源寡聚体与异源二聚体；光响应水凝胶；光控细胞信号受体。
- 候选生成: 含 AzoF 的界面建模 + 对称性约束设计（自研流程；⛔正文不可得）。
- 计算筛选器/阈值: ⛔**未获正文级证据**（无 OA 全文，摘要不含阈值）。
- MD/QM: ⚠️摘要级未见 MD；**AzoF 的光异构化（trans/cis）本质上是量子化学问题，但该文是否自算激发态（TD-DFT）无法核实** → 列入未核实清单。
- 实验验证: 发光/荧光、SEC、晶体学（"crystal structures match the design models with **atomic accuracy**"）、水凝胶、哺乳细胞光控信号。
- **命中率原始数字**: ⚠️**仅摘要级**（摘要无计数；原句 https://europepmc.org/article/MED/40877575："Here we describe a computational approach to design protein-protein interactions regulated by non-canonical amino acids, focusing on the light-responsive phenylalanine-4'-azobenzene (AzoF). … Biophysical characterization confirms the light-responsive assembly and disassembly of these complexes, and the crystal structures match the design models with atomic accuracy."）
- 演进链位置: 从"静态 binder"彻底转向"**刺激响应 + 非天然化学**"；判据必须包含"开关态都稳定、配体/光照态耦合自由能合适"（与 C03 的 ΔG 逻辑一脉相承）。

### [C16] Proteus: Exploring Protein Structure Generation for Enhanced Designability and Efficiency
- 作者/单位/角色: Wang C（王晨彤）, Qu Y, Peng Z, Wang Y, Zhu H, Chen D, **Cao L（末位通讯）**。**西湖独立 PI 的方法学工作（2024 预印本）**。
- 期刊, 年: bioRxiv 2024-02-10 | DOI: **10.1101/2024.02.10.579791** ✅（EPMC PPR804303 + bioRxiv 正文页）
- 设计对象: 蛋白**骨架生成模型**本身（为后续 binder/酶/配体设计供血）。
- 候选生成: Proteus = 深度扩散网络 + **graph-based triangle 方法 + multi-track interaction network**，**不依赖结构预测网络预训练**（对比 RFdiffusion 依赖 ESM/AF2 预训练）。
- 计算筛选器: 以 in-silico designability + 效率为核心指标（具体阈值见正文；本卡片引用的是其自述）。
- 实验验证: "comprehensive **in silico** evaluations and **experimental characterizations**"（摘要级）；其后续 Proteus2 直接用于金属蛋白酶设计（C21）。
- **命中率原始数字**: ⚠️**仅摘要级**——摘要原句："These promising results underscore Proteus's ability to generate highly designable protein"（无百分比；不编造）
- 演进链位置: **他从"用 Baker 的生成模型"走向"自研生成模型"的节点**，动机是效率（算力是他反复抱怨的成本项，见 C18 讨论）。

### [C17] De novo design of small molecule–regulated protein oligomers
- 作者/单位/角色: Jin Q（金启涵，博/后一）, Wang Y（王昱开，共一）, Chen D, Liao J, Cui Z, Fan Y, Zeng A, **Xie M（解明岐，共同通讯）**, **Cao L（曹龙兴，共同通讯/末位）**；单位含"State Key Laboratory of Gene Expression, School of Life Sciences and School of Medicine, Westlake University"等（✅ Crossref 作者单位字段）。**独立 PI 时期（2026-01-01 在线，Science 2026 年第 1 期）**。
- 期刊, 年: **Science 391(6780):eady6017, 2026（2026-01-01 在线）** | DOI: **10.1126/science.ady6017** ✅（Crossref + PubMed PMID **41477902**）；⛔无 OA 全文、无预印本（EPMC 检索不到对应 PPR）
- 设计对象: **小分子（FDA 已批金刚烷胺 amantadine）调控的蛋白同源三聚体（mAIT/dAIT）与异源二聚体/三聚体（AMA10 系列）**，单体约 **65 个氨基酸**；用于蛋白定位、无膜细胞器（condensate）与基因表达调控、小鼠体内口服给药激活肝转基因。
- 候选生成（✅二级来源+摘要）: **对称性匹配 + "对接-结合同步优化"**：RifGen 生成对称 rotamer interaction field 评估蛋白-配体结合；**蒙特卡洛片段装配**把三螺旋束单体在对称约束下组装为同源三聚体，同步优化蛋白-蛋白（RPX 哈希）与蛋白-配体（RIF 打分）相互作用；序列由 **Rosetta + ProteinMPNN** 设计；异源体系用 **RFdiffusion 生成连接螺旋 + ProteinMPNN 正负电荷设计**。
- 计算筛选器: 见上（RIF/RPX 双打分 + 对称性约束）；⛔**具体阈值数字未从正文核实**。
- MD/QM: ⚠️摘要级未见 MD/QM 证据。
- 实验验证: E. coli 表达 + SEC、SEC-MALS、ITC/BLI、晶体学（1.5 Å）、流式与报告基因、小鼠体内。
- **命中率原始数字（⛔二级来源：腾讯新闻转载西湖大学官方稿，https://news.qq.com/rain/a/20260102A04K2D00，2026-01-02/04；未在论文正文核实，务必按"待核"对待）**：
  - "在最早的设计中（即"单金刚烷胺诱导三聚体"，**mAITs**）…然而，**所设计的 24 个蛋白质中仅有一个蛋白展现微弱的"遥控组队信号"**。" → **1/24 = 4.2%**
  - "**在 48 个候选蛋白中，有 27 个"杀出重围"**，进一步，他们找到了"种子选手"：dAIT17。" → **27/48 = 56.3%（改进后的 dAIT 策略）**
  - 结构精度（⚠️来自丁香园/163 报道转述正文）："dAIT17 … **1.5 Å 分辨率晶体结构**验证了其与设计模型的高度吻合（**Cα 原子 RMSD 仅 0.67 Å**）"；"通过 RFdiffusion 生成连接螺旋将同源三聚体的两个亚基融合，结合 ProteinMPNN 的正负设计策略 … 最终获得异源二聚体 AMA10"（https://m.163.com/news/article/KI8S0U3U0532BT7X.html）。
- 演进链位置: 他组最"物理+深度学习混合"的成果：**把配体结合界面复用（对称性匹配）当作漏斗的第一道闸**，使"配体诱导组装"这类此前不可设计的目标从 4% 提到 50%+ 的投测命中。

### [C18] Design of miniprotein inhibitors targeting complement C9 to block membrane attack complex assembly
- 作者/单位/角色: Li M, Wang N, Fu X, Wei G, Zhang Z, Yu Y, Xue T, Zhao Y, Pan J, Wang D, Liu M, Li Y, Tang J, **Cao L（第 14 位）**, Jian Z, Liang S, **Yu B（于波/俞贝？末位通讯，山东第二医科大学）**。合作论文（曹为方法学贡献者）。
- 期刊, 年: **Nature Communications 17(1):3827, 2026-03-12** | DOI: **10.1038/s41467-026-70667-x** ✅ | PMID 41813685 / PMCID PMC13121834（OA）
- 设计对象: 补体 **C9** 的 mini-protein 抑制剂（阻断 MAC 膜插入）；80–130 残基较大 binder。
- 候选生成: **RFdiffusion**（骨架，1500/站点起步，最终跨位点共采样 **14,000 backbones**；总规模自述"约 25,000 binder scaffolds"）→ **ProteinMPNN**（每骨架 3 条序列）→ **AlphaFold2 打分** → 部分扩散（partial diffusion，diffuser.partial_T = 1–25，每个 T 值 1000 骨架）亲和力成熟。
- 计算筛选器（✅全文，阈值+成功率）：
  - 判据定义："**pae_interaction** represents the predicted aligned error that AlphaFold2 assigns to the binder–target interface"；"**Designs with pae_interaction < 10 are generally considered acceptable**"；"**plddt_binder** … **a threshold of > 90 is commonly required**"。
  - 放宽档："**After applying relaxed filters (pae_interaction < 15, plddt_binder > 88), Site-1 achieved a 1.20 % success rate, while Site-2 approached 0 %**."
  - "The initial success rate for **Site-3 was 0.16%**"；"generated **8000 scaffolds** with lengths ranging from 80 to 130 residues … achieving an initial success rate of **1.18%**"
  - "In a final round, the diffuser.T was set to 120 … a total of **14,000 backbones** were sampled across Site-1, Site-3 and Site-1 + 3, yielding success rates of **1.57%, 0.25% and 2.72%**, respectively."
  - 投测闸："**After filtering the combined ensemble (pae_interaction < 8.5, plddt_binder > 90), 103 top-ranking mini-protein binders** that target three distinct binding sites were selected for experimental validation."
  - 成熟闸："Applying stricter cut-offs (**pae_interaction < 6.2, plddt_binder > 90**) yielded **60 top-ranking sequences** for gene synthesis."
- MD/QM: 均未使用（全文无 MD/QM 关键词）。
- 实验验证: BLI、溶血抑制（人/豚鼠/兔血清）、CD 热复性、SEC、X 射线晶体学、AF3 复预测（pTM 0.85 / ipTM 0.93）、急性溶血小鼠模型（对比 eculizumab）。
- **命中率原始数字（✅全文）**：
  - 计算侧 in-silico 成功率 **0.16%–2.72%**（见上，按位点）；
  - 实验侧："**103** … selected for experimental validation"；部分扩散后 "**60** top-ranking sequences for gene synthesis" → "**identified 30 candidates that outperformed the parental Binder-47**" → **30/60 = 50%（成熟轮命中率）**
  - 亲和力："Binder-47 interacts more strongly with mouse C9, with **K_D values of 3 and 22 nM**"；"BLI results indicated an obvious enhancement of affinity with a **K_D of 0.7 nM between P9 and human complement C9**"（摘要口径"optimized to 700 pM via partial diffusion"）；
  - **判据失效的直接自白**："the hemolysis inhibition rates obtained from experimental validation **showed no strong correlation with the pae_interaction** … indicating the importance of experimental validation."；成本自白："we employed relatively large-scale cluster computing and generated approximately **25,000 binder scaffolds** in the initial screening phase, **which led to high computational costs**."
- 演进链位置: 展示 RFdiffusion 时代"AF2 置信度双阈值"漏斗的**真实上限**（in-silico 通过率仅 ~1–3%，且与功能不相关）。

### [C19] HalluDesign: Protein Optimization and de novo Design via Iterative Structure Hallucination and Sequence Design
- 作者/单位/角色: Fang M（方敏超）, Wang C, Shi J, Lian F, Jin Q, Wang Z, Zhang Y, Chen P, Cui Z, Wang Y, Zhang Z, Ke Y, Han Q, **Cao L（末位通讯）**。**西湖独立 PI 的方法学（2025-11-08 预印本）**。
- 期刊, 年: bioRxiv 2025 | DOI: **10.1101/2025.11.08.686881** ✅（EPMC PPR1116408 + bioRxiv 正文全文）
- 设计对象: 通用框架——蛋白优化、**de novo binder**、小分子结合蛋白、磷酸化特异性抗体/纳米抗体、核酸（见 C20）。
- 候选生成: 用 **AlphaFold3/Protenix 式结构预测模型的"幻觉"能力**做**免微调、仅前向**的序列-结构协同迭代优化（不同噪声水平控制采样空间）。
- 计算筛选器（✅全文，含成功率定义）：
  - 成功率定义原句："**The success rate is defined as:**"
  - 配体任务 in-silico："This success rate was **inversely proportional to ligand size and polarity**:"
  - 口袋定义："Binding pockets are defined using **Fpocket**,"（三种初始化：质量中心 / 口袋中心 / 幻觉）
- MD/QM: 全文未见 MD/QM 自算（⛔无相关关键词）。
- 实验验证: **每靶点固定投测 16 个设计**（BLI 结合 + 亲和力）；E. coli 表达、晶体学；对比 RFdiffusion / BoltzDesign1 基线。
- **命中率原始数字（✅全文，https://www.biorxiv.org/content/10.1101/2025.11.08.686881v1.full-text）**：
  - de novo binder："For each target, **we experimentally tested 16 de novo designed binders** and observed high success" → **50% 与 81.3%**
  - 拯救（优化 RFdiffusion 失败设计）："**Biolayer interferometry (BLI) assays demonstrated that 12 out of 16 PD-L1 binders successfully**"；图注对比："Optimized Failed Scaffold from RFdiffusion for" → **12.6% vs 75%**；**33.3% vs 50%**
  - 实验口径声明："Experimental characterization of binder design"
- 演进链位置: **这是他筛选逻辑改变的最直接证据**：不再"生成 10⁵ 设计→用物理分数排序→投 10²–10³ 个"，而是"**用预测模型自身的幻觉把设计直接推到判定阈值以上→只投 16 个/靶**"，因此"投测命中率"从 <1–5% 跳到 50–81%。**注意：分母从 10⁴–10⁵ 变成 16，正是"90%+"类传闻的口径来源。**

### [C20] HalluDesign-NA: Extending HalluDesign for De Novo Nucleic Acid Design
- 作者/单位/角色: Fang M, Wang Z, **Cao L（末位通讯）**。西湖组（2026-06-10 预印本）。
- 期刊, 年: preprint | DOI: **10.64898/2026.06.10.730767** ✅（EPMC PPR1251738）
- 设计对象: ssDNA / ssRNA / **适配体**结构域设计。
- 候选生成: HalluDesign 框架 + **NA-MPNN** 序列优化，迭代序列-结构协同。
- 计算筛选器: 置信度分数改进（pLDDT、ipTM）；约束含长度、对称性、与蛋白结构上下文。
- MD/QM: 未见。
- 实验验证: **仅计算基准（computational benchmarking）**——摘要未声称湿实验闭环。
- **命中率原始数字**: ⚠️**仅摘要级且为 in-silico**："Computational benchmarking across ssDNA, ssRNA,"。
- 演进链位置: 方法外推到核酸；提示其"以模型置信度为准入判据"的漏斗逻辑正在**脱离实验验证**（风险项）。

### [C21] De novo design of ligand binding and sensing with a physics based generative approach
- 作者/单位/角色: Zhang Y, Ke Y, Zhi R, Jin Q, Feng Y, Wang C, Fang M, Liao J, Chen D, Liu J, **Cao L（末位通讯）**。西湖组（2026-07-13 预印本）。
- 期刊, 年: preprint | DOI: **10.64898/2026.07.13.738243** ✅（EPMC PPR1279910；正文已核 https://www.biorxiv.org/content/10.64898/2026.07.13.738243v1.full-text）
- 设计对象: 小分子与金属离子结合蛋白 + **配体诱导的构象变化传感器**（DTG、CIA、DFHBI、血清素、多巴胺、Zn²⁺/Ni²⁺ 等）。
- 候选生成: **物理-based 生成 + 折叠模拟并行**："Small molecule conformers were sampled, clustered, and refined through **quantum optimization**,"；蒙特卡洛折叠采样、"if a predefined threshold of consecutive unsuccessful moves is reached,"；序列由 **Rosetta + ProteinMPNN**（异源体系用 **LigandMPNN**）。
- 计算筛选器: "the structural accuracy of the final models was assessed by **comparing each design to**"；迭代优化中"Following rigorous computational filtering, selected variants were experimentally characterized,"（阈值数字未列于正文可提取部分）
- **QM 使用: ✅有**（配体构象"quantum optimization"，用于生成 RIF 的输入）；**MD 使用: ✗未见自算**——"Computational design of Periplasmic binding protein biosensors guided by molecular dynamics"仅作为参考文献出现。
- 实验验证: E. coli 表达 + **ITC**（定量热）+ 荧光/发光读数 + 菌落筛选 + 晶体学。
- **命中率原始数字（✅全文）**：
  - 投测规模："For experimental characterization, we selected **96 DTG designs, 94 CIA designs,**"；多样性度量"**median pairwise backbone RMSD of 12.63 Å for**"（刻意最大化骨架多样性）
  - "**For CIA, 20 out of 94 designs showed binding**," → **21.3%**
  - "**For DFHBI … 2 out of 16 designs produced a clear fluorescence increase** following ligand incubation" → **12.5%**
  - 血清素："six serotonin binders exhibited binding,"；多巴胺："identified one binder with an affinity of **75.0**"
  - 迭代改良："After evaluating **16 redesigned variants** based"；"After four rounds of iterative optimization,"
  - 金属/结构："the nickel binder NiM4 displayed 1:1"；晶体与设计："Cα RMSD of **0.97 Å / 0.791 Å / 0.446 Å**"，配体 "ligand RMSD of just **0.883 Å**"
  - 自评："these results demonstrate the **high success**"
- 演进链位置: **小分子结合/传感是他组当前最硬的瓶颈**（μM 级），因此他刻意用"高骨架多样性 × 大投测数（90+）"换取 ~20% 命中——与蛋白 binder 的 50–80% 形成鲜明对比。

### [C22] De novo design of metalloproteases for targeted amyloid-β cleavage
- 作者/单位/角色: Qu Y, Wang C, Zhu H, Wang Y, **Cao L（末位通讯）**。西湖组（2026-01-06 预印本）。
- 期刊, 年: preprint | DOI: **10.64898/2026.01.06.697903** ✅（EPMC PPR1219681；正文已核）
- 设计对象: **锌金属蛋白酶**，序列特异切割 Aβ（DP 系列）。
- 候选生成: 自研 **Proteus2（flow-based 生成模型）**同时生成酶-底物复合物，条件为"目标肽序列 + 预定义催化基序（His₃）"；两步"encapsulation"策略做成 clamp 形（夹持底物）；**AF3** 建模底物构象；**LigandMPNN** 优化序列；**AF3 复预测**验证收敛到设计催化几何。
- 计算筛选器: 双闸——催化几何收敛 + 底物可裂解位姿（"considered an **in-silico success** if the design (purple) and prediction (gray) **align to a sufficient degree**"，见 C23 图注）；具体阈值在该正文以图注给出，未以数字罗列（⚠️）。
- MD/QM: 全文未见自算 MD/QM；但引用"Rates of Uncatalyzed Peptide Bond Hydrolysis … Transition State Affinities of Proteases"（过渡态化学依据）。
- 实验验证: 表达纯化、**质谱裂解产物定量**（含"约 10% of the main product's abundance"的旁路切割）、时间降解曲线、动力学（Km、kcat、-log K_tx）、突变体分析、Aβ 降解。
- **命中率原始数字（✅全文，部分）**：
  - "Notably, for DP221-S3, … a very minor peak—**representing approximately 10% of the main product's abundance**—was also observed, indicating an alternative cleavage site shifted by one residue toward the C-terminus."（特异性水平）
  - "the **DP622-S2 Y91F** variant maintained a Km nearly identical to the original,"
  - 坦诚上限："**Although the turnover rates of our designs are**"
  - **未给"投测 N 个 → 命中 M 个"的漏斗计数**（列入未核实清单）。
- 演进链位置: 酶设计从"静态 theozyme 匹配"（C08）走到"**生成模型直接共生成酶-底物复合物**"，瓶颈由"结合"转为"**精确到亚埃的催化几何 + 底物特异识别**"。

### [C23] Integrating Machine-learning and Ultra-high-throughput Screening for Enzyme spaces exploration (IMUSE)
- 作者/单位/角色: Ke Y（易开）, Zhang Y, Fang M, Zhao J, Zhu H, Xu Z, **Cao L（末位通讯）**；单位"State Key Laboratory of Gene Expression, School of Life Sciences, Westlake University" + "Artificial Intelligence Drug Design Core Laboratory,"（✅ bioRxiv 正文作者单位）。西湖组（2026-06-23 预印本）。
- 期刊, 年: preprint | DOI: **10.64898/2026.06.23.733994** ✅（EPMC PPR1259026；正文 https://www.biorxiv.org/content/10.64898/2026.06.23.733994v1.full-text）
- 设计对象: **de novo 锌水解酶**（库 Lib1 / Lib2，荧光底物 FDBz）。
- 候选生成: "a physics-based generative approach for de novo enzyme design,"："the substrate **transition state calculated using quantum chemistry**" + **RIF generation** 扰动配位几何 + **Monte Carlo fragment assembly（ProBuilder）** 自下而上建骨架 + **ProteinMPNN / Rosetta** 序列设计。
- 计算筛选器（✅原文）: "Structures featuring **all three coordination histidines** along with favorable transition state"；"Top candidate designs were selected based on **Rosetta energy metrics** and further assessed for"；"Designs are evaluated by structure prediction"；最终"**AlphaFold3-based** features, relating to the compatibility of the protein and the substrate"进入 ML 活性预测器。
- **QM 使用: ✅有**（"substrate transition state **calculated using**"）。**MD 使用: ✗未见自算显式溶剂 MD**（无 MD/GROMACS/自由能微扰关键词）。
- 实验验证方法与通量（这是他"廉价高通量代替昂贵单测"的核心答案）：**sdDE-FACS**——"we developed an ultra-high-throughput screening method by integrating **single-droplet double emulsion** with **fluorescence-activated cell sorting (sdDE-FACS)**"；"This approach enabled the screening of"；"genes encoding the designed enzyme fragments were"；"E. coli cells expressing unique enzyme sequence"；检出下限"capable of detecting **<1 nM fluorescent probe (5 orders of magnitude)**"；"thousands of droplets per second"；**NGS** 计数每轮回收的唯一设计数。
- **命中率原始数字（✅原文）**：
  - "Subsequently, we generated a second-generation" → **28/96 = 29.2%（Lib1 ≈ 6%）**
  - "Strikingly, **16 of these 28 designs (~57%)**"
  - 预测器富集："This model was able to **enrich the predictions**"
  - 结构分布证据："structure distribution quantified here by **qTM**"
  - 关键负面结论（判据失效）："Previous retrospective analysis of Lib1 dataset"
- 演进链位置: **筛选逻辑的第三次转向**：物理指标（ddG/pAE）对 de novo 酶无效 → 用**微流控液滴 + FACS 造数据** → 训练**合成适应度景观（activity predictor）**当作新的筛选器 → 用模型挑 96 个投测，命中率 6%→29%。

### [C24] Frontiers and challenges in the design of binders for intrinsically disordered proteins（综述，他本人的漏斗自述）
- 作者/单位/角色: Wang C, Zhang Y, Fang M, Peng Z, **Cao L（末位通讯）**。西湖组（2026）。
- 期刊, 年: **Current Opinion in Structural Biology, 2026-06** | DOI: **10.1016/j.sbi.2026.103256** ✅ | PMID 41887012（⛔非 OA，仅摘要级）
- 内容定位: 面向 IDP binder 设计的方法评述，是他公开陈述"该用什么判据、什么通量"的文本（⚠️正文不可得，不作引用）。
- **命中率原始数字**: 不适用（综述）。
- 演进链位置: 下一步方向——**无序蛋白/构象集合的 binder 设计**（预示其漏斗要处理"没有单一目标构象"的判据问题）。

### [C25] 应用/工具类与背景论文（合并卡片，均经 API 核验）
- **Interaction of human dendritic cell receptor DEC205/CD205 with keratins** — J Biol Chem 2024, DOI **10.1016/j.jbc.2024.105699** ✅（PMID 38301891；EPMC 亦有 PMC10914487 记录）。博后/早期结构生物学延续，非设计。
- **Mechanistic insights into the C-type lectin receptor CLEC12A-mediated immune recognition of monosodium urate** — J Biol Chem 2024, DOI **10.1016/j.jbc.2024.105765** ✅ (PMID 38367667).
- **Structure of scavenger receptor SCARF1 and its interaction with lipoproteins** — eLife 2024, DOI **10.7554/elife.93428** ✅ (PMID 39541158, PMC11563577; 预印本 10.1101/2023.11.08.566208 ✅)。
- **Nab-paclitaxel fused with the de novo designed receptor binder exhibits enhanced tumor targeting and therapeutic efficacy** — J Control Release 2026, DOI **10.1016/j.jconrel.2026.115355** ✅ (PMID 42744200；预印本 10.64898/2026.01.28.702218 ✅ PPR1226620)。**曹为第 13 位/15 人**，通讯为 He Y（何永盛）/Liu Y —— 设计 binder 的药物化应用（EGFRmb/HER2mb-Nab-PTX），非其主导漏斗工作。
- **CTBPro: A Next-Generation Cholera Toxin Subunit B-Based Neuroanatomical Tracer** — Advanced Science 2026, DOI **10.1002/advs.202522249** ✅ (PMID 42017467, PMC13335673)。曹第 11/13 位（贾洁旻组）。
- **Programmable design of functional proteins from natural language (Pinal)** — bioRxiv 2024, DOI **10.1101/2024.08.01.606258** ✅（EPMC PPR890188；33 位作者中的 **Cao L** 为众多合作者之一，通讯 Yuan F 等）。**非其主导**；其"设计荧光蛋白/PET 水解酶/醇脱氢酶/H-protein"的湿实验闭环与曹组无直接归属关系，引用时须谨慎。
- **博士期（非设计）**：HCV E1E2 异源二聚体功能表达，PLoS Pathogens 2019, DOI **10.1371/journal.ppat.1007759** ✅（PMID 31116791，曹共一）；人 M-PLA2R 冷冻电镜，J Mol Biol 2017, DOI **10.1016/j.jmb.2017.10.019** ✅（PMID 29079480）；Cbln1/Cbln4–GluD2，Cell Rep 2017, DOI **10.1016/j.celrep.2017.08.031** ✅（PMID 28877468）。→ 证明其博士训练是**结构生物学（膜受体）**，不是计算设计，也无浙大/周如鸿痕迹。
- **综述**：The JAK-STAT pathway: from structural biology to cytokine engineering, Signal Transduct Target Ther 2024, DOI **10.1038/s41392-024-01934-w** ✅（PMID 39169031，含 Correction 10.1038/s41392-024-01975-1）。

> **关于用户假设的两点更正（实证）**
> 1. **"Robust and tunable immune activation by a designed membrane-bound receptor"（Nature 2021）在曹龙兴的论文记录中不存在**。核查：Europe PMC `TITLE:"Robust and tunable immune activation by a designed membrane-bound receptor"` → **hitCount = 0**；PubMed `designed membrane-bound receptor[Title]` → **count = 1**，即 PMID **39553285**（"Membrane-bound receptor for advanced glycation end products (RAGE) is a stable biomarker of", Hum Reprod Open 2024，与曹无关）。曹 2021 年的设计论文实为 **C03（Nature 2021 biosensors）** 与 **C04（Cell Host Microbe 2021）**；免疫受体方向是他的 **C14（TGFβRII/CTLA-4/PD-L1 binder）与 C12（DNDB-CAR）**。
> 2. **曹龙兴不是 RFdiffusion / ProteinMPNN 的作者**：Crossref 实取 **10.1038/s41586-023-06415-8**（RFdiffusion, 28 位作者）与 **10.1126/science.add2187**（ProteinMPNN）作者列表，均**无 Longxing Cao**。他用这两个工具（C17、C18），但不是其发明者。

---

## 二、筛选级联总结表

| 文献 | 生成器 | 第一级计算闸（阈值） | 第二级计算闸 | 送实验规模 | 实验读出（通量） | 表达/可溶率 | 结合·功能命中率 |
|---|---|---|---|---|---|---|---|
| C01 Science 2020 | Rosetta + RIF docking | Rosetta ddG/CMS | — | 105 enriched（酵母库 NGS） | 酵母 FACS→E. coli→BLI | 12/105 = 11.4% | **11/12 = 91.7%（表达后）**；绝对 11/105 = 10.5%；终 10 个 pM–nM |
| C02 Nature 2022 | PatchDock→RifDock→Rosetta FastDesign | "Predictor"快速疏水打包（10×加速）+ 阈值概率 sigmoid | ddG / SC / 界面埋藏 SASA / **CMS**；聚类相似分 0.7 | **15,000–100,000/表位**（投测数≈设计的 1/10；10⁵ 设计 ≈ 10⁴ CPU·h） | 酵母展示文库 + 多轮 FACS + NGS（SC50）；0.1% 收集 | 骨架库层面 34,507/84,690 = 40.7% 稳定 | **数百（FGFR2/PDGFR）到 <10（TIE2/CD3δ）/100,000** ⇒ **~0.01–0.3%**；"only a small fraction of designs bind" |
| C05 PLOS ONE 2022 | Rosetta/dTERMen + 序列-only CNN | 序列-only 稳定分数 | GM 二级结构一致排序 | 1,000 GM 设计（Corpus B） | **蛋白酶解滴定 FACS+NGS，单次实验最多 10 万个蛋白** | 993/1,000 可检测表达 | **47/275 = 17% 稳定**（低同源子集）；dTERMen 组 **<1%** |
| C06 STM 2022 | 组合 linker/寡聚化设计 | 几何（末端距离 vs 开/闭态） | — | **>100 三聚体 + >100 融合体** | **CFPS 无细胞表达 + 发光** | — | 结构域层面 **9/11 = 81.8%** 至少得到 1 个可用设计 |
| C08 Nature 2023 | family-wide hallucination（trRosetta/MCMC）+ RIF | 配体结合能、H 键、**SC、CMS** | 第二轮 **AF2 pLDDT > 92** + Cα RMSD/CMS/Rosetta 结合能 | 第一轮 **7,648**；第二轮 **46** | 寡核苷酸池→E. coli 96 孔→**菌落化学发光成像直筛** | — | **3/7,648 = 0.039%** → **2/46 = 4.3%**（原文："success rate increased from 3/7,648 to 2/46"）；ML+QM/MD 加入后 **100×+** 提升 |
| C10 Cell 2024 | DHR/5HCS 对称对接 | sc > 0.65、**ΔΔG < 0**、未满足 H 键 < 2 | — | **109** 合成基因（+14 个 C2） | E. coli→SEC→**SAXS/SEC-MALS**→cryo-EM | **60/109 = 55.0% 可溶** | **28/60 单分散（25.7% 全量）**；**10/109 = 9.2% 正确寡聚态**；C2 组 **3/14 = 21.4%** |
| C11 Nature 2024 DICE | Rosetta+MotifGraft+**ProteinMPNN**(2000 seq/输入) | **ddG < −40 且 SAP < 35** | **pAE_interaction < 10 且 relaxed_ddG < −40**；**monomer pLDDT < 85 丢弃**；SAP/CST<5/净电荷 −7 | **170** 设计（自 21,000/站点→3,000→…） | E. coli 表达 + 流式/降解功能 | — | **8/170 = 4.7%** 双域结合；最优 K_D 21 nM；PD-L1 清除 77% |
| C12 Nat BME 2024 | 曹组 binder 管线 | ⛔未获正文 | ⛔ | ⛔ | CAR-T 功能 + scRNA-seq | ⛔ | ⛔ 未核实（仅摘要级） |
| C14 Nat Commun 2025 | 自建 **5HCS 7,476** 支架库 + Cao-RIF + Rosetta | 曲率（凹面准入）、结合取向、ΔSASA | **ddG < −40、CMS > 400、pAE < 10**；**AF2 mean pLDDT ≥ 80**、DeepAccNet | 投测 **96**（PD-L1 集）等 | **酵母 oligo 池 + FACS + NGS** → E. coli → BLI/ITC→晶体学 | — | **PD-L1: 2/96 = 2.1%**；**CTLA-4: 6 个 binder**；优化后 646 pM；EC50 53.3 nM |
| C17 Science 2026 | **对称性匹配 + RIFGen + Monte Carlo 装配 + Rosetta/ProteinMPNN**（异源：RFdiffusion+LigandMPNN） | 蛋白-配体 RIF 打分 × 蛋白-蛋白 RPX 同步优化 | ⛔阈值未核实 | mAIT **24**（⛔新闻）/ dAIT **48**（⛔新闻） | E. coli + SEC + ITC/BLI + **晶体学 1.5 Å** + 小鼠口服 | — | ⛔二级来源：**1/24 = 4.2%** → **27/48 = 56.3%**；dAIT17 Cα RMSD 0.67 Å |
| C18 Nat Commun 2026 | **RFdiffusion**(~25,000 骨架；终轮 14,000)→ProteinMPNN(3/骨架) | 站点疏水热点（V196/I199/V305 等） | **pAE_int < 10（可接受）/ >8.5 严格；pLDDT_binder ≥ 90（常用）**；放宽 <15/>88；成熟用 partial_T 1–25 | **in-silico 通过率 0.16–2.72%** → **103 投测**；成熟 **60** | BLI + 溶血抑制 + 晶体学 + AF3(pTM 0.85/ipTM 0.93) | — | 部分扩散 **30/60 = 50%** 优于母本；K_D 22 nM→**0.7 nM**；**"pAE 与抑制率无显著相关"** |
| C19 HalluDesign 2025 | **AF3/Protenix 幻觉（免微调前向）** | **成功率定义：蛋白 RMSD ≤ 1.5 Å & pLDDT ≥ 85 & 配体 RMSD ≤ 2 Å & 配体 pLDDT ≥ 85 & ipTM ≥ 0.85** | 配体任务 in-silico > 60%（小/疏水） | **每靶 16 个**（固定小投测） | **BLI** + 晶体学 | — | **FGFR2 13/16 = 81.3%**（最佳亚 nM）；**PD-L1 8/16 = 50%（32 pM）**；拯救 RFdiffusion 失败：PD-L1 **12/16 = 75% vs RFdiff 12/95**；IL7RA **8/16 = 50% vs RFdiff 32/96** |
| C21 physics-based 2026 | 量子优化配体构象 → RIFGen + 折叠模拟 + Rosetta/ProteinMPNN/LigandMPNN | 与 AF2 预测比对 | — | **96 DTG / 94 CIA / 32 DFHBI**（RMSD 中位 12 Å 高多样） | E. coli + **ITC** + 荧光 + 晶体学 | — | **CIA 20/94 = 21.3%**；DFHBI **2/16 = 12.5%**；血清素 6 个（72.8 μM）；迭代 4 轮提升 15.7× |
| C23 IMUSE 2026 | 量子化学过渡态 + theozyme + MC 片段装配 + ProteinMPNN | **His₃ 齐全 + 过渡态有利作用**；Rosetta 能量 | AF2/AF3 "design 与 prediction 对齐"=in-silico success；**ML 活性预测器（top-50 富集 >2×）** | **Lib2: 96 纯化候选**（Lib1 N=145） | **sdDE-FACS：单次运行筛百万液滴（数千滴/秒）+ NGS** | — | **28/96 = 29.2%（较 Lib1 的 ~6% 提升 4.9×）**；其中 **16/28 = 57%** 有可测 Km/催化；Lib1 该比例为 40%；"传统指标与活性无显著相关" |

**从表中得到的核心事实（一句话）**：他的漏斗在 2022 年是"**设计 10⁴–10⁵ → 计算排序 → 投 10²–10³ 个 → 实验命中 0.01–5%**"；到 2025–2026 年变成"**生成模型自身迭代到判定阈值（pAE/pLDDT/ipTM/RMSD 五联判据）→ 只投 16–96 个 → 实验命中 20–80%**"；分母缩小 2–4 个数量级，而不是"同一漏斗的命中率凭空提高 20 倍"。

---

## 三、方法演进时间线（Baker 组时期 → 西湖大学时期）

**阶段 1｜物理打分时代（2017–2021，博后）**
- 起点：Rosetta 能量函数 + RIF docking + 预定义骨架库（C01、C02）。判据全是**热力学/几何近似量**（ddG、SC、埋藏 SASA、CMS），且因算力瓶颈不得不加"**Predictor**"这一廉价代理打分（10× 加速 + sigmoid 通过概率）——筛选逻辑的动机是"**算力/合成成本**"，不是"分数更准"。
- 反馈学习：810,000 设计 + 240,000 单突变的数据集用于回校力场；"iterative design-build-test cycles … should lead to systematic improvements in the methodology and"（C02 原文）。
- 同期通量底座：C05（10 万蛋白/次稳定性筛选）、C06（CFPS 高通量）。

**阶段 2｜深度学生成进入 binder（2021–2023）**
- 序列侧 **ProteinMPNN**、骨架侧 **RFdiffusion** 成为工具（注意：C02 论文主体仍是 Rosetta；RFdiffusion/ProteinMPNN 原作者列表中无曹）。
- 他参与的"结构预测置信度"作为准入判据开始固化：**pAE_interaction、pLDDT**（C08 用 AF2 pLDDT>92；C11 用 pAE_int<10 + pLDDT≥85 + ddG<−40 + SAP<35 + 净电荷 −7）。
- 逻辑变化原因：**物理分数与实验结果相关性弱**（C23 直言"none of the conventional metrics showed a"），而神经网络置信度是"整链一致性"判据，能过滤掉力场失真的假阳性。

**阶段 3｜西湖独立 PI（2021– ）：三类新瓶颈与相应筛选改动**
1. **"没有目标构象"的功能型设计（开关/传感/光/小分子）**：C03→C15→C17→C21。判据从"单态结构像不像"变成"**两个态都要自洽 + 态间自由能差符号正确**"（C03 的 ΔG_open−ΔG_CK 不等式；C17 的"无配体单体稳定 / 有配体高效组装"）。因此他必须回到物理建模 + 自研生成（Proteus/C23 的物理-based generative），而不是直接用为"单一稳态"优化的扩散模型。
2. **大蛋白/高阶组装**：C10（109→10，9.2%）、C14（120 aa 凹面支架 5HCS）。瓶颈是**价态与几何**而非折叠，所以加了 SAXS/SEC-MALS、cryo-EM 这种"贵但唯一判得了"的测量。
3. **酶/化学功能**：C08（0.039%→4.3%，且有 **DFT+500 ns MD**）、C22（Proteus2 共生成酶-底物）、C23（IMUSE：QM 定过渡态 + **液滴微流控百万级筛选**造数据 + **ML 活性预测器**替人挑候选）。瓶颈是"活性 ≠ 结合 ≠ 会折叠"，所以他把筛选器从"结构一致度"改成"**数据学出来的功能预测器**"，并让通量端从 96 孔跳到百万液滴。
4. **生成模型自研（解决算力与依赖）**：Proteus（不依赖 AF/ESM 预训练，效率优先，C16）→ Proteus2（C22）→ HalluDesign（**免微调、仅前向的序列-结构协同**，五联判定阈值，C19）→ HalluDesign-NA（C20）。筛选逻辑的变化是"**把判定阈值前置到生成回路内**"，因此实验只需 16 个/靶。

**阶段 4｜转化（2024– ）**：DNDB-CAR 进入 IIT（C12）、binder 用于化疗药偶联（C25 之 Nab-PTX）、LCB1 类中和剂（C01/C04/C06）。此时判据再加两条工程属性：**CAR 表面表达 + 抗降解**（C12 摘要与单细胞转录组证据），以及**血清交叉反应/体内半衰期**（C18、C25）。

---

## 四、MD/QM 角色判定

**MD（分子动力学）——角色很轻，且主要用于"解释"而非"筛选"**
- ✅**唯一明确的 MD 计算**：C08 Nature 2023 荧光素酶（曹为第 12 位作者，Baker/Houk/Stanford 合作）——"We used a combination of **density functional theory (DFT) calculations and molecular dynamics**"；"…plotted throughout **500 ns MD simulations**"；图题"**Free-energy profile of DTZ chemiluminescence and MD simulations** of proposed"；用于解释 **50 倍底物选择性**（bis-CTZ 的苄基碳破坏过渡态形状互补、削弱 Arg65 电荷稳定）。
  → 性质：**机制解释 + 自由能剖面**，不是准入判据（7,648→3、46→2 的漏斗里没有 MD 关卡）。
- ✗**未见**他在设计漏斗中使用显式溶剂 MD 预筛、**MM/PBSA、MM/GBSA、FEP/TI、metadynamics、umbrella sampling**：对 C01、C02、C04、C05、C06、C10、C11、C13、C14、C18、C19、C21、C22、C23、ncbipmc_8074680 全部正文做了 `molecular dynamics|MD simulat|GROMACS|OpenMM|AMBER|umbrella|metadynam|MM/PBSA|MM-GBSA|free energy perturbation|thermodynamic integration|explicit solvent` 扫描，除 C08 外**仅命中参考文献条目**（C21 里的 "…guided by molecular dynamics" 是他人工作的引文）。
- ⚠️他 2021–2026 的西湖论文中，"free energy"一词只以**概念/不等式**出现（C03 的 ΔG 热力学耦合；C14 的 "reducing solvation-free energy" 讨论），非数值模拟。
- **判定（信心：高）**：曹龙兴团队的"稳定性/构象验证"靠 **AF2/AF3 置信度 + SEC/SEC-MALS/SAXS/晶体学/CD**，不靠 MD。这与其师承（Baker 组物理-统计打分传统）一致。

**QM（量子化学）——只在"酶/化学步"出现**
- ✅**C08**（DFT：阴离子态是 ³O₂ 活化的电子源；与 MD 联合）——这是"生色团/化学发光机理"类 QM。
- ✅**C23 IMUSE**："the substrate **transition state calculated**" → theozyme 构建的第一步；即 QM 给出过渡态几何，再由 RIF/MC/ProteinMPNN 装配蛋白。
- ✅**C21**：ligand conformers"refined through **quantum optimization**" → 配体构象系综由 QM 优化，再喂给 RIFGen。
- ⚠️**C22 金属蛋白酶**：催化依赖过渡态稳定，但正文未出现 QM 计算描述（仅引用无催化肽键水解速率/过渡态亲和力的文献）。
- ✗**未见**他为任何 **binder/组装体/光开关**工作做 DFT/TD-DFT（C15 的 AzoF 光异构化是否自建激发态计算无法核实，列入 §五）。
- **判定（信心：高）**：QM 在他体系里是"**化学步的输入准备器**（过渡态/配体构象/反应机理）"，而非筛选器；一旦设计对象不含共价/电子过程（binder、寡聚体），QM 与 MD 双双退出，判据完全由 Rosetta 指标 + 深度学习置信度承担。

---

## 五、未能核实的问题清单

1. **⛔ Science 2026（C17）漏斗计数的原始出处**："24 个设计只有 1 个""48 个候选 27 个成功"来自**西湖大学官方口径的中文新闻稿**（https://news.qq.com/rain/a/20260102A04K2D00，2026-01-02/04），我**未能拿到 Science 正文**（无 OA、无预印本）。**能改变结论的证据**：Science 正文或 SI 中的表（design list + SEC/ITC 结果）。当前不能把这些数字列为"论文级"。
2. **⛔ Nat Biomed Eng 2024（C12）与 Nat Chem 2025（C15）的计算阈值与投测规模**：两篇无 OA 全文，EPMC `fullTextXML` 与 NCBI efetch 均无正文；摘要与新闻稿均不含漏斗数字。**尚缺**：期刊全文或 SI 方法段。
3. **⛔ Nat Chem 2025 是否做激发态 QM（TD-DFT）处理 AzoF**：正文不可得，无法判定"是/否"。
4. **⛔ 曹龙兴博士导师**：仅由"博士期论文末位通讯均为 He Y + 单位为 SIBCB"推断为何永盛组；**未见官方"师从"表述**。
5. **⚠️ Nature 2022（C02）各靶位点的确切 binder 数（Extended Data Table 1）**：表格数值未进入 PMC XML（正文只给 "hundreds vs fewer than 10"），故各靶的分子/分母未能逐条列出；**"送测序列数"**也只有间接表述（"at least ten times as many binders were computationally designed than were ordered"）。
6. **⚠️ Nat Commun 2025（C14）的 TGFβRII 集投测数与 DeepAccNet 截断值**：正文原句在 XML 中被截（"…AccNet with a mean pLDDT cutoff of 0."），数字不完整；TGFβRII 的"投 N 中 M"未能提取。
7. **⚠️ IMUSE（C23）Lib1 的绝对投测数与"40% success rate"的确切分母**：Lib1 命中率由"28/96=29.2% 是 ~4.9× 提升"反推 ≈6%；"16/28 (~57%) … in contrast to the 40% success"这句的 40% 所指（是"活度→可测动力学"的比例）在正文上下文推断得出，未获表格级确认。
8. **⛔ 曹龙兴是否有"跨膜/膜蛋白从头设计"论文**：Europe PMC 作者检索 `AUTH:"Longxing Cao" AND TITLE:"transmembrane"` → **hitCount = 0**；`TITLE:"nanomaterial"` → **0**。→ **未发现**。他参与的"大蛋白"方向实际是**重复蛋白高阶寡聚体（C10）与 120 aa 凹面支架（C14）**，跨膜蛋白设计公开归属为**卢培龙组/Boon 等**，非曹。
9. **⛔ "周如鸿称曹龙兴（或该方向）设计成功率 90%+"的原话出处**：本次仅在曹的文献侧核实——其 24 份全文/预印本中**不存在 90%+ 的成功率表述**（最高为 13/16 = 81.3%）。周如鸿侧的核查见同目录 `zhou.md` 第四节（结论一致：未找到 90%+ 的论文出处）。**尚缺**：该讲座/发言的原始记录（未发表口径不可核实）。
10. **⚠️ HalluDesign（C19）与 physics-based（C21）尚无同行评审版本**，其 50–81% 命中率为**作者自述的预印本数字**，未经独立复现；引用时应标注为 preprint。
11. **⚠️ Pinal 自然语言设计预印本（PPR890188）**中曹龙兴只是众多作者之一（非通讯、非共同一作），不应作为"他的方法"计入。

> **引用预算截短（2026-11-08，公开仓库口径）**：本底稿有 49 条逐字引句被截短（来源编号：B06; C02、B10; C08、C03、C16、C19、C20、C21、C22、C23、C25、未归属；许可类别：ALL_RIGHTS_RESERVED、CC_BY_NC、CC_BY_ND、TEXT_MINING_ONLY、UNKNOWN、未归属），按 `deliverables/protein_design_license_audit.csv` 的逐份许可判定，单条引句截到 ≤100 字符；其中 40 条截短后仍**逐字命中同一份来源全文**，其余 9 条为**原句的前缀**（本地无全文或原句是我们自己的转写，只减不增、不新增第三方内容）。逐条改动账见 `deliverables/quote_budget_notes_ledger.csv`。
