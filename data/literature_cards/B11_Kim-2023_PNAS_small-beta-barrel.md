# [B11] 从头设计小 β 桶蛋白——把「表达→可溶→正确寡聚态→谱学证明折叠」四段漏斗第一次逐段量化

Kim D E, Jensen D R, Feldman D, Tischer D, Saleem A, Chow C M, Li X, Carter L, Milles L, Nguyen H, Kang A, Bera A K, Peterson F C, Volkman B F, Ovchinnikov S, Baker D（华盛顿大学 Biochemistry / Institute for Protein Design / HHMI；Medical College of Wisconsin；Harvard）
PNAS 2023, 120(11): e2207974120 · DOI 10.1073/pnas.2207974120 · PMID 36897987 · PMCID PMC10089152
开放获取（CC BY-NC-ND 4.0）· 全文链接 https://pmc.ncbi.nlm.nih.gov/articles/PMC10089152/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B11**（组：Baker组; 通用方法学；`batches.tsv` 第 3 批） |
| 论文 | De novo design of small beta barrel proteins，PNAS 2023, 120(11):e2207974120 |
| 本文取回方式 | PMC10089152 的 JATS/XML 去标签纯文本，2026-10-16 随 Baker 组文献批次抓取 |
| 本地全文 | `data/interim/baker_lit/ft/betaBarrel2023.txt`（66,412 B，247 行；`norm()` 归一后约 57,000 字符） |
| 登记底稿 | `sources/baker.md:147–158`（原卡），本卡在其基础上补齐：Table 1 的四段漏斗全比例、蓝图支路与幻觉支路的完整阈值链、两个高通量筛选的失效与替换、beta-bulge 与 NPSA 两处具体应对 |
| 证据级别 | **全文级**（本卡所有引句均可在本地全文里逐字命中；核验见第 9 节） |
| 结构 deposited | 溶液 NMR 结构 7UWY / 7UWZ（BMRB 31017 / 31018），晶体结构 7UR7 / 7UR8 |
| 未取到的部分 | SI Appendix（Fig S1–S12、Table S8、Supplementary text 与 Supplementary Materials and Methods：两个高通量筛选的完整协议、logistic/LASSO 回归特征表、native 结构选取标准）、Fig 1–5 的原图数值、13,990 与 45,761 条设计的逐条清单、Zenodo 归档内容。凡引用这些的地方本卡明写正文未给出 |

## 1. 这篇到底解决什么（大白话）

到 2022 年为止，从头设计蛋白在**全 α** 和 **α/β** 两类折叠上已经做得很顺，但**球状全 β** 几乎做不出来，而**小于 70 个残基的小 β 桶**（自然界里最常见的功能模块之一，如 SH3、OB-fold）在此之前**一个都没有被从头设计成功过**。作者列了三条物理原因，都在正文里写明：核心太小、桶收口时的构象张力、以及游离 β 链边缘会互相粘成一团。

这篇做的事情是把同一个目标用**两条完全不同的生成路线**各做一遍，再拿**同一套湿实验漏斗**去量它们：

- 路线一（传统、物理可解释）：**Rosetta blueprint**——人工画一张二维蓝图（每条链多长、每个残基的 ABEGO 骨架二面角分箱、哪两条链之间要有骨架氢键），让 Rosetta 从伸展肽链开始蒙特卡洛片段组装把这个拓扑搭出来，再用 Rosetta 设计序列。
- 路线二（新，深度学习）：**constrained hallucination**（约束幻觉）——把 trRosetta 这个结构预测网络的损失函数改成两项之和：一项要求你钉住的 β 链核心保持原样，一项让网络自由地把环和转角幻觉成任何它觉得能折的形状，然后用梯度下降反过来改序列。骨架出完后再交给 Rosetta 重新设计序列。

湿实验侧的关键不是"能不能表达"，而是**四段分开的漏斗**：表达 → 可溶 → 单体/二聚（正确寡聚态）→ 谱学上真的折叠（CD 有结构信号、HSQC 有数目对得上且分散良好的尖锐峰）。这篇最有迁移价值的地方在于：它把**聚集和异常寡聚**这两条**不属于折叠失败、却吃掉大部分候选**的路径量化了——原文给的是 "Indeed, 74 percent of the soluble experimentally characterized designs were oligomers, and 40 percent of the expressed designs aggregated"。也就是说，蓝图支路里"能表达而且可溶"的设计**四分之三是寡聚体**，而不是折错的单体；失败的主通道不是能量打分不准，而是分子间粘在一起。

正因为如此，他们中途**换了湿实验判据**：先用酵母表面蛋白酶解抗性做一级筛选（快、能被 NGS 读，但对全 β 失灵，只有 6% 通过、且通过者 77% 是寡聚体），再加一个 SEC + 质谱条码的二级筛选（慢、通量小，但直接读"溶液里的可溶性和寡聚态"）。最后用"深度学习出骨架 + Rosetta 出序列"的组合把 HSQC 折叠率从蓝图的 31% 拉到 92%，并把 **12,911 条**有把握折叠的小 β 桶骨架作为 scaffold set 发布出去——这一步的意义是给 binder 设计补上了**一直缺位的 β 形状空间**。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **小 β 桶天生比大桶难折，而且难在三个不同的物理点上**。原文把障碍拆成三条：核心太小 + 收口张力 + 分子间聚集（"the hydrophobic core stabilizing the fold is necessarily very small,"，以及 "intermolecular aggregation through free beta strand edges can compete with proper monomer folding"）；引言里还补了第四点——不按天然蛋白的方式加非理想特征就会积累张力（"considerable conformational strain can arise from steric clashes and unfavorable left-handed"）。 **应对**：不做通用的全 β 设计，而是**锁定四个具体拓扑**（SH3、OB、b5、b6）逐个攻，并把"自然界已有的八链桶蓝图法"（引文 7）当起点往下缩到 ≤6 链、<70 aa。 **代价**：这四类的成功率彼此差很大（见第 2.7 条），本文没有给出一个能预测"哪一类能成"的先验判据。
2. **Rosetta 片段组装搭不出 b5 的收口**——这是本文第一次真正的技术卡点，写在 Results 里很直白："Initial b5 backbone generation attempts failed to complete hydrogen bond strand pairing of the last"。要闭合桶就必须把最后一条链弯过来配对，而纯蓝图规则不允许那么大的弯曲。 **应对**：往蓝图里**人为加入 beta-bulge（β 缺陷）**，让氢键配对能沿着弯折继续下去——"To address this issue, we incorporated additional beta-bulges in the blueprint which allowed the"，图注给出证据（"the incorporation of beta bulges considerably improves the extent of hydrogen bonding,"），并且 b6 也用同一招（"Strand pairing was also improved with the"）；b5/b6 的蓝图本身是手工从零试错搭的，"blueprints which did not give rise to the"。 **代价**：bulge 是**设计意图，实验结构里并不保证存在**——幻觉支路的晶体结构 170_h_ob 就出现了链位错："The differences in the C terminus involved a"；SI Appendix 也承认"Some b5 designs that were experimentally"。
3. **主失败模式不是折错，而是粘在一起**（本文对漏斗最有贡献的一条）。作者紧接着上面那句给出比例："Indeed, 74 percent of the soluble experimentally"。也就是说：**已经可溶**的设计里 74% 是寡聚体，**已经表达**的设计里 40% 直接聚沉——这些都不是 Rosetta 能量打分能区分的东西。 **应对**：把判据从"算出来的能量低"换成**湿实验里可正交观测的三件事**（可溶性、SEC 洗脱体积落在单体/二聚区间、HSQC 峰数目与分散度），同时**引入 SAP（spatial aggregation）分数**作为计算侧的聚集倾向代理（"the soluble monomeric designs on average have improved local sequence-structure mapping, more favorable Lennard–Jones interactions, and reduced spatial aggregation (SAP) scores"），并明确写"Filtering designs based on these criteria should"。 **代价**：SAP/局部序列-结构匹配这些特征只是在**已测的两端群体之间事后富集**出来的，本文没有前瞻验证它们单独能把成功率提多少。
4. **一级高通量筛选（蛋白酶解抗性）对全 β 蛋白是坏的**。他们本来指望这个 assay——它在约 40 残基的 α 与 α/β 设计上经过多轮设计-构建-测试循环被证明能系统性提升设计质量。但这里"only six percent of the small beta barrel designs"，而且验证Top 命中后发现"suggested the screen has a selection bias toward"，机制解释也写了出来："protease resistance particularly for beta"。→ **一个代理指标被一条与设计目标无关的失效路径劫持了**。 **应对**：**不修这个 assay，而是加一个读不同物理量的正交筛选**——SEC + 质谱条码（"recently developed secondary screen that can"），并用它把 13,990 条蓝图设计的池子里能同时满足"耐蛋白酶 + 洗脱体积落在单体区间"的个体挑出来。 **代价**：作者自述新筛选的通量天花板更低——"fewer variants can be tested in parallel due to the reduced sensitivity and multiplexing capacity of mass spectrometry compared with next-generation DNA sequencing"；且两个筛选之间**没有做头对头比较**（"While we did not do a direct head-to-head comparison"），只能拿各自下游送进传统生物物理表征的比例来间接比。
5. **Rosetta LayerDesign 的一条默认规则系统性地压低了设计的稳定性**。做完蓝图支路后拿设计体和天然单体蛋白比埋藏非极性表面积，发现明显偏低（"was 62 Å 2 compared with 53 for the"），他们把根因定位到协议本身："The lower values compared with native structures"。→ 典型的**生成阶段的规则成了下游的隐性缺陷**。 **应对**：直接改规则——"we modified the layer settings"，再用 Rosetta 的 `aa_composition` 打分项把这些氨基酸连同 Thr、Met、Phe 的出现频率**偏置到天然统计值**；Met 与 Phe 之所以只进频率偏置、不进表面层放行名单，作者给了明确数字理由（天然链表面频率 0.22 与 0.26，远低于 Ile/Val/Tyr/Trp 的 0.60、0.69、0.52、0.72）。同时用片段来源的 PSSM 改善局部序列-结构匹配。 **代价**：改完后平均埋藏 NPSA 只回到 59 Å²（天然 62），**没完全补齐**；作者给的机制解释（因为核心太小，表面疏水残基通过与相邻表面残基相互作用来增加总疏水埋藏）也停留在讨论层面。
6. **自由幻觉做不出全 β**，于是必须在损失函数里加约束。他们用当时的深度网络幻觉法做前置：而"no folded proteins were obtained for all beta"（同期 α 与 α/β 是能出折叠单体的）。 **应对**：把方法改造成 **constrained hallucination**——"we adapted the hallucination"，具体做法是把 β 链中心残基（含 N 端盖帽螺旋）**钉成 motif**，只让环和转角自由幻觉；motif 项用交叉熵、非 motif 项用对背景分布的 KL 散度。他们**试过更短的 motif 并主动放弃**："We also tried shorter input"。 **代价**：约束越强就越不像自由幻觉，拓扑多样性部分回到了人工指定；且作者自己承认这套东西的**物理判据被藏进网络参数里不可读**——对比蓝图法"makes all of the concepts"。
7. **一个照抄天然蛋白的漂亮主意彻底失败，作者照实写了**。b5/b6 缺一个天然的稳定元件，他们在 Methods 里描述："For b5 and b6 designs, manual"。结果只有一句冷处理："Although such designs were"。 **应对**：**本文未解决**——作者没有解释为什么失败、也没有第二次迭代这个 motif，只是把 b5/b6 整体低成功率列了四种可能原因（"Overall, our lower success"），四个原因之间没有做区分实验。
8. **寡聚态本身在谱学上是模糊的**。蓝图支路第三个设计 17_bp_sh3 晶体结构做到了 1.6 Å，但 NMR 数据自相矛盾："There were nearly double the"。 **应对**：用**正交手段定寡聚态**（SEC-MALS 确认单体，"This design was monomeric as"），并把晶体里两条三链 β 片拼成六链片的现象解释成"这可能就是 NMR 看到的瞬时态"；同时把"边缘配对导致寡聚"上升为全 β 设计难做的总体解释。 **代价**：单体/二聚交换仍然是解释而不是观测；SEC 的单体/二聚判据本身只是按洗脱体积区间划的（15–17 mL 推定单体、13–15 mL 推定二聚），分辨率有限。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及各自在这条管线里负责什么）

- **骨架生成路线一（物理/人工规则）**：Rosetta blueprint + 蒙特卡洛片段组装，从伸展肽链起步。蓝图里显式写三样东西：二级结构及其长度、每个残基的 ABEGO 骨架二面角分箱、以及定义拓扑的骨架氢键配对；拓扑还由 **shear number S**（首末链的错位量）决定，S 决定链的倾角、桶直径和核心堆积方式。
- **骨架生成路线二（深度学习）**：**trRosetta 约束幻觉**。把要保留的 β 链核心（外加 N 端盖帽螺旋）当 motif，其余环与转角自由幻觉。损失是两项加权和 `L = w_M L_M + w_H L_H`：motif 项用相对目标几何的 one-hot 类别交叉熵，非 motif 项用相对**背景网络分布**的 KL 散度。序列用 one-hot MSA 张量表示，靠 reparameterization trick 把离散序列的梯度回传，恒定学习率梯度下降。当时 AlphaFold2 与 RoseTTAFold 还没可用。
- **序列设计**：Rosetta 柔性骨架协议 **FastDesign** + **LayerDesign**（core / boundary / surface 三层，非极性氨基酸原本只允许在 core）+ resfile 约束 β-turn 序列谱 + `aa_composition` 频率偏置 + 用 Rosetta 片段生成、再拿 BLOSUM62 伪计数与背景频率调整的位置特异性打分矩阵（PSSM）。
- **计算侧筛选器**：score_per_res、rama_per_res、omega_per_res、hbond_sr_bb、hbond_lr_bb、mismatch_probability、buried_npsa_per_res、pack、cavity_volume、sbuns、buns_all、worst9mer、sap_score、ff_metric（正向折叠能景漏斗程度）、RoseTTAFold 预测 lDDT、FastRelax 采样轨迹 rmsd 的标准差，以及一个预测蛋白酶稳定性的 logistic 回归模型。
- **新颖度与拓扑核验**：BLAST 对 NCBI 非冗余库（E-value 0.1）；DALI 与 TM-align 对 PDB 搜索（用来证明 b5/b6 骨架不是抄天然结构）。
- **湿实验（三级）**：一级＝酵母表面展示 + 蛋白酶解抗性 + 测序读数；二级＝SEC + 质谱肽条码；确证＝E. coli 表达 + Ni-NTA IMAC + SEC（Superdex 75 increase 10/300 GL，Akta Pure）+ SEC-MALS + far-UV CD（25 / 95 / 回到 25 °C）+ 1H-15N HSQC NMR；最终结构＝2 个溶液 NMR 结构 + 2 个高分辨晶体结构。
- **本文没有用的方法**：分子动力学、量子力学、自由能微扰；也**没有任何亲和力或催化活性测量**——这篇的终点是"是否折成设计的结构、以什么寡聚态存在"，不是功能。这一点决定了它的漏斗数字不能拿来校准任何活性类命中率。

### A. 路线一：Rosetta blueprint（先做，Fig 1–3）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 天然 SH3 / OB 代表结构（1KQ1、3P8D、1ZUY、4A2I、1C4Q 等）+ 手工搭建的 b5 / b6 蓝图 | 定二级结构长度、ABEGO 分箱与骨架氢键配对；SH3/OB 的 shear number 按天然代表结构取 | "Small beta barrel structures in" ；SH3 与 OB 取 S = 8 或 10 | 4 个目标拓扑（SH3、OB、b5、b6）的蓝图集合；转角限定为天然小桶里常见的四种 ABEGO 型 GG / AA / EA / AAG |
| A2 | b5、b6 的初版蓝图 | Rosetta fold assembly 试搭；搭不出目标三维结构的蓝图直接扔 | "blueprints which did not give" | b5 用链 1 与链 5 平行配对闭合、S = 8；收口失败后经加 bulge 解决 |
| A2b | 收口失败的 b5 蓝图 | **加 beta-bulge**（并在 b6 同样处理）让氢键配对沿弯折继续 | 图注判据：bulge 数 0→3 的 backbone H-bond（N–O）距离约束打分直方图，score 0 表示氢键距离建模正确 | "the incorporation of beta" |
| A3 | 每条蓝图 | 蒙特卡洛片段组装从伸展链生成骨架（Rosetta@home 分布式 + 内部集群） | 原文阈值："we extensively sampled structure and sequence space by running up to 10,000 independent trajectories of backbone generation followed by Rosetta sequence design calculations" | 每条蓝图最多 10,000 条独立骨架轨迹 |
| A4 | 生成的骨架 | Rosetta FastDesign + LayerDesign 出序列；resfile 锁 β-turn；关键位点强制（例如 3P8D 系设计的第 3 位强制 Phe）；b5/b6 另试 tyrosine corner 式的核心 Tyr/Trp | 初筛（能量分过 −50 的 Rosetta@home 设计）：score_per_res、rama_per_res、omega_per_res 三项低于各自均值，"mismatch_probabilty < 0.35,"，且 (hbond_sr_bb + hbond_lr_bb)/长度 < −0.75 | 削到能做能景计算的小集合；novelty 全部通过 "Sequence similarity to native" |
| A5 | 初筛设计 | 正向折叠（forward folding）能景计算：从伸展链做大规模 Rosetta ab initio 预测轨迹 | "Final designs were selected"，另加人工检视 | **80 条设计**下单做生物物理表征 |
| A6 | 表达纯化后的蛋白 | SEC 判寡聚态；far-UV CD 判有无结构、95 °C 判热稳定、回 25 °C 判可逆；1H-15N HSQC 判是否真有分散良好的尖锐峰 | SEC 单体判据："Based on calibration data,"；HSQC 判据＝峰数接近预期且尖锐分散 | "72 out of 80 designs expressed,"；"Eleven monomers and five dimers" |
| A7 | HSQC 合格的设计 | 解溶液 NMR 结构 / 长晶体 | 结构与设计模型的 Cα rmsd | "Both solution structures"；第三个 17_bp_sh3 晶体结构 rmsd 1.6 Å，"This design was monomeric as" |

### B. 一级 + 二级高通量筛选（同一蓝图空间，但换成阵列合成，Fig 1E / SI）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 常见 ABEGO 转角型的各种组合 | 用阵列寡核苷酸合成一次性造出上万条蓝图设计，再 E. coli 表达 | 无（生成阶段） | "A total of 13,990 blueprint" |
| B2 | 13,990 条 | **一级：酵母表面蛋白酶解抗性筛选**（NGS 读数） | 原文只给结果比例、未给抗性阈值本身："only six percent of the small" | **61 条**蛋白酶稳定设计进入下游（每条折叠组最多取前 10） |
| B2b | 各折叠组的 top 蛋白酶稳定设计 | 对命中者做传统表征，回头检验这个筛选本身可信不可信 | 检验结论："suggested the screen has a"，正文给的量是 77 percent of the top protease-resistant soluble designs were oligomers | 判该筛选对全 β 有系统性偏倚；其下游仅 "bp ps" 一行（24 条送测、13 可溶、4 单体/二聚） |
| B3 | 蛋白酶稳定的池子 | **二级：SEC + 质谱条码筛选**，直接读溶液里的可溶性与寡聚态 | 判据＝洗脱体积落在该设计单体态的预期区间 | "we were able to identify 99" |
| B4 | 99 条 SEC-MS 命中 | 取 19 条做全套传统生物物理表征 | 表达/可溶/SEC 单体峰/CD/HSQC | "we selected 19 for in vitro"；其中送 HSQC 的 6 条全部有折叠谱 |
| B5 | 99 条可溶单体 vs 全部已表征设计 | 事后比对序列与结构特征，找可提前用的计算判据 | 结论："the soluble monomeric designs" | 给出下一轮该用的三条筛子（局部匹配、Lennard-Jones、SAP），但**本文未前瞻验证** |

### C. 路线二：深度学习骨架 + Rosetta 序列（constrained hallucination，Fig 4–5）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | 188 条骨架（104 条已表征蓝图设计 + 61 条蛋白酶稳定设计 + 13 条额外 b5 + 10 条天然结构） | 定 motif 与非 motif：把 β 链**中间四个残基**（以及 N 端盖帽螺旋）钉住，其余按相对原长 ±2 个残基随机长度幻觉；要更长的插入就幻觉最多 6 残基的环、或对 ≥6 残基的环取原长 +1 | motif 保留量是试出来的："We also tried shorter input" | "To maintain a barrel-like" |
| C2 | motif + 随机序列 | trRosetta 预测全对残基的 6 个自由度，按 motif 掩码分两块算损失，梯度回传改序列；掩码只计入 Cβ 距离在截止内的残基对 | 掩码截止："The mask only included residues"，最远用过 20 Å（trRosetta 预测上限）；单序列输入可行性依据："trRosetta accurately predicts"；为补 MSA 信息，把待优化序列 logits 的 softmax 当 PSSM 喂进去 | "A total of 100 random-length" |
| C3 | 66,000 条幻觉输出 | 按折叠类 + 幻觉长度签名（例如 1KQ1_L5L8L6L4L6L1）分组，每组取总 loss 最低且 accuracy 最高的一条，做三维能量极小化 | "was selected for 3D structure" | **13,984 条**唯一长度设计的幻觉骨架 |
| C4 | 幻觉骨架 | **序列交给 Rosetta FastDesign 重做**，并修 LayerDesign 与组成偏置（见第 2.5 节） | 修完的分布目标：埋藏 NPSA 由 53 提到 "was 62 Å 2 compared with 53 for" 所指的天然水平附近（实测均值 59 Å²），"the average Rosetta energy per" | 每个设计跑 26 个 FastDesign 变体（`aa_composition` 权重 1.0 与 3.0，Trp 在表面/边界层放行与否不同），共 **45,761 条设计** |
| C5 | 45,761 条 | **五步串联筛选**（原文逐步给阈值） | 第一步：'pack ≥ 0.6, cavity_volume = 0, sbuns = 0, buns_all ≤ 10, buried_npsa_per_res ≥ 50' 与 score_per_res ≤ −3.0，并按折叠类 + 长度签名分组；第二步："Second, for each group, we"；第三步：pack ≥ 0.65、mismatch_probability ≤ 0.5、worst9mer ≤ 0.5、sap_score ≤ 30、score_per_res ≤ 均值；第四步："In the fourth step, we used a"；第五步："we filtered the designs using:" | "Up to the top 10 ranked designs" → **71 条**送测："71 were selected for experimental characterization based on the quality of their energy landscape funnels using the ff_metric" |
| C6 | 71 条送测设计 | 同一套四段湿实验漏斗 | 同 A6 | "Seventy designs expressed,"；"22 out of the 27 designs"；HSQC 有折叠谱 24/26 |
| C7 | 幻觉单体且折叠的设计 | 归类看哪类拓扑吃得住 | 结论："Most of the successful designs" | 1 条幻觉 OB 的晶体结构："We were able to obtain a"，其核心 45 残基段 rmsd 0.82 Å |
| C8 | 全部可用骨架 | 发布骨架库并用 AF2 指标给一个折叠概率标签 | 正文口径："which have a high probability" | "we provide here a scaffold set" |

### D. 四段漏斗的逐段比例（Table 1 全文原值；这是本文最该被记住的一张表）

Table 1 的列名逐字是："Designs Expressed Soluble"。

| 段 | 这段在筛什么（判据口径） | 蓝图 bp（80 条） | 蓝图-蛋白酶稳定 bp ps（24 条） | 蓝图-SEC/MS 条码（19 条） | 幻觉 + Rosetta（71 条） |
|---|---|---|---|---|---|
| 第 0 段 下单 | 计算筛选后决定合成的设计数 | 80 | 24 | 19 | 71 |
| 第 1 段 表达 | Ni-NTA 洗脱峰里有足量蛋白 | 90% (72/80) | 88% (21/24) | 100% (19/19) | 99% (70/71) |
| 第 2 段 可溶 | 可溶部分占**下单总数**的比例（前四列分母都是 N，非上一段） | 54% (43) | 54% (13) | 100% (19) | 96% (68) |
| 第 3 段 正确寡聚态 | SEC 单一弥散峰、洗脱体积落在单体或二聚区间 | 35% (28) | 17% (4) | 95% (18) | 77% (55) |
| 第 4 段 有结构（CD 25 °C） | far-UV CD 谱提示存在二级结构；分母＝实际做 CD 的条数 | 62% (16/26) | 67% (2/3) | 89% (17/19) | 81% (22/27) |
| 第 4b 段 热稳定（CD 95 °C） | 95 °C 谱不变；分母同上 | 8% (2) | 0% (0) | 11% (2) | 11% (3) |
| 第 5 段 真折叠（HSQC 25 °C） | 1H-15N HSQC 峰数接近预期且尖锐分散；分母＝实际做 HSQC 的条数 | 31% (11/35) | n/a | 83% (5/6) | 92% (24/26) |

Table 1 里 SEC-MS 行与幻觉行的原文数据逐字为："bp ps + MS barcode 100% (19/19)" 与 "Hallucinated 99% (70/71) 96%"。

**四段漏斗里最要紧的两个非直觉事实**：

1. **前四段的分母始终是下单总数 N（累计通过率），而 CD / HSQC 两列的分母换成了实际表征的子集**。所以"62% CD 折叠"和"54% 可溶"不能直接相乘当成端到端成功率——本卡的第 4 节台账对此单独标注。
2. **第 3 段（正确寡聚态）才是蓝图支路的断崖**：可溶 43 条里只有 28 条是单体或二聚（54% → 35%），而 SEC-MS 支路把这一段从 35% 抬到 95%、幻觉支路抬到 77%。作者的总结句是"With an 84 percent success rate"。
3. **两个支路的对比在正文里被写成一句话**："Roughly 90 percent of these"，而方法学上的归因是："The best results came from a"。
4. **天然与稀有拓扑之间也有落差**："We succeeded in the de novo"；而 b6 这个拓扑在投稿时"PDB 里查不到任何天然结构"："at the time of writing this"。

**这套流程的骨架值得单独记住**：生成端两条路线（人工物理规则 vs 网络约束幻觉）→ 计算端一串彼此正交的静态打分 → 湿实验端**四段各自独立读数**（表达、可溶、寡聚态、谱学折叠）→ 遇到一级代理指标被非目标失效模式（聚集）劫持时，**加一个读不同物理量的正交筛选而不是去修原筛选** → 最后把成功判据回写成计算特征（局部序列-结构匹配、Lennard-Jones、SAP）。

## 4. 关键数字台账（全部可在本地全文里搜到；出处为正文/表位置）

| 数值 | 含义 | 出处 |
|---|---|---|
| <70 aa、≤6 条 β 链 | 设计目标的硬边界（此前从未被从头做成） | Abstract 与 Introduction |
| S = 8 或 10（天然规律 S ≅ 2n） | SH3/OB 蓝图的 shear number | Results，Blueprint-Based Design 第 1 段 |
| 最多 10,000 条轨迹 / 蓝图 | 骨架生成采样量 | Results，Blueprint-Based Design 第 2 段 |
| 80 条设计 | 蓝图支路直接下单做表征的规模 | Results，蓝图段末；Table 1 bp 行 |
| **90% (72/80)** | 第 1 段：表达 | Table 1 bp 行 |
| **54% (43/80)** | 第 2 段：可溶（分母仍是 80） | Table 1 bp 行；正文 "72 out of 80 designs expressed," |
| **35% (28/80)** | 第 3 段：SEC 判为单体或二聚（19 单体 + 9 二聚） | Table 1 bp 行；正文同句 |
| **62% (16/26)** | 第 4 段：CD 25 °C 提示有结构（11 单体 + 5 二聚） | Table 1 bp 行 |
| **8% (2/26)** | CD 95 °C 仍保持结构（热稳定） | Table 1 bp 行 |
| **31% (11/35)** | 第 5 段：HSQC 峰数接近预期且分散尖锐 | Table 1 bp 行 |
| **74% / 40%** | 可溶设计里是寡聚体的比例 / 表达设计里聚集的比例 | Results，"Indeed, 74 percent of the" |
| 13,990 条 | 阵列合成、进高通量筛选的蓝图设计池 | Results，"A total of 13,990 blueprint" |
| **仅 6%** | 小 β 桶设计耐蛋白酶的比例 | Results，"only six percent of the small" |
| 77% | 耐蛋白酶且可溶的头部设计里寡聚体占比（筛选偏倚的证据） | Results，同一句括号内 |
| 99 条（85 SH3, 12 b6, 1 b5, 1 OB） | SEC-MS 条码筛在单体洗脱区间里命中的条数 | Results，"we were able to identify 99" |
| 24 送测 → 21 表达 → 13 可溶 → 4 单体/二聚 | 只走蛋白酶一级筛的 bp ps 行 | Table 1 bp ps 行（88% / 54% / 17%） |
| 19 条 → 100% / 100% / 95% / 89% / 11% / 83% | SEC-MS 支路的完整四段漏斗 | Table 1，"bp ps + MS barcode 100% (19/19)" |
| **84% / 74%** | SEC-MS 支路可溶单体成功率 / CD 确认率 | Results，"With an 84 percent success rate" |
| 188 条 motif（104+61+13+10） | 约束幻觉的输入骨架集 | Methods，Input motifs and hallucination strategy |
| β 链中心 4 残基；随机长度 ±2 | motif 保留量与环长采样范围 | Methods，同上 |
| 100 次 / run；**66,000** 条 trRosetta 输出 | 幻觉采样量 | Results，"A total of 100 random-length" |
| **13,984** 条 | 唯一长度签名的幻觉骨架数 | Results，"resulting in 13,984 hallucinated designs" |
| **45,761** 条 / 每个设计 26 个变体 | FastDesign 重设计后的总设计数 | Results，"the full set of designs generated with FastDesign (45,761 designs)" |
| 62 vs 53 → **59 Å²/残基** | 埋藏非极性表面积：天然单体集 vs 原设计 vs 改层设置后 | Results，"was 62 Å 2 compared with 53 for" |
| **−1.9 → −3.6 kcal/mol** | 平均 Rosetta 能量/残基（改序列协议后） | Results，"the average Rosetta energy per" |
| 71 送测 → 99% (70) → 96% (68) → 77% (55) → 81% (22/27) → 11% (3) → **92% (24/26)** | 幻觉支路完整四段漏斗 | Table 1，"Hallucinated 99% (70/71)"；正文 "Seventy designs expressed," |
| 7 OB / 7 SH3 / 3 b6 / 2 b5 | 幻觉支路里既单体又折叠的设计按拓扑分布 | Results，"Most of the successful designs" |
| ~90% vs ~30% | NMR 表征过的设计中幻觉 vs 蓝图的折叠比例 | Discussion 第 1 点，"Roughly 90 percent of these" |
| rmsd 1.2 / 2.3 / 1.6 / 2.38 Å（45 残基核心段 0.82 Å） | 四个已解结构与各自设计模型的距离 | Results（29_bp_sh3、33_bp_sh3、17_bp_sh3、170_h_ob） |
| <2.4 Å | 全文对实验结构对设计模型的距离上限声明 | Abstract，"with less than 2.4 Å rmsd from" |
| 29 / 59 | 170_h_ob 设计模型中幻觉时无约束的骨架残基数 | Results，"29 out of the 59 backbone" |
| BLAST E-value 0.1 | 新颖度判据（所有送测设计都无天然同源） | Results，"was not detectable using BLAST" |
| 蓝图初筛：Rosetta 总分 < −50；mismatch_probabilty < 0.35；buried_npsa_per_res > 50；(hbond_sr_bb+hbond_lr_bb)/长度 < −0.75 | 蓝图支路的计算筛选口径 | Methods，Selection |
| 五步阈值：pack ≥ 0.6、cavity_volume = 0、sbuns = 0、buns_all ≤ 10、score_per_res ≤ −3.0 → 每组前 100 → pack ≥ 0.65、mismatch_probability ≤ 0.5、worst9mer ≤ 0.5、sap_score ≤ 30 → 蛋白酶稳定概率 > 0.5 → ff_metric ≤ 20、RoseTTAFold lDDT ≥ 0.8、FastRelax rmsd SD < 0.1 → 每折叠前 10 | 幻觉支路的计算筛选口径 | Methods，Rosetta sequence redesign and selection |
| motif 掩码 Cβ 截止通常 10 Å、最大 20 Å | 约束幻觉损失函数里 motif 项的作用范围 | Methods，Loss function |
| TM-score 0.57、Cα rmsd 2.58 Å | b5/b6 生成骨架在整 PDB 里最像的天然结构（酵母线粒体核糖体大亚基链 I，长环连接） | Results（DALI 与 TM-align 搜索） |
| 单体 15–17 mL、二聚 13–15 mL | SEC 洗脱体积判寡聚态的窗口 | Methods，"Based on calibration data," |
| 约 −2.5 mL | 幻觉支路 FPLC 相对蓝图支路的洗脱偏移 | Fig. 5 图注 |
| ~230 nt | 一个小 β 桶可被压在单条可并行合成的长寡核苷酸里的长度 | Introduction 第 2 段 |
| 12,911 条（pLDDT > 88、model rmsd < 2.0） | 发布的小 β 桶骨架库及其折叠概率判据 | Discussion 末段 |

## 5. 结论——作者说了什么

1. **第一次从头做出小 β 桶**，而且四类拓扑全做成了："We succeeded in the de novo"；实验结构与设计模型的距离在 2.4 Å 以内、热稳定性高。
2. **深度学习出骨架 + Rosetta 出序列优于纯 Rosetta**："Using deep learning for backbone generation and Rosetta for sequence design yielded higher design"；最好的组合是 "The best results came from a"。
3. **两类方法的取舍**：物理规则法可控但繁、要求预先懂设计规则；网络法简单且多样但判据埋在参数里不可读。原文对蓝图法的评语包含 "makes all of the concepts"，对网络法是 "the information guiding design"。
4. **正交高通量筛选能挑出可溶单体**："With an 84 percent success rate"；并且随着深度学习设计成功率提高，"using SEC–MS as a primary"。
5. **折叠决定因素三条**：bulge 对收口必需（"Inclusion of strategically"）；核心太小时**表面疏水残基反而助折叠**（"incorporation of surface"）；真难点是疏水埋藏与桶骨架氢键的平衡（"A challenge in designing small"）。
6. **自然界折叠的采样率不等于可设计性**：b6 做成功说明 "Successful designs of the b6"，但 b5/b6 成功率仍低于广泛存在的 SH3/OB，作者列了四个未加区分的候选解释。
7. **落点是给 binder 设计补形状空间**：这些骨架 "complement the largely helical"，并释放 12,911 条骨架库。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的方法学贡献是把寡聚态当成一道独立闸口**。四段漏斗里只有第 3 段是蓝图支路崩掉的地方（54% → 35%），而它既不由 Rosetta 能量、也不由结构预测置信度控制。→ 对我们：凡"分子聚成多体、或粘在固相/细胞表面"能够冒充成功信号的环节（结合信号、荧光信号、抗蛋白酶信号），都必须配一个**读不同物理量**的正交读数；我们的等价物就是产物化学身份不能由表达量或荧光代理。
2. **一级代理指标被非目标失效模式劫持时，他们的处置是换一个而不是修它**。蛋白酶抗性失效的机制写得很明白（酵母表面聚集也抗蛋白酶），他们没有去优化蛋白酶条件，而是引入 SEC-MS 这个读别的量的筛选。→ 这与调阈值救指标的本能相反：物理上不成立的代理，调阈值只会把偏倚放大。
3. **两支路对比的分母不同，90% vs 30% 不能当方法提升倍数引用**（见第 7 节）。稳的对比是同一口径、以下单数 N 为分母的前三段：35% → 95%（换筛子）与 77%（换生成器）。
4. **生成阶段的默认规则会在下游变成系统性缺陷，这是第二次独立证实**：B09 里 Rosetta 单体能量因生成阶段已用过而失去判别力；这里是 LayerDesign 表面不放疏水的规则把埋藏 NPSA 压到低于天然、直接压低成功率。→ 对我们：任何在召回或生成阶段用过的先验，都要显式检查它有没有把下游判据的分布推向不可挽回的一侧。
5. **本文没有 MD、没有 QM，也没有任何活性或亲和力数字**，终点是结构与聚集态。因此它对催化能否被设计不提供概率证据；可借鉴的只有漏斗分段方式与代理指标失效的处置方式。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自己写出来的**

- b5 / b6 成功率显著低于 SH3 / OB，而原因**没有做区分实验**，只给了四个并列可能："Overall, our lower success"。
- 照抄天然的 tyrosine corner 元件**整批失败**："Although such designs were"，正文未给解释。
- 设计的 beta-bulge 不保证在实验结构里出现（"The differences in the C"），且部分 b5 设计根本没闭合（"Some b5 designs that were"）。
- 换用的 SEC-MS 筛选通量更低："fewer variants can be tested in"；而且两个高通量筛选之间**没做头对头比较**："While we did not do a direct"。
- 热稳定性极差：四行数据的 CD 95 °C 折叠率只有 8% / 0% / 11% / 11%——**可溶单体设计几乎都不耐高温**，本文只解决折叠与寡聚态，不解决稳定性。

**我们读出的**

1. **最可疑的一处判据：Table 1 的分母在列与列之间换了**。前三段（Expressed / Soluble / Monomer or dimer）是**以下单总数 N 为分母的累计比例**（如 bp 行 72/80、43/80、28/80），而 CD 与 HSQC 两列换成**实际送去该表征的子集为分母**（16/26、11/35、22/27、24/26）。于是 Discussion 里那句 "Roughly 90 percent of these" 是拿 24/26 比 11/35 —— **两个分母都是作者自选的表征子集**，而这两批设计在上游受到的计算筛选强度根本不同（幻觉支路过了五步含蛋白酶稳定性回归模型的闸口，蓝图支路只过 ff_metric 加人工检视）。所以这个 ~90% vs ~30% 是**混淆了筛选强度的对比**，不能当作骨架生成器质量的效应量引用。要引用只能引同口径的前三段（35% → 77% → 95%）。
2. **HSQC 折叠判据是目测**：判据措辞是 close to the expected number of well-dispersed sharp peaks，全文没给峰数偏差容许度、化学位移分散度或线宽的定量阈值；同一支路里还有 b6 要在 37 °C 才拿到分散良好的谱，说明判据在不同设计间不统一。
3. **寡聚态主要靠 SEC 洗脱体积区间推定**（15–17 mL 单体、13–15 mL 二聚），只有一个设计（17_bp_sh3）用 SEC-MALS 直接确认；其余 monomer or dimer 都是推定，且 SEC 分不出更高阶寡聚与聚集体。
4. **发布骨架库用的折叠概率标签没有本文内的自证**："which have a high probability" —— 本文没有任何对这 12,911 条设计的实验验证，"within our group" 是未随文给出的内部经验。
5. **DL 一侧的结论建立在较弱的网络上**：骨架生成用的是 trRosetta（原文明写 AlphaFold2 与 RoseTTAFold 当时尚未出现），所以"深度学习骨架更好"这一结论的证据强度只到 2022 年的距离几何网络，不宜直接外推到 RFdiffusion 时代。
6. **全文没有 MD、没有 QM、没有任何功能读数**：它证明的是"能折成设计的结构且以单体存在"，不证明有任何活性或结合能力；把这两件事之间的鸿沟当成已跨越是本卡最大的风险。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **四段漏斗的分段记账方式（对应 DP2R 标准 G0/G6）**：把候选递减按**彼此正交的物理事件**分段，每段单独报绝对条数与自己的分母，不许把累计比例和子集比例混在同一列里。我们的等价四段应写成：设计/召回数 → 表达合格 → 可溶且单体（或不聚集）→ **产物被 LC-MS/MS 确认**。任何跨段的比例都要注明分母是原始 N 还是实测子集。
2. **把非目标失败模式当一等公民量化**：本文最有价值的两个数是 74% 可溶设计为寡聚体、40% 表达设计聚集，它们不属于折错但吃掉了大半预算。→ 我们应对等地报告：无表达、包涵体、非特异起点（游离 UTP）、环化竞争（第二枚 ATP）各占多少，而不是只报折叠分或结构置信度。
3. **代理指标失效时的处置规则**：当一个快代理被一条与设计目标无关的路径劫持（蛋白酶抗性 ← 酵母表面聚集），做法是**增加一个读不同物理量的正交筛选**（SEC-MS），并公开承认通量代价；而不是调该代理的阈值。→ 我们的同类情形：若用荧光/互补报告基因代理"催化发生"，必须先证明报告信号不被非催化事件产生（无酶对照、失活位点对照），否则加一条产物化学的二级筛选。
4. **成功组 vs 全体做事后特征对比来产下一代筛子**（局部序列-结构映射、Lennard-Jones、SAP 三项），并明写"应当能提升未来成功率"但本文未前瞻验证。→ 我们的纪律：这样得到的特征必须走一次前瞻小批次验证才能进漏斗，否则只登记不启用。
5. **生成规则本身要拿天然分布来校准**：NPSA 案例（62 vs 53 → 改层设置 → 59）示范了当某默认约束系统性把关键物理量推向偏离天然的一侧时，正确做法是**改规则 + 用组成偏置把分布拉回来**，并在改后重新测量分布。
6. **每个计算闸口都要写清阈值与它在第几步**：本文的幻觉支路五步筛选（含 pack、cavity_volume、sap_score、ff_metric、RoseTTAFold lDDT、FastRelax rmsd SD、蛋白酶稳定回归概率 > 0.5）是一份可直接照抄格式的"阈值链台账"，我们的漏斗也应长成这种一串显式阈值的形式。

**不可迁移（为什么不能照搬）**

1. **pLDDT > 88 / model rmsd < 2.0 / ff_metric ≤ 20 / mismatch_probability < 0.35 / sap_score ≤ 30 全是"会不会折成设计结构"的判据，与催化无关**。UAA 的成功要三步化学事件都对且副反应不发生，结构自洽既不必要也不充分。DP2R 标准 §2 明确禁止把 binder / 折叠类的 pAE、pLDDT、RMSD 阈值当成酶活判据或成功概率使用；本文甚至没有结合体，更没有酶。
2. **92% 与 31% 的 HSQC 折叠率不能换算成我们的任何命中概率**：它们的分母是自选的表征子集（24/26、11/35），且上游筛选强度不同（第 7 节第 1 条）；更根本的是本文没有任何功能读数。引用只许引其**漏斗分段结构**，不许引数字做校准。
3. **酵母展示 / SEC-MS 式大通量在产物化学上不存在**：一次 LC-MS/MS 只能处理少量构建体，我们漏斗末端要最大化的是**信息量**（机制多样性 + 失活对照 + 副产物谱），不是样本数；照搬通量口径会得出"我们不可能做筛选"的错误结论。
4. **本文的骨架生成用的是 trRosetta，不是扩散模型**；把它当作"当前深度学习骨架生成能力"的证据会同时低估生成质量与判据强度，比较时须另找 RFdiffusion 时代的同类工作（本文无）。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/betaBarrel2023.txt

- 本地纯文本：`data/interim/baker_lit/ft/betaBarrel2023.txt`（PMC10089152 的 JATS/XML 去标签纯文本，66,412 B / 247 行；核验时经 `scripts/litcards_text.py` 的 `norm()`：HTML 实体解码 + 弯引号/破折号/数学减号转 ASCII + 拉丁 alpha 转 a + 空白折叠，**不改词、不改大小写**）。
- 结构可得性：原文写 "The structures for 29_bp_sh3"（7UWY、7UWZ；BMRB 31017、31018），17_bp_sh3 与 170_h_ob 为 7UR7、7UR8；幻觉代码在 sokrypton/TrDesign_partialhal；骨架库与筛选数据在 Zenodo 归档 doi:10.5281/zenodo.6529943，正文句为 "we provide here a scaffold set"。
- 对照底稿行号：`sources/baker.md:147–158`（原卡，已含 80→72→43→28→16 与 74%/40% 两条关键数字）；引用汇总表 `sources/baker.md:612`（第 6 段确证行，[B11] 走 X 射线 / NMR HSQC）、`sources/baker.md:642`（2023 年漏斗数字对照，[B11] 小 β 桶四段递减）。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法 / 计算筛选判据 / 阈值数字`；第 3 节 D 表与第 4 节 ↔ `候选数递减 / 实验命中率 / Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。
- 引句核验方式：与 `scripts/verify_literature_cards.py` 同一逻辑——卡内被直双引号包住、不含中日韩字符、≥20 字符且含 ≥12 个字母的片段，逐字（经 `norm()`）在该编号登记的每一份本地全文里查找，任一不命中即 FAIL。本卡登记的全文只有 `betaBarrel2023.txt` 一份（`sources/baker.md` 是登记底稿、按脚本规则不计为全文）。
- 写卡过程中被逐字核验抓出并改正的四处抄写错误：把原文 In the fourth step 误写成小写开头；把 whose C β were within a cutoff 的空格漏成 Cβ；有一处把正文里的 with short loops 省略后当原句引用；以及把同一句写重复一遍。全部按原文改回。**本卡所有英文引句为原文复制粘贴，无跨句拼接、无省略号冒充、术语未加英文引号。**

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 108 条逐字引句来自许可受限的第三方来源（B01、B11；CC_BY_NC_ND、PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（de novo 折叠/骨架设计；物理规则法与深度学习法的正面对照）
target=SH3、OB 两种天然常见拓扑与 b5、b6 两种 up-and-down 小 β 桶（≤6 条 β 链、<70 aa）；设计对象是折叠与寡聚态本身，无外源靶点、无功能位点
backbone_generation=路线一 Rosetta blueprint + 蒙特卡洛片段组装（从伸展链起步，蓝图给定二级结构长度、ABEGO 骨架二面角分箱、骨架氢键配对与 shear number S）；路线二 trRosetta 约束幻觉（钉住 β 链中心残基与 N 端盖帽螺旋、环与转角按 ±2 残基随机长度自由幻觉）；两条路线的序列都由 Rosetta FastDesign + LayerDesign 出，幻觉支路序列重做时改层设置并加 aa_composition 频率偏置
computational_filters=蓝图支路：score_per_res、rama_per_res、omega_per_res、hbond_sr_bb+hbond_lr_bb、mismatch_probability、buried_npsa_per_res、ff_metric（正向折叠能景漏斗）、BLAST 对 NCBI nr 的新颖度；幻觉支路五步：Rosetta 过滤指标组（pack、cavity_volume、sbuns、buns_all、buried_npsa_per_res、score_per_res）→ 按折叠类与长度签名分组取前 100 → 更严的 pack/mismatch/worst9mer/sap_score → logistic 回归预测蛋白酶稳定 → ff_metric + RoseTTAFold 预测 lDDT + FastRelax 轨迹 rmsd SD；事后特征对比另外给出局部序列-结构映射、Lennard-Jones、SAP 三项候选筛子
thresholds=蓝图初筛：Rosetta 总分 < −50，score_per_res/rama_per_res/omega_per_res 低于各自均值，mismatch_probabilty < 0.35，buried_npsa_per_res > 50，(hbond_sr_bb+hbond_lr_bb)/长度 < −0.75；幻觉五步：pack ≥ 0.6、cavity_volume = 0、sbuns = 0、buns_all ≤ 10、score_per_res ≤ −3.0 → 每组前 100 → pack ≥ 0.65、mismatch_probability ≤ 0.5、worst9mer ≤ 0.5、sap_score ≤ 30、score_per_res ≤ 均值 → 蛋白酶稳定概率 > 0.5 → ff_metric ≤ 20、RoseTTAFold lDDT ≥ 0.8、FastRelax rmsd SD < 0.1 → 每折叠按 ff_metric 取前 10；约束幻觉 motif 掩码 Cβ 截止通常 10 Å（最大 20 Å）；SEC 判寡聚态 15–17 mL 推定单体、13–15 mL 推定二聚；发布骨架库判据 pLDDT > 88 且 model rmsd < 2.0；新颖度 BLAST E-value 0.1
md_used=否（全文无分子动力学；ff_metric 是 Rosetta ab initio 采样轨迹的能景漏斗统计量，不是 MD 模拟）
qm_used=否
experimental_methods=阵列寡核苷酸合成基因（蓝图由 IDT 合成入 pET29b+，幻觉为 eBlock 片段 + Golden Gate 克隆 + Sanger 验证）→ E. coli Lemo21(DE3) 自诱导表达 + Ni-NTA IMAC 纯化 → SEC（Superdex 75 increase 10/300 GL，Akta Pure FPLC）+ SEC-MALS → far-UV CD（25/95/回到 25 °C）→ 1H-15N HSQC NMR（25 °C，部分 b6 在 37 °C）→ 2 个溶液 NMR 结构 + 2 个晶体结构；高通量侧为酵母表面展示蛋白酶解抗性筛选（NGS 读数）与 SEC + 质谱肽条码二级筛选
pipeline_counts=蓝图支路：每条蓝图最多 10,000 条骨架轨迹 → 80 条送测 → 72 表达 → 43 可溶 → 28 单体/二聚 → 16/26 CD 有结构（2/26 耐 95 °C）→ 11/35 HSQC 折叠 → 2 个 NMR 结构 + 1 个晶体结构；高通量蓝图池：13,990 条 → 仅约 6% 耐蛋白酶（下游共 61 条蛋白酶稳定设计）→ 24 条 bp ps 送测（13 可溶、4 单体/二聚）→ SEC-MS 命中 99 条（85 SH3、12 b6、1 b5、1 OB）→ 19 条复测（19 表达、19 可溶、18 单体/二聚、17/19 CD、5/6 HSQC）；幻觉支路：188 条输入 motif → 每次 run 100 条随机长度幻觉、共 66,000 次 trRosetta 输出 → 13,984 条唯一幻觉骨架 → 45,761 条 FastDesign 设计（每骨架 26 个变体）→ 71 条送测 → 70 表达 → 68 可溶 → 55 单体/二聚 → 22/27 CD（3/27 耐 95 °C）→ 24/26 HSQC 折叠 → 1 个晶体结构；另发布 12,911 条骨架库
hit_rate=断崖在第 3 段（正确寡聚态）：蓝图 35% vs SEC-MS 支路 95% vs 幻觉支路 77%；HSQC 折叠率蓝图 31%（11/35）vs 幻觉 92%（24/26），作者概述为约 90% 对约 30%（两个分母均为自选表征子集，不可当提升倍数引用）；主失败通道不是折错而是聚集与寡聚：可溶设计的 74% 为寡聚体、表达设计的 40% 聚集；蓝图设计仅 6% 耐蛋白酶且耐蛋白酶头部命中里 77% 是寡聚体（一级代理筛选被偏倚劫持）；b5/b6 成功率低于 SH3/OB；四组 CD 95 °C 热稳定率仅 0–11%
best_metric=未记录（本文无亲和力亦无催化活性指标，终点为结构一致性；最好的结构精度是设计模型对实验结构 Cα rmsd 1.2 Å（29_bp_sh3 溶液 NMR），170_h_ob 核心 45 残基段 0.82 Å；全文总体声明为小于 2.4 Å）
cost_or_stat_note=正文未给 GPU/CPU 单价、机时或金额，只给定性比较：约束幻觉生成高质量骨架所需计算少于 Rosetta 蓝图法，而蓝图片段组装（尤其含较多非局部相互作用时）与全原子设计、松弛末段耗时；算力来自 Rosetta@home 分布式 + 本所集群 + TACC；采样量为每条蓝图最多 10,000 条骨架轨迹、幻觉共 66,000 次 trRosetta 输出、每个幻觉骨架 26 个 FastDesign 变体（合计 45,761 条设计）
role_in_timeline=把漏斗失败的主因从打分不准补成聚集/寡聚这类不属于折叠失败的路径，并第一次完整量化表达→可溶→正确寡聚态→谱学证明折叠的四段递减比例（80→72→43→28→16/26→11/35）；同时给出 blueprint 物理法与 constrained hallucination 深度学习法的正面对照，把深度学习出骨架 + Rosetta 出序列定为本组后续默认（并明确其代价是用物理透明性换程序简单与准确度）；一级代理指标失效时改用读不同物理量的正交筛选而非调阈值，是可复用的方法学先例；释放的 12,911 条 mini-barrel 骨架库为 [B08][B09][B12][B23] 一系 binder 设计补上长期缺位的 β 形状空间
source_pointer=data/interim/baker_lit/ft/betaBarrel2023.txt（PMC10089152 去标签纯文本，66,412 B）；登记底稿 sources/baker.md:147-158，汇总表 sources/baker.md:612 与 :642；结构 7UWY/7UWZ/7UR7/7UR8，BMRB 31017/31018，代码 sokrypton/TrDesign_partialhal，骨架库 doi:10.5281/zenodo.6529943
CSV回填-->
