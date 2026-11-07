#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更正文献总表里两类"卡与表对不上"的字段，并留下可复核的改动账。

两类：
  1. 手工核对出来的事实性错值（期刊、年份、核验状态措辞）——清单在 scripts/table_field_fixes.json，
     每条都带"依据"和"为什么原来是错的"。这些列不在 14 个回填键里，所以回填脚本不会覆盖它们，
     只能显式改。
  2. `证据级别` 列整体刷新——该列从未在卡片写完后同步过，实测 152 行里 58 行与卡 §0 的判定相反
     （含 Z01/Z03/Z05 这类"表里写全文级、卡里明写未获正文"的行）。新值由
     scripts/litcards_evidence_level.py 从卡 §0 推导，机器标签放在列首，括注保留可核的细节。

用法：
    python scripts/fix_table_fields.py --dry-run    # 只算不写，先看清要改哪些格子
    python scripts/fix_table_fields.py              # 写盘（先备份，带改动账，回读核验）

写盘前自动备份到 data/interim/protein_design_literature_backup_<date>_fieldfix.csv，
改动账写到 data/interim/table_field_fixes_<date>.json（旧值/新值/依据/来源卡片）。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from litcards_evidence_level import cell, tag_from_card  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CSVP = ROOT / "data" / "protein_design_literature.csv"
INTERIM = ROOT / "data" / "interim"
SPEC = ROOT / "scripts" / "table_field_fixes.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def col_of(fields: list[str], prefix: str) -> str:
    for k in fields:
        if k.startswith(prefix):
            return k
    raise KeyError(prefix)


def load_rows() -> tuple[list[str], list[dict]]:
    with CSVP.open(encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        return list(rd.fieldnames or []), list(rd)


def apply(rows: list[dict], fields: list[str], spec: list[dict]) -> list[dict]:
    changes: list[dict] = []
    by_id = {r[col_of(fields, "编号")].strip(): r for r in rows}
    for item in spec:
        acc = item["id"]
        if acc not in by_id:
            raise SystemExit(f"清单里的编号在总表里不存在：{acc}")
        r = by_id[acc]
        c = col_of(fields, item["column"])
        old = r.get(c) or ""
        if old == item["new"]:
            continue
        r[c] = item["new"]
        changes.append({"id": acc, "column": c, "kind": "manual_fact_fix",
                        "old": old, "new": item["new"], "reason": item["reason"]})
    # 证据级别整列刷新（从卡 §0 推导）
    c = col_of(fields, "证据级别")
    for r in rows:
        acc = r[col_of(fields, "编号")].strip()
        card_rel = (r.get("精读卡文件") or "").strip()
        card = ROOT / card_rel if card_rel else None
        if not card or not card.exists():
            hits = sorted(p for p in (ROOT / "data" / "literature_cards").glob(f"{acc}_*.md"))
            card = hits[0] if hits else None
        if not card or not card.exists():
            changes.append({"id": acc, "column": c, "kind": "evidence_level_refresh",
                            "old": r.get(c) or "", "new": "", "reason": "找不到卡片，无法推导证据级别"})
            continue
        body = card.read_text(encoding="utf-8")
        tag = tag_from_card(body)
        old = r.get(c) or ""
        new = cell(tag, old)
        if new != old:
            r[c] = new
            changes.append({"id": acc, "column": c, "kind": "evidence_level_refresh",
                            "old": old, "new": new, "reason": f"按卡 §0 推导（{card.name}）"})
    return changes


def check_ledger() -> int:
    """核改动账：账里的"新值"必须等于当前表里的格子，且受管列的每一处改动都必须有账可查。

    这个门是给"账目被覆盖"和"改了表没记账"两件事兜底的：
    实测踩过同日第二次运行把 152 条记录冲成 1 条，所以账必须能被机器核。
    """
    fields, rows = load_rows()
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    ledger_p = INTERIM / f"table_field_fixes_{date.today().isoformat()}.json"
    if not ledger_p.exists():
        cands = sorted(INTERIM.glob("table_field_fixes_*.json"))
        if not cands:
            print("判定结果: FAIL — 没有改动账（data/interim/table_field_fixes_*.json）")
            return 1
        ledger_p = cands[-1]
    led = json.loads(ledger_p.read_text(encoding="utf-8"))
    entries = led.get("changes", [])
    by_id = {r[col_of(fields, "编号")].strip(): r for r in rows}

    errs: list[str] = []
    # (1) 账里的新值必须就是当前表的值
    for c in entries:
        r = by_id.get(c["id"])
        if r is None:
            errs.append(f"账目里的 {c['id']} 在总表中不存在")
            continue
        col = c["column"]
        if col not in fields:
            errs.append(f"账目里的列 {col} 在总表中不存在")
            continue
        if (r.get(col) or "") != (c["new"] or ""):
            errs.append(f"{c['id']} {col} 账目新值与当前表不一致")
    # (2) 受管列的每一处改动都必须有账：手工列以 spec 为准，证据级别列以卡 §0 推导为准
    spec_by = {(s["id"], s["column"]): s["new"] for s in spec}
    recorded = {(c["id"], c["column"]) for c in entries}
    for r in rows:
        acc = r[col_of(fields, "编号")].strip()
        for (sid, cname), new in spec_by.items():
            if sid != acc:
                continue
            real = col_of(fields, cname)
            if (r.get(real) or "") != new and (acc, real) not in recorded:
                errs.append(f"{acc} {real} 当前值既不等于清单值也没有账目记录")
        creal = col_of(fields, "证据级别")
        tag = (r.get(creal) or "").split("｜")[0].strip()
        card_rel = (r.get("精读卡文件") or "").strip()
        card = ROOT / card_rel if card_rel else None
        if not card or not card.exists():
            hits = sorted(p for p in (ROOT / "data" / "literature_cards").glob(f"{acc}_*.md"))
            card = hits[0] if hits else None
        if not card or not card.exists():
            errs.append(f"{acc} 找不到卡片，无法核证据级别")
            continue
        want = tag_from_card(card.read_text(encoding="utf-8"))
        if tag != want and (acc, creal) not in recorded:
            errs.append(f"{acc} {creal} 与卡 §0 不一致且无账目记录")

    print(f"改动账: {ledger_p.relative_to(ROOT).as_posix()} · 条目 {len(entries)} 条")
    print("判定标准: 账里每条新值 == 当前表该格；受管列每处改动都有账；证据级别与卡 §0 一致")
    if errs:
        print(f"判定结果: FAIL（退出码 1）· 不合格 {len(errs)} 处")
        for e in errs[:12]:
            print("  -", e)
        return 1
    print("判定结果: PASS（退出码 0）")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    if args.check:
        return check_ledger()

    fields, rows = load_rows()
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    # 注意：apply 直接改 rows 本身。早先版本传的是 [dict(r) for r in rows]，
    # 改动全落在副本上，写出去的 CSV 一格没变，而回读检查把这事抓了出来。
    changes = apply(rows, fields, spec)

    by_kind: dict[str, int] = {}
    for c in changes:
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1

    if args.dry_run:
        print("判定标准: --dry-run 只算不写；改动清单逐条带依据")
        print(f"判定结果: 将改动 {len(changes)} 处 —— " + "，".join(f"{k} {v}" for k, v in sorted(by_kind.items())))
        for c in changes[:12]:
            print(f"  {c['id']} {c['column']}: {c['old'][:60]!r} → {c['new'][:80]!r}")
        if len(changes) > 12:
            print(f"  … 另有 {len(changes)-12} 处")
        return 0

    if not changes:
        print("判定标准: 无改动即无需写盘")
        print("判定结果: 0 处待改（总表已与卡片一致）")
        return 0

    INTERIM.mkdir(exist_ok=True)
    today = date.today().isoformat()
    backup = INTERIM / f"protein_design_literature_backup_{today}_fieldfix.csv"
    # 备份不能被同日第二次运行覆盖：第一份备份是"本轮改动前"的状态，
    # 被第二次运行冲掉后，改动账里的 csv_sha256_before 就指不到任何一个真实文件了。
    if backup.exists():
        n = 2
        while (INTERIM / f"protein_design_literature_backup_{today}_fieldfix_{n}.csv").exists():
            n += 1
        backup = INTERIM / f"protein_design_literature_backup_{today}_fieldfix_{n}.csv"
    shutil.copy2(CSVP, backup)

    tmp = CSVP.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(CSVP)

    # 改动账同样不能被同日第二次运行覆盖（实测踩过：152 条记录被只剩 1 条）。
    # 做法：账目文件按日期存，但同日再跑就**合并**进已有账目，并保留 run_log。
    ledger_p = INTERIM / f"table_field_fixes_{today}.json"
    if ledger_p.exists():
        prev = json.loads(ledger_p.read_text(encoding="utf-8"))
        merged = list(prev.get("changes", []))
        seen = {(c.get("id"), c.get("column"), c.get("old")) for c in merged}
        added = 0
        for c in changes:
            key = (c.get("id"), c.get("column"), c.get("old"))
            if key in seen:
                continue
            merged.append(c)
            seen.add(key)
            added += 1
        run_log = list(prev.get("run_log", []))
        run_log.append({"run": len(run_log) + 1, "changes": added,
                        "csv_sha256_before": sha(backup)})
        prev["changes"] = merged
        prev["run_log"] = run_log
        prev["merged_from_ledger"] = ledger_p.name
        ledger_p.write_text(json.dumps(prev, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        ledger_p.write_text(
            json.dumps({"date": today, "csv_sha256_before": sha(backup),
                        "changes": changes,
                        "run_log": [{"run": 1, "changes": len(changes),
                                     "csv_sha256_before": sha(backup)}]},
                       ensure_ascii=False, indent=1), encoding="utf-8")

    # 回读核验
    fields2, rows2 = load_rows()
    spec_by = {(s["id"], s["column"]): s["new"] for s in spec}
    bad = []
    for r in rows2:
        acc = r[col_of(fields2, "编号")].strip()
        for (sid, cname), new in spec_by.items():
            if sid != acc:
                continue
            # cname 是列名前缀（如"年份"），真列名是"年份(year)"——回读必须按前缀解析，
            # 否则读的是不存在的列名，一致也判成不一致（这个坑第一次跑就踩了）。
            real = col_of(fields2, cname)
            if (r.get(real) or "") != new:
                bad.append(f"{acc} {real} 回读不一致")
        tag = (r.get(col_of(fields2, "证据级别")) or "").split("｜")[0].strip()
        if tag not in ("FULLTEXT", "DEGRADED", "UNKNOWN"):
            bad.append(f"{acc} 证据级别列没有机器标签: {r.get(col_of(fields2, '证据级别'))!r}")
    ok = len(rows2) == len(rows) and len(fields2) == len(fields)
    print("判定标准: 写前备份 + 逐条依据 + 回读后行数/列数不变 + 手工改动逐条命中 + 证据级别列首为机器标签")
    print(f"判定结果: 改动 {len(changes)} 处（" + "，".join(f"{k} {v}" for k, v in sorted(by_kind.items())) +
          f"）· 回读 {'一致' if ok else '不一致'} · 不合格 {len(bad)} 处")
    for b in bad[:10]:
        print("  ", b)
    print(f"备份: {backup.relative_to(ROOT).as_posix()} sha256 {sha(backup)[:16]}…")
    print(f"改动账: data/interim/table_field_fixes_{today}.json")
    return 0 if (ok and not bad) else 1


if __name__ == "__main__":
    sys.exit(main())
