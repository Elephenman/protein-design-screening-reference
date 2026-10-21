# [B22] 抗体也能从头设计——但要付出「判据失灵 + 命中率 0–2%」的代价

Bennett N R, Watson J L, Ragotte R J, Borst A J, See D L, Weidle C, … Liu C C, Baker D（华盛顿大学 IPD + UCI + CHOP）
Nature 2025, 649:183-193（Crossref issued=2025，EPMC pubYear=2026）· DOI 10.1038/s41586-025-09721-5 · PMID 41193805 · PMCID PMC12727541
预印本 10.1101/2024.03.14.585103（PMC10983868）· 开放获取（CC BY 4.0）· https://pmc.ncbi.nlm.nih.gov/articles/PMC12727541/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B22**（组：Baker组; 通用方法学; 口径对照） |
| 本地全文①（本卡引句担保） | `data/interim/baker_lit/ft/antibodyRFdiff.txt`（89,767 B，SHA-256 `d3860fc89dde2e53…`，2026-10-16 抓取，标签剥离 + `scripts/litcards_text.py` 归一化） |
| 本地全文②（同文 JATS XML，独立通路） | `data/interim/claim_lit/PMC12727541.xml`（169,840 B，SHA-256 `d7876bc73c47f2cb…`）。**注意**：门禁按 `verify_literature_cards.py` 的规则排除 `.xml`，所以引句只在①上被机器核验；本卡另用同一 `to_text()` 归一化后在②上人工比对，结果见第 9 节 |
| 两通路互证结果 | 本卡 **37/37 条逐字引句在①与②两份本地全文里同时命中**（②用 `scripts/litcards_text.py` 的 `to_text()` 去标签后比对，与门禁同一口径） |
| 对照底稿 | `sources/baker.md:290-301`（原卡）；本卡在其基础上补：微调 RF2 的热斑依赖数字、OrthoRep 提升幅度、cryo-EM 各分辨率与逐 CDR RMSD、scFv 组合装架的聚类/文库规模约束、CAR-T 失败与「设计失败」判定的原文措辞 |
| 证据级别 | **全文级**（引句逐字命中本地全文；见第 9 节门禁结果） |
| 未取到的部分 | Methods 全在 Supplementary Information（本文件只有正文 + 图注 + Extended Data 图注），因此训练细节、SPR/展示实验参数、AF3 打分脚本参数均为「正文级描述、无阈值」；Supplementary Figs 1-16、Tables 6/10 未取 |

## 1. 这篇到底解决什么（大白话）

抗体发现一直是「免疫动物 / 筛随机文库 / 从病人身上拿」，计算方只能做第二步（拿到一条能结合的抗体之后再优化）。这篇要的是**第一步**：**只给靶子和表位残基，就把 CDR 环和停靠姿态凭空生成出来**。做法是把 RFdiffusion 在抗体复合物上微调（框架序列+结构作为条件、表位用 hotspot 特征指定、框架模板只给二维距离不给相对位置，于是停靠姿态也一并采样），序列端用 ProteinMPNN 只改 CDR；再用自己微调的 RoseTTAFold2 做自洽性过滤（因为当时 AF2 预测抗体-抗原不行、AF3 还没发布）。湿实验两条轨并行：酵母展示 9,000 条/靶，或 E. coli 表达 + 单浓度 SPR 95 条/靶。产出：VHH 到四个疾病相关表位、scFv 到 TcdB 与 PHOX2B-pMHC（六个 CDR 全是设计的），多个 cryo-EM 结构证明界面达到原子精度；亲和力靠 OrthoRep 从几十~几百 nM 推到个位数 nM。**同时作者明确承认命中率只有 0–2%，并给出改进判据（AF3 ipTM）的回顾性验证。**

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **通用 binder 生成器根本做不了抗体**。原文：**"these binders almost exclusively rely on regular secondary structure-based (helical or strand) interactions with the target epitope, and the original"**（下一句接着是 vanilla RFdiffusion network is therefore unable to design antibodies de novo，两句之间夹引文编号，故本卡只引前半）。→ **他们做了什么**：在抗体复合物上微调 RFdiffusion，把框架当条件输入、把表位当 hotspot 输入，并且**故意不输入框架-靶的相对位置**，让网络自己采停靠姿态（**"the framework structure is provided in a global-frame-invariant manner during training"**）。
2. **标准自洽性闸口（AF2）在这类分子上失灵**：**"In the case of antibodies, however, AlphaFold2 fails to accurately predict antibody-antigen structures"**，而项目开始时 **"AlphaFold3 (ref. 24 ) was not available"**。→ **应对**：自己微调 RF2，并在训练时**喂入设计阶段已知但常规预测拿不到的特权信息**（holo 靶结构 + 表位位置）。**代价**：这个闸口强依赖特权信息——热斑给满时 **"With mean pAE <10, 80.3% of structures are within"** 的样本占 80.3%（原文完整口径是 100% 热斑时 pAE<10 者有 80.3% 落在设计结构 2 Å 内），热斑只给 10% 时 **"with this falling to 52.6% when only 10% of hotspots are provided"**；作者自评 **"but the filtering power of this model is limited (at least with the settings used; providing 100% of interface"**（后半句是被引号包围的 hotspots，故本卡只引到它之前）。
3. **命中率塌到 0–2%**：原文写成功Rates 在 **"which range from 0% to 2%"**，并直接把低命中率和判据弱绑在一起：**"This probably accounts for the low experimental success rates and the inaccurate SARS-CoV-2 design"**。→ **应对（本文内没做完的部分）**：不是加更贵的物理模拟，而是**加便宜的高通量湿筛**（酵母展示 9,000/靶）+ **事后用 AF3 复盘该用什么判据**：**"We found that the AlphaFold3 interface predicted template modelling (ipTM) score, a measure of model confidence over the interface, is predictive of binding success (area under the curve = 0.86;"**，以及 **"Overall, only 9% of our ordered VHH designs have an ipTM > 0.6, suggesting that success rate will be improved by incorporation of an ipTM filter"**；scFv 侧 **"Only 4% of the initial design library has ipTM > 0.85, whereas 5 out of the 6 experimentally confirmed designs pass this threshold"**。**留下的代价**：这些是回顾性分析，前瞻命中率本文没有重测。
4. **初设计亲和力弱（几十~几百 nM）**，摘要口径：**"Although initial computational designs exhibit modest affinity (tens to hundreds of nanomolar K"**（后面紧跟的是上标 d 与闭括号，故只引到 K 之前）。→ **应对**：用 OrthoRep 连续超突变做亲和力成熟，**"Affinity-matured VHHs acquired several mutations relative to the parent designs and improved binding affinities by approximately two orders of magnitude"**，并专门用 cryo-EM 复核成熟后**结合姿态没跑**：**"indicating that OrthoRep maturation preserved the predicted mode of epitope engagement"**。
5. **scFv 是两个链、六个 CDR，单个环做错就全盘皆输，而基因合成撑不起这种规模**：**"The gene synthesis problem is more formidable for scFvs than for VHHs as they are too long to be simply assembled from pairs of conventional oligonucleotides synthesized on oligonucleotide arrays, and are challenging to uniquely pair due to high sequence homology between scFvs"**。→ **应对**：**结构感知的组合装架**——把同位点、同姿态、近似可叠合的设计聚成簇，簇内 H/L 随机重组：**"by mixing CDRs from different designs that bind in the same orientation, we can effectively overcome failures due to single imperfectly designed CDRs"**；工程约束写在图注：**"Hence, we limit ourselves to large subpools (>= 100 designs), which maximizes the combinatorial amplification for the amount of additional library assembly work"** 与 **"Gray lines indicate the TM threshold chosen for library assembly, where library sizes approximately match the transformation efficiency of yeast"**。对照组：**"By contrast, random, structure-agnostic pairing rarely led to predicted binders"**。**代价**：固定配对文库没出命中（**"but not the fixed pairing libraries"**，前半句是命中来自约千万复杂度组合库）。
6. **有一条设计「折叠对、表位对、但姿态错」**，作者把它判成失败而不是勉强算成功：**"Owing to the deviation between the designed dock and the experimentally determined dock, we classified this as a design failure."** 并补了两句解释（AF3 事后能正确预测该复合物，且实测姿态更接近 AF3 的回顾预测）：**"Had AlphaFold3 been used as an initial filter, this design would have been rejected due to the discrepancy between the predicted and intended structures"**。**应对的实质**：把失败案例转成「下一版判据应当长什么样」的证据。
7. **PHOX2B-pHLA 复合物本身不稳**（正文给 T m = 44.2 °C）→ **应对**：**"we leveraged a disulfide-stabilized approach to prepare a stabilized form of the pHLA target"**；拿到 400 nM（SPR）/1 μM（ITC）的 scFv 后接进 4-1BB-CAR，**"Attempts were made to incorporate scFv binders into a 4-1BB-CAR, but T cell cytotoxicity assays demonstrated no detectable killing of a range of neuroblastoma cell lines"**，作者归因：**"probably because of the modest binding affinity and/or low levels of antigen density expressed on the tumour cells"**。**本文未解决**（细胞活性这条线就此停下）。
8. **怕被质疑「模型只是背下了训练集」**：→ **加对照**：设计 CDR 与自然序列差异大，且 **"There was no correlation between training dataset similarity and binding success"**；TcdB 的 Frizzled 表位 **"There are no antibodies binding to this epitope in the PDB, hence, this success cannot be attributed to memorization."**
9. **cryo-EM 端的两个技术障碍**：① HA 上表位被 N296 糖链部分遮挡 → 用 occupancy 与 apo/holo 对比解释：**"identified approximately 66% of haemagglutinin particles bound to a maximum of two VHHs per trimer"**；② RBD 上下翻动导致信号平均 → 对称扩展 + 局部精修（正文描述，未给定量阈值）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **生成端**：在抗体复合物上**微调的 RFdiffusion**（文中直接称 RFdiffusion，代码库 RFantibody）。三个关键设置：① 框架序列 + 框架二维模板（pairwise 距离/二面角）作条件；② 框架模板不编码与靶的相对位姿 → 停靠姿态由模型采；③ 加 one-hot **hotspot（表位）**特征。
- **序列端**：ProteinMPNN **只改 CDR 残基**，框架不动。
- **过滤端（本文的痛点所在）**：**微调 RoseTTAFold2** 复测复合物，自洽口径 = 预测结构与设计结构 RMSD + pAE（图注给的是 RMSD < 2 Å、pAE <10 才算 RF2-approved）；正交用 Rosetta ddG 与 SAP。**AF3 只在事后被拿来复盘**。
- **湿筛双轨**：酵母表面展示（高吞吐）与 E. coli 表达 + 单浓度 SPR（低吞吐、给可溶性与绝对亲和力），时间成本作者直接标出：**"In this work, we used yeast surface display and/or E. coli expression with SPR for experimental validation (taking approximately 6 weeks and 2 weeks post-oligonucleotide order, respectively), and OrthoRep affinity maturation."**
- **亲和力成熟**：OrthoRep 体内连续超突变（展示库上做）。
- **结构确证**：cryo-EM（HA、TcdB、RBD）；SPR 竞争（用已结构确证的 de novo 小蛋白 AHB2 / FZD48 抢表位）；中和试验（CSPG4-KO Vero）。
- **没有用的方法**：MD、QM、自由能微扰。

### A. VHH 主线

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 靶结构 + 表位残基（用户指定） | 微调 RFdiffusion 生骨：框架固定、CDR 与 dock 一起设计 | 无阈值（生成步） | 每靶设计库（下单前规模未给；**"Design pipelines typically produce a wide range of solutions to any given design challenge"** 为定性描述） |
| A2 | 骨架 | ProteinMPNN 只出 CDR 序列 | 无 | 序列库 |
| A3 | 序列库 | 微调 RF2 复测（喂 holo 靶结构 + 100% 热斑） | **RF2-approved = 预测与设计结构 RMSD < 2 Å 且 pAE <10**（Extended Data Fig 3c/f 图注）；诊断口径：100% 热斑时 **"With mean pAE <10, 80.3% of structures are within"** 设计构象 2 Å 内 | 过滤后送测集合：**9,000 designs/靶**（酵母展示）或 **95 designs/靶**（E. coli+SPR） |
| A4 | 两轨送测 | 展示轨：多轮 FACS + NGS；直测轨：单浓度 SPR → 命中者滴度 | 逐靶成功率见 Supplementary Methods Table 6：**"which range from 0% to 2%"** | 28 条 VHH 经 SPR 确认结合（Extended Data Fig 1 图注）；最优：**78 nM**(HA)、**1.4 μM**(RSV site III)、**5.5 μM**(RBD)、**260 nM**(TcdB，Fig 2d；图注作 262 nM) |
| A5 | 命中的表位特异疑问 | SPR 竞争：先注已确证的 de novo 结合体（AHB2/FZD48）再注 VHH | 响应被清零 = 打在同一表位 | RBD 与 TcdB 均被完全竞争掉；TcdB VHH 对 70% 同源的 TcsL **无结合** |
| A6 | TcdB VHH | 中和试验 | EC50 | **460 nM**（CSPG4-KO Vero） |
| A7 | 初命中 VHH | OrthoRep 超突变 + 展示筛选 | 亲和力提升 | **"improved binding affinities by approximately two orders of magnitude"**，到个位数 nM/亚 nM |
| A8 | 代表设计（含成熟体） | cryo-EM 结构 | 与设计模型叠合 RMSD | HA：**3.0 Å**、VHH 骨架 **1.45 Å**、CDR3 **0.8 Å**；TcdB 母体 **4.6 Å**、成熟体 **5.7 Å**（刚体对接一致，姿态未变）；RBD 成熟体全局 **3.9 Å**/局部 ~2.5 Å → **姿态偏离，判为 design failure** |

### B. scFv / 全长抗体主线（六 CDR 的组合装架）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | TcdB Frizzled 表位、PHOX2B-HLA-C*07:02 | RFdiffusion 同时设计 VH 与 VL 的六个 CDR | 无 | 母设计集 |
| B2 | 母设计集 | 按 pairwise TM score 聚类（同位点同姿态者归一簇），簇内 H/L 组合；簇即 PCR 子池 | 子池下限 **>= 100 designs**；TM 阈值选在文库规模≈酵母转化效率（10⁷） | 组合库理论复杂度 **约 10 million**；固定配对库与组合库并行 |
| B3 | 组合库 | 酵母展示分选 → 挑取 → 表达纯化 → SPR | 展示富集 + SPR Kd | 命中来自组合库、**固定配对库 0 命中**；6 条 scFv 来自 2 个不同 dock；scFv5 **460 nM**、scFv6 **72 nM** |
| B4 | scFv | 转全长 IgG1 | Kd 是否保持 | scFv6→IgG1 **68 nM**、scFv5→IgG1 **380 nM** |
| B5 | scFv6 / scFv5 | cryo-EM | 逐 CDR backbone RMSD | scFv6：**3.6 Å**、双链复合模型 **0.9 Å**；CDRH1 0.4 / CDRH2 0.3 / CDRH3 0.7 / CDRL1 0.2 / CDRL2 1.1 / CDRL3 0.2 Å；scFv5：**6.1 Å** 刚体对接一致 |
| B6 | PHOX2B 靶 | 二硫键稳定化 pHLA + 组合装架 | SPR/ITC + R6A 点突变阴性对照 | 400 nM(SPR) / 1 μM(ITC)；对 PHOX2B(R6A) 无结合；CAR-T 杀伤：**未检出（本文未解决）** |
| B7 | 全部下单设计（事后） | AF3 重打分（靶给 MSA+模板，VHH 只给模板；scFv 取 10 seeds 最大 ipTM） | ipTM>0.6（VHH）、ipTM>0.85（scFv）；AUC **0.86** | 9% 与 4% 的通过率；scFv 6 条确认设计中 5 条过 0.85；结合体 ipTM 显著高于其母设计（p=0.0025） |

**这套流程的骨架值得单独记住**：生成端**把「未知的东西」交给模型采（dock、CDR）**，过滤端**在缺通用判据时自建一个带特权信息的判据**，湿实验端**用两条通量/成本不同的轨并行**，失败端**把设计失败显式记账并转成下一版判据的证据**。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处 |
|---|---|---|
| 0–2% | 逐靶实验成功率区间（Supplementary Methods Table 6） | "which range from 0% to 2%" |
| 9,000 / 95 | 每靶酵母展示 / E. coli+SPR 下单数 | Fig A3 段正文 |
| ~6 周 / ~2 周 | 展示轨与直测轨自下单起的时间成本 | Methods 概述段（Fig 1e 图注） |
| 78 nM、1.4 μM、5.5 μM、260(262) nM | 四个靶最优 VHH 的 Kd | Fig 2a-d 段与图注 |
| 460 nM | TcdB VHH 中和 EC50（CSPG4-KO Vero） | Fig 2d 段 |
| 70% | TcsL 与 TcdB 的同源性（特异性对照） | Extended Data Fig 4b 段 |
| ~两个数量级 | OrthoRep 带来的亲和力提升 | "improved binding affinities by approximately two orders of magnitude" |
| 80.3% / 52.6% | RF2 在 pAE<10 时预测落在 2 Å 内的比例（100% vs 10% 热斑） | Extended Data Fig 2c 图注 |
| RMSD<2 Å、pAE<10 | 被记为 RF2-approved 的设计口径 | Extended Data Fig 3c/f 图注 |
| 0.026 / 0.0003 | 微调 RF2 优于 IgFold 的整体/CDR H3 精度配对 t 检验 p 值 | Extended Data Fig 2f 图注 |
| 86 条抗体、2023-01-13、<30% | 外部测试集构建口径（避免训练集泄漏） | Extended Data Fig 2e,f 图注 |
| AUC = 0.86 | AF3 ipTM 回顾性判别力 | Extended Data Fig 10b + 正文 |
| 9% / 4% | 下单 VHH 中 ipTM>0.6 的比例 / scFv 初始库中 ipTM>0.85 的比例 | 正文「Improved oracles increase success rate」 |
| 5 / 6；p=0.0025 | 过 0.85 阈值的确认 scFv 数 / 结合体 vs 母设计 ipTM 差异 | 正文 + Extended Data Fig 10c |
| 3.0 / 4.6 / 5.7 / 3.9 / 3.6 / 6.1 Å | 各 cryo-EM 分辨率（HA、TcdB 母体、TcdB 成熟体、RBD、scFv6、scFv5） | Fig 3/5 图注与正文 |
| 1.45 Å、0.8 Å；0.9 Å | HA VHH 骨架与设计 RMSD、CDR3 RMSD；scFv6 复合模型 RMSD | 正文 + Fig 5 段 |
| 0.4/0.3/0.7/0.2/1.1/0.2 Å | scFv6 六个 CDR 的 backbone RMSD | Fig 5e,f 段 |
| ~66%、最多 2 VHH/三聚体 | HA 颗粒上 VHH 占据率 | Fig 3 段 |
| 10 million；10⁷；>=100 | scFv 组合库理论复杂度 / 酵母转化效率上限 / 子池下限 | Extended Data Fig 7b,c 图注 |
| 460 nM、72 nM；380 nM、68 nM | scFv5/scFv6 的 Kd 及转全长 IgG1 后 Kd | Fig 4d-i 图注 |
| 44.2 °C | PHOX2B-HLA-C*07:02 复合物 Tm（不稳定性来源） | 正文 PHOX2B 段 |
| 400 nM(SPR) / 1 μM(ITC) | PHOX2B scFv B1.2.1 亲和力 | 正文 + Extended Data Fig 8F 图注 |
| 28 | 经 SPR 确认结合的 VHH 总数 | Extended Data Fig 1 图注 |
| 10,897 movies；41,837 / 14,384 | scFv6-TcdB 数据量与结合/游离颗粒分选数 | Extended Data Fig 9 图注 |

## 5. 结论——作者说了什么

1. 把抗体结构的微调 RFdiffusion + 展示筛选 + 结构确证拼成一条线，**首次做出「结构被验证过的 de novo 抗体」**（作者原话口径：这是本文的贡献所在，即表位特异性设计，而不是「能不能做出结合体」）。
2. 设计精度到**原子级**：VHH 的 CDR3、scFv 的六个 CDR 的 backbone 与侧链旋转构象都与 cryo-EM 结构高度一致。
3. **表位可指**：多个表位在 PDB 里没有任何天然抗体（TcdB Frizzled 界面），因此成功不能归因于记忆。
4. OrthoRep 成熟**保留设计姿态**，把亲和力推到个位数 nM/亚 nM。
5. **成功率仍然很低（0–2%）**，主因是当时的过滤判据（微调 RF2）判别力有限；作者给出下一步判据（AF3 ipTM>0.6 / >0.85）及其回顾性证据，并承认 AF3 当时不可用。
6. 作者自列的待改进：生成架构与序列模型（人源性、免疫原性，OASis 分数偏低）、非蛋白原子（糖表位）、pHLA 线的亲和力与细胞活性。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **「判据失灵时，他们的第一反应是自建一个更差的判据 + 把湿实验通量拉高」**，而不是退回到更贵的物理模拟。这条对我们很关键：当结构自洽类判据在我们的目标上不成立时，可执行的是「造一个专用判别器 + 用便宜湿实验把量摊大」，而不是堆 MD 时长。
2. **自建判据的代价被量化了**：热斑给满→给 10%，80.3%→52.6%。**判据的性能依赖「设计阶段才知道的特权信息」**，这意味着它在真实使用（信息不全）时会系统性退化——我们在评估任何打分器时必须问「它假定我手里有什么」。
3. **「失败」可以被写成资产**：SARS-CoV-2 那条姿态错的设计，被用来论证下一版判据应当Reject它。→ 我们每个失败候选都该配一个「若用判据 X，它会被提前拒掉吗」的反事实检查。
4. **组合装架是「用结构相似性把独立子问题拼起来」**：单个 CDR 不完美会拖垮整体，就按「同姿态簇」内重组来分摊。→ 对我们：多步化学事件的候选设计，若每步都由独立模块贡献，可按「模块兼容簇」组合，而非要求单条序列一次做对全部。
5. **两条湿筛轨的差别是信息类型**：展示给群体级富集（适合大库、不给绝对 Kd），E. coli+SPR 给个体级绝对亲和力（只能做 95 条）。作者把 95/9,000 的分配当成预算决策来写，这与我们「每轮最多四个构建体」的约束同构——**先定轨、再定数量**。
6. **本文不提供任何「计算判据能预测催化」的证据**：全程无 MD/QM，且成功口径是结合而非转化。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：**"the experimental success rates remain low"**（0–2%）；RF2 过滤能力有限；AF3 复盘是回顾性的；设计序列人源性不足；pHLA 线无细胞杀伤；RBD VHH 被判为设计失败。
- 我们读出：① 逐靶命中数的绝对数很小（95 条轨里最多几条、9,000 条轨里 28 条合计），**0–2% 的分母决定了它不能外推**；② 展示轨与直测轨在同一个靶（HA）上都做过，但正文没有把两轨的「单位成本命中数」放在一起比较——效率口径要读者自己补；③ 「原子精度」由 RMSD 界定，样本是**已被选中且能表达的少数**，未对失败集做同等结构分析；④ 亲和力提升来自 OrthoRep（湿实验进化），不是计算迭代——**计算端贡献的是表位特异性，不是亲和力**。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **判据失灵时的处置顺序**（G0/G6）：先承认通用判据不适用（像他们承认 AF2 对抗体无效），再决定「造专用判别器」还是「改湿实验通量」；二者要同时写明代价（专用判别器依赖特权信息 → 部署环境信息不全时会退化）。
2. **把「设计失败」写成可反事实检验的类别**：每个失败候选注明「若用判据 X 是否会在下单前被拒」，并保留该样本做下一版判据的标定数据（我们的真值面板就是靠这个长出来的）。
3. **双轨下单预算**（G8 成本门）：一轨「群体级/大量/无绝对值」，一轨「个体级/少量/给绝对量」，按每候选成本与所能提供的信息类型分配名额，而不是全押一轨。
4. **兼容簇组合**：当功能由多个子模块共同贡献时，用「结构/机制兼容」聚簇后在簇内组合，降低单点失误的杀伤半径；并保留「随机组合」作对照（他们证明随机组合几乎不出预测命中）。
5. **成熟与判据解耦**：亲和力/活性可以靠进化或再设计在后端提升，前端判据只负责「选对结合对象」。这条允许我们把漏斗前端的目标收窄为「事件是否可能发生」，不背「做到高活性」的指标。

**不可迁移（为什么不能照搬）**

1. **AF3 ipTM>0.6/0.85、RF2 的 pAE<10 与 RMSD<2 Å 判的是「预测结构与设计的界面是否自洽」**，与「能否催化三步化学事件并避开副产物」无关；DP2R 标准 §2 禁止把 binder/抗体的 pAE/ipTM 阈值当酶活闸口。
2. **本文的 0–2% 是抗体 VHH/scFv 在结合读出下的数字**，且分母为 95/9,000 的特定分配，**不得作为我们的命中率预期**，更不许换算成「某法对 UAA 成功率 X%」。
3. **酵母展示 9,000 通量在产物化学上不存在**：我们不能把「把库摊大」当成同等解法，漏斗末端要靠信息量最大化（机制多样性 + 失活/竞争副产物对照）而非样本数。
4. **OrthoRep 式进化依赖展示读出**，我们的读出是 LC-MS/MS 产物身份，通量差两个数量级；迁移「亲和力成熟」这一环时只能迁「用误差校正文库代替从头再设计」的思想，不能迁方法本身。
5. **本文无 MD/QM/自由能**，因此它不能为「用 MD/QM 判催化」提供任何命中率背书（本文无该类主张也无该类数据）。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/antibodyRFdiff.txt

- 引句底稿: data/interim/baker_lit/ft/antibodyRFdiff.txt
- 两通路互证：37/37 条引句在①（txt）与②（JATS XML，`to_text()` 去标签）里同时命中。
- 本卡引句担保全文：`data/interim/baker_lit/ft/antibodyRFdiff.txt`（SHA-256 `d3860fc89dde2e53…`）。
- 第二通路（同文 JATS XML）：`data/interim/claim_lit/PMC12727541.xml`（SHA-256 `d7876bc73c47f2cb…`，抓取 URL 记于 `inventory.json` 的 B22 记录）。门禁按规则排除 `.xml`，故机器核验只在①上做；本卡另用 `scripts/litcards_text.py` 的 `to_text()` 对②做了同一套逐字比对：**37/37 条引句在①与②同时命中**。
- 对照底稿行号：`sources/baker.md:290-301`；汇总表相关行：`sources/baker.md:605`（3a 自洽闸口）、`610`（5a 高通量湿筛）、`612`（6 确证）、`618`（抗体/VHH 仍只有 0–2%）、`624`（OrthoRep 亲和成熟廉价化）。
- 代码与数据指针（原文）：GitHub `RosettaCommons/RFantibody`；抗体训练集 Zenodo 15741710；EMDB EMD-49373 / EMD-49405；PDB 9NFU / 9NH7；US provisional patent 63/607,651。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检命令**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B21 B22 B23 --no-report`（输入：本目录 `*.md` + `sources_map.json` 登记的底稿）。结果见回报。

<!--CSV回填
work_type=论文
target=RSV site I/site III、SARS-CoV-2 spike RBD、influenza H1 HA 茎部表位、C. difficile TcdB(Frizzled/DRBD 表位)、IL-7Rα、PHOX2B 肽-HLA-C*07:02 pMHC
backbone_generation=在抗体复合物上微调的 RFdiffusion（框架序列+二维模板作条件、框架-靶相对位姿不编码以采停靠姿态、one-hot hotspot 指定表位）；序列端 ProteinMPNN 只改 CDR；scFv 走 VH/VL 结构感知组合装架（TM 聚类，簇即 PCR 子池）
computational_filters=自微调 RoseTTAFold2 复测（喂 holo 靶结构 + 热斑），自洽口径 RMSD to design <2 Å 且 pAE<10；正交 Rosetta ddG、SAP；事后用 AlphaFold3 ipTM 回顾性复盘（AUC 0.86）
thresholds=RF2-approved：RMSD<2 Å、pAE<10（诊断：100% 热斑时 pAE<10 者 80.3% 落在 2 Å 内，10% 热斑降到 52.6%）；AF3 ipTM>0.6（VHH，9% 通过）与 >0.85（scFv，4% 通过）；组合文库子池下限 >=100 设计、TM 阈值使文库规模≈酵母转化效率 10⁷
md_used=否
qm_used=否
experimental_methods=双轨湿筛（酵母表面展示 9,000 设计/靶，约 6 周；E. coli 可溶表达 + 单浓度 SPR 95 设计/靶，约 2 周）→滴度 SPR 定 Kd；SPR 竞争（AHB2/FZD48 抢表位）与 TcsL 交叉对照；CSPG4-KO Vero 中和；OrthoRep 体内连续超突变亲和力成熟；cryo-EM（HA、TcdB、RBD、scFv）；pHLA 二硫键稳定化 + SPR/ITC + R6A 阴性对照；4-1BB-CAR 神经母细胞瘤杀伤试验（失败）
pipeline_counts=每靶 9,000（展示）或 95（直测）经计算过滤后的下单量 → VHH 共 28 条 SPR 确认（逐靶成功率 0–2%）→ OrthoRep 成熟若干条；scFv 组合库理论复杂度约 10⁷ → 6 条 scFv（来自 2 个 dock 簇）→ 2 条转全长 IgG1；固定配对文库 0 命中
hit_rate=逐靶 VHH 实验成功率 0%–2%（Supplementary Methods Table 6）；scFv 6 条确认设计里 5 条过 AF3 ipTM>0.85；作者自评低命中率主要归因于微调 RF2 过滤能力有限；本文未给改进判据的前瞻命中率
best_metric=VHH：HA 78 nM、RSV site III 1.4 μM、SARS-CoV-2 RBD 5.5 μM、TcdB 260 nM（图注 262 nM）；OrthoRep 成熟至个位数 nM/亚 nM 且姿态不变；scFv6 72 nM（转 IgG1 68 nM）、scFv5 460 nM（IgG1 380 nM）；PHOX2B-HLA-C*07:02 scFv 400 nM(SPR)/1 μM(ITC)；TcdB 中和 EC50 460 nM
cost_or_stat_note=两条湿筛轨的时间成本由作者明写：展示≈6 周、E. coli+SPR≈2 周（自寡核苷酸下单起）；结构确证：HA 3.0 Å（VHH 骨架 1.45 Å、CDR3 0.8 Å）、TcdB VHH 4.6/5.7 Å、scFv6 3.6 Å（复合模型 0.9 Å，六 CDR backbone 0.2–1.1 Å）、scFv5 6.1 Å；AF3 复盘：VHH 仅 9% 下单设计 ipTM>0.6、scFv 初始库仅 4% ipTM>0.85；一条 RBD 设计被判为 design failure
role_in_timeline=把 [B09]/[B08] 的「结构自洽性闸口」推到它失灵的一类分子（抗体/CDR 环）上：作者被迫自建判别器（微调 RF2）并量化其退化（热斑依赖），命中率塌回 0–2% 后用两招补——高吞吐展示库（借 [B06] 的口径）与误差校正文库 OrthoRep 亲和成熟；同时给出下一版判据（AF3 ipTM>0.6/0.85）的回顾性证据，是「判据缺位→靠湿实验通量兜底」的最完整案例
source_pointer=data/interim/baker_lit/ft/antibodyRFdiff.txt（SHA d3860fc89dde2e53…）+ data/interim/claim_lit/PMC12727541.xml（SHA d7876bc73c47f2cb…，门禁不核验 xml）；sources/baker.md:290-301
CSV回填-->
