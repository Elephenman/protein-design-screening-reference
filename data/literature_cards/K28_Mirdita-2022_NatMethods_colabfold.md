# [K28] ColabFold：把 AlphaFold2 的三道成本墙（搜索、显存、重编译）拆掉——下游漏斗敢把 AF2 当默认闸口的成本前提

Mirdita M, Schütze K, Moriwaki Y, Heo L, Ovchinnikov S, Steinegger M（Max Planck 多学科研究所 / 首尔国立大学 / 东京大学 / Michigan State / Harvard）
Nature Methods 2022, 19:679–682 · DOI 10.1038/s41592-022-01488-1 · PMID 35637307 · PMCID PMC9184281
Brief Communication · 开放获取（CC BY 4.0）· https://doi.org/10.1038/s41592-022-01488-1

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K28**（组：通用方法学; 口径对照） |
| 本文取回方式 | Europe PMC `search`（DOI 精确命中）→ `fullTextXML`，抓取通道记录 `epmc_search_then_fulltext` |
| 本地全文 | `fulltext/K28_PMC9184281_fullTextXML.xml`（110,969 B，SHA-256 `daf0a6d49ddf394f…`）→ 去标签纯文本 `fulltext/K28_PMC9184281_text.txt`（58,465 B，SHA-256 `458432022ef0508d…`） |
| 对照底稿 | `sources/cost-benchmarks.md:64`（成本行：单 GPU 约 1,000 结构/天、搜索 40–60×、单条整体 5×；该表已注明 86 GPU·s/结构 是**本报告推算**，不是原文） |
| 证据级别 | **全文级**（本卡所有英文引句均可在本地纯文本里逐字命中；见第 9 节自检） |
| 未取到的部分 | Supplementary Figs 1–6、Supplementary Table 1、Source Data Fig. 2、Reporting Summary、Fig. 1/2 图内原始数值与散点。凡涉及这些处，本卡明写"正文只给图号，未给数值" |
| 这篇不是设计论文 | 全文没有任何 de novo 设计、没有湿实验、没有结合/催化测量；它只交付**成本与结构口径**，因此第 8 节的迁移判断只允许迁到"算得起/怎么算"，不许迁到"酶活概率" |
| 作者自述的贡献归属 | "These authors contributed equally: Milot Mirdita, Sergey Ovchinnikov and Martin Steinegger." |

## 1. 这篇到底解决什么（一句话）

AlphaFold2 的精度已经不是问题，问题是**普通实验室跑不起它**：建一个 MSA 要几小时、数据库要 2 TB 以上、显存要装得下 ~1,000 残基的输入、而 Google 免费的 AlphaFold-Colab 靠把环境库砍成八分之一来换免费、精度就掉下来了。ColabFold 做的事是把**搜索**从 HMMer/HHblits 换成 MMseqs2（快 40–60 倍）、把**环境库**重建成能装进 84 GB 内存的版本、把**推理**改成"编译一次 + 复用权重 + 早停"，结果单条预测整体快约 5 倍、批量快约 90 倍、一台单 GPU 服务器一天能出接近 1,000 个结构，而 CASP14 全集平均 TM-score 与 AlphaFold2 打平（0.887 对 0.888）。它是此后所有把 AF2 当筛子的设计论文（含本表 B09）在成本上成立的前提。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **搜索侧的存储与时间墙**（原文摆的是硬数字）："Due to their large size, searches can take up to hours for a single protein while requiring more than 2 TB of storage space alone."，推理侧还得 "graphics processing units (GPUs) with a large amount of GPU RAM (random access memory) are required even for relatively common protein sizes of ~1,000 residues"；作者并且指出真正的瓶颈在哪："For these, however, the MSA generation dominates the overall run time."
   **应对**：① 搜索整体换引擎——"ColabFold speeds up single predictions by replacing AlphaFold2's homology search with the 40-60-fold faster MMseqs2"；② 搜索放在**服务器端**做（`colabfold.mmseqs.com`），本地不下载 2 TB；③ 不搜全库而搜聚类共识序列："This expanding search results in a speed-up of ~10-fold given that only 29.3 million cluster consensus sequences are searched instead of all 277.5 million UniRef100 sequences."；④ 数据库本身削减："This reduced the total number of sequences from 2.5 billion to 513 million, thus requiring only 84 GB RAM for headers and sequences."
2. **免费方案靠砍库换速度，精度掉**：AlphaFold-Colab 的 MSA 是 "for which the input MSA is built by searching with HMMer against the UniProt Reference Clusters (UniRef90) and an eightfold-reduced environmental database"，作者直接判它的后果："This results in less accurate predictions while still requiring long search times."（FM 靶平均 TM-score：AlphaFold-Colab 0.744，AlphaFold2 0.79，ColabFold-AF2 0.826）
   **应对**：不砍库，换搜索引擎 + 重建库。把 BFD 与 MGnify 合并（>30% identity、≥90% 覆盖归簇）再按簇只留 10 条最多样序列："To reduce the size of the database we filtered each cluster, keeping only the 10 most diverse sequences using mmseqs filterresult --diff 10."
   **应对后仍留下的代价**：搜索参数是**在自由建模靶上调出来的**——"given that we used the free-modeling targets for optimization of search workflow parameters"，而 Fig. 2a 报的 FM 组分数（0.826）正是同一批靶；作者把 FM 与非 FM 分开画，但没有给"独立测试集"上的调参前后对照。
3. **内存墙在免费 Colab 上是随机的**："Reducing the memory requirement is especially helpful in Google Colaboratory, where the provided system is selected from a pool with widely differing capabilities."
   **应对**：三层截断——库里每簇留 10 条；MSA 侧用分桶多样性过滤（每桶留 3,000 条最多样，"Our filter keeps the 3,000 most diverse sequences in the identity buckets [0.0-0.2], (0.2-0.4], (0.4-0.6], (0.6-0.8] and (0.8-1.0]."）；模型输入侧沿用 AF2 自己的截断："Alphafold2, depending on model configuration, subsamples the MSA to a maximum of 512 cluster centers and 1,024 extra sequences."
   **代价**：他们自己给了"少而多样的 MSA 就够"的依据——"Prediction quality depends on the input MSA, however, often an MSA with only a few (~30) sufficiently diverse sequences is enough to produce high-quality predictions"——但这是一条**借用他人结论**（文中指向 AF2 论文的 fig. 5a），不是本文实测。
4. **推理侧的成本藏在编译与"五个模型全跑"**："The AlphaFold2 models are compiled using JAX 31 to optimize the model for specific MSA or template input sizes."（此处原文夹引文编号，故只取前句），而作者观察到 "We noted that for prediction of high certainty (pLDDT >85), all five models would often produce structures of very similar confidence, for some even without or with less than three recycles."
   **应对**：① 只编译一个模型换权重："Second, we compile only one of the five AlphaFold2 models and reuse weights."，"When no templates are provided, we compile once and, during inference, replace the weights from the other models, using the configuration of model 5."，效果 "This saves 7 min of compile time."（开模板时 "This saves 5 min of compile time."）；② 批量时按长度排序 + 只 pad 10%："We sort the input queries by sequence length and process them in ascending order."，"We pad the input features by 10% (by default)."；③ 早停："We also implemented an option to specify a tolerance threshold to stop early."，"halts additional model inferences and stops recycling if a given pLDDT or (interface) predicted TM-score threshold is reached"。
   **代价**：早停的验收口径是**模型自评分** pLDDT，不是对实验结构的 TM-score；且只在 50 条抽样蛋白上给过对照（见第 7 节）。
5. **AlphaFold2 最初不能建模复合物，而配对 MSA 需要真同源配对**："In addition to predictions for single chains, RoseTTAFold and, later, AlphaFold, were also shown to generalize to protein complexes."；他们先试拼接——"However, we found that by combining two sequences with a glycine linker 20 it could often successfully model complexes."——再改用位置编码偏移："By offsetting the residue index between two proteins to be > 32, AlphaFold2 treats them as separate polypeptide chains."；配对侧定了硬规则："We return only hits that cover all complex proteins within one species and pair only the best hit (smallest E-value) with an alignment that covers the query to at least 50%."；同源寡聚体的 MSA 复制方式还有过一个反直觉发现："Interestingly, it was found that providing a separate MSA copy (padding by gap characters to extend to other copies) works significantly better than concatenating from left to right."
   **应对后仍留下的代价**：两种模式谁更好**没有统一判据**，只有"ClusPro 上用 AlphaFold-multimer 模型精度最高"这一总体结论（Fig. 2c，17 个靶）；复合物置信度只能靠 PAE 派生量排序，"Single chain predictions are ranked by pLDDT and complexes by predicted TM-score."
6. **MMseqs2 自身的过滤会把某些靶搜坏**：他们给出一个具体病例："The prediction of target T1084 can be improved from a TM-score of 0.457 to 0.872 by ColabFold if MMseqs2's compositional filter is disabled"，并把其余异常靶交给补充材料："Supplementary Table 1 lists the additional targets for which ColabFold differed significantly from AlphaFold2."
   **应对**：把参数全部暴露给用户（advanced notebook 可改 `max_recycle`、`num_ensemble`、`is_training`、随机种子、可上传自定义 MSA），即**不替用户做决定**。
   **代价**：本文未解决——没给出"什么序列该关组成分过滤、什么该改用 HMMer 搜"的可操作判据，只给了个案与清单。
7. **设计蛋白 / 无已知同源序列的靶最难（对我们这一支最相关）**："For difficult targets as well as for designed proteins without known homologs, additional recycling iterations can result in a high-quality prediction (Supplementary Fig. 5 )."，早停也正好在这类上有用："For some designed proteins without known homologous sequences, this helped to fold the final protein"
   **应对**：把 recycle 从默认 3 提到 12 重跑 CASP14："Rerunning the CASP14 benchmark with a recycle count of 12 resulted in an improvement of targets with little MSA information, resulting in an increased average TM-score of 0.898"；再加"多种子 + dropout 采样"来扫构象多样性。
   **代价**：设计蛋白层面的证据只在补充图里，正文没有给出"多少条设计序列、多少条折对"的比例；`~30` 条多样序列就够这一说法在无同源的设计序列上是否成立，本文未解决。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **同源性搜索**：MMseqs2（文中版本 `edb822`）替掉 AF2 的 HMMer + HHblits；三次 profile 迭代 + 集群扩张；多样性过滤借用 HHblits v3.3.0 的分桶算法（移植进 MMseqs2）。
- **数据库**：UniRef30（UniRef100 的聚类版，2021_03）、自建 `BFD/MGnify`（合并后 513M 序列 / 84 GB RAM）与 `ColabFoldDB`（再加真核 SMAG/MetaEuk/TOPAZ、DNA 病毒 MGV、噬菌体 GPD、更新版 MetaClust）；模板库 PDB70。
- **结构推断**：AlphaFold2（可给模板）与 RoseTTAFold（后者可走 PyRosetta 折叠协议、侧链用 SCWRL4）；复合物走 residue-index 偏移或 AlphaFold-multimer 微调参数；可选 AMBER 力场弛豫。
- **置信度与排序**：单体按 pLDDT、复合物按 pTM / inter-PAE / iPTM；批量时 pLDDT 或 (interface)pTM 兼作早停阈值。
- **评价口径（不是筛选）**：单体 TM-score（TMalign）、复合物 DockQ、背景引用 GDT_TS。
- **交付形态**：四个 Jupyter notebook（basic / advanced / batch / RoseTTAFold）+ `colabfold_search` + `colabfold_batch` + LocalColabFold（Win10+WSL2 / macOS / Linux，CUDA 11.1+）。
- **没有用的方法**：分子动力学采样、量子化学、自由能微扰；唯一的力场用途是结构弛豫（"relaxing of the predicted structures using amber force fields"），不是轨迹/构象采样。

### A. 一次预测的执行流（正文 + Methods 2.2–2.5；服务器端搜索）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 用户 FASTA（单条序列，或复合物多条序列） | 提交到 MMseqs2 服务器；先对 UniRef30 共识序列做三次迭代 profile 搜索 | 命中接受阈值："We accept hits with an E-value lower than 0.1." | 搜索对象只有 29.3M 条共识序列（不是全 277.5M 条 UniRef100），作者称这一步带来 ~10 倍加速 |
| A2 | A1 的命中 + 簇信息 | 用最后一次迭代的 profile 把每个命中所属 UniRef100 簇的**成员**重新展开、对齐后并入 MSA（扩张式搜索） | 簇内先去冗："such that no cluster pair has a higher maximum sequence identity than 95% (--max-seq-id 0.95)." | 第一个 A3M（UniRef 侧） |
| A3 | UniRef30 序列 profile | 拿它去迭代搜 `BFD/MGnify` 或 `ColabFoldDB`："We use the UniRef30 sequence profile to perform an iterative search against the BFD/MGnify or ColabFoldDB using the same parameters, filters and expansion strategy." | 与 A1/A2 同一套参数（原文未给新的阈值） | 第二个 A3M（环境侧）；服务器共返回两个 A3M |
| A4 | 两个 A3M | 三级多样性感知过滤：簇展开阶段先按 95% identity 去冗；重对齐后只留 `--qsc` 一项；建 MSA 时按 identity 分六桶再截 | "In the second stage, after realignment we enable only the --qsc 0.8 threshold and disable all other thresholds"；"Additionally, the qsc filtering is used only if at least 100 hits are found (--filter-min-enable 100)."；"In the last stage, during MSA construction we filter again with the following parameters: --filter-min-enable 1000 --diff 3000 --qid 0.0,0.2,0.4,0.6,0.8,1.0 --qsc 0 --max-seq-id 0.95."；"In buckets containing less than 1,000 hits we disable the filtering." | 每桶最多 3,000 条最多样序列；模型侧最终只用 512 cluster centers + 1,024 extra sequences |
| A5（可选） | 同一查询 | 模板：先用 MMseqs2 在 PDB70 聚类代表上做预筛，再只对少量候选做 HHsearch 精对齐 | "Only the top 20 target templates according to E-value are then aligned by HHsearch."（AF2 原生是对全 PDB70 做 HHsearch 取 20 条） | top 20 模板；注意作者自述 "For benchmarking, no templates are given to ColabFold." |
| A6（复合物） | 复合物各组分序列 | 每个组分分别搜 UniRef100，再用新模块 `pairaln` 按物种配对，另附两份 unpaired MSA | "We return only hits that cover all complex proteins within one species and pair only the best hit (smallest E-value) with an alignment that covers the query to at least 50%." | 配对 MSA + unpaired MSA；同源寡聚体用 MSA 复制 + gap padding |
| A7 | A4/A6 的特征 | AlphaFold2 或 RoseTTAFold 推理；recycle 与 ensemble 数可调 | 默认 recycle：3（"AlphaFold2 improves the predicted protein structure by recycling (by default) three times"）；提升路径：12 | 结构 + pLDDT + PAE；单体按 pLDDT 排、复合物按 pTM 排："Single chain predictions are ranked by pLDDT and complexes by predicted TM-score." |
| A8 | 多条序列（批量） | `colabfold_batch`：按长度升序处理 + pad 10% 避免重编译 + 早停 | "We pad the input features by 10% (by default)."；"halts additional model inferences and stops recycling if a given pLDDT or (interface) predicted TM-score threshold is reached" | 单 GPU 服务器吞吐接近 1,000 结构/天（见第 4 节原句） |

### B. 加速与精度是怎么被验证的（Methods 2.7；这是"能不能引用它的成本数字"的依据）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | CASP14 全集 | 五种配置互比（AF2 默认带模板、AlphaFold-Colab 不带模板、CF-AF2-BFD/MGnify、CF-AF2-ColabFoldDB、CF-RoseTTAFold-BFD/MGnify），一律不带模板跑 ColabFold 各模式 | 评价量是 TM-score，"We compared the predictions against the experimental structures using TMalign (downloaded on 24 February 2021)"；无筛选阈值（原文未给阈值，只报平均值） | "The 65 targets contain 91 domains, among these are 20 free-modeling targets with 28 domains."；FM 组 TM 0.826/0.818/0.79/0.744/0.62，全集 0.887/0.886/0.888/0.754 |
| B2 | 同一批 CASP14 查询 | 计时：MSA 生成与模型推断**分开测**；服务器 2×14 核 Intel E5-2680v4 / 768 GB | "MSA generation was repeated five times and the MSA generation times were averaged."；"For a fair comparison, AlphaFold2 was modified to allow HMMer and HHblits to access one CPU core."；ColabFold 侧每条 MSA 也只占一个核 | 单条预测整体约 5 倍快："ColabFold is on average fivefold faster for single predictions than AlphaFold2 and AlphaFold-Colab" |
| B3 | ClusPro 复合物集 | 复合物精度对比（residue-index 模式 vs AlphaFold-multimer 模式） | 评价量 DockQ："We compare predictions of 17 ClusPro"（原文此处紧跟引文编号 4,12，故拆分不跨）；排序用 "Models are ranked by predicted interface TM-score as returned by AlphaFold-multimer." | 17 个靶；结论：AlphaFold-multimer 模式总体最好 |
| B4 | `M. jannaschii` 蛋白组 | 全蛋白组跑通：先搜后推，早停阈值设在 pLDDT 85 | "Of the 1,787 proteins, we exclude the 25 proteins longer than 1,000 residues, leaving 1,762 proteins of 268 amino acids in average length."；"For each query we stop early if any recycle iteration reaches a pLDDT of at least 85." | 搜索："we search against the ColabFoldDB (section 2.3.2 ) in 113 min on a system with an AMD EPYC 7402P 24-core CPU (no hyperthreading) and 512 GB RAM."，"MMseqs2 had a maximum resident set size of 308 GB during the search."；推理："We then predict the structures on a single Nvidia Titan RTX with 24 GB RAM in 46 h using only MSAs (no templates)." |
| B5 | 同上 | 早停收益与精度代价量化 | 早停阈值 pLDDT ≥ 85（原文未给其他阈值） | "Early stopping results in a speed-up of 3.7-fold compared with the default and 4.8-fold compared with always recompiling."；50 条抽样的平均 pLDDT 三档 90.68 / 90.22 / 89.33；全蛋白组三档 89.75 / 89.38 / 88.77 |

**这套流程的组织方式值得单独记住**：它把"一次预测"拆成**可独立优化的两段**（A1–A4 搜索、A7–A8 推理），并**分别计时**再报总倍数；对搜索段用"共识序列 + 扩张 + 分桶截断"，对推理段用"编译一次 + padding 复用 + 自评分早停"。凡本文报出的加速，都是在这两个可复算的口径上得到的。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 92.4% | AF2 在 CASP14 的中位 GDT_TS（本文背景引用值） | "at a median global distance test total score (GDT_TS) of 92.4%" |
| 数小时 / >2 TB | AF2 原生搜索的单条耗时与库存储 | "searches can take up to hours for a single protein while requiring more than 2 TB of storage space alone" |
| ~1,000 residues | 需要大显存的常见蛋白长度 | "required even for relatively common protein sizes of ~1,000 residues" |
| 40–60 倍 | MSA 搜索加速（MMseqs2 换 HMMer/HHblits） | "ColabFold's 40-60-fold faster search and optimized model utilization enables prediction of close to 1,000 structures per day on a server with one graphics processing unit." |
| ~90 倍 | 批量预测加速（免重编译 + 早停） | "and speeds up batch predictions by ~90-fold by avoiding recompilation and adding an early stop criterion." |
| 接近 1,000 结构/天 | 单 GPU 服务器吞吐（摘要口径） | 同上 40-60 倍那条原句 |
| 约 5 倍 | 单条预测整体（搜索+推断）加速 | "ColabFold is on average fivefold faster for single predictions than AlphaFold2 and AlphaFold-Colab" |
| 3 次迭代 / E-value < 0.1 | UniRef30 搜索的迭代数与命中阈值 | "We accept hits with an E-value lower than 0.1." |
| 29.3M vs 277.5M（~10 倍） | 共识序列搜索 vs 全 UniRef100 | "This expanding search results in a speed-up of ~10-fold given that only 29.3 million cluster consensus sequences are searched instead of all 277.5 million UniRef100 sequences." |
| ~30 条 | 足以出高质量预测的多样序列数（转引自 AF2 论文 fig. 5a） | "often an MSA with only a few (~30) sufficiently diverse sequences is enough to produce high-quality predictions" |
| 95%（`--max-seq-id 0.95`） | 簇展开阶段去冗阈值 | "such that no cluster pair has a higher maximum sequence identity than 95% (--max-seq-id 0.95)." |
| `--qsc 0.8`；≥100 命中才启用 | 重对齐阶段的唯一启用阈值 | "In the second stage, after realignment we enable only the --qsc 0.8 threshold and disable all other thresholds" |
| `--diff 3000`；六桶各 3,000 条；<1,000 命中的桶不过滤 | 建 MSA 阶段的分桶多样性截断 | "Our filter keeps the 3,000 most diverse sequences in the identity buckets [0.0-0.2], (0.2-0.4], (0.4-0.6], (0.6-0.8] and (0.8-1.0]." |
| 512 cluster centers + 1,024 extra sequences | 模型输入侧的 MSA 截断上限 | "subsamples the MSA to a maximum of 512 cluster centers and 1,024 extra sequences" |
| 2.5 billion → 513 million（~517 GB → 84 GB RAM） | BFD/MGnify 合并削减后的序列数与内存 | "This reduced the total number of sequences from 2.5 billion to 513 million, thus requiring only 84 GB RAM for headers and sequences." |
| ~2.2 billion 序列 / 64 million 簇；~300 million | BFD 与 MGnify(2019_05) 原始规模 | "BFD is a clustered protein database consisting of ~2.2 billion proteins organized in 64 million clusters." |
| >30% identity + ≥90% 覆盖；182 million 簇；每簇留 10 条 | 两库合并与 ColabFoldDB 的归簇规则 | "Each MGnify sequence with a sequence identity of >30% and a local alignment that covers at least 90% of its length is assigned to the respective BFD cluster." |
| 209,335,865 条代表序列 + 738,695,580 条成员 | ColabFoldDB 最终规模（原文该处误写成 "209,335,865 million"，按上下文应为 2.09 亿条） | "The final database consists of 209,335,865 million representative sequences and 738,695,580 members" |
| top 20 模板 | MMseqs2 预筛后才交给 HHsearch 精对齐的模板数 | "Only the top 20 target templates according to E-value are then aligned by HHsearch." |
| \|i-j\| 偏移 > 32 | 让 AF2 把两条链当分开多肽的位置编码技巧 | "By offsetting the residue index between two proteins to be > 32, AlphaFold2 treats them as separate polypeptide chains." |
| 覆盖 query ≥ 50%、同物种、最小 E-value | 复合物 MSA 配对规则 | "pair only the best hit (smallest E-value) with an alignment that covers the query to at least 50%." |
| recycle 默认 3；提到 12 → TM 0.898 | 循环次数与精度收益 | "Rerunning the CASP14 benchmark with a recycle count of 12 resulted in an improvement of targets with little MSA information, resulting in an increased average TM-score of 0.898" |
| 省 7 min / 5 min 编译 | 只编译一个模型（无模板 / 有模板） | "This saves 7 min of compile time." |
| pad 10%；按长度升序 | 批量避免重编译的做法 | "We pad the input features by 10% (by default)." |
| pLDDT ≥ 85 早停 → 3.7 倍 / 4.8 倍 | 早停相对默认与每次重编译的加速 | "Early stopping results in a speed-up of 3.7-fold compared with the default and 4.8-fold compared with always recompiling." |
| 1,787 → 剔 25 条 → 1,762 条（均长 268 aa） | 蛋白组基准的输入规模与剔除规则 | "leaving 1,762 proteins of 268 amino acids in average length" |
| 113 min 搜索 / RSS 308 GB / 512 GB RAM（EPYC 7402P 24 核） | 蛋白组 MSA 搜索的时间与内存 | "MMseqs2 had a maximum resident set size of 308 GB during the search." |
| 46 h 推理（Titan RTX 24 GB，无模板）｜正文写 48 h | 蛋白组结构推断时间；正文把 113 min + 46 h 合称 "in 48 h" | "We then predict the structures on a single Nvidia Titan RTX with 24 GB RAM in 46 h using only MSAs (no templates)." |
| 90.68 / 90.22 / 89.33（50 条抽样）；89.75 / 89.38 / 88.77（全蛋白组） | 三档平均 pLDDT：AF2(reduced_dbs) / ColabFold 默认 / ColabFold 早停 | "AlphaFold2 (reduced_dbs, v2.1.1), ColabFold (commit f5d0cec) default and ColabFold Stop ≥ 85 have an average pLDDT of 90.68, 90.22 and 89.33, respectively, for 50 randomly sampled proteins." |
| FM 靶 TM 0.826 / 0.818 / 0.79 / 0.744 / 0.62 | 五种配置在自由建模靶上的平均 TM-score（CF-AF2-BFD/MGnify、CF-AF2-ColabFoldDB、AF2、AF-Colab、CF-RoseTTAFold） | "The mean TM-scores for the free-modeling targets are 0.826, 0.818, 0.79, 0.744 and 0.62 for ColabFold-AlphaFold2-BFD/MGnify, ColabFold-AlphaFold2-ColabFoldDB, AlphaFold2, AlphaFold-Colab and ColabFold-RoseTTAFold-BFD/MGnify, respectively." |
| 全集 TM 0.887 / 0.886 / 0.888 / 0.754 | 全集（不含 AlphaFold-Colab）对应同一顺序的前三者 + CF-RoseTTAFold | "the TM-scores are 0.887, 0.886, 0.888 and 0.754 for the respective methods" |
| 0.457 → 0.872（T1084） | 关掉 MMseqs2 组成分过滤后的单靶改善 | "The prediction of target T1084 can be improved from a TM-score of 0.457 to 0.872 by ColabFold if MMseqs2's compositional filter is disabled" |
| 65 靶 / 91 域 / 20 FM 靶 / 28 FM 域；ClusPro 17 靶；抽样 50 条 | 三个基准的样本量 | "The 65 targets contain 91 domains, among these are 20 free-modeling targets with 28 domains." |
| 2×14 核 / 768 GB（搜索）；2×16 核 / 192 GB / 4×RTX5000 单卡跑（推理） | 计时所用的硬件 | 第 3 节 B2 |
| 120 MDa | 正文举的一个实际复合物应用（人核孔复合体，冷冻电镜） | 正文该句夹引文编号 23，故不整句引用；数值取自该句 |

## 5. 结论——作者说了什么

1. ColabFold 用 MMseqs2 替换 AF2 的同源性搜索，**搜索快 40–60 倍**；批量再靠免重编译与早停**约 90 倍**。
2. 单条预测（搜索 + 推断合计）**平均快约 5 倍**，一台单 GPU 服务器**一天接近 1,000 个结构**，因此它是"free and accessible platform"。
3. 精度上他们的措辞是**追平不是超越**："We show that ColabFold outperforms AlphaFold-Colab and matches AlphaFold2 on CASP14 targets and also matches AlphaFold-multimer on the ClusPro"（该句原文后面接引文编号 4, 12，故只引到此处）。
4. 复合物可用：residue-index 偏移 + 按物种配对 MSA 能做出高精度复合物预测，且与 AlphaFold-multimer 模型各有所长；已用于人核孔复合体（120 MDa）冷冻电镜结构解析的辅助。
5. 批量场景的取舍：把早停阈值（pLDDT ≥ 85）交给用户，作者称"几乎不牺牲精度"（正文原句为 "while sacrificing little or no prediction accuracy"）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的真正产物是"成本口径"，不是新算法**。它把"跑一次 AF2 值多少钱"变成可复算的四个数：113 min + 308 GB RSS（搜索，24 核 CPU）、46 h（推理，1 张 24 GB 卡）、1,762 条（样本量）、3.7×/4.8×（早停收益）。→ 我们此后引用 AF2/ColabFold 作漏斗闸口时，**应当引这四个数而不是引"1,000/天"**；后者是摘要级的乐观折算（含早停、且把 113 min 搜索折进 46 h 推理报成 48 h）。
2. **"1,000 结构/天" 的分母只有一种蛋白**。均长 268 aa 的 `M. jannaschii` 蛋白组，且已剔除 25 条 >1,000 残基的长蛋白——这正好是 AF2 最便宜的一段。→ 对我们：若候选里有跨膜段、长连接子、多结构域拼装，这条吞吐线不能直接套用。
3. **加速与精度是两条独立证据链**，本文的加速来自"引擎 + 编译 + 早停"，精度证据只有 CASP14 的 65 靶/91 域与 ClusPro 的 17 靶；**早停带来的精度代价是用模型自评的 pLDDT 度量的，不是用对实验结构的 TM-score 度量的**。→ 对我们：凡用"模型自评分"当闸口阈值（pLDDT / pAE / iPTM），都必须承认它没有独立精度验证时，其"几乎无损"是不可证的。
4. **两处测量口径不一致，值得警惕**：单条计时处 "For a fair comparison, AlphaFold2 was modified to allow HMMer and HHblits to access one CPU core."，蛋白组基准处又 "We changed the AlphaFold2 source code to utilize all CPU cores during the homology search."。同一篇里对基线做了两种相反的改动，40–60× 建立在"限一核"的 AF2 上、而蛋白组的 48 h 建立在"全核"的 AF2 外推上（Fig. 2d 的虚线只是按 50 条外推）。
5. **对我们最有用的一句话不是加速，而是第 7 个难点**：无同源序列的设计蛋白要靠**加大 recycle + 多种子采样 + dropout** 才折得对。这说明 AF2 对设计序列的默认 3 次 recycle 是"欠采样"设置；我们若用 AF2/ColabFold 复核设计构象，默认参数得到的低置信度**不能直接判死**，至少要跑一次高 recycle 对照。
6. **库的"多样性"是可控资源**。`--diff` 分桶截断与每簇留 10 条这类做法，本质上是在**用进化多样性而非进化条数**换内存。→ 对应我们：给 UAA 合成酶候选做 MSA 时，"多少条"不是关键，"每段 identity 桶里有没有代表性"才是；对近缘同源过多的家族，全量堆序列只会撑爆显存而不加信息。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自述/可归因于本文口径的**

- 搜索参数在 FM 靶上调的、又在 FM 靶上报分："given that we used the free-modeling targets for optimization of search workflow parameters"（本文未给独立测试集上的调参前后差）。
- 基准一律不带模板："All three ColabFold modes were executed without templates."；同时 AF2 参照组是默认带模板设置（第 3 节 B1 所列配置），两边的输入特征不等价。
- 复合物基准只有 17 个靶，且模式间互有胜负（正文承认 residue-index 模式在部分靶上更好）。
- 有靶点被自家过滤规则伤害，只给了个案与补充清单，没给判据（第 2.6 节）。

**我们读出的**

1. **"牺牲很少精度"没有独立精度验证**：早停的全部质量证据是 50 条随机抽样蛋白的平均 pLDDT（90.68 → 89.33）与全蛋白组 pLDDT（89.75 → 88.77），**没有对实验结构算 TM-score**。pLDDT 既是 stopping rule 又是评价指标，是同义反复。
2. **正文与 Methods 的 pLDDT 数字对不齐**：正文称 50 条抽样里 "The average pLDDTs of AlphaFold2 and ColabFold Stop" 为 89.75 与 88.78，而 Methods 同一 50 条抽样给的是 90.68 与 89.33；89.75 在 Methods 里是"全蛋白组 AlphaFoldDB 参照"的值。两处至少有一处口径串了。
3. **数据库规模句有笔误**："The final database consists of 209,335,865 million representative sequences and 738,695,580 members"——`209,335,865 million`（≈2×10^14）与成员数 7.4×10^8 不可能同时成立，按上文削减逻辑应是 2.09 亿条代表序列。凡引用库规模者须按此校正。
4. **加速的对照口径混用**（第 6.4 条）：CPU 核数在两个基准里被反向修改，且 AlphaFold-Colab 的计时是从 notebook 输出单元格里取的（"The JackHMMer search uses eight threads." 与本文服务器端"每条 MSA 单核"不是同一并行度）。
5. **全文没有一条湿实验**：所有"精度"都是计算结构与既有实验结构比分数；因此这篇**不能**为任何"折叠对 ⇒ 功能对"的命题提供证据。
6. 未覆盖：多序列输入的失败率、`ColabFoldDB` 相对 `BFD/MGnify` 在非细菌序列上的量化收益（正文只在补充图里说 MSA 更多样）、以及设计序列的命中率统计（正文未给出）。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **成本必须拆段报**（搜索段 vs 推理段 vs 编译段，各自给秒数与内存峰值 RSS）。我们目前只有 MD 与 xTB 的吞吐（156.6 ns/day；271 原子 153.3 s/评价），没有"每 1,000 个候选的结构预测要花多少 GPU·h、峰值内存多少"。按本文口径补一张同构表，是决定漏斗能不能扩到千级候选的前提。
2. **早停/截断必须配一条独立质量证据**。本文的教训是反面教材：用 pLDDT 当 stopping rule 又用 pLDDT 当验收。→ 我们的任何"算到一半就丢"的规则（比如 MSA 深度不足直接丢、或 MD 跑不满就截），验收量必须来自**另一个量**（对接/电子密度/实验对照），且在同样 N≥50 的随机抽样上做双口径对照。
3. **基线公平性要写成可查的口径**：本文两处对 AF2 的核数改动方向相反。→ 我们做 xTB/MD/AF23 对比时，须把"基线是否被我们改成更快/更慢配置"逐条写明，否则倍数不可比。
4. **对无同源序列的设计蛋白，默认 AF2 参数会低估**：把 recycle 提高（3 → 12）与多种子 + dropout 采样当成复核步骤，而不是拿到第一个低置信度结果就判死；同时在结果里报 MSA 深度与多样性（本文把这两项做成默认可视化输出）。
5. **MSA 用"分桶多样性"而不是条数**：`--diff` 式分桶截断可以在几乎不丢信息的情况下压内存，适合我们面对近缘家族过度采样的情形。

**不可迁移（为什么不能照搬）**

1. **pLDDT / pTM / iPTM / inter-PAE 全是"结构自洽与界面可信度"的量，与 UAA 酶活无对应关系**。DP2R 口径明令不许把 binder/折叠类置信度阈值当酶活判据或成功概率；本文更没有任何功能测量，连结合都没有。
2. **本文阈值不可移植**：`E-value < 0.1`、`--qsc 0.8`、`--diff 3000`、`pLDDT ≥ 85`、`>30% identity / 90% coverage` 全部是为"MSA 够不够建结构模型"服务的搜索/内存参数，不携带任何功能含义；把它们写进我们的活性漏斗等于引入无根据的先验。
3. **吞吐数字不能当我们的可行性证据**：268 aa 均长、剔除 >1,000 残基、无模板、带早停的细菌蛋白组，与"几百到几千条含跨膜/多结构域设计候选 + 需要构象采样"的工作负载不同；引用时只能引用**量级与方法**，不许把 1,000/天当我们的产能承诺。
4. **本文不做设计、不做序列生成、不做候选排序**，所以它在方法演进链上的位置是"成本前提"而不是"判据来源"：它使 B09 那类"把 AF2 当闸口"的漏斗算得起，但不能为任何闸口的**判别力**背书。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K28_PMC9184281_text.txt

- 本地纯文本：`fulltext/K28_PMC9184281_text.txt`（由 `fulltext/K28_PMC9184281_fullTextXML.xml` 去标签、实体解码得到；Springer 版式使正文含 `\documentclass` 等 LaTeX 残渣与夹在句中的引文编号，凡遇此处的原句本卡一律拆成不跨编号的两段引用）。
- 同一篇论文本目录另有 XML 原件一份；本卡只声明并按 `_text.txt` 那份逐字核对（两份抽取版本的引用编号位置不同）。
- 对照底稿行号：`sources/cost-benchmarks.md:64`（该行已注明"1000/day 是论文原句；单结构秒数为推算"——本卡的 86 GPU·s/结构仅按 24 h 折算，同样属推算，未当原文引用）。
- CSV 字段映射：第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only K28 --no-report` 把卡内所有不含中日韩字符、被直双引号包住且 ≥20 字符 / ≥12 个字母的片段，在声明的底稿里做逐字查找。本卡引句全部为从 `_text.txt` 复制粘贴的原句；已按硬规则避开三类坑：不跨句中引文编号（原文 `on the ClusPro 4 , 12 dataset` 与 `17 ClusPro 4 , 12 targets` 两处都夹着引文编号，本卡对应引句停在编号之前："matches AlphaFold-multimer on the ClusPro" 与 "We compare predictions of 17 ClusPro"）、不用省略号结尾、参数与状态名不加英文双引号（`--qsc 0.8` 一类一律用反引号）。原文笔误 "209,335,865 million" 按原样引用并在第 7.3 条注明，不做"顺手改正"。

<!--CSV回填
work_type=方法学论文（Nature Methods Brief Communication；加速与精度基准，非设计研究）
target=非设计对象：CASP14 65 靶/91 域（含 20 个自由建模靶/28 域）、ClusPro 17 个复合物靶、M. jannaschii 蛋白组 1,762 条（均长 268 aa）；输入为任意单体或同/异源复合物序列
backbone_generation=不生成设计骨架；候选序列由用户以 FASTA/A3M/CSV 输入，本文负责 MMseqs2 建 MSA + AlphaFold2 或 RoseTTAFold（可 PyRosetta 折叠协议、SCWRL4 侧链、AMBER 力场弛豫）做结构推断，并提供 notebook/命令行/本地版三种交付
computational_filters=搜索命中 E-value；三级多样性过滤（95% identity 去冗、qsc、identity 分桶截断）；模板按 E-value 取 top 20 后再 HHsearch；复合物按物种配对 MSA；输出排序单体用 pLDDT、复合物用 pTM/iPTM/inter-PAE；评价口径为 TM-score（TMalign）与 DockQ
thresholds=E-value<0.1；--max-seq-id 0.95；--qsc 0.8（且仅当命中≥100 时启用）；--diff 3000、六个 identity 桶各留 3,000 条、桶内<1,000 命中不过滤；模型输入截 512 cluster centers + 1,024 条附加序列；库归簇 >30% identity + ≥90% 覆盖、每簇留 10 条最多样；模板 top 20；复合物配对覆盖≥50%；residue index 偏移>32；recycle 默认 3（基准另跑 12）；早停 pLDDT≥85 或 (interface)pTM 达阈；批量 padding 10%
md_used=否（仅可选 AMBER 力场结构弛豫做能量最小化，无 MD 采样、无轨迹或自由能分析）
qm_used=否
experimental_methods=无湿实验；全部为计算结构与既有实验结构比对：CASP14 用 TMalign 算 TM-score、复合物 ClusPro 用 DockQ、计时为 MSA 生成与模型推断分开测（MSA 重复 5 次取均值；AF2 限单核以求"公平"）；另有一例辅助 120 MDa 人核孔复合体冷冻电镜结构解析（引用他人工作）
pipeline_counts=MSA 侧：UniRef30 共识序列 29.3M（替代全量 UniRef100 277.5M）→ 三次迭代 + 簇扩张 → 两个 A3M → 分桶截到每桶 3,000 → 模型输入 512+1,024；库侧：2.5 billion → 513 million（BFD/MGnify）、ColabFoldDB 约 2.09 亿代表序列 + 7.39 亿成员（原文规模句有笔误）；蛋白组侧：1,787 → 剔除 25 条 >1,000 残基 → 1,762 条；基准侧：CASP14 65 靶/91 域（FM 20 靶/28 域）、ClusPro 17 靶、抽样 50 条
hit_rate=未记录（本文无设计或湿实验命中；可比的只有精度追平：FM 靶平均 TM-score ColabFold-AF2 0.826 / ColabFoldDB 0.818 vs AF2 0.79、AlphaFold-Colab 0.744、CF-RoseTTAFold 0.62；全集 0.887/0.886 对 AF2 0.888；T1084 关组成分过滤后 0.457→0.872；recycle=12 全集 0.898）
best_metric=无 Kd/活性类指标（本文不测结合或催化）；结构质量口径最优为 CASP14 全集平均 TM-score 0.887（带模板的 AF2 参照 0.888）、recycle=12 时 0.898
cost_or_stat_note=搜索加速 40–60 倍、批量约 90 倍、单条整体约 5 倍；单 GPU 服务器接近 1,000 结构/天（摘要口径，24 h 折算约 86 GPU·s/结构属本报告推算）；早停相对默认 3.7 倍、相对每次重编译 4.8 倍；只编译一个模型省 7 min（开模板省 5 min）；数据库内存需求 ~517 GB → 84 GB；蛋白组实测：搜索 113 min（EPYC 7402P 24 核 / 512 GB RAM，MMseqs2 峰值 RSS 308 GB）、推理 46 h（单张 Titan RTX 24 GB，无模板，正文合称 48 h）；早停后 pLDDT 代价 90.68→89.33（50 条抽样）与 89.75→88.77（全蛋白组），但该项以模型自评分度量、无独立 TM-score 验证
role_in_timeline=位于 de novo 设计漏斗大规模使用 AF2 之前的成本解锁环节：把 AF2/ColabFold 从"几小时 + 2 TB + 大显存"降到单卡日千条，使 B09（pAE_interaction 界面闸口）这类"给几百万设计各跑一次 AF2"的方案在预算上成为可能；它不贡献任何判别判据，只贡献可行性与吞吐口径
source_pointer=data/literature_cards/fulltext/K28_PMC9184281_text.txt（SHA 458432022ef0508d…）+ 同目录 K28_PMC9184281_fullTextXML.xml（SHA daf0a6d49ddf394f…）；sources/cost-benchmarks.md:64
CSV回填-->
