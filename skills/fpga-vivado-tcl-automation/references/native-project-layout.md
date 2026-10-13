# 新工程：Vivado GUI 原生布局

这是用户的新建工程偏好，不是旧工程迁移或清理授权。使用目标 Vivado 的 Project Mode 原生流程；不手改 XPR XML，不套用其他版本的生成目录。

```text
<project>/
  <project>.xpr
  <project>.srcs/
    sources_1/
      new/
        top/<top>.v
        clock_reset/
        adc_acquisition/<device>/
        dac_output/
        dds_control/
        telemetry/
        common/
      ip/                  # 工具管理
      bd/                  # 实际需要时才有
    constrs_1/new/pins.xdc
    constrs_1/new/xilinx_debug.xdc   # 有调试约束才创建
    sim_1/new/<function>/
    reference/             # 非活动参考输入，不递归登记
    utils_1/               # 工具需要时保留
  <project>.runs/           # 工具按需生成，下同
  <project>.cache/
  <project>.sim/
  <project>.hw/
  <project>.ip_user_files/
  scripts/config/          # 显式源清单；长期脚本位于 scripts
  docs/provenance/         # 来源、冻结身份与映射
  docs/logs/               # 自动化日志
  release/                 # 正式发布才建立
```

示例功能名不是必须创建的目录列表；不建空目录。`.gen`、`.Xil` 和 IP 产品位置随工具版本，不手动搬移来美化。

## 源码与分类

- 先用目标版本创建原生空工程，再把手写 RTL 直接写入 `.srcs/sources_1/new/<功能>/`，然后按引用加入 sources_1；不得再 import/copy 一份活动源码。2018.3 会拒绝在预先存在同名 .srcs 的位置 create_project，不得用 -force 绕过。默认工程内自包含；必要外部库明确来源和依赖，禁止任务临时路径依赖。
- 第一层按稳定功能板块，必要时第二层按器件。不按 wire/reg/always 或临时 misc/new2 分类。用户明确选定的 u1_test～u12_test 等稳定分类可沿用，记录实例/模块映射；不将某工程编号硬编码为通用要求。
- 默认一文件一主要模块，文件名与模块名一致；冻结/第三方文件不自动拆分。原生与派生身份在功能板块内记清，不让全工程首先按 original/adapted/new 拆散功能。
- common 仅放确实共享且语义一致的模块。磁盘分组不是 HDL 层次，不能为目录增加空包装模块。
- 冻结/第三方文件保持字节和文件边界，通过来源记录及 SHA-256 维护身份；非活动 RTL/IP/约束放 `.srcs/reference`，禁止递归加入硬件源集。仿真模型按用例独立显式清单，避免同名模型混编。
- TB 与夹具放 sim_1 对应功能目录，不进入综合源集。IP/BD 由 Vivado 原生流程管理，不手工复制生成文件。
- 约束采用 [共享 XDC 风格](xdc-project-style.md)，有调试约束才创建 debug XDC；不能为凑文件数创建空文件。

## 目录卫生

- 根目录只保留 XPR、原生工具目录、必要治理文件和实际使用的 scripts/docs/release；不新增平行 build/build_vivado、output/tmp、日期备份或散落脚本/报告。
- 自动化显式将启动 log/journal 和工作目录放 `docs/logs/<唯一运行标识>/`；项目模式 runs/sim 仍用原生位置。独立仿真使用专用运行目录，不从工程根启动产生 xsim.dir。
- GUI 正常生成的日志、.Xil、缓存不算布局错误；不为了“零日志”删除活动缓存、历史 run 或失败现场。
- 一次性实验、审计和备份放工作区 `.codex_work/<任务>/`，不能成为工程依赖。正式结果留原生 run；发布时有选择地复制到 release，记录输入、工具和 BIT/LTX 身份。
- .gitignore 逐类排除可再生产物，不整段忽略 .srcs，不忽略唯一 XCI/BD/COE/MEM/手写源。

## 验收

只读检查器：`python -X utf8 -B <skill>/scripts/audit_native_layout.py <project.xpr>`。旧工程加 `--legacy` 只放宽布局要求；缺失活动输入、重复登记等正确性错误仍失败，无法确认的输入不算通过。输出 JSON，不创建/修改文件；路径/命名检查不代替 HDL、IP、GUI 和时序检查。外部库例外必须人工核实。

根 XPR 用目标版本关闭重开；核对 part/top、源集、每份源的唯一活动路径、编译顺序、IP、约束和缺失文件。不能只检查 XPR 存在。
重复执行创建应只校验兼容工程，不覆盖、不重复导入、不重置 run；已有工程不符合本布局时仅报告，不能自动迁移。
本模板的 part/top/源清单必须明确，不能使用示例器件作为默认。创建成功不等于综合/时序/硬件通过。
