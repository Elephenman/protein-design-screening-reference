# [B15] RFpeptides：把 de novo 漏斗套在"化学合成"的环肽上——筛完还得能被合成出来才算数

Rettie S, Juergens D, Adebomi V, Bueso YF, Zhao Q, Leveille AN, … Baker D, DiMaio F, Bhardwaj G（华盛顿大学 IPD + Tufts + Düsseldorf/Julich + MIT）
Nature Chemical Biology 2025, 21:1948–1956 · DOI 10.1038/s41589-025-01929-w · PMID 40542165 · PMCID PMC12643943
开放获取（CC BY 4.0）· 全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC12643943/ （前身 bioRxiv 2024.11.18.622547）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B15**（组：Baker组; 口径对照） |
| batches 状态 | **FULLTEXT**（`data/literature_cards/batches.tsv` 第 4 批） |
| 本地全文①（唯一参与引句比对） | `data/interim/baker_lit/ft/macrocyle2025.txt`（97,345 B，2026-10-16 抓取，Europe PMC fullTextXML 去标签纯文本） |
| 本地全文②（原始 XML，门禁不比对） | `data/interim/claim_lit/PMC12643943.xml`（180,736 B；核验脚本 `srcs` 明确排除 `.xml`，故本卡引句只需在①命中） |
| 对照底稿 | `sources/baker.md:198–209`（原卡），本卡在其基础上补：单体环肽生成侧的自洽性口径（pLDDT/2.0 Å/MaxCluster TMscore 0.5）、MCL1 的 1,984 中间数与 RF2 正交复预测的取舍、RbtA 的"只用两法一致区"策略、合成失败率（13/27、3/11）、结晶换同源体的应对、事后 MSA 重预测 |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中；见第 9 节） |
| 未取到的部分 | Supplementary Sections 1–5、Figs 1–59、Tables 1–10（含每个靶的指标分布图 S4、逐条设计-亲和力排名表 1b/2b/3b/4b、完整计算脚本）。凡涉及这些的地方本卡明写"正文未给出数值，仅有正文描述" |
| 与 CSV 既有字段的差异 | CSV `thresholds` 写"iPAE<0.13 / <0.3 / <0.4（按靶点调）"——正文核实：GABARAP 0.13、MDM2 0.3、RbtA 0.4，MCL1 **未给具体 iPAE 数值**（只有"on the basis of the confidence metric"）；CSV `cost_or_stat_note=未记录` 与正文一致（本文没给 GPU/CPU 秒单价） |

## 1. 这篇到底解决什么（一句话+大白话）

环肽结合体过去只有两条路：要么从**万亿级**随机肽库里捞（展示筛选，控制不了结合模式），要么用物理法设计（只能借已知结合伙伴当锚点，亲和力弱、实验结构和设计模型经常对不上）。这篇把 RoseTTAFold2 与 RFdiffusion 的相对位置编码改成**环状**（cyclic relative position encoding），得到能生成环肽骨架的 RFpeptides，然后回答一个很实在的问题：**每个靶只合成不超过 20 条环肽，能不能拿到中到高的亲和力？** 结果四个靶（MCL1、MDM2、GABARAP、RbtA）全部命中，其中 GABARAP 6 nM、RbtA 9.4 nM，并有三个 X 射线共晶结构与设计模型 Cα r.m.s.d. < 1.5 Å。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **现成扩散模型不能直接做环肽，而从零训一个新模型又没有数据**。作者写明："Developing analogous methods for peptide design from scratch has been challenging because of the limited availability of experimental data for training such models"。 **应对**：不换赛道，改现有网络——给 RF2 加环状相对位置编码，先在**已知天然环肽结构**上验证可不可用（"observed robust prediction of natural cyclic peptide structures"，正文注明结果在 Supplementary Fig 1），确认后再把同一编码搬进架构相似的 RFdiffusion 做骨架生成。
2. **为什么不用已经能预测环肽的 AfCycDesign 直接做结合体设计（它其实是"幻觉"式设计的天然候选）**：作者算了这笔账——"de novo binder design with AfCycDesign as is would be far more computationally expensive and has not been successfully implemented or experimentally validated"。 **应对**：把 AfCycDesign **从生成器降级为事后过滤器**（只用来复预测设计好的复合体、给 iPAE），生成端交给 RFdiffusion；同时给出四条选型理由（RFdiffusion 的高实验成功率可迁移、可用它的 hotspot/motif 条件生成、可迁移到后续全原子模型）。
3. **筛完还是太多，超出化学合成预算**（本文最关键的工程矛盾）。MCL1 一轮：DL 侧过阈后仍有 "the 1,984 selected designs at this stage were still more than the number of designs we could reasonably synthesize and test experimentally"。GABARAP 一轮：物理+DL 双筛后仍有 335 条。 **应对（三条不同的路，按靶子情况换）**：① MCL1 加**第二套正交网络**——用 RF2 再复预测一遍，只保留两套网络预测一致的设计（"the design models predicted identically by two orthogonal structure prediction networks (AfCycDesign and RF2) should have a higher likelihood of binding to the target as designed"），再叠 Rosetta 物理项；② MDM2 **省掉** RF2 这一层，理由是两套网络结果本来就一致（"we chose not to do any additional filtering with RF2 as the results between AfCycDesign and RF2 were fairly consistent"）——即"过滤器若不提供新信息就不该占预算"；③ GABARAP 用**结构聚类**降样本数：**"Instead of trying to synthesize and characterize all 335 cyclic peptides (which would have required substantial time and experimental resources), we clustered the 335 designs into 80 different clusters"**，再从簇里取代表（最终只合成 13 条）。
4. **化学合成环节大量掉样，这是 binder 论文里通常不存在的瓶颈**。MCL1：*"the yields for the correctly cyclized product for 13 designs were low and insufficient for further characterization"*（27 条里 13 条拿不到物料，只剩 14 条进 SPR）；MDM2：**"Three of the selected designs had poor yields during the cyclization step of the chemical synthesis, preventing further experimental characterization with them"**（11 条里 3 条卡在环化步骤）。 **应对**：不设"合成前预测产率"的判据（本文没有这类模型），只做**事后剔除**——能拿到 >90% 纯度的才进入生化表征；RbtA 一轮干脆按可用物料报数（"Four of 11 designs that were synthesized in sufficient quantity and purity showed a binding signal at 100"，即 11 条里只有部分量/纯度够，够的里面 4 条有信号）。 **代价（本文未解决）**：计算筛子的通过率与湿实验可测样本数之间存在**无法预测的漏损**，正文没给"为什么这些序列环化不出来"的任何机理或指标。
5. **阈值不是一个常数，换了靶就换数字**。作者自陈："the distribution of such metrics varies substantially across the four selected targets and adjustments to filtering thresholds were required"；MDM2 一节写得更具体："We also adjusted the filter thresholds for in silico filters as their overall distribution differed substantially from the distribution observed for MCL1"。 **应对**：按靶调 iPAE 上限（GABARAP 0.13 / MDM2 0.3 / RbtA 0.4）与 ddG 上限（-30 / -50 kcal mol），把阈值当"该靶分数分布上的分位点"用而非物理常数。 **代价**：新靶没有历史分布，阈值只能靠预实验摸（本文承认"Integration with high-throughput methods in the future should enable testing of more designs and inform absolute threshold values"）。
6. **打分排序 ≠ 亲和力排序**（漏斗内部一致但外部失准）："the relative ranking within the selected designs does not perfectly match the experimental binding affinities"；具体地，MDM2 与 RbtA 的最强结合体 iPAE 排在前二，但 **MCL1 与 GABARAP 的命中不在前三名之内**。 **应对**：本文没解决（只在结论里提出未来结合高通量数据定绝对阈值）；实验侧的补救只是"最强者再做 X 射线/AlphaScreen 确认"，不回头修打分函数。
7. **没有实验结构的靶（只有预测结构）能不能做**：RbtA 是 ESKAPE 病原 *A. baumannii* 的表面蛋白，"There are no experimentally determined structures available for this protein and sequence-based searches against the Protein Data Bank (PDB) did not return notable matches to other protein structures"。 **应对**：AF2 与 RF2 各预测一遍，只在**两法几乎一致且高置信**的区域设计（"we decided to focus our binder design calculations on regions that were predicted nearly identically and with high confidence by AF2 and RF2"；两法整体 Cα r.m.s.d. 0.4 Å over 509 residues，pLDDT>90）；事后用新解出的 apo X 射线结构回验预测结构（Cɑ r.m.s.d. 1.2 Å/1.1 Å）。→ 拿到 K_d 9.4 nM。
8. **结晶做不出来时换同源体，而不是放弃结构验证**："we did not obtain crystals of sufficiently high quality for GAB_D8 bound to GABARAP"。 **应对**：改结晶 GABARAPL1，并给出可接受的量化理由——"a homolog of GABARAP with 86% overall sequence identity and 100% sequence identity for residues within 5 Å of GAB_D8 in the design model"（界面 5 Å 内 100% 同一）。 **代价**：验证的是同源复合物，不是原靶复合物。
9. **单序列预测在环肽上有系统偏差**。设计阶段所有复合体都是**单序列**输入预测的（CSV 记录与正文一致）；作者在拿到 X 射线结构后回头补测："These MSA-based predictions of the designs matched even more closely with the X-ray crystal structures"（GAB_D8–GABARAPL1 与设计模型 1.2 Å → 0.5 Å；GAB_D23–GABARAP 1.7 Å → 0.9 Å）。 **应对**：只作为事后分析（正文没把 MSA 重预测写进漏斗），承认为"漏斗用单序列"这件事付的精度代价。

## 3. 方法与工作流程（可复现顺序）

### 用了哪些方法（工具箱，以及文中给出的选型理由）

- **生成端**：RFdiffusion + **环状相对位置编码**（对环肽链的相对位置索引在越过半环时由正切负；靶链与链间保持标准编码）→ 本卡记为 RFpeptides。作者选 RFdiffusion 而非幻觉法，理由见第 2.2 条。
- **序列端**：ProteinMPNN（作者理由："We chose ProteinMPNN for its improved performance in sequence design and ability to generate sequences with better solubility profiles over the sequences generated by traditional physics-based methods"）；单体自洽性检验里用 **LigandMPNN**（每骨架 8 条序列）。骨架→序列的迭代用 **ProteinMPNN + Rosetta Relax 交替**（正文：MCL1 走"four iterative rounds"），作者对迭代的预期是"the local changes to the generated backbone during the Rosetta Relax steps to allow for improved amino acid sequence diversity from the ProteinMPNN steps"。
- **评估端（漏斗判据）**：① **AfCycDesign**（改造过的 AF2，带环状位置编码）复预测复合体 → **iPAE**（interface predicted aligned error，链间平均 PAE，正文另有"normalized iPAE"口径）+ 设计模型与预测模型的 r.m.s.d.；②（仅 MCL1）**RF2 正交复预测**；③ **Rosetta 物理项**：ddG（算得结合亲和力）、SAP（空间聚集倾向）、CMS（界面接触分子表面积）。Methods 一句话概括整条链："Macrocyclic peptide monomers and binders were designed with RFpeptides using a three-stage pipeline: backbone generation using RFdiffusion with the cyclic offset applied to the peptide chains, followed by sequence design using ProteinMPNN and, finally, structure prediction of the designed peptide-target complexes"，并且"Designs were further filtered and downselected using Rosetta metrics and, in some cases, clustered on the basis of Cα r.m.s.d."。
- **实验端**：Fmoc 固相多肽合成 + 分子内环化 + RP-HPLC 纯化 + MS 定性 → 生物素化靶 + SPR **单周期动力学**筛选（100 µM 有信号算命中）→ 亲和力测定（九点单周期）→ 竞争式 AlphaScreen（IC50）→ X 射线共晶（**用设计模型直接做分子置换相位**，见 Methods："The X-ray crystal structure was determined by MR using the designed model for phasing by Phaser"）。
- **没有用的方法**：MD、QM/电子结构、自由能微扰；本文全程不含。也没有做任何库筛选（无展示库、无 mRNA display），这一点是它与"传统环肽发现"的正面分野。

### A. 生成器自身的标定（Fig 1b,c；先证明"环状编码"有效，再上靶）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | RF2 权重 + 改造的环状相对位置编码 | 复预测已知天然环肽结构 | 正文只写"observed robust prediction of natural cyclic peptide structures"，逐条数值在 Supplementary Fig 1，**正文未给阈值** | 判定：编码可用，继续 |
| A2 | RFdiffusion + 环状编码 | 单体环肽骨架生成（无靶） | 无 | 每个长度各生成 48,000 条骨架；"we observed 9,045 and 8,913 structurally unique 10-residue and 12-residue backbones, respectively, when 48,000 macrocycle backbones were generated for each size" |
| A3 | 生成的单体骨架 | 每条骨架用 LigandMPNN 出 8 条序列，AfCycDesign 单序列复预测，看能否折回设计构象 | 图注口径：**"predicted by AfCycDesign to refold with pLDDT > 0.8 and within 2.0 Å backbone r.m.s.d. of the designed structure"**（每长度 n = 200） | 自洽率按长度报告（数值在图内）；另用聚类口径复算："as calculated using MaxCluster 35 , 36 at a TMscore threshold of 0.5" |
| A4 | phi/psi 分布 | 检查生成骨架是否需要大量 d-氨基酸才能稳定 | 与天然蛋白 Ramachandran 分布比较（定性） | 结论原句："suggesting that generated backbones do not require extensive d -amino acids to stabilize the generated structures" |

### B. 四个靶的设计战役（同一骨架流程，阈值按靶调）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 MCL1 | 高分辨 X 射线结构起始（作者："given the availability of multiple high-resolution X-ray crystal structures available to initiate the design calculations"）；**不设 hotspot** | 生成骨架 → ProteinMPNN+Rosetta Relax 四轮迭代（每骨架 4 条序列）→ AfCycDesign 复预测 | "We selected the designs on the basis of the confidence metric"（iPAE + 设计-预测相似度）；**iPAE 具体数值正文未给** | **9,965** 条骨架 × 4 = ~40,000 模型 → 过 DL 阈 **1,984** |
| B1a | 1,984 条 | **加第二套正交网络 RF2 复预测**（只保留两套网络一致者），再上 Rosetta 物理项 | Rosetta ddG / SAP / CMS（正文未给 MCL1 的具体阈值） | → 选 **27** 条送合成："we selected 27 designs for synthesis, biochemical and biophysical characterization" |
| B1b | 27 条基因 | Fmoc SPPS + 环化 + HPLC | 纯度 >90%；环化产物量与纯度够 | **13 条产率不足被剔** → **14** 条进 SPR |
| B1c | 14 条 | SPR 单周期动力学（生物素化 MCL1） | 100 µM 有结合信号 | **3** 条命中；最佳 MCB_D2 = **2 µM**；X 射线 2.1 Å，界面对齐后环肽 Cα r.m.s.d. **0.7 Å**（单独对齐环肽 0.4 Å） |
| B2 MDM2 | 已有结构；p53 TAD 结合沟 | 生成 16–18 aa（适合化学合成的长度）骨架 × 4 序列 | "AfCycDesign predicted 7,495 of the 40,000 design models to bind MDM2 with high confidence"（normalized iPAE < 0.3）；再 "we identified 17 designs with iPAE < 0.3, ddG < -50 kcal mol -1 , CMS > 300 Å 2 and SAP < 35" | **10,000** 骨架 → **40,000** 模型 → **7,495**（iPAE）→ **17** → 按 ddG 取前 **11** 送合成（跳过 RF2 层，理由见 2.3②） |
| B2b | 11 条 | 合成 → SPR | 环化失败 3 条 → 8 条可测 | **3** 条有信号；最佳 MDB_D8 = **1.9 µM**；三条命中共享 F/W + L/M  motifs |
| B3 GABARAP | 结构是 α 螺旋 + β 链混合沟（与前两靶的全 α 沟不同）；**定义 6 个 hotspot**（Lys46/Lys48/Tyr49/Leu50/Phe60/Leu63） | 骨架数翻倍 → 序列设计 → 双筛 → **结构聚类** | "Of the resulting 80,000 design models, we selected 335 macrocyclic designs on the basis of AfCycDesign (iPAE < 0.13) and Rosetta (ddG < -30 kcal mol -1 , SAP < 35 and CMS > 300 Å 2 ) interface metrics" | **20,000** 骨架 → **80,000** 模型 → **335** → **80** 簇取代表 → 合成 **13** 条 → 高纯度可用 **6** 条 |
| B3b | 6 条 | SPR + 竞争式 AlphaScreen + 结晶 | SPR 亲和力；AlphaScreen 与 K1 竞争（IC50 拟合 Hill 方程，至少三次独立重复取均值） | **2** 条命中：GAB_D8 = **6 nM**、GAB_D23 = **36 nM**；IC50 **0.7 nM**/**2.5 nM**；作者称 "To our knowledge, GAB_D8 is the most potent macrocyclic GABARAP binder to date" |
| B4 RbtA | **无实验结构**（只有序列） | AF2+RF2 双预测靶 → 只在两法一致高置信区设计；定 7 个 hotspot（Leu144/Phe202/Phe204/Tyr206/Val208/Leu231/Ala269）；表面比前几靶**更平** | "we selected 26 designs for biochemical and structural characterization with AfCycDesign iPAE < 0.4"（该句后半还要求 ddG < -30 kcal/mol、设计-预测 r.m.s.d. < 1.5 Å、CMS > 300 Å²，正文同句给出） | **20,000** 骨架 → ×4 → **26** 入选 → 合成并量/纯度够者进筛 |
| B4b | 可测设计 | SPR（Avi-tag 表达的 RbtA N 端结构域 20–458）→ X 射线 | 100 µM 有信号 | "Four of 11 designs that were synthesized in sufficient quantity and purity showed a binding signal at 100" µM；最佳 RBB_D10 **K_d = 9.4 nM**；复合物 2.6 Å、apo 2 Å，环肽 Cα r.m.s.d. **1.4 Å**（单独对齐 0.4 Å） |

**这套流程最值得单独记住的两件事**：① 漏斗的**末端约束是合成通量而不是测序通量**——所以本文新增了"结构聚类去冗余"这一层（335 → 80 簇），这在酵母展示类论文里根本不需要；② 同一个过滤器在不同靶上的分数分布差异极大，于是"阈值"是**分位数**而不是常数。

## 4. 关键数字台账（全部可在 `macrocyle2025.txt` 逐字搜到）

| 数值 | 含义 | 出处 |
|---|---|---|
| 20 或更少 / 靶 | 每靶送测环肽数（本文的卖点） | "We tested 20 or fewer designed macrocycles against each of four diverse proteins" |
| 48,000 骨架/长度 → 9,045 / 8,913 唯一 | 单体生成规模与去冗余后规模（10-mer / 12-mer） | "9,045 and 8,913 structurally unique 10-residue and 12-residue backbones" |
| pLDDT > 0.8 + 2.0 Å backbone r.m.s.d.，n=200/长度 | 单体自洽性判据（生成器标定口径） | 图 1c 图注 |
| TMscore 0.5（MaxCluster） | 单体结构聚类阈值 | 图 1c 图注 |
| 9,965 / 1,984 / 27 / 14 / 3 / 2 µM | MCL1 逐级递减（骨架→过 DL 阈→选合成→可测→命中→最佳 Kd） | 正文 B1 各行 |
| 10,000 / 40,000 / 7,495 / 17 / 11 / 8 / 3 / 1.9 µM | MDM2 逐级递减 | "AfCycDesign predicted 7,495 of the 40,000 design models" |
| 20,000 / 80,000 / 335 / 80 簇 / 13 / 6 / 2 / 6 nM & 36 nM | GABARAP 逐级递减 | "we clustered the 335 designs into 80 different clusters" |
| iPAE < 0.13；ddG < -30 kcal mol-1；SAP < 35；CMS > 300 Å2 | GABARAP 四阈值组 | 正文 |
| iPAE < 0.3 + ddG < -50 kcal mol-1（MDM2，更严的 ddG） | MDM2 阈值组 | "we identified 17 designs with iPAE < 0.3, ddG < -50 kcal mol -1" |
| iPAE < 0.4；ddG < -30；设计-预测 r.m.s.d. < 1.5 Å；CMS > 300 Å2 | RbtA 阈值组 | "we selected 26 designs for biochemical and structural characterization with AfCycDesign iPAE < 0.4" |
| 26 / 11 / 4 / 9.4 nM | RbtA：入选→可用物料→有信号→最佳 Kd | "Four of 11 designs that were synthesized in sufficient quantity and purity" |
| 0.7 Å / 0.4 Å；1.2 Å / 0.47 Å；1.7 Å / 0.74 Å；1.4 Å / 0.4 Å | 四个共晶的界面对齐/自身对齐 Cα r.m.s.d. | 正文 Fig 2/3/4 段 |
| 0.5 Å 与 0.9 Å | 事后改用 MSA 输入重预测后更接近晶体结构 | "These MSA-based predictions of the designs matched even more closely with the X-ray crystal structures" |
| 86% / 100% | 替代结晶用同源体 GABARAPL1 的整体/界面 5 Å 内序列同一性 | 正文 |
| 0.4 Å over 509 residues；pLDDT > 90 | AF2 与 RF2 对 RbtA 预测的一致性/置信度 | 正文 |
| 10 nM / 20 µM / 50 µM 等 SPR 浓度点 | 单周期动力学九点稀释（最高 20 µM 或 50 µM），筛选点 100 µM | Methods, SPR |
| >90% 纯度 | 送测环肽的纯度门槛 | "either purchased from Wuxi AppTec at greater than 90% purity" |
| **本文未记录** | GPU/CPU 单价、每条设计的计算耗时、总机时；也未给 MCL1 的 iPAE 数值 | CSV `cost_or_stat_note=未记录` 与正文一致 |

## 5. 结论——作者说了什么

1. RFpeptides（RF2/RFdiffusion + 环状相对位置编码）能做**环肽结合体的从头设计**，四个靶每靶只测 ≤20 条就都拿到中到高的亲和力："We tested 20 or fewer designed macrocycles against each of four diverse proteins and obtained binders with medium to high affinity against all targets"。
2. 设计模型与实验结构在原子尺度上一致（三个共晶的环肽 Cα r.m.s.d. 0.7 / 1.2 / 1.4 Å）。
3. 只从**预测结构**出发也能做出高亲和力结合体（RbtA，K_d < 10 nM）。
4. DL 判据（iPAE + 复预测一致性）与物理判据（ddG/SAP/CMS）**并用**才有效："Notably, combining DL-based and physics-based in silico filters helps to select medium to high-affinity binders"。
5. 与库法相比的自我定位（作者口径，不是本文实测的对照实验）："Despite testing fewer than 20 designed candidates per target"——并自称这是"considerably higher success rate than achieved with any previous method"。
6. 作者自限：阈值必须按靶重调（2.5 条）、打分排序与亲和力排序不一致（2.6 条）、合成产率是硬瓶颈（2.4 条）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文真正的贡献不是生成器，而是"把下单预算写进漏斗"**：335 → 80 簇那一步是被合成通量逼出来的。→ 对我们：UAA 场景的等价约束是"一轮最多四个构建体的湿实验预算"，所以漏斗末端必须做**信息量最大化**的多样性削减（机制多样性 + 失活对照），而不是相似度削减；他们的 t-SNE/TM-score 聚类可以直接借作"结构多样性去冗余"的算法层。
2. **"同一个过滤器在第二个靶上分布完全变了"是本文最有代价感的观察**（2.5 条）。→ 我们的判据（PLACER 式预组织频率、S0/S1/S2 事件归类）在换底物/换酶族时同样要重标分位点，任何"全局阈值"都必须附带一句"该阈值是在哪个分布的第几分位"。
3. **正交复预测作为可选层，且作者会主动省掉它**（2.3②）。→ 给我们一条可执行规则：**任何过滤器进漏斗前先测它与上一层的相关性；相关性高就砍掉，不占预算**。本文 MDM2 那一支就是这么做的。
4. **"计算通过率"与"可测样本数"是两个独立漏损**（2.4 条：27 → 14、11 → 8）。我们的实验里对应物是"表达可溶 + 产物能被 LC-MS/MS 检出"，这一层他们没有任何预测工具，我们也不该假装能预测。
5. 他们敢用**设计模型直接做分子置换相位**——这是"自洽性判据"最硬的兑现方式：模型不准就解不出结构。→ 我们的等价兑现是"设计构象能不能解释测到的动力学差异（kcat/KM 与突变体）"，两者都是把模型押在可证伪的位置上。
6. 事后 MSA 重预测更好（2.9 条）说明**漏斗用单序列是有偏的**；但作者没有把它加进筛选，因为会破坏"单序列即可评估"的可扩展性。这类"已知更准但不用"的取舍，我们做 UAA 判据时也会遇到（如 PLACER 50 seeds 与全原子 MD 之间），应当明写代价而不是默认它不存在。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：① 阈值需按靶调整；② DL/物理指标"enrich 得好"但**内部排序与实验亲和力不符**（MCL1 与 GABARAP 的命中不在前三）；③ 合成产率不可预测（27 里 13、11 里 3 掉样）；④ 未做膜通透性/稳定性等第二性质优化，只在讨论里指向未来。
- 我们读出：① 四个靶共测 ≤20 条，命中总数很小（3+3+2+4 有信号，真正定量亲和力最好的两条为 6 nM 与 9.4 nM），**样本量不足以支撑那句 considerably higher success rate than achieved with any previous method 的横向比较**（他们没做同靶的库法平行对照）；② GABARAP 分支的 335 → 80 → 13 → 6 层层缩减，"命中率"取决于最终 6 条的运气，正文没有给出被聚类丢掉的那 255 条是否含有更强结合体——**去冗余的正确性无法从本文判定**；③ MCL1 没有给 iPAE 阈值数字（在补充图 S4），因此该战役不可严格复现；④ 全文无 MD/QM，不能为任何能量学/机理层主张提供依据。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"分位数式阈值"的写法**：我们的每个闸口报数时同时给出"该靶/该族的分数分布 + 阈值落在第几分位"，照本文"阈值随分布调整、并明写调过"的做法（第 2.5 节）。
2. **结构多样性聚类作为下单前的削预算层**（335 → 80）：可直接用 TM-score/t-SNE（MaxCluster 0.5 阈值这一类）对我们生成的候选做簇代表选取，把"四个构建体"的名额花在机制多样性上。
3. **"过滤器要先测与上游的相关性"这一条纪律**（第 6.3 条）：MCL1 加 RF2、MDM2 省 RF2 的对照是现成的方法学教材。
4. **把模型押在可证伪的实验兑现上**（设计模型直接作 MR 相位）→ 我们的等价物：设计构象必须给出可被判伪的预测（哪个残基突变会掉多少倍活性），并且真的做失活突变对照（本文与 [B17] 都做了催化残基敲除，这条是 Baker 组的稳定做法）。

**不可迁移（为什么不能照搬）**

1. **iPAE / ddG / SAP / CMS 全部是"结合界面对不对、聚不聚"的判据，与催化无关**。SAP 与 CMS 描述的是聚集倾向与埋藏面积，对 UAA 合成酶"会不会催化三步化学事件、会不会被产物抑制"既不必要也不充分。**不得**把这些阈值（如 iPAE<0.13、ddG<-50）当作酶活闸口引用（DP2R 口径：binder 阈值不得迁移为催化判据）。
2. **"每靶 ≤20 条就出结合体"不是可用的成功概率**。他们测的是**静态结合**（一个二元信号 + 一个 Kd），我们目标要多一层"化学转化 + 副产物分辨"；且本文的命中里两个最好也只有 µM 级（MCL1/MDM2）。引用时只许引用**漏斗结构**（生成→DL 筛→物理筛→聚类→合成→SPR），不许引用命中率数字。
3. **化学合成通量 ≠ 我们的表达/反应通量**：他们的瓶颈是环化产率，我们的瓶颈是蛋白可溶表达与 LC-MS/MS 产物分辨，两条预算曲线的形状不同，不能照搬"80 个代表"这类具体数字。
4. 本文没有 MD、没有 QM、没有过渡态建模，**不能**用来支持"用构象系综判催化"这类主张（那属于 [B17]/[B19] 的证据范围）。

## 9. 溯源与自检

- 本地纯文本：`data/interim/baker_lit/ft/macrocyle2025.txt`（Europe PMC fullTextXML 去标签、HTML 实体已解码、未改写内容）。
- 引句底稿: data/interim/baker_lit/ft/macrocyle2025.txt —— 本卡全部英文引句以此为唯一逐字比对对象。原始 XML `data/interim/claim_lit/PMC12643943.xml` 亦已登记，但核验脚本按 `.xml` 后缀排除在逐字比对之外。
- 对照底稿行号：`sources/baker.md:198–209`；跨论文对照表行：`sources/baker.md:606`（3b 物理项 ddG/SAP/CMS 行）、`sources/baker.md:609`（聚类去冗余 335→80 行）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。
- 本卡自检：`scripts/verify_literature_cards.py --only B15 --no-report` 把卡内所有不含中日韩字符、被直双引号包住且 ≥20 字符/≥12 字母的片段，在第 9 节声明的引句底稿里逐字查找；本轮结果见对话回报（PASS 行打印 quotes=N/N）。写卡过程中就地修正了三处非逐字草稿：一处把原文的 d -amino acids（中间有空格）连写成 d-amino acids；一处把长引句截短以避开全文里同形不同码点的 Å（U+212B 与 U+00C5 混用）；一处把自评句漏掉的 achieved with 补回。
- 本文正文没有给 MCL1 战役的 iPAE 阈值与逐条排名（在 Supplementary Fig 4 / Table 1b），本卡第 3、4 节相应位置明写"正文未给"。

<!--CSV回填
work_type=论文
target=MCL1、MDM2、GABARAP（含替代结晶同源体 GABARAPL1）、Rhombotarget A（RbtA，仅有预测结构）
backbone_generation=RFpeptides＝RFdiffusion + 环状相对位置编码生成环肽骨架；序列端 ProteinMPNN + Rosetta Relax 迭代（每骨架 4 条序列）；单体标定用 LigandMPNN（每骨架 8 条）
computational_filters=AfCycDesign（带环状位置编码的 AF2）复预测：iPAE（含 normalized iPAE）+ 设计模型与预测复合体的 r.m.s.d.；可选 RF2 正交复预测（仅 MCL1 战役使用）；Rosetta 物理项 ddG / SAP / CMS；t-SNE + TM-score 结构聚类去冗余
thresholds=iPAE<0.13（GABARAP）/ <0.3（MDM2）/ <0.4（RbtA），MCL1 正文未给数值；ddG<-30（GABARAP、RbtA）或 <-50 kcal/mol（MDM2）；SAP<35；CMS>300 Å²；设计-预测 r.m.s.d.<1.5 Å（RbtA）；单体自洽 pLDDT>0.8 且 backbone r.m.s.d.<2.0 Å；聚类 TMscore 0.5（MaxCluster）；送测纯度>90%
md_used=否
qm_used=否
experimental_methods=Fmoc 固相多肽合成 + 分子内环化 + RP-HPLC + MS 定性 → 生物素化靶 + SPR 单周期动力学（100 µM 判定有信号）→ 九点单周期测 Kd → 竞争式 AlphaScreen（IC50，Hill 拟合）→ X 射线共晶（用设计模型做分子置换相位）
pipeline_counts=MCL1 9,965 骨架→1,984→27 合成→14 可测→3 命中；MDM2 10,000 骨架/40,000 模型→7,495→17→11 合成→8 可测→3 命中；GABARAP 20,000 骨架/80,000 模型→335→80 簇→13 合成→6 高纯→2 命中；RbtA 20,000 骨架→26 入选→11 可用物料→4 有信号→1 高亲和
hit_rate=四靶每靶送测 ≤20 条，全部拿到中-高亲和结合体；但绝对命中数为 3/3/2/4 量级，作者未给统一命中率百分比，也未与库法做同靶平行对照
best_metric=Kd = 9.4 nM（RbtA，RBB_D10）与 6 nM（GABARAP，GAB_D8，AlphaScreen IC50 0.7 nM）；MCL1/MDM2 最好仅 µM 级（2 µM / 1.9 µM）
cost_or_stat_note=正文未记录 GPU/CPU 单价与总机时（与 CSV 未记录一致）；成本约束以"合成通量"形式出现：27 条中 13 条、11 条中 3 条因环化产率不足被剔；335 条未合成而改测 80 簇代表；筛选点单一浓度 100 µM
role_in_timeline=首次把 de novo 漏斗套到化学合成候选上：新增"结构聚类去冗余"层以匹配合成预算，并把 AfCycDesign 从生成器降级为事后过滤器；与 [B09] 的 pAE_interaction 闸口同构（界面级 DL 判据 + 物理判据并用），但样本量从万级降到 ≤20/靶
source_pointer=data/interim/baker_lit/ft/macrocyle2025.txt（另有 data/interim/claim_lit/PMC12643943.xml 原始 XML，不参与逐字比对）；sources/baker.md:198-209
CSV回填-->
