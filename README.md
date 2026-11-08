# 蛋白设计筛选参考库（152 篇文献 · 逐字核验版）

一句话：把"从头设计蛋白 / 结合体筛选"这条链路上**别人实际怎么做的、用了哪些判据、阈值原文是多少、
花多少钱和时间、在哪里翻车**，做成一份每个数字都能查到原文句子的可复现参考库。

建库时间 2026-10-16 至 2026-10-21；工作流模板 v2 与多轮迭代协议 2026-11-07 改版（同日核实 RFD4-Proteina）；
**2026-11-08 起本仓库公开**，第三方原文一律不入库（见下面"公开仓库口径"一节）。
当前状态：152 行 × 27 列文献表，每行背后一张十节精读卡，全量门禁 `152/152 PASS`（退出码 0）。

## 三分钟上手

1. [report.md](report.md) — 结论报告（含"我们没能核实到什么"的缺口清单 §八）。
2. [工作流模板 v2](deliverables/protein_design_workflow_template.md) — **开工就抄这份**：主线十阶段的默认阈值、
   闸口与停止条件、预算四档、阈值重校准协议，外加三个分支页（binder / 酶 / 肽与大环）。
   开工登记压到附录 §I（10 分钟填完），前沿默认链已换到 **RFD4-Proteina 共设计**（§F，含退回 RFD3 的条件）。
3. [多轮迭代协议](deliverables/protein_design_workflow_iteration.md) — **第二轮起看这份**：一轮的定义与必留三文件、
   候选/判据/路线三轴分离（一轮只动一个轴）、逐分支第二轮怎么打、T0（≤4 构建体）档怎么迭代、多轮战役怎么报数；
   §1 是**真实轮次台账**（[B17] 九轮含受控对照、[B18] 归因+反证臂、[B10] 几何知识迁移等，每条带分母），
   §3.4 是用 RFD4 时的"第 0 轮 pilot"（官方建议，不是战役记录）。
4. [证据工作流](deliverables/protein_design_workflow.md) — 模板里每个数字的原文出处与失灵域（"别人怎么做的"记录）。
5. [data/protein_design_literature.csv](data/protein_design_literature.csv) — 总表。Excel 直接打开（UTF-8 BOM）。
   看任意一行，最后两列 `精读卡文件` 给出单卡路径、`精读卡全文(方法·工作流·遇坑)` 直接把整张卡塞在单元格里。

想查某个数字的出处：先在总表 `阈值数字` / `实验命中率` / `成本/统计` 列里搜，再顺着 `原文出处指针` 列
进卡（卡 §4 数字台账、§9 溯源），最后进卡声明的 `引句底稿`（本地全文或调研记录）。

## 迁移包与"喂给别的 AI"

`python scripts/build_bundles.py` 在 `deliverables/bundles/` 生成两个包（也发布在本仓库的 GitHub Release 上）：

| 包 | 内容 | 用途 |
|---|---|---|
| `..._full_<date>.zip` | git 可见的全部文件（作者原创部分：卡片 + 总表 + 台账 + 模板 + 迭代协议 + 脚本 + 调研底稿 + 许可审计与清单）+ `LICENSE`/`NOTICE`/`CITATION.cff` | 换机器重建工作树；**不含任何第三方原文**（复核路径见下面的清单） |
| `..._ai_<date>.zip` | AI 投喂子集：卡片 + 总表 + 台账 + 模板 + 迭代协议 + 脚本 + 调研底稿，**不含** `fulltext/` 与 `data/interim/`，另附 `ai_ingest/` 分层 digest | 喂给别的 AI 当资料库 |

**两个包都不含第三方论文全文**：这是公开仓库口径（见下面"公开仓库口径"）。需要某一份原文时，
按 `deliverables/fulltext_manifest.csv` 里的路径与"重取方式"取回，并用表里的 sha256 校验。

`ai_ingest/` 的分层：`tier0_index.md`（是什么+三条禁令）→ `tier1_core.md`（README+两份工作流+模板+前沿核验+发布说明，≈5.5 万 token）
→ `tier2_cards.md`（153 个卡文件 / 152 行，≈130 万 token，**按编号取单张**，别整份喂）→ `tier3_ledgers/`（CSV，结构化问题走这里）。
喂法与 token 估算方法写在 `ai_ingest/HOW_TO_FEED.md`。包内不含论文原文，所以卡里的引句在该包内不可复核，
只能查到声明的底稿路径与哈希——需要原文复核时按 `fulltext_manifest.csv` 重取，或用本仓库的本地工作树。

最新一次发布：Release [`v1-template-and-bundles`](https://github.com/Elephenman/protein-design-screening-reference/releases/tag/v1-template-and-bundles)。
两个资产在上传后都已**从服务端重新下载并逐字节比对 sha256**，与本地一致；哈希值见 Release 资产页
（GitHub API 的 `digest` 字段）与本地生成的 `deliverables/bundles/SHA256SUMS.txt`
（该目录被 gitignore，**不进仓库也不进包**——把发布物的哈希写进被发布物本身会自指）。
**本仓库自 2026-11-08 起为公开仓库**。

## 公开仓库口径（2026-11-08 起）

公开 = 公开再分发，所以按"公开仓库 = 作者原创内容"这条线处理，规则写死在 `.gitignore` 与门禁里：

1. **第三方原文一律不入库**。全库第三方原文（PMC/出版商全文抽取、逐句转储、题录缓存、预印本正文）
   都不被 git 跟踪；它们仍留在本机磁盘，只是不进仓库、不进任何发布包。
   逐份登记在 `deliverables/fulltext_manifest.csv`（224 份：路径、字节数、sha256、许可类别、
   是否随仓库分发、重取方式），需要哪一份按表取回并校验哈希。
2. **逐篇许可判定**：87 行做过许可审计（61 行允许含商用再分发、26 行不允许），报告见
   `deliverables/protein_design_license_audit.md`，机器版同目录 `.csv`。审计只判"能不能再分发"，不判内容对错。
3. **卡与底稿里的逐字引句按"引用预算"截短**：许可受限来源（CC BY-NC / ND / NC-ND / 出版商条款 /
   仅文本挖掘 / 仅研究复用 / 保留所有权利）以及**许可未审计**的行，引句截到引用级——
   单条 ≤100 字符、同一来源行在同卡内合计 ≤600 字符；截短后仍逐字命中同一份底稿，门禁不放宽。
   可再分发的行（CC BY / CC0）保持原样，并在卡里履行署名。
   实测：卡片 7,125 条引句里受限来源的 2,180 条、257,368 字符压到 93,663 字符（−63.6%，截短 1,804 条，涉及 43 张卡）；
   调研底稿与迭代台账 618 条引句里受限来源的 160 条、21,328 字符压到 13,466 字符（−36.9%，截短 90 条，
   另有 22 条为保住卡片核验链而保留原句）；未归属引句 46 条、4,082 → 3,679 字符。
   截不短的两类例外都已登记原因：**截断点会落在 markdown 强调段/长词中间**（脚本宁可不截也不产生半截引句），
   以及**底稿引句是我们自己的转写**（大小写或连字符与原文不一致，逐字自检无法通过）——这类只保证"仍是原句前缀"。
   逐条改动账：`deliverables/quote_budget_ledger.csv`（卡）、`deliverables/quote_budget_summary.csv`、
   `deliverables/quote_budget_notes_ledger.csv`（底稿）。
4. **门禁三态**：`verify_literature_cards.py` 在有本地底稿时判 `PASS_LOCAL`，
   在公开克隆（底稿不在场）时判 `WITHHELD`（不是失败，是"按公开口径不随包分发所以本机无法复核"），
   真正的错误才判 `FAIL`。本地工作树当前是 `PASS_LOCAL 152/152 · WITHHELD 0 · FAIL 0`；
   公开克隆实测 `PASS_LOCAL 72/152 · WITHHELD 80 · FAIL 0`（缺的是第三方底稿，不是缺漏）。
   同口径的两道引用预算门禁（`apply_quote_budget.py --check`、`apply_note_quote_budget.py --check`）
   在公开克隆里把"底稿按公开口径未随仓库分发"记 `WITHHELD` 而不是 `FAIL`；
   `build_workflow_evidence.py --check` 的逐字节比对在行尾 CRLF/LF 归一后进行
   （Windows 检出会把 LF 转成 CRLF，那是平台产物不是内容差异）。
   这几处口径都在**公开克隆**里实测过：13 条门禁全部退出码 0，
   且故意改坏一条引句后 `verify_literature_cards.py` 立刻报 `FAIL 1`（门禁仍能红）。
5. **第三方论文全文再分发一律不做**（商业版同样不做）：理由是义务履行成本与客户侧一致性，
   不是许可允许与否的问题。
6. **公开树再体检**：`scripts/audit_public_tree.py` 判两件事——
   ① 清单里标"不随仓库分发"的 220 份第三方原文，**0 份**出现在 git 跟踪集里；
   ② 许可受限来源的逐字引句，单条不得超过 400 字符（实测最长 344）。
   同时打印可写进本节的口径统计：第三方引句 13,565 处 / 1,251,012 字符，
   其中许可受限 4,430 处 / 197,459 字符，可再分发来源 9,135 处未设限（署名前提下可再分发）。
   这是**本机维护者工作树**的口径；公开克隆里第三方底稿一份都不在场，
   脚本会明说"引句数不可复核"（不是"库里没有引句"）。
   `--selftest` 注入三种破坏各红一条。

## 目录

| 路径 | 内容 |
|---|---|
| `data/protein_design_literature.csv` | 文献总表：152 行 × 27 列（按 `人物组` 列首组计：通用方法学 67 / Baker 组 44 / 曹龙兴组 21 / 周如鸿组 16 / 口径对照与独立复核 4；多组重叠行有 13 行，故与"该组出现次数"口径不同） |
| `data/literature_cards/*.md` | 每行一张精读卡（共 153 个卡文件，`B28` 一行有两张同篇卡，见"已知缺陷"），十节固定：0 元信息 · 1 解决什么 · 2 难点与应对 · 3 方法工作流 · 4 数字台账 · 5 作者说了什么 · 6 我们怎么推断 · 7 局限 · 8 能不能迁移 · 9 溯源（含 14 键 CSV 回填块） |
| `data/literature_cards/AGENT_RULES.md` | 写卡规程（引句必须逐字、文件名 slug、非论文行写"取证卡"的口径） |
| `data/literature_cards/fulltext/` | **不在仓库内**（`.gitignore` 排除，仅存于本机）：本地全文抽取，41 行用本目录（另有 39 行用 `data/interim/baker_lit/ft/`、13 行用 `data/interim/claim_lit/`，6 行跨两处，合计覆盖 87 行）；`_quarantine/` 是身份体检判定"挂错行"的 9 份 + 日志。逐份登记与重取方式见 `deliverables/fulltext_manifest.csv` |
| `data/literature_cards/run.md` | 过程账：每一步的脚本、参数、实测输出、踩过的坑与更正 |
| `data/interim/` | 抓取日志、回写前的 CSV 备份、2000 处字段改动账、本轮表级改动账（157 条）与许可抓取缓存（第三方原文部分同样不入库） |
| `deliverables/fulltext_manifest.csv` | 第三方原文清单（224 份）：路径、字节数、sha256、许可类别、是否随仓库分发、重取方式。**公开仓库里复核原文的唯一入口** |
| `deliverables/quote_budget_ledger.csv` / `quote_budget_summary.csv` / `quote_budget_notes_ledger.csv` | 引用预算改动账：卡与底稿里每条引句截前/截后字符数、来源编号、许可类别、是否截短与保留原因 |
| `LICENSE` / `NOTICE` / `CITATION.cff` | 授权（只覆盖作者原创部分）／第三方声明与许可分布／引用信息。**两个迁移包都必须带上它们**，`build_bundles.py` 会检查，缺一个就红 |
| `sources/*.md` | 六份调研底稿（Baker 组、曹龙兴组、周如鸿组、成本与判据经济学、90% 声明可查证性审计、功能判定工作流） |
| `scripts/` | 建库、核验、抓取、回写、台账生成的全部脚本 |
| `deliverables/` | 工作流模板 v2（主模板+三分支）+ **多轮迭代协议** + 证据工作流文档 + **审核视图 `protein_design_workflow_visual.html`**（把 87 条默认阈值摊开、可逐行标记并导出审核意见；由 `scripts/build_workflow_visual.py` 从模板与台账编译，页面无手打数字，`--check` 的期望值从门禁现算）+ 机器生成的证据台账 + 前沿方法核验清单（S0–S22） |
| `data/interim/rfd4_2026-11-07/` | RFD4-Proteina 取证本：两份官方 README、事实台账 `rfd4_paper_findings.md`、`PROVENANCE.md`（sha256 + 重取 URL）。**预印本正文抽取 `RFD4_paper_text.txt`（283 KB）与 54.8 MB 原 PDF 均不入库**（第三方预印本正文），按 PROVENANCE 里的 URL 重取并校验哈希即可复现 |
| `deliverables/bundles/` | 迁移包与 AI 投喂包（由 `scripts/build_bundles.py` 生成，不进 git，发布走 GitHub Release） |

## 门禁（这就是"可复现"的意思）

```bash
cd <项目根目录>
set PYTHONIOENCODING=utf-8
python scripts/verify_literature_cards.py     # 152/152 PASS 才算完整；退出码非 0 = 没做完
python scripts/verify_workflow_doc.py         # 证据工作流文档的引用与链接体检
python scripts/verify_workflow_template.py    # 模板：引用可查 + 每条默认阈值带证据级别 + 链接可达
python scripts/verify_workflow_template.py --selftest   # 四种破坏必须各红一条
python scripts/build_bundles.py --check       # 包内清单与磁盘哈希一致
python scripts/build_workflow_evidence.py --check   # 台账三个产物必须与从 CSV+卡重算的结果一致（行尾 CRLF/LF 归一后逐字节比）
python scripts/build_workflow_visual.py --check     # 页面无手打数字：阈值/引用/S 条目数从门禁现算
python scripts/fix_table_fields.py --check        # 表级改动账：账里新值==当前表，受管列每处改动都有账
python scripts/audit_source_licenses.py --check    # 第三方全文缓存的许可分类：行数与逐行类别与重算一致
python scripts/build_fulltext_manifest.py --check  # 第三方原文清单：224 份的路径/字节/sha256/许可类别与磁盘一致
python scripts/apply_quote_budget.py --check       # 卡片引用预算：改动账与卡现状一致
python scripts/apply_note_quote_budget.py --check  # 底稿引用预算：改动账与底稿现状一致，卡核验链未被破坏
python scripts/audit_public_tree.py            # 公开树体检：第三方原文 0 处被跟踪 + 受限引句单条 ≤400 字符
python scripts/audit_public_tree.py --selftest  # 三种破坏必须各红一条
```

门禁判的是五件事：每行有且仅有一张卡；十节标题齐全且顺序固定；工作流表 ≥3 步、难点 ≥2 条；
**卡里每一条纯英文直引号片段必须在该卡声明的那一份底稿里逐字命中**；证据级别不许造假
（没有本地全文却写"全文级"直接 FAIL）。它不判文献内容对不对——那是卡 §7 与 `report.md` §八 的活。

在**公开克隆**里（没有本机第三方底稿），第一条门禁改判三态：
`PASS_LOCAL`（本机可逐字核验）/ `WITHHELD`（底稿按公开口径不随包分发，本机无法复核）/ `FAIL`（真错误）。

## 两个"证据级别"口径，不许混用

这个库有两个都能数出数字但含义不同的东西，2026-11-07 起在台账里分列两栏（`底稿形态` / `卡证据级别`）：

| 口径 | 数字 | 含义 |
| --- | --- | --- |
| **底稿形态** | FULLTEXT 87 / DEGRADED 65 | `inventory.json` 的 `has_fulltext`：本地存有一份登记在册的全文抽取文件 |
| **卡证据级别** | FULLTEXT 79 / DEGRADED 73 | 卡片 §0 自己声明的级别，且每条直引号已在它声明的那一份底稿里逐字命中 |

两个口径相差 **8 行**：`Z01 Z02 Z03 Z05 Z09 C13 C18 M-K29`。这 8 行的 PMC 全文就在本地，
但卡里写的是"未获正文／二级来源"，逐字命中率只有 3/11 – 32/43（缺的那些句在该 XML 里并不逐字一致）。
**本轮不把它们升级为全文级**——升级的前提是重写卡片让引句逐字命中，不是改一个标签。
这 8 行的编号、单条命中率见 `deliverables/protein_design_workflow_summary.txt`。


## 这个库遵守的三条规矩

**三态而不是含糊**：每个结论标"能证明 / 不能证明 / 尚缺什么"。例如"计算闸口把下单量从 10⁵ 压到 10²–10³
并提一个数量级成功率"能证明（[B09][B08]）；"每候选 μs 级 MD/FEP 预筛更省"不能证明（[K27]）；
"MD 精筛把命中率从 X% 提到 Y%"至今缺公开同口径基准（缺，不等于不存在）。

**分母必须跟着数字走**：`in silico` 成功率、表征子集比例、末端实测池命中率是三回事，混用就是自欺。
库里有真实案例：[B11] 的"约 90% 对约 30%"两个分母都是自选子集；[K39] 的 1%–10% 与 1%–2% 分母不同。

**价目与通量按证据级别写**：厂商挂价、核心设施收费页、公司新闻稿、本报告推算，一律写成"取证卡"，
标好分母（元/碱基、元/池、元/小时、元/样、元/对不可互算）、快照时间与"是否二手转引"。
`[K01]` 那条"便宜 100 倍"是本文转引他人文献，不是该实验室实测——这种话只有留账才不会被人当采购依据。

## 已知缺陷（公开前请读这段）

- 表级字段缺陷**已于 2026-11-07 更正并留账**（`scripts/fix_table_fields.py` + `scripts/table_field_fixes.json`，
  改动账 `data/interim/table_field_fixes_2026-11-07.json`，备份
  `data/interim/protein_design_literature_backup_2026-11-07_fieldfix.csv`）：
  `K49` 的 `期刊或预印本` 原写 Amino Acids，Europe PMC 实查是 **Biophysical Reviews 18 卷**；
  `K48` 的 `年份` 原写 2025，全文题录 2024；`B12` 的 `年份` 原写 2023，Nature 626:435-442 实为 2024
  （Crossref 在线年 2023、期号年 2024，故以期号年为准）；`K59` 的 `核验状态` 原写"✅Crossref核验"而 `DOI=未记录`
  （核验对象是 C&EN 新闻条目 DOI，已改写为写明核验对象）。同时把 `证据级别` 整列重刷成机器标签，
  并在 `verify_literature_cards.py` 里加了**表↔卡一致性**检查（2026-11-07 之前该列有 58/152 行与卡相反，
  其中 8 行把"未获正文"写成了"全文级"）。
- **改动账被覆盖过一次，已复原并加了门**：早期版本的 `fix_table_fields.py` 把改动账写成按日期命名的固定文件，
  同一天第二次运行（只改 C10 一处）把第一次运行的 **152 条**记录整体覆盖成 1 条。现已：
  ① 由 `git show f07540d:data/protein_design_literature.csv` 重放 `table_field_fixes.json` +
  `litcards_evidence_level.py`，把 157 条（152 条整列刷新 + 5 条手工更正）逐条复原回
  `data/interim/table_field_fixes_2026-11-07.json`，并与幸存的 C10 条目逐字比对一致；
  ② 脚本改为同日多次运行**合并账目、备份不覆盖**；
  ③ 新增 `python scripts/fix_table_fields.py --check`：账里每条新值必须等于当前表该格，
  受管列每处改动都必须有账，证据级别必须与卡 §0 一致（两种破坏已实测各红一条，退出码 1）。
- **两个证据口径的 8 行差集**（`Z01 Z02 Z03 Z05 Z09 C13 C18 M-K29`）见上一节，本轮不升级，理由已写明。
- **`B28` 一行有两张卡**（`..._2023_NatComputSci_ligandmpnn.md` 早期登记版与 `..._2025_NatMethods_...md` 后续版，同一篇
  Nature Methods 2025）。门禁规则是"每行 ≥1 张"，所以 152/152 仍 PASS，但卡文件数是 **153** 而不是 152。
  两张都保留（删除会切断已完成的引句核验链），**引用一律以台账 `精读卡文件` 列指向的那张为准**。过程账见 `run.md` §10.5。
- 73 行的卡按摘要级/二级来源/未获正文写（卡证据级别 DEGRADED），阈值与步骤细节不许补，卡 §2 已明写"未获正文无法核验"。
- **第三方原文已移出仓库**（2026-11-08）：`data/literature_cards/fulltext/`、`data/interim/` 里的出版商/PMC 全文抽取、
  逐句转储、题录缓存与 RFD4 预印本正文一律不被 git 跟踪，也不出现在任何发布包里；
  逐份许可与重取方式见 `deliverables/fulltext_manifest.csv`（224 份）与
  `deliverables/protein_design_license_audit.md`（87 行的逐篇许可判定）。
  卡里保留了 sha256 与身份块指针，核验链不断——缺底稿时门禁判 `WITHHELD` 而不是 `FAIL`。
- **引句按引用预算截短**（2026-11-08）：许可受限来源与许可未审计行的逐字引句被压到引用级
  （单条 ≤100 字符、同一来源行合计 ≤600 字符），截短后仍逐字命中同一份底稿，门禁不放宽；
  可再分发行（CC BY / CC0）保持原样并履行署名。改动账见
  `deliverables/quote_budget_ledger.csv` 与 `deliverables/quote_budget_notes_ledger.csv`。
  底稿里有 22 条引句为保住卡片核验链而保留原句，账上逐条写明原因。

## 与"天然 UAA 合成酶发现"那条主线的关系

本仓库是**跨实验室判据有效性与成本的参考库**，不是那条主线的判定输入。
从头设计结合体的 `pAE_interaction` / `ipTM` 阈值、适配体 FEP 命中率、展示库通量，都**不许**当成酶活判据或成功概率——
每张卡的 §8 逐条写死了这条边界。那条主线由 `A:\Data\DP2R\方案` 的判定标准管辖。
