# [K48] Aggrescan4D：把 pH 当成聚集预测的第四维——序列+结构聚集倾向、柔性、突变建议打包成一个免费网页工具（工具/方法综述）

Zalewski M, Iglesias V, Bárcenas O, Ventura S, Kmiecik S（华沙大学 Kmiecik 组 + 巴塞罗那自治大学 Ventura 组）
Protein Science 2024, 33(10):e5180 · DOI 10.1002/pro.5180 · PMID 39324697 · PMCID PMC11425640
开放获取（CC BY-NC-ND 4.0，允许非商业、不可改写）· 服务器 https://biocomp.chem.uw.edu.pl/a4d/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K48**（组：通用方法学 · 文献类型=方法 · 设计对象列=聚集/多分散失败模式的判据 · 计算筛选判据列=序列/结构聚集倾向评分） |
| 本地全文 | `fulltext/K48_PMC11425640_fullTextXML.xml`（inventory.json 记 fetch_channel=epmc_search_then_fulltext，即 Europe PMC 按 DOI 定位 PMC11425640 后取 fullTextXML，文件名按 PMC 号）→ 去标签纯文本 `fulltext/K48_PMC11425640_text.txt`（71,742 B，单行；本卡唯一引句底稿） |
| 身份核验 | 底稿开头题录自证：期刊 Protein Science、DOI 10.1002/pro.5180、PMCID PMC11425640、PMID 39324697、标题与 CSV 行标题逐字符一致（CSV 标题里的连字符是 U+2010，本卡不照抄、也不引带它的句子）→ **判定为同一篇，可以引用** |
| 只读参考 | `sources/cost-benchmarks.md` §六 第 2 行（包涵体/不溶）：本 DOI 与 CamSol（10.1093/bib/bbad004）并列作为该失败模式的候选计算判据，当时的可靠度记为 部分证据、并注明 未见其用于从头设计命中率提升的前瞻对照 |
| 证据级别 | **全文级**（本卡 65 段英文引句全部在登记底稿里逐字命中，见 §9） |
| CSV 旧值提示 | 本卡写完时 CSV 行 证据级别 列仍是 摘要级（旧值）；该列不在 14 键回填范围内，**2026-11-07 已按本卡 §0 重刷为 `FULLTEXT｜全文级`**（改动账 `data/interim/table_field_fixes_2026-11-07.json`） |
| 与全文不符处 | CSV 年份列曾记 2025，全文题录为 2024（在线 2024-09-26，刊期 2024 年 10 月卷 33 期 10）；**2026-11-07 已更正为 2024**（依据见 `scripts/table_field_fixes.json`）。CSV 的 第一或通讯作者/PMID/候选数递减/命中率/阈值 等列仍为 未记录（本次未展开精读）。以全文为准，逐条记入 §7 |
| 未取到的部分 | 图 1–7 里的数值（散点图逐点、RMSF 曲线、PDB 6YG9 各 pH 打分的具体读数）、公式 (1) 中 α β γ δ 四个参数的实际取值、A4D 原始论文（Nucleic Acids Res 2024, DOI 10.1093/nar/gkae382）的完整验证集。凡用到这些的地方本卡明写 原文未给阈值 或 本文未给出 |

## 1. 这篇到底解决什么（一句话）

Aggrescan 系列的结构版（A3D）加了一个新变量：**pH**。它把每个残基的聚集倾向分数改成随 pH 走（借 SolupHred 的 pH 依赖亲脂度标度 + pKa-ANI 的三维 pKa 估算），再套上 FoldX 稳定性、CABS-flex 柔性采样、两种自动突变建议（带电荷替换 / PAM250 进化保守替换）和一个 12 个物种约 16 万条蛋白的预计算库——目的是让人**在下单做突变之前，就用手上的结构预测出这个蛋白在某个 pH 下哪里会聚、改哪几个残基能变可溶**，作者自己的定位是："Building upon its predecessor, Aggrescan3D (A3D), A4D has undergone numerous enhancements aimed at assisting the improvement of protein solubility."

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **纯序列工具在折叠蛋白上会指错地方**（这是整条 Aggrescan 线的立足点）。作者说序列级工具快而便宜、适合伸展态与无序蛋白："These tools are particularly useful for proteins in extended conformations or intrinsically disordered proteins (IDPs), where exposed aggregation prone regions (APRs) are directly related to the sequence (Belli et al., 2011 )." 但对已折叠蛋白，埋在里面或参与相互作用的疏水片段并不致聚。 **应对**：走结构路线——A3D/A4D 只看溶剂可及的残基，并把球内（默认半径 10 Å）邻居按 Cα 距离衰减累加成 STAP（结构聚集倾向区），"Agg i represents the aggregation propensity of the central residue i , and RSA i denotes its relative surface area exposed to solvent." **仍留下的代价**：必须有三维结构才能算，于是把风险转嫁到结构质量上（见第 2.2 条）。
2. **AlphaFold 结构反而带来新型假信号**。AlphaFold 库里的模型常带一长段实验结构里不存在的伸展无序区："Structures obtained from the AlphaFold database (Jumper et al., 2021 ) often present elongated, disordered regions that are not typically observed in experimentally resolved structures." 这些尾巴会缠在球状核周围造出假表面，"These regions tend to congregate around the globular core, introducing potential surface features that could mislead the interpretation of STAPs (Ruff & Pappu, 2021 ) and undermine the accuracy of A4D predictions"。 **应对**：内置 AlphaCutter 选项，"AlphaCutter employs DSSP to pinpoint long loops and helices, followed by the calculation of a contact map."，"Additionally, it applies an AlphaFold pLDDT threshold to refine the domains further."，并对 AlphaFold 来源结构推荐开启。 **代价**：pLDDT 具体阈值本文未给数字；且默认是关的（"By default, this option is deactivated."）；切掉 IDR 之后，真正靠无序区聚集的体系就失去了这条信息——本文未讨论这个矛盾。
3. **pH 依赖需要逐个残基的 pKa，但精氨酸算不准**。作者明写："Due to limitations on satisfactory 3D pKa estimation for Arginine, its score is considered constant"。 **应对**：只让 Asp/Glu/Lys/His/Tyr 五种残基的分数随 pH 变——"Regarding pH calculations, A4D considers the pH score variation of aspartic and glutamic acids, lysine, histidine and tyrosine (see Figure 2b ), while the score of other amino acids remains unchanged."，精氨酸与其余残基冻结。 **代价**：精氨酸恰恰是抗体 CDR 与蛋白表面聚集热点上常见的高电荷残基，它的 pH 响应在 A4D 里等于不存在；本文没有量化这一近似带来的误差。
4. **极端 pH 下静态结构假设本身崩掉**。溶菌酶的实测数据显示："When analyzing the lysozyme data, we observe that A4D accurately models most of the pH range (pH 3.5-9.5) but fails for moderately basic pH values (10 and above)." 原因是碱催生的部分展开："This discrepancy is attributed to the partial unfolding of lysozyme at such pH values (Petersen et al., 2004 ), which is why the A4D server limits pH prediction range to values between 4.0 and 9.0." **应对**：**放弃该类体系**——直接把服务器可算的 pH 域砍到 4.0–9.0（共 11 个点，步长 0.5），而不是去补展开态建模。 **代价**：内体/溶酶体（pH<5）与碱性制剂（pH>9）这两个我们关心的区间正好在门外；作者也没说 4.0 那端为什么没出问题。
5. **方向对了、幅度不对，作者承认是已知缺陷**。RNase Sa 上："Finally, in the case of RNase Sa, the predicted and experimental values agree, showing a decrease in aggregation with an increase in pH."，紧接着 "However, the rate of change differs."，作者把它归为："This is a known limitation in the algorithm for some protein case studies and may result from the limitations in A4D's aggregation modeling capabilities or differences in the sensitivity of the experimental value reported."——这是二选一的解释，没有实验把它们分开。**本文未解决**。
6. **强功能之间互斥，一次跑不出全套**。选项表里 pH 计算那一行写着 "Yes /No Cannot be used alongside Dynamic mode and Improve/Enhance protein stability options."，动态模式 "It's important to note that the Dynamic mode does not support pH calculations or automatic mutations (see Figure 1 )."，自动突变 "It's noteworthy that automated mutations are not compatible with pH calculations and Dynamic mode (see Figure 1 )." **应对**：把三者做成互斥开关，让用户自己串。 **代价**：本文没有给出串联协议（先算 pH 再算突变要怎么对齐分数刻度），而且 pH 模式与 classical 模式的分数本来就不同轨——"A4D reports different numerical values for the aggregation score at neutral pH compared to the"（原句此后紧接一个带引号的 classical 一词，故本卡不整句引用）——跨模式比大小没有意义，这条限制只在这里出现一次，正文没有给出换算办法。
7. **突变效应的验证集只有十几条**。作者用的是 Brockwell 实验室在体进化 MEDI1912 的旧数据："The authors developed 18 different variants"，二值化口径是："We categorized the mutants based on their aggregation propensity considered positives (9 variants) or negatives (8 variants) those that increased or decreased the retention time with respect to the midpoint."（HP-SEC 保留时间相对中点）。 **应对**：不报单一命中率，改报六个混淆矩阵指标（§4）。 **代价（本文未解决）**：正文说 18 个变体、表 2 的表头写 19 mutants，正负类相加只有 17，三个数对不上，本文未解释；n≈17–19 时 specificity 0.25 与 0.75 的差距谈不上稳健；而且这批数据是随机突变产生的（作者承认 "the lack of control over the mutation sites caused these less aggregating variants to impact protein functionality"），拿它评测 只改面不改功能 的工具，方向性偏置没有量化。

## 3. 方法与工作流程（照 A4D 的实际流水线；输入 → 操作 → 判据/阈值 → 输出规模）

工具箱（以及每个组件在这条流水线里干什么）：

- **Aggrescan 的 in vivo 聚集倾向标度**（Conchillo-Solé 2007）：给每种氨基酸一个倾向分值，非 pH 模式（Static/Dynamic）就用它当 Agg_i。原文说这一标度来自体内数据、擅长抓短的促聚片段（该句含 U+2010 连字符，本卡不作整句引用）。
- **球内距离衰减打分式（公式 1）**：中心残基项 + 半径内邻居项按 Cα 距离 e^-δ·dist 衰减、随溶剂可及面积 RSA 放大；参数 α β γ δ 的取值本文未给（只说按 A3D 原文设定）。
- **pH 依赖亲脂度标度（SolupHred）+ 3D pKa（pKa-ANI）**：替代 Agg_i，让分数随 pH 走。
- **FoldX 力场**：输入结构优化 + 突变体的稳定性增量 ΔΔG（本文把它当能量项用，不是当筛选主判据）。
- **CABS-flex**：粗粒度柔性采样（不是全原子显式溶剂 MD）。
- **AlphaCutter**：切 AlphaFold 结构的非球状尾巴（DSSP + 接触图 + pLDDT 阈值）。
- **PAM250 矩阵**：给 进化保守替换 模式挑氨基酸替换对。
- **实验侧真值**：本文**没做**任何湿实验，全部用他人数据（HSA/BSA/溶菌酶/RNase Sa 的 pH 聚集曲线 + MEDI1912 的 HP-SEC 保留时间）。

### A. 单次预测的工作流（服务器默认路径）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 | PDB/CIF 上传，或直接给 PDB / UniProt ID（自动取 AlphaFold 结构）；RESTful 亦可提交 | 结构入库；若来源是 AlphaFold，作者推荐开 'Analysis of the globular regions' | AlphaCutter：DSSP 判长环/螺旋 + 接触图 + AlphaFold pLDDT 阈值（**具体 pLDDT 数值：原文未给阈值**；该选项默认关闭） | 一份去掉非球状尾巴的 PDB |
| 2 | 上一步结构 | FoldX 优化（'Stability calculations'，默认 Yes） | 无阈值；但 "To perform any mutation, or dynamic mode analysis, this feature has to be enabled." | 能量弛豫后的结构（突变与动态模式的前置件） |
| 3 | 优化后结构 | 对每个残基 i：取以 Cα 为中心、半径 R（默认 10 Å，可 5 Å）的球，按公式 (1) 累加自身项与邻居项 | "For most applications, the A4D score above 0 indicates potential aggregation, but scores higher than 0.5 are more likely to indicate residues that are critical to aggregation processes." | 每残基 A4D 分数表 + 结构上色（蓝=可溶、红=聚集、白=中性）；R=10 Å 看整体、R=5 Å 看单个残基 |
| 4 | 同上（可选 pH 模式） | 用 pKa-ANI 的 3D pKa + SolupHred pH 依赖亲脂度标度替换 Agg_i，逐 pH 重算 | 扫 11 个 pH（4→9，步长 0.5）；只有 Asp/Glu/Lys/His/Tyr 分数变化，Arg 与其余 15 种视为常数；服务器 pH 上限因溶菌酶失败被截到 4.0–9.0 | "If the 'pH calculations' option is enabled, A4D facilitates aggregation predictions across a range of 11 pH values from 4 to 9 with increments of 0.5." 输出每个 pH 的平均分与最大值 |
| 5 | 上一步结果 | 选汇总指标 | "Through performance analysis, we determined that for globular proteins, the maximum value, and for IDPs, the average value, better aligns with experimental observations" ——**球状用 max、无序用 avg**；服务器会自动识别并推荐 | 一条 聚集倾向 vs pH 的曲线（供与实验比斜率） |
| 6 | 可选：柔性 | CABS-flex 采样，FoldX 优化后的结构当起点，产出全原子模型集 | "For each of these models, the A4D score is calculated using the same method as in the static mode, and models are ranked from highest to lowest aggregation score, including the original structure." 无阈值，只排序；与 pH/自动突变互斥 | 模型集 + 每模型分数 + RMSF 图（高 RMSF 区提示埋着的疏水面被打出来）；bevacizumab Fab（PDB 1BJ1）为示例 |
| 7 | 可选：手动突变 | 'Mutate residues'（需先开 FoldX），可在结果页逐残基改后再算 | 无判据，用户自定 | 一个变体的重算分数；"Importantly, unlike automated mutation methods, the Mutate residues option seamlessly integrates with pH calculations and Dynamic mode." |
| 8 | 可选：自动突变建议 | 两种模式：charged（把高分残基换成 Lys/Arg 或 Asp/Glu）/ evolutionary conserved（按 PAM250 选单步替换 A→B 而非 A→C→B） | "In the automated mutations mode, A4D identifies residues with the highest A4D score, subsequently mutating them into positively charged residues (Lysine and Arginine) or negatively charged residues (Aspartic and Glutamic acids)."；进化模式的替换来自保守矩阵，"These matrices store the sum of accepted substitutions in closely related sequences, with an identity threshold of 0.85 or higher." | "Upon analysis completion, A4D generates a ranked list of suggested point mutations, accompanied by an evaluation of their solubilizing effects and energetic implications."；排序规则："Mutations that do not negatively impact stability are prioritized, appearing at the top of the list, while those that affect stability are highlighted in orange (energetic effect >0.5 kcal/mol) and red (energetic effect >1.0 kcal/mol)."（0.5/1.0 kcal/mol 是**颜色分级**，不是淘汰门槛）；用户可指定残基黑名单保护功能片段 |
| 9 | 算力/时间口径 | 按蛋白大小与选项计费时长 | 无阈值 | "For most settings, smaller proteins (around 100 amino acids) typically require only a few minutes, while larger proteins (around 300 amino acids) usually take between 10 and 15 min."；动态模式 "taking about 20 min for smaller proteins and over an hour for larger ones" |

### B. 标定与验证（作者用什么数据证明它行）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 18 个蛋白（11 球状 + 7 IDP）的 pH 依赖聚集实测 | 比实验值与预测值的线性回归斜率 | 一致率（斜率方向一致即算 agreement） | "including 11 globular proteins and 7 IDPs."；A4D 两类均 "achieving 100% agreement between the predictions and experimental results for both categories"；对照 "In comparison, CamSol had an overall agreement of 78% (64% for globular proteins and 100% for disordered proteins)." |
| B2 | HSA（PDB 6YG9）pH 7→5 | 用 pH 模式预测，再对实验 | 原文报 R²=0.88（图 3a；含 U+2010 的句子不引用） | "Utilizing the pH calculations feature of A4D, it was found that at pH 5, HSA shows a heightened propensity for aggregation compared to pH 7." |
| B3 | BSA 4F5S / 溶菌酶 1LYZ A 链 / RNase Sa 1C54 A 链 | 三种 典型失败模式 | 见 §2.4、§2.5；实验量分别为 聚集蛋白百分比、ThT 595 nm 吸光（溶菌酶与 RNase Sa），全部归一化 | 一张行为分型表：拟合好 / 极端 pH 崩 / 幅度不符（图 4） |
| B4 | MEDI1912 抗体变体集（Ebo 2020，Brockwell 实验室提供结构） | 按 HP-SEC 保留时间中点把变体二值化，再用 A4D 最大分、SolubiS 的 TANGO 分、CamSol 的结构校正值分别判 | "Mutational impact for A4D was assessed by the maximum score (the best reporter for experimental properties of folded proteins), for SolubiS the Tango score and for CamSol the structurally corrected score." | "TABLE 2 Performance of A4D, SolubiS and CamSol for a dataset of 19 mutants of the MEDI1912 monoclonal antibody as reported in ref (Ebo et al., 2020 )." 六个指标见 §4；结论句 "As reported in Table 2 , A4D displays the highest sensitivity, accuracy, and specificity" |

**这套流程值得单独记住的骨架**：一个便宜的序列/结构打分器 + 一个环境维度（pH）+ 一个能量项（FoldX）+ 一个柔性项（CABS-flex）+ 一套 改哪几个残基 的建议，且各功能之间被**互斥开关**切干净。它不是漏斗，是**一台闸口机**：所有判断都在下单之前、只用别人已有的实验数据标定。

## 4. 关键数字台账（数值 · 含义 · 出处，全部可在登记底稿里搜到）

| 数值 | 含义 | 出处 |
|---|---|---|
| >0 / >0.5 | 残基 A4D 分：>0 提示潜在聚集，>0.5 更可能是关键聚集残基 | "For most applications, the A4D score above 0 indicates potential aggregation" |
| 10 Å（可选 5 Å） | 聚集分析球半径（默认 10 Å） | §3.6；默认值见 Table 1 |
| 11 个 pH 点，4→9，步长 0.5 | pH 模式的采样密度 | "across a range of 11 pH values from 4 to 9 with increments of 0.5." |
| 4.0–9.0 | 服务器允许的 pH 区间（因溶菌酶碱性端失败而截断） | "which is why the A4D server limits pH prediction range to values between 4.0 and 9.0." |
| 5 种（Asp/Glu/Lys/His/Tyr） | 分数随 pH 变化的残基；其余（含 Arg）不变 | "lysine, histidine and tyrosine (see Figure 2b ), while the score of other amino acids remains unchanged." |
| 18 个蛋白 = 11 球状 + 7 IDP | pH 依赖预测精度验证集（数据取自 A4D 原始论文） | "including 11 globular proteins and 7 IDPs." |
| 100% vs 78%（球状 64% / 无序 100%） | A4D 与 CamSol 的实验-预测斜率一致率 | "achieving 100% agreement between the predictions and experimental results for both categories" |
| R² = 0.88 | HSA 预测分与实验聚集值的相关（图 3a，正文数字，句子含非 ASCII 故不整句引用） | §3.1 末段 |
| 0.89 / 0.75 / 0.80 / 0.82 / 0.65 / 0.20 | A4D 在 MEDI1912 集上的 Sensitivity / Specificity / Precision / Accuracy / MCC / FDR | "A4D 0.89 0.75 0.80 0.82 0.65 0.20"（Table 2 行，底稿为连排文本） |
| 0.78 / 0.25 / 0.54 / 0.53 / 0.03 / 0.46 | CamSol 同集同六指标 | "CamSol 0.78 0.25 0.54 0.53 0.03 0.46" |
| 0.89 / 0.38 / 0.62 / 0.65 / 0.31 / 0.39 | SolubiS 同集同六指标 | "SolubiS 0.89 0.38 0.62 0.65 0.31 0.39" |
| 18（正文）/ 19（表 2）/ 9+8=17（分类） | 被评测的 MEDI1912 变体数——三处口径不一致，本文未解释 | "The authors developed 18 different variants" |
| 0.85 | PAM 矩阵构建所用的近缘序列一致性阈值 | "with an identity threshold of 0.85 or higher." |
| >0.5 / >1.0 kcal/mol | 突变建议里稳定性代价的橙/红高亮分界（不是淘汰阈值） | "highlighted in orange (energetic effect >0.5 kcal/mol) and red (energetic effect >1.0 kcal/mol)." |
| 几分钟 / 10–15 min / 约 20 min / 逾 1 h | 单条任务的机时（100 aa 静态 / 300 aa 静态 / 100 aa 动态 / 300 aa 动态） | "usually take between 10 and 15 min." |
| 160,000 条蛋白 / 12 个物种 | A3D-MODB 预计算库规模 | "This resource contains a vast collection of over 160,000 proteins from the proteomes of 12 commonly studied organisms" |
| ~500,000 | A4D 服务器可直接调用的预计算任务数 | "providing easy access to nearly 500,000 precalculated jobs." |
| >2 亿 | AlphaFold 结构库条目数（本工具的结构来源） | "which includes over 200 million protein structures, has made a significant impact on structural biology." |
| Python 2.7 | A3D 独立版本（本地批量部署能跑到的那一版）的运行环境；A4D standalone 仍在开发 | "It is important to note that the current standalone version of A3D operates on Python 2.7." |

## 5. 结论——作者说了什么

1. A4D = A3D 全部功能 + **环境 pH 作为第四个维度**："A4D not only incorporates all the features of A3D but also introduces environmental pH as a variable in its calculations"；并加了自动突变协议与易用性改进："Additionally, new automated mutation modes and expanded file compatibility have further enhanced A4D's utility in protein solubility and aggregation studies"。
2. pH 依赖精度：在 18 个蛋白（11 球状 + 7 无序）上与实验斜率 **100% 一致**，CamSol 总体 78%；汇总指标要按体系选（球状 max / 无序 avg）。
3. 折叠蛋白上的突变效应判别：在 MEDI1912 变体集上，"As reported in Table 2 , A4D displays the highest sensitivity, accuracy, and specificity"（表 2 六个指标里，A4D 的 Sensitivity 0.89 与 SolubiS 并列最高，其余五项 Specificity 0.75、Precision 0.80、Accuracy 0.82、MCC 0.65、FDR 0.20 均为三者中最好，表注称最优项加粗）。
4. 柔性会造出新热点：bevacizumab Fab（PDB 1BJ1）的静态分析给出的聚集面在动态模式里扩大——图注原句 "(b) Bevacizumab Fab fragment (PDB ID: 1BJ1) aggregation propensity predictions using A4D Static mode (left side) and Dynamic mode (right side)."，正文补一句 "The Fab domain of bevacizumab is known for its high aggregation propensity, necessitating reduced concentrations in its therapeutic applications."（Dynamic mode reveals 那句含 U+2010 连字符，本卡不引用，此处为转述）。
5. 工具生态定位：可隐私（不把任务公开）、可脚本化（RESTful）、可零成本查预计算库；但**本地可跑的只有 A3D 独立版**，"While this is not the latest version of Python, the next iteration of the standalone A4D, is currently under development."
6. 展望（作者自陈待办）："One key advancement would involve the integration of machine learning algorithms to perform mutational analysis."，"Furthermore, the incorporation of empirical aggregation data into these models could refine the predictive capabilities"——也就是说，作者自己承认现版**不含机器学习突变分析**、且经验聚集数据尚未并入。
7. 作者的用途口径始终是可溶/抗聚集，不是活性：把自动突变定位成湿实验的替代品——"A4D offers an Automated mutation feature aimed at identifying more soluble variants of functional therapeutic proteins."，其目标是用计算替代耗时耗钱的展示筛选（该句后接 phage display，本卡转述）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的价值不在算法新颖，而在 把闸口做成了零门槛的网页 + API + 预计算库**。真正做方法的论文是它引用的 A4D 原文（NAR 2024, gkae382），本篇是 Tools for Protein Science 栏目的综述/说明书。→ 迁移时要引对论文：判据细节引 NAR 原始件，工程可用性（免费、RESTful、机时、互斥约束）引本篇。
2. **max 与 avg 的分岔说明这类标量打分器没有 统一口径**：同一份序列在球状与无序两类体系里的正确汇总方式相反，且分数在 pH 模式与非 pH 模式之间不可比（§2.6）。→ 我们做描述符时，必须像他们一样**先按体系类型固定汇总方式**，否则同一判据在不同候选池上含义漂移。
3. **他们对失败做了三分类**（拟合好 / 极端 pH 崩 / 方向对幅度错），并把崩溃点直接变成产品边界（pH 4.0–9.0）。→ 这是 判据适用范围要写死在工具里 的示范：我们的廉价预筛也应给 超出适用范围 状态，而不是硬给分数。
4. **能量代价只做颜色、不做门槛**（0.5/1.0 kcal/mol），把最终取舍交回人。→ 对我们：任何 抗聚集 vs 保功能 的打分器都只能排序、不能单独淘汰，因为 FoldX 类 ΔΔG 的预测力在别处已被证明偏弱（`sources/cost-benchmarks.md` §六 热稳定性行记：与 DMS 功能分平均 Spearman 仅 0.26–0.28）。
5. **验证集全部是别人的数据**（Ebo 2020 / Oeller 2023 / Li 2016 等），且样本极小（17–19）。作者没有为 A4D 生成任何新湿实验。→ 所以本文能证明的是 在它挑出来的这几个案例上排序最好，不能证明 进了设计漏斗会提高命中率；这与 `cost-benchmarks.md` §六 当时的批注（未见前瞻对照）完全一致。
6. **His 被明确纳入 pH 敏感残基**这一点值得单独记：组氨酸的 pKa 在生理附近，所以 胞内 pH / 内体 pH 之间真正会变的往往是 His。若我们的候选里有依赖 His 的催化 triad（或 UAA 激活位点里负责金属配位的 His），A4D 的 分数变化 与 催化必需 会打架——自动突变模式恰恰会把高分残基换成带电残基，可能直接改掉 His。→ 推断：任何把 A4D 建议接入我们漏斗的做法，都必须带 残基黑名单（他们提供了这个功能，"Furthermore, users can exclude specific residues"）。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：① 极端 pH（碱性的溶菌酶）算不了，服务器范围被限制到 4.0–9.0；② RNase Sa 型 幅度不符 是 已知局限；③ Arg 的 3D pKa 估不准，只能冻结；④ pH 模式与 Dynamic/自动突变互斥，一次跑不全；⑤ A4D standalone 尚未发布（本地版停在 A3D + Python 2.7）；⑥ 现版不含机器学习突变分析（列为未来工作）。
- 记录文件与全文不符处（**以全文为准；2026-11-07 已更正 CSV 的『年份』与『证据级别』两列**）：
  1. 年份：曾记 2025，实为 Protein Science **2024**, 33(10):e5180（在线 2024-09-26）；2026-11-07 已更正为 2024。
  2. CSV 的 阈值数字 / 候选数递减 / 实验命中率 / Kd或活性最好值 / 成本统计 五列全为 未记录，而全文其实给了：分数阈值 0 与 0.5、pH 网格 11 点、突变能量高亮 0.5/1.0 kcal/mol、PAM 一致性阈值 0.85、机时几分钟到逾 1 小时、混淆矩阵六指标（0.89/0.75/0.80/0.82/0.65/0.20 等）。这些在本卡 §3/§4 已补齐，等统一回填轮次再动表。
  3. CSV 的 是否用MD / 是否用QM 两列记 否 —— 与全文一致（本文无全原子 MD、无 QM），但需注明 CABS-flex 是粗粒度构象采样、FoldX 是经验力场，二者都不是 MD 也不是 QM，不能被误读成 做过模拟验证。
  4. CSV 的作者列记 （本次未展开精读），全文署名 5 人：Zalewski / Iglesias / Bárcenas / Ventura / Kmiecik。
- 我们读出的：① 表 2 的 19 mutants 与正文的 18 variants、正负 9+8=17 三处口径打架，本文未解释（见 §2.7）；② 18 蛋白验证集与 17–19 突变体评测集都是作者自选，没有独立盲测；③ 本文没有给出公式 (1) 四个参数 α β γ δ 的实际数值，也没有给 pLDDT 截断值，按本卡粒度算 原文未给阈值；④ 纯文本抽取把公式 (1) 打散了（A4D score 被拆成 A 4 D score，希腊字母与求和号混排、上标丢失），本卡只按正文对每个符号的文字解释（中心残基项 + 半径内邻居项按 Cα 距离衰减）来描述它，不复制其排版式；⑤ 许可是 CC BY-NC-ND（非商业、不得改编），若要把输出嵌进我们自己发布的产物需注意。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **设计期的 可溶/抗聚集 廉价闸口**：单条序列 → 结构（PDB/UniProt 自动取 AlphaFold）→ 每残基分数 → 0/0.5 两档告警，机时几分钟、免费、RESTful 可批量。这正好落在我们 先砍掉注定不溶的候选，再谈催化 那一档；相对本项目自己记录的 MD 单价（156.6 ns/day、新体系 10.6 GPU·h，见 B09 卡 §6.3 与 `sources/cost-benchmarks.md` §八 缺口 6），它的单价低到可以在整池候选上跑。用法建议：把 高分残基是否落在假定活性位点/底物通道内 作为交叉判据，而不是只看总分。
2. **pH 维度**：我们的反应体系跨 pH（胞内 ~7.2、纯化/储存缓冲、部分酶在最适 pH 之外失稳），A4D 能给 同一序列在不同 pH 下的聚集倾向曲线，且明确 His/Asp/Glu/Lys/Tyr 驱动——这比只看静态分数多一条 环境敏感性 检查。
3. **突变建议的排序逻辑**：先按聚集改善排序、再用能量代价（0.5/1.0 kcal/mol）着色、并允许残基黑名单。→ 直接照搬到 改面不改催化 的构造：把催化必需残基与配金属位点写进黑名单，取 排在最前且能量代价为绿 的少数几条送测。
4. **预计算库当零成本同族检索**：人/酵母等 12 物种、约 16 万条、约 50 万个预计算任务，可先查 我们的天然同源酶/近缘家族 在库里的聚集与稳定性口径，再决定要不要自己跑。
5. **状态命名与产品边界的做法**：把 已知会崩的区间 写进工具（pH 4.0–9.0 之外不给分）。→ 我们的判据也要有 超出适用范围 与 METHOD_FAIL 状态，而不是硬输出一个数。

**不可迁移（为什么不能照搬）**

1. **A4D 的 0 / 0.5 不是可表达性阈值**，更不是活性阈值。它是对残基层面聚集倾向的经验刻度，作者验证的是 会不会聚 而不是 有没有功能。不许把这两个数当 UAA 合成酶候选的 过 / 不过 门槛，也不许据此估算可溶率。
2. **MEDI1912 上的 0.89 灵敏度 / 0.82 准确率 / 100% pH 一致率不能变成我们的成功概率**。分母只有 17–19（且三处口径不一致），验证数据全是自选、抗体体系、由随机突变池二值化而来；与 UAA 合成酶（多步化学事件 + 产物身份确证）没有可比性。只许引用其**评测口径**（用混淆矩阵六指标而非单一命中率），不许引用其**数字**做校准。
3. **本文没有前瞻设计对照**——`sources/cost-benchmarks.md` §六 当时的批注（这些工具为溶解度/聚集倾向验证过，未见用于从头设计命中率提升的前瞻对照）在读完全文后**依然成立**：全文没有任何 用它筛过的设计库 vs 没筛过的库 的命中率比较。
4. **pH 范围 4.0–9.0 之外不提供任何判据**，且精氨酸被冻结；任何依赖极端 pH 或 Arg 网络的解释都不能拿它当证据。
5. **本文不含 MD、不含 QM、不含自由能**，所以它不能为 用 MD/QM 判催化 提供任何命中率背书；同理，binder 论文的 pAE/ipTM 阈值、适配体 FEP 命中率与本文无关，不得交叉借用。
6. **A4D 不做活性位点、不做结合界面亲和力、不做寡聚态预测**，它只回答 会不会聚 与 改哪里可能变可溶。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K48_PMC11425640_text.txt

- 本地纯文本：`fulltext/K48_PMC11425640_text.txt`（由 `K48_PMC11425640_fullTextXML.xml` 去标签、HTML 实体解码、空白折叠得到，内容未改写；全文 71,742 B，单行）。登记底稿共 3 份，本卡只按这一份逐字比对；另一份 XML 与 `sources/cost-benchmarks.md` §六 为同编号登记项，未用作引句来源。
- 身份核验方法：读底稿前 600 字符，标题/期刊/DOI 10.1002/pro.5180/PMCID PMC11425640/PMID 39324697 与 CSV 行一致，确认后再引用。
- 只读参考：`sources/cost-benchmarks.md` §六（第 2 行 包涵体/不溶 判据栏）与 §八 缺口 4（失败原因分布无系统统计）；未修改任何 `sources/*.md` 与 CSV。
- CSV 字段映射：本卡 §3 ↔ 计算筛选判据 / 阈值数字 / 候选生成方法；§4 ↔ 候选数递减 / 成本统计；§8 ↔ 在方法演进链的位置。14 键值均按全文实填，非全文可得的写 未记录（原因）。
- 本卡自检：`python scripts/verify_literature_cards.py --only K48 --no-report`（参数：--only K48 --no-report；输入：本卡 + 登记底稿），把卡内所有被直双引号包住、不含中日韩字符、≥20 字符、≥12 个字母的片段在底稿里逐字查找；本轮结果 **PASS K48 quotes=65/65，退出码 0**（65 段为门禁按相邻双引号切出的片段计数，去重 61 段；对应人工写入的约 40 条原文引句，其中同一句在 §3 表格与 §4 台账各引一次）。写卡时已剔除含 U+2010、Å、α、求和号、R² 的句子（改为中文叙述），跨参考文献编号的两句拆成两条，未使用省略号，未给术语/状态名加英文引号；首轮曾因把打散的公式排版当引句写入而 FAIL（1 段 MISS），改为中文描述后复跑转绿。
- 与并行工作的边界：本卡只新增 `K48_Aggrescan4D-2024_ProteinSci_pH-aggregation-engineering.md` 一个文件（2026-11-07 按全文题录把文件名里的 2025 更正为 2024，内容未变）；未跑 --sync-map、未跑不带 --no-report 的全量门禁、未改 CSV/sources/B09 样板卡/scripts/fulltext/_quarantine。

<!--CSV回填
work_type=方法（Protein Science 的 Tools for Protein Science 栏目：A4D 网络服务器的说明书/综述，非原始算法论文；原始算法见 NAR 2024 DOI 10.1093/nar/gkae382）
target=蛋白聚集/不溶失败模式（球状蛋白与 IDP 的聚集倾向；示例体系：HSA 6YG9、BSA 4F5S、溶菌酶 1LYZ、RNase Sa 1C54、bevacizumab Fab 1BJ1、MEDI1912 抗 NGF 单抗）
backbone_generation=不生成序列或骨架；对已有结构打分（PDB/CIF 上传或 PDB/UniProt ID 自动取 AlphaFold 结构），并可给出自动点突变建议（charged 替换 Lys/Arg/Asp/Glu，或按 PAM250 的进化保守替换）
computational_filters=Aggrescan in vivo 聚集倾向标度 + 溶剂可及面积 + 球内（默认半径 10 Å，可选 5 Å）邻居按 Cα 距离衰减（公式 1）；pH 模式改用 SolupHred 的 pH 依赖亲脂度标度 + pKa-ANI 的三维 pKa（仅 Asp/Glu/Lys/His/Tyr 随 pH 变，Arg 冻结）；FoldX 输入优化与突变能量增量；CABS-flex 柔性采样（模型按 A4D 分排序 + RMSF）；AlphaCutter 切 AlphaFold 非球状区（DSSP + 接触图 + pLDDT 阈值）；球状用 max 分、IDP 用 avg 分
thresholds=A4D 分 >0 提示潜在聚集、>0.5 更可能是关键聚集残基；pH 网格 4→9 共 11 点、步长 0.5，服务器允许区间 4.0–9.0（碱性端因溶菌酶部分展开预测失败而截断）；突变建议的稳定性高亮 能量效应 >0.5 kcal/mol 橙色、>1.0 kcal/mol 红色（仅颜色分级，非淘汰阈值）；PAM 近缘序列一致性阈值 0.85；AlphaCutter 的 pLDDT 阈值与公式参数 α β γ δ 取值：原文未给阈值
md_used=否（无全原子显式溶剂 MD；CABS-flex 为粗粒度构象采样、FoldX 为经验力场，二者均非分子动力学，本文亦无 MD 验证）
qm_used=否（pH 效应靠 pH 依赖亲脂度标度 + 机器学习 pKa-ANI 估算，不涉及量子化学）
experimental_methods=本文自身无湿实验；只用他人实验数据做标定与评测：HSA/BSA/溶菌酶/RNase Sa 的 pH 依赖聚集实测（含 ThT 595 nm 与聚集蛋白百分比，归一化后比回归斜率）、MEDI1912 变体的 HP-SEC 保留时间（按中点二值化，算 Sensitivity/Specificity/Precision/Accuracy/MCC/FDR）
pipeline_counts=输入 1 条序列/结构 → 每残基分数表（球半径 10 Å，11 个 pH 点） → 排序后的点突变建议列表；验证集 18 个蛋白（11 球状 + 7 IDP）+ 4 个 pH 曲线案例 + MEDI1912 变体集（正文 18 variants、表 2 记 19 mutants、正负类 9+8=17，三处口径不一致）；预计算库 A3D-MODB 逾 160,000 条蛋白/12 物种、服务器侧近 500,000 个预计算任务、AlphaFold 库逾 2 亿结构
hit_rate=无设计命中率（本文不产出设计库）；可引用的判别力仅两组：pH 依赖聚集斜率一致率 A4D 100%（球状与无序两类均是）vs CamSol 总体 78%（球状 64%、无序 100%）；MEDI1912 突变体集上 A4D Sensitivity 0.89/Specificity 0.75/Accuracy 0.82/MCC 0.65/FDR 0.20（CamSol 0.53、SolubiS 0.65 accuracy）
best_metric=未记录（本文为聚集倾向与溶解度工具，不报 Kd 或酶活；引用的 MEDI1912 野生型抗体对 NGF 为 picomolar 亲和力，属数据来源 Ebo 2020 的性质而非本文测量）
cost_or_stat_note=网页工具免费、无需注册；机时：约 100 aa 静态几分钟、约 300 aa 静态 10–15 min，动态模式约 20 min（小蛋白）至逾 1 h（大蛋白）；pH 模式与动态模式/自动突变互斥，不能一次跑完；支持 RESTful API（PDB/CIF 或 PDB/UniProt ID，cURL/Python POST）；本地版目前只有 A3D standalone（Python 2.7，pip/Conda/Docker），A4D standalone 文中仍在开发；许可 CC BY-NC-ND
role_in_timeline=失败模式→判据映射表里 包涵体/不溶 与 聚集/多分散 两行的判据来源之一（Aggrescan 序列标度 → A3D 加结构与距离衰减 → A4D 加 pH 与自动化突变）；它把 可溶/抗聚集 从论文里的判据变成任何人都能白嫖的网页+API+预计算库，是我们设计期廉价预筛档里成本最低的一档；但至本文发表仍未提供 用于从头设计漏斗并提升命中率 的前瞻对照（`sources/cost-benchmarks.md` §六 的批注在读完全文后依然成立）
source_pointer=data/literature_cards/fulltext/K48_PMC11425640_text.txt（本卡 65 段引句逐字命中，门禁 quotes=65/65）+ data/literature_cards/fulltext/K48_PMC11425640_fullTextXML.xml；只读参考 sources/cost-benchmarks.md §六（包涵体/不溶 行）；原始算法论文 10.1093/nar/gkae382（本地无全文）
CSV回填-->
