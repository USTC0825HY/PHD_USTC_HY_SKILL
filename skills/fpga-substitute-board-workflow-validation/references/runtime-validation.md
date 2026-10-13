# 脚本运行时发现

先发现已安装解释器，再用其绝对路径探测版本与任务所需导入。优先复用 `<CODEX_HOME>/tools/laser-fpga-runtime/.venv/Scripts/python.exe`，其可启动不代表每个科学计算库齐全。当前任务必须重新验证，不能沿用“环境已损坏”的历史结论，也不能仅凭文件存在断定可用。

使用 `& <verified-python> -B -c "import sys; print(sys.version); assert sys.version_info >= (3,10); import <required-modules>"`（将模块占位替换为真实导入）。DOCX 检查需要 docx/lxml；图像检查需要 PIL；MAT 严格检查需要 scipy，v7.3 还需专门的 HDF5/MATLAB 验证；PDF 渲染按实际工具验证。若专用环境缺库，可发现并探测已安装的其他解释器，不向专用环境混入别处 site-packages。

不直接调用未经验证的裸 python，不自动重建环境或安装依赖。缺失依赖记录为未运行/未验证，不能输出完整通过。脚本中的 python 示例表示已验证解释器占位。临时验证材料遵守工作区 .codex_work 任务目录规则。
