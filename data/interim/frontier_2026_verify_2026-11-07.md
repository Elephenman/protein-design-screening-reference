# 独立复核：`frontier_2026_survey.md` 的 6 条高风险断言（逐条回一手来源）

复核日期 2026-11-07 · 复核者：独立代理（未采信调研代理的本地缓存，全部重新联网取证）
被复核文件：`A:\AITEMP\frontier_2026_survey.md`
本文件位置：`A:\AITEMP\frontier_2026_verify.md` · 缓存与抓取脚本目录：`A:\AITEMP\verify_20261107\`
**未修改任何项目文件**（`A:\Data\MD\projects\protein-design-screening-20261016` 全程只读）。

## 0. 成功判据（先定义"做对了是什么"）

一句话判据：**每条断言都配一段我从一手页面逐字抓到的原文（不是转述），并给出四值判定之一；模板可抄写的措辞只能覆盖被直接引语支持的部分。**
可判定性：若某数字在任何一手来源都找不到 → 判"无法核验"并写明被什么挡住；若找到但适用对象与断言不同 → 判"部分对"并写出真实对象。

取证方式（全部 2026-11-07 实际执行，命令与产出文件见 §7）：
`curl` 直取 doi.org 解析状态码、Crossref `api.crossref.org/works/<doi>`（题录 + 摘要）、Europe PMC REST（`search` / `fullTextXML`）、bioRxiv `...v<n>.full` 正文 HTML、`raw.githubusercontent.com`（按各仓库真实默认分支）、arXiv API + `arxiv.org/abs` 页面。

---

## 1. RF3：开源时间/许可 + 手性 88/84/76 + 三个阈值的真实适用对象

**判定：部分对。** 数字全部为真；三个阈值数字确实存在，但**适用对象被写错了**（不是"设计筛选默认阈值"）。

访问到的 URL：
- `https://doi.org/10.1101/2025.08.14.670328` → HTTP 200
- `https://www.biorxiv.org/content/10.1101/2025.08.14.670328v2.full`（80,576 字符正文，缓存 `rf3_v_v2.html`）与 `...v1.full`（81,085 字符，`rf3_v_v1.html`）
- `https://api.crossref.org/works/10.1101/2025.08.14.670328` → `"posted":{"date-parts":[[2025,8,14]]}`
- `https://raw.githubusercontent.com/RosettaCommons/foundry/production/LICENSE.md`
- `https://raw.githubusercontent.com/RosettaCommons/atomworks/main/LICENSE.md` → 404；`.../master/LICENSE.md` → 200
- `https://raw.githubusercontent.com/RosettaCommons/foundry/production/models/rf3/README.md`（34,126 字节）

**(a) 日期与 BSD 许可 —— 成立。** 原文（摘要）：
> "To this end, we release the AtomWorks framework ( https://github.com/RosettaCommons/atomworks ), together with curated training data, code and model weights for RF3 ( https://github.com/RosettaCommons/modelforge ) under a permissive BSD license."

许可文件原文（Foundry，覆盖权重）：
> "BSD 3-Clause License
> Copyright (c) 2025, Institute for Protein Design, University of Washington.
> This copyright and license covers both the source code and model weights referenced for download in the README file."

口径提醒：能证到的是"预印本发布于 2025-08-14 且论文/仓库声明 BSD 放出权重"；**权重是否在 2025-08-14 当天上线，我没找到一手时间戳**（`files.ipd.uw.edu` 的 ckpt 未取到目录时间）。模板写"2025-08-14 预印本声明 BSD 开源（含权重）"，不要写"当天上线"。

**(b) 手性 88% / AF3 84% / Boltz-2 76% —— 成立，逐字对上。** 原文：
> "We find that after making these improvements, the network predicts the correct chirality for 88% of ligand chiral centers within our test set, compared to 84% for AF3 and 76% for Boltz-2 without inference-time guidance ( fig. 2a )."

图注口径（分母）："We first cluster all small molecules in our test set by CCD code and average the percentage of correctly predicted centers within each cluster."（按 CCD 聚类后取均值，非逐化合物计数）

**(c) 三个阈值的数字 —— 存在；适用对象 —— 断言写错了。** 原文（ supplements §A.2.2 "Distillation Datasets" → 小标题 "RNA Distillation"）：
> "Structures were predicted using an earlier version of RF3, grouped into bins based on length (5-nt bins), and filtered by output confidence metrics. Predictions were selected based on the union of two criteria: (1) the five predictions with the lowest predicted design error (pDE) scores per length bin, and (2) all predictions with pDE scores below a length-adjusted threshold defined as pDE ≤ ln(0.075 · length). A final filter was applied to retain only sequences with pLDDT ≥ 0.62 and pAE ≤ 15."

这段的**任务对象是 RNA**，用途是**筛掉低置信的预测结构来构造蒸馏训练集**（数据侧），不是"筛设计模型/筛设计批次"。`pDE` 在全文只出现在这一段（3 处命中其实是同一句重叠窗口），正文主结果里没有把它当设计筛选闸口。

同一段后面那句蛋白-DNA 阈值也是数据蒸馏用途（不是"复折自洽性主闸口"）：
> "Structures of the protein-DNA complexes were predicted using either RFNA [ 31 ], a fine-tuned version of RF-allatom [ 4 ], or RF-3, then filtered for high-confidence (mean pLDDT > 80, mean interface PAE < 10)."

**(d) "官方文档"这条退路也走不通。** 我对 `foundry/README.md`、`models/rf3/README.md`、`models/rfd3/README.md`、`models/rfo/README.md` 四个文件全文 grep `0.075` / `0.62` / `pDE` / `pae < 15`：**0 命中**。RF3 README 里唯一带默认数值的过滤参数是算力节流用的：
> "**`early_stopping_plddt_threshold`** *(optional)*: The average all-atom pLDDT value estimated after a single recycle that will trigger early-exit for that prediction. Defaults to `0.5`."

另外我把 RFD3 预印本正文（`https://www.biorxiv.org/content/10.1101/2025.09.18.676967v1.full`，86,483 字符）也 grep 过：`pLDDT`/`0.075` 命中 0 次 —— 调研笔记里"自家设计阈值"这条不能挂到 RFD3 上。

**模板可用措辞（可直接抄）**：
> RF3（预印本 2025-08-14；代码/数据/权重按 BSD-3 放出，Foundry 的 LICENSE.md 明确权重适用同一许可）报告其配体手性中心正确率 88%，AF3 84%，Boltz-2（不加推理引导）76%；该数字为按 CCD 聚类取均值的 in silico 指标，不是湿实验指标。
> 注：`pDE ≤ ln(0.075·len)`、`pLDDT ≥ 0.62`、`pAE ≤ 15` 出自该论文补充材料 §A.2.2 的 **RNA 蒸馏集构造**，用途是过滤预测结构以生成训练数据，**不是设计筛选阈值**；模板若要用它当设计闸口，必须标"借用，非原文用途"。

**证据级别**：能证明 = 上述 a/b/c 三条引语。不能证明 = 这三个阈值适用于设计筛选；不能证明权重上线日期。尚缺 = Baker 组任一**设计**批次上用 pDE/pLDDT/pAE 作阈值的正文表格（需 RFD3/CaGE 正文的方法学表，本轮 Science 版为订阅墙）。

---

## 2. Boltz-2：正向基准 + 三条负面结果是否各有一手来源

**判定：部分对（正向全部 CONFIRMED；三条负面都成立，但"500× 那条的一手来源不是你在题里给的两个 DOI，而是我新找到的 ChemMedChem 一篇）。**

访问到的 URL：
- `https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1.full`（Boltz-2 正文，缓存 `boltz2_v1.html`）
- `https://api.crossref.org/works/10.1021/acs.jctc.6c01334` → 存在：*Reliability of AI Methods in Drug Discovery: Evaluation of Boltz-2 for Structure and Binding Affinity Prediction*, J. Chem. Theory Comput., vol 22, pp 7811–7824, issued 2026-07-29, Wan/Zhang/Xue/Coveney
- `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13472093/fullTextXML`（JCTC 正文，72,532 字符，`jctc_ft.xml`）
- `https://export.arxiv.org/api/query?id_list=2512.06592` 与 `https://arxiv.org/abs/2512.06592` → "On fine-tuning Boltz-2 for protein-protein affinity prediction", 2025-12-06
- `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=("15-PGDH" AND "Boltz-2")` → hitCount 1，PMID 42894262
- `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13677808/fullTextXML`（15-PGDH 论文正文，47,019 字符）

**正向 ① FEP+ 四靶标 Pearson 0.66 —— 成立。** 原文：
> "On the 4-target FEP subset, Boltz-2 achieves an average Pearson correlation of 0.66, outperforming all available inexpensive physical methods and ML baselines. Remarkably, Boltz-2 approaches state-of-the-art free energy simulations, while running more than 1,000× faster"

四靶标身份与分母（正文数据节）："a 4 targets subset (CDK2, TYK2, JNK1, P38; curated in the protein-ligand-benchmark [ Hahn et al., 2022 ]) with 87 neutral compounds"；防泄漏口径："The training sets are filtered to exclude proteins with ≥ 90% sequence identity to any protein in the FEP+ benchmark"。

**正向 ② CASP16 盲测 140 对 —— 成立。** 原文：
> "Additionally, we include the CASP16 affinity challenge [ Gilson et al., 2025 ], a rigorous blind benchmark featuring 140 protein–ligand pairs across two targets. Here, while participants were given several weeks and used a range of ad-hoc machine learning and physics-based tools, we ran Boltz-2 out-of-the-box with no fine-tuning or input curation. Yet, Boltz-2 outperforms all top-ranking participants by a clear margin."

注意"超过全部参赛队伍"的原文严格说是 "all **top-ranking** participants"（表 14 是 "the top-6 highest ranked participants"），不是全部提交者。模板应写"超过全部排名靠前的参赛方案"。

**负面 ① top-100 相关性≈0 —— 成立，一手来源 = JCTC 10.1021/acs.jctc.6c01334。** 原文：
> "no correlation is observed between the initial Boltz-2 predictions and the ESMACS calculations for the top 100 compounds selected ( Figure a,b,e,f), no matter what saturation ( Figure ) and/or protonation states assigned for the compounds. The Pearson and Spearman correlation coefficients are close to zero."
> "The selection of top 100 compounds significantly reduces the variance of the Boltz-2 predicted binding affinities (within 1.0 kcal/mol of each other), which is likely to be smaller than the model's inherent uncertainty, making the correlation mathematically co[nstructed to collapse]"

全局数值（同一文）："While Boltz-2 yields a moderate correlation for TNKS2 (Pearson r = 0.45 and Spearman ρ = 0.46, see Figure ), it exhibits more limited accuracy for 3CLPro ( r = 0.24 and ρ = 0.25)."
分母："16780 compounds for 3CLPro and 21702 compounds for TNKS2"。
**必须一起抄的口径**：对照是"binding free energies derived from the physics-based ESMACS protocol"，即**模拟自由能，不是实验活性**。
顺带核验调研笔记的三条引语（都在该文）：两头互相关 "Pearson correlation coefficients of 0.21 and 0.25 for 3CLPro and TNKS2"；"Almost all compounds are predicted by Boltz-2 to have binding affinities below −4 kcal/mol, even though many are assigned very low binding probabilities"；可复现性 "Pearson r of 0.913 and 0.962"；"no universal threshold exists due to the system-dependent nature of the overestimation"。
小误差：调研笔记把该文标题写成 "**On the** Reliability of AI Methods…" —— 那是 arXiv 预印本标题（`https://arxiv.org/abs/2603.05532`，2026-03-02，我确认可访问）；期刊正式版标题无 "On the"。模板引期刊时按正式标题。

**负面 ② 跨系列看不到 500 倍提升 —— 成立，但一手来源不是 arXiv 2512.06592 / JCTC，而是我新定位到的这篇（调研笔记当时判为"缺一手 DOI、只能算线索"，现已补齐）：**
**DOI `10.1002/cmdc.70531`（ChemMedChem），PMID 42894262，PMCID PMC13677808，"Evaluating Machine Learning Affinity Prediction Methods on Novel Lead Optimization Data: A 15-PGDH Case Study"。** 摘要原文：
> "Boltz-2 performed well on series most similar to published inhibitors in its training, achieving accurate cofolding (median ligand RMSD ≤0.81 Å) and rank order. However, for a series exploring a new region of the binding pocket, Boltz-2 sometimes generated less accurate poses and predicted all ligands in the series to be less potent than a published exemplar, despite experimental potency gains of up to 500x."

正文原文（把"系列 3"和 FEP+ 对比也坐实了）：
> "Dodda and colleagues trained a bespoke 2D ML model on initial FEP+ data … 11 of 12 selected compounds (Series 3 here) were equipotent to or up to 500x more potent than the parent compound, with the 12th selected as a deliberate negative control."
> "Relative to the FEP+ approach used by Dodda and colleagues ( ρ = 0.70 ), Vina showed moderate pooled correlation ( ρ = 0.45 ). Boltz-2's pooled correlation ( ρ = 0.31 ) was considerably lower than its within-series performance on Series 1, 2, and 4, and significantly lower than FEP+ ( p adj < 0.05 )."
> "The drop in Boltz-2's performance upon pooling reflects a Simpson's paradox-like effect [ 11 ]: even when the model ranks compounds reasonably within series, systematic between-series biases degrade the overall correlation."

这是三条负面里**唯一以真实实验活性为对照**的一条（另两条是计算对照），对模板的分量最重。

**负面 ③ PPI 亲和力回归输给序列基线 —— 成立，一手来源 = arXiv 2512.06592（MLSB 2025 workshop 语料，未见期刊版）。** 摘要原文：
> "We adapt Boltz-2, a state-of-the-art structure-based protein-ligand affinity predictor, for protein-protein affinity regression and evaluate it on two datasets, TCR3d and PPB-affinity. Despite high structural accuracy, Boltz-2-PPI underperforms relative to sequence-based alternatives in both small- and larger-scale data regimes."
> "Our results echo known biases associated with training with structural data and suggest that current structure-based representations are not primed for performant affinity prediction."

作者：James King, Lewis Cornwall, Andrei Cristian Nica, James Day, Aaron Sim, Neil Dalchau（+Lilly Wollman, Joshua Meyers）；提交日期 2025-12-06。

**模板可用措辞（可直接抄）**：
> Boltz-2 亲和力头：4 靶标 FEP+ 子集平均 Pearson 0.66（87 个中性化合物，训练集已剔除 ≥90% 同一性蛋白）；CASP16 亲和力轨道 140 对/2 靶点盲测零微调，超过全部排名靠前的参赛方案（作者原话 "all top-ranking participants"）。
> 三条一手负面：(1) 对 ESMACS 计算自由能，全局 r=0.45(TNKS2)/0.24(3CLPro)，但**top-100 内 Pearson/Spearman 接近 0**——因 top-100 预测值方差被压到 1.0 kcal/mol 内、小于模型内在不确定度（JCTC 10.1021/acs.jctc.6c01334，对照为模拟而非实验）；(2) 真实实验活性对照下，15-PGDH 探索新口袋的系列中 Boltz-2 把全部化合物判得比母体弱，而实验活性最高提升 500×，池化 ρ=0.31 显著低于 FEP+ 的 0.70（ChemMedChem 10.1002/cmdc.70531）；(3) 蛋白-蛋白亲和力回归 Boltz-2-PPI 在 TCR3d 与 PPB-affinity 上小样本与大样本两种设定均逊于序列基线（arXiv 2512.06592）。
> 结论口径：只能当"系列内相对排序器"，不能当绝对门槛或跨系列/跨靶标判据。

**证据级别**：能证明 = 上述全部引语与数值。不能证明 = 0.66/140 对可迁移到"蛋白设计漏斗末端命中率"；也不能证明 top-100 塌相关发生在**实验活性**为对照的场合（该文对照是 ESMACS）。尚缺 = 把 Boltz-2 亲和力放进 de novo 设计漏斗并给"命中率–阈值曲线"的前瞻研究。

---

## 3. Chai-2 湿实验口径 + BLI 阈值 + 无亲和力头

**判定：部分对（六个数字/阈值全部逐字成立；只有一处口径错误——miniprotein 不是 52 靶点的"子集"，是另选的独立 5 靶点面板）。**

访问到的 URL：`https://www.biorxiv.org/content/10.1101/2025.07.05.663018v1.full`（正文 71,145 字符，`chai2_v1.html`；v2/v3 返回 859 字节的空页，v1 是唯一可读正文）；`https://api.crossref.org/works/10.1101/2025.07.05.663018`（posted 2025-07-06，CC BY-NC）；`https://raw.githubusercontent.com/chaidiscovery/chai-lab/main/README.md`；`https://www.biorxiv.org/content/10.1101/2024.10.10.615955v1.full`（Chai-1 正文，51,527 字符）。

命中率与分母（抗体/纳米抗体）原文：
> "For each target and antibody format we select up to 20 designs for experimental validation ( Figure 3b ). Across the 52 total targets for which we have completed assays for scFv or VHH designs, we observe at least one binder for 26 of the targets, indicating that Chai-2 can create de novo antibodies for half of the proteins evaluated ( Figure 3b ). We observe an average hit rate of 15.5% across all designed antibodies (20.0% with VHH, 13.7% with scFv, Figure 1b and c ) – an improvement of two orders of magnitude over prior state of the art [ 22 ]."
摘要级同口径："We prompt Chai-2 to design ≤ 20 antibodies or nanobodies to 52 diverse targets, completing the workflow from AI design to wet-lab validation in under two weeks."（摘要写的是 "a 16% hit rate"，正文精确到 15.5%）

BLI 判定阈值原文（结果节 + 方法节两处一致）：
> "we classified positive binding hits as designs with binding-positive curve signature while requiring that the signal is both greater than 0.1 nm above background and greater than 300% of background."
> "Across all formats, designs with binding-positive curve signature, signal greater than 300% of the negative background signal, and signal greater than 0.1nm above background were classified as positive hits."

miniprotein 68% 与其**独立面板**身份原文：
> "Beyond antibody design, Chai-2 achieves a 68% wet-lab success rate in miniprotein design – routinely yielding picomolar binders."（摘要）
> "We select a separate panel of targets for each task; (1) a benchmark set from prior miniprotein studies to facilitate comparison, and (2) set of 52 novel antigens with no known antibodies in the Protein Data Bank"
> "Using the five aforementioned targets ( Table S1 ), we experimentally validate 20 designs for each from an initial prototype Chai-1d model, and 20-25 designs from Chai-2: PD-L1 (25); IL-7Ra (23); InsulinR (20); TNF α (22); PDGFR β (21)"

→ 即 miniprotein 分母是 5 靶点 × 20–25 条（合计 111 条 Chai-2 设计 + 每靶 20 条 Chai-1d 原型），**与 52 靶点抗体集互斥**。调研笔记把它写成"子集"，模板若照抄会让读者误算总分母。

"没有亲和力头"的证据（否证式检索，我按"全文 0 命中"取证）：
- Chai-1 正文（51,527 字符）：`affinity` **0 次**、`IC50` 0 次、`potency` 0 次（同文对照词 `DockQ` 出现 24 次，说明正文确实抓全了）。
- Chai-2 正文（71,145 字符）：`affinity prediction` / `predict…affinity` / `affinity head` / `IC50` / `K D prediction` 均 **0 次**；文中 K_D 全是 BLI 实测值（"A distribution of binding affinity measurements ( K D ) are shown for all discovered binders"）。
- chai-lab README：无亲和力预测条目。

**模板可用措辞（可直接抄）**：
> Chai-2（bioRxiv 10.1101/2025.07.05.663018，CC BY-NC，权重非商用）：52 个 PDB 内无已知抗体/纳米抗体结合剂的新抗原，每靶每格式 ≤20 条设计，平均命中率 15.5%（VHH 20.0%、scFv 13.7%），26/52（50%）靶点至少 1 条确认结合剂；命中判据 = BLI 曲线呈结合特征且信号 > 背景 +0.1 nm 并 > 背景的 300%。
> miniprotein 是**独立的 5 靶点面板**（PD-L1 25、IL-7Rα 23、InsulinR 20、TNFα 22、PDGFRβ 21 条 Chai-2 设计），湿实验成功率 68%；不要写成 52 靶点的子集。
> Chai-1/Chai-2 均无结合亲和力预测头（Chai-1 正文 0 次 "affinity"；Chai-2 只报实测 K_D），不得把 Boltz-2 的亲和力用法套到 Chai 上。

**证据级别**：能证明 = 上述全部。不能证明 = scFv/VHH 命中率平移到全长 IgG（作者自列局限）；不能证明"52 靶点 × ≤20"里每靶实际下单数（正文只给上界）。尚缺 = 第三方独立复现；Chai-2 第二篇 `10.1101/2025.11.29.691346` 正文。

---

## 4. ESM3：湿实验仅 GFP 一类 + 88 条/96 孔板 + 58% 的正确读法 + 仓库署名/权重状态

**判定：部分对（"88 条/96 孔板""GFP 一类""署名 Biohub、ESM3 权重降级"全部成立；但"esmGFP 与天然 GFP 约 58% 同一性"这个数字对象错了）。**

访问到的 URL：
- `https://api.crossref.org/works/10.1126/science.ads0018` → TITLE `Simulating 500 million years of evolution with a language model`，容器 `Science`，print 2025-02-21，作者 Hayes, Rao, Akin, Sofroniew, Oktay, Lin, Verkuil, Tran, Deaton, Wiggert…（Science 页面本身对 `curl` 返 403 订阅墙，题录与摘要取自 Crossref）
- `https://www.biorxiv.org/content/10.1101/2024.07.01.600583v1.full`（正文 227,562 字符，`esm3_full.html`）
- `https://raw.githubusercontent.com/Biohub/esm/main/README.md`（22,659 字节）
- `https://raw.githubusercontent.com/Biohub/esm/main/_assets/ESM3_README.md`（6,442 字节）

88 条 / 96 孔板原文：
> "We performed a first experiment with 88 designs on a 96 well plate, evaluating the top generations in each sequence similarity bucket. Each generated protein was synthesized, expressed in E. coli , and measured for fluorescence activity at an excitation wavelength of 485 nm ( Fig. 4B left)."
选 88 条的规则也在正文附录里给死了："select the best 88 designs across 8 buckets of sequence identity to our template among intervals of width 0.1 in range [0.2, 1 ]"。B8 弱命中："a design in well B8 … with only 36% sequence identity to the 1QY3 sequence and 57% sequence identity to the nearest existing fluorescent protein, tagRFP. This design was 50x less bright than natural GFPs"；复测同口径 "observed a similar level of brightness to Experiment 1 (50x less bright than natural GFPs) ( Fig. S20 )"。

**58% 的真实对象**（这是本题必须纠正的一条）：
> "Our new protein, which we have named esmGFP, has 36% sequence identity to Aequorea victoria GFP, and 58% sequence identity to the most similar known fluorescent protein."
> "A BLAST ( 54 ) search against the non-redundant protein sequences database and an MMseqs ( 55 ) search of ESM3's training set report the same top hit— tagRFP, which was also the nearest neighbor to B8—with 58% sequence identity, representing 96 mutations throughout the sequence."
Science 摘要同口径："we found a bright fluorescent protein at a far distance (58% sequence identity) from known fluorescent proteins"。
→ 36% = 对天然 *A. victoria* GFP；58% = 对**最近的已知荧光蛋白（tagRFP，一个人工设计变体）**。"与天然 GFP 58%"是错配。另有 "the closest wildtype sequence to esmGFP from the natural world is eqFP578 … which differs from es-mGFP by 107 sequence positions (53% identity)"。

"湿实验只有 GFP 一类"：正文里 `wet-lab` 0 次、`luciferase`/`LacZ`/`hydrolase` 类功能实验 0 处；`antibody` 6 次全部是训练数据语境（OAS）与 ESM3-open 的构成说明——"ESM3-open is a 1.4B-parameter model we trained without OAS antibody sequences"。功能验证确实只有 GFP 实验 1/实验 2。

仓库署名与权重状态原文：
- README 标题行：`# A world model of protein biology: ESMC, ESMFold2, & ESM Atlas`；链接域名为 `biohub.ai`、HF 命名空间 `biohub`，正文仍保留 "Prebuilt wheels for both are published in the [EvolutionaryScale wheels release]" 与 "our API migrated from forge.evolutionaryscale.ai to biohub.ai" —— 组织迁移的直接痕迹。
- ESM3 降级为附属页：README 第 37 行 "For information on using ESM3, see the [ESM3 README](https://github.com/Biohub/esm/blob/main/_assets/ESM3_README.md)."
- 权重降级：`_assets/ESM3_README.md` "The code for ESM3 is available from Github and weights for esm3-sm-open-v1 is available on [Hugging Face](https://huggingface.co/collections/biohub/esm3-model-family). Other weights are available when the model is accessed through Biohub."（即 7B/98B 不再开放下载，只有 1.4B 的 `esm3-sm-open-v1` 可下）

顺带核到 ESMFold2 的说法是**定性无数值**：README "ESMFold2 is validated in the lab across five therapeutic targets. Inversion of ESMFold2 enables generation of de novo minibinders and antibody-derived scFvs with high hit rates, nanomolar affinities, target specificity, and functional activity."（"high hit rates" 无数字——模板不得写成命中率）。

**模板可用措辞（可直接抄）**：
> ESM3（Science 2025-02-21, DOI 10.1126/science.ads0018；预印本正文 10.1101/2024.07.01.600583）的公开湿实验功能证据目前集中在 GFP 一个功能类别：实验 1 = 96 孔板上的 88 条设计（按对模板 1QY3 的序列同一性分 8 桶取 top），最佳弱命中 B8 比天然 GFP 暗 50×；esmGFP 与 *A. victoria* GFP 36% 同一性、与最近的已知荧光蛋白（人工变体 tagRFP）58% 同一性、相差 96 个突变。论文没有给出 ESM3 的抗体/结合剂湿实验命中数据。
> 现状：仓库已迁到 github.com/Biohub/esm，README 主标题改为 ESMC/ESMFold2/ESM Atlas，ESM3 文档降级为 `_assets/ESM3_README.md`；开放权重仅 `esm3-sm-open-v1`（1.4B），其余权重需经 Biohub 平台。

**证据级别**：能证明 = 88/96 孔板、36%/58%/96 突变、GFP-only、仓库与权重状态。不能证明 = ESM3 命中率（论文只报"哪条亮了"）；不能证明 ESMFold2 的 binder 命中率高低（README 只写 "high hit rates"）；不能把"公司停更/并购"当事实。尚缺 = 实验 2 下单条数（附表未取到）；ESMFold2 正文 `10.64898/2026.06.03.729735` 的命中分母。

---

## 5. RFD3 的 Science DOI 是否真解析到 RFD3 论文

**判定：CONFIRMED（DOI 真实、指向正确、"zero shot 96 construct" 与摘要逐字一致；但"96 构型"= 下单构型数，不是 in silico 分母，且摘要不给命中率）。**

访问到的 URL 与产出：
- `https://doi.org/10.1126/science.aeh2982` → 直接 `curl` 返回 **403**（science.org 反爬/订阅墙，不是 404）
- `https://api.crossref.org/works/10.1126/science.aeh2982` → `status: ok`，AAAS 注册，indexed 2026-11-04，reference-count 116
- `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:"10.1126/science.aeh2982"` → hitCount 1，PMID **42879533**

Crossref 记录原文：
> TITLE: `Atomic functional site scaffolding in biopolymers with RFdiffusion3`
> CONTAINER: `Science`
> AUTHORS: `Jasper Butcher, Rohith Krishna, Raktim Mitra, Seth M. Woodbury, Donghyo Kim, Rafael I. Brent, Yanjing Li, Nathaniel Corley, Andrew Favor, Anqi Chen, Paul T. Kim, Jonathan Funk, …`
> ISSUED: 2026-10-15

摘要原文（关键句）：
> "Here, we describe a generative artificial intelligence method for biopolymers, RFdiffusion3 (RFD3), which employs free atom diffusion to satisfy complex sets of atomic constraints more rapidly and accurately than previous methods across several challenges from enzyme design to RNA structure design. We demonstrate experimentally the power of the RFD3 pipeline for enzyme design by designing de novo phosphotriesterases with a complex active site architecture incorporating a carbamylated lysine coordinating two metal ions and zinc proteases specific for the transthyretin protein involved in amyloid diseases; in both cases we obtain active catalysts in zero shot 96 construct design campaigns."

→ 与调研笔记 §1.5 一致（笔记的作者串 "Kim, Brent" 实际是 "Donghyo Kim" 与 "Rafael I. Brent" 两人，别当成一人）。EPMC 无 PMCID ⇒ 正文不可公开取，笔记标 `ABS` 是对的，模板里不得扩写表格数字。

**模板可用措辞（可直接抄）**：
> RFdiffusion3 已见刊 Science（DOI 10.1126/science.aeh2982，2026-10-15，Butcher & Krishna 等，PMID 42879533；正文在订阅墙内）。摘要级可引：de novo 磷酸三酯酶（氨基甲酰化 Lys 配位两个金属离子）与抗 TTR 锌蛋白酶两类设计，"in both cases we obtain active catalysts in zero shot 96 construct design campaigns"（96 = 单次下单的构建体数，非计算候选数；命中率与催化效率数值摘要未给，不可外推）。

**证据级别**：能证明 = DOI 身份 + 上面那句摘要。不能证明 = 任何具体命中率/kcat/KM。尚缺 = Science 正文表格（订阅或找作者）。

---

## 6. Foundry README：默认链 + Boltz-2 是否被接进"打分/筛选位"

**判定：部分对。** 默认链成立；Boltz-2 确实在官方链里，但**位置不是"打分/筛选闸口"，而是 RFO 迭代优化环里的另一条结构预测分支**。

访问到的 URL：
- `https://api.github.com/search/repositories?q=foundry+org:RosettaCommons` → `RosettaCommons/foundry`，default_branch = **production**，pushed_at 2026-11-04（注意：`.../main/README.md` 是 404，必须在 production 分支取）
- `https://raw.githubusercontent.com/RosettaCommons/foundry/production/README.md`（10,770 字节）
- `https://raw.githubusercontent.com/RosettaCommons/foundry/production/models/rfo/README.md`（4,774 字节）

默认链原文（README 第 3 行）：
> "Foundry provides tooling and infrastructure for using and training all classes of models for protein design, including design (RFD3), inverse folding (ProteinMPNN) and protein folding (RF3)."

教程级证据（第 69 行）：
> "For an interactive Google Colab notebook walking through a basic design pipeline with RFD3, MPNN, and RF3, please see the [IPD Design Pipeline Tutorial](https://colab.research.google.com/drive/1ZwIMV3n9h0ZOnIXX0GyKUuoiahgifBxh?usp=sharing)."

Boltz-2 的真实角色（README 第 103–104 行 + models/rfo/README.md）：
> "RFOptimization combines RF3 gradient-guided sequence optimization, Boltz-2 structure prediction, and external ProteinMPNN/LigandMPNN sequence redesign."
> "Each cycle selects RF3 gradient-guided sequence optimization with probability `backprop_fraction`, or Boltz-2 structure prediction otherwise. MPNN then redesigns the unfixed residues of chain A, and the redesigned complex seeds the next cycle."
> "backprop_fraction: 0.5  # 1 = RF3 only; 0 = Boltz only; both still use MPNN"
> "In the Boltz branch, contiguous high-confidence regions are fixed instead."
> "RFO carries the **first** MPNN sample forward when `mpnn_num_seqs > 1`; it does not rank the samples."
> "Independent AlphaFold3 filtering is outside this pipeline."

最后两句是关键限定：RFO **不做样本排序**，且官方明确"独立的 AlphaFold3 过滤"在本管线之外 —— 所以"Boltz-2 接进打分/筛选位"不成立；成立的是"官方工具用 Boltz-2 做结构预测分支，并用它的高置信连续区段决定哪些残基固定"。另外 Foundry README 里 Boltz-2 只出现在 RFO 一处（grep 结果：`Boltz` 命中 1 行）。

RFO 自身也有预印本（README 的 bibtex）：Zhang, Wang, Thompson, You, Song, DiMaio, Baker, *RFOptimization: Guiding Design Optimization with All-Atom Structure Prediction*, DOI `10.64898/2026.09.04.749184`（本轮未读正文）。

**模板可用措辞（可直接抄）**：
> 官方装配线（github.com/RosettaCommons/foundry，默认分支 production；README 版权为 BSD-3-Clause，覆盖代码与 README 列出的权重）：README 自述覆盖 design (RFD3) / inverse folding (ProteinMPNN) / protein folding (RF3)，并提供 "a basic design pipeline with RFD3, MPNN, and RF3" 的 Colab 教程 —— 即 RFdiffusion3 → ProteinMPNN/LigandMPNN → RF3 是官方公开的默认链。
> 第三方 Boltz-2 只出现在第四个组件 RFO 内：每个循环以 `backprop_fraction` 概率选 RF3 梯度引导序列优化、否则用 Boltz-2 结构预测（默认 0.5，即两条分支各半），Boltz 分支用其高置信连续区段决定固定残基。RFO 不排序 MPNN 样本，且官方注明"独立的 AlphaFold3 过滤在本管线之外"。因此 Boltz-2 在官方链里的角色是**优化循环的结构预测分支**，不是终筛打分闸口。

**证据级别**：能证明 = README 三条引语。不能证明 = "Boltz-2 被用作设计终筛打分器"；不能证明"所有 Baker 课题都走这条默认链"。尚缺 = RFO 预印本正文（看 Boltz 分支对命中率的实际贡献）。

---

## 7. 额外任务：否定式断言的抽查与"搜索范围声明"审计

被抽查的两条（题面要求抽查 2 条）：**"RFSolo 无一手来源"**（§1.4）与 **"DockDesign 未找到一手来源"**（§6），另附带把 **LockMSF** 一起重跑。

我自己的重跑（2026-11-07，命令见 §8）：

| 名称 | EPMC ABSTRACT | EPMC TITLE | arXiv all: | Crossref query.bibliographic | 结果 |
|---|---|---|---|---|---|
| RFSolo | 0 | 0 | entries 0 | total-results 0 | 与调研笔记一致 |
| DockDesign | 0（一次因限流报错，重试 0） | 0 | entries 0 | total-results 0 | 与调研笔记一致 |
| LockMSF | 0 | 0 | entries 0 | total-results 0 | 与调研笔记一致 |

再补一条笔记没做的：**网页搜索 "RFSolo" protein design Baker** —— 返回全是中文科普聚合稿（163/腾讯新闻等），无一提到 RFSolo，无任何一手论文/仓库/文档 → 笔记的"未找到一手来源"经我独立复现成立。

**"是否声明了搜索范围"的审计结论：**
1. **大部分是否定式断言写得合规**：§1.4 与 §6 逐条列出了检索面（EPMC TITLE/ABSTRACT、arXiv all、Crossref、GitHub 仓库搜索）与返回值，§0 还给出了可复跑的检索式与四个接口；并且用的是"未找到一手来源"而非"不存在"。这类措辞模板可以抄。
2. **两处越界，必须改**：
   - §6 的 MolGen 行写 "**不存在该用途的方法**"；§9 第 11 条把六个名字打包成"没有一手来源，模板禁止出现"。前者是**无范围限定的全称否定**（其证据仅列了两个 GitHub 仓库 + "EPMC 蛋白设计语境 0"，未声明时间窗、未声明未覆盖 Google Scholar/专利/公司代号）。
   - §0 的总括句"对 §6 的六个'疑似不存在'名称，四个来源**全部返回 0 条**"与自家 §6 表格矛盾：DockDesign 行自己写了 GitHub 有 1 个个人库、IG-LLM 行有 arXiv `2404.15228` 的近名命中。**"全部返回 0"这句不得进模板**，真实状态是"EPMC/Crossref 精确名 0；GitHub/arXiv 有同名但无关的命中"。
3. **给模板的规则**（按你的要求显式标注）：**全称否定未声明搜索范围，模板里不得写成"不存在"**；只能写成"截至 2026-11-07，在 Europe PMC（TITLE/ABSTRACT 精确短语）、arXiv（all: 精确短语）、Crossref（query.bibliographic）、GitHub 仓库搜索四处均未检得一手来源；未覆盖专利库、Google Scholar 与闭源内部代号"。

---

## 8. 总表（判定 / 可抄措辞 / 证据级别）

| # | 断言 | 判定 | 可直接抄进模板的措辞（若可用） | 建议证据级别标签 |
|---|---|---|---|---|
| 1 | RF3 2025-08-14 BSD 开源；手性 88/84/76；默认阈值 pDE≤ln(0.075·len)、pLDDT≥0.62、pAE≤15（用于设计筛选） | **部分对** | "RF3 预印本 2025-08-14；论文声明 AtomWorks+RF3 代码/数据/权重以 permissive BSD 放出，Foundry LICENSE.md 为 BSD-3 且覆盖权重。手性正确率 88% vs AF3 84% vs Boltz-2(无推理引导) 76%，按 CCD 聚类取均值的 in silico 指标。" 阈值段另写："pDE≤ln(0.075·len)、pLDDT≥0.62、pAE≤15 出自该文补充材料 §A.2.2 **RNA 蒸馏集构造**（过滤预测结构以生成训练数据），非设计筛选阈值；作设计闸口使用属借用，须标注。" | 能证明=引语三条；不能证明=阈值适用于设计筛选、权重当日上线；尚缺=Baker 设计批次上用这三阈值的正文表格 |
| 2 | Boltz-2 亲和 0.66(FEP+4靶)、CASP16 140 对超全部队伍；三条负面(顶部100≈0 / 500×看不见 / PPI输序列基线)各有一手来源 | **部分对** | 正向照抄（含"outperforms all **top-ranking** participants"、87 个中性化合物、CDK2/TYK2/JNK1/P38、≥90% 同一性剔除）。负面照抄三条并各挂来源：JCTC 10.1021/acs.jctc.6c01334（top-100 "close to zero"，对照=ESMACS 模拟自由能，**非实验活性**）；**ChemMedChem 10.1002/cmdc.70531 / PMID 42894262**（500×，实验活性对照；Boltz-2 池化 ρ=0.31 vs FEP+ 0.70，Simpson 型）；arXiv 2512.06592（TCR3d+PPB-affinity，两种样本量设定均逊于序列基线）。结论写"只可作系列内相对排序，不可作绝对门槛" | 能证明=上述全部引语；不能证明=0.66/140 对可迁移到设计漏斗命中率、top-100 塌相关在实验活性对照下同样成立；尚缺=设计漏斗前瞻研究、arXiv 2512.06592 的期刊同行评审版 |
| 3 | Chai-2：52 靶点、≤20/靶、15.5%、26/52、miniprotein **子集**68%；BLI >+0.1 nm 且 >300% 背景；Chai 无亲和力头 | **部分对（仅"子集"口径错）** | 全部数字照抄，但 miniprotein 必须写成"**另选的独立 5 靶点面板**（PD-L1 25/IL-7Rα 23/InsulinR 20/TNFα 22/PDGFRβ 21 条，另每靶 20 条 Chai-1d 原型），68% 湿实验成功率"；命中判据逐字 "> +0.1 nm above background and greater than 300% of background"。亲和力一句写"Chai-1 正文 0 次出现 affinity、Chai-2 只报实测 K_D，二者无亲和力预测头" | 能证明=数字与阈值+无亲和头的否证检索；不能证明=scFv/VHH 命中率平移到全长 IgG、每靶实际下单数；尚缺=第三方复现、Chai-2 第二篇正文 |
| 4 | ESM3 湿实验基本只有 GFP（实验1=88 条/96 孔，esmGFP 与天然 GFP 约 58%）；仓库已署名 Biohub、ESM3 权重降级 | **部分对（58% 对象错）** | "esmGFP 与 *A. victoria* GFP **36%** 同一性，与**最近的已知荧光蛋白 tagRFP** 58%（96 个突变）；与最近天然野生型 eqFP578 53%。实验 1 = 96 孔板上 88 条设计（对模板 1QY3 同一性分 8 桶各取 top）；B8 弱命中、比天然 GFP 暗 50×。功能验证只有 GFP，无抗体/结合剂湿实验命中。仓库现为 github.com/Biohub/esm（README 主标题 = ESMC/ESMFold2/ESM Atlas，ESM3 文档移至 `_assets/ESM3_README.md`），开放权重仅 esm3-sm-open-v1(1.4B)，其余走 Biohub 平台。" | 能证明=88/96 孔、36/58/96 突变、GFP-only、仓库与权重状态；不能证明=ESM3 命中率、ESMFold2 binder 命中率（README 仅 "high hit rates" 无数字）、公司停更叙事；尚缺=实验 2 下单条数、`10.64898/2026.06.03.729735` 正文分母 |
| 5 | RFD3 已在 Science 见刊（10.1126/science.aeh2982），"96 构型零样本拿到活性催化剂"与摘要一致，且该 DOI 确实解析到 RFD3 论文 | **CONFIRMED** | 照抄："RFdiffusion3, Science, 2026-10-15, DOI 10.1126/science.aeh2982, PMID 42879533（Butcher J, Krishna R, Mitra R, Woodbury SM, Kim D, Brent RI, Li Y, Corley N, Favor A, Chen A, Kim PT, Funk J 等）；摘要原句 'in both cases we obtain active catalysts in zero shot 96 construct design campaigns'（96=单次下单构建体数；命中率与催化效率摘要未给，正文在订阅墙内）"。注：science.org 对脚本抓取返 403，题录由 Crossref/EPMC 双证 | 能证明=DOI 身份+该句；不能证明=任何命中率/kcat/KM；尚缺=Science 正文表格（订阅或作者索取） |
| 6 | Foundry README 把 Boltz-2 接进打分/筛选位；默认链 RFD3 → MPNN/LigandMPNN → RF3 | **部分对（默认链对，Boltz-2 的位置不对）** | "官方 README（production 分支）自述 design (RFD3) / inverse folding (ProteinMPNN) / protein folding (RF3)，并给出 'a basic design pipeline with RFD3, MPNN, and RF3' 的 Colab 教程 ⇒ RFD3 → MPNN/LigandMPNN → RF3 是官方公开默认链。Boltz-2 只出现在 RFO 组件：每循环以 backprop_fraction(默认0.5) 概率走 RF3 梯度优化或 Boltz-2 结构预测，Boltz 分支用其高置信连续区段决定固定残基；RFO 'does not rank the samples'，且官方注明 'Independent AlphaFold3 filtering is outside this pipeline' ⇒ Boltz-2 是循环内的结构预测分支，不是终筛打分闸口。" | 能证明=README/RFO README 三条引语；不能证明=Boltz-2 在设计漏斗末端承担打分筛选、所有 Baker 课题走默认链；尚缺=RFO 预印本 `10.64898/2026.09.04.749184` 正文 |
| 附加 | 否定式断言（RFSolo / DockDesign / LockMSF 无一手来源） | **抽查 3 条均复现 0 命中，措辞需限定** | 模板只写"截至 2026-11-07 在 EPMC(TITLE/ABSTRACT)、arXiv(all:)、Crossref、GitHub 四处未检得一手来源；未覆盖专利库/Google Scholar/闭源代号"——**全称否定未声明搜索范围，模板里不得写成'不存在'**（笔记 §6 MolGen 行的"不存在该用途的方法"、§0 的"四个来源全部返回 0 条"两处需按此改写） | 能证明=四个索引 0 命中可复现；不能证明=名称不存在；尚缺=若来源是二手材料，需其原始出处 |

### 对调研笔记的两处"补刀"（它自己标注为缺口，现已闭合）
1. 笔记 §8 最后一行"15-PGDH / 500× 没有一手正文，只能算线索，要进模板必须先找到原始 DOI" —— **原始来源已定位：`10.1002/cmdc.70531`（PMID 42894262, PMCID PMC13677808），正文可读且含 ρ=0.31 vs 0.70、Series 3、Simpson 悖论三点**，可直接升级进模板。
2. 笔记把 JCTC 那篇的标题记成 arXiv 预印本标题（"On the Reliability…"）。期刊正式版为 "Reliability of AI Methods in Drug Discovery: Evaluation of Boltz-2 for Structure and Binding Affinity Prediction"，JCTC 2026, 22(15):7811–7824。

### 未复核范围（诚实边界）
未读：Science 正文（aeh2982、ads0018 全文均在订阅墙，只取题录+摘要）、Chai-2 第二篇 `10.1101/2025.11.29.691346`、OpenFold3 技术报告 PDF、RFO 预印本、CaGE/AlphaProtein Novo/Metal Mer 等 §7 条目（题面未要求）。`10.64898/*` 系列 DOI 的存在性未逐个复核。

---

## 9. 复现命令（本轮实际执行，全部有本地缓存于 `A:\AITEMP\verify_20261107\`）

```bash
export PYTHONIOENCODING=utf-8
# DOI 解析与题录
curl -s -o /dev/null -w "%{http_code}\n" -L "https://doi.org/10.1101/2025.08.14.670328"   # 200
curl -s -o /dev/null -w "%{http_code}\n" -L "https://doi.org/10.1126/science.aeh2982"     # 403（science.org 反爬，非 404）
curl -s "https://api.crossref.org/works/10.1126/science.aeh2982"                          # 标题/作者/日期
# 正文抓取（bioRxiv 需带浏览器 UA，取 .full）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
curl -s -A "$UA" -L "https://www.biorxiv.org/content/10.1101/2025.08.14.670328v2.full" -o rf3_v_v2.html
curl -s -A "$UA" -L "https://www.biorxiv.org/content/10.1101/2025.07.05.663018v1.full" -o chai2_v1.html
curl -s -A "$UA" -L "https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1.full" -o boltz2_v1.html
curl -s -A "$UA" -L "https://www.biorxiv.org/content/10.1101/2024.07.01.600583v1.full" -o esm3_full.html
# 已刊正文走 EPMC（PMC13472093 = JCTC 评测；PMC13677808 = 15-PGDH）
curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13472093/fullTextXML" -o jctc_ft.xml
curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13677808/fullTextXML" -o pgdh_ft.xml
# 注：PPR1068521/fullTextXML 返回 500，故 RF3 走 bioRxiv HTML
# arXiv（必须 https；http 会返回 0 条）
curl -s "https://export.arxiv.org/api/query?id_list=2512.06592"
# GitHub（foundry 默认分支是 production，不是 main）
curl -s "https://raw.githubusercontent.com/RosettaCommons/foundry/production/README.md"
curl -s "https://raw.githubusercontent.com/RosettaCommons/foundry/production/models/rfo/README.md"
curl -s "https://raw.githubusercontent.com/RosettaCommons/foundry/production/LICENSE.md"
# 否定式断言复跑
for t in RFSolo DockDesign LockMSF; do
  curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=ABSTRACT:%22$t%22&format=json"
  curl -s "https://export.arxiv.org/api/query?search_query=all:%22$t%22&max_results=5"
  curl -s "https://api.crossref.org/works?query.bibliographic=$t&rows=5"
done
```
