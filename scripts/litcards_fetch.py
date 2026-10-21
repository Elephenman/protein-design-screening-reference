#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补齐 152 行里还缺本地全文的那部分：走 Europe PMC 抓全文，落盘并记账。

规则（不许含糊）：
- 抓取失败 / 无 OA 全文 = FETCH_FAILED 或 NO_OA_FULLTEXT，是"我们没拿到"，不是"该文没有正文"。
- 已经落盘且非空的直接跳过（可续跑）。
- 每次请求间隔 sleep，串行，不并发压公共接口。
- 全程写 fetch_log.tsv：编号 / 通路 / URL / HTTP / 字节 / SHA-256前16 / 状态 / 说明。
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
import hashlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from litcards_text import norm, to_text  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "literature_cards"
FT = OUT / "fulltext"
UA = {"User-Agent": "litcards-build/1.0 (academic literature review; low rate)"}
SLEEP = 0.5
TIMEOUT = 45


def get(url: str) -> tuple[int, str, str]:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read().decode("utf-8", "replace")
            return r.status, body, ""
    except urllib.error.HTTPError as e:
        return e.code, "", f"HTTPError {e.code}"
    except Exception as e:  # noqa: BLE001
        return 0, "", f"{type(e).__name__}: {str(e)[:120]}"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def resolve_pmcid(rec: dict) -> tuple[str, str]:
    """由 PMID / DOI 反查 PMCID（先查号再取正文，不猜）。Europe PMC 查不到就换 NCBI elink。"""
    url = rec["fetch_url"]
    code, body, err = get(url)
    pmcid = ""
    msg = ""
    if code == 200 and body:
        try:
            rl = json.loads(body).get("resultList", {}).get("result", [])
        except json.JSONDecodeError:
            rl = []
        if rl:
            pmcid = rl[0].get("pmcid", "") or ""
            if not pmcid:
                oa = str(rl[0].get("isOpenAccess", "")).upper()
                msg = f"记录存在但无 PMCID (isOpenAccess={oa or 'NA'})"
        else:
            msg = "search 零命中"
    else:
        msg = f"search {code} {err}"
    if pmcid:
        return pmcid, ""
    for pmid in rec["ids"]["pmid"][:1]:
        time.sleep(SLEEP)
        e = (f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
             f"?dbfrom=pubmed&db=pmc&id={pmid}&retmode=json")
        c2, b2, err2 = get(e)
        if c2 == 200 and b2:
            try:
                d = json.loads(b2)
                for ls in d.get("linksets", []):
                    for db in ls.get("linksetdbs", []) or []:
                        if db.get("linkname", "").startswith("pubmed_pmc") and db.get("links"):
                            return f"PMC{db['links'][0]}", f"elink 补到号 ({err2[:40]})"
            except json.JSONDecodeError:
                pass
        msg += f" | elink:{c2} {err2[:50]}"
    return "", msg


def save(acc: str, tag: str, xml: str, note: str) -> tuple[str, str]:
    FT.mkdir(parents=True, exist_ok=True)
    raw = FT / f"{acc}_{tag}_fullTextXML.xml"
    txt = FT / f"{acc}_{tag}_text.txt"
    raw.write_bytes(xml.encode("utf-8"))
    body = to_text(xml)
    txt.write_text(body, encoding="utf-8")
    if len(body) < 8000:
        note += f" | 正文仅 {len(body):,} 字符, 短文/扩展摘要风险"
    return sha(raw.read_bytes()), note or "ok"


def clean_html(html_body: str) -> str:
    """预剥 HTML：去掉 script/style/head 注释，再交给 to_text 去标签。"""
    s = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", html_body)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    return s


def ncbi_efetch(pmcid: str) -> tuple[int, str, str]:
    """Europe PMC 对某些 PMC 记录回 500（有 PMC 页但没 JATS），NCBI 侧常有 XML。"""
    num = pmcid.upper().replace("PMC", "")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={num}&retmode=xml"
    code, body, err = get(url)
    return code, body, f"{err or ''} via {url[:60]}"


def biorxiv_full(rec: dict) -> tuple[int, str, str]:
    """PPR 记录 Europe PMC 常常没有 XML；直接走预印本站点的 .full HTML。"""
    url = rec["ids"].get("url", "")
    m = re.search(r"(10\.1101/[\w.:-]+?)(?:v\d+)?(?:\?|$)", url) or (rec["ids"]["doi"][0] if rec["ids"]["doi"] else "")
    doi = m.group(1) if hasattr(m, "group") else m
    host = "www.biorxiv.org" if "medrxiv" not in url else "www.medrxiv.org"
    for v in ("v1", ""):
        u = f"https://{host}/content/{doi}{v}.full"
        code, body, err = get(u)
        if code == 200 and len(body) > 20000:
            return code, clean_html(body), f"via {u}"
        time.sleep(SLEEP)
    return 0, "", f"biorxiv 未取到 ({doi})"


def main() -> int:
    inv = json.loads((OUT / "inventory.json").read_text(encoding="utf-8"))
    todo = [r for r in inv if not r["has_fulltext"] and r["fetch_channel"] != "no_id"]
    log = OUT / "fetch_log.tsv"
    rows: list[tuple] = []
    done_ids = {p.name.split("_")[0] for p in FT.glob("*_text.txt")} if FT.exists() else set()
    ok = skipped = failed = 0
    print(f"待抓 {len(todo)} 行（已有落盘的 {len(done_ids)} 个编号会跳过）")
    for rec in todo:
        acc = rec["id"]
        if acc in done_ids:
            skipped += 1
            rows.append((acc, rec["fetch_channel"], rec["fetch_url"], "-", "-", "-", "SKIP_LOCAL", "本地已落盘"))
            continue
        url = rec["fetch_url"]
        chan = rec["fetch_channel"]
        if chan == "epmc_search_then_fulltext":
            pmcid, msg = resolve_pmcid(rec)
            time.sleep(SLEEP)
            if not pmcid:
                failed += 1
                rows.append((acc, chan, url, "-", "-", "-", "NO_OA_FULLTEXT", msg))
                print(f"  {acc} NO_OA_FULLTEXT {msg}")
                continue
            url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
            tag = pmcid
        else:
            tag = rec["fetch_url"].rsplit("/", 2)[-2] if "PMC" in rec["fetch_url"] or "PPR" in rec["fetch_url"] else "rec"
            m = re.search(r"(PMC\d+|PPR\d+)", rec["fetch_url"])
            tag = m.group(1) if m else "rec"
        code, body, err = get(url)
        got, note = "", ""
        if code == 200 and len(body) > 4000:
            got = body
        elif code == 200:
            time.sleep(SLEEP)
            code2, body2, err2 = get(url)
            got = body2 if code2 == 200 and len(body2) > 4000 else ""
            if not got:
                err = f"两次 200 但正文过短({len(body)}B/{len(body2)}B)"
        if not got and code == 500:
            time.sleep(3.0)  # 500 有相当一部分是限流，间隔后再试一次
            code, body, err = get(url)
            got = body if code == 200 and len(body) > 4000 else ""
        if not got:
            for name, fn in (("ncbi_efetch", lambda: ncbi_efetch(rec["ids"]["pmc"][0])
                              if rec["ids"]["pmc"] else (0, "", "无 PMCID 可走 NCBI")),
                             ("biorxiv_full", lambda: biorxiv_full(rec)
                              if (rec["ids"]["ppr"] or "biorxiv" in rec["ids"].get("url", "")
                                  or "medrxiv" in rec["ids"].get("url", "")) else (0, "", "非预印本"))):
                time.sleep(SLEEP)
                c2, b2, e2 = fn()
                if c2 == 200 and len(b2) > 8000:
                    got, note, tag = b2, f"fallback_ok[{name}] {e2[:70]}", (tag or "fb")
                    break
                err = f"{err} | {name}:{c2} {e2[:70]}"
        if not got:
            failed += 1
            rows.append((acc, chan, url, code, len(got) or 0, "-", "FETCH_FAILED", err[:200] or "空响应"))
            print(f"  {acc} FETCH_FAILED {code} {err}")
            continue
        ident = (to_text(got) if got.lstrip().startswith("<") else norm(got))[:1500].lower()
        words = {w for w in re.sub(r"[^A-Za-z]+", " ", rec["title"]).lower().split()
                 if len(w) > 3}
        cov = (sum(1 for w in words if w in ident) / len(words)) if words else 0.0
        fpmc = re.findall(r"PMC(\d+)", ident.upper())
        rp = [x.replace("PMC", "") for x in rec["ids"]["pmc"]]
        pmc_conflict = bool(fpmc) and bool(rp) and not (set(fpmc) & set(rp))
        fdoi = {x.lower().rstrip(".") for x in
                re.findall(r"10\.\d{4,9}/[^\s;,\"'<>)）]+", ident)}
        rdoi = {d.lower().rstrip(".") for d in rec["ids"]["doi"]}
        doi_conflict = bool(fdoi) and bool(rdoi) and not (fdoi & rdoi)
        doi_ok = any(d.lower() in ident for d in rec["ids"]["doi"])
        if pmc_conflict or doi_conflict:
            failed += 1
            rows.append((acc, chan, url, code, len(got), "-", "WRONG_PAPER_Fetched",
                         f"身份块号冲突(pmc_conflict={pmc_conflict}, doi_conflict={doi_conflict}: {sorted(fdoi)[:2]} vs {sorted(rdoi)[:2]})，拒收"))
            print(f"  {acc} WRONG_PAPER 身份块号冲突 {sorted(fdoi)[:2]}，拒收不入库")
            continue
        if not (doi_ok or cov >= 0.6):
            failed += 1
            rows.append((acc, chan, url, code, len(got), "-", "WRONG_PAPER_Fetched",
                         f"正文身份块既无本行 DOI 也无标题重合(覆盖 {cov:.2f})，拒收（号反查错认）"))
            print(f"  {acc} WRONG_PAPER (DOI 不在头部, 标题覆盖 {cov:.2f})，拒收不入库")
            continue
        h, note2 = save(acc, tag, got, note)
        ok += 1
        rows.append((acc, chan, url, code, len(got), h, "OK", (note2 or "")[:180]))
        print(f"  {acc} OK {tag} {len(got):,} B {h} {note2}")
        time.sleep(SLEEP)

    with log.open("a", encoding="utf-8", newline="") as fh:
        if log.stat().st_size == 0:
            fh.write("id\tchannel\turl\thttp\tbytes\tsha16\tstatus\tnote\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    print(f"判定标准: 每行要么落盘 >4KB 全文, 要么显式记 NO_OA_FULLTEXT / FETCH_FAILED")
    print(f"判定结果: OK {ok} · SKIP {skipped} · 未拿到 {failed} · 合计 {ok+skipped+failed}/{len(todo)}")
    print(f"找出来没有: 本步骤只补正文, 不做任何判定")
    return 0


if __name__ == "__main__":
    sys.exit(main())
