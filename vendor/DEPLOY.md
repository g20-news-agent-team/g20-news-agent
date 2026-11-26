# G20 整站部署

在装有 Docker Compose 和 Node.js 24.22.1 或更新版本的部署机，克隆团队仓库并切到包含最新信源配置的分支。以下命令从仓库根目录运行：

```bash
bash vendor/deploy-aihot.sh
```

首次运行在 `~/.local/share/g20-aihot/app/.env` 生成配置。填写模型服务的 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`，然后再次运行。可用 `G20_AIHOT_STATE_DIR` 指定安装路径。启动后访问服务器的 3000 端口，后台路径是 `/admin`，管理员密码在部署机的 `.env`。数据库和内容由名为 `g20-aihot` 的 Compose 项目持久化。

首次启动会导入[`g20-sources.json`](g20-sources.json) 中的 14 个正式信源并由 AIHOT worker 按 60 或 120 分钟基础间隔持续调度。已有同 ID 信源会保留后台设置。更新已有部署时，在后台停用清单中已移除的信源，并对照新清单同步已有 ID 的地址、采集类型和规则。栏目和 RSS 入口可能包含非 G20 新闻，精选规则仍沿用上游，需要另行校准。

## 实际验收状态

新版 14 条配置已完成静态检查。部署环境仍需逐站验证列表、正文、发布时间和 RSS 条目，在后台查看试抓结果和失败原因。
