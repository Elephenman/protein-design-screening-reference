# [B30] 双组分蛋白纳米材料的自动化设计——把 ProteinMPNN 放进流水线，命中率不变、算力与人工砍掉几个数量级

de Haas Robbert J., Brunette N., Goodson A., Dauparas J., Yi S.Y., Yang E.C., Dowling Q., Nguyen H., Kang A., Bera A.K., Sankaran B., de Vries R., Baker D., King N.P.（华盛顿大学 IPD / Wageningen / LBNL）
PNAS 2024, 121(13): e2314646121 · DOI 10.1073/pnas.2314646121 · PMID 38502697 · PMCID PMC10990136
CC BY-NC-ND 4.0 · https://pmc.ncbi.nlm.nih.gov/articles/PMC10990136/ · 预印本 bioRxiv 10.1101/2023.08.04.551935（PMC10418170）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **B30**（组：Baker组） |
| 本地全文底稿 | `data/interim/baker_lit/ft/autotwo_comp2024.txt`（57,382 B，Europe PMC `fullTextXML` 抽取，2026-10-16 抓取，见 `inventory.json` fetch_channel=epmc_fulltext） |
| 对照记录 | `sources/baker.md` 第 392–405 行（原卡，本卡在此基础上补 Methods 的 7 条阈值与全流程规模） |
| 证据级别 | **全文级**（本卡全部引句均可在上述本地全文里逐字命中；见第 9 节） |
| 未取到的部分 | SI Appendix（Fig. S1–S7、Table S1/S2 的原始数字）、PDB 结构文件、设计模型 zenodo 数据集（10.5281/zenodo.8278877）。凡涉及这些的地方本卡明写"正文未给出" |
| 对现有 CSV/底稿的两处更正 | ① CSV `设计对象` 写"T33 型 icosahedral cage"，全文口径是 **tetrahedral**（两组三聚体排在四面体点群三次轴的两极，各 4 份拷贝），不是二十面体；② CSV `计算筛选判据` 写"过滤阈值未给具体数值"，**Methods 明确给了 7 条阈值**（见第 3 节 S7），该条已过期 |

## 1. 这篇到底解决什么（一句话）

把 Rosetta 设计双组分自组装蛋白纳米材料时**又慢又必须靠结构生物学家人工改突变**这两件事，换成 ProteinMPNN 出界面序列 + 一套固定阈值的自动过滤：**同样的实验命中率（17% vs 18%），算力从"每条几分钟"降到"每条约 1 秒"，人工干预降到零**，而且顺带发现 ProteinMPNN 设计的界面极性更高，因此更多材料能从两个独立纯化的组分在体外自组装出来（6/13 vs Rosetta 的 1 个）。


## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **瓶颈是"人工"，不只是"算力"（这是本文的出发点）**。
   现象/证据："The design of protein-protein interfaces using physics-based design methods such as Rosetta"，以及 "the designed interfaces often rely primarily on hydrophobic packing and require significant manual"。最硬的一条证据是回头看旧数据："This difference between the two methods is even more remarkable considering that the Rosetta"——也就是说 Rosetta 那一侧的可用结果是**人工修剪出来的**，不是流水线自己产出的。
   **应对**：换生成器而不是调势函数。序列端整体换成 ProteinMPNN，并明确写出不人工介入："We selected a maximum of three variants of each original design for experimental characterization" + "without any manual intervention"。
   **留下的代价**：所谓 fully automated 指的是"取消人工修剪"，骨架采样、序列回环、界面打分仍然全在 Rosetta 里（SymDofMover / PackRotamerMover / Rosetta 度量），并不是脱离物理引擎的全自动。

2. **自动化流水线的每一个计算判据其实都没有预测力——作者自己承认，这是本文最重要的失败点**。
   现象/证据：正文原句 "Although none of the metrics evaluated were able"；同一件事在结果段也说过："We found that ProteinMPNN and Rosetta yielded"。注意方向性矛盾：**排序键 shape complementarity 恰恰是 Rosetta 那一侧更占优的指标**，而实验赢的是 ProteinMPNN。
   **应对**：把过滤器的职能从"预测会不会成功"降级为"控制送测预算 + 排除明显劣质"（7 条硬阈值 + 每 dock 上限 3 个），不再声称判据能挑出赢家。
   **代价**：判据本身没有被替换或改进，漏斗末端选出的 76 个是"最合物理口味"的子集；本文未解决（作者没有给出任何一个能区分成功/失败的设计前判据）。

3. **疏水 packing 给组装驱动力，同时也给未组装组分带来聚集**。
   现象/证据："While hydrophobic packing provides a strong"
   **应对**：把"界面极性"当成一个可测的产品属性来做对照（图 3 B–G 六项突变/极性统计 + 每个界面的极性残基占比："Quantification of the overall fraction of polar residues at each interface showed that ProteinMPNN designs on average had a higher fraction of polar side chains"），然后**直接测商业上真正在意的下游属性**——体外自组装："We were able to successfully purify both components of six complexes by IMAC and SEC (T33-06.1, T33-08.2, T33-11.1, T33-18.2, T33-22.2, and T33-24.3; Fig. 2 )" 与 "All six nanomaterials assembled efficiently and"。
   **代价**：13 个确证设计里只有 6 个能把两组分分别纯化并体外组装（46%）；正文没有逐个交代另外 7 个失败在哪一步。DLS 上 3 个设计仍有 >100 nm 聚集体峰（"a second aggregate peak of diameter >100 nm was"，但 "in all instances these peaks represented <1% of"）。

4. **在"物理法已经做成功过的 dock"上，自动化法反而出不来**。
   现象/证据："Although ProteinMPNN did not generate successful"——同一界面、同一残基集，换个序列生成器把已知成功案例重跑，5 个里 4 个没复现。
   **应对**：不做机理归因，改用 **dock 层并集**来报成功（两法合计 13/27 个 dock 出过确证组装体），并把叙事重心放到新增覆盖上："Notably, successful designs were obtained for 8"；只保留唯一一个两法都成功的 dock（"One docked configuration yielded successful"）作为方法学可互换性的证据。
   **代价**：本文未解决——4 个已知 good dock 为什么失败没有解释；也没有对"同一 dock 换种子/换温度能不能救回来"做补充采样。

5. **阈值过筛后每个 dock 的产出量不均匀，预算规则被迫让步**。
   现象/证据："For each of the 27 docks,"（这就是 27×3=81 变成 76 的原因。）
   **应对**：不为凑数放宽阈值，接受每 dock 1–3 个的不均匀送测量，把上限 3 当作硬预算。
   **代价**：每个 dock 只有 1–3 次机会，dock 层面的结论（成功来自 9/27 个起始复合物）统计功效很低；正文没有做"阈值放宽一档，送测数与确证数各变多少"的敏感性分析。

6. **ProteinMPNN 默认不建模侧链，全自动流水线中途必须回到 Rosetta**。
   现象/证据："Although ProteinMPNN does not by default"；晶体层面也看到后果："The configurations of polar side chains around"
   **应对**：用 Rosetta threading + 全残基 repack 补出侧链，再靠晶体结构而不是打分来确认界面相互作用真的成立（"Comparing the side chains of the"）。
   **代价**：界面核心的氢键/离子对能复现，周边极性侧链构象偏差明显（作者归因于与水分子的相互作用，属定性解释，本文未量化）。


## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据/阈值 → 输出规模）

### 用了哪些方法（工具箱）

- **骨架**：不新生成骨架，而是对已有 27 个 T33 dock 做**刚体微扰采样**（Rosetta SymDofMover，属于 RPXDock 一类 docking 工具）："The symmetrical degrees of freedom of the T33"
- **序列**：ProteinMPNN 只改界面残基、其余固定："The interface sequences were optimized using"；对照臂是 Rosetta 设计（King 2020 的原 27 例）。
- **回环与打分**：Rosetta threading（resfiles）+ SymDofMover 重建完整对称组装 + PackRotamerMover 侧重排；评价用 7 个 Rosetta 侧的界面度量："To evaluate the structural"
- **实验**：双顺反子质粒共表达（一条 His 标签用于共纯化）→ 裂解液 native PAGE 快筛 → IMAC → SDS-PAGE 看共洗脱 + native PAGE 看组装 → SEC → 负染 EM + 2D class average 与计算投影比对 → 分组分纯化后体外 1:1 混装 → DLS → X 射线晶体学。
- **没有用的方法**：MD、QM、自由能微扰、机器学习置信度（AF2/RF2 的 pAE/pLDDT 在这篇里**一个都没当闸口用**——评价仍然是 Rosetta 物理量）。这点和 B09（AF2 pAE_interaction 判据）是两条完全不同的路线。

### 自动化流水线逐步骤（S1→S9 为下单前，S10 起为湿实验）

| # | 输入 | 操作 | 判据 / 阈值（原文数字） | 输出与规模 |
|---|---|---|---|---|
| S1 | King 2020 用 Rosetta 设计过的 27 个双组分 T33 复合物 | 取"四份 A 三聚体 + 四份 B 三聚体"排布在四面体三次轴两极的 T33 架构，作为重设计起点 | 原文未给"选哪些 dock"的阈值——**就是把旧的 27 个 dock 全部拿来**，为的是与 Rosetta 严格同条件对照 | 27 个 dock |
| S2 | 27 个 dock | Rosetta SymDofMover 微扰每个 building block 的刚体转动 ω 与平移 r | Δ0.5 Å 平移、Δ1° 旋转；每 dock 采 100 个 unique configurations | 2,700 个"近似但不同"的 dock 构象（每 dock 100） |
| S3 | 每 dock 构象 | 抽出共享同一界面的两个三聚体（一个 A、一个 B），沿用 King 2020 定义的同一组界面残基 | 界面残基集合与 Rosetta 原设计完全相同（保证可比）；ProteinMPNN 端"all other residues kept fixed"；后文只给出 45 positions considered for design，未说明是每侧还是每界面 | 每 dock 的界面设计任务 |
| S4 | S3 的构象 | ProteinMPNN 采样序列，sampling temperature 0.2 与 0.3、backbone noise 0.05 | 每构象 16 条序列；单价 "ProteinMPNN sequence design was rapid," | 1,600 条/dock；27 dock 合计 **43,200 条**（本卡按 100×16×27 推算） |
| S5 | 43,200 条序列 | 按 **ProteinMPNN loss score** 排序截断 | "Based on the loss score, the" → **top 50%** | 约 800 条/dock，合计约 21,600 条（推算） |
| S6 | S5 的序列 | threading 回原构象 + 全残基 repack（tetrahedral symmetry）补侧链，生成全原子设计模型 | "All residues were repacked"；无截断阈值 | 与 S5 同量级的全原子模型 |
| S7 | 全原子模型 | **7 条硬阈值联合过滤**（这是整条流水线唯一写明的判据集） | "Finally, a detailed evaluation" | 通过总数正文未给（只给了每 dock 上限后的 76） |
| S8 | S7 通过者 | 按 **shape complementarity** 从高到低，每 dock 最多取 3 个 | "For each of the 27 docks," | **76 个设计**（27×3=81，被 4 个 dock 的不足额削到 76），且 "This gave a total of 76 designs" |
| S9 | 76 个设计对 | 下单合成（Genscript，pET-29b(+)，NdeI/XhoI）："Synthetic genes for designed" | 双顺反子：两段 ORF 之间插第二个 RBS（AGAAGGAGATATCAT），只有 C 端更易接近的那条带 hexahistidine 标签 | **76 对组分 = 76 个可测设计**（对照臂 Rosetta 只送测过 27 个） |
| S10 | 76 对 | 2 mL E. coli 培养 → 裂解 → **native PAGE** 快筛 | 判据=迁移位置："Potential nanoparticle hits had" | **24 个疑似命中**（"Twenty-four designs yielded"）≈31.6% |
| S11 | 24 个疑似 | 放大到 1 L → IMAC → 重跑 native PAGE + SDS-PAGE 看哪对组分共洗脱 | "These 24 potential hits were"；共洗脱只是 "a suggestion of successful" | 进入 SEC 的候选（逐个数未给） |
| S12 | IMAC 洗脱液 | SEC（Superdex 200 Increase 10/300） | "Peaks eluting at ~13 mL strongly indicate nanoparticle formation and were fractionated and analyzed by SDS-PAGE to confirm the presence of both components." | **13 个**："Promising designs were then" |
| S13 | 13 个 | 负染 EM + 2D class average 与计算投影比对 | "Comparing 2D class averages of" | **13/13 结构确认**，即实验确证率 **13/76 = 17%**（Rosetta 臂 5/27 = 18%） |
| S14 | 13 个 | 分组分重建 + 单独纯化 + 1:1 摩尔比 ~25 µM 体外混装 + SEC/动态光散射 | 判据=EM 单分散 + DLS 出 ~15 nm 主峰、聚集体峰 <1% 质量 | **6 个**能两组分分别纯化并体外组装（Rosetta 臂只有 T33-15 一个） |
| S15 | 其中 3 个 | X 射线晶体学（PDB 8T6C / 8T6N / 8T6E） | 判据=与设计的骨架 RMSD | 0.92 / 1.14 / 0.63 Å（T33-18.2 / T33-27.1 / T33-28.3），最好分辨率 1.92 Å |

### 下单前削减了多少（本卡重点，逐层可核）

- 生成 **43,200 条序列**（27 dock × 100 构象 × 16 条）→ loss 取 top 50% ≈ **21,600** → 7 条硬阈值过滤 → 每 dock SC 前 3 → **下单 76 个设计**。
- 以"序列生成数 → 送测数"计：**约 568 倍削减**（76 / 43,200 ≈ 0.18%，本卡推算，正文只给 1,600 条/dock 与 76 这两个端点）。
- 以"dock 构象数 → 送测数"计：2,700 → 76 = **约 36 倍**（推算）。
- 关键对照：**这一整套削减没有花 GPU 训练、没有人工审序列**，只花 CPU 秒级采样 + 一次性阈值过滤；作者口径是 "ProteinMPNN had a similar"
- 湿实验侧的削减是**便宜的先筛**：76 → 24（native PAGE，2 mL 培养规模）→ 13（SEC）→ 13（EM 全确认）。**快筛的假阳率不低（24 个里只有 13 个过关），但快筛本身极便宜**，把贵的 1 L 表达只花在 24 个上。


## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段） |
|---|---|---|
| 27 | 起始 T33 dock 数（Rosetta 旧设计全集，本卡两臂共同起点） | "we used ProteinMPNN to generate" |
| 4 / 27（+1 例 T33-23 = 5/27） | Rosetta 臂旧确证数 | "In the original publication (" + 后续 EM 补一例 |
| Δ0.5 Å / Δ1° | 骨架微扰步长（平移 / 旋转） | Methods：sampled with Δ0.5 Å translation ( r ) and Δ1° rotation ( ω ) |
| 100 / dock（27×100 = 2,700，推算） | 每 dock 生成的构象数 | "and 100 unique configurations" |
| 16 / 构象；1,600 / dock；43,200（推算） | ProteinMPNN 采样序列数 | "A total of 16 sequences per" |
| T=0.2、0.3；backbone noise 0.05 | ProteinMPNN 采样温度与骨架噪声 | 同上句 |
| ~1 s / 序列（vs Rosetta 数分钟） | 序列生成单价 | "ProteinMPNN sequence design was" |
| top 50% | loss score 截断比例 | "Based on the loss score, the" |
| glycine = 0；Met < 5；aromatic < 5；clash < 3；SC > 0.5；界面强度 < 0 REU；埋藏 SASA > 1,000 Å² | 7 条硬阈值（本文唯一写明的判据集） | Methods 过滤句（见第 3 节 S7 完整引句） |
| 每 dock ≤ 3 | 预算上限（按 shape complementarity 排序） | "For each of the 27 docks," |
| 1 / 2 / 2 / 2（T33-15 / -12 / -16 / -29） | 4 个 dock 通过阈值不足额 | "with the exceptions of T33-15—where only 1 design passed the filter metrics—and T33-12, T33-16, and T33-29—where only 2 designs passed the filter metrics." |
| 76 | 下单（送测）设计数 | "This gave a total of 76 designs" |
| 24 | native PAGE 快筛疑似命中 | "Twenty-four designs yielded" |
| 13 | SEC 单峰 ~1 MDa 且 EM 确认 | "revealing 13 that eluted as" |
| 13/76 (17%) vs 5/27 (18%) | 两臂实验确证率 | "These results establish that" |
| 9 / 27 | 出过 ≥1 个成功设计的起始复合物数 | "The 13 successful designs were" |
| 0.52 Å / 16 个突变 / 45 个位置 | 同源成功设计间的平均差异 | "differing on average by only" |
| 8 | 旧 Rosetta 失败、ProteinMPNN 成功的 dock 数 | "Notably, successful designs" |
| 4 / 5 | ProteinMPNN 未能复现的旧确证纳米颗粒数 | "Although ProteinMPNN did not" |
| 13 / 27 | 两法并集的 dock 层成功数 | 同上一句后半 |
| 36 ± 5 vs 17 ± 3 | ProteinMPNN / Rosetta 每界面突变数 | "Given the same interface," |
| 59% vs 43% | T33-18.2 与 T33-18 的界面极性残基占比 | "For instance, T33-18.2 has a" |
| 6 / 13 | 能分别纯化两组分并体外组装的设计数 | "We were able to successfully" |
| 1（T33-15） | Rosetta 臂可做体外组装的设计数 | "By contrast, T33-15 was the" |
| 1:1、~25 µM、TBS（25 mM Tris pH 8.0 / 150 mM NaCl / 1 mM TCEP） | 体外组装条件 | "We mixed the components of each" |
| ~13 mL / ~15 nm / >100 nm / <1% | SEC 峰位 / DLS 主峰 / 聚集峰 / 聚集质量占比 | 图 4 图注："A scattering peak centered"、"For T33-06.1, T33-11.1, and T33-24.3, a second aggregate peak of diameter >100 nm was observed."、"in all instances these peaks" |
| 0.92 / 1.14 / 0.63 Å；1.92 Å | 三个晶体结构对设计模型的骨架 RMSD；最好分辨率 | "In each case, the crystal" |
| 0.72 Å / 33 个突变 / 11 个核心位 | 同一 dock 的 Rosetta(T33-28) 与 ProteinMPNN(T33-28.3) 界面差异 | "The designs had almost identical overall configurations, with a backbone RMSD of only 0.72 Å over the ASU. However, their interfaces differed by 33 mutations, of which 11 were at core positions." |
| >10 个 vs 0 个 | T33-28.3 与 T33-28 界面边界处的极性相互作用数 | "Several more polar residues at" |
| 8T6C / 8T6N / 8T6E（对照 4NWR） | PDB 号（T33-18.2 / T33-27.1 / T33-28.3；Rosetta 的 T33-28） | 图 5 图注与 Methods 数据 deposition 句 |


## 5. 结论——作者说了什么

1. **命中率没变，但成本与人力变了**：同一批 27 个 dock、同一组界面残基，ProteinMPNN 得 13/76（17%），Rosetta 得 5/27（18%）——"These results establish that"，且 "but much more simply and"，摘要口径是 "ProteinMPNN had a similar"
2. **准确率在高分辨率层面站得住**："These data establish that"（三个晶体结构骨架 RMSD 0.63–1.14 Å）
3. **界面化学真的不同，而且这个不同是好事**：ProteinMPNN 突变数翻倍、更少把极性改成疏水，界面极性残基占比更高；后果是 "Specifically, the lower tendency of ProteinMPNN-designed components to aggregate resulted in a higher fraction of materials that could be assembled in vitro from individually purified components."（6/13 vs Rosetta 的 1 例）
4. **自动化的意义是"可及性"**："In particular, its modest" ——以及 "As we have shown, this includes"
5. **作者明确没说的**：他们承认没有任何一个已评量度能区分成功与失败（见第 2.2 条），也没给出结合强度实测（"Although experimental determination of interface binding strength would be required to validate these predictions"）。"outperformed" 一词指的是效率与界面性质，不是命中率。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇卖的是"成本结构改造"，不是"判据进步"**。全流程的判断力仍来自 7 条 Rosetta 侧硬阈值 + shape complementarity 排序，而作者自己证明这套排序没有区分能力 → **命中率没提升是必然的**（判据没变强），提升的只是每条候选的算力单价（~1 s vs 数分钟）与人工。把它当"深度学习提高了成功率"的证据引用是错的。
2. **"每 dock 取前 3"是预算规则被伪装成判据**。它决定的只是"这一轮花多少钱"；正因如此，76 而不是 81 完全由阈值通过数决定，而不是由质量决定。→ 对我们：任何"取前 N"都应在报告里与"判据强度"分开列，别让人以为 N 是筛出来的。
3. **极性更高 = 可制造性更高，这是本文唯一被前瞻实验证实的"性质跃迁"**（6/13 可体外组装 vs Rosetta 1 例）。它的机理是"弱一点、极性一点的界面更适合分级组装"——作者自己也只说 "relatively weak interfaces can"，并且承认需要实测结合强度才能坐实。
4. **"已知成功起点重做反而失败"（4/5）是最该记住的一条**：自动化流水线的成功并不单调继承。同一界面残基集、同一 dock，换序列生成器会把旧成功案例做没。→ 对我们：任何"把已被验证过的模板重跑一遍新方法"的实验，都必须预期**净新增收益**而不是"至少不丢旧的"，否则会把旧成功案例白白消耗掉。
5. **他们把"便宜的先筛"放在湿实验最前面（2 mL 培养 + native PAGE），把贵的操作（1 L 表达、IMAC、SEC、EM、晶体学）逐级解锁**。这与 B09 的 YSD→BLI 逻辑一致：第一道关允许假阳（24→13），只要它便宜。→ 我们的第一道关（LC-MS/MS 产物身份）不便宜，所以这个"廉价粗筛"结构在我们这里**不能照搬**，只能照搬"逐级解锁贵操作"的顺序原则。
6. **两臂对照用的是同一批 dock、同一组界面残基**，因此"17% vs 18%"的对照在**任务难度上是干净的**（比 B09 跨靶的 8×/30× 更严格），但代价是分母极小（13/76、5/27），单个设计进出就能改动几个百分点——置信区间宽到不足以支持任何"效率比较之外的推断"。

## 7. 局限与失败（作者的 + 我们读出的）

- **作者自陈**：① "Although none of the metrics"（全部设计前判据无区分力）；② ProteinMPNN 界面按 Rosetta 打分更差（higher/worse ddG），即"物理评分与实验结果方向相反"；③ 4 个旧确证 dock 没能做出成功变体；④ 界面周边极性侧链构象与预测不符（水分子相互作用，未量化）。
- **我们读出**：① 对照只有 27 个 dock、76 个设计、13 个成功，**"效率提升几个数量级"里的算力总量没有一张时间表/核时表落地**——正文只给"~1 s per sequence"与"several minutes for Rosetta"两个单价，没有端到端墙钟时间、GPU/CPU 核时、总花费；② "orders of magnitude less computation"是单价之比的外推，不是实测的流水线总成本对比；③ 6/13 体外组装的另外 7 例失败原因未逐个交代，是否可算作"自动化后仍留下的湿实验失败"无法判定；④ 全文没有 MD/QM/结合自由能，"弱界面更利于组装"是引用他组工作的解释而非本文测量；⑤ 本文的成功口径是"能组装成目标架构"（结构学判据），**不含亲和力/产量/功能读数**，所以"17%"不可与结合蛋白或酶的命中率并列。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **"同起点双方法对照"的实验设计**：要判断一个新打分器/新序列生成器是不是更好，就用同一批 dock、同一组界面残基、同一预算规则跑两臂（本文 27 dock 双臂）。→ 我们的漏斗若引入新判据（如一维 QM 剖面、xTB 过渡态几何），应在**同一批候选池**上双臂对照，而不是换靶换池。
2. **单价与人工成本一起报**：ProteinMPNN 的贡献被量化成"~1 s/条 vs 数分钟/条 + 零人工"。→ 我们每个新判据都要报"每 1 个通过闸口的候选花多少 CPU·s/GPU·h + 多少人工分钟"（本轮实测单价：MD 156.6 ns/day、新体系 10.6 GPU·h、xTB 271 原子 153.3 s/评价），并把这两项分开。
3. **廉价粗筛 → 逐级解锁贵操作**的顺序原则可搬：先做几乎不花钱的判据（我们这里是序列/结构一致性与注释检索），再做需要表达纯化的产物化学确认（LC-MS/MS），最后才动机制层。但要按第 6.5 条的限制使用：我们的第一道关本身不廉价。
4. **"判据无区分力就明写无区分力"**：本文把 7 条阈值当"最低质量线"而不预测器，并把失败点写进正文。→ 我们的漏斗报告里每条判据要标注"已被验证有区分力 / 仅作质量线 / 未知"，不许把质量线当预测器卖。

**不可迁移（为什么不能照搬）**

1. **SC > 0.5、buried SASA > 1,000 Å²、clash < 3、Met < 5、Gly = 0 这些是"静态几何/组成质量线"，判的是界面会不会形成，不判任何化学反应**。UAA 合成酶的成功要判三步化学事件（游离 UTP 起始 / pppUA / 第二枚 ATP vs 环化竞争）与副产物竞争，**这些阈值既不必要也不充分**。DP2R 判据总纲明令不许把 binder/纳米材料类界面阈值当酶活闸口——本卡尤其危险，因为本文自己就说了这些阈值连"会不会组装"都判不出来。
2. **17% vs 18% 不能当成我们的"目标命中率"或校准点**。分子/分母是"能组装成设计架构"的结构学计数、样本 13/76，且实验终点是 gel 迁移 + SEC 峰 + 负染 EM 形貌，与"产物化学确认的 UAA 生成"不同量纲；把它写进漏斗预期就是编数字。
3. **本文没有任何结构预测置信度闸口**（无 AF2 pAE/pLDDT/ipTM、无 RF2），因此它**不能**用来支持"深度学习置信度可作酶设计闸口"的论点；能提供这条论据的是 B09 一类工作，不是这篇。
4. **通量口径不匹配**：ProteinMPNN 每条 1 秒意味着可以"随便生成几万条再过滤"，而我们的湿实验只能一轮几条构建体，所以我们的漏斗末端必须是**信息量最大化**（机制多样性 + 失活对照 + 单向否证锚），不是候选数最大化。本文的"每 dock 前 3"对我们也只意味着"预算要显式写死"，不意味着"可以按几何分数排序"。


## 9. 溯源与自检

引句底稿: data/interim/baker_lit/ft/autotwo_comp2024.txt

- **本地全文底稿**：`data/interim/baker_lit/ft/autotwo_comp2024.txt`（57,382 B，Europe PMC `fullTextXML` 抽取 → 去标签纯文本，`inventory.json` 记 fetch_channel=epmc_fulltext、fetch_url 指向 PMC10990136；2026-10-16 抓取）。**本卡全部英文引句只照这一份写**（同一论文若换 NCBI 抽取版本，句中参考文献编号排布不同，逐字比对会假红）。
- **该底稿的抽取特征（引句必须照此写法）**：① 句中保留行内引用编号与空格，如 `using Rosetta ( 20 )`、`during design ( 16 )`；② 比较号以 HTML 实体存在（`&lt;`、`&gt;`），核验器 `litcards_text.norm()` 会先 `html.unescape` + NFC + 破折号/引号统一 + 空白折叠，所以本卡把 Methods 的阈值写成 `< 5` / `> 0.5` / `>1,000 Å 2` 能逐字命中；③ 上标 2 与单位之间留空格（`Å 2`），本卡按原样保留。
- **对照记录行号**：`sources/baker.md:392–405`（原卡，它只摘了 shape complementarity 排序与 76 这一层，没有记阈值）。本卡相对它的增量：**Methods 里 7 条阈值的完整原文**（CSV 的 `阈值数字` 字段现写"过滤阈值未给具体数值"，与全文不符）、dock→序列→送测→确证的**逐层规模**、以及作者自陈"无一量度可区分成败"这条失败点。
- **对 CSV 的更正（本卡不改 CSV，只登记）**：CSV `设计对象` 写 T33 为 icosahedral cage，全文口径是 **tetrahedral**（四面体点群的 T33 架构；正文与图注均为 tetrahedral）。
- **未取到的部分**：SI Appendix（Fig. S1–S7、Table S1 晶体学统计、Table S2 76 个设计清单）、PDB 坐标文件、zenodo 设计模型集（10.5281/zenodo.8278877）。凡引用这些处本卡均写"正文未给出"。
- **成功测试（本卡交付的判伪口径）**：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only B30 --no-report` 必须输出 `PASS B30 quotes=N/N` 且退出码 0（10 节齐全、工作流程表 ≥3 步、难点 ≥2 条、每条引句在声明底稿里逐字命中、CSV 回填 14 键无空值）。**本轮实测结果：PASS B30 quotes=76/76，退出码 0**（写卡过程中先用一次性脚本把候选原句逐条对该底稿做过 substring 预检，两轮共 101 条候选全命中后才写入；临时脚本已清理，不在项目里留文件）。**反向自测**（只在内存里改，不写盘）：把摘要句里的 `13 new experimentally confirmed assemblies` 篡改成 `31 ...` ⇒ 同一套逐字比对立刻给出 76 条中 1 条 MISS，即"引用造假会被机器抓到"是可执行的，不是声明。**未核验的部分**：本卡的推算行（43,200 / 21,600 / 568 倍 / 36 倍 / 31.6% / 46%）由原文端点算出，门禁不判其算术；SI Appendix 里的 Table S1/S2 数字本卡没有也无法核验。
- CSV 字段映射：第 3 节 ↔ `候选生成方法/计算筛选判据/阈值数字`；第 4 节 ↔ `候选数递减/实验命中率/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。

- **引用预算截短（2026-11-08，公开仓库口径）**：本卡有 67 条逐字引句来自许可受限的第三方来源（B30；CC_BY_NC_ND），按 `deliverables/fulltext_manifest.csv` 的逐份许可判定，已把单条引句截到 ≤100 字符、同一来源总量截到 ≤600 字符；**截短后仍逐字命中同一份底稿**（门禁 `scripts/verify_literature_cards.py` 仍是逐字核验），完整原句按 §9 的重取方式与 sha256 可复核。逐条改动账见 `deliverables/quote_budget_ledger.csv`。本卡其余内容（我们自己的分析、判断与台账）未被改动。

<!--CSV回填
work_type=论文（PNAS 研究论文，计算设计 + 湿实验验证；预印本 bioRxiv 10.1101/2023.08.04.551935）
target=双组分四面体自组装蛋白纳米材料（T33 架构：四份 A 三聚体 + 四份 B 三聚体）；对 King 2020 的 27 个 Rosetta dock 做同条件重设计（CSV 原记 icosahedral 有误，全文为 tetrahedral）
backbone_generation=不新生成骨架：Rosetta SymDofMover 对既有 dock 的刚体自由度微扰采样（Δ0.5 Å 平移、Δ1° 旋转，每 dock 100 构象）；界面序列由 ProteinMPNN 只改界面残基（sampling temperature 0.2/0.3、backbone noise 0.05、每构象 16 条），再用 Rosetta resfiles 回接 + PackRotamerMover 四面体对称侧重排补侧链；对照臂为 Rosetta 界面设计
computational_filters=ProteinMPNN loss score 取 top 50%；7 条硬阈值联合过滤（甘氨酸数 = 0、甲硫氨酸 < 5、芳香族 < 5、clash < 3、shape complementarity > 0.5、预测界面强度 < 0 REU、界面埋藏 SASA > 1,000 Å²）；按 shape complementarity 每 dock 取前 3；作者自陈上述量度全部不能区分成功与失败设计，无 AF2/RF2 置信度闸口
thresholds=Gly = 0；Met < 5；aromatics < 5；clashes < 3；SC > 0.5；界面强度 < 0 Rosetta Energy Units；埋藏 SASA > 1,000 Å²；loss top 50%；每 dock ≤3；Δ0.5 Å / Δ1°；100 构象/dock；16 序列/构象；T = 0.2 与 0.3；噪声 0.05
md_used=否
qm_used=否
experimental_methods=双顺反子 pET-29b(+) 共表达（单条组分带 His 标签）→ 2 mL 培养裂解液 native PAGE 快筛（~1 MDa 迁移带）→ 1 L 表达 + IMAC → SDS-PAGE 看共洗脱 + native PAGE 看组装 → SEC（Superdex 200，~13 mL / ~1 MDa 单峰）→ 负染 EM + 2D class average 与计算投影比对 → 两组分分别纯化后 1:1、~25 µM 体外组装 + DLS → X 射线晶体学（8T6C、8T6N、8T6E；对照 Rosetta 的 4NWR）
pipeline_counts=43,200 条生成序列（27 dock × 100 构象 × 16 条，本卡按原文端点推算）→ loss top 50% 约 21,600 条 → 阈值过滤 + 每 dock 前 3 → 下单 76 个设计 → native PAGE 疑似 24 → SEC/EM 确证 13 → 可体外组装 6 → 晶体结构 3；对照臂 Rosetta：27 个下单 → 5 个确证
hit_rate=ProteinMPNN 13/76 = 17% vs Rosetta 5/27 = 18%（命中率相当）；dock 层 9/27 个起始复合物出过成功、两法并集 13/27；旧确证 5 例中 ProteinMPNN 只复现 1 例；快筛→确证 24→13；体外组装 6/13
best_metric=未记录（本文终点为结构学确认，无 Kd/活性读数；最硬的定量指标是三个晶体结构对设计模型的骨架 RMSD 0.92 / 1.14 / 0.63 Å，最好分辨率 1.92 Å）
cost_or_stat_note=序列生成 ~1 s/条 vs Rosetta 数分钟/条；作者称算力少几个数量级且零人工修剪，但全文无端到端墙钟、核时或花费表；无置信区间（分母 76 与 27、成功数 13 与 5）；ProteinMPNN 界面的 Rosetta ddG 平均更差（更高）
role_in_timeline=把 ProteinMPNN 从单体/同源寡聚体与 binder 的序列设计器推进为多组分界面的默认生成器，用同 dock 双臂对照证明收益在算力与人工（成本结构）而非判据强度；与 B09 互补——B09 建立 AF2 pAE_interaction 闸口，本文全程不用任何结构预测置信度，且明写现有阈值无区分力
source_pointer=data/interim/baker_lit/ft/autotwo_comp2024.txt（Europe PMC fullTextXML，2026-10-16）；sources/baker.md:392-405；本卡 data/literature_cards/B30_deHaas-2024_PNAS_mpnn-auto-t33.md
CSV回填-->

