#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给缺 `引句底稿:` 声明行的卡片自动补上该声明（确定性修复，不改内容）。

规则很窄：只有当该编号登记的某一份可读底稿**单独**包含卡内全部逐字引句时才补；
命中多份或零份就不动，让门禁继续判 FAIL，交回人工确认到底照着哪份写的。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from litcards_spec import slug  # noqa: E402
from litcards_text import norm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "literature_cards"
CJK = re.compile(r"[\u3000-\u30ff\u4e00-\u9fff\uff00-\uffef]")
QUOTE = re.compile(r'"([^"\n]{20,})"')


def main() -> int:
    smap = json.loads((CARDS / "sources_map.json").read_text(encoding="utf-8"))
    only = set(sys.argv[1:])
    inv = {r["id"]: r for r in json.loads((CARDS / "inventory.json").read_text(encoding="utf-8"))}
    fixed, skipped = [], []
    for acc in sorted(smap):
        if only and acc not in only:
            continue
        card = next(iter(sorted(p for p in CARDS.glob(f"{slug(acc)}_*.md")
                               if p.name not in ("README.md", "run.md"))), None)
        if card is None:
            continue
        body = card.read_text(encoding="utf-8")
        if re.search(r"引句底稿[:：]", body):
            continue
        qs = [re.sub(r"\*\*|\*|`", "", q) for q in QUOTE.findall(body)
              if not CJK.search(q) and sum(c.isalpha() for c in q) >= 12 and not q.lower().startswith("http")]
        if not qs:
            skipped.append((acc, "无引句可定位"))
            continue
        readable = [p for p in smap[acc] if (ROOT / p).exists() and not p.endswith(".xml")]
        texts = {p: norm((ROOT / p).read_text(encoding="utf-8", errors="replace")) for p in readable}
        hits = [p for p, t in texts.items() if all(norm(q) in t for q in qs)]
        if len(hits) != 1:
            skipped.append((acc, f"全部引句同时命中 {len(hits)} 份底稿，需人工指定"))
            continue
        line = f"\n引句底稿: {hits[0]}\n"
        m = re.search(r"(## 9\.[^\n]*\n)", body)
        if not m:
            skipped.append((acc, "找不到 ## 9. 标题"))
            continue
        body = body[:m.end()] + line + body[m.end():]
        card.write_text(body, encoding="utf-8")
        fixed.append((card.name, hits[0]))
    print(f"判定标准: 仅当卡内全部引句单独命中一份登记底稿时才补声明行")
    print(f"判定结果: 自动补 {len(fixed)} 张 · 仍需人工 {len(skipped)} 张")
    for f, h in fixed:
        print(f"  AUTO-OK  {f} <- {h}")
    for a, why in skipped:
        print(f"  MANUAL   {a}: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
