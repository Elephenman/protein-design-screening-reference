# [B09] 用深度学习改进 de novo 结合蛋白设计——把"漏斗该用哪个判据"变成可测问题

Bennett N, Coventry B, Goreshnik I, Huang B, … Baker D（华盛顿大学 IPD）
Nature Communications 2023, 14:2625 · DOI 10.1038/s41467-023-38328-5 · PMID 37149653 · PMCID PMC10163288
开放获取（CC BY 4.0）· 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10163288/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B09**（组：Baker组; 通用方法学; 口径对照） |
| 本文取回方式 | Europe PMC `fullTextXML`（HTTP 200，99,555 B），2026-10-20 本地抓取 |
| 本地全文①（本次抓取） | Europe PMC `fullTextXML` → `fulltext/B09_PMC10163288_fullTextXML.xml`（SHA-256 `afd6f37a0f1c824d…`），去标签纯文本 `fulltext/B09_PMC10163288_text.txt`（SHA-256 `3b4830502416a1e0…`） |
| 本地全文②（先行调研缓存，独立抽取通路） | `data/interim/baker_lit/ft/binderDL2023.txt`（49,256 B，2026-10-16 抓取） |
| 两通路互证结果 | 本卡 **36/36 条逐字引句在两份全文里同时命中**（`data/literature_cards/selfcheck.txt`） |
| 对照底稿 | `sources/baker.md` 第 120–133 行（原卡），本卡在其基础上补：单序列推理成本、DAN 成本、回顾集 10 靶的实测分布、AF2 initial-guess 协议、效率公式与 CPU/GPU 折算、ProteinMPNN-FR 数字、成功判据 SC50<4 μM |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中；见第 9 节自检） |
| 未取到的部分 | 补充信息（Supplementary Figs 1/4/5/6/9）、Source Data、Fig 1–2 原图数值。凡引这些的地方本卡明写"正文未给出，仅有正文描述" |

## 1. 这篇到底解决什么（大白话）

前作（Cao 等 2022）已经能用"只知道靶蛋白结构"设计出结合它的全新蛋白，但**做一百万个、能成的很少**，而且没人知道该在下单前丢掉哪一批。这篇做的事：把前作留下的**近 100 万条"设计 + 湿实验结果"配对数据**当成考卷，逐个测试各种打分办法能不能提前分辨"会结合"和"不会结合"，最后给出一个当时最强也最贵的判据（AF2 界面 pAE_interaction），再拿四个新靶做前瞻实验证明它真的把成功率提高了约一个数量级；顺带解决了"这个判据太贵、算不起"的问题（换成 ProteinMPNN 出序列）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **成功率低是核心痛点，而且是已知的**。原文开篇即承认："the overall design success rate is low"，并给出前作的量级：回顾集里 "**15,000–100,000 designs were experimentally tested for each target,**"（10 个靶）。→ 也就是说，同一个漏斗对不同靶点能差 3 个数量级，"平均命中率"没有意义。 **应对**：不报平均值，改为逐靶分开报，并把"该用哪个判据"变成一个能在历史数据上打分的问题（第 3 节 A 段）。
2. **失败被拆成两类，而且第二类才是主因**（这是本文最有迁移价值的概念，Fig 1 图注原句）：
   - Type I：**"Failures. The designed sequence does not fold to the designed monomer structure."**（压根没折成设计构象）
   - Type II：**"Type-2 Failures. The designed sequence folds to the designed monomer structure but does not form the designed interface."**（折对了，界面没形成）
   作者结论：AF2/RF2 在结合体判别上表现极好，这 **"strongly suggest that Type II errors are primarily responsible for the low success rates of Cao et al."** **应对**：既然瓶颈在界面而非折叠，就把筛子的重心从单体能量挪到**界面预测**（pAE_interaction），并用 Type I/II 的分法决定"哪一类失败该找哪一类工具"。
3. **原来的物理判据几乎失效**。用 Rosetta 单体能量（按链长归一）判别时，作者先说 "**Not surprisingly as this metric was already used as a stringent filter in generating the input scaffold set for the Rosetta interface design calculations**"，紧接着判定 "**it provided little discriminatory power**"（两句之间原文插了引文编号 21）——因为在生成阶段已经用它筛过一遍，再拿它当筛子等于没有筛子（**选择偏差/幸存者偏差的具体案例**）。 **应对**：把评估放到**独立于生成阶段用过的指标**之外的新信息源（结构预测自洽性）上，而不是继续调 Rosetta 权重。
4. **便宜的 accuracy 预测器不够准**：DAN 只能部分区分（"DAN was able to partially discriminate binders from non-binders"），但快（"**~0.5 GPU seconds per monomer structure**"）；AF2 单体推理 "**relatively slow (~5 GPU seconds)**"，复合物推理更贵（"**~30 GPU-seconds per design**"）。→ 判据强度和成本是一对矛盾，本文第一次把它量化成 efficiency 指标。
5. **AF2 会因靶点建模错而误判**：Spike 上一条长环建模错误，导致真正结合的 LCB1/LCB3 被 AF2 判成不结合（正文与 Supplementary Fig 1 描述）；单纯把靶点结构当 template 喂进去能纠正骨架，**但除 FGFR2 外的界面全被判错**。他们的解法是 "AF2 initial guess"（见第 3 节步骤 6a）。
6. **设计序列没有进化信息**：AF2/RF2 靠 MSA，而全新设计序列没有自然同源序列；作者依赖的是"设计序列比天然蛋白更规整更稳定，因此**单序列**也能预测准"这一前作观察。 **应对**：直接实测——先拿 5 个已有冷冻结构的 minibinder 验证"单序列预测"能不能复现实验构象（binder Cα 0.2–0.8 Å，LCB1 例外 1.5 Å），确认后再把 AF2 当筛子用。
7. **即便全套过滤，仍有靶做不成**：**"success rates among the targets remain low (<1%) and no binders were identified to Site 2 of IL2 receptor-ɑ"**，且亲和力仍在高 nM 段（"**the initially generated binders are in the high nM affinity range**"）。作者自己收口："**much about interface energetics remains poorly understood**"。 **应对（本文内没解决的部分）**：site2 换靶不做解释、亲和力靠后续再进化；本文只交付"漏斗判据 + 计算效率"两件事，没有交付高亲和力。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **骨架与序列**：Rosetta 界面设计协议（沿用 Cao 2022）出骨架；序列有两条可选路径——Rosetta LayerDesign（慢）与 **ProteinMPNN**（快，~2 CPU-s/条），后期用 ProteinMPNN + Rosetta FastRelax 交替（**ProteinMPNN-FR**）。
- **评估器（本文的真正主角）**：AF2 与 RF2 用**单序列**输入预测单体与复合物；从中取 **pAE_interaction**（链间残基对平均 predicted aligned error）、复合物 Cα RMSD、pLDDT、pTM 类指标；对照基线是 Rosetta 单体能量/链长、Rosetta ddG、DAN 精度。
- **物理侧过滤器（对照组）**：target_delta_sap、ddG、contact_patch、contact_molecular_surface（Pareto-front 组合）。
- **实验侧**：酵母表面展示 + 递减浓度流式分选 + 深测序算 SC50（群体级、通量大、只给表观亲和力），再 E. coli 可溶表达 + BLI 单浓度复验（个体级、给绝对 Kd）。
- **没有用的方法**：MD、QM、自由能微扰——本文全程不含这些，机理层解释不在其证据范围内。


### A. 回顾部分（在旧数据上"考筛子"，Fig 1）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | Cao 2022 的 10 靶设计全集 | 直接当作带实验标签的判别数据集（作者称为 **filtering** 任务） | 标签口径：YSD 的 SC50 好（见 A3） | "~1 million experimentally characterized designs"；每靶实测 15,000–100,000 条；每靶 binder 数 1–584 |
| A2a | 同一批设计 | 先测 **Type I** 方向：AF2/RF2 只用**单序列**预测 binder 单体，与 Rosetta 设计结构比 | ①单体 Cα RMSD（越像越可能成功）②pLDDT ③基线 Rosetta 单体能量/链长 ④DAN 精度 | 结论：RMSD 与 pLDDT 有判别力，Rosetta 能量几乎没有；pLDDT(RF2) 与 pLDDT(AF2) 判别力相当 |
| A2b | 同一批设计 | 再测 **Type II** 方向：AF2/RF2 预测**复合物**，看界面 | **pAE_interaction = 链间残基对的平均 predicted aligned error**；对照还有 Rosetta **ddG**、DAN 复合物精度 | 结论："the average pAE of interchain residue pairs (pAE_interaction) was **extremely effective** in identifying the experimentally confirmed binders"，"with **sharp increases in success rates for designs with pAE_interaction <10**"；AF2 略优于 RF2 |
| A3 | 同上 | 定义"成功" | **"Designs with SC 50 values better than 4 μM were considered successes"** | 用于所有 ROC / top-1% 成功率比较 |

### B. 前瞻部分（新靶真下单，Fig 2）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | LTK、ALK、IL-2Rα site1、site2、IL-10Rα 靶结构 | Rosetta 界面设计协议（Cao 管线）造计算库 | 无 | "**~2 million designs for each target**" |
| B2 | 2M/靶 | 三条并行分支削成可下单集合 | 物理分支＝Cao 的 Pareto-front（**target_delta_sap, ddG, contact_patch, contact_molec_sq5_apap_target**）；DL 分支＝**pae_interaction <10 且 af2_complex_rmsd <5 Å** | "**filtered these down to ~20,000 designs to be experimentally tested for each target: ~15,000 designs using the physically based filters of Cao et al. and ~5000 designs with AF2 pAE_interaction <10**"；"Synthetic genes were obtained for the **~80,000 designs**" |
| B3 | ~80,000 基因 | 酵母表面展示 + 递减浓度流式分选 + 深测序 | 先用 **1 μM target with avidity** 分选以不漏掉低亲和力个体，再按浓度梯度分选；算每个 design 的频率→SC50 | 成功数（4 个能做的靶）**1 到 17** 个；IL-2Rα site2 为 0 |
| B4 | YSD 命中的设计 | E. coli 可溶表达 + 单浓度 BLI 复验 | — | **"All designs which showed binding by YSD also showed binding by BLI"**（→ YSD 假阳率低，YSD→BLI 不是第二道关，只是确认） |
| B5 | 两个分支的库 | 比成功率 | 定义＝成功数/实测数 | 物理分支只对 LTK、IL-2Rα site1 出 binder；这两个靶上 AF2 分支成功率分别是 **8× 和 30×**；ALK、IL-10Rα 物理分支 **0 个**、AF2 分支有 → AF2 判据不只是提效，还把"能不能出结果"的靶集合扩大了 |
| B6a | 靶被建模错的情形 | **AF2 initial guess**：把设计结构转成 AF2 原子坐标，在第一次 recycle 时用它初始化 `prev_pos`（默认是全零），并可同时把靶结构作 template 输入 | 使 AF2 复现 5 个已测 minibinder 界面（binder Cα 1.0–2.0 Å） | 协议见 Methods，代码 https://github.com/nrbennet/dl_binder_design |
| B6b | 判据太贵（2M×30 GPU-秒） | 序列端从 Rosetta 换成 ProteinMPNN，再插 Rosetta FastRelax 回环（**ProteinMPNN-FR**） | 自定义效率指标 **Efficiency = SuccessRate × Throughput =（pAE_interaction<10 的设计数 ÷ 生成设计总数）÷（生成一个设计的计算时间）**；**折算 100 CPU-s = 1 GPU-s**（因为 GPU 稀缺） | Rosetta-design 效率 **7.6×10⁻⁷**；ProteinMPNN-FR 出 pAE<10 结构 **~6.6%**、吞吐 **1 design / 120 CPU-s**、效率 **2.2×10⁻⁶** ⇒ 平均按靶提升 **~8 倍**；ProteinMPNN 出一个序列 **~2 CPU-s**（Rosetta 远慢于此） |

**这套流程的骨架值得单独记住**：先用旧的大规模湿实验数据**给筛子打分**（A 段），再在**全新靶上前瞻**验证（B 段），两段用的是同一套指标口径；最后用"效率 = 通过率 ÷ 单价"来选**工程实现**（B6b）而不是只看命中率。我们项目缺的正是 A 段——**从来没有一个"能同时给阳性和阴性打分的筛子考卷"**。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| ~1 million / 10 靶 | 回顾集规模（带实验结果的设计数） | "experimentally characterized designs for 10 different targets" |
| 15,000–100,000 → 1–584 | 每靶实测数 → 每靶 binder 数 | "15,000-100,000 designs were experimentally tested for each target," |
| ~2M / 靶 | 前瞻计算库规模 | "~2 million designs for each target" |
| ~20,000 / 靶 = 15,000 + 5,000 | 送测集合拆分（物理 / AF2） | "~5000 designs with AF2 pAE_interaction <10" |
| ~80,000 | 合成基因总数 | "Synthetic genes were obtained for the ~80,000 designs" |
| 1 → 17 | 四靶各自成功设计数 | "the number of successes for the four targets ranged from 1 to 17" |
| **pAE_interaction < 10 + 复合物 Cα RMSD < 5 Å** | DL 分支双闸口 | "all designs passing pae_interaction <10 and af2_complex_rmsd <5 Å" |
| SC50 < 4 μM | 成功判据 | "SC 50 values better than 4 μM were considered successes" |
| ~2.3% | AF2 判据通过率 | "only ~2.3% of designs pass" |
| ~30 GPU-s | 复合物 AF2 单价 | "computationally expensive (~30 GPU-seconds per design)" |
| ~5 GPU-s / ~0.5 GPU-s | AF2 单体 / DAN 单体单价 | 见第 2.4 节 |
| 近 10×、8×、30× | 成功率提升（总体 / LTK / IL-2Rα site1） | "increases design success rates nearly 10-fold" |
| 仍 <1%；site2 = 0 | 全过滤后绝对成功率与失败靶 | "success rates among the targets remain low (<1%)" |
| 高 nM | 初始亲和力水平 | "in the high nM affinity range" |
| 7.6×10⁻⁷ vs 2.2×10⁻⁶；~6.6%；1/120 CPU-s；~8× | 效率、通过率、吞吐、工程收益 | 第 3 节 B6b |
| 100 CPU-s = 1 GPU-s | 成本折算因子（他们自定） | "conversion factor of 100 CPU-s to 1 GPU-s" |
| 9K / 2K / 2K | 最终三种池子（Rosetta-Rosetta / Rosetta-AF2 / ProteinMPNN-AF2） | 正文池规模描述 |

## 5. 结论——作者说了什么

1. 把 AF2/RF2 用作**设计后的评估闸口**（单体折叠一致性 + 界面 pAE_interaction）**使实验成功率提高近 10 倍**。
2. **pAE_interaction<10 是当时最强判别量**，于是成为后续 binder 论文的默认闸口。
3. 低成功率的主因是 **Type II（折对了但界面对不上）**，不是 Type I。
4. 用 **ProteinMPNN 取代 Rosetta 出序列**显著提升**计算效率**（约 8 倍），而不是提升命中率本身。
5. 作者自限：各靶成功率 **仍 <1%**，IL-2Rα site2 **完全没有结合体**，亲和力仍停在**高 nM**，界面能量学"远未被理解"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **他们的跃升不是来自更好的生成器，而是来自"有一批带结局标签的历史实验"**。A 段能存在，是因为 Cao 2022 把 100 万条失败也留了档。→ 对我们：没有等价标签集（**至今没有一条被产物化学确认的天然参照酶**）时，任何"目标概率"都没有 A 段地基，只能是机制论证。
2. **"已经在生成阶段用过的指标，不能再当筛子"**（第 2.3 节）→ 对应我们的教训：把同一样东西（如 Foldseek 命中、pLDDT、催化 Asn 位点）既当召回条件又当支持证据，等于自证。
3. **失败分型比分数更值钱**。Type I/II 的拆分让"该改进哪一环"变成可执行问题。→ 我们的三分法应对齐 **第一步（游离底物起始）/ 第二步（中间体形成）/ 第三步（第二底物 vs 副反应竞争）**，并让每个失败候选归到某一事件，而不是笼统给低分。
4. **"效率 = 通过率 ÷ 单价"这一条应当搬**。我们过去把预算压在长时 MD（单价极高、通过率未知），从没算过"每个通过判据的候选花多少核时"。
5. **YSD→BLI 全部一致**说明他们的第一道湿实验已经足够可靠，漏斗难点在**计算侧**；我们的第一道湿实验（LC-MS/MS 产物身份）本身就可能是难点，二者不能类比。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：见第 5.5 条；且补充信息里的结构验证（Supplementary Fig 9）只覆盖"YSD 命中者"，**没有对未命中者做实验验证**，因此 Type II 归因是推断而非直接观测。
- 我们读出：① 阈值 10 是**经验拐点**（"sharp increases"），不是物理常数；② 前瞻靶只有 4–5 个、成功数 1–17，**"10×"的分母极小**，不该当"预测能力"引用；③ AF2 用单序列预测全新设计——这个前提只在"设计序列规整且稳定"时成立，对**天然未表征蛋白**未必成立；④ 全文没有 MD，也没有 QM，机理层结论不在本文证据范围内。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么做）**

1. **A 段先行的组织方式**（本库判据 G0/G6）：先把"已知做过、已知产物"的反应按酶 / 反应 / 产物分层做成真值面板，再评估任何判据在面板上的判别力——判据不上考卷就不许进漏斗。
2. **失败分型 → 分步化学事件**：每个候选标注"卡在哪一个化学事件"，并允许写 UNKNOWN 与 METHOD_FAIL 两种状态。
3. **通过率与单价一起报**：任何新方法先给"每 1 个通过闸口的候选要多少 GPU·h"，再决定跑不跑（本轮实测单价：MD 156.6 ns/day、新体系 10.6 GPU·h、xTB 271 原子 153.3 s/评价）。
4. **闸口数量控制在 2 个强判据**（pAE_interaction + RMSD 这种），其余降为辅助。

**不可迁移（为什么不能照搬）**

1. **pAE_interaction<10 / RMSD<5 Å 是"会不会按设计结合"的判据，不是"会不会催化反应"的判据**。binder 的成功只看静态界面，酶设计的成功要看三步化学事件与竞争副产物，**结构自洽既不必要也不充分**。本库判据 §2 明写不许把 binder 的 pAE/ipTM 阈值当酶活闸口。
2. **"提升 10 倍"不能变成我们的成功概率**。分母 9K/2K/1–17、绝对 <1%，且他们的标签是二值结合/不结合，我们的目标连标签都没有。引用时只许引用**方法结构**，不许引用**命中率数字**做校准。
3. **他们没有 MD/QM/自由能**，所以这篇不能为"用 MD/QM 判催化"提供命中率背书；那类主张要另找参照（本文无）。
4. **酵母展示式的大通量**（一个库几万个序列）在产物化学上不存在——我们只能一轮、最多四个构建体，漏斗末端必须是**信息量最大化**（机制多样性 + 失活对照），不是**样本数最大化**。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/B09_PMC10163288_text.txt

- 本地纯文本：`fulltext/B09_PMC10163288_text.txt`（Europe PMC fullTextXML，标签剥离、HTML 实体已解码、未改写内容）。
- 对照底稿行号：`sources/baker.md:120–133`；引用汇总表：`sources/baker.md:605`（3a 自洽性反折叠闸口行）、`sources/baker.md:642`（漏斗数字对照）。
- CSV 字段映射：本文第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py`（参数：无；输入：本目录 `*.md` + `fulltext/` + `sources_map.json`）把卡内所有不含中日韩字符、且被直双引号包住的 ≥20 字符片段，在**该卡的每一份本地全文**里做逐字查找；任何一条不命中即 FAIL、退出码 1，登记的全文缺失同样算失败。本轮结果 **36/36 × 2 份全文 PASS**，见 `data/literature_cards/selfcheck.txt`；写本卡前同一脚本曾以 3 条 MISS 判 FAIL（一处把跨引文编号的两句连成一句、一处用省略号开头、一处把状态名 UNKNOWN/METHOD_FAIL 误当引句），已逐条改正后复跑通过。**反向自测**（同日上午，只在内存里改路径、不写生产产物）：把一处真引句里的 `nearly 10-fold` 篡改成 `nearly 20-fold`，并登记一份不存在的全文 ⇒ 脚本输出 `35/36`＋`SRC_MISSING`＋`REF FAIL`、退出码 1。也就是"引用造假会被机器抓到"这件事是可执行的，不是声明。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 2 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文
target=LTK、ALK、IL-2Rα site1/site2、IL-10Rα（4 个新靶 + 10 靶回顾集）
backbone_generation=Rosetta 界面设计协议（Cao 2022 管线）出骨架；序列走 Rosetta LayerDesign 或 ProteinMPNN（后者另加 FastRelax 回环 = ProteinMPNN-FR）；AF2/RF2 单序列输入复测
computational_filters=pAE_interaction（链间残基对平均 PAE）；AF2/RF2 复合物 Cα RMSD；单体 pLDDT/RMSD；对照基线 Rosetta 单体能量/链长、Rosetta ddG、DAN 精度；物理侧 Pareto-front（target_delta_sap、ddG、contact_patch、contact_molecular_surface）
thresholds=pAE_interaction<10 且 af2_complex_rmsd<5 Å；成功判据 SC50<4 μM；效率折算 100 CPU-s = 1 GPU-s
md_used=否
qm_used=否
experimental_methods=合成基因→酵母表面展示（1 μM + avidity 分选，再按靶浓度递减分选）→深测序算 SC50→E. coli 可溶表达→单浓度 BLI
pipeline_counts=~2M 设计/靶 → ~20,000 送测/靶（~15,000 物理 + ~5,000 AF2 pAE<10）→ 80,000 条合成基因 → 4 靶成功数 1–17；回顾集 ~1M 条设计、每靶实测 15,000–100,000、binder 1–584
hit_rate=AF2 过滤使成功率近 10×；LTK/IL-2Rα site1 分别 8×/30×；ALK 与 IL-10Rα 物理过滤 0 个、AF2 有；全套过滤后绝对成功率仍 <1%；IL-2Rα site2 无结合体
best_metric=未记录（本文给 YSD 的 SC50 口径，自述初始结合体处于 high nM affinity range，无统一 Kd 最优值）
cost_or_stat_note=~30 GPU-秒/设计（复合物 AF2）、单体 ~5 GPU-秒、DAN ~0.5 GPU-秒；AF2 通过仅 ~2.3%；ProteinMPNN 出序列 ~2 CPU-秒、ProteinMPNN-FR 吞吐 1 设计/120 CPU-秒；效率 Rosetta 7.6e-7 → MPNN-FR 2.2e-6（~8×）
role_in_timeline=把 Cao 2022 的近百万条湿实验标注变成"筛子考卷"，第一次定量回答漏斗该用哪个判据（界面 pAE_interaction<10），并给出 Type I/II 失败分型与"通过率÷单价"的效率口径；其阈值成为其后 binder 论文的默认闸口
source_pointer=data/literature_cards/fulltext/B09_PMC10163288_text.txt（SHA 3b4830502416a1e0…）+ data/interim/baker_lit/ft/binderDL2023.txt；sources/baker.md:120-133
CSV回填-->
