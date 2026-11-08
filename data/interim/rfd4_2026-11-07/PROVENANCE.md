# RFD4-Proteina 取证来源与文件哈希（2026-11-07）

本目录是前沿引用 `[S21]`（官方 README/model card）与 `[S22]`（预印本正文）的本底稿。
所有引句都按本目录内的文件逐字核验；`RFD4_paper_text.txt` 是 PDF 的可复现抽取物。

| 文件 | 大小 | sha256 | 来源 |
|---|---|---|---|
| `RFD4-Proteina_README.md` | 14,915 B | `e3327fb127c36d9ff3d464caf14afbbd76ded521158a6be1abf860c11169fa64` | https://github.com/RosettaCommons/RFD4-Proteina （默认分支 raw） |
| `HF_RFD4-Proteina_README.md` | 21,173 B | `38479d8e4c6e46ed7e1ec4ece0dd02c358ae46d73d56790c44be813201fd9b98` | https://huggingface.co/nvidia/RFD4-Proteina （model card） |
| `LICENSE-BSD-3-Clause.txt` | 1,533 B | `0927a01536709c20efa64834482fd4d50c9bb954353dbcf35c95a98675545470` | https://github.com/RosettaCommons/RFD4-Proteina/blob/main/LICENSE （上游许可证原文，随 README 一并再分发） |
| `RFD4_paper_text.txt` | 282,879 B / 272,125 字符 | `16107aa0850c7e7dfdd10d0251d5ec6a0c1f6f9b2ac838d45ab3a7c7f4773141` | 由下列 PDF 抽取，见下方命令 |
| `RFD4-Proteina_paper.pdf` | 54,797,449 B | `33f4efb4833763a76b84b6989b1e56c01cec0dd697ea83d056387feb821b8bcd` | https://rfd4-proteina.org/assets/paper/RFD4-Proteina.pdf |

**两份 README 是随仓库分发的第三方文件**（BSD 3-Clause，允许再分发），条件是保留版权声明与
许可证全文——因此把上游 LICENSE 原文一并取回存为 `LICENSE-BSD-3-Clause.txt`（见上表）。
本库的署名位置见根目录 NOTICE 第 3 节。

**PDF 不入 git**（见仓库 `.gitignore` 注释）：单文件 54.8 MB，是仓库其余内容的数倍；
下游只用它的纯文本，而纯文本已入库并逐字节可复现。需要原 PDF 时按上表 URL 重取，
用上表 sha256 校验后再跑下面的抽取命令，得到的 `RFD4_paper_text.txt` 应与上表 sha256 一致。

抽取命令（PyMuPDF）：

```python
import fitz
d = fitz.open('RFD4-Proteina_paper.pdf')
out = []
for i, p in enumerate(d):
    out.append('===== PAGE %d =====' % (i + 1))
    out.append(p.get_text())
open('RFD4_paper_text.txt', 'w', encoding='utf-8').write('\n'.join(out))
```

已知抽取形态（不是原文错误）：`˚A` 是 Å 的抽取形态，`107` 是 10^7 的抽取形态，
`10 3`／`10 4` 是 10^3／10^4 上标的抽取形态，行尾断词（如 "screen-" + "ing"）保留原样。
引句比对必须先做 NFC 归一与空白折叠，否则断行/断词处会假阴性。

## 核验记录

- 抽取代理对 `rfd4_paper_findings.md` 内 127 条合格引句（≥20 字符且 ≥12 字母）逐字比对，127/127 通过；
  另有 1 条报警经复核为误报（该行同时含 PAGE 19 与 p24 标记，引句实际归属 p24，文件标注正确）。
- 主会话另抽查 18 条最高风险数字（89/288、15/1,000、67→4、8/9、100/102、66.5→8.4、t=0.99、
  12/18、188→158、18/60、denominators 规则等），全部在原句处命中。
- **未派第二独立复核代理**。本目录不声称等同于库内 P0 的"逐字引句门禁 + 身份体检"流程。
