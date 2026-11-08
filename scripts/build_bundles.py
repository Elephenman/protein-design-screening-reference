#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把参考库打成两个可迁移的包，并生成"喂给别的 AI"的分层纯文本 digest。

两个包（都写到 deliverables/bundles/，该目录被 .gitignore 排除，发布走 GitHub Release）：

1. `protein_design_reference_full_<date>.zip`
   完整迁移包 = git 可见的全部文件（作者原创部分：卡片、总表、台账、模板、迭代协议、
   脚本、调研底稿、许可审计与清单）。
   换机器时用它可以重建整个工作树并复跑全部门禁。
   **不含第三方原文**（公开仓库 = 公开再分发）：需要某一份时按
   `deliverables/fulltext_manifest.csv` 的路径与"重取方式"取回并校验 sha256。
   也不含被 `.gitignore` 排除的大二进制，例如 RFD4 预印本原 PDF（54.8 MB，按
   `data/interim/rfd4_2026-11-07/PROVENANCE.md` 的 URL + sha256 重取）。
2. `protein_design_reference_ai_<date>.zip`
   AI 投喂包 = 卡片 + 总表 + 台账 + 工作流/模板/迭代协议 + 脚本 + 调研底稿，
   **不含** `fulltext/` 与 `data/interim/`（那两块是各出版商/PMC 的抽取缓存与抓取日志，
   喂给模型没有增量信息，只涨体积）。
   例外是 `AI_INCLUDE` 白名单里的三份归纳件（RFD4 事实台账、PROVENANCE、迭代证据台账）——
   模板与迭代协议正文直接链接它们，剔掉会让包内链接断掉。
   另附 `ai_ingest/` 分层 digest：tier0 索引 → tier1 工作流与判据 → tier2 全部卡片正文。

用法：

    python scripts/build_bundles.py            # 生成两包 + digest + manifest
    python scripts/build_bundles.py --check    # 只校验磁盘上的包与 manifest 是否一致
    python scripts/build_bundles.py --ai-only  # 只出 AI 包（调试用）

确定性：文件按相对路径排序写入，zip 时间戳固定为本次构建日期，因此同一份内容重复构建得到同样的
文件清单与同样的 manifest 哈希（zip 本身字节还依赖 deflate 实现，不作保证）。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "bundles"
DIGEST = OUT / "ai_ingest"

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def est_tokens(text: str) -> int:
    """粗估 token：中日韩字符按 1 token/字，其余按 4 char/token。方法在 digest 里如实标注。"""
    cjk = len(CJK.findall(text))
    return cjk + max(0, len(text) - cjk) // 4


def tracked_files() -> list[str]:
    """git 可见的全部文件 = 已跟踪 + 未被 .gitignore 排除的新文件。

    用 `--others --exclude-standard` 而不是只用 `ls-files`：前者让"新建但还没 add"的文档也能进包，
    否则每轮改版都要先 commit 才能打包，包内会静默缺掉最新文件。被忽略的大二进制（如 RFD4 原 PDF）
    不会出现在这里。
    """
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard"],
                         capture_output=True, text=True, check=True).stdout
    return sorted(set(p for p in out.splitlines() if p))


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


AI_EXCLUDE = (
    re.compile(r"^data/literature_cards/fulltext/"),
    re.compile(r"^data/interim/"),
    re.compile(r"^tmp/"),
)
# 例外：这两份是模板/迭代协议正文直接链接的**归纳件**（不是出版商原文、不含全文缓存），
# 剔掉会让包内链接断掉。RFD4 原 PDF 与抽出的全文文本仍然不进 AI 包（许可与体积）。
AI_INCLUDE = (
    re.compile(r"^data/interim/rfd4_2026-11-07/(rfd4_paper_findings|PROVENANCE)\.md$"),
    re.compile(r"^data/interim/iteration_evidence_2026-11-07\.md$"),
)
# 许可与署名文件必须随每个包走：没有 LICENSE 的包等于无授权地再分发。
AI_MUST_INCLUDE = ("LICENSE", "NOTICE", "CITATION.cff")
AI_EXCLUDE_TOP = {rel(OUT) }


def ai_file_list(files: list[str]) -> list[str]:
    """AI 包 = 全部内容 − 全文缓存/抓取日志/tmp − 内部派工文件 + 少量正文直接链接的归纳件。"""
    internal = re.compile(r"DISPATCH|_dispatch|queue\.tsv|rollout_status|selfcheck|fetch_log|batches\.tsv")
    keep = []
    for f in files:
        if any(rx.match(f) for rx in AI_INCLUDE):
            keep.append(f)
            continue
        if any(rx.match(f) for rx in AI_EXCLUDE):
            continue
        if internal.search(f):
            continue
        keep.append(f)
    return sorted(keep)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------- digest ----

TIER1_SRC = [
    "README.md",
    "deliverables/PUBLISH_NOTE.md",
    "deliverables/protein_design_workflow.md",
    "deliverables/protein_design_workflow_template.md",
    "deliverables/protein_design_workflow_iteration.md",
    "deliverables/protein_design_workflow_template_branch_binder.md",
    "deliverables/protein_design_workflow_template_branch_enzyme.md",
    "deliverables/protein_design_workflow_template_branch_peptide.md",
    "deliverables/frontier_methods_2025_2026.md",
    "deliverables/protein_design_workflow_summary.txt",
    "deliverables/protein_design_license_audit.md",
]


def build_digest(today: str) -> dict[str, int]:
    """生成 ai_ingest/ 下的分层 digest，返回 {相对路径: 估算 token}。"""
    sizes: dict[str, int] = {}
    card_dir = ROOT / "data" / "literature_cards"
    cards = sorted(p for p in card_dir.glob("*.md") if not p.name.startswith(("README", "AGENT_RULES", "DISPATCH", "run")))
    dup = {}
    for p in cards:
        dup.setdefault(p.name.split("_")[0], []).append(p.name)
    dups = {k: v for k, v in dup.items() if len(v) > 1}
    dup_note = ""
    if dups:
        dup_note = ("\n> **卡文件数与行数的差额**：本包有 {n} 个卡文件，对应 {rows} 行文献。差额来自 {detail}"
                    "——同一行存在两张卡（同一篇的早期登记版与后续版），台账 `精读卡文件` 列指向的是"
                    "早期命名那一张；两张都保留，因为删除会切断已有的引句核验链。引用时以台账指向为准。\n").format(
            n=len(cards), rows=len(cards) - sum(len(v) - 1 for v in dups.values()),
            detail="、".join(f"{k}（{' / '.join(v)}）" for k, v in sorted(dups.items())))

    tier0 = f"""# 蛋白设计筛选参考库 · 给 AI 的入口（构建日 {today}）

这是一份**逐字核验过**的蛋白设计/筛选文献参考库，152 行文献、每行背后一张十节精读卡（个别行有两张，见下方差额说明）。
你收到本包时按下面的顺序读，不要一次全读。

## 分层读取顺序

| 层 | 文件 | 内容 | 估算 token |
|---|---|---|---|
| T0 | 本文件 | 是什么、怎么用、禁令 | — |
| T1 | `tier1_core.md` | 项目 README + 证据工作流 + **可执行工作流模板（主模板+三分支）** + **多轮迭代协议（含真实轮次台账）** + 前沿方法核验 + 口径统计 | {sizes.get('tier1_core.md', 0):,} |
| T2 | `tier2_cards.md` | {len(cards)} 个精读卡文件全文（十节：元信息/解决什么/难点/方法工作流/数字台账/作者原话/我们的推断/局限/可迁移性/溯源） | 见该文件头 |
| T3 | `tier3_ledgers/` | 机器台账 CSV（证据台账 152 行、判据台账 679 行）+ 文献总表 152 行 × 27 列 | 结构化数据，按需检索 |
{dup_note}

**AI 投喂包不含论文全文**（本包与完整迁移包都不含第三方原文：公开仓库 = 公开再分发，
第三方原文只登记在 `deliverables/fulltext_manifest.csv`，需要哪份按表里的"重取方式"取回并校验 sha256）。
因此卡里每条引句你只能查到"它声明的底稿路径 + 该底稿的 sha256"，不能在此包内复核原文。
本包的定位是**判据、阈值、成本与流程口径的参考**，不是原文数据库。

**许可**：本包内属于作者原创的内容适用包内 `LICENSE`；第三方论文全文**不在本包内**，
逐篇许可类别与证据见 `tier3_ledgers/protein_design_license_audit.csv`，
逐份文件的 sha256 与重取方式见 `tier3_ledgers/fulltext_manifest.csv`。
卡里的英文短引句是**引用**（不是全文再分发），每条带 `[文献编号]`，出处可在 T3 台账回查；
许可受限来源的引句已按"引用预算"截到引用级（单条 ≤100 字符、同一来源行合计 ≤600 字符），
截短后仍逐字命中同一份底稿。

## 引用本库时必须遵守的三条

1. **分母跟着数字走**：in silico 通过率 / 表征子集比例 / 末端实测池命中率是三回事，引用任何百分数都要带上它卡里 §4 写的分母。
2. **证据级别不许升级**：卡 §0 的 FULLTEXT 表示有本地全文可逐字核验；DEGRADED 表示只到摘要级/二级来源，
   其阈值与步骤细节**不许**被补全或转述成原文结论。
3. **不许跨目标借阈值**：结合体的 pAE_interaction/ipTM 阈值、适配体 FEP 命中率、展示库通量，不得当成酶活或
   其它功能的判据与成功概率。每张卡 §8 逐条写死了这条边界。

## 编号约定

`B*`=Baker 组，`Z*`=周如鸿组，`C*`=曹龙兴组，`K*`=通用方法学与成本，`M-K*`=口径审计补条，
`B06; C02` 这类合并号表示跨组同文。编号可在 T3 的证据台账里按行查到全部字段。

## 版本与校验

构建日 {today}；每文件 sha256 见包内 `manifest_full.csv` / `manifest_ai.csv`；包级哈希见 `SHA256SUMS.txt`。
"""
    write_text(DIGEST / "tier0_index.md", tier0)

    parts = ["# T1 · 工作流与模板（合并自项目 README 与 deliverables/）\n"]
    for f in TIER1_SRC:
        p = ROOT / f
        if not p.exists():
            raise SystemExit(f"digest 缺少 T1 来源文件：{f}（先生成再打包，不许写占位）")
        parts.append(f"\n\n---\n\n# 来源文件：{f}\n\n")
        parts.append(read(p))
    t1 = "".join(parts)
    write_text(DIGEST / "tier1_core.md", t1)
    sizes["tier1_core.md"] = est_tokens(t1)

    cp = [f"# T2 · {len(cards)} 个精读卡文件（对应 152 行文献）\n\n",
          f"构建日 {today}。每卡前有一行 `===== <编号> | <文件> =====` 分隔。\n",
          "卡内引句声明的底稿路径在本包内不可解析（AI 投喂包不含全文缓存）。\n",
          "同行两张卡的情况见 tier0 的差额说明；引用时以台账 `精读卡文件` 列指向的那张为准。\n"]
    for p in cards:
        cp.append(f"\n\n===== {p.name.split('_')[0]} | data/literature_cards/{p.name} =====\n\n")
        cp.append(read(p))
    t2 = "".join(cp)
    write_text(DIGEST / "tier2_cards.md", t2)
    sizes["tier2_cards.md"] = est_tokens(t2)

    led = DIGEST / "tier3_ledgers"
    led.mkdir(parents=True, exist_ok=True)
    for f in ["data/protein_design_literature.csv",
              "deliverables/protein_design_workflow_evidence.csv",
              "deliverables/protein_design_workflow_criteria_ledger.csv",
              "deliverables/protein_design_license_audit.csv",
              "deliverables/fulltext_manifest.csv",
              "deliverables/quote_budget_ledger.csv",
              "deliverables/quote_budget_notes_ledger.csv"]:
        src = ROOT / f
        dst = led / Path(f).name
        dst.write_bytes(src.read_bytes())
    (DIGEST / "HOW_TO_FEED.md").write_text(
        f"""# 怎么把这个库喂给一个 AI

1. 先只给 `tier0_index.md`（约 1–2k token）。让模型复述三条禁令，确认它没有把命中率当概率、没有跨目标借阈值。
2. 再给 `tier1_core.md`（约 {sizes['tier1_core.md']:,} token 粗估）。这是回答"该用什么判据、阈值多少、花多少钱"所需的全部。
3. 需要具体某篇文献时**按编号取卡**：在 `tier2_cards.md` 里搜 `===== B09 ` 这样的分隔行，只把那一张卡塞进上下文；
   整份 T2 约 {sizes['tier2_cards.md']:,} token，别一次性全喂。
4. 结构化问题（"哪些行用了 MD""哪个判据出现最多"）走 `tier3_ledgers/` 里的 CSV，不要靠模型记忆。
5. token 估算方法：中日韩字符按 1 token/字、其余按 4 字符/token，是粗估，不同分词器会有出入。

需要原文逐字复核时，按 `tier3_ledgers/fulltext_manifest.csv` 里该底稿的路径与"重取方式"取回，
并用同一张表里的 sha256 校验；本包与完整迁移包都不含第三方原文（公开仓库口径）。
""",
        encoding="utf-8",
    )
    return sizes


# ---------------------------------------------------------------- bundling ----

def build_zip(zip_path: Path, pairs: list[tuple[str, str]], stamp: tuple[int, int, int, int, int, int]) -> list[tuple[str, int, str]]:
    """pairs = [(压缩包内路径, 磁盘相对路径)]；manifest 记磁盘路径，包内用干净路径。"""
    rows: list[tuple[str, int, str]] = []
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for arc, relpath in pairs:
            p = ROOT / relpath
            if not p.exists():
                raise SystemExit(f"清单里的文件不存在：{relpath}")
            data = p.read_bytes()
            zi = zipfile.ZipInfo(arc, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, data)
            rows.append((relpath, len(data), sha256(data)))
    return rows


def write_manifest(path: Path, rows: list[tuple[str, int, str]]) -> str:
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["path", "bytes", "sha256"])
        w.writerows(rows)
    body = path.read_bytes()
    return sha256(body)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验已生成的包与 manifest")
    ap.add_argument("--ai-only", action="store_true")
    args = ap.parse_args(argv)

    today = date.today().isoformat()
    stamp = (int(today[:4]), int(today[5:7]), int(today[8:10]), 12, 0, 0)

    if args.check:
        bad = 0
        for mf in sorted(OUT.glob("manifest_*.csv")):
            rows = list(csv.reader(mf.open(encoding="utf-8", newline="")))[1:]
            for p, n, h in rows:
                f = ROOT / p
                if not f.exists():
                    print(f"MISSING {p}")
                    bad += 1
                elif sha256(f.read_bytes()) != h:
                    print(f"HASH    {p}")
                    bad += 1
        print(f"判定标准: manifest 里每个路径都存在且 sha256 与磁盘一致")
        print(f"判定结果: {'PASS 0 处不符' if bad == 0 else f'FAIL {bad} 处不符'}")
        return 0 if bad == 0 else 1

    files = tracked_files()
    OUT.mkdir(parents=True, exist_ok=True)
    sizes = build_digest(today)
    print(f"digest: tier1≈{sizes['tier1_core.md']:,} tok, tier2≈{sizes['tier2_cards.md']:,} tok")
    results = []
    if not args.ai_only:
        full_zip = OUT / f"protein_design_reference_full_{today}.zip"
        rows = build_zip(full_zip, [(f, f) for f in files], stamp)
        mh = write_manifest(OUT / "manifest_full.csv", rows)
        results.append((full_zip, len(rows), mh))
    ai_zip = OUT / f"protein_design_reference_ai_{today}.zip"
    ai_files = ai_file_list(files)
    ai_pairs = [(f, f) for f in ai_files]
    # digest 在磁盘上位于 deliverables/bundles/ai_ingest/（被 gitignore），包内提到顶层 ai_ingest/，
    # 否则收件人要按 deliverables/bundles/ai_ingest/... 找入口，与 tier0 里写的相对路径不符。
    ai_pairs += [(d.relative_to(OUT).as_posix(), rel(d)) for d in sorted(DIGEST.rglob("*")) if d.is_file()]
    ai_pairs = sorted(set(ai_pairs))
    rows = build_zip(ai_zip, ai_pairs, stamp)
    mh = write_manifest(OUT / "manifest_ai.csv", rows)
    results.append((ai_zip, len(rows), mh))

    with (OUT / "SHA256SUMS.txt").open("w", encoding="utf-8", newline="") as fh:
        for zp, _, _ in results:
            fh.write(f"{sha256(zp.read_bytes())}  {zp.name}\n")
    for zp, n, _ in results:
        print(f"{zp.name}: {n} 文件 · {zp.stat().st_size/1024/1024:.2f} MiB")
    print(f"清单条目合计: 完整包 {len(files)} · AI 包 {len(set(ai_files))}")
    print("判定标准: 包内文件数 = 清单行数；manifest 每行 sha256 与磁盘一致；AI 包不含 fulltext/ 与 interim/"
          "（AI_INCLUDE 白名单里的三份归纳件除外）；AI 包必须带 LICENSE/NOTICE/CITATION.cff")
    leak = [p for p in ai_files
            if p.startswith(("data/literature_cards/fulltext/", "data/interim/"))
            and not any(rx.match(p) for rx in AI_INCLUDE)]
    print(f"判定结果: {'PASS AI 包 0 处缓存泄漏' if not leak else 'FAIL 泄漏 ' + str(len(leak))}")
    # 完整包同样不得含第三方原文：以清单里"随仓库分发=否"的路径为准（清单是机器生成的）。
    manifest = ROOT / "deliverables" / "fulltext_manifest.csv"
    full_leak: list[str] = []
    if manifest.exists():
        with manifest.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                if row.get("随仓库分发", "").strip() == "否" and row["path"] in set(files):
                    full_leak.append(row["path"])
    else:
        print("FAIL 缺 deliverables/fulltext_manifest.csv：无法判定完整包是否含第三方原文")
        full_leak.append("(manifest missing)")
    print(f"判定结果: {'PASS 完整包 0 处第三方原文' if not full_leak else 'FAIL 完整包含第三方原文 ' + str(len(full_leak))}")
    # 许可文件缺失 = 无授权再分发。缺一个就红。
    missing_legal = [f for f in AI_MUST_INCLUDE if f not in ai_files]
    if missing_legal:
        print(f"FAIL AI 包缺许可文件: {missing_legal}")
    else:
        print("PASS AI 包带齐 LICENSE / NOTICE / CITATION.cff")
    print("找出来没有: 本脚本只判'打包内容是否如声明'，不判文献内容对错（那走 verify_literature_cards.py）")
    return 1 if (leak or full_leak) else 0


if __name__ == "__main__":
    sys.exit(main())
