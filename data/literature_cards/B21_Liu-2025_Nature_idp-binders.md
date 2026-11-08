# [B21] 只给靶点序列就能设计结合体——把「目标构象谁来定」这件事交给扩散模型

Liu Caixuan, Wu Kejia, Choi Hojun, Han H L, … Watson J L, Knowles T P J, Baker D（华盛顿大学 IPD + Cambridge）
Nature 2025, 644:809-817 · DOI 10.1038/s41586-025-09248-9 · PMID 40739343 · PMCID PMC12367549
开放获取（CC BY 4.0）· 预印本 bioRxiv 2024-07-16 · https://doi.org/10.1038/s41586-025-09248-9

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B21**（组：Baker组） |
| 本地全文①（本卡唯一登记全文） | `data/interim/baker_lit/ft/idp_binder2025.txt`（104,799 B，SHA-256 `28c744c6b8f688ed…`，2026-10-16 抓取，通道 `epmc_search_then_fulltext`，标签剥离 + `scripts/litcards_text.py` 归一化） |
| 第二通路互证 | 未取得（`sources_map.json` 中 B21 只有上述一份全文 + `sources/baker.md` 底稿；不像 B09 有两条独立抽取通路可比对）。**本卡引句只由这一份全文担保** |
| 对照底稿 | `sources/baker.md:278-288`（原卡）；本卡在其基础上补：二级结构指定训练配方、两侧部分扩散 timestep 口径、氢键数判据、成本数据（GPU 秒/RAM）、晶体结构 RMSD 明细、SSM 与相分离/内吞等下游功能实验 |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中；见第 9 节门禁结果） |
| 未取到的部分 | Supplementary Information（Fig 1 流式门控图、Supplementary Tables 1-5 逐靶阈值与序列）、Extended Data Fig 原图数值、Zenodo 设计模型。凡涉及这些的地方本卡明写「正文未给出」 |

## 1. 这篇到底解决什么（大白话）

无序蛋白（IDP）和无序区（IDR）没有一把「标准形状」，所以过去要么用抗体（贵、且靶子在免疫后容易被降解），要么用计算方法——但那些方法**要求你先指定靶肽该折成什么构象**（ helix / strand / PPII），而「哪种构象最容易结合」本身正是不知道的事。这篇的做法是：把 RFdiffusion 改成**只吃靶子的一维序列**，让靶子和结合蛋白在扩散轨迹里**一起自由采样构象**，谁先找到合适的形状就互相锁住；对太短、构象变化太大的 IDR，再给模型加一个**只指定二级结构（不指定三维坐标）的接口条件**，逼它产出 β-strand 配对界面。然后一次一次做「部分扩散」把初筛命中往高亲和力方向推。结果是 amylin/CP/VP48/BRCA1_ARATH/G3BP1/prion/IL-2RG/FUS 一批靶子上拿到 3–100 nM 的结合体，并用细胞共定位、相分离、纤维解聚、LC-MS/MS 富集证明了在真实体系里能用。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **旧范式要求预先指定靶肽构象，而这正是不可知的**。原文：**"Although powerful, these methods require pre-specification of the target peptide geometry, which can be limiting"**，因为最优构象 **"may be quite irregular"**。→ **他们做了什么**：改成 sequence-input RFdiffusion（靶子只给序列、构象随扩散一起采样），并把「结合机制」重新表述为诱导拟合：**"the binder selects a specific conformation out of a broad ensemble"**。代价：无法保证选中的构象是生理相关构象，所以他们必须再补细胞与结构层面的验证（第 3 节 C 段）。
2. **初筛亲和力太弱，不够下游用**。第一批 96 条 amylin 设计 **"binding affinities ranging from 100 nM to 454 nM"**。→ **他们做了什么**：发明 **two-sided partial diffusion**（对母复合物的靶链与结合链**同时**加噪到 timestep 5–25/50 再重去噪），理由写在正文：**"two-sided diffusion yielded designs with better metrics than one-sided diffusion, probably because the target conformation can adapt to that of binder"**。效果：amylin 从 100–454 nM 推到 3.8 nM。**留下的代价**：正文只给「更好」的定性判断与 Extended Data Fig 2 的指标对比，机理解释是推测（probably）。
3. **单边加噪会把靶子冻死**。Extended Data Fig 2 的对照写得很具体：**"At steps 25, 30, and 35 exclusively, one-sided partial diffusion exhibited superior performance"**，但 **"in practical cases, we typically operate within fewer than 25 steps to remain the main features of parent structure"**。→ 应对：把工作点固定在 <25 步，并同时报两种做法的指标分布，而不是宣称一边永远更好。
4. **C 肽这种短而全无序的靶子，第一轮只出 1 个弱命中**：96 条设计里只有 1 条结合且很弱（初命中 CP-95 = 16 μm）。→ **他们做了什么**：**换判据**——不看 pAE/pLDDT，改看界面氢键数：**"Guided by the observation that this design had more hydrogen bonds between target and binder (13) than all but 5 of the 96 designs"**，据此再跑两侧部分扩散并按氢键数选，得到 **"Six out of 95 designs bind to CP with better than 100 nM binding affinity"**，最优 CP-35 = 28 nM。**代价**：CP 系列最终**没能拿到晶体结构**——**"We were unable to solve crystal structures of the CP binders"**，只能用 SSM 突变热图当低分辨率结构证据。
5. **对短 IDR，纯序列输入的产出率太低**。G3BP1 的 RBD 用序列输入跑，产生的构象里 helix:strand:loop 比例约 5.7:3.8:0.5，但 **"only the 23 strand-containing designs had AF2 predicted aligned error (pAE) interaction < 10 and predicted local distance difference test (pLDDT) binder > 90"**。→ **他们做了什么**：**重训模型**，加二级结构接口指定（见第 3 节 B 段），结果是 **"we specified the secondary structure as a strand which increased the fraction of designs passing the filters more than 50-fold"**，图注给出实测：**"noting 23 successes with sequence input and 1,192 with strand specification"**，作者自己算成 **"approximately 51-fold increase in efficacy"**。
6. **指定二级结构后亲和力仍不一定好，需要与序列输入对比**。prion 的 8 残基靶区：序列输入最好的 PRI22 只有 1.88 μM，二级结构指定的 PRI28 = 14 nM，正文把这句写成对照结论：**"Specifying the secondary structure of the target region as a β-strand resulted in binders with higher affinity than using the target sequence information alone"**。→ 应对：对短靶统一走 strand 指定路线；1.88 μM 那条也没扔，继续用部分扩散推到 80 nM。
7. **一部分靶子被主动放弃，而且原因分成两类**。① 安全：细胞共定位实验 **"except for the prion binder, which was excluded due to safety concerns"**；② 亲和力不够： **"the FUS binders, whose binding affinities were not considered sufficient for cellular binding"**。→ 应对：不在正文里为这两个靶做进一步辩护，功能实验只做能做的靶（G3BP1 相分离/压力颗粒、amylin 纤维与内吞、CP 的 SSM）。
8. **晶体结构只解出来一部分**：**"We attempted to solve structures for all of our designs, but only the amylin and G3BP1 complexes successfully crystallized."** → 应对：解出的三个结构（amylin-22 αβL 1.8 Å、amylin-18 αβ 2.0 Å、G3BP1-11 2.4 Å）用来核设计精度；解不出的用 CD 热稳定性 + SSM 热图 + 共定位补齐「能折、能结合」的证据链。
9. **应用端撞回亲和力上限**：用 amylin-68n 做 LC-MS/MS 富集，回收率 62.2%（血浆）/53.5%（PBS-CHAPS），但内源性 amylin 太低测不到——**"endogenous levels were too low for reliable detection"**，作者自己写：**"Tighter binders generated through further optimization will probably be necessary to enrich endogenous amylin."** **本文未解决**（该靶的实测灵敏度门槛）。
10. **特异性有漏洞，作者直接摊开**：all-by-all 里 **"binder VP48-2 weakly bound amylin above 800 nM"**，并给出解释（两个靶约 50% 螺旋含量相近）与补救方向：**"specificity could potentially be further improved through another round of partial diffusion, or decreasing the helical percentage through secondary structure specification"**。→ 应对写的是「可选项」，本文没有真的去做第二轮。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **骨架构象生成**：RFdiffusion **v1.1.0** 的两个变体——① sequence-input（靶链只给序列、坐标加噪）；② 重训的 secondary-structure specification 版（可指定靶区为 helix/strand/loop，**不给三维坐标**）。作者选 ②的理由是坐标指定法对 strand 不经济：**"the coordinate specifying approach used by Vasquez et al. 12 for helical peptides would be less efficient for targeting strands"**（引文编号插在两句之间，故不合并引）。
- **亲和力再优化**：**two-sided partial diffusion**（靶链与结合链同时按 timestep 部分加噪再重去噪；与只 diversify binder 的 one-sided 相对）。
- **局域补相互作用**：对 VP48 用 **backbone extension**（inpaint 模式，从 N/C 端或两端各接 10–20 残基）。
- **序列设计**：ProteinMPNN（v1.0.1）。
- **计算侧过滤器**：AF2 + **initial guess**（复合物）、AF2 monomer（单体 pLDDT 与设计结构 RMSD）、Rosetta FastRelax 后的 contact_molecular_surface / ddG / SAP / 氢键数。
- **实验侧**：Golden Gate 入 LM670 → E. coli 96 深孔自诱导表达 → Ni 磁珠纯化 → 单点 BLI（终浓度约 1 μM）→ 命中者做滴度 + 全局动力学拟合 Kd；CD 测折叠与 Tm；BLI all-by-all 测特异性；酵母展示 SSM 热图（CP-35）；X 射线晶体学；HeLa 线粒体靶向共定位（靶-eGFP-mito + 结合体-mScarlet）；微流控 PhaseScan 相分离图；ThT/负染电镜测纤维；EndoTag 融合做溶酶体转运；LC-MS/MS 回收率。
- **没有用的方法**：MD、QM、自由能微扰（droplet microfluidics 是成像实验，不是模拟）。

### A. 纯序列输入路线（长 IDP / 无构象偏好靶）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 靶子**一级序列**（amylin 37aa、CP 31aa、VP48 39aa、BRCA1_ARATH 941aa 中 21aa 靶区、FUS 中 29aa 靶区） | 先用 IUpred3 / Jpred4 / AF2 pLDDT 判定「确实无序」（IUPred3 分值在靶区持续 >0.5） | 正文用 disorder 预测与低 pLDDT 作准入，未给数值化阈值（除 IUPred>0.5 的描述） | 选定 5 个 IDP/长靶 |
| A2 | 序列 + 空坐标 | sequence-input RFdiffusion 生成复合物；**靶与结合体同时采样构象** | 无（生成阶段不设阈值） | **"approximately 10,000-50,000 diffused designs were generated given only sequence input of the target"** |
| A3 | 骨架库 | ProteinMPNN 出序列 → AF2 + initial guess 复测复合物、AF2 复测单体 → FastRelax 补 Rosetta 指标 | **"largely focused on interface pAE_interaction < 10, pLDDT > 90, number of hydrogen bonds > 11, RMSD < 0.5, sap score < 45 and Rosetta ddG < -40"**；但阈值本身是软的：**"Precise metrics cut-offs changed for each design campaign to get to an orderable set"** | **"Specific filtering criteria were carefully selected to narrow down the set to 48-96 designs for each target"** |
| A4 | 48–96 条/靶 | 96 孔 E. coli 表达 + Ni 磁珠 + 单点 BLI；有信号者滴度 + 全局拟合 | 单浓度 BLI 阳性 → 滴度定 Kd | amylin：**"binding affinities ranging from 100 nM to 454 nM"**（4 条初命中 100/317/431/454 nM）；CP：96 中 1 条弱命中（16 μm）；VP48：**"Of the 95 designs tested, the best binder with an affinity of 750 nM"**；BRCA1：**"2 of 41 tested designs showed binding at approximately 450 nM"**；FUS：94 中 3 条、最优 520 nM |
| A5 | 初命中复合物结构 | **two-sided partial diffusion**：靶链与结合链一起加噪 | **"The input designs were subjected to 5-25 noising timesteps out of a total of 50 timesteps in the noising schedule"**；实用工作点 **< 25 步** | **"Approximately 5-50,000 partially diffused designs were generated for each target"**；amylin **"Among the 174 top-ranked designs spanning αβ, αβL and αα amylin conformations, 107 bound amylin"**，最优 3.8 nM；CP 转氢键数判据后 6/95 条 >100 nM 内、最优 28 nM；VP48 → 39 nM；BRCA1 → 52 nM |

### B. 二级结构指定路线（短 IDR，需要 β-strand 配对）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 序列（G3BP1 RBD、prion VNITIKQH 180-187、IL-2RG ERLCLVSEIP 327-336） | 微调 RFdiffusion：训练时 50% 时间给（部分屏蔽 0–75% 的）二级结构、独立 50% 给 block adjacency，异复合体里靶链最多 50% 骨架加噪但保留序列；共训 **seven epochs** | 无（训练配方，不设判据） | 可指定 helix/strand/loop 的新模型 |
| B2 | 序列 + 指定 strand | 每个靶约 **10,000** 条扩散设计 → MPNN → AF2 + initial guess → 同一套过滤 | 与 A3 同 | G3BP1 序列输入只有 **23** 条过 pAE<10 & pLDDT>90；strand 指定后 **1,192** 条（**「more than 50-fold」**） |
| B3 | 过滤后的池子 | 单点 BLI → 滴度 | — | G3BP1：**"Five out of 78 designs bound to G3BP1 RBD , with the tightest having a binding affinity at 17 nM"**；prion：**"Of 48 designs tested, the tightest, PRI28, had a binding affinity of 14 nM"**；IL-2RG：94 条里 1 条 493 nM |
| B4 | 命中者 | 两侧部分扩散再优化 | 同 A5 | G3BP1-11 → 11 nM；IL-2RG-30 → 97 nM；PRI22 1.88 μM → 80 nM |

### C. 结构、细胞与功能验证（漏斗之外的「能不能用」）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | 全部设计 | 尝试结晶 | 有衍射质量晶体即算成功 | **"We attempted to solve structures for all of our designs, but only the amylin and G3BP1 complexes successfully crystallized."**（amylin-22 1.8 / amylin-18 2.0 / G3BP1-11 2.4 Å；PDB 9NZH、9CC5、9CC6） |
| C2 | 设计模型 vs 晶体 | 比 Cα / 侧链 RMSD | 正文给实测值，未给通过线 | amylin-22：binder Cα 0.96、复合物 2.04、界面 Cα 1.33 / 侧链 1.87；amylin-18：复合物 Cα 0.741、界面 0.958 / 1.279；G3BP1-11：复合物 Cα 0.8、界面 0.86 / 2.29 |
| C3 | 解不出晶体的 CP-35 | 159 残基全位点饱和突变（SSM）酵母库 → 先表达分选 → 1 μM with-avidity 两轮 → 200 nM/40 nM/8 nM/1.6 nM/0.32 nM without-avidity 各一轮 → NGS 算 SC50 热图 | 界面与核心残基「保守」即支持设计模型（定性） | 界面/核心残基大多保守，支持设计模型；作者注明 CP-35 因结构复杂度与 SSM 数据质量被选中做详分析 |
| C4 | 结合体-靶对（除 prion、FUS） | 靶-eGFP-mito + 结合体-mScarlet 共转染 HeLa，看共定位点；短 IDP 再在预测界面插两个点突变作阴性对照 | 共定位出现 = 细胞内结合；点突变破坏共定位 = 界面特异 | 8 对给出共定位；IL-2RG 用 CRISPR-Cas9 把内源蛋白换成 eGFP 融合构建体 |
| C5 | G3BP1-11 | 微流控 PhaseScan 画相分离图（RNA 0–8 与 0–150 ng/μl 两档）+ 细胞亚砷酸盐压力颗粒实验 | 相边界位移 / 每细胞 puncta 数（n=20 细胞每条件） | 结合体使相分离需更高 G3BP1 浓度，1 μM 处出现可见相边界；细胞里亚砷酸盐不再显著增加 puncta |
| C6 | amylin 四条结合体 | ThT + 负染电镜：抑制纤维、解聚延伸期与成熟纤维；再融合 ASGPR/IGF2R EndoTag 做内吞 | 抑制率、形貌、MFI | 1:4（10 μM 结合体 : 40 μM amylin）全部完全抑制；1:4、1:40、1:400 呈浓度依赖；成熟纤维 1 h 仍见小寡聚体、**18 h 完全解聚**；MFI 约 8×（ASGPR）与 4×（IGF2R） |
| C7 | amylin-68n 偶联磁珠 | 免疫亲和富集 + LC-MS/MS（3 种珠：目标结合体、脱靶结合体、BSA 封闭；阳性对照抗-GPVG 抗体珠） | 回收率相对纯 amylin 峰面积（100%） | 血浆 62.2%、PBS-CHAPS 53.5%；内源 amylin 测不到 |

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处 |
|---|---|---|
| 60% | IDP/含 IDR 蛋白占人类蛋白组比例（立论背景） | Introduction |
| 31–941 残基 | 靶长跨度（CP 到 BRCA1_ARATH） | Abstract / Main |
| 3–100 nM / 10–100 nM | 全长 IDP 结合体 Kd 区间 / 短 IDR（strand 指定）Kd 区间 | Abstract |
| ~10,000–50,000 → 48–96 | 每靶扩散设计数 → 送测数 | Methods「Binder design using sequence input RFdiffusion」 |
| pAE_interaction<10, pLDDT>90, 氢键>11, RMSD<0.5, SAP<45, ddG<-40 | 实际过滤判据组合 | Methods「Computational filtering」 |
| 5–25 / 50 timestep，5–50,000 条 | 两侧部分扩散加噪深度与产出 | Methods「Two-sided partial diffusion to optimize binders」 |
| 96 → 4（100/317/431/454 nM） | amylin 首轮 | Extended Data Fig 1a |
| 174 → 107 | amylin 优化轮 top-ranked → 结合数 | Fig 2a-d 段 |
| 3.8 / 10 / 15 / 100 nM | 四个构象的最优 amylin 结合体 | Fig 2a-d 段 |
| 96 → 1（16 μm）→ 95 → 6 → 28 nM | CP 全程（含氢键数=13 判据） | 正文 + Extended Data Fig 3d-f |
| 95 → 750 nM → 39 nM | VP48 全程 | 正文 Fig 2f 段 |
| 41 → 2（≈450 nM）→ 52 nM；94 → 3（520/730/750 nM） | BRCA1_ARATH 与 FUS | 正文 + Extended Data Fig 4c,g |
| 23 → 1,192（≈51×、「>50-fold」） | G3BP1 序列输入 vs strand 指定的通过数 | Extended Data Fig 5c + 正文 |
| 78 → 5 → 17 nM → 11 nM；48 → 14 nM；94 → 1（493 nM）→ 97 nM | 三个 strand 靶的递减与 Kd | 正文 Fig 2h-j 段 |
| 1.88 μM（PRI22）→ 80 nM | 序列输入 vs 指定后 + 部分扩散 | Fig 2i 段 + Extended Data Fig 6c,d |
| 1.8 / 2.0 / 2.4 Å；0.96/2.04/1.33/1.87；0.741/0.958/1.279；0.8/0.86/2.29 | 三个晶体分辨率与设计 RMSD | 正文「Structural analysis」+ Extended Data Fig 7a,b |
| 159 残基、1 μM、200/40/8/1.6/0.32 nM | CP-35 SSM 库覆盖与分选浓度梯度 | Methods「Preparation of SSM libraries」 |
| 8 对共定位；prion 与 FUS 被排除 | 细胞验证覆盖 | 正文「Binders colocalize with targets in cells」 |
| 1:4 / 1:40 / 1:400；18 h | 纤维抑制与解聚条件 | Fig 5 + Extended Data Fig 9d-f |
| 62.2% / 53.5% | 血浆 / PBS-CHAPS 的 amylin 回收率 | 正文「Enrichment for LC-MS/MS detection」 |
| 25–30 s/GPU（RTX2080 或 A4000，1 CPU 核、约 8 GB RAM）；MPNN <0.5 s/CPU | 单设计计算成本 | Methods「Computational time and hardware usage」 |

## 5. 结论——作者说了什么

1. **只给靶序列 + 让靶与结合体一起自由采样**，RFdiffusion 就能对跨度 31–941 残基、构象偏好各异的 IDP/IDR 出结合体，Kd 3–100 nM。
2. 对**短 IDR**，加入「只指定二级结构（strand）」的接口条件后，通过率提高 **>50 倍**，且亲和力优于纯序列输入（14 nM vs 1.88 μM）。
3. 设计出的结合体是**规整折叠蛋白**，通过**诱导拟合**抓住靶的一个子区、一种构象，而不是包住整个无序系综。
4. 结构侧：三个复合物晶体结构与设计模型高度一致；G3BP1-11 把靶区「夹」成 β-strand。
5. 功能侧：amylin 结合体能**抑制并解聚纤维**、把单体与纤维送进溶酶体、提高 LC-MS/MS 检测灵敏度；G3BP1 结合体**破坏压力颗粒组装**。
6. 作者自限：与最近提出的 logos 方法是**互补**而非替代（本文方法擅长「能以部分螺旋/β-strand 被结合」的序列）；特异性与内源检测仍受亲和力上限约束；IL-2RG 等细胞内应用「仍有进一步优化的空间」。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的杠杆不在过滤器更强，而在「把未知量交给生成模型」**。当「靶该是什么构象」是未知时，任何以固定靶几何为前提的打分器都在给一个假设打高分；他们的做法是让假设本身参与采样。→ 对我们：如果底物（游离底物/ATP）在口袋里的取向也不确定，用「单一对接姿态 + 静态几何打分」当主闸口，等于重复他们要替换掉的那个范式。
2. **「通过率」和「绝对命中率」被分开报，而且两者相差两个数量级**。strand 指定使通过计算闸口的比例涨 50 倍（23→1,192），但湿实验命中率仍在 5/78、3/94、1/94 的量级。→ 说明**涨的是生成端供给，不是判据的判别力**；他们的判据从头到尾没变（还是 pAE/pLDDT/RMSD/ddG）。任何「某改进把漏斗变好了 X 倍」都必须问：X 是生成端的还是判别端的。
3. **判据会在缺数据的靶上被临时替换**（CP 那次：pAE 类指标没区分开，就改看界面氢键数，并把它写进选池规则）。这是「判据服务可达标集合」的实例，和 [B23] 里「阈值按靶各调」的写法一致——阈值不是先验的。
4. **放弃是有记录的放弃**：安全（prion）与亲和力不足（FUS）两类排除被明写，没有被「平均掉」。→ 我们做阴性报告时同样要区分「测不了」和「测了不中」。
5. **功能层证据链全靠湿实验，计算侧对「在细胞里可用」没有任何判据**：共定位、相分离、内吞、LC-MS/MS 都在下单之后。这提示我们的漏斗末端必须自带一个「细胞/粗提物里能不能被看到」的层，而它不可能来自结构自洽性。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：① 部分靶未做细胞验证（prion 安全、FUS 亲和力不足）；② CP 系列无晶体结构；③ 内源 amylin 仍测不到，需要更紧的结合体；④ VP48-2 在 >800 nM 时对 amylin 有弱交叉反应；⑤ 方法擅长可部分形成规整二级结构的序列，extended 构象偏好更强的 IDR 交给别的范式（logos）。
- 我们读出：① 「two-sided 更好」的**解释是推测**（probably because），对照只在 Extended Data 图注里；② 命中率分母极小（41/48/78/94/95/96），逐靶给 1–6 个命中，**不存在可信的「平均命中率」**；③ 过滤阈值逐次调、正文自认 "changed for each design campaign"，因此外部复现需要 Supplementary Tables 1–5（本次未取）；④ 「设计正确」只由 Cα/侧链 RMSD 界定，对**结合动力学**（在细胞内被竞争、被降解）没有判据；⑤ 全文无 MD/QM，不能为「用 MD/QM 判催化」提供任何支持。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **「未知构象交给采样，而不是交给假设」**（本库判据里「底物取向未定」的那一环）：把进入的 NTP 姿态当作采样对象（多姿态/短系综），判据写成「在若干底物姿态里有多少比例同时满足成键几何」，而不是「在某一个对接姿态上是否满足」。
2. **「生成端通过率」与「判据判别力」分开报**（G0/G6）：任何改进（新条件化、新打分项）先只报「过闸候选数怎么变」，除非有独立标签集，否则不许把它写成成功率提升。
3. **判据可临时替换，但要留痕**：像他们把 CP 的选池改成按界面氢键数那样，允许为特定靶声明一个替代判据，同时必须在 run.md 写清「本靶用了什么判据、为什么」，避免跨靶汇总时口径混淆。
4. **主动放弃要显式分类登记**（「测不了/不安全」vs「测了不中」），与我们的 UNKNOWN / METHOD_FAIL 状态口径直接对齐。
5. **功能层证据链（共定位/相分离/内吞/LC-MS-MS）放在下单之后**这一事实说明：漏斗末端要留「能被看见」的检测层（我们的产物化学读出），而不是继续加计算闸口。

**不可迁移（为什么不能照搬）**

1. **pAE_interaction<10 / pLDDT>90 / RMSD<0.5 判的是「会不会按设计结合」，不是「能不能催化三步化学事件」**。这篇的靶是「结合一个肽构象」，成功标准是静态界面；目标酶要的是沿反应坐标的多个态都对。本库判据 §2 禁止把 binder 的 pAE/ipTM 阈值当酶活闸口。
2. **「通过率涨 51 倍」是生成端供给的变化，绝不能当作我们的命中率或先验**；本文湿实验命中率仍在每靶 1–6 个（分母 41–96）的量级，把它转成「某法对酶设计成功率 X%」属于编造。
3. **诱导拟合式的「选一个构象锁住」不迁移**：催化判定要排除的是错误连接（错误连接）与竞争副产物，一个被锁死的底物姿态既不能证明方向正确，也不能排除副反应；连接型必须由化学/质谱读出，而非由界面形状推断。
4. **本文无 MD/QM/自由能**：这篇不能作为「MD/QM 判催化可行」的证据参照；那类主张需另找参照（本文无）。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/idp_binder2025.txt

- 引句底稿: data/interim/baker_lit/ft/idp_binder2025.txt
- 本地纯文本：`data/interim/baker_lit/ft/idp_binder2025.txt`（SHA-256 `28c744c6b8f688ed…`；抓取通道与 URL 记于 `data/literature_cards/inventory.json` 的 B21 记录：`epmc_search_then_fulltext`）。
- 对照底稿行号：`sources/baker.md:278-288`；汇总表相关行：`sources/baker.md:605`（3a 自洽性闸口）、`611`（5b 中低通量直测）、`625`（Kd 分布 28–750 nM 段）。
- 代码与数据指针（原文）：RFdiffusion GitHub；脚本名 `examples/design_ppi_flexible_peptide.sh`、`design_ppi_flexible_peptide_with_secondarystructure_specification.sh`、`design_partialdiffusion_withseq.sh`；模型权重 `InpaintSeq_ckpt.pt`、`InpaintSeq_Fold_ckpt.pt`；设计模型 Zenodo；PDB 9NZH / 9CC5 / 9CC6。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：由 `scripts/verify_literature_cards.py` 执行——把卡内所有含直双引号、无中日韩字符、≥20 字符且 ≥12 个字母的片段，在登记的每一份本地全文里做逐字查找，任一条不命中即 FAIL。本轮结果见下方回报（命令：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B21 B22 B23 --no-report`）。

<!--CSV回填
work_type=论文
target=IDP/IDR：amylin(hIAPP)、C-peptide、VP48、BRCA1_ARATH(941aa)、FUS、G3BP1 RBD、prion 180-187、IL-2RG 327-336
backbone_generation=RFdiffusion v1.1.0 两变体（sequence-input 自由采样靶构象；重训版可指定靶区 helix/strand/loop 而不给坐标）+ two-sided partial diffusion 优化 + VP48 backbone extension(inpaint)；序列由 ProteinMPNN v1.0.1
computational_filters=AF2+initial guess 复合物 interface pAE_interaction、pLDDT；AF2 单体 pLDDT 与设计结构 RMSD；Rosetta FastRelax 后 CMS、ddG、SAP、界面氢键数；CP 系列改用氢键数选池
thresholds=pAE_interaction<10、pLDDT>90、氢键数>11、RMSD<0.5、SAP<45、ddG<-40（作者自述按 campaign 调整）；部分扩散加噪 5–25/50 步、实用 <25 步；strand 指定使通过比例提高 >50 倍（23→1,192，约 51 倍）
md_used=否
qm_used=否
experimental_methods=Golden Gate→E. coli 96 孔自诱导表达+Ni 磁珠→单点 BLI→滴度全局拟合 Kd；CD 热熔；all-by-all BLI 特异性；SSM 酵母库+多轮 FACS+NGS 算 SC50；X 射线晶体学（amylin-18/22、G3BP1-11）；HeLa 线粒体共定位（含 IL2RG CRISPR 敲入替换）；PhaseScan 微流控相分离图；亚砷酸盐压力颗粒；ThT+负染 EM 纤维抑制/解聚；EndoTag(ASGPR/IGF2R) 内吞+溶酶体共定位；磁珠亲和富集+LC-MS/MS 回收率
pipeline_counts=每靶 ~10,000–50,000（序列输入）或 ~10,000（strand 指定）扩散设计 → 48–96 送测/靶 → 命中 amylin 96→4、CP 96→1(后 95→6)、VP48 95→1、BRCA1 41→2、FUS 94→3、G3BP1 78→5、prion 48→1、IL-2RG 94→1 → 部分扩散 5–50,000/靶再优化（amylin 174→107）
hit_rate=逐靶 1–6 个命中（分母 41–96）；计算侧通过率 strand 指定 >50 倍提升；作者未给跨靶平均命中率
best_metric=Kd 3.8 nM（amylin-68n αβ，最优）；G3BP1-11 11 nM、PRI28 14 nM、CP-35 28 nM、VP48 39 nM、BRCA1_ARATH 52 nM、IL-2RG-30 97 nM、FUS 520 nM；amylin 回收率 62.2%(血浆)/53.5%(PBS-CHAPS)
cost_or_stat_note=单条骨架 RFdiffusion 约 25–30 s（1×RTX2080 或 A4000、1 CPU 核、~8 GB RAM）；ProteinMPNN <0.5 s/CPU；结合体长 80–150 残基；过滤阈值按 campaign 变动、精确值在 Supplementary Tables 1–5（未取）
role_in_timeline=把 [B09]/[B08] 的自洽性闸口推到「靶构象未知」的 IDP/IDR 场景：生成端不再假设靶几何（sequence-input 扩散 + 二级结构接口指定），并第一次把 partial diffusion 当作亲和力成熟的计算步骤；同时暴露漏斗边界——柔性靶即便全套过滤，湿实验命中仍是个位数/几十，Kd 停在数十 nM
source_pointer=data/interim/baker_lit/ft/idp_binder2025.txt（SHA 28c744c6b8f688ed…）；sources/baker.md:278-288
CSV回填-->
