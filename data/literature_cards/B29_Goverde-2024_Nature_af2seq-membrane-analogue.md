# [B29] 用 AF2seq-MPNN 把"只在膜里存在的折叠"设计成可溶蛋白——复杂拓扑与膜折叠的通用骨架生成器

Goverde C A, Pacesa M, Goldbach N, Dornfeld L J, Balbi P E M, Georgeon S, Rosset S, Kapoor S, Choudhury J, Dauparas J, Schellhaas C, Kozlov S, Baker D, Ovchinnikov S, Vecchio A J, Correia B E
Nature 2024, 631:449-458 · DOI 10.1038/s41586-024-07601-y · PMID 38898281 · PMCID PMC11236705
开放获取（CC BY 4.0）· https://doi.org/10.1038/s41586-024-07601-y
（第一单位是 EPFL Correia 实验室，Baker / Ovchinnikov 为共同作者；本文可视为 AF2 seq 骨架生成与 ProteinMPNN 序列设计的合流点）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B29**（组：Baker 组） |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory 登记 fetch_channel=epmc_fulltext，fetch_url 指向 PMC11236705） |
| 本地全文（本卡唯一比对底稿） | `data/interim/baker_lit/ft/memprot_analogue2024.txt`（164 行，正文 + 图注 + Methods 纯文本） |
| 登记底稿（门禁 sources_map） | 上述全文 + `sources/baker.md`（本卡引句只对着那份全文比对，未采用 baker.md 措辞） |
| 证据级别 | **全文级**（本卡全部引句在该全文里逐字命中；见第 9 节自检） |
| 未取到的部分 | 各图面板的数值本身（Extended Data Fig 1-4 与 Supplementary Fig 只有图注文字，无数据）、Source Data、新沉积结构坐标、动力学原始曲线。凡涉及这些处本卡明写"正文未给出，仅有正文/图注描述" |
| 已知抽取瑕疵 | 正文里阈值写作 `&gt;` / `&lt;`（HTML 实体未解码）；门禁比对前会对两侧做 html.unescape，故本卡引句按解码后的 `>` 抄。参考文献编号留在句子中间（如 `challenge 1 .`），因此本卡**不跨参考文献编号拼接引句**。`r.m.s.d.` 与 `RMSD Cα` 两种叫法混用，且 `Cα`（希腊 alpha）与 `Cɑ`（拉丁 alpha，门禁 norm 会归一成 `Ca`）在同一段里并存，抄写须与原样一致 |

## 1. 这篇到底解决什么（一句话）

让"只存在于膜环境里的复杂折叠（claudin、rhomboid 蛋白酶、GPCR 七螺旋）"与"公认难设计的复杂可溶折叠（Ig-like、β-barrel、TIM-barrel）"能用**同一套不加对称性、不加参数化约束**的深度学习流程（AF2 seq 出骨架 → ProteinMPNN 出序列 → AF2 复测三重闸口）批量设计出来，并且得到的可溶膜折叠类似物**保留天然功能界面**（CpE 毒素结合、GPCR 表位与 G 蛋白结合界面）。

拆成三个可检验的子问题：① 复杂拓扑能否不靠人为约束设计出来；② 膜折叠的可溶性是"必须专门替换表面疏水残基"的技艺，还是"按可溶环境重设计整条序列"就自然可得；③ 可溶化之后原功能位点还在不在。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，非我们推测）

1. **AF2 倒过来做设计，"骨架能行、序列不行"是这篇的出发点**。作者开篇就把限制写死："their performance in sequence design has been suboptimal, as evidenced by low experimental success rates"，并说清只有别人验证过 MPNN 能改善 AF2 生成结构的可表达性，但复杂拓扑没人验过。
   **应对**：不做新模型，做**串联**——AF2 seq 只负责出可设计骨架，序列全部交给 ProteinMPNN（"To address this challenge, we integrated our previously developed AF2-based design approach"）。
   **代价**：这条串联让"设计成功"的定义变成**结构自洽 + 可溶表达**，功能位点必须另外用移植手段（第 6 条）才谈得上。
2. **复杂折叠在 AF2 单序列模式下根本复测不出来**（这是漏斗闸口自身的失效）："we found that for some more complex design tasks, the target structure could not be predicted in single sequence mode by AF2 after ProteinMPNN redesign"。也就是"用 AF2 复测来筛 ProteinMPNN 序列"这道闸，越难的靶越容易把好设计误杀。
   **应对**：用 **AF2 seq 出的那条起始序列作为输入条件**再预测（AF2 seq -MPNN 组合），使目标折叠能被准确复现（Extended Data Fig 2，正文描述）。
   **代价**：复测时带的是"祖先序列"信息，**闸口的独立性被削弱**（同一份先验既参与生成又参与验证）。
3. **提高多样性的常规手段（给骨架加高斯噪音）与置信度直接冲突**。加噪能降低序列回收率（更多样），但 "this was at the expense of low-confidence predictions that deviated significantly from the target fold"。
   **应对**：放弃加噪（"No Gaussian noise was added to the input backbone"），把多样性来源转到**骨架本身**——AF2 seq 每次都造新的骨架模板，而不是在同一个晶体骨架上扰动；并实测对比 Rosetta backrub 与 MD 扰动的多样性远不如 AF2 seq。每个骨架只让 MPNN 出 2 条序列（"we generated two sequences per AF2 seq -designed backbone"）。
   **代价**：多样性靠生成端"免费"提供，但正文同时承认结构多样性受限（"despite the restricted structural diversity"，面板数据在未取到的 Extended Data Fig 1a,b）。
4. **膜折叠第一次做可溶化，直接全灭**：AF2 seq 的初始设计新颖度高、表面疏水比例也低，但 "none could be expressed in soluble form"。换标准 ProteinMPNN 也不解决，"the resulting sequences consistently recovered the surface hydrophobics, probably owing to the similarity of the topology to that of membrane proteins encountered during training"——模型的训练分布把序列往膜环境拉回去。
   **应对**（三步递进，前两步失败都被写进正文）：先试采样偏置 "Biasing the amino acid sampling towards hydrophilic amino acids (AF2 seq -MPNN bias ) only marginally improved the solubility of the designs"，仍不行；于是**重训网络**——"we retrained the ProteinMPNN network using a dataset of only soluble proteins, which we named soluble MPNN (MPNN sol )"，训练集只收 X-ray/cryo-EM 优于 3.5 Å、少于 10,000 残基、并**剔除注释为跨膜的 PDB 条目**。这一步把 CLF/RPF/GLF 的可溶表达率抬到 10/13、13/15、36/56。
   **代价**：可溶性是**通过训练分布注入的先验**拿到的，不是靠物理判据；换个环境需求（例如要膜环境序列）就得再训一个模型。
5. **设计轨迹不收敛 + 统一阈值在最难的靶上不成立**："Not all design trajectories of the claudin, rhomboid protease and GPCR converged"，且 rhomboid 的复测分数系统性偏低。
   **应对**：一是发明 **soft starts**——"we sampled sequences from successful trajectories and introduced mutations, while disabling distogram loss. These sequences were then used as starting points for new design trajectories, which we named soft starts, resulting in a higher convergence rate"；二是**给 rhomboid 单独放宽闸口**：TM score 0.80 降到 0.75、pLDDT 80 降到 75（Methods 明写理由："the rhomboid protease yielded slightly lower TM scores in the design trajectory; hence, we chose a cut-off value 0.75 instead"）。
   **代价**：漏斗阈值变成**按靶定制**，跨靶成功率不再同口径可比；而且放宽的正是那个 AF2 复测最不可靠的靶。
6. **功能位点不能靠从头设计得到，只能"粘贴"**：他们承认活性构象的从头设计做不成——"for the design of the active conformation, we found that it was not possible to generate high-confidence designs without the presence of G protein"，于是把 mini-Gs 结合蛋白放进梯度下降与预测的体系里。可溶化后的天然模体（DRY、PxxY、跨膜脯氨酸富集区）在设计中全部缺失，作者把这解释成优势（"This demonstrates that by design one can explore very diverse sequence spaces while removing potential evolutionary biases"）。功能则改走**表位移植**：Foldseek 在 PDB 里找 TM score 高于 0.7 的可溶骨架，把天然 epitope 序列粘回重叠区，AF2 单序列复测后挑 pLDDT 高于 90 的**人工检查**（"Structures with high pLDDT (greater than 90) and high TM scores relative to the starting scaffold were manually inspected to verify the placement of the epitope"）。
   **代价（本文未解决）**：移植体同时受功能与稳定性拉扯，正文给出现象但没有机制——"the higher proportion of native sequence preserved in claudin-1 design CLN1_14 resulted in a reduced melting temperature compared with CLN1_18"；且"人工检查"这一步没有可复现阈值。
7. **"折叠对了"不等于"像天然折叠"**：CLF_4 对设计模型 0.73 Å，但对**目标折叠** 3.63 Å；RPF_9 对设计模型 0.97 Å，对目标折叠 5.67 Å，偏差集中在胞外环；GLF 与天然 GPCR 整体骨架差 3.08 / 3.51 Å。作者的收口是承认结构复杂度的固有难度（"highlight the inherent difficulty in designing folds with such structural complexity"），并把环区偏差归因于其天然位置在水-膜界面。
   **代价**：证据链的主判据是"设计模型 vs 晶体"，天然折叠只作为参照，因此"我们复现了膜折叠"这句话的可辩护范围比标题弱一档（本文对"是否保留了天然折叠的生物学构象约束"没有给出直接实验）。

## 3. 方法与工作流程（可复现顺序）

### 用了哪些方法（工具箱，以及为什么选它）

- **骨架构图**：AF2 seq（把 AF2 网络反过来用，对序列做梯度下降，代价函数同时含拓扑项与置信度项）。选它的理由：相对 Rosetta backrub 和 MD 扰动，AF2 seq 生成的骨架能让 MPNN 产出"much greater protein sequence diversity"，且多样性来自新骨架模板而不是序列回收（Fig 1c/d、Extended Data Fig 1/2）。
- **序列图**：ProteinMPNN 三种权重并行——vanilla（训练集带 0.1 Å 噪音）、MPNN bias（极性氨基酸正采样偏置 + Ala 负偏置）、**MPNN sol**（本文新训，训练集只用可溶蛋白、剔除注释为跨膜的 PDB 条目）。
- **复测/闸口图**：AF2 三次 recycle + AMBER 力场 relaxation，再看 TM score（TM-align）、pLDDT、BLAST e-value（对 NCBI RefSeq 2022-10-01 库，max hits 1,000）；表面疏水比例用 Rosetta layer selector + SASA 定义算（"apolar amino acids (defined as 'GPAVILMFYW')"）。
- **结构搜索图**：Foldseek 对 SCOP（2023-03 下载）做折叠归属与"该折叠是否只存在于膜环境"的判定；对 PDB 做兼容表位搜索。
- **复杂度定量图**：相对接触序（Relative Contact Order）× 序列长度，用来"选出难的靶"（Extended Data Fig 3，Methods）。
- **湿实验图**：蛋白表达纯化（正文/主 Methods 未写宿主与细节，在补充信息）、SEC-MALS、变温 CD 与熔解曲线、X-ray 晶体学、cryo-EM（复合物 + Fab/纳米抗体增强）、BLI、SPR、pull-down 预筛。
- **构象特异设计**：以 A2A 受体活性态（PDB 5G53，与 mini-Gs 复合物）与失活态（PDB 3VGA）分别作模板，固定与 G 蛋白接触残基和 DRY motif；活性态必须在 mini-Gs 存在下做梯度下降与预测。
- **没有用的方法**：**MD 只作为"骨架扰动备选方案"的对照组**出现在 Fig 1d / Extended Data Fig 2，不参与机理或自由能计算；全文没有 QM、没有自由能微扰、没有酶活/催化计算。这一点很关键——这篇的能力边界是"结构 + 结合"，不含"反应"。

### 工作流（每步：输入 → 操作 → 判据/阈值 → 输出规模）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | PDB 目标结构：IGF 3SD2、BBF 6D0T、TBF 5BVL、claudin 4P79、rhomboid 3ZEB、GPCR 6FFI（缺失残基先用 AF2 带模板补全；claudin 34-40 与 GPCR 875-896 无序区分别换成三聚甘/五聚甘 linker；GPCR 去掉结晶用溶菌酶域 679-838） | AF2 seq 梯度下降生成初始序列：按目标二级结构编码初始化（Ala 螺旋 / Val β / Gly 环），每条轨迹再把 10% 氨基酸随机突变 | "In each AF2-sequence design trajectory, 500 rounds of gradient descent optimization were performed"；复合 loss 权重 "the designs were generated using loss terms W FAPE = 1.0, W pLDDT = 0.2 and W pTM = 0.2"，初始轨迹 W dist = 0.5；AF2 单序列模式、model_5_ptm、zero recycles、MSA 与 template 关闭（claudin-1/-4 例外：只用 model 1/2 且开 template） | 每个靶一批 AF2 seq 骨架；**骨架总数与收敛数正文未给，只在 Supplementary Table 1** |
| S2 | 未收敛的 claudin / rhomboid / GPCR 轨迹 | soft start：从收敛轨迹取序列、引入突变、关掉 distogram loss，重跑梯度下降 | 原文未给收敛率阈值数字，只有定性 "resulting in a higher convergence rate" | 收敛骨架池（规模在补充表，未取到） |
| S3 | AF2 seq 骨架 | ProteinMPNN 出序列（vanilla / bias / **sol** 三种） | 每骨架固定出 2 条："we generated two sequences per AF2 seq -designed backbone"；输入骨架不加高斯噪音；解码时掩蔽半胱氨酸 | 序列池 ≈ 2 × 收敛骨架数；可溶膜折叠类任务只有 MPNN sol 能通过（Fig 3d/e） |
| S4 | 全部生成序列 | AF2 复测（3 recycles）+ AMBER 力场 relaxation，再过三闸口 | 主文口径：TM score > 0.8、pLDDT > 80、e-value > 0.1；Methods 口径含例外："TM score > 0.80 for all designs except the rhomboid protease"（改为 0.75）、"pLDDT > 80 for all designs except the rhomboid protease (pLDDT > 75)"、"an e -value threshold > 0.1 for sequence novelty" | 通过 in silico 过滤的设计数正文未给（"The total numbers of designs and designs passing in silico filtering are summarized in Supplementary Table 1"） |
| S5 | 过滤后的设计 | 按 AF2 置信度 + 序列多样性排序，挑一批下单表达 | 原文未给数值阈值（"selected 19 designs for experimental characterization on the basis of AF2 confidence scores and sequence diversity"，细则在 Supplementary Fig 1/2） | 送测数：IGF 19、BBF 25、TBF 25、CLF 13、RPF 15、GLF 56 |
| S6 | 表达产物 | SEC-MALS 判单分散/寡聚 + 变温 CD 判折叠与 Tm | 定性判据（可溶 / 单体 / 螺旋或 β 特征谱 / 高 Tm）；正文里的最好稳定性读数写成"Tm 高于 90 °C"：GLF 十条全过（"All ten designs also showed high thermal stabilities"），CLF 五条深做中两条过，RPF 三个单体全过 | 可溶表达：IGF 7、BBF 6、TBF 5、CLF 10、RPF 13、GLF 36；其中折叠+单体：IGF 4（单分散峰）、BBF 6、TBF 5、CLF 3（5 条深做）、RPF 3（5 条深做）、GLF 9（10 条深做） |
| S7 | 代表设计 | 结晶 / 冷冻电镜，与**设计模型**和**目标折叠**分别算 r.m.s.d. | 原文未给通过阈值，直接报数：TBF_24 1.34 Å 分辨率、X-ray vs 设计模型 0.80 Å Cα / 2.12 Å 全原子、vs 对称模板 2.06 Å；CLF_4 0.73/1.28 Å（vs 目标折叠 3.63 Å）；RPF_9 0.97/1.83 Å（vs 目标折叠 5.67 Å）；GLF_18 1.05 Å、GLF_32 0.88 Å（vs 天然 GPCR 3.08/3.51 Å） | 4 个可溶膜折叠类似物 + 1 个复杂可溶折叠的高分辨晶体结构 |
| S8a | 想加功能位点的设计 | 表位移植：Foldseek 用可溶骨架查 PDB，取 TM score 高于 0.7 且表位周围结构相似的命中，叠加后把天然 epitope 序列粘回重叠区，AF2 单序列复测 | "Structures with high pLDDT (greater than 90) and high TM scores relative to the starting scaffold were manually inspected to verify the placement of the epitope" | 16 条 ghrelin ICL3 嵌合体进入 pull-down 预筛（9 条结合）；claudin 胞外段移植体 CLN1_14 / CLN1_18 / CLN4_20 |
| S8b | 构象特异需求 | 固定 G 蛋白接触残基与 DRY motif，活性/失活态分别设计，长度与功能位点保持一致 | 原文未给阈值；硬约束是"活性态必须带 mini-Gs 一起算"（"it was not possible to generate high-confidence designs without the presence of G protein"） | 3 条 aGLF + 3 条 iGLF，全部单体可溶折叠 |
| S9 | 功能化产物 | BLI（claudin vs CpE）、SPR（抗 ICL3 抗体、mini-Gs-414）、SEC-MALS 复合物滴定、cryo-EM（CLN4_20-cCpE-Fab-纳米抗体） | 亲和力口径：嵌合体对 ICL3 抗体 "between 150 nM and 790 nM"；阴性对照 = 未移植表位的 GLF 骨架 + 表位敲除突变体 + 失活态 iGLF | 与天然膜受体相比可比的 CpE 结合动力学；aGLF 有结合信号但亲和力无法确定（快速动力学），iGLF 无结合；DRY 点突变完全消除结合 |

**这套流程值得单独记住的骨架**：先定义"难"（RCO × 链长选靶）→ 用**两个网络串联**（一个出骨架、一个出序列）→ 用**第三个网络复测**并设三闸口（TM/pLDDT/e-value）→ 湿实验只买几十条而不是几万条 → 结构验证同时对着"设计模型"和"天然目标折叠"报两套数 → 功能不是设计出来的，是**移植 + 固定残基约束**做出来的。

## 4. 关键数字台账（数值 · 含义 · 出处）

| 数值 | 含义 | 出处（本卡引句或原句所在段落） |
|---|---|---|
| 1,075 vs 189 | SCOP 里"只在膜环境出现的折叠"数 vs 两种环境共有折叠数（本文的问题规模） | "We observed that 1,075 membrane proteins exhibited unique topologies that were not found in soluble form, with only 189 folds being present in both soluble and membrane environments" |
| TM score > 0.8；pLDDT > 80；e-value > 0.1 | 复测三闸口（主文口径） | 第 15 行方法与结果段："filtered on the basis of their structural similarity to the target topology" |
| TM 0.75 / pLDDT 75（仅 rhomboid） | 最难靶单独放宽的闸口 | "TM score > 0.80 for all designs except the rhomboid protease"；"pLDDT > 80 for all designs except the rhomboid protease (pLDDT > 75)" |
| 500 轮 / 10% | 每条 AF2 seq 轨迹的梯度下降轮数；初始序列随机突变比例 | "In each AF2-sequence design trajectory, 500 rounds of gradient descent optimization were performed"；"To diversify the generated designs, 10% of the amino acids were randomly mutated in the initial sequence of each design trajectory" |
| loss 权重 1.0 / 0.2 / 0.2（初始 W dist 0.5） | AF2 seq 复合代价函数权重 | "the designs were generated using loss terms W FAPE = 1.0, W pLDDT = 0.2 and W pTM = 0.2" |
| 2 条/骨架；0 噪音；掩蔽 Cys | ProteinMPNN 出序列设置 | "we generated two sequences per AF2 seq -designed backbone" |
| 3.5 Å 以内 / 少于 10,000 残基 / 剔除跨膜条目 | MPNN sol 训练集条件 | Methods "Training of MPNN sol"（本卡第 2.4 节引句同段） |
| 单张 Nvidia Tesla V100（32 GB） | 设计计算硬件（单价口径：正文未给 GPU-秒/设计） | "All design runs were executed on a single Nvidia Tesla V100 (32 GB) GPU" |
| 19 / 25 / 25 → 7 / 6 / 5 → 4 / 6 / 5 | 三种复杂可溶折叠：送测 → 可溶 → 折叠且单体（IGF / BBF / TBF） | "We tested 13 designs for the claudin-like fold (CLF)"同段系列句；IGF 段 "Seven designs were soluble, with four designs exhibiting monodisperse peaks in solution"；BBF 段 "We experimentally characterized 25 designs, of which six were found to be folded and monomeric in solution"；TBF 段 "We experimentally assessed 25 designs, five of which were monomeric, folded and highly thermostable in solution" |
| 13 → 10 → 5 → 3；15 → 13 → 5 → 3；56 → 36 → 10 → 9 | 三个膜折叠类似物：送测 → 可溶 → 深入表征 → 单体折叠（CLF / RPF / GLF） | "We tested 13 designs for the claudin-like fold (CLF), of which ten were found to be expressed in soluble form"；"We selected 15 designs for protein expression, of which 13 were found to be soluble"；"We tested 56 designs, of which 36 were expressed to be soluble" |
| Tm 高于 90 °C | 可溶膜折叠类似物的热稳定水平（CLF 2/5、RPF 3/3、GLF 10/10） | "All ten designs also showed high thermal stabilities"（同段括号内给 Tm 数值，°C 未进引句） |
| 1.34 Å | TBF_24 晶体结构分辨率 | "we solved a crystal structure of TBF_24 at 1.34" |
| 0.80 / 2.12 / 2.06 Å | TBF_24：X 射线 vs 设计模型（Cα / 全原子）、vs 初始对称模板 | "Comparison of the X-ray structure with the designed model showed the r.m.s.d. Cα and full-atom r.m.s.d. fa"（同句给出 0.80 Å 与 2.12 Å；对模板 2.06 Å 在同段） |
| 0.73 / 1.28 / 3.63 Å | CLF_4：vs 设计模型（Cα / 全原子）、vs 天然 claudin 目标折叠 | "as indicated by an r.m.s.d. Cα of 0.73" |
| 0.97 / 1.83 / 5.67 Å | RPF_9：vs 设计模型、vs 目标折叠 | "with r.m.s.d. Cα of 0.97" |
| 1.05 / 0.88 / 3.08 / 3.51 Å；1.54 / 1.40 Å | GLF_18 与 GLF_32：vs 设计模型、vs 天然 GPCR；两者全原子偏差 | "with r.m.s.d. Cα values of 1.05" |
| 2.84–4.03 Å；3.34–5.57 Å | CLF 与 RPF 的 **AF2 预测 vs 设计模型** 偏差（预测器在最复杂折叠上先失准） | "exhibited r.m.s.d. Cα values ranging from 2.84 to 4.03"；"with the r.m.s.d. Cα values between models and predictions ranging from 3.34 to 5.57" |
| 0.61 | 天然 GPCR 的表面疏水残基比例（设计体应远低于此） | "The fraction of surface hydrophobics of the native GLF is 0.61 (red line)." |
| 序列同一性 < 13%；最近 e-value < 0.063 | CLF 设计体与天然折叠的序列距离 | "The CLF designs showed sequence identity below 13% relative to the native fold" |
| 16 → 9；5 条 Kd 150–790 nM | ghrelin ICL3 嵌合体 pull-down 预筛命中数，与 SPR 亲和力区间 | "we prescreened 16 chimeric designs for binding and found that nine designs bound to the ICL3-targeting antibody"；"between 150 nM and 790 nM" |
| ~50% | ProteinMPNN 相对起始序列的平均回收率（前作报告值，本文用来解释可溶化失败） | "which was originally reported to consistently recover approximately 50% of the starting sequence" |
| 34% | GPCR 作为药物靶点占 FDA 已批准药物的比例（动机数字） | "About 34% of all drugs approved by the US Food and Drug Administration target GPCRs" |
| 正文未给 | 每个靶"生成多少条 / 过滤后剩多少条"（漏斗真正的分母）与 GPU-秒单价 | "The total numbers of designs and designs passing in silico filtering are summarized in Supplementary Table 1"（补充表未取回） |

## 5. 结论——作者说了什么

1. 问题的起点他们写得清楚："The robust computational design of complex protein folds remains a difficult endeavour"；而此前"no generalizable approach for the computational design of soluble membrane topologies with preserved functional aspects has been devised"。
2. 方法结论：框架本身不需要按折叠定制——"The computational framework based on AF2 seq -MPNN is flexible and generalizable, avoiding the need to perform fold-specific retraining or provide tedious parametric and symmetric design restraints for fold conditioning"。
3. 成功率结论："We designed and characterized several folds that have been very challenging to engineer with previous methods, achieving high experimental success rates in terms of soluble and folded designs"（分母口径见第 7 节）。
4. 精度结论："the computational models had very high accuracy, in terms of both overall fold and the fine details of the side-chain conformations, which are critical for the design of function"；摘要同义表述为 "Biophysical analyses demonstrate the high thermal stability of the designs, and experimental structures show remarkable design accuracy"。
5. 概念结论（这篇最想让读者记住的一句）："we showed that membrane protein folds generally follow the same design principles as soluble protein folds, and that many such folds can be readily designed in soluble form"；结果段里更谨慎的说法是 "hinting that these topologies share many of the designability principles and constraints of folds present in the soluble proteome"。
6. 功能结论（只到"结合"这一层）：可溶 claudin 与膜_bound 对照可比 —— "Binding assays using bio-layer interferometry (BLI) indicated that soluble claudin-1 and claudin-4 exhibit binding kinetics and affinities for CpE that are comparable with those of their membrane-bound counterparts"；构象态结论 —— "These results indicate that specific functional states can be designed with high accuracy while preserving critical evolutionarily conserved motifs in de novo designed scaffolds"。
7. 作者自己留的口子：aGLF 与 mini-Gs 的结合"exact affinities could not be determined owing to rapid interaction kinetics"；全文**没有一处催化活性测量**（rhomboid 的 Ser-His 催化二基团只作为"为什么这个折叠重要"的动机被提及）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

以下为推断。

1. **这篇真正的贡献不是"设计了 GPCR"，而是证明了"可溶性"这件事可以被写进序列模型的训练分布里**。AF2 seq 出的骨架已经够新、够不像膜蛋白，但标准 MPNN 仍把疏水表面"回收"回来；解决方式不是加物理项，而是重训一个"没见过跨膜蛋白"的 MPNN。→ 对我们：当一个性质（如可溶、如表达、如"能成键"）被模型训练分布决定时，**换训练集比换判据更有效**，也更能掩盖"我们其实不懂这个性质"的事实——这是能力上限的证据，不是理解深度的证据。
2. **"设计精度"被拆成两个参照系之后，故事强度差很多**：对设计模型 0.73-1.05 Å，对天然目标折叠 3.08-5.67 Å。前者证明"网络自洽"，后者才证明"折叠被复制"。作者的标题式结论靠前者，图里同时给了后者。→ 我们审任何"结构预测精度"主张时，必须问清**对谁算的 RMSD**。
3. **漏斗的"高成功率"是一个没有分母的宣称**：正文从头到尾没给出每个靶生成多少条、过滤掉多少条（唯一去处是未取回的 Supplementary Table 1）。因此 7/19、36/56 这些数字是**送测之后的命中率**，不是计算漏斗的产出率。→ 与我们的教训同源：**账面先于实测**；引用这类"成功率高"时必须标注它是哪一级的分母。
4. **功能不是设计出来的，是粘进去的**：表位移植需要"天然 epitope 序列 + 人工检查 pLDDT>90"，而从头设计时天然保守模体（DRY、PxxY）全部丢失。作者把丢失说成优势（去除进化偏差），但功能恢复完全依赖保留天然序列——CLN1_14 保留更多天然序列反而 Tm 下降。→ 对我们做酶催化位点：这是同一对矛盾的清晰版本——**催化能力与"全新"是互相拉扯的，不能两头都声称**。
5. **全文没有一次酶活测量**（"activity"一词在正文一次都没出现），所以这篇**不能**被引为"深度学习能设计催化功能"的证据；它能被引为"深度学习能给出可承载活性位点的骨架几何"的上限证据。这个区别正是我们项目里"折叠/位点几何"与"真做反应"的分界。
6. **最难的两个靶靠"降低门槛 + 增加外部组分"过关**（rhomboid 阈值放宽、活性构象必须带 mini-Gs 一起算）。→ 对我们：当一个判据在最难的样本上失配时，**必须留下按靶定制阈值的痕迹**，否则跨样本比较立刻失真。

## 7. 局限与失败（作者的 + 我们读出的）

**作者写在正文里的**
- 序列多样性受限：正文承认 AF2 seq 骨架"restricted structural diversity"（面板在未取回的 Extended Data Fig 1a,b）。
- 复测器在最复杂折叠上先失准：CLF 的设计-预测偏差 2.84-4.03 Å，RPF 更差（3.34-5.57 Å），作者明确承认这体现"the inherent difficulty in designing folds with such structural complexity"。
- 亲和力测不准：aGLF 与 mini-Gs 的相互作用"exact affinities could not be determined owing to rapid interaction kinetics"（SPR 快速动力学）。
- 环区/胞内段偏差：RPF_9 第一条胞外环与 GLF_18 胞内侧相对天然折叠明显偏移，归因于其天然位置在水-膜界面。

**我们读出的、以及本文未解决的**
- **Methods 里 core 与 surface 的定义写成同一句**："The core residues were defined as residues with less than 20"（Å² SASA），紧接着 "surface residues were defined as residues with less than 20"（Å² SASA）。两个互斥集合用同一个阈值方向定义，按字面不可能同时成立（surface 疑为大于 20 Å²）。而 Fig 1d 关于"多样性主要来自骨架而非序列回收"的核心归因，正是画在这两个集合上的——**这是本卡认为最可疑的一处判据**。
- **"避免按折叠定制"与"按折叠放宽阈值"并存**：结论声称框架无需 fold-specific 处理，但 Methods 明写 rhomboid 的 TM/pLDDT 双阈值单独下调，活性构象设计单独加入 mini-Gs。作为方法论宣称，这句比作为实验记录更响。
- **"可溶表达"和"折叠且单体"是两个不同层级的成功**，正文把它们并排写成"high experimental success rates"，读者容易只看到 36/56 而漏掉"深入表征的 10 条里 9 条单体"。
- **本文未解决**：① 没有任何催化/生化活性读数（rhomboid 的 Ser-His 二基团只当动机提及，未设计也未测）；② 没有给出漏斗上游分母（生成/过滤总数只在补充表）；③ 没有说明这些可溶类似物是否能在膜环境中重新工作（可溶化是单向的）；④ 表位移植的成功判据含"人工检查"，不可复现。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**

1. **"骨架 / 序列 / 复测"三段串联 + 三道独立闸口**的组织方式：把"生成"与"评价"用不同网络分开，并让评价闸口的每一项（几何一致 TM、置信 pLDDT、新颖度 e-value）各自可单独下调并留痕。我们本库通道（Foldseek 结构通道 / 序列通道 / 位点通道）应照此写成**可逐条放宽并记录理由**的表，而不是一个综合分。
2. **同一批结构报两套参照系**（对设计模型、对天然模板）：我们评估候选活性位点几何时，必须同时报"对 AF2 预测模型的自洽度"与"对参考酶的移植误差"，只报前者等于自证。
3. **难度先量化再选靶**（RCO × 链长）：我们应当先给 靶点集算一个复杂度指标，把"这个漏斗在难题上还行不行"和"在易题上命中率高"分开报。
4. **性质由训练分布决定时，改训练集**：如果"能否在可溶/可表达背景下成键"是我们要的性质，可以构造一个只含（或排除）某类反应背景的序列集重训模型——但要如实写成"能力证明"，不是"机理理解"。
5. **功能靠约束而非从头**：这篇的可靠路径是"固定催化相关残基 + 其余全重设计"（对应我们的固定催化残基/辅因子接触位，重排第二壳层）。它的**失败模式也要抄**：保留天然序列越多，热稳定越低（CLN1_14 现象），提示我们固定位点要尽量少、且把稳定性代价显式计入。
6. **"结合伙伴必须在计算体系里"这一条**：活性构象必须与 mini-Gs 一起算才出高置信度。对我们：判定"成键几何"时，底物/辅因子必须显式出现在被评估的结构里，脱离底物的 apo 结构自洽度不能作为支持证据。

**不可迁移（为什么不能照搬）**

1. **这篇没有任何酶活/化学转化读数**，因此它的"成功率高"不能换算成酶设计的任何概率或判据；把它的可溶表达命中率当成"设计能催化"的先验是错的（本文连测都没测）。
2. **TM score 0.80 / 0.75、pLDDT 80/75、e-value 0.1 是"折叠像不像"的判据**，与"能不能把底物装到 tRNA/肽链上"没有对应关系；尤其 rhomboid 阈值被单独下调这一事实说明这些数不是通用门槛，**不许**当作我们漏斗的默认阈值引用。
3. **它的湿实验通量（一次做几十条、每条独立纯化表征）在产物化学上不存在**。我们一轮最多四个构建体，末端的价值来自机制多样性与失活对照，不是样本数——这点与 B09 的教训一致，不能靠"多做几个"提高置信。
4. **可溶化是"把膜环境性质搬到水环境"**，不涉及化学键形成与断裂；这篇里没有自由能垒、没有过渡态、没有竞争副产物的概念，因此不能为"S1/S2 竞争"提供任何方法学支撑。

## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/memprot_analogue2024.txt

- 本地纯文本：`data/interim/baker_lit/ft/memprot_analogue2024.txt`（Europe PMC fullTextXML 抽取文本，164 行；正文 + 图注 + Methods + 参考文献列表混排，参考文献编号留在句子中间）。
- 本卡**所有**引句只对着这一份文件逐字比对；未使用 `sources/baker.md` 的措辞作引句底稿（它虽登记在同编号底稿里，但那份原卡是二手摘要，字句不同会导致假红）。
- 对照底稿行号：`sources/baker.md`（Baker 组调研卡，本卡未逐字引用）。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- **本卡自检**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B29" --no-report`（只打印、不落盘，不覆盖他人产物）。结果见本节末与对话回报。
- 已知不可核验之处：正文未给出的漏斗上游计数、补充图表数值、表达宿主与纯化细节、cryo-EM 分辨率具体值（仅图注给了 FSC 截断口径 0.143），本卡一律写"正文未给"或"在未取回的补充材料里"。

<!--CSV回填
work_type=论文（Nature 2024 全文；深度学习 de novo 蛋白设计 + 结构/生物物理验证 + 功能化）
target=六个折叠骨架：Ig-like（PDB 3SD2）、β-barrel（6D0T）、TIM-barrel（5BVL）、claudin（4P79）、rhomboid 蛋白酶（3ZEB）、GPCR（6FFI）；功能化对象为人 claudin-1/claudin-4 对 CpE、ghrelin 受体 ICL3 表位、腺苷 A2A 受体活性态（5G53）与失活态（3VGA）对 mini-Gs-414
backbone_generation=AF2 seq（AF2 网络反演做序列梯度下降）：按目标二级结构编码初始化序列（Ala 螺旋/Val β/Gly 环）+ 每条轨迹 10% 残基随机突变；每条轨迹 500 轮优化；复合 loss（W FAPE 1.0、W dist 0.5 初始、W pLDDT 0.2、W pTM 0.2）；未收敛靶用 soft starts（取收敛轨迹序列加突变并关闭 distogram loss 重启）；GPCR 活性态在 mini-Gs 存在下设计
computational_filters=AF2 复测（3 recycles + AMBER 力场 relaxation）后三闸口：TM-align TM score 相似度、pLDDT 置信度、BLAST e-value 新颖度（NCBI RefSeq 2022-10-01 库）；Foldseek 对 SCOP（2023-03）做折叠归属与"是否仅存在于膜环境"判定；Rosetta SASA 算表面疏水比例；相对接触序 RCO × 链长选难题靶；表位移植用 Foldseek 对 PDB 找兼容可溶骨架
thresholds=TM score 大于 0.80（rhomboid 单独降为 0.75）；pLDDT 大于 80（rhomboid 单独降为 75）；e-value 大于 0.1 视为足够 novel（图注另画 0.05 显著性参考线）；表位移植要求 pLDDT 大于 90 且对骨架 TM score 高于 0.7 后再人工检查；MPNN sol 训练集条件为 X-ray 或 cryo-EM 分辨率优于 3.5 Å、少于 10000 残基、剔除注释跨膜 PDB 条目；成功无统一数值判据（用可溶/单体/折叠/Tm 定性口径）
md_used=是（两处事后用途：一是作为骨架扰动多样性的对照组与 backrub、AF2 seq 并列比较，二是 cryo-EM 最终模型用 Namdinator 做 MD flexible fitting 精修；不参与设计决策、机理或自由能计算）
qm_used=否
experimental_methods=蛋白表达与纯化（宿主与细节在未取回的补充信息）→ SEC-MALS 判聚集态与分子量 → 变温 CD 与熔解曲线判折叠与 Tm → X-ray 晶体学（TBF_24 1.34 Å、CLF_4、RPF_9、GLF_18、GLF_32）→ pull-down 预筛嵌合体 → BLI（可溶 claudin 对 CpE）→ SPR（抗 ICL3 抗体、mini-Gs-414）→ cryo-EM 复合物结构（CLN4_20-cCpE-COP2 Fab-纳米抗体，FSC 截断 0.143）
pipeline_counts=正文只给送测与命中两级：IGF 19 送测 → 7 可溶 → 4 单分散；BBF 25 → 6 折叠单体；TBF 25 → 5 折叠单体；CLF 13 → 10 可溶 → 5 深做 → 3 单体；RPF 15 → 13 可溶 → 5 深做 → 3 单体；GLF 56 → 36 可溶 → 10 深做 → 9 单体；ghrelin 嵌合体 16 预筛 → 9 结合 → 5 做 SPR；生成总数与过滤后计数只在未取回的 Supplementary Table 1
hit_rate=作者口径为 high experimental success rates（可溶/折叠两级）；按可溶表达算 IGF 7/19（37%）、CLF 10/13（77%）、RPF 13/15（87%）、GLF 36/56（64%）；按折叠且单体算 IGF 4/19（21%）、BBF 6/25（24%）、TBF 5/25（20%）、GLF 深做 9/10（90%）；催化活性未测（正文无 activity 读数）；以上百分比为本卡按原文计数换算，非作者给出的比率
best_metric=结构侧：TBF_24 分辨率 1.34 Å，X 射线对设计模型 r.m.s.d. Cα 0.80 Å（CLF_4 0.73 Å、RPF_9 0.97 Å、GLF_18 1.05 Å、GLF_32 0.88 Å）；结合侧：ghrelin ICL3 嵌合体对单抗 Kd 150-790 nM；aGLF 对 mini-Gs 有结合信号但亲和力因快速动力学无法确定；无酶活数值
cost_or_stat_note=计算硬件为单张 Nvidia Tesla V100 32 GB；正文未给每条设计的 GPU-秒单价，也未给生成/过滤计数，故漏斗递减与单位成本无法从本文推算；送测规模每靶仅 13-56 条，成功率分母极小；rhomboid 与 GPCR 活性态需按靶定制阈值或外加结合伙伴
role_in_timeline=把 AF2 seq（2022 骨架生成）与 ProteinMPNN（2022 序列设计）串成通用的生成-设计-复测三段漏斗，并第一次把 claudin、rhomboid、GPCR 这类只在膜环境存在的折叠设计成可溶、高稳定、可结合的功能化骨架；同期与扩散模型骨架路线互补（本文提供不用对称/参数化约束的另一条路）；其 MPNN sol 重训是先例——性质不靠判据而靠训练分布注入
source_pointer=data/interim/baker_lit/ft/memprot_analogue2024.txt（Europe PMC fullTextXML 抽取文本，PMC11236705，PMID 38898281，本卡唯一逐字底稿）+ sources/baker.md（登记底稿，本卡未引用其措辞）
CSV回填-->
