# [B26] 用设计实验的失败数据回炉能量函数——从 DMS 救援突变到 beta_jan25：闭环"实验→打分器"的样本论文

Haddox H, Rocklin G, Motta F, Strickland D, Halabiya S, Cordray C, Park H, Klavins E, Baker D, DiMaio F（华盛顿大学 IPD / HHMI 等）
PLOS Computational Biology 2026, 22(4): e1014215 · DOI 10.1371/journal.pcbi.1014215 · PMID 42018576 · PMCID PMC13124059（CC BY 4.0）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B26**（组：Baker组） |
| 本地全文 | `data/interim/baker_lit/ft/energyfunc2026.txt`（118,211 B，2026-10-16 抓取；batches.tsv 第 8 批，state=FULLTEXT） |
| 对照底稿 | `sources/baker.md` 第 342–353 行（原卡）；汇总引用见 `sources/baker.md:613/648/660` |
| 登记底稿清单 | `sources_map.json` 键 B26：上述全文 + `sources/baker.md`；本卡全部英文引句在全文里逐字命中（门禁 `--only B26`） |
| 证据级别 | **全文级** |
| 未取到的部分 | 补充图（S1–S9）、S1/S2 Table 全表、以及 Zenodo/GitHub 数据本体（正文只给指针）。凡涉及处本卡注明"正文口径" |

## 1. 这篇到底解决什么（大白话）

Rosetta 这类物理能量函数的训练数据（小分子热力学、高分辨晶体、突变效应）太少太窄，"available training data are limited in number and diversity, prompting a need for new sources of training data"（作者概述口径）。这篇提出新范式：**让能量函数自己设计蛋白，把湿实验的成败拿回来当"体检报告"**——具体是 Rocklin 2017 数千条 miniprotein 的高通量蛋白水解稳定性数据中，"能量函数判它稳、实验判它不稳"的 21 个离群设计；对它们做全单突变的深度突变扫描（DMS），看哪些点突变能"救援"，从救援模式反推能量函数的失效模式（核心立体冲突/过堆积），再把这个失效模式拿到既有高质量基准（晶体结构 relax 的原子对距离分布）上放大权重、重拟 15 个 LJ 参数，产出 beta_jan25。全程无 MD、无 QM；是"用设计结果反馈打分器"闭环的方法论样本。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **直接拟合设计数据，泛化不了**。"initial experiments showed difficulty in getting this fitting to generalize to unseen data. Therefore, we pivoted to using an indirect learning approach"——放弃"把 DMS 数据直接进 dualOptE 拟合"的初始方案（Fig 1 上轨），改走三步间接学习："i) using the experimental data to identify a common failure mode in design, ii) identifying examples of this failure mode in a high-quality benchmark, and iii) using this benchmark and others to reparameterize the energy function"。**代价**：学到的不是设计数据本身，而是经由既有基准的放大——只适用于"失效模式恰好已在某基准里有弱信号"的情形。
2. **能量函数预判稳定、实验不稳的设计怎么办（离群者选择）**。Rosetta 对这些设计"has a limited ability to predict the stability of these designs"；他们不是丢弃离群点，而是专挑它们：先用特征+随机森林预测稳定性，把"模型预测稳（stability score > 1）但实测不稳（score < 0.3、EC 50 < 1.5、CI < 2）"的 21 个设计拉出来做 DMS（"We identified 21 outlier designs that were unstable according to the high-throughput stability assay from Rocklin et al. (stability score < 0.3, EC 50 < 1.5, and an EC 50 95% confidence interval < 2), but were predicted by the random-forest model to have a stability score > 1."）。**应对背后的假设**："The outlier designs tended to have much more favorable Rosetta energies than other unstable designs"、"We hypothesized that each of these designs are adjacent in sequence space to a highly stable sequence."——假设后被 DMS 部分证实（多数设计确有救援突变）。**遗留**：作者明写泛化边界存疑（"It is unclear whether most of the unstable miniprotein designs from Rocklin et al. would have been rescued by single mutations"，后半句含原文引号词故未整句引用，见 Discussion 第 5 段）。
3. **稀有信号 vs 噪声**。全库 ~16,000 单突变里高稳定化救援只约 1%："Across all outlier designs, ~ 1% of mutations (156 out of ~16,000 mutations tested) were highly stabilizing (Δ stability score > 1.0)"。→ **应对**：三重抗噪设计——19/21 设计做生物学重复（"We also performed biological replicates of the entire experiment for 19 of the 21 outlier designs"）；库内混入 338 个 Rocklin 蛋白对照跨研究复现性；两种蛋白酶×六个浓度各自定 EC 50、取最小值聚合。作者对模式真实性的判据是收敛性而非单点显著性："Although some of these large effects may be due to noise, many rescue mutations involved similar biophysical changes, suggesting a real effect."
4. **突变读出本身的动态范围不够**。→ **应对**：换更强蛋白水解耐受展示载体——"We used an updated version of the high-throughput stability assay described in Maguire et al."，"which involves using a more protease-resistant yeast-display vector that expands the dynamic range of the assay"；结果"the stability scores were correlated between studies, though our measurements spanned a larger dynamic range due to the updated yeast-display vector"。
5. **"设计里的冲突是不是真实物理缺陷"存疑**。DMS 推出冲突假设后，先做两步自证：其一，设计模型 vs 同一设计的晶体结构对比——"This number was always lower in the crystal structure compared to the design model, with crystal structures having ~30% fewer clashing atom pairs on average"，且"we found that many clashes were relieved through minor backbone rearrangements. However, some were relieved through much larger rearrangements that substantially altered the design's shape"；其二，意外发现提示冲突并非只属于失败设计："To our surprise, both stable and unstable miniprotein designs had similarly elevated levels of clashing, suggesting it is a general feature of the designs."→ 应对=接受"这是能量函数的一般性偏差而非个案"，全文聚焦此模式。
6. **失效模式在训练基准里信号太弱**。"the signal was relatively weak overall as the differences were fairly subtle and only affected about 10 out of 118 atom-pair distributions"（54 个训练外晶体结构的原子对距离分布基准上，beta_nov16 relax 后引入冲突）。→ **应对**：不造新基准，而是把既有原子对基准在 dualoptE 损失中加权 10 倍——"We increased the weight of the atom-pair distance-distribution benchmark by 10-fold."（并解释平衡性：beta_nov16 该基准未加权得分本来就约低 10 倍），只重拟 15 个参数（"We refit a total of 15 parameters."，含 fa_rep 与 C/H 的 LJ 半径/势阱深度，"In general, the refit parameters caused the energy function to become more repulsive"）；automated 拟合后再手工微调半径。结果："The bias was largely eliminated."但"The refitting did not completely eliminate the clashing bias."
7. **分布式志愿计算（Rosetta@home）的随机失败**。为跑数千 decoy×多 relax 协议用了志愿计算——"While useful, some of the relax protocols that we submitted stochastically failed, which is expected for this type of platform, resulting in dropout."→ **应对**：两级 QC 过滤+剔除规则：重复能量一致性（"We discarded the output data if the minimum and median energies among all replicates of either the complex, chain-A, or chain-B jobs differed by >0.1 energy units per residue."）与单链能量相对全体中位数离群（>0.1 单位/残基）；单结构 decoy 丢失 >15% 则弃该结构、中位 decoy 数 <1,000 亦弃（"This number was < 1,000 for 3 of the 62 crystal structures, which we excluded from our analysis due to high dropout."）。最终 "We ultimately obtained ΔG estimates for both beta_nov16 and beta_jan25 for a median of 5,629 decoys per crystal structure and an interquartile range of 3,642–7,204 decoys."（验证集 62 结构、排除 3 后按 59 个界面平均——这就是正文里 59/62 两个数并存的原因，见第 7 节）。
8. **第二个失效模式：假说被自己的实验否定**。预期 beta_jan25 会更偏好晶体结构（"Since crystal structures of designs have fewer clashes than corresponding design models, we hypothesized that beta_jan25 would have a greater energetic preference for the crystal structures."），实测两版函数都仍以约 0.1 kcal/mol/残基偏好设计模型（"Interestingly, both energy functions tended to strongly prefer designs over crystals, both doing so by an average of ~0.1 kcal/mol per residue"）。→ **应对（本文内的处理=记录不修复）**：分解发现驱动项是静电+氢键（"we found that it was driven by terms modeling electrostatic interactions and hydrogen bonding, and to a lesser extent by terms modeling LJ interactions"），提出这是第二种失效模式（极性或相互作用被高估），但"We do not attempt to address this potential failure mode, but highlight it to help guide future energy-function development."——**本文未解决**。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **实验**：酵母表面展示 + 蛋白酶消化 + FACS + 深测序的高通量稳定性实验（Rocklin/Maguire 版，更新载体扩动态范围）；两蛋白酶×六浓度 EC 50→stability score（log ratio：观测 EC 50 / 变性态预测 EC 50）。
- **计算诊断**：随机森林回归（特征=生物物理描述符含 Rosetta 能量）找离群设计；Rosetta FastRelax（Cartesian，beta_nov16）处理设计-晶体对；冲突计数=原子间距小于范德华半径和。
- **再训练**：dualOptE/dualoptE（ML 启发式搜参最大化基准组合得分），15 参数、基准加权 10×、手工微调→beta_jan25。
- **验证基准**：原子对距离分布（78 训练/54 验证晶体，KL 散度）；界面预测（训练 65/验证 62；每晶体 1,000 原生 decoy + 抖动扩充到 5,000，Boltzmann 判别分）；单体/界面 ΔΔG 分类（Frenz 平衡集 768→735；SKEMPI 6,185→633）；McNemar 与 1,000 次随机化检验。
- **没有用的方法**：MD 与 QM 全程未参与（OPLS 仅出现在参考文献标题；FastRelax 是能量极小化不是动力学）。

### 工作流程表

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| E1 | 三个既有数据集 | 汇集：Rocklin 数千 miniprotein 稳定性（"which used Rosetta to computationally design thousands of miniproteins (soluble proteins, ~ 40 amino acids in length), and then experimentally estimated the stability of each design using a high-throughput assay that quantifies the sensitivity of miniproteins to proteolysis"；"Designs spanned a wide range of stabilities with hundreds of both successful (stable) and failed (unstable) designs."）+ 新 DMS + 晶体集（"A third dataset involves 17 crystal structures of Rosetta designs, which we compiled across several studies and which span several protein folds and design methodologies"） | 无 | 学习原料池 |
| E2 | Rocklin 全库 | 扩展特征管线 + 逐拓扑随机森林预测 stability score | "We identified 21 outlier designs that were unstable according to the high-throughput stability assay from Rocklin et al. (stability score < 0.3, EC 50 < 1.5, and an EC 50 95% confidence interval < 2), but were predicted by the random-forest model to have a stability score > 1." | 21 个离群设计（HHH/EHEE/EEHEE 三拓扑） |
| E3 | 21 设计 | 全单突变 DMS 库（寡核苷酸饱和突变，装成 2 个大库："As described in the Methods , the 21 DMS libraries were ordered and tested as part of two larger libraries."）；展示-消化-FACS-深测；2 蛋白酶×6 浓度；19/21 生物学重复；库内 338 对照 | 聚合=两蛋白酶取最小 stability score；救援定义 Δ stability score > 1.0 | "Across all outlier designs, ~ 1% of mutations (156 out of ~16,000 mutations tested) were highly stabilizing (Δ stability score > 1.0)" |
| E4 | 救援突变表 | 生物物理归类 | 三类模式：极性→非极性（核心边界，"The most common pattern of rescue mutations involved changing a polar amino acid to a nonpolar one"，且"This class of rescue mutations suggests that the design protocol underweighted the hydrophobic effect, either due to Rosetta's energy function or the layer-based sampling procedure used to limit hydrophobic surface content"）；小→大（核心堆积）；大→小（"which all involve mutating either a valine or isoleucine in the protein core to either an alanine or glycine"）——"Closer inspection of these mutations revealed that the designed sidechains are predicted to sterically clash with neighboring sidechains in the Rosetta structural models." | 失效模式假设：能量函数低估立体冲突代价（"suggesting that large-to-small mutations might be stabilizing because they relieve energetically unfavorable clashes in the computationally designed structure"——此句在图注口径内，正文对应表述见第 2.5 节引句） |
| E5 | 设计模型 vs 晶体（17 对） | 设计模型先用 beta_nov16 在笛卡尔空间 FastRelax（"The first way we compared design-crystal pairs was by analyzing their levels of clashing. To do so, we first used Rosetta's FastRelax protocol to relax each design model in Cartesian space using the beta_nov16 energy function"；给函数"解冲突自由度"以从严检验），再数冲突原子对 | 冲突=距离短于范德华半径和 | "This number was always lower in the crystal structure compared to the design model, with crystal structures having ~30% fewer clashing atom pairs on average"；结论候选"Thus, clashes in designs may be one factor that causes crystal structures to differ from corresponding design models, interfering with accurate protein design." |
| E6 | 高分辨晶体基准（54 withheld / 78 总集） | relax 前后原子对距离分布 KL 散度 | "We used a set of 54 structures withheld from training to evaluate its performance."；beta_nov16 relax 后 "structures relaxed with the beta_nov16 energy function had elevated levels of clashing for several atom pairs, most of which involved at least one carbon atom from a nonpolar sidechain"；信号弱="the signal was relatively weak overall as the differences were fairly subtle and only affected about 10 out of 118 atom-pair distributions" | 失效模式在既有基准上的可测信号 |
| E7 | beta_nov16 参数组 | dualoptE 重训：同套基准 + 原子对基准加权 10×；只拟 15 参数（fa_rep、C/H LJ 半径与势阱；脂肪碳 LJ 参数由耦合改解耦）；跑完人工微调 | "We used dualoptE to retrain the energy function, using the same set of benchmarks used to train beta_nov16, but upweighting the contribution of the atom-pair distribution benchmark to the dualoptE loss function to amplify signal related to the clashing bias."；"We refit a total of 15 parameters."；"In general, the refit parameters caused the energy function to become more repulsive" | "We call the resulting energy function beta_jan25." |
| E8 | beta_jan25 | 多基准验证：原子对 KL（0.022→0.018，随机化检验 p = 0.002 口径）；界面预测（0.64→0.67，"The interface-prediction benchmark was used in training, but we tested the energy functions using a set of 59 structures withheld from training."）；ΔΔG 分类保持（0.55/0.55；0.64/0.66，McNemar 不显著 p = 0.78/0.50；"These tests involved a total of 735 mutations for monomers and 633 mutations for interfaces."）；重设计对照（"We saw similar results when we re-designed high-resolution crystal structures, rather than relaxing them, though clashing is more pronounced in design for both energy functions"；"We did not find evidence that the increased repulsion in beta_jan25 results in underpacking in design."→"we saw low levels of residual overpacking."） | 判据：降 clashing 且不伤其他基准 | "The bias was largely eliminated."；"The refitting did not completely eliminate the clashing bias." |
| E9 | 能量偏好实验 | 设计模型与晶体分别 relax（6 重复取最低能）后比分项能量 | 假说：beta_jan25 应更偏好晶体 | "Interestingly, both energy functions tended to strongly prefer designs over crystals, both doing so by an average of ~0.1 kcal/mol per residue"→假说不成立，登记为第二种失效模式（静电/氢键项偏强），"We do not attempt to address this potential failure mode, but highlight it to help guide future energy-function development." |

**流程骨架**：失败数据→（间接）失效模式→（放大）既有基准弱信号→（小参数面）重拟→（多基准护栏）验证→（未解决项）显式登记。它示范的是"实验回炉打分器"的最小完备闭环，而不是"把能量函数修好"。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| ~40 aa / 数千 / 数百成败 | Rocklin 数据集规模 | "which used Rosetta to computationally design thousands of miniproteins (soluble proteins, ~ 40 amino acids in length), and then experimentally estimated the stability of each design using a high-throughput assay that quantifies the sensitivity of miniproteins to proteolysis" |
| 17 | Rosetta 设计晶体结构对 | "A third dataset involves 17 crystal structures of Rosetta designs, which we compiled across several studies and which span several protein folds and design methodologies" |
| 21 / 3 拓扑 | DMS 离群设计数 | "we used deep mutational scanning (DMS) to experimentally measure the effects of all single amino-acid mutations on the stability of 21 outlier designs spanning three miniprotein topologies" |
| <0.3 / <1.5 / <2 / >1 | 离群判定四阈值 | "We identified 21 outlier designs that were unstable according to the high-throughput stability assay from Rocklin et al. (stability score < 0.3, EC 50 < 1.5, and an EC 50 95% confidence interval < 2), but were predicted by the random-forest model to have a stability score > 1." |
| 2 蛋白酶 × 6 浓度 | EC 50 测定条件 | "We independently performed the selection step with two different proteases and six increasing concentrations of protease, allowing us to estimate an EC 50 for each variant to each protease." |
| 19 / 21；2 大库；338 对照 | 重复与库组织 | "We also performed biological replicates of the entire experiment for 19 of the 21 outlier designs"；"As described in the Methods , the 21 DMS libraries were ordered and tested as part of two larger libraries." |
| ~1%；156 / ~16,000；>1.0 | 救援突变率与定义 | "Across all outlier designs, ~ 1% of mutations (156 out of ~16,000 mutations tested) were highly stabilizing (Δ stability score > 1.0)" |
| ~30% | 晶体比设计模型少的冲突对 | "This number was always lower in the crystal structure compared to the design model, with crystal structures having ~30% fewer clashing atom pairs on average" |
| 54 / 78；10/118 | 验证/训练晶体数；受影响原子对 | "We used a set of 54 structures withheld from training to evaluate its performance."；"the signal was relatively weak overall as the differences were fairly subtle and only affected about 10 out of 118 atom-pair distributions" |
| 15 参数；fa_rep；×10 权重 | 重拟范围与放大 | "We refit a total of 15 parameters."；"One controls the strength of the repulsive regime of the LJ potential (fa_rep). The others control the LJ radii and well depths of carbon and hydrogen atom types involved in the clashing problem."；"We increased the weight of the atom-pair distance-distribution benchmark by 10-fold." |
| 65 训练 / 62 验证 / 59 | 界面基准结构计数（62 中 3 个 dropout 剔除后按 59 平均） | "We trained the beta_jan25 energy function using a set of 65 crystal structures, and then validated its performance using 62 crystal structures withheld from training."；"The interface-prediction benchmark was used in training, but we tested the energy functions using a set of 59 structures withheld from training."；"This number was < 1,000 for 3 of the 62 crystal structures, which we excluded from our analysis due to high dropout." |
| 0–2 Å / 0–10° / 5,000 | decoy 抖动与规模 | "each jitter involved rigidly translating the chain between 0–2 Angstroms in a random direction in 3D space, coupled with rigidly rotating the chain between 0–10 degrees about a random axis"；"This resulted in a total of 5,000 decoys per crystal structure." |
| 5,629（IQR 3,642–7,204）；>0.1/残基 | 分析用 decoy 中位数与 QC 阈值 | "We ultimately obtained ΔG estimates for both beta_nov16 and beta_jan25 for a median of 5,629 decoys per crystal structure and an interquartile range of 3,642–7,204 decoys."；"We discarded the output data if the minimum and median energies among all replicates of either the complex, chain-A, or chain-B jobs differed by >0.1 energy units per residue." |
| 0.022→0.018；0.64→0.67 | 原子对 KL 与界面判别分（beta_nov16→beta_jan25，Table 1） | "Boltzmann-weighted probability of observing near-native structures in the protein-protein interface prediction benchmark, averaged across all 59 interfaces in the benchmark."（数值本身见 Table 1 行） |
| 735 / 633；768 / 6,185 | ΔΔG 测试突变数与来源库 | "These tests involved a total of 735 mutations for monomers and 633 mutations for interfaces."；"We obtained estimated mutational effects for 735 mutations for each energy function, a small number of input PDBs having been incompatible with our pipeline."；"We downsampled the 6,185 mutations with data to a set of 633 mutations split roughly evenly between four mutational categories" |
| p = 0.002 / p < 0.001 / p ≤ 0.001 | 显著性（随机化检验） | "None of the differences in average score from the null distribution were greater than or equal to the observed difference in average score, indicating the observed difference is significantly greater than zero with p ≤ 0.001." |
| ~0.1 kcal/mol/残基；5.1 kcal/mol 例 | 未解决偏好量级 | "Interestingly, both energy functions tended to strongly prefer designs over crystals, both doing so by an average of ~0.1 kcal/mol per residue"；例证见 Fig 5B 图注（K22/E220 静电差 5.1 kcal/mol） |

## 5. 结论——作者说了什么

1. 确立"从设计学习"的范式：设计给能量函数最大自由度暴露自身缺陷，实验失败模式可诊断函数不准处——"When designs are experimentally tested, common failure modes can suggest underlying inaccuracies in the energy function."；本文交付更新后的 beta_jan25（并入 Rosetta 发行，flag 可调）。
2. DMS 可以打在"几乎无折叠稳定性"的设计上而非天然功能蛋白："Most DMS experiments are performed on proteins that are already functional. Our DMS experiments were performed on protein designs with little-to-no initial folding stability according to the high-throughput stability assay."，且救援突变的收敛模式提示了多个失效模式。
3. 识别并"基本消除"clashing/过堆积偏差：经由高质量基准 + 10× 加权 + 15 参数重拟，其他基准不降反微升（界面预测显著改善，ΔΔG 分类持平）。
4. 首次系统比较大批设计模型与对应晶体寻找共性失败模式："this is the first study that systematically examined a large and diverse set of design models and corresponding crystal structures in search of common failure modes driving structural differences"。
5. 直接拟合走不通、间接放大可行，且此思路可外推到任何设计用模型（"This general approach of indirectly learning from designs could be applied to any macromolecular model used in design, including deep-learning models."）。
6. 自限：残留 clashing 未清零（"Despite this improvement, the problem persists at a low level for some atom pairs."）；第二失效模式（极性吸引被高估）只登记不处理；多数不稳设计能否单点救援仍是未知数。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **"失败数据回炉"的可行单元是"廉价批量结局"而非"昂贵个案机理"**：他们能启动闭环，因为 40 aa miniprotein 的稳定性读出是展示+FACS+测序（单点信息便宜、可测上万突变）。我们的等价物目前不存在——酶设计每条数据都要 LC-MS 确证。启示是：**先设计"便宜可批量、与失败同构"的中间读出**（如灭活对照/无细胞表达量），否则回炉闭环根本点不着火。
2. **"离群者"是被刻意制造的样本**：先用 ML 预测稳、实验不稳的交集聚合"函数失手"，才让失效模式从噪声里显形。我们目前没有可信的"预测 vs 实测"对，说明**下一笔预算应买的是'判据-结局配对'本身**，而不是更多候选。
3. **修函数优先"放大既有基准信号"而不是新建基准**：10/118 的弱信号、×10 权重就够。对我们：评估新判据时优先找"已存在但没被重视的数据分布"作检测器，比再造一套昂贵评测集划算。
4. **参数面小（15 个）是护栏**：只动与失效模式因果相关的参数，其余基准保持/微升，才可辩护"没按下葫芦浮起瓢"。我们若校准评分器（如 MD 派生判据权重），应同样限定改动维度并给全套护栏基准。
5. **两个 59/62 数字不是矛盾而是过滤后口径**（62 验证−3 dropout=59 分析）；提示一切"验证集规模"都应写明**过滤前后**两个数——我们交付任何命中率时也应如此。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：见第 5.6 条三条自限；另有救援效应"部分可能来自噪声"；离群者选择使覆盖面存疑（"It is unclear whether most of the unstable miniprotein designs from Rocklin et al. would have been rescued by single mutations"）；clashing 与稳定性在原始设计群体里不分成败同现（stable/unstable 都高），说明该偏差不是"失败专属"信号。
- 我们读出：① 整个闭环只服务 40 aa 单体小蛋白与界面打分，未触及催化化学——它证明"实验能修打分器"，不证明"修好的打分器能判反应"；② dualoptE 是启发式搜参+人工微调，无收敛性保证，"手工微调半径"一步不可复算；③ 界面基准用 Boltzmann 判别分这类体系内指标，跨体系不可比；④ ΔΔG 分类（±1 kcal/mol 三档）本身是粗分箱，函数改进 0.55→0.55 持平说明该护栏对细微退化并不灵敏；⑤ 志愿计算（Rosetta@home）引入的 dropout 靠启发式过滤消化，过滤规则（0.1 单位/残基）是工程约定不是物理常数。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **"失败→失效模式→基准放大→小参数面修正"的闭环模板**（本库 G7 反馈环）：我们每轮湿实验后应显式做归因分型（分步化学事件卡点），把反复出现的分型映射到某个判据分布上找弱信号，只调与该分型因果相关的少数判据参数，其余判据跑护栏集确认不退化。
2. **离群者抽样策略**：判据说好、便宜读出说差的"矛盾样本"优先重测/深查——这是本文发现 clashing bias 的发动机，也是我们最便宜地暴露自家漏斗盲区的做法。
3. **两级 QC 过滤（重复一致性 + 群体中位数离群）直接搬进 LC-MS 与 MD 数据处理**：同一样品多次进样的峰面积/碎片比差超阈值即作废；某候选信号偏离本轮全体中位数过远即复核——并把被剔除比例与剔除理由写进台账（本文 3/62、>15%、<1,000 三条规则就是范例）。
4. **验证集规模报"过滤前/后"双数**：62→59 的写法应成为我们所有命中率表的标准列。
5. **随机化检验/McNemar 的显著性口径**：判据 A vs 判据 B 的比较必须带配对检验与置换次数（1,000 次），不能只报均值差。

**不可迁移（为什么不能照搬）**

1. **beta_jan25 与本库无直接接口**：它修的是全原子 LJ 排斥面，服务于折叠/界面打分；不能声称"换上 beta_jan25 我们的酶活判据就变准"——催化判据（过渡态几何、化学选择性）不在本文任何基准里，也无 MD/QM 证据。引用它只许作为"闭环方法论"的先例，不许作为"打分器精度"的背书。
2. **DMS 蛋白水解稳定性读出 ≠ 酶活**：EC 50/稳定性 score 是折叠概率的代理，不含周转数与产物比；~1% 救援率、0.55/0.64/0.67 等数字一概不得转用作酶设计成功概率。
3. **"廉价批量突变库"的规模优势不可移植**：我们单轮只能送几个构建体（LC-MS 确证上限），漏斗末端的策略仍是"信息量最大化（机理多样性+失活对照）"而非"样本数最大化"，与本文路线不同。
4. **离群判定阈值不可借用**：stability score <0.3、EC 50 <1.5、Δ>1.0 属于该 assay 的标定体系，挪到任何别处都是无校准的乱用。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/energyfunc2026.txt

- 本地全文：`data/interim/baker_lit/ft/energyfunc2026.txt`（Europe PMC 通路，2026-10-16 抓取，batches.tsv 第 8 批登记 B26 唯一全文；另有登记底稿 `sources/baker.md:342–353`）。
- 汇总引用：`sources/baker.md:613`（第 7 环"反馈回炉"行引 B26：Δstability>1.0、156/16,000）、`sources/baker.md:648`（21 库/16,000 突变重训消除 clashing bias）、`sources/baker.md:660`（OPLS 仅出现于 B26 参考文献标题——与本卡第 3 节"无 MD/QM"互证）。
- CSV 字段映射：第 3 节 ↔ `计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：全部候选引句先经与门禁同一 `litcards_text.norm` 预校验（一处因将正文「this experiment involves…」误写为「which involves…」而 MISS，已按原文改正；一处图注句属 B25 全文，已从本卡剔除）。含内嵌弯引号的句子（如 stability score 定义句）在卡内保留弯引号原字符，归一化后与全文一致；含「outlier」引号的原句已截断引用避免嵌套。59/62 两数并存已在第 2.7/4/6 节给出解释（62 验证集，dropout 弃 3，按 59 平均），非本文自相矛盾。

<!--CSV回填
work_type=论文（能量函数开发/方法学）
target=Rosetta 设计的 40 aa 级 miniprotein（Rocklin 库中判稳实测不稳的 21 个离群设计）+ 17 对设计/晶体结构 + 原子对/界面/ΔΔG 基准
backbone_generation=无新骨架生成；沿用 Rocklin 设计库；诊断用随机森林（生物物理特征含 Rosetta 能量）挑选离群者
computational_filters=研究对象本身=beta_nov16 的 ddG/total score 体系（clashing bias）；再训练= dualoptE 启发式搜参（15 参数）；QC=重复能量一致性>0.1 单位/残基弃、中位 decoy <1,000 弃、单结构丢 >15% 弃
thresholds=离群判定：stability score<0.3、EC50<1.5、EC50 CI<2、ML 预测>1；救援判定：Δ stability score>1.0；原子对基准在 dualoptE 损失中 ×10 权重；QC 过滤 0.1 能量单位/残基；ΔΔG 分箱 ±1 kcal/mol
md_used=否（FastRelax 为能量极小化非动力学；OPLS/MD 仅见参考文献标题）
qm_used=否
experimental_methods=酵母展示+蛋白酶消化+FACS+深测序的 DMS（Maguire 更新载体版；2 蛋白酶×6 浓度 EC50，取最小值聚合；21 库装入 2 大库、库内 338 对照、19/21 生物学重复）；设计-晶体冲突计数；界面/原子对/ΔΔG 基准全部为 Rosetta 计算评估
pipeline_counts=数千设计（Rocklin）→21 离群设计→约 16,000 单突变（~1% 救援：156）→失效模式→54 withheld 晶体基准（10/118 原子对弱信号）→15 参数重拟→beta_jan25；界面基准 65 训练/62 验证（弃 3 后 59 分析）/中位 5,629 decoys/结构；ΔΔG 768→735 与 6,185→633
hit_rate=救援突变率 ~1%（156/16,000）；clashing 偏差"基本消除"（KL 0.022→0.018 p=0.002；界面 0.64→0.67 p<0.001）；ΔΔG 分类持平（0.55/0.55，0.64/0.66，McNemar p=0.78/0.50）；第二失效模式（偏好设计模型 ~0.1 kcal/mol/残基）未解决
best_metric=无单一 Kd/活性值；代表数字：原子对 KL 0.018、界面判别分 0.67（beta_jan25）
cost_or_stat_note=志愿计算 Rosetta@home 跑大量 relax（随机失败致 dropout，靠 QC 过滤）；DMS 21 库并入 2 大库控费；全文未记 GPU/机时数字；随机化检验 1,000 次
role_in_timeline=闭环的最后一块：把湿实验失败数据变成能量函数的诊断与新训练信号（间接放大既有基准而非新建数据），修正 beta_nov16 的 clashing bias 产出 beta_jan25（并入 Rosetta 发行）；与 B09（用实验标注选 DL 判据）互补——B09 选筛子，B26 修秤；并显式登记下一失效模式（极吸引过强）供后续开发
source_pointer=data/interim/baker_lit/ft/energyfunc2026.txt（全文）+ sources/baker.md:342-353（底稿）；代码/数据 https://github.com/Haddox/design_guided_optE；beta_jan25 已入 Rosetta（flag -beta_jan25）
CSV回填-->
