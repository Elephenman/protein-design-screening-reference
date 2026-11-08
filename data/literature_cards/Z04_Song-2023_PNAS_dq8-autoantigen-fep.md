# [Z04] 单点突变的 FEP 几乎全打负——周如鸿组的应对不是改力场，而是换突变类型（双突变/换位突变）

Yi Song, David R. Bell, Rizwan Ahmed, Kevin C. Chan, Sangyun Lee, Abdel Rahim A. Hamad（Johns Hopkins，免疫实验端）, **Ruhong Zhou**（浙大 IQB / IBM CBMC / Columbia）
PNAS 2023, 120(16):e2214430120 · DOI 10.1073/pnas.2214430120 · PMID 37040399 · PMCID PMC10120010
开放获取（CC BY-NC-ND 4.0）· 全文 https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10120010/fullTextXML

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **Z04**（组：周如鸿组） |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory 记 `fetch_channel=epmc_fulltext`，本地抓取） |
| 本地全文 | `data/literature_cards/fulltext/Z04_PMC10120010_text.txt`（55,116 B，SHA-256 `6028eea6a0b6c69e…`）；同源 XML `Z04_PMC10120010_fullTextXML.xml`（119,817 B） |
| 对照底稿 | `sources/zhou.md:59-70`（原卡）、`sources/zhou.md:210`（演进链"2023–2024 纯物理 FEP 主导 + 暴露痛点"段） |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中） |
| 未取到的部分 | ①**SI Appendix 全部**：表 S1（穷举点突变与其 ΔΔG 全表，即"点突变命中率"的分母与分子）、表 S2（双突变全表）、表 S3（p6 的 13 个突变值）、表 S4（frustration 计算用值）、图 S1（RMSD）、图 S2（Val4 结构）、图 S3（R² 分布）、图 S4（TCR 序列）、图 S5（相关性分布）与 SI 公式；②图 2-5 的原图数值；③增殖/CD69 的逐条百分比。凡涉及这些之处本卡只写正文口径并明写"正文未给出" |
| 与底稿的差异（本次补出来的内容） | 原卡的 MD/FEP 参数（500 ns、<0.5 nm/300+ ns、34 λ × ≥200 ps、≥340 ns/突变）本次**逐条在全文 Methods 里命中并补上原句**；另补：为什么用 FEP 而不用 ML、突变集怎么来的（含**审稿人要求补锚点全类别突变**）、点突变几乎全负之后的转向逻辑、intuition 被自己的计算推翻（p6-p7 双酪氨酸 motif）、frustration index 1.5 的算法口径、"95% CI 与零重叠所以不能说结论性一致"、阴性对照 M7 意外阳性后的解释方式（猜测 register shift）、catch-bond 替代解释、以及未跑 μs 级构象采样这一自认局限 |

## 1. 这篇到底解决什么（大白话）

1 型糖尿病（T1D）的一个自身抗原 X-idiotype（来自同时表达 TCR 与 BCR 的"X-cell"）已知能结合 HLA-DQ8 并激活 CD4 T 细胞。要做抗原疫苗，需要知道**抗原上每一个残基对结合贡献多少、能不能改一改让结合更强**。实验测这些亲和力（量热/结合实验）"costly and time-consuming"，序列型机器学习又只能在有限数据集里学；他们于是用**自研体系不受既有数据分布约束**的物理路线：MD 选出稳定复合物结构 → FEP 逐个突变算 ΔΔG → 把预测增强的多肽合成出来，用 PBMC 的 CFSE 增殖 + CD69 活化做功能回验。

**结果分两层**：计算层"几乎全部点突变都让结合变差"，能挑出来的少数有利突变来自**换位/双突变**；实验层 7 条设计抗原 CD69 活化全部高于天然抗原，增殖 4/7 增强或维持。预测与功能读数的相关性作者自己写"though low"，只够分"增强/减弱"两个方向。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **主矛盾：点突变的 FEP 命中率极低，且这是重复发生的事**。原句："Fig. 2 B reveals that almost all our initial point mutations resulted in a loss of binding"
   **应对**：不是去调力场或加采样，而是**换候选类型**——"Given the low success rate of point mutations,"，并把前作验证过的换位策略直接搬过来："In our previous investigation of HLA antigen binding, we found that residue-swapping mutations,"，初轮换位集就是穷举出来的："Initial residue-swapping mutations included p3-p4, p3-p7, p4-p5, p4-p7, p5-p6,"
   **代价**：突变数量（也就是算力）翻倍以上；正文没有给点/双/换位各自的命中分数（分母在未取到的 SI 表 S1/S2），因此"命中率低"是作者的定性陈述，不是一个可引用的数字。
2. **自己的直觉是错的，而且错在关键 motif 上**。他们本以为 p6-p7 双酪氨酸是结合必需的："Our intuition led us to believe that this Tyr6-Tyr7 motif was largely stable"（原文此处紧跟一个带引号的短语，本卡不跨引），实测相反："Surprisingly, the p5-p6 swap mutation of Val5->Tyr and Tyr6->Val (V5Y_Y6V) was determined to be"、"However, numerous double mutants of Tyr6-Tyr7 quickly confirmed that this motif was improvable upon"
   **应对**：接受计算结论并把它转成可检验的机理假设——先分解（"From decomposition of the favorable Val5Tyr6Tyr7"），再对 p6 做**系统化突变扫描**："Lastly, we sought to explore the mutation space"；最后用**frustration 分析**给"为什么能改"补一个独立指标："From a targeted frustration analysis ( 46 ,"
   **代价**：换位/双突变的"为什么好"最后落在体积相关（R²=0.37）与一个自算的 frustration index 上，作者自己承认疏水性无相关（R²=0.02），机理并未闭合。
3. **审稿人要求扩表，计算量被迫追加**。"SI Appendix , Table S1 shows a list of all"，且穷举口径写得很清楚："Categorical mutations included either residues of"
   **应对**：照做（锚点 p1/p4/p6/p9 + 高接触面 p7 全类别突变），并明确排除 Pro 的理由（主链突变歧义）。
   **代价**：这一轮"补全表"是纯成本，没有提高命中率；也说明正文里的"低命中率"部分是审稿之后补齐的样本，不是原计划的对照设计。
4. **误差棒与零重叠 ⇒ 结论性一致不敢讲**。实验 4 条趋势相符的突变体，作者自己下了限制："For instance, mutants M2 (Y6V_Y7V), M3 (Y6Q_Y7Q),"
   **应对**：①统一口径 "All error bars in this work are 95% CI."；②对预测与实验分歧最大的两条给出可检验的归因假设："The M1 (V5Y_Y6V) swap mutant and M6 (Y6I) point" + "posit that we may not have captured important"；③把整体预测能力降格成"够用就行"："This correlation value, though low,"
   **代价**：**这是本篇最硬的一条限制**——ΔΔG 的置信区间跨过 0，意味着"FEP 判增强"在统计上并未成立；他们靠"方向对 + 实验都阳性"来支撑结论，而不是靠区间分离。
5. **阴性对照意外阳性，没有解释，只有猜测**。"The M7 (Y6R_Y7R) mutant was"
   **应对**：先用结构事实给一个可能机制："Given the absence of charged"（他们此前工作已知 DQ8 可用不同 register 结合同一抗原）。**本文未解决**：没有做 register 交换的验证实验，负对照失效就留在讨论里。
6. **"活化"与"增殖"两个读数不一致**。"X-Id mutants M3, M5, and M6 show reduced" 与 "Despite differences in proliferation, all CD4 T cell populations were found to be functionally activated as measured by the upregulation of surface CD69 activation marker when compared with unstimulated cells"。
   **应对**：不强行归一到"亲和力决定功能"，而是承认这条链条本身不闭合："Importantly, the HLA-TCR"、"However, affinity maturation"；再引一个**替代优化目标**（catch bond）来安放这些数据："For this technique, pHLA-TCR"
   **代价**：目标函数从"亲和力最大化"变成"按治疗意图挑方向"（HLA-blocker 型反而要 TCR 结合弱："In this case, the X-idiotype mutants V5Y_Y6V and Y6Q_Y7Q are superior due to their enhanced binding affinity for HLA and reduced binding affinity for TCR."），命中率因此无法定义成单一指标。
7. **FEP 前置结构的采样极限，作者主动写明**。"Notably, we do not run extensive MD simulations ( ≈ μ s ) to account for any structural changes that could occur upon mutation ( 48 )."，并给出不做的理由："Single point mutations in"
   **应对**：改在**同一结构上做大量突变、再用长窗口多副本复算有希望的**（见第 3 节 C 段），把算力花在自由能收敛而不是构象搜索。
   **代价**：位点特异的结构重塑风险被假设排除；这与第 2.4 条"没抓到长时间尺度构象变化"是同一处漏洞的两面。
8. **建模侧的取舍与人工介入**：只保留 α1/β1（"After the initial MD simulations, only the HLA-α1 and HLA-β1 domains were modeled; α2 and β2 domains were excluded due to their distance from the antigen."）；TCR 靠 Modeller 以 6DFX 为模板搭（"The TCR homology structure"）；抗原是把 PDB 5UJT 里的天然 mimotope 用 VMD 原地改成 X-idiotype 序列（"The HLA-X-idiotype antigen"）。**应对**：用 500 ns MD 的 RMSD 稳定性来给建模结果"发合格证"（"Briefly, this antigen-bound"；判据句见第 3 节）。**代价**：三级复合物的界面完全来自同源建模 + 短均衡，没有任何界面结构实验验证（cryoEM/晶体未做，本文无）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **结构准备**：VMD 定点改序列建模（HLA-DQ8–X-idiotype，源 PDB 5UJT）+ Modeller 同源建模 TCR 可变域（模板 PDB 6DFX）；NAMD2 + CHARMM36 + TIP3P + 100 mM NaCl，310 K、2 fs。
- **准入判据（第一道）**：**MD 稳定性**——RMSD 达标才拿来算自由能。原句："After MD simulation, the final"
- **打分器（核心）**：**FEP（soft-core 势能）**，结合态/游离态两态分别算 ΔG，取差 ΔΔG；误差用 **95% CI**（多副本平均）。
- **归因/辅助分析**：HLA–抗原接触面积分析（定锚点与 p7）、突变体周围残基相互作用解析、体积-亲和力与 Eisenberg 疏水性-亲和力的 Pearson 相关、**single-residue frustration index**（用同一位点 13 个突变的自由能分布算）。
- **实验回验**：固相多肽（Peptide 2.0，>95% 纯度）→ DQ8+ T1D 供者 PBMC → CFSE 稀释法 CD4 增殖 → 流式（Attune-Nxt，TCRab+CD4+ 门控）→ anti-CD69 活化；无抗原与抗 CD3-CD28 作阴性/阳性对照。
- **没有用的方法**：**QM/MM、DFT、机器学习势、ML 预测器**（他们对 ML 的态度是"快但受限于数据集"，见 2.1 与第 3 节 A1）；也没做结合实验层面的 SPR/ITC/biolayer（功能读出全部是细胞层面的）。

### A. 建模与准入（正文 Results 首段 + Methods）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 起点问题：要不要用 ML 做突变亲和力预测 | 方法论选择（引言明确对比） | 判据＝是否受既有数据集分布约束："Although machine learning"；选 FEP 的理由："One of the advantages of the" | 路线定为 in silico 突变扫描 + 细胞功能回验 |
| A2 | PDB 5UJT | VMD 把 mimotope 原地突变成 X-idiotype；TIP3P + 100 mM NaCl 溶剂化；CHARMM36 | 最小化两步各 50,000 步（先重原子约束、后无约束）→ 10 ns 均衡 | 二元复合物 HLA-DQ8–X-idiotype 起点结构（序列 "The X-idiotype sequence is"） |
| A3 | A2 体系 | NAMD2 生产 MD，310 K、2 fs | **RMSD <0.5 nm 且持续 300+ ns** 才算稳定并作为后续结构 | **500 ns** MD；选出用于 FEP 的构象 |
| A4 | A3 结构 | 接触面积 / 溶剂暴露分析定"可突变位点" | 判据＝锚点残基 + 高接触面残基（正文：p7 意外高接触但非传统锚点） | 锚点 Asp1/Met4/Tyr6/Asp9 + 高接触 Tyr7 → 后续突变集 |
| A5 | A3 结构 + 只保留 α1/β1 | 建 TCR 可变域（Modeller，模板 6DFX）、对齐到 6DFX、同样溶剂化与最小化流程 | 与 A3 同一 MD 判据 | 三级复合物 pHLA-TCR；TCR 接触面取生产轨迹末帧、按 **4.5 Å** 判接触原子 |

### B. 第一轮点突变（几乎全负 → 转向）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | A4 定义的位点 | 初始点突变：同类残基替换 + 已知能提升柔性的替换 + 经验猜测 | ΔΔG<0 记"增强"；误差 **95% CI** | 结果句："almost all our initial point mutations resulted in a loss of binding affinity"；只有 p4 两条有利："two substantially hydrophobic" |
| B2 | 同一批结构 | FEP 单次计算 | **34 λ 窗口 × ≥200 ps = 6.8 ns/次**，soft-core 势能 | 每条突变的 ΔΔG ± 95% CI |
| B3 | 审稿意见 | 追加锚点 p1/p4/p6/p9 与 p7 的**全类别点突变**（14 种非 Pro 氨基酸集 + 同电荷替换） | 排除 Pro（主链突变歧义） | 全表在未取到的 SI Table S1；正文只给"穷举"这一事实 |
| B4 | 有利/不利结果 | 结构归因（残基埋藏深度、与 HLA 具体残基的作用差异） | 判据＝侧链填充与接触数变化 | 解释 M4V 不利："reveals poor space-filling"；并给出 M4L、M4I、M4V 的 ΔΔG 数值（见第 4 节） |
| B5 | 反向验证 | 检查侧链朝外残基（Ala3、Phe8）的突变 | 预期＝中性；实测吻合 | "Most of the mutations on" |

### C. 第二轮：双/换位突变 → p6 系统扫描 → 复算 → 实验

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | B1 的低命中 | 改做**换位突变 + 双突变**（6 组换位 + 双突变集，全表在 SI Table S2） | ΔΔG<0 且 95% CI | 头部结果 V5Y_Y6V（"robustly favorable"）与 Y6V_Y7V |
| C2 | C1 结果 | 把有利双突变**拆解到单残基**归因 | 判据＝哪个位点贡献增益 | "Val5 and Tyr7 mutations largely" → 锁定 p6 |
| C3 | p6 | Tyr6 → **13 个残基**逐一 FEP（SI Table S3） | 体积相关 R² **0.37**；疏水性相关 R² **0.02** | 作者结论 "The binding improvement of" → 小体积疏水残基有利；frustration index 1.5 佐证天然 Y6 高受挫 |
| C4 | C1/C3 的有利突变 | **复算加长**：结合态/游离态两态、多副本 | "Mutations that were found"；**34 λ × ≥1 ns = 34 ns/次**，"These FEP calculations were" | 复算名单（正文点名）：HLA 侧 M4L、V5Y、Y6V、Y6I、Y7W、V5Y_Y6V；pHLA-TCR 侧 Y6C、Y6I、Y6V_Y7V。全研究累计模拟量正文口径："The total simulation time for"（约 5 μs） |
| C5 | C4 的 pHLA-TCR 预测 | 选 7 条 mutant 序列送合成（表 1：x-Id-mutant-1 至 mutant-7），加天然 X-Id 与 insulin-mimotope 对照 | 合成品纯度 **>95%** | 7 条设计多肽 + 2 条对照；供者为单个 DQ8+ T1D subject |
| C6 | C5 多肽 | PBMC CFSE 标记 → 24 孔（1.5–2.0×10⁶ cells/well）抗原刺激 **7 d** → 流式门控 CFSE-low CD4 | 每样采集 **400,000–500,000** 淋巴细胞；无抗原/抗 CD3-CD28 作阴/阳对照 | 增殖：M1、M2、M4、M7 相当或增强（"expand CD4 T cell populations"）；M3、M5、M6 减弱 |
| C7 | C6 细胞 | anti-CD69 染色读活化 | "We used anti-CD69 staining as a" | 全部设计抗原 CD69 活化高于天然："revealing that all designed" |
| C8 | C4 预测 vs C6/C7 实测 | 逐条比对方向 + 算 Pearson 相关（相关分布仅在 SI Fig S5） | 判据＝趋势方向一致 + 95% CI 是否跨 0 | 结论句："This correlation value, though" |

## 4. 关键数字台账（全部来自本地全文）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 500 ns | HLA-抗原、HLA-抗原-TCR 体系的生产 MD 时长 | "we simulated the system for 500" |
| 310 K / 2 fs / 10 ns 均衡 / 50,000 步 ×2 | 温度、步长、均衡时长、最小化步数 | "The structure was then minimized for 50,000 steps with heavy atom protein constraints and then an additional 50,000 steps without constraints"；"After 10 ns of equilibration" |
| **<0.5 nm 持续 300+ ns** | 结构准入判据（RMSD 稳定性） | "the final structure was selected based on rmsd analysis showing structural stability (<0.5 nm) for 300+ ns" |
| 34 λ 窗口 × ≥200 ps = **6.8 ns/次** | 初筛 FEP 的窗口数与单次时长 | "All FEP calculations were" |
| 34 λ × ≥1 ns = **34 ns/次**；≥5 副本 × 2 态 = **≥340 ns/突变** | 复算档位的时长/副本/两态口径 | "conducted over 34 λ windows"；"an aggregate of at least 34ns ×" |
| ≈5 μs | 全研究累计模拟时长 | "The total simulation time for" |
| M4L **−1.3 ± 1.0**、M4I **−0.6 ± 0.4**、M4V **+2.1 ± 0.7** kcal/mol | 三个 p4 突变的 ΔΔG（±95% CI） | "M4L with Δ Δ G = - 1.3 ± 1.0 kcal/mol and M4I with Δ Δ G = - 0.6 ± 0.4 kcal/mol, ± 95%CI"；"A similar hydrophobic mutation," |
| 13 个 | p6（Tyr6）被单独突变的残基数 | "by mutating Tyr6 to 13 different residues individually" |
| 体积 R² **0.37** / 疏水性 R² **0.02** | 突变亲和力与残基体积/疏水性的 Pearson 相关 | "resulting in a Pearson's"；"Surprisingly, Eisenberg hydrophobicity has no correlation with affinity, R 2 = 0.02" |
| frustration index **1.5** | 天然 p6 Tyr 的单残基受挫指数（>1.0 SD 即"highly frustrated"） | "The single-residue-level" |
| 6 组换位 | 初轮换位突变组合（p3-p4、p3-p7、p4-p5、p4-p7、p5-p6、p3′-p4） | "Initial residue-swapping" |
| 14 种氨基酸集（无 Pro） | 全类别点突变的替换残基集 | "mutated to the set of A, C, F," |
| 4.5 Å | TCR 接触面判定距离（生产轨迹末帧） | "showing contacting TCR atoms" |
| 7 条设计抗原；4/7 增殖；CD69 7/7 | 实验回验送样与功能结果 | "four out of seven antigens" |
| 四到七倍 / 一到七倍 | 增殖倍数（增强组）与突变体间增殖跨度 | "expand CD4 T cell populations"；"CD4 T cell proliferation" |
| >95% 纯度；1.5–2.0×10⁶ cells/well；7 d；40万–50万事件 | 多肽纯度、接种量、培养时长、流式采集量 | "all antigenic peptides used in"；"Around 400,000 to 500,000 lymphocytes (singlet gated) were acquired for each sample" |
| NAMD2 / CHARMM36 / TIP3P / 100 mM NaCl / IBM Power8；Modeller、模板 6DFX；PDB 5UJT | 模拟软件与建模来源 | "All simulations were run using" |
| 95% CI | 全文所有误差棒口径 | "All error bars in this work are" |

## 5. 结论——作者说了什么

1. X-idiotype 的锚点贡献可拆解：p4 Met 可被更疏水的小一号残基替换而**略微**增强 HLA 结合（M4L/M4I）。
2. **点突变几乎全负、双/换位突变才有货**：这是他们从数据里得出的、并写进推荐的意见——"We have previously found ( 31"
3. p6 是主要的可改进位点，机制是**位阻/受挫**（小体积疏水有利、frustration 1.5、疏水性与亲和力无相关）。
4. pHLA-TCR 端可以**朝两个方向挑**：Y6C/Y6I 增强 TCR 结合；V5Y_Y6V、Y6Q_Y7Q 增强 HLA 但削弱 TCR，适合做成 HLA-blocker 型治疗。
5. 实验端："These in silico predictions"；全部设计抗原 CD69 活化不低于天然，7 条里 4 条增殖增强或维持。
6. 自我定位的预测能力：相关性"though low"，但"足以把增强型与减弱型分开"；四条趋势相符的突变体因 95% CI 跨 0 而不能称"结论性一致"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **他们真正的筛子是"MD 稳定性准入 + ΔΔG<0"两件事，而命中率低的原因是候选空间的性质，不是力场不够准**。当"几乎全部点突变都变差"时，任何判据都无法提高命中率（正类本来就稀少）；他们靠**改变候选类型**（换位/双突变）把正类造出来。→ 对我们：若某类事件在计算上几乎不可能出现正例，应改候选生成方式（例如把位点组合/环改造/多步突变纳入空间），而不是把筛子调严。
2. **长窗口 + 多副本 + 两态复算是"置信度"开销，不是"筛选"开销**。340 ns/突变 花在已经通过初筛的少数突变上。→ 对我们：把算力分两档（便宜粗筛 / 昂贵复核）是可行的，但必须像本文一样在正文点名复核名单，否则无法复盘漏斗。
3. **ΔΔG 的 95% CI 跨 0 ⇒ "预测被验证"这句话在本篇并不成立**；支撑结论的是**实验端的方向一致 + 全部阳性**。也就是说：这一篇的证据强度来自湿实验，而不是来自 FEP。引用它时不能把"FEP 命中"当预测能力。
4. **功能读数有两个（CD69 活化、CFSE 增殖），且彼此不一致**，作者没有把它们合成一个分数，而是保留双口径 + 承认相关性低。→ 对齐我们的要求：产物化学读出与细胞读出必须分开记，允许写"两个读出不一致"，不许压成一个总分。
5. **负对照失效（M7）后他们没有撤回结论，而是给出可检验的替代机制（register shift）并明写是猜测**。这比"删掉异常数据"更符合我们的记录纪律；但同时也说明：**这类体系的阴性对照不是可靠闸门**，我们自己设计对照时必须预期"失效也需解释"。
6. **他们没有 μs 级构象搜索，却把"没抓到长时间尺度变化"当成失败归因**——这是本文对自身方法最诚实的一句自限。若我们要用长时 MD 判催化，必须先把"多少 ns 才够"变成可测问题（Z08 正是这条的实证，见该卡）。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者自述：①"though low" 的预测-功能相关性；②95% CI 跨零使四条"相符"的突变体不能被称结论性一致；③未做 μs 级构象采样（2.7）；④"higher TCR binding affinity does not necessarily correspond with higher T cell functional activity"，亲和力成熟不必然等于功能；⑤M7 负对照意外阳性未解释；⑥M3/M5/M6"高活化低增殖"未解释，只提 catch bond 假说并"encourage additional study"。
- 我们读出：①**所有突变清单与命中率分母都在未取到的 SI 表里**，正文只给定性结论"低命中率"，因此"点突变命中 <X%"这类数字本文给不出，任何引用都不该编造；②样本量：功能实验来自**单个 DQ8+ T1D 供者、未设生物学重复描述**（正文只写 PBMC 分离与门控），个体差异未评估；③HLA-DQ8 二元结构与整个 pHLA-TCR 界面来自同源建模 + 500 ns MD 末态，无界面实验验证；④p7、p5、p9 等位点在双/换位轮里覆盖到什么程度取决于 SI 表，正文的"p6 是关键位点"可能受审稿补表影响（选择是在算完之后陈述的）；⑤全文没有一条 Kd/KD 实测值，功能读出是细胞层面的相对量，不能与其他工作的亲和力数字横向比较。

## 8. 迁移判断：哪些能搬、哪些不能搬

**先划边界（本卡的强制性提醒）**：这篇是**抗原被 HLA 呈递、以及 pHLA 被 TCR 识别的结合亲和力优化**。它的全部判据（ΔΔG、RMSD 稳定性、frustration、体积相关）都是**静态界面热力学**；实验读出是 T 细胞活化/增殖。**它不是酶，没有任何化学转化事件，没有任何转换数或产物身份数据。** 因此：**周组这套 FEP 在这类体系里的"命中"与"命中率低"，不能当成目标酶催化能力的判据或先验概率**；同理，把 Z01/Z02 的适配体-蛋白亲和力 FEP 命中率搬过来也不行（那是同一族的边界错误）。

**可迁移（怎么用）**

1. **"MD 稳定性当准入，FEP 当打分"的两段式结构**，且两段时长差一个数量级（500 ns 选结构 / 6.8 ns 粗筛 / ≥340 ns 复核）。→ 我们若用 MD+端点法/xTB 打分，也应明确"结构准入 vs 候选打分"是不同预算档位，并在正文点名谁进了复核档。
2. **正例稀到几乎不存在时，改候选空间而不是改阈值**（点突变→双/换位突变）。→ 对我们：若单点突变在计算上必然打负，应把"多残基组合 + 环重构 + 金属/辅因子位点协同改造"纳入候选生成，而不是收紧 ΔΔG 阈值把负类切得更干净。
3. **误差口径统一 + 不许跨零断言**（"All error bars in this work are"；CI 跨 0 时明写"contesting a statement of"）。→ 直接搬：我们每个通过判据的候选必须带区间，且区间跨零时不得写"预测被证实"，只能写"方向一致"。
4. **双功能读数并存（活化 vs 增殖）不做归一** → 我们保留"产物检出"与"转化量/竞争副产物"两条读数，允许不一致并写明。
5. **失败/异常结果给出可检验的机制假说而不是删掉**（register shift、catch bond）→ 我们给"无产物候选"标注可能卡住的事件（分步化学事件），并把它们列入可反驳清单。
6. **正交解释指标**（frustration index、体积相关性）用于把"数字大小"变成"结构理由"→ 我们可以用几何/静电/柔性指标解释候选好坏，但这些**只作解释**，不作准入闸口（见下一条）。

**不可迁移（为什么不能照搬）**

1. **ΔΔG<0 不是"能催化"的判据**。它衡量某一结合态相对另一结合态的自由能差；酶活需要的是**反应路径上的能垒与竞争性副产物分支**。用本文的 ΔΔG 阈值去闸酶设计候选，等于用"绑得紧不紧"判"会不会转"。
2. **"FEP 对 pHLA 体系方向对但幅度不精"不能外推成"FEP 对酶突变有效"**。本文自己的置信区间跨零，且没有任何速率数据。
3. **RMSD <0.5 nm/300+ ns 这条准入判据衡量的是"复合物在模拟里不漂"，与催化几何无关**：漂不漂与能不能催化没有蕴含关系（我们的催化位点可能要求在纳秒尺度有特定柔性/瞬时排布，此时"稳定"反而是排除条件）。若要引用，只能作为**结构可信度前置检查**，不能作为酶活证据。
4. **frustration index / 体积-亲和力相关是"结合位点可改造性"的启发，不是活性位点可造性的度量**；酶设计的活性位点问题不是"天然残基受挫"，而是"人工组装的催化阵列能否走通化学步骤"。
5. **细胞功能读出（CD69/CFSE）没有等价物**：我们的功能读出必须回到化学（LC-MS/MS、同位素、产物身份），不能类比成"某个生物读数上升即成功"。
6. 本文没有 QM/QM-MM、没有过渡态、没有速率，所以它既不能支持也不能反驳"用 QM 判催化能否发生"；那类主张要另找参照（本文无）。

## 9. 溯源与自检

- 引句底稿: data/literature_cards/fulltext/Z04_PMC10120010_text.txt（本卡全部英文引句均从这一份逐字复制；同源 XML `Z04_PMC10120010_fullTextXML.xml` 与登记底稿 `sources/zhou.md` 见 `sources_map.json`）。
- 归一化说明：本地纯文本由 Europe PMC fullTextXML 去标签得到，HTML 实体已解码、引号/破折号统一、空白折叠；上标（如 R 2、Δ Δ G、μ s）在原 XML 里是 `<sup>` 标签，去标签后留下空格形态，本卡引句按该形态原样抄写。
- 阅读定位方式：先把归一化单行全文按句切到临时文件（`A:\AITEMP\Z04.sent.txt`，737 句）再分段精读；正文内容集中在句 20–337，其后为参考文献。
- 对照底稿行号：`sources/zhou.md:59-70`（原卡，含 FEP/MD 参数与 4/7 命中率）；`sources/zhou.md:210`（演进链里对 Z04 的定位："单点突变 FEP success rate 低 → 被迫上双突变/换位突变"）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字/是否用MD`；第 4 节 ↔ `候选数递减/实验命中率/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only Z04 --no-report` 把卡内所有不含中日韩字符、被直双引号包住的 ≥20 字符片段，在"引句底稿"指向的全文里逐字查找，任何一条不命中即 FAIL；本轮结果见交付回报。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 62 条逐字引句来自许可受限的第三方来源（Z04；CC_BY_NC_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（物理模拟 + 合作湿实验闭环；方法校准与候选优化并重）
target=HLA-DQ8 呈递的 X-idiotype 自身抗原（1 型糖尿病疫苗抗原）及其与 TCR（TRAV29/DV5-J53 / TRBV6-5-D1-JB1-1）的三元复合物 pHLA-TCR
backbone_generation=不做 de novo 骨架：从 PDB 5UJT 用 VMD 把 mimotope 原地改为 X-idiotype 序列（CARQEDTAMVYYFDYW），Modeller 以 PDB 6DFX 为模板建 TCR 可变域；候选=锚点 p1/p4/p6/p9 + 高接触 p7 的全类别点突变穷举，点突变不利后转双突变与 p3-p4/p3-p7/p4-p5/p4-p7/p5-p6/p3′-p4 换位突变，再对 p6 做 13 个单点突变系统扫描
computational_filters=准入判据＝MD 稳定性（RMSD <0.5 nm 持续 300+ ns）；打分器＝FEP（soft-core，34 λ 窗口）ΔΔG<0 判增强、误差用 95% CI；归因指标＝HLA 接触面积/溶剂暴露、突变体周围残基相互作用、体积与 Eisenberg 疏水性的 Pearson 相关、single-residue frustration index（同位点 13 个突变自由能分布）；ML 预测器被明确排除（受限于有限序列数据集）
thresholds=RMSD <0.5 nm 且持续 300+ ns；初筛 FEP 34 λ × ≥200 ps = 6.8 ns/次；复核 34 λ × ≥1 ns = 34 ns/次 × ≥5 副本 × 2 态 = ≥340 ns/突变；判"增强"用 ΔΔG<0（未给绝对数值阈值）；误差棒一律 95% CI；TCR 接触判定 4.5 Å；多肽纯度 >95%；310 K、2 fs、100 mM NaCl、CHARMM36、TIP3P、NAMD2
md_used=是（两处核心用途：①500 ns 生产 MD 用于选稳定复合物构象并作候选准入闸门；②FEP 的 λ 窗口 MD 采样本身；并非只做事后机理）
qm_used=否
experimental_methods=固相多肽合成（Peptide 2.0，>95% 纯度）→ DQ8+ T1D 供者 PBMC（Ficoll）→ CFSE 标记 + 24 孔 1.5–2.0×10⁶ cells/well 抗原刺激 7 d（无抗原／抗 CD3-CD28 作阴／阳对照）→ Attune-Nxt 流式门控 TCRab+CD4+、按 CFSE-low 计增殖（每样 40 万–50 万事件）→ anti-CD69 活化染色
pipeline_counts=锚点 p1/p4/p6/p9 + p7 全类别点突变（SI Table S1，未取到分母）→ 点突变几乎全部降低结合（正文定性）→ 双/换位突变（SI Table S2）→ p6 的 13 个单点突变（SI Table S3）→ 有希望者进 ≥340 ns/突变的复算（正文点名 6 条 HLA 端 + 3 条 pHLA-TCR 端）→ 7 条 mutant 肽送合成（另加天然 X-Id 与 insulin-mimotope 对照）→ 实验：CD69 活化 7/7、增殖增强或维持 4/7
hit_rate=点突变：作者称 almost all our initial point mutations resulted in a loss of binding affinity，且与前作 only a low rate of the tested mutations turns out to be favorable 持平（正文未给可复算的分母）；有利单点仅 p4 的 M4L/M4I 与 p6 的若干突变，头部增益来自换位/双突变 V5Y_Y6V、Y6V_Y7V；实验端功能读出 4/7（≈57%）增殖增强或维持、CD69 7/7；预测-功能相关性作者自述 though low、且 4 条趋势相符者的 95% CI 跨零
best_metric=未记录（全文报 ΔΔG kcal/mol 而非 Kd：M4L −1.3 ± 1.0、M4I −0.6 ± 0.4、M4V +2.1 ± 0.7 kcal/mol；实验端只给相对增殖/活化倍数，无绝对亲和力）
cost_or_stat_note=全研究累计模拟时长正文口径约 5 μs；每突变复算 ≥340 ns（34 ns × 5 副本 × 2 态）；IBM Power8 集群；无 GPU 时/金额数字；实验为单个 T1D 供者、未做预测-实验的统计显著性检验，误差一律 95% CI
role_in_timeline=周如鸿组 2021–2023 纯物理 FEP 阶段的核心论文：①给出该组少见的"初筛 6.8 ns → 复核 ≥340 ns"两档算力分配；②把"单点突变 FEP 命中极低"写成公开事实并据此转向双/换位突变（不是调力场）；③同时暴露这条路线的两处天花板——ΔΔG 的 95% CI 跨零使预测不能被称验证、以及亲和力成熟与 T 细胞功能不等价（后续 Z08 转而检验筛选器本身可靠性）
source_pointer=data/literature_cards/fulltext/Z04_PMC10120010_text.txt（SHA 6028eea6a0b6c69e…）+ Z04_PMC10120010_fullTextXML.xml；sources/zhou.md:59-70、210
CSV回填-->
