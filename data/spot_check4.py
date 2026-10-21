# -*- coding: utf-8 -*-
"""
spot_check4.py — 交付前最后一轮定点取证（三件事）：
  1) 撤销误引的证据：PMID 33956864 实际是哪篇论文；DOI 10.1093/bioinformatics/btab35 是否解析。
  2) PLACER 'MD 太贵' 原句 + 丝氨酸水解酶 1.6%/5.2%/84% 原句（PNAS / Science 正文）。
  3) RFdiffusion2 的 11/96 与 41/41 原句（Nat Methods 正文）——纠正我自己一次误判。
"""
import re, json, urllib.request, urllib.parse

E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
FT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{}/fullTextXML"


def get(u):
    try:
        r = urllib.request.Request(u, headers={"User-Agent": "chk4/1.0"})
        return urllib.request.urlopen(r, timeout=50).read().decode("utf-8", "replace")
    except Exception as e:
        return "__ERR__" + type(e).__name__ + ":" + str(e)


def clean(s):
    return re.sub(r"[\r\n\t ]+", " ", re.sub(r"<[^>]+>", " ", s))


def show(label, pat, blob, width=260):
    m = re.search(pat, blob, re.I)
    print(("  [HIT ] " if m else "  [MISS] ") + label)
    if m:
        print("         …" + blob[max(0, m.start() - 130):m.start() + width] + "…")


print("== 1) 误引核查 ==")
show("DOI 10.1093/bioinformatics/btab35 是否可解析（期望 404）", r"__ERR__HTTPError",
     get("https://api.crossref.org/works/10.1093/bioinformatics/btab35"), 120)
x = get(E + "efetch.fcgi?db=pubmed&id=33956864&retmode=xml")
t = re.findall(r"<ArticleTitle>(.*?)</ArticleTitle>", x, re.S)
print("  PMID 33956864 真实标题：", (t[0][:120] if t else "取不到"))
print("  → 与'氢键网络深度学习设计'无关，故 build 阶段该行的 DOI/PMID 判为误录并已撤销")

print("\n== 2) PLACER 与丝氨酸水解酶（已复核原句） ==")
pnas = clean(get(FT.format("PMC12625923")))
show("PLACER：MD 被成本否弃作主筛器", r"computationally expensive and cannot be applied to large numbers of designs", pnas)
sci = clean(get(FT.format("PMC12288761")))
show("丝氨酸水解酶：仅 1.6% 过 AF2 的设计被 PLACER 判为预组织", r"Only 1\.6% of round 2 designs[^.]{0,150}", sci)
show("丝氨酸水解酶：末端 45→38（84%）", r"45 two-state filtered designs[^.]{0,180}", sci)
show("丝氨酸水解酶：两轮投测量 129 / 192", r"129 and 192 designs", sci)
show("丝氨酸水解酶：活性率 3%→17%", r"from 3% to 17%", sci)
show("丝氨酸水解酶：DFT 定过渡态", r"B3LYP-D3\(BJ\)/6-31G", sci)

print("\n== 3) RFdiffusion2（纠正我自己的误判） ==")
rfd = clean(get(FT.format("PMC12791007")))
show("RFdiffusion2：第二批 96 个里 11 个功能酶", r"we identified 11 functional enzymes[^.]{0,160}", rfd)
show("RFdiffusion2：首批 96 个里 3 与 5 个功能酶", r"identified three functional enzymes[^.]{0,200}", rfd)
show("RFdiffusion2：in silico 41/41 vs 16/41", r"for 41/41 cases while RFdiffusion achieves 16/41", rfd)
show("RFdiffusion2：kcat/KM 53,000 与 16,000", r"53,000", rfd)
