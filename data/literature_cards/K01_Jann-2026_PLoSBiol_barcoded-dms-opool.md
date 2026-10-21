# [K01] 用芯片寡核苷酸池 + 两步克隆搭建带条形码的 DMS 文库——把"大基因突变扫描太贵"变成成本工程问题

Jann G, Gagnon-Arsenault I, Pageau A, Dubé AK, Fijarczyk A, Durand R, Landry CR（拉瓦尔大学）
PLoS Biology 2026, 24(2):e3003645 · DOI 10.1371/journal.pbio.3003645 · PMID 41671286 · PMCID PMC12923136
开放获取（CC BY 4.0）· 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12923136/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K01**（组：通用方法学; 口径对照；该行 `文献类型` 现填 价目表，但本文实体是**方法学论文**，成本数字只是它的论证之一——本卡按论文口径写，成本口径单独在 §4/§7 拆清） |
| 本文取回方式 | Europe PMC 检索后取 fullTextXML（`fetch_channel`: epmc_search_then_fulltext），DOI 10.1371/journal.pbio.3003645 |
| 本地全文 | `fulltext/K01_PMC12923136_fullTextXML.xml` → 去标签纯文本 `fulltext/K01_PMC12923136_text.txt`（157,044 字符；含正文 + 图注 + Supporting information 图注/表注 + **公开审稿往来全文**） |
| 对照底稿 | `sources/cost-benchmarks.md` §一（该行证据类型标注为 论文实测＋引厂商价目）；同一目录 K02（Twist 挂价）、K04（GenScript oPools 报价）是**厂商价目快照**，与本文数字不同口径，见 §7 |
| 证据级别 | **全文级**（本卡所有引句均可在上面那份纯文本里逐字命中；§9 有自检） |
| 未取到的部分 | S1–S10 Table、S1–S14 Fig 的原文件（仅有图注文字）、S1–S9 Data 数值表、厂商实际报价单。凡引用这些处本卡明写 仅有表注/图注文字，无原始数值 |

## 1. 这篇到底解决什么（大白话）

DMS（深度突变扫描）要一次把某个基因里**每一个氨基酸位点换成全部 20 种氨基酸**，靠的是简并密码子（NNK）合成池。基因越长，要合成的序列越多、要把每个突变和它的条形码配对所需的测序越贵，所以长基因基本做不动。这篇做的事：不追求"一条长分子上同时带着突变和条形码"，而是**在芯片合成 oligo 池的那一步就让突变与条形码物理连在同一根 DNA 上**，之后用普通克隆（Gibson + Golden Gate）拼回质粒，只在克隆后用便宜的短读测序**一次性建立条形码-突变对照表**，从此下游只看条形码。于是长读测序（PacBio/Nanopore 配对）被换成"便宜的芯片池 + 便宜的短读测序"，作者用酵母 3.2 kb 的多药转录因子 PDR1 全部 43 个片段做了一遍，并在其中一个片段 F13 上跑完 POSA（泊沙康唑）抗性筛选，证明条形码读数与直接读突变序列的结论几乎一致。

它是一篇**方法/成本工程**论文：没有任何蛋白设计漏斗、没有结合力判据、没有催化判据。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **基因长度直接卡死成本**（问题的起点）。原文：全文级难点描述 "Gene size limits DMS scalability due to the complexity of the variant library and the associated synthesis and sequencing costs, including for linking variants to DNA barcodes." 又说测序便宜了但仍然不够："Although the cost of high-throughput sequencing has steadily declined over the past 20 years, the large size of many target genes makes the cost of such experiments prohibitive."
   **应对**：把目标基因切成芯片能合成的短片段再拼装——"Our approach involves fragmenting a gene of interest" + "into subregions of up to 150 base pairs (bp), in accordance with the synthesis length limits of single-stranded oligonucleotide pools (oPools)."；实际把 PDR1 切成 43 段，"the 3,204 bp PDR1 gene was divided into 43 fragments of 75 bp each, except the last one which is of 54 bp."
   **代价**：片段数 = 独立的文库数 = 独立的长 PCR 数，工程量线性上升（见第 8 条审稿人意见）。

2. **条形码与突变必须在同一个分子上，否则短读测序认不出谁是谁**。原文把它们的做法写成卖点："Each degenerate codon variant is physically associated with multiple DNA barcodes during synthesis, which overcomes the need for long-read sequencing for linking variants to barcodes."
   **应对**：合成时就把 barcode 与变异片段排在同一条 oligo 上；再在 Gibson 之后**立刻测序**建立关联表——"a necessary short-read sequencing using PBS_i5" 加 "is performed to associate each barcode with its corresponding mutation and to assess both barcode diversity per mutation and mutation coverage for the whole fragment"（两句之间原文插了 5′ 引物的括号说明，本卡拆成两条引句），Golden Gate 只测条形码确认没丢。
   **代价 / 未解决**：Reviewer #2 追问"如果不做这步关联测序、直接相信 oPool 的设计序列，错误率是多少"，**本文未解决**（正文只给了"关联测序后"的读数）。

3. **每一步克隆都会丢多样性，导致某些突变只剩 1–2 个条形码**（内部重复数不足→噪声）。现象：原文自述 "As each cloning step inevitably results in some diversity loss"。
   **应对**：用**加大转化子数**硬扛。Gibson 步目标 ~25,000 个转化子/片段（换算 ~350 transformants/bp），Golden Gate 步再翻 4 倍到 ~100,000 个/片段（"the number of transformants recovered after Golden Gate assembly was increased 4-fold (~1,400 transformants per bp)."）；操作上不是做更大的一次转化，而是**每个片段跑多管并行反应再合并**（Gibson 2 管 + ~5 次转化；Golden Gate 2 管 + ~10 次转化），事后把菌落全部刮下合并。指标随之达标：Gibson 后 "This level of recovery yields 300-350 informative barcodes covering all possible mutations, with over 99.8% of mutations represented by #barcodes >4 and over 97.0% by #barcodes >9"；Golden Gate 后 "our cloning strategy ensured over 99.8% of mutation coverage and preserved high barcode diversity: over 93.6% of mutations were still covered by #barcodes >4, and over 68.6% by #barcodes >9"。
   **代价 / 未解决**：需要的转化子数**随片段而变、作者没解释**。Reviewer #3 第二轮仍指出："In contrast, F43 suggests that ~150 transformants would suffice. This sizable difference deserves discussion. What accounts for the discrepancy?" 本文正文没有给出解释——**本文未解决**。

4. **芯片 oligo 池是单链、且合成会截断**，不完整产物直接进克隆会污染文库。
   **应对**：把"单链→双链"的两步 PCR 做成有偏置的纯化流程——"The first PCR consisted of a single cycle using only the reverse primer (PCR4)." 然后 "Amplicons were purified using magnetic beads at a bead:DNA ratio of 1.8 to enrich for full-length oligonucleotides and to minimize the incorporation of truncated sequences"，第二 PCR 限量循环（"involving both forward and reverse primers and limited to five cycles to reduce PCR-related errors"），并且 "Each oPool amplification was performed in four replicates, which were pooled after the second PCR to maximize the diversity of variants carried into downstream cloning steps."
   **代价**：仍然有合成 dropout——全基因 43 库合并分析显示 Nearly all expected mutations 只到 ~98,4%，"with only a few absent positions likely attributable to synthesis dropout in the oPools."；另有 "absent representation (19 codon positions in the entire PDR1 gene: S5 - S8 Figs )" 的位置完全缺失。作者把它们归因于合成而非克隆，但没有补救手段。

5. **载体里自带 BsaI 位点会拆掉 Golden Gate**。现象：目标基因 PDR1 与载体上有 3 个 BsaI 位点，而 Golden Gate 全靠 BsaI。
   **应对**："As a BsaI restriction site is used in the construction of the PDR1 DMS plasmid library, we had to remove three BsaI restriction sites in pRS31N- ScPDR1 ." 具体 "The three sites were mutated by site-directed mutagenesis (site 1) or by homologous recombination with a short double-stranded DNA fragment (gBlock)"（site2/3 用一段 2238-2720 的 gBlock 替换）。
   **代价**：每个新基因都要先做一轮"去位点 + 重造模板"的前处理；本文只给了 PDR1 一个基因，**没有给这套前处理在其它基因上的成功率（本文未记录）**。

6. **想要的阴性背景（完全敲除内源基因）做不出来**。现象（作者自述失败并改道）："We chose this approach after observing low transformation efficiency when attempting to transform a yeast strain harboring a complete PDR1 deletion."
   **应对**：不换菌株思路，改成**条件压制**——"we replaced its endogenous promoter with a DOX-repressible promoter (tetO7). This allowed inhibition of genomic PDR1 expression and complementation by plasmid-encoded variant libraries."（用 yTHC 库的 KANMX-tetO7 盒替换 chrVIII:121683-121733 的 50 bp 上游区），并加 mEGFP 融合做表达开关的验证。
   **代价**：内源基因不是零表达，Reviewer #3 由此怀疑抗性位点上的**阳性/中性读数可能来自泄漏**（stop codon 出现"轻度负"而非"强负"选择系数）——本文对此只做了部分回应。

7. **NNK 简并天生不均一**：氨基酸的同义密码子数不同 → 条形码数与读数不均。
   **应对**：把"均一性"补成**第四个质量参数**（这是审稿人 #1 要求加的）——"Variant uniformity (i.e., how evenly individual variants are represented within the library), ensuring balanced abundance and accurate quantitative comparisons"，并用 Gini 系数与文献 [28] 的 uniformity score 量化："Overall, uniformity remained high across all 43 fragments (Gini coefficients consistently <0.5)."；下游分析再按同义密码子取中位数聚合。
   **代价 / 未解决**：作者自己承认偏置不是同义密码子数能解释完的——"codon-level analyses revealed that synonymous codon multiplicity alone does not fully explain the observed patterns"，且 "Certain codons rich in thymine or guanine (e.g., TTT, GGG, TGG, TTG) consistently showed higher barcode diversity, while others were underrepresented"（Pro/Thr/Ala 偏低）。机理**本文未解决**。

8. **建库时不做 PCR 偏置控制，也没有把 43 个子库混合筛过**。
   **应对（作者自述的局限与说明）**：测序建库用复孔合并防取样瓶颈，但承认 "Although this approach ensures robust amplification of the library and sufficient sequencing depth, it does not directly account for potential amplicon sequencing biases." 并给出补救方向 "Incorporating Unique Molecular Identifiers (UMIs) during PCR when preparing sequencing libraries would help mitigate the possible occurrence of such biases."——本卡记为**本文未做**（只在 discussion 里点到）。
   **代价（审稿人指出、本文未解决）**：Reviewer #3 反复要求真做 pool 实验："In my view, a complete validation of the proposed approach should demonstrate that a pool of sub-libraries can indeed be successfully screened. Without pooling, barcoding brings little added value"；并记录作者的回答是"以前成功混过子库，所以这里不必再证"——"In their response, the authors suggest that because they have successfully pooled sub-libraries previously, there is no need to demonstrate the effectiveness of pooling here." 审稿人反驳："I am not asking for a full gene-scale pool, but rather a small number of pooled regions"。**最终本文仍未给出混合子库的功能筛选数据**。

9. **卖点里的成本数字撑不住**（本卡最要紧的一条，与 §4/§7 直接相关）。
   **应对**：作者的原文只有一句转引——"This strategy utilizes the economical oPools, which are ~100-fold cheaper per base than double-stranded DNA synthesis (<$0.001 versus ~$0.05 per base)"，后面挂的是文献 [22, 23]（两篇方法学章节/综述），**不是本实验室的采购账单**。
   **代价（审稿人原话，被期刊全文公开）**：Reviewer #1："My suggestion is to remove the cost comparison or to greatly strengthen the rigor behind the claims"；"the claims behind the numbers are not well sourced and cannot be independently verified"；"Second, the cost comparison presented here omits time and labor requirements of the method, which appear to be quite substantial."；"In my opinion, the quality of the paper does not rest on an economic argument." 作者没有撤掉这句成本比较，只是补了与 Twist 逐密码子建库的**均一性**对照（见 §4 末行）——**人工/时间成本仍未量化，本文未解决**。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **生成端**：芯片法单链简并 oligo 池（oPools），每片段每密码子一条 NNK 变体；条形码 = 两段 12 bp 固定块 + 6 个随机 N（位置特异性条形码，不是全随机）。
- **克隆端**：Gibson  assembly（把 oPool 插入线性化酵母表达载体）→ Golden Gate/BsaI 一锅法（把缺失的 3′ 端、终止子、PBS_i5 补回来）。
- **读出端**：Illumina NovaSeq 6000 S4 短读（PE 100/150），两个共用结合位点 PBS_i5/PBS_i7 让建库只剩一次 PCR；分析用自家 gyōza（Cutadapt + PANDAseq + VSEARCH），条码模式与密码子模式各跑一遍互为对照。
- **结构侧**：AlphaFold 3 预测 Pdr1 用于**结果可视化**（"As no experimentally determined structure was available for Pdr1 in the Protein Data Bank (PDB, RCSB), we used the AlphaFold 3 server"，pTM = 0.72），不参与任何筛选判据。
- **没有用的方法**：无 MD、无 QM、无结合力/亲和力测定、无蛋白设计漏斗；表型只有酵母 pooled competition 的生长富集。

### A. 建库（芯片池 → 43 套条形码质粒库）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| A1 | S. cerevisiae PDR1 CDS | 按芯片合成上限切段，每段一条 NNK 简并密码子 | 片段上限 150 bp（芯片单链池长度限制）；简并位总数上限 9：3 给 NNK + 6 给条形码 | 43 个片段（75 bp/25 密码子，末段 54 bp）；每池 25 条序列；每条 oligo 186-258 bp |
| A2 | 全部 12-nt 条形码序列（公开 Python 脚本穷举） | 过滤 + 拼接成 30 bp 条形码 | 保留 30,000 条：GC 40-60%、Hamming distance 3；再剔除含 BsaI 位点者、剔除首尾同碱基重复者；两段合成后总 GC ~50% | 30 bp 条形码 = 12 bp + NN + 12 bp + NN + 12 bp 结构 + 6 个 N；库容量 30,000 |
| A3 | 单链 oPool | 两步 PCR 转双链 + 磁珠纯化 + 复孔合并 | 第一轮只加反向引物、单循环；bead:DNA 1.8（富集全长）；第二轮限 5 个循环（压 PCR 错误）；每池 4 复孔合并 | 每片段一份双链插入库，量供后续克隆 |
| A4 | pRS31N-ScPDR1（含启动子 834 bp + CDS 3,207 bp + 终止子 345 bp） | 去除 3 个 BsaI 位点（site1 定点突变，site2/3 用 2238-2720 gBlock 同源重组）；PCR 产物 DpnI 1 h30 @37 °C | 载体与基因内 BsaI 位点数 = 0（否则 Golden Gate 自切） | 模板质粒 pRS31N-ScPDR1 WT |
| A5 | A4  backbone（PCR6 线性化）+ A3 插入池 | Gibson：每片段 2 管 10 μL 并行 + 约 5 次化学转化，平板上直接加 5 mL 2YT 刮菌合并 | 目标 ~25,000 转化子/片段 ≈ 350 transformants/bp | 43 套 Gibson 中间质粒库；达标读数：每突变 300-350 个有效条形码、>4 条形码覆盖 99.8%、>9 覆盖 97.0% |
| A6 | A5 的每片段质粒库 | 建库三段 PCR（PCR9/10 扩增"突变片段+条形码"并加 i5，稀释 1:1,000 后 PCR11 加 index，3 复孔合并）→ NovaSeq | 起始 20 ng 质粒；测序深度 ~250 reads/期望变异；过滤：丢长度不符/多突变/条形码异常/缺碱基的读段；覆盖 <2 reads 的突变丢弃 | F13 保留 >60% 读段、F43 保留 >80%；产出条形码-变异关联表 + 覆盖/多样性指标 |
| A7 | A5 库（作载体）+ 补 3′ 端 amplicon（PCR7，两端加 BsaI，含终止子与 PBS_i5） | Golden Gate 一锅法：每片段 2 管 20 μL + 约 10 次转化，同样刮菌合并 | 目标 ~100,000 转化子/片段 ≈ 1,400 transformants/bp（相对 Gibson 4 倍） | 最终 43 套全长 PDR1 单突变条形码质粒库；覆盖仍 99.8%，>4 条形码 93.6%、>9 68.6% |
| A8 | A5/A7 两次测序数据 | 均一性与 QC：Gini + 90/10 百分位对数差的 uniformity score；非编程变异计数；6 个库做全长质粒测序 | Gini <0.5 判为可接受（全 43 片段一致）；单条读段（singleton）丢弃 | 全库 Gini ~0.32；WT 读段 ~10%、双突变 ~10%；6 个质粒 "No unintended mutations were present in the PDR1 promoter, coding sequence, or terminator regions." |

### B. 功能筛选（只有 F13 这一个片段做了完整 DMS）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| B1 | S. cerevisiae R1158 | 用 KANMX-tetO7 替换 PDR1 内源启动子（50 bp 上游，chrVIII:121683-121733），G418 200 μg/mL 筛选；mEGFP 融合 + 流式确认开关 | 放弃全敲除株（转化效率低）；DOX 10 μg/mL 压制 | ScPDR1-DOX 菌株（原文：We chose this approach after observing low transformation efficiency when attempting to transform a yeast strain harboring a complete PDR1 deletion.） |
| B2 | A7 的 F13 库 | 醋酸锂逐个片段转化进 B1，每片段回收约 100,000 菌落，刮菌合并、OD₆₀₀=80 分装冻存 | 原文阈值：每片段 ~100,000 菌落以保证覆盖与条形码多样性 | 酵母内 F13 条形码库（起点约 ~10,000 cells/variant） |
| B3 | B2 库 | pooled competition：YPD + NAT 100 μg/mL + DOX 10 μg/mL ± POSA；对照加 0.1% DMSO；两轮 OD 0.05 → 0.80 生长 | POSA 0.40 μg/mL（抑制 ~50% 野生型生长的浓度）；两轮共约 8 个有丝分裂代 | TP0 / TP1 / TP2 三个时间点各 5 个 OD₆₀₀ 单位的样 |
| B4 | B3 各点提质粒 | 同时建两种库：直接测 F13 突变区（PCR18 M13 先只扩 PDR1）与只测条形码；NovaSeq PE150 | 每期望变异 ≥500 reads（F13 ~0.4 M reads/样，条形码 ~4 M reads/样）；TP1 未测（4 代之内频率变化太小） | TP0/TP2 × 两种读法的测序集（SRA BioProject PRJNA1269095） |
| B5 | B4 读段 | gyōza 密码子模式 + 条形码模式；TP0→TP2 折数变化除以代数，再减去沉默变异中位数归一 | 高置信变异阈值：TP0 每条核苷酸序列 ≥5 reads；同义密码子取平均聚合 | 525 个单氨基酸变异的**选择系数**表（resistant/sensitive 按 0.6 到 -0.6 分档） |
| B6 | 两套选择系数 | 交叉验证条形码推定 vs 直接读突变；再按"每变异需要几个条形码"做 1-10 档、每档 100 次随机重采样 | 全条形码 r = 0.97；4 个条形码时 r = 0.91；不一致者 8/525 | 结论级指标：r 值曲线（Fig 2C）；本卡把它当作"条形码可替代直接测序"的证据强度 |

**这套流程的骨架值得单独记住**：它的可复用资产不是某条阈值，而是**一次性的"条形码-突变关联表"**——建好之后，同一个库在任意条件下都能只读条形码复测。与 B09 那张卡对照：B09 的漏斗难点在计算端，本文的漏斗难点全在**湿实验建库端**，而且它的"判据"（覆盖度、条形码多样性、Gini）都是**文库质量指标，不是变体的功能判据**。

## 4. 关键数字台账（数值 · 含义 · 出处；末列区分 本文实测 / 转引）

| 数值 | 含义 | 出处（正文位置/原句片段） | 性质 |
|---|---|---|---|
| 150 bp | 芯片单链 oligo 池的分段上限（设计约束） | in accordance with the synthesis length limits of single-stranded oligonucleotide pools | 转引（合成工艺通识） |
| 75 bp / 54 bp / 43 段 | PDR1 实际切段与文库数 | the 3,204 bp PDR1 gene was divided into 43 fragments of 75 bp each, except the last one which is of 54 bp | 本文实测 |
| 3,204 bp vs 3,207 bp | 同一基因两处不同长度（分段口径 vs 插入片段 CDS） | 正文 Methods 两处；本卡记为原文内部不一致 | 本文实测 |
| 1,068 aa | Pdr1 蛋白长度（说明为何传统法做不动） | a large protein of 1,068 amino acids, whose comprehensive mutagenesis would have been financially and technically challenging | 本文实测 |
| 9 = 3 + 6 | 每条 oligo 简并位预算（NNK 3 位 + 条形码 6 位） | Current oligonucleotide synthesis technologies allow for a total of nine degenerate positions per fragment | 转引（合成工艺限制） |
| 30,000 条 / GC 40-60% / Hamming 3 | 条形码库筛选口径 | From these, 30,000 barcodes with a GC content between 40 and 60% and a Hamming distance of 3 were selected | 本文实测 |
| 186-258 bp | 每条 oPool 序列总长 | for a total of 186-258 bp per oPool | 本文实测 |
| bead:DNA 1.8 / 5 cycles / 4 复孔 | 单链→双链的偏置控制参数 | Amplicons were purified using magnetic beads at a bead:DNA ratio of 1.8；limited to five cycles to reduce PCR-related errors | 本文实测 |
| ~25,000（~350/bp） | Gibson 步每片段目标转化子数（第一道闸口） | To reach a target of ~25,000 transformants per fragment；~350 transformants per bp are needed to optimize sufficient informative barcode, mutation coverage, and barcode diversity | 本文实测（经验拐点） |
| ~100,000（~1,400/bp，4×） | Golden Gate 步目标转化子数 | the number of transformants recovered after Golden Gate assembly was increased 4-fold (~1,400 transformants per bp) | 本文实测 |
| ~150/bp | F43 显示所需转化子远低于 F13，作者未解释 | In contrast, F43 suggests that ~150 transformants would suffice. This sizable difference deserves discussion.（Reviewer #3 第二轮，本文正文未答） | 审稿读数 |
| 99.8% / 97.0% | Gibson 后 #条形码>4 / >9 的突变覆盖 | with over 99.8% of mutations represented by #barcodes >4 and over 97.0% by #barcodes >9 | 本文实测 |
| 99.8% / 93.6% / 68.6% | Golden Gate 后覆盖、>4、>9 | over 93.6% of mutations were still covered by #barcodes >4, and over 68.6% by #barcodes >9 | 本文实测 |
| 98.3% / 71.7% | 表现最差的 F13（残基 322-324）局部读数 | they still showed high mutation coverage (98.3%) and acceptable barcode diversity, with 71.7% of mutations with #barcodes >4 | 本文实测 |
| ~98.4% / ~97.5% / ~95.4% / ~0.32 | 全部 43 库的覆盖与均一性汇总 | were recovered, with only a few absent positions likely attributable to synthesis dropout in the oPools；after Gibson assembly, ~97,5% mutations were represented by #barcodes >4, and after Golden Gate assembly this remained true for ~95.4% of positions；Gini coefficient ~0.32（原文小数用逗号写法 98,4/97,5/95,4） | 本文实测 |
| <0.5（全 43 片段） | 均一性可接受判据 | Overall, uniformity remained high across all 43 fragments (Gini coefficients consistently <0.5) | 本文实测 |
| 19 个密码子位点 | 整个 PDR1 里完全缺失的位置（归因合成 dropout） | absent representation (19 codon positions in the entire PDR1 gene: S5 - S8 Figs ) | 本文实测 |
| ~10% WT / ~10% 双突变 | 非编程变异占比（下游可剔除或做上位性分析） | We additionally quantified the representation of non-programmed variants and found that ~10% of reads corresponded to the WT sequence and ~10% to double-mutants | 本文实测 |
| >60% / >80% | 读段过滤后保留率（F13/F43） | After filtering, more than 60% and 80% of all reads were retained for F13 and F43, respectively | 本文实测 |
| <2 reads 丢弃 / ≥5 reads 高置信 | 两级读段计数阈值 | Mutations with coverage of less than two reads were discarded；A minimum threshold of five reads per nucleotide sequence was used to define high-confidence variants | 本文实测 |
| ~250 / ≥500 reads/期望变异；~0.4 M / ~4 M reads/样 | QC 与功能筛选的测序深度 | Libraries were sequenced at an average depth of ~250 reads per expected variant；All samples were sequenced to achieve a minimum of 500 reads per expected variant | 本文实测 |
| 16 管 × 5,000/7,500 转化子 × 100 次随机排序 | 图 1B 那条"转化子数-质量"曲线的构造方式 | To measure the impact of combining results from multiple transformations (16 reactions, each with 5,000 (F13) or 7,500 (F43) transformants), we calculated the cumulative % of different metrics across all transformations sorted in a randomized manner | 本文实测（重采样，非独立实验） |
| POSA 0.40 μg/mL；DOX 10 μg/mL；NAT 100 μg/mL；8 代；~10,000 cells/variant | 筛选条件与库深度起点 | 原文作 POSA was used at a final concentration of 0.40（单位在原文为 μg/mL），后接 corresponding to the concentration that inhibits approximately 50% of WT growth；DOX/NAT 浓度见 Pooled competition assay 段 | 本文实测（浓度口径转引自本组前作 [5]） |
| r = 0.97（全部条形码）/ r = 0.91（4 个条形码）；8/525 不一致 | 条形码推定 vs 直接测序的一致性 | The estimates from the barcodes or from the F13 coding region were strongly correlated ( r = 0.97, all available barcodes, S13 Fig )；Only a few discrepancies between barcode- and sequence-based estimates were observed (8 out of 525 mutations), most of which involving mutations supported by few barcodes | 本文实测 |
| pTM = 0.72（AlphaFold 3） | 仅用于把 DMS 结果映射到结构，非筛选判据 | As no experimentally determined structure was available for Pdr1 in the Protein Data Bank (PDB, RCSB), we used the AlphaFold 3 server | 本文实测（单条预测，无置信区间） |
| **<$0.001/base vs ~$0.05/base，约 100 倍** | 芯片 oligo 池 vs 双链基因合成的每碱基价 | This strategy utilizes the economical oPools, which are ~100-fold cheaper per base than double-stranded DNA synthesis (<$0.001 versus ~$0.05 per base) 后面挂文献 [22, 23] | **转引，非本文实测**（本文没有采购单、没有报总账单；见 §7） |
| 77% / 69%（SUNi 两库） | 对照方法的突变覆盖率 | the authors report substantially lower coverage, with 77% and 69% of mutation coverage for two independent libraries | 转引（文献 [28] 的数字） |
| Gini ~0.52 vs 本方法 | 与逐密码子 Twist 合成建库的均一性对照（S7 表注） | The CaERG11 library was constructed using a highly precise, low-throughput method: DNA fragments synthesized by Twist Bioscience were cloned codon-by-codon into a yeast expression vector；The comparison indicates that the uniformity achieved by our barcoded strategy is certainly less efficient than the CaERG11 reference, but it is perfectly acceptable for robust DMS experiments (Gini coefficient around 0.52) | 本文实测（但 0.52 归属哪一侧，表注文字有歧义，见 §7） |

## 5. 结论——作者说了什么

1. 他们把长基因 DMS 建库做成了**便宜且可扩展**的路线："In summary, we developed an efficient, scalable, and cost-effective two-step cloning strategy for the construction of high-quality, barcoded DMS plasmid libraries for genes of any length."
2. 条形码推定与直接测序**几乎等价**："We demonstrate a near-perfect correspondence in the measurement of amino acid variants impact when assessed by barcode sequencing and direct sequencing of the mutated coding sequence."（定量即 r = 0.97；4 个条形码时 r = 0.91）
3. 质量指标达标：99.8% 突变覆盖、>4 条形码的内部重复、43 个片段 Gini 一致 <0.5。
4. 与 SUNi / Jones-Howard / DIMPLE 的差异被他们定位为**成本与条形码自由度**：近完整覆盖（99.8%）优于 SUNi 的 77%/69%，比 DIMPLE 便宜且能在合成时就把条形码挂上（indels 本文没做，只说他们的旧工作 [30] 支持 oPool 做 indel 库）。
5. 生物学交付：PDR1 F13 的 525 个变异的选择系数图，residues 301-312 富集获得抗性突变、313-324 作用有限，且与已报道的 T304N、I307S、M308I、R310S 等一致。
6. 作者的收口立场："This approach reduces both technical and financial barriers, facilitating its broader application across diverse gene sizes, biological systems, and experimental contexts."

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文真正的杠杆是"把一次性配对成本前置"**：关联表在 Gibson 后建一次，之后所有条件下只读条形码。→ 对我们：任何需要重复测同一批构建物的实验（多个反应条件、多个底物组合），值得把"身份确认"做成一次性的资产，而不是每轮重测；这与我们把每个候选的 LC-MS/MS 判定重复到每一轮的做法是相反的成本结构。
2. **"内部重复"是本文最可迁移的概念**：一个氨基酸变异挂 300 多个条形码，本质是用**同一标签的多次独立实现**换取噪声估计。→ 对应我们：同一构建体做多次独立反应（不同批酶、不同起始 OD）比同批复孔更接近这个逻辑；我们现在只有同孔重复，估不出批间噪声。
3. **它的"99.8% 覆盖率"是文库覆盖度，不是命中率**——分母是"应该存在的突变数"，而不是"有功能的候选数"。这个区别对我们极重要：我们习惯把"某条判据通过 90%"读成"90% 成功"，而本文没有任何一个数字是功能成功概率。
4. **最贵的一步被藏在工程里**：n 个片段 = n 次长 PCR + n 次并行 Gibson + n 次并行 Golden Gate。审稿人算得很直白："The major disadvantage of their method is in the need for n separate long-length PCRs to generate the linearized DNA for Gibson assembly in step 1 (here n is the number of tiles)."→ 我们若把任何"多构建体并行"当省钱方案，必须把 n 次前处理的人力写进单价，否则和本文的成本主张犯同一个错。
5. **他们靠"直接测序那条路"来证明便宜路线可信**（Fig 2 上半区是直接测序，下半区才是条形码推定）。→ 教训：便宜代理指标要挂一个贵但少量的金标准做校准，我们的机制层读数（LC-MS/MS、xTB 剖面）应当扮演那个金标准，只跑少量样本，而把大批量交给便宜的序列/结构代理。
6. **本文没有交付任何亲和力、产量或催化数**，因此它对我们的"能测到什么程度"没有先验贡献，只贡献了**建库/复用/内部重复**的工程方法学。

## 7. 局限与失败（作者的 + 审稿人的 + 我们读出的）

**作者自己承认的**：
- 不做 UMI，承认可能有扩增偏置（见 §2 第 8 条两句原话）。
- 只做了 1 个基因、只完整功能筛选了 1 个片段：正文里 F13/F43 之外的 41 个片段只给建库质控，"Although the main text presents in detail only the characterization of the mutant libraries for two representative PDR1 fragments (F13 and F43)"。
- 全长质粒测序只做了 6 个库，其余没做，理由是成本："Although pre-sequencing of all PCR-amplified fragments prior to Golden Gate assembly could further ensure accuracy, it was not performed here due to cost and scalability considerations."
- 没有 indels（只有 NNK 替换）。
- TP1 被舍弃，理由本身承认数据不够："TP1 was excluded, as the limited frequency changes observed after just four generations hindered robust genotype-phenotype associations."

**审稿人指出、期刊公开、本文未解决的**（同一份全文里带公开审稿记录，逐句可查）：
- 范围与标题不匹配："Specifically, the authors did not demonstrate the method on multiple genes; did not create a barcoded full length saturation NNK library of their gene of interest; and did not perform a deep mutational scan on the full-length gene."
- 混合子库的功能筛选从未实证（§2 第 8 条引文）。
- 人工与时间是成本论证的缺口："Second, the cost comparison presented here omits time and labor requirements of the method, which appear to be quite substantial."；"43 of these reactions is quite a molecular biology load, and would scale unfavorably as you increase the length of YFG."
- 数字来源不可独立核验："the claims behind the numbers are not well sourced and cannot be independently verified"。
- 条形码位置特异性设计**没有与全随机条形码做过保真度对比**："Do the authors have any evidence that this scheme leads to higher fidelity variant-barcode associations compared with fully random barcodes?"
-  assays 的内部重复性未报："what is the internal reproducibility of the assay (barcode vs. barcode or tile vs. tile)?"——**本文只有条形码 vs 直接测序的一致性，没有生物学重复之间的一致性**。
- F13 与 F43 所需转化子数差 2 倍以上未被解释（§2 第 3 条）。

**我们读出的（推断）**：
1. **成本数字的口径必须分三层引用**：①本文的实测只有"覆盖率/条形码多样性/均一性"这类文库指标；②`<$0.001 per base` 与 `~$0.05 per base` 及"约 100 倍"是**转引文献 [22, 23]**（Kuiper 2022 Chembiochem、Maciá Valero 2025 Methods Mol Biol，二者本身也是引厂商价的二手口径），作者没有给出自家采购单、通量或折扣；③本目录 K02（Twist 12 ¢/base 起价）、K04（GenScript 1K-8M oligos/池 From $800）是我们自己抓的**厂商挂价快照**，与①②既不同年、不同供应商、也不同分母（per base vs per pool）。三者不可连乘成"每候选美元"，任何这样算出来的数字必须在 `run.md` 标为 本报告推算。
2. **S7 表注的 Gini 0.52 归属不清**：正文另一处给全库 Gini ~0.32、判据 <0.5；表注那句 "The comparison indicates that the uniformity achieved by our barcoded strategy is certainly less efficient than the CaERG11 reference" 紧跟 "but it is perfectly acceptable for robust DMS experiments (Gini coefficient around 0.52)"，读者无法确定 0.52 是本方法还是 Twist 金标准（若为本方法则与 ~0.32 冲突）。本卡不替作者仲裁，记为歧义，引用时只可说 存在 <0.5 与 ~0.52 两个读数。
3. **阳性对照体系有泄漏嫌疑**（stop codon 未给强负选择系数），所以 F13 那张抗性图的**绝对值**不能当作定量参考，只能当作"与文献突变一致"的定性确认。
4. 全文没有 MD/QM/催化层内容，AlphaFold 3 只出现在可视化里；它**不能**为"结构预测可判功能"提供任何命中率先验。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"内部重复"的实现方式**：同一功能单元挂多个独立可辨识标签，用标签间的离散度直接给出技术噪声。→ 用于我们：每个候选反应做**独立批次重复**（不同酶批、不同 Day 制备的底物），把"读数离散度"变成可报的量，而不是只报一次 LC-MS/MS 峰面积。
2. **把身份确认做成一次性资产**（条形码-突变关联表逻辑）：我们做一次"构建体序列 ↔ 产物谱"的金标准配对（LC-MS/MS + 全长测序），之后各条件只读便宜代理；这与本文 A6→B4→B6 的关系同构。
3. **质量指标与功能指标分离**：本文所有覆盖率数字都是"文库做出来没有"，不是"突变有没有功能"。→ 我们的漏斗也必须先给"每条 S0/S1/S2 反应有没有可检出的产物信号（检测覆盖率）"，再给命中率；两者混写就是本文 §4 那种台账要避免的错误。
4. **"n 份前处理要写进单价"**：本文的隐性成本是 43 次长 PCR/克隆；我们对应的成本是"每个构建体的克隆+验证次数"。任何方案对比里，`通过率 ÷ 单价` 的分母要把 n 次前处理的人力/机时算进去（沿用 B09 卡的效率口径）。
5. **失败可归因到具体工艺环节**（dropout vs 克隆效率 vs 覆盖度），本文靠"位置特异性条形码能反查片段与位置"这一设计做到的。→ 我们给每个候选标注"卡在合成/克隆/表达/化学哪一环"时，需要类似的可回溯标识（构建体编号 + 制备批次 + 反应批号三位一体）。

**不可迁移（为什么不能照搬）**

1. **它的判据是文库质量，不是功能判据**：99.8% 覆盖、>4 条形码、Gini<0.5 都不含"这个变体有没有活性"的信息。DP2R 判定标准禁止用这类"文库指标"充当酶活闸口；把它们写成 UAA 的支持证据属于口径替换。
2. **表型只有生长富集**，读出是"选择系数"，来自抗药性这一**可被生长救回的**表型；UAA 合成酶的产物化学事件（S0/S1/S2、pppUA、竞争副产物）在酵母里没有对应的生长读出，因此本文的 pooled competition 不能直接搬到我们的检测端。
3. **成本锚不能当概率用**：<$0.001/base 只是"每碱基买多少"，且本文这条是转引（见 §7.1）。它只能进"能不能做得起"这一栏，绝不能进"某条候选有多可能成"这一栏，也不能反过来用 K02/K04 的挂价去换算本文的覆盖度。
4. **展示库/突变库的通量数字与本项目的样本量不可比**：本文一个片段就 525 个变异、酵母库 ~100,000 菌落；我们一轮最多几个构建体。所以本文的统计功效（中位数、重采样 100 次、≥5 reads 阈值）在我们的小样本上全部不成立，不能照搬任何阈值或显著性口径。
5. 本文无 MD、无 QM、无结构判据；AlphaFold 3 pTM 0.72 只用于画图，**不能**引用为"结构预测支持功能推断"的证据。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K01_PMC12923136_text.txt

- 本地纯文本：`fulltext/K01_PMC12923136_text.txt`（Europe PMC fullTextXML 去标签、HTML 实体解码、未改写内容；同一论文在本目录只登记这一份可读全文，另一份 `K01_PMC12923136_fullTextXML.xml` 是 XML 源，门禁按规则不参与逐字比对）。
- 该编号在 `sources_map.json` 里还登记了 `sources/cost-benchmarks.md`（价目侧底稿），本卡引句**只以那份 txt 为准**；§7.1 的三层口径划分同时对照该 md 的第 16 行。
- 本文件含**公开审稿记录**（Decision Letters / Reviewer #1-#3 / author responses）——§2 第 3、8、9 条与 §7 的审稿人引句都出自这部分；它们不是作者正文，本卡在行文里逐条标了说话人。
- CSV 字段映射：§3 ↔ 候选生成方法/计算筛选判据/阈值数字；§4 ↔ 候选数递减/成本统计引用；§5-§6 ↔ 在方法演进链的位置。注意 CSV 该行 `文献类型` 现为 价目表，本卡 §0 已标注与论文口径的差异。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K01" --no-report`，结果见本轮回报；引句全部先经脚本按同一 `norm`（NFC + 实体解码 + 引号/破折号统一 + 空白折叠）逐字命中后才写盘。

<!--CSV回填
work_type=论文（方法学/资源类，PLoS Biol 2026 24(2):e3003645；CSV 该行现标 价目表 不准确，成本数字仅为转引口径）
target=酵母 PDR1（3.2 kb、1,068 aa 多药转录因子）的完整单氨基酸替换 DMS 文库；功能筛选只做 F13（残基 301-325，525 个变异）的泊沙康唑抗性
backbone_generation=芯片单链简并 oPool（每片段 75 bp/25 密码子、每池 25 条 NNK 变体、含 30 bp 位置特异性条形码 + PBS_i7）→ 两步 PCR 转双链 → Gibson 插入线性化 pRS31N-ScPDR1 → Golden Gate/BsaI 补 3 端与 PBS_i5；酵母株用 KANMX-tetO7 压制内源 PDR1
computational_filters=无计算漏斗；文库质量指标为 有效条形码数/突变覆盖率/条形码多样性(>4、>9)/均一性（Gini 与 90-10 百分位对数差）+ 读段过滤（长度、多突变、条形码异常、缺碱基、<2 reads 丢弃）；AlphaFold 3 仅用于结果可视化，pTM 0.72
thresholds=片段≤150 bp（芯片合成长度限制）、简并位≤9（NNK 3 + 条形码 6）；条形码库 GC 40-60% 且 Hamming 距离 3、共 30,000 条；Gibson 目标 ~25,000 转化子/片段 ≈ ~350/bp，Golden Gate ~100,000/片段 ≈ ~1,400/bp（4 倍）；QC 深度 ~250 reads/期望变异、功能筛选 ≥500 reads/期望变异；高置信变异 ≥5 reads/序列；可接受均一性 Gini<0.5（实测全库 ~0.32，另一处读数 0.52 归属有歧义）；一致性判据 4 个条形码时 r>0.9
md_used=否
qm_used=否
experimental_methods=磁珠纯化 PCR（bead:DNA 1.8）、E. coli NEB 5-alpha 化学转化（Gibson 2 管×约 5 次、Golden Gate 2 管×约 10 次转化/片段）、定点突变/gBlock 去 BsaI 位点、Sanger 与 Oxford Nanopore 全长质粒测序（6 个库）、Illumina NovaSeq 6000 S4 PE100/150、酵母锂乙酸转化（~100,000 菌落/片段）、POSA 0.40 μg/mL 与 DOX 10 μg/mL 下的 pooled competition（TP0/TP2，约 8 代）、gyōza Snakemake 流程（Cutadapt/PANDAseq/VSEARCH，密码子模式与条形码模式互校）
pipeline_counts=PDR1 CDS 3,204 bp → 43 片段（75 bp×42 + 54 bp×1）→ 每池 25 条 oligo（186-258 bp/条）→ 43 套 Gibson 中间库（各 ~25,000 转化子，F13/F43 QC 用 25,000 与 100,000 转化子对照）→ 43 套最终条形码质粒库（各 ~100,000 转化子）→ 仅 F13 转入酵母（~100,000 菌落，起点 ~10,000 细胞/变异）→ 525 个变异的选择系数
hit_rate=不适用（本文无功能命中概率）；给的是文库指标：Gibson 后 >4 条形码覆盖 99.8%、>9 覆盖 97.0%；Golden Gate 后 99.8%/93.6%/68.6%；全 43 库覆盖 ~98.4%、>4 条形码 Gibson ~97.5%、Golden Gate ~95.4%；19 个密码子位点完全缺失；WT 读段 ~10%、双突变 ~10%；条形码推定与直接测序一致性 r = 0.97（全部条形码）与 0.91（4 个条形码），不一致 8/525
best_metric=未记录（本文不测亲和力/催化效率，最硬读数只有 r = 0.97 的方法一致性与选择系数 0.6 至 -0.6 的分档热图，无单个最佳变体的定量值）
cost_or_stat_note=芯片 oPool <$0.001/base vs 双链 DNA 合成 ~$0.05/base、约 100 倍——此三个数字为本文转引其文献 [22, 23]（Kuiper 2022 Chembiochem；Maciá Valero 2025 Methods Mol Biol），非本实验室采购实测；Reviewer #1 明写 remove the cost comparison ... not well sourced and cannot be independently verified 且 omits time and labor requirements；本文实测的只有文库指标与建库参数（43 片段 × 各 ~25,000/~100,000 转化子、~250/≥500 reads/变异）；与 K02（Twist 12 ¢/base 起价）、K04（GenScript From $800/池）分母与年份不同，不可连乘换算每候选美元
role_in_timeline=在"展示库→条形码 DMS"这条湿实验成本线（DMS 侧）上的关键工程节点：把条形码与变异在同一根合成 oligo 上连锁，从而用短读测序替代长读测序做基因长度无限的条形码 DMS 建库；它是本表 <$0.001/base 口径的论文来源（K02/K04/K05 为该口径提供厂商价目与成本拆解，但那些数字不来自本文）；同时也标出这条路线的隐性代价（n 段 = n 次长 PCR 与 n 套并行克隆，混合子库从未实证）
source_pointer=data/literature_cards/fulltext/K01_PMC12923136_text.txt（Europe PMC fullTextXML 抽取，含正文/图注/表注/公开审稿记录）+ sources/cost-benchmarks.md §一 第 16 行；原文 DOI 10.1371/journal.pbio.3003645；代码 Zenodo 10.5281/zenodo.18342596；测序 SRA PRJNA1269095
CSV回填-->
