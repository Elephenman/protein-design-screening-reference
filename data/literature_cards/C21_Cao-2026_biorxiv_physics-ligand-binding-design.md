# [C21] 物理判据放进生成循环：de novo 配体结合与传感设计（曹龙兴组，bioRxiv 2026 预印本 v1）

Zhang Y, Ke Y, Zhi R, Jin Q, … Liu J, Cao L（西湖大学生命科学学院 / AI 药物设计核心实验室）
De novo design of ligand binding and sensing with a physics based generative approach
预印本 v1 · DOI 10.64898/2026.07.13.738243（2026-07-13 投稿，页面标注 Posted July 14, 2026）· Europe PMC PPR1279910 · **未经同行评审**
本地底稿 https://www.biorxiv.org/content/10.64898/2026.07.13.738243v1（抽取文本不含 Methods 与 Supplementary）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C21**（组：曹龙兴组） |
| 标题 | De novo design of ligand binding and sensing with a physics based generative approach |
| 作者 | Zhang Y（张彦哲）, Ke Y（ Ke Yitao）, Zhi R, Jin Q, Feng Y, Wang C, Fang M, Liao J, Chen D, Liu J, **Cao L（曹龙兴，末位通讯）**；通讯邮箱 caolongxing{at}westlake.edu.cn；单位：西湖医学生命科学与技术研究院/生命学院 基因表达国重 + AI 药物设计核心实验室 |
| **版本与日期（预印本，未同行评审）** | **bioRxiv v1**，DOI 10.64898/2026.07.13.738243（编号里嵌的日期 2026.07.13 = 投稿日），页面标注 "Posted July 14, 2026"；引文格式行： "bioRxiv 2026.07.13.738243; doi: https://doi.org/10.64898/2026.07.13.738243"；Europe PMC 记录号 PPR1279910；本地底稿对应 URL https://www.biorxiv.org/content/10.64898/2026.07.13.738243v1 |
| 本地全文 | `data/literature_cards/fulltext/C21_PPR1279910_text.txt`（57,102 字符）；同目录 `C21_PPR1279910_fullTextXML.xml`（238,736 B，实为 bioRxiv 页面 HTML，非 JATS）；`batches.tsv` 第 19 行 `state=FULLTEXT`、`fetch_status=OK`、`fetch_note=fallback_ok[biorxiv_full]` |
| **全文覆盖范围（重要）** | 抽取文本含 Abstract、Introduction、Design pipeline、四节 Results（小分子/神经递质/金属/晶体）、Sensor 两节、Characterization、Discussion、Figure legends（Fig 1–5）、参考文献。**不含 Methods、不含任何 Supplementary 图/表正文**，也没有 Code/Data availability 段（在本底稿里检索 `Methods` 只命中参考文献条目名，如 Nature Methods 与 Methods in Enzymology；`Code availability` 与 `Data availability` 两个词串则完全不存在）。因此本文所有"过滤阈值"在本底稿里只能引到**定性描述**，无法引到数字；本卡在相应位置明写"原文未给阈值" |
| 证据级别 | 正文级 + 图注级逐字可核（本卡全部引句均可在本地全文逐字命中）；**方法细节级别低于正文**：Methods 与 Supp 未获，故不做任何"补充材料里可能给了阈值"的推断 |
| 对照底稿 | `sources/cao.md` 第 333–349 行（先行调研卡），第 421 行（漏斗对照表 C21 行）、第 455 行（MD 扫描结论）、第 462 行（QM 用途）、第 480 行（预印本未经独立复现的风险标注） |
| 身份复核 | 本地全文首尾的作者串、标题、DOI 与 CSV 行一致；文末 "Posted July 14, 2026" 与 `sources/cao.md:334` 的"2026-07-13 预印本"同一条记录（投稿日 vs 上线日） |

## 1. 这篇到底解决什么（一句话）

一句话：他不做"先造一百万个骨架再去筛哪个能结合"的筛选式路线，而是**把配体（小分子构象系综或金属配位几何）预先做成能量场（RIF），让骨架在蒙特卡洛折叠模拟里边长边被这个能量场打分**，于是物理判据出现在漏斗最上游（生成引导），机器学习判据（AF2 比对）只放在最下游做结构一致性复核；然后用"高骨架多样性 × 几十条量级的全量送测"直接换命中率（DTG 14/96、CIA 20/94、血清素 6/38、多巴胺 1/33、每个金属 10 条），并把结合体改造成配体诱导再折叠/片段重组的传感器（血清素、多巴胺、锌）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **做结合体容易、做传感器难：结合不等于构象变化**（全文开篇的立论）。原文："yet converting these designs into functional sensors remains a major challenge due to the need for"；对现有深度学习方法的判断是 "these designs typically emphasize static, high-affinity binding,"。
   **他们做了什么**：把"可拆分/可耦合折叠"写进生成目标而不是事后改造——"Our objective was to generate protein scaffolds that are readily adaptable for biosensor development"，做法是只生**规则螺旋束**（4/5/6 螺旋）拓扑，并让 apo 态故意不稳定：金属体系明写 "The use of such small scaffolds was intended to ensure that, in the absence of the metal ion,"，即"配体结合=折叠=全局构象变化"。
   **代价**：牺牲亲和力上限与骨架类型上限（全部限定为螺旋束，天然小分子受体常见的 β-桶/多层结构被排除在本方法能力外）。
2. **传统物理路线靠"预造口袋库 + docking"，对每个新配体都要重铺库**。原文："the vast chemical diversity of small molecules means that scaffold libraries rarely contain"，并把这种类比挑明：虚拟筛选需要 "extremely large chemical libraries"（该句在原文里紧跟引文编号 20、21，故此处只引前半句）。
   **他们做了什么**：倒过来做——"Rather than relying on the docking of"，改为骨架绕配体从头长；Discussion 收口 "our method eliminates the reliance on"。
   **代价**：每换一个新配体都要重跑一次配体侧准备（构象采样 + 聚类 + QM 精修 + RIFGen 建表），且**本文全程没有报生成规模与算力成本**（正文/图注/结论里没有 GPU 时、CPU 时、每条设计的耗时；`cost_or_stat_note` 因此只能填未记录）。
3. **可解释性与可控性 vs 深度学习**：原文 "most deep learning based approaches lack"。
   **他们做了什么**：把机器学习模型放在两个不同的位置上——生成与打分一律用物理项（RPX 折叠 + RIF 结合），**AF2 只在末端做复核**："the structural accuracy of the final models was"；序列端才用神经网络（ProteinMPNN，变体阶段 LigandMPNN）。注意：**这里的 AF2 复核没有给任何阈值**（原文未给阈值），所以它既不是可复算的闸口，也不能被引用为提效证据。
   **代价**：AF2 复核的实际通过率、被它删掉多少设计，正文没有数字；本卡不推断。
4. **超小极性配体（血清素/多巴胺）几乎没有可接触的原子**。原文："For very small and polar ligands,"；实测也确实掉下来："The low success for DPA highlighted the increased"。
   **他们做了什么**：三条并用——(a) 把关键氢键在采样里加权（"To enhance ligand specificity,"）；(b) 提高送测数并**刻意最大化骨架多样性**（"we designed 120-residue, six-helix bundle"）；(c) 命中后做**计算过滤 + 实验轮次**的迭代序列优化："Following rigorous computational filtering, selected variants were experimentally characterized, with the highest-affinity binder advanced to the next optimization round"。
   **代价**：绝对亲和力仍只有低 μM（血清素最佳 72.8 μM、多巴胺 75.0 μM，多巴胺只有 1 条）；迭代轮的过滤判据与阈值正文未列（原文未给阈值）。
5. **拆分式传感器的背景信号（无配体时片段自己会拼回去）**。原文点名："A major challenge with split protein sensors is"。
   **他们做了什么**：从**一个非预期构造里提炼出通用招**——最初命中的菌落变体带 8 个氨基酸的螺旋重复，作者明写它不是设计产物："This duplicated helix region is most likely"，然后据此提机理假设 "We hypothesized that this repeat might increase"，再把它工程化：换到另一个结合体 SRO_26 上试不同重复长度（13.8%）、加 5 残基截断（"To further decrease self-association,"，78.9%）、界面大疏水换小残基（"we further screened interface variants by"）、扫 linker（→339.9%）。
   **代价**：这条起点是一条 PCR 装配副产物，且响应值在 **10 mM** 血清素下测（与生理浓度差 3–5 个数量级）；SRO_26/DPA_9 两条传感器被作者自己标为低通量小样本——"The SRO_26 and DPA_9 based sensors are all"（n = 24 与 n = 9），并承认 "Although their current performance is suboptimal"。
6. **金属选择性撞上 Irving-Williams 序列**（Cu²⁺ 热力学上本应压过 Zn²⁺）。原文："This strong selectivity is"，并宣称 "yet our design successfully"（两句之间夹引文编号 42、45，故拆成两条引句）。
   **他们做了什么**：把选择性交给**配位几何与残基组合的显式建模**（图注原句 "For each metal ion, the coordination geometry and residue types were defined, and the coordination rotamer at each coordination site was systematically sampled"；镍用两个双齿残基凑八面体），再靠 ITC 专属性面板（Zn 对 Cu/Co/Ni 无检出；NiM4 对 Ca/Co/Mg 无检出）验回。铜在传感器里仍有微弱响应，作者给的解释未经检验："Copper induced minimal signal,"。
   **代价**：每金属只测 10 条，最终只有 1 条 Zn、1 条 Ni 进到详细表征；"绕过 Irving-Williams"只在一对离子上成立，没做浓度/竞争滴定排除动力学成因。
7. **命中率数字的分母不一致（本文未解决）**。三处正文级不一致，本卡只登记不解释：
   - DFHBI 送测数在两段里不同：前段 "we selected 96 DTG designs,"，后段却是 "fluorescence assays revealed"（16 这个分母从哪来，正文未说明）；
   - 同一个亲和力数值出现在两个不同配体上：CIA "For CIA, 20 out of 94 designs showed binding" 的最佳值写作 43.7 μM，DFHBI 段又写 "The most effective binder"；
   - CIA 句子里的图号指向 Fig. 3（金属结合体图）："with the highest measured"，而 CIA 的实际图是 Fig. 2b。
   **应对**：正文未见任何更正或说明——**本文未解决**（与 `sources/cao.md:480` 的"预印本数字未经独立复现"标注一致）。
8. **图注与正文对"送测集怎么选"的说法互相矛盾（本文未解决）**。图注说 "Well-packed scaffolds were selected for sequence optimization, and top-scoring designs were chosen for experimental characterization"，正文却说选这批是为了 "capturing a broad range of"（并给出中位两两骨架 RMSD 12.63/11.98/12.68 Å 这种极大离散度）。
   **应对**：作者没有在任何地方调和两者；本卡按正文口径记（多样性抽样），并把这条列为 §7 的头号局限。

## 3. 方法与工作流程（每步：输入 → 判据/阈值 → 输出规模）

### 先回答两个关键问题

**（A）物理判据与 ML 判据各自在漏斗哪一段？**

| 段 | 用什么判据 | 具体项 | 阈值 |
|---|---|---|---|
| 生成阶段（骨架一边长一边打分） | **纯物理**，且是**主判据** | 复合打分 = RPX（residue-pair transform，折叠项）+ RIF（rotamer interaction field，结合项，逐查表估能量）+ 特权氢键可加权；Monte Carlo 移动按 Metropolis 接受/拒绝；连续失败步达到预设阈值就把 folding root 换到另一个 RIF 锚定残基 | 原文未给阈值（连"连续失败步数"的具体数字都没写；Methods 不在本底稿里） |
| 序列设计阶段 | 无（该步只有生成器，不打分） | 序列由 Rosetta 与 ProteinMPNN 生成；迭代改良阶段换成 LigandMPNN，只动配体邻近残基 | 原文未给阈值 |
| 设计后过滤阶段 | **物理为主** | 四个口径 = apo 折叠、配体相互作用能、蛋白-配体氢键数目与几何（金属换成配位残基数目与几何）、整体形状互补 | 原文未给阈值 |
| 设计后过滤阶段（末端） | **ML 只做一致性复核** | 把每个设计与 AF2 预测结构比对，评结构准确度 | 原文未给阈值 |
| 送测选择阶段 | **既不是物理也不是 ML，而是多样性** | 按覆盖宽架构挑一批送去表达（中位两两骨架 RMSD 12.63/11.98/12.68 Å） | 无阈值；报的是所选集合的离散度 |

结论性一句：这篇与 B09（Bennett 2023）**结构相反**。B09 是"物理生成 → 让 AF2 pAE_interaction<10 当**主闸口**削 2M→5K"；C21 是"物理判据同时充当生成引导与过滤器，AF2 只在末端复核，**ML 判据不承担任何削减分母的职责**"。原因在分母上：C21 没有百万级库可供打分（生成规模根本没报，见下），闸口自然没地方放。

**（B）库规模 → 送测 → 命中，每一层分母到底是什么？**（这是本文最大的一处证据缺口）

| 层 | 分母 | 状态 |
|---|---|---|
| L0 物理生成总骨架数/靶 | — | **正文未报告**（无"生成 N 个模型"字样，只有"在每条采样轨迹里我们从伸展链开始"这类流程描述） |
| L1 过滤后剩余设计数 | — | **正文未报告**（"rigorously filtered" 无通过数、无通过率） |
| L2 AF2 复核通过数 | — | **正文未报告** |
| L3 送测设计数 | DTG 96 / CIA 94 / DFHBI 32 / SRO 38 / DPA 33 / Zn 10 / Ni 10 | 已报告 |
| L4 表达可溶单体数 | "The majority"（DTG/CIA/SRO/DPA 无具体数）；金属：8 条 Zn + 8 条 Ni 单体 | 只有定性词与金属的实数 |
| L5 ITC/荧光命中数 | DTG 14/96、CIA 20/94、DFHBI 2/16（与 L3 的 32 不一致）、SRO 6/38、DPA 1/33 | 已报告（DFHBI 分母存疑） |
| L6 改良轮次 | DTG 16 条重设计变体（1 轮）；SRO 4 轮（每轮变体数未报）；传感器低通量 n=24（SRO_26 路线）与 n=9（DPA_9 路线） | 部分报告 |
| L7 结构确证 | 4 个晶体结构（SRO_30、SRO_26_L7F、DPA_9、ZK2） | 已报告 |

也就是说：命中率（如 CIA 20/94 = 21.3%，本卡换算）是**以 L3 送测数为分母**的，不含 L0→L3 的任何压缩比。把 21.3% 读成"这套物理生成的通过概率"是错的——它读的是"故意打散架构去测 94 条"的结果。

### 工作流程表（按原文顺序）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | 目标小分子（DTG、CIA、DFHBI、血清素 SRO、多巴胺 DPA） | 代表性构象系综采样 → 聚类 → **quantum optimization 精修** → 用 RIFGen 从精修构象生成 RIF；再枚举 favorable 侧链-配体相互作用，得到相互作用能与"关键接触残基图" | 原文未给阈值（QM 方法与基组在 Methods，本底稿缺） | 每个配体一套优化构象 + 对应 RIF；条数未报告 |
| W2 | 目标金属离子（Zn²⁺ 四面体、Ni²⁺ 八面体） | 按偏好残基类型与几何建"配位 RIF 表"，系统采样每个配位位点的配位旋转异构体；每条带配位位点标签（可控制完整/部分配位球） | 残基类型限定 His / Asp / Glu；镍用两个双齿残基 | 配位 RIF 表；条目数未报告 |
| W3 | 伸展链（长度与拓扑先定：小分子 120 aa、五或六螺旋；金属 65 aa、四螺旋束），随机指派二级结构元件 | 随机选一个残基对齐随机 RIF 锚点 = **folding root**（该步之后固定），从 root 向外做 **Monte Carlo 片段组装**（片段库取自天然结构），每步用复合打分同时优化折叠与结合 | "Protein folding is assessed by"（RPX 分）+ 结合由 RIF 快速估计；特权氢键可上调权重；按 Metropolis 接受/拒绝；"if a predefined threshold of" | **原文未给阈值**（连续失败步数、收敛判据、每条靶采样规模都没有数字；输出规模未报告） |
| W4 | W3 的骨架 | 选"折叠良好且配体相互作用有利"的骨架进入序列优化 | 定性判据（well-folded / favorable ligand interactions），原文未给阈值 | 未报告 |
| W5 | W4 骨架 | 序列优化用 Rosetta 与 ProteinMPNN | 无（生成步） | 未报告 |
| W6 | W5 设计 | **物理侧严格过滤**：apo 蛋白折叠、配体相互作用能、蛋白-配体氢键数目与几何（金属则为配位残基数量与几何）、整体形状互补 | 原文未给阈值 | 未报告 |
| W7 | W6 通过者 | **ML 侧末端复核**：每个设计与 AF2 预测结构比对，评结构准确度 | 原文未给阈值 | 未报告； Supplementary Fig. 2 显示所选构型多样 |
| W8 | W7 通过者 | **按多样性挑送测集**（图注措辞是 top-scoring，正文措辞是 broad range of architectures，两者冲突，见 §2.7 与本节末） | 无阈值；报中位两两骨架 RMSD 作离散度 | 96 DTG / 94 CIA / 32 DFHBI / 38 SRO / 33 DPA / 每金属 10 |
| W9 | 送测序列 | E. coli 表达 + SEC（可溶、单体判定） | 可溶 + 单体峰 | DTG/CIA/SRO/DPA "The majority"；金属：Zn 8/10、Ni 8/10 单体 |
| W10 | 可溶蛋白 | ITC 初筛结合（DTG、CIA、SRO、DPA）；DFHBI 用结合后荧光激活做荧光筛查 | 结合/荧光上升 | DTG 14/96（最佳 4.94 μM）；CIA 20/94（最佳 43.7 μM）；SRO 6 条（最佳 72.8 μM）；DPA 1 条（75.0 μM）；DFHBI 2/16 |
| W11 | 命中者 | 界面破坏突变（接触残基换 Ala / 引入大体积残基造成位阻）+ ITC 复测 | 结合完全消失即支持设计结合模式 | "ITC experiments on these" |
| W12 | DTG 最佳候选 | 螺旋延伸策略：N 或 C 端各加两条螺旋以稳定结合螺旋、提高结构预组织 | 计算过滤后送测 | 16 条重设计变体 → 971 nM，作者称 15.8 倍（与 4.94 μM 起点不自洽，见 §6.3） |
| W13 | SRO_26 / SRO_30 | **4 轮**"Rosetta 序列设计 + LigandMPNN（只改配体邻近残基）→ 严格计算过滤 → 实验表征 → 最高亲和者进下一轮" | "Following rigorous computational filtering, selected variants were experimentally characterized, with the highest-affinity binder advanced to the next optimization round"；每轮变体数与过滤阈值原文未给 | SRO_26 变体 29.9 μM，作者称 15.7 倍；累积突变主要在口袋、以疏水为主 |
| W14 | 金属命中者（ZK2、NiM4） | IMAC 纯化后切 His-tag；±EDTA 做 SEC 与 CD；ITC 测亲和力与专属性 | EDTA 洗出离子后洗脱体积变大 + CD 由无规卷曲转螺旋 = 结合耦合折叠 | Zn：8/10 单体，4 条 EDTA 位移；Ni：8/10 单体，1 条位移；ZK2 Kd 150 nM、1:1，对 Cu/Co/Ni 无检出；NiM4 Kd 5.38 μM、1:1，对 Ca/Co/Mg 无检出 |
| W15 | 代表性设计 | X 射线晶体学（SRO_30、SRO_26_L7F、DPA_9、ZK2） | 骨架与配体位姿与设计模型比对 | 分辨率 2.58 / 2.00 / 2.47 / 1.23 Å；Cα RMSD 0.97 / 0.791 / 0.446 Å；配体 RMSD 1.997 Å（SRO_30）、0.883 Å（DPA_9） |
| W16 | SRO_30 / SRO_26 / DPA_9 | 拆分片段 + cpsfGFP；error-prone PCR 建库 + 平板菌落荧光（加血清素前后各测一次）筛分裂位点与有益突变 | "Colonies displaying robust"；阈值原文未给 | wcSRO_30_0.1 ΔF/F₀ 27.6% @10 mM → 界面突变 wcSRO_30_0.5 179.4% → linker 筛 wcSRO30_1.0 339.9%；SRO_26 路线 13.8%→78.9%（n=24）；DPA_9 路线 24.3%→37.5%（n=9，作者称首个可溶多巴胺传感器） |
| W17 | wcSRO30_1.0 | 光谱/滴定/专属性/E. coli 菌落与 HEK293T（流式 + 实时成像）表征 | 与 iSeroSnFR 对比 EC₅₀ 与动态范围 | 激发/发射 417/507 → 493/512 nm；EC₅₀ 539.9 μM vs iSeroSnFR 959 μM；ΔF/F₀ 411% vs 930%（E. coli）；ITC 105 μM；传感模块 129 aa vs 272 aa |
| W18 | ZK2 | split-NanoLuc 互补策略（片段接 ZK2 两端），扫 linker | 加锌后发光上升 | ZK2_Nluc_4 / ZK2_Nluc_7 两条构建体；EC₅₀ 72.8 nM / 78.7 nM（1 μM 离子做专属性面板） |
## 4. 关键数字台账

| 数值 | 含义 | 出处（正文/图注位置） |
|---|---|---|
| 120 amino acids（五或六螺旋）；65 amino acids（四螺旋束） | 小分子结合体与金属结合体的骨架长度/拓扑 | "we generated helical bundle"；"we designed compact four-helix" |
| 96 / 94 / 32 / 38 / 33 / 每金属 10 | 送测设计数（DTG / CIA / DFHBI / SRO / DPA / Zn 与 Ni） | "we selected 96 DTG designs,"；"selected 38 SRO and 33 DPA"；"For each metal ion, we selected" |
| 12.63 / 11.98 / 12.68 Å | 所选送测集的中位两两骨架 RMSD（DTG/CIA/DFHBI）= 刻意打散架构 | "median pairwise backbone RMSD of 12.63 Å for DTG, 11.98 Å for CIA, and 12.68 Å for DFHBI" |
| 14/96 = 14.6%（本卡换算） | DTG 命中率（ITC 初筛） | "Initial screening of 96 DTG" |
| 4.94 μM | DTG 初筛最佳 Kd | "with the top candidate exhibiting an affinity of 4.94 μM" |
| 16 条变体 → 971 nM，自述 15.8 倍 | DTG 螺旋延伸改良（1 轮） | "we achieved a 15.8-fold increase in affinity, reaching 971 nM"（**本卡换算 4.94 μM/971 nM = 5.09 倍，与 15.8 倍不自洽**） |
| 20/94 = 21.3%（本卡换算） | CIA 命中率（ITC） | "For CIA, 20 out of 94 designs showed binding" |
| 43.7 μM | CIA 最佳 Kd；同一数值又被写成 DFHBI 最佳 Kd | "with the highest measured"；"The most effective binder" |
| 2/16 = 12.5%（本卡换算） | DFHBI 荧光激活命中率（分母与送测数 32 不一致） | "fluorescence assays revealed" |
| 6/38；1/33 | 血清素 / 多巴胺结合体数（分母 = 送测数，本卡换算 15.8% 与 3.0%） | "ITC experiments revealed that"；"we successfully identified one" |
| 72.8 μM / 75.0 μM | 血清素 / 多巴胺最佳 Kd（低 μM） | "with the highest measured"；"we successfully identified one" |
| 4 轮 → 29.9 μM，自述 15.7 倍 | SRO_26 迭代序列优化（Rosetta + LigandMPNN，每轮变体数未报） | "After four rounds of iterative" |
| 150 nM，1:1 | ZK2 对 Zn²⁺ 的 Kd 与化学计量；对 Cu/Co/Ni 无检出 | "the design ZK2 demonstrated a" |
| 5.38 μM，1:1 | NiM4 对 Ni²⁺ 的 Kd 与化学计量；对 Ca/Co/Mg 无检出 | "the nickel binder NiM4 displayed 1:1 stoichiometry with a Kd of 5.38 μM" |
| 8/10 与 8/10 单体；4 条 Zn、1 条 Ni 有 EDTA 位移 | 金属设计的"表达可溶"与"结合耦合折叠"两层分母 | "SEC in the presence of the"；"revealed clear shifts in the" |
| 2.58 / 2.00 / 2.47 / 1.23 Å | 四个晶体结构分辨率（SRO_30、SRO_26_L7F、DPA_9、ZK2） | "at a resolution of 2.58 Å"；"resolved at 2.00 Å"；"at 2.47 Å resolution"；"determined at 1.23 Å resolution" |
| Cα RMSD 0.97 / 0.791 / 0.446 Å | 实验骨架与设计模型一致性 | "with a Cα RMSD of 0.97 Å"；"(Cα RMSD of 0.791 Å)"；"(Cα RMSD of 0.446 Å)" |
| 配体 RMSD 1.997 Å / 0.883 Å | 配体位姿与设计预测一致性（血清素 vs 多巴胺） | "ligand RMSD of 1.997 Å using"；"with a ligand RMSD of just" |
| 27.6% → 179.4% → 339.9% | wcSRO_30_0.1 → 界面变体 0.5 → linker 终版 wcSRO30_1.0 的 ΔF/F₀（都在 10 mM 血清素下） | "which exhibited a ΔF/F₀ of"；"displayed a much greater ΔF/F₀"；"which showed a ΔF/F₀ of 339.9%" |
| 13.8% → 78.9%；24.3% → 37.5% | SRO_26 路线（重复螺旋→5 残基截断）与 DPA_9 路线（1-5 拆分→linker）的 ΔF/F₀ | "we quickly identified a variant"；"achieving a ΔF/F₀ of 78.9%"；"a 1-5 split variant with a"；"we obtained a construct with a" |
| n = 24 与 n = 9 | SRO_26 / DPA_9 传感器路线的筛取样量（低通量） | "The SRO_26 and DPA_9 based" |
| 5 个分裂位点组合；8 残基重复 | SRO_30 拆分方案数与那个非预期重复长度 | "We split this protein into two"；"it contains an eight-amino-acid" |
| EC₅₀ 539.9 μM vs 959 μM；ΔF/F₀ 411% vs 930% | wcSRO30_1.0 与 iSeroSnFR 的灵敏度/动态范围对比 | "wcSRO30_1.0 exhibited improved" |
| 417/507 → 493/512 nm | 加血清素前后激发/发射峰位移 | "In the absence of serotonin," |
| 105 μM | 传感器构建体 wcSRO30_1.0 自身的 ITC Kd | "ITC measurements showed a" |
| 129 aa vs 272 aa | 传感模块大小对比 iSeroSnFR | "the SRO sensing module in" |
| 10 mM（SRO）、1 mM（五种竞争配体）、1 μM（金属面板） | 传感器响应与专属性测试浓度 | "in response to 10 mM serotonin"；"at 1 mM concentrations"；"the zinc sensors tested against" |
| EC₅₀ 72.8 nM / 78.7 nM | 锌传感器 ZK2_Nluc_4 / ZK2_Nluc_7 | "Titration experiments revealed" |
| **未报告** | 每靶生成骨架总数、过滤通过数/通过率、AF2 复核通过数、任何计算单价（GPU·h / CPU·h） | 全文（含图注）无对应数字；见 §3(B) 分母表 |

## 5. 结论——作者说了什么

1. **范式主张**：物理-based 生成能替代"预造骨架库 + docking"，并同时控制折叠与结合——"Overall, the high level of"；"In contrast to previous methodologies focused primarily on static, high-affinity binding, our strategy enables direct coupling of ligand recognition to conformational transitions"。
2. **命中率主张**：对小分子结果的评价是 "these results demonstrate the"（对应 DTG 14/96、CIA 20/94）。
3. **小配体主张**："SRO and DPA represent some of"。
4. **结合位点主张**：靠界面破坏突变后结合完全消失来支撑设计的结合模式（不是靠预测分数）。
5. **金属主张**：选择性可绕过 Irving-Williams 序列的热力学偏好；且 "Upon metal binding, the protein"。
6. **传感器主张**：血清素传感器灵敏度优于 iSeroSnFR（EC₅₀ 539.9 μM vs 959 μM）但动态范围更低；多巴胺传感器被宣称为同类第一个可溶体系——"marking the first reported"。
7. **作者自限**："Although their current performance is suboptimal"；"there remains considerable"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **"物理 vs 机器学习"在这篇里不是判据优劣之争，而是分母之争**。物理判据能当主闸口，是因为生成规模小到不需要再削分母（正文连 L0/L1/L2 三个数都没给）；B09 的 ML 判据成为主闸口，是因为那里真有 2M 级库必须削。→ 对我们：**"该用哪个判据"取决于可下单的分母规模，不取决于哪个更物理**（把握度：中-高；两篇漏斗结构可直接对照）。
2. **本文真正的验证层是界面突变与 ±EDTA/CD，不是 AF2**。AF2 复核无阈值、无通过率、无对照，只构成"看起来像"，不构成判别力证据。→ 不能引用这篇来支持"结构预测自洽可当闸口"（把握度：高；缺失项正文明确未给出）。
3. **约 20% 命中率是"故意打散架构 + 全部下单"的产物，不是计算排序能力的产物**（正文口径为 capturing a broad range of architectures，与图注 top-scoring 冲突）。若有人拿 21.3% 当"某判据通过率"校准，属口径误用（把握度：中；能改变结论的证据 = Methods/Supp 给出送测集的选择规则与真实生成规模）。
4. **倍效数字必须先回补材料才能引用**：4.94 μM → 971 nM 是 5.09 倍，与作者所称 15.8 倍不符；血清素 15.7 倍无法从正文重算（SRO_26 起点 Kd 未给）。两处在正文内可直接重算（把握度：高）。
5. **结合模块嵌进报告体系后读数系统性变差**：血清素结合体群的最佳值是 72.8 μM（正文没写这条是不是 SRO_30 本身），而传感器构建体 wcSRO30_1.0 自身 ITC 为 105 μM、读出 EC₅₀ 539.9 μM。→ 对我们：候选接上检测体系后的信号不等于分子本身性质（把握度：中；作者未做同条件系统比较，只有一对数字）。
6. **最有用的设计原则来自一条意外的装配副产物**（重复螺旋提高自缔合能垒），他们做对的是先测序归因、再提假设、再换结合体验证可推广。→ 对我们：筛到意外构造应测序归因，不要当噪声丢（把握度：高，有原文流程支持）。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自述的**
- 传感器性能：见 §5.7；SRO_26/DPA_9 两条路线是低通量小样本（n = 24 与 n = 9），且明确没有做定向进化。
- 拓扑局限：方法只围绕螺旋束（以 GPCR/核受体为灵感），未声称能生非螺旋架构。
- 绝对亲和力仍停在 μM 段（血清素最佳 72.8 μM、多巴胺 75.0 μM，多巴胺只 1 条）。
- 讨论里把提升交给未来工作：需要定向进化与体内验证才能扩展适用面。

**我们读出的（附证据位置）**
1. **漏斗分母大面积缺失**：L0 生成数、L1 过滤通过数、L2 AF2 复核通过数、以及任何计算单价，正文与图注都没有（见 §3 的分母表）。因此"物理判据把库削掉了多少"不可评估，这篇也给不出"某判据的提效率"。
2. **三处内部不一致（预印本笔误风险）**：DFHBI 分母 32 vs 16；43.7 μM 同时挂在 CIA 与 DFHBI 上；CIA 句子里图号写成 Fig. 3b（正文无更正，见 §2.7）。
3. **送测集选择口径自相矛盾**：图注说按 top-scoring，正文说按架构多样性覆盖（见 §2.8）。这直接决定 14.6%/21.3% 该怎么解释，作者没有调和。
4. **近 2 Å 的配体位姿偏差被写成 aligned closely**（同句给 1.997 Å），而 0.883 Å 的那条才是"位姿准"的水平；四个晶体里只有两个报了配体 RMSD，存在选择性报告风险。
5. **专属性面板的浓度对照不明**：竞争物在 1 mM 测，响应表征常用 10 mM 血清素；正文没写该面板里血清素自身用什么浓度，所以"选择性高"这句话的对照强度**无法判定**（不是已证明不行，是缺一个数）。
6. **传感器只在 mM 分析物浓度下报响应**（10 mM），比脑内血清素/多巴胺的 nM–μM 区间高 3–5 个数量级；EC₅₀ 539.9 μM 本身也说明实用窗口还在 mM 附近。
7. **无 MD、无反应化学**：全文无自算分子动力学（唯一出现的 molecular dynamics 在参考文献标题里，是他人工作）；QM 只用于配体构象精修，不含反应坐标、过渡态或能垒。
8. **同行评审状态**：v1 预印本（2026-07-13 投稿、2026-07-14 上线），无独立复现。

## 8. 迁移判断：哪些能搬、哪些不能搬（含"把配体结合能当主闸口在我们这里能不能用"）

**先给判定（分三层，不给一句含糊话）**

| 子问题 | 判定 | 依据与把握度 |
|---|---|---|
| 把"配体结合能"当酶设计 **酶活主闸口（GO/NO-GO）** | **不能用** | 本文所有成功判据都是非反应性结合的 Kd（ITC），没有任何化学转化被设计或被测量；QM 只做配体构象精修（"Small molecule conformers were sampled, clustered, and refined through quantum optimization"），不含反应坐标。结合能与催化活性之间，这篇没有建立过任何联系。把握度：高。能改变结论的证据：一篇 de novo 体系以结合能为主判据、同时报 kcat/Km 并带定点失活对照的前瞻实验——本文不是 |
| 把"配体结合能"当**生成阶段引导项 / 召回条件** | **位置能借，能量函数不能借** | 他们的 RIF 是侧链-配体相互作用能查表，之所以能在蒙特卡洛每一步使用，是因为它便宜且与目标（把配体包埋）同向（"Protein folding is assessed by the residue-pair transform" + 结合由 RIF 估）。我们要引导的是**催化几何**（进攻原子 in-line、α磷酸与供体/离去基团间距、金属配位数），不是包埋形状。可迁移的是"把目标相互作用写进生成循环"这件事，不是他们的势能面 |
| 把"配体结合能"当**末端一致性复核**（不削分母、不参与排序） | **能用，且这正是本文的定位** | 本文把唯一一次 ML 介入放在最后只比结构一致性（"the structural accuracy of the final models was assessed by comparing each design to AlphaFold2-predicted structures"），且不报通过率。我们的对应做法：结合能只作为辅助读数写进档案，不写进 GO/NO-GO 式，避免与生成目标同源而自证 |

**可迁移（具体怎么用）**
1. **特权相互作用加权 → 催化原子对强制约束**：他们把关键氢键在采样里上调权重（"To enhance ligand specificity,"）。我们的等价物是把"进攻原子—P—离去原子"几何写成可加权项，在骨架构建时生效，而不是等设计完再打分。
2. **apo 故意不稳 → 位点靠配体诱导成形**：金属那套思路（"The use of such small scaffolds"）提醒我们：把催化残基在无底物时也强制成位，代价很可能是不溶或错折叠；"先不稳、结合后再成形"是一条可直接借的构型策略，也天然给出一条可证伪的对照（去掉底物应无活性构象）。
3. **末端用独立实验层做因果判定**：本文最有说服力的两步是界面突变使结合完全消失（"ITC experiments on these"）与 ±EDTA 的 SEC/CD 双读。我们的等价物是**产物化学 + 定点失活对照**，这是漏斗末端信息量最高处，不能省。
4. **闸口配置跟着分母走**：某一层真能产出上万候选时，才给那层配一个带阈值的 ML 闸口（B09 式）；若只产出几十条（本文式），闸口是浪费，预算应直接给实验与失活对照。
5. **通过率与单价必须成对报**：本文两者都没报，所以它的"高效"无法被复用；我们的判据总纲里，任何新判据要先有"每个通过闸口的候选花多少核时"。

**不能照搬（为什么）**
1. **命中率数字不许搬**。14.6%/21.3%/15.8%/3.0% 全部以"送测条数"为分母，终点是二值 ITC 结合，且是多样性抽样的结果。我们的终点是"有没有目标产物 + 旁路产物占比"，一轮最多几条构建体，既无同等通量也无同类标签——把这两个百分数当酶设计先验概率，就是把配体结合口径当酶活口径（本卡 §3 已说明它们不是同一层分母）。
2. **阈值一个都不能引用**。本文没有任何可复算的过滤阈值：生成阶段的连续失败步阈值、物理过滤四项、AF2 比对口径全是定性描述，Methods 不在本地底稿里（见 §0）。它不能当"某阈值下通过率 X"的先例。
3. **"高通过率"这句话的解释力被内部矛盾限制**（§7.2、§7.3）：独立复现前只能按"作者自述的预印本读数"引用。
4. **展示式/ITC 式的通量在我们这里不存在**。我们漏斗末端要的是信息量最大化（机制多样性 + 失活对照），不是样本数最大化；本文恰恰是反过来做的（几十条全测），它的成本结构对我们不可复制。
5. **本文不含 MD/QM 反应层**，因此不能为"用 MD/QM 判催化"提供任何命中率背书；那类主张需另找参照。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/C21_PPR1279910_text.txt

- **实际照着写的那一份**：`data/literature_cards/fulltext/C21_PPR1279910_text.txt`（57,102 字符）。同目录 `C21_PPR1279910_fullTextXML.xml`（238,736 B）是同一内容的 **HTML 原文**（文件首行为 DOCTYPE html，即 bioRxiv 文章页，不是 JATS/XML）；`batches.tsv` 第 19 行记 `state=FULLTEXT`、`fetch_status=OK`、`fetch_note=fallback_ok[biorxiv_full]`，说明 Europe PMC 对该 PPR 记录返回的也是 bioRxiv 页面。本卡全部引句只以这份 `_text.txt` 逐字复制。
- **该底稿里不存在的东西**：Methods 全节、任何 Supplementary 图/表内容（含 Supplementary Figs 1-14 与 Supplementary Table 7）、Code/Data availability、任何算力单价、以及"生成规模/过滤通过数"。凡涉及这些的格子，本卡写"原文未给阈值"或"未报告"，未做任何补齐性推断。
- **身份复核**：本地全文首部的作者串（Yanzhe Zhang … Longxing Cao）、标题与 DOI 10.64898/2026.07.13.738243 与 CSV 行、`sources/cao.md:333-335` 一致；文末的 Posted July 14, 2026 与 CSV 记的 2026-07-13 是同一记录的上线日/投稿日。
- **对照底稿（先行调研，行号可查）**：`sources/cao.md:333-349`（C21 卡）、`:421`（漏斗数字对照表 C21 行）、`:455`（全文 MD 扫描：仅命中参考文献条目）、`:462`（QM 仅用于配体构象优化）、`:480`（预印本命中率未经独立复现的风险标注）。
- **与先行调研的出入（本卡以全文为准）**：`sources/cao.md` 与 CSV 行都把候选生成写成"物理-based 生成 + 折叠模拟并行"，本卡按正文口径细化为"RIF 锚定的蒙特卡洛片段组装，复合打分 RPX + RIF 同步优化折叠与结合"；CSV 行 `阈值数字=未记录` 与本卡结论一致（本底稿确无可复算阈值）。
- **CSV 字段映射**：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：命令 `cd A:\Data\MD\projects\protein-design-screening-20261016` + `PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only C21 --no-report`（输入：本卡 + 上面声明的单一底稿；判据：卡内每条被直双引号包住、无中日韩字符、≥20 字符且≥12 个字母的片段都要在该底稿里逐字命中，另查 10 节齐全、工作流程表≥3 步、难点≥2 条、回填块 14 键非空）。首轮曾出现 1 条 MISS，原因是把图注里小写的 the 抄成句首大写（比对区分大小写），改正后复跑；最终计数写在交付回报里。
- **把握度小结**：漏斗**位置**（物理判据在生成端与过滤端、ML 判据在末端复核）与**送测→命中**两层的分母是清楚的；**生成→送测**之间的压缩比与**任何数值阈值**在本底稿里不存在，必须靠 Methods 才能补，本卡不猜也不引用二手推测。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 72 条逐字引句来自许可受限的第三方来源（C21；CC_BY_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=预印本（bioRxiv v1，未同行评审；DOI 10.64898/2026.07.13.738243，投稿 2026-07-13、页面标注 Posted July 14, 2026；EPMC 记录 PPR1279910）
target=小分子结合蛋白（DTG=dolutegravir 抗 HIV 整合酶抑制剂、CIA=cianidanol 抗氧化类黄酮、DFHBI 荧光激活染料、血清素 SRO、多巴胺 DPA）+ 金属结合蛋白（Zn²⁺ 四面体配位的 ZK2、Ni²⁺ 八面体配位的 NiM4）+ 由这些结合体改造的血清素/多巴胺 cpsfGFP 传感器与锌 split-NanoLuc 传感器
backbone_generation=自研物理-based 生成（在 ProBuilder 内）：配体构象系综采样→聚类→quantum optimization 精修→RIFGen 建 RIF；金属按配位几何与残基类型建带配位位点标签的配位 RIF 表；随机残基对齐随机 RIF 锚点定为 folding root 并固定，Monte Carlo 片段组装由根向外长骨架，复合打分 = RPX 折叠分 + RIF 结合估计（特权氢键可上调权重），Metropolis 接受、连续失败步达阈值就换 root；序列由 Rosetta + ProteinMPNN 生成，迭代改良阶段改用 LigandMPNN 只动配体邻近残基
computational_filters=设计后物理侧过滤四项：apo 蛋白折叠、配体相互作用能、蛋白-配体氢键数目与几何（金属换成配位残基数量与几何）、整体形状互补；末端 ML 一致性复核 = 每个设计与 AlphaFold2 预测结构比对；迭代改良阶段另有一层内容未列明的 rigorous computational filtering；送测集按架构多样性挑（中位两两骨架 RMSD ~12 Å），与图注的 top-scoring 措辞互相冲突
thresholds=原文未给任何可复算阈值（本底稿不含 Methods；连续失败步数阈值、四项过滤阈值、AF2 比对口径均只有定性描述）；可核的数值只有事后结构一致性：Cα RMSD 0.97/0.791/0.446 Å、配体 RMSD 1.997/0.883 Å、分辨率 2.58/2.00/2.47/1.23 Å
md_used=否（全文无自算 MD；本底稿里 molecular dynamics 只出现在参考文献标题中，即他人工作 O'Shea 2024）
qm_used=是-仅配体侧构象准备（小分子构象系综经 quantum optimization 精修后喂 RIFGen；不含反应坐标、过渡态或酶活化学）
experimental_methods=E. coli 表达 + SEC 单体判定 + ITC 定量结合与专属性；界面破坏突变（Ala 替换或引入大体积残基）验证结合位点；DFHBI 用结合激活荧光筛查；金属用 ±EDTA 的 SEC 与 CD 证明结合耦合折叠；X 射线晶体学 4 个结构；传感器为拆分片段 + cpsfGFP（error-prone PCR 菌落平板荧光筛分裂位点与有益突变、界面弱化突变、5 残基截断、linker 扫描）与 split-NanoLuc 互补；E. coli 菌落与 HEK293T（流式 + 实时荧光成像）读出
pipeline_counts=唯一完整报告的是送测层及其后：96 DTG / 94 CIA / 32 DFHBI / 38 SRO / 33 DPA / 每金属 10 → 命中 14 DTG、20 CIA、2 DFHBI（此处分母写作 16，与 32 不一致）、6 SRO、1 DPA；金属 8 Zn + 8 Ni 单体，其中 EDTA 位移 4 Zn + 1 Ni → 改良：DTG 16 条重设计变体（1 轮）、SRO_26 4 轮迭代（每轮变体数未报）、传感器低通量 n=24（SRO_26 路线）与 n=9（DPA_9 路线）→ 晶体 4 个。生成层与计算过滤层分母（每靶骨架数、过滤通过数、AF2 复核通过数）正文未报告
hit_rate=以送测数为分母（本卡换算）：DTG 14/96 = 14.6%、CIA 20/94 = 21.3%、SRO 6/38 = 15.8%、DPA 1/33 = 3.0%、DFHBI 2/16 = 12.5%；作者自评 high success rate。传感器：wcSRO30_1.0 EC₅₀ 539.9 μM（iSeroSnFR 959 μM）但 ΔF/F₀ 411% 低于对照 930%；锌传感器 EC₅₀ 72.8/78.7 nM；SRO_26/DPA_9 路线自述 performance is suboptimal
best_metric=DTG 971 nM（螺旋延伸后；作者称 15.8 倍，但按正文起点 4.94 μM 重算为 5.09 倍，不自洽）；ZK2 Kd 150 nM（1:1，对 Cu/Co/Ni 无检出）；锌传感器 EC₅₀ 72.8 nM；血清素最佳 29.9 μM（4 轮迭代，自述 15.7 倍，起点 Kd 正文未给）；多巴胺 75.0 μM（仅 1 条）；NiM4 Kd 5.38 μM
cost_or_stat_note=未记录（正文、图注与讨论均未给 GPU/CPU 时、单条设计耗时、生成规模、任何过滤通过率或计算单价；本底稿不含 Methods，无法补算，本卡不做估算）
role_in_timeline=曹龙兴组从蛋白 binder 的 ML 闸口漏斗（B09 一脉：物理生成 + AF2 pAE_interaction 主闸口）转向小分子/金属分支的物理-based 生成：把配体能量场写进生成循环，因而不再依赖预造骨架库，并显式控制拓扑与折叠-结合平衡，使产物可直接改造成传感模块；代价是没有可报告的漏斗压缩比与阈值，命中率靠高骨架多样性 × 几十条全量送测换取，绝对亲和力停在 μM 段
source_pointer=data/literature_cards/fulltext/C21_PPR1279910_text.txt（bioRxiv 页面抽取，57,102 字符，不含 Methods 与 Supplementary）+ sources/cao.md:333-349、:421、:455、:462、:480
CSV回填-->
