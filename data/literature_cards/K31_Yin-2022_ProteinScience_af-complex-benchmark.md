# [K31] 用 CAPRI 基准考 AlphaFold 复合物预测——「界面位对没位对」的判据与失效边界

Yin R, Feng BY, Varshney A, Pierce BG（马里兰大学 IBBR / 计算机系）
Protein Science 2022, 31(8):e4379 · DOI 10.1002/pro.4379 · PMID 35900023 · PMCID PMC9278006
开放获取（CC BY 4.0）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K31**（组：通用方法学; 口径对照；`文献类型=benchmark`；`证据级别=全文级`） |
| 本文取回方式 | Europe PMC 先按 DOI 检索再取 `fullTextXML`（inventory 记录 `fetch_channel=epmc_search_then_fulltext`） |
| 本地全文 | `data/literature_cards/fulltext/K31_PMC9278006_text.txt`（80,755 B，标签剥离+实体解码后的单行纯文本）；同源 XML `K31_PMC9278006_fullTextXML.xml` |
| 身份体检 | 文件头书目块 = "Benchmarking AlphaFold for protein complex modeling reveals accuracy determinants" / Yin Rui, Feng Brandon Y, Varshney Amitabh, Pierce Brian G / 10.1002/pro.4379 / PMC9278006 / 35900023，与 CSV 的 DOI 一致 ⇒ **未挂错行** |
| 登记行本身的错（本卡不改 CSV，只留记录） | CSV `第一或通讯作者` 写成 `Yin R, Feng X, Varshney D, Pierce BGT`，与全文作者缩写（Feng BY / Varshney A / Pierce BG）不符；CSV `标题` 里带 JATS 内联标签 `<scp>AlphaFold</scp>`，而本地 `.txt` 已把标签剥掉，所以本卡引句按 `.txt` 里的实际字符取（标题在 txt 里是纯文本 `Benchmarking AlphaFold ...`） |
| 证据级别 | **全文级**（本卡全部引句可在该本地纯文本里逐字命中，见第 9 节自检） |
| 未取到的部分 | 补充信息 Appendix S1（Table S1–S8、Figure S1–S8 的逐案例明细）与图内原始数值。凡涉及这些的地方本卡明写「仅正文汇总值，逐案例表未取」。Table 1（AUC 主表）被抽取进正文文本，可搜到 |

## 1. 这篇到底解决什么（一句话+大白话）

一句话：**它不是设计方法，而是一份「考卷」**——把 AlphaFold（及其 ColabFold / AlphaFold-Multimer 变体）当成复合物结构预测器，在一批已知晶体结构的天然蛋白-蛋白复合物上按 CAPRI 标准打分，回答两个问题：（a）端到端深度学习预测复合物到底几成把握、跟传统刚体对接比怎么样；（b）**在什么条件下这套把握会失灵**。

大白话：作者拿 152 个天然异源二聚体做基准，AlphaFold 有 149 个跑出来了，其中约一半能给出 acceptable 及以上准确率的模型、43% 能给出 near-native（medium 及以上）的排名第一模型，比用未结合态结构做刚性对接的 ZDOCK（9%）高一大截。但同一套流程**在抗体-抗原上全军覆没**（BM5.5 里的 11 例 0 成功），扩充到 100 例新发布抗体复合物也只有 6%（排名第一）/11%（五个模型内），TCR-pMHC 14 例只成 2 例。作者据此把失灵归因到「界面缺少共进化信号」，并顺带给出哪些内部打分（pTM、界面 pLDDT/PAE、ipTM）能用、能用到什么程度。

对我们的价值不在「AF 很准」，而在**它给出的准/不准的边界条件与分母口径**（见第 7、8 节）。

## 2. 难点与应对（作者自述，不是我们的推测）

1. **训练集泄漏（基准可能已被 AlphaFold 见过）** → 现象/原句：作者反复承认这是无法排除的偏置，"it is possible that individual chain structures from BM5.5 complex structures were part of the AlphaFold training set, which could influence the predicted conformations of the subunits and indirectly influence the complex structure models"；对唯一的正例示范（2X9A）也只能写"it is possible that one or both of the component proteins were part of the AlphaFold training set, however the protein-protein interface and binding orientation were not"（后半句是推测，不是验证）。 → **他们做了什么**：(i) 主实验直接把模板关掉——"the use of structural templates was disabled in this study"，理由是避免「用已知单体构象隐式偏置预测」；(ii) Multimer/抗体扩充集只取 2018 年 5 月之后发布的结构，"the test set included only antibody-antigen complexes from May 2018"；(iii) 开模板时卡日期，"a template release date cutoff of April 30, 2018 was applied when the use of templates was enabled"；(iv) 用 ZDOCK（输入未结合态结构）做同期对照。 → **代价**：BM5.5 主表（43%/51%）的泄漏问题**没有被关闭，只被承认**；只有追加集合是时间隔离的。作者还自曝一个不利于对照组的判断：对接方法用未结合态结构，AlphaFold 可能「免费」知道结合态构象。

2. **「成功」取决于选 CAPRI 哪一档，档位之间差 8–30 个百分点** → 现象/原句：评级口径是"Models were assessed as acceptable, medium, or high accuracy, or incorrect, based on using CAPRI criteria"，而作者明说 acceptable 这一档很松："While acceptable accuracy models can include moderate deviation from known structures"（同一句紧接着给出括注 including models with up to 10 Å L‐RMSD，并注明 medium/high 才更接近以往文献的 near-native 定义，正文另用 2.5 Å I-RMSD 作为 near-native 的参照 cutoff）。 → **他们做了什么**：三档数字分开报、不合并成「一个成功率」（"AlphaFold was able to generate models with acceptable or higher accuracy for approximately half (51%) of the 149 test cases for which models were generated"；同句再给 medium 43%、high 21%），并把 medium/high 统一称为 near-native 用于后续分组分析。 → **代价**：跨论文引用时极容易被「只取 51%」或「只取 43%」，本文与同行工作（Bryant 等，另一 216 例集合）比对时也是这么做的："they reported a 63% success rate for acceptable or higher model quality, which is similar to our observed 51% success for models of that quality from AlphaFold"。

3. **抗体-抗原整类失灵，但原因不明** → 现象/原句："Notably, the antibody-antigen complexes had no successfully generated models, while other complex categories considered all showed approximately commensurate levels of AlphaFold performance"；正文另处（2.5 节）把它称作"Due to the lack of any successful structural prediction of 11 antibody-antigen complexes from the BM5.5 set"。抽象层的定性是"however AlphaFold modeling of antibody-antigen complexes within our set was unsuccessful"。 → **他们做了什么**（这是一连串**排除法实验**，本文最有方法学价值的部分）：(i) 追加 20 例非冗余抗体-抗原复合物（"we assembled a set of 20 additional nonredundant antibody-antigen complexes with known structures to assess AlphaFold accuracy"）→ 仍几乎全错，只有两例侥幸（"While AlphaFold modeling of most of those complex structures resulted in no accurate predictions, surprisingly two of the antibody-antigen complexes were modeled accurately, with medium CAPRI accuracy models ranked #1 for each complex"）；(ii) 观察失败模型形态，"many of the inaccurate models had few or no contacts between antibody and antigen chains"（两链压根没碰上）；(iii) 换受体架构排除「免疫球蛋白折叠本身有问题」——用 7 例 VLR/repebody（无 Ig 结构域）测，"Only one out of the seven VLR and repebody complexes tested had any correct models from AlphaFold"，据此得"indicating that the immunoglobulin architecture was not responsible for the observed limited AlphaFold success for antibody-antigen complexes"；(iv) 用 AlphaFold-Multimer 在同一批上带/不带 MSA 对照（Table 2），发现去掉 MSA 对抗体案例影响小、对非抗体案例影响大，"it appears to have less of impact on antibody-antigen complex structure prediction"；(v) 扩到 100 例定量： "Success rates for this set were found to be low, with 6% of cases with medium or high accuracy models ranked #1, and 11% of cases with medium or high accuracy models in one or more of the five models generated per case"。 → **应对后仍留下的代价**：失灵被**归因**为共进化信号缺失，但作者没有（也无法在此文里）给出修法；且 20 例里有 2 例成功、说明是「低概率」而非「不可能」，本文未解决「什么时候能成」的预测规则。

4. **内部打分在准确率类别之间高度重叠，单一分数当不了门槛** → 现象/原句：pTM/pLDDT 有信号但类别间重叠（Figure 5a 描述），于是"the overlap in scores between accuracy categories (Figure 5a ) led us to explore additional scoring functions to predict the structural quality of AlphaFold models"。 → **他们做了什么**：把打分改成**只看界面残基**——interface PAE 与 interface pLDDT，并与传统对接打分 IRAD、ZRANK2、Rosetta 跨界面结合能一起用 ROC/AUC 横比："AUCs of 0.93 and 0.97 for interface PAE and interface pLDDT, respectively"；界面定义也做了宽松度敏感性检验（4 Å 起，测到 10 Å，"no major difference in model assessment accuracy was observed"）；对没有界面接触的模型给了哨兵值（"An interface pLDDT score of 0 and an interface PAE score of 35 was assigned to models without any interface contacts within the distance cutoff"）；Multimer 那批另外测 ipTM："ipTM alone showed promising model discrimination accuracy, with an ipTM score threshold of approximately 0.75 corresponding to a possible model confidence cutoff"。 → **代价（关键）**：所有阈值是**在同一批评测数据上取切点**得到的，没有独立留出集："Based on discrimination of incorrect versus medium and high accuracy models and maximization of sensitivity and sensitivity, possible score cutoffs for model selection are pTM = 0.8"（原文此处即写作 sensitivity and sensitivity，为逐字复制；方法节另说明用 cutpointr 包按 sensitivity+specificity 之和最大化取切点）；且 Table 1 里二分类 AUC 好看（0.93/0.97），**多分类 AUC 明显掉下来**（interface pLDDT 多分类 0.84、pTM 0.80），意味着「三档/四档一起判」时判据弱得多。

5. **想靠配对 MSA（共进化信号）救复合物，结果没救成** → 现象/原句："the addition of paired sequences did not appear to improve AlphaFold performance over use of unpaired MSAs as input, while use of paired sequences alone was detrimental to successful complex modeling in some cases"。 → **他们做了什么**：只在能满足配对前提的 17 例（同原核物种的两条链）上测，MSA 来自 ColabFold（2021-09-04 取），并把同一批配对 MSA 喂给 RoseTTAFold 做交叉验证（"we observed lower overall success for the models generated with that method"）；顺带把「MSA 深度不够」这个候选解释也做了统计检验并否掉——"Limited MSA depth for either or both partner proteins was explored as a possible factor in poor predictive performance, but it was not found to have a significant impact"。 → **代价**：唯一例外 1F6M 属个案；「深度不够 vs 配对缺失」这两个机制在这批数据上分不开，作者改用「去掉 MSA 输入」的反向对照（见第 3 条）才做出归因。

6. **工程性失败被从分母里拿掉** → 现象/原句："AlphaFold failed to generate predictions for three complexes, thus AlphaFold predictions were obtained for 149 complexes"，方法节交代得很具体："Three out of the 152 test cases failed to complete in the AlphaFold pipeline due to GPU memory limits during structure prediction, or errors during feature preparation: 1ZM4, 2OZA, and 1B6C"。 → **他们做了什么**：明确声明成功率用 149 作分母（Fig 1 图注），并保留 152 作为样本集合大小。 → **代价**：正文另一处样本描述（方法 4.1）写"By filtering for heterodimeric protein-protein complexes in BM5.5, we obtained a total of 152 cases"并给出 12 例抗体-抗原 / 72 例含酶 / 68 例其他，结果部分却说 11 例抗体-抗原（见第 3 条引句），差异未解释；讨论里刚体占比也写成 64%（"most complexes in our BM 5.5 set are classified as rigid"，同一句给 64%），而 95/152 = 62.5%、95/149 = 63.8%——**同一篇文章里分母口径在 152/149 之间来回换**。这类「分母漂移」是本卡最需要留防的地方。

7. **「折叠错」还是「对接错」分不清** → 现象/原句：他们先确认单体链基本折对（"in most cases the individual ligand and receptor chains were modeled accurately"，同一句给出判据为骨架 RMSD 相对结合态单体链 <2.5 Å），再看界面 RMSD 与最大亚基 RMSD 无关联，得"indicating that incorrect binding mode, versus inaccurate chain folding, was the primary cause of incorrect AlphaFold complex models"。 → **他们做了什么**：把失败原因从「折不动」改判为「位不对」，从而把判据重心移到界面级指标（见第 4 条）。 → 代价：这条只对 BM5.5 这种两条链各自都折得好的天然复合物成立，不能推广。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **被考生**：AlphaFold（本地安装，GitHub 版，DB 版本 UniRef90 2020_01 / MGnify 2018_12 / Uniclust30 2018_08 / BFD；unpaired MSA；禁用模板；链 junction 残基编号 +200；每例出 5 个模型；按 pTM 排序）；ColabFold `advanced` 界面（MMseqs2 出 MSA，关掉 Amber relaxation）；RoseTTAFold（Robetta 服务器，只用于配对 MSA 对照）；AlphaFold-Multimer（2021-11-02 下载版，可切 paired/unpaired/no MSA 四种输入模式）。
- **对照组考生**：ZDOCK 3.0.2 刚体对接，输入 BM5.5 未结合态结构（HETATM 删除），稠密角采样，IRAD 排序。
- **评分尺**：CAPRI 四级（I-RMSD、L-RMSD、f_nat；用骨架原子），自写脚本判级。
- **模型质量判别量**：pTM、平均 pLDDT、平均 resolved pLDDT、interface PAE（4 Å）、interface pLDDT（4 Å）、IRAD、ZRANK2、Rosetta 跨界面结合能、界面面积、界面氢键数、界面残基数、shape complementarity；Multimer 加 ipTM。
- **建模前后处理**：把 AlphaFold 默认的 Amber relaxation 换成 Rosetta constrained FastRelax（`-relax:constrain_relax_to_start_coords -relax:coord_constrain_sidechains -relax:ramp_constraints false -ex1 -ex2 -use_input_sc -no_optH false -flip_HNQ -nstruct 1`），弛豫后的结构才送去算 IRAD/ZRANK2/Rosetta 分数。
- **统计**：Wilcoxon rank-sum（incorrect vs medium、incorrect vs high 分组比特征）；Pearson 相关；pROC/multiROC 算 AUC，2000 次分层 bootstrap 出 95% CI；cutpointr 取切点。
- **没有用的方法**：MD、QM、自由能微扰、任何湿实验表达/结合测定——本文全部对照物都是**已发表的晶体/冷冻电镜结构**，不做新实验。

### 主流程（表格）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 | BM5.5（对接基准库） | 过滤出异源二聚体，取 PDB `seqres` 序列；难度分级与 BSA 直接从 BM5.5 站点取 | 非冗余 + BM5.5 原有分类；样本口径见原句"BM5.5 is a set of structures of nonredundant transient protein-protein complexes from the PDB" | 152 例（12 抗体-抗原 / 72 含酶 / 68 其他）；难度 Rigid 95、Medium 34、Difficult 23 |
| 2 | 152 例的两条链序列 | AlphaFold 本地跑复合物预测：unpaired MSA、**禁模板**、编号 +200 造链断、每例 5 模型 | 无精度阈值（固定 5 模型/例）；原文未给「该丢弃哪档」的阈值 | "AlphaFold failed to generate predictions for three complexes, thus AlphaFold predictions were obtained for 149 complexes"；745 个模型（149×5） |
| 3 | 同一批序列 | ColabFold `advanced`（MMseqs2）并行跑；与 AlphaFold 比逐案例一致性 | 用二者成功率是否"commensurate"判断能否拿 ColabFold 代替 AlphaFold（后续大批量就靠它） | 结论：两者高度相关、成功率高≈同；用于 100 例抗体集的算力可行性 |
| 4 | BM5.5 未结合态结构 | ZDOCK 3.0.2 刚体对接 + IRAD 排序，作为传统方法基线 | 稠密采样"generating 54,000 predictions per complex"；主表取 T1/T5，分组图放宽到 top 25 | T1：acceptable+ 13%、medium+ 9%、high 1%（与 149 例同分母） |
| 5 | 所有模型 | 按 CAPRI 判级 | 四档 acceptable/medium/high/incorrect，用 I-RMSD、L-RMSD、f_nat（骨架原子）；acceptable 档可含 10 Å 量级的 L-RMSD 偏差（正文括注）；正文另引 2.5 Å I-RMSD 作 near-native 参照 | 每例每档标签，成功率 = 有该档模型的案例占比（**分母是案例不是模型**） |
| 6 | 判级结果 | 分组找失灵条件：按对接难度 / 复合物类别 / 物种来源 | 三档分别统计（不合并） | 难度分档 47/55/78%（acceptable+，T5）、39/48/57%（medium+）、27/16/17%（high）；**抗体-抗原类 0 成功** |
| 7 | 判级结果 + 结构/序列特征 | 算 BSA、N_eff、总残基数、界面残基占比，做分布比较 | Wilcoxon rank-sum；BSA 在 incorrect vs medium/high 上 p = .007；N_eff 定义"clustered at the 62% sequence identity"（CD-HIT，词长 4）；显著性标记 ns p > .05、* p ≤ .05、** p ≤ .01、*** p ≤ .001 | 结论：大蛋白+相对小界面最关联失败；MSA 深度不显著 |
| 8 | 149 例 × 5 模型 | 打分器横比：pTM/pLDDT/界面 PAE/界面 pLDDT/IRAD/ZRANK2/Rosetta 能量 | AUC（二分类与多分类）；界面定义 4 Å 起测到 10 Å；无接触模型给哨兵值 | interface PAE 0.93、interface pLDDT 0.97（incorrect 对 high 的二分类）；多分类 AUC 仅 0.77–0.84 |
| 9 | 打分分布 | 取「可用切点」 | 用 cutpointr 按 sensitivity+specificity 之和最大化，**在同一批 149 例上取切点、无留出集** | `pTM = 0.8`；`interface pLDDT = 84`；`IRAD = -128`；`Rosetta cross-interface binding energy = -16` |
| 10 | 失灵归因 | 配对 MSA 对照（17 例同原核物种）、RoseTTAFold 交叉验证、VLR/repebody 换架构、with/without MSA 对照 | "1 out of 17 cases, or 6% success"（无 MSA 的非抗体组）；"success (13/17 cases, or 76%, with a medium/high accuracy model ranked #1) versus antibody-antigen case success (2/7 cases, or 29%, with a medium/high accuracy model ranked #1)"（有 MSA） | 归因于界面无共进化信号，而非架构或尺寸 |
| 11 | 追加抗体集 | 从 SAbDab 选 20 例非冗余抗体-抗原（17 heavy-light + 3 nanobody）跑 AlphaFold | 分辨率 cutoff < 3.25 Å；与 BM5.5 去冗余（可变域 < 90% identity；抗原 blastp 默认参数无 hit） | 2/20 达 medium 且排 #1，其余无正确预测 |
| 12 | 100 例新抗体集 + AlphaFold-Multimer | 在 ColabFold 跑 Multimer（开模板但卡 2018-04-30 之前的模板） | 只取 2018-05 之后发布；抗原 BLAST 去冗余（E-value 5、≥ 40% identity）；heavy/light 可变域与 CDR 冗余阈值另加 | 73 heavy-light + 27 nanobody；**T1 6% / T5 11%**（摘要只报 11% 这一档） |
| 13 | TCR-pMHC 集合 | 从 TCR3d 取 Class I TCR-pMHC，四条链（TCR α/β、肽、MHC α1α2）分别输入 Multimer | 2018-04 之后发布；可变域 < 90%（且对单条 α/β < 95%）identity 去冗余；排除含非典型/修饰氨基酸肽；分辨率 3.25 Å，唯一破例 7RM4（3.33 Å） | 14 例，"showed a success rate of 2 out of 14 complexes (14%)" |

**这套流程的骨架值得单独记住**：固定样本（非冗余天然复合物）→ 固定评级尺（CAPRI）→ 换「考生」（AF/ColabFold/Multimer/ZDOCK/RoseTTAFold）→ 换「输入条件」（有无 MSA、有无配对、有无模板）→ 换「评分尺」（pTM → 界面级 → 能量）→ 最后**用失灵类别反证机制**。第 12–13 步的「只取训练截止日期之后的结构」是我们做口径对照时唯一能直接抄的设计动作。

## 4. 关键数字台账（数值 · 含义 · 出处）

| 数值 | 含义 | 出处 |
|---|---|---|
| 152 例 | 基准样本总数（BM5.5 过滤出的异源二聚体） | 方法 4.1 原句 + 结果 2.1；组成为 12 抗体-抗原 / 72 含酶 / 68 其他 |
| 11 例（结果）vs 12 例（方法） | 同一批抗体-抗原案例的两个不同计数，差异未解释 | 结果 2.5 引句（11）/方法 4.1 原句（12） |
| 95 / 34 / 23 | Rigid / Medium / Difficult 对接难度案例数 | "the cases had unbound docking difficulty classifications of Rigid (95 cases), Medium difficulty (34 cases) and Difficult (23 cases)" |
| 149 例；3 例失败 | 实际参与成功率计算的分母；失败原因 | "AlphaFold failed to generate predictions for three complexes, thus AlphaFold predictions were obtained for 149 complexes" + 方法 4.2 点名 1ZM4、2OZA、1B6C（GPU 内存/特征准备报错） |
| 51% / 43% / 21% | T1 模型达 acceptable+ / medium+ / high 的案例占比 | "AlphaFold was able to generate models with acceptable or higher accuracy for approximately half (51%) of the 149 test cases for which models were generated"（同句给 43%、21%） |
| 54% / 44% / 23% | 放宽到每例 5 个模型（T5）的同一三档占比 | "and only a modest improvement in success was observed when allowing five predicted models per case (T5) (54%, 44%, and 23% success rates for acceptable accuracy or better, medium accuracy or better, or high accuracy, respectively)" |
| 13% / 9% / 1% | ZDOCK+IRAD 的 T1 三档占比（传统对接基线） | 结果 2.1（摘要口径只取其中 medium+ 那一档，写作"greatly surpassing the performance of unbound protein-protein docking"） |
| 54,000 / complex | ZDOCK 稠密角采样产生的姿态数 | "Dense rotational sampling was used, generating 54,000 predictions per complex" |
| 47% / 55% / 78% | AlphaFold T5 在 rigid/medium/difficult 三档难度上的 acceptable+ 成功率（**难案例反而最高**） | "success rates for AlphaFold were found to be 47%, 55%, and 78% for rigid, medium, and difficult docking difficulty categories, respectively" |
| 39% / 48% / 57%；27% / 16% / 17% | 同三档难度的 medium+ 与 high 成功率（严档下难度优势消失/反转） | 结果 2.2 |
| ~25% | 高准确率成功率对「同物种 vs 跨物种」「真核 vs 细菌」几乎不变 | 结果 2.2 |
| 64% | 讨论里给的 BM5.5 刚体占比（与 95/152 = 62.5% 略有出入） | "most complexes in our BM 5.5 set are classified as rigid" + "(64%)" |
| p = .007 | BSA（界面积）与 AlphaFold 成功的关联（incorrect vs medium/high，Wilcoxon） | 结果 2.2 / Table S2（逐案例表未取） |
| 62% identity + 词长 4 | N_eff（MSA 深度）定义：CD-HIT 聚类后的簇数 | "score is defined as the number of clusters after the raw MSA inputs were clustered at the 62% sequence identity" |
| < 2.5 Å | 多数案例单条链本体建模准确的判据（骨架 RMSD，原文写作 backbone RMSD with bound component chains <2.5 Å） | "in most cases the individual ligand and receptor chains were modeled accurately" |
| r = .82；r = -.55 | pTM 与真实 TM-score、pTM 与 I-RMSD 的相关（p < .001） | 结果 2.4 |
| AUC 0.93 / 0.97 | interface PAE / interface pLDDT 在 incorrect 对 high 的二分类上的判别力 | "AUCs of 0.93 and 0.97 for interface PAE and interface pLDDT, respectively" |
| Table 1 多分类 AUC：interface pLDDT 0.84、interface PAE 0.81、pTM 0.80、cross-interface binding energy 0.84 | 同一批分数在四档同时判时的能力（明显低于二分类读数） | Table 1（正文文本内，可逐值搜到） |
| Table 1 二分类 AUC：Rosetta 跨界面结合能 0.99（0.99-1.00）、IRAD 0.96、ZRANK 0.95、平均 pLDDT 0.66 | 能量类/简单几何类打分并不输给 AF 自带分数 | Table 1 |
| pTM = 0.8；interface pLDDT = 84；IRAD = -128；Rosetta 跨界面结合能 = -16 | 作者给的「可选模型筛选切点」，由 sensitivity+specificity 之和最大化算出 | "Based on discrimination of incorrect versus medium and high accuracy models and maximization of sensitivity and sensitivity, possible score cutoffs for model selection are pTM = 0.8" |
| ipTM ≈ 0.75 | Multimer 案例（Table 2 那批）上 ipTM 单独用的置信切点 | "ipTM alone showed promising model discrimination accuracy, with an ipTM score threshold of approximately 0.75 corresponding to a possible model confidence cutoff" |
| 4 Å → 10 Å | 界面残基定义的接触 cutoff 敏感性检验范围；放宽后结论基本不变 | 方法 4.7 + 结果 2.4 |
| 界面 pLDDT = 0 / 界面 PAE = 35 | 无界面接触模型的哨兵值赋值（会直接把「链没碰上」记成「高分/低分」） | "An interface pLDDT score of 0 and an interface PAE score of 35 was assigned to models without any interface contacts within the distance cutoff" |
| 0/11 | BM5.5 抗体-抗原案例的正确预测数（本类全灭） | 结果 2.5 引句 |
| 2/20 | 追加非冗余抗体集上 medium 且排 #1 的案例数 | "While AlphaFold modeling of most of those complex structures resulted in no accurate predictions, surprisingly two of the antibody-antigen complexes were modeled accurately, with medium CAPRI accuracy models ranked #1 for each complex" |
| 1/7 | VLR/repebody（非免疫球蛋白受体）案例有正确模型的数量 | "Only one out of the seven VLR and repebody complexes tested had any correct models from AlphaFold" |
| 13/17 = 76%（非抗体）vs 2/7 = 29%（抗体）；1/17 = 6%（非抗体、无 MSA） | Multimer 带/不带 MSA 的分类命中（T1 medium+） | "success (13/17 cases, or 76%, with a medium/high accuracy model ranked #1) versus antibody-antigen case success (2/7 cases, or 29%, with a medium/high accuracy model ranked #1)" + "1 out of 17 cases, or 6% success" |
| 100 例（73 heavy-light + 27 nanobody）；6%（T1）/ 11%（T5） | 最大抗体-抗原扩展集的结果；**摘要只报 11%（对应 T5 口径），正文 T1 是 6%** | "Success rates for this set were found to be low, with 6% of cases with medium or high accuracy models ranked #1, and 11% of cases with medium or high accuracy models in one or more of the five models generated per case" 与摘要"confirmed a low rate of success for antibody-antigen complexes (11% success)" |
| 14 例 → 2/14 = 14% | Class I TCR-pMHC 集合（Multimer，T1 或 T5 内命中 medium/high） | "showed a success rate of 2 out of 14 complexes (14%)" |
| < 3.25 Å | 追加案例的晶体结构分辨率门槛（7RM4 以 3.33 Å 破例保留） | 方法 4.1 |
| 63%（Bryant 等，216 例）vs 本文 51% | 同口径（acceptable+）不同样本集的可比性 | "While the authors used a distinct test set of 216 protein complexes from the Dockground protein docking benchmark" + "they reported a 63% success rate for acceptable or higher model quality, which is similar to our observed 51% success for models of that quality from AlphaFold" |
| 5 模型/例；2000 bootstrap | 每例产出与 CI 计算量 | 方法 4.2 / 4.12 |

## 5. 结论——作者说了什么

1. AlphaFold 端到端预测瞬态复合物**总体是成功的**："AlphaFold is largely successful at predicting binary transient protein complex structures"，且大幅超过用未结合态结构的刚体对接（43% vs 9%，medium+ 的 T1 口径）。
2. **失灵是有类别的**："some complexes were not successfully modeled, most notably antibody-antigen and other adaptive immune interactions, while other categories of test cases showed upper limits of success as well"；抗体失灵与 TCR 失灵被合写为"showing that adaptive immune recognition poses a challenge for the current AlphaFold algorithm and model"。
3. **失灵的机制归因是共进化信号缺失**，不是接口几何或免疫球蛋白架构（由 VLR 与 with/without MSA 两组排除法支持）。
4. **判据该看界面而不是看全局**：界面残基级 pLDDT/PAE 明显优于平均 pLDDT 与 pTM；Rosetta 跨界面结合能与 IRAD/ZRANK2 同级甚至更强（95% CI 重叠，作者写"their performance is essentially equivalent"）；Multimer 场景 ipTM 单独用也行得通（≈0.75）。
5. 失败的主要形态是**结合姿态错而非单体折叠错**，且不少抗体失败模型干脆两链没接触。
6. 作者自认的边界：BM5.5 训练泄漏无法完全排除；配对 MSA 没帮上忙；本文只"highlights areas of improvement for future developments"，不交付修复。

## 6. 结论——我们读出了什么

以下为推断。

1. **这篇给的是「上限读数」而不是「命中率读数」**。它的样本是 PDB 里已被解析、彼此共进化、序列在数据库里能被大量同源命中配对的天然复合物；AlphaFold 在这里 43%/51% 的把握，是**在问题最友好的分布上**取的。第 12–13 步（无 MSA 时非抗体案例从 76% 掉到 6%）其实自己给了证据：**当界面共进化信号被抽掉，这套流程的近-native 命中就跌到个位数**。
2. **由此可推（但不能当数字引用）**：我们从零设计的「酶-非天然底物」复合物，界面上既没有共进化、序列也不在 DB 里，其情形更接近「no MSA 档」而不是「有 MSA 的 76% 档」。这是本文对我们**最有用的一条定性警示**，但它是外推类比，不是本文结论。
3. **它把「判据失灵」做成了可迁移的模板**：失灵类别（抗体）→ 换架构排除（VLR）→ 换输入信号排除（MSA on/off）→ 扩样本定量（100 例）→ 给出失败形态（无原子接触）。这套「四步归因」比任何阈值都值钱，我们的漏斗判据遇到「整体分数好看但某类候选系统性错」时应当照此做。
4. **「界面级 > 全局级」这一条可以搬**（interface pLDDT/PAE、ipTM、能量项都是界面切片）：我们若要用结构预测打分做闸口，也应只看活性位点-底物残基对，而不是全链 pLDDT。
5. **但切点是拟合出来的**：pTM 0.8 / 界面 pLDDT 84 / IRAD -128 / 能量 -16 / ipTM 0.75 全部来自同一批 149 例的 sens+spec 最大化，无留出集，且多分类 AUC 掉到 0.80 左右；作者自己还承认哨兵值赋值（无接触 → 界面 pLDDT 0 / PAE 35）会把「链没碰上」直接变成「分数极端」。→ 我们的本库判据里「阈值凑池/经验拐点」这一条缺陷清单，本文是**又一例实证**（与 B09 的 pAE_interaction<10 同类）。
6. **摘要与正文的口径差要记账**：摘要给"11% success"（对应正文 T5 口径），正文 T1 是 6%；摘要给"9%"对接基线（对应正文 medium+ 的 T1），正文还有 13%（acceptable+）；抗体数 11/12、刚体占比 62.5%/64% 也两处不一。引用这篇时必须把「哪一档 + 哪个分母 + T1 还是 T5」一起带出来，否则数字会被无声漂移。

## 7. 局限与失败（作者的 + 我们读出的）

**作者承认的**
- 见第 5.2、5.6 条：抗体/TCR 整类做不好；BM5.5 的单体构象可能在训练集里（"it is possible that individual chain structures from BM5.5 complex structures were part of the AlphaFold training set, which could influence the predicted conformations of the subunits and indirectly influence the complex structure models"）；配对 MSA 无效、RoseTTAFold 更差；其他类别也各有"upper limits of success"。
- 3 例因 GPU 内存/特征准备报错没跑出来（工程失败，非科学失败），直接从分母里减掉。

**我们读出的（推断）**
- **样本口径窄**：全部是「天然、二元、瞬态、已被解析、非冗余」的复合物，且 62–64% 是刚体（几乎不变构象）。这不覆盖：底物是小分子/金属离子/修饰残基的情形、酶-小分子底物情形、多聚体 >2 条链的情形（本文只测异源二聚体）、以及任何「设计出来的」序列。
- **分母是案例不是模型**：所有百分比都是「149 例里有几例至少有一个某档模型」，不是「模型级的精确率/召回率」。把 43% 读成「每次预测有 43% 概率准」是错的。
- **acceptable 档很松**（可含 10 Å 级 L-RMSD），而 medium/high 才对得上常用 near-native 定义；跨论文比较时若没盯住档名，同一句「成功率」能差 30 个百分点。
- **无独立验证集**：判据的 AUC 与切点在同一批数据上算，过拟合风险未评估；多分类读数明显低于二分类读数。
- **无任何湿实验、无 MD、无 QM**：这篇的证据链是「预测结构 vs 已有实验结构」的几何比较，不涉及结合自由能、不涉及催化。
- **补充材料缺失**：逐案例结果（Table S1–S8）本地未取，故本卡无法核验「哪些具体 PDB ID 属于哪个失败模式」这一层，涉及处均标「仅正文汇总值」。
- **与本工程调研记录的差异（以全文为准）**：`sources/cost-benchmarks.md` §3.4 论文 A 记的 152 例、AlphaFold top-1 43%（medium 及以上）、ZDOCK 未结合态 9%、抗体-抗原体系失败、新 Ab-Ag 集 11% —— 五个数字在全文里都能对上，只有最后一条需要补口径：全文的 11% 是「每例 5 个模型里至少有一个 medium/high」（T5），而排名第一模型命中只有 6%；摘要引的是 11% 那一档。本卡因此把 6%/11% 两档分开写（见 §2.3、§4），引用时不带档位就是错引。

## 8. 迁移判断：能不能拿 AF 预测的复合物结构判一个催化事件

**这篇的基准口径（先讲清楚，再谈能不能用）**
- **样本集合** = Protein-Protein Docking Benchmark 5.5 里的 152 个天然异源二聚体（其中 72 例含酶！——但这里的「酶」是「酶-蛋白抑制剂/蛋白底物复合物」，判的是**蛋白-蛋白界面姿态**，不是化学步骤），外加时间隔离的抗体/VLR/TCR-pMHC 追加集合。
- **准确率分母** = 案例数（149 或各类子集），不是模型数、不是设计数、更不是表达/纯化后的实测数。
- **正确性参照** = 已发表的实验结构 + CAPRI 三指标（I-RMSD/L-RMSD/f_nat）。
- 这些数字**不能**外推到我们从零设计的酶：我们的对象是「设计的酶序列 + 非天然小分子底物/辅因子」，既不在训练分布、也没有共进化配对信号、CAPRI 的界面指标也不能表达「能不能成键」。

**可迁移（怎么用）**
1. **「判据失灵边界」的证据引用**：当我们说「AF 类结构自洽判据在某个体系类别上会系统性失灵」，本文是标准弹药（抗体 0/11、100 例 6%/11%、TCR 2/14、VLR 1/7），并且给出**失灵时的形态学特征**（两链无原子接触 / 姿态错而折叠对）——对应到我们：AF 预测的「酶-底物复合物」若出现底物与催化残基零接触，就属于本文记录的失败形态，应判 METHOD_FAIL 而不是判「负结论」。
2. **界面切片优于全局分数**（第 5.4 条）→ 若我们保留任何结构预测闸口，只看「活性位点残基 ↔ 底物原子对」的子集指标（界面 pLDDT/PAE 类比物），不看全链 pLDDT。
3. **时间隔离设计**（训练截止后取样本 + 模板日期 cutoff）→ 任何我们声称「判据有效」的评测，都应有一批「晚于模型训练日期」的留出样本；本文提供了可抄的做法。
4. **反证式归因四步**（第 6.3 条）作为我们的判据体检模板。

**不可迁移（为什么不能照搬）**
1. **不许把 43%/51%/76% 写成「AF 能正确预测我们设计复合物的概率」**：这些是天然刚体二聚体、案例级、有 MSA 信号条件下的读数，与我们的分布几乎不相交。
2. **不许把 pTM 0.8 / interface pLDDT 84 / ipTM 0.75 / IRAD -128 / 结合能 -16 当我们漏斗的阈值**：它们是 sens+spec 最大化的经验切点、在同一批数据上取、无留出验证，且判的是「结合姿态对不对（vs 实验结构）」。本库判据标准明确禁止把 binder/复合物类阈值当酶活判据。
3. **本文没有任何催化几何判据**：全文未给出键长/键角/攻击角度/Met416-Lys72 那类距离阈值（原文未给阈值），也没有任何关于「预测结构与真实过渡态/产物化学关系」的讨论。想论证「AF 复合物结构能否作催化判定输入」，本文**只能支持到「结构对≠化学对」这一侧的警示**，不能支持正向结论。
4. **无 MD/QM/自由能**：本文不能为任何机制层主张（构象采样、过渡态稳定化）提供命中率背书。
5. **通量口径不可比**：这里「通量」是每例 5 个模型 × 149 例的单机 GPU 计算，不存在展示库、不存在下单-实测的漏斗递减，因此不能拿它的「命中率」填我们 CSV 的 `实验命中率` 列（该列本文只能写「不适用/无湿实验」）。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K31_PMC9278006_text.txt

- 本地纯文本：`fulltext/K31_PMC9278006_text.txt`（Europe PMC fullTextXML 抽取，标签剥离、HTML 实体已解码、未改写内容）。同一论文若有第二份抽取版本（NCBI efetch），本卡未使用；**全部引句只对照上面这一份**。
- 本卡引句为**逐字复制**：原文两处 `AlphaFold-Multimer`、`near-native`、`medium/high-accuracy` 等连字符在抽取文本里是 U+2010（非 ASCII），故凡被引句跨到的片段都已改用 ASCII 连字符安全段或截断在标记之前，未做跨句拼接；`maximization of sensitivity and sensitivity` 一处的重复词是**原文如此**（正文 2.4），方法 4.12 里的正确写法是 `the sum of the sensitivity and specificity`。
- 数字均可在该全文搜到；逐案例明细在 Table S1–S8（本地未取），涉及处已在 §0/§7 标注。
- CSV 字段映射：第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/成本统计`；第 7 节 ↔ `在方法演进链的位置`。
- 本卡自检命令：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K31" --no-report`（结果见本次交付回报；未跑全量门禁、未跑 `--sync-map`）。

<!--CSV回填
work_type=论文（计算基准/benchmark，非设计方法，无湿实验）
target=152 个 BM5.5 异源二聚体（12 抗体-抗原/72 含酶/68 其他）+ 追加 20 例与 100 例抗体-抗原、7 例 VLR/repebody、14 例 Class I TCR-pMHC
backbone_generation=不适用（不做候选生成）；被评测的模型由 AlphaFold 本地版 / ColabFold advanced / AlphaFold-Multimer / RoseTTAFold 各出 5 个模型每案例，对照组 ZDOCK 3.0.2 刚体对接每案例 54,000 姿态
computational_filters=pTM；平均 pLDDT 与 resolved pLDDT；interface PAE(4 Å)；interface pLDDT(4 Å)；ipTM；IRAD；ZRANK2；Rosetta 跨界面结合能与界面面积/氢键数/残基数/shape complementarity；N_eff 与 BSA 作为失败关联特征；评级用 CAPRI（I-RMSD/L-RMSD/f_nat）
thresholds=pTM=0.8；interface pLDDT=84；IRAD=-128；Rosetta cross-interface binding energy=-16；ipTM≈0.75；near-native 参照 2.5 Å I-RMSD（acceptable 档可含 up to 10 Å L-RMSD）；追加晶体分辨率 cutoff<3.25 Å；N_eff 用 CD-HIT 62% identity；界面接触 cutoff 测 4–10 Å——以上切点均由同一批 149 例按 sensitivity+specificity 之和最大化算出，无独立留出集
md_used=否（无分子动力学；仅在模型后处理把 AlphaFold 默认 Amber relaxation 换成 Rosetta constrained FastRelax 做结构弛豫，非动力学采样）
qm_used=否（全文无量子化学/过渡态计算）
experimental_methods=无新增湿实验；参照物为 PDB/SAbDab/TCR3d 已发表实验结构，按 CAPRI 标准几何比对（自写脚本），统计用 Wilcoxon rank-sum、Pearson、pROC/multiROC AUC（2000 bootstrap CI）、cutpointr 取切点
pipeline_counts=152 例入选 → 149 例成功建模（3 例 GPU 内存/特征报错）→ 149×5 模型；分组难度 95/34/23；追加抗体集 20 例 → 2 例 medium 且排 #1；VLR/repebody 7 例 → 1 例有正确模型；Multimer 抗体 7 例 vs 非抗体 17 例；抗体大集 100 例（73 heavy-light + 27 nanobody）；TCR-pMHC 14 例 → 2 例命中
hit_rate=AlphaFold T1：acceptable+ 51%、medium+ 43%、high 21%（T5：54%/44%/23%）；ZDOCK T1：13%/9%/1%；难度分档 47/55/78%（acceptable+，T5）与 27/16/17%（high）；抗体-抗原 BM5.5 子集 0/11；100 例抗体集 T1 6% / T5 11%（摘要只报 11%）；TCR-pMHC 2/14=14%；无 MSA 非抗体 1/17=6% vs 有 MSA 13/17=76%
best_metric=不适用（本文不测亲和力或催化活性，无 Kd/活性最好值；判别力最好读数为 Rosetta 跨界面结合能二分类 AUC 0.99（0.99-1.00），interface pLDDT 0.97、interface PAE 0.93，但多分类 AUC 仅 0.81–0.84）
cost_or_stat_note=单机 GPU（NVIDIA Titan RTX / Quadro 6000），每案例 5 模型，3 例因 GPU 内存报错未完成；ColabFold 用于百例级批量；pTM 与 TM-score r=.82、与 I-RMSD r=-.55（p<.001）；BSA 与成功关联 p=.007 而 MSA 深度不显著；同行独立基准（216 例 Dockground）报 acceptable+ 63% 对本文 51%，说明口径/样本集换一套读数就变
role_in_timeline=AF2 复合物预测能力的第一批系统基准之一：把「AF 端到端能预测复合物」确立为可用，同时划出适用边界（抗体-抗原、VLR、TCR-pMHC 这类无共进化信号界面失灵），并把模型质量判据从全局 pTM/pLDDT 推进到界面切片指标（interface pLDDT/PAE、ipTM）——即后来 binder 设计类论文 pAE_interaction/ipTM 闸口的方法学前身；同时提供「判据阈值在同一批数据上取切点、无留出」的典型缺陷样本
source_pointer=data/literature_cards/fulltext/K31_PMC9278006_text.txt（Europe PMC fullTextXML，80,755 B；DOI 10.1002/pro.4379 / PMC9278006 / PMID 35900023）；登记底稿另见 sources/cost-benchmarks.md §3.4 论文 A
CSV回填-->
