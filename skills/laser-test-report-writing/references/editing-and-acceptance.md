# DOCX 局部编辑与验收接口

## 纯文本格

scripts/docx_safe_edit.py 的 set_cell_text(tc,text,color="000000") 仅用于纯文本格。保留tcPr、首段pPr和首个rPr，重建文本并显式指定字体颜色；空格使用xml:space preserve，换行使用w:br。改焊前格调用时指定595959。含公式、图片、域、超链接或修订的格拒绝处理，必须逐对象编辑。

不要克隆深蓝表头当普通数据格后只改底色：rPr仍可能为白字。修改底色同时核对文字颜色。vMerge延续格用底层XML验证，不用python-docx合并后重复的cell代理推断结构。

## 表格与分页

- 两级表头两行均tblHeader；vMerge、gridSpan和tblGrid共同核对。
- tblW/tcW的pct是百分之一的五十分之一（100%=5000），dxa为twips；不混用数字。修改时保持总宽、网格和跨列宽一致。
- cantSplit防止单行内拆分；配对后/前行还要在首行段落设置keepNext。仅短比较表适合整表同页，长矩阵不得全部链成不可分页块。
- 新表深蓝1F4E79/白字，后行B8CCE4，前行E5B8B7/595959；旧合法变体按改焊参考保留。
- --table-profiles JSON 示例：{"3":{"required_columns":["完整性","最差隔离度"]}}。表号为1起；只有明确表型才要求这些列，值消费分析汇总，不在编辑脚本重新计算。

## 作用域核验

audit_result_summary_docx.py <after> --mode surgical --before <before> --scope-json <scope.json> --json

scope键 before_body/after_body 是word/document.xml正文直接子节点的1起索引，分别列出允许修改/插入/删除的节点；其余节点序列和属性必须相同。allowed_parts 列出明确授权修改的精确ZIP部件名，例如本次替换图片对应word/media/image1.png；不能整包豁免document.xml。表内局部修改时另核对未改格的内容/属性，不把授权修改一个表节点当作可以改整表。

只运行 --mode surgical 而未提供基线和scope，输出scope_verified=false，只是全局建议。局部工作必须完成差异核验，不因全局建议重新排版。对新文档使用 --mode new --final-content；模板含占位内容，不加final-content。

## 占用、视觉与交付

snapshot(path) 检查~$锁文件和Windows目标独占读取，再记录size/mtime/SHA-256；不因其他WINWORD进程阻止操作。编辑前后重新比较，源变更则回到最新用户版，不能覆盖并发修改。不要自动关Word或杀进程。

用LibreOffice独立用户配置目录渲染任务副本，pdftotext定位、pdftoppm出页图。第一轮查看全部改动页及相邻分页，新文档看全页；修复后第二轮复查问题页/关联页。可用视觉工具不限于历史visual-judge；没有能力时标未验证。

先将通过验证的文件交付到授权位置，再读回检查文件内容和哈希，最后记录MD5/SHA-256。渲染缓存不是正式交付物。

## 严格局部验收与图片身份

`audit_result_summary_docx.py after.docx --mode surgical --strict --before before.docx --scope-json scope.json` 同时检查越界和新增表格缺陷。未变的历史缺陷为警告，新白底白字/网格错误仍失败；没有基线不能宣称局部验收通过。

单元格 scope 示例：`{"before_body":[],"after_body":[],"allowed_parts":[],"cells":[{"before_body":[2,3,1],"after_body":[2,3,1]}]}`。三元组为正文直接子节点、XML 行、物理 tc 的 1 起索引；合并格不能用可视列号替代。cell-scoped 表不能同时整体豁免，未授权格、行属性和表属性继续比较。

figure manifest 原八列保留；新改图严格模式补 source_path、source_sha256、traceability_row，可选 embedded_part、embedded_sha256。source_path 相对 manifest 所在目录；traceability_row 是七列表格的数据行 1 起索引，器件/接口须一致且图源在对应分析结果路径内。使用 `audit_figure_mapping.py report.docx --manifest figures.csv --strict --mode new`；局部用 --mode surgical --before baseline.docx。字节相同或可解码后的 RGBA 像素完全一致通过身份检查；有损变换需保留经核实的派生图及哈希，不用近似相似度自动认证。旧图只有题注和嵌入字节都未变才免新增字段，仍标明旧图身份未重新认证。单项结构 passed 不等于严格身份通过。
