#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给**调研底稿**（sources/*.md）里的逐字引句设"引用预算"，与卡片用同一套规则。

为什么（2026-11-08 实测）：
  卡片里的引句已经按许可类别截短过（`scripts/apply_quote_budget.py`），但四份调研底稿
  里还有 74,729 字符的逐字引句，其中相当一部分来自同一批许可受限的来源。
  公开仓库里这两类内容都是"我们自己写的文档里复制了第三方正文"，口径必须一致，
  否则"卡里截了、底稿里留着"等于没截。

规则与卡片完全一致（只对**许可受限来源**生效，CC BY / CC0 等可再分发的行原样保留）：
  1. 单条引句 ≤ 100 字符（句号 / 分号 / 冒号 / 逗号 / 空格边界截断，不切断单词，
     也不落在 markdown 强调段中间）；
  2. 同一份底稿对同一来源行的引句总量 ≤ 600 字符；超出后单条上限降到 50 字符。
  3. 截短后必须仍然**逐字命中该来源的本地全文**（脚本逐条自检）。
     本地没有全文的行（许可从未审计过的 65 行）改为自检"截短结果是原句的前缀"。
  4. **不得破坏卡片的逐字引句核验链**：73 张卡把 sources/*.md 声明为"引句底稿"，
     底稿里的引句一旦被截到卡片引句之前，那张卡就再也核验不了。
     所以每截一条就回头验一遍"这张卡声明的底稿里的每条引句还在不在"，
     不在就把这条还原成原句，并在改动账里写明原因。

归属判定（2026-11-08 实测，把 55 条"查不到出处"的引句压到 55 条里能说清大部分）：
  一级：标题归属——底稿里的 `### [B01] …` / `### [Z16] …` 逐篇小节，
        该小节下的引句就属于这一行（baker 242 条、cao 175 条、zhou 18 条命中）；
  二级：同一行的 DOI / PMID 回连文献总表（claim-90pct 28 条、cost 1 条命中）；
  三级：在该行的第三方全文里做逐字 / 宽松窗口匹配（baker 7 条、cao 6 条、cost 33 条命中）；
  四级：仍查不到 → 记"未归属"。未归属且 ≥ 120 字符的（看起来是完整句子而不是标题或术语）
        按受限口径截短；标题、短术语、检索串保持原样。
  许可类别取自 `deliverables/protein_design_license_audit.csv`；组合编号（"B06; C02"）
  的第二段继承该行类别；总表里有、但审计里没有的行（65 行，只拿到摘要级证据）
  类别记为 UNKNOWN——与卡片脚本一致，UNKNOWN 走受限口径。

用法:
  python scripts/apply_note_quote_budget.py --dry-run   # 只算账
  python scripts/apply_note_quote_budget.py             # 截短并写改动账
  python scripts/apply_note_quote_budget.py --check     # 核验改动账与底稿现状一致

产出: deliverables/quote_budget_notes_ledger.csv
      （逐条：底稿、引句序号、归属方式、来源编号、许可类别、前后字符数、
        是否截短、是否因护住卡引句而保留）
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from litcards_text import norm  # noqa: E402
from apply_quote_budget import (  # noqa: E402
    RESTRICTED, PER_QUOTE_CAP, PER_PAIR_CAP, PER_QUOTE_CAP_TAPER,
    MIN_ALPHA, MIN_QUOTE_CHARS, clean, quotes_of, truncate,
)

CARDS = ROOT / "data" / "literature_cards"
INVENTORY = CARDS / "inventory.json"
AUDITCSV = ROOT / "deliverables" / "protein_design_license_audit.csv"
LITCSV = ROOT / "data" / "protein_design_literature.csv"
NOTES = ROOT / "sources"
LEDGER = ROOT / "deliverables" / "quote_budget_notes_ledger.csv"
MANIFEST = ROOT / "deliverables" / "fulltext_manifest.csv"

# 除了六份调研底稿，还要管住一份**随迁移包发布**的证据台账：
# data/interim/iteration_evidence_2026-11-07.md（AI 投喂包的白名单文件之一）。
# 它逐篇抄了受限来源的整句，属"我们自己的文档里复制了第三方正文"，口径必须一致。
EXTRA_NOTES = [ROOT / "data" / "interim" / "iteration_evidence_2026-11-07.md"]

NOTE_MARK = "引用预算截短"
DECL = re.compile(r"引句底稿[:：]\s*[`\"']?([\w./\\-]+?\.(?:txt|md))")
# 与门禁一致：AGENT_RULES.md / README.md / run.md 不是文献卡，不参与引句核验链
# （AGENT_RULES.md 里那段"引句"其实是 Python 代码片段，按正则会被误当成引句）。
NON_CARDS = {"README.md", "run.md", "AGENT_RULES.md"}

HEAD_RE = re.compile(r"^(#{1,6})\s*(.*)$")
TAG_RE = re.compile(r"^\[([A-Z]{1,2}-?\d+)\]")
# 台账类文档的小节标题写成 `### B17 — Lauko et al. …`（没有方括号），
# 这时归属同样由标题决定，否则整节引句会被记成"未归属"而误截。
TAG_RE2 = re.compile(r"^([A-Z]{1,2}-?\d+)\s*(?:[/、,，]\s*([A-Z]{1,2}-?\d+))?\s*[—–-]\s*")
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s`\]),，、|]+")
# 未归属引句达到这个长度才按受限口径截短（更短的多半是标题、术语、检索串）
UNATTRIBUTED_LONG = 120
# 归属不到具体行时，截短额度按这个虚拟来源记账（总量上限同样生效）
PSEUDO_ACC = "未归属"
# 许可允许再分发的类别：这些行**原样保留**，账上不允许出现"被截短"。
# （实测踩过：一条 CC BY 的引句在归属还没解析到 K39 时按"未归属"被截了，
#   账上写着被截短，文件里却只剩 47 字符——口径与做法对不上。）
REDISTRIBUTABLE = {"CC_BY", "CC_BY_SA", "CC0", "PUBLIC_DOMAIN"}
# 底稿末尾说明块：条数、来源编号、许可类别必须与改动账逐条一致。
BLOCK_RE = re.compile(
    r"本底稿有 (\d+) 条逐字引句被截短（来源编号：(.+?)；许可类别：(.+?)）")
# 说明块里的"逐字命中 / 原句前缀"分账
BLOCK_SPLIT_RE = re.compile(
    r"其中 (\d+) 条截短后仍\*\*逐字命中同一份来源全文\*\*，"
    r"其余 (\d+) 条为\*\*原句的前缀\*\*")
# 截短后的自检结果（写进改动账，末尾说明块按它分账，不说空话）
V_VERBATIM = "逐字命中"          # 截短结果仍逐字命中该来源的本地全文
V_PREFIX = "原句前缀"            # 本地有全文，但原句是我们的转写 → 只保证是原句前缀
V_NOFT = "本地无全文·原句前缀"   # 该来源本地没有全文（许可未审计）→ 只保证是原句前缀


def load_license() -> dict[str, str]:
    """编号 token -> 许可类别。

    审计 CSV 以行首编号为键；总表里有组合编号（"B06; C02"，同一篇论文在两个组各登记一次），
    组合编号的第二段继承该行的类别。审计里没有的行 → ""（调用方按 UNKNOWN 处理）。
    """
    audit: dict[str, str] = {}
    with AUDITCSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            audit[r["编号"]] = r["许可类别"]
    out = dict(audit)
    for toks in iter_rows_tokens():
        cat = audit.get(toks[0], "")
        for t in toks:
            if not out.get(t):
                out[t] = cat
    return out


def iter_rows_tokens() -> list[list[str]]:
    """总表每行的编号 token 列表（组合编号按分号拆开）。"""
    out: list[list[str]] = []
    with LITCSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            toks = [t.strip() for t in re.split(r"[;；]", r["编号(id)"] or "") if t.strip()]
            if toks:
                out.append(toks)
    return out


def load_doi_index() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """DOI / PMID -> 总表里的编号集合（回连文献总表用）。"""
    doi2acc: dict[str, set[str]] = {}
    id2acc: dict[str, set[str]] = {}
    with LITCSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            toks = [t.strip() for t in re.split(r"[;；]", r["编号(id)"] or "") if t.strip()]
            if not toks:
                continue
            d = (r.get("DOI(doi)") or "").strip().lower()
            if d and d not in ("未记录", "na", "-"):
                doi2acc.setdefault(d, set()).update(toks)
            for m in re.findall(r"\d{6,9}", r.get("PMID/PMCID/arXiv(other_ids)") or ""):
                id2acc.setdefault(m, set()).update(toks)
    return doi2acc, id2acc


def load_fulltexts() -> dict[str, str]:
    """编号 -> 该行第三方全文的归一化文本（只用 inventory 的 local，不含我们自己的底稿）。"""
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for rec in inv:
        parts = []
        for p in rec.get("local") or []:
            f = ROOT / p
            if f.exists() and f.suffix in (".txt", ".xml"):
                parts.append(norm(f.read_text(encoding="utf-8", errors="replace")))
        if parts:
            out[rec["id"]] = "\n".join(parts)
    return out


def withheld_absent_ids() -> set[str]:
    """按公开口径不随仓库分发、且本机缺失的第三方全文所对应的编号。

    公开克隆里没有这些底稿，"截后自检"（逐字命中 / 原句前缀 / 本地无全文）就**无法重算**，
    只能记 WITHHELD，不能判 FAIL。本机维护者工作树里底稿齐备，照常重算。
    """
    if not MANIFEST.exists():
        return set()
    man: dict[str, dict] = {}
    with MANIFEST.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            man[r["path"]] = r
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    out: set[str] = set()
    for rec in inv:
        for p in list(rec.get("local") or []) + list(rec.get("records") or []):
            if man.get(p, {}).get("随仓库分发") == "否" and not (ROOT / p).exists():
                out.add(rec["id"])
    return out


def load_required() -> dict[str, list[tuple[str, str]]]:
    """底稿路径 -> [(卡片名, 该卡必须能在这份底稿里逐字命中的引句)]。

    比对口径与门禁 `verify_literature_cards.py` 完全一致：先把卡里的引句去掉
    markdown 强调符号（**、*、`），再在底稿的归一化文本里找。
    """
    out: dict[str, list[tuple[str, str]]] = {}
    for p in sorted(CARDS.glob("*.md")):
        if p.name in NON_CARDS:
            continue
        t = p.read_text(encoding="utf-8")
        mm = DECL.search(t)
        if not mm:
            continue
        decl = mm.group(1).replace(chr(92), "/")
        for _s, _e, q in quotes_of(t):
            out.setdefault(decl, []).append((p.name, clean(q)))
    return out


def loose(s: str) -> str:
    """去掉空白与 markdown 强调、破折号、省略号，只留字母数字与中文。

    底稿里的引句是"原文 + 我们自己加的 **强调** + 省略号 ……"，
    直接子串匹配会漏掉一大半，所以匹配前两边都压成同一套字符集。
    """
    s = re.sub(r"[\*`]", "", s)
    s = s.replace("…", "").replace("—", "").replace("–", "")
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", s)


def quote_segments(q: str, min_len: int = 0) -> list[str]:
    """把一条引句按省略号切成"逐字连续的片段"。

    底稿里我们用"……"表示省略（原文有、我们没抄的部分）。省略号**之前**的片段
    一定是原文的连续逐字片段，可以直接拿去和来源全文比对；省略号之后的片段同理。
    实测踩过：一条 244 字的引句因为中间省略了原文的一句 "often reaching pM values"，
    首尾窗口匹配失败 → 被记成"未归属"→ 按受限口径被截短，
    而它其实是 CC BY 许可的 K39 原文，按口径应当原样保留。
    """
    if min_len <= 0:
        min_len = MIN_ALPHA * 4
    parts = re.split(r"……|\.\.\.|…", q)
    return [p.strip() for p in parts if p and len(p.strip()) >= min_len]


def ft_hits(q: str, fulltexts: dict[str, str], loose_texts: dict[str, str]) -> list[str]:
    """引句可能属于哪几行：谁家第三方全文里有这段文本。

    四级匹配，逐级放宽：
      1. 逐字命中（去 markdown 强调后）；
      2. 首尾各 60 字符的宽松窗口命中；
      3. 按省略号切出的连续片段逐字宽松命中（处理"我们省略了原文一句"的情况）；
      4. 更短的连续片段（≥24 字符），但**只在唯一命中时**采纳。
         第 4 级是为覆盖"引句以我们的省略号开头"的情况（省略号前没有片段）。
         唯一性是防误配的闸门：像 "guided by molecular dynamics" 这种通用短语会同时
         命中多行，那时宁可保持"未归属"（按受限口径处理），也不猜一个来源。
    """
    nq = clean(q)
    hits = [acc for acc, text in fulltexts.items() if nq and nq in text]
    if hits:
        return hits[:8]
    lq = loose(q)
    if len(lq) < 40:
        return []
    head, tail = lq[:60], lq[-60:]
    for acc, lt in loose_texts.items():
        i = lt.find(head)
        if i < 0:
            continue
        if lt.find(tail, i + len(head) - 1) < 0:
            continue
        hits.append(acc)
        if len(hits) >= 8:
            break
    if hits:
        return hits
    # 第 3 级：省略号切出的连续片段
    for seg in quote_segments(q):
        ls = loose(seg)
        if len(ls) < 60:
            continue
        for acc, lt in loose_texts.items():
            if ls in lt:
                hits.append(acc)
                if len(hits) >= 8:
                    break
        if hits:
            break
    if hits:
        return hits
    # 第 4 级：短片段 + 唯一命中才采纳
    cands: set[str] = set()
    for seg in quote_segments(q, 24):
        ls = loose(seg)
        if len(ls) < 24:
            continue
        for acc, lt in loose_texts.items():
            if ls in lt:
                cands.add(acc)
                if len(cands) > 1:
                    break
        if len(cands) > 1:
            break
    if len(cands) == 1:
        return list(cands)
    return hits


def first_segment(q: str, cap: int) -> str | None:
    """引句里省略号之前的第一段原文（若它本身就 ≤ cap 且够长）。

    底稿里的引句是我们从原文里摘的，中间用"……"表示省略。第一段是连续的原文，
    逐字命中原文；带省略号的前缀则不是。
    """
    for sep in ("……", "...", "…"):
        if sep in q:
            seg = q.split(sep)[0].strip()
            if MIN_QUOTE_CHARS <= len(seg) <= cap and sum(c.isalpha() for c in seg) >= MIN_ALPHA:
                return seg
            return None
    return None


def heading_rows(lines: list[str]) -> list[str | None]:
    """逐行给出它所属的文献行（`### [B01] …` 或 `### B17 — …` 形式的小节标题）。

    不匹配这两种形式的标题（章节标题、"附：…"）一律置空——
    否则会把整节汇总里的引句记到上一篇论文头上。
    """
    out: list[str | None] = []
    cur: str | None = None
    for line in lines:
        m = HEAD_RE.match(line)
        if m:
            body = m.group(2).strip()
            t = TAG_RE.match(body)
            if t:
                cur = t.group(1)
            else:
                t2 = TAG_RE2.match(body)
                cur = t2.group(1) if t2 else None
        out.append(cur)
    return out


def recompute_verify(rows: list[dict], fulltexts: dict[str, str]) -> None:
    """按底稿现状重算每一行的"截后自检"，就地写回 rows。

    口径：
      · 该来源本地没有全文（许可未审计）→ "本地无全文·原句前缀"；
      · 截短后的引句逐字命中来源全文 → "逐字命中"；
      · 其余（本地有全文，但原句是我们自己的转写）→ "原句前缀"。
    末尾说明块的分账直接来自这一列，所以它必须与文件里的引句一致。
    """
    cache: dict[str, list[str]] = {}
    for r in rows:
        if r.get("是否截短") != "是":
            r["截后自检"] = ""
            continue
        rel = str(r["底稿"])
        if rel not in cache:
            f = ROOT / rel
            cache[rel] = ([q for (_s, _e, q) in quotes_of(f.read_text(encoding="utf-8"))]
                          if f.exists() else [])
        qs = cache[rel]
        i = int(r["引句序号"]) - 1
        if not (0 <= i < len(qs)):
            r["截后自检"] = ""
            continue
        ft = fulltexts.get(str(r["来源编号"]))
        if ft is None:
            r["截后自检"] = V_NOFT
        elif clean(qs[i]) in ft:
            r["截后自检"] = V_VERBATIM
        else:
            r["截后自检"] = V_PREFIX


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="重跑已经带『引用预算截短』标记的底稿（改动账按行合并，不覆盖）")
    args = ap.parse_args()

    lic = load_license()
    doi2acc, id2acc = load_doi_index()
    fulltexts = load_fulltexts()
    loose_texts = {acc: loose(t) for acc, t in fulltexts.items()}
    required = load_required()
    note_files = sorted(list(NOTES.glob("*.md")) + [p for p in EXTRA_NOTES if p.exists()])

    def cat_of(acc: str) -> str:
        c = lic.get(acc, "")
        return c if c else "UNKNOWN"

    ledger: list[dict] = []
    plans: list[tuple[Path, list[dict], str]] = []
    before = after = 0
    before_r = after_r = 0
    method_stat: dict[str, int] = {}

    for nf in note_files:
        raw = nf.read_text(encoding="utf-8")
        processed = NOTE_MARK in raw
        # 已经处理过的底稿不再重复截短（否则改动账会记成"从已截短版本再截一次"），
        # 但仍然重算归属并刷新末尾说明块——说明块必须与改动账逐条对得上。
        do_trim = (not processed) or args.force
        qs = quotes_of(raw)
        if not qs:
            continue
        rel = nf.relative_to(ROOT).as_posix()
        lines = raw.splitlines(keepends=True)
        offs: list[int] = []
        acc_len = 0
        for l in lines:
            offs.append(acc_len)
            acc_len += len(l)
        hrow = heading_rows(lines)

        def line_of(pos: int) -> int:
            lo = 0
            for i, o in enumerate(offs):
                if o <= pos:
                    lo = i
                else:
                    break
            return lo

        # 逐行的 DOI / PMID 回连结果（同一行多次用，缓存）
        line_acc_cache: dict[int, set[str]] = {}

        def line_accs(i: int) -> set[str]:
            if i not in line_acc_cache:
                found: set[str] = set()
                text = lines[i]
                for d in DOI_RE.findall(text):
                    found |= doi2acc.get(d.rstrip(".,;)]").lower(), set())
                for m in re.findall(r"\b(\d{7,9})\b", text):
                    found |= id2acc.get(m, set())
                line_acc_cache[i] = found
            return line_acc_cache[i]

        used: dict[str, int] = {}
        rows: list[dict] = []
        for idx, (s, e, q) in enumerate(qs, 1):
            li = line_of(s)
            accs: list[str] = []
            method = ""
            if hrow[li]:
                accs, method = [hrow[li]], "标题"
            else:
                la = sorted(line_accs(li))
                if la:
                    accs, method = la, "DOI/PMID行"
                else:
                    hits = ft_hits(q, fulltexts, loose_texts)
                    if hits:
                        accs, method = hits, "全文匹配"
            if not accs:
                acc, cat, method = PSEUDO_ACC, "未归属", "未归属"
            else:
                # 命中多行时（例如同一份转储文件同时属于两行）取受限的那一行——
                # 保守侧：宁可多截。
                ranked = sorted(accs, key=lambda a: (cat_of(a) not in RESTRICTED, a))
                acc = ranked[0]
                cat = cat_of(acc)
            method_stat[method] = method_stat.get(method, 0) + 1
            rows.append({"idx": idx, "start": s, "end": e, "q": q, "acc": acc, "cat": cat,
                         "method": method, "new": q, "changed": False, "kept": "",
                         "verify": ""})
        for row in rows:
            if not do_trim:
                break
            restricted = row["cat"] in RESTRICTED
            long_unattr = (row["acc"] == PSEUDO_ACC and len(row["q"]) >= UNATTRIBUTED_LONG)
            if not (restricted or long_unattr):
                continue
            acc = row["acc"]
            cur = used.get(acc, 0)
            cap = (PER_QUOTE_CAP if cur + len(row["q"]) <= PER_PAIR_CAP
                   else PER_QUOTE_CAP_TAPER)
            if len(row["q"]) <= cap:
                used[acc] = cur + len(row["q"])
                continue
            cand = truncate(row["q"], cap)
            if not cand:
                used[acc] = cur + len(row["q"])
                continue
            # 自检 1：截短后仍逐字命中该来源的本地全文；
            #          本地没有全文的行（许可未审计）改为"截短结果是原句的前缀"。
            # 三级判定（2026-11-08 补：前两级都会给出**逐字命中来源全文**的结果，
            # 比"前缀"口径更严；实测补上了两条本该能截却没截的引句）：
            #   ① 截短结果本身逐字命中来源全文 → 直接采用；
            #   ② 原句是逐字片段但截断点落在我们自己的省略号之后 → 退到省略号前的第一段；
            #   ③ 原句是我们自己的转写 → 同样试第一段；第一段也不是原文片段就保留原句。
            ft = fulltexts.get(acc)
            if ft is not None:
                if clean(cand) in ft:
                    row["verify"] = V_VERBATIM  # ① 截短结果逐字命中来源全文，自检通过
                elif clean(row["q"]) in ft:
                    # 原句本身是原文的逐字片段 → 截短结果也必须仍是原文的逐字片段。
                    # 底稿里的引句常带我们自己的省略号"……"，截断点落在省略号之后时
                    # 前缀就不再逐字等于原文。这时退一步：**只留第一段**
                    #（省略号之前的原文连续片段），它才是能在原文里逐字命中的。
                    seg = first_segment(row["q"], cap)
                    if not seg or clean(seg) not in ft:
                        used[acc] = cur + len(row["q"])
                        continue
                    cand = seg
                    row["verify"] = V_VERBATIM
                else:
                    # 原句不是该来源的逐字片段（底稿里是我们自己的转写：大小写、连字符或
                    # 省略号都改过）。先按老口径走：截短结果是原句的前缀——
                    # 不增加任何第三方内容；前缀不成立时再退到省略号之前的第一段
                    #（那一段若仍是原文的连续片段，结果就逐字命中来源全文）。
                    if row["q"].startswith(cand):
                        row["verify"] = V_PREFIX
                    else:
                        seg = first_segment(row["q"], cap)
                        if not seg or clean(seg) not in ft:
                            used[acc] = cur + len(row["q"])
                            continue
                        cand = seg
                        row["verify"] = V_VERBATIM
            elif not row["q"].startswith(cand):
                # 本地没有全文的行（许可未审计）：截短只保证是原句的前缀——
                # 不增加任何第三方内容。
                used[acc] = cur + len(row["q"])
                continue
            else:
                # 本地没有全文的行（许可未审计），截短结果是原句的前缀
                row["verify"] = V_NOFT
            # 自检 2：不得破坏卡片对这份底稿的逐字引句核验链
            new_text = raw[: row["start"]] + cand + raw[row["end"]:]
            broken = [c for c, cq in required.get(rel, [])
                      if norm(cq) not in norm(new_text)]
            if broken:
                row["kept"] = f"为保住卡 {broken[0]} 的逐字引句而保留原句"
                used[acc] = cur + len(row["q"])
                continue
            row["new"] = cand
            row["changed"] = True
            used[acc] = cur + len(cand)
        # 全部有引句的底稿都进 plans：末尾说明块要按**合并后的账**重写。
        plans.append((nf, rows, raw))
        for row in rows:
            if row["cat"] in RESTRICTED or row["acc"] == PSEUDO_ACC:
                before_r += len(row["q"])
                after_r += len(row["new"])
            before += len(row["q"])
            after += len(row["new"])
            ledger.append({
                "底稿": rel,
                "引句序号": row["idx"],
                "归属方式": row["method"],
                "来源编号": row["acc"],
                "许可类别": row["cat"],
                "截前字符": len(row["q"]),
                "截后字符": len(row["new"]),
                "是否截短": "是" if row["changed"] else "否",
                "保留原因": row["kept"],
                "截后自检": row["verify"],
                "截后片段": row["new"][:120] if row["changed"] else "",
            })

    n_changed = sum(1 for r in ledger if r["是否截短"] == "是")
    n_kept = sum(1 for r in ledger if r["保留原因"])
    if not args.check:
        print(f"底稿 {len(note_files)} 份 · 引句 {len(ledger)} 处")
        print(f"全部引句：{before} → {after} 字符（-{before - after}）")
        print(f"其中受限或未归属来源：{before_r} → {after_r} 字符（-{before_r - after_r}）")
        print(f"被截短 {n_changed} 处（{len(plans)} 份底稿）；因护住卡引句而保留原句 {n_kept} 处")
        print("归属方式分布：" + "，".join(f"{k} {v}" for k, v in sorted(method_stat.items())))

    if args.dry_run:
        print("--dry-run：未改动任何底稿")
        return 0

    if args.check:
        if not LEDGER.exists():
            print("判定结果: FAIL — 改动账不存在")
            return 1
        bad = 0
        withheld_n = 0
        unverifiable_ids = withheld_absent_ids()
        rows = list(csv.DictReader(LEDGER.open(encoding="utf-8-sig", newline="")))
        by_note: dict[str, list[dict]] = {}
        for r in rows:
            by_note.setdefault(r["底稿"], []).append(r)
        for rel, rs in by_note.items():
            f = ROOT / rel
            if not f.exists():
                bad += 1
                print("  ", rel, "底稿缺失")
                continue
            cur = quotes_of(f.read_text(encoding="utf-8"))
            if len(cur) != len(rs):
                bad += 1
                print("  ", rel, f"引句条数 {len(cur)} != 账上 {len(rs)}")
                continue
            for r, (_s, _e, q) in zip(rs, cur):
                # 账上"截后字符"必须等于底稿现状——**每一行都要核**，
                # 只查"被截短"的行会让"被改过但没记账"的行漏网（实测踩过）。
                if len(q) != int(r["截后字符"]):
                    bad += 1
                    print("  ", rel, f"第 {r['引句序号']} 条现状长度 {len(q)} != 账上截后字符 {r['截后字符']}")
                if int(r["截前字符"]) < int(r["截后字符"]):
                    bad += 1
                    print("  ", rel, f"第 {r['引句序号']} 条截前字符 < 截后字符")
                # 许可允许再分发的来源必须原样保留，账上不许出现"被截短"
                if r["许可类别"] in REDISTRIBUTABLE and r["是否截短"] == "是":
                    bad += 1
                    print("  ", rel, f"第 {r['引句序号']} 条许可类别 {r['许可类别']} 可再分发，不该被截短")
                if r["是否截短"] == "是" and q.count("**") % 2:
                    bad += 1
                    print("  ", rel, f"第 {r['引句序号']} 条强调标记不成对")
            # "截后自检"必须与现状重算一致（说明块的分账就是靠它）
            for r in rs:
                want = ""
                unverifiable_row = False
                if r.get("是否截短") == "是":
                    ft = fulltexts.get(str(r["来源编号"]))
                    if ft is None:
                        if (str(r["来源编号"]) in unverifiable_ids
                                and str(r.get("截后自检", "")) != V_NOFT):
                            # 底稿按公开口径未随仓库分发 → 本机无法重算，记 WITHHELD
                            unverifiable_row = True
                            withheld_n += 1
                        else:
                            want = V_NOFT
                    else:
                        i = int(r["引句序号"]) - 1
                        if 0 <= i < len(cur) and clean(cur[i][2]) in ft:
                            want = V_VERBATIM
                        else:
                            want = V_PREFIX
                if not unverifiable_row and str(r.get("截后自检", "")) != want:
                    bad += 1
                    print("  ", rel, f"第 {r['引句序号']} 条截后自检 {r.get('截后自检', '')!r} != 重算 {want!r}")
            # 末尾说明块必须与账一致（条数、来源编号、许可类别、逐字/前缀分账）
            trimmed = [r for r in rs if r["是否截短"] == "是"]
            blk = BLOCK_RE.search(f.read_text(encoding="utf-8"))
            if trimmed and not blk:
                bad += 1
                print("  ", rel, "缺少『引用预算截短』说明块")
            elif blk:
                if int(blk.group(1)) != len(trimmed):
                    bad += 1
                    print("  ", rel, f"说明块条数 {blk.group(1)} != 账上已截短 {len(trimmed)}")
                accs = sorted({r["来源编号"] for r in trimmed})
                cats = sorted({r["许可类别"] for r in trimmed})
                if blk.group(2).split("、") != accs:
                    bad += 1
                    print("  ", rel, f"说明块来源编号 {blk.group(2)} != 账上 {accs}")
                if blk.group(3).split("、") != cats:
                    bad += 1
                    print("  ", rel, f"说明块许可类别 {blk.group(3)} != 账上 {cats}")
                # 分账：逐字命中 / 原句前缀
                n_verb = sum(1 for r in trimmed if r.get("截后自检") == V_VERBATIM)
                n_pref = len(trimmed) - n_verb
                m = BLOCK_SPLIT_RE.search(f.read_text(encoding="utf-8"))
                if n_pref:
                    if not m:
                        bad += 1
                        print("  ", rel, "说明块缺少逐字/前缀分账")
                    else:
                        if int(m.group(1)) != n_verb or int(m.group(2)) != n_pref:
                            bad += 1
                            print("  ", rel, f"说明块分账 {m.group(1)}/{m.group(2)} != 账上 {n_verb}/{n_pref}")
                else:
                    if "**全部截短后仍逐字命中同一份来源全文**" not in f.read_text(encoding="utf-8"):
                        bad += 1
                        print("  ", rel, "说明块未声明『全部逐字命中』")
        # 卡片侧的核验链必须仍然成立
        for rel, req in required.items():
            f = ROOT / rel
            if not f.exists():
                continue
            t = norm(f.read_text(encoding="utf-8"))
            for card, q in req:
                if norm(q) not in t:
                    bad += 1
                    print("  ", rel, f"卡 {card} 的引句在底稿里不再逐字命中")
        print("判定标准: 每份底稿引句条数不变；**每一行**的现状长度等于改动账上的截后字符数；"
              "截前字符 ≥ 截后字符；可再分发的许可类别不许被截短；截短处强调标记成对；"
              "末尾说明块的条数与来源编号、许可类别等于改动账；卡对底稿的逐字引句链未被破坏")
        print(f"判定结果: {'PASS 0 处不符' if bad == 0 else f'FAIL {bad} 处不符'}")
        return 0 if bad == 0 else 1

    if not ledger and LEDGER.exists():
        # 没有任何底稿带引句：不重写改动账，否则会把已有的逐条记录清成空表。
        print("没有底稿引句：未改动任何底稿，改动账保持原样")
        print("下一步：跑 scripts/verify_literature_cards.py 与本脚本 --check 复核")
        return 0

    # 改动账按 (底稿, 引句序号) 合并：旧行保留原"截前字符"（原始会计口径不许丢），
    # 只有当这一条确实又变短时才更新。账目条数不许变少。
    # 合并必须在写文件之前：末尾说明块要按**合并后的账**重写，
    # 否则"文件里写的条数"和"账里记的条数"会对不上（实测踩过：
    # 账被修复脚本更新过，六份底稿末尾的说明块还停在旧数字上）。
    old_rows: list[dict] = []
    if LEDGER.exists():
        old_rows = list(csv.DictReader(LEDGER.open(encoding="utf-8-sig", newline="")))
    merged = [dict(r) for r in old_rows]
    # 键要统一成字符串：旧账是从 CSV 读出来的（引句序号是 str），
    # 新算出来的是 int，不统一会把同一行记成两行（实测过）。
    idx = {(r["底稿"], str(r["引句序号"])): i for i, r in enumerate(merged)}
    for r in ledger:
        k = (r["底稿"], str(r["引句序号"]))
        if k in idx:
            old = merged[idx[k]]
            new = dict(r)
            # "截前字符"是**原始会计口径**（截短之前的原句长度），只存在于旧账里：
            # 已经处理过的底稿在磁盘上就是截短后的样子，重算不出原来有多长。
            # 所以取旧账与新算的较大值，既不许丢历史，也不许小于现状。
            before = max(int(old.get("截前字符") or 0), int(r["截前字符"]))
            new["截前字符"] = before
            after = int(r["截后字符"])
            # 是否截短 = 现状比原始短。引句被还原回原文（截后 == 截前）就不算截短。
            new["是否截短"] = "是" if after < before else "否"
            if new["是否截短"] == "否":
                new["截后片段"] = ""
            else:
                new["截后片段"] = new.get("截后片段") or old.get("截后片段", "")
            # "保留原因"也是历史事实（为护住卡片核验链而没截），不许被重算覆盖
            if old.get("保留原因"):
                new["保留原因"] = old["保留原因"]
            merged[idx[k]] = new
        else:
            merged.append(r)
            idx[k] = len(merged) - 1
    if len(merged) < len(old_rows):
        print(f"拒绝写入：改动账条数变少（{len(old_rows)} → {len(merged)}），账目不许被覆盖")
        return 1

    # "截后自检"按**底稿现状**重算：说明块的分账必须与文件里真实的引句一致
    # （旧账里的这一列可能是上一轮算的，且上一轮的文件状态不同）。
    recompute_verify(merged, fulltexts)

    n_files = 0
    for nf, rows, raw in plans:
        rel = nf.relative_to(ROOT).as_posix()
        new_raw = raw
        for row in sorted(rows, key=lambda r: -r["start"]):
            if not row["changed"]:
                continue
            new_raw = new_raw[: row["start"]] + row["new"] + new_raw[row["end"]:]
        mrows = [r for r in merged if r["底稿"] == rel]
        trimmed = [r for r in mrows if r["是否截短"] == "是"]
        # 重跑时先把上一轮追加在末尾的说明块去掉，避免叠加多份说明。
        cut = new_raw.find(f"> **{NOTE_MARK}")
        if cut >= 0:
            new_raw = new_raw[:cut].rstrip() + "\n"
        if trimmed:
            accs = sorted({str(r["来源编号"]) for r in trimmed})
            cats = sorted({str(r["许可类别"]) for r in trimmed})
            # 说明块按改动账里的"截后自检"分账：
            # 逐字命中的那几条确实仍能在来源全文里逐字找到；
            # 其余是原句前缀（本地无全文或原句是我们自己的转写）——
            # 只减不增，不新增任何第三方内容，但**不能**说成"仍逐字命中"。
            n_verb = sum(1 for r in trimmed if r.get("截后自检") == V_VERBATIM)
            n_pref = len(trimmed) - n_verb
            if n_pref:
                tail = (f"；其中 {n_verb} 条截短后仍**逐字命中同一份来源全文**，"
                        f"其余 {n_pref} 条为**原句的前缀**（本地无全文或原句是我们自己的转写，"
                        f"只减不增、不新增第三方内容）")
            else:
                tail = "；**全部截短后仍逐字命中同一份来源全文**"
            note = (f"\n> **{NOTE_MARK}（2026-11-08，公开仓库口径）**：本底稿有 {len(trimmed)} 条逐字引句被截短"
                    f"（来源编号：{'、'.join(accs)}；许可类别：{'、'.join(cats)}），按 "
                    f"`deliverables/protein_design_license_audit.csv` 的逐份许可判定，单条引句截到 "
                    f"≤{PER_QUOTE_CAP} 字符{tail}。"
                    f"逐条改动账见 `deliverables/quote_budget_notes_ledger.csv`。\n")
            new_raw = new_raw.rstrip() + "\n" + note
        else:
            new_raw = new_raw.rstrip() + "\n"
        if new_raw != raw:
            nf.write_text(new_raw, encoding="utf-8")
            n_files += 1

    with LEDGER.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ledger[0].keys()), lineterminator="\n",
                           restval="")
        w.writeheader()
        w.writerows(merged)
    print(f"已改写 {n_files} 份底稿；改动账 → {LEDGER.relative_to(ROOT)}（累计 {len(merged)} 行）")
    print("下一步：跑 scripts/verify_literature_cards.py 与本脚本 --check 复核")
    return 0


if __name__ == "__main__":
    sys.exit(main())
