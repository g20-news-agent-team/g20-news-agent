# 项目目录设计

项目根目录为 `g20-news-agent`。前端和后端各自按产品功能组织，公共能力集中复用。以下以《G20 新闻生产智能体项目根目录设计 V1.0》为根目录依据，模块内部文件在实际开发时按需建立。

## 根目录

| 路径 | 作用 |
| --- | --- |
| `frontend/` | Vue 3 前端，核心代码位于 `frontend/src/` |
| `backend/` | FastAPI 后端，核心代码位于 `backend/app/` |
| `docs/` | 共享的需求、技术栈、架构、数据库、API 和协作设计 |
| `scripts/` | 按需加入的环境初始化、测试数据和维护脚本 |
| `.github/` | Pull Request 模板和后续 Actions 工作流 |
| `README.md` | 项目说明、环境状态和参与方式 |
| `AGENTS.md` | 统一的 Codex 开发约束 |
| `.gitignore` | 忽略密钥、缓存、构建产物和本地运行数据 |
| `.env.example` | 环境变量模板 |
| `compose.yaml` | 计划提供的容器编排，待服务及容器环境验证后创建 |

## 前端

`frontend/src/features/` 按功能划分，规划包含以下目录。

| 目录 | 职责 |
| --- | --- |
| `home/` | 产品首页 |
| `hotspots/` | 热点发现 |
| `subscriptions/` | 议题订阅 |
| `qa/` | 智能问答 |
| `documents/` | 通稿研读 |
| `cases/` | 案例库 |
| `workspace/` | 选题工作台 |
| `toolbox/` | 分析工具包 |
| `auth/` | 用户系统 |

`src/` 下规划通用的 `components/`、`layouts/`、`router/`、`stores/`、`api/`、`assets/`、`styles/`、`utils/` 和 `types/`。功能目录内部可按需放置 `pages/`、`components/`、`api/`、`stores/`、`composables/`、`tests/`、`types.ts` 和 `routes.ts`。

## 后端

`backend/app/modules/` 按功能划分，规划包含以下目录。

| 目录 | 职责 |
| --- | --- |
| `collection/` | 获取、解析及清洗新闻，维护采集适配 |
| `corpus/` | 管理公共新闻、官方通稿、来源、分段及索引 |
| `hotspots/` | 热点发现与新闻价值分析 |
| `subscriptions/` | 议题订阅 |
| `qa/` | 智能问答 |
| `documents/` | 通稿研读 |
| `cases/` | 案例库 |
| `workspace/` | 选题工作台 |
| `toolbox/` | 分析工具包 |
| `auth/` | 用户认证与账号管理 |

模块内按需使用 `router.py` 承载 API、`service.py` 承载业务、`repository.py` 承载读写、`models.py` 定义模型、`schemas.py` 定义传输格式、`prompts.py` 保存专用提示词、`constants.py` 保存业务常量，并在需要 Python 包时创建 `__init__.py`。

- `backend/app/shared/` 承载公共 AI、连接和会话、检索、配置、异常、日志和安全能力。按需建立 `ai/`、`db/`、`retrieval/`，存储方案确认后再建立 `storage/`。
- `backend/app/jobs/` 承载后台任务入口和调度，调用相应业务模块。
- `backend/alembic/`、`backend/config/` 和 `backend/tests/` 在实际建立迁移、非敏感配置和测试时加入。

公共 `analysis/` 模块待团队结合功能需求决定。Git 骨架仅为已有明确分工的基础目录保留少量 `.gitkeep`，各业务目录随实现加入。
