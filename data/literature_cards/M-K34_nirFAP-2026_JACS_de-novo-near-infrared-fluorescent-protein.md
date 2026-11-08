# [M-K34] 从头设计近红外荧光激活蛋白——"80%+"末端数字的分母层级活体样本（口径对照行）

Liu Y., Arús B.A., Mishra K., Wang T., … Xu C., Baker D.（华盛顿大学 IPD / DKFZ / Helmholtz / NIBS 等）
Journal of the American Chemical Society 2026, 148(23):23530–23539 · DOI 10.1021/jacs.5c19594 · PMID 42227562 · PMCID PMC13560888
开放获取（CC BY 4.0）· 链接 https://doi.org/10.1021/jacs.5c19594

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **M-K34**（组：口径对照与独立复核；**不是 Baker binder 漏斗组本身**） |
| 本行当初为何进表 | `sources/claim-90pct.md` 第 110 行把它列为"表达率/结合率被转述成设计成功率"陷阱的**可核验邻近案例**：原文 10/12（83%）的分母是"合成下单的 12 条"，判据是"表达且结合视网膜醛"双条件——用来对照讲座里"90%+"到底是哪种口径 |
| 本地全文 | `data/interim/baker_lit/ft/nirFAP2026.txt`（44,480 B，PMC13560888 接收稿 NIHMS2203894 的纯文本抽取；写卡前已读文件头 600 字符核验身份：DOI 10.1021/jacs.5c19594、PMCID PMC13560888、页码 23530–23539 均与本行一致） |
| 证据级别 | **全文级**（本卡全部引句均可在该底稿里逐字命中；见第 9 节）。**口径变更留账：CSV 行 `证据级别` 列仍为 已核验DOI（旧值），该列不在 14 键回填范围内，未擅自改表** |
| 未取到的部分 | 论文的 Methods / 设计脚本 / 补充图全部在 Supporting Information（正文只写 "see Supporting Information"），本地未取。凡涉及计算筛选的数值参数、NCAA 力场参数、晶体学统计表，本卡一律明写"原文未给阈值（正文层面）"，不编造 |

## 1. 这篇到底解决什么（大白话）

已有的天然/ redesign 荧光蛋白在近红外（800–1000 nm）和短波红外（SWIR，1000–2000 nm）窗口里要么没有、要么太暗，而深组织成像恰恰需要这个窗口（散射与自发荧光低）。这篇的做法是把两条路拼起来：**有机化学家合成出"结合蛋白并被质子化后才发光"的聚甲炔染料（MeroCy7/MeroCy9）**，**计算设计者从头造出带中央孔道、孔内预埋一枚赖氨酸的螺旋束蛋白**，让染料与赖氨酸自发形成希夫碱共价键、质子化后被"点亮"。交付物：远红的 MC7BP34（激发 663 / 发射 685 nm）与近红外-SWIR 的 MC9BP81（激发 892 nm，发射主峰 920 nm、次峰延伸到 1100 nm 以上），后者在活体（包珠植入小鼠）里比对照 iRFP720 看得清。对我们的意义不在荧光，而在它是总表里"末端小分母高比例"（10/12=83%）的**口径对照样本**。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **配体柔性与蛋白侧链"共采样"是小分子结合蛋白设计的公认瓶颈**。作者原句："efficiently co-sampling ligand conformations alongside protein side chains within the binding pocket remains a key challenge"。→ **他们做了什么**：绕开常规对接，"Instead, we explicitly modeled the Schiff base between the merocyanine retinals and lysine residues, treating the combination as an unnatural amino acid within the Rosetta noncanonical amino acid (NCAA) framework"，于是"This allowed us to use the Rosetta machinery to simultaneously pack the ligand and the surrounding protein residues, eliminating the need for global docking."（图注同口径："To enable simultaneous sampling of the ligand conformation and design of the amino acid identities of the surrounding pocket, we treat the merocyanine retinal-lysine conjugates as NCAAs in Rosetta and allow them to sample a wide range of rotameric states."）。→ **应对后仍留下的代价**：NCAA 的建模参数与采样设置全在 SI，正文层面无法复算；且设计判据只有两个名字（形状互补 + 界面面积），正文没给任何数值阈值。
2. **六聚体连成单链后初始设计全部聚沉**。原句："Initial designs aggregated, which we hypothesized resulted from the sequence repetition arising from bridging the hexameric protein into a single chain"（他们给出的机理假设：重复序列导致链内/链间多种可竞争的重复相互作用）。→ **他们做了什么**："To solve this problem, we redesigned the entire protein breaking the repetitive sequence pattern"，并追加 Rosetta HBNet 搜氢键网络稳定目标折叠态、在分子周围放谷氨酸/天冬氨酸促希夫碱质子化（"We also positioned glutamate and aspartate residues around the small molecule to facilitate protonation of the Schiff base."）。→ **代价**：这一支 12 条下单只有 2 条结合染料——"Of 12 such designs, absorption spectroscopy indicated that two bound the dye."，还要再做第二轮核心重设计才出 MC9BP72。
3. **计算设计只能保证"结合"，不能保证"点亮"**。荧光激活依赖希夫碱氮的质子化，而质子化取决于蛋白微环境——正文里这一步不是设计出来的，是**试验出来的**："We found that two designed glutamate substitutions of RET2 (resulting in design RET2_EE) led to MeroCy7 fluorescence activation within the far-red region"，随后"we conducted site-saturation mutagenesis (SSM) focusing on residues near the fluorophore, integrated the fluorescence-enhancing mutations identified from the SSM library screening, and redesigned the loops and positions distal to the dye binding site to optimize yield"。→ **代价**：功能跃迁（暗→亮）发生在湿实验迭代环节，计算漏斗没有覆盖"光物理激活"这一层。
4. **共价结合的直接结构证据拿不到**。MC7BP34 晶体分辨率不足以看到染料："Due to the low resolution, the dye molecule is not discernible in the crystal structure."→ **他们做了什么**：改用间接三重证据链——分子量证据"Intact protein Electrospray Ionization Mass Spectrometry (ESI-MS) of MC7BP34 labeled with MeroCy7 revealed a 262 Da mass increase, consistent with covalent attachment of the dye to the protein"、敲除突变证据"Fluorescence was completely abolished when the active lysine residue was mutated to arginine"（图注："The absorption peak shifts from 505 nm for the unbound dye to 655 nm for the protein-dye complex; the knockout mutant K57R does not induce a shift in the absorption spectra, suggesting that the dye molecule binds specifically to the lysine residue as designed."）、以及蓝色晶体的颜色证据。→ **代价**：染料在口袋里的实际构象与质子化环境始终没有被直接观测。
5. **两项作者自述"本文未解决"的遗留**：SWIR 亮度不如临床染料 ICG——"The brightness of our designed NIR protein in the SWIR range is still not on par with that of ICG"；游离染料水相不稳定——"While the protein-bound MeroCy9 dye is stable, the unbound dye gradually loses color in aqueous environments, which limits the broad applications of our designed proteins"。作者给出的出路（定向进化、染料化学改造、可逆醛保护）在本文中没有执行。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **计算侧**：参数化螺旋束骨干设计（parametric design）；RosettaDesign 序列优化；**把"染料-赖氨酸共轭物"当成非天然氨基酸（NCAA）进 Rosetta 与口袋残基共采样**（替代全局对接）；Rosetta HBNet（氢键网络）；AlphaFold **仅做事后结构对照**（正文与图注里没有把 AF 置信度当筛选闸口的句子）。
- **化学侧**：MeroCy7/MeroCy9 芪三酚聚甲炔染料有机合成（MeroCy9 经串联 Suzuki 反应，路线在 SI）。
- **实验侧**：E. coli 表达 + 镍柱/SEC 纯化 + 圆二色谱 + X 射线晶体学；UV-vis 吸收与荧光光谱（结合判据 = 吸收峰红移；激活判据 = 出现长波发射）；积分球量子产率；完整蛋白 ESI-MS；定点突变（K→R 敲除）；SSM 突变库筛选；活细胞成像（U2OS/HEK293T/K562）与小鼠 SWIR 活体成像（alginate 包珠腹腔植入）。
- **正文没有的方法**：分子动力学、量子化学/光物理计算在**本地正文与图注里零提及**（`sources/claim-90pct.md` 记录的"MD + QM 处理光物理"应出未取到的 SI，见第 7 节口径账）。

### 工作流（正文自述顺序）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 骨干验证 | 参数化设计的两环螺旋束（五聚体 WSHC5、六聚体 WSHC6）中央孔道适合拉长形分子 | E. coli 表达、镍柱 + SEC 纯化、圆二色谱、X 射线晶体结构与设计模型叠合 | 判据 = 可溶表达 + 预期 α 螺旋 CD + 晶体与设计模型吻合（正文给 Cα RMSD 0.86 Å 与 0.89 Å，为描述值而非筛选门槛；WSHC5 热稳定性到 95 °C） | 2 个验证过的对称孔道骨干（PDB 8U5W；WSHC6 用已发表的 6TJ1） |
| S2 视网膜醛支路（先打通管线） | WSHC5 骨干 + all-trans retinal | 短环把五个亚基连成单链（打破对称性，因染料无循环对称）；retinal-lysine 共轭物按 NCAA 进 Rosetta，RosettaDesign 优化口袋；再做 in silico 选择 | 计算选择判据只有两个名字：形状互补 + 界面面积（"After in silico selection based on the shape complementarity and the interface area between all-trans retinal and the designed binding proteins"）；**原文未给数值阈值** | 12 条设计合成基因下单 |
| S3 第一批湿实验 | 12 条下单设计 | E. coli 表达 + UV-vis 吸收谱验 dye 结合 | 成功判据 = **表达且结合视网膜醛**（双条件，不含发光） | "we obtained synthetic genes for 12 designs, out of which 10 exhibited successful expression in E. coli and bound retinal"（10/12；本卡推算 83%，作者称高成功率）；取表达最高、聚集最少的 RET2 进下一步 |
| S4 远红激活 | RET2 + MeroCy7 | 按设计模型改造希夫碱与芳环邻位残基促质子化 → RET2_EE 出远红激活 → 荧光团近旁 SSM + 远端/环区重设计提产量 | 判据 = 出现远红荧光；优化后 MC7BP34 结合 MeroCy7 时激发峰 663 nm、发射 685 nm；混合后约 30 min 达激活平台 | MC7BP34：量子产率 0.44、摩尔消光系数 150,000（原文上标单位，本卡不引原文写法），作者称亮度超过 FPbase 收录的全部荧光蛋白；PDB 8U1A |
| S5 SWIR 支路 | WSHC6 骨干 + MeroCy9 | 单链化 + NCAA（只允许孔道朝内位置）+ Glu/Asp 布置；初始设计聚沉 → 整蛋白重设计打破重复序列 + HBNet | 结合判据 = 吸收谱显示染料结合；**原文未给计算阈值** | 12 条下单 → 2 条结合染料（"Of 12 such designs, absorption spectroscopy indicated that two bound the dye."） |
| S6 第二轮优化 | 最有希望的 2 条之一 | 围绕核心重设计提升结合与消光系数 → MC9BP72；再突掉口袋入口 4 个 Ser/Thr（去翻译后修饰位点）→ MC9BP81 | 判据 = 吸收/发射读数与 ESI-MS 共价证据；AlphaFold 模型与设计模型对照（图注值 Cα RMSD 1.41 Å，非筛选门槛） | MC9BP72：吸收 904 nm（较游离染料红移近 300 nm）、785 nm 激发下 SWIR 发射 920 nm（比 ICG 的 810 nm 红移超 100 nm）、次峰 1050 nm 延伸过 1100 nm；MC9BP81：激发 892 nm |
| S7 细胞与活体定标 | MC9BP81-EGFP-EGFRc / EGFRn 融合蛋白 | 与 MeroCy9 预孵育上色后标记 K562（EGFR 阳性 / 阴性对照）；900 nm 长通滤片采集；包珠（细胞浓度约每微升 5000 个、每颗直径约 600 微米的珠约 565 个细胞）腹腔植入小鼠，与 iRFP720（激发 672 nm）对照 | 判据 = 阳性细胞有信号而阴性无信号；活体上能否分辨珠子 | "In contrast, the MC9BP81-EGFP-EGFRc-MeroCy9 signal allowed clear identification of the beads, likely due to reduced tissue autofluorescence at longer wavelengths."（iRFP720 对照信号不足以分辨珠子） |

**流程骨架一句话**：对称孔道骨干先湿验证 → 染料-赖氨酸共轭物当 NCAA 一次设计到口袋 → 小批量（12 条）下单快速回环 → "结合"与"点亮"分两级判据、点亮靠实验迭代（定点双突变 + SSM）→ 聚沉就整蛋白重设计。计算漏斗末端送测数就是两位数。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（正文位置） |
|---|---|---|
| 12 → 10 | 视网膜醛支路：in silico 选择后下单 12 条 → 表达且结合 10 条 | Results 第一段（引句见 §2.3 与 CSV 回填 hit_rate）；83% 为本卡推算，原文只有"This high success rate" |
| 12 → 2 | MeroCy9 支路：12 条下单 → 吸收谱显示 2 条结合染料 | "Of 12 such designs, absorption spectroscopy indicated that two bound the dye." |
| 0.86 / 0.89 / 1.41 Å | 晶体 vs 设计模型（WSHC5/WSHC6）、AlphaFold vs 设计模型（MC9BP72）的 Cα RMSD | Results 首段、图 2a、图 3b 图注（本卡不以引句形式引用，含 Å） |
| 505 → 655 nm | MeroCy7 游离态 vs 与 MC7BP34 复合物（K57R 突变体不移位） | 图 2d 图注引句 |
| 663 / 685 nm | MC7BP34-MeroCy7 激发/发射峰 | §2.3 引句（excitation maximum at 663 nm，emission at 685 nm） |
| 0.44 | MC7BP34 量子产率（积分球实测；对照 Cy5 0.28、Alexa647 0.33 为文献值） | 引句见 §2；对照值在括注内 |
| 150,000 | MC7BP34 摩尔消光系数（原文带上标单位，本卡不引原文写法） | Results 中段 |
| 262 Da | ESI-MS 检出 MeroCy7 共价偶联的质量增量 | 引句见 §2.4 |
| ~30 min | MeroCy7 与 MC7BP34 混合后荧光激活达平台 | 正文含 "~30 min"（上标符号不入引句） |
| 904 nm / 近 300 nm | MC9BP72-MeroCy9 吸收峰 / 相对游离染料的红移量 | 引句与图 3d 图注 |
| 785 / 920 / 1050 / 1100 nm | MC9BP72 复合物激发 / SWIR 主发射 / 次峰 / 次峰延伸边界 | 引句见 §2；图 3e |
| 810 nm / 672 nm / 892 nm | ICG 发射（对照）/ iRFP720 激发（对照）/ MC9BP81 激发 | 摘要与正文对照句 |
| 900 nm 长通 | 活体/细胞 SWIR 采集滤片 | 图 4 图注与正文 |
| 约 5000 细胞/微升；约 565 细胞/珠（直径约 600 微米） | 活体植入实验的包珠浓度（原文单位含 µ，本卡转述） | Results 活体段 |
| 95 °C | WSHC5 圆二色谱热变性稳定上限 | Results 首段 |
| PDB 8U5W / 8U1A / 6TJ1 | WSHC5 / MC7BP34 / WSHC6 结构登记号 | 正文与数据可用性声明 |

## 5. 结论——作者说了什么

1. 计算蛋白设计 + 有机合成结合，可以从头做出跨长波段的荧光激活蛋白："we sought to develop a general approach integrating computational protein design with organic synthesis for creating long-wavelength fluorescence-activating proteins from scratch"。
2. 视网膜醛支路的首批 12 条设计里 10 条"表达且结合"，作者把高成功率归因于底物化学而非筛选算法："This high success rate likely reflects the hydrophobic nature of the merocyanine retinal"（类疏水口袋与疏水配体的天然匹配）。
3. MC7BP34 的亮度超过 FPbase 收录的全部同类波长荧光蛋白（"is brighter than all the fluorescent proteins documented in FPbase"），且与 HaloTag/SNAP-tag 正交（"No cross-reactivity was detected, indicating that MC7BP34 provides an additional orthogonal channel for multicolor imaging."）；作者把高亮度归因于口袋对染剂的屏蔽与构象限制："The high brightness likely arises from a compact, well-designed dye-binding pocket within the protein that shields the dye from solvent and restricts its conformational flexibility"。
4. MC9BP81 活体 SWIR 成像优于 iRFP720 对照，机理是长波自发荧光低："In contrast, the MC9BP81-EGFP-EGFRc-MeroCy9 signal allowed clear identification of the beads, likely due to reduced tissue autofluorescence at longer wavelengths."
5. 作者自报的两处不如人意：SWIR 亮度仍不及 ICG（引句见 §2.5）；游离 MeroCy9 水相褪色限制应用（同 §2.5）。改进路线（定向进化、染料改造、跨膜化做电信号传感器）是展望，不是本文交付。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **10/12 是"三级漏斗末端"的数字**：设计生成数（未报）→ in silico 选择（判据无名无阈值）→ 下单 12 → 湿实验 10。任何把 83% 说成"设计成功率"的转述都偷掉了前两级。这正是本行进总表的原因。
2. **他们的两级判据分离得很干净**：第一级只看"表达 + 结合"（UV-vis 位移），第二级才看"发光激活"（光谱）。结合是几何/疏水问题（可设计），激活是质子化微环境问题（本文靠突变库碰）。→ 对应我们：酶设计筛选里"结合底物"与"催化转化"也必须分成两级闸口，混在一起报数会重演本文的口径歧义。
3. **"整批失败→机理假设→结构性重做"的应对模式值得记**：聚沉不是靠调阈值救回来的，是靠改掉失败的构造本身（打破序列重复）——失败归因到设计策略层而不是参数层。
4. **间接证据链可以补足拿不到的直接证据**（ESI-MS 质量增量 + K→R 敲除 + 颜色/光谱位移三角互证）。我们在产物化学受限时可仿照这种"多正交读数列联"的证法。
5. 正文没给计算筛选的任何数值阈值这一事实本身说明：**这篇论文的可复现重心在 SI**，正文只是叙事；引用它做"漏斗参数依据"时只能引方法结构，不能引数字（数字不在正文里）。

## 7. 局限与失败（作者的 + 我们读出的 + 与登记记录的口径账）

**作者的局限**：见 §5.5 与 §2.4–2.5（亮度不及 ICG、染料水相不稳定、晶体看不到染料、"点亮"靠实验迭代）。

**我们读出的局限**：① 12 条/2 条的两个分母都极小，10/12 与 2/12 之间的巨大差（同一套管线、不同染料）说明该比例对化学底物高度敏感，不能外推；② in silico 选择只给了判据名字没有阈值，"漏斗收缩了多少"在正文层面不可核算；③ 全文没有 MD/QM/自由能字样的计算，机理层（质子化如何被微环境调控）只有事后归因。

**与 `sources/claim-90pct.md` / CSV 既有记录的口径账（以全文为准）**：
- CSV `计算筛选判据` 列写"生色团预组织筛选：MD + QM 处理光物理；AF 类置信度 + 能量项"——本地全文正文与图注**零次**提及 MD/QM，AlphaFold 只出现在事后对照（图 3b），未见"AF 置信度当筛选闸口"的句子。该记录应出未取到的 SI 或转述加工，本卡回填按正文实写（md_used/qm_used 记 未记录）。
- CSV `阈值数字` 列现为"未记录"——与正文一致（正文确实没给数值阈值），无需更正。
- CSV `候选数递减` 列"12 个下单 → 10 个成功"——属实但只是**视网膜醛支路**；同文 MeroCy9 支路是 12 → 2。引用时漏掉后者会系统性高估这条管线的普适命中率。
- `证据级别` 列现值"已核验DOI"为旧口径；本卡按全文级写（§0 已留账），该列不在 14 键回填范围，未改表。
- `sources/claim-90pct.md` 第 110 行对本行的使用（作为"表达率≠设计成功率"的对照案例）与全文一致，无误记。

## 8. 迁移判断：哪些能搬、哪些不能搬

**这一行的特殊风险（总表口径对照组的职责）**：表里收它就是为了做口径对照——凡"命中率/成功率"必须区分是**靶点级战役读数**（该靶出了至少一个可用分子）还是**候选级比例**（下单 N 条里中 M 条），并且分母处于漏斗哪一级要写死。本行的 83% 是"候选级、末端分母（12）、双条件判据（表达且结合）"。

**可迁移（只迁移方法层）**

1. **"计算漏斗 + 少量送测"这一层组织方式**：先用已验证的结构骨干把风险剥离（折叠/表达问题先解决），功能设计只在一个干净底座上做一次；末端送测两位数规模、两轮下单快速回环。→ 我们的候选分级提交可仿照。
2. **两级判据分离**：先"结合在不在"，后"功能亮不亮"，各级用各自的正交读数（UV-vis 位移 vs 荧光发射；对我们：底物占据口袋 vs 产物化学确认），不许合并报一个笼统"成功率"。
3. **把配体-催化残基共价复合物整体当 NCAA 参与设计**这一思路，对应我们"把反应中间体（中间体等）而不是游离底物放进口袋设计"的可能性——是方法启发，不是现成参数。
4. **失败的结构性重做**（§6.3）与**间接证据三角互证**（§6.4）。

**不可迁移（为什么不能照搬）**

1. **不许把 10/12（83%）迁移成酶设计的成功概率**。它的分母是 in silico 选择后的下单数，生成端规模未知；判据是结合一个疏水分子，无化学转化；我们的任务要判三步化学事件与副反应竞争，二者不同构。
2. **不许把光谱激活判据（吸收红移、量子产率、亮度、900 nm 长通信号）当作酶活判据**。荧光蛋白的"成功"是物理发光，酶设计的"成功"是催化产物身份；本文没有任何催化读数可借。
3. 本文正文**不含 MD/QM 命中率数据**，不能给"用 MD/QM 判催化"提供任何概率背书（claim-90pct 里那句 MD+QM 记录未经正文核验，见 §7）。
4. 希夫碱形成是自发化学，蛋白只提供口袋与质子化环境；不存在"设计催化步骤"的成功率可引。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/nirFAP2026.txt

- 本地全文为 PMC13560888 接收稿纯文本（44,480 B），身份块（DOI/PMCID/卷页）在文件头 1500 字符内已逐字段核验与本 CSV 行一致后才开写。
- 登记的另一底稿 `data/interim/claim_lit/PMC13560888.xml` 为 XML（门禁按规则跳过），`sources/claim-90pct.md` 为记录底稿；本卡全部引句只声明对照 nirFAP2026.txt。
- 对照底稿行号：`sources/claim-90pct.md:110`（本行进表原因）；CSV 行 M-K34（口径对照与独立复核组）。
- 含非 ASCII 字符（Å、°、µ、α、上标、en-dash）的原句一律不放入英文引号，数值以中文叙述转写（如"近 300 nm 红移""约 5000 细胞/微升"）；跨引文编号（如 "framework. 36 , 37"、"Rosetta HBNet 40"、"FPbase 24"）的句子在编号处截断成两条或止于编号前。
- CSV 字段映射：第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`；第 0 节口径账 ↔ `证据级别`（该列不在回填范围，仅留账）。
- **本卡自检**：`scripts/verify_literature_cards.py --only M-K34 --no-report`，全部引句在该底稿逐字命中后方可交回。

<!--CSV回填
work_type=论文
target=merocyanine 合成染料（MeroCy7/MeroCy9）与 all-trans retinal 的结合/荧光激活蛋白（远红—近红外—SWIR 探针；retinal 结合蛋白即 FAFPR 类）
backbone_generation=参数化双环螺旋束寡聚体（五聚体 WSHC5/六聚体 WSHC6）短环连成单链 + RosettaDesign 口袋序列优化；MeroCy9 支路聚沉后整蛋白重设计打破序列重复并加 Rosetta HBNet 氢键网络
computational_filters=retinal-lysine（染料-赖氨酸希夫碱）共轭物作为 NCAA 进 Rosetta 与口袋残基共采样以替代全局对接；in silico 选择按形状互补 + 界面面积两判据（正文未给数值阈值）；AlphaFold 仅事后结构对照，未见 AF 置信度作闸口
thresholds=正文未给计算筛选数值阈值（只有判据名：shape complementarity、interface area）；0.86/0.89/1.41 Å 为晶体或预测模型对设计模型的描述性 Cα RMSD，非筛选门槛
md_used=否（本地全文正文与图注未出现分子动力学；claim-90pct 所记 MD 说法未能从正文核验，或出未取到的 SI）
qm_used=否（同上，正文无量子化学/光物理计算字样）
experimental_methods=E. coli 表达+镍柱/SEC 纯化+圆二色谱+X 射线晶体学；UV-vis 吸收与荧光光谱；积分球量子产率；完整蛋白 ESI-MS；K→R 定点敲除；SSM 突变库；活细胞成像（U2OS/HEK293T/K562）；alginate 包珠小鼠腹腔植入 SWIR 活体成像（对照 iRFP720）
pipeline_counts=骨干 2 个验证（WSHC5/WSHC6）；retinal 支路：设计→in silico 选择（规模未报）→12 条下单→10 条表达且结合；MC7 支路：RET2→RET2_EE→SSM+重设计→MC7BP34；MC9 支路：12 条下单→2 条结合染料→二轮核心重设计→MC9BP72→突变 4 个 Ser/Thr→MC9BP81
hit_rate=10/12（83%，本卡推算；作者原文只有"This high success rate"）=候选级末端比例，分母为合成下单数，判据为表达且结合双条件，不含发光；同管线 MC9 支路仅 2/12；不许迁移为目标酶成功概率
best_metric=MC7BP34：激发 663 nm/发射 685 nm，量子产率 0.44，摩尔消光系数 150,000（原文上标单位），作者称亮度超 FPbase 全部同类荧光蛋白；MC9BP81：激发 892 nm，发射主峰 920 nm+次峰 1050 nm 延伸过 1100 nm；SWIR 亮度作者自述仍不及 ICG
cost_or_stat_note=正文无计算成本台账；实验成本规模=两轮基因下单共 24 条（12+12）；作者自报遗留：游离 MeroCy9 水相褪色、蛋白-dye 复合物在活体信号弱于理想；未记录其他成本
role_in_timeline=口径对照与独立复核组样本：给出"80-90% 末端数字"的完整拆解案例（分母层级=下单候选级、判据=表达+结合双条件、靶点级与生成端规模均不可得），用于校验讲座/新闻里"90%+"口径的转述陷阱；非 Baker binder 漏斗组成员
source_pointer=data/interim/baker_lit/ft/nirFAP2026.txt（PMC13560888 接收稿纯文本）+ sources/claim-90pct.md:110
CSV回填-->
