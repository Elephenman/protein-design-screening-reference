# [B33] 超螺旋匹配 + 几何哈希：为"重复序列肽段"设计模块化结合蛋白，并打到内源无序区

Wu Kejia, Bai Hua, Chang Ya-Ting, Redler Rachel, McNally Kerrie E., Sheffler William, … Derivery Emmanuel, Silva Daniel Adriano, Bhabha Gira, Ekiert Damian C., Baker David（华盛顿大学 Biochemistry/IPD + NYU + MRC LMB）
Nature 2023, 616:581-589 · DOI 10.1038/s41586-023-05909-9 · PMID 37020023 · PMCID PMC10115654
开放获取（CC BY 4.0）· https://pmc.ncbi.nlm.nih.gov/articles/PMC10115654/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B33**（组：Baker组） |
| 本文取回方式 | NCBI efetch 兜底通路（batches.tsv：`fallback_ok[ncbi_efetch]`），本地存 `fulltext/B33_PMC10115654_fullTextXML.xml` 与去标签纯文本 `fulltext/B33_PMC10115654_text.txt`（约 110 KB，单行长文本，无换行符） |
| 对照底稿 | `sources/baker.md:431-441`（原卡为摘要级元数据，且明写"未逐段核对方法细节与命中率"；本卡补齐全工作流程、阈值与两轮实测计数） |
| 证据级别 | **全文级**（本卡全部引句在第 9 节声明的底稿里逐字命中，门禁 PASS） |
| 未取到的部分 | Extended Data 图与表（含 Extended Data Table 1a/1b 的逐靶命中明细、Extended Data Fig. 1 的非 PPI 设计示例）、Supplementary Table 1 的晶体学统计、Source Data 蛋白质组学全表、Fig 原图数值。凡引用这些处本卡明写"正文只给概述，明细在未取到的扩展数据里" |
| 特别提示 | 全文抽取里参考文献编号以裸数字留在句内（如 energies 12 , interface），本卡引句要么绕开、要么原样保留，不做跨句拼接 |

## 1. 这篇到底解决什么（一句话与大白话）

**一句话**：给"由二/三肽重复单元串成、骨架呈多聚脯氨酸II（PPII）构象的肽段"，从头设计一个同样呈超螺旋的螺旋重复蛋白（DHR），让蛋白与肽的超螺旋参数（rise/twist/radius）同相位、并让蛋白侧链与肽骨架之间形成成排的叉齿状（bidentate）氢键，从而做出 nM~pM 级、可模块化拆装的肽结合蛋白；再用"改个别重复模块"打破对称性，把识别范围扩到非重复序列和人源无序蛋白区段（ZFC3H1/PAXT）。

**大白话**：天然蛋白里 armadillo 重复、TPR 这类"积木式"蛋白能一段一段地咬住带重复序列的肽，但几何被天然骨架锁死、亲和力大多只到 µM。本文的思路是把"锁死"变成"匹配"：任何重复聚合物都绕出一个超螺旋，用三个数（每个重复单元沿轴平移 rise、绕轴旋转 twist、离轴半径 radius）就能刻画；让设计蛋白的这三个数和目标肽的这三个数对上（rise/twist 几乎相等、radius 差够大不撞），再把"肽骨架上那些必须被满足的极性氢键"预先做成一张查询表（几何哈希），界面就被约化成"查表拼装"而不是自由搜索。最后用晶体结构证明拼出来的和设计的几乎一样，用活细胞重定位和 HeLa 裂解液 pull-down 证明拿出去能用。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **难点一：模块化识别的前提是"几何相位对得上"，对不上就根本没有一一对应可言。**
   现象/证据：作者把这列为两个主要挑战之一 —— "This requires solving two main challenges: first, building protein structures with a repeat spacing and orientation matching that of the target peptide conformation; and, second, ensuring the replacement of peptide-water hydrogen bonds in the unbound state with peptide-protein hydrogen bonds in the bound state"，并解释为什么它是硬约束："if individual repeat units in the protein are to bind individual repeat units on the peptide in the same orientation, the geometric phasing of the repeat units on protein and peptide must be compatible"。
   **他们做了什么**：把"匹配"降级成三个可计算的数（rise / twist / radius）："All repeating polymeric structures trace out superhelices that can be described by three parameters: the translation (rise) along the helical axis per repeat unit; the rotation (twist) around this axis; and the distance (radius) of the repeat unit centroid from the axis"；然后两侧各造一大库（"We generated large sets of repeating-protein backbones that sampled a wide range of superhelical geometries"、"We then generated corresponding sets of repeating-peptide backbones by randomly sampling di-peptide and tri-peptide conformations (avoiding intra-peptide steric clashes), and then repeating these 4-6 times to generate 8-18-residue peptides"），再按固定容差配对："requiring the rise to be within 0.2 Å, the twist to be within 5° and the radius to differ by at least 4 Å"，并交代为什么 radius 反而要差开："the difference in radius is necessary to avoid clashing between peptide and protein; the peptide can wrap either outside or inside the protein"。
   **应对后仍留下的代价**：容差把可配对几何变稀疏，而且随肽的重复单元长度不均衡 —— "For the polyproline helix, there are roughly three residues per turn, and, probably because of this, we obtained more designs that target three-residue than two-residue proline-containing repeat units"；正文未给出"骨架库 → 匹配对"的通过率数字。

2. **难点二：肽骨架上被埋掉的极性基团若不补氢键，结合要付脱水能代价（这正是亲和力做不高的物理原因）。**
   现象/证据："the NH and C=O groups make hydrogen bonds with water in the unbound state that need to be replaced with hydrogen bonds to the protein upon binding to avoid incurring a substantial free-energy penalty"。
   **他们做了什么**：不指望自由搜索做出氢键，而是把"叉齿状氢键"预先当作**特权相互作用**建库 —— "bidentate hydrogen bonds between side chains on the protein and pairs of backbone groups or backbone and side-chain groups on the peptide could allow the burying of sufficient peptide surface area on the protein to achieve high-affinity binding without incurring a large desolvation penalty"，"As the geometric requirements for such bidentate hydrogen bonds are quite strict, we developed a geometric hashing approach to enable rapid identification of rigid-body docks of the peptide on the protein that are compatible with ladders of bidentate interactions"；建表范围明确列出："Hash tables were generated for Asn and Gln making bidentate interactions with the N-H and C=O groups on the backbone of a single residue or adjacent residues, for Asp or Glu making bidentate interactions with the N-H groups of two successive amino acids, and for side-chain-side-chain pi-pi and cation-pi interactions"。 docking 侧利用"同轴匹配只剩两个自由度"把搜索降维："we took advantage of the fact that for matching two superhelical structures along their common axis, there are only two degrees of freedom: the relative translation and rotation along this axis"，网格步长 "we performed a grid search in these two degrees of freedom, sampling relative translations and rotations in increments of around 1 Å and 10°"；不够的就直接扔："docks for which the number of matches was less than a set threshold were discarded"。
   **应对后仍留下的代价**：①"less than a set threshold"的**具体数值正文未给**；②哈希只覆盖上述几类几何，界面其余部分靠后续能量优化补 —— "The remainder of the protein sequence is then optimized for folding and peptide binding"；③哈希命中的残基在序列优化里被钉住不动："keeping the residues that were identified in the hash matching fixed, and enforcing sequence identity between repeats in both the peptide and the protein"。

3. **难点三：首轮实验确实做出来了，但亲和力与特异性都偏低 —— 这是本文方法学跃迁的真实动因。**
   现象/证据："Many of the designs bound peptides with sequences similar to those targeted, but the affinity and specificity were both relatively low, with most of the successes for three-residue repeat units"；表达端还有硬损耗："Out of 49, 30 were monomeric and soluble"。
   **他们做了什么**（第二轮把协议改成四条可检查的约束）：
   - 几何/化学特异性："First, we required that each non-proline residue in the peptide make specific contacts with the protein, and that the pockets and grooves engaging side chains emanating from the two sides of the peptide were quite distinct"；
   - 逐残基能量检验："Second, after the design stage, we evaluated the change in binding energy (Rosetta ddG)"，随后 "and selected only designs for which the design target sequence made the most favourable interactions with the designed protein"；
   - 去掉非特异疏水面："Third, we used computational alanine scanning to remove hydrophobic residues on the protein surface that did not contribute to binding specificity, to decrease non-specific binding"；
   - 构象收敛检验（本文里相当于给每个设计做"分布外稳健性"测试）："Fourth, to assess the structural specificity of the designed peptide-binding interface, we performed Monte Carlo flexible backbone docking calculations, starting from large numbers of peptide conformations with superhelical parameters in the range of those of the proteins, and selected those designs with converged peptide backbones (root-mean-square deviation (RMSD) < 2.0 between the 20 lowest ddG designs) close to the design model (RMSD < 1.5)"；
   - 另外在下单前加了一道分子动力学一致性过滤："and which consistently retained more than 80% of the interchain hydrogen bonds in 20-ns molecular dynamics trajectories"。
   **应对后仍留下的代价**：第二轮仍是漏斗 —— "We tested 54 second-round designed protein-peptide pairs using the yeast flow cytometry assay described above"、"Forty-two of the designed proteins were solubly expressed in E. coli , and 16 bound their targets with considerably higher affinity and specificity than in the first round"。逐靶命中率的分母只写在 Extended Data Table 1a/1b（本卡未取到），正文只给汇总数，因此"提高多少倍"无法从正文算出。

4. **难点四：从头设计的骨架生成与验证太贵，会卡住整个漏斗。**
   现象/证据："Rosetta ab initio verifies that the design is a lower-energy state than the thousands of alternative conformations sampled"，"Simulating a protein using Rosetta@home can take several days on hundreds of CPUs"。
   **他们做了什么**：先用一组便宜的几何/包装门槛淘汰（"The loops are required to be within 0.4 Å of a naturally occurring loop or rebuilt"、"Structures with helices above 0.14 Å appear bent and kinked and are discarded"、"And poorly packed structures in which fewer than four helices are in contact with each other are filtered"、"Designs with poor core packing as measured by Rosetta Holes < 0.5 are then filtered"），再换掉最贵的那一步 —— "To speed this up, we used machine learning to filter designs that were most likely to fail"。
   **代价**：ML 过滤器的训练集与假阴率正文未给，等于用一个未标注黑盒替换了可解释的物理验证。

5. **难点五：想用到活细胞里，但常规支架（抗体片段）在胞质还原环境里折不好。**
   现象/证据："A bottleneck in such studies is that binders obtained from antibody scaffold (scFV or VHH)-based library screens often do not fold properly in the reducing environment of the cytosol, resulting in a loss of binding"。
   **他们做了什么**：把设计目标本身当作对策 —— "We reasoned that our binders would not have this limitation as they are designed for stability and lack disulfide bonds"；然后用 GFP/mScarlet 重定位到线粒体或过氧化物体做活细胞读出（"Thus, the PLPx6-RPB_PLP2_R6 pair retains binding activity in cells"，另一对 "Similar results were obtained for IRPx6-GFP and RPB_LRP2_R6_FW6"），并进一步验证两对可同时正交使用。
   **代价**：细胞内只有定位/共定位层面的证据，正文未给胞内亲和力或化学计量。

6. **难点六：方法天生只认"完全重复"的肽 —— 这是模块化的必然代价。**
   现象/证据：作者直述边界 —— "As described thus far, our approach enables the specific binding of peptides with perfectly repeating structures"。
   **他们做了什么**：只在少数模块上打破对称、其余不动以保住亲和力 —— "We broke the symmetry in the designed repetitive binding interface by redesigning both protein and peptide in one or more repeats of six-repeat complexes; the rest of the interface was kept untouched to maintain the binding affinity"；筛选口径也相应改成"换新的之后要更爱新肽"—— "Designs were selected for experimental characterization as described above, favouring those for which the new design had a lower binding energy for the new peptide than the original peptide"。做出 RPB_hyb1_R6（PLP2-PEP2-PLP2）与 RPB_hyb2_R6（IYP3-RYP3）。
   **代价**：只做到 1–3 个模块的替换，正文未给混合体的 Kd（只有归一化 Octet 热图），所以"去对称之后还剩多少亲和力"无法定量。

7. **难点七：天然无序区（IDR）没有重复语法可匹配 —— 想打到内源蛋白必须先回答"打哪一段"。**
   现象/证据：作者给的理由是 IDR 反而好打 —— "Intrinsically disordered regions have been very difficult to specifically target using other approaches, but are in principle good targets, because binding is not complicated by folding"；但真正的卡点是靶段选择。
   **他们做了什么**：写代码把"能被打"变成可筛条件 —— "To evaluate which endogenous proteins could at present be targeted with our method (Fig. 6 ), we developed Python code to search databases for sub-sequences that match permutations of the set of amino acid triplets for which we designed binders in this study"，然后"ranked all outputs to find the longest sub-sequence possible, and manually inspected the candidates to find sub-sequences landing in disordered regions"，选中 ZFC3H1 的两条理由（"this protein possesses the sequence (PLP)x4 within a large disordered domain, with downstream sequence (PEDPEQPPKPPF) within the reach of our binder design method"）；设计上把重复段与尾巴分开处理 —— "On the peptide side, we kept the (PLP)x4 backbone fixed, and used Monte Carlo sampling with Ramachandran map biases to model the remaining sequence (PEDPEQPPKPPF)"；结果 "These eight designs were expressed, and seven were found to bind the extended target peptide by bio-layer interferometry"。
   **代价**：亲和力显著下降 —— "The two highest-affinity designs-αZFC-high and αZFC-low-were found by fluorescence polarization to have K d values of less than 200 nM and around 1.2 µM, respectively"，作者自己写 "somewhat weaker than the synthetic constructs described above"；靶段是**从语法倒推挑出来的**，本文未解决"任意无序序列的从头靶向"。
   他们补的对照值得注意：用大小/表面组成相近但序列不匹配的另一条 binder 做非特异吸附阴性 —— "αZFC-low hence provides a control for non-specific association"，并用共洗脱与内源 pull-down 证明上下文可用 —— "demonstrating that the binder can recognize the target peptide in the context of a larger protein"、"Mass spectrometry revealed that MTR4 was enriched in the αZFC-high pull-down, demonstrating that the binder can recognize the native PAXT complex in a physiological context"。

8. **难点八：正交性不是设计出来的性质，而是测出来的，且有例外。**
   现象/证据："The PLPx6, LRPx6, PEWx6, IYPx6 and PKWx6 binders showed almost complete orthogonality in the concentration range from around 5 nM to 40 nM, with each design binding its cognate designed repeat peptide much more strongly than the other repeat peptides"，但 "Some cross-talk was observed between the PRMx6 and LRPx6 binders, perhaps involving the arginine residue, which makes cation-pi interactions in both designs"。
   **他们做了什么**：只做了归因假设（精氨酸在两套设计里都参与 cation-pi），并给出浓度区间作为使用边界。
   **本文未解决**：没有用突变实验验证这条解释，也没有把交叉反应纳入设计目标函数。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **骨架侧：DHR（designed helical repeat）重复蛋白骨架生成**。Rosetta fragment assembly guided by motifs（RPX motif 打分），"Each designed helical repeat (DHR) scaffold is formed by a helix-loop-helix-loop topology that is repeated four or more times"；选它是因为只有重复拓扑才能把"一个模块对一个肽单元"的对称性写进约束。
- **目标侧：重复肽骨架的随机构象生成**。随机采二/三肽的 φ/ψ 再串 4–6 次（见 A2）。
- **界面的核心工具：几何哈希（geometric hashing）**。把"能形成叉齿状氢键"的刚性取向预先枚举成查询表，对接时只查表不优化 —— "we developed a geometric hashing approach to enable rapid identification of rigid-body docks of the peptide on the protein that are compatible with ladders of bidentate interactions"。
- **序列侧：Rosetta 组合优化 + 对称设计**。"Design begins in a symmetrical mode in which each repeat is identical using the RepeatProteinRelax mover"，score function 固定（"The Rosetta score function beta_nov16 was chosen in all design cycles"）。
- **稳健性侧：正向对接（forward docking）+ 20 ns MD**。前者查"换构象还认不认"，后者查"界面氢键会不会掉"。
- **实验侧**：E. coli 表达 + Ni-NTA/TEV/SEC（含 SEC-MALS 定绝对分子量）、CD 热稳定性、SAXS 溶液形状、酵母表面展示 + FACS + Sanger、SSM 芯片突变库 + Illumina 富集、BLI（Octet RED96）、荧光偏振、X-ray 共晶、U2OS 活细胞成像（GFP/mScarlet 重定位）、HeLa 裂解液 pull-down + Western + LC-MS/MS 蛋白组。
- **没用到的方法**：QM、自由能微扰、结合自由能分解；MD 只做界面氢键保持率的稳定性校验，不进反应坐标、不做机理。

### A. 计算侧流程（从语法到可下单的设计）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 无（几何需求来自目标肽构象） | 生成 DHR 骨架库：3,200 步 Monte Carlo fragment assembly，每插一个片段就把刚性变换传播到下游重复 | 参数范围："the designs were required to have a twist (omega) between 0.6 and 1.0 radians, a radius of 0 to 13 Å and a rise between 0 and 10 Å"；native-like 过滤："The loops are required to be within 0.4 Å of a naturally occurring loop or rebuilt"、"Structures with helices above 0.14 Å appear bent and kinked and are discarded"、"And poorly packed structures in which fewer than four helices are in contact with each other are filtered"、"Designs with poor core packing as measured by Rosetta Holes < 0.5 are then filtered" | "We generated large sets of repeating-protein backbones that sampled a wide range of superhelical geometries"（正文未给具体条数；另用 "To speed this up, we used machine learning to filter designs that were most likely to fail" 替代最贵的 ab initio 验证） |
| A2 | 二肽/三肽单元 | 随机采 φ/ψ 后重复 4–6 次串成肽，再算其超螺旋参数 | 位阻门："If any pair of φ and ψ angles gets a high Rosetta Ramachandran score above the threshold of -0.5, it means that this pair of torsion angles is likely to introduce intra-peptide steric clashes" | "We then generated corresponding sets of repeating-peptide backbones by randomly sampling di-peptide and tri-peptide conformations (avoiding intra-peptide steric clashes), and then repeating these 4-6 times to generate 8-18-residue peptides" |
| A3 | A1 蛋白骨架 + A2 肽骨架 | 配对搜索超螺旋同相位 | "requiring the rise to be within 0.2 Å, the twist to be within 5° and the radius to differ by at least 4 Å"（并说明 "the difference in radius is necessary to avoid clashing between peptide and protein; the peptide can wrap either outside or inside the protein"） | 匹配的蛋白-肽骨架对（正文未给对数）；构象不限时"designs were generated with a wide range of peptide conformations"，含 β-strand、PPII、螺旋等（Extended Data Fig. 1a-c，本卡未取到） |
| A4 | 特权相互作用类型清单 | 建哈希表：PDB 取种子 → 刚性扰动 + 骨架二面角采样 → 只留低能叉齿氢键构型 → 反推侧链 rotamer 放置 → 哈希键入库 | 采样幅度："random rigid-body perturbations were applied to the backbone residues, with a random set of Euler angles drawn from a normal distribution with 0° as the mean and 60° as the standard deviation"；键维数："the geometry relationship of each set of residues keeping the intended interactions was subjected to an 8D hash function (6D rigid-body transformation plus two torsion angles), and represented with a 64-bit unsigned integer as the key of an entry in the hash table"，跨两个残基时用 "For Asn, Gln, Asp or Glu interacting with two residues on the backbone, a 10D hash table was applied for representing the geometry relationship" | "Hash tables were generated for Asn and Gln making bidentate interactions with the N-H and C=O groups on the backbone of a single residue or adjacent residues, for Asp or Glu making bidentate interactions with the N-H groups of two successive amino acids, and for side-chain-side-chain pi-pi and cation-pi interactions" |
| A5 | A3 的匹配对 + A4 的哈希表 | 同轴对齐后沿轴平移 / 绕轴旋转做 2D 网格搜索，逐残基对算哈希键查表，命中就把侧链身份与二面角装回所有等价位置 | 步长："we performed a grid search in these two degrees of freedom, sampling relative translations and rotations in increments of around 1 Å and 10°"；淘汰："docks for which the number of matches was less than a set threshold were discarded"（**匹配数阈值的数字原文未给**） | 可形成叉齿氢键阶梯的刚性 dock（正文未给保留数目） |
| A6 | 通过 A5 的 dock | 肽裁到与蛋白同重复数、两侧都按对称链接残基，Rosetta 三轮疏水/亲水 FastDesign 交替出序列 | 设计域："the interface neighbour distance is set as 9 Å as the whole designable range around the DHR-peptide binding interface, and 11 Å as the whole minimization range"；"Three rounds of full hydrophobic FastDesign" 之后 "followed by hydropathic FastDesign were carried out, with each hydrophobic or hydrophilic FastDesign repeating twice"；粗筛："In the produced complex, the peptide itself with an averaged score (three calculations were carried out) larger than 20.0 or a complex score larger than -10.0 were rejected directly"；约束："keeping the residues that were identified in the hash matching fixed, and enforcing sequence identity between repeats in both the peptide and the protein" | 首轮设计复合体全集（正文未给条数） |
| A7 | A6 的设计 | 两侧"sanity check"突变扫描（针对三肽重复单元） | 肽侧："for the peptide side, in the tripeptide repeat units, every two amino acids other than proline were scanned for a possible mutation to all twenty amino acids except cysteine"，接受条件 "the mutation was accepted if the delta DDG (DDG_after - DDG_before) was larger than 1.0"；蛋白侧对原为亲水而设计成疏水的残基用 -5.0 门，"For the designed hydropathic amino acids, a delta DDG of -2.0 was used as the threshold" | 进入首轮下单的候选池（正文未给条数） |
| A8 | 首轮暴露的特异性问题 → 第二轮协议 | 加四条硬约束后重新出设计 | ①"First, we required that each non-proline residue in the peptide make specific contacts with the protein, and that the pockets and grooves engaging side chains emanating from the two sides of the peptide were quite distinct"；②"and selected only designs for which the design target sequence made the most favourable interactions with the designed protein"；③"Third, we used computational alanine scanning to remove hydrophobic residues on the protein surface that did not contribute to binding specificity, to decrease non-specific binding"；④"Fourth, to assess the structural specificity of the designed peptide-binding interface, we performed Monte Carlo flexible backbone docking calculations, starting from large numbers of peptide conformations with superhelical parameters in the range of those of the proteins, and selected those designs with converged peptide backbones (root-mean-square deviation (RMSD) < 2.0 between the 20 lowest ddG designs) close to the design model (RMSD < 1.5)" | 第二轮 54 个蛋白-肽对（B2） |
| A9 | 全部待下单设计 | 下单前的统一计算门（含 MD） | "We selected for experimental characterization 43 designed complexes with near-ideal bidentate hydrogen bonds between protein and peptide" + Methods 里的具体数字："favourable protein-peptide interaction energies (DDG ≤ -35.0), interface shape complementarity (Iface_SCval ≥ 0.65), tolerable interface unsatisfied hydrogen bonds (Iface_HbondsUnsatBB ≤ 2, Iface_HbondsUnsatSC ≤ 4) and low peptide apo energies (ScoreRes_chainB ≤ 0.9)" + "and which consistently retained more than 80% of the interchain hydrogen bonds in 20-ns molecular dynamics trajectories" | 首轮 43 个复合物（对应取到 49 条基因，见 B1） |
| A10 | 二轮的选定复合物 | **正向对接检验结构特异性**：用设计序列重生成大量任意肽构象，对未改动的 DHR 重新对接 + FastRelax，画 DDG–骨架 RMSD 收敛图 | "For each designed complex, 10,000 arbitrary peptide conformations were generated as above, using the designed sequence"；"FastRelax"（图注给的范围是 "usually 10,000-50,000 trajectories"）；"peptide backbone RMSD < 2.0Å among the top 20 designs with the lowest DDG during forward docking" | 只有"收敛"的复合物进入实验（图注："Only the 'converged' complexes were selected for experimental characterization"） |

### B. 实验侧流程（每一步都在削分母）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | A9 选出的设计 | 基因合成（IDT 或 GenScript，按宿主密码子适应指数与可合成性反向翻译）→ Lemo21(DE3) 表达 → Ni-NTA →（首轮）TEV 去标签 + IMAC → SEC / FPLC | 可溶且单体才进结合实验："We obtained synthetic genes encoding the designed proteins with 6×His tags for purification and terminal biotinylation tags for fluorescent labelling, expressed the proteins in Escherichia coli and purified them by Ni-NTA chromatography" | "Out of 49, 30 were monomeric and soluble"；第二轮 "We tested 54 second-round designed protein-peptide pairs using the yeast flow cytometry assay described above"、"Forty-two of the designed proteins were solubly expressed in E. coli , and 16 bound their targets with considerably higher affinity and specificity than in the first round" |
| B2 | 设计蛋白 + 靶肽 | **酵母表面展示 + 流式**判"认不认"，同时用芯片全合成肽库判"认谁" | 正文未给分选阈值数字；肽库构造："we in parallel used large-scale array-based oligonucleotide synthesis to generate yeast display libraries encoding all two- and three-residue repeat peptides with eight repeat units each, and used fluorescence-activated cell sorting (FACS) followed by Sanger sequencing to identify the peptides recognized by each designed protein" | 首轮 "Many of the designs bound peptides with sequences similar to those targeted, but the affinity and specificity were both relatively low, with most of the successes for three-residue repeat units"（逐靶明细在未取到的 Extended Data Table 1a） |
| B3 | B2 命中的设计 | BLI：生物素化肽上样链霉亲和素传感芯片，twofold 系列稀释 | "Bio-layer interferometry characterization of binding to biotinylated target peptides immobilized on Octet sensor chips revealed K d values ranging from less than 500 pM (below the instrument level of detection) to around 40 nM"，动力学门 "five out of six had a dissociation half-life of at least 500 s, and for three of the six there was little dissociation after 2,000 s" | 六个代表设计（diverse superhelical parameters）进入全面表征 |
| B4 | 六个设计 | 单体/形状/热稳定性：SEC-MALS、SAXS 与设计模型比对、CD 升温 | "Circular dichroism studies showed that all six were largely helical and thermostable up to 95 °C"；SAXS 判据为实验曲线与模型计算曲线接近（正文未给拟合阈值） | 六个设计均"hyperstable"，可 4 °C 存放 30 天不失活（正文述及 "little decrease in binding was observed after storage of the proteins for 30 days at 4 °C"） |
| B5 | 若干设计的界面 | **界面饱和突变库（SSM）+ 展示分选 + 二代测序富集**，既找更好的突变也反读结合模式 | 覆盖范围："we ordered a SSM library covering the central span of 65 amino acids within the whole repeat protein, owing to the chip DNA size limitation"；肽浓度按初始结合力定："various concentrations of the target peptide, depending on the initial peptide-binding abilities, ranging from 1 nM to 1,000 nM"；富集值 = 结合群频率 / 表达群频率后取 log10 | "after the incorporation of one to three enriched substitutions, binding was observed by flow cytometry using only 10 pM biotinylated cognate peptide" |
| B6 | 四个复合物（3 首轮 + 1 二轮）+ 1 个游离设计 | X-ray 共晶 + 精修，与设计模型逐层叠合 | 判据是 Cα RMSD 分层（蛋白 / 界面+肽 / 全复合体）：例如 "matching the design model with near atomic accuracy (Cα RMSD for protein, protein-peptide interface and full complex: 1.70 Å, 2.00 Å and 1.64 Å, respectively; Fig. 4b and Extended Data Fig. 5b )"、"The lowest-energy docked structure was close to the crystal structure, with Cα RMSD values of 1.15 Å, 0.98 Å and 1.16 Å for the protein alone, the peptide plus interface and the entire complex, respectively" | "We obtained high-resolution co-crystal structures of three first-round designs (RPB_PEW3_R4-PAWx4, RPB_LRP2_R4-LRPx4, RPB_PLP3_R6-PLPx6) and one second-round design (RPB_PLP1_R6-PLPx6)"，另有 "The 2.15-Å crystal structure of the second-round design RPB_PLP1_R6-PLPx6"；逐结构侧链 RMSD 在未取到的 Extended Data Table 2a |
| B7 | PLPx6 / IRPx6 肽 + 对应 binder | U2OS 活细胞共表达（肽-GFP；binder 融合 mScarlet + 线粒体或过氧化物体定位序列），spinning disk 共聚焦看 GFP 是否被搬走 | 判据是定位而非亲和力：未表达 binder 时 GFP 弥散在胞质，共表达后 GFP 信号重定位；两对同时表达时"the absence of overlap between channels" | 两对系统在细胞内保持活性："Thus, the PLPx6-RPB_PLP2_R6 pair retains binding activity in cells" |
| B8 | 6 对设计 | 正交性矩阵：BLI 交叉结合，信号按同型复合物最大值归一 | 浓度区间判据："The PLPx6, LRPx6, PEWx6, IYPx6 and PKWx6 binders showed almost complete orthogonality in the concentration range from around 5 nM to 40 nM, with each design binding its cognate designed repeat peptide much more strongly than the other repeat peptides" | 五条近乎完全正交，一对例外："Some cross-talk was observed between the PRMx6 and LRPx6 binders, perhaps involving the arginine residue, which makes cation-pi interactions in both designs" |
| B9 | 4/6 重复两种版本 | 变重复数以测"模块化是否真的一一对应"（两种方向：改蛋白重复数、改肽重复数） | 判据为亲和力随重复数单调上升且特异性不降；正文未给 Kd 数字（在 Extended Data Fig. 4a/b） | "Six-repeat versions of RPB_LRP2_R6 and RPB_PEW2_R6 had a higher affinity for eight-repeat LRP and PEW peptides than did four-repeat versions, without any decrease in specificity"，"Similarly, six-repeat IYP and PLP peptides had a higher affinity for six-repeat versions of the cognate designed repeat proteins (RPB_IYP1_R6 and RPB_PLP1_R6) than did four-repeat versions" |

### C. 从"重复语法"外推到非重复序列与内源蛋白

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | 已建好的六个重复模块复合物 | 只改其中 1–2 个模块的蛋白口袋 + 对应肽单元，其余界面不动；肽骨架再经 Monte Carlo 重采样与刚体优化 | "We broke the symmetry in the designed repetitive binding interface by redesigning both protein and peptide in one or more repeats of six-repeat complexes; the rest of the interface was kept untouched to maintain the binding affinity"；取舍："Designs were selected for experimental characterization as described above, favouring those for which the new design had a lower binding energy for the new peptide than the original peptide" | RPB_hyb1_R6（PLP2PEP2PLP2）与 RPB_hyb2_R6（IYP3RYP3）："The redesigned protein, called RPB_hyb1_R6, bound the redesigned peptide considerably more tightly in Octet experiments, whereas the original design favoured the previous perfectly repeating sequence, resulting in nearly complete orthogonality" |
| C2 | 全蛋白组序列 | 用自写脚本找"能被本研究的三肽语法覆盖"的最长片段并落在无序区 | 语法集合是硬编码的："we developed Python code to search databases for sub-sequences that match permutations of the set of amino acid triplets for which we designed binders in this study"；选靶理由 "(1) this protein possesses the sequence (PLP)x4 within a large disordered domain, with downstream sequence (PEDPEQPPKPPF) within the reach of our binder design method; and (2) this protein is well studied, and-in particular-commercial, highly specific and validated antibodies exist against it" | 人 ZFC3H1（226-kDa，PAXT 复合物成员） residues 594-620，位于约 100 残基的无序区 |
| C3 | PLPx4 复合物 + ZFC3H1 靶段 | 肽侧固定 (PLP)x4、尾巴用带 Ramachandran 偏置的 MC 建模；蛋白侧延长四个重复模块并设计其界面 | 8 个设计全部表达后以 BLI 判结合；亲和力用荧光偏振定量 | "These eight designs were expressed, and seven were found to bind the extended target peptide by bio-layer interferometry"，最高两条 "The two highest-affinity designs-αZFC-high and αZFC-low-were found by fluorescence polarization to have K d values of less than 200 nM and around 1.2 µM, respectively"，作者注 "somewhat weaker than the synthetic constructs described above" |
| C4 | αZFC-high / αZFC-low | 三步递进验证：与 103 残基 GFP 融合片段共洗脱（SEC）→ HeLa 裂解液 His pull-down + Western → pull-down 产物 LC-MS/MS | 判据是"内源靶被特异拉下"，并用近尺寸/近表面的 αZFC-low 作阴性："αZFC-high specifically pulled down the endogenous ZFC3H1 from human cell extracts when assessed by western blot"、"αZFC-low hence provides a control for non-specific association"；质谱鉴定门 "setting a threshold of five peptides for correct identification" | 共洗脱成立："demonstrating that the binder can recognize the target peptide in the context of a larger protein"；复合物层面 "Mass spectrometry revealed that MTR4 was enriched in the αZFC-high pull-down, demonstrating that the binder can recognize the native PAXT complex in a physiological context"，另检出 Bioplex 互作表中的 BUB3、ZN207 等与若干 RNA 结合蛋白（全表在未取到的 Source Data） |

**这套流程最值得单独记住的骨架**：难点不在"能不能设计"，而在**把自由搜索改造成查表拼装**（A4→A5 把六维刚体问题压成"两个自由度 + 一张哈希表"），再用**三条不同性质的检验**分别守特异性（A8 的构象收敛、A9 的界面能量/形状互补/不饱和氢键、A10 的正向对接）与**一条守动态**（20 ns MD 的界面氢键保持率）。最后每一层漏斗的损失都被明确写出来：设计全集→43（首轮）→49 基因→30 可溶；54 对→42 可溶→16 结合→6 精细表征；ZFC3H1 8 设计→7 结合→2 定量→1 个能做内源 pull-down。


## 4. 关键数字台账（数值 · 含义 · 出处；全部可在第 9 节声明的底稿里搜到）

| 数值 | 含义 | 出处 |
|---|---|---|
| rise 差 <0.2 Å、twist 差 <5°、radius 差 ≥4 Å | 蛋白-肽超螺旋同相位匹配容差（radius 必须差开以免撞） | Results 起始段 Design approach（§2 难点一、§3 A3 引句） |
| twist 0.6–1.0 rad、radius 0–13 Å、rise 0–10 Å | DHR 骨架生成时要求的参数采样范围 | Methods: Generation of DHR scaffolds |
| 3,200 | 每个骨架的 Monte Carlo fragment assembly 步数 | Methods: Generation of DHR scaffolds |
| 环 0.4 Å / 螺旋 0.14 Å / Holes <0.5 / 至少 4 条螺旋接触 | 骨架 native-like 与包装过滤的四条门槛 | Methods: Generation of DHR scaffolds（§2 难点四引句） |
| 8D / 10D / 6D、64-bit 无符号整数 | 哈希键维度（刚体 6D + 两个二面角；跨两残基用 10D；pi-pi 与 cation-pi 只用 6D） | Methods: Modular peptide docking and hashing |
| 网格步长约 1 Å 与 10° | 同轴对接搜索的两个自由度采样密度 | Results Design approach（§3 A5 引句） |
| 界面可设计邻域 9 Å、最小化全域 11 Å | Rosetta 界面设计的作用半径 | Methods: Design of the peptide-binding interface |
| 肽平均能 >20.0 或复合物能 > -10.0 直接拒 | 设计产物的第一道能量淘汰 | Methods: Design of the peptide-binding interface |
| delta DDG > 1.0（肽侧）；-5.0（原亲水改疏水）；-2.0（疏水/亲水设计残基） | 二次 sanity check 突变扫描的三条接受门 | Methods: Design of the peptide-binding interface（§3 A7 引句） |
| DDG ≤ -35.0；Iface_SCval ≥ 0.65；Iface_HbondsUnsatBB ≤ 2；Iface_HbondsUnsatSC ≤ 4；ScoreRes_chainB ≤ 0.9 | 首轮下单的五条定量门（正文只写定性口径，数字在 Methods） | Methods: Design of the peptide-binding interface（§3 A9 引句） |
| 20 ns、界面氢键保持 >80% | MD 一致性过滤（本文唯一明确的 MD 用途） | Results: Experimental characterization 前段（§2 难点三、§3 A9） |
| 10,000（图注 10,000–50,000）、top 20、RMSD < 2.0 Å、RMSD < 1.5 Å | 正向对接的构象收敛门 | Methods: Forward docking + Extended Data Fig. 1d 图注（§3 A8/A10） |
| 10.9 Å（容差 0.5 Å）、螺旋 20 或 21 残基、环 3 残基 | 二轮为对齐 PPII 脯氨酸间距而设的 atom-pair 约束与拓扑 | Methods: Backbone generation of curved repeat-protein monomers in polyproline II conformation |
| Ramachandran 分数阈 -0.5 | 肽骨架构象是否引入链内位阻的判据 | Methods: Design of peptide binders（§3 A2 引句） |
| Euler 0°±60°、平移 0 Å±1 Å | 哈希表构建时的扰动采样强度 | Methods: Modular peptide docking and hashing（§3 A4 引句） |
| 二/三肽 × 4–6 次 → 8–18 残基 | 目标肽库的构造口径 | Results Design approach（§3 A2 引句） |
| 43 | 首轮送实验的复合物数 | Results: Experimental characterization（§3 A9） |
| 49 → 30 | 首轮取到基因数 → 单体可溶数 | Results: Experimental characterization（§2 难点三、§3 B1） |
| 54 → 42 → 16 | 二轮测对的蛋白数 → 可溶表达数 → 显著结合数 | Results: Experimental characterization（§3 B1） |
| 6 | 深入表征的设计数（diverse superhelical parameters） | Results: Experimental characterization（§3 B3–B9） |
| Kd < 500 pM（低于仪器检测限）～约 40 nM | 六个设计的 BLI 亲和力区间 | Results（§3 B3 引句） |
| 5/6 解离半衰期 ≥500 s；3/6 在 2,000 s 几乎不解离 | 结合动力学（慢解离）水平 | Results（§3 B3 引句） |
| 95 °C；4 °C 30 天 | CD 热稳定性与存放后活性保持 | Results + Fig. 2d 描述（§3 B4） |
| 10 pM | SSM 富集 1–3 个突变后流式检出所用生物素化肽浓度 | Results（§3 B5） |
| 65 aa（约 1.5 个重复单元、跨三条螺旋）；肽浓度 1–1,000 nM | SSM 库覆盖范围与分选浓度档 | Methods: Preparation of SSM libraries（§3 B5） |
| 3 个首轮共晶 + 1 个二轮共晶 + 1 个游离设计 | 结构验证样本量 | Results: High-resolution structural validation（§3 B6） |
| 1.70 / 2.00 / 1.64 Å | RPB_PLP3_R6-PLPx6：蛋白 / 界面+肽 / 全复合体 Cα RMSD | Results（§3 B6 引句） |
| 2.08 Å / 2.12 Å | RPB_PEW3_R4-PAWx4：蛋白 RMSD / 肽与界面 RMSD | Results（§3 B6 附近原句） |
| 1.15 / 0.98 / 1.16 Å | RPB_LRP2_R4-LRPx4：蛋白 / 肽+界面 / 全复合体 Cα RMSD | Results（§3 B6 引句） |
| 2.15 Å（分辨率）；界面 1.11 Å、复合体 1.91 Å | RPB_PLP1_R6-PLPx6（二轮设计）的晶体分辨率与 RMSD | Results（§3 B6） |
| 5–40 nM | 正交性成立所需的浓度区间 | Results（§2 难点八、§3 B8） |
| ZFC3H1 226 kDa；残基 594-620；约 100 残基无序区；103 aa 片段 | 内源靶的尺度与所用构建体 | Results: Generalization to native disordered regions + Methods（§3 C2） |
| 8 → 7 | ZFC3H1 延长设计表达数 → BLI 结合数 | Results（§3 C3 引句） |
| <200 nM（αZFC-high）与约 1.2 µM（αZFC-low） | 对 ZFC3H1 延长肽的荧光偏振 Kd | Results（§3 C3 引句） |
| 约 100 nM | 作者在结论中自评的内源 binder 亲和力水平 | Conclusion（§8 迁移判断相关） |
| 5 条肽段 | 质谱鉴定"正确识别"的阈（图注口径） | Fig. 6f 图注（§3 C4 引句） |
| 6×His、TEV、NdeI/XhoI、Lemo21(DE3)、37 °C 6–8 h 后 18 °C 约 14 h | 构建与表达条件（可复现口径） | Methods: Synthetic gene constructs / Protein expression and purification |

正文未给的东西（本卡不编）：骨架库与匹配对的**条数**、网格搜索通过 dock 的**保留数**、哈希匹配数阈值的具体数字、逐靶命中率分母（只在 Extended Data Table 1a/1b）、ML 过滤器的训练集与假阴率、MD 的软件/力场/重复次数、混合设计（hyb1/hyb2）的 Kd。

## 5. 结论——作者说了什么

1. 用超螺旋参数匹配 + 几何哈希，能为"骨架呈 PPII 的重复三肽"从头设计出模块化的螺旋重复蛋白结合剂："Our results show that by matching superhelical parameters between repeating-protein and repeating-peptide conformations, and incorporating specific hydrogen-bonding and hydrophobic interactions between matched protein and peptide repeats, we can now design modular proteins that bind to extended peptides with high affinity and specificity"。
2. 亲和力达到 pM–nM，并且在活细胞里有效（摘要口径）："The proteins are hyperstable and bind to four to six tandem repeats of their tripeptide targets with nanomolar to picomolar affinities in vitro and in living cells"。
3. 结构层面按设计实现，包括从蛋白侧链到肽骨架的氢键梯："Crystal structures reveal repeating interactions between protein and peptide interactions as designed, including ladders of hydrogen bonds from protein side chains to peptide backbones"，"All interacting side chains from both the protein side and the peptide side in the computational design model are nearly perfectly recapitulated in the crystal structure"。
4. 改个别模块就能把识别范围推到非重复序列与天然无序区："By redesigning the binding interfaces of individual repeat units, specificity can be achieved for non-repeating peptide sequences and for disordered regions of native proteins"，"The strategy should be generalizable to a wide range of repeating-peptide structures, and the ability to break symmetry by redesigning individual repeat units opens the door to more general peptide recognition"。
5. 相对天然支架路线的优势声明："an advantage of our method is that a much broader range of protein conformations and binding-site geometries can be generated by de novo protein design than by starting with a native protein backbone"。
6. 内源靶的可用性判断："The affinity of around 100 nM that we attained for this endogenous binder is compatible with other cellular applications"，并主动交代成像类应用要权衡："in which a trade-off must always be found between high-affinity interactions for labelling specificity and low-affinity interactions to avoid perturbing protein function"。
7. 展望的下一步是把模块刚性拼接，做出对完全不重复序列的识别："rigid fusion of protein modules designed to recognize different di-, tri- and tetrapeptide sequences, using the approach described here, provides an avenue to achieving sequence-specific recognition of entirely non-repeating sequences"。

## 6. 结论——我们读出了什么（以下为推断，不是作者原文）

1. **这篇的真正贡献是"把不可搜索的问题变成查表问题"，不是"做出了高亲和力结合剂"**。几何哈希把六维刚体自由度先约成"只有平移 + 旋转两个自由度"，再用一张预计算表替代优化 —— 这种"把特权相互作用穷举成表"的做法，与我们做催化几何筛查时该用的东西同构：把"供体-金属-尿嘧啶"这类必须成立的空间关系穷举成几何门，而不是让对接器自由找。
2. **它的漏斗是分层的，每层用一种不同性质的判据**：静态能量（DDG/形状互补）→ 构象分布（正向对接的 RMSD 收敛）→ 动态（20 ns 界面氢键保持率）→ 实验（可溶单体、酵母结合、BLI）。只有第一层的候选池最大、后两层各削一刀。→ 对我们：单一判据（比如 Foldseek 命中或 pLDDT）不该同时决定召回和排序；至少要有"分布层"（对扰动稳健）和"动态层"（对时间稳健）各一票。
3. **"提高特异性"靠的是加约束而不是换打分函数**（第二轮四条约束，见 §2 难点三）。作者没有调 Rosetta 权重，而是加了"两侧口袋必须明显不同""非脯氨酸都要有特异接触""去掉不贡献特异性的疏水面""重采构象看收敛"。→ 对我们：漏斗里的规则型约束（可解释、可否证）比再堆一个 ML 分数更值得先做。
4. **MD 在这篇里是"一致性校验器"，不是"机理揭示器"**：唯一的用途是看界面氢键会不会在 20 ns 内掉下 20%，而且没有软件/力场/重复次数写进正文。→ 这条支持我们把 MD 预算限定在"短时程稳健性一票"，而不是长时反应采样；但也说明**这篇不能为"MD 能判催化"提供任何证据**。
5. **内源靶的成功是"语法倒推"的成功**：先有六个三肽语法，再去蛋白组里找能被语法覆盖的无序片段（§3 C2）。所以"能靶向 IDR"这句话的真实强度是"能靶向 IDR 里恰好像合成肽的那一段"。作者自己在结论把水平定在约 100 nM，比合成体系的 pM 低两个数量级 —— 这条落差是本文最诚实的数字。
6. **"模块化"带来的最可复用的工程属性是亲和力可用重复数调**（B9），以及模块可拆换（C1）。这两条对"设计可组合的试剂"有价值，但对"设计能催化的酶"没有直接对应物 —— 催化位点不是重复单元，不能靠增加拷贝数线性增效。


## 7. 局限与失败（作者的 + 我们读出的）

**作者写出来的**
- 适用面被几何锁死：整条路线建立在"目标肽本身有重复单元并且呈 PPII 类超螺旋"上，非重复序列要靠"改模块"这种有限手段外推（§2 难点六、七），任意序列仍未拿下。
- 天然重复支架路线的对照事实：TPR 类能认更多序列与构象，但代价是 µM 级亲和力与配准漂移 —— "Tetratricopeptide-repeat proteins bind to peptides with a variety of sequences and conformations with lower (micromolar) affinity"；本文的设计换来高亲和力，同时把适用范围换窄。
- 内源靶的绝对水平只有约 100 nM（结论自陈），且作者承认成像应用要"高亲和保特异 vs 低亲和不扰动功能"的权衡。
- 交叉反应有例外未解释清楚：PRMx6/LRPx6 的 crosstalk 只给了 "perhaps involving the arginine residue" 的假设。
- 表达损耗是真实瓶颈：作者明写首轮 "Out of 49, 30 were monomeric and soluble"（49−30=19 的差额是本卡算术，不是原文措辞），二轮 54 条里 "Forty-two of the designed proteins were solubly expressed in E. coli , and 16 bound their targets with considerably higher affinity and specificity than in the first round"。设计成功 ≠ 能拿到蛋白。

**我们读出的**
- **下单前的定量门只写在 Methods，正文只写定性口径**（正文那段是 "We selected for experimental characterization 43 designed complexes with near-ideal bidentate hydrogen bonds between protein and peptide"，后面三项（界面相互作用能、形状互补、不饱和氢键）在正文里被参考文献编号打断，没有数字）。若只读正文，会以为筛选是主观挑选；真正的门是 Methods 里的 DDG ≤ -35.0 这类数（见 §3 A9）—— 而这些数**没有一个是经过留出验证的**（全文没有"把阈值换成别的值会怎样"的敏感性分析）。
- **阈值是"凑够一池可下单候选"定的，不是"预测力"定的**。正文只给漏斗的通过数（43、54），从不给"某个阈值单独能把阳性和阴性分多远"的 ROC 类证据，因此这些阈值的判别力无法从本文评估。
- **MD 这一票缺方法学细节**（软件、力场、温度、重复次数、>80% 的氢键定义方式都没进正文/Methods 可读部分），却承担"下单前过滤"的角色，是整条漏斗里最难复现的一环。
- **结构验证的样本量很小**：只有 4 个共晶 + 1 个游离结构，且这 5 个都是从通过全部计算门和实验门的成功者里挑的 —— 没有对失败设计做结构解析，所以"设计准"这个结论有幸存者偏差（与 B09 那条"生成阶段用过的指标不能当筛子"是同型问题）。
- **没有动力学以外的定量正交性**（热图按最大信号归一），也没有胞内亲和力；活细胞部分只到"能重定位"的层级。
- 全文没有 QM、没有结合自由能分解、没有催化相关任何内容 —— 它是一篇纯"结合界面"的工作。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"特权相互作用穷举成哈希表"的思路**（§3 A4/A5）：把"必须成立的少数空间关系"离线枚举（我们这里是：金属位 Asp/Glu/His 排布、尿嘧啶识别双供体氢键几何、Pfam 结构域内的催化残基对距离），线上只做查表与两个自由度的粗对齐。**用法是召回 + 排序的一票，不是终点判据**。
2. **分层漏斗的"三性质"划分**（§6.2）：静态能量层 / 构象分布层 / 短时动态层各设一票，并明确每一层的输入输出规模。→ 直接对齐 DP2R 标准的门表：每一门要能回答"这一削削掉多少、留下多少"。
3. **构象收敛检验（forward docking）值得移植**：不是问"最优姿态好不好"，而是问"从 10,000 个随机起点出发，是否收敛到同一处且能量占优"。→ 我们可做同类：对同一候选，用多个不同结构/序列起点（Foldseek 与 HMM 与 blastp 三通道）各自打分，看**跨通道一致性**而不是单通道最高分。本文的数字（top 20 内 RMSD < 2.0 Å、对设计模型 RMSD < 1.5 Å）是它自己体系的判据，**不许当我们的阈值**；要移植的是"要求收敛、不收敛就丢"这个动作。
4. **语法倒推靶段的组织方式**（§3 C2）：先声明"我目前只会做哪几类语法"，再用代码在蛋白组里枚举符合语法且落在目标结构情境（对我们=结构域内且有底物结合迹象）的片段，作为**可行动清单**；这比"随机挑天然酶试"更省预算。
5. **失败/成功都要留分母**：本文把 49→30、54→42→16 都写了出来，这是可复现漏斗的最低要求，也是我们报告里每轮必须印的三行（判定标准/判定结果/找出来没有）里"结果"那一行的形态。

**不可迁移（为什么不能照搬）**

1. **本文全部判据是"结合"判据**（界面能量、形状互补、不饱和氢键、解离半衰期）。UAA 合成酶的成败取决于**三步化学事件与竞争副产物**，一个静态界面的 pM 亲和力既不必要也不充分。**不许**把 DDG ≤ -35.0、Iface_SCval ≥ 0.65、Kd < 500 pM、解离 t½ ≥ 500 s 这类数字当作酶活闸口或"成功概率"引用。
2. **它的 MD 是 20 ns 的界面氢键保持检验，不是反应采样**：不能用来支持"MD 能判 UAA 成键"这类主张，也不能引用"MD 过滤后命中率提升"（本文没有这种数字）。
3. **通量结构完全不同**：本文靠合成基因批量下单（43、54 一组），末端用展示/BLI 快速过筛；我们的末端是 LC-MS/MS 产物身份确认，一轮最多几个构建体。因此本文"漏斗削到 6 个精细表征"的策略对我们不可复制，我们只能把削枝放在**计算侧 + 机制多样性 + 失活对照**。
4. **它的靶是"预先设计好的重复肽语法"**，等于问题里有 ground truth 结构；UAA 的目标酶在天然序列空间里**没有已验证阳性锚**（本文的晶体/SAXS 验证之所以成立，是因为设计与实验对象一一对应）。所以本文的"设计—晶体几乎重合"不能换算成我们对天然候选的任何置信度。
5. **不引入它的"改模块保亲和力"数字**：RPB_hyb1/hyb2 的 Octet 只给归一化热图，连 Kd 都没有，不足以支撑任何"改造效率"估计。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/B33_PMC10115654_text.txt

- 本地纯文本：`fulltext/B33_PMC10115654_text.txt`（NCBI efetch 兜底通路 → `fulltext/B33_PMC10115654_fullTextXML.xml` 去标签、HTML 实体解码、空白折叠，未改写内容）。同一篇论文若有 Europe PMC 抽取版本，句内裸引用的数字编号位置会不同，因此**本卡只声明并对齐这一份**。
- 对照底稿：`sources/baker.md:431-441`（原卡为摘要级，明写未逐段核对方法细节与命中率）。本卡的 §2、§3、§4 全部改从全文 Methods / Results / 图注取数，未从原卡继承任何数字。
- 未取到、因此本卡不写细节的材料：Extended Data Table 1a/1b（逐靶命中数）、Extended Data Table 2a/2b（晶体学与 SEC-MALS 统计）、Extended Data Fig. 1–7、Supplementary Table 1/2、Source Data 蛋白组全表、Fig 原图数值。凡涉及处本卡均写"在未取到的扩展数据里"或"正文未给阈值"。
- CSV 字段映射：§3 ↔ `候选生成方法/计算筛选判据/阈值数字`；§4 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计`；§2 与 §7 ↔ `在方法演进链的位置`；§8 只作本项目的迁移判断，不写回 CSV。
- **本卡自检**：`scripts/verify_literature_cards.py --only "B33" --no-report`（输入：本目录 `*.md` + `fulltext/` + `sources_map.json`；行为：把卡内所有不含中日韩字符、被直双引号包住、≥20 字符且 ≥12 个字母的片段，在 §9 声明的底稿里逐字查找，任一不命中即 FAIL）。写作过程中用同一套逐字逻辑先抓出并改掉三处：① 一处把跨参考文献编号的两句连成一句（原文 FastDesign 之后插了引文编号 21），已拆成 "Three rounds of full hydrophobic FastDesign" 与 "followed by hydropathic FastDesign were carried out, with each hydrophobic or hydrophilic FastDesign repeating twice" 两条；② 一处在引句里用省略号代替被引文编号打断的半句，已改成两条独立引句；③ 一处把句首 On the peptide side 误写成小写开头（逐字比对区分大小写），已还原。本轮门禁结果见回报。

<!--CSV回填
work_type=论文
target=呈多聚脯氨酸II构象的二/三肽重复序列（LRP、PEW、PLP、IYP、PKW、IRP、LRT、LRN、LRQ、RRN、PSR、PRQ 等三肽单元）；外推到非重复混合肽（PLP2PEP2PLP2、IYP3RYP3）与内源无序区（人 ZFC3H1 残基 594-620，PAXT 复合物）
backbone_generation=从头设计螺旋重复蛋白（DHR，helix-loop-helix-loop 重复 4 次以上）：Rosetta fragment assembly guided by RPX motifs，3,200 步 Monte Carlo；序列用 RepeatProteinRelax 对称模式 + structure profile 偏向天然蛋白；肽骨架由随机 phi/psi 采样的二/三肽重复 4-6 次构成（8-18 残基）；另有一类以 10.9 Å atom-pair 约束生成的曲线 PPII 单体
computational_filters=超螺旋参数匹配（rise/twist/radius）；bidentate 氢键几何哈希（8D/10D/6D 键，64-bit 整数）；同轴 2D 网格搜索；Rosetta 组合优化（beta_nov16，三轮 hydrophobic/hydropathic FastDesign）；界面 DDG 与突变扫描（delta DDG）；计算丙氨酸扫描；柔性骨架正向对接构象收敛（RMSD 门）；20-ns MD 界面氢键保持率；native-like 骨架过滤（loop 0.4 Å、helix 0.14 Å、Rosetta Holes、螺旋接触数）；ML 过滤器替代昂贵的 Rosetta ab initio 验证
thresholds=匹配容差 rise<0.2 Å、twist<5°、radius 差>=4 Å；DHR 采样范围 twist 0.6-1.0 rad、radius 0-13 Å、rise 0-10 Å；网格步长约 1 Å 与 10°；Ramachandran 分数阈 -0.5；atom-pair 10.9 Å 容差 0.5 Å；设计域 9 Å / 最小化域 11 Å；肽平均能>20.0 或复合物能>-10.0 拒；delta DDG 肽侧>1.0、蛋白侧 -5.0 与 -2.0；下单门 DDG<=-35.0、Iface_SCval>=0.65、Iface_HbondsUnsatBB<=2、Iface_HbondsUnsatSC<=4、ScoreRes_chainB<=0.9；MD 界面氢键保持>80%（20 ns）；正向对接 10,000（图注 10,000-50,000）构象、top20 内 RMSD<2.0 Å、对模型 RMSD<1.5 Å；质谱鉴定阈 5 条肽段
md_used=是（仅作下单前的结构一致性过滤：20-ns 轨迹里检查链间氢键是否保持 80% 以上；不做机理、不做反应坐标、正文未给软件/力场/重复次数）
qm_used=否
experimental_methods=基因合成（IDT/GenScript）→ Lemo21(DE3) 表达 + Ni-NTA（首轮 TEV 去标签 + IMAC）→ SEC/FPLC 与 SEC-MALS → 酵母表面展示 + 流式细胞术（含芯片合成的全部二/三肽重复单元展示库 + FACS + Sanger）→ 界面饱和突变库（SSM，65 aa 跨度，Illumina 富集分析）→ BLI（Octet RED96，生物素化肽，twofold 稀释）→ 荧光偏振（ZFC3H1 体系 Kd）→ CD 热稳定性 → X-ray 共晶结构（4 个复合物 + 1 个游离）→ U2OS 活细胞成像（GFP/mScarlet 重定位至线粒体/过氧化物体，双通道正交）→ HeLa 裂解液 His pull-down + Western + LC-MS/MS 蛋白组
pipeline_counts=骨架库与匹配对条数正文未给；首轮 43 个复合物下单 → 49 条基因 → 30 个单体可溶；第二轮 54 个蛋白-肽对 → 42 个可溶表达 → 16 个显著结合 → 6 个精细表征；结构验证 3 个首轮 + 1 个二轮共晶 + 1 个游离；ZFC3H1 延长设计 8 个表达 → 7 个 BLI 结合 → 2 个定量 Kd → 1 个用于内源 pull-down；正向对接 10,000-50,000 条轨迹/复合物
hit_rate=正文未给统一命中率分母（逐靶命中数在 Extended Data Table 1a/1b，本卡未取到）；可核对的是二轮相对一轮的定性提升（16/54 有更强结合）与首轮 30/49 可溶；内源靶亲和力较合成体系低约两个数量级（<200 nM/约 1.2 µM vs 最低 <500 pM）
best_metric=Kd 低于 500 pM（BLI，原文注明低于仪器检测限），5/6 设计解离半衰期 >=500 s、3/6 在 2,000 s 几乎不解离；内源 ZFC3H1 体系最佳约 100 nM 级（结论自述）；结构精度最佳界面 Cα RMSD 0.98-1.11 Å、复合体 1.16-1.91 Å
cost_or_stat_note=骨架验证阶段 Rosetta ab initio 需数天/数百 CPU（因此改用 ML 过滤器替代，正文未给该过滤器成本与假阴率）；基因合成 49 条（首轮）与 54 对（二轮）；SSM 库受芯片 DNA 长度限制只覆盖 65 aa；X-ray 共晶 4 个（分辨率之一为 2.15 Å）；蛋白组学只有 pull-down 一次实验的定性输出
role_in_timeline=Baker 组 de novo 结合蛋白主线从"靶是球蛋白表面"（Cao 2022 / Bennett 2023 的 AF2 闸口路线）扩展到"靶是短肽与内在无序区"；把界面设计从自由搜索改为几何哈希查表 + 超螺旋同相位匹配，并引入可拆卸的重复模块语法（模块=三肽单元）；其"改个别模块打破对称"是后续把重复语法外推到非重复序列的接口；本文的漏斗判据全部是结合类判据，未涉及催化
source_pointer=data/literature_cards/fulltext/B33_PMC10115654_text.txt（NCBI efetch，110 KB 单行纯文本）+ 同目录 B33_PMC10115654_fullTextXML.xml；对照底稿 sources/baker.md:431-441；Nature 2023, 616:581-589, DOI 10.1038/s41586-023-05909-9, PMID 37020023, PMCID PMC10115654
CSV回填-->

