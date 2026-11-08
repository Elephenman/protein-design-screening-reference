# [K32] AlphaFold 抗体–抗原建模的系统基准（427 个复合物）——置信度分数能不能提前判断模型能不能用

Yin Rui, Pierce Brian G（University of Maryland Institute for Bioscience and Biotechnology Research / Dept. of Cell Biology and Molecular Genetics）
Protein Science 2024, 33(1):e4865 · DOI 10.1002/pro.4865 · PMID 38073135 · PMCID PMC10751731
开放获取（CC BY 4.0）· 全文链接 https://pmc.ncbi.nlm.nih.gov/articles/PMC10751731/ · 预印本 bioRxiv 2023-07-21

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K32**（组：通用方法学; 口径对照） |
| 本文取回方式 | Europe PMC `fullTextXML`（PMC10751731），本地抓取，2026-10-20 |
| 本地全文① | `data/literature_cards/fulltext/K32_PMC10751731_fullTextXML.xml`（原始 XML） |
| 本地全文②（本卡逐字比对的底稿） | `data/literature_cards/fulltext/K32_PMC10751731_text.txt`（剥标签纯文本，66,985 B，单行） |
| 对照底稿 | `sources/cost-benchmarks.md` §3.4 论文 B（登记项，本卡未修改） |
| 证据级别 | **全文级**（本卡所有英文引句均可在上述纯文本里逐字命中；见第 9 节自检） |
| 本文性质 | 结构预测 **benchmark + 判据评估**，不是设计论文：不生成新蛋白、不做湿实验、无 MD、无 QM |
| 未取到的部分 | Supplementary Results 与 Figures S1–S17、Table S1 逐条清单、Figure 1/2/5/7/8 柱状图的原始数值。**凡本卡写不出精确数字处即明写"正文未给出，仅有正文描述"**（例如 ColabFold 与 AF2 的逐档差值、各分数分箱的具体阈值） |
| 关键身份点 | 作者 Rui Yin / Brian G. Pierce（Pierce 实验室， docking 背景，ZDOCK/ClusPro 对照组即其自有方法）；它是 B22 rfantibody 那条"抗体设计必须回到展示库"叙事的外部基准证据来源之一 |

## 1. 这篇到底解决什么（一句话）

把 AlphaFold 2（v2.2 / v2.3）与 ColabFold、AFsample 在 **427 个非冗余、高分辨率抗体–抗原复合物**上的建模成功率逐档量化（top-1 与 top-25、CAPRI 四级），并回答一个工程问题：**AlphaFold 自带的置信度分数（model confidence = pTM+ipTM 线性组合、pTM、ipTM、以及界面 pLDDT）到底能不能在下单前判断一个抗体–抗原模型是否可用**——结论是能排序、但判别力有限且有循环风险；同时给出改进方向（更新训练版本、加大采样、改善亚基/CDRH3 预测、MSA 配对）。

### 与 K31（Yin et al., 2022，同一组作者的前作）到底差在哪

本卡只登记**本文自己写明的那几处差别**；凡本文没有复述前作细节的格子，写"本文未复述"，不代 K31 编内容。

| 维度 | K31（前作，Yin et al., 2022） | K32（本文） | 出处（本文原句） |
|---|---|---|---|
| 样本集 | 100 个抗体-抗原复合物 | 442 例送建模、427 例有模型；"with the current study representing a substantial expansion over the cases used previously" | "since our initial test of AlphaFold v2.1 on a set of 100 antibody-antigen complexes (Yin et al., 2022 )" |
| 被测版本与访问方式 | 更旧的 AlphaFold 版本、经 ColabFold 访问 | 本地集群装 AlphaFold v2.2.0（2022-05）与 v2.3.0（2023-02），ColabFold 1.4.0 降为**对比管线**而非被测主体 | "compared to our previous benchmarking that used an older AlphaFold version accessed via ColabFold, and was based on a limited set of 100 antibody-antigen cases (Yin et al., 2022 )" |
| 成败读数 | 前作 top-ranked near-native 不到 10% | 同一口径升到 18%（top-25 22%）；作者把涨幅归给**两因并存**：版本更新 + 测试集不同，因此这两个数不是同集同版本的严格对照 | "This difference is likely due to the newer version of AlphaFold used in this study (v2.2 vs. v2.1), which uses a retrained multimer model, as well as different sets of test cases, with the current study representing a substantial expansion over the cases used previously." |
| 采样设置 | 本文未复述前作的每例模型数 | 每例 **25 个预测**、按 model confidence 排序；为对齐还把 ColabFold 改成每例 25 个；并新增**逐 recycle 回收轨迹**与 **AFsample 大采样**两种采样口径 | "For each complex, 25 predictions were generated and ranked by AlphaFold model confidence score." |
| 置信度指标与精度的相关性 | 前作已用过 model confidence 与界面 pLDDT 类分数（本文称沿用其用法） | 本文把**四个置信量放在同一评测集上做成 ROC AUC 对照表（Table 1）**，并加 Pearson r 对连续 DockQ、以及剔除人为赋值点后重算的敏感性分析；结论是 I-pLDDT 最强、pTM 与 ipTM 单独用并不优于组合分数（前作是否给过同口径 AUC 表，本文未复述） | "We also tested the individual components of the model confidence scores (pTM and ipTM) (Figure S9 ), which did not yield improved correlations with DockQ scores versus model confidence." |
| 失败归因方式 | 本文未复述 | 五类**消融/干预**：模板 oracle（100 例）、MSA 开关、回收逐档（426 例）、版本对照（41 例）、采样对照（37 例）；前作没有这些子集设计 | "Modifications were made to the AlphaFold pipeline to optionally input specific selected PDB templates for each chain." 与 "The removal of MSAs was implemented through modifications to the AlphaFold pipeline, as noted in the Section 4 ." |
| 是否给可用阈值 | 本文未复述 | **仍然没给**任何一个可当闸口的 model confidence / ipTM / pLDDT 数值阈值；只给排序性能（AUC、r、分级分布）。可核验证据：本会话在底稿里检索 threshold 一词，命中 **0 次**（全文只有 date cutoff、resolution、序列 ID、4 Å 距离截断这几类截断，没有置信度阈值） | 见本卡第 8 节的读数分类与第 4 节台账 |


## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **训练集泄漏风险：基准结构可能就在 AlphaFold 的训练样本里**。这是结构预测基准最常见的失效方式。→ 现象/证据：数据集按发布日期硬性截断，"The date cutoff was selected to avoid overlap with the training set of the tested version of AlphaFold (v2.2.0, hereafter denoted as v2.2 for brevity)"，并额外声明 "A template date cutoff of April 30, 2018 was applied to avoid template overlap with benchmarking set"；v2.3 的 41 例子集则改用 "released after the September 30, 2021 training date"。 **应对**：cutoff 日期同时施加到**结构收集**与**模板检索**两处（模板不施加就会把结合态构象直接喂进去）。**留下的代价**：cutoff 只能按 PDB 发布日期粗判——v2.3 "trained on PDB structures released until September 30, 2021"，而 41 例子集正是选在这条线之后，样本因此只剩 41 个。
2. **上一版基准只有 100 例，且成功率低到无法定位原因**（前作 v2.1 的 top-ranked near-native 不足 10%；本文里可整段逐字命中的 ASCII 句是 "We observed higher success in modeling antibody-antigen complexes by AlphaFold in this study versus our previous benchmarking study"，该句后半用了非 ASCII 连字符，本卡不整段引用）。→ **应对**：把集合扩到 442 例（实得模型 427 例），并把"成功率"拆成 top-1 与 top-25 两个口径、CAPRI 四级分开报（"Success rates increased when all 25 predictions per complex were taken into consideration, leading to 37% of the cases achieving acceptable or higher accuracy predictions, 22% achieving medium or higher accuracy predictions, and 6% achieving high accuracy predictions"）；再用冗余标准保证不是同一抗体家族刷分："Sequence criteria for nonredundancy are: (1) heavy chain variable domain sequence ID <90% and full variable domain sequence ID <90%, or (2) no match between antigen chain sequences"，再叠结构冗余剔除："Structural nonredundancy criteria were then applied to the set."（具体线是抗原叠合后重链 Cα RMSD <5 Å 且 ID >70%，数量见第 3 节 A3 与第 4 节阈值行）。**代价**：扩样后**分格子**的样本反而更薄——界面含糖/配体只有 49 例、high 精度类只有 26 例（图 6）、AFsample 只 37 例、模板实验只 100 例；作者自己在图注里承认 "the relatively small numbers of high accuracy cases limit this comparison"。
3. **AlphaFold 不建模糖基化与非蛋白配体，而抗体常直接识别糖**。→ 现象/证据："As glycans are not modeled by AlphaFold and antigen glycosylation can be an important component in antibody-antigen recognition (in some cases with glycans contacted directly by antibodies) (Kappler & Hennet, 2020 ), the subset of complexes with antibody-antigen interface glycans in our set was identified ( N = 45) to assess the impact of antigen glycosylation on modeling outcome."，量化结果（正文：这 49 例里 top-ranked 只出到 medium 档 8%、high 档 0，其余类别 19% 达到 medium+）。作者据此下结论："Thus, the lack of explicit consideration of interface glycans and ligands may reduce modeling accuracy for some antibody-antigen complexes."。 **应对**：把这 49 例（45 糖 + 4 非蛋白配体）单独成组做对比，并进一步**不满足于晶体里看得见的糖**——用抗原来源生物 + 表面暴露 N-糖基化模体到结合位点的距离，再标出 91 例可能有近界面糖（16% vs 20% for N = 287, Figure S4）。**代价**：他们自己写清这套计算判据不可靠（原文承认非糖/配体组的 378 例里有些成员在体内可能确有近界面糖，且糖位点占据率、细胞定位未考虑，需质谱才能定论；Results 2.2 该两句含非 ASCII 连字符，本卡不逐字引用），**方法本身没有改进**（AF2 依旧无糖），只是把误差归了类。
4. **置信度分数需要一个"连续真值"来校准，而 AF2 的分数在无界面接触时没有定义**。→ **应对**：双口径评估（连续 DockQ + 离散 CAPRI），同时测 model confidence、pTM、ipTM 与自建 I-pLDDT（界面残基 pLDDT 均值，4 Å 截断）；对无接触模型赋最低值："Models without antibody-antigen interface contacts were assigned an interface pLDDT value of 30."；随后做**敏感性分析**，把这批点剔掉重算："the correlation between the interface pLDDT and DockQ increased to r = 0.57"、对照 model confidence "the correlation between the model confidence and DockQ" 为 r = 0.53。 **代价（本卡认为最可疑的一条）**：这个 30 是他们自认的人为最低值（Results 2.3 在交代 Figure S10 时把这个赋值称作 arbitrary minimum value），而"有没有 4 Å 内的界面接触"与 CAPRI 判 incorrect 的几何条件高度同源，于是 incorrect vs high 的 AUC = 1.00 有一部分是定义带来的，不是测量能力。
5. **要逐次回收看精度演化，默认 AlphaFold 跑不动**。→ **应对**：换管线而不是降要求——"Predictions were generated with ColabFold due to its faster model generation speed compared to AlphaFold"，并改 `load_models_and_params` 用不同随机种子凑够 25 个模型（"producing five predictions per AlphaFold model parameter"）；为公平比较，反向也对 ColabFold 动手："For fairness of the comparison with the full AlphaFold pipeline's results, ColabFold was modified to generate 25 predictions per complex."。**代价**：拿 ColabFold 得到的回收结论不能直接归给 AlphaFold，作者承认两者 MSA 与模板数据库不同、"with slightly lower success observed for ColabFold"；另外 15 例因显存/内存失败被排除在分母之外。
6. **分不清失败是"亚基折错"还是"界面对错"**（这正是 Type I / Type II 之分类似物）。→ **应对**：做 **oracle 实验**：把实验测定的结合态重链/轻链/抗原链作为各自 template 输入，看天花板——"A substantial improvement in accuracy was observed when experimentally determined antibody-antigen chains were used as individual chain templates"（该句后半给出的成功率是 52%，原文用 near-native top-ranked 表述，本卡第 4 节台账已记）；对照默认模板："On this subset of 100 cases, the use of default templates identified from the AlphaFold pipeline resulted in 18% success"；再加一个非学习的对照——"docking in ZDOCK with bound component inputs achieved comparable, although moderately higher, medium/high accuracy success compared to AlphaFold with bound component templates"（原文该句主语为 rigid-body docking，作者即 ZDOCK 开发组，所以这是拿自家老方法做上限对照）。**代价（本文未解决）**：给了正确亚基也只有约五到六成，且残留失败有明确物理特征："AlphaFold has difficulty predicting the complex structure for antibody-antigen interactions with less favorable computed interface energies and with smaller hydrophobic interface area" —— 界面能量学本身仍是黑洞，本文没有给出任何能提前算出它的方法。
7. **想解释纳米抗体为何明显更容易建模，第一个假设被自己的数据否掉了**。→ 现象/证据："For nanobody-antigen complexes ( N = 132), 27% of cases had medium or higher accuracy"，而重链-轻链抗体只有 14%（N = 295）。他们先假设是交叉链 MSA 更好构建，结果 "after analyzing the MSA depth, we found no statistically significant difference in the number of effective sequences"。**应对**：负结果照登，改口为结构性解释——"This suggests that other factors, such as fewer CDR loops and a smaller search space, may contribute to the observed difference in modeling success."。**代价**：替代解释只是推测（纳米抗体 3 条 CDR vs 6 条），本文没有对照实验去验证它；**这一条本文未解决**。
8. **算力限制直接吃掉样本**。→ 证据："During the structure prediction or feature preparation step in the AlphaFold pipeline, 15 cases failed to complete because of GPU and memory limitations out of a total of 442 test cases." **应对**：失败例从统计里剔除（427 而非 442），并在 ColabFold 对比时进一步缩到 426 例（两法都能出模型者）。**代价**：被剔除的 15 例大概率是超大/多链复合物，成功率分母因此偏乐观，作者未做敏感性分析。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **被评估的预测器**：AlphaFold v2.2.0（2022-05 装在本地集群，全程用 multimer 模型；文中统一称 AlphaFold）、AlphaFold v2.3.0（2023-02）、ColabFold 1.4.0（commit 26de12d3afb5f85d49d0c7db1b9371f034388395，用 localcolabfold 脚本安装）、AFsample（Wallner 2023 的大采样：推理期开 dropout + 随机扰动 + 大量模型池化）。
- **真值与判分**：PDB 实验结构为真值；DockQ 计算 I-RMSD、L-RMSD、fnat、DockQ 分并按 CAPRI 归为 incorrect / acceptable / medium / high 四档。本文把 medium 与 high 合称 near-native。
- **自建的置信度量**：model confidence（AF2 输出的 pTM 与 ipTM 线性组合）、pTM、ipTM 单独、以及 **I-pLDDT** = 界面残基 pLDDT 均值（残基定义：与非氢原子距离 ≤4.0 Å 的界面对手链原子）。
- **物理侧解释变量（只做归因，不做筛选）**：Rosetta InterfaceAnalyzer（REF15 能量函数）算界面能；界面疏水部分 ΔSASA；CD-Hit（80% identity）算 MSA 深度 Neff。
- **对照组方法**：刚体对接 ZDOCK 与 ClusPro（antibody mode），以建模后的未结合亚基为输入。
- **序列/结构注释工具**：ANARCI（去非可变域、AHo 编号、划 CDR），FAST（结构比对做抗原叠合），ProFit v3.1（CDR backbone RMSD），PyMOL 出图，R 的 ggplot2 / ggpubr / ggsignif / pROC / multiROC 做统计。
- **没有用的方法**：MD、QM、自由能微扰、任何湿实验验证、任何新结合蛋白的生成。本文是纯评估型基准。

### A. 主基准管线（数据集 → 建模 → 判分）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | SAbDab 全量抗体结构数据集（2022 年 1 月下载） | 建 v2.2 基准集：按来源、分辨率、冗余度逐条过滤（沿用前作协议） | ①结构分辨率 ≤3.0 Å ②抗原必须是蛋白（按 SAbDab 注释）③与 2018-04-30（AlphaFold v2.2 训练截止日）之前发布、分辨率 ≤9.0 Å 的 Ab-Ag 复合物按序列判非冗余 | 进入建模的 442 个测试例（Table S1；其中 15 例因 GPU/内存失败未出模型，原句见第 2 节第 8 条） |
| A2 | A1 的候选 | 序列层面判冗余 | 重链可变域序列 ID <90% 且完整可变域序列 ID <90%；**或**抗原链序列 BLAST（默认参数，blastp）无命中 | 满足其一即保留 |
| A3 | A2 保留集 | 结构层面判冗余：先用 FAST 叠合抗原，再看抗体 | "Structural nonredundancy criteria were then applied to the set."——具体线是删除抗原叠合后重链 Cα 原子 RMSD <5 Å 且重链可变域/轻链可变域/CDR 拼接序列 ID >70% 者（该句原文含非 ASCII 的 Å 与 Cα 符号，本卡不逐字引用，数量见第 4 节阈值行） | 消除同家族刷分 |
| A4 | A3 保留集 | 剔除抗原有大段未解析区域的结构（避免让模型去猜看不见的部分） | seqres 注释序列与解析区长度差 >70%；或差 >35% 且解析抗原长度 >500 aa | 原文未给该步单独的输出数 |
| A5 | A4 保留集 | 剔除非经典复合物与注释不完整的抗原链 | 手工检查 PDB bioassembly；排除 antibody-tetramerization、dimeric sdAb、constant domain binding、SAbDab 抗原链标注不完整（原文未给该步数量阈值） | 最终 **427 例有模型**（442 − 15 例 GPU/内存失败）；ColabFold 对比用 **426 例**（两法都出模型者） |
| A6 | 427 例的 PDB seqres 序列 | ANARCI 切除非可变域；AF2 v2.2 multimer 建模；模板日期 cutoff 设为 2018-04-30 | 每例 25 个预测（改 `load_models_and_params`，每个模型参数用不同随机种子出 5 个）；排序键 = model confidence | 427 × 25 = **10,675 个模型**；CAPRI 类分布 incorrect 9,062 / acceptable 773 / medium 684 / high 156 |
| A7 | A6 的模型 | 用 DockQ 对实验结构判分，报 top-1 与 top-25 两档成功率 | 成功 = 该档内至少一个模型达到指定 CAPRI 级别；near-native = medium 或 high | top-1：acceptable+ **26%**、near-native **18%**、high **5%**；top-25：**37% / 22% / 6%** |
| A8 | A6/A7 结果 | 按天然复合物属性分组归因 | 界面无糖且无配体 N = 378 vs 有糖/配体 N = 49（45 糖 + 4 非蛋白配体）；nanobody/VHH N = 132 vs heavy-light N = 295 | 有糖/配体组 medium 档 top-ranked 仅 **8%**、high 为 **0**；无糖/配体组 medium+ 为 **19%**；纳米抗体 medium+ **27%** vs 传统抗体 **14%** |

### B. 判据评估与消融实验（本文真正交付的东西）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 10,675 个模型 | 用四种分数（model confidence、pTM、ipTM、I-pLDDT）去区分正确/错误模型 | I-pLDDT 的界面残基定义 = 非氢原子距对手链 4.0 Å 内；无界面接触者 **I-pLDDT 赋 30**；评价用 DockQ 连续相关 + CAPRI 分级 + ROC AUC | I-pLDDT AUC：incorrect vs high = **1.00**、incorrect vs medium+ = **0.92**、三分类 = **0.88**；model confidence = 0.99 / 0.88 / 0.85；ipTM = 0.99 / 0.87 / 0.85；pTM = 0.99 / 0.88 / 0.84。pTM 与 ipTM 单独用**未优于** model confidence |
| B2 | 同 B1 | 敏感性分析：把被人为赋 30 的无接触模型剔掉再算相关 | 剔除"4 Å 内无侧链接触"的数据点 | I-pLDDT–DockQ 相关升到 **r = 0.57**，model confidence–DockQ **r = 0.53**（两者差距被放大，说明 30 这个赋值本身在压低 I-pLDDT 的表现） |
| B3 | 426 例 × 25 | 改 ColabFold 让它导出每一次回收的中间输出，逐 recycle 统计精度与 L-RMSD、CDRH3 RMSD | recycle = 0 表示回收开始前；统计口径 = 每例 25 个预测里指定 CAPRI 档的比例；Wilcoxon rank-sum 比较 recycle 0 vs 3 | 回收进行到第 3 次后达到 medium+ 的预测里约 **50%** 在回收前是 incorrect；recycle 3 的 medium/high 子集为 **106 个预测**（25 × 426 全量的子集）。示范例 PDB 7kd2：I-RMSD 17.98 → 10.90 → 2.52 → 1.45 Å，L-RMSD 49.95 → 4.25 Å，而 CDRH3 RMSD 全程 1.39/1.19/1.27/1.17 Å 基本不动 |
| B4 | 未结合抗体结构（同管线生成，模板 cutoff 2018-04-30） | 比较 unbound 模型 CDR 与复合物中真实 CDR 的 RMSD，与复合模型成败关联 | CDR 定义（AHo 编号）：CDR1 24-42、CDR2 57-76、CDR3 107-138；ProFit 算 backbone RMSD | 高 accuracy 复合模型的 unbound CDRH3 精度显著高于 incorrect 组（**p ≤ 0.05**）；结论限于 CDRH3（其他 CDR 环 RMSD 变异太大，作者改聚焦 CDRH3） |
| B5 | 从 427 例里随机取 **100 例**（要求界面无观测糖、且不属于 partial antigen assembly 类别，因为这两组表现明显不同） | 改 AlphaFold 的模板特征化函数（借 alphafold_finetune 的实现），允许为每条链单独指定 PDB 模板；做三档对照：默认模板检索 / 结合态抗体链 + 结合态抗原链 / 结合态抗体 + 默认抗原 | 成功 = near-native（medium 或 high）top-ranked 的比例 | 默认模板 **18%** → 全结合态链模板 **52%**；对照组 ZDOCK 用结合态输入达到与之一致、略高的水平；作者据此给出天花板："albeit not in all cases (~50%-60% medium/high accuracy success"（原文该句结尾为 50%-60% medium/high accuracy success for top-ranked models，本卡只取 ASCII 可命中的片段）；只用部分实验链模板或借用别的抗体结合的同一抗原则精度下降（Figures S14/S15） |
| B6 | 同 100 例子集的 top-ranked 成败 | 找"给了结合态亚基仍然失败"的物理特征 | 比较 incorrect vs high 组的 Rosetta 界面能分布与疏水界面 ΔSASA，Wilcoxon rank-sum | 两组差异显著（**p ≤ 0.01**）→ 界面能不利、疏水界面面积小者即使有正确亚基也接不上 |
| B7 | 427 例 | 关掉 MSA：把链特征的 `all_seq_msa_features` 改成只含 query 序列（单序列模式），其余不变 | 与有 MSA 的同一批对照比较 near-native 成功率 | "Our results indicated a notable decrease in accuracy when MSA was disabled"（具体降幅正文未给单一数字，见图 5/S14b,c）；另按 CD-Hit 80% identity 算 Neff 分组：incorrect/acceptable/medium/high 例数为 **272 / 63 / 65 / 26**，incorrect vs medium 与 vs high 均 **p ≤ 0.01**；按 MSA 深度分箱看 DockQ 只有"轻微趋势" |
| B8 | v2.2 基准里发布日期在 2021-09-30 之后的 **41 例**子集（并对该日之前结构做非冗余判断） | 用 v2.3.0 重跑（模板 cutoff 改 2021-09-30）；再做拆解实验：把 v2.3 的回收次数降到与 v2.2 相同 | 与 v2.2 在同一 41 例上的成功对照 | near-native top-ranked：**36%（v2.3）vs 23%（v2.2）**；减回收次数后 v2.3 成功率不变 → 收益归因于训练数据（截至 2021-09-30、+30% 训练量、更大 interface crop、更多链、最大回收 3 → 20 加 early stopping），CDR 环精度无显著差异 |
| B9 | **37 例**（AFsample 所有模型都成功生成的子集） | 跑 AFsample（推理期 dropout 随机扰动 + 大规模采样 + 池化不同模型与参数），与同批上 v2.2/v2.3 对照 | 同一 CAPRI 口径、同一 top-N 定义 | top-1 near-native：**51%（AFsample）vs 35%（v2.3）vs 24%（v2.2）**；看 top-25 升到 **59%**；作者明确代价是 "although with substantially higher computational cost"（**具体核时/GPU 时数字正文未给出**） |

**这套流程的骨架值得单独记住**：它不是"用 AF2 设计东西"，而是**先造一个有真值的评测集（A 段），再把每个候选判据放到这个评测集上算 AUC / 相关 / 分级分布（B1–B2），最后用消融实验（模板、MSA、回收、版本、采样量）去定位失败原因**。它的"改进方向"全部是**增加采样或改善输入信息**，没有任何一步是靠调一个自造的阈值把 18% 变成 36%。**要单独记住的还有：全文没有给出任何一个可用作闸口的 I-pLDDT / model confidence 数值阈值**——只有排序性能和 AUC，这就是为什么它不能直接搬进漏斗。

## 4. 关键数字台账（全部来自本地全文）

| 数值 | 含义 | 出处（正文/图注/表注位置，必要时原句） |
|---|---|---|
| 442 / 427 / 426 / 15 | 送建模的测试例 / 实际有模型的例数 / 与 ColabFold 双方都能出模型的例数 / 因 GPU 与内存失败的例数 | Methods 4.2（442、15）；Results 2.1（427）；"ColabFold's modeling success was similar to that of AlphaFold for 426 cases for which both algorithms were able to generate models, with slightly lower success observed for ColabFold (Figure S1 )." |
| 25 个预测/例，排序键 = model confidence | 采样与排序设置（成功率算 top-1 与 top-25 两档） | Figure 1a 图注："For each complex, 25 predictions were generated and ranked by AlphaFold model confidence score." |
| 26% / 18% / 5%（top-1）；37% / 22% / 6%（top-25） | AlphaFold v2.2 在 427 例上 acceptable+ / near-native（medium+）/ high 的成功率 | Results 2.1；"Success rates increased when all 25 predictions per complex were taken into consideration, leading to 37% of the cases achieving acceptable or higher accuracy predictions, 22% achieving medium or higher accuracy predictions, and 6% achieving high accuracy predictions." |
| <10% → 18% | 前作（K31，v2.1）与本文（v2.2）在同一口径（top-ranked near-native）上的读数差 | Results 2.1 末："We observed higher success in modeling antibody-antigen complexes by AlphaFold in this study versus our previous benchmarking study"（同一句后半的 fewer than 10% 与 18% 对照部分原文带 U+2010 连字符，本卡只在第 2 节第 2 条以中文转述，不作逐字引句） |
| ≤3.0 Å；≤9.0 Å；<90%；>70%；<5 Å；>70%；>35%；>500 aa | 集合构建的全部数量阈值：目标分辨率 / 参与非冗余比较的旧结构分辨率 / 可变域序列 ID / 结构冗余的身份与 Cα RMSD / seqres 与解析区长度差 | Methods 4.1 各条，含 "Sequence criteria for nonredundancy are: (1) heavy chain variable domain sequence ID <90% and full variable domain sequence ID <90%, or (2) no match between antigen chain sequences (no hit detected using BLAST (Camacho et al., 2009 ) with default parameters)." |
| 2018-04-30 / 2021-09-30 | 两道防泄漏日期线：v2.2（与 ColabFold）的结构收集与模板检索 cutoff / v2.3 的 cutoff | Methods 4.2："Unless otherwise specified, a template date cutoff of April 30, 2018 was applied for benchmarking AlphaFold v.2.2 and ColabFold, and a template date cutoff of September 30, 2021 was applied for benchmarking of AlphaFold v.2.3, to avoid using bound structures as template." |
| N = 378 vs N = 49（45 糖 + 4 非蛋白配体）；19% vs 8%，high 档 0 | 界面无糖无配体组 vs 有糖/配体组的 top-ranked medium+ 成功率 | Results 2.2 与 Figure 2a/2c 图注 |
| N = 91 vs N = 287；16% vs 20% | 用"来源生物 + 表面暴露 N-糖基化模体到结合位点距离"计算判定的近界面糖分组 | Results 2.2 与 Figure S4。作者自述该计算判据的边界（N-糖位点占据率与细胞定位未考虑，需质谱才能定论）——该句原文含 U+2010 连字符与 Å，本卡不作逐字引句，只给位置指针；其结论已在第 2 节第 3 条以中文转述 |
| N = 132 vs N = 295；27% vs 14% | 纳米抗体/VHH 组 vs 重链-轻链抗体组的 top-ranked medium+ 成功率 | Results 2.2 与 Figure 2c 图注（分组计数 N = 295 与 N = 132 见图注首行；成功率句见正文） |
| Neff 两组无显著差异；CD-Hit 80% identity；incorrect/acceptable/medium/high = 272/63/65/26 | "纳米抗体更好建模"的第一假设（交叉链 MSA 更好建）被否；MSA 深度分组的样本量 | Results 2.2/2.6 与 Figure 6 图注："Numbers of data points in incorrect, acceptable, medium and high categories are 272, 63, 65 and 26." |
| 10,675（本报告推算） | 427 例 × 25 个模型的总数；原文未直接给这个总数，只给四档计数 | 由 Table 1 表注相加得到："which assigned antibody-antigen models into incorrect ( n = 9062), acceptable ( n = 773), medium ( n = 684), and high ( n = 156) accuracy categories." |
| AUC 1.00 / 0.92 / 0.88 | **I-pLDDT** 在 incorrect vs high、incorrect vs medium+、多分类三种口径下的 ROC AUC（Table 1 第一行；正文给的是 medium+ 与 model confidence 的那一对数） | "TABLE 1 Area under the ROC curve (AUC) value for protein model quality classes as a function of different scoring metrics." 与 "Model confidence, ipTM, and pTM are confidence scores from AlphaFold." |
| AUC 0.99 / 0.88 / 0.85（model confidence）、0.99 / 0.87 / 0.85（ipTM）、0.99 / 0.88 / 0.84（pTM） | 另三个置信量在同一评测集上的同口径读数：pTM 与 ipTM 单独用**未优于**组合分数 | Table 1；"We also tested the individual components of the model confidence scores (pTM and ipTM) (Figure S9 ), which did not yield improved correlations with DockQ scores versus model confidence." |
| 4.0 Å；I-pLDDT = 30 | 界面残基定义（与非氢原子距对手链 4.0 Å 内）；无界面接触模型的**人为最低赋值** | Methods 4.4 与 Table 1 表注；逐字可命中的 ASCII 句同第 2 节第 4 条所引（Methods 4.4 原句写作带非 ASCII 连字符的 I-pLDDT 形式，故本卡引 Table 1 表注的同义句） |
| r = 0.57（I-pLDDT）vs r = 0.53（model confidence） | 剔除被人为赋 30 的无接触点后，两个量与连续 DockQ 的 Pearson 相关 | Results 2.3 敏感性分析（Figure S10a,b） |
| 0.88 / 0.75 / 0.85；I-RMSD 0.68 / 3.35（图注）与 3.55（正文）/ 1.02 | 三个示例模型（6nmv high、6j15 acceptable、6v7y medium）的 model confidence 与 I-RMSD；**同一模型 6j15 的 I-RMSD 在图注与正文里是两个数** | Figure 1b/1c 图注 vs Results 2.1 正文；Figure 2b 图注 |
| ~50% | recycle 3 达到 medium+ 的预测中，回收开始前本是 incorrect 的比例 | "In fact, approximately 50% of predictions of medium or higher accuracy after the third recycling iteration were incorrect models before recycling iterations (Figure S11 )." |
| 426 complexes × 25；106 predictions；recycle = 0 为回收前 | 回收分析的分母与 medium/high 子集规模 | Figure 4a/4b 图注："Success rate is defined as the proportion of predictions of specific level of CAPRI criteria in a total of 25 prediction per complex, 426 complexes total, at the given recycle." |
| PDB 7kd2：I-RMSD 17.98 → 10.90 → 2.52 → 1.45 Å；L-RMSD 49.95 → 24.68 → 5.42 → 4.25 Å；CDRH3 RMSD 1.39 / 1.19 / 1.27 / 1.17 Å | 回收把**对接位姿**救回、但**救不动 CDRH3 构象**的示例（界面由 incorrect 升到 medium，CDRH3 全程不动） | Figure 4d 图注（四档数值原文含 Å，此处只作位置指针）；性质句可逐字命中的 ASCII 原句："This prediction was of incorrect accuracy before recycling iterations and was improved to a medium accuracy prediction at Recycle 3." |
| 100 例；18%（默认模板）→ 52%（结合态链模板）；~50%-60% 天花板 | 模板 oracle 实验：给了正确亚基后的成功率与作者自己划的天花板 | Figure 5 图注："Benchmarking was performed on a total of 100 antibody-antigen complexes." 与 "Antibody-antigen modeling success of AlphaFold by utilizing (a) templates identified through the default template search protocol, (b) bound antibody and antigen chains as templates, (c) bound antibody and default antigen chains (identified by the default search protocol) as templates."（18% 与 52% 所在的完整原句含非 ASCII 连字符，本卡在第 2 节第 6 条引的是同句中 ASCII 可命中的前半段，数字另在本行与第 3 节 B5 记录）；"Using only subsets of experimentally determined antibody-antigen chains as templates, as well as use of experimentally resolved antigens bound to other antibody structures, resulted in a decrease in model accuracy, compared to using all experimentally determined chains as templates (Figures S14 and S15 ; Supplementary Results )." |
| 41 例；36%（v2.3）vs 23%（v2.2）；训练数据 +30%；recycles 3 → 20 加 early stopping；减回收次数后 v2.3 成功率不变 | 版本对照子集与其结论：涨点归训练数据而非采样步数 | "This version also increased the maximum number of recycles, from 3 recycles in v.2.2 to 20 recycles in v.2.3, with early stopping, and utilized larger interface regions (crops) and more chains during training." |
| 37 例；51%（AFsample）vs 35%（v2.3）vs 24%（v2.2）；top-25 59% | 大采样对照子集；与上一行的 41 例**不是同一个子集**，所以 35% 与 36% 不可当同一读数比较 | "When the top 25 predictions were considered, AFsample's medium or higher success rate increased to 59%." |
| 单价成本：无 | AFsample 的计算代价只有定性一句，全文没有核时/GPU 时数字 | "although with substantially higher computational cost" |
| 算力与软件口径 | 本地集群 NVIDIA Titan RTX 与 Quadro 6000；ColabFold 1.4.0（commit 26de12d3afb5f85d49d0c7db1b9371f034388395）；SAbDab 于 2022 年 1 月下载；AF v2.2 于 2022-05 装、v2.3 于 2023-02 装；CDR 定义 AHo 24-42 / 57-76 / 107-138 | Methods 4.2 与 4.5："AlphaFold and ColabFold modeling runs were performed using NVIDIA Titan RTX and Quadro 6000 GPUs." |
| p ≤ 0.05 / 0.01 / 0.001 | 各处 Wilcoxon rank-sum 显著性档位（界面能、Neff、I-pLDDT 分档、unbound CDRH3、回收前后） | Figure 2d、Figure 3、Figure 4、Figure 6 图注与对应正文 |


## 5. 结论——作者说了什么

1. **基准读数**：AlphaFold v2.2 在 427 例上 top-1 为 acceptable+ 26%、near-native 18%、high 5%；把 25 个预测全算进来升到 37% / 22% / 6%。相比前作（K31：v2.1、100 例、top-ranked near-native 不到 10%），作者把涨幅同时归给"版本更新（v2.2 的重训练 multimer 模型）"与"测试集不同（本文明显扩样）"两件事，没有只归给版本。
2. **置信度分数可用，但只有排序意义**：作者用四种量（model confidence、pTM、ipTM、界面 pLDDT）去区分正误模型，结论是界面 pLDDT 最好、可作首要质量指标（Results 2.3 末句）；单独用 pTM 或 ipTM **不比组合分数好**："We also tested the individual components of the model confidence scores (pTM and ipTM) (Figure S9 ), which did not yield improved correlations with DockQ scores versus model confidence."；他们给出的理由是界面 pLDDT 只盯抗体-抗原界面，而 ipTM 把重轻链、多条抗原链等**所有链间界面**一起算，会被无关部分带偏（Results 2.3 倒数第二段）。
3. **成败与天然复合物属性绑定**：界面有糖/非蛋白配体者成功率显著低；纳米抗体（27%）明显高于重轻链抗体（14%）；界面能越负越容易成："We found that more negative interface energies, indicative of more energetically favorable protein-protein interactions, are associated with higher AlphaFold modeling success."；但对纳米抗体优势的机制，作者只给出**否定的结果 + 未验证的推测**："However, after analyzing the MSA depth, we found no statistically significant difference in the number of effective sequences (N eff , a measure of the effective sequence count in an MSA [Jumper et al., 2021a ]) between the two types of complexes (Figure S5 )." 与 "This suggests that other factors, such as fewer CDR loops and a smaller search space, may contribute to the observed difference in modeling success."
4. **回收能救位姿、救不动环**："Our analysis demonstrates an increase in model accuracy as recycling iterations progress (Figure 4a )."；"In fact, approximately 50% of predictions of medium or higher accuracy after the third recycling iteration were incorrect models before recycling iterations (Figure S11 )." 但因 CDRH3 变异太大，作者把环的分析收窄："Given the high variability in CDRH3 RMSD (Figure S6 ), compared to the RMSD of other CDR loops, we focused our analysis of CDR loops on the CDRH3."
5. **亚基（尤其 CDRH3）预测准是复合物成功的前提**：为此他们改造管线喂入结合态链模板——"Modifications were made to the AlphaFold pipeline to optionally input specific selected PDB templates for each chain."——成功率从 18% 抬到 52%，但作者明说天花板只有约五到六成；只用部分实验链模板或借用别的抗体结合的同一抗原则精度下降。
6. **MSA 不能去掉**："Despite the lack of explicit coevolutionary signal, our data show that the inclusion of diverse sequence information in MSAs is helpful for maintaining AlphaFold's modeling success of antibody-antigen complexes." 按 MSA 深度分箱看 DockQ 只有轻微趋势，作者据此提出"给浅 MSA 的复合物加深 MSA"这一改进方向。
7. **涨点来自版本与采样，不来自任何判据**：v2.3 在同一 41 例上把 near-native top-1 从 23% 提到 36%，且"Additional benchmarking revealed that reducing the number of recycling iterations in v2.3 to match the number of recycling iterations in v2.2 resulted in unchanged modeling success for v2.3 (Figure S17 ; Supplementary Results )."（即收益不来自回收次数）；AFsample 大采样再抬到 51%（top-25 59%），作者同时给出代价句 "although with substantially higher computational cost"。
8. **对使用者的定位**：作者认为在当前成功率与置信度打分能力下，AlphaFold 对这类复合物"可能实际有用"，并且能补充或辅助实验结构解析（Discussion 末段）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

以下为推断。

1. **作者交付的是"排序能力"，不是"判定线"**。全文把置信度分数只用在两处：给同一复合物内部的 25 个模型排序，以及在带真值的评测集上算 AUC / Pearson r。没有任何一句给出"分数高于多少就可以用"。→ 对我们的做法：指标先上考卷再进漏斗；没有考卷时，指标只许用于排序与分组归因，不许写进判定线。
2. **最高的那个 AUC = 1.00 里有定义循环**。界面 pLDDT 的界面残基定义（4.0 Å 内有非氢原子接触）与 CAPRI 判 incorrect 的几何条件同源，而"完全无接触"被人为赋 30 分——等于同一几何条件被数了两遍（一次进标签、一次进分数）。他们剔除这批点后相关升到 r = 0.57，恰好说明这个赋值在**压低**表观表现，也说明读数对"如何定义无接触"敏感。→ 我们的判定线若用同一套距离/接触定义既标"催化位点存在"又给"支持分"，会造出同类假高分（与 B09 卡里"生成阶段用过的指标不能再当筛子"是同一条教训的两个方向）。
3. **本文所有提升都发生在生成侧**（更新训练版本、加大采样、喂入结合态模板、加深 MSA），**没有一项发生在筛选侧**。也就是说这篇基准给出的"进步路径"是信息更多 + 样本更多，而不是阈值调得更准。我们把预算压在筛子与长时 MD 上的次序，与这篇的证据方向相反。
4. **作者的失败归因分两个等级，只有后者是因果证据**：糖/配体、抗体类别、界面能、Neff 都是**分组相关观察**（没有干预）；模板 oracle、MSA 开关、回收逐档、版本对照、AFsample 五项才是**干预/消融**。→ 我们机制层的判断需要干预式可证伪量（换底物、失活突变、竞争反应对照），再叠一个相关性分数不构成机制证据。
5. **文内分母是碎的，跨表百分比不可相减**：442 / 427 / 426 / 100 / 41 / 37 各用一套口径。v2.3 的 36%（41 例子集）与 AFsample 对照里的 35%（37 例子集）不是同一个数集，"36% vs 23%"与"51% vs 35%"不能串成一条增长曲线。引用时必须带子集名。
6. **这是回顾性基准，没有前瞻实验**（对照 B09：那边有四个新靶的下单验证）。所以本文能支持"某判据在既有真值集上有判别力"，**不能**支持"按它筛完就会做出东西"。任何拿这篇当"成功率背书"的写法都是越界。

## 7. 局限与失败（作者的 + 我们读出的）

**作者写明的**

- 样本薄的地方直接承认：high 精度类例数太少限制 CDR 环与成败的比较（见第 2 节第 2 条所引图注句）；模板实验只 100 例；AFsample 只 37 例；v2.3 只 41 例。
- 糖的判定只是计算近似：糖位点占据率与细胞定位未考虑，作者要求质谱级别的验证才能定论（Results 2.2）。
- 为效率只建模可变域，恒定域被切掉："For efficiency, we only utilized the variable domains of the antibody sequences for modeling." 因此所有读数都不含恒定域参与的结合面。
- ColabFold 与 AlphaFold 不是一回事：两者 MSA 构建/配对方式与序列、模板库不同，回收分析（B3）与 ColabFold 对比（A6/A7）的结论不能无条件归给 AlphaFold——"The difference in success may be due to factors such as different MSAs or structural templates, as ColabFold and AlphaFold employ distinct approaches for building and pairing MSAs, and utilize different sequence and template databases."
- 界面能量学没解决：给了结合态亚基也只有 ~50%-60%，失败例与不利的 Rosetta 界面能、小的疏水界面面积显著相关，作者没有给出任何可提前算出这一项的方法。
- 算力失败被剔但不做敏感性分析：15 例（442 分之 15）因 GPU/内存失败直接从分母消失。
- AFsample 的代价只有定性一句，全文无核时/GPU 时数字，故"多采样值不值"无法量化。

**我们读出的**

- **无前瞻、无湿实验、无 MD/QM**：本文全部证据是"用 DockQ/CAPRI 对静态几何打分"。它不能为任何涉及动力学或化学反应的主张供证。
- **分布外推问题**：427 例是"已被实验解析、分辨率 ≤3.0 Å、抗原是蛋白、可变域可建模"的天然复合物，天然偏向表达良好、构象稳定、经典表位的体系。对工程酶 / 非天然底物 / 大段柔性区域那类我们要判的对象，这篇的成功率与 AUC 都不代表。
- **判别力读数没有做样本外验证**：Table 1 的 AUC 与相关都在**同一个用来设计分析的评测集**上事后算出，全文没有划分训练/验证、也没有报告分数在独立集上的表现，因此 0.88–1.00 这一档存在高估风险。
- **文内自相矛盾的读数**：同一个 6j15 acceptable 模型的 I-RMSD，图 1c 图注写 3.35 Å，正文写 3.55 Å（本卡两处都记、不替作者取舍）。这类不一致意味着引用该文数值时要指定是图注还是正文。
- **未取到的部分使本卡无法复算绝对数**：Supplementary Results 与 Figure S1–S17、Table S1 逐条清单、图 1/2/5/7/8 柱状图原始数值都没有本地副本，因此本卡凡只写百分比之处，其例数不可由本卡推出（见第 0 节"未取到的部分"）。
- **"置信度能不能当阈值"这个问题，作者其实只答了一半**：他们证明了这些分数**能排序**，没有证明它们**能设线**；把前者当成后者是本文最常见的误读方式（本卡第 8 节据此禁止搬用）。

## 8. 迁移判断：哪些能搬、哪些不能搬

**这一节只回答一个问题：AlphaFold 的置信度指标能不能当筛选阈值。**

先分清作者给的是哪一类读数（决定它能被搬去干什么）：

| 读数 | 本文给的具体量 | 它是什么 | 它**不是**什么 |
|---|---|---|---|
| Pearson 相关（对连续 DockQ） | 界面 pLDDT r = 0.57、model confidence r = 0.53（剔除人为赋 30 的点之后；Figure 3a,b 给全量点的相关与 p 值） | 线性一致性强度 | 不是"分数高则模型对的概率"；r = 0.57 只解释 DockQ 方差的约三分之一（本报告推算 r^2 约 0.32） |
| ROC AUC（对 CAPRI 四级） | 界面 pLDDT 1.00 / 0.92 / 0.88，model confidence 0.99 / 0.88 / 0.85，ipTM 0.99 / 0.87 / 0.85，pTM 0.99 / 0.88 / 0.84 | 随机取一对样本排对序的概率（成对排序能力） | 不是工作点上的精度；AUC 高完全可以伴随"在你选的那个阈值下阳性预测值很低" |
| 分组分布 + Wilcoxon 检验 | 图 3c,d、图 2d、图 6 的按 CAPRI 档分组的分数分布与 p 值 | 组间是否可分 | 不是可用于单例判决的规则 |

**适用边界**（作者自己给的条件）：只在这 427 个抗体-抗原复合物、v2.2 的每例 25 个模型池、CAPRI 四级标签、界面残基按 4.0 Å 定义、且真值来自同一批 PDB 实验结构的范围内成立。ipTM 与 model confidence 还被作者明说会被"无关的链间界面"带偏（多链体系里尤其如此）；界面 pLDDT 的优势正来自它只看界面。

**可迁移（怎么用）**

1. **评测集先行的组织方式**（A 段 → B1/B2 → B3–B9）：先造带真值的池子，再把每个候选判据放上去算相关/分级/AUC，最后用消融找失败原因。本库的判据标准里"判据不上考卷就不许进漏斗"这条，本文是方法学上的又一例证（与 B09 的 A 段同理，但本文的真值来自公共数据库而非自家湿实验台账）。
2. **指标的两种合法用法**：同批候选内部**排序**（AlphaFold 自己就是拿 model confidence 排 25 个模型），和按成败分组做**归因对比**。我们的判定线里若出现 pLDDT/ipTM，只允许这两种用法。
3. **局部分子优于全局汇总**：界面残基 pLDDT 优于跨所有链的 ipTM。→ 多域/多链体系里应只读催化界面对手残基那一部分的分数，不读整链汇总。
4. **敏感性分析照搬**（本文最便宜也最值得学的一步）：把人为赋值/无接触的那批数据点剔掉重算，看结论是否变化。任何"我们自造的最低分/缺测补零"都应做这一步再报数。
5. **失败分型 + 干预**：模板 oracle、MSA 开关、回收、版本、采样五项是干预实验；糖/抗体类别/界面能/Neff 是观察。我们的机制层结论要按前者设计（可干预、可证伪），不能停在后者。

**不可迁移（为什么不能照搬）**

1. **判的东西不同**：本文判"结合位姿对不对"（I-RMSD / L-RMSD / fnat 的静态几何），我们的判定线问"三步催化事件能否发生、副反应会不会抢"。界面 pLDDT 高分既不必要也不充分；把 binder 侧的 ipTM/pAE 阈值当酶活闸口已被本库判据标准明令禁止。
2. **作者根本没给阈值**：全文没有一个"分数高于 X 可用"的数字，能搜到的只有分位数化的成功率与 AUC。因此任何"按 ipTM > 0.7 / pLDDT > 80 设线"的做法都是我们自造的，不能引本文作支持。
3. **读数类型不允许当概率用**：AUC 与 Pearson r 是排序一致性，本文没有校准（无可靠性曲线、无 PPV/召回随阈值的曲线），所以不能把 0.88 之类的数换算成"我们判定线上的通过概率"。
4. **循环定义风险**：本文最高的 AUC = 1.00 部分来自"指标与标签共用同一个 4 Å 几何判据"。我们若用同一距离定义既标注催化位点、又给出支持分，会重演同一种假高分。
5. **标签与分布都不可外推**：他们有 427 例公共真值；我们的目标（天然参照酶）**至今没有一条被产物化学确认的阳性标签**，AUC 这类读数在我们这里连分母都凑不出来。同时他们的样本是"已被解析、分辨率 ≤3.0 Å"的天然体系，工程酶/非天然底物属分布外。
6. **成本不可知**：AFsample 的提升（51% / 59%）伴随一句定性的更高计算代价，全文无核时数字 → 不能用本文论证"多采样在我们预算内划算"。

一句话结论：**本文支持"置信度分数可用来排序与归因"，不支持"置信度分数可设成筛选闸门"**；在我们没有阳性标签的现实下，把 ipTM/pLDDT 写进判定线属于自造阈值，只能作为排序特征存在。


## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K32_PMC10751731_text.txt

- **底稿唯一性**：本卡所有英文引句只对照上面这一份纯文本逐字核验。同一编号另有同源 XML `data/literature_cards/fulltext/K32_PMC10751731_fullTextXML.xml`（Europe PMC `fullTextXML`，2026-10-20 本地抓取，138,485 B），本会话实测 `norm(strip_tags(XML)) == text.txt`（两份都归一到 66,514 字符，逐字符相等），所以 text.txt 就是那份 XML 的剥离版，不存在 Europe PMC / NCBI 两套抽取文本句子内参考文献编号不同的问题；核验器按规则只把 `.txt` 计入可比对底稿（`.xml` 被排除）。
- **引句字符集**：本卡 66 条被门禁识别为引句的片段**全部为纯 ASCII**（不含 U+2010 连字符、Å、Cα 等非 ASCII 字符），因此逐字比对不受字符归一影响；凡原文只能用非 ASCII 字符才说清的句子（界面 pLDDT 赋 30 的 Methods 句、<5 Å / Cα 冗余线、near-native top-ranked 类表述），本卡一律改为**位置指针 + 中文转述**，不硬凑引句。另：本会话实测底稿里 threshold 一词命中 **0 次**（不区分大小写），这是第 1 节差别表末行与第 8 节"作者没给阈值"这两条断言的依据。
- **登记项对照**：`sources/cost-benchmarks.md` §3.4 论文 B（本卡未修改该文件，仅作登记底稿参与"至少命中一份"的检查）。
- **写作时踩到并改正的四处引用问题**（都是本项目门禁设计要抓的那类）：① 第 3 节 A1 原写的引句用省略号跨掉了中间半句（15 cases failed to complete 一句），不是原文连续片段，已改为在第 2 节第 8 条给完整原句、A1 只留指针；② 抄版本对比句时把 "20 recycles in v.2.3" 误写成 v2.3（作者正文用 v.2.3、图 8 图注用 v2.3，两种写法在文内并存），按正文原样改回；③ 界面 pLDDT 赋 30 那句在 Methods 里写作带非 ASCII 连字符的形式，本卡改引 **Table 1 表注里的同义句**；④ 第 2 节第 2、3 条原先抄了含非 ASCII 连字符的句子，已换成同段落纯 ASCII 原句，并把 8% / 19% / <10% 这些数字留在中文叙述里（数字本身均可在全文搜到）。教训：同一篇内版本号与连字符写法不统一时，必须逐字抄而不是按记忆归一。
- **本卡自检**：`scripts/verify_literature_cards.py`，参数 `--only K32 --no-report`（不写 selfcheck.txt / rollout_status.tsv，避免覆盖其它代理产物）。逻辑：把卡内被直双引号包住、不含中日韩字符、≥20 字符且 ≥12 个字母的片段视为逐字引句，在 `引句底稿` 声明的那份全文里做 `norm()` 后（NFC + 实体解码 + 智能引号/破折号转 ASCII + 空白折叠）逐字查找，任一条不命中即 FAIL、退出码 1。本轮实测输出：**PASS K32 quotes=66/66，退出码 0**（改动前同一命令为 FAIL，唯一未命中项就是上面第 ① 条）。
- **反向自测**（本会话实跑，只在内存里改、未落盘）：把第 4 节台账里 "Numbers of data points in incorrect, acceptable, medium and high categories are 272, 63, 65 and 26." 的 26 改成 27 ⇒ 该条立即转为 MISS（脚本报 1 条不命中）。也就是说"改一个数字就会被抓到"是可执行的，不是声明。
- **内容边界**：本卡没有引用任何未取到的补充材料数值；凡正文只有图而无数值之处，均写"正文未给出，仅有正文描述"。K31（前作）的细节一律以"本文所述"为限，凡本文未复述的格子写"本文未复述"，未代前作编内容。
- **CSV 字段映射**：第 3 节 ↔ `候选生成方法 / 计算筛选判据 / 阈值数字`；第 4 节 ↔ `候选数递减 / 实验命中率 / 成本统计`；第 1 节差别表与第 8 节 ↔ `在方法演进链的位置`；本行 ↔ `原文出处指针`。

<!--CSV回填
work_type=论文（结构预测基准 + 置信度判据评估；非设计论文，无湿实验）
target=抗体-抗原复合物：427 例非冗余高分辨率 PDB 复合物（纳米抗体/VHH 132 例、重轻链抗体 295 例；界面无糖无配体 378 例、有糖或配体 49 例）
backbone_generation=不生成新蛋白序列/骨架；仅对既有 PDB seqres 序列（ANARCI 切至可变域）用 AlphaFold v2.2.0 与 v2.3.0 multimer、ColabFold 1.4.0、AFsample 建模，每例 25 个预测、按 model confidence 排序
computational_filters=被评估的置信度判据：model confidence（pTM+ipTM 线性组合）、pTM、ipTM、界面 pLDDT（I-pLDDT，界面残基=与非氢原子距对手链 4.0 Å 内的残基，均值；无接触赋 30）；真值判分 DockQ（I-RMSD/L-RMSD/fnat/DockQ + CAPRI 四级）；归因变量 Rosetta InterfaceAnalyzer 界面能（REF15）、疏水界面 ΔSASA、CD-Hit（80% identity）算 Neff、ProFit 算 CDR backbone RMSD
thresholds=集合构建：分辨率 ≤3.0 Å；与 2018-04-30 前发布、分辨率 ≤9.0 Å 的 Ab-Ag 复合物按序列非冗余（可变域 ID <90% 或抗原 BLAST 无命中）；结构冗余 <5 Å 重链 Cα RMSD 且 ID >70% 剔除；seqres 与解析区长度差 >70%（或 >35% 且解析抗原 >500 aa）剔除；模板日期 cutoff 2018-04-30（v2.2/ColabFold）与 2021-09-30（v2.3）；I-pLDDT 界面定义 4.0 Å、无接触赋值 30；CDR 定义 AHo 24-42/57-76/107-138；统计显著性 p ≤ 0.05/0.01/0.001。判据侧只有排序性能读数（AUC 与 Pearson r），全文未给任何可作筛选闸口的 model confidence/ipTM/pLDDT 数值阈值
md_used=否（全文无分子动力学）
qm_used=否（全文无量子化学/自由能微扰）
experimental_methods=无湿实验；真值全部取自 PDB 已解析实验结构（X 射线/cryo-EM），以 DockQ 与 CAPRI 判分；作者建议未来用质谱确定抗原糖型（本文未做）
pipeline_counts=442 例送建模 → 427 例有模型（15 例 GPU/内存失败）→ 426 例用于 ColabFold 双方对比；427 × 25 = 10,675 个模型（本报告相加，原文只给四档计数 incorrect 9,062 / acceptable 773 / medium 684 / high 156）；消融子集：模板 oracle 100 例、v2.3 对照 41 例、AFsample 对照 37 例、MSA 深度分组 272/63/65/26 例
hit_rate=AlphaFold v2.2（427 例）：top-1 acceptable+ 26%、near-native 18%、high 5%；top-25 37%/22%/6%。同口径 v2.3（41 例）near-native top-1 36% vs v2.2 23%。AFsample（37 例）top-1 near-native 51%，同批 v2.3 35%、v2.2 24%；top-25 59%。分组：界面无糖无配体 19% vs 有糖/配体 8%（high 0）；纳米抗体 27% vs 重轻链抗体 14%；结合态链模板 52% vs 默认模板 18%（作者天花板约 50%-60%）
best_metric=界面 pLDDT（I-pLDDT）：incorrect vs high AUC 1.00、incorrect vs medium+ 0.92、多分类 0.88；model confidence 0.99/0.88/0.85、ipTM 0.99/0.87/0.85、pTM 0.99/0.88/0.84。剔除人为赋值 30 的无接触点后与 DockQ 的 Pearson r：I-pLDDT 0.57、model confidence 0.53。原文未给 Kd/活性类实验量（无湿实验）
cost_or_stat_note=全文无核时/GPU 时或金钱成本数字；AFsample 代价仅一句 "although with substantially higher computational cost"；算力口径只有 NVIDIA Titan RTX 与 Quadro 6000、本地 IBBR 与 Zaratan HPC；统计仅 Pearson 相关与 Wilcoxon rank-sum（p ≤ 0.05/0.01/0.001），ROC AUC 用 R 的 pROC/multiROC；15 例算力失败被剔出分母且未做敏感性分析；high 精度只有 156 个模型/26 例；同一模型 6j15 的 I-RMSD 在图注 3.35 Å 与正文 3.55 Å 之间不一致
role_in_timeline=K31（Yin et al. 2022，100 例、AlphaFold v2.1、经 ColabFold 访问）的同组后续：样本扩到 427 例、被测版本换成本地 v2.2/v2.3、每例固定 25 个预测并新增回收/模板/MSA/采样四类消融，并第一次把抗体-抗原置信度指标做成同集 ROC AUC 对照表（Table 1，界面 pLDDT 最优）；它给"AF 用于抗体-抗原建模能排序但不能设线"提供了基准证据，是 B22 rfantibody 那条"抗体设计必须回到展示库"叙事的外部对照来源之一；本身不含设计、不含湿实验
source_pointer=data/literature_cards/fulltext/K32_PMC10751731_text.txt（Europe PMC fullTextXML 剥标签纯文本，66,985 B）+ 同名 _fullTextXML.xml（138,485 B）；登记项 sources/cost-benchmarks.md §3.4 论文 B；文章 https://pmc.ncbi.nlm.nih.gov/articles/PMC10751731/ · DOI 10.1002/pro.4865 · PMID 38073135；代码 https://github.com/piercelab/alphafold_v2.2_customize
CSV回填-->

