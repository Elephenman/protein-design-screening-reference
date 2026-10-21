#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""卡片里 CSV 回填块的唯一定义：核验器与回写脚本共用，防止两边字段清单漂移。

块写法（放在卡片 ## 9. 溯源 一节内，原样一小段）：

<!--CSV回填
work_type=论文
target=LTK、ALK、IL-2Rα site1/site2、IL-10Rα
backbone_generation=Rosetta 界面设计协议出骨架 + LayerDesign/ProteinMPNN 出序列
computational_filters=pAE_interaction；复合物 Cα RMSD；target_delta_sap；ddG
thresholds=pAE_interaction<10；复合物 Cα RMSD<5 Å
md_used=否
qm_used=否
experimental_methods=酵母表面展示+递减浓度分选+深测序；E. coli 表达+BLI
pipeline_counts=~2M/靶 → ~20,000 送测(15K 物理+5K AF2) → 80,000 基因 → 成功 1–17/靶
hit_rate=成功率近 10×；两靶 8×/30×；绝对 <1%；site2 0 个
best_metric=未记录（本文只给 SC50 口径与高 nM 段）
cost_or_stat_note=~30 GPU-秒/设计；AF2 通过仅 ~2.3%；100 CPU-s = 1 GPU-s
role_in_timeline=把 Cao 2022 的近百万标注变成筛子考卷，定下 pAE_interaction 闸口
source_pointer=data/literature_cards/fulltext/B09_…；sources/baker.md:120-133
CSV回填-->

规则：值里不许换行；确实没有的写 `未记录（原因）`，不许留空、不许猜。
"""
from __future__ import annotations

import re

CSV_KEYS = [
    "work_type", "target", "backbone_generation", "computational_filters", "thresholds",
    "md_used", "qm_used", "experimental_methods", "pipeline_counts", "hit_rate",
    "best_metric", "cost_or_stat_note", "role_in_timeline", "source_pointer",
]

# CSV_KEYS -> 中文表头前缀（用于 DictReader 的宽表头匹配）
CSV_COL = {
    "work_type": "文献类型", "target": "设计对象", "backbone_generation": "候选生成方法",
    "computational_filters": "计算筛选判据", "thresholds": "阈值数字", "md_used": "是否用MD",
    "qm_used": "是否用QM", "experimental_methods": "实验验证手段",
    "pipeline_counts": "候选数递减", "hit_rate": "实验命中率", "best_metric": "Kd或活性最好值",
    "cost_or_stat_note": "成本/统计", "role_in_timeline": "在方法演进链的位置",
    "source_pointer": "原文出处指针",
}

BLOCK = re.compile(r"<!--CSV回填\s*\n(.*?)\nCSV回填-->", re.S)


def slug(acc: str) -> str:
    """编号里可能带分号与空格（如 'B06; C02'），文件名只留字母数字和连字符。"""
    return re.sub(r"[^A-Za-z0-9]+", "-", acc).strip("-")


def parse_card(text: str) -> tuple[dict[str, str], list[str]]:
    """返回 (键值, 错误列表)。缺块、缺键、空值、多行值都算错。"""
    m = BLOCK.search(text)
    if not m:
        return {}, ["卡片没有 <!--CSV回填 ... CSV回填--> 块"]
    vals: dict[str, str] = {}
    errs: list[str] = []
    for ln in m.group(1).splitlines():
        ln = ln.strip()
        if not ln or "=" not in ln:
            continue
        k, v = ln.split("=", 1)
        k = k.strip()
        if k not in CSV_KEYS:
            errs.append(f"回填块有未知键 {k}")
            continue
        vals[k] = v.strip()
    for k in CSV_KEYS:
        if k not in vals:
            errs.append(f"回填块缺键 {k}")
        elif not vals[k]:
            errs.append(f"回填块键 {k} 值为空（没有就写 未记录（原因））")
    return vals, errs
