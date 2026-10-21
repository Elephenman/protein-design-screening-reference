import io, sys
p = r"A:\Data\MD\projects\protein-design-screening-20261016\sources\baker.md"
t = open(p, encoding="utf-8").read()

subs = []

subs.append((
 "- 失败机理分类（该文最有价值的概念）",
 "- 时间线位置: 把 [B06] 的近百万条湿实验标注变成『筛选器训练/评估集』，第一次给出『漏斗该用哪个判据』的定量答案，并把失败归因结构化（Type I / Type II）；其结论（AF2/RF2 界面 pAE_interaction 是最强判据、阈值 10）直接成为 [B08] 之后所有 binder 论文的默认闸口，其暴露的成本（30 GPU-秒/设计、仅 2.3% 通过）则催生 [B05]/[B28] 的序列端加速。\n"
 "- 失败机理分类（该文最有价值的概念）"))

subs.append((
 "- MD 使用: 未核对 / QM 使用: 未核对",
 "- MD 使用: 未核对 / QM 使用: 未核对\n"
 "- 实验验证方法与通量: 仅摘要级（本卡片未抓取正文方法段，故不填写未经核实的通量与命中率）"))

subs.append((
 "- DOI: 10.1101/2025.09.18.676967 ✅（Crossref 核验；未核验正式刊期 ⚠️）",
 "- DOI: 10.1101/2025.09.18.676967 ✅（Crossref 核验，23 人，has_baker=True；未见正式刊期记录 ⚠️）  PMID: 无（预印本，PubMed 未收录）"))

subs.append((
 "- MD: 否 / QM: 否（摘要级）",
 "- MD: 否 / QM: 否（均为摘要 + bioRxiv 页面级判断，未见判据细节）\n"
 "- 实验验证方法与通量: 摘要级——bioRxiv 摘要页未给下单数/命中率，仅『designing and experimentally characterizing DNA binding proteins and cysteine hydrolases』"))

subs.append((
 "- 关键原文（摘要）: \"While there is still room for improvement",
 "- 设计对象/靶点: 不适用（综述，覆盖 fold / 组装体 / 蛋白结合体 / 酶 / 多态开关全谱）\n"
 "- 候选生成方法与计算筛选器: 不适用（综述；正文未抓取，本报告仅使用摘要）\n"
 "- MD / QM 角色: 摘要未提及，不作为证据\n"
 "- 实验验证方法与通量: 不适用（综述）\n"
 "- 关键原文（摘要）: \"While there is still room for improvement"))

missing = []
for a, b in subs:
    if a in t:
        t = t.replace(a, b, 1)
    else:
        missing.append(a[:60])
open(p, "w", encoding="utf-8").write(t)
print("applied:", len(subs) - len(missing), "missing:", missing)
