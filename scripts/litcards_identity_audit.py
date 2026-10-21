#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""底稿身份体检：每份"全文"必须真的是它挂在名下的那篇论文。

踩过的坑：PMID→PMCID 反查会错认（C09 的 PMC13419775 实际是另一篇 2026 预印本，
本尊只出现在它的引文列表里）。所以认领之后还要再按标题与 DOI 复核一次。

判据：文件里必须出现 (a) 该行 DOI（去大小写、去尾点），或 (b) 标题实词覆盖率 >= 0.6。
两条都不满足 = MISMATCH，文件移进 fulltext/_quarantine/ 并改名保留证据，该行退回 DEGRADED。
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from litcards_text import norm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "literature_cards"
FT = CARDS / "fulltext"
QUAR = FT / "_quarantine"
STOP = set("the a an of and or in on for to with by de novo design novel using via from is are as "
            "protein proteins its their that this study new".split())


def col(row: dict, prefix: str) -> str:
    for k in row:
        if k.startswith(prefix):
            return (row[k] or "").strip()
    return ""


def content_words(title: str) -> set[str]:
    t = re.sub(r"<[^>]+>", " ", title)
    t = re.sub(r"[^A-Za-z]+", " ", t).lower()
    return {w for w in t.split() if len(w) > 3 and w not in STOP}


def dois_in(text: str) -> set[str]:
    """身份块里出现的 DOI（用于'号冲突即否'——他文只在参考文献里引本文时标题词也能凑够覆盖率）。"""
    return {x.lower().rstrip(".") for x in
            re.findall(r"10\.\d{4,9}/[^\s;,\"'<>)）]+", text)}


def main() -> int:
    rows = list(csv.DictReader((ROOT / "data" / "protein_design_literature.csv").open(encoding="utf-8-sig")))
    inv = {r["id"]: r for r in json.loads((CARDS / "inventory.json").read_text(encoding="utf-8"))}
    map_ = json.loads((CARDS / "sources_map.json").read_text(encoding="utf-8"))
    ok = mism = skipped = 0
    bad_files: list[str] = []
    for r in rows:
        acc = col(r, "编号")
        rec = inv.get(acc)
        if not rec:
            continue
        cand = [p for p in map_.get(acc, [])
                if (ROOT / p).exists() and (p.endswith("_text.txt") or "/ft/" in p)
                and not p.endswith(".xml") and Path(p).stat().st_size > 12000]
        if not cand:
            continue
        title = col(r, "标题")
        doi = col(r, "DOI").split()[0].rstrip(".") if col(r, "DOI") else ""
        words = content_words(title)
        for p in cand:
            text = norm((ROOT / p).read_text(encoding="utf-8", errors="replace"))
            # 只认身份块：参考文献列表里既有 DOI 也有完整标题，
            # 用全文匹配会把"引用它的论文"判成 OK（实测 C09 挂上的其实是 CAD 那篇 2026 预印本，
            # C17 挂上的是 JACS 2026 那篇只在参考文献里引本文）。
            ident = text[:1500].lower()
            head = text[:6000].lower()
            file_pmc = re.findall(r"pmc(?:id)?[^\w]?(\d{6,8})", text[:600].lower())
            row_pmc = re.findall(r"PMC(\d+)", " ".join(
                [col(r, "PMID/PMCID"), col(r, "链接")]))
            if file_pmc and row_pmc:
                # 两边都有 PMC 号时以号为准：号不同就不是同一篇，别给 DOI 顺带命中蒙混
                ok_id = bool(set(file_pmc) & set(row_pmc))
            else:
                ok_id = bool(doi) and doi.lower() in ident
            # DOI 冲突优先否定：身份块自带别的 DOI => 这是另一篇（C17 实测：
            # 挂在名下的文件是 JACS 2026 那篇，只在参考文献里引用本文，标题词覆盖率仍凑到 0.75）
            conflict = bool(doi) and bool(dois_in(ident)) and doi.lower() not in dois_in(ident)
            cov = (sum(1 for w in words if w in head) / len(words)) if words else 0.0
            if conflict:
                mism += 1
                bad_files.append(p)
                print(f"  MISMATCH {acc} <- {Path(p).name} (身份块 DOI={sorted(dois_in(ident))[:2]} != 行 DOI {doi})")
            elif ok_id or cov >= 0.6:
                ok += 1
                print(f"  OK       {acc} <- {Path(p).name} (身份号匹配={ok_id} 标题覆盖={cov:.2f})")
            else:
                mism += 1
                bad_files.append(p)
                print(f"  MISMATCH {acc} <- {Path(p).name} (号不匹配, 标题覆盖={cov:.2f}) 标题={title[:60]}")

    # 第二段体检：fulltext/ 里按编号命名的文件，必须真的属于那个编号
    # （sources_map 没登记也会被查到——C09_PMC13419775_text.txt 就是这么揪出来的）
    byslug = {}
    for r in rows:
        acc = col(r, "编号")
        byslug.setdefault(re.sub(r"[^A-Za-z0-9]+", "-", acc).strip("-"), (acc, col(r, "标题"), col(r, "DOI").split()[0].rstrip(".")))
    orphans = 0
    for f in sorted(FT.glob("*_text.txt")):
        acc, title, doi = byslug.get(f.name.split("_", 1)[0], ("?", f.name, ""))
        head = norm(f.read_text(encoding="utf-8", errors="replace"))[:6000].lower()
        words = {w for w in re.sub(r"[^A-Za-z]+", " ", title).lower().split() if len(w) > 3}
        cov = (sum(1 for w in words if w in head) / len(words)) if words else 0.0
        ident = norm(f.read_text(encoding="utf-8", errors="replace"))[:1500].lower()
        fpmc = re.findall(r"pmc(?:id)?[^\w]?(\d{6,8})", ident)
        okd = bool(doi) and doi.lower() in ident
        fdoi = dois_in(ident)
        conflict = bool(doi) and bool(fdoi) and doi.lower() not in fdoi
        if acc == "?":
            print(f"  ORPHAN   {f.name}: 文件名前缀不是任何 CSV 编号")
            orphans += 1
        elif conflict:
            mism += 1
            bad_files.append(str(f.relative_to(ROOT)).replace("\\", "/"))
            print(f"  MISMATCH {acc} <- {f.name} (身份块 DOI={sorted(fdoi)[:2]} != 行 DOI {doi})")
        elif not (okd or cov >= 0.6):
            mism += 1
            bad_files.append(str(f.relative_to(ROOT)).replace("\\", "/"))
            print(f"  MISMATCH {acc} <- {f.name} (doi={okd} 标题覆盖={cov:.2f})")
    if "--apply" in sys.argv and bad_files:
        QUAR.mkdir(parents=True, exist_ok=True)
        for p in bad_files:
            src = ROOT / p
            dst = QUAR / src.name
            shutil.move(str(src), str(dst))
            print(f"  移入隔离区: {p} -> {dst.relative_to(ROOT)}")
    print(f"判定标准: 身份块(文件开头 1500 字符)内比对——行 DOI 与文件 DOI 冲突即 MISMATCH(不看标题)；"
          f"否则要求行 DOI 命中或 PMC 号相等，再退到标题实词覆盖率>=0.6；"
          f"另查 fulltext/ 里按编号命名的文件是否挂错行")
    print(f"判定结果: OK {ok} · MISMATCH {mism} · 无候选全文跳过 {len(inv)-ok-mism} 行（{'已隔离' if '--apply' in sys.argv else '未改动，需 --apply'}）")
    print("找出来没有: 本体检只判「这份文件是不是这篇论文」，不判论文内容对错")
    return 1 if mism else 0


if __name__ == "__main__":
    sys.exit(main())
