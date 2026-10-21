import sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, r"A:\Data\MD\projects\protein-design-screening-20261016\data\interim\baker_lit")
from lit import download

B1 = {
 "rfdiffusion2023": "PMC10468394", "binderDL2023": "PMC10163288", "helicalpeptide2024": "PMC10849960",
 "antibodyRFdiff": "PMC12727541", "nanocage_hier2025": "PMC11821544", "serinehydrolase2025": "PMC12288761",
 "metallohydrolase2026": "PMC12727532", "rfdiff2_natmeth": "PMC12791007", "luciferase2023": "PMC9946828",
 "accelscaling2026": "PMC13586242", "mp3seq2024": "PMC11511666", "snakvenom2025": "PMC11882462",
 "tnfr2024": "PMC12416549", "idp_binder2025": "PMC12367549", "macrocyle2025": "PMC12643943",
 "switches2019": "PMC6733528", "smallfolds2022": "PMC9684540", "integrin_miniprot2023": "PMC10500007",
 "immune_receptor_binder2025": "PMC11865580", "beta_pairing2026": "PMC12852815",
 "quasisym2comp2026": "PMC13412984", "energyfunc2026": "PMC13124059", "endocytosis2025": "PMC11839401",
 "pHC_binders2025": "PMC13077772",
}
B2 = {
 "cao2022": "PMC9117152", "proteinmpnn2022": "PMC9997061", "kemp2025": "PMC12310539",
 "motifscaffold2026": "PMC12727513", "md_jctc2019": "PMC7532806", "hallucination2021": "PMC9293396",
 "placer2025": "PMC12625923", "confdyn2023": "PMC10161014", "oligomorph2025": "PMC12170342",
 "helicalbundle_pH2023": "PMC10578055", "amyloidtraps2024": "PMC11288891", "metathase2025": "PMC12638248",
 "smallmol_family2026": "PMC13194776", "fap2021": "PMC7870846", "nirFAP2026": "PMC13560888",
 "chlorophyll2024": "PMC11213709", "dnabinding2025": "PMC12618268", "repeatprot2023": "PMC10643118",
 "nanopore2024": "PMC11549965", "betaBarrel2023": "PMC10089152", "memprot_analogue2024": "PMC11236705",
 "autotwo_comp2024": "PMC10990136",
}
download(B1)
download(B2)
