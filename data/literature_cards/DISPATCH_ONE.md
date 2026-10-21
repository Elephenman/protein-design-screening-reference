# 单张卡的作业单（一个代理只写一张）

前置：一个代理只负责一个 CSV 编号。上一批让代理一次读三篇 40–90 KB 的全文，结果读完就断了、磁盘上什么都没留下。

按顺序做，不许跳步：

1. 读 `data/literature_cards/AGENT_RULES.md`（10 节格式 + 引句硬规则 + CSV 回填块键名）和样板卡 `data/literature_cards/B09_Bennett-2023_NatComms_af2-filter.md`。
2. 在 `data/literature_cards/batches.tsv` 里按 id 找到你这一行，读 `state`、`fulltexts`、`records` 三列；再对照 `data/literature_cards/sources_map.json` 里该编号登记的底稿清单。
   - `state=FULLTEXT`：必须真读 `fulltexts` 里的全文（用 Grep 定位 Abstract/Results/Methods/图注/Discussion，再分段读，不要整篇一次吞）。
   - `state=DEGRADED`：只准按 `records`（`sources/*.md` 对应卡片段落）和摘要级信息写降级卡；第 3、4 节不许编造阈值与步骤；卡内不许出现"全文级"。
3. **先落盘再写内容**：立刻 Write 出 `data/literature_cards/<slug>_<短标题slug>.md` 的十节骨架（`## 0.` 到 `## 9.`，标题按 AGENT_RULES 的关键词），然后逐节 Edit。任何时刻中断，磁盘上都要有一张能看的卡。
   - `<slug>`：CSV 编号里非字母数字的字符全换成 `-`。编号 `B06; C02` → 文件名 `B06-C02_xxx.md`。写错文件名 = 门禁判"无卡片文件"。
4. 引句纪律（门禁逐字比对，一条不命中整卡 FAIL）：
   - 引句必须是从全文里复制粘贴的原句；
   - 不跨句拼接（原文两句之间夹参考文献编号 `21`、脚注、`Fig. 1` 时，拆成两条引句）；
   - 不用省略号开头/结尾冒充引句；
   - 术语、状态名（UNKNOWN、METHOD_FAIL 这类）不要加英文双引号；
   - 有全文的卡 ≥8 条引句，降级卡 ≥2 条且必须能在登记底稿里命中。
- **每张卡必须在 §9 溯源里写一行**：`引句底稿: data/literature_cards/fulltext/<编号>_<PMC号>_text.txt`（或降级卡的 `sources/xxx.md`）。门禁只拿这一份文件逐字比对全部引句；同一篇论文可能有 Europe PMC 与 NCBI 两份抽取版本，句子中间夹的参考文献编号不一样，所以必须声明你实际照着写的那一份。**不写这行 = 卡片直接 FAIL。**
5. 三块重点写厚：第 3 节工作流程表 ≥3 步（每步 `输入 → 操作 → 判据/阈值 → 输出规模`，阈值必须是原文数字，没有就写"原文未给阈值"）；第 2 节难点 ≥2 条，每条都要写"**他们做了什么应对**"，作者没解决的明写"本文未解决"；第 4 节数字台账每行 `数值 · 含义 · 出处`。
6. 第 9 节末尾写 `<!--CSV回填` … `CSV回填-->` 块：14 个键一个不能少，值不能为空也不能换行，确实没有写 `未记录（原因）`。
7. 自检到绿为止：

```bash
cd A:\Data\MD\projects\protein-design-screening-20261016
PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "<你的编号原样带空格分号，要加引号>" --no-report
```

看到 `PASS <编号> quotes=N/N` 且退出码 0 才算完成。

禁止：`--sync-map`；不带 `--no-report` 的全量门禁；改 CSV、`sources/*.md`、样板卡 B09、`scripts/` 下任何文件；新的网络抓取。

回报（120 字内）：PASS/FAIL、引句数、卡片文件名、这篇最可疑的一个判据或结论（一句话）。
