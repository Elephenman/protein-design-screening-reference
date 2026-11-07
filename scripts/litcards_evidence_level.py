#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从卡片 §0 的「证据级别」行推导 CSV 总表 `证据级别` 列的机器标签。

为什么要它：`证据级别` 不在那 14 个回填键里，所以卡写完之后，这一列一直停留在建库初期的旧值。
实测 152 行里有 58 行的 CSV 取值与卡片判定相反——包括 Z01/Z03/Z05 这类"CSV 写全文级、卡里明写
未获正文"的行，正是本库自己禁止的"证据级别升级"。

推导规则（只用卡里的话，不另设判据）：
  1. 卡 §0 的证据级别行含「全文级」或「正文级 …逐字命中」→ FULLTEXT
  2. 否则含「摘要级 / 二级来源 / 未获正文 / 题录级 / 已核验DOI / 未标注」→ DEGRADED
  3. 两者都读不出 → UNKNOWN（须人工看卡）

写进 CSV 的格子格式：`<机器标签>｜<中文口径>`，例如
  FULLTEXT｜全文级（本次独立复核 PMC9117152）
  DEGRADED｜摘要级/二级来源/未获正文（本次经 PubMed/Crossref 核对，未读正文）
机器可 grep（列首就是标签），人也能读懂；细节仍以卡 §0 为准，卡路径在同一行的 `精读卡文件` 列。
旧值里的括注（如"本次独立复核 PMC…"）保留，但当旧值与新标签矛盾时整段丢弃——
保留一句与事实相反的括注，比丢掉它更糟。
"""
from __future__ import annotations

import re

DEGRADED_KW = ("摘要级", "二级来源", "未获正文", "题录级", "已核验DOI", "未标注")
FULLTEXT_KW = ("全文级", "正文级")
PAREN = re.compile(r"^(.*?)（(.*?)）\s*$")


def _level_text(card_body: str) -> str:
    """在 §0 表格里找证据级别那一行。

    不能只认 `| 证据级别 |`：卡里还有 `| 本卡证据级别 |`（C10）、`| 证据级别（本卡口径）|` 这类写法，
    只匹配前者会把这些行判成 UNKNOWN，再落进表里就成了"未标注"。
    """
    for ln in card_body.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) >= 2 and "证据级别" in cells[0]:
            return cells[1]
    return ""


def tag_from_card(card_body: str) -> str:
    """从卡 §0 的证据级别行推出机器标签。

    只认**开头那一句的断言**，不认整格里出现的词。早先版本用"整格含'全文级'就算 FULLTEXT"，
    结果 C10 翻车：它的级别写的是「未获正文／二级来源转录（…卡内不声明正文级核验…）」，
    "正文级"三个字出现在解释句里，被当成了 FULLTEXT 断言——把一行没取到正文的降级卡写成了全文级。
    所以规则改成：先剥掉强调符号与空白，取开头；开头断言"全文级/正文级"才 FULLTEXT，
    否则开头出现降级词就是 DEGRADED。
    """
    s = _level_text(card_body)
    if not s:
        return "UNKNOWN"
    head = re.sub(r"[*`\s]", "", s)[:60]
    if head.startswith("全文级") or head.startswith("正文级"):
        return "FULLTEXT"
    if any(k in head for k in DEGRADED_KW):
        return "DEGRADED"
    return "UNKNOWN"


def _old_category(old: str) -> str:
    if not old:
        return ""
    lead = PAREN.match(old.strip())
    lead = (lead.group(1) if lead else old).strip()
    if "全文级" in lead or "正文级" in lead:
        return "FULLTEXT"
    if any(k in lead for k in DEGRADED_KW):
        return "DEGRADED"
    return ""


ZH = {
    "FULLTEXT": "全文级",
    "DEGRADED": "摘要级/二级来源/未获正文",
    "UNKNOWN": "未标注",
}


def cell(tag: str, old: str = "") -> str:
    zh = ZH.get(tag, ZH["UNKNOWN"])
    paren = ""
    m = PAREN.match((old or "").strip())
    if m and _old_category(old) == tag:
        paren = f"（{m.group(2).strip()}）"
    return f"{tag}｜{zh}{paren}"
