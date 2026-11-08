# [C01] 从零设计皮摩尔级 SARS-CoV-2 最小蛋白——物理打分时代的天花板，与"筛不出最好的候选"这一自认瓶颈

Cao L, Goreshnik I, Coventry B, Case JB, Miller L, Kozodoy L, Chen RE, Carter L, Walls AC, Park YJ, Strauch EM, Stewart L, Diamond MS, Veesler D, Baker D（华盛顿大学 IPD + 圣路易斯华盛顿大学 + 西雅图儿童研究所）
Science 2020, 370(6515):426–431 · DOI 10.1126/science.abd9909 · PMID 32907861 · PMCID PMC7857403（CC BY 4.0）
预印本 bioRxiv 10.1101/2020.08.03.234914 · 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7857403/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C01**（组：曹龙兴组；第一作者曹龙兴，博后期间 2020，末位 Baker D） |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory.json 登记 fetch_channel=epmc_fulltext），2026-10-20 本地抓取 |
| 本地全文 | `data/literature_cards/fulltext/C01_PMC7857403_fullTextXML.xml`（115,068 B）；去标签纯文本 `data/literature_cards/fulltext/C01_PMC7857403_text.txt`（40,312 B） |
| 对照底稿 | `sources/cao.md` 第 36–51 行（原卡）。本卡全部引句取自本地全文而非底稿 |
| 底稿需核对之处 | 底稿说骨架库"承 C05 的 84,690 条骨架库"——**C01 正文未给骨架库规模**，只写 "large in silico miniprotein libraries ( 11 )"（引文 11 = Chevalier 2017 Nature 流感 minibinder 库）；84,690 是 C02/C05 论文的口径，属推断而非 C01 自述 |
| 门禁登记 | `sources_map.json` 的 C01 条目原只登记底稿 `sources/cao.md`，本卡写作时已把上述两份全文补进该条目（与 inventory.json 一致），否则逐字引句无法对全文核验 |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中，见第 9 节） |
| 未取到的部分 | 补充材料（science.org DC1：Materials and Methods、Figs. S1–S14、Tables S1–S3）不在本地 XML 内。设计阈值、文库构建细节、表位竞争计算表等凡涉补充材料处，本卡明写"正文未给出" |

## 1. 这篇到底解决什么（一句话）

疫情头几个月，用纯计算（Rosetta 物理打分 + RIF 对接）从零设计出 56–64 个残基的小蛋白，让它们以皮摩尔级亲和力抢占 SARS-CoV-2 刺突蛋白 RBD 的 ACE2 结合位点、阻断活病毒感染——并且用 cryo-EM 证明折出来的结构和设计模型几乎一致（骨架 Cα RMSD 1.27/1.9 Å）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **最大的一层损耗在"表达"，不在"结合"——而且分母口径必须逐层报清**。漏斗是：NGS 从酵母分选里鉴定出 3 个 ACE2 螺旋支架设计（"approach 1"）与 105 个从头界面设计（"approach 2"）→ "All three ACE2-scaffolded designs and 12 of the de novo designs were expressed in Escherichia coli and purified." → "One of the ACE2-scaffolded designs and 11 of the 12 de novo designs were soluble and bound RBD with affinities ranging from 100 nM to 2 μM in biolayer interferometry"。**他们做了什么**：逐层分开报数（12/105 表达 = 11.4%；11/12 结合 = 91.7%；绝对 11/105 = 10.5%）。**代价与易误读处**：91.7% 是"表达成功者里的结合率"，把它说成"设计成功率约 90%"就是把分母从 105 偷换成 12；而且 105 本身已是 FACS 富集后的集合（"that were enriched after fluorescence-activated cell sorting (FACS) for RBD binding"），正文从头到尾**没有给计算生成的总库规模**，所以整条漏斗的绝对命中率按本文口径根本算不出来。
2. **ACE2 螺旋路线（approach 1）亲和力上去了、热稳定性塌了**：PCR 定向进化得到 AHB1（"Affinity maturation of the ACE2-scaffolded design by means of polymerase chain reaction (PCR) mutagenesis led to a variant, AHB1, which bound RBD with an affinity of ~1 nM"），但作者紧接着写该设计 "consistent with the design model, but had low thermostability"。**他们做了什么**：不再单点修补，而是把 AHB1 的结合螺旋发卡整体移植进新支架——"We generated 10 additional designs incorporating the binding helix hairpin of AHB1 and found that one bound the RBD and was thermostable"（第二代支架即 AHB2 的来路）。**代价**：approach 1 这条线最后只剩一个设计进入组合优化（作者自述该路线的路线性收敛）。
3. **BLI 测不动最强的两个设计**：LCB1/LCB3 "the K d values were below 1 nM, which is too strong to measure reliably with this technique"。**他们做了什么**：加三条独立正交读数——酵母表面 5 pM 浓度下加胰蛋白酶/糜蛋白酶消化后仍有信号（"On the surface of yeast cells, LCB1 and LCB3 showed binding signals at 5 pM of RBD after protease (trypsin and chymotrypsin) treatment"）、CD 热熔（"the melting temperatures for most were greater than 90°C"）、室温 14 天活性保持（"The designs retained full binding activity after 14 days at room temperature"），最后以活病毒中和 IC50 作为功能终点。**代价**：正文对最优设计只给"低于 1 nM"，无精确 Kd；摘要口径为 100 pM–10 nM。
4. **cryo-EM 全局图不足以看清界面相互作用**：**他们做了什么**——"We improved the resolvability of the RBD/LCB1 and RBD/LCB3 densities by using focused classification and local refinement yielding maps at 3.1 and 3.5 Å resolution"；另外 LCB3 复合物里三 RBD 全开的颗粒只是少数（"we identified a subset of particles with three RBDs open for the LCB3 complex"），按构象亚群分开处理。**代价**：局部精修图只用于界面可视化，整体复合物分辨率仍 2.7/3.1 Å。
5. **起始时靶结构都没有**："We began to design minibinders in January 2020 on the basis of a Rosetta model of the SARS-CoV-2 spike structure and switched to the crystal structures once they became available"。**他们做了什么**：先用预测模型下单，晶体结构一发布立刻换输入。**代价**：早期设计基于模型结构，后期靠结构更新补救。
6. **作者自认的真正瓶颈不是设计、是"识别"**（这是本文最有价值的自我诊断）："the main challenges to overcome are not in the de novo design of proteins with shape and chemical complementarity to the target surface, but in recognizing the best candidates and identifying a small number of affinity-increasing substitutions"。**他们做了什么（本文内）**：把"识别最好候选"外包给实验——50 个设计逐个做全域单点突变库并深测序（见第 3 节 W7–W8），再组合富集突变；同时明写计算侧才是终局——"it should be possible to streamline the workflow described here, which required screening of large sets of computational designs, followed by experimental optimization, to identify very-high-affinity binders"。**本文未解决的部分**：如何**在下单前**用计算方法挑出那 1/105——这句话直接构成 B09（Bennett 2023）整篇"给筛子当考卷"的问题来源。
7. **免疫原性只是论证、没有实验**：作者把潜在免疫原性问题交给文献外推（小 de novo 蛋白此前"little or no immune response has been observed"），本文无动物免疫原性数据。**本文未解决**（该实验直到 C04 才补做）。

## 3. 方法与工作流程（每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **生成端**：Rosetta 物理能量函数 + 两条设计路线——approach 1 用 Rosetta blueprint builder 把 ACE2 结合螺旋嵌入小骨架；approach 2 用 RIF（rotamer interaction field）对接大规模计算骨架库 + Rosetta 序列设计。
- **计算筛选端**：正文可查的判据只有定性表述（对设计模型算 Rosetta ddG/形状与化学互补等界面指标来挑选对接与序列；摘要侧只有 "their amino acid sequences were designed to optimize target binding, folding, and stability" 这类无阈值描述）；**正文与图注均未给出任何数值阈值**（数值阈值体系在 C02/B09 才成文）。
- **实验筛选端**：酵母表面展示 + 荧光标记 RBD 的 FACS 多轮分选 + NGS；SSM 单点突变全图 + 组合突变库；E. coli 表达 + BLI；CD 热熔；cryo-EM；活病毒空斑减少中和试验（FRNT, Vero E6）。
- **没有用的方法**：MD、QM、自由能微扰全无；深度学习只做后来的 cryo-EM/结构比对语境，未进设计漏斗。

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | 2020-01 起的刺突结构 | 先按 Rosetta 模型设计，晶体结构发布后切换输入 | 结构可用性（原文未给阈值） | 靶：RBD 及胞外域三聚体 |
| W2a | ACE2 螺旋（人 ACE2 残基 23–46） | "we used the Rosetta blueprint builder to generate miniproteins that incorporate the ACE2 helix (human ACE2 residues 23 to 46)" | 原文未给阈值 | approach 1 设计池（规模正文未报） |
| W2b | 自有从头骨架库 + RBD 表面 | "we used rotamer interaction field (RIF) docking ( 12 ) with large in silico miniprotein libraries ( 11 ) followed by design"，围绕 ACE2 结合位点周边的不同区域生成结合模式 | 形状/化学互补（定性，无数字阈值） | approach 2 设计池（规模正文未报） |
| W3 | 两条路线的设计池 | "were encoded in long oligonucleotides and screened for binding to fluorescently tagged RBD displayed on the surface of yeast cells"，FACS 分选后 NGS 统计富集 | 判据=分选后富集（阈值原文未给） | "Deep sequencing identified three ACE2 helix scaffolded designs"，"and 105 de novo interface designs" |
| W4 | 上述 3+105 个克隆 | E. coli 表达 + 纯化 | 可溶/可得量 | 3 + "12 of the de novo designs were expressed" |
| W5 | 表达产物 | BLI 测亲和力 | 结合即算命中 | 1 + "11 of the 12 de novo designs were soluble and bound RBD with affinities ranging from 100 nM to 2 μM in biolayer interferometry"（初始结合体，μM–百 nM 级） |
| W6 | ACE2 路线最优者 | PCR 易错突变亲和力成熟 → AHB1（~1 nM）；因热稳定性差，移植其结合螺旋发卡重设计 10 条 | 酵母表面竞争（ACE2 竞争掉结合）+ CD | AHB1 及第二代支架（1/10 结合且耐热） |
| W7 | approach 2 的 50 个 minibinder + 第二代支架 | "we generated site saturation mutagenesis libraries (SSMs) in which every residue in each design was substituted with each of the 20 amino acids one at a time"，分选前后 NGS 定位移熵/富集 | 界面与核心保守判据：保守=设计模型大体正确 | "residues at the binding interface and protein core were largely conserved for 40 out of the 50 approach 2 minibinders"（40/50 判为"设计对了"） |
| W8 | SSM 里富集的少量突变 | 组合突变库（ACE2 路线 1 个 + 最高亲和 8 个 approach 2 设计）再次酵母展示筛选 | 结合浓度下探至 20 pM（"screened for binding to the RBD at concentrations down to 20 pM"） | "Each library converged on a small number of closely related sequences"→ 每个设计定 1 条：AHB2 + LCB1–LCB8 |
| W9 | AHB2、LCB1–LCB8 | E. coli 表达纯化 → BLI/CD/蛋白酶耐受/室温稳定性 | 原文口径：可测 Kd 区间、Tm>90°C 视为合格 | "For seven of the designs, the dissociation constant ( K d ) values ranged from 1 to 20 nM"；LCB1/LCB3 低于 1 nM 不可测 |
| W10 | LCB1/LCB3 + 刺突三聚体 | cryo-EM 制样解析 | 分辨率判据：全局 2.7/3.1 Å；界面用 focused classification + local refinement 到 3.1/3.5 Å | "show that the overall binding modes closely match the design models with backbone Cα root mean square deviation of 1.27 and 1.9 Å for LCB1 and LCB3, respectively"；埋藏面积 "Both LCB1 and LCB3 form multiple hydrogen bonds and salt bridges with the RBD with buried surface areas of ~1 000 and ~800 Å 2 , respectively" |
| W11 | 纯化 minibinder + 100 FFU 活病毒 | Vero E6 空斑减少中和（FRNT），含流感 minibinder 阴性对照 | 每剂 2 重复、2 独立实验 | "AHB1 and AHB2 strongly neutralized SARS-CoV-2 (IC 50 of 35 and 15.5 nM, respectively), whereas a control influenza minibinder showed no neutralization activity"；"We observed even more potent neutralization of SARS-CoV-2 by LCB1 and LCB3 with IC 50 values of 23.54 and 48.1 pM, respectively, within a factor of three of the most potent anti-SARS-CoV-2 monoclonal antibody described to date"（加大孵育体积可到 11 pM） |

## 4. 关键数字台账（全部可在本地全文搜到）

| 数值 | 含义 | 出处（见 §2/§3 原句） |
|---|---|---|
| 3 / 105 | 分选富集后 NGS 鉴定的设计数（approach 1 / approach 2） | "Deep sequencing identified three ACE2 helix scaffolded designs" / "and 105 de novo interface designs" |
| 12/105（11.4%） | E. coli 表达成功数 | "12 of the de novo designs were expressed" |
| 11/12（91.7%）＝表达后结合率；**绝对 11/105＝10.5%** | BLI 结合 | "11 of the 12 de novo designs were soluble and bound RBD"。**禁止写成"设计成功率约 90%"**：分母是表达者，且 105 已是 FACS 富集后集合 |
| 100 nM–2 μM | 初始结合体 BLI 亲和力区间 | 同上句 |
| ~1 nM / 10 条追加 | AHB1 成熟亲和力；为救热稳定性追加的设计数 | §2.2 |
| 50 个 SSM；40/50 保守 | 全域单点突变库覆盖数；界面+核心保守数 | "For 50 of the minibinders made by using approach 2"；"40 out of the 50 approach 2 minibinders" |
| 20 pM | 组合库筛选的最低 RBD 浓度 | "screened for binding to the RBD at concentrations down to 20 pM" |
| 1+8 个组合库；AHB2/LCB1–LCB8 | 组合优化覆盖的设计 | "the ACE2-based design and the eight highest-affinity approach 2 designs" |
| 7 个 1–20 nM；2 个 <1 nM | 纯化 BLI 终值 | §3 W9 |
| >90°C；14 天室温；5 pM+蛋白酶 | 热稳定性/存放稳定性/表面法亲和力 | §2.3 |
| 2.7 / 3.1 Å；3.1 / 3.5 Å | cryo-EM 全局 / 局部精修分辨率 | §3 W10 |
| 1.27 / 1.9 Å；~1 000 / ~800 Å² | LCB1/LCB3 设计-实验骨架 Cα RMSD；埋藏面积 | §3 W10 |
| 35 / 15.5 nM；23.54 / 48.1 pM；11 pM | AHB1/AHB2；LCB1/LCB3；加大孵育体积后的 IC50 | §3 W11 |
| 10 个设计、100 pM–10 nM、IC50 24 pM–35 nM | 摘要级最终成果口径 | "Ten designs bound the RBD, with affinities ranging from 100 picomolar to 10 nanomolar, and blocked SARS-CoV-2 infection of Vero E6 cells with median inhibitory concentration (IC 50 ) values between 24 picomolar and 35 nanomolar." |
| 56 / 64 残基；0.16 ng/mL | LCB1/LCB3 大小；最强者按质量的 IC50 | "The most potent, with new binding modes, are 56- and 64-residue proteins (IC 50 ~ 0.16 nanograms per milliliter)." |
| 5% 分子量 / 20 倍位点 / 6 倍效价 | 对全长抗体的按摩尔替代优势 | "The designs have only 5% the molecular weight of a full antibody molecule, and hence in an equal mass have 20-fold more potential neutralizing sites"；"the designs are sixfold more potent than the best monoclonal antibodies" |
| 计算总库规模、GPU/CPU 成本 | 正文未给出（补充材料未取回） | 未记录（原因：本地正文无该信息） |

## 5. 结论——作者说了什么

1. 两条 de novo 路线 + 实验成熟，得到 10 个 RBD 结合体、最佳 IC50 至 11 pM 级、"The most potent, with new binding modes, are 56- and 64-residue proteins"，且无需哺乳细胞表达、可鼻喷/雾化递送。
2. "These data show that the computational design method can have quite high accuracy."——设计-实验结构一致性（1.27/1.9 Å）证明界面形状与化学互补的**设计本身**已经不是主要问题。
3. 瓶颈在"识别最好的候选 + 找出少量增亲和突变"（§2.6 原句），并提出应把实验产生的大数据喂回 Rosetta 原子模型与机器学习。
4. 时间论：从基因组序列到超亲和力设计应可压缩到数周。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这是一篇"漏斗分母不闭合"的典型样本**：正文能给的最上游一层是 FACS 富集后的 105，计算库规模缺失。任何引用本文命中率的下游综述若不逐层列分母（105→12→11→10→2 个 pM），就必然产生"90% 成功率"这类误读——我们在 CSV 里必须把三层分母都写死。
2. **失败主因层级和 B09 相反**：C01 的最大流失在表达（93/105 未得蛋白），B09 回顾的是结合失败。说明"哪一层流失最狠"随靶/骨架/表达系统而变，漏斗判据必须按流失层配置。
3. **SSM 熵图 = 设计正确性的廉价代理**：40/50 保守意味着"分选富集谱的形状"本身携带了'这个设计按预期界面折叠'的信息——这比任何单一打分更接近真值，因为它用**负样本（耗竭突变）**说话。我们做酶设计验证时可类比：与其只报"命中"，不如把每个构建体的突变耐受图谱做出来，保守核心即"折叠对了"的证据。
4. **作者把最重的结论（"识别才是瓶颈"）放在讨论倒数第二段**，随后其组内三年（B09→C02→C15+）全部围着这句话转——做文献卡时，"作者自认没解决什么"比"作者宣称解决了什么"更能预测下一步。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：需筛选"large sets of computational designs"+多轮实验优化；亲和力成熟靠湿实验穷举；免疫原性仅外推文献。
- 我们读出：① 计算端**零阈值披露**（本地正文连 ddG/SC 的 cutoff 都没有），本文方法学不可仅凭正文复现；② 105 的上游规模未知，导致本文无法回答"计算漏斗整体通过率"；③ 结构验证（cryo-EM）只覆盖 2 个最优设计，其余 8 个结合体无独立结构；④ 中和实验仅 Vero E6 + WA1/2020，变体逃逸留给 C04/C06；⑤ 无 MD/QM，机理层（为什么 11 pM）不在本文证据范围内。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **分层分母台账**（105→12→11→10→2）：我们的筛选漏斗同样必须按"计算候选→可溶表达→化学确认产物→定量活性"逐层列数并各给比率，禁止跨层相乘成"成功率"（本库口径纪律）。
2. **表达失败与结合失败分开记账**：先修表达（C04 用极性点突变救 LCB1 的可表达性即此招），再谈功能判据——对应我们先做可溶/可纯化的构建体工程，别在未表达的候选上浪费 xTB/MD 预算。
3. **正交读数组合替代单点不可测**：Kd 测不动时用"表面法 + 蛋白酶耐受 + 功能中和"三读数——对应我们 LC-MS 之外加放射性/荧光旁证与全长 RNA 环化产物读出。
4. **"识别瓶颈"论**是酶设计侧的同构问题：我们连 105 这一层都没有（无展示通量），因此瓶颈只会更靠前，任何"先大库后筛选"的类比不成立。

**不可迁移（为什么不能照搬）**

1. **酵母展示通量（一轮几万个克隆、20 pM 浓度梯度分选）在产物化学上不存在**：底物氨酰化/环化只能 LC-MS/MS 逐样本，无等价富集步骤；不能把 C01 的漏斗规模当成我们漏斗的期望规模。
2. **"11/12=91.7%"、pM 亲和力、六倍于抗体等数字，与酶活无任何校准关系**：结合≠催化，静态界面≠三步化学事件（中间体→第二底物→副反应）；本库判据标准禁止把 binder 亲和力数字当酶设计成功概率。
3. 本文无计算阈值、无成本统计，**不能作为"物理打分漏斗该设哪些 cutoff"的依据**——那要引 C02/B09 的成文阈值。

## 9. 溯源与自检

- 本地纯文本：`fulltext/C01_PMC7857403_text.txt`（Europe PMC fullTextXML 标签剥离、实体解码、空白折叠，未改写内容）。
- 引句底稿: data/literature_cards/fulltext/C01_PMC7857403_text.txt
- 底稿指针：`sources/cao.md:36–51`；其第 41 行"承 C05 的 84,690 骨架库"为跨论文推断（见 §0），本卡未采用。
- CSV 字段映射：§3 ↔ 候选生成方法/计算筛选判据；§4 ↔ 候选数递减/实验命中率；§8 ↔ 在方法演进链的位置。
- 本卡引句共 16 条，写卡前后均先对本地全文做逐字命中预检（111 条候选 0 缺失），门禁复跑结果见交付回报。

<!--CSV回填
work_type=论文
target=SARS-CoV-2 刺突 RBD（对 ACE2 结合位点的竞争型 minibinder；LCB/AHB 系列）
backbone_generation=approach 1：Rosetta blueprint builder 嵌入 ACE2 螺旋（残基 23–46）；approach 2：RIF docking 自有从头骨架库 + Rosetta 界面序列设计
computational_filters=Rosetta 界面指标（ddG/形状与化学互补，正文仅定性描述，未给数值阈值）；实验侧：FACS 富集+NGS、SSM 熵图保守性、组合库低浓度竞争
thresholds=正文未给数值阈值；实验判据：RBD 结合浓度下探 20 pM、可溶表达、Tm>90°C、Kd<1 nM 视为最强
md_used=否
qm_used=否
experimental_methods=酵母表面展示+FACS+NGS→E. coli 表达纯化→BLI→SSM/组合突变库→CD 热熔→蛋白酶/室温稳定性→cryo-EM（全局+局部精修）→活病毒 FRNT 中和
pipeline_counts=计算库规模正文未报→FACS 富集鉴定 3（approach 1）+105（approach 2）→表达 3+12→结合 1+11（初始 100 nM–2 μM）→SSM 50 个→组合优化定 AHB2+LCB1–LCB8→终 10 个高亲和（100 pM–10 nM）→LCB1/LCB3 cryo-EM 验证
hit_rate=表达 12/105=11.4%；表达者结合 11/12=91.7%（口径：表达后，不是设计成功率）；绝对 11/105=10.5%；SSM 设计正确代理 40/50
best_metric=LCB1 中和 IC50 23.54 pM（加大孵育体积可至 11 pM）、Kd<1 nM 不可精确测；摘要口径 IC50 24 pM–35 nM
cost_or_stat_note=正文未给计算成本与库规模；中和实验 2 独立实验×技术双重复；结构仅 LCB1/LCB3（2.7/3.1 Å 全局，1.27/1.9 Å 设计-实验偏差）
role_in_timeline=曹龙兴博后首篇：物理打分（Rosetta/RIF）时代 binder 设计的天花板与自我否定（"识别最好的候选"才是瓶颈），直接引出 C02（通用化）与 B09（深度学习过滤器）；其 LCB1/LCB3 成为 C04/C05 之外全部 SARS-CoV-2 转化线（C06 多价、C11 等）的母体设计
source_pointer=data/literature_cards/fulltext/C01_PMC7857403_text.txt；sources/cao.md:36-51
CSV回填-->
