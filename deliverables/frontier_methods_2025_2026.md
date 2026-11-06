# 前沿方法核验清单（2025-06 → 2026-11）· 工作流模板的库外引用

模板 [protein_design_workflow_template.md](protein_design_workflow_template.md) 里所有 `[S1]`、`[S12]` 这样的编号都在本页定义。
**本页的存在理由**：152 篇精读卡的门禁只覆盖库内文献；工作流要跟上 2025–2026 的默认工具链，就必须有一条
独立、可查、带访问日期的库外引用通道，并把它的取证级别如实标出来——**不许把调研记忆写成"前沿事实"**。

- 调研与取证日期：2026-11-07（全部 URL 当日实际访问）。
- 取证级别：`FT`=读到正文/全文页 · `ABS`=仅摘要页 · `README`=官方仓库 README 或官方文档 · `2ND`=二手转引（**不得进模板**）。
- 与库内关系：`[S9]` 对应库内 [B35]（同一工作的预印本，库内是摘要级）；`[S2]` 的置信度阈值与库内 [B08] [B09] 的 pAE/pLDDT 口径同族。

| 编号 | 条目 | 一手来源 | 取证级别 | 模板里能用到哪一步 | 复核 |
|---|---|---|---|---|---|
| S0 | 六个查无一手来源的方法名（禁用） | 四路索引检索记录 | 检索级 | §I 禁用清单 | 复核中 |
| S1 | 官方默认链 RFD3 → MPNN/LigandMPNN → RF3，RFO 引入 Boltz-2 | https://github.com/RosettaCommons/foundry | README | ②③④ 选型 | 复核中 |
| S2 | RF3 技术报告（阈值/手性/步数/早停陷阱） | https://doi.org/10.1101/2025.08.14.670328 | FT | ④ 阈值候选 | 复核中 |
| S3 | Boltz 两个亲和力输出的分工 | https://github.com/jwohlwend/boltz | README | ④ 亲和力用法 | 复核中 |
| S4 | Boltz-2 亲和力可靠性独立评测（负面为主） | https://doi.org/10.1021/acs.jctc.6c01334 | FT | ④ 禁用绝对门槛 | 复核中 |
| S5 | 通用置信度在抗体–抗原近乎无效（AUC 0.5–0.6） | https://doi.org/10.64898/2026.05.13.724924 | ABS | A.2 失灵触发表 | 复核中 |
| S6 | Boltz-2 自报基准（FEP+ Pearson 0.66、CASP16 盲测 140 对） | https://doi.org/10.1101/2025.06.14.659707 | FT | ④ 量级参考 | 复核中 |
| S7 | 任务专用相互作用模型替代置信度（纳米抗体 3.3%→8.0%） | https://doi.org/10.64898/2026.06.23.733997 | ABS | A.2/A.3 路线切换 | 复核中 |
| S8 | Chai-2 零样本抗体设计（52 靶 × ≤20 条，15.5%） | https://doi.org/10.1101/2025.07.05.663018 | FT | A.1 命中率口径与 BLI 判据 | 复核中 |
| S9 | RFdiffusion3 正式见刊（96 构型零样本拿到活性催化剂） | https://doi.org/10.1126/science.aeh2982 | ABS | B.1 零样本规模 | 复核中 |
| S10 | 有本靶标活性标签后微调亲和力头 | arXiv `2609.24302` | ABS | ⑩ 回灌升级 | 复核中 |
| S11 | OpenFold3 检查点互不兼容、分数不可横比 | https://github.com/aqlaboratory/confornets + https://github.com/aqlaboratory/openfold-3 | README | §A 参数表"模型版本" | 复核中 |
| S12 | 多态酶设计：单过渡态约束被点名为缺陷 | https://doi.org/10.64898/2026.09.11.750617 | ABS | B.2 约束升级 | 复核中 |
| S13 | CaGE：把 RF3 再训练成设计条件网络 + 迭代衰减 | https://doi.org/10.64898/2026.10.02.756307 | FT | B.1/B.2 活性位约束 | 复核中 |
| S14 | MD+QM/MM 用于**解释**设计–进化差距（Kemp elimase） | https://doi.org/10.64898/2026.09.09.750330 | ABS | B.2 MD 的位置 | 复核中 |
| S15 | 设计与进化的稳定性/动力学互作（负面：初版只考虑过渡态） | https://doi.org/10.64898/2026.05.29.728685 | ABS | B.2 负面判据 | 复核中 |
| S16 | Metal Mer：无定向进化的金属酶选择性（ee > 99%，13 底物） | https://doi.org/10.64898/2026.10.13.758590 | ABS | B.5 三态收口 | 复核中 |
| S17 | AlphaProtein Novo：同骨架序列系综是主判据（DEHPase 新骨架 11%） | https://doi.org/10.64898/2026.10.01.756017 | FT | B.2 闸口设计 | 复核中 |
| S18 | 蛋白–肽复合物：AF2 优于 OF3，且 DockQ 阈值不可从蛋白–蛋白搬来 | https://doi.org/10.64898/2026.04.21.720042 | ABS | C.1 判据边界 | 复核中 |
| S19 | OpenBind：早期实验结构微调共折叠模型改善位姿与虚拟筛选 | https://doi.org/10.64898/2026.08.27.747600 | ABS | B.3/H 微调路径 | 复核中 |

## 逐条要点（含分母与局限）

### S1 Foundry = 官方默认链
`pip install "rc-foundry[all]"` → `foundry install base-models`（一次装最新 RFD3 + RF3 + MPNN），官方镜像
`rosettacommons/foundry`；Colab 教程标题即"a basic design pipeline with **RFD3, MPNN, and RF3**"。
第四个组件 RFO 定义为"RF3 梯度引导序列优化 + **Boltz-2 结构预测** + 外部 ProteinMPNN/LigandMPNN 重设计"。
**能证明**：官方对外教的默认三件套与"第三方模型进打分位"。**不能证明**：所有 Baker 组论文都按此组合
（库内 [B17] [B20] 用的是 Chai-1 复折）。**尚缺**：一份同口径湿实验命中率对比（RFD3+MPNN+RF3 vs RFdiffusion1+MPNN+AF2）。

### S2 RF3（原子级复折与置信度）
三个检查点：Latest(01/24)、Preprint(01/24)、Benchmark(09/21 训练截断，用于同截断对比)。
自报（`FT`，分母=自建非冗余测试集，按 40% 序列同一性/CCD 聚类，全部 in silico）：手性中心正确率
**RF3 88% / AF3 84% / Boltz-2 76%**（不加推理引导）；`num_steps` 200→50 精度不降、速度 >2×；
开 `early_stopping_plddt_threshold`（默认 0.5）后产出提升 **10–20×**。
论文正文自家设计筛选阈值：`pDE ≤ ln(0.075·length)` + `pLDDT ≥ 0.62` + `pAE ≤ 15`；蛋白–DNA 复折用
`mean pLDDT > 80` + `mean interface PAE < 10`。
**两个必须写进方案的坑**：无 MSA 时模型早停（只出 `.score` 不出结构文件）→ 批量筛除要把 `early_stopped` 单列，
"没结构"≠"结构差"；自定义配体与 CCD 同名会"catastrophically wrong"，需加 `L:` 前缀。
**尚缺**：这些阈值在他人体上的 ROC（作者未给留出集），因此模板只把它们列为"候选默认值"，进 §H 重标。

### S3 + S4 + S6 亲和力头：能做什么、不能做什么
分工（官方 README）：`affinity_probability_binary` 管 hit discovery 的二分；`affinity_pred_value` = log10(IC50, µM)
管系列内排序；两者训练数据与监督不同，不可混用。自报基准（`FT`）：FEP+ 四靶平均 Pearson **0.66**、算力快 >1000×；
CASP16 亲和力 track 140 对/2 靶盲测"clear margin"超过全部提交方；Recursion 8 个内部盲测 assay 中 **3/8 Pearson > 0.55**、其余有限。
独立评测（`FT`，16,780/21,702 化合物，Boltz-2 vs ESMACS ΔG）：整体 r=0.45/ρ=0.46（TNKS2）、r=0.24/ρ=0.25（3CLPro），
**top-100 集合内相关≈0**，几乎全部预测 < −4 kcal/mol（压缩），作者结论明确"不存在可迁移的通用阈值"。
→ 模板用法：只做系列内排序与二分提示；**禁止**设绝对门槛、禁止报"预测 K_D"；池子小于 ~100 时相关性会退化。

### S5 + S7 抗体–抗原：通用置信度失灵，任务专用模型可用
S5（`ABS`，519 条治疗性 mAb × 同源/随机非同源抗原）：Boltz-2 各类置信度 ROC-AUC 仅 **0.5–0.6**，
多特征/多变量建模"little to no improvement"，采样 ~15–20 seed 后收益递减。
S7（`ABS`，10 个新靶点）：用相互作用模型（BoltzPPI 类）替代结构置信度排序，纳米抗体命中率 **3.3% → 8.0%**；
可开发性五项全过 58%（对照 BoltzGen 40%、临床期 VHH 21%）。
→ 模板用法：抗体分支默认走"任务专用模型排序 + 展示库"，不走通用 ipTM 淘汰（与库内 [B22] 的 0%–2% 一致）。

### S8 Chai-2：本清单里分母最干净的一组
`FT`：**52 个新抗原**（PDB 中原无抗体/纳米抗体结合剂），每靶 **≤20 条**设计；平均实验命中率 **15.5%**
（VHH 20.0%、scFv 13.7%），**26/52 靶**至少 1 条确认结合剂；作者称此前 de novo 抗体设计的实验室成功率通常 <0.1%。
命中判据（可抄）：BLI 信号 **> 背景 + 0.1 nm 且 > 背景的 300%**。miniprotein 5 靶湿实验成功率 **68%**，
PD-L1/IL-7Rα/PDGFRβ/InsulinR 达皮摩尔级。表位到湿实验确认 **< 2 周**（E. coli 无细胞表达）。
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
  `>=0.5.0` 默认参数换成 OpenBind-0（训练截断 2025-06）。→ 模板 §A 参数表要求写死"模型版本 + 训练截断"。
- **S18**（271 个非冗余蛋白–肽复合体，CAPRI 判据，分 IDR/Non-IDR）：整体成功率 AF2 一致优于 OF3；AF2 在其训练集已含的
  复合体上有记忆效应；OF3 的 PAE 分布削弱了派生分数判别力；**蛋白–蛋白的 DockQ 阈值不能直接搬到蛋白–肽**。
- **S19**（肠道病毒 2A 蛋白酶，925 个晶体学结合事件/699 化合物/601 亲和力）：对接表现强依赖口袋构象、构象难排序；
  **用片段筛选阶段的晶体结构微调 OpenFold3-p2 可显著改善后续化合物位姿与虚拟筛选** → 支持"早期实验结构→本靶标微调共折叠模型"。

### S0 禁用清单（查无一手来源）
`RFSolo`、`DockDesign`、`MolGen`（作为蛋白设计方法）、`IG-LLM`、`LockMSF`、`PoseChains` 六个名称，
2026-11-07 在 EPMC（TITLE/ABSTRACT）、arXiv、Crossref、GitHub 四路检索均无一手论文/一手仓库。
**模板里禁止出现这些名字，也禁止写成"这些方法不存在"**——检索范围已声明，但全称否定不成立。

## 复现

- 取数方式：逐条 URL 于 2026-11-07 访问（DOI 走 https://doi.org/ 解析；README 走 raw 页面），
  取证级别按"读到正文 / 仅摘要 / 仅 README"三档如实标注，`2ND` 级条目已从可抄列表剔除。
- 独立复核：本轮另派一名复核代理逐条回原文核对 6 条最高风险断言（S1/S2/S4/S8/S9/S11），
  结果记录在 `data/literature_cards/run.md` 本轮小节；未被复核通过的条目仍标 `复核中`，
  模板引用它们时一律用 `P3`（仅 README/摘要级）而不是 `P2`。
- 本页与模板的联动由 `scripts/verify_workflow_template.py` 检查：模板里每个 `[S..]` 必须能在本页表格首列找到。
