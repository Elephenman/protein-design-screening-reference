# [K56] 非键力场参数是怎么被拟合出来的——RESP2：把电荷极化做成可调参数 δ，并与 Lennard-Jones 一起重拟合

Schauperl M, Nerenberg PS, Jang H, Wang LP, Bayly CI, Mobley DL, Gilson MK（UCSD Skaggs 药学院 / CSULA / UC Davis / OpenEye / UC Irvine）
Communications Chemistry 2020, 3:44 · DOI 10.1038/s42004-020-0291-4 · PMID 34136662 · PMCID PMC8204736 · NIHMS1590865
开放获取（CC BY 4.0）· https://doi.org/10.1038/s42004-020-0291-4

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K56**（组：通用方法学）。**本行是一组五篇**（CSV 作者字段自写"五篇"）：RESP2（Commun Chem 2020, 10.1038/s42004-020-0291-4）、W-RESP（JCTC 2021, 10.1021/acs.jctc.0c00976）、AM1-BCC II（J Comput Chem 2002, 10.1002/jcc.10128）、constant-pH MD 力场基准（JCTC 2026, 10.1021/acs.jctc.6c00678）、晶体质子化态（JPCB 2024, 10.1021/acs.jpcb.4c05947†）。**本卡只覆盖有本地全文的第一篇（RESP2）**，其余四篇本地无全文，卡内不引它们的任何数字或结论 |
| 本文取回方式 | Europe PMC 按 DOI 检索 → fullTextXML（`data/literature_cards/inventory.json` 记 fetch_channel=epmc_search_then_fulltext），2026-10-20 本地抓取 |
| 本地全文 | `data/literature_cards/fulltext/K56_PMC8204736_text.txt`（75,725 B，SHA-256 `a4155d1f3ea55855…`；XML 原件 `K56_PMC8204736_fullTextXML.xml` 193,836 B）。**全文是单行文本**（无换行符），且正文公式的 LaTeX 残留块未被剥离，所以本卡所有引句都取自不含公式块的句子 |
| 底稿身份复核 | 按项目规则核对文件头部身份块：Communications Chemistry / 10.1038/s42004-020-0291-4 / PMC8204736 / PMID 34136662 / 标题 Non-bonded force field model with advanced restrained electrostatic potential charges (RESP2) / 作者 Schauperl…Gilson，与 CSV 行的标题与 DOI 逐项一致 ⇒ 未挂错行 |
| 对照底稿 | `sources/cost-benchmarks.md:167`（表"电荷/质子化与力场参数"行，登记五篇 DOI 与一句 His 质子化态的引文）。那句 His 引文不在本卡所引全文里，本卡不重复、不据其写数字 |
| 证据级别 | **全文级**（本卡全部引句均可在本地纯文本里逐字命中；见第 9 节自检）。CSV 行原标"摘要级"是因为该行代表五篇而当时只有二级来源；本卡按 batches.tsv 的 `state=FULLTEXT` 写第一篇的全文级卡 |
| 未取到的部分 | 补充信息（Supplementary Figures 1–6、Tables 1–4、Notes 1–4）、Peer Review File、以及 Fig. 1–6 原图数值；GitHub 仓库（MSchauperl/RESP2、lpwgroup/respyte）本轮未抓取。**关键后果：正文没有给出任何一个 MUE/MSE 的具体数值，全部精度读数都在图里**，所以本卡只能引"哪个组合更好"的方向，不能引"好多少"的幅度；凡本卡写"原文未给数值"处即此意 |

## 1. 这篇到底解决什么（大白话）

先讲清背景，不然后面的判断看不懂：

- 经典分子动力学（MD）不用真的电子，而是给每个原子安一个固定的"部分电荷"，加上一个描述原子大小与吸引强度的 Lennard-Jones（LJ）参数（两个数：ε 深度、rmin 半径）。这两样合起来叫**非键参数**。我们所有 MD 读数的地基就是这两样。
- 行业默认做法（RESP1，1993 年提出）是：在**气相**里用一套很老的量子方法 HF/6-31G* 算分子周围的静电势，再拟合电荷去重现它。这套方法有个"凑巧"：它会把分子算得**过极化**一点，多出来的那点恰好近似"分子泡在水里被周围溶剂拉回来"的极化效应。于是这套气相算出来的电荷可以直接用在不带极化的 MD 里。
- 麻烦在于这个"凑巧"不稳定：不同分子被高估的程度不一样，甚至有的分子算出来的偶极比参考的气相值还小（本文实测到了，见第 2 节第 1 条）。也就是说，**电荷质量的调节杆被藏在一个没人控制的巧合里**。
- 这篇做的事：把调节杆拿出来变成显式参数。先用更准的量子方法（PW6B95/aug-cc-pV(D+d)Z）分别算**真空中**和**连续水介质中（介电常数 78.39）**两套静电势，各拟合一套电荷，再按 `q = (1−δ)·q_gas + δ·q_aqueous` 线性混合。δ 取多少**不靠物理推导，靠实验数据拟合**：把 δ 和 LJ 参数一起交给 ForceBalance，对纯液体的密度和汽化焓做优化，然后在一批**没参与拟合**的分子上验密度、汽化焓、液体介电常数、水合自由能。
- 结论（作者口径）：δ≈0.6 加上一起重拟合的 5 类 LJ 参数最准，介电常数改善最明显；但他们自己声明"还不能定论 RESP2 优于 RESP1"。
- **对我们项目的意义不在于它能当判据（它不能），而在于它把三件事说清了**：① MD 里那套电荷/范德华参数是被哪 4 个别相性质约束出来的；② 电荷与 LJ 必须成组拟合、成组评估，只换电荷不动 LJ 是无效的；③ 明确列出这套模型族在原理上算不准什么（电子极化贡献、介电常数系统性低估、反应/断键成键、金属配位）。第 8 节把这些落到"我们若用经典 MD 判 3′–5′ 成键几何，力场本身的可信边界在哪"。


## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **RESP1 的电荷质量靠一个不可控的巧合，而且这个巧合被本文实测破了**。现象/证据：作者先陈述机制 **"This QM method fortuitously overestimates the gas-phase polarity of molecules by about the right amount to yield charges appropriate for hydrated molecules, which are polarized by the reaction field of the solvent"**，紧接着给出反面 **"still appears to underestimate the polarization typically induced by hydration and to be inconsistent across different molecules"**（该句主语是 HF/6-31G* 的过极化；本卡从 still 起截取，因为基组写法里的星号会被门禁的 Markdown 清理步骤吃掉，逐字比对会假红）；到结果部分他们拿偶极矩直接验出来了——**"some RESP1 dipole moments are less than the corresponding gas-phase QM results"**（同因只截到 results，原文此后接 indicating that HF/6-31G* 不总能给出被假定的过极化，并夹引文编号 36）。**他们做了什么**：不再依赖巧合，改用"以最高精度为目标"的更高级 QM 方法（选型见第 3 节步骤 S0），把极化程度做成显式可调参数 δ，并用实验数据决定 δ。**留下的代价**：贵。作者自述 **"The chief drawback of RESP2 is that it is slower than RESP1, because it requires two higher-level QM calculations, one of them with an implicit solvent model, for each molecular conformer included in the calculation."**，具体量级：气相计算比 HF/6-31G* 慢约 7 倍、带隐式溶剂慢 20 倍、单分子全套约 30 分钟（单 CPU）。
2. **只改电荷不动 LJ，等于没改**。现象/证据：**"both Cerutti and coworkers 19 , and Mobley and coworkers 40 found that changing the charge parameters alone did not increase the accuracy of simulations."**；作者据此立论 **"Regardless of what improvement is brought to the calculation of partial atomic charges, the total non-bonded energy depends not only on charges but also on LJ interactions, so using more accurate charges without adjusting LJ parameters also may not in fact afford greater accuracy."**（该句本身完整、内部不夹参考文献编号，可整句照引）。**他们做了什么**：对每一个 δ 都单独用 ForceBalance 重拟合 LJ（第 3 节 S7–S8），并把三套对比做齐：RESP1/SMIRNOFF（现成参数）、RESP1/LJ opt、RESP2δ/LJ opt。**留下的代价（这是本文最反身的一条）**：LJ 一跟着动，电荷模型之间的差别就被抹平了——**"One broad observation is that, when LJ parameters are adjusted for each value of δ in the RESP2 model, the level of error becomes much less sensitive to δ , so the blue curves in Fig. 3 are much flatter than those in Fig. 2 ."**，作者明确写 **"Thus, the empirical utility of a charge model cannot be fully assessed without determining how well it performs with correspondingly optimized LJ parameters."** 也就是说**不存在一把独立于 LJ 的电荷标尺**；好处是结论更诚实，坏处是任何单点比较（只比电荷、固定 LJ）都不具备判定力。
3. **最优点 δ 是权重假设的产物，不是物理常数**。现象/证据：**"With this in mind, the best value of δ appears to be between 0.5 and 0.7, and provisionally choose the center of this range, 0.6, as the best current choice."** 作者自己拆台：**"Note, however, that the shape of the graph depends on the weighting of the four experimental properties. Here, they have been accorded equal weight."**、**"If densities and HOV were weighted more heavily, the minimum would shift to the left."**；曲线本身的抖动也来自拟合噪声——**"Some of the roughness of the graph appears to be noise, such as from slight variations in the convergence behavior of the ForceBalance runs with different values of δ ."**。**他们做了什么**：把权重如实写成等权、把取值写成临时（provisionally）、并给出 0.5–0.7 的区间而非单点。**留下的代价**：δ=0.6 只能理解为"这 4 个别相性质等权时最平衡的那个点"，换一类用途（例如只关心酶活性位点静电）它就不一定是 0.6。
4. **训练数据极窄：15 个分子的密度与汽化焓，5 类 LJ 参数**。现象/证据：**"In order to enable efficient optimization, we restricted the number of LJ types to five, corresponding to elements, C, O, and N, along with polar and nonpolar H, for a total of ten LJ parameters"**（后面原文接公式块，本卡不跨）、**"Training was based on measured HOV and pure liquid densities of 15 molecules (Fig. 8a ) with a variety of functional groups."**、**"The resulting parameters were tested against measured HOVs and densities for a separate set of 53 molecules (Fig. 8b ), as well as the measured dielectric constants and HFE of a subset of these compounds."**；简化过头会被罚：**"(Using a single H type led to markedly worse agreement with experiment; see sample results in Supplementary Table 4 )."**。**他们做了什么**：把氢拆成极性与非极性两类（极性氢用 SMARTS 定义 **"Polar hydrogens were defined by the following extended SMARTS pattern: [#1:1]-[#7,#8]."**），在 10 维参数空间里优化，并保留训练/测试分离以便与不优化 LJ 的那一轮对照。**留下的代价**：参数空间里没有 P、没有 S、没有卤素、没有金属——**这套拟合结果对核苷酸（UTP/ATP 的磷酸基团）与二价镁离子不覆盖**；作者也把"LJ 类型到底需要多少"外推给后续工作：**"These observations raise the question whether all of the LJ types in smirnoff99Frosst are necessary."**、**"This issue is beyond the scope of the present study and will be addressed in a subsequent work."**
5. **测试量里有一项（水合自由能）先天测不准这件事**。现象/证据：**"Note, however, that the HFE calculations are not pure tests of the present FF approaches, because they use the TIP3P water model, and other water models will give different results."**、**"This is because they rely on a specific water model, TIP3P, which was chosen somewhat arbitrarily from among other excellent options"**，以及 **"We anticipate that changing to a different water model will have a nonuniform effect on the accuracy of the various models tested here."**。**他们做了什么**：如实声明它不是干净的判据，并把这一层"水模型未标定"写进解释（**"It is also worth noting that both HFE and HOV could place a needless burden on fixed-charge models whose intended use is only for the calculation of condensed-phase properties."**）。**留下的代价**：本文没有换水模型重跑，**本文未解决**；他们只是把它列为未来工作。
6. **被拿来当卖点的"介电常数改善"，恰好是固定电荷模型在原理上算不准的量**。现象/证据：**"FFs that do not account explicitly for electronic polarization are not able to model the electronic contribution to the dielectric constants of organic liquids."**、**"As a consequence, they tend to underestimate these dielectric constants, particularly for nonpolar compounds where orientational polarizability cannot compensate for the lack of electronic polarization."**。**他们做了什么**：把这条当作"该换哪些标定性质"的论证——**"Thus, although dielectric constants, HOV, and HFE have long been a mainstay for the adjustment and testing of FFs, it would seem preferable to focus in the future on other experimental properties that involve only condensed-phase processes and can be modeled accurately with non-polarizable FFs e.g., liquid mixture data and surface tension"**（未来工作，本文未做）。**留下的代价**：本文第 4 项性质里至少一项（体相介电）带着原理性天花板；用"电荷更接近 QM"来解释它的改善，属于机制推测而非被隔离证明的因果。
7. **构象准备这一步的合理性是看出来的，不是算出来的**。现象/证据：**"First, up to five conformers (using the maxconfs keyword) were generated with the program Omega"**、**"Conformers with energy >10 kcal/mol (based on the Omega energy function) above the most stable conformer were discarded."**，而"这些构象代表凝聚相"的依据是 **"Based on visual inspection, the conformations generated by this protocol were not particularly compact and did not have a high degree of intramolecular hydrogen bonding, so they seem reasonably representative of the condensed phase."**。**他们做了什么**：给出明确截断阈值（≤5 个构象、>10 kcal/mol 丢弃、按 RMSD 分箱 RangeIncrement 2 / RMSRange 0.5 1.0 1.5 2.0）并把选择写成默认而非验证过。**留下的代价**：构象依赖只做"视觉确认"；对柔性大底物（寡核苷酸、NTP）本文未验证，**本文未解决**（作者仅写 more conformers may be appropriate for larger and more flexible compounds）。
8. **他们自己拒绝下最终结论**。现象/证据：**"However, this initial study cannot definitively establish RESP2 as superior to RESP1."**、**"Additional studies spanning a range of experimental observables and against the background of additional FF optimizations will be needed to fully compare the two methods."**；而 GAFF2/CHARMM/OPLS3 这些真正在用的现成力场，本文根本没测，只列为未来：**"Ultimately, it will be important to assess the accuracy of FFs based on the present approach with that of other popular force fields, e.g. OPLS3, CHARMM, and GAFF2 (refs. 48 , 49 ), which provide highly competitive performance relative to RESP1/GAFF, which in turn is similar to RESP1/SMIRNOFF"**。**他们做了什么**：把主张收缩到 δ≈0.6 是"当前最佳选择" + 一句方法论主张 **"we would argue that a charge model should ultimately be assessed within the context of a full optimization of the entire FF, based on a range of suitable reference data that can include both experimental and QM results"**。**留下的代价**：**这篇不能为"某现成力场（含 GAFF2）在某体系上有多准"提供任何实测数字**——CSV 标题常被读成 GAFF2 论文，本卡在此明确：正文只在未来工作里提到 GAFF2，未对其做任何拟合或测试。


## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **量子化学**：`psi4`（v1.3.2，做全部电荷推导与 ESP 计算）＋`Gaussian16`（只用于选型那一轮，因为当时 psi4 不支持双杂化泛函的所需性质）。方法选型：5 个方法（MP2、HF、B3LYP、PBE0、PW6B95）×5 个基组，参考基准是双杂化 DSD-PBEP86-D3BJ/aug-cc-pV(Q+d)Z。
- **构象生成**：OpenEye `Omega`（maxconfs、能量截断、RMSD 分箱三个关键词）。
- **电荷拟合**：`respyte`（开源，做 MSK 静电势选点 + RESP 两段约束拟合；代码在 github.com/lpwgroup/respyte）。
- **参数优化**：`ForceBalance`（把 δ 与 10 个 LJ 参数当作可优化量，目标函数＝训练集模拟性质对实验的偏差 + Tikhonov 正则项）。
- **性质计算引擎**：`OpenMM`（由 ForceBalance 逐轮调用）；水合自由能用 `YANK` 做 alchemical 计算、MBAR 分析。
- **实验参照数据来源**：汽化焓 HOV 全部取 ThermoML；密度取 ThermoML（缺则 PubChem）；介电常数取文献多源；水合自由能取 FreeSolv 数据库。
- **键合项（键长/键角/二面角）**：**没有拟合**，直接沿用 SMIRNOFF v1.0.7。这条对第 8 节至关重要。
- **没有用的东西**：没有湿实验、没有蛋白/核酸体系、没有自由能微扰用于结合 affinity、没有 pKa/质子化态（后者是本 CSV 行另外四篇的范围）。

### 主流程（编号 S0–S9；表内阈值全部是原文数字）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| S0 QM 方法选型 | 71 个测试分子（含 Hickey/Rowley 基准集），几何用 Open Babel 2.4.1 建、B3LYP/aug-cc-pV(Q+d)Z 优化 | 5 方法×5 基组各算气相偶极矩与 ESP（MSK 网格：17 点/单位面积、10 层），与 DSD-PBEP86-D3BJ/aug-cc-pV(Q+d)Z 参考比，同时记耗时（归一到 HF/6-31G*） | 原文未给误差阈值数字，判据表述是速度与精度的折中；结论性句子 **"We selected PW6B95/aug-cc-pV(D + d)Z as a solid combination of speed and accuracy for use with RESP2."**；另 **"As shown in Fig. 1 , all post-HF methods yield more accurate dipole moments and ESPs than HF."** | 定下 1 套 QM 方法；误差数值只在 Fig. 1 原图，正文无表 |
| S1 构象准备 | 分子的 SMILES | Omega 生成构象，关键词 RangeIncrement 2、RMSRange 0.5 1.0 1.5 2.0 | **原文数字**：最多 5 个构象（**"First, up to five conformers (using the maxconfs keyword) were generated with the program Omega"**）；**"Conformers with energy >10 kcal/mol (based on the Omega energy function) above the most stable conformer were discarded."** | ≤5 构象/分子 |
| S2 构象量子优化 | S1 构象 | psi4 做能量极小化 | 用 PW6B95/cc-pV(D + d)Z（注意：与 S4 算 ESP 用的 aug-cc-pV(D + d)Z 不是同一基组） | 优化后构象集；代表性仅由视觉检查背书（见第 2 节第 7 条） |
| S3 静电势选点 | 优化后构象 | respyte 生成 Merz-Singh-Kollman（MSK）壳层点 | **原文数字**：内外半径 1.6 Ri 与 2.0 Ri、层间距 0.2 Ri（Ri 为 Bondi 范德华半径）、每层密度 2.4 points/Å² | 每构象一组 ESP 采样点 |
| S4 两套 ESP 计算 | S3 点位 | psi4 在同一方法下算两遍：真空中一次、隐式溶剂一次 | **"The ESPs at these points were calculated with psi4 using PW6B95/aug-cc-pV(D + d)Z, first in vacuo and then with implicit solvent"**，隐式溶剂为 CPCM、**ε = 78.39**、Bondi 半径；耗时 **"Carrying out a full RESP2 calculation for one of the present training or test set compounds takes ~30 min with psi4 on a single CPU."** | 每分子两套（气相/水相）ESP |
| S5 RESP 两段拟合出 q_gas、q_aqueous | S4 两套 ESP（所有构象等权） | 标准 RESP 两段：第一段全原子独立拟合，第二段强制化学对称、只重拟合非极性部分 | **原文数字**：第一段弱双曲约束常数 0.005（中心 0.0）、第二段 0.01；两处数字之后原文紧跟的单位串被抽取成 e / a 0 2（即 e/a0²），本卡照录不另行解释。引句在数字处截断，因为其后即接公式块：**"In the first optimization step, all charges are allowed to change independently, with a weak hyperbolic restraint constant of 0.005"**／**"In the second step, chemical symmetry is enforced and only apolar parts of the molecules are refitted, with a higher restraint constant of 0.01"** | 每分子 2 套电荷 |
| S6 混合成 RESP2 电荷 | q_gas、q_aqueous | 按 δ 线性组合（原文式 1：q_RESP2 = (1−δ)q_gas + δ q_aqueous） | δ 扫描范围与步长：**"The program ForceBalance 41 was used to optimize the LJ parameters for RESP1 charges and for RESP2 with values of δ from 0 to 1 in steps of 0.05."**；等价性 **"Note, too, that setting δ = 0.5 causes RESP2 charges to equal IPolQ-Mod charges"** | 21 套候选电荷（δ = 0, 0.05, …, 1） |
| S7 LJ 参数优化（拟合） | 每套电荷 + 训练集 15 分子的实验 HOV 与密度 | ForceBalance 调 5 类 LJ（C/N/O/极性 H/非极性 H）×2 参数 = 10 维；起点取 SMIRNOFF v1.0.7（**"Starting parameters were drawn from SMIRNOFF v1.0.7 (Supplementary Notes 1 )."**）；先验宽度 ε = 0.4184 kJ/mol、rmin-half = 1.0 Å；正则权 w_reg = 10；性质尺度因子 d_HOV = 0.3 kJ/mol、d_density = 30 kg/m³ | 终止条件原文数字：**"The ForceBalance procedure was terminated when the step size for the mathematical parameters fell <0.01 or the objective function changed <1.0 between two iterations"**；极化氢定义 **"Polar hydrogens were defined by the following extended SMARTS pattern: [#1:1]-[#7,#8]."** | 每个 δ 一套 10 个数（数值本体在 Supplementary Fig. 6 与 Notes 2–4，正文未给） |
| S8 性质计算（拟合与测试都靠它） | 参数组合 | ForceBalance 调 OpenMM：每分子每轮跑一次气相 + 一次液相模拟；液相密度取 NPT 平均体积、HOV 取气/液平均势能差加 RT、介电常数取盒子偶极涨落 | 原文数字：气相 **"Single-molecule gas-phase simulations were run for 25 ns (5 ns equilibration, 20 ns production) with a timestep of 1 fs using a Langevin integrator with a collision frequency of 1 ps -1 and, infinite distance cutoffs and without periodic boundary conditions."**；液相 **"Liquid-phase calculations, with 700 molecules in the box, were run for 1.2 ns (0.2 ns equilibration, 1 ns production), with a Langevin integrator timestep of 1 fs and a collision frequency of 1 ps -1 ."**；温度 **"In each iteration, a gas-phase and a liquid-phase simulation at T = 298 K were run for each molecule, to enable the calculation of liquid state properties and of the HOV."**；静电项 **"For the liquids, long-ranged electrostatics were included via Particle Mesh Ewald summation with a cutoff of 8.5 Å."**（另有 1 atm Monte Carlo barostat、每 25 步一次、长程色散校正、含氢键用 CCMA/SETTLE 约束、键合项一律 SMIRNOFF v1.0.7） | 每个参数组合得到 2–4 个别相性质 |
| S9 独立测试与总账 | 未参与拟合的 53 个分子 | 测密度与 HOV；其子集测液体介电常数；全部分子的水合自由能用 YANK 另算 | **"The resulting parameters were tested against measured HOVs and densities for a separate set of 53 molecules (Fig. 8b ), as well as the measured dielectric constants and HFE of a subset of these compounds."**；HFE 设置：**"We used 5 lambda values in gas-phase and 20 lambda windows (5 windows for the electrostatics and 15 for the steric interactions) for the solution."**、**"The calculations used Hamiltonian replica exchange over 1000 iterations consisting each of 500 timesteps of 2 femtoseconds each."**、分析用 MBAR；总评分用相对基线 RESP1/SMIRNOFF 的平均无误差（原文式 6，N_P = 4 个性质等权） | 得到 Fig. 2（不优化 LJ）、Fig. 3（优化 LJ）、Fig. 4（总相对误差随 δ）三条曲线 + 结论 δ 最优 0.5–0.7、暂定 0.6 |
| S10 电荷本身的对照检验 | RESP1 vs RESP2₀.₆ 的分子偶极与原子电荷 | 拿电荷算出的偶极直接与 QM 偶极回归；并画电荷两两散点（RESP1/RESP2₀.₆、RESP2 气相/水相、AM1-BCC/RESP1） | **"Thus, dipole moments computed with RESP2 0.6 charges have R 2 values of 0.99 against both gas-phase and aqueous QM dipole moments, while RESP1 yields R 2 values of 0.97 and 0.96, respectively."**；**"In contrast, RESP2 dipole moments are never below the corresponding QM gas-phase results."** | RESP2 偶极比 RESP1 大约 10%（斜率给出）、单个分子差值可达 30%；而电荷本身幅度几乎不变（回归斜率 0.999） |

**这套流程的骨架值得单独记住**：它不是一次"算个电荷然后用起来"，而是一个**闭环拟合工程**——QM 产生候选电荷 → 分子模拟把参数翻译成可比实验的量 → ForceBalance 反算参数 → 独立测试集验收。所有判定都在**体相纯液体性质**层面完成，从头到尾没有一个蛋白、一个核酸、一个反应坐标。


## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段，均在本地全文里可搜到） |
|---|---|---|
| 71 molecules | QM 方法选型用的测试集规模（比偶极与 ESP 的误差） | We used a set of 71 molecules (Supplementary Fig. 3 ) |
| 5 方法 × 5 基组 | 选型网格：MP2/HF/B3LYP/PBE0/PW6B95 × aug-cc-pV(D+d)Z、cc-pV(T+d)Z、jun-cc-pV(T+d)Z、aug-cc-pV(T+d)Z、aug-cc-pV(Q+d)Z | We evaluated five methods with five different basis sets against the DSD-PBEP86-D3BJ reference |
| DSD-PBEP86-D3BJ / aug-cc-pV(Q + d)Z | 参考（金标准）级别；双杂化，接近 CCSD 精度但便宜得多 | High-quality reference calculations were carried out using DSD-PBEP86-D3BJ (ref. 42 ) with an aug-cc-pV(Q + d)Z basis set |
| PW6B95/aug-cc-pV(D + d)Z | 最终选定的电荷推导级别 | We selected PW6B95/aug-cc-pV(D + d)Z as a solid combination of speed and accuracy |
| 约 7 倍 / 20 倍 | 相对 HF/6-31G* 的耗时（气相 / 再加隐式溶剂） | these gas-phase calculations are around seven times slower than HF/6-31G*; When used with implicit solvent, the calculations are 20 times slower than HF/6-31G* |
| ~30 min（单 CPU） | 一个训练/测试分子的完整 RESP2 电荷推导耗时 | takes ~30 min with psi4 on a single CPU |
| ε = 78.39（CPCM）、Bondi 半径 | 水相那套 ESP 的隐式溶剂设置 | first in vacuo and then with implicit solvent（ε = 78.39, CPCM (refs. 61 , 62 ), Bondi radii） |
| ≤5 构象；>10 kcal/mol 丢弃 | 构象数与能量截断 | up to five conformers (using the maxconfs keyword); Conformers with energy >10 kcal/mol |
| MSK 壳层 1.6 Ri / 2.0 Ri，层间距 0.2 Ri，2.4 points/Å² | 静电势选点密度（respyte） | with inner and outer radii of 1.6 R i and 2.0 R i , and 0.2 R i spacing between point layers |
| 17 点/单位面积、10 层 | 选型那一轮用的 MSK 网格（与上面不同） | ESP points were selected based on (MSK) grids 28 with 17 points per unit area and ten layers |
| 约束 0.005 e（第一段）/ 0.01 e（第二段） | RESP 两段拟合的双曲 restraint 常数 | with a weak hyperbolic restraint constant of 0.005; with a higher restraint constant of 0.01 |
| δ = 0 → 1，步长 0.05（共 21 档） | 被优化的电荷极性旋钮扫描范围 | with values of δ from 0 to 1 in steps of 0.05 |
| 5 类 LJ / 10 个参数 / 10 维空间 | 被重拟合的范德华参数规模（C、N、O、极性 H、非极性 H，各 ε 与 rmin-half） | for a total of ten LJ parameters; the optimizations were done in a ten-dimensional parameter space |
| 训练 15 个分子（HOV + 密度）/ 测试 53 个分子 | 参数拟合与验收的数据规模 | measured HOV and pure liquid densities of 15 molecules; a separate set of 53 molecules |
| N_P = 4 | 总评分里的实验性质数（密度、HOV、介电常数、水合自由能），等权 | Here j indexes the N P = 4 experimental properties |
| 先验宽度 0.4184 kJ/mol（ε）、1.0 Å（rmin-half）；正则权 w_reg = 10；尺度因子 0.3 kJ/mol（HOV）、30 kg/m³（密度） | ForceBalance 的目标函数与约束强度 | Prior widths were set to 0.4184 kJ/mol; w reg = 10; d HOV = 0.3 kJ/ mol; d density = 30 kg / m 3 |
| 步长 <0.01 或目标函数两次迭代变化 <1.0 | 优化终止条件 | the step size for the mathematical parameters fell <0.01 or the objective function changed <1.0 between two iterations |
| 气相 25 ns（5 平衡 + 20 生产）；液相 1.2 ns（0.2 + 1.0），700 分子/盒 | 每轮拟合的模拟采样量 | run for 25 ns (5 ns equilibration, 20 ns production); run for 1.2 ns (0.2 ns equilibration, 1 ns production) |
| 1 fs 步长、Langevin 1 ps⁻¹、298 K、1 atm（MC barostat 每 25 步）、PME 截断 8.5 Å、长程色散校正 | 模拟设置（键合项未拟合，取 SMIRNOFF v1.0.7，X-H 键约束 CCMA/SETTLE） | Single-molecule gas-phase simulations were run for 25 ns; Liquid-phase calculations, with 700 molecules in the box; a cutoff of 8.5 Å |
| HFE：YANK，气相 5 个 λ、溶液 20 窗口（静电 5 + 位阻 15），1000 轮 × 500 步 × 2 fs，MBAR | 水合自由能计算量 | We used 5 lambda values in gas-phase and 20 lambda windows; over 1000 iterations consisting each of 500 timesteps of 2 femtoseconds each |
| R² = 0.99（RESP2₀.₆）对 0.97 / 0.96（RESP1） | 电荷推出的分子偶极与 QM 偶极的回归 | have R 2 values of 0.99 against both gas-phase and aqueous QM dipole moments, while RESP1 yields R 2 values of 0.97 and 0.96 |
| 偶极约大 10%；单分子差值可达 30%；电荷回归斜率 0.999 | RESP2 相对 RESP1 的极化幅度变化（电荷本身量级几乎不变） | RESP2 charges tend to yield 10% larger dipole moments; range up to 30%; the regression coefficient (slope) of 0.999 |
| 腈碳 ε：0.21 → 0.085 kcal/mol | 5 类 LJ 里被改动最大的一个数 | which decreases from 0.21 kcal/mol to 0.085 kcal/mol |
| δ 最优 0.5–0.7、暂定 0.6；0.6 与 IPolQ 的 0.5 接近 | 全文唯一给出的"推荐参数值"，且明确是临时的 | the best value of δ appears to be between 0.5 and 0.7 |
| 1 个数字都没有 | **正文没有给出任何一个 MUE/MSE 数值**；Fig. 2/3/4/5/6 的误差棒全在图里，本卡无法登记，也不能引用 | 正文相关句只给方向（about as accurate as; more accurate; somewhat less accurate），无数值 |


## 5. 结论——作者说了什么

1. **RESP2 的定义与推荐值**：用一个显式参数 δ 混合气相与水相 RESP 电荷；配合高级别 QM（PW6B95/aug-cc-pV(D+d)Z）与实验数据拟合，作者主张 **"We argue that RESP2 with δ ≈ 0.6 (60% aqueous, 40% gas-phase charges) is an accurate and robust method of generating partial charges, and that a small set of Lennard-Jones types is a good starting point for a systematic re-optimization of this important non-bonded term."**
2. **电荷不能单独评估**——这是全文最强的方法论主张：**"As a consequence, the utility of a given charge set cannot be properly assessed unless LJ parameters are adjusted along with it."**，并进一步 **"Thus, the empirical utility of a charge model cannot be fully assessed without determining how well it performs with correspondingly optimized LJ parameters."**
3. **重拟合 LJ 带来普遍改善，且只需 5 类 LJ**：**"When the complete non-bonded force field model, including Lennard-Jones parameters, is optimized to liquid properties, improved accuracy is achieved, even with this reduced set of five Lennard-Jones types."**；**"A key observation is that optimizing LJ parameters significantly reduces the errors relative to experiment for all of the charge sets."**；并推测 **"The present LJ optimization results also suggest that the many LJ types in most current FFs may not be needed, because similarly accurate results might be obtainable with a much smaller number of types."**
4. **δ 一优化 LJ 就变得不敏感**（第 2 节第 2 条），因此最终推荐是 **RESP2₀.₆ + 与它一起优化的 LJ**，相对基线 RESP1/SMIRNOFF 在密度、介电常数、HFE 上更好、HOV 略差：**"Overall, RESP2/LJ opt with δ < 0.6 led to improved dielectric constants, densities, and HFE, but some loss in accuracy for HOV, relative to RESP1/LJ opt."**
5. **明确的自限**：**"However, this initial study cannot definitively establish RESP2 as superior to RESP1."**，需要更多观测量与更多力场层优化；且他们把 GAFF2/CHARMM/OPLS3 只列为**未来才需要比较**的对象（见第 2 节第 8 条）。
6. **给出后续方向**：训练二代 AM1-BCC 去匹配 RESP2（**"It may thus be of interest to develop what amounts to a second-generation AM1-BCC method"**）、把 RESP2 当物理基准去训快速机器学习电荷（**"The encouraging results for RESP2 0.6 found here suggest it as a promising physics-based charge model to train fast ML methods."**）、把标定性质换成只涉及凝聚相的实验量（混合物数据、表面张力），以及 **"It is also worth noting that optimization of valence terms, especially torsions, along with the current non-bonded forces should result in further improvement in accuracy."**（价键项尚未做）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正交付的不是 RESP2，而是一条反身规则：改了 A 就必须允许 B 一起改，否则结论不成立**。这条直接打在我们项目的软处：我们若换配体电荷模型（AM1-BCC → RESP2 之类）或换水模型，**旧的验证与阈值一律作废**，必须成组重跑；把"只改一个字段"当成小改动是不成立的。
2. **精度证据全在图里，正文一个 MUE 都没给**。所以对我们而言，这篇的可引用内容只有"方向 + 流程 + 边界"，**任何想用它的数字画误差棒的做法都必须先取回原图或 SI**（本轮未取，故本卡未登数字）。
3. **标定面比想象中小**：15 个分子的密度+汽化焓，5 类元素参数，性质全是体相单相量。它证明的是"这套参数族在这批纯液体上自洽"，**不是**"这套参数对任意含 P/S/金属的生物分子可靠"。我们对 UTP/ATP/磷酸二酯键的 MD 属于**外推使用**，外推声明必须由我们自己写。
4. **"电荷不是可观测量"这一句决定了校验层次**（原文 **"Because atomic charges are not physical observables, one cannot directly assess the accuracy of the charges themselves."**）：所以"我们算出来的电荷看着合理""活性位点静电看起来对"不能作为证据；只有把它转成可观测的量（偶极、介电、水合自由能，或在我们的场景里——产物化学）才算检验。这条与本库口径里"判据必须能说清它对应哪个物理量"是同一件事。
5. **固定电荷把环境极化折进一套静态参数，因此参数天生带环境**。本文用 ε=78.39 的水做参考，作者自己承认这对低介电环境是简化。我们判的是酶活性位（低介电、强电场、His 质子化态随环境变），这是**双重外推**：既外推出参数覆盖的元素范围，又外推出它被拟合时所假设的环境。这也解释了为什么同一 CSV 行要挂 constant-pH 基准那几篇——本卡这篇管不到质子化态。
6. **"LJ 与电荷的耦合"给我们的分块记账一个硬约束**：非键读数（距离、取向、静电）与键合读数（键长、角、二面角）来自**两套不同来源、且本文只拟合了前者**，因此它们在证据上不该被当成同源的可加项（与本仓库 `sources/function-assignment-workflows.md:107` 记的"同一构象系综的统计不可相乘"是同一类错误的两个面）。


## 7. 局限与失败（作者的 + 我们读出的）

**作者自认的**

1. 不能定论：见第 5.5 条原句；且需要跨更多观测量与更多层（价键项）的优化才能比较。
2. 贵：见第 2.1 条的 chief drawback；作者给出的出路（二代 AM1-BCC / ML 电荷）都只是设想，本文未做。
3. 测试量本身有问题：HFE 依赖 TIP3P（**"which was chosen somewhat arbitrarily from among other excellent options"**），HOV 与 HFE 对只做凝聚相计算的模型是 **"could place a needless burden on fixed-charge models whose intended use is only for the calculation of condensed-phase properties"**。
4. 固定电荷的原理性天花板：算不出有机液体介电常数的电子贡献，并系统性低估它（第 2.6 条两句原句）。
5. 价键项没做：非键之外的全部参数原封不动沿用 SMIRNOFF v1.0.7。

**我们读出的（并且是第 8 节的依据）**

6. **正文与正文之间自相矛盾，而且矛盾恰好落在最关键的判据方向上**。第 3.2 节（不优化 LJ）写 **"However, pure liquid dielectric constants are somewhat more accurate with RESP2 charges when δ > 0.2."** 与 **"with HOV and densities somewhat more accurate overall for δ > 0.5 but dielectric constants and HFE more accurate for δ > 0.5"**（前一句说 HOV/密度、后一句说介电/HFE，两个方向都写 δ > 0.5，可这句话开头却是"随 δ 偏离 0.5 时各性质的变化模式不同"）；而第 3.3 节（优化 LJ）写的是相反方向：**"However, RESP2/LJ opt with δ < 0.2 yields the most accurate dielectric constants"**、**"Overall, RESP2/LJ opt with δ < 0.6 led to improved dielectric constants, densities, and HFE"**。我们在本地 XML 里核对过，两个方向的符号（&lt; 与 &gt;）确实是原文所载，不是抽取丢字符。**结论：这段的 δ 方向性描述不可作为可复现判据引用**，只能引 Fig. 4 的结论句（δ 0.5–0.7、暂定 0.6）。这是本卡认为全文最可疑的一处。
7. **没有任何蛋白/核酸/金属/磷酸酯体系**：训练与测试全是小分子有机液体的体相性质，71+15+53 分子集合里不含酶、不含活性位点、不含 Mg²⁺。
8. **精度数字没进正文**：全部 MUE/MSE 在图里，正文给的是 about as accurate、somewhat more accurate 这一类形容词。引用它支撑任何量化误差界，必须先去取原图/SI。
9. **δ=0.6 是等权假设下的拐点**（第 2.3 条），不是物理常数，且曲线粗糙处含拟合噪声。
10. **构象代表性靠目测**（第 2.7 条），柔性分子/多构象体系未验证。
11. **CSV 行标题容易被读成 GAFF2 论文**：本文对 GAFF2 只有未来工作的一句提及，**没有任何拟合或对比实验**；如果我们的文档需要"GAFF2 非键参数被标定到什么程度"，这篇不能回答（本卡未在本仓库找到能回答它的其它全文）。

## 8. 迁移判断：哪些能搬、哪些不能搬：我们若用经典 MD 判 3′–5′ 成键几何，力场本身的可信边界在哪

**先说结论（一句话版）**：这篇把"非键参数能被标定到什么程度"讲得很清楚，而**我们真正要判的那件事（3′–5′ 磷酸二酯键能否形成）恰好落在这套标定的三个盲区里——键合项没拟合、P/金属不在参数集里、反应坐标在固定拓扑力场里根本不存在**。因此它能迁移给我们的是**声明与配套纪律**，不是任何可信度证据。

**可迁移（具体怎么做）**

1. **成组引用参数，并写明"这套电荷配的是哪套 LJ"**。第 2.2 条已经证明：只改电荷不改 LJ 的改动不会带来精度收益。→ 落地：每个 MD 体系在 `run.md` 里必须记 全蛋白质（如 ff14SB/ff19SB）+ 配体电荷模型（AM1-BCC 或 RESP 几段约束）+ LJ 组合 + 水模型 四元组，四元组里任何一项变动，之前所有几何阈值同时作废（要重新校验，不能沿用）。
2. **把"能不能算准"转成可观测量再检验**。原文的检验链是：电荷 → 偶极/介电/密度/汽化焓 → 与实验比。我们没有体相实验，等价做法只能是：把力场层的检验压到**能被 QM 或晶体统计量到的量**（例如把活性位内该键合几何与同类晶体结构分布对比、把非键接触能与 xTB/PySCF 单点比较），而不是用"看起来合理"。本项目机制层已冻结的 3′–5′ 进攻几何口径（距离 ≤4.0 Å、角 ≥150°，登记在 uaa-top2-md-20261011 工程，不在本仓库）属于**几何统计**，其可信边界必须按本卡第 3、4 条明写。
3. **照抄它的"标定面申报"写法**：训练 15 / 测试 53 / 4 性质 / 5 类 LJ 这种一句话把外推面写死的方式。→ 我们任何"力场/判据可用"的声明都要配一句"在 X 个化学环境、Y 个观测量、Z 类元素上标过；P/S/Mg/酶活性位不在其中"。
4. **ForceBalance 那套口径直接可用**（第 4 节先验宽度、正则权、终止条件三行）：若我们未来真要去拟合核苷酸片段或金属位参数，这是最小可复现的模板，且它同时示范了"训练/测试分离 + 独立数据库做验收"。
5. **模拟设置可作交叉核对基线**（OpenMM + PME 8.5 Å + 1 fs + H 键约束 + MC barostat），与我们同引擎；但它自己的采样并不长（液相仅 1.2 ns、每轮如此），说明**体相性质收敛相对容易，蛋白活性位的几何分布不是**——不要用它的设置时长来论证我们的 420 ns 够了。

**不可迁移（为什么不能照搬，逐条给理由）**

1. **δ≈0.6、5 类 LJ 够用、介电常数改善——这三条都不是"成键几何可信度"的任何一档证据**。本文没有任何一处涉及蛋白、核酸、酶活性位或反应；把它当"我们 MD 判成键可信"的背书属于跨域滥用（本库口径禁止借无关域阈值当闸口，同一纪律适用）。
2. **键合项（键长/键角/二面角）本文完全没拟合**，作者只写价键项优化"应能带来进一步改善"（第 5.6 条原句）。所以我们真正看的 P–O 距离、进攻角、糖环折叠、核糖 2′/3′-OH 取向里，**凡由键合项与二面角决定的部分，其误差界不在这篇（也不在 RESP2 系）的标定范围内**；而"3′–5′ vs 2′–5′"的区分恰恰由糖环折叠与 OH 取向决定，这部分是全文标定面最薄的一层。
3. **参数集不含 P、S、卤素与任何金属**（只有 C/N/O/H 五类）。两金属离子机制（motif A 的 Mg²⁺/Mn²⁺）是我们判定的核心，而金属配位、电荷转移、配位数变化在这套参数里根本没有定义 → 我们的"金属 A/B 位几何"读数**不能引用本篇作为力场可信依据**；本仓库 `sources/function-assignment-workflows.md` 里那条"必须以 apo/金属游离态为参照"的要求，仍是唯一可执行的防御。
4. **固定拓扑 MD 里"成键"这件事不存在**。本文全部计算都在不改变连接性的前提下评估体相性质；我们项目已经出现过实际后果：中间体产物在拓扑里被预置为已连接（属 uaa-top2-md-20261011 工程记录），于是那条 MD 永远不会"成键"。→ 结论：经典 MD 能给的只有"预反应复合物的取向与距离分布"，"能不能越过能垒"必须由 QM/xTB 的一维剖面回答（本项目实测 xTB 271 原子约 153 s/单点，只做一维剖面），力场层不给这个证据。
5. **静电环境双重外推**：本文电荷是在 ε=78.39 的水里标定、用于纯有机液体（作者自陈 **"This choice might be expected to lead to excessive polarization of the compounds making up organic liquids with much lower dielectric constants."**）；酶活性位是低介电、强电场、且质子化态依赖环境的环境。本 CSV 行另外那篇 QM/MM 综述里"经典力场无法可靠预测 His 的环境依赖质子化态"那句话（英文原句登记在 `sources/cost-benchmarks.md:167`）**不出现在本卡所引全文里**，本卡不把它当本文引句使用 → 我们若判静电引导（正电环对三磷酸），必须自己声明这是外推。
6. **它不提供任何"命中率/成功率"**，所以绝不能出现在我们任何一版的成功概率表里；本卡在时间线里的作用是"给 MM 层结论加边界声明"，与 B09 那类漏斗卡不共享任何数字。


## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K56_PMC8204736_text.txt

- **本卡全部引句只照这一份文件写**。同一篇论文可能有 Europe PMC 与 NCBI 两份抽取版本，句中夹的参考文献编号（例如 refs. 19 , 40 ）在两版里位置不同，因此换版本就会逐字不命中。
- 底稿特性（决定了引句怎么取）：① 全文是**单行无换行**文本；② 公式的 LaTeX 块（以 \documentclass 开头、含 $$ 的残留）未被剥离，紧贴在数字后面；③ 图号与补充材料编号被抽成带空格的裸文本（如 Fig. 3 、Supplementary Table 4 ）。凡句子中间含公式块或跨句夹编号处，本卡一律**在数字之前截断或拆成两条**，没有跨句拼接、没有省略号冒充。
- 底稿身份复核见第 0 节（DOI/PMCID/PMID/标题/作者逐项与 CSV 行一致，未挂错行）。
- 对照底稿：`sources/cost-benchmarks.md:167`（本 CSV 行登记的五篇清单，其中 W-RESP、AM1-BCC II、constant-pH MD 基准、JPCB 晶体质子化态四篇**本地无全文**，本卡未引其任何数字）；`sources/function-assignment-workflows.md:107` 与 `:174`（我们项目侧"固定拓扑 MD 的构象统计"口径，第 8 节引用为项目内部依据，不作为本文引句）。
- CSV 字段映射：本文第 3 节 ↔ 计算筛选判据/阈值数字/候选生成方法（本行需按"参数化方法"重写）；第 4 节 ↔ 阈值数字/成本统计；第 7–8 节 ↔ 在方法演进链的位置 + 是否用 MD/QM 两列的说明文字。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K56" --no-report`（参数：--only K56 --no-report；输入：本卡 + 上面这一份底稿 + `sources_map.json` 登记清单）；结果见本节末的运行输出行（PASS K56 quotes=N/N），脚本把卡内所有不含中日韩字符、被直双引号包住、≥20 字符且≥12 个字母的片段在底稿里做逐字查找，任何一条不命中即 FAIL。

<!--CSV回填
work_type=方法（非键力场参数化；本 CSV 行为五篇一组，本卡只覆盖第一篇 RESP2 2020）
target=小有机分子的原子中心固定部分电荷 + Lennard-Jones 非键参数（C/N/O/极性 H/非极性 H 五类；无 P/S/卤素/金属；无蛋白与核酸体系）
backbone_generation=不适用（本文不生成候选分子或蛋白；被"生成"的候选是 21 档 δ 的电荷组合与各档配套重拟合的 10 个 LJ 参数）
computational_filters=无筛选漏斗；判据是拟合/验收目标性质——纯液体密度与汽化焓（训练），密度、汽化焓、液体介电常数、水合自由能（测试，式 6 的 E(δ) 等权取平均相对误差）；辅助检验为电荷偶极与 QM 偶极的回归、RESP1/RESP2/AM1-BCC 电荷两两散点
thresholds=δ 最优区间 0.5-0.7、暂定 0.6（等权假设下）；δ 扫描 0-1 步长 0.05；构象上限 5 个且 >10 kcal/mol 丢弃；RESP 约束 0.005 e 与 0.01 e；ForceBalance 终止为步长 <0.01 或目标函数两迭代变化 <1.0；先验宽度 0.4184 kJ/mol 与 1.0 Å；PME 截断 8.5 Å；R2 0.99 vs RESP1 的 0.97/0.96
md_used=是-参数拟合与性质评估引擎（OpenMM 由 ForceBalance 逐轮调用：气相 25 ns、液相 700 分子 1.2 ns，算密度/汽化焓/介电涨落；YANK 算水合自由能；不是候选筛选闸口，也不判任何几何成键问题）
qm_used=是-电荷与静电势参考数据生产（PW6B95/aug-cc-pV(D+d)Z 气相 + CPCM 隐式水 ε=78.39 两套 ESP；选型网格 5 方法 x 5 基组；参考级 DSD-PBEP86-D3BJ/aug-cc-pV(Q+d)Z；71 分子）
experimental_methods=无湿实验；全部对照取自实验数据库：ThermoML（汽化焓、密度）、PubChem（密度缺值补充）、文献多源（液体介电常数）、FreeSolv（水合自由能）
pipeline_counts=选型 71 分子 x 5 方法 x 5 基组 → 每分子 <=5 构象两套 ESP → 21 档 δ → 每档 10 个 LJ 参数（5 类 x 2）→ 训练 15 分子（密度+HOV）→ 测试 53 分子（密度+HOV，子集介电常数）+ FreeSolv 水合自由能
hit_rate=不适用（本文非候选筛选，无通过率/命中率类读数；正文也未给出任何 MUE/MSE 数值，误差全在 Fig. 2-4 图内）
best_metric=未记录（本文无 Kd/活性类指标；最接近"最好值"的结论是 δ=0.6 时相对 RESP1/SMIRNOFF 在密度、介电常数、水合自由能上更好、汽化焓略差，正文未给数值）
cost_or_stat_note=单分子完整 RESP2 电荷推导约 30 min（psi4 单 CPU）；气相比 HF/6-31G* 慢约 7 倍、含隐式溶剂慢 20 倍；每轮拟合需气相 25 ns + 液相 1.2 ns x 15 个训练分子；作者自陈 chief drawback 即耗时
role_in_timeline=把"固定电荷该有多极"从 HF/6-31G* 的巧合过极化变成显式可调参数 δ，并与 LJ 成组对实验体相性质重拟合——是 SMIRNOFF/OpenFF 系非键参数"可拟合化"的节点论文；其方法论主张（电荷不可脱离 LJ 单独评估、最终要放进整个力场的全优化里判）即 Open FF 项目的中心策略；对 GAFF2 等现成力场本文只在未来工作里提及、未做任何拟合或对比；在我们时间线里承担 MM 层结论的边界声明（键合项未拟合、无 P/Mg 参数、固定拓扑不含反应坐标）
source_pointer=data/literature_cards/fulltext/K56_PMC8204736_text.txt（Commun Chem 2020, 3:44, DOI 10.1038/s42004-020-0291-4, PMC8204736, PMID 34136662, SHA-256 a4155d1f3ea55855…）+ sources/cost-benchmarks.md:167（本行五篇清单；其余四篇本地无全文）
CSV回填-->

