# [K40] PPIscreenML：先造一张"结合/不结合"的难考卷，再训一个判结合的打分器

Mischley V, Maier J, Chen J, Karanicolas J（Fox Chase Cancer Center / Drexel University / Triana Biomedicines / Temple University）
eLife 2026 · DOI 10.7554/eLife.98179 · PMCID PMC13099138 · PMID 42012336 · 预印本 10.1101/2024.03.16.585347（PMC10979958）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K40**（组：通用方法学; 口径对照 · 文献类型=方法） |
| 论文标题（全文正文题） | PPIscreenML is a method for structure-based screening of protein-protein interactions using AlphaFold（版本记录题名）；正文另有一行短题 PPIscreenML: Structure-based screening for protein-protein interactions using AlphaFold（预印本题名残留），两者指同一篇 |
| 身份核验 | 开写前读底稿开头 600 字符：含 `PMC13099138`、`42012336`、`10.7554/eLife.98179`，题名与作者（Mischley / Maier / Chen / Karanicolas）与本行 CSV 一致 ⇒ 认定为本行全文 |
| 本地全文（本卡唯一比对底稿） | `data/literature_cards/fulltext/K40_PMC13099138_text.txt`（69,243 B，单行；SHA-256 `e5c2a1d670153f1a…`）；同源 XML `fulltext/K40_PMC13099138_fullTextXML.xml`（SHA-256 `763622c4800b864a…`，门禁按规则排除 .xml） |
| 取回通路 | inventory.json 记录 `fetch_channel=epmc_search_then_fulltext`（Europe PMC 按 DOI 检索后取全文） |
| 证据级别 | **全文级**——本卡全部英文引句均在该底稿里逐字命中（第 9 节） |
| **口径变更留账** | CSV 行的 `证据级别` 列现在仍写 **摘要级（旧值）**，那是全文取回之前记的；本卡按**全文级**写。`证据级别` 列不在 14 键回填范围内（14 键里只有 work_type/target/… /source_pointer），**未擅自动表**，CSV 保持原样待总表负责人回填 |
| 对照底稿 | `sources/cost-benchmarks.md` §3.9（第 147 行，当时只有题录＋摘要级描述）＋ §交叉对照表第 201 行。凡与全文不符处记入第 7 节，一律以全文为准 |
| 本文不含 | 没有任何湿实验由作者本人完成；TNFSF 案例的"真值"取自他人已发表的流式细胞实验（Bossen 2006）；无 MD、无 QM、无自由能计算 |
| 未取到的部分 | 补充图（Figure 1-fig-suppl 1–4、Figure 2-fig-suppl 1–4）的原图与逐复合物打分表；Table 1 只拿到文本版数字（已录入第 4 节）；GitHub 仓库正文未展开（评审人指出仓库缺模型文件，见第 7 节） |

## 1. 这篇到底解决什么（一句话＋大白话）

**一句话**：AF2 无论你丢进去的是不是真相互作的两个蛋白，都会照样吐出一堆结构，所以"这两个蛋白到底结不结合"没有直接可测的量；这篇造了一个**专门冲着这个判别任务去训练/评测的监督分类器 PPIscreenML**（吃 AF2 置信度描述子＋Rosetta 能量项），并先造出一套"很难的负样本"当考卷。

大白话拆解：

- 现有做法是把"评价模型质量"的分数（pDockQ、iPTM）拿来当"是否相互作用"的证据用，作者指出这些量当初不是为了这个任务开发的，"there have been no rigorously benchmarked methods for this task"（摘要原句）。
- 作者的定位差别在训练目标本身："PPIscreenML is deliberately and intentionally trained/tested to distinguish between models of interacting proteins and compelling decoy pairs"——不是先打分再看顺不顺眼，而是把"结合/不结合"当成有标签的二分类去优化。
- 难点在**负样本从哪来**：没人能证明一对蛋白"不结合"，于是他们用结构相似但不配对的方式合成"诱饵复合物"（decoy），故意做到"不容易用 trivial criteria 排除"，逼模型去学细粒度界面线索（第 2 节第 1 条）。
- 最终成品是一个只用 **7 个特征**的 XGBoost 分类器（从 57 个特征里筛出来），在同一套留出测试集上 AUC 0.884，胜过 iPTM 0.843 与 pDockQ 0.710；再拿训练里完全没出现过的 TNFSF 配体/受体家族（18×28=504 对）做外推 benchmark，AUC 0.93。
- 一句话价值判断：**它贡献的不是模型复杂度，而是"负样本该怎么造 + 判别器该怎么评"的口径**。模型本身简单到只有 7 个特征，这一点比 XGBoost 更值得记。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **难点一：负样本没法真造——没人能证明一对蛋白「不结合」。**
   现象/证据：作者明确说训练集的关键是编译 active 与 decoy 样例，而 decoy 必须是"结构上像真的、但按前提不配对"的一对；他们的策略是故意把负样本做难："our approach seeks to build highly compelling decoy complexes, so that the resulting model is challenged to distinguish actives from decoys that cannot be resolved using solely trivial criteria"。
   他们做了什么：不随机配负样本，而是拿每个已知复合物当模板，把两条链各自替换成"结构最像的另一条链"（TM-score 最近邻）；如果两个最近邻恰好来自同一个复合物（那等于造出一个真互作对），就退到次近邻——"the analogs with the second-best TM-scores were used to generate a new decoy pairing"。
   仍留下的代价：负样本标签是**推断的**（结构相似 ⇒ 假定非 cognate），不是实测的"不结合"。公开评审直接打在这里，Reviewer 1："In my opinion, this set rather presents a set of non-cognate or weekly interacting protein pairs"（原文如此，weekly 为原文笔误，本句按底稿逐字照录）。也就是说 0.884 这个 AUC 度量的是"能否把 cognate 界面从**结构近亲**里挑出来"，而不是"能否判出真实不结合"。本文未解决。

2. **难点二：造负样本的方法自带一个尺寸偏置，模型会作弊。**
   现象/证据："The method we describe for building compelling decoy complexes does exhibit a slight bias for building decoy pairs from component proteins larger than the starting template"（原因是 TMalign 给长链查询更容易拿到高分）。
   他们做了什么：把它当成泄漏来堵——"This artifact can allow a model to 'cheat' if it includes any features that can serve as a proxy for the total number of residues in a model; accordingly, we ensured that no such features were included in developing PPIscreenML"，并把任何显式随总尺寸缩放的特征剔除："such features were excluded from our study"。
   仍留下的代价：靠"人工保证不含尺寸代理特征"，是纪律不是机制；特征表里 33 个 counting 特征与尺寸弱相关的风险并未被量化（补图 Figure 1-figure supplement 4 只给了直方图）。跨到别人复用时，这个约束不会自动继承。

3. **难点三：AF2 自己会把真互作对折错，脏样本要不要进训练？**
   现象/证据：训练只保留 DockQ≥0.23 的活性模型，这一步"Filtering on model quality in this manner excluded 932 models from training, leading to a total of 6473 active models with median DockQ value of 0.88"。
   他们做了什么：训练/验证侧过滤，**测试侧反而不过滤**，故意让错构模型留在考卷里——"To ensure a realistic estimate of the performance that can be expected in future prospective experiments, complexes with structures that were mis-predicted by AF2 were not excluded from the test set"；并且保留全部过阈模型而不只留最高分那个，用来掺噪声："Keeping all models with a DockQ score greater than 0.23 rather than taking only the model with the highest DockQ score allowed us to introduce some noise into our training dataset"。
   仍留下的代价：测试集 AUC 同时混着两种失败（AF2 折错 / 分类器没认出来），作者自己承认"the test set performance thus reflects more than the success of PPIscreenML"。他们靠换版本对照（AF-PTM、AF-Multimer v2.2 稍差）把差距归因到折错率上升："In both cases, the AUC values were slightly worse than for AF-Multimer v2.3, but analysis of incorrect predictions shows that this difference can be traced to the fact that AF-PTM and AF-Multimer v2.2 build mis-docked models of active complexes slightly more often than AF-Multimer v2.3 does"——归因是相关性观察，不是干预实验。

4. **难点四：类别先验被人为设成 1:1，与真实筛选的信噪比差几个数量级。**
   现象/证据：正文引言自己给出量级——"the human interactome is estimated to contain between 74,000 and 200,000 protein interactions"，而配对空间是天文数字；基准集却是活性与诱饵近乎等量。Reviewer 3 点破："In the benchmark set, the authors used about 1:1 ratio of positive (active) and negative controls"，并补："However, in real-life applications, the signal-to-noise ratio of PPI screening is very low"。
   他们做了什么：不报单一准确率，改报**阈值→指标曲线**（Table 1），让使用者按场景挑操作点："The use of a high (stringent) threshold value yields high precision but poor recall"（蛋白组级粗筛）与 "a lower (less stringent) threshold value yields poorer precision but improved recall"（家族内补全）；讨论里也承认放大到全蛋白组必须先解决阈值口径："this will allow for defining thresholds that ideally balance precision and recall"。
   仍留下的代价：precision 一列仍是**基准条件下的数字**，换成真实富集度会整体塌陷（1:1 下阈值 0 时 precision 恰好 0.50，即瞎猜水平，见第 4 节）。作者未提供低富集度仿真，"本文未解决"这一条他们自己在讨论里也没做完。

5. **难点五：同一个复合物有 5 个 AF2 模型，极易信息泄漏。**
   现象/证据："training on one AF2 model of a given complex then using a different model of the same complex in the test set would introduce obvious information leakage"。
   他们做了什么：以复合物为单位整体分配 split——"To avoid this, all five models for a given complex were together placed in either the training set or the validation set or the test set"，交叉验证同样按复合物分："Stratified fivefold cross-validation was used for the training and validation sets"。
   仍留下的代价：这条纪律在文中**写得自相矛盾**——Results 段写 "In each case, models were trained using fivefold cross-validation within the test set and applied to a validation set that was not included in each fold of training"，而 Methods 写 "All model optimization (selecting the framework, feature reduction, and hyperparameter tuning) was carried out using the validation set to define the best model, and not ever the test set"。两句互相冲突（前者若按字面成立，测试集就被用于模型选择了）。我们无法从正文判断 0.924 到底是在哪个集合上做 CV 得到的；以 Methods 口径为工作假设，但这是**未闭合的记录缺陷**（第 7 节再记一次）。

6. **难点六：模型只在二聚体上训练，可 TNFSF 是三聚配体＋三个受体的 3:3 组装。**
   现象/证据：作者需要外推到超家族选择性 benchmark，而该体系"Given the shared arrangement of subunits in all complexes described to date, a 3:3 stoichiometry was assumed in all cases"，建模方式也随之改造："Because three receptor subunits separately engage the outside edges of the trimeric ligand, AF2 models included three copies of the ligand with one copy of the receptor"。
   他们做了什么：用实体映射把训练/使用口径接上——"Because PPIscreenML was trained on heterodimeric complexes, the three copies of the trimeric ligand were considered as the first entity and the receptor was considered as the second entity"；同时靠"训练与测试集只收二聚体"这一点保证 TNFSF 全程未被见过："Importantly for this benchmark, no TNFSF ligands or receptors were included in the development of PPIscreenML thus far, because the training and testing sets were restricted to dimeric complexes"。
   仍留下的代价：3:3 是**假设**（"a 3:3 stoichiometry was assumed in all cases"），界面特征只在"三聚体=第一实体"这一个人为切法下成立；换化学计量或换不对称复合体，实体边界要重设，判别口径是否仍一致没有测过。另外 456 条蛋白-肽复合物被整体排除在蛋白-蛋白训练集之外（第 3 节 W1），小界面情形不在其适用声明内。

7. **难点七：成本与算力约束直接砍掉了数据集与建模配置。**
   现象/证据：复合物建模很贵，作者因此限长——"Any heterodimeric complex with a total length greater than 1550 amino acids was filtered out of the dataset, due to our modeling capabilities at the time"，总算力开销为"Approximately 7700 GPU hours were used to build the AF2 models in this work"，硬件是"All models were built on ACCESS San Diego Supercomputer's Expanse NVIDIA V100 GPU processors"。
   他们做了什么：把约束写进纳入标准（长度上限、分辨率上限 3 Å、发布时间截点），并在 Methods 里明确建模配置（模板开、12 次 recycle、AMBER relax、每条 5 个模型）。
   仍留下的代价：>1550 aa 的大复合体从未进入训练与评测，作者用"at the time"承认这是当时算力限制而非科学结论；这条截断直接限制可外推的复合物规模范围。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **结构生成**：ColabFold Batch 跑的 AF-Multimer（Methods 建集段落写 v2，Impact of AF2 version 段落写开发与全部 benchmark 用 v2.3，两处不完全一致，见第 4 节版本行），每条复合物出 5 个模型。作者自述目标差异："PPIscreenML is deliberately and intentionally trained/tested to distinguish between models of interacting proteins and compelling decoy pairs"。
- **判别特征（三组共 57 个）**："7 features representing AF2 confidence measures, 33 structural 'counting' features, and 17 features from the Rosetta energy function"；界面残基的判定用 Cβ（甘氨酸用 Cα）到另一条链的距离阈值（原文给了数字，见第 4 节，因含非 ASCII 单位符号不入引句）。iPAE top ¼ 与 tPAE top ¼ 的取法在 Methods 里各有一句定义（同样是四分位取法，原文用分数符号 ¼，故不逐字入引）。
- **分类器**：七种常规 ML 框架横评，"we evaluated seven standard machine learning frameworks to build classification models"，最终选 XGBoost；其余为决策树、随机森林、KNN、逻辑回归、AdaBoost、Bagging。
- **参考/对照指标**：iPTM、pDockQ、PIscore（AlphaPulldown 里算的那三个），它们本是模型质量指标被挪用做互作判别——"performance for this task was only modest, however, presumably because development of pDockQ was fundamentally focused elsewhere"。
- **不用的方法**：全文无 MD、无 QM、无自由能计算；作者本人无任何湿实验，真值全部来自 PDB（活性）与他人已发表流式数据（TNFSF）。

### 工作流（W1→W12；阈值一律为原文数字）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| W1 正样本来源 | DockGround 库里的异源二聚复合物（"Heterodimeric protein complexes were downloaded from the DockGround database"） | 按发表月份/分辨率/类型/序列冗余/尺寸层层过滤：PDB 发表截至 01/26/23、最高分辨率 3 Å、去掉同源二聚体与抗体-抗原复合物、序列同一性上限 30%、总长上限 1550 aa、任一链 <50 aa 的移交给蛋白-肽子集 | "Upon filtering for a maximum of 30% sequence identity, there remained 1481 nonredundant protein-protein complexes with experimentally defined structures" | 1481 个蛋白-蛋白复合物（另有 456 个蛋白-肽复合物被分出，不进本模型）："After filtering, there were a total of 1481 protein-protein complexes and 456 protein-peptide complexes" |
| W2 AF2 复合物预测 | 1481 复合物的组分序列（直接从 PDB 取） | ColabFold Batch + AF-Multimer v2 建模 | 采样/回收配置为原文三项："Templates were used in building AF2 models, each model was recycled 12 times, and the AMBER relax step was included"；每复合物 5 个模型 | "we used the sequences of the component proteins to build five AF2 models for each of these 1481 nonredundant complexes"（MSA 具体参数原文未记录，只给了上述三项） |
| W3 正样本质检 | 7405 个活性 AF2 模型（5×1481，本卡推算） | 用 DockQ 对每模型算与实验结构的相符度，低于"可接受"就剔除 | "a DockQ score of 0.23 or greater is considered at least 'acceptable' quality"；"Complexes are included in the dataset only if their DockQ scores are at least 0.23, but most DockQ scores for these active pairings are much higher" | "Filtering on model quality in this manner excluded 932 models from training, leading to a total of 6473 active models with median DockQ value of 0.88" |
| W4 负样本（诱饵）构造 | 同一批 1481 复合物拆成单链池 | 每条链找全池里 TM-score 最近的**非自身**结构近邻，两条链同时替换 → 得到一个"形似活性"的新配对；若两个近邻恰好同属一个复合物则改用次近邻 | 近邻强度："87% of the proteins in our set were paired with a structural analog having TM-score greater than 0.5, a cutoff far beyond that which is observed between random protein pairs"；同复合物冲突处置："the analogs with the second-best TM-scores were used to generate a new decoy pairing" | 1481 个诱饵复合物，各再建 5 个 AF2 模型（配置同 W2）；序列层面已排同源，仍能找到近邻："Despite the fact that homologs had been excluded from our dataset on the basis of sequence identity, close structural matches could nonetheless be identified in most cases" |
| W5 划分与防泄漏 | 活性 + 诱饵全部复合物（各 5 模型） | 按复合物整体随机分三份；交叉验证也按复合物分组 | "To train PPIscreenML, data was partitioned using a 60/20/20 split"；泄漏理由与做法："training on one AF2 model of a given complex then using a different model of the same complex in the test set would introduce obvious information leakage" / "To avoid this, all five models for a given complex were together placed in either the training set or the validation set or the test set" | 训练/验证/测试三份；训练侧活性只留 DockQ>0.23 模型，验证与测试侧五模型全留 |
| W6 取描述子 | 全部 AF2 模型 | 三个 Python 脚本分别抽 AF2 置信度、Rosetta 能量（pyRosetta）、结构计数（BioPandas）三组特征 | 界面残基定义：一条链的 Cβ（Gly 用 Cα）与另一条链 Cβ 距离在 12 Å 内即算界面残基（数字见第 4 节，含单位符号不逐字入引） | 每模型一张 57 列特征表："7 features representing AF2 confidence measures, 33 structural 'counting' features, and 17 features from the Rosetta energy function"；显式随总残基数缩放的特征被剔除 |
| W7 选分类器 | 57 特征训练/验证数据 | 七框架横评 + 折内交叉验证 + 合并 AUC 排名 | "All seven models had similar performance, with XGBoost (an implementation of gradient-boosted decision trees) yielding the highest AUC value of 0.924"；调参项："Finally, the model was hyperparameter tuned on the following parameters: maximum depth, number of estimators, learning rate, gamma, regularized lambda, and minimum child weight" | 一个 XGBoost 基线模型（57 特征） |
| W8 特征削减 | 57 特征 XGBoost | 序列后向选择（sequential backward selection），只用验证集判停 | "This approach provided a model with only seven features that maintained the AUC of the model with all features when evaluated using the validation set"；"All model optimization (selecting the framework, feature reduction, and hyperparameter tuning) was carried out using the validation set to define the best model, and not ever the test set" | 7 特征模型：AF2 置信度 1 个（界面 PAE 前 ¼ 均值）＋结构计数 1 个（"one structural 'counting' feature (number of charged amino acids in the interface)"）＋Rosetta 5 个（含 "the average Lennard-Jones attractive score for interfacial residues"、"the average electrostatic score for interfacial residues"、"the proportion of interfacial residues involved in beta-sheet structures"） |
| W9 留出测试协议（与验证集两处不同） | 从未参与开发的 20% 复合物 | ①不按 DockQ 过滤（错构活性照留）；②按**复合物**计分：5 个模型都打分，取最高分定该复合物类别 | ①"To ensure a realistic estimate of the performance that can be expected in future prospective experiments, complexes with structures that were mis-predicted by AF2 were not excluded from the test set"；②每复合物取五模型最大值 | 57 特征 XGBoost："Applying the XGBoost model to the held-out test set with these conditions yielded an AUC value of 0.892"；7 特征模型："this 7-feature PPIscreenML model yields an AUC of 0.884, comparable to the full 57-feature model" |
| W10 与既有指标同台 | 同一份留出测试集 | 把 iPTM / pDockQ /（PIscore 在 AlphaPulldown 里可算）逐模型打分，同样取每复合物最高分 | 同一"按复合物取最高分"口径 | "its AUC value is 0.884, compared to AUC values of 0.843 and 0.710 for iPTM and pDockQ, respectively"；分离度差异："PPIscreenML assigns (correct) scores very close to either 1 or 0 for most of the actives or decoys, with clear separation between them" |
| W11 阈值-取舍表 | 7 特征模型在测试集上的分数分布 | 沿阈值扫描算 FPR/TPR/FNR/TNR/precision/recall/F1（Table 1），不钦定单一阈值 | 高端操作点："The use of a high (stringent) threshold value yields high precision but poor recall"；低端操作点："a lower (less stringent) threshold value yields poorer precision but improved recall"；原文 Table 1 直接读出的两个可用点：阈值 0.95 → precision 0.96 / recall 0.16；阈值 0.75 → precision 0.82 / recall 0.80 | 20 行阈值表（数字全录第 4 节） |
| W12 跨家族外推案例（TNFSF） | 18 个配体 × 28 个受体（序列取自 UniProt） | 每个配对按 3:3 计量建模（三拷贝配体＋一拷贝受体），AF-Multimer v2.3、模板、12 recycle、AMBER relax，每对 5 模型；配体三聚体算第一实体、受体算第二实体，再喂 PPIscreenML | 题量与真值："The TNFSF comprises 18 protein ligands and 28 receptors in humans, leading to 504 potential pairings"；"However, only 36 of these pairings are reported to show productive binding to one another, as observed in a comprehensive flow cytometry experiment"；未见过的保证："Importantly for this benchmark, no TNFSF ligands or receptors were included in the development of PPIscreenML thus far, because the training and testing sets were restricted to dimeric complexes" | "for 14 of the 18 TNFSF ligands, the receptor with the highest PPIscreenML score is indeed a true interactor"（Top-2 命中 17/18）；"the AUC value of 0.93 in this new benchmark is similar to that observed when applying PPIscreenML to the held-out test set of heterodimeric complexes (0.88)" |

**这套流程值得单独记住的三点骨架**：

1. **先造考卷再训模型**——数据集设计（W4 的"难负样本"）就是本文的主要方法学产出，模型只有 7 个特征。
2. **训练侧干净、评测侧脏**（W3/W5 vs W9）：他们故意让测试集保留 AF2 折错的活性样本，把"上游预测器失败"计入端到端表现，代价是 AUC 不再纯粹属于分类器。
3. **按实体整体划分 + 按复合物取最高分**（W5/W9）：前者防泄漏，后者是可直接照搬的筛查协议（同对一个 N 模型 → 取最优）。

## 4. 关键数字台账

除标注"本卡推算"外，以下数值均可在 `fulltext/K40_PMC13099138_text.txt` 里直接搜到。

| 数值 | 含义 | 出处（原文位置/片段） |
|---|---|---|
| 74,000–200,000 | 人相互作用组预计真互作条数（引言给的任务背景量级） | Introduction（引 Venkatesan 2009） |
| 65% / 10 个实验 | 回收 65% 真互作需合并 10 种不同实验（湿实验侧的痛） | Introduction（引 Choi 2019） |
| ≤3 Å / 01/26/23 / 30% / 1550 aa / 50 aa | 活性集五道纳入闸门：分辨率上限、PDB 发表截点、序列同一性上限、总长上限、肽链下限（后者移入蛋白-肽子集） | Methods - Set of active complexes |
| 1481 | 非冗余异源二聚复合物（活性集） | "Upon filtering for a maximum of 30% sequence identity, there remained 1481 nonredundant protein-protein complexes" |
| 456 | 被分出去的蛋白-肽复合物（不进本模型） | "After filtering, there were a total of 1481 protein-protein complexes and 456 protein-peptide complexes" |
| 5 | 每个复合物建的 AF2 模型数（活性与诱饵同） | "we used the sequences of the component proteins to build five AF2 models for each" |
| 12 / 模板开 / AMBER relax | 每个模型的 recycle 次数与建模配置三项 | "Templates were used in building AF2 models, each model was recycled 12 times, and the AMBER relax step was included" |
| 0.23 | DockQ"至少算可接受"的质量闸门（训练侧过滤用） | "a DockQ score of 0.23 or greater is considered at least 'acceptable' quality" |
| 932 → 6473 | 被剔除的活性模型数 → 保留的活性模型数 | "Filtering on model quality in this manner excluded 932 models from training, leading to a total of 6473 active models with median DockQ value of 0.88" |
| 0.88 | 保留活性模型 DockQ 中位数 | 同上 |
| 7405 | 活性模型总数（1481×5，**本卡推算，非原文数字**；与"932 剔除→6473 保留"精确自洽） | 本报告推算，用于第 7 节那条一致性观察 |
| 0.5 / 87% | 诱饵近邻的 TM-score 门槛与该门槛下的覆盖率 | "87% of the proteins in our set were paired with a structural analog having TM-score greater than 0.5" |
| 1481（诱饵） | 诱饵复合物数（每个活性造一个） | Figure 1 图注："Five AF2 models were built for each of these 1481 decoy complexes" |
| 60/20/20 | 训练/验证/测试划分比例 | "To train PPIscreenML, data was partitioned using a 60/20/20 split" |
| 57 = 7 + 33 + 17 | 初始特征总数 = AF2 置信度 + 结构计数 + Rosetta 能量 | "7 features representing AF2 confidence measures, 33 structural 'counting' features, and 17 features from the Rosetta energy function" |
| 12 Å | 界面残基判定：跨链 Cβ（Gly 用 Cα）距离阈值 | Methods - Feature extraction（含单位符号，故不入引句） |
| 7 种框架 | 横评的常规 ML 分类器数量 | "we evaluated seven standard machine learning frameworks to build classification models" |
| 0.924 | 57 特征 XGBoost 的合并交叉折 AUC（验证口径） | "All seven models had similar performance, with XGBoost (an implementation of gradient-boosted decision trees) yielding the highest AUC value of 0.924" |
| 57 → 7 | 序列后向选择后的特征数 | "The number of features was reduced using sequential backward selection, from 57 features to 7 features"（Figure 2B 图注） |
| 0.892 / 0.884 | 留出测试集 AUC：57 特征 / 7 特征（PPIscreenML 定稿） | "yielded an AUC value of 0.892" / "this 7-feature PPIscreenML model yields an AUC of 0.884" |
| 0.843 / 0.710 | 同一测试集上 iPTM / pDockQ 的 AUC | "its AUC value is 0.884, compared to AUC values of 0.843 and 0.710 for iPTM and pDockQ, respectively" |
| 0.87 | pDockQ 首次报道时自己那个（较易）分类实验的 AUC | "pDockQ provided an AUC value of 0.87 in its first-reported classification experiment" |
| Table 1 关键行 | 阈值 → precision / recall：0.98→1.00/0.00；0.95→0.96/0.16；0.9→0.85/0.39；0.85→0.85/0.60；0.8→0.83/0.74；0.75→0.82/0.80；0.6→0.79/0.89；0.5→0.78/0.93；0.21→0.73/0.95；0.05→0.67/0.97；0→0.50/1.00 | Results 段 Table 1（阈值列为 PPIscreenML threshold，其余列为 FPR/TPR/FNR/TNR/Precision/Recall/F1） |
| 0.50（阈值 0 时） | 1:1 基准下"全判为结合"的 precision = 瞎猜水平（第 2 节第 4 条的依据） | Table 1 末行 |
| 18 / 28 / 504 / 36 | TNFSF 配体数 / 受体数 / 全部配对 / 文献报道的真结合对 | "The TNFSF comprises 18 protein ligands and 28 receptors in humans, leading to 504 potential pairings"；"only 36 of these pairings are reported to show productive binding" |
| 14 / 18；17 / 18 | Top-1 命中真互作的配体数；Top-2 命中的配体数 | "for 14 of the 18 TNFSF ligands, the receptor with the highest PPIscreenML score is indeed a true interactor" |
| 0.93 | TNFSF benchmark 的 AUC | "the AUC value of 0.93 in this new benchmark" |
| 3:3 | TNFSF 建模假定的化学计量 | "a 3:3 stoichiometry was assumed in all cases" |
| v2 / v2.2 / v2.3 / AF-PTM | 建模版本；跨版本稳健性用 AF-PTM 与 v2.2（后两者 AUC 略低）。**注意原文两处口径不完全一致**：Methods 说复合物建模用 AF-Multimer v2，而 Impact of AF2 version 说"Development of PPIscreenML and all performance benchmarking used models built with AF-Multimer v2.3"，TNFSF 又写 v2.3——本卡照两处原文并列记录，不替作者圆场 | Methods - Set of active complexes / Impact of AF2 version / TNFSF case study |
| 7700 GPU·h | 本文全部 AF2 建模的算力开销 | "Approximately 7700 GPU hours were used to build the AF2 models in this work" |
| 0.44–0.52 GPU·h/模型（约 26–31 GPU·分钟） | 单价的**量级推算**（**非原文数字**）：分子取原文 7700 GPU·h，分母取模型总数——若只算活性＋诱饵为 2962×5=14810 个模型（0.52 h/个），若再计入 TNFSF 的 504×5=2520 个则为 17330 个（0.44 h/个）；原文没有拆分这两笔 | 本报告推算，输入全部来自上行两条原文数字（7700 GPU·h 与 5 模型/复合物） |

## 5. 结论——作者说了什么

1. **任务口径**：这是第一个"专门为'判是否相互作用'而训练并评测"的结构侧方法；此前借用别人指标做这件事缺乏严格基准——"there have been no rigorously benchmarked methods for this task"。
2. **同台比较赢**：同一份留出测试集上，"its AUC value is 0.884, compared to AUC values of 0.843 and 0.710 for iPTM and pDockQ, respectively"；作者认为差距来自分数分布形态——PPIscreenML 把多数样本推到接近 0 或 1，"PPIscreenML assigns (correct) scores very close to either 1 or 0 for most of the actives or decoys, with clear separation between them"。
3. **难考卷才是关键**：同一指标在自己的难集上明显掉分，作者用它论证基准更难也更贴近现实——"pDockQ provided an AUC value of 0.87 in its first-reported classification experiment"，"but only 0.71 when applied to this newer set"。
4. **能跨家族外推**：完全没参与开发的 TNFSF 上，Top-1 命中 14/18、Top-2 命中 17/18，AUC 0.93；作者据此主张泛化性——"Analysis of benchmark results using complexes not seen in PPIscreenML development strongly suggests that the model generalizes beyond training data"。
5. **阈值该按场景选**：作者不给单一钦定阈值，而是给阈值-精度/召回表，并写明两种使用姿态（蛋白组级粗筛用高阈值、家族内补全用低阈值）。
6. **7 个特征就够**：削减后测试集 AUC 0.884 ≈ 全 57 特征的 0.892，作者用验证集判停以避免过训："This approach provided a model with only seven features that maintained the AUC of the model with all features when evaluated using the validation set"。
7. **作者自认的天花板在 AF2 本身，不在判别器**：他们把当前扩展瓶颈归到建模失败——"the true bottleneck in extending PPIscreenML may not lie with distinguishing correct versus incorrect interfaces"，并明确"active pairings cannot be reliably identified if their structures are incorrectly built"；对 AF-PTM/v2.2 稍差的表现，归因于折错率更高："In both cases, the AUC values were slightly worse than for AF-Multimer v2.3, but analysis of incorrect predictions shows that this difference can be traced to the fact that AF-PTM and AF-Multimer v2.2 build mis-docked models of active complexes slightly more often than AF-Multimer v2.3 does"。
8. **作者对既有文献用法的批评**：大量研究把 AF2 复合物结构本身当作互作证据，"Numerous studies have incorporated AF2 models to justify or rationalize the structural basis for a particular PPI, and in many cases, use either iPTM or pDockQ as further support for the relevance of the proposed interaction"——他们要修正的正是这个习惯。
9. **同期他人工作**：作者承认 AF2Complex 也显示优于 iPTM，"the AF2Complex method also shows superiority over iPTM"，但认为其评测用的是随意集合而非精心构造的诱饵。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

以下为推断。

1. **这篇的硬通货是"难负样本的构造法"，不是模型**。定稿只有 7 个特征、框架是常规 XGBoost；真正让它区别于 pDockQ/iPTM 的是 W4 那套"结构近亲替换 + 同复合物退次近邻"的造题手法。→ 对我们：值得搬的是"造题"的纪律，而不是"模型"的复杂度。
2. **赢 iPTM 的幅度其实很小**（0.884 vs 0.843，差 0.041），而 AF2 自带的 ipTM 是一个免训练、免算 Rosetta 能量的量。公开评审也把这篇定性为 modest improvement（见第 7 节）。所以正确的引用口径是"在同一套难负样本上略优于 ipTM、显著优于 pDockQ"，不是"完胜现有方法"；而 vs pDockQ 的 0.710 之所以好看，一部分是"考卷更难"造成的（pDockQ 在自己旧题上 0.87）。
3. **"0.924 交叉折 AUC"和"0.884 留出 AUC"不可直接比较**：前者是逐模型口径（且来自验证/交叉折），后者是逐复合物取五模型最大值＋不剔错构模型。也就是说作者**换了两次考法**，数字下降里既有难度上升也有协议变化。→ 对我们：任何"内部 CV 分数 vs 外部分数"的对比必须连评测口径一起搬，否则差值不可解释。
4. **"取五个模型的最高分"本身在抬分**。一个按复合物取 max 的协议，等价于给每个复合物 5 次机会；若同一模型改为逐模型评测，AUC 必然变化，作者没给这个对照数字（本卡推算：5 次独立取最优对 AUC 的贡献无法从正文分离）。→ 对我们：漏斗里"多构象取最优"这一招要单独标定，别把它算进判据强度。
5. **1:1 构造把 precision 全部锚在了先验 0.5 上**（阈值 0 那行 precision 恰为 0.50 就是证据）。TNFSF 那一侧则相反：真值 36/504 ≈ 7% 富集度（本卡推算），更接近真实筛查，但那里作者只报 AUC 与 top-k 命中，没报 precision。→ 推断：**该工具真实部署时的 precision 会比 Table 1 低一个量级**，而原文没有把这个数算给读者。
6. **一句内部口径含混**（值得记，不影响结论但影响复现）：正文说 "Filtering on model quality in this manner excluded 932 models from training, leading to a total of 6473 active models"。本卡推算：5×1481=7405，7405−932=6473 精确成立，说明这道过滤实际作用在**全体活性复合物**上；若真只作用于 60% 的训练子集（约 889 个复合物、至多 4443 个模型），6473 这个数字装不下。因此此处的 training 更可能指"数据集"而非"训练 split"。同一篇文章里 Results 与 Methods 对交叉验证所在集合的表述互相冲突（第 2 节第 5 条），两处合起来提示：**该文的 split 叙述是给人读的，不是可机械执行的配方**，真要复现必须照 GitHub 代码。
7. **上限被 AF2 卡死这件事，作者的定性比数字重要**：他们说瓶颈是"折错"而不是"分不清对错界面"，等于承认再优化分类器的边际收益低于优化上游建模；但这是从错误样本的 DockQ 分布看图得出的（Figure 2-fig-suppl 3/4），不是干预实验。

## 7. 局限与失败（作者的 + 我们读出的 + 与旧对照底稿的差异记账）

### 7.1 作者自己写的界限

- 端到端表现混入上游失败："While the test set performance thus reflects more than the success of PPIscreenML, this strategy enhances confidence that the observed test set performance will carry forward to prospective applications in the future"——即测试集 AUC 不等于分类器能力。
- 扩展瓶颈在建模侧（第 5 节第 7 条两句）。
- 尺寸截断是算力限制而非科学选择："due to our modeling capabilities at the time"（>1550 aa 全部排除）。
- 化学计量靠假设：TNFSF "a 3:3 stoichiometry was assumed in all cases"；实体切法为迁就二聚体训练集而人为设定。
- 蛋白-肽界面不在本模型内（456 条被分出去）。

### 7.2 公开评审记下的洞（同属本底稿的 eLife public review 段，非作者正文）

- 数据集性质被质疑：负类实为非 cognate 而非"证明不结合"——"In my opinion, this set rather presents a set of non-cognate or weekly interacting protein pairs"（Reviewer 1，weekly 系原文笔误）。
- 基准偏易：真值多为稳定互作——"The benchmark set from Dockground mostly consists of stable interactions that are actually relatively easily distinguished from non-interacting pairs"；且建议补做瞬时弱互作——"I suggest the authors test how well their tools will perform on weaker and transient interactions or discuss this limitation"（Reviewer 3，均系评审原话）。
- 类别先验与现实差几个数量级——"In the benchmark set, the authors used about 1:1 ratio of positive (active) and negative controls"（Reviewer 3）。
- 提升幅度与消融缺失："The improvement is small compared with the default AlphaFold score (AUROC from 0.84 to 0.88)"；"Quite likely the most significant contributor is the ipTM (and other scores from AF2)"（Reviewer 2——即没做"去掉 AF2 置信度只留 Rosetta"这类消融，我们无法判断 7 个特征里谁在干活）。
- 对照实现版本可疑："pDockQ comparison is (likely) incorrect"（Reviewer 2，认为应比 v2.1 而非 v1.0）；未与 AF2 默认排序置信分对比。
- 可复现性："The GitHub repository does not contain the models - so the data can not be examined carefully"，且"No license is provided for the code in the Git repository"（Reviewer 2）。
- eLife 评估编辑给的定性：既肯定方法学价值也点出数据集生成的顾虑——"This study explores simple machine learning frameworks to distinguish between interacting and non-interacting protein pairs, offering solid computational results despite some concerns about dataset generation"，并把增益定为 "a modest improvement"。

### 7.3 我们读出的额外局限

- **两个 AUC 口径不可比 + 交叉验证集合表述自相矛盾**（第 2 节第 5 条、第 6 节第 3/6 条）：本文的 split/CV 叙述不构成可执行配方；本卡按 Methods 口径书写工作流，但该冲突无法在本地底稿内消解。
- **precision 一类数字全都隐含"先验 0.5"**：Table 1 阈值 0 那行 precision 恰 0.50 直接暴露了 1:1 构造；真实蛋白组尺度（引言自陈 74,000–200,000 条真互作对 vs 天文数字配对空间）下同样的阈值会给出完全不同的 precision（本文未量化）。
- **"泛化"只有两级证据**：一个留出测试集 + 一个超家族。0.93>0.884 只说明 TNFSF 在这个任务上不吃力（其真值富集度 36/504≈7%，本卡推算），不足以支撑"任何家族都行"。
- **无作者自有湿实验**：TNFSF 真值来自他人流式实验（Bossen 2006），该实验自身的假阳/假阴会直接进入 AUC 与 top-k 命中；本文没有把这部分误差传下去。

### 7.4 与对照底稿（`sources/cost-benchmarks.md` §3.9）的差异记账——一律以全文为准

| # | 旧描述（题录级，当时未取全文） | 全文核验后的更正 |
|---|---|---|
| 1 | 特征只写"AF2 置信度描述子 + Rosetta 能量项" | 实际是三组：AF2 置信度 7 ＋结构计数 33 ＋Rosetta 17；定稿 7 特征里含 **1 个结构计数特征**（界面带电残基数），旧描述漏了这一组 |
| 2 | 引"outperforms methods such as pDockQ and iPTM"（无数字） | 有数字：0.884 vs iPTM 0.843 / pDockQ 0.710；对 iPTM 的领先只有 0.041 AUC，评审与 eLife 评估均定性为 modest improvement ⇒ "优于"成立但幅度须带数 |
| 3 | "把'能不能筛互作对'从打分阈值变成监督学习问题" | 不确：监督分类器**仍要选阈值**（Table 1 整张表就是阈值-取舍），变化在于"判据由带标签数据学出来"，而非取消阈值 |
| 4 | "在 TNFSF 配体/受体选择性上正确复现" | 原文有边界：Top-1 命中 14/18、Top-2 命中 17/18、AUC 0.93 ⇒ 是"大体复现"，不是全部正确 |
| 5 | 无任何阈值/规模/成本数字（当时写"阈值数字=未记录"） | 全文给出 DockQ 0.23、TM-score 0.5、60/20/20、57→7、12 Å、1550 aa、12 recycles、5 模型、AUC 系列、7700 GPU·h ⇒ CSV 的 `阈值数字` 键可回填（见第 9 节） |
| 6 | 未区分"实验确证的互作"与"推断的非互作" | 负类是结构近亲拼出来的诱饵（标签为推断），这是本文最需要带走的限定条件 |
| 7 | CSV 的 `证据级别` 列仍是"摘要级" | 本卡为**全文级**；该列不在 14 键回填范围，未改表，留待总表负责人处理（第 0 节已记账） |

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"用置信度描述子做判别器"这件事本身**：AF2 的 pLDDT/pAE/pTM 是分链分残基的置信度场，把它按界面切片＋分位统计＋配上物理能量项，就能喂给一个浅层分类器——这套"特征工程配方"与我们手上"Foldseek/pLDDT/几何描述子 → 判定器"的路线同构，可直接借鉴的是**特征的组织方式**（置信度组 / 计数组 / 能量组三分，且禁止尺寸代理特征）。
2. **难负样本的构造法**（对我们最值钱的一条）：不要拿随机对当负例，而是用结构近亲替换组分来造"看起来该结合但其实不结合"的负例；对我们等于——评判任何 UAA 相关判据时，负样本必须挑**折叠相似、口袋相似但产物化学已知为阴性**的那一类，而不是随便挑无关蛋白。这一条能直接改进我们真值面板的对照组选取。
3. **按实体整体划分 + 按复合物取 N 模型最大值**：同一对象的多个模型绝不跨 split（防泄漏），筛查时对同一查询取最优——这两条是纯流程纪律，改我们的候选打分脚本即可落地，与判据内容无关。
4. **不钦定单一阈值，改给阈值→precision/recall 曲线**：与我们 DP2R 标准里"判据必须先在真值面板上给出操作点"的要求一致；本文 Table 1 是这一格式的现成范本（含 FPR/TPR/FNR/TNR/F1 全列，比我们只报单一分数强）。
5. **把上游预测器的失败计入端到端指标**（训练侧干净、评测侧保留错构样本）：对应我们"判据分数与 Foldseek/AF2 建模可靠性分开标定"的做法；他们用一句定性承认换来更保守的外推预期，这个姿态可抄。
6. **效率口径**：他们给总算力（7700 GPU·h）并按模型数摊单价，与我们"每通过一个闸口的候选花多少核时"的记法一致（B09 卡同条），可直接沿用格式。

**不可迁移（为什么不能照搬）**

1. **AUC 0.884 / 0.93 与 Table 1 的阈值不是 UAA 判据**。PPIscreenML 回答的是"这一对会不会按这个界面结合"，其真值是 PDB 共结晶的静态界面；UAA 合成酶要回答的是"能不能催化 S0/S1/S2 三步化学事件并避开竞争副产物"。**结合判别既不必要也不充分**。DP2R 标准 §2 明确禁止把别人的 pAE/ipTM/分类器阈值当酶活闸口，本篇的 AUC 与阈值数字同样在被禁之列——它们只能作为"别人怎么做判别器"的参照，不能作为我们的门槛或先验。
2. **不能拿它的性能数字推断我们的成功概率**。它的正负标签齐全（1481＋1481，全部有结构），我们没有一条被产物化学确证的天然 UAA 合成酶作为正样本 ⇒ **同类监督分类器我们根本训不出来**（没有 y）。"PPIscreenML 在 X 上 0.884"不能变成"我们对 UAA 也有 XX% 把握"。
3. **TNFSF 案例的外推教训是反的**：它证明的是"在同一家族内部区分 cognate / 非 cognate 界面"可行，而该家族的配体与受体结构高度保守、且真值来自他人流式实验；这与"从一个未表征家族里发现新催化功能"不是一个问题。引用它只许引**评测设计**，不许引**命中数字**做校准。
4. **本文无 MD、无 QM、无表达与产物化学**，因此它既不能为"用 MD/QM 判催化"提供命中率背书，也不能被用来主张"结构置信度足以替代功能实验"。
5. **12 Å 界面切片与 3:3 实体映射是二聚/寡聚界面的定义**，对"底物结合口袋＋催化残基空间关系"这种酶问题没有对应物；照搬会把口袋当成界面。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K40_PMC13099138_text.txt

- **本卡全部英文引句只照这一份底稿逐字抄写**（SHA-256 `e5c2a1d670153f1a6f356c023c80456a9b91210214f1d818a0704255567d3935`，69,243 B，单行去标签纯文本）。同目录另有 `K40_PMC13099138_fullTextXML.xml`（源 XML，门禁按规则不参与逐字比对）。写卡前已核对底稿开头 600 字符含 `10.7554/eLife.98179`＋`PMC13099138`＋`42012336` 与四位作者，确认与本行编号一致。
- 该底稿同时包含 eLife 的公开评审段（Reviewer 1/2/3 与编辑评估）。**第 7.2 节的引句出自评审段，不是作者正文**，本卡在行文处已逐条标明说话人，不得当作作者主张引用。
- 对照底稿：`sources/cost-benchmarks.md` §3.9（第 147 行题录级旧描述）与第 201 行（Type II 对照表里提到 PPIscreenML 型监督分类）；差异记账见第 7.4 节。
- CSV 字段映射：第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。CSV 的 `证据级别` 列旧值"摘要级"未改（不在 14 键内，见第 0 节）。
- 未取到：补充图原图（含 Figure 1-fig-suppl 4 的尺寸直方图、Figure 2-fig-suppl 1 的七框架 ROC 组、fig-suppl 3/4 的跨版本 DockQ 分布）、逐复合物打分表、GitHub 里的模型权重（评审称仓库不含模型）。凡涉及这些处本卡只写正文描述，不补数字。
- **非原文数字的自证**：第 4 节 7405、0.44–0.52 GPU·h 与第 6 节的 36/504≈7%、889/4443 均为本卡算术推算，行内已标"本卡推算/本报告推算"，不作为文献数字引用。
- 门禁：`python scripts/verify_literature_cards.py --only K40 --no-report`（输入=本卡 + 上述登记底稿；只判完整性与逐字命中，不判内容对错）。

<!--CSV回填
work_type=方法（论文；eLife 2026 Tools and Resources；预印本 10.1101/2024.03.16.585347 同名）
target=蛋白-蛋白互作对的二分类判别：1481 个非冗余异源二聚复合物（正类）＋1481 个结构近亲诱饵（负类）；外推 benchmark 为 TNFSF 18 配体×28 受体=504 对（36 对已知结合）
backbone_generation=不生成新设计骨架；对既有 PDB 组分序列做复合物结构预测——ColabFold Batch 的 AF-Multimer v2（建集）与 v2.3（正文与 benchmark），模板开、12 次 recycle、AMBER relax、每对象 5 个模型；TNFSF 按 3:3 计量（3 拷贝配体＋1 拷贝受体）
computational_filters=57 个特征分三组（AF2 置信度 7＋结构计数 33＋Rosetta 能量 17）→ 七种常规 ML 框架横评选 XGBoost → 序列后向选择降到 7 特征（1 个 AF2 置信度、1 个界面带电残基计数、5 个 Rosetta 能量项）；同台对照判据 iPTM、pDockQ（PIscore 由 AlphaPulldown 提供）；禁用随总残基数缩放的尺寸代理特征
thresholds=训练侧 DockQ≥0.23 才保留；诱饵近邻 TM-score>0.5（87% 覆盖）；60/20/20 划分且同复合物 5 模型整体归一份；界面残基=Cβ（Gly 用 Cα）跨链 12 Å 内；总长>1550 aa 剔除、任一链<50 aa 移入蛋白-肽；分辨率≤3 Å、序列同一性≤30%；留出 AUC 0.884（57 特征 0.892、交叉折 0.924）vs iPTM 0.843 / pDockQ 0.710；TNFSF AUC 0.93；分类阈值可调（0.98→precision 1.00/recall 0.00；0.75→0.82/0.80；0.05→0.67/0.97）
md_used=否（全文无分子动力学；Rosetta 项是对单一 AF2 模型的静态能量打分）
qm_used=否（全文无量子化学计算）
experimental_methods=作者无自有湿实验；正类标签来自 PDB 实验结构（DockGround 下载），负类为构造诱饵；TNFSF 真值取 Bossen 2006 已发表的综合流式细胞选择性表；仅用计算 benchmark 与已知选择性对照
pipeline_counts=DockGround 异源二聚复合物 → 五道过滤得 1481 蛋白-蛋白（另有 456 蛋白-肽被分走）→ 每复合物 5 个 AF2 模型＋1481 个诱饵各 5 模型 → DockQ≥0.23 剔 932 个活性模型、留 6473（DockQ 中位 0.88）→ 57 特征 → 7 特征 → 留出测试集 + TNFSF 504 对配对打分
hit_rate=二分类留出 AUC 0.884（交叉折口径 0.924，两者不可直接比）；TNFSF Top-1 命中真互作 14/18 配体、Top-2 命中 17/18、AUC 0.93；无实验命中率（本文不做表达与结合测定）
best_metric=未记录（本文只判结合/不结合，不报亲和力 Kd、不报活性或转化数，无可引用的最好功能数值）
cost_or_stat_note=约 7700 GPU·小时建成全部 AF2 模型（Expanse 集群 NVIDIA V100）；建模配置 5 模型/对象、12 recycles、模板、AMBER relax；本卡推算单价 0.44–0.52 GPU·h/模型（原文未拆分）；7 特征即达 0.884，说明判别不依赖复杂模型
role_in_timeline=把"能不能筛互作对"从挪用模型质量指标＋固定阈值（iPTM、pDockQ 的次生用途）升级为带难负样本标签的监督学习判别器，并交付阈值→precision/recall 使用表；同时把自己的天花板归回上游 AF2 建模可靠性，是 B09 那条"界面判据"路线上专门做 PPI 筛查的姊妹工作
source_pointer=data/literature_cards/fulltext/K40_PMC13099138_text.txt（SHA-256 e5c2a1d670153f1a…，已核验 DOI 10.7554/eLife.98179 与 PMC13099138）；旧题录对照 sources/cost-benchmarks.md §3.9 第 147 行
CSV回填-->
