# [B31] 一个设计蛋白家族同时覆盖六种小分子的结合与感应——漏斗判据、命中分母与"结合≠感应"的处理

Lee G R, Pellock S J, Norn C, Tischer D, Dauparas J, Anishchenko I, … Yeh A H-W, Baker D（华盛顿大学 IPD + UCSC + Broad）
Nature Communications 2026, 17:503853 · DOI 10.1038/s41467-026-70953-8 · PMID 41904144 · PMCID PMC13194776
开放获取（CC BY 4.0）· https://pmc.ncbi.nlm.nih.gov/articles/PMC13194776/ · 预印本前身 bioRxiv 10.1101/2023.11.01.565201

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B31**（组：Baker组） |
| 本卡实际写作用底稿 | `data/interim/baker_lit/ft/smallmol_family2026.txt`（89,988 B 去标签纯文本；文件头身份块含 PMC13194776、PMID 41904144、DOI 10.1038/s41467-026-70953-8、Nat Commun，与 CSV 行号/DOI 逐项对上） |
| 同编号另一登记底稿 | `data/interim/claim_lit/PMC13194776.xml`（原始 fullTextXML；门禁只读非 .xml 底稿，本卡引句一律照上份 txt 复制） |
| 对照记录 | `sources/baker.md` 的 [B31] 段 |
| 证据级别 | **全文级**（本卡全部引句在登记 txt 里逐字命中，见 §9） |
| 未取到的部分 | Supplementary Figs 1–15/20、Supplementary Tables 1–6、Source Data、图内数值。凡正文只写"见补充"而没给数字的地方，本卡明写"正文未给出阈值（在 Supplementary Table 1）" |

## 1. 这篇到底解决什么（大白话）

Baker 组问的是一个**家族级**问题：同一个可设计骨架族（NTF2 折叠，天然就是"一个大口袋包小分子"的特权折叠），能不能一次性覆盖**六种化学上互不相干的小分子**（皮质醇 HCY、华法林 WRF、罗库溴铵 ROC、阿哌沙班 APX、SN-38/IRI、17α-羟孕酮 OHP），而且不止结合——能不能再升级成**感应器**。做法是三步：(1) 用深度学习幻觉 + 参数化生成把 NTF2 扩成 10,000+ 个口袋几何各异的骨架族（Set 1/2/3）；(2) 同一套漏斗（RIFdock 装配体 + Rosetta/LigandMPNN 出序列 + Rosetta 与 AF2 度量过滤）对六个靶各下一单，下单规模 630–19,390 条/靶；(3) 湿实验（酵母展示 + FACS + 深度测序）当主力筛子，命中 1–117 条/靶，纯化测到 K_D 高 nM–低 µM；最后把皮质醇结合体 hcy129 进化成 hcy129.1（K_D 68 nM），再在它的基础上设计**皮质醇依赖的异源二聚体**（CID），接到 NanoBiT 荧光素酶上做出 EC 50 72 nM 的基因编码感应器。**对我们最像的一条**：他们全程把"能结合"和"能输出功能信号"当成两个**分开证明**的事件——结合用 ITC/FP/BLI 证明，功能用"有配体/无配体两条件对比"证明，两者的判据完全不同。

## 2. 遇到的难点，以及遇到问题时他们做了什么

1. **极性界面难做：口袋里的极性残基会破坏折叠**。原文定位为核心难题："Designing polar interfaces remains an outstanding challenge in protein design"，并解释机理："an internal pocket with polar residues is needed to interact with polar functional groups of a ligand without destabilizing the protein fold"。 **他们做了什么**：两条并行设计路线——approach 1 把 Set 1 骨架里**预装的氢键网络 HBNet** 当极性锚点，"required that at least one protein"配体相互作用由 HBNet 残基介导（biased RIFdock 强制该氢键对）；approach 2 直接换用在小分子-蛋白复合物上训练过的 LigandMPNN 出序列（"we reason that the recently developed LigandMPNN, a deep learning model for protein sequence design trained on protein-small molecule complexes, can generate protein-ligand interactions more effectively than previous approaches"）。 **应对后仍留下的代价**：SSM 回验显示设计的氢键确实高度保守（"Overall, analysis of the SSMs revealed high conservation of the designed protein-ligand interactions, including key hydrogen bond and hydrophobic interactions"），但亲和力天花板仍只到高 nM/低 µM。
2. **同一个族对六个靶的命中率极不均衡，且"像天然 KSI 配体"才容易成**。六个靶下单 630–19,390 条不等，NGS 去重命中却是 1/46/19/8/8/117 条；回顾分析发现功能设计的骨架几乎都落在天然类固醇异构酶 KSI 附近："the backbone structures leading to functional designs closely resembled native KSI structures"，Discussion 也承认 "Notably, many of the high-affinity binders we generated targeted ligands with chemical similarity to those recognized by the NTF2-fold ketosteroid isomerase family." **他们做了什么**：用 TM-score + MDS 做结构距离回顾分析（28 个天然 KSI 复合物结构 vs 三个 Set），把"族覆盖广"降级为"实际有效子集窄"；但没有解决——本文未给出如何让偏离天然构象空间的 Set 3 骨架也出功能设计。
3. **结合富集第一名的设计反而折叠最差（roc22182：排序信号≠可开发性）**。原文："For rocuronium, the most enriched hit identified by yeast display showed poor folding by SEC"。 **他们做了什么**：(a) SSM 找有利突变；(b) AlphaFold multimer 预测识别出一个会形成二聚、"likely precludes binding to rocuronium" 的突变；(c) 组合成 roc22182.1（九突变）——"Combining these mutations improved solubility and enabled characterization of binding"。 **应对后仍留下的代价**：溶解度修好、结合测到，但化学计量仍然坏："the binding stoichiometry observed for roc22182.1 was very low (approximately 1:10)"，作者自收："This suggests that binding behavior remains suboptimal, possibly due to residual aggregation of the protein or ligand, or cooperativity effects."（本文未解决，只归因。）
4. **结合但不特异：ohp1952 与 albumin 对照**。为 OHP 设计的结合体同时紧绑皮质醇："ohp1952, which was designed to bind 17α-hydroxyprogesterone (OHP), exhibited tight binding to the ligand cortisol (HCY) as well, indicating low target specificity"；WRF 结合体 wrf1071 与血清白蛋白的非特异结合同处 µM 量级："albumin exhibited a micromolar-range binding affinity to WRF-TAMRA (K D 5.0 µM), which is in a similar range to that of the binder wrf1071 (K D 1.1 µM)"。 **他们做了什么**：加 albumin 作"万能疏水粘合剂"阴性对照；做六结合体 × 六配体 all-by-all 交叉矩阵（"The designed binders showed preferential binding to their cognate targets, whereas albumin exhibited no binding to the target ligands HCY, IRI, APX, and ROC, and weak binding to OHP"）；对测不出的弱相互作用统一记 10 mM 上限（"When the K D value could not be estimated due to weak or no ligand binding, the lowest binding affinity value of 10 mM was assigned"）。 **代价**：作者明写 "further improvements in our design approach are necessary to enhance specificity and sensitivity, especially regarding targets with chemical similarities (such as HCY and OHP), and hydrophobic ligands (such as WRF)"。
5. **结合但不感应：功能化要靠第二个判据、第二次筛选**。全篇最关键的结构性先决条件是配体结合模式必须**露出半个配体**才能往上盖 CID："The binding mode of cortisol in the hcy129.1 leaves part of its structure exposed"——这不是亲和力判据，是"能不能长出感应功能"的几何判据。 **他们做了什么**：CID 湿筛直接用**两条件对照流式**做闸门——分别测"仅 biotinylated hcy129.1_CID"与 hcy129.1_CID 加 1 µM 皮质醇 两种条件，收的是**皮质醇依赖的结合增强**而不是结合本身（"Three million cells were collected after applying the gate shown in Supplementary Fig. 12A from the library that was incubated with 1uM cortisol"）；再独立验证三元复合物（SEC 位移 + native MS）与功能输出（NanoBiT 发光，"titrated them with cortisol, which generated a luminescent signal with an estimated EC 50 of 72 nM"），并补测无配体态背景："which revealed an estimated K D of >5 μM"，即 "at least 2 orders of magnitude weaker than the EC 50 identified for cortisol-induced dimerization"。 **仍留下的**：感应器只区分到"响应皮质醇/可的松/OHP、不响应 corticosterone"（"The sensor responded to cortisol, cortisone, and OHP, but not to corticosterone."），归因为 "This lack of response is likely due to the absence of a hydroxyl group at the 17-position carbon in corticosterone, which is essential for a key polar interaction in our design model"；11 位取代根本未设计相互作用，交叉响应消不掉，作者写 "further redesign and method development will be required to enhance the designed sensors' sensitivity and specificity"（本文未解决）。
6. **计算漏斗本身判不动，判别主力被压到湿实验**。计算侧过滤只用较松的 Rosetta/AF2 度量组合，具体选择阈值正文未给出（登记在 Supplementary Table 1）；下单规模因此被迫保持万级："After filtering, we obtained oligonucleotides encoding the binders for experimental characterization, including 630 for HCY, 1661 for ROC, 16,276 for WRF, 9024 for APX, 19,390 for IRI, and 7573 for OHP"（六靶合计 51,554 条）。作者自己对比："the success rate of high-affinity binder designs in our approach was lower than alternative methods utilizing the four-helical bundles"，并把缺口写成 "the need to develop methods capable of designing scaffolds to accommodate a broader range of targets" 与 "accurately predicting binding prior to experimental validation"。 **应对**：不假装计算侧已解决——用 YSD+NGS 大通量兜底；计算预判本身本文未解决。

## 3. 方法与工作流程（输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **骨架族生成**：family-wide hallucination（TrRosetta 幻觉 + NTF2 家族序列/几何约束，MCMC 优化，预装 HBNet）→ Set 1；幻觉骨架 + ProteinMPNN 重设计 + AF2 验证 → Set 2；Rosetta 参数化枚举（前作 Basanta 算法）+ 同样重设计验证 → Set 3。
- **配体侧**：ChemDraw → RDKit ETKDGv2 起构象；CSD 构象生成器补充采样；antechamber/xtb（approach 1 用）、MMFF + AIMnet 终最小化（approach 2 用）；openbabel → Rosetta 配体参数。
- **装配体对接**：RIFdock（Rotamer Interaction Field），approach 1 用 tuning_file 偏置强制指定"氨基酸类型–配体原子"氢键对，approach 2 无约束；CID 阶段 PatchDock 播种 + RIFdock 对接迷你蛋白库。
- **序列设计**：Rosetta FastDesign + NTF2 家族 PSSM（氢键残基冻结）；LigandMPNN（T=0.2，每输入 8 条，×3 轮 LigandMPNN+RosettaPackMin/FastRelax，配体中心基团–邻近 Cα 距离约束 10 Å 内、谐波 σ=0.5 Å）；ProteinMPNN（表面重设计做结晶、CID 阶段冻结距皮质醇 5 Å 内残基）。
- **计算过滤**：Rosetta ddG、contact molecular surface（CMS）、SASA、氢键数 nHb、按序列同一性聚类；AF2 单序列（model 4、10 recycles）plDDT/Cα RMSD/结合位点侧链 RMSD；GALigandDock 回接配体（all-atom RMSD <2 Å）；CID 阶段 AF2 initial-guess pAE_interaction 与 plDDT_binder。
- **实验侧**：ssDNA（Twist）→ qPCR 组装 → pETCON3 酵母表面展示；表达分选（anti-c-Myc-FITC）+ 结合分选（biotinylated ligand + SAPE），≥3 轮；MiSeq 深测序 + PEAR 合并，binding/expression 频率 log ratio 算富集因子；ITC（microcal PEAQ）、FP、BLI（Octet）；SEC + native MS；SSM/组合突变库；NanoBiT（SmBiT/LgBiT + DTZ）发光。
- **没有用的方法**：MD、QM/自由能微扰全程缺席（xtb/AIMnet 只用于**配体构象优化**，不是蛋白-配体结合自由能计算）。

### A. 家族构建 + 六靶结合体漏斗

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | NTF2-like 家族信息 | family-wide hallucination（HBNet 预装 + 原生上下文偏置设计） | 正文未给骨架层阈值 | Set 1: 1,615 scaffolds |
| A2 | 幻觉骨架 + Rosetta 参数化骨架 | ProteinMPNN 重设计（HBNet 固定/全重设计 × 极性偏置 on/off 四组合），AF2 单序列验证 | "Structures of resulting sequences were predicted by AlphaFold2 in single-sequence mode, using model 4 with 10 recycles, and structures with Cα RMSDs less than 1 Å compared to the original scaffold and an average plDDT greater than 92 were selected for docking." | Set 2: 3230 backbones；Set 3: 6838 backbones；"With a designed family of over 10,000 NTF2s with diverse pocket geometries in hand" |
| A3 | 六种配体 | 构象采样：Set1 路线选 ≤15 个构象；Set2/3 路线每配体 200 构象 → 聚类取最低能代表（"1, 26, and 4 cluster representatives with the lowest energy were selected respectively for OHP, APX, SN-38"） | 能量排序 + 人工挑选（Set1） | 每配体 1–26 个对接输入构象 |
| A4a | 配体 × Set 1（HCY/WRF/ROC/APX/IRI，approach 1） | biased RIFdock 把配体极性基团怼到 HBNet → Rosetta FastDesign + PSSM，氢键残基冻结 | 至少一条 HBNet 介导的蛋白-配体氢键（"required that at least one protein"）；Rosetta ddG/CMS/SASA/nHb + 序列同一性聚类挑单，**具体切点正文未给出（Supplementary Table 1）** | 并入 A5 下单数 |
| A4b | 配体 × Set 2/3（OHP/APX/IRI，approach 2） | 无约束 RIFdock → CMS 初筛 → LigandMPNN（"Eight sequences were generated with temperature T = 0.2 per input"）×3 轮 + PackMin/FastRelax → Rosetta 指标 + AF2 指标（plDDT/Cα RMSD/侧链 RMSD，切点正文未给出）→ GALigandDock 换构象（"the docking solutions with ligand all-atom RMSD lower than 2 Å were used as inputs for the next iterative round of sequence design"）→ 二轮设计终选 | 同上 | 并入 A5 下单数 |
| A5 | 两路 designs 合并 | 过滤后下单合成 ssDNA | — | HCY 630 / ROC 1,661 / WRF 16,276 / APX 9,024 / IRI 19,390 / OHP 7,573（"After filtering, we obtained oligonucleotides encoding the binders for experimental characterization, including 630 for HCY, 1661 for ROC, 16,276 for WRF, 9024 for APX, 19,390 for IRI, and 7573 for OHP"；合计 51,554） |
| A6 | 酵母展示库 | "Binding screens were performed with yeast surface display coupled to fluorescence-activated cell sorting (FACS)"：先表达分选，再生物素化配体 + SAPE 结合分选，"this same process was repeated for at least two more rounds of sorting" | 每轮配体/SAPE 浓度逐 sort 调整（"The concentrations of the biotinylated ligand and SAPE were chosen differently for each sort"，具体浓度在 Supplementary Fig. 3，正文未给统一阈值） | "Binding signal was detected for all six targets and significant enrichment was observed after multiple rounds of sorting" |
| A7 | 终分选群体 | MiSeq 深测序，binding 频率/expression 频率 log ratio 富集分析 | 以 unique 序列计 hit | "Deep sequencing of the final sorted populations revealed 1, 46, 19, 8, 8, and 117 unique hits for HCY, WRF, ROC, APX, IRI, and OHP, respectively."（**命中分母 = 51,554 条下单设计，总命中 199 条**；HCY 命中率 1/630，OHP 117/7,573 ≈ 1.5%） |
| A8 | 富集因子最高的候选（每靶 1/7/5/5/7/8 条） | E. coli 表达 + 纯化 | SEC 单体峰 | "All selected designs displayed some level of expression and 23 of 33 showed distinct monodisperse peaks by size-exclusion chromatography (SEC)" |
| A9 | 纯化蛋白（每靶 1/2/1/4/2/4 条） | ITC / FP / BLI 测 K_D（FP/BLI 用氟基团或生物素修饰配体） | 单体 SEC 峰位置≈设计分子量的倾向更高亲和 | "the K D of the highest affinity binders across all targets ranged from low micromolar to high nanomolar" |
| A10 | 命中设计 | AF2/Rosetta 度量回看 + SSM 界面保守性 + 双结晶结构 | "AF2 metrics for the identified hits revealed high confidence (pLDDTs ranging from 86.0 to 95.0) and accuracy (Cα RMSDs less than 2.0 Å)"；Rosetta "target median ddG <−30"、"target median CMS >240"（此三项是**命中者回顾读数**，不是下单前的切点） | hcy129_mpnn5·cortisol 1.5 Å："Structural alignment of the crystal structure to the design model revealed a Cα RMSD of 1.1 Å over 120 residues"；apx1049·apixaban 2.1 Å："The structure shows sub-angstrom agreement to the design model with Cα RMSD of 0.6 Å over 113 residues"（PDB 8UQF/8VFQ/8VEZ） |

### B. 从结合体到感应器（皮质醇 CID 漏斗）——每一步都是新判据，不是把 A 段阈值复用

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | hcy129（原始设计） | SSM → 取有利突变做组合突变库（IDT eblocks + Golden Gate，酵母展示再筛） | "To improve the binding affinity of hcy129 for use as a cortisol biosensor, we screened a library of combinatorial mutants based on favorable mutations identified from the SSM of hcy129" | hcy129.1："This variant, hcy129.1, displayed a K D of 68 nM, a 31-fold improvement in affinity compared to the original design"（达标依据：生理浓度口径，"diseases such as Cushing's syndrome can be diagnosed when the plasma cortisol level is higher than 38 nM"） |
| B2 | hcy129.1·cortisol AF2+GALigandDock 模型 | 几何先决检查：配体是否外露（"The binding mode of cortisol in the hcy129.1 leaves part of its structure exposed"）→ 口袋开口表面重设计（ProteinMPNN T=0.1，排除 Cys，AF2 验证 Cα RMSD<1 Å、plDDT>90、结合残基 rotamer 保留）→ 得 hcy129.1_CID（R43I/R95Q/Q128L） | 外露 + 表面重塑不伤界面 | 三元复合物设计靶 |
| B3 | hcy129.1_CID-cortisol 复合物 × 迷你蛋白库（3 螺旋束库） | PatchDock 播种 → RIFdock（对外露口袋残基**和配体原子**同时建 RIF）："was docked using RIFdock to yield around 5 million total docks" | "A preliminary 'predictor' design step was used to rank the in silico designs using Rosetta ddG and contact molecular surface in which 1 million docks were selected for the downstream Rosetta design" | 5,000,000 docks → 1,000,000 → FastDesign 优化三组分界面 → CMS/contact patch/ddG 过滤 → ProteinMPNN（"residues within 5 Å of the cortisol ligand were fixed"）→ "Finally, we ran Alphafold2 prediction with the initial guess protocol"，"the heterodimeric complexes were computationally selected with AlphaFold2 structure prediction applying cutoffs of pAE <10 and plDDT >85" → "the designs passing pae_interaction <10 and plDDT_binder > 85 were ordered as a synthetic oligo pool" |
| B4 | 60k 迷你结合体酵母展示库（"Yeast surface display library containing 60k designed minibinders was prepared as previously described"） | **两条件对照 FACS**：加/不加 1 µM 皮质醇测对 biotinylated hcy129.1_CID 的结合 | 收"皮质醇依赖富集"群体，单克隆复测两条件（0.2 µM ± 0.2 µM 皮质醇） | "Three million cells were collected after applying the gate shown in Supplementary Fig. 12A from the library that was incubated with 1uM cortisol" → 一个可用 mini binder：miniH11 |
| B5 | hcy129.1_CID + miniH11 | SEC 共洗脱位移（1 µM ± 10 µM 皮质醇）+ native MS（UniDec 去卷积）定三元复合物 | 有无配体的峰位移 + 分子量匹配 | 证实配体依赖异源二聚 |
| B6 | CID × NanoBiT 融合（SmBiT/LgBiT，各 200 nM + DTZ） | 皮质醇滴定发光曲线；再做无配体二聚背景滴定 | EC 50 对照 K_D；背景对照信号差 | "titrated them with cortisol, which generated a luminescent signal with an estimated EC 50 of 72 nM"；"which revealed an estimated K D of >5 μM"，"at least 2 orders of magnitude weaker than the EC 50 identified for cortisol-induced dimerization" |
| B7 | 传感器 | 结构近似配体面板（cortisone/corticosterone/OHP/WRF/ROC） | 响应谱与设计模型互洽 | "The sensor responded to cortisol, cortisone, and OHP, but not to corticosterone."（交叉响应与失响应都如实报告，未砍数据） |

**流程骨架小结**：家族（10k+ 骨架）→ 配体专属漏斗 ×6（计算松筛 → 万级下单 → 湿法大通量真筛）→ 命中者三级确认（SEC 折叠 → K_D → SSM/晶体）→ 功能升级另起炉灶（亲和力达标 ≠ 能感应，外露几何 + 二元对照筛选 + 独立读出三层各自设卡）。

## 4. 关键数字台账（数值 · 含义 · 出处）

| 数值 | 含义 | 出处 |
|---|---|---|
| 1,615 / 3230 / 6838 | Set 1（幻觉）/ Set 2（幻觉+MPNN+AF2）/ Set 3（Rosetta 参数化）骨架数；家族总数 over 10,000 | L7 结果段；Set 大小以正文原数为准（括注记法 Set 1: 1,615 scaffolds 等） |
| 6 个配体 | HCY(皮质醇)/WRF(华法林)/ROC(罗库溴铵)/APX(阿哌沙班)/IRI(SN-38)/OHP(17α-羟孕酮) | 结果段六靶列举 |
| 630 / 1,661 / 16,276 / 9,024 / 19,390 / 7,573 | 各靶过滤后下单（合成 ssDNA）设计数 | "After filtering, we obtained oligonucleotides encoding the binders for experimental characterization, including 630 for HCY, 1661 for ROC, 16,276 for WRF, 9024 for APX, 19,390 for IRI, and 7573 for OHP" |
| 51,554 | 六靶下单合计（**本卡求和**，非原文数字） | 上行加总 |
| 1 / 46 / 19 / 8 / 8 / 117 | 各靶 NGS 去重 unique 命中数（合计 199，本卡求和）＝命中分母口径 | "Deep sequencing of the final sorted populations revealed 1, 46, 19, 8, 8, and 117 unique hits for HCY, WRF, ROC, APX, IRI, and OHP, respectively." |
| 1 / 7 / 5 / 5 / 7 / 8 | 各靶送去纯化的富集因子最高候选数 | 富集挑选段（每靶列举） |
| 23 of 33 | 纯化候选中 SEC 单分散峰数 | "All selected designs displayed some level of expression and 23 of 33 showed distinct monodisperse peaks by size-exclusion chromatography (SEC)" |
| 1 / 2 / 1 / 4 / 2 / 4 | 各靶进入 K_D 测定的纯化蛋白数（合计 14，本卡求和） | K_D 测定段列举 |
| 高 nM – 低 µM | 各靶最佳 K_D 区间 | "the K D of the highest affinity binders across all targets ranged from low micromolar to high nanomolar" |
| 68 nM、31-fold | hcy129.1 对皮质醇 K_D 及相对原始设计的提升 | "This variant, hcy129.1, displayed a K D of 68 nM, a 31-fold improvement in affinity compared to the original design" |
| 38 nM | 皮质醇生理/临床参照（库欣综合征诊断界值，设定亲和力目标） | "diseases such as Cushing's syndrome can be diagnosed when the plasma cortisol level is higher than 38 nM" |
| 72 nM、>5 μM、2 个数量级 | NanoBiT 传感器 EC 50；无皮质醇时 CID 组分间 K_D；两者差距 | "estimated EC 50 of 72 nM" / "estimated K D of >5 μM" / "at least 2 orders of magnitude weaker than the EC 50 identified for cortisol-induced dimerization" |
| 1:10 | roc22182.1 实测结合化学计量（约值，原文 approximately） | "the binding stoichiometry observed for roc22182.1 was very low (approximately 1:10)" |
| 1.5–5.5-fold | iri807 SSM 组合突变 SN-38 K_D 改善幅度 | "the K D improvements of selected variants ranged from 1.5 to 5.5-fold based on FP using SN-38-TAMRA" |
| 5,000,000 → 1,000,000 → 60k → 3,000,000 细胞 | CID 漏斗：RIFdock 总对接 → predictor 排序入选 → AF2 闸口后下单寡核苷酸池 → 分选收细胞数 | "around 5 million total docks" / "1 million docks were selected for the downstream Rosetta design" / "the designs passing pae_interaction <10 and plDDT_binder > 85 were ordered as a synthetic oligo pool"（60k 库） / "Three million cells were collected" |
| Cα RMSD <1 Å、平均 plDDT >92、model 4、10 recycles | 骨架族 AF2 验证闸口 | "Structures of resulting sequences were predicted by AlphaFold2 in single-sequence mode, using model 4 with 10 recycles, and structures with Cα RMSDs less than 1 Å compared to the original scaffold and an average plDDT greater than 92 were selected for docking." |
| T = 0.2 × 8 条 × 3 轮；10 Å 邻域、σ 0.5 Å；RMSD <2 Å | LigandMPNN 采样温度与条数；配体距离约束范围/强度；GALigandDock 回接容差 | "Eight sequences were generated with temperature T = 0.2 per input" / 距离约束方法段 / "ligand all-atom RMSD lower than 2 Å" |
| ≤15；200；1 / 26 / 4 | 配体构象数：Set1 路线每配体≤15；Set2/3 路线每配体 200 采样；聚类代表（OHP/APX/SN-38） | "1, 26, and 4 cluster representatives with the lowest energy were selected respectively for OHP, APX, SN-38" |
| pAE <10、plDDT_binder >85 | CID 三元复合物 AF2 initial-guess 下单闸口 | "the heterodimeric complexes were computationally selected with AlphaFold2 structure prediction applying cutoffs of pAE <10 and plDDT >85" |
| pLDDT 86.0–95.0、Cα RMSD <2.0 Å、ddG <−30、CMS >240 | **命中者回顾读数**（不是下单前切点） | "AF2 metrics for the identified hits revealed high confidence (pLDDTs ranging from 86.0 to 95.0) and accuracy (Cα RMSDs less than 2.0 Å)"；"target median ddG <−30"；"target median CMS >240" |
| 1.5 Å / 1.1 Å / 120 残基；2.1 Å / 0.6 Å / 113 残基 | hcy129_mpnn5·cortisol 与 apx1049·apixaban 晶体分辨率与设计-RMSD | "Structural alignment of the crystal structure to the design model revealed a Cα RMSD of 1.1 Å over 120 residues" / "The structure shows sub-angstrom agreement to the design model with Cα RMSD of 0.6 Å over 113 residues"（PDB 8UQF、8VFQ、8VEZ） |
| 10 mM | 交叉反应矩阵中"测不出即记上限"的封顶值 | "When the K D value could not be estimated due to weak or no ligand binding, the lowest binding affinity value of 10 mM was assigned" |
| 5.0 µM vs 1.1 µM | 白蛋白与 wrf1071 对 WRF-TAMRA 的 K_D 对照 | "albumin exhibited a micromolar-range binding affinity to WRF-TAMRA (K D 5.0 µM), which is in a similar range to that of the binder wrf1071 (K D 1.1 µM)" |
| 153 条 | iri807 组合突变库经 AF2（plDDT > 90.0、Cα RMSD < 1.5 Å）挑选后下单数 | "153 sequences that yielded predictions with plDDT > 90.0 and Cα RMSD < 1.5 Å were chosen" |
| 26 → 7 | WRF 的 SSM 池 26 个候选富集后进入纯化的结合体数 | "For WRF, we pooled the SSM libraries of 26 potential hits from the yeast binding screening for further selection, and this led to selecting the 7 binders" |
| 28 | 回顾分析所用的天然 KSI-配体复合物结构数 | Methods MDS 段（KSI structures from the PDB，列于补充表） |
| ≥3 轮 | 酵母展示分选最少轮数 | "this same process was repeated for at least two more rounds of sorting"（表达轮+结合轮×≥2） |

## 5. 结论——作者说了什么

1. 深度学习骨架生成（幻觉/参数化）+ ProteinMPNN/LigandMPNN 序列设计 + AF2 结构过滤，可以让一个"特权折叠"家族（NTF2）在口袋几何空间内被充分采样，并对**六种不同小分子**都拿到功能结合体。
2. 同族的结合体可以升级为 CID 感应系统：hcy129.1（68 nM）→ hcy129.1_CID + miniH11 → NanoBiT 融合，EC 50 72 nM，无配体背景 K_D >5 μM，证明"设计的小分子结合体可以被改造成生物传感器"。
3. 界面设计精度获晶体结构支持：hcy129_mpnn5·cortisol Cα RMSD 1.1 Å（120 残基）、apx1049·apixaban 0.6 Å（113 残基），HBNet 介导的极性接触"按设计工作了"（"Notably, multiple polar interactions are mediated by a pre-installed HBNet unique to scaffold Set 1, demonstrating that this approach worked as intended to generate preorganized polar contacts"）。
4. 作者自限：高亲和力命中偏向与天然 KSI 配体化学相似的靶；本文方法的高亲和力成功率低于四螺旋束路线；特异性和灵敏度仍需方法与再设计改进；对 ROC 连化学计量都没修好。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **"结合"与"感应"被拆成三个正交事件分别设卡**：占据（K_D，ITC/FP/BLI）、几何可达（配体外露，"The binding mode of cortisol in the hcy129.1 leaves part of its structure exposed"）、依赖式输出（±配体两条件 FACS + NanoBiT 发光，与 apo 背景定量）。这正是我们区分"能结合底物"与"能生成目标产物"最该抄的结构：**结合亲合力永远不能替代产物读数**；"能结合底物"只回答第一卡，"能生成目标产物"必须有一个化学身份正交的终端读出（LC-MS/MS 产物），并且最好有"依赖 vs 独立"两条件对照（±底物/±供体），对应他们的 ±皮质醇。
2. **"结合但不感应/不特异"在他们手里是常态而非事故**：roc22182.1 结合但 1:10 化学计量、ohp1952 结合但交叉紧绑、wrf1071 结合但只与白蛋白同级、传感器对 cortisone/OHP 响应但对 corticosterone 不响应——他们的处理方式是**逐条如实分层报告 + 给出结构归因 + 声明未解决**，而不是砍掉或合并进"命中率"。我们给候选标分步化学事件事件时应当同样保留"结合位点正确但化学计量/输出不成立"这一档，不许让单一分数抹平。
3. **命中分母完全由计算判据的松紧决定，且逐靶漂移 3 个数量级**（HCY 1/630 到 OHP 117/7,573，命中率 0.16%→1.5%，本卡算）——同一个族、同一套漏斗，每靶下单规模却要先验地按靶定制（配体浓度、轮数、下单数都逐靶不同）。"家族方法"不等于均匀产出，任何跨靶平均命中率都是无意义数。
4. **富集排序第一≠可开发**（roc22182 折叠最差）：YSD 富集因子是"表观占据"排序，不是溶解度/化学计量/功能排序。我们若用单一代理指标（如对接分、pLDDT）排候选，终选必须留一个与排序指标正交的确认层（SEC 级=我们的表达/可溶层）。
5. **计算漏斗没长出来，判别主力外包给了湿实验**——这是"小分子方向漏斗仍不充分"的一手证据（正文自比四螺旋束、并明写需要 "accurately predicting binding prior to experimental validation"）。对我们的含义：**"有没有一个计算判据能提前判目标成键能力"这个问题，连 Baker 组在小分子结合这个更弱的问题上都没有答案**；不能指望从这类文献借到任何"计算闸口成功率"。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者明写：高亲和力成功率低于四螺旋束路线（"the success rate of high-affinity binder designs in our approach was lower than alternative methods utilizing the four-helical bundles"）；特异性/灵敏度需继续开发；ROC 结合行为 suboptimal（"This suggests that binding behavior remains suboptimal, possibly due to residual aggregation of the protein or ligand, or cooperativity effects."）；有效骨架坍缩到天然 KSI 相似区（"the backbone structures leading to functional designs closely resembled native KSI structures"）。
- 我们读出：① **计算下单切点几乎全部登记在 Supplementary Table 1，正文不可核验**——本文的"阈值"其实是两半：能复述的只有骨架 AF2（RMSD<1 Å、plDDT>92）和 CID 的 pAE_interaction<10/plDDT_binder>85；② 命中率没有统一分母口径（下单数≠设计生成数≠库容量，NGS unique hits 与富集挑选数混排叙述）；③ 交叉反应矩阵把测不出统一记 10 mM 是**删失数据**，热图会系统性夸大结合体与白蛋白的"差异感"；④ 传感器对 OHP 有响应，实质是"该阴性样本上的假阳性"，被叙述为选择性面板而非失败；⑤ SEC+native MS 只证明三元复合物**形成**，不证明结合耦合能量学；⑥ 全文无 MD、无 QM、无动力学（k_on/k_off 未报），机理层不能向本文引用。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **三卡正交协议**（占据 → 几何可达 → 依赖式输出）直接映射到我们：LC-MS/MS 证"能生成目标产物"是第三卡；第一卡（结合 UTP）过而不做第三卡，全族证据里就是 ohp1952/wrf1071 类"结合但无用"；两条件（±底物/±供体）FACS 的设计改成两条件（±UTP）产物对照即可。
2. **失败分层不归一**：折叠（SEC 23/33）、占据（K_D）、化学计量（1:10）、特异性（all-by-all）、输出（EC 50 vs apo K_D 差 2 个数量级）各有一张独立表。对齐我们本库的分步化学事件 + UNKNOWN/METHOD_FAIL 状态，一个候选只许在对应层失败，不许跨层冲销。
3. **"外露几何"作为功能化的先决筛**：我们的类比是"结合姿态必须把 α-磷酸/核糖留出来成键，而不是全包埋"——这是几何判据（可静态评估），不是自由能判据；把它从"结合亲和力"里拆出来单列。
4. **下单规模诚实记账**：他们把"计算判据松→必须下万级单"写进正文。我们任何漏斗报告都应带 分母=实际送测数、判据松紧=通过率 两列。

**不可迁移（为什么不能照搬）**

1. **pAE_interaction<10、plDDT_binder>85、ddG<−30、CMS>240 全是"结合/复合物自洽"度量**，没有一个含任何催化信息；本库判据明禁把 binder 阈值当酶活判据——本篇再次示范了即使全过这些闸口，也仍需万级湿筛才出一个 68 nM 结合体。
2. **68 nM / 72 nM / 199 命中 / 51,554 下单都不许换算成"酶设计成功概率"**：他们的标签是结合（静态、二元、酵母展示可测），我们连一个被产物化学确认的正样本都没有，无 A 段考卷（对照 B09 卡的教训）。
3. **酵母展示 + 生物素化配体的通量在酶化学上不存在**：产物鉴定是 LC-MS/MS 逐样品的，漏斗末端必须信息量最大化（机制多样性 + 失活对照 + ±底物对照），不能照抄"60k 库 + 收 300 万细胞"的样本数逻辑。
4. 本文**没有 MD/QM**，其为"用自由能/动力学判催化"不提供任何命中率或阈值参照。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/smallmol_family2026.txt

- 本卡全部引句从该 txt 复制粘贴。该文件是 PMC13194776 登记全文的去标签纯文本，文件头身份块复核通过（PMC13194776 / PMID 41904144 / DOI 10.1038/s41467-026-70953-8 / Nat Commun 2026，与 CSV B31 行一致）。同编号另登记的 `data/interim/claim_lit/PMC13194776.xml` 是原始 fullTextXML（门禁只读非 .xml 底稿，不参与逐字比对）；对照记录 `sources/baker.md` [B31] 段。
- 正文中"某数字在 Supplementary Fig./Table N"的说明均转述正文括注，补充图表本身未取回，凡依赖其阈值处本卡写明"正文未给出阈值"。
- CSV 字段映射：§3 ↔ 计算筛选判据/阈值数字/候选生成方法；§4 ↔ 候选数递减/实验命中率/Kd最好值/成本统计；§6/§8 ↔ 在方法演进链的位置。
- 门禁命令：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B31" --no-report`，本卡引句全数在登记 txt 逐字命中（见本轮运行输出）。

<!--CSV回填
work_type=论文
target=6 种小分子（皮质醇 HCY、华法林 WRF、罗库溴铵 ROC、阿哌沙班 APX、SN-38/IRI、17α-羟孕酮 OHP）+ 基于皮质醇结合体的 CID 生物传感器
backbone_generation=NTF2 家族：family-wide hallucination 预装 HBNet（Set 1，1,615）；幻觉骨架 ProteinMPNN 重设计+AF2 验证（Set 2，3230）；Rosetta 参数化枚举（Set 3，6838）；CID 用设计好的迷你蛋白/3 螺旋束库 × 三元复合物 RIFdock
computational_filters=biased/unconstrained RIFdock；Rosetta ddG、contact molecular surface、SASA、nHb、contact patch、序列同一性聚类；LigandMPNN 迭代（+PackMin/FastRelax，配体距离约束）；AF2 单序列 plDDT/Cα RMSD/结合位侧链 RMSD；GALigandDock 回接；CID 阶段 AF2 initial-guess 的 pAE_interaction 与 plDDT_binder
thresholds=骨架闸：AF2 model 4/10 recycles、Cα RMSD<1 Å、平均 plDDT>92；LigandMPNN T=0.2×8 条×3 轮、距离约束 10 Å 内 σ=0.5 Å；回接 all-atom RMSD<2 Å；CID 下单闸：pAE_interaction<10 且 plDDT_binder>85；命中回顾读数 ddG<−30、CMS>240、pLDDT 86.0–95.0、Cα RMSD<2.0 Å；主漏斗各靶下单切点正文未给出（在 Supplementary Table 1）
md_used=否（xtb/AIMnet 仅用于配体构象优化，无蛋白-配体分子动力学）
qm_used=否（无反应坐标/电子结构计算，配体最小化不构成对催化主张的 QM 证据）
experimental_methods=ssDNA 库→酵母表面展示→表达分选+生物素化配体/SAPE 结合分选（≥3 轮，逐 sort 调浓度）→MiSeq 深测序算富集因子→E. coli 表达+SEC→ITC/FP/BLI 测 K_D→SSM/组合突变库→晶体结构（8UQF、8VFQ、8VEZ）→SEC+native MS 验三元复合物→NanoBiT 发光测 EC 50
pipeline_counts=家族 10,000+ 骨架 → 六靶下单 630/1,661/16,276/9,024/19,390/7,573（合计 51,554，本卡加总）→ NGS unique 命中 1/46/19/8/8/117（合计 199）→ 送纯化 33 → SEC 单分散 23 → K_D 测定 14 → 结晶 2；CID：5,000,000 docks → 1,000,000 predictor 入选 → pAE<10/plDDT>85 → 60k 下单 → 收 3,000,000 细胞 → miniH11 一个
hit_rate=正文未给统一命中率；按本卡加总口径：命中/下单 从 1/630（HCY，0.16%）到 117/7,573（OHP，1.5%）；作者自述高亲和力成功率低于四螺旋束路线
best_metric=hcy129.1 对皮质醇 K_D 68 nM（31 倍于原始设计）；传感器 NanoBiT EC 50 72 nM（apo 背景 K_D>5 μM，差 2 个数量级）；apx1049 对阿哌沙班达纳摩尔段
cost_or_stat_note=未做样本量统计预设；无结合/测不出的 K_D 统一记 10 mM 上限（删失处理）；CID 收样 3×10^6 细胞/库；正文无计算成本口径
role_in_timeline=Baker 组把蛋白-蛋白方向验证过的 家族骨架+DL漏斗（Cao 2022/Bennett 2023 一脉）平移至小分子：同一 NTF2 族复用六靶并首次接出基因编码感应器；但漏斗仍不紧（下单停在万级、判别主力在湿实验、有效骨架坍缩回天然 KSI 相似区），与 binder 方向百级下单形成对照——印证小分子/极性界面的计算预判仍是未解问题
source_pointer=data/interim/baker_lit/ft/smallmol_family2026.txt（PMC13194776 fullTextXML 去标签文本，身份块已复核）+ data/interim/claim_lit/PMC13194776.xml + sources/baker.md [B31]
CSV回填-->
