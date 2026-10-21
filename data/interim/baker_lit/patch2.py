p = r"A:\Data\MD\projects\protein-design-screening-20261016\sources\baker.md"
t = open(p, encoding="utf-8").read()
subs = [
 ("- Nature, 2026（在线 2025-12），649:183-193（2024-03 预印本 10.1101/2024.03.14.585103）",
  "- Nature, 649:183-193（Crossref issued=2025，EPMC pubYear=2026；预印本 10.1101/2024.03.14.585103 ✅）"),
 ("- Nature, 2026（在线 2025-12），649:246-253",
  "- Nature, 649:246-253（Crossref issued=2025，EPMC pubYear=2026）"),
 ("- Nature Methods, 2026（在线 2025），23:96-105",
  "- Nature Methods, 23:96-105（Crossref issued=2025，EPMC 归入 2026 卷期）"),
 ("- Nature, 2025（在线 2024-12），638:553-561",
  "- Nature, 638:553-561（Crossref issued=2024，EPMC pubYear=2025）"),
 ("- Nature, 2025（在线 2024-12），638:546-552",
  "- Nature, 638:546-552（Crossref issued=2024，EPMC pubYear=2025）"),
 ("- Nature, 2025, 639:225-231（预印本 10.1038/s41586-024-08393-x；Research Square 2024-05-17）",
  "- Nature, 2025, 639:225-231（Research Square 预印本 2024-05-17，见全文 'Previous version available' 声明）"),
 ("- Nature, 2024, 638:796-804", "- Nature, 638:796-804（Crossref issued=2024，EPMC pubYear=2025）"),
]
missing = []
for a, b in subs:
    if a in t:
        t = t.replace(a, b, 1)
    else:
        missing.append(a[:50])
open(p, "w", encoding="utf-8").write(t)
print("applied:", len(subs) - len(missing))
print("missing:", missing)
