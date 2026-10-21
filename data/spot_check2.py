# -*- coding: utf-8 -*-
"""spot_check2.py — 对报告里最吃重的数字做宽松匹配复核（容忍排版差异）。"""
import re, sys, json, urllib.request
from concurrent.futures import ThreadPoolExecutor

FT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{}/fullTextXML"
SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={}&format=json&pageSize=5&resultType=core"

JOBS = [
    ("Bennett2023 AF2 过滤成本与通过率", "PMC10163288", [r"GPU[- ]?seconds?", r"2\.3\s*%"]),
    ("RFdiffusion2023 19% 与 每靶<100 设计", "PMC10468394", [r"success rate[^.]{0,120}19\s*%", r"19\s*%", r"fewer than\s*100\s*designs"]),
    ("CAAMO eLife2026 five out of the six", "PMC13368180", [r"five out of the six", r"8[0-9]\s*%", r"success rate"]),
    ("Gerasimavicius2023 rho 0.26/0.28", "PMC10413815", [r"0\.26", r"0\.28", r"rho values"]),
    ("Rocklin2017 6% -> 47%", "PMC5568797", [r"from 6% to 47%", r"47\s*%"]),
    ("PLACER 'MD 太贵不能用于大量设计' 原句", None, [r"cannot be applied to large numbers of designs"]),
]


def get(url, tries=2):
    last = ""
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "spotcheck2/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = f"{type(e).__name__}:{e}"
    return "__ERR__ " + last


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[\r\n\t ]+", " ", s)


def run(job):
    name, pmcid, pats = job
    if pmcid:
        blob = clean(get(FT.format(pmcid)))
    else:
        q = urllib.parse.quote('FULL_TEXT:"cannot be applied to large numbers of designs"')
        j = get(SEARCH.format(q))
        blob = ""
        try:
            res = json.loads(j)["resultList"]["result"]
            ids = [r.get("pmcid") for r in res if r.get("pmcid")]
            blob = clean(" ".join(get(FT.format(i)) for i in ids[:2]))
            name += " | 命中记录数=" + str(len(res)) + " | " + "; ".join(
                (r.get("title", "")[:60] + " [" + (r.get("doi") or "") + "]") for r in res[:3])
        except Exception as e:
            blob = "__ERR__ " + str(e) + " :: " + j[:200]
    out = []
    for p in pats:
        m = re.search(p, blob, re.I)
        out.append((p, "HIT" if m else "MISS",
                    blob[max(0, m.start() - 150):m.start() + 200] if m else ""))
    return name, out, len(blob)


import urllib.parse
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=6) as ex:
        for name, res, size in ex.map(run, JOBS):
            allhit = all(r[1] == "HIT" for r in res)
            print(f"\n### {'PASS' if allhit else 'REVIEW'} — {name}  (文本长度 {size})")
            for pat, st, ctx in res:
                print(f"  [{st}] /{pat}/")
                if ctx:
                    print(f"        …{ctx.strip()[:320]}…")
