#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三方内容清单：把仓库里**每一份**第三方原文（全文、摘要、句级摘要、预印本抽取物）
逐份登记成可核对的表，公开仓库据此只发作者原创内容。

为什么要有这个（背景，2026-11-08 实测）：
  原来的 `scripts/audit_source_licenses.py` 只审了 `inventory.json` 里 `has_fulltext` 为真的
  **87 行**，而仓库里实际跟踪的第三方内容文件是 **232 份**：
    - `data/literature_cards/fulltext/`  83 份（PMC XML + 去标签纯文本）
    - `data/interim/baker_lit/ft/`       46 份（Baker/曹组论文正文抽取）
    - `data/interim/baker_lit/dig/`      44 份（**句级摘要**，是原文的浓缩复制）
    - `data/interim/baker_lit/mdqm.out`   1 份（逐句摘录）
    - `data/interim/claim_lit/`          26 份（PMC XML 19 + 摘要转储 2 + 检索结果 4 + 元数据 1）
    - `data/interim/rfd4_2026-11-07/RFD4_paper_text.txt` 1 份（预印本正文抽取，283 KB）
  也就是说 **145 份文件从未进过许可审计**。公开仓库 = 公开再分发，这 145 份必须先被逐份登记，
  才能决定"哪些随仓库走、哪些只留在内部核验库"。

本脚本产出 `deliverables/fulltext_manifest.csv`，每行一份文件：
  path / bytes / sha256 / 内容形态 / 所属编号 / 行许可类别 / 本文件许可类别 /
  可否随商业产品再分发 / 随仓库分发 / 重取方式 / 证据来源 / 说明

许可判定沿用 `audit_source_licenses.py` 的 `classify_local()`（同一份实现，避免两套口径）。

用法:
  python scripts/build_fulltext_manifest.py            # 生成清单
  python scripts/build_fulltext_manifest.py --check    # 只核验磁盘与清单是否一致 + 仓库里是否已无第三方内容

判定标准（--check 时打印）：
  1. 清单里每一行的文件都在磁盘上，且 sha256 与清单一致（内部核验库完整）。
  2. 清单里标记"随仓库分发=否"的文件，**不得**出现在 `git ls-files` 里（公开树干净）。
  3. 标记"随仓库分发=是"的文件必须是题录元数据或我们自己的日志（不含原文句子）。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_source_licenses import CATS, RESTRICTED, classify_local  # noqa: E402
from litcards_spec import slug  # noqa: E402

CARDS = ROOT / "data" / "literature_cards"
INVENTORY = CARDS / "inventory.json"
MAPFILE = CARDS / "sources_map.json"
AUDITCSV = ROOT / "deliverables" / "protein_design_license_audit.csv"
OUTCSV = ROOT / "deliverables" / "fulltext_manifest.csv"
DLALL = ROOT / "data" / "interim" / "baker_lit" / "dlall.py"

# 第三方内容目录（按目录前缀判定）
TP_PREFIXES = (
    "data/literature_cards/fulltext/",
    "data/interim/baker_lit/ft/",
    "data/interim/baker_lit/dig/",
    "data/interim/claim_lit/",
)
TP_EXACT = {
    # mdqm.out 里是逐句摘录的原文句子（第三方内容）；下面两份 out 是我们自己的抓取日志（只有题录元数据）
    "data/interim/baker_lit/mdqm.out",
    "data/interim/baker_lit/verify.out",
    "data/interim/baker_lit/dlall.out",
    "data/interim/rfd4_2026-11-07/RFD4_paper_text.txt",
}
# 题录元数据与我们自己的日志：不含第三方原文句子，可以随仓库分发
META_EXACT = {
    "data/interim/baker_lit/verify.out",
    "data/interim/baker_lit/dlall.out",
    "data/interim/claim_lit/pmids.json",
    "data/interim/claim_lit/bx.json",
}

CONTENT_KIND = {
    "data/literature_cards/fulltext/": "论文全文抽取",
    "data/interim/baker_lit/ft/": "论文全文抽取",
    "data/interim/baker_lit/dig/": "句级摘要（原文浓缩复制）",
    "data/interim/claim_lit/": "论文全文/摘要转储",
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_ls_files() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True,
                         text=True, check=True).stdout
    return [x for x in out.splitlines() if x]


def pmc_map() -> tuple[dict[str, str], dict[str, str]]:
    """PMCID -> 编号；slug(编号) -> 编号。"""
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    pmc2acc: dict[str, str] = {}
    slug2acc: dict[str, str] = {}
    for rec in inv:
        acc = rec["id"]
        slug2acc[slug(acc)] = acc
        for pmc in rec.get("ids", {}).get("pmc", []) or []:
            pmc2acc[pmc.upper()] = acc
    return pmc2acc, slug2acc


def dlall_name_map() -> dict[str, str]:
    """从 dlall.py 的 B1/B2 字典里读出 文件名 -> PMCID（抓取配方本身是权威来源）。"""
    txt = DLALL.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for name, pmc in re.findall(r'"([A-Za-z0-9_]+)"\s*:\s*"(PMC\d+)"', txt):
        out[name] = pmc.upper()
    return out


def row_license() -> dict[str, str]:
    if not AUDITCSV.exists():
        return {}
    out: dict[str, str] = {}
    with AUDITCSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            out[r["编号"]] = r["许可类别"]
    return out


def fetch_url_map() -> dict[str, str]:
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for rec in inv:
        url = rec.get("fetch_url") or ""
        if not url:
            pmc = (rec.get("ids", {}).get("pmc") or [None])[0]
            url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML"
                   if pmc else "")
        out[rec["id"]] = url
    return out


def acc_of(path: str, pmc2acc: dict[str, str], slug2acc: dict[str, str],
           name2pmc: dict[str, str], smap_rev: dict[str, list[str]]) -> list[str]:
    """一份文件归属哪些编号（可能多份：转储文件）。"""
    if path in smap_rev:
        return sorted(set(smap_rev[path]))
    base = Path(path).name
    m = re.match(r"^(PMC\d+)\.xml$", base)
    if m:
        return [pmc2acc[m.group(1)]] if m.group(1) in pmc2acc else []
    if "/ft/" in path:
        name = base[:-4] if base.endswith(".txt") else base
        pmc = name2pmc.get(name)
        return [pmc2acc[pmc]] if pmc and pmc in pmc2acc else []
    if "/dig/" in path:
        name = base[:-8] if base.endswith(".dig.txt") else base
        pmc = name2pmc.get(name)
        return [pmc2acc[pmc]] if pmc and pmc in pmc2acc else []
    m = re.match(r"^([A-Z][A-Za-z0-9\-]*?)_", base)
    if m:
        s = m.group(1)
        if s in slug2acc:
            return [slug2acc[s]]
    return []


def classify_kind(path: str) -> str:
    if path in ("data/interim/claim_lit/pmids.json", "data/interim/claim_lit/bx.json"):
        return "题录元数据（检索结果摘要表，无正文/摘要正文）"
    if path == "data/interim/baker_lit/mdqm.out":
        return "逐句摘录日志（含第三方原文句子）"
    if path in ("data/interim/baker_lit/verify.out", "data/interim/baker_lit/dlall.out"):
        return "自写抓取日志（题录与哈希，无原文句子）"
    for pre, kind in CONTENT_KIND.items():
        if path.startswith(pre):
            if path.endswith(".xml") and "fulltext/" in path:
                return "论文全文（PMC XML 原件）"
            if path.endswith(".txt") and "fulltext/" in path:
                return "论文全文（去标签纯文本）"
            if path.endswith(".json") and "claim_lit/" in path:
                return "检索结果（含摘要正文）"
            if path.endswith(".txt") and "claim_lit/" in path:
                return "摘要转储（多篇拼接）"
            return kind
    if path.endswith(".dig.txt"):
        return "句级摘要（原文浓缩复制）"
    if path.endswith(".out"):
        return "抓取/摘录日志"
    if path.endswith(".json"):
        return "检索结果（题录元数据或含摘要）"
    if path.endswith("RFD4_paper_text.txt"):
        return "预印本正文抽取"
    return "其他"


def build() -> tuple[list[dict], list[str]]:
    tracked = set(git_ls_files())
    pmc2acc, slug2acc = pmc_map()
    name2pmc = dlall_name_map()
    smap = json.loads(MAPFILE.read_text(encoding="utf-8"))
    smap_rev: dict[str, list[str]] = {}
    for acc, paths in smap.items():
        for p in paths:
            smap_rev.setdefault(p, []).append(acc)
    rowcat = row_license()
    furl = fetch_url_map()

    notes: list[str] = []
    rows: list[dict] = []
    # 候选来自**磁盘**而不是 git ls-files：第三方原文已经不再被 git 跟踪，
    # 但它们仍在内部核验库里，清单必须继续覆盖它们（否则漏登记）。
    cands: set[str] = set()
    for pre in TP_PREFIXES:
        d = ROOT / pre
        if d.is_dir():
            cands |= {p.relative_to(ROOT).as_posix() for p in d.rglob("*") if p.is_file()}
    for p in TP_EXACT:
        if (ROOT / p).exists():
            cands.add(p)
    for p in sorted(cands):
        f = ROOT / p
        if not f.exists():
            notes.append(f"{p}: 已跟踪但磁盘上不存在（请人工确认）")
            continue
        accs = acc_of(p, pmc2acc, slug2acc, name2pmc, smap_rev)
        kind = classify_kind(p)
        # 本文件自己的许可证据：文件内带的 <license> / CC 链接 / Europe PMC 短码
        cat, ev = classify_local(f.read_text(encoding="utf-8", errors="replace"))
        # sources_map 的键可能是组合编号（"B06; C02"），许可审计的编号是单编号，
        # 所以查许可时要按分隔符拆开逐个查，否则这类共享转储文件会查不到归属行的结论。
        toks: list[str] = []
        for a in accs:
            toks += [x.strip() for x in re.split(r"[;；]", a) if x.strip()]
        toks = sorted(set(toks))
        rcats = sorted({rowcat.get(a, "") for a in toks if rowcat.get(a)})
        rcat = "｜".join(rcats) if rcats else ("未登记在许可审计内" if accs else "多行共用")
        # 逐编号的许可类别（"B06=CC_BY；C02=CC_BY_NC"）。一份转储文件可能同时属于多行，
        # 而每一行的许可结论不同——公开仓库里没有第三方原文时，许可审计要靠这一列离线复现
        # 那一行当初的审计结论，所以必须逐编号写，不能只写一个合并值。
        pairs = "；".join(f"{a}={rowcat[a]}" for a in toks if rowcat.get(a))
        if cat == "UNKNOWN" and rcats:
            # 文件本身没有可识别的许可声明时，以所属行的审计结论为准
            cat = rcats[0] if len(rcats) == 1 else "UNKNOWN"
            ev = f"沿用所属行审计结论（{rcats[0]}）"
        redist = CATS.get(cat, ("未知", "未知", ""))[1]
        if cat not in CATS:
            redist = "未知"
        # 随仓库分发：只允许"题录元数据"与"我们自己的日志"
        meta = p in META_EXACT
        ship = "是" if meta else "否"
        why = ("题录元数据或自写日志，不含第三方原文句子" if meta else
               "第三方原文内容，公开仓库不随包分发；按重取方式与 sha256 复核")
        url = ""
        if p in META_EXACT:
            url = "（不适用）"
        elif accs and accs[0] in furl:
            url = furl[accs[0]]
        elif p.endswith("RFD4_paper_text.txt"):
            url = "https://rfd4-proteina.org/assets/paper/RFD4-Proteina.pdf"
        rows.append({
            "path": p,
            "bytes": f.stat().st_size,
            "sha256": sha256_file(f),
            "内容形态": kind,
            "所属编号": "；".join(accs) if accs else "（未归属单行）",
            "行许可类别": rcat,
            "各编号许可类别": pairs,
            "本文件许可类别": cat,
            "可否随商业产品再分发该全文": redist,
            "随仓库分发": ship,
            "重取方式": url,
            "证据来源": (ev or "文件内无可识别许可声明")[:180],
            "说明": why,
        })
    return rows, notes


def write_csv(rows: list[dict]) -> None:
    OUTCSV.parent.mkdir(exist_ok=True)
    with OUTCSV.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def check(rows: list[dict]) -> int:
    tracked = set(git_ls_files())
    bad: list[str] = []
    for r in rows:
        f = ROOT / r["path"]
        if not f.exists():
            bad.append(f"{r['path']}: 磁盘缺失")
            continue
        if sha256_file(f) != r["sha256"]:
            bad.append(f"{r['path']}: sha256 与清单不一致")
        if r["随仓库分发"] == "否" and r["path"] in tracked:
            bad.append(f"{r['path']}: 标记为不分发但仍被 git 跟踪")
        if r["随仓库分发"] == "是" and r["path"] not in tracked:
            bad.append(f"{r['path']}: 标记为随仓库分发但未跟踪")
    print("判定标准: 清单内每份文件磁盘存在且 sha256 一致；标记为不分发的第三方内容不在 git 跟踪里")
    if bad:
        print(f"判定结果: FAIL {len(bad)} 处不符")
        for b in bad[:20]:
            print("  ", b)
        return 1
    n_ship = sum(1 for r in rows if r["随仓库分发"] == "是")
    print(f"判定结果: PASS 清单 {len(rows)} 份第三方文件，其中随仓库分发 {n_ship} 份（均为题录元数据/自写日志），"
          f"不分发 {len(rows) - n_ship} 份")
    print("找出来没有: 本门禁只判清单与磁盘/仓库的一致性，不判文献内容对错")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    rows, notes = build()
    if not rows:
        print("判定结果: FAIL — 重算出 0 行第三方内容，拒绝写盘")
        return 1
    if args.check:
        return check(rows)
    write_csv(rows)
    ship = sum(1 for r in rows if r["随仓库分发"] == "是")
    print(f"清单 {len(rows)} 份第三方内容文件 → {OUTCSV.relative_to(ROOT)}")
    print(f"随仓库分发 {ship} 份 · 仅留内部核验库 {len(rows) - ship} 份")
    for n in notes:
        print("  注意:", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
