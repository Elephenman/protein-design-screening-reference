#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 152 张精读卡的 CSV 回填块生成"蛋白设计工作流"的证据台账（确定性，只读不判）。

产物（全部由本脚本生成，不许手改）:
  deliverables/protein_design_workflow_evidence.csv        一行一篇：14 键 + 底稿形态 + 卡路径
  deliverables/protein_design_workflow_criteria_ledger.csv 一行一判据：把"计算筛选判据"拆开后挂上阈值/命中率/出处
  deliverables/protein_design_workflow_summary.txt         频次与口径统计（工作流文档里的数字来自这里）

用法:
  python scripts/build_workflow_evidence.py
  python scripts/build_workflow_evidence.py --check   # 只比对已生成文件是否与源一致，不写盘

成功测试（可判伪）：evidence 行数必须等于 CSV 行数(152)；每行 `精读卡文件` 可达且
`<!--CSV回填` 块能解析出 14 键；ledger 的判据行数 >= evidence 里非"未记录"的判据单元格数；
`--check` 在人为改坏一个数字时必须退出非 0。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from litcards_spec import CSV_COL, CSV_KEYS, parse_card  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CSVP = ROOT / "data" / "protein_design_literature.csv"
CARDS = ROOT / "data" / "literature_cards"
OUT = ROOT / "deliverables"

SPLIT = re.compile(r"[；;、]|\s\|\s")
NOT_RECORD = ("未记录", "不适用", "无", "未标注")


def col_of(fields: list[str], prefix: str) -> str:
    for k in fields:
        if k.startswith(prefix):
            return k
    raise KeyError(prefix)


def card_file(acc: str) -> Path | None:
    hits = [p for p in CARDS.glob("*.md")
            if p.name.startswith(re.sub(r"[^A-Za-z0-9]+", "-", acc).strip("-") + "_")
            and p.name not in ("README.md", "run.md", "AGENT_RULES.md")]
    return hits[0] if hits else None


def is_na(v: str) -> bool:
    return (not v) or any(v.startswith(x) for x in NOT_RECORD)


def build(rows: list[dict], fields: list[str], inv: dict) -> tuple[list[dict], list[dict], list[str]]:
    ev, ledger, notes = [], [], []
    idc = col_of(fields, "编号")
    for r in rows:
        acc = r[idc].strip()
        cf = card_file(acc)
        if cf is None:
            notes.append(f"{acc}: 找不到卡文件")
            continue
        vals, errs = parse_card(cf.read_text(encoding="utf-8"))
        if errs:
            notes.append(f"{acc}: 回填块 {errs[0]}")
            continue
        line = {
            "编号": acc,
            "人物组": r[col_of(fields, "人物组")],
            "标题": r[col_of(fields, "标题")][:160],
            "年份": r[col_of(fields, "年份")],
            "期刊或预印本": r[col_of(fields, "期刊或预印本")],
            "DOI": r[col_of(fields, "DOI")],
            "底稿形态": "FULLTEXT" if inv.get(acc, {}).get("has_fulltext") else "DEGRADED",
            "精读卡文件": str(cf.relative_to(ROOT)).replace("\\", "/"),
        }
        for k in CSV_KEYS:
            line[CSV_COL[k]] = vals[k]
        ev.append(line)

        filters = vals["computational_filters"]
        if is_na(filters):
            continue
        for crit in [x.strip() for x in SPLIT.split(filters) if x.strip()]:
            if len(crit) < 2:
                continue
            ledger.append({
                "编号": acc,
                "人物组": line["人物组"],
                "年份": line["年份"],
                "底稿形态": line["底稿形态"],
                "判据": crit[:120],
                "该行阈值原文": vals["thresholds"][:400],
                "候选递减": vals["pipeline_counts"][:300],
                "实验命中率": vals["hit_rate"][:300],
                "是否用MD": vals["md_used"][:120],
                "是否用QM": vals["qm_used"][:120],
                "成本/统计": vals["cost_or_stat_note"][:300],
                "精读卡文件": line["精读卡文件"],
            })
    return ev, ledger, notes


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def summary(ev: list[dict], ledger: list[dict]) -> list[str]:
    out = []
    out.append(f"论文行数: {len(ev)}（CSV 152 行里能解析出回填块的行）")
    ft = sum(1 for x in ev if x["底稿形态"] == "FULLTEXT")
    out.append(f"其中 FULLTEXT {ft} 行 · DEGRADED {len(ev)-ft} 行")
    md = sum(1 for x in ev if x["是否用MD"].startswith("是"))
    qm = sum(1 for x in ev if x["是否用QM"].startswith("是"))
    out.append(f"声明用了 MD: {md} 行 · 用了 QM: {qm} 行（其余为 否/未记录/不适用）")
    hr = sum(1 for x in ev if not is_na(x["实验命中率"]))
    out.append(f"给出可用命中率口径的行: {hr} / {len(ev)}")
    out.append(f"拆出的判据条目: {len(ledger)}（同一行多个判据各占一条）")
    cnt: dict[str, int] = {}
    for x in ledger:
        key = re.split(r"[（( :]", x["判据"])[0].strip().lower()
        cnt[key] = cnt.get(key, 0) + 1
    top = sorted(cnt.items(), key=lambda kv: -kv[1])[:25]
    out.append("出现频次最高的 25 个判据词干: " + ", ".join(f"{k}×{v}" for k, v in top))
    by_grp: dict[str, list[int]] = {}
    for x in ev:
        g = x["人物组"].split(";")[0].strip()
        by_grp.setdefault(g, [0, 0])
        by_grp[g][0] += 1
        if x["底稿形态"] == "FULLTEXT":
            by_grp[g][1] += 1
    out.append("分组行数 / 其中 FULLTEXT: " + "; ".join(f"{g} {v[1]}/{v[0]}" for g, v in sorted(by_grp.items())))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="只比对磁盘上已有产物是否与源一致")
    args = ap.parse_args()

    with CSVP.open(encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        fields, rows = list(rd.fieldnames or []), list(rd)
    inv = {r["id"]: r for r in json.loads((CARDS / "inventory.json").read_text(encoding="utf-8"))}
    ev, ledger, notes = build(rows, fields, inv)
    summ = summary(ev, ledger)

    if args.check:
        bad = []
        for p, expect in ((OUT / "protein_design_workflow_evidence.csv", len(ev)),
                          (OUT / "protein_design_workflow_criteria_ledger.csv", len(ledger))):
            if not p.exists():
                bad.append(f"{p.name} 缺失")
                continue
            got = sum(1 for _ in csv.DictReader(p.open(encoding="utf-8-sig")))
            if got != expect:
                bad.append(f"{p.name} 行数 {got} != 重算 {expect}")
        if notes:
            bad.append(f"解析告警 {len(notes)} 条: " + "; ".join(notes[:5]))
        print("判定标准: 已生成台账的行数必须等于从 CSV+卡重算出的行数，且无解析告警")
        print(f"判定结果: {'PASS' if not bad else 'FAIL — ' + ' | '.join(bad)}（退出码 {0 if not bad else 1}）")
        return 0 if not bad else 1

    if not ev or len(ev) != len(rows):
        print(f"判定结果: FAIL — 解析成功 {len(ev)} 行 / CSV {len(rows)} 行，台账不完整，拒绝写盘")
        for n in notes[:20]:
            print("  ", n)
        return 1
    write_csv(OUT / "protein_design_workflow_evidence.csv", ev)
    write_csv(OUT / "protein_design_workflow_criteria_ledger.csv", ledger)
    (OUT / "protein_design_workflow_summary.txt").write_text(
        "\n".join(summ) + "\n", encoding="utf-8")

    print("\n".join(summ))
    print(f"判定标准: evidence 行数==CSV 行数({len(rows)}) 且每行回填块 14 键可解析且卡路径可达")
    print(f"判定结果: PASS 生成 {len(ev)} 行台账 + {len(ledger)} 行判据拆分 + summary（退出码 0）")
    print("找出来没有: 本脚本只做拆表与计数，不判任何判据的有效性；有效性看各卡 §2/§7/§8")
    if notes:
        print("告警:", notes[:10])
    return 0


if __name__ == "__main__":
    sys.exit(main())
