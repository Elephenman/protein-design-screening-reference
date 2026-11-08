# [B39] 静态结构判据看不见的失败：用一个设计的 β-strand 结合蛋白 C34，实测其激发态与功能竞争

Rennella E, Sahtoe D D, Baker D, Kay L E（Toronto 大学分子遗传/生化/化学 + UW 生化/蛋白质设计研究所/HHMI）
PNAS 2023, 120(18): e2303149120 · DOI 10.1073/pnas.2303149120 · PMID 37094170 · PMCID PMC10161014
CC BY-NC-ND 4.0 · https://pmc.ncbi.nlm.nih.gov/articles/PMC10161014/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B39**（组：Baker组） |
| 本文取回方式 | Europe PMC `fullTextXML`（`fetch_channel=epmc_fulltext`、`fetch_url=…/rest/PMC10161014/fullTextXML`，见 `data/literature_cards/inventory.json` 的 B39 记录） |
| 唯一底稿 | `data/interim/baker_lit/ft/confdyn2023.txt`（67,521 B；文件系统时间戳 2026-10-16 19:18。该缓存文件**不在** `data/literature_cards/fetch_log.tsv` 里，抓取日期只能取自时间戳）——`fulltext/` 目录下**没有** B39 的重复抽取版本，故本卡全部引句只对这一份逐字负责 |
| 身份复核 | 文件头串 `PMC10161014`、`10.1073/pnas.2303149120`、`37094170`、标题 `Exploiting conformational dynamics to modulate the function of designed proteins` 与 CSV 行、`inventory.json` 一致（按既往教训：抓回的全文必须核头部身份块） |
| 对照底稿 | `sources/baker.md:511-522`（原卡）；CSV 行原记 `计算筛选判据=无（用 NMR 弛豫色散看见激发态）`、`候选数递减/命中率/最好值=未记录`，本卡把这些空位补成全文数字 |
| 证据级别 | **全文级**（正文 + 图注 + Materials and Methods 全文可读；所有引句均可在本地底稿逐字命中，见第 9 节） |
| 未取到的部分 | SI Appendix（Fig. S1–S13、Table S1–S8）未落地。凡涉及 SI 的数值（逐残基 Δϖ 全表、逐峰结合分数、三位点模型对比表）本卡只转述正文中已写出的部分，并明写正文未给出，仅有正文描述 |

## 1. 这篇到底解决什么（一句话）

一个**已经设计成功、结合态结构完全符合设计预期**的 de novo 蛋白（C34，124 残基，来自 Sahtoe/Baker 2021 那套隔离淀粉样 β-strand/发夹的 α/β 支架家族），对靶肽的亲和力为什么还是上不去？答案是：**它自己 C 末端的 β4 链在游离态会折进自己的结合沟**，于是 apo 态在两个同样低能的闭合构象之间以约 400 s⁻¹ 互换，而这个互换直接与配体结合竞争；他们把这件事**量化成可测的物理量**（交换速率 kex、两态布居比、逐残基化学位移差 Δϖ 及其推定的二级结构、以及 KD 梯度），并证明**当前最强的静态结构预测器（AF2 单序列预测 + pLDDT）对此完全没有预警能力**。最后反过来利用这个动态性，用少量定点突变做出一个**由第二个配体（Abp1p SH3 结构域）远程开关的变构肽结合体**。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **难点：游离态压根测不到——共振被毫秒级交换全部展宽**。原文："preventing the complete assignment of resonances from triple-resonance based experiments"，即使把温度升到 50 °C 也只是改善："Gaps in the secondary structure profile for apo C34 WT are the result of a lack of data due to"。
   → **他们做了什么**：不硬啃 apo 谱，改成**借信号**——用 1:1（各 450 μM）C34–八肽混合样，把高质量、可观测的**结合态当作放大中继**，用 CEST 把游离态的化学位移转移过来（"allowing observation of the resonance positions of the apo form via magnetization transfer"）。
   → **应对后仍留下的代价**：这是"用配体换可见性"，代价是只能拿到**与结合态差异最大的那一个游离态**的位移（他们自己定义 Δϖ max = max(Δϖ AB, Δϖ AC)，得到的 SSP 是 "a hybrid apo state that is maximally distinct from the peptide bound conformation"），B 与 C 两个态各自的完整位移集并没有被分开解出来。

2. **难点：CPMG 给了速率给不了布居**。原文："It is not possible to estimate the relative populations of the interconverting states from these"。
   → **应对**：把 CEST 与 CPMG **联合拟合**到三位点模型（ChemEx 数值积分 Bloch-McConnell），用 k ex, BC 的联合拟合值（~420 s⁻¹）与 CPMG 独立拟合的 ~400 s⁻¹ 互为一致性检验；布居只能给比值 "the best fit suggests that they are similar"（B:C = 1:1.76）。
   → **代价**：作者明写 "Although the populations of states B and C are not very well defined"——**两态布居是本文最软的量化量**，后续所有 β4 自我抑制的定量归因都建立在这个不确定比值上。

3. **难点：模型本身不可分辨**。原文："Further, similar fits are obtained for any three-state model"；同时两个游离态互换太快（"the relatively fast interconversion between them (~400 s −1 )"），使"某一个 apo dip 属于 B 还是 C"无法判定（原文："complicates assignment of a given" 与 "dip unequivocally to either state B or state C" 之间夹着作者给 apo 加的引号，故本卡拆成两条引句）。
   → **应对**：放弃"从拟合里分峰"，改用**湿实验造锚点**——设计三个把交换淬灭掉的突变体（删掉 β4 的 C34 Δβ4、把 β4 改得更像八肽的 C34 E119V 与 C34 E124RE），让每个候选态变成可以单独拿高质量谱去指认的实体，再拿 Δϖ 相关性把 WT 的 B/C 归到具体突变体上（见第 3 节 S6）。
   → **代价**：突变体是模拟态而非真实态，归因靠相关性 + 拓扑合理性；他们自己承认 β4 在 FC1 里到底成不成折叠都无法判定："The dashed C-terminal region for FC1 indicates"。

4. **难点：功能上必须存在的那个态（开口 FO）观测不到，也造不出来**。原文："A third apo state with an open binding pocket"
   → **应对**：用定向突变去**故意破坏** FC1 的形成（在 Δβ4 背景里把 β3 末端的 V106 换成更大的 L，制造与 α3 上 R50/A51 主链的位阻），并配合升温。
   → **结果：失败**——原文："failed, as did increasing the temperature to 50 °C"。本文没有解决如何观测/稳定真正参与结合的那个过渡性构象（**本文未解决**），只是在模型里把它作为必要但不可见的中间态写下。

5. **难点：最强的静态预测器给出高置信度的错误答案**。AF2 单序列预测的 apo C34 四个螺旋与四条链全部高 pLDDT，且形状就是 FC1："Notably, the locations of all four helices and"，而 "There is no indication, based on the model,"。
   → **应对**：他们没有去修 AF2 或加第二个几何判据，而是把结论写成流程主张——"highlighting the importance of experimental data"，并给出未来路线（动态轨迹库 / 低能构象数据库）。
   → **代价**：**本文没有提供可批量执行的替代判据**；pLDDT 之类静态置信度在这里不是阈值调错，而是原则上不可能报警（预测器只输出一个态）。

6. **难点：连亲和力本身都可能被交换污染**。用峰强比算结合分数时，原文警告："because of millisecond-timescale dynamics in apo"。
   → **应对**：加一道内部对照——只保留那些比率能在 15 N CPMG 的 10 与 30 ms 弛豫间隔平面上被重复到误差以内的峰（"we have only selected those peaks for analysis"），并承认 "Not surprisingly, bound/free intensity ratios are"。
   → **代价**：可用于拟合的峰被裁成子集（逐峰表在 SI Appendix , Tables S3–S8，正文未给出用了几个峰、拟合优度）；正文一处内部不一致：图注与正文给 C34 Δβ4 的 KD 是 "~55 μM"，而简化计算段落写 "A simple calculation ( SI"——同一变体两个实验值（55 与 60 μM）。

7. **难点：蛋白在冰箱里就沉**。Methods："Precipitation of the C34"。
   → **应对**：全部实验在 25 °C（apo 指认除外，用 50 °C）、浓度 0.045–1 mM 现用现测；未见额外配方优化。
   → **代价**：本文未解决（正文没有解释沉淀与构象交换的关系，也没有在更低温度或更稀样品上重测）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

**先说清一件事**：本文**不是筛选漏斗**，没有任何先算后下单的闸口——它是对**一个已成设计体**做事后动态审计，再用突变体做正/反验证。下表里的判据全部是**测量与拟合判据**，阈值一律是原文数字。

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | C34 及变体的 15 N/13 C 均匀标记蛋白（M9 + 15 NH 4 Cl + {U- 13 C}D-glucose；Ni-NTA 30 mM 咪唑洗、0.5 M 咪唑洗脱、TEV 切标签、Superdex 75） | 采 apo 与复合物 1 H N - 15 N HSQC；跑 15 N CPMG 弛豫色散 | 两位点交换模型能否拟合出色散；速率是否与蛋白浓度无关（无关 ⇒ 单分子过程） | "a rate of interconversion"；0.5 mM 与 1 mM 两个浓度、每样 16 h、22 个 ν CPMG（33 到 1,000 Hz）、恒定弛豫窗 T = 30 ms |
| S2 | 同一样 | 用 1:1 C34 WT–八肽（各 450 μM，约一半分子处于结合态）采多核 CEST | 一个残基的 CEST 剖面出现**三个 dip** ⇒ 至少两个游离态；dip 位置 = 不可见态的化学位移。CEST 适用下限："so long as the fractional" | 1 H N：5 Hz 场 51 planes/44 h + 10 Hz 场 81 planes/75 h；15 N：5(10) Hz、51(61) planes、~35 h/dataset；13 C α：110 planes/140 h；13 CO：104 planes/150 h；T EX 0.5 s（15 N 为 1 s） |
| S3 | CEST + CPMG 数据 | ChemEx 数值积分 Bloch-McConnell，χ² 最小化，**三位点模型联合拟合**（apo 数据约束 [A] = 0） | 拟合需同时解释 k ex, AB、k ex, AC、k ex, BC；Δϖ 的核种保留阈：|Δϖ max WT | 大于 0.2 ( 1 H N ), 0.6 ( 15 N), 1.2 ( 13 C α ), 1.0 ( 13 CO) ppm | "k ex, AB (= k AB + k BA ) and k"，"while the exchange between the"；布居比 B:C = 1:1.76 |
| S4 | S3 拟合出的 Δϖ max WT 逐残基值 | 反推不可见态位移 ϖ max BC = Δϖ max WT + ϖ A，再用 SSP 程序转成二级结构倾向 | α-helix 判 SSP > 0.5，β-strand 判 SSP < −0.5 | 得到与结合态差别最大的杂合 apo 二级结构；β4 区出现负 13 C α / 13 CO、正 1 H N 位移 ⇒ 这段在结合态里本是无规卷曲（"which is unstructured in the"），却"assumes a β-structure in at" |
| S5 | 三个锁定单构象的突变体：C34 Δβ4（残基 1 to 115）、C34 E119V（β4 = 118 EVRYRVE 124）、C34 E124RE（β4 = 118 EERYRVRE 125） | 逐个采 HSQC / 三共振指认 / 3D NOESY-HSQC（mixing time 150 ms） | 交换被淬灭的判据 = 谱线窄："The NMR spectra of all three"；拓扑靠 1 H α - 1 H N 与 1 H N - 1 H N NOE | 两个闭合态的真实结构：Δβ4 = β1/β2/β3 三链片（β2-β3 平行、β1-β2 反平行）；E119V 与 E124RE = β4 反平行插进 β2–β3 沟内（模拟八肽） |
| S6 | S4 的 Δϖ max WT 与 S5 的 Δϖ Δβ4 / Δϖ E124RE | 算 Δϖ max MUT = max{Δϖ E124RE , Δϖ Δβ4 } 并与 Δϖ max WT 作分段相关 | 分段归属规则：S1–G84 段 Δϖ max WT ~ Δϖ Δβ4；β3 C 端到 C 末端（V110-E124）段 Δϖ max WT ~ Δϖ E124RE | 把 WT 的两个 apo 态 B/C 分别指派为 FC1（≈Δβ4 型）与 FC2（≈E124RE 型）；相关图为 Fig. 4 C |
| S7 | 想用突变逼出开口态 FO | 在 Δβ4 背景里 V106L 制造与 α3 R50/A51 主链位阻（阻止 β3 插进沟）+ 升温到 50 °C | 能否观测到 open 态信号 | **失败**："failed, as did increasing the"；FO 全程未被观测 |
| S8 | apo C34 WT 序列 | 取 AF2 预测结构 + 逐残基 pLDDT 作静态判据的对照 | 原文判读：四螺旋四链均高置信、形状等于 FC1、"There is no indication, based" | 结论：静态预测对这条功能失效路径无预警能力（Fig. 4 D） |
| S9 | 各变体 + 八肽（DVRFQVRE，固相 Fmoc 合成 + RP-HPLC 纯化） | 两个浓度条件（450 μM:450 μM 与 45 μM:450 μM，即 1:10）滴定，逐峰量化结合/游离峰体积比，拟合 KD | 只用比率在 CPMG 10 ms 与 30 ms 平面上可重复的峰 | KD 递增序 "that increase as C34 Δβ4"；独立计算给出 Δβ4 预测 ~90 μM vs 正文实验 60 μM |
| S10 | 亲和最差的 C34 E119V（FC2 稳定株） | 在 β3-β4 loop 中插入 Abp1p 靶肽 Ark1p（两侧 GSSG spacers），做成 C34 E119V β3,4-Ark1p；外加 Abp1p SH3 结构域 | 设计逻辑："the Ark1p peptide would be"；验证 = apo 态 NOE 拓扑仍是 FC2 | 1:1.3 蛋白:SH3 时 "the K D for dissociation of the"（SH3 用量 45/60 μM 或 600 μM，八肽 450 μM） |

## 4. 关键数字台账（全部来自本地底稿，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 124 残基 | 被审计的设计体 C34 链长（预测 4 α + 4 β） | "The 124-residue C34 is one of a" |
| 结合态例外：β4 不形成 | 设计模型与实测几何的唯一偏差 | "with the exception that the" |
| ~400 s⁻¹（25 °C，浓度无关） | apo 两态交换速率 k ex（毫秒尺度） | "with a rate of interconversion" |
| ~420 s⁻¹ / a few s⁻¹ | 三位点联合拟合：两个游离态之间 vs 游离↔结合 | "while the exchange between the" |
| B:C = 1:1.76 | 两个 apo 态的布居比（最佳拟合，作者自承定义不良） | "the best fit suggests that they"，随后给 "(B:C = 1:1.76" |
| 0.5% / several hundred s⁻¹ | CEST 能看见稀有态的布居与速率下限 | "so long as the fractional" |
| ~1% | NMR（相对 cryo-EM 单颗粒）能在生理温度下探测到的最小构象占比 | "with sensitivity to the presence of relatively small percentages (~1%) of conformers that can, nonetheless, assume functional roles" |
| 0.2 / 0.6 / 1.2 / 1.0 ppm | 逐残基 Δϖ max 的核种保留阈（1 H N / 15 N / 13 C α / 13 CO） | "values are larger than 0.2 ( 1" |
| SSP > 0.5 / < -0.5 | 从化学位移推二级结构的判据（helix / strand） | "A residue is considered to be" |
| KD：~55 → ~200 → ~400 → ~8,000 μM | Δβ4 / WT / E124RE / E119V 的八肽亲和力梯度（最差与最好差 ~145 倍） | 第 3 节 S9 引句 |
| ~90 μM（算）vs 60 μM（测） | 同一变体 C34 Δβ4 的两个口径，正文另一处写 ~55 μM | "A simple calculation ( SI" |
| ~10 mM | E119V 的结合被写到第二个数量级（与 ~8,000 μM 同值不同写法） | "or dramatically impaired" |
| ~100 μM，五倍 | 变构体加 SH3 后八肽 KD 与改善倍数（1:1.3 C34:SH3） | "the K D for dissociation of the" |
| SH3–Ark1p K D ~ 1 μM | 二配体模块的既有亲和力（文献 33/36，本文未测） | 正文第 3 节 S10 段落直接给出（本卡未加引号，因底稿此处带参考文献编号） |
| 35–150 h / 数据集 | 多核 CEST 的谱仪时间（15 N ~35 h、1 H N 44 h 与 75 h、13 C α 140 h、13 CO 150 h） | "For the 13 C α (110 planes," |
| 0.5 mM 与 1 mM、各 16 h | CPMG 样品浓度与耗时（用于证明速率与浓度无关） | "15 N CPMG experiments (16 h for" |
| 22 个 ν CPMG，33–1,000 Hz，T = 30 ms | 弛豫色散的采样密度 | "A total of 22 values of v CPMG" |
| 450 μM（1:1）、45 μM vs 450 μM（1:10） | CEST 与 KD 测量的样品配比 | "CEST experiments were recorded" |
| 0.045–1 mM；25 °C（apo 指认 50 °C）；14.1 T 与 18.8 T | 全部样品的浓度/温度/场强范围 | "Samples varied in protein" |
| 150 ms | 3D NOESY-HSQC mixing time（拓扑归属用） | "NOESY-HSQC ( 28 ) experiments" |
| 残基 1 to 115 / 118 EERYRVE 124 / 118 EVRYRVE 124 / 118 EERYRVRE 125 | Δβ4 删除范围与三条 β4 序列改写 | "referred to as C34 Δβ4, residues 1 to 115"；"there is some similarity" |
| 本文不含任何 N→M→K 漏斗计数 | 无计算筛选、无命中率统计 | 见第 3 节首段说明 |

## 5. 结论——作者说了什么

1. **设计的结合蛋白在游离态不是单构象**："establishing that it interconverts between a pair of distinct conformers that compete with binding of the cognate peptide"；两个闭合态 FC1（β2-β3 平行三链片）与 FC2（β4 反平行插进自己的结合沟）以 ~400 s⁻¹ 互换。
2. **这种动态性削弱功能**："The conformational dynamics"；把 FC2 去掉（Δβ4）或稳定 FC2（E119V）分别得到亲和力的两端。
3. **静态预测器看不见它**："These dynamics are in contrast"，且 AF2 形状就是 FC1。
4. **动态性可以被工程化利用**：把观察到的运动 "exploited to develop an allosterically regulated peptide binder whose binding affinity can be controlled through the addition of a second molecule"，实测五倍改善。
5. **对设计流程的主张（展望，不是本文成果）**："There is thus a strong need to"；具体路径点名为 MD 与 NMR："minimum energy molecular"，"The development of databases of"
6. **序列如何编码动态性尚属未知**："robust design strategies that"

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇给出的不是"新筛子"，而是"筛子的失效模式清单"**。可筛选量的形态很清楚（kex、两态布居、逐残基 Δϖ→SSP、KD 梯度），但**每一项都是单样品测量**，不是可批量计算的分数。→ 对我们：动态量在漏斗里只能站在末端（对少数构建体做机制判决），不能站中段（对几百候选做过滤）。
2. **静态几何失败的方式很具体**：C34 的结合态几何是**符合设计**的（除 β4），AF2 的 apo 预测也**高置信度**，两处都没有错——错在"只有一个态"这个前提。这比 B09 的 Type II（界面对不上）更狠：**界面完全对得上，功能仍然被同一条序列自带的另一个构象竞争掉**。→ 我们的失败分法需要第三类：Type III = 折叠对、界面/活性位几何也对，但催化相关构象在布居上被竞争性态压住。
3. **"亲和力下降 ~145 倍"是纯几何判据的盲区的定量刻度**（55 μM 对 8 mM）。这个数字不能外推成"我们漏掉的催化失败也有 145 倍"，但它说明：**用静态结构给一个功能态打分，即使分数很高，也可能对应一个实际上被另一个同能量态严重稀释的功能**。
4. **他们的应对手法值得直接抄：把不可见的态变成可指认的样品**。不是继续调拟合（模型不可分辨），而是设计突变体把某个态单独稳定下来，再回头比对位移。→ 对应我们：机制层应当用**成对构建体**（预测的活性构象锁定株 vs 竞争性构象锁定株 + 失活对照），而不是只跑一个轨迹看几何。
5. **最弱的一环是"用配体换可见性"**（1:1 结合样品的 CEST 中继）。这决定了本方法只能用于**有可用配体、能到几百 μM 且可均匀标记**的体系——我们的多步催化事件没有这种"把产物态加到 450 μM 就看得见酶"的条件（K m 远低于此，且真正的关键态是过渡态类似物而非底物）。
6. **变构那一节其实是本文最有建设性的部分**：他们证明了"把功能做成受第二个分子控制"只需要理解并复用已有的交换，不需要新骨架生成。→ 对我们：若某个设计的催化位点处于少数态，与其把它推成多数态，不如把它设计成**可被外部事件切换**的状态，判据会更清晰（开关比 = 两个条件下的活性比）。

## 7. 局限与失败（作者的 + 我们读出的）

- **作者自陈的**：① 开口态 FO 从未观测到，稳定它的突变与升温均失败，因此"结合如何发生"的通路（FC1/FC2 → FO → 结合态）里最关键的一步是**推论而非观测**；② B/C 两态布居 "not very well defined"；③ 三位点模型不可分辨（三角 vs 线性拟合同等好）；④ FC1 中 β4 是否折叠 "not possible to establish"；⑤ KD 由峰强比得到，而作者自己承认毫秒交换会让该比率失真，只保留了 CPMG 平面可重复的峰；⑥ 同一变体 Δβ4 的 KD 在正文里有两个数（~55 μM 与 60 μM）。
- **我们读出的**：⑦ 全部定量结论建立在**一个设计体、四个变体、一条八肽**上，没有跨靶重复，"设计家族普遍存在这种竞争性 apo 态"仍是外推；⑧ 本文没有计算漏斗，因此对"如何在下单前筛掉这类失败"没有任何实证方案，只有一句展望；⑨ 全文**没有 MD、没有 QM**（MD 只以"应该有用"的措辞出现），所以这篇不能用来支持或否定"用 MD 判催化"；⑩ CEST 的适用窗口（稀有态 ≥0.5%、kex < 几百 s⁻¹）本身就是选择性口径：**更快或更稀的态在这篇的方法学里也是不可见的**，与它批评 AF2 "看不见"是同一种限制的更精细版本。

## 8. 对 UAA 筛选的迁移判断

**正面回答：我们能否只靠静态结构几何判一个多步催化事件？**

**不能——这篇是全项目文献集中最直接的反例（把握度：高，因为它是本文实测结论而非评论）。** 三条理由，每条都有出处：

1. **静态几何可以完全正确而功能仍然失败**。C34 的结合态几何与设计一致、AF2 的 apo 预测高置信度，功能仍被同一条序列的另一个同能量构象竞争掉，亲和力两端差约 145 倍（~55 μM 对 ~8,000 μM）。对多步催化事件，情形只会更糟：静态几何判的是一个**态**，而三步化学（S0 游离 UTP / S1 pppUA / S2 第二枚 ATP 与环化竞争）要求的是**一系列态之间的相对自由能与可达性**——一个少数态催化几何就足以让"总活性"与"几何分"脱钩。
2. **但是"因此要上动态性判据"也不能照搬**。这篇里动态性之所以能量化成可筛选量，靠的是：均匀标记蛋白 0.045–1 mM、单核种 CEST 数据集 35–150 h 谱仪时间、需要一个能加到 450 μM 的高质量配体、以及只能用峰强比的近似亲和力。这是**每个构建体几天到几周的深测**，通量比一个静态几何分低若干个数量级，永远做不了中段筛子。→ 迁移方式：动态量只允许出现在漏斗**末端机制判决**（1–4 个构建体），中段仍用静态几何 + 序列保守性做召回。
3. **本文提供的可迁移"量"，不是方法而是量的种类**：交换速率（kex，毫秒尺度）、态布居比、由位移反推的局部二级结构倾向（SSP 阈值 >0.5 / <-0.5）、以及"把某态单独稳定下来"的突变体对（Δβ4 / E119V / E124RE）+ 由此得到的功能比值。→ 我们可移植的最小版本：把候选催化位点的**构象可及性**当成一个可标注属性（UNKNOWN 也要显式写出），并把"竞争性闭合构象"写进失败归因表；把成对构建体（锁定株 vs 失活株）写进湿实验设计。

**可迁移（怎么用）**

- **失败分型再补一类**：在 B09 的 Type I（不折叠）/Type II（界面错）之外，加 **Type III = 几何对但功能态是少数态**。每个失败候选必须归入某一类，归不进的写 UNKNOWN。
- **用"开关比"而不是"绝对活性"验证机制**：本文的变构实验（KD 五倍改善）示范了如何用一个外部事件把不可见态变成可读信号。我们的等价做法是"加竞争底物/去掉 Mg²⁺/换成失活点突变"这类条件对照，看活性比而不是绝对值。
- **静态置信度不许当充分性证据**：pLDDT/PAE/几何分只可用作召回与排序，凡"结构预测高置信度"不得写成"该候选功能成立"的支撑。

**不可迁移（为什么不能照搬）**

1. **NMR/CEST 的通量与样品门槛**（450 μM 均匀标记、140 h/数据集）在 UAA 场景不可能对几百候选跑；把它写成我们的筛子就是编造通量。
2. **本文的观测量是单一平衡结合的 KD**，不涉及转化数、过渡态或副产物分支；把 55 μM 这类亲和力数字当"催化能力"的证据是范畴错误。
3. **binder 类阈值（pAE_interaction、复合物 RMSD、ipTM）与本文无关**，本文没有用任何计算筛选器，不得把它们的阈值嫁接到动态性判据上。
4. **本文不含 MD/QM，也没有任何命中率统计**，不得用来为"MD 能判催化"或"某法对 UAA 成功率 X%"提供背书或校准。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/confdyn2023.txt

- **底稿唯一性**：`data/literature_cards/fulltext/` 下**没有** B39 的重复抽取版本，本卡全部引句只对 `data/interim/baker_lit/ft/confdyn2023.txt`（67,521 B，Europe PMC PMC10161014 fullTextXML 去标签文本）负责；`sources_map.json` 中 B39 登记的两条底稿即此文件 + `sources/baker.md`。
- 对照底稿行号：`sources/baker.md:511-522`（原卡，其中 `计算筛选判据=无`、`候选数递减/命中率/最好值=未记录`，本卡用全文补齐）；`sources/baker.md:657`（MD 使用统计行，本文归入"用 NMR 而非 MD 抓激发态"）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `阈值数字/成本统计引用/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B39" --no-report` ⇒ **PASS B39 quotes=61/61，退出码 0**（只验本编号、不带共享报告落盘，避免覆盖并行代理的产物）。逐字比对由同一份 `scripts/litcards_text.norm`（NFC + 实体解码 + 引号/破折号统一 + 空白折叠）双侧归一后做子串查找。**首轮曾判出 3 条 MISS**（用同口径的临时比对脚本，在写完第 2、3 节时立刻抓到）：一处把跨引号的两句话连成一条（原文 apo 一词自带英文引号）、一处把正文没有的 assuming 写进引句（原文是 suggesting）、一处把带 SI Appendix 括号的布居比整段引了进来；逐条拆句/改字/去引后，补写第 4–9 节的 30 条新引句一次全命中。
- 写卡过程中另跑了一份临时逐字自检脚本（`A:\AITEMP\check_quotes_B39.py`，只读比对、不写生产产物），交付后已删除。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 47 条逐字引句来自许可受限的第三方来源（B39；CC_BY_NC_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（全文级；PNAS 2023 Research Article，Biophysics and Computational Biology）
target=C34（de novo 设计 α/β β-strand 捕获蛋白，124 残基，Sahtoe/Baker 2021 淀粉样隔离支架家族）+ 其优化八肽配体 DVRFQVRE；改造体 C34 Δβ4 / E119V / E124RE / E119V β3,4-Ark1p + Abp1p SH3 结构域
backbone_generation=无新骨架生成：取既有设计体做定点突变（删除 β4 得残基 1-115；E119V；E124→RE 插入；β3-β4 loop 插 Ark1p 肽配 GSSG spacer），并用 V106L 试逼开口态（失败）
computational_filters=无计算筛选器；判据全部是测量/拟合量：15 N CPMG 弛豫色散两位点拟合、多核 CEST 三位点联合拟合（ChemEx，Bloch-McConnell）、逐残基 Δϖ→SSP 二级结构倾向、3D NOESY 拓扑、峰体积比→KD；AF2（pLDDT）与 Rosetta 模型只作对照，未当闸口
thresholds=kex(B,C) ≈ 400 s⁻¹（CPMG，25 °C）/ ~420 s⁻¹（联合拟合）、kex(A,B)/(A,C) 数 s⁻¹；CEST 可见下限 布居 ≥0.5% 且 kex < 几百 s⁻¹；Δϖ 保留阈 0.2(1HN)/0.6(15N)/1.2(13Cα)/1.0(13CO) ppm；SSP > 0.5 判 α、< -0.5 判 β；KD 只采用在 CPMG 10/30 ms 平面可重复的峰；NMR 布居灵敏度 ~1%
md_used=否（正文仅展望性写 minimum energy molecular dynamics trajectories 可提示须考虑的构象，本文未跑任何 MD）
qm_used=否
experimental_methods=15N/13C 均匀标记 E. coli BL21(DE3) M9 表达 + Ni-NTA/TEV/SEC 纯化；1H-15N HSQC 滴定（1:1 与 1:10）；15N CPMG 弛豫色散；1HN/15N/13Cα/13CO CEST；3D 三共振指认 + NOESY-HSQC(150 ms)；SSP 化学位移二级结构倾向；ChemEx 拟合 KD；八肽 Fmoc 固相合成 + RP-HPLC；BLI/ITC 未使用
pipeline_counts=无 N→M→K 漏斗计数（本文不做设计筛选）；实体数 = 4 个蛋白变体 + 1 条八肽 + 1 个 SH3 结构域；CEST 平面数 51/61/81/104/110，对应谱仪 44/35/75/140/150 h；CPMG 22 个 ν（33–1,000 Hz）、0.5 与 1 mM 各 16 h
hit_rate=未记录（本文不报告设计命中率或筛选命中率；给出的是构象依赖的亲和梯度 KD 55/200/400/8,000 μM，以及变构改造后 ~100 μM、约五倍改善）
best_metric=最优 KD ~55 μM（C34 Δβ4–八肽；正文他处写实验 60 μM、简化计算预测 90 μM）；最弱 ~8,000 μM（E119V，正文亦写 ~10 mM）；变构体加 SH3 后 ~100 μM
cost_or_stat_note=纯实验成本无算力口径：单核种 CEST 数据集 35–150 h 谱仪、CPMG 每样 16 h、样品需 0.045–1 mM 均匀标记（CEST/KD 用 450 μM）；KD 误差以 ±1 SD 表示；两态布居 B:C = 1:1.76 作者自承 not very well defined；蛋白 4 °C 沉淀、50 °C 复溶
role_in_timeline=Baker 设计链中唯一一次对已成设计体做实验态构象动态审计：为 Type II 式失败补出第三类机制（低能激发态与功能位点自竞争，静态几何完全正确仍掉 ~145 倍亲和），并给出 AF2/pLDDT 类静态判据对这类失败无预警能力的直接证据；同时把 MD 与 NMR 定位为"下一步该引入动态性"的工具（本文未实现），末段用动态性做出可被第二配体开关的变构结合体
source_pointer=data/interim/baker_lit/ft/confdyn2023.txt（Europe PMC PMC10161014 fullTextXML 去标签文本，67,521 B，DOI 10.1073/pnas.2303149120 / PMID 37094170）+ sources/baker.md:511-522 与 sources/baker.md:657
CSV回填-->
