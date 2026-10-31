# 维护手册：网站访问排查与发布流程

> 从 README 移出的运维说明。返回 [README](../README.md)。

## 网站打不开怎么办

**第一步：** 打开 [站点入口](https://aipmandy.github.io/chinese-x-creators/)；如果仍打不开，先用 [GitHub 上的首页 HTML](index.html) 与 [关于项目](about.html) 查看内容（GitHub 的源码预览不会渲染成完整网站）。

**第二步：** 打开 [Pages 设置](https://github.com/AIPMAndy/chinese-x-creators/settings/pages)，将 **Build and deployment → Source** 选为 **GitHub Actions**。本项目自带 `.github/workflows/deploy-pages.yml`，会验证、构建并自动部署，也可以在 [Actions](https://github.com/AIPMAndy/chinese-x-creators/actions/workflows/deploy-pages.yml) 手动重跑。

**第三步：** 在 [Actions](https://github.com/AIPMAndy/chinese-x-creators/actions) 查看最近一次 **Deploy Pages** 是否成功。若失败，先查看日志，再检查仓库 Pages 设置。GitHub Pages 可能受到所在网络访问限制；源码和 CSV 可以直接通过 GitHub 仓库阅读。

## 如何发布 GitHub 仓库

这是一个**独立开源仓库**，不覆盖已有的 `x-income-handbook`。

如果你已安装 [GitHub CLI](https://cli.github.com/) 并登录 `AIPMAndy` 账号，在项目根目录执行：

```bash
bash scripts/publish.sh
```

脚本会创建（或使用）`AIPMAndy/chinese-x-creators` 并推送源码。仓库现在使用 GitHub Actions 自动部署网站；请在 `Settings → Pages` 选择 `GitHub Actions` 为发布源，工作流会在推送到 `main` 后运行。站点将在 Pages 成功部署后位于：

`https://aipmandy.github.io/chinese-x-creators/`

**不要在发布前将这个网址当成已上线网站。**
