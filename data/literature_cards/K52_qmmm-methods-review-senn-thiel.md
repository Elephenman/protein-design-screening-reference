# K52 · QM/MM Methods for Biomolecular Systems（Senn & Thiel, Angew Chem Int Ed 2009，方法总论综述）（降级卡）

## 0. 元信息

| 项 | 内容 |
|---|---|
| CSV 编号 | K52（组：通用方法学） |
| 条目类型 | 综述（QM/MM 方法学总论）；本卡按降级口径写 |
| 标题／作者 | "QM/MM Methods for Biomolecular Systems" · Senn HM, Thiel W |
| 期刊／年份／DOI | Angew Chem Int Ed · 2009 · 10.1002/anie.200802019（CSV 行标 ✅Crossref核验） |
| 登记底稿 | `sources/cost-benchmarks.md` §四 表格〔QM/MM 方法学总论〕行 + §四 尺度论据段（10–50 倍与 point-charge embedding 句、His 质子化态句均登记于此） |
| 证据级别 | 摘要级／二级来源／未获正文（照 CSV 行） |
| 本卡性质 | 降级卡：只引底稿里确实存在的句子，不复建综述章节结构 |

## 1. 解决什么（一句话）

按 CSV 行口径：QM/MM 成本-精度折中的方法学依据——边界处理、嵌入方式、精度—成本折中三件事在这篇总论里成体系；时间线里它是"QM 只能局部用"这一论断的方法学出处（CSV 备注：策略通常较完整 DFT 省 10–50 倍算力，同时在关注区保持化学精度）。

## 2. 难点与应对

1. **2009 年的快照，覆盖不了今天的算力形态**。难点：底稿同时登记了 2025 年的周期性 GPU QM/MM MD 实现（K53 行），说明本篇的"成本折中"论述有时代边界。→ 作者做了什么：底稿未记录本篇内部对策，**本文未解决**。→ 我们的处置：时效问题用 K53（硬件加速）与 K56 行的电荷/pKa 工作交叉补，本卡只把该综述当方法学依据、不当现状依据。
2. **两条尺度数字是两种性质的口径，极易混用**。现象/证据：本行对应 "strategies typically reduce computational costs by" + "compared to complete DFT while maintaining chemical accuracy in the region of interest"（底稿记为 QM/MM 综述亦指出）；而 "method-dependent accuracy ~500 atoms, 0.5-2.0 kcal/mol" 出自 2026 年那篇方法综述、底稿明标**作者估算**。→ 处置：台账分两行标注口径与出处，引用时禁止把估算档位升级成实测。→ 代价：10–50 倍本身也只是综述陈述，我们没有任何一篇的实测加速比。
3. **底稿挂在另一行下的 QM/MM 综述原句，无法确认是否出自本篇**。现象/证据："Histidine residues in enzyme active sites frequently exhibit context-dependent protonation states that" 与 "classical force fields cannot reliably predict" 两句登记在 §四 表〔电荷/质子化与力场参数〕行，底稿只写 QM/MM 综述原句。→ 处置：本卡如实转引并标"底稿未指名哪篇 QM/MM 综述，本文未解决（无正文可验）"。
4. **无 OA 正文的取证困难与处置**。难点：无全文，章节、图表、原始论述位置全部不可核验。→ 处置：引句全部逐字取自 `sources/cost-benchmarks.md`；§3 只写取证流程；缺口不在本轮处理、也不新增缺口条目。

## 3. 取证方法与工作流程

| 步 | 输入 | 操作 | 判据／阈值 | 输出规模 |
|---|---|---|---|---|
| 1 | CSV 行 K52 + `sources/cost-benchmarks.md` §四 | 对表〔QM/MM 方法学总论〕行与尺度论据段逐项核对 | 标题、期刊（Angew Chem Int Ed 2009）、DOI 逐项一致；底稿标〔Crossref 核验〕 | 方法学定位 1 条 + 可引句 4 组 |
| 2 | 尺度论据段全文 | 拆分"哪句算本行口径、哪句属 2026 综述估算" | 底稿 170 行标"作者估算"的句子一律不加到本行名下 | 2 套口径表（第 4 节） |
| 3 | §四 表〔电荷/质子化与力场参数〕行 | 摘 His 质子化态引句并查归属 | 底稿未指名出处 → 卡内写"疑似本行综述，未确认" | 1 条带保留的引文归属 |
| 4 | 上述 + K53/K55/K56 交叉 | 落卡并限定用途 | 本行只供"分区与嵌入是标准折中"这一方法论依据，禁止供任何阈值 | CSV 行 K52 对应卡 1 张 |

## 4. 数字台账

| 数值 | 含义 | 出处 |
|---|---|---|
| 2009 / Angew Chem Int Ed / 10.1002/anie.200802019 | 题录（CSV 行标 ✅Crossref核验） | CSV 行与 §四 表行 |
| 10–50 倍 | QM/MM 分区策略相对完整 DFT 的成本节省——底稿记为 QM/MM 综述亦指出，属**综述陈述**（非任何一篇的实测加速比） | `sources/cost-benchmarks.md` §四 尺度论据段 |
| QM 区截断、point-charge embedding | 底稿给出的两类折中手段 | 同段括注 |
| ~500 原子；~10,000 原子全体系且 QM 区 ~200 原子；O(N³)；2 万原子复合物例 | 尺度上限档——**全部属 2026 综述（10.1080/19420889.2025.2603140）且底稿明标作者估算**，不挂在本行名下 | §四 尺度论据段首条 |
| 综述内部数值表：未记录 | 未获正文，本节只登底稿已有的句子级口径 | — |

## 5. 作者说了什么

底稿在本行名下记录：这篇总论覆盖边界处理、嵌入方式、精度—成本折中三件事；尺度论据段另以"QM/MM 综述亦指出"引出 "strategies typically reduce computational costs by" 与 "compared to complete DFT while maintaining chemical accuracy in the region of interest"。综述自身的分层论述、示例体系与误差表均未获正文，本节不复述底稿以外内容。

## 6. 我们（以下为推断）

- 本行是 K51/K53/K54/K55 四行的方法学锚点：分区与嵌入的可信度若立不住，其余各行"只在局部用 QM"的写法都失去依据。把握度中（题录与用途口径一致，内容未验）。
- 若 His 质子化态那句确出自本篇（归属未确认），则它对本项目的含义是：低介电活性位里的残基质子化态超出经典力场可靠预测能力——我们任何以 MM 静电做活性位判断的读数都必须带这条边界声明；本卡只把它用到"底稿所引 QM/MM 综述原句"这个强度。

## 7. 局限

- 2009 年时间点：不含周期性 GPU 实现（K53）、不含 RESP2 之后的电荷工作（K56）；综述陈述不可当现状。
- 无任何可复用的实测数值；10–50 倍是区间性陈述。
- His 引句归属模糊；底稿未给综述内页码或章节，无法回溯。

## 8. 迁移到我们的筛选／判定工作流

- **可用**：作为"QM 只作用于局部反应中心、全蛋白留给 MM"这一分工的总论依据；我们若自建机制层，按"QM 区截断 + 嵌入方式"框架申报自己的分区选择（写进 run.md 口径）。
- **不可用**：不许把 10–50 倍当我们 GPU/CPU 预算系数（它无我们引擎的接口数据）；**不许把综述的精度档位（0.5–2.0 kcal/mol 等，且部分为作者估算）当成我们的判定阈值**；不许引成本篇来论证我们可以对大规模候选做 QM 排序。

## 9. 溯源

- 唯一底稿：`sources/cost-benchmarks.md` §四（表格〔QM/MM 方法学总论〕行 + 尺度论据段 + 表〔电荷/质子化与力场参数〕行的综述原句转引）。本卡全部引句均出自该文件并逐字比对。
- 题录：DOI 10.1002/anie.200802019（CSV 行标 ✅Crossref核验）；无本地全文，本轮未做网络抓取。
- 自检：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K52" --no-report` 应报 PASS K52。

引句底稿: sources/cost-benchmarks.md

<!--CSV回填
work_type=综述（QM/MM 方法学总论；降级卡，未获正文）
target=生物分子体系（酶为主）的 QM/MM 分区计算：边界处理、嵌入方式、精度—成本折中
backbone_generation=不涉及（方法学综述，不产生候选）
computational_filters=不适用；本行提供分区与嵌入的方法学依据（QM 区截断、point-charge embedding）
thresholds=未记录（CSV 行阈值列为未记录；10–50 倍为综述陈述，非可复用阈值）
md_used=未记录（CSV 行该列为未记录；综述本身不跑 MD）
qm_used=是-化学步（照 CSV 行：QM/MM 处理化学步）
experimental_methods=无自跑实验；来源为综述（CSV 行文献类型=综述）
pipeline_counts=不适用（无候选漏斗）
hit_rate=不适用（综述无命中率）
best_metric=未记录（无性能读数；可引的最强口径只是精度—成本折中的陈述）
cost_or_stat_note=摘要级／未获正文；仅 Crossref 题录核验；10–50 倍属综述陈述、~500 原子与 0.5–2.0 kcal/mol 档属 2026 综述作者估算（底稿明标），两口径禁混用
role_in_timeline=QM/MM 成本-精度折中的方法学依据；QM 在蛋白设计中真实用途边界一节的总论支撑
source_pointer=sources/cost-benchmarks.md §四〔Crossref 核验〕；DOI 10.1002/anie.200802019
CSV回填-->
