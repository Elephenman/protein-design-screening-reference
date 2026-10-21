# -*- coding: utf-8 -*-
"""polish_report.py — 去掉 §10 里重复的条目行，并在缺口清单插入两条更正。"""
import io

P = r"A:\Data\MD\projects\protein-design-screening-20261016\report.md"
lines = io.open(P, encoding="utf-8").read().split("\n")

seen, out, removed = set(), [], 0
for ln in lines:
    if ln.startswith("- **可复跑脚本**") or ln.startswith("- **调研底稿"):
        key = ln[:60]
        if key in seen:
            removed += 1
            continue
        seen.add(key)
    out.append(ln)
s = "\n".join(out)
print("删除重复行:", removed)

s = s.replace("通用方法学与成本 23（跨组重复条目已按 DOI 合并",
              "通用方法学与成本 23（其中 K27–K36 是为“90%+ 口径审计”与“MD 为何不当主筛”补的对照条目，"
              "含分子之心 Zenodo 技术报告、PLACER 与丝氨酸水解酶的已复核原句；跨组重复条目已按 DOI 合并")

old7 = '7. "设计失败原因分布"缺跨靶点统一口径的系统统计'
new7 = ('7. **一处更正（必须说明）**：底稿 `sources/baker.md` 记的“金属水解酶 96 → 11/96、零样本 >10⁴ M⁻¹s⁻¹”'
        '未能在 RFdiffusion2 正式论文（✅ [10.1038/s41592-025-02975-x](https://doi.org/10.1038/s41592-025-02975-x)，PMC12791007）中复核到；'
        '该论文实际写的是 “We obtained 96 designs for each and identified three functional enzymes for the 4MU-butyrate reaction and five for the '
        '4MU-phenylacetate reaction”，即 **3/96 与 5/96**，最佳 k_cat/K_M = 77±10 M⁻¹s⁻¹。“11/96”更可能出自尚未正式发表金属蛋白酶预印本'
        '（10.1101/2025.11.20.689622，无 OA 正文）。正文与 CSV 已改用复核后的数字。\n'
        '8. 分子之心 MMDesign 与 Anthropic 的“90%+”都是**技术报告/公司口径、未经同行评议**，且分母是靶点/战役级，'
        '不能与论文里的候选级命中率混用。\n'
        '9. "设计失败原因分布"缺跨靶点统一口径的系统统计')
assert old7 in s, "缺口第 7 条未找到"
s = s.replace(old7, new7)

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("报告行数:", s.count("\n"))
