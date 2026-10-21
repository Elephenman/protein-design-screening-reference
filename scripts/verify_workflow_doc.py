#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工作流文档的溯源体检：文档里每个 [编号] 必须能在证据台账里找到，每个相对链接必须可达。

用法: python scripts/verify_workflow_doc.py [--doc deliverables/protein_design_workflow.md]
判据: 三条都过才算 PASS——(1) 引用编号 100% 命中台账；(2) 相对链接 0 断链；
      (3) 文档引用的台账/脚本文件真实存在。内容对错不在本门范围（那是各卡 §7 与 report.md 的事）。
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID_PAT = re.compile(r"\[([A-Za-z]+-?\d+[a-z]?(?:;\s?C\d+)?)\]")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", default="deliverables/protein_design_workflow.md")
    args = ap.parse_args()
    docp = ROOT / args.doc
    doc = docp.read_text(encoding="utf-8")

    ledger = ROOT / "deliverables" / "protein_design_workflow_evidence.csv"
    if not ledger.exists():
        print("判定结果: FAIL — 证据台账不存在，先跑 scripts/build_workflow_evidence.py")
        return 1
    ids = {r["编号"] for r in csv.DictReader(ledger.open(encoding="utf-8-sig"))}

    refs = sorted(set(ID_PAT.findall(doc)))
    unknown = [x for x in refs if x not in ids]

    base = docp.parent
    broken = []
    for m in re.findall(r"\]\(([^)\s]+)\)", doc):
        if m.startswith(("http", "#", "mailto")):
            continue
        target = (base / m.split("#")[0]).resolve()
        if not target.exists():
            broken.append(m)

    named = sorted(set(re.findall(r"`?(scripts/[A-Za-z0-9_\-\.]+\.py)`?", doc)))
    missing_scripts = [s for s in named if not (ROOT / s).exists()]

    errs = []
    if unknown:
        errs.append(f"引用编号不在台账: {unknown}")
    if broken:
        errs.append(f"文档内断链: {broken}")
    if missing_scripts:
        errs.append(f"文档提到的脚本不存在: {missing_scripts}")

    print(f"文档: {args.doc} | 引用编号 {len(refs)} 个（去重）| 台账行数 {len(ids)}")
    print("判定标准: 引用编号全部命中台账 + 相对链接零断链 + 提到的脚本都在盘上")
    if errs:
        print("判定结果: FAIL（退出码 1）")
        for e in errs:
            print("  -", e)
        return 1
    print("判定结果: PASS（退出码 0）")
    print("找出来没有: 本体检只判\"引得到、点得开\"，不判文档结论对不对（看各卡 §7 与 report.md §八 缺口清单）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
