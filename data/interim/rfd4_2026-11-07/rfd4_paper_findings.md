# RFD4-Proteina 预印本正文挖掘 — 事实台账

来源底稿: `RFD4_paper_text.txt` (116 页, 272,125 字符, `===== PAGE n =====` 分页; 正文 p1–21, 参考文献 p22–27, 补充材料 p28–116)
论文: *Biomolecular design through latent reasoning with RFD4-Proteina*, Corley/Didi/Kazman/Brent 等, Baker Lab × NVIDIA GenAIR, 2026 预印本。PAGE 1: "This preprint has not been peer reviewed."
证据三档: 【正文】= 正文原句; 【图表/补充】= 仅图注或补充材料; 【二手】= 两份 README; 推断单独标 `以下为推断`。
引句均为底稿抽取后真实连续字符串; PDF 抽取断行/断词处已注明。`˚A` 是 Å 的抽取形态, `107` 等是 10^7 的抽取形态, 照抄。

## 1. 湿实验验证台账

### 1.1 钙调蛋白 Ca2+ 构象态特异 binder 【正文+补充】
- PAGE 12: "12 showed calcium-dependent binding with a quantified apparent KD < 1 µM and no" (上行 "Of 18 designs tested,", 抽取断行)。分母=18 个测试设计, 分子=12 个钙依赖结合 (有钙 KD<1 µM 且无钙不可检出), 12/18=66.7% (PAGE 102 Table S31 明写 "Calcium-dependent hits: 12/18 (66.7%).")。
- PAGE 12: "calcium ranged from 69 pM to 37 nM (Supplementary Table S31)." 读数=BLI 表观 KD。
- 【图表/补充】PAGE 14 Fig.4a 注: "pM; 95% confidence interval, 3.4–92 pM" — 最佳 69 pM 的 CI; 估计合并独立重复。
- 测定边界【补充】PAGE 92: "the assay’s lower resolvable limit of 10−5 s−1 under the 300-s dissociation conditions." (原文弯撇号) — 最低两个 KD 估计的 koff 触到仪器分辨下限, KD 与 CI 以此为条件 (PAGE 92: "The affinity estimates and confidence intervals are conditional on this limit and do")。
- 表达=无细胞体系 (Adaptyv), 下单数=18, 未见"从更大池筛到 18"的选取规则 → 论文未给。

### 1.2 pMHC binder (MART-1 / SARS-CoV-1 / Phox2B) 【正文+补充】
- 工作流是**设计寡核苷酸库 → 酵母展示 FACS → 挑单克隆测序**, 不是逐个下单: PAGE 92: "For yeast surface display, all designed protein sequences were first padded at both ter-" (350 bp 寡核苷酸库, 统一 102 aa)。库容 (设计条数) 论文未给。
- PAGE 14: "concentrations of 340 pM, 710 pM, and 1.60 nM for binders targeting MART-1, SARS-" (抽取断行, 下接 CoV-1)。读数=酵母展示四聚体滴定表观半最大浓度, **带 avidity, 非溶液 Kd** (PAGE 103 Table S32: "half-maximal concentrations with avidity. A dash indicates an")。
- 分母口径【补充】PAGE 103 Table S32: 克隆水平表征, 测序单克隆数 SARS 30 / Phox2B 41 / MART-1 20; 例如 "SARS-CoV-1 (30 colonies sequenced)"。命中率按克隆计, 不按设计计。
- 特异性 PAGE 14: "over 100-fold specificity to the on-target in all cases. The off-targets for the Phox2B" — 对 6 个 pMHC 交叉筛 >100 倍; Phox2B/SARS 脱靶肽与靶肽仅差 1/2 个残基。
- 【补充】PAGE 104 Fig.24 注: "followed by two binding sorts with target and related off-target pMHC tetramers." — 表达排序 + 两轮结合排序 (靶标与近缘脱靶双色竞争)。

### 1.3 IDR 无序肽 binder (8 条肽, 每肽 94 个设计) 【正文+补充】
- PAGE 14: "mational reasoning could enable binder design against eight IDR peptides: five known" — 5 条结合时可成二级结构 + 3 条无倾向。
- 分母【补充】PAGE 105 Table S33: "Screening hits among 94 designs tested" (下行 "per target.")。逐靶标筛选命中: G3BP1 11/94, PAR2 16/94, YAP1 18/94, EA1 0/94, TDP-A1 0/94, N17 6/94, Tau-153 3/94, PER2 5/94。**EA1 与 TDP-A1 两个靶标零命中**。
- PAGE 14: "sity (Fig. 4c; Supplementary Fig. 25). We obtained tight binders against all but one" — 正文称每类"只差一个"; 与 Table S33 两个 0/94 存在口径张力 ("tight binder" 可能指 SPR 表征级命中而非筛选命中) → 未解决, 引用时以 Table S33 数字为准。
- 亲和力【图表】PAGE 14 Fig.4c 注: "lines show 1:1 kinetic fits (KD = 112 pM, 527 pM, 3.28 nM and 189 nM, respectively)." — YAP1/Tau153/N17/PER2 SPR Kd; 正文称 YAP1、Tau 所测表位的首个 de novo binder。
- 特异性: 5 条 IDR 肽 all-by-all SPR, 每对测一次 (PAGE 93), 各 binder 对靶标响应高于脱靶, 区分度不一。

### 1.4 Trk 家族 binder 【正文+补充】
- 无约束 hTrkA 结合: PAGE 15: "micromolar hits out of 188 designs collectively (84%) compared to 18/60 (30%) hits for" (上行 "yielding 158 sub-", 抽取断行)。分母=188 设计合计, 分子=158 亚微摩尔命中 (84%); 对照 Claude Mythos Preview 18/60 (30%)。
- 任务特异命中表【补充】PAGE 106 Table S34: 人特异 TrkA 68/94 (72.3%), 人/鼠跨反应 18/94 (19.1%), TrkB 1/94 (1.1%), TrkC 20/94 (21.3%, 仅筛选级)。命中定义: "an estimated KD < 1 µM; cross-reactive hits must meet this cutoff" (下行 "for both targets. TrkA hits also require an SPR response ≥20 RU")。
- 分母规则【补充】PAGE 106: "Denominators include transformation failures and exclude positive" (下行 "and buffer controls.") — 转化失败算分母, 对照不算。
- 以下为推断: 188 = 94 (人特异战役) + 94 (跨反应战役); 158 是两战役中"只要结合 hTrkA 就算"的宽松口径合计, 68+18=86 是"满足各自特异性约束"的严格口径。论文未给 158 的逐战役拆分。
- 人特异战役选择性证据仅 n=4: PAGE 15: "assayed the four strongest hTrkA binders against these off-targets, observing no" (下行 "binding in all cases.")。
- 跨反应战役: PAGE 15: "Of 94 designs, 18 exhibited the desired cross-reactivity and specificity patterns, with" — 最强 hTrkA 亚 nM, mTrkA 37.7 nM。
- TrkB/TrkC: PAGE 15: "obtaining one sub-micromolar hit to TrkB (30.2 nM) and 20 screening hits for TrkC" — 正文称两者均为首个计算设计 binder; TrkC 精确亲和力未测。

### 1.5 糖基化控制 (保留 Man9/Glc1Man9) 【正文+补充】
- PAGE 15: "MS/MS-detected structures, with 8/9 designs having >90% oligomannose on occupied" — 8/9 占位点 >90% 寡甘露糖。
- **分母口径实锤**【补充】PAGE 107 Fig.26 注: "ples; campaign hit rates were not assessed." (上行 "Counts describe the characterized sam-", 抽取断词)。9 个是 LC–MS/MS 表征子集 (对照: 97 个 RFDAA 基线 + 43 个 ΔRASA 过滤 RFDAA 谱), **不是战役命中率**; 初始 plate-scale screen 测了多少论文未给。
- PAGE 15: "RFDAA-based method, and an initial plate-scale screen yielded glycoproteins that" — 存在初筛; Expi293F 1 mL×4 表达 (PAGE 94)。
- 排除规则【补充】PAGE 107: 占用率 <5% 的谱与 F8 三聚体被排除 ("profiles below 5% occupancy and the F8 trimer are excluded.")。

### 1.6 磷酸化识别 binder (H3pS10 / H3pT11) 【正文+补充】
- PAGE 15: "histone H3 tail, pS10 and pT11, obtaining phosphorylation-dependent binders against" — 两位点均获磷酸化依赖 binder, 对相邻位点 (pS28) 磷酸化保持选择性。
- 工作流=设计库 → 酵母展示, 表达富集 + sort1 (500 nM 靶肽) + 竞争排序 (200 nM 未磷酸化诱饵/APC vs 100 nM 磷酸化靶/PE): PAGE 95: "at final peptide concentrations of 200 nM and 100 nM, respectively. Cells with high"。库容/设计数论文未给; 表征克隆: pS10 hit04, pT11 hit09/hit10 (PAGE 109)。
- 读数=酵母展示表观滴定 (图 5 中点 133/179 nM), 非溶液亲和力: PAGE 109 Fig.28 注: "show measurements and lines show Hill fits describing apparent binding in yeast display, rather than" (下行 "monovalent solution affinity.")。选择性读数为 NGS 富集, PAGE 110: "This enrichment-based readout is not a binding affinity."
- 多轮排序是文库选择轮, 不是设计轮: PAGE 95: "Selected populations were regrown and reinduced between rounds."

### 1.7 有机磷水解酶 PTE / paraoxon (双锌, 8 残基 theozyme) 【正文+补充】— 重点
- 计算筛: PAGE 17: "precise active site scaffolding (Fig. 6b). On this eight-residue theozyme, 15 of 1,000" + "RFD4-Proteina designs (1.5%) passed common motif-RMSD and substrate-confidence" — 15/1,000 (1.5%) 过 AF3 重预测双判据; RFD3 0/10,000。判据数值【图表】PAGE 19 Fig.6c 注: "and 18 substrate atoms for both models: motif RMSD < 1 ˚A and minimum protein–substrate PAE" (下行 "< 1.5 ˚A."), 用 47 motif 原子 + 18 底物原子。
- 湿实验: PAGE 17: "ing yielded 89 active RFD4-Proteina designs among 288 tested, spanning 25 of 47" (上行 "Experimental screen-", 抽取断词)。分母=288 测试设计 (3×96 eBlock 板, PAGE 96), 分子=89 活性 (31%), 覆盖 25/47 骨架家族; RFD3 平行对照 0/192。
- **分母口径关键**: 288 个下单设计 ≠ 15 个双判据通过者; 从生成池到 288 的选取规则论文未给 (S13.7 只说沿用先前 metallohydrolase 流程)。89/288 是测试池活性率, 不是全池命中率, 也不是计算通过者的湿实验转化率。
- 初筛读数: 洗脱液 405 nm 硝基酚释放, 600 µM paraoxon, 25 °C 1 h (PAGE 98); 活性事后按 A280 浓度归一。初筛缺陷自述【补充】PAGE 97: "sequence-verified and could be polyclonal." (上行 "These initial cultures were not"); PAGE 98: "Enzyme concentrations were not normalized" (初筛时未归一)。
- 表征: 6 个设计 (4 家族) 做稳态动力学; 最佳 PAGE 17: "kcat/KM = 3,600 ± 500 M−1 s−1 and kcat = 0.9 s−1, a 1.5 × 107-fold rate enhancement" — 较非催化水解提速 1.5×10^7 倍; 6 个全部超旧 6 残基 theozyme PTE 10–1,000 倍 (PAGE 17: "efficiencies of our earlier six-residue-theozyme phosphotriesterases by 10- to 1,000-fold")。动力学=3 技术重复×1 生物重复, Monte Carlo 误差传播 (PAGE 116)。
- **"第一轮就有活性"核对**: 正文没有与新闻稿 many designs active from the first round 对应的原句。可支撑的事实: 89/288 初筛有活性、无定向进化/亲和力成熟步骤描述、6 个直接进动力学。新闻稿是对 31% 测试池活性率的转述; 288 的选取口径未明, 模板引用必须带分母与"选取规则未给"注记。
- 锌蛋白酶: 本文无新锌蛋白酶湿实验。ZAPP-1/ZAPP-2 是已发表 RFD3 PTE, 仅作 Fig.6g 对比 (PAGE 19 注: "and the published RFD3 designs ZAPP-1"); p24 "Computational design of metalloproteases." 是引文标题。

### 1.8 连接酶 (lenacapavir API 酰胺合成步骤) 【正文+补充】
- PAGE 19: "obtained genes encoding 67 designs for experimental testing. Four of these showed clear" — 分母=67 下单设计, 分子=4 个明确高于背景的酰胺形成 (6.0%); RFD3 旧战役 0/72。
- 策略: PAGE 19: "alytic triad [57] with RFD4-Proteina (Fig. 6i) and using multi-state AF3 filtering to" (上行 "scaffolding a cysteine protease cat-", 抽取断词) — 半胱氨酸蛋白酶催化三联体 scaffolding + 多态 AF3 筛偏向氨解。
- 初筛细节【补充】PAGE 113 Fig.32 注: "enzyme buffer control (6.8 ± 0.4%). Teal bars mark the eight designs above 10% conversion (52, 58," (下行 "25, 47, 43, 54, 28 and 46); the next design reaches 8.9%.") — 8 个 >10% 转化 (无酶对照 6.8±0.4%), 正文"4 个"是更严格的"明确高于背景"口径; 两个口径都要记。
- 读数: UPLC 转化率, PAGE 19: "designs 52 and 58 converted 79.0% and 61.7% of the (S)-amine to amide, compared" — (R)-胺 8.8%/14.6%, 无酶 4.3%/6.2%; 16 h 30 °C 终点; CysKO 对照证明依赖设计 Cys。酸副产物 0.29 vs 无酶 0.26 mM (水解被抑制)。
- 定位【正文】PAGE 19: "first proof-of-concept demonstration of a de novo designed enzyme catalyzing a step" (下行 "in active pharmaceutical ingredient (API) synthesis.") — 首个 API 合成步骤 de novo 酶概念验证。

## 2. 多轮迭代

**结论: 论文未描述任何"第一轮→第二轮→第三轮"的序贯湿实验设计战役 (DBTL 循环)。** 逐条核对过的替代性事实:
1. **跨论文/spec 迭代 (PTE)**: RFD3 六残基 theozyme 效率低 (PAGE 17: "paratively low catalytic efficiencies (up to 4 ± 3 M−1 s−1) [6]. We hypothesized that", 上行末 "com-", 抽取断词) → 触发假设 PAGE 17: "adding two more catalytic residues could improve catalysis, but would require more" → RFD4 八残基 theozyme 新战役 (1,000 生成→15 过筛; 288 测试→89 活性→6 表征)。改的是**模型 (RFD3→RFD4) + 条件 spec (6→8 催化残基)**, 触发观察是旧酶催化效率低。这是跨代战役演进, 不是同模型多轮。
2. **平行战役 (Trk)**: 人特异 94 与跨反应 94 是不同 spec 的平行战役, 非序贯轮次 (Table S34)。188="collectively" 合计。
3. **文库内多轮排序 (pMHC/磷酸肽)**: sort1→sort2/竞争排序是酵母展示选择轮, 设计集合不变 (PAGE 95/104), 不属于设计迭代。
4. **计算性二次机会 (partial diffusion rescue)**: 对 RFD1 已发表失败设计做 partial diffusion 救活 100/102 (PAGE 12), 是"旧设计→精修"的计算流程, 无湿实验复测。
5. **论文提供的迭代机制 (工具, 非战役记录)**: 【补充】PAGE 56 Table S17 agent skill rfd4-proteina-autoresearch: "Runs iterative pilot experiments to compare" (下行 "design inputs, inference settings and search", 再下行 "rewards."); rfd4-proteina-commitment-curves: "Uses partial diffusion from a grid of restart steps" (测特征何时定型)。正文 PAGE 4: "In practice, we find that small-scale pilots are helpful in determining the best" (下行 "reasoning configurations for a given design challenge.") — 官方迭代建议=小规模 pilot 定推理配置, 再上生产。
- 以下为推断: 模板的多轮迭代节只能写成三种有证据的模式 — pilot 定配置、失败设计 partial diffusion 精修、跨代 spec 升级 — 不能写成"论文做了三轮战役"。

## 3. 论文实际用的计算筛选判据

### 3.1 四大基准 pass criteria (in silico 评测判据, 非湿实验下单筛) 【补充 S8.2, PAGE 72】
- 蛋白结合: "aligned binder backbone RMSD ≤2.5 ˚A, binder pTM ≥0.80, and minimum interface" (下行 "PAE ≤1.5 ˚A.")。靶标序列在生成中不得改变, 偏离即失败。
- 小分子结合: "ing designs require protein-backbone RMSD ≤1.5 ˚A, backbone-aligned ligand RMSD" (下行 "≤5 ˚A, protein-small molecule ipTM ≥0.80, and protein-small molecule minimum", 再下行 "interface PAE ≤1.5 ˚A.")。作者明言比原 DISCO 判据更严。
- 酶 scaffolding (AME): "require backbone RMSD ≤2 ˚A, motif all-atom RMSD ≤1.5 ˚A, and minimum interface" (下行 "PAE < 1.5 ˚A.")。作者改造了 RFD2 原判据: 加 min PAE<1.5 Å、删 clash 滤。
- DNA 结合: "require DNA-aligned binder backbone RMSD ≤8 ˚A and minimum interface PAE" (下行 "≤1.5 ˚A."); binder 长度改为 120–150 残基。
- 分母: 每靶标 200 次尝试, 失败留在分母 (PAGE 72: "Failed attempts and outputs with unmatched required motifs remain in the denomi-"); clustered pass rate=通过结构簇/200 (Foldseek TM-score 0.5, PAGE 89)。**计算通过率≠湿实验命中率。**

### 3.2 示例酶 (肽-DNA 键切割) 完整判据表 【补充 Table S21, PAGE 62】
- 生成结构侧: 粗接触对 ≥275; 总氢键 ≥18; DNA 氢键 ≥9; 肽氢键 ≥3; 1.5 Å 内重叠重原子=0; motif 映射完整正确; 联合 motif RMSD < 3 Å。
- AF3 侧: DNA 界面 min-iPAE < 2; 肽界面 min-iPAE < 2; binder 平均 pLDDT > 80; binder 骨架 RMSD < 1.5 Å; motif RMSD < 3 Å; 局部 DNA/肽骨架 RMSD < 3 Å。
- 引句 (表内连续行): "Target heavy atoms within 1.5 ˚A of any binder heavy atom" / "Binder mean pLDDT" 对应值 "> 80"。粗接触定义 PAGE 62: "A coarse contact is a binder Cα–peptide Cα or binder Cα–DNA C4′ pair separated by < 12 ˚"。
- 通过率 (Table S18, PAGE 61): naive 23,316 完成→3 通过; temporal search 4,057 完成→35 通过 (9 unique); 各 24 GPU-h。

### 3.3 酶+配体包埋 / 小分子相互作用加难判据 【补充, PAGE 63–65】
- 包埋任务 (Table S25): 常规判据 + 每个非单原子配体 AF3 包埋分数 > 0.85 (SASA 定义, ProtOr 半径 1.4 Å 探针)。中途继续条件 (Table S23): step25 motif RMSD<2 (包埋版另需 Burial≥0.80); step45 iPAEmin<3, AF3 motif RMSD<3, AF3 bb RMSD<3。
- 小分子相互作用 (Table S27): 未满足的氢键/π 堆积要求 ≤1 (每配体 5–18 个要求, RDKit 指派); step30 早停条件 m≤2。最终仍须 ipTM≥0.80、min PAE≤1.5 Å、BB RMSD≤1.5 Å、配体 RMSD≤5 Å。

### 3.4 湿实验战役实际筛子 【正文/图表】
- PTE: motif RMSD<1 Å + 蛋白-底物 min PAE<1.5 Å (Fig.6c, 见 1.7); 1.5% 通过。连接酶: motif RMSD<1 Å + 配体 pLDDT≥50 (PAGE 19 Fig.6j 注: "j, Computational success on the ligase task: motif RMSD < 1 ˚A and"; pLDDT≥50 为 PAGE 18 图内标签), 双判据 5.1% vs RFD3 0%; 另有多态 AF3 筛 (PAGE 19)。**从过筛池到下单 (288/67) 的选取规则论文未给** — 这是分母链缺口。
- binder 战役 (calmodulin/IDR/Trk/pMHC/磷酸肽/糖基化): 论文未给下单前的数值筛选阈值 → 论文未给, 模板不得把 3.1 基准判据冒充为这些战役的下单筛。

### 3.5 训练/数据构造参数, 不是筛子 (防误引)
- 32 维残基 latent (PAGE 3)、K=4 explorative modeling (PAGE 9: "set K = 4 and backpropagate through the candidate with the lowest combined coor-")、Dirichlet α=3 序列概率条件化 (PAGE 37: "remains a free parameter, set to α = 3 in RFD4-Proteina.")、酶活性位点样 tip-atom 约束采样 (PAGE 3) — 均为训练侧参数。
- 能量监督微调降 Rosetta 能量 1.07 kcal/mol/残基、键角偏差降 62% (PAGE 3) — 训练效果, 不是筛选阈值。

## 4. 序列设计这一步还在不在

- **共设计内置序列**: PAGE 8 Fig.2 注: "intrinsic sequence design and model-specific internal prediction but excludes downstream AF3 evalu-" — 吞吐已含内在序列设计。动机: RFD3 "high-quality sequences for its generated structures, limiting simultaneous optimiza-" (PAGE 3, 抽取断行)。
- **RFD4 自身可替代 inverse folding**: PAGE 11: "inverse folding tool by resampling side-chain identities while keeping the backbone" + "RFD4-Proteina consistently achieved higher pass rates than LigandMPNN at matched"。实现【补充】PAGE 86: "RFD4-Proteina was run by partial diffusion from the input backbone (t = 0.99)" + "with the sequence latents at t = 0 and 60 steps of the temporal-score-rescaled sampler," + "where the backbone is effectively fixed (Cα RMSD to the input below 0.4 ˚A)."
- **MPNN 的不可替代场景被内置**: 逐位残基概率条件化 (排除 Cys、活性位点指定电荷等), PAGE 37: "specify arbitrary position-wise residue-type probabilities." + "constraints such as avoiding cysteine residues that may impact expression in E. coli." + "ProteinMPNN that cannot remodel the backbone." (指 post-hoc 法无法回改骨架)。
- **MPNN 在论文中的实际角色=基线**: BindCraft 单骨架协议含一步 ProteinMPNN (PAGE 73: "tocol: one backbone-optimization trajectory followed by one ProteinMPNN sequence,"), Genie3 配 CA-MPNN, AlphaProtein-novo 有 LigandMPNN 重设计变体; 侧链 packing/inverse folding 对比用 LigandMPNN v1.1.1。**湿实验战役描述中未见任何 MPNN 步骤** (S13 全部为 RFD4 设计直接下单/建库)。
- 以下为推断: 模板"③ 序列设计"可改为可选步 — 默认共设计已含序列; 仅在需要 logit 级偏置且不想用 RFD4 条件化、或沿用旧骨架时才保留 MPNN。

## 5. reward-guided search 与 partial diffusion 的机制与代价

### 5.1 机制与参数 【正文+补充】
- 分阶段剪枝: PAGE 4: "At each checkpoint, we discontinue trajectories that" + "depart from the current criterion as they are unlikely to be rescued by subsequent steps."; 检查点按特征收敛时序 (界面面积~20%、氢键~50%、AF3 置信~80%, PAGE 4: "20%, 50%, and 80% of the way through generation, respectively.")。
- beam 参数 (肽-DNA 例, PAGE 61): "use the same beam-search parameters: beam width one, a branching factor of two at" (下行 "steps 13 and 37, and a branching factor of four at step 45"); 可中途终止 (PAGE 61: "trajectory termination if none of the branches meet the continuation criteria."); 打分可用完成 rollout 或单步 Euler 预测 (PAGE 61: "thermore, temporal search can score either a completed rollout, or a single-step Euler")。
- 酶包埋任务 (PAGE 63): "branches per root and retained one candidate; surviving trajectories then completed" (steps 25/45 各 2 分支留 1)。SAM 蛋白氢键消融 (Table S16, PAGE 54): "runs, beam width two, branching factor two, and checkpoints at 25% and 50% of integration steps,"。
- oracle: search 期间蛋白结合用 AF2-Multimer, 小分子/AME/DNA 用 OpenFold3 (PAGE 78: "RFD4-Proteina search uses AF2-Multimer for protein binding and OpenFold3 [100]"); 最终统一 AF3 评测另计; 能量 oracle=TMol (可微 Rosetta, PAGE 20)。奖励=各指标 clip 到有界区间后加权求和 (PAGE 61 公式)。
### 5.2 代价与收益边界 【正文+补充】
- 示例酶 3 倍效率: PAGE 4: "cleaving enzyme yielded three times as many unique passing designs per GPU-hour" (Table S18: 0.38 vs 0.13 unique passers/GPU-h, 各 24 GPU-h)。
- 加难任务收益: 酶包埋 +22.6% (PAGE 63: "the highest observed yield; with burial, temporal search yielded 22.6% more passing", 下行 "clusters per GPU-hour than naive sampling (Table S22)."); 小分子相互作用 +24.6% (PAGE 65: "With a compute budget of 4 GPU-hours per target, search yielded 674 unique")。
- **标准基准上 search 反而降效**: PAGE 78: "benchmark criteria reduced passing-cluster yield per GPU-hour." (Table S29: 蛋白结合 high-thinking 66.5 → search 8.4 clusters/GPU-h, 尽管通过率 10.6%→14.9%)。正文 PAGE 9: "late in the trajectory, we found that the efficiency gains from search do not outweigh" (下行 "the computational overhead")。
- 加速措施【补充】PAGE 78: 常驻 worker 保留已加载模型、按 padding 长度编译、输入预取 (S8.7)。
### 5.3 partial diffusion 数值与用途 【补充】
- 救活失败 binder: fraction 0.9, 每父本 6 次 (PAGE 88: "(fraction 0.9) per parent, compared with the first six HalluDesign outputs and six"); 对象=146 个已发表不结合 RFD1 设计中过不了现代 AF3 筛的 102 个 (PAGE 87: "Of 146 published non-binding RFdiffusion designs, 102 failed the common AF3 filter:"); 筛子 PAGE 87: "chain-of-interest pTM ≥0.80, minimum interface PAE ≤1.5 ˚A and target-aligned" (下行 "binder backbone RMSD ≤2.5 ˚A.")。结果 100/102 救活 (PAGE 12)。**PAGE 88: "These outcomes are computational, not experimental binding measurements."**
- 柔性骨架界面重设计: fraction 0.5 + TMol 引导 beam search (PAGE 87: "using partial diffusion (fraction 0.5) and TMol-guided beam search."); 序列改动限界面 8 Å (固定版) / 12 Å (柔性版) 内。
- 固定骨架补序列: t=0.99 (见第 4 节)。特征定型测量: 从重启步网格做 partial diffusion (Table S17 commitment-curves)。
- 用途结论: 精修/救活/补序列/多样化 (侧链 packing 噪声 0.3–15 扫描) 均有实例; 未见"噪声强度-成功率"系统曲线用于 de novo 主战役。

## 6. 算力与可及性

- 采样步数/recycle【补充】PAGE 73: "For RFD4-Proteina, all three thinking levels use 60 denoising steps, with task-"; 蛋白结合总 trunk passes 120/180/300 (low/med/high): "specific schedules for recurrent refinement. Protein binding uses 120, 180 and 300 total"; 小分子/酶 120/150/180, DNA high=每步 5 次共 300 (PAGE 73: "150 and 180 passes, concentrated at intermediate steps. DNA binding uses the same")。
- 吞吐【正文】PAGE 8: "2,388 with low-thinking to 986 with high-thinking." (蛋白 binder designs/GPU-h, 不含 AF3); 含 AF3 每 GPU-h 通过簇 66.5 (蛋白) / 237.1 (小分子) / 155.2 (AME) / 52.3 (DNA) (PAGE 7 图内)。
- 训练算力【补充】PAGE 49: "Complete training of the autoencoder required ∼4,000 GPU hours on NVIDIA H200s."; 发布模型预训练 ~16,000 H200 GPU-h (320k 步, K=4) + LoRA 微调 ~2,000 GPU-h (PAGE 50: "model for another ∼2,000 GPU-hours with low-rank adaptation (LoRA) with rank 32,"); 消融在 16×H200 (PAGE 47: "All ablation runs—and baselines—are trained on 16 H200 NVIDIA GPUs; training")。
- **论文算力数字的版本归属**: Table S11 (PAGE 50) 的 10.6/14.3/12.1/3.5% 对应 K=4 release-scale 模型 (~18,000 GPU-h, 含微调), 即发布权重; 正文所有基准/实验数字均属此版。
- 训练数据截断【补充】PAGE 31: "Experimental structures used for training were restricted to those deposited before" (下行 "1 January 2024.")。另有 ESMFold2/TCR 等蒸馏数据 (PAGE 31)。
- 硬件门槛【二手, HF_RFD4-Proteina_README.md L242–251】: 权重 FP32 1.74 GB; 峰值显存取决于 token 数、batch size 与 recycle 深度而非权重本身; 实测 GPU 覆盖 Blackwell (B200/GB200/RTX PRO 6000/GB10) 到 Ampere (A100 40/80GB), Linux x86_64 + Python 3.12 + CUDA 13 驱动; 有 ZeroGPU 与专用 GPU 两种 HF Studio; 输入与设计过 SecureDNA 筛查 (L159)。
- **HF 效率表版本警告**【二手, HF_RFD4-Proteina_README.md L255, 转述非引句】: 该表自称测自上一版权重对 (previous release pair), 基准为 2026-10-09 冻结的项目基准, 早于当前 checkpoint, 未在当前版本重测, 不应读作描述当前版本。HF 效率表≠当前权重性能; 论文数字才是发布版实测。
- 代码/权重: PAGE 20: "Source code is available at https://github.com/RosettaCommons/RFD4-Proteina." (宽松许可, 含数据处理/训练/推理代码与权重)。

## 7. 作者自述的局限与失败模式

- 计算指标≠实验成功的自认: PAGE 20: "In cases where existing computational metrics have not yet" + "translated to experimental success, the ability to generate diverse candidates meeting" — RFD4 被定位为检验新筛选假设的基础, 不保证湿实验转化。
- search 开销边界: PAGE 9 (见 5.2); 标准基准上 search 降效 (Table S29)。
- 失败任务如实报告: IDR 靶标 EA1、TDP-A1 各 0/94 (Table S33); TrkB 1/94; TrkC 亲和力未测; RFD3 对照 PTE 0/192、连接酶 0/72。失败归因: 论文未给 EA1/TDP-A1/TrkB 的机制性归因 → 论文未给。
- 无"某类靶标不适用"的一般性声明; 最接近的是推理配置需按任务 pilot (PAGE 4) 与 search 只在难任务划算 (PAGE 9)。
- 表征子集≠战役命中率: 糖基化 PAGE 107: "ples; campaign hit rates were not assessed."; rescue PAGE 88: "These outcomes are computational, not experimental binding measurements."
- 统计自限【补充】: retroaldolase AUROC 0.90 vs PLACER 0.82, 但 PAGE 87: "The main-panel intermediate was selected retrospectively." + "paired intervals do not establish a method advantage."; HBDesigner 柔性 vs 固定比较 PAGE 87: "isolate backbone flexibility. This measures predicted partner separation; the flexible" (上行末 "Fixed", 完整句跨行: 固定/柔性配方的 recycling 与打分也不同, 比较不能孤立骨架柔性因素), 且柔性 RFD4 vs HBDesigner 区间含零。
- 测定局限: calmodulin 最低 KD 受 koff 分辨下限条件化 (PAGE 92, 见 1.1); PTE 初筛培养物未测序验证、可能多克隆、酶浓未归一 (PAGE 97–98); pMHC/磷酸肽读数为 avidity/富集而非溶液亲和力 (PAGE 103/109/110)。
- 阴性/机制对照清单: 连接酶无酶对照 + CysKO (Fig.6m,n, PAGE 114 原始色谱无基线校正展示); PTE RFD3 平行 0/192 + 无酶背景扣除; calmodulin EDTA/无钙 + 非结合 ligand 对照 (PAGE 92); pMHC 脱靶四聚体竞争; IDR all-by-all; 糖基化 RFDAA 历史对照谱。
- 基准适配自述: AME 41 任务剔除 4 个 (3 个共价加合物需未索引修饰残基支持, 1 个缺磷酸原子坐标, PAGE 72); 小分子判据严于原 DISCO; DNA binder 长度改 120–150。