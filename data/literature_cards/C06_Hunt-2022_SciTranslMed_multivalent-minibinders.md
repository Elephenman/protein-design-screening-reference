# [C06] 单价设计打不出高亲和力时，他们不改进判据，改用"几何多价组装 + 无细胞表达通量"换亲和力

Hunt AC, Case JB, Park YJ, **Cao Longxing**, Wu K, Walls AC, …, Veesler D, Jewett MC, **Baker D**（47 人；华盛顿大学 IPD + 芝加哥西北 + 圣路易斯华盛顿）
Science Translational Medicine 2022, 14(646):eabn1252 · DOI 10.1126/scitranslmed.abn1252 · PMID 35412328 · PMCID PMC9258422
开放获取（CC BY 4.0）· 全文 https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9258422/fullTextXML · 预印本 10.1101/2021.07.07.451375

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C06**（组：曹龙兴组） |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory 记 `fetch_channel=epmc_fulltext`，2026-10-20 本地抓取） |
| 本地全文 | `data/literature_cards/fulltext/C06_PMC9258422_text.txt`（95,391 B，SHA-256 `26d26abf05bf311a…`）；同源 XML `C06_PMC9258422_fullTextXML.xml`（225,093 B） |
| 对照底稿 | `sources/cao.md:116-129`（原卡）、`sources/cao.md:412`（对比表 C06 行）、`sources/cao.md:455`（"曹组设计漏斗里未见显式 MD 预筛"的全库字符串审计） |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中） |
| 未取到的部分 | ①**Materials and Methods 的实操细节全部在补充材料**（正文只到 "MATERIALS AND METHODS Study design" 一段，随后即 References；原文自述 "SUPPLEMENTARY MATERIALS Materials and Methods Fig. S1 to S19 Table S1 to S5"），故本卡第 3 节的阈值只能取正文里出现的数字；②表 S1/S2/S4/S5（构建体命名表、亲和力与 mAb 对比、escape 概率推算）与数据文件 S1-S3 未取；③图 1-6 的原图数值。凡引用这些之处本卡写"正文未给出，仅有正文描述" |
| 与底稿的差异（本次补出来的内容） | 原卡只有 4 条引语；本次补：CFPS 流程的时间/仪器口径（6 小时、Echo 525）、off-rate 竞争实验的操作定义与判读阈值（100 倍过量 competitor、7 天、~1×10⁻⁷ s⁻¹）、11 个寡聚化结构域→9 个可用的分母口径、G 连接子被 E. coli 蛋白酶截断这一失败模式、负染 EM 交联作为"是否单价内跨联"的二级判据、cryoEM 分辨率与 MON2 设计-实测偏差 1.3 Å、escape 筛查的 36 孔与单/双突变覆盖率推算、鼻内给药剂量、以及作者自陈的三条局限 |

## 1. 这篇到底解决什么（大白话）

前作（C02/B06 那条线）已经能"只看靶结构"设计出单价的 SARS-CoV-2 小蛋白结合剂（LCB1、LCB3、AHB2，正文称 MON1/MON2/MON3），但**单价的东西一旦被变异体突变顶掉就失效**：LCB1 在 Beta/Gamma 上亲和力下降，AHB2 本身只有 nM 级（正文：23 pM 到 15 nM 的跨度）。这篇不做新的单价界面设计，而是做**"把已经设计好的单价模块按几何拼成三价"**：均三聚体（TRI，靠自组装结构域把 3 个单价模块摆到与 S 三聚体三个 RBD 匹配的位置）与多域融合体（FUS，靠 linker 串起来）。为了试得起上百种组合，他们把**湿实验通量**换成了核心资产——无细胞表达（CFPS）6 小时出纯化蛋白 + AlphaLISA 溶液竞争解离筛。最后用 cryoEM 证明设计模型基本实现（MON2 与设计模型主链 Ca RMSD 1.3 Å），并用活病毒中和、escape 筛查与小鼠保护把 TRI2-2 推到临床前。

**对我们最有价值的一点**：这是一篇**漏斗主力在实验侧、不在计算侧**的论文。它的"筛选判据"是几何约束（连多长要跨过开/闭态的末端距离）+ 表观解离速率，而不是打分函数阈值。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **单价亲和力不够、且会被突变顶掉**。原文给的起点：前作单价 minibinder "These minibinders neutralize the WA1/2020 SARS-CoV-2 virus with half maximal inhibitory concentration (IC 50 ) values in the range of 23 pM (LCB1) to 15 nM (AHB2)"；并且 "LCB1 has demonstrated protective activity as both pre-exposure prophylaxis and post-exposure therapy in human ACE2 (hACE2)-expressing transgenic mice, but mutations in the B.1.351 (Beta) and P.1 (Gamma) VOCs were shown to reduce binding potency"。深变扫还直接指出逃逸位点：LCB1 的 K417N 使亲和力下降 >10 倍、E406W 与 Y453K/R 下降 >100 倍。
   **应对**：不去重做界面，而是把"亲和力"当成可以被组装放大的量，并写下这个策略的理论依据 "Multivalent minibinders might be less sensitive to mutations that would escape binding of the monovalent minibinders; a 100x reduction in binding affinity of a sub-picomolar binder would still result in an affinity in a therapeutic range in a multivalent construct"。
   **代价**：亲和力提升集中在**解离速率**（表观 KD 的组成变了），并没有修正单价界面本身"错一点就全错"的问题；而且多价化引入了新的失败模式（见 2.4）。
2. **判据该测什么：不测平衡亲和力，改测解离速率**。他们明确说明为什么换指标："Because multivalency largely impacts dissociation rate constants of protein-protein interactions, we reasoned that an in-solution off-rate screen could distinguish differences between mono- and multivalent binding"。
   **应对**：定量的竞争解离协议 "Multivalent minibinders were allowed to fully associate with the target protein, then reactions were split in two and either 100-fold molar excess of untagged competitor (to prevent reassociation) or buffer was added."，用两种靶（单体 RBD 与三聚体 S6P）并行读数，靠"三聚体上明显更慢"来证明真是多价结合，而不是把 off-rate 慢当成亲和力高的替代读数。
   **代价**：指标是**表观**的（作者措辞 "likely apparent dissociation rate constant"），且判读依赖"7 天几乎不解离"这种接近量程上限的观察，无法给出可比较的绝对 KD。
3. **要试的组合太多，合成/表达是瓶颈**。他们为此专门造工具："To rapidly prototype multivalent minibinder designs, we developed a cell-free protein synthesis (CFPS) workflow which combines an in vitro DNA assembly step followed by polymerase chain reaction (PCR) to generate linear expression templates that are used to drive CFPS and enable rapid prototyping of new minibinder designs"；能力口径 "The workflow enables assembly and translation of synthetic genes and generation of purified protein in as little as 6 hours, is compatible with high-throughput, automated experimentation using an acoustic liquid handler (Echo 525), and is easily scaled for the production of mg quantities of protein"。
   **应对**：用 CFPS 支撑两个各 >100 条的组合库："We designed and screened more than 100 different homotrimeric minibinders, with varied linker lengths and homotrimzeriation domains, using the CFPS workflow." 与 "We screened more than 100 different fusions using the CFPS workflow, evaluating different minibinder orderings and a range of linker compositions and lengths"。
   **代价**：正文未给这套流程的单条成本；且无细胞表达量与真核/大肠杆菌表达并不等价，进入中和与动物实验时仍需换表达系统。
4. **构建体自身会失败，而且要归因**。三类可观察的失败都被写下来：
   - 序列层面被切："We observed occasional truncation of the G linkers during expression and purification by E. coli proteases; however, this was less frequent for the P linkers than for the G linkers."→ 应对：把 linker 组成当成一个筛选维度（G 与 P 平行比较），并优先用 P 类。
   - 几何不对（跨颗粒交联）："initial screening using negative stain EM revealed considerable cross-linking and aggregation of S trimers upon addition of the constructs"；而 "In contrast, for constructs TRI2-2, FUS231-G10, FUS231-P24 and FUS31-G10, we observed less cross-linking, consistent with multivalent engagement of a single S trimer for each minibinder."→ 应对：**加一道正交的形态学判据**（负染 EM 看交联），用它筛掉"跨两个 S 三聚体"的假多价，再决定谁进 cryoEM。正文还补了为什么这一步必要："We next determined how the designed multivalent proteins engage multiple RBDs on a single S trimer; multivalent engagement on a virion typically requires binding of a single S trimer due to the relatively sparse S distribution"。
   - 结构域不行（domain 4 与 11）："Designs with domains four and eleven exhibited slower dissociation rates compared to their monomeric counterpart, but faster than the top designs"，归因为 "this is likely indicative of an inability to simultaneously engage all three target epitopes or dissociation of the oligomerization domains themselves."→ 应对：不放弃，只把可用结构域收窄（11 个里取 9 个），并把两个 trimeric scaffold 定为 SB175 与 T4 foldon："We selected two trimeric scaffolds, the designed two ring helical bundle SB175 (domain 2) and the T4 foldon (domain 1)"。
5. **结构验证有分辨率上限，他们承认并降级结论**。"The limited resolution in the region comprising the minibinder-bound RBDs and linkers precludes definitive assignment of minibinder identity at each binding site and relative connectivity between each minibinder module."
   **应对**：改为**弱一级的判据**——只比对末端距离是否与设计模型相容："The distances between the termini of the minibinder domains, however, is compatible with the computational design models and suggestive of engagement of either 2 (FUS31-G10) or 3 of the RBDs (FUS231-P24) in a single S trimer by the multivalent minibinders."；并对关键界面另做 focused classification + local refinement 拿到 2.9 Å："Starting from the TRI2-2/S6P cryoEM data, we improved the RBD/MON2 densities using focused classification and local refinement, yielding a map at 2.9 Å resolution enabling visualization of the interactions formed by MON2 with the RBD"。整体三条结构 "The cryoEM structures of the TRI2-2, FUS31-G10, and the FUS231-P24 constructs in complex with S6P were determined at resolutions of 2.8, 4.6, and 3.9 Å respectively"。
   **代价**：FUS 类"到底几个 RBD 被一个分子占住"没被直接证明，属推断。
6. **亲和力提升后，"能不能被病毒逃逸"变成新的问题**。他们做的是正向逃逸筛选而不是只看变异表型："Plaque assays were performed with a VSV-SARS-CoV-2 S chimera on Vero CCL-81 cells with minibinders included in the overlay to halt spread of non-resistant viruses."；对照有效（2B04 "resulted in multiple escape mutants in each plate similar to previously reported escape mutants"），而 "In contrast, for both FUS231-P12 and TRI2-2, escape mutants were not isolated in 36 replicate wells for each protein"。
   **应对**：把"0 个逃逸"换算成覆盖率，避免读者把阴性结果当成证明："we estimated ( table S5 ) that, for the multivalent minibinders, the screened pool of viral mutants contains a large fraction of the possible single amino acid substitutions (34% to 88%) and a small fraction of the possible double amino acid substitutions (0.4% to 9.6%) within the region of the RBD that contacts the minibinders"，据此只敢给一个下限结论 "these findings indicate that at least two or more mutations in the RBD are likely necessary to escape binding of the multivalent minibinders"。
   **代价**：双突变覆盖率只有 0.4%–9.6%，也就是"没筛出来"里很大一部分是真没测到；这一点作者自己量化了，没含糊。
7. **多价不是万能，两个具体翻车点没有解释**：①对变异体点的耐药性不匀——"The two-domain fusions (FUS23 and FUS31) did not show improved binding to the tested point mutants."，并且三域融合体在高危突变组合上仍被拉快 "although E406W, Y453R, and the combination of K417N, E484K, and N501Y mutations (present in the B.1.351 S trimer) increased the dissociation rate more than 100-fold"；②FUS231 类对 Omicron 干脆打不满："except for the FUS231 proteins, which did not fully neutralize the B.1.1.529 variant in the tested concentration range"。
   **应对**：不做机理解释，改用**平行造多套几何**（TRI1/TRI2/TRI3 + FUS23/FUS31/FUS231 的矩阵）让"哪个靶能扛"由实验挑出来；最后收口在 TRI2（MON2 是 ACE2 拟态、靶位本身难变）："The TRI2 proteins maintained the strongest binding across all S trimer variants tested, likely because MON2 is an ACE2 mimic, similar to the recently reported S2K146 mAb"。**本文未解决**：E406W 对多价也仍然有效这一现象没有解释。
8. **体内端的数据不完整、也没做功效计算**："Substantial concentrations of TRI2-2 were detected in the lung lysate and serum 48 hours after administration ( fig. S19 ) but was too low for confident quantification in nasal turbinates after the first time point and for confident quantification in nasal washes at all time points."；且 "No sample-size calculations were performed to power each in vivo study."；作者自列局限还包括免疫原性未知："First, anti-drug antibodies are a concern with non-human proteins and, although MON1 and other minibinders ( 26 , 71 ) elicit little or no immune response, additional studies are required to determine the immunogenicity of the multivalent constructs."
   **应对**：治疗组里"哪个组织没降"照实写（鼻冲洗/脾脏部分未降），不裁数据；把药代与免疫原性推到 IND 前研究。**本文未解决**：给药部位暴露量、半衰期、免疫原性。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **计算侧（很薄，但很关键）**：沿用前作的 Rosetta 设计单价 minibinder（本文不重做）；本文的计算工作 = **几何组装设计**——用单价模块在结合态下"末端之间的距离"（要跨 RBD 的"开"与"闭"两种状态）来定 linker 长度范围，用 11 种寡聚化结构域定三价的空间排布。原文把它概括为 "In summary, our integration of structure-guided computational protein design, cell-free DNA assembly, cell-free expression, and a competition-based off-rate screen enabled the rapid design and optimization of S trimer-engaging multivalent minibinders."
- **实验漏斗侧（本文主力）**：CFPS（体外 DNA 装架 + PCR 线性模板 + 无细胞表达，6 h 出纯化蛋白，Echo 525 自动化）→ AlphaLISA 溶液竞争解离（off-rate）筛 → E. coli 重组表达 + **热处理纯化**（低成本路线验证）→ SPR/BLI 复测（正文与补充图 S13）→ 负染 EM 看交联 → cryoEM 定结合模式 → BRET 传感器（顺带的诊断读出）→ 假病毒/活病毒中和 → 人肾类器官 → VSV 嵌合逃逸筛选 → K18-hACE2 小鼠鼻内预防/治疗。
- **没有用的方法**：**MD、QM、自由能微扰、显式溶剂模拟，全篇没有**（这一点与 `sources/cao.md:455` 对曹组全部正文的字符串审计结论一致）。因此本文不能为"用模拟判催化/判结合"提供方法学依据。

### A. 设计与通量底座（Fig 1、图 S3-S5）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 前作单价设计 LCB1/AHB2/LCB3（本文称 MON1/MON2/MON3，表 S1 未取到） | 先做 RBD 位点饱和深变扫，找出会打掉单价结合的位点 | 正文口径：>10 倍（K417N）与 >100 倍（E406W、Y453K/R）亲和力下降即视为"会被逃逸" | 结论：三类单价都有可逃逸位点，构成后续多价化的动机 |
| A2 | 单价模块 | 建 CFPS 快速原型线：体外 DNA 装架 → PCR 线性表达模板 → 无细胞表达纯化 | 原文阈值口径："in as little as 6 hours"（装配到纯化蛋白），可放大到 mg 量 | 支撑 A3/A4 两个 >100 条的组合库 |
| A3 | MON1/2/3 + 11 种寡聚化结构域 × 多种 linker 长度 | 设计自组装均三聚体（TRI），CFPS 表达后测解离 | **"either 100-fold molar excess of untagged competitor (to prevent reassociation) or buffer was added"**；比"加竞争者/不加"两管的比例得解离分数 | **>100** 条均三聚体；**11 个寡聚化结构域中 9 个**至少出 1 条可用设计 |
| A4 | 同上 | 设计二域/三域融合体（FUS），比较 G（甘-丝）与 P（脯-丙-丝）linker 及不同域序 | linker 长度要覆盖 RBD 开/闭态下域末端距离（正文无数值阈值） | **>100** 条融合体 |
| A5 | A3/A4 的解离曲线 | 判"是否多价"：同一条构建体分别在单体 RBD 与三聚体 S6P 上测 | 判据是差值方向：三聚体上显著更慢 ⇒ 多价；"much larger effects were observed with dissociation from the S trimer than monomeric RBD, consistent with multivalent binding" | 头部表观 k_off ≤ ~1×10⁻⁷ s⁻¹（7 天不解离推得）；TRI2 相对单价改善 **>4 个数量级** |
| A6 | 可用结构域收窄 | 选 trimeric scaffold 继续 | 依据＝筛查结果 + 既往经验（正文未给显式阈值） | 取 SB175（domain 2）与 T4 foldon（domain 1） |

### B. 结构、诊断、逃逸与体内（Fig 2-6）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | TRI/FUS 头部构建体 + S6P | 负染 EM 先看形态 | 判据＝**是否交联/聚沉**（交联 ⇒ 跨两个 S 三聚体，假多价） | FUS31-G8、TRI1-5-G2 被判交联；TRI2-2、FUS231-G10、FUS231-P24、FUS31-G10 进入 B2 |
| B2 | B1 入选复合物 | cryoEM 结构解析（含 focused 3D classification + local refinement） | 判据＝能否分辨单价模块与界面；分辨率 2.8 / 4.6 / 3.9 Å，局部界面 2.9 Å | 3 条冷冻电镜结构 + 1 条负染重构；MON2 与设计模型主链 Ca RMSD **1.3 Å** |
| B3 | FUS231-P12 | 改装成 BRET 传感器（teLuc/mCyRFP3 挂两端），加 S2P 读数 | 判据＝三价同时结合把两端拉近 ⇒ BRET 上升；实测 590/470 nm 比值 **+350%**，检出限 **11 pM S2P**；单加 RBD 无此变化 | 顺带反证多价结合模式；诊断用途读出 |
| B4 | 头部多价构建体 × 变异 S6P（点突变 + Alpha/Beta/Gamma） | 竞争 AlphaLISA（24 h）+ ACE2 竞争 ELISA + SPR | 判据＝解离率变化 >100 倍记为"被该突变打掉" | TRI2 类对全部测试突变 24 h 内几乎不解离；FUS231 对 E406W/Y453R/B.1.351 组合 >100 倍加快 |
| B5 | 同一批构建体 | 假病毒 + 活病毒中和（含 Omicron、Delta、Iota 及嵌合株），加人肾类器官 | 判据＝IC50 是否落在测试浓度范围内；超范围记 N/A（假病毒 >50,000 pM、活病毒 >30,000 pM） | 头部候选保持 pM 级 IC50；FUS231 对 B.1.1.529 未打满 |
| B6 | TRI2-2、FUS231-P12、对照 2B04 | VSV-SARS-CoV-2 S 嵌合病毒斑块法逃逸筛选，抑制剂放 overlay | 判据＝出现能扩大的斑块＝逃逸；每药 **36 个独立孔** | 2B04 每板多个逃逸；两药 36 孔 0 逃逸；按表 S5 推算覆盖单突变 34%–88%、双突变 0.4%–9.6% ⇒ 只下"至少 2 个突变才能逃逸"的下限结论 |
| B7 | TRI2-1 / TRI2-2 | K18-hACE2 小鼠鼻内给药（预防 D-1 / 治疗 D+1），攻毒 10³ FFU | 判据＝体重下降是否被保护、6 dpi 各组织病毒载量 | 单次 **50 μg（约 2.5 mg/kg）**；n=6（两次独立实验），作者自述未做样本量功效计算 |
| B8 | TRI2-2 | 定量竞争 ELISA 测鼻内给药后暴露 | 判据＝能否可靠定量 | 肺裂解液与血清 48 h 可测；鼻甲/鼻冲洗液定量失败（作者明写） |

**这套流程的骨架值得单独记住**：当计算侧判据不够强（单价打不出高亲和力/易逃逸）时，他们的做法**不是加一道更贵的计算筛子**，而是①换一个能表征目标效应的物理量（亲和力→解离速率）；②把候选空间限制在"几何可行"里（用结构域末端距离定 linker），剩下的交给便宜的实验通量（CFPS 6 h）；③给漏斗加**正交的形态学判据**（负染 EM 交联）来识别"指标好看但机理不对"的假阳性。

## 4. 关键数字台账（全部来自本地全文）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 23 pM（LCB1）– 15 nM（AHB2） | 前作单价 minibinder 的活病毒 IC50 跨度 | "in the range of 23 pM (LCB1) to 15 nM (AHB2)" |
| 75 残基 | AHB2（MON2）单价模块长度 | "a homo-trimeric version of the 75-residue angiotensin converting enzyme 2 (ACE2) mimic AHB2 (TRI2-2)" |
| >100 倍 / >10 倍 | K417N、E406W、Y453K/R 对单价亲和力的影响 | "the widely observed K417N mutation results in a greater than 10-fold reduction in affinity and the E406W and Y453K/R mutations result in a greater than 100-fold reduction in affinity" |
| 100 倍 | 竞争解离实验里未标记 competitor 的过量倍数 | "either 100-fold molar excess of untagged competitor (to prevent reassociation) or buffer was added" |
| 6 小时 | CFPS：合成基因 → 装配 → 表达 → 纯化蛋白 | "generation of purified protein in as little as 6 hours" |
| Echo 525 | 自动化声驱动液体处理（高通量支撑） | "is compatible with high-throughput, automated experimentation using an acoustic liquid handler (Echo 525)" |
| >100 + >100 | 均三聚体库与融合体库各筛这么多（CFPS） | "We designed and screened more than 100 different homotrimeric minibinders"；"We screened more than 100 different fusions using the CFPS workflow" |
| 11 → 9 | 寡聚化结构域测试数 → 至少出一条可用设计的结构域数 | "we tested eleven different oligomerization domains and found that nine of these domains yielded at least one design with a linker length that improved dissociation rates" |
| 7 天 / ~1×10⁻⁷ s⁻¹ | 头部构建体对 S 三聚体的观察时长与推得表观解离速率上限 | "The top binders exhibited little to no dissociation from S trimer after 7 days of incubation with competitor"（速率数值正文以 "1×10" 上标形式给出，本卡不复述上标串） |
| >4 个数量级 | TRI2 相对单价解离速率的改善 | "more than four orders of magnitude for the TRI2 proteins, over the dissociation rate constants of the corresponding monomeric minibinders" |
| 2.8 / 4.6 / 3.9 Å；2.9 Å | TRI2-2、FUS31-G10、FUS231-P24 复合物分辨率；界面局部精修分辨率 | "were determined at resolutions of 2.8, 4.6, and 3.9 Å respectively"；"yielding a map at 2.9 Å resolution" |
| 1.3 Å | MON2 设计模型 vs cryoEM 结构主链 Ca RMSD | "closely matched the design model with backbone Ca RMSD of 1.3 Å" |
| +350%；11 pM | BRET 传感器响应幅度与 S2P 检出限 | "we observed a 350% increase in the 590 nm:470 nm BRET ratio"；"determined the limit of detection to be 11 pM S2P" |
| 24 h / >100 倍 | 变异体竞争解离观察时长；E406W+Y453R+Beta 组合使 FUS231 解离加快倍数 | "the TRI2 designs showed little dissociation after 24 hours against any of the tested S trimer mutants"；"increased the dissociation rate more than 100-fold" |
| N/A：>50,000 pM / >30,000 pM | 图 4E/4F 里"未完全中和"的定义（超测试浓度范围） | "N/A indicates an IC 50 value above the tested concentration range and an IC 50 greater than 50,000 pM"；活病毒阈值同句为 30,000 pM |
| 36 孔 / 0 个 | 每条药的逃逸筛选重复孔数与逃逸体数量 | "escape mutants were not isolated in 36 replicate wells for each protein" |
| 34%–88% / 0.4%–9.6% | 筛查池覆盖的单氨基酸置换比例 / 双置换比例 | "contains a large fraction of the possible single amino acid substitutions (34% to 88%) and a small fraction of the possible double amino acid substitutions (0.4% to 9.6%)" |
| ≥2 个突变 | 由覆盖率推出的"逃逸所需最少突变数"下限 | "at least two or more mutations in the RBD are likely necessary to escape binding of the multivalent minibinders" |
| 50 μg ≈ 2.5 mg/kg；10³ FFU；n=6；6 dpi | 小鼠鼻内单次剂量、攻毒量、每组动物数、取材时点 | "a single 50 μg dose (about 2.5 mg/kg) of TRI2-1 or TRI2-2 was administered directly to the nasal cavity (intranasal administration) one day prior to inoculation"；图 6 图注 n = 6、6 dpi |
| 0.3 μM | 肾类器官中和实验用药浓度 | "Replicating authentic B.1.351 virus in the presence of minibinder constructs (0.3 μM) was quantified in human kidney organoids" |
| P < 0.05 | 统计显著性口径（全部非参数检验） | "Statistical significance was determined by a P value < 0.05 using GraphPad Prism 9 software"；"Only non-parametric tests were used throughout this article" |
| 11 篇结构沉积 | PDB 7UHC / 7UHB；EMDB EMD-26507 至 26512 | 数据可用性段（正文原句列举，未逐字引） |

## 5. 结论——作者说了什么

1. 两条多价路线（自组装均三聚体 TRI、多域融合体 FUS）都比单价对照"结合更牢、中和更广、更难被逃逸"："Both strategies for generating multivalent S protein binders from miniproteins, self-assembling homotrimers (TRI) and multi-domain fusions (FUS), yielded designs with improved affinity, neutralization of current and historical VOCs, and resistance to escape mutants over their monovalent counterparts"。
2. **TRI2（AHB2 的均三聚体）是最好的**：对包括 Omicron、Delta 在内的全部测试变异体保持强效中和；"TRI2-2 neutralized Omicron (B.1.1.529), Delta (B.1.617.2), and all other variants tested with greater potency than that of monoclonal antibodies used clinically for the treatment of COVID-19"；且"按质量计"强于当时获批 mAb。
3. 机制解释落在"三价 + 受体拟态"："This combination of trivalency and receptor mimicry could be a useful general approach for combating viral escape and antigenic drift"。
4. 结构层面：设计与实验一致（TRI2 在 S 顶端形成 tripod，同时抓三个 RBD；MON2 与设计模型 1.3 Å）。
5. 顺带交付一个诊断读出（FUS231-based BRET 传感器）与一条低成本纯化路线（热处理）。
6. 体内：鼻内给药在 K18-hACE2 小鼠上同时给出预防与治疗保护，多数组织病毒载量下降。
7. 作者自限：免疫原性未测、给药途径/分布需再评估、长期毒性与稳定性未测；"These efforts will address limitations in our current study."

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的"漏斗"本质是实验通量漏斗，不是计算判据漏斗**。计算只提供"几何可行域"（linker 长度要跨过开/闭态末端距离），其余交给 6 小时一轮的 CFPS。→ 对我们：当计算判据无法保证机制正确时，把预算搬到"每轮能做多少个可判读实验"上，可能比把判据做复杂更划算；但前提是实验读数本身能表征目标事件（见第 3 条）。
2. **"换指标"比"调阈值"更有效**。他们从平衡亲和力换到解离速率，是因为要考察的效应（多价重结合）在旧指标里不可见。→ 对应我们的教训：如果 UAA 的真实目标是"三步化学事件是否发生"，那么用"结合得分"排序候选就是错的指标，必须换成能区分 S0/S1/S2 化学事件的读数（产物身份/同位素掺入），而不是把结合阈值调得更严。
3. **他们给自己加了一道"正交假阳性判据"**（负染 EM 看交联）：off-rate 好看但机理是跨两个 S 三聚体的构建体被剔掉。→ 我们的等价物必须是"能识别机制来源"的正交实验（失活突变对照、底物竞争、无酶/无底物空白），而不是第二个能量分数。
4. **阴性结果的定量化是这篇最可复用的写作纪律**：0 个逃逸不直接说"不会逃逸"，而换算成覆盖率区间，再只下"至少 2 个突变"的下限结论。→ 我们报告"某判据没命中/某候选没产物"时，应同样给出被筛池的实际覆盖度。
5. **"多价化是补救，不是能力"**：作者从没声称计算能预测哪个组合会成；他们靠把设计空间限制到"几何合理"再大量实测。这提醒我们：任何"命中率提升"若来自扩大实验量而非判据改进，引用时只能引**结构**，不能当**预测能力**。
6. 他们没做 MD/QM/自由能，所以本文对"用物理模拟判催化"既不提供支持也不提供反证；它提供的是"实验通量优先"这一条路线的完整落地细节。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者自述（正文原句）：①免疫原性未知（见第 2.8 条）；②给药方式与人体上呼吸道分布需重做；③长期稳定性/毒性未测。此外作者明确写未做样本量功效计算、动物未设盲（"Animal caretakers and researchers were not blinded to the study groups or during the assessment of the outcomes."）。
- 我们读出：①**全部定量表（亲和力数值、构建体命名表、escape 概率推算）都在未取到的补充材料里**，正文只给方向与数量级，任何具体 pM/nM 数值都不应从本卡引用为"最好值"；②判据是**表观解离速率**，7 天"几乎不解离"意味着测到的是量程边界而非真实速率，跨构建体比较时分辨率有限；③FUS 类的"单个分子占住几个 RBD"没有被结构直接证明（作者承认分辨率不足）；④多价化在 B.1.351 的 E406W 组合上仍被拉快 >100 倍，说明"组装换亲和力"对某些位点无效，本文未解释；⑤深变扫只覆盖单价（MON1/MON2）逃逸谱，多价构建体的逃逸谱靠斑块法阴性推断；⑥小鼠模型（K18-hACE2、高剂量攻毒 10³ FFU）与人体感染部位差异是作者自述的适用性限制。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"表观速率指标 + 加过量未标记竞争物"这一类读数设计**：UAA 反应筛选同样需要一个"能区分真催化与表面结合/吸附"的读数；做法是把我们的产物检测改成"竞争/稀释后是否仍可检出"的形式（稀释到无信号 vs 保持信号），从而把非特异吸附从命中里剔除。
2. **正交形态/机制判据（负染 EM 那道关）→ 我们加"失活对照 + 无底物/无酶对照 + 竞争底物"**：每一个通过化学读数的候选必须同时给出机制证据，否则记 UNKNOWN，而不是只报分数。
3. **"便宜通量当漏斗主力"的成本账**：先测"一轮能做完多少个可判读实验"（我们：一轮、最多四个构建体），再决定是否值得上昂贵计算——这正是 B09 的"通过率÷单价"口径的实验侧对应物。
4. **几何/结构约束代替打分阈值**：当我们对催化几何只能给"必须满足的刚性距离/角度条件"时，应像本文一样把它当**空间可行性过滤**（只用于缩小构建空间），而不是当"会不会催化"的判据。
5. **阴性结果换算覆盖率再下结论**：0 命中时报告"测了多少、覆盖了什么、因此只能说至少需要几步改动"。

**不可迁移（为什么不能照搬）**

1. **这里的"命中"是结合/中和/体内保护，不是催化**。TRI/FUS 的成功判据是"表观 k_off 更慢 + 病毒被中和"，完全没有化学转化事件。UAA 的目标是"生成新化学键/新产物"，**结合再好也不会自己产生 UTP→pppUA 的转化**。因此 9/11 这个"结构域可用率"绝不能被引用成"某组装策略对酶的成功率"。
2. **pM 级亲和力提升不可当作酶活上限的推断**。作者把 100 倍亲和力损失仍在治疗区间当作多价化的理论依据，这是**结合热力学 + 药代**的论证；酶活要看 kcat/Km 与副产物竞争，二者无对应关系。
3. **无细胞表达高通量（6 h、Echo 525）不能等价搬到我们的产物化学**：我们的读出是 LC-MS/MS 单样品时间，通量提升不来自表达端；照搬只会把预算错配到表达环节。
4. **本文不含 MD/QM/自由能**，因此它不能用来支持或反驳"物理模拟能判催化"；引用它时只许引用漏斗结构与实验设计，不许引用命中率或计算精度。
5. **SARS-CoV-2 变异体逃逸逻辑（受体拟态位点天然难变）在 UAA 里没有对应物**：我们面对的不是病毒突变压力，不能用"靶点不易变异 ⇒ 耐受性高"这类论证替代机制验证。

## 9. 溯源与自检

- 本地纯文本：`data/literature_cards/fulltext/C06_PMC9258422_text.txt`（Europe PMC fullTextXML 去标签、HTML 实体解码、引号/破折号归一，未改写内容）。
- 引句底稿: data/literature_cards/fulltext/C06_PMC9258422_text.txt（本卡全部英文引句一律从这一份逐字复制；另一份同源 XML 与登记底稿 `sources/cao.md` 见 `sources_map.json`）。
- 阅读定位方式：用一次性脚本把归一化的单行全文按句切分（临时文件放在 `A:\AITEMP`，任务结束已清理，不留档），再分段精读；正文内容集中在句 51-340，句 341-829 为资助/致谢/参考文献（已确认正文级 Materials and Methods 细节不在本地全文中）。
- 对照底稿行号：`sources/cao.md:116-129`（原卡）；`sources/cao.md:412`（对比表 C06 行：>100 三聚体 + >100 融合体、9/11=81.8%）；`sources/cao.md:433`（C06 作为同期通量底座）；`sources/cao.md:455`（曹组全部正文的 MD/QM/FEP 字符串审计，本文归入"未见使用"）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only C06 --no-report`（输入：本目录 `*.md` + `fulltext/` + `sources_map.json`）把卡内所有不含中日韩字符、被直双引号包住的 ≥20 字符片段在登记底稿里做逐字查找；本轮结果见交付回报。
- **登记状态说明**：`data/literature_cards/sources_map.json` 现已为 C06 登记 `C06_PMC9258422_fullTextXML.xml` + `C06_PMC9258422_text.txt` + `sources/cao.md`，与 `inventory.json` 的 `local`/`records` 一致（本卡未改该文件、未跑 `--sync-map`；写卡过程中观察到该键已由并行流程补齐）。未改 CSV、未改 `sources/cao.md`、未改脚本。

<!--CSV回填
work_type=论文（转化/实验主导型；计算只提供几何约束）
target=SARS-CoV-2 刺突三聚体 S6P/RBD；把前作单价 minibinder LCB1(MON1)、AHB2(MON2)、LCB3(MON3) 组装成均三聚体 TRI 与二/三域融合体 FUS
backbone_generation=单价界面沿用前作 Rosetta 设计（本文不重做）；本文计算侧＝几何组装设计（11 种寡聚化结构域 × linker 种类 G/P × 长度，长度由结合态下域末端距离覆盖 RBD 开/闭态决定）+ PCR 线性模板/无细胞 DNA 装架
computational_filters=无打分函数阈值型筛选器；计算判据只有"结合态末端几何是否相容/能否同时够到三个 RBD"；实验闸口=CFPS 后 AlphaLISA 溶液竞争解离（off-rate）、RBD 与 S6P 双靶差值、负染 EM 交联判据、ACE2 竞争 ELISA、cryoEM 与设计模型比对、逃逸斑块筛选
thresholds=未标记 competitor 过量 100 倍；解离观察 24 h 与 7 d；表观 k_off ≤ ~1×10⁻⁷ s⁻¹（头部构建体 7 d 几乎不解离推得）；几何约束原文未给数值阈值；N/A 定义为 IC50 超出测试浓度范围（假病毒 >50,000 pM、活病毒 >30,000 pM）；统计显著性 P<0.05 且只用非参数检验；未做样本量功效计算
md_used=否
qm_used=否
experimental_methods=CFPS 无细胞表达（6 h 内装配+表达+纯化，Echo 525 自动化）→AlphaLISA 竞争解离筛→E. coli 表达+热处理纯化→SPR/BLI→负染 EM→cryoEM（含 focused 3D 分类与局部精修）→BRET 传感器→假病毒与活病毒中和→人肾类器官感染抑制→VSV-SARS-CoV-2 嵌合病毒逃逸斑块筛选（每药 36 孔）→K18-hACE2 小鼠鼻内预防/治疗+组织病毒载量 RT-qPCR
pipeline_counts=单价 MON1/2/3 → >100 条均三聚体 + >100 条融合体（CFPS 初筛）→ 11 个寡聚化结构域缩到 9 个可用（其中 domain 4、11 被判次优）→ 选 SB175 与 T4 foldon 两种三聚 scaffold → 头部候选进中和/逃逸（TRI2-2、FUS231-P12 等）→ 2 条进小鼠（TRI2-1、TRI2-2）；3 条 cryoEM 结构 + 1 条负染重构
hit_rate=结构域层面 9/11（作者口径：至少给出 1 条与头部解离速率相当的设计）；逃逸筛选 2 条药各 36 孔均 0 个逃逸（阳性对照 2B04 每板多个）；TRI2 对全部测试变异体（含 B.1.1.7、Wash-B.1.351、Wash-P.1、B.1.617.2、B.1.1.529）保持 pM 级 IC50；FUS231 未能完全中和 B.1.1.529；小鼠预防组体重与病毒载量全面改善、治疗组部分组织（鼻冲洗/脾）未降
best_metric=未记录（本文正文只给数量级与图内趋势，绝对 KD/IC50 数值在图 4E-F 与未取到的表 S4/数据文件 S2-S3 中；正文可核的最强口径为"表观 k_off ≤ ~1×10⁻⁷ s⁻¹、TRI2 相对单价改善 >4 个数量级"）
cost_or_stat_note=CFPS 6 小时从基因到纯化蛋白；mg 量可放大；cryoEM 分辨率 2.8/4.6/3.9 Å、界面局部 2.9 Å；MON2 设计-实验主链 Ca RMSD 1.3 Å；小鼠单次 50 μg（~2.5 mg/kg）鼻内、攻毒 10³ FFU、n=6 两次独立实验；作者自述未做样本量功效计算、动物未盲；无计算成本记录（本文无 MD/QM）
role_in_timeline=曹龙兴组早期（2022，博后末期/西湖初）的"多价化补救"节点：当一价 de novo 设计亲和力与抗逃逸不足时，用几何组装 + 无细胞表达通量（而非更强的计算判据）换亲和力与广度；它是 binder 演进链上少见的"漏斗主力在实验侧"样本，也是后续 C11/C14 等体内功能工作的通量底座
source_pointer=data/literature_cards/fulltext/C06_PMC9258422_text.txt（SHA 26d26abf05bf311a…）+ C06_PMC9258422_fullTextXML.xml；sources/cao.md:116-129、412、455
CSV回填-->
