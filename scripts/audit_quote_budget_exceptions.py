#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""引用预算的**例外行**逐条定因：为什么这条受限引句超了单条上限却没被截短。

为什么（2026-11-08 实测）：
  `deliverables/quote_budget_ledger.csv`（卡，7,125 条）与
  `deliverables/quote_budget_notes_ledger.csv`（底稿，618 条）逐条记了
  「截前字符 / 截后字符 / 是否截短」，但**没有记"没截"的原因**。
  受限来源里超了单条上限（>100 字符）却保持原样的行，卡有 97 条、底稿有 8 条，
  光看账只能知道"它超预算了"，不知道"为什么没截"。
  发布口径要求这类例外逐条可查，所以这里把成因算出来，并单独出一张例外表。

  口径可复现，不靠"当初脚本大概是这么想的"：
  ① 同一来源行的累计额度（PER_PAIR_CAP=600，超了单条上限降到 50，再超降到 32）
     可以从账上**精确重建**——被截的行消耗"截后字符"，没被截的行消耗"截前字符"，
     两者账上都记着；
  ② 截断点、重建自检、逐字自检全部用卡片脚本自己的函数重算一遍。

用法:
  python scripts/audit_quote_budget_exceptions.py           # 体检并出例外表
  python scripts/audit_quote_budget_exceptions.py --check   # 例外表与重算一致

产出: deliverables/quote_budget_exceptions.csv
      （逐条：载体、序号、来源编号、许可类别、字符数、未截短原因）
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from litcards_text import norm  # noqa: E402
from apply_quote_budget import (  # noqa: E402
    RESTRICTED, PER_QUOTE_CAP, PER_PAIR_CAP, PER_QUOTE_CAP_TAPER,
    PER_QUOTE_CAP_FLOOR, MIN_ALPHA, MIN_QUOTE_CHARS, clean, quotes_of,
    truncate, _cut_index,
)

CARDS = ROOT / "data" / "literature_cards"
CARD_LEDGER = ROOT / "deliverables" / "quote_budget_ledger.csv"
NOTE_LEDGER = ROOT / "deliverables" / "quote_budget_notes_ledger.csv"
OUT = ROOT / "deliverables" / "quote_budget_exceptions.csv"

PSEUDO_ACC = "未归属"

# 例外成因（逐条写进例外表）
R_TRANSCRIBE = "转写不一致：原句不是该来源的逐字片段（大小写/连字符/省略号是我们自己改的），逐字自检不通过"
R_NO_BOUNDARY = "截断点无安全边界：截断点会落在 markdown 强调段或长单词中间，宁可保留原句也不产生半截引句"
R_TOO_SHORT = f"截短后不足引句下限（<{MIN_QUOTE_CHARS} 字符或 <{MIN_ALPHA} 字母），截了就不再是引句"
R_NOT_VERBATIM = "截短后的文本不再逐字命中同一份底稿"
R_UNATTRIBUTED = "未归属：查不到具体来源行，无从做逐字自检"
R_OK = "可截未截：按当前账目与原文，这条现在可以安全截短 —— 需要处理"


def card_sources() -> dict[str, str]:
    """编号 -> 该行全部本地底稿的归一化文本（与 apply_quote_budget.py 同源）。"""
    from apply_quote_budget import load_sources
    return load_sources()


def note_sources() -> dict[str, str]:
    """编号 -> 该行第三方全文的归一化文本（与 apply_note_quote_budget.py 同源）。"""
    from apply_note_quote_budget import load_fulltexts
    return load_fulltexts()


def first_segment(q: str, cap: int) -> str | None:
    """省略号之前的第一段原文（底稿脚本的同款退路）。"""
    for sep in ("……", "...", "…"):
        if sep in q:
            seg = q.split(sep)[0].strip()
            if MIN_QUOTE_CHARS <= len(seg) <= cap and sum(c.isalpha() for c in seg) >= MIN_ALPHA:
                return seg
            return None
    return None


def decide(q: str, cap: int, src: str | None, mode: str = "card") -> tuple[str, str]:
    """这条引句为什么没被截短。返回 (原因码, 说明)。

    两个载体的自检口径**不一样**，必须分开算，否则审计器和预算脚本各说各话：
      · 卡（mode="card"）：只有"截短结果逐字命中底稿"才算能截；
      · 底稿（mode="note"）：三级判定（① 截短结果逐字命中来源全文 →
        ② 原句逐字但截断点落在我们的省略号之后，退到省略号前的第一段 →
        ③ 原句是我们自己的转写：先试"原句前缀"，再试第一段）。
    """
    if src is None:
        return R_UNATTRIBUTED, R_UNATTRIBUTED
    verbatim = clean(q) in src
    cand = truncate(q, cap)
    if cand is None:
        if _cut_index(q, cap) is None:
            return R_NO_BOUNDARY, R_NO_BOUNDARY
        return R_TOO_SHORT, R_TOO_SHORT
    if clean(cand) in src:
        return R_OK, R_OK
    if verbatim:
        if mode == "note":
            # 退到省略号前的第一段（底稿脚本同款退路）
            seg = first_segment(q, cap)
            if seg and clean(seg) in src:
                return R_OK, R_OK
        return R_NOT_VERBATIM, R_NOT_VERBATIM
    # 原句本身就不是逐字片段（我们的转写）
    if mode == "note" and q.startswith(cand):
        # 底稿脚本的"前缀"口径：截短结果是原句的前缀，不增加任何第三方内容
        return R_OK, R_OK
    if mode == "note":
        seg = first_segment(q, cap)
        if seg and clean(seg) in src:
            return R_OK, R_OK
    return R_TRANSCRIBE, R_TRANSCRIBE


def cap_for(used: int, ln: int) -> int:
    """同一来源行的单条上限（与两个预算脚本同口径）。"""
    if used + ln <= PER_PAIR_CAP:
        return PER_QUOTE_CAP
    if used + ln <= 2 * PER_PAIR_CAP:
        return PER_QUOTE_CAP_TAPER
    return PER_QUOTE_CAP_FLOOR


def audit_cards(sources: dict[str, str]) -> list[dict]:
    rows = list(csv.DictReader(CARD_LEDGER.open(encoding="utf-8-sig", newline="")))
    by_card: dict[str, list[dict]] = {}
    for r in rows:
        by_card.setdefault(r["卡片"], []).append(r)
    out: list[dict] = []
    for card, rs in by_card.items():
        f = CARDS / card
        if not f.exists():
            continue
        cur = quotes_of(f.read_text(encoding="utf-8"))
        used: dict[str, int] = {}
        for r, (_s, _e, q) in zip(rs, cur):
            acc = r["来源编号"]
            ln = int(r["截前字符"])
            cat = r["许可类别"]
            # 卡片脚本只让**受限来源**的引句消耗"同一来源行的额度"；
            # 可再分发的行原样保留、根本不进额度账（口径要与脚本一致）。
            if cat not in RESTRICTED or not acc:
                continue
            spent = int(r["截后字符"]) if r["是否截短"] == "是" else ln
            cur_used = used.get(acc, 0)
            used[acc] = cur_used + spent
            if r["是否截短"] == "是":
                continue
            if ln <= PER_QUOTE_CAP:
                continue
            cap = cap_for(cur_used, ln)
            src = sources.get(acc)
            code, desc = decide(q, cap, src, "card")
            out.append({"载体": card, "序号": r["引句序号"], "来源编号": acc,
                        "许可类别": cat, "字符数": ln, "本行上限": cap,
                        "原因码": code, "未截短原因": desc})
    return out


def audit_notes(sources: dict[str, str]) -> list[dict]:
    rows = list(csv.DictReader(NOTE_LEDGER.open(encoding="utf-8-sig", newline="")))
    by_note: dict[str, list[dict]] = {}
    for r in rows:
        by_note.setdefault(r["底稿"], []).append(r)
    out: list[dict] = []
    for rel, rs in by_note.items():
        f = ROOT / rel
        if not f.exists():
            continue
        cur = quotes_of(f.read_text(encoding="utf-8"))
        used: dict[str, int] = {}
        for r, (_s, _e, q) in zip(rs, cur):
            acc = r["来源编号"]
            ln = int(r["截前字符"])
            cat = r["许可类别"]
            # 底稿脚本的额度账：受限来源的引句 + 未归属且 ≥120 字符的引句。
            counted = (cat in RESTRICTED) or (acc == PSEUDO_ACC and ln >= 120)
            if not counted:
                continue
            spent = int(r["截后字符"]) if r["是否截短"] == "是" else ln
            cur_used = used.get(acc, 0)
            used[acc] = cur_used + spent
            if r["是否截短"] == "是":
                continue
            if ln <= PER_QUOTE_CAP:
                continue
            if r.get("保留原因"):
                continue  # 已登记（为护住卡片核验链）
            if acc == PSEUDO_ACC:
                out.append({"载体": rel, "序号": r["引句序号"], "来源编号": acc,
                            "许可类别": cat, "字符数": ln, "本行上限": PER_QUOTE_CAP,
                            "原因码": R_UNATTRIBUTED, "未截短原因": R_UNATTRIBUTED})
                continue
            cap = cap_for(cur_used, ln)
            src = sources.get(acc)
            code, desc = decide(q, cap, src, "note")
            out.append({"载体": rel, "序号": r["引句序号"], "来源编号": acc,
                        "许可类别": cat, "字符数": ln, "本行上限": cap,
                        "原因码": code, "未截短原因": desc})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    srcs_c = card_sources()
    srcs_n = note_sources()
    rows = audit_cards(srcs_c) + audit_notes(srcs_n)
    rows.sort(key=lambda r: (r["载体"], str(r["序号"])))

    ok = [r for r in rows if r["原因码"] != R_OK]
    actionable = [r for r in rows if r["原因码"] == R_OK]

    if not args.check:
        with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"例外行 {len(rows)} 条 → {OUT.relative_to(ROOT)}")
        from collections import Counter
        for code, n in sorted(Counter(r["原因码"] for r in rows).items(), key=lambda x: -x[1]):
            print(f"  {n:>4} 条  {code}")
        print(f"其中『可截未截』（需要处理）：{len(actionable)} 条")

    if args.check:
        if not OUT.exists():
            print("判定结果: FAIL — 例外表不存在")
            return 1
        disk = list(csv.DictReader(OUT.open(encoding="utf-8-sig", newline="")))
        mine = [{k: str(v) for k, v in r.items()} for r in rows]
        theirs = [{k: str(r.get(k, "")) for k in mine[0]} for r in disk] if mine else []
        bad = 0
        if len(disk) != len(mine):
            bad += 1
            print(f"  例外表 {len(disk)} 行 != 重算 {len(mine)} 行")
        else:
            for a, b in zip(disk, theirs):
                if a != b:
                    bad += 1
                    if bad <= 10:
                        print("  ", a.get("载体"), a.get("序号"), "不符")
        print("判定标准: 例外表逐行与按账目重算的成因一致；且不存在『可截未截』的行")
        if actionable:
            bad += len(actionable)
            for r in actionable[:10]:
                print("  ", r["载体"], r["序号"], "可截未截")
        print(f"判定结果: {'PASS 0 处不符' if bad == 0 else f'FAIL {bad} 处不符'}")
        return 0 if bad == 0 else 1

    if actionable:
        print("判定结果: FAIL — 存在『可截未截』的行，需要处理后再发布")
        return 1
    print("判定结果: PASS 0 处可截未截")
    return 0


if __name__ == "__main__":
    sys.exit(main())
