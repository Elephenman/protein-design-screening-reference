# 前沿方法核验清单（2025-06 → 2026-11）· 工作流模板的库外引用

模板 [protein_design_workflow_template.md](protein_design_workflow_template.md) 里所有 `[S1]`、`[S12]` 这样的编号都在本页定义。
**本页的存在理由**：152 篇精读卡的门禁只覆盖库内文献；工作流要跟上 2025–2026 的默认工具链，就必须有一条
独立、可查、带访问日期的库外引用通道，并把它的取证级别如实标出来——**不许把调研记忆写成"前沿事实"**。

- 调研与取证日期：2026-11-07（全部 URL 当日实际访问）。
- **独立复核**：2026-11-07 另派一名复核代理逐条回原文核对 6 条最高风险断言，结论文件已归档为
  `data/interim/frontier_2026_verify_2026-11-07.md`。它的四处判读已直接改写进本页与模板，原始笔记
  （含被否证的写法）保留在 `data/interim/frontier_2026_survey_2026-11-07.md`，形成"笔记—复核—采用"三段链。
- 取证级别：`FT`=读到正文/全文页 · `ABS`=仅摘要页 · `README`=官方仓库 README 或官方文档 · `2ND`=二手转引（**不得进模板**）。
- 与库内关系：`[S9]` 对应库内 [B35]（同一工作的预印本，库内是摘要级）；`[S2]` 的置信度阈值与库内 [B08] [B09] 的 pAE/pLDDT 口径同族。

| 编号 | 条目 | 一手来源 | 取证级别 | 模板里能用到哪一步 | 复核 |
|---|---|---|---|---|---|
| S0 | 六个查无一手来源的方法名（禁用） | 四路索引检索记录 | 检索级 | §F 禁用清单 | 已复现，但范围声明需收窄 |
| S1 | 官方默认链 RFD3 → MPNN/LigandMPNN → RF3；RFO 里有 Boltz-2 分支 | https://github.com/RosettaCommons/foundry（默认分支 `production`） | README | ②③④ 选型 | 部分对：默认链成立；"打分位"说法被否证 |
| S2 | RF3 技术报告（手性/步数/早停陷阱；阈值出处已纠正） | https://doi.org/10.1101/2025.08.14.670328 | FT | ④ 复折器选型 | 部分对：三阈值不是设计筛选阈值 |
| S3 | Boltz 两个亲和力输出的分工 | https://github.com/jwohlwend/boltz | README | ④ 亲和力用法 | 未单独复核（与 S6 同源交叉） |
| S4 | Boltz-2 亲和力可靠性独立评测（对照是 ESMACS 模拟自由能，不是湿实验） | https://doi.org/10.1021/acs.jctc.6c01334（arXiv `2603.05532`） | FT | ④ 禁用绝对门槛 | 部分对：500× 那条不属本篇 |
| S5 | 通用置信度在抗体–抗原近乎无效（AUC 0.5–0.6） | https://doi.org/10.64898/2026.05.13.724924 | ABS | A.2 失灵触发表 | 未单独复核 |
| S6 | Boltz-2 自报基准（FEP+ Pearson 0.66、CASP16 盲测 140 对） | https://doi.org/10.1101/2025.06.14.659707 | FT | ④ 量级参考 | 部分对：数字为真，解释见下 |
| S7 | 任务专用相互作用模型替代置信度（纳米抗体 3.3%→8.0%） | https://doi.org/10.64898/2026.06.23.733997 | ABS | A.2/A.3 路线切换 | 未单独复核 |
| S8 | Chai-2 零样本抗体设计（52 靶 × ≤20 条，15.5%）；miniprotein 是独立 5 靶面板 | https://doi.org/10.1101/2025.07.05.663018 | FT | A.1 命中率口径与 BLI 判据 | 部分对：68% 不是 52 靶子集 |
| S9 | RFdiffusion3 正式见刊（96 构型零样本拿到活性催化剂） | https://doi.org/10.1126/science.aeh2982 | ABS | B.1 零样本规模 | **CONFIRMED** |
| S10 | 有本靶标活性标签后微调亲和力头 | arXiv `2609.24302` | ABS | ⑩ 回灌升级 | 未单独复核 |
| S11 | OpenFold3 检查点互不兼容、分数不可横比 | https://github.com/aqlaboratory/confornets + https://github.com/aqlaboratory/openfold-3 | README | §I 开工登记"模型版本" | 已复核（见 S1 条内） |
| S12 | 多态酶设计：单过渡态约束被点名为缺陷 | https://doi.org/10.64898/2026.09.11.750617 | ABS | B.2 约束升级 | 未单独复核 |
| S13 | CaGE：把 RF3 再训练成设计条件网络 + 迭代衰减 | https://doi.org/10.64898/2026.10.02.756307 | FT | B.1/B.2 活性位约束 | 未单独复核 |
| S14 | MD+QM/MM 用于**解释**设计–进化差距（Kemp elimase） | https://doi.org/10.64898/2026.09.09.750330 | ABS | B.2 MD 的位置 | 未单独复核 |
| S15 | 设计与进化的稳定性/动力学互作（负面：初版只考虑过渡态） | https://doi.org/10.64898/2026.05.29.728685 | ABS | B.2 负面判据 | 未单独复核 |
| S16 | Metal Mer：无定向进化的金属酶选择性（ee > 99%，13 底物） | https://doi.org/10.64898/2026.10.13.758590 | ABS | B.5 三态收口 | 未单独复核 |
| S17 | AlphaProtein Novo：同骨架序列系综是主判据（DEHPase 新骨架 11%） | https://doi.org/10.64898/2026.10.01.756017 | FT | B.2 闸口设计 | 未单独复核 |
| S18 | 蛋白–肽复合物：AF2 优于 OF3，且 DockQ 阈值不可从蛋白–蛋白搬来 | https://doi.org/10.64898/2026.04.21.720042 | ABS | C.1 判据边界 | 未单独复核 |
| S19 | OpenBind：早期实验结构微调共折叠模型改善位姿与虚拟筛选 | https://doi.org/10.64898/2026.08.27.747600 | ABS | B.3/H 微调路径 | 未单独复核 |
| S20 | 药化真实项目里 ML 亲和力看不见跨系列 500× 提升（Boltz-2 池化 ρ 0.31 vs FEP+ 0.70） | https://doi.org/10.1002/cmdc.70531（PMID 42894262 / PMC13677808） | FT | ④ 禁用绝对门槛（湿实验对照） | 复核时新定位的一手来源 |
| S21 | **RFD4-Proteina**：序列–结构联合共设计、partial diffusion、reward-guided search；权重配对与硬件门槛 | https://github.com/RosettaCommons/RFD4-Proteina + https://huggingface.co/nvidia/RFD4-Proteina | README | ②③④ 选型、§F 默认链、迭代精修 | 本轮新增，两份官方 README 当日取回并逐字引用 |
| S22 | RFD4-Proteina 预印本正文（*Biomolecular design through latent reasoning with RFD4-Proteina*） | https://rfd4-proteina.org/assets/paper/RFD4-Proteina.pdf | FT | ②③④ 与迭代协议的实验口径 | 全文已本地归档；引句逐字核验 127/127（抽取代理）+ 主会话另抽查 18 条；**未派第二独立复核代理** |

## 逐条要点（含分母与局限）

### S1 Foundry = 官方默认链（复核后收窄了说法）
`pip install "rc-foundry[all]"` → `foundry install base-models`（一次装最新 RFD3 + RF3 + MPNN），官方镜像
`rosettacommons/foundry`；Colab 教程标题即"a basic design pipeline with **RFD3, MPNN, and RF3**"。
**能证明**：官方对外教的默认三件套是 RFD3 → MPNN → RF3（README 首行声明三类模型 + Colab 教程标题）。
**复核否证的一条（不许再抄）**：原先写的"Boltz-2 已接入打分/筛选位"不成立。RFO 的 README 把 Boltz-2 写成
每个循环按 `backprop_fraction` 概率切换的**结构预测分支**，且原话 **"it does not rank the samples"**、
"Independent AlphaFold3 filtering is outside this pipeline"。所以模板里只能说"官方 RFO 在优化循环里用了
Boltz-2 做结构预测分支"，不能说它当筛子。
取 README 必须走默认分支 `production`（`main` 分支 404）。许可事实（复核补充）：Foundry 与 AtomWorks 的
`LICENSE.md` 均写 "BSD 3-Clause License … covers both the source code and model weights"。
**尚缺**：一份同口径湿实验命中率对比（RFD3+MPNN+RF3 vs RFdiffusion1+MPNN+AF2）。

### S2 RF3（原子级复折与置信度）
三个检查点：Latest(01/24)、Preprint(01/24)、Benchmark(09/21 训练截断，用于同截断对比)。
自报（`FT`，分母=自建非冗余测试集，按 40% 序列同一性/CCD 聚类，全部 in silico）：手性中心正确率
**RF3 88% / AF3 84% / Boltz-2 76%**（不加推理引导）；`num_steps` 200→50 精度不降、速度 >2×；
开 `early_stopping_plddt_threshold`（默认 0.5）后产出提升 **10–20×**。
**复核改掉的一条硬错**：`pDE ≤ ln(0.075·length)` + `pLDDT ≥ 0.62` + `pAE ≤ 15` 这三个数**不是设计筛选阈值**，
它们出现在补充材料 **§A.2.2「RNA 蒸馏集构造」**里，用途是过滤预测结构以构造训练数据；全文 `pDE` 只在该段出现，
且 rf3/rfd3/rfo/主 README 四个文件里 grep `0.075`、`0.62`、`pDE` 全部 0 命中。数字本身逐字为真，
但**不许当成"RF3 自带的默认筛子"抄进方案**。正文里可安全引用的是同篇的复折口径
`mean pLDDT > 80` + `mean interface PAE < 10`（蛋白–DNA 那组）。
**两个必须写进方案的坑**：无 MSA 时模型早停（只出 `.score` 不出结构文件）→ 批量筛除要把 `early_stopped` 单列，
"没结构"≠"结构差"；自定义配体与 CCD 同名会"catastrophically wrong"，需加 `L:` 前缀。
**尚缺**：这些阈值在他人体上的 ROC（作者未给留出集），因此模板只把它们列为"候选默认值"，进 §H 重标。

### S3 + S4 + S6 + S20 亲和力头：能做什么、不能做什么
分工（官方 README）：`affinity_probability_binary` 管 hit discovery 的二分；`affinity_pred_value` = log10(IC50, µM)
管系列内排序；两者训练数据与监督不同，不可混用。自报基准（S6 `FT`）：FEP+ 四靶平均 Pearson **0.66**、算力快 >1000×；
CASP16 亲和力 track 140 对/2 靶盲测"clear margin"超过全部提交方；Recursion 8 个内部盲测 assay 中 **3/8 Pearson > 0.55**、其余有限。
独立评测（S4 `FT`，16,780/21,702 化合物）：整体 r=0.45/ρ=0.46（TNKS2）、r=0.24/ρ=0.25（3CLPro），
**top-100 集合内相关≈0**，几乎全部预测 < −4 kcal/mol（压缩），作者结论明确"不存在可迁移的通用阈值"。
**复核纠正的两点归属**：①S4 的对照是 **ESMACS 模拟自由能**，不是湿实验活性——所以它是"对一个物理计算"的一致性检验；
②"跨系列 500× 提升看不见"那条**不属于** S4，也**不属于** arXiv `2512.06592`，一手来源是复核时新定位的
**S20 ChemMedChem `10.1002/cmdc.70531`**（PMID 42894262 / PMC13677808）：15-PGDH 四个真实化合物系列，
系列 3（探索新亚口袋）里 Boltz-2 **未预测出任何成员优于母体**，而实验活性提升达 **500×**；
池化相关 **Boltz-2 ρ=0.31 vs FEP+ 0.70**（p_adj<0.05）、系统性系列间偏差（Simpson 悖论式），Vina 在多数系列反而更好。
这是三条负面里**唯一以真实实验活性为对照**的一条，权重最高。
→ 模板用法：只做系列内排序与二分提示；**禁止**设绝对门槛、禁止报"预测 K_D"；池子小于 ~100 时相关性会退化；
   一旦某系列开始探索新亚口袋，ML 亲和力分数**默认不可信**（[S20]）。

### S0 禁用清单（查无一手来源，且范围已收窄）
`RFSolo`、`DockDesign`、`MolGen`（作为蛋白设计方法）、`IG-LLM`、`LockMSF`、`PoseChains` 六个名称，
2026-11-07 在 EPMC（TITLE/ABSTRACT）、arXiv、Crossref、GitHub 四路检索均无一手论文/一手仓库。
复核代理独立重跑了 RFSolo / DockDesign / LockMSF 三个名，四路同样 0 命中，结论可复现。
**复核判定的措辞边界**：原始笔记写过"不存在该用途的方法"和"四个来源全部返回 0 条"，两处都不合格——
前者是无范围限定的全称否定，后与笔记自己的表格矛盾（DockDesign 有一个无关的个人仓库、IG-LLM 有 arXiv 近名命中）。
模板与本页一律采用**带范围的表述**："截至 2026-11-07，在上述四个索引未检得一手来源；
未覆盖专利库、Google Scholar 与闭源公司内部代号。" 因此**模板里禁止出现这六个名字，也禁止写成"这些方法不存在"**。

### S5 + S7 抗体–抗原：通用置信度失灵，任务专用模型可用
S5（`ABS`，519 条治疗性 mAb × 同源/随机非同源抗原）：Boltz-2 各类置信度 ROC-AUC 仅 **0.5–0.6**，
多特征/多变量建模"little to no improvement"，采样 ~15–20 seed 后收益递减。
S7（`ABS`，10 个新靶点）：用相互作用模型（BoltzPPI 类）替代结构置信度排序，纳米抗体命中率 **3.3% → 8.0%**；
可开发性五项全过 58%（对照 BoltzGen 40%、临床期 VHH 21%）。
→ 模板用法：抗体分支默认走"任务专用模型排序 + 展示库"，不走通用 ipTM 淘汰（与库内 [B22] 的 0%–2% 一致）。

### S8 Chai-2：本清单里分母最干净的一组
`FT`：**52 个新抗原**（PDB 中原无抗体/纳米抗体结合剂），每靶 **≤20 条**设计；平均实验命中率 **15.5%**
（VHH 20.0%、scFv 13.7%），**26/52 靶**至少 1 条确认结合剂；作者称此前 de novo 抗体设计的实验室成功率通常 <0.1%。
命中判据（可抄）：BLI 信号 **> 背景 + 0.1 nm 且 > 背景的 300%**。
**miniprotein 是另一个面板，不是 52 靶的子集**（复核纠正）：独立 5 个靶点
（PD-L1 25 条、IL-7Rα 23、InsulinR 20、TNFα 22、PDGFRβ 21，每靶另跑原型模型 Chai-1d 20 条），
湿实验成功率 **68%**，PD-L1/IL-7Rα/PDGFRβ/InsulinR 达皮摩尔级。**把 68% 说成 52 靶里的子集会让读者算错总分母。**
表位到湿实验确认 **< 2 周**（E. coli 无细胞表达）。
局限（作者原述）：数据全部在 scFv/VHH 格式取得，不保证平移到 Fab/全长 IgG；表位归属需竞争结合 + 结构确认；
交叉反应性不因"打同一表位"自动获得。**Chai-1/Chai-2 均无亲和力头**，不许把 Boltz-2 的用法套到 Chai 上。

### S9 + S13 + S12 + S17 酶设计四条
- **S9**（`ABS`，Science 订阅墙，正文未取）：全原子功能位点支架（RFD3），磷酸三酯酶与 TTR 锌蛋白酶两个体系
  "in both cases we obtain active catalysts in zero shot 96 construct design campaigns"。库内 [B35] 是同一工作的预印本
  （摘要级），应把该行的 `文献类型/核验状态` 视为"已见刊、正文仍未取得"。
- **S13**（`FT`）：把 RF3 训练成可接受 5 类设计条件（界面热点、相对可及度、氢键供受体身份、界面类型、原子对距离），
  用 classifier-free guidance 多轮**衰减**约束，交替"约束引导结构预测 → LigandMPNN 重设计"。实测：非血红素铁设计 A11
  产物信号高于背景且 **56% ee**（配位点突变对照为外消旋）；PLP retro-aldolase CaGE-RA1.0 **2.7 Å** 晶体、骨架
  **r.m.s.d. 0.702 Å**、按设计为单体、质谱 +231 Da 与 Schiff 碱一致。作者也点明：复杂约束下"内部一致的设计占比可低到
  计算不可负担"——即**单轮生成 + 置信度筛选在复杂活性位会失败**。
- **S12**（`ABS`）：多态（沿整条反应坐标）约束设计 Morita–Baylis–Hillman 酶，最佳变体双底物效率比单态设计高 **>100×**，
  并在效率与对映选择性上超过一条经大量定向进化的天然/进化酶；负面判据可写："单态优化可能人为制造动力学瓶颈"。
- **S17**（`FT`）：AlphaProtein Novo，DEHP 降解首轮 81 条中 4 条高于背景 3 SD，两轮后**新骨架 hit rate 11%、
  回收骨架 39%**（命中定义 = 活性 ≥ 对照天然酶 QHH21706.1 的 2%）；作者明示主判据是
  "evaluates ensembles of sequences derived from the same backbone"，并声明**各反应 hit rate 定义不同、不许跨反应比较**。
  同一篇里还给了对照口径：筛 65 个天然酯酶只找到 1 条有活性 DEHPase。

### S14 + S15 + S16 机理层（MD/QM 放在这里，不放在漏斗里）
- **S14**（`ABS`）：de novo Kemp elimase 设计版 vs 进化版，大规模 MD + QM/MM 反应势垒；结论是势垒与质子转移反应能强相关，
  进化让基态系综富集"反应性构象"，并出现负活化热容。→ **MD 的位置=解释设计–进化差距**，不是当筛子（补库内 [K27] 缺口旁的正面材料）。
- **S15**（`ABS`）：两轮定向进化到高催化效率；最有价值的负面发现"the initial design considered only the transition state
  but not substrate binding, leading to a dynamic Michaelis complex"。
- **S16**（`ABS`，正文未取）：锌依赖氢转移酶最佳变体在 13 个底物上 **ee > 99% 且不经定向进化**；甾体底物区域/非对映选择性 > 19:1；
  铁催化烯烃双官能化 10% 收率、70:30 e.r.。**命中率总分母未给** → 只能引选择性数字，不能引成功率。

### S11 + S18 + S19 版本与迁移边界
- **S11**：OF3p1(`of3_ft3_v1.pt`) 与 OF3p2(`of3-p2-155k.pt`) 检查点互不兼容，`openfold3==0.3.1` 才能复现某篇数值；
  `>=0.5.0` 默认参数换成 OpenBind-0（训练截断 2025-06）。→ 模板 §I 开工登记要求写死"模型版本 + 训练截断"。
- **S18**（271 个非冗余蛋白–肽复合体，CAPRI 判据，分 IDR/Non-IDR）：整体成功率 AF2 一致优于 OF3；AF2 在其训练集已含的
  复合体上有记忆效应；OF3 的 PAE 分布削弱了派生分数判别力；**蛋白–蛋白的 DockQ 阈值不能直接搬到蛋白–肽**。
- **S19**（肠道病毒 2A 蛋白酶，925 个晶体学结合事件/699 化合物/601 亲和力）：对接表现强依赖口袋构象、构象难排序；
  **用片段筛选阶段的晶体结构微调 OpenFold3-p2 可显著改善后续化合物位姿与虚拟筛选** → 支持"早期实验结构→本靶标微调共折叠模型"。

### S21 RFD4-Proteina：为什么它改的是工作流形状，不只是版本号

`README`（两份官方 README 于 2026-11-07 取回，本地归档
`data/interim/rfd4_2026-11-07/RFD4-Proteina_README.md` 与 `HF_RFD4-Proteina_README.md`）。
Baker Lab × NVIDIA GenAIR，BSD 3-Clause，权重发布 **2026-10-19**，
Hub revision `a06e2509c7033b010fc43614e9fd840303588502`。

**它改了什么（这决定模板 ②③ 的形状）**：model card 原句
"It generates protein sequences and all-atom structures together, conditioned on the molecular context you want to preserve"。
即**序列与全原子结构一次出**，v1 的"骨架 → MPNN 序列 → 复折"三件套里的 ③ 不再是必经步。
GitHub README 另列两条直接影响迭代的能力：
"Reward-guided search: beam search over generation paths scored by structure-prediction oracles and custom metrics."
与 "Partial diffusion to refine or diversify existing structures."
→ 前者把一部分筛选前移进生成过程，后者是**第二轮精修**的现成工具（见迭代协议 §2/§3）。

**四条必须一起抄的限制**：

1. **权重是配对的，跨版本混用不报错**。flow model 与 autoencoder 一对；当前对 latent 32 维、残基词表 147 类，
   上一对是 16 维 / 33 类。原句："mixing a flow model with a different autoencoder produces nonsense rather than an error"。
   → 模板 §H 第 5 步因此要求钉住 Hub revision，而不只是写"RFD4"。
2. **硬件门槛**。"Linux x86_64, Python 3.12, and an NVIDIA GPU with a CUDA 13-compatible driver"，
   且 "macOS and Windows are not supported."。权重 1.74 GB（FP32，435,622,465 参数），环境约 7 GB。
   峰值显存取决于 token 数/batch/recycle 深度而不是权重大小。→ 够不上就退回 RFD3 三件套 [S1]，判据不变。
3. **算力预设是 recycle 深度而不是"步数"**：60 步上按 `(steps, recycle depth)` 分带，
   low = 120 次 trunk pass、**medium（默认）= 180**、high = 300。
   → 报"每条设计多少算力"时必须同时报用的是哪一档，否则不可比。
4. **效率表不是本版本的读数**。model card 自己在表前声明：
   "These numbers were measured on the previous release pair"，
   "They have not been re-measured on the current release and should not be read as describing it."
   表后还有一句 "Computational passers do not establish experimental activity."。
   表的口径是"每 GPU-小时、每靶、结构上可区分的**计算**通过者数"（含生成与共同 AF3 评估），
   每靶 200 次原始尝试，失败尝试计入耗时，setup/编译/CPU 打分/空闲分配不计：
   蛋白 binder 24 靶 **71.60**（对照 Proteina-Complexa 13.24）、小分子 binder 77 靶 **112.25**（BoltzGen 15.48）、
   Atomic Motif Enzyme 37 靶 **91.18**（AlphaProtein-novo Codesign 26.02）、DNA binder 3 靶 **41.97**（BoltzGen fixed DNA 9.46）。
   作者同时声明各法条件化方式不同（PPI 用骨架条件 vs 多个基线用全原子条件；DNA 只有 3 个靶）。
   → **这张表只能当"上一版权重的计算产能量级"，不许当本版本产能规划依据，更不许当湿实验命中率。**

**尚缺**：RFD4 自己的**设计筛选数值阈值**（可直接抄的 pAE/ipTM 切点与通过率）在两份 README 里没有给；
想要开箱阈值仍须走模板 §H 在自己体系标定。预印本正文的核对见 S22。

### S22 RFD4-Proteina 预印本正文

`FT`：*Biomolecular design through latent reasoning with RFD4-Proteina*，Corley / Didi / Kazman / Brent 等，
Baker Lab × NVIDIA GenAIR，2026，预印本（PAGE 1 自标 "This preprint has not been peer reviewed."；
GitHub README 的 citation 块自标 `note = {Preprint}`）。
全文 116 页于 2026-11-07 取回并本地归档：`data/interim/rfd4_2026-11-07/RFD4-Proteina_paper.pdf`
（54,797,449 B）与抽出的纯文本 `RFD4_paper_text.txt`（272,125 字符，带 `===== PAGE n =====` 分页标记；
正文 p1–21、参考文献 p22–27、补充材料 p28–116）。
逐条实验台账、迭代轮次、筛选判据与局限的摘录见
[rfd4_paper_findings.md](../data/interim/rfd4_2026-11-07/rfd4_paper_findings.md)（127 条合格引句对底稿逐字核验通过）。
**本节所有数字均属发布权重版**（Table S11 的 release-scale 模型，~18,000 H200 GPU·h 含 LoRA 微调），
与 S21 那张"上一版权重"的 HF 效率表**不是同一批读数**。

#### 一、湿实验分母台账（引用任何一条都必须带上它的分母口径）

| 体系 | 计算侧 | 湿实验分母 → 读数 | 口径陷阱 |
|---|---|---|---|
| **PTE / paraoxon 有机磷水解酶**（双锌、8 残基 theozyme） | **15 / 1,000（1.5%）** 过 motif RMSD <1 Å + 蛋白–底物 min PAE <1.5 Å；RFD3 对照 **0 / 10,000** | **288 条测试 → 89 条活性（31%）**，覆盖 25/47 骨架家族；RFD3 平行对照 **0 / 192**；6 条（4 家族）进稳态动力学，最佳 k_cat/K_M **3,600 ± 500 M⁻¹s⁻¹**、k_cat 0.9 s⁻¹，较非催化水解提速 **1.5×10⁷ 倍** | **288 ≠ 15**。从生成池/过筛池到 288 条下单的选取规则**论文未给**（S13.7 只说沿用先前 metallohydrolase 流程）。89/288 是**测试池活性率**，不是全池命中率，也不是计算通过者的湿实验转化率。初筛自述缺陷："These initial cultures were not" + "sequence-verified and could be polyclonal."，且初筛时酶浓未归一 |
| **连接酶**（lenacapavir API 酰胺合成步） | 双判据（motif RMSD <1 Å + 配体 pLDDT≥50）**5.1%** vs RFD3 **0%**；另有多态 AF3 筛偏向氨解 | **67 条下单 → 4 条明确高于背景（6.0%）**；RFD3 旧战役 **0 / 72**。补充 Fig.32 另给 **8 条 >10% 转化**（无酶对照 6.8 ± 0.4%） | 正文"4 条"与补充"8 条 >10%"是**两条不同判定线**，都要记。最佳两条把 (S)-胺转化 79.0% / 61.7%，(R)-胺仅 8.8% / 14.6%；CysKO 对照证明依赖设计 Cys |
| **钙调蛋白 Ca²⁺ 构象态特异 binder** | 论文未给下单前数值筛 | **18 条测试 → 12 条钙依赖结合（66.7%）**（Table S31 明写 "Calcium-dependent hits: 12/18 (66.7%)."）；表观 K_D **69 pM – 37 nM** | 最低两个 K_D 的 k_off 触到仪器分辨下限（300 s 解离条件下 10⁻⁵ s⁻¹），作者明写亲和估计与 CI **以该下限为条件**。无细胞表达（Adaptyv），18 条的选取规则未给 |
| **IDR 无序肽 binder**（8 条肽） | 论文未给 | **每靶 94 条**（Table S33 "Screening hits among 94 designs tested"）：G3BP1 11/94、PAR2 16/94、YAP1 18/94、**EA1 0/94**、**TDP-A1 0/94**、N17 6/94、Tau-153 3/94、PER2 5/94 | **两个靶零命中**。正文称 "tight binders against all but one"，与 Table S33 的两个 0/94 有口径张力（"tight" 可能指 SPR 表征级而非筛选级）→ **以表格数字为准**。论文未给 EA1/TDP-A1 的机制性归因 |
| **Trk 家族 binder** | 论文未给 | 宽松口径：**188 条合计 → 158 条亚微摩尔（84%）**，对照 Claude Mythos Preview **18/60（30%）**。任务特异口径（Table S34）：人特异 TrkA **68/94**、人/鼠跨反应 **18/94**、TrkB **1/94**、TrkC **20/94**（仅筛选级，亲和力未测） | 188 = 94 + 94 两个**平行战役**（不同 spec），不是两轮。158 是"只要结合 hTrkA 就算"的宽松合计，68+18=86 是满足各自特异性约束的严格口径；**论文未给 158 的逐战役拆分**。分母规则明写："Denominators include transformation failures and exclude positive"（对照不算）。人特异战役的选择性证据仅 **n=4** |
| **糖基化控制**（保留 Man9/Glc1Man9） | RFDAA + ΔRASA 过滤 | **8/9** 占位点 >90% 寡甘露糖 | **补充 Fig.26 明写 "campaign hit rates were not assessed."** —— 9 个是 LC–MS/MS **表征子集**（对照 97 个 RFDAA 基线 + 43 个过滤谱），**不是战役命中率**；初筛 plate-scale 测了多少论文未给 |
| **pMHC / 磷酸化识别 binder** | 论文未给库容 | 酵母展示库 → FACS → 挑单克隆测序。pMHC 表观半最大浓度 340 pM / 710 pM / 1.60 nM；测序克隆数 SARS 30 / Phox2B 41 / MART-1 20 | 读数是**带 avidity 的展示滴定，不是溶液 K_d**（Table S32 明写）；磷酸肽选择性读数是 NGS 富集，作者明写 "This enrichment-based readout is not a binding affinity."。命中率按**克隆**计不按设计计 |
| **partial diffusion 救活旧失败设计** | 146 个已发表不结合 RFD1 设计里 **102 个**过不了现代 AF3 筛 → fraction 0.9、每父本 6 次 → **100/102 救活** | **无湿实验复测** | 补充明写 **"These outcomes are computational, not experimental binding measurements."** → 这条只能当计算能力证据，**不许当命中率** |

原句（底稿 `RFD4_paper_text.txt`，PAGE 17）：
"On this eight-residue theozyme, 15 of 1,000" + "RFD4-Proteina designs (1.5%) passed common motif-RMSD and substrate-confidence"；
"ing yielded 89 active RFD4-Proteina designs among 288 tested, spanning 25 of 47"；
PAGE 19："obtained genes encoding 67 designs for experimental testing. Four of these showed clear"。

**"第一轮就有活性"这句新闻转述的核对结果**：正文**没有**与 "many designs active from the first round" 对应的原句。
可支撑的事实只有：89/288 初筛有活性、全文未描述定向进化/亲和力成熟步骤、6 条直接进动力学。
新闻稿是对 **31% 测试池活性率**的转述，而 288 的选取口径未明 → **模板引用必须带分母与"选取规则未给"注记**。

#### 二、多轮迭代：论文**没有**序贯湿实验战役

逐条核对过的结论：**本文未描述任何"第一轮→第二轮→第三轮"的序贯设计战役（DBTL 循环）**。
容易被误读成迭代的四件事，实际各是别的东西：

1. **跨代 spec 迭代（PTE）**：RFD3 六残基 theozyme 催化效率低（"up to 4 ± 3 M−1 s−1"）→ 假设
   "adding two more catalytic residues could improve catalysis, but would require more" → RFD4 八残基 theozyme 新战役。
   改的是**模型（RFD3→RFD4）+ 条件 spec（6→8 催化残基）**，触发观察是旧酶效率低。这是跨代演进，不是同模型多轮。
2. **平行战役（Trk）**：人特异 94 与跨反应 94 是不同 spec 的平行战役，188 是 "collectively" 合计。
3. **文库内多轮排序（pMHC / 磷酸肽）**：表达排序 → 结合排序 → 竞争排序是**酵母展示选择轮**，
   设计集合不变（"Selected populations were regrown and reinduced between rounds."），不属于设计迭代。
4. **计算性二次机会**：partial diffusion 救活 100/102 是"旧设计→精修"的**计算**流程，无湿实验复测。

**论文真正给出的迭代建议是工具层的**：PAGE 4 "In practice, we find that small-scale pilots are helpful in determining the best"
+ "reasoning configurations for a given design challenge."；补充 Table S17 列出 agent skill
`rfd4-proteina-autoresearch`（"Runs iterative pilot experiments to compare" + "design inputs, inference settings and search" + "rewards."）
与 `rfd4-proteina-commitment-curves`（"Uses partial diffusion from a grid of restart steps"，测特征何时定型）。
→ **可抄的三种模式：pilot 定推理配置、失败设计 partial diffusion 精修、跨代 spec 升级。
不可写成"论文做了三轮战役"。** 迭代协议 §1 的轮次链因此全部取自库内 [B17] [B18] [B10] 等，不取自本篇。

#### 三、序列设计这一步：共设计已内置，MPNN 在本文只是基线

- 共设计内含序列：PAGE 8 Fig.2 注 "intrinsic sequence design and model-specific internal prediction but excludes downstream AF3 evalu-"。
  动机是 RFD3 无法同时优化结构与序列（PAGE 3）。
- **RFD4 自己就能做 inverse folding**：PAGE 11 "inverse folding tool by resampling side-chain identities while keeping the backbone"
  + "RFD4-Proteina consistently achieved higher pass rates than LigandMPNN at matched"（diversity）。
  实现【补充 PAGE 86】："RFD4-Proteina was run by partial diffusion from the input backbone (t = 0.99)"
  + "with the sequence latents at t = 0 and 60 steps of the temporal-score-rescaled sampler,"
  + "where the backbone is effectively fixed (Cα RMSD to the input below 0.4 ˚A)."
- MPNN 的不可替代场景也被内置：逐位残基概率条件化（PAGE 37 "specify arbitrary position-wise residue-type probabilities."
  + "constraints such as avoiding cysteine residues that may impact expression in E. coli."）。
- **MPNN 在本文的实际角色 = 基线**：BindCraft 单骨架协议含一步 ProteinMPNN、Genie3 配 CA-MPNN、
  AlphaProtein-novo 有 LigandMPNN 重设计变体；侧链 packing/inverse folding 对比用 LigandMPNN v1.1.1。
  **全部湿实验战役描述中未见任何 MPNN 步骤**（补充 S13 一律 RFD4 设计直接下单/建库）。
→ 模板 ③ 因此降为**可选的序列复核/重设计步**（已写进主模板 ③ 与 binder 分支的 RFD3 退路段）。

#### 四、reward-guided search 的代价边界：**标准基准上反而降效**

- 机制：分阶段剪枝，检查点按特征收敛时序设（界面面积 ~20%、氢键 ~50%、AF3 置信 ~80%）；
  oracle 在 search 期间蛋白结合用 AF2-Multimer、小分子/AME/DNA 用 OpenFold3，最终统一 AF3 评测另计；能量 oracle = TMol。
- **划算的场景**：示例肽-DNA 切割酶 "three times as many unique passing designs per GPU-hour"
  （Table S18：0.38 vs 0.13 unique passers/GPU·h，各 24 GPU·h；naive 23,316 完成→3 通过，search 4,057 完成→35 通过/9 unique）；
  酶包埋任务 **+22.6%**（"with burial, temporal search yielded 22.6% more passing" + "clusters per GPU-hour than naive sampling"）；
  小分子相互作用加难任务 **+24.6%**。
- **不划算的场景**：PAGE 78 "benchmark criteria reduced passing-cluster yield per GPU-hour."
  Table S29 蛋白结合 high-thinking **66.5 → search 8.4** clusters/GPU·h（尽管通过率 10.6%→14.9%）。
  正文 PAGE 9 自述原因："the efficiency gains from search do not outweigh" + "the computational overhead"。
→ **模板 ④ 的"生成内筛选"行必须带这条边界：search 不是默认开，只在难任务（复杂活性位/包埋/多相互作用）上开。**

#### 五、论文实际用的计算判据（**基准评测判据 ≠ 湿实验下单筛**）

四大基准 pass criteria【补充 S8.2，PAGE 72】：蛋白结合 = 骨架 RMSD ≤2.5 Å + binder pTM ≥0.80 + min 界面 PAE ≤1.5 Å；
小分子结合 = 蛋白骨架 RMSD ≤1.5 Å + 配体 RMSD ≤5 Å + ipTM ≥0.80 + min 界面 PAE ≤1.5 Å（作者明言严于原 DISCO）；
酶 scaffolding（AME）= 骨架 RMSD ≤2 Å + motif 全原子 RMSD ≤1.5 Å + min 界面 PAE <1.5 Å（改造了 RFD2 原判据：加 min PAE、删 clash 滤）；
DNA 结合 = DNA 对齐骨架 RMSD ≤8 Å + min 界面 PAE ≤1.5 Å（binder 长度改 120–150）。
分母：每靶 **200 次尝试**，失败留在分母（"Failed attempts and outputs with unmatched required motifs remain in the denomi-"）；
clustered pass rate = 通过结构簇 / 200（Foldseek TM-score 0.5）。

**湿实验战役真正用的筛子只有两处给了数值**：PTE = motif RMSD <1 Å + 蛋白–底物 min PAE <1.5 Å（Fig.6c）；
连接酶 = motif RMSD <1 Å + 配体 pLDDT≥50（Fig.6j）。
**binder 战役（钙调蛋白/IDR/Trk/pMHC/磷酸肽/糖基化）论文未给下单前的数值筛选阈值**
→ 模板**不得**把上面的基准判据冒充成这些战役的下单筛。想要开箱阈值仍须走模板 §H 在自己体系标定。

#### 六、作者自述的局限（除上表已列外）

- 计算指标 ≠ 实验成功的自认：PAGE 20 "In cases where existing computational metrics have not yet"
  + "translated to experimental success, the ability to generate diverse candidates meeting"
  → RFD4 被定位为**检验新筛选假设的基础**，不保证湿实验转化。
- 统计自限：retroaldolase AUROC 0.90 vs PLACER 0.82，但 PAGE 87 "The main-panel intermediate was selected retrospectively."
  + "paired intervals do not establish a method advantage."；HBDesigner 柔性 vs 固定比较里 recycling 与打分也不同，
  **不能孤立骨架柔性因素**，且柔性 RFD4 vs HBDesigner 的区间含零。
- 失败任务如实报告（EA1/TDP-A1 各 0/94、TrkB 1/94、TrkC 亲和力未测、RFD3 对照 PTE 0/192 与连接酶 0/72），
  但**未给机制性归因**；也**没有**"某类靶标不适用"的一般性声明。
- 训练数据截断：实验结构限 **2024-01-01** 前沉积（PAGE 31），另有 ESMFold2/TCR 等蒸馏数据。
  → 模板 §I 开工登记要求写死"模型版本 + 训练截断"，本篇的截断就是 2024-01-01。
- 基准适配自述：AME 41 任务剔除 4 个（3 个共价加合物需未索引修饰残基支持、1 个缺磷酸原子坐标）。

## 复现

- 取数方式：逐条 URL 于 2026-11-07 访问（DOI 走 https://doi.org/ 解析；README 走默认分支 `production` 的 raw 页面），
  取证级别按"读到正文 / 仅摘要 / 仅 README"三档如实标注，`2ND` 级条目已从可抄列表剔除。
- 独立复核：另一名复核代理逐条回原文核对 6 条最高风险断言（S1/S2/S4/S6/S8/S9/S11 + S0 的范围声明），
  结论归档为 `data/interim/frontier_2026_verify_2026-11-07.md`。6 条里只有 **S9 完全可用**，
  其余四条为"部分对"并各有一处硬错已被改写（见 S1/S2/S4/S8 与 S20）。
  **标 `未单独复核` 的条目在模板里一律只允许 `P3`（README/摘要级），不许升级成 `P2`。**
- 本页与模板的联动由 `scripts/verify_workflow_template.py` 检查：模板里每个 `[S..]` 必须能在本页表格首列找到。
