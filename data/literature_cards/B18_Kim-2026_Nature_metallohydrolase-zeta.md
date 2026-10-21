# [B18] Computational design of metallohydrolases——DFT theozyme + RFdiffusion2 + PLACER 预组织，零轮实验优化做出 >10⁴ M⁻¹s⁻¹ 的锌酯酶

Kim D, Woodbury SM, Ahern W, Tischer D, Kang A, Joyce E, … Kalvet I, Hilvert D, Baker D（华盛顿大学 IPD；ETH Zürich）
Nature 2026, 649:246–253（在线 2025-12-03；收稿 2024-11-12，接收 2025-10-13）· DOI 10.1038/s41586-025-09746-w · PMID 41339547 · PMCID PMC12727532
开放获取（CC BY）· 全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC12727532/
（同组论文：方法学本体见 [B20] RFdiffusion2；打分器本体见 [B19] PLACER。B20 正文里明确把本文的金属水解酶案例细节甩给这篇：ref. 49）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B18**（组：Baker组） |
| 本文取回方式 | 先行调研缓存（baker_lit，2026-10-16），非本轮 cards/fetch_log 抓取（fetch_log.tsv 无 B18 行）；文本为 PMC XML 抽取的纯文本 |
| 登记全文 | `data/interim/baker_lit/ft/metallohydrolase2026.txt`（66,182 B；本目录 `sources_map.json` 中 B18 唯一登记全文） |
| 对照底稿 | `sources/baker.md` 第 238–249 行（原卡，含 B18 命中率原始数字摘录） |
| 证据级别 | **全文级**（本卡所有英文引号片段均为该全文的逐字子串，经 `scripts/verify_literature_cards.py` 门禁逐字比对） |
| 未取到的部分 | Supplementary Information（Figs 1–27、Tables 1–5、Methods 4.1/4.2 细则）、Extended Data 图、36 组 DFT 坐标（Supplementary Data 1）与订购序列（Data 2/3）。凡涉及补充信息里的阈值与流程细节，本卡明写"正文未给出，仅正文描述" |

## 1. 这篇到底解决什么（大白话）

de novo 酶设计的老办法是：先给活性位点里每个催化残基**定死**序列位置和侧链构象（逆 rotamer 枚举），再让生成模型去配骨架。本文用配套新方法 RFdiffusion2（[B20]）绕开这一步——只给"围绕过渡态的侧链官能团坐标 + 底物 + Zn²⁺"这一小撮原子（theozyme，由 DFT 量子化学算出），序列位置和 rotamer 交给模型在每条生成轨迹里自己推。然后围绕同一个反应（4MU-PA 酯水解）连做两轮各 96 个的湿实验：第一轮 1/96 个效率 >10³ M⁻¹s⁻¹（最好的 ZETA_1 = 16,000 M⁻¹s⁻¹，比此前设计金属水解酶高 2–4 个数量级）；从失败数据里学到"通用碱 D67 其实在跟组氨酸抢锌"之后，第二轮把催化碱显式写进 DFT theozyme、换更大训练集的新版模型，11/96 命中、最好 53,000 M⁻¹s⁻¹，且全部是零实验优化（不进化）。最后用 X 射线晶体结构证明实验结构与设计模型几乎重合。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **旧管线的组合爆炸是根本障碍**。RFdiffusion 需要逐个指定催化残基的 backbone 坐标与序列位置，作者给出量级："even with relatively coarse sampling around the side-chain chi angles χ 1 , χ 2 , and the backbone torsion angle ψ , there are on the order of 10 18 possible choices for the side-chain conformations and sequence placements of our full catalytic site"，并且 "Whereas each RFdiffusion run has to be initialized with a specific (and generally randomly selected) choice from this enormous set of combinations"——每次运行只随机押一个组合，空间根本盖不住。→ **应对**：改用 RFdiffusion2 的原子级 + 无索引 motif 条件化，把枚举变成模型在轨迹内的联合推断（"RFdiffusion2 as described above searches the entire space in each trajectory"）。→ **代价**：要训练新模型（单价见 [B20]：17 天 × 24 A100），本文正文不含其训练细节。
2. **第一轮设计里"通用碱"失效且原因隐蔽**。第一轮 theozyme 未显式含催化碱；ZETA_1 活性位里出现的天冬氨酸 D67 本应活化水，但突变实验反常："mutation of the proposed general base D67 to alanine had little effect on k cat / K M and increased Zn( II )-binding affinity"。→ **应对**：作者用"双位点竞争"解释（"H134/H118/H130 and H134/H118/D67 may be competing Zn( II )-binding sites"），并拿 Chai-1 对蛋白–Zn–底物复合物的预测佐证（模型 1 里 H130 翻出、D67 配锌）；随后**从"显式含催化碱"的新 DFT theozyme 重起第二轮**。结果第二轮 11/96 命中且 5 个 >10⁴。→ **残留代价**：ZETA_1 的碱到底起没起作用仍是"不太可能高效工作"级别的推断（"Thus, it is unlikely that D67 is functioning efficiently, if at all, as a general base"），正文未给直接观测。
3. **筛选闸口会不会错杀好设计，本身是个待验证问题**。设计阶段有 7 个 ZETA_1 同骨架家族的设计因 PLACER 预组织指标差被剔除。→ **应对**：他们没有让这一步留在暗处——"Seven designs based on the same ZETA_1 backbone family were initially filtered out during the design selection phase, as they had suboptimal PLACER metrics; we retrospectively expressed and purified these designs and found that they had very low or no activity"，用回溯实验给 PLACER 闸口补了一次阴性对照。→ **代价**：这只是**一个骨架家族的 7 个样本**，闸口的假阴性率仍未知；正文未给 PLACER 排序的具体阈值（在 Supplementary Fig. 3 / Methods 4.1，未取到）。
4. **金属亲和力弱于天然酶**：锌滴定 "measured a dissociation constant ( K D ) for Zn( II ) of 41 ± 5 nM"，而天然锌水解酶 "typically have K D values less than 10 nM"。→ **应对**：本文不做进化补救（口径就是不进化），把"更好预组织金属结合残基"列为未来方向。→ **代价**：稀锌/复杂介质场景未测。
5. **晶体结构出现与设计不符的构象**：锌浸泡晶体里 "one of the Zn( II )-coordinating histidines (H110) was flipped out to interact with a Zn( II ) ion bound at the surface of the protein"，作者归因于浸泡液锌浓度过高（250 mM），并自问催化碱 E34 的构象变化是结晶假象还是真实动态——Extended Data Fig. 8 里承认 "If it is dynamic, this poses an interesting question of whether the dynamics accelerate or hinder the activity of ZETA_2"。**本文未解决**，只提出用 buttress 重设计去检验。
6. **第一轮命中率其实很低**。两轮口径一样（各 96 个送测），"The success rate in the second design campaign was considerably higher than the first campaign"（11/96 对 1/96，判据为 k_cat/K_M > 10³）。→ **应对**：归因写回第一轮分析（补充讨论 2），并落实为两处改动（theozyme 加碱 + "a newer version of RFdiffusion2 trained from random weight initialization on a threefold-larger dataset"）。→ **代价**：第一轮 96 个名额里 95 个阴性结果没有公开逐条台账（序列与设计模型在 Supplementary Data 2/3，本地未取）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **QM（本文的输入端主角）**：DFT 优化过渡态几何（Zn²⁺-氢氧根对酯羰基的亲核攻击），产出 theozyme 坐标（三个组氨酸咪唑 + Zn + 过渡态）。注意：**QM 只用来定义输入，不用来给候选打分**。
- **生成**：RFdiffusion2（原子级、无索引 motif 条件化；本文档另用了一版"threefold-larger dataset、随机初始化训练"的新模型）。
- **序列**：第一轮 ProteinMPNN 出序列，几何优化阶段改**迭代 LigandMPNN + 约束 Rosetta repacking/minimization**（把催化基团和 Zn–TS 复合物钉在 DFT 几何附近）。
- **结构复核**：AlphaFold2（第一轮主闸）、Chai-1（第二轮复合物态：蛋白–Zn–膦酸酯过渡态 mimic）。
- **预组织打分**：PLACER（[B19]）生成活性位构象系综，看催化侧链与底物是否在设计位置"钉住"。
- **湿实验**：线性 DNA 片段 → E. coli（C 端 Strep-tag 质粒）→ Strep 亲和纯化 → SDS-PAGE 判可溶 → 补 ZnSO₄ 后 4MU-PA 荧光水解初速度 → 单克隆 SEC 纯化 → Michaelis–Menten；CD、锌螯合(1,10-phenanthroline)/回补、K_D 滴定、定点突变、X 射线晶体学。
- **没有用的方法**：MD 全程缺席（预组织由 PLACER 近似，理由见 [B19] 第 2.1 条）；也没有定向进化——两轮都靠重设计而非进化。

### A. 第一轮：以 ZETA_1 为终点的漏斗

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 反应机理假设（Zn²⁺-OH 亲核攻击 4MU-PA） | DFT 找过渡态；按四面体中间体立体化学 × 氧阴离子洞类型取 **4 种排列** | 正文未给能量/几何阈值（Supplementary Methods 4.1，未取到） | 4 组 theozyme 坐标（三咪唑+Zn+TS；Supplementary Data 1 前 4 组） |
| A2 | theozyme | RFdiffusion2 推理轨迹建骨架，逐条 ProteinMPNN 出序列 | 无（生成不设闸） | "A total of 5,120 RFdiffusion2 inference trajectories were carried out starting from different random seeds" |
| A3 | 骨架+序列 | AF2 复折，取预测接近设计模型者；再修催化几何 | "predicted structure was close to the design model"（原文该词组中间插着引文编号 35；正文未给数值阈值） | 进入下一闸的集合规模未公布；几何优化为 "were further optimized using iterative LigandMPNN 36 and constrained Rosetta repacking and minimization" |
| A4 | 修复后的设计 | 硬约束过滤：拟通用碱（Glu/Asp/His 与 Zn 结合水成氢键距离）、TS 氧阴离子的侧链氢键、AF2 预测成目标结构 | "Designs containing a proposed general base positioned to activate the water molecule (that is, Glu, Asp or His within hydrogen bonding distance of the Zn( II )-bound water) and side-chain hydrogen bonds stabilizing the transition-state oxyanion (if applicable), and that AlphaFold2 predicted to adopt the target structure" | 存活者进 PLACER |
| A5 | A4 存活者 | PLACER 系综评估预组织 + 排序选送测名单 | "predicted active site geometry and preorganization"（正文未给 PLACER 指标阈值） | "A total of 96 designs were selected for experimental characterization" |
| A6 | 96 设计 | 线性 DNA→E. coli 表达→Strep 纯化→SDS-PAGE 判可溶→补锌→4MU-PA 荧光初速度 | 活性显著高于缓冲背景 | "Eighty-six out of ninety-six designs were expressed and soluble"；"Five designs (A1, A8, B9, C4 and F7) had activity well above background" |
| A7 | 5 个活性设计 | 单克隆 SEC 纯化（判单体）→ 稳态动力学 | Michaelis–Menten 拟合 | A1：k_cat/K_M 16,000 ± 2,000；其余四个 "values in the range of 35"（35–140 M⁻¹s⁻¹）；对照：先前设计金属水解酶 "ranged from 3 to 60" |

### B. 第二轮与反查验证

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 第一轮突变学 + Chai-1 复合物预测结论 | **新 DFT theozyme：显式含催化碱**；换新版 RFdiffusion2（随机初始化、三倍数据） | 同上 | 32 组新 theozyme 坐标（Data 1 后 32 组，正文口径） |
| B2 | 新骨架库 | Chai-1 预测蛋白–Zn–膦酸酯过渡态 mimic 接近设计模型 + 高置信，PLACER 判高度预组织 | "closely matched the design models with high confidence"（正文未给数值） | "Ninety-six such designs spanning 37 RFdiffusion2-generated backbones were selected for experimental characterization" |
| B3 | 96 设计（第二轮） | 同 A6 流程 | 锌依赖性活性 | "Eighty-five of the 96 designs were expressed and soluble"；"11 designs spanning 3 different folds had substantial zinc-dependent 4MU-PA hydrolysis activity"；5 个 >10⁴、6 个 >10³；ZETA_2 = 53,000 ± 5,000（k_cat 1.5 ± 0.1 s⁻¹）、ZETA_3 = 19,000、ZETA_4 = 1,100 |
| B4 | 被 PLACER 剔除的同家族设计 | 回溯表达纯化测活 | 有/无活性 | "we retrospectively expressed and purified these designs and found that they had very low or no activity"（7 个，支持 PLACER 闸口） |
| B5 | 机理归因 | 锌螯合/回补、K_D 滴定、定点突变（N17A、H118A/H130A/H134A 等） | 活性与锌亲和力变化 | "extraction of bound Zn( II ) by dialysis in the presence of the chelator 1,10-phenanthroline completely eliminated activity, and activity was subsequently restored by addition of zinc to the solution"；"the N17A mutation led to a 8.1-fold decrease in k cat / K M"；三组氨酸全突变与 118/134 双突变 "completely inactivated the enzyme"；H130A 仅降 13 倍 |
| B6 | ZETA_2 | X 射线衍射（apo + 锌浸泡） | 与设计模型叠加 | apo 3.5 Å（PDB 9PYJ）"nearly superimposable backbones (Cα root mean squared deviation (r.m.s.d.) = 1.1 Å)"；浸泡 2.1 Å（9PYL）Cα 0.8 Å、Zn 位 100% 占比 r.m.s.d. 1.7 Å（H110 翻出，见第 2.5 条） |

**这套流程的骨架值得单独记住**：QM 在**输入端**（定 theozyme）而不在**打分端**；打分端是"复折一致性 + 硬几何约束 + PLACER 系综"三级漏斗；实验预算固定 96 个/轮；失败归因（D67 抢锌）直接改写了下一轮 theozyme 的定义——**漏斗的每一环都能被湿实验反查**。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| ~10¹⁸ | 旧管线要枚举的侧链构象×序列位置组合数 | "on the order of 10 18 possible choices for the side-chain conformations and sequence placements" |
| 5,120 | 第一轮 RFdiffusion2 推理轨迹总数 | "A total of 5,120 RFdiffusion2 inference trajectories were carried out starting from different random seeds" |
| 96 / 96 | 两轮各自的固定送测数 | "A total of 96 designs were selected for experimental characterization"；"Ninety-six such designs spanning 37 RFdiffusion2-generated backbones" |
| 86/96、85/96 | 两轮表达且可溶数 | "Eighty-six out of ninety-six designs were expressed and soluble"；"Eighty-five of the 96 designs were expressed and soluble" |
| 5（第一轮）、11（第二轮） | 高于背景的活性设计数 | "Five designs (A1, A8, B9, C4 and F7) had activity well above background"；"11 designs spanning 3 different folds" |
| 16,000 ± 2,000 / 35–140 / 3–60 | ZETA_1 效率 / 第一轮其余命中 / 先前设计金属水解酶区间（M⁻¹s⁻¹） | "the most active has a catalytic efficiency"；"values in the range of 35"；"ranged from 3 to 60" |
| 53,000 ± 5,000；19,000；1,100 | ZETA_2/3/4 效率 | "with k cat / K M values of up to 53,000" |
| 1.5 ± 0.1 s⁻¹；10 轮进化 | ZETA_2 转换数；对照 MID1sc10 靠定向进化 | "a threefold increase over the k cat of ZETA_1, and close to that of the metallohydrolase MID1sc10 obtained after 10 rounds of directed evolution" |
| 11/96 对 1/96 | 两轮成功率（>10³ 判据） | "The success rate in the second design campaign was considerably higher than the first campaign" |
| 41 ± 5 nM / <10 nM | ZETA_1 锌 K_D / 天然酶典型 K_D | "measured a dissociation constant ( K D ) for Zn( II ) of 41 ± 5 nM"；"typically have K D values less than 10 nM" |
| 8.1 倍 / 13 倍 / 完全失活 | N17A / H130A / 三 His 全突变的效果 | "the N17A mutation led to a 8.1-fold decrease in k cat / K M"；"completely inactivated the enzyme" |
| ≥1,000 周转 | ZETA_1 稳健性 | "A1 is also a relatively robust enzyme, and retains activity for at least 1,000 turnovers" |
| 0.41 / 0.49 | ZETA_1 对 PDB / AFDB 最近结构的 TM 分数 | "have TM scores 38 of 0.41 and 0.49, respectively" |
| 600 原子球 | PLACER 随机化范围 | "fully randomizes the positions of the substrate and all side chains within a 600-atom sphere" |
| 3.5 Å→1.1 Å；2.1 Å→0.8 Å；250 mM | ZETA_2 apo 晶体分辨率与设计模型 Cα RMSD / 锌浸泡 / 浸泡锌浓度 | "in the apo state at 3.5 Å using X-ray crystallography (PDB: 9PYJ"；"probably because of the high Zn( II ) concentration in the crystal soaking buffer (250 mM)" |
| 10⁴ ~ 10⁶ | 天然同类底物金属水解酶的典型效率区间 | "The catalytic efficiencies of ZETA_1–3 are within the range typically observed for native metallohydrolases with similar substrates" |

## 5. 结论——作者说了什么

1. RFdiffusion2 只需侧链官能团坐标（不必指定序列位置/骨架），从 DFT theozyme 直接造出了"orders of magnitude higher than previously designed metallohydrolases"的锌酯酶（摘要句 "From an initial set of 96 designs tested experimentally, the most active has a catalytic efficiency"）。
2. 零实验优化：ZETA_1 是 96 个中计算排名第一的设计——"the top-ranked in silico design out of a total of 96 tested straight from the computer, with no experimental optimization"；第二轮又从新 96 个零 shot 得到 3 个高活性酶。
3. ZETA_1–4 结构互相不同、也与已知结构不同（TM 0.41/0.49），ZETA_2 晶体结构与设计模型高度一致；"The catalytic efficiencies of ZETA_1–3 are within the range typically observed for native metallohydrolases with similar substrates"。
4. 机理证据：锌绝对必需（螯合全灭、回补恢复）；活性位组装方式与 theozyme 假设一致（三 His 配 Zn、Zn 兼作氧阴离子洞，"there are no nearby side-chain hydrogen bond donors"——此句在 Extended Data Fig. 5 描述语境，正文对应表述为锌离子充当氧阴离子洞）。
5. 展望：把"RFdiffusion2–PLACER"当成通用范式推向更多键断裂/键形成反应（"we have found the RFdiffusion2–PLACER design approach described here to yield biocatalysts for a variety of bond-breaking and bond-making chemical reactions"）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的价值不在 96→11 的命中率，而在"闸口可反查"**：PLACER 剔除的 7 个被回溯表达验证了阴性；突变学发现的机理缺陷被翻译成下一轮输入（theozyme 加碱）。我们项目里对应动作是：每道闸口都要留一个"能证伪它"的回溯子集，否则闸口只是玄学。
2. **QM 的正确站位是"出题人"，不是"阅卷人"**。DFT 只负责定义过渡态几何；打分全靠便宜的 ML 系综。对照我们：xTB/QM 应产出机制性输入（态几何、电荷分布），不该按候选逐个长算。
3. **实验预算固定 96 个/轮 + 表达率 ~90% 的前置事实**，使"送测名单怎么排"成为唯一可优化的自由度。我们没有表达通量，但同样可以把"一轮最多测 N 个"写死，倒推漏斗该保留多少多样性（他们第二轮 96 个只覆盖 37 个骨架家族——刻意留家族内多样性）。
4. **第一轮失败的根因是 theozyme 假设不完整（碱缺位）**，而不是模型不准。→ 我们的 S0/S1/S2 三事件里，若某事件没进"theozyme 等价物"，模型不会替你补上；机制假设的完备性是上限。
5. **"零 shot"叙事依赖两个隐性条件**：送测前已完成全部筛选（排序第一名即中）+ 判据是连续动力学参数而非二值结合。我们连产物身份的湿实验判据都还没稳定，"排名第一即命中"没有可比性。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者自认：锌亲和力仍弱于天然酶（41 vs <10 nM）；D67 是否作通用碱"不太可能高效工作"；ZETA_2 晶体里 H110/E34 构象"可能是结晶浸泡假象也可能是真实动态"，本文未解决；两轮共 192 个送测里第一轮 95 个阴性、第二轮 85 个阴性，正文没有逐一归因。
- 我们读出：① 正文未给 PLACER/AF2/Chai-1 闸口的**数值阈值**（全部在 Supplementary Methods 4.1/4.2，本地未取），所以本卡工作流表里相应步骤标"原文未给阈值"；② "1 out of 96"的判据是 >10³ M⁻¹s⁻¹，把 35–140 区间的另外 4 个活性设计划在"成功"外——**同一批数据的成功率可以随判据口径翻倍**，引用时必须注明口径；③ 底物是荧光报告分子 4MU-PA，非工业/环境底物；④ 无 MD、无自由能计算，构象动态只被 PLACER 系综近似（时间维度缺失，见 [B19] 第 2.1 条）；⑤ 摘要与正文对 ZETA_2–4 的 k_cat/K_M 表述有 ± 与圆整差异（摘要 53,000 M⁻¹s⁻¹ 级，正文 53,000 ± 5,000），引用建议带误差。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么做）**

1. **QM 站输入端**：用 DFT 定义 our-theozyme 等价物（UAA 合成酶各步反应的过渡态几何与必需相互作用），喂给结构生成/评估；打分端一律用便宜代理（复折一致性 + PLACER 式系综 + 硬几何约束）。这与 B09 §8 的"判据不上考卷不进漏斗"配套：QM 定义的是**考题**，不是**分数**。
2. **闸口反查制度**：像"7 个被 PLACER 剔除的设计回溯表达"一样，每道计算闸口留出一小批"被它杀掉"的候选，送进湿实验验证假阴性率。我们一轮 4 个构建体的预算下可以这样省：把反查名额与探索名额合并（反查样本本身选在闸口边界附近）。
3. **机理缺陷→改输入，不改权重**：第一轮教训（碱缺位）是通过重写 theozyme 解决的。我们的对应操作：S1/S2 竞争中暴露的假设漏洞应回改机制假设面板（DP2R 标准 G0 真值），而不是调模型阈值。
4. **固定实验预算的漏斗设计**（96 个/轮）与"先判可溶/表达，再判活性"的两段湿实验排序（86/96 可溶是重要前置统计量）。

**不可迁移（为什么不能照搬）**

1. **本文一切数字（1/96、11/96、16,000、53,000 M⁻¹s⁻¹）是"锌指酯水解"这一被完美表征反应的成功率**，不得当作 UAA 合成酶命中概率引用或校准；连作者都只敢外推到"bond-breaking and bond-making"的自家后续论文。UAA 三事件（S0 游离 UTP 起始 / S1 pppUA / S2 第二枚 ATP vs 环化）没有等价的 DFT 过渡态输入——**本文成立的前提"theozyme 可由 DFT 可靠定义"在我们这里未成立**。
2. **PLACER 需要输入完整化学图（原子类型+成键）与可信骨架坐标**；我们的目标体系连配体（UTP/衍生物）在活性位的确切结合态都是假设对象，预组织指标没有可算的底座。
3. **判据口径不可平移**：这里的"成功"= 稳态动力学参数超过数值线；我们的产物化学判据是 LC-MS/MS 身份+定量，二者不是同一层次；binder 的 pAE/ipTM 阈值更与本文无关，不能混入（DP2R 标准 §2）。
4. **零 shot 叙事不能当承诺**：作者只交付了两个靶向反应；把"straight from the computer"外推到全新机制反应没有依据。

## 9. 溯源与自检

- 引句底稿: data/interim/baker_lit/ft/metallohydrolase2026.txt（本卡全部英文引号片段的逐字比对对象）
- 本地全文：`data/interim/baker_lit/ft/metallohydrolase2026.txt`（PMC12727532 XML 抽取纯文本，先行调研缓存；本卡引句在 norm（HTML 实体解码+NFKC+空白折叠）后逐字命中）。
- 对照底稿：`sources/baker.md:238–249`（B18 原卡，含引句摘录）；`sources/baker.md:5,39`（"MD 不作筛选器"时间线）、`sources/baker.md:618,646,662`（96 送测与 DFT-theozyme 口径行）。
- 关联卡：方法本体 [B20]（RFdiffusion2 的训练与基准在那篇；B20 正文也把金属水解酶案例细节指回这篇），打分器本体 [B19]。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B18 --no-report` 输出 `PASS B18 quotes=N/N`（引句全部逐字命中登记全文；门禁不判内容对错，正文口径仍需按上表指针复核）。补充信息未取回，凡"原文未给阈值"处不可当作原文沉默的阈值使用。

<!--CSV回填
work_type=论文
target=Zn(II) 金属水解酶（4MU-PA 荧光酯水解；ZETA_1–4）
backbone_generation=RFdiffusion2 围绕 DFT theozyme 生成骨架（5,120 轨迹）；序列 ProteinMPNN，几何优化用迭代 LigandMPNN + 约束 Rosetta repacking/minimization；第二轮用随机初始化+三倍数据集训练的新版模型
computational_filters=AF2 预测与设计模型一致性；硬几何约束（Glu/Asp/His 通用碱氢键距离、氧阴离子侧链氢键）；Chai-1 蛋白-Zn-膦酸酯复合物预测；PLACER 活性位预组织系综排序
thresholds=正文未给数值阈值（PLACER/复折指标在 Supplementary Methods 4.1/4.2，本地未取）；成功判据口径：k_cat/K_M > 10³ 与 > 10⁴ M⁻¹s⁻¹ 分档
md_used=否（全程无 MD；预组织由 PLACER 系综近似）
qm_used=是（DFT 定过渡态/theozyme 几何，作为生成模型的输入端，不作逐候选打分）
experimental_methods=线性 DNA→E. coli Strep-tag 表达→亲和+SEC 纯化→SDS-PAGE 可溶判定→补 ZnSO₄ 的 4MU-PA 荧光初速度→Michaelis–Menten；CD；1,10-phenanthroline 螯合/回锌；锌 K_D 滴定；定点突变；X 射线晶体学（9PYJ/9PYL）
pipeline_counts=第一轮：5,120 轨迹 → 复折+硬约束+PLACER → 96 送测 → 86 可溶 → 5 活性 → 1 个 >10³（ZETA_1）；第二轮：新 theozyme → 96 送测（37 骨架）→ 85 可溶 → 11 活性（3 折叠，5 个 >10⁴）；另回溯表达被剔除的 7 个
hit_rate=第一轮 1/96、第二轮 11/96（>10³ M⁻¹s⁻¹ 口径）；两轮均无定向进化（零 shot）
best_metric=k_cat/K_M = 53,000 ± 5,000 M⁻¹s⁻¹（ZETA_2，k_cat 1.5 ± 0.1 s⁻¹）；第一轮最优 ZETA_1 = 16,000 ± 2,000
cost_or_stat_note=正文无算力/成本数字；结构新颖性 TM 0.41（PDB）/0.49（AFDB）；锌 K_D 41 ± 5 nM；ZETA_2 晶体与设计模型 Cα RMSD 1.1 Å（3.5 Å apo）与 0.8 Å（2.1 Å 锌浸泡）
role_in_timeline=与 [B20][B19] 构成「RFdiffusion2 + PLACER + DFT theozyme」三件套的首个酶学落地：酶设计第一次做到「计算排名第一的 96 分之一零优化即达标」，并示范了闸口阴性反查（7 个被剔除设计回溯表达）
source_pointer=data/interim/baker_lit/ft/metallohydrolase2026.txt（PMC12727532 抽取文本，66,182 B）；sources/baker.md:238-249
CSV回填-->
