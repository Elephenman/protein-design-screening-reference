# [Z11] gp100 抗原模拟表位的纯计算突变设计：把"两路自由能 + 结构可解释"立成双闸口（降级精读卡）

## 0. 元信息与证据级别

| 项 | 内容 |
|---|---|
| CSV 编号 | Z11（`data/protein_design_literature.csv` 第 56 行；组：周如鸿组） |
| 标题 | In Silico Design of High-Affinity gp100 Antigenic Mimotopes for Targeting Melanoma |
| 作者／期刊年 | Rui Ye, Yuxuan Yang, Kevin C. Chan, Dong Zhang, Ruhong Zhou；J Phys Chem B, 2025（2025 Jul 31;129(30):7708-7718） |
| DOI／PMID | 10.1021/acs.jpcb.5c01507（底稿记 ✅Crossref 核验）· PMID 40692510 |
| 条目类型 | 论文（CSV 文献类型=论文；PMID 备注"纯计算"） |
| 状态 | **DEGRADED**：无本地正文（`inventory.json` 的 `ids.pmc` 为空，`local` 只有两份 PubMed 摘要转储），本卡只用摘要级材料写 |
| 登记底稿①（内容） | `sources/zhou.md` 的 [Z11] 段落（本项目 2026-10-16 调研记录） |
| 登记底稿②（引句） | `data/interim/claim_lit/abs.txt`（NCBI/PubMed 摘要转储，`inventory.json` 把 Z11 的 `local` 登记为 abs.txt / abs2.txt；本卡英文引句一律从这一份逐字抄，`sources_map.json` 已登记且文件存在） |
| 证据级别 | **摘要级／未获正文**（照 CSV `证据级别` 列写；底稿 `sources/zhou.md:141` 同记"纯计算，摘要级"） |
| 未取到的部分 | FEP 的 λ 窗数／窗长／副本数、体系准备与力场、ΔΔG 具体数值与单位、"affinity-matured TCR structure"取自哪一篇、TCR-pHLA 那一路的自由能是怎么算的、双突变体的扫描范围。以上本卡一律写"未记录（本次未取正文）"，不做推断填充 |

## 1. 这一条解决什么问题（一句话）

在一个已被实验确认的天然抗原九肽（gp100 280-288(288V)，序列 YLEPGPVTV，由 HLA-A*02:01 呈递）上做 in silico 突变扫描，用**两路自由能同时过关**（peptide-HLA 结合增强 + TCR-pHLA 结合不受损）再叠加**结构可解释性复核**，挑出既能稳定呈递又不破坏 TCR 识别的模拟表位（mimotope）候选。


## 2. 难点与应对（含"无 OA 正文"的取证困难）

以下"作者做了什么"全部限定在摘要与登记底稿确实记下的动作，正文层面的协议改动本次无法核验。

1. **难点：单点突变把 peptide-HLA 做"强"了，却把 TCR 那一侧做坏。**
   现象／证据（摘要原句）："the E3A and E3V mutations improved peptide-HLA binding but weakened the TCR-pHLA binding affinity"——只看一路自由能，这两个突变是"成功候选"。
   **作者做了什么**：①把判据写成**两路**（HLA 结合增强 **且** TCR-pHLA 不受损，"E3I and E3L mutants increased HLA binding without affecting TCR binding"是过关的那两个）；②对被拒的两个做**结构归因**："insufficient occupancy of the HLA pocket by residue 3 in the E3A and E3V mutants would induce a twisted peptide conformation at positions 4 to 6"，即口袋填不满→肽 4-6 位扭曲→界面被破坏；③把这一条上升为设计原则句："it is crucial to consider the impact of single-residue mutations that alter peptide conformation on TCR binding"。登记底稿 `sources/zhou.md:142` 把这一步记作"给出自由能之外必须有结构解释的组内惯例"，并在 `sources/zhou.md:190` 的组内漏斗表里把这一层列为"机理一票否决"（该层同时挂 Z06/11/12，属组内共用口径，不是本篇自报的数值阈值）。
   **应对后仍留下的代价**：判据从"一个数"变成"两个数 + 人工结构解释"，通量与自动化程度下降；结构解释这一步没有可核验的量化标准（本次未取正文，看不出他们是否有客观指标），底稿也把它记为"惯例"而非阈值。

2. **难点：一路"增强"没有实验终审，整条链停在计算端。**
   现象／证据：CSV `实验验证手段` 列写"无实验送检数字（论文本身不声称闭环）"；摘要自述止于 "Our work provides structural insights for the rational design of favorable gp100 mimotopes" 与 "may contribute to developing gp100 epitope-based vaccines"（"may"是作者自己的限定词）。
   **作者做了什么**：在计算端把候选面拓宽——除单点外再做双突变叠加，"the E3I+V7L and E3L+V7L double mutants are also found to produce favorable binding affinity changes"，把"单点过关"外推成"可组合"。
   **本文未解决**：没有任何合成／结合／功能读数，因此**没有命中率可报**；E3I/E3L 是否真的能增强 CTL 反应，本篇不给答案（作者也没声称）。

3. **难点：两路自由能用的结构起点本身是个前提。**
   现象／证据：方法句只给到 "with all-atom molecular dynamics (MD) simulations and free energy perturbation (FEP) methods, we designed a series of potential mimotopes through in silico mutagenesis studies"，并限定 "utilizing the latest affinity-matured TCR structure"。
   **作者做了什么**：显式改用"亲和力成熟后的 TCR 结构"作受体端（这是摘要里唯一可见的一次方法层面的换输入动作）。
   **代价／未记录**：这个 TCR 结构来自哪里、亲和力成熟到什么程度、它对 pHLA 复合物的建模误差如何传导到 ΔΔG——本次未取正文，全部未记录。

4. **无 OA 正文的取证困难与处置（这一条是取证层，不是本文的困难）。**
   困难：本行在 `data/literature_cards/batches.tsv` 第 101 行状态列为 DEGRADED；`inventory.json` 给 Z11 的 `ids.pmc` 为空、`local` 只有两份 PubMed 摘要转储（`data/interim/claim_lit/abs.txt` 与 `abs2.txt`，都是多条目混合文件），**没有任何一份正文**。风险是"摘要有几句、正文没有，越写越像是有正文"。
   **处置**：①本卡所有方法学动词只落在摘要可见句子与 `sources/zhou.md:138-143` 的记录上；②§3 表的"判据／阈值"列凡底稿没给数字的一律写"原文未给阈值（本次未取正文）"，不从同组他篇（如 Z12/Z04 的 MD 稳定性门槛）挪数；③引句全部声明并逐字命中 `data/interim/claim_lit/abs.txt`（见 §9），不伪造正文引用；④`阈值数字／候选数递减／实验命中率／Kd或活性最好值／成本统计`五个 CSV 列按 CSV 现值写"未记录"，并在回填块注明原因。


## 3. 方法与工作流程（摘要级口径，不补正文细节）

**工具箱（摘要与底稿点名的，就这么几件）**：全原子 MD、FEP（alchemical 自由能微扰，摘要原话 "free energy perturbation (FEP) methods"）、位点定向 in silico 突变扫描、结构分析（口袋占据 + 肽主链／残基构象观察）。
**没点名的**：机器学习打分器、结合 free-energy 端点法（MM-PBSA/GBSA）、QM、任何实验平台——摘要未提，本次未取正文，不写成"他们用了"。

| # | 输入 | 操作 | 判据／阈值 | 输出规模 |
|---|---|---|---|---|
| 1 | gp100 280-288(288V)（YLEPGPVTV）+ HLA-A*02:01 + "the latest affinity-matured TCR structure" | 建 peptide-HLA 与 TCR-pHLA 两路复合物，跑全原子 MD | 原文未给阈值（本次未取正文；盒大小／力场／时长／副本数均未记录） | 起点复合物（数量未记录） |
| 2 | 起点复合物 | 对肽**位点 3（E3）**做 in silico 突变扫描，用 FEP 算两路结合自由能变化 | 判据是**双路定性**：peptide-HLA 结合改善 **且** TCR-pHLA 不劣化；ΔΔG 的数值门槛原文未给阈值（本次未取正文） | 摘要点名单点 4 个：E3I、E3L（过关）、E3A、E3V（被拒）；扫描总突变数未记录 |
| 3 | 被拒的 E3A/E3V | 结构分析找原因（残基 3 对 HLA 口袋的占据程度、肽 4-6 位构象） | 判据＝"口袋填充不足→肽扭曲→TCR 相互作用被破坏"这一机理链；无机值阈值（未记录） | 机理解释 1 条（残基 3 占据不足 / 位置 4 到 6 扭曲） |
| 4 | 过关的 E3I/E3L | 叠加 **V7L** 再做双突变 FEP | 判据＝与单点"类似的有利结合变化"（原文未给阈值，本次未取正文） | 双突变 2 个：E3I+V7L、E3L+V7L |
| 5 | 全部计算结果 | 与实验对照／送合成 | **无这一步**（CSV 记"无实验送检数字"，摘要自述只到"provides structural insights"） | 送样 0 条；命中率未记录（不适用） |

**流程骨架可复述的部分**：定结构起点 → 定点突变扫描 → 双路自由能定性判 → 结构机理复核（可否解释得通）→ 组合放大（单点→双点）。**不可复述的部分**：每一步的数值门槛与计算预算，本卡不猜。


## 4. 数字台账

| 数值 | 含义 | 出处 |
|---|---|---|
| 280-288（九肽），序列 YLEPGPVTV | 设计起点：gp100 的免疫显性表位肽 | 摘要句 "One such epitope, gp100280-288(288 V) (YLEPGPVTV), is presented by human leukocyte" |
| HLA-A*02:01 | 呈递该肽的血清型（复合物另一半） | `data/interim/claim_lit/abs.txt`（原文写作 HLA)-A*02:01，本行不加引号因含星号会被门禁剥掉） |
| 位点 3（E3） | 单点突变扫描的靶位 | 摘要句 "insufficient occupancy of the HLA pocket by residue 3" |
| 位置 4 到 6（4 to 6） | 被扭曲的肽段区间 | "would induce a twisted peptide conformation at positions 4 to 6" |
| 单点候选 4 个：E3I、E3L、E3A、E3V | 摘要点名的四个突变体（2 过关 / 2 被拒） | "Our results showed that E3I and E3L mutants"；"the E3A and E3V mutations improved peptide-HLA binding" |
| 双点候选 2 个：E3I+V7L、E3L+V7L | 在过关单点上叠加 V7L | "the E3I+V7L and E3L+V7L double mutants are also found" |
| 送样数 0、命中率无 | 无实验终审（CSV：无实验送检数字） | `sources/zhou.md:143`（命中率: 无实验送检数字） |
| ΔΔG 数值、FEP 窗数／窗长／副本数、MD 时长 | 本卡**未记录** | 本次未取正文；底稿 `sources/zhou.md:141` 只标"纯计算，摘要级" |
| 2025 Jul 31;129(30):7708-7718 | 出版卷期页 | `data/interim/claim_lit/abs.txt` 该条目头部行 |
| DOI 10.1021/acs.jpcb.5c01507 / PMID 40692510 | 身份核 | `sources/zhou.md:141`（✅Crossref）、CSV 第 56 行 |

## 5. 作者说了什么

1. 定位是"计算与实验互补"，不是替代实验："Computational approaches, particularly the predictions on peptide-HLA (pHLA) and TCR-pHLA binding affinities" 与 "are complementary to experimental approaches in guiding further optimization and design"。
2. 做了什么：全原子 MD + FEP，用最新亲和力成熟 TCR 结构，对 gp100 280-288(288V) 做 in silico 突变设计。
3. 结果：E3I/E3L 增 HLA 结合而不伤 TCR 结合；E3A/E3V 反例（HLA 好、TCR 差）；结构解释为残基 3 占据不足导致肽 4-6 位扭曲；E3I+V7L、E3L+V7L 双突变与单点同等有利。
4. 原则句：设计有效抗原模拟表位时必须考虑"改变肽构象的单点突变对 TCR 结合的影响"。
5. 作者自限：交付的是结构洞察（"provides structural insights for the rational design"），对疫苗的贡献用 "may contribute to developing gp100 epitope-based vaccines" 表述；**没有给出任何实验确认、亲和力数值或成功率**。

## 6. 我们读出了什么（以下为推断）

1. **真正可复用的是"双路判据 + 一票否决"这套结构，不是任何数字**。他们把目标性质拆成两个必须同时成立的量（呈递稳定 × 识别不被破坏），并让第二个量拥有否决权。→ 对应我们：UAA 合成酶候选的"结合／定位正确"与"三条化学事件能否发生"必须各自独立过关，任何一路不过就否决，不能合成一个加权总分。
2. **被拒样本比被留样本信息量大**。E3A/E3V 是"一路指标变好但整体失败"的活教材，与 B09 那篇 Type II 失败（折对了但界面没形成）是同一类问题在肽-HLA 体系的版本。→ 我们的漏斗要把这类候选单独归档（"指标改善但机理失败"），而不是当噪声丢掉。
3. **没做实验却仍把候选写进结论**，这在文献里的价值只有"生成端"，没有任何"校准端"价值。→ 引用本行时只能引用判据的组织方式，绝不引用命中率或改善幅度。
4. **底稿把这一步归入组内"机理一票否决"层**（`sources/zhou.md:190`，同层挂 Z06/Z12），说明这是该组反复使用的固定层，不是本篇临时加的解释；但同层口径不等于本篇阈值，本卡不为其补数。

## 7. 局限

- 证据级别只有摘要级：**无法核验**两路 ΔΔG 是否真有数值门槛、FEP 收敛怎么判、扫描总共做了多少个突变体（摘要只点名 6 个）、TCR 结构来源与建模误差。
- 无实验闭环：所有 "potential""may contribute" 都是计算侧推测用语。
- 底稿与摘要有粒度差：底稿 `sources/zhou.md:142` 把判据概括为"ΔΔG 降低／不劣化"，摘要本身没写 ΔΔG 数值——本卡因此不写任何"改善了多少"的句子。
- 单一体系、单一血清型（HLA-A*02:01）、单一位点（E3），不构成方法学结论，也不构成跨体系外推的依据。

## 8. 迁移到我们的筛选／判定工作流

**可迁移（怎么用）**

1. **双路同时成立才准入**：把"结构／结合侧"与"功能／化学侧"做成两条独立判据，功能侧拥有否决权——这是本行唯一能直接搬进我们漏斗的组织形式（不附带任何阈值）。
2. **失败反例做结构归因**：对"一路变好一路变坏"的候选，先做机理解释再决定是否弃；解释不出来就保留 UNKNOWN 状态，不硬判。
3. **过关候选再做组合放大**（单点→双点）可用于"在已过关构型上叠加第二处改动"，但叠加后必须重跑同一套判据，不能假设可加和（本篇自己的双突变结论也只是"similar to those of the E3I and E3L mutants"这一比较句）。

**不可迁移（为什么不能照搬）**

1. **pHLA／TCR-pHLA 结合自由能不能当 UAA 酶活判据**。本行的成功定义是"呈递更稳且识别不被破坏"，全是静态结合热力学；没有任何一步涉及化学键生成、转换数或副产物分支。把这类 ΔΔG 门槛搬进酶筛选属于判据对象错配。
2. **没有实验终审 → 没有可借用的概率**。本行不报命中率；也不得与同组 Z13 的 5/5 合并成"该组方法成功率高"这类口径。
3. **摘要级证据不许当方法细节引用**。我们若在方案里写"按 Ye 2025 的 FEP 窗口设置"，那是本篇支撑不了的（未取正文）。

## 9. 溯源

- 引句底稿: data/interim/claim_lit/abs.txt
- 内容底稿：`sources/zhou.md:138-143`（[Z11] 段落，本项目 2026-10-16 调研记录）；`sources/zhou.md:190`（组内漏斗表第 4 层"机理一票否决"，出处挂 Z06/11/12）；`sources/zhou.md:235`（组内准入判据总述："相对亲代 ΔΔG<0 + 结构机理可解释"，无全局数值阈值）。
- CSV 行映射：本卡 §0/§3/§4 ↔ `候选生成方法／计算筛选判据／阈值数字`；§4/§5 ↔ `候选数递减／实验命中率／Kd或活性最好值`；§8 ↔ `在方法演进链的位置`。
- 为什么引句底稿不是 sources/zhou.md：`inventory.json` 把 Z11 的本地底稿登记为 `data/interim/claim_lit/abs.txt` 与 `abs2.txt`（NCBI 摘要转储，两份都含本条目），`sources_map.json` 同；因该行的 `has_fulltext` 被置真，门禁要求 ≥8 条引句，而 `sources/zhou.md` 的 [Z11] 段落里纯 ASCII 可核片段只有 2 条（标题行与作者行）。故本卡把引句底稿声明为 abs.txt（登记且存在的底稿，仍是摘要级材料），内容层陈述仍以 `sources/zhou.md` 为准。两份文件都未改写，本卡未使用任何未登记的来源，也没有取过正文。
- 归一化说明：门禁按 `scripts/litcards_text.py` 的 norm（实体解码、`–—−`→`-`、`\xa0`→空格、空白折叠）逐字比对；本卡引句按归一化后的形态抄写（如 "(288 V)" 处的空格），未做美化。
- 本次未做的事：没有跑 `--sync-map`，没有改 CSV／底稿／样板卡／脚本，没有做任何网络抓取。

<!--CSV回填
work_type=论文（纯计算，无实验闭环）
target=gp100 280-288(288V)（YLEPGPVTV）黑色素瘤抗原模拟表位，呈递于 HLA-A*02:01
backbone_generation=in silico 突变扫描（肽位点 3 单点 E3I/E3L/E3A/E3V；过关单点再叠加 V7L 成双点）
computational_filters=全原子 MD + FEP 双路自由能：peptide-HLA 结合改善且 TCR-pHLA 结合不劣化；另加结构可解释性复核（残基 3 对 HLA 口袋占据、肽 4-6 位构象）
thresholds=未记录（本次未取正文；摘要与底稿均未给数值阈值，底稿 sources/zhou.md:141 仅记"纯计算，摘要级"，组内同层口径是"相对亲代改善 + 机理可解释"）
md_used=是（全原子 MD 与 FEP 一起作主筛选器，摘要原话 all-atom molecular dynamics (MD) simulations and free energy perturbation (FEP) methods）
qm_used=否（CSV 是否用QM=否；摘要未提 QM）
experimental_methods=无实验送检数字（CSV 现值；论文本身不声称闭环）
pipeline_counts=摘要点名单点 4 个 + 双点 2 个；总扫描数与逐层递减未记录（本次未取正文）
hit_rate=未记录（无湿实验送样，不适用）
best_metric=未记录（摘要只给定性 increased HLA binding without affecting TCR binding，无 Kd 或 ΔΔG 数值）
cost_or_stat_note=未记录（正文未取；无算力、窗口时长或成本口径）
role_in_timeline=周组漏斗第 4 层"机理一票否决"的样本之一（sources/zhou.md:190 同层挂 Z06/11/12）；dynamic pocket 概念与 Z12 同源；纯物理 FEP 路线在 2025 年的"无实验闭环"侧证
source_pointer=data/interim/claim_lit/abs.txt（PubMed 摘要转储，本卡引句底稿）；sources/zhou.md:138-143（内容底稿）；DOI 10.1021/acs.jpcb.5c01507、PMID 40692510
CSV回填-->
