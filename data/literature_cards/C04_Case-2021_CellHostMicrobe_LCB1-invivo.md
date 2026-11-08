# [C04] LCB1 的体内之旅——设计论文不产新漏斗数字，转化论文才回答"能不能用"

Case JB, Chen RE, Cao L, Ying B, Winkler ES, Johnson M, Goreshnik I, Pham MN, Shrihari S, Kafai NM, Bailey AL, Xie X, Shi PY, Ravichandran R, Carter L, Stewart L, Baker D, Diamond MS（圣路易斯华盛顿大学 + 华盛顿大学 IPD + UTMB；曹龙兴第 3 位，博后期间 2021）
Cell Host & Microbe 2021, 29(7):1151–1161.e5 · DOI 10.1016/j.chom.2021.06.008 · PMID 34192518 · PMCID PMC8221914（CC BY 4.0）
预印本 bioRxiv 10.1101/2021.03.01.433110 · 全文链接 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8221914/

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **C04**（组：曹龙兴组） |
| 本文取回方式 | Europe PMC `fullTextXML`（inventory.json 登记 fetch_channel=epmc_fulltext），2026-10-20 本地抓取 |
| 本地全文 | `data/literature_cards/fulltext/C04_PMC8221914_fullTextXML.xml`（144,190 B）；去标签纯文本 `data/literature_cards/fulltext/C04_PMC8221914_text.txt`（72,240 B） |
| 对照底稿 | `sources/cao.md` 第 90–98 行。底稿的定性判断"设计侧无新漏斗数字（继承 C01 的 105→12→11），主要贡献是体内效力"经本卡全文核对**成立** |
| 门禁登记 | `sources_map.json` 的 C04 条目原只登记底稿，本卡写作时已把上述两份全文补进登记（与 inventory.json 一致） |
| 证据级别 | **全文级**（所有引句在本地纯文本逐字命中） |
| 未取到的部分 | Figures S1–S6 与补充方法细节（正文 STAR Methods 已含主要实验参数，缺的只是补充图原值） |
| 本文性质提醒 | 这是**转化验证**论文：没有计算设计漏斗，没有新阈值。写卡与引用时的正确姿势是把它当"设计品的体内考场"，而不是方法学证据 |

## 1. 这篇到底解决什么（一句话）

把 C01 设计出的 LCB1 改造成两个可体内用药的版本（单体 LCB1v1.3、Fc 融合 LCB1-Fc），在两种免疫健全小鼠模型里证明：注射或鼻喷给药、暴露前 5 天到暴露后 2–3 天的任意时间窗内，都能把 SARS-CoV-2（含 B.1.1.7 与 E484K/N501Y 重组株）压到接近检测限并完全防止肺病。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述）

1. **母体设计 LCB1 不能直接当药**：缺两样东西——体内可表达量/可溶性与药代。应对分两路：**表达路**——"we introduced polar mutations into LCB1 to increase expression yield and solubility without"；具体是相对原始 LCB1 的 7 个极性突变："LCB1v1.3 with polar mutations (4N, 14K, 15T, 17E, 18Q, 27Q,"（Methods 还配了热处理裂解这一步。） **代价**：本文没有披露这 7 个位点是怎么选的（设计侧记录在 C01/补充），v1.3 与 LCB1 的结合差异只有"without altering RBD binding"一句定性保证。
2. **两条改造路线各有短板，作者用"分工"应对**：Fc 融合延长循环半衰期、启动免疫效应臂，但按文献推断 Fc 融合体在上呼吸道蓄积不高（讨论引 Reynolds 1988）；单体只有 9.1 kDa，"we used LCB1v1.3 because of its small 9.1-kilodalton size (versus an Fc fusion protein), which allows for binding to an increased number of RBD molecules for a given mass dose and greater neutralizing activity"。于是 **LCB1-Fc 走腹腔注射管全身与肺，LCB1v1.3 走鼻喷管局部**——两套给药路线分别做完整的时间窗与剂量阶梯。 **代价**：等于把同一个分子做成两个候选、实验量翻倍；且作者自认正式 PK/安全/毒理仍缺（"Although formal pharmacokinetics, safety, and toxicology studies are needed for our miniprotein prior to clinical studies"）。
3. **系统给药清不掉鼻腔病毒（4 dpi）**：现象——"LCB1-Fc treatment had no effect on viral RNA levels in nasal wash samples obtained at 4 dpi"，与一篇仓鼠抗体研究一致。**他们做了什么**：不回避，加测 7 dpi，"However, viral RNA levels were reduced at 7 dpi,"；并在讨论里直接把"鼻喷局部给药"立为弥补该短板的方向。 **代价**：上呼吸道灭菌不完全是本文遗留问题，只有"400 倍降低（D-5 预防）"这类间接证据。
4. **K18-hACE2 模型太狠、治疗窗本应很窄**：作者明知"Since K18-hACE2 mice are highly vulnerable to infection,"，仍选致死剂量（10^3 PFU）做治疗实验。 **应对成果**："Despite this, LCB1-Fc treatment begun at D+2 or D+3 conferred 100% survival after a lethal dose"；对照组 "Whereas control binder-treated animals succumbed to infection by day 11 post-inoculation,"。另用**第二个不依赖 hACE2 转基因的模型交叉佐证**——"we tested the efficacy of LCB1-Fc in a"，且 "Prophylaxis with 250 μg of LCB1-Fc,"。 **代价**：两种模型都是小鼠，作者自认需仓鼠/NHP（见 §2.7）。
5. **变体逃逸的担忧**：E484K/N501Y 已知能让大量单抗失效。他们先拿 C01 的 cryo-EM 结构做**预测**（只有 N501Y 预计影响 LCB1 结合），再实测两个变体：体外 "Although the neutralizing activity of LCB1v1.3"；体内 50 μg 预防仍全组织保护。 **后续应对（文中列为计划）**：继续计算优化结合 + 组合不同表位 binder。 **代价**：用的是重组株，不是真 B.1.351/B.1.1.28——作者自己承认两个突变"do not encompass all antigenic properties"。
6. **免疫原性（小蛋白是不是抗原）**：设计 18 天每 3 天鼻喷重复给药实验，"Only one of ten mice developed IgG antibodies"，且复剂量组仍全部保护。 **但作者主动给出相反解释的可能**："While we interpreted this result as a lack of"，并要求换剂量方案/浓度/更长观察重做。 **代价**：只测了 v1.3，LCB1-Fc 未测（Limitations 自述）。
7. **半衰期只能"功能性测量"**：没有现成的针对小分子的 PK 平台。应对：用两类平行读出互证——FRNT 测标本中和活性（1/EC50 per mL）+ 竞争性/直接 ELISA 测绝对浓度，"at 48 h, substantial levels of neutralizing activity remained present within the lungs and nasal turbinates, with approximately 10-fold reductions seen at 24-h intervals"；再由时间窗外推 "we speculated that the half-life of i.n."，讨论段收敛为 "our functional analyses suggest that the"。 **代价**：同一篇里两个估算区间（12–24 h 的推测 vs 6–12 h 的功能半衰期）不完全一致，说明这组数字是推断级，不是拟合级。
8. **D+2 鼻喷后治疗效果还不够好**："While we observed reductions in lung viral burden"。本文未解决，只列了对策清单。

## 3. 方法与工作流程（每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **分子工程**：极性点突变（v1.3）与人 IgG1 Fc 融合（LCB1-Fc，pCMVR/Expi293F 瞬转 + MabSelect PrismA 纯化）；v1.3 走 pet29b/Lemo21 + 80°C 热裂解 + IMAC + SEC。
- **结合/活性**：BLI（Octet RED96，biotin-RBD/SA 传感器，缔合 3600 s + 解离 7200 s）；活病毒空斑减少中和（FRNT）EC50。
- **体内**：K18-hACE2 转基因小鼠（致死 10^3 PFU 鼻内攻毒）+ 129S2 非转基因（N501Y 适应株）；读出=生存/体重/ plaque assay 感染病毒/RT-qPCR 病毒 RNA（肺心脾脑鼻洗液）/flexiVent 呼吸力学/H&E 病理/细胞因子 qPCR。
- **药代与免疫原性**：FRNT 功能性浓度 + 竞争 ELISA（v1.3）/直接 ELISA（Fc）；18 天反复给药后血清抗 v1.3 IgG。
- **没有用的方法**：无计算设计漏斗、无 MD、无 QM；结构信息只被**引用**（C01 的 cryo-EM 结构用于预测哪个突变会影响结合）。

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| W1 | C01 的 LCB1（56 残基） | 背景交代："We recently generated a panel"；本文起点 "we previously designed LCB1 as a potent" | 无（继承） | 母体设计 1 个 |
| W2 | LCB1 | 双路改造：7 极性突变→LCB1v1.3；+hIgG1 Fc→LCB1-Fc | 判据：表达量/可溶性↑且结合不变；Fc 融合↑生物利用度 | 变体 2 个 |
| W3 | 两个变体 | BLI 结合 + WA1/2020 活病毒 FRNT | Kd、EC50 | "LCB1v1.3 and LCB1-Fc bound avidly to a single RBD"；"LCB1v1.3 and LCB1-Fc also"；对照 binder EC50 >10,000 nM |
| W4 | K18-hACE2 小鼠 | LCB1-Fc 250 μg i.p. 预防（D-1），攻毒 10^3 PFU | 判据：体重、生存、plaque（感染病毒）、RT-qPCR（RNA 达检测限）、呼吸力学、H&E、细胞因子 | "a single 250-μg (∼10 mg/kg)"；肺感染病毒 "After LCB1-Fc prophylaxis,"；n=10（生存）/n=8（组织），两实验 |
| W5 | 同上模型 | 治疗：D+1/2/3 给药 | 生存终点 | 4/7 dpi 全组织病毒载量降、病理改善；见 §2.4 的 D+2/D+3 100% 生存句；阴性现象见 §2.3（鼻洗液 4 dpi） |
| W6 | 129S2 小鼠 | 换模型佐证（N501Y 适应株 + B.1.1.7 天然分离株） | 同上读数 | 肺与鼻洗液病毒负担降低（§2.4 两句） |
| W7 | LCB1v1.3 | 鼻喷时间窗矩阵：预防 D-5/-3/-1/-6h，治疗 D+1/+2；剂量阶梯 2/10/50 μg | 判据：肺病毒 RNA 降幅、体重；"Treatment with as little as 2"；"Doses of 10 μg (0.5 mg/kg) or" | "even mice receiving LCB1v1.3 5"；50 μg 组几乎无肺炎（H&E） |
| W8 | 给药动物系列 | PK：C57BL/6J，i.n. 200 μg v1.3（1/8/24/48 h）或 i.p. 250 μg Fc（24/48/72 h）；FRNT 1/EC50 + ELISA 双读出 | 判据：检出限、24 h 递降 | "at 48 h, substantial levels of"；Fc 血清浓度三天恒定；n=3/组单次实验；半衰期推断见 §2.7 |
| W9 | v1.3 反复给药队列 | 18 天每 3 天 50 μg 鼻喷 → 血清 ELISA → 次日攻毒 | 判据：抗 v1.3 IgG 阳性数；攻毒后保护 | "Only one of ten mice developed"；复剂量组仍全部保护（n=10–12/组） |
| W10 | B.1.1.7 分离株 + WA1/2020-E484K/N501Y/D614G 重组株 | 体外 FRNT + 体内 50 μg D-1 预防（含 D-5/D-3 持久性） | 判据：EC50 倍数变化、体重、6 dpi 全组织 RNA | 见 §2.5 句（45–50 倍降、仍 ∼800/667 pM）；两变株攻毒下所有组织均受保护；6–8 周龄、n=5–6、两实验 |

## 4. 关键数字台账

| 数值 | 含义 | 出处 |
|---|---|---|
| 7 个极性突变（4N,14K,15T,17E,18Q,27Q,38Q） | LCB1→LCB1v1.3 | §2.1 句 |
| Kd <625 / <156 pM | v1.3 / Fc 对单 RBD | W3 |
| EC50 14.4 / 71.8 pM；对照 >10,000 nM | WA1/2020 活病毒中和 | W3 及其图注 |
| 250 μg ≈ 10 mg/kg i.p. | LCB1-Fc 预防/治疗剂量 | W4 |
| 10^3 PFU | 致死攻毒量（K18-hACE2） | W4 |
| 100% 生存 vs 对照 day 11 全死亡 | D+2/D+3 治疗 | §2.4 |
| ~400 倍 | D-5 鼻喷后 7 dpi 肺 RNA 降幅 | W7 |
| 2 μg（0.1 mg/kg）/ 10 μg（0.5 mg/kg）/ 50 μg | 鼻喷剂量阶梯三档 | W7 |
| 1/10 小鼠 IgG 阳性 | 18 天反复给药免疫原性 | W9 |
| 12–24 h（推测）/ 6–12 h（功能半衰期）/ 10 倍每 24 h 递降 | v1.3 呼吸道药代 | W8、§2.7 |
| 45–50 倍；~800 pM；667 pM | 对 B.1.1.7 与 E484K/N501Y/D614G 的 EC50 变化 | §2.5 |
| 9.1 kDa | v1.3 分子量（vs Fc 融合体） | §2.2 |
| n=3–12/组、多为两独立实验、p<0.05 | 统计口径 | 各图注（如 W4/W7） |

## 5. 结论——作者说了什么

1. LCB1-Fc 腹腔给药在预防与暴露后治疗（至 D+3）都防住 K18-hACE2 小鼠的致死感染：病毒载量近检测限、肺力学与病理等同未感染组、100% 生存；129S2 模型佐证。
2. LCB1v1.3 单次鼻喷在 D-5 至 D+2 窗口有效，0.1 mg/kg 即可防止体重下降；对 B.1.1.7 与 E484K/N501Y/D614G 仍体内保护。
3. v1.3 弱免疫原、功能半衰期数小时~一天级，"the pharmacodynamic and pharmacokinetic half-lives of LCB1v1.3 and LCB1-Fc at key sites of viral replication are sufficient to provide protection for several days after a single dose."
4. 相对单抗的四条优势：每个刺突三聚体三个 protomer 都能结合（按摩尔位点多）、制造便宜、可再设计追变体、可连接器多聚化防逃逸。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **"设计成功"与"可用"之间隔着至少 4 个新问题**（表达量、半衰期、局部递送、免疫原性），这篇论文的全部贡献都在 C01 漏斗**之外**。对我们项目的镜像：就算筛出 UAA 合成酶候选，也还差可表达、可稳定、 assay 时间窗匹配这些工程层，别把命中率当可用性。
2. **双路线分工（Fc 管全身、单体管局部）是处理"一个物理性质不够好"的经典手法**——不硬改分子，而是改变给药生态位。对应我们：某候选催化慢但稳定，可以换读出窗口而不是急着判死。
3. **半衰期两处估算不一致（12–24 vs 6–12 h）提醒：本文 PK 是"功能性"测量**（中和活性/检出限外推），不是房室模型拟合。引用这篇时只能说"他们测到呼吸道活性可持续数日"，不能说"半衰期=X"。
4. **"用已有高分辨结构预测哪个逃逸突变会失效，再只对预测做实验"**——结构信息在这里的作用是**缩小实验矩阵**（只测 N501Y 相关株），这是结构设计闭环最省钱的一次落地，值得我们的机制级验证预算分配参考。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者自列（Limitations）：需仓鼠/NHP 复核；Fc 半衰期实验时长不够；未做全身生物分布；免疫原性只测 v1.3 且可能是耐受假象；重组两突变株≠真 B.1.351/B.1.1.28 的全部抗原性；D+2 治疗效果需提高（对策：加量/复次/延长半衰期改造）。
- 我们读出：① 本文零计算筛选，任何"命中率"都继承自 C01，引用时不许把体内保护率混入设计漏斗数字；② "无活病毒分离株在考"（变体用重组株）在 2021 年是务实选择，但让"对变体有效"的证据级别低于对 WA1/2020 本身；③ 保护终点里最硬的只有生存与 plaque 未检出，其余是 RNA 拷贝数——qRT-PCR 读数对"感染"与"残留 RNA"不加区分，作者未讨论这一混淆。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"先改造、再考核"的转化模板**：对筛出的候选酶，把"表达/溶解性/半衰期"类工程问题单列一层（极性表面突变、融合标签是现成手段），漏斗命中率与该层解耦记账。
2. **双路线分工**：同一候选做"全身型"（融合/大分子化）与"局部型"（小分子化）两条制剂路线，各配各自终点——对我们即"体外重构生化验证"与"细胞内功能读出"两条独立考核。
3. **用结构先验缩小实验矩阵**（§6.4）：我们的机制模型（S0/S1/S2 三步化学事件）应同样先验预测哪些突变是"预期影响/预期无影响"，只对差异做昂贵验证。
4. **弱项不藏**：4 dpi 鼻洗液无效、D+2 治疗不足都如实报，并给出对策清单——我们的失败候选台账应照此格式（现象→归因→是否补救→代价）。

**不可迁移（为什么不能照搬）**

1. **小鼠保护率不是任何筛选方法的命中率**：这里没有候选池，"100% 生存"不可换算成设计成功率；DP2R 口径禁止。
2. **FRNT/ELISA 药代读出、Fc 融合增效应，是给药科学，不回答"能不能催化 UAA 掺入"**；两者不可类比。
3. **本文没有计算方法**（无 MD/QM/打分），不能为任何计算判据提供"经过体内检验"的背书——它检验的是 C01 的产品，不是某种打分法。

## 9. 溯源与自检

- 本地纯文本：`fulltext/C04_PMC8221914_text.txt`（Europe PMC fullTextXML 剥离归一，未改写）。
- 引句底稿: data/literature_cards/fulltext/C04_PMC8221914_text.txt
- 底稿指针：`sources/cao.md:90–98`；母体设计漏斗见本目录 C01 卡；多价化后续见 C06（同 LCB 系列）。
- CSV 字段映射：§3 ↔ 实验验证手段；§4 ↔ 成本/统计；§8 ↔ 在方法演进链的位置。
- 引句全部从本地全文复制，写卡前经 111 条候选预检（0 缺失），门禁复跑结果见交付回报。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 25 条逐字引句来自许可受限的第三方来源（C04；RESEARCH_REUSE_ONLY），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（转化/体内验证，非设计方法学）
target=SARS-CoV-2 刺突 RBD 中和（LCB1v1.3 单体 与 LCB1-Fc 融合，含 B.1.1.7、WA1/2020-E484K/N501Y/D614G）
backbone_generation=无新设计：继承 C01 的 LCB1，本文只做蛋白工程改造（7 个极性点突变→LCB1v1.3；hIgG1 Fc 融合→LCB1-Fc）
computational_filters=无计算漏斗；仅引用 C01 cryo-EM 结构做定性预测（只有 N501Y 预计影响结合），据此选择待测变体
thresholds=动物保护判据：生存/体重/plaque 未检出/RT-qPCR 达检测限、呼吸力学对齐未感染组；统计 p<0.05（Prism）；剂量档 2/10/50 μg(i.n.)、250 μg(i.p.)
md_used=否
qm_used=否
experimental_methods=BLI(Octet RED96)、活病毒 FRNT 中和（Vero E6/Vero-hACE2-TMPRSS2）、K18-hACE2 与 129S2 小鼠感染模型（i.p./i.n. 预防与治疗）、flexiVent 呼吸力学、H&E 病理、细胞因子 qPCR、免疫原性 18 天复 dose ELISA、功能性 PK（FRNT 1/EC50+竞争/直接 ELISA）
pipeline_counts=母体设计 1（C01 的 LCB1）→工程变体 2（v1.3、Fc）→两模型×时间窗 D-5…D+3×剂量阶梯；每读数 n=3–12、多为两独立实验；无候选漏斗
hit_rate=本文不产设计命中率（继承 C01：105→12→11）；体内侧：D+2/D+3 治疗 100% 生存；复 dose 免疫原性 1/10 阳性；变体 EC50 降 45–50 倍仍 <1 nM
best_metric=LCB1v1.3 EC50 14.4 pM（WA1/2020 活病毒）、Kd<625 pM；LCB1-Fc EC50 71.8 pM、Kd<156 pM；变体仍 ~800/667 pM
cost_or_stat_note=BSL3/A-BSL3 活病毒平台；计算成本无；PK 仅功能性测量（半衰期两口径 12–24 h 推测 vs 6–12 h 功能推断，不一致）；正式 PK/毒理未做（作者自述）
role_in_timeline=把 C01 的 pM 结合体推进到体内 prophylaxis/therapy+变体证据与免疫原性/PK 首批数据，完成 binder 平台"能设计→能用"的转化闭环；曹龙兴博后期的转化出口（与 C06 多价、C11/C12 应用线同根）
source_pointer=data/literature_cards/fulltext/C04_PMC8221914_text.txt；sources/cao.md:90-98
CSV回填-->
