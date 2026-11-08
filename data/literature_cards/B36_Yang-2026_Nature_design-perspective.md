# [B36] Baker 组 2026 立场综述：哪些设计问题已被视为接近解决（降级卡：摘要级，未获正文）

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 第 37 行，编号 **B36**（组：Baker 组；`文献类型` 列=综述；`证据级别` 列原文即写 摘要级） |
| 题目 | The past, present and future of de novo protein design |
| 作者 | Yang W, Wang S, Lee G, Zhang J, Courbet A, Juergens D, Wang X, Schlichthaerle T, Abedi M, Ragotte R, … Baker D（24 人）（`sources/baker.md:472`） |
| 出处 | Nature, 2026, 652:1139-1152 · DOI 10.1038/s41586-026-10328-7（✅Crossref）· PMID 42056544（无 PMC） |
| 正文取回状态 | ⛔ **未获正文**。`fetch_log.tsv:4` 与 `:62`：EPMC search（EXT_ID:42056544，resultType=core）返回 `NO_OA_FULLTEXT`，注记 记录存在但无 PMCID（isOpenAccess=N）；`inventory.json` B36 项 local=[]、has_fulltext=false |
| 登记底稿（本卡唯一引句来源） | `sources/baker.md` 第 471–481 行（[B36] 卡段） |
| **⚠️ 挂错行的所谓全文** | 批次抓取曾按 PMC13660641 下到 HTTP 200 / 98,018 B 的全文并记 OK（`fetch_log.tsv:117`）；身份体检改判 `WRONG_PAPER_Fetched`（`fetch_log.tsv:162`：doi_conflict ['10.1016/j.mrl.2026.200309'] vs 本行期望 ['10.1038/s41586-026-10328-7']），文件已移入 `data/literature_cards/fulltext/_quarantine/B36_PMC13660641_text.txt`。**本卡不取该文件任何句子作引句、不视其为正文**（处置范本见 C17 样板卡） |
| 证据级别 | **摘要级 / 未获正文**（与 CSV 行一致；正文未抓取，底稿 `:477` 原记 本报告仅使用摘要） |
| 未取到的部分 | 综述正文的全部论证与引文表格；「接近解决」判断所依据的具体命中率对比；未解清单的定量口径。凡涉及处均写 未记录（本次未取正文） |

## 1. 这篇解决什么（一句话）

**一句话**：这不是一场设计战役而是一份**领域状态判词**——Baker 组官方宣布 fold / 组装体 / 蛋白结合体三类任务的「怎么设计」问题接近解决、剩余问题变成「设计什么」，并把真正的未解方法学定位为**高活化能反应的催化设计**与**开关/纳米机器**。

底稿记录：覆盖 fold / 组装体 / 蛋白结合体 / 酶 / 多态开关全谱（`:476`）；时间线位置=Baker 组对「漏斗已经够用」的官方判断（`:481`）。它给本项目的价值是**边界标记**：我们的酶活任务落在它点名的未解区（高活化能催化），不能拿「接近解决」当背景先验。

## 2. 难点，以及遇到问题时作者做了什么（依据登记底稿，不含正文级细节）

> 综述无单一方法流程；本节按「这份判词自身的坑 + 我们取证的坑」写。作者自述部分未获正文，无法核验。

1. **「close to being solved」是自述立场，摘要层没有任何定量审计。** 现象/证据：底稿转录摘要两句判断（逐字引句见第 4 节：`the long-standing challenges of designing new protein structures, assemblies and protein binders are` 与 `close to being solved`）。→ 作者做了什么（就摘要可见）：把剩余问题显式列出——催化高能垒反应与开关/纳米机器（第 2.2 条），即**用自己的未解清单给乐观判断配了边界**。→ 仍留下的代价：三类任务「按什么指标、哪些数字」算接近解决，摘要没给、正文未抓取 → **本文未解决（定量依据进不了可核层，对我们是取证缺口）**。

2. **判词依赖的开源工具链主张同样只到摘要层。** 现象/证据：摘要句 `The key current questions in these areas are not how to design, but what to design, and open-source design methodology such as` … `enable biochemists and molecular biologists to broadly explore possible applications`（底稿 `:480` 转录）。→ 作者做了什么：把「问题已转移」归因于 RFdiffusion/ProteinMPNN + 结构预测工具的公开可得。→ 代价：本卡无法核对他们引用的证据清单（哪些 campaign、什么通过率）；转引的乐观不能进我们的先验。

3. **取证困难（我们的）：曾下载到的 OA 文件经身份体检挂错行，已隔离，故本卡为降级卡。** PMC13660641 那份文件内 DOI 为 10.1016/j.mrl.2026.200309，与本行 10.1038/s41586-026-10328-7 冲突（`fetch_log.tsv:162`）——照抄会把别家论文写成 Baker 综述。→ 处置：引句底稿声明为 `sources/baker.md`；§0 证据级别停在摘要级；隔离文件留给协调表负责人回收，本代理未改动任何调度文件。

## 3. 方法与工作流程（这里记的是作者的论证工作流；每步：输入 → 操作 → 判据/阈值 → 输出规模）

**降级卡硬约束**：正文未抓取（`:477`），本节只写摘要转录的论证形态；**全流程原文未给阈值（本次未取正文）**，不编造。

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | de novo 蛋白设计全领域（fold、组装体、蛋白结合体、酶、开关/纳米机器） | 把任务分类，逐类评估「怎么设计」是否仍是问题 | 原文未给阈值（本次未取正文）；判据形态=领域内自述 | 前 3 类判为接近解决、后 2 类列为开放问题（摘要层） |
| S2 | 「接近解决」判断 | 给出剩余关键问题的表述：not how to design, but what to design（见第 4 节引句） | 原文未给阈值（本次未取正文） | 应用探索被交给开源工具链主张 |
| S3 | 方法学开发方向 | 点名两个未解区：高活化能反应催化 + 开关/纳米机器（第 4 节引句） | 原文未给阈值（本次未取正文） | 未解清单 2 项 |

**工具箱说明**：综述不产生候选；底稿对本文的 候选生成方法与计算筛选器 记录即「不适用（综述；正文未抓取，本报告仅使用摘要）」（`:477`）。MD / QM 角色：摘要未提及，底稿明写不作为证据（`:478`）。

## 4. 关键数字台账（全部能在登记底稿 `sources/baker.md` 里搜到；本卡共 5 条逐字引句）

| 数值/条目 | 含义 | 出处 |
|---|---|---|
| "the long-standing challenges of designing new protein structures, assemblies and protein binders are" | 摘要判断前半句（注意原文此处之后接粗体强调，片段止于强调前） | `sources/baker.md:480` |
| "close to being solved" | 摘要判断的落点短语 | `sources/baker.md:480` |
| "The key current questions in these areas are not how to design, but what to design," | 问题转移声明（片段止于强调前） | `sources/baker.md:480` |
| "enable biochemists and molecular biologists to broadly explore possible applications" | 开源工具链主张的后半句 | `sources/baker.md:480` |
| "Current challenges for methods development include" | 未解清单引导句 | `sources/baker.md:480` |
| "and, more generally, design of switches and nanomachines" | 未解清单第二项 | `sources/baker.md:480` |
| Nature, 2026, 652:1139-1152；DOI 10.1038/s41586-026-10328-7 ✅；PMID 42056544（无 PMC） | 题录与核验状态 | `sources/baker.md:473–474` |
| 24 人 | 作者规模 | `sources/baker.md:472`；CSV 行同 |
| 不适用（综述） | 设计对象/生成方法/筛选器/实验验证四栏的底稿原记 | `sources/baker.md:476–479` |

## 5. 作者说了什么（只有摘要转录层）

1. 设计新蛋白结构、组装体与蛋白结合体的长期挑战接近解决；关键问题已从「怎么设计」变成「设计什么」（第 4 节引句 1–4）。
2. 方法开发的当前挑战包括高活化能反应催化，以及更一般地，开关与纳米机器的设计（引句 5–6）。
3. 他们**没有**给出：判断所依据的命中率对照表、各任务的量化「解决线」、RFdiffusion/ProteinMPNN 之外的新实验。底稿 `:477` 与缺口清单均确认正文未抓取。

## 6. 我们读出了什么（以下为推断，非作者原文）

1. **这是时间线上的边界桩，不是效果证据**：它把 fold/binder 的筛选问题标记为「组内已收敛」，把催化/开关标记为开放——与我们自己在本库线的判断（静态自洽判据对共价化学事件不够）方向一致，可作为「问题定位」的引文锚，但其乐观程度不可量化引用。
2. **「success rates and activities 仍有提升空间」这句自留余地值得留意**：底稿 `:480` 转录的原文开头即承认改进空间存在——即「接近解决」不等于「已校准」，没有任何通过率被宣布封顶。
3. **综述级条目的卡片应更薄**：它提供的可核内容只有两句判断+一份未解清单；把 24 人综述写成方法卡会是补脑。本卡按底稿粒度封顶。把握度：对「底稿只到摘要」高；对「正文论证是否更强」未知。

## 7. 局限

- 二级证据（自述立场）+ 摘要级：无定量依据可核。
- 作者名单含 Ragotte 等组内方法学贡献者，判断存在利益相关（自述解决状态，无第三方审计）→ 底稿与 CSV 均无独立核对记录。
- 挂错行隔离事件使任何「本卡有全文」的猜测都不成立；正文级论证在换回正确文本前全部记为缺口。

## 8. 迁移判断：哪些能搬、哪些不能搬

**可迁移（怎么用）**：
1. 用它的**未解清单**给本项目定位：酶设计活化酶设计=「高活化能反应催化」类，按 Baker 组自评连他们自己都没收敛——这支持我们把失败归因于任务难度而非单纯执行问题（仅作定性定位，不折算概率）。
2. 「问题从 how 转向 what」在我们线的对应物：当召回与打分链稳定后，下一瓶颈是任务定义与判据选择；这可以指导我们把轮次预算往判据设计倾斜。

**不可迁移（为什么不能照搬）**：
1. 「close to being solved」**禁止**用作我们 binder/酶候选成功率的背景先验——分领域、无数字、自述立场（本库判据 §2 同源禁令）。
2. 综述不产生阈值；本卡无任何数值可搬，也不得从它的乐观程度反推「催化设计上限低」。

## 9. 溯源与自检

引句底稿: sources/baker.md

- **本卡是降级卡**：B36 无开放获取正文（`fetch_log.tsv:4`、`:62` 记 `NO_OA_FULLTEXT`，PMID 42056544 无 PMCID、isOpenAccess=N）。**曾下载到的 OA 文件（PMC13660641）经身份体检挂错行（文件内 DOI 10.1016/j.mrl.2026.200309 与本行期望 DOI 冲突），已隔离至 `fulltext/_quarantine/`，故本卡为降级卡**：其句子一律未用作引句。降级卡引句规则（≥2 条、逐字命中登记底稿）；本卡共 6 条逐字引句，全部命中 `sources/baker.md:480`。
- **登记底稿核对**：`sources_map.json` B36 项只登记 `sources/baker.md`（实存）。对照行号：`:471–481`（[B36] 卡段）。CSV 行：`data/protein_design_literature.csv:37`（文献类型=综述、证据级别=摘要级）。
- **门禁自检**：命令 `cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "B36" --no-report`。本卡未改 CSV、`sources/*.md`、样板卡、`scripts/`、`batches.tsv`、隔离目录，未做网络抓取。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 1 条逐字引句来自许可受限的第三方来源（B01；PUBLISHER_TERMS），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=综述（降级卡：摘要级，正文未抓取）
target=不适用（覆盖 fold / 组装体 / 蛋白结合体 / 酶 / 多态开关全谱的领域状态判词）
backbone_generation=不适用（综述；正文未抓取，底稿仅使用摘要）
computational_filters=不适用（综述）
thresholds=未记录（原文未给阈值；本次未取正文）
md_used=未记录（摘要未提及，底稿明写不作为证据）
qm_used=未记录（同上）
experimental_methods=不适用（综述）
pipeline_counts=不适用；综述无候选递减
hit_rate=未记录（判断所依据的命中率对照表未从正文核实）
best_metric=未记录
cost_or_stat_note=「close to being solved」为自述立场、无第三方审计；本组仅能核到摘要转录层
role_in_timeline=Baker 组对「漏斗已经够用」的官方判断：fold/组装体/蛋白-蛋白结合体被视为接近解决；未解=高活化能反应催化 + 开关/纳米机器
source_pointer=sources/baker.md:471-481（[B36] 卡段）；DOI 10.1038/s41586-026-10328-7 ✅Crossref、PMID 42056544；⚠️ fulltext/_quarantine/B36_PMC13660641_text.txt 为挂错行他文（文件内 DOI 10.1016/j.mrl.2026.200309），未用作本卡证据
CSV回填-->
