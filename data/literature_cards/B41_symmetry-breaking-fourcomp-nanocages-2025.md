# [B41] 把「对称破缺」这个设计意图翻译成可算约束——四组分 T=4 蛋白纳米笼（该成的界面要成 + 不该成的界面不许成）

Lee S, Kibler RD, Ahn G, Hsia Y, Borst AJ, Philomin A, Kennedy MA, Huang B, Stoddard B, Baker D（华盛顿大学 IPD / HHMI / POSTECH / Fred Hutch）
Nature 638:546-552（Crossref issued 2024-12-18，期号 8050，纸质刊期 2025-02-14）· DOI 10.1038/s41586-024-07814-1 · PMID 39695226 · PMCID PMC11821509
开放获取（CC BY 4.0）· https://pmc.ncbi.nlm.nih.gov/articles/PMC11821509/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B41**（组：Baker组；`年份=2024`，venue 字段同时记 Crossref issued=2024 与 EPMC pubYear=2025） |
| 本文取回方式 | Europe PMC `fullTextXML`（见 `data/literature_cards/inventory.json` B41 记录：`fetch_channel=epmc_fulltext`） |
| 本卡唯一底稿 | `data/interim/baker_lit/ft/fourcomp_cages2025.txt`（56,632 B，85 行；B41 在 `sources_map.json` 里登记的**唯一**本地全文；`data/literature_cards/fulltext/` 下**没有** B41 文件） |
| 对照记录（非全文） | `sources/baker.md:539-550`（原卡）与 `sources/baker.md:648`（2025 年时间线行） |
| 证据级别 | **全文级**（本卡所有英文引句均在该底稿逐字命中，条数与结果见第 9 节门禁命令） |
| 未取到的部分 | 补充信息（Supplementary information 1-4、Supplementary Figs 1-51、Supplementary Tables 1-13）、Extended Data 图、方法学细节原文（计算设计全部写在小信息里）。凡涉及 RPXdock 分数阈值、AF2 负向判据通过率、投测前的计算库规模，正文只给了"用哪些工具"没给数字，本卡明写"原文未给阈值" |
| 正文与登记记录的出入 | 见第 7 节末尾三条（MD 用途、`2%` 偏差数字归属、`14 组`口径）；本卡**不改** `sources/baker.md` 与 CSV |

## 1. 这篇到底解决什么（一句话）

自然界的高三角化数（T>1）衣壳靠"对称破缺"（同一亚基换象 = quasisymmetry，或近缘但不同序列的亚基 = pseudosymmetry）才能把笼子做大；而计算设计过去只会做**完美点群对称**的一/二组分笼。这篇的做法是：**把"对称破缺"这个意图翻译成三条可以逐条检查的界面约束**——用几何完全相同、序列不同的 ABC 型假对称异源三聚体替换同源三聚体，借此精确指定"哪一条三聚体–三聚体界面必须消失、哪一条异源界面必须形成、哪两条同源界面必须不形成"，从而按层级把 T=1 笼拆出可独立验证的"冠"（crown）子结构，再用冠 + 一个同源三聚体组装出**四组分、六个不同界面**的 T=4 笼（四面体 48 亚基/33 nm、八面体 96 亚基/43 nm、二十面体 240 亚基/75 nm），用电镜（含冷冻电镜 6.87 Å 与 13.15 Å）确认结构，并做了 ASGPR 融合笼被肝细胞内吞的概念验证。

原文对自己动机的两句关键交代："the design of assemblies with multiple identical or nearly identical chains in non-symmetry equivalent positions is an outstanding challenge"；以及选路线的理由——"we reasoned that using closely related but distinct subunits (pseudosymmetry) would have the advantage over quasisymmetry as it avoids the complexity of designing single subunits with multiple distinct states and sets of interactions"。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **「对称破缺」本身不是可算量，必须先把意图降解成界面级的正/负约束。**
   现象/证据：完美点群只有那几个（"Although there are no other point group symmetries"），而多链非等价位置的设计是公认难题（"the design of assemblies with multiple identical or nearly identical chains in non-symmetry equivalent positions is an outstanding challenge"）。
   他们做了什么：把破缺变成三条可实现的动作——(a) 用几何不变的假对称异源三聚体替换同源三聚体："This can be accomplished by substituting the homotrimers with geometrically identical (that is, pseudosymmetric) heterotrimers composed of three distinct chains with different amino acid sequences."；(b) 明确要消掉哪一条界面："Extracting pentons from T = 1 cages requires that one of the three interfaces joining each trimer with its nearest neighbours be eliminated."；(c) 把消掉的那面朝外的臂表面改成极性，物理阻断再结合："The surface of the arm of ch_C, which points outwards from the crown, was redesigned to be entirely polar."；(d) 闸口里同时写正向与负向条件："We selected designs for which AF2 predicted the ch_A–ch_B interface with RMSD < 2 Å and did not predict the ch_A–ch_A or ch_B–ch_B homodimer interfaces to form"。
   仍留下的代价：负向那半句没有任何数值阈值，也没有对"AF2 判为不形成的界面"做过实验反验；本卡在第 7 节把它标为未闭合。

2. **不做直接设计高 T 笼，改为层级化拆步——代价是实验总量放大。**
   现象/证据：作者写明的理由是 "a design strategy that started with creating T = 1 architectures from homotrimers, and then extended these to T = 4 by inserting pseudosymmetric heterotrimers, would be more robust than directly designing for higher T-number cages, as subsets of the cage forming interfaces could be experimentally validated independently"。
   他们做了什么：把整条链拆成多级各自独立送测（带臂同源三聚体 39 个 → host×guest 组合 28 种中实测 18 种 → ABC 异源三聚体 5 个 → T=1 笼 19 个 → 冠 19 组 → T=4 笼 14 组），每一级都用 SEC / nMS / SDS-PAGE / nsEM 单独确认后才进下一级。
   仍留下的代价：任一级窄就是整链瓶颈——二十面体 T=1 只有 1/4 过关（"One of the icosahedral cages, Ico T = 1 -1, had a single peak on SEC and was close to the design model by nsEM"，同一句后面承认 "although imperfectly formed cages were also observed"），C5 冠只有 2/7 在 SEC 上给出预期洗脱体积；作者没有给出"层级化比直接设计省了多少"的对照。

3. **假对称化不是任意可做的：界面必须先移植进同源背景验证兼容性。**
   现象/证据：异源三聚体靠界面移植生成——"To design pseudosymmetric heterotrimers, we used an interface transplantation approach"，"A homotrimer was selected as the host scaffold and three different protomer–protomer interfaces from different homo-oligomers (guests) were transplanted onto the subunit–subunit interfaces"；兼容性用一条前置检验处理："We first checked the compatibility between a host and a guest in the homo-oligomer context by symmetrically transplanting the guest interface into the host."
   他们做了什么：只挑高表达且均一的骨架做杂交（"We selected highly expressed and homogenous homotrimers for hybridization: seven with arms (BGL0_A10, BGL0_A11, BGL17_A31, BGL17_A32, BGL18_A35, BGL19_A38 and BGL19_A39) as host scaffolds and four without arms (BGL0, BGL17, BGL18 and BGL19)"）；实测后收敛到一个通用宿主——"The BGL17_A32 host backbone was found to be compatible with multiple guest interfaces"。
   代价：组合空间按现实比例被削掉（"We experimentally characterized 18 of the 28 combinations"；其中 "14 of 18 had SEC peaks at the correct oligomeric size"、"11 of 18 had strong nMS signals at the correct masses"；最终 "Three of five heterotrimers" 形成 ABC 型）。作者把路线的适用条件写成一句带前提的承诺——"This approach to creating pseudosymmetric hetero-oligomers should be readily applicable to symmetric protein oligomers quite generally, if the amino acid sequence of the protomer–protomer interface can be diversified."

4. **负向闸口在八面体分支上几乎不筛东西（判据饱和），他们没有收紧阈值，而是换了工具。**
   现象/证据：正文原句——"Very few initial designs for the octahedral architecture did not form predicted self interfaces"。也就是"同源界面不形成"这条判据在该分支上通过率接近 100%，等于没有筛子。
   他们做了什么：不去调 AF2 判据本身，而是引入显式负设计——"to decrease the probability of self-interaction, we performed explicit negative design using proteinMPNN"，用途写得很直白："against the predicted self interfaces"。
   代价：全文没有给出这一步过滤掉多少条、也没有报"负设计后 self 界面不形成的预测比例提升了多少"；八面体分支真正起作用的是**生成端**（负设计）而不是**筛选端**（AF2 判据），但正文口径仍统一写成 "that passed the AF2 filters"。

5. **脱靶结构没有被消灭，只被降级成次要物种。**
   现象/证据：冠这一步的重设计是被可能的脱靶结构逼出来的——"this was necessary to avoid a potential off-target structure possible with the original C2 interface"；T=4 投测后 "the major species in each case was the designed T = 4 structure; we also observed minor species of smaller off-target T = 1-like cages"。
   他们做了什么：用 nsEM 2D class averages / 3D 重建分辨主次物种，并在冷冻电镜数据表里把脱靶小笼一并登记（Extended Data Table 7 的说明行原文即 "T = 4 cages (Oct T=4 -3 and Ico T=4 -4) and off target small cages (T = 1 cages) found in Oct T=4 -3 and Ico T=4 -4 systems"）。
   代价：成功判据是"major species"这一**半定量**口径，正文没有给主/次物种比例；且 DLS 看不见这些脱靶物——"the smaller T = 1 contaminants observed by electron microscopy were not resolved by DLS probably due to the screening effect of the larger of two similarly sized particles"，所以稳定性结论只适用于主物种。

6. **设计构象与实测取向不一致（倒装），他们把模型翻过来拟合而不是当作失败。**
   现象/证据：二十面体 T=4 的冠与三聚体取向反了——"but the orientations of the C5 crowns, and homotrimers appeared inverted from the design model"。
   他们做了什么：不重设计，而是检验倒装构象能否解释密度："The design model with inverted components fits well into the cryo-EM density following relaxation"。四面体/八面体留下同一类偏差——"overall, the relaxed model matches well with the design model, with the exception of a slight twist of the overall structure resulting from curvature in the arm near the homotrimer–heterotrimer interface"，"but a slightly curved connection between crowns and homotrimers leading to a slight twist of the overall structure"。
   代价：**本文未解决**。"为什么会倒装"（即 RPXdock + AF2 选出的界面集是否唯一解）没有任何分析，只给了"能装进去"的相容性证据。

7. **四组分体系慢组装导致不均一，他们用一条纯经验的时间参数补救。**
   现象/证据：Methods 里专门为二十面体笼写了一段——"we kept the IMAC-eluted sample at room temperature for 24 h before concentrating and running SEC. The 24-h equilibration was important to generate homogeneous samples"，理由是自陈的推测："Given the complexity of this sample (4 components, 6 different interfaces and 240 subunits), a relatively slow assembly kinetics seems reasonable"。
   他们做了什么：只对 Ico T=4-4 加 24 h 室温熟化，其余体系照常（"For all other systems, the equilibration time is not a critical issue"）。
   代价：单点经验，没有做时间梯度实验；作者自己保留猜测口径——"we think that an even longer equilibration time could be helpful to further increase the level of homogeneity"。

8. **His 标签纯化本身会优先捞上非特异的多 His 复合物。**
   现象/证据："as this was found to improve the yield of single-His-tagged complexes over nonspecific multiple-His-tagged complexes, which can arise at high concentrations and probably dominate binding to the Ni-NTA resin"。
   他们做了什么：为异源复合物单独配 Het 变体的裂解/洗杂/洗脱缓冲液，并用 TEV 切标签后再过一次 SEC——"After TEV cleavage, samples were exchanged into lysis buffer and passed over a Ni-NTA gravity column and washed with 10 ml lysis buffer"。
   代价：机理停留在 probably 这一措辞；化学计量靠 SDS-PAGE 灰度间接控制——"the amount of each protein was estimated by SDS–PAGE gel densitometry, and appropriate amounts of culture were combined to achieve mixtures with stoichiometric amounts of the three chains"，没有对复合物链比做绝对定量。

9. **三个 T=4 笼里，叙述最完整的四面体反而拿不到高分辨率结构。**
   现象/证据："we were not able to conduct cryo-EM for T = 4 tetrahedral cages, because the cages were aggregated when they are concentrated higher than"，随后一句给出可稳定工作的浓度上限（数值见第 4 节台账）。
   他们做了什么：放弃该分支冷冻电镜，只保留负染电镜证据，把冷冻电镜资源转向八面体与二十面体。
   代价：三个 T=4 笼的证据等级不同（6.87 Å / 13.15 Å / 仅 nsEM），正文却并列叙述；Tet 的均一性判断只能靠 2D 类别平均支撑。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **几何/对接**：RPXdock（"The source code from RPXdock for the protein docking is freely available at https://github.com/willsheffler/rpxdock"），用于沿对称轴采样旋转+平移；层级化 building-block fusion（把螺旋重复蛋白臂刚性融到三聚体末端）用来调笼径与界面几何。
- **序列设计**：ProteinMPNN（"The source code from ProteinMPNN for the sequence design is freely available at https://github.com/dauparas/ProteinMPNN"）；后期在八面体分支上加 **explicit negative design**（同一工具，但目标是"不该成的界面"）。
- **评估闸口（本文的方法学核心）**：AF2 界面预测的**双向判据**——正向 = 目标异源界面 RMSD 阈值；负向 = 同源界面不形成。正文另有一处概括口径："Designs were filtered based on the formation of the designed interface, and lack of formation of the self interfaces, in AF2 predictions"。
- **假对称化**：界面移植（interface transplantation，host/guest 框架），沿用先前 pseudosymmetric 杂合寡聚物工作。
- **实验侧**：E. coli 表达（两条方案：Protocol 1 分开发再按比例混合、Protocol 2 共转化）；IMAC + SEC；SDS-PAGE（含灰度定量控化学计量）；LC-MS 完整分子量；nMS 寡聚态；SAXS；负染电镜（Talos L120C 120 kV + CryoSPARC）；冷冻电镜（Titan Krios 300 kV / Glacios 200 kV + K3）；X -ray 晶体学（8FLX）；DLS（Z-average 直径随温度/pH）；共聚焦内吞（HEP3B + 抗 His-Alexa-488）；Namdinator 式分子动力学柔性拟合把设计模型放入密度。
- **没有用的方法**：QM、自由能微扰/MM-PBSA 类端点自由能、结合亲和力测定（全文没有 Kd/SPR/BLI 数据）；MD 只出现在"把模型拟合进电镜密度"这一步。

### 工作流程表（12 步，全部为正文/Methods 明示顺序）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| 1 | 先前设计的环形同源三聚体家族 | 刚性融合不同长度螺旋重复蛋白臂，得到约 10 nm 直径带臂同源三聚体 | 实验四道：SEC 保留体积与设计模型一致、SEC 单分散、nMS 确认三聚态、SAXS 曲线与设计模型一致；nsEM 2D 类别平均/3D 重建看臂构型。**计算端原文未给阈值** | 39 个设计：37 个可溶、33 个 SEC 对、22 个单分散、27 个 nMS 确认三聚、19 个 SAXS 一致；1 个结晶结构（BGL17_A31） |
| 2 | 7 个带臂 host × 4 个无臂 guest | 界面移植前先做**兼容性预检**：把 guest 界面**对称**移植进 host，看还能不能形成正确寡聚体 | 对称移植版本在 SEC/nMS 上给出正确寡聚态才继续 | 28 种组合中实测 18 种；14/18 SEC 峰在正确寡聚尺寸；11/18 nMS 在正确质量处有强信号 |
| 3 | 通过兼容检验的 host（BGL17_A32 系） | 把不同 guest 界面拼接成 ABC 型；并给三条链不同臂长（A 减 1 个重复、C 加 1 个重复）以便在 EM 里认出链型 | SEC + SDS-PAGE + nMS 证明只形成 ABC 异源三聚体（nMS 图上"only the heterotrimeric ABC species is observed"）；2D nsEM/3D 重建要能看出臂长差 | 5 个候选中 3 个成 ABC 型；其中 2 个（hetBGL0-18-17_A32、hetBGL0-19-17_A32）有 EM 臂长证据 |
| 4 | BGL17_A32 带臂同源三聚体 | 用 RPXdock 采样三聚体 C3 轴沿各点群三重/四重/五重轴的旋转与平移，扫臂长 | 形状互补性 + RPX 打分取每个对称性的最高分模型；**原文未给 RPX 分数阈值**。实测最优臂重复数：四面体 1.5、八面体 2.5、二十面体 3.5 | 三类 T=1 笼的对接模型集 |
| 5 | T=1 对接模型 | ProteinMPNN 设计新生成的 arm–arm 笼界面；AF2 单序列预测该界面 | **AF2 预测的 arm–arm 界面相对设计模型 RMSD < 2.0 Å** 才送实验 | 19 个 T=1 笼：7 个 Tet（12 亚基，直径约 13 nm）、8 个 Oct（24 亚基，约 20 nm）、4 个 Ico（60 亚基，约 40 nm） |
| 6 | 19 个 T=1 笼设计 | E. coli 表达 + IMAC + SEC + nsEM | SEC 单峰在预期保留体积；nsEM 2D 类别平均与 3D 重建与设计模型吻合 | Tet 7/7 SEC 合格、4/7 nsEM 均一；Oct 7/8 SEC 合格、2/8 nsEM 均一；Ico 1/4 SEC 合格且 nsEM 接近（另有不完全成笼）→ 结构确认共 7 个 |
| 7 | 结构确认的 T=1 笼 + hetBGL0-18-17_A32 | **对称破缺落地**：用假对称异源三聚体原位替换同源三聚体；ProteinMPNN 重设计 ch_A/ch_B 的 trimer–trimer 界面；朝外的 ch_C 臂表面全改极性 | **AF2 预测 ch_A–ch_B 界面 RMSD < 2 Å，且不预测 ch_A–ch_A / ch_B–ch_B 同源界面形成**（正+负双条件） | 19 组冠（C3 冠 5 组、C4 冠 7 组、C5 冠 7 组）通过过滤并取得基因 |
| 8 | 19 组冠（每组 3 条链） | 三链分别表达，SDS-PAGE 灰度估量后按化学计量混合、共裂解共纯化 | SEC 在预期洗脱体积出峰 + SDS-PAGE 出现三条不同带（证明是异源三聚体而非同源混合物）+ nsEM 与设计模型匹配 | C3 冠 4/5、C4 冠 5/7、C5 冠 2/7 通过 SEC（本卡求和 = 11/19）；冠径 11 nm（C3）/20 nm（C4）/35 nm（C5） |
| 9 | 实验确认的冠 + BGL17_A32 同源三聚体 | 冠分别对齐 T-sym 三重轴 / O-sym 四重轴 / I-sym 五重轴，余下三重轴放同源三聚体；RPXdock 采样相互作用臂长度与沿共有轴的旋转平移 | 取每个对称性最高 RPX 分模型出序列（**未给分数阈值**） | 生成 Tet/Oct/Ico 三类 T=4 组装模型 |
| 10 | T=4 对接模型 | ProteinMPNN 出序列；AF2 预测界面 | 正向：设计的 heterotrimer–homotrimer 界面要形成；负向：self 界面不能形成（**未给数值阈值**）。八面体分支因 "Very few initial designs for the octahedral architecture did not form predicted self interfaces" → 追加 explicit negative design，其作用对象写为 "against the predicted self interfaces" | 14 组 T=4 笼设计（Tet T=4 5 组、Oct T=4 4 组、Ico T=4 5 组）通过 AF2 过滤并投测 |
| 11 | 14 组四组分设计 | 四链分别转化表达，按 1:1:1:1 混合共裂解，IMAC + SEC；Ico T=4-4 额外在室温静置 >24 h 再浓缩跑 SEC | 原文未给数值阈值；判据为 SEC 单峰 + nsEM 主物种是否为设计的 T=4 结构 | 14 组中"the major species in each case was the designed T = 4 structure"，同时存在较小的脱靶 T=1 样笼为次要物种；实测直径 33 nm（Tet，48 亚基）、43 nm（Oct，96 亚基）、75 nm（Ico，240 亚基） |
| 12 | 纯化的 T=4 笼 | nsEM（0.05–0.1 mg/ml）→ 冷冻电镜（0.5–1.0 mg/ml，defocus −0.7 至 −1.8 μm）→ 3D 重建与精修；模型柔性拟合入密度；DLS 测 dZ 随温度/pH；ch_ho 融合 ASGPR 结合体做细胞内吞 | 分辨率判据：Oct T=4-3 精修到 **6.87 Å**（可见二级结构）、Ico T=4-4 精修到 **13.15 Å**；Tet 上不了冷冻电镜（高于 0.3 mg/ml 聚集、低于 0.15 mg/ml 太稀）；稳定性判据：dZ 在 25–70 °C 不变、>75 °C 下降，pH 8.0–5.3（Ico）/8.0–6.4（Oct）不变 | 三个 T=4 架构的冷冻/负染电镜证据 + EMD-40260/40267/40268/40269 + 8FLX；60 个 ASGPR 迷你结合体展示在 Ico 笼外表面，HEP3B 共聚焦见点状胞内积累、仅二抗无信号 |

## 4. 关键数字台账（全部来自本地全文；出处列为正文/图注/Methods 中的原句位置，未加引号者为可直接检索的片段）

| 数值 | 含义 | 出处（可在全文检索到的位置/片段） |
|---|---|---|
| 39 / 37 / 33 / 22 / 27 / 19 | 带臂同源三聚体设计数 / 可溶 / SEC 保留体积合模型 / SEC 单分散 / nMS 确认三聚 / SAXS 合模型 | Main 第一段 Design of pseudosymmetric heterotrimers：Of the designs, 37 of 39 were soluble…22 of the designs…for 27 of 39 designs…for 19 |
| 约 10 nm | 带臂同源三聚体直径 | yielding homotrimers of approximately 10 nm in diameter |
| 28 / 18 / 14 / 11 | host×guest 组合数 / 实测组合 / SEC 正确寡聚尺寸 / nMS 强信号 | We experimentally characterized 18 of the 28 combinations…14 of 18…11 of 18 |
| 7 host + 4 guest | 7 个带臂骨架作 host、4 个无臂界面作 guest | seven with arms…as host scaffolds and four without arms |
| 5 / 3 / 2 | 拼接出的异源三聚体候选 / 形成 ABC 型 / 有 EM 臂长证据 | Three of five heterotrimers…For two of these |
| 1.5 / 2.5 / 3.5 | Tet / Oct / Ico 各自最优臂重复单元数 | different numbers of repeat units of arms (1.5, 2.5 and 3.5 repeat units |
| **RMSD < 2.0 Å** | T=1 笼 arm–arm 界面的 AF2 正向阈值 | the AF2 prediction of the arm–arm interface was less than 2.0 Å root-mean-square deviation |
| **RMSD < 2 Å + 同源界面不形成** | 冠（crown）这一步的 AF2 正负双判据 | We selected designs for which AF2 predicted the ch_A–ch_B interface with RMSD < 2 Å |
| 7 / 8 / 4 | 送实验的 T=1 笼数（Tet / Oct / Ico） | these comprise seven tetrahedral cages…8 octahedral cages…4 icosahedral cages |
| 12 / 24 / 60 亚基；约 13 / 20 / 40 nm | 三架构 T=1 笼亚基数与直径 | with 12 subunits and diameters of approximately 13 nm…24 subunits…60 subunits |
| 7/7 与 4/7；7/8 与 2/8；1/4 | T=1 笼 SEC 通过数与 nsEM 均一数 | All of the tetrahedral designs had peaks…Seven of the octahedral cages…One of the icosahedral cages |
| 19 组（5 C3 + 7 C4 + 7 C5） | 通过 AF2 正负双判据并取得基因的冠集合 | We obtained genes encoding 19 sets of crowns that passed these filters |
| 4/5、5/7、2/7（合计 11/19，本卡求和） | C3/C4/C5 冠在 SEC 上出预期洗脱峰的比例 | By SEC, four of five C3, five of seven C4 and two of seven C5 crowns had peaks |
| 11 / 20 / 35 nm | C3 / C4 / C5 冠直径 | The diameters of the crowns are 11 nm (C3), 20 nm (C4) and 35 nm (C5) |
| 14 组（5 Tet + 4 Oct + 5 Ico） | 通过 AF2 过滤并投测的 T=4 四组分设计 | We experimentally tested 14 sets of T = 4 cage designs |
| 48 / 96 / 240 亚基；33 / 43 / 75 nm；4 链 / 6 界面 | 三个 T=4 笼的实测规模 | T = 4 cages with 48 (tetrahedral), 96 (octahedral) and 240 (icosahedral) subunits, each with 4 distinct chains and 6 different protein–protein interfaces, and diameters of 33 nm, 43 nm and 75 nm, respectively |
| 11.5 nm 与 6.0 nm | Tet 笼中 homotrimer–heterotrimer 与 heterotrimer–heterotrimer 距离 | The homotrimer–heterotrimer distance (11.5 nm) is almost twice the heterotrimer–heterotrimer distance |
| 6.0 nm / 10 nm / 约 50 nm（体积约 6.55 × 10⁴ nm³） | Tet 内部通道宽 / Oct 中心腔 / Ico 中心空孔内径与体积 | the interior volume is a tetrahedral channel 6.0 nm in width…a 10-nm cavity in the centre…approximately 50 nm |
| −1 与 +1 个重复 | 给 A 链减臂、C 链加臂以在 EM 中分辨链型 | we varied the number of repeat units on the arms protruding from each chain |
| 6.87 Å | Oct T=4-3 冷冻电镜 3D 重建分辨率（可见二级结构） | resulted in a 3D cryo-EM map with 6.87 Å resolution with clear secondary structure features |
| 13.15 Å | Ico T=4-4 冷冻电镜 3D 重建分辨率 | yielded a 3D cryo-EM map with 13.15 Å resolution |
| 1,320 与 1,048 movies / 6,678 movies；0.44 Å 与 0.84 Å 像元；约 50 与约 61 e⁻ Å⁻² 总剂量；defocus −0.7 至 −1.8 μm | 冷冻电镜采集量与参数 | Movies ( n = 1,320 and 1,048 ) were collected…6,678 movies were collected…random defocus ranges spanning between −0.7 µm and −1.8 μm |
| 0.3 与 0.15 mg/ml | Tet T=4 上冷冻电镜失败的浓度窗口（高于 0.3 聚集、低于 0.15 太稀） | aggregated when they are concentrated higher than 0.3 mg ml −1 . They were stable below 0.15 mg ml −1 |
| 0.005 / 0.05–0.1 / 0.5–1.0 mg/ml | 负染用浓度（寡聚物 / 冠与笼）与制样浓度（冷冻） | diluted (0.005 mg ml −1 for oligomers and 0.05–0.1 mg ml −1 for crowns and cages) ; 3 μl of 0.5–1.0 mg ml −1 |
| 24 h（>24 h）室温熟化 | 仅 Ico T=4-4 需要的组装平衡步骤 | we kept the IMAC-eluted sample at room temperature for 24 h before concentrating and running SEC |
| 1:1:1 与 1:1:1:1 | 三组分冠与四组分笼的混合化学计量 | mixed with a correct stoichiometry for target assemblies (1:1:1 for heterotrimers and crowns; 1:1:1:1 for T = 4 cages) |
| 25–70 °C 不变、>75 °C 下降；Tm > 70 °C | DLS 测得的两个笼的热稳定性 | was unchanged from 25–70 °C and then decreased above 75 °C；melting temperatures higher than 70 °C |
| pH 8.0→5.3 不变、pH 4.7 上升；pH 8.0→6.4 不变、pH 5.9 及以下上升 | Ico / Oct 的 pH 耐受窗口（后者疑似聚集） | The Ico T = 4 -4 d Z of around 80 nm was unchanged from pH 8.0 to pH 5.3, but increased at pH 4.7, probably due to aggregation |
| 60 个 | 展示在 Ico T=4-4 外表面的 ASGPR 迷你结合体拷贝数 | Sixty ASGPR mini-binders were displayed on the outer surface of the Ico T = 4 -4 cage through genetic fusion |
| 420 亚基 | 展望中可由同一路线构造的 T=7 笼规模 | T = 7 cages with 420 subunits can be constructed by incorporating a second heterotrimer |
| 100 ng 质粒 / 10 µl 感受态 / 500 µl→50 ml / 100 µg ml⁻¹ 卡那 / 37 °C 225 rpm 18–24 h | 表达参数（TBM-5052 诱导 18–24 h） | Plasmids (100 ng) were transformed into a chemically competent E. coli expression strain |
| 4,000 g 10 min / 18,000 g ≥30 min / 30 ml 重悬 / 300 µl PMSF / 70% 超声 5 min / 1.5 ml Ni-NTA / 15 ml×2 洗 / 10 ml 洗脱 / 500 ml 培养分六根柱 | IMAC 纯化参数 | Cultures were harvested by centrifugation at 4,000 g for 10 min |
| 1 mg TEV : 100 mg 底物，24–72 h 室温 | 标签切除条件 | cleaved with TEVp at a ratio of 1 mg TEV per 100 mg substrate for 24–72 h |
| 300 V 18 min；2% 甲酸铀酰；120 kV Talos L120C；300 kV Krios / 200 kV Glacios（K3） | SDS-PAGE 跑胶、负染与电镜设备 | Gels were run at 300 V for 18 min；a 120 kV Talos L120C transmission electron microscope |
| 8FLX；EMD-40260 / 40267 / 40268 / 40269 | 晶体结构（BGL17_A31）与电镜密度库登录号 | Crystallographic data of BGL17_A31 have been deposited in the Protein Data Bank (ID 8FLX ) |

## 5. 结论——作者说了什么

1. 对称破缺路线做出**四组分、六界面**的 T=4 笼并被电镜确认：48（四面体）/96（八面体）/240（二十面体）亚基，直径 33 / 43 / 75 nm。
2. 与既有工作的复杂度差距被明确写出："Our T = 4 assemblies are a considerable advance in compositional and structural complexity over previous nanocage designs, which have one or two distinct components and up to three distinct interfaces; the designs described here have four distinct core structural components and six distinct interfaces"。
3. 路线自称可泛化："Our design approach can be applied to any set of protein oligomers that can be pseudosymmetrized and have dockable interfaces for the target point group symmetry."，且不限于 T=4——"T = 7 cages with 420 subunits can be constructed by incorporating a second heterotrimer"。
4. 冠的提取本身被当作可复用的方法学结论："Thus, symmetric substructures can be extracted from larger symmetric assemblies by substituting homotrimers with pseudosymmetric heterotrimers."
5. 应用侧（作者口径为第一步/概念验证）：笼子热稳定（Tm > 70 °C）、在内吞途径的 pH 区间有可逆性状的转变、且 ASGPR 融合笼被 HEP3B 内吞——"This result suggests that these large designed T = 4 cages can be internalized by cells for delivery or LYTAC applications"。
6. 作者对同组另一篇的让步式比较："describes a route to even larger, albeit less homogeneous, structures using two-component heterotrimers"（即本文的优势在均一性/界面可控，不在尺寸上限）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的真正方法学创新不是"造出更大的笼"，而是把一个组合/对称性问题编译成了若干个二值界面命题**：每加一个组分，界面数从 1→3→6 上升，但判据形态不变（该成的要成、不该成的不许成）。所以可扩展性的瓶颈在**判据能不能表达否定式**，而不在建模能力。这正好对上我们漏斗里"必须写明替代反应/错载不发生"的需求。
2. **命中率要按级联乘积读，不能按单级比值读**（本卡推算）：39 个基座设计 → 28 组合中 18 实测 → 5 个异源三聚体候选中 3 个成功 → 19 个 T=1 笼中 7 个结构确认 → 19 组冠中 11 组 SEC 合格（求和）→ 14 组 T=4 中主物种为设计结构、但只有 2 组拿到冷冻电镜、1 组看到二级结构。任何"7/19""11/19""14/14"单独引用都会误导；作者也全程没有给出总链成功率。
3. **判据饱和是自评环节最容易漏的一格**：正文自己承认八面体分支上负向闸口几乎不筛东西（"Very few initial designs for the octahedral architecture did not form predicted self interfaces"）。他们的处理很务实——把判别力问题转给生成端（负设计）而不是继续调阈值——但**没有报出这一步的通过率**，所以读者无法区分"判据有效"与"判据空转"。我们的门禁应该把"通过率"设成每个闸口的必填字段。
4. **结构判据是相容性判据，不是唯一性判据**：二十面体笼实测取向与设计相反，而把倒装模型放进去也能拟合密度（"The design model with inverted components fits well into the cryo-EM density following relaxation"）。这说明"AF2 说这个界面对"只排除了部分解，序列层面存在装配简并；与 binder 领域"pAE 低不等于按设计结合"是同一类失效，只是这里被更高分辨率的手段抓出来了。
5. **MD 在本文的位置是事后拟合，不是筛选**（relaxation via molecular dynamics 只出现在把设计模型放进冷冻电镜密度那一步）。因此本文不能作为"MD 可以筛装配/功能"的证据。
6. 他们把"能不能上冷冻电镜"变成判据的一部分（浓度窗口 0.15–0.3 mg/ml）：样本物理可行性会直接决定证据等级；我们的湿实验设计里也要预判"最低可检出量"，否则结论会停在定性层。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自陈的**
- 只有 3 个 T=4 架构被详细刻画，且证据等级不齐（Oct 6.87 Å、Ico 13.15 Å、Tet 仅 nsEM）；Tet 上不了冷冻电镜的原因写在 Methods（聚集/浓度窗口）。
- 二十面体笼的取向与设计不一致（倒装），本文未解决，只给出"倒装模型也能拟合"。
- 脱靶 T=1 样笼在八面体与二十面体体系里作为次要物种存在；正文没有给主/次物种比例。
- 功能层只到定性内吞（共聚焦），无亲和力、无细胞摄取定量、无体内数据。
- 作者把 24 h 熟化的机理写成推测（a relatively slow assembly kinetics seems reasonable），且称"we think that an even longer equilibration time could be helpful"。
- 通篇没有统一的"设计 N → 过滤 M → 送测 K → 命中 L"分母口径；计算库规模（对接前采样了多少模型）正文未给，全在补充信息里。

**我们读出的**
- 正向阈值 2.0 Å / 2 Å 只在两个阶段给了数值，最后的 T=4 阶段只写"based on the formation of the designed interface, and lack of formation of the self interfaces"，没有数值、没有通过率 → 漏斗里最贵的一级判据反而是最不可复核的一级。
- 负向判据（同源界面不许形成）从未被实验反向验证：EM 看的是最终装配，不能证明"某条同源界面确实不形成"，只能证明没有出现那种装配。
- nMS/SAXS/SEC 的通过口径互不一致（有的按 39 计、有的按 18 计、有的按 5 计），跨阶段不可加。

**与登记记录（CSV / sources/baker.md）不一致的三条**（本卡只登记，不改动底稿）
1. **MD 用途**：CSV 字段 `是否用MD(md_used)=否`、`sources/baker.md:547` 亦作 MD: 否；但本正文结果段确有 "Following relaxation via molecular dynamics" 一步。检索口径：在本底稿全文里 molecular dynamics 只出现 **2 次**，一次是上面这句结果叙述，一次是参考文献 24 的题名（Namdinator — automatic molecular dynamics flexible fitting of structural models into cryo-EM and crystallography experimental maps）。准确表述应为**是，仅事后把模型柔性拟合进密度图，不参与任何筛选判据**；若 CSV 口径特指"MD 作为筛选器"，则该字段应写成"否（作为筛选器）/ 是（事后拟合）"两栏，而不是单值否。
2. **cryo-EM 偏差数字归属**：`sources/baker.md:648` 的时间线行把 `cryo-EM 与设计偏差 2%` 与 [B25]/[B41] 并列写出。检索口径：在本底稿全文里 `2%` 只命中 **1 处**，且是负染染色剂 2% uranyl formate，与结构偏差无关；本文给出的结构尺度只有 6.87 Å / 13.15 Å 两个分辨率，以及 slight twist / inverted 的**定性**描述。因此该 2% 不可能来自 B41 正文（可能来自 [B25] 或本文未取回的补充信息），需要重新核验来源。
3. **漏斗分母口径**：CSV `候选数递减(pipeline_counts)= 19 组 crown 通过过滤 → 14 组 T=4 笼设计投测` 与原文一致但只含末端两级，容易被读成"整条漏斗只有两级"；上游 39/28→18/5→3/19 个 T=1 笼→7 个结构确认这一段在 CSV 里缺失。CSV `实验命中率(hit_rate)=未记录` 与原文相符（原文未报统一命中率），本卡不改动。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **把"设计意图"编译成正/负双语界的界面判据**（本文：AF2 要预测 ch_A–ch_B 成、且不预测 ch_A–ch_A / ch_B–ch_B 成）。用法：对我们每一个候选，把"要发生的化学事件"与"必须不发生的化学事件"写成成对命题（如：氨酰化供体正确 vs 错载/非特定位点酰化），并要求打分器对**否命题**也给出可判读数；不能只给"位点看起来对"的单向支持分。
2. **explicit negative design 放在生成端而不是筛选端**。本文在八面体分支发现负向筛子不筛东西后，改为在序列生成时就把 self 界面作为负例。用法：在候选生成/重采样阶段就把已知失败模式（例如把 UTP 结合位点暴露成非特异吸附面）作为负例注入，而不是事后加一道昂贵判据。
3. **层级化拆步 + 每级独立实验确认**，把组合爆炸换成 N 个可独立判伪的小问题。用法：把"酶 + 正交 tRNA + 底物 + 供体"的合取要求拆成可单独验证的模块级判据，每级设一个便宜的实验确认点，通过才进下一级；同时把每级的通过率写进台账。
4. **每个闸口必须同时报"通过率"**（本文缺这一格，成为最可疑处）。用法：在我们的漏斗标准里把"该闸口过滤掉多少 / 留下多少"设成必填；通过率接近 100% 或接近 0% 的闸口要标注"无判别力/饱和"。
5. **不要用"major species"作为通过口径**。用法：预注册一个量化阈值（例如 LC-MS 峰面积主/次产物比、或目标产物占全部检出产物的比例下限），并在下单前定死；本文正是因为只写"主要物种"而无法复核。
6. **样本物理可行性属于判据链的一部分**（浓度窗口决定能否上高分辨）。用法：为每个候选写明"最低可测得量/最低检出浓度"，把"测不到"与"不合格"分开记状态。

**不可迁移（为什么不能照搬）**

1. **本文没有任何催化、没有任何产物化学鉴定**。它的"确认率"是**结构自洽/装配正确**的确认率，与 UAA 合成酶需要的"化学事件发生且副反应不发生"不是同一件事；把 7/19、11/19、14/14 之类数字当成酶活概率或校准依据是错误引用。
2. **AF2 界面 RMSD < 2 Å / "不预测形成"是静态几何自洽判据**，不含能量学与动力学，更不含过渡态化学；对催化三步事件（供体选择、键形成、竞争副反应）没有对应量。任何把该阈值搬到酶位点评估的做法都需要另找证据。
3. **共聚焦内吞（定性、二抗对照）不构成功能验证模板**。我们的功能终点是化学身份，二者证据等级不可互估；不能由此推"某功能读出容易/难做到"。
4. **工艺经验（24 h 熟化、Het 缓冲液、1:1:1:1 混合、SDS-PAGE 灰度定化学计量）是这一个四组分体系的一条性优化**，没有梯度实验支撑，不能作为我们的默认操作参数，更不能当判据。
5. **通量口径不可比**：本文每一步的湿实验量是个位数到十几组，属"少量精致构建体"路线；这与展示库式上万通量、或我们单轮最多几个构建体的情形都不同——既不能拿他们的做法论证"我们也能上万条"，也不能拿他们的确认率当我们的期望值。
6. **MD 只做过柔性拟合**：本文不提供"MD 可评估催化预组织/反应坐标"的任何正面证据，反向也不构成否证（他们根本没做）。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/fourcomp_cages2025.txt

- **本卡唯一逐字比对源**：`data/interim/baker_lit/ft/fourcomp_cages2025.txt`（Europe PMC `fullTextXML` 去标签纯文本，85 行 / 56,632 B；文件头身份块为 PMC11821509 · PMID 39695226 · DOI 10.1038/s41586-024-07814-1 · Nature 638:546-552，与 CSV `B41` 行的三个 id 完全一致，故不存在挂错行）。B41 在 `data/literature_cards/sources_map.json` 里只登记了这一份全文 + `sources/baker.md`（记录，非全文）；`data/literature_cards/fulltext/` 下**没有** B41 文件，因此本卡不声明该路径。
- 对照记录行号：`sources/baker.md:539-550`（原卡）；`sources/baker.md:648`（2025 年时间线行，含与本文不符的 cryo-EM 偏差 2% 表述，见第 7 节）；`data/literature_cards/batches.tsv` 第 41 行（`state=FULLTEXT`）。
- CSV 字段映射：本卡第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/成本统计引用`；第 7 节 ↔ `是否用MD`（现值与原文不符，本卡只登记不改）；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检命令**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B41 --no-report`（`--no-report` 以避免覆盖并行代理的 `selfcheck.txt` / `rollout_status.tsv`）。核验器把卡内所有被直双引号包住、纯英文、≥20 字符且 ≥12 个字母的片段，按 NFC + 引号/破折号统一 + 空白折叠的同一套归一化，在上述底稿里逐字查找；任一条不命中即 FAIL。逐字命中结果以门禁实际输出为准（本卡未手工统计条数）。
- 抽取造成的书写差异（引句一律按归一化后的形态复制）：正文里的 `RMSD < 2 Å` 在原始文本中写作 HTML 实体 `&lt;`；`–`（en dash）、`−`（U+2212）与 NBSP 由 `litcards_text.norm()` 统一为 `-` 与空格，本卡引句按归一化结果照抄，未做任何改写、拼接或省略号截断。
- 未取到因而**没有**写进本卡的内容：Supplementary information 1–3（RPXdock/ProteinMPNN/AF2 的具体参数与阈值表、投测前的计算库规模）、Supplementary Figs 19/25/33/34/37/42/45/47–50、Supplementary Tables 1–13、Extended Data 序列表。凡这些位置本卡一律写"原文未给阈值"或"正文未给出，仅有正文描述"。

<!--CSV回填
work_type=论文（Nature 正刊，结构/装配设计型工作，无酶活与产物化学）
target=T=4 四组分蛋白纳米笼：四面体 48 亚基/33 nm、八面体 96 亚基/43 nm、二十面体 240 亚基/75 nm；每条笼含 4 种链、6 种不同蛋白–蛋白界面；另含 T=1 笼、C3/C4/C5 冠与 ASGPR 融合内吞笼
backbone_generation=先前设计的环形同源三聚体 + 刚性融合螺旋重复蛋白臂（1.5/2.5/3.5 个重复对应 Tet/Oct/Ico）→ 界面移植（host 7 个带臂 × guest 4 个无臂，先对称移植验兼容）生成 ABC 假对称异源三聚体 → RPXdock 沿点群对称轴采样旋转平移 → ProteinMPNN 出序列；T=4 级在八面体分支追加针对预测 self 界面的 explicit negative design
computational_filters=AF2 单序列界面预测的双向判据：正向要求目标异源界面按设计形成（T=1 阶段 arm–arm 界面 RMSD<2.0 Å；冠阶段 ch_A–ch_B 界面 RMSD<2 Å），负向要求同源界面（ch_A–ch_A / ch_B–ch_B，以及 T=4 阶段的 self 界面）不被预测形成；朝外 ch_C 臂表面重设计为全极性以物理阻断再结合；T=4 阶段只有描述性判据无数值阈值；无 MD/QM 参与筛选
thresholds=T=1 笼：AF2 预测 arm–arm 界面相对设计模型 RMSD<2.0 Å；冠：AF2 预测 ch_A–ch_B 界面 RMSD<2 Å 且不预测 ch_A–ch_A / ch_B–ch_B 同源界面形成；T=4：设计界面形成且 self 界面不形成（原文未给数值阈值）；RPXdock 取每对称最高分模型（未给分数阈值）；冷冻电镜分辨率读数 6.87 Å（Oct T=4-3）与 13.15 Å（Ico T=4-4）；冷冻制样浓度窗口 0.15–0.3 mg/ml（Tet 因聚集不可测）
md_used=是（仅事后：把设计模型用分子动力学柔性拟合进冷冻电镜密度图，正文见 relaxation via molecular dynamics，引文 24 为 Namdinator；不参与任何筛选/入选判据。CSV 该字段现记为否，与本全文不符，详见卡内第 7 节不一致条 1）
qm_used=否（全文无 QM/DFT/自由能计算，也无任何反应坐标）
experimental_methods=E. coli 表达（Protocol 1 分开发按比例混合 / Protocol 2 共转化）→ IMAC（异源复合物用 Het 变体缓冲液）→ SEC（Superdex 200 或 Superdex 6）→ TEV 切标签再 SEC → SDS-PAGE（含灰度定化学计量）→ LC-MS 完整分子量 → native MS 寡聚态 → SAXS → 负染电镜（Talos 120 kV + CryoSPARC 2D 类别平均与 3D 重建）→ 冷冻电镜（Krios 300 kV / Glacios 200 kV，K3）→ X 射线晶体学（8FLX）→ DLS 温度/pH 滴定 → HEP3B 共聚焦内吞（抗 His-Alexa-488）
pipeline_counts=带臂同源三聚体 39（37 可溶 / 33 SEC 对 / 22 单分散 / 27 nMS 三聚 / 19 SAXS 对）→ host×guest 28 组合中实测 18（14 SEC 对、11 nMS 强）→ 异源三聚体候选 5 中 3 成 ABC 型 → T=1 笼 19 通过 AF2 阈值（7 Tet / 8 Oct / 4 Ico；SEC 合格 7+7+1，nsEM 均一 4+2+1）→ 冠 19 组通过 AF2 正负双判据（5 C3 / 7 C4 / 7 C5；SEC 合格 4+5+2）→ T=4 笼 14 组通过 AF2 过滤投测（5 Tet / 4 Oct / 5 Ico），3 个架构被详细电镜刻画、2 个有冷冻电镜图
hit_rate=原文未给统一命中率（无分母一致的"设计→送测→命中"口径）。分级读数：T=1 笼结构确认 7/19；冠 SEC 合格 11/19（本卡按原文分组计数求和）；T=4 十四组均以设计的 T=4 结构为主要物种（同时出现脱靶 T=1 样次要物种，未量化比例）。故 CSV 原字段"未记录"在事实层面成立，本行仅补充分级观测
best_metric=未记录（本文不测亲和力与催化活性；功能层只有定性内吞。可引用的最佳结构指标：Oct T=4-3 冷冻电镜 6.87 Å 且二级结构可辨；Ico T=4-4 直径 75 nm、中心空孔内径约 50 nm、体积约 6.55×10⁴ nm³；Tm>70 °C；pH 稳定窗口 Ico 8.0–5.3、Oct 8.0–6.4；外表面展示 60 个 ASGPR 迷你结合体）
cost_or_stat_note=正文未报算力/试剂成本。可核对的资源量：冷冻电镜采集 1,320 + 1,048 张 movies（Oct，0.44 Å 像元，约 50 e⁻ Å⁻²）与 6,678 张 movies（Ico，0.84 Å，约 61 e⁻ Å⁻²）；defocus −0.7 至 −1.8 μm；表达 50 ml TBM-5052/构建（结晶用 500 ml）；IMAC 1.5 ml Ni-NTA；TEV 1 mg:100 mg 底物、24–72 h；Ico T=4-4 需 IMAC 洗脱后室温静置 >24 h 才得均一样品；Tet T=4 上不了冷冻电镜（>0.3 mg/ml 聚集，<0.15 mg/ml 太稀）
role_in_timeline=与 [B25]（Dowling 等同期论文）一起把多组分不对称组装变成可设计对象：B41 用假对称化把"对称破缺"翻译成界面级正/负约束，做出四链六界面的 T=4 笼并把"该成的界面要成 + 不该成的界面不许成"确立为漏斗里的判据形态；相对上一代一/二组分完美点群笼（King 2012/Lai 2014/Hsia 2016 一脉），其贡献是**判据表达方式**（负向筛 + 显式负设计 + 层级化分步实验确认），而不是新的生成模型。同时暴露两类新缺陷：负向闸口可饱和（八面体分支几乎不筛东西）、结构判据只给相容性不给唯一性（二十面体实测取向相对设计倒装）
source_pointer=data/interim/baker_lit/ft/fourcomp_cages2025.txt（唯一逐字底稿，Europe PMC PMC11821509 fullTextXML）；sources/baker.md:539-550 与 :648；data/literature_cards/batches.tsv 第 41 行；DOI 10.1038/s41586-024-07814-1；PDB 8FLX；EMD-40260/40267/40268/40269；代码 https://github.com/willsheffler/rpxdock 与 https://github.com/dauparas/ProteinMPNN
CSV回填-->
