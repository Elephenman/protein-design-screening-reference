# -*- coding: utf-8 -*-
"""spot_check3.py — 复核报告中剩余三条吃重数字（宽松匹配 + 正确的检索端点）。"""
import json, re, urllib.request, urllib.parse

E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
S = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={}&format=json&pageSize=8&resultType=core"
FT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{}/fullTextXML"


def get(u):
    try:
        r = urllib.request.Request(u, headers={"User-Agent": "chk3/1.0"})
        return urllib.request.urlopen(r, timeout=40).read().decode("utf-8", "replace")
    except Exception as e:
        return "__ERR__" + type(e).__name__ + ":" + str(e)


def clean(s):
    return re.sub(r"[\r\n\t ]+", " ", re.sub(r"<[^>]+>", " ", s))


def pmcids_for(term):
    j = get(S.format(urllib.parse.quote(term)))
    try:
        return [(r.get("pmcid"), r.get("title", "")[:70], r.get("doi"))
                for r in json.loads(j)["resultList"]["result"] if r.get("pmcid")], j
    except Exception:
        return [], j


# --- A. Rocklin 2017: "from 6% to 47%"（用 PubMed 摘要 XML） ---
pm = get(E + "esearch.fcgi?db=pubmed&term=Global+analysis+of+protein+folding+using+massively+parallel+design&retmax=3&retmode=json")
ids = re.findall(r'"uid":"(\d+)"', pm)
abs_txt = ""
if ids:
    a = get(E + "efetch.fcgi?db=pubmed&id=" + ids[0] + "&retmode=xml")
    abs_txt = clean(" ".join(re.findall(r"<AbstractText[^>]*>(.*?)</AbstractText>", a, re.S)))
print("A) Rocklin2017 PMID", ids[:1])
for pat in [r"from 6%? to 47%?", r"6% to 47", r"47%"]:
    m = re.search(pat, abs_txt)
    print("   ", "HIT " if m else "MISS", pat, ("…" + abs_txt[max(0, m.start()-120):m.start()+120] + "…") if m else "")

# --- B. Gerasimavicius 2023: rho 0.26/0.28 ---
recs, _ = pmcids_for('DOI:"10.1002/pro.4688"')
print("\nB) Gerasimavicius2023 记录:", recs)
blob = ""
if recs:
    blob = clean(get(FT.format(recs[0][0])))
if len(blob) < 500:  # 退路：直接找开放版本
    recs2, _ = pmcids_for('TITLE:"Correspondence between functional scores from deep mutational scans"')
    for pmcid, t, d in recs2:
        b2 = clean(get(FT.format(pmcid)))
        if len(b2) > 1000:
            blob, recs = b2, [(pmcid, t, d)]
            break
print("   文本长度:", len(blob))
for pat in [r"0\.26", r"0\.28", r"average rho", r"Spearman"]:
    m = re.search(pat, blob, re.I)
    print("   ", "HIT " if m else "MISS", pat, ("…" + blob[max(0, m.start()-160):m.start()+160] + "…") if m else "")

# --- C. PLACER：MD 太贵不能用于大量设计 ---
recs3, j3 = pmcids_for('FULL_TEXT:"numbers of designs" AND FULL_TEXT:"preorganization"')
print("\nC) PLACER 全文检索命中（带 PMCID）:", recs3)
hit = None
for pmcid, t, d in recs3:
    b = clean(get(FT.format(pmcid)))
    m = re.search(r"molecular dynamics[^.]{0,400}expensive[^.]{0,200}", b, re.I)
    if m:
        hit = (pmcid, t, d, m.group(0))
        break
print("   ", "HIT" if hit else "MISS", (hit[3][:420] + "…") if hit else "（未找到原句，需回读 bioRxiv 正文）")
if hit:
    print("   来源:", hit[0], hit[1], hit[2])
