# G20 整站部署

在装有 Docker Compose 和 Node.js 24.22.1 或更新版本的部署机，克隆团队仓库并切到 `feat/g20-sample-pipeline`。以下命令从仓库根目录运行：

```bash
bash vendor/deploy-aihot.sh
```

首次运行在 `~/.local/share/g20-aihot/app/.env` 生成配置。填写模型服务的 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`，然后再次运行。可用 `G20_AIHOT_STATE_DIR` 指定安装路径。启动后访问服务器的 3000 端口，后台路径是 `/admin`，管理员密码在部署机的 `.env`。数据库和内容由名为 `g20-aihot` 的 Compose 项目持久化。

首次启动会导入表中的 18 个信源并由 AIHOT worker 按 60 或 120 分钟基础间隔持续调度。已有同 ID 信源保留后台设置。栏目和 RSS 入口可能包含非 G20 新闻，精选规则仍沿用上游，需要另行校准。

## 实际验收状态

部署入口和 18 条配置已做静态校验。当前环境没有 Docker，尚未启动整站。信源表中的 8 个原始地址本次返回 403、404 或空响应；央广网 RSS 地址虽返回 200，内容是错误网页。新华网和中新网实际返回 RSS。网页选择器仍需在部署环境逐站验证，后台可查看试抓和失败原因。
