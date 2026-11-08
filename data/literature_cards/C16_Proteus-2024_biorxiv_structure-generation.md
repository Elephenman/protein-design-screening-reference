# [C16] Proteus：不用预训练的蛋白骨架扩散生成器——它把"能不能设计"定义成同族深度学习模型的自评

Wang C（王晨彤，浙大/西湖）、Qu Y、Peng Z（Duke）、Wang Y、Zhu H、Chen D、Cao L（曹龙兴，末位通讯，西湖生命科学学院）
bioRxiv 预印本，2024-02-10 提交、**2024-02-12 posted**（本地底稿页脚原句："Posted February 12, 2024."）· DOI 10.1101/2024.02.10.579791 · 登记号 EPMC PPR804303
**注意版本**：本卡读的是 **v1 预印本（bioRxiv，未经同行评审）**，不是正式发表版；截至底稿抓取时**尚无 Nature/NatComms 版本可对照**，且作者自己声明代码在接收前不公开。CSV 里的标题（Exploring Protein Structure Generation…）与预印本页面正文标题（pioneering protein structure generation…）**用词不同**，本卡一律以底稿正文标题为准。

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 第 73 行，编号 **C16**（组：曹龙兴组；年份 2024；类型：预印本） |
| 本文取回方式 | 登记 `batches.tsv` 第 18 行：`state=FULLTEXT`、`fetch_status=OK`、`fetch_note=fallback_ok[biorxiv_full] via https://www.biorxiv.org/content/10.1101/2024.02.10`；实际落盘文件名为 `PPR804303`（Europe PMC 预印本记录号） |
| 本地全文（唯一底稿） | `data/literature_cards/fulltext/C16_PPR804303_text.txt`（51,664 B，单行无换行）＋同名 `C16_PPR804303_fullTextXML.xml`（211,399 B） |
| 版本与日期 | **预印本 v1**：bioRxiv 2024.02.10.579791，doi 10.1101/2024.02.10.579791，posted February 12, 2024；底稿无修订版本号字段（无 v2/v3 记录） |
| 登记底稿对照 | `sources/cao.md:260–267`（原卡为**摘要级**）与 CSV 第 73 行（多处写"未记录/摘要级"）——本次按全文写卡后，原记录的保守程度**已过时**：正文其实含 Methods、数据集约 5 万条的构建规则、消融与 16 条湿实验计数 |
| 证据级别 | **全文级**（本卡全部引句均可在 `C16_PPR804303_text.txt` 逐字命中；见第 9 节） |
| 未取到的部分 | **Table 1/2/3/4/5/6 的表体数值全部缺失**（底稿里只有 "View this table: View inline View popup Download powerpoint" ＋表题；实测 XML 中 `<td>` 计数为 0）。因此"Proteus 超过 RFdiffusion 多少个百分点""success efficiency 具体秒数""消融各档得分"在本地**不可复算**，本卡凡涉及处一律写"作者声称，数值未取到"。Fig 1–4 原图、补充信息、代码（作者声明接收后才放）同样未取到 |

## 1. 这篇到底解决什么（大白话）

蛋白从头设计现在的主流做法是：先用一个**骨架生成器**（扩散模型，如 RFdiffusion）造出一堆"理论上能折叠"的全新蛋白骨架，再用反向折叠模型（ProteinMPNN）填序列，最后靠实验筛。RFdiffusion 效果最好，但它是**从 RosettaFold2 预训练来的**——作者认为这让它"不可解释、架构想改也改不动"。于是一批**不做预训练、从零训练**的替代品（FoldingDiff、FrameDiff、Genie、Chroma）出现，但它们的设计可成功率都追不上 RFdiffusion。

这篇做三件事：

1. **换架构**：把 AlphaFold2 里那个很贵但很有用的"三角注意力"（考虑残基对 i-j、j-k、i-k 三条边互相约束）搬到**K 近邻图**上算，复杂度从 O(N³) 降到 O(NK²)，同时把节点/边/结构三轨（multi-track）互相喂信息。这样既不用预训练，又能在 100 步采样内出结果（对比 Genie 1000 步、FrameDiff/Chroma 500 步）。
2. **换数据**：训练集不只用 PDB 里的单体，还把**寡聚体拆成单链**、按 UniProt 去重、限长 60–512 残基、限制 loop 比例，凑到 50,773 条（FrameDiff 只有 20312 条，底稿不带千分位）。
3. **给一套"计算自评"口径 + 少量湿实验**：计算侧用 ProteinMPNN（8 条序列/骨架）→ ESMFold 回折 → **self-consistency Cα-RMSD < 2 Å** 判"可设计"，再用 A40 GPU 秒数折算成"success efficiency"；湿实验侧只下单 16 条长蛋白（12 条 300 aa + 4 条 500 aa），看 E. coli 表达、SEC 单分散峰、CD 二级结构与 25–95°C 热稳定。

**它的生成目标本身**（与既有骨架生成器的差别，一句话）：Proteus 做的是**无条件单体/多聚体骨架生成**（unconditional monomer generation + dimer/trimer/tetramer 复合物骨架），**不做**结合位点定向、motif scaffolding、配体/底物共折叠——即它只保证"造出来的骨架大概率能设计"，不保证"这个骨架能干某件活"。把功能约束写进生成回路是他们后续工作（Proteus2 / C22、HalluDesign / C19）才做的事。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **"不预训练"这一条本身带来的性能落差，是全文的出发点。** 作者先把前人路线的失败摆出来：FoldingDiff 用内坐标+双向 transformer 迭代去噪，"Though FoldingDiff yields protein-like backbones, the majority of generated structures are predicted to not be designable"；对整批免预训练模型的判断是 "there remains a significant gap compared to RFdiffusion"，并直接指出后果 "This disparity results in limitations for these models,"。同时把 RFdiffusion 的问题说成架构层面："which makes it very uninterpretable and impossible to modify the model architecture for performance"。
   → **他们做了什么**：不改用预训练，而是改**网络模块**——把 AF2 的三角注意力搬到 KNN 图上（graph triangle block），再加 self-condition 与数据集扩充。
   → **应对后仍留下的代价**：作者自己在消融里承认前两项不够——"Though these modifications greatly improve the model's performance, it still lags behind RFDiffusion"，只有"Proteus surpasses RFdiffusion by introducing the local triangle graph"；而支撑这句话的 Table 4 表体数值**本地未取到**，所以"超过多少"不可复算。
2. **AF2 的三角模块搬到扩散上，第一道墙是显存和墙钟。** 原句给了具体量级："A single layer of Evoformer can consume up to 20GB of memory when training on a 384-residue protein"（因此需要 gradient checkpoint，而 Evoformer 有 48 层）；"In terms of diffusion modeling,"。
   → **他们做了什么**：只在**每个残基的 K 近邻**上算三角注意力，"we define k nearest neighbor residues for each"，把复杂度写成 O(NK²)，N∗N 边只保留便宜的 multiplicative update；由此单层不再需要裁剪输入，"we can now train on much longer proteins without"，"We can handle proteins up to 512 residues in"。
   → **代价**：三角约束从"全局"变成"局部图"，长程几何只能靠 self-condition 与边更新间接传播；作者用"at least a threefold speedup"和步数下降来替代对这一损失的直接测量，**没有给出 K 值消融**（正文未记录 K 的具体取值与敏感性）。
3. **第二个概念性难点：三角技术原本靠 MSA 喂边表示，扩散任务里没有结构可用。**"Another inconsistency when applying the triangle"。
   → **他们做了什么**：反过来利用扩散过程**带噪的输入结构**——"we calculate the third edge's inter-atom"，并用节点表示经前馈网络做门控，使 node/edge/structure 三轨都能进这一层。作者把这一步当成新发现："which is a new finding that is unexplored by"。
   → **代价**：该 bias 在噪声极大的早期步几乎无信息，作者未分析信噪比随 timestep 的变化（只写了辅助损失"仅在 t < 0.25 时施加"这一条经验规则）。
4. **效率不只是速度，而是"每出一个可设计骨架要花多少秒"。** 作者定义 "Success efficiency is computed as the computation"，并强调 "With finite computational resources,"。
   → **他们做了什么**：把采样步数压到 100（"This is in contrast to Genie,"），理由是表示能力增强后"the model achieves superior results even with"；同时把基线模型的失败按口径分开报：Genie 的长度上限问题"Genie fails to generate backbones larger than 600"，Chroma 的时间-质量权衡"Chroma becomes more time-efficient when"但"its success efficiency lags"。
   → **代价**：步数-设计性曲线（Table 3）表体未取到，"100 步足够"这一结论本地只能当作作者声明；对比表里还出现整模型零命中的记号——"* means the model does not predict any designable backbone in 200 samples"，说明基线在小分母下会出现"0 命中"这类不可比较的格子。
5. **基线之间的"公平性"问题：反折叠器与评判器不该一家通吃。**
   → **他们做了什么**：评价统一用 ProteinMPNN（temperature 0.1），但**唯独 Chroma 换用它自家的 ChromaDesign**，理由是 "we have observed a higher"（底稿里 ChromaDesign 被排版断词成 Chro-maDesign，本卡按底稿原样引；图注固定为 "8 sequences of each backbone"）。这是一次**为基线放宽口径**的对照修正。
   → **代价**：不同模型的 scRMSD 来自不同评判器，"跨模型可设计性"因此不是同一把尺子；ChromaDesign 的具体参数（temperature 0.1、diffusion augmentation 0.5）虽给了，但"换评判器带来多少分数增益"没有单独量化。
6. **多样性指标容易被"垃圾结构"刷高——作者主动把不合格样本从分母里剔掉。**"Notably, we only consider designable back-bones defined as those with a C α -RMSD of < 2, Å"，解释是 "sub-optimal models often"、"Including such backbones in the"。聚类用"we cluster the backbones using"。
   → **代价（本文未解决）**：分母被条件化之后，"diversity = 可设计簇数 ÷ 生成总数"里的总数到底是全部生成数还是可设计数，正文表述不一致；读者无法据此还原簇数。
7. **湿实验侧的短板，作者没有正面处理。** 全篇实验只有"16 条下单"这一档，判定口径是表达＋SEC 单分散＋CD 二级结构＋热稳定，没有任何原子分辨率结构或功能测定（本地全文里 **crystal / NMR / cryo-EM / activity 等关键词一次都没出现**）。
   → **本文未解决**：这 16 条是怎么从生成的上千条骨架里挑出来的（按 scRMSD 排序？随机？人工挑形貌？），正文**未记录**；实验也不回算每条的 scRMSD 与命中的对应关系，因此湿实验既不能校准 scRMSD 阈值，也不能给出可引用的命中概率。作者仍把两件事并列写成结论："Proteus demonstrated cutting-edge designability and efficiency in computational evaluations"、"We tested the reliability of"。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **生成器本体**：SE(3) 扩散（沿用 FrameDiff/IG-SE(3) 那条线：平移在 R³ 上做前向、旋转在 SO(3) 上用 Brownian motion 的概率估计与条件 score），采样用 Euler-Maruyama 离散化。损失端 "We have adopted the training"（去噪平移+旋转 score matching，加 pairwise distance matrix 与骨架原子坐标两个辅助损失；"We apply auxiliary losses when"）。
- **架构三轨**："A folding block comprises an"；IPA 之后接标准 transformer，Backbone Update 取自 AF2 的线性层出平移/旋转增量；边表示初始化用 AF2 的相对序列距离图，self-condition 时再加上一轮预测的 Cα 距离图与相对旋转特征；层间不共享权重（"The entire network consists of"）。
- **训练数据**：PDB（截止 2023-08-01）→ 寡聚体拆单链 → UniProt 映射去重 → 长度与 loop 比例过滤 → 50,773 条单链。
- **计算评判器（本文的"成功"由此定义）**：ProteinMPNN（temperature 0.1；Chroma 骨架改用 ChromaDesign）出序列 → **ESMFold** 单序列回折 → scTM（越高越好）与 self-consistency Cα-RMSD，阈值 **< 2 Å**；计时用 **A40 GPU**；多样性用 **MaxCluster**（TM-score cutoff 0.6）聚类。
- **复合物生成**：在相对位置索引上加 chain break（"we add chain breaks first"）；初始帧"sampled from rotation and"。
- **湿实验**：合成基因（"Synthetic genes encoding"）→ pET28a（His tag + HRV 3C 酶切位点）→ BL21(DE3) → Ni-NTA IMAC → 3C 切 tag 后二次 IMAC → Superdex 200 Increase 10/300GL SEC → CD 光谱（"Circular dichroism spectra were"）。
- **没有用的方法**：本文**没有任何 MD、QM、自由能微扰，也没有结合/催化功能测定**；结构侧只有"设计骨架 vs AF2/ESMFold 预测"的叠合（Fig 4B 图注："Designs (grey) overlaid with AF2 predictions (colours) are shown on the left"）。这决定了它能给"会不会折叠、会不会表达"的证据，给不了"会不会干活"。

### 生成目标与既有骨架生成器的差别（本文自己的坐标系）

| 对象 | 它的生成目标 | Proteus 相对它的差别（作者说法 + 本地可核的部分） |
|---|---|---|
| RFdiffusion | **条件**生成（binder、motif scaffolding、对称设计），从 RosettaFold2 预训练 | Proteus **不预训练**、只做无条件单体/寡聚体骨架；作者称设计性与效率反超，尤其长链："Proteus is comparable with"、讨论里进一步写"we even largely surpass RF"；具体数值在 Table 1，**本地不可复算** |
| FrameDiff | SE(3) 扩散 + 简单消息传递层，PDB 单体 20312 条、采样 500 步 | 同一扩散公式与损失，换的是**边更新模块**（graph triangle）＋数据集拆链扩到 50,773 条＋步数降到 100 |
| Genie | 残基坐标直接扩散，AF-SwissProt 195214 条（pLDDT 阈值 80、最多 256 残基）、采样 1000 步 | Proteus 训练长度上限更高（512、不裁剪）；作者给出 Genie 的两个失败模式：步数与"Genie fails to generate backbones larger than 600 residues due to being out of memory" |
| Chroma | 通用可控生成（图 + 调和约束），采样 500 步 | 同属 graph-based，但用 IPA＋三角把表示能力提上去："With the best designability and"；短于 400 残基 Proteus 更快（"Proteus is faster than Chroma"），长于 400 时 Chroma 更省时间，但"its success efficiency lags" |
| FoldingDiff | 内坐标/二面角序列去噪，CATH 30395 条、crop 128 | Proteus 直接在 SE(3) 帧上扩散；作者对前者的结论是"Though FoldingDiff yields" |
| EvoDiff（纯序列扩散） | 只生成序列 | 作者拿它的实验表现作反面："the structure prediction" |

**一句话概括差别**：别人的改进点在"条件与功能"（RFdiffusion 的 scaffolding、Chroma 的可控生成），Proteus 的改进点在**"无条件骨架的设计性 + 每-可设计-骨架-成本"**，即把生成器本身做成更便宜更准的底座；功能约束（位点、配体、底物）留给他们后续的 Proteus2 / HalluDesign。

### 工作流程表

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 数据 curation | PDB 全部条目，"with a cutoff date of August" | 寡聚体拆成单链 → 序列映射 UniProt ID → 同 UniProt 且重叠达标只留最高分辨率 → 长度与 loop 过滤 | 长度 **60–512** 残基；**最多 50% loop**（DSSP 判定）；"having an 80 percent sequence"；"We kept proteins that contained" | "This curation process resulted"（对照：FrameDiff "resulting in a dataset containing 20312 chains"、Genie 用 195214 条 AF-SwissProt、FoldingDiff "FoldingDiff uses a total of"） |
| W2 训练 | 50,773 条单链骨架帧 | SE(3) 扩散 + 去噪 score matching；三轨 folding block；可选 self-condition（上一轮预测的 Cα 距离图 + 相对旋转特征） | 辅助损失只在 **t < 0.25** 施加："Empirically, we have observed"；训练长度上限 **512** 残基、不裁剪 | 单一模型权重（Table 6 训练参数表体本地未取到） |
| W3 采样（单体） | 随机初始帧（平移取高斯、旋转由 so(3) 正交基系数合成） | Euler-Maruyama SDE 求解，迭代 N 步；"Proteus takes the input noisy" | Proteus 用 **100 步**，理由"Proteus only requires 100"；对照"This is in contrast to Genie," | 正文口径："We sample 200 backbones for"；**Fig 1 图注多出一档 800**："All metrics are averaged from" ⇒ 正文 5 档、图注 6 档，两处口径不一致，本卡不合并；Table 1 表题另一口径"average from length 100, 200," |
| W4 计算评价（designability） | 每条生成骨架 | ProteinMPNN 出序列（每骨架 8 条、temperature 0.1；Chroma 用 ChromaDesign）→ 每条序列 ESMFold 回折 → 取与设计骨架的最高 TM-score（scTM）与 scRMSD | "We use a C α -RMSD threshold of"；"8 sequences of each backbone"；"The designability of the" | 各模型每长度的可设计比例 → Table 1（**表体数值本地缺失**，故"超过 RFdiffusion"只能记为作者声明） |
| W5 计算评价（efficiency） | 生成一条骨架的墙钟 | 在单张 A40 上计时，再算 success efficiency | "Efficiency is estimated based"；"Success efficiency is computed"；"* means the model does not*" | Table 2（逐长度逐模型秒数，**表体缺失**）；作者据此称三角+图带来"This results in at least a" |
| W6 计算评价（diversity） | 全部**可设计**骨架 | MaxCluster 按 TM-score 聚类，算可设计结构簇数 ÷ 生成骨架总数 | "we cluster the backbones using"；"Notably, we only consider" | Fig 1 雷达图的 diversity 轴（数值未取到）；剔除理由见第 2.6 条 |
| W7 复合物生成 | 2/3/4 条链，链间允许断链 | 相对位置索引加 chain break 后采样，与 Chroma 同口径比 | "We test scRMSD on two chains(dimer), three chains(trimer), and four chains(tetramer). Each chain is fixed to 200 residues"；"We compare Proteus' ability to" | Fig 3（每类 200 条样本）；作者称"far surpassing Chroma"，数值未取到 |
| W8 消融 | 同一评测口径 | 把改进拆三块分别加回：数据集扩充 / self-condition / 架构（local triangle graph 与 structure bias） | "Ablation data is presented in"；判据仍是 W4/W5 的 scRMSD 与效率 | "We make detailed ablations in"；结论是加完前两项仍"it still lags behind RFDiffusion"，"Proteus surpasses RFdiffusion"（Table 4 表体缺失） |
| W9 湿实验（本文唯一的非计算证据） | 生成出的长蛋白设计 | 下单合成基因 → pET28a（N 端或 C 端 His tag + 3C 位点）→ BL21(DE3)、50 ml LB + 50 mg/ml 卡那 → IPTG 诱导（37°C 过夜，或 37°C 长 6–8 h 后 20°C 过夜）→ 超声裂解、12,000 × rpm 澄清 → Ni-NTA IMAC（"were washed five times with 5"，30 mM 咪唑洗 / 300 mM 咪唑洗脱）→ 15% SDS-PAGE → 3C 切 tag + 二次 IMAC → Superdex 200 SEC → CD | 判定口径**只有三条**：SEC 单分散峰对应预期分子量、CD 二级结构与设计模型一致、25→95°C 二级结构保持；热熔解"measuring CD at 222 nm"，波长扫描"Wavelength scans (190 to 260"，蛋白浓度"protein concentrations ranging"；**这 16 条如何从生成池挑出、挑选用什么阈值，原文未给阈值** | "We ordered 16 designs, including 12 designs of 300 amino acid proteins and 4 designs of 500 amino acid proteins"；"All designs were expressed in"；命中"9 of the 300 amino acid designs" ⇒ **12/16**；"Experimental data is shown in" |

## 4. 关键数字台账（全部可在本地底稿逐字搜到；表体缺失处明写）

| 数值 | 含义 | 出处（底稿原句/位置） |
|---|---|---|
| 50,773（正文另一处写作 50773） | 训练用单链蛋白条数 | "This curation process resulted"；消融处 "resulting in a dataset of 50773" |
| 20312 / 195214 / 30395 | 对照数据集规模：FrameDiff（PDB 单体）/ Genie（AF-SwissProt）/ FoldingDiff（CATH） | "resulting in a dataset containing 20312 chains"；"FoldingDiff uses a total of" |
| 60–512 残基、80% 重叠、≤50% loop | 数据过滤阈值 | "ensuring a maximum chain length"；"having an 80 percent sequence"；"a maximum of 50 percent of the" |
| 20 GB / 384 残基 / 48 层 | Evoformer 单层显存量级（他们要绕开的成本） | "A single layer of Evoformer can" |
| ≥10 min / V100 / 50 步 | 用 AF2 做扩散生成的墙钟 | "Alphafold2 can take at least 10" |
| O(N³) → O(NK²) | 三角注意力的复杂度削减（本文核心工程主张） | "we introduce the graph triangle" |
| 512 vs 384 | 训练可容纳的最大链长（Proteus vs AF2/RFdiffusion） | "We can handle proteins up to" |
| at least 3× | 图三角带来的加速（作者自述，无对照表可核） | "This results in at least a" |
| 100 步 vs 500 / 1000 步 | Proteus 与 FrameDiff/Chroma/Genie 的采样步数 | "This is in contrast to Genie," |
| 200 条/长度；长度 100/200/300/400/600（正文）；600/800（图注多出 800） | 计算评测的送样分母 | "We sample 200 backbones for"；"All metrics are averaged from" |
| temperature 0.1；8 条序列/骨架；ChromaDesign augmentation 0.5 | 反向折叠评价参数 | "To evaluate designability,"；"8 sequences of each backbone" |
| scRMSD **< 2 Å**（且 scTM 越高越好） | "可设计"的判定线（本文最重要判据） | "We use a C α -RMSD threshold of" |
| 单张 A40 秒数 | success efficiency 的计价单位 | "Efficiency is estimated based"；"how many seconds on a single A40" |
| \*（200 样本内 0 命中） | 表 2 里某模型整栏无可设计骨架的记号 | "* means the model does not*" |
| TM-score cutoff 0.6（MaxCluster） | diversity 的聚类阈值 | "we cluster the backbones using" |
| 辅助损失仅 t < 0.25 | 训练细节 | "We apply auxiliary losses when" |
| dimer / trimer / tetramer，每链 200 残基，每类 200 条 | 复合物评测设定 | "We test scRMSD on two chains(dimer), three chains(trimer), and four chains(tetramer). Each chain is fixed to 200 residues" |
| **16 条下单 = 12×300 aa + 4×500 aa** | 湿实验的**送测分母** | "We ordered 16 designs, including 12 designs of 300 amino acid proteins and 4 designs of 500 amino acid proteins" |
| **9/12 与 3/4 → 12/16** | SEC 单分散峰命中数（本文唯一实验命中计数） | "9 of the 300 amino acid designs" |
| 25°C–95°C；222 nm；190–260 nm；0.6–0.9 mg/ml | CD 与热熔解测量口径 | "maintaining a stable secondary"（同句写作 ther-mostable）；"Thermal melt analyses were"；"Wavelength scans (190 to 260"；"protein concentrations ranging" |
| pET28a / BL21(DE3) / 50 ml LB + 50 mg/ml 卡那 / 1 mM IPTG / 12,000 × rpm / 30 与 300 mM 咪唑 / 15% SDS-PAGE / Superdex 200 Increase 10/300GL | 湿实验全部定量参数（可照抄复现） | 附录 "B. In vitro experiment protocol" 段，例如 "The cell lysate was cleared by"、"and eluted with 6 mL of elution"、"Both eluates were analyzed" |
| **不可获得**：Table 1/2/3/4 的任何单元格数值 | 各家模型的 scTM/scRMSD 分布、每长度的秒数、消融各档得分、K 值与 L 层数（Table 5/6） | 底稿只有表题与 "View this table: View inline"，XML 内 `<td>` 计数为 0 ⇒ 本卡所有"Proteus 优于 X"的说法只能记为作者声明 |

## 5. 结论——作者说了什么（只写作者写过的）

1. **免预训练也能赢预训练**："we accomplish higher designability and efficiency without pretraining"；摘要口径是 "Proteus demonstrated cutting-edge designability and efficiency in computational evaluations"，并称 "it is able to generate proteins"。
2. **设计性上超过全部现有扩散模型，含 RFdiffusion**："We surpass all current diffusion models in designability"（底稿此处把 RFdiffusion 断词成 "even RFdif-fusion, which uses a"，引句按底稿原样保留，不做拼写"修正"）；长链优势："Proteus is comparable with"，讨论里进一步写 "we even largely surpass RF"。
3. **效率上与 Chroma 同档、步数只有 100**："Notably, while maintaining the"；success efficiency 口径下作者称全面领先（Table 2 数值本地不可核）。
4. **复合物生成的外推能力**："The outstanding performance of"。
5. **湿实验用作可靠性背书**："We tested the reliability of"；具体为 16 条下单、E. coli 表达、12/16 出单分散峰、CD 与设计一致、25–95°C 稳定（"Experimental data is shown in"）。
6. **消融自陈的失败模式（作者自己写的短板）**：只加数据与 self-condition 时 "Though these modifications"，必须 "Proteus surpasses RFdiffusion"；并认为结构 bias 的作用是新发现（"The structure bias used in the"）。
7. **未来方向**：大纳米颗粒生成（"First, there is the area of"）与蛋白-配体共折叠（"we aim to bring accurate and"）。
8. **可复现性自我声明**："The source code of Proteus will"（即截至该版预印本无代码）；Impact Statement 里未列出具体风险："There are many potential"。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **评价口径是"计算自评为主、湿实验为点缀"，而且自评是同族深度学习闭环**。生成器是 DL（Proteus），评判器也是 DL（ProteinMPNN 出序列 + ESMFold 回折，湿实验图里还叠加 AF2 预测），全程没有物理量（无能量、无 MD、无 QM）。所以"remarkably high success rate"实际含义是**高自洽率**：同族模型之间互相认得。湿实验只能否证极端情形（完全表达不出来），**不能确证阈值**。
2. **最可疑的一条判据：他们把计算阈值直接写成了对实验结局的断言**。底稿里有一句被图注打断的话——前半 "A generated protein is considered non-functional and likely to fail experimental validation if"，后半在图注之后才接上 "the C α -RMSD between the"（两句在原文被 Figure 3 图注隔开，本卡分成两条引句、不拼接）。这就是**用判据定义结局**：scRMSD 超 2 Å 就被预先判了实验死刑，于是后续任何"实验成功率高"都不可能是独立验证。
3. **12/16 是全文最硬、也最脆的数字**。硬在它是唯一非计算的观测；脆在三处：分母只有 16；**送测 16 条的挑选口径未记录**（正文没有 select/filter 描述）；判定口径是"可溶 + 单分散 + CD 二级结构"，**没有原子分辨率结构、没有任何功能测定**。按这三条，12/16 最多支持"这批骨架长得像折叠蛋白"，不支持"设计成功"。
4. **长链优势有一部分来自对手的显存墙，而不是自己的长程建模能力**。训练上限是 512 残基，却在 600（正文）/800（图注）残基上做评测并与 RFdiffusion 比——这是**分布外长度外推**；同时他们自己承认 Genie 在 >600 残基 OOM、Chroma 在 >400 残基比自己省时间。所以"长链更好"至少部分可比性来自对手跑不动，而非分数更高。
5. **作者把单体实验的结果外推到了复合物**。讨论里写 "Proteus has demonstrated"，但底稿的实验部分只有单体（16 条），复合物侧只有与 Chroma 的计算对比（Fig 3）。这一句在我们的记录里应当标为**超出其证据范围的表述**。
6. **真正的贡献是工程与口径，不是生物学**：KNN 图上的三角注意力（把 O(N³) 降到 O(NK²)）、把寡聚体拆链扩充训练集、以及把"设计性 × 每秒成本"合成 success efficiency。第三点与 B09（Bennett 2023）的 Efficiency=成功率×吞吐 是同一时代的同一动作：**当判据变强但变贵时，社区开始用单价重新选判据**。
7. **他们缺什么（对我们最有提示意义的缺口）**：没有把 scRMSD 与湿实验结果逐条对上（没有混淆矩阵），因此 2 Å 这条线在本文里从未被实验校准；也没有任何"失败长什么样"的可复用清单（不溶性 vs 聚集 vs 二级结构不符未分型）。这两点正是 B09 的 Type I/II 分型在做的事——本文在判据验证上比 B09 更弱。

## 7. 局限与失败（作者的 + 我们读出的）

**作者写明/可归因于作者的**

- 无代码、无权重："The source code of Proteus will"；训练超参与输入特征表（Table 5/6）表体亦未进本地底稿 ⇒ K 值、层数 L、hidden 维度、训练时长全部**不可复现**。
- 无预训练 = 放弃先验：作者以此为卖点，但也因此无法解释"为何 5 万条就能追上"；底稿 Impact Statement 未列任何具体风险："There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here"。
- 实验体量：16 条，作者未讨论这能否代表分布。

**我们读出、且本地可指证的**

- **口径不一致**：正文 "We sample 200 backbones for" vs 图注 "All metrics are averaged from"；表题又写 "The metric is average from"。三处两套长度，无法确定主表口径。
- **最强结论的数字不在本地**：Table 1/2/3/4 只有表题（底稿里就是一行 "View this table: View inline"，XML 中 `<td>` 计数 0）。⇒ 任何引用本卡的人**不得**把"Proteus 超过 RFdiffusion"当作已验证事实。
- **判据与被评对象同源**：可设计性由 ESMFold 单序列回折定义，而 ESMFold/ProteinMPNN 与生成器共享训练分布（PDB/UniRef）；底稿没有任何独立验证（无实验结构、无热力学 ΔG、无聚集体判断）。
- **湿实验挑选标准缺失**：底稿通篇没有"如何选出这 16 条"的记录 ⇒ 存在无法排除的选择偏倚。
- **复合物侧没有实验**，但结论里出现 "experimental success rates"（见第 6.5 条）。
- **底稿本身有残缺**：关键的阈值断言句被图注打断（见第 6.2 条），"Proteus takes the input noisy"段落亦与图注交错；抽取把 CD 一句写成 ther-mostable（连字符残留）。所以引用必须逐字，不能"顺手补全"。
- **登记记录与全文不同源**：`sources/cao.md:267` 记的"摘要原句"（These promising results underscore Proteus's ability to generate highly designable protein backbones efficiently）在本底稿中**搜不到**（该句来自 bioRxiv 摘要页/另一版本文本），CSV 第 73 行也因此把该文标为"摘要级/未记录"。本卡按底稿重写后，该文应升级为"全文级、但表体数值缺失"。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **把"单价"写进判据本身**（本文的 success efficiency = 出一个可设计骨架要多少 A40 秒；B09 的 Efficiency = 通过率 × 吞吐）。用法：我们每个判定动作都要报"每 1 个通过闸口的候选花多少核时"，再决定跑不跑。单价数字只能用我们自己实测的那批（MD 156.6 ns/day、新体系 10.6 GPU·h、xTB 271 原子 153.3 s/评价），**本文的 A40 秒数、步数不可搬来当我们的预算**。
2. **反向折叠只当"否证工具"，永不当"支持证据"**。他们的做法（生成骨架 → 出序列 → 单序列回折 → 比 RMSD）能廉价地否掉"任何序列都折不出这个形状"的骨架。对我们：结构通道候选可以加一条同构的折叠一致性检查，用于**淘汰明显非物理的预测结构**，但通过它不增加任何"会催化"的信念（见下条不可迁移 1）。
3. **扩充参照池而不动判据**：他们把寡聚体拆成单链，训练集从 20312 → 50,773 条并做消融证明有效。对我们：Foldseek/HMMER 的背景库、阳性锚集同样可以按链拆分条目以提覆盖；但必须像他们一样**为扩充单独做一档消融**，否则"库变大"只是把召回与自证混在一起。
4. **公开写对手的失败模式与自己的短板**（Genie 在 >600 残基 OOM、Chroma 的 success efficiency 落后、只加数据与 self-condition 仍 "it still lags behind RFDiffusion"）。这正是我们负面清单该长成的样子：点名哪个量具在哪一环失效、失效方向是什么。
5. **教训级迁移（最值钱的一条）**：**不许用判据定义结局**。本文把 scRMSD 超限直接写成"很可能实验失败"，从而让湿实验失去校准能力。对应我们的规则：任何"预计失活/预计无产物"的断言，必须由**独立阴性锚**（如 BcCdnD 的 9SAX 类读数）或已知失活背景支持，不能由同一套打分自证。

**不可迁移（为什么不能照搬）**

1. **scRMSD < 2 Å / scTM 是"骨架能不能被某条序列折叠"的静态判据，不是酶活判据**。我们的目标是三步化学事件（供体定位、中间体、竞争副产物）与催化几何，折叠一致既不必要也不充分；本库判据标准也明令禁止把结构自洽度当活性闸口。**本文全程不含任何活性或功能读数，不能为任何酶活判据提供依据。**
2. **12/16（75%）不得变成我们的"成功概率"或校准点**。分母只有 16、判定口径是可溶/单分散/CD、送测挑选标准未记录、且没有把实验结果与计算分对上（无混淆矩阵）。引用本文只许引方法结构，引数字只许引"分母与口径"作为反面教材。
3. **本文没有 MD、没有 QM、没有自由能微扰**，所以它对"用 MD/QM 判催化"这一类主张**不提供任何命中率背书**（那类参照本文没有）。
4. **它的生成目标是"无条件骨架"**，不含结合位点、催化基序、配体/底物条件。因此不能拿本文证明"Proteus 能设计带功能的蛋白"；功能条件化在曹组的后续工作里（Proteus2 → C21/C22、HalluDesign → C19），而**那些模型截至相应预印本未公开权重与协议**（"The source code of Proteus will be released once accepted."）。
5. **通量不可类比**：他们一次能采 200 条/长度、下 16 条基因；我们一轮最多几个构建体。所以漏斗末端必须是**信息量最大化**（机制多样性 + 失活对照 + 阴阳性同域），不是样本数最大化。
6. **表体数值本地不可得** ⇒ 本文的任何性能数值（含"at least a threefold speedup"这类自述）不得进入我们的对比表或论证链。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/C16_PPR804303_text.txt

- **实际照着写的那一份**：`fulltext/C16_PPR804303_text.txt`（51,664 B，单行、无换行；由 Europe PMC 预印本记录 PPR804303 的 fullTextXML 剥标签得到，同目录 `C16_PPR804303_fullTextXML.xml` 211,399 B 为原始 XML）。登记底稿另有 `sources/cao.md`（本卡只用于对照原记录，**不作为引句来源**，因为该文件里记的摘要句在本底稿中不存在，见下）。
- **本底稿的已知残缺（写卡时已逐条规避）**：① Table 1/2/3/4/5/6 只有表题，表体数值缺失（XML 内 `<td>` 计数为 0）；② Figure 1–4 只有图注文字，无图；③ 排版断词残留（RFdif-fusion、Chro-maDesign、back-bone/back-bones、ther-mostable）；④ 一处关键句被图注打断（"A generated protein is considered non-functional and likely to fail experimental validation if" 与 "the C α -RMSD between the" 之间插入了 Figure 3 图注），本卡拆成两条引句、未跨句拼接；⑤ 正文长度档 [100,200,300,400,600] 与图注 6 档（含 800）不一致，本卡两处各引各的、不合并。
- **对照登记记录（本次全文写的结果与原记录的差）**：`sources/cao.md:260–267` 与 CSV 第 73 行把本文记为**摘要级**、候选数递减与实验命中率均写"未记录"。全文核对后应更正为：**方法级信息齐备**（数据集 50,773 条与全部过滤阈值、采样步数、评价判据 2 Å/A40、16 条湿实验与 12/16 命中），但**性能数值不可得**（表体缺失）。原记录引用的那句摘要（These promising results underscore…）在本底稿中搜不到 ⇒ 属跨版本引用，今后不得作为逐字引句使用。
- **版本声明**：预印本 v1，doi 10.1101/2024.02.10.579791，底稿页脚 "Posted February 12, 2024."；无正式发表版对照；代码未公开。
- **本卡自检方式**：写卡过程中用与门禁同口径的正则（ASCII 直双引号、≥20 字符、不含中日韩、≥12 字母）在本地对底稿做逐字比对，共两轮：第一轮暴露 3 条 MISS（两条标题异体写法、一条含 ChromaDesign 的跨断词句），第二轮暴露 2 条（一条被断词、一条是我打算检验"登记摘要句是否存在"而故意下的探针——结论：不存在）；逐条改正或改为中文叙述后复跑，最终 `verify_literature_cards.py --only C16 --no-report` 输出见对话记录。**卡内不写"未验证"的数字**：凡表体缺失处一律标注"作者声称，数值未取到"。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/成本统计引用`；第 7 节 ↔ `实验命中率/最优指标`（本文这两格只能是"口径而非概率"）；第 8 节 ↔ `在方法演进链的位置`。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 122 条逐字引句来自许可受限的第三方来源（C16；CC_BY_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（bioRxiv 预印本 v1，2024-02-12 posted，未经同行评审；DOI 10.1101/2024.02.10.579791）
target=无具体靶蛋白：无条件蛋白骨架（单体 100–600/800 残基）+ 同源寡聚体复合物骨架（dimer/trimer/tetramer，每链 200 残基）；不含结合位点、催化基序或配体条件
backbone_generation=Proteus：SE(3) 扩散（继承 FrameDiff 的前向/score 公式与训练损失，无预训练）+ 三轨 folding block（IPA-Transformer、AF2 式 backbone update、graph triangle block）；三角注意力只在 K 近邻子图上算（O(NK²) 代替 O(N³)），N∗N 边仅做 multiplicative update；structure bias 取噪声结构的第三边原子间距 RBF 并由节点表示门控；可选 self-condition（上一轮 Cα 距离图+相对旋转特征）；层间不共享权重；寡聚体在相对位置索引加 chain break；Euler-Maruyama 采样 100 步
computational_filters=可设计性：ProteinMPNN（temperature 0.1，每骨架 8 条序列；Chroma 骨架改用 ChromaDesign temp 0.1 + diffusion augmentation 0.5）出序列 → ESMFold 单序列回折 → scTM 与 self-consistency Cα-RMSD；效率：单张 A40 计秒并换算 success efficiency；多样性：MaxCluster 按 TM-score 聚类；实验侧无计算-实验逐条对上（无混淆矩阵）；全文不含 MD/QM/自由能
thresholds=scRMSD < 2 Å 记为可设计（唯一成功判据）；辅助损失仅在 t < 0.25 施加；训练链长 60–512 残基、不裁剪；UniProt 同 ID 且 80% 序列重叠只留最高分辨率；DSSP loop 比例 ≤50%；MaxCluster TM-score cutoff 0.6；每长度采样 200 条（长度正文 100/200/300/400/600，图注含 800）；采样步数 Proteus 100 vs Genie 1000 vs FrameDiff/Chroma 500；湿实验送测挑选阈值原文未给
md_used=否（全文无分子动力学、无构象采样、无自由能计算）
qm_used=否（全文无量子化学、无过渡态或反应坐标计算）
experimental_methods=E. coli 表达（pET28a + His tag + HRV 3C 位点，BL21(DE3)，50 ml LB/50 mg/ml 卡那，1 mM IPTG 37°C 或 6–8 h 后 20°C 过夜）→ 超声裂解、12,000 × rpm 澄清 → Ni-NTA Superflow IMAC（30 mM 咪唑洗 5 次、300 mM 咪唑洗脱）→ 15% SDS-PAGE → 3C 切 tag + 二次 IMAC → Superdex 200 Increase 10/300GL SEC 判单分散峰 → CD（Chirascan V100，0.6–0.9 mg/ml，190–260 nm 扫描与 222 nm 热熔解 25→95°C）；无晶体/冷冻电镜/NMR，无结合或催化功能测定
pipeline_counts=训练集 50,773 条单链（PDB 截止 2023-08-01，寡聚体拆链）→ 计算评测每长度采 200 条骨架（5–6 档长度；总数为 200×档数推算，原文未直接给合计）→ 复合物每类 200 条 × 3 类 → 湿实验下单 16 条（12×300 aa + 4×500 aa）→ SEC 单分散命中 12 条（9/12 与 3/4）；生成池如何缩到 16 条：原文未记录
hit_rate=湿实验 12/16（300 aa 组 9/12、500 aa 组 3/4）为 SEC 单分散口径，非折叠正确、非功能命中，且送测挑选标准未记录；计算侧命中率（可设计比例）在 Table 1 表体，本地未取到，仅有作者定性声明（称超过全部扩散模型含 RFdiffusion、长链优势明显）；正文另有一句把 scRMSD 超限直接等同于很可能实验失败，属用判据定义结局
best_metric=未记录（本地底稿无 Table 1/2/3/4 表体 ⇒ 无 scTM/scRMSD 均值或分布、无 success efficiency 秒数；实验侧最优读数只有 25→95°C 二级结构保持与 SEC 单分散，作者未给 Tm 数值或 RMSD 数值）
cost_or_stat_note=计价口径：单张 A40 生成一条骨架的秒数，success efficiency = 得到一条 scRMSD<2 Å 骨架所需秒数；表内 * 表示 200 样本内零可设计命中；作者自述三角图带来 at least a threefold speedup；对照成本 AF2 扩散 50 步在 V100 上 at least 10 minutes、Evoformer 单层 20GB/384 残基、Genie 在 >600 残基 OOM；Proteus 采样 100 步；Table 5/6（输入特征与训练参数）表体缺失 ⇒ 训练成本与超参不可复现；代码声明接收后才公开
role_in_timeline=曹龙兴组从"使用 Baker 系生成器（RFdiffusion + ProteinMPNN）"转向"自研生成器底座"的节点，动机是免预训练（可改架构、可解释）与算力/显存成本；此后该线直接供血自家下游功能设计：Proteus2 用于酶-底物复合物共生成（C21/C22）、HalluDesign 用于迭代幻觉设计（C19）；本文自身停留在无条件骨架的设计性-效率层，未涉及功能判据，也未有实验-计算配对的阈值校准（对比同代 B09 用近百万湿实验标注给筛子打分）
source_pointer=data/literature_cards/fulltext/C16_PPR804303_text.txt（唯一逐字底稿，51,664 B，Table 1–6 表体缺失）+ 同源 C16_PPR804303_fullTextXML.xml（211,399 B）；对照登记记录 sources/cao.md:260-267 与 data/protein_design_literature.csv 第 73 行（原记为摘要级，本卡升级为方法级-全文级）
CSV回填-->
