# [B40] De novo design of proteins housing excitonically coupled chlorophyll special pairs

（骨架已落盘，逐节填充中）

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B40**（组：Baker组；`batches.tsv` 第 40 行，state=FULLTEXT） |
| 论文 | Ennist N M, Wang S, Kennedy M A, Curti M, Sutherland G A, … Baker D. De novo design of proteins housing excitonically coupled chlorophyll special pairs |
| 单位（按全文顺序） | UW Institute for Protein Design / Dept of Biochemistry / Dept of Cell Biology & Skirball / Dept of Chemistry / Dept of Microbiology（Seattle）、Fred Hutchinson Cancer Center、University of Sheffield（School of Biosciences）、NYU School of Medicine、UC Santa Barbara（Dept of Chemistry & Biochemistry）、Lawrence Berkeley National Lab（ALS）、HHMI-UW。**全文里没有 Arizona State（ASU）这条单位**（见第 9 节与底稿的差异） |
| 出处 | Nature Chemical Biology, 2024, 20:906-915 · DOI 10.1038/s41589-024-01626-0 · PMID 38831036 · PMCID PMC11213709 · CC BY 4.0 |
| 取回通路（按 inventory.json） | Europe PMC `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11213709/fullTextXML`，标签剥离后落盘 |
| 本地全文（本卡唯一比对底稿） | `data/interim/baker_lit/ft/chlorophyll2024.txt`（118,884 B，172 行；正文在第 4–26 行，Methods 在 27–55 行） |
| 对照登记底稿 | `sources/baker.md:525-537`（原卡）——本卡只对照、不修改底稿 |
| 证据级别 | **全文级**（本卡全部引句在该本地全文里逐字命中，见第 9 节自检） |
| 未取到的部分 | Supplementary Figs 1–22、Supplementary Tables 1–7、Source Data Fig. 2/4/5、Supplementary Videos 1–2（纳米笼 breathing 电影）、PDB 条目内的逐残基数据。凡涉及这些的本卡明写"正文未给出" |
| 结构登记 | PDB 7UNJ（SP1−ZnPPaM）、7UNI（SP2−ZnPPaM）、8EVM（SP3x apo）、SP2 apo 未给 PDB 号；EMDB EMD-40208 map 1 / EMD-40209 map 2；光谱计算原始数据存 ioChem-BD 10.19061/iochem-bd-6-268 |

## 1. 这篇到底解决什么（一句话/大白话）

一句话：**让计算机从零设计出的蛋白，把两分子叶绿素像天然"特殊对"那样紧挨着摆好，好让两者的激发态互相"搭"起来（激子耦合）——这在以前只有天然光合蛋白做得到，人造体系从来没拿到过按设计几何摆放的叶绿素二聚体结构。**

大白话展开：天然光合反应中心的"特殊对"（special pair）是两靠得极近的叶绿素分子，它们一旦耦合，吸收和荧光峰会分裂、红移，并成为一个高效能量陷阱/电子给体。作者要做的是把这个性质搬到人工蛋白里。难点不在于"设计一个能结合色素的口袋"（前人做过单体结合蛋白），而在于：

1. 要摆对的是**两个**色素的相对位姿，第二个色素的自由度不受蛋白骨架控制；
2. 想要的结果（激子耦合，单位 cm⁻¹）是**激发态量子性质**，Rosetta 的静态能量函数根本不算它；
3. 天然复合物色素太多、光谱拥挤，没法单看这一对。

他们的做法可以概括成一句可迁移的方法学：**把"物理性质"拆成（a）设计期能算的必要条件（对称性 + 配位几何 + 色素对相对位姿）和（b）造出来之后只能靠光谱直接读的性质本身**，前者用来下单、后者用来判定成败——两者绝不能互相替代。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **哈希 motifs 的原料不够：PDB 里没有现成的 His−叶绿素二聚体例子。**
   现象/证据："the number of example structures of the His-Chl dimer motif found in PDB is not acceptable for effectively populating a motif hash table"；而这套方法本身要求可扩展到海量支架——"Identifying residue positions capable of accommodating the Chl special pair, and that are scalable to millions of potential scaffolds"。
   **他们做了什么**：不去找更多天然结构，而是**用 NeRF 算法自己造 motif**——改变色素相对位置、His 配位二面角、His 侧链 rotamer，生成构象后沿 C2 轴复制成对称复合物，评测色素环及取代基是否 clash 并过滤，再对咪唑环 ε 氮与 δ 氮两种配位方式各重复一遍；最后把 His 的 N-Cα-C 三元原子的 6D 变换哈希进 multivalue 表（`stapler`、`getpy`、`nerf` 三个开源包）。
   残留代价：motif 是"化学上合理"而非"天然验证过"的构象库；配位几何是否真能给出可用口袋，只能在湿实验端才知道。
2. **第二个小分子不受控：结合界面里有一半不是蛋白。**
   现象/证据："Binding a small molecule as a dimer is a computational challenge because the binding interface involves not only the protein but also the second small molecule, which has an independent set of rotational and translational degrees of freedom"。
   **他们做了什么**：用**对称性把这个自由度消掉**——设计完美 C2 同源二聚体，让蛋白与色素对的 C2 轴重合（"symmetry axes of the protein and chromophore are coincident"），并给出物理理由："ensures that the two bound Chl molecules will have near-degenerate site energies, improving the resonance between pigment transitions necessary to create delocalized states"。支架选的是超稳定 C2 重复蛋白二聚体，其疏水核心与色素口袋彼此独立，因此改口袋几乎不动骨架。
   残留代价：对称把两色素强制等价，也砍掉了天然特殊对里普遍存在的不对称性；Discussion 自己承认细菌天然对的耦合更强是因为 bacteriochlorin 的 Qy 跃迁偶极矩更大，这不是对称性能补偿的。
3. **静态设计判据和功能性质不同向——最漂亮的结构反而耦合最弱。**
   现象/证据：SP1 的色素二聚体对天然紫色细菌特殊对达到 "Alignment of the tetrapyrrole rings of the SP1-ZnPPaM dimer with nine native BChl a special pairs from different species of purple bacteria gave r.m.s.d. values of 0.23-0.28"，蛋白骨架也与设计一致；但它算出来的耦合只有 "Calculations on the SP1-ZnPPaM dimer crystal structure (Fig. 3e ) yielded a lower excitonic coupling of 87 cm"，作者明说 "SP1 exhibits weaker excitonic coupling than SP2 and the BChl special pair of purple photosynthetic bacteria, despite its close structural similarity to the latter"。反之 SP2（几何刻意非天然）才有强耦合。
   **他们做了什么**：把成败判据从"几何像不像"换成"性质本身可观测没有"——用 UV/vis/NIR 圆二色的 bisignate Cotton 效应作为廉价探针（"CD spectra can serve as a convenient probe of excitonic interactions between Chl molecules"，机理是 "excitonic interactions can produce delocalized transitions with chiral character, yielding CD signals that are stronger and conservative"），再加 Qy 吸收分裂、低温双发射带、能量传递寿命下降；量子化学只用于**解释与对账**，不用于下单前打分。
   残留代价：设计期完全没有办法预判耦合强弱，只能把所有通过静态判据的设计全部送测——命中率的分母因此是"全部下单数"，不是"计算预测通过数"。
4. **SP2 色素按设计摆错了 3.5 Å，但目标算达成。**
   现象/证据："Despite the accuracy of the protein backbone design, the crystal structure shows that the ZnPPaM molecules are rotated and translated relative to the design model"；解释是 holo 态结合腔 "the SP2 binding cavity widens by ~1.6" 从而腾出体积。
   **他们做了什么**：把 SP2 的成功标准改述为"造出一个非天然的二聚体几何"这一层级目标——"the crystal structure nevertheless satisfies the objective of creating a non-native dimer geometry"；同时把这个**实际**（非设计）几何直接拿去做 QM 计算和光谱模拟（"Using the SP2-ZnPPaM dimer crystal structure (Fig. 3h ), we calculated an excitonic coupling energy of 241 cm"）。
   残留代价：设计模型对最终性质的预测力无法评估——性质是用真实结构算的，等于把验证基准挪到了实验之后。
5. **668/690 nm 两条带可能不是激子耦合，而是两种色素聚集体混在一起。**
   现象/证据：作者自己立了这个待排除项："To investigate the origin of the SP2-ZnPPaM bands at 668 and 690 nm and rule out the possibility that they represent two populations of distinct ZnPPaM oligomers"。
   **他们做了什么**：加**配比对照片**——单体样只加 0.3 当量 ZnPPaM、二聚样加 2.0 当量，都做 75 K 蔗糖/海藻糖膜；结果 "The monomer sample lacked a red-shifted shoulder (Fig. 4b ), but in the SP2-ZnPPaM dimer sample, two emission bands were observed at 673 and 692 nm"；再用 PigmentHunter 模拟谱去复现"低能态弱振子强度 + 吸收/荧光大位移"这两个只有激子模型才给的指纹。
   残留代价：模拟谱的输入耦合值本身经过经验缩放（见第 7 节），所以"模拟与实验吻合"不是完全独立的确认。
6. **SP3 的 holo 结构解不出来。**
   现象/证据："We did not succeed in solving the holo-state structure of SP3"。
   **他们做了什么**：换近缘设计做 apo 结构（SP3x 与 SP3 序列同一性 94%，3.05 Å），并改用**CD 符号计算比对**去支持 SP3 按设计组装成 P700-样二聚体——"In the SP3 dimer, the calculated spectrum based on the design model agreed with the experimentally measured signs of the CD Cotton effects, suggesting that the P 700 -like ZnPPaM dimer in SP3 assembles as designed"。
   残留代价：SP3 的色素几何从未被直接观测；"as designed"是间接推断。
7. **纳米笼冷冻电镜只有 6.5 Å，且颗粒被冰压坏。**
   现象/证据："During data collection, we noted a high proportion of damaged (compressed or fragmented) nanocage particles"；"Continuous conformational heterogeneity likely limited the resolution of the full nanocage map"。
   **他们做了什么**：三招——按冰厚与 CTF 拟合剔除（"Curation of micrographs to exclude those with the thinnest ice and with CTF fit resolution lower than ~6"）、针对最常被漏的稀有视图改用单模板补拾再拿去重训 Topaz（"204,039 versus 19,355 in the initial Topaz training set"）、T 对称扩展 + partial signal subtraction 做局部聚焦精修，并把模型按丙氨酸残基加约束精修（"Due to the intermediate map resolution, all residues were modeled as alanine"）。
   残留代价：作者承认 "Although the resolution is not sufficient to confidently determine the orientations of the Chl molecules, the cryo-EM density map is consistent with the Chl dimer geometry in the SP2 crystal structure"——笼内 24 个色素的真实几何仍是未观测项，本文未解决。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **支架与序列**：预先存在的超稳定 C2 对称重复蛋白（DHR）同源二聚体库（文献 34–36 的产物，正文说这类库已有 "Several thousand C 2 -symmetric homodimers that sample a wide range of superhelical curvature, rise and radius parameters have been generated" 的量级）；口袋用 **symmetric Rosetta FastDesign** 重设计。
- **把色素几何变成可搜索约束**：**motif-hash（6D 变换哈希）** 方法 + 自写的 `NeRF` 构象生成 + `getpy` 多值哈希表 + `stapler` Python 包（三个 GitHub 仓库，Methods 明写）。
- **激发态/光谱（只在造出来之后用）**：Gaussian 16 的 **EET 模块**做电子耦合；**PCM**（n-octanol 近似蛋白介电）；**Excitonic Analysis Tool** 算 CD；**PigmentHunter** 在线应用做吸收/荧光线形模拟；力场参数用 **MCPB.py + restrained ESP（RESP 类）+ Seminario 力常数**。
- **MD**：**Amber18 / ff14SB / TIP3P**，配方是 QM 优化过的色素参数。**注意：正文（Results/Discussion）没有报告任何由 MD 得到的判据量或数字**，MD 只出现在 Methods 与作者贡献里（"M.C. conducted molecular dynamics simulations and calculations of CD spectra"），因此本文的 MD 属于**事后机理/参数化**用途，不是漏斗筛子。
- **结构验证**：X-ray（SP1/SP2/SP3x）、SAXS、负染 EM、cryo-EM（6.5 Å）。
- **功能验证**：UV/vis/NIR CD（Qy 区 bisignate Cotton 效应）、吸收/荧光滴定、75 K 蔗糖/海藻糖膜低温光谱、FLIM + 纳米压印接触打印的能量传递、单光子计数寿命。
- **没有用的方法**：AF2/RF2 置信度打分、Rosetta ddG 之外的界面预测闸口、自由能微扰、定向进化（Discussion 把它列为下一步）。

### A. 设计期：把"激子耦合"拆成可算的必要条件

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | 目标色素二聚体几何（天然 P865 型 + 若干非天然型）+ His−Chl 单体 | 用 NeRF 把内坐标转全局坐标生成构象（改色素相对位姿、His 配位二面角、His 侧链 rotamer），沿 C2 轴复制成对称复合物；对 ε 氮与 δ 氮配位各重复一遍 | 相对取向改变时评测并过滤环与取代基的 clash（**原文未给阈值**） | de novo motif 构象集，用于填补 PDB 样本不足 |
| W2 | motif 构象集 + 数千个 C2 重复蛋白支架 | 把配位 His 的 N-Cα-C 三原子 **6D 变换哈希**成多值表；对每个支架的对称残基对算同样的 6D 变换查表，命中就重建 His−Chl 复合物放进蛋白里评估 | "If the Chl molecules did not clash with the backbone atoms of the protein, the placement was accepted and passed into the protein design process" | 候选"支架 + 口袋残基对 + 色素位姿"三元组（正文未给具体数量） |
| W3 | W2 命中的复合物 | symmetric Rosetta FastDesign 重设计口袋，优化疏水堆积与氢键 | **四件静态判据**："Designs were filtered on the basis of the Rosetta full-atom energy, the solvent-accessible surface area of the Chl dimer, His rotamers and His N"（末词为 ε−metal ligation geometry）；**原文未给任一数值阈值** | "We selected 43 designs based on 13 unique scaffolds for experimental characterization"；单体 20.6-28.4 kDa（179-261 aa）；另有 5 个按晶体结构反馈的再设计变体 ⇒ 共 48 |

### B. 湿实验漏斗：送测与命中分母

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W4 | 48 个设计基因（pET29b，His6-TEV） | Lemo21(DE3) 自诱导表达 + Ni-NTA + TEV 切标签 + SEC（Superdex 200） | ①SDS-PAGE 可溶带 ②SEC 保留体积等于二聚体预期 | "SDS-PAGE gels showed that all 48 designs were present in the soluble fractions of the lysates"；"All SEC traces exhibited protein absorption at the elution volume expected for homodimer formation"（**48/48、48/48**） |
| W5 | apo 蛋白 | SAXS（ALS SIBYLS，30 μl/96 孔板）与 FoXS 预测曲线对比 | 曲线一致（正文未给阈值） | "Of the 20 designs investigated by small-angle X-ray scattering (SAXS) in the apo state, 15 had SAXS profiles that suggested a three-dimensional (3D) shape consistent with the design model" ⇒ **15/20**；Rg 预测偏低归因于高电荷蛋白的水化层 |
| W6 | 高产 3 个设计 | far-UV CD + 222 nm 热熔（2-98 °C） | 208/222 nm 双谷 = 高 α-螺旋；holo 与 apo 都要耐熔 | 三个设计表达量 "≥140 mg l" 级（单位 l⁻¹），apo/holo 均高度耐熔 |
| W7 | 蛋白 + ZnPPaM/ZnPPa | 吸收/荧光/CD 滴定（0.3、1.0、2.0 当量等） | **性质探针**："CD spectra can serve as a convenient probe of excitonic interactions between Chl molecules"，机理为 "excitonic interactions can produce delocalized transitions with chiral character, yielding CD signals that are stronger and conservative" | 双位点 Kd：SP2−ZnPPaM 300 nM/2.5 μM（CD 拟合）、SP3 800 nM/1.0 μM；吸收拟合 SP1 290/430 nM、SP2 110 nM/2.0 μM、SP3 350/940 nM；荧光 1:1 拟合 SP1 660、SP2 480、SP3 120 nM |
| W8 | W5–W7 表现最好的候选 | X-ray 晶体学 | 主链一致性阈值：**"both had protein backbone conformations that matched the corresponding design models to within 1.7" Å Cα 级 r.m.s.d.** | SP1−ZnPPaM **2.0 Å**（holo）、SP2 **2.4 Å**（apo）/**2.5 Å**（holo）、SP3x **3.05 Å**（apo）；SP1 色素环对九个天然特殊对 0.23–0.28 Å、对 SP2 自身两拷贝 0.22 Å |

### C. 性质判定层：静态判据换不到的一切都要在这里买

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W9 | SP2x−ZnPPaM，单体样 0.3 当量 / 二聚样 2.0 当量 | 75 K 蔗糖/海藻糖膜低温吸收 + 荧光，对照"是否两种色素聚集体混样"这一竞争假说 | 单体样不得有红移肩峰；二聚样应有两条发射带 | "The monomer sample lacked a red-shifted shoulder (Fig. 4b ), but in the SP2-ZnPPaM dimer sample, two emission bands were observed at 673 and 692 nm"；室温吸收：单体 ε669 = 49,900 M⁻¹cm⁻¹ ⇒ 二聚 ε668 = 38,200、ε690 = 17,700（单体只有 9,400） |
| W10 | 晶体结构（真实几何）与设计模型 | Gaussian EET 算电子耦合；PigmentHunter 对角化 Frenkel 激子哈密顿量模拟谱 | "Electronic couplings were calculated using the EET (electronic energy transfer) module from Gaussian"；"Environmental effects were considered through the polarizable continuum model"（n-octanol）；"The EET analysis considered six singlet excited states per chromophore"；模拟谱线形 FWHM 500 cm⁻¹、"Simulations in Fig. 4 are ensemble averaged over 10 6 realizations of pigment site energies chosen randomly from a Gaussian distribution with full-width at half-maximum of 500 cm" 的取值、位能单体 14,925 / 二聚体 14,750 cm⁻¹ | SP2 耦合 **241 cm⁻¹**（晶体结构算），实验 Qy 分裂 **477 cm⁻¹ ⇒ 耦合 239 cm⁻¹**；SP1 耦合 **87 cm⁻¹**，低温谱只有轻微展宽 | 
| W11 | 设计模型/晶体几何 | Excitonic Analysis Tool 算 CD 旋转强度 | "Spectral line shapes were simulated as Gaussians, with a full-width at half-maximum of 350 cm" 用于 Qy/Qx、Soret 区 1,150 cm⁻¹；"The spectra were shifted by -0.25 eV to reproduce the experimental position of the Q" 带 | 判据形式=**符号一致**：SP1/SP2 用晶体几何、SP3 用设计模型，Cotton 效应符号与实验相符 |
| W12 | 设计模型或晶体结构 | Amber18 MD：QM 优化色素 + MCPB.py 参数、H++ 定质子化、九步最小化+短 MD、NPT 300 K 生产 | "the protocol consists of nine sequential energy minimizations and short molecular dynamics runs, which sum to 4,000 steps of minimization and 40,000 molecular dynamics steps (totaling 30 ps), followed by a final molecular dynamics equilibration (500,000 steps, 1,000 ps)"；"Then, after discarding the first 200 ns, production runs were done in the isothermal-isobaric (NPT) ensemble at 300.0 K"；PME 截止 1.0 nm、Langevin 2 ps⁻¹、SHAKE | **正文未给出 MD 的任何输出量或筛选结论**（未报告轨迹长度、涨落、耦合分布）⇒ 本卡按"事后参数化/CD 谱计算的前置"记录 |
| W13 | CpcA−PEB（供体）与 SP2−ZnPPa（受体） | 纳米压印接触打印 2D 十字阵列（~5 μm 线宽）+ 宽场 620/680 nm 成像 + FLIM 单光子计数 | 交叉点应"供体降、受体升"；寿命下降量化效率："Regions with both CpcA-PEB and SP2-ZnPPa show reduced fluorescence intensity" 且寿命由 τav 2,058 ps 降到 839 ps | 能量传递效率 **59%**，"similar to the efficiencies recorded for natural fluorescent proteins"；SP2−ZnPPa（非 ZnPPaM）无 Qy 分裂 ⇒ "the peripheral substituents of chlorin have a role in excitonic coupling" |
| W14 | SP2 二聚体 + C3 三聚体支架库 | RPXDock 形状互补对接成 O32 八面体笼，界面做 symmetric RosettaDesign（侧链 layer design，骨架当刚性） | "The ten docking configurations with the best score for each scaffold were subsequently sequence designed by symmetric RosettaDesign calculations"；五道静态闸口："all cage designs were filtered on the basis of shape complementarity (>0.6), interface surface area (solvent-accessible surface area, 1,000" 到 1,600、"dd G" < −20 kcal mol⁻¹、uhb < 3、clash < 3 | "Twenty-one designs were experimentally characterized, and one was found to assemble into octahedral structures by negative-stain EM" ⇒ **1/21**；cryo-EM 6.5 Å、"The cryo-EM structure of the 600-kDa octahedral nanocage with 24 ZnPPaM molecules bound to it was solved to 6.5" Å；非对称单元对设计模型 3.4 Å 主链 r.m.s.d.；笼内 SP2-like 组件与原 SP2 序列同一性 87% |

### 这两层之间的优先级关系（本文最有价值的方法学结论）

1. **静态判据（能量/SASA/rotamer/配位几何/形状互补/ddG）只决定"能不能下单、会不会折叠、会不会按设计组装"**，全文没有任何一处用计算打分去预判耦合强弱。
2. **激子耦合这一物理性质进入设计的方式是"必要条件约束"而不是"打分项"**：对称性保证两个色素位点能量近简并（这是耦合的前提），6D 哈希保证配位几何与色素相对位姿在化学上可行，clash 过滤保证放得下。这三条都可算、都可提前筛；而耦合能本身（cm⁻¹）直到拿到真实晶体几何后才由 QM 计算。
3. **顺序不可倒过来**：实测证据是 SP1（几何最像天然、结构最准）耦合只有 87 cm⁻¹，弱于几何"设计没做到"的 SP2（241 cm⁻¹）。也就是说静态几何代理与目标性质在本体系里**不同向**，把静态判据当性质预测器会被直接打脸。
4. 因此本文的命中率分母是"全部通过静态判据并下单的数量"（48 个），而不是"预测通过数"；性质层面的成败只能靠光谱买。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（在全文里的位置） |
|---|---|---|
| 43 designs / 13 scaffolds | 通过静态判据后选定做湿实验的设计数与支架数 | Results 第 1 段末（De novo protein design strategy） |
| 48 | 送测设计总数（43 + 依晶体结构反馈再设计的 5 个变体） | Results 第 1 段末；Stability and pigment binding 段首句 |
| 48/48 可溶；48/48 SEC 呈二聚体峰 | 表达与组装层命中率（分母＝全部下单数） | Results 第 2 段（Special pair protein stability and pigment binding） |
| 20 → 15 | apo-SAXS 测得数 → 与设计模型一致数 | Results 第 2 段 |
| ≥140 mg l⁻¹ | 三个高产设计的表达量 | Results 第 2 段 |
| 20.6–28.4 kDa（179–261 aa） | 单体大小范围 | Results 第 1 段末 |
| 1.7 Å | SP1、SP2 主链对设计模型的 Cα r.m.s.d.（结构闸门值） | Results X-ray 段首句 |
| 2.0 / 2.4 / 2.5 / 3.05 Å | SP1 holo / SP2 apo / SP2 holo / SP3x apo 分辨率 | Results X-ray 段；Methods 晶体学两段 |
| 0.23–0.28 Å（9 个天然特殊对）；0.22 Å（同一复合物两结构互差）；0.25 Å（SP1 色素对模型） | 色素环几何精度 | Results X-ray 段（SP1） |
| 3.5 Å | SP2 色素二聚体偏离设计模型的 r.m.s.d.（48 原子环对齐口径） | Results SP2 段；Methods Protein structure alignment 段 |
| ~1.6 Å | holo 态结合腔相对 apo 的扩张量 | Results SP2 段 |
| 94% / 87% | SP3x 对 SP3、笼内 SP2-like 组件对 SP2 的序列同一性 | Results 第 3 段末 / 超复合物段 |
| 241 cm⁻¹ vs 239 cm⁻¹（实验分裂 477 cm⁻¹） | 计算耦合（晶体结构）vs 实验耦合（Qy 分裂的一半） | Results Excitonic coupling 段（Fig. 4 之后那段） |
| 87 cm⁻¹ | SP1 的计算耦合（弱耦合） | Results 单独一段（Fig. 3e 之后） |
| 199 cm⁻¹ 与缩放因子 1.212 | PigmentHunter 自动算的色素间耦合，及为与 CD 计算一致而采用的经验缩放 | Methods PigmentHunter 段末 |
| 14,925 / 14,750 cm⁻¹；500 cm⁻¹；10⁶ 次采样；10 cm⁻¹ 卷积 | 模拟谱的色素位点能与无序展宽设置 | Methods PigmentHunter 段 |
| 350 cm⁻¹（Qy/Qx）、1,150 cm⁻¹（Soret）、−0.25 eV 平移 | CD 模拟线形与能量平移参数 | Methods CD 谱段 |
| 6 个单重激发态/色素；CAM-B3LYP；PCM n-octanol | EET 电子耦合计算设置 | Methods Calculation of Chl dimer excitonic coupling 段 |
| B3LYP/6-31G* | 色素 QM 几何优化与 ESP 电荷所用级别 | Methods MD 段 |
| 4,000 步最小化 / 40,000 步（30 ps）/ 500,000 步（1,000 ps）/ 弃前 200 ns / NPT 300.0 K / 2 fs / 1.0 nm / 2 ps⁻¹ | MD 协议全部数字 | Methods 的三段 MD |
| 669 → 668 nm；ε 49,900 → 38,200 M⁻¹cm⁻¹；690 nm 处 9,400 → 17,700 | 单体变二聚体时 Qy 峰位移与消光系数变化（振子强度重排） | Results Excitonic coupling 段 |
| 673 / 692 nm（75 K） | 二聚样品的两条发射带 | Results 低温光谱段 |
| 荧光寿命 >3 ns | SP2 的长寿命激发态（为后续电子转移预留） | Discussion 末段 |
| Kd：SP1 290/430 nM，SP2 110 nM、2.0 μM，SP3 350/940 nM；CD 拟合 SP2 300 nM/2.5 μM、SP3 800 nM/1.0 μM；荧光 1:1 拟合 660/480/120 nM | 双位点结合强度（色素二聚体结合） | Results 第 3 段（长波长 CD 段） |
| 59%；2,058 → 839 ps；>4,000 → <1,000 a.u. | 接触打印 2D 阵列里 CpcA−PEB → SP2−ZnPPa 的能量传递效率与供体寿命/强度下降 | Results 能量传递段末 |
| ~5 μm 线宽、~300 nm 空间分辨率 | 纳米压印接触打印与 FLIM 像素尺度 | Results 能量传递两段 |
| 21 → 1 | 纳米笼送测设计数 → 负染 EM 判定形成八面体数 | Results Chl-binding supercomplex 段 |
| 600 kDa；24 个 ZnPPaM；12 个二聚体 + 8 个三聚体；6.5 Å；3.4 Å | 八面体笼的组成与结构精度 | Results supercomplex 两段 |
| SC > 0.6；1,000 < SASA < 1,600；ddG < −20 kcal mol⁻¹；uhb < 3；clash < 3 | 纳米笼五道静态筛选闸口 | Methods Nanocage design 段 |
| 每支架前 10 个对接构象 | 对接后进入序列设计的构象数 | Methods Nanocage design 段 |
| 204,039 vs 19,355 | Topaz 重训所用粒子数对比（初训集） | Methods cryo-EM 数据处理段 |
| 97% | 天然光合的能量传递/电荷分离量子产率（本文 motivation 基线） | Introduction 首段 |

## 5. 结论——作者说了什么

1. 造出了能按定义好的紧密几何**容纳叶绿素二聚体的全新设计蛋白**，其中 SP1 以亚埃精度复现天然紫色细菌特殊对几何，SP2 给出另一种更紧凑的非天然几何。
2. 这些蛋白里的叶绿素**确实发生激子耦合**：吸收/荧光/CD 加 TD-DFT 共同支持；SP2 有 Cotton 效应、吸收荧光带位移、以及与天然捕光蛋白 CpcA 的能量传递活性。
3. **对称性一举两得**：既简化设计、又保证两个色素位点能量等价从而增强耦合，还让特殊对蛋白能被装进更大的超复合物。
4. 纳米笼是**走向人工光合区室（类囊体/色素泡）的第一步**，12 个 ZnPPaM 二聚体装上八面体笼。
5. 作者自陈的不足与下一步：SP1 耦合弱于 SP2 也弱于天然 BChl 特殊对；光谱性质的预测本身很难（耦合量与热能量、Franck−Condon 振动/声子重组能同量级），需要稳健模型体系去 benchmark 理论方法；要做定向进化去改色素特异性和红移幅度；下一步是把激发态电子交给低电位受体，实现电荷分离。摘要级承诺见第 3 行的 Abstract："A de novo-designed protein that precisely assembles a chlorophyll dimer has been developed"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

以下为推断。

1. **这篇的真正方法学贡献是"把物理性质拆层"**：可提前算的（对称性→近简并位点能；配位几何→6D 哈希；放置可行性→clash）留在设计期；不可提前算的（耦合能、光谱位移、能量传递效率）用一次性、廉价的观测探针（Qy 区 CD 双峰符号）先分流，再用贵的手段（75 K 光谱 + QM + 模拟谱）定性定量。对我们：UAA 酶活也必须这样切成"设计期能约束的必要几何条件"与"只能造出来才能读的化学结局"两层，并承认第二层没有计算替身。
2. **静态精度与功能方向不同向是本篇最硬的负面内证**：结构最准的 SP1 耦合最弱（87 vs 241 cm⁻¹）。这直接说明"设计模型自洽性"类判据（我们熟悉的 pLDDT/ipTM/RMSD/ddG）**不能当功能预测器**，只能当"能否折叠/能否组装"的准入闸。
3. **决定性质的那个自由度恰恰是不受设计控制的自由度**（第二个色素的 6 个平动/转动）。这条与我们的处境同构：UAA 反应里底物/UTP 的取向与质子转移路线也是"第二个分子"的自由度；若目标函数里没有显式变量，精度做得再高也不解决问题。
4. **"配比率对照 + 符号一致性"这类零成本判据值得抄**：0.3 vs 2.0 当量区分单体/二聚体、CD Cotton 符号区分几何手性排列，都是不需要新仪器就能排除竞争解释的设计。我们的产物化学判定同样应当先设计"能区分主路径与副路径"的对照读数（如 S0 游离 UTP vs S1 pppUA vs S2 环化），而不是只报"有没有活性"。
5. **本文的 MD 与 QM 都不在漏斗里**：QM 用于事后把几何翻译成可观测谱，MD 在正文连一个输出量都没报告。因此它不能作为"用 QM/MD 预筛功能"的命中率先例——这一点与底稿 `sources/baker.md:537` 的判断方向一致（QM 是定义成功标准的工具），但底稿对"筛选器"的表述需要按本文实际内容修正（见第 9 节）。
6. **命中率数字要看清分母**：48 送测 → 20 SAXS → 3 深入表征 → 3 个晶体结构（其中一个还是 holo 失败后的替代设计）→ 真正"功能成功"只有 SP1/SP2（其中 SP2 的色素几何是意外）。纳米笼 21 → 1。这类"少数几个能深做"的漏斗形态说明：**深表征瓶颈在蛋白量与晶体，不在计算**，我们的漏斗瓶颈在湿实验产物鉴定通量，形态相似但瓶颈位置不同，不能类比迁移阈值。

## 7. 局限与失败（作者的 + 我们读出的）

作者自己写出来的：

- **性质预测难，且需要被 benchmark**：作者承认 "Prediction of the spectroscopic properties of a Chl dimer in a protein is complicated by the fact that Chl-Chl coupling energies are typically similar in magnitude to the available thermal energy" 这一类困难，并给出 "Accurate optical predictions require benchmarking of theoretical methods using robust model systems"。
- **SP1 没达到设计意图的功能水平**：几何最像天然，却 "SP1 exhibits weaker excitonic coupling than SP2 and the BChl special pair of purple photosynthetic bacteria, despite its close structural similarity to the latter"；作者把天然更强归因于 bacteriochlorin 更大的 Qy 跃迁偶极矩——即**色素本体的选择**超出了蛋白设计能调的范围。
- **SP2 的色素没有按设计摆放**（3.5 Å 偏差），SP3 的 holo 结构从未解出，笼内色素取向受分辨率限制无法确定："Although the resolution is not sufficient to confidently determine the orientations of the Chl molecules, the cryo-EM density map is consistent with the Chl dimer geometry in the SP2 crystal structure"。
- **只做到了能量传递，没做到电荷分离**：作者明确下一步 "To couple light absorption to charge separation for solar fuel production, the next step is to engineer the transfer of the excited-state electron to a low-potential electron acceptor"；也未做定向进化。
- **冷冻电镜分辨率被样品柔性/制冰压坏限制**：连续构象异质性 "likely limited the resolution of the full nanocage map"，柔性用 3D 变异性分析可视化（补充电影）。

我们读出的（推断）：

- **计算与实验的"吻合"里有一个经验缩放因子**：PigmentHunter 自动算的色素间耦合是 199 cm⁻¹，但为与 CD 计算一致"the intersite coupling was rescaled by a factor of 1.212 to a value of 241 cm" —— 而 241 cm⁻¹ 正是被用来和实验 239 cm⁻¹ 对账的那个数。模拟谱复现实验因此不是完全独立的确认（本文未讨论该缩放对结论强度的影响）。
- **成功判据存在事后改述**：SP2 的色素几何偏离设计，但作者把它归入"满足目标"，因为目标层被表述为"造出一个非天然几何"。这套表述让"设计是否成功"在几何层与性质层之间可切换，读者无法判断哪一层是预注册的。
- **没有阴性验证**：所有 QM/CD/低温光谱都只在被选中的 SP1/SP2/SP3 上做，43 个设计里其余 40 个从未做性质层面测量 ⇒ 无法回答"设计期判据能否提前区分强弱耦合"，这一正是我们最想借的结论。
- **MD 属于"有协议、无读数"**：Methods 写得很细（协议、步数、恒温恒压、切割半径），正文里没有任何 MD 导出的量。据此不能推断 MD 起了判据作用。

## 8. 对 UAA 筛选的迁移判断

可迁移（怎么用）：

1. **两层判据的分工写法直接照搬**（DP2R 标准里的判据分层）：给每个物理/化学性质列出三行——①设计期可算的必要条件（如对称性/几何/配位等价类）②造出来之后才能读的观测探针（一次实验就能分流的那种）③需要贵手段才能定量的量。凡第①类不能预测第③类的情况，必须在判据文档里明写"不许用①的分数给③排序"。
2. **用对称性/等价性代替显式打分**：当我们没有能力算出"催化构象自由能"时，可以像本文用 C2 强制近简并位点能那样，用**结构性约束**（两个候选供体位点等价、金属离子配位几何等）把目标性质的前提做成硬约束，剩下的交给实验。
3. **零成本的竞争假说对照**：0.3 vs 2.0 当量式配比对照、CD 符号对照，是我们能在产物化学里复制的形式——例如"加入游离 UTP 是否竞争掉产物信号"（S0 vs S1）、"环化产物与线性产物的质谱裂解/保留时间指纹"（S1 vs S2），先让替代解释被排除，再谈活性。
4. **把性质探针做便宜**：本文选 ZnPPaM/ZnPPa 而非天然 Chl a，就是为了让"一对色素"的信号不被其他色素淹没。对我们：应优先选**背景最干净**的检测底物/同位素标记体系，而不是信号最强的体系。

不可迁移（为什么不能照搬）：

1. **cm⁻¹ 级的激子耦合有"一光谱就能分流"的廉价探针（Qy 区 CD 双峰符号），UAA 酶活没有等价探针**。产物化学是逐条样品的，通量上限决定我们不能把 48 个设计全送测——所以本文"静态判据只闸准入、性质一律实测"的做法在我们的预算下不成立，必须另找可算的性质代理，且要按本文教训承认代理可能不同向。
2. **不能引用本文任何比率当作我们的成功概率**：48/48 可溶、15/20 SAXS、21→1 纳米笼，这些数字来自 hyperstable C2 重复蛋白支架这一**已被前人反复验证过的支架家族**，与我们从天然聚合酶骨架出发的处境无关（这是支架性质不是方法性质）。
3. **本文的 QM 不构成"QM 预筛酶活"的先例**：TD-DFT/EET 全部在拿到真实几何之后运行，用于把几何翻译成光谱；从未有候选因为 QM 打分被提前剔除。同理，本文的 MD 没有产生任何判据数字。谁要主张"用 QM/MD 判催化可行性"，本文既不支持也不反驳，只能另找参照。
4. **不许把本文的结构阈值当功能阈值**：1.7 Å 主链、0.23–0.28 Å 色素环、SC>0.6/ddG<−20/uhb<3 是"能否按设计组装"的闸口；而功能（激子耦合、能量传递 59%）与最严的结构精度反向。UAA 侧同理：Foldseek/pLDDT/几何 RMSD 一类静态阈值只配闸准入，不配预测活性。
5. **展示库通量、binder 的 pAE/ipTM 阈值与本篇无关**，不得混用（DP2R 标准明禁）。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/chlorophyll2024.txt

- 本卡全部英文引句都是**照这一份**本地纯文本写的（Europe PMC fullTextXML 去标签、HTML 实体已解码、空白已折叠；未改写内容）。同一论文若存在 NCBI 抽取版本，句内参考文献编号位置不同，故不混用。
- 对照底稿：`sources/baker.md:525-537`（本卡只读不改）。与本地全文不一致之处，单独列出、不改底稿：
  1. 底稿写"作者/单位: …（UW-IPD + **ASU/其他**）"；全文作者单位列表里**没有 Arizona State**，实际含 UW（IPD/生化/细胞生物学与 Skirball/化学/微生物）、Fred Hutchinson Cancer Center、University of Sheffield、NYU School of Medicine、UC Santa Barbara、Lawrence Berkeley（ALS）、HHMI-UW。
  2. 底稿写"候选生成方法: 全原子/配体约束的 de novo 设计（**RFAA 系工具链**）"；全文的方法链是 **motif-hash（6D 变换哈希）+ NeRF 构象生成 + C2 重复蛋白支架 + symmetric Rosetta FastDesign**，通篇未出现 RFAA/RFdiffusion。
  3. 底稿写"计算筛选器: 色素几何/间距约束 + **模型置信度**"；全文实际筛选器是 Rosetta 全原子能量、Chl 二聚体可及表面积、His rotamer、His Nε−金属配位几何（设计层）与 SC/SASA/ddG/uhb/clash 五闸（纳米笼层）；**没有任何 AF2/pLDDT/ipTM 类模型置信度**。
  4. 底稿写"命中率数字: 本论文正文未给统一的设计→表达→命中计数"；正文其实给了可核对的漏斗数（43 设计/13 支架 → 48 全可溶 → 20 SAXS/15 一致 → 3 深表征 → SP1/SP2/SP3x 结构；纳米笼 21 → 1）。缺的是"计算预测通过数"这一层，不是没有计数。
  5. 底稿把 MD 概括为"用于光谱建模与参数化"——方向正确，但需补一句：**正文未报告任何 MD 导出的判据量**，MD 只在 Methods 与作者贡献里出现。
  6. 底稿把 Fig. 4 图注里的激子分裂句写成了带省略号的拼接式引句（跨了句子边界）；本文该处完整原句是模拟谱由 PigmentHunter 生成、分裂对应 241 cm⁻¹ 的 DFT 估计耦合，本卡改用完整句逐字引（见 §2/§3），不用省略号拼接。
- 字段映射：本文第 3 节 ↔ CSV `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- 未核验项：补充图 1–22、补充表 1–7、Source Data Fig. 2/4/5 的具体数值本卡未引用；PDB/EMDB 条目内数据未打开核对。
- 本卡自检：`scripts/verify_literature_cards.py --only B40 --no-report`（输入：本目录 `*.md` + `sources_map.json` + 上述底稿），逐字比对本卡全部引句；结果见交付回报。

<!--CSV回填
work_type=论文
target=容纳叶绿素（ZnPPaM/ZnPPa）特殊对的 C2 对称同源二聚体光合能量转移蛋白；及其八面体纳米笼超复合物（无蛋白靶点，靶是小分子色素二聚体几何）
backbone_generation=既有超稳定 C2 重复蛋白（DHR）同源二聚体支架库 + motif-hash（His 的 N-Cα-C 6D 变换哈希）匹配口袋残基对 + symmetric Rosetta FastDesign 重设计色素口袋；NeRF 自造 His-Chl 二聚体 motif 构象；纳米笼用 RPXDock 对接 SP2 二聚体与 C3 三聚体后 symmetric RosettaDesign 设计界面
computational_filters=设计期四闸：Rosetta 全原子能量、Chl 二聚体可及表面积、His rotamer、His Nε-金属配位几何；色素放置可行性=clash 检查；无 AF2/pLDDT/ipTM 类模型置信度；纳米笼五闸：形状互补、界面 SASA、ddG、埋藏未满足氢键、clash；激子耦合本身只在事后用 TD-DFT/EET（CAM-B3LYP）+ PigmentHunter Frenkel 激子模型计算，不参与筛候选
thresholds=结构闸门：主链 Cα r.m.s.d. 1.7 Å 内、色素环 48 原子对齐 0.23-0.28 Å（对 9 个天然特殊对）；纳米笼：SC>0.6、1000<界面SASA<1600、ddG<-20 kcal/mol、uhb<3、clash<3、每支架取前 10 对接构象；设计期四闸原文未给数值阈值；QM/光谱：EET 每色素 6 个单重激发态、PCM n-octanol、CD 线形 FWHM 350/1150 cm-1 与 -0.25 eV 平移、PigmentHunter 10^6 次位能采样 FWHM 500 cm-1、耦合经验缩放因子 1.212（199→241 cm-1）；MD：4000 步最小化 + 40000 步(30 ps) + 500000 步(1000 ps) 平衡、弃前 200 ns、NPT 300 K、2 fs、PME 1.0 nm、Langevin 2 ps-1
md_used=是（仅事后：Amber18 ff14SB/TIP3P + MCPB.py 给 ZnPPaM 做力场参数与结构弛豫，配合 CD 谱计算；正文未报告任何 MD 导出的判据量或通过率，未参与漏斗筛候选）
qm_used=是（仅事后判定与解释：Gaussian 16 EET/CAM-B3LYP 算色素二聚体电子耦合 241/87 cm-1、PCM n-octanol；B3LYP/6-31G* 做色素几何优化与 RESP 电荷；PigmentHunter 与 Excitonic Analysis Tool 模拟吸收/荧光/CD；全部在晶体结构或设计模型几何上运行，未用于下单前剔除候选）
experimental_methods=E. coli(Lemo21 DE3) 自诱导表达 + Ni-NTA/TEV/SEC；SDS-PAGE 与 SEC 保留体积；apo-SAXS(FoXS 比对)；far-UV CD 与 222 nm 热熔；UV/vis/NIR CD（Qy 区 bisignate Cotton 效应）；吸收/荧光滴定拟 Kd；75 K 蔗糖/海藻糖膜低温吸收与荧光、TCSPC 寿命；X-ray（SP1 2.0、SP2 2.4/2.5、SP3x 3.05 Å）；纳米压印接触打印 2D 阵列 + FLIM/单光子计数；负染 EM 与 cryo-EM(6.5 Å, EMDB-40208/40209)；LC-MS 验证分子量
pipeline_counts=motif 哈希 + 数千支架 → 43 设计/13 支架选定送测（+5 个按晶体反馈的再设计变体 = 48）→ 48/48 可溶且 SEC 呈二聚体 → 20 个做 apo-SAXS 其中 15 与设计一致 → 3 个高产(≥140 mg/L)做完整光谱表征 → 结构：SP1 holo、SP2 apo/holo 解出，SP3 holo 失败改解 SP3x apo(3.05 Å)；功能确认只在 SP1/SP2/SP3 上做；纳米笼 21 个送测 → 1 个形成八面体笼 → cryo-EM 6.5 Å、600 kDa、24 ZnPPaM、非对称单元对模型 3.4 Å
hit_rate=设计与组装层：48/48 可溶、48/48 二聚体峰、15/20 SAXS 一致、SP1/SP2 主链 1.7 Å 内、SP1 色素几何 0.23-0.28 Å（对天然）但 SP2 色素偏离设计 3.5 Å；性质层：激子耦合证据只在 SP2（强，241 cm-1 计算/239 cm-1 实验）成立，SP1 弱（87 cm-1）、SP3 靠 CD 符号间接支持；能量传递效率 59%；纳米笼 1/21；原文未给"计算预测通过数"这一层分母
best_metric=无 Kd/活性统一最优值可引（结合：SP2 吸收拟合 Kd1=110 nM、Kd2=2.0 μM；功能：SP2 激子耦合分裂 477 cm-1、CpcA-PEB 到 SP2-ZnPPa 能量传递效率 59%、激发态寿命 >3 ns）
cost_or_stat_note=计算成本正文未给；实验成本可见的规模：43-48 个设计全表达、20 个 SAXS、3 个完整光谱表征、3 个晶体结构、21 个纳米笼设计、cryo-EM 双网格 204,039 粒子重训 Topaz；QM 为单体级 EET/CAM-B3LYP 与 PigmentHunter 10^6 次系综采样；MD 为 Amber18 平衡至 1 ns 生产段（协议数字见阈值键），未报告核算成本
role_in_timeline=Baker 组把 de novo 设计从"结合/折叠"推进到"带激发态物理功能的色素二聚体性质"的节点：第一次给出设计蛋白中叶绿素二聚体的实验结构并证明激子耦合与能量传递；同时暴露静态设计判据与目标物理性质不同向（结构最准的 SP1 耦合最弱），并把 QM/MD 定位成事后翻译工具而非漏斗筛子；其纳米笼分支把 B 链的对称组装能力（DHR 支架、RPXDock、界面设计）与功能色素位点合流，为后续光合区室类结构铺路
source_pointer=data/interim/baker_lit/ft/chlorophyll2024.txt（Europe PMC fullTextXML for PMC11213709，118,884 B）；对照底稿 sources/baker.md:525-537；PDB 7UNJ/7UNI/8EVM，EMDB EMD-40208/EMD-40209；代码 github.com/atommoyer/stapler、/atom-moyer/nerf、/atom-moyer/getpy
CSV回填-->
