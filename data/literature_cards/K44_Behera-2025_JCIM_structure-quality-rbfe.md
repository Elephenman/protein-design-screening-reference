# [K44] 把「起始结构质量」当成可操纵变量，量出它对结合自由能误差的影响——AF 模型能用来做化学判定吗

Behera S, Hahn D F, Wilson C J, Marsili S, Tresadern G, Gapsys V, de Groot B L（马普学会 Göttingen 计算生物分子动力学组 + Janssen R&D Beerse/Toledo）
Journal of Chemical Information and Modeling 2025, 65(13): 6927–6938 · DOI 10.1021/acs.jcim.5c00947 · PMID 40583448 · PMCID PMC12264970
开放获取（CC BY 4.0）· 输入文件与 ΔΔG 数值 https://github.com/deGrootLab/Initial_Structure_Modeling_RBFE_2025/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K44**（组：通用方法学；标题字段完整为 Quantification of the Impact of Structure Quality on Predicted Binding Free Energy Accuracy；`期刊=J Chem Inf Model`、`年份=2025`、`DOI=10.1021/acs.jcim.5c00947`；缺口字段：`PMID/PMCID=未记录`、`核验状态=⚠️未核验`、`证据级别=未获正文`、`成本/统计=†仅 Europe PMC 侧列出、Crossref 未复核`、方法类字段全部 `未记录`——本卡把这些填上） |
| batches.tsv 状态 | `state=FULLTEXT`，`fetch_status=OK`，登记全文 `data/literature_cards/fulltext/K44_PMC12264970_text.txt`，记录底稿 `sources/cost-benchmarks.md` |
| 本地全文 | `fulltext/K44_PMC12264970_fullTextXML.xml`（177,626 B）→ 去标签纯文本 `fulltext/K44_PMC12264970_text.txt`（73,391 B，整篇折叠成 1 行），2026-10-20 抓取；文件头身份块与本行标题/DOI 一致（非挂错行那种情况） |
| 身份复核（本卡的增量之一） | 本地全文头同时给出 **PMCID PMC12264970 · PMID 40583448 · DOI 10.1021/acs.jcim.5c00947 · JCIM 65(13):6927-6938 · 上线 2025-06-30 · Received 2025 Apr 28 / Accepted 2025 Jun 24 · CC BY 4.0**，可填进 CSV 空缺的 PMID/PMCID。**注意**：这些编号同出自这份 Europe PMC 抽取，本卡未做 Crossref 独立复核（新的网络抓取本次禁止），故 CSV 的 `⚠️未核验` 只能升格为「本地全文自证一致」，不等于「独立核验通过」 |
| 登记底稿（sources_map.json） | 上面两份 + `sources/cost-benchmarks.md`；后者对本篇只有一行题录（§3.9 第 151 行「结构质量对自由能精度的影响（J Chem Inf Model 2025，DOI 10.1021/acs.jcim.5c00947†）」，无方法与数字），因此本卡全部事实只以纯文本全文为准 |
| 证据级别 | **全文级**（本卡所有英文引句均可在声明的纯文本里逐字命中，见第 9 节） |
| 未取到的部分 | 补充材料（Table S1 的 23 靶/PDB 清单、Figure S1–S15、Section S1/S2）与图内数值。具体缺口：① **AF2/AF3 的 AUE 数值正文未给出**，图注只说写在图 5a 角标；② 分辨率→UE 回归线的**斜率/方程正文未给**；③ 逐靶的 n、AUE、区域 rmsd 只在图 5b–d 与 Fig S15 里 listed，正文未复述。凡涉及这些，本卡明写「正文未给」。 |

## 1. 这篇到底解决什么（一句话＋大白话）

一句话：**过去所有人都说「FEP 算不准是因为起始结构不好」，这篇把结构质量拆成三个能单独动手干预的开关，在 80 对活性悬崖上把每个开关对误差的影响量成了 kcal/mol。**

大白话拆解：相对结合自由能（RBFE/FEP）的「金标准」是 "The gold standard for RBFE calculations is achieved when their accuracy matches experimental results within 1 kcal/mol."，但 "However, real-world applications often yield larger deviations, frequently exceeding 2 kcal/mol."。误差来源一堆（力场、采样、起始结构、实验值本身），作者明说归因困难。他们的设计要点是**一次只动一个变量**：

1. **换分辨率**——不重建结构，直接用数据集里现成的不同分辨率晶体结构（同一对配体的两个复合物常带不同分辨率）；
2. **删晶体水**——同一结构跑两遍，一遍保留晶体水、一遍把所有晶体水删掉，再测试补水工具（SOLVATE/WarPP/WaterDock）能不能替代真晶体水；
3. **换 AI 模型**——干脆不用晶体结构，用 AF2/AF3 预测的 apo 模型，把晶体结构里的配体坐标搬进去，走同一套准备与模拟协议。

对我们最关心的那问（能不能拿 AF 模型做化学判定），这篇给的量化答案是**分层的**：绝对幅度层面 AF 不如晶体结构，作者把它翻译成名义分辨率 "to a structural resolution of >3 Å and 2.8 Å, respectively."（AF2 >3 Å、AF3 2.8 Å）；但方向层面 "both the AF2 and AF3 predicted structures exhibit the ability to predict the sign of the true ΔΔ G with an accuracy of 68 ± 5% and 73 ± 5% (82 ± 3% for CS, n = 80 for AF and n = 160 for CS), respectively."——**幅度不可信、排序仍有信息**，这是本卡对我们最有价值的一条结论形状。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **误差来源天生纠缠，无法干净归因**。原文："Further, it is not easy to decouple the contributing factors, which can be highly interlinked."，并举例 "For example, an issue with force fields or initial structure modeling can lead to sampling problems."。
   → **他们做了什么**：不做多因子回归式的归因，改成**单变量干预 + 配对比较**——固定力场/协议/副本数，只换分辨率档、只开关晶体水、只把 CS 换成 AF；再靠活性悬崖数据集「一对两个结构」的天然配对性质，用配对内差异（分辨率差 ≥0.4 Å 才比较）而不是全库相关来找信号。
   → 代价：结论只在「3D 相似度 ≥0.9、活性差 ≥100 倍的大 ΔΔG 子集」里成立，小差值区域（常规 lead optimization 的主战场）没被测。
2. **实验参考值本身的噪声能吃掉全部判据分辨率**。原文："It has been observed that the root-mean-squared error (RMSE) associated with experimental reproducibility is ∼1 kcal/mol, which sets the natural limit for the achievable accuracy for any affinity prediction method."
   → **他们做了什么**：把数据集按「两个亲和力是否来自同一篇文献」分类分别算 AUE（同来源 1.46 ± 0.22 vs 跨来源 1.87 ± 0.15 kcal/mol，consensus，n=24/56），并把「基准数据必须同源」写进最终建议第 (iv) 条。
   → 代价：同来源子集只有 24 条；他们只是**分类报告**，没有对跨来源数值做噪声校正，也没给出「该给多大方差预算」的可操作公式。
3. **结构质量指标与误差的相关都很弱，多特征组合也救不回来**。原文："All these features show mild correlations with UE."，且 "Further, a partial least-squares regression (PLSR) analysis ( Figure S12 ) show only marginal improvement in correlation compared to using resolution alone."
   → **他们做了什么**：放弃「找一个好的结构质量预测器」，退回两件事——(a) 保留分辨率作为**唯一可用的粗略定量框架** "Figure a provides a rough quantitative framework for estimating the expected UE based on the resolution of a given complex."；(b) 把注意力转向**可干预**的那个特征：结合位点水量 n_Wat，"Besides resolution, the number of water molecules in the binding site (n_Wat) has the largest impact on AUE."，然后用删水/补水的干预实验把它做成因果证据而不是相关。
   → 代价：所谓定量框架只是图 3a 的一条目测回归线，斜率与拟合优度正文未给；这意味着「按分辨率预估误差」这条建议实际不可复算。
4. **删掉晶体水之后，没有工具能可靠地把它补回来**。原文：默认参数下 "Using the default scaling factor of 0.57 for van der Waals radii during water placement, gmx solvate accurately predicted only 29 ± 16% of crystal water positions in the binding site ( Figure b)."，判定口径是 "A predicted water molecule is considered correctly placed if it falls within 1 Å cutoff from a crystal water position in the ligand binding site."
   → **他们做了什么**：三连招——扫 van der Waals scaling factor（"While reducing the scaling factor improved prediction accuracy, it plateaued at 42 ± 13%."）、加短平衡（5 ns 后升到 ∼60%）、换专业工具 SOLVATE/WarPP/WaterDock（"These tools demonstrated superior performance in predicting crystal water positions, with accuracies ranging from 60 to 75% ( Figure c), outperforming gmx solvate ."）。同时给出天花板参照："This is still lower than the ∼80% retention rate of crystal waters after equilibration (horizontal solid lines in Figure c)."
   → 代价：仍不及真晶体水——"they still fall short of the accuracy achieved when using actual crystal water positions"；而且全库加 SOLVATE 的平均改善 "While the overall improvement in accuracy was modest and statistically not significant, with the AUE for all structures decreasing from 1.87 ± 0.1 to 1.71 ± 0.11 kcal/mol"，只有「水少的子集」显著（1.94 ± 0.15 → 1.54 ± 0.16，n=68）。
5. **AF 模型既没水、又是 apo，直接下单会把两个缺陷混在一起**。
   → **他们做了什么**：明确把水的问题先从 AF 结构里剥离出来再评模型本身，"Since water molecules are missing from the predicted structures, SOLVATE was first used on these structures before the final solvation with gmx solvate ."；holo 态不预测而是搬坐标，"The holo states were modeled using these apo structures by first aligning them with the crystal structures (CS) and then transferring the coordinates of the ligands from CS to the predicted structures."；AF 侧只取最优姿态，"The structure with the best ranking was considered for further modeling and simulations."；此后走与晶体结构**完全相同**的准备协议（"These structures were then subjected to the same structure preparation protocol (hydrogen addition, termini capping, etc.) as the CS."）。
   → 代价（他们自己承认）：这等于把晶体结构的构象信息借给了 AF 体系，所以「AF-only」的独立性被削弱；同时 "The conformational differences between the predicted structures and CS could also stem from the fact that the predicted structures are in the apo state"，因此本文**没有**给出「纯 AF 独立预测 + 自主对接姿态」的那一档。
6. **AF 的训练集泄漏，使本文的高分不能当预期表现**——这是这篇最重要的一条自限。原文："However, it is important to note that AF is trained on these crystal structures, and hence the high accuracy obtained does not reflect the true accuracy achievable when applied to an unknown target in a prospective application."；他们也没有做盲测，只补了一句方向性的告诫 "Identifying the key determinants of reliable RBFE results from AI-predicted structures is essential for enabling the confident and widespread adoption of these powerful tools in drug discovery and design."
   → **本文未解决**：没有前瞻盲测、没有「哪些靶上 AF 会崩」的预测因子，只有逐靶波动这一现象描述（thrombin 的螺旋/环错判、Aurora-A 的开合构象错判，而 A4-h 上 AF 反而优于晶体）。
7. **最漂亮的数字来自事后择优（oracle），不可前瞻复制**。他们把「同一对里与实验偏差更小的那个结构」定义为 Best set，其 AUE 1.29 ± 0.16 kcal/mol（n=80）明显好于 consensus（1.75 ± 0.13）与全数据（1.87 ± 0.1）；而删水实验、SOLVATE 相关分析恰恰主要建立在 Best set 及其子集上。
   → **他们做了什么**：三种口径同时报（Best/consensus/all），并在正文保留 consensus 作为主张口径。
   → 代价：**本文未解决**——没有说明「事前怎么判断哪一侧是 Best」，也没给出避开 oracle 的替代协议；读者容易把 Best set 的数字当作可达精度。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **数据集构建**：沿用 Furtmann 等的 3D 活性悬崖集（用同时考虑构象/位置/原子性质的 3D 相似函数配对）。本文**不再自己判悬崖**，只做复筛。
- **自由能引擎**：GROMACS-2022.6 + pmx 的**非平衡 alchemy**（nonequilibrium work + Crooks Fluctuation Theorem 最大似然估计），不是 FEP+。作者用它与 Pérez-Benito 的 FEP+ 结果在 n=30 交集上对表，证明开源管线能达到同级精度。
- **体系准备链**：pdbfixer 补缺失残基/原子 → PropKa 在 pH 7.0、**有配体存在下**给蛋白残基质子化 → 配体走 ACEPREP 网页服务器出质子化态再加人工检查 → ACPYPE/Antechamber 出 GAFF2 + AM1BCC 电荷（Cl/Br 加带正电虚粒子表 σ-hole）→ pmx 出杂合配体与端基 ACE/NME → 蛋白拓扑 AMBER99SB*-ILDN。
- **电荷变化扰动的特殊处理**：double-system-single-box（DSSB）维持电中性，两条体系同盒、COM 沿最长轴排布，加位置约束防止相互作用。
- **水位预测工具**：SOLVATE（hydration 工具）、WarPP、WaterDock（Vina 打分+聚类），对照 GROMACS 自带的 gmx solvate。
- **AI 结构**：AF2 走 ColabFold（apo），AF3 走 AlphaFold Web server；holo 靠「对齐 CS + 搬配体坐标」而非共折叠。
- **统计口径**：所有 AUE、百分比类不确定度用 bootstrap（n_boot=1000）标准误；ΔΔG 报 3 个独立副本的均值。
- **没有用的方法**：QM/MLFF/极化力场（只在引言里作为「尚未有实证收益」的对照被评述）、自由能以外的打分函数、任何湿实验。

### 主工作流

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | Furtmann 2015 的 3D 活性悬崖集 | 按 3D 相似度复筛（上游已用过严标准） | 上游：3D 相似度 cutoff 0.8 + 活性差 100 倍 + 两侧晶体结构 resolution <3 Å；本文只留 3D 相似度 ≥0.9 | 80 组活性悬崖 / 23 个蛋白靶（"The selected data set comprises 80 activity cliffs across 23 distinct protein targets, derived from the collection reported by Furtmann et al."） |
| S2 | 113 条蛋白-配体复合物（PDB ID） | 从 PDB 提取，逐条准备：补缺失、质子化、端基、配体参数化、pmx 杂合 | pH 7.0（PropKa，有配体）；AMBER99SB*-ILDN + GAFF2/AM1BCC；变换方向定为强配体=state A 使实验 ΔΔG 恒为正 | 每对两套起始复合物 CS-1 / CS-2；实验 ΔΔG 跨度 2.7–6.6 kcal/mol（补充图 S1） |
| S3 | CS-1 / CS-2 体系 | TIP3P 溶剂化 + 150 mM Na+/Cl−；能量极小 → NVT 10 ps → NPT 6 ns → 弃前 2.250 ns → 从最后 3.750 ns 均匀取 80 帧 → 逐帧做非平衡变换（电荷守恒 200 ps、电荷变化 500 ps）→ Crooks FT 正反向最大似然 | 每系统全流程独立跑 3 副本；报告值=3 副本平均；DSSB 中两体系间距 ≥30 Å、距盒壁 ≥15 Å、约束力常数 1000 kJ mol⁻¹ nm⁻² | ΔΔG 单值 n=160（CS-1、CS-2 各一遍）与 consensus n=80；AUE 分别为 1.87 ± 0.1 与 1.75 ± 0.13 kcal/mol |
| S4 | 同一批数据 + 结构特征表 | 质量维度①：把误差 UE 对 5 个结构特征做相关（分辨率、配体平均 B 因子、位点 5 Å 内水数 n_Wat、位点 5 Å 内蛋白残基 B 因子、packing score），再做 PLSR | 单特征相关只有 "All these features show mild correlations with UE."；PLSR 相对只用分辨率只有 marginal improvement；配对比较要求 "a minimum difference of 0.4 Å was chosen to avoid noise"；图 3a 分箱用 ±0.1 Å | 结论：分辨率是唯一可用的粗略定量框架，位点水量 n_Wat 是除分辨率外影响最大的特征；回归线斜率正文未给 |
| S5 | 同一批 CS 结构 | 质量维度②：删掉**全部**晶体水，把整个自由能协议重跑一遍 | 分析子集自定义：+CW 时 UE ≤ 1 kcal/mol 且 −CW 使 UE 变化 > 1 kcal/mol | 在 Best set 上 AUE 由 1.29 ± 0.12 恶化到 1.75 ± 0.13 kcal/mol（n=80）；讨论里概括为 "The removal of crystal water reduces the accuracy by ∼0.5 kcal/mol for a set of structures" |
| S6 | 去水后的同一批结构 | 补水替代实验：gmx solvate（扫 scaling factor、含 5 ns 平衡）vs SOLVATE / WarPP / WaterDock，再各跑一遍自由能 | 命中口径 1 Å；gmx solvate 默认 scaling 0.57 命中率 29 ± 16%，调参上限 42 ± 13%，5 ns 平衡后 ∼60%；三工具 60–75%；晶体水自身平衡后保留 ∼80%；SOLVATE 10 Gaussians + ≥5 Å 溶剂壳、WarPP 位点定义为配体原子 6.5 Å 内、WaterDock 用 15 Å 立方盒 | 三工具**都优于** gmx solvate 单独使用，**但都不如**真晶体水；SOLVATE 在自由能精度上优于 WarPP/WaterDock |
| S7 | 全集 | 把 SOLVATE 加进全流程（含 −CW 与 +CW 两种起点）再算一遍 | 判据：全集 AUE 变化是否显著 | 全集 1.87 ± 0.1 → 1.71 ± 0.11 kcal/mol（n=160，作者明写 statistically not significant）；Lower n_Wat 子集 1.94 ± 0.15 → 1.54 ± 0.16 kcal/mol（n=68）；Higher n_Wat 子集不受影响 |
| S8 | 23 个靶的序列 | 质量维度③：AF2/AF3 预测 apo 结构（取 best ranking）→ 对齐 CS 搬入配体坐标 → SOLVATE 预水化 → 与 CS **同一套**准备与模拟协议 | 无额外阈值（不筛置信度、不看 pLDDT/ipTM——本文完全没用 AI 置信度指标做闸口） | AF2、AF3 两套全库 RBFE；"The results, as shown in Figure a, reveal that the free energy accuracy achieved using AF2 and AF3 structures falls short of that obtained with crystal structures (CS)." |
| S9 | S8 的误差 | 把 AI 结构的结果**翻译成结构质量语言**（双向）：①用 AUE 反查分辨率↔UE 关系线，给 AI 模型贴「名义分辨率」；②另立一个方向性判据：只看 ΔΔG 符号对不对 | ①正文未给映射公式，只有图 3a 目测线；②符号判据口径：n=80（AF）与 n=160（CS） | AF2 → >3 Å、AF3 → 2.8 Å（AF2/AF3 的 AUE 数值本身正文未给，仅见图 5a 角标）；符号正确率 AF2 68 ± 5%、AF3 73 ± 5%、CS 82 ± 3%；AF3 一致性优于 AF2 |

**流程骨架值得记住的一点**：他们把「结构质量」变成**可操纵的实验变量**（删水/换分辨率/换模型），而不是给候选结构打一个静态分数；并且给 AI 模型留了两条**互不替代**的评据（幅度 AUE、方向 sign accuracy），最终结论是这两条给出的答案相反。

## 4. 关键数字台账（数值均出自本地全文；出处为正文小节/图注定位）

| 数值 | 含义 | 出处 |
|---|---|---|
| 80 对 / 23 靶 / 113 PDB ID | 活性悬崖对数、蛋白靶数、复合物晶体结构数（唯一结构数 113） | §2.1、§2.2、图 3a 图注 |
| 0.8 · 100 倍 · <3 Å · ≥0.9 | 上游悬崖定义阈值（3D 相似度、活性差、分辨率要求）与本文复筛（相似度） | §2.1 Data Set |
| 2.7 – 6.6 kcal/mol | 实验 RBFE（ΔΔG）跨度 | §2.1，指补充图 S1 |
| ∼1 kcal/mol | 实验重复性 RMSE，即任何亲和力方法可达精度的自然上限 | §1 Introduction |
| 1.75 ± 0.13（n=80） | consensus（两结构取平均）AUE —— 作者主口径 | §3.1、§4 Discussion |
| 1.87 ± 0.1（n=160） | 全部 CS 单值 AUE | §3.1 |
| 1.29 ± 0.16（n=80） | Best set（事后择优）AUE；删水实验的基准即在此口径 | §3.1、§3.3 |
| 1.12 ± 0.18 / 1.56 ± 0.18 vs 1.15 ± 0.17 / 1.64 ± 0.18 | FEP+（Pérez-Benito，n=30 交集）vs 本文（同子集）的 Best/consensus AUE，开源与商用同级 | §3.1，补充图 S6 |
| 1.65 ± 0.14 vs 2.08 ± 0.15（各 n=80） | 高亲和力侧结构 vs 低亲和力侧结构的 AUE | §3.1、图 2a |
| 1.4 ± 0.26（n=24）vs 1.77 ± 0.18（n=56） | 高亲和力子集：参考值同源 vs 异源 | §3.1、图 2b,c |
| 1.46 ± 0.22（n=24）vs 1.87 ± 0.15（n=56） | consensus 口径的同源 vs 异源；另有 1.38 ± 0.25（n=24）为同源高亲和力子集 | §4 Discussion、图 2b |
| ≥0.4 Å / ±0.1 Å | 配对比较的最小分辨率差 / 图 3a 分箱宽度 | 图 3 图注、§3.2 |
| mild / marginal | 5 个结构特征与 UE 的相关强度；PLSR 相对单用分辨率的提升 | §3.2、补充图 S12 |
| 1.29 ± 0.12 → 1.75 ± 0.13（n=80）；∼0.5 kcal/mol | 删晶体水对 Best set AUE 的恶化（讨论里的概括量级） | §3.3（补充图 S14）、§4 |
| UE ≤ 1 且变化 > 1 kcal/mol | 补水分析子集的构造口径 | §3.3 |
| 29 ± 16% / 42 ± 13% / ∼60% / ∼80% / 60–75% | gmx solvate 默认命中率 / 调参上限 / 5 ns 平衡后 / 真晶体水平衡后保留率 / SOLVATE·WarPP·WaterDock 命中率 | §3.3、图 4b,c |
| 1 Å · 0.57 · 10 Gaussians · ≥5 Å · 6.5 Å · 15 Å | 水位命中判定 / gmx solvate 默认 vdW scaling / SOLVATE 参数 / WarPP 位点半径 / WaterDock 盒边长 | §2.3、§3.3 |
| 1.87 ± 0.1 → 1.71 ± 0.11（n=160） | 全库加 SOLVATE：作者判为改善幅度 modest 且不显著 | §3.3、图 4e |
| 1.94 ± 0.15 → 1.54 ± 0.16（n=68） | Lower n_Wat 子集加 SOLVATE 的显著改善 | §3.3、图 4f |
| >3 Å（AF2）/ 2.8 Å（AF3） | AI 结构的名义分辨率（由 AUE 反查关系线得出，正文未给映射公式与 AF 的 AUE 数值） | §3.4、图 5a 图注 |
| 68 ± 5% / 73 ± 5% / 82 ± 3% | ΔΔG 符号正确率：AF2 / AF3 / CS | §3.4 末句 |
| 67% | 引作背景：AF2 结构即使无配体也多呈 holo-like 构象（说明其 apo 标签本身不纯） | §4 Discussion |
| 10 ps / 6 ns / 2.250 ns / 3.750 ns / 80 帧 / 200 ps / 500 ps / 3 副本 / n_boot 1000 | 采样与统计配置（NVT、NPT、丢弃、取帧窗口、两种变换时长、独立副本数、bootstrap 次数） | §2.2 |
| 15 Å / 150 mM / 30 Å / 1000 kJ mol⁻¹ nm⁻² / 11 Å | 盒壁间距 / 盐浓度 / DSSB 两体系间距 / 位置约束力常数 / PME 与 vdW switch 截断 | §2.2 |
| 0.25 – 0.5 kcal/mol | 图 5b–d 逐靶 AUE 的 bootstrap 标准误范围（即逐靶差异的噪声水平） | 图 5 图注 |

## 5. 结论——作者说了什么

1. **结构质量与误差之间可以建定量映射**：分辨率是那条可用的线（"The relationship between resolution and UE provides a quantitative basis for assessing the potential reliability of RBFE predictions based on the resolution of available crystal structures ( Figure a)."），但它是**弱相关的粗略框架**，不是精确公式。
2. **晶体水是决定性因素，而不是次要细节**：删掉全部晶体水使 Best set 的 AUE 从 1.29 ± 0.12 升到 1.75 ± 0.13 kcal/mol（讨论里概括为 ∼0.5 kcal/mol 的恶化）；位点水分子数 n_Wat 是除分辨率外最能区分准/不准的结构特征。
3. **SOLVATE 值得默认加进协议**：全库平均改善不显著（1.87 → 1.71），但「晶体水少」的子集改善显著（1.94 ± 0.15 → 1.54 ± 0.16，n=68），作者据此给出 "the inclusion of SOLVATE in the free energy simulation protocol is strongly recommended to enhance the reliability of binding affinity predictions."（该句在讨论段，本卡未作逐字引用，逐字口径见第 9 节声明的引句底稿）。
4. **AI 预测结构可用于 RBFE，但精度低于晶体结构**：AF2/AF3 的 AUE 劣于 CS（数值仅在图 5a 角标）；作者把它们折算为名义分辨率 "to a structural resolution of >3 Å and 2.8 Å, respectively."；AF3 稳定优于 AF2；个别靶（A4-h）上 AI 结构反而比晶体结构更准（"In some cases, like A4-h ( Figure d), the predicted structures are in excellent agreement with CS and have lower AUE than CS."）。
5. **方向性另有评价，且与幅度解耦**：AF2/AF3 判 ΔΔG 符号的正确率 68 ± 5% / 73 ± 5%，晶体结构 82 ± 3%（"both the AF2 and AF3 predicted structures exhibit the ability to predict the sign of the true ΔΔ G with an accuracy of 68 ± 5% and 73 ± 5% (82 ± 3% for CS, n = 80 for AF and n = 160 for CS), respectively."）。
6. **四条 best practice**（结论段原序）：用结合最强配体的蛋白结构；工作流里加 SOLVATE（尤其 AI 结构无水时）；"(iii) select a lower resolution crystal structure if available"；基准实验值取自同一来源。
7. **作者自限**：AI 结构的这些数字不能当前瞻表现（"However, it is important to note that AF is trained on these crystal structures, and hence the high accuracy obtained does not reflect the true accuracy achievable when applied to an unknown target in a prospective application."）；名义分辨率是本数据集特定规模的产物（"It is important to note that these values are derived from the current data set, which includes 23 protein targets and 80 ligand transformations. These results may vary when applied to a larger data set."）；跨靶波动大需要谨慎。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **「能不能拿 AF 模型做化学判定」的正确问法被这篇拆开了**：幅度（AUE，能给 kcal/mol）与方向（sign accuracy，只能给百分比排序）是两套结论，而且它们可以**互相矛盾**——AF 在本文里幅度上不达标、方向上仍有 68–73% 信息量。→ 对我们：任何用 AF 模型下的化学结论都必须写清自己主张的是哪一层；主张「谁更可能催化/谁更可能结合」与主张「结合能是多少 kcal/mol」不是同一件事，不能共用一张合格表。
2. **「名义分辨率」是一次量纲互换，且是循环的**：先承认结构特征与误差只有弱相关（mild / marginal），再拿误差反查那条弱回归线给 AI 模型贴分辨率标签。它作为沟通语言可以，作为**闸口**不行（用它做筛选等于用判据的输出当判据的输入）。→ 我们若用 pLDDT/ipTM/pAE 给「化学结论的可信档位」命名，同样会掉进这个循环，必须显式声明它是**读数**不是**资格**。
3. **本文最有迁移价值的不是数字而是这个失败模式清单**：AF 的错误形态是**局部二级结构与开合状态的错**（thrombin 两段螺旋/环、Aurora-A 开-闭构象），这类错误**不会体现在任何全局置信度指标上**（正文完全没用 pLDDT/ipTM 做闸口），只能在「残基层局部对照晶体结构」这一层被看见。→ 对我们：判定 AF 模型能否承载某个化学结论时，要看**催化几何所在的那几段局部构象**是否与任何实验/高置信参照一致，全局置信度分布不能替代局部核查。
4. **AF 体系进 MD 之前，「补水」不是可选项**：作者专门先跑 SOLVATE 再 gmx solvate，理由就是预测结构没有水。→ 对我们：AF + MD 的机制层判定，如果没做保守水/配位水的显式重建，其误差量级在本篇的坐标系里属于「已知会额外贡献 ∼0.5 kcal/mol 级别」的未控项；至少要报告做没做。
5. **标签噪声能吃掉判据分辨率**：同源 vs 跨来源的 AUE 差（1.46 ± 0.22 vs 1.87 ± 0.15）与他们试图量化的结构质量效应**同数量级**。→ 对我们：建真值/参考面板时「同一篇文献、同一 assay」应作为硬约束，而且我们要像他们一样把这个约束做成一个**可读的数字**，而不是写一句「数据要干净」。
6. **最值得抄的实验设计**：单变量干预 + 配对同源体系（同一对配体、两个结构、同一协议、3 副本、bootstrap 误差）。这比「给一批结构打分看哪个指标与结局相关」强得多，因为后者在他们的数据里已经证明只能得到 mild correlation。→ 我们该做的不是再找一个静态打分闸口，而是造一个「CS vs AF、±补水、±删水」的 2×2 对照，让误差被**做出来的**而不是被**回归出来的**。
7. **一条反向警戒**：他们最常被引用的漂亮数字（1.29 kcal/mol）来自事后择优。我们引用任何「某判据下误差是 X」时，必须先确认 X 不是在同一份数据上「谁更接近真值就选谁」挑出来的。

## 7. 局限与失败（作者的 + 我们读出的）

**作者明写的**
- 名义分辨率只在本数据集规模上成立，数据集更大时可能变（见第 5.7 条两条原句）。
- AF 训练在同源晶体结构上，本文高分不代表前瞻表现。
- 跨靶表现不一致（thrombin/HSP90-A 差、A4-h 反超），作者称 "the variability in performance observed across different protein targets" 需要谨慎与进一步研究；本文未给出「何时可信」的判据，明写这是待解问题。
- 全库加 SOLVATE 的改善 "modest and statistically not significant"；作者没有把它说成普适收益。

**我们读出的、作者没说的**
1. **AF 的 AUE 数值没进正文**（只在图 5a 角标），逐靶 n 与 rmsd 也只在图里 listed → 本文对 AF 的定量结论**无法从正文复算**，只能靠名义分辨率这一转译值；这对一篇以「量化」为卖点的文章是明显的证据缺口。
2. **holo 建模靠对齐晶体结构搬配体坐标** → 所谓「用 AF 做 RBFE」在这篇里其实是「AF 蛋白骨架 + CS 配体姿态 + CS 参考系的对齐」的混合体系。**姿态误差被排除在考察范围之外**，因此不能拿本文回答「没有晶体结构时能不能用 AF/对接姿态做 FEP」——那恰恰是前瞻场景里最难的一环。
3. **数据集是极端子集**：3D 相似度 ≥0.9、活性差 ≥100 倍、实验 ΔΔG 2.7–6.6 kcal/mol —— 这是「大信号」区域。符号正确率 68–73% 是在 ΔΔG 很大的样本上算的，**不能外推到 ΔΔG 接近 0 的常规优化决策**（那里正负号本身就常被实验噪声翻转）。他们自己在引言里就指出「预测与实验的偏差在实验值更大时更高」，方向性结论与大 ΔΔG 子集之间还有这层未被讨论的耦合。
4. **Best set 是 oracle**，且删水、补水的机制性结论都建立在它及其子集上（详见第 2.7 条），所以「水很重要」这条结论的**效应量**带有择优偏差；不过它的**方向**在 consensus/all 口径下依然存在，这一点无需 oracle。
5. **本文没有置信度层级的分析**（这是**搜过的缺失**，不是没找）：在归一化后的 73,391 字符纯文本里做大小写不敏感计数，pLDDT、pTM、ipTM、PAE/pAE、predicted aligned error 均为 **0 次出现**；confidence 仅 3 次，两处指「对自由能计算结果的信心」这一日常用法、一处在参考文献标题（high-confidence activity cliffs），没有一处是 AF 的每残基置信度。→ 所以**本文不能用来回答「AF 模型的置信度指标能否预测 RBFE 误差」**——它既不支持也不反对我们拿 pLDDT/pAE 做化学判定资格门，这条仍是我们的开放问题，不许引用本文来关闭。
6. **体系域外，而且域外程度无法完全核对**：本文用的是经典力场组合（AMBER99SB*-ILDN 蛋白 + GAFF2/AM1BCC 配体 + TIP3P），正文未讨论金属中心的特殊参数化（全文 metal 一词只出现在参考文献标题里，属已搜过的缺失）；但**逐靶/逐配体清单在 Table S1（本地未取）**，所以「配体里有没有核酸类似物/多价金属酶」这一点对本卡是**未核**而非「没有」。我们的酶设计/聚合酶场景（Mg²⁺/Mn²⁺ 依赖、磷酸底物、电荷变化扰动占比更高）落在本文覆盖范围之外的概率很大，因此**不能把本文的误差量级当成我们的预算**。
7. **无前瞻、无湿实验**：所有「实验值」都是从文献里取的既有数据（含同源/异源噪声问题），本文的证据链终点是「与已发表数值对表」，不是新测量。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **「幅度 vs 方向」双层报告口径**（本库判定表可直接加一列）：任何基于 AF 模型的化学结论，分别登记 `sign/rank 正确率`（本数据集实测 CS 82 ± 3%、AF3 73 ± 5%、AF2 68 ± 5% 只作为**该方法学层级的量级参照**，不是我们的预期值）与 `误差幅度`。主张只许引用对应那一层的数字。
2. **把结构质量做成可操纵变量**：对我们的机制层判定，应设计「同一体系 × {CS 参照 / AF 模型} × {补水 / 不补水}」的对照，让「AF 能不能用」变成一个有 AUE/位移分布可比的实验，而不是继续争论置信度分数。这是本篇方法层最值得抄的一点。
3. **AF + MD 的前置项清单**：保守水重建（SOLVATE 一类）+ 端基/质子化（PropKa 类）+ 局部构象核查（对照任何实验参照，检查催化几何所在片段而非整体）。三项都应在 `run.md` 里显式记录做/没做。
4. **标签纪律**：真值面板按「同一来源、同一 assay」优先，并把同源 vs 跨源的读数差做成一个可见数字（他们的 1.46 ± 0.22 vs 1.87 ± 0.15 kcal/mol 是「标签噪声与待测效应同量级」的具体案例）。
5. **oracle 自检**：凡出现「多结构/多模型里取与参照更接近的那个」的报告口径，必须同时给出 consensus 与 all 两个口径，并禁止把 oracle 口径用于任何前瞻性主张。
6. **误差预算的量级感**（仅作定性参照，不作阈值）：在化学判定的能量语言里，结构质量类误差是 **∼0.5 kcal/mol 一个台阶**（删晶体水）、**∼1 kcal/mol 是实验重复性地板**。这提示我们：任何小于 1 kcal/mol 的判定差，在本文坐标系里都落在噪声内。

**不可迁移（为什么不能照搬）**

1. **不许把本文任何 AUE/符号率当我们的成功率或阈值**。那是小分子 RBFE 在 23 个可溶药靶、大 ΔΔG 悬崖子集上的读数，且部分建立在事后择优口径上。本库判定标准禁止把 binder/FEP 的能量阈值当酶活闸口；同理，1.29/1.75/68%/73% 这些数字**不构成**「AF 模型对我们的化学判定可用」的概率依据。
2. **名义分辨率 >3 Å / 2.8 Å 不能当成 AF 模型的质量等级**，更不能用它去换算 pLDDT/ipTM 该取多少。它是本数据集弱回归线的反查值，作者自己声明换数据集可能变。
3. **本文没有回答「置信度指标能否预测能量误差」**（全文未用 pLDDT/pAE/ipTM），所以它既不支持也不反对我们拿 AF 置信度做化学判定资格门——这条仍然是我们的开放问题，不许引用本文来关闭。
4. **本文的 holo 体系有晶体配体姿态兜底**；我们的场景（无复合物结构的天然/设计蛋白 + 底物在溶液里）没有这个兜底，误差来源比本文更多，不能按本文量级乐观估计。
5. **不是 de novo/蛋白-蛋白界面体系**：binder 侧的 pAE_interaction<10、复合物 RMSD<5 Å 一类闸口（B09）与本篇的 ΔΔG/AUE 语言**不同量纲、不同判定对象**，两者不可互换、不可互相校准；本篇也不能用来给「结构预测自洽性判据」的能量意义背书。
6. **力场与化学域外**：GAFF2/AM1BCC + TIP3P 对小分子药物化学适用，对酶设计/核苷酸/多价金属体系需另行验证，本文的误差量级不自动成立。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K44_PMC12264970_text.txt

- 本地纯文本 `fulltext/K44_PMC12264970_text.txt`（73,391 B）由同目录 `K44_PMC12264970_fullTextXML.xml`（177,626 B，Europe PMC fullTextXML，2026-10-20 抓取）经标签剥离 + 实体解码生成；本卡引句一律照这份纯文本复制，抽取版里图号引用（Fig./Figure 编号）被标签剥离留成空格，故引句中出现的 " Figure a " 这类残缺就是底稿原样，逐字比对以它为准。
- 该编号在 `sources_map.json` 里另登记 `sources/cost-benchmarks.md`；本篇在其中的登记形态只有一行题录（`sources/cost-benchmarks.md:151`，§3.9「其他已定位但本次未展开精读的判据类文献」，写作中文描述 + DOI + †未复核标记），没有方法、阈值或数字，故本卡不从它取任何事实，只作对照。
- 正文缺口（不是本卡省略，是原文未给）：AF2/AF3 的 AUE 数值（仅图 5a 角标）、分辨率↔UE 回归线的斜率/方程（仅图 3a）、逐靶 n 与区域 rmsd（图 5b–d 与 Fig S15 listed）、Table S1 的 23 靶与 PDB 清单。这些在第 0/4/7 节均已明写为「正文未给」。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/成本统计`；第 5 节第 4–5 条 ↔ `实验命中率/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K44" --no-report` 把卡内所有被直双引号包住、无中日韩字符、≥20 字符且 ≥12 个字母的片段，在声明的引句底稿里做逐字查找（两侧同用 `litcards_text.norm`：NFC + 实体解码 + 弯引号/破折号归一 + 空白折叠）。结果为 `PASS K44 quotes=N/N`、退出码 0（N 见交付回报）。
- 未核验项（如实声明）：本卡只保证「引句逐字来自底稿」与「数字能在底稿中搜到」，**不保证**作者原始作图数据与补充材料内容一致；第 6、7、8 节的判断为本项目推断，标在「以下为推断」之后。

<!--CSV回填
work_type=论文（方法学/基准研究，J. Chem. Inf. Model. 2025, 65(13):6927-6938）
target=23 个可溶药靶上的 80 组 3D 活性悬崖对（含 thrombin、Aurora-A、HSP90-A、 leukotriene A4 hydrolase 等），113 条蛋白-配体晶体结构 + 各自 AF2/AF3 apo 预测模型
backbone_generation=不适用（不生成蛋白骨架）；起始结构链路为 pdbfixer 补缺失 + PropKa pH 7.0（有配体）质子化 + pmx 端基 ACE/NME 与杂合配体 + GAFF2/AM1BCC（ACEPREP 定质子化态）；AI 分支为 ColabFold(AF2)/AlphaFold Web server(AF3) 取 best ranking 的 apo 模型，再对齐晶体结构搬入配体坐标得 holo
computational_filters=不做筛选器，做误差归因：UE 对分辨率、配体平均 B 因子、位点 5 Å 内水分子数 n_Wat、位点 5 Å 蛋白残基 B 因子、packing score 的相关性 + PLSR 组合；水位命中率（与晶体水 1 Å 内记命中）；ΔΔG 符号正确率（方向性判据，独立于幅度）；名义分辨率折算
thresholds=复筛 3D 相似度 ≥0.9（上游 0.8 + 活性差 100 倍 + 双方 resolution <3 Å）；配对比较最小分辨率差 0.4 Å；图 3a 分箱 ±0.1 Å；水位命中 1 Å；gmx solvate 默认 vdW scaling 0.57；补水分析子集口径 +CW 时 UE ≤ 1 kcal/mol 且 −CW 变化 > 1 kcal/mol；NVT 10 ps + NPT 6 ns、弃 2.250 ns、取 80 帧、变换 200 ps（电荷守恒）/500 ps（电荷变化）、3 副本、n_boot=1000；SOLVATE 10 Gaussians 与 ≥5 Å 溶剂壳、WarPP 位点 6.5 Å、WaterDock 盒 15 Å；DSSB 间距 30 Å/15 Å、约束 1000 kJ mol^-1 nm^-2
md_used=是（核心手段而非事后机理：GROMACS 2022.6 显式溶剂 MD（TIP3P、150 mM、PME 11 Å、LINCS、Beutler 软核）产出构象系综，供非平衡 alchemy 自由能积分；结构质量三开关（分辨率/删晶体水/换 AF 模型）都通过重跑 MD 来测量）
qm_used=否（配体电荷为 AM1BCC 半经验推导 + ACEPREP 质子化态 + 人工检查，属参数化不是 QM 计算；全文无 QM/MM、无 FEP 之上的电子结构层）
experimental_methods=无湿实验；用文献既有亲和力数据作参考（按同源/跨来源分类审计实验噪声），无新测量、无前瞻盲测
pipeline_counts=Furtmann 3D 悬崖集 → 复筛后 80 对 / 23 靶 / 113 PDB ID → 每对两套起始复合物 CS-1、CS-2（n=160 单值、n=80 consensus）→ 同一数据集再各跑一遍 −CW、gmx solvate/SOLVATE/WarPP/WaterDock 补水、AF2、AF3 全协议（每系统 ×3 副本）；水位命中率分析用一个自定义子集（+CW UE ≤1 且 −CW 变化 >1 kcal/mol）
hit_rate=本文不用命中率口径；替代读数：consensus AUE 1.75 ± 0.13 kcal/mol（n=80）、全 CS 1.87 ± 0.1（n=160）、Best set 1.29 ± 0.16（n=80，事后择优）；ΔΔG 符号正确率 CS 82 ± 3%、AF3 73 ± 5%、AF2 68 ± 5%；加水 SOLVATE 全库不显著（1.87 → 1.71），Lower n_Wat 子集 1.94 ± 0.15 → 1.54 ± 0.16（n=68）
best_metric=未记录（本文不报 Kd/活性绝对值，只报误差：最低 AUE 为 Best set 1.29 ± 0.16 kcal/mol，属事后择优口径；同来源高亲和力子集 1.38 ± 0.25 kcal/mol，n=24）
cost_or_stat_note=正文未给机时/GPU 与单对成本（只有采样配置：3 副本全流程、6 ns NPT、80 帧 × 正反 200/500 ps）；不确定度全部为 bootstrap 标准误（n_boot=1000），图 5b–d 逐靶 AUE 标准误范围 0.25–0.5 kcal/mol；实验重复性地板 ∼1 kcal/mol；删晶体水的代价 ∼0.5 kcal/mol；FEP+ 对照子集 n=30
role_in_timeline=药物化学 FEP 一侧第一次把「起始结构质量」拆成三个可单变量干预的开关（分辨率 / 晶体水 / AI 预测模型）并量成 kcal/mol 的论文；给「AF 模型能否用于结合自由能判定」提供了幅度与方向分离的量化答案（名义分辨率 AF2 >3 Å、AF3 2.8 Å；符号正确率 68%/73% vs CS 82%），同时自陈 AF 训练泄漏使这些数字不代表前瞻表现。与 binder 侧 B09（pAE_interaction 闸口）互为镜像：那侧量「会不会按设计结合」，这侧量「能量差值算得多准」
source_pointer=data/literature_cards/fulltext/K44_PMC12264970_text.txt（由 K44_PMC12264970_fullTextXML.xml 抽取，Europe PMC PMC12264970，DOI 10.1021/acs.jcim.5c00947，PMID 40583448）；输入文件与 ΔΔG 数值 https://github.com/deGrootLab/Initial_Structure_Modeling_RBFE_2025/；登记底稿 sources/cost-benchmarks.md 无本篇条目
CSV回填-->

<!--CSV回填
work_type=论文
target=待填
backbone_generation=待填
computational_filters=待填
thresholds=待填
md_used=待填
qm_used=待填
experimental_methods=待填
pipeline_counts=待填
hit_rate=待填
best_metric=待填
cost_or_stat_note=待填
role_in_timeline=待填
source_pointer=data/literature_cards/fulltext/K44_PMC12264970_text.txt
CSV回填-->
