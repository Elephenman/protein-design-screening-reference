#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把工作流模板编译成一页可审核的 HTML（数据全部来自模板与台账，不在这里手打数字）。

输出：
- `deliverables/protein_design_workflow_visual.html` — 独立单文件（可直接双击打开/随包迁移）
- `deliverables/protein_design_workflow_visual.fragment.html` — 同样内容但只含 body 片段，供会话内展示

用法：
    python scripts/build_workflow_visual.py            # 生成
    python scripts/build_workflow_visual.py --check    # 数量对账（阈值条目数、引用可查率、S 条目数）

对账口径与 verify_workflow_template.py 一致：表头首行必须有单元格文本恰好等于"默认阈值"，
其下的每一行算一条待审条目。两边数目不等就说明有一侧解析跑偏。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEL = ROOT / "deliverables"
FILES = {
    "main": ("主模板 · 十阶段", DEL / "protein_design_workflow_template.md"),
    "iteration": ("多轮迭代", DEL / "protein_design_workflow_iteration.md"),
    "binder": ("分支 A · 结合体", DEL / "protein_design_workflow_template_branch_binder.md"),
    "enzyme": ("分支 B · 酶", DEL / "protein_design_workflow_template_branch_enzyme.md"),
    "peptide": ("分支 C · 肽与大环", DEL / "protein_design_workflow_template_branch_peptide.md"),
    "evidence": ("把握度边界", DEL / "protein_design_workflow.md"),
}
FRONTIER = DEL / "frontier_methods_2025_2026.md"

CITE = re.compile(r"\[(S\d{1,3}|[A-Z]{1,2}-?\d{1,3}[a-z]?(?:; ?[A-Za-z0-9-]+)*)\]")
PTAG = re.compile(r"\bP([0-5])\b")
HEADING = re.compile(r"^(#{2,4})\s+(.*)$")


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep(cells: list[str]) -> bool:
    return bool(cells) and all(set(c) <= set("-: ") and c for c in cells)


def strip_md(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return text.strip()


def cites(text: str) -> list[str]:
    out: list[str] = []
    for m in CITE.findall(text):
        for part in re.split(r";", m):
            part = part.strip()
            if part and part not in out:
                out.append(part)
    return out


def parse_doc(path: Path) -> list[dict]:
    """返回 [{heading, sub, tables:[{kind, header, rows:[{cells, text, p, cites}]}], lists, paras}]"""
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[dict] = []
    h2 = h3 = ""
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = HEADING.match(ln)
        if m:
            lvl, title = len(m.group(1)), strip_md(m.group(2))
            if lvl == 2:
                h2, h3 = title, ""
            elif lvl == 3:
                h3 = title
            else:
                h3 = h3 or title
            i += 1
            continue
        if ln.strip().startswith("|"):
            header = split_row(ln)
            j = i + 1
            if j < len(lines) and is_sep(split_row(lines[j])):
                j += 1
            rows = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = split_row(lines[j])
                if any(cells):
                    joined = " | ".join(cells)
                    rows.append({"cells": cells, "p": (PTAG.search(joined).group(0) if PTAG.search(joined) else ""),
                                 "cites": cites(joined)})
                j += 1
            blocks.append({"h2": h2, "h3": h3, "header": header, "rows": rows, "kind": classify(header)})
            i = j
            continue
        if re.match(r"^\s*\d+\.\s+", ln) or ln.startswith("- ") or ln.startswith("* "):
            items = []
            while i < len(lines) and (re.match(r"^\s*(\d+\.|-|\*)\s+", lines[i]) or lines[i].startswith("  ")):
                if lines[i].strip():
                    items.append(strip_md(re.sub(r"^\s*(\d+\.|[-*])\s+", "", lines[i])))
                i += 1
            blocks.append({"h2": h2, "h3": h3, "kind": "list", "items": items, "header": [], "rows": []})
            continue
        if ln.strip() and not ln.startswith("```"):
            blocks.append({"h2": h2, "h3": h3, "kind": "para", "text": strip_md(ln), "header": [], "rows": []})
        i += 1
    return blocks


def classify(header: list[str]) -> str:
    h = [c.strip() for c in header]
    if "默认阈值" in h:
        return "threshold"
    if "陈述" in h and "状态" in h:
        return "triage"
    if "不许做" in h:
        return "forbid"
    if "闸口" in h:
        return "gate"
    if h and h[0] in ("档", "层次"):
        return "budget"
    if h[:2] == ["标签", "含义"]:
        return "legend"
    if "填什么" in h:
        return "params"
    if h[0] == "阶段":
        return "flow"
    return "table"


def load_ledger() -> dict[str, dict]:
    out: dict[str, dict] = {}
    keep = ["标题", "年份", "期刊或预印本", "底稿形态", "文献类型", "计算筛选判据", "阈值数字",
            "候选数递减", "实验命中率", "成本/统计", "精读卡文件", "人物组"]
    for r in csv.DictReader((DEL / "protein_design_workflow_evidence.csv").open(encoding="utf-8-sig", newline="")):
        rec = {k: (r.get(k) or "")[:600] for k in keep}
        for part in re.split(r";", r["编号"]):
            out[part.strip()] = {"id": part.strip(), **rec}
        out[r["编号"].strip()] = {"id": r["编号"].strip(), **rec}
    return out


def load_frontier() -> dict[str, dict]:
    txt = FRONTIER.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    for ln in txt.splitlines():
        if not ln.strip().startswith("|"):
            continue
        cells = split_row(ln)
        if not cells or not re.fullmatch(r"S\d{1,3}", cells[0]):
            continue
        out[cells[0]] = {"key": cells[0], "claim": cells[1], "source": cells[2],
                         "grade": cells[3], "use": cells[4], "review": cells[5] if len(cells) > 5 else ""}
    return out


def build() -> dict:
    ledger, frontier = load_ledger(), load_frontier()
    data = {"tabs": [], "ledger": ledger, "frontier": frontier, "counts": {}}
    n_thr = n_cites = 0
    missing: list[str] = []
    for key, (title, path) in FILES.items():
        blocks = parse_doc(path)
        for b in blocks:
            for row in b["rows"]:
                n_cites += len(row["cites"])
                for c in row["cites"]:
                    if c.startswith("S"):
                        if c not in frontier:
                            missing.append(f"{key}:{c}")
                    elif c not in ledger:
                        missing.append(f"{key}:{c}")
                if b["kind"] == "threshold":
                    n_thr += 1
        data["tabs"].append({"key": key, "title": title, "file": path.name,
                             "blocks": [{k: v for k, v in b.items() if k != "header"} | {"header": b["header"]}
                                        for b in blocks]})
    data["counts"] = {"thresholds": n_thr, "cites": n_cites, "missing": len(missing),
                      "ledger_ids": len(ledger), "frontier_keys": len(frontier)}
    data["missing_list"] = missing[:40]
    return data


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#1c2024;--mut:#5b6470;--line:#dfe3e8;--p0:#1b7f4d;--p1:#a06a00;
--p2:#0b62a4;--p3:#6b4fa0;--p4:#8a6d3b;--p5:#8b2e2e;--flag:#c1440e}
*{box-sizing:border-box}
.body-font{color:var(--ink);font:15px/1.55 "Segoe UI","Microsoft YaHei",system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:20px 22px 90px;background:var(--bg);min-height:620px}
h1{font-size:22px;margin:0 0 4px}
.sub{color:var(--mut);font-size:13px;margin-bottom:14px}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.tabs button{border:1px solid var(--line);background:var(--card);padding:7px 13px;border-radius:20px;cursor:pointer;font-size:14px}
.tabs button.on{background:#1c2024;color:#fff;border-color:#1c2024}
section.grp{margin:0 0 26px}
h2.grp{font-size:17px;margin:0 0 3px;padding-bottom:4px;border-bottom:2px solid var(--line)}
h3.grp{font-size:15px;color:var(--mut);margin:10px 0 8px}
.para{color:var(--mut);font-size:13.5px;margin:6px 0}
.rows{display:grid;gap:10px}
.row{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--line);border-radius:8px;padding:11px 13px}
.row.threshold{border-left-color:#0b62a4}
.row.triage{border-left-color:#1b7f4d}
.row.forbid{border-left-color:#8b2e2e}
.row.gate{border-left-color:#6b4fa0}
.rtop{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.rname{font-weight:650;font-size:15px}
.chip{display:inline-block;font-size:11.5px;padding:2px 8px;border-radius:11px;color:#fff;white-space:nowrap}
.P0{background:var(--p0)}.P1{background:var(--p1)}.P2{background:var(--p2)}.P3{background:var(--p3)}.P4{background:var(--p4)}.P5{background:var(--p5)}
.cell{margin-top:6px;font-size:14px}
.lab{color:var(--mut);font-size:12px;letter-spacing:.02em;text-transform:none}
.val{margin-top:1px}
.val.thr{font-family:ui-monospace,Consolas,monospace;font-size:13.5px}
.cite{display:inline-block;border:1px solid var(--line);background:#fafbfc;border-radius:5px;padding:1px 7px;
margin:2px 4px 0 0;font-size:12.5px;cursor:pointer;font-family:ui-monospace,Consolas,monospace}
.cite:hover{border-color:#0b62a4;background:#eef6fb}
.marks{margin-top:9px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.marks button{border:1px solid var(--line);background:#fff;border-radius:6px;padding:3px 9px;font-size:12.5px;cursor:pointer}
.marks button.on{background:var(--flag);color:#fff;border-color:var(--flag)}
.marks input{flex:1;min-width:180px;border:1px solid var(--line);border-radius:6px;padding:4px 8px;font-size:12.5px}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:9px 0 10px;margin-bottom:12px}
.bar .stat{font-size:13px;color:var(--mut)}
.bar button{border:1px solid #1c2024;background:#1c2024;color:#fff;border-radius:6px;padding:5px 12px;cursor:pointer;margin-left:6px}
.drawer{position:fixed;right:0;top:0;width:min(520px,92vw);height:100vh;background:#fff;border-left:1px solid var(--line);
box-shadow:-6px 0 22px rgba(0,0,0,.13);transform:translateX(102%);transition:transform .18s;padding:16px 18px;overflow:auto;z-index:20}
.drawer.open{transform:none}
.drawer h4{margin:2px 0 8px;font-size:16px}
.drawer .kv{border-top:1px solid var(--line);padding:7px 0;font-size:13.5px}
.drawer .close{position:absolute;right:14px;top:12px;border:1px solid var(--line);background:#fff;border-radius:6px;padding:2px 9px;cursor:pointer}
pre.out{background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px;white-space:pre-wrap;font-size:12.5px;min-height:80px}
.legend{display:flex;gap:8px;flex-wrap:wrap;margin:4px 0 10px}
.count{font-variant-numeric:tabular-nums;font-weight:650}
@media (max-width:720px){.row{padding:10px}}
"""

JS = r"""
const D=window.__WFDATA__;
const marks=Object.create(null), notes=Object.create(null);
let tabKey="main";
function esc(s){return (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function pchip(p){return p?'<span class="chip '+p+'">'+p+(p==="P0"?" 全文逐字":p==="P1"?" 摘要级":p==="P2"?" 库外一手全文":p==="P3"?" 库外仅摘要/README":p==="P4"?" 本报告推算":" 未记录")+'</span>':'<span class="chip P5">无级别</span>';}
function citeChips(list){return list.map(c=>'<span class="cite" data-c="'+esc(c)+'">'+esc(c)+'</span>').join("");}
function cellOf(cells,i){return cells[i]!==undefined?cells[i]:"";}
function rowHtml(b,r,idx){
  const c=r.cells, isThr=b.kind==="threshold";
  const name=esc(cellOf(c,0));
  let body="";
  if(isThr){
    body='<div class="cell"><div class="lab">默认阈值</div><div class="val thr">'+esc(cellOf(c,1))+'</div></div>'+
         '<div class="cell"><div class="lab">不适用／失灵时怎么办</div><div class="val">'+esc(cellOf(c.length>4?c.length-1:3))+'</div></div>';
  } else {
    for(let k=1;k<c.length;k++){
      if(!c[k]) continue;
      body+='<div class="cell"><div class="lab">'+esc(b.header[k]||("列"+k))+'</div><div class="val">'+esc(c[k])+'</div></div>';
    }
  }
  const id=tabKey+"#"+idx;
  const mk=["keep","doubt","change"].map(m=>'<button data-id="'+id+'" data-m="'+m+'" class="'+(marks[id]===m?"on":"")+'">'+
      (m==="keep"?"保留":m==="doubt"?"存疑":"要改")+'</button>').join("");
  return '<div class="row '+b.kind+'"><div class="rtop"><span class="rname">'+name+'</span>'+
    (isThr||r.p?pchip(r.p):'')+'</div>'+body+
    (r.cites.length?'<div class="cell"><div class="lab">出处</div><div>'+citeChips(r.cites)+'</div></div>':'')+
    '<div class="marks">'+mk+'<input data-n="'+id+'" placeholder="批注（可选）：这里要改什么" value="'+esc(notes[id]||"")+'"></div></div>';
}
function blockHtml(tab){
  let out="", lastH2=null, n=0;
  for(const b of tab.blocks){
    if(b.h2 && b.h2!==lastH2){
      if(lastH2!==null) out+="</section>";
      out+='<section class="grp"><h2 class="grp">'+esc(b.h2)+"</h2>"; lastH2=b.h2;
    }
    if(b.kind==="para"){out+='<p class="para">'+esc(b.text)+"</p>";continue;}
    if(b.kind==="list"){out+='<div class="row table">'+b.items.map(i=>'<div class="cell">'+esc(i)+"</div>").join("")+"</div>";continue;}
    if(!b.rows.length) continue;
    const label=b.header.filter(Boolean).map(esc).join(" · ");
    out+='<h3 class="grp">'+esc(b.h3?b.h3+" — ":"")+label+"（"+b.rows.length+" 行）</h3><div class=\"rows\">";
    for(const r of b.rows){out+=rowHtml(b,r,n++);}
    out+="</div>";
  }
  if(lastH2!==null) out+="</section>";
  return out;
}
function openCite(id){
  const f=D.frontier[id], l=D.ledger[id], el=document.getElementById("drawer");
  let h="";
  if(f){
    h='<h4>['+id+'] 库外前沿条目</h4><div class="kv"><b>'+esc(f.claim)+'</b></div>'+
      '<div class="kv"><div class="lab">一手来源</div>'+esc(f.source)+'</div>'+
      '<div class="kv"><div class="lab">取证级别</div>'+esc(f.grade)+'　<div class="lab">复核</div>'+esc(f.review)+'</div>'+
      '<div class="kv"><div class="lab">模板里用到</div>'+esc(f.use)+'</div>'+
      '<div class="kv para">全文见 deliverables/frontier_methods_2025_2026.md 的 S 节。</div>';
  } else if(l){
    h='<h4>['+id+'] 库内行</h4><div class="kv"><b>'+esc(l["标题"])+'</b><br><span class="para">'+
      esc(l["年份"])+" · "+esc(l["期刊或预印本"])+" · "+esc(l["人物组"])+" · "+esc(l["底稿形态"])+" · "+esc(l["文献类型"])+"</span></div>"+
      '<div class="kv"><div class="lab">计算筛选判据</div>'+esc(l["计算筛选判据"])+"</div>"+
      '<div class="kv"><div class="lab">阈值原文</div>'+esc(l["阈值数字"])+"</div>"+
      '<div class="kv"><div class="lab">候选递减</div>'+esc(l["候选数递减"])+"</div>"+
      '<div class="kv"><div class="lab">实验命中率（含分母）</div>'+esc(l["实验命中率"])+"</div>"+
      '<div class="kv"><div class="lab">成本／统计</div>'+esc(l["成本/统计"])+"</div>"+
      '<div class="kv"><div class="lab">精读卡</div>'+esc(l["精读卡文件"])+"</div>";
  } else {
    h='<h4>['+id+'] 台账里查不到</h4><div class="kv para">这条引用没有对应记录——正是审核要找的问题之一。</div>';
  }
  el.innerHTML='<button class="close" onclick="document.getElementById(\'drawer\').classList.remove(\'open\')">关闭</button>'+h;
  el.classList.add("open");
}
function refresh(){
  const tab=D.tabs.find(t=>t.key===tabKey);
  document.getElementById("content").innerHTML=blockHtml(tab);
  document.querySelectorAll(".tabs button").forEach(b=>b.classList.toggle("on",b.dataset.k===tabKey));
  const ids=Object.keys(marks);
  const cnt={keep:0,doubt:0,change:0};ids.forEach(i=>cnt[marks[i]]++);
  document.getElementById("stat").innerHTML='本模板阈值条目 <span class="count">'+D.counts.thresholds+
    '</span> 行 · 引用 <span class="count">'+D.counts.cites+'</span> 处（台账查不到 <span class="count">'+D.counts.missing+
    '</span> 处）· 已标：保留 '+cnt.keep+" · 存疑 "+cnt.doubt+" · 要改 "+cnt.change;
}
function report(){
  const lines=[];
  for(const t of D.tabs){
    let idx=0;
    for(const b of t.blocks){
      for(const r of b.rows){
        const id=t.key+"#"+idx++;
        if(!marks[id]&&!notes[id]) continue;
        const head=b.h3||b.h2||t.title;
        lines.push("- **["+t.title+"｜"+esc(head)+"]** "+(marks[id]==="change"?"要改":marks[id]==="doubt"?"存疑":"保留")+
          "：`"+r.cells[0]+"`"+(notes[id]?(" —— "+notes[id]):""));
      }
    }
  }
  document.getElementById("out").textContent=lines.length?lines.join("\n"):"（还没有任何标记或批注；先在行上点“要改／存疑”或写批注）";
  return lines;
}
function wire(){
  document.addEventListener("click",e=>{
    const t=e.target;
    if(t.classList.contains("cite")){openCite(t.dataset.c);return;}
    if(t.dataset.m){const id=t.dataset.id;marks[id]=marks[id]===t.dataset.m?"":t.dataset.m;refresh();return;}
    if(t.id==="btabs")return;
  });
  document.addEventListener("input",e=>{if(e.target.dataset.n!==undefined){notes[e.target.dataset.n]=e.target.value;}});
  document.getElementById("tabs").addEventListener("click",e=>{if(e.target.dataset.k){tabKey=e.target.dataset.k;refresh();}});
  document.getElementById("btn-report").onclick=()=>{report();document.getElementById("outbox").style.display="block";};
  document.getElementById("btn-copy").onclick=async()=>{
    const txt=report().join("\n");if(!txt)return;
    try{await navigator.clipboard.writeText(txt);document.getElementById("btn-copy").textContent="已复制";}
    catch(err){const ta=document.createElement("textarea");ta.value=txt;document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove();document.getElementById("btn-copy").textContent="已复制";}
    setTimeout(()=>document.getElementById("btn-copy").textContent="复制审核意见",1500);
  };
  document.getElementById("btn-clear").onclick=()=>{Object.keys(marks).forEach(k=>delete marks[k]);Object.keys(notes).forEach(k=>delete notes[k]);refresh();};
  document.getElementById("drawer").addEventListener("click",e=>{if(e.target.id==="drawer")e.target.classList.remove("open");});
}
wire();refresh();
"""


def html(data: dict, standalone: bool) -> str:
    body = (f'<div class="wrap">'
            f'<h1>蛋白设计工作流模板 · 审核视图</h1>'
            f'<div class="sub">编译自 {len(data["tabs"])} 份模板/文档；每条阈值带证据级别（点编号看原文字段），'
            f'行尾可标 保留／存疑／要改 并写批注，最后点"生成审核意见"。本页不重复结论，只把模板摊开给你审。</div>'
            f'<div class="bar"><div class="stat" id="stat"></div>'
            f'<div style="margin-top:7px"><button id="btn-report">生成审核意见</button>'
            f'<button id="btn-copy">复制审核意见</button><button id="btn-clear">清空标记</button></div></div>'
            f'<div class="legend">' + " ".join(
                f'<span class="chip P{i}">P{i}</span>' for i in range(6)) +
            ' <span class="para">P0 全文逐字核验 · P1 摘要级/二级来源 · P2 库外一手全文 · P3 库外仅摘要/README · P4 本报告推算 · P5 未记录</span></div>'
            f'<div class="tabs" id="tabs">' + "".join(
                f'<button data-k="{t["key"]}" class="{"on" if t["key"] == "main" else ""}">{t["title"]}'
                f'<span class="para"> · {t["file"]}</span></button>' for t in data["tabs"]) + '</div>'
            f'<div id="content"></div>'
            f'<div id="outbox" style="display:none"><h2 class="grp">审核意见（Markdown）</h2><pre class="out" id="out"></pre></div>'
            f'</div><div class="drawer" id="drawer"></div>')
    # 只有字面 </script 会提前终结脚本块；数据与脚本里都只替换这一种（其余 </ 无害，别乱动）。
    payload = ("<script>window.__WFDATA__="
               + json.dumps(data, ensure_ascii=False).replace("</script", "<\\/script")
               + ";</script>")
    script = "<script>" + JS.replace("</script", "<\\/script") + "</script>"
    if not standalone:
        return f'<style>{CSS}</style><div class="body-font">{body}</div>{payload}{script}'
    return (f'<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>蛋白设计工作流模板 · 审核视图</title>'
            f'<style>{CSS}body{{margin:0;background:var(--bg)}}</style></head><body class="body-font">'
            f'{body}{payload}{script}</body></html>')


def gate_counts() -> tuple[int, int, list[str]]:
    """期望值从门禁脚本现算，不在本文件里写死。

    写死过 85/21，模板一改就要手改两处、漏改就假绿（实测踩过的维护陷阱）。
    改成单一事实来源：门禁数到多少，可视化就必须渲染出多少。
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import verify_workflow_template as gate

    texts = {f: (DEL / f).read_text(encoding="utf-8") for f in [*gate.DOCS, gate.FRONTIER]}
    errs, stats = gate.check(texts, gate.load_ids(), gate.frontier_keys())
    return stats["thr_rows"], len(gate.frontier_keys()), errs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    data = build()
    c = data["counts"]
    if args.check:
        exp_thr, exp_s, gate_errs = gate_counts()
        print(f"判定标准: 阈值条目数==门禁现算({exp_thr}) · 引用缺失==0 · S 条目数==门禁现算({exp_s}) · 门禁自身 0 处不合格")
        ok = (c["thresholds"] == exp_thr and c["missing"] == 0
              and c["frontier_keys"] == exp_s and not gate_errs)
        print(f"判定结果: 阈值 {c['thresholds']}/{exp_thr} · 引用 {c['cites']} 处缺失 {c['missing']} · "
              f"S {c['frontier_keys']}/{exp_s} · 门禁不合格 {len(gate_errs)} 处 · {'PASS' if ok else 'FAIL'}")
        if data["missing_list"]:
            print("缺失样本:", data["missing_list"][:10])
        for e in gate_errs[:5]:
            print("门禁:", e)
        return 0 if ok else 1

    (DEL / "protein_design_workflow_visual.html").write_text(html(data, True), encoding="utf-8")
    (DEL / "protein_design_workflow_visual.fragment.html").write_text(html(data, False), encoding="utf-8")
    print(f"生成: {DEL/'protein_design_workflow_visual.html'} ({(DEL/'protein_design_workflow_visual.html').stat().st_size:,} B)")
    print(f"生成: {DEL/'protein_design_workflow_visual.fragment.html'} ({(DEL/'protein_design_workflow_visual.fragment.html').stat().st_size:,} B)")
    print(f"判定标准: 阈值 {c['thresholds']} 行 · 引用 {c['cites']} 处（缺失 {c['missing']}）· S 条目 {c['frontier_keys']} · 台账行 {c['ledger_ids']}")
    print(f"判定结果: {'PASS' if c['missing'] == 0 else 'FAIL 有引用查不到'}")
    return 1 if c["missing"] else 0


if __name__ == "__main__":
    sys.exit(main())
