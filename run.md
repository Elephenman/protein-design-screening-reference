# run.md — 本次任务的执行记录

- 日期：2026-10-16 ｜ 会话：Qoder Desktop ｜ 任务：从头设计蛋白的"筛选-成本"逻辑审计（周如鸿 / David Baker / 曹龙兴）+ 文献 CSV
- 交付目录：`A:\Data\MD\projects\protein-design-screening-20261016\`
- 版本控制：本项目未初始化 git（纯文献交付物，无源码变更）；所有可复现性靠下面的命令与数据文件本身。

## 1. 成功测试（开工前定义）

| # | 判据 | 实测结果 | 判定 |
|---|---|---|---|
| T1 | 报告与 CSV 中每条文献条目带可解析 DOI/PMID/arXiv，且经 Crossref（Zenodo 条目走 Zenodo API）实解析并核对标题 | 152 行：**121 行 OK**（标题 token 重合度 ≥0.3）、**0 行解析失败**、29 行价目表/厂商页/公司自述无 DOI（已标注）、2 行"汇总卡"（一行覆盖多篇，DOI 填代表论文，已在 `核验状态` 列写明） | **PASS（含 4 行如实标注的例外）** |
| T2 | 对"筛选用什么手段"给出具体论文 + 具体阈值/通过率数字 | 报告 §3、§4、§5、§6 与 CSV 的 `阈值数字`/`实验命中率`/`候选数递减` 列；关键原句由 `spot_check*.py` 从 Europe PMC 全文 / PubMed 摘要 / Zenodo API 独立复核（清单见报告 §10） | **PASS** |
| T3 | Baker / 周如鸿 / 曹龙兴各 ≥8 篇 2019–2026 | Baker 44 篇、周如鸿 16 篇、曹龙兴 22 篇（CSV 分组计数） | **PASS** |
| T4 | 呈现方法演进时间线（逻辑链） | 报告 §7 一页链 + 各底稿第三节逐年链 | **PASS** |

## 2. 命令与脚本

```
# 结构化文献表（解析 sources/*.md 的卡片 + 手工核对的 K 类条目 → CSV）
cd A:\Data\MD\projects\protein-design-screening-20261016\data
set PYTHONIOENCODING=utf-8
python build_csv.py           # 解析 sources/*.md → protein_design_literature.csv（UTF-8 BOM）
python finalize_csv.py      # 撤销误引 + 官方标题回填 + 追加口径审计行 + 回填已复核原句（幂等）

# 机械门禁：逐行 DOI 解析 + 标题重合度 + 年份差
python verify_gate.py         # 输出 gate.json + gate_report.md

# 关键原句独立复核（三批，宽松匹配，容忍排版差异）
python spot_check.py          # 按 DOI 解析 PMCID → Europe PMC fullTextXML → 搜原句
python spot_check2.py         # 宽松正则（GPU-seconds / 2.3% / 19% / fewer than 100 等）
python spot_check3.py         # Rocklin 6→47%、Gerasimavicius 0.26/0.28、PLACER 原句
python spot_check4.py > spot_check4.out   # 终轮取证：误引核查 + PLACER/丝氨酸水解酶/RFdiffusion2 原句

# 报告文字补丁（去重 + 更正条目）
python polish_report.py
```

外部数据源（全部只读 GET）：`api.crossref.org/works/<doi>`、`api.crossref.org/works?query.bibliographic=`、
`www.ebi.ac.uk/europepmc/webservices/rest/search|<PMCID>/fullTextXML`、`eutils.ncbi.nlm.nih.gov/entrez/eutils/{esearch,esummary,efetch}.fcgi`、
`export.arxiv.org/api/query`、`zenodo.org/api/records/<id>`、`www.biorxiv.org/content/...`。

调研分工：4 个并行子代理分别产出 `sources/baker.md`（44 卡片+46 篇全文缓存）、`sources/zhou.md`（16 卡片）、
`sources/cao.md`（25 卡片）、`sources/cost-benchmarks.md`（成本与判据相关性）、`sources/claim-90pct.md`（"90%+"口径审计）。
主代理（Qoder）负责：CSV 抽取与门禁、原句独立复核、报告撰写与更正。

## 3. 已知限制与诚实声明

- CSV 的 `实验命中率` / `候选数递减` 列由正则从底稿正文抽取，**是提示性线索而非可信终值**；引用硬数字请回到 `sources/*.md` 的原句与 URL（每行 `原文出处指针` 列给了卡片号）。
- **门禁抓到并撤销的一条误引**：抽取脚本补入的"氢键网络深度学习"条目，DOI `10.1093/bioinformatics/btab35` 经 Crossref 返回 404，PMID `33956864` 经 efetch 核对是 *Distribution of Merlin in eukaryotes…*（另一领域）。已从 CSV 删除，替换为 10.1021/acs.jctc.8b00033（JCTC 2018）与 10.64898/2026.06.08.730848（HBDesigner 预印本）两条可核验条目；核查命令在 spot_check4.py。
- 底稿转引而本次未能独立复核的数字，已在报告 §9 逐条列出（曹组 Science 2026 的 24→1 / 48→27 只有新闻口径；周组数篇付费全文的窗口与阈值；RFdiffusion3 等 2026 预印本命中率）。
- **一次自查纠正**：我复核 RFdiffusion2 论文时先用了 `"11 of the 96"` 这类写法匹配、未命中，差点把底稿正确的"96 → 11/96、k_cat/K_M 53,000"判成"未核实"并写进更正；换原文写法（"we identified 11 functional enzymes"、"41/41 cases"）后确认底稿正确，报告 §9 第 7 条记录了这次纠错。
- `data/interim/claim_lit/`：口径审计用的 19 份全文 XML 与页面快照（原在 tmp/，按规则归档到 interim）。项目根 `tmp/` 现为空。
- 中国核心设施价目表是公开收费页快照（部分页面为 2010/2019/2021 年），只用于量级比较。
- "每候选美元 vs 每候选 GPU·小时"的对比是本报告按已核验单价做的算术，标注为〔本报告推算〕，不是文献结论。
- 周如鸿与曹龙兴**未发现任何合著论文**（PubMed/Europe PMC/ORCID 多种检索串均为 0）；讲座中"90%+"的原始口径无法核实，需要讲者 PPT 数据页才能定论。

## 4. 中间产物

- `data/interim/baker_lit/`：Baker 侧 46 篇 Europe PMC 全文缓存（`ft/`）、逐句抽取（`dig/`）、MD/QM 分类输出（`mdqm.out`）、DOI 核验输出（`verify.out`）与抓取/核验脚本。保留理由：报告结论可逐条回溯。项目根 `tmp/` 已清空。

## 5. 2026-10-20 追加：逐篇文献精读卡（样板阶段）

- 目录：`data/literature_cards/`（`README.md` 定 10 节格式与批量推广规则，`run.md` 记命令与产物，`B09_Bennett-2023_NatComms_af2-filter.md` 是样板卡）。
- 新增脚本：`scripts/verify_literature_cards.py`（逐字引句 × 多份本地全文互证 + 行号可达性；PASS 退出 0 / FAIL 退出 1）。
- 本轮判定：**样板卡 PASS（36/36 × 2 份全文）**；反向自测（篡改一个数字 + 登记缺失全文）判 FAIL 退出码 1。
- 待用户确认样板格式后再按 P1→P5 批次铺开 151 行。
