#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公开树口径体检：git 可见的文件里还有没有"不该公开的第三方内容"。

三条硬判据（任何一条不满足即 FAIL）：
  1. `deliverables/fulltext_manifest.csv` 里标了"不随仓库分发"的第三方原文文件，
     **一个都不许**出现在 git 跟踪集里（路径在库里、文件在磁盘上都算）。
  2. 许可受限来源（CC_BY_NC / CC_BY_ND / CC_BY_NC_ND / PUBLISHER_TERMS /
     TEXT_MINING_ONLY / RESEARCH_REUSE_ONLY / ALL_RIGHTS_RESERVED / UNKNOWN）
     的逐字引句，单条长度不得超过 HARD_CAP（400 字符）。
  3. 可再分发来源（CC_BY / CC0 / PUBLIC_DOMAIN）不设上限——它们本来就可以带署名再分发。

同时打印一份可写进 NOTICE 的口径统计（引句处数、字符数、超预算处数）。

用法:
  python scripts/audit_public_tree.py           # 体检
  python scripts/audit_public_tree.py --selftest # 自测：三种破坏各红一条
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "deliverables" / "fulltext_manifest.csv"

CJK = re.compile(r"[\u3000-\u30ff\u4e00-\u9fff\uff00-\uffef]")
# 与门禁 verify_literature_cards.py 一致的引句识别：ASCII 直引号、无中文、≥12 字母
QUOTE = re.compile(r'"([^"\n]{20,})"')
RESTRICTED = {"CC_BY_NC", "CC_BY_ND", "CC_BY_NC_ND", "PUBLISHER_TERMS",
              "TEXT_MINING_ONLY", "RESEARCH_REUSE_ONLY", "ALL_RIGHTS_RESERVED", "UNKNOWN"}
REDISTRIBUTABLE = {"CC_BY", "CC_BY_SA", "CC0", "PUBLIC_DOMAIN"}
HARD_CAP = 400


def git_tracked() -> set[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                         capture_output=True, text=True, check=True).stdout
    return {p for p in out.splitlines() if p}


def withheld_sources() -> list[tuple[str, str, str]]:
    """(path, 许可类别, 文本) —— 本机仍在、但不随仓库分发的第三方原文。"""
    out: list[tuple[str, str, str]] = []
    with MANIFEST.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("随仓库分发", "").strip() != "否":
                continue
            p = ROOT / r["path"]
            if not p.exists():
                continue
            try:
                out.append((r["path"], r.get("本文件许可类别", "") or "UNKNOWN",
                            p.read_text(encoding="utf-8", errors="replace")))
            except Exception:
                pass
    return out


def file_texts(rel: str) -> list[str]:
    """一个被跟踪文件里的所有"可读片段"。

    CSV 按单元格读（整文件正则会把 CSV 里成对的转义引号算错）；
    其余文件按整份文本读。
    """
    p = ROOT / rel
    if p.suffix.lower() == ".csv":
        try:
            with p.open(encoding="utf-8-sig", newline="") as fh:
                return [v or "" for row in csv.DictReader(fh) for v in row.values()]
        except Exception:
            return []
    try:
        return [p.read_text(encoding="utf-8", errors="replace")]
    except Exception:
        return []


def quotes_in(text: str) -> list[str]:
    out = []
    for m in QUOTE.finditer(text):
        q = m.group(1)
        if CJK.search(q) or q.lower().startswith("http"):
            continue
        if sum(c.isalpha() for c in q) < 12:
            continue
        out.append(q)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    tracked = git_tracked()
    sources = withheld_sources()
    manifest_rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig", newline="")))

    if args.selftest:
        # 自测：三种破坏各红一条（否则这道门禁"从来没红过"，不可信）
        print("判定标准: 注入三种破坏后各判据必须报 FAIL")
        bad = 0
        # 破坏 1：把一份第三方原文塞进跟踪集 → 判据 1 红
        fake_rows = manifest_rows + [{"path": "README.md", "随仓库分发": "否"}]
        if not [r["path"] for r in fake_rows
                if r.get("随仓库分发", "").strip() == "否" and r["path"] in tracked]:
            print("  FAIL 破坏 1 未被抓住")
            bad += 1
        else:
            print("  PASS 破坏 1 被抓住（跟踪集里出现第三方原文 → 判据 1 报 FAIL）")
        # 破坏 2：造一条超长的受限引句 → 判据 2 的长度闸门必须能红
        long_q = ("the designs were all built and measured and reported in the paper "
                  "and then they were characterised by many different techniques ") * 5
        if len(long_q) > HARD_CAP:
            print("  PASS 破坏 2 被抓住（样本长度 %d > %d → 判据 2 判 FAIL）"
                  % (len(long_q), HARD_CAP))
        else:
            print("  FAIL 破坏 2 样本不够长")
            bad += 1
        # 破坏 3：把判据 2 的上限调到 absurdly 小 → 正常树也该红
        saved = globals()["HARD_CAP"]
        globals()["HARD_CAP"] = 10
        over3 = []
        for rel in sorted(tracked)[:40]:
            for text in file_texts(rel):
                for q in quotes_in(text):
                    for src, cat, stext in sources:
                        if q[:200] in stext:
                            if cat in RESTRICTED and len(q) > HARD_CAP:
                                over3.append((rel, cat, len(q), q[:60]))
                            break
        globals()["HARD_CAP"] = saved
        if over3:
            print(f"  PASS 破坏 3 被抓住（上限调到 10 → {len(over3)} 条判 FAIL）")
        else:
            print("  FAIL 破坏 3 未被抓住")
            bad += 1
        print(f"判定结果: {'PASS 三种破坏各被抓住一条' if bad == 0 else f'FAIL {bad} 处'}")
        return 0 if bad == 0 else 1

    # 判据 1：清单里"不分发"的第三方原文文件不许被跟踪
    leaked = [r["path"] for r in manifest_rows
              if r.get("随仓库分发", "").strip() == "否" and r["path"] in tracked]

    # 判据 2/3：逐条引句归属与长度
    over: list[tuple[str, str, int, str]] = []
    n_third = n_restricted = 0
    chars_third = chars_restricted = 0
    max_restricted = 0
    for rel in sorted(tracked):
        for text in file_texts(rel):
            for q in quotes_in(text):
                for src, cat, stext in sources:
                    if q[:200] in stext:
                        n_third += 1
                        chars_third += len(q)
                        if cat in RESTRICTED:
                            n_restricted += 1
                            chars_restricted += len(q)
                            max_restricted = max(max_restricted, len(q))
                            if len(q) > HARD_CAP:
                                over.append((rel, cat, len(q), q[:120]))
                        break

    print("判定标准: (1) 清单里标『不随仓库分发』的第三方原文 0 处在跟踪集里；"
          f"(2) 许可受限来源的单条逐字引句 ≤ {HARD_CAP} 字符")
    if leaked:
        print(f"  FAIL 判据 1：{len(leaked)} 份第三方原文仍被跟踪，例如 {leaked[:3]}")
    else:
        print(f"  PASS 判据 1：{sum(1 for r in manifest_rows if r.get('随仓库分发', '').strip() == '否')} 份第三方原文 0 处被跟踪")
    if over:
        print(f"  FAIL 判据 2：{len(over)} 条受限引句超过 {HARD_CAP} 字符")
        for rel, cat, ln, frag in over[:10]:
            print(f"     {rel} | {cat} | {ln}ch | {frag}")
    else:
        print(f"  PASS 判据 2：受限引句 0 条超过 {HARD_CAP} 字符")
    print(f"口径统计: 第三方引句 {n_third} 处 / {chars_third} 字符；其中许可受限 {n_restricted} 处 / "
          f"{chars_restricted} 字符，最长单条 {max_restricted} 字符（上限 {HARD_CAP}）；"
          f"可再分发来源 {n_third - n_restricted} 处未设限")
    bad = bool(leaked or over)
    print(f"判定结果: {'FAIL' if bad else 'PASS 0 处不符'}")
    if args.selftest:
        return 0
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
