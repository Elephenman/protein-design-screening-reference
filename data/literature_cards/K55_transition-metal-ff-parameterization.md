# K55 · 过渡金属经验力场参数拟合（JCTC 2016 + Methods Mol Biol 2016 + Theor Chem Acc 2021，一行三篇）（降级卡）

## 0. 元信息

| 项 | 内容 |
|---|---|
| CSV 编号 | K55（组：通用方法学） |
| 条目类型 | 方法，一行三篇（QM 拟合 MM 参数）；本卡按降级口径写 |
| 第一篇 | "Estimation of Transition-Metal Empirical Parameters for Molecular Mechanical Force Fields"（JCTC 2016，10.1021/acs.jctc.6b00416，本行 DOI 代表它） |
| 第二篇 | "Computational Design of Multinuclear Metalloproteins Using Unnatural Amino Acids"（Methods Mol Biol 2016，10.1007/978-1-4939-3569-7_10） |
| 第三篇 | Comparison of different approaches to derive classical bonded force-field parameters for a transition metal cofactor… non-heme iron（Theor Chem Acc 2021，10.1007/s00214-021-02796-z；底稿标题原样含省略号，本卡引句在省略号前截断） |
| 登记底稿 | `sources/cost-benchmarks.md` §四 表格〔金属位点参数化〕行（三篇均标 Crossref 核验）+ §四 尺度论据段 |
| 证据级别 | 摘要级／二级来源／未获正文（照 CSV 行） |
| 本卡性质 | 降级卡：覆盖三篇这一组，只引底稿存在且可逐字命中的句子 |

## 1. 解决什么（一句话）

按底稿口径：金属酶/金属结合体设计能做大规模筛的前提是 QM 只做参数化——用 QM 拟合 MM 参数（金属配位几何、键合力常数），随后整套筛选仍在 MM 层；底稿称这是"QM 进入设计漏斗的正规路径"。

## 2. 难点与应对

1. **一行三篇、且跨越 2016–2021 两代做法**。现象/证据：第一篇拟合通用过渡金属经验参数，第二篇直接拿非天然氨基酸做多核金属蛋白的计算设计，第三篇比较不同键合力场参数推导路线（非血红素铁）。→ 处置：卡内不合并三篇的任何数字或结论，只保留共同口径；每篇单独登记题录。→ 代价：三篇各自的拟合目标、参考数据规模全未获正文，本文未解决。
2. **金属参数化与通用蛋白力场（如 RESP2 一类非键拟合）是两套盲区**。难点：K56 行底稿记的那条"经典力场算不准金属配位/电荷转移"的原理性限制，其英文原句登记在〔电荷/质子化与力场参数〕行且归属 QM/MM 综述（见 K52 卡第 2 条），不能算到本行三篇头上。→ 处置：本卡不引那句，交叉引用 K52/K56 卡。→ 代价：金属位点参数化质量的可引证据在本卡仍是零。
3. **无 OA 正文的取证困难与处置**。难点：三篇的拟合流程、验证集、误差数字都拿不到，第二篇还是章节文集（Methods Mol Biol）——即使有 OA 也未必是原章。→ 处置：引句只用底稿命中的标题串；阈值一律未记录；缺口留在底稿体系，本轮不抓取。

## 3. 取证方法与工作流程

| 步 | 输入 | 操作 | 判据／阈值 | 输出规模 |
|---|---|---|---|---|
| 1 | CSV 行 K55 + `sources/cost-benchmarks.md` §四 | 对表〔金属位点参数化〕行核对三篇标题/期刊/年份/DOI | 三篇均标 Crossref 核验；本行 DOI=第一篇 | 3 行题录口径 |
| 2 | §四 表行说明列 | 提炼"QM 拟合 MM 参数 → 大规模筛选留在 MM 层"的流程口径 | 底稿未给任何数值 → 阈值数字=未记录 | 1 条正规路径表述 |
| 3 | 交叉比对 K52/K56/K18 类金属设计行 | 界定本组三篇在参数层的位置 | 不许把别行引文（如 His 质子化句）并入本卡名下 | 归属标注 3 条 |
| 4 | 上述 + CSV 空字段 | 落卡并限定用途 | 用途=金属位点参数化的存在性证据与流程口径；禁作排序/命中判据 | CSV 行 K55 对应卡 1 张 |

## 4. 数字台账

| 数值 | 含义 | 出处 |
|---|---|---|
| 2016 / JCTC / 10.1021/acs.jctc.6b00416 | 第一篇题录（"Estimation of Transition-Metal Empirical Parameters for Molecular Mechanical Force Fields"；本行 DOI 代表它） | `sources/cost-benchmarks.md` §四 表行 |
| 2016 / Methods Mol Biol / 10.1007/978-1-4939-3569-7_10 | 第二篇题录（"Computational Design of Multinuclear Metalloproteins Using Unnatural Amino Acids"） | 同段 |
| 2021 / Theor Chem Acc / 10.1007/s00214-021-02796-z | 第三篇题录（Comparison of different approaches to derive classical bonded force-field parameters for a transition metal cofactor，底稿标题在此后接省略号与 non-heme iron） | 同段 |
| QM → 提取参数（电荷、金属配位几何、力常数）→ MM/Rosetta/MD 层大规模筛 | 底稿记载的现实路径（三篇共同支撑的流程口径，无各自数值） | §四 尺度论据段 |
| 拟合误差/验证集规模：未记录 | 三篇正文均未获取 | — |

## 5. 作者说了什么

底稿在本行名下记录：QM 用来拟合 MM 参数（金属配位几何、键合力常数），随后整套筛选仍在 MM 层——这是 QM 进入设计漏斗的正规路径；第二篇标题层面自述用非天然氨基酸做多核金属蛋白的计算设计。三篇各自的拟合流程、参考数据与误差结论均未获正文，本节不复述底稿以外内容。

## 6. 我们（以下为推断）

- 本组是我们"金属位点判定"的方法论前提：金属 A/B 位几何这类判定要能在 MM/MD 层大规模跑，前提是配位几何与力常数被外部拟合过；判定本身既不由 QM 逐候选给出、也不由这三篇直接给出。把握度中。
- 第二篇（酶设计做多核金属蛋白设计）与我们酶设计-金属桥接场景直接同域——其标题本身即显示该场景的设计层在 MM+几何、QM 在参数层；但无正文，不能引它的任何成败读数。

## 7. 局限

- 三篇都只有标题级信息；无任何可引数字。
- 第二篇是方法丛书章节（Methods Mol Biol），即使后续补抓，可及性也最差。
- 第三篇标题原文含省略号（非血红素铁），引句只能在省略号前截断，标题完整性受损。

## 8. 迁移到我们的筛选／判定工作流

- **可用**：作为"QM 在我们项目里只做局部反应中心计算与参数拟合（金属配位几何、力常数），排序与大规模筛选留在 MM 层"这一分工的文献依据；我们金属位体系的参数来源声明可引本组为"正规路径"先例。
- **不可用**：不得用本组论证"我们的金属参数已可靠"——拟合质量读数全部未获正文；不得把任何 QM 精度档位（含 2026 综述作者估算的 0.5–2.0 kcal/mol）当成我们的判定阈值；不得写成金属酶设计成功率或命中率的来源。

## 9. 溯源

- 唯一底稿：`sources/cost-benchmarks.md` §四（表格〔金属位点参数化〕行，三篇均标 Crossref 核验 + 尺度论据段）。本卡全部引句均出自该文件并逐字比对；第三篇引句在底稿省略号之前截断，不跨省略号拼接。
- 题录：DOI 10.1021/acs.jctc.6b00416、10.1007/978-1-4939-3569-7_10、10.1007/s00214-021-02796-z（CSV 行标 ✅Crossref核验）；无本地全文，本轮未做网络抓取。
- 自检：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K55" --no-report` 应报 PASS K55。

引句底稿: sources/cost-benchmarks.md

<!--CSV回填
work_type=方法（一行三篇：金属位点 MM 参数的 QM 拟合与多核金属蛋白计算设计）
target=过渡金属辅因子/金属位点的力场参数（金属配位几何、键合力常数）；非血红素铁辅因子键合参数
backbone_generation=第二篇自述以非天然氨基酸做多核金属蛋白计算设计（标题级口径）；本组不产出筛选候选库
computational_filters=不适用；本组定位在参数层（QM 拟合 → MM 层大规模筛）
thresholds=未记录（CSV 行阈值列为未记录；三篇拟合误差全未获正文）
md_used=未记录（CSV 行该列为未记录；参数供 MM/MD 使用属底稿流程口径，非本组实测）
qm_used=是-力场参数化（照 CSV 行）
experimental_methods=底稿记"力场拟合 + 计算验证"（CSV 行）；无可核验湿实验信息
pipeline_counts=不适用（参数化研究，无候选漏斗）
hit_rate=不适用（非筛选研究；CSV 行标未记录）
best_metric=未记录（无参数误差或设计成功读数进底稿）
cost_or_stat_note=摘要级／未获正文；三篇均 Crossref 核验；本行 DOI 代表第一篇（JCTC 2016）；第二篇为 Methods Mol Biol 章节，可及性最差
role_in_timeline=金属酶/金属结合体设计能大规模筛的前提：QM 只做参数化，不做排序——QM 进入设计漏斗的正规路径
source_pointer=sources/cost-benchmarks.md §四〔三篇均 Crossref 核验；本行 DOI 代表第一篇〕；DOI 10.1021/acs.jctc.6b00416、10.1007/978-1-4939-3569-7_10、10.1007/s00214-021-02796-z
CSV回填-->
