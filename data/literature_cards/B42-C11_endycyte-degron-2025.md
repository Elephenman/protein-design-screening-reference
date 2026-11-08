# [B42; C11] EndoTag / pLYTAC：设计判据只买到「会结合」，细胞级功能全靠实验端重扫——漏斗账本在这里出现断层

Huang B, Abedi M, Ahn G, Coventry B, Sappington I, Tang C, Wang R, Schlichthaerle T, … **Cao L**, … Bertozzi CR, **Baker D**（华盛顿大学 IPD / Stanford / Novo Nordisk / UT Southwestern / Johns Hopkins / UCSF / Hubrecht / Harvard / Caltech / 西湖大学 / 里斯本 IMM，45 人）
Nature 2025, 638(8051):796–804（在线 2024-09-25，正式卷期 2025-02）· DOI 10.1038/s41586-024-07948-2 · PMID 39322662 · PMCID PMC11839401 · 预印本 10.1101/2023.08.19.553321
开放获取（CC BY 4.0）· https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11839401/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B42; C11**（同一篇论文在 Baker 组清单与曹龙兴组清单各登记一行；组：Baker组; 曹龙兴组） |
| 本地全文（本卡唯一引句底稿） | `data/interim/baker_lit/ft/endocytosis2025.txt`（103,860 B，160 个段落级长行；2026-10-16 抓取） |
| 文件头身份块复核 | PMC11839401 / 11839453 / PMID 39322662 / DOI 10.1038/s41586-024-07948-2 / NIHMS2029412，标题 Designed endocytosis-inducing proteins degrade targets and amplify signals —— 与 CSV 行标题一致 |
| 对照底稿（不作为引句源） | `sources/baker.md:552–563`、`sources/cao.md:185–201`（该两处的阈值句与本文措辞略有出入，见第 9 节） |
| 证据级别 | **全文级**（本卡 76 条独立逐字引句、按出现次数共 110 处，全部门禁逐条命中同一份 txt） |
| 未取到的部分 | Extended Data Fig. 1–9 与 Table 1 的原图数值、Supplementary Figs 1–23、Supplementary Tables 1–5、Source Data Fig. 2。凡引用这些的地方本卡明写「正文未给出，仅有正文描述」 |
| 抽取文本的特殊性 | 去标签后**参考文献编号留在句中**（例如 AlphaFold2 后紧跟 `25`、ProteinMPNN 后紧跟 `21`），HTML 实体未全部解码（`&lt;`）。本卡引句按该 txt 归一化（NFC + 实体解码 + 破折号/空白归一）后的原样复制，含这些编号，不做改写也不跨句拼接 |

## 1. 这篇到底解决什么（大白话）

已有的「把细胞外的蛋白拽进细胞里烂掉」技术（LYTAC 一类）都靠**天然的内吞配体**——M6P 走 IGF2R、GalNAc 走 ASGPR。这套东西有三个天花板：天然配体自己会触发别的信号、结合位点早被体内已有的配体占满、要多价化学修饰才好使（难放大生产）。这篇换成**全蛋白、可基因编码的人工内吞标签（EndoTag）**：先用 de novo 设计做出「只抓受体、不跟天然配体抢位点」的结合蛋白，再按每个受体的内吞机制**定制设计策略**——常驻循环型受体（sortilin、TfR）只要绑对非竞争位点就够；构象变化型（IGF2R）必须把受体的 domain 6 和 domain 11 强行拉到一起；成簇触发型（ASGPR）必须做成多价把受体凑成三聚体。然后把这些 EndoTag 与第二个结合模块（抗 EGFR minibinder、cetuximab、atezolizumab、抗 CTLA4、protein G、BCL2）融合成 pLYTAC，做受体降解、可溶蛋白清除、AND 逻辑门降解、细胞局部分泌降解、以及 SNIPR 合成信号通路的放大，最后进小鼠肿瘤模型。

**对本项目最要紧的一句话**：这是本调研里第一篇「设计目标不再是结合、而是让一个活细胞把膜蛋白吞进去烂掉」的论文，于是它把 B09 那套 AF2/pAE 阈值的**适用边界**摊开给你看——计算端判据买到的是「结合 + 折得对」，而功能端（内吞、降解）靠的是**连接肽长度、结构域间距、价态**这些没进过任何打分函数的自由度，全部要在实验端重扫一遍。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **「会结合」与「能触发内吞」是两件事，而且中间没有计算判据**。作者立题时就把这条讲清楚：抗体也能刺激内吞，但这是纯实验活——"Antibodies have been identified that stimulate endocytosis, but this can require considerable empirical screening for any target receptor"。而位点选择性那条更难：对 sortilin/TfR 这类常驻循环受体，"the challenge is not to actively induce endocytosis, but to bind to the receptor at a site that does not compete for the natural ligand"。 **应对**：把「机制类型」当成设计前置条件，为四类受体分别设三条不同路线（非竞争位点结合 / 强行拉近 D6–D11 / 多价成簇），而不是一条通用漏斗走到底。 **代价**：三条路线各自重新做一遍设计—展示—BLI—细胞摄取，没有一条能靠前一环的阈值直接推断后一环。
2. **柔性连接肽的几何完全在打分函数之外，只能扫**。原文自述失败模式："Longer linkers decreased the uptake level, whereas a shorter Gly-Ser (GS) linker abolished uptake"，作者的解释也是事后归因："suggesting that the orientation and distance of the two binding domains modulates IGF2R endocytosis"。更干脆的一条："Constructs with two copies of one minibinder (D6mb-linker-D6mb and D11mb-linker-D11mb) were not taken up"。 **应对**：先穷举（"To generate flexible IGF2R agonists, all combinations of GS linkers with various lengths linking D6mb and D11mb were modelled with AlphaFold2"），再用一条粗滤子把结构不像的丢掉："The designs with poor monomer plddt (plddt < 85) were dropped"；随后干脆换成**刚性融合**（motif 提取 + inpainting 把两个界面螺旋按受体构象焊死）。 **代价**：pLDDT 门只筛单体折叠，筛不出「能不能内吞」；从柔性到刚性这一段，命中率始终没有以「功能命中 / 送测数」的形式给出。
3. **亲和力最强的设计不是功能最强的设计，作者用两个反例承认了这点**。同一受体上的两种刚性设计亲和力排布完全不同："Different designs had distinct affinities for domain 6 and domain 11"——IGF_EndoTag3 是 6 nM（D6）/190 nM（D11），IGF_EndoTag4 是 15 nM（D6）/4.3 µM（D11），而功能上 "IGF_EndoTag3 was internalized similarly to IGF2 and twofold more efficiently than IGF_EndoTag4"。ASGPR 分支更直白：单体 binder 明明结合（ASmb1，2.7 µM），降解却不动——"resulted in a 40% decrease in total EGFR levels, whereas fusions to the monomeric ASGPR binder had little effect"。 **应对**：把「功能」写成可与亲和力解耦的独立变量——价态（2C/3C）、几何（刚性 fusion）、位点（正交于天然配体），并做机制验证："To determine the oligomerization state induced by AS_EndoTag, we mixed ASGPR and AS_EndoTag-3C at a 1:3 ratio and separated the generated species by size-exclusion chromatography (SEC)"，结果 "AS_EndoTag induced formation of a trimeric ASGPR complex as expected given the three ASGPR-binding sites"。 **代价**：SEC 只证明「能凑出三聚体」，没有给出亲和力/价态/摄取之间的定量关系，也没有任何预测模型。
4. **计算漏斗的中间段命中率没记全，分母在 sortilin 分支上自相矛盾**。Methods 给的数不能连成一条单调下降的链：先用 "21,000 binders were generated to each of 2 sites on the sortilin"，再 "we used a set of scaffold libraries to generate several million docks to each of the sites"，然后 "As in the protocol, 100,000 docks were sub-selected and sequence was designed"、"Helical motifs were extracted, and 3,000 designs were selected, grafted and subjected to further design"，最后 "This resulted in 42,000 designs that were tested experimentally"——3,000 之后反而变成 42,000（42,000 恰好等于 2×21,000，说明这几个数来自协议里不同层，不是同一条队列）。送实验之后更是一条黑箱：只报最终那条 "the highest affinity design (Sort_EndoTag) had a dissociation constant ( K d ) for Sortilin of 21 nM"。 **应对**：改用**独立实验通道**验证计算模型是否画对了界面，而不是补漏斗数字——N-糖基化块状扫描："All positions 10 Å away from the interface were screened using RosettaMatch"，几何过滤 "Computational models were minimized and filtered based on geometrical restraints, CST-score <5"，最终 "Four sortilin variants that introduce N-linked glycans close to the designed Sort_EndoTag interface blocked binding"。 **代价**：位点验证只能证明「界面大致对」，无法证明「设计判据在 42,000 条里把对的挑了出来」；本卡无法从正文算出 sortilin 分支的任何命中率。
5. **能算出分母的两条分支，命中率都掉到个位数百分比以下，而功能段仍无分母**。ASGPR：2,689 条进展示筛选只出 4 条，"We used yeast display for 2,689 designs that were predicted to bind ASGPR by AlphaFold2 25 followed by fluorescence-activated cell sorting (FACS) and next-generation sequencing to reveal four highly enriched designs"（4/2,689 ≈ 0.15%），且其中最强也只有 "the design with the highest affinity, ASmb1, bound to ASGPR with an affinity of 2.7 µM"。IGF2R 刚性融合："We tested 170 designs for which AlphaFold2 25 predictions matched the intended structures for binding to both IGF2R domains, and expressed eight designs that interacted with both domains in E. coli"（8/170 ≈ 4.7%）。 **应对**：不再指望单点亲和力，改从**结构自由度**（域间距/价态）与**受体选择**（组织分布不同）两端找回功能。 **代价**：8 条表达之后哪几条真能内吞，正文只报了 IGF_EndoTag3 与 EndoTag4 两条；「功能命中 ÷ 表达数」这个最关键的比值，全文没有给。
6. **自己的设计会挡住自己的通路，而且强弱不可预判**。IGF_EndoTag2 与内源 IGF2 抢位点："pre-incubation of cells with IGF_EndoTag4 did not inhibit IGF2 uptake or transport, whereas IGF_EndoTag2 did reduce IGF2 uptake"。而 M6P 位点被内源糖酶占满，天然构成容量上限："The M6P-binding site on IGF2R is largely occupied by M6P-tagged lysosomal hydrolases, limiting the maximal degradation capacity through this receptor"。 **应对**：正交性从**设计约束**里做出来（位点避开 M6P/IGF2 界面），并用 GNPTAB 敲除细胞验证不吃亏："the extent of binding of IGF_EndoTag2 was not altered by knockout of GNPTAB in UMRC2 cells"；同时接受「正交性与效力此消彼长」这一实测结论："indicating that orthogonality with IGF2 interaction can be achieved by modulating the binding affinity to IGF2R domain 11 while preserving the binding to domain 6"。 **代价**：这是一句调参式的经验规律，没有任何阈值或模型能让设计者在下单前知道该把 D11 亲和力调到多少。
7. **降解读数本身建立在 n=1 的单点实验上，作者把统计口径明写在 Methods**。"No statistical analysis was used to determine the sample size"，且 "Western blot experiments in vitro and BLI binding assays were conducted with sample size of one based on low variance from previous experience"。清除还有饱和天花板，作者在结果句里用括号直接承认：（"clearance may be limited by the number of available receptors"）。 **应对**：靠**遗传学对照**补统计的缺——受体敲除后降解消失（"Knockout of these receptors eliminated EGFR degradation by the corresponding EndoTags, demonstrating that degradation is dependent on the target receptors"），界面突变体失活、以及溶酶体共定位只在受体阳性的细胞里出现（"similar co-localization was not observed in HeLa cells that did not express IGF2R"）。 **代价**：40%/55%/78%/80%/85% 这些降解百分比既无剂量—响应曲线也无 n 与散布，跨受体的强弱排序不能当定量结论用。
8. **体内与转化端的两处未解决，作者自己在结论里点名**。免疫原性与剂量：「"it will be important to assess and, if necessary, reduce the immunogenicity of EndoTags"」，回收式催化变体只是设想（"catalytic versions that recycle to the plasma membrane following delivery of target to the lysosome could enable considerable dose sparing"）；信号放大只在自己的合成回路上成立："Further studies will be required to determine whether EndoTags can enhance signalling through endogenous pathways"。 **应对**：本文未解决（这两条被明写成 future work）。另可注意 Methods 与正文的分组不一致：正文写 "ATZ-IGF_EndoTag3 and ATZ-IGF_EndoTag4 were considerably more effective than ATZ alone in reducing tumour size and mass"，而动物 Methods 写的分组是 "with the mice been randomly assigned to receive ATZ, ATZ-IGF_EndoTag1 or ATZ-IGF_EndoTag4 and isotype as controls ( n = 6 mice per group)."——EndoTag1/EndoTag3 哪一个真进了这一组，正文未能自洽，本文未解决。

## 3. 方法与工作流程（可复现顺序）

### 用了哪些方法（工具箱）

- **骨架/界面设计**：Rosetta de novo binder 设计协议（Cao 系：PatchDock → RifDock → FastDesign/FastRelax）、Rosetta MotifGraft（螺旋模体嫁接）、**RFInpainting / protein inpainting**（在两个已固定的界面螺旋之间补一段连接骨架）、ProteinMPNN 出序列。
- **计算评估器**：AlphaFold2（单体 pLDDT、复合物 pAE_interaction、与设计模型骨架 RMSD）、RosettaFold LDDT（inpaint 区）、Rosetta ddG / relaxed_ddG、SAP（spatial aggregation propensity）、contact_molecular_surface、暴露疏水性 sap_score、净电荷优化到 −7。
- **实验筛选**：酵母表面展示 + FACS 双阳性门 + MiSeq 深测序；BLI（Octet RED96）测 Kd；SEC（受体寡聚态、抗体融合纯化）；N-糖基化块状扫描验证表位（RosettaMatch + CST-score）。
- **细胞级读出**：荧光标记蛋白 + 流式测细胞关联荧光（内吞代理）、共定位成像（LysoTracker / anti-LAMP2A）、Western blot 测总受体蛋白、磷酸化流式测 pERK、上清荧光测可溶蛋白清除。
- **逻辑门与合成回路**：Co-LOCKR（AND 门）、质粒瞬时转染后上清分泌、ortho-SNIPR（LHDB 胞外 + Notch 跨膜 + 转录因子→BFP）。
- **体内**：BALB/c 皮下 A20 淋巴瘤，瘤内给药，瘤组织 WB + 生存曲线。
- **没有用的方法**：分子动力学、量子化学、自由能微扰——全文无 MD/QM，机理层（内吞为何发生）不在其证据范围内。

### 工作流程表（A 段=设计，B 段=功能与转化；每步 输入 → 操作 → 判据/阈值 → 输出规模）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| A1 sortilin 位点 | sortilin 结构 + 已知互作界面清单 | 选两个非竞争表位（site1 五个残基 F92/V93/T546/T559/T561），要求暴露疏水斑块 + 避开已知互作 + 落在低 pH 构象变化区 | 定性选择，原文未给数值阈值 | 2 个位点，各位点 21,000 binders |
| A2 sortilin 生成 | 螺旋 scaffold 库 | 全库对接 → 子采样出序列 → 提取螺旋模体 → grafting 再设计 | 每点 several million docks；取 100,000 docks；选出 3,000 designs | 进入物理打分 |
| A3 sortilin 打分过滤 | 上一步 designs | Rosetta 界面打分过滤 | "Designs were filtered based on their Rosetta ddG and ContactMolecularSurface to the hydrophobic residues listed above"（阈值数值原文未给） | "This resulted in 42,000 designs that were tested experimentally"；酵母展示+FACS+测序；**中间命中数未报** |
| A4 sortilin 验证 | 终选设计 | BLI 定亲和力；N-糖基化扫描验表位 | 界面 10 Å 内位点用 RosettaMatch 找 NXS/T 植入点，几何过滤 CST-score <5 | 最强设计 Kd 21 nM；4 个糖基化变体全部阻断结合 |
| A5 IGF2R 单体 binder | PDB 6UM2（D6）与 1GP0（D11），以 IGF2 结合位点残基为 hotspot | FastRelax 精修 → PatchDock/RifDock → FastDesign → ddG + contact_molecular_surface → MotifGraft 重采样 → sap_score + 净电荷 | "Candidates passing previous filters were then filtered again with exposed hydrophobicity (sap_score) and optimized with a net-charge of -7"（其余阈值数值原文未给） | D6mb 41 nM；D11mb 190 nM → 优化后 D11mb2 6.5 nM |
| A6 柔性 IGF_EndoTag | D6mb + D11mb | 穷举 GS 连接肽长度 × 域顺序，AF2 建模 | "The designs with poor monomer plddt (plddt < 85) were dropped"（通过数未给） | 实验端：D11mb-GGS-D6mb（IGF_EndoTag1）可摄取；更长 linker 摄取下降、更短 GS 消失；同源二聚体不摄取 |
| A7 刚性 IGF_EndoTag | D6mb 两条界面螺旋 + D11mb 一条界面螺旋（或天然 IGF2 结合螺旋），以 6UM2 的内吞构象为几何模板 | 界面残基（3 Å 内）保持原样，随机扰动 D11 螺旋（平移 ≤5 Å、旋转 ≤10 radians）→ inpainting 补骨架 → ProteinMPNN 出序列（界面残基固定） | "The best inpainting outputs were selected by RosettaFold LDDT metrics (>0.5) for the inpainted region and used for sequence design with ProteinMPNN"；"After 2,000 sequences were generated for each ProteinMPNN input, designs were filtered by predicted Rosetta ddG"；"AlphaFold2 structure predictions of the designed sequences were filtered by the pLDDT metric (keeping those with pLDDT > 90)" + 亚埃骨架 RMSD；终闸 "Designs with ddG metrics less than -40 and spatial aggregation propensity scores less than 35 were selected for expression and experimental assays" | "We tested 170 designs for which AlphaFold2 25 predictions matched the intended structures for binding to both IGF2R domains, and expressed eight designs that interacted with both domains in E. coli"（8/170≈4.7%）→ 报出 EndoTag3（6 nM/190 nM）与 EndoTag4（15 nM/4.3 µM） |
| A8 ASGPR | ASGPR 晶体结构 PDB 5JQ1，避开糖结合位点 | Rosetta 对接 + **ProteinMPNN 出序列 + AF2 复评**（本文唯一写明 AF2 复合闸口用于生成的分支）→ 再采样一轮 → 终轮三指标 | "Designs with pae_interaction<10 and relaxed_ddg < -40 were selected for resampling with another round of protein-MPNN prediction followed by Rosetta Fastrelax"；终轮再过 pae_interaction / relaxed_ddg / sap_score，净电荷 −7 | 2,689 条送酵母展示 → 4 条高富集（4/2,689≈0.15%）→ ASmb1 Kd 2.7 µM |
| A9 ASGPR 功能化 | ASmb1 | 用 GS 连接肽串 2 个 / 3 个域；SEC 定寡聚态 | 无计算阈值（纯经验构造） | 相对单体摄取 2.5×（2C）与 4.5×（3C）；1:3 混合得三聚 ASGPR 复合物 |
| B1 内吞验证 | 各 EndoTag（AF647 标记或生物素+SA-AF647） | 37 °C 孵育 → 洗涤 → 流式测细胞关联荧光；共定位成像 | 归一化基准：荧光控制组（AF647-LHDB，正文称无内吞）或 SA-AF647 单独 | Sort_EndoTag **90×**（"there was a 90-fold increase in fluorescence compared with fluorophore-conjugated control"）；TfR_EndoTag **50×**（"with a 50-fold increase in cellular uptake over the LHDB scaffold control"）；EndoTag2 比天然 IGF2 高 **2×** |
| B2 正交性 | TfR_EndoTag / IGF_EndoTag | 与天然配体共孵育；GNPTAB 敲除细胞结合量对比 | 原文未给阈值 | TfR 分支不影响转铁蛋白结合与摄取；GNPTAB 敲除不改变 EndoTag2 结合；EndoTag4 不抢 IGF2、EndoTag2 抢 |
| B3 pLYTAC 降解 | EndoTag + 第二模块（EGFRn / CTX / ATZ / CTLA4mb） | 200 nM（部分 100 nM）孵 48 h → WB 测总蛋白 / 流式测表面 | 原文未给「算成功」的阈值；降解率取单点 | EGFR：AS 分支 40%、TfR 55%、sortilin 78%、IGF_EndoTag2 >80%；CTX–EndoTag1 在 10 nM 即 85%；PD-L1 48 h 消除 77%（4 h 内已起效）；CTLA4 3 h 降 45% |
| B4 机制依赖 | 受体 KO 细胞（SORT1/TfR/IGF2R）+ 界面突变体 | 平行实验对比降解 | 判据：降解消失 | KO 消除对应 EndoTag 的降解；失活变体使降解能力大致消失；EGF 诱导的 pERK 信号被 largely ablated |
| B5 可溶蛋白清除 | LHDA/LHDB 对、protein G + IgG-AF647；对照 protein G–M6Pn | 48 h 后取上清测荧光（647 nm），归一到无 EndoTag 组 | 原文未给阈值 | LHDB：MFI **40×**、48 h 溶液清除 50%；IgG：摄取 80×（K562）/360×（Jurkat），48 h 耗竭 70%；EndoTag 比 M6Pn 摄取高 2× |
| B6 逻辑门降解 | EGFR–Key + HER2–LOCKR + BCL2–EndoTag2 | AND 门只在双标记细胞上暴露 Bim 肽 | 原文未给阈值 | K562-HER2⁺ 中 EGFR 降解 80%；K562-HER2⁻ 中 EGFR 水平不变 |
| B7 分泌式降解 | IGF2R-KO HeLa 转染表达 EGFRn–IGF_EndoTag | 收上清直接处理 EGFR⁺ K562 | 判据：与纯蛋白等效 | 上清组与纯化蛋白组清除效率一致（正文未给百分比数值） |
| B8 信号放大 | LHDA–EndoTag + LHDB-SNIPR Jurkat | 剂量—响应 + 抑制剂剖分 | 判据：氯喹阻断、γ-secretase 阻断、细胞表面蛋白酶抑制剂不阻断 | 最高 **100×** 信号（EndoTag2），定位于内体 |
| B9 体内 | BALB/c 皮下 5×10⁶ A20，瘤 ~100 mm³ 起治 | 瘤内 5 mg kg⁻¹，每 3 天 1 次共 3 次，每组 n=6；对照 ATZ 与 isotype | 判据：瘤体积/质量/生存/体重；humane endpoint 为 20% 体重下降 | EndoTag3/EndoTag4 显著减瘤；EndoTag4 组 55 天半数存活 vs ATZ 组全部死亡；瘤组织 PD-L1 降解；体重无差异 |

### 削减量与命中分母（四段账，能算出来的只有两段）

1. **sortilin 分支**：21,000×2 → 每点 several million docks → 100,000 docks 出序列 → 3,000 grafting → **42,000 送实验** → 命中数未报 → 1 条命名设计（21 nM）。**该分支算不出命中率**（送实验数与中间富集数都缺，且 3,000→42,000 不单调）。
2. **ASGPR 分支**：计算过滤（pAE_int<10、relaxed_ddG<−40、sap、净电荷 −7）→ **2,689 送展示** → **4 富集**（4/2,689 ≈ 0.15%）→ ASmb1 2.7 µM → 单体功能为 0 → 2C/3C 才有效。
3. **IGF2R 刚性分支**：每 ProteinMPNN 输入 2,000 条 → 多重阈值 → **170 条 AF2 结构自洽** → **8 条双域结合并表达**（8/170 ≈ 4.7%）→ 功能段（能内吞几条）**分母未报**，正文只报 EndoTag3/EndoTag4。
4. **功能段一律没有分母**：90×/50×/2.5×/4.5×、40%/55%/78%/>80%/85%/77%/45% 全是「相对单一对照的单点读数」，没有一条写成「N 个设计里 M 个达标」。

## 4. 关键数字台账（全部可在本地全文里搜到；出处给原句片段）

| 数值 | 含义 | 出处（原句片段 / 位置） |
|---|---|---|
| 21,000 × 2 位点 | sortilin 每个位点生成的 binder 数 | "21,000 binders were generated to each of 2 sites on the sortilin" |
| several million docks / 位点 | 对接总量（未给确切数） | "we used a set of scaffold libraries to generate several million docks to each of the sites" |
| 100,000 | 被取来做序列设计的 docks | "As in the protocol, 100,000 docks were sub-selected and sequence was designed" |
| 3,000 | 模体提取后被 grafting 再设计的数量 | "Helical motifs were extracted, and 3,000 designs were selected, grafted and subjected to further design" |
| 42,000 | sortilin 分支送实验的设计总数 | "This resulted in 42,000 designs that were tested experimentally" |
| 21 nM | Sort_EndoTag 对 sortilin 的 Kd（该分支最终命名 1 条） | "the highest affinity design (Sort_EndoTag) had a dissociation constant ( K d ) for Sortilin of 21 nM" |
| 90× / 50× | Sort_EndoTag / TfR_EndoTag 相对荧光对照的细胞关联增幅 | "there was a 90-fold increase in fluorescence compared with fluorophore-conjugated control"；"with a 50-fold increase in cellular uptake over the LHDB scaffold control" |
| 4 个变体 | 界面附近植入 N-糖链后阻断结合（表位验证） | "Four sortilin variants that introduce N-linked glycans close to the designed Sort_EndoTag interface blocked binding" |
| 41 nM / 190 nM / 6.5 nM | D6mb、D11mb、优化后 D11mb2 的 Kd | "The tightest binder to domain 6 (D6mb) had an affinity of 41 nM"；"which was improved to 6.5 nM following optimization (D11mb2)" |
| pLDDT < 85 | 柔性融合唯一写明的丢弃阈值 | "The designs with poor monomer plddt (plddt < 85) were dropped" |
| LDDT > 0.5；2,000 条/输入；pLDDT > 90；ddG < −40；SAP < 35 | 刚性融合的五道计算闸 | "The best inpainting outputs were selected by RosettaFold LDDT metrics (>0.5) for the inpainted region and used for sequence design with ProteinMPNN"；"After 2,000 sequences were generated for each ProteinMPNN input, designs were filtered by predicted Rosetta ddG"；"AlphaFold2 structure predictions of the designed sequences were filtered by the pLDDT metric (keeping those with pLDDT > 90)"；"Designs with ddG metrics less than -40 and spatial aggregation propensity scores less than 35 were selected for expression and experimental assays" |
| 5 Å / 10 radians / 3 Å | 刚性融合里模体扰动幅度与界面残基冻结半径 | "the domain 11 helix motif was randomly perturbed by rigid-body translations (up to 5 Å) and rotations (up to 10 radians) for each design prior to inpainting a scaffold between the motifs" |
| **170 → 8** | AF2 判为双域结构自洽的设计 → 实际在大肠杆菌里表达且双域结合（≈4.7%） | "We tested 170 designs for which AlphaFold2 25 predictions matched the intended structures for binding to both IGF2R domains, and expressed eight designs that interacted with both domains in E. coli" |
| 6 nM / 190 nM；15 nM / 4.3 µM | IGF_EndoTag3 与 EndoTag4 各自对 D6/D11 的亲和力 | "Different designs had distinct affinities for domain 6 and domain 11"；"IGF_EndoTag3 was internalized similarly to IGF2 and twofold more efficiently than IGF_EndoTag4" |
| **2,689 → 4** | AF2 预测能结合 ASGPR 的设计数 → 展示筛选高富集数（≈0.15%） | "We used yeast display for 2,689 designs that were predicted to bind ASGPR by AlphaFold2 25 followed by fluorescence-activated cell sorting (FACS) and next-generation sequencing to reveal four highly enriched designs" |
| 2.7 µM | ASGPR 分支最强结合体 ASmb1 的 Kd（比 sortilin 分支弱 ~130×） | "the design with the highest affinity, ASmb1, bound to ASGPR with an affinity of 2.7 µM" |
| pae_interaction<10 且 relaxed_ddg<−40 | ASGPR 分支的 AF2/Rosetta 双闸口 | "Designs with pae_interaction<10 and relaxed_ddg < -40 were selected for resampling with another round of protein-MPNN prediction followed by Rosetta Fastrelax" |
| 净电荷 −7；CST-score <5 | 可溶性与表位验证用的两个次要阈值 | "Candidates passing previous filters were then filtered again with exposed hydrophobicity (sap_score) and optimized with a net-charge of -7"；"Computational models were minimized and filtered based on geometrical restraints, CST-score <5" |
| 2.5× / 4.5× | AS_EndoTag-2C / -3C 相对单体 ASmb1 的细胞荧光增幅 | "2.5-fold and 4.5-fold more fluorescence was associated with cells for AS_EndoTag-2C and AS_EndoTag-3C, respectively, compared with monomeric ASmb1" |
| 1:3 比 → 三聚体 | SEC 证明 AS_EndoTag-3C 把 ASGPR 凑成三聚复合物 | "To determine the oligomerization state induced by AS_EndoTag, we mixed ASGPR and AS_EndoTag-3C at a 1:3 ratio and separated the generated species by size-exclusion chromatography (SEC)" |
| 40% / 55% / 78% / >80% | 200 nM、48 h 后 EGFR 被四类 pLYTAC 降低的幅度（AS / TfR / sortilin / IGF2R-EndoTag2） | "resulted in a 40% decrease in total EGFR levels, whereas fusions to the monomeric ASGPR binder had little effect"；"with EGFRn-TfR_EndoTag resulting in a 55% reduction of EGFR"；"EGFRn-Sort_EndoTag resulting in a 78% reduction of EGFR"；"was the most effective opf these fusions, leading to more than 80% clearance of EGFR" |
| 85%（10 nM） | CTX–IGF_EndoTag1 在 10 nM 时对 EGFR 的降低 | "incubation with 10 nM CTX-IGF_EndoTag1 led to an 85% reduction in EGFR" |
| 77%（48 h）/ 45%（3 h） | ATZ-pLYTAC 对 PD-L1、CTLA4mb 融合对 CTLA4 的清除 | "77% of the PD-L1 in the cells was eliminated after 48 h"；"resulted in a 45% decrease of CTLA4 in Jurkat cells expressing CTLA4 (Jurkat-CTLA4) cells after 3 h" |
| 40× / 50% | LHDA–IGF_EndoTag3 对 LHDB-AF647 的摄取增幅与 48 h 溶液清除 | "with IGF_EndoTag3 producing a remarkable 40-fold increase in mean fluorescence intensity compared with LHDB-AF647 alone"；"resulted in 50% clearance of 100 nM LHDB from the solution after 48 h incubation in Jurkat cells" |
| 80× / 360× / 70% | protein G–IGF_EndoTag3 对 IgG 的摄取增幅（K562/Jurkat）与 48 h 耗竭 | "leading to an overall 80-fold increase in IgG in K562 cells and a 360-fold increase in Jurkat cells"；"resulted in depletion of 70% of the IgG" |
| 2× | protein G–EndoTag3 相对 protein G–M6Pn 的 IgG 摄取优势 | "Protein G-IGF_EndoTag3 elicited twofold higher cellular uptake of IgG than protein G-M6Pn" |
| 80%（HER2⁺）vs 不变（HER2⁻） | Co-LOCKR AND 门条件下的 EGFR 降解 | "In K562 cells overexpressing both EGFR and HER2, addition of BCL2-IGF_EndoTag2 resulted in 80% degradation of EGFR, whereas in K562 cells expressing EGFR without HER2, the EGFR level remained unchanged" |
| 最高 100× | LHDA–EndoTag 对 SNIPR 信号的放大（EndoTag2） | "We found that fusion of IGF_EndoTags to LHDA resulted in an increase of up to 100-fold (in the case of IGF_EndoTag2) in signal activation" |
| 5×10⁶ 细胞 / 100 mm³ / 5 mg kg⁻¹ / q3d×3 / n=6 / 1,000 mm³ 终点 | 小鼠实验的给药与分组口径 | "with the mice been randomly assigned to receive ATZ, ATZ-IGF_EndoTag1 or ATZ-IGF_EndoTag4 and isotype as controls ( n = 6 mice per group)." |
| 55 天半数存活 vs ATZ 组全死 | 体内生存获益（每组 n=6） | "after 55 days, half of the mice treated with the EndoTag fusion remained alive, whereas all mice treated with ATZ alone had died" |
| n=1（体外 WB 与 BLI）；n=3（小鼠 WB） | 作者自述的样本量口径 | "Western blot experiments in vitro and BLI binding assays were conducted with sample size of one based on low variance from previous experience"；"Western blot experiments in mice were performed with sample size of 3 to reduce the variance of protein level across animals from our previous best practice" |
| 未做统计学样本量估算 | 统计口径声明 | "No statistical analysis was used to determine the sample size" |

## 5. 结论——作者说了什么

1. 主张的总纲（摘要级原句）："Computationally designed genetically encoded proteins can be used to target surface proteins, thereby triggering endocytosis and subsequent intracellular degradation, activating signalling or increasing cellular uptake in specific tissues"。
2. EndoTag 相对天然配体的三点优势：可打到天然配体不占的位点、不需要多价化学修饰、全蛋白便于生产与基因编码；作者的说法是 "The designed EndoTag approach considerably expands the possibilites for targeted degradation as a therapeutic modality" 以及 "The all-protein nature of our pLYTACs simplifies manufacturing and enables deployment of targeted degradation approaches in adoptive cell therapies using secretion from engineered cells"。
3. 按机制分型设计是有效的：常驻循环型（sortilin、TfR）只要正交结合就内吞；构象变化型（IGF2R）要把 D6 与 D11 拉近；成簇型（ASGPR）要多价。组织分布不同 → 降解可做组织限定："Thus, the ASGPR EndoTags function as liver-specific targeted degraders"。
4. 降解是受体依赖的，且能一路传到信号层与体内：敲除对应受体后降解消失；EGFR 被降后 EGF 诱导的 pERK 消失（"pre-incubation of EGFRn-IGF_EndoTag largely ablated EGF signalling"）；ATZ 融合在模型里减瘤并延长生存（"after 55 days, half of the mice treated with the EndoTag fusion remained alive, whereas all mice treated with ATZ alone had died"）；作者总结 "such fusions not only block disease-asociated interactions of the target (like the unfused antibody) but also induce cellular uptake and degradation of the target in the lysosome"。
5. 逻辑门与分泌两条能力被作者视为新东西："Such logic-gated targeted degradation has not been achieved with current extracellular protein-degradation systems"，以及 "Thus, EndoTags remain functional when secreted from cells, providing a means for adoptive cell therapies to degrade proteins in the surrounding environment for greater efficacy, and to degrade self proteins for feedback control"。
6. 信号放大：融合 EndoTag 让原本主要在内体激活的 ortho-SNIPR 提高至 100×（"We achieved a 100-fold enhancement of maximum signalling effect by fusing the SNIPR ligand to EndoTags"），并判定其发生在内体（氯喹与 γ-secretase 抑制剂阻断、细胞表面蛋白酶抑制剂不阻断）。
7. 作者自限（明写在 Conclusion/Discussion）：内吞触发受体的适用范围只是推测；免疫原性必须评估（"it will be important to assess and, if necessary, reduce the immunogenicity of EndoTags"）；回收式催化变体（可省剂量）尚未做；对天然信号通路是否也有效未回答（"Further studies will be required to determine whether EndoTags can enhance signalling through endogenous pathways"）；可溶配体的清除可能被受体数量卡住（"clearance may be limited by the number of available receptors"）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇真正的贡献不是「设计出一个内吞蛋白」，而是把「功能」拆成一道独立的、计算端无法代理的闸**。设计判据（ddG、SAP、pAE_interaction、pLDDT）买到的是结合与折叠；决定内吞的是连接肽长度、域间距、价态——正文用「变长就降、变短就消失、同二聚就不摄取」这组阴性结果证明了这一点。对我们：任何「结构自洽 → 会有活性」的推理链，在这里被直接切断，酶设计项目里对应的断点是「活性位点几何自洽 → 会催化三步化学事件」，同样不能代理。
2. **命中分母在三条分支上是断的，而且断在关键位置**：sortilin 分支连「多少条通过展示」都没报；ASGPR 报 2,689→4 但功能靠后续价态；IGF2R 报 170→8 但「8 条里几条真能内吞」不报。也就是说，全文没有一处把「设计→结合→内吞→降解」四级漏斗的转化率连起来算过。→ 推断：作者手里也没有可算的四级队列，功能段是**逐个构建体定点验证**而不是群体筛选。这正是我们该走的路（一轮几个构建体、信息量最大化），而不是去羡慕他们的通量。
3. **最强结合体不等于最强功能体，且方向不一致**：ASGPR 分支最强结合只有 2.7 µM（比 sortilin 的 21 nM 弱约 130 倍），却因为价态设计成了有效的降解器；IGF2R 分支 D11 端 4.3 µM 的 EndoTag4 仍能内吞且**更正交**。→ 推断：在这个体系里亲和力甚至与功能**负相关**（越黏越可能卡在受体上或与天然配体抢位），所以「把 Kd 当优化目标」的默认漏斗在此会优化错方向。
4. **降解读数的口径很软**：200 nM、48 h、n=1（作者自述体外 WB 与 BLI 都做 n=1），只给单一百分比、无剂量—响应、无散布。40%/55%/78%/>80% 的差异**不能**读成「受体路线优劣」，只读成「在这些条件下能降到这个程度」。→ 推断：作者用 KO + 失活变体 + 共定位缺失这三条**定性对照**替代了统计重复；这是可信的机制证据，但不是可比较的量级证据。
5. **本文与 B09 是同一套计算闸口、不同模态边界**：ASGPR 分支明确用 pAE_interaction<10 作闸口（B09 建立的那一套），一旦目标从结合升级到内吞，这套闸口的通过率就变成 4/2,689 与 8/170 的量级，而且**功能命中根本不在它的管辖范围**。→ 推断：判据强度与任务复杂度成反比；把 binder 漏斗的阈值直接搬到「事件型功能」上，风险不是命中率低，而是**优化了错误的自由度**。
6. Methods 与正文在体内分组上不一致（EndoTag1 vs EndoTag3），且 PD-L1 结果同时报 4 h 起效与 48 h 77% 却以 n=1 口径做体外 WB。→ 推断：这是本文最该被追问的两处账面细节；但不影响主线结论（受体依赖降解确实成立，因为有 KO 对照）。

## 7. 局限与失败（作者的 + 我们读出的）

**作者承认的**
- 内吞诱导的普适性未知："there are likely to be many more receptor targets that can undergo rapid endocytosis upon suitable triggering at the cell surface" 只是展望，本文只做了 4 个受体。
- 免疫原性未评估（本文无免疫原性数据）；剂量学靠未来「催化回收式」变体解决。
- 内吞的机制解释是定性的：构象变化型受体的「哪种构象才被内吞」靠把 D6/D11 拉近这一假设成立，作者没有给出可直接计算的构象判据。
- 天然信号通路的放大未验证；降解容量受受体数量限制（自述）。

**我们读出的（不计入作者结论）**
- **漏斗没有闭环记账**：sortilin 分支 42,000 送实验却无中间命中数、且 3,000→42,000 与前述步骤不单调，说明「送实验数」这个分母在论文里来自不同层；无法据此评估任何判据的通过率。
- **功能段完全没有阈值定义**：全文没有一条「降幅 ≥X% 才算这个设计成功」的标准；百分比全部是结果而非判据。
- **计算端与功能端零耦合**：没有任何一条计算指标被回过头来检验「能否预测内吞/降解」（B09 至少做过判据-结局的 ROC 式对比，本文没有）。这是本文相对 B09 最大的方法学退步。
- **单点、单浓度为主**：降解实验多在 200 nM/48 h；10 nM 才出现在 CTX 对照组；跨实验的 fold-change 归一基准不同（AF647-LHDB 或 SA-AF647 单独），彼此不可直接比较。
- **体内 n=6 单中心、皮下 A20 同系模型、瘤内给药**（不是系统给药），说明全身暴露与毒理未在这篇里回答。
- **无 MD/QM/自由能**：全文没有任何动力学或电子结构层面的机理证据，内吞的构象机制是结构模型 + 定性实验支撑。
- **正文/方法自相矛盾之处**：体内分组到底是 ATZ–IGF_EndoTag1 还是 ATZ–IGF_EndoTag3，正文与 Methods 不一致（两句都在全文里，见第 9 节）。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **「结合级判据」与「事件级判据」必须分家，事件级要单列一道闸**（对应本文把 binding 与 endocytosis 拆成两段、中间不做代理）。我们的用法：第一步（游离底物起始）/ 第二步（中间体形成）/ 第三步（第二底物 vs 副反应竞争）三个化学事件各自要有**独立判据与独立阴性对照**；结构自洽、pLDDT、界面能量只能作为准入，不得写成支持「会催化」的证据。本文用「短 linker 直接 abolish」证明了几何自由度是功能开关——我们对应用底物通道/邻近性/柔性 loop 这一类**不被打分函数表达**的自由度，必须显式列出而不是指望序列评分覆盖。
2. **把「最强结合体≠最强功能体」写进候选排序规则**：本文里 2.7 µM 的 ASmb1 靠价态变成有效降解器、190 nM 端亲和力反而更正交。我们的用法：候选排序不许只按单一打分降序，要按**机制多样性**排（不同事件假说、不同几何假设各留一条），并在预算里给「非最优分数但结构自由度不同」的条目留名额。
3. **削减量与分母逐段记账**（本文的教训来自它**没记全**）：每一段都写「进段数 / 出段数 / 判据 / 未报数」，缺就明写缺——与我们第 13 轮的分层附录做法一致（一段一 sheet、含失败与 METHOD_FAIL）。本文 42,000/2,689/170/8 说明：**只要有一段没记出段数，整条漏斗的判据强度就无法事后评估**。
4. **用定性遗传/化学对照替代统计重复来支撑机制主张**：本文在 n=1 WB 之下仍靠「受体 KO 后活性消失 + 界面突变体失活 + 共定位只在阳性细胞出现」把机制钉住。我们的对应做法：每个阳性读数必须配一条**失活/去背景对照**（死酶、缺底物、位点突变），并在报告里把「机制是否成立」与「幅度多大」分开写。
5. **「正交于内源竞争」作为设计约束前置**：本文把位点选在天然配体之外，用 GNPTAB 敲除证明不丢功能。对应到酶设计：目标反应要显式声明**与哪条内源通路竞争**（内源核苷酸池、内源聚合酶），并把「不与内源底物争」列为可检验判据而不是附带好处。

**不可迁移（为什么不能照搬）**

1. **pAE_interaction<10、relaxed_ddG<−40、SAP<35、pLDDT>90/85、净电荷 −7 全是「结合界面 + 单体可折」阈值，与催化无关**。本库判定标准明令禁止把 binder 的 pAE/ipTM 阈值当酶活闸口；本文自己更是**没有用任何计算判据去预测内吞**，所以它连「阈值能代理功能」都不支持，更不能代理三步化学事件。
2. **40%/55%/78%/>80%/85% 的降解率、80×/360× 的清除增幅、55 天半数存活，一律不得当作酶设计的成功概率或转化率预期**。分母是 n=1 或 n=3、单浓度单时间点、归一基准各不相同；而且这些数字描述的是「把膜蛋白吞掉」，与「合成一个非天然氨基酸并留下可检产物」不是同一类事件。
3. **2,689 / 170 / 42,000 这种通量来自展示库 + FACS + 深测序**，产物化学端不存在等价通道（我们一轮最多几个构建体、每个要 LC-MS/MS 定产物身份）。照搬通量叙事会得出「我们注定失败」的错误结论——本文的功能段同样是**逐构建体定点验证**，与我们的做法同构。
4. **酵母展示双阳性门（PE+FITC）是群体级表观读数，没有个体化学确认**；我们的第一道湿实验本身就是产物身份鉴定，二者不同层，不能类比成「他们的 YSD ≈ 我们的 LC-MS」。本文里 YSD 之后还要 BLI、E. coli 表达、细胞摄取三级复验，恰好说明群体级读数不足。
5. **本文无 MD、无 QM、无自由能**，因此它既不能为「用长时 MD 判催化」提供命中率背书，也不能为「结构自洽即功能」提供反例以外的机制证据。它在方法演进链上的价值是**边界证据**：告诉我们计算漏斗在何处停止对功能负责。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/endocytosis2025.txt

- **唯一引句底稿**：`data/interim/baker_lit/ft/endocytosis2025.txt`（103,860 B，2026-10-16 抓取；文件头身份块 PMC11839401 / PMID 39322662 / DOI 10.1038/s41586-024-07948-2 已复核，与 CSV 行标题一致）。本文在 `sources_map.json` 里另登记 `sources/baker.md`、`sources/cao.md` 两处二手对照底稿，**不作为引句源**：这两处把阈值句转写成 `relaxed_ddG < −40`、`pae_interaction < 10`（加空格、大写 G）等排版形式，与全文抽取文本的 `relaxed_ddg < -40`、`pae_interaction<10` 并非逐字一致，故本卡引句一律按 txt 原样（含句中残留的参考文献编号，如 AlphaFold2 后的 `25`）复制。
- 二手底稿行号：`sources/baker.md:552–563`（B42 行，命中率 8/170 与 4/2,689 的出处）、`sources/cao.md:185–201`（C11 行，阈值体系汇总）。本卡相对这两处补充：sortilin 分支的 21,000/100,000/3,000/42,000 非单调削减链、pLDDT<85 与 LDDT>0.5 两道柔性/刚性融合闸、SEC 三聚体验证、n=1 统计口径、正文与 Methods 的体内分组不一致。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/Kd或活性最好值/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`scripts/verify_literature_cards.py --only "B42; C11" --no-report`（该脚本把卡内所有不含中日韩字符、被直双引号包住、≥20 字符且 ≥12 个字母的片段，在声明底稿的归一化文本（NFC + HTML 实体解码 + 引号/破折号统一 + 空白折叠）里逐字查找；任何一条不命中即 FAIL）。本轮实测结果 **PASS，quotes=110/110**（其中 76 条互不重复的引句，其余为同一句在第 2/3/4 节的复用）；首轮曾因一处句末空格写法（`per group )` 对 `per group).`）报 2 处 MISS，改正后复跑转绿。
- **本文献级别的把握度**：设计—结合这一段为**全文级、可复算**（所有阈值与分母都可在 txt 里搜到）；「计算判据不能代理功能」这一条为**中—高把握**（依据是作者自述的三条阴性结果与分母缺失，属论文自身证据）；「亲和力与功能负相关」为**我们的低—中把握推断**（n=1、单浓度、样本仅 2–3 条设计，不足以成为规律，只足以禁止把 Kd 当唯一目标）。**能改变结论的证据**：若补充信息（Supplementary Figs 1–23 / Tables 1–5，本卡未取到）里给出各段通过数与判据-功能回归，则第 6.2/6.3 条需要重估。

引句底稿: data/interim/baker_lit/ft/endocytosis2025.txt

<!--CSV回填
work_type=论文
target=内吞受体 IGF2R（domain 6 / domain 11）、ASGPR、sortilin、TfR；下游被降解对象 EGFR、PD-L1、CTLA4、IgG、LHDB
backbone_generation=Rosetta de novo binder 设计（PatchDock→RifDock→FastDesign/FastRelax）+ MotifGraft 螺旋模体嫁接；ProteinMPNN 出序列；RFInpainting/protein inpainting 把 D6mb 两条界面螺旋与 D11mb 一条界面螺旋刚性焊合；柔性变体穷举 GS 连接肽长度与域顺序；抗体端为 Expi293F transient 共转染的 ATZ/CTX–EndoTag 融合
computational_filters=Rosetta ddG 与 contact_molecular_surface；暴露疏水性 sap_score / SAP；AlphaFold2 单体 pLDDT 与复合物 pAE_interaction；AF2 与设计模型的亚埃骨架 RMSD；RosettaFold LDDT（inpaint 区）；Rosetta FastRelax 后 relaxed_ddG；净电荷优化到 −7；表位侧 RosettaMatch + CST-score
thresholds=pae_interaction<10 且 relaxed_ddg<−40（ASGPR 生成端）；ddG<−40 且 SAP<35（刚性 IGF_EndoTag 终闸）；AF2 pLDDT>90（刚性）与丢弃 monomer plddt<85（柔性）；RosettaFold LDDT>0.5；净电荷 −7；CST-score<5；界面 3 Å 内残基固定；模体扰动平移≤5 Å、旋转≤10 radians；内吞/降解功能段原文未给成功阈值
md_used=否
qm_used=否
experimental_methods=酵母表面展示 + FACS 双阳性门 + MiSeq 深测序；BLI（Octet RED96）测 Kd；E. coli 表达 + IMAC/SEC 纯化；流式测细胞关联荧光（内吞）与表面受体量；Western blot 测总受体；LysoTracker/LAMP2A 共定位成像；上清荧光测可溶蛋白清除；SEC 定 ASGPR 寡聚态；受体/GNPTAB 敲除与界面突变体失活对照；磷酸化流式 pERK；N-糖基化扫描验表位；Co-LOCKR AND 门；ortho-SNIPR-BFP 剂量—响应与抑制剂剖分；BALB/c 皮下 A20 瘤内给药 + 生存曲线
pipeline_counts=sortilin：21,000×2 位点 → 每点 several million docks → 100,000 docks 出序列 → 3,000 grafting → 42,000 送实验（中间命中数未报）→ 1 条命名设计；IGF2R 刚性：2,000 序列/ProteinMPNN 输入 → 170 条 AF2 结构自洽 → 8 条双域结合并表达 → 功能段分母未报；ASGPR：2,689 送展示 → 4 高富集 → ASmb1 → 2C/3C 才有功能；内吞/降解/体内各段为逐构建体定点验证，无群体分母
hit_rate=4/2,689≈0.15%（AF2 预测结合 → 展示富集）；8/170≈4.7%（AF2 自洽 → 表达且双域结合）；内吞与降解读数无命中率口径；单点功能读数：EGFR 降 40%（AS）/55%（TfR）/78%（sortilin）/>80%（IGF_EndoTag2）、CTX–EndoTag1 在 10 nM 降 85%、PD-L1 48 h 消除 77%、CTLA4 3 h 降 45%、IgG 48 h 耗竭 70%、SNIPR 信号最高 100×
best_metric=亲和力最好：IGF_EndoTag3 对 D6 6 nM 与 D11mb2 6.5 nM；sortilin 分支 Sort_EndoTag 21 nM；ASGPR 分支仅 2.7 µM；功能端最好单点：EGFR >80% 清除（200 nM、48 h）与 CTX–EndoTag1 85%@10 nM；体内 ATZ–IGF_EndoTag4 组 55 天半数存活（每组 n=6）
cost_or_stat_note=全文未记录计算成本（无 GPU/CPU 秒）；作者自述体外 Western blot 与 BLI 样本量为 1、小鼠 Western blot 为 3、每组 6 只，且明写未用统计学确定样本量；降解率多为单一浓度单一时间点，fold-change 归一基准各不相同（AF647-LHDB 或 SA-AF647 单独），跨实验不可直接比较
role_in_timeline=B09 那套 AF2 闸口（pAE_interaction<10）在本篇被搬到生成端用于 ASGPR 分支，但目标从「结合」升级为「触发内吞/降解」后，计算判据与细胞功能之间没有任何桥：功能靠连接肽长度、域间距与价态在实验端重扫，且出现「短 linker 完全 abolish」「同源二聚体不摄取」「单体 binder 结合却不降解」三类作者自述失败模式，命中率量级跌到 0.15% 与 4.7% 而功能段无分母。它是「阈值体系已成型、功能段记账缺失」的边界样本，也是 binder 漏斗阈值不得外推到事件型功能（酶活/产物生成）的直接反证
source_pointer=data/interim/baker_lit/ft/endocytosis2025.txt（文件头身份块 PMC11839401 / PMID 39322662 / DOI 10.1038/s41586-024-07948-2）；对照底稿 sources/baker.md:552–563、sources/cao.md:185–201
CSV回填-->
