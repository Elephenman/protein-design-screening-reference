# [B12] 把 binder 漏斗改造成"多闸口 + 反推阈值"的工程——螺旋肽与柔性靶的首次通吃

Vázquez Torres S, Leung P J Y, Venkatesh P, Lutz I D, … Watson J L, Rogers J M, Baker D（华盛顿大学 IPD + 哥本哈根大学）
Nature 2024, 626:435-442 · DOI 10.1038/s41586-023-06953-1 · PMID 38109936 · PMCID PMC10849960
开放获取（CC BY 4.0）· 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10849960/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B12**（组：Baker组；标题 De novo design of high-affinity binders of bioactive helical peptides） |
| 本文取回方式 | 2026-10-16 本地抓取（先行调研缓存通路） |
| 本地全文①（本次唯一登记全文） | `data/interim/baker_lit/ft/helicalpeptide2024.txt`（74,815 B，Europe PMC fullTextXML 去标签纯文本） |
| 登记底稿 | `sources/baker.md` 第 160–170 行（原卡） |
| 证据级别 | **全文级**（本卡所有英文引句均在该本地纯文本里逐字命中；见第 9 节门禁自检） |
| 年份口径 | 刊期年 **2024**（Nature 2024, 626:435-442）；Crossref 的在线年标是 2023，两种写法都写在本行『期刊或预印本』列。2026-11-07 把 CSV 的『年份』列统一为刊期年 2024（改动账 `data/interim/table_field_fixes_2026-11-07.json`） |
| 未取到的部分 | Supplementary Methods/Tables 1–9/Figs 1–12、Extended Data 原图数值、FP/ITC 原始曲线。凡涉这些处本卡明写"正文未给出" |
| 文本细节 | 抓取文本里 `&lt;`/`&gt;` 为未解码实体；本卡涉及阈值的引句按归一化后的 `<`/`>` 书写（门禁两侧同用 `scripts/litcards_text.py` 的 `norm()`，故命中）；`RF joint`、`K d` 等是标签剥离后的写法，本卡照录 |

## 1. 这篇到底解决什么（大白话）

肽类激素（PTH、胰高血糖素 GCG、NPY、PYY、促凋亡 BH3 域 Bid/Bim）在**自由状态下基本是无规线团，只有结合受体时才折成一段 α 螺旋**。现有设计工具是为"结合一个刚性、有凹槽的蛋白表面"造的，对这种"又短、又软、还要靠结合才成形"的靶几乎无效；而抗体的 CDR 环本身又不擅长抓螺旋（作者指出几乎所有抗肽抗体抓的是非螺旋构象）。这篇做的是**四代方法排在同一条流水线上当接力**：① Rosetta 参数化生成"三螺旋沟槽 + 两根支撑螺旋"的脚手架库（人设计的几何）；② RoseTTAFold Inpainting（RF joint）+ ProteinMPNN 把界面**撑大**、序列**重出**；③ 把肽"穿线"到已有的螺旋结合脚手架上重设计；④ AF2 Hallucination 在**序列空间**做 Monte Carlo，完全不定几何地从零长出结合体；⑤ 最后用 **RFdiffusion**（含本文成型的 **partial diffusion**）既做局部优化也做全新生成。结果：PTH、Bim 拿到 KD < 500 pM，且**"without any subsequent experimental optimization"**，并顺带把结合体做成生物传感器（lucCagePTH）与 LC-MS/MS 富集试剂，证明**设计蛋白可以替换抗体当亲和试剂**。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **螺旋肽靶有两条独立的物理难点，作者把它明确拆开写**。
   - 形状不匹配：**"have shapes suitable for binding rigid concave targets, but not for cradling extended peptides"**（上一代 pM 级 50–65 残基 minibinder 的形状是为凹面靶做的）；用卷曲螺旋绕过去也不行——**"coiled-coil subunits generally self-associate in the absence of binding partners owing to considerable exposed hydrophobic surface, considerably reducing the effective target-binding affinity"**。
   - 熵代价：**"peptides have fewer residues to interact with, and are often partially or entirely unstructured in isolation"** → **"there can be an entropic cost of structuring the peptide into a specific conformation"** → **"which compromises the favourable free energy of association"**。
   → **他们做了什么**：针对第一条改**几何**（三螺旋沟槽 + 支撑螺旋屏蔽疏水面，"the helices flanking the groove could limit self-association of the recessed hydrophobic surfaces"）；针对第二条改**采样策略**（不预设构象，让模型自己在序列空间或扩散里找结合态，"Hallucination using AF2 or RoseTTAFold has the advantage that neither the binder nor the peptide structure needs to be specified during the design process, enabling the design of binders to peptides in different conformations"）。
2. **参数化沟槽库能结合，但亲和力只有 µM，作者承认必须换方法**：实测 **"Many of the designs bound their targets (3, 4 and 8 out of 12 to PTH, GCG and NPY, respectively) but with only micromolar affinities"**，并据此判断 **"These results suggest that groove-shaped scaffolds can be designed to bind helical peptides, but also that design method improvement was necessary to achieve high-affinity binding"**。→ **他们做了什么**：不换靶、不弃题，而是**上第二道工具**（RF joint Inpainting 扩界面 + ProteinMPNN 重出序列），把起点 PTH 结合体推进约三个数量级：**"the affinity of the starting PTH binder was improved by approximately three orders of magnitude, and the computational model of the highest-affinity binder had 19% greater surface area contacting the target peptide"**。
3. **并且他们做了归因实验，发现收益不来自序列、而来自界面几何**（本文最有迁移价值的一条自证）：**"the structural extension was critical to the improvement in binding affinity"** 与 **"sequence redesign with ProteinMPNN of the original binding interface did not measurably increase affinity"**。→ **他们做了什么**：把"扩界面"与"重出序列"拆开各跑一遍，用差分实验定因，而不是笼统归功于新模型。→ **代价**：这个结论只在 PTH 一条起点上给出，其他靶没有等价的消融。
4. **Hallucination 会造出"能过打分但做不出来"的对抗序列**（作者直接引前作教训）：**"Previous work has demonstrated that AF2 Hallucination yields adversarial sequences that do not work experimentally"**。→ **他们做了什么**：**换序列来源**，把 Hallucination 只当结构发生器，序列交给 ProteinMPNN：**"However, designs can be rescued with ProteinMPNN redesign of the sequences"**，并解释**"the output binder structure was subsequently redesigned with ProteinMPNN"**。风险也被事前写明：**"Hallucination directly optimizes metrics correlated with binding, albeit with the possible hazard of generating adversarial protein sequences"**。
5. **传统方法要"围绕起点结构提高活性"几乎不可做**（这是他们引入 partial diffusion 的动机）：**"A long-standing challenge in protein design is to increase the activity of an input native protein or designed protein by exploring the space of plausible closely related conformations for those with predicted higher activity"**，而 **"This is difficult for traditional design methods as extensive full-atom calculations are needed for each sample around a starting structure"**，并且 **"it is not straightforward to optimize for higher binding affinity without detailed modelling of the binder-target side-chain interactions"**。→ **他们做了什么**：用扩散模型的"半程性质"绕开全原子计算——**"We reasoned that, by contrast, RFdiffusion might be able to rapidly generate plausible backbones in the vicinity of a target structure, increasing the extent and quality of interaction with the target guided by the extensive knowledge of protein structure inherent in RoseTTAFold"**，做法是只加噪到指定步（例如 70/40 步）再去噪（**"We therefore reasoned that ensembles of structure with varying extents of deviation from an input structure could be generated by partially noising initial starting structures to different extents"**）。
6. **柔性靶（无序两端、没有可用结构）时，固定靶结构那套失效**。→ **他们做了什么**：**改模型本身**——重训 RFdiffusion，"只给序列、不给结构"也能围绕它生成结合体（**"We next sought to generalize RFdiffusion to enable binding to flexible targets from a specification of the target sequence alone"**、**"We fine-tuned RFdiffusion by training on two chain systems from the Protein Data Bank"**）。→ **代价（作者自己承认）**：这条路掉亲和力——**"Note that here we explored using shorter binder chain lengths in these calculations, resulting in smaller designs, which probably accounts for the lower affinity than in the fixed structure case above"**，且 **"Lower affinity binders were also obtained for PTH and GCG using this flexible backbone RFdiffusion approach"**（PYY 得 24.5 nM，PTH/GCG 只到 µM 段）。
7. **阈值不是物理量，是"削到可下单规模"的工具**：Methods 明写 **"Precise metrics cutoffs changed for each design campaign to get to an orderable set,"**，并对每条支路给出目标池规模：**"The precise values used for filtering were chosen to reduce the set down to 46 designs"**（Hallucination 支路）与 **"The precise values used for filtering were chosen to reduce the set down to 96 designs for each target"**（扩散支路）。→ **他们做了什么**：先定"能测多少个"，再反推阈值，而不是先定阈值再看剩多少。
8. **GCG 在真实血清里富集效率不行**。→ **他们做了什么**：把结论降级并交代下一步——**"further increases in specificity of this design will probably be necessary for actual applications"**（缓冲液里回收率 91.1%，提取物里低）。→ **代价**：这一支没有做到应用级，只在缓冲液与加标血浆（PTH 53%/43%）上成立。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **参数化生成（人给几何）**：Crick 螺旋束参数化采样"三螺旋沟槽 + 两支撑螺旋"，Rosetta ConnectChainsMover 连环，Rosetta 设计+过滤。
- **界面/序列改造**：**RF joint（RoseTTAFold Inpainting，可联合设计序列与结构）** 扩界面；**ProteinMPNN** 重出序列。
- **穿线法（threading）**：把目标肽序列穿到已知的螺旋结合脚手架上，按界面疏水接触过滤，再 ProteinMPNN + AF2 with initial guess 复算。
- **序列空间优化**：AF2 Hallucination（改自 [B09] 与 Wicky 2022 的代码，model_4_ptm），自定义 loss 组合 + Metropolis 模拟退火。
- **扩散（本文的主引擎）**：**RFdiffusion** 常规复合物生成 + **partial diffusion**（只加噪到指定步再去噪）做局部优化 + **重训版 RFdiffusion**（target 只给序列）做柔性靶。辅助势：最小化复合物回转半径。
- **读出**：NanoBiT 分裂荧光素酶（初筛）→ 酵母表面展示 → FP（荧光偏振定量 KD）→ ITC/CD/SEC → X 射线晶体学 → 嫁进 lucCage 做生物传感器 → 偶联磁珠做 LC-MS/MS 富集。
- **没有用的方法**：MD、QM。全文只把 MD 作为"传统方法为什么贵"的背景提了一次（**"This is difficult for traditional design methods as extensive full-atom calculations are needed for each sample around a starting structure"**），并未用其筛选。

### A. 四代工具的接力（Fig 1，参数化 → Inpainting → 穿线 → Hallucination）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | Crick 参数化几何 | 采**三螺旋沟槽 + 两支撑螺旋**：**"each parametric helix was 15-19 residues long"**；超螺旋度从**偏向高超螺旋**的分布采样 | **"A supercoiling value was randomly selected from a biased distribution favouring more supercoiled scaffolds, given that these scaffolds were more likely to fail in the subsequent looping step"**（因为易失败，所以过采样）；**"This biased sampling strategy was chosen to achieve a more uniform distribution of supercoiling within the final scaffold library, with sufficient numbers of highly supercoiled bundles"** | **"This process was used to sample a set of 200,000 arrangements of 5 helices"** → **"was used to loop this set into approximately 135,000 successful scaffold backbones"** → **"to yield a final library of 18,000 scaffolds"** |
| A2 | 18,000 沟槽库 | 用改造过的 minibinder 界面设计流程对接 PTH/GCG/NPY：**"in which only the binder interface was designed and the target was restricted to only rotamer repacking"** | 无（初筛） | 每靶 **"and screened 12 designs for each target using a NanoBiT split-luciferase binding assay"** → 结合 3/4/8 条，但**"but with only micromolar affinities"** |
| A3 | 最紧的 parametric PTH 结合体 | **RF joint Inpainting** 扩界面 + ProteinMPNN 重出序列：**"We used RF joint Inpainting to extend the binder interfaces and ProteinMPNN to redesign the sequences, reasoning that the combination of these two methods could lead to more favourable interactions with the peptide"** | AF2 with initial guess 验证与过滤（正文未给该支路数值阈值） | 实测 192 条：**"Out of 192 designs tested, 44 showed binding against PTH in initial yeast display screening"** → SEC 后最优 **"the best binder was found to bind with 6.04 nM affinity to PTH using fluorescence polarization (FP)"**；特异性对照 PTHrp（**"a related peptide sequence with 34% sequence identity"**） |
| A4 | A3 结果 | **归因消融**：扩界面 vs 只重出序列 | 差分 | **"the structural extension was critical to the improvement in binding affinity"**；**"sequence redesign with ProteinMPNN of the original binding interface did not measurably increase affinity"**；同法得 GCG 231 nM、NPY 3.5 µM（**"Using weak parametric binders as a starting point, we extended their binding interfaces and redesigned their sequences"**） |
| A5 | 已有的螺旋结合脚手架库（数千条全螺旋） | **穿线**：把目标肽序列穿到已结合的螺旋上，按界面疏水接触数最大筛选，再 ProteinMPNN + AF2 initial guess 复算：**"We threaded sequences of peptides of interest onto these complexes, and filtered for interfacial hydrophobic interactions between the target sequence and the scaffolds"** | 未给数值阈值 | **"Initial screening using yeast surface display identified 4/66 binders for SCT"** → **"all four of the designs were found to bind with submicromolar affinity using FP, with the highest-affinity design binding with an affinity of 2.7 nM for SCT"**；交叉：**"The SCT binder design bound GCG, which has 44% sequence identity to SCT"** |
| A6 | 只有 Bid 一级序列 + 随机种子 binder 序列 | **AF2 Hallucination**：**"Starting from only the Bid primary sequence, and a random seed binder sequence (of length 60, 70, 80, 90 or 100 residues), we carried out a Monte Carlo search in sequence space"** | loss 组合与权重：**"For all examples shown in this work, the losses were weighted with relative weights of 1:1:0.1:3:5"**；**"Monte Carlo simulated annealing was carried out, with a starting temperature of 0.01, and the half-life of the exponential decay set to 500 steps"**；**"Alterations were accepted or rejected using the Metropolis criterion"**；**"A total of 5,000 steps were carried out during design"**；收敛 **5,000 步**（**"The trajectories typically converged in 5,000 steps"**）；提速：**"To further speed up convergence, alterations were selectively made to residues with the lowest 50% of AF2 pLDDTs"** | 每 backbone **"Sixty-four sequences were designed per backbone, and were subsequently filtered on the basis of AF2 pLDDT, pTM, RMSD to the design model, RMSD of the monomer to the binder model (without the peptide), and Rosetta ddG"** → **"The precise values used for filtering were chosen to reduce the set down to 46 designs"** |
| A7 | 46 条 Hallucination 设计 | 共表达 GFP-Bid + His-binder，共洗脱判结合：**"with co-elution of GFP and binder used as a readout for binding"** | 可溶、单体、珠下拉 | **"We experimentally tested 46 of the Hallucinated designs"** → **"Four of these designs were further characterized, and showed soluble, monomeric expression even in the absence of peptide co-expression"**、**"and could be pulled down using Bid BH3 peptide immobilized on beads"**；CD 证实诱导折叠：**"Circular dichroism experiments indicated that the Bid peptide was unstructured in solution, and that helicity increased on interaction with the Hallucinated proteins"**；FP：**"FP measurements revealed a 7-nM-affinity binder to Bid peptide"**，且强于天然互作：**"a higher-affinity interaction than that between Bid and the native partner Mcl-1"** |

### B. RFdiffusion 两条支路（Fig 2–3，本文的新引擎）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 机理准备：验证 partial diffusion 能否重采样/规整骨架 | 只加噪到指定步再去噪；用"单序列 AF2 预测"作一致性度量（**"We next explored the ability of partial diffusion"** 一句起） | 骨架多样性可调：**"As expected, partial diffusion allowed diversification of a starting protein fold, and the magnitude of this diversity could be tuned by varying how much noise was added to a starting structure"**；设计性判据 TM：**"as indicated by the TM (Template Modeling) score exceeding 0.5"** | **500 条天然骨架**规模测试：**"500 native proteins of length 100 to 300 residues were selected from the PDB"**；结论 **"The backbones resulting from partial diffusion exhibit higher designability compared to the native backbone, implying that they have been idealised for design purposes"**、**"Furthermore, partial diffusion can considerably increase the designability of input protein models"**；特异性可在家族内被小改动切换（colicin–immunity 体系）：**"that the small changes in protein backbone that partial diffusion can sample are sufficient to mediate specificity changes within protein families"** |
| B2 | Inpainting 产物（GCG 231 nM、NPY 3.5 µM） | 对 Inpainted 的 AF2 模型做部分扩散：**"The models were subjected to 40 noising time steps out of a total of 200 time steps in the noising schedule, and subsequently denoised"**；去噪轨迹上加辅助势：**"An auxiliary potential minimizing the radius of gyration of the binder-peptide complex was used during denoising"** | 势的时序：**"It is more important to apply the potential at the initial denoising steps, and less so towards the end when the quaternary structure is largely fixed"**、**"the scaling factor with which the gradients are multiplied has a cubic decay over the course of the denoising trajectory"**；过滤 **AF2 pAE, pLDDT, RMSD 到设计模型, 单体 RMSD, Rosetta ddG**：**"The resulting libraries were filtered on AF2 pAE, pLDDT, RMSD to the design model, RMSD of the monomer to the binder model (without the peptide) and Rosetta ddG"** | **"Approximately 2,000 partially diffused designs were generated for each target"** → **"The precise values used for filtering were chosen to reduce the set down to 96 designs for each target"**；酵母展示：**"Initial screening with yeast surface display revealed quite high binding success rates, with 25 out of 96 designs binding GCG, and 20 out of 96 binding NPY at 10 nM peptide concentration"**；FP：**"their binding affinities were determined using FP to be 5.6 nM to NPY"**、**"and below the limit of detection in the picomolar range to GCG"**；特异：**"the NPY binder did not show any cross-reactivity to peptide YY"**（PYY 与 NPY **"with 63% sequence identity to NPY"**） |
| B3 | B2 的两个 GCG 变体（Inpainted vs partially diffused） | 解晶体结构做机理归因 | **"Both designs were very close to their design models"**；**"Subtle structural changes in the protein backbone between the original Inpainted design model and the partially diffused model are nearly perfectly recapitulated in the corresponding crystal structures"** | 位移量化：**"a 2.7-Å shift towards the target in the binder backbone enables an isoleucine to fit into a pocket previously occupied by a phenylalanine side chain at position 13"**、**"a 3.6-Å shift in the backbone allows a tyrosine residue to pack underneath the peptide and form a hydrogen bond to the peptide backbone where previously a serine could not make any contacts"**；堆积变好：**"These backbone movements and accompanying sequence changes increase the interaction shape complementarity"**；平行验证：**"We observed similar improvements in estimated binding energy (Rosetta ddG) and contact molecular surface after running partial diffusion starting from the Inpainted designs for GCG and NPY"** |
| B4 | 螺旋构象的 PTH / Bim 肽（固定结构） | **全新 de novo**：给序列 + 结构、拓扑与结合模式全不定：**"and provided RFdiffusion with the sequence and structures of the two peptides in helical conformations"**、**"leaving the topology of the binding protein and the binding mode completely unspecified"**；加同样的回转半径势 | 生成端**不设数值阈值**，只按 AF2 置信度排序后取 96/靶（**"The precise values used for filtering were chosen to reduce the set down to 96 designs for each target"**）；轨迹观感：**"starting from a random distribution of residues surrounding the PTH peptide in a helical conformation, in sequential denoising steps the residue distribution shifts to surround the peptide and progressively organizes into a folded structure that cradles almost the entire surface of the peptide"** | **"We obtained synthetic genes encoding 96 designs for each target"**；酵母展示 PTH **"Using yeast surface display, we found that 56 of the 96 designs bound to PTH at 10 nM peptide concentration"**、Bim **"For Bim, 25/96 of the designs bound by yeast surface display"**；KD 已到检测下限：**"The highest-affinity design again bound too tightly for accurate K"**、**"instead FP data provide an approximate upper bound"**（< 500 pM）；特异：**"Binding was also highly specific; no binding was observed to the related PTHrp"** |
| B5 | Bim 结合体 | 解晶体结构 | **"and found that it closely matched the design model"** | **"A kinked helix on the binder adjacent to the interface is well recapitulated in the structure, and a cross-interface hydrogen-bond network designed between Thr73 and Asn77 of the binder and Asn20 of Bim forms in the otherwise hydrophobic interface"**；形状仍像人设计的沟槽：**"The completely de novo diffused binders again had considerable structural similarity to our starting groove binding concept"** |
| B6 | 只有 PYY 序列（两端无序、cryo-EM 不完全解析） | **重训 RFdiffusion**："一条链给结构、一条链只给序列"（**"We next sought to generalize RFdiffusion to enable binding to flexible targets from a specification of the target sequence alone"**、**"We fine-tuned RFdiffusion by training on two chain systems from the Protein Data Bank"**） | 训练配方：**"In 20% of cases, no sequence or structure was provided to the model (for unconditional generation)"**、**"In the other 80% of cases, 20-100% of the protein was noised"**、**"In contrast to RFdiffusion, however, the structure of up to 50% of the protein"** 与紧接的 **"was noised (diffused), while providing the sequence of those residues"**；学习目的 **"Thus, RFdiffusion learns to condition its predictions on the sequence (without structure) of part of a protein (the monomer) or of a target to bind to"**；**"This version of RFdiffusion was trained for seven epochs"** | **"We found that the fine-tuned version could readily design folded structures around a variety of peptides given only sequence information"**、**"Starting from only the amino acid sequence of PYY, RFdiffusion generated solutions with the peptide in a range of conformations"** → 有一条**与实验构象不同**的设计仍结合：**"A design with the peptide adopting a different conformation from the experimental structure bound PYY with 24.5 nM affinity"**；作者自陈掉亲和力：**"Note that here we explored using shorter binder chain lengths in these calculations, resulting in smaller designs, which probably accounts for the lower affinity than in the fixed structure case above"**、**"Lower affinity binders were also obtained for PTH and GCG using this flexible backbone RFdiffusion approach"** |

### C. 用结合体做工具（Fig 4，应用支路）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | pM 级 PTH 结合体 | 嫁进 lucCage 系统：**"we grafted the 6.1-nM PTH binder into the lucCage system"** | LOD 与激活倍数 | **"screened eight designs for their luminescence response in the presence of PTH, and identified a sensitive lucCagePTH biosensor"**（正文：**"fold luminescence activation in the presence of PTH"**） |
| C2 | PTH / GCG 结合体偶联磁珠 | 免疫亲和富集 + LC-MS/MS：**"We explored the use of our picomolar-affinity RFdiffusion-generated binders to PTH and GCG as capture reagents in immunoaffinity enrichment coupled with liquid chromatography-tandem mass spectrometry"** | 回收率；对照抗体珠 | PTH 缓冲液/血浆 **"with recoveries of 53% and 43%, respectively"**（内源水平不够：**"the endogenous levels are too low for reliable detection"**）；GCG **"The GCG binder beads had comparable peptide capture efficiency to that of monoclonal GCG antibody beads"**；重复使用：**"which lost almost all GCG-binding activity after the first use"** vs **"the GCG-binder-conjugated beads retained almost full binding activity in a second capture experiment"** |
| C3 | C2 现象 | 归因到稳定性 | — | **"This greater robustness to washing and repeated use probably reflects the exceptional stability of the designed binders"**、**"which could substantially lower cost (as they are no longer single use) and extend shelf life compared to using antibodies"** |

**这条流水线里最该记住的一条**：他们的阈值不是从物理推出来的，而是从**下单能力**反推的——**"Precise metrics cutoffs changed for each design campaign to get to an orderable set,"**；且四代工具是**接力**而非并列（参数化 → Inpainting → 穿线 → Hallucination → RFdiffusion，后一级以前一级的产物为起点）。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 50–65 残基 | 上一代 minibinder 的形状前提（不适合承托伸展肽） | "have shapes suitable for binding rigid concave targets, but not for cradling extended peptides" |
| 15–19 残基 | 参数化库中每根螺旋的长度 | "each parametric helix was 15-19 residues long" |
| 200,000 → ~135,000 → 18,000 | 五螺旋排列 → 连环成功骨架 → 最终沟槽脚手架库 | "This process was used to sample a set of 200,000 arrangements of 5 helices"；"to yield a final library of 18,000 scaffolds" |
| 12 条/靶 → 3, 4, 8 | NanoBiT 初筛规模与各靶结合数（µM 级） | "Many of the designs bound their targets (3, 4 and 8 out of 12 to PTH, GCG and NPY, respectively) but with only micromolar affinities" |
| 192 → 44 → 6.04 nM | Inpainting 支路：送测 → 展示命中 → 最优 KD | "Out of 192 designs tested, 44 showed binding against PTH in initial yeast display screening"；"the best binder was found to bind with 6.04 nM affinity to PTH using fluorescence polarization (FP)" |
| 约三个数量级；19% | PTH 起点结合体的亲和力提升与界面增大 | "the affinity of the starting PTH binder was improved by approximately three orders of magnitude, and the computational model of the highest-affinity binder had 19% greater surface area contacting the target peptide" |
| 34% | PTHrp 与 PTH 的序列一致性（特异性对照依据） | "a related peptide sequence with 34% sequence identity" |
| 231 nM / 3.5 µM | Inpainting 后 GCG / NPY 的最优 KD | "Using weak parametric binders as a starting point, we extended their binding interfaces and redesigned their sequences" |
| 4/66 → 2.7 nM | 穿线支路：SCT 送测命中与最优 KD | "Initial screening using yeast surface display identified 4/66 binders for SCT"；"all four of the designs were found to bind with submicromolar affinity using FP, with the highest-affinity design binding with an affinity of 2.7 nM for SCT" |
| 44% | GCG 与 SCT 的序列一致性 | "The SCT binder design bound GCG, which has 44% sequence identity to SCT" |
| 60/70/80/90/100 残基 | Hallucination 的随机种子 binder 链长 | "Starting from only the Bid primary sequence, and a random seed binder sequence (of length 60, 70, 80, 90 or 100 residues), we carried out a Monte Carlo search in sequence space" |
| 1,250 ×3 / 2,500 ×2 / 1,250 ×1 | 每步提议的置换数衰减 | "The number of amino acid changes proposed at each step is decayed throughout the trajectory" |
| 0.01 / 500 步 / 5,000 步 | 模拟退火初温 / 衰减半衰期 / 总步数 | "Monte Carlo simulated annealing was carried out, with a starting temperature of 0.01, and the half-life of the exponential decay set to 500 steps"；"A total of 5,000 steps were carried out during design" |
| 1:1:0.1:3:5 | 五个 loss 的相对权重（pLDDT / pTM / 回转半径 / 接触概率 / 界面 pAE） | "For all examples shown in this work, the losses were weighted with relative weights of 1:1:0.1:3:5" |
| 64 条序列 / backbone → 46 | Hallucination 序列重出规模与最终送测数 | "Sixty-four sequences were designed per backbone, and were subsequently filtered on the basis of AF2 pLDDT, pTM, RMSD to the design model, RMSD of the monomer to the binder model (without the peptide), and Rosetta ddG"；"The precise values used for filtering were chosen to reduce the set down to 46 designs" |
| 46 → 4 → 7 nM | Bid 实测 → 深入表征 → 最优 KD | "We experimentally tested 46 of the Hallucinated designs"；"FP measurements revealed a 7-nM-affinity binder to Bid peptide" |
| 500 条 | partial diffusion "规整天然骨架"实验规模 | "500 native proteins of length 100 to 300 residues were selected from the PDB" |
| TM > 0.5 | 保持同一 fold 的判据 | "as indicated by the TM (Template Modeling) score exceeding 0.5" |
| 40 / 200 步 | Inpainted 模型的部分扩散加噪幅度 | "The models were subjected to 40 noising time steps out of a total of 200 time steps in the noising schedule, and subsequently denoised" |
| ~2,000 → 96 / 靶 | 部分扩散与全新扩散的生成量与送测量 | "Approximately 2,000 partially diffused designs were generated for each target"；"The precise values used for filtering were chosen to reduce the set down to 96 designs for each target" |
| 25/96、20/96（10 nM 肽） | 部分扩散支路的酵母展示命中（GCG / NPY） | "Initial screening with yeast surface display revealed quite high binding success rates, with 25 out of 96 designs binding GCG, and 20 out of 96 binding NPY at 10 nM peptide concentration" |
| 5.6 nM / pM 超下限 | 部分扩散后 NPY 与 GCG 的 KD | "their binding affinities were determined using FP to be 5.6 nM to NPY"；"and below the limit of detection in the picomolar range to GCG" |
| 63% | PYY 与 NPY 的序列一致性（特异性的难度标尺） | "with 63% sequence identity to NPY" |
| 2.7 Å / 3.6 Å | 两处骨架位移（Ile13 进袋、Tyr16 与肽成氢键） | "a 2.7-Å shift towards the target in the binder backbone enables an isoleucine to fit into a pocket previously occupied by a phenylalanine side chain at position 13" |
| 56/96（PTH）、25/96（Bim）、< 500 pM | 全新 RFdiffusion 支路的命中与最优 KD | "Using yeast surface display, we found that 56 of the 96 designs bound to PTH at 10 nM peptide concentration"；"For Bim, 25/96 of the designs bound by yeast surface display" |
| 24.5 nM | 柔性靶（只给 PYY 序列）支路最优 KD | "A design with the peptide adopting a different conformation from the experimental structure bound PYY with 24.5 nM affinity" |
| 33% / 29%；29% / 21% | 扩散后 CMS 与 Rosetta ddG 的改善（GCG、NPY） | "the average contact molecular surface for the partially diffused GCG binders and NPY increased by 33% and 29% respectively compared to that of the starting models, and the Rosetta ddG improved by 29% and 21%" |
| 8 条 → 10 nM LOD | lucCagePTH 传感器 | "screened eight designs for their luminescence response in the presence of PTH, and identified a sensitive lucCagePTH biosensor" |
| 53% / 43%；91.1% | PTH 缓冲液/血浆回收率；GCG 相对单抗的回收率 | "with recoveries of 53% and 43%, respectively"；"The GCG binder beads had comparable peptide capture efficiency to that of monoclonal GCG antibody beads" |
| 20% / 80%；20–100%；至多 50%；7 个 epoch | 重训版 RFdiffusion 的条件化配方 | "In 20% of cases, no sequence or structure was provided to the model (for unconditional generation)"；"In the other 80% of cases, 20-100% of the protein was noised"；"This version of RFdiffusion was trained for seven epochs" |
| pAE < 10、pLDDT > 92、pTM > 0.8、RMSD <1.75 Å | 穿线支路两轮共用的硬闸口（全文数值） | "Both rounds had gate filters of interface pAE < 10, mean pLDDT > 92, predicted template modelling (pTM) score > 0.8 and RMSD to input backbone <1.75" |
| pAE (<10)、pLDDT (>80)、Rosetta ddG (<−40) | 全文给出的"通用"过滤侧重（但明写每批都变） | "Precise metrics cutoffs changed for each design campaign to get to an orderable set," |

## 5. 结论——作者说了什么

1. 螺旋肽结合蛋白的设计难点可以**分头解决**：形状靠沟槽脚手架、构象不确定性靠"不预设结构"的方法；**"Design of peptide-binding proteins is challenging for two reasons"** 是他们自己的框架句。
2. **参数化、Inpainting、穿线、Hallucination、RFdiffusion 五种方法都能出结合体**，但亲和力阶梯分明：µM（参数化）→ nM（Inpainting/穿线/Hallucination）→ pM（RFdiffusion 全新 + 部分扩散）。
3. 深度学习方法与人类设计**收敛到同一个解**：**"The deep learning methods largely converged on the overall solution to the helical peptide-binding design problem"**（沟槽 + 螺旋衬里），增益主要来自直接"按靶形状造脚手架"带来的更高形状互补。
4. **partial diffusion 是通用局部优化器**：既能优化设计体，也能"规整"天然骨架（**"We found that RFdiffusion improves the"** 一句，原文续"designability"），甚至足以改变家族内特异性。
5. **无实验优化的 pM 结合体**是其核心主张：**"To our knowledge, the Bim- and PTH-binding proteins diffused starting from random noise are the highest-affinity binders to any target (protein, peptide or small molecule) achieved directly by computational design with no experimental optimization"**。
6. 应用侧主张可替代抗体：**"Antibodies have served as the industry standard for affinity reagents for many years, but their use is often hampered by variable specificity and stability"**；优势四条（螺旋埋藏、易接传感器、更稳更便宜、免免疫动物）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **本文的"方法演进"其实是消融实验的编年史**：第 2.3 条（扩界面有效、换序列无效）与第 2.6 条（柔性靶掉亲和力）都是**主动做的负结果**。→ 对我们：每个漏斗环节必须能回答"去掉它会怎样"，否则无法定位瓶颈；我们目前的漏斗缺这种成对的消融。
2. **阈值 = 下单预算的函数**（**"The precise values used for filtering were chosen to reduce the set down to 46 designs"** 与 **"The precise values used for filtering were chosen to reduce the set down to 96 designs for each target"** 成对出现）。这一条比 [B09] 的"效率=通过率÷单价"更直接：**先定能测多少个，再定筛多严**。→ 对我们：湿实验每轮只够测个位数构建体，那漏斗的任务就不是"排出最好的 1%"，而是"排出信息量最大的 4 个"（机制多样性 + 失活对照），阈值应按**读出多样性**而非分数排序。
3. **"同一批零件换用途"是本文真正的杠杆**：结合体 → 传感器（lucCage）→ 富集试剂（LC-MS/MS），一次设计三处复用，且他们**用负例支撑**（抗体珠一次即失效 vs 设计珠二次仍有效）。→ 对我们：一个酶设计相关蛋白候选应当同时设计成"报告反应可行性"与"报告副产物"两种读出，而不是只为一个活性读数。
4. **"绕开全原子计算"不等于"不需要机理"**。他们用**晶体结构 + 位移量（2.7 Å / 3.6 Å）+ 堆积判据**做了等价的机理归因。→ 对我们：在没有 MD/QM 预算时，"结构位移 + 定点突变 + 产物化学"这条三角验证是可复制的低成本替代。
5. **"只给序列就能设计"会掉亲和力，且作者给出了可能原因（链长更短）**——这是全文最诚实的一条边界。→ 对我们：当我们为了处理柔性/未知构象而放弃显式模板时，必须**同时报告因此损失的量级**，不许只报"能做出来"。
6. **他们没做的事**：全文没有 MD/QM/自由能，没有把 pAE/pLDDT 与催化量做相关；因此本文不能为任何"结构置信度→活性"的推断提供证据。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：① 参数化沟槽初筛只有 µM；② 柔性靶（只给序列）支路亲和力下降，PTH/GCG 到 µM 段，PYY 24.5 nM；③ Hallucination 会产生对抗序列，需 ProteinMPNN 补救；④ GCG 在提取物中回收率低，"将需要进一步提高特异性"；⑤ Inpainting 的收益只来自界面扩展，序列重出不涨（**"sequence redesign with ProteinMPNN of the original binding interface did not measurably increase affinity"**）。
- 我们读出：① **阈值口径不统一**——同一篇里同时有"硬闸口四件套"（pAE<10/pLDDT>92/pTM>0.8/RMSD<1.75 Å）与"每批都变的侧重"（pAE<10/pLDDT>80/ddG<−40），说明这些数字不是可迁移的常数；② 各支路的命中率分母不同（12 / 66 / 192 / 46 / 96），跨支路比较"成功率"没有意义；③ Hallucination 的成功率 4/46 与 pM 级结果来自**不同支路**，本文的跃升主要由**生成端换模型**贡献，不是判据端贡献；④ 结构验证只覆盖最优个体（4 条深入表征、2 条晶体），未命中者无任何实验反证；⑤ 全文的"pM"多数是 FP 给出的**上限/低于检测限**式表述（**"instead FP data provide an approximate upper bound"**），不是拟合出的 KD 分布。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **"反推阈值"的预算思维**：把湿实验单轮能承载的构建体数当自变量，反推漏斗应削到多大（本文即"削到 46 / 96"）。我们的做法：单轮 4 个构建体 → 漏斗输出必须是 4 个**互补机制假设**的候选 + 内置失活对照，而不是排序前 4 名。
2. **成对消融的写法**：每个筛子/步骤都要配一个"只做几何不改序列 / 只改序列不动几何"的对照，否则不许进漏斗。对应我们：任何"折叠约束"或"位点约束"的改动都要单独测它对分步化学事件各自的影响。
3. **"绕开全原子"的替代归因**：结构位移 + 定点突变 + 产物确证三角互证（本文 2.7 Å/3.6 Å 位移→Ile13/Tyr16 接触→CMS/形状互补数字）。我们可用 xTB/短 MD 做同规模的位移—接触对照，但必须**明确它不替代能量学**。
4. **柔性/未知构象时的模型改造思路**：与其硬套模板，不如改训练/采样配方（本文"一条链给结构、一条链只给序列"）。对我们：面对"底物构象未知"的 酶-底物复合物，可以显式引入"只约束配体连接原子、不约束其整体构象"的条件化生成，并**同步报告因此损失的亲和力/命中率**。
5. **同一零件的多读出复用**：把"能结合的蛋白"同时做成传感器与富集试剂；对应我们把同一批酶变体同时用于"产物身份确证"（LC-MS/MS）与"竞争反应读出"，提高每次湿实验的信息量。

**不可迁移（为什么不能照搬）**

1. **本文全部判据（interface pAE、pLDDT、pTM、RMSD、Rosetta ddG、接触分子表面）都是"结构自洽 + 界面埋藏"类**，其成功定义是"结合得紧不紧、特异不特异"。目标酶的成功要判三步化学事件（分步化学事件）与副产物分支，**结构自洽既不必要也不充分**；本库判据 §2 禁止把 binder 的 pAE/pLDDT/ipTM 阈值当酶活闸口。
2. **"pM 级、无需实验优化"不能转成我们的成功概率**。他们测的是纯结合平衡（FP/BLI），有天然配体的可测 KD 与明确上限；我们没有对应的可测标签，也没有被产物确证的阳性集。只许引用其**工作流组织方式**，不许引用其命中率/亲和力数字做校准。
3. **µM→nM→pM 的阶梯是"结合能"阶梯，不是"催化能力"阶梯**。酶活涉及势垒与过渡态，本文全程无 MD/QM/自由能，因此这篇**不能**为"用结构置信度预测酶活"提供任何支持证据。
4. **12 / 46 / 66 / 96 / 192 这类展示与 FP 通量在产物化学里不存在**。我们的末端不是"通量最大化"而是"机制多样性 + 失活对照"的信息量最大化，不能照搬他们"削到 96 条再测"的量级假设。

## 9. 溯源与自检

- 引句底稿: data/interim/baker_lit/ft/helicalpeptide2024.txt
- 唯一登记全文：`data/interim/baker_lit/ft/helicalpeptide2024.txt`（74,815 B，Europe PMC fullTextXML 去标签纯文本；`&lt;`/`&gt;` 未解码实体由 `scripts/litcards_text.py` 的 `norm()` 在比对时统一还原）。
- 登记底稿：`sources/baker.md:160–170`（原卡把参数化初筛写成"每靶 12 条……但只有微摩尔亲和力"这种跨句拼接；本卡改为分别引用图中句子 **"and screened 12 designs for each target using a NanoBiT split-luciferase binding assay"**（A2 行）与正文句子 **"Many of the designs bound their targets (3, 4 and 8 out of 12 to PTH, GCG and NPY, respectively) but with only micromolar affinities"**，因为这两句在原文之间夹有图号与补充图号，拼接会被门禁判为不命中）。
- 引句处理约定：本卡凡因标签剥离导致空格变化的片段（如 `6.04 nM`、`25 out of 96`、`<1.75 Å`）均按归一化后的形态书写；对含 `1,250 ×3 steps`、`&lt;−40`、`µM`、`K d`、希腊字母（α/β/κ）等**易发生字符漂移**的位置，本卡**不做英文引句**，仅在数字台账里以中文叙述给出。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：由 `scripts/verify_literature_cards.py --only B12 --no-report` 执行，把卡内所有"直双引号包住、不含中日韩字符、≥20 字符且 ≥12 个字母"的片段在 引句底稿 里逐字命中检查，任一条不命中即 FAIL。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 3 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文
target=α-螺旋肽与柔性肽靶：PTH、PTHrp（特异性对照）、GCG、GLP1、GIP、SCT、NPY、PYY、促凋亡 BH3 域 Bid 与 Bim；下游做 lucCage 生物传感器与 LC-MS/MS 富集试剂
backbone_generation=三代并行 + 接力：① Rosetta 参数化"三螺旋沟槽 + 两支撑螺旋"库（Crick 参数化，200,000 排列 → ~135,000 连环骨架 → 18,000 库）；② RoseTTAFold Inpainting（RF joint）扩界面 + ProteinMPNN 重出序列；③ 把肽序列穿线到已有螺旋结合脚手架并按界面疏水接触筛选；④ AF2 Hallucination 在序列空间做 Monte Carlo（60–100 残基随机种子，5,000 步）后由 ProteinMPNN 重出序列；⑤ RFdiffusion 自由扩散（固定靶结构）与 partial diffusion（对 Inpainted/天然骨架只加噪到指定步再重去噪，配合最小化复合物回转半径的辅助势）；另有针对柔性靶重训的 RFdiffusion（对靶链只给序列不给结构）。序列端统一 ProteinMPNN（部分支路 ProteinMPNN + Rosetta FastRelax），复测统一 AF2 with initial guess
computational_filters=interface pAE；mean pLDDT；pTM；RMSD 到输入骨架 / 到设计模型；单体—结合体模型间 RMSD；Rosetta ddG；contact molecular surface 与形状互补；membrane insertion potential（负设计）；Hallucination 侧为五 loss 加权和（bound-state pLDDT、bound-state pTM、半径 of gyration、contact probability、interface pAE）；设计性检验用 TM 分数与单序列 AF2 复现度
thresholds=穿线支路两轮硬闸口：interface pAE < 10、mean pLDDT > 92、pTM > 0.8、RMSD 到输入骨架 <1.75 Å；全文通用侧重 pAE <10、pLDDT >80、Rosetta ddG <−40（明写每批浮动）；Hallucination loss 权重 1:1:0.1:3:5、退火初温 0.01、半衰期 500 步、共 5,000 步、仅改 pLDDT 最低的 50% 残基；部分扩散加噪 40/200 步（示例 time step 70）；设计性检验 TM > 0.5；削池目标 Hallucination 46 条、扩散每靶 96 条；展示与 FP 分选肽浓度 10 nM；回转半径辅助势梯度三次衰减
md_used=否（MD 只在"传统方法为何做不了局部优化"的论证里被提及一次："This is difficult for traditional design methods as extensive full-atom calculations are needed for each sample around a starting structure"；正文未用 MD 做筛选）
qm_used=否（全文无 QM/过渡态/自由能计算）
experimental_methods=NanoBiT 分裂荧光素酶初筛 → 酵母表面展示（多浓度分选）→ E. coli 可溶表达 + SEC → 荧光偏振 FP 定量 KD → ITC/CD 热熔（95 °C 稳定性与可重折叠）→ X 射线晶体学（GCG Inpainted 与部分扩散体、Bim 结合体）→ 共表达 GFP-Bid/His-binder 共洗脱与肽下拉 → 嫁进 lucCage 做生物传感器（八条筛 LOD 与激活倍数）→ 结合体偶联磁珠 + 免疫亲和富集 + LC-MS/MS（缓冲液与人血浆加标、单抗珠对照、二次使用回收率）
pipeline_counts=参数化：200,000 排列 → ~135,000 骨架 → 18,000 库 → 每靶 12 条 NanoBiT 筛（结合 3/4/8，µM）；Inpainting：192 条送测 → 44 条展示命中 → 最优 6.04 nM（PTH），另有 GCG 231 nM、NPY 3.5 µM；穿线：4/66 命中 SCT → 2.7 nM；Hallucination：每 backbone 64 条序列 → 削到 46 条送测 → 4 条深入表征 → 7 nM；部分扩散：~2,000 条/靶 → 削到 96 条/靶 → GCG 25/96、NPY 20/96 展示命中 → NPY 5.6 nM、GCG 低于检测限（pM 段）；全新扩散：96 条合成基因/靶 → PTH 56/96、Bim 25/96 → KD < 500 pM（FP 上限式表述）；柔性靶（只给序列）：PYY 24.5 nM，PTH/GCG 掉到 µM；天然骨架规整实验：500 条 PDB 蛋白
hit_rate=支路间差异极大且分母不同，不可合并成一个总命中率：NanoBiT 参数化 3–8/12（µM）；Inpainting 展示 44/192；穿线 4/66；部分扩散展示 25/96（GCG）与 20/96（NPY）；全新扩散展示 56/96（PTH）与 25/96（Bim）；Hallucination 共洗脱 4/46 深入表征；作者据此主张 pM 级结合体可在无实验优化条件下直接由计算得到
best_metric=PTH 与 Bim：FP 给 K d 上限 < 500 pM（正文写"too tightly for accurate K d estimation"）；GCG：低于检测限（pM 段）；NPY 5.6 nM、PTH（Inpainting）6.04 nM、SCT 2.7 nM、Bid 7 nM、PYY 24.5 nM；传感器 lucCagePTH：LOD 10 nM、约 21 倍 luminescence activation；LC-MS/MS 回收率：PTH 缓冲液 53% / 人血浆 43%，GCG 相对单抗 91.1%
cost_or_stat_note=正文未给 CPU/GPU 单价与总核时（本文成本口径缺失，仅可读到"RFdiffusion 比 Hallucination 计算效率高得多"的定性比较："RFdiffusion directly generates protein structures with diverse topologies, and is much more compute efficient than Hallucination"）；重训版 RFdiffusion 训练 7 个 epoch；每靶下单规模统一削到 46 或 96 条，阈值随批次变化而非物理常数；合成基因 96 条/靶
role_in_timeline=把 [B08]/[B09] 建立的"RFdiffusion 生成 + AF2 自洽闸口"漏斗首次推到**柔性/短肽靶**这一新靶类，并把其中两个部件标准化：① partial diffusion（从中间时间步重采样）作为通用局部优化器（与 [B14] 同期、互相印证），② 阈值按"能测多少"反推（46/96）作为工程实践；同时首次把设计结合体推进到工具属性（生物传感器 + 替代抗体的 LC-MS/MS 富集试剂），为后续 [B21]（IDP 靶）与 [B24]（把结局标签当货币）铺路
source_pointer=data/interim/baker_lit/ft/helicalpeptide2024.txt（唯一登记全文，74,815 B）+ sources/baker.md:160-170
CSV回填-->
