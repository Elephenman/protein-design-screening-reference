#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成写卡任务的分组清单 data/literature_cards/batches.tsv。

优先级 = 信息价值：Baker → 曹龙兴 → 周如鸿 → 通用方法学 → 口径对照。
每批 3 行（一个代理读 3 篇全文已经很多，再大会开始凭记忆写引句）。
降级行（无本地全文）单独标 DEGRADED，代理只准按底稿写、不许冒充全文级。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "literature_cards"
ORDER = ["Baker", "曹", "周", "通用", "口径"]
BATCH = 3


def rank(group: str) -> int:
    for i, k in enumerate(ORDER):
        if k in group:
            return i
    return len(ORDER)


def main() -> int:
    inv = json.loads((CARDS / "inventory.json").read_text(encoding="utf-8"))
    fetched = {}
    log = CARDS / "fetch_log.tsv"
    if log.exists():
        for ln in log.read_text(encoding="utf-8").splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 7:
                fetched[p[0]] = (p[6], p[7] if len(p) > 7 else "")
    for rec in inv:
        txts = [p for p in rec["local"] if p.endswith("_text.txt") or "/ft/" in p]
        xmls = [p for p in rec["local"] if p.endswith(".xml")]
        # 抓回来的新全文在 fulltext/ 下，按编号前缀补进 local
        for f in sorted((CARDS / "fulltext").glob(f"{rec['id']}_*_text.txt")):
            rel = str(f.relative_to(ROOT)).replace("\\", "/")
            if rel not in txts:
                txts.append(rel)
        rec["txts"] = sorted(set(txts))
        rec["xmls"] = xmls
        rec["has_txt"] = bool(rec["txts"])
        rec["fetch_status"] = fetched.get(rec["id"], ("-", ""))[0]
        rec["fetch_note"] = fetched.get(rec["id"], ("-", ""))[1]
    inv.sort(key=lambda r: (0 if r["has_txt"] else 1, rank(r["group"]), r["id"]))
    with (CARDS / "batches.tsv").open("w", encoding="utf-8", newline="") as fh:
        fh.write("batch\tid\tstate\tgroup\ttitle\tfulltexts\trecords\tfetch_status\tfetch_note\n")
        for i, rec in enumerate(inv):
            b = i // BATCH + 1
            state = "FULLTEXT" if rec["has_txt"] else "DEGRADED"
            fh.write("\t".join([str(b), rec["id"], state, rec["group"], rec["title"][:70].replace("\t", " "),
                                ";".join(rec["txts"]) or "-", ";".join(rec.get("records", [])) or "-",
                                rec["fetch_status"], (rec["fetch_note"] or "").replace("\t", " ")[:80]]) + "\n")
    nf = sum(1 for r in inv if r["has_txt"])
    print(f"152 行分 {(len(inv) + BATCH - 1)//BATCH} 批，每批 {BATCH} 行")
    print(f"判定标准: 全文 = fulltext/ 或 interim 缓存里按文件头身份块认领到的 _text.txt|/ft/ 文件")
    print(f"判定结果: FULLTEXT {nf} 行 · DEGRADED {len(inv)-nf} 行 · 清单 data/literature_cards/batches.tsv")
    print("找出来没有: 本步骤只分组，不判定论文内容")
    return 0


if __name__ == "__main__":
    main()
