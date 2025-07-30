# MsPro - FastAPI 异步项目通用脚手架

MsPro 是一个基于 **FastAPI 异步框架**
的通用项目脚手架，旨在帮助开发者快速构建具备健壮架构和可扩展性的后端服务。它内置标准开发模块（CRUD、数据模型、路由、数据结构）与企业级最佳实践，让你从繁杂的基础构建中解放出来，专注于业务逻辑。

---

## ✨ 项目亮点

- 🚀 **异步架构**：基于 FastAPI 异步框架，支持高并发处理。
- 🧱 **模块化结构**：标准化目录，包含 `crud/`、`models/`、`routes/`、`schemas/` 等核心模块。
- 🔒 **JWT 鉴权体系**：内置安全的 Token 授权与用户认证机制。
- 🧬 **SQLModel 数据建模**：采用 SQLModel 统一 ORM 模型与 Pydantic Schema。
- 📦 **Pydantic V2.0 支持**：新一代数据校验体系，更快更强。
- 📊 **日志跟踪系统**：基于 Python `logging` 优化配置，便于调试和生产环境日志分析。
- ⚙️ **代码生成器**：基于模型定义，可一键生成整套 CRUD + Routes + Schemas。
- 🛠️ **管理工具脚本**：集成本地测试、开发部署、数据库初始化等一键管理命令。

---

## 📂 项目结构总览

```
MsPro/
├── alembic/                # 数据库升级/迁移
├── app/
│   ├── crud/               # CURD 操作
│   ├── models/             # SQLModel 模型定义
│   ├── routes/             # 路由入口
│   ├── schemas/            # Pydantic 数据结构
│   ├── tasks/              # 异步任务调度
│   ├── utils/              # 工具函数
│   └── main.py             # FastAPI 应用入口
├── logs/                   # 日志目录
├── module_generator.py     # 模型生成脚本
├── manage.sh               # 本地/部署环境一键控制脚本
├── .env                    # 环境变量配置
├── requirements.txt        # 依赖列表
└── README.md
```

---

## 📦 安装方式

### 方式一：通过 pip 安装并初始化项目

```bash
pip install mspro-python
mspro-init my_project
```

这将会在当前目录下生成名为 `my_project/` 的完整项目脚手架。

---

## 🔧 使用指南

1. 安装依赖：

```bash
cd my_project
python -m venv venv
./manage.sh setup
```

2. 启动开发环境：

```bash
python app/main.py
# 或使用 manage.sh 提供的一键启动脚本
./manage.sh test
```

3. 使用 `module_generator.py` 自动生成模块：

```bash
python module_generator.py User
```

4. 生产环境部署/运维：

```bash
# 在生产环境项目目录下
# 部署
./manage.sh build
# 运维
./manage.sh start/stop/restart/upgrade
```

---

## 📚 未来规划（TODO）

- 增加部署 Dockerfile 和 CI/CD 支持
- 提供 PostgreSQL、SQLite 切换配置

---

## 🧑‍💻 作者

由 [JENA] 设计与维护。欢迎提交 issue 与 PR 一起共建开源生态。

---

## 📄 License

本项目遵循 MIT License，详见 [LICENSE](LICENSE) 文件。
