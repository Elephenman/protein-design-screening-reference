# [C19] HalluDesign（bioRxiv 预印本 v1）——把判定阈值前置进生成回路：先把自己推到闸门口，再每靶只投 16 个

Fang Minchao（方敏超）, Wang Chentong, Shi Jungang, Lian Fangbai, Jin Qihan, Wang Zhe, Zhang Yanzhe, Cui Zhanyuan, Wang YanJun, Ke Yitao, Han Qingzheng, **Cao Longxing（曹龙兴，末位通讯）**
西湖大学生命科学学院（Gene Expression 国家重点实验室）+ 西湖实验室 AI 药物设计核心实验室 · bioRxiv 2025.11.08.686881（v1，Posted 2025-11-09，预印本，**本地未见同行评审版本**）· DOI 10.1101/2025.11.08.686881 · EPMC 题录号 PPR1116408
正文页 https://www.biorxiv.org/content/10.1101/2025.11.08.686881v1 · 代码 https://github.com/MinchaoFang/HalluDesign 与 https://github.com/MinchaoFang/CoDP

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C19**（组：曹龙兴组） |
| **预印本版本/日期** | **bioRxiv v1**，Manuscript ID 2025.11.08.686881，本地正文页底部自记 Posted November 09, 2025（投稿日期 2025-11-08）；DOI 已在 Crossref 核验（`data/gate.json`：`status=OK`、`registry=Crossref`、标题重合度 1.0、年份 2025）。**这是未经同行评审、未经独立复现的预印本**；本库判据标准文件点过这篇，凡引用其命中率数字必须带预印本 / v1 版本标注（本卡所有数字口径同此） |
| 本文取回方式 | Europe PMC `fullTextXML`（`PPR1116408`）**两次返回 HTTP 500**，第 3 次回退到 bioRxiv 正文页 HTML 成功：`fetch_log.tsv` 第 134 行 `channel=epmc_fulltext · http=500 · bytes=235,602 · sha16=815e8ee604006ee7 · OK · note=fallback_ok[biorxiv_full] via https://www.biorxiv.org/content/10.1101/2025.11.08.686881v1.full` |
| 本地全文（本次抓取，2026-10-20 12:24） | 原始 `fulltext/C19_PPR1116408_fullTextXML.xml`（235,944 B，实为 bioRxiv HTML，SHA-256 `815e8ee604006ee7…`）→ 去标签纯文本 `fulltext/C19_PPR1116408_text.txt`（55,493 B，SHA-256 `1a68c94cc1b69271…`）。**本卡引句只对照这一份纯文本**（登记见 `sources_map.json`） |
| 身份复核 | 文件头 8,000 字符内实搜到标题 HalluDesign… 、作者序列 Minchao Fang → Longxing Cao、`doi: https://doi.org/10.1101/2025.11.08.686881`，与 CSV 行一致，未挂错行 |
| 对照底稿 | `sources/cao.md:305–320`（原卡）与汇总表 `sources/cao.md:420`、口径警示 `sources/cao.md:30`、`sources/cao.md:480`；本卡在其基础上补：三种配体初始化与 Fpocket 口袋定义、150/200/50 步的实际分工与 6-7 轮收敛、CoDP 排序器的训练口径、AF3 from-scratch 失败与换 Protenix 的因果、配体侧 5 例晶体结构与分辨率、ITC/BLI 各自的靶集合 |
| 证据级别 | **全文级（仅正文 + 图注）**：本卡全部引句可在本地纯文本逐字命中（见第 9 节）。**但本地这份抽取不含 Methods 章节**——正文止于 Conclusions / Code Availability，`Method` 一词的 4 次命中全在参考文献期刊名里；也**没有任何表格**（`Table` 出现 0 次）。因此实验协议参数（表达载体、BLI/ITC 缓冲液与浓度梯度、送测清单的选取规则、生成库规模）本地不可得，本卡一律写 原文未给阈值 而不猜 |
| 与登记底稿的分歧 | ① `sources/cao.md:317` 与 CSV 把 FGFR2 最优结合剂写作 sub-nanomolar；**本地正文原句是 digital nanomolar affinity**（原文如此，疑为排版/笔误），本卡按本地全文记并标注两种口径不可同时引用。② `sources/cao.md:311` 的五联成功率定义、`:312` 的 >60% 与 Fpocket、`:318` 的 12/95 与 32/96 对照，本地全文逐字命中，予以采纳。③ 底稿把本篇称作 HalluDesign 框架 + NA-MPNN 的说法属于 C20，与本篇无关 |
| 未取到的部分 | Methods 全文、主图 Fig.1–5 与补充图 S1–S14 的图本体（本地只有图注文字）、补充表、每个靶逐条送测清单与其计算分数、任何 GPU-h/核时数字。凡引用这些处本卡明写 正文未给出，仅有正文/图注描述 |

## 1. 这篇到底解决什么（大白话）

AlphaFold3 这类模型算得准，但一直只被当**裁判**用：生成器（RFdiffusion 一类）先撒几十万条骨架，再拿 AF2/AF3 的置信度阈值事后挑出能过关的，最后下单几百到几万个做实验。要么就是另一路——对模型做反向传播去优化序列，作者原话是 "they typically require high computational costs and often fail to converge due to the rugged"。本文想改的是**这个次序本身**：把 AF3 扩散模块天生会犯的毛病——低置信区域也能编出看着合理的结构（文中称 structure hallucination）——当成**优化器**来用。

做法是一个只走前向、不微调、不反传的循环：①结构更新 = 不再从纯高斯噪声起跑，而是给现有（或上一次的）结构加**用户指定的噪声水平**，让模型从那里反向扩散出一个更干净的结构；噪声越大探索越宽，噪声越小只做局部精修；②序列更新 = ProteinMPNN/LigandMPNN 在新骨架上采样一批序列，再用自研的轻量打分器 CoDP 排序，取最好的一条回喂给下一轮。模型自带的 pLDDT/ipTM 在循环里当实时进度读数。

关键差别（也是最该被本库记住的一点）：**功能约束在生成阶段就已经是条件**，而不是生成完再筛。配体从第一步就被放进蛋白里一起优化（三种初始化：蛋白质量中心 / Fpocket 定义口袋的中心 / 让 AF3 自己找位置），靶蛋白可以作 template 喂进去，环肽靠改 AF3 的位置索引强制头尾环化，非天然氨基酸（NCAA）作为共价弹头直接写进序列，抗体的 CDR 用坐标噪声 + 全甘氨酸序列起手重建。于是设计在**下单前**就已经被推到判定阈值以上，实验只需极小批量：配体靶每靶不足 16 个、PPI 靶每靶恰好 16 个。作者据此声称拿到 50–81% 的投测命中率——但注意它的分母是 16，见第 5、7 节。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **两条既有路线各自卡死：反传太贵不收敛，微调要靠海量骨架过关**。现象/证据：引言里对梯度法的判断是 "they typically require high computational costs and often fail to converge due to the rugged"；对微调/生成式的判断是 "However, a large number of scaffolds and subsequent sequence sampling are necessary in order to"；对能景粗糙性的定性是 "The real protein sequence-structure landscape is highly rugged"。**他们做了什么**：两条都不走，改成只前向的迭代幻觉——"Crucially, the entire process involves only forward passes through the structure prediction and"，并把扩散轨迹截断成长度旋钮（噪声小=局部精修，噪声大=宽域探索）。**应对后仍留下的代价**：本地正文**没有任何算力成本数字**（无 GPU-h、无核时、无每秒设计数），只有定性表述 "the complementary sequence design stage is performed,"；与反传法（RSO）/扩散法（RFdiffusion、BoltzDesign1）的对比只有指标曲线，没有单价，因此 本文未解决 成本这条轴。

2. **噪声水平是双刃剑：同一招对差骨架有用、对好骨架有害**。现象/证据：图 2 图注把两件事写实了——"For low-quality backbones such as Chroma ," 与 "For high-quality Binder complex backbones from"；正文同样承认步长取舍 "shorter trajectories (e.g.,"。**他们做了什么**：按任务分档定死参数——精修/保持拓扑用短轨迹（50 步），修批量低质骨架用长轨迹（图 1 图注称可把至多 1000 条 Chroma 骨架修成高质量结构），设计任务默认把扩散截到 150 步："we truncated the diffusion step to 150 unless"；比较 RFdiffusion partial diffusion 时也把两边步数对齐写明（RFD 12 步/总 50 步 vs HalluDesign 50 与 150 步/总 200 步）。**代价**：档位是经验选择，**没有给出何时换挡的判据**，也没给出这些设置下的通过率数字；>300 aa 的大蛋白要更长轨迹或更多轮次（"This trade-off was more pronounced for large"），但没给大蛋白的量化收敛。

3. **真 from scratch（无任何骨架）在 AF3 引擎上做不成，大于肽的蛋白一律塌掉**。现象/证据：原句 "However, when this de novo strategy was applied"，归因是 "We hypothesized this is because the random"。**他们做了什么**：换引擎而不改算法——"To overcome this, we substituted the AF3 engine"，理由是语言模型嵌入把能景抹平："allowing Protenix to find a convergence path even"（该短语在本地文本里带排版引号粘连，本卡只作定位用，不列为逐字引句）。**代价**：换引擎换来新失败模式，作者在补充图注里自承 "However, Protenix tends to suffer from"，本地正文没有对 over-hallucination 给出任何量化定义或规避阈值；换引擎后 PD-L1/FGFR2 的成功率数字也因此**不能与 AF3 引擎的曲线直接比较**。

4. **柔性/大极性配体是最弱的一环，作者只给了方向没给数字**。现象/证据：与固定配体的生成式做法对比，他们的优势是同时优化蛋白与配体构象——"This enhancement was particularly pronounced for"、"Our model excels in handling ligands with"；但 in-silico 成功率随配体性质剧烈变化："This success rate was inversely"**他们做了什么**：把配体当生成条件的一部分（black hole initialization + 三种初始化对比）、并用 150 步截断降成本；绕过 docking："This direct co-optimization approach bypasses the"。**代价**："considerably lower" 后面**没有数字**（本地全文只有 >60% 这一档，大极性配体的百分比只在补充图里，本地不可得），所以这句话现在只是作者自述的方向性坦白，不能拿来当可用率。

5. **实验端没有漏斗：直接把投测规模压到 16，跳过了排序-淘汰这一层**。现象/证据：正文自述这是刻意选择——"Unlike conventional high-throughput design"、"HalluDesign achieved binder discovery in a"、"For each small-molecule target,"；PPI 侧是 "For each target, we experimentally tested 16 de novo designed binders and observed high success rates"；拯救实验是 "We selected 16 rescued designs"。**他们做了什么**：用五联判定阈值（见第 3 节 S2）在生成回路内自证过关，只把过关者送去表达。**代价（本卡认为最要害的一条）**：**选取规则与生成规模本地全文均未给出**——没有 生成多少条 / 多少条过五联阈值 / 这 16 条是不是 top-16 的任何记录，所以 50–81% 只是**末端投测命中率**，整条管线的设计成功率无法计算（对比 Baker 组 B09 那种 2M→20K→1–17 的分层台账，本篇完全没有中间层）。本文未解决。

6. **磷酸化特异性抗体这一栏只有单浓度读数**。现象/证据：设计上靠自由采样肽构象——"Unlike conventional methods"、"HalluDesign models free sampling of peptide conformations."；实验上 "Experimental results demonstrated specific binding to the phosphorylated form of Aβ, with no detectable interaction with native Aβ"，机理解释是 "This is consistent with our"；图注写明读数口径是单浓度——"BLI binding affinities are"，同段给出 "with measurements taken at a"。**他们做了什么**：把磷酸基团当选择压力（设计端就是按磷酸化肽建模），并用去磷酸化肽做同浓度阴性对照。**代价**：本地正文没有这两个抗体的 K_D 数字，也没有浓度梯度；纳米抗体路线（EGFR，Protenix + contact distance 定 hotspot）**在本地只有图注与置信度描述，未见湿实验结果**。

7. **假阳风险的来源被作者自己点出来了但没闭环**。现象/证据：优化器与评估器同源（都是 AF3 类模型），作者为此专门做了交叉评估（补充图 6：AF3 优化分别用 AF3/Protenix/Chai-1/Boltz1 评；补充图 8 检查 optimizer confidence 与 evaluator confidence 的一致性，如 "Consistency between protein-binder complex designs optimized by AF3 and confidence scores from AlphaFold-Multimer evaluation."）。**他们做了什么**：用独立预测器复评 + 把置信度曲线随循环单调上升当证据。**代价**：这些一律是**计算自评**；只有配体与 PPI 那几个靶有湿实验（ITC/BLI/晶体学）回填，抗体只到 BLI 单浓度；磷酸化特异性抗体的自洽性与纳米抗体没有任何实验否定路径，本文未解决。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **结构更新（本文的主角）**：AlphaFold3 式模型的扩散模块 + **截断扩散**——不从纯噪声起跑，而是给输入结构加用户指定噪声水平再反向扩散。"Instead of initializing the"；短轨迹保拓扑、长轨迹逃逸局部极小："Shorter trajectories, corresponding to lower noise levels, prompt local refinement, which is well-suited for optimization tasks requiring the preservation of overall topology." / "Conversely, longer trajectories, corresponding to higher noise levels, enable broader exploration of structure space to escape local minima"
- **序列更新**：反向折叠模型采样 + 自研轻量排序器 CoDP 选一条回喂。"In the subsequent sequence"；"The top-ranked sequence is then"；CoDP 的训练口径："CoDP was then trained to"（训练结构来自 AFDB："The CoDP model was trained on"）
- **回路内的实时判据**：模型自带置信度。"The built-in confidence metrics"
- **功能约束的三种前置写法**：①配体位置：蛋白质量中心 / Fpocket 口袋中心 / 让 AF3 自己决定（"AF3 prediction is directly"）；②模板与拓扑：靶蛋白作 template、改 AF3 位置索引强制头尾环化（"This application involved two"）、NCAA 作共价弹头；③抗体：框架保留、CDR 加坐标噪声并用甘氨酸序列起手（"CDR residues are centered and"）。
- **引擎可换**：AF3 / Protenix（带 ESM 语言模型嵌入）；评估侧还用了 Chai-1、Boltz1、AlphaFold-Multimer、ESMFold 做交叉复评。
- **实验侧（本地可见的只有这些）**：E. coli 表达；配体结合用 **ITC**（口袋点突变验位置、交叉结合验特异性）；PPI/抗体用 **BLI**；**X 射线晶体学** 复算设计构象（cAMP、AD、Zn 复合物 + DTG、TRP apo）。
- **明确没有用的方法**：本地全文对 `molecular dynamics`、`MD simulat`、`GROMACS`、`OpenMM`、`AMBER`、`umbrella`、`metadynam`、`MM/PBSA`、`MM-GBSA`、`free energy`、`thermodynamic integration`、`explicit solvent`、`quantum`、`DFT` 全部 **0 命中**；也没有任何催化/酶活词（`cataly`、`turnover`、`enzyme`、`kcat`、`Michaelis` 全 0 命中）。→ 本篇与 MD/QM、与酶活测量**无任何关系**，不能为它们提供任何命中率背书。

### 工作流程表（按论文叙述顺序；括号内为原文出处）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 优化既有骨架 | 低质单体骨架（Chroma；反传法 RSO 骨架）；已实验验证的高质 RFdiffusion PPI 骨架；RFdiffusion all-atom 生成的配体结合剂 | 结构更新（截断扩散，噪声步数按任务选）↔ 序列设计（ProteinMPNN/LigandMPNN 采样 + CoDP 排序）交替多轮 | 无独立淘汰阈值（这是优化任务，不是筛库）；观察量为 RMSD、pLDDT、RMSD-to-origin 随轮次单调改善。Chroma 用 100-200 步、"typically within 6-7 cycles" 收敛；高质 RFdiffusion 骨架更多步"provides no substantial improvement" | 至多 1000 条 Chroma 低质骨架被修成高质量结构（图 1 图注）；RSO、RFdiffusion PPI 集、配体集为图 2-3、补充图 S1-7 的基准集，**具体条数本地未给** |
| S2 预定义骨架 + 配体的 de novo 设计 | NTF2 支架 / 沿伪对称轴带口袋的伪环支架 / 抗体 scFv 与纳米抗体框架 / 环肽（靶作 template）+ 随机选取的配体三维构象 | 把配体放到蛋白中心或 Fpocket 口袋中心并随机旋转（black hole initialization），或让 AF3 自定位置；跑标准共优化循环，**设计任务把扩散截到 150 步**（默认 200 步） | **五联 in-silico 成功率定义（图 S9 图注，其标题限定在 Scaffold-based ligand-binding protein design 这一任务）："The success rate is defined as: protein RMSD ≤ 1.5 Å, protein pLDDT ≥ 85, ligand RMSD ≤ 2 Å, ligand pLDDT ≥ 85, and ipTM ≥ 0.85."** 同图注给出三种配体初始化；口袋定义原句："Binding pockets are defined"；抗体侧只看 pLDDT/pTM 随循环上升（图 3 图注），未给独立阈值 | in-silico 成功率随配体大小与极性反比："for small, hydrophobic ligands,"，大极性配体 "considerably lower"（本地无数字）；作者称显著高于 RFdiffusion all-atom 与 BoltzDesign1 |
| S3 真·from scratch | 纯高斯噪声坐标 + 随机序列（无任何结构输入）；第二轮起换成 Protenix 引擎 | 先跑一次预测拿到初始构象，再把它接进标准循环："This general strategy initiates"；"After a single prediction pass" | 原文未给阈值（仅以 pLDDT/pTM/ipTM 随轮次上升为进度） | AF3 引擎下**大于肽的蛋白全部失败**（塌成单条长螺旋等低复杂度构象）；换 Protenix 后得到 PD-L1、FGFR2 结合剂的全新骨架，但 Protenix 有 over-hallucination 新问题 |
| S4 实验下单（配体侧） | S2 产出的 cAMP/ATP/AD/CA/DTG/TRP/Zn 结合剂设计 | E. coli 表达 → ITC 测结合 → 口袋点突变竞争 → 交叉结合（TRP vs Tyr/Phe；AD vs NE）→ 晶体学复算 | 原文未给下单前的排序阈值；判据是湿实验本身 | 每靶**不足 16 条**送测；"ITC measurements confirmed one"；得到 5 个结构：cAMP 3.1 Å、AD 2.4 Å、Zn 1.6 Å、DTG 与 TRP apo 各 2.0 Å |
| S5 实验下单（PPI 拯救） | RFdiffusion 公开 PPI 集里**先前失败**的设计（PD-L1、IL7RA） | 截断 AlphaFold3 扩散轨迹，以初始复合物或中间轮预测作条件做优化，各取 16 条送 BLI | 计算侧看 binder RMSD/pLDDT 改善与偏离原结构的程度；实验侧 BLI 结合信号 + 亲和力 | "Biolayer interferometry (BLI)"；"Overall, these designs displayed low nanomolar affinities for their respective targets." |
| S6 实验下单（de novo binder + 抗体） | S3 的 Protenix 全新结合剂（PD-L1、FGFR2，靶为 β-折叠面）；Herceptin scFv 重建 CDR 靶向 pS8-Aβ | 每靶 16 条设计表达后做 BLI；抗体组另测去磷酸化 Aβ 作阴性对照 | 结合信号（BLI）；抗体特异性按单浓度 **1000 nM** 比较（图 5 图注） | "8 out of 16 PD-L1 binders"（末短语为原文写法，见 §0 分歧①） |
| S7 计算侧交叉复评（防自评膨胀） | 同一批优化结果 | 分别用 AF3 / Protenix / Chai-1 / Boltz1 / AlphaFold-Multimer / ESMFold 重新评估；检查 optimizer 与 evaluator 置信度一致性 | 图 S6 图注给出的参考线："Red line indicates 5 Å RMSD," | 补充图 S1-14 的曲线与分布（本地仅图注文字，无数值表）；环肽侧只对 top 分位画曲线："The optimization curves display" |

## 4. 关键数字台账（全部来自本地全文 C19_PPR1116408_text.txt，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段 / 位置） |
|---|---|---|
| protein RMSD ≤ 1.5 Å；protein pLDDT ≥ 85；ligand RMSD ≤ 2 Å；ligand pLDDT ≥ 85；ipTM ≥ 0.85 | 本文 in-silico 成功率的五联定义（全部同时满足才算一条成功设计） | Supplementary Information Figure 9 图注："The success rate is defined as: protein RMSD ≤ 1.5 Å, protein pLDDT ≥ 85, ligand RMSD ≤ 2 Å, ligand pLDDT ≥ 85, and ipTM ≥ 0.85." |
| > 60% | 小、疏水配体的 in-silico 成功率；大极性配体仅定性说 considerably lower（本地无数字） | "for small, hydrophobic ligands," |
| 150 步（默认 200 步）；50 步；100-200 步；6-7 轮；>300 aa | 截断扩散的档位：设计默认 150 步，精修 50 步，低质骨架 100-200 步且常 6-7 轮收敛；大于 300 残基需更长/更多轮 | "we truncated the diffusion step"；"Longer trajectories (100-200"；"This trade-off was more pronounced for large proteins (>300 aa), which required longer trajectories or additional cycles to accommodate the substantial conformational changes needed for convergence." |
| 12 步 / 总 50 步 vs 50 与 150 步 / 总 200 步 | 与 RFdiffusion partial diffusion 的对照设置（RSO 骨架基准） | Supp Fig 2 图注："For the RFdiffusion partial" |
| 至多 1000 条 | 被优化的低质量 Chroma 骨架批量 | Fig 1 图注："This allows for the optimization of up to 1000 low-quality Chroma backbones into high-quality, refined structures." |
| 12 条 | 配体结合蛋白优化基准的样本数 | Supp Fig 5 图注提到 "the RMSD of twelve ligand-binding proteins relative to the original scaffold" |
| 5 Å / 2 Å | 配体优化基准图里的两条参考线 | Supp Fig 6 图注："Red line indicates 5 Å RMSD," |
| 不足 16 条 / 靶 | 配体侧实验送测规模（低通量是刻意设计） | "For each small-molecule target," |
| 每靶 16 条 | de novo PPI 结合剂与拯救实验的送测规模 | "For each target, we experimentally tested 16 de novo designed binders and observed high success rates"；"We selected 16 rescued designs" |
| 8/16 = 50%（PD-L1）、32 pM | de novo PPI 结合剂的投测命中率与最佳亲和力 | "8 out of 16 PD-L1 binders" |
| 13/16 = 81.3%（FGFR2） | de novo PPI 结合剂投测命中率（FGFR2 最佳值本地原文写作 digital nanomolar affinity，与二级底稿的 sub-nanomolar 不同，见 §0） | "and 13 out of 16 FGFR2 binders" |
| 12/16 = 75%（PD-L1 拯救）、8/16 = 50%（IL7RA 拯救） | 把 RFdiffusion 失败设计救回来的投测命中率 | "Biolayer interferometry (BLI)" |
| 12/95 = 12.6%、32/96 = 33.3% | 图注给出的 RFdiffusion 原实验口径（对照分母 95/96，非本文生成） | Fig 5 图注："RFdiffusion reports a success rate of 12/95 for PDL1, whereas our method achieves a higher success rate of 12/16."；同段 "RFdiffusion reports a success rate of 32/96 for IL7RA, while our method achieves a higher success rate of 8/16." |
| low nanomolar | 拯救设计的亲和力水平（无逐条 K_D，无最优值表） | "Overall, these designs displayed low nanomolar affinities for their respective targets." |
| 3.1 Å / 0.74 Å / 1.07 Å / 7 条氢键 | cAMP 复合物晶体分辨率、蛋白与配体 Cα RMSD、预测氢键在晶体中全部出现 | "The cAMP-binder complex was"；"Notably, all seven hydrogen" |
| 2.4 Å / 0.65 Å | AD 复合物晶体与 Cα RMSD | "The AD binder complex was" |
| 1.6 Å / 0.81 Å / 四配位 | Zn 复合物晶体、Cα RMSD、四面体配位几何与四个配位残基位置 | "The zinc binder complex was" |
| 2.0 Å / 0.31 Å 与 0.81 Å | DTG 与 TRP 的 apo 晶体分辨率与 Cα RMSD | "We also obtained apo structures" |
| 1000 nM（单浓度） | 磷酸化特异性抗体 BLI 的比较口径（本地无 K_D） | Fig 5 图注："The binding affinities are also" |
| pLDDT 88.65 / 86.4 | 含非天然氨基酸 AcrK 的头尾环肽（共价靶向 EGFR Cys797）的**计算置信度**，非实验值 | Supp Fig 14 图注："Cyclic peptide pLDDT = 88.65" |
| top 10% | 环肽优化曲线只画最优分位（本地无绝对数值） | Supp Fig 13 图注："The optimization curves display" |
| 7 个配体靶 | cAMP、ATP、AD、CA、DTG、TRP、Zn²⁺；支架为 NTF2 / 伪环 / 杂合 NTF2 | "NTF2 scaffolds were used for" |
| 0 次 | 本地全文里 MD、QM、自由能、催化/酶活相关关键词的出现次数（见 §3 工具箱末条） | 自查命令见第 9 节 |

## 5. 结论——作者说了什么（只写原文，且把分母与证据层级分开）

**5.1 方法层的自述结论**
1. 幻觉可当优化器用："While this property is an"；并声称"only forward passes"、免微调免反传（见 §2.1 引句）。
2. 噪声水平当任务旋钮："Structure conditioning at"
3. 结论段的收口："Our approach smooths the rugged"；并预期随预测模型进步该策略更强。
4. 低通量是卖点而非妥协："HalluDesign achieved binder"

**5.2 作者自述的命中率数字，逐条附分母**

| 作者的说法 | 分母是什么 | 该分母在本地全文是否可核查 |
|---|---|---|
| 配体侧：每靶 ITC 确认到至少一条结合剂，"ITC measurements confirmed one" | 每靶**不足 16 条**送测（7 个配体/金属靶，各自条数未列） | 部分可核：条数只写到 fewer than 16，无逐靶清单、无生成了多少条 |
| de novo PPI：PD-L1 8/16（最强 32 pM）、FGFR2 13/16 | **恰好 16 条**为每靶合成并做 BLI 的设计 | 命中率可核；但**这 16 条怎么从计算池里挑出来，原文未给规则与阈值** |
| 拯救 RFdiffusion 失败设计：PD-L1 12/16、IL7RA 8/16，"Overall, these designs displayed low nanomolar affinities for their respective targets." | 每靶 16 条，且每条都来自一个**先前失败**的设计 | 可核（BLI）；对照方 12/95、32/96 是 RFdiffusion 已发表数字，非本文实测 |
| 磷酸化特异性抗体：只认 pS8-Aβ，与非磷酸化 Aβ 无检出 | 2 条设计抗体、单浓度 1000 nM 的 BLI 比较 | 可核；本地无 K_D、无浓度梯度 |
| in-silico 成功率：小/疏水配体 > 60%；对大极性配体明显更低；且高于 RFdiffusion all-atom 与 BoltzDesign1 | 五联阈值（1.5 Å / 85 / 2 Å / 85 / ipTM 0.85）下通过的**计算设计复合物数**；生成分母本地未给 | 仅方向可核，数字只在补充图（本地无图本体） |
| 摘要级总括："Experimental characterization" | 上述各集合的合并叙述 | 该句把**计算自评与湿实验混在一起说**，本卡不据此得出统一成功率 |

**5.3 作者自认的边界（原话）**
- from-scratch 在大蛋白上失败并靠换引擎解决："However, when this de novo"
- 换引擎的新毛病："However, Protenix tends to"
- 大极性配体的弱项：见 §5.2 最后一行（"considerably lower"，本地无数字）。
- 明确强调实验不可替代（配体侧靠突变与交叉结合自证）："Mutational analysis of the"

**5.4 湿实验 vs 计算自评的清单（作者层面的划分，非本文推理）**
- **上了湿实验的**：小分子/金属离子结合剂（E. coli 表达 + ITC + 口袋点突变 + 交叉特异性 + 5 例晶体学：cAMP/AD/Zn 复合物与 DTG/TRP apo）；PD-L1、FGFR2 的 16 条 de novo 结合剂（BLI）；PD-L1、IL7RA 的 16+16 条拯救设计（BLI）；靶向 pS8-Aβ 的两条 scFv（BLI 单浓度 + 去磷酸化阴性对照）。
- **只有计算自评、本地全文未见湿实验的**：1000 条 Chroma 骨架与 RSO 骨架的优化；RFdiffusion PPI 高质骨架的再优化；五联阈值的 in-silico 成功率与 >60%；与 BoltzDesign1/RFdiffusion all-atom 的比较；AF3/Protenix/Chai-1/Boltz1 交叉评估与置信度一致性（S6-S8）；抗体 CDR 重建的优化曲线（S11）；**EGFR 纳米抗体（S12）**；**环肽与含非天然氨基酸 AcrK 的共价环肽（S13-S14，只有 pLDDT 88.65 / 86.4 这类置信度数字）**。
- **作者完全没有声称的**：任何催化、酶活、turnover、底物转化——本地全文 `cataly`、`turnover`、`enzyme`、`kcat`、`Michaelis` 均 0 次命中；也没有 MD、QM、自由能计算。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的贡献不是新网络，而是把漏斗的方向倒过来**：从 生成大库→事后排序→投 10²–10³ 个，改成 把判定阈值写成生成条件→投 16 个。Baker 组 B09 那条链是"用带标签的历史湿实验数据给筛子打分"，本篇是"让生成器自己朝着筛子的形状走"。前者需要百万级标注（他们没有），后者只需要一个可微/可迭代的目标函数（他们用置信度替代）。
2. **命中率数字的信息量被分母换掉了**。16 这个分母既不是生成池也不是候选池，而是**作者自选的送测小集合**，而且选取规则本地不可得。因此 8/16、13/16 只能读成 这 16 条里有多少条表达并可测，读不出 生成了多少条、淘汰了多少条。**同一批数字与 B09 的 1–17/20,000 不在同一口径上，谁都不该拿去校准谁的命中率。**
3. **五联阈值是"设计自洽度"，不是功能**。protein RMSD ≤ 1.5 Å + pLDDT ≥ 85 + ligand RMSD ≤ 2 Å + ligand pLDDT ≥ 85 + ipTM ≥ 0.85 全部来自被优化那一系模型自身或其近亲；把它当成功概率的分母，等于把考官出的题和给出的分混成一件事。作者的交叉评估（Protenix/Chai-1/Boltz1/AF-Multimer/ESMFold，补充图 S6/S8）是在缓解这一点，但**没有改变"评估器与优化器同源"这一结构问题**。
4. **本篇对我们筛选漏斗最有用的反面证据是"from-scratch 大蛋白失败"**：AF3 幻觉在缺乏语言模型先验时把设计推进到"单条长螺旋"。这提示纯置信度驱动的搜索存在**退化吸引子**——优化目标可以完全满足而生物学上无意义。我们的判据若只用结构置信度类分数，会遇到同型风险。
5. **它对非天然氨基酸的处理方式值得单独记下**：把 NCAA 写进生成回路（AF3 的共价修饰建模 + 位置索引改写，做共价弹头环肽 AcrK 靶向 EGFR Cys797），但目前**只有 pLDDT 88.65 / 86.4 这一类计算置信度**，没有掺入率、没有反应验证。也就是说 用幻觉设计 NCAA 载体 这条路在他们那里也还停在自评阶段。
6. **"没有 MD/QM 也能拿到实验命中"是这篇的存在方式**，因此它既不能支持也不能反对我们用 MD/QM 判催化的路线；两者的判据对象不同（静态复合物自洽 vs 反应路径）。引用它时只能引用**方法结构**（约束前置），不能引用**任何数字**做校准。
7. 我们读出的口径风险：摘要句把计算与实验合并叙述（"comprehensive computational and"），而正文里 success rate 一词至少指两件事（五联阈值的 in-silico 通过率 / BLI 或 ITC 的投测命中率）。**任何引用必须当场写明是哪一个**，否则就像本库里已经出现过的 90%+ 传闻那样，把末端小分母读成管线成功率。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自己写在正文里的**
1. 真·从头设计在大蛋白上失败，靠换引擎绕过："However, when this de novo"
2. 换引擎带来的新毛病（补充图注自承）："However, Protenix tends to"
3. 大极性/大配体的 in-silico 成功率明显低于小疏水配体的 >60% 档，但未给数字："This success rate was inversely"
4. 步数/轨迹长度对已经高质的设计并不总是有益，甚至会把结构推离原位："For high-quality Binder complex"

**我们读出的方法学局限（按严重度排）**
5. **成功率的分母不可复算**。全篇没有 生成了多少条 / 过五联阈值多少条 / 为什么选这 16 条 的任一层数字，也没有中间淘汰表；因此 50–81% 只能作为 末端投测命中率 引用，**不能作为 管线设计成功率**。与 B09（2M→20K→1–17，每层有数）相比，本篇在漏斗记账上是倒退的。
6. **证据层级混用**。摘要用一句 "Experimental characterization" 同时涵盖 ITC/BLI/晶体（湿实验）与 pLDDT/ipTM 曲线（自评）；EGFR 纳米抗体、含 NCAA 的环肽、抗体 CDR 优化曲线在本地全文里**只有计算置信度**。
7. **预印本、未见同行评审、未见独立复现**（`sources/cao.md:480` 同判）。FGFR2 最佳值的写法在本地正文是 digital nanomolar affinity，与二级底稿的 sub-nanomolar 不一致（§0 分歧①）；本地也无逐条 K_D 表 → 32 pM 是本文唯一有明确数字的亲和力。
8. **本地这份抽取不含 Methods 与表格**（§0 证据级别行）：表达/纯化条件、BLI 与 ITC 参数、晶体筛选与配体浓度、生成与评估的实现细节（采样温度、序列数、循环轮数上限）全部不可核；因此本卡第 3 节多数步骤的判据一栏只能写 原文未给阈值。
9. **对照基线是引用来的**。12/95、32/96 直接取自 RFdiffusion 已发表数字（图注），实验体系（表达、检测、判定）是否与本篇 16 条同一口径，本地无法核对 → 75% vs 12.6% 这类 六倍 之差不能当作方法学效应的定量结论。
10. **自评风险**：优化器与主判据同源于 AF3 一系模型；交叉评估只到 用另一族预测器再打一次分，仍未脱离结构置信度范畴，也没有独立物理量（能量、动力学、反应势垒）。
11. **对功能只做到结合，没做到催化**。全文 0 次出现 catal/turnover/enzyme/kcat；因此本篇证据链末端是 K_D 与晶体，不含任何活性数字 —— 这也是本卡判定它对酶活筛选无校准力的根据。
12. 晶体只覆盖配体侧 5 例（cAMP/AD/Zn/DTG/TRP），PPI 结合剂侧本地未见复合物结构验证声称；抗体侧只有单浓度 BLI。样本极小，任何 原子级准确 的表述应限定在这 5 例上（原句为 "The high experimental success"，其外推范围是配体结合平台）。
13. **五联阈值的适用范围比二手记录窄**。该定义出现在 补充图 9 图注，其标题限定为 Scaffold-based ligand-binding protein design；本地全文**没有**把它写成 PPI、抗体或 from-scratch 任务的判定式（PPI 侧只有 BLI/ITC 的实验口径与 pLDDT/ipTM 曲线）。`sources/cao.md:420` 与 CSV 阈值列把它当本篇通用的 成功率定义 引用，属于口径放大——引用时必须写明 这是配体结合任务的 in-silico 判定式。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用；只借方法结构，一律不借它的数字）**

1. **把功能约束写成生成条件，而不是生成后再筛**（本库 G0–G10 门中判据前置/生成条件类；本仓库口径见 `data/literature_cards/README.md:17`）。他们的做法是可复算的三种前置：配体三维构象进口袋（质量中心 / Fpocket 口袋中心 / 模型自定）、靶蛋白作 template、改位置索引强制头尾环化与 NCAA 共价。→ 我们的等价动作：把 UTP（或目标底物片段）与参与催化的残基类型一起写成设计/打分的条件，让候选从第一轮就带着底物位姿走，而不是先造口袋再用结构一致度事后挑。
2. **单一旋钮控制探索幅度**：截断扩散的步数/噪声水平决定 局部精修 vs 宽域探索，且他们按输入质量分档（低质骨架长轨迹、高质短轨迹）。→ 我们做侧链重排或局部精修时应有同样的显式保守/激进档位，并把 何时该换挡 写成可测条件（本篇没做，见 §2.2 代价）——这是我们比它必须补齐的部分。
3. **回路内实时读数 + 单调性当作有效性信号**："The built-in confidence metrics"。→ 我们的 xTB/MD 评价应记录逐轮曲线并检查单调改善；不单调甚至震荡就是判据本身失效的告警，而不是继续调权重。
4. **用廉价排序器替掉反传**：CoDP 只做 distogram 预测 + 对比学习给 MPNN 采样序列排序（"The CoDP model was trained on"）。→ 我们可以造一个便宜的几何/静电预筛器排在 xTB 与 MD 之前，**但它的训练标签不许来自将被它评估的同一族模型**，否则就复制了本篇的自评风险（§7.10）。
5. **NCAA 进入生成回路而不是事后修饰**：把共价弹头残基当序列的一部分（Supp Fig 14 图注 "Design of a head-to-tail cyclic"）。→ 与酶设计主题同构的只是表示层：设计阶段就允许非天然残基占位。注意这条**目前只到置信度自评**，没有湿实验，不能当可行性证据。
6. **特异性的成对实验设计**：口袋点突变 + 交叉结合（TRP 结合剂不认 Tyr/Phe；AD 结合剂对只差一个甲基的 NE 几乎不认），原句见 "for example, the TRP binder did"。→ 我们每个候选的湿实验应同样配 近邻底物交叉测试 + 关键残基失活 两路，用来区分 结合 与 催化、并把失败归到具体化学事件（分步归属）。

**不可迁移（为什么不能照搬）**

1. **五联 in-silico 阈值不是酶活判据**。protein RMSD ≤ 1.5 Å / pLDDT ≥ 85 / ligand RMSD ≤ 2 Å / ligand pLDDT ≥ 85 / ipTM ≥ 0.85 全部回答的是复合物是否按设计自洽，与能否把底物接到 tRNA 路径上无对应关系。本库与本目录门禁都把借 binder 的 pAE/ipTM 阈值当酶活判据列为禁止项，本篇的 ipTM/pLDDT 阈值属同类，**同样禁止搬用**。
2. **不许把它对 PD-L1 / FGFR2 / IL7RA 的投测比例当成对酶活的预测能力**。8/16、13/16、12/16、8/16 的分母是作者自选的 16 条送测集，且任务全是结合（BLI），不是催化；这些数字与目标酶没有任何校准关系，也不许换算成某法对酶设计成功率 X%（本目录明令不许编造）。
3. **配体结合设计不等于酶**。他们做的 ATP、cAMP、肾上腺素、胆酸、dolutegravir、色氨酸、Zn²⁺ 结合蛋白只是 认得出配体，全文没有任何 turnover、kcat、Km 或产物转化鉴定；因此本篇**不能**支持 能设计 ATP 结合蛋白 → 能设计用 ATP 的酶 这一步推理。
4. **全文无 MD、无 QM、无自由能**（§3 工具箱末条的 0 命中核查）。它既不能作为 用 MD/QM 判催化 的命中率背书，也不构成反证——它与这条路线无关。
5. **低通量下单（16 条/靶）不能照搬成我们的规模策略**。我们一轮最多几个构建体，比它还少，但我们的瓶颈是**产物化学身份**而非表达量，因此末端必须做 机制多样性 + 失活对照 的信息量最大化，而不是复现它那种 高投测命中率 的可观数字。
6. **Protenix/AF3 引擎与置信度不能进我们的闸口**：作者自己点出 over-hallucination（"However, Protenix tends to"），且其 from-scratch 模式会把大蛋白推入单螺旋这类退化构象——把它当准入判据会把我们带到同类陷阱里。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/C19_PPR1116408_text.txt

- **本卡实际照着写的唯一底稿**：`data/literature_cards/fulltext/C19_PPR1116408_text.txt`（55,493 B，SHA-256 `1a68c94cc1b69271…`，由同目录 `C19_PPR1116408_fullTextXML.xml`（235,944 B，SHA-256 `815e8ee604006ee7…`，实为 bioRxiv v1 正文页 HTML）经 `scripts/litcards_text.py` 的去标签+归一化生成，未改写内容）。本篇只有这一份本地全文（Europe PMC 与 NCBI 双版本不存在于本地），因此不存在跨抽取版本的引文编号差异风险。
- **抓取通道**：`data/literature_cards/fetch_log.tsv` 第 134 行（前两次 HTTP 500 记录在第 15、84 行）；`data/literature_cards/batches.tsv` 第 18 行 `state=FULLTEXT · fulltexts=…C19_PPR1116408_text.txt · records=sources/cao.md · OK · fallback_ok[biorxiv_full]`。本地落盘时间 2026-10-20 12:24（`stat` 实测）。本卡未做任何新的网络抓取。
- **对照底稿行号**：`sources/cao.md:305–320`（原卡）、`:420`（曹组漏斗对照表 C19 行）、`:30`（90%+ 传闻的口径核查）、`:455`（该组正文 MD/QM 关键词扫描）、`:480`（预印本未复现警示）；CSV 行 `data/protein_design_literature.csv` 编号 C19；DOI 核验 `data/gate.json`（`status=OK`，Crossref）。
- **本地缺失的核验面**：Methods 与全部表格（`Table` 0 次命中）、Fig.1–5 与 S1–S14 图本体。凡涉及这些的判据本卡写 原文未给阈值 / 正文未给出，仅有图注描述。
- **自查命令（本卡逐条复跑）**：
  - 门禁：`cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "C19" --no-report` → 实测输出 **`PASS C19 quotes=105/105`**，退出码 0（首次运行为 FAIL：第 4 节两处用省略号截断了引句，改为完整原句后复跑转绿）。**未跑** `--sync-map`，**未跑**不带 `--no-report` 的全量门禁。
  - MD/QM/酶活 0 命中核查（§3、§7 用）：对该纯文本 `grep -c` 以下模式全部为 0 —— `molecular dynamics`、`MD simulat`、`GROMACS`、`OpenMM`、`AMBER`、`umbrella`、`metadynam`、`MM/PBSA`、`MM-GBSA`、`free energy`、`thermodynamic integration`、`explicit solvent`、`quantum`、`DFT`、`cataly`、`turnover`、`enzyme`、`kcat`、`Michaelis`。
  - 无表格核查：`Table` 出现 0 次；`Method` 仅 4 次且全在参考文献条目（期刊名）。
- **口径提醒（写给回写 CSV 与后续引用的人）**：本卡的 50% / 81.3% / 75% 全部是 **16 分母的投测命中率**，且为 **bioRxiv v1 预印本（2025-11-08 投稿 / 2025-11-09 发布）作者自述、未经同行评审与独立复现**；引用时必须同时带上 预印本 与 分母 16 两个限定。FGFR2 最佳亲和力本地原文写作 digital nanomolar affinity，与二级底稿 `sources/cao.md:317` 的 sub-nanomolar 不一致，本卡以本地全文为准并保留分歧记录。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本/统计`；第 5 节 ↔ `实验验证手段/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 85 条逐字引句来自许可受限的第三方来源（C19；CC_BY_NC），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=预印本（bioRxiv v1，2025-11-08 投稿 / 本地正文页自记 Posted 2025-11-09，DOI 10.1101/2025.11.08.686881，EPMC 题录号 PPR1116408，未经同行评审与独立复现）
target=通用 all-atom 框架：单体骨架优化、de novo 小分子与金属离子结合蛋白（cAMP/ATP/AD/胆酸/dolutegravir/色氨酸/Zn2+）、de novo PPI 结合剂（PD-L1、FGFR2）、RFdiffusion 失败设计拯救（PD-L1、IL7RA）、磷酸化特异性抗体（pS8-Aβ）与环肽/纳米抗体（后两者本地仅计算）
backbone_generation=不新造生成器：用 AF3 扩散模块的截断幻觉做结构更新（用户指定噪声水平，设计默认 150 步、默认 200 步、精修 50 步）与 ProteinMPNN/LigandMPNN 序列采样 + 自研 CoDP 排序交替迭代；仅前向、免微调免反传；真 from scratch 需把引擎换成 Protenix（带 ESM 嵌入）
computational_filters=五联 in-silico 成功率定义（蛋白 RMSD、蛋白 pLDDT、配体 RMSD、配体 pLDDT、ipTM）；回路内 pLDDT/pTM/ipTM 逐轮单调性；RMSD-to-origin 偏离度；交叉评估器 Protenix/Chai-1/Boltz1/AlphaFold-Multimer/ESMFold；口袋定义用 Fpocket；未用任何物理能量、MD、QM
thresholds=protein RMSD ≤ 1.5 Å；protein pLDDT ≥ 85；ligand RMSD ≤ 2 Å；ligand pLDDT ≥ 85；ipTM ≥ 0.85；扩散步数 150（设计默认 200，精修 50，低质骨架 100-200 步、通常 6-7 轮收敛，>300 aa 需更多）；基准图参考线 5 Å 与 2 Å RMSD；送测前排序阈值原文未给
md_used=否（本地全文对 molecular dynamics、GROMACS、OpenMM、AMBER、umbrella、metadynam、MM-PBSA/GBSA、free energy、explicit solvent 全部 0 次命中）
qm_used=否（quantum、DFT 0 次命中；无任何势垒、过渡态或反应坐标计算）
experimental_methods=E. coli 表达；ITC 测配体结合（每靶确认 ≥1 条）+ 口袋点突变竞争 + 交叉特异性（TRP vs Tyr/Phe、AD vs NE）；X 射线晶体学（cAMP 3.1 Å、AD 2.4 Å、Zn 1.6 Å、DTG 与 TRP apo 2.0 Å）；BLI 测 PPI 与抗体结合（抗体侧仅 1000 nM 单浓度对比磷酸化/非磷酸化 Aβ）
pipeline_counts=生成分母与中间淘汰数原文未给 → 配体侧每靶不足 16 条送测（7 个靶）；de novo PPI 每靶 16 条（PD-L1、FGFR2）；拯救实验 PD-L1 与 IL7RA 各 16 条（全部源自先前失败设计）；至多 1000 条 Chroma 低质骨架被优化（计算侧）
hit_rate=作者自述的末端投测命中率（分母全为自选的 16 条）：FGFR2 13/16 = 81.3%、PD-L1 8/16 = 50%、拯救 PD-L1 12/16 = 75%、拯救 IL7RA 8/16 = 50%；对照方 12/95 = 12.6% 与 32/96 = 33.3% 为 RFdiffusion 已发表数字非本文实测；in-silico 侧仅 小/疏水配体 > 60% 一档有数，大极性配体只说 considerably lower 无数字；整条管线成功率无法由本文复算
best_metric=K_D = 32 pM（PD-L1 最强结合剂，BLI，本地全文唯一明确亲和力数字）；拯救设计整体为 low nanomolar（无逐条值）；FGFR2 最佳值本地原文写作 digital nanomolar affinity，与二级底稿 sources/cao.md:317 的 sub-nanomolar 不一致，本卡以本地全文为准
cost_or_stat_note=本地全文未给任何算力单价（无 GPU-h/核时/每秒设计数），仅有定性表述 序列阶段比结构阶段高效、设计用 150 步以省算力；无 Methods 与表格，因此 BLI/ITC 参数、送测清单选取规则、生成与评估实现细节不可核；晶体仅 5 例；EGFR 纳米抗体与含 NCAA（AcrK，pLDDT 88.65 / 86.4）的环肽停在计算自评
role_in_timeline=曹龙兴组筛选逻辑转向的最直接证据：不再 生成大库→物理/置信度分数排序→投 10^2-10^3 个，而是把判定阈值（五联）与功能约束（配体位姿、模板、共价/NCAA、CDR 起点）前置进只前向的生成回路，使每靶只需投 16 个；分母从 10^4-10^5 缩到 16 正是 90%+ 类传闻的口径来源（与 C22、C23 同一转向；C20 为该框架的核酸外推）
source_pointer=data/literature_cards/fulltext/C19_PPR1116408_text.txt（SHA 1a68c94cc1b69271…，唯一逐字底稿）+ 同目录 fullTextXML.xml；sources/cao.md:305-320 与 :420/:480；fetch_log.tsv:134；batches.tsv 第 18 行；data/gate.json（Crossref 核验 OK）
CSV回填-->
