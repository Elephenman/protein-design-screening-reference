# [Z08] 把"筛选器该用哪个"变成可测问题：同一批构象上比 MM-PBSA / T-REMD / Rosetta / 非平衡 PMF，并给出反直觉的"跑更久反而更不准"

Ida Autiero, Damiano Buratto, Fengyi Guo, Wanding Wang, Malay Ranjan Biswal, Kevin C. Chan, **Ruhong Zhou**, Francesco Zonta（CNR 那不勒斯 / 浙大 IQB / 西交利物浦）
Journal of Chemical Theory and Computation 2025, 11(21):11271-11281（在线 2025-10-23）· DOI 10.1021/acs.jctc.5c01231 · PMID 41129205 · PMCID PMC12613313
开放获取（CC BY 4.0）· 预印本 10.1101/2025.09.25.678535

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **Z08**（组：周如鸿组） |
| 本文取回方式 | Europe PMC `search` 定位后取 `fullTextXML`（inventory 记 `fetch_channel=epmc_search_then_fulltext`） |
| 本地全文 | `data/literature_cards/fulltext/Z08_PMC12613313_text.txt`（48,342 B，SHA-256 `a1cb212dacac1914…`）；同源 XML `Z08_PMC12613313_fullTextXML.xml`（106,939 B，SHA-256 `ef8af3310b01c1c7…`） |
| 身份复核 | 全文首行含 `PMC12613313 41129205 10.1021/acs.jctc.5c01231` 与标题原文 "Assessing Computational Strategies for the Evaluation of Antibody Binding Affinities"，作者与 CSV 登记一致 ⇒ 与编号对得上（这条必须查，因为抓取走的是 search 而非直接 PMCID） |
| 对照底稿 | `sources/zhou.md:110-119`（原卡，摘要级）、`sources/zhou.md:180`（全组 QM 取证结论把 Z08 列为"SMD-PMF 被其自有数据否决"）、`sources/zhou.md:211`（演进链第③项"筛选器本身的可靠性实证"）、`sources/zhou.md:230`（当时列为"未核验的付费全文细节：Z08 各方法相关系数数值"——**本卡已补齐**） |
| 证据级别 | **全文级**。注意 `inventory.json` 里本行的 `evidence` 字段仍写"摘要级"（登记时未拿到正文），本卡的级别判定以"已登记且存在的本地全文"为准；差异已在此写明，不改登记文件 |
| 未取到的部分 | ①补充材料（Figure S1 Ramachandran 对比、Figure S2 ΔG 的温度依赖 PDF）；②各方法的**标准差/置信区间与 R² 的统计显著性**（正文只给点估计）；③实验端 K_D 原值与测定方法（作者写"have been characterized experimentally in previous work"，未在本篇复述）；④Table 1 里 MMPBSA 列的部分数值排版在去标签后有粘连，本卡不复述未确认的单元格 |

## 1. 这篇到底解决什么（大白话）

这一篇**不设计任何新分子**，它检验的是"用来筛分子的那把尺"。体系固定：一个抗 CXCR2 抗体（文中改名 AbWT）加 8 个点突变变体，结合同一个 CXCR2 N 端肽，实验亲和力大约跨 10 倍。他们让**四把计算尺量同一批东西**：①常规 MD + MM-PBSA（前作）；②温度副本交换 MD（T-REMD）+ MM-PBSA；③同一批构象上用 Rosetta 能量函数打分；④非平衡方法（steered MD 起步 + umbrella sampling 重建 PMF）。然后跟实验值对相关性。

结果三件事：**平衡 MM-PBSA 比非平衡 PMF 更贴合实验**（R² 0.57 vs 0.19）；**Rosetta 在同一批构象上几乎无相关**（0.01/0.02）；以及最反直觉的一条——**采样更多、轨迹更长，相关性反而下降**（用满 20-100 ns 只有 0.29/0.31，只用 20-50 ns 有 0.57），于是他们转而推荐"10 段 5 ns 短模拟取后半段做 MM-PBSA"作为**便宜的筛选协议**（每 GPU 每天可测 3-5 个抗体）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **难点：MM-PBSA 结果方差太大，端点法对构象取样极敏感**。原句："an important shortcoming of MMPBSA is the large variance of the results, even within a well-equilibrated and homogeneous simulation."，他们的因果判断是 "For this reason, it is essential to obtain an accurate sampling of the configuration space."
   **应对**：上增强采样，但**只把增强采样限制在界面**以压成本——"To reduce the computational cost of the calculations, we limited the T-REMD strategy to the interface between the antibodies and peptides."；界面外原子被谐波约束住："Antibody atoms outside the region of interaction, defined by all the residues within 15 Å of the peptide, were harmonically restrained at the starting position with a force constant of 10 kJ mol"（原句此后接单位与维度描述）。规模：9 个变体各 64 副本 × 100 ns，300-380 K，交换尝试每 2 ps ⇒ "For each of the nine antibody variants considered, we performed 64 replicas of 100 ns simulations, with temperatures ranging from 300 to 380 K, resulting in a total simulated time of 57.6 μs."
   **应对后仍留下的代价**：**每个亲和力评估要 6.4 μs**（"Both RE-MMPBSA and PMF required long simulations for the evaluation of each binding affinity"），而且增强采样并没有让相关性变好（见第 2.3 条）；另外，界面外约束意味着非界面构象变化被人为抹掉，这本身可能改变结合自由能的构成。

2. **难点：怎么证明"增强采样"真的增强了**。
   **应对**：加一个**独立的、与方法结论无关的**检查——关键肽残基的 Ramachandran 覆盖："Sampling enhancement was verified by monitoring the Ramachandran angles for the peptide residue critical to binding ( Figure S1 ): the exploration of the φ-ψ torsion angles is noticeably greater in the T-REMD simulations than in the standard MD simulations."；再加"副本交换需要时间"的物理解释来定丢弃窗口："This appears to be the time required to obtain an appropriate number of exchanges between the different temperature replicas i.e. to achieve equilibration for the 300 K simulations."，据此 "Therefore, the first 20 ns were excluded in the calculation of the average binding free energies."
   **代价**：验证只看一个残基的二面角，且只放在补充材料里；丢弃窗口由作者按图判定（正文只写 "the free energy decreases during the first 20 ns of the simulation before reaching a stable plateau"），不是自动化的收敛判据。

3. **难点（本文最要紧的一条）：更多采样、更长轨迹 ≠ 更准**。原句："In our previous work, longer simulations did not necessarily yield better agreement with experimental data." 与实测 "the prediction based on the 20-50 ns interval showed a higher correlation ( R 2 = 0.57) with the experiments than the prediction obtained with the full 20-100 ns interval ( R 2 = 0.29)"；图注给出的另一处口径是 "The correlation coefficients are R 2 = 0.31 and R 2 = 0.57, respectively."（正文 0.29 / 图注 0.31，同一件事两个数字）。
   **应对**：①把它写成**方法学结论**而不是噪声："This counterintuitive finding - that longer simulations do not always translate into more accurate predictions - likely stems from several factors."；给出三个候选原因 "Atomistic force fields could show some limitations in reproducing protein-protein interactions correctly."、"Furthermore, longer simulations may drift from the true conformational ensemble or become trapped in local minima that are nearly optimal but not representative of the native binding state."；②承认这把标准化协议堵死了："This observed effect complicates the development of standardized protocols, as optimal simulation length appears to require empirical determination for each system type."；③反过来把结论工程化：**筛选就用便宜短模拟**——"From a practical standpoint, however, this has very important implications, because we have proven that short simulations are sufficient to reproduce experimental results qualitatively, and therefore can be used effectively in a screening process."，并回引前作协议 "It consisted of running 10 different simulations of 5 ns equilibrium dynamics."、"From the second half of these simulations, we extracted configurations every 100 ps and calculated the binding affinity as the average of the binding free energies obtained with MMPBSA."
   **代价（我们读出的，见第 6/7 节）**：0.57 这个"最好结果"与"窗口选择"是在**同一批 9 个点的数据上**挑出来的，没有留出验证集，也没有独立体系复现；同时正文/图注的 0.29 与 0.31 不一致，说明该数字未被逐位核对。

4. **难点：Rosetta 在同一批构象上完全不灵**。"Calculation based on the Rosetta force field, instead, produced results that did not correlate with the experimental data."；量化 "The correlation with experiments is indeed R 2 = 0.01 for the 20-50 ns set and R 2 = 0.02 for the 20-100 ns when we use the Rosetta energy function to calculate the binding energy"。
   **应对**：①做**公平对照**（同一批构象、同一采样区间），排除"是不是采样不同导致差异"；②观察时间序列给出机理解释："contrary to the calculation performed with the MMPBSA method, where transient trends may appear on time scales of about 10 ns, binding energies calculated with the Rosetta energy function never change significantly during the simulation, indicating that this calculation method is less sensitive to minor configurational variations."；③把 Rosetta 归入"effective potentials 类方法"并宣称 MM-PBSA 短模拟协议优于它："This method outperforms methodologies based on effective potentials (such as PRODIGY or Rosetta ), while remaining fast enough for rapid screening."
   **代价**：结论只在"亲和力跨度约 10 倍的抗体-肽体系"上成立（"Only calculations based on the Rosetta energy function are not sensitive enough in the binding affinity range explored in our systems."）；Rosetta 在此被当成打分器使用（不做 repack 搜索优化构象），与它在界面设计里的用法不是同一件事，本文未讨论这一差别（这是我们的判断，非作者原文）。

5. **难点：非平衡 PMF 的窗口间距第一轮就不够用**。"In the first iteration of the PMF calculation, we used a fixed 0.5 Å interval between every umbrella sampling windows along the reaction coordinate" → 失败现象 "However, this spacing proved to be insufficient in most cases, leading to abrupt transitions between the bound and the unbound states and insufficient sampling of intermediate configurations."
   **应对**：把窗口加密一半并明确写"最终"设置："Eventually, estimation of the PMF for each antibody was done by setting the window width to 0.3 Å, resulting in approximately 100 umbrella windows per system."、"For each window, a 2 ns simulation was carried on for a total of about 200 ns for each antibody"；起步构象用 SMD 拉出来（"Initial configurations for the umbrella sampling simulations were obtained using a nonequilibrium pulling simulation (steered MD Simulation)."）。
   **代价**：花了 200 ns/体系（合计 ~1.8 μs）仍然最差："The correlation between experiments and simulations in this case is R 2 = 0.19, notably lower than the results obtained with the MMPBSA method."。他们给出的解释是本体系特有的："Since the peptide interacts with the antibody via two hydrophobic residues, the two molecules separate abruptly under the external force, making the sampling of intermediate positions more difficult."，并强调体系依赖性："Indeed, PMF calculations based on umbrella sampling have shown high accuracy in other systems, but underperformed in our case."

6. **难点：MD 抽帧样本自相关 ⇒ 误差被低估**（端点法/WHAM 都靠帧平均）。原句："As configurations are extracted from molecular dynamics trajectories, the samples are autocorrelated, leading to an overestimation of the effective sample size and an underestimation of the true statistical uncertainty."
   **应对**："To address this issue, we used the PyMBAR Python library to analyze the statistical properties of each umbrella sampling window and estimate the number of effectively uncorrelated samples, which have been used to calculate averages and standard deviations."（只用于 umbrella 窗口）。
   **代价**：该修正只写在 PMF 一节，MM-PBSA 的每 100 ps 抽帧平均**没有**报告等价的自相关校正，所以 R²=0.57 的误差条并未同尺度处理（据正文；未取到的 SI 可能补充）。

7. **难点：早期绝对量级不真实（>10 kcal/mol）**。"However, the binding affinity difference calculated using the replica exchange is more realistic than in our previous estimation, having obtained a maximum ΔΔ G around 6 kcal/mol instead of unrealistic differences of more than 10 kcal/mol obtained in our earlier work."
   **应对**：①用增强采样压量级；②改用**归一化 ΔΔG**做跨方法比较（除以 WT 与最佳变体 Ab02 之差）："we consider the normalized value of the binding energy ΔΔ G by dividing it by the absolute value of the ΔΔ G between the WT and the Ab02, which is considered the best antibody from the experimental point of view"，并把 K_D 换成自由能再比："Experimental values were also normalized using the same approach, after converting dissociation constants K D into binding free energies"；③把"能不能分强弱"降级为可辩护的目标："Despite these important differences, we can observe how the different methods generally agree in discriminating between strong and very strong binding antibodies, with remarkable sensitivity, even if the experimental difference is relatively small (about 10-fold)."
   **代价**：**归一化的分母本身是实验最强者（Ab02）**，等于用被检验数据里的一个点定标；同时 6 kcal/mol 对 10 倍亲和力（约 1.4 kcal/mol）仍偏大一个量级，作者未再做尺度校准。

8. **难点：方法之间彼此也不一致，而且有系统性的判错**。"On the other hand, the correlation between different methods is generally low, the best agreement being observed between RE-MMPBSA and umbrella sampling"；对反例 Ab01："However, in disagreement with experiments, we observe that simulations almost always identify Ab01 as a worse antibody than the WT."
   **应对**：不裁决、并列两种解释并要求后续研究："On one hand, it could indicate a limitation of the computational methods, which failed to correctly sample the configuration space for these specific antibodies."、"On the other hand, experimental data are also affected by measurement errors, meaning these antibodies may not have been properly characterized in the experiments."；同时把"实验即真值"这一前提也放松："Even if we have treated experiments as the ground truth so far, we must recognize that experiments come with errors as well, and good leads may be lost in the process because of experimental uncertainties"。**本文未解决**：Ab01（以及被两法共同判为优于 WT 却与实验不符的 Ab10、Ab38）到底是谁错，没有做复测，也没法从本篇数据判定。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **采样端**：显式溶剂 MD（GROMACS 2023.2、Amber14SB、TIP3P、0.15 M KCl、PME、LINCS、2 fs、八面体盒边距 1.1 nm）；**T-REMD**（64 副本、300-380 K、每 2 ps 交换尝试、界面外 15 Å 原子谐波约束）；**非平衡**（steered MD 拉离 → umbrella sampling → WHAM 重建 PMF）。
- **打分端**：**MM-PBSA 单轨迹近似**（gmx_MMPBSA，ΔG = G_complex − (G_peptide + G_antibody)）；**Rosetta InterfaceAnalyzer**（score_jd2 预处理、ref2015、`-pack_input true`、`-pack_separated true` 取 dG_separated、`-compute_packstat true`）；PMF 的结合自由能取 bound 与 unbound 之差。
- **统计端**：PyMBAR 估"有效不相关样本数"用于 umbrella 的均值与标准差；跨方法比较用归一化 ΔΔG；与实验比较用 Pearson R²。
- **基准真值**：先前工作已表征的 9 个抗体（AbWT + 8 变体）的实验 K_D（约 10 倍跨度）。
- **没有用的方法**：FEP/TI 全转换自由能（本篇刻意用端点法与非平衡拉伸替代）、QM/MM、机器学习亲和力预测器（引言里作为"依赖训练集、单构象"的对照被点名）。**注意：本篇是打分器基准，不是候选生成管线。**

### A. 体系准备（Methods 5.2-5.4）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 抗体-肽复合物（只取抗体可变区 VH+VL，图注口径 "Only the variable part of the antibody (VH and VL region) is taken into consideration during the simulation."） | 命名归一：abN48→AbWT，abN48-2…-38→Ab02…Ab38 | — | **9 个体系**（WT + 8 变体） |
| A2 | 各体系 | 溶剂化 + 0.15 M KCl、中和、能量最小化 | 判据＝消除位阻与应力（原文："to prevent steric clashes and reduce structural strains within the system"） | 周期体系，八面体盒边距 1.1 nm |
| A3 | A2 | 两段短平衡：NVT 后 NPT，各带 α 碳位置约束 | 每段 **100 ps**；LINCS 约束氢键、步长 **2 fs** | 生产/REMD 起点 |
| A4 | A3 | T-REMD：64 副本 NPT × 100 ns，300-380 K，每 2 ps 尝试交换；水先最小化 + 300 K 10 ps 约束弛豫，再从 50 K 六步升温到 300 K | 界面判据＝距肽 **15 Å** 内为自由区，区外原子谐波约束力常数 **10 kJ/mol**（三向） | 每抗体 6.4 μs（64×100 ns）；9 个抗体合计 **57.6 μs** |

### B. 四种打分在同一批数据上的对比（Results 2.1、2.3；Methods 5.5-5.8）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | A4 的 300 K 副本轨迹 | 逐帧算 MM-PBSA（单轨迹近似，每 **100 ps** 取帧） | 收敛判据＝自由能前 20 ns 下降后进平台；据此**丢弃前 20 ns**；对比两个窗口 **20-50 ns** 与 **20-100 ns** | RE-MMPBSA ΔΔG 两套（Table 1）；最佳相关性 **R²=0.57**（20-50 ns） |
| B2 | 同一批构象 | 换能量函数：Rosetta score_jd2 → InterfaceAnalyzer（ref2015、`-pack_input true`、`-pack_separated true`、`-compute_packstat true`）取 dG_separated | 同 B1 的两窗口 | **R²=0.01 / 0.02**；时间序列无显著漂移 |
| B3 | A3 起点 | 非平衡拉离（SMD）：两 pull group 沿 z 轴加谐波势，pull group1=抗体骨架 60-100 位 13 个 α 碳、group2=肽 7 个 α 碳 | 力常数 **2000 kJ/mol·nm²**、拉伸速率 **2 nm/ns**、跑 **3 ns** | 每体系的反应坐标（两端质心距离）与"完全分离"构象 |
| B4 | B3 坐标 | umbrella sampling 分窗重跑再 WHAM 重建 PMF | **第一轮 0.5 Å 间距被判不足** → 改 **0.3 Å**、约 **100 窗**、每窗 **2 ns**（~200 ns/抗体，全套 ~1.8 μs）；bias K=2000 kJ/mol·nm² | **R²=0.19**；PMF 平台高低即结合强弱排序 |
| B5 | 四套 ΔΔG | 归一化后与实验 K_D 换算值（RT ln，300 K）逐点比 Pearson | 归一化分母＝WT 与 Ab02 之差 | 方法间相关性普遍低，最高 RE-MMPBSA vs umbrella **R²=0.47**（Table 1） |

### C. 结论的工程化（Discussion）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | B1 的两窗口对比 | 反直觉结果落地成协议选择 | 判据＝与实验的 Pearson R² 且必须"够便宜" | 推荐前作协议：10 × 5 ns 平衡模拟、取后半段每 100 ps 抽帧做 MM-PBSA（合计 50 ns/次） |
| C2 | 推荐协议 | 折算通量与成本 | 正文口径："with modern GPUs able to simulate ∼300 ns/day for systems of this size, the proposed protocol allows testing 3-5 antibodies per GPU per day." | 每 GPU 每天 **3-5** 个抗体；对比实验端"days to weeks" |
| C3 | 全篇方法结论 | 写下适用边界 | 判据＝体系依赖必须实测："The reliability of the different methods also appears to be system specific." | 结论：最优模拟长度需按体系经验标定；本文不做跨体系外推 |

## 4. 关键数字台账（全部来自本地全文）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 9 个抗体（WT + 8 变体），实验亲和力 ~10 倍跨度 | 基准集规模与分辨率 | "In addition to the wild-type antibody, we evaluate the binding of eight of its variants to the same target, covering approximately a 10-fold range in experimentally measured binding affinity." |
| 64 副本 × 100 ns；300-380 K；每 2 ps 交换尝试；合计 **57.6 μs**；单体系 **6.4 μs** | T-REMD 规模与单价 | "we performed 64 replicas of 100 ns simulations, with temperatures ranging from 300 to 380 K, resulting in a total simulated time of 57.6 μs"；"The temperature distribution ranged from 300 to 380 K, and an exchange trial between adjacent replicas was performed every 2 ps." |
| 丢弃前 **20 ns**；对比 **20-50** 与 **20-100 ns**；抽帧 **每 100 ps** | 收敛窗口与采样密度 | "Therefore, the first 20 ns were excluded in the calculation of the average binding free energies."；"configurations extracted from the T-REMD trajectories every 100 ps in the equilibrated portions of the simulations (20-50 ns or 20-100 ns)" |
| **R²=0.57**（20-50 ns）vs **R²=0.29**（20-100 ns，正文）/ **R²=0.31**（图注） | 同一方法、不同窗口的相关性反转 | "showed a higher correlation ( R 2 = 0.57) with the experiments than the prediction obtained with the full 20-100 ns interval ( R 2 = 0.29)"；图注句 "The correlation coefficients are R 2 = 0.31 and R 2 = 0.57, respectively." |
| **R²=0.01 / 0.02**（Rosetta） | 同批构象上 Rosetta 打分与实验无相关 | "The correlation with experiments is indeed R 2 = 0.01 for the 20-50 ns set and R 2 = 0.02 for the 20-100 ns when we use the Rosetta energy function to calculate the binding energy" |
| **R²=0.19**（PMF） | umbrella 非平衡法与实验相关性 | "The correlation between experiments and simulations in this case is R 2 = 0.19, notably lower than the results obtained with the MMPBSA method." |
| **R²=0.47** | 方法间最高一致性（RE-MMPBSA vs umbrella） | "the best agreement being observed between RE-MMPBSA and umbrella sampling" |
| umbrella 间距 **0.5 Å → 0.3 Å**；**~100 窗** × **2 ns** = **~200 ns/抗体**（全套 ~1.8 μs）；bias **2000 kJ/mol·nm²** | PMF 的失败修正与成本 | "this spacing proved to be insufficient in most cases, leading to abrupt transitions between the bound and the unbound states and insufficient sampling of intermediate configurations."；"setting the window width to 0.3 Å, resulting in approximately 100 umbrella windows per system" |
| SMD：**3 ns**、**2 nm/ns**、pull group 13 / 7 个 α 碳 | 拉伸起步设置 | "The MD simulation was run for 3 ns with a pulling rate of 2 nm/ns." |
| 最大 ΔΔG 从 **>10 kcal/mol** 降到 **~6 kcal/mol** | 增强采样后的量级修正 | "having obtained a maximum ΔΔ G around 6 kcal/mol instead of unrealistic differences of more than 10 kcal/mol obtained in our earlier work" |
| 界面判据 **15 Å**；约束力常数 **10 kJ/mol** | 只增强界面采样的做法 | "defined by all the residues within 15 Å of the peptide, were harmonically restrained at the starting position with a force constant of 10 kJ mol" |
| 前作对照协议：**10 × 5 ns**（50 ns/次）→ 同样拿到 R²=0.57 | "便宜版本"已达到同等（甚至更好）相关性 | "which required 50 ns (10 replicas of 5 ns simulations) for each calculation ( R 2 = 0.57)" |
| **~300 ns/day/GPU**；**3-5 抗体/GPU/天** | 成本折算 | "with modern GPUs able to simulate ∼300 ns/day for systems of this size, the proposed protocol allows testing 3-5 antibodies per GPU per day." |
| GROMACS 2023.2 / Amber14SB / TIP3P / 0.15 M KCl / NVT+NPT 各 100 ps / 2 fs / 盒边距 1.1 nm | 模拟引擎与力场口径 | "Simulations were conducted using the Gromacs 2023.2 package, using the Amber14SB force field and the TIP3P water model" |
| Rosetta：ref2015、dG_separated、score_jd2、InterfaceAnalyzer | 打分器实现细节 | "The standard ref2015 energy function was applied for scoring." |
| Table 1 数值范围（RE-MMPBSA 20-50：Ab38 −6.3 至 Ab03 +2.4 kcal/mol） | 8 个变体各方法的 ΔΔG | 正文表格（本卡不复述未逐字确认的单元格文本） |

## 5. 结论——作者说了什么

1. **同一批体系上，平衡 MM-PBSA 比非平衡 PMF 更贴合实验**："Contrary to some previous reports, we find that equilibrium molecular mechanics Poisson-Boltzmann surface area (MMPBSA) calculations yield better agreement with experimental binding affinities than nonequilibrium potential of mean force evaluations, underscoring the system-dependent performance of these methods."
2. **REMD 只带来有限改进、成本却显著上升**："We also observed a modest improvement in accuracy when MMPBSA is combined with replica exchange molecular dynamics, albeit at a significantly higher computational cost."
3. **Rosetta 力场打分在本体系不与实验相关**（见第 2.4 条引句）。
4. 他们把失败归因于两点体系特征："We attribute these findings to two factors, which could limit the applicability of some methodologies that are widely used in computing the binding energy: the high potency of the antibodies studied and the dominance of hydrophobic interactions between the antibodies and the peptide."
5. **定性排序可用**："This shows that MD-based methods are reliable tools for affinity screening of antibodies."（其证据形式是"各方法一致地把 Ab02/Ab29/Ab38/Ab10/Ab28 判为优于 WT"，与实验一致）
6. **筛选实践结论**：短模拟即可用，"careful empirical calibration of simulation length is required"；简单协议（多个短副本 + MM-PBSA）是精度与可行性的折中。
7. 自陈的总前提：准确性仍取决于构象系综采样，熵/柔性/溶剂贡献是难点（"This is due to the significant contributions of entropy, the intrinsic flexibility of proteins, and solvent effects."）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的真正可复用产物不是"MM-PBSA 更好"，而是"怎么测判据"的模板**：同一批构象、多个候选打分器、与外部真值逐点对比、并报告方法彼此的相关性。→ 对应我们缺的正是 B09 那篇 A 段的等价物：**把判据放上考卷**，而且 Z08 展示了"考卷可以同时给多个判据打分、包括给自家方法打低分"。
2. **"窗口/长度要选"这一步必须在独立数据上做**。本文把 20-50 ns 选出来当最好结果，但没有留出体系或留出验证，等于在同一批 9 个点上做一次带自由度的选择。→ 我们若用 MD 打分，必须预先固定"取哪段轨迹、多少个副本、多少帧"，或至少把窗口选择放到与测试不同的体系上做；否则相关性数字不可比、不可信。
3. **他们承认并量化了"误差被低估"这一坑（自相关）**，却只在 PMF 一侧修正 → 我们的 MD 端点法读数应默认带 block-average / 有效样本数校正，并把这一项写进成本，否则"置信区间"没意义。
4. **归一化用被检验数据里的最强点做分母**，这是把标尺钉在自己要测的对象上——我们做"候选 vs 已知"的归一化分数时要避免同一结构（与 B09 第 6.2 条"同一指标既当召回又当证据"同源）。
5. **本文给出的"3-5 抗体/GPU/天"是亲和力打分的通量单价，不是酶活筛选的单价**；但它证明了一件对我们有用的事：当判据的通过率与单价同时被报出来时，选择"哪个判据进漏斗"变成可决策问题，而不是信仰问题。
6. **他们对 Ab01 反例不做裁决，只把两种可能并列**，这是诚实但也意味着这篇无法用于"校准失败概率"；引用时只可引用方法结构，不可引用任何命中率。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者自述：①"The reliability of the different methods also appears to be system specific."，明确不做跨体系外推；②最优模拟长度需按体系经验标定；③MMPBSA 方差大；④PMF 在本体系欠采样中间态（疏水"突然断裂"）；⑤实验数据本身可能有测量误差；⑥对 Ab01/Ab10/Ab38 的矛盾无结论；⑦REMD 成本显著更高但只换来"modest improvement"。
- 我们读出：①**n=9（有效比较点 8）**，两个 Pearson R² 之差（0.57 vs 0.29/0.31）在这种样本量下几乎肯定不显著，正文也没给区间或检验；②正文与图注的 0.29/0.31 不一致，说明数值一致性未被复核；③四个方法只在**一个体系、一个窄亲和力区间（约 10 倍）**上比较，而筛选真实使用时要区分的是更宽/更弱的结合，判据在此区间"够不够灵敏"未被测（Rosetta 被判定"不敏感"恰是因为跨度太窄——作者自己写了 "not sensitive enough in the binding affinity range explored in our systems"）；④"ground truth"是前人实验 K_D，本篇未复测，且未给测量误差；⑤约束界面外原子、只用 VH/VL、丢弃前 20 ns、帧间隔 100 ps 这些选择叠加后，方法之间并非完全公平；⑥自相关校正只用于 umbrella，MM-PBSA 的 R² 没有同尺度的不确定性表达；⑦没有 FEP/TI 作对照（该组自己的主力打分器），因此本篇不能被引用为"物理方法排序比较已完备"。

## 8. 对 UAA 筛选的迁移判断

**先划边界（本卡的强制性提醒）**：Z08 检验的是**抗体-肽结合亲和力**的排序能力（ΔG/ΔΔG、K_D 换算），全部判据都是**静态/平衡结合热力学**，读出是"谁比谁绑得紧"。它**不涉及化学键生成、不涉及转换数、不涉及竞争性副产物**。因此：**R²=0.57 不能被引用为"MD/MM-PBSA 能预测酶活"的证据；同理，周组在抗原-HLA（Z04）或适配体-蛋白（Z01/Z02）上的 FEP 命中率，也不能当成 UAA 合成酶催化能力的判据或成功概率。** 酶活判据必须另有考卷（真值面板里有"产物是否生成"的化学标签），本文只提供测法不提供数字。

**可迁移（怎么用）**

1. **"多判据同卷考试"的做法**：固定同一批构象与同一份真值，把 N 个候选打分器（端点法 / 增强采样 / 有效势 / 非平衡 / ML）一起跑，报①各自与真值的 R² ②方法彼此的相关性。→ 我们的判据面板应照此设计：Foldseek 命中、催化几何 RMSD、口袋能量、xTB 能垒、MM-GBSA……全部在同一真值面板上考试，并**报方法间一致性**（这能暴露"多个判据其实是同一个信号"的伪独立）。
2. **"通过率 ÷ 单价"要有单价数字**：本篇给出 ~300 ns/day/GPU、3-5 抗体/GPU/天、RE-MMPBSA 6.4 μs/次 vs 50 ns/次的对比。→ 我们每个判据必须挂上核时单价（本项目实测：MD 156.6 ns/day、新体系 10.6 GPU·h、xTB 271 原子 153.3 s/评价），才能决定进不进漏斗。
3. **先定"取哪段轨迹、多少帧、多少副本"再打分**，并把自相关/有效样本数校正作为强制项（PyMBAR 那条）。→ 直接照搬：我们所有 MD 端点法读数都配 block-average 有效样本数，且窗口选择在预注册里写死。
4. **"体系依赖"要写成显式限制**，而不是把 R² 当常数搬走。→ 我们引用任何外部判据性能时，注明"该数字只在 X 体系、Y 动态范围内成立"。
5. **反例不做裁决时就不许报命中率**。本篇不报"命中率"，只报相关性与定性排序——这是我们对 UAA 候选"未做化学确认前"应当采取的表述姿势。
6. **"便宜的短模拟"这一思路可用于我们预算分配**：把昂贵方法（长时 MD/QM）限制在少量复核候选上，粗筛用便宜协议；但**必须像本文一样先证明便宜版与贵版在同一考卷上排序一致**（本文其实没做到：便宜版 R²=0.57 与贵版 20-50 ns 的 0.57 是不同采样的巧合性巧合，他们只写了"correlates as well"）。

**不可迁移（为什么不能照搬）**

1. **判据对象不同**：R² 建立在"K_D 换算的自由能"上；UAA 的靶标问题是"三条化学事件是否发生 + 副产物分支"。静态结合的排序好，不等于反应能垒的排序好；把 MM-PBSA 分数当催化闸口属于误用。
2. **动态范围只有 ~10 倍**：筛选场景需要区分的是 >3 个数量级或"有无活性"。本文自己的结论正是"跨度小时 Rosetta 失效"，这反向说明：**用它校准我们的判据灵敏度时，必须先把我们判据的可用动态范围测出来**，不能直接借用 R²。
3. **无 FEP/TI、无 QM/MM**：本篇不能为"用 QM 判催化能否发生"提供任何证据（无论支持或反驳）。
4. **体系只有 1 个、只有 9 个数据点**：不足以支撑"某法在某类问题上表现 X"的全称结论；引用它时只能说"这一组作者在这一对抗体-肽体系上做了这个比较"。
5. **他们没有生成端**：从"候选构象从哪来"这一步开始就是本文之外的问题。我们的困难一半在候选生成（活性位点构型从哪来），Z08 对这一半没有任何说法。

## 9. 溯源与自检

- 引句底稿: data/literature_cards/fulltext/Z08_PMC12613313_text.txt（本卡全部英文引句均从这一份逐字复制；同源 XML `Z08_PMC12613313_fullTextXML.xml` 与登记底稿 `sources/zhou.md` 见 `sources_map.json`，门禁不把 .xml 当可读底稿）。
- 归一化说明：本地纯文本由 Europe PMC fullTextXML 去标签得到（HTML 实体解码、引号/破折号统一、空白折叠）；上标/下标（R 2、Δ Δ G、μ s、φ-ψ）在原 XML 是标签，去标签后留下带空格的形态，本卡引句按该形态原样抄写，未做"美化"。
- 阅读定位方式：先把归一化单行全文按句切到临时文件（`A:\AITEMP\Z08.sent.txt`，478 句）再分段精读；正文内容集中在句 4–225，其后为参考文献；Methods（第 5 节）全部在句 173–212 之间，本卡第 3 节阈值均出自该段。
- 对照底稿行号：`sources/zhou.md:110-119`（原卡）；`sources/zhou.md:180`（QM 取证：全组 2019–2026 设计管线无一篇以 DFT/QM-MM 作准入判据，筛选器全为 MM/GBSA、MM/PBSA、FEP、FEP/HREX、SMD-PMF，后者在 Z08 被自有数据否决）；`sources/zhou.md:211`（演进链③）；`sources/zhou.md:230`（原列为未核验细节的方法相关系数，本卡已补齐）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字/是否用MD`；第 4 节 ↔ `候选数递减/成本统计`；第 7-8 节 ↔ `实验命中率/Kd或活性最好值/在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only Z08 --no-report` 把卡内所有不含中日韩字符、被直双引号包住的 ≥20 字符片段，在"引句底稿"指向的全文里逐字查找；任何一条不命中即 FAIL、退出码 1。本轮结果见交付回报。
- 一处需要下游注意的**原文内部不一致**：正文写 20-100 ns 的 R² 为 0.29，图 1 图注写 0.31，Discussion 又用 0.31 与 PMF 0.19 并列。本卡两个数字都按原句列出，未择一。

<!--CSV回填
work_type=论文（方法校准/打分器基准；不生成新候选、无设计端）
target=抗 CXCR2 抗体（AbWT，原 abN48）及其 8 个点突变变体，结合 CXCR2 N 端肽（GPCR N 端段）；共 9 个复合物体系
backbone_generation=无候选生成；仅取先前已实验表征的 9 个抗体-肽复合物做打分基准（模拟只包含抗体可变区 VH+VL）
computational_filters=四把尺同卷对比：①T-REMD(64 副本 300-380K)+MM-PBSA 单轨迹(RE-MMPBSA)；②常规 MD+MM-PBSA(前作协议 10×5 ns)；③同批构象上的 Rosetta ref2015 InterfaceAnalyzer dG_separated；④非平衡 PMF（steered MD 起步 + umbrella sampling + WHAM）；统计端 PyMBAR 估有效不相关样本数、跨方法用归一化 ΔΔG、与实验 K_D 换算的 ΔΔG_exp 比 Pearson R²
thresholds=丢弃前 20 ns（自由能达平台 + REMD 交换配平）；对比窗口 20-50 ns 与 20-100 ns；抽帧每 100 ps；界面外 15 Å 原子谐波约束 10 kJ/mol；盒边距 1.1 nm、0.15 M KCl、2 fs、NVT/NPT 各 100 ps；umbrella 窗距 0.5 Å 判不足→0.3 Å（约 100 窗 × 2 ns）；SMD 力常数 2000 kJ/mol·nm²、速率 2 nm/ns、3 ns；判据本身只用 Pearson R²，无准入阈值
md_used=是（全文核心就是 MD：显式溶剂平衡 MD、T-REMD 增强采样、steered MD + umbrella 非平衡拉伸；打分器 MM-PBSA/Rosetta/PMF 都跑在 MD 构象上）
qm_used=否
experimental_methods=无新实验；实验端全部取先前已发表的抗体变体亲和力（K_D），在 300 K 下用 RT ln 关系换算为 ΔΔG_exp 作真值
pipeline_counts=9 个抗体（WT+8 变体）× 4 套方法（+前作短模拟共 5 套 ΔΔG）；REMD 每抗体 64×100 ns=6.4 μs、总计 57.6 μs；PMF 每抗体约 100 窗 × 2 ns≈200 ns、全套约 1.8 μs；Table 1 列 8 个变体 × 6 组 ΔΔG 值
hit_rate=不报命中率（无候选筛选环节）；报相关性与排序一致性：RE-MMPBSA 20-50 ns R²=0.57 最佳、20-100 ns 降到 0.29（正文）/0.31（图注）、非平衡 PMF R²=0.19、Rosetta R²=0.01-0.02；方法间最高一致 RE-MMPBSA vs umbrella R²=0.47；定性层面各法一致把 Ab02/Ab29/Ab38/Ab10/Ab28 判为优于 WT，但几乎总把 Ab01 判为劣于 WT（与实验相左，未裁决）
best_metric=未记录（本篇不做亲和力改进、无最优 K_d；只报最大 ΔΔG 量级由早期 >10 kcal/mol 修正为约 6 kcal/mol，以及各方法与实验的 R²）
cost_or_stat_note=体系规模下现代 GPU 约 300 ns/day；推荐筛选协议（10×5 ns + MM-PBSA）每 GPU 每天可测 3-5 个抗体，vs 实验端"数天到数周"；RE-MMPBSA 单价 6.4 μs/亲和力、PMF 200 ns/亲和力；计算成本显著低于实验平台（无需耗材）；未给标准差/显著性检验，n=9（有效比较点 8）
role_in_timeline=周如鸿组漏斗的"筛选器自检"环节（2025）：把组内实际在用的物理打分器（MM/GBSA-MC 粗筛如 ANUBI、FEP 精排如 Z03/Z05/Z09、以及自家曾用的 SMD-PMF 路线）放在同一批抗体-肽体系上与实验真值对表，给出"平衡端点法优于非平衡 PMF、Rosetta 类有效势在此类窄动态范围不灵、更长轨迹不一定更准、便宜短模拟够用于筛选"四条工程结论，同时把体系依赖与采样长度需经验标定写成显式限制
source_pointer=data/literature_cards/fulltext/Z08_PMC12613313_text.txt（SHA a1cb212dacac1914…）+ Z08_PMC12613313_fullTextXML.xml；sources/zhou.md:110-119、180、211、230
CSV回填-->
