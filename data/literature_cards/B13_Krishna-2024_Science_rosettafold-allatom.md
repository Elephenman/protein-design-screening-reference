# [B13] RoseTTAFold All-Atom：把建模与设计延伸到原子层（降级卡：未获正文）

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 第 14 行，编号 **B13**（组：Baker 组；`证据级别` 列原文即写 摘要级） |
| 题目 | Generalized biomolecular modeling and design with RoseTTAFold All-Atom |
| 作者 | Krishna R, Wang J, Ahern W, … Baker D（UW-IPD）（`sources/baker.md:173`） |
| 出处 | Science, 2024, 384: eadl2528 · DOI 10.1126/science.adl2528（✅Crossref）· PMID 38452047（无 PMC） |
| 正文取回状态 | ⛔ **未获正文**。`fetch_log.tsv:58`：EPMC search（EXT_ID:38452047，resultType=core）返回 `NO_OA_FULLTEXT`，注记 记录存在但无 PMCID（isOpenAccess=N）；`inventory.json` B13 项 local=[]、has_fulltext=false |
| 登记底稿（本卡唯一引句来源） | `sources/baker.md` 第 172–183 行（[B13] 卡段）；另参 第 673 行（§五 缺口 2：RFAA 的送测→命中分母未核实） |
| 证据级别 | **摘要级 / 未获正文**（与 CSV 行一致；本卡全部方法描述来自底稿转录的摘要句） |
| 未取到的部分 | 正文 Methods 的每靶点送测名额与命中率、全原子复合物置信度的具体阈值、最好的 Kd 数字（底稿 `:182` 原样记为 未给出 N/M/命中率数字，`:673` 缺口 2 同） |

## 1. 这篇解决什么（一句话）

**一句话**：把结构预测与生成模型从「只表示蛋白」升级到全原子（RoseTTAFold All-Atom / RFdiffusionAA），使围绕 digoxigenin、heme、bilin 这类小分子/辅因子的结合蛋白重新变得可建模、可设计、可筛选——修的是**筛选器本身失效**的问题，而不是某一场战役的命中率。

底稿记录的三层信息：① 设计对象=digoxigenin（地高辛）、heme、bilin 等小分子/辅因子结合蛋白（`:177`）；② 生成=RFAA 建模 + RFdiffusionAA（全原子扩散，围绕小分子生成蛋白）（`:178`）；③ 筛选器=全原子（非残基级）复合物置信度，取代「只表示蛋白」的 AF2 自洽（`:179`）。时间线位置（`:183`）：全原子化转折的方法学底座，此前 AF2/RF2 无法评估金属、辅因子、共价修饰，导致小分子/酶设计的筛选器失效。

## 2. 难点，以及遇到问题时作者做了什么（依据登记底稿，不含正文级细节）

> 本文未获正文：以下「他们做了什么」只到底稿转录摘要的粒度；作者自述的取舍无法核验，凡未记录处一律照实写未记录。

1. **筛选器失效：AF2/RF2 的表示里没有非蛋白组分。** 现象/证据：底稿 `:183` 记「此前 AF2/RF2 无法评估金属、辅因子、共价修饰，导致小分子/酶设计的筛选器失效」——即在这类任务上，用只表示蛋白的自洽性打分等于没筛。→ 他们做了什么：换成 RFAA 的全原子（非残基级）复合物置信度做筛选器（`:179`），生成端同步换成 RFdiffusionAA 围绕小分子做全原子扩散（`:178`）。→ 应对后仍留下的代价：置信度的数值阈值**原文未给阈值（本次未取正文）**（`:175` 明写本卡片仅摘要级），本卡给不出可复算的门槛。

2. **设计起点没有骨架：从围绕目标分子的随机氨基酸分布出发。** 现象/证据：摘要原句（底稿 `:182` 转录）—— "Starting from random distributions of amino acid residues surrounding target small molecules,"。→ 他们做了什么：不做先折叠再对接的两步，直接全原子扩散生成，末端用 X 射线晶体学 + 结合测定确认（`:181`）。→ 代价：摘要**未给出 N/M/命中率数字**（`:182` 原话），底稿 §五缺口 2（`:673`）写明「Europe PMC 无 PMC 全文（RFAA）……缺观察：正文 Methods 中每靶点的 96/几十名额与命中率」→ **命中率与递减链本文未解决（对我们是取证缺口）**。

3. **取证困难（我们的）：曾下载到的 OA 文件经身份体检挂错行，已隔离。** `fetch_log.tsv:114` 记 2024 批次曾按 PMC13669634 抓到 HTTP 200 / 218,930 B 的全文并标 OK；后续身份体检改判 `WRONG_PAPER_Fetched`（`fetch_log.tsv:160`：doi_conflict，文件内 DOI 为 10.1093/nar/gkag999，与本行期望 10.1126/science.adl2528 冲突），该文件已移入 `data/literature_cards/fulltext/_quarantine/`。→ 处置：本卡**没有**取该文件任何句子当引句、不把它当正文；引句底稿声明为 `sources/baker.md`，§0 证据级别不高于摘要级（处置范本见 C17 样板卡）。

## 3. 方法与工作流程（每步：输入 → 操作 → 判据/阈值 → 输出规模）

**降级卡硬约束**：本节只有底稿记到的操作序列与判据形态；所有阈值一律写 原文未给阈值（本次未取正文），不编造。

工具箱（仅底稿记录）：RFAA 建模；RFdiffusionAA 全原子扩散；实验侧 X 射线晶体学 + 结合测定（`:178`、`:181`）。MD: 否 / QM: 否（`:180`，注明是**摘要层面**的判断）。

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | 目标小分子/辅因子（digoxigenin、heme、bilin） | 以「围绕目标小分子的随机氨基酸分布」为起点（摘要原句见第 2.2 条引句） | 原文未给阈值（本次未取正文） | 未记录（底稿无设计库规模） |
| S2 | S1 的起点复合物 | RFdiffusionAA 全原子扩散，围绕小分子生成蛋白 | 原文未给阈值（本次未取正文） | 未记录 |
| S3 | S2 生成的复合物 | RFAA 全原子（非残基级）复合物置信度打分，取代只表示蛋白的 AF2 自洽 | 原文未给阈值（本次未取正文）；置信度字段的门槛值未记录 | 通过数未记录 |
| S4 | S3 幸存者 | 湿实验确认：X 射线晶体学 + 结合测定 | 判据形态（结构+结合双重确认）见于底稿；数值阈值未记录 | 摘要声明三个靶均有实验验证成功的结合蛋白；N/M 未给出（`:182`） |

**骨架（可记住的部分）**：漏斗要处理含辅因子/共价组分的设计对象，**第一道修复是筛选器的表示能力**（全原子置信度），其次才是生成器；但本卡给不出递减链，所有分母未记录。

## 4. 关键数字台账（全部能在登记底稿 `sources/baker.md` 里搜到）

| 数值/条目 | 含义 | 出处 |
|---|---|---|
| "we designed and experimentally validated, through crystallography and binding measurements" | 摘要原句片段：验证方式=晶体学+结合测定 | `sources/baker.md:182` |
| "the cardiac disease therapeutic digoxigenin, the enzymatic cofactor heme," | 摘要原句片段：三个验证靶 | `sources/baker.md:182` |
| digoxigenin / heme / bilin | 设计对象（小分子/辅因子结合蛋白） | `sources/baker.md:177` |
| MD: 否 / QM: 否（摘要层面） | 是否用 MD/QM 的可核状态 | `sources/baker.md:180`；CSV B13 行 是否用MD / 是否用QM 填 否 |
| 未给出 N/M/命中率数字 | 摘要不含分母；缺口 2 待正文/SI | `sources/baker.md:182`、`:673` |
| Science, 2024, 384: eadl2528；DOI 10.1126/science.adl2528 ✅；PMID 38452047（无 PMC） | 题录与核验状态 | `sources/baker.md:174–175` |
| PMC13669634 → DOI 10.1093/nar/gkag999（冲突） | 曾下载文件的**真实身份**（NAR 侧论文，非本文），已隔离 | `fetch_log.tsv:114`、`:160` |

## 5. 作者说了什么（本卡无正文，以下均为底稿转录的摘要级声明）

1. 他们声称：从随机分布出发，**设计并经晶体学与结合测定实验验证了**结合 digoxigenin、heme、bilin 的蛋白（两句逐字引句见第 2.2 条与第 4 节，均出自底稿 `:182` 转录的摘要）。
2. 他们声称（题目级）：这是面向一般化生物分子建模与设计的工具（RFAA），生成端为 RFdiffusionAA（底稿 `:172`、`:178`）。
3. 他们**没有**在底稿转录层给出：任何 N/M、命中率、Kd、置信度阈值。作者自述局限未获正文，无法核验。

## 6. 我们读出了什么（以下为推断，非作者原文）

1. **这篇的角色是「修筛选器」**：全原子复合物置信度取代蛋白自洽（底稿 `:179` 的记法），意味着在含辅因子任务上，此前所有 AF2 式闸口的读数都不可信。→ 对我们：凡设计对象含非蛋白组分（辅因子、共价加合物、金属位），用只表示蛋白的自洽性做终闸在原理上就不成立——这是我们该抄的**结构性结论**，不是它的数字。
2. **没有分母就没有跃升声明**：底稿缺口 2（`:673`）设想的「全原子路线把命中率从 X 提到 Y」在当前证据层**既不能证实也不能证伪**；任何引用 B13 谈命中率提升的说法都应视为待正文。把握度：对「底稿未见数字」为高；对「正文里没有数字」为低。
3. **它是谱系锚点**：RFAA→LigandMPNN→RFdiffusion2/3（`:183`）；[B35] 的 one-shot 全原子路线以它为前设。谱系判断可由本卡支撑，效果量判断不行。

## 7. 局限

- 摘要级：阈值、送测分母、命中率、最好 Kd 全部未记录（`:175`、`:182`、`:673`）。
- MD/QM 的「否」只到摘要层面（`:180` 原注），不能据此断言 Methods 里没用。
- 曾下载的全文文件挂错行已隔离，不构成任何补充证据；在其换回正确正文之前，B13 的一切正文级细节都是缺口。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**：
1. 「筛选器的表示必须覆盖设计对象的全部组分」——直接用于我们对自己漏斗的自检：候选含辅因子/共价中间体时，把只表示蛋白的打分降为参考读数、不作终闸。
2. 「先修表示、再谈阈值」的工程顺序：底稿记录的转折点是换置信度的定义域（残基级→原子级），不是调旧阈值的数值。

**不可迁移（为什么不能照搬）**：
1. RFAA 的复合物置信度**没有任何可核阈值**（本次未取正文），不得写成我们的闸口数值，也不得据它给「全原子提高命中率」赋概率。
2. 小分子结合蛋白的「结合对不对」≠ UAA 酶活的「化学事件发生没发生」；binder 判据不得搬作酶活判据（DP2R 标准 §2 的禁令同样适用于本文）。
3. 无 N/M 数字 → 本篇**不得**被引为任何成功率或校准锚。

## 9. 溯源与自检

引句底稿: sources/baker.md

- **本卡是降级卡**：B13 无开放获取正文（`fetch_log.tsv:58` 记 `NO_OA_FULLTEXT`）。引句规则按降级卡执行（≥2 条、逐字命中登记底稿）；本卡共 3 条逐字引句（第 2.2 条整句 + 第 4 节两条片段），全部命中 `sources/baker.md:182`。
- **⚠️ 挂错行文件的处置记录（交接用）**：批次抓取曾按 PMC13669634 下到一份全文并记 OK（`fetch_log.tsv:114`，HTTP 200 / 218,930 B / sha 前缀 33f6ae0286d6a859）；身份体检改判 WRONG_PAPER_Fetched（`fetch_log.tsv:160`：doi_conflict ['10.1093/nar/gkag999'] vs ['10.1126/science.adl2528']），文件现位于 `data/literature_cards/fulltext/_quarantine/B13_PMC13669634_text.txt`。本卡未取其中任何句子作引句、未视其为正文；曾下载到的 OA 文件经身份体检挂错行、已隔离，故本卡为降级卡。
- **登记底稿核对**：`sources_map.json` B13 项只登记 `sources/baker.md`（实存）。对照行号：`:172–183`（[B13] 卡段）、`:673`（§五 缺口 2）。CSV 行：`data/protein_design_literature.csv:14`（证据级别列=摘要级）。
- **门禁自检**：命令 `cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B13" --no-report`。本卡未改 CSV、`sources/*.md`、样板卡、`scripts/`，未做网络抓取。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 2 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（降级卡：摘要级，未获正文）
target=digoxigenin（地高辛）、heme、bilin 等小分子/辅因子结合蛋白
backbone_generation=RFAA 建模 + RFdiffusionAA（全原子扩散，围绕小分子生成蛋白）
computational_filters=全原子（非残基级）复合物置信度，取代只表示蛋白的 AF2 自洽
thresholds=未记录（原文未给阈值；本次未取正文）
md_used=否（摘要层面记录；正文未见，不排除 SI 细节）
qm_used=否（摘要层面记录；同上）
experimental_methods=X 射线晶体学 + 结合测定
pipeline_counts=未记录（摘要未给 N/M；见 sources/baker.md:673 缺口 2）
hit_rate=未记录（未获正文；本卡不得引用任何命中率）
best_metric=未记录（摘要只声明三个靶均有实验验证成功的结合蛋白，无 Kd 数字）
cost_or_stat_note=未记录
role_in_timeline=全原子化转折的方法学底座：此前 AF2/RF2 无法评估金属、辅因子、共价修饰导致筛选器失效；RFAA→LigandMPNN→RFdiffusion2/3 把漏斗延伸到原子层
source_pointer=sources/baker.md:172-183（[B13] 卡段）、:673（缺口 2）；DOI 10.1126/science.adl2528 ✅Crossref、PMID 38452047；⚠️ fulltext/_quarantine/B13_PMC13669634_text.txt 为挂错行他文（文件内 DOI 10.1093/nar/gkag999），未用作本卡证据
CSV回填-->
