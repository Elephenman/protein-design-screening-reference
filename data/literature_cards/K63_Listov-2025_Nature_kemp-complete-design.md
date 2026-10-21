# [K63] 完全计算设计的高效 Kemp 消除酶——"算完直接中"案例的判据、漏斗与验证细节

Listov D, Vos E, Hoffka G, Hoch SY, Berg A, Hamer-Rogotner S, Dym O, Kamerlin SCL, Fleishman SJ（Weizmann 研究所; Georgia Tech; Lund; Debrecen; Uppsala）
Nature 2025, 643:1421-1427 · DOI 10.1038/s41586-025-09136-2 · PMID 40533551 · PMCID PMC12310539
（注：作者列表无 Baker，has_baker=False，不得算作 Baker 组工作；见 sources/baker.md:592）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K63**（组：通用方法学；batches.tsv 第 85 行，state=FULLTEXT） |
| 本文取回方式 | Europe PMC `fullTextXML`（PMC12310539，2026-10-16 抓取；inventory.json 登记 fetch_channel=epmc_fulltext） |
| 本地全文底稿 | `data/interim/baker_lit/ft/kemp2025.txt`（96,423 B，剥标签纯文本，含参考文献编号残留） |
| 对照底稿 | `sources/baker.md:592`（题录 + Crossref 作者核验：9 人、**has_baker=False，不得算作 Baker 组工作**；本地全文 MD 命中 28 句、QM 命中 29 句） |
| 证据级别 | **全文级**（本卡所有英文引句均可在 `data/interim/baker_lit/ft/kemp2025.txt` 里逐字命中；见第 9 节门禁结果） |
| 未取到的部分 | Extended Data 图/表、Supplementary Tables 1–7、Nature Reporting Summary、正文图（Fig 1–4）原图数值；**该文在 Europe PMC 前置元数据里标有 modified publication（出版后被修订/更正），但更正正文不在本地底稿里，本卡不引用任何更正内容** |

## 1. 这篇到底解决什么（一句话）

"算完直接中"的标杆案例：以前从头设计的酶比天然酶慢几个数量级、必须靠反复定向进化补救；这篇用一串成熟的原子级计算工具（模块装配件骨架 + PROSS 稳定化 + theozyme 几何嫁接 + Rosetta 活性位点设计与模糊逻辑过滤 + 预组织校验 + FuncLib 局部优化），针对 Kemp 消除这个无天然酶对应的模型反应，把最优变体推到 kcat 30 s⁻¹、kcat/KM 1.23×10⁵ M⁻¹s⁻¹——作者声称达到了天然酶中位水平（10 s⁻¹ / 10⁵ M⁻¹s⁻¹），且全程不用大库筛选、不用定向进化。注意：其"完全计算"是低通量实验反馈（累计上百个构建体逐个测）意义上的，不是零实验。

## 2. 遇到的难点（作者自述），以及遇到问题时他们做了什么

1. **从头设计的活性一直差几个数量级，而且失败原因是结构层面失真的**。作者列举既有病灶："the designed active sites exhibited significant structural distortions relative to the design conception"，且 "shifts of the catalytic constellation by a few degrees or tenths of an Ångstrom from optimality may translate into orders of magnitude decreases in efficiency"；旧方法还被迫依赖进化："Such cycles are inefficient and are restricted to reactions that can be assayed in medium-to-high-throughput fashion"。 **应对**：提出总假设 "Our working hypothesis is that effective enzyme design demands control over all protein degrees of freedom to establish stability, foldability and accurate positioning of the theozyme"，落地为四件事——放弃理想化 de novo 折叠改用天然 TIM-barrel（"we focused on the TIM-barrel fold, which is one of the most prevalent protein folds found among enzymes"）、全蛋白稳定化（"Unlike previous approaches, this workflow emphasizes stability across the entire protein."）、几何匹配 + 约束设计、以及下单前的预组织校验。 **代价**：他们承认理想折叠缺功能所需的非理想元件——"generating backbones that are dominated by ideal secondary structure elements that lack the non-ideal elements that may lower foldability but are nonetheless needed for sophisticated functions"，这是换天然折架的隐含理由，也是对 fold-design 路线的让步。
2. **漏斗里的能量目标是互相冲突的，单一阈值没法同时保稳定与保活性**。原文："This approach balances potentially conflicting objectives that are critical for design of function, such as low system energy and high desolvation of the catalytic base." **应对**：用模糊逻辑多目标函数（"The workflow results in millions of designs which are filtered using a ‘fuzzy-logic’ optimization objective function"）替代硬阈值，六个目标并列排序（见第 3 节 S4），排序后只取"few dozen"进下一步。 **代价**：多目标排序不给出物理上可解释的截断，第 7 节会看到真正的高活性跃迁并不来自这个排序器。
3. **底物溶解度封顶，米氏饱和做不到**。图注原句："When substrate saturation could not be attained due to limited substrate solubility, the data were fitted to the linear region of the Michaelis-Menten model"。 **应对**：低浓度区按斜率取 kcat/KM（正文 "Kinetic parameters were obtained by fitting the data to the Michaelis-Menten equation"），高功能设计重复 2–5 次生物学重复。 **代价**：多数设计的 KM 与 kcat 不能分别解出，"效率"与"速率"的拆分依赖少数饱和可及的设计。
4. **第一轮设计的绝对水平仍然不够看**：初测 3 个活性设计（"Three designs showed measurable KE activity in an initial screen"）与其前设计同档——"falling short by several orders of magnitude from comparable natural eliminases and from designed Kemp eliminases that were optimized through laboratory-evolution campaigns"。 **应对**：对已验证有活性的亲本做去同源化的 FuncLib 优化——"To optimize these designs computationally, we applied FuncLib to active-site positions, excluding the theozyme residues."，并进一步 "we removed all homology-based restrictions in the active site, thus using atomistic energy as the sole optimization objective function"，18 个变体送测后 Des27 系提升 10–70 倍。 **代价**：这一步的输入是**实验挑出的活性亲本**（Fig 1 图注明写流程顺序："Following experimental screening (step 5), we apply FuncLib" "to the active sites of select functional designs (step 6)"），所以"完全计算"叙事在此处有明确的实验咬合点。
5. **自己用了二十年的催化几何假设被自己的结果推翻**。他们按文献惯例强制 theozyme 含一个芳香堆叠残基："We note that the aromatic theozyme residue was forced in all our design steps and was based on previous Kemp eliminase design studies"；但 Phe113Leu 单点突变把 kcat/KM 与 kcat 再抬一个数量级。 **应对**：补做结合态/游离态模型比对，给出机理解释——"suggesting that this mutation improves active-site preorganization"，并公开承认假设错了——"This finding challenges a two-decade assumption in computational Kemp eliminase design that an aromatic residue is important for ligand binding"。 **代价**：这一步是**实验先于计算**的发现（计算只负责事后的能量等价与几何解释），说明该漏斗的排序器当时**预测不了最大的一步提升**；本文未解决（作者把它归为未来 theozyme 建模改进："Future improvements in modelling theozymes may enable fully programmable biocatalysis"）。
6. **晶体结构里总有一段环对不上设计**。Des27.7 主链大部分与设计一致，但 "but 65 amino acids either deviated or did not exhibit significant electron density, probably due to backbone flexibility in this region"；第二轮 R2 系两个结构同样有环缺密度或构象大变。 **应对**：对 R2.Des39.2 专门用 FuncLib 稳定这些区域（16 个变体，3 个命中，最高提升 20 倍至 2,000 M⁻¹s⁻¹），并解释该片段"在 IGPS 家族本来就动态"。 **代价**：没有任何 loop 变体超过 Des27.7，柔性片段问题在本文内没有一般性解法。
7. **单条 EVB 轨迹出现活性位坍塌**。"in one of the initial 30 EVB trajectories for Des27.7 with the substrate in the out conformation, we observed active-site distortion with the catalytic Asp moving into a non-reactive conformation"。 **应对**："This trajectory was excluded from further analysis, with an extra trajectory being run to create a full set of 30 replicas." **代价**：剔除判据是作者人工观察，属可讨论但已声明的处理。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **骨架构建**：Rosetta 模块化装配（modular assembly，5 条 IGPS 链切 5 段 all-vs-all 重组）+ PROSS（含 PSSM 约束的稳定性设计；第二轮起还叠加全蛋白突变扫描最优突变组合）+ 一个内部"活性预测器"排序。
- **位点构建**：theozyme 几何来自此前量子化学计算（亲本质子的碱 Glu/Asp + 一个与底物 π-堆积的残基）；本文显式**去掉**了传统 theozyme 中与异噁唑氧形成极性相互作用的第三位点（理由是水分子可满足、错放的极性基会压低催化碱 pKa）。Rosetta Matcher 几何放置 + 配体/催化残基周围 8 Å 壳层序列设计（theozyme + PSSM 约束；IGPS 天然催化残基做突变扫描，ΔΔG_system < +1 R.e.u. 的突变才进允许集）。
- **过滤/排序**：模糊逻辑多目标函数（能量密度、同骨架内能量排名、活性位 vdW、催化碱 vdW、配体溶剂化、theozyme 几何精度）；活性位低能突变枚举（ΔΔG_system < +3 R.e.u.）；pSUFER 全蛋白扫描 + FuncLib 重设计被标记位点。
- **计算校验（下单前）**：无配体刚体最小化后催化碱 r.m.s.d. > 1.2 Å 者丢弃；第二轮系列加 AF2 预测模型 vs Rosetta 模型 r.m.s.d. < 1 Å 接受。
- **实验后优化**：对活性亲本做"去同源化 FuncLib"（丢掉同源序列过滤，只剩原子能 + 稳定化过滤），每轮选 10–15 条最低能送测。
- **机理侧（事后，不参与入选）**：Amber24 经典 MD（ff19SB/OPC，每体系 5×1 µs，共 15 µs）+ EVB 反应自由能（Q6/OPLS-AA/SCAAS，30 副本×10.2 ns，每体系累计 612 ns；底物 RESP 电荷在 HF/6-31G(d)、几何 B3LYP/6-31G(d) 优化）。
- **实验**：E. coli 表达（bdSUMO 融合）、Ni-NTA、nanoDSF 表观 Tm（20–95 °C）、96 孔板 380 nm 吸光动力学、Michaelis-Menten（底物不溶时用线性区）、X 射线晶体学（3 个结构：9HVB/9HVH/9HVG，1.9–2.1 Å）。

### A. 第一轮主漏斗（模块装配系列，Fig 1b 步骤 1–6）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | 5 条 IGPS 结构（1LBF/1I4A/1JCM/1VC4/4FB7） | 按最大结构保守点切 5 段，all-vs-all 组合 + Rosetta 序列设计优化片段兼容 | 分割点位于 44/105/154/206（以 1I4N 计）；原文未给组合级阈值 | "resulting in 2,500 backbones" |
| S2 | 2,500 条骨架 | PROSS 稳定化（PSSM 约束）；designs 37–73 另加全蛋白突变扫描稳定协议 | PSSM 由每条结构经 PROSS 生成；原文未给通过阈值（排序） | 进入活性预测器的骨架池（正文口径 thousands of backbones） |
| S3 | 稳定化骨架 | 内部活性预测器排序取头部 | "and the top 1,000 designs were chosen" | 1,000 条骨架进入位点构建 |
| S4 | 1,000 条骨架 × KE theozyme | Rosetta Matcher 几何放置 + 8 Å 壳层序列设计（theozyme/PSSM 约束） | "After matching, Rosetta sequence design was performed in an 8 Å shell around the ligand and catalytic residues."；催化残基突变扫描只纳入 ΔΔG_system < +1 R.e.u. | "The Rosetta Match and design steps generated 10 5 to 10 6 designs for each starting structure"（10⁵–10⁶/条，总量百万级） |
| S5 | 百万级设计 | 模糊逻辑多目标过滤 + 活性位枚举（ΔΔG_system < +3 R.e.u.）+ pSUFER/FuncLib 全蛋白再优化 | "energy density (system energy divided by the protein length), energy rank relative to other designs in the same backbone, active-site vdW energy, catalytic base vdW, ligand solvation and accuracy of theozyme geometry" | "A few dozen top designs are chosen for further core (green spheres) and active-site stabilization (step 4)"（数十条） |
| S6 | 数十条 | 无配体刚体最小化预组织校验 | "Structures in which the catalytic base exhibited an r.m.s.d. > 1.2 Å relative to the ligand-unbound model were discarded." | 73 条送实验："We selected 73 designs for experimental testing." |
| S7 | 73 条基因（Twist 合成） | 表达 + nanoDSF + 380 nm 初筛 + 动力学 | 可溶表达；协同热变性；可测 KE 活性 | "In total, 66 designs were solubly expressed and 14 showed cooperative thermal denaturation"；"Three designs showed measurable KE activity in an initial screen"（Des27=210、Des61=130 M⁻¹s⁻¹） |
| S8 | Des27 / Des61 活性亲本 | 去同源化 FuncLib 优化活性位（不动 theozyme），按能量取低值送测 | "We selected 6 and 12 low-energy designs for experimental testing for Des61 and Des27, respectively, each comprising 5-8 specific mutations relative to their origin" | "eight designs on the basis of Des27 showed increased catalytic rates by 10-70-fold"；Des27.7 达 kcat/KM 12,700 M⁻¹s⁻¹、kcat 2.85 s⁻¹，"a rate that is an order of magnitude greater than that of any previously reported computational design" |
| S9 | Des27.7 | 晶体结构验证 + 机理分析（MD/EVB）+ 按 Rosetta 能量等价换 Phe113 为 Met/Leu 单点验证 | 活性位设计-结构一致性；Asp162 vdW 能与效率相关 | "All active-site positions aligned well with the design conception"（<0.7 Å/20 残基）；"MD simulations show that Asp162 is conformationally dynamic in the ligand-unbound models, sampling multiple metastable conformations"；Phe113Leu：kcat/KM 123,000 M⁻¹s⁻¹、kcat 30 s⁻¹ |

### B. 第二轮对照漏斗（不用模块装配，验证流程可迁移性）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| R1 | T. maritima IGPS 序列（1I4N） | BLAST 非冗余库 → CD-HIT 聚类 → ColabFold AF2 建模 → PROSS（pLDDT 低区禁用）→ 每条 8 个设计 | "by 30-90% sequence identity to one another and 1,200 were selected for further analysis"；"Models with average local confidence in predicted structures (predicted local distance difference test (pLDDT)) scores below 90 were discarded, leaving 1,072 backbones." | 4,381 → 1,200 → 1,072 条骨架 |
| R2 | 1,072 骨架 | 重复 S4–S6 + 额外 AF2-vs-Rosetta 一致性校验 | "Designs were accepted if the r.m.s.d. between the AlphaFold2 model and the Rosetta model was less than 1 Å." | 55 条送测（"we applied the subsequent steps of the workflow to 1,072 representative IGPSs that were modelled using AlphaFold2"） |
| R3 | 55 条 | 表达/变性/活性 | 同上 | 49 可溶（89%）、28 协同折叠（50%）、"In total, 70% of the cooperatively folded designs (20 designs) showed measurable KE activity"（kcat/KM 0.5–155 M⁻¹s⁻¹）；R2 两轮 FuncLib（6 个亲本×9–14 变体、loop 稳定 16 变体）后最高仅 300→2,000 M⁻¹s⁻¹，无一超过 Des27.7 |

### C. 组件消融（"必要且充分"实验，Fig 4）

| 输入 | 操作 | 判据/观测 | 输出 |
|---|---|---|---|
| 模块装配基线（92 突变，无 PROSS 无位点设计） | 表达 + Tm + 活性 | "This variant exhibited an apparent melting temperature of 57 °C and no detectable KE activity." | 仅装配 = 稳定但无功能 |
| +11 条 PROSS 突变 | 同上 | "Adding the 11 PROSS-designed mutations substantially improved both bacterial expression and thermal stability"（69 °C） | 稳定化模块单独贡献 |
| +Des27.7 活性位 15 突变（无 PROSS） | 同上 | "grafting the active site from Des27.7 (15 mutations) onto the combinatorial assembly starting point (without PROSS stabilizing mutations) conferred high activity levels"（2,900 M⁻¹s⁻¹） | 活性位模块单独贡献 |
| Des27.7 全组件 / D162A | 同上 | "resulting designs did not exhibit the trade-offs between stability and activity that were often reported in laboratory-evolution campaigns"；"Mutating the catalytic base Asp162 to Ala completely abolished activity, verifying that the designed base is essential."，且 "this single-point mutation also markedly increased protein stability, with the apparent melting temperature rising from 85 °C in Des27.7 to above boiling point" | 组件间正协同；电荷埋藏是稳定性的主要负担 |

**流程骨架一句话**：骨架多样性（装配/AF2 天然家族）→ 全蛋白稳定化 → 几何+能量多目标排序 → 预组织校验 → 小批量实验（73+55）→ 只对实验命中者做能量制导局部优化（FuncLib）→ 结构/动力学事后解释。MD 与 QM/EVB 全部在**下单之后**，不参与候选削减。

## 4. 关键数字台账

| 数值 | 含义 | 出处（原句/原字段） |
|---|---|---|
| 1–420 M⁻¹s⁻¹ / 0.006–0.7 s⁻¹ | 此前计算设计 Kemp 消除酶的 kcat/KM 与 kcat 历史区间 | Fig.1 前正文（"computationally designed Kemp eliminases exhibited low catalytic efficiencies and rates"） |
| 10⁵ M⁻¹s⁻¹ / 10 s⁻¹ | 天然酶催化效率/速率中位数（本文对标基准，引 ref. 16） | "median values of enzymes in nature" |
| 2,500 → 1,000 | 模块装配产生的骨架数 → 活性预测器保留数 | "resulting in 2,500 backbones" / "and the top 1,000 designs were chosen" |
| 10⁵–10⁶ /条骨架 | Matcher+设计产生的候选数 | "generated 10 5 to 10 6 designs for each starting structure" |
| 数十 → 73 | 模糊逻辑过滤后规模 → 最终送测数 | "We selected 73 designs for experimental testing." |
| 245–268 aa；30–93%；41–59% | 送测设计链长与序列多样性（彼此间/对天然蛋白） | "The designs ranged from 245 to 268 amino acids and were diverse, with 30-93% sequence identity to one another and 41-59% identity to any natural protein." |
| 66 → 14 → 3 | 可溶表达 → 协同热变性 → 初筛有活性（第一轮 73 条内） | "In total, 66 designs were solubly expressed and 14 showed cooperative thermal denaturation" / "Three designs showed measurable KE activity in an initial screen" |
| 130 / 210 M⁻¹s⁻¹；kcat < 1 s⁻¹ | 初筛最好的 Des61 / Des27 | 正文 Round-1 段 |
| 6 + 12 变体（5–8 突变） | FuncLib 去同源化优化送测数（Des61/Des27） | "We selected 6 and 12 low-energy designs for experimental testing for Des61 and Des27, respectively, each comprising 5-8 specific mutations relative to their origin" |
| 10–70 倍；8 个 | Des27 系 FuncLib 变体的速率提升幅度与命中数 | "eight designs on the basis of Des27 showed increased catalytic rates by 10-70-fold" |
| 3,600 M⁻¹s⁻¹ / 0.85 s⁻¹ | Des61 系最好变体 | "One design derived from Des61 showed catalytic efficiency of 3,600 M -1 s -1 and k cat of 0.85 s -1" |
| 12,700 M⁻¹s⁻¹ / 2.85 s⁻¹；141 突变 | Des27.7（比此前任何计算设计高一个数量级；与最近天然蛋白的差异） | "a rate that is an order of magnitude greater than that of any previously reported computational design"；"a pairwise sequence alignment to the closest protein in the non-redundant sequence database reveals 141 mutations and multiple insertions and deletions" |
| 123,000 M⁻¹s⁻¹ / 30 s⁻¹ | Des27.7 Phe113Leu 单点变体（全文最高，比 AI 生成蛋白设计高两个数量级：0.03–0.7 s⁻¹） | 正文 Phe113 段 |
| ΔΔG_system < +1 R.e.u.；< +3 R.e.u.；r.m.s.d. > 1.2 Å 弃；AF2-vs-Rosetta < 1 Å；pLDDT ≥ 90；10–15 条/轮 | 各计算判据阈值（突变扫描允许集 / 活性位枚举 / 预组织校验 / R2 一致性校验 / R2 骨架保留 / FuncLib 送测上限） | Methods（Initial active-site design / Active-site and core stabilization / Computational validation / Backbone generation / Active-site optimization） |
| 4,381 → 1,200 → 1,072 → 55 → 49 → 28 → 20 | 第二轮：同源→聚类→AF2 合格→送测→可溶→协同折叠→有活性 | "identifying 4,381 IGPS homologues"；"by 30-90% sequence identity to one another and 1,200 were selected for further analysis"；"leaving 1,072 backbones"；R2 段各百分比 |
| 0.5–155 M⁻¹s⁻¹ → 300 → 2,000；Tm 47–88 °C | R2 活性区间 → FuncLib 后最高 → loop 稳定后最高（无一超 Des27.7） | "In total, 70% of the cooperatively folded designs (20 designs) showed measurable KE activity with k cat / K M in the range of 0.5-155 M -1 s -1"；"reaching k cat / K M 2,000 M -1 s -1" |
| 57 °C（92 突变）→ 69 °C（+11 PROSS）→ 2,900 M⁻¹s⁻¹（+15 活性位突变）→ >85 °C / 12,700（全组件）；D162A 活性清零、Tm 超沸 | 组件消融链 | Fig 4 段（"grafting the active site from Des27.7 (15 mutations) onto the combinatorial assembly starting point (without PROSS stabilizing mutations) conferred high activity levels"；"with the apparent melting temperature rising from 85 °C in Des27.7 to above boiling point"） |
| <0.7 Å（20 残基）/ Phe113 0.78 Å / 180 of 257 < 0.6 Å / 65 残基偏离或缺密度 | Des27.7 晶体 vs 设计一致性（9HVB，2.0 Å；另两结构 9HVH 2.1 Å、9HVG 1.9 Å） | "All active-site positions aligned well with the design conception (less than 0.7 Å all-atom root mean squared deviation (r.m.s.d.) across 20 residues)" |
| ρ = −0.88（P = 6×10⁻⁵）；5×；717→829 Å³ | Asp162 vdW 能与效率的 Spearman 相关；Des27.7 底物驻留为 Des27 的 5 倍；口袋体积 | "the Rosetta-computed van der Waals (vdW) energy of Asp162 is highly correlated with catalytic efficiency among the FuncLib designs"；"with Des27.7 showing five times more substrate retention"；"increasing the volume of the pocket from 717 to 829 Å" |
| P = 7.7×10⁻⁹ vs P = 0.088 | Des27.7 的 in/out 两种底物构象活化能差显著、Des27 不显著（Wilcoxon） | Fig 3e 图注 |
| 15 µs（5×1 µs×3 体系）；612 ns/体系（30×10.2 ns）；总计 4.8 µs | 经典 MD 与 EVB 模拟量（全为事后机理） | "resulting in a total of 5 µs of simulation time per system and 15 µs across all systems"；"leading to a cumulative 612 ns of EVB simulation time per system" |
| 4 Å；380 nm；0.05–0.75 mM | MD 结合判定阈值；检测波长；动力学底物浓度区间 | Methods（Simulation analysis / Activity assay） |

## 5. 结论——作者说了什么

1. 全流程计算管线得到实验背书："Taken together, our results verify a fully computational pipeline that designs an accurate de novo active site and generates a stable and high-efficiency new-to-nature enzyme"。
2. 能力宣言（作者原话口径）："the ability to design large sets of diverse backbones and encode high protein stability and active-site preorganization is necessary and sufficient for generating high-efficiency enzymes of model reactions"，且 "the results confirm that current atomistic methods are already sufficiently reliable to generate efficient enzymes in natural folds without extensive experimental screening, big-data analyses or artificial intelligence-generated scaffolds"。
3. 最优变体的量级："The best variant showed high stability and remarkable catalytic efficiency for a fully designed enzyme"（>85 °C、12,700 M⁻¹s⁻¹），单点设计突变后再升至 123,000 M⁻¹s⁻¹，kcat 30 s⁻¹ 与天然酶中位值"on par"（作者自己对标 10⁵ M⁻¹s⁻¹ / 10 s⁻¹）。
4. 机理解释：优势来自活性位预组织与多种可反应结合模式并存——"Active-site preorganization combined with the ability to adopt multiple catalytically competent substrate-bound modes distinguishes this design from previously generated ones."
5. 附带科学发现：芳香堆叠不是必需（Phe113Leu 反而更快），"This finding challenges a two-decade assumption in computational Kemp eliminase design that an aromatic residue is important for ligand binding"；D162A 灭活但显著增稳，说明埋藏电荷是稳定性负担。
6. 组件消融结论：模块装配 + PROSS + 活性位设计三者缺一不可且正协同，"resulting designs did not exhibit the trade-offs between stability and activity that were often reported in laboratory-evolution campaigns"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **"完全计算设计"的实际定义是"无大库、无定向进化"**，不是无实验反馈：73+55 条初测、18 条 Des 系 FuncLib、R2 系 ~70+16 条变体，累计约 230 个构建体做了表达/熔解/活性三件套。真正的突破（Des27.7 与 Phe113Leu）都长在"先实验挑出亲本/先实验测出跃迁"的枝干上。引用这篇时只能说"实验反馈轮次少"，不能说"预测命中"。
2. **漏斗排序器与最终活性弱耦合**：模糊逻辑打分选出的 73 条里最好只有 210 M⁻¹s⁻¹；10–70 倍来自去同源化 FuncLib 的能量排序（这仍是计算选择）；再 10 倍来自计算"能量等价建议"+实验实测的单点突变。三步中只有第二步是计算直接命中，且步幅最小。→ 该漏斗的**上限不是由下单前判据决定的**。
3. **本文最可复用的其实是 C 段消融实验与 R2 对照**：它们把"哪个组件贡献了什么"拆开了——这是"算完直接中"故事里唯一带对照设计、可被独立检验的部分；主结果反而是单谱系孤例。
4. **kcat 是他们的金标准**（批评前人只靠超低 KM 堆高效率），对应到我们：判定 UAA 合成酶时**周转/产物定量是金标准，结合检测不能替代**——这条口径可直接搬。
5. **MD/EVB 全在事后**（只为解释 Des27 vs Des27.7 差异），预组织判据用的是 Rosetta 刚体最小化而非动力学。所以这篇**不是**"MD 筛出好酶"的证据，是"能量+几何判据+小实验反馈到实用级"的证据。
6. 对标"天然酶中位"是把**单一模型反应**（无天然酶、单步质子抽取、有机相底物）与**全酶库统计中位**比较——修辞意义大于物理意义；同反应实验室内进化的酶（他们引的 ref 6/7 系）本来就在这个量级，"追平实验室进化"的主文与"追平自然"的宣传口径之间有缝。

## 7. 局限与被质疑之处

**作者自留的余地（原文可查）**

- 第一轮 73 条里只有 3 条有活性（"Three designs showed measurable KE activity in an initial screen"），且初测水平与前设计同档："falling short by several orders of magnitude from comparable natural eliminases and from designed Kemp eliminases that were optimized through laboratory-evolution campaigns"。达到 10⁴–10⁵ 量级靠的是后续两轮 FuncLib + 单点突变，全部以实验挑出的亲本为起点。
- theozyme 里芳香残基是强制先验："We note that the aromatic theozyme residue was forced in all our design steps and was based on previous Kemp eliminase design studies"——而最大的 10 倍跃迁（Phe113Leu 至 123,000 M⁻¹s⁻¹）恰恰推翻了这一先验，作者承认它 "This finding challenges a two-decade assumption in computational Kemp eliminase design that an aromatic residue is important for ligand binding"。下单前判据**没预测出**最优解。
- 作者把未来缺口落在 theozyme 建模："Future improvements in modelling theozymes may enable fully programmable biocatalysis"。

**我们的批判性阅读（推断）**

1. **单点案例不能读成方法成功率**。"necessary and sufficient"结论（第 5.2 条引句）建立在单一反应、单一折叠家族、单谱系消融（Des27.7 一条线）上；第二轮 R2 系列可复现出"稳定且 foldable、20 条有活性"，但活性天花板只有 2,000 M⁻¹s⁻¹——**流程可复现的是"能做出弱活性设计酶"，不是"能做出 10⁵ 高效酶"**。
2. **"追平天然酶"的对标口径有缝**：kcat 30 s⁻¹ 对比的是全天然酶库中位 10 s⁻¹（引 ref 16 的统计量），而 Kemp 消除本身是单步质子抽取的模型反应、底物唯一、产物 380 nm 直接可见；且溶解度限制下多数设计只能线性拟合 kcat/KM（"When substrate saturation could not be attained due to limited substrate solubility, the data were fitted to the linear region of the Michaelis-Menten model"），KM 与 kcat 不可分。同反应经实验室进化的前作（其引文 6/7）本就在此量级，"一步到位 vs 多轮进化"是通量叙事差异，不是绝对性能跨越。
3. **MD/EVB 是事后解释器**，15 µs 常规 MD + EVB 只覆盖 Des27/Des27.7 两个变体；EVB 有一条轨迹因活性位坍塌被剔除并补跑（"This trajectory was excluded from further analysis, with an extra trajectory being run to create a full set of 30 replicas."）。它没有参与候选削减，因此本文不能给"MD/QM 当筛子提高命中率"供证据。
4. **晶体验证只覆盖活性端**：3 个结构全部来自功能设计，失败设计为何失败（折叠错还是位点错）无直接观测，与 B09 的 Type I/II 盲区同类。

**后来被质疑/被超越的本地记录（二级来源，标注证据级别）**

- 我们语料登记：`sources/function-assignment-workflows.md:190` 记录一篇 2026 年 Nature Chem Biol（DOI 10.1038/s41557-026-02125-6，摘要级）报道**由通用结合蛋白演化出的从头 Kemp 裂合酶 kcat/KM 达 3.2×10⁶ M⁻¹s⁻¹**、称超过此前任何深度学习前设计数倍——即 K63 的"追平天然"上限在一年内被 DL+进化路线再抬约 26 倍。K63 的历史位置应写成"原子级工具单点触顶"，不是"酶设计已达到实用水平"。
- 本地底稿的 Europe PMC 前置元数据带 modified publication 标记（见本卡第 0 节"未取到的部分"），出版后有修订记录，但修订内容不在本地底稿内，**具体更正了什么属未核验**；引用本文结论时以此为一个已知未知项。
- 综合置信度：K63 的**数字台账可信**（全文级、3 个 PDB 结构可查）；其**"判据足以预测高效酶"的结论不可信**（被自己的 Phe113Leu 发现与一年后超越双重削弱）。能改变本判断的证据：一篇对多谱系/多反应前瞻验证同一漏斗且给出分母命中率的后续论文（本语料暂无）。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **多目标"模糊逻辑"过滤的结构，不是它的数值**：把"系统能量/链长、同骨架构内排名、催化残基 vdW、脱溶剂化、几何精度"并列排序、只取头部几十个——这正对我们"单一硬阈值互相打架"的问题；我们的对应项应换成 S0/S1/S2 事件的几何与能量列（判据内容自定，1 R.e.u./8 Å 壳层这些数值不搬）。
2. **下单前的预组织校验**：无配体刚体最小化后催化碱移位 >1.2 Å 即丢弃——这是本文里**唯一真正在实验前削减候选的动力学式判据**（虽然只用 Rosetta）。对 UAA 可类比"去掉底物/辅因子后，催化 constellation 是否还坐在设计位置"，作为廉价闸口替代长时 MD。
3. **全蛋白稳定化与活性位设计分开做、再消融验证**（Fig 4 逻辑）：我们每加一条漏斗判据，应像他们一样准备"关掉该组件"的小对照组，在真值面板上证明它贡献了哪个指标——这比端到端命中率便宜且可解释。
4. **kcat 口径优先于 kcat/KM**：对应我们"以周转/产物定量为金标准，结合检测（Foldseek/pLDDT/展示结合）只算必要条件"的既定纪律；本文给了这条纪律的一个成功先例。
5. **去同源化 FuncLib 的思路**（丢掉进化过滤、只留能量）在产物化学上不可做大规模，但"对实验挑出的少数活性亲本，做计算引导的 5–8 点局部组合优化"可以映射到我们"一轮、少量构建体、每点有假设"的迭代设计。

**不可迁移（为什么不能照搬）**

1. **几何 theozyme 匹配的前提是"反应坐标已知且单步"**。Kemp 消除=一个质子抽取过渡态；UAA 合成酶涉及多步化学事件与竞争性副产物，不存在单一 theozyme 可摆放。本文的成功不构成"摆位判据能筛 UAA 酶活"的任何概率证据。
2. **数字不许搬**：123,000 M⁻¹s⁻¹、30 s⁻¹、2.85 s⁻¹、"10–70 倍"、"追平天然中位"都是单反应单谱系结果；禁止作为我们任何候选的先验命中率或"算完直接中"的成功率引用（DP2R 口径：不许把别靶/别反应的数字当 UAA 判据）。
3. **他们的实验反馈便宜**（96 孔板 380 nm 一步读产物），我们每轮验证是 LC-MS/MS 级的贵——他们漏斗末端"73+18+16 条逐个测"的规模在我们预算下不存在；迁移的是"小批量、多样化、有亲本选择逻辑"的反馈设计，不是批量数字。
4. **TIM-barrel/IGPS 支架选择是反应特异的**（腔体大小恰好容纳底物）；不能推论"选个常见折叠+装催化位点"对 UAA 底物同样成立。
5. MD/EVB 在本文只做机理，**不能引用本文为"用 MD 筛酶"背书**；同理其 pLDDT≥90、r.m.s.d.<1 Å 只用于骨架质控，不是催化判据。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/kemp2025.txt

- 本地全文：`data/interim/baker_lit/ft/kemp2025.txt`（Europe PMC fullTextXML → 剥标签纯文本，96,423 B，2026-10-16 抓取；inventory.json 对 K63 登记 fetch_url = europepmc/webservices/rest/PMC12310539/fullTextXML）。本卡全部英文引句逐字对照**这一份**底稿生成（含其参考文献编号残留的跨句拆分与 U+212B 安培号原字符）。
- 对照底稿：`sources/baker.md:592`（题录、Crossref 9 人作者核验、has_baker=False 警示、MD/QM 句数统计）。
- 二级来源指针（第 7 节）：`sources/function-assignment-workflows.md:190`（2026 Kemp 3.2×10⁶ M⁻¹s⁻¹，摘要级）；Europe PMC 前置元数据 modified publication 标记见本地全文第 2 行。
- CSV 字段映射：第 3 节 ↔ 候选生成方法/计算筛选判据/阈值数字；第 4 节 ↔ 候选数递减/实验命中率/Kd或活性最好值/成本统计；第 7、8 节 ↔ 在方法演进链的位置。
- 未取到：Extended Data 图表、Supplementary Tables、更正文本本体。凡涉此处均已在卡内明写"未在本地核验"。
- **本卡自检**：交回前运行 `PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K63" --no-report`，结果见交付回报；引句在写卡前后各用同规则脚本对本底稿扫一遍，逐条命中才落笔。

<!--CSV回填
work_type=论文
target=Kemp 消除（5-硝基苯并异噁唑脱质子，无天然酶对应的模型反应），IGPS/TIM-barrel 支架
backbone_generation=Rosetta 模块装配：5 条 IGPS 链各切 5 段 all-vs-all 重组 + Rosetta 序列设计（2,500 骨架）；PROSS 稳定化（PSSM 约束）；内部活性预测器取 top 1,000；第二轮改用 BLAST 同源 4,381 → CD-HIT 1,200 → AF2 建模 pLDDT≥90 留 1,072
computational_filters=Rosetta Matcher 几何匹配摆放 QM 预置 theozyme（碱 Glu/Asp + 强制芳香残基；本文明示去掉第三位点极性相互作用）；8 Å 壳层 PSSM+theozyme 约束序列设计；模糊逻辑多目标过滤（能量密度、同骨架排名、活性位 vdW、催化碱 vdW、配体溶剂化、theozyme 几何精度）；活性位枚举 ΔΔG_system<+3 R.e.u.；pSUFER 标记位 FuncLib 重设计；无配体刚体最小化预组织校验；R2 系列 AF2-Rosetta 一致性校验；FuncLib 去同源化能量排序
thresholds=催化残基突变扫描允许集 ΔΔG_system<+1 R.e.u.；活性位枚举 ΔΔG_system<+3 R.e.u.；标记位重设计 ΔΔG_system<0（至少 5 个有利替换）；预组织 r.m.s.d.>1.2 Å 丢弃；AF2-vs-Rosetta r.m.s.d.<1 Å 接受；R2 骨架 pLDDT<90 丢弃；FuncLib 每轮取 10–15 条最低能；MD 结合判定 4 Å；nanoDSF 20–95 °C；活性检测 380 nm、底物 0.05–0.75 mM
md_used=否（不参与筛选；仅事后机理：Amber24 ff19SB/OPC，Des27/Des27.7 各 5×1 µs，共 15 µs，分析 Asp162 构象、底物驻留与口袋体积）
qm_used=是（仅机理与预置：theozyme 几何来自此前 QM 计算并作为匹配模板；底物 RESP/HF/6-31G(d) 参数化；EVB（Q6/OPLS-AA/SCAAS）算质子抽取活化自由能，30×10.2 ns/体系，均不参与候选排序）
experimental_methods=E. coli（BL21 DE3）+bdSUMO 表达、Ni-NTA；nanoDSF 表观 Tm；96 孔板 380 nm 动力学（Michaelis-Menten，底物不溶时线性区拟合 kcat/KM）；X 射线晶体学（Des27.7/9HVB 2.0 Å、R2.Des39/9HVH 2.1 Å、R2.Des49/9HVG 1.9 Å，AF2 模型做分子替换）；组件消融与单点突变验证
pipeline_counts=第一轮：2,500 骨架→top 1,000→每骨架 10⁵–10⁶ 设计（百万级）→模糊过滤+预组织校验→数十→73 送测→66 可溶→14 协同折叠→3 有活性→FuncLib 18 变体（6+12）→8 个提升 10–70 倍→Des27.7（12,700 M⁻¹s⁻¹/2.85 s⁻¹）→Phe113Leu（123,000 M⁻¹s⁻¹/30 s⁻¹）；第二轮：1,072 骨架→55 送测→49 可溶→28 折叠→20 活性（0.5–155 M⁻¹s⁻¹）→FuncLib 6×(9–14)+loop 16→最高 2,000 M⁻¹s⁻¹
hit_rate=73 条初筛 3 条有活性（约 4%）；折叠且可溶子集内命中更高但绝对活性低；唯一 10⁵ 级结果是单谱系（Des27→Des27.7→Phe113Leu），R2 复现系列上限仅 2,000 M⁻¹s⁻¹；不许外推为方法成功率
best_metric=kcat/KM 123,000 M⁻¹s⁻¹、kcat 30 s⁻¹（Des27.7-Phe113Leu）；Des27.7 本体 12,700 M⁻¹s⁻¹、2.85 s⁻¹、表观 Tm>85 °C
cost_or_stat_note=无 GPU·h/CPU 成本统计报告；MD 15 µs + EVB 每体系累计 612 ns 均为事后；实验侧约 150–230 个构建体的低通量测试（73+18+55+90 上下）；统计：Asp162 vdW 与效率 Spearman ρ=−0.88、P=6×10⁻⁵，EVB in/out ΔG‡ Wilcoxon P=7.7×10⁻⁹（Des27.7）/0.088（Des27），2–5 生物学重复
role_in_timeline=原子级设计工具链（模块装配+PROSS+Matcher/fuzzy+FuncLib）在模型反应用于酶上首次把 kcat 推到天然中位量级、且不经定向进化；但其 aromatic 先验被自身 Phe113Leu 结果推翻，一年后本地语料登记一篇 DL+结合蛋白演化路线把 Kemp 效率再抬约 26 倍（3.2×10⁶ M⁻¹s⁻¹，摘要级）；对 UAA 筛选是可迁移判据结构的参照系，不是成功率先例
source_pointer=data/interim/baker_lit/ft/kemp2025.txt（Europe PMC PMC12310539 fullTextXML，2026-10-16）；sources/baker.md:592；sources/function-assignment-workflows.md:190
CSV回填-->
