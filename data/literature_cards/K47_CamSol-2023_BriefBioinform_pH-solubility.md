# [K47] 用序列预测 pH 依赖的蛋白溶解度——CamSol 3.0，把 配方 pH 该定在哪 变成下单前的免费计算

Oeller M, Kang R, Bell R, Ausserwöger H, Sormanni P, Vendruscolo M（剑桥大学 Misfolding Diseases 中心）
Briefings in Bioinformatics 2023, 24(2):bbad004 · DOI 10.1093/bib/bbad004 · PMID 36719110 · PMCID PMC10025429
开放获取（CC BY-NC 4.0）· 工具地址 https://www-cohsoftware.ch.cam.ac.uk/index.php/camsolph

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K47**（组：通用方法学; 口径对照；文献类型：方法） |
| 文献 | Oeller M, Kang R, Bell R, Ausserwöger H, Sormanni P, Vendruscolo M. Sequence-based prediction of pH-dependent protein solubility using CamSol. Brief Bioinform 2023;24(2):bbad004 |
| 身份核验 | 开写前读了底稿开头 1,500 字符：题录区标题、DOI 10.1093/bib/bbad004、PMC10025429、PMID 36719110 三项与 CSV 行完全一致，确认本底稿就是本篇（不是引用它的论文） |
| 本文取回方式 | Europe PMC 通道（inventory 记录：先 search 后取 fullTextXML，抓取记录见 `data/literature_cards/inventory.json` 的 K47 条目），2026-10-20 本地抓取 |
| 本地全文 | `fulltext/K47_PMC10025429_fullTextXML.xml`（原始 XML）→ 去标签纯文本 `fulltext/K47_PMC10025429_text.txt`（36,512 B，归一化后 36,483 字符，单行无换行） |
| 对照底稿 | `sources/cost-benchmarks.md` 第 198 行（§六 失败模式→计算判据 映射表的 包涵体/不溶 行），CSV 的 原文出处指针 亦指向该处；本卡把它从摘要级口径升级为全文级口径 |
| 证据级别 | **全文级**（本卡 113 条引句实例、去重后 99 条，全部在该纯文本里逐字命中；门禁结果见 §9） |
| 与 CSV 不一致处 | CSV 行 证据级别 列仍为 摘要级（旧值），该列不在 14 键回填范围内，未擅自改表 |
| 未取到的部分 | 补充材料 CamSol_pH_SI_R1_bbad004 未在本仓库存档：Table S1（20 种氨基酸 pKa 全表）、Table S2（BSA 三种 pKa 方案逐残基对照）、Table S3/S4（逐点实测溶解度与全部相关系数）、Figure S1–S7（含各蛋白 pH 曲线与 α-synuclein/insulin 的无校正对照）。凡正文只写 见 Table S3 之类、本卡只能标注为 正文未给数值 |
| 公式不可复算 | 纯文本抽取把公式打断了：LogD 的定义只剩一句带 where 的文字描述（本卡 §3 引），δ 的定义式与图中公式内容无法从底稿复算；这是抽取通路的已知损失，不是本文没写 |

## 1. 这篇到底解决什么（大白话）

CamSol（2015 年的老工具）做的事是：只给一条氨基酸序列，就逐残基打一个溶解度分，用来提前判断哪些区段容易不溶、哪些突变会让蛋白变溶。它的痛点是 pH 处理极其粗糙——原文举的例子就是 "For example, all histidine residues would acquire a charge of +1 for an input pH below 6.5."，作者自己判定这种描述 "Although rooted on general physicochemical principles, this description of the pH-dependence of residue p K a is very coarse, and can be substantially improved."

这一篇是 CamSol 3.0，把 pH 真正做进模型，三处改动：（i）用 Henderson-Hasselbalch 方程把整数电荷换成部分电荷；（ii）把疏水项从只看中性态的 logP 换成随 pH 走的 logD；（iii）残基 pKa 给三套可选来源（更新过的表值 / 需要结构的 PROPKA / 纯序列的 IPC 2.0），外加把 C 端 His-tag 的组氨酸 pKa 手工从 6.5 降到 6。

难点在验证数据：公开的 同一蛋白不同 pH 下的溶解度 数据几乎没有——"Since the availability of high-quality solubility data at varying pH values is limited, we set out to carry out experimental measurements of relative solubility." 所以作者自己用 PEG 沉淀法测了 7 个蛋白（含一个纳米抗体、一个全长 IgG4 及其突变体、一个内在无序蛋白、一个多肽胰岛素）在 pH 3–9 的相对溶解度，再和预测算 Pearson 相关，交付的结论是 "Our results show that CamSol not only captures the overall trend in solubility upon pH changes well, but the predicted values are also highly correlated with the experimental values with Pearson's coefficients of correlation always greater than 0.67"（最好的两个是 IgG4 的 0.96 与其突变体的 0.97）。

**它交付的是 pH 曲线的形状与相对排序（谁比谁更溶、最不溶的 pH 在哪），不是绝对溶解度浓度**。摘要把它定位成给开发管线用的廉价预筛："Since experimental methods for measuring protein solubility are material intensive and time consuming, computational methods have recently emerged to enable the rapid and inexpensive screening of solubility for large libraries of proteins, as it is routinely required in development pipelines." 而这一版要补的缺口是："there is still an unmet need for sequence-based predictors capable of accurately assessing the effects of formulation pH on the solubility of proteins."

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **pH 只能靠粗糙的整数电荷，是本文的起点问题**。旧版 CamSol 已经能吃进 pH，但做法是按表定质子化状态，原文举例 "For example, all histidine residues would acquire a charge of +1 for an input pH below 6.5."，并据此判定 "Although rooted on general physicochemical principles, this description of the pH-dependence of residue p K a is very coarse, and can be substantially improved." **他们做了什么**：改用 Henderson-Hasselbalch 方程按 pH 与 pKa 的比值给每个可电离残基一个小数电荷（"to determine the ratio between protonated and charged residues to estimate the partial charge of each amino acid."），并给 N 端酰胺与 C 端羧酸也加上电荷（"We also introduced charges for the amide group at the N-terminus and the carboxylic acid at the C-terminus."）。**仍留下的代价**：偏电荷只是单残基对 pH 的独立响应，残基间的静电耦合要靠 PROPKA 那类外部预测器带入，CamSol 自身不做自洽迭代；选哪套 pKa 会明显改变结果（见第 6 条），而文中给的是逐蛋白择优，没有可先验执行的统一选择规则。

2. **没有现成的 pH 依赖溶解度数据可供验证**。"Since the availability of high-quality solubility data at varying pH values is limited, we set out to carry out experimental measurements of relative solubility." **他们做了什么**：自己做实验——用已发表的 PEG 沉淀法测相对溶解度（"The relative solubility of proteins was measured using a recently developed polyethylene glycol (PEG) solubility assay"），并把验证集刻意铺宽：球状蛋白、纳米抗体、全长 IgG4、内在无序蛋白、多肽各占一席（"We illustrate the resulting pH-dependent predictions on a variety of antibodies and other proteins to demonstrate that these predictions achieve an accuracy comparable with that of experimental methods."）。**仍留下的代价**：验证集只有 7 个蛋白加 1 个突变体、全部由本组自测或送样（IgG4 由 Novo Nordisk 提供），无独立第三方数据集；读出是 PEG 沉淀拐点这种相对代理量，不是引言里定义的临界浓度（"The solubility of proteins is defined thermodynamically in terms of the critical concentration"，该句后半带文献编号故不整句引），因此 R 高不等于能报出 mg/ml 级的绝对溶解度。

3. **实验本身在两端就测不准，而两端恰是最需要预测的地方**。"The range of pH values was limited by the experimental behavior of the proteins." 并且 "At extreme pH values (3-4 and 8-9) the measurements become more inaccurate resulting in data with relatively large errors." **他们做了什么**：把测量范围限制在 pH 3–9，并用两句论证把损失正当化——极端 pH 测量误差较大、且这些条件本就不是生物相容配方可及的范围。**仍留下的代价**：pH 窗口窄、端点误差大，R 的有效数据点少（图 3 的抗体突变体只有 4 个点，其 R 是作者由这 4 点估出的，图注里就标了这件事）；对 pI 落在 4.5 或 11 附近的蛋白，最不利 pH 可能正落在误差最大的区间。

4. **蛋白在某个 pH 上若变性，溶解度读数就不可信**。这是他们主动加的一道对照："To ensure that the solubility measurements are not affected by large conformational changes (e.g. unfolding) of the protein under scrutiny at certain pH values, we measured the circular dichroism (CD) spectra of every sample after the incubation time employed in the solubility assay"。**他们做了什么**：每个做过溶解度测定的样品，在 48 h 孵育后再测一次 CD（0.1 mg/ml、200–250 nm），用以排除去折叠造成的假信号。**仍留下的代价**：CD 的判据阈值原文完全没给（多少椭圆率算仍保持折叠、哪些点因此被剔除，都没写），且测的是孵育 48 h 之后的构象，不等于沉淀发生那一刻的构象。

5. **换疏水标度会连带要求把整个打分体系重拟合**。logP 只描述中性态，带电态必须用 logD（"Whereas logP values only consider the neutral state of a species, logD values take the neutral and charged states into account."）。**他们做了什么**：用 Zamora 等的 pH 依赖氨基酸脂溶性标度取 logD，但为了不重拟合 CamSol 已有参数，把它线性归一化回原来 logP 的取值范围——"We normalized and linearly fitted calculated logD values to the range of logP values previously used in CamSol to maintain consistency in the range of hydrophobicity values and to avoid the necessity to refit the scoring parameters of CamSol." **仍留下的代价**：这是一次量纲对齐而非重新标定，logD 与 logP 之间的非线性残差被留在未重拟合的参数里；归一化系数与拟合优度在引文 26 与 SI 中，本卡无法核验（正文未给数值）。

6. **纯序列的 pKa 预测器（IPC 2.0）在纳米抗体上不升反降，作者只承认、不解释**。同一套方案给 BSA/HSA 带来提升（0.75→0.92、0.78→0.88），给纳米抗体 DesAbO 却把相关系数从 0.8 拉到 0.47——"However, the case of the nanobody indicates the limits of the IPC approach, as the coefficient of correlation drops to 0.47 (0.39 without any correction)." **他们做了什么**：没有回头修 IPC，而是把三套方案按蛋白类型分工使用并写进使用建议："Option 2 is the most accurate for structured proteins, whereas option 3 works best for highly dynamic ones."（结构法给球状蛋白、序列法给动态蛋白）。**本文未解决**：全文没有分析为什么同一个 pKa 预测器在纳米抗体这一类小球状蛋白上失效，也没给可操作的诊断指标；用户在拿到结果之前无法知道自己处在哪一侧。

7. **C 端 His-tag 被结构法整段漏掉，他们用了一个手工个案参数补上（本篇最可疑之处）**。"The His-tag was not part of the structure and the p K a values were therefore not adjusted by using PROPKA." 但物理上讲不通——"Nevertheless, it is clear from a physicochemical standpoint that the p K a values must change if so many ionizable residues are near each other." **他们做了什么**：假设这七个组氨酸的 pKa 从 6.5 降到 6 再算（Methods 里写成默认规则："Lastly, the p K a for histidine residues that are part of a terminal His-tag is lowered to 6 from 6.5"），其依据句是 "since the proximity of these histidine residues to each other causes a lowering of their p K a values to avoid electrostatic repulsion"，而这句话挂的参考文献 28 是 Qiagen 的产品手册（The QIA Expressionist, 2003），不是实验测量。**仍留下的代价**：没有一个可推广的规则（tag 长度、位置、邻近电荷都不在参数里），且作者没有报告校正后 DesAbO 的 R 变成多少（正文只说这样能让电荷效应被更准确地估计），于是这次修正的实际收益无法核验——等于用不可核验的手工参数把一个失败案例从结果里抹掉。

8. **模型不能处理辅因子与大修饰，于是这类蛋白被排除在验证集之外**。"A further criterion was that such proteins should not contain large co-factors (e.g. bound heme or large heteroatom groups) or metals, as these components can significantly alter their solubility and are not yet accounted for by the CamSol method." 结论部分承认得更彻底："Moreover, other large modifications such as glycosylation, lipidation or the presence of co-factors are not yet taken into account in our method." **他们做了什么**：只挑能做的项目（"we test our method on proteins that were either commercially available or already produced in our laboratory."），把 heme/金属/糖基化/脂化类靶排除。**本文未解决**：Discussion 里把这条列为局限并给了预期方向（"Nevertheless, we acknowledge that the new version of CamSol is still limited to proteins that do not contain large co-factors such as heme, as we expect that these can alter the pH-dependent solubility significantly and CamSol cannot currently account for these aspects."），但没有任何处理方案或误差估计。后果是验证集天然偏向模型能处理的那类蛋白——幸存者式验证。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及各自在这条管线里干什么）

- **描述符本体（沿用 CamSol 1.0/2.0，本文不动它）**：CamSol 的逐残基分数由四种理化性质组合而成，原文表述为 charge、hydrophobicity、α-helical propensity、β-sheet propensity 四项（底稿里 α/β 是希腊字母，故不作英文引句），性质组合方式作者明确说是唯象的——"CamSol is based on a phenomenological combination of physicochemical properties, and therefore its results are readily interpretable in terms of these properties."，软件血统来自预测淀粉样聚集倾向的 Zyggregator（"which predicts amyloid aggregation propensity of proteins."）。逐残基分数先做邻域平滑（"which is then smoothed to account for the effect of neighboring residues"），再按疏水-亲水排布与 gatekeeper 校正，gatekeeper 的定义原句为 "gatekeepers are charged residues flanking hydrophobic regions and modulate their effects on solubility"，最后合成总溶解度分（"an overall solubility score is calculated which was updated in version 2 of CamSol"）。**注意：局部疏水/电荷倾向、螺旋与折叠倾向这四个描述符本身不是本文新增，本文新增的是让它们随 pH 变。**
- **pH 引入方式一（电荷）**：Henderson-Hasselbalch 方程算质子化/去质子化比例，把整数电荷换成部分电荷——"CamSol assesses partial charges using the Henderson-Hasselbalch equation."；动机是 pH 主要改变可电离残基的质子化态与静电荷（"Changes in pH mainly affect ionisable residues, as the pH determines the protonation state and therefore the electrostatic charges of these residues."），而这套计算的命门是 pKa 本身（"An important component of these calculations is an accurate p K a value, which determines the pH range where the residue is charged."）。
- **pH 引入方式二（疏水）**：logP 换成 pH 依赖 logD（Zamora 等的连续溶剂化标度），再线性归一化回旧 logP 范围以免重拟合参数；底稿里 logD 的定义被抽取打断了，只剩这句带 where 的文字描述："LogD combines the partition coefficient logP of neutral and ionized species where"，其后至 "is the difference between p K a and pH"（δ 的定义式，公式体在纯文本里断裂，本卡不复算）。
- **pKa 三套来源（本文的核心工程决策）**：Option 1 更新表值（"In the first method, we revisited the tabulated p K a values used in the original version of CamSol and updated them with more accurate values"，取自 PKAD 数据库，"we retrieved p K a values from the computational biophysics and bioinformatics database"，该库规模是 "which contains over 1500 experimentally measured residue p K a values from a wide range of proteins"，取法是 "We then employed the median p K a value observed in this database for each of the 20 amino acid types."）；Option 2 PROPKA（需结构，"which requires the knowledge of the structure of the input protein or of an accurate structural model."，机制为 "PROPKA uses a combination of thermodynamic calculations and empirical shifts."）；Option 3 IPC 2.0（纯序列，"This method uses a mixture of support vector regression and deep learning models trained on the PKAD database"，"IPC is especially useful for peptides and proteins that are intrinsically disordered or highly dynamic."，且 "Using p K a values updated in this way helps refine the solubility predictions and improves accuracy while keeping the method completely sequence-based."）。三选一由用户按可得信息决定："The user may choose which approach to use, depending on the information available on the protein under scrutiny."
- **组氨酸与质子化模型的三处特判**：（a）旧版一条 pH 规则覆盖所有 His（pH 6.5 以下整残基 +1）；（b）新版 His-tag 的 His 一律把 pKa 设为 6；（c）半胱氨酸默认改判为成对（二硫/盐桥态、不可带电）——"In the original CamSol method cysteine residues were assumed to be reduced. We changed the default to assume that all cysteine residues are in salt bridges and therefore cannot be charged."，自由 Cys 要用户手工把字母 C 改成 B——"Free cysteine residues can be assigned by replacing the letter 'C' with the letter 'B' in the input sequence."
- **实验侧（本文新增的验证数据来源）**：PEG 6000 梯度沉淀（相对溶解度）、圆二色谱（构象核查）、SEC 与脱盐柱（纯化与换液）、酶标仪吸光读数。缓冲为 10 mM 磷酸氢二钠七水合物 + 10 mM 柠檬酸一水合物（"Ten-millimolar sodium phosphate dibasic heptahydrate (MP Biomedicals, 191 441) and 10-mM citric acid monohydrate (Fisher Scientific, 5949-29-1) were combined."），每个实验用 NaOH/HCl 调 pH（"For each experiment the pH was adjusted using NaOH or HCl."）。
- **没有用的方法**：分子动力学（引言只把 SAP 这类基于 MD 的疏水暴露方法列为前人工作）、量子化学（logD 与 PROPKA 都是查表/经验连续介质）、机器学习训练 CamSol 本身（IPC 2.0 是外部现成预测器）。本文不训练溶解度模型，只把既有唯象打分器接上 pH。

### 主工作流（本文自己就是这条流程；阈值一律用原文数字，无阈值处明写）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| 1 | 氨基酸序列 + 目标 pH（可选：3D 结构） | 定性质参数：电荷按 Henderson-Hasselbalch 取部分电荷；疏水项按 pH 依赖 logD | 旧版规则：pH 低于 6.5 时所有 His 记 +1（本文废弃）；新版在 pH 接近残基 pKa 时允许小数电荷 | 每个可电离残基一个偏电荷 + 端基电荷（N 端酰胺、C 端羧酸新增） |
| 2 | 同一序列 | 选 pKa 来源：Option 1 表值 / Option 2 PROPKA（需结构）/ Option 3 IPC 2.0（纯序列） | 选择规则（作者口径）：有稳定折叠结构用 Option 2，动态或无序体系用 Option 3，只追速度用 Option 1；表值取自 PKAD，20 种氨基酸各取其实验值中位数，库内含超过 1500 个实验 pKa | 一套逐残基 pKa；三种方案在 BSA 上的逐残基差异只列在 SI 表 S2（正文未给数值） |
| 3 | 含 C 端 His-tag 的构建体（如 DesAbO） | 把 tag 内 7 个 His 的 pKa 从 6.5 手工下调到 6 | 阈值：pKa 6（原 6.5）；理由为邻近 His 静电排斥，依据挂 Qiagen 产品手册（参考文献 28） | 一处逐构建体手工参数；未报告校正前后的 R 变化 |
| 4 | 序列中的 Cys | 默认按成对（不可带电）处理；需自由 Cys 时把字母 C 改写为 B | 无阈值（默认值改变，CamSol 1.0 原默认为全还原态） | 输入序列需人工标注；未标注即假定全部成对 |
| 5 | 逐残基性质参数 | 按 CamSol 原框架合成逐残基分数：四种理化性质组合 → 邻域平滑 → 疏水-亲水排布校正 → gatekeeper 校正 → 总溶解度分 | 打分参数沿用 CamSol 2.0，未重新拟合（这正是 §2 第 5 条把 logD 归一化回 logP 范围的原因） | 逐残基溶解度 profile + 一个总分数（无量纲评分，非 mg/ml） |
| 6 | 蛋白样品（商用或本组表达纯化；IgG4 由 Novo Nordisk 提供） | SEC 进一步纯化 + 每次测定前脱盐换液到目标缓冲 | 排除标准：不含大辅因子（如血红素、大杂原子基团）与金属；无结构/构象合格阈值 | 7 种蛋白进入实验（BSA、HSA、鸡卵溶菌酶、纳米抗体 DesAbO、α-synuclein、胰岛素、全长 IgG4）再加 1 个 IgG4 突变体 |
| 7 | 每个蛋白 × 每个 pH | PEG 沉淀测相对溶解度：PEG 6000 滴定到终浓度 0–33%，终蛋白 1 mg/ml，同一缓冲同一 pH 起始，加 PEG 后需重新调 pH，48 h 孵育后离心、转移上清、酶标仪读数（220–700 nm，25 °C） | 读出判据：沉淀曲线呈 sigmoid，取曲线拐点作为溶解度代理 | 每条曲线一组拐点；pH 3–9 全曲线，逐点数值只在全表 SI 表 S4（正文未列全） |
| 8 | 溶解度测定后的同批样品 | 测 CD 谱核查构象，排除去折叠污染溶解度读数 | 原文未给阈值（无椭圆率判据、无剔除规则） | 每种蛋白每个 pH 一条 CD 谱（图 S2，本仓库存无） |
| 9 | 预测分数 vs 实测拐点 | 按蛋白分别算 Pearson 相关系数 R，三种 pKa 方案各算一遍，另加完全不校正 pKa 的对照 | 达标口径：作者报告所有测试蛋白的 R 均大于 0.67；无统计检验、无留出集 | 图 2 A–F（6 个蛋白）与图 3 A–B（IgG4 及变体）；数值全表在 SI 表 S3/S4 |
| 10 | 验证集设计（对应训练/标定问题） | 刻意铺开 pI 与体系类型，覆盖理论 pI 4.5–11；无序蛋白与多肽只走 IPC，球状蛋白走 PROPKA | 覆盖判据：pI 跨度 4.5–11（作者理由：pI 通常指示溶解度最低点所在的 pH） | 8 条曲线（7 蛋白 + 1 突变体）；IgG4 突变体仅 4 个数据点，其 R 由 4 点估出 |
| 11 | 大规模候选库（建议用法，非本文实测） | 两级漏斗：先用 Option 1（表值 pKa，计算极快）做超大规模 pH 依赖初筛，再对排名靠前者用 PROPKA 或 IPC 精算 | 原文未给数值切点，只给排序语义（top-ranking）；成本口径只有 极快、极少计算资源 的定性描述 | 论文本身没有跑任何设计库；未记录 候选数与漏斗递减 |

**这条流程的骨架，对我们最有价值的是第 11 步那两级漏斗**：把一个几乎零成本但误差较大的序列版（表值 pKa）放在前面吞掉全量，再让需要结构、误差较小的版本只服务排名靠前的一小撮——"Option 1 is provided as its calculations are extremely fast, and it can therefore be employed for very large-scale screenings of pH-dependence using little computational resources." 与 "The pH-dependence of the solubility of the top-ranking proteins from such screenings can then be calculated more accurately by employing either PROPKA or IPC calculated residue p K a values." 两句合起来就是它的全部工程口径，代价是没有给任何量化切点。

## 4. 关键数字台账（全部来自本地全文，§9 逐条命中）

| 数值 | 含义 | 出处（原句片段 / 位置） |
|---|---|---|
| 3.0 | 本版 CamSol 版本号，公开网页版 | "We make this method publicly available at https://www-cohsoftware.ch.cam.ac.uk/index.php/camsolph , as the version 3.0 of CamSol." |
| 4 种性质 | 逐残基打分的描述符：电荷、疏水性、α-螺旋倾向、β-折叠倾向（α/β 为希腊字母，不作英文引句） | Methods 理论部分："CamSol is based on a phenomenological combination of physicochemical properties" |
| >1500 / 20 | PKAD 库内实验测得残基 pKa 条数 / 取其实验中位数的氨基酸种类数 | "which contains over 1500 experimentally measured residue p K a values from a wide range of proteins" 与 "We then employed the median p K a value observed in this database for each of the 20 amino acid types." |
| 6.5 → 6 | C 端 His-tag 内组氨酸 pKa 的手工下调值（本文新增默认规则） | "Lastly, the p K a for histidine residues that are part of a terminal His-tag is lowered to 6 from 6.5" |
| 7 个 His | DesAbO 的 C 端纯化标签长度，即被整体按 pKa 6 处理的残基数 | "When we analyzed DesAbO, we realized that the charge effect of the C-terminal His-tag (i.e. the sequence of seven histidine residues used for purification) could be estimated more accurately." |
| pH 低于 6.5 记 +1 | 旧版对全部组氨酸的粗规则（本文废弃的对象） | "For example, all histidine residues would acquire a charge of +1 for an input pH below 6.5." |
| pH 3–9 | 实测与预测所用的 pH 窗口 | "at pH values ranging from 3 to 9"；窗口上限由蛋白本身实验行为决定："The range of pH values was limited by the experimental behavior of the proteins." |
| 3–4 与 8–9 | 作者自认测量误差显著变大的两个极端区间 | "At extreme pH values (3-4 and 8-9) the measurements become more inaccurate resulting in data with relatively large errors." |
| pI 4.5–11 | 验证集刻意覆盖的理论等电点跨度 | "With the proteins tested experimentally, we aimed at covering a broad range (4.5-11) of theoretical pI values" |
| R 全部 > 0.67 | 作者给出的总体验证结论（达标口径，非统计检验阈值） | "Our results show that CamSol not only captures the overall trend in solubility upon pH changes well, but the predicted values are also highly correlated with the experimental values with Pearson's coefficients of correlation always greater than 0.67" |
| BSA 0.75 / 0.92 / 0.63 | BSA 在 PROPKA / IPC / 完全不校正 三种 pKa 方案下的 Pearson R | "BSA and HSA ( Figure 2B and D ) showed a good agreement between experimental values and predicted results with a Pearson's coefficient of correlation of 0.75 and 0.78, respectively" 与 "These correlations improved to 0.92 and 0.88 with the use of IPC, and are still relatively good even if the p K a values are not corrected (0.63 and 0.78)." |
| HSA 0.78 / 0.88 / 0.78 | 同上，人血清白蛋白 | 同上一行的两句（0.78 属 HSA，IPC 后 0.88，无校正仍 0.78） |
| DesAbO 0.8 / 0.47 / 0.39 | 纳米抗体在 PROPKA / IPC / 无校正 下的 R——本文唯一一处方法互换后明显变差 | "The nanobody DesAbO shows an even better agreement with a coefficient of correlation of 0.8" 与 "However, the case of the nanobody indicates the limits of the IPC approach, as the coefficient of correlation drops to 0.47 (0.39 without any correction)." |
| 溶菌酶 0.9 | 本文球状蛋白里 PROPKA 方案最好的常规蛋白 | "Lysozyme shows almost a perfect correlation, with a correlation coefficient of 0.9" |
| α-synuclein 0.71（无校正 0.72）/ insulin 0.67（无校正 −0.67） | 两个只走 IPC 的体系（内在无序蛋白与多肽）；胰岛素在无校正时相关系数变号 | "only the IPC method was applied since intrinsically disordered Proteins (IDPs) and peptides do not form stable structures that can be used for PROPKA." 与 "The correlations are slightly lower, with a coefficient of correlation of 0.71 and 0.67, respectively (0.72 and -0.67 without any correction)." |
| mAbIgG4 0.96 / 0.88 / 0.85 | 全长 IgG4 在三种方案下的 R（本文最好的一组） | "We then tested the method on a IgG4 antibody (mAbIgG4). The coefficient of correlation is 0.96 with PROPKA p K a values" 之后接 "0.88 with IPC ( Figure S5" 与 "and 0.85 with no correction ( Figure S6" |
| 变体 0.97 / 0.86 / 0.82 | 两个降 pI 突变（重链 S70E、轻链 V99D）构成的 IgG4 变体的三种方案 R | "CamSol can predict well the solubility of this variant with a coefficient of correlation of 0.97" 与 "(B) Same plot for a mutational variant of mAbIgG4 harboring two mutations that lower the pI (S70E V99D on heavy and light chain respectively)"；0.86 与 0.82 见 "0.86 and 0.82, respectively for IPC and no p K a correction" |
| 仅 4 个点 | 上述 0.97 的 R 是由 4 个实验点估出的（图注里作者自己标注） | 图 3 图注说明该 R 由仅有的四个可用点估计（原句含 markdown 星号标记 R 的上标，故不作英文引句） |
| PEG 0–33% / 1 mg/ml / 48 h | PEG 6000  crowding 梯度、终蛋白浓度、孵育时间 | "PEG 6000 is used as a crowding agent and titrated to final PEG concentrations of 0-33% and final protein concentration of 1 mg/ml" 与 "After a 48-h incubation period, plates are centrifuged, the supernatant is transferred into a fresh plate and the soluble fraction is measured using a plate reader." |
| sigmoid 拐点 | 溶解度代理量的定义（不是绝对浓度） | "A sigmoidal behavior is seen for the precipitation of proteins, and the inflection point of the curve is used as a solubility proxy." |
| 10 mM / 10 mM | 缓冲体系：磷酸氢二钠七水合物 + 柠檬酸一水合物，pH 用 NaOH/HCl 调 | "Ten-millimolar sodium phosphate dibasic heptahydrate (MP Biomedicals, 191 441) and 10-mM citric acid monohydrate (Fisher Scientific, 5949-29-1) were combined." |
| 0.1 mg/ml、200–250 nm、带宽 1 nm、步长 0.5 nm、1 s/point、光程 1 mm | CD 构象核查的采集参数 | "Three spectra were obtained using an Applied Photophysics Chirascan and a High Precision Cell made of quartz (Hellma Analytics, path length 1 mm) between 200 and 250 nm with a bandwidth of 1 nm, step size of 0.5 nm and scanning speed of 1 s/point." 与 "Proteins were diluted to a concentration of 0.1 mg/ml." |
| 220–700 nm、25 °C | 酶标仪吸光读数窗口与温度 | "Absorbance was measured with a plate reader (BMG Clariostar)"（后半句含摄氏度符号，故用中文叙述） |
| 7 蛋白 + 1 变体 | 验证集规模：BSA、HSA、鸡卵溶菌酶、DesAbO、α-synuclein、胰岛素、全长 IgG4（HzATNP，Novo Nordisk 供）及其突变体 | "BSA (Sigma, A9418), HSA (Sigma, A3782) and chicken egg white lysozyme (Sigma, L6876) were resuspended in buffer and then further purified and buffer-exchanged by carrying out size exclusion chromatography" 与 "mAbIgG4 and its variant were provided by Novo Nordisk." 与 "as well as that of the full-length IgG4 monoclonal antibody HzATNP and one of its mutational variants" |
| 每次测定前换液 | 样品新鲜度控制 | "Each protein was freshly buffer-exchanged into the correct buffer (Cytiva, HiTrap Desalting column) before each assay." |
| 三套 pKa + 一套不校正 | 验证矩阵：每个蛋白都跑了表值/PROPKA/IPC/无校正的组合（图 2 与 SI 图 S3–S6） | "In this work, we employed three alternative strategies to obtain accurate p K a values." 与 "The results with IPC and without any p K a corrections are shown in Figures S3 and S4" |
| 逐点数据在表 S4 | 正文未列全实测溶解度数值，完整表在补充材料（本仓库存无） | "Figures and Tables as referenced in the text including Table S4"，其后半句为 "which contains the complete list of measured solubility for all proteins tested" |
| 33 条参考文献 | 本文体量（方法短文：无大型数据集、无基准集、无设计库） | 参考文献列表编号至 33（第 33 条即本组 2021 年的开源 PEG 沉淀法协议）；鸣谢含 Novo Nordisk 供样、AstraZeneca 资助博士生（"M.O. is a PhD student funded by AstraZeneca."）、Royal Society 大学研究研究员与 Wellcome Trust 项目资助 |

## 5. 结论——作者说了什么

1. CamSol 3.0 是纯序列输入（有结构时可加结构信息），能把 pH 效应带进溶解度预测："The method is incorporated in the CamSol software and, if the structure is not known, works only using the sequence."
2. 预测精度达到与实验方法相当的水准（作者原话，见 §1 所引摘要句），且趋势与数值同时吻合："Our results show that CamSol not only captures the overall trend in solubility upon pH changes well, but the predicted values are also highly correlated with the experimental values with Pearson's coefficients of correlation always greater than 0.67"
3. 方法适用范围跨尺度铺开：纳米抗体、全长抗体、内在无序蛋白、多肽都能算——"By employing CamSol 3.0, we show that we can accurately predict the solubility behavior at different pH values of proteins with varying sizes, including nanobodies, full-length antibodies and intrinsically disordered proteins."
4. 微小突变造成的 pH 依赖位移也抓得住："We have shown that CamSol 3.0 can reliably predict the solubility of globular proteins with a wide range of pI values"（跨度 4.5–11），且 "CamSol 3.0 is also capable of capturing the changes induced by small mutations that shift the overall pI value of the protein."
5. 三套 pKa 方案给出分工口径："Option 2 is the most accurate for structured proteins, whereas option 3 works best for highly dynamic ones." 并把 Option 1 定位为超大规模廉价初筛、精算留给 top-ranking（两句见 §3 末）。
6. 概念层结论：溶解度最低点不等于 pI。作者承认 pI 是常用近似但不够——"The pI value is usually used as an approximation of the pH value at which a protein is least soluble as this is the point at which the overall charge on a protein is neutral." 与 "Although in many cases this assumption is rather accurate, in general the solubility of folded proteins does not only depend on the overall charge." 理由是电荷分布与疏水变化并不同步："The distribution of these charges is crucial, as patches of opposing charges can act as starting points for aggregation due to strong attractive intermolecular forces." 与 "Although the changes in hydrophobicity are related to the changes in charge upon pH variations, these are not perfectly correlated and hence can move the point of least solubility away from the pI value as well."
7. 定位与自我限制：这是相对比较工具，不是绝对溶解度预测器——"In its current implementation, CamSol is aimed at performing relative comparisons of the solubility of a protein at varying conditions (including pH) or of similar proteins such as mutational variants." 辅因子/糖基化/脂化仍处理不了（§2 第 8 条两句）。总结句："with version 3.0 of CamSol we have presented a sequence-based method that can accurately predict the solubility of proteins at varying pH values."
8. 面向未来的自我期许（本文唯一一处提到从头设计）："In addition to aid the development of protein biologics, we expect our method to be useful in protein engineering and de novo protein design, adding to the increasingly powerful arsenal of computational methods emerging in these fields."

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这是一篇 把已有唯象打分器接上物理量 的增量文，不是新模型**。四个描述符一个都没新增，新增的只是让电荷与疏水随 pH 走（偏电荷 + logD + 三套 pKa）。→ 对我们：这类改造的成本极低（无训练、无重拟合，作者刻意用线性归一化躲开重拟合），是廉价判据档位里性价比最高的改法；我们若给现有序列描述符加 pH/质子化维度，可以照抄这条不改。
2. **它最强的迁移价值是两级漏斗的口径，而不是任何数字**。Option 1（表值 pKa，几乎零成本）扫全量 → top-ranking 才上 PROPKA/IPC。→ 对应我们漏斗的 便宜序列判据先削量、贵判据只做头部 这一档，且原文连切点都没给，说明这类漏斗的切点本来就是按预算定的，不是按物理定的。
3. **R>0.67 不是判据阈值，而是事后描述**。它是 预测曲线与实测曲线在同一个蛋白的不同 pH 点上算相关，分母是每条曲线上的少数 pH 点（图 3 的变体只有 4 个点），是同一蛋白内的重复测量，不是跨蛋白的判别能力，更没有阴性样本池。把它当闸口用会犯两个错：把曲线拟合当成分类能力、把同一蛋白的自相关当成外部效度。
4. **作者的验证设计里有一处自我选择**：能排除的蛋白（含辅因子、金属、大修饰）都排除了，而这三类恰是 UAA 酶最可能的形态（辅基/金属簇/修饰）。所以本文对 我们的靶会不会溶 的证据力，天然低于它对自己验证集的证据力。
5. **His-tag 那一处（§2 第 7 条）是全篇工程味道最浓的地方**：结构法漏了 tag → 手工改一个 pKa → 不报校正后 R。这不是造假，但它示范了一种我们必须警惕的模式：**用不可核验的手工参数把模型的已知失败点遮盖掉**。我们自己的判定器若允许 手工调整某轴权重后不再报原始数字，会退化成同一种东西。
6. **同一套 IPC 在 BSA 上升、在纳米抗体上降**（0.75→0.92 vs 0.8→0.47），说明这类经验/半经验标度的收益与蛋白类别强相关且不可预测。→ 对我们：任何 加一条修正就普遍变好 的假设都要在分层小集上分别验证，且允许写出 在某类上变差 的结论。

## 7. 局限与失败（作者的 + 我们读出的 + 与记录文件不符处）

**作者自认（见 §5.7 与 §2）**
- 不能处理大辅因子、金属、糖基化、脂化（原话两句在 §2 第 8 条）。
- 只做相对比较，不给绝对溶解度。
- 极端 pH 端点误差大；验证集 7+1 个蛋白，样本量小。
- IPC 在纳米抗体上失效，只承认 limits、未解释（§2 第 6 条）。
- 本文没有做任何 de novo 设计上的前瞻对照：工具面向设计是 Discussion 里的一句期许（§5.8），不是结果。

**我们读出的**
- 无训练/留出切分这回事：CamSol 是唯象打分器，本文的 验证 是 外部对照实验 而非 交叉验证，因此不存在 泛化到未见序列 的任何定量保证；换成我们的话，就是 没有考卷，只有 8 条曲线的目测一致性。
- 相关系数是同一蛋白跨 pH 的曲线吻合度，与 能否把一个不溶的候选提前丢掉 不是一回事；全文没有 ROC、AUC、富集率之类的判别指标，也没有把 7 个蛋白当 70 个候选来排序。
- R 的分母极小（每蛋白几个 pH 点，最少的一处只有 4 个点），未报告不确定度、未做统计检验、未给置信区间；0.97 与 0.96 之间相差 0.01 在原文口径下不可解释。
- 归一化 logD 回 logP 范围这一步（§2 第 5 条）把一次模型改动伪装成 不改变参数量 的零成本升级，代价（残差被吸收进未重拟合的参数）在正文里没有量化。
- CD 只用于 确保 而没有判据数字，因此无法复核哪些数据点构象上是干净的（§2 第 4 条）。

**与项目记录文件不符 / 需要以全文为准之处**
- `sources/cost-benchmarks.md` §六 把 10.1093/bib/bbad004 挂在 包涵体/不溶 这一行的判据列，CSV 的 设计对象 亦写为 包涵体/不溶这一失败模式的候选判据。**以全文为准的修正**：CamSol 3.0 验证的是配方条件下的相对溶解度（PEG 沉淀代理量，pH 3–9，纯化蛋白），不是大肠杆菌表达位点上的可溶表达量；引言里明写 PON-sol、SOLpro、PROSO II 才是预测可溶表达产量的方法——"PON-sol [ 12 ], SOLpro [ 13 ] and PROSO II [ 14 ] use machine learning techniques to predict solubility in terms of soluble expression yield."，而 CamSol 走的是聚集倾向区段那条路线——"Other methods derive the solubility from aggregation-prone regions"。因此把它写成 包涵体判据 属于口径混用：它能做 表达后是否易聚沉 的序列级旁证，不能顶替 表达可溶性 判据。
- CSV 行 证据级别 列仍为 摘要级（旧值），该列不在 14 键回填范围内，未擅自改表；本卡按全文级写。
- CSV 行 阈值数字 为 未记录，与全文一致（本文确实没有可移植的筛选阈值）；CSV 行 成本/统计量引用 写 工具在天然蛋白上验证过；本次未检索到它们用于从头设计命中率提升的前瞻对照 —— 与全文核验一致，本卡不改。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **设计期用序列级溶解度/聚集倾向做廉价预筛**：CamSol 型打分只吃序列、单次计算近零成本，输出逐残基 profile。我们可以在 RFdiffusion/Placer 出骨架、MPNN 出序列之后，立刻跑一个序列级溶解度打分（CamSol/Aggrescan 型），把 局部疏水斑块 + 无 gatekeeper 保护 的候选先削掉，位置放在 结构自洽闸口之后、表达实验之前——它替代不了结构闸口，但能在同一个成本档上多加一条独立证据。
2. **pH 依赖这条轴是我们完全没有的**：我们的判定器目前是 pH 单点（反应缓冲固定），CamSol 的做法提示：对同一批候选，把 pH 当成第二个自变量扫一遍（表值 pKa 版几乎免费），可以把 只在一个 pH 上看着可溶 的候选区分成 全 pH 段稳 与 靠某个 pH 撑着 两类。对我们真正有用的是后者：UAA 反应的 pH 与辅因子（ATP/Mg2+）条件本身要调，这条轴能给 配方侧 而不是 命中侧 提供信息。
3. **两级漏斗的组织方式（Option 1 全量 → top-ranking 精算）**：这是本篇最该照抄的工程结构，与我们已有的 便宜判据削量、贵判据做头部 预算口径一致；而且它示范了如何诚实地写 切点没给，只有排序语义。
4. **gatekeeper 概念可以直接进我们的序列描述符**：带电残基夹住疏水区段这一条是序列 motif 级规则（不需结构、不需能量），比 平均疏水性 更可操作，且能给出 改哪一位能救可溶性 的具体建议（作者原话支持这种用法："Therefore, this analysis can aid the engineering of mutations to alter the pH-dependence of the solubility." 与 "Looking at these solubility profiles helps pinpoint specific sequence regions whose contribution to solubility is most affected by changes in pH."）。
5. **加一条构象对照再解读溶解度**：本文用 CD 排除去折叠假信号，提醒我们——任何 可溶 读数若不配一条 折叠状态 对照，就无法区分 不溶 与 变性聚集。我们目前只有 SEC/SDS-PAGE，量级更粗。

**不可迁移（为什么不能照搬）**

1. **不许把它的 R（0.67–0.97）当 UAA 酶活判据、命中率或成功概率**。R 是同一蛋白跨 pH 的曲线吻合度，每个体系只有几个 pH 点（最少 4 点），无阴性池、无 ROC/AUC、无统计检验；它衡量的是 预测器与实验的一致性，不是 该预测器能否提前挑出会表达的酶。本文全程没有 de novo 设计实验，更没有 UAA 合成酶。DP2R 口径下，任何 binder/可开发性工具的曲线吻合度都不能填进我们的成功概率字段。
2. **不许把 包涵体/不溶 当成 CamSol 能判的失败模式**（见 §7 最后一条口径修正）：它测的是纯化蛋白在配方缓冲里的相对溶解度，而我们的失败发生在异源表达、含辅因子/金属簇的酶上；CamSol 明写不能处理辅因子与大修饰，而这恰是 UAA 合成酶的常态形态。
3. **pKa=6 这类手工个案修正不许搬进我们的判定器**：无推广规则、无校正后收益数字、依据是厂商手册。我们的规则是：任何手工参数必须同时留下 校正前后的原始分数 与 依据出处，缺一不许进漏斗。
4. **它的 溶解度 与 稳定性/催化 三者互不替代**：本文连热稳定都没测（只有 CD 作构象排除），更没有任何活性数据；引用它只能引用 序列级溶解度预筛可行 这一条方法结构，不能引用任何 性能数字 去支撑 这样做能提高酶命中 的说法。
5. **成本侧不许反向引用**：本文没给 CPU 时间、单价、通量数字，只有 extremely fast 的定性说法；所以它不能作为 我们跑 CamSol 便宜 X 倍 的成本依据，只能作为 这一级判据值得跑 的定性依据（真实单价要我们自己测）。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K47_PMC10025429_text.txt

- 本地纯文本：`fulltext/K47_PMC10025429_text.txt`（Europe PMC 通道 XML 去标签 + HTML 实体解码 + 引号/破折号统一 + 空白折叠，未改写内容；原始 XML 同目录 `K47_PMC10025429_fullTextXML.xml`）。
- 同一篇论文只登记了这一份抽取版，故不存在跨抽取通路句子断裂的差异风险；底稿开头题录（标题 / DOI / PMC / PMID）与本行一致，核验过程记在 §0。
- 对照记录文件：`sources/cost-benchmarks.md` 第 198 行（§六 失败模式→计算判据 映射表，本行是该表的 包涵体/不溶 行判据来源之一）；CSV 行的 原文出处指针 亦指向此处。
- 底稿已知缺陷（影响本卡两处）：公式体被打断（logD 与 δ 的定义式只剩文字连接，见 §3）；上标/希腊字母以 `p K a`、α、⍺（U+237A）形态出现，含这些字符的句子一律改为中文叙述承载数字，不作英文引句。
- CSV 字段映射：本卡 §3 ↔ 计算筛选判据/阈值数字；§4 ↔ 候选数递减/成本统计引用；§7 最后一段 ↔ 设计对象 与 在方法演进链的位置；§8 ↔ 在方法演进链的位置。
- **本卡自检**：`scripts/verify_literature_cards.py --only K47 --no-report`（参数 `--only K47 --no-report`；输入：本卡 + `fulltext/K47_PMC10025429_text.txt`）把卡内所有被直双引号包住、不含中日韩字符、≥20 字符且 ≥12 个字母的片段，在登记的底稿里逐字查找，任何一条不命中即 FAIL、退出码 1。写卡过程中先用同一个 `litcards_text.norm` 函数对 196 条候选原句做过预检，其中 4 条凭记忆重写的版本未命中（当场弃用，改回底稿原句），入卡的 113 条引句实例（去重后 99 条）全部逐字命中，卡内引句无一处含非 ASCII 字符、无一处含 markdown 星号。本轮实跑结果：**PASS K47 quotes=113/113，退出码 0**。按并行写卡约定只用了 `--no-report`，因此本目录的 `selfcheck.txt` 与 `rollout_status.tsv` 不由本代理改写（他人产物保持原样）；未跑 `--sync-map`，未改 CSV、`sources/*.md`、样板卡 B09、`scripts/`、`fulltext/` 与 `_quarantine/`。

<!--CSV回填
work_type=论文（方法学：序列级 pH 依赖溶解度预测工具 CamSol 3.0 + 湿实验对照验证）
target=无设计对象。验证集为 7 个天然/商用蛋白加 1 个 IgG4 突变体（BSA、HSA、鸡卵溶菌酶、纳米抗体 DesAbO、α-synuclein、胰岛素、全长 IgG4 HzATNP 及其 S70E/V99D 变体），pH 3 至 9
backbone_generation=不生成骨架或序列。输入为氨基酸序列（可选 3D 结构），自由半胱氨酸须把字母 C 手工改为 B；C 端 His-tag 的 His 默认 pKa 由 6.5 设为 6
computational_filters=CamSol 逐残基唯象打分（电荷、疏水性、α-螺旋倾向、β-折叠倾向四性质组合）+ 邻域平滑 + 疏水-亲水排布校正 + gatekeeper 校正 + 总溶解度分；本版新增：Henderson-Hasselbalch 部分电荷、pH 依赖 logD 线性归一化回 logP 范围、残基 pKa 三选一（PKAD 中位数表值 / PROPKA 结构法 / IPC 2.0 序列法）、N 端与 C 端端基电荷
thresholds=无筛选阈值可移植（阈值数字 列可留 未记录）。原文出现的数值口径：验证结论为所有测试蛋白 Pearson R 大于 0.67（最高 0.96 与 0.97，纳米抗体用 IPC 时降到 0.47）；His-tag pKa 6.5 降到 6；旧版 His 在 pH 低于 6.5 时记 +1；实验侧 pH 3 至 9、PEG6000 终浓度 0 至 33%、终蛋白 1 mg/ml、孵育 48 h、验证集理论 pI 覆盖 4.5 至 11
md_used=否（引言仅把 SAP 这类基于 MD 的疏水暴露-聚集倾向方法列为前人工作，本文计算全程不含 MD）
qm_used=否（PROPKA 为热力学项加经验位移的经验连续介质法；logD 取自 Zamora 等已发表的连续溶剂化计算氨基酸标度，本文只查表，未做量子化学计算）
experimental_methods=PEG6000 梯度沉淀法测相对溶解度（sigmoid 拐点为代理量）+ 酶标仪吸光读数（220 至 700 nm、25 摄氏度）+ 圆二色谱构象核查（0.1 mg/ml、200 至 250 nm）+ SEC 与脱盐柱纯化换液；10 mM 磷酸氢二钠与 10 mM 柠檬酸缓冲，NaOH/HCl 调 pH
pipeline_counts=无候选漏斗。计算侧：每条序列 × 每个 pH × 三套 pKa 方案（另加完全不校正对照）；实验侧 7 蛋白加 1 变体、pH 3 至 9、IgG4 变体仅 4 个数据点；逐点实测值在 SI 表 S4（本仓库存无）
hit_rate=不适用，本文未给任何命中率口径（无设计库、无候选到命中的递减、无前瞻对照）；验证口径只有跨 pH 的 Pearson 相关系数
best_metric=最高 Pearson R 等于 0.97（IgG4 S70E/V99D 变体，PROPKA pKa，由仅 4 个点估得）与 0.96（亲本 IgG4）；无 Kd、无酶活、无绝对溶解度浓度
cost_or_stat_note=成本口径只有定性表述：表值 pKa 版计算极快、可用极少计算资源做超大规模 pH 依赖初筛，排名靠前者再用 PROPKA 或 IPC 精算；未给 CPU 时间、单价或通量数字。实验侧口径：溶解度实验耗材耗时、不便高通量，故用低样品消耗的 PEG 法。本文未检索到用于从头设计命中率提升的前瞻对照
role_in_timeline=CSV 该行是 失败模式到计算判据 映射表中 包涵体/不溶 行的判据来源之一；提供两件事：序列级 pH 依赖溶解度打分可作设计期廉价预筛（与 Aggrescan 型聚集倾向路线同源），以及 廉价表值版全量初筛加 结构或序列精算版只做头部 的两级漏斗范式。它不是 de novo 设计命中率证据；同段引言把可溶表达产量判据归给 PON-sol/SOLpro/PROSO II，CamSol 属于聚集倾向区段那条路线，口径不可与包涵体判据混用
source_pointer=data/literature_cards/fulltext/K47_PMC10025429_text.txt（同一篇另有 fullTextXML 原始件）；sources/cost-benchmarks.md 第 198 行；工具页 https://www-cohsoftware.ch.cam.ac.uk/index.php/camsolph
CSV回填-->
