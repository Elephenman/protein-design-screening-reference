# 蛋白设计筛选参考库（152 篇文献 · 逐字核验版）

一句话：把"从头设计蛋白 / 结合体筛选"这条链路上**别人实际怎么做的、用了哪些判据、阈值原文是多少、
花多少钱和时间、在哪里翻车**，做成一份每个数字都能查到原文句子的可复现参考库。

建库时间 2026-10-16 至 2026-10-21。当前状态：152 行 × 27 列文献表，每行背后一张十节精读卡，
全量门禁 `152/152 PASS`（退出码 0）。

## 三分钟上手

1. [report.md](report.md) — 结论报告（含"我们没能核实到什么"的缺口清单 §八）。
2. [工作流模板](deliverables/protein_design_workflow_template.md) — **开工就抄这份**：十个阶段的默认阈值、闸口、
   停止条件、预算四档、阈值重校准协议，外加三个分支页（binder / 酶 / 肽与大环）。
3. [证据工作流](deliverables/protein_design_workflow.md) — 模板里每个数字的原文出处与失灵域（"别人怎么做的"记录）。
4. [data/protein_design_literature.csv](data/protein_design_literature.csv) — 总表。Excel 直接打开（UTF-8 BOM）。
   看任意一行，最后两列 `精读卡文件` 给出单卡路径、`精读卡全文(方法·工作流·遇坑)` 直接把整张卡塞在单元格里。

想查某个数字的出处：先在总表 `阈值数字` / `实验命中率` / `成本/统计` 列里搜，再顺着 `原文出处指针` 列
进卡（卡 §4 数字台账、§9 溯源），最后进卡声明的 `引句底稿`（本地全文或调研记录）。

## 迁移包与"喂给别的 AI"

`python scripts/build_bundles.py` 在 `deliverables/bundles/` 生成两个包（也发布在本仓库的 GitHub Release 上）：

| 包 | 内容 | 用途 |
|---|---|---|
| `..._full_<date>.zip` | git 跟踪的全部 445 个文件（含全文缓存与抓取日志） | 换机器重建；能原样复跑逐字引句门禁 |
| `..._ai_<date>.zip` | 卡片 + 总表 + 台账 + 模板 + 脚本 + 调研底稿，**不含** `fulltext/` 与 `data/interim/`，另附 `ai_ingest/` 分层 digest | 喂给别的 AI 当资料库 |

`ai_ingest/` 的分层：`tier0_index.md`（是什么+三条禁令）→ `tier1_core.md`（README+两份工作流+模板+前沿核验，≈2.7 万 token）
→ `tier2_cards.md`（152 张卡全文，≈130 万 token，**按编号取单张**，别整份喂）→ `tier3_ledgers/`（CSV，结构化问题走这里）。
喂法与 token 估算方法写在 `ai_ingest/HOW_TO_FEED.md`。AI 包不含论文原文，所以卡里的引句在该包内不可复核，
只能查到声明的底稿路径与哈希——需要原文复核时必须用完整包或本仓库。

## 目录

| 路径 | 内容 |
|---|---|
| `data/protein_design_literature.csv` | 文献总表：152 行 × 27 列（按 `人物组` 列首组计：通用方法学 67 / Baker 组 44 / 曹龙兴组 21 / 周如鸿组 16 / 口径对照与独立复核 4；多组重叠行有 13 行，故与"该组出现次数"口径不同） |
| `data/literature_cards/*.md` | 每篇一张精读卡，十节固定：0 元信息 · 1 解决什么 · 2 难点与应对 · 3 方法工作流 · 4 数字台账 · 5 作者说了什么 · 6 我们怎么推断 · 7 局限 · 8 能不能迁移 · 9 溯源（含 14 键 CSV 回填块） |
| `data/literature_cards/AGENT_RULES.md` | 写卡规程（引句必须逐字、文件名 slug、非论文行写"取证卡"的口径） |
| `data/literature_cards/fulltext/` | 本地全文抽取：41 行用本目录（另有 39 行用 `data/interim/baker_lit/ft/`、13 行用 `data/interim/claim_lit/`，6 行跨两处，合计覆盖 87 行）；`_quarantine/` 是身份体检判定"挂错行"的 9 份 + 日志 |
| `data/literature_cards/run.md` | 过程账：每一步的脚本、参数、实测输出、踩过的坑与更正 |
| `data/interim/` | 抓取日志、回写前的 CSV 备份、2000 处字段改动账 |
| `sources/*.md` | 四份调研底稿（Baker 组、周如鸿组、曹龙兴组、成本与判据经济学） |
| `scripts/` | 建库、核验、抓取、回写、台账生成的全部脚本 |
| `deliverables/` | 工作流模板（主模板+三分支）+ 证据工作流文档 + 机器生成的证据台账 + 前沿方法核验清单 |
| `deliverables/bundles/` | 迁移包与 AI 投喂包（由 `scripts/build_bundles.py` 生成，不进 git，发布走 GitHub Release） |

## 门禁（这就是"可复现"的意思）

```bash
cd <项目根目录>
set PYTHONIOENCODING=utf-8
python scripts/verify_literature_cards.py     # 152/152 PASS 才算完整；退出码非 0 = 没做完
python scripts/verify_workflow_doc.py         # 证据工作流文档的引用与链接体检
python scripts/verify_workflow_template.py    # 模板：引用可查 + 每条默认阈值带证据级别 + 链接可达
python scripts/verify_workflow_template.py --selftest   # 三种破坏必须各红一条
python scripts/build_bundles.py --check       # 包内清单与磁盘哈希一致
python scripts/build_workflow_evidence.py --check   # 台账行数必须等于从 CSV+卡重算的行数
```

门禁判的是五件事：每行有且仅有一张卡；十节标题齐全且顺序固定；工作流表 ≥3 步、难点 ≥2 条；
**卡里每一条纯英文直引号片段必须在该卡声明的那一份底稿里逐字命中**；证据级别不许造假
（没有本地全文却写"全文级"直接 FAIL）。它不判文献内容对不对——那是卡 §7 与 `report.md` §八 的活。

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

- 表级待改：`K49` 的 `期刊或预印本` 写 Amino Acids，Europe PMC 实查是 **Biophysical Reviews 18 卷**（DOI 与全文没错）；
  `K48` 的 `年份` 写 2025，全文题录 2024；`K59` 的 `核验状态` 写"✅Crossref核验"而 `DOI=未记录`（核验对象是 C&EN 新闻条目 DOI）。
  这三列都不在 14 个回填键范围内，所以是"记录在案、尚未改表"，改动账见 `data/interim/csv_field_corrections.json` 的规则说明。
- 65 行是 DEGRADED（没拿到正文）：它们的卡按摘要级/二级来源写，阈值与步骤细节不许补，卡 §2 已明写"未获正文无法核验"。
- `data/literature_cards/fulltext/` 与 `data/interim/` 缓存的是各出版商/PMC 的开放获取全文抽取，
  **仅用于逐字引句核验**。若要公开发布，建议把这两个目录移出仓库（卡里已保留 SHA/身份块指针，核验链不断）。

## 与"天然 UAA 合成酶发现"那条主线的关系

本仓库是**跨实验室判据有效性与成本的参考库**，不是那条主线的判定输入。
从头设计结合体的 `pAE_interaction` / `ipTM` 阈值、适配体 FEP 命中率、展示库通量，都**不许**当成酶活判据或成功概率——
每张卡的 §8 逐条写死了这条边界。那条主线由 `A:\Data\DP2R\方案` 的判定标准管辖。
