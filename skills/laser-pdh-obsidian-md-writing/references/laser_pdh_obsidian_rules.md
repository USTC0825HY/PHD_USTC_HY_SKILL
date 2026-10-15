# Laser/PDH Obsidian规则

## 位置与范围

先读科研主系统AGENTS.md/MEMORY.md；当前按研究活动分类：理论02、文献03、建模04、RTL05、实验06、分析07、论文汇报08、资料工具09、治理99。513/CW已完成阶段仍在06实验测试。旧`02_Laser_PDH知识体系`、`03_超稳激光系统工程`等名称仅用于历史定位，不自动重建。

同一正文只保留一个主位置，其他项目通过导航链接。原始工程、完整原理图、大型数据及正式报告留在权威资产目录；笔记保留必要局部图和来源链接。个人记录、QID、公式编号、块ID、已有标题定位和needs_check不因整理丢失。

## 写作与元数据

新正式Laser笔记可使用`cssclasses: [laser-pdh-note]`，并记录title、project、status、created/updated、category、note_type、source_origin。保留现有有效frontmatter；缺少未知信息不编造值。不要把所有项目强行改名为Laser_PDH_Study。

普通教学笔记可按核心结论、问题、物理图像、推导、实验关联和来源展开；遥测笔记按`telemetry-note-layout.md`组织。源文不能原样堆成正式笔记。区分原始事实、计算推导与实测结果，文字简明但不删除影响结论的条件。

内部知识使用Wikilink。资产链接可用已核实的绝对路径，笔记本地资源优先相对路径。需要Question_Index、Formula_Index或来源映射时先查其当前实际位置，不按旧路径新建第二套。索引更新限于本次明确范围，不扫描全库后顺带改写无关内容。

## 检查

本地修订用`audit_laser_pdh_md.py --root <科研主系统> --file <笔记>`，可重复指定。检查链接存在、图片、Mermaid配套、公式与表格风险；渲染、缩放、截图可读性另行检查。备份与哈希记录留在本次任务证据目录，不写满长期MEMORY。
