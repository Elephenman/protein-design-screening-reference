# -*- coding: utf-8 -*-
"""spot_check.py — 对 report.md 里最关键的原句/数字做独立复核。
按 DOI 解析 PMCID（Europe PMC core 记录）-> 抓 OA 全文 XML -> 搜原句片段。
输出每条断言 PASS / PARTIAL / NOTFOUND / NO_OA_FULLTEXT。
"""
import json, re, sys, time, urllib.request, urllib.parse

SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={}&format=json&pageSize=3&resultType=core"
FT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{}/fullTextXML"

CLAIMS = [
    ("C1 Bennett2023 AF2过滤 30 GPU-秒 与 2.3% 通过率", "10.1038/s41467-023-38328-5",
     ["30 GPU-seconds", "2.3% of designs pass"]),
    ("C2 Bennett2023 pAE_interaction 阈值", "10.1038/s41467-023-38328-5", ["pAE_interaction"]),
    ("C3 Bennett2023 命中率近 10 倍提升", "10.1038/s41467-023-38328-5", ["nearly 10-fold"]),
    ("C4 RFdiffusion2023 总体实验成功率 19% 与 每靶 <100 设计", "10.1038/s41586-023-06415-8",
     ["success rate", "100 designs"]),
    ("C5 Cao2022 15,000–100,000 与 fewer than 10 与 100,000 CPU hours", "10.1038/s41586-022-04654-9",
     ["15,000", "fewer than 10", "100,000 CPU hours"]),
    ("C6 Science2020 12 of the de novo designs 与 11 of the 12", "10.1126/science.abd9909",
     ["12 of the de novo", "11 of the 12"]),
    ("C7 CAAMO eLife2026 five out of the six (~83%)", "10.7554/eLife.107785",
     ["five out of the six"]),
    ("C8 Gerasimavicius2023 rho 0.26 / 0.28", "10.1002/pro.4688", ["0.26", "0.28"]),
    ("C9 PLACER bioRxiv 否弃 MD 作筛器的原句", "10.1101/2024.08.29.610411",
     ["molecular dynamics", "expensive"]),
    ("C10 Rocklin2017 6% -> 47%", "10.1126/science.aan0693", ["47%"]),
    ("C11 抗体设计 0% 到 2% 成功率", "10.1038/s41586-025-09721-5", ["0% to 2%"]),
    ("C12 综述命中率共识 1% 到 10%", "10.34133/csbj.0070", ["1% to 10%"]),
]


def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "spotcheck/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return "__ERR__ " + type(e).__name__ + ":" + str(e)


def resolve_pmcid(doi):
    q = urllib.parse.quote('DOI:"%s"' % doi)
    j = get(SEARCH.format(q))
    try:
        d = json.loads(j)
    except Exception:
        return None, "search_fail"
    for rec in d.get("resultList", {}).get("result", []):
        if rec.get("pmcid"):
            return rec["pmcid"], rec
    return None, d.get("hitCount")


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[\r\n\t ]+", " ", s).strip()


def main():
    lines = []
    for name, doi, needles in CLAIMS:
        pmcid, meta = resolve_pmcid(doi)
        if not pmcid:
            # 退回到摘要
            j = get(SEARCH.format(urllib.parse.quote("DOI:" + doi)))
            blurb = ""
            try:
                r = json.loads(j)["resultList"]["result"][0]
                blurb = r.get("abstractText", "")
            except Exception:
                pass
            blob = clean(blurb)
            src = "摘要"
        else:
            blob = clean(get(FT.format(pmcid)))
            src = pmcid + " 全文"
        if blob.startswith("__ERR__") or len(blob) < 200:
            lines.append((name, "NO_OA_FULLTEXT", doi, src, ""))
            continue
        hits = [n for n in needles if n in blob]
        st = "PASS" if len(hits) == len(needles) else ("PARTIAL" if hits else "NOTFOUND")
        ctx = ""
        if hits:
            i = blob.find(hits[0])
            ctx = blob[max(0, i - 170):i + 170]
        lines.append((name, st, doi, src, ctx))
        time.sleep(0.3)

    with open(__file__.replace("spot_check.py", "spot_check.out"), "w", encoding="utf-8") as fh:
        for name, st, doi, src, ctx in lines:
            fh.write(f"{st}\t{name}\t{doi}\t{src}\nCTX: …{ctx}…\n\n")
    for name, st, doi, src, ctx in lines:
        print(f"[{st}] {name}\n     来源={src}  DOI={doi}\n     …{ctx[:300]}…\n")
    npass = sum(1 for x in lines if x[1] == "PASS")
    print(f"汇总: PASS {npass}/{len(lines)}；其余见 spot_check.out")


if __name__ == "__main__":
    main()
