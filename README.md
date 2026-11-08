# 蛋白设计筛选参考库

**152 篇文献 · 一文献一卡 · 每个阈值都能回到原文那一句**

[![papers](https://img.shields.io/badge/papers-152-1f6feb?style=flat-square)](data/protein_design_literature.csv)
[![cards](https://img.shields.io/badge/deep--read%20cards-153-1f6feb?style=flat-square)](data/literature_cards)
[![columns](https://img.shields.io/badge/table-27%20columns-1f6feb?style=flat-square)](data/protein_design_literature.csv)
[![gates](https://img.shields.io/badge/gates-13%2F13%20passing-2ea043?style=flat-square)](scripts)
[![python](https://img.shields.io/badge/python-3.10%2B-2ea043?style=flat-square)](scripts)
[![license](https://img.shields.io/badge/license-custom%20%C2%B7%20see%20LICENSE-8957e5?style=flat-square)](LICENSE)

> A verifiable reference library for protein design screening: 152 papers, one deep-read card per paper,
> 87 default thresholds, 13 regression gates. Every quoted number is matched word-for-word against the
> paper text that it cites — no paraphrased numbers, no reconstructed citations.

从零设计一个结合体或一个酶，真正难的不是"用哪个模型"，而是**判据**：pAE 多少算过、界面氢键几条算过、
一轮该下多少个候选、命中率的分母到底是谁、哪个读数只是 `in silico` 的自嗨。这些问题在论文里散落着、
口径互不相同，而且经常被二手转述改掉。本库把它们收在一处，并且给每个数字留一条可以走回去的路。

---

## 30 秒判断这是不是你需要的

- 你正在**选阈值**，但不知道文献里那些人实际用的是多少、在什么条件下失效。
- 你正在**写方法学或立项书**，需要"别人用了多少候选、命中率多少、花了多少钱"的一手数字。
- 你要给**别的 AI** 一份能直接投喂的蛋白设计知识库，而不是一堆 PDF。
- 你要一套**今天就能开工**的模板，以及"第二轮该怎么打"的迭代协议。

如果以上有一条命中，[三分钟上手](#三分钟上手) 下面的五个入口就够了。

---

## 亮点

**每个数字都有一句原文。** 每张卡的英文直引号片段，必须在该卡声明的那一份底稿里**逐字命中**，由脚本强制；
没有本地全文的行只能写"摘要级/二级来源"，写"全文级"直接判失败。引句、卡、总表三者不许各说各话。

**结论分三态，不含糊。** 每条判断都落成"能证明 / 不能证明 / 尚缺什么"。例如"计算闸口把下单量从 10⁵ 压到
10²–10³，并把成功率提一个数量级"能证明（[B09][B08]）；"每候选 μs 级 MD/FEP 预筛更省"不能证明（[K27]）；
"MD 精筛把命中率从 X% 提到 Y%"至今缺公开同口径基准——缺，不等于不存在。

**判据前置，不是事后解释。** 工作流模板里 87 条默认阈值，每条带 P0–P5 证据级别；证据级别不够的阈值
不许写成"推荐值"。要把默认值变成"你的数"，走模板 §H 的七步重校准协议。

**机器可复现。** 13 道门禁覆盖"卡是否齐全、引句是否逐字命中、证据级别是否造假、台账是否与源数据逐字节一致、
公开树里有没有混进不该有的东西"。改坏一条引句，门禁立刻变红。

**公开即合规。** 224 份第三方原文逐份登记（路径、字节、sha256、许可类别、重取方式），87 篇逐篇许可判定，
受限来源的引句按统一预算截短并留改动账。仓库只分发作者原创内容，第三方全文一份都不随包走。

---

## 三分钟上手

1. [report.md](report.md) — 结论报告。先看这里，包括"我们没能核实到什么"的缺口清单（§八）。
2. [工作流模板 v2](deliverables/protein_design_workflow_template.md) — **开工就抄这份**：主线十阶段的默认阈值、
   三个闸口与停止条件、预算四档、阈值重校准协议，外加 binder / 酶 / 肽与大环三个分支页。
   开工登记压到附录 §I（10 分钟填完）；前沿默认链已换到 **RFD4-Proteina 共设计**（§F，含退回条件）。
3. [多轮迭代协议](deliverables/protein_design_workflow_iteration.md) — **第二轮起看这份**：一轮的定义与必留三文件、
   候选/判据/路线三轴分离（一轮只动一个轴）、逐分支第二轮怎么打、T0（≤4 构建体）档怎么迭代、多轮战役怎么报数。
4. [证据工作流](deliverables/protein_design_workflow.md) — 模板里每个数字的原文出处与失灵域。
5. [文献总表](data/protein_design_literature.csv) — 152 行 × 27 列，Excel 直接打开（UTF-8 BOM）。
   任意一行最后两列给出单卡路径，并把整张卡塞进单元格，复制即可投喂。

想查某个数字的出处，按下面这条路径走，不走回头路：

```
总表「阈值数字 / 实验命中率 / 成本·统计」列
      → 「原文出处指针」列
      → 精读卡 §4 数字台账 / §9 溯源
      → 卡声明的引句底稿（路径 + sha256）
      → 按 deliverables/fulltext_manifest.csv 里登记的 URL 重取并校验
```

---

## 库里有什么

| 内容 | 规模 | 入口 |
|---|---|---|
| 文献总表 | 152 行 × 27 列：设计对象、候选生成方法、计算判据、阈值、是否用 MD/QM、实验手段、候选递减、命中率、最好读数、证据级别、成本与统计、出处指针 | `data/protein_design_literature.csv` |
| 精读卡 | 153 个文件（B28 一行保留早期与后续两版同篇卡，引用以台账指向的那张为准），固定十节：元信息 · 解决什么 · 难点与应对 · 方法工作流 · 数字台账 · 作者原话 · 我们的推断 · 局限 · 能不能迁移 · 溯源 | `data/literature_cards/*.md` |
| 结构化抽取 | 679 条判据条目；76/152 行给出可用命中率口径；36 行声明用了 MD、18 行用了 QM | `deliverables/protein_design_workflow_evidence.csv` |
| 工作流模板 | 主线十阶段 + 三个分支页 + 预算四档 + 七步重校准；87 条默认阈值 | `deliverables/protein_design_workflow_template.md` |
| 多轮迭代协议 | 真实轮次台账（每条带分母）+ 三轴分离 + 第 0 轮 pilot + T0 档 | `deliverables/protein_design_workflow_iteration.md` |
| 审核视图 | 单文件 HTML，把 87 条阈值、379 处引用摊开，可逐行标记并导出审核意见；页面无手打数字 | `deliverables/protein_design_workflow_visual.html` |
| 前沿核验清单 | 23 条（S0–S22），每条给出核实状态与一手件 | `deliverables/frontier_methods_2025_2026.md` |
| 调研底稿 | 六份：Baker 组、曹龙兴组、周如鸿组、成本与判据经济学、90% 声明可查证性、功能判定工作流 | `sources/*.md` |
| 脚本 | 22 个：建库、核验、抓取、回写、台账生成、打包、许可审计 | `scripts/` |

分组（按总表首组计）：通用方法学 67 · Baker 组 44 · 曹龙兴组 21 · 周如鸿组 16 · 口径对照与独立复核 4。
多组重叠行 13 行，所以与"某组出现次数"口径不同。

---

## 工作流模板：主线十阶段

模板不是"工具说明书"，是一条从靶点到下一轮的顺序，每个阶段都有**输入、默认动作、闸口、停止条件**：

| 阶段 | 要回答的问题 | 关键出口 |
|---|---|---|
| ① 定靶与位点 | 表位/活性位点定在哪，哪些残基不许动 | 位点定义 + 反例清单 |
| ② 骨架生成 | 用哪条生成链，出多少骨架 | 骨架池与多样性口径 |
| ③ 序列设计 | 序列由谁定，固定位点怎么传 | 每条骨架的序列候选 |
| ④ 计算预筛（闸门 A） | 哪些读数能真的预测实验成败 | 递减曲线，不是单一分数 |
| ⑤ 递减到可下单规模 | 从 10⁵ 减到 10²–10³ 的依据 | 下单表 |
| ⑥ DNA 与合成 | 序列到构建体的误差从哪来 | 构建体清单与预算 |
| ⑦ 表达、可溶与折叠 | 表达失败怎么和设计失败分开 | 表达筛查读数 |
| ⑧ 结合/功能初筛（闸门 B） | 一次便宜读数换一个生死判断 | 初筛通过集 |
| ⑨ 定量与结构确证 | 只给末端 1–5% 花这个钱 | Kd/活性/结构 |
| ⑩ 回灌与下一轮 | 这轮学到的东西写回哪里 | 下一轮的三个文件 |

模板另有三个分支路由（binder / 酶 / 肽与大环）、预算四档（先选档再谈判据）、防自欺六问，以及"哪些阈值
不能跨目标搬运"的边界表——每张卡 §8 逐条写死了"能不能迁移"。

**第二轮起**看迭代协议：一轮 = 一个假设 + 一组改动的轴 + 三个必留文件；候选轴、判据轴、路线轴分开，
一轮只动一个轴；什么时候该换打法、什么时候该停，协议里给了可判定的条件，而不是"再试一轮看看"。

---

## 可复现：13 道门禁

```bash
cd <项目根目录>
set PYTHONIOENCODING=utf-8

python scripts/verify_literature_cards.py            # 152/152 PASS 才算完整
python scripts/verify_workflow_doc.py                # 证据文档的引用与链接体检
python scripts/verify_workflow_template.py           # 模板：引用可查 + 阈值带证据级别 + 链接可达
python scripts/verify_workflow_template.py --selftest    # 四种破坏各红一条
python scripts/build_workflow_evidence.py --check    # 台账 = 从 CSV+卡 重算的结果（CRLF/LF 归一后逐字节）
python scripts/build_workflow_visual.py --check      # 页面无手打数字
python scripts/build_bundles.py --check              # 包内清单与磁盘哈希一致
python scripts/build_fulltext_manifest.py --check    # 224 份原文的路径/字节/sha256/许可与磁盘一致
python scripts/audit_source_licenses.py --check      # 许可分类逐行与重算一致
python scripts/audit_quote_budget_exceptions.py --check   # 引句预算例外逐条有理由
python scripts/apply_quote_budget.py --check         # 卡片引句预算账与现状一致
python scripts/apply_note_quote_budget.py --check    # 底稿引句预算账与现状一致
python scripts/audit_public_tree.py                  # 第三方原文 0 处被跟踪 + 受限引句单条 ≤400 字符
python scripts/audit_public_tree.py --selftest       # 三种破坏各红一条
python scripts/fix_table_fields.py --check           # 表级改动账：账里新值 == 当前表
```

门禁判的是五件事：每行有且仅有一张卡；十节标题齐全且顺序固定；工作流表 ≥3 步、难点 ≥2 条；
**卡里每一条英文直引号片段必须在该卡声明的那份底稿里逐字命中**；证据级别不许造假。
它不判文献内容对不对——那是卡 §7 与 `report.md` §八 的活。

上面的代码块里，带 `--selftest` 的两条是**门禁自身的破坏自测**（必须变红才算通过），其余 13 条是判定门禁。

在**公开克隆**里（本机第三方底稿不在场），第一条门禁按三态判定：
`PASS_LOCAL`（可逐字核验）/ `WITHHELD`（底稿按公开口径不随包分发）/ `FAIL`（真错误）。
实测：维护者工作树 `PASS_LOCAL 152/152 · WITHHELD 0 · FAIL 0`；公开克隆 `WITHHELD 80 · FAIL 0`，
在场的 72 行全部 `PASS_LOCAL`。把一条引句改坏，立刻 `FAIL 1`——门禁依然能红。

---

## 公开仓库的四条硬规矩

公开 = 公开再分发，所以本库按"只分发作者原创内容"处理，规则写死在 `.gitignore` 与门禁里：

1. **第三方原文一律不入库。** PMC/出版商全文抽取、逐句转储、题录缓存、预印本正文都不被 git 跟踪，
   也不进任何发布包。逐份登记在 `deliverables/fulltext_manifest.csv`（224 份：路径、字节、sha256、
   许可类别、是否随仓库分发、重取方式），需要哪一份按表取回并校验哈希。
2. **逐篇许可判定。** 87 行做过许可审计（61 行允许含商用再分发，26 行不允许），报告见
   `deliverables/protein_design_license_audit.md`，机器版为同目录 `.csv`。审计只判"能不能再分发"，
   不判内容对错。
3. **引句按统一预算截短。** 许可受限来源与许可未审计的行，引句截到引用级：单条 ≤100 字符、
   同一来源行在同卡内合计 ≤600 字符；截短后仍逐字命中同一份底稿，门禁不放宽。可再分发行（CC BY / CC0）
   保持原样并履行署名。
   实测：卡片 7,125 条引句里受限来源 2,180 条、257,368 字符压到 93,663 字符（−63.6%，截短 1,804 条，43 张卡）；
   调研底稿与迭代台账 618 条引句里受限 160 条、21,328 → 13,466 字符（−36.9%）。
   每条截前/截后字符数、来源编号、许可类别与例外理由见 `deliverables/quote_budget_*.csv`。
4. **公开树再体检。** `scripts/audit_public_tree.py` 判两件事：清单里标"不随仓库分发"的 220 份第三方原文
   **0 份**出现在 git 跟踪集里；受限来源的逐字引句单条不超过 400 字符（实测最长 344）。
   当前口径：第三方引句 13,565 处 / 1,251,012 字符，其中受限 4,430 处 / 197,459 字符。

商业交付版本同样不含第三方全文——这是义务履行成本与客户侧一致性的选择，不是许可允不允许的问题。

---

## 迁移包与"喂给别的 AI"

`python scripts/build_bundles.py` 在 `deliverables/bundles/` 生成两个包，同时发布在本仓库的 Release 上：

| 包 | 内容 | 用途 |
|---|---|---|
| `..._full_<date>.zip`（约 270 个文件） | git 可见的全部原创文件 + `LICENSE`/`NOTICE`/`CITATION.cff` | 换机器重建工作树；不含任何第三方原文 |
| `..._ai_<date>.zip`（约 253 项） | 卡片 + 总表 + 台账 + 模板 + 迭代协议 + 脚本 + 调研底稿 + `ai_ingest/` 分层 digest | 喂给别的 AI 当资料库 |

`ai_ingest/` 分四层，按需加载，别一次全喂：

| 层 | 文件 | 内容 | 粗估 token |
|---|---|---|---|
| T0 | `tier0_index.md` | 是什么 + 三条禁令 | 1–2k |
| T1 | `tier1_core.md` | README + 两份工作流 + 模板 + 前沿核验 + 发布说明 | ≈58k |
| T2 | `tier2_cards.md` | 153 张卡 / 152 行，**按编号取单张** | ≈127 万（别整份喂） |
| T3 | `tier3_ledgers/` | CSV 台账，结构化问题走这里 | — |

喂法、复述校验与 token 估算方法写在 `ai_ingest/HOW_TO_FEED.md`。包内不含论文原文，所以卡里的引句在包内
不可复核，只能查到声明的底稿路径与哈希；需要原文复核时按 `fulltext_manifest.csv` 重取，或用本机工作树。

最新发布：Release [`v1-template-and-bundles`](https://github.com/Elephenman/protein-design-screening-reference/releases/tag/v1-template-and-bundles)。
两个资产上传后都**从服务端重新下载并逐字节比对 sha256**，与本地一致；哈希见 Release 资产页的 `digest`
字段与本地的 `deliverables/bundles/SHA256SUMS.txt`（该目录被 gitignore，不进仓库也不进包——
把发布物的哈希写进被发布物本身会自指）。

---

## 目录

| 路径 | 内容 |
|---|---|
| `report.md` | 结论报告：能证明什么、不能证明什么、缺口清单 |
| `run.md` | 过程账：每一步的脚本、参数、实测输出与更正 |
| `data/protein_design_literature.csv` | 152 行 × 27 列文献总表 |
| `data/literature_cards/` | 153 张十节精读卡 + 写卡规程 `AGENT_RULES.md`；`fulltext/` 为本地底稿（不入库） |
| `data/interim/` | 抓取日志、CSV 回写备份、字段改动账、许可抓取缓存（第三方部分不入库） |
| `deliverables/` | 模板、迭代协议、证据工作流、审核视图、证据/判据台账、前沿核验、许可审计与引句预算账 |
| `deliverables/rfd4_2026-11-07/` | RFD4-Proteina 取证本：官方说明、事实台账、`PROVENANCE.md`（sha256 + 重取 URL） |
| `sources/` | 六份调研底稿 |
| `scripts/` | 建库、核验、抓取、回写、台账、打包、许可审计脚本 |
| `LICENSE` / `NOTICE` / `CITATION.cff` | 授权（只覆盖原创部分）／第三方声明与许可分布／引用信息 |

---

## 常见问题

**这是一份综述吗？**
不是。综述按主题叙述，本库按"判据 + 数字 + 出处"索引。目标是让你在十分钟内查到"这条阈值是谁定的、
在什么体系上成立、换体系还成不成立"，而不是读完一段流畅的转述。

**能直接把模板里的阈值拿去跑吗？**
默认值是起点，不是承诺。模板 §H 给了七步重校准：先定你自己的阴性与阳性锚，再改阈值，再验证门禁，
每步都要留数。跨目标搬阈值正是本库反复标注的失败模式。

**为什么有些卡写"摘要级"？**
因为那份正文没有可核验的本地底稿，或者引句在手上那份全文里并不逐字一致。这时库只允许写摘要级，
阈值与步骤细节不许补——写"全文级"会被门禁直接判失败。严格标注比好看更重要。

**包里为什么没有论文 PDF？**
公开再分发第三方全文不是本库要做的事。224 份原文的路径、哈希与重取方式都登记在清单里，
需要时按表取回即可复现核验链。

---

## 引用与许可

如果本库的阈值表或工作流模板帮到了你，请引用：

```
蛋白设计筛选参考库，Elephenman，2026。
逐篇文献出处见 data/protein_design_literature.csv 的 DOI / PMID 列。
```

机器可读信息见 `CITATION.cff`；许可条款见 `LICENSE`（只覆盖作者原创部分，第三方内容明确排除），
第三方许可分布见 `NOTICE` 与 `deliverables/protein_design_license_audit.md`。

建库时间 2026-10-16 至 2026-10-21；工作流模板 v2 与多轮迭代协议 2026-11-07 改版（同日核实 RFD4-Proteina）；
本仓库自 2026-11-08 起公开。
