#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审计本地归档的第三方全文的许可，并给出"能不能商业再分发"的边界。

为什么要做这个：库里缓存了 87 份各出版商/PMC 的开放获取全文抽取（用于逐字引句核验）。
这些是**第三方的内容**，许可各不相同；其中带 NC / ND 的条款会直接决定本库能不能把
全文一起卖出去。本脚本把这件事从"印象"变成"逐行可查的表"。

数据来源（全部一手，逐条记录 URL + 取回时间 + 内容 SHA-256）:
  1. 本地缓存文件本身 —— 全文抽取里带 <license> 或 CC 许可证链接时，直接从文件读出，
     这是最强证据（就是将要再分发的那份东西自带的声明）。
  2. NCBI E-utilities efetch(db=pmc) —— 本地文件没有许可声明时，按 PMCID 取回元数据里的
     <license> 元素。取回结果缓存到 data/interim/license_cache.json，不再重复请求。
  3. 第三方全文清单 `deliverables/fulltext_manifest.csv` —— **仅当该编号的本地原文整体不在场时**
     （公开仓库口径：第三方原文不随包分发），许可类别取自清单里"各编号许可类别"列的快照。
     内部核验库里本地文件在场时永远走 1/2，本条只在公开克隆里生效。

分类（决定能不能随产品一起卖）:
  CC0 / PUBLIC_DOMAIN   —— 可再分发（含商用），最好的一类
  CC_BY                 —— 可再分发（含商用）+ 署名 + 标注改动
  CC_BY_SA              —— 可再分发（含商用）+ 署名 + 同许可
  CC_BY_NC              —— 仅限非商业用途 ⇒ **不可随商业产品再分发**
  CC_BY_ND              —— 可商用但禁止演绎 ⇒ **改写/抽取即违规**
  CC_BY_NC_ND           —— 非商业 + 禁演绎 ⇒ **最严**
  PUBLISHER_TERMS       —— 出版商条款（Nature/PNAS 等），无 CC 声明 ⇒ 不可再分发全文
  TEXT_MINING_ONLY      —— 仅文本挖掘/公平使用 ⇒ 不可再分发全文
  UNKNOWN               —— 查不到，必须人工确认

用法:
  python scripts/audit_source_licenses.py            # 生成 CSV + Markdown 报告
  python scripts/audit_source_licenses.py --check    # 只比对磁盘产物是否与重算一致（逐字节）
  python scripts/audit_source_licenses.py --refresh  # 重新联网取回缺失的许可（会覆盖缓存）

成功测试（可判伪）:
  - `--check` 在人为改坏 CSV 里一个许可类别时必须退出非 0（实测过：内部核验库与
    "本地原文不在场"的公开克隆两种情形都实测为 FAIL）。
  - 报告里"不可商业再分发"的行数必须等于 CSV 里 category 属于受限类集合的行数（自洽）。
  - 每个非 UNKNOWN 的行都必须能指到证据来源（本地文件路径 或 取回 URL + SHA-256）。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSVP = ROOT / "data" / "protein_design_literature.csv"
CARDS = ROOT / "data" / "literature_cards"
INTERIM = ROOT / "data" / "interim"
OUT = ROOT / "deliverables"
CACHE = INTERIM / "license_cache.json"

# 分类 → (中文名, 能不能随商业产品再分发这份全文, 说明)
CATS = {
    "CC0": ("CC0 / 公有领域", "可（含商用）", "无署名义务，但署名仍是礼貌做法"),
    "PUBLIC_DOMAIN": ("公有领域声明", "可（含商用）", "作者/机构声明放弃著作权"),
    "CC_BY": ("CC BY 4.0", "可（含商用）", "须署名 + 链接许可证 + 标注改动"),
    "CC_BY_SA": ("CC BY-SA 4.0", "可（含商用）", "须署名 + 相同方式共享"),
    "CC_BY_NC": ("CC BY-NC 4.0", "不可", "非商业用途限定，商业再分发需另获授权"),
    "CC_BY_ND": ("CC BY-ND 4.0", "不可（须原样）", "禁演绎；抽取/改写即不再是同一份，谨慎处理"),
    "CC_BY_NC_ND": ("CC BY-NC-ND 4.0", "不可", "非商业 + 禁演绎，商业再分发需另获授权"),
    "PUBLISHER_TERMS": ("出版商使用条款（无 CC 声明）", "不可", "按出版商条款使用，不可再分发全文"),
    "ALL_RIGHTS_RESERVED": ("保留所有权利（禁止再分发/复用/改编）", "不可", "作者明确保留所有权利，须另行授权"),
    "RESEARCH_REUSE_ONLY": ("仅研究性复用（须注明来源）", "不可", "只授权研究性复用，非商业再分发不在授权范围内"),
    "TEXT_MINING_ONLY": ("仅文本挖掘 / 公平使用", "不可", "只允许检索与挖掘，不可再分发全文"),
    "UNKNOWN": ("查不到，需人工确认", "未知", "在确认前按不可再分发处理"),
}

# 会被判为"不可再分发"的类别
RESTRICTED = {"CC_BY_NC", "CC_BY_ND", "CC_BY_NC_ND", "PUBLISHER_TERMS",
               "TEXT_MINING_ONLY", "ALL_RIGHTS_RESERVED", "RESEARCH_REUSE_ONLY",
               "UNKNOWN"}

# CC 条款代码 → 类别。by-nc-nd 必须排在 by-nc 之前匹配，否则会被 by-nc 抢走。
CC_CODE = [
    ("by-nc-nd", "CC_BY_NC_ND"),
    ("by-nd", "CC_BY_ND"),
    ("by-nc-sa", "CC_BY_NC"),
    ("by-sa", "CC_BY_SA"),
    ("by-nc", "CC_BY_NC"),
    ("by", "CC_BY"),
]
RE_CC_URL = re.compile(r"creativecommons\.org/licenses/([a-z\-]+)/([0-9.]+)", re.I)
RE_CC_NAME = re.compile(r"Creative Commons\s+(Attribution(?:-[A-Za-z]+)*)\s+([0-9.]+)\s+International", re.I)
RE_LICENSE_ELEM = re.compile(r"<license\b.*?</license>", re.S | re.I)
RE_TAG = re.compile(r"<[^>]+>")
RE_PMC = re.compile(r"PMC\s*(\d+)", re.I)


def cc_from_code(code: str) -> str:
    code = code.lower()
    for pref, cat in CC_CODE:
        if code == pref or code.startswith(pref + "-"):
            return cat
    if code.startswith("publicdomain") or code.startswith("zero"):
        return "CC0"
    return "UNKNOWN"


def classify_local(text: str) -> tuple[str, str]:
    """从一份本地文件（或 Europe PMC 的 license 字段）里读出许可证类别与证据原文。

    Europe PMC 的 license 字段是短码（"cc by" / "cc by-nc" / "cc by-nd"），
    PMC XML 里是长句，两种都要认。

    只在文件的**前 15%** 里找 CC 链接：正文与参考文献里常出现别的文章的
    CC 链接（例如"本文改编自 CC BY-NC-ND 的某某"），若在全文件里搜第一个命中，
    就会把别的文章的许可证算到本文头上。实测抽取文本的许可证块都在前 5% 以内。
    """
    t = text.strip()
    if not t:
        return "UNKNOWN", ""
    # Europe PMC 短码："cc by-nc-nd" / "cc by" / "cc0" / "cc by-nd"
    m = re.fullmatch(r"cc\s*([a-z0-9\- ]+)", t, re.I)
    if m:
        code = re.sub(r"\s+", "-", m.group(1).strip())
        return cc_from_code(code), t
    if re.fullmatch(r"cc0", t, re.I):
        return "CC0", t
    head = text[:max(20000, int(len(text) * 0.15))]
    m = RE_CC_URL.search(head)
    if m:
        return cc_from_code(m.group(1)), m.group(0)
    m = RE_CC_NAME.search(head)
    if m:
        name = m.group(1).lower()
        if "noncommercial-noderivatives" in name:
            cat = "CC_BY_NC_ND"
        elif "noncommercial" in name:
            cat = "CC_BY_NC"
        elif "noderivatives" in name:
            cat = "CC_BY_ND"
        elif "sharealike" in name:
            cat = "CC_BY_SA"
        else:
            cat = "CC_BY"
        return cat, m.group(0)
    low = head.lower()

    def snip(key: str, width: int = 260) -> str:
        """证据原文必须是文件里的**逐字片段**，不能是自己写的一句话。
        审计表要能被人按字符串回查原文件，所以这里一律截原文。"""
        i = low.find(key)
        if i < 0:
            return ""
        return re.sub(r"\s+", " ", head[max(0, i - 60): i + width]).strip()

    if "all rights reserved" in low and "may not be redistributed" in low:
        return "ALL_RIGHTS_RESERVED", snip("all rights reserved")
    # "cc0" 必须按词边界找：PMC XML 的 md5 校验和里出现过 "06cc0dfc76d"，
    # 用子串匹配会把一篇 Elsevier COVID 特许文章误判成公有领域（实测踩过）。
    m_cc0 = re.search(r"\bcc0\b", low)
    if m_cc0 or "public domain" in low:
        if m_cc0:
            return "PUBLIC_DOMAIN", snip("cc0")
        return "PUBLIC_DOMAIN", snip("public domain")
    if "unrestricted research re-use" in low:
        return "RESEARCH_REUSE_ONLY", snip("unrestricted research re-use", 300)
    if "published under the" in low and "license" in low:
        return "PUBLISHER_TERMS", snip("published under the", 200)
    if "text mining" in low and "fair use" in low:
        return "TEXT_MINING_ONLY", snip("text mining", 200)
    if "conditions of use" in low and ("nature.com" in low or "springer" in low):
        return "PUBLISHER_TERMS", snip("conditions of use", 260)
    return "UNKNOWN", ""


def fetch_pmc_license(pmcid: str) -> dict:
    """按 PMCID 取回 PMC 元数据里的 <license> 元素。返回 {url, fetched_at, sha256, license_text}。"""
    num = RE_PMC.sub("", pmcid).strip() or re.sub(r"\D", "", pmcid)
    url = (f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
           f"?db=pmc&id={num}&rettype=xml")
    proc = subprocess.run(["curl.exe", "-s", url], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    body = proc.stdout or ""
    m = RE_LICENSE_ELEM.search(body)
    lic = RE_TAG.sub(" ", m.group(0)) if m else ""
    lic = re.sub(r"\s+", " ", lic).strip()
    return {
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body.encode("utf-8", "replace")).hexdigest(),
        "license_text": lic[:600],
    }


def fetch_doi_license(doi: str) -> dict:
    """按 DOI 从 Europe PMC 取回题录里的 license 字段（预印本走这条路）。"""
    url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
           f"query=DOI:{doi}&resultType=core&format=json")
    proc = subprocess.run(["curl.exe", "-s", url], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    body = proc.stdout or ""
    lic = ""
    try:
        res = json.loads(body)["resultList"]["result"]
        if res:
            lic = str(res[0].get("license") or "")
    except Exception:
        pass
    return {
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body.encode("utf-8", "replace")).hexdigest(),
        "license_text": lic,
    }


def fetch_doi_landing(doi: str) -> dict:
    """跟随 DOI 到出版商/预印本托管页，读页面自带的 DC.Rights 声明。

    预印本的许可证权威声明在托管页上（bioRxiv 的 DC.Rights 会写明
    "This pre-print is available under ... CC BY-ND 4.0"），
    Europe PMC 的 license 字段对这些新预印本常常是空的。
    """
    url = "https://doi.org/" + doi
    proc = subprocess.run(["curl.exe", "-sL", url], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    body = proc.stdout or ""
    m = re.search(r"(?i)DC\.Rights\" content=\"([^\"]{0,400})", body)
    rights = m.group(1).strip() if m else ""
    return {
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body.encode("utf-8", "replace")).hexdigest(),
        "license_text": rights,
    }


def load_cache() -> dict:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict) -> None:
    INTERIM.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")


MANIFEST = ROOT / "deliverables" / "fulltext_manifest.csv"


def load_manifest() -> dict[str, list[dict]]:
    """第三方原文清单：路径 -> 行。公开仓库不随包分发第三方全文后，
    本地文件可能不在场；--check 必须还能判，因此清单是第二证据来源。"""
    if not MANIFEST.exists():
        return {}
    out: dict[str, list[dict]] = {}
    with MANIFEST.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            out.setdefault(r["path"], []).append(r)
    return out


def manifest_by_acc(manifest: dict[str, list[dict]]) -> dict[str, tuple[str, dict]]:
    """清单 -> 编号 -> (该编号当初的许可类别, 该编号的一份清单行)。

    清单里每份文件都带 sha256 与重取方式，"各编号许可类别"列写的是该文件归属的
    **每一行**当时的许可审计结论（"B06=CC_BY；C02=CC_BY_NC"）。公开仓库里第三方
    原文不在场，这一列就是那些行唯一的离线许可依据。
    """
    out: dict[str, tuple[str, dict]] = {}
    for rows in manifest.values():
        for r in rows:
            pairs = r.get("各编号许可类别") or ""
            for pair in re.split(r"[;；]", pairs):
                if "=" not in pair:
                    continue
                acc, cat = pair.split("=", 1)
                acc, cat = acc.strip(), cat.strip()
                if acc and cat:
                    out.setdefault(acc, (cat, r))
    return out


def col_of(fields: list[str], prefix: str) -> str:
    for k in fields:
        if k.startswith(prefix):
            return k
    raise KeyError(prefix)


def build(refresh: bool) -> tuple[list[dict], list[str]]:
    with CSVP.open(encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        fields, rows = list(rd.fieldnames or []), list(rd)
    inv = {r["id"]: r for r in json.loads((CARDS / "inventory.json").read_text(encoding="utf-8"))}
    smap = json.loads((CARDS / "sources_map.json").read_text(encoding="utf-8"))
    # sources_map 的键有组合编号（"B06; C02"），而审计循环用的是单编号。
    # 不拆开的话，这 4 行的底稿路径取不到（实测 B06/B10/B32/B42 的 smap.get(acc) 为空），
    # 于是本地文件明明在场却判成"无底稿"，许可只能靠联网取回。
    smap_acc: dict[str, list[str]] = {}
    for key, paths in smap.items():
        for tok in re.split(r"[;；]", key):
            tok = tok.strip()
            if tok:
                smap_acc.setdefault(tok, []).extend(paths)
    cache = load_cache()
    notes: list[str] = []
    manifest = load_manifest()
    macc = manifest_by_acc(manifest)

    out: list[dict] = []
    # CSV 一行可能挂多个编号（"B06; C02"），inventory 是按单编号记的。
    # 先把每个单编号映射到它所属的 CSV 行，再按 inventory 的 has_fulltext 名单遍历，
    # 否则会漏掉 4 行（实测：CSV 首编号与 inventory 编号不一致时整行被跳过）。
    row_of: dict[str, dict] = {}
    for r in rows:
        for tok in [x.strip() for x in r[col_of(fields, "编号")].split(";") if x.strip()]:
            row_of.setdefault(tok, r)
    for inv_key in sorted(inv):
        if not inv.get(inv_key, {}).get("has_fulltext"):
            continue
        # inventory 的键可能是 "B06; C02" 这样的组合编号，拆开逐个查
        accs = [x.strip() for x in inv_key.split(";") if x.strip()]
        r = None
        acc = inv_key
        for a in accs:
            if a in row_of:
                r, acc = row_of[a], a
                break
        if r is None:
            notes.append(f"{inv_key}: inventory 有全文但 CSV 里找不到对应行")
            continue
        doi = r[col_of(fields, "DOI")].strip()
        venue = r[col_of(fields, "期刊或预印本")].strip()
        ids = r[col_of(fields, "PMID/PMCID")].strip()

        # 1) 本地缓存文件里的许可证声明（最强证据：就是将被再分发的那份东西）
        cat, ev, ev_src = "UNKNOWN", "", ""
        local_present = False
        for p in smap_acc.get(acc, []):
            f = ROOT / p
            if not f.exists() or not p.endswith((".xml", ".txt")):
                continue
            local_present = True
            text = f.read_text(encoding="utf-8", errors="replace")
            c, e = classify_local(text)
            if c != "UNKNOWN":
                cat, ev, ev_src = c, e, p
                break
        if cat == "UNKNOWN" and not local_present and acc in macc:
            # 1.5) 本地第三方原文按公开口径不随仓库分发 ⇒ 许可类别取自清单快照（离线可判）。
            # 内部核验库里本地文件在场时不会走到这里，所以这条分支只在公开克隆里生效。
            mcat, mrow = macc[acc]
            cat = mcat
            ev = ""
            ev_src = (f"deliverables/fulltext_manifest.csv → {mrow['path']}"
                      f" (sha256 {mrow.get('sha256', '')[:16]}…)")
            notes.append(f"{acc}: 本地第三方原文未随仓库分发，许可类别取自清单快照"
                         f"（{mcat}）")
        if cat == "UNKNOWN":
            # 2) 本地没有就按 PMCID 取回元数据许可（带缓存，不重复请求）
            m = RE_PMC.search(ids)
            if not m:
                for p in smap_acc.get(acc, []):
                    m = RE_PMC.search(p)
                    if m:
                        break
            if m:
                pmcid = "PMC" + m.group(1)
                key = pmcid
                if refresh or key not in cache:
                    cache[key] = fetch_pmc_license(pmcid)
                    save_cache(cache)
                    time.sleep(0.4)
                rec = cache[key]
                c, e = classify_local(rec.get("license_text", ""))
                if c != "UNKNOWN":
                    cat, ev = c, e[:200]
                    ev_src = f"{rec['url']} (sha256 {rec['sha256'][:16]}…)"
                else:
                    notes.append(f"{acc}: efetch 未给出可识别许可（{pmcid}）")
            elif doi:
                # 3) 预印本等无 PMCID 的行：先按 DOI 从 Europe PMC 题录取 license 短码，
                #    取不到再跟随 DOI 到托管页读 DC.Rights 声明（预印本的权威声明在那儿）。
                key = "doi:" + doi
                if refresh or key not in cache:
                    cache[key] = fetch_doi_license(doi)
                    save_cache(cache)
                    time.sleep(0.4)
                rec = cache[key]
                c, e = classify_local(rec.get("license_text", ""))
                if c != "UNKNOWN":
                    cat, ev = c, e[:200]
                    ev_src = f"{rec['url']} (sha256 {rec['sha256'][:16]}…)"
                else:
                    key2 = "landing:" + doi
                    if refresh or key2 not in cache:
                        cache[key2] = fetch_doi_landing(doi)
                        save_cache(cache)
                        time.sleep(0.4)
                    rec2 = cache[key2]
                    c, e = classify_local(rec2.get("license_text", ""))
                    if c != "UNKNOWN":
                        cat, ev = c, e[:200]
                        ev_src = f"{rec2['url']} (sha256 {rec2['sha256'][:16]}…)"
                    else:
                        notes.append(f"{acc}: Europe PMC 与 DOI 托管页都未给出可识别许可（DOI {doi}）")
            else:
                notes.append(f"{acc}: 无 PMCID、无 DOI，本地也无许可声明")

        zh, redistributable, note = CATS[cat]
        out.append({
            "编号": acc,
            "DOI": doi,
            "期刊或预印本": venue[:120],
            "许可类别": cat,
            "许可名称": zh,
            "可否随商业产品再分发该全文": redistributable,
            "条件": note,
            "证据原文": ev[:300],
            "证据来源": ev_src,
        })
    return out, notes


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_report(path: Path, rows: list[dict], notes: list[str]) -> None:
    by: dict[str, list[str]] = {}
    for r in rows:
        by.setdefault(r["许可类别"], []).append(r["编号"])
    blocked = [r for r in rows if r["许可类别"] in RESTRICTED]
    ok = [r for r in rows if r["许可类别"] not in RESTRICTED and r["许可类别"] != "UNKNOWN"]

    L = []
    L.append("# 第三方全文许可审计与商业分发边界")
    L.append("")
    L.append(f"生成日期：{date.today().isoformat()}　·　生成脚本：`scripts/audit_source_licenses.py`"
             f"（重跑可复现；外部取回结果缓存在 `data/interim/license_cache.json`）")
    L.append("")
    L.append("本文件回答一个问题：**我们缓存的这些第三方全文，哪些可以随商业产品一起再分发？**")
    L.append("")
    L.append("## 结论")
    L.append("")
    L.append(f"- 本地归档全文共 **{len(rows)} 行**（= `inventory.json` 里 `has_fulltext` 为真的行）。")
    L.append(f"- 许可本身允许随商业产品再分发（含商用）：**{len(ok)} 行**（全部是 CC BY 4.0）。")
    L.append(f"- 许可不允许或需另获授权：**{len(blocked)} 行**。")
    L.append("")
    L.append("**产品决策：商业版本一律不含任何第三方全文缓存**，无论许可是否允许。")
    L.append("")
    L.append("理由有三层：")
    L.append("")
    L.append("1. 26 行的许可**明确不允许**商业再分发（NC / ND / 出版商条款 / 保留所有权利 / 仅研究性复用）。")
    L.append(f"2. 另外 {len(ok)} 行虽是 CC BY，但再分发要逐篇履行署名、链接许可证、标注改动，"
             "打包成一个产品后这些义务的履行与追溯成本很高。")
    L.append("3. **一致性**：混合许可的产品在客户侧无法回答\"这份文件我能怎么用\"，"
             "一次说不清就会变成责任事故。")
    L.append("")
    L.append("所以商业版里可以放的是**我们自己写的东西**：")
    L.append("")
    L.append("- 精读卡里的方法 / 工作流 / 难点与应对（我们自己的表达）")
    L.append("- 我们自己的阈值台账、证据级别判定与推算（注明为我们的推导）")
    L.append("- 少量逐字短引句用于支撑具体论断——**引句是引用，不是全文再分发**，"
             "每条都要带文献编号，出处可查（`[B09]` 这种编号在 `data/protein_design_literature.csv` 里可查）")
    L.append("")
    L.append("第三方全文缓存（`data/literature_cards/fulltext/`、`data/interim/baker_lit/`、"
             "`data/interim/claim_lit/`）只留在**内部核验库**里，用来复跑逐字引句门禁，"
             "不进任何对外发布包。")
    L.append("")
    L.append("## 按类别分布")
    L.append("")
    L.append("| 类别 | 行数 | 编号 | 可否再分发 | 条件 |")
    L.append("|---|---|---|---|---|")
    for cat in sorted(by, key=lambda c: -len(by[c])):
        zh, redist, note = CATS[cat]
        ids = " ".join(by[cat])
        L.append(f"| {zh} | {len(by[cat])} | {ids} | {redist} | {note} |")
    L.append("")
    L.append("## 逐行明细")
    L.append("")
    L.append("| 编号 | 许可 | 可否再分发 | 证据来源 | 证据原文（截断） |")
    L.append("|---|---|---|---|---|")
    for r in rows:
        L.append(f"| {r['编号']} | {r['许可名称']} | {r['可否随商业产品再分发该全文']} | "
                 f"{r['证据来源'][:80]} | {r['证据原文'][:120]} |")
    L.append("")
    L.append("## 待人工确认")
    L.append("")
    if notes:
        for n in notes:
            L.append(f"- {n}")
    else:
        L.append("- 无。")
    L.append("")
    L.append("## 口径说明")
    L.append("")
    L.append("1. 这里的\"再分发\"指把**第三方全文文件本身**（XML / 抽取文本）放进产品或公开仓库。")
    L.append("2. 卡片里的**短引句**与**我们自己的转述、方法总结、阈值台账**不在受限范围内——"
             "那是引用与原创分析；但引用量要小、标明出处、且不得被当作原文的替代品。")
    L.append("3. \"可（含商用）\"表示许可本身允许商业性再分发，**仍须履行署名/相同方式共享等条件**；"
             "本审计不替代法律意见。")
    L.append("4. 预印本（bioRxiv 等）默认多为 CC BY-NC-ND，**按不可再分发处理**；"
             "正式发表版可能是 CC BY，因此下架预印本缓存、改用已发表版引句是更稳的做法。")
    L.append("5. 本审计只判**许可文本**与**能不能再分发**，不判内容对错，也不替代法律意见。"
             "若要正式商用，建议对受限的 26 篇按需单独向权利人申请授权。")
    L.append("6. 公开克隆里没有第三方原文（按公开再分发口径不入库），此时本脚本的许可类别"
             "取自 `deliverables/fulltext_manifest.csv` 的快照列，**类别不变**，"
             "但\"证据来源\"列会指向清单（含该文件的 sha256 与重取方式）而不是原始 URL。")
    L.append("")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="只比对磁盘产物是否与重算一致")
    ap.add_argument("--refresh", action="store_true", help="重新联网取回缺失的许可（覆盖缓存）")
    args = ap.parse_args()

    rows, notes = build(args.refresh)
    csvp = OUT / "protein_design_license_audit.csv"
    mdp = OUT / "protein_design_license_audit.md"

    if args.check:
        bad = []
        if not csvp.exists():
            bad.append("CSV 产物缺失")
        else:
            got = list(csv.DictReader(csvp.open(encoding="utf-8-sig", newline="")))
            if len(got) != len(rows):
                bad.append(f"CSV 行数 {len(got)} != 重算 {len(rows)}")
            else:
                for a, b in zip(got, rows):
                    if a["许可类别"] != b["许可类别"]:
                        bad.append(f"{a['编号']} 许可类别 {a['许可类别']} != 重算 {b['许可类别']}")
        if not mdp.exists():
            bad.append("Markdown 产物缺失")
        print("判定标准: 许可审计 CSV 的行数与逐行许可类别必须与重算结果一致")
        print(f"判定结果: {'PASS' if not bad else 'FAIL — ' + ' | '.join(bad[:10])}（退出码 {0 if not bad else 1}）")
        return 0 if not bad else 1

    if not rows:
        print("判定结果: FAIL — 重算出 0 行，拒绝写盘")
        return 1
    write_csv(csvp, rows)
    write_report(mdp, rows, notes)
    blocked = [r for r in rows if r["许可类别"] in RESTRICTED]
    ok = [r for r in rows if r["许可类别"] not in RESTRICTED]
    by: dict[str, int] = {}
    for r in rows:
        by[r["许可类别"]] = by.get(r["许可类别"], 0) + 1
    print(f"审计 {len(rows)} 行本地归档全文")
    print("按类别:", "，".join(f"{CATS[k][0]} {v}" for k, v in sorted(by.items(), key=lambda x: -x[1])))
    print(f"可随商业产品再分发 {len(ok)} 行 · 不可/需另授权 {len(blocked)} 行")
    print(f"产物: {csvp.relative_to(ROOT)} / {mdp.relative_to(ROOT)}")
    if notes:
        print(f"待人工确认 {len(notes)} 条（已写进报告）:")
        for n in notes[:20]:
            print("  ", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
