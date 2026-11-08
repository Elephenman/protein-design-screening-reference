# [B32; C14] 给凸面免疫受体做凹面支架：5HCS 五螺旋凹面库 + 三段式漏斗拿下 TGFβRII / CTLA-4 / PD-L1 的亚纳摩尔结合蛋白

Yang W, Hicks DR, Ghosh A, Schwartze TA, Coventry B, Goreshnik I, … Cao L, … Baker D（华盛顿大学 IPD + Einstein + Pitt）
Nature Communications 2025, 16:2001 · DOI 10.1038/s41467-025-57192-z · PMID 40011465 · PMCID PMC11865580
开放获取（CC BY 4.0）· 预印本 10.1101/2024.05.01.592114

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B32; C14**（Baker组; 曹龙兴组 共用同一行同一篇） |
| 状态 | FULLTEXT（batches.tsv 第 32 行，id=`B32; C14`） |
| 本文取回方式 | 先行调研缓存 `data/interim/baker_lit/ft/immune_receptor_binder2025.txt`（66,255 B，2026-10-16 抓取，PMC 抽取版纯文本） |
| 引句底稿（本卡声明） | `data/interim/baker_lit/ft/immune_receptor_binder2025.txt` —— 本卡全部引句只对着这一份逐字核验（同一论文如另有 Europe PMC 抽取版，句内参考文献编号位置不同，不混用） |
| 对照底稿 | `sources/baker.md:419–429`（B32 原卡）、`sources/cao.md:230–247`（C14 原卡）、`sources/cao.md:417`（漏斗数字对照表行） |
| 证据级别 | **全文级**（本卡所有英文引句均可在声明底稿里逐字命中；见第 9 节自检） |
| 未取到的部分 | 补充信息与图（Supplementary Figs 2/3/4/5/6/7/8/9/10/11/12/13/14）、Supplementary Table 1/2（晶体学统计与序列）、Source Data、Reporting Summary 正文未含。凡涉及这些的本卡明写"正文未给出"；TGFβRII 初筛命中条数正文即未给出 |

## 1. 这篇到底解决什么（大白话）

免疫检查点/细胞因子受体（CTLA-4、PD-L1、TGFβRII 等）的结合位点大多在免疫球蛋白折叠结构域的**凸面**上。上一代 de novo binder 管线用的是小的球状迷你蛋白支架，表面要么平要么凸，贴不住凸面——形状互补做不出来，亲和力就卡在微摩尔段上不去。这篇做了两件事：**①先造一套"凹面"工具**：5HCS——五螺旋束、三根螺旋（H1/H3/H5）形成可调曲率的凹面结合面、两根在背面支撑、全长压到 120 aa 以内、以稳定性换耐突变，最终留下 7476 个骨架；**②再用同一套漏斗（对接→界面序列设计→ddG/CMS/pAE 三闸→酵母展示下单）对三个凸面靶做设计**，用 67 条 5HCS 设计对 4310 条迷你蛋白设计做同靶头对头对照，最富集的 binder 全部来自 5HCS。之后走"SSM 热图/ProteinMPNN 重采样→简并密码子组合库→酵母展示亲和成熟"把三个靶都推到亚纳摩尔甚至 <100 pM，共晶结构与设计模型 RMSD 0.34–0.55 Å，细胞功能（受体封闭/信号抑制）全部做活，还补了一个六聚体版本把 CTLA-4 功能的 EC50 拉到和药近水平。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **凸面表位与球状支架形状不匹配，是选题动机也是被明说的行业痛点**（摘要原句）："traditional Rosetta based protein binder methods using small globular scaffolds have difficulty achieving high affinity on convex targets"。→ **应对**：不继续在球状支架上调序列，而是**为靶的几何类别定制支架家族**——按三条性质（曲率多样、高稳定、80–120 aa 小型化）设计凹面五螺旋束，"We focused on five-helix bundle scaffolds, with three helices forming the concave interface and two providing structural support"；并在同一靶（TGFβRII）上做**头对头对照**："We tested in parallel 67 5HCS based designs and 4310 designs based on the globular scaffolds used by Cao et al. for comparison to our previous approach"，结果"the most enriched binders were all from the 5HCS design set (with no additional substitutions) despite the nearly 100-fold greater diversity of the minibinder library"。→ **留下的代价**：正文未给出 TGFβRII 初筛命中条数（只说最富集者全来自 5HCS），对照结论建立在"富集排名"而非统一命中率口径上；凹面支架对非凸面表位无优势，本文没有讨论适用边界。
2. **CTLA-4 上 AF2 与设计复合模型不自洽**（作者原句，两句连排，句内有引文编号故只引中间连续段）："predicted models were not consistent with the designed complex model, we combined the most enriched substitutions from the SSM heatmap"，"instead of using the ProteinMPNN 25 resampling followed by Alphafold2 20 filtering method"——即 TGFβRII 分支用的虚拟优化路线（MPNN 重采样+AF2 过滤）在 CTLA-4 上做不下去了。→ **应对**：**把第二道计算闸口换成实验闸口**：直接对 SSM 位点饱和突变热图取最富集突变，编成简并密码子组合库再走酵母展示（"We again encoded these substitutions using degenerate codons"）。→ **代价**：SSM 库是全库每位置换 19 种氨基酸、要 FACS+NGS 的贵手段；"为什么 AF2 在这个靶上不一致"本文未解决，也没给判据说明何时该弃 AF2。
3. **亲和力与细胞功能脱节**：5HCS_CTLA4_1 结合 <100 pM，但封闭功能 EC50 53.3 nM，比抗体药 Ipilimumab 的 15.0 nM 差 3.5 倍——而抗体本身结合还弱它两个数量级以上（原句连续段）："despite the at least two order weaker binding affinity for CTLA-4"。→ **应对**：作者猜空间/价态效应（"Steric or avidity effects may contribute"），于是**做 avidity 工程**：把 binder 融合到已知对称寡聚模块上，得到高表达单分散六聚体 5HCS_CTLA4_1_c6，EC50 16.1 nM，"comparable to the antibody"。→ **代价**：机理仍是假设未量化，六聚体版本没给绝对 KD；"Kd→细胞效价"的这条断裂只是被绕过、没有被解释。
4. **重组 PD-L1 蛋白在 BLI 上行为异常**（原句）："association traces were more regular using SPR than BLI, perhaps due to poor behavior of the recombinant native PD-L1 protein"。→ **应对**：换第二种结合度量测手段（SPR）交叉确认，最终报 646 pM（"is expressed at high levels, very stable and has an affinity of 646 pM"）。→ **代价**：蛋白为何行为异常没有诊断，"poor behavior"是猜测式归因；换仪器并不能排除靶蛋白本身构象不均一。
5. **最强 CTLA-4 binder 亲和力超出测量上限**（原句连续段）："had an off rate too slow and a binding affinity for CTLA-4 too tight"，正文记为 <100 pM——BLI 解不出真实 KD。→ **应对**：接受"测不准"，改用解离上限加功能 EC50 双线呈现。→ **本文未解决**：5HCS_CTLA4_1 的真 KD 数值至今（本文内）未知，也没有换用更慢洗脱的测定（如 ITC/预解离实验）的记载。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **支架生成**：理想螺旋+loop 片段 → helix-turn-helix-turn 模块 → 三段重复 → N/C 端截断（Rosetta 生态：LayerDesign 出序列、HybrizeMover 做骨架多样化）。选五螺旋束是为了在 DHR 式可调曲率（但 ">150 residues"）与小型化之间折中。
- **几何量化工具（本文特色）**：RANSAC 球面拟合 + "凸度=半径倒数 + 内积符号定凹凸"，用来（a）把曲率凸的骨架滤掉、（b）给靶表位分型（Table 1 的 binder/target convexity 列）。
- **界面设计**：PatchDock 对接 + 结合取向过滤；TGFβRII/PD-L1 走 ProteinMPNN 界面序列设计（靶链固定天然序列），CTLA-4 走 RosettaScript。
- **计算闸口**：AF2 initial guess 的 ddG、contact molecular surface、pAE；支架端用 AF2 pLDDT + DeepAccNet。
- **实验漏斗**：oligo 池编码 → 酵母表面展示（with-avidity / without-avidity 两种标记）+ 多轮 FACS + NGS；SSM 全饱和突变库做"结合指纹"；简并密码子组合库做亲和成熟；E. coli 表达 → BLI/SPR → CD 热稳定性 → X 射线（共）晶 → 三种细胞报告基因功能实验 + A431 敲除 specificity 验证。
- **没有用的方法**：MD、QM、自由能微扰全程为零；讨论里"reducing solvation-free energy"只是概念性表述。RFdiffusion 仅在讨论中作为未来方向被提及，未使用。

### A. 5HCS 支架库构建（Methods 5HCS Scaffolds library design）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 既往迷你蛋白用的理想螺旋/loop 片段库 | 组装 helix-turn-helix-turn 模块（30–50 aa），重复 3 次成三段重复蛋白，再试全部 N/C 端截断组合 | 每根螺旋 18–22 aa（5–6 圈）；总长压进 120 aa 内；"All possibilities of N- and C- terminal truncation were assessed and the most concave compact structure under 120 amino acids was chosen" | 五螺旋束骨架母版（Fig 1b） |
| A2 | 骨架母版 | Rosetta HybrizeMover 以骨架自身为模板做多样化；Rosetta LayerDesign 出序列（凹面残基按二级结构 + layerselector 选重原子层） | 原文未给多样化倍率数字 | 待评骨架集合（规模正文未给） |
| A3 | 骨架+界面原子坐标 | RANSAC 球面拟合三根界面螺旋表面，算凸度（半径倒数），内积符号定凹/凸，剔除凸面者 | "fit spherical surfaces from the coordinates of the interfacial atoms"；阈值 1 Å、max iteration 100k（同段原句，阈值数字在正文记作 1 Å，本文本抽取件里该数字后带单位异体空格，故不入引句） | 只留凹面骨架 |
| A4 | 凹面骨架 | AlphaFold2 + DeepAccNet 复测折叠一致性 | "The designed scaffolds were later filtered by the AlphaFold2 with a mean plDDT cutoff of 80 and AccNet with a mean plDDT cutoff of 0.8" | **7476 条**："The selected 7476 scaffolds, referred to as 5HCS (5 helix concave scaffolds), exhibit a wide range of curvatures"（库与代码公开：github.com/proteincraft/5HCS） |

### B. 三靶 binder 漏斗（Docking and interface design，Methods）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | 5HCS 库；靶：TGFβRII 的 TGF-β3 结合位点（PDB 1KTZ）、CTLA-4 的 CD86 结合区 β-turn（1I85）、PD-L1 的 PD-1 结合位点（3BIK） | PatchDock 对接（TGFβRII 用 Cao 2022 的 RIF 协议）；再按结合取向过滤 | "Only designs with interfacial residues as the concave surfaces were kept"（三靶通用） | 取向合格的设计集（规模未给） |
| B2a | TGFβRII | ProteinMPNN 界面序列设计 → AF2 initial guess 复算 | "The designs were later filtered by ddG (less than -40), contact molecular surface (larger than 400), and pAE (less than 10) from AlphaFold2 initial guess" | **67 条**（5HCS）；对照组迷你蛋白库同流程出 **4310 条**（"Finally, 67 and 4310 designs from 5HCS and mini protein libraries passed the filters and were tested experimentally, respectively." 为原文连续句，数字已入台账） |
| B2b | CTLA-4 | RosettaScript 界面设计（非 MPNN） | ddG 小于 −40、CMS 大于 400 两闸；**pAE 闸此靶未提** | **4600 条**下单 |
| B2c | PD-L1 | ProteinMPNN 界面设计 + AF2 initial guess | 同 B2a 三闸 | **96 条**下单 |
| B3 | 上述设计 → oligo 池 → 酵母展示库 | 多轮 FACS：初库先 with-avidity 后 without-avidity 递减浓度 | "All the original libraries of de novo designs were sorted using the with-avidity method for the first few rounds of screening to exclude weak binder candidates" | 命中：TGFβRII 最富集者全来自 5HCS（条数正文未给）；CTLA-4 "identified six CTLA-4 binders which match the designs with 100% sequence identity"；PD-L1 "Two PD-L1 binders were obtained from a set of 96 designs" |
| B4 | 初命中（TGFβRII 的 5HCS_TGFBR2_0、PD-L1 的 5HCS_PDL1_0） | 结合态下 ProteinMPNN 界面重采样 + AF2 过滤复合模型（虚拟优化） | "Interfacial residues were re-sampled massively (5000 replicates)"，温度 0.4；按预测 ΔddG 低于初始命中排序，突变出现频次决定编入简并密码子的优先级 | 突变清单 → 组合库（转化效率约 10^7） |
| B4' | CTLA-4 初命中 5HCS_CTLA4_0 | AF2 不自洽 → 改走 SSM 热图：取最富集突变编简并密码子库 | "predicted models were not consistent with the designed complex model, we combined the most enriched substitutions from the SSM heatmap" | 同上，进展示分选 |
| B5 | 组合库 | 中浓度靶浓度富集两轮取上 10%，第三轮滴度递减浓度收集最低浓度结合群；挑优者 E. coli 表达、BLI 测 | 组合库两轮 top 10%；BLI 三浓度全局拟合（1:1 模型） | TGFβRII：表达 4 个，最优 5HCS_TGFBR2_1 "was found using biolayer interferometry" 记 KD 小于 1 nM；序列同一性 "The sequence identity between 5HCS_TGFBR2_0 and 5HCS_TGFBR2_1 is 88.12%"。CTLA-4：表达 4 个，最优 5HCS_CTLA4_1（与 _0 同一性 82.86%）"had an off rate too slow and a binding affinity for CTLA-4 too tight"，记 <100 pM。PD-L1：表达 10 个，最优 5HCS_PDL1_1（与 _0 相似度 93.2%）"is expressed at high levels, very stable and has an affinity of 646 pM" |

### C. 结构-功能闭环（Results + Structure determination）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| C1 | 三个成熟 binder | SSM 全库（每位置换其余 19 种氨基酸）+ 荧光标记靶 FACS + NGS，按位置算 Shannon 熵 | 分选浓度：TGFβRII 1.6 nM、CTLA-4 10 nM、PD-L1 6 nM（图注）；判据为界面/核心残基强保守 | "Design of such extended grooves and pockets is nearly impossible using small globular miniproteins"（作者据此确认凹面沟槽是命中率来源）；界面螺旋 H1/H3/H5 上的关键氢键逐一在晶体结构中复现 |
| C2 | binder:受体复合物 | X 射线（共）晶 + 分子置换（MR 用计算设计模型） | 结构与设计模型比对 RMSD | TGFβRII 共晶 1.24 Å、全复合物 Cα RMSD 0.55 Å；CTLA-4 复合物晶体 2.72 Å、复合物 RMSD 0.34 Å、游离体与结合态 0.416 Å；PD-L1 仅**游离态**晶体 1.88 Å、对设计模型 105 个 Cα RMSD 0.75 Å |
| C3 | 成熟 binder | CD 热熔（25→95 °C 快速复折回 25 °C）；BLI/SPR | 208/222 nm 螺旋峰 + 95 °C 信号几乎不变 | 三个 binder Tm 均大于 95 °C（Table 1） |
| C4 | 成熟 binder | 细胞功能：HEK293 CAGA12 SMAD2/3 荧光素酶（10 pM TGF-β3 刺激）；Jurkat CTLA-4 / PD-1 报告基因封闭 | 四参数 logistic 拟合 IC50/EC50 | TGFβRII 抑制 IC50 30.6 nM；CTLA-4 活化 EC50 53.3 nM（Ipilimumab 15.0 nM）；六聚体 c6 EC50 16.1 nM；PD-L1 EC50 2.1 nM |
| C5 | PD-L1 binder | CRISPR RNP 敲 A431 的 CD274，WT vs KO 表面染色（浓度不低于 10 倍 EC50），FACS 对照商品抗体 | KO 信号与阴性对照持平 | 高特异性（Fig 4d；p 值 2.874×10⁻⁴ / 4.269×10⁻²，正文/图注） |

**流程骨架小结**：几何分型（凹/凸量化）→ 定制支架库（两道折叠闸）→ 同一套界面三闸（CTLA-4 例外砍掉 pAE）→ 展示漏斗 → 双路亲和成熟（计算虚拟优化 or SSM 反馈，视 AF2 自洽与否切换）→ 结构+功能闭环。

## 4. 关键数字台账（数值 · 含义 · 出处；全部可在声明底稿中搜到）

| 数值 | 含义 | 出处 |
|---|---|---|
| 18–22 aa / <120 aa / 30–50 aa | 单螺旋长度 / 支架总长上限 / 模块长度 | Results 第一段与 Methods Backbone generation |
| pLDDT 80、AccNet 0.8 | 支架端 AF2/DeepAccNet 折叠闸 | 引句见第 3 节 A4（The designed scaffolds…cutoff of 0.8 整句） |
| 7476 | 最终 5HCS 凹面支架数 | "The selected 7476 scaffolds" |
| ddG < −40；CMS > 400；pAE < 10 | 界面设计三闸（CTLA-4 分支只前两闸） | Methods Docking and interface design |
| 67 / 4310 | TGFβRII 送测设计数（5HCS / 迷你蛋白对照） | Results TGFβRII 段与 Methods |
| 4600 → 6 | CTLA-4 送测 → 命中 binder 数（与设计 100% 序列一致） | Methods "Finally, 4600 designs"; Results "six CTLA-4 binders" |
| 96 → 2 | PD-L1 送测 → 命中数 | "Two PD-L1 binders were obtained from a set of 96 designs" |
| 5000 倍重采样、温度 0.4 | ProteinMPNN 虚拟优化规模 | "Interfacial residues were re-sampled massively (5000 replicates)" |
| 10^7 上下 | 组合库酵母转化效率 | Methods Combinatorial library design |
| 88.12% / 82.86% / 93.2% | 三个成熟体对初始命中的序列同一性/相似度 | Results 三段 |
| <1 nM / <100 pM / 646 pM（0.646±0.02 nM） | 三靶最优 KD（Table 1 同值） | Results + Table 1 |
| 1.24 Å / 0.55 Å；2.72 Å / 0.34 Å / 0.416 Å；1.88 Å / 0.75 Å（105 Cα） | TGFβRII 共晶分辨率/复合物 RMSD；CTLA-4 复合物分辨率/复合物 RMSD/游离-结合一致度；PD-L1 游离晶体分辨率/对设计 RMSD | Results + Methods Structure determination |
| Tm >95 °C（三靶）；208/222 nm | 热稳定性与螺旋特征 | Table 1 + CD 段与 Methods |
| IC50 30.6 nM；EC50 53.3 / 15.0 / 16.1 / 2.1 nM | TGFβ 信号抑制；CTLA-4 封闭（binder / Ipilimumab / 六聚体 c6）；PD-L1 封闭 | Results 功能段；Ipilimumab KD 18.2 nM（引文 27） |
| 1.6 / 10 / 6 nM | 三个 SSM 库分选用靶浓度 | Fig 2d / 3a / 4b 图注 |
| ≥10× EC50；5000 细胞/孔，2/4 孔重复 | A431 染色浓度与重复设计 | Fig 4d 图注 |
| 0.5 Å²；40% 序列同一性；1 Å、100k 次 | 界面残基判定 ΔSASA / PDB 复合物聚类 / RANSAC 拟合阈值 | Methods Protein surface convexity calculation |
| −0.0669/0.056、−0.0593/0.058、−0.0310/0.001（1/Å） | 三对复合物中 binder（负=凹）与靶（正=凸）的凸度实测 | Table 1 Convexity 列 |
| PDB 1I85 / 1KTZ / 3BIK / 5V52 / 7TZH / 1M9Z | 凸面表位示例复合物 / TGFβRII-TGFβ3 / PD-1-PD-L1 / TIGIT-CD112 / LAG3-抗体 / phasing 用 TβRII | Fig 1a 图注 + Methods |

## 5. 结论——作者说了什么

1. 为凸面表位定制的凹面螺旋支架（5HCS）能做出球状迷你蛋白做不到的延伸沟槽/口袋结合面，"Design of such extended grooves and pockets is nearly impossible using small globular miniproteins"，同靶头对头下最富集 binder 全部来自 5HCS。
2. 三个免疫治疗靶点均获亚纳摩尔到皮摩尔级亲和力（低 nM 至 <100 pM）且经实验优化后显示强生物活性（摘要："achieving low nanomolar to picomolar affinities and potent biological activity following experimental optimization"）。
3. TGFβRII 与 CTLA-4 共晶结构与设计模型高度一致（"structures of the TGFβRII and CTLA-4 binders in complex with their respective receptors closely match the design models"）；SSM 保守性指纹证明设计界面上的核心/界面残基如模型所料被强保守。
4. CTLA-4 binder 六聚体化后功能 EC50 与 Ipilimumab 持平，提示空间位阻/avidity 是抗体效价优势的来源之一。
5. 展望：设计小蛋白既往在人上未见高免疫原性、可融 Fc/白蛋白域延长循环；5HCS 可与 partial RFdiffusion 等 ML 骨架生成法衔接；重复蛋白架构适合加装条件性结合/掩蔽逻辑做下一代组织特异性免疫治疗（讨论段，属作者前瞻主张，本文无体内数据支撑）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇的杠杆在"靶几何分型→工具家族定制"，不在筛子本身**。三闸阈值（ddG/CMS/pAE）与 B09/C02 一脉相承、几乎没改；改的是**支架形状与表位形状的匹配**。→ 对我们：筛选漏斗第一问也许不是"阈值取多少"，而是"靶位点的化学几何属于哪一类、现有工具库里有没有对应形状"。
2. **计算闸口有失效模式，且他们备了实验闸口兜底**：AF2 与模型不自洽时直接切 SSM 热图（第 2.2 条）。注意兜底路径把"筛选"从算力换成了库通量——**当预测器不可信时，他们宁可花展示库的钱也不信一个不自洽的 AF2**。我们目前只有"信/不信 xTB"的二元选择，缺这条降级路线。
3. **Kd 与细胞效价可以解耦甚至倒置**（第 2.3 条：结合强抗体两个数量级、封闭功能反而弱）。对治疗语境，受体占有率/几何 ≫ 亲和力数字；对酶设计，类比是"结合底物 ≠ 转换底物"，亲和力类判据不能代理催化。
4. **命中率口径在三个靶之间不统一**（67 无命中数、4600→6、96→2），作者没有把三靶放进同一张命中率表。这提示其展示漏斗的瓶颈在"下单条数预算"而不是筛子通过率——与 B09（先给筛子打分再下单）是两种工程姿态：B09 优化"送测集合的纯度"，本篇优化"支架与靶的适配"。
5. **"设计端只管拿到命中、亲和力靠便宜的展示端成熟"** 是本篇固化的分工：计算端最贵的 AF2 只出现在准入与初始过滤，成熟阶段主力是组合库+分选。这条分工是 Baker 系 binder 论文（C02→B09→B11/DICE→本篇）演进链上的稳定架构。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：CTLA-4 最优 binder 亲和力超出 BLI 可测范围（<100 pM 是上限而非测量值）；PD-L1 用 SPR 才拿到规整结合曲线；Ipilimumab 效价优势只给了 "may contribute" 级别的解释。
- 作者未做（我们读出）：① **无体内数据**——无 PK、无免疫原性、无动物疗效，讨论段的转化主张全部悬空；② TGFβRII 初筛命中数缺失，三靶无法横向算统一命中率；③ PD-L1 只有**游离态**晶体，复合物结构未解（0.75 Å 是游离体对设计模型的偏差，不等于界面预测正确）；④ CTLA-4 靶区正文前后记法不一致（引入段说 beta-turn 132–140，结构段一处写 L98–Y104、另一处写 L128–Y136），本卡不复择其是、只如实登记矛盾；⑤ AF2 为何在 CTLA-4 不自洽没有分析，"何时弃用 AF2 闸"没有判据；⑥ 全程无 MD/QM，任何动力学/机理层面的说法都不在本文证据范围内。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **表位几何分型先行**：他们的"凸度=球拟合半径倒数+内积符号"是可计算的靶预分类。对我们：对每个候选酶的可结合/可作用表面做同类几何与化学分型（凹槽/平面/凸脊、电荷分布），**按类别指定工具**（对接友好者用对接、需诱导契合者用短 MD、需要电子结构者才上 xTB），而不是全库共用一套漏斗。
2. **双路亲和成熟的降级开关**：预测器与设计模型不自洽 → 立刻切换实验反馈路径。对我们：为每个判据（Foldseek 自洽、xTB 能垒、MD 接触时间）预先写明"不自洽时的替代证据源"（如同位点失活突变谱、无酶活阴性参照组的信号谱），避免卡死在单一预测器上。
3. **头对头小样本对照**（67 vs 4310 同靶并跑）：新工具验证不需要绝对命中率，只需要**同一靶、同一预算、并排跑**。我们评估任何新打分器都应先做这种同靶头对头，而不是拿历史平均值对比。
4. **功能读数与结合读数并报**：他们把 KD 与细胞 EC50 分开报、并暴露两者倒置。对我们：任何"预测结合/预测构象"指标必须与化学事件级读数（分步化学事件归因）并报，禁止用前者代理后者。

**不可迁移（为什么不能照搬）**

1. **ddG<−40 / CMS>400 / pAE<10 是"结合界面"判据**，binder 成功 = 静态界面形成；酶设计成功 = 三步化学事件顺序完成且不出副产物。本库判据标准明令禁止把 binder 阈值当酶活闸口——这篇不例外，这些数字对我们**只有流程位置参考价值，没有阈值移植价值**。
2. **展示库通量不可比**：酵母 one-pot 库 + 多轮 FACS 动辄 10^7 转化、4600 条送测；我们的湿实验一轮最多几个构建体、LC-MS/MS 逐个产物鉴定。他们"漏斗后段靠便宜大样本成熟"的经济结构在我们这里不成立，末端必须是信息量最大化。
3. **"亚 nM/皮摩尔亲和力 + 共晶 0.34 Å"不可作为我们任何成功概率或校准点**：这是结合蛋白的指标，与催化效率无映射关系（本文自己也证明了 Kd→EC50 可以倒置）。
4. **SSM 全饱和库**对我们同样奢侈：每个候选位点×19 突变×产物化学验证做不起，只能借"保守性指纹"的**思想**（把突变效应当第二证据），不能借其实现。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/immune_receptor_binder2025.txt

- 本卡全部英文引句均从上述抽取件复制粘贴（写卡前逐条 substring 预检，其中 4 条因抽取件数字与单位间存在细空格 U+2009/不间断空格而弃用或截断到安全边界，见第 3/4 节正文对未入引句数字的说明）。
- 对照底稿行号：`sources/baker.md:419–429`（[B32] 原卡）；`sources/cao.md:230–247`（[C14] 原卡）、`sources/cao.md:417`（C14 漏斗对照表行）。
- CSV 字段映射：第 3 节 ↔ 计算筛选判据/阈值/候选生成；第 4 节 ↔ 候选递减/命中率/成本；第 8 节 ↔ 方法演进链位置。
- **自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B32; C14" --no-report`，结果见本节末运行记录（引句逐条命中声明底稿）。

<!--CSV回填
work_type=论文（de novo binder 设计 + 结构/细胞功能验证）
target=TGFβRII、CTLA-4、PD-L1（三个凸面表位的癌症免疫治疗受体）
backbone_generation=理想螺旋/loop 片段组装 helix-turn-helix-turn 模块（30–50 aa）×3 重复、N/C 端截断成 <120 aa 五螺旋凹面束；Rosetta HybrizeMover 骨架多样化 + LayerDesign 出序列；RANSAC 球面拟合（阈值 1 Å、max iteration 100k）量化凸度并剔除凸面骨架
computational_filters=支架端：AlphaFold2 mean pLDDT cutoff 80 + DeepAccNet 0.8；界面端：ddG 小于 −40、contact molecular surface 大于 400、AF2 initial guess pAE 小于 10（CTLA-4 分支无 pAE 闸）；组合库端：ProteinMPNN 5000 倍重采样（温度 0.4）+ ΔddG 突变排序；CTLA-4 分支 AF2 不自洽后改用 SSM 富集热图做实验闸
thresholds=AF2 pLDDT≥80；AccNet≥0.8；ddG<−40；CMS>400；pAE<10；螺旋 18–22 aa；支架<120 aa；RANSAC 1 Å/100k 迭代；界面残基 ΔSASA 0.5 Å²；PDB 聚类 40% 序列同一性；组合库富集取前 10%；BLI 三浓度全局 1:1 拟合
md_used=否（全文无 MD；solvation-free energy 仅概念性表述）
qm_used=否
experimental_methods=oligo 池编码→酵母表面展示（with/without-avidity 两种标记，多轮 FACS+NGS）→SSM 全饱和突变库结合指纹→简并密码子组合库亲和成熟→E. coli 表达+SEC→BLI（PD-L1 加 SPR）→CD 热熔→X 射线共晶/游离晶体（SER-CAT 22-ID、LRL-CAT ID-31、NSLS-II 17-ID-1/17-ID-2）→HEK293 SMAD2/3 与 Jurkat CTLA-4/PD-1 报告基因封闭实验→A431 CRISPR 敲除染色特异性
pipeline_counts=支架库 7476；送测 TGFβRII 67（5HCS）+4310（迷你蛋白对照）、CTLA-4 4600、PD-L1 96；命中 CTLA-4 6 个（与设计 100% 序列一致）、PD-L1 2/96、TGFβRII 初筛条数原文未给；成熟阶段 E. coli 复测 4/4/10 个克隆
hit_rate=PD-L1 2/96≈2.1%；CTLA-4 6/4600≈0.13%；TGFβRII 未给（只报最富集者全来自 5HCS）；同靶头对头 67 vs 4310 下 5HCS 全胜；成熟后亲和力低 nM–<100 pM
best_metric=5HCS_CTLA4_1 对 CTLA-4 亲和力记作 <100 pM（BLI 解离过慢无法定量）；5HCS_PDL1_1 K_D 0.646±0.02 nM；共晶复合物 RMSD 0.34 Å（CTLA-4）与 0.55 Å（TGFβRII，1.24 Å 分辨率）
cost_or_stat_note=合成基因购自 IDT；组合库酵母转化效率约 10^7；三靶 SSM 分选浓度 1.6/10/6 nM；BLI 解离相 800–3600 s；晶体学数据取自三/四条同步射线束线；全文未报 GPU/CPU 计算成本；Ipilimumab 对照 KD 18.2 nM（引自文献 27）
role_in_timeline=Baker binder 演进链上"支架形状适配表位几何"的代表作：沿用 C02（曹 2022）RIF 对接与 ddG/CMS 漏斗、B09 的 AF2 pAE 闸口，解决其球状迷你蛋白在凸面免疫受体表位上做不出亚纳摩尔的形状互补瓶颈；确立"设计端出命中、展示端出亲和力"的三段式分工，并把 partial RFdiffusion 与条件性掩蔽列为后续方向（曹龙兴署名第 16/28 位，同时登记为 C14）
source_pointer=data/interim/baker_lit/ft/immune_receptor_binder2025.txt; sources/baker.md:419-429; sources/cao.md:230-247,417
CSV回填-->
