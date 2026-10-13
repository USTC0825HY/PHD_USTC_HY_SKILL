# qu-ai-wei · 本地维护版

![version](https://img.shields.io/badge/version-0.8.2-local.1-blue.svg)

当前 v0.8.2-local.1。基于上游 qu-ai-wei v0.8.2，本地修订日期 2026-10-12；不是上游发布。许可证 MIT，来源：https://github.com/LifelongLazyLearner/qu-ai-wei 。

## 当前行为

按用户授权润色简体中文。默认交付终稿；仅审查只给发现；保留事实、术语、证据强度和目标语体。不会根据猜测作者身份拒绝修改，也不强制补个人经历或附打磨报告。具体执行以 SKILL.md 与按需引用为准。

技能名称和自动发现保持。通用写作、社交、品牌、学术和工程场景继续适用；本地版不自动转换繁体。现有 CLI/编辑器兼容文件仍由 scripts/build-flat.sh 生成。

## 维护与验证

不要在无 Git 源仓库的安装副本执行 update.sh；本地更新使用备份、白名单和冲突检查。保留上游来源及许可；AGENTS.md 的评审规则继续适用。

测试说明见 tests/README.md。现行行为验证保存真实输入、输出、环境和语义评审；历史 fixtures/baseline/after 保持原样，不能把其中旧门检/强制报告作为本地版本的验收要求。flat 与版本同步是结构检查，不替代行为评估。

## 本地变更

- **v0.8.2-local.1（2026-10-12）**：授权驱动的审查/润色分支，按需引用，技术内容保护；更新引用、活动测试和 flat 构建。

## 上游历史版本记录（历史行为不作为当前要求）

完整历史版本请看 [`CHANGELOG.md`](./CHANGELOG.md)。

最近更新：

- **v0.8.2（2026-07-01）**：**新增 flat-build 确定性守卫 [`tests/check-flat-sync.sh`](./tests/check-flat-sync.sh)**。把 `SKILL.md` + `references/` 拷进临时目录重新拍平,跟仓库里 commit 的 `.cursorrules` / `WARP.md` 做字节级比对 —— 抓「改了源文件忘了重跑 `build-flat.sh`」导致的 flat 文件漂移。补上 v0.8.1 评审记档的 roadmap 项(`check-version-sync.sh` 只查版本号字符串、不查 flat 正文这个盲区)。无规则变更,无行为变更。

- **v0.8.1（2026-07-01）**：**对照 [agentskills.io](https://agentskills.io) 最佳实践做评审 + 两处实质优化**（详见 [`docs/agentskills-review.md`](./docs/agentskills-review.md)）。① **frontmatter `description` 触发词优化** —— 新增 `改自然点 / 读着别扭 / 太生硬了` 三个高频触发话术(抓「能感到别扭但说不出『AI 味』」的用户),去掉跟正文重复的 `这段太 AI 了`;`暂未纳入` 改成更如实的 `不自动处理`(§2 停手门检其实接受繁體输入)。② **品牌表去重** —— 「品牌广告 vs 自媒体识别线」此前在 `SKILL.md` 和 `references/brand-voice.md` 各一份(flat build 发两遍),`SKILL.md` 改留一行指针,canonical 留 `brand-voice.md`,顺带修了「**两个**边界场景」却列 4 条的预存 bug。③ 新增 [`tests/trigger-manifest.txt`](./tests/trigger-manifest.txt) + [`tests/check-triggers.sh`](./tests/check-triggers.sh) —— 描述内容守卫(每条触发词断言锚定在 description 里),复用既有 manifest 格式,不另起 `evals/` 目录。51 条模式、冲突仲裁顺序、语体矩阵全保留。

- **v0.8.0（2026-06-18）**：**对照 [humanizer](https://github.com/blader/humanizer) 同步,补 3 条模式(全折叠进既有规则,总数仍 51)**。新增 **#19b 假坦诚开场**（`讲真 / 说实话` 当钩子 + 后接套话,判别式同时进 `SKILL.md` 必加载层防误杀真诚 `说实话`）、**#37 格言公式子模板**（`XX 是成年人的 YY`,密度 + 落点门）、**#19 伪洞察枢纽扩展**（`真正的问题是 / 核心在于 / 说到底`,口语 marker 不误杀）。修正 `whitelists.md` 的 `TBH → 说实话` 三向歧义;humanizer 规则计数去精确数。新增回归样本 `18-fake-candor-aphorism`。

- **v0.7.1（2026-05-28）**：**上下文减重,行为不变**。移除 `SKILL.md` 里的装饰性 emoji,把 H 组平台 / 文体规则 #37/#38/#49/#50 拆到 [`references/platform-patterns.md`](./references/platform-patterns.md),并让 [`scripts/build-flat.sh`](./scripts/build-flat.sh) 在 `patterns.md` 后同步拼接该文件。`SKILL.md` 从 5,390 words / 77,331 bytes 降到 4,833 words / 67,691 bytes。51 条规则、冲突仲裁顺序、简体中文-only 范围、`【门检】`、`打磨报告`、#47b 硬证据口径均保留。

- **v0.7.0（2026-05-12）**：**文档结构重整,行为不变**。新增「冲突仲裁顺序」唯一优先级树,六级仲裁覆盖 §1 不发明事实 → §6 打磨抬升,各章节散落的"优先级更高"声明统一引用。拆出 3 个新参考文件:`references/whitelists.md`(体育 / 通用技术缩写 / 人物昵称 / 护肤成分四类白名单)、`references/punctuation.md`(标点功能分工第二层)、`references/syntax.md`(10 类英式语序残留)。压缩 `避免过度修正` 反向验证(5 问 → 3 问)、`过度消毒反制` 毛边类型(5 类 → 3 类)、frontmatter description。SKILL.md 从 1259 行降到 1012 行(-20%)。51 条 AI 腔模式、9 种语体识别、6 条打磨动作、自检与打磨报告格式全保留。
- **v0.6.6（2026-04-25）**：基于 5 组当代小红书 AI 样本的诊断发现,修正 patterns.md 里"2021 年老 AI 自媒体腔基本绝迹"这条陈旧判据 —— 2025-2026 AI 小红书生成大量复用 `🆘 / 家人们谁懂啊 / 姐妹们快冲 / 宝藏 / 神器 / 不好吃回来打我` 等老模板,新老套路并存。新增规则/白名单:**#47b AI 模板占位符残留**(`XX 路 / X 号线 X 口` 单次出现即硬证据,规范为"保留 + 显式标注 + 不发明")、**#37-B info-block emoji 微模板**(`✅ 必点 / 📍 地址 / ⏰ 营业时间 / 🌟 晨间护肤`)、**身份标签 + 反向 CTA 组合**、**hashtag 尾巴平台冗余清理**、**护肤 / 美妆成分白名单**(`神经酰胺 / B5 / 氨基酸 / 皮肤屏障` 按行业标准词保留)。新增 5 条回归样本 `13-xhs-classic-templates / 14-xhs-ootd / 15-xhs-office-tips / 16-xhs-skincare / 17-xhs-home`,覆盖老模板复用、OOTD、技术信息保护、成分白名单、毒性正能量缝合五个场景。规则总数维持 51 条(#47b 是 #47 的结构性兄弟,不单独计数)。
- **v0.6.5（2026-04-24）**：扩展回归覆盖，新增 7 条样本（`06-brand-voice` / `07-academic-tech` / `08-weishendu-consulting` / `09-xhs-healing` / `10-bilibili-script` / `11-negation-stacking` / `12-table-abuse`），覆盖品牌广告、学术 / 科技、公众号伪深度、小红书伪疗愈、B 站科普、否定对举密度、表格滥用等此前缺失的语体与子语体；smoke check 加入 `KNOWN_GAPS` 机制与结构化断言（门检 / 语体 / 规则引用 / 终稿 token 保留）。本版无规则变更。
- **v0.6.4（2026-04-23）**：精简运行时 qu-ai-wei 文本里的版本历史噪音，细化 #48 对「不是 X,也不是 Y」否定对举的判据；新增 `04-negative-pairings.md` / `05-human-stop.md` 两条回归样本和 `tests/check-version-sync.sh` 自动同步检查。
- **v0.6.3（2026-04-23）**：`SKILL.md` 一致性校准（规则计数统一、门检分支更清晰、全角标点对照修正），并同步拍平到 `.cursorrules` / `WARP.md`。
- **v0.6.2（2026-04-22）**：`SKILL.md` 重构为核心 + references/ 按需加载结构，并新增拍平脚本与回归样本。
- **v0.6.1（2026-04-22）**：引入叶圣陶「写话」与《咬文嚼字》流行语刷新机制，强化 #49 的时效锚点。


写作参考与原始来源见 [references/sources.md](references/sources.md)；历史说明以 CHANGELOG.md 为准。
