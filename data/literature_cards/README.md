# 逐篇文献精读卡（152 行全覆盖）

CSV（`data/protein_design_literature.csv`）是**索引**：一行一篇，字段短。本目录是**内容**：一篇一张卡，写清"用了什么方法、工作流程一步步怎么走、遇到问题时他们做了什么"。卡片完成后，内容按 §6 回写进 CSV 对应行背后。

## 1. 卡片固定格式（10 节，编号必须是 `## 0.` ~ `## 9.`）

| 节 | 标题必须含 | 写什么 | 不许做什么 |
|---|---|---|---|
| 0 | 元信息 | DOI/PMID/PMCID、 venue、本地底稿文件+SHA、抓取通路、证据级别、未取到的部分 | 把"摘要级"写成"全文级" |
| 1 | 解决什么 / 一句话 | 大白话一段：这篇要解决什么、比前作多做了什么 | 堆术语 |
| 2 | 难点 | **遇到的问题，以及遇到问题他们做了什么**：每条 = 难点 → 现象/证据（尽量原句）→ 应对动作 → 应对后仍留下的代价 | 只写难点不写应对；把我们的猜测当作者原话 |
| 3 | 方法 + 工作流 | 先"用了哪些方法（工具箱+为什么选它）"，再**步骤表**：每步 `输入 → 操作 → 判据/阈值 → 输出规模`，顺序可复现 | 只写"用了 AF2 筛选"这种无顺序无阈值的话 |
| 4 | 台账 | 关键数字一行一条：数值 · 含义 · 出处（原句或表号） | 写没有出处的数字 |
| 5 | 作者 | 作者本人的结论，含他们自认的边界 | 替作者加码 |
| 6 | 我们 | 我们的推断，与第 5 节物理分开 | 与第 5 节混写 |
| 7 | 局限 | 作者承认的 + 我们读出的方法学漏洞 | 省略"其实没做成的部分" |
| 8 | 迁移 | 对酶设计筛选：可迁移（怎么用）/ 不可迁移（为什么不能照搬），挂本库 G0–G10 门 | 借 binder 的 pAE/ipTM 阈值当酶活判据 |
| 9 | 溯源 | 本地底稿路径+行号、原文短引、核验命令与结果、CSV 回填块 | 只写"见 PMC" |

**没有本地全文的行**（`inventory.json` 里 `has_fulltext=false` 且抓取记 `NO_OA_FULLTEXT`/`FETCH_FAILED`）只能出**降级卡**：第 3、4 节只允许写摘要、图注、以及 `sources/*.md` 里已核过的句子；第 2 节要写明"作者自述部分未获正文，无法核验"；第 0 节证据级别必须写"摘要级/二级来源/未获正文"。降级卡不许出现"全文"字样。

## 2. 逐字引句的硬规矩（机器执行）

- 卡内**直双引号包住、纯 ASCII、≥20 字符**的片段 = 声明为逐字引用，必须在**该编号登记的每一份本地全文**里逐字命中；一条不命中 → 该卡 FAIL。
- 不许跨句拼接（原文两句之间插着参考文献编号/脚注时，拆成两条引句）；不许用省略号开头冒充引句；状态名、术语不要加英文引号（会被当引句核验）。
- 有全文的卡 ≥8 条引句；降级卡 ≥2 条且必须命中登记的底稿。

## 3. 底稿登记（不许靠记忆）

- `data/literature_cards/inventory.json`：每行的号、本地底稿路径、抓取通道与 URL。底稿判定只在缓存文件**头部 8000 字符**内按 PMCID/PPR/DOI 实搜（全文正文里引用别人的号会误配，已踩过一次）。
- `data/literature_cards/sources_map.json`：编号 → 该卡要核验的全部底稿路径。用 `--sync-map` 重建，不手写。
- 新抓的全文一律进 `fulltext/<编号>_<号>_fullTextXML.xml` + 同名 `_text.txt`（归一化由 `scripts/litcards_text.py` 唯一实现，抓取侧与核验侧共用，防止两侧处理方式不同导致假红/假绿）。

## 4. 命令

```bash
python scripts/litcards_inventory.py                       # 对账：每行 ↔ 号 ↔ 本地底稿
python scripts/litcards_fetch.py                           # 缺全文的行走 Europe PMC 抓取并记账
python scripts/verify_literature_cards.py --sync-map       # 重建 sources_map.json
python scripts/verify_literature_cards.py                  # 全量门禁（红则退出 1）
python scripts/verify_literature_cards.py --only B09 B20    # 只验指定编号
python scripts/litcards_embed_csv.py                       # 卡片内容回写 CSV（需全量门禁先 PASS）
```

## 5. 批量推广批次（按信息价值排序）

P1 Baker 35 行 → P2 曹龙兴 25 行 → P3 周如鸿 16 行 → P4 通用方法学 67 行 → P5 口径对照 4 行；每代理 8–10 行，交批次前必须跑到 `verify_literature_cards.py --only <本批编号>` 全 PASS。

## 6. 回写 CSV（卡片完成后的动作）

`litcards_embed_csv.py` 在**全量门禁 PASS** 后做两件事：① 用卡片第 9 节的 CSV 回填块覆盖 14 个内容字段（`未记录` 只允许在卡片明写未记录时出现）；② 追加两列 `精读卡文件` 与 `精读卡全文(方法·工作流·遇坑)`（整张卡原样塞进对应行背后）。改写前先备份 `data/interim/protein_design_literature_backup_<日期>.csv` 并记 SHA-256。

## 7. 样板卡

[B09_Bennett-2023_NatComms_af2-filter.md](B09_Bennett-2023_NatComms_af2-filter.md)（36/36 条引句 × 2 份独立全文命中）。写新卡前先看它。
