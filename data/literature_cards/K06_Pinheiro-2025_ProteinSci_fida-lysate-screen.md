# [K06] 用 FIDA(流散分析)在未纯化裂解液里一步筛查 de novo 结合蛋白——把"筛几百个候选"的湿实验瓶颈做短

Pinheiro F, Nowak JS, Zueva E, Pheasant EC, Grene IK, Lampinen V, Kjaerga M（奥胡斯大学 MBG / PROMEMO / DANDRITE）
Protein Science 2025, 34(10): e70286 · DOI 10.1002/pro.70286 · PMID 40944422 · PMCID PMC12432402
开放获取（CC BY 4.0）· https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12432402/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K06**（组：通用方法学; 口径对照） |
| 论文类型 | Methods and Applications（方法学短文，非新功能蛋白报道）——它的贡献是**筛查手段**，不是设计算法本身 |
| 本文取回方式 | PMC JATS→text 抽取（本目录同时存有 XML 与纯文本两份，同一 PMC 记录，非双通路互证） |
| 本地全文①（本卡逐字比对底稿） | `data/literature_cards/fulltext/K06_PMC12432402_text.txt`（56,593 B，去标签纯文本；本卡所有引句以此为唯一比对源） |
| 本地全文②（同源 XML） | `data/literature_cards/fulltext/K06_PMC12432402_fullTextXML.xml`（97,988 B，未在本卡逐字比对中使用） |
| 对照底稿 | `sources/cost-benchmarks.md`（state=FULLTEXT，正文已完整读入，不依赖底稿写作） |
| 证据级别 | **全文级**（本卡全部引句均可在 `K06_PMC12432402_text.txt` 里逐字命中；见第 9 节自检） |
| 未取到的部分 | 补充图 FIGURE S1–S6、TABLE S1/S2 的原表数字（正文只在文字里点名 Table S1/S2，未展开）；protocols.io 上的操作细节。凡涉及这些处本卡明写"仅正文描述，补充材料未取" |

## 1. 这篇到底解决什么（大白话）

de novo 设计（RFdiffusion + ProteinMPNN）已经能一批批造出候选结合蛋白，但"设计出来"和"确认它真的结合、而且亲和力够用"之间隔着湿实验：传统做法要 Ni-NTA 纯化、再上 BLI 单点测，几百个候选一个一个过，费人费设备。这篇不谈怎么设计，专攻**怎么把筛选这一步做快做省**：把一种叫 FIDA（flow-induced dispersion analysis，流致分散分析）的微流控技术拿来当筛子。FIDA 的原理是给靶标（indicator）打上荧光，让它跑过一根毛细管，用 Taylor 扩散分析测出它的**流体动力学半径 Rh**；一旦靶标被结合蛋白抓住，复合物变大、扩散变慢、峰变宽、Rh 上升——于是"结合与否"变成一个**体积/尺寸读数**，不需要把靶标固定在传感器上。作者拿两个尺度差很多的靶做验证：2 kDa 的 α-螺旋短肽 **ALFA-tag**，和 34 kDa 球状的 **PSD-95 GK 结构域**（用 SH3-GK 双结构域模块）。核心卖点是：候选蛋白**不用纯化**，直接把细菌裂解液（尤其是加热裂解液）热处理、稀释后就能测，一次 capmix 测量给出结合/不结合，表达后约 1 天内就能定初筛命中。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **湿实验本身才是瓶颈，不是设计算法**。作者开篇定位："identifying binders with sufficient affinity still requires biochemical screening of many designs"，并给出量级："binder design projects still require the screening of tens to hundreds of candidates"。→ 纯化和 BLI 一道一道过是耗时耗钱的主因。 **应对**：整个方法学改赌 FIDA——免固定化、免纯化、单点读数，把筛选从"过柱 + 上样"压成"裂解液稀释后跑一次毛细管"。
2. **裂解液自发荧光高，一次带来两个具体故障**。原句 "Bacterial cell lysates exhibit high autofluorescence"。作者拆成两难：① 背景抬高，必须把 indicator 浓度从纯蛋白实验用的 50 nM 提到 200 nM 才保住信噪比 S/N > 50；② capmix 里裂解液（脏基线）与 indicator（干净缓冲）基线不一致，会扭曲 Taylor 峰形、污染 Rh 读数。 **应对**：给出三条消解路径——(i) 再把 indicator 提浓到失真可忽略、(ii) 分析前先把裂解液与 indicator 预混、(iii) 用干净缓冲稀释裂解液压低自发荧光。作者明确选了 (iii)，理由是它在时间、样品消耗、装置简单性上最优；低稀释因子还会因黏度造成 Rh 假性升高，他们用相对保留时间估黏度再做扩散率归一化校正。
3. **判命中用统计显著还是固定百分比，两种都会翻车**。先用 2 路 ANOVA 做 Dunnett 多重比较：对去污剂裂解液几乎所有 Rh 都相对前培养对照显著偏高——因阴性对照方差极小，微小变化即"显著"。作者判定 "In this case, the significance test becomes too permissive and so we explored more stringent criteria."。 **应对**：改用两套判据并按靶选择——ALFA 这种大尺寸跳变的靶用固定阈值（相对单独 indicator 的 Rh 增加 ≥10% 判阳性）；GK 这种预期变化小的靶反过来不能用固定 10%（否则连 K_D 44 nM 的高亲和结合体 3B 都会被漏，见 §3/§4），改用相对空白裂解液的显著性检验。最终把两个主观旋钮（稀释因子 + Rh 阈值）交给逐案优化：先用 30 倍稀释把假阳性压到 0，同时不牺牲真阳性。
4. **FIDA 靠尺寸变化测结合，天生对大靶标不敏感**。作者自陈 "The most important limitation of screening using FIDA is its reliance on size change to assess binding."，并补 "This works well when the binder is approximately the same size as the target."。量化对比：ALFA 结合后预期 Rh 变化 80%-113%，GK 只有 9%-22%（最小 7.9%）。 **应对**：主张上机前先由预测复合物结构估算预期 Rh 变化，据此判断 FIDA 合不合适；对预期变化小的 GK，判据从固定百分比切换到统计显著性。作者还展望新一代 FIDA 探测器加入光谱读数（发射波长/强度变化）与长波长荧光团（自发荧光更低）以缓解这一硬伤——但那是本文之外的能力。
5. **免纯化=不做表达量归一，会漏掉高亲和但低表达的结合体**。作者承认 "the absence of normalization to protein expression levels means that high‐affinity binders with poor expression might be missed"；实测中 GK 的 binder 5A（低微摩尔亲和力）就被漏了，归因 "likely due to its very low expression level"。 **应对**：给一个务实折中——对处在检测阈值附近的候选补测表达量，只把低表达者纳入后续纯化复测。作者把这叫 pick-the-winners：接受单点裂解液筛会漏一些真命中，换取通量。
6. **热裂解顺带筛选了热稳定，可能误伤不耐热的复杂设计**。原文 "it inherently selects for both binding and heat stability"，对小螺旋束友好，但可能排除非耐热的更复杂 binder。 **应对**：这类改用去污剂（chemical）裂解液，代价是要纯化并滴定更多结合体、且去污剂裂解液假阳性率在各稀释度都高下不来（见 §4：热裂解 1:30 与 1:100 时假阳性降到 0，去污剂始终偏高）。

## 3. 方法与工作流程（输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **设计端（沿用他人管线，非本文创新）**：RFdiffusion 出骨架 + ProteinMPNN 出序列（Dauparas 2022 / Watson 2023），设计复合体再用 **AlphaFold2（ALFA）或 AlphaFold3（SH3-GK）** 预测打分，取 **pAE interaction**（链间残基对的 predicted aligned error）当计算闸口；预期 Rh 由预测复合物结构经 FIDA 软件内 PDB correlator 算出。
- **筛查端（本文主角）FIDA**：微流控 + Taylor 扩散分析，测荧光标记靶标（indicator）及其复合物的**流体动力学半径 Rh**；结合→复合物变大→扩散变慢→峰变宽→Rh 上升。免固定化、免纯化、单次 capmix 测量。
- **样品前处理**：两种细菌裂解方式——化学（B-PER 去污剂）与热（95°C 加热）；热处理既碎细胞又沉淀宿主蛋白、失活蛋白酶，顺带富集耐热的设计蛋白。配套一个中通量流程（24/96 孔板 + 96 孔加热模块 + 96 孔滤板离心）。
- **亲和力定量**：FIDA 滴定曲线拟 1:1 结合模型算 K_D；对照方法在正文里点名的是 BLI（单点、需固定化、假阳高），本文只作定性比较、没做头对头 BLI 实验。
- **没有用的方法**：MD、QM、自由能微扰、深度突变扫描、展示文库（噬菌体/酵母/mRNA display）——全文不含这些；作者在结论里只是"展望"FIDA 也可用于筛选那些展示法产生的结合体，但本文未实测。
- **统计判据**：one-way / two-way ANOVA + Dunnett 多重比较（GraphPad Prism 10.5.0），p<0.05/0.01/0.001 三档显著性。

### A. 设计与计算过滤（两个靶各走一遍）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1-ALFA | ALFA-tag:nanobody 复合物 PDB 里 ALFA 坐标作 RFdiffusion 模板；表位取 L4/L8/L12 三疏水残基 + R3/R10 精氨酸放大界面 | RFdiffusion 设计 + AF2 复合预测打分 | "resulting in an in silico success rate of about 5% with a threshold of pAE interaction < 10"；pAE interaction<7 的折叠才细看，只有两螺旋的折叠因稳定性/界面尺寸担忧被剔 | "The remaining folds were resampled 300 times in proteinMPNN, and for each of the top 5 folds, the two sequences with the lowest pAE interaction were selected for characterization" ⇒ 合成 **10 条**候选（密码子优化、N 端 thrombin 可切 His-tag） |
| A2-GK | PSD-95 GK:phospho-SAPAP 晶体结构的 GK 坐标作 RFdiffusion 输入；靶残基 L552/Y580/Y604/Y609（某次设计再加 L680）+ R568/R571 | 按 ALFA 同样流程设计与打分（SH3-GK 用 AF3 预测复合体） | "resulting in a 7.7% in silico success rate prior to proteinMPNN resampling"；取六个多样折叠里 pAE interaction 最低的两条序列 | **12 条**候选（6 折叠 × 2 序列，命名 1A–6B） |
| A3 | 10+12 条设计 | E. coli BL21(DE3)、ZYM-5052 自诱导、37°C 20–22 h 表达；化学或热裂解 + Ni-NTA 重力柱一步洗脱 + 透析（ALFA 再 thrombin 切 tag） | 可溶表达 & 能纯化即算过 | "All 10 binders resulted in soluble expression and proteins that could be purified, although with varied yield (3-148 mg protein per liter of culture)"（产量跨度约 50 倍） |

### B. FIDA 湿实验工作流（纯化 → 裂解液直筛 → 滴定定 K_D）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | FIDA1 仪器；永久涂层毛细管（内径 75 μm、总长 1 m、到检测窗 84 cm）；assay 缓冲 20 mM 磷酸钠 pH7.6 + 300 mM NaCl + 0.05% pluronic F-127 | LED 荧光（激发 480 nm / 发射>515 nm），capmix 四步自动序列：75 s 3500 mbar 预平衡 → 20 s 3500 mbar 进 analyte → 10 s 50 mbar 进 indicator → 180 s 400 mbar 进 analyte（末步记录数据）；复孔三次 | Rh 由 FIDA 软件 v3.1 取 Taylorgram fraction 75% 拟合；反应时间 <1.8 min（缔合慢的结合体可能测不到） | 单个测量 ≈ 一次 capmix，3 复孔 |
| B2-筛纯化 ALFA | 纯化的 10 条 ALFA 结合体 | 步骤 2/4 载 10 μM 结合体、步骤 3 载 50 nM FITC-ALFA | Rh 相对单独 FITC-ALFA（实测 1.15 nm，预测约 1 nm）增加 **≥10%** 判阳性 | 命中 **1A/1B/5A/5B**（1B 误差偏大存疑） |
| B3-热稳 | 同上结合体 | 上机前 95°C 加热 5 min 再做 FIDA | 加热后仍能抬高 Rh = 既结合又耐热（或不聚集体重折叠） | 保留 **1A/5A/5B**；1B 掉下（易受热或初筛假阳） |
| B4-滴定 ALFA | 3 阳性 + 2 阴性（3A/4A）纯化体 | 约 100 μM 起 2 倍系列稀释到 0.1 μM，拟 1:1 模型 | 复合体 Rh 与预测值差在 0.2 nm 内（PDB correlator 报 ~9% 误差） | K_D：1A、5A、5B 分别 **10.0 / 2.76 / 5.71 μM**（微摩尔级）；阴性对照 K_D 高或测不出 |
| B5-裂解液直筛 | 化学/热裂解上清 | 指示剂提到 200 nM 保 S/N>50；1:2→1:100 系列稀释降自发荧光；用相对保留时间估黏度校正 Rh；加不含结合体的前培养（PC）对照 | ALFA 沿用固定 10% Rh 增量（相对 PC） | 化学与热裂解下都能把已验证结合体全部识别；"However, the false positive rate was highly dependent on the lysis method and dilution factor"——去污剂各稀释度假阳性都高，热裂解在 **1:30 与 1:100** 假阳性降到 **0** |
| B6-筛 GK | 热裂解 1:30 稀释 + 200 nM AF488-SH3-GK（实测 Rh 2.96 nm，预测无标记 2.86 nm） | 因预期 Rh 变化小（最小 7.9%），**不**用固定 10%，改用相对 PC 的显著性检验 | one-way ANOVA Dunnett，p<0.05/0.001 判阳性 | 命中 **3A/3B/5B**；纯化复测 K_D **646 / 44.1 / 727 nM**（纳摩尔级，比 ALFA 强一个量级）；binder 5A（低微摩尔亲和力）被漏，归因低表达 |
| B7-中通量 | 2 mL 培养、24 孔板 | 96 孔加热模块热裂解（**最多 96 个培养并行**）+ 96 孔滤板离心除去热敏感宿主蛋白 | 直接得高纯裂解液供 FIDA，免过柱 | 一套可复制的 protocols.io 流程（Grene 2025 / Nowak 2025），把"表达→可测"压到 1 天内 |

**这套流程的骨架值得单独记住**：设计端阈值（pAE interaction<10、<7、剔除两螺旋）与 B09 一脉相承，本文真正的新东西全在湿实验端——把"要不要纯化""用什么判据算命中（固定 10% vs 显著性）""用哪种裂解（化学 vs 热）""稀释到几倍"四件事当成可调旋钮系统扫描，然后给出一句可操作结论：**一次 capmix + 30 倍稀释热裂解液 = 假阳性归零且不漏真阳**。它给的不是命中率，是**单位筛选成本与流程步数**。

## 4. 关键数字台账（数值 · 含义 · 出处）

| 数值 | 含义 | 出处（原句/位置） |
|---|---|---|
| 19% @ 10 μM（5 靶平均） | 引用 Watson 2023 背景：RFdiffusion+ProteinMPNN 候选显示结合的平均比例 | 引言正文叙述 |
| tens to hundreds of candidates | 每个结合体设计项目仍需筛的候选数 | 见第 2.1 节引句 |
| pAE interaction < 10 | ALFA 设计 AF2 复合打分计算闸口，对应 ~5% in silico 成功 | "with a threshold of pAE interaction < 10" |
| pAE interaction < 7 | 低于此值的折叠才被人工细看 | "Folds with pAE interaction below 7 were inspected" |
| 300× | 剩余折叠在 ProteinMPNN 里重采样次数 | "resampled 300 times in proteinMPNN" |
| ~5% / 7.7% | ALFA / GK 的设计端 in silico 成功率 | 见 §3 表 A1/A2 |
| 10 条 / 12 条 | ALFA / GK 送实验的候选数（6 折叠×2） | §3 表 A1/A2 |
| 3–148 mg/L | ALFA 结合体纯化产量跨度 | "with varied yield (3-148 mg protein per liter of culture)" |
| 50 nM → 200 nM | indicator 浓度（纯化缓冲 → 裂解液，为保 S/N>50） | §2.2 / §3 表 B5 |
| 1.15 nm | 单独 FITC-ALFA 实测 Rh（预测约 1 nm） | §3 表 B2 |
| ≥10% Rh 增量 | ALFA 结合判定的固定阈值（相对单独/PC） | §2.3 / §3 表 B2 |
| 10.0 / 2.76 / 5.71 μM | 1A / 5A / 5B 对 ALFA 的 K_D（微摩尔级） | §3 表 B4 |
| 9%–22%（最小 7.9%） | GK 结合后预期 Rh 变化（远小于 ALFA 80%–113%） | §2.4 / §3 表 B6 |
| 2.96 nm（预测 2.86） | 单独 AF488-SH3-GK 实测 Rh | §3 表 B6 |
| 646 / 44.1 / 727 nM | 3A / 3B / 5B 对 SH3-GK 的 K_D（纳摩尔级） | §3 表 B6 |
| 1:30 与 1:100 | 热裂解下假阳性降为 0 的稀释度 | §3 表 B5 |
| 最多 96 个并行 | 96 孔加热模块一次热裂解的培养数 | §3 表 B7 |
| ~1 天 | 从表达到定初筛命中的时间 | 摘要 / 结论叙述 |
| ~9% | PDB correlator 预测 Rh 的报告误差 | §3 表 B4 |

（注：以上 K_D、Rh、mg/L 等数值均取自正文；正文未把每个候选完整列成表，逐条对应见 Table S1/S2 原表，本卡未取补充材料。）

## 5. 结论——作者说了什么

1. FIDA 能在**一次测量、直接在细菌裂解液里**（尤其热裂解）检出 de novo 结合体，无需纯化，"allowing the identification of positive hits within 1 day of protein expression and with low material consumption"。
2. 最优筛查方案是"一次 capmix + 30 倍稀释热裂解液"：能把假阳性全部排除又不牺牲真阳性。
3. ALFA（小肽）给出微摩尔级 K_D、GK（大结构域）给出纳摩尔级 K_D，FIDA 的 sigmoid 结合曲线说明检出的是**特异、可饱和**的相互作用，排除了非特异。
4. FIDA 相对 BLI 的差异是正交的：它不需要固定化靶标、能给复合物尺寸/化学计量/异质性等额外质量控信息。
5. 作者自限：判据的两旋钮（稀释因子、Rh 阈值）主观、须逐案优化；筛 GK 这类"预期尺寸变化小"的靶敏感度受限；低表达的高亲和结合体可能被漏（binder 5A）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇把"漏斗末端"当成工程问题而非概率问题**：它不提新算法、不追求更高命中率，而是把"确认一个候选要不要几步、多少样品、多长时间"量化成可调参数。→ 对我们：酶设计筛选的瓶颈很可能同样不在"设计出候选"，而在"每个候选要付出多少湿实验成本才能判生死"，该学它把成本步数做成显式旋钮。
2. **"判阳性的阈值必须随靶的预期信号幅度重定"**。同一套 FIDA，ALFA 用固定 10%、GK 必须改用显著性，否则漏掉 44 nM 的真结合体——这是"一把阈值不能跨靶复用"的具体证据。→ 对应我们：不能拿一个 pLDDT / pAE / 打分阈值套所有目标反应类型（分步化学事件信号本底不同）。
3. **免纯化=拿表达量信息换通量**，代价是漏低表达高亲和者。这是明确的 trade-off，不是纯赢。→ 提醒我们：任何"省一步纯化/省一步对照"的加速，都要标出它牺牲了哪一类真命中。
4. **"pick-the-winners"承认了筛查会漏**，并把漏的部分转成"对阈值附近候选回补表达量"。这比声称"我们的筛子全召回"诚实。
5. 尺寸/体积读数（Rh）是**结合层**的正交 QC，不直接反映亲和力强弱；亲和力仍要靠滴定另测。→ 对我们：结构自洽类读数只能当"复合物按预期形成"的旁证，不能当催化活性的判据。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：① FIDA 靠尺寸变化，"The most important limitation of screening using FIDA is its reliance on size change to assess binding."，对大靶敏感度差；② 热裂解会误筛不耐热设计；③ 不做表达量归一会漏低表达高亲和者；④ 稀释因子与 Rh 阈值两个主观旋钮需逐案调；⑤ 显著性检验要严格就得多个生物学重复，反过来牺牲通量（他们退而用技术重复 + 对小幅显著 Rh 存疑）。
- 我们读出：① 全篇只 **2 个靶、10+12 个候选**，"1 天出命中"是流程步数口径、不是统计意义上的召回率，不能当"筛子多可靠"的概率引用；② GK 的 44 nM 结合体在裂解液单筛里能过靠的是改用显著性判据——若机械套用 10% 阈值就漏，说明"假阳性归零"是在特定靶特定稀释度下才成立；③ 无 BLI/SPR 头对头对照，FIDA 优于 BLI 属作者定性主张；④ 无 MD/QM，本文对"为什么结合/催化"不给机理层解释，机理结论不在其证据范围内。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么做）**

1. **把"单位候选的湿实验成本/步数"当一等公民**（本库效率口径）：像本文把纯化步数、样品体积、"表达→判定"天数摆到台面上一样，我们的每个筛选漏斗判据都应附带"过闸口前要付出几步湿实验"，再决定是否纳入。
2. **阈值随靶重定 + 双判据并存**：固定百分比阈值与显著性检验两条都要备，按目标信号幅度（对酶设计：产物信号相对本底的抬升幅度）选用，并显式写出"用固定阈值会漏哪一档"。这与 B09 的"效率=通过率÷单价"是同一思路的湿实验版。
3. **免纯化的粗样品直筛思路**（若对应分析可兼容）：目标酶若走 LC-MS/MS 产物读出，可评估"能否跳过纯酶、直接用粗裂解液 + 空白前培养对照扣本底"来提通量——照搬其"PC 对照处理非特异"的对照设计。
4. **正交的结构性 QC**：用与亲和力不同的观测量（本文是尺寸）交叉验证命中，降低单一读数的假阳。对酶设计可用"产物身份 + 计量比/化学计量"作旁证，而非只看一个峰面积。

**不可迁移（为什么不能照搬）**

1. **这是结合体（binder）筛查，不是酶活筛查**。FIDA 判的是"复合物有没有按预期形成（尺寸变化）"，不判"有没有让底物氨酰化/催化了化学反应"。本库判据 §2 明令：不许把 binder 的 pAE/ipTM、尺寸读数、结合 K_D 当成酶活判据或成功概率。这里没有一条能改写成催化判据。
2. **它没有任何 MD/QM/自由能**，所以不能为"用 MD/QM 判催化"提供命中率背书（本文无相关证据，要另找参照）。
3. **"1 天出命中 / 假阳性归零"是在 2 靶、10+12 候选、特定稀释度下得到的小样本工程结论，不是可外推的召回率或命中率**。不许把它换算成"酶设计筛选成功率 X%"，那属于凭空编造。
4. **它靠尺寸变化这一物理前提，对"催化一个化学事件后分子大小几乎不变"的目标反应根本不成立**——氨酰化 tRNA/UTP 转化这类事件不产生 ALFA-tag 那种 80%–113% 的相对尺寸跳变，FIDA 式单点尺寸读数在这里既非必要也不充分。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K06_PMC12432402_text.txt

- 本地纯文本：`fulltext/K06_PMC12432402_text.txt`（PMC 抽取、标签剥离、未改写内容；同一记录另有 `K06_PMC12432402_fullTextXML.xml`，本卡逐字比对只声明并只使用上述 .txt 一份，避免抽取版本差异误判）。
- CSV 字段映射：本文第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- 本卡为**方法学短文**：核心可迁移件是"筛漏斗末端的湿实验成本与判据旋钮"，不是命中率数字；引用时只许引方法结构，不许引"1 天/假阳性归零/19%"等做酶设计概率校准。
- 自检命令：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K06" --no-report`，须输出 `PASS K06 quotes=N/N`、退出码 0。

<!--CSV回填
work_type=论文
target=ALFA-tag（2 kDa 螺旋短肽表位）与 PSD-95 GK 结构域（以 SH3-GK 双结构域模块，34 kDa）
backbone_generation=沿用 RFdiffusion 出骨架 + ProteinMPNN 出序列（复合物用 AlphaFold2/AlphaFold3 预测打分）；本文不提出新设计算法，创新在湿实验筛查端
computational_filters=AF2/AF3 复合预测的 pAE interaction（链间残基对 PAE）；预期 Rh 由预测复合物经 FIDA 软件 PDB correlator 计算，用于判复合物尺寸是否匹配；无 MD/QM/自由能
thresholds=设计端 pAE interaction<10（in silico ~5%）、pAE<7 才细看、两螺旋折叠剔除；筛查端 ALFA 用固定 Rh 增量>=10% 判阳、GK 因预期变化小改用相对空白裂解液的 ANOVA-Dunnett 显著性（p<0.05）；最优裂解液稀释 30 倍（热裂解 1:30/1:100 假阳性=0）
md_used=否
qm_used=否
experimental_methods=E. coli BL21(DE3) 自诱导表达；化学(B-PER)/热(95度)裂解；Ni-NTA 重力柱纯化；FITC-ALFA / AF488-SH3-GK 荧光标记；FIDA capmix 单点筛查 + 2 倍系列稀释滴定拟 1:1 模型算 K_D；95 度 5 min 热稳筛选；96 孔板中通量；ANOVA-Dunnett 统计
pipeline_counts=ALFA：10 条设计候选（top5 折叠 x2 序列，蛋白MPNN 重采样 300 次）全部可溶表达产量 3-148 mg/L，纯化筛出 4 命中(1A/1B/5A/5B)、热稳后 3 命中(1A/5A/5B)；GK：6 折叠 x2=12 候选，热裂解筛出 3 命中(3A/3B/5B)、漏 5A；引用背景 19% 平均结合率(Watson 2023)
hit_rate=设计端 in silico 成功率 ALFA ~5%、GK 7.7%；湿实验端为定性小样本(2 靶/10+12 候选)，本文不报统一命中率，仅给"表达后约 1 天定初筛命中""30x 热裂解假阳性归零"的流程口径
best_metric=未记录（无单一最优指标口径；GK 纳摩尔级最强为 binder 3B K_D 44.1 +/- 16 nM，ALFA 最强为 5A K_D 2.76 +/- 0.25 uM，属各靶最优非全局）
cost_or_stat_note=免纯化/免固定化；单次 capmix 反应时间<1.8 min；毛细管 75 uM 内径 1 m；样品消耗低；最多 96 培养并行热裂解；PDB correlator 预测 Rh 误差 ~9%
role_in_timeline=把 de novo 结合蛋白漏斗末端的湿实验筛查(原为 Ni-NTA 纯化 + BLI 单点)换成免纯化、尺寸读数的 FIDA 单点法，量化"判阳阈值/裂解方式/稀释度"三个可调旋钮并给可复制 protocol；与 B09 的 pAE_interaction<10 计算闸口相接，补的是设计之后的实验确认环节，非算法环节
source_pointer=data/literature_cards/fulltext/K06_PMC12432402_text.txt（Protein Sci 2025;34(10):e70286; DOI 10.1002/pro.70286; PMID 40944422; PMCID PMC12432402）
CSV回填-->
