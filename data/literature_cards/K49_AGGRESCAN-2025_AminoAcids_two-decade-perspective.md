# [K49] AGGRESCAN 家族二十年——一把"序列聚集倾向"尺子是怎么一代一代补漏的

Pesce G, Solé O, Bárcenas O, Ventura S（巴塞罗那自治大学 IBB / 生化与分子生物学系 + IQAC-CSIC + Parc Taulí 研究所）
Biophysical Reviews 2026, 18:83-94（在线 2026-01-19；收稿 2025-11-28，接收 2025-12-29）· DOI 10.1007/s12551-025-01404-9 · PMID 41909611 · PMCID PMC13031676
开放获取（CC BY 4.0）· 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13031676/
（CSV 行记为 Amino Acids 2025，与全文题录不符，见 §0 与 §7）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K49**（组：通用方法学；文献类型：综述） |
| 文献类型 | **综述／方法史**（正文自述为 mini-review，只综述自家 Aggrescan 平台，不含新的自做实验；`Data availability` 明写本次研究未生成或分析数据集） |
| 本地全文 | `data/literature_cards/fulltext/K49_PMC13031676_text.txt`（56,635 B，Europe PMC 检索后取 fullTextXML 再剥标签；登记通道见 `inventory.json`：`epmc_search_then_fulltext`；同名 `_fullTextXML.xml` 为原始件） |
| 身份核验 | 底稿前 600 字符内的标题、DOI 10.1007/s12551-025-01404-9、PMCID PMC13031676 与分派行一致 ⇒ 认定是本篇；**但期刊字段不一致**（见下一行） |
| 期刊/年份不符 | 全文题录头是 `biophysrev / Biophysical Reviews / Biophys Rev`，卷 18、页 83-94、DOI 前缀 s12551（Springer 的 Biophysical Reviews 刊号）；CSV `期刊或预印本` 记 Amino Acids、`年份` 记 2025。**以全文为准**：Biophysical Reviews（2026 年卷，2026-01-19 在线）。差异已记入 §7，未改 CSV |
| 对照底稿 | `sources/cost-benchmarks.md` 第 198 行（"包涵体/不溶"判据行，仅以 DOI 转引本评述，无方法细节）——本卡内容一律取自全文，未从该行取材 |
| 证据级别 | **全文级**（本卡所有英文引句均可在该份本地纯文本里逐字命中；见 §9 自检）。**CSV 行 `证据级别` 列仍为 摘要级（旧值），该列不在 14 键回填范围内，未擅自改表** |
| 未取到的部分 | Fig 1-3 只有图注文字、无原图数值；A4D 基准的逐例结果在其原文补充材料里（本卡只引到"18 例／300 余篇"这一层）；AGGRESCAN 逐残基聚集标度的具体数值表不在本文（本文只描述其来源与用法）；A3D/A4D 的 Web 服务参数页不在本文 |

## 1. 这篇到底解决什么（大白话）

它不报告新实验，而是回答一件事：**自家那把"预测蛋白哪里爱聚集"的尺子，二十年里是怎么一代代补漏的、每一代补的是哪一类失效**。写法是"失效驱动"的编史：2007 AGGRESCAN 只用线性序列（第一批同类工具只看物化标度和统计力学，不吸收生物学测量），于是对球状蛋白会高估、且把空间上凑在一起的残基当远亲；2015/2019 Aggrescan3D 把聚集标度投影到三维结构上、只算暴露面并加柔性采样；2024 Aggrescan4D 再加 pH 环境维度、直连 AlphaFold 数据库取结构、并换成基于进化保守的突变建议。它同时给出这条家族的验证证据（在大肠杆菌里高分为包涵体、低分为可溶；A3D 系统基准；A4D 在 18 例 pH 定量案例上的表现）与应用面（抗体可开发性、神经退行、晶体蛋白、抗菌肽、酶与生物材料改造），最后落到"还缺什么"：数据稀缺、能量学简化、翻译后修饰、全原子动力学、相分离与规模化部署。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **纯序列尺子对球状蛋白系统性高估**。难点：序列算法把埋在水合核心里的疏水段也算进总分。原句证据："Because the hydrophobic core is not solvent-exposed under physiological conditions, including its contribution, leads to an overestimation of the aggregation propensity of the native protein." 与更早的自陈："Nevertheless, because AGGRESCAN relies on linear sequence information, its applicability to folded, globular proteins is limited"。→ **做了什么**：出 A3D，把 AGGRESCAN 标度投影到结构坐标上，只统计溶剂可及残基的贡献，并按暴露程度加权（全暴露满贡献、部分暴露按比例、低于 10% 暴露直接剔除）。→ **仍留下的代价**：判据换成"必须有结构"，且 10% 这个截断值是人为设定，文中未给该阈值的敏感性分析。
2. **序列邻近不等于空间邻近**。原句证据："Additionally, sequence proximity does not necessarily correspond to spatial proximity: residues that are adjacent in the sequence may lie far apart in the folded structure, while distant residues can cluster in three-dimensional space." → **做了什么**：从"线性 APR"改提"结构聚集倾向斑块 STAP"，对每个残基以其α碳为中心取球形邻域（默认半径 10 Å，见 Fig. 2 B 图注），把邻域内所有暴露残基按距离加权平均——这等于把滑窗从一维搬到三维。→ **代价**：邻域尺度与权重函数由结构精度决定；无结构的蛋白只能靠外部模型补（这也是后来接 AlphaFoldDB 的动因）。
3. **静态结构会低估风险**。原句证据："In 80% of the cases surveyed, the average of all conformations was higher than that of the static structure, suggesting that the starting structure may lie within a local structural minimum that underestimates aggregation risks of the ensemble" → **做了什么**：在 A3D 里接入 CABS-flex 粗粒度分子动力学做构象采样，从输入结构生成 12 个构象，取构象系综平均，捕捉晶体结构里看不到的瞬态暴露斑块。→ **代价**：粗粒度不是全原子，作者自己在展望里承认这是待升级项："Current flexibility modeling relies on CABS-flex simulations."（并列出希望引入全原子 MD、温度/氧化/拥挤等应力条件）。
4. **可定量的实验基准数据稀缺**。原句证据：A4D 的定量基准 "Finally, Aggrescan4D was benchmarked on 18 cases that met the criteria for quantitative evaluation, selected from over 300 peer-reviewed studies reporting pH-dependent changes in protein aggregation or solubility."；作者也把这件事列为现存问题："Moreover, the availability of reliable, well-annotated experimental datasets-particularly those reporting pH-dependent aggregation or solubility behavior across defined structural states-remains limited, constraining rigorous benchmarking, comparative assessment, and effective model optimization." → **做了什么**：从 300 余篇文献里按可定量标准筛出 18 例做对照（数据与其原文补充材料一起公开），并把"数据稀缺"写进局限与未来计划（希望用深度突变扫描与蛋白质组聚集谱做训练/验证集）。→ **代价**：18 例的样本量下，"完美预测表现"这种说法分母极小；本文未解决数据稀缺本身。
5. **突变建议可能伤结构/功能**。原句证据（A3D 一代的做法）："Its user-friendly mutational design protocol allows researchers to introduce targeted substitutions at selected residues or to apply an automated mutation scheme that prioritizes the most aggregation-prone sites and proposes charge-based solubilizing mutations." 代价评估靠能量学工具外挂："To assess the energetic effect of these mutations, the pipeline integrates FoldX calculations"。A4D 一代改为按进化保守性选突变："Aggrescan4D also incorporates a new mutation protocol based on evolutionary substitution matrices." 与 "This new protocol introduces evolutionarily conserved solubilizing mutations to minimize the effects of mutations on protein structure and function." → **仍留下的代价**：作者自评能量学层仍是简化假设——"Current stability calculations and mutation impact predictions rely on simplified energetic and structural assumptions that, while computationally efficient, may not fully capture the complex interplay between folding, conformational dynamics, and aggregation, underscoring the need for refinement supported by systematic experimental validation."
6. **环境维度与翻译后修饰：一个刚补上、一个仍未做**。pH 这一维在 2024 补上（"The incorporation of environmental pH effects enhanced the physiological relevance of the predictions"），并给出工业侧动机："Moreover, in industrial settings, it offered the opportunity to control aggregation simply by tuning buffer conditions rather than altering the protein sequence, thereby reducing the risk of destabilizing the fold and avoiding complications related to manufacturability or intellectual property."；但磷酸化/泛素化/糖基化/乙酰化**本文未解决**，只写成计划："While Aggrescan4D allows users to simulate structural exposure and charge-state changes, future versions could include explicit modeling of PTMs at the sequence and structural levels."
7. **预测与实验之间仍有反向不一致**。转述案例：HγD-crystallin 的 W42 突变体系里，作者原预期"更极性或更小的侧链应当更安全"，实测打分相反——"Unexpectedly, polar and/or small residue mutations produced, on average, the highest A3D score values over the course of the simulation." → **他们（被转述的研究者）做了什么**：改用 MD 轨迹上的 A3D 打分而非静态结构，并提出机理解释："The authors hypothesized that the smaller-sized side chains lead to the opening of a small pore, allowing water molecules to enter the hydrophobic core of the N-terminal, resulting in unfolding and exposure of the hydrophobic core."（这是综述转述他人工作，不是本文自做）
8. **规模化部署与判据边界**。作者承认 Web 服务不满足蛋白质组级/工业高通量需求："Standalone versions of AGGRESCAN and Aggrescan4D are currently under development, with plans to use them in distributed computing networks and academic supercomputers, helping broaden their adoption and support real-time design in large teams or across institutions."（**尚未交付**）。对液-液相分离，本文划清边界而不是扩口——"While Aggrescan is not intended to predict condensate formation per se"，只主张它能为凝聚体老化/不可逆转变提供机理线索（**本文未解决**，属展望）。

## 3. 方法与工作流程

### A. 综述自身的组织方法（这篇"怎么把二十年写成一条线"）

| # | 输入 | 操作 | 判据／阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 自家三代工具（AGGRESCAN 2007 / A3D 2015 与 2.0 2019 / A4D 2024）+ 前代工具（TANGO、PASTA、WALTZ、FoldAmyloid）的时间线 | 按 Fig. 1 的**发布时间轴**排列，把每一代绑定到"它要修的上一代失效类别"，而不是按功能列表平铺 | 分代依据写死在正文：序列 vs 结构 vs 结构+环境；SAP 2009 被标为"从序列转向结构"的界碑，CamSol 3.0（2023）被标为"环境敏感预测"的起点（图注原文把它写成 structure-based，而它引用的原论文标题是序列法——本文这里以图注转述，存疑，见 §7） | 三代自家算法 + 4 个前代算法 + 2 个竞品（SAP、CamSol 3.0）的相对位置 |
| A2 | 每代算法的原始方法文献（Conchillo-Solé 2007；Zambrano 2015；Kuriata 2019a/19b；Pujols 2022；Badaczewska-Dawid 2022；Bárcenas 2024；Zalewski 2024 等） | 逐代拆成"打分标度来自哪 → 窗口/邻域怎么算 → 阈值怎么定 → 输出什么"四问，并用 Fig. 2 A/B 图注把两代算法的差别写成对照 | 判据以原文给的数字为准：滑窗窗口按链长分档（5/7/9/11）、hotspot 需连续≥5 个残基且不含脯氨酸、暴露低于 10% 不计、球形邻域默认 10 Å、CABS-flex 生成 12 个构象 | 一节一段的算法卡片，读者可据此复算，不需查原工具文档 |
| A3 | 验证证据 | 分三层摆：**内部**（A4D 定量基准）、**横向**（与其它预测器比较）、**前瞻**（自家实验室用 A3D 改造 GFP 的可溶变体） | 内部基准的入选口径是"met the criteria for quantitative evaluation"，从 300 余篇里只留 18 例；横向结论只写成"显著更好的灵敏度/特异度/精确度"（本文未给具体数值） | 三层证据各自的强度差别被明写出来（本文自己称早期证据为 anecdotal evidence） |
| A4 | 应用文献（抗体/S100B/cofilin-1/γD-晶体蛋白/胰岛素/抗菌肽/醇脱氢酶/Reteplase/卵白蛋白肽凝胶） | 按"用哪一代工具 + 是否被实验证实 + 证实到什么程度"排比，不平均着墨 | 每个案例都给出实验回收率或验证方式（如胰岛素 4 个预测区里 HPLC-MS 证实 2 个；cofilin-1 四种预测器里只有 AGGRESCAN 找出 9 区） | 6 类应用场景（可开发性、致病机理、生理性聚集体、肽类抗菌、酶改造、生物材料） |

### B. 被综述对象的工作流（三代算法各自怎么跑；阈值来自全文）

| # | 输入 | 操作 | 判据／阈值 | 输出与规模 |
|---|---|---|---|---|
| B1（AGGRESCAN 2007，打分标度的来历） | Aβ42 中央疏水簇的点变体库（对 Phe19 做突变扫描，得 20 个肽变体） | 把变体融合到 GFP 上游在大肠杆菌里表达，用 GFP 荧光当聚集读数（上游肽聚集 ⇒ GFP 折不起来 ⇒ 荧光下降） | 逐残基聚集倾向由荧光读数反推；该经验标度随后被拿去与正辛醇分配疏水性标度、Kyte-Doolittle 标度和β折叠倾向对照，作者称其强相关 | 一张**逐残基聚集倾向标度**（后来所有代都用它当底层分数） |
| B2（AGGRESCAN 2007，打分） | 任意氨基酸序列 | 滑窗平均：窗口中心残基取窗口内各残基聚集值的平均；为模拟末端化学环境，N 端加一个虚拟碱性残基、C 端加一个虚拟酸性残基；无法入窗的末端残基取最近窗口的值 | 窗口按链长动态取 5／7／9／11（对应 ≤75、≤175、≤300、>300 残基四档）；hotspot 阈值取"按 SwissProt 频率加权的平均分"；hotspot 定义＝连续 5 个以上残基超阈且不含脯氨酸（脯氨酸是强β断裂子） | 每个位点一个 AAP（Average Aggregation Propensity）值的完整剖面 + hotspot 清单及其相对强度 + 整条肽链的总分 |
| B3（A3D 2015／2.0 2019，结构投影） | 蛋白质三维结构（单体或多链复合体） | 判定溶剂暴露 ⇒ 只让暴露残基参与 ⇒ 以每个残基为中心取球形邻域、按距离加权平均 ⇒ 得到局部结构聚集分；配色为蓝（可溶）到红（易聚集） | 完全暴露贡献最大、部分暴露按比例、**暴露低于 10% 的残基不计入**；默认邻域半径 10 Å（Fig. 2 B 以 BSA 第 228 位缬氨酸为例说明） | 逐残基三维聚集图 + 空间聚集斑块 STAP（可跨链）；A3D 2.0 另有面向人蛋白质组的预计算库（本文以文献转述） |
| B4（A3D 柔性采样） | 输入结构 | CABS-flex 粗粒度分子动力学采样 ⇒ 构象系综 ⇒ 对每个构象算 A3D 分数再平均 | 生成 12 个构象；判据是系综平均分高于静态结构分数即说明静态结构低估 | 揭示静态晶体里被埋住的瞬态暴露 STAP；80% 被调查案例中系综平均高于静态结构 |
| B5（A3D／A4D 改造回路） | 打分结果 | 挑最易聚集位点做突变建议：A3D 走电荷型增溶突变（手动指定或自动方案），A4D 改用进化替换矩阵给保守增溶突变 ⇒ 再用 FoldX 估每个突变的折叠自由能变化 | 增溶与稳定两条线一起看：聚集分下降 + ΔΔG 不显著负向（本文未给 ΔΔG 数值门槛） | 一张"该改哪几位、改成什么、会不会拆结构"的可下单突变清单；本家族最常被引用的自证成果是用 A3D 改造出作者称迄今最可溶的 GFP 变体 |
| B6（A4D 2024，环境维 + 结构来源） | UniProt 登录号 + 目标 pH | 直连 AlphaFold 数据库取模型（无需实验结构）⇒ 按 pH 调节氨基酸固有亲脂性/电荷态后重算结构聚集分 | pH 依赖来自前序工作：Zamora 2019 的 pH 依赖氨基酸亲脂性标度（连续介质溶解计算）、Santos 2020 与 SolupHred 2021 把 pH 写进打分函数 | 同一蛋白在不同 pH/不同亚细胞环境下的聚集分对照；工业侧的替代路径是"调缓冲条件而不动序列" |

**这套流程的骨架值得单独记住**：它的推进逻辑不是"换更好的模型"，而是**每发现一类系统性失效，就加一个维度**（序列 → 结构 → 构象系综 → pH 环境 → 结构来源与突变建议），并且每一维都能追到一条生物学读数（GFP 荧光、包涵体比例、HPLC-MS、体外纤维）。

## 4. 关键数字台账（数值 · 含义 · 出处，全部可在本地全文里搜到）

| 数值 | 含义 | 出处（原句片段／位置） |
|---|---|---|
| 20 个肽变体（对 Phe19 扫描） | AGGRESCAN 经验聚集标度的实验底料 | "A mutational scan of position Phe19" 段；GFP 融合 + 大肠杆菌荧光读数 |
| 2007 / 2015 / 2019 / 2024 | AGGRESCAN、A3D、A3D 2.0、A4D 发布年 | "AGGRESCAN - 2007"、"Aggrescan3D & Aggrescan3D 2.0-2015 & 2019"、"Aggrescan4D - 2024" 三个小标题 |
| 窗口 5 / 7 / 9 / 11 | 滑窗尺寸按链长 ≤75 / ≤175 / ≤300 / >300 残基分档 | "The window size was adjusted using a known database of amyloidogenic proteins, dynamically adapting it to protein length (5 for ≤ 75 residues, 7 for ≤ 175 residues, 9 for ≤ 300 residues, and 11 for > 300 residues, respectively)."（含≤符号，此处按中文叙述） |
| 连续 ≥5 个残基 + 不含脯氨酸 | hotspot（聚集热点）的定义 | "aggregation hotspot regions-defined as stretches of five or more consecutive residues with scores above the hotspot threshold" |
| 暴露 <10% 不计 | A3D/A4D 里残基是否参与打分的一刀切阈值 | "residues with < 10% exposure are excluded from the calculation" |
| 10 Å（邻域半径，默认） | A3D/A4D 球形邻域大小；示例为 BSA 第 228 位 | Fig. 2 B 图注（示例句含 Å 符号，不列入引句，此处以中文叙述） |
| 12 个构象 | CABS-flex 由一个输入结构产生的构象数 | "generating 12 conformers from the input structure and identifying transiently exposed STAPs that would remain hidden in a static crystal structure" |
| 80% | 被调查案例里"系综平均分 > 静态结构分"的比例 ⇒ 静态结构低估 | "In 80% of the cases surveyed, the average of all conformations was higher than that of the static structure" |
| 18 例 / >300 篇 | A4D 定量基准的可用案例数与其筛选自的文献数 | "Aggrescan4D was benchmarked on 18 cases that met the criteria for quantitative evaluation, selected from over 300 peer-reviewed studies" |
| 1,500 次以上 | 本文给出的该套件被引规模（唯一的"影响力"数字，无对照口径） | "Globally recognized and cited over 1,500 times, the Aggrescan suite has established itself as a valuable and reliable resource for researchers worldwide." |
| 4 个预测区 → 2 个被证实 | 胰岛素及其类似物里 AGGRESCAN 等工具预测的 APR 数与实验回收（A 链 1 个、B 链 3 个；HPLC-MS 证实 2 个） | "Their analysis revealed one APR in the A chain and three in the B chain." / "Subsequent experimental validation using HPLC-MS confirmed two of the four predicted regions." |
| 4 个预测器 → 9 个区 | cofilin-1：AGGRESCAN 与 TANGO、FoldAmyloid、AmylPred2 并列测试，只有 AGGRESCAN 找出 9 个易聚集区 | "Among four aggregation predictors tested (AGGRESCAN, TANGO, FoldAmyloid, and AmylPred2), AGGRESCAN uniquely identified nine aggregation-prone regions, demonstrating superior sensitivity." |
| 96 条肽 → 1 条（Oct-P2） | A3D 2.0 用于肽类排序的通量示例（章鱼抗菌肽） | "They used Aggrescan3D 2.0 to rank the aggregation propensity of 96 peptides and identified Oct-P2 as the peptide with the highest A3D score." |
| 0 个新数据集 | 本文（综述）自身没有实验、没有产出/分析数据 | Data availability 声明："No datasets were generated or analysed during the current study." |

## 5. 结论——作者说了什么

1. AGGRESCAN 的历史意义在"**经验标度**"：它是第一批把生物学测量（细胞内聚集读数）而不是物化直觉当作底层标度的预测工具；早期工具"were based on physicochemical scales and statistical mechanics and did not incorporate biological measurements of aggregation"。
2. 三代工具的演进被作者归纳为：序列 ⇒ 三维结构上下文 ⇒ 环境（pH）条件，并且新近的 AlphaFold 整合把这套分析推到蛋白质组规模。
3. 验证侧作者主张：预测高分者在大肠杆菌里成包涵体、低分者保持可溶；预测的 APR 与α-突触核蛋白、Tau、朊蛋白、IAPP 等"实验确认过的关键片段"重合；A3D 相对其它预测器在灵敏度/特异度/精确度上更好；A4D 在 18 例定量基准上"达到完美预测表现"并优于唯一同类（CamSol 3.0）。
4. 应用侧作者主张：同一把尺子既能改良性状（抗体可开发性、酶与胰岛素、可溶 GFP 变体、Reteplase、醇脱氢酶），也能反向利用聚集（抗菌肽 Oct-P2、卵白蛋白肽水凝胶），还能揭示机理（S100B 的抗聚集表面、cofilin-1 的半胱氨酸氧化机制、γD-晶体蛋白的部分解折叠孔道）。
5. 作者自陈的局限：能量学与突变效应仍建立在简化假设上；可靠的、标注良好的实验数据集（尤其 pH 依赖、跨结构态的）仍然稀缺，这既卡住基准也卡住把 PTM、拥挤等变量加进模型；柔性建模仍靠 CABS-flex；standalone 版本仍在开发中。作者并未把本文当成性能评测或前瞻命中率报告。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

以下为推断，非作者原文。

1. **"每加一维都要能用生物学读数验证"是这条线能活二十年的原因**：从 GFP 荧光到包涵体到 HPLC-MS。→ 对我们：任何新加的描述符（比如某条活性口袋几何轴）如果不能被一个便宜的湿实验读数校准，它进入漏斗的速度就该被压住。
2. **本文最有价值的迁移物是"上限"而不是"分数"**：作者自己承认高分/低分与可溶性的关系只在**大肠杆菌异源表达**这一口径下成立；到胰岛素那种"没有标准方法"的场合，4 个预测区只回收 2 个。这条家族二十年的努力，本质上一直在补"序列聚集倾向与实验可溶性相关性上限"的漏。
3. **"辅助工具互补"被反复强调**（CamSol 与 Aggrescan 并用、FoldX 与 A3D 并用）——单一聚集分从不单独决定结论。→ 我们的漏斗也应把"聚集倾向"降为并列证据之一，而不是裁决项。
4. **18 例基准 vs 300 篇文献这个对比本身就是结论**：不是模型不行，是**带结构态标注的可定量实验数据不够**。→ 我们项目"没有一条被产物化学确认的天然 UAA 合成酶"是同一个瓶颈类型（分母问题），不是算法问题。
5. **综述里"只有 AGGRESCAN 找出 9 区"这类单一案例比较，不能读成"AGGRESCAN 比其它工具准"**：n=1、且没有阴性对照。我们引用时必须把这类句子标注为轶事级证据。

## 7. 局限与失败（作者的 + 我们读出的 + 与 CSV 行不符之处）

- **作者自陈**：见 §5 第 5 条（简化能量学、数据稀缺、PTM 未建模、粗粒度柔性、standalone 未交付、不做相分离预测）。
- **我们读出的**：① 全文没有任何 ROC、AUC、相关系数或前瞻盲测数字，所有"更好"都是转引原论文的定性结论；② A3D 的系统基准数值（灵敏度/特异度具体值）本文未给出，只说"significantly improved"；③ hotspot 阈值是"按 SwissProt 频率加权的平均分"这种内部归一，不是跨蛋白可比的绝对标尺；④ 10% 暴露截断、10 Å 邻域、12 个构象这三个参数在本文里没有敏感性分析；⑤ 综述由工具作者自己撰写（同一实验室），"迄今最可溶的 GFP 变体""完美预测表现"是自评而非第三方复现；⑥ 应用案例的证据强度不齐——从"6 种工具打分 + 一条凝胶"到"四种预测器比较中只有一种命中"都被平铺在同一节里；⑦ Fig. 1 图注把 CamSol 3.0 描述为 "structure-based, environment-sensitive aggregation prediction" 的起点，但它引用的原论文是序列法（"Sequence-based prediction of pH-dependent protein solubility using CamSol"），此处图注与其引文库标题自相矛盾，本文未澄清——本文里最可疑的一处。
- **与 CSV 行不符（以全文为准）**：① 期刊：CSV 记 Amino Acids，全文题录是 Biophysical Reviews（DOI 前缀 s12551 亦属该刊）；② 年份：CSV 记 2025，全文为 2026 年卷（2026-01-19 在线，2025-11-28 收稿 / 2025-12-29 接收）；③ `PMID/PMCID/arXiv` 列 CSV 记 未记录，实际为 PMID 41909611 / PMCID PMC13031676；④ `证据级别` 列 CSV 仍为 摘要级（旧值），本卡按全文级写；⑤ `是否用MD`／`是否用QM` 两列 CSV 记 未记录，全文实为：MD 以"综述转述的方式"出现（CABS-flex 粗粒度采样是 A3D 的内置模块；另转述一个 MD 轨迹 + A3D 联用的他人研究），QM 未被本文使用。以上差异**只记录不改表**（CSV 与 `sources/*.md` 均非本代理写域）。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"序列聚集倾向可作廉价预筛"这一层直接可用**：AGGRESCAN 级别的滑窗打分是 CPU 秒级、无需结构、可批量，适合放在漏斗很前面把明显不溶的构建体剔掉，或在同一条候选上比较不同突变体的相对优劣（"enabling direct comparison of sequence variants"）。我们的用法：对候选酶及其变体算相对排名，不问绝对阈值。
2. **"每加一维都要配一个便宜读数"的工程纪律**：本文三代各自绑定一个实验口径（荧光／包涵体／pH 定量案例）。我们的漏斗若要加新维（如口袋几何、催化残基保守度），应同步写清"哪一条湿实验读数能在短期内校准它"，否则不进闸口。
3. **"调环境而不动序列"作为平行分支**：A4D 的工业动机（改缓冲条件即可控聚集，避免拆折叠与专利问题）对应我们的可执行分支：当某候选被聚集轴卡住时，先把它当成表达/缓冲条件问题（温度、pH、融合标签、辅因子浓度）而不是立刻放弃该靶。
4. **把"预测—能量—可溶"三件分开记账**：A3D 用聚集分 + FoldX ΔΔG 两条独立证据，而不是把它们合成一个分。我们保留"聚集倾向 / 折叠稳定性代理 / 催化位点完整度"三条独立列，不做单值合分。

**不可迁移（为什么不能照搬）**

1. **本文没有可借的命中率**。它既没有 AUC，也没有前瞻漏斗的通过率；唯一的"完美预测表现"是 18 例自评基准，且**分母与口径都不是酶活**。把这类聚集类工具的性能数字当作 UAA 酶活判据、或换算成"我们的成功概率"，属于口径挪用（本项目的 DP2R 标准同样禁止把 binder 类阈值当酶活闸口）。
2. **"高分=包涵体、低分=可溶"的验证只在大肠杆菌异源表达这一口径成立**；UAA 合成酶筛的不只是可溶，还包括三步化学事件与竞争副反应，可溶既非必要也非充分。预筛剔掉的是"根本不表达"的浪费，不能反过来把"表达了"当成支持催化的证据。
3. **本文没有催化层信息**：没有活性位点几何、没有过渡态/自由能计算（QM 未被使用，MD 只是 A3D 的构象采样模块与他人案例的转述）。因此它不能为"用 MD/QM 判催化"提供任何命中率背书。
4. **pH 依赖打分要谨慎移植**：A4D 的 pH 项建立在氨基酸固有亲脂性/电荷态的连续介质标度上，其 18 例基准针对的是聚集体/溶解度读数，不是酶动力学；我们若要引入 pH 维度，必须先确认目标反应的缓冲窗口与聚集读数口径一致。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K49_PMC13031676_text.txt

- 本地纯文本：`data/literature_cards/fulltext/K49_PMC13031676_text.txt`（56,635 B；Europe PMC 检索后取 fullTextXML，剥标签、HTML 实体已解码、内容未改写；原始件同目录 `_fullTextXML.xml`）。同一论文只登记了这一份抽取版本，因此所有引句只需对该文件逐字命中。
- 只读参考：`sources/cost-benchmarks.md:198`（该行的 `证据级别` 旧值即"摘要级"的出处；本卡未从中取材，也未修改它）。
- CSV 字段映射：§3 ↔ `计算筛选判据/阈值数字/候选生成方法`；§4 ↔ `候选数递减/成本统计引用`；§7 ↔ `核验状态/期刊与年份字段`；§8 ↔ `在方法演进链的位置`。
- 与原文不符之处的处理：凡卡内数字/年份/期刊与全文冲突，均以全文为准并在 §7 列出；本文（综述）自身无实验、无数据产出，故 `实验验证手段`、`实验命中率`、`Kd或活性最好值` 三键按"不适用/未记录（原因）"写，未从被转述研究中冒领结果。
- **本卡自检**：`python scripts/verify_literature_cards.py --only K49 --no-report`（不写共享报告文件）把卡内所有不含中日韩字符、被直双引号包住的 ≥20 字符片段，在声明的这份底稿里逐字查找。本轮结果见交付回报；含非 ASCII 符号（Å、≤、β、Δ、重音字母）的句子一律改为中文叙述写数字，不放进英文引号。

<!--CSV回填
work_type=综述/方法史（正文自述 mini-review，无新实验；Data availability 声明本次研究未生成或分析数据集）
target=蛋白聚集倾向与可溶性的序列/结构/环境依赖预测（APRs 与 STAPs），对象为治疗性蛋白、神经退行相关蛋白、酶与肽类材料，非 UAA 酶设计
backbone_generation=不适用（本文不生成骨架）；被综述算法：AGGRESCAN 2007 滑窗序列打分、Aggrescan3D 2015/2.0 2019 结构投影+柔性采样、Aggrescan4D 2024 加 pH 维与 AlphaFoldDB 取结构
computational_filters=AGGRESCAN 经验聚集倾向标度 + 滑窗平均 AAP 剖面与 hotspot 识别；A3D/A4D 溶剂暴露加权的三维邻域打分（STAP）；CABS-flex 构象系综平均；FoldX 折叠自由能变化评估突变代价；A4D 进化替换矩阵给保守增溶突变；横向对照 CamSol 3.0、TANGO、PASTA、WALTZ、FoldAmyloid、AmylPred2
thresholds=滑窗按链长分档 5/7/9/11（对应 ≤75、≤175、≤300、>300 残基）；hotspot 需连续 ≥5 个残基超阈且不含脯氨酸；hotspot 阈值取按 SwissProt 频率加权的平均分；溶剂暴露低于 10% 的残基不计入；球形邻域默认半径 10 Å；CABS-flex 生成 12 个构象；A4D 定量基准 18 例（筛自 300 余篇）；FoldX ΔΔG 未给数值门槛（原文未给阈值）
md_used=是（综述转述，非本文自做）：A3D/A4D 内置 CABS-flex 粗粒度分子动力学采样 12 个构象以捕捉瞬态暴露斑块；另转述他人 MD 轨迹 + A3D 联用的 γD-晶体蛋白案例；本文未运行任何模拟
qm_used=否（本文无量子化学计算；仅转述 A4D 的 pH 依赖氨基酸亲脂性标度来自他人连续介质溶解计算 Zamora 2019）
experimental_methods=本文无实验；综述转述的验证口径为：大肠杆菌表达的高分形成包涵体/低分保持可溶、GFP 融合荧光聚集读数、α-突触核蛋白与 Tau 等 APR 与实验片段重合、A3D 系统基准（灵敏度/特异度/精确度）、A4D 在 18 例 pH 定量案例上的对照、案例侧 HPLC-MS 与体外纤维/细胞实验
pipeline_counts=无自建漏斗；转述的案例规模：A4D 基准 300 余篇筛至 18 例、胰岛素 4 个预测 APR 中 2 个被 HPLC-MS 证实、96 条章鱼抗菌肽经 A3D 2.0 排至 Oct-P2、cofilin-1 四种预测器中 AGGRESCAN 独占 9 个易聚集区、Aβ42 Phe19 突变扫描得 20 个肽变体
hit_rate=不适用（本文未给前瞻命中率或 ROC/AUC 类数字；作者自评 A4D 在 18 例基准上达到完美预测表现，属小样本自评，不可外推）
best_metric=未记录（本文无 Kd 或活性最优值；最接近的性能表述为 A4D 的 18 例基准优于 CamSol 3.0，未给具体数值）
cost_or_stat_note=方法评述；无单价/机时统计；给出计算取向为"AGGRESCAN 因可解释、免费、计算便宜而适合蛋白质组级大规模分析"；唯一影响力数字是被引 1,500 次以上；柔性采样使静态结构低估风险的案例占 80%；作者列出的瓶颈是可靠标注实验数据集稀缺与能量学简化假设
role_in_timeline=聚集类判据的方法学背景与谱系梳理：把 2004-2024 聚集预测从序列到结构到环境敏感（含 AlphaFold 整合）的三代演进写成失效驱动的时间线，明确本家族只做溶解度/聚集倾向、不做催化与相分离预测；CSV 原记其为"聚集类判据的方法学背景"仍成立
source_pointer=data/literature_cards/fulltext/K49_PMC13031676_text.txt（PMCID PMC13031676，PMID 41909611，DOI 10.1007/s12551-025-01404-9）；只读参考 sources/cost-benchmarks.md:198；期刊字段以全文题录 Biophysical Reviews 2026, 18:83-94 为准（CSV 记 Amino Acids 2025 与全文不符，未改表）
CSV回填-->
