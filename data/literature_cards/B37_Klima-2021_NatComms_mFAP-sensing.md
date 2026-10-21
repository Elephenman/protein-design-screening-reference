# [B37] 把"传感功能"变成可筛选读出——de novo 设计荧光激活蛋白（mFAP）的功能改造

Klima JC, Doyle LA, Lee JD, Rappleye M, Gagnon LA, Lee MY, Barros EP, Vorobieva AA, Dou J, Bremner S, Quon JS, Chow CM, Carter L, Mack DL, Amaro RE, Vaughan JC, Berndt A, Stoddard BL, Baker D（华盛顿大学 IPD / Fred Hutch / UCSD）
Nature Communications 2021, 12:856 · DOI 10.1038/s41467-020-18911-w · PMID 33558528 · PMCID PMC7870846
开放获取（CC BY 4.0）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B37**（组：Baker组） |
| 本文取回方式 | Europe PMC `fullTextXML`（`inventory.json` 记 `fetch_channel=epmc_fulltext`，URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7870846/fullTextXML`），2026-10-16 本地抓取 |
| 本地全文（唯一底稿） | `data/interim/baker_lit/ft/fap2021.txt`，152,878 B，SHA-256 `7c3b6f18652270ef83666d6abfa749a1ae94240e1ae61ad442057a583a43194b` |
| 身份复核 | 文件头部自带 `PMC7870846 / 33558528 / 10.1038/s41467-020-18911-w / Incorporation of sensing modalities into de novo designed fluorescence-activating proteins / Klima Jason C … Baker David`，与 CSV 行 B37 的 DOI、PMID/PMCID、标题、作者逐项一致（同一篇，未挂错行） |
| 对照底稿 | `sources/baker.md:483–495`（原卡）。本卡在其基础上补齐：完整的多轮文库漏斗数字、Rosetta 十项过滤阈值的原值、E. coli 挑克隆口径、失败轮次（mFAP3–mFAP8）、split 片段的 Kd 下限、CP 漏斗 4000→12、以及 MD/QM 的确切位置 |
| 证据级别 | **全文级**（本卡全部引句均可在 `fap2021.txt` 里逐字命中；见第 9 节） |
| 未取到的部分 | 全部补充信息：Supplementary Figs 1–23、Supplementary Tables 1–3、Supplementary Data 1–17（**每个突变库的实际理论多样性、据此挑取的克隆绝对数、每轮筛选的孔数与重复数都在 Supplementary Data 里，正文只给了倍数关系**）、Supplementary Note 1/2/3、Supplementary Movie 1–3、Source Data。凡涉及这些的地方本卡明写"正文未给绝对数"或"原文未给阈值"，不外推 |

## 1. 这篇到底解决什么（一句话）

前一篇（Dou 等 2018，Nature 561:485，本文参考文献 1）用 Rosetta 从头设计出一批 β-桶蛋白（mFAP），本身不发光，但**结合小分子 DFHBI 后把它稳在 cis-平面构象、于是亮起来**。这篇做的事：把"发光"这件事当成一个**可以直接在 96 孔板里读的表型**，然后围着它做六个方向的改造——更亮、挑生色团、对 pH 敏感、对 Ca²⁺ 别构敏感、可拆成两段当可逆的蛋白互作报告器、可环化重排（cpmFAP）。它的价值不只在传感器本身，而在**"功能即读出"这套筛选口径**：在 extended loop 那条线上，十项 Rosetta 物理指标只砍掉 99.2% 就把剩下的交给人测，真正的决定层是"粗裂解液 + 加底物 + 酶标仪读数"，于是漏斗每一层的数字都可数：extended loop 线 7,748 → 59 → 5，linker 线 1,140 → 385 → 25，环化线 4,000 → 12，分裂线 7 种切点 → 4 组定量。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **同一个荧光读出同时混着"表达量""结合亲和力""激活效率"三件事，改亮就会掉亲和力**。
   现象/证据：为了把亮度做上去，他们在 mFAP2.5 上做了一轮 7 位点组合库（往 β-桶疏水核里塞更多甲基），拿到 mFAP2b；紧接着正文单独一句承认代价 —— "It was demonstrated that mFAP2b had ~10-fold weaker affinity for DFHBI than the initial mFAP2 design."
   **他们做了什么**：不回头改打分函数，而是**改读出的物理条件**——把生色团浓度降到接近或低于 Kd，让"亮"变成"低底物下还亮 = 亲和高"。原文两轮都写明了浓度："Screening for fluorescence intensity of the phenolate state of DFHBI using a relatively low-DFHBI concentration (555 nM) resulted in mFAP2b(V13A,M15F), known as mFAP2a" 与 "Screening for fluorescence intensity of DFHBI-1T using a low-DFHBI-1T concentration (250 nM) resulted in mFAP2a(W27I,W93F), also known as mFAP10"。
   留下的代价：亮度与亲和力无法再用一个数排序，Table 1 里每个复合物都要各自补测消光系数（1 个数据点按 Beer 定律估）、积分球绝对量子产率（10 次扫描）、8 个技术重复的滴定 Kd —— 判据的歧义被**后移成了表征成本**。另一点值得记下：亲和力并没有永久丢掉，Table 1 显示 mFAP2a 对 DFHBI 的 Kd 回到 0.15 µM（起点 mFAP2 ~0.18 µM），mFAP10 更到 0.017 µM —— **代价不是不可逆，而是要多花两整轮文库才换回来**（从 mFAP2b 到 mFAP10 共 +5 与 +6 两个位点轮次）。

2. **通量最大的那一层（粗裂解液直接读数）本身就是最不可靠的一层**。
   现象/证据：筛选流程是"挑克隆 → 深孔板培养 → IPTG 诱导 → 裂解 → 离心取上清 → 加生色团 → 酶标仪读数"，阳性判据只有一句："Clones that demonstrated greater than an approximately twofold change in fluorescence intensity between CaCl 2 and EGTA conditions were Sanger sequenced"（Ca²⁺ 那轮），正文没有给这一轮的重复数、孔内本底分布或阴性克隆的假阳率；只有被确认有荧光的克隆才测序（"Clones that demonstrated fluorescence were Sanger sequenced via colony PCR of overnight cultures"）。而后续表征图里多处是单次测量（Fig. 4a–c 图注："Normalized fluorescence intensities ( n  = 1) are fit to a sigmoid function"）。
   **他们做了什么**：用"挑克隆数 = 4 倍理论多样性"堆冗余（"The number of E. coli colonies picked for functional screening was approximately 4-fold the theoretical diversity of each library."），再在下游用纯蛋白复测 + 测序序列回溯把单孔噪声筛掉。
   留下的代价：**每库理论多样性与实际克隆绝对数只写在 Supplementary Data 3–9 里，正文未给绝对数**，本卡不外推；因此这一层无法做"每孔成本/每命中成本"的核算。

3. **Rosetta 物理指标对"有没有功能"几乎没有预测力**。
   现象/证据：extended loop 那一轮，7,748 条设计按十项 Rosetta 指标过滤后剩 59 条 —— "Only 59 designs with extended loops built onto loops 1, 3 and 7 of mFAP2b passed the filter criteria for experimental testing"；送测后功能命中只有 5 条 —— "We identified five extended loop7 variants that maintain the β-barrel fold and are compatible with DFHBI binding"。计算层通过率 0.76%，功能层命中率 8.5%，端到端 5/7,748 ≈ 0.065%。
   **他们做了什么**：不去调那十个阈值，而是**把实验筛出来的 5 条当成可用元件库**，用自写脚本穷举它们的 linker 组成 —— "An in-house script (Supplementary Note  3 ) was written to prune the experimentally validated extended loop7 sequences one residue at a time"，得到理论多样性 1,140 的组合 linker 库，再用荧光直接筛。等于承认这一层"计算只能定规模，不能定功能"。
   留下的代价：linker→别构方向之间没有任何预测模型，后续每一层都靠穷举 + 湿测。

4. **拆成两段后片段裸露疏水面，可溶性和亲和力双双塌方**。
   现象/证据："As the split mFAP fragments would have solvent-exposed hydrophobic patches that could hamper solubility, we initially tagged split mFAP fragments to maltose-binding protein (MBP) to improve soluble expression levels." 补合滴定更糟：片段 Kd 低到测不出平台 —— "resulted in reconstitution of fluorescence at high-protein concentrations, but the signal did not plateau even at the highest concentrations tested"，于是只能给下限："The estimated split mFAP fragment dissociation constants ( K d values) are ≥281 µM for m12 and m38, ≥22.0 µM for m14 and m58, ≥232 µM for m16 and m78, and ≥354 µM for m17 and m8"。
   **他们做了什么**：① 先上 MBP 标签救可溶性；② 放弃"用片段亲和力做传感器"这条路，改为**把两个互补片段各自融到 nM 级高亲和对上**（BCL2 家族蛋白与其设计结合体，"high affinity ( K d  ≃  1 nM) designed binding partners"），靠蛋白互作把两段局部拉到一起，读出因此变成"互作发生 = 复桶 = 发光"："the fluorescence increased linearly until reaching a plateau at equimolar concentrations of complementary split mFAP fragments"。
   留下的代价：片段亲和力仍是 ≥281 µM 这种量级，作者自己在 Table 3 里把它写成相对 splitFAST 的**弱 2 个数量级**（"(similar to splitFAST but with ~2 orders of magnitude lower fragment affinities)"），即"可逆"是拿"结合很弱"换来的。

5. **正别构还是负别构，事前无法从序列推出来**。
   现象/证据： grafting 之后方向完全由 linker 决定 —— "we found that Ca 2+ binding was allosterically coupled to DFHBI binding" 但方向"depending only on the amino acid sequence of the linkers"，而同一个 EF-hand 换 linker 会翻向。
   **他们做了什么**：把"正/负"当成两个平行分支各自穷举，让两条谱系互不干扰：单 EF-hand 的正/负 linker 分别再去接 2 个 EF-hand（PDB 1FW4，理论多样性 385），负别构的 2-EF linker 再去接 4 个 EF-hand（PDB 1PRW 钙调蛋白，理论多样性 25）。方向与强度最后靠事后结构 + MD 解释（共结晶 6OHH 找到 K101 与 DFHBI 的直接氢键；突变掉就掉 ~21 倍亲和）与自由能面偏置（构象选择）。
   留下的代价：方向是**筛出来的不是设计出来的**；机理证据只在 EF1p2_mFAP2b 这一条上有（一个结构、一组 MD），其它变体没有。

6. **在体灵敏度对 GCaMP6f 完全不是对手**。
   现象/证据：Table 2 的实测峰 |ΔF/F₀| —— mFAP 三条 0.12±0.092、0.42±0.14、0.46±0.12，GCaMP6f 是 11±1.8。正文承认："the Ca 2+ -responsive mFAPs have lower fluorescence dynamic range at the DFHBI concentrations used, but are highly photostable"。
   **他们做了什么**：三层应对——① 不拼 ΔF/F，改拼**工作点**：把 DFHBI 浓度设在 (Kd⁺·Kd⁻)^(1/2)（两态解离常数的几何平均值，原文记号 K d + ⋅ K d − 1 / 2），"To optimize detection sensitivity and photostability while compromising on fluorescence dynamic range"（明写牺牲动态范围）；② 把负别构变成优势读出（同一方向的读出，既有 FP 传感器是下降的）："as existing Ca 2+ -responsive fluorescent protein sensors targeted to the SR report Ca 2+ effluxes as decreases in fluorescence signal"，他们用负别构变体靶向肌浆网（SR），把"钙外排"报成**信号上升**；③ 用高亲和变体（EF4n_mFAP2b，Ca²⁺ Kd 7.0 µM）与作者声称的超过 500 倍亲和力跨度（Supplementary Table 2）覆盖不同浓度窗口。
   留下的代价：与 GCaMP 的绝对动态范围差距没有缩小，作者把它放进了 Discussion 的"现有 FP 传感器仍占优"清单。

7. **有一整轮文库整体失败，而且作者没有解释**。
   现象/证据：为继续提高酚式态亮度在 mFAP2a 上做 3 位点组合库，"a combinatorial library (Supplementary Data  8 ) was constructed at three positions of mFAP2a, resulting in designs mFAP3 through mFAP8"，结果 "However, these mutants were dimmer and demonstrated lower expression levels than mFAP2b or mFAP2a"。
   **他们做了什么**：放弃这一支的亮度目标，只保留一个副产品结论 "mFAP3 showed to be the brightest DFHO-binding variant"（即换生色团通道而不是继续改蛋白），下一轮直接换到 6 位点针对 DFHBI-1T 界面上做。
   留下的代价：**为什么变暗伴随表达量下降（折叠？包埋空腔？methyl 塞过头？）本文未解决**，正文没有对该轮做任何结构或热力学归因。

8. **作者自己给出的结构性天花板**。
   现象/证据："the engineering of useful fluorogenic sensors based on mFAPs is still in its early days"；"Currently, existing fluorescent protein-based sensors still have numerous advantages over mFAPs in brightness (e.g., EGFP is ~2.1-fold brighter than the mFAP10-DFHBI-1T complex)"；Table 3 的表头是大写形式的 Potential advantages（见第 5.3 条），Discussion 正文的原句为 "At this stage, the possible advantages of de novo designed mFAP sensors over existing fluorescent protein-based reporters are listed in Table 3"。
   **他们做了什么**：把主张从"更好"收缩到"有别的可用性"——更小、更光稳、可逆、可按时空需要现场加染料；并留一句可外推方法学："More generally, as brighter and more photostable fluorogenic compounds are developed, the methodologies described herein should be readily applicable to creating protein-based fluorogenic optical sensors from binders to these compounds"。
   留下的代价：亮度、Ca²⁺ 亲和、动态范围三项对既有 FP 体系**本文没有翻盘**；pH 线的比值动态范围（~250 倍）是本文唯一在核心指标上明显胜出的项目。

## 3. 方法与工作流程（输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **计算设计**：Rosetta / RosettaRemodel（β-hairpin loop 片段取自 RCSB PDB，自建 β-桶 loop 片段库；3-mer 与 9-mer 片段；blueprint 文件 + RosettaScripts XML 做 centroid  grafting → 侧链 Monte Carlo 重打包 → 全原子最小化）；Rosetta 把 DFHBI / DFHBI-1T 建模进口袋做**形状互补 vs 位阻**判断；EF-hand / 钙调蛋白嫁接（PDB 1NKF、1FW4、1PRW）；环化（cpmFAP）用 Rosetta 设计 de novo α-螺旋/无序 linker。
- **序列构建（文库侧）**：SwiftLib 设计简并密码子寡核苷酸 → IDT 合成 → 相同基因区的寡核苷酸**按理论氨基酸多样性等摩尔 pooling** → assembly PCR（Phusion）全长基因 → Gibson 克隆进 pET15b / pcDNA5/FRT/TO → Lemo21(DE3) 转化 → LB/抗板。extended loop 库的 loop1/loop3/loop7 三个子库**按各自理论多样性成比例混合**。
- **筛选闸口（真正做决定的那一层）**：E. coli 单菌落 → 1 mL 深孔板过夜 → 25 µL 转 1 mL 长 3–4 h → 0.5 mM IPTG 诱导 4 h → 2272 × g 离心 → 50 µL 裂解液（含 PMSF/DNase I/溶菌酶）25–37 °C 振 12–48 h → 澄清 → 15 µL 上清 + 185 µL 缓冲液（含指定浓度生色团）→ BioTek Synergy Neo2 酶标仪 endpoint 读数 → 阳性孔 Sanger 测序 → 最亮的进大规模纯化。
- **二级表征（把判据拆开）**：荧光滴定（8 个技术重复，单位点等温线非线性最小二乘拟合 Kd，误差为拟合值 s.d.）；积分球绝对量子产率（Hamamatsu C9920-12，每样 10 次扫描）；消光系数（1 个吸收数据点按 Beer 定律估）；pH 滴定与比值荧光 F_ratio（红移激发/蓝移激发之商）；CD（二级结构与热变性，220 nm，25→95 °C，2 °C 步长）；SEC-MALS（单聚态，ASTRA 7.2 加权平均分子量）；激光共聚焦光稳定性（固定 COS-7，~0.885 Hz、200 帧、4 个 ROI，对比 AcGFP1）；X 射线共结晶（EF1p2_mFAP2b–DFHBI–Ca²⁺，2.1 Å，PDB 6OHH）；活细胞/心肌细胞成像（HEK293 细胞外/胞质、hiPSC-CM 肌浆网，n = 10–15 ROI × 3 技术重复，~16.7 Hz）。
- **MD 与 QM 的位置（关键）**：MD 只在共结晶结构之后做机理，四条件（apo / Ca²⁺ / DFHBI / 两者）× 三独立重复 × 500 ns，前 100 ns 弃用，PyEMMA 聚 25 簇看自由能面；QM 只有 Gaussian 09 给 DFHBI 做几何优化以生成 GAFF/Antechamber 力场参数。**两者都不在筛选闸口**。没有 FEP/自由能微扰，没有任何"用计算预测功能命中率"的尝试。

### A. 亮度 / 生色团选择性这条线（逐轮文库漏斗，Methods 段 + Supplementary Fig. 1）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A0 | 前作的 mFAP1、mFAP2 | 选定起点 mFAP2 | 原文给出的选择依据：mFAP2 绝对量子产率 φc = 2.1%、对 DFHBI 酚式态 Kd ≈ 180 nM，两者都优于 mFAP1 | 1 个起点支架 |
| A1 | mFAP2 计算模型 | 依前作深度突变扫描图谱手工挑突变，构建 3 条预设变体（P50T,S52V / S52T / P50T,S52V,G100D） | CD 看 pH 2.93 稳定性、荧光看 pH 3.66 含 DFHBI 时的强度（原文未给数值阈值） | 3 条设计 → mFAP2(P50T,S52V) 定为 mFAP2.1 |
| A2 | mFAP2.1 | 建一个**最小定点突变库（SDM），15 个残基位点**，粗裂解液在 pH 3.66 与 pH 7.36 双读 | 判据 = 荧光比值 fold-change（式 2，λex 387/483 nm、λem 501/504 nm）从低 pH 到高 pH 的最大值 | 挑出 mFAP2.1(T50P) = mFAP2.2，比 mFAP2.1 高 ~1.3 倍 |
| A3 | mFAP2.2 | **两个并行组合库**：5 位点（提 loop7 刚性）+ 8 位点（优化 β-桶疏水核堆积） | 判据 = pH 7.36 酚式态 DFHBI 荧光强度（λex 484 nm、λem 505 nm；带 W27 突变的克隆改读 511 nm） | 两库各取最亮：mFAP2.3 = A100E,G101N,N102D,T104H（~1.1 倍）、mFAP2.4 = M27W,V39I,V57A,F93W（~3.4 倍）；两者突变合并成 mFAP2.5 |
| A4 | mFAP2.5 | 7 位点组合库（往核里塞更多甲基） | 判据 = 激发光谱（λem 525 nm）下的酚式态荧光 | 命中单个突变 V67I → **mFAP2b**：比 mFAP2.5 ~1.2 倍、比 mFAP2.4 ~1.3 倍；**代价：对 DFHBI 亲和力比最初 mFAP2 弱 ~10 倍** |
| A5 | mFAP2b | 5 位点组合库（芳香 + 脂肪同时packing，提去质子态亲和而不掉亮度） | 判据 = **低底物 555 nM DFHBI 下的酚式荧光**（把读出从"亮"改成"低浓度还亮"） | mFAP2b(V13A,M15F) = **mFAP2a**，低浓度下比 mFAP2b 亮 ~1.3 倍 |
| A6 | mFAP2a | 3 位点组合库（继续塞甲基 + 容纳 Y71W 的几何） | 判据 = 中性 pH 酚式态荧光 | **失败轮**：mFAP3–mFAP8 全部更暗且表达更低；只保留 mFAP3 作为最亮的 DFHO 通道变体（mFAP3+10 µM DFHO 比 mFAP2b+10 µM DFHBI 暗 ~10 倍） |
| A7 | mFAP2a | 6 位点组合库（改生色团结合口袋里紧邻 DFHBI-1T 的脂肪/芳香残基） | 判据 = **250 nM 低浓度 DFHBI-1T 的荧光强度** | mFAP2a(W27I,W93F) = **mFAP10**：绝对量子产率 23.7%（99.9% 生色团被结合条件下）、比 mFAP2–DFHBI 亮 17.5 倍、比游离 DFHBI-1T 激活 242 倍；亮度 15,900 M⁻¹cm⁻¹（Table 1 注：2.1x dimmer than EGFP） |
| A8 | A2/A3 两库中酚式态荧光最高的变体 | 把它们的 loop7 突变与疏水核突变**手工组合**成 14 条设计 | 判据 = pH 3.61 与 pH 7.34 之间荧光变化（Supplementary Fig. 5） | 14 条 → 其中 1 条即 **mFAP_pH**：pH 8.38→3.63 比值荧光 ~250 倍变化（对照 pHRed ~34 倍、pHluorin2 ~3.5 倍）；酚式/去酚式两态 Kd 近乎相当（~190 nM 与 ~160 nM） |

### B. 全新功能加装这条线（计算漏斗 + 湿测，正文与 Methods 都给了绝对数）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | b11、b32 两个 de novo β-桶支架 + 自建 β-hairpin loop 片段库（RCSB 来源） | RosettaRemodel 固定 loop1/3/5/7 两端，取 3-mer 与 9-mer 片段重建 loop | 判据 = **环能否成功闭合**（原文未给能量阈值） | **2,226** 条环闭合成功的设计 |
| B2 | B1 的 loop 坐标（.pdb） | 转成 Rosetta blueprint（指定氨基酸类型、二级结构、ABEGO 类型），重建到 mFAP2b 的 loop1/3/5/7 | 无（只是格式转换与建模） | **8,904** 份 blueprint |
| B3 | B2 的 blueprint | RosettaScripts：centroid 能量 grafting → 侧链 Monte Carlo 重打包 → 全原子笛卡尔最小化 | 无 | **7,748** 条设计 |
| B4 | B3 的 7,748 条 | 按脚本打分的十项设计指标过滤 | **geometry = 1; total_score_res ≤ -3.72714; holes ≤ -1.2729; pstat ≥ 0.755044; buns_sc_heavy ≤ 2; buns_bb_heavy ≤ 2; interfE ≤ -38.375; SC ≥ 0.734076; p_aa_pp ≤ -40.8947; omega ≤ 2.8757** | **59** 条送测（计算层通过率 59/7,748 = **0.76%**） |
| B5 | 59 条 extended loop 设计 | 粗裂解液 + DFHBI 荧光筛 | 判据 = 保持折叠且兼容 DFHBI 结合（有荧光） | **5** 条有效（功能层 5/59 = **8.5%**；端到端 5/7,748 ≈ **0.065%**） |
| B6 | mFAP2b 原 loop7 + B5 的 5 条实测有效 loop7 | 自写脚本"每次削掉一个残基"，EF-hand 两端各留至多 4 残基，N 端可选加 Gly、C 端可选加 Gly/Pro → 嫁接 1 个 EF-hand（PDB 1NKF）到 mFAP2b 的 loop7 | 判据 = 在 2 mM CaCl₂ 与 25 mM EGTA 两种条件下荧光变化 **>~2 倍**，达标的克隆才 Sanger 测序 | 理论多样性 **1,140** 条 linker → 得到正向与负向别构的单 EF-hand 变体（正文未给这一层的绝对命中数） |
| B7 | B6 中正向/负向别构的单 EF-hand linker | 组合采样，嫁接 2 个 EF-hand（PDB 1FW4，N 端螺旋按成功嫁接的单 EF 设计截短） | 同 B6（>~2 倍 CaCl₂/EGTA 荧光变化） | 理论多样性 **385** 条 linker |
| B8 | B7 中负向别构的双 EF-hand linker | 组合采样，嫁接 4 个 EF-hand / 钙调蛋白（PDB 1PRW） | 同 B6 | 理论多样性 **25** 条 linker；正文图注给出的 Ca²⁺ Kd：EF1p2 2,300 µM（正别构，单 EF）、EF1n 260 µM（负别构，单 EF）、EF2n 60 µM（双 EF）、EF4n 7.0 µM（四 EF，钙调蛋白），即 2,300/7.0 ≈ 330 倍跨度；作者另在 Supplementary Table 2 上称整体跨度 **超过 500 倍**，Hill 系数 ~1（GCaMP6f 为 ~2–3） |
| B9 | 有效变体 + mFAP2a 的核突变（A13,F15） | 把核突变并入别构变体 | 判据 = Ca²⁺ Kd 的改变方向 | 正别构方向 Ca²⁺ 亲和最多升 11.7 倍，负别构方向最多降 11.6 倍 |
| B10 | mFAP2b / mFAP2a 计算模型 + DFHBI-1T | Rosetta 把 DFHBI-1T 建模进口袋 | 判据 = **形状互补 vs 位阻**（mFAP2a 因 V13A/M15F 留出空腔可容 CF₃，mFAP2b 位阻） | 预测被实验滴定证实：mFAP2b 对 DFHBI 比 DFHBI-1T 亮 ~30 倍、亲和高 ~6.1 倍；mFAP2a/mFAP2/mFAP10 反而是 DFHBI-1T 更亮（~2.5–12 倍）但 DFHBI 亲和更高（~2.6–39 倍） |

### C. 分裂与环化这两条线（通量骤降、靠设计多样性取胜）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | mFAP2a 单链模型 | 手工在 β-hairpin 与 loop7 处找切点做二段式 split | 8 条 β-链 → **7** 种可能的二段式切法 | 7 种候选 split；片段先接 MBP 标签保可溶 |
| C2 | MBP 融合的各对片段 | 过量 DFHBI-1T 下做 β-桶补合实验 | 判据 = **高于本底的荧光激活倍数** | m12/m38 最高，比平均本底高 **7.34 倍**；减去本底后最亮/最暗组合差 **184 倍** |
| C3 | 四组片段对 | 相互滴定测补合 Kd | 判据 = 能否拟合出平台 | **未能给确切值**：信号不饱和，只能报下限 ≥281 µM（m12/m38）、≥22.0 µM（m14/m58）、≥232 µM（m16/m78）、≥354 µM（m17/m8） |
| C4 | m14/m58 | 把两个互补片段分别融到 BCL2 家族蛋白与其高亲和（Kd ≈ 1 nM）设计结合体 | 判据 = 等摩尔处出现荧光平台（互作把两段局部浓缩） | 转为**蛋白互作实时报告器**：竞争法可正向读结合（BCLXL/BCL2/BFL1 三对）、反向读解离（aBCL2 挤掉 m14_aBFL1）；三种异二聚体峰值倍数不同 → 说明互作几何本身影响复桶亮度 |
| C5 | 4 个最亮 bipartite split 的切点 | 用 Rosetta + 自写脚本做环化（切点在 loop2/4/6/7），并重设计 cpmFAP 两端各 2 个残基；de novo 结构化/无序 linker 融合原来相邻的 N/C 端 | 判据 = 按设计指标过滤排序后取前 12 条 | **4,000** 条 → **12** 条送测（另把 3 条 cp-mFAP2b 用 V13A/M15F 改回 mFAP2a 背景）→ 最亮 cp35-34_mFAP2a_12 达 mFAP2a 的 **~93%** 荧光、SEC-MALS 为单聚体 |
| C6 | 上述各轮阳性克隆 | 大规模纯化后逐一表征；把实测有效的 linker 反过来当作下一轮的组合母库 | 判据 = 各线自己的核心指标（亮度 / 比值动态范围 / 别构方向） | 下一轮理论多样性直接被上一轮命中数限制：1,140 → 385 → 25 |

**这套流程的骨架值得单独记住**：**决定谁是赢家的是湿实验孔板，不是计算分数**；计算只负责把规模压到"能挑克隆"的量级（7,748→59）。同时他们把读出的**工作点**当设计变量（底物浓度、pH、Ca²⁺/EGTA 双条件、比值而不是强度），于是"功能"变成了一个可以用一个数字排序的量。通量大的层（A2–A7、B5）用低信息量判据 + 冗余克隆；通量小的层（C2–C5）用高信息量判据 + 上一轮实测元件。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段/位置） |
|---|---|---|
| φc 2.1%、Kd ~180 nM | 起点 mFAP2 的绝对量子产率与对 DFHBI 酚式态亲和力（选它的理由） | "mFAP2 was chosen for optimization because it has the highest absolute fluorescence quantum yield" / "and highest affinity ( K d of ~180 nM) for the phenolate form of DFHBI compared to mFAP1"（Results 首段） |
| 12、10、11 个突变 | mFAP2a / mFAP2b / mFAP10 相对 mFAP2 各自累计的突变数 | "we obtained three brighter and chromophore-selective mFAP2 variants: mFAP2a, mFAP2b, and mFAP10 that incorporate 12, 10, and 11 mutations, respectively" |
| 15 / 5 / 8 / 7 / 5 / 3 / 6 个位点 | 七轮组合突变库的位点数（SDM、loop7 刚性、疏水核、塞甲基、提亲和、mFAP3-8 轮、DFHBI-1T 界面） | Methods 各轮：15（SDM）、5 与 8（两个并行库）、7（V67I）、5（mFAP2a）、3（mFAP3–mFAP8）、6（mFAP10） |
| ~1.3 / ~1.1 / ~3.4 / ~1.2 / ~1.3 / ~1.3 倍 | 各轮最亮变体相对上一代的亮度或比值提升（T50P、mFAP2.3、mFAP2.4、mFAP2b、mFAP2a、mFAP10 低浓度） | Methods 段首句 "Fluorescence screening of the SDM library at pH 3.66 and pH 7.36 revealed that the most pH-responsive mutant mFAP2.1(T50P)" 起，至 "known as mFAP10" 止的各轮结论句 |
| ~10 倍**变弱** | mFAP2b 对 DFHBI 的亲和力相对最初 mFAP2 掉了一个数量级（亮度提升的代价） | "It was demonstrated that mFAP2b had ~10-fold weaker affinity for DFHBI than the initial mFAP2 design" |
| 555 nM / 250 nM | 后两轮刻意选的低生色团浓度（把读出改成对亲和力敏感） | "using a relatively low-DFHBI concentration (555 nM)" / "using a low-DFHBI-1T concentration (250 nM)" |
| 23.7% / 17.5 倍 / 242 倍 | mFAP10–DFHBI-1T 的绝对量子产率、相对 mFAP2–DFHBI 的亮度增益、相对游离 DFHBI-1T 的激活倍数 | "The mFAP10-DFHBI-1T complex is the brightest, with 23.7% absolute quantum yield" 段 |
| 15,900 vs 33,600 M⁻¹cm⁻¹ | mFAP10–DFHBI-1T 亮度 vs EGFP 亮度（Table 1 注 "2.1x dimmer than EGFP"） | Table 1 |
| Kd：0.15 / 5.8 / 1.8 / 11 / 0.017 / 0.045 µM | mFAP2a、mFAP2b、mFAP10 各自与 DFHBI、DFHBI-1T 的 Kd（8 技术重复拟合） | Table 1 的 K d (μM) 列 |
| ~2.7 / ~2.5 / ~12 倍 与 ~30 / ~39 / ~2.6 倍 | 三者对 DFHBI-1T 的亮度优势 vs 对 DFHBI 的亲和力优势（方向相反） | Results 第二段滴定总结句 |
| ~250 倍 vs ~34 倍 vs ~3.5 倍 | mFAP_pH、pHRed、pHluorin2 的比值动态范围 | "mFAP_pH showed a marked ~250-fold-change in ratiometric fluorescence" / "a ~34-fold-change in F ratio from pH 8.38 to pH 4.79 for pHRed 20 and a ~3.5-fold-change in F ratio from pH 8.83 to pH 5.14 for pHluorin2 21" |
| ~190 nM / ~160 nM | mFAP_pH 对酚式与去酚式 DFHBI 近相当的亲和力（能做 pH 传感器的结构前提） | "The phenolic and phenolate forms of DFHBI had nearly equivalent affinities ( K d values) for mFAP_pH of ~190 nM and ~160 nM, respectively" |
| 2,226 → 8,904 → 7,748 → 59 → 5 | extended loop 这条线的逐层规模（环闭合 blueprint → blueprint 文件 → 设计 → 过筛 → 功能命中） | "from which 2226 designs with successfully closed loops were generated" / "resulting in 8904 Rosetta blueprint files" / "Seven-thousand seven-hundred forty-eight resulting designs were filtered" / "Only 59 designs with extended loops built onto loops 1, 3 and 7 of mFAP2b passed the filter criteria for experimental testing" / "We identified five extended loop7 variants" |
| 0.76% / 8.5% / 0.065% | 本卡按上行数字算出的：计算层通过率、功能层命中率、端到端命中率（**这三个是本卡的算术派生，不是原文给的**） | 由 59/7,748、5/59、5/7,748 计算 |
| geometry=1；total_score_res ≤ -3.72714；holes ≤ -1.2729；pstat ≥ 0.755044；buns_sc_heavy ≤ 2；buns_bb_heavy ≤ 2；interfE ≤ -38.375；SC ≥ 0.734076；p_aa_pp ≤ -40.8947；omega ≤ 2.8757 | 十项 Rosetta 设计指标的过滤阈值原值（本漏斗唯一一组写死的计算阈值） | Methods "Design of extended loop library" 段：原句为 "geometry = 1; total_score_res ≤ -3.72714; holes ≤ -1.2729; pstat ≥ 0.755044; buns_sc_heavy ≤ 2; buns_bb_heavy ≤ 2; interfE ≤ -38.375; SC ≥ 0.734076; p_aa_pp ≤ -40.8947; and omega ≤ 2.8757." |
| 1,140 / 385 / 25 | 三轮 linker 组合库的理论多样性（1 EF-hand / 2 EF-hand / 4 EF-hand） | "had a theoretical diversity of 1140 linkers" / "of 385 linkers" / "of 25 linkers" |
| >~2 倍 | Ca²⁺ 响应的主筛判据（2 mM CaCl₂ vs 25 mM EGTA 两条件荧光变化） | "Clones that demonstrated greater than an approximately twofold change in fluorescence intensity between CaCl 2 and EGTA conditions were Sanger sequenced" |
| 2,300 / 260 / 60 / 7.0 µM；Hill ~1 | EF1p2、EF1n、EF2n、EF4n 的 Ca²⁺ Kd 与 Hill 系数；作者称整体跨度超 500 倍 | Fig. 4 图注与 "Overall, the Ca 2+ -responsive mFAPs exhibit over 500-fold differences in affinity for Ca 2+" |
| 11.7 倍 / 11.6 倍 | 并入 mFAP2a 核突变后 Ca²⁺ 亲和的正/负向改变上限 | "increased Ca 2+ affinity by up to 11.7-fold for positively allosteric proteins and decreased Ca 2+ affinity by up to 11.6-fold" |
| ~21 倍 / ~29 倍 | K101A 点突变后 DFHBI 亲和（过量 Ca²⁺ 下）与 Ca²⁺ 亲和（过量 DFHBI 下）的下降 | "the K101A lysine-to-alanine substitution in EF1p2_mFAP2b reduces DFHBI affinity ~21-fold in the presence of excess Ca 2+" |
| 2.19 Å | 嫁接的 EF-hand 与 NMR 结构 1NKF（La³⁺）之间的 Cα-RMSD；共结晶分辨率 2.1 Å | Fig. 5 图注 / "at 2.1 Å resolution" |
| 7 种切点；7.34 倍；184 倍 | 8 链 β-桶的二段式 split 可能性数、最优组合高于本底的激活倍数、最亮/最暗组合之差 | "there are seven possible bipartite split mFAPs" / "m12 and m38 displayed the highest fluorescence activation above background, with 7.34-fold higher mean fluorescence intensity over mean background fluorescence intensity" / "had 184-fold higher mean fluorescence intensity than the dimmest fragment combination, m1 and m28" |
| ≥281 / ≥22.0 / ≥232 / ≥354 µM | 四组片段对的补合 Kd（只能给下限，因为最高浓度仍不饱和） | "The estimated split mFAP fragment dissociation constants ( K d values) are ≥281 µM for m12 and m38, ≥22.0 µM for m14 and m58, ≥232 µM for m16 and m78, and ≥354 µM for m17 and m8" |
| ≈1 nM；0.8 ± 0.5 nM / 320 ± 40 nM | 所用设计结合体（BCL2 家族）的亲和力级别；BCL2–aBCL2  cognate 与 BCL2–aBFL1 非 cognate 的 Kd（竞争法的前提） | "high affinity ( K d ≃ 1 nM) designed binding partners" / "the non-cognate BCL2–aBFL1 complex has a dissociation constant ( K d ) of 320 ± 40 nM, the cognate BCL2–aBCL2 complex has a K d of 0.8 ± 0.5 nM" |
| 4,000 → 12 → ~93% | 环化线：设计数 → 送测数 → 最亮 cpmFAP 相对 mFAP2a 的荧光强度 | "4000 resulting designs were filtered and sorted on design metrics. The top 12 designs were chosen for experimental testing" / "displayed ~93% of the fluorescence intensity of mFAP2a" |
| 6.2 / 3.5 / 6.1 倍（饱和 50 µM）；5.0 / 3.8 / 4.7 倍（亚饱和 500 nM） | mFAP2a–DFHBI、mFAP2a–DFHBI-1T、mFAP2b–DFHBI 相对 AcGFP1 的光稳定性提升 | "we found at 50.0 µM chromophore (saturating conditions) a 6.2-fold, 3.5-fold, and 6.1-fold improved photostability" |
| 0.12±0.092 / 0.42±0.14 / 0.46±0.12 vs **11±1.8** | ACh 刺激下三条 mFAP 构建体 vs GCaMP6f 的峰 \|ΔF/F₀\|（mFAP 用的 DFHBI 20–43.3 µM，GCaMP6f 0 µM）；ROI 数 15/10/15/12 | Table 2 |
| ~0.5 | 细胞外钙滴定（0→10 mM Ca²⁺）下的荧光变化倍数（ΔF/F₀） | "Titration of Ca 2+ from 0 to 10 mM final concentration under constant DFHBI concentration resulted in a fluorescence fold-change" |
| ~16.7 Hz（60 ms/帧）；96 ± 45 ms | 心肌细胞成像采帧率与"SR 荧光峰 → 收缩峰"的滞后（20 个收缩周期平均） | "The image acquisition rate in these experiments was ~16.7 Hz" / "Temporal analysis averaged over 20 cardiac contraction cycles revealed a 96 ± 45 ms" |
| 4 条件 × 3 重复 × 500 ns（弃前 100 ns）；25 簇；2.49 Å | MD 规模与聚类口径（唯一一处 MD，事后机理） | "Each of the four system conditions were simulated in three independent 500 ns replicates" / "jointly clustered into 25 clusters" |
| ~4 倍 | 每库挑取克隆数相对该库理论多样性的倍数（**唯一给通的湿实验通量口径，绝对数在 Supplementary Data**） | "The number of E. coli colonies picked for functional screening was approximately 4-fold the theoretical diversity of each library" |

## 5. 结论——作者说了什么

1. **功能可以被"加装"进一个已经设计好的支架**：亮度、生色团选择性、pH 响应、Ca²⁺ 别构、二段式可逆拆分、环化重排，六件事都只靠"改残基/接 motif/换 linker"，不需要重新设计折叠。摘要原句："We show through further design that the fluorescence intensity and specificity of mFAPs for different chromophores can be tuned, and the fluorescence made sensitive to pH and Ca 2+ for real-time fluorescence reporting."
2. **分裂式 mFAP 的最大卖点是可逆**："Bipartite split mFAPs enable real-time monitoring of protein-protein association and (unlike widely used split GFP reporter systems) are fully reversible, allowing direct readout of association and dissociation events."（摘要）——既能读结合也能读解离，这是既有 split GFP 做不到的方向。
3. **核心指标上各有胜负，作者自己列清楚了**：mFAP 胜在更小、更光稳（相对 AcGFP1 达 3.5–6.2 倍）、pH 比值动态范围（~250 倍 vs pHRed ~34 倍 / pHluorin2 ~3.5 倍）；输在亮度（EGFP 比 mFAP10–DFHBI-1T 亮 ~2.1 倍）、Ca²⁺ 亲和、ΔF/F 动态范围（vs GCaMP6f 差两个数量级）。
4. **方法学可以外推**："More generally, as brighter and more photostable fluorogenic compounds are developed, the methodologies described herein should be readily applicable to creating protein-based fluorogenic optical sensors from binders to these compounds." —— 只要有一种"结合后变亮"的化学物，这套筛选结构就能复用。
5. **作者自我定界**："the engineering of useful fluorogenic sensors based on mFAPs is still in its early days"；Table 3 的表头用词是 "Potential advantages"，即优势清单是**候选优势**不是已证明的替换。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的贡献不是任何一个传感器，而是"把功能变成一列可排序数字"这件事**。判据本身极便宜（裂解液 + 加染料 + 读一次酶标仪），所以每一轮都能承受"位点数少、克隆数多"的库。反过来说：他们能这么玩的前提是**功能与信号之间只隔一步物理耦合（结合→构象稳→发光）**，中间没有需要化学确证的中间产物。
2. **计算闸口在这里几乎没有决策权**。7,748 → 59 只砍掉 99.2%，而 59 → 5 完全由湿测定。十项 Rosetta 阈值看起来极严（小数点后五位），但**在本地这份全文里检索不到任何"把这些阈值挪动后看功能命中率怎么变"的分析**（搜索范围：本地全文整篇；检索词及计数为 receiver operating 0 次、ROC 作为独立词 0 次（17 次子串全在 Semrock / hydrochloric / processed 等词内）、discriminat 0 次、success rate 0 次、threshold 0 次、stringent 0 次、hit rate 0 次、false 0 次；补充材料未取回，不能排除补充里有）——**因此就本文可核验的部分而言，它是一组沿用性的工程参数，不是被验证过的判据**。这与 B09（binder 论文里 pAE_interaction 在百万条带标签数据上被逐项考过）形成鲜明对照。
3. **他们的库设计里藏着一条我们该学的原则：读出的工作点是设计变量**。555 nM / 250 nM 两次刻意把底物降到接近 Kd 以下，才让"亮度"变成"亲和力"的代理；Ca²⁺ 那轮的 CaCl₂/EGTA 双条件、pH 那轮的低/高 pH 双读，本质都是**用两个条件相减把无关变量（表达量）消掉**。任何单孔单次读数都会被表达量劫持。
4. **失败被"降维利用"而不是被解释**。mFAP3–mFAP8 那一轮整体变暗且低表达，作者没有归因，只是把 mFAP3 挪去当 DFHO 通道的最优件。extended loop 那轮 5/59 的命中率也没有回头改打分，而是把 5 条当 linker 元件库穷举。→ 对我们：**在小样本的轮次里，"失败的产物"最有价值的用法是当作下一轮的枚举母库，而不是当作模型修正的样本**（样本量根本不够修正任何东西）。
5. **"漏斗每层数字"这件事不需要大数据集也能做**。本文绝对规模其实不大（正文没给任何一层的克隆绝对数，只给了 59、12、25/385/1,140 这类设计/多样性数，以及挑克隆 = 4× 多样性这一条倍数口径），但作者把**每层的输入数、通过数、判据**逐层写清了。→ 对我们：一轮湿实验即使只有几个构建体，也完全可以在开工前就规定好每层报什么数；做不到不是因为样本少，是因为没提前定口径。

## 7. 局限与失败（作者的 + 我们读出的）

- **作者自承**：见 5.3 与 5.5——亮度、Ca²⁺ 亲和、动态范围三处未翻盘；且 Table 3 通篇是候选优势（表头用词 Potential advantages，Discussion 正文用词 possible advantages）。
- **我们读出、且原文没有闭合的四条**：
  1. **主筛判据 ~2 倍变化 大概率落在噪声里**。这一层是粗裂解液单孔读数：Methods 的 Screening libraries 一节（本地全文偏移 57089–59950，共 2,861 字符）**内含 0 处 technical replicate、0 处 n = 标注**，全篇 11 处 technical replicate 都落在图注与其他表征段落里；正文也没写阴性本底分布或假阳率。而下游表征图里确有单次测量（Fig. 4a–c 图注写明 n = 1）。从理论多样性 1,140 的 linker 库按 ">~2 倍" 挑正/负别构变体，这个阈值没有配套的噪声标定——**本卡认为这是全文最可疑的一条判据**（把握度：判据缺噪声标定=高，因为可直接核对段落；实际命中率是否被污染=中，补充材料未取回）。
  2. **每层通过数只给了倍数关系，没给绝对数**。挑克隆数 = 4× 理论多样性，但各库理论多样性只写在 Supplementary Data 3–9（本地未取），因此**无法核算每孔成本与每命中成本**，也无法判断 5/59 是否已经把所有可溶的算进去了。
  3. **MD 与 QM 都不在闸口，且只覆盖一个变体**。MD 只在 6OHH 共结晶之后解释别构（4 条件 × 3 × 500 ns），QM 只做 DFHBI 的几何优化以生成力场参数。所以这篇**不能**被引为"计算能预测功能"的证据，也不能被引为"MD 能筛活性"的证据。
  4. **"功能命中"的判据与"设计成立"的判据是同一件事的两面**：他们要的是"结合生色团后变亮"，读出就是"结合生色团后变亮"。这在传感类任务上成立（功能=可测表型），但在**催化类任务上不成立**——催化要的是转化率/turnover，而产物身份本身还需要化学确证，读出与被测功能之间存在额外一层不确定性（见第 8 节）。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **把"设计→表达→读出"每一层单独计数、单独命名瓶颈**。本文示范了最小可行版本：设计层 2,226/8,904/7,748 → 计算闸口 59（0.76%）→ 功能层 5（8.5%）→ 下游枚举 1,140/385/25 → 环化 4,000→12。我们唯一一轮湿实验也必须按同样的口径出四个数：**设计的构建体数 → 表达/可溶的构建体数 → 检出任何新产物峰的构建体数 → 产物身份被化学确证的构建体数**，且**失败的层要显式写出 0**（这与本项目"分层附录、每层一个 sheet、含失败"的既有规则一致）。
2. **把读出的"工作点"当设计变量，而不是固定条件**。mFAP 那两轮把底物降到接近/低于 Kd，才让"亮"变成"亲和"的代理。对我们：一轮里同一构建体应至少跑 **2 档底物（或 2 档酶量）**，因为单点读数无法区分"没活性"与"活性在线性区以下"；在 Km 未知时，用 2 档比值本身就可以给出"是否随底物单调"这个最低限度的机制信息。
3. **比值型读出抗表达量/加样误差**（他们用 F_ratio = 红移激发/蓝移激发之商、以及 CaCl₂ vs EGTA 双条件相减）。对我们：产物峰必须以**内标归一 + S2/S1 或 产物/剩余底物 的比值**报告，不用绝对峰面积；同时保留失活对照（同源点突变/去催化残基）作为"表达量相同但功能为零"的锚。
4. **功能读出必须能在未纯化的粗体系上跑**。他们全部高通量筛选都在**澄清裂解液**里完成，纯化只给极少数终点候选。对我们这一轮的硬约束是同一方向的：**如果判据要求先把蛋白或产物纯化，就等于把可用通量压到 0**，所以读出必须对粗反应液兼容（直接进样 LC-MS/MS、或粗液直接读），把大规模纯化留作事后确证而不是筛选闸口。
5. **通量小就别装成通量大**：他们通量最小的两层（7 种 split 切点、25 条 linker、12 条 cp）靠**结构多样性 + 上一轮实测元件**取胜，而不是靠样本数。我们一轮最多几个构建体时，正确做法是**让每个构建体占据机制轴上一个不同的位置**（不同候选机制/不同竞争副产物路径/一个失活对照），使"全为负"也能排除某些假设，而不是把重复花在同一个假设上。
6. **失败产物转成下一轮的枚举母库**（他们把 5 条实测有效 loop7 变成 1,140 条 linker 库）。对我们：一轮之后，无论命中与否，"实测表达了 + 实测有/无某产物"的构建体清单本身就是下一轮的种子集，其价值高于事后调打分函数。

**不可迁移 / 限制（为什么不能照搬）**

1. **他们的判据是"零中间步的内源信号"，我们的判据隔着一层化学身份确证**。荧光读数与被测功能（结合生色团并激活它）是同一个事件；我们的 LC-MS/MS 读数与被测功能（催化某步成键）之间还夹着"这个峰真的是这个产物吗"的鉴定问题。**因此他们的任何倍数阈值（>~2 倍、7.34 倍高于本底、184 倍、~93% 强度）都不许搬来做我们的判据**，连量纲都不对应。
2. **他们没有阳性对照的问题，我们有（而且方向相反）**。mFAP2 本身就是已知会亮的起点，每一轮都有"上一代最优件"作为阳性锚；**我们至今没有一条被产物化学确认过的天然 UAA 合成酶**，所以一轮实验里没有"一定能测出信号"的锚点。这带来两个具体限制：① 阈值只能自造（噪声底 + 空白），因而**任何命中都必须配失活对照**才能排除杂质峰；② 没有阳性锚时"检出率"没有分母意义，不许把它当命中率引用。
3. **不许把本文的计算通过率当我们的成功概率**。7,748→59→5 的 0.76% / 8.5% / 0.065% 是**结合并激活一个已知小分子**的概率，与"设计一个能催化高活化能反应的酶"不是同一件事；本文作者自己在 Discussion 里把这条线的成熟度定为 early days。DP2R 判据口径也禁止把 binder/传感器类的阈值与命中率转成 UAA 酶活判据。
4. **本文的 MD/QM 恰好证明它们不该进闸口**。MD 是共结晶之后的机理说明，QM 只做配体力场参数化。→ 若我们打算用 MD/xTB 做筛选层，**本文不提供任何支持**；它支持的定位是"湿实验之后解释为什么"。
5. **他们的漏斗可以被无限重放，我们的不能**。菌种、质粒（Addgene）、纯化蛋白都可复得，同一孔的克隆可以反复测；LC-MS/MS 样本消耗后不可复得，一轮就是死的。所以他们的"先粗筛一遍再复测"策略在我们这里必须换成**在进仪器之前就预登记每个样本要回答哪个假设**，并把重复内嵌进同一轮（同一样本分两管/两次进样），而这会直接吃掉构建体名额——这是本轮预算最紧的取舍，必须在实验设计里显式写清。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/fap2021.txt

- **本卡全部引句照着写的那一份**：`data/interim/baker_lit/ft/fap2021.txt`（Europe PMC `fullTextXML` 抽取后去标签的纯文本，2026-10-16 抓取，152,878 B，SHA-256 `7c3b6f18…43194b`）。本卡没有参考同一论文的其它抽取版本（本仓库里 B37 只登记了这一个 local 全文），因此不存在"两句之间夹的参考文献编号版本不同"的风险；卡内凡引句带 `20`、`21`、`37`、`47` 这类残留编号处，均按这份底稿原样保留、未做删除或跨接。
- **对照底稿（仅作行号指针，不作引句来源）**：`sources/baker.md:483–495`（B37 原卡）。本卡相对它的增量：Rosetta 十项过滤阈值的原值、7,748→59 与 4,000→12 两级漏斗、每库挑克隆 = 4× 理论多样性这一通量口径、555 nM / 250 nM 两次低底物筛选、mFAP3–mFAP8 的整轮失败、split 片段 Kd 的 ≥ 下限与 184 倍跨度、以及 MD/QM 的确切落点。**原卡把 hit_rate 记为 5/59，本卡复核后确认该口径为"功能层命中率"（5/59），并补出计算层 59/7,748 与端到端 5/7,748。**
- 全文结构定位（供复核）：Results 起于偏移 ~9191；Discussion 起于 ~39995；Methods 主体 ~44101–~135232（含 Design of brighter and pH-responsive mFAPs / Design of chromophore-selective mFAPs / Design of extended loop library / Design of Ca²⁺-responsive mFAPs / Design of split mFAPs and cpmFAPs / Synthetic DNA construction / Screening libraries / Fluorescence intensity assays / pH-dependent fluorescence assays / Circular dichroism / Quantum yield measurements / SEC-MALS / Molecular dynamics simulations / X-ray / 细胞成像）；Data availability ~128596；Code availability ~130168。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字/实验验证手段`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本/统计量引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only "B37" --no-report` 结果 **PASS B37 quotes=70/70**，退出码 0。过程记录：首稿有 5 条 MISS，全部是"用省略号截短引句"（SDM 首轮结论句、pHRed/pHluorin2 两句各截一半、Only 59 designs 句、split 片段 Kd 句），逐条换成从底稿复制粘贴的完整连续原句后转绿；随后 §7 又出现 1 条 MISS，原因是把 Table 3 的表头词顺手小写成 potential advantages（原文为大写 Potential advantages），已改为不用引号的转述。另两处规避：Rosetta 阈值清单前面夹着参考文献编号 47、清单内括号夹着编号 2，因此把 Seven-thousand seven-hundred forty-eight resulting designs were filtered 与 geometry = 1; total_score_res ≤ -3.72714; … 至 and omega ≤ 2.8757. 这两段拆成两条独立引句（前一条已在第 3 节 B4 行逐字引用，后一条在第 4 节阈值行逐字引用），不做跨编号拼接。**追加一次真实红→绿记录**：本卡在最后一次改动（给 §9 自检条目补写规避说明）时误把带省略号的省略式写法又放回了直双引号里，门禁当场判 `FAIL … 引句未逐字命中 … geometry = 1; …and omega ≤ 2.8757.`、退出码 1，改写为不加引号的段内指代后复跑回到 70/70、退出码 0——也就是"引句造假或偷懒会被机器抓到"这件事在本卡上是实际发生过的，不是声明。Fig. 3i 的 pHRed/pHluorin2 对照句原文含残留编号 20、21，引句按底稿原样保留。
- **本卡里不属于原文的数字**（显式声明，避免被当作原文引用）：0.76%（59/7,748）、8.5%（5/59）、0.065%（5/7,748）、330 倍（2,300/7.0）四个比例为本卡算术派生；各库"理论多样性 → 实际挑取克隆数"的绝对数原文未给（在 Supplementary Data 3–9），本卡未推算。
- 未取到的材料清单：Supplementary Figs 1–23、Supplementary Tables 1–3、Supplementary Data 1–17、Supplementary Note 1–3、Supplementary Movies 1–3、Fig 1–6 的 Source Data。第 4 节凡标注 Supplementary 的数值均转引自正文对它们的表述，未独立核对补充材料。

<!--CSV回填
work_type=论文
target=de novo 设计的迷你荧光激活蛋白 mFAP（结合并激活 DFHBI / DFHBI-1T / DFHO 生色团），在其上加装亮度、生色团选择性、pH 响应、Ca²⁺ 别构、二段式可逆拆分与环化重排六种功能模态
backbone_generation=以已发表的 mFAP2/mFAP2a/mFAP2b β-桶支架为起点做定点与组合突变（SwiftLib 简并密码子 + assembly PCR）；新功能层用 Rosetta / RosettaRemodel 自建 β-hairpin loop 片段库在 loop1/3/5/7 上重建、EF-hand 与钙调蛋白嫁接（PDB 1NKF/1FW4/1PRW）、Rosetta 设计 de novo linker 做环化与分裂位点手工设计
computational_filters=十项 Rosetta 设计指标（geometry、total_score_res、holes、pstat、buns_sc_heavy、buns_bb_heavy、interfE、SC、p_aa_pp、omega）+ 生色团在口袋内的形状互补 vs 位阻建模；功能判定完全交给湿实验（粗裂解液加生色团的酶标仪荧光读数、pH 比值 fold-change、CaCl₂ vs EGTA 双条件荧光变化、高于本底的补合激活倍数）
thresholds=geometry = 1; total_score_res ≤ -3.72714; holes ≤ -1.2729; pstat ≥ 0.755044; buns_sc_heavy ≤ 2; buns_bb_heavy ≤ 2; interfE ≤ -38.375; SC ≥ 0.734076; p_aa_pp ≤ -40.8947; and omega ≤ 2.8757；Ca²⁺ 主筛判据为两条件荧光变化 >~2 倍；低底物筛选浓度 555 nM DFHBI / 250 nM DFHBI-1T；挑克隆数 = 每库理论多样性的 ~4 倍
md_used=是，仅事后机理：从 6OHH 共结晶结构起算，apo / Ca²⁺ / DFHBI / Ca²⁺+DFHBI 四条件 × 3 独立重复 × 500 ns（各弃前 100 ns），PyEMMA 聚 25 簇看 loop7 构象自由能面，用来解释 Ca²⁺ 结合把体系推向荧光态；不进任何筛选闸口
qm_used=是，仅力场参数化：DFHBI 配体用 Antechamber + GAFF 参数化，几何优化用 Gaussian 09；无反应能垒、无 DFT 机理计算、无自由能微扰
experimental_methods=E. coli 深孔板表达 → IPTG 诱导 → 溶菌酶裂解 → 澄清裂解液 + 指定浓度生色团 → BioTek Synergy Neo2 酶标仪荧光 endpoint/比值 → 阳性孔菌落 PCR + Sanger 测序 → 小规模/大规模纯化 + SEC；下游表征：8 技术重复荧光滴定拟合 Kd、积分球绝对量子产率（每样 10 次扫描）、紫外吸收估消光系数、圆二色（二级结构+热变性）、SEC-MALS 单聚态、激光共聚焦光稳定性（4 ROI × 200 帧 vs AcGFP1）、X 射线共结晶 2.1 Å、固定/活 COS-7 与 HEK293 成像、hiPSC-CM 肌浆网钙瞬态成像
pipeline_counts=extended loop 线：2,226 环闭合成功设计 → 8,904 blueprint → 7,748 设计 → 十项指标过滤剩 59 送测（计算层 0.76%）→ 湿测得 5 条兼容 DFHBI（功能层 8.5%，端到端 0.065%）；linker 枚举线 1,140 → 385 → 25（理论多样性，实测命中数正文未给）；亮度线 7 轮文库位点数 15/5/8/7/5/3/6，其中 mFAP3–mFAP8 一轮整体失败；分裂线 7 种切点 → 4 组给出 Kd 下限 → m14/m58 嫁到 nM 级互作对；环化线 4,000 → 12 送测 → 1 条达母体 ~93% 强度；每库挑克隆数 = 理论多样性 × ~4（绝对数在未取回的 Supplementary Data）
hit_rate=计算过滤层 59/7,748 = 0.76%；功能层 5/59 = 8.5%；端到端 5/7,748 ≈ 0.065%（三个比例为本卡算术派生）；分裂片段最优组合 m12/m38 高于本底 7.34 倍；Ca²⁺ 线以 >~2 倍 CaCl₂/EGTA 荧光变化为主筛判据（原文未给该轮命中数、重复数与假阳率）
best_metric=荧光性能最优：mFAP10–DFHBI-1T 绝对量子产率 23.7%、亮度 15,900 M⁻¹cm⁻¹（比 EGFP 低 2.1 倍）、Kd 0.045 µM（对 DFHBI-1T）/ 0.017 µM（对 DFHBI），比游离 DFHBI-1T 激活 242 倍；pH 线最优：mFAP_pH 比值动态范围 ~250 倍（酚式/去酚式 Kd 各 ~190/~160 nM）；Ca²⁺ 线最优：EF4n_mFAP2b 的 Ca²⁺ Kd 7.0 µM（Hill ~1），在体峰 |ΔF/F₀| 0.46±0.12，仍低于 GCaMP6f 的 11±1.8
cost_or_stat_note=湿实验通量口径只给了倍数（挑克隆 ≈ 4× 库理论多样性），绝对孔数/测序数/每孔成本原文未记录；MD 为 4 条件 × 3 重复 × 500 ns（弃前 100 ns）；量子产率每样 10 次积分球扫描、消光系数仅按 1 个吸收点估；滴定 8 技术重复、Kd 误差为拟合值 s.d.；别构表征 Fig 4a–c 为 n = 1 单次；在体成像 n = 10–15 个 ROI × 3 技术重复；光稳定性 4 ROI × 200 帧 @~0.885 Hz；心肌细胞采帧 ~16.7 Hz；本文没有任何"每命中一个候选花多少机时/试剂钱"的核算
role_in_timeline=Baker 组 2019–2021 期把 de novo 设计从「折对结构 / 结合靶点」推进到「加装可测功能」的一环：以生色团激活作为可直接排序的读出，把 Rosetta 物理指标降为只压规模的前置闸口（0.76%），把湿测荧光当作真正的决定层；同时是「MD 与 QM 都出现在 Methods 里但都不在闸口」的典型样本（与 [B38]  oligomorphism、[B39] 构象动力学同一取向）。相对 binder 线（[B09] 在百万条带标签数据上逐项考核筛子），本文这一侧在可核验的正文里找不到"给计算判据做过阴阳性同域考卷"的分析（见 §6.2 的检索词与计数；补充材料未取回，不能排除补充里有）
source_pointer=data/interim/baker_lit/ft/fap2021.txt（SHA-256 7c3b6f18652270ef83666d6abfa749a1ae94240e1ae61ad442057a583a43194b，Europe PMC fullTextXML，PMC7870846）；对照底稿 sources/baker.md:483-495；PDB 6OHH；代码 https://github.com/klimaj/mFAPs 与 Rosetta/RosettaRemodel（rosettacommons.org）；质粒 Addgene（David Baker 页）
CSV回填-->
