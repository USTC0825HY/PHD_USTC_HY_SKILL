# 单一记录与脚本接口

## 文件关系

`manifest.json` 保存当前板版本、证据、节点、逐段路由和展示字段；`profile.json` 保存独立核对后的预期地址、物理输入、级联入口、连接器配对及选源条件。不要从待检路由直接抄一份profile作为“独立验证”。`changes.json` 只说明本次允许的表格变化。

从assets模板开始填入任务数据。模板为未完成记录，检查应返回needs_review。每条稳定记录只维护一份display字段，各视图绑定同一记录。完整路由文字和endpoint仍须人工与segments对照；自动字符串相等不是原理图取证。

## schema_version=2：多链路及不同视图范围

v1保持原有地址键兼容。新多链路任务使用`manifest.v2.template.json`和`profile.v2.template.json`，manifest/profile的schema_version须一致；changes仍为1。

- route新增非空唯一`route_id`及`chain_id`；address只存规范HEX（不带链路前缀或括号）。已知地址的唯一键为(chain_id, 数值地址)。未知address可为null，链路也未知时chain_id为null，检查返回待核验。不同链路同号地址合法，同一链路重复地址报错。
- profile.expected_routes以route_id为键，每项显式含chain_id和address（允许null），其余input/mux/endpoint/选源检查沿用v1。input用全局唯一的板卡／器件输入ID；未知输入为null并返回待核验。
- display.address_text保存完整展示值，例如`0x05（IN5）`，不能从它模糊推导ADC类型或命令。板卡／信号显示字段共同核对身份。v2中显式null表示对应单元格应为空；缺少字段不是空值，仍报告缺少预期。不同视图的简短名称和详细描述可绑定不同display字段，但通道身份和技术参数仍共用同一记录。
- 每张workbook.sheets声明`route_ids`（本视图的非空唯一子集）及`row_bindings`（字符串行号到route_id）。绑定必须精确覆盖first_data_row至last_data_row，包括筛选隐藏行。脚本逐格比较address_text及fields；排序或编辑后需重新建立绑定，不把旧行号当记录身份。
- 装配确认scope在v2增加`version`，与boards[board].version相符；TSD覆盖必须同时匹配板卡、版本和位号。v1旧记录仍按原语义检查。

v2只扩展记录检查，不解析原理图、不计算任意字符串公式。各视图的route_ids可不同；交集技术字段应一致，额外通道不自动加入简表或笔记。

## manifest，schema_version=1

| 字段 | 内容 |
| --- | --- |
| boards | 板卡ID -> label、version、evidence_set；当前每板一套连接依据 |
| evidence | 证据ID -> kind、locator、path、sha256；path相对manifest目录或绝对路径 |
| nodes | 节点ID -> board、ref、pin、net；net保留精确内部网名，pin用字符串 |
| routes | 每地址一条，字段见下文 |
| workbook | 表单与字段绑定、可选局部加粗及数值缓存检查 |

证据kind使用 `netlist`、`schematic`、`rtl`、`datasheet`、`interface_confirmation`、`assembly_confirmation`、`continuity`。文件证据提供真实path及SHA-256；确认记录可无文件，但locator应写日期、内容和出处。assembly_confirmation还包含 `scope: {board, refs:[...]}`，限定板卡与位号。测试夹具可用临时文本作为证据，仅说明脚本行为，不构成硬件证明。

route字段：

- address为`0x00`形式文本；kind为ground/measurement；mode、status为当前模式与complete/partial/unavailable。
- input是profile.physical_inputs里的ID；mux为各级器件到S输入选择的对象。
- segments顺序反向追踪，每段包含kind、from/to节点ID、evidence证据ID列表；kind为net/component/connector/gap。
- component段另有component对象：ref、value、marker、state、assembly_evidence。state为fitted/unfitted/unknown。两端必须是同位号的不同脚。
- gap段用note说明缺口，路线不得标complete。
- source_board、source_interface和endpoint分别为源板ID、源接口节点ID、原始测点节点ID；本板基准的source_interface使用local。复杂差分测点以一个主endpoint结束，另在记录中保存另一端及极性，不将两端短接成net段。
- 可选summary_endpoint/detail_endpoint在已有外部记录归并时检查一致，正常情况无需复制。
- conversion保存bits、coding、vref、vref_basis；output_kind为adc_voltage或physical_quantity。后者必须有source_parameters_confirmed=true、source_formula、source_unit，并在外部取证中支持其参数。
- display存两表用的文字字段，如source_board_label、source_interface_text、endpoint_text、route_text、conversion_text。内部net与展示别名不得混为一项。

脚本支持的标准码制：twos_complement、offset_binary、unipolar_binary，比例均为对应标准理想传输模型；非标准器件/量程模型单独复核。decode_adc是数值助手，不执行任意字符串公式。

## profile，schema_version=1

- mode：此次选源模式。
- physical_inputs：输入ID -> {node}。物理S输入全部列入，包括级联、接地与未接输入。
- cascade_inputs：属于级联入口的输入ID。
- expected_routes：地址 -> input、mux，可加source_board、endpoint、required_components、forbidden_components。
- connector_pairs：from/to节点ID、evidence列表；一条代表一对物理接触位置。双针并接应逐接触位记录，不用模糊区间代替。

脚本检查图内声明及源文件哈希，不解析PST。独立PST查询仍由现有技能完成。配对表中重复或自相矛盾的定义、未绑定的跨板完整路线应被检出。未使用输入也需有明确路线状态，不可从覆盖统计中隐去。

## workbook绑定

每张表指定name、header_row、first_data_row、last_data_row、address_column、headers（列字母到表头文字）、fields（列字母到display字段）、route_columns（扫描展示符号/内部网号的列）。v1按地址匹配，v2按显式route_id绑定；均不依赖两表排序一致。

可选 `required_bold: [{sheet,cell,text}]` 检查富文本局部加粗。`numeric_checks: [{sheet,cell,expected,tolerance}]`检查已存数值；不证明已重新计算。没有数值缓存时报告待复核，不当0。

## changes，schema_version=1

```json
{
  "schema_version": 1,
  "cells": {"遥测简表": {"G14": ["value", "runs"]}},
  "moves": {},
  "meta": {},
  "rows": {},
  "parts": []
}
```

cells按输出坐标白名单，允许字段仅为value/formula/style/runs/attributes。修改富文本通常需value及runs，但这不是允许把所有字设成同一字体；指定required_bold和视觉检查补充验证。moves为表名 -> 旧坐标到新坐标的映射；移动后的单元格仍逐字段检查。meta允许精确sheet子项，如cols、sheetViews、mergeCells、autoFilter、dimension；rows允许明确行号的高度等属性改变；parts允许明确ZIP成员变化，如某个table XML或某幅图。

保留的字符即使因改字拆分/合并了runs，其字体和粗体仍应不变。只有明确授权局部重排字体时，另加typography许可。新增字符的格式和复杂跨运行样式仍须视觉复核。

白名单不支持通配符。不能为了全绿列出所有单元格和所有parts。新增/删除表单目前只报告差异，不在该保真检查器中自动放行；此类任务另行人工验收。

## 命令与返回值

```text
python scripts/audit_routes.py --manifest manifest.json --profile profile.json --report route-check.json
python scripts/audit_workbook.py --before before.xlsx --after after.xlsx --manifest manifest.json --changes changes.json --report workbook-check.json
```

Python仅用标准库；无Excel、无网络调用、无源文件写入。报告路径必须与所有输入不同且尚不存在。出现错误时输出input_error，不清空旧报告。

- 0 passed：已实现检查未发现异常，不包含视觉/硬件验收。
- 1 failed：确定的映射、结构或保留差异。
- 2 needs_review：证据、模型、覆盖或缓存不足。
- 3 input_error：文件、格式或报告目标错误。

结果含finding代码、位置、统计和输入哈希。源文件哈希不同视为证据发生变化，不静默采用旧结论。任何失败都不自动修复。
