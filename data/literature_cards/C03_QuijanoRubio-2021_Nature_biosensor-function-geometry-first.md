# [C03] 模块化、可调的 de novo 蛋白生物传感器——先把"功能几何"定下来，再去找序列

Quijano-Rubio A, Yeh H-W, Park J, Lee H, Langan RA, Boyken SE, Lajoie MJ, Cao L, Chow CM, Miranda MC, Wi J, Hong HJ, Stewart L, Oh B-H, Baker D（华盛顿大学 IPD / KAIST）
Nature 2021，卷 591（issue 7850）· DOI 10.1038/s41586-021-03258-z · PMID 33503651 · PMCID PMC8074680（正式版页码本卡不断言：本地抽取头部与 `sources/cao.md:78` 均记 482–487，见第 0 节）
本卡底稿为 NIHMS 作者手稿版（NIHPA Author Manuscripts, NIHMS1686140）· 全文 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8074680/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C03**（CSV 组标签：曹龙兴组） |
| 作者与通讯 | 第一作者 Quijano-Rubio A，共同一作 Yeh H-W；通讯为 **D. Baker 与 B.-H. Oh**。曹龙兴（Cao L）为第 8 位作者，本文里他的贡献是提供了他自己设计的 RBD 结合蛋白 LCB1（作者贡献原句：`L.C. designed the RBD binder LCB1`；本文第 4 节引作 ref 4 = Cao et al. Science 2020）。**所以这篇的组归属是 Baker/IPD + KAIST，CSV 把它挂在曹龙兴名下是按他参与计算的署名，读的时候要清楚这不是他的通讯工作** |
| 题目/出处 | De novo design of modular and tunable protein biosensors；Nature 2021，卷 591、期 7850；DOI 10.1038/s41586-021-03258-z；PMID 33503651；PMCID PMC8074680；预印本 bioRxiv 10.1101/2020.07.18.206946（PMC7386493）。本地抽取头部记录的页码字段为 `482 487`（与 `sources/cao.md:78` 记的 482–487 一致），本卡照录、不另行断言 |
| 本文取回方式 | NCBI efetch（`db=pmc&id=8074680`）fullTextXML，`batches.tsv` 第 15 行 fetch_note = fallback_ok[ncbi_efetch] |
| 本地底稿①（引句比对用） | `data/literature_cards/fulltext/C03_PMC8074680_text.txt`（82,954 B，2026-10-20 抓取；由 `C03_PMC8074680_fullTextXML.xml` 去标签而得） |
| 底稿性质提醒 | 该 XML 是 **NIHPA Author Manuscripts / NIHMS1686140**（作者接收稿），文件头明写 `pmc-prop-is-real-version no`。也就是说：正文与图注齐备，但**排版版式、部分表格（Table S1–S6）与补充方法正文（Supplementary methods / Supplementary discussion）不在本地**，凡涉及这些的本卡都标「正文未给出」 |
| 对照底稿 | `sources/cao.md` 第 76–89 行（原卡）。本卡纠正它两处：① 原卡「实验验证」栏写了 **酵母展示**，本文全文检索 `yeast` 命中 **0 次**，全部蛋白都是 E. coli 表达 + Ni-NTA/SEC 纯化，没有酵母展示环节；② 原卡「BLI（OTK 生物传感器层）」里的仪器名在本文是 **Octet RED96（ForteBio）**，只有 sCageHA 与 lucCageTrop627/lucCageTrop、lucCageHBVα/lucCageHBV 用了 BLI，其余靠发光 |
| 证据级别 | **全文级**（本卡所有英文引句均可在本地纯文本里逐字命中；见第 9 节） |
| 未取到的部分 | 补充方法（GraftSwitchMover 打分细节、β-strand threading 参数）、Supplementary discussion、Table S1–S6 内容、各图原始数据点。凡引用这些处本卡明写「正文未给阈值」 |

## 1. 这篇到底解决什么（大白话）

生物传感器要「**认得出靶**」和「**变得了信号**」两件事同时成立。天然蛋白开关能做到，但**数量少、每个都不一样**，所以每换一个靶都得重做一遍工程。这篇的做法：不要天然开关，而是拿一个**已经设计好的两态蛋白笼（lucCage）+ 一把钥匙（lucKey）**当底盘，先把「**功能几何**」定死——笼子里那根螺旋锁扣（latch）上，**装一段认靶的模体**，再在**同一段锁扣上固定位置**放纳米荧光素酶的小片段 SmBiT；笼子闭合时这两个位点都被埋住（既认不了靶，也拼不出荧光素酶），笼子张开时两个都露出来，钥匙一结合就把 SmBiT 和钥匙上的 LgBit 拼回酶，发光。于是要不要发光就只取决于三个自由能的不等式，跟靶长什么样**无关**——换个靶只换那段模体，读数方式一模一样。

他们把这套流程反过来用（原来的 LOCKR 开关是「加肽钥匙→触发结合」，这里是「靶结合→触发钥匙结合」），然后一口气演示了 Bcl-2、BoNT/B、IgG1-Fc、Her2、cTnI、抗 HBV 抗体、抗 SARS-CoV-2 M/N 抗体、SARS-CoV-2 RBD 与三聚体 Spike 共 **9 个靶系**；最好的那个（lucCageRBD）LOD **15 pM**，把 lucKey 截短调 K_CK 后动态范围推到 **5300%**。

**本卡要抽出来的东西**：这是一篇「**先定功能几何、再在几何约束下搜序列/位置**」的范例——搜索空间不是十万条序列，而是「模体插在锁扣上哪个螺旋 register」的**十几个位置**，所以每个靶只合成 5–13 条就出结果。代价也在这里：真正把设计变成传感的判据（闭合态确实挡住靶、结合确实换来信号幅度）**没有算**，靠肉眼检查和事后晶体结构，而且结合能（决定 LOD）与耦合效率（决定信号幅度）在文中被反复混用。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **天然开关不可复用，半合成体系又必须海量筛**。原文交代动机："the number of such switches is limited, and engineering them is often challenging as each is different"；已有模块化系统"**usually require considerable screening to find potential candidates due to limited predictability**"。
   → **他们做了什么**：把开关换成一个**自带两个近似等自由能态的设计骨架**（asymmetric LOCKR 的闭/开态），并把「耦合」这件事**只写成热力学不等式**，从而「换靶只换结合模体」："Because the sensor is based purely on thermodynamic coupling of analyte binding to sensor activation, only one target binding domain is required, which simplifies sensor design and allows direct readout in solution"（摘要原句）。
   → **仍留下的代价**：正因为只剩热力学，灵敏度上限被结合能锁死（见第 2.4 条），而信号幅度这件事他们承认模型算不出来（见第 2.5 条）。
2. **SmBiT 在纳米荧光素酶全酶里是 β-strand，而宿主骨架是螺旋束**——构象假设没有依据。原文的处理方式是把假设写出来再实测："SmBiT adopts a β-strand conformation within the luciferase holoenzyme, but we assumed that it could adopt a helical secondary structure in the context of the helical bundle scaffold, since secondary structure can be context dependent"。
   → **应对**：不证结构，改用**穷举 threading + 能量排序 + 实验一票否决**："We sampled different threadings for the two peptide sequences across the latch, selected the lowest energy solutions"，然后"**expressed twelve designs in E. coli**"混 key、加 Bcl-2 看发光；成功的（SmBiT312-Bim339，命名 lucCageBim）留下当基座："operated in reverse can function as a biosensor"。
   → **代价**：这一步没有任何计算判据说「哪个 register 会成」，12 进 1 是纯实验命中；而且基座一旦选定，后面所有靶都继承这个未验证的 α-螺旋假设。
3. **把整蛋白（不是一段肽）塞进锁扣会撑坏笼子**。蛋白结合域比锁扣螺旋长，硬grafting 装不下。
   → **应对**：三件工具叠加——① 只取「**界面主二级结构片段**」而不整段插："the main secondary structure element segment forming the interface of the binding protein domain with the target was identified"；② 超长处改用柔性 backbone 建模："we made use of Rosetta Remodel"（原文这一处工具名后夹引文编号 43，后半句 to model the C-terminus extension of lucCage 与前半句之间不能连成一条引句）；③ 故意破坏锁扣刚性："three consecutive residues on the latch were intentionally substituted with glycine to allow for conformational freedom"，并换用截短稳定版骨架 sCage。
   → **并且他们做了一件别的设计论文少做的事：拿晶体结构回头验证「功能几何」是否真的成立**——"**Two of five designs were functional, and bound HA in the presence but not the absence of key**"（注意判据方向：只有加 key 才结合，才算传感器，只算 binder 不算传感器），随后解析 sCageHA_267-1S（"**determined to 2.0 Å resolution**"，PDB 7CBC），"**showed that all HA-binding interface residues except one (F273) interact with the cage domain (blocking binding of the latch to the target) as intended by design**"。
   → **代价**：9 个靶系里只有 1 个设计有晶体结构；其余靶的「闭合态挡住了靶」这一步**从未被直接观测**，只是从「不加 key 就不发光」反推。图注还留下反面细节：F273 反而暴露在外、"the Y287 hydroxyl group is buried in the apolar environment"——几何意图与实际结构之间仍有未被修补的偏差。
4. **LOD 撞到结合能的天花板上，临床靶做不到**。cTnI 的诊断浓度窗在低 pM，而他们的传感器检出下限被 latch–靶亲和力定死："was able to detect cTnI but not at sufficiently low levels for clinical use because the rule-in and rule-out levels of cTnI assay for diagnosis of AMI in patients are in the low pM range"。
   → **应对**：**不动开关、只加结合能**。先重申模型给出的标度律："the limit of detection (LOD) of our sensor platform is about 0.1 x K d of the latch-target affinity"，据此"**we further increased the affinity of our sensor to cTnI by fusing cTnC to its terminus**"，结果"**lucCageTrop showed 7-fold higher affinity to cTnI than lucCageTrop627**"，得到"**has a single-digit pM LOD suitable for quantification of clinical samples**"。同一逻辑在 HBV 上第二次使用："a second copy of the peptide was introduced at the end of the latch to increase latch affinity with the bivalent antibody"，LOD 从 ~2 nM 降到 260 pM。
   → **代价**：这条链把「传感」压缩成「**一个带发光读数的结合实验**」：改善灵敏度的唯一旋钮是提高 ΔG_LT（换更强 binder、加二价），而不是提高耦合效率；图注直接这么写——"Higher binding affinity leads to improved dynamic range and sensitivity of the sensor"。凡是耦合本身坏掉的靶，这个旋钮就没用了（见第 2.5 条）。
5. **实测信号幅度系统性低于热力学模型预测——也就是「结合了但没换成信号」**。作者明写："there is considerable variation between different sensors in the level of activation at saturating target concentrations or high lucKey concentrations, which for most is lower than that expected for the complete luciferase reconstitution predicted by the model"。最刺眼的单例是同一个 lucCageRBD 对单体 RBD 与三聚体 Spike：Spike 亲合力更高，信号反而做不满——"**In the presence of spike protein, the same sensor was unable to yield the maximal bioluminescent signal, suggesting the effect of factors not captured by the simulations such as steric hindrance against complete luciferase reconstitution**"。
   → **应对**：给出一条几何解释并**提出但没做**修法："This may be a consequence of steric interference between target binding to the latch and luciferase reconstitution as the target binding motif and the luciferase SmBiT are adjacent to each other in the latch" ——"such interference could be resolved by increasing the separation between the two in the switch"。**这条是本卡最关键的一句话：它承认「结合位点与信号耦合位点的相对排布」本身就是功能判据的一部分，而全文没有为它做任何计算或实验**（没有重新设计一个拉开间距的版本）。→ **本文未解决**：他们只补了两件间接控制——换短 lucKey 调 K_CK（"**We further increased the dynamic range of lucCageRBD to 5300% by using a short version of lucKey to tune K CK**"）和降低 lucKey 浓度（"Decreasing lucKey concentration increases the dynamic range of lucCageRBD due to reduced background signal, but with accompanying reduced maximum bioluminescence signal"，即动态范围与绝对亮度之间换），并在 Table S4 里逐传感器记录偏差。
6. **背景与信号是一对反向约束，K_open/K_CK 必须同时调**。模型模拟的结论写成了对称的两句话："too tight cage-latch interaction results in low signal in the presence of target, and too weak an interaction results in high background in the absence of target"；而调这两个量的手段**是经验突变而不是计算**——沿用 Langan 2019 的 I328S / L345S（图注："I328S and L345S indicate mutations introduced to tune the latch-cage interface"）与截短 helix。图注里给 K_open 的定位："K open exerts a predominant effect on the dynamic range, while K CK provides an additional one-order of tunability"。
   → **代价**：本文没有为任何一个具体设计**算出** K_open 或 K_CK 的数值；最后解释 lucCageRBD 为什么好用时是事后归因——"the near optimal K open value results in a very low background in the absence of target without compromising the extent of activation at low target concentrations"（这个「near optimal」既没测也没算，见第 7 节）。
7. **生物基质吃掉绝对亮度**。血清/模拟鼻拭子矩阵里绝对发光强度与动力学都变："Absolute bioluminescence intensities and the emission kinetics were different across the matrices due to matrix inhibition effect and substrate turnover"。
   → **应对**：接受同行建议引入 BRET 内参做比值读数（"we controlled for variation in absolute luminescence signal in spiked serum samples from four different donors and spiked simulated nasal matrix using a BRET internal reference"；结果句"found that with such calibration the RBD could be accurately quantified without compromising sensor dynamic range"——两句之间原文夹了引文编号 39 与 40，故拆成两条），用 Antares2 双通道光谱解混，常数预标（"The constant f for Antares2 was consistently determined to be 0.43"），得到 "calibration with Antares2 resulted in stable ratiometric signals"。
   → **代价**：他们同时承认**报告原始比值会伤动态范围**——"Reporting the raw ratio (T 470 /T 590 ) as a function of the RBD concentration compromises the sensor dynamic range"，也就是说这个补救本身要在通道串扰上再付一次费。
8. **筛选通量与统计口径很薄**。多处图注是单次实验："Each experiment was performed once"（sCageHA 的 BLI 验证）、"This experiment was performed using single replicates in two independent instances"（Fc、Her2、cTnT）；统计分析自陈："No statistical methods were used to pre-determine the sample size"，并且"no blinding was employed"。
   → **应对**：以「跨批次重复」替代统计功效："Results were successfully reproduced using different batches of pure proteins on different days"；特异性用互靶矩阵兜住——"Each sensor responded rapidly and sensitively to its cognate target, but not to any of the others"。
   → **代价**：抗 SARS-CoV-2 抗体的两个传感器其实是用**动物源交叉反应抗体**演示的，不是病人血清；作者自己收口："For robust serological analysis, generation of an expanded set of more sensitive sensors spanning multiple SARS-CoV-2 epitopes recognized will be necessary"——这一条在本文里没有做。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱）

- **骨架**：不自造。直接继承 Langan 2019 的 asymmetric LOCKR（设计好的六/五螺旋束 + 螺旋锁扣，闭态=锁扣 intramolecular 埋进笼内、开态=释放），以及 Boyken/sCage 那类截短稳定版（"optimized to improve stability and facilitate crystallization efforts"）与 Langan 的 I328S / L345S  tuning 突变。**这一步等于把「有两个可用态」当成给定的物理资源，不参与本次设计。**
- **序列/位置搜索**：**GraftSwitchMover**（他们自写的，"a RosettaScripts-based protein design algorithm"），加 RosettaScripts、Rosetta Remodel（柔性 backbone 建模 C 端延伸）、Rosetta FastRelax（能量最小化）、MergePDBMover + PyMOL 2.0（把全长结合域放回收缩上下文里看）。
- **功能模型**：**自写数值模拟**（`model_simulation.py`，公开在 IPD 文件站）解耦合平衡，参数是 K_open、K_LT、K_CK 与两个组分浓度；这是本文真正的「判据发生器」。
- **实验**：E. coli Lemo21(DE3) 可溶表达 + His-tag/镍柱/SEC 纯化；**发光重建**为主读数（Nano-Glo/furimazine，96 孔，pre-equilibrate 60 min）；**BLI（Octet RED96）** 只用于三处（sCageHA 的 ±key 结合、lucCageTrop 系列亲和力、lucCageHBVα/lucCageHBV 的 Kd）；晶体学（SeMet SAD，PHENIX/AutoSol，beamline 5C PAL）出一个结构 7CBC。
- **明确没有用的方法**：全文检索 `molecular dynamics`、`quantum`、`AlphaFold`、`pLDDT`、`deep learning`、`machine learning`、`yeast` **均为 0 次命中**。所以这篇是**物理能量 + 热力学模型 + 小样本人工筛选**时代的方法，没有任何学习类判据、没有任何长时间模拟。

### 工作流程表（A 段=定几何，B 段=找序列/位置，C 段=功能闸口）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| A1 | Langan 2019 asymmetric LOCKR 闭合态模型 + SmBiT114 序列（"The low affinity SmBiT 114 (VTGYRLFEEIL)"）+ Bim 肽 | 用 GraftSwitchMover 把两段肽先后 graft 进 latch，定义「闭合态同时埋住信号片段与结合模体」这个几何 | 采样窗口："The grafting sampling range was assigned between residues 300-330"；筛选方式仅"energy-minimized, visually inspected and selected for subsequent gene synthesis, protein production and biochemical analyses"——**原文未给能量数值阈值** | 用于合成的设计集合（正文"**expressed twelve designs in E. coli**"，ED Fig 2b 记为"**Experimental screening of 11 de novo Bcl-2 sensors**"，两处差 1） |
| A2 | 已定的双态骨架 | 把「要不要发光」写成三条物种自由能关系，作为整套平台的设计宪法 | 无靶时必须成立："in the absence of target (ΔG open - ΔG CK >> 0)"；有靶时："drives latch opening and luciferase reconstitution (ΔG open - ΔG CK - ΔG LT << 0)"；图注版把这句话翻译成位点排布要求："For sensitive but low background analyte detection, ΔG open and ΔG CK must be tuned such that the closed state (species 1) is substantially lower in free energy than the open state (species 6) in the absence of target, but higher in free energy than the open state in the presence of target (species 7)"——**只有符号判据（>>/<<），没有给任何 ΔG 数值目标** | 设计可行域的概念定义；后续 9 个靶系全部沿用同一套参数命名 |
| A3 | A2 的不等式组 | **先算再做**：对耦合平衡做数值模拟，扫 K_open（a、e、f、g）、K_LT（b）、[lucCage]tot:[lucKey]tot（c、d） | 固定基准："K LT and K CK were set to 1 × 10 -3 , 10 -9 M, and 10 -8 M respectively, and the concentration of the sensor components to 10:100 nM"（⚠️这句话给了三个数值但只点名两个常数，图注标题里另外还扫了 K open，本地版里标签与数值的对应关系有歧义，见第 4 节注） | 两条可直接用于设计决策的结论：**"The sensitivity of analyte detection is a function of ΔG LT , with a lower limit of roughly one-tenth the K D for analyte binding"**；以及 K_open 主导动态范围、K_CK 只提供额外一个数量级调幅 |
| B1 | 目标结合模体（肽/表位）序列 | threading：在 latch 上穷举插入位置 | "into all α-helical registers between residues 325-359 of lucCage"（这句的前半是 The amino acid sequence for each sensing domain was grafted using + Rosettascripts，两处之间原文夹引文编号 42，故只引后半）；能量最小化后"visually inspected and typically less than ten designs were selected for subsequent protein production and biochemical characterization" | **每靶 <10 条**（HBV 明确："Following the Rosetta FastRelax protocol, eight designs were selected for protein production"；BoNT/B 9、Her2 7、Fc 6、cTnI 11、RBD 13） |
| B2 | 完整结合蛋白（HB1.9549.2、Bot.0671.2、Protein A 的 C 域、Her2 affibody、LCB1） | 三步压缩成可 grafting 的对象：① "the main secondary structure element segment forming the interface of the binding protein domain with the target was identified"；② 超长时用柔性 backbone 建模工具（原文该句在 "we made use of Rosetta Remodel" 之后夹了引文编号 43 才接 to model the C-terminus extension of lucCage，跨编号不能连引，本卡只引前半句）；③ "MergePDBMover and Pymol 2.0 to align, model and visualize the full-length binding domain in the context of the switch" | 能量最小化用 Rosetta fast relax；再加人眼检查；柔性化补丁："three consecutive residues on the latch were intentionally substituted with glycine to allow for conformational freedom" | sCageHA 5 条、lucCageBot 9 条、lucCageProA 6 条、lucCageHer2 7 条、lucCageRBD 13 条（**总数可数的送测设计 ≥70，最终每靶留 1 个**） |
| C1 | 表达纯化后的每个候选笼 | **第一道功能闸口（这才是真正的筛选判据）**：20 nM cage + 20 nM key，加/不加靶各测发光 | "The designs were screened by measuring bioluminescence signal for each design lucCage at 20 nM mixed with lucKey at 20 nM, in the presence or absence of 200 nM target protein"（cTnI、抗体的筛选用 100 nM；SARS-CoV-2 抗体筛选用 50 nM 笼 + 50 nM key）；发光值归一化成"normalized to 100 in the absence of"靶——**原文未给通过/淘汰的数值 cut-off，靠排序取最优** | 每个靶系取 1 个最优命名（lucCageBim / lucCageBot 349_2S / lucCageProA 351_2S / lucCageHer2 354_2S / lucCageTrop627 / lucCageHBV(HBV344) / lucCageRBDdelta4_348 / lucCageSARS2-M(M3_1-17_334) / -N(N62_369-382_340)） |
| C2 | 同一个候选 | **第二道闸口，只在 sCageHA 上做，也是全文唯一把「结合」与「传感」分开测的地方**：BLI 分别在 ±key 下测对靶的结合 | 判据方向被写成"bound HA in the presence but not the absence of key"；浓度条件"The concentration of the sCages and the key were 1 μM and 2 μM, respectively"；负荷阈值"threshold of 0.5 nm response"。**其余 8 个靶系没有做这道反证**，只用发光正向读数选了设计 | "Two of five designs were functional"（5 进 2）；随后晶体学回溯："showed that all HA-binding interface residues except one (F273) interact with the cage domain (blocking binding of the latch to the target) as intended by design" |
| C3 | 选中的传感器 | 剂量响应曲线 → 提取 EC50 / LOD / 动态范围 | EC50 拟合口径："the top three peak bioluminescence intensities at individual analyte concentrations were averaged, subtracted from blank, and used to fit the sigmoidal 4PL curve"；**LOD 定义式："The LOD was determined as 3×(s.d./S)"**（线性区回归的 s.d. 与斜率）；采集时长 6000–10000 s，多个笼子:钥匙比例（如 1:10、0.5:0.5）平行测 | 每传感器一张 LOD-vs-浓度曲线，用来做灵敏度调谐（改 [lucCage]:[lucKey] 就能平移检出窗） |
| C4 | 卡在 LOD 天花板上的传感器 | 按 A3 的 0.1×K_LT 标度律**只加结合能**：cTnC 融合、二价双表位、换更强 binder | 目标：把 K_LT 推到临床浓度以下 10 倍；实测："lucCageTrop showed 7-fold higher affinity to cTnI than lucCageTrop627"；lucCageHBVα 的 BLI："K d=0.68 nM"对比 lucCageHBV 的"Kd=20 nM" | cTnI：单-digit pM LOD；抗 HBV：LOD **260 pM**、动态范围 **225%**（原 lucCageHBV ~2 nM、~150%） |
| C5 | 信号幅度不足（不是 LOD 不足）的传感器 | 调 K_CK：把 lucKey 截短——"A truncated lucKey (short lucKey), 14 residue shorter than the full-length key at its C-terminus"，以及降低 lucKey 浓度 | 判据来自动态范围与背景：**DR 1700% → 5300%**，且"while the LOD remains the same"；代价写明"with accompanying reduced maximum bioluminescence signal" | lucCageRBD 达到摘要口径"has a limit of detection of 15 pM and a signal over background of over 50-fold" |
| C6 | 最终传感器 | 特异性互靶矩阵 + 真实基质标定 | 条件："Each sensor at 1 nM was incubated with 50 nM of its cognate target (magenta lines) and the targets for the other biosensors (grey lines)"；基质用 Antares2 BRET 内参双通道解混，"The constant f for Antares2 was consistently determined to be 0.43" | 无交叉响应；RBD 在 10% 模拟鼻基质里"LOD was calculated to be 12 pM"，Spike 在 20% 混合血清里"LOD was calculated to be 47 pM" |

**这套流程的骨架值得单独记住（也是本卡的重点）**：**顺序是 A（先定功能几何与自由能不等式）→ B（在几何允许的位置集合里搜序列，每靶只送 <10 条）→ C（用发光一票闸口定生死）**。它与 binder 漏斗的根本差别在于：搜索维度是**「同一个模体插在第几号残基的哪个螺旋 register」**，而不是「十万条序列」——所以库规模从百万掉到几十，而代价是**功能能不能成立完全押在骨架的两态物理是否可靠，以及人眼对几何的检查上**；全篇没有任何一个把「闭合态挡住靶」变成可计算量的判据（A2 只有 >>/<< 符号，B 步只有总能量排序）。

## 4. 关键数字台账

| 数值 | 含义 | 出处（原句片段，均可在第 9 节底稿逐字命中） |
|---|---|---|
| residues 300-330 | 基座构建时 latch 上的 grafting 采样窗口 | "The grafting sampling range was assigned between residues 300-330" |
| residue 312 | 最终 lucCage 基座里 SmBiT 的插入位 | "The best SmBit position on the latch was experimentally determined to be an insertion at residue 312" |
| residues 325-359 | 传感模体 threading 的全部 α-helical register 范围 | "into all α-helical registers between residues 325-359 of lucCage" |
| twelve designs / 11 sensors | Bcl-2 首轮送测数（正文与图注差 1，本卡照录两个说法） | "expressed twelve designs in E. coli" 与 "Experimental screening of 11 de novo Bcl-2 sensors" |
| 2 of 5 | sCageHA 功能命中率（判据：只在有 key 时结合） | "Two of five designs were functional, and bound HA in the presence but not the absence of key" |
| 9 / 6 / 7 / 11 / 8 / 13 | BoNT/B / Fc / Her2 / cTnI / HBV / RBD 各自送测设计数 | "Experimental screening of 9 de novo BoNT/B sensors"、"6 de novo Fc domain sensors"、"7 de novo Her2 sensors"、"designed eleven biosensor candidates by inserting 6 truncated cTnT sequences at different latch positions"、"The best of 8 designs tested"、"Of 13 candidates tested, the best, which we refer to as lucCageRBD" |
| <10（typically） | 每个靶从全部 register 里送进湿实验的设计数上限 | "typically less than ten designs were selected for subsequent protein production and biochemical characterization" |
| ≥70 → 9 | 可数送测设计总数 → 每靶留下 1 个命名传感器（抗 SARS-CoV-2 抗体靶的筛选数原文未给，故为下限） | 上行各句相加；命中器一律取"was selected as the best candidate due to high sensitivity and stability" |
| 20 nM + 20 nM / 200 nM（100 nM） | 一次筛选的笼:钥匙浓度与加/不加靶条件 | "The designs were screened by measuring bioluminescence signal for each design lucCage at 20 nM mixed with lucKey at 20 nM, in the presence or absence of 200 nM target protein" |
| LOD = 3×(s.d./S) | 检出限的定义式（本文唯一的解析阈值公式之一） | "The LOD was determined as 3×(s.d./S)" |
| LOD ≈ 0.1 × K_LT | 模型给出的灵敏度下限标度律（决定 cTnI/HBV 要不要加亲和力） | "the limit of detection (LOD) of our sensor platform is about 0.1 x K d of the latch-target affinity" |
| K_LT 与 K_CK = 1×10^-3 / 10^-9 M / 10^-8 M | 模拟基准值（⚠️原文这一句**两个标签配三个数值**，本地抽取版无法确定谁对应 1×10^-3；按图注小标题顺序推断第一个数是 K open，本卡不下结论） | "K LT and K CK were set to 1 × 10 -3 , 10 -9 M, and 10 -8 M respectively" |
| 10:100 nM | 模拟里 [lucCage]tot:[lucKey]tot 的基准比 | 同上句后半"and the concentration of the sensor components to 10:100 nM" |
| 2.0 Å / 7CBC | 唯一的功能几何结构验证（闭态埋界面残基） | "determined to 2.0 Å resolution"（PDB 7CBC，"Two point mutations (Glu99Tyr and Thr144Tyr) were introduced in an attempt to induce favorable crystal packing interactions"） |
| 3.2 Å | 晶体里 HB1.9549.2 的 N 端螺旋被 latch 挤离位的实测位移（几何意图与实际结构的偏差量级） | "The N-terminal helix of HB1.9549.2 is displaced from the latch helix (⍺6) by 3.2 Å" |
| 15 pM / >1700% → 5300% | lucCageRBD 的 LOD 与动态范围（截短 lucKey 调 K_CK 后） | "15 pM LOD and >1700% dynamic range for the RBD detection"；"We further increased the dynamic range of lucCageRBD to 5300% by using a short version of lucKey to tune K CK" |
| over 50-fold | 摘要里对同一传感器信背比的口径（与正文 1700%/5300% 的关系需读者自行换算，见第 7 节） | "has a limit of detection of 15 pM and a signal over background of over 50-fold" |
| 14 residue | short lucKey 比全长 key 短的残基数 | "A truncated lucKey (short lucKey), 14 residue shorter than the full-length key at its C-terminus" |
| 7-fold / single-digit pM | 融合 cTnC 带来的亲和力提升与最终 cTnI LOD | "lucCageTrop showed 7-fold higher affinity to cTnI than lucCageTrop627"；"has a single-digit pM LOD suitable for quantification of clinical samples" |
| 0.68 nM vs 20 nM；260 pM；225% | 双表位改造前后的抗体 Kd、LOD 与动态范围 | "K d=0.68 nM"对比"Kd=20 nM"；"had a LOD of 260 pM and a dynamic range of 225%" |
| ~150%（lucCageHBV） | HBV 首轮唯一可用设计的信号增幅（对比 lucCageHBVα 的 225%） | "The best of 8 designs tested, lucCageHBV had a ~150% increase in luciferase activity upon addition of the anti-HBV antibody HzKR127-3.2" |
| 2–5 min；~50–70% | 抗体传感器到满信号的时间与动态范围 | "These sensors reached full signal in 2-5 minutes and had a ~50-70% dynamic range in response to low nanomolar amounts of antibodies" |
| 12 pM / 47 pM | 10% 模拟鼻基质里的 RBD LOD；20% 混合血清里的 Spike LOD | "LOD was calculated to be 12 pM"；"LOD was calculated to be 47 pM" |
| f = 0.43 | Antares2 内参在 470/40 nm 与 590/35 nm 间的预标常数 | "The constant f for Antares2 was consistently determined to be 0.43 by either recording the full spectra or from the filter set" |
| ~20 folds | 饱和 RBD 下比值读数的信背比（光谱解混后才保住） | "the dynamic range becomes ~20 folds over the background with ratiometric readouts" |
| 0.5 nm / 1 μM / 2 μM | BLI 的负荷判定阈值与 ±key 实验浓度 | "threshold of 0.5 nm response"；"The concentration of the sCages and the key were 1 μM and 2 μM, respectively" |
| 60 min / 1000 × g / 6000–10000 s | 发光实验的预平衡、离心与采集时长 | "The lucCage and lucKey components were incubated for 60 minutes at RT to enable pre-equilibration" |

（待填）

## 5. 结论——作者说了什么

1. **反向使用 de novo 蛋白开关可以造出「一大类」蛋白生物传感器**，而且模块化的根据是纯热力学耦合（摘要："Because the sensor is based purely on thermodynamic coupling of analyte binding to sensor activation, only one target binding domain is required, which simplifies sensor design and allows direct readout in solution"）。
2. **换靶几乎不需要重新工程**："This enables the incorporation of various binding modalities, including small peptides, globular miniproteins, antibody epitopes and de novo designed binders, to generate sensitive sensors for a wide range of protein targets with little or no optimization"。
3. **灵敏度只由结合自由能决定，与结合的几何细节无关**（讨论里的核心主张）："its sensitivity depends on the free energy change upon the sensing domain binding to the target but not the specific geometry of the binding interaction"。
4. **平台可调**：LOD 由 K_LT 决定（下限约 0.1×K_LT），动态范围由 K_open 主导、K_CK 再给一个数量级；因此改笼/钥浓度、改 key 长度就能把检出窗平移到临床浓度。
5. **实际交付的成绩**：9 个靶系各出一个传感器；cTnI 与抗 HBV 达到"the sub-nanomolar sensitivity necessary to detect clinically relevant concentrations of these molecules"；RBD 传感器"has a limit of detection of 15 pM and a signal over background of over 50-fold"；互靶特异性"Each sensor responded rapidly and sensitively to its cognate target, but not to any of the others"；可直接在溶液里读、免洗、几分钟到满信号。
6. **领域层面的收口**：认为 de novo 设计的能力边界已经从单态推进到多态——"the focus of de novo protein design was on the design of proteins with new structures corresponding to single deep free energy minima"——"our results highlight the progress in the field which now enables more complex multistate systems to be readily generated"；并展望阵列化（"the ability to modularly design sensors with identical readouts for diverse targets could enable quick readout of large numbers of different compounds using an array of hundreds of different sensors"）。
7. **作者自己承认没做到的**：真实激活幅度普遍低于模型预测（第 2.5 条原句）；几何修法（拉开结合模体与 SmBiT 间距）只是"could be resolved"；血清学应用还需更多表位与更灵敏的传感器（"For robust serological analysis, generation of an expanded set of more sensitive sensors spanning multiple SARS-CoV-2 epitopes recognized will be necessary"）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的贡献不是某个传感器，而是「把功能拆成几何 + 自由能符号，再把搜索维度换成插入位置」这件事**。搜索空间是「同一个模体在 latch 上第几个螺旋 register」，所以每靶送测 <10 条就够——**库规模小不是因为序列聪明，是因为功能约束先把自由度吃掉了**。→ 对我们：写清「配体/底物结合位点—催化中心—构象耦合位点」的相对排布要求，应当发生在生成阶段（约束采样），而不是打分阶段（事后筛）。
2. **符号判据（>>/<<）在他们那里是可执行的，因为骨架的两态自由能是别人已经表征过的**（Langan 2019 给过 LOCKR 的开关能级与 I328S/L345S 效果）。他们自己一个 ΔG 数值都没算出来。→ 我们若想照搬「先写不等式再算可行域」，前提是**能拿到一组两态自由能已知的设计骨架**；目前没有，所以不等式只能停在定性。
3. **0.1×K_LT 这条标度律的本质是：报告系统不创造灵敏度，只转读结合能**。他们两次改进灵敏度（cTnC 融合、双表位）都是**在结合侧加钱**，没有一次是在耦合侧加钱。→ 对应我们：读数装置（LC-MS/MS 的灵敏度、内标）不会提高化学转化率，转化率的问题只能在酶本身解。
4. **「结合≠传感」在他们自己的数据里出现，却被讨论段的一句话盖过去**。第 2.5 条的 Spike 亚最大信号、以及 9 靶里只有 1 靶做了 ±key 结合反证，说明「结合得上」和「结合换来信号」是两个独立命题；但讨论里写的是几何无关论。→ 对我们：漏斗里必须给「产物化学确认」与「结合/表达」各设一道**互不代替**的闸口，任何一道过了都不许宣称另一道也过。
5. **他们唯一一次把几何假设拿出来验，是在事后**（7CBC 晶体结构 + 3.2 Å 位移 + F273/Y287 两个不符合设计意图的细节）。也就是说「功能几何」这套方法论的自证，是**一个结构 + 一双人眼**，不是可批量化的判据。→ 我们若声称某个候选满足某种催化几何，必须准备至少一个可以直接看的东西（结构、突变失活、底物依赖的时间进程），否则就是叙事。
6. **9/9 靶都出了一个可用传感器，这个数字不该被引用为方法预测力**：每个靶的结合元件都是**现成的**（Bim 肽、HB1.9549.2、Bot.0671.2、Protein A、affibody、cTnT、PreS1 表位、LCB1），结合侧的难处已由别人的工作解决；本文解决的是「怎么把结合转成信号」。**把最难的一步当前提**，正是这类模块化平台论文的通用结构。

## 7. 局限与失败（作者的 + 我们读出的）

**作者写在文内的**
- 模型系统性高估激活幅度，且原因只到猜测层面（steric interference），提出的几何修法没有做（第 2.5 条）。
- 只有 sCageHA 一个设计有晶体结构验证「闭态挡住靶」；其余靶的闭合态阻断靠「不加 key 不发光」间接推断。
- 抗体传感器用的是**动物源、对 SARS-CoV-1 的交叉反应抗体**做演示（ProSci anti-M pAb、clone 18F629.1 anti-N mAb），不是 COVID-19 病人血清；作者自己说需要扩展表位与灵敏度。
- 全程体外（含 spiked serum / 模拟鼻基质），没有细胞、没有体内、没有临床样本评价；讨论里的 POC 与阵列都是展望。
- 统计口径：无样本量预估、无盲法，多处单次实验（"Each experiment was performed once"、"single replicates in two independent instances"）。

**我们读出的（口径不一致与判据缺口）**
- **同一件事三个数**：摘要给 RBD 传感器"has a limit of detection of 15 pM and a signal over background of over 50-fold"；正文给"15 pM LOD and >1700% dynamic range"（≈17–18× 背景）；ED Fig 10 说截短 key 才把 DR 推到 5300%（≈54×）；ED Fig 11d 在比值读数下又是"~20 folds"。摘要那句 50-fold 到底对应哪一版传感器，本地底稿里没法确定。**引用这篇的性能数字必须指明是哪一版、哪个读数方式。**
- **正文与图注的送测数差 1**（twelve designs vs 11 de novo Bcl-2 sensors），说明漏斗第一级的计数口径本身不严格。
- **模拟基准值那句标签与数值对不上**："K LT and K CK were set to 1 × 10 -3 , 10 -9 M, and 10 -8 M respectively" 给了三个数、点了两个常数名（其中 1×10^-3 无单位、量纲上更像无量纲的 K open）。本地抽取版无法核对，本卡不下结论；若要复用这套模拟参数需要回原文 Supplementary 核对。
- **最可疑的一条结论 = 第 5.3 条「灵敏度与结合几何无关」**。它与本文两个实测（Spike 亚最大信号、以及作者提出的「拉开结合模体与 SmBiT 间距」这一几何修法）自相矛盾：几何对**LOD**也许无关，对**信号能否被产出**明确有关。把「结合能决定灵敏度」与「结合能决定传感器好坏」混为一谈，正是**功能判据被结合判据替代**的地方。
- 次可疑："the near optimal K open value results in a very low background"——K_open 全文没算、没测，用它解释 lucCageRBD 为什么好用属于事后归因。
- 底稿限制：本地是 NIHMS 作者稿（`pmc-prop-is-real-version no`），补充方法（GraftSwitchMover 的具体打分项）与 Table S1–S6 不在本地，因此「能量最小化 + 肉眼检查」里到底有没有未公开的数值阈值，本文无法判断。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **「功能几何先于序列」的顺序本身**（第 6.1 条）。做法：在生成候选前，把「底物/腺苷酸结合位点 — 催化残基群 — 构象或界面耦合位点」三者的相对排布写成**硬性几何约束**（残基对距离区间、朝向、是否同侧），按约束采样，而不是先造一批再事后打分。这不依赖任何学习模型，纯几何即可执行，且能把搜索空间从序列级压到位置级。
2. **「符号不等式 + 便宜模型画可行域」**（A2/A3）。先回答「要什么样的自由能排序，功能才可能成立」，再谈能不能算准。我们的对应物是三步化学事件的排序要求（起始/聚合的相对自由能、竞争副产物路径必须更高），用静态结构 + 简单能量估算就能画出符号层面的可行域。**注意边界：这只规定「什么样的排布值得一试」，不是「酶活有多高」的判据。**
3. **功能闸口必须独立于结合闸口**（C1/C2 的教训）。他们把「±靶才发光」当唯一生死判据，只在一个靶上补做了「±key 才结合」的反证。对我们：把「产物身份（LC-MS/MS 定量产物峰）」与「候选可表达/可纯化/能结合底物」分成两道**互不代替**的闸口，任一通过不得推定另一通过；每个下单批次里固定包含失活对照（关键残基突变）与无酶/无底物对照。
4. **搜索维度换成「位置」以后，实验量级会掉到几十**（每靶 <10 条、总共 ≥70 条）。这给我们一个现实的下单尺度参照：**当我们有可信骨架 + 可信几何约束时，正确动作是少量、位置多样化的构建体，而不是扩量**。这与我们一轮最多 4 个构建体的约束一致。
5. **报告端用内参做比值校准**（Antares2 那一步）是可以直接搬的工程手法：湿实验读数受批次/基质影响时，加一个与功能无关的内标把绝对量转成比值，代价（串扰会吃动态范围）要同时报出来。

**不可迁移（为什么不能照搬）**

1. **他们的「两态骨架」是别人已表征的现成物理资源**（LOCKR 闭/开态、I328S/L345S 调过的界面能）。UAA 合成酶方向没有等价的「已知闭合/开放对」，所以「换靶只换模体」这个模块化前提不成立，**不能把他们的每靶 <10 条当成我们的下单数参考，也不能把 9/9 靶出结果当成我们的成功概率**。
2. **全篇是平衡态自由能，没有过渡态、没有速率**。用 ΔG_open/ΔG_CK/ΔG_LT 这套不等式去判「能不能催化」是类别错误；本文也**没有** MD、**没有** QM，不能为任何「用 MD/QM 判催化」的主张提供命中率或阈值背书（第 3 节工具箱已给全文检索 0 次命中的证据）。
3. **他们的成功判据是二值的（发光上升/不上升）、且读数在均相溶液里几分钟出**。我们的判据是**化学结构身份 + 定量转化率**，通量低、每轮一次。因此「库规模 12 进 1」这类比例在我们这里没有对应物，不许换算成 UAA 的期望命中数。
4. **本文的 LOD 数字（15 pM / 260 pM / 单-digit pM）是分析物检出限，不是亲和力，更不是活性**。它们与 DP2R 的任何酶活口径不同量纲，禁止当作「某法对 UAA 成功率 X%」的输入。
5. **他们的靶每一个都自带现成 binder/表位**（结合侧已被别人解决）。我们的问题里结合侧本身就是未解的一环，所以这篇的方法论只能搬到「几何 + 功能闸口」两层，搬不到「命中率」层。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/C03_PMC8074680_text.txt

- **本卡实际照着写的那一份**：`data/literature_cards/fulltext/C03_PMC8074680_text.txt`（由同目录 `C03_PMC8074680_fullTextXML.xml` 去标签、HTML 实体解码、空白折叠而来；NCBI efetch 通路，非 Europe PMC）。同一论文若另有 Europe PMC 抽取版，句内夹的参考文献编号位置会不同，所以本卡全部引句只对上面这一份负责。
- **抄写纪律**：凡原文两句之间夹参考文献编号（如 `LOCKR actuator 2 operated in reverse`、`Rosetta Remodel 43 to model`、`using Rosettascripts 42 GraftSwitchMover`、`Maarten Merkx 39 , we controlled`、`internal reference 40 for internal calibration`）处，本卡一律拆成两条引句或在括号里说明，不跨编号拼接、不用省略号冒充引句。
- **与登记底稿的核对**：`sources_map.json` 给 C03 登记了 `fulltext/C03_PMC8074680_fullTextXML.xml`、`fulltext/C03_PMC8074680_text.txt`、`sources/cao.md` 三项，本地均存在。对照 `sources/cao.md:76-89` 原卡，本卡纠正两处：**原文没有酵母展示**（全文 `yeast` 检索 0 命中，全部 E. coli 表达），BLI 仪器是 Octet RED96 而非原卡写的「OTK 生物传感器层」；原卡「无 pLDDT/ipTM 类阈值（早于该体系）」一句成立，本卡补充：本文连 Rosetta 能量数值阈值也没给，只有"lowest energy solutions"的相对排序 + 肉眼检查。
- **CSV 字段映射**：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **门禁**：`scripts/verify_literature_cards.py --only "C03" --no-report`（不落盘 selfcheck.txt/rollout_status.tsv，避免覆盖其他代理产物）。本卡引句条数与 PASS/FAIL 以最后一次运行为准，见回报。
- **没有取回的部分**：补充方法与补充讨论正文、Table S1–S6 内容、任何图的原图数据点。凡涉及处本卡均写明「正文未给阈值 / 本地底稿不含」。

<!--CSV回填
work_type=论文（Nature 2021，Baker/IPD + KAIST；曹龙兴为第 8 位作者，贡献是提供其设计的 LCB1）
target=别构两态开关平台 lucCage/lucKey 上集成 9 个靶系：Bcl-2、BoNT/B、人 IgG1-Fc、Her2、cTnI、抗 HBV(PreS1) 抗体、抗 SARS-CoV-2 M/N 抗体、SARS-CoV-2 RBD 与三聚体 Spike；结构验证用流感 HA 结合蛋白 HB1.9549.2 的 sCageHA
backbone_generation=不新造骨架：继承 Langan 2019 asymmetric LOCKR 闭/开两态笼 + 截短稳定版 sCage；自写 RosettaScripts 算法 GraftSwitchMover 把传感模体 graft 进 latch 的指定 α-helical register（长模体用 Rosetta Remodel 建模 C 端延伸、MergePDBMover+PyMOL 放回上下文）；序列侧无深度学习、无 MPNN
computational_filters=热力学符号不等式（无靶时 ΔG_open-ΔG_CK>>0；有靶时 ΔG_open-ΔG_CK-ΔG_LT<<0）；自写耦合平衡数值模拟画 K_open/K_CK 可行域与 LOD 标度律；Rosetta 能量最小化(FastRelax) 的相对排序 lowest energy solutions；界面主二级结构片段识别；肉眼检查（visual inspection）；全文无 pLDDT/ipTM/AF2/DNN 类判据
thresholds=grafting 采样窗口 residues 300-330（基座）与 all α-helical registers 325-359（传感模体）、HBV 在 residues 336 之后每个位置；每靶送测 typically less than ten designs；筛发光条件 20 nM cage + 20 nM key ± 200 nM 靶（抗体/cTnI 用 100 nM，抗 SARS-CoV-2 抗体筛选 50 nM）；LOD=3×(s.d./S)；模型标度律 LOD≈0.1×K_LT；模拟基准 K_LT/K_CK 记为 1×10-3 / 10-9 M / 10-8 M（原文标签与数值对应存歧义）且 [lucCage]:[lucKey]=10:100 nM；BLI 负荷阈值 0.5 nm；Rosetta 能量与闭态阻断均无绝对数值阈值
md_used=否（全文检索 molecular dynamics 0 次命中；无任何长时间模拟，机理层只有平衡态热力学模型与自写数值模拟）
qm_used=否（全文检索 quantum 0 次命中）
experimental_methods=E. coli Lemo21(DE3) 表达 + His-tag/镍柱 + SEC 纯化；均相生物发光重建读数（Nano-Glo/furimazine，96 孔，pre-equilibrate 60 min，6000-10000 s 动力学，Synergy Neo2）；系列稀释靶拟合 sigmoidal 4PL 取 EC50、线性回归取 LOD；BLI（Octet RED96，链霉亲和芯片）做 ±key 结合反证与 Kd；X 射线晶体学（SeMet SAD，PHENIX，7CBC，2.0 Å）；Antares2 BRET 双通道比值内参标定血清/模拟鼻基质
pipeline_counts=可数的送测设计 ≥70（Bcl-2 12 或 11、sCageHA 5、BoNT/B 9、Fc 6、Her2 7、cTnI 11、HBV 8、RBD 13；抗 SARS-CoV-2 抗体靶的筛选数原文未给）→ 每靶留 1 个命名传感器（共 9）→ 再优化版 2 个（lucCageTrop 由 cTnC 融合、lucCageHBVα 由双表位、lucCageRBD 由短 lucKey）；sCageHA 功能命中 2/5
hit_rate=作者未报整库命中率；可复算的部分：sCageHA 功能命中 2 of 5，其余靶系均为「N 进 1」（12/11 进 1、9 进 1、8 进 1、13 进 1 等）；改进前后灵敏度：cTnI 单-digit pM LOD（Kd 提升 7-fold）、抗 HBV LOD ~2 nM→260 pM（Kd 20 nM→0.68 nM）、RBD LOD 15 pM 且 DR 1700%→5300%（改 K_CK，LOD 不变）；无交叉响应（互靶矩阵）
best_metric=未记录（本文只给 LOD/EC50/动态范围与 BLI 的 Kd：lucCageHBVα Kd=0.68 nM；分析物检出限 RBD 15 pM（缓冲液）、12 pM（10% 模拟鼻基质）、Spike 47 pM（20% 混合血清）、cTnI 单-digit pM；未给 catalytic/Kcat 类活性量）
cost_or_stat_note=纯计算成本未报（Rosetta 单点能量+自写数值模拟，无 GPU 计时）；湿实验成本极小：每靶送测 <10 条设计、E. coli 表达即可测；结构验证仅 1 个（7CBC，2.0 Å，需 SeMet 与 E99Y/T144Tyr 两个助结晶突变）；统计口径自陈无样本量预估、无盲法，多处单次实验；代码与设计模型公开于 IPD 文件站（designcode_and_models.zip、model_simulation.py）
role_in_timeline=把 de novo 设计的对象从「单一自由能极小的静态结构」推进到「两个近似等自由能态 + 态间耦合符号判据」的多态装置：功能几何（结合位点与信号耦合位点在锁扣上的相对排布）先行、序列/位置搜索在后，因此库规模从 binder 论文的 1e5-1e6 降到每靶 <10；它是 binder 侧成果（LCB1、Bot.0671.2、HB1.9549.2）被当作现成输入的一步，也是后来刺激响应/配体诱导组装类设计（本项目 C 线）的判据来源；此时还没有 AF2/pAE 类学习闸口
source_pointer=data/literature_cards/fulltext/C03_PMC8074680_text.txt（NCBI efetch fullTextXML，NIHMS1686140 作者稿）+ data/literature_cards/fulltext/C03_PMC8074680_fullTextXML.xml；对照底稿 sources/cao.md:76-89（本卡纠正其酵母展示与仪器名两处）
CSV回填-->
