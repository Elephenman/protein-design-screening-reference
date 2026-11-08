# [B25] 层级化设计准对称纳米笼——当"破坏对称"比"造界面"更难：物理打分在负向目标上失效

Dowling Q, Park Y-J, Fries C, Gerstenmaier N, Ols S, Yang E, Wargacki A, Dosey A, Hsia Y, … Veesler D, Baker D, King N（华盛顿大学 IPD / 生工 / 生化，HHMI）
Nature 638:553–561（2024-12-18 在线；2025 刊期）· DOI 10.1038/s41586-024-08360-6 · PMID 39695230 · PMCID PMC11821544（CC BY 4.0）
预印本：bioRxiv 2023-06-17 / Research Square 2023-07-10（题录见全文首部）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B25**（组：Baker组） |
| 本地全文 | `data/interim/baker_lit/ft/nanocage_hier2025.txt`（92,623 B，2026-10-16 抓取；batches.tsv 第 8 批，state=FULLTEXT） |
| 对照底稿 | `sources/baker.md` 第 329–340 行（原卡）；汇总引用见 `sources/baker.md:550/612/648` |
| 登记底稿清单 | `sources_map.json` 键 B25：上述全文 + `sources/baker.md`；本卡全部英文引句在全文里逐字命中（门禁 `--only B25`） |
| 证据级别 | **全文级** |
| 未取到的部分 | 补充信息（SI 序列表 Supplementary Table 1、凝胶源图）、Extended Data Fig 1–6 原图数值、cryo-EM 地图文件本身。涉及处本卡注明"正文/图注口径" |

## 1. 这篇到底解决什么（大白话）

以往 de novo 自组装颗粒全靠"严格对称 + 现成寡聚体"，把要设计的新界面数量压到最少，代价是结构空间极窄——最大只做到 120 亚基。这篇借病毒衣壳的"准对称"（pseudosymmetry，序列不同、骨架近似对称）思路，用**层级化**办法：先在一个超稳同源三聚体（1WA3 醛缩酶）上做出"序列不对称但几何仍对称"的杂三聚体，再把三聚体当积木拼出 240、540、960 亚基、直径 49/71/96 nm 的二十面体准对称纳米笼——"the largest bounded computationally designed protein assemblies generated to date"。核心方法学贡献不在打分更准，而在**换了一个便宜读出**（与既有 I53-50 笼共组装后跑非变性胶）把"基因型→表型"接上。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **打破对称=界面数翻倍，直接做不可行**。作者盘点四条扩size路线后自否："it is currently impractical, as it would compound the low success rates of existing interface design methods"（逐条设计非对称界面的路线）；准对称路线也因"current computational protein design methods lack the precision required to reliably encode in a single amino acid sequence the multiple subtly different backbone conformations"（同序列多构象，Caspar–Klug 式准等效）被搁置。→ **应对**：层级化——"a hierarchical approach in which pseudosymmetric oligomers are designed first and subsequently used as the building blocks of larger pseudosymmetric assemblies would enable the distinct interfaces to be designed and validated individually"，先把不对称压缩进三聚体，再只做一次 dock-and-design 扩到 240+。
2. **物理打分对"负向目标"几乎失效（本文最有迁移价值的失败）**。他们要的不是"稳定界面"而是"破坏同源三聚对称"，用 Rosetta 全单/双突变扫描（阈值：单突变使 ddG 或总分升超 100 REU 算候选破坏突变——"Ninety-six unique individual mutations increased the predicted homotrimerization energy (ddG) or Rosetta score by more than 100 Rosetta energy units"；理想对："Ideal mutant pairs were those where one or both single mutations increased the energy of the trimer relative to the wild type (that is, normalized scores > 0) while the double mutation had no effect or stabilized the trimer (that is, normalized scores ≤ 0)"）。结果湿测完全不对齐：82 个单突变里只有 3 个真的破坏——"The 1WA3 trimer proved remarkably plastic: only 3 out of the 82 single mutants tested did not yield a band corresponding to the assembled I53-50 nanocage"。→ **应对**：换读出/认账——把筛选做成"能否与 I53-50B 共组装成笼"（genotype→phenotype），"Key to our success was having an efficient screen for connecting genotype to phenotype (in this case, maintenance of backbone symmetry)"；并把失效原因归到起点选择上："Although this choice contributed to the successful expression of a large number of mutants, it also led to the low success rate of symmetry-breaking mutations: 1WA3 proved remarkably resilient to mutations intended to disrupt the homotrimer"。→ **遗留代价**：方法学目前只在"已有组装读出"的寡聚体上打通（"Although at present this approach may limit the use of our experimental screen to a subset of known protein oligomers"），寄望于结构预测进步后放开（"We expect this limitation to further diminish as methods for protein structure prediction and design continue to yield improved success rates"）。
3. **想要 ABC 三等分杂三聚体，做出来的却是 AAB/ABB+AAA 污染物**。三顺反子 ABC 共表达经 IMAC+StrepTrap 两步纯化后 "SDS–PAGE analysis suggested the presence of trimers comprising predominantly a mixture of the A and B subunits, with little of the C subunit"。→ **应对**：不加更多打分，改做"机制确认+废物利用"：构建 AB 双顺反子对照排除 C 链干扰，用天然质谱把组分认全——"a trimer comprising one copy of the A chain and two copies of the B chain ('ABB'), as well as a trimer comprising two copies of the A chain and one copy of the B chain ('AAB')"（Fig 1h）；随后承认"Although not the intended ABC heterotrimer, we realized that these heterotrimers were probably pseudosymmetric"，把 AAB/ABB 转作积木；再验证骨架对称未破（与 I53-50B 1:1 组装后负染 EM 看到 I53-50 形貌）。**代价**：此后所有制备都要处理 AAB/ABB 交叉污染（IMAC 梯度三峰分离 ABB/AAB/AAA；"This step removed the I3-01-like assemblies but did not resolve the ABB and AAB trimers."——SEC 分不开二者）。
4. **意外污染反而"发现"了 540 亚基笼**。GI4-F7 电镜图里混着 71 nm 颗粒——"Unexpectedly, in a number of the GI 4 -F7 micrographs we also observed a 71-nm nanocage with a similar wireframe morphology and hexagonal pores"。→ **应对**：数六角孔定 h=3 → T=9，提出机制解释（AAB 制剂中的少量 ABB 形成二聚体"disymmetron"占二十面体二重轴），并反过来利用：分别抛光 AAB/ABB 组分按 1:1:1 与 CCC 组装以提高均一性，得到 6.7 Å 结构。→ **遗留问题**：GI9 因此是"准对称+准等效(quasisymmetric)"混合体，同一界面出现 5 个准等效位置；两个 A:A 界面实测不同（1.3 Å 互差、对设计模型 2.0/2.4 Å），作者给的是提案式解释："We propose that the lowest-energy state of the A:A interface is not perfectly symmetric, but that the symmetry requirements for nanocage assembly force it to adopt a higher-energy, two-fold-symmetric configuration where appropriate"——本文未直接验证。
5. **高 T 数尺寸失控**。无控制机制时四组分混合应得分布而非单分散（"In the absence of other control mechanisms, the inclusion of BBB homotrimer in assembly reactions should yield distributions of large T number assemblies rather than monodisperse preparations of a single species"）。→ **应对**：用化学计量当旋钮——按 T=4,9,16,25,36,49,64,81,100 配比组装、DLS 跟踪（"the Z -average hydrodynamic diameter measured by dynamic light scattering (DLS) increased with increasing target T number (from 47.5 ± 0.4 nm to 188 ± 1.1 nm), though the observed hydrodynamic diameter deviated from the predicted diameter at higher T numbers"），并加 3% CHAPS 防预组装（"components were mixed at various stoichiometries depending on the target assembly state in the presence of 3% CHAPS, a condition that prevented premature assembly"，理由是"This was necessary to prevent the assembly of off-target species during addition of the multiple components required to generate the target assemblies"）+ 加料顺序控制。→ **偏差归因（作者自陈，未闭环）**："This deviation could be due to contaminating AAB trimer in the ABB fraction"；"Furthermore, smaller assemblies will be kinetically favoured over larger assemblies, which could bias the resulting particle distribution"。
6. **免疫学读出看不到抗原**："the displayed antigen could not be seen owing to its small size and flexible linkage to each nanocage"（负染 2D 分类图里）。→ **应对**：改用共价证据（SpyTag/SpyCatcher 偶联后 SDS-PAGE 分子量上移）+ 功能读出（RAMOS-BCR Ca²⁺ flux），并把"更强"作为结论："Activation by both RBD-bearing nanocages was more robust than by the anti-IgG control, peaking both faster and higher"。**代价**：未见抗原密度=柔性连接未被结构确证；体内免疫原性本文未测（作者只说 suggest potential utility）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **突变设计**：Rosetta 全单/双突变扫描（total score + ddG filter，界面接触定义=跨界面重原子 4 Å 内）；归一化升降双指标（式 1/式 2）；GREMLIN 共进化耦合矩阵做第二信息源。
- **组装读出**：E. coli 澄清裂解液直接与纯 I53-50B 五聚体三浓度混合，native PAGE 看笼带（"The lack of an I53-50 nanocage band on the native gel indicated single mutations that disrupted either trimer formation or trimer geometry such that the mutant trimer was no longer assembly-competent"——图注口径见 Methods）；天然质谱（Orbitrap 超质量范围，UniDec 解卷积）分辨 AAB/ABB/AAA；负染 EM、cryo-EM（300 kV，金标准 FSC 0.143）、DLS。
- **较大笼设计**：I3-01 界面复用 + pentasymmetron 刚体对接 C3 同源三聚体（沿用两组 2018/2022 对接脚本改写入参）；Rosetta FastDesign 造 B:C 新界面。
- **功能演示**：SpyTag/SpyCatcher 偶联 RBD，RAMOS 细胞 BCR Ca²⁺ flux。
- **没有用的方法**：MD、QM 全无；无深测/展示库（全程阵列蛋白生化）。

### 工作流程表

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | 1WA3 同源三聚体界面 | Rosetta 算全部单/双突变的 Δscore 与 ΔddG（对 WT 归一，式1/式2） | "the energetic effects of all possible single and pairwise mutations in 98 contacting residue pairs over 36 positions in the 1WA3 homotrimer interface were evaluated using Rosetta"；破坏候选=升超 100 REU；理想对=单升双不升（见第 2.2 节引句） | 96 个"升能"单突变；子集有补偿对 |
| W2 | 同界面 | GREMLIN 共进化：找与 WT 对负相关的低频单突变+高频补偿双突变 | 耦合矩阵（例 H91I / V118Y） | 第二突变源，与 Rosetta 通道互补 |
| W3 | 目视核查后的突变对 | 单突变入 I53-50A，裂解液+三浓度 I53-50B，native PAGE | 有无 120 亚基笼带 | "In total, mutations from 76 mutant pairs were selected for experimental screening"；实测 "only 3 out of the 82 single mutants tested did not yield a band" |
| W4 | 破坏×补偿组合 | 组合突变（三顺反子 ABC 及各双顺反子），同法组装 + IMAC/SEC/天然质谱 | 笼带恢复=功能对；质谱定 AAB/ABB | 仅三对成立："three pairs of functional disrupting and compensatory mutations were identified: H91I/V118Y, P90F/P147A and P114F/F131V"；ABC 失败、AAB/ABB 成立 |
| W5 | AAB/ABB 混合物 | 1:1 与 I53-50B 组装→SEC→负染 EM | 呈 I53-50 已知形貌=骨架对称保持（层级前提成立） | 确认可作积木 |
| W6 | I3-01（60 亚基设计笼） | 取五重轴周围 5 个三聚体，非配对亚基回突变+12 个负电突变，融成单链→pentasymmetron 按同五聚体处理；刚体对接 CCC 同源三聚体并设计 B:C 界面 | 对接构型人工筛查界面必须在未配对亚基上；暴露疏水设计残基回 WT | 240 亚基 T=4 模型（GI 命名：Goldberg-icosahedral-T-X） |
| W7 | 3 个 T=4 设计 | 三顺反子共表达，Ni2+ 共沉淀三链 | SDS-PAGE 三带齐=组装证据 | "We expressed three initial designs in E. coli as tricistronic genes with a 6×His tag on only the C chain, and found that Ni 2+ beads co-precipitated all three subunits of two of the designs, suggesting assembly"；"We proceeded with the better expressing and more soluble of the two"→GI 4 -F7 |
| W8 | GI4-F7 组分 | AB 双顺反子大表达→IMAC 梯度三峰（ABB/AAB/AAA）→Superdex200 去 I3-01-like→与纯 CCC 在 3% CHAPS 下过量混合，透析入 TBS 组装→S-500 SEC | 洗脱峰位置+负染/cryo-EM | "We mixed the AAB heterotrimer with an excess of the CCC homotrimer in the presence of detergent and initiated assembly by dialysing overnight into Tris-buffered saline" |
| W9 | GI4-F7 样品 | cryo-EM 单颗粒（300 kV）+对称扩展局部精修；与设计模型对齐 | 4.4 Å 全笼/3.1 Å asu；"The cryo-EM structure agrees well with the design model, with a Cα root mean-squared deviation (r.m.s.d.) of 9.3 Å across all 240 subunits and 3.0 Å within the asu" | "the diameter of GI 4 -F7 observed by cryo-EM is within 2% of the design model"；刚体偏差分解（五聚积木转 5.9°/移 5.8 Å，CCC 转 12.4°/移 4.0 Å；asu 内 1.4–2.1 Å） |
| W10 | 同一制备的意外颗粒 | 数六角孔→T=9→建 GI9 模型（12 pentasymmetron+30 disymmetron+60 CCC）；组分再抛光按 1:1:1 组装 | 6.7 Å 全笼/4.0 Å asu | "the GI 9 -F7 cryo-EM structure deviates from the design model by only 11.5 Å Cα r.m.s.d. across all 540 subunits, 1.6% of the nanocage diameter" |
| W11 | BBB+CCC+（AAB/ABB）四组分 | 按 T=4…100 化学计量配比、DLS 追踪；T=16 配比下 cryo-EM 验证 | Z-平均水合直径随 T 升 | "GI 16 -F7 is predicted to have a diameter of 96 nm and contains 12 pentasymmetrons, 120 CCC homotrimers, 60 disymmetrons and 20 BBB homotrimers for a total of 960 subunits"；"We determined a 14.9 Å resolution cryo-EM map of GI 16 -F7 and found that it closely matches the expected geometry of the design" |
| W12 | GI4/GI9 + SpyCatcher-CCC | RBD-SpyTag 偶联→SDS-PAGE/负染→RAMOS BCR Ca²⁺ flux（对照：单体 RBD、裸笼、抗 IgG） | 偶联=带移；功能=Ca²⁺ 曲线 | "We conjugated SpyTagged RBD to GI 4 -F7 and GI 9 -F7 nanocages bearing SpyCatcher 52 as a genetic fusion on the CCC subunit, yielding a theoretical maximum of 60 and 180 RBDs per nanocage, respectively"；"Activation by both RBD-bearing nanocages was more robust than by the anti-IgG control, peaking both faster and higher" |

**流程骨架**：层级分解（先积木后装配）+ 便宜正交读出（共组装上胶）+ 意外产物的机制化（污染→GI9）+ 化学计量当尺寸旋钮。打分器只在"造界面"时当闸口，在"破对称"时几乎只是排错器。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 240 / 540 / 960 亚基；49 / 71 / 96 nm | 三代笼子规模与直径 | "At 49, 71 and 96 nm diameter, these nanocages are the largest bounded computationally designed protein assemblies generated to date" |
| 120 亚基 | 旧法（严格对称）上限 | "The largest and most complex structures designed using this approach comprise 120 subunits and have strict icosahedral symmetry" |
| 98 接触对 / 36 位点 | Rosetta 突变扫描空间 | "the energetic effects of all possible single and pairwise mutations in 98 contacting residue pairs over 36 positions in the 1WA3 homotrimer interface were evaluated using Rosetta" |
| >100 REU；96 个 | 破坏突变能量阈值与数量 | "Ninety-six unique individual mutations increased the predicted homotrimerization energy (ddG) or" |
| 76 对 | 送测突变对 | "In total, mutations from 76 mutant pairs were selected for experimental screening" |
| 82 单测 → 3 破坏 | 对称破坏实测成功率 | "The 1WA3 trimer proved remarkably plastic: only 3 out of the 82 single mutants tested did not yield a band corresponding to the assembled I53-50 nanocage" |
| 3 对成立 | 破坏/补偿功能对 | "three pairs of functional disrupting and compensatory mutations were identified: H91I/V118Y, P90F/P147A and P114F/F131V" |
| 3 设计 → 2 共沉淀 → 1 | GI4 初筛 | "We expressed three initial designs in E. coli as tricistronic genes with a 6×His tag on only the C chain, and found that Ni 2+ beads co-precipitated all three subunits of two of the designs, suggesting assembly" |
| 4.4 Å / 3.1 Å / 9.3 Å / 3.0 Å / 2% | GI4-F7 结构精度 | "The cryo-EM structure agrees well with the design model, with a Cα root mean-squared deviation (r.m.s.d.) of 9.3 Å across all 240 subunits and 3.0 Å within the asu"；"the diameter of GI 4 -F7 observed by cryo-EM is within 2% of the design model" |
| 5.9°/5.8 Å/12.4°/4.0 Å/2.1 Å/1.4 Å | 刚体偏差分解 | "The main rigid-body deviation is a 5.9° clockwise rotation of the pentasymmetron, accompanied by a 5.8 Å translation away from the origin" |
| 6.7 Å / 4.0 Å / 11.5 Å / 1.6% | GI9-F7 结构精度 | "the GI 9 -F7 cryo-EM structure deviates from the design model by only 11.5 Å Cα r.m.s.d. across all 540 subunits, 1.6% of the nanocage diameter" |
| 1.3 / 2.0 / 2.4 Å | 两个 A:A 界面互差与对模型差 | "interfaces 4 and 5 appear to differ, with a Cα r.m.s.d. of 1.3 Å to each other and Cα r.m.s.d. values of 2.0 and 2.4 Å to the GI 9 -F7 design model, respectively" |
| 12+30+60 / 960 | GI9/GI16 组分计数 | "GI 16 -F7 is predicted to have a diameter of 96 nm and contains 12 pentasymmetrons, 120 CCC homotrimers, 60 disymmetrons and 20 BBB homotrimers for a total of 960 subunits" |
| 90 倍内腔体积 | GI16 对比旧严格对称笼/AAV | "This assembly has an internal volume that is roughly 90-fold larger than our previously designed nanocages with strict icosahedral symmetry" |
| 47.5±0.4 → 188±1.1 nm | DLS 随 T 数变化（T=4→100） | "the Z -average hydrodynamic diameter measured by dynamic light scattering (DLS) increased with increasing target T number (from 47.5 ± 0.4 nm to 188 ± 1.1 nm), though the observed hydrodynamic diameter deviated from the predicted diameter at higher T numbers" |
| 60 / 180 | RBD 理论最大展示数 | "We conjugated SpyTagged RBD to GI 4 -F7 and GI 9 -F7 nanocages bearing SpyCatcher 52 as a genetic fusion on the CCC subunit, yielding a theoretical maximum of 60 and 180 RBDs per nanocage, respectively" |
| 3 链 vs 4 链；3 链 vs 7 链 | 双组分积木的"编码经济性" | "The T = 4 structure requires only 3 distinct chains, compared with 4 chains for the more conceptually straightforward approach of a strictly pseudosymmetric ABC heterotrimer and DDD homotrimer"；"only 3 unique chains are required to make T = 9 nanocages, but 7 would be needed for the strictly pseudosymmetric approach" |
| 4 Å 内重原子 | 界面接触定义 | "Contacts were defined as any residue with a heavy (that is, non-hydrogen) atom within 4 Å of a heavy atom in a residue across the interface" |
| 15 个负电突变/单链化 | pentasymmetron 处理 | "We reverted the interface residues on the unpaired subunit back to the original 1WA3 sequence, mutated 12 residues to negatively charged amino acids to enhance expression and facilitate purification"（注：12 个，见引句；此行为口径核对） |

## 5. 结论——作者说了什么

1. 准对称积木（序列破对称、骨架保对称）+ 层级设计可以造出远超旧上限的有界组装体（240/540/960 亚基，96 nm），且几何精度到"直径偏差 2%"级。
2. 成功关键不是打分而是**读出**：用"已有更大组装体的组分"这一特性把组装/几何破坏变成一条 native PAGE 带（genotype→phenotype 高效筛选）；起点 1WA3 的超稳定性是双刃剑（表达好但破对称难）。
3. 双组分杂三聚体（AAB/ABB）带来"编码经济性"（T=9 只要 3 条链），代价是精度低于同期配套论文（accompanying Article）的严格准对称路线，且引入 quasisymmetry（同一界面多个准等效环境）。
4. 高 T 数无新界面需求（"Thus, obtaining GI 16 -F7 and the larger nanocages in the series does not require new interface design, only production of BBB homotrimer"），尺寸靠化学计量调，但仍分不开（DLS 偏差+动力学偏好小笼）。
5. 抗原装示 RBD 能有效激活 BCR（超过抗 IgG 阳性对照），提示疫苗支架潜力；作者寄望结构预测与设计成功率提升后泛化到任意寡聚体。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **判据必须与目标同向**。这里的目标是"让某个界面不成/对称被破坏"，而 Rosetta ddG/总分是按"造出稳定界面"校准的正向打分器——用它做负向选择，结果 82 测 3 中，判据与目标几乎正交。教训直接对表我们：用"结合/折叠稳定"类判据去筛"要有催化活性、还要避开副反应"的目标酶，就是同型错误——正向判据饱和≠负向目标达成。
2. **"超稳积木"的韧性把设计窗口压窄**：他们选 1WA3 是为了表达成功率和复用已有读出，但同一属性使破坏性突变失效。工程取舍里"让 A 变容易的性质恰好让 B 变难"，选起点时必须写下这笔债。
3. **便宜的端到端读出比打分器更值钱**：native PAGE 一条带就替代了不可靠的打分。我们等价物是"产物化学 LC-MS 一条峰"——但它贵且慢，所以更要区分哪些环节可以用便宜读出（表达量、可溶性、失活对照）替代贵判据。
4. **失败/污染要机制化而非丢弃**：AAB 里的 ABB 污染"错出"了 GI9；AAA 峰、I3-01-like 峰都在纯化流程里被显式命名并加以利用/剔除。漏斗每一环给"意外"留归因通道（组分/条件），才可能把事故变成新设计。
5. **精度声明要用相对量纲**："1.6% of the nanocage diameter"比 11.5 Å 更可迁移到不同尺寸的宣称——我们的活性位点判据也应给"相对于该体系自然波动尺度"的口径，而非裸 Å 数。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：实验筛选目前绑定"已知寡聚体+已有组装读出"（"Although at present this approach may limit the use of our experimental screen to a subset of known protein oligomers"）；对称破坏突变成功率低归因于 1WA3 韧性；SEC 无法分开 AAB/ABB（"This step removed the I3-01-like assemblies but did not resolve the ABB and AAB trimers."），BBB 制备受 AAB 污染影响高 T 数均一性（"This deviation could be due to contaminating AAB trimer in the ABB fraction"）；GI9 的 A:A 界面差异只给了提案（"We propose that…"），未实验闭环；抗原在负染图中不可见；B 细胞激活只是体外 Ca²⁺ 读出，无体内免疫数据。
- 我们读出：① 全程没有预测性打分器层面的改进——这篇的"计算"是 Rosetta 扫描+对接复用，它对"下一次能否算准"没有贡献，只贡献了"怎样便宜地验证"；② 240→540 的发现路径是偶发（污染颗粒），不可作为"该方法能按 T 数定制生产"的强证据；③ 100 REU、±0 归一分数这套阈值是排错用的粗筛，实际淘汰都发生在湿实验端——引用时不能把它说成有效闸口。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **正向/负向目标分列判据**：酶设计项目同时含正向判据（结合/折叠/辅因子装载）与负向判据（排除竞争副反应路径、排除错误环化）。本文示范了"拿正向校准的打分器做负向筛选"的失效形态——我们每个负向闸口必须自带独立证据（同位素/产物碎片比、失活对照），不得复用 ddG/pLDDT 类正向分数取反。
2. **"积木复用+一次新界面"的层级降维**：把大目标拆成"已验证组件 + 仅一个新增接口"，新增风险面最小。对我们的多步催化设计：优先复用已有功能模块（已确证结合 UTP/腺苷的元件），每轮只新造一个化学事件相关界面/口袋改动，失败归因才可判。
3. **起点性质债登记**：选高稳支架（利于表达/纯化）时同步记录它可能钝化" destabilizing/重塑型"筛选方向，并在预算里预留更大突变扫描量（本文 82 测 3 中就是量级参照——只作成本量级参照，不得当酶设计概率）。
4. **意外的组分归因通道**：纯化峰全部命名（ABB/AAB/AAA/I3-01-like），混合读出（native PAGE+天然质谱+DLS）分层。我们的 LC-MS 图谱亦应保留"非目标峰"台账（起始物、环化副产物、错误连接物），它是失败模式的原料而不是废数据。

**不可迁移（为什么不能照搬）**

1. **读出不等价**："能否共组装成已知笼"是二值、批量、非定量的便宜判据；酶活是 turnovers + 产物比 + 竞争路径的连续量，无同等便宜的"一条带"判据。不得把本文的筛法类比为"给酶设计找一个 native PAGE 式判据"就完事。
2. **数字禁搬**：100 REU、3/82、2%、1.6%、540 亚基、IC 曲线等全部属于纳米笼体系；与催化成功概率无关（本库判据亦禁止 binder/组装体阈值转作酶活判据）。
3. **无酶、无活性位点化学**：本文不含活性位点设计、金属/辅因子化学、MD/QM——不能为"物理法判催化"提供任何证据。
4. **cryo-EM 确证路径不可用**：96 nm 均一颗粒适合单颗粒，我们对目标酶-底物瞬态/低丰度产物无法用同级结构确证。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/nanocage_hier2025.txt

- 本地全文：`data/interim/baker_lit/ft/nanocage_hier2025.txt`（Europe PMC 通路，2026-10-16 抓取，batches.tsv 第 8 批登记 B25 唯一全文；另有登记底稿 `sources/baker.md:329–340`）。
- 汇总引用：`sources/baker.md:550`（负向筛选新判据形态）、`sources/baker.md:612`（确证行：直径偏差 <2%、Cα 11.5 Å/540 亚基）、`sources/baker.md:648`（准对称笼条目）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：写卡前用与门禁同一的 `litcards_text.norm` 预校验全部候选引句（四处首字母大小写不一致致 MISS，已按原文改回 We/The；一处 pentasymmetron 单引号缺失致 MISS，已补）。引句分布：Abstract/引言 6 处、Results 叙述段为主、Methods 5 处、Extended Data 图注 1 处（「The lack of an I53-50 nanocage band…」句在 Methods 段内，卡中以全句逐字引用）。台账第 4 节「12 residues」行已按原文数值标注核对（原文为 mutated 12 residues，本卡正文口径一致）。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 1 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（结构/材料设计）
target=准对称 I53-50 型杂多聚体纳米笼：GI4-F7（240 亚基/49 nm）、GI9-F7（540 亚基/71 nm）、GI16-F7（960 亚基/96 nm）；支链=RBD 抗原展示与 BCR 激活
backbone_generation=Rosetta 界面突变全扫描（单+双突变，Δscore/ΔddG 对 WT 归一）+ GREMLIN 共进化选对；pentasymmetron 刚体对接 CCC 同聚体后 Rosetta 设计 B:C 新界面；ProteinMPNN 未用于本篇主流程（底稿所载 ProteinMPNN 为组内其他线）
computational_filters=ddG/Rosetta 总分相对野生型归一化升降（式1/式2）；>100 REU 升能=破坏候选；理想对=单突变升能>0 且双突变≤0；界面接触=重原子 4 Å；对接构型人工筛查+暴露疏水残基回 WT
thresholds=单突变升能>100 Rosetta 能量单位；理想突变对=归一分数>0（单）且≤0（双）；组装正确性=与五聚体共组装后 native PAGE 笼带；结构验收=直径偏差 2%、Cα 9.3 Å@240 亚基/11.5 Å@540 亚基（1.6% 直径）
md_used=否
qm_used=否
experimental_methods=E. coli 裂解液共组装+native PAGE 筛选；三顺反子/双顺反子表达；IMAC（梯度三峰）/StrepTrap/SEC 纯化；天然质谱（Orbitrap+UniDec）；负染 EM；cryo-EM 单颗粒（4.4/3.1、6.7/4.0、14.9 Å）；DLS 化学计量曲线；SpyTag/SpyCatcher RBD 偶联；RAMOS BCR Ca2+ flux
pipeline_counts=98 接触对/36 位点全扫描→96 升能单突变→76 突变对送测→82 单突变实测（仅 3 破坏）→3 对功能突变→ABC 失败→AAB/ABB 成立；GI4 三设计→2 共沉淀→1 推进；GI16 组分=12+120+60+20 三聚体=960 亚基
hit_rate=对称破坏突变命中率 3/82（且为"筛选意义上"的破坏读出）；三设计 2 装（GI4 初筛）；高 T 数尺寸不可单分散（DLS 偏差未消除）
best_metric=cryo-EM 对设计模型：直径偏差 2%（GI4-F7）；11.5 Å Cα r.m.s.d./1.6% 直径（GI9-F7，540 亚基）；RBD 笼 BCR 激活峰值超过抗 IgG 阳性对照（无 Kd/活性类定量）
cost_or_stat_note=全程阵列生化无展示库；分辨率 4.4–14.9 Å；无 MD/QM 机时；主要成本=突变对湿测（76 对）与三代替 cryo-EM 数据收集（正文未记单价）
role_in_timeline=展示漏斗的"负向判据失效"形态：物理打分器按造界面校准，对破坏对称几乎无判别力，作者以便宜端到端读出（共组装上胶）替代；同时把多组分不对称组装的验收标准推到"该成的界面成、不该成的界面也要可控"，为后续四组分笼（B41）与同期配套论文的严格准对称路线铺路
source_pointer=data/interim/baker_lit/ft/nanocage_hier2025.txt（全文）+ sources/baker.md:329-340（底稿）；PDB/EMDB 入库号在正文未列出（仅正文提及 deposited via PDB，本卡未核）
CSV回填-->
