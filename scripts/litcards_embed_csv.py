#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把精读卡内容回写进 CSV 对应行背后。

做两件事：
  1. 用卡片第 9 节的 CSV 回填块覆盖 14 个内容字段（未记录 只允许在卡片明写时出现）。
  2. 追加两列：精读卡文件（相对路径） + 精读卡全文（整张卡原样塞进对应行背后）。

前置：全量门禁必须先 PASS（脚本自己跑一次，红就不写）。
写前先备份原 CSV 并把 SHA-256 记进 data/interim/csv_embed_manifest.json。
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from litcards_spec import CSV_COL, CSV_KEYS, parse_card, slug  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CSVP = ROOT / "data" / "protein_design_literature.csv"
CARDS = ROOT / "data" / "literature_cards"
INTERIM = ROOT / "data" / "interim"
NEW_COLS = ["精读卡文件", "精读卡全文(方法·工作流·遇坑)"]


def col_of(fieldnames: list[str], prefix: str) -> str:
    for k in fieldnames:
        if k.startswith(prefix):
            return k
    raise KeyError(prefix)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def card_for(acc: str) -> Path | None:
    hits = sorted(p for p in CARDS.glob(f"{slug(acc)}_*.md")
                  if p.name not in ("README.md", "run.md", "AGENT_RULES.md"))
    return hits[0] if hits else None


def preview(rows, fields) -> int:
    """--dry-run：只算不写。用来在全绿之前先看清"哪些行还没卡、回填块哪里缺键、
    会改动多少个字段、哪些卡正文短于回读门限"。门禁与 CSV 都不动。"""
    no_card, bad_block, short, changes = [], [], [], 0
    per_field: dict[str, int] = {}
    for r in rows:
        acc = r[col_of(fields, "编号")]
        card = card_for(acc)
        if card is None:
            no_card.append(acc)
            continue
        body = card.read_text(encoding="utf-8")
        vals, errs = parse_card(body)
        if errs:
            bad_block.append(f"{acc}: {errs[0]}")
            continue
        if len(body) < 2000:
            short.append(f"{acc}({len(body)} B)")
        for k in CSV_KEYS:
            col = col_of(fields, CSV_COL[k])
            if (r.get(col) or "") != vals[k]:
                changes += 1
                per_field[CSV_COL[k]] = per_field.get(CSV_COL[k], 0) + 1
    print(f"判定标准: --dry-run 只算不写；无卡行=0 且 回填块报错=0 且 短卡=0 才算可写")
    print(f"判定结果: 无卡 {len(no_card)} 行 · 回填块报错 {len(bad_block)} 行 · "
          f"正文<2000B {len(short)} 行 · 将改动字段 {changes} 处")
    print("  按字段统计:", "，".join(f"{k} {v}" for k, v in sorted(per_field.items(), key=lambda x: -x[1])))
    for label, lst in (("无卡", no_card), ("回填块", bad_block), ("短卡", short)):
        if lst:
            print(f"  {label}: {' '.join(map(str, lst[:25]))}{' …' if len(lst) > 25 else ''}")
    print(f"列数将 {len(fields)} → {len(fields) + len([c for c in NEW_COLS if c not in fields])}")
    return 0 if not (no_card or bad_block or short) else 1


def main() -> int:
    if "--dry-run" in sys.argv:
        with CSVP.open(encoding="utf-8-sig", newline="") as fh:
            rd = csv.DictReader(fh)
            return preview(list(rd), list(rd.fieldnames or []))
    gate = subprocess.run([sys.executable, str(ROOT / "scripts" / "verify_literature_cards.py")],
                          capture_output=True, text=True, encoding="utf-8")
    if gate.returncode != 0:
        print("全量门禁未通过，拒绝写 CSV。")
        print(gate.stdout[-2000:])
        return 1
    with CSVP.open(encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        fields = list(rd.fieldnames or [])
        rows = list(rd)

    backup = INTERIM / f"protein_design_literature_backup_{date.today().isoformat()}.csv"
    INTERIM.mkdir(exist_ok=True)
    backup.write_bytes(CSVP.read_bytes())
    out_fields = fields + [c for c in NEW_COLS if c not in fields]
    filled, missing, corrections = 0, [], []
    for r in rows:
        acc = r[col_of(fields, "编号")]
        card = card_for(acc)
        if card is None:
            missing.append(f"{acc}: 无卡")
            continue
        body = card.read_text(encoding="utf-8")
        vals, errs = parse_card(body)
        if errs:
            missing.append(f"{acc}: 回填块 {errs[0]}")
            continue
        for k in CSV_KEYS:
            col = col_of(out_fields, CSV_COL[k])
            if (r.get(col) or "") != vals[k]:
                corrections.append({"id": acc, "field": CSV_COL[k],
                                    "old": (r.get(col) or "")[:220], "new": vals[k][:220],
                                    "card": card.name})
            r[col] = vals[k]
        r["精读卡文件"] = str(card.relative_to(ROOT)).replace("\\", "/")
        r["精读卡全文(方法·工作流·遇坑)"] = body
        filled += 1
    if missing:
        print(f"拒绝写入：{len(missing)} 行不合格")
        for m in missing[:20]:
            print("  ", m)
        return 1

    tmp = CSVP.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=out_fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    CSVP.replace(INTERIM / "protein_design_literature_pre_embed.csv")
    tmp.replace(CSVP)
    (INTERIM / "csv_field_corrections.json").write_text(json.dumps(corrections, ensure_ascii=False, indent=1), encoding="utf-8")
    (INTERIM / "csv_embed_manifest.json").write_text(json.dumps({
        "date": date.today().isoformat(),
        "csv_rows": len(rows), "cards_filled": filled, "field_corrections": len(corrections),
        "csv_columns_before": len(fields), "csv_columns_after": len(out_fields),
        "backup": str(backup.relative_to(ROOT)).replace("\\", "/"),
        "backup_sha256": sha(backup),
        "previous_csv_kept_as": "data/interim/protein_design_literature_pre_embed.csv",
        "new_csv_sha256": sha(CSVP),
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    # 回读核验（不许只看写完就报成功）
    with CSVP.open(encoding="utf-8-sig", newline="") as fh:
        rd2 = csv.DictReader(fh)
        f2 = list(rd2.fieldnames or [])
        rows2 = list(rd2)
    ok = (len(rows2) == len(rows) and len(f2) == len(out_fields))
    bad = []
    for r in rows2:
        acc = r[col_of(f2, "编号")]
        if not r.get("精读卡文件") or not Path(ROOT / r["精读卡文件"]).exists():
            bad.append(f"{acc} 卡片路径不可达")
        if len(r.get("精读卡全文(方法·工作流·遇坑)", "")) < 2000:
            bad.append(f"{acc} 行内卡正文过短")
    print(f"字段改动 {len(corrections)} 处已记入 data/interim/csv_field_corrections.json（旧值/新值/卡片名，不改卡片不改备份）")
    print(f"判定标准: 门禁 PASS + 152 行全部有卡 + 回读后行数/列数一致 + 每行的卡路径可达且正文已进单元格")
    print(f"判定结果: 回写 {filled}/{len(rows2)} 行 · 列数 {len(fields)}→{len(f2)} · 回读 {'一致' if ok else '不一致'}"
          f" · 坏行 {len(bad)}")
    for b in bad[:10]:
        print("  ", b)
    print(f"备份: {backup.relative_to(ROOT)} sha {sha(backup)[:16]}…")
    return 0 if (ok and not bad) else 1


if __name__ == "__main__":
    sys.exit(main())
