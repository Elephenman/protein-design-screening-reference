# [B44] 把"选择性"当成设计目标而不是筛选结果——RGD 迷你蛋白同时打中 αvβ6 / αvβ8 的亚型与构象，一路做到吸入给药

Roy Anindya, Shi Lei, Chang Ashley, Dong X, … Cherf G, … Springer T, Van Ry P, Cochran J, Baker David（华盛顿大学 IPD + BYU + 波士顿儿童医院/哈佛 + Fred Hutch + Stanford + AstraZeneca 等，40 人）
Nature Communications 2023, 14:5660 · DOI 10.1038/s41467-023-41272-z · PMID 37704610 · PMCID PMC10500007
开放获取（CC BY 4.0）· 全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC10500007/ · 代码 https://github.com/aroy10/avb6-publication

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B44**（组：Baker组） |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory 记录 `fetch_channel=epmc_fulltext`，`fetch_url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10500007/fullTextXML`），2026-10-16 本地抓取 |
| 本地全文（本卡唯一逐字底稿） | `data/interim/baker_lit/ft/integrin_miniprot2023.txt`（120,718 B、121 行）；文件头身份块含 DOI `10.1038/s41467-023-41272-z`、PMCID 10500007、PMID 37704610，与本行一致，**不是挂错行的文件** |
| 登记底稿（门禁清单） | 上述全文 + `sources/baker.md`（本项目的原卡：`sources/baker.md:578–589`） |
| 证据级别 | **全文级**（本卡所有英文引句在该份本地全文里逐字命中，见第 9 节自检输出） |
| 未取到的部分 | Supplementary Figures 1–18、Supplementary Data 1–6、Source Data、Reporting Summary 均未本地化。凡序列全集、亲和力矩阵（Supplementary Table 1/2/3）、每组动物数、cryoEM 流程图只在正文/图注里被**指向**的地方，本卡明写"正文未给出，仅有正文描述" |
| 本卡相对原卡的补充 | 原卡把本文定位成"蛋白酶切割=构象筛选"，本卡补齐：设计漏斗的逐步递减数字、两轮设计的实际关系（第二轮用第一轮的**晶体结构**而不是模型对接）、冷冻电镜对设计构象的复核口径（残基对命中而非整体 RMSD）、以及五处正文/图注互相打架的数字（第 7 节） |

## 1. 这篇到底解决什么（大白话）

八个不同的整合素亚型共用同一个 RGD 结合位点，所以小分子做不出"只打一个亚型"的药；抗体要精细区分又得付出大量负向筛选。更难的是同一家药的**安全性**取决于把靶点锁在哪个构象上——锁在"弯-闭合"的抗体 BG00011 因病情加重和死亡事件被停掉，而稳定"伸展-开放"构象、诱导受体内吞的小分子在临床试验里没出现药相关严重不良事件。这篇做的事：不凭空造全新结合模式，而是把天然配体 L-TGF-β 上那段 RGD extended-turn 构象当"锚"，用 Rosetta 在整个 PDB 里找**能容纳这段构象又不与靶点撞骨架**的小折叠（α/β 铁氧还蛋白折叠，小于 75 个氨基酸）当支架；然后故意让支架上的环去接触 β6 与 β8 **彼此不一样**的两个区域（SDL2 上打包 LXX(L/I) 的 Tyr/Leu 位、以及 β 亚基 E316/K304 的电荷反转），把选择性写进设计意图，而不是指望从库里筛出来。之后走"酵母展示 + 蛋白酶切割加压 + 递减浓度分选 + 测序富集 + 饱和突变"做亲和成熟，用 BLI/细胞滴定点名测八种 RGD 整合素，用负染与冷冻电镜复核设计构象，最后把这个几十残基的蛋白雾化吸入，给药到小鼠肺纤维化模型，显著降低纤维化负荷并改善肺力学；同时在人肺类器官里给出方向一致的读数。作者的说法是："Here we describe a generalized method for computationally designing RGD-containing miniproteins selective for a single RGD integrin heterodimer and conformational state."

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **同家族选择性做不出来，而且光有选择性还不够，还得选对构象**（立项理由，作者原话）。小分子侧："share the conserved RGD binding sequence, it has not been possible to generate selective RGD-mimetic small molecules for individual integrins"；抗体侧的代价："This can be difficult to achieve with small molecules that share a conserved binding site, and the development of antibody panels capable of fine discrimination require considerable amounts of negative selection."。更狠的是构象维度："conformations (bent-closed, extended-closed, and extended-open) by orthosteric and allosteric inhibitors has dramatically different outcomes on receptor internalization"——锁定非内吞构象的抗体 "has been discontinued because it exacerbated disease at higher doses among other serious adverse effects (SAE) including mortality"，作者还补了机制归因 "The SAEs were attributed to increased alveolar inflammation, increased MMP12 generation, and emphysema due to the long half-life of BG00011"，而稳定伸展-开放构象的小分子 "and have not shown any drug-related serious adverse events in clinical trials"。
   **他们做了什么**：把选择性从"筛出来"改成"设计出来"——先从共晶结构里定位 β6/β8 的两个差异区（SDL2 打包 LXX(L/I) 的 Tyr185/Leu174、以及 E316/K304 电荷反转），让设计的 α-loop/β-loop 专门去接触这两处；β8 一侧因为天然配体在那里本来就"包得不紧"，他们用**环延长**（RosettaRemodel 采样不同长度与构象的 β-loop）+ 允许 LXX(L/I) 模体本身重新设计，来容纳更粗的残基。选择性随后用回变实验反证：把 MAVY 换回天然的 LATI 会丢掉对 αvβ8 的选择性，而 LATY（单个 I→Y）反而把 αvβ8 推到 500 pM。
   **应对后仍留下的代价**：计算阶段没有任何"选择性打分"，只按预测结合能排序取前 9 条；选择性完全靠事后全谱实验（八种 RGD 整合素 + 转染细胞株 + BLI + 竞争 ELISA）逐个测出来。**"能否在设计阶段预测亚型选择性"这一问，本文未解决。**

2. **设计构象与实验构象对不上——整体位姿错、只有界面是对的**。第一轮最佳结合体的晶体结构："The crystal structure fits the designed model well except for a rigid body translation of the C-terminal helix along the helical axis by one helical turn"（正文给 ~3.4 Å）。冷冻电镜里同样："In the cryoEM map, the overall orientation of the minibinder is shifted relative to initial design, but the RGD loop positioning is as predicted"，图注也写明 "Although the overall angle of the minibinder is shifted, the RGD loop positioning is as predicted"。
   **他们做了什么**：(i) 把约束只放在真正承载功能的地方——设计时 "constraining torsion angles in the region corresponding to the RGD peptide to those observed in the co-crystal structure using Rosetta"；(ii) 评价口径改成**接触图谱**而不是刚体 RMSD："Of the 13 interacting pairs of residues present in the cryoEM model, 11 are present in the computational design model, including all three salt bridges."，两条没预见的相互作用被单独点名（都是骨架接触）；(iii) 第二轮设计不再拿模型对接，而是把**第一轮的晶体结构**叠到靶上重采样两个界面环（Methods Computational techniques 段）。
   **代价**：C 端螺旋那一整圈的平移没有任何纠正手段，作者只描述、不解释，也没做"把平移后的结构再优化回去"的对照。

3. **模板构象本身就选错了**：B6_BP_dslf 是在闭合头部构象（PDB ID 4UM9）上设计的，但实验结构显示结合时 βI 结构域 "rearranges to the same open conformation as when bound to ligand"——设计用的是闭合态，实际结合态是开放态。
   **他们做了什么**：承认这一点，并把"稳定哪一种构象"变成一个可观测的性质而不是模型假设：上样时用阳离子把平衡推到开放态，"All minibinder-integrin complexes were formed in a buffer containing excess Mn 2+ ions to push the conformational equilibrium towards extended-open and to ensure the availability of the MIDAS cation, which is known to be crucial for ligand binding"；再用负染 2D 类均先看全局构象分布，再上冷冻电镜。
   **代价**：这条路线只在 αvβ6 上得到"打开"的读数，αvβ8 侧是 "no open headpieces were observed, with or without minibinder"，也就是说这对设计只能证明"闭合态被保持"，无法证明构象被主动选择；正文没有给未结合态开放/闭合占比的定量基线（只有 Fig 3a 的定性描述"两者都在"）。

4. **复合物柔性大、分辨率不均、分类结果单一**。作者直说 "although the resolution varies considerably due to the intrinsic flexibility of both integrins"。
   **他们做了什么**：四件事——(i) focused refinement 与局部精修（正文给名义整体分辨率 3.4 Å 与 2.9 Å）；(ii) 制样时加去垢剂，"Just prior to sample application, 10% CHAPS detergent was added to each complex up to a final concentration of 0.025%."；(iii) 同一复合物跨网格、跨倾转角多套采集（负染 296/337 张；冷冻电镜 αvβ6 两套 1152 与 722 张，αvβ8 三套 1460/570/3174 张，含 0°/30°/35° 倾转）；(iv) 模型构建用已知结构起算再手改、糖链手动补，"Models (including glycans) were refined and relaxed using Rosetta."。
   **代价**：即使做了 extensive 3D 分类，"we did not observe any subclasses of the integrin-minibinder complex in a closed headpiece conformation"。"只看到一种构象"这件事，从正文证据无法区分"设计真的把构象锁死"与"分类流程把另一种扔掉了"。

5. **体内模型一开始做不出纤维化**（实验协议失败被写进正文）。"Using this method, we observed limited fibrotic development"，于是 "we changed our method as advised by our IACUC committee to use isoflurane to anesthetize and added the application of approximately 10"（后接 µL 级 2% 利多卡因涂喉部）"to inhibit spontaneous closing of the vocal cords"，此后才有所谓"severe"模型。
   **他们做了什么**：把"造模是否成功"写成进组门槛——"Exclusion criteria A (no development of fibrosis): for inclusion in the study mice had to have a weight loss of 3% or greater by day 7 from day 0 and noticeable fibrotic regions on the micro-CT scans."，"Exclusion criteria B (morbid weight loss): if any mice lost 30% or more of their body weight from day 0, they were euthanized and removed from analysis."，另有排除标准 C（死于操作并发症）；再加随机化与笼内混组 "Mice were randomly assigned to the treatment groups before any experimental assessments were made. Each cage had a combination of treatment groups to control for cage variation."，盲法与离群值规则 "Analysis was done blinded to the treatment group assigned."、"Outliers were identified using Grubb's test (Q = 5%)."，µCT 分割阈值用两群对照的直方图交点定 "Dense tissue was defined as anything above the intensity where non-treated mice and bleomycin-treated mice intersected on the frequency of intensities histogram."
   **代价**：入组判据（µCT 可见纤维区）与读出终点（µCT 健康肺体积）来自同一台仪器、同一套阈值口径；因排除标准被剔除的动物数与每组最终只读数写在 Supplementary Data 6，正文未给。

6. **吸入给药把蛋白逼到液-气界面上**（制剂侧的物理失败模式）。"While inhaled tissue-restricted delivery of drugs at the site of action minimizes overall toxicity, dose, and adverse effects, a challenge in development of inhaled biologics is instability or aggregation at the liquid-air interface."
   **他们做了什么**：先在分子层面加约束——"Four variants with additional disulfide bonds stapling the N and C terminus had considerably increased thermostability"，最终交付的 B6_BP_dslf / B8_BP_dslf 都是这种二硫键变体；再验证二硫键是否真的是因果，"To investigate the role of the engineered disulfide bond on stability, 1 mM TCEP was added to the protein to measure thermal stability under reducing conditions."；最后把"雾化前后"当成一对自身对照，实际用 Aeroneb 雾化、按两种粒径收集气溶胶，复测聚集态/二级结构/亲和力三件事，得到 "the protein is monomeric, thermostable, has the same CD spectrum"。
   **代价**：短半衰期没有被解决，只是被当成优点使用——"B6_BP_dslf was rapidly cleared from the blood following IV and IP administration with a half-life of ~10 min, and following inhaled administration, B6_BP_dslf had a half-life in the lungs of ~1 h"；作者提出可用位点特异 PEG 化或 Fc 融合改善药代，但本文没做。

7. **结晶时空间群/孪晶标错**（一处纯方法学的失败与人工补救，写在 Methods 里）。数据最初按六方空间群标度，"The diffraction data for binding protein were originally scaled to P6 1 22 space group with large Patterson peaks 1/3 and 2/3 along the c axis"，用设计模型做分子置换能找到解，但 "Autobuild was able to rebuild most sequences in the model, but R and Rfree were still very high, at 44%/47% with reasonably good electron density maps."
   **他们做了什么**：换空间群并按四孪晶精修，"Data were then re-scaled to the P3 1 space group with 12 molecules per asymmetric unit and refined with tetrahedral twinning with three twin laws: -k, -h, -l; k, h, -l; and -h, -k, l."，再用 AUTOBUILD 建三分之一的序列、COOT 手建与 PHENIX/RefMAC 多轮迭代，最后用 MolProbity 验证。
   **代价**：补救靠人工反复试空间群与孪晶律，正文没给"如何提前判断空间群标错"的规则或指标；这是全文唯一一处解析失败被写进 Methods 的地方，也是"R/Rfree 高但密度图看起来不错"这种矛盾读数被明说的地方。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及各自在这条漏斗里干什么）

- **计算侧（很薄，只干三件事）**：
  - Rosetta 片段组装 + ideal protein 规则（参考文献 25 Koga 2012）：从片段拼可折叠支架，同时把 RGD 区的二面角锁成共晶观测值；
  - RosettaRemodel（参考文献 26）：给 β-loop 采样不同长度与构象（这是为 αvβ8 支路准备的）；
  - AlphaFold（参考文献 27）：**只用来给 200 个环模型排序**，取预测结合能最低的 9 条送实验。正文没有给 AF2 的绝对分数门槛。
  - 外加自定义脚本："In silico design the analysis of the inhibitors was performed using a combination of bash, python, and Rosetta. All scripts used in this paper have been uploaded to a github account"，协议与 XML 也公开（"Detailed step by step protocol and all associated codes have been deposited on github"）。
  - **没有用的方法**：全篇无 MD、无 QM、无自由能计算；也没有"设计-实验配对大数据集"用来给筛子打分。
- **实验侧筛选（真正做递减的地方）**：酵母表面展示（pCon2 / Aga2-Myc，FITC 抗 Myc 看展示、生物素化 αvβ6 + PE 链霉亲和素看结合，FACS）；site-saturation mutagenesis 库（诱变引物见 Supplementary Data 2/3）+ **蛋白酶切割加压** + 递减浓度结合 + 前后池条形码化 + Illumina 测序算 enrichment ratio；E. coli BL21(DE3*) 自诱导表达 + Ni-NTA + SEC（S75 10/300）+ 质谱确认；BLI（Octet RED96，Ni-NTA 与链霉亲和素传感器，结合 900 s/解离 1200 s）；CD 光谱与热融化（222 nm，4–95 °C，2 °C/min，另在 1 mM TCEP 还原条件下复测）；细胞表面滴定（K562 稳定转染株、A431）；X 射线晶体学（1.8 Å）；负染 EM（Talos L120C）与冷冻电镜（Glacios 200 kV、K3、cryoSPARC + CTFFIND4 + MotionCor2）；TMLC 与 CAGA 报告细胞共培养（TGF-β 激活 IC50）；hLAP1 竞争 ELISA；荧光体内成像与离体分布；flexiVent 肺力学 + HR-µCT + Masson 三色/Ashcroft + Sirius Red + Sircol + western + BALF 细胞因子芯片；人肺类器官 hFLO。
- **对照与阳参（这是本文实验设计最结实的部分）**：小分子 PLN-74809（自己合成，">97.5% HPLC 纯度" 由 WuXi STA 提供，见 Methods Synthesis 段）、GSK3008348（数据取自 Decaris 2021）、抗体 3G9/STX-100、264RAD、7.1g10、ADWA11、无关纳米抗体；机制阴性对照 RGD→KGE 突变；构象/选择性阴性对照 MAVY→LATI 回变；空白传感器测非特异结合；PBS 注射小鼠做成像背景。

### 工作流程表（按正文与 Methods 的实际先后顺序）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| W1 | 人 αvβ6 + L-TGF-β3 肽（RGDLGALA）共晶结构 PDB ID 4UM9；整个 PDB 数据库 | 在计算机里扫 PDB 找能容纳这段 8 残基 extended turn 的拓扑：把低 RMSD 匹配片段（肽骨架 + 两端各 5 个残基）叠回复合物里的结合态构象 | 骨架级 clash 判据："Low RMSD matches to the peptide backbone conformation, along with the five flanking residues on both the N- and C-termini, were superimposed on the bound peptide conformation in the complex structure, and those making backbone level clashes with the integrin were discarded"（RMSD 数值阈值正文未给） | 能无 clash 承载该 loop 的小 α/β 铁氧还蛋白折叠若干（正文未给候选数量）；同时要求这些支架能与 α、β 两个亚基各成一段接触（α-loop / β-loop） |
| W2 | W1 选出的折叠片段 | 按 ideal protein 规则拼装，采样不同 α 螺旋/β 折叠/环长度；与 αvβ6 叠合对接后优化界面残基能量 | "Structures were assembled from fragments following rules for constructing ideal proteins 25 , sampling different alpha helix, beta sheet, and loop lengths, while constraining torsion angles in the region corresponding to the RGD peptide to those observed in the co-crystal structure using Rosetta"（能量阈值正文未给） | 理想化铁氧还蛋白折叠设计；两轮设计与优化后选 2 条高亲和变体深入表征：B6B8_BP（av6_3_E13T）与 B6_BP（av6_3_A39KG64R） |
| W3 | 第一轮最佳设计（模型 + 其晶体结构） | 第二轮设计：把**第一轮晶体的结构**叠到 αvβ6 的 RGD loop 上，识别两处靠近靶的环并重采样长度/构象 | 判据是"预测能与靶做成选择性接触"，取 16 条送实验："We identified two loop regions in the design close to the integrin and sampled a range of lengths and conformations for the two loops, and selected 16 designs with loops predicted to make selective interactions with the integrin for experimental testing" | 16 条设计进入实验（这是送测数，不是能量阈值） |
| W4 | 第二轮设计 + SSM 突变库 | 酵母展示筛选，第一轮先做蛋白酶切割再测结合，第二轮只加浓度压力 | 第一轮 "The library was first treated with 4" µM 胰蛋白酶 + 0.8 µM 糜蛋白酶 45 s 后，用 200 pM 生物素化 αvβ6 取 **top 5%**；第二轮用 **100 pM** 取 **top 1%**；分选前后池条形码化后测序："DNA was extracted from pre and post sorted pools and barcoded. Enrichment ratios were calculated after sequencing the pools using Illumina." | 界面富集到 5 处取代（"Five substitutions at the interface which primarily increase charge complementarity were enriched"）；表达纯化 **9** 条富集变体，BLI 全部亚纳摩尔（原始 av6_3 对 αvβ6 Kd 1.2 (±0.006) nM） |
| W5 | αvβ8 支路（模板 PDB ID 6OM2，L-TGF-β1/αvβ8） | RosettaRemodel 生成不同长度与构象的 β-loop 模型（环延长 1 个残基），按 RGD 肽叠合；同时允许 LXX(L/I) 模体本身重新设计 | 计算侧唯一的排序阈值：AlphaFold 预测后取预测结合能最低的 **9** 条——"Both the loop extension and LXX(L/I) structural motif sequences were redesigned using Rosetta and the 9 designs with lowest predicted binding energy following structure prediction using AlphaFold 27 were selected"（AF2/能量绝对阈值正文未给） | 200 个环模型 → 9 条送测 → **4/9** 优先结合 αvβ8；最佳者 B8_BP_dslf 对 αvβ8 Kd 1.9 nM，1 µM 以内对 αvβ6 无可测结合 |
| W6 | W4/W5 得到的骨架 | 在 N/C 末端之间加二硫键（dslf 系列），CD 热融化表征；还原条件下复测以确认二硫键的因果作用 | 稳定性判据是"热稳定性明显提高且仍亚纳摩尔结合"（Tm 具体数值在 Supplementary Fig 9，正文未给阈值）；还原对照："To investigate the role of the engineered disulfide bond on stability, 1 mM TCEP was added to the protein to measure thermal stability under reducing conditions." | 4 条二硫键变体；其中 B6_BP_dslf 深入表征。机制阴性对照：RGD→KGE 消除结合，证明结合由 RGD loop 介导 |
| W7 | 最终变体（B6_BP / B6B8_BP / B8_BP_dslf / B6_BP_dslf） | 亚型选择性全谱：K562 稳定转染的七种其它 RGD 整合素 + 纯化蛋白 BLI + A431 细胞表面滴定 | 观测上限即判据：浓度到 **200 nM** 仍不交叉反应，作者折算为 >1000 倍选择性；BLI 结合 900 s/解离 1200 s，"An empty sensor with no loaded binding protein was included to discard any non-specific binding" | B6_BP 对 αvβ6 0.11 (±0.09) nM、对 αvβ8 580 (±40) nM；B6B8_BP 1.7 (±0.2) / 7.3 (±1.2) nM；A431 细胞上 B6_BP 30 (±0.004) pM vs B6B8_BP 167 (±0.028) pM；B8_BP-LATY 对 αvβ8 500 pM，500 nM 内对 αvβ6 无结合 |
| W8 | 同一批变体 + 靶头域蛋白 | 功能与竞争性读数：CAGA 报告细胞共培养测 TGF-β 激活抑制；hLAP1 竞争 ELISA 测与内源配体抢位 | 剂量响应判据 = IC50，拟合口径写明："Data were plotted in Prism 9 (GraphPad Software, San Diego, CA) to determine the 50% inhibitory concentration (IC 50 ) using a four-parameter logistic regression model."；竞争实验稀释规则："Serial dilutions of B6_BP_dslf, B6B8_BP_dslf, B8_BP_dslf, and PLN-74809 starting at 100 nM and diluting 3-fold seven times" | B6_BP_dslf 抑制 αvβ6 介导 TGF-β 激活 IC50 32.8 (±3.4) nM；hLAP1 竞争 αvβ6：B6_BP_dslf 1.84 nM < B6B8_BP_dslf 3.79 nM < PLN-74809 4.36 nM，B8_BP_dslf 无可测结合；αvβ8：B8_BP_dslf 2.68 nM < B6B8_BP_dslf 8.48 nM < PLN-74809 < B6_BP_dslf |
| W9 | 复合物（1:2 integrin:minibinder，室温 60 min） | 负染 EM 先看全局构象分布，再冷冻电镜定结构并与设计模型比 | 制样判据："The integrin-minibinder complexes were formed using a 1:2 integrin to minibinder ratio, incubated at room temperature for 60 min"，Mn2+ 过量推平衡；分辨率 3.4 Å（αvβ6+B6_BP_dslf）/2.9 Å（αvβ8+B8_BP_dslf，focused refinement）；设计一致性用复合物 RMSD 0.6 Å / 0.7 Å vs design，以及残基对命中 11/13 | 负染：296/337 张图 → 34,794/36,710 颗粒 → 2D 类均用 22,096/24,532 颗；冷冻电镜：αvβ6 两套 1152+722 张、αvβ8 三套 1460/570/3174 张 → 360,600 与 3,325,476 颗粒 → 建模用 124,715 与 116,587 颗；数据入 EMD-41153/41154、PDB 8TCF/8TCG |
| W10 | B6_BP / B6_BP_dslf | 可开发性与体内：雾化前后复测（两种 MMAD 2.5–4 与 4–6 µm）；AF680-B6_BP 尾静脉 1.5 nmol 成像 A431(+) vs HEK293T(-)；IV/IP/IN 三途 PK；BLM 1 U/kg 气管内造模后 OA 给药 43.6 与 185.2 µg/kg 隔日一次（day 7→19，共 7 次） | 入组门槛："Exclusion criteria A (no development of fibrosis): for inclusion in the study mice had to have a weight loss of 3% or greater by day 7 from day 0 and noticeable fibrotic regions on the micro-CT scans."；剔除门槛：减重 ≥30%；统计口径：one-way ANOVA + Tukey、Grubb's Q = 5%、p < 0.05、盲法 | 6 h 离体分布示肿瘤与肾蓄积（tumor-to-kidney 1:1.04），主要经肾小球滤过清除；血 t1/2 ~10 min、肺 ~1 h；185.2 µg/kg 组 Ashcroft、可溶/不溶胶原、FVC、静态顺应性与 IL-6/TNF-α/TIMP-1 均显著改善；hFLO 类器官（BLM 20 µg mL−1 三天 + 10 nM 药四天，N = 15 个细胞团）中 α-SMA 与纤连蛋白显著下降 |

**这条漏斗的形状值得单独记**：计算端只做三件事（找无 clash 拓扑、锁 RGD 二面角、AF2 给环模型排序取前 9），**每一步的数量递减几乎都由便宜湿实验完成**（16 → 9 → 4；200 → 9 → 4/9），而选择性、构象、成药性、体内效力是四道彼此独立的实验关。全文没有一处"用计算分数决定要不要合成"的统一阈值——这跟 B09 那种"百万条带标签数据先考筛子"的路线正好相反：**这里没有考卷，所以闸口只能建在实验上。**

## 4. 关键数字台账（全部来自本地全文；出处给可定位的原句片段）

| 数值 | 含义 | 出处（原句片段，可逐字搜索） |
|---|---|---|
| <75 amino acids | 设计目标：迷你蛋白链长上限（Computational design strategy 首段自设目标） | "generates small (<75 amino acids) hyperstable de novo integrin binding proteins" |
| 8 残基 extended turn / RGDLGALA | 被当作锚的天然肽构象 | "capable of hosting the 8 residue extended turn conformation of the peptide (RGDLGALA" |
| 4UM9 / 6OM2 / 4UM8 | αvβ6+L-TGFβ3 共晶（设计模板）/ αvβ8+L-TGFβ1 共晶 / 无配体 αvβ6（SDL2 有序） | "PDB ID 4UM9"、"PDB ID 6OM2"、"(PDB ID 4UM8)" |
| 200 | β-loop 重采样模型数（αvβ8 支路） | "We generated 200 models with different lengths and conformations of the" |
| 16 | 第二轮设计送实验数 | "and selected 16 designs with loops predicted to make selective interactions with the integrin for experimental testing" |
| 9（两轮各一次） | 第一轮 SSM 富集后表达纯化的变体数；第二轮 AF2 排序后送测数 | "the 9 designs with lowest predicted binding energy following structure prediction using AlphaFold 27 were selected" |
| 4/9 | αvβ8 支路里优先结合 αvβ8 的比例 | "Four out of 9 designs showed preferential binding to" |
| 4 µM 胰蛋白酶 + 0.8 µM 糜蛋白酶，45 s | 第一轮分选前的蛋白酶切割加压 | "The library was first treated with 4" µM Trypsin and 0.8 µM chymotrypsin 53 for 45 s |
| 200 pM → top 5%；100 pM → top 1% | 两轮分选的靶浓度与取样比例 | "followed by labeling with 200" pM of biotinylated"、"For the second and final round of selection, 100" pM |
| 9/9 亚纳摩尔；av6_3 Kd 1.2 (±0.006) nM | SSM 富集变体的实测结合水平 | "all had subnanomolar binding affinity (the original av6_3 binds to" |
| 5 处取代 | 界面被富集到的取代数（主要是电荷互补） | "Five substitutions at the interface which primarily increase charge complementarity were enriched" |
| 1.9 nM（αvβ8）；1 µM 内无 αvβ6 结合 | B8_BP_dslf 亲和力与选择性 | "and binds to human" αvβ8 with 1.9 nM affinity, with no appreciable binding to human" |
| 1.13 nM（对 αvβ6） | MAVY→LATI 回变体 avb8_12 丢失选择性后的读数 | "Purified avb8_12 with the reversion mutations loses selectivity towards" |
| 500 pM（αvβ8）/ 500 nM 内无 αvβ6 | 单点 I→Y 的 B8_BP-LATY | "B8_BP-LATY with a single substitution from I to Y bound to" |
| 0.11 (±0.09) nM vs 580 (±40) nM；1.7 (±0.2) vs 7.3 (±1.2) nM | B6_BP 与 B6B8_BP 在 K562 表面对 αvβ6/αvβ8 的 Kd | "with a K d of 0.11 (±0.09) and 580 (±40) nM, respectively" |
| 30 (±0.004) pM vs 167 (±0.028) pM | A431 细胞表面滴定（AF488 标记） | "B6_BP binds to A431 cells with higher potency than B6B8_BP (30 (±0.004) pM vs 167 (±0.028) pM)" |
| 200 nM / >1000 倍 | 交叉反应观测上限与折算选择性 | "at concentrations up to 200 nM in cell surface binding experiments" |
| 32.8 (±3.4) nM | B6_BP_dslf 抑制 αvβ6 介导 TGF-β 激活 IC50（CAGA 报告） | "B6_BP_dslf inhibits TGF-β activation with an IC50 of 32.8 (±3.4) nM" |
| 1.84 / 3.79 / 4.36 nM；2.68 / 8.48 nM | hLAP1 竞争 IC50（αvβ6 侧与 αvβ8 侧，含 PLN-74809 对照） | "For αvβ6 integrin, B6_BP_dslf had the lowest IC 50 (1.84 nM), followed by B6B8_BP_dslf (3.79 nM), PLN-74809 (4.36 nM)" |
| 1.8 Å | 第一轮最佳结合体（复合物）晶体分辨率 | "We solved the crystal structure of the best binder at 1.8" Å |
| 3.4 Å / 2.9 Å | 两个复合物的 cryoEM 名义整体分辨率（focused refinement） | "the nominal overall resolution is 3.4" Å for the |
| 0.6 Å / 0.7 Å | 迷你蛋白-整合素复合物 vs 设计模型的 RMSD | "complex RMSD 0.6" Å vs design；"complex RMSD 0.7" Å |
| 11/13；12 对 | αvβ6 复合物中设计命中的残基对（含三条盐桥全中）；αvβ8 复合物的相互作用对数 | "Of the 13 interacting pairs of residues present in the cryoEM model, 11 are present in the computational design model, including all three salt bridges." |
| 3.4 Å（one helical turn） | 晶体相对设计的 C 端螺旋整体平移 | "by one helical turn (~3.4" Å" |
| 296/337；34,794/36,710；22,096/24,532 | 负染：图数/拾取颗粒/进入 2D 类均的颗粒（αvβ6/αvβ8） | "The final particle counts contributing to 2D class averages were 22,096" |
| 1152+722；1460/570/3174 | 冷冻电镜每个复合物采集的图数（不同网格与倾转角） | "one dataset of 1152 micrographs was collected from an Quantafoil grid" |
| 360,600 / 3,325,476 → 124,715 / 116,587 | 冷冻电镜拾取颗粒数 → 进入最终 3D 结构建模的颗粒数 | "The particle counts contributing to the final 3D structures into which the models were built are 124,715" |
| 1 U/kg；50 µl/animal | 气管内 bleomycin 剂量 | "intratracheally instilled with a single dose of 1 U/kg bleomycin sulfate in 0.9% sterile saline (50" µl/animal)" |
| 100 µg/kg 与 1 mg/kg（IP）；43.6 与 185.2 µg/kg（OA，隔日，day 7→19，共 7 次） | 两条给药路线的剂量方案（Fig 5 图注把低剂量写作 46.3 ug/kg，见第 7 节） | "we administered B6_BP_dslf intraperitoneally at 100" µg/kg in the mild bleomycin model and at 1" mg/kg in the severe" |
| ≥3%（day7）；≥30% | 入组与剔除的减重门槛 | "Exclusion criteria A (no development of fibrosis): for inclusion in the study mice had to have a weight loss of 3% or greater by day 7 from day 0" |
| 0–8 分/视野；10x 视野全肺 | 改良 Ashcroft 计分口径 | "slides were scored using a modified Ashcroft scoring applied to the whole lung divided into 10x fields where sections were given a score of 0-8 per section" |
| ~10 min（血）；~1 h（肺） | B6_BP_dslf 半衰期（IV/IP 与吸入） | "with a half-life of ~10 min, and following inhaled administration, B6_BP_dslf had a half-life in the lungs of ~1 h" |
| 1.5 nmol；5–10 mm；tumor-to-kidney 1:1.04；n = 5 | 尾静脉成像给药量、开始成像瘤径、6 h 分布比与动物数 | "injected via the tail vein with 1.5 nmols of AlexaFluor-680 labeled B6_BP" |
| 2.5–4 µm 与 4–6 µm（MMAD）；~1–5 µm 为到达下呼吸道的要求 | 雾化粒径档位与解剖学判据 | "we nebulized B6_BP_dslf using an Aeroneb nebulizer and collected aerosols of two different MMADs: 2.5"–4 µm and 4"–6 µm" |
| 10 nM，4 天；BLM 20 µg mL−1，3 天；N = 15 个细胞团 | 人肺类器官 hFLO 治疗方案与统计单位 | "hFLO organoids were allowed to self-pattern for 7 days after which fibrosis was induced using bleomycin for 3 days prior to treatment with 10 nM B6_BP_dslf for 4 days." |
| 44% / 47%；P3 1，12 分子/AU，三条孪晶律 | 空间群标错时的 R/Rfree 与纠正后的晶胞设置 | "Autobuild was able to rebuild most sequences in the model, but R and Rfree were still very high, at 44%/47% with reasonably good electron density maps." |
| 24,000 g 45 min；<5 EU/ml | 迷你蛋白纯化工艺：裂解后离心条件；体内用蛋白的内毒素上限 | "Cells were lysed using microfluidizer and cell debris was separated by centrifuging at 24,000 g for 45 min."、"protein was subjected to further purification to achieve endotoxin level <5 EU/ml." |
| 800 mL / 3.0 × 10 6 cells per mL；4000 rcf 5 min | 整合素头域制备规模与澄清条件（Expi293F 悬浮培养） | "800 mL cultures of Expi293F cells were grown in suspension to a density of 3.0 × 10 6 cells per mL"、"Supernatants were clarified by centrifugation (5 min at 4000 rcf)" |
| 900 s / 1200 s；0.025% CHAPS；1:2 复合物比 | BLI 结合/解离时长、制样去垢剂、复合物配比 | "Association and dissociation steps were recorded for 900 s and 1200 s respectively." |
| 7LMV / 7LMX / 8TCF / 8TCG；EMD-41153 / 41154 | 沉积结构（第一轮设计与 B6B8_BP_dslf 单体；两个复合物） | "Structures from the first-round design and B6B8_BP_dslf monomer have been deposited in the Protein Data Bank with accession numbers 7LMV" |

## 5. 结论——作者说了什么（只写原文明确主张）

1. **方法学主张**：这是一条通用方法，不是单个靶的例子。"Here we describe a generalized method for computationally designing RGD-containing miniproteins selective for a single RGD integrin heterodimer and conformational state."；作者自认的产物是 "We design hyperstable, selective" 的 αvβ6 与 αvβ8 抑制剂（摘要）。
2. **结构主张**：设计模型被实验结构证实。"CryoEM structures of the designed inhibitor-integrin complexes are very close to the computational design models"，具体到"复合物 RMSD 0.6 Å / 0.7 Å"与"Of the 13 interacting pairs of residues present in the cryoEM model, 11 are present in the computational design model, including all three salt bridges."；同时作者明说位姿有偏移但 RGD loop 如预测："Although the overall angle of the minibinder is shifted, the RGD loop positioning is as predicted"。
3. **选择性主张**：两个终分子各自单选，且比小分子更干净。"Taken together, these data confirm that B6_BP_dslf and B8_BP_dslf have exquisite selectivity and affinity for their respective integrin targets"，图注补充 "Rows shaded in gray indicate the RGD integrin(s) for which each molecule is selective (i.e B6_BP_dslf and B8_BP-LATY are both mono-selective whereas PLN-74809 and GSK3008348 are dual- and tri-selective, respectively)" 的口径（原文如此，n/a not available）。
4. **选择性开关的分子基础**：作者给出因果链——天然配体侧 LXX(L/I) 打包在 β6 的 Y185 上"packs optimally"而 β8 的 L174 上"packs much less tightly"，于是他们对 β8 允许更粗的残基，并在实验结构里看到 "we find that Y16 forms stabilizing interactions with A115 of the" β8 亚基、对 β6 侧则写 "we hypothesize that the steric clash would interfere with binding."（作者自己标为假设）。系统逐位点扫模体是他们的确认手段："We systematically varied each position within the LATI motif to determine which residue plays a critical role in determining selectivity (Fig. 2e )."
5. **构象主张**：迷你蛋白不只是占据结合位点，还稳定特定构象态——αvβ6 被诱导/稳定为开放头部，αvβ8 保持伸展-闭合；图注原句 "no open headpieces were observed, with or without minibinder"。
6. **体内与成药性主张**：吸入给药在小鼠肺纤维化模型里有效。"inhibitor potently reduced fibrotic burden and improved overall lung mechanics, demonstrating the therapeutic potential of de novo designed integrin binding proteins with high selectivity"；制剂侧 "inhibitor remains monomeric and maintains biological activity following aerosolization and shows excellent efficacy in bleomycin induced lung fibrosis"（编辑摘要段）；作者汇总的"目标产品特性"是 "give B6_BP_dslf an improved target product profile as a therapeutic candidate for IPF"，理由清单包括短血清半衰期、高选择性、稳定开放构象、E. coli 易产、超热稳定、可雾化。
7. **作者自己写出的边界**：(i) 药代没有优化——"Further improvement in the pharmacokinetic/pharmacodynamic properties of these molecules could likely be achieved by site-selective chemical PEGylation or fusion to an immunoglobulin Fc domain for immune-oncology indications"；(ii) 电镜分辨率不均——"although the resolution varies considerably due to the intrinsic flexibility of both integrins"；(iii) 只有一个 αvβ6 分子进了体内，αvβ8 只到体外选择性/功能；(iv) 普适性主张是外推句式："this approach should be widely applicable to developing binders with high selectivity and affinity to individual members of the many therapeutically important families of cell surface receptors"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这条漏斗的计算端几乎没有做决策**。全文只有一处计算排序真正决定"送测谁"（AF2 预测结合能取最低 9 条），其余递减由实验完成。原因不是他们不想，而是**没有可用的历史标签集**：一个全新靶、全新支架，没有任何"设计+结局"配对数据可以事先给筛子打分。→ 对照 B09（有 Cao 2022 的近百万条标注才能"考筛子"），B44 展示的是**没有考卷时的做法**：把决策权交给便宜、可解释、带阴性对照的实验闸口。我们的 UAA 现状更接近 B44 而不是 B09，所以这套"实验闸口 + 阴性锚点"的组织方式比"pAE 阈值"更值得学。
2. **蛋白酶切割那一步的性质，作者没解释，别当作折叠验证**。原文只写操作（4 µM 胰蛋白酶 + 0.8 µM 糜蛋白酶 45 s，再测结合、取 top 5%），没有任何一句说"因为只折成目标构象才抗切割"。抗蛋白酶同样可能选中"柔性环少""末端裸露少""表面电荷排布不利于酶结合"的变体。→ 我们若借用"物理化学应激 + 富集"当正交闸口，必须先做一次校准（应激读数与目标构象/目标活性是否相关、有无相关方向反转的样本），不能默认它是折叠筛。本项目原卡 `sources/baker.md:589` 把该步解释为"只有折成目标 turn 的设计才抗切割"，这属于我们的推断，本次已在本卡标明为推断。
3. **"选择性"在这篇里是被事后点突变证明的，不是被设计预测的**。MAVY→LATI 全回变丢选择性、单个 I→Y（LATY）反而把 αvβ8 推到 500 pM，说明关键位点可以在成熟阶段用单点扫描找到。→ 对 UAA：不要指望第一轮设计就带"底物选择性"，但要把"能在成熟阶段用少数单点突变移动选择性"当成可规划的第二步，并提前留好位点假设（我们的对应物是催化口袋第二圈残基，不是界面残基）。
4. **报告"设计正确性"时他们刻意选了负责功能的自由度**（残基对接触、三条盐桥，而不是整体位姿 RMSD）。这既合理也自利：整体 RMSD 会因为 3.4 Å 的螺旋平移与 minibinder 角度偏移而难看，而接触图谱 11/13 好看。→ 我们做机制层验证时，验证口径要预先声明"看哪几个相互作用/几何量"，并同时报告被忽略的自由度（这篇做到了，把两条未预见接触单独列出，是我们该照抄的诚实做法）。
5. **亲和力读数的口径混用，引用时必须分层**。"picomolar"只在摘要出现；纯化蛋白 BLI 的量级是 nM–亚 nM（1.2 nM、1.9 nM、0.11 nM），而 pM 读数（30 pM、167 pM）来自**细胞表面滴定**（A431 全细胞，配体密度与亲和力都不同于均相 BLI）。另外 30 (±0.004) pM、1.2 (±0.006) nM 这类"SD 远小于测量本身"的写法，加上 "Data are presented as mean values +/- SD ( n = 3 independent experiments)"，更像拟合参数的标准误被当成 SD 报告（推断，非作者说明）。→ 我们引用他文亲和力时，必须记"体系（纯化/细胞表面）+ 方法（BLI/FACS 拟合）+ 散布是 SD 还是 SEM/拟合误差"三项，否则跨文比较无意义。
6. **体内效力建立在"入组门槛"上，而门槛与终点同源**。排除标准 A 用 µCT 可见纤维区选人，读数又用 µCT 健康肺体积与 Ashcroft。虽然 A 在实验开始前就设好（"Exclusion criteria A was in place prior to the beginning of the study."），随机化、笼内混组、盲法、Grubb's 检验也都写了，但"救援幅度"里仍混有"被选进来的动物恰好严重到可被救援"的成分。→ 我们的候选准入协议若也用同一个量既做准入又做读出，必须在报告里显式声明这一点，并另设一个独立读出（例如化学产物定量）。
7. **正文与图注的剂量/面板编号对不上，说明这套数据的"数字层"未经统一核对**（详见第 7 节）。最可能的解释是补做实验时改过剂量方案而稿件未统一，而不是有意的两批实验——这是我们的判断，作者没有说明。

## 7. 局限与失败（作者的 + 我们读出的）

**作者承认的**（见第 5.7 条）：分辨率受柔性限制、αvβ8 侧看不到开放构象、药代未优化、只有一个分子进入体内、αvβ6 的"闭合态为何没被观察到"未回答（"we did not observe any subclasses of the integrin-minibinder complex in a closed headpiece conformation"）、C 端螺旋一整圈平移未解释。

**我们读出的（按可核验程度排序）**：

1. **同一剂量三个写法**：正文 Results 与 Methods 都写 OA 43.6 与 185.2 µg/kg（"mice were administered B6_BP_dslf via oropharyngeal administration (OA, 43.6 and 185.2 µg/kg)"、"with drug concentrations of 43.6 and 185.2 µg/kg"），Ashcroft 段写成 **43.62 µg/kg**（"compared to the BLM and 43.62 µg/kg B6_BP-disulf treatment group"），而 Fig 5 图注全部写 **46.3 ug/kg**（含所有 P 值标签）。同一组低剂量在一份正文里出现三种数字，读者无法判断哪一个是实际给药量。
2. **面板编号错位**：western（Collagen1、p-SMAD2）与 Sircol 可溶/不溶胶原在 Results 里被指向 "Fig.  4e, f" 与 "Fig.  4g, h"，而这四个面板由 Fig 5 图注定义（e Whole lung tissue homogenate western blot of Collagen1… f p-SMAD2… g Soluble… h Insoluble）；同段 FVC 又正确写 Fig. 5c。Fig 4 是活体成像图，没有 e–h 面板。
3. **亚基归属笔误**：Methods 描述盐桥时写 "interacts with negatively charged E316 of the" 后接 β2 亚基，而 E316 在 Results、Fig 1f 与 Fig 2a 中都属于 β6；本文没有设计任何 β2 靶。
4. **变体命名不统一**：B6_BP_dslf / B6_BP-disulf / B8_BP_dslf / Methods 模型构建段的 **B8_BP2_dslf**、回变体的 **avb8_#12** 与 **avb8_12** 并存；序列全在 Supplementary Data 1，正文无法一一对上（正文未给）。
5. **摘要与正文的亲和力口径不一致**：摘要 "bind with picomolar affinity"，正文 BLI 是 nM–亚 nM，pM 只出现在细胞表面滴定（见第 6.5 条）。
6. **设计侧没有可复现的阈值**：整个计算漏斗没有给能量分数、RMSD 匹配上限、或"多少条设计进入第一轮"的数字，两轮设计与优化的细节被推到补充（"Following two rounds of design and optimization (see supplementary info for details"）；本卡因此只能标"正文未给阈值"。**这意味着这条路线目前不可按原样复算，只可按原样重做实验。**
7. **没有阴性/失败计数的正文可见性**：16 条与 9 条送测的失败者未逐条列出（正文只报成功子集与富集结果），因此无法从正文重建完整混淆矩阵，也无法估计"AF2 预测结合能排序"到底有没有判别力——**这是本文方法学上最大的可审计缺口**。
8. **对照小分子的数据一半来自他文**：PLN-74809 与 GSK3008348 的结合数据取自 Decaris et al. 2021（图注自述 "Binding data for PLN-74809 and GSK3008348 are taken from Decaris et al. 2021"），选择性倍数比较并非同一实验室同一批次平行测得。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"平行活性谱"作为必出数据**：B44 对每个终分子都测全部八个 RGD 整合素（转染细胞株 + BLI + 竞争 ELISA），并把"双选/三选/单选"写成表型（"Rows shaded in gray indicate the RGD integrin(s) for which each molecule is selective"）。→ 我们的每个 UAA 候选必须配一张**近缘底物/近缘反应的平行谱**（天然氨基酸 + 至少两种结构近似 UAA + 至少一个按机制预测应失活的变体），否则"有活性"这个读数没有可解释性。这是可以原样照搬的实验结构，与判据数值无关。
2. **阴性锚点做成设计的一部分**：RGD→KGE 消除结合、MAVY→LATI 消除选择性、TCEP 还原条件下复测二硫键的因果——三条都是"按机制预测应当失效，且真的失效"的对照。→ 我们的机制层判定必须含**同域阴性锚**（催化残基突变失活、缺 ATP/缺 UTP 起始、非底物氨基酸），并把"锚点没有失效"当作整批读数作废的条件。
3. **便宜正交量当第二道闸口**：蛋白酶切割、热融化、雾化前后复测——都是几分钟一价、可在几十条样品上并行、且与靶结合正交的测量。→ UAA 侧可用"预处理稳定性/溶解度/表达量"这类便宜量做**排序性**过滤（不是判据门槛），但必须先按第 6.2 条做相关性校准。
4. **验证只看负责功能的自由度**：11/13 残基对 + 三条盐桥，比整体 RMSD 更能说明"界面对不对"。→ 我们对催化几何的判定也应当写成"指定的几组距离/角度是否出现"（本项目已有冻结口径 ≤4.0 Å / ≥150°），并同时报告被忽略的自由度，而不是只报一个全局 RMSD。
5. **准入与统计口径先写死并盲法执行**：随机分组、笼内混组、排除标准 A 事先设定、盲法读片、Grubb's 去离群、p<0.05。→ 直接对应 DP2R 标准的"预注册 + 判定标准先行"做法；我们可以在候选准入协议里照抄这个结构（尤其"门槛在实验开始前设好"这一条）。
6. **把成药/工程属性当独立一关**：B44 用四件事（可聚集性、热稳定、酶切抗性或半衰期、可生产性）单独给分子打分，而不是把它们折进"命中"。→ 我们的候选报告应把"能不能成键/能不能催化"与"在实验室里能不能做出来（表达、可溶、可检测）"分成两栏，避免后者污染前者的命中率。

**不可迁移（为什么不能照搬）**

1. **本文没有任何与"催化"相关的判据**。全文计算部分只有 Rosetta 组装/重采样与 AF2 排序；无 MD、无 QM、无自由能、无过渡态或几何反应簇。→ 不能用它的成功来说明"MD/QM 判催化可行"，也不能引用它的任何数字作为酶活概率。它连一个化学键的形成都没有测。
2. **Kd/IC50/选择性倍数不能当 UAA 阈值**：这些是"结合"与"抑制配体激活"的量，与"生成共价产物"不共线。本项目判定标准明写不许把 binder 的 pAE/ipTM/Kd 阈值当酶活闸口；B44 的 0.11 nM、32.8 nM、>1000 倍同理只能作为文献参照，不可写成我们的门槛或成功概率。
3. **酵母展示 + 测序富集那种通量在产物化学上不存在**：本文的分选一次过几万个变体、取 top 1%；我们的检测是 LC-MS/MS 逐样品的，一轮最多几个构建体。→ 末端设计不是"样本数最大化"，而是"信息量最大化"（机制多样性 + 阴阳性同域 + 失活对照），照搬"取 top 1%"式的比例阈值毫无意义。
4. **吸入/组织限制给药这一整套开发属性与我们的目标函数无关**（MMAD 档位、雾化后单聚体、肺 PK 半衰期）：只能当作"若将来要做治疗应用"的清单参考，不能进入筛选漏斗的任何一级。
5. **支架与拓扑知识不可复用**：α/β 铁氧还蛋白迷你蛋白支架靠"容纳既有一段肽构象 + 无骨架 clash"起步。UAA 合成酶是带催化中心的完整酶（多结构域、需要金属/辅因子与构象变化），不存在"从一个 8 残基 turn 出发搭支架"的对应物；本文的"设计即模拟天然配体构象"前提在酶设计上不成立。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/integrin_miniprot2023.txt

- **唯一逐字底稿**：`data/interim/baker_lit/ft/integrin_miniprot2023.txt`（Europe PMC fullTextXML 去标签纯文本，2026-10-16 抓取，120,718 B）。本卡全部英文引句只在**这一份**文件上逐字核对；本项目同一论文没有第二份抽取版本，故不存在"跨版本参考文献编号不同"的引句风险（与 B09 那种双通路情形不同）。
- **身份复核**：该文件第 1 行头部块含 DOI `10.1038/s41467-023-41272-z`、PMCID 10500007、PMID 37704610、标题 "De novo design of highly selective miniprotein inhibitors of integrins" 与本行（CSV B44）完全一致，非挂错行文件。
- **登记底稿**：门禁清单 `data/literature_cards/sources_map.json` 的 B44 = 上述全文 + `sources/baker.md`；本项目原卡段落为 `sources/baker.md:578–589`（其"蛋白酶切割=构象筛选"的解释性表述属推断，本卡在第 6.2 条重新定性）。
- **未本地化的部分**：Supplementary Figs 1–18、Data 1–6、Table 1–3、Source Data。凡引用它们的地方本卡写"正文未给出"。
- **CSV 字段映射**：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B44" --no-report` ⇒ **PASS B44 quotes=117/117，退出码 0**（10 节齐全、工作流程表 10 步、难点 7 条、CSV 回填 14 键非空；引句含重复共 117 处、去重后 107 条，全部逐字命中上述底稿）。写作过程中的两处自纠：① 初稿把链长上限写成带省略号的片段（`generates small (…75 amino acids)`），逐字核验判 MISS，已改为底稿实际字符；② 底稿里比较符号仍以 HTML 实体形式存储（`&lt;`、`&gt;`、`&amp;`），而核验器读取底稿时会先解码，因此本卡凡需要引到含 `<` 的句子时写的是**解码后的 `<`**（如 `(…75 amino acids)` 与 `endotoxin level <5 EU/ml` 两处），其余含 `&gt;`/`&amp;` 的句子一律只写进中文叙述而不加引号——卡内没有一条引句带 HTML 转义串。

<!--CSV回填
work_type=论文（Baker组; de novo 迷你蛋白治疗性结合剂；含结构 + 体内效力证据链）
target=整合素 αvβ6 与 αvβ8（RGD 型 L-TGF-β 肽构象模拟；抑制 TGF-β 激活；αvβ6 侧进体内吸入给药）
backbone_generation=Rosetta 片段组装 + ideal protein 规则（Koga 2012）搭 α/β 铁氧还蛋白迷你蛋白支架；以 4UM9/6OM2 共晶为模板 in silico 扫 PDB 找能容纳 8 残基 extended turn 且无骨架 clash 的拓扑；RosettaRemodel 重采样 β-loop 长度/构象（200 模型）；第二轮用第一轮晶体结构对接；第二轮设计 + site-saturation mutagenesis 库
computational_filters=界面能量优化（正文未给阈值）；RMD/RGD 区二面角约束为共晶观测值；冷冻电镜复核口径 = 复合物 RMSD vs 设计 + 界面残基对命中数；无选择性预测量（选择性完全靠实验全谱）
thresholds=送测数：第二轮 16 条、αvβ8 支路 200 模型→AF2 预测结合能最低 9 条；分选阈值：4 µM 胰蛋白酶 + 0.8 µM 糜蛋白酶 45 s，第一轮 200 pM 生物素化 αvβ6 取 top 5%，第二轮 100 pM 取 top 1%；交叉反应观测上限 200 nM；cryoEM 3.4 Å / 2.9 Å；复合物 RMSD 0.6 Å / 0.7 Å；残基对命中 11/13；入组门槛 day7 减重 ≥3% + µCT 可见纤维区，剔除门槛减重 ≥30%；统计 p<0.05、Grubb's Q=5%
md_used=否（全文无分子动力学）
qm_used=否（全文无量子化学/过渡态计算）
experimental_methods=酵母表面展示 + FACS；SSM 文库 + 蛋白酶切割加压 + 递减浓度分选 + 条形码 + Illumina 深测序算富集比；E. coli 自诱导表达 + Ni-NTA + SEC + 质谱；CD 热融化（含 1 mM TCEP 还原对照）；BLI（Octet RED96）；K562 转染细胞表面滴定与八种 RGD 整合素选择性面板；A431 细胞滴定；TMLC 与 CAGA 报告细胞共培养 IC50；hLAP1 竞争 ELISA；X 射线晶体学 1.8 Å；负染 EM 与 Glacios cryoEM（focused refinement、多网格多倾转）；AF680 活体成像与离体分布；IV/IP/IN 三途 PK；雾化（Aeroneb，两档 MMAD）；BLM 气管内 1 U/kg 致纤维化 + 或咽给药；HR-µCT + flexiVent 肺力学 + Masson/Ashcroft + Sirius Red + Sircol + western + BALF 细胞因子芯片；人肺类器官 hFLO
pipeline_counts=设计端正文未给首轮库规模（两轮设计与优化细节在补充）→ 第二轮 16 条送测 → SSM 富集后表达纯化 9 条（BLI 全部亚纳摩尔）→ 界面 5 处取代 → 2 条深入表征（B6B8_BP=E13T、B6_BP=A39K G64R）→ 二硫键变体 4 条 → αvβ8 支路 200 环模型 → AF2 取 9 条 → 4/9 优先结合 αvβ8 → 终分子 B6_BP_dslf 与 B8_BP_dslf/LATY；电镜颗粒：负染 34,794/36,710 → 22,096/24,532；cryoEM 360,600/3,325,476 → 建模用 124,715/116,587
hit_rate=正文未给整体设计命中率与库规模；可见的递减读数：SSM 富集 9/9 亚纳摩尔结合；αvβ8 支路 4/9 优先结合 αvβ8；αvβ6 侧选择性由单点 A39K（对 αvβ8 从 ~7.3 nM 变 >500 nM）与 β8 侧 MAVY→LATY 单点（对 αvβ8 500 pM、500 nM 内对 αvβ6 无结合）达成；功能端 B6_BP_dslf 抑制 αvβ6 介导 TGF-β 激活 IC50 32.8 nM，185.2 µg/kg 或咽给药显著改善 Ashcroft/FVC/胶原，43.6(43.62/46.3 写法不一) µg/kg 无效
best_metric=αvβ6：Kd 0.11 (±0.09) nM（K562 表面）、A431 细胞表面 30 (±0.004) pM、hLAP1 竞争 IC50 1.84 nM；αvβ8：B8_BP-LATY Kd 500 pM（BLI）、B8_BP_dslf 1.9 nM；TGF-β 激活抑制 IC50 32.8 (±3.4) nM
cost_or_stat_note=原文未给计算成本/耗时数字（算力来自 Rosetta@Home 志愿者、Hyak 与 Rhino 集群，仅致谢提及）；样本量：A431 滴定 n=3、BLI 突变体系至少重复 2 次、活体成像 n=5 只、western 与 Sircol 三个生物学重复、hFLO 每处理 N=15 个细胞团；多处 ±值疑似拟合标准误而非 SD（本卡推断）；无公开设计-结局配对数据，故本文的筛子从未在标签集上被打分
role_in_timeline=Baker 组 de novo 结合剂路线里第一个把"亚型选择性 + 构象态选择 + 吸入制剂 + 疾病模型疗效"一次做完的治疗学终点样本；方法学位置上它是 B09 那种"用大数据考筛子"的反面——没有标签集时的做法：计算端只做拓扑匹配与 AF2 排序，递减交给便宜实验（蛋白酶切割、浓度递减分选、测序富集），并用全谱选择性面板与机制阴性变体（RGD→KGE、MAVY→LATI）承担否证功能；与 B24 的 SAPP/SEC-MALS 同属"便宜实验替代昂贵验证"，但本文没有给出任何可复算的阈值
source_pointer=data/interim/baker_lit/ft/integrin_miniprot2023.txt（Europe PMC fullTextXML，2026-10-16；本卡唯一逐字底稿）+ sources/baker.md:578-589；结构沉积 7LMV/7LMX/8TCF/8TCG、EMD-41153/41154；代码 https://github.com/aroy10/avb6-publication
CSV回填-->
