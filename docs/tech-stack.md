# 技术选型

本文件整理《G20 新闻生产智能体技术选型方案 V2.1》的开发基线及待验证事项。依赖小版本与配置参数在基础运行环境验证后锁定。

## 前端

| 层次 | 基线 |
| --- | --- |
| 开发语言与框架 | TypeScript、Vue 3 |
| 构建与依赖 | Vite、Node.js LTS、npm，纳入 `package-lock.json` |
| 界面与路由 | Element Plus、Vue Router |
| 共享状态与图表 | Pinia、Apache ECharts |
| 检查与测试 | ESLint、Prettier、Vitest |

## 后端和数据库

| 层次 | 基线 |
| --- | --- |
| 运行与依赖 | Python 3.12、uv，纳入 `pyproject.toml` 与 `uv.lock` |
| HTTP 服务 | FastAPI、Uvicorn、REST API、JSON、OpenAPI／Swagger UI |
| 数据校验与配置 | Pydantic、Pydantic Settings，使用本地 `.env` 与版本化的 `.env.example` |
| 存储与迁移 | PostgreSQL、Psycopg 3、SQLAlchemy 2.x、Alembic |
| 检索 | 关键词检索、pgvector 向量语义检索、RAG |
| 工程基础 | Python logging、FastAPI Exception Handler、Tenacity、Ruff、pytest 与 HTTPX |

使用 Alembic 同步各成员的本地数据库结构。验证中文及跨语言检索效果后再确定文本处理和索引策略。重试需限制次数并考虑重复写入和模型计费，日志需避免记录密钥及用户隐私。

## 新闻采集和调度

团队通过 YAML 配置来源、采集方式与频率。依次评估官方 API、RSS、普通网页和必要的动态网页，结合 HTTPX、Feedparser、Trafilatura、BeautifulSoup4 与按需使用的 Playwright。APScheduler 负责定时调度，业务逻辑由相应模块提供。

逐站确认访问权限、使用条款、版权、`robots.txt` 和频率限制。全文留存许可不足时，仅保存允许使用的元数据和链接。

## AI 与证据

生成和向量能力由统一的千问远程调用模块提供。调用模块管理连接配置、结构化输出、重试、异常和用量。业务模块保留各自的提示词及专项分析。RAG 问答检索真实证据，核验引用、原句和出处，并在证据不足时明确提示。

| 待验证项 | 推荐初始配置 |
| --- | --- |
| 接入 | 阿里云百炼的 OpenAI 兼容 API 与 OpenAI Python SDK |
| 轻量模型 | `qwen-flash`，用于初筛、分类、摘要和关键词 |
| 主力模型 | `qwen-plus`，用于新闻价值分析、问答和选题 |
| 向量模型 | `text-embedding-v4`，推荐先验证 1024 维及中英文效果 |

锁定模型配置前，确认实际 API 平台、权限、费用、模型 ID、参数与向量维度。Codex 开发额度与产品 API 费用分别管理。

## 用户系统与运行

- 独立账号使用 Cookie 与服务端 Session，由 FastAPI 校验，Session 存入 PostgreSQL。密码使用 pwdlib 与 Argon2id，业务接口通过 RBAC 和 FastAPI Depends 校验权限。
- 上线前验证 HTTPS、安全 Cookie、CSRF 防护、登录限流、会话过期和撤销。
- 使用 Git、GitHub 和 GitHub Actions 协作。Docker Compose 统一基础运行环境。Uvicorn 与 Nginx 是正式部署的推荐组合，学校服务资源、网络和存储条件有待验证。

## 后续选型

多人实时协作、音视频分析属于 P2。实时协作方案可在需求明确后评估 Tiptap、Yjs、WebSocket、Yjs Awareness 和 Hocuspocus。文档导入导出按所需格式评估，文件存储等待服务器资源确认。确认持久化路径、配额和权限后，再评估本地文件存储与统一存储接口。

现阶段维持模块化单体和 PostgreSQL 基线。额外消息中间件、缓存服务、独立搜索或向量基础设施、本地大模型及其他 AI 编排框架的引入须由团队结合实际需求评估。
