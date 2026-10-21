# [K29] GROMACS 上云：把"MD/自由能计算该花多少钱、多久能跑完"变成可查表的工程问题

Kutzner C, Kniep C, Cherian A, Nordstrom L, Grubmüller H, de Groot BL, Gapsys V（Max Planck 多学科科学研究所 + AWS）
J Chem Inf Model 2022, 62:1691–1711 · DOI 10.1021/acs.jcim.2c00044 · PMID 35353508 · PMCID PMC9006219
开放获取（CC BY 4.0）

---

## 0. 元信息与核验状态

| 项 | 值 |
|---|---|
| CSV 行 | `data/protein_design_literature.csv` 编号 **K29**（组：通用方法学; 口径对照） |
| 本文取回方式 | Europe PMC（epmc_search_then_fulltext，按 DOI 10.1021/acs.jcim.2c00044 检索），本地抓取 |
| 本地全文 | `data/literature_cards/fulltext/K29_PMC9006219_text.txt` |
| 对照底稿 | `sources/cost-benchmarks.md` 第 66、68 行（经典 MD 云端单价、云vs自建口径行，即本文） |
| 证据级别 | **全文级**（本卡所有引句均可在本地纯文本里逐字命中；见第 9 节自检） |
| 未取到的部分 | Tables 5–11 的完整 ns/d、ns/$ 数值矩阵在正文抽取中只剩表题与正文转述；Fig 1/5/6/8/9/10/11 原图未取。凡涉及处本卡明写"正文未给出逐格数值" |

## 1. 这篇到底解决什么（大白话）

一句话：做药算结合自由能（FEP/ABFE 这类）最缺的不是算法而是"算得完 + 算得起"，这篇用 GROMACS + AWS 把这两件事全部量化。它回答三个问题：(a) 云上几十种实例，哪些跑 MD 最快、哪些性价比最高（用 ns/day 和 ns/美元 两张色阶表逐个实测）；(b) 算一条轨迹，云端总成本（硬件+人力+机房+电+制冷）和自建集群比到底谁贵（结论：选对实例则大致打平，自建 GROMACS 优化集群约 0.85× Spot 云成本）；(c) 一个本来要在自建集群上跑几周的高通量配体筛选（19 872 个独立任务、约 200 μs 合计轨迹），用全球多区域云 + 廉价可抢占实例多久能跑完、每个自由能差值要花多少钱（结论：约 2 天跑完；第二轮挑实例后约 $16/个差值，比朴素做法便宜约 9 倍）。

## 2. 遇到的难点，以及遇到问题时他们做了什么（作者自述，不是我们的推测）

1. **廉价的前提——Spot 可抢占实例——随时会被回收**。便宜最多 90% 的 Spot 池"可以被 Amazon EC2 随时收回"，只给 2 分钟预警（原文："However, a Spot instance can be claimed back at any time by Amazon EC2 with a 2 min warning."）。整个大规模跑法如果直接架在 Spot 上，一次回收就废掉一段轨迹。
   **应对**：做了一套 checkpoint-restart 工程——平衡轨迹切成 8 段（"Part i is executed in eight chunks (lines 28 and 29) so that upon instance termination only a small part needs to be recomputed"）、每个变换完成立即存 S3（"If an instance terminates during one of the 80 transformations, the job is continued from the start of that transformation"）、实例被收回时 Lambda 自动把任务重新投回 HyperBatch、并按各区域 Spot 池大小比例申请实例、混用各种 vCPU 规格在一台大实例上塞多个任务（"A single 96 vCPU c5.24xl instance could then, for example, end up running one 48 vCPU job plus six 8 vCPU jobs at the same time."）。
   **残留代价**：实测 3070 次重启（约占任务数 15%）；最坏情况丢 1 ns/任务，总算力损失上界约 1.5%。作者承认彻底避免损耗还需改进协议（用 2 分钟预警信号触发写 checkpoint），本文没做。

2. **云上强扩展撞墙：多 GPU/多实例不是免费的快**。PME 远程静电力不能分发到多 GPU，单实例塞多个 GPU 反而负载均衡变差（"the P/P ratio plunges when distributing a simulation across multiple GPUs on an instance"）；小系统（MEM）跨实例扩展效率掉到 <40%（"For the 81 k atom MEM system, the maximal performance is reached on 4 hpc6a instances, however at a parallel efficiency of less than 40%"）；hpc6a 云集群扩到 32 实例仍到不了自建专用 HPC 的量级（同一基准在自建集群峰值 303 ns/d MEM、204 ns/d RIB）。
   **应对**：三条——(a) N 卡实例改为同时跑 N 个独立单 GPU 任务（GROMACS 的 multidir），p4d.24xl/8 这样跑轨迹产出与性价比约提高 4 倍；(b) 分配 1/4 到 1/3 的 rank 专算 PME（separate PME ranks）削通信瓶颈；(c) 跨实例扩展时 PME 留在 CPU 侧跑（只有那里能并行）。
   **残留代价**：他们明说云内互连仍不如自建 HPC（"The hpc6a instances, however, never reach the scaling performance of an on-premises dedicated HPC cluster."）；本文对"能不能逼近自建 HPC 的强扩展"没有解决，答案是放弃 HPC 路线、改打 HTC（19 872 个互相独立的任务并行）。

3. **单区域资源池不够、实例种类会突然抢不到**。为压时间只选三种 g4dn GPU 实例是 risky 的（"g4dn instances are not very abundant in the AWS cloud, and if they happen to be in high demand at the time of our screening study, we might not get many of them"）。
   **应对**：全球多区域方案——用 AWS HyperBatch 做跨区统一入口，按区域权重分发任务（"HyperBatch distributes jobs across regions according to region weights reflecting the compute capacity of the regions"），并加入永远有货的 c5/c5d 大 CPU 实例兜底；第二轮研究进一步印证："a multiregion approach is necessary for decent job throughput when limiting oneself to only a few instance types"。
   **残留代价**：第二轮里 GPU 任务仍因 g4dn Spot 容量不足总共跑了约 30 h、爱尔兰与北弗吉尼亚两区隔了几小时才放出货；"把 19 872 个任务 24 h 内一次跑完"的设想没能兑现（他们只是推测可以）。

4. **第一轮自己的调度脚本有 bug，实例跑完不关机，白烧钱**（"Unfortunately, there was a glitch in the initial version of our setup that prevented finished instances to terminate properly."）。
   **应对**：如实报两个口径——$56/FE 差值（实际账单）与 $40/FE（只算有效时间）；第二轮修好设置并只保留高性价比实例类型，降到约 $16/FE。
   **残留代价**：无（这一条被第二轮消化了，但提醒：成本数字对工程实现细节极其敏感）。

5. **FE（alchemical）任务比普通 MD 慢且无现成基准可借**：开了自由能微扰要多算一张 PME 网格、被扰动原子走的是未优化 kernel，"even at equal atom count a FE simulation will be slower than a plain MD system"；且 2020 版带扰动电荷时 PME 不能下放 GPU。
   **应对**：不能用 MEM/RIB 外推，专门从筛选全集里挑 4 个代表体系（小/中/大蛋白-配体 + 一个水中配体）重做基准；换 GROMACS 2021（PME 可上 GPU，作者测得提速超过 2 倍）；结果连同价格整理成公开的网页基准库（http://pmx.mpibpc.mpg.de/aws.pl）。
   **残留代价**：基准是 2021 年 5 月美东价格快照，作者注明 Spot 价格随区域与时间变动；所有性价比结论都带"当时当地"的保质期。

6. **总成本对比"没有普适答案"**：作者直承自建 vs 云取决于集群规模、软件多样性、占用率（"Therefore, no generalizable results or guidance can be provided here."）。
   **应对**：放弃给通用结论，改为给一个可复算的特例口径——以 RIB 基准 1 μs 轨迹为单位，把自建的硬件（<2000 €/节点）、机架 500 €/U、维护人力 100 000 €/年、机房 30 000 €/年、集群软件 40 €/节点/年逐项列出，与 g5.2xl 按需/预留/Spot 三种计费对比。
   **残留代价**：该口径仅在"整个集群只跑 GROMACS 且用消费级 GPU"时成立，文中明确说明软件一多就 tune 不到这么极致、优势消失。

## 3. 方法与工作流程（可复现顺序；每步：输入 → 操作 → 判据 → 输出规模）

### 用了哪些方法（工具箱，以及为什么选它）

- **模拟引擎**：GROMACS 2020.2 / 2021.1（mixed precision，GCC/Intel MPI 或 thread-MPI，GPU 版 CUDA 10.2/11.1），Spack 0.15.4 装包、ParallelCluster 2.10.0/2.9.1 建集群、SLURM 排队。
- **自由能方法**：pmx + GROMACS 的开源工作流，非平衡热力学积分（TI，λ 插值，Crooks 涨落定理估计器）算**相对**结合自由能；配体连成网络（图），对每条边做 A→B 与 B→A 变换。文中对照：Schrödinger 的 FEP 方法与本工作流的 TI "两者在相近计算量下给出相近精度的相对结合自由能"。
- **云编排**：AWS EC2 各代实例（Intel/AMD/ARM、GPU g4dn/g5/p3/p4d）、HyperBatch 跨区调度（DynamoDB + Lambda + Step Functions + Kinesis + SQS + API Gateway）、S3 存取输入输出与 checkpoint、ECR 存各架构 Docker 镜像、Kibana 全局监控。
- **没有用的方法**：QM（全程无量子化学）；没有湿实验；不做打分函数/精度改进，只做性能-价格实测。

### A. 实例选型基准（决定后面所有成本账的地基）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| A1 | 7 个基准体系（Table 2：PEP 12 495 503 原子、RIB 2 136 412、MEM 81 743；FE 体系 SHP-2 107 330、c-Met 67 291、HIF-2α 35 546、水中配体 6 443） | 单实例跑 GROMACS 2020；MEM/RIB 跑 20 k 步（跨实例 40–50 k 步），丢掉最初几千步（开局偏慢不代表长期性能）；ranks×threads 铺满核数、逐个尝试 separate PME ranks | 原文未给统一性能阈值；以 P/P（ns/美元，按美东按需价）与并行效率 E_n 排序；GPU 实例每 GPU 一个 rank、短程非键合全下放 GPU | 每实例类型 ns/d 与 ns/$ 色阶表（Tables 5–6）；结论：单 GPU 的 g4dn(4–16 vCPU) 与 g5(4–32 vCPU) 性价比全场最佳，CPU 侧 hpc6a 最优 |
| A2 | 挑选出的高 P/P 且网络 ≥50 Gbps 的实例 | 跨 1–32 实例强扩展（hpc6a、g4dn.8xl、g4dn.16xl） | 并行效率 E_n = P_n/(n×P_1)；原文未给最低可接受效率 | RIB 在 8×hpc6a 达 ~60 ns/d（E=69%）、32 实例 115 ns/d（11 倍）；MEM 扩不动（4 实例后效率 <40%、8 实例 E=0.18）；云内最好互连也达不到自建 HPC 峰值（MEM 303 / RIB 204 ns/d） |
| A3 | 4 个 FE 代表体系 | 分别基准平衡段（6 ns：10 k 步起测，丢前半；若 PME 网格调参超 5 k 步则跑 20 k 步）与变换段（取一次 50 ps/25 k 步变换计时，不丢步——80 次短变换每次都含慢启动，必须计入） | 汇总成"每个 FE 差值的成本 vs time-to-solution"散点（Fig 8）；绿色象限 = g5.2xl/g5.4xl/g4dn.xl/2xl/4xl 上 ≤15 h 且 <$20 | 每个 ΔΔG 需 12 份独立运行（复合物 3 复本×正反方向 + 水中配体同数）；2021 版可下放 PME 后 GPU 上 FE 提速超过 2 倍，故正式跑全部改用 GROMACS 2021 |

### B. 全球云跑高通量筛选（两次实盘研究）

| # | 输入 | 操作 | 判据 / 阈值 | 输出与规模 |
|---|---|---|---|---|
| B1 | Study 1 数据：Schindler 2020 的 8 个蛋白-配体体系（CDK8…HIF-2α，Table 3），每条图边 3 复本 × 2 方向 × 3 种小分子力场（GAFF 2.11 / CGenFF 3.0.1 / OpenFF 2.0.0） | 每任务 = 6 ns 平衡 + 80×50 ps 变换（从平衡轨迹等距起点出发）＝10 ns/任务 | 目标是最小化 time-to-solution；入选实例硬阈值：任何单任务 ≤9 h（g4dn.2xl/4xl/8xl + 兜底的 c5/c5d.24xl/18xl）；水中配体放 ≥8 vCPU 的 c5 上（约 5 h、<$2） | 2×9936 = 19 872 个独立任务、1656 个 ΔΔG、合计 ~200 μs 轨迹 |
| B2 | 19 872 个任务定义 | Cloud9 提交至 HyperBatch 入口；跨 6 区域按权重分发（GPU 任务权重 (6,6,3,1,1,4)）；Spot 计费；实例从 ECR 拉 pmx+GROMACS 镜像；Perl 脚本管每个任务生命周期 | 区域权重 ∝ 各区域 Spot 池大小；申请混合 vCPU 规格、大实例塞多任务；断点续跑（S3 已有输出则续传，否则重跑） | 首 30 min 拿到 ~140 000 vCPU、2 h 内 ~3000 GPU、峰值 >4000 实例、6 区域；3070 次 Spot 重启（≈15% 任务），算力损失上界 1.5% |
| B3 | 第一波 9936（蛋白体系，周一 17 时）+ 第二波 9936（配体，24 h 后） | Kibana/DynamoDB 全局监控运行中实例与区域分布 | 原文未给阈值；每波约 1 天完成 | 全部约 2 天跑完（自建数百节点集群要数周）；同数据集在 Tier-2 超算 Raven（480 节点）约 3 天 |
| B4 | 第一轮账单 | 对账：实例小时费 vs S3 传输 | S3 传输 <0.5% 总成本 | 实际 $56/ΔΔG（因收尾 glitch）；只算有效时间 $40/ΔΔG |
| B5 | Study 2 数据：14 个公开体系、只留 OpenFF 一种力场（Table 4），每边 3 复本 × 2 方向 = 6× | 改目标为最小成本：剔除低性价比实例，全部蛋白任务放 GPU Spot | 目标口径：预期落在 Fig 8 g4dn 基准区间 | 6984 任务 → 582 个 ΔΔG、70 μs；峰值 ~35 000 vCPU、平均 500 GPU 实例跑了 26 h（GPU 总时长 ~30 h，容量不足所致）；实测约 $16/ΔΔG（≈第一轮的 1/3），若配体任务也上 g4dn 可至 $14，自建 GROMACS 优化集群折算 ~$8.5 |
| B6 | 全部 ΔΔG 结果 | 正确性复核：与先前发表的同数据集计算逐值比 | Student's t test：无统计显著差异 | 云端结果与文献结果一致（本文不重报精度数字） |

**这套流程的骨架值得单独记住**：先用小基准集把"每种硬件跑这类任务的单价"测成表（A 段），再用这张表反过来定"下单白名单"（B1 的 ≤9 h、B5 的高性价比白名单），最后把执行层的失败率（Spot 重启 15%）当成可量化、可用工程手段压到 1.5% 的噪声，而不是事故。

## 4. 关键数字台账（全部来自本地全文，第 9 节逐条命中）

| 数值 | 含义 | 出处（原句片段或所在小节） |
|---|---|---|
| 19 872 任务 / 1656 个 ΔΔG / ~200 μs | Study 1 总规模（2×9936，复合物+自由配体各半） | 摘要与 §4.4.1 |
| >4 000 实例、140 000 cores、3 000 GPUs 同时 | 峰值并行资源（30 min 内拿到 vCPU、2 h 内拿到 GPU） | 摘要；§4.4.1 |
| ~2 天 vs 数周 | Study 1 云端完成时间 vs 典型数百节点自建集群 | 摘要；§4.4.1 |
| 6 ns 平衡 + 80×50 ps 变换 = 10 ns/任务 | 每个 FE 任务的轨迹配方 | §3.2 末段、§3.3.2 |
| 3 复本 × 2 方向 × 3 力场 = 18× 边数 | Study 1 任务数构成；Study 2 为 3×2=6× | Table 3/4 脚注 |
| 单任务 ≤9 h | Study 1 实例入选硬阈值 | §4.4.1 |
| ≤15 h 且 <$20 | FE 单差值成本-时间的绿色象限（g5.2xl/4xl、g4dn.xl/2xl/4xl） | §4.3.1 |
| $56 / $40 每 FE 差值 | Study 1 实际账单 / 只算有效时间 | §4.4.1 |
| ~$16（可到 $14；自建折算 ~$8.5） | Study 2 每 FE 差值成本 / 配体也上 GPU 的估计 / 自建 GROMACS 优化集群等价 | §4.4.2 |
| 约 9 倍 | 相对朴素实现的总成本削减（Spot 3× × 选实例 3×） | §5 |
| 3070 次重启 ≈ 15% 任务；最坏 1 ns；上界 1.5% | Spot 回收损耗与容忍度 | §4.4.1 |
| 折扣：Spot 最高 90%、预留 50–70%；预警 2 min | 计费模型参数 | §2.1 |
| hpc6a：10.8→~60 ns/d（8 实例，E=69%）→115 ns/d（32 实例，11 倍） | RIB 跨实例强扩展 | §4.1.3；Table 7 |
| MEM 峰值 303 / RIB 204 ns/d | 自建专用 HPC 集群同基准峰值（云内未达到） | §4.1.3（引其文献 43） |
| 4 实例后效率 <40%（127.5→201.1 ns/d 区间） | MEM 小系统扩不动 | §4.1.3；Table 7 |
| p4d.24xl/8 约 4×、g4dn.12xl/4 约 2× | 多卡改跑多任务（multidir）的性价比增益 | §4.1.2 |
| 消费级 GPU 节点 P/P ≥ CPU/专业卡节点 3 倍 | 硬件层性价比规律（选型依据） | §2.2 |
| g5.2xl 7.55 ns/d（RIB）；自建 E5-2630v4+RTX2080 节点 5.9 ns/d | 每节点产量 | §4.2 图 6 图注 |
| 3200 €/μs；<2000 €/节点；机架 500 €/U；人力 100 000 €/年；机房 30 000 €/年；管理 40 €/节点/年 | 按需 g5.2xl 轨迹成本 vs 自建各项成本 | §4.2 |
| 0.85× | 自建消费级 GPU 集群 vs Spot 云的轨迹成本比 | §5 |
| 6984 任务 / 582 ΔΔG / 70 μs；峰值 ~35 000 vCPU；平均 500 GPU 实例跑 26 h；GPU 总时长 ~30 h | Study 2 规模与资源曲线 | §4.4.2 |
| Raven 超算 ~3 天（480 节点） | 同数据集自建超算对照 | §4.4.2 |
| 85 AZ / 26 区域（2021） | AWS 规模背景 | §2.1 |
| 基准体系原子数：PEP 12 495 503 / RIB 2 136 412 / MEM 81 743 / SHP-2 107 330 / c-Met 67 291 / HIF-2α 35 546 / 水中配体 6 443 | Table 2 输入体系 | Table 2 |
| S3 传输 <0.5% 成本 | 成本结构：几乎全是计算小时费 | §4.4.1 |
| 2021 版 PME 下放 GPU 后 FE 提速 >2× | 换 GROMACS 版本的原因 | §4.3、Fig 7 |

## 5. 结论——作者说了什么

1. 在只跑 GROMACS、实例与计费选对的前提下，云与自建集群的总成本（含硬件、人力、机房、电、制冷）已到打平点（"break even"）；自建消费级 GPU 集群约为 Spot 云成本的 0.85 倍。
2. 高通量 alchemical 筛选这种"高峰值、短周期"负载，云能在约 2 天内完成自建集群要数周的任务；时间可压到 ensemble 中最长单任务的运行时间。
3. 成本可以比朴素实现降约 9 倍：Spot 替代按需（3 倍）×按基准挑最优实例（3 倍），后者的代价是 time-to-solution 变长。
4. 对 GROMACS，g4dn/g5 单 GPU 实例性价比最高，hpc6a 是 CPU 侧最优；互连最快的实例（c6i.32xl、hpc6a、c5n.18xl）扩展最好，但云内强扩展仍不及自建专用 HPC。
5. 单价可给到每个自由能差值：第二轮研究约 $16（进一步挑实例 $14），对比自建优化集群约 $8.5。
6. 云跑的结果与先前发表的计算一致（t test 无显著差异）。

## 6. 结论——我们读出了什么（以下为推断，非作者原文）

1. **这篇是"单价表"，不是"命中率表"**。它所有可迁移的东西都是成本口径（ns/day、$/FE、9 h/任务白名单、1.5% 损耗上界），一个关于"筛出来的东西好不好"的判据都没有。我们项目引用它只能引预算与排期论证，引不了任何成功概率。
2. **9 倍成本削减全部来自工程（计费方式+选型+容错），不来自算法**。同一条轨迹、同一套 TI 方法，换个买法就便宜 9 倍——这提示我们：MD 预算的方差可能主要藏在"在哪跑、怎么买、怎么容错"，不在模拟参数里。
3. **他们对"结果对不对"只做了与旧计算的一致性复核，没有对实验值重新验精度**——精度证据继承自 Schindler 2020 等前作。引用"$16/FE"时不能顺带暗示"这个价买到了验证过的精度"。
4. **≤9 h/任务的下单阈值是个好实践模板**：把"单个任务必须短于某时长"作为漏斗的实例选择约束，天然限制了断点损耗与排队不确定性。我们的 MD 预筛若要上云/上集群排队，可设同类约束（数值自定，原文数字仅适用于他们的体系）。
5. **他们为选型专门重测了 FE 基准而不是套用通用 MD 基准**（第 2 节第 5 条）→ 对应我们的教训：判据/成本数字必须来自"和目标任务同构"的实测，跨任务类型外推单价会系统性偏差。

## 7. 局限与失败（作者的 + 我们读出的）

- 作者承认：无普适的自建-vs-云结论；打平结论依赖"只跑 GROMACS 这一种软件"与消费级 GPU 的极端调优；hpc6a 当时只有按需计费所以不进 FE 成本图；GPU Spot 容量不足导致第二轮没能在 24 h 跑完；首轮有收尾 glitch 导致多花钱；价格全部是 2021 年 5 月美东快照。
- 我们读出：① 单提供商（AWS）单引擎（GROMACS），换引擎/换云没有现成结论；② 15% 重启率、1.5% 算力损耗是"2 分钟预警 + 8 段切分"这套特定容错的产物，更短预警或更大 checkpoint 粒度会改变这笔账；③ $16/FE 是 2021 Spot 价，今天美元口径不可直接照抄；④ 本文没有报告 ΔΔG 相对实验的误差（MUE 等），它只是成本研究，不能当 FEP 精度证据引用；⑤ 全文没有 QM、没有湿实验验证结合亲和力。

## 8. 对 UAA 筛选的迁移判断

**可迁移（怎么用）**

1. **成本台账口径**：我们的 MD/自由能预算应照这篇的格式记"每 ns 轨迹单价、每判定任务成本、损耗上界"（DP2R 里"通过率÷单价"同族）；run.md 里报 GPU·h 时同时报实际账单口径与有效时间口径（$56 vs $40 的双口径做法）。
2. **任务时长上限入选制**：把"单任务 >X 小时就不进这批下单"作为排期约束，超时长体系留到下一轮拆分重做。
3. **容错三件套**：checkpoint 分段、产物即时上传、被抢占自动重投——任何上云/上共享集群的长批处理直接照搬协议结构（数值阈值按我们的任务时长重定）。
4. **先测单价再下单**：对新的任务类型（如含 UAA 残基的非标准力场 MD）先跑少量代表体系测 ns/day 与 P/P，再决定实例与预算，而不是套用普通蛋白 MD 的单价。

**不可迁移（为什么不能照搬）**

1. **他们的"筛选"是已知配体网络的结合自由能排序，发生在药物流程后段**；不是设计候选的前置漏斗。$16/FE、19 872 任务这些数字不能换算成任何"UAA 酶活筛选的通量或概率"——我们的湿实验瓶颈（LC-MS/MS 产物鉴定）在他们的账本里根本不存在。
2. **本文不产出任何生物学判据**：没有阈值可用于"折叠/结合/催化"的判定；把 ns/day 当质量指标是范畴错误。
3. **Spot 经济账依赖 2021 年 AWS 定价与"只跑 GROMACS"的前提**（作者自限），我们若用混合软件栈或多引擎，0.85× 结论直接失效。
4. **140 000 核级峰值是公有云商业容量**，不是实验室自建可达；我们项目内的"global 超算"类比只能停在"用任务独立性换墙钟时间"这一组织原则上。

## 9. 溯源与自检

引句底稿: data/literature_cards/fulltext/K29_PMC9006219_text.txt

- 本地纯文本：`fulltext/K29_PMC9006219_text.txt`（Europe PMC 通路，epmc_search_then_fulltext；去标签、实体已解码、未改写内容）。
- 对照底稿：`sources/cost-benchmarks.md:66`（经典 MD 云端单价行，即本文的 g5.2xl 7.55 ns/d 与消费级 GPU 性价比结论）、`sources/cost-benchmarks.md:68`（云vs自建总成本打平行）。
- CSV 字段映射：本文第 3 节 ↔ `计算筛选判据/阈值数字/候选生成方法`；第 4 节 ↔ `候选数递减/成本统计引用`；第 8 节 ↔ `在方法演进链的位置`。
- 本卡 §2/§3 的英文引句均为从本地全文逐字复制；数字台账的每一数值都在正文或表注中原文可搜。Tables 5–11 的逐格性能矩阵与 Fig 6/8 的图上数值未在正文出现，本卡凡引用该层级数字处均取自正文明写的句子，未从图中读数。
- 自检命令：`PYTHONIOENCODING=utf-8 python scripts/verify_literature_cards.py --only "K29" --no-report`，结果见交付回报。

（CSV 回填块见下）

<!--CSV回填
work_type=方法学与成本基准论文（云端 MD / alchemical 相对结合自由能工作流）
target=8+14 个已知蛋白-配体体系（CDK8、SHP-2、PFKFB3、Eg5、c-Met、SYK、TNKS2、HIF-2α；CDK2、P38、ROS1、Bace×3、JNK1、PTP1B、PDE2、TYK2、PDE10、thrombin、galectin、MCL1）的相对结合自由能计算；非设计蛋白
backbone_generation=不涉及候选生成；蛋白-配体输入体系取自 Schindler 2020 工业 FEP 数据集与公开来源（Table 2-4）
computational_filters=按实测 ns/day 与 ns/$ 性价比选实例；Study1 只保留单任务 ≤9 h 的实例；Study2 只保留最高性价比实例；FE 计算绿色象限 = ≤15 h 且 <$20/差值
thresholds=单任务时间上限 9 h；每任务 6 ns 平衡 + 80×50 ps 非平衡变换 = 10 ns；Spot 回收预警 2 min；重启损耗上界约 1.5% 总算力
md_used=是（本文主体：GROMACS 非平衡 TI alchemical 相对结合自由能 + 纯 MD 性能基准）
qm_used=否
experimental_methods=无湿实验；仅用 Student's t test 复核与先前报告的 ΔΔG 值一致性（无统计显著差异）
pipeline_counts=Study1：8 体系 → 2×9936 = 19 872 个独立任务 → 1656 个 ΔΔG → ~200 μs → 约 2 天；Study2：14 体系单一力场 → 6984 任务 → 582 个 ΔΔG → 70 μs
hit_rate=未记录（本文是算力成本与工程研究，不报筛选命中率）
best_metric=不涉及亲和力精度（未报 MUE/R²）；性能口径：g5.2xl 对 RIB 7.55 ns/d、FE 单价 $16/差值（进一步挑实例可到 $14）
cost_or_stat_note=Spot 折扣最高 90%、预留实例 5–7 折；Study1 实际 $56/FE（仅计有效时间 $40）、Study2 约 $16/FE、自建 GROMACS 优化集群折算约 $8.5/FE；总成本较朴素实现降约 9 倍（Spot 3× × 选实例 3×）；S3 传输 <0.5% 成本；3070 次重启 ≈ 15% 任务数；自建总成本 ≈ 云端（0.85×）
role_in_timeline=把"云跑 MD/FEP"从习惯用法变成可查表的成本-时间权衡口径，给后续 MD 预筛预算提供 ns/day 与 $/FE 单价参照；不提供任何设计漏斗判据
source_pointer=data/literature_cards/fulltext/K29_PMC9006219_text.txt；sources/cost-benchmarks.md:66,68
CSV回填-->
