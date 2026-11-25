# 团队协作规范

三名开发成员共同使用私有仓库，采用简化的 GitHub Flow。`main` 是唯一的长期稳定分支，业务变更从短期任务分支经 Pull Request 合入。

## 任务分支

| 前缀 | 用途 |
| --- | --- |
| `feature/` | 新功能 |
| `fix/` | 问题修复 |
| `docs/` | 文档更新 |
| `refactor/` | 代码结构优化 |
| `test/` | 测试补充 |
| `chore/` | 工程配置及维护 |

分支对应具体任务，名称采用 `kebab-case`，例如 `feature/news-collection`。提交使用简化的 Conventional Commits 风格，例如 `feat: add news collection module`、`docs: update project architecture` 或 `chore: initialize repository structure`。

## 开发与评审流程

1. 克隆同一个 GitHub 仓库，同步最新 `main`，创建任务分支。
2. 阅读根目录的项目说明、Codex 规范和任务设计，按授权范围开发。涉及公共模块、资料库、迁移、依赖和接口时，事先取得对应确认。
3. 运行相关本地检查和测试，提交变更并推送任务分支。
4. 发起以 `main` 为目标的 Pull Request，按模板填写任务、影响、测试结果和敏感信息检查。
5. 由至少一名其他成员审核。在可用检查通过后，优先使用 Squash Merge。合并后删除已完成的任务分支。

## 主分支规则

团队流程要求通过 Pull Request 和至少一名其他成员的审核合入 `main`，禁止直接推送、强制推送和删除 `main`。GitHub 套餐支持时，为 `main` 启用上述强制保护。仓库不具备强制保护条件时，由成员和仓库所有者按相同流程人工执行，合并人核对评审和测试记录。

## 自动化检查

基础环境跑通后，在 GitHub Actions 配置 Ruff、pytest、ESLint、TypeScript 类型检查、Vitest 及前端构建。验证各检查实际执行且状态稳定后，再将需要的检查设为 PR 合并条件。

## 成员邀请

仓库所有者取得另两位成员的 GitHub 用户名后，在仓库的协作者设置中通过 `Add people` 发送邀请。成员接受后先确认能访问仓库，再克隆并创建各自的任务分支。 [协作者设置](https://github.com/czy-jpg23/g20-news-agent/settings/access)
