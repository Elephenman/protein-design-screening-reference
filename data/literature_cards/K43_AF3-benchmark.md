# K43 — AlphaFold3 全类别第三方基准：九套数据集上 AF3 对 AF2/AF-Multimer/RoseTTAFoldNA 的实测边界

Peng C, Ni W, Liu Q, Hu G, Zheng W. A comprehensive benchmarking of the AlphaFold3 for predicting biomacromolecules and their interactions. Briefings in Bioinformatics 2025;26(6):bbaf616. DOI 10.1093/bib/bbaf616 · PMID 41313605 · PMCID PMC12661943。通讯：郑伟（南开）。CC BY-NC 4.0。

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K43**（组：通用方法学；batches.tsv 第 72 行，state=FULLTEXT） |
| 本地全文 | `data/literature_cards/fulltext/K43_PMC12661943_text.txt`（113,031 B，Europe PMC fullTextXML 抽取、标签剥离、空白折叠后落盘）＋同目录 `K43_PMC12661943_fullTextXML.xml`（194,689 B） |
| 对照底稿 | `sources/cost-benchmarks.md:150`（先行调研仅登记一行题录 AF3 基准，无内容——本卡为首次全文精读） |
| 证据级别 | **全文级**（本卡全部引句均可在登记底稿 text.txt 里逐字命中；见第 9 节自检） |
| 未取到的部分 | Table S1–S39 补充表、Fig. S1–S17 补充图、Zenodo 基准数据本体（https://zenodo.org/records/15502855，本任务禁止新抓取）。凡正文只说"见 Table Sxx"而没给数的，本卡明写"数值在补充表，正文未给出" |

## 1. 这篇到底解决什么（一句话）

DeepMind 官方论文的 AF3 成绩是"内部版本＋内部评测"，第三方一直缺一套同口径对比——这篇用 2024 年以后新 released、且与 AF3 训练集严格去泄漏的九套 PDB 基准（蛋白单体/孤儿蛋白/双构象/蛋白多聚体/肽-蛋白/抗原-抗体/RNA/RNA 多聚体/蛋白-核酸复合物），把 AF3（服务器版＋本地开源包）与 AF2、AlphaFold-Multimer、RoseTTAFoldNA、RhoFold+、NuFold、trRosettaRNA 在同一套指标口径下逐靶配对，给出一张"AF3 到底在哪类目标上强、强多少、哪里不行"的第三方分级表。作者自述动机："there is still an absence of third-party benchmarks to fairly demonstrate the performance of the"。

**必须先钉死的一条边界：九套数据里没有一套是蛋白-小分子配体（ATP/UTP 这类核苷酸游离配体的对接精度根本没测）**——最接近的是肽-蛋白（肽链 5–30 残基），其余全是聚合物-聚合物体系。

## 2. 难点，以及遇到问题时他们做了什么（作者自述）

1. **官方评测不可信 + 数据泄漏风险**：AF3 原论文的结论基于内部版本，而 PDB 老结构大量在训练集里。→ **应对**：九套基准全部取训练截止日（"The training dataset for AlphaFold3 (v3.0.1) and AlphaFold-Multimer (v2.3.0) contains all"）之后 released 的条目，并逐条排除与训练集高相似的："structures with sequence similarity >40% and coverage >80% to those in the AlphaFold3 training"，同时要求晶体覆盖："each of the structures must cover at least 80% of the residues in the corresponding crystal"；再用 CD-HIT/US-align 聚类去冗余（TM-score=0.5 为聚类阈）。**留下的代价**：AF2 v2.3.0 的训练截止是 2018-04-30，比 AF3 早三年多——作者自己在结论承认这是混淆因素（conclusions 里明写若 AF2 用同数据集重训结论可能不同），本文没有重训、无法排除。
2. **服务器版与本地版在同一靶上结果差异巨大**：如单体 8JGO 两版 TM-score 差约 0.300，多聚体 8VA1（server 0.976 vs local 0.304）、8JF2 反向。→ **应对**：对可疑靶各跑 20 次（server 每次 5 模型，共 100 模型）比分布："both versions produced nearly identical TM-score and LDDT distributions"，判定两版是在同一模型分布里抽样，单次差异是随机性＋排名选模的锅："its built-in model ranking struggles to distinguish high-quality models"。**留下的代价**：本文只诊断不解决，明说需要更好的评估模型精度（EMA）方法；单靶 20 次重复也没覆盖全部九套数据，只是抽查。
3. **全局指标会掩盖界面错误**（对迁移最有价值的一条）：肽-蛋白体系上 TM-score/LDDT 很高但界面差，"over 85% of predictions reached a TM-score ≥"；作者解释 "DockQ specifically measures the accuracy of the"。→ **应对**：为每类目标配专门的界面/局部指标——DockQ（蛋白互作）、FNAT（蛋白-核酸界面）、自建的 CDR-TMscore（抗体结合环）、INF（RNA 二级结构相互作用网络），并在报告里把"全局达标率"和"界面达标率"分开设阈展示。**留下的代价**：抗原-抗体界面即便换了指标，AF3 绝对水平仍低（见第 4 节 27.5% 条），换指标只是让问题可见，不是把问题解决。
4. **多构象（替代状态）本质上不是单次预测能答的题**。AF3 服务器每次只交 5 个模型："Since the AlphaFold3 server can generate only"。→ **应对**：每序列 20 个随机种子跑满 100 模型，再用状态特异性打分（对两态 TM-score 之差）挑"专属于某一状态"的模型；结果两态都预测对的只有 14/60（server）。作者收口是劝退式警告："users should proceed with caution when using AlphaFold3 to model proteins which may have multiple conformational states, as the sensitivity to detect alternative conformations without modified/enhanced sampling approaches may be limited"。**本文未解决**：增强采样策略（改 MSA/模板）只是转引他人 AlphaFold2 工作，自己没做。
5. **RNA 侧没有单一赢家，比较对象还分档位**。trRosettaRNA 全局精度反而最高（"trRosettaRNA achieved the highest mean TM-score"），AF3 居中游但局部和二级结构最好。→ **应对**：不报综合名次，把 TM-score / LDDT / INF 三个维度分开报、按 easy/hard 分层（模板 TM>0.5 为 easy），多方法比较做 Bonferroni 校正。**留下的代价**：RNA 多聚体样本只有 23 个，全局差异统计不显著（P=9.18×10⁻²），"能证明 AF3 局部更好、不能证明全局更好"就是这个样本量的天花板。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱）

- **被测工具**：AlphaFold3 服务器版（alphafoldserver.com）与本地开源包 v3.0.1（两者全程并列报告，分别称 AlphaFold3-server / AlphaFold3-local）；对照 AlphaFold2 v2.3.0、AlphaFold-Multimer v2.3.0（模板库截止 2021-09-30，与 AF3 一致）、RoseTTAFoldNA、RhoFold+、NuFold、trRosettaRNA。
- **判分工具**：US-align（TM-score，参数 "-TMscore 7 -ter 0"）、OpenStructure 算 LDDT（截断 0.5/1/2/4 Å，邻居半径 15 Å）、DockQ 包（Wallner 版，默认参数；FNAT 也用 DockQ 包算）、ClaRNA 算 INF、自写脚本算 CDR-TMscore。
- **统计**：Wilcoxon signed-rank 配对检验（作者注 "which is also used throughout this work for"——该说明在正文中带括号内嵌，本卡引文截到 "test" 为止）；两个比例差异用 two-sample proportion test；RNA 多方法比较做 Bonferroni 校正。
- **没有用的方法**：MD、QM、自由能微扰、湿实验、前瞻设计——这是纯回顾式计算基准，所有"对/错"都是模型对 PDB 实验结构。

### 评测流水线

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | PDB 全库（按各类截止日） | 建九套基准：日期过滤 → CD-HIT（或 CD-HIT-EST）去冗余 → 与 AF3 训练集（≤2021-09-30）比相似 → 晶体覆盖检查 → US-align 按 TM=0.5 聚类留一个代表 | 排除口径示例："structures with sequence similarity >40% and"；覆盖口径 "each of the structures must cover at least 80% of"；RNA/DNA 链 BLASTN e-value<10 查重 | I:150 单体（60–1700 aa）；II:113 孤儿（41–1012 aa）；III:60 组双构象；IV:206 多聚体（100–3000 aa、≤11 链）；V:80 肽-蛋白；VI:102 抗原-抗体；VII:52 RNA（40–1000 nt）；VIII:23 RNA 多聚体（26–814 nt）；IX:59 蛋白-核酸复合物 |
| S2 | 九套序列/链组合 | AF3-server、AF3-local 及各对照方法按默认参数推理，取各自排名分的 top-1 模型 | "Unless otherwise specified,"；"the top-ranked models from both methods," | 每靶每方法 1 组 top 模型（除 S5 的 100 模型实验） |
| S3 | 预测模型 × 实验结构 | 逐靶打分：全局 TM-score、局部 LDDT、界面 DockQ/FNAT、RNA 二级 INF、抗体 CDR-TMscore | 全局："A TM-score >0.5 typically indicates that the two"；界面分级："a score < 0.23 is generally considered to be an"，0.23–0.49 acceptable、0.49–0.80 medium、≥0.80 high；"FNAT is specifically calculated using DockQ to"；"INF is defined as the Matthews correlation"；CDR 口径："the model is first superposed" | 每靶每方法 5–6 个标量；汇总入 Table S10–S39 |
| S4 | 配对分数 | 逐靶 Wilcoxon 配对检验＋head-to-head 散点＋easy/hard、单域/多域、同源/孤儿分层 | RNA 多方法比较 Bonferroni 校正后 adjusted P<10⁻⁴（LDDT）与 <10⁻²（INF）；单体再取 <25% 同相似度子集复核："we selected 52 monomers from" | 每类目标一张显著性表；泄漏敏感性结论："after close homologs were" |
| S5 | 可疑靶（8JGO、8VA1、8JF2、7URM_v、8UPT_A、8QA9、8P5Q）＋全部 60 组双构象 | 每版本×每序列 20 次随机种子重跑（server 5 模型/次 → 100 模型），比较两版分布与 top-模型差距 | "both the AlphaFold3-server and"；构象专一性口径：一态 TM>0.8 且另一态 <0.8 | 分布基本重合 → 判定差异源于抽样随机＋排名；双构象达标规模见第 4 节 |
| S6 | 单序列无 MSA 模式（Benchmark-I 的 150 条）＋孤儿集 | AF3-local 与 AF2 去掉 MSA/模板重跑，另取 14 条 MSA 完全检不到同源物的孤儿细看 | 成功口径同 S3（TM≥0.5） | "26.0% of AlphaFold3-local"；作者同时点明两边都差："most predictions falling below" |
| S7 | 全部运行 | 记录 wall-clock 时间对比成本 | 统一硬件（见第 4 节成本行） | "AlphaFold3 achieves faster" |

## 4. 关键数字台账（数值 · 含义 · 出处；全部来自本地全文）

| 数值 | 含义 | 出处（原句片段，§9 底稿逐字可查） |
|---|---|---|
| 150 / 113 / 60 / 206 / 80 / 102 / 52 / 23 / 59 | 九套基准各自的靶数 | 如 "150 monomers, ranging from 60"；"This procedure yielded a final"；"206 protein multimers, with"；"80 nonredundant peptide-protein"；"Finally, 102 antigen-antibody"；"52 RNA structures, with nucleotide lengths ranging from 40 to 1000, were selected for the Benchmark- VII dataset"；"the Benchmark- VIII dataset"；"This resulted in 59 protein-nucleic acid complexes in our Benchmark- IX dataset"（III 的 60 组见第 2.4 节；IV 中 35 heteromer/171 homomer，VII 中 22 easy/30 hard） |
| 单体：TM 0.817 vs 0.812（P=.16）；LDDT 0.792 vs 0.787（P=2.67×10⁻³） | AF3-server vs AF2 全局不显著、局部显著 | "produced models with higher"；"AlphaFold3-server outperformed" |
| 多构象：两态全对 14/60（23.3%）；一态 30（50%）；零态 16（26.7%） | server 版；local 12/60；AF2 9/60 | "both conformational states were"；专一性达标 32/120（server）、54/120（local）、43/120（AF2）（数值见正文，第 2.4 节引句同段） |
| 多聚体：TM 0.821/0.824 vs 0.812（P=.49/.74）；LDDT 0.860/0.861 vs 0.851；DockQ 0.589 vs 0.568（P=.19）；正确界面（DockQ≥0.23）78.2% vs 71.8%（P=.14） | AF3 vs AF-Multimer 全局与界面均不显著、局部显著 | "The average LDDT scores were"；异源四聚体 DockQ 提升显著："AlphaFold3-server achieved an"（同源仅 +2.7%，P=.72） |
| ipTM–DockQ 相关 0.81 / 0.79 / 0.76 | 置信分与界面质量的秩相关（206 靶） | "showing strong correlations:" |
| 肽-蛋白：TM ~0.91–0.92、pLDDT ~0.86、DockQ ~0.63，三法持平；TM≥0.5 达标 >95%，DockQ≥0.23 达标 ~85% | 两版 AF3 与 AF-Multimer 无法区分 | "the three methods exhibited"；"more than 95% of predictions" |
| 抗原-抗体：TM 0.739/0.735 vs 0.683（+8.1%/+7.5%）；DockQ 0.422/0.418 vs 0.325（+29.8%）；正确界面 27.5%/28.4% vs 9.8%；CDR-TMscore 0.183/0.176 vs 0.074；CDR 折对 18.6%/17.6% vs 7.8% | AF3 相对增益最大的一类，绝对水平仍低 | "Both the server and local"；"AlphaFold3 correctly modeled"；"correct CDR folds (CDR-TMscore" |
| RNA 单体：TM trRosettaRNA 0.548 > NuFold 0.525 > AF3 0.510/0.504 > RFNA 0.449 > RhoFold+ 0.431；LDDT AF3 0.713/0.715（领先次优 ≥13.0%）；INF 0.814/0.816（≥2.9% 领先） | 全局中游、局部与二级结构第一 | "trRosettaRNA achieved the"；"Both versions achieved the" |
| RNA 多聚体：TM 0.300/0.299 vs RFNA 0.242（P=.092/.119，不显著）；正确全局折叠 2/23 vs 0/23；LDDT 0.564/0.571 vs 0.462（显著） | AF3 只保住局部精度的显著性 | "The server and local versions"；"only two of the 23 complexes"；"fewer than 10% of RNA multimers" |
| 蛋白-核酸复合物：TM 0.745 vs 0.653（+14.1%，P=1.04×10⁻⁵）；LDDT 0.774/0.753 vs 0.677；FNAT 0.410/0.417 vs 0.186；FNAT>0.5 占比 ~35.6% vs 16.9%；亚基 TM：蛋白 0.875 vs 0.835、RNA 0.401 vs 0.297、DNA 0.309 vs 0.267 | AF3 对 RFNA 的全维度优势（本文最强的一类） | "the average TM-score achieved"；"AlphaFold3-server achieved"；"~35.6% of structures predicted"（FNAT 均值句见第 2.3 节同段："the average FNAT scores achieved by AlphaFold3-server and AlphaFold-local were 0.410"） |
| 单序列模式：TM 0.413 vs 0.353；LDDT 0.433 vs 0.377；AF3 绝对水平比默认模式低 20%–30% | 无 MSA 时 AF3 优势最大但都不可靠 | "26.0% of AlphaFold3-local"；结论节 "although its absolute accuracy"（该句在 conclusions 内，数值可查） |
| easy vs hard：整体差 ~20%-30%；hard 组三法基本持平（TM 0.691/0.685/0.687） | 模板可得性主导难度 | "performance metrics on the easy" |
| 成本：AF3 平均 ~20 min（单体）/~31 min（多聚体）/~47 min（抗体）/~10 min（RNA）/~23 min（蛋白-核酸）vs RFNA ~996 min、AFM ~382 min 等 | 所有基准集 AF3 最快 | "on benchmark-IX (protein-nucleic acid complexes), AlphaFold3 and RoseTTAFoldNA required ~23 and ~996 min, respectively"；"the average runtimes of AlphaFold3, RoseTTAFoldNA, RhoFold+, NuFold, and trRosettaRNA were ~10, ~445, ~402, ~531, and ~426 min, respectively"；"All results were obtained on an" |
| 结论级总分：RNA/PNA 平均 TM 0.510、0.745 远低于蛋白 0.898、复合物 0.821 | 作者自己给的"核酸类仍欠一截" | "the average TM-scores for"——注意 0.898 与正文 Benchmark-I 的 0.817 对不上，见第 7 节 |
| CASP16 对照：>30% 寡聚体靶仍高难，各队约只对上四分之一 | 本文抗体结果与社区盲测一致 | "In CASP16, more than 30% of" |

## 5. 结论——作者说了什么

1. 增益分级（作者原话）："The improvement of AlphaFold3"——蛋白多聚体整体上新旧管线无显著差别（抗体除外）。
2. 单体：全局打平、局部小赢；蛋白复合体：全局与界面打平 AF-Multimer、局部显著小赢；肽-蛋白：不可区分；抗原-抗体：全指标显著优于 AF-Multimer 但绝对水平低。
3. RNA 单体：AF3 全局中游（trRosettaRNA/NuFold 更高）、局部与 INF 第一；RNA 多聚体：仅 LDDT 显著，"fewer than 10% of RNA multimers"。
4. 蛋白-核酸复合物：AF3 对 RoseTTAFoldNA 是"更全面可靠的工具"（原文 "These findings suggest that"——该句在 PNA 节末），归因于亚基（尤其核酸链）建模与界面接触（FNAT）两项都更好。
5. 排名与抽样是独立瓶颈："Even when correct models were"；把 AF3+AF-Multimer 模型合池按 0.8×ipTM+0.2×pTM 挑优，"still did not lead to a significant improvement in TM-score"。
6. 复杂结构预测"远未解决"：作者要求 "Substantial methodological"。
7. 对多构象目标的适用边界（原文警告句已引于第 2.4 节）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇是"相对增益分级表"，不是"绝对能力证明"**。它全部结论都是同一工具族在晶体结构对照下的相对排序；AF3 比 RFNA 在蛋白-核酸上强 14.1% 这件事，与"AF3 能不能把核苷酸放对到能判定催化几何"是两个问题——后者的判据（供体原子间距/角度、反应路径）这篇根本没设。
2. **核酸类目标的"赢"含金量低**：AF3 在 PNA 复合物上 RNA/DNA 亚基平均 TM 只有 0.401/0.309（低于 0.5 的同拓扑线），意味着作者口中"更强"很大程度上是"比一个很弱的对照强"。→ 对我们：拿 AF3 判含核苷酸复合物时，核酸链本身的构象应当默认不可信，除非逐链重算 TM/FNAT 过关。
3. **server≠local、单次≠分布**是工程事实：两版随机抽样自同一分布但 top-1 可能差 0.3–0.6 TM。→ 对我们：任何用 AF3 产出的关键复合物判断都必须固定版本＋多seed重跑＋自定选模标准，不能拿"一次服务器结果"当证据（我们酶设计项目里机制层对象的复合物几何若来自单次运行，应视为未定）。
4. **全局指标骗人**这条被三个体系反复印证（肽-蛋白 TM≥0.8 但 DockQ≥0.8 仅 ~40%；抗体近天然全局但 CDR 折对 18.6%；PNA 近天然全局但 RFNA 靠全局分掩盖 FNAT 0.013）。→ 对我们：判"核苷酸结合模式对不对"必须用界面口径（FNAT 类接触清单＋几何量），pLDDT/pTM/ipTM 高只说明整体像，不说明活性位点像。
5. **本文没有任何蛋白-小分子配体结果**，AF3 官方论文声称的小分子/离子/修饰残基能力在本基准里是空白。→ 对我们：项目里若要用 AF3 摆放 ATP/UTP/中间体这类游离核苷酸，本文提供的第三方证据是零，既不能引用它支持、也不能引用它反对；只能另设几何复核。

## 7. 局限与失败（作者的 + 我们读出的）

- **作者自认**：AF2 权重训练截止 2018-04-30 与 AF3 不同（结论节明写混淆可能）；抗原-抗体界面与 CDR 绝对精度低；RNA 多聚体全局不显著、ab initio RNA-RNA 折叠未解决；排名/评估是共同短板；多构象采样能力不足；蛋白单体精度可能已触及"当前架构与数据库规模"的平台期。
- **我们读出的**：① conclusions 里 protein monomer 平均 TM 写 0.898，正文 Benchmark-I 是 0.817——同一篇论文两个数对不上（未说明 0.898 的口径，疑似取错子集或笔误），引用该结论级对比时要带此存疑；② 九套集全部是"有实验结构可对照"的靶，等于只测了分布内回归题，对无模板可对照的全新设计/无标签天然体系没有外推力；③ 样本量小（VIII 仅 23、IV 的异源体仅 35），P=.09/.14 这类"不显著"可能只是功效不足，不能反向引用为"证明无差别"；④ 没有前瞻湿实验、没有结合自由能、没有对预测做实验验证闭环；⑤ FNAT 的界面接触重定义用了 10 Å 宽松截断（这是 DockQ 包口径，不是本文选择，但引用其 FNAT 数字时必须记得它衡量的是"宽界面"）；⑥ 表/图号（Table S10–S39、Fig. S1–S17）里的细粒度数字未进入本卡台账（正文只给摘录）。

## 8. 迁移判断：哪些能搬、哪些不能搬（含"用 AF3 判含核苷酸复合物"意味着什么）

**可迁移（怎么用）**

1. **"AF3 判含核苷酸复合物"的正确用法**：本文给出的证据是——在蛋白-核酸复合物这一类上，AF3 是现有端到端工具里最强的一档（TM 0.745、FNAT 0.41，对 RFNA 全维度显著）。因此**做复合物几何假设时选 AF3、而不是因为"官方论文说它行"选它**，这是有第三方证据的选型依据。同时把该类的两个硬底牌写进协议：核酸亚基平均 TM 0.401/0.309（多数情况下核酸链自身构象不达同拓扑线）、约 2/3 复合物界面接触过半——即 AF3 的 PNA 输出默认是"可用但需逐链复核"，不是"可直接采信的复合物结构"。
2. **界面口径照搬结构、不照搬数值**：本文把 DockQ/FNAT/CDR-TMscore 这类"专门测界面"的指标与全局指标并列报告，是可直接移植的评测组织方式。我们的对应物：对中间体/ATP 位点预置复合物，用接触清单＋冻结几何口径（如既有协议的 ≤4.0 Å/≥150° 桥接判据）逐靶重算，并像本文一样分层报告"全局达标率"与"界面达标率"两个数。
3. **多 seed 重跑＋分布对照**（本文 20×5=100 模型协议）直接可用于我们机制层对象（MGYP000657498120 类）的复合物几何稳定性检验：固定版本、N 次随机种子、报 top-1 与分布的差距，把"排名不可信"变成可测读数。
4. **泄漏排除口径**（训练截止日＋>40%/80% 相似剔除＋晶体覆盖≥80%）是我们做任何"用 AF3 打分的历史回放"时的卫生标准。
5. **成本口径**：AF3 单次几分钟~几十分钟（A100 40 GB/8 核/40 GB 内存档），比 RFNA 低一个量级以上——支持"AF3 当廉价几何预筛、昂贵判定留给下游"的漏斗排布。

**不可迁移（为什么不能照搬）**

1. **不得外推为对目标催化能力的预测力**。本文全部指标（TM/LDDT/DockQ/FNAT/INF/CDR-TM）测的都是"静态结构与实验结构的接近度"，没有一个测化学：没有过渡态、没有反应坐标、没有自由能。"AF3 把蛋白-核酸复合物摆得比 RFNA 好"到"AF3 能预测某蛋白能否把底物装上 tRNA"之间隔着本文完全没有覆盖的一步。本卡的 §6/§8 判读只允许引用到"几何假设的质量分级"这一层。
2. **本文没测任何蛋白-小分子配体体系**（第 1 节已钉死）。ATP/UTP/中间体作为游离小分子配体的结合姿态精度在本文是空白，禁止用 0.745/0.41 这类 PNA 聚合物数字给小分子配体场景背书或判死。
3. **不得把本文达标率当命中率**。27.5%、18.6%、2/23 这些数的分母是"有晶体结构可对照的 PDB 靶"，我们的靶是无同源标注、无实验结构的候选酶——分布不同，任何"成功率校准"都不成立。
4. **CASP16 的 ~1/4 抗体正确率、ipTM-DockQ 相关 0.81** 是蛋白互作场景的读数；本库判据标准禁止把 binder 类置信分阈值（ipTM 类）直接当酶活闸口，本卡同样不提供酶设计场景的替代阈值。
5. 本文无 MD/QM，因此它**既不能支持也不能反驳**"用 MD/QM 判催化"的路线；引它只为结构预测工具选型服务。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K43_PMC12661943_text.txt

- 本地纯文本：`fulltext/K43_PMC12661943_text.txt`（Europe PMC fullTextXML → 标签剥离、实体解码、空白折叠，未改写内容；同目录 `.xml` 为原始 XML，登记在 sources_map.json 但未参与逐字比对）。本卡**只声明这一份引句底稿**——同一论文若存在 NCBI 抽取版本，夹注的参考文献编号位置不同，跨版本逐字比对会假红。
- 对照底稿行号：`sources/cost-benchmarks.md:150`（先行调研仅题录级一行，本卡为全文级首读，无先行内容可沿用，也无冲突可对照）。
- CSV 字段映射：本文第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`；hit_rate 字段本卡填的是"模型达标率"口径并注明非实验命中率。
- **本卡自检**：`scripts/verify_literature_cards.py --only K43 --no-report` 把卡内所有不含中日韩字符、被直双引号包住、≥20 字符且 ≥12 字母的片段，在声明底稿里逐字查找（norm 后 NFC＋破折号/引号归一＋空白折叠）。写作过程中先用同一 `litcards_text.norm` 对 66 条候选句做过预检，发现 3 条因首字母大小写或断句位置差异 MISS（The average LDDT 句首大写、the Benchmark- VIII 句、The server and local versions 句），已按底稿原文修正后入卡；未做跨句拼接、未用省略号开头/结尾冒充引句、术语与状态名不加英文引号。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 60 条逐字引句来自许可受限的第三方来源（K43；CC_BY_NC），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（第三方回顾式基准评测，非设计方法、无湿实验）
target=九类体系：蛋白单体150/孤儿蛋白113/双构象60组/蛋白多聚体206/肽-蛋白80/抗原-抗体102/RNA 52/RNA多聚体23/蛋白-核酸复合物59；无蛋白-小分子配体集
backbone_generation=不适用（不生成候选；评测 AF3-server/AF3-local v3.0.1 对 AF2 v2.3.0、AlphaFold-Multimer v2.3.0、RoseTTAFoldNA、RhoFold+、NuFold、trRosettaRNA，均默认参数 top-1 对比）
computational_filters=无漏斗判据；用指标口径评模型质量：TM-score（US-align -TMscore 7 -ter 0）、LDDT（OpenStructure 0.5/1/2/4 Å）、DockQ、FNAT、INF（ClaRNA MCC）、CDR-TMscore；Wilcoxon 配对检验，RNA 比较 Bonferroni 校正
thresholds=TM>0.5 同拓扑；DockQ<0.23 incorrect、0.23–0.49 acceptable、0.49–0.80 medium、≥0.80 high；CDR-TM≥0.5；泄漏排除=对训练集相似度>40%且覆盖>80%剔除；晶体覆盖≥80%；RNA/PNA 复合物总残基<1000、链≥10 nt
md_used=否
qm_used=否
experimental_methods=无湿实验；唯一对照是 PDB 实验结构（回顾式基准，含 20 次随机种子重跑的稳定性抽查）
pipeline_counts=九套基准 150/113/60/206/80/102/52/23/59 靶；不稳定靶与双构象每版本 20 次×5 模型=100 模型/版本
hit_rate=模型对晶体结构达标率（非实验命中率）：抗原-抗体正确界面 AF3 27.5–28.4% vs AFM 9.8%；CDR 折对 18.6%；RNA 多聚体正确全局折叠 2/23（<10%）；PNA 界面接触过半 ~35.6% vs RFNA 16.9%；单序列模式 TM≥0.5 仅 26% vs 16%
best_metric=蛋白-核酸复合物 AF3-server 平均 TM 0.745（较 RoseTTAFoldNA +14.1%，P=1.04×10⁻⁵）；RNA LDDT 0.713/INF 0.814 全场最优
cost_or_stat_note=AF3 全类别最快：~20 min 单体/~31 min 多聚体/~47 min 抗体/~10 min RNA/~23 min PNA（对照 RoseTTAFoldNA PNA ~996 min）；统一硬件 NVIDIA A100 40 GB＋EPYC 7763、每任务 8 核 40 GB 内存
role_in_timeline=首个 AF3 全类别第三方基准：给出相对增益分级（抗原-抗体与蛋白-核酸 substantial、单体与 RNA 多聚体 minor、肽-蛋白不可区分）、server/local 随机性与 top-1 排名缺陷、以及九套集未测小分子配体的适用边界；为含核苷酸聚合物的复合物几何选型提供第三方证据，但不为催化能力提供任何证据
source_pointer=data/literature_cards/fulltext/K43_PMC12661943_text.txt（另有同名 fullTextXML.xml）；sources/cost-benchmarks.md:150
CSV回填-->
