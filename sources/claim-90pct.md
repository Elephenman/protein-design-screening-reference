# "设计成功率 90%+" 的可查证性审计（2026-10-16）

> 审计对象：用户听浙江大学**周如鸿（Ruhong Zhou，求是讲席教授，定量生物中心主任 / 生命科学学院院长 2021.10–2026.04）**讲座后得到的转述——"其团队从头设计蛋白的成功率可达 90% 以上"。
> 方法：PubMed / Europe PMC / Crossref / bioRxiv / Research Square / Zenodo API 实取 + 全文正则扫描 + 中英文网页检索。所有 DOI、PMID、百分数均对应本次实际 API 返回或已下载全文；未取得的一律标注"未找到 / 未取到"。

---

## 一、检索记录表（检索串 / API 或站点 / 命中数 / 处理）

| # | 检索串 | API / 站点 | 命中数 | 处理 |
|---|---|---|---|---|
| 1 | `Zhou Ruhong[Author] AND 2024:2026[dp]` | PubMed esearch (eutils) | **67** | 全部 67 条 PMID 取回，esummary 批量取标题（`tmp/pmids.json`） |
| 2 | `AUTH:"Ruhong Zhou" AND SRC:MED AND PUB_YEAR:[2024 TO 2026]` | Europe PMC | **67** | 与 #1 同集合（同名作者混入，需按方向筛选） |
| 3 | `"Ruhong Zhou" AND ("success rate" OR "high hit rate" OR "hit rate")` | Europe PMC | **8** | 逐条下载全文并正则扫描（eLife CAAMO、NEOM、Sci Rep、JZUS-B 综述、3 条非相关/会议摘要） |
| 4 | `"Ruhong Zhou" AND "90%"` | Europe PMC | **58** | 全部为纯度 / CO₂ 浓度 / 汇合度 / 序列一致性等语境，**无一条为设计成功率**（逐条扫描确认） |
| 5 | `"Ruhong Zhou" AND "de novo design"` | Europe PMC | **13** | 多为纳米材料；仅 CAAMO 相关 |
| 6 | `"Ruhong Zhou" AND "experimentally validated"` | Europe PMC | **8** | 命中 CAAMO(eLife/2020)、TCR 深度学习、AttABseq 等 |
| 7 | `"Ruhong Zhou" AND "affinity matured"` | Europe PMC | **1** | gp100 模拟表位（JPCB 2025，非 OA，见 §2） |
| 8 | `"Ruhong Zhou" AND "success of the design"` | Europe PMC | **1** | 仅 Protein Society 2024 会议摘要增刊 |
| 9 | `"Ruhong Zhou" AND "design success"` | Europe PMC | **0** | 无命中 |
| 10 | `"Ruhong Zhou" AND SRC:PPR`（预印本） | Europe PMC | **34**（≥2024 年 15 条） | 15 条全部列出 DOI，见 §2 表；含 TCR-mimic、ANUBI、AlphaVacc、NEOM、CDK7、MolJam、PRISM、BioLab 等 |
| 11 | `query.bibliographic=Reengineering the antigen optimization process for superior neoantigen vaccine design` + `filter=type:posted-content` | Crossref | 10（首条命中） | 得 `10.1101/2025.08.03.668363`，作者含 Ruhong Zhou |
| 12 | `query.author=Ruhong Zhou&filter=type:posted-content` | Crossref | total-results 96387 | 检索串**无效**（宽泛匹配），前 100 条内 `given==Ruhong && family==Zhou` 命中 0；改用 #10 的 EPMC PPR 通道 |
| 13 | `api.biorxiv.org/details/biorxiv/2025-08-01/2025-08-10` | bioRxiv | 接口返回非 JSON（空） | 放弃；改 EPMC PPR + `biorxiv.org/...full-text` HTML |
| 14 | `biorxiv.org/content/10.1101/2025.10.03.680404v1.full-text` | bioRxiv HTML | 首次 429 限流；冷却 90s 后 **270 KB 全文到手** | 全部 `N/M` 分数逐条摘录（§2 行 3） |
| 15 | elink PMID→PMC（9 个设计类 PMID） | NCBI | 4 个有 PMCID/OA | 非 OA（gp100、ANUBI、anti-EGFR、GAD65）标为"全文未取得" |
| 16 | `AUTH:"Longxing Cao" AND ("success rate" OR "hit rate")` | Europe PMC | **8** | 下载 heterochiral(Cell Res 2024)、C9 miniprotein(Nat Commun 2026) 全文扫描 |
| 17 | `AUTH:"David Baker" AND "de novo design" AND ("success rate" OR "hit rate") AND PUB_YEAR:2024-2026` | Europe PMC | **54** | 取 6 篇 OA 全文扫描（RFdiffusion 抗体、RFpeptides 大环肽、β-pairing、multiepitope scaffolding、β-barrel、NIR 荧光蛋白） |
| 18 | `"de novo design" AND "success rate" AND PUB_YEAR:2025-2026 AND open_access:Y` | Europe PMC | **497** | 过噪，仅作背景；未用于结论 |
| 19 | `AUTH_ORCID:"0000-0003-4002-3648"` | Europe PMC | **0** | 该字段不被支持；改用 #16 姓名串 |
| 20 | `"Ruhong Zhou" AND (antimicrobial OR "antibacterial peptide") AND PUB_YEAR:2024-2026` | Europe PMC | **12** | 无膜活性肽"设计+实验命中率"工作 |
| 21 | `"Ruhong Zhou" AND amyloid AND design AND PUB_YEAR:2024-2026` | Europe PMC | **14** | 均为纳米材料抑制淀粉样（综述/机制），无设计命中率数据 |
| 22 | `"Ruhong Zhou" AND (nanobody OR "TCR mimic") AND PUB_YEAR:2024-2026` | Europe PMC | **2** | 无正式发表 TCR-mimic 论文 → 见 #23 |
| 23 | `"TCR-mimicking binders for pHLA high potency"` | PubMed esearch | **0** | 确认 TCR-mimic 工作**仅为预印本**（Crossref 亦仅返回 `10.1101/2025.10.03.680404`） |
| 24 | `all:"Ruhong Zhou"`（max_results=40） | arXiv API | 40 条中 **2024+ 署名 Ruhong Zhou = 0** | 该方向无 q-bio 预印本 |
| 25 | `q=MMDesign nanobody de novo` | Zenodo API | total 1233177（语义宽泛），**取到 2 份 MMDesign 报告** | `10.5281/zenodo.20526590`、`10.5281/zenodo.23321531`，摘要含 90.9% / 94.7% 原句（§4） |
| 26 | `https://www.anthropic.com/research/accelerating-protein-design` | WebFetch | **404** | 一手博客 URL 未能定位；`anthropic.com/claude-fable-and-mythos-5-1` 页面存在并含"典型命中率 10–15%"字样（二级引用） |

WebSearch 检索串（中文/讲座线索，9 条）：

| 串 | 结果 |
|---|---|
| `周如鸿 蛋白质设计 成功率 浙大` | 10 条，全为浙大个人主页 / 学会特刊简介 / 团队介绍，**无任何百分比** |
| `周如鸿 浙大 讲座 2026 从头设计 蛋白 AI 分子动力学` | 命中上交"分子动力学与人工智能研讨会"(2026-07-02) 等，**未见周如鸿带数字的讲座通告** |
| `周如鸿 成功率 90% 蛋白 从头设计 实验验证` | 命中的是**其他团队**：字节 PXDesign（六靶点最高 73%）、中科大 SCUBA-D（70 条设计 53 条可溶表达 ≈80%）、BindCraft（85 设计、平均成功率 46.3%）、Anthropic（15 靶点 14 成功） |
| `曹龙兴 西湖大学 蛋白设计 成功率 90% TCR mimic` | 命中曹龙兴 2026 首篇 Science（小分子调控蛋白从头设计）、CAR-T Binder 等新闻稿，**通篇无 90% 数字** |
| `周如鸿 学术讲座 海报 2026 生命科学与医学论坛` | 未找到带百分比的海报/通告 |
| `周如鸿 团队 公司 蛋白质设计 转化 杭州 2026 报告` | 未找到；仅个人主页与"AI 蛋白质设计培训班"广告 |
| `"从头设计" 蛋白质 "成功率" "90%" 团队 2026 中国` | **命中分子之心 MMDesign："靶点成功率超过 90%"**（新浪/果壳硬科技/知乎/头条，2026-06） |
| `分子之心 MMDesign 纳米抗体 论文 preprint bioRxiv 许锦波` | 命中 Zenodo 技术报告 + Gator Bio 供应商页复述数据（12 靶点/11 成功、PD-L1 命中率 86.7%、TNFα 14 测 7 中） |
| `Anthropic protein design 15 targets 14 success 93%` | 命中中文二手报道（百家号/头条 2026-08-19~09-02）；一手博客未取到 |

---

## 二、周如鸿 2024–2026 设计-验证类论文与成功率原句

**总判定：其团队经同行评议的论文中，可查到的最高"设计+实验验证"成功率为 83%（分母 6）；≥90% 的数字只出现在一处非同行评议预印本，且分母为 5（同时特异性成功率仅 2/5=40%）。**

| 论文（DOI / PMID） | 分子类型 & 末端分母 | 百分数原句（verbatim） | 末端 or 端到端 |
|---|---|---|---|
| **CAAMO RNA 适配体（SARS-CoV-2 RBD）**<br>eLife 2026, `10.7554/elife.107785`, PMID 42446520, PMC13368180 | RNA 适配体；6 个设计候选→5 个 SPR/BLI/EMSA 确认 | "Notably, the success rate of the in silico design via the CAAMO framework is very promising, with **five out of the six (~83%)** computationally designed candidate aptamers experimentally confirmed to have improved binding affinities." ；"…the high success rate **(0.83, 5/6)** achieved in this structure-based rational design process underscores the reliability of the RBD-aptamer Ta complex model…" ；"This high success rate (**~83%**) validates the reliability of the putative 3D binding model…" | **末端**（投测 6 个）。漏斗上游：对接生成 1000 个 Ta–RBD 构象→879 个同界面→聚成 6 簇→6 个候选→5 个成功；端到端 ≈ 5/1000 量级（论文未如此表述） |
| **NEOM 新抗原亲和力成熟**<br>Sci Rep 2026, `10.1038/s41598-025-34618-8`, PMID 41554915, PMC12865018（预印本 `10.1101/2025.08.03.668363`；最早 2024 版 `10.1101/2024.08.14.607669`） | 9-mer 肽；38 候选→FEP 筛出 6→5 个验证 | "Free energy perturbation (FEP) analysis further narrowed **38 candidates to six** peptides with"；"…with **6 out of the total 38** selected peptides (**roughly ~ 1/6**),"；"…we narrowed 38 initial candidates to six with favorable binding affinities,"；"Our findings indicate that most complexes remain stable,"；"This metric alone yields an average **success rate of around 80%**," | 末端 5/6 ≈ **83%**；端到端 **5/38 ≈ 13%**；40% 是 MD 稳定性判据、80% 是 NetMHC 单指标 |
| **TCR-mimic pHLA 结合分子设计**（预印本，**未经同行评议**）<br>bioRxiv 2025-10-04, `10.1101/2025.10.03.680404`；Teng Xie, Yaqi Fu, Shi-Meng Gong, Damiano Buratto, **Ruhong Zhou**（通讯），Institute of Quantitative Biology, ZJU | 多肽/微型结合体；投测分母 5、15、11、9 | "When reapplied to p53 R175H, these strategies improved **success rates from 2/5 to 5/5**…"；"…MPNN- and chimera-based optimization improved KRAS G12V binder selectivity and outperformed"；"This workflow yielded a high success rate:"；"…more than half of the promising candidates (**5/9**) yielded mutants that successfully passed both" | **末端小分母**：结合成功率 5/5 = **100%（N=5）**，但同一段同时给出**特异性成功率 2/5 = 40%**。无期刊版本（PubMed 检索串 #23 = 0 命中） |
| **AlphaVacc：自引导强化学习设计 HLA 呈递肽疫苗**（Research Square 预印本 2026-06-02）<br>`10.21203/rs.3.rs-9120093/v1`；作者含 **Ruhong Zhou**、Guanqiao Zhang、Yaqi Fu、Shi-Meng Gong、Liquan Huang、Zaixing Yang 等 | 肽；16 对 pHLA 突变体 | 摘要原句："Experimental validation across **16 representative pHLA mutation pairs confirmed the majority of**" | **无法量化**：正文未被 EPMC 收录（`isOpenAccess=N`、无 PMCID），Research Square 页面仅返回摘要，**未给出任何百分数或分子/分母** |
| **gp100 抗原模拟表位设计**<br>JPCB 2025, `10.1021/acs.jpcb.5c01507`, PMID 40692510 | 多肽 | 摘要内**无** success/hit-rate 数字（efetch 全文核验：仅"strongly improved affinity"类表述） | 全文非 OA，**未取得** |
| **GAD65(114-122) 自身抗原改造**<br>JPCB 2025, `10.1021/acs.jpcb.5c04875`, PMID 41362047 | 多肽 | 摘要无命中率 | 非 OA，未取得 |
| **ANUBI 蛋白/肽亲和力优化平台**<br>JCTC 2026, `10.1021/acs.jctc.5c01640`, PMID 41401395（预印本 `10.1101/2025.10.20.683353`） | 蛋白+肽 | 摘要仅有"…identifying variants with significantly improved predicted binding energy (approximately 20" | **纯计算，无实验命中率** |
| **物理启导 anti-EGFR 抗体改造** IJBM 2025, PMID 39986495 | 抗体 | 摘要无命中率 | 非 OA，未取得 |
| **植物肽 PSK 突变体优化** CSBJ 2025, PMC11994915 | 肽 | "They have a strong promoting effect (**20 % enhancement**) on stimulating root development compared with the wild-type PSK treatment." | 活性提升，非命中率 |
| **CDK7 抑制剂 SAGE** JPCB 2025（`10.1101/2024.11.13.623385`）、**FEP 辅助模拟表位筛选** Brief Bioinform 2025 `10.1093/bib/bcaf566`(PMID 40635188, PMC12240735)、**TCR 识别几何深度学习** Brief Bioinform 2026 `10.1093/bib/bbag048`(PMC12989321) | 小分子/方法 | 全文扫描（`success rate|hit rate`）**零命中设计命中率** | — |

**方向覆盖情况（任务 A 要求逐个查）**：蛋白/多肽亲和力成熟 ✔（NEOM、ANUBI、gp100、GAD65、PSK、anti-EGFR）；RNA 适配体 CAAMO ✔（eLife 2026 5/6；2020 EpCAM 版 PMID 32234785 "we have designed **two** RNA aptamers … we confirm"，仅 2/2 量级、无百分数，全文非 OA）；新抗原/疫苗肽 NEOM/AlphaVacc ✔；TCR-mimic ✔（仅预印本）；抗菌肽/膜活性肽 ✘（检索串 #20，12 命中无一为"设计+实验命中率"）；淀粉样纤维抑制分子 ✘（#21，14 命中全为纳米材料机制/综述）；纳米材料 ✔（PNAS 2026 DNA 骨架硅化等，无设计命中率）；AI+MD 筛选闭环 ✔（CAAMO/NEOM/ANUBI/SAGE/FEP）。**未发现任何一篇 ≥90% 的实验命中率。**

---

## 三、中文新闻与讲座线索

| 线索 URL | 原文句子 | 对应论文 / 口径 |
|---|---|---|
| `http://iqb.zju.edu.cn/a/rencai/zzjs/2021/0405/10.html`；`https://person.zju.edu.cn/ruhong`；`http://csid.zju.edu.cn/zjuwk/people/detail?id=40288…` | "在蛋白质设计、纳米药物设计、肿瘤免疫机制等领域取得了一系列国际领先的原创性成果…发表论文 300 余篇…H 因子 94" | 官方简介，**无任何成功率数字** |
| `https://wap.sciencenet.cn/blog-3516770-1479599.html`（Biomolecules 特刊通知） | 同上个人简介 | 无数字 |
| `https://m.sohu.com/a/677916292_121124375/`（2023-05-22 专访"设计出新型抗原有望开发为糖尿病疫苗"） | "我们的这项研究采用理论与实验相结合的方法…优化设计出了新型抗原" | GAD65/自身抗原线，**无百分比** |
| `http://iqb.zju.edu.cn/a/news/zxgg/2023/0417/207.html`（杭州定量生物学 2023 研讨会·团队介绍） | "团队聚焦'计算+'在蛋白分子机器结构与功能中的应用…" | 无数字 |
| 讲座海报/通告 | **未找到**任何 2024–2026 周如鸿讲座海报中出现"90%"（检索串见 §一 WebSearch 表 2、5、8 行） | — |
| `https://finance.sina.cn/2026-06-04/detail-iniafvzn3591049.d.html`（分子之心 MMDesign 发布） | "…成功在细胞因子、免疫检查点、病毒蛋白及多次跨膜受体（如 GPCR）等十多个高价值靶点上，实现了高精度的实用级纳米抗体的从头设计与验证，**靶点结合成功率超过 90%**, 最佳亲和力达皮摩尔级别。" | **非周如鸿**：分子之心（许锦波）公司口径 |
| `https://m.163.com/dy/article/KUM03EG20531MXCY.html`（果壳硬科技，2026-06-05） | "在纳米抗体设计任务上，仅以极小的实验样本量…在十多个真实靶点上实现了特异性结合，**靶点成功率（指产生至少一个有效分子的靶点比例）超过 90%**…在每个靶点仅挑选 **14 到 50 个**AI 设计的候选分子进行实际湿实验表达与测试" | **定义了 90% 的算法 = 靶点级、末端小分母** |
| `https://baijiahao.baidu.com/s?id=1873909452216829847`（2026-08-19，Anthropic 实验） | "针对 **15 个蛋白质靶点**从头设计结合体，其中 **14 个靶点获得成功**…命中率 **22.6% 至 26.7%**…典型命中率只有 10% 至 15%"；另 `m.toutiao.com/article/7687891118528266787/`："…靶点成功率高达 **93%**…目标级别的命中率最高可达 **90%**，最低可达 0%" | **非学术口径**：Anthropic 官方博客（一手 URL 未取得，404） |
| `https://www.ebiotrade.com/newsf/2024-10/20241013070409429.htm` / `jiqizhixin.com/articles/2024-11-22-7`（中科大 SCUBA-D） | "对共计 70 条设计序列进行了实验表征，其中**近 80% 的序列（53 条）可溶表达**" | **可溶表达率**，非结合命中率（任务 C 假设 ii 的现实范例） |
| `https://baijiahao.baidu.com/s?id=1844788530697964417`（字节 PXDesign） | "六个靶点，**五个成功率超 20%，最高 73%**" | 领域真实量级参照 |
| `https://zhuanlan.zhihu.com/p/1944768822495121550`（BindCraft） | "共设计 85 种…进入实验验证环节…平均成功率高达 **46.3%**，而传统方法通常只有微不足道的 0.1%" | 端到端可核算量级的最好例子 |

---

## 四、任务 C 判定：谁的口径可能是 90%？

**（iii）公司/新闻口径 —— 证据最强。**
分子之心（MoleculeMind，许锦波）MMDesign 两份 Zenodo **技术报告（非同行评议）**，其中新版发布日 **2026-10-12**，恰好早于本次讲座（2026-10-16）4 天，时间高度吻合：

- `10.5281/zenodo.20526590`（2026-06-03, "Practical De Novo Nanobody Discovery with Tens of Experimental Candidates"）原句：
  "Experimental testing of only **14–50 candidates per target** yielded confirmed binders for **10 of 11 targets (90.9%)**, with best measured affinities ranging from picomolar to nanomolar levels, demonstrating broad **target-level** success at experimentally tractable scale. Notably, MMDesign achieved a **50% hit rate on TNFα**…"
- `10.5281/zenodo.23321531`（2026-10-12, "MMDesign: Robust De Novo Binder Discovery Across Diverse Targets and Modalities"）原句：
  "The consolidated evaluation spans **19 campaigns on 18 distinct targets**, with confirmed binders in **18 of 19 campaigns (94.7%)** while experimentally testing **9–50 candidates per campaign**. VHH discovery succeeded in **16/17 campaigns**, including all six tested GPCRs, with **30/30 hits for NK3R** and **10/11 for GPR68**…"（同一报告里 MMFold 的结构预测成功率仅 **39.4% Top-1 / 72.5% acceptable-or-better**）

  → 口径特征完全对得上"90% 以上"：**靶点级**（一个靶点只要出一个有效分子就算成功）、**末端小分母**（每靶点仅测 9–50 个）、**候选池生成端数万个不进分母**、**公司技术报告 + 新闻稿**（新闻中靶点数在 11/12/十余之间漂移，说明是宣传口径而非可核算数字）。

**（i）某论文末端小分母的高比例 —— 同样能造出"90%+"，且就在周如鸿自己团队。**
`10.1101/2025.10.03.680404`（谢腾等，周如鸿通讯）"binding success rate: 2/5 → **5/5**" = 100%，但 N=5，且同行句里 **specificity success rate 1/5 → 2/5（40%）**。讲座若把这一句讲成"我们设计 5 个成 5 个"，被听众记成"90% 以上"完全可能。经同行评议的对应数字则是 CAAMO 的 **5/6 ≈ 83%** 与 NEOM 的 **5/6 ≈ 83%**（端到端 5/38 ≈ 13%）。

**（ii）把"表达率/纯度"当成设计成功率 —— 领域内确有此陷阱，但未在周如鸿论文里发现 ≥90% 的表达率表述。**
可核验的邻近案例：JACS 2026 `10.1021/jacs.5c19594`（Baker 系 NIR 荧光激活蛋白）"we obtained synthetic genes for **12 designs, out of which 10 exhibited successful expression in E. coli and bound retinal** … This high success rate…" = 83%，且以"表达+结合"双条件；RFpeptides 大环肽 Nat Chem Biol 2025 `10.1038/s41589-025-01929-w`(PMC12643943) 里唯一的 ">90%" 其实是化学纯度——"We successfully synthesized six designs with **high purity (>90%)** and tested them for binding to GABARAP using SPR"（真实命中率是六投两中），这正是"90% 被误传"的典型机制。

**曹龙兴（西湖大学）与 Baker 组：查无 ≥90% 端到端成功率论文。**
- Baker 组 RFdiffusion 从头设计抗体，Nature 2026 `10.1038/s41586-025-09721-5`(PMC12727541)：*"Supplementary Methods Table 6 for **success rates against each target, which range from 0% to 2%**"*；*"Although our results demonstrate that the de novo design of antibodies is possible, the **experimental success rates remain low**"*；*"Overall, **only 9%** of our ordered VHH designs have an ipTM > 0.6"*。
- β-pairing RFdiffusion，Nat Commun 2026 `10.1038/s41467-025-67866-3`(PMC12852815)：*"over **9.2%** of β-strand interface conditioned designs meeting reasonable quality metrics, in contrast to **0.98%** success rates by RFdiffusion conditioned on target hotspots alone"*。
- 多表位支架，Nat Chem Biol 2026 `10.1038/s41589-025-02083-z`(PMC13038408)：*"…with a success rate at tenfold binding enrichment of **33.7%**, compared to **3.3%** for hallucination-only and **21.7%** for ProteinMPNN and charge adjustment"*。
- β-barrel/纳米孔，PNAS 2025 `10.1073/pnas.2425459122`(PMC12478100)：*"…**>50% in silico success** in many cases"*（**计算**成功率，非实验）。
- 曹龙兴组 C9 迷你蛋白抑制剂，Nat Commun 2026 `10.1038/s41467-026-70667-x`(PMC13121834)：*"Site-1 achieved a **1.20 % success rate**, while Site-2 approached **0 %**… **0.16%**…**1.18%**…**1.57%, 0.25% and 2.72%**"*，最终挑 103 个骨架进实验。
- 曹龙兴 heterochiral，Cell Res 2024 `10.1038/s41422-024-01014-2`(PMC11614891)：全文仅泛称 "…could ultimately enhance the success rate of protein design"，**无 ≥90% 数字**。

**结论排序（置信度）**：
- 高置信：**讲座的"90%+"最可能是 2026 年 6–10 月 circulating 的公司/新闻口径（分子之心 MMDesign 90.9%→94.7% 靶点成功率，或 Anthropic 15 靶点 14 成 93%）**，或周如鸿团队自身**末端小分母比例（5/5=100%）**被概括为"90% 以上"。
- 中置信：**"表达率/可溶率"被转述为"设计成功率"**（领域内确有此现象，如 SCUBA-D 80% 可溶表达、JACS 2026 的 10/12 表达+结合），但周如鸿论文里未找到 ≥90% 的表达率句子。
- 低置信：周如鸿团队存在某篇/某报告给出 ≥90% **端到端**成功率。

---

## 五、结论：该声明目前能否被公开文献支持？

**不能（针对"周如鸿团队端到端从头设计蛋白成功率 ≥90%"这一具体表述）。**

- 已核实的、属于周如鸿团队的最强公开数字只有两个层级：
  1. 同行评议：**5/6 ≈ 83%**（eLife 2026 CAAMO；Sci Rep 2026 NEOM 末端），端到端分别约 5/1000（构象池）与 **5/38 ≈ 13%**（NEOM）。
  2. 非同行评议预印本：结合成功率 **5/5 = 100%（N=5）**，同时特异性成功率 **2/5 = 40%**、MD 过滤 11/15、FEP 5/11（bioRxiv `10.1101/2025.10.03.680404`）。
- 缺什么证据才能支持/否定：
  1. **讲座材料**（PPT/海报/讲稿截图、报告题目与日期、主办方），用以确认"90%+"的原口径与分母定义——这是当前唯一能闭环的缺口，公开检索已穷尽。
  2. AlphaVacc（`10.21203/rs.3.rs-9120093/v1`）与 TCR-mimic（`10.1101/2025.10.03.680404`）的**正式发表版**及其"16 对 pHLA 突变体 / 全部投测候选"的完整分母表（含失败计数）。
  3. 周如鸿团队非 OA 全文（gp100 `10.1021/acs.jpcb.5c01507`、GAD65 `10.1021/acs.jpcb.5c04875`、anti-EGFR PMID 39986495）正文中的命中率表——目前只能证明"摘要无 ≥90%"。
  4. 若"90%+"确指**蛋白**（而非 RNA/肽）：迄今**未见任何一篇周如鸿团队论文报告蛋白结合剂的实验命中率**，其已验证设计工作全部落在 RNA 适配体与肽/新抗原上；这点必须向讲者或团队直接确认。
- 若把口径换成"靶点级、末端小分母"，则 **90%+ 在 2026 年公开材料中确实存在**，但归属是分子之心（Zenodo 技术报告 90.9%/94.7%）与 Anthropic（14/15=93%），**不是周如鸿团队**，且两者都未经同行评议。

（本审计所有原文句均取自本次下载的 Europe PMC fullTextXML / bioRxiv full-text HTML / Crossref & Zenodo API 返回；中间文件留在 `A:\Data\MD\projects\protein-design-screening-20261016\tmp\`，含 19 份 XML 与 `tcr.html`。）

> **引用预算截短（2026-11-08，公开仓库口径）**：本底稿有 10 条逐字引句被截短（来源编号：Z03、Z07、Z13、未归属；许可类别：CC_BY_NC_ND、UNKNOWN、未归属），按 `deliverables/protein_design_license_audit.csv` 的逐份许可判定，单条引句截到 ≤100 字符；其中 3 条截短后仍**逐字命中同一份来源全文**，其余 7 条为**原句的前缀**（本地无全文或原句是我们自己的转写，只减不增、不新增第三方内容）。逐条改动账见 `deliverables/quote_budget_notes_ledger.csv`。
