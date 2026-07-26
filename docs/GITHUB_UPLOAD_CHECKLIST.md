# GitHub 发布检查表

## 首次上传前

- [ ] 仓库可见性为 **Private**。
- [ ] `validate_registry.py` 返回成功，密钥疑似项为 0。
- [ ] 没有 `.env`、凭据、私钥、Cookie、内网配置和本机绝对路径泄露。
- [ ] 没有单文件达到 GitHub 100 MB 限制。
- [ ] 未纳入 `node_modules`、虚拟环境、构建缓存和嵌套 `.git`。
- [ ] 许可证未确认的 Skill 保持 `private-only-until-reviewed`。
- [ ] `git diff --check` 通过，提交内容与预期一致。

## GitHub 设置

- 保持仓库私有，仅添加必要协作者；
- 开启 Secret Scanning、Push Protection 和 Dependabot（若账户计划支持）；
- 为 `main` 启用分支保护，后续通过 PR 合并维护变更；
- 禁止 force push 和删除受保护分支；
- 定期导出或镜像仓库，验证备份可恢复。

## 公开前的额外门槛

公开不是首次备份的必要条件。若未来需要公开，应逐 Skill 完成来源、许可证、署名、
项目保密性、个人信息和二进制资产审查；在所有未决项清零前，不切换仓库可见性。
