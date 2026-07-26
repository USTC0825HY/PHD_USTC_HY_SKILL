# Template Contract

Use `assets/超稳激光电控箱测试报告标准模板.docx` as the style source for formal Word reports.

## Required Template Features

1. The title uses `报告题名`, the visible subtitle uses `报告短题名`, and neither is part of the outline.
2. The cover uses a two-column information table plus a revision-history table. It records version, test time, report date, location, personnel, and author/reviewer/approver.
3. Cover, directory, and body use separate new-page sections. The cover has no page furniture, the directory uses lower-Roman numbering, and the body uses a short-title `STYLEREF` header plus decimal numbering restarted at 1.
4. A `TOC \\u` field covers outline levels 1 through 3, including the unnumbered custom level 3.
5. `TOC 1/2/3` explicitly define left alignment, zero first-line indent, 0/21/42 pt level indents, and a right-aligned dotted page-number tab at 14.65 cm.
6. The visible quick styles are `一级标题`, `二级标题`, and `三级标题`. They use Microsoft YaHei at 15/12/12 pt, are bold, have Word outline levels 1/2/3, use the spacing in `style_contract.py`, and enable pagination protection.
7. All three styles share the automatic `1.`/`1.1`/`1.1.1` list at 510/226 twip left/hanging indents.
8. Ordinary numbered lists use an independent definition and cannot advance section numbering. When a legacy file reused the heading definition, preserve the visible list labels while detaching it from the section list.
9. Table and figure captions use `图表题注` plus `SEQ 表` or `SEQ 图` fields.
10. Normal body text, captions, tables, images, and report information use the dedicated styles in `report-standard.md`.
11. Tables use `报告表格样式`, `DDEBF7` header fill, white body fill, and `808080` 0.5 pt single borders. Cells use 85 twip vertical and 102 twip horizontal margins. Only formal values in a `结论` column receive the four restrained status fills. Cell paragraphs use `表格表头` or `表格文字`, have explicit zero point and character-unit indents, center the table object and all content, fit within the body width, repeat the header row, and prevent data-row splitting.
12. Image-anchor paragraphs use `图片`, have zero point and character-unit paragraph indents, and remain centered whether the image is in body text or a layout table.
13. Formula paragraphs contain Pandoc-generated professional OMML from LaTeX; the template ASD formula contains a real subscript and radical structure.

## Required Section Skeleton

Use the following neutral placeholders in a new report:

- `测试目的与结论摘要`
- `测试对象、接口与公共条件`
  - `被测对象及接口映射`
  - `端接、负载、时钟与软件状态`
  - `公共采集条件`
- `测试仪器、系统连接与数据处理方法`
- `分器件或分链路测试结果`
  - 每个结果项依次使用三级标题填写测试指标与条件、测试方法、数据处理、结果分析和指标判定
- `异常现象、证据限制与未测试项`
- `指标实测对比总表与后续计划`
  - `指标实测对比`
  - `后续测试计划`
- `附录`
  - `计算公式与处理参数`
  - `仪器设置与原始记录`
  - `数据与脚本索引`

Replace placeholders with actual device names and evidence. Keep one core result-summary table in the opening chapter. Put item-specific methods, processing, result figures, and conclusions inside the corresponding device/result subsection and remove the placeholder image after replacement. Delete empty sections only when they are not applicable; do not add an unnumbered replacement heading.

## Legacy Report Conversion

Create a copy first. Classify paragraphs in this order:

1. First nonempty paragraph becomes the title.
2. `测试时间` through `测试内容` become `报告信息`.
3. Existing section headings become `一级标题/二级标题/三级标题` after stripping a leading manual number; level 3 remains unnumbered.
4. Figure and table captions become `图表题注`; retain their descriptive text and replace typed sequence numbers with fields.
5. Image-anchor paragraphs become `图片`; table cells become `表格表头` or `表格文字`.
6. Normal narrative remains Normal unless it is a mislabeled heading.

Use `--append-required-sections` only when a legacy report lacks a follow-up-test or data-source section; the script inserts empty `待填写` rows rather than inventing evidence. Do not force the old `指标需求与判定依据` chapter into a reconstructed engineering report.

Review every conversion result. Automated conversion must not infer the meaning of an unnumbered ordinary paragraph.
