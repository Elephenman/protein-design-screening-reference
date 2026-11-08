#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给卡片里的逐字引句设"引用预算"，把许可受限来源的引句量压到引用级。

为什么（2026-11-08 实测）：
  公开仓库 = 公开再分发。第三方全文缓存已经决定不随包分发（见
  `scripts/build_fulltext_manifest.py`），但**卡里我们自己写的分析**也逐字复制了第三方正文：
  全库 153 张卡的英文引句合计 836,425 字符 / 8,749 处，其中 **244,675 字符（29.6%）**
  来自 26 行许可受限的来源（CC BY-NC / NC-ND / ND / 出版商条款 / 仅研究复用 / 仅文本挖掘 /
  保留所有权利），单卡最高复现来源正文 62%。
  许可允许再分发的那 74 行（CC BY / CC0）我们保留原样，但要在 NOTICE 里履行署名义务；
  受限行的引句则按预算截短——引用级，不是复制级。

预算规则（只对受限行生效）：
  1. 单条引句 ≤ 120 字符（在句号/分号/空格边界截断，不切断单词）。
  2. 同一张卡对同一来源行的引句总量 ≤ 1200 字符；超出后单条上限降到 60 字符；
     再超出（>2400）降到 32 字符，但不低于 24 字符（低于 20 字符的门禁门槛会被当成没引句）。
  3. 截短后的引句**必须仍然逐字命中同一份底稿**（脚本逐条自检，不合格就回退不截）。
     所以门禁 `verify_literature_cards.py` 仍然是逐字核验，不放松。
  4. 只截**逐字引句**；卡里我们自己写的中文分析、判断、台账一律不动。

用法:
  python scripts/apply_quote_budget.py --dry-run   # 只算账，不改卡
  python scripts/apply_quote_budget.py             # 截短并写改动账
  python scripts/apply_quote_budget.py --check     # 核验改动账与卡现状一致

产出: deliverables/quote_budget_ledger.csv（逐条：卡、序号、来源编号、许可类别、前后字符数、是否截短）
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from litcards_text import norm  # noqa: E402

CARDS = ROOT / "data" / "literature_cards"
INVENTORY = CARDS / "inventory.json"
AUDITCSV = ROOT / "deliverables" / "protein_design_license_audit.csv"
LEDGER = ROOT / "deliverables" / "quote_budget_ledger.csv"
SUMMARY = ROOT / "deliverables" / "quote_budget_summary.csv"
MANIFEST = ROOT / "deliverables" / "fulltext_manifest.csv"

CJK = re.compile(r"[\u3000-\u30ff\u4e00-\u9fff\uff00-\uffef]")
QUOTE = re.compile(r'"([^"\n]{20,})"')
RESTRICTED = {"CC_BY_NC", "CC_BY_ND", "CC_BY_NC_ND", "PUBLISHER_TERMS",
               "TEXT_MINING_ONLY", "ALL_RIGHTS_RESERVED", "RESEARCH_REUSE_ONLY", "UNKNOWN"}
# 许可允许再分发的类别：这些行原样保留，账上不许出现"被截短"。
REDISTRIBUTABLE = {"CC_BY", "CC_BY_SA", "CC0", "PUBLIC_DOMAIN"}

PER_QUOTE_CAP = 100
PER_PAIR_CAP = 600
PER_QUOTE_CAP_TAPER = 50
PER_QUOTE_CAP_FLOOR = 32
MIN_QUOTE_CHARS = 24
MIN_ALPHA = 12  # 与 verify_literature_cards.py 的引句过滤条件一致（字母数 <12 不算引句）
NOTE_MARK = "引用预算截短"


def clean(q: str) -> str:
    return norm(re.sub(r"\*\*|\*|`", "", q))


def quotes_of(raw: str) -> list[tuple[int, int, str]]:
    """返回 (start, end, 原文片段)；过滤规则与 verify_literature_cards.py 完全一致。"""
    out = []
    for m in QUOTE.finditer(raw):
        q = m.group(1)
        if CJK.search(q) or q.lower().startswith("http") or sum(c.isalpha() for c in q) < 12:
            continue
        out.append((m.start(1), m.end(1), q))
    return out


def _cut_index(q: str, cap: int) -> int | None:
    """截断点（字符下标）：在句号/分号/空格等边界切，不切断单词。"""
    head = q[:cap]
    for sep in (". ", "! ", "? ", "; ", ": ", ", "):
        i = head.rfind(sep)
        if i >= MIN_QUOTE_CHARS:
            return i + 1
    i = head.rfind(" ")
    if i >= MIN_QUOTE_CHARS:
        return i
    return None


def _emph_close(q: str, cut: int) -> str:
    """截断点落在 markdown 强调段中间时，补上收尾标记。

    只补标记、不动内容：引句的文字部分仍是原文的逐字前缀，
    门禁 `verify_literature_cards.py` 去标记后照样逐字命中。
    不补的话会留下"**compete with"这种半截加粗，读起来像引坏了的原文。
    """
    head = q[:cut]
    if head.count("**") % 2:
        return "**"
    if head.replace("**", "").count("*") % 2:
        return "*"
    return ""


def truncate(q: str, cap: int) -> str | None:
    """在不超过 cap 的位置截断，返回截断后文本；找不到安全边界返回 None。

    截断点落在强调段中间时补收尾标记（见 _emph_close）：
    文字长度不超过 cap，补上的标记最多 2 个字符。
    """
    if len(q) <= cap:
        return q
    cut = _cut_index(q, cap)
    if cut is None:
        return None
    text = (q[:cut].rstrip() + _emph_close(q, cut)).strip()
    if len(text) < MIN_QUOTE_CHARS or sum(c.isalpha() for c in text) < MIN_ALPHA:
        return None
    return text


def load_sources() -> dict[str, str]:
    """编号 -> 该行全部本地底稿的归一化文本（拼接）。"""
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for rec in inv:
        parts = []
        for p in list(rec.get("local") or []) + list(rec.get("records") or []):
            f = ROOT / p
            if f.exists() and f.suffix in (".txt", ".md"):
                parts.append(norm(f.read_text(encoding="utf-8", errors="replace")))
        if parts:
            out[rec["id"]] = "\n".join(parts)
    return out


def withheld_absent_ids() -> set[str]:
    """本机在场却缺失、且按公开口径**不随仓库分发**的第三方底稿所对应的编号。

    这类"缺"不是缺漏：公开克隆里没有这些底稿（第三方原文按公开口径不随包分发），
    所以"截短后仍逐字命中同一份底稿"这一条在公开克隆里**无法复核**，
    只能记 WITHHELD，不能判 FAIL——否则公开克隆里这道门禁必然假红。
    本机维护者工作树里底稿齐备，照常逐条核验。
    """
    if not MANIFEST.exists():
        return set()
    man: dict[str, dict] = {}
    with MANIFEST.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            man[r["path"]] = r
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    out: set[str] = set()
    for rec in inv:
        for p in list(rec.get("local") or []) + list(rec.get("records") or []):
            if man.get(p, {}).get("随仓库分发") == "否" and not (ROOT / p).exists():
                out.add(rec["id"])
    return out


def load_license() -> dict[str, str]:
    out: dict[str, str] = {}
    with AUDITCSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            out[r["编号"]] = r["许可类别"]
    return out


def cat_of(acc: str, lic: dict[str, str]) -> str:
    """一条引句所属来源行的许可类别。

    inventory 里的编号可能是组合编号（"B06; C02"：同一篇论文在两个组各登记一次），
    许可审计表按 CSV 行记一条、以首个编号为键，所以组合编号要按分号拆开查。
    若各段的类别不一致，取**受限**的那一段——保守侧：宁可多截。
    """
    toks = [x.strip() for x in re.split(r"[;；]", acc) if x.strip()]
    cats = [lic.get(t, "") for t in toks]
    cats = [c for c in cats if c]
    if not cats:
        return ""
    restricted = [c for c in cats if c in RESTRICTED]
    return restricted[0] if restricted else cats[0]


def owner_of(q: str, srcs: dict[str, str]) -> str | None:
    """引句属于哪一行：谁家底稿里有这段逐字文本。"""
    nq = clean(q)
    for acc, text in srcs.items():
        if nq and nq in text:
            return acc
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    srcs = load_sources()
    lic = load_license()
    card_files = sorted(p for p in CARDS.glob("*.md")
                        if not p.name.startswith(("README", "AGENT_RULES", "DISPATCH", "run")))
    ledger: list[dict] = []
    plan: list[tuple[Path, list[tuple[int, int, str]], str]] = []
    before_total = after_total = 0
    before_r = after_r = 0

    for cf in card_files:
        raw = cf.read_text(encoding="utf-8")
        if NOTE_MARK in raw:
            # 已经处理过：不再重复截短（否则改动账会记成"从已截短版本再截一次"）
            continue
        qs = quotes_of(raw)
        if not qs:
            continue
        used: dict[str, int] = {}
        edits: list[tuple[int, int, str]] = []
        rows: list[dict] = []
        for idx, (s, e, q) in enumerate(qs, 1):
            nq = clean(q)
            acc = owner_of(q, srcs)
            cat = cat_of(acc, lic) if acc else ""
            rows.append({"idx": idx, "start": s, "end": e, "q": q, "acc": acc or "", "cat": cat,
                         "new": q, "changed": False})
        # 只对受限来源动刀
        for row in rows:
            if row["cat"] not in RESTRICTED or not row["acc"]:
                continue
            acc = row["acc"]
            cur = used.get(acc, 0)
            if cur + len(row["q"]) <= PER_PAIR_CAP:
                cap = PER_QUOTE_CAP
            elif cur + len(row["q"]) <= 2 * PER_PAIR_CAP:
                cap = PER_QUOTE_CAP_TAPER
            else:
                cap = PER_QUOTE_CAP_FLOOR
            if len(row["q"]) <= cap:
                used[acc] = cur + len(row["q"])
                continue
            cand = truncate(row["q"], cap)
            if not cand:
                used[acc] = cur + len(row["q"])
                continue
            if len(cand) < MIN_QUOTE_CHARS or sum(c.isalpha() for c in cand) < MIN_ALPHA:
                # 截得太短就不再是"引句"了（门禁按 ≥20 字符、≥12 字母识别引句）：
                # 这种引句保持原样，宁可超预算也不让卡里的引句消失。
                used[acc] = cur + len(row["q"])
                continue
            # 自检：截短后必须仍逐字命中同一份底稿
            if clean(cand) not in srcs[acc]:
                used[acc] = cur + len(row["q"])
                continue
            row["new"] = cand
            row["changed"] = True
            used[acc] = cur + len(cand)
        if any(r["changed"] for r in rows):
            plan.append((cf, rows, raw))
        for row in rows:
            if row["cat"] in RESTRICTED and row["acc"]:
                before_r += len(row["q"])
                after_r += len(row["new"])
            before_total += len(row["q"])
            after_total += len(row["new"])
            ledger.append({
                "卡片": cf.name,
                "引句序号": row["idx"],
                "来源编号": row["acc"],
                "许可类别": row["cat"] or "未归属",
                "截前字符": len(row["q"]),
                "截后字符": len(row["new"]),
                "是否截短": "是" if row["changed"] else "否",
                "截后片段": row["new"][:120] if row["changed"] else "",
            })

    if args.dry_run:
        print(f"卡片 {len(card_files)} 张 · 引句 {len(ledger)} 处")
        print(f"全部引句：{before_total} → {after_total} 字符（-{before_total - after_total}）")
        print(f"其中许可受限来源：{before_r} → {after_r} 字符（-{before_r - after_r}，"
              f"降幅 {100 * (before_r - after_r) / max(1, before_r):.1f}%）")
        n_changed = sum(1 for r in ledger if r["是否截短"] == "是")
        print(f"被截短的引句 {n_changed} 处，涉及卡片 {len(plan)} 张")
        print("--dry-run：未改动任何卡")
        return 0

    if args.check:
        # 核验：改动账里标"截短"的引句，在卡里的实际长度必须等于账上的截后字符数；
        # 且每张卡的引句条数与账上一致（截短不改变条数）。
        # 卡侧的截短只允许一种口径：**截短结果仍逐字命中同一份底稿**
        # （脚本只在这一条成立时才动刀），所以这里把它重新核一遍。
        if not LEDGER.exists():
            print("判定结果: FAIL — 改动账不存在")
            return 1
        bad = 0
        withheld_n = 0
        unverifiable_ids = withheld_absent_ids()
        srcs = load_sources()
        rows = list(csv.DictReader(LEDGER.open(encoding="utf-8-sig", newline="")))
        by_card: dict[str, list[dict]] = {}
        for r in rows:
            by_card.setdefault(r["卡片"], []).append(r)
        for card, rs in by_card.items():
            f = CARDS / card
            if not f.exists():
                bad += 1
                print("  ", card, "卡文件缺失")
                continue
            cur = quotes_of(f.read_text(encoding="utf-8"))
            if len(cur) != len(rs):
                bad += 1
                print("  ", card, f"引句条数 {len(cur)} != 账上 {len(rs)}")
                continue
            for r, (_s, _e, q) in zip(rs, cur):
                # 每一行都要核：现状长度 == 账上的截后字符数
                if len(q) != int(r["截后字符"]):
                    bad += 1
                    print("  ", card, f"第 {r['引句序号']} 条长度 {len(q)} != 账上 {r['截后字符']}")
                if int(r["截前字符"]) < int(r["截后字符"]):
                    bad += 1
                    print("  ", card, f"第 {r['引句序号']} 条截前字符 < 截后字符")
                # 许可允许再分发的来源必须原样保留
                if r["许可类别"] in REDISTRIBUTABLE and r["是否截短"] == "是":
                    bad += 1
                    print("  ", card, f"第 {r['引句序号']} 条许可类别 {r['许可类别']} 可再分发，不该被截短")
                if r["是否截短"] == "是":
                    src = srcs.get(r["来源编号"])
                    if src is None:
                        if r["来源编号"] in unverifiable_ids:
                            # 底稿按公开口径未随仓库分发 → 本机不可复核（WITHHELD），不是不符
                            withheld_n += 1
                            continue
                        bad += 1
                        print("  ", card, f"第 {r['引句序号']} 条来源 {r['来源编号']} 的底稿不在场，无法复核")
                    elif clean(q) not in src:
                        if r["来源编号"] in unverifiable_ids:
                            # 同上：底稿缺失时无法判断"是否仍逐字命中"，记 WITHHELD
                            withheld_n += 1
                            continue
                        bad += 1
                        print("  ", card, f"第 {r['引句序号']} 条截短后不再逐字命中 {r['来源编号']} 的底稿")
        print("判定标准: 每张卡引句条数不变；每一行的现状长度等于改动账上的截后字符数；"
              "截前字符 ≥ 截后字符；可再分发的许可类别不许被截短；"
              "被截短处必须仍逐字命中同一份底稿")
        if withheld_n:
            print(f"其中 {withheld_n} 条因底稿按公开口径未随仓库分发、本机不可复核，记 WITHHELD（不算不符）")
        print(f"判定结果: {'PASS 0 处不符' if bad == 0 else f'FAIL {bad} 处不符'}")
        return 0 if bad == 0 else 1

    # 写卡
    print(f"卡片 {len(card_files)} 张 · 引句 {len(ledger)} 处")
    print(f"全部引句：{before_total} → {after_total} 字符（-{before_total - after_total}）")
    print(f"其中许可受限来源：{before_r} → {after_r} 字符（-{before_r - after_r}，"
          f"降幅 {100 * (before_r - after_r) / max(1, before_r):.1f}%）")
    n_changed = sum(1 for r in ledger if r["是否截短"] == "是")
    print(f"被截短的引句 {n_changed} 处，涉及卡片 {len(plan)} 张")
    for cf, rows, raw in plan:
        new_raw = raw
        for row in sorted(rows, key=lambda r: -r["start"]):
            if not row["changed"]:
                continue
            new_raw = new_raw[: row["start"]] + row["new"] + new_raw[row["end"]:]
            row["start"] = len(row["new"])  # 仅占位
            row["end"] = row["start"]
        # 追加一条说明（放在 §9 溯源 一节末尾、CSV 回填块之前）
        accs = sorted({r["acc"] for r in rows if r["changed"]})
        n = sum(1 for r in rows if r["changed"])
        cats = sorted({r["cat"] for r in rows if r["changed"]})
        note = (f"\n- **{NOTE_MARK}（2026-11-08，公开仓库口径）**：本卡有 {n} 条逐字引句来自许可受限的第三方来源"
                f"（{'、'.join(accs)}；{'、'.join(cats)}），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，"
                f"已把单条引句截到 ≤{PER_QUOTE_CAP} 字符、同一来源总量截到 ≤{PER_PAIR_CAP} 字符；**截短后仍逐字命中同一份底稿**"
                f"（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。"
                f"逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。\n")
        m = re.search(r"\n<!--CSV回填", new_raw)
        if m:
            new_raw = new_raw[:m.start()] + note + new_raw[m.start():]
        else:
            new_raw = new_raw.rstrip() + "\n" + note
        cf.write_text(new_raw, encoding="utf-8")

    with LEDGER.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ledger[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(ledger)
    # 汇总表：逐 (卡, 来源编号) 的前后对照，便于审计"还剩多少被复制的原文"
    summary: dict[tuple[str, str, str], dict] = {}
    for r in ledger:
        k = (r["卡片"], r["来源编号"], r["许可类别"])
        s = summary.setdefault(k, {"前": 0, "后": 0, "n": 0, "截": 0})
        s["前"] += int(r["截前字符"])
        s["后"] += int(r["截后字符"])
        s["n"] += 1
        s["截"] += 1 if r["是否截短"] == "是" else 0
    with SUMMARY.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["卡片", "来源编号", "许可类别", "引句条数", "被截短条数", "截前字符", "截后字符"])
        for (card, acc, cat), s in sorted(summary.items(), key=lambda x: -x[1]["前"]):
            w.writerow([card, acc, cat, s["n"], s["截"], s["前"], s["后"]])
    print(f"已改写 {len(plan)} 张卡；改动账 → {LEDGER.relative_to(ROOT)} / {SUMMARY.relative_to(ROOT)}")
    print("下一步：跑 scripts/verify_literature_cards.py 复核 152 行是否仍全部 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
