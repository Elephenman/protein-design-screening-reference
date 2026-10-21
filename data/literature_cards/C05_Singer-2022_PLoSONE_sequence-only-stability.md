# [C05] 用"便宜、吵闹"的十万通量稳定性数据养一个只看序列的模型——曹龙兴 binder 漏斗的底层 assay 出处

Singer JM, Novotney S, Strickland D, Haddox HK, Leiby N, Rocklin GJ, Chow CM, Roy A, Bera AK, Motta FC, **Cao L**, Strauch EM, Chidyausiku TM, Ford A, Ho E, Zaitzeff A, Mackenzie CO, Eramian H, DiMaio F, Grigoryan G, Vaughn M, Stewart LJ, Baker D, Klavins E（24 人；Two Six Technologies + 华盛顿大学 +西北大学 + TACC + Dartmouth；曹龙兴第 11 位，作者贡献角色为 Data curation/Resources）
PLOS ONE 2022, 17(3):e0265020 · DOI 10.1371/journal.pone.0265020 · PMID 35286324 · PMCID PMC8920274（CC BY）
预印本 bioRxiv 10.1101/2021.03.12.435185 · 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8920274/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C05**（组：曹龙兴组） |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory.json 登记 fetch_channel=epmc_fulltext），2026-10-20 本地抓取 |
| 本地全文 | `data/literature_cards/fulltext/C05_PMC8920274_fullTextXML.xml`（335,315 B）；去标签纯文本 `data/literature_cards/fulltext/C05_PMC8920274_text.txt`（176,558 B） |
| 对照底稿 | `sources/cao.md` 第 100–114 行 |
| **底稿勘误（本卡以全文为准）** | 底稿第 113 行把 "less than 1% of designs achieved stability scores greater than 1" 归属为"**dTERMen 对照组**"。原文该句属于 Materials 里 Library 3 第三组——**用 Rosetta 替代 dTERMen 做 motif 连接与序列设计的那一组**，且原文明说这组 "this protocol was less successful than the dTERMen protocol"。即 <1% 是"Rosetta 连接组"的失败率，dTERMen 是本文的**成功基线**（与 Rosetta 专家设计同入训练集），底稿归属反了 |
| 门禁登记 | `sources_map.json` 的 C05 条目原只登记底稿，本卡写作时已把上述两份全文补进登记（与 inventory.json 一致） |
| 证据级别 | **全文级**（所有引句在本地纯文本逐字命中） |
| 未取到的部分 | S1–S39 补充图与表 1 之外全部图件原值；库设计的物理细节（芯片布局、引子序列）；凡涉补充图处本卡只转述正文自述 |

## 1. 这篇到底解决什么（一句话）

设计出的稳定蛋白在序列空间里"天文数字稀有"（"Stable designs, however, are astronomically rare within the space of all possible amino acid sequences."），逐个用物理打分评估又贵又不准——于是把**酵母展示蛋白酶解滴定 + FACS + NGS** 这个低精度但单次十万通量的 assay 自动化，攒出约 20 万条"序列→稳定性分"数据，训一个**只看序列**的 CNN（EM）当廉价判据、一个 NMT 生成器（GM）造新序列，再用 EM 引导的迭代点突变把任意设计**实测稳定性推高一个数量级**，全程不碰三维结构。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **训练数据根本不存在**（稳定性测量历史上是体力活）。应对："Here we use a high-throughput, low-fidelity assay to experimentally evaluate the stability of approximately 200,000 novel proteins."；"We used this combination of the existing assay and software-based automation to evaluate the stability of up to 100,000 proteins in a single experiment."（自动化=BIOFAB + Aquarium 软件）。 **代价**：作者明说 assay 吵闹——"There is relatively high experimental noise, the results depend on multiple assumptions and models, and stability values are limited by the protease resistance of the expression vector."；他们的取舍写在讨论里："Given that machine learning models tend to perform (and in particular to generalize) better with a high quantity of noisy data than with a low quantity of cleaner data, this assay is a good partner for machine learning methods."——**用噪声换通量是自觉策略，不是无奈**。
2. **测得的"抗蛋白酶性"混着折叠无关成分**：天然序列本身抗消化。上一作（Rocklin 2017，引文 26）用 unfolded-state model（USM）把这部分减掉；本文发现 "Because this correction is imperfect-for example, it only modestly improves agreement between trypsin- and chymotrypsin-derived stability scores-we reasoned that potential latent factors, such as the propensity of the sequence to form residual unfolded-state structures incompatible with binding to the active site of the protease, could also affect the cleavage resistance."。 **应对**：造更灵活的 USM（每个蛋白酶一个、学 100 个 kernel、取最大激活而非求和、并入 Library 2 的 scramble），并用两蛋白酶分数一致性验证分数优于裸 EC50。 **代价**：USM 仍是模型，"EM 可能钻 USM 的空子把分刷高而不真稳"成为贯穿全文的头号假阳性假说（见 §2.4）。
3. **模型可能只背下了"专家设计的印记"**（拓扑/方法学的序列 tell）。应对一：**留一类跨 27 个设计类别交叉验证**——"The EM achieved a mean R 2 of 0.17 over all classes, indicating that the previous results reflect some overfitting to topology or design methodology, but also demonstrating a substantial level of generalization."（同段对照：常规留 5000 测试集 "The mean R 2 score for the EM was 0.48 ( r 2 = 0.49), slightly better than the relationships between trypsin and chymotrypsin stability scores"，作者由此判断 "performance is near the limit imposed by the assay"）。应对二：用 BLAST 证明 27 类之间本就差异大（最大同源性均值 47.0±8.3%），且模型误差与类间相似度无相关。应对三：拿 7 组**天然蛋白**单点突变热熔数据外部体检："weak but consistently positive correlations between EM stability predictions and thermal stability"（表 1：r 从 0.363 到 0.019，多数 p>0.05——弱而一致）。 **代价**：跨类泛化 R²=0.17 远低于类内 0.48/0.52，作者承认对新类别只是"好于瞎猜均值"。
4. **担心 EM 的"优化"其实是欺骗 assay**（尤其 Refinement 疯狂加色氨酸：3276/5850 次引导突变是变 Trp）。应对是教科书级的一组三连：**（a）对照拆解**——"However, random mutations to tryptophan show virtually no change in assayed stability score (mean increase of 0.016), compared to a substantial increase in stability score when those substitutions are guided by the EM (mean increase of 0.215)."，结论 "Taken together, these observations show that increasing the tryptophan count of a protein in and of itself does not increase stability-the changes to tryptophan must be at the right location for the protein in question."；**（b）约束再优化**（Corpus C）——"This consisted of 97,702 proteins, including three sets representing refinements governed by increasingly stringent constraints."，依次禁止"降低 USM 预测 EC50"、禁 Trp（"Explicitly prohibiting tryptophan eliminated the 823 mutations to tryptophan seen in the least-constrained refinements, but otherwise altered the pattern of changes and their effects relatively little"）、禁八个非极性残基，收益仍在（详见台账）；**（c）负控集**——"We attempted to refine a set of randomly scrambled expert-designed proteins, with no success."，作者把这一步解读为"REFINE 不是把任意序列哄成分高"的证据："This failure to refine scrambles provides evidence that refinement is not merely changing arbitrary sequences in such a way that they fool the assay into viewing the sequences as more stable."
5. **不同批次/不同实验室/两代表达载体的数据不可比**。应对：用贯穿所有库的 ladder 校准蛋白做正交回归对齐批次——"For each chip and each protease, we performed an orthogonal regression between observed EC 50 values of ladder proteins on the new chip and observed EC 50 values of ladder proteins on the original four chips."；旧载体压顶（"beyond a certain value, the expression vector itself would start to suffer measurable cleavage"）→ 换抗蛋白酶进化载体扩动态范围，再用分段线性正交回归把新载体数据映射回旧载体空间（保证与训练集可比）；"This evolved vector expands the dynamic range of the assay."。 **代价**：所有绝对分数依赖校准函数，跨论文比较时"稳定性分"不是自然常数。
6. **EM 对单点突变幅度系统性低估**："The EM's predictions systematically underestimated the magnitude of mutational impacts, exposing limitations of the model."；对 Corpus B 的 14 类扰动，"the model systematically underestimated the impacts of these sequence perturbations"（正文措辞），但仍能把 14 类扰动按平均去稳强度排对（Spearman ρ=0.908）。 **应对**：不修模型，改用法——**只求排序正确，用 beam search 多轮小步迭代**（k=50、五轮）："Although this approach required the prediction of stability for hundreds of millions of primary sequences, the computationally efficient EM yielded these predictions in only a few hours using a single GPU." 成果 "On average, this iterative refinement increased assayed stability more than ten-fold (i.e., one stability score unit) after five single-site substitutions"。 **代价**：连最好的单蛋白相关都很弱（HEEH_rd3_0726 全单点图谱上 "The Pearson correlation coefficient between antilogs of predicted and experimental stability scores for this protein was only 0.419"）——多步收益与单点精度并存，机制上作者也没解释透。
7. **生成器（GM）没有三维/稳定性概念，怎么让它产出稳定序列？**："Note that the GM is simply learning to translate from secondary sequences to primary sequences; it knows nothing explicit about tertiary structure or stability."。应对三件：训练集只用 Corpus A 的稳定富集子集并加权；用 **Reverse GM**（一级→二级，等价物是 PSIPRED）反向核验，按输入-预测二级结构一致性选 1000 条（"We selected 1000 GM designs with the highest agreement between the input secondary structure and the Reverse GM's predicted secondary structure"，同时承认 "Note that this selection process further encourages sequences to be similar to those in the training set."）；报告 perplexity 基线（对照 RNN 1.8、机遇 19、GM 1.1："it achieves a perplexity of 1.1-by considering secondary structure information"）。 **代价**：筛选偏向训练集相似——为处理"新颖性"，另按 BLAST 身份分层报数（见 §2.8）。
8. **稳定与新颖不可兼得**。应对：分层记账——"Of the 993 designs that expressed at a detectable level, 275 had a maximum identity less than 95% and 47 of these 275 (17%) had an empirical stability score greater than 1.0"；"Of the 120 designs with a maximum identity below 75%, 17 (14%) were stable."；Corpus C 直接要求 GM 设计对专家最近邻 <50% 身份（"All GM designs on this chip were required to have less than 50% sequence identity with the most similar expert-designed protein, and all refinements used a new version of the EM trained on Corpora A and B."），再用 EM 精炼拉起来；策略总结 "It is also possible to sacrifice stability performance for novelty, generating marginally stable but highly distinct proteins (with < 50% amino acid identity to their nearest neighbors in the training set) that can then be stabilized through EM-guided refinement."。 **遗留**：拓扑覆盖不全——"The GM produced stable sequences for six of the nine topologies that were represented by at least 500 designs in the training set."（九个才成六，另三个为什么不行，本文未解决）；Rosetta 连接组 <1% 的失败也未给机理解释。
9. **EM 长不了（架构+数据都只覆盖 ≤65 残基小蛋白）**：讨论承认 "While the current EM is limited by both architecture and training data to small proteins"，且正文明说这套稳定性 assay 对至少某些较大蛋白已经不再与 ΔG unfolding 相关（该句含 Δ 符号，未作引句登记）。**本文未解决**，只列了需要新 assay + 更大数据。

## 3. 方法与工作流程（每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **实验判据**：酵母表面展示 + 胰蛋白酶/糜蛋白酶浓度滴定 + FACS + NGS → 每蛋白酶 EC50 → USM 校正 → 稳定性分 = min(两蛋白酶分)；分>1.0 记 stable。
- **预测器 EM**：三层卷积 CNN（one-hot 23×175 输入），双输出头（稳定性分 + 二级结构，多任务）；训练时混入天然蛋白三元组（天然 vs 其 scramble 的排序惩罚，无标签）；22,354 条 25–65 aa 天然序列入训。
- **生成器 GM**：神经机器翻译式 attention encoder-decoder，二级结构序列→一级序列；配套 Reverse GM 做一致性核验。
- **精炼**：EM 引导的 beam search（每轮对全部单点突变打分，k=50 保留为新基底，五轮）；Corpus C 加约束版（禁降 USM/禁 Trp/禁非极性组）。
- **物理侧对照**：无能量函数参与打分（Rosetta 只在"造训练数据"的上游出现）。**MD、QM 全无**；Rosetta 属经典能量近似，不是量子化学。
- **结构复核（末端、少量）**：E. coli 表达 + IMAC/SEC/质谱 + CD 热熔 + 一个结晶结构；AF2 与 trRosetta 只做事后比对。

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | 专家设计（Rosetta/dTERMen）序列 | 自动化 assay：合成寡核苷酸库→酵母展示→双蛋白酶滴定→FACS→NGS→EC50→USM 校正 | 判据：稳定性分 >1.0 记为稳定（原文口径 "empirical stability score greater than 1.0"）；EC50 置信区间宽度≤2 方可入分析 | 训练母库 Corpus A："This model was trained on a corpus of 107,948 proteins"；另约 20 万条新测定 |
| W2 | Corpus A | 训 EM；留 5000 随机设计做测试（训练 5 次取均值） | R²（严于 r²，可负） | 类内 "The mean R 2 score for the EM was 0.48 ( r 2 = 0.49), slightly better than the relationships between trypsin and chymotrypsin stability scores"；"performance is near the limit imposed by the assay" |
| W3 | 同上 | 27 类（拓扑×方法×长度）留一类交叉验证 | 类外 R² 均值 | "The EM achieved a mean R 2 of 0.17 over all classes, indicating that the previous results reflect some overfitting to topology or design methodology, but also demonstrating a substantial level of generalization." |
| W4 | 7 组天然蛋白单点突变热熔文献值 | EM 预测分 vs 实测 Tm 相关（表 1） | Pearson r（原文承认弱） | "weak but consistently positive correlations between EM stability predictions and thermal stability"（CspB r=0.363…STI-2A r=0.019，多数 p>0.05） |
| W5 | 测试集 5000 设计 | 造 Corpus B：14 类扰动（单点替/插/删、倒序、循环移位、删半）+ 精炼 + GM 设计，共 "of 96,799 designs, which fell into three main categories"；全部实测 | 分析仅取 CI≤2 者："We analyzed the 45,840 of these designs for which the credible intervals for both measured protease EC 50 values were no greater than 2." | 45,840 条上 "Across this set of designs, the EM's predictions were highly consistent with the observed stability scores ( R 2 = 0.52, r 2 = 0.59, Fig 2B and 2C )"；扰动排序 ρ=0.908 但幅度低估 |
| W6 | 1215 个测试集设计 | EM 引导 beam search 五轮（k=50） | 判据=预测稳定性分排序；成本 "Although this approach required the prediction of stability for hundreds of millions of primary sequences, the computationally efficient EM yielded these predictions in only a few hours using a single GPU." | "On average, this iterative refinement increased assayed stability more than ten-fold (i.e., one stability score unit) after five single-site substitutions"；"raised the mean stability score from 0.23 in the base population (green) to 1.27 after five amino acid changes, as compared to random substitutions (blue) which dropped it to -0.06"；随机对照 0.23→-0.06 |
| W7 | Corpus A 稳定富集子集 | 训 GM（二级→一级 NMT）+ Reverse GM（一级→二级） | Reverse GM 字符错误率 "achieves a secondary-sequence character error rate of 0.67%"，类外 "Even when evaluated on topologies that the model was not trained on, it achieves a CER of 9% for secondary sequence."；GM 困惑度 "this control model achieved a perplexity of 1.8."、"A perplexity of 19 would indicate chance"、GM "it achieves a perplexity of 1.1-by considering secondary structure information" | 高速产出：讨论句 "This approach is able to generate hundreds of thousands of designs, of comparable stability to those generated by experts using Rosetta, in a day." |
| W8 | GM 输出 | 按 Reverse GM 一致性选 1000 条入 Corpus B 实测 | "We selected 1000 GM designs with the highest agreement between the input secondary structure and the Reverse GM's predicted secondary structure" | "Of the 993 designs that expressed at a detectable level, 275 had a maximum identity less than 95% and 47 of these 275 (17%) had an empirical stability score greater than 1.0"；"Of the 120 designs with a maximum identity below 75%, 17 (14%) were stable."；"The GM produced stable sequences for six of the nine topologies that were represented by at least 500 designs in the training set." |
| W9 | GM 1000 条 | EM 精炼（与 W6 同法） | 稳定性分升幅 | "with a mean of 0.67; EM-guided refinement further increased it to 1.67"（=十倍，因分数是对数标度）；"Guided substitutions overall yielded ten-fold increases in the stability of GM designs"；"This demonstrates that we are able to design and iteratively improve highly stable proteins de novo, using an automated, rapid pipeline." |
| W10 | 全部引导/随机单点事件 | 逐"替换类型"统计成败 | 引导 70.7% 提升 vs 随机 56.9% 下降 | "guided substitutions increased stability score 4138 out of 5850 times (70.7%); the mean stability change over all guided substitutions was 0.208"；"Random substitutions, meanwhile, decreased stability score 2731 out of 4798 times (56.9%); the mean stability change over all random substitutions was -0.074"；Trp 集中现象 "it was the amino acid of choice in 3276 of the 5850 guided single-site substitutions" |
| W11 | 专家+GM 设计 | Corpus C 三层约束精炼（97,702 条） | 约束1：USM 预测 EC50 不得降；约束2：禁 Trp；约束3：禁 A/F/I/L/M/V/W/Y 八种非极性 | "This consisted of 97,702 proteins, including three sets representing refinements governed by increasingly stringent constraints."；引导-随机差 0.6（专家）/0.51（GM）/0.56（禁 Trp）分单位，专家禁非极性组四轮后仅 -0.22 |
| W12 | 12 条人工挑选（低身份+多样+代表株） | 台式复核：E. coli His6-IMAC、SEC、质谱、CD 光谱与热熔、结晶 | 可溶/单体/热熔>99°C | "Eight of the designs were expressed as reasonably soluble proteins and seven of those were monomeric as judged by size exclusion chromatography (SEC)."；"Five of the eight monomeric/oligomeric designs are highly thermostable ( S24 Fig ); four do not unfold even at a temperature of 99°C."；nmt_0994_guided_02 "EM-guided refinement then changed two residues to tryptophan, which raised the empirical stability score from -0.18 to 1.88."；晶体 vs AF2 "The prediction and the crystal structure have a C α RMSD of 3.4 Å"，vs trRosetta 3.7 Å |

**流程骨架一句话**：把判据的**单价**打到地上（EM 一次 GPU 小时出上亿预测："the ability to generate on the order of 100,000,000 predictions per GPU-hour"），再用通量把**标签**喂饱（一次实验十万条），最后用带约束与负控的精炼证明"便宜判据没被骗"。

## 4. 关键数字台账

| 数值 | 含义 | 出处 |
|---|---|---|
| ~200,000 / 100,000 每条实验 | 评估过的 novel 蛋白总数 / assay 单实验通量 | §2.1 |
| 107,948 | Corpus A 训练集规模 | W1 |
| 0.48（r²=0.49）vs 0.34/0.38（r²=0.47） | EM 类内 R² vs 两蛋白酶分互相的一致性（≈噪声上限） | W2 |
| 27 类 / 0.17 | 跨类交叉验证类别数与平均 R² | W3 |
| 47.0±8.3% / 34.5±5.1 | 跨类 BLAST 最大身份与最大 bit score（均值±SD） | §2.3 |
| 96,799 / 45,840 | Corpus B 总数 / 进入分析数（CI≤2） | W5 |
| R²=0.52、r²=0.59 | Corpus B 上 EM 表现 | W5 |
| ρ=0.908（p=7.30×10⁻⁶）/ 0.432 | 14 类扰动排序 / 单蛋白排序能力 | W5 |
| 0.23→1.27 vs -0.06 | 专家设计五轮引导 vs 随机的均分 | W6 |
| 0.419；2.25/1.89 倍 | HEEH_rd3_0726 单点相关；该蛋白 3/4 引导突变实测增益 | §2.6 |
| 1.1 / 1.8 / 19 | GM / 对照 RNN / 机遇的困惑度 | W7 |
| 0.67% / 9% | Reverse GM 类内/类外字符错误率 | W7 |
| 1000→993→275→47（17%）；120→17（14%）；6/9 拓扑 | GM 设计漏斗分层计数 | W8 |
| 0.67→1.67 | GM 群引导精炼前后均分 | W9 |
| 4138/5850（70.7%）；2731/4798（56.9%）；0.208 / -0.074 | 引导/随机单点成功率与均变 | W10 |
| 3276/5850；+0.016 vs +0.215；191 类型中 148 引导更优；24 显著中 23 引导 | Trp 集中度；随机-到-Trp 对照；替换类型分解 | W10、§2.4 |
| 97,702；0.6 / 0.51 / 0.56 / -0.22；823 | Corpus C 规模；三约束档引导-随机差；禁 Trp 消除的原 Trp 突变数 | W11 |
| 8/12 可溶、7/8 单体、5/8 高热、4 个 99°C 不展开；-0.18→1.88；3.4 Å / 3.7 Å | 台式复核与晶体 | W12 |
| 100,000,000 预测/GPU·h | EM 吞吐 | 流程骨架句 |
| 22,354 条 25–65 aa 天然序列 | EM 辅助训练数据 | 工具箱 |
| <1% | Rosetta 连接组（非 dTERMen 组）稳定性分>1 的比例 | §0 勘误、W1 语境 |

## 5. 结论——作者说了什么

1. 序列-only CNN 预测稳定性可达 assay 噪声上限（类内 R²≈0.5），跨类仍"好于预测均值"；预测速度比物理方法快数量级以上（1e8 预测/GPU·h），可直接嵌入现有设计管线当补充。
2. EM 引导的五轮 beam search 把专家设计与 GM 设计的实测稳定性都提高一个数量级（分数 +1.0 单位），且带约束（禁 USM 降、禁 Trp、禁非极性）依然成立；随机扰动方向相反。
3. GM（二级→一级翻译）能产出与专家设计稳定性相当的新序列；以牺牲相似性换新颖性（<50% 身份）后仍可靠 EM 精炼拉回。
4. 台式复核证明这条纯数据管线产出的是"可溶、单体、耐热、按预期拓扑折叠"的真蛋白（一个结晶结构）。
5. 作者自限：EM 低估突变幅度、有对拓扑/方法过拟合残余、受噪声与载体上限约束、只适用于小蛋白；scramble 精炼失败划定能力边界（"there may be some degree of baseline plausibility to the unstable GM designs, which random scrambles do not possess, that permits successful refinement"）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的真正产品是"判据审计"方法**：约束式精炼（W11）+ scramble 负控（§2.4c）+ 类外交叉验证（W3）三件套，回答的是"这个便宜判据是不是在骗我"。我们的 xTB/MD 打分进漏斗前，应当同样配"应该骗不过判据的构造"（失活突变、乱序骨架、无催化几何的假阳集）——这正是我们 DP2R 缺的"筛子考卷"的**负样本版本**。
2. **"排序对但幅度错"够用**：EM 单点预测差（0.419）不妨碍 beam search 成功。对 UAA 的启示：机制判据不要求能量绝对值准，只要**候选间相对排序**稳定，就可以做小步迭代筛选；但这条只在"判据与目标确有弱相关"时成立（GM 之成立以 17%/14% 打底为限）。
3. **命中率永远按新颖性分层报**（95%/75%/50% 身份三档）。我们引用他人"X% 成功"时必须先问同源度口径——C05 自己就演示了：同批 GM 设计，全量口径和 <75% 身份口径的"稳定率"差着来源。
4. **曹龙兴在这篇只是数据提供者**，但其 assay 正是 C02 那个 84,690 骨架库预筛（34,507 条过稳定线）的底层工具——即"他后来 binder 漏斗的便宜第一闸"出自这篇。理解他为何信任大规模预筛，要看这篇对噪声的自觉取舍，而不是只看 binder 论文本身。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：类外泛化 R²=0.17；扰动幅度系统性低估；数据噪声大、依赖 USM 与载体上限；只限小蛋白（≤65 aa），并明确指出 assay 对较大蛋白与 ΔG unfold 不再相关；Trp/组成偏置未从根上消除，只是"约束后仍然有效"。
- 我们读出：① "稳定"判据本身是**群体层面**的（FACS 富集频率→EC50 曲线），单分子折叠路径不奇异性，与需要"事件级"读出的 UAA 化学确认不同型；② 17%（<95%身份）与 14%（<75%身份）分母是"表达可检出者"，若从 1000 下单数直接算只有 4.7%——两种口径都出现，引用必须写分母；③ 9 拓扑只成 6、Rosetta 连接组 <1%：这两处失败作者未给机制解释，属于"未解决"而非"已解决"；④ 全文无 MD/QM，"为什么 Trp-在表面有效"这类物理解释缺席。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **判据审计三件套**（类外交叉验证 / 约束式使用 / scramble 负控）——直接照搬进 DP2R：任何新打分（xTB 垒高、MD 接触指纹、序列 motif 分数）上线前先过"应该骗不过"的构造集。
2. **排序即够用**的 beam search 思想：对少数有活性的候选做"单点突变全库打分→保留头部→小步迭代"，用相对排序而非绝对能量。
3. **成本-通量对表**：EM 的卖点=单价（1e8 预测/GPU·h）×标签免费（一次实验十万条）。我们做每个判据都先报"每通过一个候选的核时"，再决定是否入漏斗（B09 效率公式的下界版）。
4. **新颖性分层报数**（身份档 bin）作为报告规范。

**不可迁移（为什么不能照搬）**

1. **稳定性分>1.0 是"抗蛋白酶滴定"群体口径，不是酶活、不是催化**。把它类比成"UAA 掺入成功率 17%"直接违反 DP2R 禁令——C05 没有任何化学事件读出，folded≠functional 在这里比在 binder 里更强（连结合都不测）。
2. **EM/GM 只看序列**，对"活性位点几何"零信息；UAA 的判据核心恰是几何与电子结构（Asn 位点、ATP 结合口袋、环化竞争），序列-only 模型没有可迁移的命中率证据。
3. **十万级通量来自展示文库富集**，LC-MS/MS 无法复制；"20 万条标签数据养判据"的前提在 UAA 不存在（我们连正样本都没有），所以 C05 的"数据换精度"路线对我们是**未来时**，不是现在时。

## 9. 溯源与自检

- 本地纯文本：`fulltext/C05_PMC8920274_text.txt`（Europe PMC fullTextXML 剥离归一，未改写）。
- 引句底稿: data/literature_cards/fulltext/C05_PMC8920274_text.txt
- 底稿指针：`sources/cao.md:100–114`（含 §0 所述归属勘误）；与 C02 骨架库（84,690/34,507）的承接关系见 `sources/cao.md` C02 卡第 71 行。
- CSV 字段映射：§3 ↔ 候选生成方法/计算筛选判据/阈值数字；§4 ↔ 候选数递减/实验命中率/成本统计；§8 ↔ 在方法演进链的位置。
- 引句全部从本地全文复制，写卡前经 111 条候选预检（0 缺失），门禁复跑结果见交付回报。

<!--CSV回填
work_type=论文（方法学/数据平台）
target=通用 mini-protein 稳定性（≤65 残基，拓扑 HHH/EHEE/EEHEE/HEEH 及 beta-grasp/ferredoxin/thio 等，非特定功能蛋白）
backbone_generation=Rosetta 与 dTERMen 专家设计（训练母库）+ GM（NMT attention encoder-decoder，二级结构→一级序列，Reverse GM 一致性选设计）
computational_filters=EM：序列-only 三层 CNN（多任务：稳定性分+二级结构，混天然蛋白三元组训练）；按预测分做 beam search 引导精炼（k=50、五轮）；Corpus C 约束版（禁降 USM EC50/禁 Trp/禁八种非极性）；跨 27 类留一类交叉验证
thresholds=stable=稳定性分>1.0（min 两蛋白酶）；分析要求两蛋白酶 EC50 置信区间≤2；BLAST 身份分层 <95%/<75%/<50%；GM 选择=输入与 Reverse GM 二级结构一致性最高 1000 条；显著性 t 检验 p<0.05（未校正）
md_used=否
qm_used=否（Rosetta/dTERMen 为经典能量函数，非量子化学）
experimental_methods=酵母展示+双蛋白酶浓度滴定+FACS+NGS（单实验十万通量，BIOFAB+Aquarium 自动化，USM 校正出稳定性分，ladder 正交回归跨批校准，进化载体扩动态范围）；E. coli 表达 IMAC/SEC/质谱、CD 热熔、1 例结晶结构（对照 AF2/trRosetta）
pipeline_counts=Corpus A 107,948（训练）→Corpus B 96,799（其中 45,840 入分析）→Corpus C 97,702；总计约 200,000 novel 蛋白实测；GM 1000→993 表达可检出→275（<95% 身份）→47 稳定（17%）→12 台式复核（8 可溶/7 单体/5 耐热/1 结晶）；<75% 身份层 120→17（14%）
hit_rate=GM 新颖子集稳定率 47/275=17%（低同源层）与 17/120=14%（<75% 身份层），分母为可检出表达者；EM 引导单点 70.7% 提升（4138/5850）、随机 56.9% 下降（2731/4798）；Rosetta 连接组 <1% 稳定（底稿误记为 dTERMen 组，本卡已勘正）
best_metric=nmt_0994_guided_02 稳定性分 -0.18→1.88（两次引导 Trp），99°C 不展开，晶体 vs AF2 C α RMSD 3.4 Å；EM 预测精度 R2=0.52（Corpus B），类外均值 R2=0.17；跨批与天然蛋白仅弱相关（表1）
cost_or_stat_note=EM 约 1e8 预测/GPU·小时；1215 设计×五轮 beam search=数亿序列预测仅单 GPU 数小时；一次 assay 十万蛋白；R² 5 次重训取均值；扰动排序 ρ=0.908；scramble 负控全部失败
role_in_timeline=曹龙兴线（挂名数据提供者）的"便宜第一闸"底座：其蛋白酶解滴定-FACS-NGS assay 成为后续 binder 管线骨架库预筛（C02 的 84,690→34,507 稳定）与稳定性判据的数据工厂；方法论上确立"低精度高通量数据+序列模型排序+约束/负控审计"范式，是 B09 式筛子审计的先声（早于其发表且同用真/负样本对照思想）
source_pointer=data/literature_cards/fulltext/C05_PMC8920274_text.txt；sources/cao.md:100-114（归属勘误见 §0）
CSV回填-->
