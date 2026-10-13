---
name: qu-ai-wei
description: "润色简体中文中空泛、重复或生硬的表达，保留事实、术语和目标语体。用于显式 /qu-ai-wei 或去 AI 味、去ai味、改得说人话、改自然点、读着别扭、太生硬了或 humanize 中文；仅审查时只给发现，不自动改稿。不按文风判断作者身份，不自动转换繁体。"
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
metadata:
  version: "0.8.2-local.1"
  compatibility: "cursor claude-code codex opencode kiro factory slate hermes"
---

# 中文表达润色

改善用户指定文本的表达，保留它要传达的事实、语气和用途。不要为了“像真人”增加内容，也不要把风格偏好当作错误。

## 先确定本次授权

| 用户要求 | 执行方式 |
|---|---|
| 仅检查、仅审查、指出问题 | 给出具体问题及理由，不改文件、不输出整篇替换稿。 |
| 润色、去 AI 味、直接改写 | 在已授权范围内改写，默认直接交付终稿。 |
| 仅改某段、保留某句、只改注释 | 只改指定范围，其余保持原样。 |
| 修改说明、前后对照、打磨报告 | 按要求补充简短说明，引用真实改动，不虚构次数。 |

不从文字特征猜测真人/AI 作者身份并据此停手。用户已授权润色时，保留值得保留的个人表达，同时完成所要求的修改。不要要求用户再确认一次已说明的目标；只有缺失信息会实质改变意思或交付场景时才澄清。

没有文本或明确文件时，先取得待处理内容。繁体、翻译和纯新写作不是本技能的默认范围，不自动转换文字体系；用户明确要求的任务按其范围另行处理。

## 修改时保持的内容

- 事实、数字、单位、日期、版本、人物和对象准确；保留限制条件、否定、因果与证据强度。不能把“推测”“待验证”润色成“已证实”。
- 技术术语、变量、命令、型号和接口名称按任务保留。不得凭润色改技术结论；疑似事实错误单独指出，不能静默补造。
- 引语与作者声音按授权保护。没有要求改引语时保持其原文；语体跟随用途，不把学术报告改成聊天口吻，也不把个人叙述统一改成公文。
- 原文已有且适合场景的具体感受、犹疑或个人判断可以保留；没有这类内容时，不强制补“毛边”、第一人称、经历或观点。给虚构内容加“请核对”不构成许可。
- 词频、句长、连接词和弱动词比例只是检查线索，不是作者身份检测器，也不是必须达标的阈值。逐句判断有没有空转、重复或歧义；有效表达可以不改。
- 用户只要压缩、摘要或改变语体时，按其目标取舍，仍不改变关键事实和论点；不要把“保持原文”变成拒绝已授权编辑的理由。

## 按任务读取参考

普通短文只需本入口；发现具体问题后再读有关章节，不全量加载参考：

- 文体或工程边界拿不准：[references/editing-modes.md](references/editing-modes.md)。
- 需要核对空泛、重复、修辞或句式：[references/patterns.md](references/patterns.md)；平台文案另读 [references/platform-patterns.md](references/platform-patterns.md)。其中历史频率、年份和阈值是经验线索，不是当前统计事实。
- 品牌短句与宣传文案：[references/brand-voice.md](references/brand-voice.md)。
- 术语保护、标点或语序：[references/whitelists.md](references/whitelists.md)、[references/punctuation.md](references/punctuation.md)、[references/syntax.md](references/syntax.md)，只选需要的一份。
- 需要输出对照示例：[references/examples.md](references/examples.md)；需要风格参考或依据：[references/reference-models.md](references/reference-models.md)、[references/sources.md](references/sources.md)。

## 交付前复核

对照输入检查：该改的冗余或歧义是否解决，事实/数字/条件是否保留，语体是否合适，授权外内容是否保持。代码场景只改指定注释或说明，不触碰可执行语句、信号名、端口或时序含义。

内部自检不要求展示逐步思考。默认输出终稿，不附作者身份判断、初稿、自审记录或打磨报告。若存在会影响理解的真实歧义，简短指出；不要为了凑“人味”编补信息。
