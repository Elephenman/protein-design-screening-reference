# [B10; C08] 用深度学习设计荧光素酶——把 de novo 设计的目标从「会不会结合」升级到「会不会催化一个新反应」，并实测了漏斗迭代带来的命中率跃升（3/7,648 → 2/46）

Yeh AHW, Norn C, Kipnis Y, Tischer D, Pellock SJ, Evans D, Ma P, Lee GR, Zhang JZ, Anishchenko I, Coventry B, **Cao L**, Dauparas J, Halabiya S, DeWitt M, Carter L, **Houk KN**, **Baker D**（华盛顿大学 IPD + UCLA + UCSC + 西安交大）
Nature 2023, 614(7949):774–780 · DOI 10.1038/s41586-023-05696-3 · PMID 36813896 · PMCID PMC9946828
开放获取（CC BY 4.0）· https://pmc.ncbi.nlm.nih.gov/articles/PMC9946828/
（同一篇在两条口径里都登记：Baker 组编号 B10、曹龙兴组编号 C08；曹龙兴为本文第 12 作者。）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **`B10; C08`**（组：Baker组; 曹龙兴组）；卡片文件名把非字母数字换成连字符：`B10-C08_*.md` |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory 登记 fetch_channel=epmc_fulltext，fetch_url `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9946828/fullTextXML`），2026-10-16 抓取 |
| 本地全文（门禁认定的唯一全文） | `data/interim/baker_lit/ft/luciferase2023.txt`（58,865 B；strip_tags + norm 归一后的纯文本，含正文、图注、Extended Data 图注、致谢/作者贡献/数据与代码可得性） |
| 其余登记底稿（非全文） | `sources/baker.md:134–145`（B10 条目）、`sources/cao.md:142–156`（C08 条目） |
| 证据级别 | **全文级**（本卡每一条英文引句都在本地全文里逐字命中；门禁 `--only "B10; C08"` 自检通过） |
| 未取到的部分 | **Methods 正文不在本地全文里**——原文自己声明补充文件才含方法（"This file contains the Methods section"），故 family-wide hallucination 的损失函数权重、MCMC 步数、SSM 文库构建细节、DFT 泛函/基组/溶剂模型、MD 力场与体系构建参数本卡一律标「正文未给」。补充信息（Supplementary Figs 1–4、Supplementary Tables 1/2/5、Supplementary Methods）与 Source Data 也未取到 |
| 特别提示 | 本文与 binder 类论文（B09/B12）最大的差别：**筛选判据里没有界面 pAE_interaction**，用的是配体（DTZ）结合能/氢键/形状互补/contact molecular surface + AF2 pLDDT；机制侧才出现 DFT 与 MD |

## 1. 这篇到底解决什么（大白话）

生物发光（荧光素酶 + 荧光素底物）在活体成像里比荧光蛋白方便（不需要激发光），但天然荧光素酶又少、又多二硫键、还不认合成的底物、彼此不特异，做不了多路复用。这篇想**从零造一个全新的酶**：它要催化的反应（合成底物 DTZ 的氧化化学发光）在自然界里没有对应的酶，也没有任何天然结构可以直接借用。作者的做法分两层：第一层解决「骨架从哪来」——用深度学习做 family-wide hallucination，把 NTF2 这个小超家族「幻觉」出 1,615 条理想化新骨架，每条都带一个能装下 DTZ 的疏水口袋；第二层解决「活性位点怎么放」——先用量子化学与实验文献确定「反应经过阴离子中间体」，于是在口袋里放一个精氨酸胍基去稳负电荷，再用 RIF 场对接 + Rosetta/ProteinMPNN 出序列。第一轮 7,648 条设计送测只中 3 个（LuxSit 等），第二轮把「第一轮学到的活性位点几何 + 更稳的 ProteinMPNN + AF2 pLDDT>92 预筛骨架」用起来，只送 46 条就中 2 个（HTZ3-D2/G4）；再经饱和突变把 LuxSit-i 的光子通量提到比 LuxSit 高 100 倍以上、对 DTZ 的选择性比对其他底物高 50–100 倍以上，并在人细胞里做出双通道复用检测。

一句话：**这是 Baker 组第一次把「催化」而非「结合」作为 de novo  DL 设计的交付目标，并公开了两轮漏斗的原始计数。**

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **天然骨架根本不够用，而且改造天然蛋白的行为不可预测**。作者原话："there are few native structures with binding pockets appropriate for DTZ, and the effects of sequence changes on native proteins can be unpredictable"；引言里也说 de novo 酶设计"but has been limited by a lack of suitable protein structures and the complexity of native protein sequence-structure relationships"。天然的 NTF2 结构本身也有毛病："Native NTF2 structures have a range of pocket sizes and shapes but also contain features that are not ideal, such as long loops that compromise stability"。
   → **应对**：不做「找骨架 → 改骨架」，改为**批量生成骨架**：先 "we first docked DTZ into 4,000 native small-molecule-binding proteins" 用对接确定「哪类折叠能装 DTZ」（拓扑选择），再对该拓扑做 family-wide hallucination 生成 1,615 条理想骨架。作者把这条写成结论："Computational enzyme design has been constrained by the number of available scaffolds, which limits the extent to which catalytic configurations and enzyme-substrate shape complementarity can be achieved"，并宣称 "The use of deep learning to produce large numbers of de-novo-designed scaffolds here eliminates this restriction"。
2. **要催化的反应没有几何模板（不知道过渡态长什么样）**。传统做法依赖理想活性位点/theozyme："Computational enzyme design generally starts from an ideal active site or theozyme consisting of protein functional groups surrounding the reaction transition state that is then matched into a set of existing scaffolds"，但本文的底物类酶 "the detailed catalytic geometry of native marine luciferases is not well understood because only a handful of apo structures and no holo structures with luciferin substrates have been solved"，且历史证据都来自虚拟溶剂计算或纯有机溶剂发光——"As all the historical pieces of evidence are based on calculations in the virtual solvents or chemiluminescence in ideal organic solvents"，所以 "the detailed mechanism of a luciferase-catalysed luminescence reaction has remained unclear"。
   → **应对（本文的换题方式）**：**不设计「匹配过渡态几何的 theozyme」，改设计「稳定阴离子态的反应场」**。依据是 QM 与实验都指向阴离子路径："the chemiluminescent reaction proceeds through an anionic species and that the polarity of the surroundings can substantially alter the free energy of the subsequent single-electron transfer (SET) process with triplet molecular oxygen"；据此 "we sought to design a shape-complementary catalytic site that stabilizes the anionic state of DTZ and lowers the SET energy barrier, assuming that the downstream dioxetane light emitter thermolysis steps are spontaneous"——注意这里明确**假设**下游二氧杂环丁烷分解自发发光，即把不能验证的化学步骤排除在设计目标之外。落点变成一个可几何化的动作："To stabilize the anionic state, we focused on the placement of the positively charged guanidinium group of an arginine residue to stabilize the developing negative charge on the imidazopyrazinone group"，实施为 "An arginine guanidinium group was placed adjacent to the N1 atom of the imidazopyrazinone group to stabilize the negative charge"。
   → **代价**：设计目标从「过渡态稳定」退化为「阴离子/反应场稳定」，因此对「为什么某个设计活性高」只能事后用 DFT/MD 解释（见第 3 节 M 段），不能事前打分排序。
3. **第一轮命中率极低，几乎不可用**。原文计数："After sequence optimization, the designs were filtered on the basis of ligand-binding energy, protein-ligand hydrogen bonds, shape complementarity and contact molecular surface, and 7,648 designs were selected and ordered as pooled oligos for experimental screening"，结果 "Three active designs were identified"（0.039%）。
   → **应对**：作者自己归因并改动两处：**把第一轮学来的活性位点几何固化成模板**（用 "the histidine and arginine substrate interaction geometries that were most successful in the first round"）+ **序列端从 RosettaDesign 换成 ProteinMPNN** + **骨架端先用 AF2 置信度预筛**（"with matching pocket shapes and high model confidence (AlphaFold2-predicted local-distance difference test (pLDDT) > 92)"）。第二轮："we selected and experimentally expressed 46 designs in E. coli and identified 2 (HTZ3-D2 and HTZ3-G4) that had luciferase activity with the h-CTZ luciferin substrate"，原文明写效果："The success rate increased from 3/7,648 to 2/46 sequences in the second round, probably owing to the knowledge of active-site geometry from the first round and the increased robustness of the ProteinMPNN method of sequence design"。
   → **代价**：作者用了 probably owing to（推测归因），**没有做拆解实验**分离「知识迁移」与「ProteinMPNN 更鲁棒」各自的贡献；且第二轮靶（h-CTZ）与第一轮靶（DTZ）不同，两次漏斗不是同题重测。
4. **设计的酶拿不到实验结构**。原话："Although we were not able to determine the crystal structure of LuxSit, the structure predicted by AlphaFold2"，随后用预测与设计的吻合度代替实验结构："is very close to the design model at the backbone level (root-mean-square deviation (RMSD) = 1.35 Å)"。
   → **应对**：改用**功能侧的独立证据**支撑设计模型——对底物结合口袋每个残基做饱和突变并逐个测活："we constructed a site-saturation mutagenesis (SSM) library in which each residue in the substrate-binding pocket was mutated to every other amino acid one at a time"，再检验设计模型的预言是否成立："the active-site-saturation mutagenesis results support the design model, with the Tyr14-His98 and Asp18-Arg65 dyads having key roles in catalysis and the substrate-binding pocket largely conserved"。计算侧另加一条对照：把预测的结合自由能变化与实测活性对画（Extended Data Fig. 5），结论是 "This shows that the sequence is near-optimal for substrate binding and the design model is reliable"。
   → **代价**：**结构层面没有实验确证**（既无晶体也无冷冻电镜结构落在本卡可读到的正文里）；「设计模型可靠」的证据是活性与突变偏好的一致性，属于间接证据。
5. **天然与改造过的荧光素酶都不特异，定向进化也治不好**。作者原话："Native and previously engineered luciferases are quite promiscuous, with activity on many luciferin substrates"，并承认 "a luciferase with high specificity to one luciferin substrate has been difficult to control even with extensive directed evolution"。
   → **应对**：把**小而形状互补的口袋**当作特异性的来源（设计阶段就追求 shape complementarity），实测得 "By contrast, LuxSit-i exhibited exquisite specificity for its target luciferin, with 50-fold selectivity for DTZ over bis-CTZ"、"28-fold selectivity over 8pyDTZ (differing only in one nitrogen atom) and more than 100-fold selectivity over other luciferin substrates"，并总结 "Overall, the specificity of our designed luciferases is much greater than that of native luciferases"。选择性差异再用 MD 给出机理解释："the added benzylic carbon of bis-CTZ (green trace) disrupts the shape complementarity between LuxSit-i and the transition states"，"This charge stabilization is necessary for the reaction to proceed, explaining the high substrate specificity of LuxSit-i for DTZ over bis-CTZ"。
6. **活性仍不够好、发光动力学不合适**。LuxSit-i 的 "the luminescent signal decays over time owing to fast catalytic turnover"，且 "Similar to native luciferases that use CTZ, the apparent Michaelis constants ( K m ) of both LuxSit-i and LuxSit-f are in the low-micromolar range"；细胞里衰减更慢被归因于扩散："The more extended emission kinetics in HeLa cells is likely due to the diffusion rate of DTZ across cell membranes"。第二轮两个 h-CTZ 设计也比 LuxSit 弱（见第 4 节 ~25%/~58% 那条）。
   → **应对**：用随机化文库穷举三个位点："We generated a fully randomized library at 60, 96, and 110 positions to screen all possible combinations exhaustively"，得到 "The A96M and M110V mutants (highlighted in pink) increase activity by 16-fold and 19-fold, respectively, over LuxSit"，再组合出 "Optimization guided by these results yielded LuxSit-f (A96M/M110V), with a flash-type emission kinetic, and LuxSit-i (R60S/A96L/M110V), with a photon flux more than 100-fold higher than that of LuxSit"。
   → **本文未解决**：作者对 R60 为何可突变只给推测——"Arg60 is confirmed to be mutable among all selected mutants as Arg60 may be structurally less well-defined because it emanates from a loop and has no hydrogen-bonding partner"；h-CTZ 设计的活性差距没有再优化；以及「直接从计算机算出这么高的活性」这件事，作者明写仍未解决："by contrast, the predicted differences in ligand-side-chain interactions between LuxSit and LuxSit-i are very subtle" 之后接的括注 "achieving such high activities directly from the computer remains a challenge in computational enzyme design"。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **深度学习（骨架生成）**：trRosetta 作为可微/可评估的结构预测网络，用它对序列的「预测置信度」当损失函数做 **hallucination**；拓扑信息用 NTF2 家族的结构一致性项加进去（作者称 family-wide hallucination）。为什么：只有生成足够多、口袋形状足够多样的骨架，才谈得上摆出不同的催化几何假设——"our family-wide hallucination method opens up an almost unlimited number of scaffold possibilities for substrate binding and catalytic residue placement"。
- **物理能量侧（活性位与序列）**：RifGen 生成旋光基相互作用场（RIF）→ RifDock 对接进骨架空腔 → RosettaDesign 两步序列优化（含 PSSM 偏置，"with a bias towards the naturally observed sequence variation to ensure foldability"）；第二轮序列端换成 ProteinMPNN，理由原文是 "which can result in better stability, solubility and accuracy than RosettaDesign"。
- **结构自洽性侧（送测前筛子）**：Rosetta 配体结合能、蛋白-配体氢键数目、shape complementarity、contact molecular surface；第二轮额外加 AF2 pLDDT>92 与 Cα RMSD。
- **QM/DFT 用在哪一步（原文明确）**：**不进入计算筛选漏斗**。用在两处——(i) 设计之前：确立「反应经过阴离子态」这一设计前提，据此决定要放精氨酸胍基（Extended Data Fig. 1 图注："Density functional theory (DFT) calculation suggested that the formation of an anionic state is the essential electron source for the activation of triplet oxygen"）；(ii) 设计之后：算反应自由能面与解释活性/选择性差异（"We used a combination of density functional theory (DFT) calculations and molecular dynamics (MD)"）。计算由 Houk 组承担，作者贡献里写明 "K.N.H. mentored D.E. and P.M. for MD and quantum mechanics calculations and contributed to the writing of the mechanistic parts of the manuscript"。
- **MD 用在哪一步（原文明确）**：同样**只用于事后机理**，不做候选排序。三处具体用法：① 把反应中间体 Int2/Int3 分别装进 LuxSit 与 LuxSit-i 跑轨迹比较结合——"Int2 and Int3 were docked into both LuxSit and LuxSit-i and the bindings were evaluated by molecular dynamics (MD)"；② 观测关键氢键/电荷距离随时间演化——"The distances between His98 to O1 (top row) and Arg65 to N1 (bottom row) of the substrate were plotted throughout 500 ns MD simulations"；③ 解释 bis-CTZ 为何不被认——对应 "MD simulations suggest that this arises from greater transition-state shape complementarity"。
- **实验侧**：寡核苷酸池 → PCR 扩增/Gibson 式组装/pBAD 克隆 → DH10B 转化 → 菌落水平喷 DTZ 成像直接筛活性 → 96 孔表达复测 → 纯化表征（SDS-PAGE/SEC/质谱/CD 熔解）→ 稳态动力学（Km、kcat/Km）→ SSM 与 NNK 随机化文库做活性优化 → HEK293T/HeLa 活细胞成像与双信号复用检测。**注意这里的「筛选」是直接筛功能（发光），不是先筛可表达/会结合。**

### A. 骨架生成与活性位设计→第一轮送测（DTZ）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 拓扑选型 | 天然小分子结合蛋白结构集合 | 把 DTZ 对接进去看哪类折叠能容纳："we first docked DTZ into 4,000 native small-molecule-binding proteins"；图注给出排除条件："The RIF was docked into 4,000 native small-molecule-binding proteins, excluding proteins that bind the luciferin substrate using more than five loop residues" | 口袋形状互补性与尺寸合适；排除「靠 5 个以上 loop 残基抓底物」的蛋白 | 选定 NTF2-like 超家族："Most of the top hits were from the NTF2-like protein superfamily" |
| S2 家族级幻觉（骨架） | "Starting from the sequences of 2,000 naturally occurring NTF2s"；结构参照 "obtained from 85 experimental structures of NTF2-like proteins" | trRosetta 网络在序列空间做 Monte Carlo（步内做点突变并预测结构）；核心区用结构一致项、loop/可变区用网络置信度；允许 loop 长度插删；再嵌入埋藏长程氢键网络 | "we used the confidence of the neural network in the predicted structure"，"supplemented with a topology-specific loss function over core residue pair geometries"；"in the loop regions, we also allowed the number of residues to vary, which resulted in short near ideal loops"；"To further encode structural specificity, we incorporated buried, long-range hydrogen-bonding networks"（具体权重正文未给，在 Supplementary Methods） | "The resulting 1,615 family-wide hallucinated NTF2 scaffolds provided more shape-complementary binding pockets for DTZ than did native small-molecule-binding proteins"；质量对照 "Using the family-wide hallucination scaffold generation protocol, we generated 1,615 scaffolds and found that these yielded better predicted RIF binding energies than the native proteins"，几何上 "This method samples protein backbones that are closer to native NTF2-like proteins" |
| S3 底物构象系综 | 阴离子态 DTZ | "we first generated an ensemble of anionic DTZ conformers"（生成协议细节在补充方法，正文未给阈值） | 覆盖阴离子底物的可用构象 | 逐构象携带一个 RIF 进入对接 |
| S4 RIF 生成（活性位蓝图） | 每个 DTZ 阴离子构象 | "we used the RifGen method" 在三维网格上枚举侧链旋光相互作用场（氢键 + 非极性堆积），并强制放入精氨酸胍基 | 胍基邻位 N1："An arginine guanidinium group was placed adjacent to the N1 atom of the imidazopyrazinone group to stabilize the negative charge"；口袋内 "An average of eight side-chain rotamers, including an arginine residue to stabilize the anionic imidazopyrazinone core, were positioned in each pocket" | 网格为 "millions of placements of amino acid side chains" 量级的 RIF 场 |
| S5 RIF 对接 | 每条骨架的中心空腔 × 每个构象-RIF | "RifDock was then used to dock each DTZ conformer and associated RIF in the central cavity of each scaffold to maximize protein-DTZ interactions"；HBNet 与 DTZ 的相互作用被显式要求 | "interactions of these HBNet side chains with DTZ were explicitly required in the RifDock step to ensure the preorganization of residues that are essential for catalysis"；取 "For the top 50,000 docks with the most favourable side chain-DTZ interactions" | **50,000** 条进入序列优化的对接 |
| S6 两步序列设计 | 50,000 条 top dock | RosettaDesign 优化剩余序列；骨架/侧链/底物在笛卡尔空间弛豫 | 第一步 "the identities of all RIF and HBNet residues were kept fixed, and the surrounding residues were optimized to hold the side chain-DTZ interactions in place and maintain structural specificity"；第二步 "the RIF residue identities (except the arginine) were also allowed to vary, as Rosetta can identify apolar and aromatic packing interactions that were missed in the RIF owing to binning effects"；"During sequence design, the scaffold backbone, side chains and DTZ substrate were allowed to relax in Cartesian space"；序列偏置 "with a bias towards the naturally observed sequence variation to ensure foldability" | 全套设计序列进入 S7 过滤 |
| S7 送测前过滤（第一轮） | 全部设计 | 按四个物理量过滤 | "filtered on the basis of ligand-binding energy, protein-ligand hydrogen bonds, shape complementarity and contact molecular surface"（**具体数值阈值正文未给，在 Supplementary Methods**） | "7,648 designs were selected and ordered as pooled oligos for experimental screening" |
| S8 直接筛功能（第一轮湿实验） | 寡核苷酸池 | "Oligonucleotides encoding the two halves of each design were assembled into full-length genes and cloned into an Escherichia coli expression vector"；图注补充 "Computationally designed DNA sequences were purchased in an oligo array, where the fragments were amplified by PCR, assembled, and ligated into a pBAD bacterial expression vector"；菌落成像直接筛："A colony-based screening method was used to directly image active luciferase colonies from the library"，"Each colony grown on the LB agar plate represented one luciferase design. The plates were sprayed with DTZ solution and imaged to identify active colonies using a ChemiDoc imager"，复测 "the activities of selected clones were confirmed using a 96-well plate expression" | 判据＝**是否发光**（功能读数，不是表达/结合读数）；正文未给发光强度截断值 | "Three active designs were identified"（3/7,648 ≈ 0.039%）；最优记为 LuxSit，"which at 117 residues (13.9 kDa) is, to our knowledge, smaller than any previously described luciferase" |

### B. 第二轮（h-CTZ）——把第一轮的知识搬进漏斗

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S9 | 新底物 h-CTZ（分子形状不同）："Because the molecular shape of h-CTZ is different from that of DTZ, we created an additional set of NTF2 superfamily scaffolds" | 重新造一批口袋形状匹配的骨架 → 安装催化位（用第一轮最成功的 His/Arg 相互作用几何）→ 剩余序列交给 ProteinMPNN | 骨架端硬阈值："with matching pocket shapes and high model confidence (AlphaFold2-predicted local-distance difference test (pLDDT) > 92)"；催化位端 "using the histidine and arginine substrate interaction geometries that were most successful in the first round for DTZ"；序列端换用 ProteinMPNN（理由见 A 段工具箱） | 一批 pLDDT>92 的新骨架池 |
| S10 | 第二轮设计全集 | 送测前过滤 | "After filtering on the basis of the AlphaFold2-predicted pLDDT, Cα RMSD,"（数值阈值正文未给） | "we selected and experimentally expressed 46 designs in E. coli and identified 2 (HTZ3-D2 and HTZ3-G4) that had luciferase activity with the h-CTZ luciferin substrate"（2/46 ≈ 4.3%）；原文自评 "The success rate increased from 3/7,648 to 2/46 sequences in the second round, probably owing to the knowledge of active-site geometry from the first round and the increased robustness of the ProteinMPNN method of sequence design" |

### C. 命中之后的表征、优化与机理（不参与漏斗）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S11 结构确证 | LuxSit | 尝试结晶失败 → 用 AF2 预测与设计模型比 + 生化表征 | "Although we were not able to determine the crystal structure of LuxSit, the structure predicted by AlphaFold2"，"is very close to the design model at the backbone level (root-mean-square deviation (RMSD) = 1.35 Å)"；热稳定判据是 CD 熔解："CD melting experiments showed that the protein is not fully unfolded at 95"（°C，摘要另记 melting temperature 高于 95 °C） | 设计活性位描述："The designed LuxSit active site contains Tyr14-His98 and Asp18-Arg65 dyads, with the imidazole nitrogen atoms of His98 making hydrogen-bond interactions with Tyr14 and the O1 atom of DTZ"；"The centre of the Arg65 guanidinium cation is 4.2 Å from the N1 atom of DTZ and Asp18 forms a bidentate hydrogen bond to the guanidinium group and backbone N-H of Arg65"；发光峰 "Incubation of LuxSit with DTZ resulted in luminescence with an emission peak at around 480 nm" |
| S12 口袋饱和突变（图谱＋验证） | LuxSit 口袋每个残基 | SSM 逐位点全突变并测活，得氨基酸偏好谱 | "we constructed a site-saturation mutagenesis (SSM) library in which each residue in the substrate-binding pocket was mutated to every other amino acid one at a time"；关键结论 "Arg65 is highly conserved"，"its dyad partner Asp18 can only be mutated to Glu (which reduces activity), suggesting that the carboxylate-Arg65 hydrogen bond is important for luciferase activity"；"As all active variants had hydrogen-bond donors and acceptors at these positions, the dyads might help to mediate the electron and proton transfer required for luminescence" | "the active-site-saturation mutagenesis results support the design model"；计算对照侧 "which suggested that these designed catalytic residues are not favourable for substrate binding"，"This shows that the sequence is near-optimal for substrate binding and the design model is reliable" |
| S13 三 site 穷举优化 | 位点 60/96/110 | NNK 全组合随机化 + 菌落筛 + 逐株测活 | "We generated a fully randomized library at 60, 96, and 110 positions to screen all possible combinations exhaustively"；单突变增益 "The A96M and M110V mutants (highlighted in pink) increase activity by 16-fold and 19-fold, respectively, over LuxSit" | "Optimization guided by these results yielded LuxSit-f (A96M/M110V), with a flash-type emission kinetic, and LuxSit-i (R60S/A96L/M110V), with a photon flux more than 100-fold higher than that of LuxSit" |
| S14 机理（DFT + MD，事后） | LuxSit 与 LuxSit-i、DTZ 及 bis-CTZ | DFT 画反应自由能面；把中间体对接进两个酶跑 500 ns MD 比距离/结合；再对 bis-CTZ 做同样 MD | 机理假设来自 QM："Density functional theory (DFT) calculation suggested that the formation of an anionic state is the essential electron source for the activation of triplet oxygen"；总目标写法："the goal of this study is to design an enzyme reaction field surrounding the substrate to stabilize the anionic substrate state and alter the local proton activity, solvent polarity, and hydrophobicity"；MD 观测 "Int2 and Int3 were docked into both LuxSit and LuxSit-i and the bindings were evaluated by molecular dynamics (MD)"，"The distances between His98 to O1 (top row) and Arg65 to N1 (bottom row) of the substrate were plotted throughout 500 ns MD simulations"，"This binding orientation brings N1 of the substrate much closer to Arg65, providing better charge stabilization for the high energy transition state"；选择性解释 "the added benzylic carbon of bis-CTZ (green trace) disrupts the shape complementarity between LuxSit-i and the transition states" | 支撑 "We used a combination of density functional theory (DFT) calculations and molecular dynamics (MD)" 的两条结论："the results support the anion-stabilization mechanism" 与 LuxSit-i 过渡态电荷稳定更好；泛函/基组/力场正文未给 |
| S15 应用（细胞与复用） | LuxSit-i | 哺乳细胞表达 + 定位标签 + 与 RLuc/PP-CTZ 组成双通道 | 特异性判据 "By contrast, LuxSit-i exhibited exquisite specificity for its target luciferin, with 50-fold selectivity for DTZ over bis-CTZ"，"28-fold selectivity over 8pyDTZ (differing only in one nitrogen atom) and more than 100-fold selectivity over other luciferin substrates"；复用靠底物分辨与光谱分辨（528/20 与 390/35 滤片） | "HEK293T cells expressing LuxSit-i-mTagBFP2 showed DTZ-specific luminescence"；"Thus, the high substrate specificity of LuxSit-i enables multiplexed reporting of diverse cellular responses" |

**这套流程的骨架值得单独记住**：漏斗一共只有两道——**S7（四个物理量过滤）**和**S10（AF2 pLDDT/Cα RMSD/CMS/Rosetta 结合能过滤）**；QM 与 MD 一道都不在漏斗里，QM 在漏斗之前提供「该放什么相互作用」的前提，MD 在漏斗之后解释「为什么这个中、那个不中」以及「为什么只认这个底物」。湿实验的筛子是**直接测功能（发光）**，因此不存在 binder 论文里「先确认会表达/会结合」的中转层。

## 4. 关键数字台账（全部可在本地全文逐字检索到）

| 数值 | 含义 | 出处（原句片段所在段） |
|---|---|---|
| 4,000 | DTZ 被对接进去的天然小分子结合蛋白数（拓扑选样池） | Fig. 1e 图注与引言段（"we first docked DTZ into 4,000 native small-molecule-binding proteins"） |
| ≤5 个 loop 残基 | 拓扑选样的排除条件（排除靠太多 loop 抓底物的蛋白） | "excluding proteins that bind the luciferin substrate using more than five loop residues" |
| 2,000 | 起始的天然 NTF2 序列数 | "Starting from the sequences of 2,000 naturally occurring NTF2s" |
| 85 | 提供距离/取向分布参照的 NTF2-like 实验结构数 | "obtained from 85 experimental structures of NTF2-like proteins" |
| 1,615 | family-wide hallucination 生成的理想化 NTF2 骨架数 | "The resulting 1,615 family-wide hallucinated NTF2 scaffolds" |
| 数百万（millions） | RIF 网格中侧链摆放的枚举规模 | "on three-dimensional grids consisting of millions of placements of amino acid side chains"（此句在 Fig. 1c 图注，正文同段有 "we used the RifGen method"） |
| 平均 8 条 | 每个口袋里放置的旋光基（含 1 个精氨酸）数 | "An average of eight side-chain rotamers, including an arginine residue to stabilize the anionic imidazopyrazinone core, were positioned in each pocket" |
| 50,000 | 进入 RosettaDesign 序列优化的 top dock 数 | "For the top 50,000 docks with the most favourable side chain-DTZ interactions" |
| **7,648 → 3** | 第一轮送测设计数 → 命中活性设计数（≈0.039%） | "and 7,648 designs were selected and ordered as pooled oligos for experimental screening"；"Three active designs were identified" |
| 117 残基 / 13.9 kDa | LuxSit 大小（作者称比任何已报道荧光素酶都小） | "which at 117 residues (13.9 kDa) is, to our knowledge, smaller than any previously described luciferase" |
| AF2 vs 设计模型 Cα RMSD **1.35 Å** | 无晶体结构时的结构一致性替代证据 | "is very close to the design model at the backbone level (root-mean-square deviation (RMSD) = 1.35 Å)" |
| 4.2 Å | Arg65 胍基中心到 DTZ N1 的距离 | "The centre of the Arg65 guanidinium cation is 4.2 Å from the N1 atom of DTZ" |
| ~480 nm | LuxSit + DTZ 发光峰 | "Incubation of LuxSit with DTZ resulted in luminescence with an emission peak at around 480 nm" |
| >95 °C | 熔解温度/CD 下 95 °C 不完全展开 | "CD melting experiments showed that the protein is not fully unfolded at 95"；摘要 "with a melting temperature higher than 95 °C" |
| **pLDDT > 92** | 第二轮骨架预筛的 AF2 置信度阈值（本文明确给出的唯一数字阈值） | "with matching pocket shapes and high model confidence (AlphaFold2-predicted local-distance difference test (pLDDT) > 92)" |
| **46 → 2** | 第二轮送测数 → 命中数（HTZ3-D2、HTZ3-G4；≈4.3%） | "we selected and experimentally expressed 46 designs in E. coli and identified 2 (HTZ3-D2 and HTZ3-G4)" |
| 3/7,648 → 2/46 | 两轮成功率对比（作者自评归因） | "The success rate increased from 3/7,648 to 2/46 sequences in the second round" |
| 7.9 / 19.5 μM；~25% / ~58% Imax | HTZ3-D2 与 HTZ3-G4 的 Km 与最大信号（相对 LuxSit） | "HTZ3-D2 and HTZ3-G4 showed K m values of 7.9 and 19.5 μM with ~25% and ~58% I max of LuxSit, respectively" |
| 低 μM 段 Km | LuxSit-i/LuxSit-f 的表观米氏常数区间 | "Similar to native luciferases that use CTZ, the apparent Michaelis constants ( K m ) of both LuxSit-i and LuxSit-f are in the low-micromolar range" |
| +16 倍 / +19 倍 | A96M、M110V 相对 LuxSit 的活性增益 | "The A96M and M110V mutants (highlighted in pink) increase activity by 16-fold and 19-fold, respectively, over LuxSit" |
| >100 倍 | LuxSit-i（R60S/A96L/M110V）相对 LuxSit 的光子通量 | "with a photon flux more than 100-fold higher than that of LuxSit" |
| 38% | LuxSit-i 光子通量高于天然 RLuc 的幅度 | "and the photon flux (photons per second) is 38% greater than that of the native Renilla reniformis luciferase (RLuc)" |
| 10⁶ M⁻¹ s⁻¹ 量级 | LuxSit-i 的催化效率（作者称进入天然荧光素酶范围、超过既往 de novo 酶） | "the most active of these is a small (13.9 kDa) and thermostable (with a melting temperature higher than 95 °C) enzyme that has a catalytic efficiency on diphenylterazine"；"LuxSit-i has higher activity than any previous de-novo-designed enzyme" |
| 50 倍 / 28 倍 / >100 倍 | LuxSit-i 对 DTZ 相对 bis-CTZ、8pyDTZ、其余底物的选择性 | "with 50-fold selectivity for DTZ over bis-CTZ"；"28-fold selectivity over 8pyDTZ (differing only in one nitrogen atom) and more than 100-fold selectivity over other luciferin substrates" |
| 500 ns | LuxSit vs LuxSit-i 中间体复合物的 MD 采样长度 | "were plotted throughout 500 ns MD simulations" |
| 15,000 细胞 | 复用检测每孔用的细胞数 | 图注类描述（Fig. 4 图注 "Luminescence signals were acquired from the lysate of 15,000 cells in CelLytic M reagent"） |
| 数十轮（tens of rounds） | 对比：既往 de novo  retroaldolase 要几十轮定向进化才达同等催化效率 | "as tens of rounds of directed evolution were required to obtain catalytic efficiencies in this range for a designed retroaldolase, and the structure was remodelled considerably" |

## 5. 结论——作者说了什么

1. 深度学习批量生成骨架**解除了「可用骨架数量」对计算酶设计的限制**："Computational enzyme design has been constrained by the number of available scaffolds" → "The use of deep learning to produce large numbers of de-novo-designed scaffolds here eliminates this restriction"。
2. 口袋形状/尺寸的多样性让他们能**枚举多种催化几何假设**："The diversity of shapes and sizes of scaffold pockets enabled us to consider a range of catalytic geometries and to maximize reaction intermediate-enzyme shape complementarity"。
3. 设计出的 LuxSit 折叠在自然界没有对应："to our knowledge, no native luciferases have folds similar to LuxSit, and the enzyme has high specificity for a fully synthetic luciferin substrate that does not exist in nature"。
4. 加三个突变后活性超过既往任何 de novo 设计酶、催化效率进入天然荧光素酶区间："LuxSit-i has higher activity than any previous de-novo-designed enzyme"，且与 retroaldolase 的对比是 "as tens of rounds of directed evolution were required to obtain catalytic efficiencies in this range for a designed retroaldolase, and the structure was remodelled considerably"，而本文 "by contrast, the predicted differences in ligand-side-chain interactions between LuxSit and LuxSit-i are very subtle"。
5. 漏斗迭代的自我评价（作者原话，含归因的推测语气）："The success rate increased from 3/7,648 to 2/46 sequences in the second round, probably owing to the knowledge of active-site geometry from the first round and the increased robustness of the ProteinMPNN method of sequence design"。
6. 特异性带来多路复用应用："Thus, the high substrate specificity of LuxSit-i enables multiplexed reporting of diverse cellular responses"。
7. 作者自留的未解问题："achieving such high activities directly from the computer remains a challenge in computational enzyme design"；方法学定位（对他们后续最有价值的一句）："which is particularly important when the reaction mechanism and how to promote it are not completely understood"，"many alternative structural and catalytic hypotheses can be readily enumerated with shape and chemically complementary binding pockets but different catalytic residue placements"。
8. 外推主张（作者自己给的范围）："the approach developed here should be readily applicable to a wide variety of chemical reactions"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **他们的「QM/MD 有用」和我们的「QM/MD 有用」不是同一件事。** 本文 QM 的作用是**在下单之前定义「该造什么相互作用」**（阴离子 → 放精氨酸胍基），这是一个可以被翻译成几何约束的化学结论；MD 的作用是**在命中之后解释活性/选择性差异**。两者都没有用来给成千上万候选排序。→ 对我们：QM 的价值位置应放在「把化学事件翻译成可打分几何约束」这一环，而不是「直接判谁有活性」。
2. **第二轮的 4.3% 不是「漏斗变准了」，而是「送测集变小且被知识重塑了」。** 分母从 7,648 变成 46，同时第一轮的信息（His/Arg 几何）被固化成模板、骨架池被 pLDDT>92 提前削掉。所以 3/7,648→2/46 里「命中率」的可比性很弱，真正硬的信息是：**同一套自动化流程下，把上一轮的机制知识写进下一轮生成约束，比继续加大送测量更管用**。
3. **湿实验筛子直接读功能，是本文与 binder 漏斗最大的结构差别。** 因为产物（光子）可读、无需分离个体，他们能用菌落成像一次扫完 7,648 条；这带来一个后果：**计算侧过滤不必承担「省下表达成本」的重任，而承担「省下合成/测序与读数成本」**。我们的产物检测（LC-MS/MS）单价远高于发光读数，所以我们的漏斗末端容量必然受化学检测通量限制，不能照搬「送测数千条」的做法。
4. **作者用功能数据（SSM 活性谱）替代了缺失的实验结构。** 这是「结构证据拿不到时，用突变-活性一致性当设计模型的独立检验」的实例：SSM 显示关键 dyad 保守、突变偏好与原设计一致。→ 对我们：拿不到复合物结构时，「失活对照 + 关键位点突变活性谱」是能替代结构确证的信息层，不能只报一个活性数字。
5. **本文最可疑之处：设计目标与评价目标错位。** 他们设计时优化的是「阴离子态稳定 + 形状互补」，评价时用的是「发光强度」，而发光强度取决于 DFT 假设自发的后续步骤；作者明确写了 "assuming that the downstream dioxetane light emitter thermolysis steps are spontaneous"。也就是说**漏斗对「真正决定活性的高低」的那一步不做任何判别**，这解释了为什么 7,648 送测中 3、以及为什么三处突变的增益只能靠穷举与事后 MD 找到。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认的：①「从计算机直接算出这么高活性」仍未解决（"achieving such high activities directly from the computer remains a challenge in computational enzyme design"）；②LuxSit 无晶体结构（"Although we were not able to determine the crystal structure of LuxSit"）；③天然荧光素酶机理本身不清楚（"the detailed mechanism of a luciferase-catalysed luminescence reaction has remained unclear"）；④第二轮两个 h-CTZ 设计明显弱于 LuxSit（"HTZ3-D2 and HTZ3-G4 showed K m values of 7.9 and 19.5 μM with ~25% and ~58% I max of LuxSit, respectively"）；⑤归因是推测（"probably owing to"）。
- 我们读出的：①**送测前的四个物理量过滤与第二轮四项过滤，正文都没给数值阈值**，阈值在 Supplementary Methods（本文正文里唯一明确的数字阈值是 pLDDT>92），因此这张卡不能把「过滤」当成可复现的定量闸口引用；②两轮漏斗的**靶不同、生成集不同、序列方法不同**，同时改了三件事，"100 倍级"的相对提升无法归因；③MD/DFT 只在两个命中酶与少数中间体/底物上做，样本极小（500 ns 级轨迹、若干对接构象），属于**个案解释**而非可推广的判据；④设计时把「发光」简化为阴离子稳定 + 后续步骤自发，这一步假设没有实验检验（正文与 Extended Data 图注均为 proposed/suggested 语气）；⑤筛选池的构建（oligo 池、组装、克隆）成功率与库覆盖率正文未给，无法判断 3/7,648 里有多少设计实际被表达出来。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **「骨架数量不足」用生成解决，而不是用检索解决。** 当我们发现可用天然支架池太小（例如找不到带合适口袋的既有酶家族），本文给出的路径是：先用底物对接确定「哪类拓扑能装」（S1，含排除条件「靠 5 个以上 loop 抓底物」这种可写成规则的先验），再对该拓扑做家族级生成。对应我们：把「候选生成」与「候选打分」分开，生成端保证多样性，打分端才有可比较的对象。
2. **把不可直接优化的化学步骤，翻译成一个可几何化的替代目标。** 本文不做「匹配过渡态」，而做「稳定阴离子 + 合适的局部反应场」，落实为「胍基放在 N1 旁边 4 Å 级」。→ 我们对目标反应三步化学事件（分步化学事件）也应挑一个「能被几何约束表达的中间态/电荷态」作为设计目标，并明写哪些步骤被假设自发（本文明写了，这是可审计的诚实做法）。
3. **拿不到结构证据时，用「关键位点突变 → 活性谱」作为设计模型的独立检验**（SSM 那条），并把失活对照一起报。
4. **迭代时把上一轮机制知识写进下一轮生成约束**（His/Arg 几何模板 + 更鲁棒的序列模型 + pLDDT 预筛），并像本文一样**公开两轮各自的原始计数**（7,648/3 与 46/2），哪怕归因是推测。
5. **QM/MD 的位置可以直接照搬**：QM 前置到「定义该造什么相互作用」，MD 后置到「解释命中与选择性的差异」，都不进漏斗；这与本调研 B19/PLACER 对 MD 的否弃结论一致。

**不可迁移（为什么不能照搬）**

1. **pLDDT>92 / Cα RMSD / contact molecular surface / Rosetta 结合能这套过滤是「会不会把一个疏水底物按设计姿势抱住」的判据，不是「会不会催化目标成键」的判据。** 本文的成功读数只有一个化学事件（DTZ 氧化发光），且把后续步骤假设成自发；我们的目标包含多步质子/电子转移与竞争副产物路径，静态口袋自洽既不必要也不充分。本库判据标准不允许把这类结合判据当酶活闸口。
2. **本文的「3/7,648 → 2/46」绝不能被引用成我们的成功概率估计。** 第一轮的 0.039% 是「造一个全新酶的催化活性」这一最难情形的实测下限；第二轮的 4.3% 是在同族骨架 + 已知活性位模板 + 骨架预筛下的极小集合，且分母只有 46、分子只有 2。引用时只许引用**结构（漏斗两道、功能直读、迭代带知识）**，不许引用数字做校准或预期。
3. **菌落喷底物直接成像式的大通量功能筛选，在酶设计场景不存在。** 发光读数可在完整细胞/菌落上读，我们的产物身份必须 LC-MS/MS 逐样确认（还要区分中间体与副反应副产物），因此漏斗末端的容量由化学检测通量决定；把本文「送测 7,648 条」当作目标量级是错配。
4. **本文没有任何展示库/酵母表面/深测序环节**，因此不能作为「展示库通量」或「DMS 数据给筛子打分」的参照（那是 B09/B11/B12 那条线）；同理，binder 论文的 pAE_interaction<10 阈值在本篇完全不出现，不可混用。
5. **DFT/MD 在本文只是事后个案解释，没有产生任何「用 MD 预测催化效率」的可迁移指标**（只有 500 ns 距离轨迹与自由能剖面图）。任何「用 MD 判酶活」的主张，本文给不了命中率支持。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/luciferase2023.txt

- 本地纯文本（唯一全文，本卡全部英文引句都从这一份复制粘贴）：`data/interim/baker_lit/ft/luciferase2023.txt`（Europe PMC `fullTextXML`，`strip_tags` + `norm` 后的纯文本；正文、Fig. 1–4 图注、Extended Data Fig. 1–10 图注、致谢、作者贡献、数据/代码可得性都在其中；**Methods 不在其中**，原文声明 "This file contains the Methods section"）。
- 登记底稿行号：`sources/baker.md:134–145`（B10 条目）、`sources/cao.md:142–156`（C08 条目）；时间线对照 `sources/baker.md:642`（2023 年段 [B10] 7,648→3、46→2）、`sources/baker.md:656–658`（MD/QM 角色判定第 1 条即以本文为例）。
- 代码/数据指针（正文原句可检）：RIF 对接实现、family-wide hallucination 脚手架生成脚本与全部生成骨架、设计脚本均以 URL 形式给出（Code availability 段），LuxSit-i 基因序列入库 "The gene sequence for LuxSit-i has been deposited to GenBank under the accession number OP820699"。
- CSV 字段映射：本卡第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字/是否用MD/是否用QM`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检方式**：`scripts/verify_literature_cards.py --only "B10; C08" --no-report` 把卡内所有「直双引号 + 纯英文 + ≥20 字符 + ≥12 字母」的片段，在门禁认定的本文全文（`/ft/` 下那份）与两份登记底稿里逐字查找；本卡引句均从本地全文复制，不跨参考文献编号、不跨 `Fig. 1` 之类图号拼接（凡原文两句之间夹有引文序号处，本卡拆成两条或只引其后半段）。结果见本次运行输出（PASS，引句数见 `quotes=N/N`）。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 4 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文
target=催化合成底物 DTZ（二苯基噁哒嗪）与 h-CTZ（2-脱氧共协三嗪）氧化化学发光的全新荧光素酶 LuxSit/LuxSit-f/LuxSit-i（117 残基、13.9 kDa）与 HTZ3-D2/HTZ3-G4；NTF2-like 超家族全新骨架
backbone_generation=先做 DTZ 对接 4,000 个天然小分子结合蛋白定拓扑（NTF2-like），再以 2,000 条天然 NTF2 序列 + 85 条实验结构为参照，用 trRosetta 置信度损失 + 拓扑一致项做序列空间 MCMC（family-wide hallucination，loop 允许插删、嵌入埋藏长程 HBNet）生成 1,615 条理想化骨架；活性位用 RifGen 生成 RIF（含精氨酸胍基压 N1）、RifDock 对接进空腔；序列端第一轮 RosettaDesign 两步优化（PSSM 偏置）、第二轮改 ProteinMPNN
computational_filters=第一轮（送测前）：配体结合能、蛋白-配体氢键、shape complementarity、contact molecular surface；第二轮：AlphaFold2 pLDDT、Cα RMSD、contact molecular surface、Rosetta 计算结合能（第二轮骨架生成阶段另用 pLDDT>92 预筛）；对接阶段取 side chain-DTZ 相互作用最好的前 50,000 个 dock；界面氢键网络（HBNet）与 DTZ 的相互作用在 RifDock 中显式要求以保证催化残基预组织
thresholds=pLDDT>92（本文正文唯一明确给出的数字阈值）；top 50,000 docks；排除靠 5 个以上 loop 残基结合底物的天然蛋白；口袋平均 8 条侧链旋光基（含 1 个 Arg）；第一轮四项过滤与第二轮四项过滤的具体数值正文未给（在 Supplementary Methods）；AF2 预测 vs 设计模型 Cα RMSD 1.35 Å 为事后一致性证据非筛选阈值
md_used=是（仅事后机理，不进筛选漏斗）：把 Int2/Int3 中间体分别对接进 LuxSit 与 LuxSit-i 后跑 500 ns MD，观测 His98-O1、Arg65-N1 距离随时间演化以解释 LuxSit-i 更高活性；bis-CTZ 过氧化物阴离子形态对接进 LuxSit-i 的 MD 用于解释对 DTZ 的 50 倍选择性；正文原句为 "We used a combination of density functional theory (DFT) calculations and molecular dynamics (MD)"
qm_used=是（两处，均不进漏斗）：设计前——DFT 与实验证据共同确立「反应经阴离子态、周围极性改变 SET 自由能」，据此把设计目标定为稳定阴离子并放 Arg 胍基（Extended Data Fig. 1 图注给出 DFT 结论与 ΔG_SET/GRCTIL 机理图）；设计后——DFT 计算 DTZ 化学发光自由能剖面（Int1→Int2→TS1→Int3→OSS TS2→Int4*→Int5）；QM/MD 由 UCLA Houk 组承担（作者贡献与致谢中写明 NSF 与 NSFC 22103060 提供计算资源）
experimental_methods=寡核苷酸池 → 两半片段 PCR 扩增组装 → pBAD 载体 → DH10B 转化 → 菌落水平喷 DTZ 用 ChemiDoc 成像直接筛发光活性 → 96 孔表达复测；纯化与表征（SDS-PAGE、SEC、去卷积质谱、far-UV CD 与 CD 熔解）；稳态动力学与发光光谱；口袋残基饱和突变文库（SSM）与位点 60/96/110 的 NNK 全组合文库；HEK293T/HeLa 活细胞成像与核/膜/线粒体定位；与 RLuc-PP-CTZ 的底物分辨与光谱分辨（528/20、390/35）双通道复用检测
pipeline_counts=拓扑选样 4,000 个天然结合蛋白 → 幻觉起点 2,000 条天然 NTF2 序列 → 1,615 条理想骨架 → top 50,000 docks → 过滤后 7,648 条送测（oligo 池）→ 3 条命中（0.039%，LuxSit 等）；第二轮 46 条表达 → 2 条命中（HTZ3-D2、HTZ3-G4；4.3%）；优化侧 SSM 覆盖口袋每残基全突变 + 三 site NNK 全组合 → LuxSit-f 与 LuxSit-i（>100 倍光子通量）
hit_rate=第一轮 3/7,648 ≈ 0.039%；第二轮 2/46 ≈ 4.3%；作者自评提升并给出推测归因（"The success rate increased from 3/7,648 to 2/46 sequences in the second round, probably owing to the knowledge of active-site geometry from the first round and the increased robustness of the ProteinMPNN method"）；两轮靶与序列方法均不同，故非同一集合的严格前后对比
best_metric=LuxSit-i 对 DTZ 的催化效率 kcat/Km 处于 10⁶ M⁻¹ s⁻¹ 量级（作者称高于既往任何 de novo 设计酶、进入天然荧光素酶范围），光子通量比天然 RLuc 高 38%、比 LuxSit 高 100 倍以上；熔解温度高于 95 °C；对 DTZ 相对 bis-CTZ 50 倍、相对 8pyDTZ 28 倍、相对其他底物 >100 倍选择性；第二轮两个设计仅为 LuxSit 的 ~25%/~58% Imax（Km 7.9/19.5 μM）
cost_or_stat_note=未记录（正文与 Extended Data 图注未给 GPU/CPU 时长、每设计计算成本或测序/合成单价；成本侧只隐含在「7,648 条 oligo 池送测」的规模里）；MD 为 500 ns/体系；正文唯一数字阈值为 pLDDT>92；补充方法中的过滤阈值与建库细节本卡未取到
role_in_timeline=深度学习从「设计会结合的蛋白」跨到「设计会催化的全新反应」的开端（2023）；同时暴露旧范式代价——7,648 送测仅中 3，逼出后续以活性位预组织为判据的便宜打分器（PLACER/B17-B19）与原子级生成（RFdiffusion2/B20、RFAA/B13、LigandMPNN/B28）；本调研 MD/QM 角色判定中「MD 只做事后机理顾问」的一手例证之一
source_pointer=data/interim/baker_lit/ft/luciferase2023.txt（Europe PMC fullTextXML，PMCID PMC9946828，2026-10-16 抓取）+ sources/baker.md:134-145 + sources/cao.md:142-156；正文链接 https://pmc.ncbi.nlm.nih.gov/articles/PMC9946828/
CSV回填-->
