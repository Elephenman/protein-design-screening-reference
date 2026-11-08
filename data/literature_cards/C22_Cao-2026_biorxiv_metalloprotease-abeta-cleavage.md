# [C22] de novo 设计锌金属蛋白酶去切 Aβ 的指定肽键——把“催化几何 + 底物序列”一起写成生成条件

Qu Yannan, Wang Chentong, Zhu Hongli, Wang Yanjun, **Cao Longxing（通讯，西湖大学）**
bioRxiv 2026.01.06.697903（Posted 2026-01-06，预印本）· DOI 10.64898/2026.01.06.697903 · EPMC PPR1219681
链接 https://doi.org/10.64898/2026.01.06.697903 · 本地正文抽取 2026-10-20

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C22**（组：曹龙兴组；西湖大学 / Westlake Lab of Life Sciences and Biomedicine） |
| 论文 | De novo design of metalloproteases for targeted amyloid-β cleavage · Qu Y, Wang C, Zhu H, Wang Y, **Cao L（末位通讯）** · bioRxiv 2026.01.06.697903，Posted 2026-01-06 · DOI 10.64898/2026.01.06.697903 · EPMC 编号 PPR1219681 |
| 本文取回方式 | Europe PMC `fullTextXML` 请求回退到 bioRxiv 正文页 HTML（`batches.tsv` 第 58 行 `fetch_note = fallback_ok[biorxiv_full]`），本地落盘 2026-10-20 12:25 |
| 本地全文 | `fulltext/C22_PPR1219681_fullTextXML.xml`（232,495 B，实为 bioRxiv HTML）→ 去标签纯文本 `fulltext/C22_PPR1219681_text.txt`（51,459 B，SHA-256 `8596f085f1a9c551…`） |
| 对照底稿 | `sources/cao.md:351–365`（原卡），本卡在其基础上补：母酶与基序来源（PPEP-1 6r4w / Fungalysin 4k90）、两步封装的实际操作、26 条/组合的送测规模、五个命中酶名单、全套动力学数字（160.8 / 28.4 / 24.3 / 4.2 / 3.8 M⁻¹s⁻¹）、突变体的**方向性**结论、三底物交叉特异性的真实结果 |
| 证据级别 | **全文级（仅正文）**：本卡全部引句均可在本地纯文本里逐字命中（见第 9 节）。**但本地这份正文不含 Methods 章节**——正文写了「(see Methods)」，抽取到的 HTML 里从 Discussion 直接跳到 Code availability 与参考文献，因此协议参数（缓冲液、锌浓度、孵育时长、生成库规模、计算闸口的数值阈值）**本地不可得**，本卡一律写“原文未给阈值”而不是猜 |
| 未取到的部分 | Methods 全文、Extended Data Fig. 1–7 与 Table 1–3 的图/表本体（正文只引用其编号）、任何晶体/低温电镜结构、SPR/BLI、热稳定与锌含量测定。凡引用这些处本卡明写“正文未给出，仅有正文描述” |
| 与登记底稿的分歧 | `sources/cao.md:356` 把「in-silico success / align to a sufficient degree」记为本文筛选器，但该措辞**不在本地正文里**（`grep` 结果：`in silico` 0 次、`sufficiently` 0 次），其自注“见 C23 图注”证实它属于 C23；同理 `-log K_tx` 也不在本文正文。本卡不采纳这两项 |

## 1. 这篇到底解决什么（大白话）

以前的 de novo 酶设计（同组 C08/C23、以及 Baker 组的 Kemp 消除酶、金属水解酶）做成的都是**模型反应**：切一个小而疏水的活化酯，不需要认出“切哪一条键”。这篇要的是**真蛋白酶**——在一条天然多肽（Aβ42）里，只切指定的那一条肽键，相邻序列一律不切。作者把问题定义成：设计一个蛋白，要同时做到三件事——"preserves the strict metal-dependent catalytic geometry, locks the scissile bond into position,"，并承认此前"an objective that has so far remained out of reach"。

做法上最关键的一步跳转：**不再“先造酶再找底物”，而是让生成模型直接把“酶 + 底物 + 锌”作为一个复合物一起生成**，条件是（a）目标肽的氨基酸序列、（b）预先定好的催化基序（三个锌配位残基 + 一个作广义碱的 Glu + 一个组成 oxyanion hole 的 Tyr 或 His）。为的是让“结合”和“催化就位”在同一轮扩散里同时被优化。他们自述这是为了绕开改造天然蛋白酶的死路——天然酶的底物识别摊在柔性环上，改动识别就伤催化。

结果：在 Aβ 上选 3 个切割位点、用两条策略（PP = 保留模板核心只重建结合环；DP = 只拿极简催化基序、骨架全新）造酶，实验验证到 **5 个酶**能在设计位点切开融合底物与全长 Aβ42，最快 4 小时完全降解；相对无催化水解加速 >10⁷ 倍；但绝对 turnover 只有 10⁻⁴ s⁻¹ 量级，比天然酶低几个数量级，且 5 个里只有 1 个（PP507-S1）做到真正只切自己的底物。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **改造天然蛋白酶这条路被判定走不通，于是整篇换靶换策略**。现象/证据：作者开篇就给结论 "Attempts to retarget protease through directed evolution" 与理性突变"have met with limited success"，并给出机理性原因——"substrate specificity is typically distributed across flexible loops that are conformationally"；又说"Exhaustive screening can explore only a minute fraction of sequence space"、"Consequently, conventional sequence redesign seldom retargets these enzymes while maintaining"。 **他们做了什么**：放弃“改造现成酶”，改为从天然酶里**只抠出催化基序**（PP 路线连结合环一起切掉重建；DP 路线只留锌配位 + Glu + oxyanion hole，骨架全新），把特异性问题从“突变哪些残基”转成“重新生成一个夹子的几何”。 **仍留下的代价**：新骨架没有进化压力可借用，turnover 只有 10⁻⁴ s⁻¹；作者自己承认"Although the turnover rates of our designs are lower than those of natural enzymes"。

2. **一步扩散造不出可用的活性位点堆积，改成两步封装**。现象/证据：正文对比 conventional one-step diffusion，指出这类做法"which frequently yield suboptimal packing and limited control over overall enzyme topology"；他们的解法是"we developed a 'two-step encapsulation'"——先围着催化 Glu 生成骨架（把广义碱稳住、把底物"pre-wrapping"一半），再围着 oxyanion hole 生成第二部分把底物封起来。 **他们做了什么**：把一次生成拆成两次带条件生成，换来"clamp-like enzymes"形态与更密的界面堆积。 **仍留下的代价**：**本地正文没有任何数值阈值**（无 RMSD/无位阻能量/无通过率），“两步一定比一步好”只有定性断言 + 下游 5 个命中支撑，无法判断这一步在漏斗里到底淘汰了多少。

3. **Aβ 肽太疏水，常规荧光-淬灭剂短肽底物根本做不出来，动力学测不了**。现象/证据：原文"The intrinsic hydrophobicity of the Aβ target"。 **他们做了什么**：换底物形式——不用化学肽，改用**蛋白级 FRET 传感器**，"we engineered a FRET-based biosensor by inserting"，靠裂解后 FRET 下降读数。 **仍留下的代价（这是本文最硬的内在矛盾）**：传感器把目标序列埋进两个大荧光蛋白之间，作者自己发现读数与降解曲线打架——"The discrepancy observed for DP720-S1-which"。解释是推测（"may be attributable"），**没有做对照实验排除**；也就是说 DP720-S1 的 3.8 M⁻¹s⁻¹ 这个数是可疑值，而全部 kcat/Km 都建立在同一套被怀疑有位阻的体系上。本文未解决。

4. **oxyanion hole 的突变结果与设计意图相反，说明“过渡态稳定”没被证明**。现象/证据：设计时把 Tyr/His 当 oxyanion hole 摆进去，但"Interestingly, in the DP designs,"，H191A 甚至增强降解；作者的解释是"These findings suggest that the oxyanion"。 **他们做了什么**：把结论从“oxyanion hole 必需”退成“第二壳层与 oxyanion hole 通过调 kcat 起作用”，并补测突变体动力学（D126A 的 kcat 三倍、Y91F 的 kcat/Km 两倍、H191A 2.7 倍）。 **仍留下的代价**：催化机制的**直接证据只剩一条**——催化 Glu→Ala 普遍失活；oxyanion hole 这个“过渡态稳定装置”在实验上等于没被证明存在，而全文没有晶体结构、没有 QM、没有 MD，作者也承认"a parameter that remains challenging to"。

5. **PP 策略在 3 个位点里有 2 个全灭，作者给了归因但没验证**。现象/证据："In contrast, the PP strategy generated active"。 **他们做了什么**："We attribute the limited success of the PP"，即模板骨架保得太多、容不下 S2/S3 的序列与几何；应对方式是**换策略**（DP 允许更大构象采样），不是回头修 PP。 **仍留下的代价**：位阻解释没有结构或计算证据支撑，也没有把 PP 的骨架保留比例做成变量重跑；因此“DP 比 PP 好”是**样本量各 26 条的单次比较**，不能当结论推广。

6. **摘要与正文对特异性的说法不一致（本卡认定这是本文最可疑之处）**。摘要写"Experimental characterization validated five"；但正文的三底物交叉实验给出"PP532-S1 displayed broader substrate tolerance,"，"DP622-S2 and DP221-S3 exhibited partial"。 **他们做了什么**：没有撤回摘要口径，而是把特异性归因转成**序列组成解释**（S1 侧翼富大块芳香/亲水残基、S2/S3 侧翼是小脂肪族与 Gly；GS linker 与序列重叠造成交叉）+ 承认要加阴性设计："We anticipate that future"。 **仍留下的代价**：5 个酶中真正单底物特异的只有 1 个；DP221-S3 的 H191A 虽"virtually abolishing cleavage activity toward"，代价却是"the scissile bond shifted"——特异性上去了、位点正确性丢了。本文未解决。

7. **金属配位本身缺少独立于活性的实验判据**。现象/证据：正文只有两点与“金属”直接相关的实验事实——反应必须在锌存在下读（"Upon overnight incubation of"）和 Fig 3a 图注描述"coordination of the zinc ion by"；突变表里动的都是**碱（Glu）、oxyanion hole（His/Tyr）与第二壳层**，即"we mutated the newly generated"。 **他们做了什么**：把金属配位的证据间接化——用第二壳层突变影响活性来旁证配位环境存在。 **仍留下的代价**：本地正文**没有**螯合剂（EDTA/1,10-菲啰啉）敲除-回补实验、没有 ICP-MS 锌计量、没有“三 His→Ala 直接失活”的对照、也没有 apo/holo 结构。因此“这是一个锌蛋白酶、锌是催化必需的”在设计层面仍是**推定而非实测**。本文未解决。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **活性位点构建（本文核心，不是“骨架生成后随便挂个位点”）**：从两个天然锌内肽酶取催化基序——"To establish catalytic motifs"（PPEP-1，PDB 6r4w；Fungalysin，PDB 4k90）。两酶同机制但 oxyanion hole 组成不同："Notably, their oxyanion hole"。基序内容 = **三个锌配位残基 + 广义碱 Glu + oxyanion hole（Tyr 或 His）**。两条路线：
  - **PP（peptide-binding pocket designed protease）**：删环留核再重建——"we developed a strategy that"，保留的是天然钳形沟的折叠逻辑。
  - **DP（de novo protease）**：极简基序 + 全新生成骨架——"we extracted only the minimalist catalytic motif-comprising the zinc-coordinating residues, the general base glutamate, and the oxyanion hole histidine"，代价是"This minimalist approach"。
- **底物在活性位点里的“该摆成什么形状”**：不猜，用 AlphaFold3 在模板酶里预测底物构象——「we used AlphaFold3」（此句后原文插了引文编号 43），读到的结果是"The predictions revealed that"，随后**只截取参与 β 配对的那段骨架原子**当几何约束：Fungalysin 取 P2-P1′、PPEP-1 取 P3-P1。
- **生成模型**：自研 **Proteus2**（flow-based），"we integrated a customized"，训练任务是 dual-modality motif scaffolding；关键性质是"sequence and structure conditions are treated as independent masking tracks"，因而能吃"hybrid inputs comprising"——**这正是“序列特异”被写进生成回路的地方**，而不是生成后再用打分挑。
- **两步封装扩散（two-step encapsulation）**：先围催化 Glu、再围 oxyanion hole，逐步把底物封进钳内。
- **序列设计**：骨架定了之后"Following backbone generation,"（配体环境条件化的 MPNN，此处后插引文 44）。
- **计算侧复验**：把设计好的复合物重新预测一遍，"the resulting protease-substrate-zinc complex structures were validated with AlphaFold3 to ensure convergence to the intended catalytic geometry"。
- **实验侧**：E. coli 表达 + Ni-NTA + HRV3C 切 His 标签 + SEC 纯化；**融合底物**（MBP-Aβ片段-SUMO）SDS-PAGE 读切割；裂解产物质谱定位点；时间降解曲线；蛋白级 FRET 传感器测 Michaelis-Menten；定点突变验证机制；三底物交叉测特异性；三酶 cocktail 切全长 Aβ42。
- **本文没有用的方法**：MD（本地正文对 `molecular dynamics`、`dynamics`、GROMACS、OpenMM、AMBER、umbrella、metadynamics、explicit solvent 全部 0 命中；登记底稿 `sources/cao.md:455` 的全文关键词扫描同样确认）、QM/DFT（`quantum`、`DFT` 0 命中；作者只在讨论里引用 Radzicka & Wolfenden 的“无催化肽键水解速率/过渡态亲和力”文献作为加速倍数的分母）、无结构解析（`crystal` 的 2 次命中都在参考文献期刊名 Acta Crystallogr 里，正文无晶体/冷冻电镜数据）、无螯合敲除或金属计量、无定向进化/显示库筛选。

### 工作流程表（按正文出现顺序；阈值一栏如实标注本地是否可得）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | PPEP-1（6r4w）与 Fungalysin（4k90）实验结构 | 定催化基序；PP 路线删结合环保核心，DP 路线只留极简基序 | 原文未给阈值（选择依据是机制清楚 + oxyanion hole 一个是 Tyr 一个是 His，构成两套可比较的位点） | 2 套基序模板 × 2 条策略 |
| W2 | 模板蛋白酶 + 目标底物肽 | 用 AlphaFold3 预测底物在活性位点中的构象，取与酶活性位点旁 β 链配对的一段骨架原子作几何约束 | 定性判据：底物呈 β-strand；"these segments form strand" | Fungalysin 的 P2-P1′ 骨架原子、PPEP-1 的 P3-P1 骨架原子 |
| W3 | Aβ42 序列（中央疏水核 17-21、C 端 30-42） | 选 3 个切割位点：1 个在中央疏水核、2 个在 C 端疏水区；每个位点分别走 PP 与 DP | 原文未给选位点阈值（理由是可聚性/治疗相关性） | 3 位点 × 2 策略 = 6 个“策略-底物”组合 |
| W4 | 基序模板 + 坐标无定义的底物序列 | Proteus2 共生成“酶-底物复合物”骨架；**两步封装**：第 1 步生成催化 Glu 周围骨架并部分包裹底物，第 2 步围绕 oxyanion hole 完成包封 | 定性判据：减少位阻、提高界面堆积密度、生成 clamp 形；**无任何数值阈值**（本地无 Methods 节） | 未披露生成库规模（正文只给“送测前平均挑选数”） |
| W5 | 复合物骨架 | LigandMPNN 设计序列 | 原文未给阈值（本地无 Methods 节，采样数/挑选规则未披露） | 每条骨架对应的设计序列 |
| W6 | 设计三元复合物（蛋白酶-底物-锌） | AlphaFold3 复预测，看是否收敛到设计的催化几何 | "to ensure convergence to the"——定性；**本卡无法给出通过/不通过的数值线**（登记底稿里的 in-silico success 措辞属 C23，见 §0） | 入选实验的设计集 |
| W7 | 6 个策略-底物组合 | 人工挑选送实验的设计并表达纯化 | 表达与可溶纯化：E. coli、Ni-NTA 磁珠、HRV3C 去 His 标签、SEC | "On average, 26 designs were"（≈156 条，正文未给总数） |
| W8 | 设计的蛋白酶 + MBP-Aβ片段-SUMO 融合底物 | 含锌条件下过夜孵育，跑 SDS-PAGE 看是否变成两条低分子量带 | 判据：出现 MBP/SUMO 分离带来的分子量位移；"Successful proteolytic cleavage" | **5 个有活性酶**：DP720-S1、DP622-S2、DP221-S3、PP507-S1、PP532-S1；PP 在 S2/S3 为 0 |
| W9 | 命中酶的裂解产物 | 质谱测产物分子量，与理论值比对定位切割位点 | 判据：observed 匹配 theoretical；旁路峰占比（DP221-S3 的次要峰约为主峰的 10%，位点向 C 端偏一个残基） | 5 个酶的设计位点确认（含 1 个 10% 旁路） |
| W10 | 命中酶 + 底物 | 时间进程降解曲线，1:2 酶:底物摩尔比 | 判据：完全降解所需时间 | DP622-S2 4 h；DP720-S1 与 PP507-S1 8 h；PP532-S1 近 12 h；DP221-S3 12 h 时切掉一半以上 |
| W11 | 命中酶的定点突变体 | 广义碱 Glu→Ala、oxyanion hole（DP 的 His / PP 的 Tyr）→Ala、DP 的第二壳层（与锌配位残基成氢键者）→Ala 或 Phe，再跑 SDS-PAGE/动力学 | 判据（活性方向性）：设计位点残基换成 Ala/Phe 后，SDS-PAGE 是否仍出现切割条带；单突变 vs 双突变对比（原文未给量化阈值） | 结论：E→A 在 DP 与 PP 里普遍 abolish；oxyanion His→A 影响极小甚至为正（H191A 增强）；D128A(DP720-S1)、N111A(DP221-S3) 显著降；DP622-S2 的 D126A 或 Y91F 单突变影响小、D126A/Y91F 双突变 dramatic decrease |
| W12 | 目标序列插入 mTurquoise2 与 mVenus 之间构成的 FRET 传感器 | 测初速度随底物浓度变化，按 Michaelis-Menten 拟合 kcat、Km、kcat/Km | 判据：拟合参数；与 W10 时间曲线交叉核对 | kcat 普遍 10⁻⁴ s⁻¹ 量级、Km µM 级；DP622-S2 160.8（kcat 0.0009 s⁻¹、Km 5.36 µM）、PP507-S1 28.4、PP532-S1 24.3、DP221-S3 4.2、DP720-S1 3.8 M⁻¹s⁻¹；平均加速 >10⁷ 倍；DP720-S1 与时间曲线不一致（作者归因位阻） |
| W13 | 突变体 | 重测动力学（Y91F、D126A、H172A、H191A、Y91F/D126A） | 判据：kcat/Km 相对母本设计的变化 | DP622-S2 三个单突变全部升高（D126A 的 kcat 三倍、Y91F 的 kcat/Km 两倍）；双突变 Y91F/D126A 下降；H191A 2.7 倍 |
| W14 | 5 个酶 × 3 种融合底物 | 交叉特异性（SDS-PAGE） | 判据：对非靶底物是否可检出切割 | PP507-S1 只切 Substrate 1；PP532-S1 三种都高效切；DP720-S1 对 Substrate 2 有可检出但降低的活性；DP622-S2 与 DP221-S3 互有交叉（效率明显低于各自靶） |
| W15 | PP507、DP622 Y91F、DP221 H191A 三酶 cocktail + 全长合成 Aβ42 | 共孵育后质谱找预期片段 | 判据：检出三条预期片段 | 检出 DAEFRHDSGYEVHHQKL、VFFAEDVGSNKGAIIGL、VVIA ⇒ 全长 Aβ42 上按设计位点切割成立（Extended Data Fig. 7，本体未随本地文本提供） |

**这套流程对我们最有信息量的骨架**：活性位点不是“设计完再挑”，而是**先由 AF3 定出底物该摆的构象（β-strand + 具体 P2-P1′ 骨架原子），把化学几何写成生成模型的条件，再让模型连底物一起生成**；计算闸口只有一道定性的“复预测是否收敛到设计几何”，真正的闸门是**湿实验**（26 条/组合的小批量 + SDS-PAGE 位移 + 质谱定位点）。也就是说：本漏斗的淘汰逻辑是“少送、每送一条都要能定位到化学事件”，而不是“多筛、靠阈值砍掉大部分”。

## 4. 关键数字台账（全部可在本地全文里逐字搜到）

| 数值 | 含义 | 出处（正文原句片段，逐字） |
|---|---|---|
| 3 位点 × 2 策略 = 6 组合 | 设计任务的规模 | "we selected three distinct"（原文 hydrophogic 为笔误） |
| `6r4w` / `4k90` | 催化基序来源的两株锌内肽酶（PPEP-1 / Fungalysin）的 PDB 号 | 正文两处分别给出 PDB 号；两句之间原文插了引文编号 37、38，故本卡不合并引用 |
| 17-21 / 30-42 | Aβ42 上被认定为聚集核心的两段疏水区 | "The pathological self-assembly" |
| P2-P1′ / P3-P1 | 生成时被固定下来的底物骨架原子范围 | "From these predicted structures, we extracted the P2-P1′ backbone atoms of the Fungalysin substrate peptide" |
| 平均 26 条/组合 | 每个策略-底物组合送去湿实验的设计数（推算总送测约 156 条，正文未给总数与生成库规模） | "On average, 26 designs were" |
| 5 个酶 | 实验验证到有活性的设计（DP720-S1、DP622-S2、DP221-S3、PP507-S1、PP532-S1） | "Experimental characterization" |
| 4 h / 8 h / 8 h / ~12 h / 12 h 切一半 | 完全降解所需时间（依次为 DP622-S2、DP720-S1、PP507-S1、PP532-S1、DP221-S3），酶:底物 = 1:2 摩尔比 | "At a 1:2 enzyme-to-substrate"；"while PP532-S1 required nearly"；"In contrast, DP221-S3 displayed" |
| ~10% | DP221-S3 旁路切割次要质谱峰相对主峰的占比（裂解位点向 C 端偏一个残基） | "a very minor peak-representing" |
| kcat 约 10⁻⁴ s⁻¹；Km 微摩尔级 | 五个设计的全局动力学水平 | "Analysis revealed that the" |
| 160.8 M⁻¹s⁻¹（kcat 0.0009 s⁻¹、Km 5.36 µM） | 最佳设计 DP622-S2 的催化效率 | "achieving a k cat / K m of" |
| 28.4 / 24.3 / 4.2 / 3.8 M⁻¹s⁻¹ | PP507-S1 / PP532-S1 / DP221-S3 / DP720-S1 的催化效率 | "The PP507-S1 and PP532-S1" |
| >10⁷ 倍 | 相对无催化肽键水解的加速（分母取自文献 33，不是本文实测的同一底物） | "These k cat values represent an" |
| 三倍 / 两倍 / 2.7 倍 | D126A 的 kcat 提升；Y91F 的 kcat/Km 提升；DP221-S3 H191A 的 kcat/Km 提升 | "notably, the DP622-S2 D126A"；"The DP221-S3 H191A mutation had" |
| 1 / 5 | 三底物交叉实验里真正单底物特异的酶数（只有 PP507-S1） | "PP507-S1 exhibited the highest" |
| 3 条片段 | 三酶 cocktail 切全长 Aβ42 的质谱预期产物 | "Mass spectrometry analysis" |
| 0 次 | 本地正文里 MD / QM / 螯合剂 / 金属计量类关键词的命中数（本卡以 `grep -i` 实测：molecular dynamics、dynamics、GROMACS、OpenMM、AMBER、umbrella、metadynamics、free energy perturbation、explicit solvent、quantum、DFT、EDTA、ICP、RMSD、threshold、pAE、pLDDT 均为 0；Rosetta 仅 2 次且都在 Code availability 一句里；crystal 仅 2 次且都在参考文献的期刊名 Acta Crystallogr 里） | 见第 3 节工具箱末条与第 7 节 |

## 5. 结论——作者说了什么

1. 序列信息可以**写进生成回路**：把目标肽序列和催化基序同时作为生成条件，就能造出识别特定序列的金属蛋白酶（"By explicitly integrating"）。
2. 两步封装做出 clamp 形、把底物包住，从而同时最大化特异性与区分能力。
3. de novo 酶设计**从“结合”跨到“功能性蛋白水解生理靶”**：三个不同 Aβ 位点都拿到活性酶，并能在**全长 Aβ42** 上按设计位点切割。
4. 机制上：活性来自设计的活性位点（Glu→Ala 普遍失活是主要支撑），第二壳层与 oxyanion hole 残基**主要通过调 kcat 影响效率**，且这种调优是**上下文相关**的（DP622-S2 单突变升、双突变降）。
5. 绝对性能：kcat 10⁻⁴ s⁻¹ 量级、Km 达微摩尔（与 IDE 等天然 Aβ 降解酶同量级），平均加速 >10⁷ 倍；作者明说 turnover 仍低于天然酶。
6. 作者自限三处：（i）"Achieving strict substrate"；（ii）关键微环境因素（溶剂、第二壳层配位、动态催化过程）当前方法建模不准；（iii）特异性要靠**未来的显式阴性设计**才谈得上提升。
7. 展望：该框架可推广到丝氨酸/半胱氨酸蛋白酶，作者定位为治疗导向的“可编程蛋白水解”。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的真正创新不在“又一个 de novo 酶”，而在把“要切哪条键的序列”当成生成模型的一等条件**。B09/C08 那代管线是“生成 → 事后打分挑选”，这里是“底物序列与坐标共同条件化生成”，把特异性前移到回路内（与同组 C23 把判定前移是同一思路的两条实现）。对我们的直接含义：如果 UAA 合成酶筛选只在“结构像不像”上打分，我们就永远拿不到“能不能认这个底物/能不能成这个键”的信号；条件化在生成阶段注入功能约束，比事后加闸口更有效。
2. **活性位点的可复现单位是“基序 + 底物构象”这一对，不是基序单独**。他们先用 AF3 定出底物在模板里是 β-strand、再截取参与配对的 P2-P1′/P3-P1 原子，才让几何有唯一解。→ 我们做 UTP→pppUA 类反应时，“催化残基摆对了”不足以定义活性位点；**底物（核苷酸/三磷酸）在口袋里的取向必须被同时固定**，否则生成的口袋对底物是“空槽”。
3. **“5 个命中 / 约 156 条送测”这个数字要看清它测的是什么**。送测集是**人工挑的**、每条都带可定位的化学读出，因此这个比率是“精挑小批量里多少条真能切”，不是“生成库 → 命中”的全漏斗命中率。作者也从未给生成库规模。→ 我们的类比必须是“表达率/可溶率/产物生成率”分别记账，不能混成一个“命中率”。
4. **金属配位的实验证据链只有半条**。Glu→Ala 全面失活证明“广义碱不可省”，这是化学事件级的证据；但锌本身的必要性（螯合敲除+回补）、配位数与计量（ICP）、三配位 His 突变效应、以及 apo/holo 结构，本地正文都没有。第二壳层突变的“单突变升、双突变降”更像是**微环境扰动而非配位失效**。→ 迁移到我们：任何“金属/辅因子是催化必需”的主张，必须配一条**去掉辅因子 → 活性消失 + 补回 → 活性恢复**的实验，否则只是“在含锌缓冲液里能反应”。
5. **oxyanion hole 突变不伤活性这件事，应该看成方法学信号而非小瑕疵**。设计时把它当过渡态稳定的关键件，实验却发现去掉也行（甚至更好），作者的替代解释是水分子补位。→ 含义：**当前设计回路无法区分“这个残基真的稳定过渡态”与“这个位置有别的东西能顶上”**；这正是需要 MD/QM 却没有做的位置（本文既无 MD 也无 QM）。我们的 S1/S2 化学步骤判定同样会遇到这种情况——“设计里必需的残基，突变后仍出产物”——那时不能用“设计成功”结案，必须承认机制未定。
6. **特异性与位点正确性在这篇里是一对会互换的代价**。H191A 让 DP221-S3 几乎不切非靶，却把裂解位点整体搬到偏移一个残基的次要位点。→ 对我们：任何“提高选择性”的闸口若只看单一读数（产物条带/荧光），可能同时在改变反应路径本身。**判据必须成对：既问“只出这一种产物”，也问“这一种是不是设计的那一种”**。
7. **摘要口径与正文结果的背离是本文最需要记住的教训**（详见第 2.6 条）。"minimal or undetectable activity on non-cognate substrates" 在正文里只对 1/5 个酶成立。→ 对我们：写结论时把每个“高特异/高效”限定到具体构建体与具体底物集，禁止用“平均”覆盖掉交叉反应。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者自陈：见第 5.6 条三处（严格底物排他性远难于做出活性；kcat 相关微环境当前方法建模不准；特异性待未来的显式阴性设计）。另在正文中承认"the turnover rates of our designs are lower than those of natural enzymes"。
- 作者披露的可复现性缺口：**「Code availability」只说 Rosetta 套件公开，本文自己的"Design protocols, analysis"**——即截至预印本，Proteus2 的生成协议与权重不公开；且已声明将申请临时专利，公开范围存在进一步收窄的风险。
- 我们读出的：① 本地正文**没有 Methods 节**，所有关键参数（锌浓度、孵育条件、生成采样数、两步扩散的输入构造、LigandMPNN 与 AF3 复验的通过线）不可核验，本卡的工作流只能按正文描述排序，**顺序可复现、参数不可复现**；② 计算闸口是**定性的**（"convergence to the intended"），因此本文无法告诉我们“哪条设计会被计算淘汰”，也就无法给出漏斗递减；③ 全部动力学来自蛋白级 FRET 融合传感器，与真正的全长 Aβ/APP 底物环境不同，作者用同一体系内的时间曲线互证时发现 DP720-S1 冲突，却未做正交读出；④ 无任何结构解析（无晶体/冷冻电镜），“设计的活性位点几何被实现”这一环没有直接观测；⑤ 无 QM/MD，所以对“10⁷ 倍加速来自哪一步的能垒下降”没有任何机理层证据；⑥ 送测集与命中集之间可能有人工挑选偏差（挑选规则未披露），“5/约156”不应作为该方法对任意位点的期望命中率引用。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **“功能约束前移到生成条件”的组织方式**（挂 DP2R 的 G0–G10 门，本仓库内的落点是 `data/literature_cards/README.md:17` 的迁移节口径；只借方法结构，不借它的数字）：我们生成/挑选 UAA 合成酶候选时，应把“底物分子 + 目标化学事件”作为条件之一（哪怕是粗粒度的：底物取向 + 参与催化的残基类型），而不是先造口袋再用结构一致度事后挑。
2. **活性位点=基序+底物位姿的双要素**：他们从天然酶取“锌三配位 + 广义碱 Glu + oxyanion hole”，又用 AF3 定底物构象，然后**只截取与酶 β 链配对的那段骨架原子**。→ 我们的等价动作：从已知核苷酸转移酶/连接酶里取“三磷酸/镁离子配位 + 亲电进攻取向”的最小基序，并同时固定 UTP/ATP 片段在口袋里的位姿，两者一起交给打分回路。
3. **金属/辅因子必需性的实验判据设计（本文只做了半条，我们要做全）**：主证 = 催化残基点突变使产物消失；辅证 = **螯合剂敲除 + 等摩尔回补的双向实验**、金属计量（ICP-MS）、配位残基逐个点突变。本文缺后三条，正是我们应写进我们自己协议的地方。
4. **“融合标签 + 一条可定位的化学读出”这个底物工程思路**：他们把难溶的 Aβ 片段插进 MBP-SUMO 之间，用 SDS-PAGE 位移直接读出“这一条键断没断”。→ 对我们：把 UAA 合成酶的产物检测做成**分子量位移/正交标签可读**的形式（如底物蛋白 + 产物质量位移），比只看“消耗了多少底物”更能定位到化学事件。
5. **小批量、信息量最大化的送测策略**：每个组合只送 26 条，但每条都有位点级质谱确认与突变体验证。这与我们“一轮最多几个构建体”的现实一致——**每条都要能回答一个机制问题**，并保留失活对照（他们的 Glu→Ala 就是标准失活对照，值得直接照搬）。
6. **特异性和位点正确性成对报告**（第 6.6 条）：我们的每个候选要同时给“是否只出目标产物”和“该产物是否为设计的那一步产物（S0/S1/S2 归属）”。

**不可迁移（为什么不能照搬）**

1. **本文的加速倍数、kcat/Km 数字不能当我们的目标值或成功概率**。kcat 10⁻⁴ s⁻¹、最好 kcat/Km 160.8 M⁻¹s⁻¹ 是**这个人工锌位点对这个融合底物**的测量，且分母是文献的无催化水解速率。本系列门禁（`data/literature_cards/README.md:17` 明确把“借 binder 的 pAE/ipTM 阈值当酶活判据”列为禁止项，DP2R 的 G0–G10 门）同样禁止把别的设计案例的活性数字当作 UAA 酶活的判据或成功概率校准。
2. **“约 156 送测得 5 命中”不是漏斗命中率**，因为生成库规模与人工挑选规则未披露、也没有阴性设计的计算淘汰环节。任何“因此 UAA 合成的命中率约为 X%”都是编造（本文无此数据）。
3. **他们的成功判据是“切断了设计的那条肽键”，我们的成功判据是“生成了设计的化学产物并排除竞争副产物”**：水解一个肽键是单事件、单一化学产物；UAA 合成是多步且环化/副反应竞争。所以本文那种“单点突变 → 全或无”的机制验证强度不足以覆盖我们的判定，我们不能用“设计残基突变后失活”单独作为证据。
4. **本文没有 MD、没有 QM、没有显式溶剂效应建模**，因此这篇**不能**为我们“用 MD/QM 判催化可行性”的主张提供任何命中率或有效性背书。相反，它的作者结论恰恰是“kcat 相关的微环境当前方法建模不了”——这是对我们重计算路线的**警示**而非支持。
5. **不能照搬“生成模型直接共生成酶-底物复合物”这一实现**：Proteus2 未公开、且已声明要申请专利，我们无权重、无协议；能搬的是“把功能约束写成条件”的思想，不是这条具体管线。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/C22_PPR1219681_text.txt

- 本地纯文本：`fulltext/C22_PPR1219681_text.txt`（51,459 B，SHA-256 `8596f085f1a9c551…`；由 `fulltext/C22_PPR1219681_fullTextXML.xml` 经标签剥离、HTML 实体解码、未改写内容得到；该 XML 实为 bioRxiv 正文页 HTML，故**不含 Methods 节**）。同一论文在登记表里还挂了 `sources/cao.md`（该路径在本仓库根目录 `sources/cao.md`，存在），但本卡**全部引句只对照上面那份 `.txt` 逐字写入**，未从底稿抄任何英文句子。
- 对照底稿行号：`sources/cao.md:351–365`（原卡 [C22]），以及该文件的跨卡结论 `sources/cao.md:443`（酶/化学功能演进链）、`:455`（全组 MD/自由能关键词扫描，除 C08 外仅命中参考文献）、`:463`（C22 无自算 QM 的警示）。本卡对上述第 455/463 条做了本地独立复核（对本文 `.txt` 直接 `grep -i` 计数：molecular dynamics / dynamics / GROMACS / OpenMM / AMBER / umbrella / metadynamics / explicit solvent / quantum / DFT / EDTA / ICP / RMSD / threshold / pAE / pLDDT 全为 0 命中；crystal 的 2 次命中均在参考文献期刊名中，Rosetta 的 2 次命中均在 Code availability 句中）。
- 与登记底稿的两处分歧（本卡按本地正文为准）：`sources/cao.md:356` 记的 in-silico success 判据措辞属 C23；`sources/cao.md:358` 实验列里的 `-log K_tx` 未见于本文正文。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。CSV 现值中 `thresholds/候选数递减/实验命中率` 三格原记为“未记录”，本卡给出的 `26 条/组合 → 5 命中`属**送测口径、非全漏斗口径**，回填时须按第 8 节不可迁移第 2 条加注。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "C22" --no-report`（不带 `--sync-map`、不落 selfcheck.txt/rollout_status.tsv，避免覆盖他人产物）把本卡所有被**直双引号**包住、不含中日韩字符且 ≥20 字符 / ≥12 字母的片段，在上面那一份 `.txt` 里逐字查找。本卡约定：**英文逐字引句只用直双引号，中文叙述里的引述一律用全角引号或直角引号**——因为门禁是按行配对直双引号的，混用会让相邻引句被当成一整段而漏检（写卡过程中实测出现过：一处跨引文编号 43 的拼接被拆成两条；一轮批量把中文引述改成全角引号的操作因配对错位把相邻引句的闭合号吃掉了，已回滚重做，改后核验从 57 条升到 **67 条、67/67 命中**）。最终结论：**PASS C22 quotes=67/67，退出码 0**。
- **反向自测（证明"引用造假会被机器抓到"不是声明）**：在内存里把本卡一条真引句的 `160.8` 篡改成 `161.8`，用门禁自己的 `quotes_of()` + `norm()` 逐字比对本地 `.txt` ⇒ 该条变 MISS、命中率 66/67，与门禁判 FAIL 的口径一致；不落任何文件。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 53 条逐字引句来自许可受限的第三方来源（C22；ALL_RIGHTS_RESERVED），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=预印本（bioRxiv 2026.01.06.697903，Posted 2026-01-06，未同行评审，将申请临时专利）
target=锌依赖金属蛋白酶（de novo），序列特异切割 Aβ42 的 3 个位点（中央疏水核 17-21 内 1 个 + C 端 30-42 内 2 个）；催化基序取自 PPEP-1（PDB 6r4w）与 Fungalysin（PDB 4k90）
backbone_generation=自研 Proteus2（flow-based 生成模型；UniRef50 预训练蛋白语言模型 + 辅助结构解码目标；序列/结构作独立 masking 轨）共生成"蛋白酶-底物-锌"复合物；两步封装扩散（先催化 Glu 侧、再 oxyanion hole 侧）；底物活性构象先用 AlphaFold3 建模（取 β-strand 的 P2-P1′/P3-P1 骨架原子）；LigandMPNN 出序列；AF3 复预测验证几何收敛；两条路线 PP（删 PPEP-1 结合环保核心）与 DP（只留极简催化基序全新骨架）
computational_filters=催化基序预定义（三个锌配位残基 + 广义碱 Glu + oxyanion hole Tyr/His）；底物片段与酶活性位点旁 β 链的配对几何；两步封装后的位阻与界面堆积（定性）；LigandMPNN 后 AF3 复预测确认收敛到设计的催化几何；正文无任何数值化计算闸口（无 RMSD/pAE/能量阈值），也没有 MD 或 QM
thresholds=原文未给数值阈值（本地正文不含 Methods 节；几何收敛为定性判据）；实验侧数字仅有：每策略-底物组合平均 26 条送测、酶:底物 = 1:2 摩尔比、DP221-S3 旁路裂解峰约为主峰 10%
md_used=否（本地正文 0 命中 MD 关键词；同组全表扫描 sources/cao.md:455 亦确认除参考文献外无命中）
qm_used=否（未见自算 QM/DFT；仅引用 Radzicka & Wolfenden 的无催化肽键水解速率文献作为 >10^7 加速的分母，故本文不能为"QM 判催化"提供命中率背书）
experimental_methods=E. coli 表达 + Ni-NTA 磁珠 + HRV3C 去 His 标签 + SEC 纯化；MBP-Aβ片段-SUMO 融合底物 SDS-PAGE 判读裂解；裂解产物质谱定位切割位点；时间进程降解曲线；蛋白级 FRET 生物传感器（mTurquoise2-目标Aβ序列-mVenus）+ Michaelis-Menten 拟合 kcat/Km/kcat/Km；定点突变（催化 Glu→Ala、oxyanion hole His/Tyr→Ala、第二壳层 D/N→A 与 Y→F、及双突变）；三底物交叉特异性；三酶 cocktail 切全长合成 Aβ42
pipeline_counts=3 位点 × 2 策略 = 6 个策略-底物组合 → 每组合平均 26 条送测（推算约 156 条；正文未给总数、未给生成库规模、未披露计算淘汰数）→ SDS-PAGE 有活性 5 条（DP720-S1、DP622-S2、DP221-S3、PP507-S1、PP532-S1）→ 质谱位点确认 5 条（DP221-S3 含约 10% 旁路峰）→ 动力学定量 5 条 → 单底物特异的仅 1 条（PP507-S1）→ 全长 Aβ42 cocktail 3 条（PP507 + DP622 Y91F + DP221 H191A）
hit_rate=送测约 156 条（26×6 组合，正文未给总数与百分比、也未给生成库规模）得 5 个有活性酶；PP 策略在 S2/S3 两位点 0 命中；5 个中只有 PP507-S1 对两个非靶底物无可检出活性（与摘要"minimal or undetectable activity on non-cognate substrates"口径不一致）
best_metric=DP622-S2 的 kcat/Km = 160.8 M^-1 s^-1（kcat 0.0009 s^-1、Km 5.36 µM）；相对无催化肽键水解平均加速 >10^7 倍；最优突变体 DP622-S2 Y91F 催化效率提升两倍、DP221-S3 H191A 提升 2.7 倍（但后者裂解位点整体偏移到次要位点）
cost_or_stat_note=无补充信息正文（Extended Data Fig.1-7/Table1-3 仅被引用）；本地无 Methods 节 ⇒ 锌浓度、缓冲液、孵育时长、生成采样数、两步扩散输入构造与挑选规则均不可复现；Proteus2 权重与协议未公开（作者承诺"upon final publication"提供）；全文无晶体/冷冻电镜结构、无 ICP 金属计量、无螯合敲除-回补对照；kcat 普遍仅 10^-4 s^-1 量级，低于天然酶
role_in_timeline=曹龙兴组酶设计漏斗从"物理基序搭建 + 能量指标挑选"（C08/C23 的 theozyme+QM+Rosetta 指标）推进到"生成模型把目标肽序列与催化基序同时条件化、共生成酶-底物复合物"，并把判定前移进生成回路；是本 CSV 链上第一篇把 de novo 催化设计从活化酯模型反应推到真实多肽底物（Aβ）单键切割的工作，其瓶颈由"会不会折叠/会不会结合"变为"亚埃级催化几何 + 底物序列识别"；同组后续 C23 用 ML 活性预测器补上本文缺失的计算闸口环节
source_pointer=data/literature_cards/fulltext/C22_PPR1219681_text.txt（SHA-256 8596f085f1a9c551…，51,459 B，由 C22_PPR1219681_fullTextXML.xml（bioRxiv 正文页 HTML）去标签得到，不含 Methods 节）；对照底稿 sources/cao.md:351-365；CSV 行 C22
CSV回填-->
