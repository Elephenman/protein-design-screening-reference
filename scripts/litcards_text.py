#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全文文本归一化的唯一实现：抓取脚本和核验脚本必须用同一个函数，
否则"卡里引句命中全文"会因为两侧处理方式不同而假红/假绿。
"""
from __future__ import annotations

import html
import re
import unicodedata

_TRANS = (("\u201c", '"'), ("\u201d", '"'), ("\u2018", "'"), ("\u2019", "'"),
          ("\u2013", "-"), ("\u2014", "-"), ("\u2212", "-"), ("\u00a0", " "))


def strip_tags(xml: str) -> str:
    """去掉 XML/JATS 标签；ref-tag 里的数字编号留在原位（核验时引句不得跨它）。"""
    xml = re.sub(r"<[^>]+>", " ", xml)
    return re.sub(r"\s+", " ", xml).strip()


def norm(s: str) -> str:
    """实体解码 + 引号/破折号统一 + 空白折叠。不改词，不改大小写。"""
    s = unicodedata.normalize("NFC", html.unescape(s))
    for a, b in _TRANS:
        s = s.replace(a, b)
    s = s.replace("\u0251", "a")  # 拉丁 alpha(ɑ) 归一成 a，避免 Cɑ/Cα 型抄写差异
    return re.sub(r"\s+", " ", s).strip()


def to_text(raw: str) -> str:
    return norm(strip_tags(raw)) if raw.lstrip().startswith("<") else norm(raw)
