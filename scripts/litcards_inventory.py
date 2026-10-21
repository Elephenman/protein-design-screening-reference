#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文献卡片：把 CSV 每行 ↔ 本地全文 ↔ 待抓取 三者对上账。

输出:
  data/literature_cards/inventory.tsv   每行一篇: 编号/标题/号/证据级别/本地全文/是否需要抓/抓取URL
  data/literature_cards/inventory.json  同内容机器版

判据(不猜): 本地全文 = 在项目目录里按 PMCID / DOI 字符串实际搜到的 .txt|.xml 文件。
搜到才算有, 搜不到一律 needs_fetch=yes; 抓不到也不许写成"该文不存在"(取回失败≠权威阴性)。
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "protein_design_literature.csv"
OUT = ROOT / "data" / "literature_cards"
CACHE_DIRS = [ROOT / "data" / "interim" / "baker_lit" / "ft",
              ROOT / "data" / "interim" / "claim_lit",
              OUT / "fulltext"]


def col(row: dict, prefix: str) -> str:
    for k in row:
        if k.startswith(prefix):
            return (row[k] or "").strip()
    return ""


def extract_ids(r: dict) -> dict:
    """号只从权威列取：DOI 列 + other_ids/URL 里的 PMC/PPR/PMID。
    出处指针列里顺带提到的 DOI 不参与底稿匹配（实测 abs.txt 被 Z06/Z07/Z11 三行同时认领，
    就是因为那行只是"顺带引用"了同一篇，认领错了论文）。"""
    blob_ids = col(r, "PMID/PMCID")
    url = col(r, "链接")
    doi = re.findall(r"10\.\d{4,9}/[^\s;,（）()】✅❌]+", col(r, "DOI"))
    return {
        "pmc": sorted(set(re.findall(r"PMC\d+", blob_ids + " " + url))),
        "ppr": sorted(set(re.findall(r"PPR\d+", blob_ids + " " + url))),
        "pmid": sorted(set(re.findall(r"PMID\s*(\d{7,9})", blob_ids))),
        "doi": sorted(set(d for d in doi if not d.endswith(".")))[:2],
        "url": url,
    }


ID_CHARS = 1500  # 只有文件最开头的"身份块"里的号才算这篇论文自己的号


def header_index() -> dict[str, list[str]]:
    """扫缓存文件: 认领只认文件开头 ID_CHARS 字符内的号。

    两条误配都实测踩过：
      1) 正文参考文献里的别人 PMCID/DOI 会把引用它的论文认领成本身（antibodyRFdiff.txt ↔ Bennett 2023）；
      2) 多摘要拼接文件（claim_lit/abs.txt）头部含好几个 DOI，会被多行同时认领。
    只认头部身份块后，一个文件天然只属于它自己那篇。
    """
    idx: dict[str, list[str]] = {}
    for d in CACHE_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.rglob("*") if d.name != "fulltext" else d.glob("*")):
            if f.suffix.lower() not in (".txt", ".xml") or "_quarantine" in f.parts:
                continue
            body = f.read_text(encoding="utf-8", errors="replace")
            # 错误响应体与半截文件不算底稿：实测 claim_lit/PMC7165443.xml 只有 150 B，
            # 内容是 Europe PMC fullTextXML 的 HTTP 500 JSON，却因头部带 PMC 号被认领成"有全文"。
            if len(body) < 4000 or body.lstrip().startswith('{"timestamp"'):
                continue
            ident = body[:ID_CHARS]
            keys = set(re.findall(r"PMC\d+", ident)) | set(re.findall(r"PPR\d+", ident))
            # DOI 大小写不敏感（RFC 3697）：实测 eLife 的 XML 头写 10.7554/eLife.98179 而 CSV 行写
            # 10.7554/elife.98179，区分大小写会让 K40 明明有全文却被记成"无底稿"。
            keys |= {k.rstrip(".,;)").lower() for k in re.findall(r"10\.\d{4,9}/[^\s\"'<,;]+", ident)}
            if not keys:
                continue
            rel = str(f.relative_to(ROOT)).replace("\\", "/")
            for k in keys:
                idx.setdefault(k, []).append(rel)
    return {k: sorted(set(v)) for k, v in idx.items()}


PUBMED_CITE = re.compile(r"\b\d{4} [A-Z][a-z]{2} \d{1,2};\d")


def is_abstract_dump(path: Path) -> bool:
    """多条 PubMed 摘要拼在一起的文件（claim_lit/abs.txt、abs2.txt）。
    判据用"年 月 日;卷"式题录头出现 >=2 次，**不用** doi: 计数——实测 21 份真全文
    （B09/C05/K01/C21…）的参考文献里也各有 3–70 个 doi:，用 doi: 计数会把它们误降级。"""
    try:
        body = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    if body.lstrip().startswith("<"):
        return False
    return len(PUBMED_CITE.findall(body)) >= 2


def local_files(ids: dict, index: dict[str, list[str]]) -> list[str]:
    """在头部倒排索引里按号实搜（DOI 一侧统一转小写，见 header_index 的注释）。"""
    hits: list[str] = []
    for n in ids["pmc"] + ids["ppr"] + [d.lower() for d in ids["doi"]]:
        hits.extend(index.get(n, []))
    return sorted(set(hits))


def fetch_target(ids: dict) -> tuple[str, str]:
    """返回 (通路, URL)。优先级: PMCID > PPR > PMID > DOI(先换 PMCID)."""
    if ids["pmc"]:
        return ("epmc_fulltext",
                f"https://www.ebi.ac.uk/europepmc/webservices/rest/{ids['pmc'][0]}/fullTextXML")
    if ids["ppr"]:
        return ("epmc_fulltext",
                f"https://www.ebi.ac.uk/europepmc/webservices/rest/{ids['ppr'][0]}/fullTextXML")
    if ids["pmid"]:
        return ("epmc_search_then_fulltext",
                f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:{ids['pmid'][0]}&resultType=core&format=json")
    if ids["doi"]:
        return ("epmc_search_then_fulltext",
                f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%22{ids['doi'][0]}%22&resultType=core&format=json")
    return ("no_id", "")


def record_files(r: dict) -> list[str]:
    """从 原文出处指针 列里取 sources/*.md 底稿（不是全文，是本次调研的逐条记录）。"""
    ptr = col(r, "原文出处指针") + " " + col(r, "成本/统计")
    out = []
    for name in sorted(set(re.findall(r"sources/[A-Za-z0-9_\-\.]+\.md", ptr))):
        if (ROOT / name).exists():
            out.append(name)
    return out


def main() -> int:
    rows = list(csv.DictReader(CSV.open(encoding="utf-8-sig")))
    index = header_index()
    recs = []
    for r in rows:
        ids = extract_ids(r)
        loc_all = local_files(ids, index)
        # 摘要拼接文件降级为"记录"，不算全文（Z11 实测：唯一本地文件 abs.txt 里有 14 块摘要、21 个 doi:）
        dumps = [p for p in loc_all if is_abstract_dump(ROOT / p)]
        loc = [p for p in loc_all if p not in dumps]
        chan, url = fetch_target(ids)
        recs.append({
            "id": col(r, "编号"),
            "group": col(r, "人物组"),
            "title": col(r, "标题"),
            "year": col(r, "年份"),
            "venue": col(r, "期刊或预印本"),
            "evidence": col(r, "证据级别"),
            "ids": ids,
            "local": loc,
            "records": record_files(r) + [p for p in dumps if p not in record_files(r)],
            "has_fulltext": bool(loc),
            "fetch_channel": chan,
            "fetch_url": url,
        })
    n = len(recs)
    have = sum(1 for x in recs if x["has_fulltext"])
    fetchable = sum(1 for x in recs if not x["has_fulltext"] and x["fetch_channel"] != "no_id")
    dead = [x["id"] for x in recs if not x["has_fulltext"] and x["fetch_channel"] == "no_id"]
    (OUT / "inventory.json").write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
    with (OUT / "inventory.tsv").open("w", encoding="utf-8", newline="") as fh:
        fh.write("id\thas_fulltext\tlocal_n\tfetch_channel\ttitle\tevidence\n")
        for x in recs:
            fh.write(f"{x['id']}\t{'yes' if x['has_fulltext'] else 'no'}\t{len(x['local'])}\t"
                     f"{x['fetch_channel']}\t{x['title'][:60]}\t{x['evidence']}\n")
    print(f"CSV 行 {n} · 本地已有全文 {have} · 缺全文但可抓 {fetchable} · 无任何号可抓 {len(dead)}")
    print("无号行:", dead)
    print(f"判定标准: 本地全文必须在缓存目录的**头部 1500 字符**内按 PMCID/PPR/DOI 实搜命中才算'有'")
    shared: dict[str, list[str]] = {}
    for x in recs:
        for p in x["local"]:
            shared.setdefault(p, []).append(x["id"])
    amb = {p: v for p, v in shared.items() if len(v) > 1}
    if amb:
        print("AMBIGUOUS 一份底稿被多行认领(需人工确认归属):",
              {p.rsplit("/", 1)[-1]: v for p, v in list(amb.items())[:10]})
    print(f"判定结果: {have}/{n} 行有底稿, 差额 {n-have} 行走抓取通路; 退出码 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
