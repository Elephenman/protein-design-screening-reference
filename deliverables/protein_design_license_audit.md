# 第三方全文许可审计与商业分发边界

生成日期：2026-11-08　·　生成脚本：`scripts/audit_source_licenses.py`（重跑可复现；外部取回结果缓存在 `data/interim/license_cache.json`）

本文件回答一个问题：**我们缓存的这些第三方全文，哪些可以随商业产品一起再分发？**

## 结论

- 本地归档全文共 **87 行**（= `inventory.json` 里 `has_fulltext` 为真的行）。
- 许可本身允许随商业产品再分发（含商用）：**61 行**（全部是 CC BY 4.0）。
- 许可不允许或需另获授权：**26 行**。

**产品决策：商业版本一律不含任何第三方全文缓存**，无论许可是否允许。

理由有三层：

1. 26 行的许可**明确不允许**商业再分发（NC / ND / 出版商条款 / 保留所有权利 / 仅研究性复用）。
2. 另外 61 行虽是 CC BY，但再分发要逐篇履行署名、链接许可证、标注改动，打包成一个产品后这些义务的履行与追溯成本很高。
3. **一致性**：混合许可的产品在客户侧无法回答"这份文件我能怎么用"，一次说不清就会变成责任事故。

所以商业版里可以放的是**我们自己写的东西**：

- 精读卡里的方法 / 工作流 / 难点与应对（我们自己的表达）
- 我们自己的阈值台账、证据级别判定与推算（注明为我们的推导）
- 少量逐字短引句用于支撑具体论断——**引句是引用，不是全文再分发**，每条都要带文献编号，出处可查（`[B09]` 这种编号在 `data/protein_design_literature.csv` 里可查）

第三方全文缓存（`data/literature_cards/fulltext/`、`data/interim/baker_lit/`、`data/interim/claim_lit/`）只留在**内部核验库**里，用来复跑逐字引句门禁，不进任何对外发布包。

## 按类别分布

| 类别 | 行数 | 编号 | 可否再分发 | 条件 |
|---|---|---|---|---|
| CC BY 4.0 | 61 | B04 B05 B06 B07 B08 B09 B10 B12 B14 B15 B17 B18 B19 B21 B22 B23 B24 B25 B26 B27 B28 B29 B31 B32 B33 B34 B37 B40 B41 B42 B43 B44 C01 C05 C06 C13 C18 K01 K06 K28 K29 K31 K32 K33 K34 K35 K38 K39 K40 K41 K42 K44 K49 K56 K64 M-K29 M-K34 Z01 Z05 Z08 Z09 | 可（含商用） | 须署名 + 链接许可证 + 标注改动 |
| CC BY-NC-ND 4.0 | 11 | B11 B16 B20 B30 B38 B39 K48 K63 K67b Z03 Z04 | 不可 | 非商业 + 禁演绎，商业再分发需另获授权 |
| 仅文本挖掘 / 公平使用 | 4 | B02 B03 C03 K65 | 不可 | 只允许检索与挖掘，不可再分发全文 |
| CC BY-NC 4.0 | 4 | C19 C20 K43 K47 | 不可 | 非商业用途限定，商业再分发需另获授权 |
| CC BY-ND 4.0 | 3 | C16 C21 C23 | 不可（须原样） | 禁演绎；抽取/改写即不再是同一份，谨慎处理 |
| 出版商使用条款（无 CC 声明） | 2 | B01 Z02 | 不可 | 按出版商条款使用，不可再分发全文 |
| 仅研究性复用（须注明来源） | 1 | C04 | 不可 | 只授权研究性复用，非商业再分发不在授权范围内 |
| 保留所有权利（禁止再分发/复用/改编） | 1 | C22 | 不可 | 作者明确保留所有权利，须另行授权 |

## 逐行明细

| 编号 | 许可 | 可否再分发 | 证据来源 | 证据原文（截断） |
|---|---|---|---|---|
| B01 | 出版商使用条款（无 CC 声明） | 不可 | data/interim/baker_lit/ft/switches2019.txt | e purposes of academic research, subject always to the full Conditions of use: http://www.nature.com/authors/editorial_p |
| B02 | 仅文本挖掘 / 公平使用 | 不可 | data/literature_cards/fulltext/B02_PMC7532806_fullTextXML.xml | <permissions><license><license-p>This file is available for text mining. It may also be used consistent with the princip |
| B03 | 仅文本挖掘 / 公平使用 | 不可 | data/literature_cards/fulltext/B03_PMC9293396_fullTextXML.xml | <permissions><license><license-p>This file is available for text mining. It may also be used consistent with the princip |
| B04 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/B04_PMC7971855_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| B05 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/proteinmpnn2022.txt | creativecommons.org/licenses/by/4.0 |
| B06 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/cao2022.txt | creativecommons.org/licenses/by/4.0 |
| B07 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/smallfolds2022.txt | creativecommons.org/licenses/by/4.0 |
| B08 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/rfdiffusion2023.txt | creativecommons.org/licenses/by/4.0 |
| B09 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/binderDL2023.txt | creativecommons.org/licenses/by/4.0 |
| B10 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/luciferase2023.txt | creativecommons.org/licenses/by/4.0 |
| B11 | CC BY-NC-ND 4.0 | 不可 | data/interim/baker_lit/ft/betaBarrel2023.txt | creativecommons.org/licenses/by-nc-nd/4.0 |
| B12 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/helicalpeptide2024.txt | creativecommons.org/licenses/by/4.0 |
| B14 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/tnfr2024.txt | Creative Commons Attribution 4.0 International |
| B15 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/macrocyle2025.txt | creativecommons.org/licenses/by/4.0 |
| B16 | CC BY-NC-ND 4.0 | 不可 | data/interim/baker_lit/ft/mp3seq2024.txt | creativecommons.org/licenses/by-nc-nd/4.0 |
| B17 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/serinehydrolase2025.txt | Creative Commons Attribution 4.0 International |
| B18 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/metallohydrolase2026.txt | creativecommons.org/licenses/by/4.0 |
| B19 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/placer2025.txt | creativecommons.org/licenses/by/4.0 |
| B20 | CC BY-NC-ND 4.0 | 不可 | data/interim/baker_lit/ft/rfdiff2_natmeth.txt | creativecommons.org/licenses/by-nc-nd/4.0 |
| B21 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/idp_binder2025.txt | creativecommons.org/licenses/by/4.0 |
| B22 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/antibodyRFdiff.txt | creativecommons.org/licenses/by/4.0 |
| B23 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/beta_pairing2026.txt | creativecommons.org/licenses/by/4.0 |
| B24 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/accelscaling2026.txt | creativecommons.org/licenses/by/4.0 |
| B25 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/nanocage_hier2025.txt | creativecommons.org/licenses/by/4.0 |
| B26 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/energyfunc2026.txt | creativecommons.org/licenses/by/4.0 |
| B27 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/dnabinding2025.txt | creativecommons.org/licenses/by/4.0 |
| B28 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/B28_PMC11978504_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| B29 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/memprot_analogue2024.txt | creativecommons.org/licenses/by/4.0 |
| B30 | CC BY-NC-ND 4.0 | 不可 | data/interim/baker_lit/ft/autotwo_comp2024.txt | creativecommons.org/licenses/by-nc-nd/4.0 |
| B31 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/smallmol_family2026.txt | creativecommons.org/licenses/by/4.0 |
| B32 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/immune_receptor_binder2025.txt | creativecommons.org/licenses/by/4.0 |
| B33 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/B33_PMC10115654_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| B34 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/buttressedloops2024.txt | creativecommons.org/licenses/by/4.0 |
| B37 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/fap2021.txt | creativecommons.org/licenses/by/4.0 |
| B38 | CC BY-NC-ND 4.0 | 不可 | data/interim/baker_lit/ft/oligomorph2025.txt | creativecommons.org/licenses/by-nc-nd/4.0 |
| B39 | CC BY-NC-ND 4.0 | 不可 | data/interim/baker_lit/ft/confdyn2023.txt | creativecommons.org/licenses/by-nc-nd/4.0 |
| B40 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/chlorophyll2024.txt | creativecommons.org/licenses/by/4.0 |
| B41 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/fourcomp_cages2025.txt | creativecommons.org/licenses/by/4.0 |
| B42 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/endocytosis2025.txt | creativecommons.org/licenses/by/4.0 |
| B43 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/snakvenom2025.txt | creativecommons.org/licenses/by/4.0 |
| B44 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/integrin_miniprot2023.txt | creativecommons.org/licenses/by/4.0 |
| C01 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/C01_PMC7857403_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| C03 | 仅文本挖掘 / 公平使用 | 不可 | data/literature_cards/fulltext/C03_PMC8074680_fullTextXML.xml | <permissions><license><license-p>This file is available for text mining. It may also be used consistent with the princip |
| C04 | 仅研究性复用（须注明来源） | 不可 | data/literature_cards/fulltext/C04_PMC8221914_fullTextXML.xml | epositories, such as the WHO COVID database with rights for unrestricted research re-use and analyses in any form or by  |
| C05 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/C05_PMC8920274_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| C06 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/C06_PMC9258422_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| C13 | CC BY 4.0 | 可（含商用） | data/interim/claim_lit/PMC11614891.xml | creativecommons.org/licenses/by/4.0 |
| C16 | CC BY-ND 4.0 | 不可（须原样） | https://doi.org/10.1101/2024.02.10.579791 (sha256 11464e0f9937ed62…) | creativecommons.org/licenses/by-nd/4.0 |
| C18 | CC BY 4.0 | 可（含商用） | data/interim/claim_lit/PMC13121834.xml | creativecommons.org/licenses/by/4.0 |
| C19 | CC BY-NC 4.0 | 不可 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1101/2025.1 | cc by-nc |
| C20 | CC BY-NC 4.0 | 不可 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.64898/2026. | cc by-nc |
| C21 | CC BY-ND 4.0 | 不可（须原样） | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.64898/2026. | cc by-nd |
| C22 | 保留所有权利（禁止再分发/复用/改编） | 不可 | https://doi.org/10.64898/2026.01.06.697903 (sha256 94561154b9128d2c…) | xiv. The copyright holder for this pre-print is the author. All rights reserved. The material may not be redistributed,  |
| C23 | CC BY-ND 4.0 | 不可（须原样） | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.64898/2026. | cc by-nd |
| K01 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K01_PMC12923136_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K06 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K06_PMC12432402_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K28 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K28_PMC9184281_text.txt | creativecommons.org/licenses/by/4.0 |
| K29 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K29_PMC9006219_text.txt | creativecommons.org/licenses/by/4.0 |
| K31 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K31_PMC9278006_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K32 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K32_PMC10751731_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K33 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K33_PMC10273344_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K34 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K34_PMC13213910_text.txt | creativecommons.org/licenses/by/4.0 |
| K35 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K35_PMC12721093_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K38 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K38_PMC13513569_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K39 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K39_PMC13113996_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K40 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K40_PMC13099138_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K41 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K41_PMC12412469_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K42 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K42_PMC13225634_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K43 | CC BY-NC 4.0 | 不可 | data/literature_cards/fulltext/K43_PMC12661943_fullTextXML.xml | creativecommons.org/licenses/by-nc/4.0 |
| K44 | CC BY 4.0 | 可（含商用） | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=12264970&ret | creativecommons.org/licenses/by/4.0 |
| K47 | CC BY-NC 4.0 | 不可 | data/literature_cards/fulltext/K47_PMC10025429_fullTextXML.xml | creativecommons.org/licenses/by-nc/4.0 |
| K48 | CC BY-NC-ND 4.0 | 不可 | data/literature_cards/fulltext/K48_PMC11425640_fullTextXML.xml | creativecommons.org/licenses/by-nc-nd/4.0 |
| K49 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K49_PMC13031676_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K56 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/K56_PMC8204736_fullTextXML.xml | creativecommons.org/licenses/by/4.0 |
| K63 | CC BY-NC-ND 4.0 | 不可 | data/interim/baker_lit/ft/kemp2025.txt | creativecommons.org/licenses/by-nc-nd/4.0 |
| K64 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/motifscaffold2026.txt | creativecommons.org/licenses/by/4.0 |
| K65 | 仅文本挖掘 / 公平使用 | 不可 | data/literature_cards/fulltext/K65_PMC5940506_fullTextXML.xml | <permissions><license><license-p>This file is available for text mining. It may also be used consistent with the princip |
| K67b | CC BY-NC-ND 4.0 | 不可 | data/literature_cards/fulltext/K67b_PMC13277954_fullTextXML.xml | creativecommons.org/licenses/by-nc-nd/4.0 |
| M-K29 | CC BY 4.0 | 可（含商用） | data/interim/claim_lit/PMC13038408.xml | creativecommons.org/licenses/by/4.0 |
| M-K34 | CC BY 4.0 | 可（含商用） | data/interim/baker_lit/ft/nirFAP2026.txt | Creative Commons Attribution 4.0 International |
| Z01 | CC BY 4.0 | 可（含商用） | data/interim/claim_lit/PMC13368180.xml | creativecommons.org/licenses/by/4.0 |
| Z02 | 出版商使用条款（无 CC 声明） | 不可 | data/interim/claim_lit/epcam.xml | g/site/aboutpnas/licenses.xhtml</ali:license_ref><license-p>Published under the <ext-link xmlns:xlink="http://www.w3.org |
| Z03 | CC BY-NC-ND 4.0 | 不可 | data/interim/claim_lit/PMC12865018.xml | creativecommons.org/licenses/by-nc-nd/4.0 |
| Z04 | CC BY-NC-ND 4.0 | 不可 | data/literature_cards/fulltext/Z04_PMC10120010_fullTextXML.xml | creativecommons.org/licenses/by-nc-nd/4.0 |
| Z05 | CC BY 4.0 | 可（含商用） | data/interim/claim_lit/PMC11994915.xml | creativecommons.org/licenses/by/4.0 |
| Z08 | CC BY 4.0 | 可（含商用） | data/literature_cards/fulltext/Z08_PMC12613313_text.txt | creativecommons.org/licenses/by/4.0 |
| Z09 | CC BY 4.0 | 可（含商用） | data/interim/claim_lit/PMC12240735.xml | creativecommons.org/licenses/by/4.0 |

## 待人工确认

- 无。

## 口径说明

1. 这里的"再分发"指把**第三方全文文件本身**（XML / 抽取文本）放进产品或公开仓库。
2. 卡片里的**短引句**与**我们自己的转述、方法总结、阈值台账**不在受限范围内——那是引用与原创分析；但引用量要小、标明出处、且不得被当作原文的替代品。
3. "可（含商用）"表示许可本身允许商业性再分发，**仍须履行署名/相同方式共享等条件**；本审计不替代法律意见。
4. 预印本（bioRxiv 等）默认多为 CC BY-NC-ND，**按不可再分发处理**；正式发表版可能是 CC BY，因此下架预印本缓存、改用已发表版引句是更稳的做法。
5. 本审计只判**许可文本**与**能不能再分发**，不判内容对错，也不替代法律意见。若要正式商用，建议对受限的 26 篇按需单独向权利人申请授权。
6. 公开克隆里没有第三方原文（按公开再分发口径不入库），此时本脚本的许可类别取自 `deliverables/fulltext_manifest.csv` 的快照列，**类别不变**，但"证据来源"列会指向清单（含该文件的 sha256 与重取方式）而不是原始 URL。

