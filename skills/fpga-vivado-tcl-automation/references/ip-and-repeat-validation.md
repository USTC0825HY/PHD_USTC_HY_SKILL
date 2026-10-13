# IP 登记与重复执行

模板配置 `ip_sources` 可省略，默认空列表；填写最终 `.srcs/sources_1/ip/` 下的 XCI/XCIX 路径。兼容 `sources` 中的 IP，内部单独处理；两处指定同一路径报错。不要同时列 XCIX 及其虚拟 XCI。`sources` 仍要求非空硬件源码，约束和仿真列表允许显式为空。

首次先创建原生空工程，再执行项目自己的 `prepare_sources`。需要外部 IP 时，在该首次准备步骤使用本版本 Vivado 的导入流程，将最终路径写入配置；核验 component/version/config/port、关联数据和 OOC 设置。准备步骤是需要检查其副作用的项目代码，不是每次同步都执行的复制任务。

已有工程只检查身份、源清单和逻辑 IP，不再次调用准备步骤，不重设 OOC/增量属性，不无条件 generate_target 或 reset_run。输入不匹配报告差异，由用户任务范围决定后续修复；不自动迁移。模板保留 create/check/synth/impl/bit 接口，默认 create。

每个仿真用例用独立显式清单/仿真源集，同名模型不能合并编译，更不能递归加入硬件源集。模板的 sim_sources 表示本次选定 sim_1 清单；切换已有工程的仿真清单需显式配置操作，不由重复 create 偷换。

## 静态检查器的证据

`project_inputs.py` 保留原 inputs/runs/issues/status 字段，新增 logical_ips、active_ip_count、containers。inputs 中容器虚拟成员附 container/container_member，exists 表示物理文件或已验证的容器成员；sha256 为实际成员内容。独立 BlockSrcs 的 OOC run 关联及启用属性参与判断；缺少关联返回 needs_review。此处“活动”表示工程登记的阶段输入，不声称所有 IP 在 HDL 顶层可达。

XCIX ZIP 校验 CRC、成员路径和根 XCI，再按相同文件集的虚拟路径关联；逻辑计数合并容器及根 XCI，成员清单保留大小/哈希。无法确定的关联或 BD 依赖需工具证据；缺失/损坏容器、配置身份不符、重复登记失败。历史 ImportPath 和历史 run 元数据不作为当前输入文件打开。

静态通过只证明所检查的登记、身份及文件存在性；不执行有效 Tcl/XDC、不证明 IP 全部外部资产或工具配置兼容。随后按任务范围分别进行语法、RTL elaboration、综合实现和板级测量。OOC stub 展开成功不能替代 IP 内部实现验证。

重复执行验收：记录输入哈希、run 名称/目录/状态，关闭重开再执行并比较；确认未生成旧 build/rtl/ip/targets 树。原生缓存及 GUI 日志允许按工具行为变化。新增版本支持必须在隔离目录复验，不把旧工具案例视为新版本事实。
