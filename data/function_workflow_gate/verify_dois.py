import json, urllib.request, urllib.parse, time

BASE = "A:/Data/MD/projects/protein-design-screening-20261016/tmp/cr/"
dois = [l.strip() for l in open(BASE + "dois.txt", encoding="utf-8") if l.strip()]
out = open(BASE + "doi_verify.txt", "w", encoding="utf-8", buffering=1)
okc = 0
for d in dois:
    resolved = False
    failed = False
    for attempt in range(5):
        try:
            url = "https://api.crossref.org/works/" + urllib.parse.quote(d, safe="")
            req = urllib.request.Request(url, headers={"User-Agent": "doi-verify/1.0"})
            m = json.load(urllib.request.urlopen(req, timeout=25))["message"]
            out.write("OK   %s | %s\n" % (d, (m.get("title") or ["?"])[0][:80]))
            okc += 1
            resolved = True
            break
        except Exception as e:
            r = repr(e)
            if "429" in r or "timed out" in r.lower():
                time.sleep(6)
                continue
            out.write("FAIL %s | %s\n" % (d, r[:70]))
            failed = True
            break
    if not resolved and not failed:
        out.write("FAIL %s | exhausted retries\n" % d)
    time.sleep(0.4)
out.write("SUMMARY OK=%d / %d\n" % (okc, len(dois)))
out.close()
