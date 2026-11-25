# G20 新闻生产智能体

本项目面向新闻与传播专业学生和初入新闻行业的采编人员。团队计划把新闻采集、热点分析和选题策划接入同一套工作流程，帮助用户找到可追溯的新闻素材，并把素材和分析用于选题。

## 功能范围

- 新闻采集和公共资料库支持获取、整理和检索团队确认的媒体报道与官方通稿。
- 热点发现和议题订阅支持跟踪新闻趋势及关注议题。
- 智能问答和通稿研读围绕新闻证据提供检索、引用及分析。
- 案例库、选题工作台和分析工具包支持采编学习及选题准备。
- 用户系统提供独立账号，并隔离个人订阅、收藏、问答和选题。

具体功能、优先级和验收条件由团队继续细化。

## 当前阶段

项目处于开发准备阶段，尚未完成正式业务功能。本仓库提供基础目录、开发规范和配置模板。应用的安装、运行和测试命令待基础运行环境初始化后补充。`compose.yaml` 在确认实际服务、容器镜像和运行参数后编写。

## 技术栈

| 范围 | 技术基线 |
| --- | --- |
| 前端 | Vue 3、TypeScript、Vite、Node.js LTS、npm、Element Plus、Vue Router、Pinia、Apache ECharts |
| 后端 | Python 3.12、FastAPI、Uvicorn、Pydantic、Pydantic Settings、SQLAlchemy 2.x、Psycopg 3、Alembic、uv |
| 数据与 API | PostgreSQL、pgvector、关键词检索、向量语义检索、RAG、REST API、JSON、OpenAPI／Swagger UI |
| 采集与调度 | HTTPX、Feedparser、Trafilatura、BeautifulSoup4、按需使用的 Playwright、APScheduler、YAML 来源配置 |
| AI | 千问远程 API、统一模型调用服务 |
| 认证 | Cookie 与服务端 Session、PostgreSQL 会话存储、pwdlib 与 Argon2id、RBAC、FastAPI Depends |
| 检查与运维 | ESLint、Prettier、Vitest、Ruff、pytest、Python logging、Tenacity、GitHub Actions、Docker Compose |

开发版本、千问接入配置、部署方案及待验证范围见 [技术选型](docs/tech-stack.md)。

## 项目目录

| 路径 | 职责 |
| --- | --- |
| `frontend/src/features/` | 按产品功能组织前端业务 |
| `backend/app/modules/` | 按产品功能组织后端业务，采集与公共资料库分别维护 |
| `backend/app/shared/` | 集中维护公共 AI、数据库、检索、配置等能力 |
| `backend/app/jobs/` | 定时调度和任务入口 |
| `docs/` | 共享的设计基线、文档状态和团队协作规范 |
| `scripts/` | 按需放置项目辅助脚本 |
| `.github/` | Pull Request 模板及后续 Actions 工作流 |
| `AGENTS.md` | 三名开发人员使用 Codex 时的统一工程约束 |
| `.gitignore` 与 `.env.example` | 本地文件忽略规则和非敏感配置模板 |

各模块和容器配置的规划见 [项目目录设计](docs/project-structure.md)。

## 安全与环境变量

仓库为私有仓库。真实环境变量保存在本地 `.env` 或部署环境的密钥配置中，仓库只提交 `.env.example` 的非敏感示例。千问 API 密钥仅由后端持有。日志、真实用户数据、采集原文和上传文件按团队的数据安全与来源授权规范管理。

## 参与开发

1. 由仓库所有者邀请已确认的 GitHub 账号。接受邀请后，克隆团队的同一个仓库。
2. 阅读开发约束和任务相关设计，从最新 `main` 创建独立任务分支。 [Codex 开发规范](AGENTS.md) · [共享设计文档](docs/README.md)
3. 在授权范围内改动，运行相关检查和测试，通过任务分支发起 Pull Request。由至少一名其他成员审核后合并到 `main`。
4. 合并后删除已完成的任务分支。分支命名、提交格式和分支保护约定见 [团队协作规范](docs/collaboration.md)。

## 待确认事项

- 团队细化产品需求、模块分工、数据库结构、API 契约、`analysis` 公共分析模块及新闻来源清单。
- 验证千问平台与权限、模型 ID、费用、向量维度、中文及跨语言检索效果，并确认依赖版本和容器镜像。
- 确认学校可提供的常驻服务资源、系统规格、安装权限、Docker、数据库、公网或校园网访问条件及持久化存储。
- 明确案例库与工具包细节、文档导入导出，以及实时协作和音视频分析的范围。

## 开发计划

1. 初始化前后端运行环境，验证开发依赖、数据库、迁移、前后端通信和千问接入，再建立真实的 CI 检查。
2. 按团队细化的优先级，优先跑通 P0 的采集、分析与选题流程。
3. 在 P1 完善问答、证据引用、订阅和通稿研读等功能。按需求与资源评估 P2 功能和正式部署。

项目仓库 [czy-jpg23/g20-news-agent](https://github.com/czy-jpg23/g20-news-agent)
