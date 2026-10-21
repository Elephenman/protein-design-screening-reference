import re, glob, os, sys, warnings
warnings.filterwarnings("ignore")
FT = r"A:\Data\MD\projects\protein-design-screening-20261016\data\interim\baker_lit\ft"
MD = re.compile(r"(molecular dynamics|GROMACS|Gromacs|AMBER|OpenMM|LLDN |Langevin|MM/PBSA|MM-PBSA|free energy perturbat|metadynamics|umbrella sampling|explicit solvent|equilibrat\w* (for|over) \d|100 ns|molecular-mechanical)", re.I)
QM = re.compile(r"(density functional|DFT\b|QM/MM|quantum mechanic|quantum chemistr|ab initio|transition state|theozyme|B3LYP|M06-2X|Gaussian|TD-DFT|coupled cluster|CC2|MP2)", re.I)
FILTER = re.compile(r"(filter|select|screen|priorit|enrich|rank|threshold|cutoff|pass)", re.I)
for f in sorted(glob.glob(os.path.join(FT, "*.txt"))):
    n = os.path.basename(f)[:-4]
    txt = re.sub(r"\s+", " ", open(f, encoding="utf-8").read())
    sents = re.split(r"(?<=[.!?])\s+", txt)
    md = [s for s in sents if MD.search(s) and len(s) < 500]
    qm = [s for s in sents if QM.search(s) and len(s) < 500]
    if not md and not qm:
        print("\n#####", n, "| MD:0 QM:0")
        continue
    print("\n#####", n, "| MD:%d QM:%d" % (len(md), len(qm)))
    for s in md[:4]:
        tag = "FILTERISH" if FILTER.search(s) else "analysis"
        print("   MD[%s] %s" % (tag, s[:340]))
    for s in qm[:4]:
        tag = "FILTERISH" if FILTER.search(s) else "analysis"
        print("   QM[%s] %s" % (tag, s[:340]))
