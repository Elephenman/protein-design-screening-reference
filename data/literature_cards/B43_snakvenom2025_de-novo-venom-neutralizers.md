# [B43] De novo designed proteins neutralize lethal snake venom toxins（Nature 2025）—— 从靶点到体内保护的证据链

Vázquez Torres S, Benard Valle M, … Laustsen AH, … Baker D（华盛顿大学 IPD / 丹麦 DTU / 利物浦热带医学院）
Nature 2025, 639:8053, 225–231 · DOI 10.1038/s41586-024-08393-x · PMID 39814879 · PMCID PMC11882462

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B43**（组：Baker 组） |
| 论文 | Nature 2025, 639:225–231（DOI 10.1038/s41586-024-08393-x · PMID 39814879 · PMCID PMC11882462）；全文注明基于 2024-05-17 Research Square 预印本 |
| 本地全文（本卡唯一底稿） | `data/interim/baker_lit/ft/snakvenom2025.txt`，68,787 B，142 行，SHA-256 `0d2dd174b172c66c58b3168dc348d29c…`（2026-10-16 落地） |
| 身份复核 | 文件首行为抽取头 `981 npgopen Nature Nature PMC11882462 11882462 11882462 39814879 10.1038/s41586-024-08393-x De novo designed proteins neutralize lethal snake venom toxins …`，PMID/DOI/PMCID/标题与 CSV 行一致 ⇒ 未挂错行；第 2 行版权块另注 modified publication 2026、许可证由 CC-BY-NC-ND 改为 CC-BY |
| 登记底稿清单 | `sources_map.json` 里 B43 登记两份：上述全文 + `sources/baker.md`（对应第 565–577 行的原卡段落）。**本卡全部引句只从上述全文复制**，声明见第 9 节 |
| 证据级别 | **全文级**（本卡所有英文引句均可在该全文里逐字命中；门禁结果见第 9 节） |
| 未取到的部分 | 补充信息 Supplementary Figs 1–10 与 Table 1、Extended Data Table 1 的衍射/精修统计表、Fig 2/4 的逐点原始读数、来源数据与代码仓库具体内容（正文只给 GitHub 链接）。凡涉及这些，本卡写"正文未给出"。**注意：全文里出现的 `N  =  3`、`T m`、`&lt;` 等是去标签后的残留排版，本卡引句按门禁的空白折叠口径写成单空格形式** |
| 本文不含 | MD、QM、自由能微扰、任何亲和力/结合自由能计算（第 3 节的四个阈值全是结构自洽与经验能量项） |

## 1. 这篇到底解决什么（大白话）

蛇咬死的、致残的人绝大多数在缺资源的农村地区，现在唯一的特效药是"给马/羊免疫后抽血做出来的多克隆抗体血清"，它有三个硬毛病：贵、要冷链、会过敏休克；而且对眼镜蛇科毒液里最要命的一类小蛋白——三指毒素（3FTx，含 α-神经毒素和细胞毒素）——常常**中和不够**，因为这类小分子在 immunized 动物身上本来就激不起强抗体应答。作者的思路是：**干脆不做免疫、不建大文库**，直接用深度学习从头画结合蛋白——已知靶毒素的结构或序列就够，把全新的约 100 个氨基酸的小蛋白"贴"到毒素上，把它结合人体受体/破坏细胞膜的那几个环给挡住。

结果是三层：① 只下单了几十条设计（44/42/55 条），就从计算设计里拿到了 nM 级结合体（最好了 0.9 nM）；② 这些结合体在细胞电生理里 1:1 摩尔比就完全阻断毒素对乙酰胆碱受体的抑制，比同类纳米抗体还强；③ 给小鼠打 3 倍致死量（LD50）的神经毒素，提前 30 分钟或事后 15 分钟给到 10 倍摩尔过量的设计蛋白，**24 小时 100% 存活**，而且用非靶结合体做交叉处理对照证明是特异性的。唯一没打通的是细胞毒素那条支线：它在细胞培养里能中和 7 种眼镜蛇毒液的细胞毒活性（70–90%），但**在小鼠皮内注射毒液致皮肤坏死模型里没能缩小病灶**，作者明写亲和力还得再优化。

用作者自己的话（摘要）："With limited experimental screening, we obtained protein designs with remarkable thermal stability, high binding affinity and near-atomic-level agreement with the computational models"，"The designed proteins effectively neutralized all three 3FTx subfamilies in vitro and protected mice from a lethal neurotoxin challenge"。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **"会结合"不等于"会中和"——这是全文最难的一环，他们把它前移成几何判据**。
   难点：α-神经毒素靠环（loop）堵住烟碱型乙酰胆碱受体（nAChR）而致死，随便一个高亲和结合体未必挡得住这个界面。
   证据（原句）："we focused on binding modes that block neurotoxin binding to nAChRs through steric hindrance"；"Rather than focusing on the nAChR-binding site like previously discovered antibodies"；"Top candidates were selected for in vitro validation on the basis of their ability to interfere with toxin binding to nAChR, guided by structural alignments comparing the neurotoxin–nAChR complex with and without the designed binder"。
   **他们做了什么**：改变生成条件而不是改打分函数——用二级结构张量 + 块邻接张量把 RFdiffusion 约束到"与设计 β-strand 与毒素暴露的边缘 β-strand 配对成扩展片层"这一种结合模式，一条链一条链地生成；再拿毒素–nAChR 复合物结构做叠合，人工挑出会位阻的模型送实验。
   代价：这条**功能预筛没有阈值、没有通过率**（"原文未给阈值"），也没有预测中和剂量比；真正判定中和靠膜片钳。
2. **极性、扁平、只有三根环可抓的靶，第一轮命中率极低**。
   证据：ScNtx 那条支线 "Synthetic genes encoding 44 designs targeting ScNtx were screened via yeast surface display, and one candidate was identified to bind ScNtx with a dissociation constant ( K d ) of 842 nM, as confirmed by bio-layer interferometry (BLI)"；α-cobratoxin 那条支线 "Of 42 RFdiffusion designs against α-cobratoxin, one candidate had a binding affinity of 1.3 µM using BLI"。
   **他们做了什么**：加做第二轮**局部再扩散（partial diffusion）**做界面成熟——"The models were subjected to 10 and 20 noising time steps out of a total of 50 time steps in the noising schedule and subsequently denoised"，且"Following ProteinMPNN and AF2 screening, partial diffusion was used to further optimize the designs with the best metrics"；每靶再生成约 2,000 条、用**同一套阈值**复筛，然后只下单 78（ScNtx）与 38（cobratoxin）条。
   收益与代价：ScNtx 线 "11 of 78 designs had higher affinity than the initial hit"，最好了 0.9 nM（SPR）；也就是说**亲和力是从 842 nM→0.9 nM 靠第二轮采样+实验测出来的**，第一轮结构自洽分数无法预警谁会被改善。
3. **细胞毒素的机制不给你"配对 β-strand"的机会**。
   证据："To target cytotoxins, we hypothesized that relying solely on β-strand pairing interactions might not adequately prevent cytotoxin insertion into membranes"（原因：它的三根手指环本身就在插膜）。
   **他们做了什么**：换成 hotspot-residue 条件生成，直接绑定三根环；为了覆盖宽度，先由 86 条 UniProt 序列做共识体（"To increase the breadth of neutralization, we targeted a consensus sequence derived from 86 different snake cytotoxins"）。
   代价：这一条最终只做到 271 nM（CYTX），且**体内皮肤病变模型失败**（见第 5 条）；共识体带来的"广度"完全是实验测出来的（7 种毒液），计算上没有任何跨序列结合预测。
4. **计算筛子管不住"能不能表达成单体"**。
   证据：细胞毒素线 "A total of 55 protein designs were recombinantly expressed using Escherichia coli , and following SEC purification, 18 designs with monomeric populations were tested in a luminescent cell viability assay"；"Of these, one protein binder (CYTX) had high solubility, with a single monomeric peak in SEC and high neutralization activity against Naja pallida and Naja nigricollis whole venoms"。
   **他们做了什么**：把可溶性/单体峰当成**实验层的第二道闸**（SEC），而不是去找一个计算代理量；只有 18/55 单体可用，说明 PAE/pLDDT/ddG 三条阈值对"表达成败"几乎没有约束力。
   代价：这条漏斗的真实分母被隐藏了——**全文没有报告 ~2,000 条设计里过滤后剩多少**，读者只能拿到"下单数"（44/42/55/78/38）。
5. **细胞毒素在活体皮肤里没中和成（本文未解决）**。
   证据："However, preliminary studies indicated that the CYTX design, in 1:1, 1:2.5 and 1:5 molar ratios (toxin:binder), did not significantly decrease the size of the dermonecrotic lesions induced by intradermal"（模型是 N. nigricollis 毒液皮内注射）；作者自限："The affinity of CYTX likely needs to be further optimized for full in vivo neutralization of cytotoxins."
   **他们做了什么**：只把它写成 pilot 并如实报告阴性——"For sample size, N = 3 was used for groups receiving the cytotoxin binder because this was a pilot experiment"；病灶大小用 VIDAL 工具量化。
   本文未解决的部分：没有组织穿透/PK 测量、没有与抗体血清头对头比较、也没解释"细胞活力实验 70–90% 保护"为什么到不了活体皮肤。
6. **柔性影响结晶，靠工程改造换取结构证据（有代价）**。
   证据："To reduce flexibility to favour crystallization, a disulfide bond was introduced in a flexible loop connecting the β-sheet segment to the two α-helices of CYTX, yielding a candidate (CYTX_B10) with improved thermal stability ( T m = 70.3 °C) and monomeric profile during SEC, but a slightly weaker K d of 740 nM"。
   **他们做了什么**：为拿晶体（以及验证设计构象）主动改造一个变体，接受亲和力从 271 nM 退到 740 nM；这也顺带证明 RFdiffusion 能生成"违反常规结构规则"的开折迭骨架："The unusual open fold of CYTX_B10 highlights the power of RFdiffusion to custom generate scaffolds shape-matched with protein targets"。
7. **对照体系必须能区分"特异性中和"与"通用保护作用"**。
   **他们做了什么**：三层都配了非同源对照——电生理里"a control nanobody targeting phospholipase A 2 had no effect"、体内用交叉处理（cross-treatment）实验、以及单给结合体的耐受对照（"The SHRT binder provided complete protection (100%) to mice when preincubated and administered intraperitoneally with the corresponding short-chain neurotoxin at a 1:10 molar ratio of toxin to binder"，而"as expected, it did not neutralize the non-target"α-cobratoxin）；小鼠只给药不中毒时"Mice injected with the binder alone showed no negative effects at 24 and 48 h post-injection or up to 2 weeks post-injection."
   代价：神经毒素两条线**彼此不交叉中和**，说明"3FTx 家族级泛中和剂"并没有做出来——泛覆盖仍要靠多设计组合（Discussion 里只作为展望）。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **生成**：RFdiffusion，用二级结构张量与块邻接张量做条件约束（两种模式：与靶边缘 β-strand 配对；或指定环上 hotspot 残基）。
- **序列**：ProteinMPNN 出序列 → Rosetta FastRelax 松弛 → 结构评估。
- **评估闸口（全文唯一的一组定量阈值）**：AlphaFold2 + initial guess 单序列预测，取 **界面 PAE < 10**、**pLDDT > 80**、**Rosetta ddG < −40**；两轮设计用**同一组阈值**。
- **功能预筛（非定量）**：把复合物模型与毒素–nAChR 复合物叠合，看是否位阻阻断。
- **界面再优化**：partial diffusion（对最优模型的骨架加噪 10/20 步后再去噪）。
- **实验层**：酵母表面展示 + 单设计流式分选（结合）；BLI/SPR（亲和力）；SEC（单体）；CD 熔解（Tm）；X 射线晶体学（设计构象是否被实现）；RD 细胞平面膜片钳（受体层面中和）；HEK293T/N/TERT 发光细胞活力（毒素层面与整毒液中和）；小鼠 LD50、体内保护/救援、皮内毒液皮肤病变模型（疗效）。
- **本文不含**：MD、QM、结合自由能、任何动力学/pKa/催化几何计算。亲和力、可表达性、中和效力、体内暴露**全部是测出来的**。

### 证据链逐层走法（L0→L13；本卡重点是每层的"判据"与"分母"）

| 层 | 输入 | 操作 | 判据 / 阈值 | 输出与规模（分母） |
|---|---|---|---|---|
| L0 靶点与结构输入 | ScNtx（PDB 7Z14）、α-cobratoxin（PDB 1YI5）、共识细胞毒素用 AF2 模型 | 决定"能不能设计"的前提：有结构或序列数据 | "The crystal structures of ScNtx (PDB 7Z14 ) and α-cobratoxin (PDB 1YI5 ) served as the inputs for RFdiffusion"；"In the case of the consensus cytotoxin, the AF2 model was used" | 3 个设计靶（短链神经毒素共识体 / 长链神经毒素天然体 / IA 型细胞毒素共识体） |
| L1 共识序列 | UniProt 查询 snake three-finger toxin family Short-chain subfamily Type IA cytotoxin sub-subfamily | Clustal Omega 多序列比对，逐列取最频氨基酸；无显性则用按电荷/疏水性归类的共识符号 | "The resultant 86 unique CTX sequences were subjected to multiple sequence alignments in Clustal Omega"；"a consensus symbol was used to represent a group of similar amino acids on the basis of their properties, such as charge or hydrophobicity" | 86 条序列 → 1 条共识靶 |
| L2 条件张量 | 目标毒素的暴露（edge）β-strand；结合模式设计 | 构造 [L,4] 二级结构 one-hot（0=α、1=β、2=loop、3=masked）+ [L,L,3] 邻接 one-hot；binder 全 masked，仅预设 strand 残基标 β 并置为与靶 strand 邻接 | "the secondary structure tensor indicated an entirely masked binder structure, with the exception of binder residues set to β-strand identities" | 每条神经毒素按"一次一根暴露 β-strand"分别条件化生成 |
| L3 骨架生成（第一轮） | L0/L1 靶结构 + L2 张量 | RFdiffusion 扩散去噪 | 原文未给阈值（生成阶段不设卡） | "Approximately 2,000 diffused designs were generated for each target, using the secondary structure and block adjacency tensors in the RFdiffusion model" |
| L4 序列 + 结构自洽过滤 | ~2,000 骨架/靶 | ProteinMPNN 出序列 → Rosetta FastRelax → AF2 + initial guess | **AF2 PAE < 10、pLDDT > 80、Rosetta ddG < −40**："The resulting libraries were filtered on the basis of AF2 predicted aligned error (PAE) < 10, predicted local distance difference test (pLDDT) > 80 and Rosetta Delta Delta G (ddg) < -40" | **过滤后通过数原文未报**；进入下单的是 44（ScNtx）与 42（α-cobratoxin）条 ⇒ 计算命中率的分母不可得 |
| L5 功能（位阻）预筛 | 过滤后的复合物模型 | 与毒素–nAChR 复合物做结构叠合，看结合体是否挡住受体结合面 | 无定量阈值（人工/几何判断）："Top candidates were selected for in vitro validation on the basis of their ability to interfere with toxin binding to nAChR, guided by structural alignments comparing the neurotoxin–nAChR complex with and without the designed binder" | 决定谁被下单；细胞毒素支线不做此步（改绑环） |
| L6 结合实验（第一轮） | 下单设计（基因由 eBlocks 合成，Golden Gate 入 pETcon3/LM627） | 酵母表面展示：EBY100 诱导表达、生物素化毒素标记、96 孔自动进样流式逐设计分选；命中者 E. coli 表达 + BLI | "labelled for 40 min with biotinylated toxin targets at room temperature using the without-avidity labelling condition"；"individually sorted on the basis of each unique design using a 96-well compatible autosampler" | ScNtx：**1/44** 结合（Kd 842 nM）；α-cobratoxin：**1/42** 结合（1.3 µM BLI） |
| L7 界面再优化（第二轮） | 第一轮最优设计的 AF2 模型 | partial diffusion：50 步噪声计划里取 10 与 20 步加噪再去噪 → ProteinMPNN（在 Rosetta FastRelax 之后）→ AF2 + initial guess → **同一组阈值**复筛 | "The models were subjected to 10 and 20 noising time steps out of a total of 50 time steps in the noising schedule and subsequently denoised"；"Approximately 2,000 partially diffused designs were generated for each target." | 每靶再 ~2,000 → 下单 78（ScNtx）与 38（α-cobratoxin）；**ScNtx 线 11/78 优于初 hit**，最佳 SHRT 0.9 nM（SPR）/0.7 nM（BLI）、LNG 1.9 nM（SPR）/6.7 nM（BLI）；**过滤通过数同样未报** |
| L8 生物物理确证 | 命中设计 | SEC 看单体峰；CD 看 αβ 二级结构与熔解温度 | "SHRT showed a single monomeric peak in size exclusion chromatography (SEC), characteristic αβ-protein circular dichroism (CD) spectra and thermal stability with a melting temperature ( T m ) of 78 °C" | SHRT Tm 78 °C；LNG Tm > 95 °C；CYTX 61 °C；CYTX_B10 70.3 °C。细胞毒素线分母：**55 表达 → 18 单体 → 进中和实验 → 1 个 CYTX（271 nM）** |
| L9 结构验证 | 纯化蛋白（± 毒素复合物） | 坐滴气相扩散结晶 + 同步辐射 AMX 线 + 分子置换（Phaser）+ Phenix/Coot 精修 | 以晶体与设计模型的重叠程度为准（RMSD） | "we determined the structure of the SHRT design in the apo state, which closely matched the computational design model (2.58 Å resolution; 1.04 Å root-mean-square deviation (RMSD))"；LNG "which closely matched the computational design model (2.68 Å resolution; 0.42 Å RMSD over design, 0.61 Å over toxin"（另有"there was a slight deviation in the positioning of the toxin relative to the binder"）；CYTX_B10 2.0 Å、设计 1.32 Å、毒素 0.58 Å；PDB 9BK5/9BK6/9BK7 |
| L10 体外功能中和 | 毒素 + 设计/纳米抗体 | RD 细胞（内源肌型 nAChR）平面膜片钳：约 1 个 IC80 的毒素与设计预孵，梯度比 1:1、1:3、1:9、1:27；ACh 70 µM 响应归一化 | "Protein binders were preincubated with approximately one 80% inhibitory concentration (IC 80 ) of α-cobratoxin or ScNtx at various toxin-to-binder molar ratios (1:1, 1:3, 1:9 and 1:27) and then added to the cells"；判据 = 1:1 完全恢复 ACh 响应（n = 16） | SHRT 与 LNG 均在 1:1 完全中和，优于对应纳米抗体（TPL1163_02_A01 / TPL1158_01_C09）；细胞毒素支线：7 种 Naja 毒液（IC50 的 2 倍、1:5）→ **70–90% 保护**，分离细胞毒素 → 85%（n=3 复孔，mean±s.d.） |
| L11 致死剂量标定 | 毒素（α-cobratoxin、重组 ScNtx） | 雄性 non-Swiss albino 小鼠（20–30 g）腹腔注射，5 个剂量 × 每剂量 3 只，100 µl；观察 2 h 与 24 h | LD50 由 Quest Graph LD 50 Calculator 计算："For toxin LD 50 determination, five doses with three mice per dose were used, and a 100 µl bolus was injected intraperitoneally" | α-cobratoxin LD50 **0.098 µg g −1**、ScNtx **0.087 µg g −1**（与文献静脉值 0.1 µg g −1 相符）；攻击剂量定为 3×LD50（0.294 / 0.261 µg g −1） |
| L12 体内保护（疗效终点） | 3×LD50 毒素 + 对应 binder | 三种时序：预孵 30 min 后共注射；中毒后 15 min 给药；中毒后 30 min 给药。比例 1:10 与 1:5（毒素:binder），每组 5 只；另有非靶 binder 交叉处理与单给 binder 对照 | "three LD 50 values of the toxins (α-cobratoxin, 0.294 µg g -1 mouse; ScNtx, 0.261 µg g -1 mouse) were mixed with a ten-fold molar excess of their respective protein binders in PBS and incubated at room temperature for 30 min before intraperitoneal administration"；"Protection against lethality was measured as per cent mortality at 24 h" | **1:10 预孵：SHRT 100%、LNG 100%（各自靶）；+15 min 1:10：100%；+30 min 1:10：SHRT 100%、LNG 60%；+15 min 1:5：SHRT 100%、LNG 80%**；存活鼠无肢体/呼吸麻痹；分母＝**进入体内层的 2 个神经毒素设计**（每组 5 只） |
| L13 体内细胞毒素（失败层） | N. nigricollis（坦桑尼亚野生）毒液 63 µg 皮内 | CD1 雄性小鼠，吗啡 5 mg kg −1 预处理，毒液与 binder 按 1:1、1:2.5、1:5 预孵 30 min 后注射；72 h 取病灶，VIDAL 量面积 | "crude venom was preincubated (30 min at 37 °C) with varying cytotoxin:binder ratios of 1:1, 1:2.5 and 1:5 before injection"；"The outcome measured was the lesion size" | **无显著缩小**；N = 3（binder 组，pilot）/N = 5（毒液对照），共 17 只；原文明写"no further randomization was performed"、"No inclusion or exclusion criteria were used during the experiment, and all data points were used in the analysis"、"All experimenters were aware of the group allocation during the experiment and analysis" |

**这条链的顺序本身要记住**：结构自洽（L4，唯一有硬阈值的计算层）→ 几何功能预筛（L5，无阈值）→ 结合（L6/L7，实验）→ 生物物理与构象证实（L8/L9）→ 受体层面中和（L10）→ 剂量标定（L11）→ 活体保护（L12）→ 活体组织损伤（L13，失败）。**每一层换一次度量，层与层之间没有同一个量的连续预测**。

## 4. 关键数字台账（数值 · 含义 · 出处）

| 数值 | 含义 | 出处（原句片段／所在段落） |
|---|---|---|
| ~2,000 / 靶（两轮各一次） | RFdiffusion 生成骨架数；partial diffusion 再生成数 | Methods 的 De novo 3FTx binder design 段与 Partial diffusion 段各一句（本卡 L3、L7 行） |
| 10 与 20 / 共 50 步 | partial diffusion 加噪步数 | "The models were subjected to 10 and 20 noising time steps out of a total of 50 time steps in the noising schedule and subsequently denoised" |
| PAE < 10；pLDDT > 80；ddG < −40 | 唯一的三条定量计算阈值（两轮同一套） | Methods De novo 3FTx binder design 与 Partial diffusion 两段 |
| 44 → 1 | ScNtx 下单数 → 结合命中（Kd 842 nM，BLI） | Results Design of α-neurotoxin-binding proteins 第 1 段 |
| 78 → 11 | ScNtx 第二轮下单数 → 亲和力优于初 hit 的数目 | "11 of 78 designs had higher affinity than the initial hit" |
| 0.9 nM（SPR）/ 0.7 nM（BLI） | SHRT 最佳亲和力（两种读数） | "with the best (SHRT) having a binding affinity of 0.9 nM, as determined by surface plasmon resonance (SPR)"；"a very similar value of 0.7 nM was obtained by BLI" |
| 42 → 1（1.3 µM，BLI） | α-cobratoxin 第一轮下单数 → 命中 | "Of 42 RFdiffusion designs against α-cobratoxin, one candidate had a binding affinity of 1.3 µM using BLI" |
| 38 → 1（1.9 nM SPR / 6.7 nM BLI） | α-cobratoxin 第二轮下单数 → 最佳 LNG | "Partial diffusion optimization of the binding interface generated 38 designs"；"the highest affinity of which, LNG, had a K d of 1.9 nM, as measured by SPR"；"BLI yielded a value of 6.7 nM" |
| 86 | 用于构建细胞毒素共识序列的 UniProt 序列数 | "The resultant 86 unique CTX sequences were subjected to multiple sequence alignments in Clustal Omega" |
| 55 → 18 → 1 | 细胞毒素线：E. coli 表达数 → SEC 单体数 → 中和命中 CYTX | Results Design of cytotoxin-binding proteins |
| 271 nM / 740 nM | CYTX 对 N. pallida 细胞毒素 Kd（SPR）／CYTX_B10 变体 Kd | "The K d for the cytotoxin from N. pallida was determined to be 271 nM via SPR"；二硫键变体句 |
| 78 °C / >95 °C / 61 °C / 70.3 °C | SHRT / LNG / CYTX / CYTX_B10 熔解温度（CD） | Results 三段 + Methods Circular dichroism（升温 1 °C min −1，20→95 °C） |
| 2.58 Å · 1.04 Å；2.68 Å · 0.42 Å（binder）·0.61 Å（toxin）；2.0 Å · 1.32 Å · 0.58 Å | 三例晶体分辨率与对设计模型的 RMSD | Results 三处 crystal structure 句；PDB 9BK5/9BK6/9BK7 |
| ~100 aa | 设计蛋白规模（作者推测利于组织穿透） | Discussion："Their small size (approximately 100 amino acids) may enable them to penetrate rapidly into deep tissue" |
| 1:1（摩尔） | SHRT、LNG 在膜片钳里完全中和毒素的毒素:binder 比 | "When preincubated with ScNtx, the SHRT design achieved complete neutralization at a 1:1 molar ratio (toxin:binder), which was better than the previously characterized ScNtx nanobody (TPL1163_02_A01)" |
| 1:1、1:3、1:9、1:27 | 电生理剂量比梯度 | Methods electrophysiology 段 |
| 1:5 + 2×IC50 | 细胞活力法中和 7 种 Naja 毒液的条件 → 70–90% 保护；分离毒素 85% | "Preincubating CYTX with venom (two IC 50 values) at a 1:5 molar ratio (toxin:binder) provided 70–90% protection against venom-induced cytotoxicity"；"Similarly, preincubation of the cytotoxin binder with the isolated cytotoxin from N. pallida (two IC 50 values) at a 1:5 molar ratio (toxin:binder) provided 85% protection" |
| 70% | 把整毒摩尔数折成"细胞毒素当量"所用的假设（来自文献蛋白组，不是实测） | Fig 4c 图注："This ratio was estimated assuming that 70% of the whole venom consists of cytotoxins, on the basis of previous proteomic analyses"；正文："Immortalized human keratinocytes (N/TERTs) were exposed to venoms from seven different Naja species, which previous proteomic analyses suggested primarily consist (approximately 70%) of cytotoxins" |
| 0.098 / 0.087 µg g −1 | α-cobratoxin、ScNtx 小鼠腹腔 LD50（攻击量 3×＝0.294 / 0.261 µg g −1） | Results In vivo protection 第 1 句；Methods 体内保护段 |
| 5 剂量 × 3 只 | LD50 标定的动物数配置 | "For toxin LD 50 determination, five doses with three mice per dose were used" |
| 100% / 100% / 60% / 80% | 1:10 预孵保护；+15 min 1:10 救援；+30 min 1:10（LNG）；+15 min 1:5（LNG） | Results In vivo protection 段（n=5/组） |
| 100% / 60% | SHRT 在 +30 min（1:10）与 LNG 同条件的对比 | "Administering the SHRT binder 30 min after toxin injection also provided 100% protection against ScNtx, whereas the LNG binder conferred 60% protection" |
| 63 µg、17 只、N=3 / N=5 | 皮肤病变模型毒液量与分组（pilot） | Methods dermonecrosis 段："A venom-only control group of five mice received 63"；"In total, 17 mice were used"；"For sample size, N = 3 was used for groups receiving the cytotoxin binder because this was a pilot experiment" |
| n = 16、n = 3 复孔 | 电生理与细胞活力的重复数 | Methods electrophysiology；"Experiments were performed in triplicate, and the results are expressed as mean ± s.d." |
| **未报** | ① 通过 L4/L7 阈值的设计条数（计算漏斗分母缺失）；② 任何 GPU/CPU 秒、吞吐、单设计成本；③ PK/分布/半衰期；④ 与现有抗蛇毒血清的头对头效力比较 | 全文检索无对应表述（本卡按"原文未给"处理） |

## 5. 结论——作者说了什么

1. 深度学习从头设计可以**不经动物免疫、不建大文库**就做毒素结合蛋白："our in silico design approach avoids animal immunization and/or construction and several rounds of selection and/or screening of large libraries, providing a low-cost methodology for the rapid development of toxin binders to the many components of snake venom when structural or sequence data exist for these targets"。
2. 三个 3FTx 亚家族都拿到了结合体，且性质优越：热稳定（Tm 78 °C、>95 °C）、nM 级亲和、晶体结构与设计模型接近原子级吻合；摘要原句："With limited experimental screening, we obtained protein designs with remarkable thermal stability, high binding affinity and near-atomic-level agreement with the computational models"。
3. 体外与体内疗效："The designed proteins effectively neutralized all three 3FTx subfamilies in vitro and protected mice from a lethal neurotoxin challenge"；两个神经毒素结合体在 1:1 摩尔比完全中和、在 3×LD50 攻击下 1:10 给到 100% 保护（救援 15 min 也 100%），效力优于同文献里最好的纳米抗体与 IgG："Our designed neurotoxin binders demonstrate comparable potency to the best immunoglobulin G antibodies and nanobodies reported in the literature"。
4. 细胞毒素支线：体外中和 7 种 Naja 毒液（70–90%），但**作者明写体内皮肤病变模型未成功**、"The affinity of CYTX likely needs to be further optimized for full in vivo neutralization of cytotoxins."。
5. 方法学层面的收获（作者自评）："The unusual open fold of CYTX_B10 highlights the power of RFdiffusion to custom generate scaffolds shape-matched with protein targets"；以及"the crystal structure of our cytotoxin binder highlights the ability of RFdiffusion to custom design scaffolds to match almost any target shape and to generate binders to loop regions of proteins"、"The inhibitory activity of our anti-cytotoxin designs directly supports a hypothesized role for the cytotoxin loops in membrane disruption."
6. 定位与展望：现有抗蛇毒血清短期内仍是基石，设计蛋白可作**强化剂**（"our de novo designed binders could potentially be used as fortifying agents to improve the efficacy of antivenoms"），并可扩展到其他毒素（"RFdiffusion could be used to generate designs that neutralize other medically relevant toxins, expediting the formulation of antivenoms with broader species coverage"）；更宏观的主张是计算设计**降低治疗发现门槛**："Beyond snakebite, our results highlight how computational design could help democratize therapeutic discovery, particularly in resource-limited settings, by substantially reducing costs and resource requirements for the development of therapies for neglected tropical diseases"。
7. 作者**没有**说的：没有报告过滤通过率与计算成本；没有 PK/毒理学/免疫原性；没有与商用抗蛇毒血清头对头实验；没有做出跨短链/长链的单一泛中和体（两个 binder 各守各自靶）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的"证据链"不是同一个量的逐级放大，而是四次换度量**：结构自洽（PAE/pLDDT/ddG）→ 结合亲和力（BLI/SPR）→ 受体阻断（膜片钳）→ 活体生存（LD50 攻击）。每层的判据都不由上一层计算给出，所以**"计算预测结合"到"实际中和毒性"之间的因果桥是实验搭的，不是模型搭的**。
2. **计算侧的真实命中率在本文里不可复算**。可查的分母只有"下单数"（44 / 42 / 78 / 38 / 55），而 ~2,000 条生成设计经 PAE<10、pLDDT>80、ddG<−40 之后**剩多少没有报**。⇒ 1/44（≈2.3%）是**实验命中率**，不能被引成"计算漏斗命中率"或"设计成功率"；把它当计算能力用就是拿"下单口径"冒充"候选口径"。
3. **动物实验的命中分母只有 3 个设计（2 成 1 败），不是统计量**。进入体内层的对象是 SHRT、LNG、CYTX；神经毒素 2/2 达标、细胞毒素 0/1（皮肤病变）。每组 n=5（LD50 标定 5 剂量×3 只；病变组 N=3 且作者自称 pilot）、无随机化、不设盲、无纳入排除标准——这些原文都在 Methods 里明写。⇒ **"100% 保护"是个案展示级别，能证明"这条路可以打通"，不能证明"打通的概率"**。
4. **从 Kd 到给药剂量之间没有计算**。1:10、1:5 这些摩尔过量倍数是按经验搜索选的，与实测 nM 级 Kd 之间作者没给任何换算模型；而细胞毒素支线甚至要用"毒液 70% 是细胞毒素"这个来自文献蛋白组的**假设**才能定义摩尔比。⇒ 亲和力数字本身不足以决定疗效，**化学计量与暴露才是瓶颈，而这两项本文都没算**。
5. **第二轮 partial diffusion 是本文最可复用的工程动作，但它的收益无法预警**：11/78 优于初 hit 是实验测出来的，第一轮的结构自洽分数（同一套阈值）并不能指出哪些界面值得再采样。⇒ "再优化"这一步本质是把计算预算花在**局部重采样 + 少量下单**上，靠实验回读收敛。
6. **可表达性/单体性是漏斗里唯一"计算完全不管"的入口税**：细胞毒素线 55 表达 → 18 单体（≈33%），说明 PAE/pLDDT/ddG 对表达成败几无约束力；对下游实验设计预算来说，这一层的淘汰率比"结合命中率"更值得提前估。
7. **"泛覆盖"是设计假设而不是预测结果**：共识靶（86 条序列 → 1 条）带来跨毒液活性的说法，只有 7 种 Naja 毒液的细胞活力实验支持；而同一篇里短链/长链 binder 互不交叉中和，说明"设计一个共识体 → 得到家族级广度"这条推理链的中间环节（表位保守性与结合能）没有被任何计算检验。
8. **对我们项目的映射**：这篇是**计算少、 assay 多**的终点样本——计算只交付了**折叠与界面几何的自洽**，其余四个关键属性（亲和力、可表达性、中和效力、体内暴露）全部由湿实验补位。若我们的漏斗末端要宣称「预测到功能」，必须先回答「这一层的判据由谁给出」；UAA 合成酶课题里，**化学转化（产物身份）就是这里的 L10/L12 层，没有任何 binder 式代理量可以替代**。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自述/文中可见的**

1. 细胞毒素的体内疗效未达成：三种摩尔比都没缩小皮肤病变（"However, preliminary studies indicated that the CYTX design, in 1:1, 1:2.5 and 1:5 molar ratios (toxin:binder), did not significantly decrease the size of the dermonecrotic lesions induced by intradermal"），且被明确标注为 pilot（"For sample size, N = 3 was used for groups receiving the cytotoxin binder because this was a pilot experiment"）。
2. 动物实验的方法学强度有限（原文明写）：病变实验"no further randomization was performed"、"No inclusion or exclusion criteria were used during the experiment, and all data points were used in the analysis"、"All experimenters were aware of the group allocation during the experiment and analysis"；生存实验每组 5 只、终点只有 24 h 死亡率。
3. 前提条件限定：整套低成本主张只在有结构/序列数据的靶上成立（"providing a low-cost methodology for the rapid development of toxin binders to the many components of snake venom when structural or sequence data exist for these targets"）。
4. 机制性属性未测：小尺寸利于深部组织穿透只是推测（"Their small size (approximately 100 amino acids) may enable them to penetrate rapidly into deep tissue"），全文无 PK、分布、半衰期、免疫原性、给药剂次/多次给药数据；与商用抗蛇毒血清无头对头比较。
5. 只覆盖 3FTx 一个毒素家族：PLA2、金属蛋白酶、丝氨酸蛋白酶等致死/出血组分本文没有设计（体内实验里 PLA2 靶向纳米抗体只作为阴性对照出现）。
6. 跨亚家族广度没做到：短链与长链 binder 互不中和非靶毒素，所谓"泛蛇毒中和剂"目前只能是组合，作者在 Discussion 里也把它列为后续（"RFdiffusion could be used to generate designs that neutralize other medically relevant toxins, expediting the formulation of antivenoms with broader species coverage"）。

**我们读出的**

1. **漏斗中段是黑箱**：两轮各 ~2,000 条设计经 PAE<10 / pLDDT>80 / ddG<−40 之后各剩多少，全文没有报；也没有任何算力/成本数字。⇒ 无法做"每 GPU 秒换多少命中"的效率核算，也就无法把这篇与其他 Baker 线论文在同口径下比较。
2. **亲和力读数依赖固定化方式**：SHRT 0.9 nM(SPR) vs 0.7 nM(BLI)、LNG 1.9 nM(SPR) vs 6.7 nM(BLI)，同一分子两种技术差 2–3.5 倍；论文把 SPR 值放在主图、BLI 值放补充材料，**没有统一的 Kd 口径声明**。引用时只该说「低 nM 级」，不该精确到 1.9 nM 当成可比数。
3. **结构验证只覆盖成功者**：三例晶体（9BK5/9BK6/9BK7）全是被选中的最优设计；失败的 43/41/54 条设计没有任何构象层面的实验信息，所以"Type II 型失败"在这篇里无法定量。
4. **共识靶的"保守表位"假设没有被检验**：共识序列只按逐列最频氨基酸/共识符号构造（序列层面），没有结合能或结构保守性分析，广度全靠后实验的 7 种毒液活力测定；70% 细胞毒素占比也是取自文献蛋白组的假设值。
5. **中和效力与致死保护之间仍缺一层定量**：膜片钳给出 1:1 完全阻断，但体内用的是 1:10（部分场景 1:5），两者之间没有剂量-暴露关系的推导或测量；换句话说，**这篇证明了"能保护"，没有证明"为什么这个剂量能保护"**。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **把"疗效"拆成有名字的层，每层单独报分母与判据**。本文的 L4（结构自洽）/L6–L7（结合）/L8（可表达）/L10（受体阻断）/L12（活体保护）是一条可照抄的记账模板：我们的漏斗对应成 **S-折叠/表达 → S-结合底物 → S-化学转化（LC-MS 产物身份）→ S-转化率或产量提升**，每一层必须写清"分母是谁给的"（生成数 / 过滤通过数 / 下单数 / 表达成功数），并允许写 UNKNOWN 与 METHOD_FAIL。
2. **"功能预筛用几何而非能量"这一招可以搬**。作者判断"会不会中和"用的是与受体复合物叠合看位阻，没有任何能量阈值——对应我们：**催化几何判据（供体原子与靶原子的距离/角度）本质上也是几何层**，可以当"值得下单"的排序量，但必须像本文一样承认它不预测幅度。
3. **局部重采样（partial diffusion）式的第二轮**：先小预算生成、下单、把实验读数回灌到"最优点的邻域"再采样一次。这条对我们的机制层很实用——**在已审计的活性位点构象上做小范围扰动，比整库重跑更省核时**，而且本文证明第二轮确实能把 842 nM 推到 0.9 nM（尽管不可预警）。
4. **共识/代表序列降维**：86 条序列 → 1 条共识体，把一个家族级问题变成一个单结构问题。对我们：家族级候选可先归约到"代表成员 + 决定列"，但必须像本文一样，**广度只在实验层声明**（本文是 7 种毒液），不许从共识构造本身推出覆盖度。
5. **阴性的诚实记账**：皮肤病变模型只有 N=3 且明写 pilot、明写未随机化未设盲——这种"将失败与配置一起交付"的写法正是我们判定卡该有的格式（判据 + 样本量 + 未解决）。

**不可迁移（为什么不能照搬）**

1. **PAE<10 / pLDDT>80 / ddG<−40 是"会不会按设计结合"的阈值，不是"会不会催化"的阈值**。这三个量里没有底物、没有过渡态、没有竞争副产物；UAA 合成酶的成功要同时满足三步化学事件（起始/pppUA 桥接/环化竞争），**结构自洽既不必要也不充分**。项目 DP2R 判定标准明令禁止把 binder 的 pAE/ipTM 类阈值当酶活闸口使用，本文再一次给出理由：连作者自己都不能用这些分数预测亲和力谁高谁低（要靠 11/78 的实验回读）。
2. **本文任何命中率都不能换算成我们的成功概率**。可引用的是口径而非数值：44 下单 → 1 结合、18/55 单体可用、3 个设计进动物 → 2 个成功；分母极小、无重复队列、且度量对象是"静态结合与外源毒素化学计量中和"。我们的目标连一层真值标签都没有，**"这篇做到 100% 保护"对我们不构成任何概率含义**。
3. **治疗终点与酶活终点在物理上不同**：蛇毒中和可以靠**给到 10 倍摩尔过量的结合剂**解决（毒素是外源、定量的），UAA 供给要在细胞内跑赢内源代谢、浓度不可自由调；本文"1:10 比例即疗效"这类设计在酶发现里没有对应杠杆。
4. **本文无 MD / 无 QM / 无自由能**：它不能为"用 MD/QM 判催化"提供任何方法资格或命中率参照；这类主张的参照物要在别处找（本文不提供）。
5. **通量结构不同**：他们的湿实验是"几十条设计逐个分选/表达"（96 孔自动化、单设计分选），我们一轮最多几个构建体且必须靠机制多样性 + 失活对照来最大化信息量。照搬他们"多下单几十条"的容错预算会直接耗尽我们的湿实验额度。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/snakvenom2025.txt

- **本卡全部英文引句只从这一份底稿复制粘贴**（该文件是 PMC11882462 的去标签纯文本抽取，68,787 B / 142 行，SHA-256 `0d2dd174b172c66c58b3168dc348d29c7d44afb6272af1525e5422f3e9b4875c`；文件首行身份头含 PMCID/PMID/DOI/标题，与 CSV 行 B43 一致，故未挂错行）。同一篇论文若另有 Europe PMC / NCBI 的其它抽取版本，本卡不以其为准。
- 底稿里的排版残留已按门禁 `litcards_text.norm()` 的口径处理：HTML 实体（`&lt;`、`&gt;`）在比对时解码为 `<`、`>`；U+2212 负号归一为 `-`；连续空白折叠为单空格（所以 `N  =  3`、`T m`、`K d`、`N.   pallida` 在卡里写成单空格形式）；含 U+2010（如正文若干处 `α‐cobratoxin`）的句子本卡一律避开或截到该字符之前，故不引这些句。
- 对照底稿：`sources/baker.md:565–577`（本编号的旧卡段落，其中第 575 行摘录了 44/1/78/38/55/18 等命中率原始句，与本卡一致）。**另需登记一处口径问题**：CSV 行 44 的 `候选数递减` 字段把第二轮写成"partial diffusion 生成 38/78 设计"，未区分支线；正文口径是 ScNtx 第二轮下单 **78** 条、α-cobratoxin 第二轮下单 **38** 条，本卡按正文分列（本卡不改 CSV，只在此登记）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计引用`；第 6–8 节 ↔ `在方法演进链的位置`。
- **门禁自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B43 --no-report`（输入：本目录卡片 + `sources_map.json` 中 B43 登记的底稿），结果见本次回报与 `data/literature_cards/rollout_status.tsv`（他人产物未被本代理覆盖，因带 `--no-report`）。
- **本卡不能证明的事**：过滤层通过数、算力成本、PK/毒理、与商用抗毒血清的比较——正文没有，本卡一律写"原文未给/未报"，不做估算。

<!--CSV回填
work_type=论文
target=3FTx 家族三个亚家族：短链 α-神经毒素共识体 ScNtx、长链 α-神经毒素 α-cobratoxin（Naja kaouthia，UniProt P01391）、IA 型细胞毒素共识序列（86 条 UniProt 序列）；疗效对象另含 7 种 Naja 属整毒液
backbone_generation=RFdiffusion 以 [L,4] 二级结构 one-hot + [L,L,3] 块邻接 one-hot 条件生成（两种模式：与设计 β-strand 和靶边缘 β-strand 配对；或在毒素三指环上设 hotspot 残基），每靶约 2,000 条骨架；序列由 ProteinMPNN 给出并经 Rosetta FastRelax 松弛；第二轮用 partial diffusion（50 步噪声计划里加噪 10/20 步再去噪）对最优界面再采样，每靶再约 2,000 条
computational_filters=AF2 + initial guess 单序列结构预测给出的界面 PAE 与 pLDDT；Rosetta ddG（界面ΔΔG）；binder–target β-片层延伸几何（张量条件本身）；与毒素–nAChR 复合物叠合判断位阻阻断（人工/几何，无定量分数）。不含 MD、不含 QM、不含结合自由能
thresholds=AF2 PAE < 10；pLDDT > 80；Rosetta ddG < -40（第一轮与 partial diffusion 第二轮同一套）；功能（位阻）预筛原文未给阈值；过滤后通过条数原文未报；体外中和判据为 1:1 摩尔比完全阻断 ACh 响应；体内攻击剂量 3×LD50、给药摩尔比 1:10 与 1:5；病变模型毒素:binder 1:1、1:2.5、1:5
md_used=否（全文无分子动力学）
qm_used=否（全文无量子化学/反应能垒计算；亲和力与催化均非计算所得）
experimental_methods=酵母表面展示 + 96 孔自动进样流式逐设计分选；BLI；SPR（异质配体拟合）；E. coli/Hi5 之外的可溶表达 + SEC 单体判定；CD 熔解测 Tm；X 射线晶体学与分子置换（PDB 9BK5/9BK6/9BK7）；RD 细胞平面膜片钳（n=16）；HEK293T 与 N/TERT 发光细胞活力中和（3 复孔）；小鼠 LD50 标定与腹腔攻击的存活/救援实验；小鼠皮内毒液致皮肤坏死模型（VIDAL 量病灶）
pipeline_counts=每靶约 2,000 计算设计 →（阈值过滤通过数未报）→ 下单 44（ScNtx）与 42（α-cobratoxin）→ 各得 1 个结合体（842 nM、1.3 µM）→ 第二轮约 2,000 → 下单 78（ScNtx）与 38（α-cobratoxin）→ 11/78 亲和力优于初 hit → SHRT 0.9 nM、LNG 1.9 nM；细胞毒素支线 55 条 E. coli 表达 → 18 条单体进中和实验 → 1 条 CYTX（271 nM）；进动物层的设计共 3 个（SHRT/LNG/CYTX）；动物规模：LD50 标定 5 剂量×3 只、保护实验每组 5 只、病变模型 binder 组 N=3 与毒液对照 N=5 共 17 只
hit_rate=下单层面 1/44（约 2.3%，ScNtx）与 1/42（α-cobratoxin）；第二轮 11/78 亲和力提升；可表达层面 18/55（约 33%）为单体；细胞毒素中和 1/18；活体保护层面进入 3 个设计、神经毒素 2/2 达 100% 保护（1:10 预孵与 +15 min 救援；+30 min 时 SHRT 100%、LNG 60%；1:5 时 SHRT 100%、LNG 80%），细胞毒素皮肤病变 0/1（本文未解决）。注意：这些是实验/下单口径，不是计算漏斗命中率（过滤分母未报）
best_metric=SPR Kd 0.9 nM（SHRT 对 ScNtx；BLI 平行读数 0.7 nM）与 1.9 nM（LNG 对 α-cobratoxin；BLI 6.7 nM）；Tm SHRT 78 °C、LNG >95 °C、CYTX 61 °C、CYTX_B10 70.3 °C；晶体与设计模型 RMSD 1.04 Å（SHRT apo）、0.42 Å binder/0.61 Å toxin（LNG 复合物）、1.32 Å/0.58 Å（CYTX_B10）
cost_or_stat_note=全文未报计算成本（无 GPU/CPU 秒、无过滤通过率、无吞吐），湿实验通量为自述的 limited experimental screening（44/42/78/38/55 条设计逐条测，不是文库）；动物统计配置：每组 n=5、每组未做随机化与盲法（原文明写 no further randomization was performed、experimenters were aware of group allocation）、病变组 N=3 自称 pilot、无纳入排除标准；Kd 读数依固定化方式不同（同一分子 SPR 与 BLI 相差 2–3.5 倍）
role_in_timeline=Baker 管线里第一个把 de novo 结合蛋白推到体外中和 + 致死攻击活体保护的治疗学终点样本；计算侧沿用 [B09] 的 AF2 结构自洽闸口口径（PAE/pLDDT）并加 Rosetta ddG，但不再做大规模湿实验标注考卷，因此该文对漏斗的贡献是证据链分层示范（结构自洽 → 结合 → 可表达 → 受体阻断 → 活体保护）与局部重采样（partial diffusion）这一低成本再优化动作，而不是新的判别量
source_pointer=data/interim/baker_lit/ft/snakvenom2025.txt（PMC11882462 去标签全文，SHA-256 0d2dd174b172c66c…，见第 0 节身份复核）；对照旧卡 sources/baker.md:565-577；DOI 10.1038/s41586-024-08393-x
CSV回填-->
