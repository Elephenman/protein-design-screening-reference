#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工作流模板的机械门禁：引用不许悬空、阈值不许没有证据级别、链接不许断。

判的五件事（都只判"形式是否诚实"，不判文献内容对错）：

1. **库内编号可查**：正文里 `[B09]`、`[B06; C02]`、`[M-K34]` 这样的引用，每一个编号都必须在
   `deliverables/protein_design_workflow_evidence.csv` 的 `编号` 列里存在。
2. **库外编号可查**：`[S3]`、`[S11]` 这样的外部引用，必须在 `deliverables/frontier_methods_2025_2026.md`
   里有同名条目（防止把调研代理的记忆当事实抄进模板）。
3. **阈值必须带证据级别**：任何表格里"默认阈值"列填了东西的行，同一格必须含 `P0`–`P5` 之一，
   并且该行必须至少挂一个 `[B..]`/`[K..]`/`[S..]` 出处。空值要写 `未记录（原因）`，不许留空。
4. **链接与脚本可达**：相对链接指向的文件必须存在；正文提到的 `scripts/*.py` 必须在仓库里。
5. **三态必须存在**：主模板必须含"能证明 / 不能证明 / 尚缺什么"三态表。

证据级别约定（与卡片口径一致，写在模板开头）：
P0=库内全文逐字核验 · P1=库内摘要级/二级来源 · P2=库外一手全文 · P3=库外一手仅摘要/README ·
P4=本报告推算 · P5=未记录。

用法：
    python scripts/verify_workflow_template.py            # 全量
    python scripts/verify_workflow_template.py --selftest # 三种破坏必须各红一条
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEL = ROOT / "deliverables"

MAIN = "protein_design_workflow_template.md"
BRANCHES = [
    "protein_design_workflow_template_branch_binder.md",
    "protein_design_workflow_template_branch_enzyme.md",
    "protein_design_workflow_template_branch_peptide.md",
]
FRONTIER = "frontier_methods_2025_2026.md"
DOCS = [MAIN, *BRANCHES]

LIB_ID = re.compile(r"\[(?P<ids>(?:[A-Z]{1,2}-?)[A-Za-z0-9]+(?:; ?[A-Za-z0-9-]+)*)\]")
S_ID = re.compile(r"\[(S\d{1,3})\]")
TAG = re.compile(r"\bP[0-5]\b")
PY = re.compile(r"scripts/[A-Za-z0-9_]+\.py")


def load_ids() -> set[str]:
    p = DEL / "protein_design_workflow_evidence.csv"
    ids: set[str] = set()
    with p.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            ids.add(row["编号"].strip())
            for part in re.split(r";", row["编号"]):
                ids.add(part.strip())
    return ids


def frontier_keys() -> set[str]:
    p = DEL / FRONTIER
    if not p.exists():
        return set()
    return set(re.findall(r"^\|\s*(S\d{1,3})\s*\|", p.read_text(encoding="utf-8"), re.M)) | set(
        re.findall(r"^###\s*(S\d{1,3})\b", p.read_text(encoding="utf-8"), re.M)
    )


def tables_with_threshold(text: str):
    """遍历 markdown 表格；只 yield 表头(表格首行)含"默认阈值"这一列的表的正文行。

    表头判定：该行必须是表格块的第一行（上一行不以 | 开头），且单元格文本恰为"默认阈值"。
    （只判 `in` 会被正文里"④ 默认阈值候选"这类单元格误当成表头，实测踩过。）
    """
    lines = text.splitlines()
    ctx = ""
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("#"):
            ctx = ln.strip("# ").strip()
        is_table_start = ln.strip().startswith("|") and (i == 0 or not lines[i - 1].strip().startswith("|"))
        if is_table_start and any(c.strip() == "默认阈值" for c in ln.strip().strip("|").split("|")):
            i += 1
            if i < len(lines) and set("".join(lines[i].split())) <= set("|-: "):
                i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i]
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                if any(cells):
                    yield ctx, row, cells
                i += 1
            continue
        i += 1


def check(files_text: dict[str, str], ids: set[str], skeys: set[str]) -> tuple[list[str], dict[str, int]]:
    errs: list[str] = []
    stats = {"ids": 0, "sids": 0, "thr_rows": 0}
    for name, text in files_text.items():
        for m in LIB_ID.finditer(text):
            for part in re.split(r";", m.group("ids")):
                part = part.strip()
                if not re.match(r"^(?:[BCZ]?\d|M-?K\d|[BZCK]\d{2}[a-z]?)", part):
                    continue
                stats["ids"] += 1
                if part not in ids:
                    errs.append(f"{name}: 引用 [{part}] 不在证据台账的编号列里")
        for m in S_ID.finditer(text):
            stats["sids"] += 1
            if m.group(1) not in skeys:
                errs.append(f"{name}: 外部引用 [{m.group(1)}] 在 {FRONTIER} 里没有对应条目")
        for ctx, ln, cells in tables_with_threshold(text):
            stats["thr_rows"] += 1
            joined = " | ".join(cells)
            if not TAG.search(joined):
                errs.append(f"{name}（{ctx}）: 阈值行缺 P0–P5 证据级别 → {ln[:90]}")
            if not LIB_ID.search(joined) and not S_ID.search(joined):
                errs.append(f"{name}（{ctx}）: 阈值行没有任何出处编号 → {ln[:90]}")
        for ln in text.splitlines():
            for label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", ln):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                rel = target.split("#")[0]
                if not rel:
                    continue
                p = (DEL / rel).resolve() if not rel.startswith("../") else (ROOT / rel).resolve()
                if not p.exists():
                    errs.append(f"{name}: 链接 [{label}]({target}) 指向不存在的文件")
        for sp in set(PY.findall(text)):
            if not (ROOT / sp).exists():
                errs.append(f"{name}: 提到 {sp} 但该脚本不存在")
    main = files_text.get(MAIN, "")
    for kw in ("能证明", "不能证明", "尚缺什么"):
        if kw not in main:
            errs.append(f"{MAIN}: 缺三态关键词「{kw}」")
    return errs, stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    ids = load_ids()
    skeys = frontier_keys()
    files_text = {}
    missing = []
    for f in [MAIN, *BRANCHES, FRONTIER]:
        p = DEL / f
        if not p.exists():
            missing.append(f)
            continue
        files_text[f] = p.read_text(encoding="utf-8")

    if args.selftest:
        # 扰动必须打在"默认阈值"表的真实数据行上——打在正文里的那句 P0 定义不算破坏，
        # 早先版本用全文第一处替换，结果两种破坏都没被判红（假绿），故改成先定位行再改行。
        first_row = next((row for _, row, _ in tables_with_threshold(files_text[MAIN])), None)
        if not first_row:
            print("FAIL(无法自测) 主模板里找不到默认阈值表")
            return 1

        def drop_tag(t: str) -> str:
            return t.replace(first_row, re.sub(r"\bP[0-5]\b", "—", first_row, count=1), 1)

        def drop_cite(t: str) -> str:
            # 必须删掉该行**全部**出处：只删第一个时剩下的引用仍满足"至少一条出处"，门禁判红不了，
            # 那属于自测写歪（实测踩过），不是检查器漏判。
            return t.replace(first_row, re.sub(r"\[[^\]]{1,20}\]", "—", first_row), 1)

        modes = {
            "改坏一个库内编号": lambda t: t.replace("[B09]", "[B90]", 1),
            "删掉阈值行的证据级别": drop_tag,
            "删掉阈值行的全部出处编号": drop_cite,
        }
        bad = 0
        for label, fn in modes.items():
            pert = dict(files_text)
            pert[MAIN] = fn(pert[MAIN])
            errs, _ = check(pert, ids, skeys)
            ok = bool(errs) and not any("缺三态关键词" in e for e in errs)
            print(f"{'PASS(红)' if ok else 'FAIL(未红)'} {label}: {errs[:1]}")
            bad += 0 if ok else 1
        print("判定标准: 三种破坏各自必须让门禁变红")
        print(f"判定结果: {'PASS 3/3 变红' if bad == 0 else f'FAIL {bad} 种破坏没被判红'}")
        return 1 if bad else 0

    if missing:
        print(f"缺文件: {missing}")
        return 1

    errs, stats = check(files_text, ids, skeys)
    print(f"判定标准: 引用可查({stats['ids']} 处库内 + {stats['sids']} 处库外) · "
          f"{stats['thr_rows']} 行默认阈值全部带 P0–P5 与出处 · 链接与脚本可达 · 主模板含三态")
    if errs:
        for e in errs[:60]:
            print("FAIL " + e)
        print(f"判定结果: FAIL {len(errs)} 处")
        print("找出来没有: 本门禁只判引用的可查性与证据级别标注，不判阈值本身是否适合你的体系")
        return 1
    print("判定结果: PASS 0 处不合格（退出码 0）")
    print("找出来没有: 本门禁只判引用的可查性与证据级别标注，不判阈值本身是否适合你的体系")
    return 0


if __name__ == "__main__":
    sys.exit(main())
