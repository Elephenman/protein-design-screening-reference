"""Literature helper (Europe PMC / Crossref / PubMed / arXiv). Persistent copy."""
import sys, re, json, warnings, os
warnings.filterwarnings("ignore")
import requests

BASE = r"A:\Data\MD\projects\protein-design-screening-20261016\data\interim\baker_lit"
UA = {"User-Agent": "lit-review-agent/1.0 (research)"}


def epmc(query, n=20):
    r = requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search",
                    params={"query": query, "format": "json", "pageSize": min(n, 100), "resultType": "core"},
                    headers=UA, timeout=60)
    r.raise_for_status()
    d = r.json()
    out = []
    for it in d.get("resultList", {}).get("result", []):
        out.append({"title": it.get("title"), "journal": it.get("journalTitle"), "year": it.get("pubYear"),
                    "doi": it.get("doi"), "pmid": it.get("pmid"), "pmcid": it.get("pmcid"),
                    "authors": "; ".join([a.get("lastName", "") + " " + a.get("firstName", "")[:1] for a in (it.get("authorList") or {}).get("author", [])][:8]),
                    "nauth": len((it.get("authorList") or {}).get("author", [])),
                    "type": it.get("pubtype"), "abs": (it.get("abstractText") or "")[:2600]})
    return {"hitCount": d.get("hitCount"), "items": out}


def epmc_fulltext(pmcid):
    pmcid = pmcid if pmcid.upper().startswith("PMC") else "PMC" + pmcid
    r = requests.get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML", headers=UA, timeout=90)
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}"
    txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", r.text, flags=re.S)
    txt = re.sub(r"</(p|div|sec|table|tr|h1|h2|h3|li)>", "\n", txt)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"[ \t]+", " ", txt)
    return re.sub(r"\n\s*\n+", "\n", txt), None


def crossref(query, n=5):
    r = requests.get("https://api.crossref.org/works", params={"query.bibliographic": query, "rows": n}, headers=UA, timeout=60)
    r.raise_for_status()
    return [{"title": (it.get("title") or [""])[0], "journal": (it.get("container-title") or [""])[0],
             "year": (it.get("issued", {}).get("date-parts", [[None]])[0][0]), "doi": it.get("DOI"),
             "authors": ", ".join([a.get("family", "") for a in it.get("author", [])][:6]),
             "vol": it.get("volume"), "page": it.get("page") or it.get("article-number")}
            for it in r.json()["message"]["items"]]


def cr_doi(doi):
    r = requests.get(f"https://api.crossref.org/works/{doi}", headers=UA, timeout=60)
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code} {doi}"}
    it = r.json()["message"]
    return {"title": (it.get("title") or [""])[0], "journal": (it.get("container-title") or [""])[0],
            "year": it.get("issued", {}).get("date-parts", [[None]])[0][0], "doi": it.get("DOI"),
            "nauth": len(it.get("author", [])),
            "authors": ", ".join([a.get("family", "") + " " + (a.get("given", "") or "")[:1] for a in it.get("author", [])][:10]),
            "has_baker": any("baker" in (a.get("family", "") or "").lower() for a in it.get("author", [])),
            "vol": it.get("volume"), "page": it.get("page") or it.get("article-number")}


def download(names):
    os.makedirs(os.path.join(BASE, "ft"), exist_ok=True)
    for name, pmcid in names.items():
        fn = os.path.join(BASE, "ft", name + ".txt")
        if os.path.exists(fn) and os.path.getsize(fn) > 5000:
            print("cached", name, os.path.getsize(fn)); continue
        for attempt in range(2):
            try:
                txt, err = epmc_fulltext(pmcid)
            except Exception as e:
                print("ERR", name, e); continue
            if err:
                print("FAIL", name, pmcid, err)
            else:
                open(fn, "w", encoding="utf-8").write(txt)
                print("OK", name, pmcid, len(txt))
            break


def digest_sentences(path, maxs=45):
    txt = open(path, encoding="utf-8").read()
    sents = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", txt))
    keep, seen = [], set()
    for s in sents:
        if 40 < len(s) < 700 and re.search(r"\d", s) and re.search(
            r"(we (designed|made|screened|tested|expressed|generated|filtered|selected)|(\d,000|\d{4,7}) designs|screened|tested|hit rate|success rate|% of|% (of )?(designs|binders|sequences|constructs)|expressed and (bound|purified)|Kd of|K D of|filter|threshold|pLDDT|scTM|ipTM|pAE|recovery|ddG|Rosetta energy|yeast display|display library|out of \d|of the \d )", s, re.I):
            if s[:80] not in seen:
                seen.add(s[:80]); keep.append(s.strip())
    return keep[:maxs]
