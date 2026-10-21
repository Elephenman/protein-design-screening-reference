#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文献精读卡唯一核验器（152 行全覆盖门禁）。

用法:
  python scripts/verify_literature_cards.py                # 全量核验, 红则退出 1
  python scripts/verify_literature_cards.py --sync-map     # 按 inventory.json 重建 sources_map.json
  python scripts/verify_literature_cards.py --only B09 B20 # 只验这些编号

判定标准（机器执行，不靠人自觉）：
  A 每行必须有且仅有一张卡；卡内 10 个 section 标题齐全、顺序正确。
  B §3 工作流程表 >=3 步；§4 难点与应对 >=2 条。
  C 卡内所有"直双引号 + 纯 ASCII"片段视为逐字引句，必须在**该编号登记的每一份全文**里命中；
    没有本地全文的卡，引句至少要命中登记的非全文底稿（sources/*.md 等）。
  D 证据级别不许造假：卡里没有本地全文却在卡头声明"全文级" ⇒ FAIL。
  E 引句数量下限：有全文的卡 >=8 条；无全文的降级卡 >=2 条且必须写明受限。
输出: data/literature_cards/selfcheck.txt + rollout_status.tsv（逐行 PASS/FAIL 与原因）。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from litcards_spec import parse_card, slug  # noqa: E402
from litcards_text import norm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "literature_cards"
FULLTEXT = CARDS / "fulltext"
INVENTORY = CARDS / "inventory.json"
MAPFILE = CARDS / "sources_map.json"
CSVP = ROOT / "data" / "protein_design_literature.csv"

CJK = re.compile(r"[\u3000-\u30ff\u4e00-\u9fff\uff00-\uffef]")
QUOTE = re.compile(r'"([^"\n]{20,})"')
# PubMed 题录行（2023 Feb 1;15(2):34-50）。整份文件里出现 >=2 次 = 摘要转储拼接，不是单篇全文。
PUBMED_CITE = re.compile(r"\b\d{4} [A-Z][a-z]{2} \d{1,2};\d")
NON_CARDS = {"README.md", "run.md"}

# 卡片必须正好有 ## 0. ~ ## 9. 十个编号小节，且每节标题含指定关键词
SECTION_KEYWORDS = {
    0: ("元信息",), 1: ("解决什么", "一句话"), 2: ("难点",), 3: ("方法", "工作流"),
    4: ("台账",), 5: ("作者",), 6: ("我们",), 7: ("局限",), 8: ("迁移",), 9: ("溯源",),
}
DEGRADED = ("摘要级", "二级来源", "未获正文", "题录级", "已核验DOI", "未标注")


def col(row: dict, prefix: str) -> str:
    for k in row:
        if k.startswith(prefix):
            return (row[k] or "").strip()
    return ""


def clean(q: str) -> str:
    return norm(re.sub(r"\*\*|\*|`", "", q))


def quotes_of(card_body: str) -> list[str]:
    out = []
    for m in QUOTE.finditer(card_body):
        q = m.group(1)
        if CJK.search(q) or q.lower().startswith("http") or sum(c.isalpha() for c in q) < 12:
            continue
        out.append(clean(q))
    return out


def card_for(acc: str) -> Path | None:
    hits = sorted(p for p in CARDS.glob(f"{slug(acc)}_*.md") if p.name not in NON_CARDS)
    return hits[0] if hits else None


def build_map() -> dict:
    """编号 -> 全部本地底稿。完全由 inventory.json 重建（不并入旧表，
    否则上一版宽松匹配留下的误配（把引用它的论文当成本身）会永久残留。"""
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    m: dict[str, list[str]] = {}
    for rec in inv:
        m[rec["id"]] = sorted(set(rec["local"]) | set(rec.get("records", [])))
    MAPFILE.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    return m


def load_map() -> dict:
    if not MAPFILE.exists():
        return build_map()
    return json.loads(MAPFILE.read_text(encoding="utf-8"))


def check_sections(body: str) -> list[str]:
    """按 ## N. 编号判存在、唯一、顺序与标题关键词（只扫标题行，正文同词不算）。"""
    bad: list[str] = []
    seen: dict[int, str] = {}
    order: list[int] = []
    for ln in body.splitlines():
        m = re.match(r"^##\s*(\d+)\.\s*(.*)$", ln.strip())
        if not m:
            continue
        num = int(m.group(1))
        if num in seen:
            bad.append(f"小节 ## {num}. 出现多次")
        seen[num] = m.group(2)
        order.append(num)
    for num, kws in SECTION_KEYWORDS.items():
        if num not in seen:
            bad.append(f"缺小节 ## {num}.（应含 {'/'.join(kws)}）")
            continue
        if not any(k in seen[num] for k in kws):
            bad.append(f"小节 ## {num}. 标题「{seen[num][:28]}」里没有 {'/'.join(kws)}")
    if order != sorted(order):
        bad.append(f"小节编号顺序乱: {order}")
    return bad


def _section_span(body: str, keyword: str) -> str:
    m = re.search(rf"##[^\n]*{keyword}[^\n]*\n(.*?)(?=\n## |\Z)", body, re.S)
    return m.group(1) if m else ""


def workflow_steps(body: str) -> int:
    seg = _section_span(body, "工作流程")
    return len([ln for ln in seg.splitlines() if re.match(r"^\s*\|", ln)]) - 2  # 去表头/分隔


def difficulty_blocks(body: str) -> int:
    seg = _section_span(body, "难点")
    return len(re.findall(r"^\s*(?:\d+[\.\)]|[-*|]\s*\*\*)", seg, re.M))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sync-map", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-report", action="store_true",
                    help="只打印，不落盘 selfcheck.txt/rollout_status.tsv（多代理并行时用，避免互相覆盖）")
    args = ap.parse_args()
    if args.sync_map:
        m = build_map()
        print(f"sources_map.json 重建完成：{len(m)} 个编号，{sum(1 for v in m.values() if v)} 个有底稿")
        return 0

    rows = list(csv.DictReader(CSVP.open(encoding="utf-8-sig")))
    inv = {r["id"]: r for r in json.loads(INVENTORY.read_text(encoding="utf-8"))}
    smap = load_map()
    want = set(args.only) if args.only else None
    report: list[str] = []
    status: list[dict] = []
    failures = 0

    for r in rows:
        acc = col(r, "编号")
        if want and acc not in want:
            continue
        rec = inv.get(acc, {})
        line = {"id": acc, "title": col(r, "标题")[:40], "has_fulltext": "yes" if rec.get("has_fulltext") else "no",
                "card": "no", "quotes": "", "errors": ""}
        errs: list[str] = []
        card = card_for(acc)
        if card is None:
            errs.append("无卡片文件")
        else:
            line["card"] = card.name
            body = card.read_text(encoding="utf-8")
            errs += check_sections(body)
            _, cb_errs = parse_card(body)
            errs += cb_errs
            qs = quotes_of(body)
            w, d = workflow_steps(body), difficulty_blocks(body)
            if w < 3:
                errs.append(f"§工作流程表只有 {w} 步 (<3)")
            if d < 2:
                errs.append(f"§难点与应对只有 {d} 条 (<2)")
            srcs = [p for p in smap.get(acc, []) if (ROOT / p).exists() and not p.endswith(".xml")]
            missing_reg = [p for p in smap.get(acc, []) if not (ROOT / p).exists()]
            for p in missing_reg:
                errs.append(f"登记底稿缺失 {p}")
            texts, raws = {}, {}
            for p in srcs:
                raw = (ROOT / p).read_text(encoding="utf-8", errors="replace")
                raws[p], texts[p] = raw, norm(raw)
            # 拼接式摘要转储（如 claim_lit/abs.txt 把 21 篇的摘要装进一个文件）必须切到本行那一段再比引句，
            # 否则"从同一文件里别人的摘要抄一句"也能过门——这是实测存在的漏洞（文件含 14 块，Z11 只占 1 块）。
            # 触发条件用 PubMed 题录行特征 "\d{4} Abb 1;12:3"（实测：abs.txt 8 次、abs2.txt 3 次，
            # 而 84 份真全文/记录文件全部 0 次）。早先用 "doi: 出现 >=3 次" 当触发是错的——
            # 真全文的参考文献里本来就有 3~70 个 doi:，K50 的 sources/baker.md 因此被误判为空底稿。
            row_doi = col(r, "DOI").split()[0].rstrip(".") if col(r, "DOI") else ""
            for p, t in list(texts.items()):
                n_cite = len(PUBMED_CITE.findall(raws[p]))
                blocks = [b for b in re.split(r"(?=\d+\.\s+[A-Z][A-Za-z .&\-]{2,}\. \d{4})", t) if b.strip()]
                if n_cite >= 2 and len(blocks) >= 3:
                    keep = [b for b in blocks if row_doi and row_doi.lower() in b.lower()]
                    if keep:
                        texts[p] = " ".join(keep)
                        line.setdefault("notes", []).append(f"{Path(p).name}: 摘要转储文件，已切到本行 {len(blocks)}/{len(blocks)} 块中的 1 块")
                    else:
                        texts[p] = ""
                        errs.append(f"{p} 是多记录拼接文件但其中找不到本行 DOI，禁止作为引句底稿")
            m = re.search(r"引句底稿[:：]\s*[`\"']?([\w./\\-]+?\.(?:txt|md))", body)
            declared = m.group(1).replace("\\", "/") if m else ""
            if not declared:
                errs.append("§9 没写 引句底稿: <路径>，门禁不知道该拿哪份全文逐字比对")
            elif declared not in srcs:
                errs.append(f"引句底稿 {declared} 不在该编号登记的可读底稿里")
            elif qs:
                miss = [q for q in qs if q not in texts[declared]]
                for q in miss[:6]:
                    errs.append(f"引句未逐字命中 {declared}: {q[:110]}")
                line["quotes"] = f"{len(qs)-len(miss)}/{len(qs)}"
            if not srcs and qs:
                errs.append("该编号没有任何可读底稿，却有英文引句")
            for q in [q for q in qs if not any(q in t for t in texts.values())][:4]:
                errs.append(f"引句在所有底稿里都不命中: {q[:110]}")
            if rec.get("has_fulltext") and len(qs) < 8:
                errs.append(f"有全文但引句仅 {len(qs)} 条 (<8)")
            head0 = _section_span(body, "元信息") or body[:1200]
            if not rec.get("has_fulltext"):
                if len(qs) < 2:
                    errs.append(f"降级卡引句仅 {len(qs)} 条 (<2)")
                if not any(k in head0 for k in DEGRADED):
                    errs.append("无本地全文却未在 §0 标降级证据级别（摘要级/二级来源/未获正文/题录级）")
                if "全文级" in head0:
                    errs.append("证据级别造假：§0 声明全文级但没有本地全文")
        if errs:
            failures += 1
            line["errors"] = " ; ".join(errs)
            report.append(f"FAIL {acc} {line['title']}\n     " + "\n     ".join(errs))
        else:
            report.append(f"PASS {acc} quotes={line['quotes']}")
        status.append(line)

    if not args.no_report:
        (CARDS / "selfcheck.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
        with (CARDS / "rollout_status.tsv").open("w", encoding="utf-8", newline="") as fh:
            fh.write("id\thas_fulltext\tcard\tquotes\terrors\n")
            for s in status:
                fh.write("\t".join(str(s[k]).replace("\n", " ") for k in
                         ("id", "has_fulltext", "card", "quotes", "errors")) + "\n")
    total = len(status)
    npass = total - failures
    if args.no_report:
        print("\n".join(report))
    print(f"判定标准: 每行一张卡、10 节齐全、工作流程>=3 步、难点>=2 条、逐字引句在登记底稿里全部命中、证据级别不许造假")
    print(f"判定结果: {npass}/{total} 张卡 PASS，{failures} 行不合格（退出码 {'1' if failures else '0'}）")
    print(f"找出来没有: 本门禁只判卡片的完整性与引用真实性；正文内容对错仍需按 §溯源 指针人工复核")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
