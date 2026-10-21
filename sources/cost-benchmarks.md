# 设计→验证的成本结构与预筛判据的定量证据（调研于 2026-10-16）

> 调研范围：跨实验室通用技术与经济学；不重复 Baker / 周如鸿 / 曹龙兴 的论文清单（另有人在做），但引用其中可作为定量证据的原文。
> **DOI 核验方式**：本文所有 DOI 均经 Crossref REST API（`api.crossref.org/works/<doi>`）或 Europe PMC REST 实际返回确认；标注 `†` 者仅由 Europe PMC 检索结果列出、Crossref 未复核（多为 2026 年新文章）。原文数字尽量以论文原句摘录。
> **证据类型标签**：〔价目表〕公开收费页 / 〔论文实测〕论文方法与结果 / 〔作者估算〕论文或综述作者的推算 / 〔公司自述〕厂商与市场稿 / 〔本报告推算〕由已核验单价做算术，输入均注明。
> 汇率换算假设：1 USD ≈ 7.1 CNY（2026-10 近似，**假设值**，仅用于量级比较）。

**成功测试（本文件的判定标准）**：八个章节均有内容；每条成本数字带出处与证据类型标签；每个引用 DOI 可被 API 复核；对"MD/QM 太贵不能筛"与"MD 精筛提升命中率"两问，分别给出已核验原文或明确记为未核实。判定：**PASS（第 3 项"MD 精筛提升命中率 X%→Y%"的正面原文未能核实到，已如实写入第八章缺口）**。

---

## 一、成本表（实验验证侧）

| 环节 | 单价 / 通量 | 规模与口径 | 出处 | 证据类型 |
|---|---|---|---|---|
| 寡核苷酸池合成（每碱基） | oPools 类芯片池：**<$0.001/base**，比双链 DNA 片段合成（~$0.05/base）**便宜约 100 倍** | 用于 DMS 变异文库；作者据此论证"基因大小→合成与测序成本"是 DMS 可扩展性的主要限制 | Jann et al., PLoS Biol 2026, 10.1371/journal.pbio.3003645（原文引用其 [22,23] 号 vendor 价目） | 论文实测＋引厂商价目 |
| 基因合成（克隆型，短基因） | Twist "Complex Gene Synthesis" **起价 12¢/base**，15 个工作日 | 当前官网挂价；600 bp 基因 ≈ $72；300 bp 设计基因 ≈ $36 | twistbioscience.com 产品页（2026-10 抓取） | 价目表 / 公司自述 |
| 基因合成（常规，历史报价） | 克隆型 **$0.09/bp**、非克隆型 **$0.07/bp**；1 kb 片段 4 天交付 **$70** | 公司 CEO 访谈口径（2023），**可能已过时**，仅作趋势参考 | 转引自 2023 年中文行业报道对 Twist 的访谈（phirda.com、腾讯新闻） | 公司自述（二手转引） |
| 引物池（小池） | GenScript oPools（1K–8M oligos/chip）**From $800/池** | 1K 条池 → 上限 ≈ $0.8/条；池越大单条越便宜 | genscript.com/gentitan-oligo-pools.html（2026-05 抓取） | 价目表 |
| 基因合成的成本构成 | 600 bp 基因 ≈ **170 元**，其中 oligo 合成 90 元（53%）、组装 50 元、Sanger 测序 QC 30 元； oligo 错误率 0.2%/nt → 600 bp 全对概率仅 **30%**；0.08% → **62%**（挑克隆/测序 QC 成本减半） | 行业成本拆解，非一手价目 | 合成生物学行业分析（zhihuiya / xueqiu，2024-06） | 作者估算（行业分析） |
| 展示/文库用 DNA 的实际上机规模 | 顶级 ~31,000 条设计以 **芯片合成 DNA** 交付后走酵母表面展示筛选 | 单批次规模量级 10^4–10^5 序列 | Qian et al., Nat Commun 2026, 10.1038/s41467-026-76740-9（SAPP/DMX） | 论文实测 |
| 微阵列 DNA → 阵列化克隆 | 条码化 + 短读长测序解混，把 **基因合成成本再降 5 倍**；96→192 个克隆反应 **2 小时** | DMX 协议：约 2000 基因的大规模解混需采 ~8000 个克隆（20×384 板）达 >95% 回收；实测 4608 克隆回收 78% 文库变体 | 同上，10.1038/s41467-026-76740-9 | 论文实测 |
| 表达（E. coli 小规模） | 24/96 孔板、**每孔约 2 mL** 培养 | 设计筛选阶段的常规规模 | Pinheiro et al., Protein Sci 2025, 10.1002/pro.70286（FIDA） | 论文实测 |
| 表达＋纯化＋表征通量 | **每天数百个设计**，"每个构建体的成本≈几条 DNA 寡核苷酸"；SEC 是瓶颈：约 **300 样/天/台**层析仪；192 样 SEC 过夜（15 h，**<5 min/样**）；FP 变体 96 个一周内表征完 | 半自动蛋白制备（SAPP）：产量、分散度、寡聚态、吸光/荧光 | 10.1038/s41467-026-76740-9 | 论文实测＋作者估算（成本口径） |
| 蛋白表达/纯化的方法学基线 | 常规小量表达与纯化的产量/可行性基准（无价格；Crossref 该条目无作者字段记录） | 用于判断"能否在微规模拿到可测蛋白" | *Protein production and purification*, Nat Methods 2008, 10.1038/nmeth.f.202 | 论文（方法综述） |
| 可溶表达 / 正确寡聚态的经验率 | 无条件生成的设计中"**一半可溶表达**、CD 与模型一致且高热稳定"；某次 44 个体外表达纯化设计中 **37 个** SEC 符合目标寡聚态；另一组 9/18 表达为预期单体峰 | 说明"表达+SEC"本身就是廉价且高信息量的判据 | Watson et al., Nature 2023, 10.1038/s41586-023-06415-8（RFdiffusion） | 论文实测 |
| 单点结合筛选（BLI/SPR）成本与命中率 | RFdiffusion 五靶点 campaign：每靶点测 **<100 个设计**，总体实验成功率 **19%**（10 µM 单点、≥50% 正响应） | 与"动辄数千设计"的旧范式对照 | 同上，10.1038/s41586-023-06415-8 | 论文实测 |
| BLI 机时 | Octet RED96：**100 元/小时**（院内院外同表） | 中科院微生物所结构与功能分析平台 | im.cas.cn 生物分子结构与功能分析平台收费页（2026-03 抓取） | 价目表 |
| BLI 通量 | 96 样动力学：Octet R2 **>19 h**、R4 **5 h**/板；定量模式 60–120 min/96 样 | 厂家对比表 | sartorius.com.cn Octet 型号比较页（2026-07 抓取） | 公司自述 |
| SPR 机时 | Biacore 8K：**300 元/h**（北大医学部国重）；**150–250 元/h 校内、500 元/h 校外**（华南农大）；100/300 元/h（微生物所）；Biacore T200 100/300 元/h（中国药科大学） | 核心设施公开收费 | skl.bjmu.edu.cn、cszx.scau.edu.cn、im.cas.cn、sklnmggpt.cpu.edu.cn 设备页 | 价目表 |
| SPR 芯片耗材 | CM5（含偶联试剂）**1600 元/张**；SA **3800 元/张** | 该通知发布于 **2010 年**，价格已过时 | ibp.cas.cn 平台通知（2010-08） | 价目表（旧） |
| SPR 单芯片通量 | Biacore 8K 高通量配置：24 个检测位点、**24 h 内可分析约 8800 个相互作用**；Sierra SPR-32：>4400 样/天 | 厂商仪器页转述 | antpedia 仪器简介页（Biacore 8K / Sierra-32 条目） | 公司自述（二手） |
| ITC | 单次测量：**100 元/小时**（微生物所 AFFINITY ITC）；委托全套服务（设计、上样、滴定、分析、清洗）：**5300 元/对**（国家蛋白质科学中心上海，Peaq ITC） | 一个 20 次滴定的滴定集 ≈ 5300 元 ≈ **$750** | im.cas.cn 收费页；上海科技创新券平台 cxq.stcsm.sh.gov.cn 蛋白质设施服务条目（2025 抓取） | 价目表 |
| DLS | **50 元/样（校内）–150 元/样（校外）** | 微生物所平台 | im.cas.cn | 价目表 |
| 热稳定/聚集筛查 | Prometheus NT.48（DSF/ nanoDSF）：**100 元/小时** | 微生物所平台；每板多样、材料消耗 µL 级 | im.cas.cn | 价目表 |
| 无标记结合筛查（FIDA） | 单条毛细管读数即可判"结合/不结合"；**表达后 1 天内出命中**；可直接测**未纯化的热裂解液**；75 µm 内径毛细管、样品消耗极小 | 定位为"时间与成本高效"的设计筛选工具；局限：依赖流体力学半径变化，需先估算 ΔRh | 10.1002/pro.70286；配套协议 10.17504/protocols.io.j8nlkyo5dg5r/v1† | 论文实测 |
| 测序式 PPI 并行读出 | MP3-seq 单次实验可测 **>100,000 个蛋白–蛋白相互作用** | 用于设计杂合二聚体的成对验证，替代逐构建体纯化 | Baryshev et al., Nat Chem Biol 2024, 10.1038/s41589-024-01718-x | 论文实测 |
| 展示筛选单批规模（实测口径） | 酵母表面展示一次筛 **9,000 个设计/靶**（抗体片段）；另一批 4841 / 1298 条设计库；芯片合成 DNA 的大规模折叠筛：**13,990 blueprint designs** 经"酵母表面蛋白酶解抗性＋SEC-MS 条码"两级廉价筛 | 与 95 个/靶的 E. coli 表达＋单点 SPR 并行使用 | Kim D et al., PNAS 2023, 10.1073/pnas.2207974120；*Atomically accurate de novo design of antibodies with RFdiffusion*, Nature 2026, 10.1038/s41586-025-09721-5（原句已从 OA 全文核实）；10.1038/s41467-025-67866-3† | 论文实测 |
| 展示筛选通量与边际成本 | 常见口径：YSD/phage 库 10^7–10^13 克隆、每命中候选边际成本极低；**本次未逐条核到一手原文数字** | 见第八章 | — | 未核实 |
| 核磁/质谱类确证 | DIA 蛋白组 **378 USD/例**（工业客户）、磷酸化 535–1417.5 USD/例（芝加哥大学质谱平台） | 用于"设计蛋白是否真的成形/修饰"的重型确证 | 转引自 2023 年中文综述对 uchicago.edu Proteomics Platform 费率页的引用 | 价目表（二手转引，未直接核对） |
| 冷冻电镜（300 kV） | 校外 **9,000–10,000 元/24 h**（南方科技大学 Krios G3/G3i）；北大 **15,000 元/天**（校外，2024-04-02 生效）；上海药物所 **18,000 元/天（院所）/30,000 元/天（企业）**（2020，或已过时）；河南师大 Krios G4 校内 5,000/校外 10,000 元/天；KEK（日）Titan 学术 **3,000 円/h**、企业 **15,000 円/h**（最少 24 h/天） | 24 h 机时 ≈ **$1,270–$4,200**；一台 Krios 一天可完成一个中等数据集 | cryoem.sustech.edu.cn；cryoem.pku.edu.cn；simm.cas.cn；gxxt.henu.edu.cn；www2.kek.jp/imss/sbrc | 价目表 |
| 电镜耗材与制样 | C-clip+环 180–260 元/套；Quantifoil 300 目铜网 60 元/片、金网 200 元/片；Vitrobot 制样 100–200 元/h；筛样（Ceta）300 元/h、K3 收集 400 元/h（200 kV Glacios） | 单个样品的"上机前置成本"约几十到数百元 | sjzx.genetics.ac.cn 冷冻电镜平台规定（2021，偏旧）；cryoem.pku.edu.cn | 价目表 |
| X 射线晶体学（实验室） | 结晶板 60 元/板（校内）、结晶 Kit 600 元/盒；Mosquito 分液 **20 元/板**；Gryphon 55 元/板；Rigaku 单晶衍射 **320 元/小时**；晶体观察 80 元/h | 清华蛋白质研究技术中心 X 射线晶体学平台（页面日期 2019-09，**可能过时**） | phoenix.tsinghua.edu.cn/info/1064/1620.htm | 价目表 |
| 同步辐射机时 | 上海光源晶体数据（平台代收）：**200 元/颗晶体（校内）/500 元/套数据（校外）**；蛋白设施"五线六站"技术支持 212 元/h、委托 800 元/h | 学术通道常通过提案免费，付费口径为平台代收/技术服务 | 同上清华收费页；cxq.stcsm.sh.gov.cn 国家蛋白质设施条目 | 价目表 |
| 流式分选（FACS） | 分选机时 **600–800 元/小时**（清华各台）；分析 **40–60 元/管**；无菌管路制备 1000 元/次；校外 300–800 元/h；开机费 200 元 | 酵母/噬菌体展示富集与单细胞分选的上机成本 | yqgx.tsinghua.edu.cn（多个仪器页）；ketao.tten.cn；dygx.xidian.edu.cn；clab.smu.edu.cn | 价目表 |
| FACS 速度上限（设备规格） | FACSAria III：分析 100,000 事件/s、分选 70,000 细胞/s、纯度 >98% | 决定"10^7 级库 + 多轮分选"是否可行 | dygx.xidian.edu.cn 设备页（厂商标称） | 公司自述 |

**每候选"合成＋表达＋纯化＋一次单点结合"的总边际成本（本报告推算）**：
- 输入：DNA 用芯片池 ≈ $0.3–4/构建体（10.1371/journal.pbio.3003645、12¢/bp 价目表）；表达/纯化耗材与 2 mL 培养 → 论文口径"约等于几条寡核苷酸"（10.1038/s41467-026-76740-9）；单点 BLI 机时摊薄 < $3（100 元/h ÷ 96 样）。
- 结论区间：**自建微规模管线 $5–50/候选（不含人力）**；若加 SPR 动力学＋ITC 定量，则升到 **$200–1,000+/候选**（机时 300 元/h × 数小时 + 芯片 1,600 元 + ITC 5,300 元/对）。
- 人力与日历时间是真正的瓶颈：SAPP 明确说传统流程"几十个设计要花数周"。

---

## 二、计算成本表（每候选）

| 计算动作 | 每候选成本 | 出处（原文口径） | 备注 |
|---|---|---|---|
| Rosetta 序列设计（全组合优化） | **~350 CPU-s** | Bennett et al., Nat Commun 2023, 10.1038/s41467-023-38328-5："ProteinMPNN is very fast, generating a sequence for a minibinder backbone in ~2 CPU-s compared to ~350 CPU-s for Rosetta-design" | 同文给出效率指标：Rosetta-design ≈ **7.6×10⁻⁷ 个成功设计 / CPU-s**（换算因子 100 CPU-s = 1 GPU-s） |
| 大规模 binder 设计（dock-and-design 全跑） | **~100,000 CPU·小时 / 10 万个设计**（即约 1 CPU·小时/设计） | Cao et al., Nature 2022, 10.1038/s41586-022-04654-9："CPU time requirements to produce 100,000 designed binders to be tested experimentally were typically around 100,000 CPU hours (usually at least ten times as many binders were computationally designed than were ordered)" | 同时给出"计算量→下单量"的 10 倍漏斗惯例 |
| ProteinMPNN 序列生成 | **~2 CPU-s**（原文另有 1.2 s vs 4.3 min/100 残基 的对比口径） | 10.1038/s41467-023-38328-5；10.1126/science.add2187（Science 2022） | 序列端已不是瓶颈 |
| ProteinMPNN + Rosetta FastRelax 循环 | **~120 CPU-s/设计**，其中 **6.6%** 过 AF2 过滤 → 效率 **2.2×10⁻⁶ 成功设计/CPU-s**，较 Rosetta-design 平均提 **~8 倍** | 10.1038/s41467-023-38328-5 | 折中方案：物理端做局部精修 |
| AlphaFold2 复折叠（过滤用） | **~30 GPU-s/设计**，且**仅 ~2.3% 设计通过** | 10.1038/s41467-023-38328-5："the AF2 filter is computationally expensive (~30 GPU-seconds per design) and only ~2.3% of designs pass" | 用的是"减少 MSA＋initial guess"的加速配置 |
| AlphaFold2（ColabFold 常规全流程） | **单 GPU 服务器约 1,000 结构/天**（≈ 86 GPU-s/结构的量级，本报告按 24 h 折算）；MSA 搜索比 AF2 原生快 **40–60 倍**、单条预测整体快约 **5 倍** | Mirdita et al., Nat Methods 2022, 10.1038/s41592-022-01488-1 | "1000/day"是论文原句；单结构秒数为推算 |
| RFdiffusion 骨架生成 | **100 残基设计、15 步采样、约 11 s（NVIDIA A4000）**，且减少步数常不降低 in silico 成功率（>60%） | 10.1038/s41586-023-06415-8 | 生成端已便宜到"秒级" |
| 经典 MD（显式溶剂，云端 GPU） | AWS g5.2xl 在超大系统（核糖体 RIB）上 **7.55 ns/天**；CPU/GPU 实例间性能/价格差异显著，消费级 GPU + 便宜 CPU 组合性价比最好 | Kutzner C, Kniep C, Cherian A, et al., *GROMACS in the Cloud: A Global Supercomputer to Speed Up Alchemical Drug Design*, J Chem Inf Model 2022, 10.1021/acs.jcim.2c00044 | 一般 5–10 万原子蛋白体系更快（**未核实具体 ns/day，见第八章**）；若按此量级，1 µs 的超大体系需 **~132 GPU·天** |
| FEP/ABFE（相对/绝对结合自由能） | "小时级"每配体计算；**端态法（MM/PBSA、MM/GBSA）单样耗时与 alchemical ABFE 相当，但少用一个数量级的节点数**；加空间约束需更多 λ 窗、**成本再升最多 30%** | "The Last Mile Problem", J Chem Inf Model 2026, 10.1021/acs.jcim.6c00942 | 综述式对照表（Communicative & Integrative Biology 2026, 10.1080/19420889.2025.2603140）给出 **classical FEP：~50,000 原子、天级、MUE 0.9–1.5 kcal/mol**；QM/MM：~10,000 原子（QM 区 ~200 原子）、天级、0.8–1.8 kcal/mol |
| 硬件/集群口径 | 云端与自建集群"总成本（硬件＋人力＋机房＋能耗）大致相当，前提是选对实例" | 10.1021/acs.jcim.2c00044 | 说明"MD 便宜"依赖已有算力，不依赖美元 |

### 「MD 预筛 N 个候选 vs 合成测试 N 个候选」谁贵（本报告推算，输入均已在表内核验）

| 规模 N | 湿实验（自建微规模） | 显式溶剂 MD（每候选 200 ns） | 单候选一次 FEP |
|---|---|---|---|
| N = 100 | $500–5,000（＋数天人力） | 0.5–2 GPU·年量级取决于体系；按 g5.2xl 7.55 ns/d 为 **2,650 GPU·天** | 100–400 GPU·天 |
| N = 1,000 | $5,000–50,000 | **26,500 GPU·天** | 10^4–10^5 GPU·h |
| N = 10,000 | 已到 SAPP/展示库可吞的规模 | 比湿实验贵约 **两个数量级** | 完全不可行 |

结论（明确三态）：
- **能证明**：在"设计端"（RFdiffusion/ProteinMPNN/AF2 过滤，秒—分钟级）计算远便宜于合成测试；每候选 30 GPU-s 的 AF2 过滤 ≈ $0.1–0.5 量级，而每候选湿实验 $5–50。因此计算漏斗能把下单数从 10^5 降到 10^2–10^3（Cao/Bennett/RFdiffusion 原文数字见第一、三节）。
- **不能证明**：一旦进入"每候选 μs 级显式溶剂 MD 或 FEP"，计算成本与湿实验同数量级甚至更高（按上表）；此时用美元判断不如用**日历时间与人力**判断：湿实验受克隆/表达/纯化周节奏限制，计算只要排得上队就能并行。
- **尚缺什么**：缺少一篇公开、可复现、以"每候选 GPU·小时 × 云单价"直接对比"每候选美元"的基准论文；见第八章。

---

## 三、判据→实验相关的定量证据（逐条）

### 3.1 结构自洽性判据（AF2/RF2）是最强的实验命中预测器

- **论文**：Bennett NR, Coventry B, Goreshnik I, et al. *Improving de novo protein binder design with deep learning.* Nat Commun 2023. DOI **10.1038/s41467-023-38328-5**（Crossref 核验）。
- **统计量/原文**：
  - "increases design success rates nearly **10-fold**"（回顾＋前瞻两套实验）。
  - 前瞻：AF2 过滤库相对物理过滤库的成功率为 **8 倍（LTK）与 30 倍（IL-2Rα site 1）**；且 AF2 过滤让物理法完全失败的靶点（ALK、IL-10Rα）拿到了命中。
  - 判据阈值："sharp increases in success rates for designs with **pAE_interaction < 10**"；过滤条件为 pAE_interaction<10 且 af2_complex_rmsd<5 Å。
  - 池规模漏斗："~2 million designs per target → ~20,000 to be experimentally tested（~15,000 物理过滤 + ~5,000 AF2 过滤）"，最终池 9 K / 2 K / 2 K。
  - 失败归因（原文分类）："Type I failures"（序列不折叠成设计态）与 "Type II errors"（设计态本身不会结合）——"The excellent performance of both AF2 and RF2 on the binder discrimination task strongly suggest that **Type II errors are primarily responsible** for the low success rates of Cao et al."
  - 自限：即便全套过滤，"success rates among the targets remain low (**<1%**)"。
- **意义**：这是目前最接近"哪个计算判据最能预测实验成功"的对照实验答案——界面 pAE/复合物 RMSD（即 AF2 自洽性）显著优于 Rosetta 物理打分，且给出了**成本**（30 GPU-s/设计、2.3% 通过率）。

### 3.2 生成模型升级 + AF2 过滤的"两个数量级"分解

- **论文**：Watson JL, Juergens D, Bennett NR, et al. *De novo design of protein structure and function with RFdiffusion.* Nature 2023. DOI **10.1038/s41586-023-06415-8**。
- **原文数字**："For IL-7Rα, InsR, PD-L1 and TrkA, RFdiffusion has success rates roughly **two orders of magnitude higher** than the original design campaigns. **We attribute one order of magnitude to RFdiffusion, and the second to filtering with AF2**"；总体实验成功率 **19%**；MDM2 螺旋支架：**96 个设计中 55 个结合**；每靶点测试"<100 个设计"而非此前的数千个；"high-affinity binders can be identified from dozens of designs, in many cases **eliminating the requirement for slow and expensive high-throughput screening**"。
- **意义**：明确论证"便宜的计算闸口（AF2 过滤）＋更好的生成器"共同消灭了昂贵的展示库环节。

### 3.3 迭代"计算↔实验"能把命中率从 6% 提到 47%（非 MD 驱动，而是打分/协议迭代）

- **论文**：Rocklin GJ, Chidyausiku TM, Goreshnik I, et al. *Global analysis of protein folding using massively parallel design, synthesis, and testing.* Science 2017. DOI **10.1126/science.aan0693**（摘要经 PubMed E-utilities 实取）。
- **摘要原文**："combined computational protein design, next-generation gene synthesis, and a high-throughput protease susceptibility assay to measure folding and stability for **more than 15,000 de novo designed miniproteins**, 1000 natural proteins, 10,000 point mutants, and 30,000 negative control sequences… **Iteration between design and experiment increased the design success rate from 6% to 47%**"。
- **意义**：命中率提升的最硬历史范例来自**并行湿实验（蛋白酶解 + 测序读出）+ 打分迭代**，不是 MD/QM。

### 3.4 判据失灵边界：抗体–抗原体系（AF2 不可靠的定量证据）

- **论文 A**：Yin R, Feng X, Varshney D, Pierce BGT. *Benchmarking AlphaFold for protein complex modeling reveals accuracy determinants.* Protein Sci 2022. DOI **10.1002/pro.4379**。
  - 数字：152 个异源二聚体基准；AlphaFold **top-1 有 43% 达 medium 及以上**（可接受及以上约一半：51%），而**未结合态 docking（ZDOCK）仅 9%**；但"AlphaFold modeling of antibody–antigen complexes within our set was unsuccessful"；AF-Multimer 在新一批 Ab–Ag 结构上 **成功率 11%**，TCR–抗原同样失败。
- **论文 B**：Yin R, Pierce BG. *Evaluation of AlphaFold antibody–antigen modeling with implications for improving predictive accuracy.* Protein Sci 2024. DOI **10.1002/pro.4865**。
  - 数字：**427 个非冗余 Ab–Ag 复合物**；top-1：acceptable+ **26%**、near-native(medium+) **18%**、high **5%**；用全部 25 个模型则 37%/22%/6%；"the latest version of AlphaFold improves near-native modeling success to **over 30%, versus approximately 20%** for a previous version, while increased AlphaFold sampling gives **approximately 50%** success"；"The default AlphaFold model confidence score was found to be **well correlated with antibody–antigen model accuracy**"。
- **论文 C（产业端后果）**：*Atomically accurate de novo design of antibodies with RFdiffusion.* Nature 2026. DOI **10.1038/s41586-025-09721-5**†。
  - baker.md 已核录的原文：对多个靶点 "success rates … range from **0% to 2%**"；作者找到 **AF3 ipTM 对结合有预测力（AUC = 0.86）**，但"only **9%** of our ordered VHH designs have an ipTM > 0.6"；scFv 端 "only **4%** of the initial design library has ipTM > 0.85, whereas **5 of the 6** experimentally confirmed designs pass this threshold"。
  - **意义**：这是"加入新判据（ipTM 阈值）本可提升命中率"的定量缺口证明，也解释了为什么抗体设计还得回到展示库（9,000 设计/靶）。

### 3.5 物理 ΔΔG 判据对实验功能分的预测力其实很弱（关键否定性定量证据）

- **论文**：Gerasimavicius L, Livesey B, Marsh JA. *Correspondence between functional scores from deep mutational scans and predicted effects on protein stability.* Protein Sci 2023. DOI **10.1002/pro.4688**（Crossref 核验）。
- **原文数字**："the overall correlations tend to be fairly low, with the **average rho values throughout the benchmark at 0.26 and 0.28 for ΔΔG and \|ΔΔG\|**, respectively"；Rosetta ΔΔG 与多个 DMS 数据集平均 Spearman 仅 **0.25**；**FoldX 与 Rosetta 最强**；二者取平均的 **"Foldetta" 共识分比最好单工具再高约 0.15 个 rho**，可与 EVcouplings/SNAP2 等专用变异效应预测器匹敌甚至超过（对 abundance 型 DMS）；DMS 数据集之间自身平均 Spearman ≈ **0.66**（说明噪声上限）；预测器两两一致性平均 |rho| ≈ **0.49**。
- **意义**：对"用单个物理分数（ΔΔG/ddG）筛设计"给出**量化的低预期值**；共识/集成打分比单点阈值更可靠；也说明"abundance/表达型读数"最容易被稳定性预测器解释，"活性型读数"最不容易。

### 3.6 结合自由能（FEP/端态法）与实验的相关性（蛋白–配体侧最硬的对照）

- **论文**：*The Last Mile Problem: A Critical Assessment of Physics-Based and AI Tools for Small Molecule Binding Prediction in Virtual Screening.* J Chem Inf Model 2026. DOI **10.1021/acs.jcim.6c00942**（Crossref 核验，OA 全文 PMC13213910）。
- **原文统计量**：alchemical **ABFE 与实验 BFE 的 Pearson r = 0.73（无约束）→ 0.77（加约束）**，但加约束"increases the computational cost by up to **30%**"；同一靶点内部（intratarget）相关性 **Pearson 0.44–0.75、Spearman 0.19–0.74**，即"精度依赖具体复合物，不能事前评估某一次 ABFE 是否可信"；端态法（MM/GBSA、MM/PBSA）"scored well in recognizing actives from decoys in DUD-E but showed **little correlation with experimental values in PDBbind**"；ML 打分（GNINA、RF-Score-VS）相关性最弱；结论建议**分级：AI 模型（Boltz-2）做主过滤 → 只对少量候选上 alchemical ABFE**；并明确指出"the cost of running alchemical simulations for hundreds of ligand–protein complexes is likely to remain significant"、"the costs per compound in this final step are **orders of magnitude higher** than in all previous steps"。
- **对照综述的量化表**（作者估算）：Niazi S. *Quantum mechanics in drug design: Progress, challenges, and future frontiers.* Commun Integr Biol 2026. DOI **10.1080/19420889.2025.2603140**：Docking 2.5–3.5 kcal/mol MUE / 分钟级；MM/PBSA 1.5–2.5 / 小时级、~10^5 原子；**Classical FEP 0.9–1.5 / 天级、~5×10^4 原子**；QM/MM 0.8–1.8 / 天级、~10^4 原子（QM 区 ~200）；纯 QM 0.5–1.5 / 小时—天、**~500 原子**；"optimal performance zone (<1.0 kcal/mol error, **<1,000 GPU hours**)"；"targeted applications … yield the highest return on computational investment"。
- **前瞻性验证**：*Prospective Evaluation of Structure-Based Simulations Reveal Their Ability to Predict the Impact of Kinase Mutations on Inhibitor Binding.* J Phys Chem B 2025. DOI **10.1021/acs.jpcb.4c07794**†——把结构基模拟用于**预测突变对抑制剂结合的影响**（OA 全文本次未取到，统计量待补）。
- **蛋白–蛋白 FEP 的现状**：本次检索**未找到**把 alchemical FEP 系统用于从头设计蛋白–蛋白结合体、并给出与实验 Kd 的 RMSE/相关系数的公开基准论文（最接近的是综述性方法学对照与 10.1021/acs.jcim.6c00089† OpenFE 大规模协作评测）。已写入第八章。

### 3.7 "置信度指标 ≠ 热力学稳定性/可实验折叠"的明确论述

- **论文（综述）**：Li W, Cadet X, … de Brevern AG, Cadet F. *Diffusion-Based Protein Structure Design: Geometric Modelling, Validation Strategies, and Thermodynamic Challenges.* Int J Mol Sci 2026. DOI **10.3390/ijms27167151**。
- **原文短句**："A high pLDDT value indicates that the predictor is confident in the local geometry, but it **does not provide direct evidence that the sequence is thermodynamically stable, experimentally foldable, or functionally active**"；"ensemble-oriented diffusion models must be **validated against molecular simulations, experimental observables, or independently estimated free-energy landscapes** before thermodynamic or kinetic interpretations can be assigned"；"A generated sequence or structure may appear computationally designable, yet exhibit **poor recombinant expression, limited solubility, aggregation, chemical instability, proteolytic sensitivity, immunogenicity or unsuitable oligomerisation**"；并呼吁基准报告"computational cost, software versions, random seeds and candidate-selection procedures"。

### 3.8 命中率区间的"共识口径"（用于报告锚定）

- **论文（综述）**：*AI-Driven De Novo Binder Design: From Structure Prediction to Closed-Loop Optimization.* Comput Struct Biotechnol J 2026. DOI **10.34133/csbj.0070**。
- **原文**："Even with these stringent in silico filters, designers should expect substantial false-positive rates: **typical experimental hit rates for de novo binders currently range from 1% to 10%, occasionally reaching up to 20% for highly favorable targets**, underscoring that computational scores enrich for success rather than guarantee it"；"initial computational screens for these targets yielded experimental hit rates of roughly **1% to 2% from tens of thousands of candidates**, which were subsequently matured to subnanomolar or picomolar affinities… via yeast display optimization"；筛选层级定义："Feasibility gate: Drop low-expression, insoluble designs early → L1: high-throughput binding screen (phage or yeast display) → expression/SEC/Tm → SPR/BLI"。

### 3.9 其他已定位但本次未展开精读的判据类文献（供后续补充）

- **PPIscreenML**：Mischley V, Maier J, Chen J, Karanicolas J. *PPIscreenML is a method for structure-based screening of protein-protein interactions using AlphaFold.* eLife 2026, DOI **10.7554/elife.98179**；预印本 10.1101/2024.03.16.585347。用 AF2 置信度描述子 + Rosetta 能量项训练分类器判别"两个蛋白是否相互作用"，"outperforms methods such as **pDockQ and iPTM**"，并在 TNFSF 配体/受体选择性上正确复现——把"能不能筛互作对"从打分阈值变成监督学习问题。
- **非 Baker 系的命中率基线（独立实验室）**：*A Complementarity-Based Approach to De Novo Binder Design*, Adv Sci 2025, DOI **10.1002/advs.202502015**（Crossref 核验，OA 全文 PMC12412469）。原句："this approach required the screening of **thousands of candidates** in order to identify a few nanomolar binders"；对"表面指纹 + 深度网络"路线自评 "has also resulted in a **low success rate (<1%)**"；其互补性检索在"数万张 subject map"中**>70% 的情形**能把正确配对排进前 100；产物 nanoDSF 熔解温度多数 **>100 °C**（作者实测）。
- **Scaffold-Lab**（PLoS Comput Biol 2026，DOI **10.1371/journal.pcbi.1014290**）：统一框架内对骨架生成方法做批判性排序评测。
- **AF3 基准**（Brief Bioinform 2025，DOI **10.1093/bib/bbaf616**）。
- **结构质量对自由能精度的影响**（J Chem Inf Model 2025，DOI **10.1021/acs.jcim.5c00947**†）。

---

## 四、QM 在蛋白设计中的真实用途边界

**能干什么（每条都有已核验文献）：**

| 用途 | 代表工作 / DOI | 说明 |
|---|---|---|
| theozyme（理想过渡态复合物）→ 反推催化位点 | Siegel JB et al., *Computational Design of an Enzyme Catalyst for a Stereoselective Bimolecular Diels-Alder Reaction*, Science 2010, **10.1126/science.1190239** | QM（Houk 组过渡态几何/能量）生成"theozyme"几何，再交给 Rosetta 建库；QM 只作用于**十几个原子的反应中心** |
| 设计酶的催化机理核验（势垒/步序） | De Raffele A, Martí N, Moliner S, *QM/MM Theoretical Studies of a de Novo Retro-Aldolase Design*, ACS Catal 2019, **10.1021/acscatal.8b04457** | 对**已设计出来**的酶做 QM/MM 能垒计算，解释为何慢；这是"事后机理"而非"事前筛库" |
| QM/MM 方法学总论 | Senn HM, Thiel W, *QM/MM Methods for Biomolecular Systems*, Angew Chem Int Ed 2009, **10.1002/anie.200802019** | 边界处理、嵌入方式、精度—成本折中 |
| 周期性 QM/MM MD（酶催化，GPU） | *Accurate QM/MM Molecular Dynamics for Periodic Systems in GPU4PySCF with Applications to Enzyme Catalysis*, J Chem Theory Comput 2025, **10.1021/acs.jctc.4c01698** | 现成 GPU 实现，但仍限于小 QM 区 |
| 生色团光化学/激发态 | *QM/MM Study of Substituent and Solvent Effects on the Excited State Dynamics of the Photoactive Yellow Protein Chromophore*, J Chem Theory Comput 2017, **10.1021/acs.jctc.6b01069**；*QM/MM Calculations on Excited-State Proton Transfer and Photoisomerization of a Red Fluorescent Protein mKeima*, Biochemistry 2024, **10.1021/acs.biochem.4c00586** | 激发态本质上是电子结构问题，经典力场不可用；QM 区仍是发色团 + 第一壳层 |
| 金属位点参数化 | *Estimation of Transition-Metal Empirical Parameters for Molecular Mechanical Force Fields*, JCTC 2016, **10.1021/acs.jctc.6b00416**；*Computational Design of Multinuclear Metalloproteins Using Unnatural Amino Acids*, Methods Mol Biol 2016, **10.1007/978-1-4939-3569-7_10**；*Comparison of different approaches to derive classical bonded force-field parameters for a transition metal cofactor… non-heme iron*, Theor Chem Acc 2021, **10.1007/s00214-021-02796-z** | QM 用来**拟合 MM 参数**，随后整套筛选仍在 MM 层——这是 QM 进入设计漏斗的"正规路径" |
| 电荷/质子化与力场参数 | *Non-bonded force field model with advanced restrained electrostatic potential charges (RESP2)*, Commun Chem 2020, **10.1038/s42004-020-0291-4**；*W-RESP: Well-Restrained Electrostatic Potential-Derived Charges*, JCTC 2021, **10.1021/acs.jctc.0c00976**；*Fast, efficient generation of high-quality atomic charges. AM1-BCC model: II*, J Comput Chem 2002, **10.1002/jcc.10128**；组氨酸等质子化态：constant-pH MD 力场基准 *Protein Titration Benchmark of CHARMM36, Amber99sb-ildn, Amber14sb, OPLS-AA/M, and Martini 2 Force Fields for Constant pH Molecular Dynamics in GROMACS*, JCTC 2026, **10.1021/acs.jctc.6c00678**（Crossref 核验）；晶体质子化态 **10.1021/acs.jpcb.4c05947**† | QM 定残基/配体电荷、pKa 环境依赖态；QM/MM 综述原句："Histidine residues in enzyme active sites frequently exhibit context-dependent protonation states that **classical force fields cannot reliably predict**" |

**为什么不能拿 QM 筛上万个全蛋白候选（可核验的尺度论据）：**
- 综述定量表（10.1080/19420889.2025.2603140，作者估算）：纯 QM 体系上限 **~500 原子**、QM/MM 全体系 **~10,000 原子且 QM 区 ~200 原子**、DFT 标度 **O(N³)**、"method-dependent accuracy ~500 atoms, 0.5–2.0 kcal/mol"；对 2 万原子的 200 残基蛋白–蛋白复合物，QM 连"一次能量评估"都不现实。
- 该综述同时给出可操作结论："**targeted applications** to metal-containing systems, covalent modifications, and polarization-dominated interactions yield the **highest return on computational investment**"——即 QM 只在化学键生成/断裂、电子效应占主导的**局部**用。
- 现实路径（已在文献中成型）：QM → 提取参数（电荷、金属配位几何、力常数）→ 交给 MM/Rosetta/MD 在全蛋白尺度上做大规模筛选；QM/MM 综述亦指出"strategies typically reduce computational costs by **10–50×** compared to complete DFT while maintaining chemical accuracy in the region of interest"（QM 区截断、point-charge embedding 等）。

---

## 五、廉价高通量湿筛技术清单

| 技术 | 可达规模 / 通量（口径） | 每候选边际成本量级 | 局限 | 出处 |
|---|---|---|---|---|
| 酵母表面展示（YSD）＋ FACS | 单批筛 **9,000 设计/靶**（实测）；常规库 10^7 级 | 池化 DNA + 培养 + 抗体标记，$1–5/候选（本报告按价目表组件推算）；分选机时 600–800 元/h | 单体/寡聚体非共价组装**不适用**；显示量与折叠态混淆 | 10.1038/s41586-025-09721-5†；10.1038/s41592-025-02975-x†；10.1038/s41467-026-76740-9（"非共价寡聚体本质上不适合展示"）；分选价目表 yqgx.tsinghua.edu.cn |
| 芯片合成 DNA → 阵列化表达（SAPP/DMX） | **数百样/天**；192 反应克隆 2 h；SEC 瓶颈 ~300 样/台/天；基因合成成本再降 **5 倍** | "≈几条寡核苷酸/构建体"（作者口径） | 需要液滴/机器人 + 层析机；SEC 为瓶颈 | **10.1038/s41467-026-76740-9** |
| 无纯化裂解液直测（FIDA） | 每候选**一次毛细管读数**；表达后 **1 天内**出命中；热裂解纯化度高于去垢剂法 | 未纯化 → 省去柱层析与浓缩；样品 µL 级 | 依赖 ΔRh（尺寸变化）；需统计检验与重复，重复会吃掉通量 | **10.1002/pro.70286**；协议 10.17504/protocols.io.j8nlkyo5dg5r/v1† |
| 单点 BLI/SPR 筛（96/384 板） | Octet 96 样动力学 5 h（R4）–>19 h（R2）；Biacore 8K 高通量位点 24 h 约 8,800 相互作用 | 机时 $14–42/h；单样摊薄 $0.7–3（本报告推算） | 需固定化或标签；假阳性/传质限制；仍需蛋白量 | 价目表 im.cas.cn / cszx.scau.edu.cn；厂商 sartorius / antpedia 仪器页 |
| 测序式并行互作读出（MP3-seq） | 单次 **>100,000 个 PPI** | 主要是测序与培养成本 | 需兼容测序条形码体系；测"是否互作"而非亲和力 | **10.1038/s41589-024-01718-x** |
| 蛋白酶解 + 测序的大规模稳定性测（DMS/Proteomics 型） | 一次 **>15,000 设计 + 10,000 点突变 + 30,000 阴性对照**（实测） | 芯片池 DNA（<$0.001/base）＋测序；规模化后极低 | 读出为"稳定性/丰度"代理，不直接给功能 | **10.1126/science.aan0693**；成本口径见 **10.1371/journal.pbio.3003645** |
| 条码化质粒 DMS 文库构建（低成本方案） | 面向大基因；用 oPools 代替 dsDNA 合成（**~100× 便宜**） | <$0.001/base 合成 + 短读长测序 | 基因大小→文库复杂度；条形码与变体的对应噪声 | **10.1371/journal.pbio.3003645** |
| 体外展示（核糖体/mRNA 展示） | 可拿到 pM 亲和力的全合成抗体（经典实例） | 无细胞表达，避开转化瓶颈 | 库规模数字本次未从一手原文核到（见第八章） | **10.1038/82407**（Hanes & Plückthun, Nat Biotechnol 2000） |
| 液滴微流控（单细胞/单分子区室化筛选） | 论文标题即"ultrahigh-throughput"，可把 10^6–10^8 区室并行处理；数字未逐一核到一手原文 | 试剂体积极小，但需自制装置 | 区室内反应与天然条件差异、读出偏置 | 已定位：10.1016/bs.mie.2020.06.002（Methods Enzymol 章节）；10.1021/jacs.5c04962（Droplet 细胞表达多重筛选）†；10.1021/acs.analchem.5c01029† |
| 热稳定/聚集快速表征 | nanoDSF（Prometheus）**100 元/h**、DLS **50 元/样** | 每样 µL 级、无需纯化 | 只给 Tm/聚集信号，不给结合 | im.cas.cn 价目表 |

---

## 六、失败模式 → 对应计算判据 映射表

| 失败模式（实验观察） | 现场证据 | 能拦截它的计算判据 | 判据的可靠度（有无定量证据） |
|---|---|---|---|
| **完全不表达/低表达** | Cao 2022 中"少于 10 个 binder 来自 10 万个设计"的靶点（TIE2、CD3δ）；Bennett 后仍 <1% | 无成熟通用判据。可用：疏水表面重排（减少暴露非极性）、净电荷/极性再分配；ProteinMPNN 似然/伪似然 | **未证实**：本次未找到"MPNN 伪似然 ↔ 实验表达率"的定量相关研究（第八章缺口 2）。SAPP 明确用"先丢弃低表达/不溶设计"作为最前置可行性闸（10.34133/csbj.0070 原文："Feasibility gate: Drop low-expression, insoluble designs early"） |
| **包涵体/不溶** | RFdiffusion："一半无条件设计可溶表达" | 序列疏水性、暴露 β-链倾向、CamSol 型 pH 依赖溶解度预测（**10.1093/bib/bbad004**）、Aggrescan/Aggrescan4D（**10.1002/pro.5180**；AGGRESCAN 二十年评述 **10.1007/s12551-025-01404-9**） | 部分证据：这些工具针对"溶解度/聚集倾向"验证过，但**未见其用于从头设计命中率提升的前瞻对照** |
| **聚集/多分散** | 小 β 桶设计论文："**74%** 的可溶表征设计是寡聚体，**40%** 的表达设计发生聚集"（**10.1073/pnas.2207974120**） | 表面 Cβ 相互作用打分（SAP）、Rosetta 全原子能量＋界面 CMS 约束；对称/寡聚态预测 | 有对照值：SEC 表观寡聚态与模型一致率（87–126/608，10.1038/s41586-023-06415-8）——即"SEC 是最便宜的结构性真值" |
| **错折叠（设计态不是最小自由能态，Type I）** | Bennett 原文定义 Type I 失败并用 AF2/RF2 单链置信度（pLDDT、复折叠 RMSD）识别 | **AF2/RF2 复折叠 pLDDT + Cα RMSD 到设计模型**；ProteinMPNN 重设计后再折叠 | 有定量证据（3.1）：pAE_interaction<10 使成功率跳升；"discrepancies between design models and AF2 or RF2 structure predictions"可识别 Type I |
| **折叠正确但界面不结合（Type II）** | Bennett："Type II errors are primarily responsible for the low success rates of Cao et al." | **界面 pAE_interaction / ipTM / 复合物 RMSD**（AF2/RF2/AF3）；PPIscreenML 型监督分类 | 强证据（3.1、3.9）；AF3 ipTM 对结合命中 **AUC = 0.86**（10.1038/s41586-025-09721-5†） |
| **热稳定性不足（成药性）** | IJMS 综述："high pLDDT … does not provide direct evidence that the sequence is thermodynamically stable"（**10.3390/ijms27167151**） | ΔΔG 类物理打分（FoldX/Rosetta）**预测力弱**：与 DMS 功能分平均 Spearman 仅 **0.26–0.28**；共识分 Foldetta **+0.15** | 直接量化证据：**10.1002/pro.4688**；结论——别指望单一 ΔΔG 阈值，用集成＋湿实验 Tm（nanoDSF） |
| **催化位点未预组织（酶）** | 丝氨酸水解酶设计：**仅 1.6%** 通过 AF2 RMSD 过滤的设计被 PLACER 判为预组织；经 PLACER 四态过滤后测 11 个 **10 个有活性（91%）**〔转引自本项目 `sources/baker.md` [B17]，原文摘录，**本次未独立核对全文**（该文目前只检索到预印本 10.1101/2024.08.29.610411，无 OA 全文）〕 | PLACER 构象系综预组织指标；theozyme 几何约束；RFdiffusion2 原子级 active-site scaffolding | 命中率数字（4/96→11/96；1/96→11/96）同为转引；RFdiffusion2 的 DOI 已核验：**10.1038/s41592-025-02975-x** |
| **柔性/IDP 靶：几何对了但不结合** | IDP binder 设计（baker.md [B21]）命中率 3/94、5/78，亲和力停在数百 nM；TNFR 平坦极性表面"用 scaffold 引导的常规做法 little success"（10.1126/science.adp1779） | 需要系综/多态生成与"ensemble-aware confidence metrics"（综述原话）；单帧 AF2 不足 | 综述指出方向但无定量阈值（10.34133/csbj.0070） |
| **翻译后修饰/二硫键/糖基化意外** | 综述列举 developability 失败："chemical instability, proteolytic sensitivity, immunogenicity"（10.3390/ijms27167151） | 序列 motif 级规则（去除非预期 sequon、自由半胱氨酸计数）＋质谱确证 | 未见针对"从头设计命中预测"的定量研究（第八章缺口 4） |
| **抗体类：设计端 ipTM 失灵** | "only 9% of ordered VHH designs have ipTM>0.6"；需要展示库 + OrthoRep 误差校正亲和成熟 | 抗体专用共折叠模型 / ipTM 过滤 / 展示库回退 | 有原始数字（3.4） |

---

## 七、公司自述的循环通量与成功率（全部标注为公司自述，未见公开审计）

| 公司 | 公开可核到的表述 | 类型 / 出处 | 可信度评注 |
|---|---|---|---|
| Profluent | 1）"AI 设计基因编辑器（OpenCRISPR-1），公司称其为**首个完全由 AI 从头设计**的基因编辑器，2025 年 7 月发表成果"；2）融资稿称模型工作流"省去传统试错式实验的 **90% 以上时间成本**"（B 轮 $106M，2025-11）；3）数据集规模"超过 **1,150 亿条**蛋白序列" | 公司自述（Business Wire 稿 + 中文转载；baike/huxiu 二次转述） | "节省 90% 时间"为营销口径，**无对照实验与分母**；本轮未能在 Crossref 核到 OpenCRISPR-1 原始 Nature 论文的 DOI（见第八章 7） |
| Xaira Therapeutics | 融资与报道稿：$1B 种子轮；西雅图团队做设计、湾区团队做测试；"实验室用高通量机器合成并测试大量设计，数据快速回流模型迭代"（DBTL）；技术底座为 RFdiffusion/ProteinMPNN/RFantibody | 公司自述＋媒体（techlifesci、sina/163 转述） | **未披露**每周构建体数、命中率、周期天数等可核算指标 |
| Generate:Biomedicines | Flagship 融资稿标题"raises $370 million for de novo protein design"（C&EN 记录，DOI 10.47287/cen-09942-buscon15） | 媒体 | 无公开通量/命中率数字 |
| Iambic Therapeutics | 已定位与 Baker 系同源的"从头设计胰岛素受体激动剂"结构证据（PDB **10.2210/pdb9dn6/pdb**、**10.2210/pdb9dnn/pdb** 等；糖尿病相关会议摘要 **10.2337/db25-2148-lb**†） | 结构数据库记录（可核） | 不是通量表述；本次**未找到** Iambic 公布的"每周期构建体数/命中率" |
| Nabla Bio / Morphic | 本次未检索到可核验的通量或成功率数字（Crossref 与 Europe PMC 的作者单位检索接口在本次会话返回错误） | — | 明确记为未核实 |
| 行业锚点（对照用） | "一个蛋白结构平均约 **10 万美元 + 数月到数年**"（AI 出现前的实验成本） | 中文科普转述（163.com 2025-04），**未核到一手文献** | 只可作叙事锚，不可作证据引用 |

**报告可用的最强公司侧论证不是通量而是学术侧替代**：Baker 系论文给出的实测通量（SAPP 数百样/天、RFantibody 9,000 设计/靶展示筛、MP3-seq >100,000 互作/实验）比任何新闻稿都可核查，建议在正文用这些替代公司口径。

---

## 八、未能核实的问题清单（缺什么才能定论）

1. **"MD 精筛把命中率从 X% 提到 Y%"的正面原文**：本次检索（Europe PMC 相关性检索＋arXiv API＋Crossref）**未找到**把显式溶剂 MD 或 FEP 作为设计漏斗主闸口、并给出与"不用 MD"对照的命中率提升数字的论文。反向论证（因算力成本否弃 MD 作主筛器）与相邻证据是有的：10.1021/acs.jcim.6c00942（"last-mile"成本级差论证）、10.1080/19420889.2025.2603140（方法×精度×算力表）、10.1038/s41467-023-38328-5（AF2 过滤 30 GPU-s/设计、2.3% 通过，成本与收益都被量化）。**要定论需要**：一篇公开对照实验——同一批 RFdiffusion/ProteinMPNN 候选，随机分为"AF2 过滤后直接下单"与"AF2＋每候选 ≥200 ns 显式溶剂 MD 复筛"，报告两者下单数与命中数。
2. **ProteinMPNN 伪似然 ↔ 实验表达率/可溶率的相关系数**：未找到定量研究。**要定论需要**：以 MPNN 似然为自变量、SAPP/FIDA 表达与命中为因变量的回归（>10^3 候选，单靶点起步）。baker.md 记录 [B02] 提示 2019 年有过"MD+ML 当筛选器"的探索但未给湿实验命中率。
3. **蛋白–蛋白（大分子）体系的 FEP+ 定量表现**：仅找到蛋白–配体基准（ABFE Pearson 0.73–0.77、MUE 0.9–1.5 kcal/mol）与 OpenFE 大规模协作评测（10.1021/acs.jcim.6c00089†，本次未取到全文统计量）；另 10.1021/acs.jpcb.4c07794†（前瞻性用结构基模拟预测激酶突变对抑制剂结合的影响）已定位 DOI 但 OA 全文未取到，其 RMSE/相关系数**待补**。**要定论需要**：设计结合体的 ΔΔG 预测 vs 实测 Kd（≥100 对）的 RMSE/相关系数与失败模式分层。
4. **"设计失败原因分布"的系统统计**：现有证据是分散的单篇数字（40% 表达设计聚集、74% 可溶设计是寡聚体，10.1073/pnas.2207974120；Type I/II 划分，10.1038/s41467-023-38328-5；SAPP/DMX 的克隆与回收率）。**要定论需要**：跨靶点的统一口径失败分类（建议以"不表达 / 不溶 / 聚集 / 错折叠 / 界面不变形失败 / 稳定性不足 / 修饰异常"七类，配 nanoDSF＋SEC＋质谱的最小确证面板）。
5. **单候选湿实验成本的公开账本**：只有价目表（机时、耗材、芯片）＋论文通量口径，**没有**任何一篇论文给出"每构建体美元全成本（含人力）"。**要定论需要**：核心设施或公司发布按构建体计费的服务价目（现有 CRO 报价多为"询价"，本次未取到数字）。
6. **每候选 GPU·小时 × 云单价 ↔ 每候选美元 的统一基准**：已有零件（g5.2xl 7.55 ns/day 的超大系统、云与自建等成本结论、AF2 30 GPU-s/设计），但**缺一个把三者同口径化的公开基准**；本报告第二节给出的对比是"本报告推算＋输入可核"，不是文献结论。
7. **OpenCRISPR-1 原始论文 DOI** 与 Profluent 湿实验循环规模（每轮测多少构建体、命中率）：本次 Crossref/Europe PMC 未命中主论文记录。**要定论需要**：以 Nature 官方页面/PMID 直接核 DOI，再从方法部分提取"设计→突变→复测"的每轮样本量。
8. **各展示平台（phage/ribosome/mRNA/哺乳细胞展示/液滴）"每命中候选的边际成本"**：规模数字（10^7–10^14）在教科书与综述里常见，但本次**未逐一从一手原文核到**；仅核到了实测批次规模（9,000/靶、31,000 芯片合成、>100,000 互作、>15,000 设计）与合成单价（<$0.001/base）。
9. **欧洲/美国同步辐射与冷冻电镜付费机时**（本次核到的是中国设施＋日本 KEK）。**要定论需要**：Diamond/ESRF/ALS 的官方 fee schedule 页面（本次检索未命中）。
10. **中国核心设施价目表的时效**：清华晶体学平台页日期 2019-09、IBP SPR 通知 2010-08、遗传发育所规定 2021 年，均**可能已调价**；引用时应注明"公开收费页快照日期"。

---

### 附：本次经 API 实际核验的 DOI 清单（用于报告引文核对）

**Crossref 核验通过（主证据）**：
10.1038/s41467-023-38328-5；10.1038/s41586-023-06415-8；10.1038/s41586-022-04654-9；10.1126/science.adp1779；10.1126/science.aan0693；10.1126/science.add2187；10.1126/science.1190239；10.1002/pro.70286；10.1038/s41467-026-76740-9；10.1038/s41589-024-01718-x；10.1038/s41592-025-02975-x；10.1038/s41586-025-09721-5；10.34133/csbj.0070；10.3390/ijms27167151；10.1002/pro.4379；10.1002/pro.4865；10.1002/pro.4688；10.1002/pro.5180；10.1073/pnas.2207974120；10.1093/bib/bbad004；10.1093/bib/bbaf616；10.1007/s12551-025-01404-9；10.1080/19420889.2025.2603140；10.1021/acs.jcim.6c00942；10.1021/acs.jcim.2c00044；10.1021/acs.jctc.1c01214；10.1038/s41592-022-01488-1；10.1002/anie.200802019；10.1021/acscatal.8b04457；10.1021/acs.jctc.4c01698；10.1038/s42004-020-0291-4；10.1021/acs.jctc.0c00976；10.1021/acs.jctc.6b00416；10.1021/acs.jctc.6b01069；10.1021/acs.biochem.4c00586；10.1021/acs.jctc.6c00678；10.1002/jcc.10128；10.1007/978-1-4939-3569-7_10；10.1371/journal.pbio.3003645；10.1371/journal.pcbi.1014290；10.7554/elife.98179；10.1101/2024.03.16.585347；10.1038/82407；10.1007/978-1-0716-2285-8_2；10.1016/bs.mie.2020.06.002；10.1038/nmeth.f.202；10.1002/advs.202502015；10.47287/cen-09942-buscon15；10.1101/2024.08.29.610411（仅预印本记录）。

**仅 Europe PMC 侧列出、Crossref 未复核（引用前请再核）**：
10.1038/s41467-025-67866-3；10.1021/acs.jcim.6c00089；10.1021/acs.jpcb.4c07794；10.1021/acs.jcim.5c00947；10.1021/acs.jpcb.4c05947；10.1021/jacs.5c04962；10.1021/acs.analchem.5c01029；10.17504/protocols.io.j8nlkyo5dg5r/v1；10.2337/db25-2148-lb；10.1002/pro.70698；10.2210/pdb9dn6/pdb、10.2210/pdb9dnn/pdb（PDB 记录）。
