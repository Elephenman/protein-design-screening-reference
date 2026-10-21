# -*- coding: utf-8 -*-
"""
verify_gate.py — 交付前机械门禁：对 CSV 每一行的 DOI 走 Crossref 实解析，
并把 Crossref 返回标题与 CSV 标题做 token 重合度比对（防串号/防笔误）。
输出 gate_report.md + gate.json。
"""
import csv, json, os, re, sys, time, urllib.request, urllib.error, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
CSVIN = os.path.join(HERE, "protein_design_literature.csv")
OUT_MD = os.path.join(HERE, "gate_report.md")
OUT_JSON = os.path.join(HERE, "gate.json")

STOP = set("de novo design of with and the a an protein proteins using for in on study".split())


def tokens(s):
    return {w for w in re.findall(r"[a-z0-9µé]+", s.lower()) if w not in STOP and len(w) > 2}


def fetch(doi, tries=3):
    # Zenodo/DataCite 前缀不在 Crossref 注册，走 Zenodo API
    if doi.startswith("10.5281/zenodo."):
        rec = doi.split("zenodo.")[-1]
        u = "https://zenodo.org/api/records/" + rec
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "lit-gate/1.0"})
            with urllib.request.urlopen(req, timeout=25) as r:
                md = json.loads(r.read().decode("utf-8"))["metadata"]
            return {"message": {"title": [md.get("title", "")],
                                "container-title": ["Zenodo 技术报告（非同行评议）"],
                                "published-online": {"date-parts": [[int(md.get("publication_date", "1970")[:4])]]}}}, None
        except Exception as e:
            return None, f"zenodo_{type(e).__name__}"
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "lit-gate/1.0 (mailto:research@example.org)"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8")), None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, "404_not_found"
            time.sleep(1.5 * (k + 1))
        except Exception as e:
            time.sleep(1.5 * (k + 1))
            err = f"{type(e).__name__}:{e}"
    return None, "unreachable_after_retries"


def main():
    from concurrent.futures import ThreadPoolExecutor
    rows = list(csv.DictReader(open(CSVIN, encoding="utf-8-sig")))
    indexed = list(enumerate(rows, 1))

    def work(item):
        n, r = item
        doi = r["DOI(doi)"].strip()
        rec = {"id": r["编号(id)"], "csv_title": r["标题(title)"], "doi": doi,
               "group": r["人物组(group)"], "csv_year": r["年份(year)"]}
        if not doi or doi == "未记录":
            rec["status"] = "no_doi(价目表/不适用)"
            return rec
        data, err = fetch(doi)
        if err:
            rec["status"] = "FAIL_" + err
        else:
            m = data["message"]
            ct = (m.get("title") or [""])[0]
            a = tokens(ct); b = tokens(r["标题(title)"])
            jac = len(a & b) / max(1, len(a | b))
            yr = ""
            for f in ("published-print", "published-online", "issued"):
                if m.get(f, {}).get("date-parts"):
                    yr = str(m[f]["date-parts"][0][0]); break
            reg = "Zenodo/DataCite" if doi.startswith("10.5281/") else "Crossref"
            rec.update(status="OK" if jac >= 0.3 else "TITLE_MISMATCH",
                       registry=reg,
                       crossref_title=ct, crossref_year=yr, overlap=round(jac, 3),
                       container=(m.get("container-title") or [""])[0])
        return rec

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(work, indexed))

    json.dump(results, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ok = sum(1 for x in results if x["status"] == "OK")
    mismatch = [x for x in results if x["status"] == "TITLE_MISMATCH"]
    fail = [x for x in results if x["status"].startswith("FAIL")]
    nod = [x for x in results if x["status"].startswith("no_doi")]
    yr_diff = [x for x in results if x["status"] == "OK" and x.get("crossref_year") and x["csv_year"] not in ("", "未记录")
               and abs(int(x["crossref_year"]) - int(x["csv_year"])) > 1]
    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write("# CSV 文献表机械门禁报告\n\n")
        fh.write(f"- 总行数：**{len(results)}**\n")
        fh.write(f"- DOI 经 Crossref 解析且标题重合度 ≥0.3：**{ok}**\n")
        fh.write(f"- 标题重合度 <0.3（需人工确认是否串号）：**{len(mismatch)}**\n")
        fh.write(f"- DOI 解析失败（404/网络）：**{len(fail)}**\n")
        fh.write(f"- 无 DOI 行（价目表/公司页等）：**{len(nod)}**\n")
        fh.write(f"- 年份与 Crossref 记录相差 >1 年：**{len(yr_diff)}**\n\n")
        if mismatch:
            fh.write("## 需人工确认的标题重合度低条目\n\n")
            for x in mismatch:
                fh.write(f"- [{x['id']}] {x['doi']} 重合度={x['overlap']}\n  - CSV: {x['csv_title'][:90]}\n  - Crossref: {x.get('crossref_title','')[:90]}\n")
        if fail:
            fh.write("\n## 解析失败条目\n\n")
            for x in fail:
                fh.write(f"- [{x['id']}] {x['doi']} → {x['status']}\n")
        if nod:
            fh.write("\n## 无 DOI 行\n\n")
            for x in nod:
                fh.write(f"- [{x['id']}] {x['csv_title'][:70]}（{x['status']}）\n")
        if yr_diff:
            fh.write("\n## 年份差异（在线年 vs 印刷年，通常无害）\n\n")
            for x in yr_diff:
                fh.write(f"- [{x['id']}] CSV={x['csv_year']} Crossref={x['crossref_year']} {x['doi']}\n")
    print(f"rows={len(results)} OK={ok} TITLE_MISMATCH={len(mismatch)} FAIL={len(fail)} no_doi={len(nod)} year_diff={len(yr_diff)}")
    print("报告:", OUT_MD)


if __name__ == "__main__":
    main()
