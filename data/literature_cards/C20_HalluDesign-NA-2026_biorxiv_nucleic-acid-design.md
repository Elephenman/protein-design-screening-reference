# [C20] HalluDesign-NA——把曹组自己的"结构幻觉迭代"回路从蛋白搬到核酸：目前只有置信度自涨，零湿实验闭环

Fang Minchao（方敏超）, Wang Zhe, Cao Longxing（曹龙兴，末位通讯）
西湖大学生命科学学院（Gene Expression 国家重点实验室）+ 西湖实验室 AI 药物设计核心实验室 · bioRxiv 预印本 2026.06.10.730767（Posted June 11, 2026，**未经同行评审**）· DOI 10.64898/2026.06.10.730767 · EPMC 题录号 PPR1251738（无 PMID、无 PMC 号）
代码 https://github.com/MinchaoFang/HalluDesign_NA 与前作 https://github.com/MinchaoFang/HalluDesign · 通讯邮箱见正文页 caolongxing{at}westlake.edu.cn

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 第 77 行，编号 **C20**（组：曹龙兴组） |
| 文献类型 / 版本 | **bioRxiv 预印本 v1**，manuscript ID 2026.06.10.730767，正文页自记 Posted June 11, 2026；DOI 已 Crossref 核验（CSV 第 23 列 `✅Crossref核验`）。作者仅 3 人（Fang M, Wang Z, Cao L），是一篇**短文**，不是完整论文体量 |
| **预印本口径风险（引用前必读）** | 本文的**全部评测口径都是作者自述**：所谓 benchmark 指 in silico 基准，指标是模型自带的置信度（pLDDT、pTM，摘要另写 ipTM），**从未经过同行评议，也没有任何独立复现或第三方审计**。因此本卡第 3 节的判据栏、第 4 节的分数与第 5 节的结论，**只描述这篇稿子声称了什么**，不构成任何方法有效性的证据；正式发表与否**本地不可知（是否见刊未知）**，本卡不做判断，也不引用任何本地不存在的评审版本 |
| 本卡与正式发表版的关系 | **本地不存在任何正式发表版**：CSV 的 venue 列写 `预印本`，`other_ids` 只有 EPMC 题录号 `PPR1251738`，**无 PMID、无 PMC 号**。按本次作业纪律未做任何网络核查，所以本卡**不断言**这篇有没有被期刊接收；只把结论钉在预印本口径上——**本卡全部数字与判据来自 bioRxiv v1 正文+图注，若正式发表版补上 Methods 或湿实验，第 3、4、7 节必须回改**（前作 C19 同样是预印本且本地亦无评审版本，见 `C19_HalluDesign-iterative-hallucination.md` §0） |
| 本文取回方式 | Europe PMC `fullTextXML`（`PPR1251738`）**两次 HTTP 500**（`fetch_log.tsv` 第 16、85 行），第 3 次回退到 bioRxiv 正文页 HTML 成功（`fetch_log.tsv` 第 135 行：`channel=epmc_fulltext · http=500 · bytes=90,586 · sha16=d38c8b84c20cd3be · OK · note=fallback_ok[biorxiv_full] via https://www.biorxiv.org/content/10.64898/2026.06.10.730767v1.full`） |
| 本地全文（本次抓取，2026-10-20 12:24） | 原始 `fulltext/C20_PPR1251738_fullTextXML.xml`（磁盘 90,677 B，实为 bioRxiv HTML，SHA-256 `d38c8b84c20cd3be…`，与 fetch_log 记录的字节数差 91 B，为响应体与落盘换行差异，SHA 一致）→ 去标签纯文本 `fulltext/C20_PPR1251738_text.txt`（**15,950 B，单行**，SHA-256 `63a03553da337e17…`）。**本卡引句只对照这份纯文本**（登记见 `sources_map.json`） |
| 身份复核 | 纯文本开头实搜到标题 HalluDesign-NA: Extending HalluDesign for De Novo Nucleic Acid Design、作者序列 Minchao Fang → Zhe Wang → Longxing Cao、`doi: https://doi.org/10.64898/2026.06.10.730767`，与 CSV 行一致，未挂错行 |
| 全文实际含什么 | Abstract / Background / HalluDesign-NA Framework / Computational Design of DNA and RNA structures / Computational Design of protein binding DNA aptamers / Discussion / Conclusion / Code availability / 19 条参考文献 + 站点页脚（下载、邮件分享、引文管理器、学科分类）。**没有 Methods 章节**（本目录里 `Methods` 的命中全部在期刊名 Nature Methods 与 URL 编码串里），**没有任何表格**，**没有任何图本体**（只有 Fig. 1–4 图注文字） |
| 证据级别 | **全文级（仅正文 + 图注）**：本卡全部引句可在本地纯文本逐字命中（见第 9 节）。但这份全文**不含实验协议、不含筛选规则、不含任何设计条数**，所以第 3 节大量判据栏只能写 原文未给阈值，第 4 节台账只有长度与最好 pLDDT 一类数字 |
| 与登记底稿（`sources/cao.md:322–331`）的分歧 | ① 底稿与 CSV 把计算筛选器记为 置信度分数改进（pLDDT、ipTM）——本地全文里 **ipTM 只出现 1 次且只在摘要**，正文结果句用的是 **pLDDT 与 pTM**（本卡 grep 实测：pLDDT 4 次、ipTM 1 次、pTM 作为独立词 1 次；按子串计 pTM 会得 2 次，因为 ipTM 这个词里含 pTM。计数是本卡实测，非原文表述），全文**没有任何 pTM 或 ipTM 的数值**。② 底稿记 仅计算基准，摘要未声称湿实验闭环，与正文一致，采纳。③ 底稿记 约束含长度、对称性、与蛋白结构上下文，三者在正文/图注均逐句可核，采纳。④ CSV 第 21 列 `证据级别` 仍写 **摘要级**，是全文取回前的旧口径；本卡按实际持有的本地全文记为 全文级（仅正文+图注），不改 CSV |
| 未取到的部分 | 迭代轮数与每轮序列采样数、停止条件、任何准入阈值、Protenix 与 AF3 两个引擎的定量对比、pTM/ipTM 绝对值、生成设计总数、送测清单、全部湿实验。凡引用这些处本卡明写 原文未给阈值 或 原文未记录，不猜 |

## 1. 这篇到底解决什么（大白话）

一句话：**把曹组前作 HalluDesign（C19）那个"让结构预测模型自己幻觉出更自信的结构、再用 MPNN 回填序列、如此循环"的回路，把其中的蛋白序列模块换成核酸序列模块（NA-MPNN），从而在 DNA/RNA 上跑同一套迭代协同优化。**

背景是他们自己承认的落差：AlphaFold3 一类模型已经能把核酸与蛋白-核酸复合物算到原子级，但 "However, the de novo design of structured and functional nucleic acids remains a significant challenge."，并且 "the de novo design of functional nucleic acids remains far behind that of functional proteins, which can now be designed to target a diverse range of functionalities."——现有功能核酸（尤其适配体）几乎全靠 SELEX 这类高通量筛选拿，而不是设计出来的。

本文的做法与结论范围：框架侧 "This new framework, HalluDesign-NA, enables iterative sequence-structure co-optimization, facilitating the de novo design of nucleic acids."，具体只换了一个零件——用 NA-MPNN 更新核酸序列、替代原来的 ProteinMPNN/LigandMPNN，其余不动；起手段用随机序列初始化；在 Protenix 与 AF3 两个底座上都做了实现。任务侧覆盖三类：ssDNA/ssRNA 单体（含长链与对称二聚体）、以及靶向 IL-6 的 DNA 适配体（设计时蛋白靶固定）。

**它交出的"结果"只有一件事**：迭代过程中模型自己的置信度分数（pLDDT、pTM；摘要另写 ipTM）持续上升，加上"能设计出 200–300 nt、能设计对称二聚体、设计出的结合位点和已知晶体结构的位点大体重合"这几条定性观察。整篇**没有任何湿实验**，作者在正文里把这一点写得很直白——选取哪个计算指标去送实验、以及实验本身，都还在 exploring（原句见第 2.1、第 3 节）。因此这篇在方法演进链上的价值不在结论强度，而在**它是幻觉迭代式漏斗走到完全脱离实验验证的那一步的记录**。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **主难点：整条路线没有实验闭环，而且连送实验该用哪个计算指标都还没定下来**。
   现象/证据：引言直陈核酸生成模型的现状是 "the de novo design of functional nucleic aptamers capable of interacting with other molecules using these generative models remains challenging, and, to date, no experimental validation has been reported."；适配体那节结尾他们自己把两件未完成的事并列写出——"We are exploring optimal computational metrics for selecting designs for experimental characterization, as well as experimentally characterizing the designed aptamers, with the goal of advancing the structural-level design of functional nucleic acids."；Discussion 开头再把话说死："De novo design of functional nucleic acids or aptamers in low-throughput scenarios remains far from routine."，并承认 "Although our in silico benchmark demonstrates its potential, several obstacles must still be overcome to ensure experimental success."
   **他们做了什么**：把交付物明确降格为 in-silico 基准（原话 "Our in silico benchmark results show that HalluDesign-NA can generate nucleic acids with high-confidence metrics, providing researchers with promising starting points for experimental validation."），即先证明回路能在核酸上跑通、指标能往上推，再谈筛选与送测；选实验设计的那道闸口刻意**留空不写**。
   **代价**：这篇不提供任何命中率、不提供任何结合数据，也没有可复现的准入阈值；本文未解决（作者自己把它列为 future work）。对我们而言它是"漏斗判据未定"状态的一手样本，而不是"漏斗判据已定"的证据。

2. **数据难点：可作为训练/校验底子的核酸结构（尤其核酸-蛋白复合物）太少**。
   现象/证据："One major challenge is the limited availability of resolved nucleic acid-protein complexes, or even isolated nucleic acid structures, especially when compared to the vast number of protein structures available in the PDB"；前一句还给出替代来源的局限——"While current aptamer selection methods support efficient, high-throughput sequence identification, the majority of experimental results remain sequence-based"。
   **他们做了什么**：不去补数据、也不微调模型，只走免训练的前向回路（框架侧只有两处改动：序列模块换成 NA-MPNN，"The rest of the framework remains unchanged"），并把外部结构校验压缩到**一个已知晶体结构**做定性对照："Notably, the designed binding site mostly overlaps with the aptamer binding site identified in the crystal structure (PDB ID: 4NI7)."
   **代价**：唯一的结构层外部证据是 1 例、且口径是 mostly overlaps 这种定性词，全文**没有界面 RMSD、没有接触残基一致率、没有第二个靶点**；数据稀缺这条他们承认了但没有应对，本文未解决。

3. **表征难点：序列层学到的东西迁移不到结构层**（这是他们选结构路线的理由，也是自认的短板）。
   现象/证据："Sequence models can learn sequence-level representations, yet reliably transferring these features to the structural domain-particularly for design-remains difficult."
   **他们做了什么**：干脆绕开"序列模型直接生成功能核酸"这条既有路线（他们对既有(sequence-based)路线的定性是 "While several promising sequence-based methods have been developed for generating functional aptamers"，并另指出 "Nevertheless, researchers are increasingly exploring the potential for de novo functional nucleic acid design in low-throughput settings."），改成以结构预测模型为回路核心：结构由 AF3/Protenix 的幻觉更新，NA-MPNN 只负责在给定骨架上回填序列（"we explored whether NA-MPNN could replace the protein sequence design ProteinMPNN/LigandMPNN module in HalluDesign"）。
   **代价**：结构对不对仍只由同一个模型的自信度说话（见第 7 节循环论证问题）；且没有任何一条功能读数能判定这次迁移到底成不成。

4. **条件难点：核酸结构对缓冲液、温度、离子强度极敏感，而数据集不记录这些参数**。
   现象/证据："Moreover, the secondary and tertiary structures of nucleic acids are highly sensitive to environmental factors such as temperature, buffer composition, and ionic strength"，具体到操作层面是 "Variations in cooling rate (rapid versus slow) and subtle changes in solution conditions can significantly alter experimental structural outcomes, which may diverge from those found in physiological environments."，而可复现性的根因是 "Unfortunately, many existing datasets do not provide detailed documentation of these experimental parameters, further complicating the reproducibility and reliability of structure prediction and de novo design-especially in the context of limited training data."
   **他们做了什么**：**本地全文里没有任何应对**——设计回路中没有出现温度/离子强度/退火程序作为输入或条件，评估侧也没有把环境条件写进指标。作者只是把它作为 Discussion 的坦白列出。
   **代价**：本文未解决。这一条对迁移最要命：核酸侧"预测结构 = 某一实验条件下的结构"这个等式本身不成立，所以拿 pLDDT 当成功判据在核酸上比在蛋白上更弱。

5. **工程难点：对称约束与长链怎么在回路里实现、以及底座（Protenix 还是 AF3）怎么选**。
   现象/证据：对称性他们不改进结构模型，而是下移给序列模块："For symmetric design, by incorporating NA-MPNN symmetry sequence constraints during sequence design, HalluDesign-NA is able to generate symmetric structures."，并给出结果口径 "the symmetric dimer designs achieve a pLDDT score of up to 80"；长链的口径是 "This approach supports the design of nucleic acid monomers with lengths exceeding 300 nucleotides, with some monomers achieving pLDDT scores of up to 80"；底座问题他们不裁决，两套都做："We develop HalluDesign-NA implementions on both the foundation model Protenix and AF3."（原文 implementions 拼写如此），适配体段同样写 "Similarly, the AF3-style model Protenix and AF3 both can be served as the foundational structure prediction model, and nucleic acid sequences were randomly initialized to generate the initial design models."，图 2 图注也把两条并列为 from scratch 基准。起手段统一用随机序列："And during the design process, we use random sequence initialization to generate the starting sequences for both DNA and RNA design."
   **代价**：对称二聚的"对称性偏差"没有量化（无 C2 对称 RMSD、无对称违反数）；>300 nt 只报"支持"与个别 pLDDT up to 80，没有收敛轮数与成功率；两个底座的定量对比在本地全文里是空的（图 2 有曲线，但图本体与数值缺失）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及本文实际改了什么）

- **回路骨架**：完全继承前作 HalluDesign（C19）——结构侧靠 AF3 式扩散模块的幻觉效应做结构更新，序列侧用 MPNN 回填，两轮交替迭代。本文的原话是 "By integrating a sequence design module, such as LigandMPNN or ProteinMPNN"（接结构预测模型即为 HalluDesign），并且 "The rest of the framework remains unchanged"。
- **唯一被替换的零件**：核酸序列设计模型 **NA-MPNN**（"we explored whether NA-MPNN could replace the protein sequence design ProteinMPNN/LigandMPNN module in HalluDesign"），并支持对称序列约束。
- **底座（结构预测/幻觉引擎）**：AF3 与其开源复刻 **Protenix** 两套实现（"We develop HalluDesign-NA implementions on both the foundation model Protenix and AF3."）。
- **起点**：随机序列初始化，DNA 与 RNA 都这么做（"And during the design process, we use random sequence initialization to generate the starting sequences for both DNA and RNA design."）。
- **评估**：只有模型自带置信度（正文用 pLDDT、pTM；摘要另列 ipTM），加一处与晶体结构位点的定性重叠对照。**没有任何实验读数**。
- **本文没有用的方法**：MD、QM、Rosetta/物理能量、SELEX 或任何展示/亲和力实验、任何外部排序器（前作 C19 的 CoDP 在本文正文没有出现）。本地全文对这些关键词均无自述段落。

### 工作流程（按本文三个任务并列展开；判据栏里 原文未给阈值 表示全文确实没有数字）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 单体设计 | 指定长度的随机核酸序列（ssDNA 与 ssRNA），底座为 Protenix 或 AF3 | HalluDesign 式迭代：NA-MPNN 出序列 → 结构模型幻觉更新结构 → 再出序列，循环 | **原文未给阈值**（无停止条件、无轮数、无准入分数）；作者只给方向性描述 "Starting from randomly initialized sequences, HalluDesign-NA consistently improved computational metrics of the nucleic acid structures, including pLDDT and pTM." | 正文句称探索长度为 50–80 nt（"We first used HalluDesign-NA to design single-stranded DNA (ssDNA) and RNA (ssRNA) monomers, exploring sequence lengths ranging from 50 to 80 nucleotides"）；图 3A 图注则写 "Designs of short ssDNA and ssRNA with lengths of 30-60 nucleotides."；**设计条数原文未记录** |
| W2 单体结果检查 | W1 的最终模型 | 目视/统计检查碱基配对模式与紧凑度 | 原文未给阈值（无 RMSD、无与已知结构的定量比较，仅 "The final designs displayed a variety of base pairing patterns and compact structures"） | 图 3A 短链（30–60 nt）若干，拓扑多样；无条数 |
| W3 长链外推 | 更长长度的随机序列 | 同一回路直接拉长 | 原文未给阈值；报告的最好分数即 "This approach supports the design of nucleic acid monomers with lengths exceeding 300 nucleotides, with some monomers achieving pLDDT scores of up to 80" | 图 3B 为 "Designs of long ssDNA and ssRNA with lengths of 200-300 nucleotides."；最好 pLDDT ~80（some monomers，非全部） |
| W4 对称结构 | 对称二聚体目标 + **NA-MPNN 的对称序列约束** | 把对称性作为序列生成约束下移给 NA-MPNN，结构侧不改 | 原文未给阈值；结果口径 "For symmetric design, by incorporating NA-MPNN symmetry sequence constraints during sequence design, HalluDesign-NA is able to generate symmetric structures."，分数 "the symmetric dimer designs achieve a pLDDT score of up to 80" | 图 3C "Symmetric DNA dimer design with a length of 150 nucleotides."；单链长 150 nt 的二聚体 |
| W5 适配体（蛋白结合）设计 | **IL-6 蛋白靶结构固定**（图 1 图注："During aptamer design, the protein target is kept fixed."）+ 随机初始化核酸序列 | 同一回路迭代，蛋白序列冻结，只优化核酸；底座仍是 Protenix 或 AF3 | 计算侧 原文未给阈值，只有趋势句 "HalluDesign-NA consistently optimized computational metrics over iterative design cycles, with the protein sequence held fixed in ssDNA aptamer design"；**结构侧唯一判据是定性对照**："Notably, the designed binding site mostly overlaps with the aptamer binding site identified in the crystal structure (PDB ID: 4NI7)."（无重叠率数字） | "We next applied HalluDesign-NA to design DNA aptamers targeting IL6, exploring aptamer lengths ranging from 30 to 60 nucleotides"；图 4 图注给长度口径 "HalluDesign-NA generates diverse topologies of IL-6-targeting aptamers with lengths of 30-60 nucleotides."；设计条数原文未记录 |
| W6 送测与实验 | W1–W5 的计算设计 | **本文没有这一步** | 选设计用的计算指标尚未确定，作者原话："We are exploring optimal computational metrics for selecting designs for experimental characterization, as well as experimentally characterizing the designed aptamers, with the goal of advancing the structural-level design of functional nucleic acids." | 实验送测数 = 0；无任何结合/活性数据 |
| W7 与底座相关的成本记录 | — | — | — | 全文无算力成本数字（无 GPU-h、无每设计秒数、无吞吐）；无代码级参数（超参在 GitHub 仓库，本地不可得） |

**这张表读法要点**：七步里只有 W1–W5 是真做过的计算动作，而 W1–W5 的**判据栏全部是 原文未给阈值**；本文所有出现的定量口径只有两类——设计长度（nt）与最好的 pLDDT（up to 80）。W6 空缺就是这篇的核心信息：**没有闸口定义，就没有漏斗**。

## 4. 关键数字台账（数值 · 含义 · 出处；全部来自本地全文，第 9 节逐条命中）

先说清这份全文的数字密度：正文+图注里**能落到数值的东西只有两类**——设计长度（nt）和最好的 pLDDT（up to 80）。轮数、序列采样数、停止条件、准入阈值、设计总条数、送测数、界面 RMSD、亲和力、算力成本，**一个都没有**。所以本表的"数值"列里出现 0 与 grep 实测计数是正常的，那不是原文给的数，是**本卡对原文缺失的量化**（凡此均标注"本卡 grep 实测，非原文表述"）。

| 数值 | 含义 | 出处（原句片段 / 定位） |
|---|---|---|
| 50–80 nt | 正文口径的 ssDNA/ssRNA 单体探索长度 | "We first used HalluDesign-NA to design single-stranded DNA (ssDNA) and RNA (ssRNA) monomers, exploring sequence lengths ranging from 50 to 80 nucleotides" |
| 30–60 nt | 图 3A 图注口径的**短链**长度（与正文 50–80 不一致，见第 7 节） | "Designs of short ssDNA and ssRNA with lengths of 30-60 nucleotides." |
| 200–300 nt | 图 3B 图注口径的**长链**长度（正文写的是"超过 300"） | "Designs of long ssDNA and ssRNA with lengths of 200-300 nucleotides." |
| >300 nt | 正文声称可支持的最长单体 | "This approach supports the design of nucleic acid monomers with lengths exceeding 300 nucleotides" |
| up to 80（pLDDT） | 长链单体的最好置信度分数，口径是 some monomers 而非全体 | "with some monomers achieving pLDDT scores of up to 80" |
| up to 80（pLDDT） | 对称二聚体的最好置信度分数 | "the symmetric dimer designs achieve a pLDDT score of up to 80" |
| 150 nt | 图 3C 对称 DNA 二聚体（单条链长） | "Symmetric DNA dimer design with a length of 150 nucleotides." |
| 30–60 nt | IL-6 DNA 适配体的探索长度（正文与图 4 图注两处一致） | "We next applied HalluDesign-NA to design DNA aptamers targeting IL6, exploring aptamer lengths ranging from 30 to 60 nucleotides"；"HalluDesign-NA generates diverse topologies of IL-6-targeting aptamers with lengths of 30-60 nucleotides." |
| 1 个蛋白靶 | 适配体任务只有 IL-6，且设计时蛋白被冻结 | "During aptamer design, the protein target is kept fixed." |
| 1 处外部结构校验 | 全文唯一的非自评分数证据，且是定性词 | "Notably, the designed binding site mostly overlaps with the aptamer binding site identified in the crystal structure (PDB ID: 4NI7)." |
| 2 个底座 | Protenix 与 AF3 两套实现并列，无定量对比 | "We develop HalluDesign-NA implementions on both the foundation model Protenix and AF3."（原文 implementions 拼写如此） |
| 1 个被替换的零件 | 相对前作 HalluDesign（C19）只换序列模块 | "HalluDesign-NA employs NA-MPNN ( 15 ) to update nucleic acid sequences, replacing the original protein sequence design model"；"The rest of the framework remains unchanged" |
| pLDDT 4 次 / pTM 独立 1 次 / ipTM 1 次 | 正文结果句用 pLDDT+pTM，摘要写 pLDDT+ipTM（**摘要与正文指标名不一致**） | "Starting from randomly initialized sequences, HalluDesign-NA consistently improved computational metrics of the nucleic acid structures, including pLDDT and pTM."；摘要句 "consistent improvements in confidence scores (pLDDT, ipTM)"。计数为本卡 grep 实测（pTM 按子串计为 2，因 ipTM 含 pTM），非原文表述 |
| 0 | 全文出现的绝对阈值得分（无 pTM/ipTM 数值、无 RMSD、无 Kd、无命中率） | RMSD 与 Kd 在本地全文出现 0 次（本卡 grep 实测，非原文表述） |
| 0 | 湿实验数 / 送测清单 / 设计总条数 | 原文未记录；作者只在 Discussion/Conclusion 层面承认待做："We are exploring optimal computational metrics for selecting designs for experimental characterization, as well as experimentally characterizing the designed aptamers" |
| 0 | 迭代轮数、每轮采样数、停止条件 | 原文未记录（无 Methods 章节） |
| 0 | 算力成本（GPU-秒、CPU-秒、吞吐、单价） | 原文未记录；GPU 一词在本地全文出现 0 次（本卡 grep 实测，非原文表述） |
| 3 次 / 0 章 | Methods 这个词只出现在期刊名 Nature Methods（参考文献 7/14/18），正文**没有 Methods 章节** | 本卡 grep 实测，非原文表述；见第 0 节 全文实际含什么 行 |
| Fig. 1–4，4 条图注 | 只有图注文字存活，图本体与图中数值不在本地全文里 | "Fig. 1. Overview of the HalluDesign-NA framework." 等 4 条；图注与正文之间夹有 "Download figure Open in new tab" 站点噪声 |
| 19 条参考文献 | 体量证据：这是短文（3 位作者、无 Methods、无表格、图仅图注） | References and Notes 编号 1.–19.（末条为 Tinoco 与 Bustamante, How RNA folds） |
| 15,950 B / 15,914 字符（归一化后） | 本地纯文本体量 | 见第 0 节；SHA-256 `63a03553da337e17…` |

## 5. 结论——作者说了什么（只列作者自述，逐条可在本地全文命中）

1. **框架层面**：把前作 HalluDesign 的序列模块换成 NA-MPNN 就得到核酸版，其余不动；在 Protenix 与 AF3 两个底座上都做了实现；起点一律随机序列初始化。原话："This new framework, HalluDesign-NA, enables iterative sequence-structure co-optimization, facilitating the de novo design of nucleic acids."
2. **评测层面（摘要口径）**：三类任务（ssDNA、ssRNA、适配体）上置信度分数**一致上升**，并声称这支持在长度、对称性、蛋白结构上下文三种约束下做 de novo 核酸设计的可行性——"Computational benchmarking across ssDNA, ssRNA, and aptamer design tasks demonstrates consistent improvements in confidence scores (pLDDT, ipTM), supporting the feasibility of de novo nucleic acid design under various constraints, such as sequence length, symmetry, and protein structure context."
3. **结构层面（正文口径）**：随机序列出发分数稳步上行 "Starting from randomly initialized sequences, HalluDesign-NA consistently improved computational metrics of the nucleic acid structures, including pLDDT and pTM."；最终设计呈现多样配对模式与紧凑结构 "The final designs displayed a variety of base pairing patterns and compact structures"。
4. **能力边界（作者的三个"能做到"）**：>300 nt 的单体（some monomers pLDDT up to 80）、对称二聚体（pLDDT up to 80，靠 NA-MPNN 对称序列约束）、IL-6 的 30–60 nt DNA 适配体；适配体设计的位点与晶体结构 4NI7 的位点"大体重合" "Notably, the designed binding site mostly overlaps with the aptamer binding site identified in the crystal structure (PDB ID: 4NI7)."
5. **作者对现状的定位**：功能核酸的 de novo 设计远落后于蛋白，且既有生成模型（RFpoly、Odesign 一类）做适配体"至今没有实验验证被报道" "However, the de novo design of functional nucleic aptamers capable of interacting with other molecules using these generative models remains challenging, and, to date, no experimental validation has been reported."
6. **作者自己划的交付边界**：本文只交付 in-silico 基准，且明确说送实验用的计算指标尚未选定、实验表征还在做 "We are exploring optimal computational metrics for selecting designs for experimental characterization, as well as experimentally characterizing the designed aptamers, with the goal of advancing the structural-level design of functional nucleic acids."；结论段把价值定位成"给实验提供有希望的起点" "Our in silico benchmark results show that HalluDesign-NA can generate nucleic acids with high-confidence metrics, providing researchers with promising starting points for experimental validation."
7. **作者承认的障碍**（Discussion 原文列出四条）：低通量场景下远未常态化 "De novo design of functional nucleic acids or aptamers in low-throughput scenarios remains far from routine."；in silico 有潜力但要跨过若干障碍才能确保实验成功 "Although our in silico benchmark demonstrates its potential, several obstacles must still be overcome to ensure experimental success."；核酸-蛋白复合物与孤立核酸结构数据稀缺；序列层表征难迁移到结构层；核酸结构对温度/缓冲/离子强度敏感而数据集不记录这些参数。
8. **展望**：作者预期该框架会加速功能核酸在诊断、药物开发与合成生物中的应用 "As HalluDesign-NA extends generative design to nucleic acids, we anticipate broad applications in molecular diagnostics, drug development, and synthetic biotechnology."
9. **代码**：作者声明全部源码在 GitHub（HalluDesign-NA 与 HalluDesign 两个仓库）。**但本地全文没有任何超参、轮数、阈值等可复现参数**，Code availability 只有两行链接。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的"结果"是同义反复**：回路优化的目标函数就是评价它的那个函数。NA-MPNN 出序列 → AF3/Protenix 打分 → 保留高分 → 再出序列，循环；于是"pLDDT 一致上升"是这套迭代的**定义级后果**，不是设计成功的证据。作者没有引入任何**独立于打分器**的证据（除 4NI7 那处定性对照），所以第 2 节里"该用哪个计算指标去送实验"这件事本文回答不了，只能用原文那句 exploring 把它挂为待做。**可迁移的教训**：任何"自评分数上升"曲线都不进我们的漏斗账，判据必须来自生成/打分之外的信息源。
2. **正文与图注的长度口径不一致（50–80 对 30–60、>300 对 200–300）**，最合理的解释（推断，原文未说明）是正文与图取的是不同批次或不同配置的设计。对我们读文献的直接含义：**一篇短文若正文与图注的样本口径不能对齐，它的任何"规模"数字都不能被登记为事实**，只能登记成两个互相冲突的读数——本卡就是这么做的（第 4 节把两套长度并列，不合并、不取中间值）。
3. **摘要写 ipTM、正文写 pTM，全文没有这两个数的任何值**（推断：摘要与正文由不同轮次的结果写出，或摘要用了未进正文的指标）。这意味着**连"改进的到底是哪个指标"都不确定**，登记底稿 `sources/cao.md` 与 CSV 把 pLDDT/ipTM 当作本文的"计算筛选判据"，其实是把**摘要的自述**当成了**方法的细节**。我们做二次引用时必须区分这两层。
4. **"约束可满足"被当成了"设计可用"**：长度、对称性、蛋白上下文是三个*生成时施加的约束*（对称性来自 NA-MPNN 的约束项，蛋白上下文来自冻结蛋白），本文证明的是回路**不违反约束**，没有证明约束下的产物有功能。我们的目标同样带硬约束（线性、5′-ppp、U-A-A 起始、Nₙ 链长、3′-OH），这条提醒是：**把候选写成满足约束的形态 ≠ 找到能催化它的酶**，两者之间隔着我们目前完全没有的量具。
5. **"in silico 复筛"与"湿实验命中"之间没有桥**，这篇是链条走到最左端就停住的样本：零送测、零结合数据。它给我们的反面标准是——任何我们在时间线上标注"候选已生成/已复筛"的行，都必须显式区分 计算通过 / 已下单 / 已被化学确认 三种状态，否则就会像本文一样只剩第一种状态却以"design success/feasibility"的语言叙述。
6. **核酸的环境敏感性这条坦白对我们比对蛋白更致命**（作者列出但没应对）。我们的配体是带电荷与化学端基的 RNA 短链（5′-三磷酸、3′-OH），其在溶液里的真实构象依赖离子强度与温度；**结构预测给出的"这个复合物长这样"本身就是一个条件依赖的陈述**。因此任何"用 AF3/Protenix 类模型判断我们那条寡核苷酸能不能被识别"的尝试，都应写为**假设生成**，不是判据。
7. **值得单独记录的一个正面事实**（推断）：他们在适配体段把蛋白靶冻结、只优化核酸，这与"给定底物/靶、只优化另一侧序列"的回路形态是同构的；这条路在**没有实验时也能跑**，所以它的产品是*一批可下单的候选*而非结论——恰好是我们一轮最多四个构建体的湿实验预算真正需要的东西。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自己写出来的**（详见第 5.7 条，四条全在 Discussion）：低通量场景下功能核酸 de novo 设计远未常态化；in silico 有潜力但要跨过若干障碍才谈得上实验成功；核酸结构数据稀缺；序列层表征迁移不到结构层；核酸二级/三级结构对温度、缓冲组成、离子强度敏感，而现有数据集不记录这些实验参数。以及一句最关键的自认——送测该用哪个计算指标还在探索、实验表征还没做（第 2.1 节原句）。

**我们读出的，按"能不能被下游引用"排序**：

1. **不可复现是结构性的**：本地全文**没有 Methods**（Methods 一词的 3 次命中全是期刊名 Nature Methods，本卡 grep 实测）。迭代轮数、每轮序列采样数、随机初始化怎么随机、NA-MPNN 用哪个版本/是否微调、停止条件、分数取哪种聚合（残基平均还是取最大值）——全都没有。Code availability 只有两行 GitHub 链接。→ 本卡第 3 节判据栏大量写 原文未给阈值，不是疏漏，是这篇的客观状态。
2. **"up to 80" 是极值口径，分母未报**：原文写 "with some monomers achieving pLDDT scores of up to 80"，some 是多少、总共有多少条、分布如何一概没有。→ 这是本项目清单里"极值当代表作/阈值凑池"这一类缺陷的又一个一手样本；引用时只许说"作者报了一个上界"，不许说"该方法能达到 pLDDT 80"。
3. **摘要与正文不咬合**：摘要把结论强度写在 "consistent improvements in confidence scores (pLDDT, ipTM)"，正文里 ipTM 一次都没出现，被换成了 pTM，而且两者都没有任何数值。→ 二次引用时若只看摘要，会以为本文有一个叫 ipTM 的闸口；实际没有。
4. **正文与图注的样本口径互相冲突**（50–80 对 30–60、exceeding 300 对 200–300）：全文没解释，无法判断是不同批次、不同配置还是笔误。→ 本卡第 4 节把两套数字并列登记，不合并。
5. **唯一的非自评证据是 1 例、且是定性词**：4NI7 的"mostly overlaps"没有重叠率、没有界面 RMSD、没有接触残基一致率、没有第二个靶点。RMSD 在本地全文出现 0 次。→ 本文不能为任何 RMSD 或界面重叠阈值提供先例。
6. **两个底座（Protenix 与 AF3）谁强没有答案**：图 2 名义上是这两个模型的 from scratch 基准（"Fig. 2. HalluDesign-NA benchmark on ssDNA monomer and ssRNA and ssDNA aptamer from scratch design using Protenix or AF3 model."），但**图本体与图中数值不在本地全文里**，正文也没有一句对比。→ 本卡不声明任何底座排序。
7. **对称性、长链两条都只有"能"没有"多能"**：无对称违反数、无 C2 对称 RMSD、无收敛所需轮数、无不同长度上的成功率曲线。150 nt 二聚体和 >300 nt 单体是**图注里的样例**，不是可统计的结果。
8. **他们批评别人的话适用于他们自己**：引言用 "to date, no experimental validation has been reported" 指出 RFpoly/Odesign 这类生成模型缺实验；本地全文里本文同样一个实验都没有——这句批评在本文的引用范围里不包括本文自己（作者显然知道，所以才把交付物写成 promising starting points for experimental validation）。
9. **抽取质量层面的两条**（属本地底稿状态，不代表原文）：① 本地纯文本是 bioRxiv 正文页 HTML 去标签的结果，混有 "Download figure Open in new tab"、引文管理器、学科分类计数等站点噪声，凡本卡引用处都已在引句里避开或原样保留；② 本地文本的第 9 条题录只有 "O. Zhang et al. ( 2025 )"、缺题名，无法判定是原文如此还是抽取丢失，故本卡不使用该条支撑任何论断。
10. **版本风险**：这是 v1 预印本，未见刊与否本地不可知；作者自述的评测口径从未经过同行评议。若正式发表版补上 Methods 或湿实验，本卡第 3、4、7 节必须回改。

## 8. 对 UAA 筛选的迁移判断

先写清**表面相似性在哪、本质差异在哪**，否则这一行很容易被误当成"支持我们用 AF3 类模型做 RNA 短链设计"的证据。

- 相似（表面）：本文的对象是核酸、约束里有链长与对称性、适配体段还冻结蛋白靶去设计能结合蛋白的 DNA；我们的目标配体是线性 5′-ppp-U-A-A-Nₙ-3′OH，也是核酸、也有链长变量 Nₙ、也要和蛋白（合成酶）发生识别。关键词层面两边高度重叠。
- 本质不同（三条，逐条都会决定能不能搬）：
  1. 本文设计的是**要折叠成特定二级/三级结构的核酸**，其成功口径是"结构自信度"；我们的目标寡核苷酸是**非折叠的线性底物**，其被识别与被延伸取决于**端基化学**（5′-三磷酸、3′-OH、U-A-A 起始顺序）而不是折叠形态。
  2. 本文的 NA-MPNN 做的是"给定骨架反推序列"，输出是核酸序列；我们要的是**蛋白/酶一侧**能否催化三步化学事件（S0 游离 UTP 起始、S1 生成 pppUA、S2 加第二枚 ATP 而非环化）。方向相反。
  3. 全文对**化学端基**（triphosphate 桥接、3′-OH）一个字都没提，也没有说明 AF3/Protenix 能否把 5′-ppp 与 3′-OH 正确表达在输入/输出里。→ 迁移时端基是**未验证的空白**，不是可继承的能力。

**可迁移（怎么用）**

1. **"换序列模块、不动回路"的移植骨架**（本文唯一的方法学动作，第 5.1 条）。对我们：如果要把蛋白设计回路用于"识别一段寡核苷酸的表面"，正确的最小改动是把序列生成器换成适配该链的那一个，而回路、打分、迭代节奏沿用已审计过的版本——一次只动一个零件，并且把"只动了这一个"写成可核验的声明。这条是本卡认为这篇唯一值得抄的东西。
2. **"冻结一侧、只优化另一侧"的任务写法**（原文在适配体段的实现：蛋白靶固定，"During aptamer design, the protein target is kept fixed."）。对我们：造"底物/产物类似物固定 + 只改蛋白序列"的计算复筛任务时，这套接口形态可以直接借；但要清楚借的是**任务构造方式**，不是它的评价指标。
3. **把约束写成生成时的显式条件**（长度、对称性由 NA-MPNN 的对称序列约束实现，而非事后丢弃不合格品）。对我们：搜索/生成候选时把 线性、5′-ppp、U-A-A 起始、Nₙ 范围、3′-OH 作为**生成约束**写进协议，比事后过滤更可审计——因为事后过滤的分母我们同样报不出来，而本文正是连分母都没报的例子。
4. **"闸口未定"也要入账**（作者把送测指标选择列为待做，第 2.1 条）。对我们的用途：这是"该用哪个计算指标把候选送去化学确认"在 2026 年中仍是公开空白的**一手证据**，可以在方案里引用它来论证"我们的漏斗必须自己定义并冻结闸口"，但不能引用它给出任何闸口的具体数值。
5. **反面教材（本文对我们最大的价值）**：它完整演示了"自评回路 + 极值口径 + 零实验"如何被写成一篇有摘要、有四张图、有 feasibility 措辞的稿子。我们每一张卡/每一轮报告都要用它来对照自查：**分数上升有没有独立证据、有没有分母、状态词有没有越过 计算通过**。

**不可迁移（为什么不能照搬，逐条点名数字）**

1. **pLDDT up to 80 不是判据，也不是概率**。它是模型对自身输出的置信度、由被优化的同一个打分器给出、且是 some monomers 的上界（分母未报）。禁止出现在我们的准入阈值表里；禁止换算成"我们的候选有 X% 能被识别"。DP2R 判定标准 §2 已禁止把 binder 侧 pAE/ipTM 类置信度当酶活闸口，本文的 pLDDT/pTM/ipTM 同理且更弱（本文连一次实验校准都没有）。
2. **本文没有任何 RMSD 阈值可借**：全文 RMSD 出现 0 次（本卡 grep 实测）。4NI7 的重叠是 mostly overlaps 这种定性表述。→ 谁要把"界面 RMSD < X Å"挂到这篇名下，就是凭空造数；我们自己的结构一致性阈值只能来自我们自己审计过的参照系（例如 BcCdnD 三张晶体的实测几何），且已被证明会被失活背景反超时不许当正向判据。
3. **长度数字（30–80 / 150 / 200–300 nt）与我们的 Nₙ 没有对应关系**。它们说的是"这个回路能生成多长的折叠核酸"，不是"多长的底物能被酶接受"。我们 Nₙ 的可用范围由酶的过程性与起始机制决定，本文不能提供上界也不能提供下界。
4. **in silico 复筛结果绝不许当湿实验命中**。本文的实验命中数=0、送测清单=0，它的全部产出停在 计算通过 这一格。我们时间线上任何由这类回路产出的候选，状态字段最多写到 计算通过（或 已下单），**不允许**写"命中""得到结合体""验证可行"；命中率字段一律填 未记录（本文无实验）。
5. **核酸结构模型的输出本身条件依赖**（作者自述温度/缓冲/离子强度敏感、数据集不记录这些）。我们若要评估那条寡核苷酸的可及性，必须把溶液条件作为显式变量，否则"预测到的构象"和"我们反应体系里的构象"不是同一个东西——这条限制的是**我们能从结构层推断什么**，与本文的置信度数字无关，但正是本文替我们说清楚了的代价。
6. **不许把 SELEX/展示库式高通量当作我们的对照通量**：本文引用的既有路线靠高通量筛选拿功能核酸（"Currently, functional nucleic acids are primarily obtained through high-throughput screening approaches such as SELEX"），而它自己的路线是 low-throughput 设计。我们的产物化学确认一轮最多四个构建体，属于更低通量：漏斗末端目标是**信息量最大化**（机制多样性 + 失活对照 + 阴阳性同域），不是样本数最大化，也不存在能算 SC50/Kd 的库。
7. **禁止编造**：不得写"某法对 UAA 合成酶的成功率为 X%"，不得把 C19（蛋白侧 HalluDesign）的成果外推给核酸版，也不得把本文对 RFpoly/Odesign 的批评当作对本文自身有效性的替代证明。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/C20_PPR1251738_text.txt

- **本卡所有引句只对照这一份底稿**。同一编号在本地还有 `fulltext/C20_PPR1251738_fullTextXML.xml`（磁盘 90,677 B），但那实际是 bioRxiv 正文页 HTML 的原始响应（Europe PMC fullTextXML 通道两次 HTTP 500 后回退取回的，见第 0 节），**未登记为可比对底稿**，本卡不与之比对，避免 HTML 标签/实体差异造成的假红。
- 底稿生成方式：抓取脚本对原始响应做去标签 + `litcards_text.norm`（实体解码、弯引号/破折号归一、空白折叠），本卡照抄归一化后的实际字符，不做二次改写；原文拼写错误（implementions）、正文与图注的连字符长度写法（ranging from 50 to 80 nucleotides 对 lengths of 30-60 nucleotides）均按原样保留。
- 对照底稿：`sources/cao.md:322–331`（登记卡原段）；CSV 行 `data/protein_design_literature.csv` 编号 C20（第 77 行）。与本卡的分歧已在第 0 节最后一条列出（pLDDT/pTM 对 ipTM 的指标名冲突、CSV 证据级别仍为旧口径 摘要级），本卡不改 CSV、不改 `sources/*.md`。
- 时间线位置参照：前作 C19（HalluDesign 蛋白版，同为预印本）见 `C19_HalluDesign-iterative-hallucination.md`；本项目对曹组方法演进的整体判断见 `sources/cao.md:444`。
- CSV 字段映射：第 3 节 ↔ 候选生成方法 / 计算筛选判据 / 阈值数字；第 4 节 ↔ 候选数递减 / 实验命中率 / 成本统计；第 8 节 ↔ 在方法演进链的位置；第 0 节 ↔ 文献类型 / 证据级别 / 原文出处指针。
- **本卡自检**：`scripts/verify_literature_cards.py --only C20 --no-report`（输入：本目录 `*.md` + `fulltext/` + `sources_map.json` + `inventory.json`）。判据为：10 节齐全且标题含关键词、工作流程表 ≥3 步、难点 ≥2 条、14 键回填块无空值、§9 声明的底稿在该编号登记列表内、卡内每条被直双引号包住且不含中日韩字符的 ≥20 字符片段在该底稿里逐字命中。本轮结果见下方回报（PASS 与 quotes=n/n 由脚本打印，非本卡手写）。写作过程中一次中途自查（填完第 4 节后）为 63/63 命中、0 MISS；本卡未使用跨句拼接、未使用省略号截断、未把状态名加英文引号。**末轮实跑结果：PASS C20 quotes=80/80，退出码 0**（2026-10-21 本地跑，参数仅 `--only C20 --no-report`）。
- **一次真实的环境抖动（留账，非本卡问题）**：本卡首次复跑门禁时报 `证据级别造假：§0 声明全文级但没有本地全文`，原因是并行的抓取/身份体检进程在 11:48 重建了 `inventory.json`，那一版把 C20 的纯文本归到 `records` 而把 `has_fulltext` 记为 false；11:51 再次重建后恢复 `has_fulltext=true` 且 `local=[data/literature_cards/fulltext/C20_PPR1251738_text.txt]`，同一张卡同一命令随即 PASS。**本卡没有修改 `inventory.json`、`sources_map.json`、CSV 或任何脚本**，只在被抖动的那一次运行后确认了登记状态；若后续重建再次把本行降为无全文，则 §0 的证据级别与本卡第 3、4 节的写法需要按当时的登记状态重读，而不是自动当作成立。
- **反向自测口径**：本卡的数字（长度、pLDDT 上界、4NI7、grep 计数）全部可在底稿里用字符串搜索复现；凡本卡标注 本卡 grep 实测，非原文表述 的计数，都不属于原文主张，不得被下游当成论文结论引用。

<!--CSV回填
work_type=论文（bioRxiv 预印本 v1，2026-06-11 posted，未经同行评审；3 位作者的短文，本地全文无 Methods 章节、无表格、无图本体）
target=ssDNA 与 ssRNA 单体（含最长超过 300 nt 的长链与对称 DNA 二聚体）+ 靶向 IL-6 的 DNA 适配体（设计时蛋白靶冻结）
backbone_generation=HalluDesign（C19）迭代幻觉回路的核酸版：随机序列初始化 → NA-MPNN（可用对称序列约束）生成核酸序列 → Protenix 或 AF3 幻觉更新结构 → 交替迭代；相对前作只替换序列模块，其余不变
computational_filters=仅模型自带置信度：正文用 pLDDT 与 pTM、摘要另写 ipTM（三者全文均无数值）；另有 1 处与晶体结构 4NI7 结合位点的定性重叠对照；无外部排序器、无物理能量函数、无 MD、无 QM
thresholds=原文未给阈值（无迭代轮数、无停止条件、无准入分数、无界面判据）；全文仅有的数值口径是设计长度（正文 50-80 nt 与 exceeding 300 nt、图注 30-60 与 200-300 与 150 nt）和最好 pLDDT up to 80（some monomers 的上界，分母未报）
md_used=否（本地全文无 MD/分子动力学相关内容）
qm_used=否（本地全文无 QM/自由能相关内容）
experimental_methods=无。本文零湿实验、零送测清单；作者自述送测该用哪个计算指标仍在探索、实验表征仍待做（列为 future work）
pipeline_counts=原文未记录（设计总条数、每轮采样数、送测数全缺，原因：无 Methods 章节）；实验送测数=0；长度口径两套且冲突：单体正文 50-80 nt 对图 3A 30-60 nt，长链正文 exceeding 300 nt 对图 3B 200-300 nt，对称二聚体单链 150 nt，适配体 30-60 nt
hit_rate=未记录（本文无任何实验结果，命中率不存在；作者只声称置信度分数随迭代一致上升）
best_metric=未记录（无 Kd、无亲和力、无活性读数；全文最好的量化值只是 pLDDT up to 80，且是 some monomers 的上界）
cost_or_stat_note=原文未记录算力成本（GPU、CPU-秒、吞吐均无，GPU 一词在本地全文出现 0 次，本卡 grep 实测）；超参不在正文、仅在 GitHub 仓库；作者自述的 in silico 评测口径未经同行评议，独立复现暂不可行
role_in_timeline=曹组方法链 HalluDesign（C19，蛋白）→ HalluDesign-NA（本篇，核酸）：第一次把幻觉迭代式序列-结构协同回路完全脱离实验闭环地搬到核酸上，并演示了换序列模块即可跨域移植的骨架；在本项目时间线里它是 漏斗闸口未定 与 in silico≠湿实验 两个缺陷的一手样本，不是任何判据或命中率的来源
source_pointer=data/literature_cards/fulltext/C20_PPR1251738_text.txt（15,950 B，SHA-256 63a03553da337e17…）；原始响应 data/literature_cards/fulltext/C20_PPR1251738_fullTextXML.xml（实为 bioRxiv 正文页 HTML，SHA-256 d38c8b84c20cd3be…，取回日志 fetch_log.tsv 第 16/85/135 行）；登记底稿 sources/cao.md:322-331
CSV回填-->
