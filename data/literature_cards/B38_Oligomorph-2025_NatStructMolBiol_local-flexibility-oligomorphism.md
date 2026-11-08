# [B38] 局部柔性驱动寡变体（oligomorphism）——设计好的笼子折成了别的对称性

Khmelinskaia A, Bethel NP, Fatehi F, Mallik BB, … Twarock R, King NP（华盛顿大学 IPD / LMU / York / Utrecht / Scripps）
Nature Structural & Molecular Biology 2025, 32:1050-1060 · DOI 10.1038/s41594-025-01490-z · PMID 40011747 · PMCID PMC12170342
本地文件内的日期串依次为 24 11 2023 / 14 1 2025 / 26 02 2025 / 18 06 2025 / 11 07 2025（抽取时 XML 标签已剥离，故哪个是收稿、哪个是接收本卡不作断言）；正式刊期 32 卷 6 期 1050-1060 页；Change history 记 2025-07-09 补致谢勘误；预印本 bioRxiv 10.1101/2023.10.18.562842（PMC10614843，文件内日期 19 10 2023）
许可 CC BY-NC-ND 4.0 · 全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC12170342/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B38**（组：Baker组） |
| 论文标题 | "Local structural flexibility drives oligomorphism in computationally designed protein assemblies" |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory 登记 fetch_channel=epmc_fulltext） |
| 本地全文 | `data/interim/baker_lit/ft/oligomorph2025.txt`（182 行，PMC12170342 抽取版） |
| 登记底稿（sources_map.json） | 上述全文 + `sources/baker.md` |
| 证据级别 | **全文级**（本卡所有英文引句均可在本地全文里逐字命中；见第 9 节自检） |
| 未取到的部分 | Extended Data Figs. 1-8、Extended Data Table 1、Supplementary Tables 1-3、Fig. 1-6 原图数值、Nature Reporting Summary。凡涉及这些的读数本卡只写正文/表 1/图注里出现的数字，其余明写"正文未给出" |
| 本文性质 | 不是方法学论文，而是**三个已发表设计（KWOCA 18、KWOCA 70、I32-10）的结构事后解剖** + 一个"反向验证"重设计（KWOCA 70 D7） |

## 1. 这篇到底解决什么（一句话）

三个**早已设计好、也确实在自组装**的蛋白纳米颗粒，湿实验拿到的对称性和设计模型不一样（想八面体给出 D2/D3，想二十面体给出 D2/D5，双组分体系给出六种），作者要回答的是：**偏离是随机的塌陷/聚集，还是由亚基内部某一处局部柔性所"限定"的少数几种架构？** 答案是后者——柔性集中在三聚体两结构域之间的 junction/hinge，它使亚基能取多种准对称（quasisymmetric）构象，从而只形成有限几种规整笼；把这一处刚性化重设计，就救回了原本想要的八面体。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **设计阶段用过的常规结构指标，全都看不出这个坑**。AF2 对三个三聚体支架给的**整体平均置信度都非常高**："Overall, AF2 predicted all scaffolds with high confidence"，平均 pLDDT 分别是 93、95、94；DLS 与 SEC 也只报告"均一"——"Dynamic light scattering (DLS) and size-exclusion chromatography (SEC) of the purified proteins"。也就是说**"表征说均一"和"对称性说错了"可以同时为真**。
   → **他们做了什么**：把 pLDDT 从"全链平均"改成**分区比对**，把假定的柔性区（junction / hinge）与 core 区的**每残基均值**分开画："the former present on average lower pLDDT scores"；再叠加**独立于 AF2** 的物理量（Rosetta 计算的溶剂可及面积 SASA 与 average degree，即 10 Å 内邻居残基数）做旁证："the junction and hinge regions appear to be more exposed to solvent and less well embedded in the protein structure than the core regions"。
   → **代价**：这套分区读数是**事后诊断**，没有变成设计前的过滤器；正文也没给"pLDDT 低于多少就算柔性区"的阈值（**原文未给阈值**，只给区域均值±标准差的图）。
2. **柔性体系在冷冻电镜里拿不到高分辨率，而且结果不可复现**。I32-10 最终只得到六个 7-15 Å 的图（表 1 记为 ~10 to 25 Å），作者对流程的处理写得很直白：迭代式 3D 分类、不加对称算符、参考模型由上一轮输出派生，"These initial iterations revealed the additional presence of a diverse set of nanoparticle assembly"；最后一轮 gold-standard 精修前对初始模型做低通滤波，"Maps and particles that did not reach a geometry resembling the symmetrically refined input map at"，而这样做的理由是承认失败："This decision stemmed from a reduced level of confidence due to the system's flexibility,"。
   → **他们做了什么**：①改用**无对称 C1 分类 + 事后按目视几何指定对称群再精修**；②用"按测得的 2D 直径选择性剔除粒子"帮 3D 分类分开不同组装态；③对 I32-10 放弃 MD 快照路线，改用**从设计模型里直接抽两块能引入铰链自由度的刚体**去拟合，"Rigid-body fitting using these building blocks recovered all six of the observed architectures"；④样本制备上也针对聚集做处理（两轮离心 + 100 mM glycine + 冰上再平衡一小时）。
   → **代价**：他们自己承认六个图"很可能只是溶液中结构的**一个子集**"（摘要："six cryo-EM reconstructions for the third likely represent a subset of its solution-phase structures"）；被丢弃的粒子/图没有留账。
3. **不知道柔性来自哪一层**（作者明确列出三个候选来源：三折轴即三聚螺旋束、两折轴即设计的蛋白-蛋白界面、亚基内部两结构域连接处）。
   → **他们做了什么**：对每个三聚体/二聚体 building block **以及它们之间的界面**分别跑 MD，看均方根涨落，发现域本身是刚的——"While the simulations suggest that the individual"——但"large fluctuations between trimer arms were"，微小亚基内涨落在三聚臂末端（正是设计界面所在处）被放大。然后做**反事实对照**：用原始完美对称设计模型的刚体去拟合，"using rigid bodies extracted from the original,"。结论落到亚基内部："the main source of flexibility is not at the"。
   → **代价**：判定用的是"**最少需要几张 MD 快照能拼出该架构**"（KWOCA 18 的 D5/D2 各需 1 与 2 张三聚体快照、2 与 5 张界面快照；KWOCA 70 的 D2/D3 需 4 与 4、5 与 4），这是拟合充分性的代理指标，不是能量判据。
4. **看得见的架构只是被实验采样到的那几个，看不到全景**。
   → **他们做了什么**：把"可能的多面体架构"变成**几何枚举问题**——只允许正则五边形与正方形面，用欧拉公式 2F4+F5=12 列出 8/10/12/14/16/20 三聚体的全部解（其中 F4=1、F5=10 明写不可能成笼），再用两个几何量约束：三聚体三个内角之和 S、界面角 δ（外加把三聚臂扭开的 θ）。前提假设作者自己摊开写了："The key assumption behind our approach was that the geometric features of the most populated species detected by nMS and cryo-EM represent the most energetically favorable conformations of the constituent proteins"。判据即"平均 δ 是否落在实测架构的 δ 区间内"。
   → **代价**：S/δ/θ 的"实测区间"来自分辨率 7-8 Å 的图上拟合出来的模型；把 16-三聚体架构否掉靠的是"θ 至少要增大 119%/148%"这种外推，不是实验。
5. **反向验证只做了体系里的一个、且只有 15 条设计**。
   → **他们做了什么**：用 RFdiffusion + ProteinMPNN 只重构 junction 区，两条路线共 15 条设计进湿实验，"Initial experimental screening of 15 designs" 挑出 KWOCA 70 D7，DLS/SEC 显示粒径回到 19 nm（原 KWOCA 70 是 32 nm），nsEM 二维类别平均出现"清楚的四折投影"。但**判据只有一半站得住**：作者承认 Rosetta 侧没改善——"While Rosetta analysis did not show appreciable differences in the per-residue solvent accessible surface area (SASA) or average degree of the KWOCA 70 D7 junction compared to the original KWOCA 70 design, we did observe an improvement in the average pLDDT such that it was indistinguishable from the core region"。
   → **仍留下的（本文未解决）**：其余 14 条设计的结果正文未逐条交代；没有给 KWOCA 70 D7 的冷冻电镜三维重构或原生质谱（只有 DLS/SEC/nsEM 的低分辨读出）；KWOCA 18 与 I32-10 没有做对应的刚性化重设计；柔性区残基清单在 Extended Data Table 1，正文未列。

## 3. 方法与工作流程（按论文可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **低分辨/溶液态表征**：DLS（UNcle、DynaPro NanoStar、Zetasizer 三种机子）、SEC（Agilent Bio SEC-5 500 Å 用于 KWOCA、1,000 Å 用于 I32-10，Superose 6 Increase 用于 D7）、SAXS（SIBYLS 光源，FOXS 服务器拟合理论模型）、负染电镜 nsEM（Talos L120C / EPFL BioTalos，cryoSPARC v.3.2.0 做 2D 类别平均）。
- **高分辨与质量**：单颗粒冷冻电镜（Talos Arctica 200 kV 用于两个 KWOCA，Glacios 200 kV 用于 I32-10；MotionCor2 + GCTF + cryoSPARC 初始模型 + Relion v.3.0 分类精修）；原生质谱 nMS（Orbitrap Q Exactive UHMR）+ 电荷检测质谱 CDMS + 串联 MS（四极杆-线性离子阱选母离子、HCD 打碎）。
- **计算侧**：AF2 multimer 预测（pLDDT 分区比对）、Rosetta（SASA、average degree，即 10 Å 内邻居残基数、模型放松）、Amber 18/AmberTools18 MD（ff19SB、OPC 水、150 mM NaCl）、Situs v.3.1 `colores` 刚体拟合、几何/多面体枚举（欧拉公式 + CaGe 程序）、RFdiffusion + ProteinMPNN 重设计。
- **没有用的方法**：QM/第一性原理、自由能微扰、结合/催化活性测定；没有把任何打分函数做成"下单前的过滤器"（除 D7 重设计里的小规模筛选）。全文不含酶活或功能读出——**这篇的证据全是结构读出与质量读出**。

### 主流程表

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | 三个已发表设计：KWOCA 18（拟二十面体，一组分）、KWOCA 70（拟八面体，一组分）、I32-10（拟二十面体，三聚体+二聚体两组分） | E. coli（Lemo21(DE3)、pET29b）表达 → Ni-NTA → Superose 6 Increase 10/300 GL 纯化 → DLS + SEC + SAXS + nsEM 四路低分辨表征 | 正文未给量化判定线，按"是否单峰/均一 + 实测粒径 vs 设计模型粒径"对比；每个测量重复至少三次独立实验 | 实测水合直径 **25、32、37 nm**，设计模型预期 **21、13、25 nm**；SEC/DLS 显示"mostly homogeneous"，但三个都不符合设计模型；nsEM 显示 I32-10 明显不均一 |
| S2 | 同一批纯化蛋白 | 找"设计期就能看出柔性"的指标：AF2 multimer 预测三聚体支架，按 **junction/hinge 区 vs core 区**分别算每残基 pLDDT 均值；再算 Rosetta SASA 与 average degree（10 Å 内邻居残基数） | 判据＝**分区对比**而非绝对阈值（原文未给阈值）；佐证方向：SASA 更高 + average degree 更低 ⇒ 欠堆积 | 三支架整体平均 pLDDT **93、95、94**（全部高置信）；junction/hinge 区 pLDDT **平均更低**、更暴露、更浅埋在结构里 |
| S3 | 纯化样品（KWOCA 18 4.93 mg/ml，KWOCA 70 4.58 mg/ml，I32-10 初值 2 mg/ml） | 冷冻制样（Vitrobot Mark IV，T=10 °C、湿度 100%、吸胀 4-7 s；KWOCA 样品制样时先把 0.5 μl 的 0.04 mM lauryl maltose neopentyl glycol 储备液与 3.5 μl 样品混合，再取 3 μl 上样）→ Talos Arctica / Glacios 200 kV 采集 → MotionCor2/GCTF → cryoSPARC 2D 类别平均与初始模型 → **C1 无对称 3D 分类** → 按目视几何指定对称群做 3D 精修 | KWOCA 18：三轮 C1 分类分出两个主类；KWOCA 70：一轮 C1 分类分出两个子集；I32-10：迭代 3D 分类、参考来自上一轮输出，末轮精修前低通滤波，几何不像对称精修输入图的**直接丢弃** | KWOCA 18：1,803 张显微图 → 300,970 粒子 → 45,922 与 22,981，分辨率 **8.0 与 7.1 Å**，D5（**10 个三聚体**）与 D2（**12 个**）。KWOCA 70：2,364 张图 → 360,972 粒子 → 32,790 与 302,683，**7.2 与 7.1 Å**，D2（**12 个**）与 D3（**14 个**）。I32-10：3,381 段视频 → **六张图，7-15 Å**（表 1 记 ~10 to 25，C1），包括预期二十面体（20 三聚体+30 二聚体）、一个四面体（28+42）、三个二面体（26/32/36 三聚体 + 39/48/54 二聚体）与一个低对称环式（30+45），全部属 fullerene 笼系列 |
| S4 | KWOCA 18 与 70 的 SEC 洗脱组分 | 换 150 mM 醋酸铵（pH 8，50 kDa MWCO 超滤）→ 金涂层硼硅毛细管纳电喷雾 → Orbitrap Q Exactive UHMR 原生 MS（去溶剂电压 -75 V，HCD 100-125 V）；CDMS 单独按 mass = m/z × z - z 算单粒子质量；串联 MS 用 150-175 V HCD 打碎选定的母离子 | 判据＝**去卷积后的实测质量与按化学计量算出的质量的偏差** | KWOCA 18：m/z 12,000-16,500 处三种组装体含 **28、30、36 个亚基**，质量 **827、886、1,064 kDa**，"These measured masses are highly consistent with"（偏差 <0.3%）。KWOCA 70：m/z 14,000-18,500 处 **36 与 42 亚基**，**1,137 与 1,327 kDa**，均在 0.1% 内。KWOCA 18 可指认 trimer 到 decamer 的连续分布（单体加/减），KWOCA 70 的中间态亚基数**都是 3 的倍数**（三聚体更稳定）；I32-10 质谱"宽谱无可分辨峰"，未进一步分析 |
| S5 | 三个三聚体/二聚体 building block 及其界面 | Amber18（CUDA）MD：每模型 **4 条并行轨迹 × 240 ns**（2 fs 步长，ff19SB、OPC、150 mM NaCl、1 bar、298 K、非键截断 10 Å）；算每残基均方根涨落与沿序列的分布 | 判据＝涨落幅度与来源定位（域内 / 三折轴 / 两折界面 / junction-hinge） | 每模型累计 **960 ns**；单个域内平均 r.m.s.d. 约 **1 Å**（刚），三聚臂末端（设计界面所在）涨落被放大；界面与 I32-10 二聚体轨迹涨落整体低于三聚体 |
| S6 | MD 轨迹快照 + S3 的冷冻电镜密度图 | Situs `colores` 逐个界面掩膜拟合（快照每 **2 ns** 取一张），按互相关打分，"Snapshots were scored by cross-correlation,"；拼接后用一段 **20 残基螺旋区**的 r.m.s.d. 给相邻三聚/二聚体打分，整笼按拼接区总 r.m.s.d. 排序取最低；最后 Rosetta 3 依密度放松 | 判据＝**拼出该架构所需的不同快照张数**（越少越说明柔性够用），以及对称刚体对照的拟合质量 | KWOCA 18 的 D5/D2 各需 **1 与 2 张三聚体快照 + 2 与 5 张界面快照**；KWOCA 70 的 D2/D3 需 **4 与 4、5 与 4**。用原始对称设计模型的刚体拟合**更差**，出现大错位与立体冲突。I32-10 因分辨率低改走"两块设计刚体（中央三螺旋束 / 二聚体+相邻三聚体两个球状域）"路线，**六个观测架构全部重构成功** |
| S7 | S6 得到的模型 + 欧拉公式枚举的正则五边形/正方形笼 | 用三个几何量描述：S=α+β+γ（三聚体扁平度）、δ（界面角）、θ（三聚臂绕棱的非对称扭转）；从实测模型量出 S 与 δ 的区间，再看 8/10/12/14/16/20 三聚体各架构所需的平均 δ 是否落在区间内 | KWOCA 18 实测 S **278-288°**（设计二十面体单值 **277°**）、KWOCA 70 **305-312°**（设计八面体单值 **318°**）；实测平均 δ：KWOCA 18 **56-60°**、KWOCA 70 **74-79°**；θ 可达范围按冷冻电镜结构估为 **0-20°（KWOCA 18）与 0-12°（KWOCA 70）** | 结论：其余架构的 δ **全部落在实测区间之外**。KWOCA 18 要缩 9° 或扩 3° 才能碰下一个架构；KWOCA 70 要缩 3° 才够到 10-三聚体，16-三聚体在无极端不对称（θ 需比观测上限至少再大 119%/148%）时无法实现 ⇒ **柔性受限，只通向少数规整架构，而非无序聚集或多态** |
| S8 | 假设"把 junction 刚性化就能回收单一对称架构" | 对 KWOCA 70 junction 做两条重设计路线：①只用 ProteinMPNN 重出序列（**48 条**）；②用 RFdiffusion 对 junction（含上下各 5 残基侧翼）做 partial diffusion，**每个定义 24 个骨架**，再对扩散残基+5 侧翼用 ProteinMPNN 出 **每条骨架 48 条序列**；AF2 单序列、无模板、一次 recycle 预测 | 进实验的门槛："the top five designs from approach 1 (KWOCA 70 OG"，且要求 r.m.s.d. < 1 Å | **15 条设计**进湿实验 → **KWOCA 70 D7** 命中：DLS/SEC 粒径 **19 nm**（原 KWOCA 70 为 32 nm），nsEM 二维类别平均出现设计模型式的**四折投影 ⇒ 八面体**；AF2 分区 pLDDT 升到与 core 无法区分，而 Rosetta SASA/average degree **无可见差异** |

**这套流程的骨架值得单独记住**：偏离设计 ≠ 失败噪声——先用**多路低分辨读出**发现"粒径不对"，再用**分区 pLDDT + 独立物理量**定位嫌疑区，再用**MD + 刚体拟合的最少快照数**证明该区柔性足以重建观测架构，再用**几何枚举 + 区间判据**把"还能形成什么"限定成小集合，最后用**只改一处刚性的重设计**做因果闭环。全程是"结构读出 + 质量读出 + 几何可行性"，没有任何功能性/活性判据。

## 4. 关键数字台账（数值 · 含义 · 出处）

| 数值 | 含义 | 出处（原句片段或正文明确定位） |
|---|---|---|
| 25 / 32 / 37 nm | 三个设计实测平均水合直径（KWOCA 18 / 70 / I32-10） | "the measured average hydrodynamic diameter was" |
| 21 / 13 / 25 nm | 设计模型预期的水合直径 | 同上句后半 "than expected from the design models (21," |
| 93 / 95 / 94 | 三支架 AF2 平均 pLDDT（整体高置信） | "Overall, AF2 predicted all scaffolds with high"；括注 "93, 95 and 94 for KWOCA 18, KWOCA 70 and I32-10," |
| 7-8 Å；7-15 Å | KWOCA 的三维重构分辨率；I32-10 六个图的范围 | "revealed that KWOCAs 18 and 70"；"revealing even greater heterogeneity"（两个分辨率数值在同一句群内，因原文紧跟度数/Å 符号而未纳入引句） |
| 8.0/7.1 Å；7.2/7.1 Å；~10 to 25 Å | 表 1 三个样品的最终地图分辨率 | Table 1 Cryo-EM data collection, refinement and validation statistics 的 Map resolution 行（原文含 Å 符号，不作引句；同表 FSC threshold 一行空值，Map resolution range 三列均记 NA） |
| D5=10、D2=12（18）；D2=12、D3=14（70） | 两种实测架构的各含三聚体数 | "KWOCA 18 forms species with D5"；"KWOCA 70 forms species with D2" |
| 20+30；28+42；26/32/36 + 39/48/54；30+45 | I32-10 六架构的三聚体+二聚体计数（均为 fullerene 笼） | "in addition to the originally" |
| 28 / 30 / 36 亚基；827 / 886 / 1,064 kDa | KWOCA 18 原生质谱三种组装体及其去卷积质量 | "three distinct assemblies"；"the acquired masses of these" |
| <0.3%；0.1% | 实测质量与计算质量偏差（18 / 70） | "These measured masses are"（正文括注 <0.3% deviation）；"both within 0.1% of the expected masses for these assembly states" |
| 36 / 42 亚基；1,137 / 1,327 kDa | KWOCA 70 原生质谱两种组装体 | "two different assemblies formed" |
| ~1 Å | MD 中单个结构域的平均 r.m.s.d.（域本身是刚的） | "with average root mean square" |
| 240 ns × 4 = 960 ns | 每模型 MD 时长（累计模拟量） | "the production simulations were" |
| 2 ns；top 100 | 拟合用快照取样间隔 / 互相关进入拼接的候选数 | "snapshots from the production"；"Snapshots were scored by" |
| 20 残基 | 拼接打分所用的螺旋区长度 | "adjacent trimer and dimers were"（原文 "an 20-residue" 如此） |
| 1+2、2+5；4+4、5+4 | 重建 KWOCA 18（D5/D2）与 70（D2/D3）所需三聚体/界面快照张数 | "one and two trimeric and two"；"Modeling the D2 and D3 assemblies of KWOCA 70 required four and four trimeric and five and four interface snapshots, respectively" |
| S = 278-288° vs 277°；305-312° vs 318° | 实测三聚体内角和区间 vs 完美对称设计模型单值 | 正文几何段照录（原文用度数符号，未纳入引句）；对照句："these ranges deviated from the" |
| δ = 56-60° / 74-79° | 实测架构的平均界面角区间（几何枚举的准入带） | 正文几何段（该句以希腊字母 δ 作主语并含度数符号，故不作引句）；同段结论句："fell outside the observed" |
| θ = 0-20° / 0-12° | 由冷冻电镜结构估出的三聚臂扭转可达范围 | "gauged from the cryo-EM structures of each protein"（数值 0-20 与 0-12 在同一句内，原文带度数符号，不入引句） |
| 9° / 3° / 3° | 触及下一架构所需界面角变化量（18 缩/扩，70 缩到 10 三聚体） | "to access the next architectures in the series"；"and no angle was found to" |
| 119% / 148% | 实现 16-三聚体所需扭转角相对观测上限的最小增幅（外推） | "increased by at least 119% for" |
| 2F4 + F5 = 12；6/5/4/3/2/1/0 组解 | 欧拉公式给出的候选笼全集（8/10/12/14/16/20 三聚体；F4=1、F5=10 明写不可能） | "They can be classified using"；枚举清单逐条给出："cube made of eight trimers"、"an assembly with D5 symmetry"、"an assembly with D3 symmetry"、"it is not possible to form an"、"a dodecahedron (icosahedral"（Methods 段，公式符号在原文为斜体下标） |
| 48 / 24 / 48 per backbone | 两条重设计路线的生成规模（序列数 / 骨架数 / 每骨架序列数） | "redesign the sequence only of"；"partial diffusion of the"；两个 48 与 24 的括号数值见 Methods 的 KWOCA 70 redesign 段（原文在工具名后夹参考文献编号，故不整句引用） |
| 15 条 | 送湿实验的设计总数（5 条 OG + 10 条 D） | "Initial experimental screening"；进实验的准入是 r.m.s.d. 上限 1（原文此处带 Å 符号，不作引句）与 "based on highest pLDDT scores" |
| 19 nm vs 32 nm | D7 与原始 KWOCA 70 的水合直径 | "DLS and SEC suggested the" |
| 1,803 / 2,364 / 3,381 | 三个样品的显微图（视频）数 | "The KWOCA 18 dataset comprised"；"For KWOCA 70, we collected"；"A total of 3,381 videos were" |
| 300,970 / 360,972 → 45,922+22,981 / 32,790+302,683 | 进入 3D 的初始粒子数 → 两个最终类别的粒子数 | 正文各段；表 1 行 "Initial particle images (no.)" 与 "Final particle images (no.)" |
| 200 kV；1.15/1.15/1.16 Å；50.1/50.1/60.0 e-/Å2 | 三样品采集条件（表 1；I32-10 方法段另记约 75 e-/Å2） | Table 1 的 Voltage / Pixel size / Electron exposure 三行（原文含 Å 与上标，不作引句）；正文采集段："Nominal exposure magnification" 后接 ×36,000 与像素 1.15 |
| 至少 3 次 | 每个低分辨测量的独立重复数（Fig. 1 图注） | "Each measurement was repeated" |

## 5. 结论——作者说了什么（只写作者的原话所能支撑的）

1. 三个设计都**偏离了设计架构**，但不是乱掉：cryo-EM 与原生质谱给出两个体系各有**两种**规整架构，第三个体系有**六张图**（且"很可能只是溶液中结构的一个子集"）。
2. 柔性的来源被定位到**亚基内部两结构域之间的 junction/hinge**，而不是三折或两折界面："the main source of flexibility"。
3. 亚基内**受约束的**柔性导致"有限几种架构"而非无序聚集："our results indicate that"；"leading to the formation of a"。
4. 这些组装体是**准对称（quasisymmetric）**的：同一 building block 取多种相关但不相同的构象，且"these architectures are symmetrically and morphologically distinct, including several that to our knowledge have not been previously observed in natural protein assemblies"。
5. 因果闭环：只把 junction 刚性化重设计即可**救回设计意图**——"Redesigning the flexible region"（摘要句），正文收口为 "these results support our"。
6. 作者的定位性陈述：这是**该领域第一次可控地把结构柔性纳入设计以得到多种组装结果**之前的空白——"there are currently no computational protein design methods that controllably integrate structural flexibility to achieve multiple assembly outcomes"；并且现行方法"mostly focus on combining"。
7. 展望（作者说的，非本文做的）：柔性笼可能像 clathrin 一样自适应包裹不同尺寸货物，"interactions between such"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **"整体 pLDDT 高"与"组装对称性错"不矛盾，且前者对本次失败完全没有预警力**。三个支架的平均 pLDDT 93-95 都算高置信，问题只在**分区比对**下才露头。→ 对我们的直接含义：任何"用 pLDDT/pTM 之类全局均值给候选放行"的门槛，对**局部柔性/多构象**这类失效模式是结构性失明的；能救的只有"同一分子内部按区域切分比较"，而且本文没给出可用的切分阈值。
2. **对称性/寡聚态的预测能力，本文是靠"事后几何枚举 + 实测区间"实现的，不是靠学习模型**。判断"还能形成什么架构"用的是 S/δ/θ 三个几何量落在不在实测带内，而实测带来自 7-8 Å 的重构。→ 我们若想把"寡聚态能否被预测"做成可判定问题，缺的正是这种**独立于神经网络、且能写出不等式**的判据；AF2 系列在本篇里只做诊断，不做准入。
3. **"最少 MD 快照数能拼出观测架构"实际上是一个柔性充分性的度量**（1/2、2/5、4/4、5/4），并附带一个漂亮的反事实：完美对称刚体拟合更差且有立体冲突。→ 可借鉴的形式是"用**最简模型能否解释观测** + **更刚的假设是否被观测否证**"，这比"分数高即通过"信息量大。
4. **原生质谱是这里唯一能直接数亚基的手段**，而且它给出的信息是"分布 + 质量偏差"，不是"命中率"。质量偏差 <0.3%/0.1% 只证明**指认的化学计量自洽**，不证明那几种架构是全部或主要物种。→ 我们若讨论寡聚态，必须区分"质量谱指认"与"结构重构"两种证据强度，别把二者混成一个结论。
5. **本文的"成功"里没有一条活性数据**。KWOCA 70 D7 的回收只靠 DLS/SEC/nsEM（粒径 + 四折投影），没有 cryo-EM 三维重构、没有质谱。→ 推断：这是**成本/优先级**选择，不是"不需要"；对我们写"合格线"时的启示是——**低分辨读出足以否决，但确认需要更硬的读出**，反之亦然。
6. **15 选 1 不是命中率**。正文只写 "identified KWOCA 70 D7 as"，其余 14 条未逐条报告。→ 不许把 1/15 当"刚性化重设计的成功率"引用，分母与分子的定义都不完整。

## 7. 局限与失败（作者的 + 我们读出的）

- **作者自己承认的**：①I32-10 的六个图只是子集，且"the inconsistency in achieving"；②I32-10 的原生质谱"yielded a broad spectrum with"；③几何枚举建立在"最富物种=最有利构象"这一假设上；④低分辨让 I32-10 的 α 螺旋难以精确对接，只能换更粗的刚体建模；⑤"much"式的开放问题（clathrin 样自适应组装）留给展望而非本文数据。
- **我们读出的**：
  1. 诊断指标全部是**事后**的：分区 pLDDT、SASA、average degree 都没进入设计前的过滤器；只有 D7 重设计里出现了小规模准入（r.m.s.d. < 1 Å、最高 pLDDT、最低 ProteinMPNN 分数）。
  2. 重设计的正面证据只有**一个体系的一个变体**，且 Rosetta 侧无改善——即"柔性区被刚性化"这件事在两套独立指标上**只有一套支持**。
  3. 三个 building block 都是**双域拓扑 + 域间连接**这一类（两个由 helical fusion 加序列重设计拼成，作者明写这可能引入连接处堆积缺陷；一个是天然三聚体支架 1SED，本身含铰链环）。→ 结论对"单域、无融合junction"的支架是否成立，本文没有证据。
  4. 没有任何功能/活性读出，因此"寡变体是缺陷还是可利用特性"在本篇里无法判定，作者也只把它作为设计原则提出。
  5. 全文不含 UAA、酶、催化、底物；没有任何可转移到"酶活"的判据或数字。

## 8. 对 UAA 筛选的迁移判断

**这篇的证据来自哪些读出（先把边界钉死）**：DLS 水合直径、SEC 洗脱峰形、SAXS 曲线与 FOXS 拟合、nsEM 二维类别平均（投影对称性）、单颗粒冷冻电镜三维重构（对称群 + 分辨率 + 粒子数）、原生质谱与电荷检测质谱（亚基数与质量）、串联 MS（中间态分布）、MD 涨落、刚体拟合的快照数、几何量 S/δ/θ 的区间、AF2 分区 pLDDT、Rosetta SASA/average degree。**全部是"结构/组装态/质量"的读出，零个催化或结合活性读出。**

**可迁移（怎么用）**

1. **失败归因的层级拆分**：他们把"设计没实现"拆成三折轴 / 两折界面 / 域间 junction 三个候选源，再各跑 MD 分别看涨落。→ 我们做 UAA 合成酶筛选时，同样要把"预测不符"拆成**独立可测的层级**（折叠/寡聚态/活性位点几何/辅因子或底物通道），每层配一个自己的读出，而不是笼统给低分。
2. **分区比对优于全局均值**：本文明确显示全局 pLDDT 高到 93-95 仍漏判。→ 我们用 AF2/ESM 类置信度时，应加一条纪律：**把活性位点邻域（催化残基及其接触网络）单独统计，与全链均值对比**；只看全链平均即视为未检验。但**不许**因此造一个"分区 pLDDT 低于 X 就淘汰"的数字门槛——本文没有给阈值，我们也没有标定数据。
3. **"更刚的假设被观测否证"这类反事实检验**可以直接搬：对某个候选，先问"若完全按设计模型（刚性/对称）解释观测，会不会出现不可消除的冲突？"——冲突本身即证据。比"分数排个序"更硬。
4. **寡聚态要单独测、不能从结构预测反推**：他们用 SEC（均一但粒径不对）+ 质谱（数亚基）+ 电镜（看对称）三件独立仪器才敢下"寡聚态偏离"的结论。→ 我们若需要知道设计/挑选的构建体的寡聚态，**必须安排独立的寡聚态读出**（SEC-MALS 或 natives MS 类），不能拿 Foldseek/pLDDT/ipTM 的输出当寡聚态证据。

**不可迁移（为什么不能照搬）**

1. **本文没有任何活性判据，其"成功/合格"是结构符合设计意图（octahedral/icosahedral、粒径匹配）。UAA 筛选的门槛是化学事件能否发生（产物身份、辅因子/底物选择性）。二者不可互换**：把"恢复单一对称架构"当作"恢复功能"的代理，在本篇里也不成立（作者没测任何功能）。DP2R 标准禁止把 binder/组装类判据当酶活闸口，本文同理。
2. **δ/S/θ 的"实测区间准入带"是几何可行性判据，不是概率判据**，更不能变成我们的"寡聚态预测成功率"。它的输入是 7-8 Å 的蛋白质笼模型，UAA 合成酶的多聚体系（多为多结构域、带底物通道）不在这套正则五边形/正方形笼的枚举空间里。
3. **"15 条设计里挑出 D7"不能当命中率或成本模型引用**（分母与分子定义不全，其余 14 条未报告）。同样不许把"240 ns × 4 = 960 ns/模型"的 MD 量当作我们 MD 阶段的预算依据——他们的目的是看涨落谱，不是收敛自由能。
4. **对称设计（严格点群 + 刚性 building block）这一整套生成范式与 UAA 酶无对应物**：UAA 合成酶的目标不是自组装笼的对称群，而是活性位点的化学微环境；把"quasisymmetry 提供新的结构空间"迁移成"允许候选有多样寡聚态"没有依据，我们的候选是否必须均一寡聚态应由活性测定决定，不由结构美学决定。
5. 不许从本文导出"某法对 UAA 成功率 X%"之类数字——本文与 UAA 无交集。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/oligomorph2025.txt

- 本卡引句一律照 `data/interim/baker_lit/ft/oligomorph2025.txt`（Europe PMC fullTextXML 抽取版，182 行）逐字复制；核验器把 U+2013/U+2014/U+2212/U+2018-2019/窄空格归一后再比对，因此卡内英文引句里的破折号与撇号按归一后的 ASCII 写法（- 与 '）书写，正文中出现的 U+00B0（°）等非 ASCII 符号**不放进引句**，改在表格里用中文/数字表述并标注"原文用希腊字母 δ/θ/α"。
- 登记底稿共两份（`sources_map.json` 的 B38）：上表全文 + `sources/baker.md`；引句只承诺命中前者，后者仅作行级对照（本卡未从中取引句）。
- 未取到的材料：Extended Data Figs. 1-8、Extended Data Table 1、Supplementary Tables 1-3、Fig. 1-6 原图数值、Reporting Summary；涉及处本卡明写"正文未给出"。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B38" --no-report`，判据＝10 节齐全、§3 工作流程表 ≥3 步、§2 难点 ≥2 条、卡内所有英文引句逐字命中声明底稿、CSV 回填 14 键非空。结果见本轮终端输出（`PASS B38 quotes=N/N`，退出码 0）。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 60 条逐字引句来自许可受限的第三方来源（B38；CC_BY_NC_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（三个已发表设计的结构事后解剖 + 一个刚性化重设计的因果验证；非方法学论文）
target=KWOCA 18（拟二十面体，一组分三聚体）、KWOCA 70（拟八面体，一组分三聚体）、I32-10（拟二十面体，三聚体+二聚体两组分）、KWOCA 70 D7（junction 刚性化重设计变体）
backbone_generation=沿用已发表设计（helical fusion + 序列重设计出 KWOCA；两组分对称对接设计出 I32-10）；新设计部分用 RFdiffusion 对 junction 区做 partial diffusion 出骨架，再用 ProteinMPNN 出序列，AF2 单序列/无模板/一次 recycle 预测
computational_filters=AF2 multimer 的 pLDDT（整体平均 + junction/hinge 与 core 分区比对）；Rosetta 的 SASA 与 average degree（10 Å 内邻居残基数）；MD 每残基均方根涨落；冷冻电镜密度的刚体拟合互相关打分与拼接 r.m.s.d.；几何量 S=α+β+γ、界面角 δ、扭转角 θ 的实测区间准入；重设计选型用 r.m.s.d. 上限 + 最高 pLDDT + 最低 ProteinMPNN 分数
thresholds=MD 域内平均 r.m.s.d. 约 1 Å；快照取样 2 ns、互相关前 100 个拟合进拼接、20 残基螺旋区 r.m.s.d. 打分；实测 S 278-288°（KWOCA 18）/305-312°（KWOCA 70），设计模型单值 277°/318°；实测平均 δ 56-60°/74-79°，θ 可达 0-20°/0-12°；重设计进实验门槛 r.m.s.d. < 1 Å；柔性区 pLDDT 只给分区对比，原文未给阈值
md_used=是（Amber18 ff19SB，每模型 4 条并行轨迹 × 240 ns，累计 960 ns，用于定位涨落来源与提供拟合用结构快照；非自由能/收敛计算）
qm_used=否
experimental_methods=E. coli 表达 + Ni-NTA + Superose 6 凝胶过滤；DLS（UNcle/DynaPro/Zetasizer，10 次重复）；SEC（Bio SEC-5 500 Å 与 1,000 Å、0.35 ml/min）；SAXS（SIBYLS + FOXS 拟合）；负染电镜 + 2D 类别平均（cryoSPARC）；单颗粒冷冻电镜（Talos Arctica/Glacios 200 kV，MotionCor2+GCTF+cryoSPARC+Relion v.3.0，C1 分类后按对称精修）；原生质谱与电荷检测质谱（Orbitrap Q Exactive UHMR）+ 串联 MS（HCD）；完整质量 RP-LC-MS
pipeline_counts=三个设计 → 各自实测：KWOCA 18（1,803 图 / 300,970 粒子 → 45,922+22,981，D5 10 三聚体、D2 12 三聚体，8.0/7.1 Å）、KWOCA 70（2,364 图 / 360,972 粒子 → 32,790+302,683，D2 12、D3 14，7.2/7.1 Å）、I32-10（3,381 段视频 → 六架构 7-15 Å：20+30、28+42、26/32/36+39/48/54、30+45 三聚体+二聚体）；质谱 KWOCA 18 28/30/36 亚基（827/886/1,064 kDa，<0.3%）、KWOCA 70 36/42 亚基（1,137/1,327 kDa，0.1%）；重设计 48 条序列 + 24 骨架 × 48 序列 → 15 条进实验 → 1 条（D7）回收八面体
hit_rate=本文不设命中率口径；唯一"选型"读数为 15 条重设计中报告 KWOCA 70 D7 为 particularly promising，其余 14 条结果正文未逐条交代（不可当成功率引用）
best_metric=未记录（本文无结合/催化活性量度；最接近"最好结果"的读出为 KWOCA 70 D7 的水合直径 19 nm 对原设计 32 nm，以及质谱质量偏差 0.1%）
cost_or_stat_note=MD 960 ns/模型（2 fs 步长、4 并行）；每个低分辨测量独立重复至少三次；冷冻电镜 200 kV、像素 1.15/1.15/1.16 Å、剂量 50.1/50.1/60.0 e-/Å2（I32-10 方法段记约 75）；最终地图分辨率 7.1-8.0 Å（KWOCA）与 7-15 Å（I32-10，表 1 记 ~10 to 25）
role_in_timeline=把 Baker 组"刚性 building block + 严格点群对称"自组装设计范式的偏离事件，转成可诊断问题：确立 junction/hinge 局部柔性是寡变体（oligomorphism）主因、且受限柔性只通向少数规整架构而非无序聚集；给出"分区 pLDDT + 独立物理量 + MD/刚体反事实 + 几何枚举"的事后归因组合，并以单点刚性化重设计完成因果闭环，为后续"可控柔性/准对称组装"设计留出接口
source_pointer=data/interim/baker_lit/ft/oligomorph2025.txt（PMC12170342，Europe PMC fullTextXML 抽取）；对照登记 sources/baker.md；DOI 10.1038/s41594-025-01490-z；NSMB 32:1050-1060
CSV回填-->
