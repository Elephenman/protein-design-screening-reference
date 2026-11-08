# [C18] 靶向补体 C9 的 mini-protein 抑制剂（阻断 MAC 组装）（降级卡：逐字底稿为转写层）

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 第 75 行，编号 **C18**（组：曹龙兴组; **口径对照**）。该行 `证据级别` 列写的是「有正文快照」那一档，**本卡不复写该措辞**：本次任务口径是 state=DEGRADED，卡内逐字底稿只有 `sources/cao.md`（其 [C18] 段落自称转写自正文），差异登记在 §9 交协调人裁定 |
| 题目 | "Design of miniprotein inhibitors targeting complement C9 to block membrane attack complex assembly" |
| 作者（底稿行原样） | Li M, Wang N, Fu X, Wei G, Zhang Z, Yu Y, Xue T, Zhao Y, Pan J, Wang D, Liu M, Li Y, Tang J, Cao L（第 14 位）, Jian Z, Liang S, Yu B（末位通讯，山东第二医科大学）；底稿标注为**合作论文（曹为方法学贡献者）** |
| 出处 | "Nature Communications 17(1):3827, 2026-03-12" · DOI 10.1038/s41467-026-70667-x（✅Crossref 核验）· PMID 41813685 · PMCID PMC13121834（OA） |
| 正文取回状态 | 按本次口径：**未取正文快照**。`batches.tsv:90` 的 C18 行 state=**DEGRADED**、fulltexts=`-`、fetch_status 为空；`fetch_log.tsv` 里**没有 C18 的任何抓取记录**；`fulltext/` 目录下**不存在任何 `C18_*` 文件**（即本编号没有挂错行文件，也没有可引用文件）。`inventory.json` 的 C18 项 local=`data/interim/claim_lit/PMC13121834.xml`，本代理读文件头身份块复核：article-title 即本文题目、journal-title=Nature Communications、surname 序列 Li/Wang/Fu/Wei 对得上作者行，**确属本文**；其参考文献表另收了 C15 的 DOI 10.1038/s41557-025-01929-2（卷页 1910-1919），可作交叉印证。但门禁只接受 `*_text.txt` / `sources/*.md` 作逐字底稿（`verify_literature_cards.py:177` 排除 `.xml`），故本卡不以其为引句来源 |
| 登记底稿（本卡唯一引句来源） | `sources/cao.md` 第 284–304 行（[C18] 卡段，含底稿自称「✅全文」的原句与阈值）、第 419 行（曹组漏斗对照表 C18 行）、第 446 行（阶段 4 转化：血清交叉反应/体内半衰期点名 C18）、第 455 行（MD 关键词扫描把 C18 计入「仅命中参考文献条目」清单）、第 268 行（C16 段末：算力成本是他反复抱怨的项，「见 C18 讨论」） |
| 证据级别 | **摘要级 / 二级来源 / 未获正文快照**（本卡口径）。本卡能达到的最强一层是「底稿自称从正文转写的原句」——阈值与规模数字都属这一层，**可信度高于新闻转述，但仍不是我们亲自核正文**；凡引句只在 `sources/cao.md` 逐字命中 |
| 未取到的部分 | 正文的图号/表号归属、每个位点的设计-合成-表达逐级递减明细、表达量与可溶比例、溶血抑制的具体 IC50 数值、AF3 之外是否还有结构验证、SI 里的完整阈值表。凡涉及处写 未记录（本次未取正文快照） |

## 1. 这篇到底解决什么（一句话）

**一句话**：针对补体 **C9**，用 RFdiffusion→ProteinMPNN→AlphaFold2 置信度双阈值这条主流漏斗，设计**阻断膜攻击复合物（MAC）膜插入**的 mini-protein 抑制剂，并用「放宽档/可接受档/投测档/成熟档」四套阈值把约 25,000 个骨架压到 103 个送测，再用 partial diffusion 做亲和力成熟把 Kd 从 nM 段推到 0.7 nM——**同时把这条漏斗的真实上限（in-silico 通过率 0.16%–2.72%）和它的失效现场（置信度与功能不相关）都自报了**。

拆开说四层（按 `sources/cao.md:284–304`）：

1. **对象难度**：C9 的抑制界面大且平，需要的是「80–130 残基较大 binder」而不是六七十残基的小 miniprotein（`:287`）。底稿对位点的记录是站点疏水热点（V196/I199/V305 等）（`:419`）。
2. **判据主体是 AF2 置信度双阈值**：`pae_interaction`（AF2 给 binder–target 界面的预测对齐误差）+ `plddt_binder`（结合体自身置信度），配套定义原句见 §3。
3. **它同时是一行「口径对照」**：CSV 把本行归入「曹龙兴组; 口径对照」，因为它给了本项目最缺的那类东西——**分位点的 in-silico 成功率、投测数、成熟轮命中率**（`:292–300`），以及一句判据失效自白（`:302`）。
4. **应用轴**：人/豚鼠/兔血清溶血抑制 + 急性溶血小鼠模型对比 eculizumab（`:297`），即对标已上市补体药。底稿把这条归入阶段 4 新增判据：**血清交叉反应/体内半衰期**（`:446`）。

## 2. 遇到的难点，以及遇到问题时作者做了什么（引句逐字命中登记底稿 `sources/cao.md`）

> 本卡按降级口径写：**未直接取正文快照**。本节数字来自底稿自称的正文转写句（层级 ⚠️转写级，比新闻稿硬，但页码/图表归属不可核）。

1. **靶界面又大又平，小骨架设计不出可用结合物 → 必须放大 binder 长度并按位点分头做。**
   现象/证据：设计对象被记为「补体 **C9** 的 mini-protein 抑制剂（阻断 MAC 膜插入）；80–130 残基较大 binder」（`:287`）；骨架侧「RFdiffusion（骨架，1500/站点起步，最终跨位点共采样 **14,000 backbones**；总规模自述『约 25,000 binder scaffolds』）」（`:288`），其中一段原句是 "with lengths ranging from 80 to 130 residues"。
   他们做了什么：**把位点当成一等变量**——Site-1 / Site-2 / Site-3 分别设计（站点疏水热点 V196/I199/V305 等，`:419`），每站点先 1500 骨架起步，末端一轮改成 "In a final round, the diffuser.T was set to 120"，跨 Site-1 / Site-3 / Site-1+3 共采样 14,000 骨架（`:288`、`:293`）。
   应对后仍留下的代价：**位点之间差一个数量级以上**——放宽档下 "After applying relaxed filters (pae_interaction < 15, plddt_binder > 88), Site-1 achieved a 1.20 % success rate, while Site-2 approached 0 %"，Site-3 初轮只有 0.16%（`:291–292`）。也就是说「换骨架生成器」救不了选错的位点；底稿未记录他们据此做了什么位点重选规则 → 这条对**我们**是可核实缺口（**本文未解决（在我们能看到的层级）**）。

2. **AF2 置信度双阈值的真实通过率只有 ~1–3%，单一阈值要么筛光要么放脏。**
   现象/证据：判据定义原句 "represents the predicted aligned error that AlphaFold2 assigns to the binder-target interface"，配套 "Designs with pae_interaction < 10 are generally considered acceptable" 与 "a threshold of > 90 is commonly required"（`:290`）；实测 in-silico 成功率 0.16%–2.72%（`:291–293`、`:299`）。
   他们做了什么：**把阈值做成四层分档而不是一个线**：可接受档（<10 / >90）→ 放宽档（<15 / >88，用来给 Site-1 抬通过率）→ 投测闸 "After filtering the combined ensemble (pae_interaction < 8.5, plddt_binder > 90), 103 top-ranking mini-protein binders" + "that target three distinct binding sites were selected for experimental validation"（`:294`）→ 成熟闸用更严的 <6.2 / >90 取出 60 条下单（`:295`）。
   应对后仍留下的代价：**分档只改变通过率，不改变「分数与功能无关」这件事**（见第 3 条）；且约 25,000 骨架换来的是 103 投测——上游算力账单由作者自报（第 4 条）。底稿未记录每档各自的输入规模（只有终末几档的产出数），所以本卡 §3 的规模列部分写 未记录（本次未取正文快照）。

3. **结构置信度排序预测不了功能——作者直接自白了判据失效。**
   现象/证据：原句 "the hemolysis inhibition rates obtained from experimental validation" + "showed no strong correlation with the pae_interaction"，结论是 "indicating the importance of experimental validation."（`:302`，底稿把这整条列在「判据失效的直接自白」名下）。
   他们做了什么：**没有回去调阈值来挽救相关性**，而是保留功能测量（溶血抑制 + BLI）作为不可省的一端，并把改进放在**亲和力成熟**上：partial diffusion（diffuser.partial_T = 1–25，每个 T 值 1000 骨架）+ 更严的成熟闸（<6.2 / >90）出 60 条下单，结果 "identified 30 candidates that outperformed the parental Binder-47"（`:300`）→ **30/60 = 50%（成熟轮命中率）**。
   应对后仍留下的代价：**in-silico 排序与功能之间没有桥**，这条是本文对我们最有价值的负面结论；底稿未记录他们是否提出替代判据（如 AF3 的 pTM/ipTM 只用于单个复合物确认：pTM 0.85 / ipTM 0.93，`:297`）→ 「AF3 指标能不能当筛选闸」本文没有回答。

4. **通量与成本的矛盾：把命中率提上去的手段是加大采样，而算力是明码账单。**
   现象/证据：原句 "we employed relatively large-scale cluster computing and generated approximately" + "in the initial screening phase" + "which led to high computational costs"（约 25,000 binder scaffolds，`:302`）。
   他们做了什么：**用集群把初筛规模拉满**，同时把「省」的位置放在下游——只有 103 个进入表达验证、60 个进入基因合成（`:294–295`）。
   应对后仍留下的代价：底稿未记录绝对机时或金额（CSV 的 成本/统计量 列对本行写 未记录）。这条成本自白在曹组内部的下游影响是可核的：C16（Proteus）段末写「算力是他反复抱怨的成本项，见 C18 讨论」（`:268`）→ 本文的高成本陈述是他**转向自研生成模型**的动因之一。

5. **转化轴的新判据（血清交叉反应 + 体内等效）与亲和力排序打架。**
   现象/证据：实验链含「溶血抑制（人/豚鼠/兔血清）」「急性溶血小鼠模型（对比 eculizumab）」（`:297`）；亲和力侧母本 "Binder-47 interacts more strongly with mouse C9, with" 两个数（底稿记 **3** 与 **22 nM**，即对鼠强于对人，`:301`），成熟后 "BLI results indicated an obvious enhancement of affinity with a" 0.7 nM 对人 C9（P9，摘要口径 "optimized to 700 pM via partial diffusion"，`:301`）。
   他们做了什么：**多种属血清并行 + 体内模型对标上市药**，而不是只在人源分子上把 Kd 压低；底稿把这条归入阶段 4 判据扩张：**血清交叉反应/体内半衰期**（`:446`）。
   应对后仍留下的代价：种属偏好方向是**反的**（母本更贴鼠 C9），而体内模型用的是小鼠 → 底稿未记录 P9 的人/鼠 Kd 比与体内剂量换算，「0.7 nM 对人」是否等于体内更优，未记录（本次未取正文快照）。

6. **取证困难（我们的，不是作者的）：CSV 与读卡表对同一行的证据层级各说一套，而真正属于本文的 XML 门禁不认。**
   现象/证据：`sources_map.json` 的 C18 项登记两份，其中 `data/interim/claim_lit/PMC13121834.xml` 经身份块复核**确为本文**；但 `verify_literature_cards.py:177` 把 `.xml` 排除在可读底稿之外、`:182` 的 `引句底稿:` 正则只接受 `.txt/.md`，而 `batches.tsv:90` 记 state=**DEGRADED**、`fetch_log.tsv` 无 C18 记录。三个表互不一致（CSV 的 `证据级别` 列 = 最高档、batches = DEGRADED、门禁可用底稿 = 只有 cao.md）。
   我们做了什么处置：① 全部 12 条引句只在 `sources/cao.md` 逐字命中（见 §9）；② 底稿正文转写句多带 markdown 强调（`**…**`），门禁会剥卡内星号而源文本仍带星号，跨星号整句必不命中 → 我把这类句子**按连续无星号区段拆条引用**（如 :290/:291/:294/:302 各拆 2–3 条），不改写词、不用省略号拼接；③ 凡底稿未转写的细节（每档输入规模、IC50、机时金额、图号）一律写 未记录，不去 XML 里捞句子；④ 明确登记：**C18 名下未发现挂错行文件**（`fulltext/` 无 `C18_*`），与 C12/C15/C17 的情况不同。
   遗留代价：卡的粒度受限于转写层；若按 FULLTEXT 重跑本行，§3/§4 应以正文为准重写，本卡的「未记录」不等于「原文没写」。

## 3. 方法与工作流程（每步：输入 → 操作 → 判据/阈值 → 输出规模）

**判据定义（底稿转写的正文句，`:290`）**：`pae_interaction` = AF2 赋给 binder–target 界面的预测对齐误差；常用口径是 pae_interaction < 10 视为可接受、plddt_binder > 90 为常用门槛。以下每步的阈值只写底稿出现过的数字，未出现的写 未记录（本次未取正文快照）。

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| S1 | C9 结构 + 位点疏水热点（V196/I199/V305 等） | 位点定义：把大且平的 MAC 插入界面切成 Site-1 / Site-2 / Site-3（含合并位点 Site-1+3） | 底稿未给位点准入阈值（未记录） | 3 个位点（+1 个组合位点） |
| S2 | 各位点定义 | RFdiffusion 生成 80–130 残基骨架，每站点 1500 起步 | 无（本步只生成） | 初轮 1,500/站点；一轮 "with lengths ranging from 80 to 130 residues" 的 **8000 骨架** |
| S3 | S2 骨架 + ProteinMPNN 出序列（每骨架 3 条） | AlphaFold2 打分 → 双阈值判 in-silico 成功 | 可接受档 pae_interaction < 10、plddt_binder > 90；放宽档 "After applying relaxed filters (pae_interaction < 15, plddt_binder > 88), Site-1 achieved a 1.20 % success rate, while Site-2 approached 0 %" | in-silico 成功率：Site-3 初轮 0.16%、8000 骨架那轮 1.18%、Site-1 放宽档 1.20%、Site-2 ≈0% |
| S4 | 终轮采样 | "In a final round, the diffuser.T was set to 120" → 跨 Site-1 / Site-3 / Site-1+3 共采 **14,000 骨架** | 同上双阈值口径 | 成功率 **1.57% / 0.25% / 2.72%**（按位点） |
| S5 | S3+S4 的合并样本 | 投测闸：AF2 双阈值收紧后取 top-ranking | "After filtering the combined ensemble (pae_interaction < 8.5, plddt_binder > 90), 103 top-ranking mini-protein binders"，且 "that target three distinct binding sites were selected for experimental validation" | **103 个**进入实验验证 |
| S6 | 103 个的湿实验结果 | E. coli 表达 + SEC + CD 热复性 + BLI + 溶血抑制（人/豚鼠/兔血清） | 底稿未记录该层判据与通过率（未记录） | 未记录（103 里表达/纯化成功多少，底稿未给） |
| S7 | 表现最好的母本 Binder-47 | 亲和力成熟：partial diffusion，diffuser.partial_T = 1–25（每个 T 值 1000 骨架） | 成熟闸 pae_interaction < 6.2、plddt_binder > 90（`Applying stricter cut-offs` 之后取 60，`:295`） | **60 条**序列进入基因合成 |
| S8 | 60 个成熟构建体 | 湿实验比较成熟体 vs 母本 Binder-47 | 判据：优于母本 | "identified 30 candidates that outperformed the parental Binder-47" → **30/60 = 50%** |
| S9 | 命中成熟体 + 小鼠 | 结构与体内确认：X 射线晶体学、AF3 复预测（pTM 0.85 / ipTM 0.93）、急性溶血小鼠模型对比 eculizumab | 底稿未给这些指标的准入线（未记录） | 单案例级确认，无群体分母 |

**这条流程的骨架（可记住的部分）**：漏斗不是「一个阈值 + 一次生成」，而是**位点轴 × 阈值档位轴 × 成熟轮**三层：位点决定可达上限（Site-2 接近 0），档位决定投测规模（103），成熟轮决定质量（0.7 nM）。而作者自己报告了这三层的接缝处是断的：**结构置信度与溶血抑制率无强相关**（`:302`）——所以这条漏斗的终点不是「分数最高」，是「必须做功能测量」。

## 4. 关键数字台账（全部能在登记底稿 `sources/cao.md` 里搜到；层级标注见出处列）

| 数值 | 含义 | 出处 |
|---|---|---|
| 80–130 残基 | 设计 binder 的长度（较大 binder，非六七十残基小蛋白） | `sources/cao.md:287`、`:292` |
| 1500 / 站点 | RFdiffusion 每一起始位点的骨架采样数（起步规模） | `sources/cao.md:288` |
| **8000 骨架** | 某一轮采样的骨架数（80–130 残基区间） | `sources/cao.md:292` |
| **14,000 backbones** | 终轮跨 Site-1 / Site-3 / Site-1+3 的总采样 | `sources/cao.md:288`、`:293` |
| 约 **25,000 binder scaffolds** | 初筛阶段总规模（作者自述，且自陈带来高计算成本） | `sources/cao.md:288`、`:302` |
| ProteinMPNN 每骨架 **3** 条序列 | 序列生成倍率 | `sources/cao.md:288` |
| pae_interaction **< 10** / plddt_binder **> 90** | 「可接受 / 常用」双阈值 | `sources/cao.md:290` |
| pae_interaction **< 15** / plddt_binder **> 88** | 放宽档（用于抬 Site-1 通过率） | `sources/cao.md:291` |
| pae_interaction **< 8.5** / plddt_binder **> 90** | 投测闸 → 103 个 | `sources/cao.md:294` |
| pae_interaction **< 6.2** / plddt_binder **> 90** | 成熟闸 → 60 条下单 | `sources/cao.md:295` |
| **0.16%** | Site-3 初轮 in-silico 成功率 | `sources/cao.md:292` |
| **1.18%** | 8000 骨架那一轮的 in-silico 成功率 | `sources/cao.md:292` |
| **1.20% / ≈0%** | 放宽档下 Site-1 / Site-2 的 in-silico 成功率 | `sources/cao.md:291` |
| **1.57% / 0.25% / 2.72%** | 终轮 Site-1 / Site-3 / Site-1+3 的 in-silico 成功率 | `sources/cao.md:293` |
| **0.16%–2.72%** | 全部分位点 in-silico 通过率的区间（本行的「真实上限」） | `sources/cao.md:299`、`:419` |
| **103** | 通过投测闸、进入实验验证的 binder 数（覆盖三个位点） | `sources/cao.md:294`、`:300` |
| **60** | 成熟闸后进入基因合成的序列数 | `sources/cao.md:295`、`:300` |
| **30 / 60 = 50%** | 成熟轮命中率（优于母本 Binder-47） | `sources/cao.md:300` |
| diffuser.partial_T = **1–25**（每 T 值 1000 骨架）；终轮 diffuser.T = **120** | partial diffusion 亲和力成熟的采样设定 | `sources/cao.md:288`、`:293` |
| K_D **3** 与 **22 nM** | 母本 Binder-47 对**鼠**与**人** C9 的亲和力（鼠更强） | `sources/cao.md:301` |
| K_D **0.7 nM**（摘要口径 700 pM） | 成熟体 P9 对**人** C9 的亲和力（BLI） | `sources/cao.md:301` |
| pTM **0.85** / ipTM **0.93** | AF3 对复合物的预测质量（事后确认用） | `sources/cao.md:297` |
| 人 / 豚鼠 / 兔血清；急性溶血小鼠模型（对比 eculizumab） | 功能与体内评价链 | `sources/cao.md:297` |
| 「溶血抑制率与 pae_interaction 无强相关」 | 判据失效的作者自白 | `sources/cao.md:302` |
| 否（MD）/ 否（QM） | 底稿记「均未使用（全文无 MD/QM 关键词）」，并有 MD 关键词扫描旁证 | `sources/cao.md:296`、`:455`；CSV 两列同为 否 |
| Nature Communications 17(1):3827, 2026-03-12 / DOI 10.1038/s41467-026-70667-x / PMID 41813685 / PMCID PMC13121834 | 题录与标识符（✅Crossref；标注为 OA） | `sources/cao.md:286` |
| Cao L 第 14 位；Yu B 末位通讯（山东第二医科大学） | 作者位次：曹是方法学贡献者，非通讯 | `sources/cao.md:285` |
| **未记录（本次未取正文快照）**：每档阈值的输入规模、103 中的表达/可溶比例、各抑制读数（IC50）、机时/金额成本、图号与表号归属 | 底稿未转写 → 本卡不给出，也不从同组他篇挪 | `sources/cao.md:289–302`（无该类记录）；CSV 成本列本行 = 未记录 |
| （旁注，非本文数字）`data/interim/claim_lit/PMC13121834.xml` | 属于本文的 XML 快照（身份块复核通过；其参考文献含 C15 的 DOI），但门禁不认作逐字底稿，本卡未据其引用 | `sources_map.json` C18 项；`verify_literature_cards.py:177` |

## 5. 结论——作者说了什么（底稿自称转写自正文的句子；本卡无正文页码可指）

1. **判据是他们公开写出来的，不是隐含的**：`pae_interaction` 的定义原句 "represents the predicted aligned error that AlphaFold2 assigns to the binder-target interface"，加上 "Designs with pae_interaction < 10 are generally considered acceptable" 与 "a threshold of > 90 is commonly required"（`:290`）。这是曹组条目里**唯一把置信度双阈值连同分档一起公开**的一篇（C11/C14 也有阈值但不是他主导的漏斗末端）。
2. **他们声称 in-silico 通过率就是 1–3% 量级，并分位点报告**：放宽档下 "After applying relaxed filters (pae_interaction < 15, plddt_binder > 88), Site-1 achieved a 1.20 % success rate, while Site-2 approached 0 %"（`:291`）；初轮 Site-3 为 0.16%（`:292`）；终轮三个位点组合分别 1.57% / 0.25% / 2.72%（`:293`）。
3. **他们声称送测是被闸出来的，不是挑出来的**："After filtering the combined ensemble (pae_interaction < 8.5, plddt_binder > 90), 103 top-ranking mini-protein binders"，"that target three distinct binding sites were selected for experimental validation"（`:294`）。
4. **他们声称成熟轮有效**：60 条下单后 "identified 30 candidates that outperformed the parental Binder-47"（`:300`）→ 50%；亲和力端 "BLI results indicated an obvious enhancement of affinity with a" 0.7 nM（对人 C9，P9），母本则是 "Binder-47 interacts more strongly with mouse C9, with" 3 与 22 nM（`:301`），摘要口径为 "optimized to 700 pM via partial diffusion"（`:301`）。
5. **他们自报了判据失效**：这是本文最重要的作者声明——"the hemolysis inhibition rates obtained from experimental validation" 与 "showed no strong correlation with the pae_interaction"，他们的结论是 "indicating the importance of experimental validation."（`:302`）。
6. **他们自报了成本**："we employed relatively large-scale cluster computing and generated approximately" 约 25,000 binder scaffolds，"in the initial screening phase"，"which led to high computational costs"（`:302`）。
7. **作者没有说的部分（本卡空白）**：MD/QM 均未使用（`:296`，另有底稿级关键词扫描旁证 `:455`）；每档阈值的输入规模、表达/可溶比例、溶血抑制的 IC50、机时与金额，底稿均未转写 → 未记录（本次未取正文快照）。

## 6. 我们读出了什么（以下为推断，非作者原文）

1. **这一行是整套表里最好的「筛子考卷」参照物**：作者把 in-silico 通过率（0.16%–2.72%）与湿实验结局（103 投测、30/60 成熟命中）**同时**报了，还报了两者**不相关**。→ 对我们：任何「用打分排序预筛」的方案都必须回答同一个问题——分数与终点的秩相关是多少；本项目在 C23 一侧见过同类自白（传统指标与活性无显著相关），本文给了 binder/抑制方向的第二个独立案例。把握度：高（数字与自白都在底稿转写句里）。
2. **「位点」是一等变量，其影响大于「模型」**：Site-2 接近 0% 而 Site-1+3 达 2.72%——同一套 RFdiffusion + 同一套阈值，跨位点差一个数量级。→ 对我们：酶设计筛选里「口袋/位点可不可达」应作为召回阶段的**独立轴**登记（对应本项目 B_SITE），并且**分位点报通过率**，不许把多位点合并成一个平均数——平均会同时掩盖 Site-2 的 0 和 Site-1+3 的 2.72%。
3. **阈值分档是「规模控制」而不是「质量保证」**：四档（可接受/放宽/投测/成熟）改变的是通过数与算力账单，从未声称改变「功能对错」；作者在 S6/S8 仍然要靠湿实验定胜负。→ 对我们：我们的闸口也应区分「控规模的档」与「定资格的档」，后者必须绑一个功能读数（产物身份），否则只是花算力挑一堆没测过的东西。
4. **成熟轮（partial diffusion）与初筛轮不是同一件事**：初筛是「从零生成 binder」，成熟是「在已验证母本附近做局部重设计」，因此 50%（30/60）与 1–3%（初筛）**不可放在同一张成功率表里比较**。→ 对我们：任何「优化轮 vs 生成轮」的命中率对比必须显式标注母本是否已被实验验证过——这是本项目最容易犯的比值错（C19 的 12/16 vs C02 的 10⁵ 是同一形状）。
5. **本文给出的最硬的「不要做」是：不要用结构置信度当终点**。作者自己证明了秩相关不存在（`:302`），因此若我们的方案里出现「ipTM 高就直接升层」，本文是现成的反驳材料（引用时要带上它是「设计 binder 抑制 MAC」而非酶的背景）。
6. **曹是方法学贡献者（第 14 位、非通讯）**：所以本行在 CSV 里被标为「曹龙兴组; 口径对照」是准确的——它的价值在**口径**（阈值 + 递减 + 失效自白），不在「他的方法」。→ 对我们：写方法演进链时不要把 C18 写成「曹的漏斗改革」，它是他用别人主线漏斗做的一例**外部对照**。

## 7. 局限与失败（作者的 + 我们读出的）

**作者自报（底稿转写，层级：正文转写级）**

- 判据失效：溶血抑制率与 pae_interaction 无强相关（`:302`）→ 置信度不能替代功能测量。
- 成本高：约 25,000 骨架初筛，作者明写带来高计算成本（`:302`）；绝对机时/金额未记录。
- 位点不均：Site-2 在放宽档下仍接近 0%（`:291`），作者未给出位点选择的定量准则 → 这条**本文未解决**（我们看到的是没有准则，不是他们承认没解决）。

**我们读出的局限（推断）**

1. **递减链有两处断口**：103 投测之后「表达/可溶/结合各剩多少」底稿未记录，60 下单的 30 命中也没有对应的「池子有多大」→ 本文的漏斗不是完整链，只有「初筛率 + 两个末端产出数」；任何由 25,000→103 反推「总命中率 0.4%」的算法都忽略了中间未记录的轮次。
2. **种属方向是个未闭合的风险**：母本 Binder-47 对**鼠** C9 更强（3 nM）而对人 22 nM（`:301`），成熟体 P9 报的是**人** 0.7 nM；但体内模型（急性溶血小鼠 + 对比 eculizumab）在小鼠里做。底稿未记录 P9 的鼠 Kd → 「小鼠体内有效」与「人源亲和力最优」之间没有换算证据。这是我认为**本行最可疑的判据缺口**。
3. **AF3 的 pTM 0.85 / ipTM 0.93 是事后确认，不是筛选闸**（`:297`）：底稿未记录它们被用于淘汰任何候选。引用时不许写成「他们用 ipTM 闸住了候选」。
4. **「pae_interaction < 10 一般可接受」是行业口径而非本文自设**：原句用 "generally considered acceptable"、"commonly required"（`:290`）——这两个词表明阈值是共识量，本文真正的贡献是把**分档 + 分位点**的通过率公开出来。搬用时不要把共识阈值当成本文的原创判据。

## 8. 迁移判断：哪些能搬、哪些不能搬（本文是我们最该抄「口径」的一篇，但阈值本身不可照搬）

先回答核心问题：**能搬的是「分位点报通过率 + 阈值分档并说明每档目的 + 公开分数与功能的秩相关检验 + 生成轮与成熟轮分开记账」这四条登记与做法；不能搬的是 pae_interaction / plddt_binder 的任何数值线、以及把界面置信度当成活性判据这件事本身**。本库迁移边界（§8） 明禁把 binder 的 pAE/ipTM 阈值当成酶活判据——本文作者本人的自白（`:302`）正是这条禁令的实验依据。

**可迁移（具体怎么用）**

1. **秩相关检验必须进我们的判据表**。他们把「设计分数 vs 功能读数」的相关性当作结果之一报告（结论是无关）。搬法：我们每轮至少对一个批次做**显式秩相关**（打分序 vs S1/S2 产物比或通量比），无论结果是什么都写进登记；结果为「无相关」时，处置照他们的做法——保留功能测量为不可省的一端，而不是回去调阈值。
2. **分位点/分事件报通过率，禁止合并成平均**。他们报的是 Site-1 1.20%、Site-2 ≈0%、Site-3 0.16%、Site-1+3 2.72%。搬法：我们按 **第一步压制 / 第二步生成 / 第三步环化 vs 二掺** 分别报通过数与分母，并保留「0」这种读数（0 是最有信息量的数）。
3. **阈值分档 + 每档写明目的**。可接受档（判可行性）/ 放宽档（救某一位点）/ 投测闸（控湿实验规模）/ 成熟闸（控下单成本）。搬法：我们的闸口表也应是四档并各带目的栏，且**每档必须同时登记输入规模与输出规模**（他们没登记输入规模，这是我们不该照抄的地方）。
4. **生成轮 vs 成熟轮分开记账**。他们的 1–3%（无母本）与 50%（有已验证母本 Binder-47）从不混报。搬法：我们凡是「在已验证构建体附近优化」的一轮，命中率必须单列，不与首轮生成率比较——直接对标本项目在 C19（16 个/靶）与 C02（10⁵ 设计）之间踩过的分母坑。
5. **成本自白要留账**。他们把算力规模（25,000 骨架）与「高成本」写进正文。搬法：我们的 run.md 里每轮要登记生成规模与算力口径，作为下一轮「是否改用更省的路线」的依据（本文的高成本陈述正是同组转向自研生成模型 C16 的动因，见 `:268`——这条因果链对我们同样成立）。
6. **「位点可达性」前置为独立召回轴**。跨位点差一个数量级，说明再贵的生成也救不了不可达界面。搬法：我们的 B_SITE（能否同时容纳底物与催化几何）应在召回阶段就作为闸门，而不是排序阶段的一个加分项。

**不可迁移（为什么不能照搬）**

1. **pae_interaction < 10 / 8.5 / 6.2、plddt_binder > 90 / 88 一律不得进我们的闸口**。它们量的是「AF2 对界面/链的自洽度信心」，而我们要的是「有没有按设计成键」；作者本人已证它与功能不相关（`:302`），照搬等于搬一个被原作者否掉的判据。
2. **in-silico 通过率 0.16%–2.72% 不能当我们的期望值或校准锚**。那是「binder 对补体 C9 平坦界面」这个具体问题的分布；我们既无展示库级通量、也无同一分母。禁止写「酶设计的 in-silico 通过率预期 1–3%」。
3. **30/60 = 50% 不能当我们的成熟轮预期**。其分母是**已验证母本附近**的 60 条下单序列，判据是「优于母本」；我们的成熟/改造轮分母与判据（产物比、内标定量）都不同，量纲不可比。
4. **0.7 nM 不是我们的通过线**：那是 BLI 亲和力（结合强度），我们的合格线是化学计量与通量比（例如 S2 环化/二掺比）；把 nM 类读数写进酶活规格是本项目明禁的跨域挪用。
5. **溶血抑制 / eculizumab 对标是补体通路特异读出**，没有任何酶设计对应物；可类比者只有「与一个金标准治疗/参考酶并排测」这个**做法**，不是它的读数。
6. **本文不含 MD/QM**（`:296`），所以它既不支持也不反对我们在机制层上自由能计算；引用时不得写「连 C18 都不用 MD」。

## 9. 溯源与自检

引句底稿: sources/cao.md

- **本卡按降级口径写**（state=DEGRADED，见 `batches.tsv:90`）：逐字底稿只有 `sources/cao.md`。本卡引句共 **21 条不同片段 / 门禁计 43 处命中**（题目、期刊卷期行，以及底稿自称转写自正文的方法/阈值/结果/自白句），全部只在 `sources/cao.md` 内逐字命中；本行 inventory 的 `has_fulltext=true` 使门禁按「有全文卡 ≥8 条」的严格侧要求本卡，已满足。
- **引句被拆条的原因（交接用）**：底稿在正文转写句里大量使用 markdown 强调（`**…**`）。门禁的 `clean()` 会剥掉卡内引句的星号，而源文本仍带星号，跨星号区段的整句不可能命中（本项目 AGENT_RULES 已把这条列为坑）。处置：按**连续无星号区段**拆条（如 `:290` 拆 3 条、`:294` 拆 2 条、`:302` 拆 4 条、`:301` 拆 3 条），被剥掉的数值在正文里用非引号文字补出。**没有省略号拼接、没有改写任何词、没有加删空格。**
- **证据层级差异（交协调人裁定）**：CSV 第 75 行的 `证据级别` 列写的是最高档，`inventory.json` 的 C18 项 local=`data/interim/claim_lit/PMC13121834.xml`（本代理读文件头身份块复核，**确属本文**：article-title 与本文一致、journal-title=Nature Communications、surname 序列 Li/Wang/Fu/Wei 与作者行相符；其参考文献表内含 C15 的 DOI 10.1038/s41557-025-01929-2，可交叉印证），但 `batches.tsv:90` 记 state=**DEGRADED**、`fetch_log.tsv` 无 C18 记录、`verify_literature_cards.py:177` 与 `:182` 只接受 `*_text.txt` / `sources/*.md` 作逐字底稿。三套表互不一致，本卡按任务口径（DEGRADED）写，并在此登记：要把本行升到正文级，缺的不是文件而是一份进入 `data/literature_cards/fulltext/` 的 `C18_*_text.txt` 抽取件 + 一次重跑。**本代理未改 CSV、`sources/*.md`、`inventory.json`、`sources_map.json`、`batches.tsv`、样板卡与 `scripts/`。**
- **挂错行文件的排查结论（C18：未发现）**：`data/literature_cards/fulltext/` 下不存在任何以 C18 命名的文件（本代理实跑目录列举确认）；`sources_map.json` 的 C18 项只有上面那份 claim_lit XML 与 `sources/cao.md`。身份体检（只读，不带 `--apply`）：`PYTHONIOENCODING=utf-8 python scripts/litcards_identity_audit.py` → **OK 78 · MISMATCH 0 · 无候选全文跳过 74 行**（C18 属被跳过行）。判断依据写在这里供复核：体检绿 ≠ 身份已核，被跳过行没有可体检文件；本卡的「claim_lit XML 属本文」结论来自直接读文件头身份块，不来自体检。
- **同批四行里确有误挂的是 C12 与 C15**：`fulltext/C12_PMC13676076_fullTextXML.xml`（Neoplasia 综述，DOI 10.1016/j.neo.2026.101375）与 `fulltext/C15_PMC13676841_fullTextXML.xml`（Small 论文，DOI 10.1002/smll.75187）——两者均只在参考文献里引用各自对应的本文，已分别在本卡 §0/§2/§9 记录处置；本代理未移动、未删除、未引用它们。
- **CSV 字段映射**：本卡 §3 ↔ 候选生成方法 / 计算筛选判据 / 阈值数字；§4 ↔ 候选数递减 / 实验命中率 / Kd或活性最好值 / 成本统计；§8 ↔ 在方法演进链的位置。
- **门禁自检**：命令 `cd A:\Data\MD\projects\protein-design-screening-20261016 && PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "C18" --no-report`（仅本编号、不落盘报告，避免覆盖他人产物）。结果见交回回报。

<!--CSV回填
work_type=论文（本卡按降级口径写：逐字底稿只有 sources/cao.md；CSV 该行的 证据级别 列记为更高档，差异见 §9）
target=补体 C9 的 mini-protein 抑制剂（阻断膜攻击复合物 MAC 的膜插入）；位点 Site-1 / Site-2 / Site-3 及 Site-1+3；80–130 残基较大 binder；对标 eculizumab
backbone_generation=RFdiffusion 骨架生成（1500/站点起步；一轮 8000 骨架；终轮 diffuser.T=120，跨位点共采 14,000 backbones；总规模自述约 25,000 binder scaffolds）→ ProteinMPNN（每骨架 3 条序列）→ AlphaFold2 打分 → partial diffusion 亲和力成熟（diffuser.partial_T=1–25，每 T 值 1000 骨架）
computational_filters=AF2 置信度双阈值 pae_interaction（binder–target 界面的预测对齐误差）+ plddt_binder，分四档使用：可接受 <10/>90、放宽 <15/>88、投测 <8.5/>90、成熟 <6.2/>90；位点疏水热点（V196/I199/V305 等）定义靶面；AF3 复预测 pTM 0.85/ipTM 0.93 仅作事后确认
thresholds=pae_interaction <10（一般可接受）/ <15（放宽）/ <8.5（投测）/ <6.2（成熟）；plddt_binder >90（常用）/ >88（放宽）；in-silico 成功率 Site-1 1.20%（放宽档）、Site-2 ≈0%、Site-3 0.16%、8000 骨架轮 1.18%、终轮 1.57%/0.25%/2.72%
md_used=否（底稿 :296 记均未使用，另有 :455 的 MD 关键词扫描旁证；属底稿级结论）
qm_used=否（同上；本文设计对象不含共价/电子步骤）
experimental_methods=E. coli 表达；SEC；CD 热复性；BLI；溶血抑制（人/豚鼠/兔血清）；X 射线晶体学；AF3 复预测（pTM 0.85/ipTM 0.93）；急性溶血小鼠模型（对比 eculizumab）
pipeline_counts=约 25,000 骨架初筛（in-silico 通过率 0.16%–2.72%，分位点报告）→ 投测闸 103 个（pae<8.5 且 plddt>90）→ 部分扩散 + 成熟闸 60 条下单（pae<6.2 且 plddt>90）→ 30 个优于母本；中间各档输入规模与表达/可溶比例 未记录（本次未取正文快照）
hit_rate=成熟轮 30/60 = 50%（判据为「优于已验证母本 Binder-47」，分母不是设计库，禁止当生成轮命中率或酶设计成功概率引用）；初筛 in-silico 通过率 0.16%–2.72%（分位点）
best_metric=P9 对人 C9 K_D 0.7 nM（BLI；摘要口径 700 pM via partial diffusion）；母本 Binder-47 对鼠/人 C9 为 3 与 22 nM（鼠更强）
cost_or_stat_note=作者自白：相对大规模集群计算、初筛生成约 25,000 binder scaffolds，导致高计算成本（绝对机时/金额 未记录）；另自白实验溶血抑制率与 pae_interaction 无强相关，即结构置信度排序不预测功能（本文最重要的口径信息）
role_in_timeline=RFdiffusion 时代「AF2 置信度双阈值」漏斗的真实上限展示（in-silico 1–3% 且与功能不相关）；同时是曹组阶段 4 转化判据扩张（血清交叉反应/体内等效，对标 eculizumab）的口径对照行；其算力成本自白是同组转向自研生成模型（C16 Proteus）的动因之一
source_pointer=sources/cao.md:284-304（[C18] 卡段，:290-:295 为阈值与规模原句、:300-:302 为命中率与两条自白）、:419（漏斗对照表行）、:446（阶段4新增判据点名本文）、:455（MD 关键词扫描旁证）、:268（算力成本动因）；DOI 10.1038/s41467-026-70667-x ✅Crossref、PMID 41813685、PMCID PMC13121834；旁注 data/interim/claim_lit/PMC13121834.xml 身份复核为本文但门禁不认作逐字底稿（未据其引用）；C18 名下未发现挂错行文件
CSV回填-->
