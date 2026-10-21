import sys, os, glob, re, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, r"A:\Data\MD\projects\protein-design-screening-20261016\data\interim\baker_lit")
from lit import digest_sentences
BASE = r"A:\Data\MD\projects\protein-design-screening-20261016\data\interim\baker_lit"
os.makedirs(os.path.join(BASE, "dig"), exist_ok=True)
for f in sorted(glob.glob(os.path.join(BASE, "ft", "*.txt"))):
    n = os.path.basename(f)[:-4]
    out = os.path.join(BASE, "dig", n + ".dig.txt")
    if os.path.exists(out):
        continue
    ks = digest_sentences(f)
    open(out, "w", encoding="utf-8").write("\n".join("- " + k for k in ks))
    print(n, len(ks))
