# [B28] LigandMPNN——把「非蛋白原子」当成序列设计器的输入，让序列端第一次能看见配体

Dauparas J, Lee G R, Pecoraro R, An L, Anishchenko I, Glasscock C, Baker D（华盛顿大学 Biochemistry / Institute for Protein Design / HHMI）
Nature Methods 2025, 22:717–723 · DOI 10.1038/s41592-025-02626-1 · PMID 40155723 · PMCID PMC11978504
开放获取（CC BY 4.0）· 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11978504/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B28**（组：Baker组；文献类型：方法） |
| 本文取回方式 | Europe PMC `fullTextXML`（HTTP 200，125,708 B，记 `OK ok`），2026-10-20 本地抓取；见 `data/literature_cards/fetch_log.tsv` 的 B28 行 |
| 本地全文 | `data/literature_cards/fulltext/B28_PMC11978504_fullTextXML.xml`（SHA-256 `7e33fb90a1f61701…`）与归一化纯文本 `data/literature_cards/fulltext/B28_PMC11978504_text.txt`（57,853 B / 归一后 56,924 字符） |
| **证据级别升级说明** | `inventory.tsv` 与 CSV 的 `证据级别` 字段仍写「摘要级」——那是 2026-10-16 建库时的状态（当时只取到 PubMed 摘要，`sources/baker.md` 因此只能引摘要里的数字）。**本行 `batches.tsv` 的 state 是 FULLTEXT**，本卡按全文写；旧底稿里那条摘要级引句（63.3% versus 50.4% and 50.5% 那一串）在本卡里改成全文原句后**顺序不同**（全文正文口径是 Rosetta 50.4 / ProteinMPNN 50.4，摘要口径是 50.4 and 50.5），见第 7 节第 1 条 |
| 对照底稿 | `sources/baker.md` 第 368–379 行（原卡，摘要级）；本卡补齐：模型三张图的确切构造、25 最近原子与 0.1 Å 噪声的选择理由、全部消融数字、侧链打包模型的分布形式、以及本文**唯一两处真湿实验**（rocuronium 与 cholic acid）的实际设计与样本量 |
| 证据级别 | **全文级**（本卡引句均可在本地全文里逐字命中；见第 9 节自检） |
| 未取到的部分 | Supplementary Figs 1–8、Source Data Figs 2/3/4、Methods 里没有给的送测条数与命中数（本文**本身没有前瞻实验漏斗**，只重设计了别人已测过的失败设计）、以及被引文献 3–5 的内部数据。凡依赖处本卡明写「本文未给」 |

## 1. 这篇到底解决什么（大白话）

[B05] 的 ProteinMPNN 已经把「给一个骨架配一条会折成它的序列」做成了 1 秒钟的事，但它的输入**只有蛋白骨架坐标**：小分子、DNA/RNA、金属离子在它眼里不存在。于是凡是要设计「跟非蛋白原子打交道」的界面——酶活性位点、小分子结合体、传感器、核酸结合蛋白——就只能退回 Rosetta 的侧链打包 + 蒙特卡洛，慢、要为新化合物手工写参数、而且容易被骨架弛豫牵走。

这篇的做法：**给 ProteinMPNN 加两条处理「配体图」的编码层**，让每个残基在做序列决策时能看到它周围最近的配体原子（元素类型 + 距离 + 相对骨架坐标架的角度），顺带再训一个同架构的网络直接吐**侧链构象**（四个二面角的分布，而不只是氨基酸种类）。结果：配体 5 Å 内的天然序列回收率从 Rosetta 与 ProteinMPNN 的 ~50% 提到 63.3%，核酸从 ~35% 提到 50.5%，**金属从 ~36–40% 提到 77.5%**；比 Rosetta 快约 250 倍；并且它已经作为部件被组内多篇论文用掉（>100 个实验验证的结合界面、5 个共晶结构），本文还现场演示**把两个原本「完全不结合/结合极弱」的 Rosetta 小分子设计用 LigandMPNN 重设计后结合回来了**。

一句话定位：**这是序列端的全原子化**。它不改变骨架怎么生成、不改变怎么筛，只把「配体在这里」这件事交进序列设计器。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **根本障碍：现有深度学习序列设计器看不见非蛋白原子**。原话："current state-of-the-art deep-learning-based sequence design methods are unable to model nonprotein atoms and molecules"，并且点名 ProteinMPNN 的输入边界："ProteinMPNN explicitly considers only protein backbone coordinates while ignoring any other atomic context"，而这件事恰恰是所有功能相关界面的核心（"which is critical for designing enzymes, nucleic-acid-binding proteins, sensors and all other protein functions involving interactions with nonprotein atoms"）。 **应对**：不重造架构，只**最小扩展** ProteinMPNN——增加蛋白–配体图与配体内图，并加两条编码层："We experimented with introducing two additional protein-ligand encoder layers to encode protein-ligand interactions"，代价被量化为参数量 1.66M → 2.62M、单条 100 残基推理 0.6 s → 0.9 s（同一颗 CPU）。
2. **训练数据天生少**（PDB 里有配体的复合物远少于 apo 蛋白），作者开工前心里没底："At the outset, we were unsure whether the accuracy of ProteinMPNN could extend to protein-ligand systems given the small amount of available training data, but our results suggest that, for the vast majority of ligands, there are sufficient data." **应对**：①按化学类型**分域评测**（小分子 / 核酸 / 金属三套分别报），而不是给一个平均回收率；②把「数据不够时会怎样」写成一个具体的使用规则（见第 2.5 条），并把「物理法与深度学习法混合」留作低数据区的出路："Hybridization of the physically based and deep-learning-based approaches may provide a better solution to the amino-acid and sidechain optimization problems in the low-data regime."
3. **配体原子太多、图会爆炸，而且远处原子本就不该影响选择**。 **应对**：用物理尺度决定邻域半径并把它写成假设："We reasoned that, with the backbone and ligand atoms fixed in space, only ligand atoms in the immediate neighborhood (within ~10 Å) would affect amino-acid sidechain identities and conformations because the interactions (van der Waals, electrostatic, repulsive and solvation) between ligands and sidechains are relatively short range"，实现上取「按 virtual Cβ 到配体原子距离排最前的 25 个原子」："We obtained the best performance by selecting for the protein-ligand and individual residue intraligand graphs the 25 closest ligand atoms based on protein virtual Cβ and ligand atom distances"。**留下的代价**：消融显示减少每残基的 context 原子数"Decreasing the number of context atoms per residue primarily diminished sequence recovery around nucleic acids, probably because these are larger and contain more atoms on average than small molecules and metals"——也就是 25 这个数对核酸这类大配体是**勉强够用**，不是安全值。
4. **网络会「背」晶体结构里的天然序列**（骨架坐标里已被精修程序写进了侧链信息）。 **应对**：加高斯噪声，并把理由讲透："we wanted our models to work well with novel protein backbones as opposed to crystal backbones, and for this reason, we added Gaussian noise to all the protein and other atom coordinates to blur out fine-scale details that would not be available during the design"；正文另有一句说得更直接：晶体精修会把天然序列的记忆写进局部骨架（"crystal structure refinement programs introduce some memory of the native sequence into the local backbone"），基线模型用 0.1 Å。**关键的一条口径纪律**：噪声会同时改变所有方法的读数，所以 "when comparing performance across methods, similar levels of noising must be used"——并为此专门重训了 ProteinMPNN："For fair comparison, we retrained ProteinMPNN on the same training dataset of PDB biounits as LigandMPNN"，"except none of the context atoms was provided during training"。**留下的代价**：噪声大小本身是可调旋钮，实测 0.05 Å / 0.2 Å 让回收率分别升降约 2%（"Training with 0.05 Å and 0.2 Å noise instead increased and decreased sequence recovery by about 2%, respectively"），因此不同论文之间这类数字不可直接比。
5. **新化合物没有力场参数**（Rosetta 的老问题）——作者把它列为「易用性」收益而不是自己的难点："The method is also easier to use because no expert customizations are required for new ligands (unlike Rosetta and other physically based methods that can require new energy function or force field parameters for new compounds)." 但反过来遇到**训练集里几乎不存在的元素**时，网络也没辙。**应对**：给出一条明确的边界与土办法："Nevertheless, we suggest some care in using LigandMPNN for designing binders to compounds containing elements occurring rarely or not at all in the PDB (in the latter case it is necessary to map to the most closely occurring element)."——至于这条「把陌生元素映射成最接近的已见元素」的做法本身有没有验证，本文未给（我们的判断，不是作者原话）。
6. **元素身份到底有没有被用起来？**（怕网络只是靠几何形状猜）。 **应对**：做消融并给出分域差异："Finally, a model trained without chemical element types as input features had much lower sequence recovery near metals" 但对小分子与核酸几乎不变，作者由此推断"the model can to some extent infer chemical element identity from bonded geometry"。同类处理还有两处：把蛋白–配体图与配体内图整个砍掉 → "Ablating the protein-ligand and ligand graphs led to a 3% decrease in sequence recovery"；只用侧链原子当 context（完全不给小分子/核酸/金属）→ "Training on sidechain context atoms only (no small molecules, nucleotides or metals) reduced sequence recovery around small molecules by 3.3%"。**留下的代价**：这些增益是**个位数百分比**，与金属位那种 77.5% vs 36.0% 的量级差不同，说明「配体条件化」的收益高度依赖化学类型。
7. **想让功能位点「保持原样」但没有这个入口**（设计时常常要锁住几个催化残基，但周围残基要重排）。 **应对**：训练时随机挑 2–4% 残基把**它们自己的侧链原子当配体上下文**："We augmented the training dataset by randomly selecting a small fraction of protein residues (2-4%) and using their sidechain atoms as context ligand atoms in addition to any small-molecule, nucleotide and metal context."。作者诚实承认这一招对回收率没用——"Although this augmentation did not significantly increase sequence recoveries"——真正的目的是打开一个接口："training in this way also enables the direct input of sidechain atom coordinates to LigandMPNN to stabilize functional sites of interest"，正文另一处对应 "Providing sidechain atoms as additional context did not significantly affect LigandMPNN performance"。**这是「实验不涨点但保留机制入口」的一个干净例子。**
8. **只要序列不够用，还需要侧链到底怎么摆**。 **应对**：用同一套架构再训一个侧链打包网络，输出概率分布而非单一构象："We also trained a sidechain packing neural network using the basic LigandMPNN architecture to predict the four sidechain torsion angles for each residue following the sequence design step"，具体形式是三成分圆正态混合（"The model predicts a mixture (three components) of circular normal distributions for the torsion angles (chi1, chi2, chi3 and chi4)."），并且按 chi1→chi2→chi3→chi4 自回归分解（"We autoregressively decompose the joint chi angle distribution by decoding all chi1 angles first, then all chi2 angles, chi3 angles and finally all chi4 angles"）。**留下的代价（作者直写）**："All the models struggle to predict chi3 and chi4 angles correctly."（小分子集上 LigandMPNN 的 chi1–chi4 加权正确率 84.0%/64.0%/28.3%/18.7%，Rosetta 74.5%/50.5%/24.1%/8.1%）——长侧链的远端二面角基本没学会。
9. **侧链打包这一项，配体条件化的增益其实很小**——这是个「自己的卖点在自己指标上不显著」的坑。 **应对**：不藏，直接写出来并给出解释：chi1 回收率对 Rosetta 明显更好，但相对去掉配体上下文的 LigandMPNN-wo 只有边际优势（"but only marginally better than LigandMPNN-wo"），作者的解释是："suggesting that most of the information about sidechain packing is coming from the protein context rather than from the ligand context, consistent with binding site preorganization"；同时把增益集中在化学上说得通的位置类型上（"the biggest improvements in terms of root-mean-square deviation are obtained for glutamine (Q) in the small-molecule dataset, for arginine (R) in the nucleotide dataset and for histidine (H) in the metal context dataset"，并注 "consistent with the important roles of interactions of these residues with the corresponding ligands"）。
10. **「会不会只是拟合训练分布」这一问，用一个可证伪的实验回答**。 **应对**：拿**训练集里根本不存在的配体类别**做重设计——"We tested the capability of LigandMPNN to design binding sites for small molecules starting from previously characterized designs generated using Rosetta that either bound weakly or not at all to their intended targets: the muscle relaxant rocuronium, for which no binding was previously observed" 与结合很弱的 cholic acid；并把泛化的理由写实："these results indicate significant generalization beyond the PDB training set: there were no rocuronium-binding protein complex structures in the PDB training set"，对胆酸还给了结构距离："the cholic-acid-binding protein in the PDB that is closest to our cholic-acid-binding design (PDB: 6JY3 ) has a quite different structure (template modeling score 0.59)"，并点明结合位点位置完全不同。**留下的代价**：这个「泛化证据」的湿实验规模极小（图注写 "The error bars show the mean and standard deviations for three LigandMPNN and two Rosetta measurements."），见第 7 节。
11. **本文自己的实验只能救「别人失败的旧设计」，没有前瞻漏斗**。 **应对（其实是自我定位）**：把验证责任分给组内已发表的项目，并说明两种用法："In these studies, LigandMPNN was either used as a drop-in replacement for Rosetta sequence design retaining the backbone relaxation of RosettaFastDesign"，或 "or used independently without backbone relaxation"；累计口径写成 "more than 100 protein-DNA binding interfaces and protein-small-molecule binding interfaces designed using LigandMPNN have been experimentally demonstrated to bind to their targets, and 5 co-crystal structures have been solved that in each case are very close to the computational design models"，并单独点名 DNA 那个共晶："The crystal structure of a DNA-binding protein designed with LigandMPNN recapitulated the design model closely"（PDB 8TAC，即 [B27]）。**本文未解决**：没有前瞻的「按新方法设计 → 下单 → 命中率」实验，因此**没有本文自己的命中率数字**。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **主干：MPNN（ProteinMPNN 的 encoder/decoder 原样复用）**——"We used the same MPNN architecture as used in ProteinMPNN for the encoder, decoder and protein-ligand encoder blocks"。选它的理由是能直接继承已被验证的性质（随机自回归解码、能设计对称与多状态蛋白）。
- **新增三张图**：①蛋白图（残基为节点，N/Cα/C/O/virtual Cβ 两两距离为边）；②配体内图（原子为节点，元素类型 one-hot + 原子间距离为边，每个残基的最近邻配体原子全连接）；③蛋白–配体图（残基 × 配体原子的距离与角度特征）。消息传递方向是「先在配体图里更新、再把信息经蛋白–配体边喂回残基」。
- **virtual Cβ**：由 N/Cα/C 骨架坐标线性组合推出来（算法 10 里给了系数），为的是甘氨酸也有一个代表侧链方向的点。
- **侧链打包网络**：同架构、输出 4×3 的圆正态混合参数（混合系数/均值/方差）。
- **评测方式**：native sequence recovery（回收天然氨基酸）+ chi 角回收率/侧链 RMSD + 预测置信度与真实回收的相关性。
- **实验方式（本文内）**：酵母表面展示 + 流式（rocuronium，1 μM 生物素化 rocuronium + SAPE）与荧光偏振竞争（cholic acid-FITC），对象是**已有的 Rosetta 失败/弱设计**。
- **没有用的方法**：MD、QM、自由能。全文无系综、无反应坐标、无电子结构；作者留下的只是展望——"As with ProteinMPNN, we anticipate that LigandMPNN will be widely useful in protein design, enabling the creation of a new generation of small-molecule-binding proteins, sensors and enzymes."，而展望不是验证。

### A. 造模型（训练侧）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | PDB 复合体（截至 16 December 2022） | 取 X 射线或冷冻电镜结构，删去溶剂/常见离子后按链聚类，划出互不重叠的测试集 | 分辨率 "determined by X-ray crystallography or cryo-electron microscopy to better than 3.5 Å resolution and with a total length of less than 6,000 residues"；剔除清单 "We parsed all residues present in the PDBs except" 后面五项（HOH, NA, CL, K, BR）；聚类 "The train-test split was based on protein sequences clustered at a 30% sequence identity cutoff." | 留出集："We held out a nonoverlapping subset of proteins that have small-molecule contexts (a total of 317), nucleotide contexts (a total of 74) and metal contexts (a total of 83)." |
| A2 | 每个复合体 | 造三种图 + 特征：残基–残基 K 近邻（按 Cα–Cα），每残基取最近的 M 个配体原子 | 元素类型用 one-hot（另拼化学基团/周期表分组，线性层到 64/147 维），距离用径向基函数 rbf（r = 16），角度用相对 N-Cα-C 坐标架的 sin/cos；配体原子数按 A4 消融定为 25 | 归一化后的节点/边张量：蛋白 [N] 与 [N,K]、配体 [N,M] 与 [N,M,M]（配体内全连接） |
| A3 | 特征 | 加高斯噪声后再训 | 标准差 0.1 Å（蛋白与 context 原子都加）："Protein and context atoms were noised by adding 0.1 Å standard deviation Gaussian noise to avoid protein backbone memorization"；另加 2–4% 残基的侧链原子当伪配体做数据增强 | 一个能吃的「非设计态骨架 + 配体」混合训练分布 |
| A4 | 训练集 | 训序列模型 + 侧链打包模型 | "Models were trained with a batch size of 6,000 tokens, automatic mixed precision and gradient checkpointing on a single NVIDIA A100 graphics processing unit for 300,000 optimizer steps."；"For optimization, we used Adam with beta1 of 0.9, beta2 of 0.98 and epsilon of 1e-9, the same as for ProteinMPNN."；损失 "We used categorical cross entropy for the loss function following the ProteinMPNN paper" | 2.62M 参数模型（"the LigandMPNN neural network has 2.62 million parameters compared with 1.66 million ProteinMPNN parameters."）；推理 "ProteinMPNN 0.6 s and LigandMPNN 0.9 s on a single central processing unit for 100 residues), scaling linearly with respect to the protein length" |
| A5 | 训好的模型 | 逐 metaparameter/特征做消融与变化 | 评测口径固定为「侧链原子距任一非蛋白原子 5.0 Å 内的残基」："We determined the native amino-acid residue sequence recovery for positions close to the ligand (with sidechain atoms within 5.0 Å of any nonprotein atoms)." | 5 条消融结论（配体原子数、侧链 context、噪声、砍图、砍元素类型），全部写进第 2.3/2.4/2.6/2.7 条 |

### B. 评测（计算侧）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 317 / 74 / 83 三个留出集 | 每个蛋白设计 10 条序列，算近配体残基的天然回收率 | "The median sequence recoveries (ten designed sequences per protein)"；对照组是同一训练集重训的 ProteinMPNN 与 Rosetta（小分子用 genpot 能量函数，核酸用为蛋白-DNA 界面优化过的能量函数，金属那一档正文只写 Rosetta 并在其后紧跟引文编号） | 小分子 63.3%（LigandMPNN）对 50.4%（Rosetta）/50.4%（ProteinMPNN）；核酸 50.5% 对 35.2%/34.0%；**金属 77.5% 对 36.0%/40.6%** |
| B2 | 同上 | 逐蛋白比较（而非只看均值）+ 检查置信度是否可用 | "Sequence recoveries were consistently higher for LigandMPNN over most proteins in the validation dataset"；并指出蛋白间表现相关，"performance was correlated, probably reflecting variation in the crystal structure and the amino-acid composition of the site" | Fig 2b 的逐蛋白散点；"the expected confidence correlates with the actual sequence recovery accuracy"（Fig 2c 口径） |
| B3 | 同一批蛋白 | 固定骨架与配体，各生成 10 个侧链打包样本，比 Rosetta / LigandMPNN / LigandMPNN-wo | "We generated ten sidechain packing examples with the fixed backbone and fixed ligand context using Rosetta, LigandMPNN and LigandMPNN without ligand context"；命中定义 "The median chi1 fraction (within 10° from crystal packing) near small molecules was 76.0% for Rosetta, 83.3% for LigandMPNN-wo and 86.1% for LigandMPNN" | chi1：小分子 86.1 vs 76.0（Rosetta）、核酸 71.4 vs 66.2、金属 79.3 vs 68.6；chi1–chi4 加权 84.0/64.0/28.3/18.7%（LigandMPNN）对 74.5/50.5/24.1/8.1%（Rosetta）；侧链 RMSD 各方法接近 |

### C. 本文的两处湿实验（救旧设计，非前瞻漏斗）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | Rosetta 做出的、**此前完全不结合**的 rocuronium 设计 | 保留骨架与配体坐标，只用 LigandMPNN 重新出结合位点序列，让新侧链保留/引入与配体的氢键 | 判据是酵母表面展示结合信号：用 1 μM 生物素化 rocuronium + SAPE 染色后流式（"flow cytometry of yeast is shown, with the designs following incubation with 1 μM biotinylated rocuronium and streptavidin phycoerythrin"）；重设计前后再看侧链预组织（LigandMPNN 氨基酸概率，红 0 → 蓝 1） | "LigandMPNN redesigns either rescued binding"；样本量按图注：3 个 LigandMPNN 测量与 2 个 Rosetta 测量 |
| C2 | Rosetta 做出的、**结合很弱**的 cholic acid 设计 | 同上重设计 | 荧光偏振：测 cholic acid-FITC 的结合（"fluorescence polarization measurements of binding to cholic acid-fluorescein isothiocyanate are shown"） | 结果是提高结合亲和力；更强的 100 倍来自另一篇论文里「从已解析复合物出发重设计」的例子："where, starting from the crystal structure of a previously designed complex, LigandMPNN increased binding affinity 100-fold"（本文把它作为引文证据而非自有测量） |
| C3 | 组内已发表的多项设计工作 | 汇总 LigandMPNN 在真实项目里的用法与验证 | 用法两档：替换 Rosetta 序列设计但保留骨架弛豫 / 独立使用不弛豫骨架 | "more than 100 protein-DNA binding interfaces and protein-small-molecule binding interfaces designed using LigandMPNN have been experimentally demonstrated to bind to their targets, and 5 co-crystal structures have been solved that in each case are very close to the computational design models"；点名 [B27] 的 DNA 结合蛋白共晶（8TAC）与三类小分子结合体系（17α-羟基孕酮/apixaban/SN-38 为 nM–μM，胆酸/甲氨蝶呤/甲状腺素为 nM，地高辛精/血红素/胆绿素来自 RFdiffusion-allatom 骨架） |

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| **63.3% vs 50.4% vs 50.5%**（摘要口径） | 小分子附近天然序列回收率（LigandMPNN / Rosetta / ProteinMPNN） | "LigandMPNN significantly outperforms Rosetta and ProteinMPNN on native backbone sequence recovery for residues interacting with small molecules (63.3% versus 50.4% and 50.5%), nucleotides (50.5% versus 35.2% and 34.0%) and metals (77.5% versus 36.0% and 40.6%)" |
| **50.4%（Rosetta）/ 50.4%（ProteinMPNN）/ 63.3%**（正文口径） | 同上，正文把 ProteinMPNN 也写成 50.4%——与摘要的 50.5% 差 0.1 个点 | "The median sequence recoveries (ten designed sequences per protein) near small molecules were 50.4% for Rosetta using the genpot energy function" |
| 50.5% / 35.2% / 34.0% | 核酸附近回收率 | "For residues near nucleotides, median sequence recoveries were 35.2% for Rosetta 2 (using an energy function optimized for protein-DNA interfaces), 34.0% for ProteinMPNN and 50.5% for LigandMPNN" |
| **77.5% / 36.0% / 40.6%** | 金属附近回收率（本文最大的一项增益） | "and for residues near metals, 36.0% for Rosetta 41 , 40.6% for ProteinMPNN and 77.5% for LigandMPNN" |
| 86.1% / 83.3% / 76.0% | chi1 命中（距晶体 10° 内）：LigandMPNN / LigandMPNN-wo / Rosetta，小分子集 | "The median chi1 fraction (within 10° from crystal packing) near small molecules was 76.0% for Rosetta, 83.3% for LigandMPNN-wo and 86.1% for LigandMPNN" |
| 84.0 / 64.0 / 28.3 / 18.7 %（vs Rosetta 74.5 / 50.5 / 24.1 / 8.1） | chi1–chi4 加权正确率；远端二面角仍然很差 | "For LigandMPNN, weighted average fractions of correctly predicted chi1, chi2, chi3 and chi4 angles for the small-molecule dataset were 84.0%, 64.0%, 28.3% and 18.7%, for Rosetta 74.5%, 50.5%, 24.1% and 8.1%" |
| 317 / 74 / 83 | 三个留出集规模（小分子 / 核酸 / 金属） | "We held out a nonoverlapping subset of proteins that have small-molecule contexts (a total of 317), nucleotide contexts (a total of 74) and metal contexts (a total of 83)." |
| 5.0 Å / ~10 Å / 25 | 评测半径 / 影响的邻域假设 / 每残基取的配体原子数 | "We obtained the best performance by selecting for the protein-ligand and individual residue intraligand graphs the 25 closest ligand atoms based on protein virtual Cβ and ligand atom distances" |
| 0.1 Å（及 0.05 / 0.2 Å） | 输入高斯噪声标准差；噪声升降 ±~2% 回收率 | "Training with 0.05 Å and 0.2 Å noise instead increased and decreased sequence recovery by about 2%, respectively" |
| 3.5 Å / <6,000 残基 / 30% 同一性 / 16 Dec 2022 | 训练数据准入条件 | "The train-test split was based on protein sequences clustered at a 30% sequence identity cutoff." |
| 2–4% | 被拿侧链原子当伪配体做增强的残基比例 | "We augmented the training dataset by randomly selecting a small fraction of protein residues (2-4%) and using their sidechain atoms as context ligand atoms in addition to any small-molecule, nucleotide and metal context." |
| 2.62M / 1.66M；0.9 s / 0.6 s；~250× | 参数量与单 CPU 100 残基推理时间；对 Rosetta 的速度 | "It is about 250 times faster (because the expensive Monte Carlo optimization over sidechain identities and compositions is completely bypassed)" |
| 300,000 步 / 6,000 tokens / 1×A100 / Adam 0.9,0.98,1e-9 | 训练配置 | "Models were trained with a batch size of 6,000 tokens, automatic mixed precision and gradient checkpointing on a single NVIDIA A100 graphics processing unit for 300,000 optimizer steps." |
| −3%（砍图）/ −3.3%（只用侧链 context）/ −8%（去元素类型，金属） | 三项消融的回收率变化 | "Ablating the protein-ligand and ligand graphs led to a 3% decrease in sequence recovery" |
| >100 / 5 / 100-fold / 0.59 | 组内累计实验验证界面数、共晶结构数、最强的一次亲和力提升（来自引文）、与最近天然胆酸结合蛋白的 TMscore | "the cholic-acid-binding protein in the PDB that is closest to our cholic-acid-binding design (PDB: 6JY3 ) has a quite different structure (template modeling score 0.59)" |
| 3 / 2 | 本文 Fig 4 里 LigandMPNN 与 Rosetta 的测量重复数 | "The error bars show the mean and standard deviations for three LigandMPNN and two Rosetta measurements." |

## 5. 结论——作者说了什么

1. LigandMPNN 显式建模非蛋白原子，**在近配体残基的序列回收率上系统性超过 Rosetta 与 ProteinMPNN**，三个化学域各自给数（见第 4 节）。
2. 它顺带输出侧链构象分布，"LigandMPNN generates not only sequences but also sidechain conformations to allow detailed evaluation of binding interactions."，因此可以在计算阶段直接检查「设计出来的接触是不是真能成」。
3. 工程收益："The deep-learning-based LigandMPNN is superior to the physically based Rosetta for designing amino acids to interact with nonprotein molecules." 且 "It is about 250 times faster (because the expensive Monte Carlo optimization over sidechain identities and compositions is completely bypassed)"，加上新配体不需要写参数。
4. 外部验证的口径：已被用于设计 >100 个实验验证的小分子/DNA 结合界面、5 个共晶结构、把 Rosetta 小分子结合体重设计后亲和力最多提高 100 倍（摘要口径："redesign of Rosetta small-molecule binder designs has increased binding affinity by as much as"）。
5. 作者自留的边界：①稀有/未见元素要谨慎或映射到最接近元素；②低数据区建议与物理法混合；③chi3/chi4 仍然预测不好；④本文没有前瞻设计漏斗，验证主要靠组内其他工作。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **它解决的是「界面化学」而不是「催化」**。全文没有任何反应坐标、没有过渡态、没有能垒——金属位 77.5% 的回收率说明网络学到了「配位几何该放哪种氨基酸」，但**没有说这个位点会不会催化**。→ 对我们：LigandMPNN 适合做「把已确定的催化几何填进骨架」这一步（等价于我们漏斗里 motif → scaffold 之后的序列化），不能替代任何对「沿反应坐标多个态都对」的判断。
2. **最有价值的迁移点其实是被弱化的那一项**：侧链打包 + 置信度。作者以为卖点，但在 chi1 上对去掉配体上下文的版本只赢边际；这恰恰暴露了一个我们能用的判据——**「预组织」在结合位里主要由蛋白环境决定**（作者自己的解释 "consistent with binding site preorganization"）。这与 [B17]/[B19] 的 PLACER 系综判据是同一物理直觉的两个不同便宜实现：一个用 Boltzmann 权重、一个用自回归分布。我们若要给 UAA 催化位加「预组织」项，应该优先选这种不需要采样的形式。
3. **「公平比较」在这里被做成硬动作**：为了比 ProteinMPNN，他们在同一训练集上重训了一遍 ProteinMPNN，并规定比较时必须同噪声水平。→ 我们此前拿不同来源的分数（不同工具、不同版本）横向比过，这条纪律可以直接搬：换训练集/预处理之后旧分数失效，必须重训同基线再比。
4. **他们的「验证」是分布式借用**：本文自己的湿实验只有两个救援案例（且是 n=3/2 的重复数），其余靠 [B27]、Lee/An/Krishna 等论文的引用。这本身不是问题（Nature Methods 的方法类论文常这样），但意味着**任何「LigandMPNN 提升 X 倍」的引用都必须带出处层级**：摘要里的 100 倍来自别人论文的晶体起点重设计，不是本文的测量。我们引用第三方方法的证据时同样要分「本文测的 / 引文测的」。
5. **一个可复用的失败救援动作**：拿到一批「已合成、已测、结论是不结合」的旧设计，不扔，改成新设计器的输入再测一轮（C1/C2）。这几乎是本项目最便宜的一次机制检验——用同一骨架、同一配体坐标，只换序列，若结合出现就说明**瓶颈在序列端而非骨架端**。我们手里那批失败候选正是这个结构，值得排一轮这样的重设计。

## 7. 局限与失败（作者的 + 我们读出的）

- **作者承认**：稀有元素不可靠（要映射到最接近元素）；低数据区需要与物理法混合；chi3/chi4 未解决；侧链打包上配体条件化只带来边际改善；消融中多数增益是 2–3% 量级。
- **我们读出的**：①**摘要与正文的对照数字不一致**（小分子处 ProteinMPNN 在摘要里是 50.5%、正文里是 50.4%；共晶数量摘要写 "four X-ray crystal structures"、正文写 "5 co-crystal structures have been solved"）。差异小，但**说明这类 headline 数字不该被下游按位引用**。②**主指标（天然序列回收率）衡量的是「复现自然」而不是「设计成功」**：PDB 里被回收的那个氨基酸可能根本不是最优选择；回收率高 ≠ 结合好，本文也没有在近配体残基层面做过突变实验去验证这条链条。③**本文没有前瞻漏斗**：没有「按 LigandMPNN 建议设计 N 条 → 测 → 命中 M」的自有数字，因此**不能引用本文给任何 UAA 成功概率做校准**。④救援实验的重复数极少（3 / 2），且 cholic acid 那条只是「提高亲和力」，本文没给本文自己的 Kd。⑤训练集截至 2022-12-16、且以 PDB 复合物为分布——设计骨架（非晶体骨架）与训练分布的差距靠 0.1 Å 噪声缓解，这个缓解是否充分本文没有直接实验（只有噪声扫描 ±2%）。⑥无 MD、无 QM，因此本文也不能为「原子级判据是否足以判催化」提供正反证据。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **把它接在「催化几何已确定」之后**：我们的正确用法是 [B20]/[B17] 式 motif scaffolding 给出位点几何后，**用 LigandMPNN（而不是 Rosetta 打包）出周围序列**，并显式把催化残基的侧链坐标作为 context 输入（正是第 2.7 条那个「增强不涨点但留了接口」的能力："training in this way also enables the direct input of sidechain atom coordinates to LigandMPNN to stabilize functional sites of interest"）。这是本项目目前完全没用过、且成本几乎为零的一步。
2. **用它的置信度做二次排序**（不改变生成，只是先测谁）："LigandMPNN predicts amino-acid probability distributions and uncertainties for each residue position"，而置信度与真实回收相关。→ 具体做法：每个骨架出 N 条序列后，按「催化位周围残基的平均预测概率」排序，取分布两端各若干条进湿实验（同时保留低置信度者作为机制反证），把这当作**免费的多样性/把握度信号**，而不是当作成功判据。
3. **借「同训练集重训基线 + 同噪声水平才许比较」这条口径**（第 6.3），写进我们任何方法对比协议里：不同预处理下的分数不许跨方法比。
4. **借失败救援结构**（第 6.5）：已测不结合的旧候选 → 同骨架同配体坐标、只换序列设计器 → 重测。它能把「骨架错」与「序列错」分开，是 DP2R 标准里少见的**归因型实验**（而非命中型实验）。
5. **预组织可用便宜的分布量近似**：若需要「位点是否已经摆好」的判据，RotamerBoltzmann（[B27] 用）或 LigandMPNN 的 chi 分布/置信度都是**无采样**的实现，比跑系综便宜几个数量级；但两者都只是预组织的代理（见不可迁移第 2 条）。

**不可迁移（为什么不能照搬）**

1. **回收率数字（63.3/50.5/77.5%）不是任何功能命中率**，与 UAA 催化毫无可比性；把它们当「设计成功概率」属于误用（DP2R 标准 §2：禁止把非功能指标当酶活闸口）。同理，~250 倍加速只说明**单价便宜**，不说明通过率；本项目「通过率 ÷ 单价」的效率口径（见 B09 卡第 8 节）仍然要自己测通过率。
2. **它是静态单态判据**。LigandMPNN 学的是「在这个固定配体位置旁边该放什么氨基酸」，而 UAA 合成酶要同时容纳多个化学态（游离 UTP / pppUA / 环化竞争），配体自己在变、电荷在变。→ 单态条件化的序列对第二、第三个态没有任何承诺；这一层仍要另找证据（本文没有，也不能外推）。
3. **本文没有任何前瞻漏斗，也就没有任何可借的「实验→命中」分母**；引用它的 >100 界面与 5 个共晶只能作为「工具被组内项目用过」的存在性，不能作为「我们的靶能成」的概率。
4. **金属位 77.5% 的漂亮数字不能推到 UAA 的金属辅因子场景**：那是回收天然 PDB 里已有的金属配位氨基酸（多数是 His/Cys/Glu 的规律排布），本质是「学会常见配位模式」；我们的问题里金属位是否成立要靠机制层证据，而不是这个回收率。
5. **无 MD/QM** —— 与 [B17]/[B19]/[B20] 那一族不同，本文完全不能用于「要不要用系综/量子化学」的论证。

## 9. 溯源与自检

- 引句底稿: data/literature_cards/fulltext/B28_PMC11978504_text.txt
- 本地全文（Europe PMC fullTextXML 归一化：剥标签、HTML 实体解码、破折号/引号/负号统一，未改写内容）；原始 XML 为同目录 `B28_PMC11978504_fullTextXML.xml`（SHA-256 `7e33fb90a1f61701…`，抓取记 HTTP 200 / 125,708 B）。`sources_map.json` 的 B28 条目已登记这两份全文加 `sources/baker.md`；xml 按门禁规则不作为可读底稿，故本卡引句只与上面声明的 `_text.txt` 逐字比对。
- 旧底稿（摘要级）：`sources/baker.md:368–379`，其中摘要引句与本文正文口径的差异已在第 7.① 条记录；CSV 的 `证据级别` 字段仍写「摘要级」，属建库时状态，`batches.tsv` 本行 state 为 FULLTEXT。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/成本统计/Kd或活性最好值`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B28 --no-report`（输入：本卡 + `sources_map.json` 中 B28 登记的可读底稿，并按 §9 声明的 `引句底稿` 逐字比对）。本卡结果 **PASS B28 quotes=91/91，退出码 0**。首轮有 1 条 MISS：我把原文里那句展望按英文句首大写的习惯抄成了 We anticipate 开头，但归一化全文中它前面紧跟 As with ProteinMPNN, 这个连接短语，所以真正可逐字命中的形态是带前缀的整句；把前缀补回引句后转绿；此后又红过一次——原因是 §9 自检段里用直双引号举了这个抄错的片段作例子，那一行本身被门禁当引句比对，改成中文述句后转绿。本行只有一份全文通路（Europe PMC），无第二份独立抽取互证，已在第 0 节标明。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 2 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=方法（深度学习序列设计器）
target=任何含非蛋白原子的界面：小分子结合/传感蛋白、DNA/RNA 结合蛋白、金属配位位；本文自有湿实验对象是此前 Rosetta 做的不结合（rocuronium）与极弱结合（cholic acid）设计
backbone_generation=不生成骨架（输入给定骨架 + 配体坐标）；序列端用 LigandMPNN：三张图（蛋白图 / 配体内图 / 蛋白-配体图），每残基取按 virtual Cβ 距离最近的 25 个配体原子，额外两条蛋白-配体编码层，随机自回归解码；另用同架构网络在序列之后输出 chi1-4 三成分圆正态混合（侧链构象）
computational_filters=训练期过滤（结构分辨率、链长、去除 HOH/NA/CL/K/BR、30% 同一性划分训练/测试）；评测期用近配体残基（侧链距非蛋白原子 5.0 Å 内）的天然序列回收率、预测置信度与回收率的相关性、chi 角命中率与侧链 RMSD；使用侧的排序信号是模型给出的氨基酸概率/不确定性（本文不引入新的复合物级筛选器）
thresholds=训练数据 ≤3.5 Å 且 <6,000 残基（PDB 截至 16 Dec 2022）；聚类切分 30% 序列同一性；每残基 25 个 context 原子；输入高斯噪声 0.1 Å（0.05/0.2 Å 分别 ±约 2% 回收率）；评测半径 5.0 Å；邻域物理假设 ~10 Å；chi 命中判据 距晶体 10° 内；训练 300,000 步 / batch 6,000 tokens / 单张 A100；侧链增强比例 2-4%
md_used=否
qm_used=否
experimental_methods=本文自有：酵母表面展示 + 流式（1 μM 生物素化 rocuronium + SAPE）与荧光偏振（cholic acid-FITC）重设计前后对比；结构证据与其余功能证据来自组内引用工作（[B27] DBP 共晶 8TAC、Lee/An/Krishna 的小分子结合体系），非本文测量
pipeline_counts=无前瞻漏斗：训练/留出集为 PDB 复合物（小分子 317、核酸 74、金属 83 个留出结构），每蛋白设计 10 条序列 / 生成 10 个侧链打包样本；实验侧只有 rocuronium 与 cholic acid 两组重设计（图注给 3 个 LigandMPNN 与 2 个 Rosetta 测量）；组内累计 >100 个小分子/蛋白-DNA 结合界面被实验证明结合、5 个共晶结构（引用口径）
hit_rate=本文未给自有命中率（没有「设计 N 条→命中 M 条」的前瞻实验）；可引用的是留出集回收率：小分子附近 63.3% vs Rosetta 50.4% / ProteinMPNN 50.4%（摘要口径把 ProteinMPNN 写为 50.5%），核酸 50.5% vs 35.2% / 34.0%，金属 77.5% vs 36.0% / 40.6%
best_metric=本文 Fig 4 未给 Kd；摘要与讨论给出的最强功能改善是 "redesign of Rosetta small-molecule binder designs has increased binding affinity by as much as"，正文注明该 100 倍来自从已解析复合物出发重设计的另一篇工作（ref 4）；引用工作中的小分子结合体为 nM（胆酸/甲氨蝶呤/甲状腺素）至 nM–μM（17α-羟孕酮/apixaban/SN-38）
cost_or_stat_note=推理 0.9 s（100 残基、单 CPU）对 ProteinMPNN 0.6 s、Rosetta 约慢 250 倍；参数量 2.62M 对 ProteinMPNN 1.66M；单张 A100 训 300,000 步、batch 6,000 tokens；消融增益多为 2–3%（砍蛋白-配体/配体图 −3%、只用侧链 context −3.3%、去元素类型在金属处 −8%），噪声旋钮自身影响 ±~2%
role_in_timeline=序列端的「全原子化」：承接 [B05] ProteinMPNN（纯骨架条件化）与 [B13]/[B20] 的全原子 motif scaffolding（生成端全原子化），把非蛋白原子正式变成序列设计器的输入，并附带输出侧链构象与置信度；[B27] 在真实 DNA 设计项目里把它作为 Rosetta LayerDesign/FastDesign 的替代分支（暴露两者优劣不对称）；对 2026 年的原子级生成路线（RFdiffusion2/3、RFAA）而言它是「几何定下来之后如何廉价填序列」的默认件
source_pointer=data/literature_cards/fulltext/B28_PMC11978504_text.txt（归一化后 56,924 字符）+ 同名 _fullTextXML.xml（SHA 7e33fb90a1f61701…）；sources/baker.md:368-379（旧摘要级卡）、:604（序列设计换代行）、:644（LigandMPNN 原子环境条件化条目）
CSV回填-->
