# [B02] 用分子动力学给配体结合蛋白设计"事后判卷"——把 MD 变成可筛选的一步

Barros E P, Schiffer J M, Vorobieva A, Dou J, Baker D, Amaro R E（UCSD / 华盛顿大学 IPD / Janssen）
J Chem Theory Comput 2019, 15(10):5703-5715 · DOI 10.1021/acs.jctc.9b00483 · PMID 31442033 · PMCID PMC7532806
NIHPA 作者手稿版 · https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7532806/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B02**（组：Baker组） |
| 本文取回方式 | Europe PMC `fullTextXML`（`inventory.json` 记 fetch_channel=epmc_fulltext，URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7532806/fullTextXML`） |
| 本地全文①（原始 XML） | `fulltext/B02_PMC7532806_fullTextXML.xml`（162,674 B，SHA-256 `152f6203c85c8f18…`） |
| 本地全文②（本卡引句底稿） | `fulltext/B02_PMC7532806_text.txt`（70,786 B，SHA-256 `3729f748fc98876b…`，去标签纯文本） |
| 文本版本性质 | PMC 里挂的是 **NIHPA Author Manuscripts** 手稿版（PMC7532806.1，PMCID 记录显示 2020-09-27 释放、`pmc-prop-is-real-version no`），不是 ACS 排版正刊；因此正文里的引用编号（如 `Figure 2f`、`Table 1` 前后数字）以空格与行内数字形式留在句子里，本卡引句一律在句内断开、不跨编号拼接 |
| 对照底稿 | `sources/baker.md` 的 [B02] 卡。该登记写于抓取失败当日（Europe PMC 当时返回 HTTP 500），故 CSV 的 `证据级别` 仍记"摘要级"、`hit_rate/成本` 记"未记录"；全文现已取得，**本卡按全文级写**，CSV 侧回填见第 9 节块 |
| 证据级别 | **全文级**（本卡全部引句均可在 `fulltext/B02_PMC7532806_text.txt` 里逐字命中；见第 9 节自检） |
| 未取到的部分 | Supporting Information 只有正文清单式描述（Figure S1–S10、Table S1），图与数据未取到；Fig 1–5 原图像素值未取到。本卡凡涉及只出现在补充材料里的量化对比处，明写"正文未给出数值，仅有正文描述" |
| 特别缺项 | **正文没有给 MD 的 GPU 型号、卡时/核时与单价数字**，只有"整套 MD 准备-模拟-分析在并行 GPU 上不到 2 周"这一自估口径（原文见第 3 节 S11 与第 2 节第 8 条） |

## 1. 这篇到底解决什么（一句话）

它不设计任何新蛋白：把两篇已发表工作（Baker 组 2013 NTF2-digoxigenin 结合体、2018 de novo β-barrel-DFHBI 荧光激活体）留下的 **37 个已知结局的设计体**（成功结合体 / 折对了但不结合 / 压根没折稳）全部拿去做**显式溶剂全原子 MD 的 apo 与 holo 双态模拟**（每重复 500–1000 ns，3–5 重复，累计 184 µs），从轨迹里提 10 个"动力学指纹"，再用 PCA+k-means（无监督）与 k-NN/逻辑回归（有监督）**回顾性**把它们分开——目的是回答一个方法学问题：**MD 能不能从"事后解释失败"升级为"实验下单前的筛选步骤"**（作者原话 "MD could act as a screening step in protein design, resulting in a more efficient process"）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **起点结构本身可能是错的**——漏斗要筛的候选恰恰是没有实验结构的模型。作者把这当成方法论的第一号风险直接写出来："A question might arise in the application of MD simulations for design screening regarding the accuracy and reliability of the results obtained from possibly inaccurately modeled starting structures"。 → **应对**：对两个有 X 射线结构的 tight binder（DIG10.2 取自 4J8T 的 A/B 链、DIG10.3 取自 4J9A 的 C/F 链）额外跑 Rosetta 模型版本（命名为 DIG10.2a、DIG10.3a，"Simulations were run for 500 ns both in apo and holo states, and here we compare results from equivalent simulation lengths of the crystallographic structures"），比对疏水 SASA、腔体积分布、腔内水数、配体 RMSD 四项，得到 "Overall, the dynamics obtained from the modeled structures showed similar distribution profiles to those derived from the simulations of the crystal structures"，并据此下结论 "Our results suggest that simulations starting from modeled structures are therefore accurate enough in sampling protein dynamics to be used with confidence in the assessment of these designs"。 → **代价**：这个对照只覆盖 **2 个设计 × 1 个骨架 × 且两者都是已知成功结合体**（从未拿"模型版会判错"的失败设计做对称检验）；模型版并非处处一致，"In terms of ligand RMSD, DIG10.3a showed a significant tail of higher ligand RMSD values"，原因是 "due to a large transient ligand displacement in one of the runs"。也就是说"模型能用"这一关键前提是**单向验证**的。
2. **静态设计结构的描述子完全分不开成败**（这是本文立论的地基）。作者明写："the descriptors generated from the static structures are not sufficient to distinguish successes from failures"。 → **应对**：把整套评估从静态模型搬到轨迹上，即"动力学指纹"（NOC、疏水 SASA、腔体积、apo 中体积低于阈值的帧数、配体 RMSD、氢键数、腔内水数、水存活概率等）。 → **代价**：静态 vs 动态的对照只以 Supplementary Figure 7 呈现，**正文没有给出静态特征的 accuracy/precision 数字**，因此"动态带来多少增量判别力"在本文里是**定性主张**，不可量化引用。
3. **模拟要多长、跑几份重复——事前没有依据，跑久了又违背初衷**。作者的态度很直白："we do not intend to perform an exhaustive investigation of the design dynamics, as this would likely require extremely long simulations and defeat the purpose of using molecular dynamics to increase the efficiency of the design process"，并补一句 "we aimed at obtaining sufficient sampling for insightful discrimination between the large number of design candidates"。 → **应对**：做显式收敛检验——"computing the average difference between the features for 100 rounds of random selection without replacement"（Knapp/Ospina/Deane 协议），在 DIG 全集 + 5 条 β-barrel 子集（2 个一代 binder + 3 个 non-binder）上以 5×1 µs 跑，结论是 "Analysis of the identified dynamical features indicated that the simulations do not need to be run so extensively, with results either reaching approximately constant values or maintaining constant relation among each other at around 500 ns" 与 "three or four replicas yield property mean values satisfactorily converged and independent, within small variations, of the identity of the replicate simulations"；于是**把后续 33 条 β-barrel 的量降到 500 ns × 3 重复**（"the following results will be discussed for equivalent sampling times for all simulations"）。 → **代价**：判据用词是 "satisfactorily converged"，**原文未给量化收敛阈值**（没有说平均差要小于多少算收敛）；验证子集只有 9 条体系，外推到 33 条全靠作者自陈的效率动机。
4. **固定质子化态是已知失效点，本文只是承认它**：β-barrel 跑到 500 ns 后复查，"observed that about 30% of the histidine residues were assigned a different protonation state due to structural rearrangements, evidencing the limitations of conventional MD when it comes to fixed protonation states"。 → **应对**：**本文未解决**。作者没有重跑、没有改用 constant-pH MD（那句末尾只是引了别人的方法），只在 PROPKA 于 pH 7 赋态（"All starting structures were processed with Maestro-integrated PROPKA to assign protonation states at pH 7"）之后加了一段坦白。这条对本卡后面所有"电荷/氢键网络"类特征都是污染源，而氢键计数恰是他们的主特征之一。
5. **每一个单独特征都有反例，逼着他们换指标而不是设阈值**（这一条对我们最有用）：
   - 腔体积：本想把"apo 腔塌陷"当失败标志，结果 "The non-binders DIG12 and DIG16 have occasional complete closure of the cavity, but the same also happens for the successful binder DIG10.2"，且 "All designs, regardless of binding affinity, showed large variations of cavity volume in the apo state, indicating that the pocket deviates from its designed conformation but that does not necessarily preclude ligand binding"。 → **应对**：把指标从"体积多大"换成"塌陷有多频繁"——"The apo simulations of some of these designs showed such a large number of frames with completely collapsed pockets that it became evident that another useful discriminating metric would be something that could capture this phenomenon"，最终选的是 apo 轨迹中体积低于 30 Å³ 的**帧数**，阈值由配体几何反推（"which represents a pocket volume too small to allow for ligand binding"，依据是 holo 态最小观测体积 33 Å³）。
   - 水计数：绝对水数不足以反映能量学，"as the absolute water count inside the cavity likely does not provide the full picture of the energetics of interactions, we calculated the survival probability of the waters inside the binding pocket in the apo simulations"。 → **应对**：换指标为水存活概率（取 apo 最后 100 ns）。
   - 氢键数：非结合体 DIG12 也能建立大量瞬态氢键，"Interestingly, DIG12 also establishes a large number of transient hydrogen bonds besides those modeled in the design structure due to its larger ligand dynamics"；正文亦承认 "While there's a lot of fluctuation in the number of hydrogen bonds due to the dynamics of the ligands and side chains"。 → **应对**：不把氢键数当独立判据，只作为多特征之一进 PCA/分类器。
   - 疏水 SASA：在 β-barrel 上 "The solvent exposure of hydrophobic residues does not allow for such a clear distinction between the design classes"，作者只肯给一个"经验提示"（约 0.29 nm² 以上只剩非成功设计），并明说那是 suggestion，**没有进分类器当阈值**。
6. **类别极不平衡 + 假阳性来源说不清**：一代 24 条里只有 2 条真结合（"This data set included 24 first-generation designs, among which only two were found to bind with high affinity"，其中 2 条折不稳、20 条折对不结合），无监督 k-means 两簇分不开（"Using the k-means algorithm, the designs were not accurately clustered when only two clusters were used"），三簇才成立。误分里最刺眼的一条是**把不稳定的 HBI_38 归进了成功簇**："One of the false positives in this classification is HBI_38, the non-stable design that did not display as different feature profiles as HBI_41 in Figure 4"。 → **应对**：①把"看不清"的中间地带单独立一个 Uncertain 簇（而非强行二值化）；②对 HBI_38 的误分给出机理解释并承认是时间尺度不够——"the likely much longer timescale that would be required to properly sample the difference between these designs structural stability"（HBI_38 与 HBI_11 只差 N 端两个突变、后者形成分子内二硫键）；③改用有监督，把方向性明确写清："the recall metric at 1.0 for both algorithms, given as the ratio of true positive assignments over all assignments of the real positive class (including false negatives), indicates a complete absence of tight binders being classified as unsuccessful designs"，同时承认 "The precision values, the rate of true positive classifications over all positive assignments (including false positives), indicate the presence of misclassified non-binders"。 → **代价**：这是**牺牲特异性换敏感性**的分类器（漏掉 0 个 binder、但放进来一批假阳），他们没量化"要重测多少条假阳才能捞出 2 个真阳"的实验成本，只在别处给过总账。
7. **无监督模型不跨骨架，泛化能力靠 4 条样本撑**："This unsupervised approach is useful to identify inherent differences between designs of the same structural scaffold, but lacks transferability with the DIG design results"。 → **应对**：转向有监督（"we explored the use of supervised learning for the classification of the joint design scaffold"），并专门做**跨骨架留出**：只用 β-barrel 训练、去预测另一骨架的 4 条 DIG（"yields perfect classification of the designs of the distinct DIG scaffold"）；反向只用 4 条 DIG 训练去预测 33 条 β-barrel，结果作者自己承认精度掉下来（"Conversely, models trained solely on the 4 DIG designs display lower accuracy and precision due to the much smaller training set in this case, but the recall still indicates a perfect absence of false negative classification"）。另外补一句降低未来成本的主张："Logistic regression, in particular, resulted in good classifiers even when trained on small sets"（50% 甚至 33% 训练集，见 Table S1，正文未给数值）。 → **代价**：跨骨架测试集 n=4，"perfect classification" 的统计意义接近于零；两个骨架共 37 条、正类 15 条（本卡按 Table 1 计数），5-fold 交叉验证在这种规模上方差极大——正文表值确实全是 `0.93 ± 0.10` 这类**标准差与均值同量级**的写法。
8. **收益账只能自己估，且他们知道估值偏乐观**："We estimate that the early identification of the 12 unsuccessful designs from the F cluster and the 6 designs from the U cluster could have saved about 6 weeks of work, including protein expression, purification, folding and binding assays"，紧跟着自我拆台："this is likely to be a low-bound estimate as the Baker lab is very well equipped for protein characterization and the entire process could probably take 2 to 3 times longer in a different lab"；MD 一侧是"the MD system preparation, simulation and analysis workflow greatly automates the required steps such that the whole set of proteins can be simulated and analyzed in less than 2 weeks, using parallel GPUs and requiring minimal human intervention"。 → **应对**：用 Kepler 自动化工作流（"We used the MD Kepler Workflow developed by our lab to enable automated MD minimization and equilibration for such a large number of systems"）把人工介入压到最低，并把 MD 输入文件与分析 notebook 开源（正文两处指向 GitHub 仓库）。 → **代价（本文未解决）**：全文**没有 GPU 型号、卡时数、能耗或金钱成本**任何一个数字，"2 周"与"6 周"都无记账依据，无法核对；也没有做过一次真正的前瞻下单来检验这笔账。
9. **标签是二手的**：37 条设计体的 Binder / Non-binder / Unstable 分类与 Kd 全部复用 refs 5 与 7 的既有表征，其中 9 个优化设计的 Kd 在 Table 1 注里标为**基于粗略滴定数据的估计值**；本文未做任何新湿实验。 → **应对**：作者用词一直是 retrospective（"The simulations provide retrospective insights into the properties affecting ligand affinity"）。 → **代价：本文未解决**——没有任何一批新设计是"按 MD 建议下单并被实验确认"的，所以"MD 当筛子"在本文状态是**待验证假设**，其乐观性见第 7 节。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 先列方法工具箱（用了什么、为什么用它）

- **被评估的对象（不是本文生成的）**：Rosetta 配体结合设计管线的产物，直接取自两篇已发表工作——NTF2 骨架 digoxigenin 结合体 4 条（"Four designs of the digoxigenin-binders based on Nuclear Transport Factor 2 (NTF2) folds were selected"）与 de novo β-barrel 骨架 DFHBI 结合体 33 条（"In the work of Dou et al these successful initial designs were further optimized, resulting in 9 second and third-generation designs with higher ligand affinity"）。标签口径由原作者定："This set included examples of tight binders as well as unsuccessful designs, thus classified due to failures to fold properly or to bind to the ligand with high affinity"。
- **MD 引擎与力场**：GPU 加速 Amber14（ff14SB 蛋白、TIP3P 水、NaCl），配体用 Antechamber + GAFF 参数化、Gaussian 09 做几何优化（"The digoxigenin and DFHBI ligands were parametrized using Antechamber and the generalized Amber force field (GAFF)"）；PME 处理长程静电（"the long-range electrostatic interactions were approximated by particle mesh Ewald"）；"The simulations used a 2 fs time step with the SHAKE algorithm to constrain hydrogen atoms"。
- **体系准备工具**：Schrödinger Maestro/Prime 补缺失残基与侧链、PROPKA 赋质子化态、Dowser 往摘掉配体的空腔补水（"was used to hydrate the protein cavity following removal of the ligand's coordinates for apo simulations"）、Kepler Workflow 做自动化最小化与平衡。
- **分析工具**：VMD 可视化 + CPPTRAJ / MDTraj / PyEMMA / MDAnalysis 提特征 + POVME 2.0 测腔体积（"Cavity volume was investigated using POVME (Pocket Volume Measurer), version 2.0"）；机器学习用 scikit-learn（"Python's scikit-learn library was used to perform unsupervised and supervised learning on the features extracted from 500 ns of simulations"）；notebook 与 MD 输入文件公开在 GitHub（"The Jupyter notebooks are available for download on GitHub"）。
- **本文没有用的方法**：MM-PBSA/TI/FEP 等**自由能计算一个都没做**；没有 QM/MM、没有反应坐标、没有结合常数预测；没有新做湿实验。它的证据类型只有"轨迹描述子 + 分类器指标"。

### A. 从设计集到轨迹（生产段）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | refs 5、7 已发表设计体与其实验结局 | 选样，覆盖成功/失败两类，跨两个骨架两种配体 | **原文未给阈值**（标签沿用原论文：Binder / Non-binder / Unstable；Kd 数值见 Table 1） | 4 条 DIG（含 2 binder、2 non-binder）+ 33 条 β-barrel（2 条一代 binder、20 条折对不结合、2 条折不稳、9 条优化后 binder）= **37 个设计** |
| S2 | 上述设计的序列与设计模型 | 有晶体结构的用晶体（DIG10.2 → 4J8T 链 A/B；DIG10.3 → 4J9A 链 C/F），其余用 Rosetta 模型；缺失末端用 Maestro 补、缺失侧链用 Prime 补 | 无阈值；"The structures of DIG10.2 and DIG10.3 have been solved by X-ray crystallography and were the starting structures of the simulations" | 每条一个起始坐标；另加 DIG10.2a / DIG10.3a 两个模型版对照组 |
| S3 | 配体 digoxigenin、DFHBI | Antechamber + GAFF 参数化，Gaussian 09 几何优化；DFHBI 单独抬高 C2-C1-C7-C8 二面角势垒以强制平面（"For DFHBI, the torsional parameters of the C2-C1-C7-C8 dihedral were increased to model the molecule's expected planarity due to its aromaticity in the bound fluorophore state"） | 无阈值（人为加高势垒＝先验设定，不是数据定的） | 两套配体拓扑参数 |
| S4 | 全体系 | PROPKA 赋态 + Dowser 补水 + 加离子溶剂化 | 质子化态按 **pH 7**；水盒缓冲距离 **β-barrel 13 Å / DIG 15 Å**；盐浓度 **150 mM NaCl**（"with counter ions for charge neutrality, and 150 mM NaCl to simulate the experimental ionic concentration"） | apo 与 holo 两套状态，每个体系各一份起点 |
| S5 | S4 的体系 | 五阶段最小化（仅氢 → 溶剂 → 溶剂+配体 → 侧链 → 全体系），最陡下降 + 共轭梯度混合 | **13,000 cycles**（"Minimization consisted of five stages: hydrogen only, solvent, solvent and ligand, side chains, and the full system resulting in 13,000 cycles using a combination of steepest decent and conjugate gradient methods"） | 最小化后构象 |
| S6 | 最小化构象 | 加热与平衡：恒容 100 K 加热 50 ps → 恒压 298 K、1 bar 加热 200 ps → 298 K/1 bar 再平衡 2.25 ns；并跟踪 RMSD 演化确认松弛 | 判据为"RMSD 演化确认已松弛收敛"，**原文未给 RMSD 数值阈值**（"Since the majority of the starting structures were not experimentally-resolved conformations, we performed a long equilibration protocol and verified RMSD evolution to ensure system relaxation and convergence"） | 生产模拟起点 |
| S7 | S6 起点 | NPT 生产 MD（1 bar、298 K，非键截断 10 Å，PME，2 fs + SHAKE）；初始数据集每条 5 重复 × 1000 ns，验证体系 3 重复 × 500 ns，apo 与 holo 各跑（"All systems were simulated in their apo and ligand-bound (holo) states"；"The initial design data set was simulated for five replicas of 1,000 ns each in the apo and holo states, while additional validation systems were simulated in three 500 ns replicas of each state"） | 采样长度阈值由 S8 的收敛检验**事后**确定 | 累计 **184 µs**（正文原句给 "resulting in a total sampling of 184 µs"）；Table 1 共 39 个模拟条目（37 设计 + DIG10.2a/10.3a） |
| S8 | DIG 全集 + 5 条 β-barrel 子集（2 个一代 binder、3 个 non-binder），5×1 µs | 收敛/重复数检验：按 Knapp-Ospina-Deane 协议做随机无放回抽样比特征均值差（"computing the average difference between the features for 100 rounds of random selection without replacement"） | 经验结论：**约 500 ns** 特征近常数或保持恒定相对关系（"Analysis of the identified dynamical features indicated that the simulations do not need to be run so extensively, with results either reaching approximately constant values or maintaining constant relation among each other at around 500 ns"）；**3 或 4 重复**即可（"three or four replicas yield property mean values satisfactorily converged and independent, within small variations, of the identity of the replicate simulations"）；无量化收敛数值阈值 | 决定把其余 β-barrel 降为 **500 ns × 3 重复**，全部结果按等采样时长比较 |

### B. 从轨迹到判据（分析段；10 个动力学指纹）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S9a | apo/holo 轨迹 | 结构柔性：Cα RMSF（CPPTRAJ，骨架对齐）＋用 PyEMMA 正则空间聚类得**簇数 NOC**（"to obtain the number of clusters (NOC) sampled"） | 聚类用 Cα 坐标 + RMSD 度量，**cutoff 1.5 Å**；每 **100 帧**取一次；NOC 越大＝越柔（"the number of clusters (NOCs) thus obtained was used as a representation of structural flexibility since at least in principle more flexible proteins sample a larger conformational ensemble in the simulations"） | 每设计 NOC（apo/holo 各一） |
| S9b | 同上 | 疏水核暴露：逐帧算 Ala/Ile/Leu/Phe/Val/Pro/Gly/Met/Trp 的 SASA（MDTraj） | 本文只给趋势；β-barrel 上的"经验线"是 apo/holo 疏水 SASA 约 **0.29 nm²** 以上只剩非成功设计，作者称之为 suggestion 而非阈值（"The solvent exposure of hydrophobic residues does not allow for such a clear distinction between the design classes"） | 每设计平均 SASA/疏水残基 |
| S9c | 同上 | 腔预组织：POVME 2.0 算腔体积，同一骨架共用同一组 POVME 球、关闭 convex hull（"To allow for comparison across designs, the same POVME spheres were used for each scaffold"） | 体积累计分布 + holo 平均体积；**"低于 30 Å³ 的帧数"**作为塌陷计数指标，30 Å³ 的依据是配体装得下的最小观测体积 33 Å³（"which represents a pocket volume too small to allow for ligand binding"）；每 100 帧算一次（"Volume calculations were performed for every 100 frames of the aligned trajectories"） | 每设计两个数：塌陷帧数 + holo 平均体积 |
| S9d | 同上 | 界面氢键：算设计时指定与配体成键残基的 χ1 是否停在设计构象；数蛋白-配体氢键 | 只计"强与中等强"两类：强＝X–H···Y 1.2–1.5 Å 且角 170–180°，中等＝1.5–2.2 Å 且 130–170°（原文该句含公式上标，本卡不整句引用）；对照组：所有设计当初都被设计成至少 4 条氢键（"all generated designs had been originally intended to form at least four hydrogen-bonding interactions with the ligand"） | 每设计每帧平均氢键数 |
| S9e | holo 轨迹 | 配体动力学：轨迹按蛋白坐标对齐后算配体相对设计构象的 RMSD | 无固定阈值；定性分档——binder 配体几乎不动，non-binder 大幅位移，DIG16 甚至脱落（"the ligand showed a large degree of displacement from its starting position, probably influenced by the larger size of the cavity, including complete dissociation from one of the monomers in 2 out of the 5 holo DIG16 trajectories"） | 每设计配体 RMSD 分布（37 × apo/holo） |
| S9f | apo（补水）/holo 轨迹 | 腔内水：数限定球内水分子（digoxigenin 以 C7 原子为心 **半径 8 Å**、DFHBI 以 C1 为心 **半径 7 Å**；"we counted the number of water molecules within a sphere delimiting the binding site"），并算 apo 最后 100 ns 的**水存活概率**（"was used to calculate water survival probability within the same defined spheres in the last 100 ns of the apo simulations"） | 无阈值；结论为 binder 的水更长驻（"survival probability for the tight DIG binders decay more slowly than that for the non-binders, indicating presence of longer-lived waters inside these cavities"） | 每设计水数 + 存活曲线 |
| S10 | S9a–S9f 的 10 个特征 | 特征缩放后做 PCA，投到 3 个主成分看类别分布 | 3 个 PC 合起来解释 **80% 方差**；判据是"成功体聚在 PC1/PC2 小值区"（"the successful binders cluster together in regions of smaller PC1 and PC2, while the non-binders are more spread along the principal components"）；缩放按骨架分别做（"Feature scaling was performed among the designs of a particular scaffold to prevent dominance of larger-valued features"） | 33 条 β-barrel 的 3D 分布 + 特征载荷解释（熵主导 PC1、诱导契合 PC2、焓 PC3："Entropy seems to play the most pronounced role in determining binding"） |
| S11 | 同上 | 无监督 k-means 分簇 → 命名 Successful (S) / Uncertain (U) / Failed (F) | 两簇分不开（"Using the k-means algorithm, the designs were not accurately clustered when only two clusters were used"），三簇才可用（"but assigning the data to three distinct clusters yielded interesting results with good clustering quality (average silhouette value of 0.45)"）；**外部阈值＝无**，簇边界完全由数据决定 | 33 条分成 F 簇 12 条、U 簇 6 条、S 簇含全部 tight binders 且"with only 4 inaccurate classifications and no false negative assignments"；作者据此估算"could have saved about 6 weeks of work, including protein expression, purification, folding and binding assays"，同时自认这是低 bound 估计（"this is likely to be a low-bound estimate as the Baker lab is very well equipped for protein characterization and the entire process could probably take 2 to 3 times longer in a different lab"）；MD 一侧"can be simulated and analyzed in less than 2 weeks, using parallel GPUs and requiring minimal human intervention" |
| S12 | joint 37 条（两个骨架合并）的 10 指纹 | 有监督分类：k-NN 与逻辑回归，5 折交叉验证（"K-nearest neighbors and logistic regression classifiers were trained using 5-fold cross validation on the 10 dynamical fingerprints"）；k-NN 用 k=2 或 5、均匀权重、欧氏距离；逻辑回归用 liblinear 求解器、tolerance 1e-4 | 指标口径：accuracy / precision / recall / MCC / F1（作者自己解释 precision 说明有误分的 non-binder、recall=1.0 说明没有 binder 被判死）；无外部通过阈值 | joint 集：k-NN 0.84±0.16 acc / 0.79±0.21 prec / 1.0 recall / MCC 0.74±0.25；逻辑回归 0.93±0.10 acc / 0.87±0.17 prec / 1.0 recall / MCC 0.87±0.16 / F1 0.92±0.10（Table 2，值为 5 折的均值与标准差） |
| S13 | 只用 β-barrel 训练（33 条按 70:30 随机切）→ 预测另一骨架的 4 条 DIG | 跨骨架泛化检验，重复 10 次随机切分 | 判据＝测试集指标；**DIG 测试集只有 4 条**（"yields perfect classification of the designs of the distinct DIG scaffold"） | Table 3：逻辑回归验证集 0.91±0.08 acc，DIG 测试集 acc/prec/MCC 全 1.0、recall 1.0；k-NN 测试集 acc 1.0、prec 1.0、recall 0.95±0.15 |
| S14 | 反向：只用 4 条 DIG 训练 → 预测 33 条 β-barrel | 小训练集能不能外推 | 判据同上 | Table 4：k-NN(k=2) 与逻辑回归都是 acc 0.70 / prec 0.52 / recall 1.0 / MCC 0.53 / F1 0.69；作者补"the 12 non-binders correctly identified correspond exactly to the designs classified in the F cluster using unsupervised learning" |
| S15 | 训练集大小消融 | 只给 33% 或 50% 数据训练，看前瞻可行性 | **数值在 Table S1（未取到）**，正文只有定性句"resulted in good classifiers even when trained on small sets" | 正文结论：需要实验验证的设计数可以很少 |

### C. 这套流程的骨架（值得单独记住）

它的顺序是 **① 先在别人的、已有结局的体系上把 MD 特征造出来 → ② 先用收敛检验把单价压到能接受（1 µs×5 降到 500 ns×3）→ ③ 单特征逐个试、失败就换指标而不是加阈值 → ④ 多特征联合：先无监督（分不出就用三簇 + 中间态 U）→ ⑤ 再有监督（分骨架留出、报 precision/recall 双向）→ ⑥ 最后才谈省了多少周**。
第 ③ 步和第 ⑥ 步是本文最诚实的两处：**通篇没有一处把单个 MD 特征写成硬闸口**，也**没有一次前瞻下单**。这两点直接决定它在 UAA 项目里能充当"MD 可不可能成为判定闸口"的**可行性证据**，而不是**命中率证据**。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段 / 位置） |
|---|---|---|
| 37 个设计 / 2 个 fold | 被模拟的设计体总数（4 条 NTF2-DIG + 33 条 β-barrel-HBI） | "Simulations ranging from 500 to 1000 ns per replicate were conducted on 37 designed protein variants encompassing two distinct folds and a range of ligand affinities" |
| 184 µs | 累计采样时长（全项目） | "resulting in a total sampling of 184 µs"（Methods，MD protocol 段末） |
| 5 × 1,000 ns；3 × 500 ns（apo 与 holo 各一套） | 初始数据集 / 后续验证体系的重复与长度 | "The initial design data set was simulated for five replicas of 1,000 ns each in the apo and holo states, while additional validation systems were simulated in three 500 ns replicas of each state" |
| 39 个模拟条目 | Table 1 实列行数＝37 设计 + DIG10.2a + DIG10.3a 两个模型版对照（**本卡按 Table 1 逐行数**） | Table 1 文本（Design name / KD / Classification / 重复数 / 长度 五列） |
| 24 → 2 / 20 / 2 | 一代 β-barrel 设计数 → 真结合体 / 折对不结合 / 折不稳 | "This data set included 24 first-generation designs, among which only two were found to bind with high affinity"；"two were verified to be structurally unstable and thus not fold in the predicted β-barrel structure (HBI_38 and HBI_41), 20 fold properly but fail to bind to the ligand" |
| 9 | 二/三代优化后设计数（全部为 binder，Kd 约 0.5 µM 级） | "resulting in 9 second and third-generation designs with higher ligand affinity"；Table 1 中 b11_loop、b11L5F.* 、mFAP0 标 ~0.5 µM（作者注明为粗略滴定估计），mFAP1 = 0.56 µM |
| 8.9 nM / 541 pM / 12.8 µM / 49.8 µM | DIG10.2 / DIG10.3 / HBI_11 / HBI_32 的 Kd（Table 1 原值） | Table 1 文本行；DIG 值来自 ref 5，HBI 值来自 ref 7 |
| 56 条 → 2 条 | 被复用的前作漏斗账（β-barrel 那篇：表征 56 条高分序列得 2 个结合体） | "required the generation of thousands of designs and experimental characterization of 56 high-scoring sequences to yield two successful binders" |
| 13,000 cycles / 五阶段 | 最小化协议规模 | "Minimization consisted of five stages: hydrogen only, solvent, solvent and ligand, side chains, and the full system resulting in 13,000 cycles using a combination of steepest decent and conjugate gradient methods" |
| 100 K 50 ps → 298 K 200 ps → 2.25 ns | 加热与平衡时长（恒容→恒压 1 bar→恒压） | "Equilibration involved an initial heating to 100 K at constant volume for 50 ps followed by heating to 298 K at constant pressure, 1 bar, for 200 ps"（其后一句给 2.25 ns） |
| 13 Å（β-barrel）/ 15 Å（DIG）；150 mM NaCl；pH 7 | 水盒缓冲距离 / 离子浓度 / 质子化赋态 pH | "with counter ions for charge neutrality, and 150 mM NaCl to simulate the experimental ionic concentration"；"All starting structures were processed with Maestro-integrated PROPKA to assign protonation states at pH 7" |
| ~30% 的 His 态在 500 ns 后应改 | 固定质子化态的失效率（作者复查结果，未重跑） | "observed that about 30% of the histidine residues were assigned a different protonation state due to structural rearrangements, evidencing the limitations of conventional MD when it comes to fixed protonation states" |
| 约 500 ns；3–4 重复 | 采样收敛的经验结论（无量化阈值） | "with results either reaching approximately constant values or maintaining constant relation among each other at around 500 ns"；"three or four replicas yield property mean values satisfactorily converged and independent, within small variations, of the identity of the replicate simulations" |
| 1.5 Å | PyEMMA 正则空间聚类的 RMSD cutoff（NOC 特征） | "to obtain the number of clusters (NOC) sampled"（Methods，聚类句内含 1.5 Å cutoff） |
| 30 Å³（塌陷判定体积）；33 Å³（holo 最小观测体积） | apo 腔"太小装不下配体"的帧计数阈值及其依据 | "which represents a pocket volume too small to allow for ligand binding"（同句给 30 与 33 两个数，单位 Å³ 带空格，本卡不整句引用） |
| ~0.29 nm² | 疏水残基 SASA 的"经验提示线"（作者自称 suggestion，未进分类器） | "The solvent exposure of hydrophobic residues does not allow for such a clear distinction between the design classes"（同段随后给 0.29 nm² 提示） |
| 8 Å / 7 Å | 腔内水计数球半径（digoxigenin 以 C7 为心 / DFHBI 以 C1 为心）；存活概率取 apo 最后 100 ns | "we counted the number of water molecules within a sphere delimiting the binding site"；"was used to calculate water survival probability within the same defined spheres in the last 100 ns of the apo simulations" |
| 1.2–1.5 Å + 170–180°（强）；1.5–2.2 Å + 130–170°（中等） | 计入的蛋白-配体氢键几何定义 | Methods 的 H-bond 段（同句给出两类定义，含 Å/° 与破折号，本卡不整句引用）；设计侧对照："all generated designs had been originally intended to form at least four hydrogen-bonding interactions with the ligand" |
| 2 out of 5 | holo DIG16 轨迹中配体完全从一条单体脱落的次数 | "including complete dissociation from one of the monomers in 2 out of the 5 holo DIG16 trajectories" |
| 3 PC = 80% 方差 | β-barrel 特征 PCA 降到三维的解释量 | "projected the β-barrel dataset into three principal components (PC) which describe 80% of the data variance" |
| 3 簇；silhouette 0.45 | k-means 最佳分簇数与轮廓系数（2 簇不可分） | "but assigning the data to three distinct clusters yielded interesting results with good clustering quality (average silhouette value of 0.45)" |
| F 12 条 / U 6 条 / S 簇 4 条误分、0 假阴 | 无监督三簇的人数与误分方向 | "the unsupervised learning approach here employed on the features measured from the simulations was thus able to identify the high affinity binders with only 4 inaccurate classifications and no false negative assignments"；"We estimate that the early identification of the 12 unsuccessful designs from the F cluster and the 6 designs from the U cluster could have saved about 6 weeks of work, including protein expression, purification, folding and binding assays" |
| 88% accuracy（33 条） | 无监督（PCA+k-means）在 β-barrel 集上的总体准确率 | "resulted in a 88% accuracy of binding ability classification using unsupervised learning" |
| 2 真阳 + 4 假阳 = 6 条预测；绝对命中率 2/6 ≈ 33%；富集 ((2/6)/(2/24)) = 4× | 若把该法用于 24 条一代设计筛选的实际收益 | "which constitutes a 4-fold enrichment ((2/6)/(2/24)) over the initial candidate design data set" |
| 逻辑回归 joint 集：acc 0.93±0.10、prec 0.87±0.17、recall 1.0±0.0、MCC 0.87±0.16、F1 0.92±0.10 | 有监督在合并 37 条上的 5 折交叉验证 | Table 2；口径见 "The precision values, the rate of true positive classifications over all positive assignments (including false positives), indicate the presence of misclassified non-binders" 与 "the recall metric at 1.0 for both algorithms, given as the ratio of true positive assignments over all assignments of the real positive class (including false negatives), indicates a complete absence of tight binders being classified as unsuccessful designs"；± 值含义见 "Values correspond to average and standard deviation of the 5 cross validations" |
| k-NN joint 集：acc 0.84±0.16、prec 0.79±0.21、recall 1.0、MCC 0.74±0.25、F1 0.87±0.13 | 同一考卷上的最近邻基线 | Table 2（同上两句口径） |
| β-barrel 训练→DIG 测试：acc 1.0、prec 1.0、MCC 1.0（LR）；k-NN 测试 acc 1.0、recall 0.95±0.15 | 跨骨架泛化，**测试集只有 4 条** | Table 3；"yields perfect classification of the designs of the distinct DIG scaffold"；± 口径见 "Values correspond to average and standard deviation of 10 rounds of random splits of the data set according to the 70%:30% training:validation ratio" |
| DIG 训练→β-barrel 测试：acc 0.70、prec 0.52、recall 1.0、MCC 0.53、F1 0.69 | 反向（小训练集 4 条）的外推代价 | Table 4；"Conversely, models trained solely on the 4 DIG designs display lower accuracy and precision due to the much smaller training set in this case, but the recall still indicates a perfect absence of false negative classification" |
| 12 条 non-binder 与 F 簇完全重合 | 两种方法在同一批失败样本上一致 | "the 12 non-binders correctly identified correspond exactly to the designs classified in the F cluster using unsupervised learning" |
| 省约 6 周湿实验 / 别的实验室要 2–3 倍 / MD 全流程 <2 周 | 收益账（作者自估，**无卡时或金钱数字**） | "this is likely to be a low-bound estimate as the Baker lab is very well equipped for protein characterization and the entire process could probably take 2 to 3 times longer in a different lab"；"can be simulated and analyzed in less than 2 weeks, using parallel GPUs and requiring minimal human intervention" |

## 5. 结论——作者说了什么

1. **设计与模拟的结构系综不一致**："It became evident that the design model generated by the protein design protocol may differ from the ensemble of structures accessed by the simulations, such that the modeled structural descriptions can be further enriched by the incorporation of dynamic fingerprints."
2. **成功与失败设计在动力学性质上有系统性差异**，且**熵项是主因**、现有经验设计力场难以纳入："Entropic components play a significant role in determining ligand affinity, which are complex and often very challenging to incorporate in the empirical models of protein design"（摘要版说法："Features indicate that entropic components are particularly important for affinity, which are not easily incorporated in the empirical models often used in design protocols"）。
3. **易测的 MD 描述子（NOC、腔体积、疏水 SASA、腔内水数、氢键数）在 33 条 β-barrel 上做到 88% 分类准确率**；对 24 条一代设计做筛选会得到"2 个真结合体 + 4 个假阳"，即 **4 倍富集**、至少一个月工时的"节省"。
4. **有监督（k-NN / 逻辑回归）在两个骨架合并集上准确率良好且没有假阴**，因此作者认为该方法有泛化性；结论句是 "thus, emerges as a potential general and scaffold-independent screening methodology to aid the challenging protein design process"。
5. **总定位**：本文的落点是"MD 可以作为设计流程里的一道筛选步骤，从而避开对不稳定/低亲和力设计的实验测试、提高管线效率"——原句 "The results here described emphasize how MD can act as a promising screening step in the protein design process"，以及摘要里的 "MD could act as a screening step in protein design, resulting in a more efficient process"。
6. 作者的自限性表述（同一篇里就有）：无监督法"lacks transferability"跨骨架、precision 里存在误分的 non-binder、收益估计"likely to be a low-bound estimate"、机理动机是 retrospective 而非前瞻（"The simulations provide retrospective insights into the properties affecting ligand affinity"）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的贡献不是"MD 能筛"，而是"MD 只能以事后判卷的方式小规模筛"**。它的证据结构是 37 条回顾样本、0 条前瞻下单，所以"screening step"在文中是**目标**而不是**结果**。把它当"MD 已证明可当判定闸口"来引，就是把作者的假设句读成了结论句。
2. **最有价值的工程决策是把单价砍下来那一步**（S8：1 µs×5 → 500 ns×3，且明确说"跑穷尽就失去意义"）。这正是我们缺的口径——我们过去把预算压在长轨迹上却没有先做"特征需要多长才稳"的收敛检验。这条**可原样搬**。
3. **他们的"三簇 + Uncertain 中间态"就是我们需要的 UNKNOWN 制度化**。单特征全都有反例（DIG10.2 也塌腔、DIG12 也有一堆瞬态氢键），于是他们放弃"一个数一条线"，改成联合分布 + 中间态。对我们：**任何一维几何/动力学量都不许单独做闸口**，且必须允许"判不动"这一输出存在。
4. **"recall=1.0、precision<1"是有方向的选择**：他们宁可多测假阳也不漏真 binder。UAA 项目的处境相反——我们最缺的是**否证能力**（把不该做的候选挡掉），所以真正该看的是他们的 precision 0.52–0.87 那一侧，也就是"MD 说要淘汰的里面错了几个"。本文从未报告这个方向的数字（**未记录**）。
5. **"4 倍富集"是本文里最容易被误引成概率的数字**。它的分子分母都是同一批 24 条回顾数据，绝对命中率 2/6，且正类只有 2 条。把它读成"用 MD 有 X% 概率找到活性分子"是没有依据的（详见第 8 节）。
6. **两个骨架的样本结构（37 条里正类 15 条，DIG 只占 4 条）意味着任何"跨骨架泛化"的检验功效都极低**：Table 3 的 1.0 是 4 个样本的 1.0。这不是造假，是**功效不足**，而正文语气（"perfect classification""evidence the generality"）明显超出样本能支撑的强度。

## 7. 局限与失败（作者的 + 我们读出的）

**作者承认的**
- 无监督跨骨架不可迁移："This unsupervised approach is useful to identify inherent differences between designs of the same structural scaffold, but lacks transferability with the DIG design results"。
- 分类器有假阳（precision 0.52–0.87 各处），只是没有假阴。
- 收益估算是下界："this is likely to be a low-bound estimate as the Baker lab is very well equipped for protein characterization and the entire process could probably take 2 to 3 times longer in a different lab"。
- 固定质子化态是 conventional MD 的局限（30% His 那句），本文未处理。
- 本文定位是回顾性洞察，不是前瞻筛选。

**我们读出的（更关键的几条）**
1. **零前瞻验证**：全部标签来自 refs 5、7 的历史实验，且 9 条优化设计的 Kd 本身在 Table 1 注里被标成"粗略滴定估的"。**没有一批新设计是按 MD 建议下单再被湿实验确认的**——所以"MD 提高漏斗效率"从未被这篇直接测过。
2. **规模与漏斗不在一个量级**：37 条 × apo+holo × 3–5 重复；同一项目的对照前作（本文自己引的 β-barrel 那篇）是"数千设计 + 表征 56 条得 2 个结合体"，DL 漏斗（本库 B09）是每靶约 2M 设计。**MD 一侧连千分之一都覆盖不到**，只能做"末端几十条的复筛"，不可能当召回闸口。
3. **验证的模型-晶体一致性是单向的**：只用 2 条**已知成功**的设计验了「模型版结果可用」，没有验证过「模型版把失败设计误判为成功」的情形；反而观察到模型版配体 RMSD 出现长尾。第 1 条难点的结论（原文那句 accurate enough in sampling protein dynamics to be used with confidence）比证据支持的强度更大。
4. **判据全部是几何/统计量，没有能量学**：没有 MM-PBSA、没有 TI/FEP、没有结合自由能、没有动力学速率（k_on/k_off）。也就是说这篇**没有把 MD 的物理优势（自由能/路径）用进去**，只用了它的构象系综，因此它对"MD 能不能判催化"的支撑比它看起来更弱。
5. **表内 ± 与均值同量级**（如 accuracy 0.84±0.16），说明交叉验证在 37 条上极不稳定；正文没有给出置信区间或置换检验。任何"分类器性能"的引用都必须带这个不确定性。
6. **类别不平衡与阈值不可迁移**：88% 与 4× 富集都绑定在"2 个具体骨架 + 2 个具体小分子 + 该配体的体积下限 30 Å³"上。这些数在换成别的配体（更别说换成'酶促反应能不能成键'）时**没有任何理由仍成立**。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"MD 只做事后判卷、不当生成器"这个定位可以直接用**。我们的候选末端只有几十条量级（第 11/13 轮的可路由候选池），恰好落在本文的适用尺度：对少数候选跑 apo+holo 双态、多重复、固定窗口提特征，是**负担得起**的；本文的输入文件与 notebook 开源（GitHub）也给了可照抄的协议骨架（五阶段最小化 13,000 cycles、100 K/50 ps → 298 K/200 ps → 2.25 ns、PME + 10 Å 截断、2 fs + SHAKE、150 mM NaCl、PROPKA pH 7）。
2. **S8 的收敛-定长流程必须照搬**：先在少数阴阳性同域体系上用"100 轮无放回随机抽样的特征均值差"判"多短够用、几份重复够独立"，再定全量预算。这与本项目实测单价（MD 156.6 ns/day、新建体系 10.6 GPU·h）可以直接合成一条"每条判据多少核时"的预算线。
3. **三簇（S/U/F）+ 没有假阴的方向性报告**，对应我们的三态输出（支持 / 否证 / UNKNOWN）与"哪个方向的错误更贵"必须显式写清。UAA 侧的方向性我们应当是**优先要否证能力**（挡住不该做的），因此报告指标要以"被判死的候选里有没有真阳性"为主，本文的 recall=1.0 口径反过来用。
4. **"单特征不许当闸口"这条教训可直接进判定标准**：我们的最小化距离/角度类几何量（如 ≤4.0 Å、≥150° 那类冻结口径）在本项目 2026-10-19 实测里已经出现"D73N 失活背景反而优于 WT"的反转——与本文"DIG10.2 也塌腔、DIG12 也一堆氢键"是同一种失效；解法一致：**改成计数/系综量 + 多特征联合 + 允许中间态**。

**不可迁移（为什么不能照搬）**

1. **任何阈值都不许搬**：30 Å³ / 33 Å³ 是"这个配体装不装得进这个腔"的几何下限，0.29 nm² 是这两个骨架的疏水暴露经验线，1.5 Å 是聚类分辨率，silhouette 0.45 与 80% 方差是这批 33 条数据的量，1e-4 / k=2 或 5 是这批特征的分类器超参。**它们与 UAA 合成酶能不能完成三步化学事件（尿嘧啶聚合起始、pppUA 成键、第二枚 ATP vs 环化竞争）没有任何映射关系**。尤其本项目已有实测：pppUA 体系连接数已为 1（预置成键），MD 的"腔/键"几何量在那里根本不会给出方向信息。
2. **不许把 88% accuracy、4× 富集、2/6≈33% 命中率、"省 6 周"当我们的概率或收益**：那是二值结合标签 + 回顾集 + n=2 正类下的数字；本文没有任何酶活读数，把它写成"MD 对 UAA 候选成功率 X%"属于编造（本库 AGENT_RULES 第 7 条禁止）。
3. **本文不含 QM/MM、自由能或反应路径**，所以它**不能为"用 MD/QM 判催化"提供命中率背书**；它能为"MD 能在几十条规模上做机制层复筛"提供**可行性**参照，仅此而已。作者提到酶设计里"短模拟提示关键催化相互作用被破坏、并被提议作为酶设计的筛选方法"只是引别人的动机（ref 35），不是本文结果。
4. **本文没有湿实验闭环，我们也不能指望它有**：UAA 的判定终点是 LC-MS/MS 产物身份，第一道湿实验本身就是难点（本库 B09 里 YSD→BLI 全一致的情形在这里不存在）。因此本文的"MD 判据 → 少做实验"的净收益链条，在我们这里中间还夹着一道未验证的产物化学。
5. **固定质子化 + 缺自由能这两处在 UAA 活性位点是加重而非减轻的问题**：合成酶活性位点带金属离子与磷酸/尿嘧啶电荷网络，His/Asp/Glu 质子化态与金属配位状态对成键几何的影响比本文两个纯疏水/氢键腔更大；本文对此只承认知而未改（"本文未解决"）。若照搬其协议，必须在 run.md 里明写这条未消除的风险。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/B02_PMC7532806_text.txt

- **本卡全部引句只对照这一份底稿**：`fulltext/B02_PMC7532806_text.txt`（70,786 B，SHA-256 前 16 位 `3729f748fc98876b`），由 `fulltext/B02_PMC7532806_fullTextXML.xml`（162,674 B，`152f6203c85c8f18…`）经 `scripts/litcards_text.py` 的去标签 + 实体解码 + 空白折叠生成；该文是 Europe PMC `fullTextXML` 通道取回的 **NIHPA 作者手稿版**（同一论文若换成 NCBI/ACS 排版抽取版，句内引用编号与单位空格会不同，故本卡只声明这一份为底稿）。
- **凡本卡带 Å / nm² / Å³ / ° / µs / ± 的数值，均不出现在引号里**（这些字符不是 ASCII，且原文把它们与数字之间留了空格，如 `30 Å 3`），只在正文里以数字 + 单位陈述；对应用句在台账中标注"同句给两数、本卡不整句引用"。
- 对照底稿（非引句来源）：`sources/baker.md` 的 [B02] 卡。该登记形成于抓取失败当日，写的是"Europe PMC fullTextXML 返回 HTTP 500 → 摘要级 + Crossref 元数据"，其 `hit_rate / best_metric / 成本统计` 均记为"未记录"；本卡用已取得的手稿全文把这些坑填上（见第 4 节与回填块），**CSV 行本身未由本卡改动**（按规程，不改 CSV，只交回填块）。
- 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **未取到 / 未核验的部分**（不许当已证事实引用）：Supporting Information 的 Figure S1–S10 与 Table S1（训练集 33%/50% 消融的具体数值）；Fig 1–5 的原图读数；MD 的 GPU 型号、卡时与任何金钱成本；本文没有前瞻湿实验，因此"MD 筛子提高成功率"没有独立实验闭环可查。
- **自检命令与结果**：`cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B02" --no-report` → 见本次交付回报的 `PASS B02 quotes=N/N` 行与退出码 0。写卡过程中所有引句都是先用同一 `norm()` 函数在本底稿上逐条试命中、确认 HIT 才写入（脚本 `A:\AITEMP\b02_qcheck.py` + 四份候选清单，交付后已清理）；期间试出 7 条 MISS 全部弃用或改写大小写/边界后重测（例如把跨 `β-barrel` 的句子断开、把句首大写改回原文的 `The apo simulations...` / `One of the false positives...`、删掉自造的 `there is a lot of variability...` 与省略号式截短 `accurate enough... with confidence`）。

<!--CSV回填
work_type=论文（方法学/回顾性评估；不含新设计、不含新湿实验）
target=计算设计的配体结合蛋白：NTF2 骨架 digoxigenin 结合体 4 条（DIG10.2/10.3/12/16）+ de novo β-barrel 骨架 DFHBI 结合体 33 条（24 条一代 + 9 条优化代）
backbone_generation=本文不生成骨架；起点全部复用 refs 5、7 的 Rosetta 设计模型与 X 射线结构（4J8T 链A/B、4J9A 链C/F），另建 DIG10.2a/10.3a 模型版对照
computational_filters=显式溶剂全原子 MD（apo+holo 双态）的 10 个动力学指纹：Cα 聚类簇数 NOC、疏水残基 SASA、POVME 腔体积、apo 中体积低于 30 Å3 的帧数、holo 平均腔体积、配体 RMSD、蛋白-配体氢键数、腔内水数、水存活概率、设计残基 χ1；下游接 PCA+k-means（无监督 S/U/F 三簇）与 k-NN/逻辑回归（有监督，5 折交叉验证 + 跨骨架留出）
thresholds=采样长度约 500 ns、3-4 重复（收敛判据为经验结论，原文未给量化阈值）；聚类 RMSD cutoff 1.5 Å；塌陷体积阈值 30 Å3（依据 holo 最小观测 33 Å3）；氢键几何 强 1.2-1.5 Å 且 170-180°、中等 1.5-2.2 Å 且 130-170°；k-means 取 3 簇（平均 silhouette 0.45）；PCA 前 3 主成分解释 80% 方差；逻辑回归 tolerance 1e-4 liblinear、k-NN k=2 或 5 均匀权重欧氏距离；pH 7 赋态、150 mM NaCl、非键截断 10 Å、2 fs + SHAKE、最小化 13,000 cycles；疏水 SASA 约 0.29 nm2 仅为作者 suggested 经验线（未进分类器）
md_used=是-作为事后筛选器/判据来源（本文主用途）：37 设计 × apo+holo × 3-5 重复 × 500-1000 ns，累计 184 µs；不做结构精修、不做自由能计算
qm_used=否（Gaussian 09 仅用于配体几何优化与 GAFF 参数拟合，无电子结构、无反应能/反应坐标计算）
experimental_methods=无新湿实验；全部结局标签复用 refs 5、7 既有表征（结合常数、可溶/CD 折叠判定、酵母表面展示等），9 条优化设计的 Kd 在 Table 1 注中标为基于粗略滴定的估计值
pipeline_counts=37 个设计（4 DIG + 33 β-barrel，Table 1 共 39 个模拟条目）→ 无监督 33 条分入 F 簇 12 / U 簇 6 / S 簇（含 4 条误分、0 条假阴）→ 有监督 joint 37 条 5 折交叉验证 → 跨骨架：β-barrel 训练(70:30) 测 4 条 DIG、反向 DIG 训练测 33 条 β-barrel
hit_rate=回顾性、非前瞻：无监督在 33 条上 88% accuracy；用于 24 条一代设计筛选会得 2 真阳 + 4 假阳（绝对命中率 2/6，富集 ((2/6)/(2/24)) = 4 倍）；有监督逻辑回归 accuracy 0.93±0.10、precision 0.87±0.17、recall 1.0、MCC 0.87±0.16、F1 0.92±0.10；k-NN 0.84±0.16/0.79±0.21/1.0/0.74±0.25/0.87±0.13；β-barrel 训练→DIG(4 条) 测试 acc 1.0；DIG 训练→β-barrel 测试 acc 0.70、precision 0.52、recall 1.0；本文未报告"被 MD 判死的候选里有多少是真阳性"这一反向指标
best_metric=DIG10.3 541 pM（Kd，Table 1；为被复用设计的原值，本文未做亲和力优化；其余 DIG10.2 8.9 nM、mFAP1 0.56 µM、HBI_11 12.8 µM、HBI_32 49.8 µM）
cost_or_stat_note=作者自估：提前剔除 F(12)+U(6) 共 18 条可省约 6 周湿实验（明称 low-bound 估计，他实验室需 2-3 倍）；MD 准备-模拟-分析在并行 GPU 上 <2 周、Kepler 工作流自动化；全文未给 GPU 型号、卡时数或金钱成本任何一项；分类指标为均值±标准差且方差与均值同量级（如 0.84±0.16），交叉验证在 37 条上功效不足
role_in_timeline=位于 Baker 组两代配体结合设计（2013 Tinberg、2018 Dou）之后，与 2023 深度学习漏斗（本库 B09）同期但路线相反：B09 用 AF2 界面 pAE 做大规模下单前闸口（每靶 2M 设计），本文证明 MD 只能在几十条规模做机制层复筛且从未前瞻验证；本项目据此把 MD 定位为末端机制判卷而非召回闸口（CSV 备注 2025 PLACER 等后续工作弃用 MD 作筛选器）
source_pointer=data/literature_cards/fulltext/B02_PMC7532806_text.txt（Europe PMC fullTextXML 抽取得到的 NIHPA 作者手稿版纯文本，70,786 B，SHA256 3729f748fc98876b…）；原始 XML data/literature_cards/fulltext/B02_PMC7532806_fullTextXML.xml；登记底稿 sources/baker.md [B02]（该卡当日记录为 HTTP 500/摘要级，现已升级为全文级，CSV 行未改动）
CSV回填-->
