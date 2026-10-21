# -*- coding: utf-8 -*-
"""
finalize_csv.py — 在 build_csv.py 产出的 CSV 上做确定性收尾（可重复运行，幂等）：

  A) 撤销无法复现的误引（K67：DOI 10.1093/bioinformatics/btab35 → Crossref 404；PMID 33956864 → 是另一篇
     完全不同的论文）。改为两条可核验的氢键判据文献（10.1021/acs.jctc.8b00033 与 HBDesigner 预印本）。
  B) 用 gate.json 里 Crossref/Zenodo 返回的官方标题替换我底稿里的中文简称（防串号、便于检索）。
  C) 从 k_rows.py 追加"90%+ 口径审计"与"独立复核原句"条目（按 DOI 去重，不新增未核验文献）。
  D) 回填本次从 Europe PMC 全文/PubMed 摘要/Zenodo API 逐句复核过的原句到对应行。

流程：build_csv.py → verify_gate.py → finalize_csv.py → verify_gate.py（出最终 gate_report.md）
"""
import csv, json, os, re, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSVIN = os.path.join(HERE, "protein_design_literature.csv")
GATE = os.path.join(HERE, "gate.json")
sys.path.insert(0, HERE)
from k_rows import K_ROWS as K_TUPLES

# ---------- A) 误引处置 ----------
BAD_DOI = "10.1093/bioinformatics/btab35"
REPLACEMENTS = [
    {
        "编号(id)": "K67a",
        "标题(title)": "Rapid Sampling of Hydrogen Bond Networks for Computational Protein Design",
        "DOI(doi)": "10.1021/acs.jctc.8b00033",
        "链接(url)": "https://doi.org/10.1021/acs.jctc.8b00033",
        "年份(year)": "2018",
        "期刊或预印本(venue)": "J Chem Theory Comput",
        "人物组(group)": "通用方法学",
        "文献类型(work_type)": "方法",
        "设计对象(target)": "氢键网络（埋藏 HBnet）的快速采样与界面设计",
        "候选生成方法(backbone_generation)": "Rosetta（HBnet 采样器嵌入设计循环）",
        "计算筛选判据(computational_filters)": "埋藏氢键网络满足度（HBnet）作为可优化/可打分项",
        "PMID/PMCID/arXiv(other_ids)": "PMID=30221938（含 2018 勘误条目）",
        "是否用MD(md_used)": "否", "是否用QM(qm_used)": "否",
        "证据级别(evidence_level)": "本次经 PubMed/Crossref 核对题录",
        "核验状态(doi_verified)": "✅Crossref核验",
        "在方法演进链的位置(role_in_timeline)": "把'氢键'从人工约束变成可采样判据的节点；氢键判据谱系的可靠起点之一",
        "成本/统计量引用(cost_or_stat_note)": "替代被撤销的误引条目",
        "原文出处指针(source_pointer)": "sources/baker.md §五 缺口 4 + 本次 PubMed esearch（Kuhlman AND hydrogen bond networks AND protein design，返回 7 条）",
    },
    {
        "编号(id)": "K67b",
        "标题(title)": "Deep learning based design of buried hydrogen bond networks with HBDesigner",
        "DOI(doi)": "10.64898/2026.06.08.730848",
        "链接(url)": "https://doi.org/10.64898/2026.06.08.730848",
        "年份(year)": "2026",
        "期刊或预印本(venue)": "bioRxiv（预印本）",
        "人物组(group)": "通用方法学",
        "文献类型(work_type)": "预印本",
        "设计对象(target)": "埋藏氢键网络（HBnet）的深度学习设计",
        "候选生成方法(backbone_generation)": "深度学习（HBDesigner）",
        "计算筛选判据(computational_filters)": "未记录（本次仅核对题录）",
        "PMID/PMCID/arXiv(other_ids)": "PMID=42327288",
        "是否用MD(md_used)": "未记录", "是否用QM(qm_used)": "未记录",
        "证据级别(evidence_level)": "题录级（本次经 PubMed/Crossref 核对，未读正文）",
        "核验状态(doi_verified)": "✅Crossref核验",
        "在方法演进链的位置(role_in_timeline)": "氢键判据由物理采样（10.1021/acs.jctc.8b00033）走向可学习模型的当前节点",
        "成本/统计量引用(cost_or_stat_note)": "替代被撤销的误引条目",
        "原文出处指针(source_pointer)": "本次 PubMed esearch 记录（PMID 42327288）+ Crossref 10.64898/2026.06.08.730848",
    },
]

# ---------- D) 本次逐句复核回填 ----------
VERIFIED_PATCH = {
    "10.1126/science.adu2454": {
        "阈值数字(thresholds)": "已复核原句：'Only 1.6% of round 2 designs that passed the AF2 RMSD filter were predicted to be preorganized by PLACER'；'we obtained synthetic genes encoding 129 and 192 designs for rounds 1 and 2'；'We obtained genes encoding 45 two-state filtered designs … and found 38 (84%) labeled with FP-probe'；过渡态几何由 'DFT geometry optimization (B3LYP-D3(BJ)/6-31G(d))' 确定",
        "候选数递减(pipeline_counts)": "round1 129→2 活性(1.6%)；round2 192→10 活性(5.2%)；AF2 过滤后仅 1.6% 过 PLACER 预组织；两态过滤后 45→38(84%)",
        "实验命中率(hit_rate)": "2/129（1.6%）；10/192（5.2%）；末端 38/45（84%）",
        "Kd或活性最好值(best_metric)": "裂解液活性率 3%→17%（两轮之间 5 倍）；活性位点 all-atom RMSD 0.38 Å/22 原子",
        "是否用QM(qm_used)": "是-化学步",
        "成本/统计量引用(cost_or_stat_note)": "同一篇里端到端 1.6%/5.2% 与末端 84% 并列：这就是'90% 类数字'的产生机制",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC12288761）",
    },
    "10.1073/pnas.2427161122": {
        "阈值数字(thresholds)": "已复核原句：'The most general way to evaluate such preorganization is molecular dynamics simulations, but as sidechain reconfiguration can occur on the microsecond time scale, such simulations are computationally expensive and cannot be applied to large numbers of designs'",
        "是否用MD(md_used)": "否-被明确否弃作主筛器",
        "成本/统计量引用(cost_or_stat_note)": "'considerably more expensive MD simulations' 的同篇表述；PLACER 较 GALigandDock 提升对接成功率 7.3%（配体 RMSD<1 Å）；基准 1,112 个非天然构象/65 靶点",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC12625923）",
    },
    "10.1038/s41592-025-02975-x": {
        "阈值数字(thresholds)": "已复核原句：'We obtained 96 designs for each and identified three functional enzymes for the 4MU-butyrate reaction and five for the 4MU-phenylacetate reaction'；'In a second set of 96 designs tested including a general base to activate the water, we identified 11 functional enzymes, the best of which had a k_cat/K_M of 53,000 ± 5,000 M⁻¹s⁻¹'；'RFdiffusion2 samples at least one scaffold passing the success filters for 41/41 cases while RFdiffusion achieves 16/41'",
        "候选数递减(pipeline_counts)": "每批固定 96 个实验名额（预算口径）；首批 3/96 与 5/96 → 加一般碱的第二批 11/96",
        "实验命中率(hit_rate)": "3/96、5/96（首批两种底物）；11/96（第二批）",
        "Kd或活性最好值(best_metric)": "k_cat/K_M = 53,000±5,000（第二批最优）；16,000±2,000（零样本最优）；77±10",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC12791007）",
    },
    "10.1002/pro.4688": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句：'the average rho values throughout the benchmark at 0.26 and 0.28 for ΔΔG and |ΔΔG|'；Rosetta 'averaging at around 0.25'；DMS 之间 'averaging at around 0.66'",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC10273344）",
    },
    "10.1126/science.aan0693": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句（PubMed 摘要）：'Iteration between design and experiment increased the design success rate from 6% to 47%'",
        "证据级别(evidence_level)": "摘要级（本次独立复核）",
    },
    "10.1038/s41467-023-38328-5": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句：'the AF2 filter is computationally expensive (~30 GPU-seconds per design) and only ~2.3% of designs pass'；'increases design success rates nearly 10-fold'",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC10163288）",
    },
    "10.1038/s41586-023-06415-8": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句：'The overall experimental success rate … was 19%'；'fewer than 100 designs tested per target compared to thousands in previous studies'",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC10468394）",
    },
    "10.1038/s41586-022-04654-9": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句：'we designed 15,000–100,000 binders for each of the 13 target sites'",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC9117152）",
    },
    "10.1126/science.abd9909": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句：'All three ACE2-scaffolded designs and 12 of the de novo designs were expressed in Escherichia coli and purified'；'11 of the 12 de novo designs were soluble and bound RBD'",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC7857403）",
    },
    "10.7554/eLife.107785": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句：'with five out of the six (~83%) computationally designed candidate aptamers experimentally confirmed to have improved binding affinities'",
        "证据级别(evidence_level)": "全文级（本次独立复核）",
    },
    "10.1038/s41586-025-09721-5": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句：'success rates against each target, which range from 0% to 2%'",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC12727541）",
    },
    "10.34133/csbj.0070": {
        "成本/统计量引用(cost_or_stat_note)": "已复核原句：'typical experimental hit rates for de novo binders currently range from 1% to 10%, occasionally reaching up to 20% for highly favorable targets, underscoring that computational scores enrich for success rather than guarantee it'",
        "证据级别(evidence_level)": "全文级（本次独立复核 PMC13113996）",
    },
}


def k_tuple_to_row(t, cols):
    if len(t) > 16:
        t = list(t)
        del t[14]
        t = tuple(t)
    (i, title, venue, year, doi, wt, target, filt, stat, md, qm, exp, counts, hit, kd, note) = t
    row = {c: "未记录" for c in cols}
    row.update({
        "编号(id)": "M-" + i, "人物组(group)": "口径对照与独立复核", "标题(title)": title,
        "第一或通讯作者(lead_authors)": "见 sources/claim-90pct.md 或 sources/cost-benchmarks.md 对应条目",
        "期刊或预印本(venue)": venue, "年份(year)": str(year),
        "DOI(doi)": doi or "未记录",
        "链接(url)": ("https://doi.org/" + doi) if doi else "未记录",
        "文献类型(work_type)": wt, "设计对象(target)": target,
        "计算筛选判据(computational_filters)": filt,
        "阈值数字(thresholds)": stat, "是否用MD(md_used)": md, "是否用QM(qm_used)": qm,
        "实验验证手段(experimental_methods)": exp,
        "候选数递减(pipeline_counts)": "未记录" if counts == "—" else counts,
        "实验命中率(hit_rate)": "未记录" if hit == "—" else hit,
        "Kd或活性最好值(best_metric)": "未记录" if kd == "—" else kd,
        "在方法演进链的位置(role_in_timeline)": note,
        "成本/统计量引用(cost_or_stat_note)": stat,
        "证据级别(evidence_level)": "已核验DOI",
        "核验状态(doi_verified)": ("✅Crossref核验" if doi and not doi.startswith("10.5281/")
                              else "✅Zenodo API 核验（原句已逐字比对）" if doi.startswith("10.5281/") else "不适用"),
        "原文出处指针(source_pointer)": "sources/claim-90pct.md [%s]" % i if i in
            ("K27", "K28", "K29", "K30", "K31", "K32", "K33", "K34", "K35", "K36") else "sources/cost-benchmarks.md [%s]" % i,
    })
    return row


def main():
    rows = list(csv.DictReader(io.open(CSVIN, encoding="utf-8-sig")))
    cols = list(rows[0].keys())
    doi_index = {}
    for r in rows:
        d = r["DOI(doi)"].strip().lower()
        if d and d != "未记录":
            doi_index.setdefault(d, r)

    # ---- A) 撤销误引 ----
    n_bad = 0
    keep = []
    for r in rows:
        if r["DOI(doi)"].strip() == BAD_DOI:
            n_bad += 1
            continue
        # 幂等：清掉上一次 finalize 追加的、无 DOI 的 M- 行（价目表类由 build_csv 的 K 行覆盖）
        if r["编号(id)"].startswith("M-") and r["DOI(doi)"].strip() in ("", "未记录"):
            n_bad += 1
            continue
        keep.append(r)
    rows = keep
    for rep in REPLACEMENTS:
        if rep["DOI(doi)"] in doi_index:
            continue
        nr = {c: "未记录" for c in cols}
        nr.update(rep)
        rows.append(nr)

    # ---- D) 复核内容回填 ----
    n_patch = 0
    for r in rows:
        d = r["DOI(doi)"].strip().lower()
        if d in VERIFIED_PATCH:
            for k, v in VERIFIED_PATCH[d].items():
                if k in r:
                    r[k] = v
            n_patch += 1

    # ---- C) 追加口径审计条目（按 DOI 去重）----
    added, merged = 0, 0
    for t in K_TUPLES:
        nr = k_tuple_to_row(t, cols)
        d = nr["DOI(doi)"].strip().lower()
        if not d or d == "未记录":
            continue          # 无 DOI 的条目不重复追加（价目表类已在 build_csv 覆盖）
        if d in doi_index:
                tgt = doi_index[d]
                if "口径对照" not in tgt["人物组(group)"]:
                    tgt["人物组(group)"] += "; 口径对照"
                merged += 1
                continue
        doi_index[d] = nr
        rows.append(nr)
        added += 1

    # ---- B) 官方标题回填 ----
    gate = json.load(io.open(GATE, encoding="utf-8"))
    off = {}
    for x in gate:
        if x.get("crossref_title"):
            off[(x.get("doi") or "").strip().lower()] = re.sub(r"\s+", " ", x["crossref_title"]).strip()
    n_title = 0
    for r in rows:
        d = r["DOI(doi)"].strip().lower()
        t = r["标题(title)"]
        if d in off and t != off[d] and "汇总" not in t and "合并" not in t:
            r["标题(title)"] = off[d]
            n_title += 1

    with io.open(CSVIN, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({c: (r.get(c) or "") for c in cols})

    n_doi = sum(1 for r in rows if re.match(r"^10\.\d{4,9}/", r["DOI(doi)"]))
    print("总行数 %d｜撤销误引 %d 行｜补入替代条目 %d 行｜官方标题回填 %d 行｜复核回填 %d 行｜追加口径审计 %d 行（并入已有 %d 行）｜有 DOI 的行 %d"
          % (len(rows), n_bad, len(REPLACEMENTS), n_title, n_patch, added, merged, n_doi))


if __name__ == "__main__":
    main()
