# CiliAI短剧平台 - 项目结构整理

## 一、项目整体结构

```
d:\ciliAI\                          # 项目根目录
│
├── ciliAI\                          # 用户应用端（主应用）
│   ├── src\                           # Vue前端源码
│   ├── public\                        # 静态资源
│   ├── dist\                         # 生产构建产物
│   ├── templates\                     # Flask模板目录
│   ├── venv\                          # Python虚拟环境
│   ├── app.py                         # Flask后端主应用
│   ├── requirements.txt               # Python依赖
│   ├── package.json                   # Node依赖
│   ├── vite.config.js                 # Vite配置
│   ├── .env                          # 环境变量
│   ├── Dockerfile                     # Docker配置
│   ├── docker-compose.yml            # Docker编排
│   ├── start.bat                      # Windows启动脚本
│   ├── deploy.sh                     # Linux部署脚本
│   └── ciliAI.db                   # SQLite数据库
│
├── ruoyi\                            # 管理后台端
│   ├── src\                          # Vue前端源码
│   ├── templates\                    # HTML模板
│   ├── uploads\                      # 上传文件目录
│   ├── app.py                        # Flask后端API
│   ├── package.json                  # Node依赖
│   ├── vite.config.js                # Vite配置
│   ├── index.html                    # 入口HTML
│   └── Dockerfile                    # Docker配置
│
├── *.md                              # 文档文件
├── *.py                              # 辅助脚本
└── test_*.py                         # 测试脚本
```

---

## 二、用户应用端详细结构

### 2.1 目录树

```
ciliAI\
│
├── src\                              # Vue前端源码目录
│   ├── components\                    # 可复用组件
│   │   ├── CreateProjectModal.vue    # 创建项目弹窗
│   │   │   功能：创建新的AI项目
│   │   │   依赖：Element Plus对话框
│   │   │
│   │   ├── LoginModal.vue            # 登录弹窗
│   │   │   功能：8位邀请码登录验证
│   │   │   依赖：API验证接口
│   │   │
│   │   ├── NovelDetailModal.vue      # 小说详情弹窗
│   │   │   功能：展示小说/项目详情
│   │   │
│   │   └── ProjectManager.vue        # 项目管理
│   │       功能：项目列表、删除、重命名
│   │
│   ├── views\                        # 页面视图
│   │   ├── Home.vue                  # 首页
│   │   │   路由：/
│   │   │   功能：平台介绍、开始创作
│   │   │
│   │   ├── Task.vue                  # 任务页面
│   │   │   路由：/task
│   │   │   功能：AI图像生成任务
│   │   │
│   │   ├── ProjectDetail.vue         # 项目详情
│   │   │   路由：/project/:id
│   │   │   功能：项目详情、生成记录
│   │   │
│   │   ├── Works.vue                 # 作品展示
│   │   │   路由：/works
│   │   │   功能：社区作品展示
│   │   │
│   │   ├── Order.vue                 # 订单页面
│   │   │   路由：/order
│   │   │   功能：算力消耗记录
│   │   │
│   │   └── Profile.vue               # 个人中心
│   │       路由：/profile
│   │       功能：用户信息、算力余额
│   │
│   ├── router\                       # 路由配置
│   │   └── index.js                  # 路由定义
│   │
│   ├── styles\                       # 样式目录
│   │   └── global.css               # 全局样式
│   │
│   ├── utils\                        # 工具函数
│   │   └── volcengine.js            # 火山引擎SDK
│   │
│   ├── routes\                       # API路由（前端）
│   │   └── api\
│   │       └── verify-invite-code.js
│   │
│   ├── App.vue                      # Vue根组件
│   └── main.js                      # Vue入口
│
├── public\                           # 静态资源
│   ├── ads\                         # 广告图片
│   │   ├── ad1.png
│   │   ├── ad2.png
│   │   └── ad3.png
│   └── logo-C5RxjwAw.png            # Logo
│
├── dist\                             # 生产构建产物
│   ├── index.html
│   ├── assets\
│   ├── ads\
│   └── logo.png
│
├── templates\                        # Flask模板（开发模式）
│
├── venv\                             # Python虚拟环境
│   ├── Scripts\                      # 可执行脚本
│   ├── Lib\                          # Python库
│   └── python.exe
│
├── 说明\                             # 产品文档
│   ├── 1544714_即梦AI图像生成计费说明.md
│   ├── 1544715_即梦AI视频生成计费说明.md
│   ├── 1544716_产品简介.md
│   ├── 1616429_即梦文生图3.0-接口文档.md
│   └── ...（20+个接口文档）
│
├── app.py                            # 【核心】Flask主应用
│   功能：API服务、数据管理、AI调用
│   端口：5001
│
├── debug_api.py                     # API调试
├── debug_start.py                   # 调试启动
│
├── index.html                       # 入口HTML
│
├── package.json                     # npm依赖
│   依赖：vue@3.5.13, vite@6.0.5, element-plus@2.8.4
│
├── vite.config.js                   # Vite配置
│   端口：3000
│   代理：/api -> localhost:5001
│
├── requirements.txt                 # Python依赖
│   flask, flask-cors, python-dotenv, volcengine, requests
│
├── .env                            # 【重要】环境变量
│   VOLC_AK, VOLC_SK
│
├── .env.example                     # 环境变量示例
│
├── Dockerfile                       # Docker配置
├── docker-compose.yml               # Docker编排
├── deploy.sh                        # Linux部署脚本
├── start.bat                       # Windows启动脚本
│
└── ciliAI.db                     # 【重要】SQLite数据库
    表：users, projects, generation_records,
        chat_messages, compute_power_logs, invite_codes, ip_works
```

### 2.2 核心文件说明

| 文件 | 类型 | 功能 | 重要性 |
|-----|------|------|-------|
| `app.py` | Python | Flask后端API主应用 | ★★★★★ |
| `ciliAI.db` | SQLite | 数据库文件 | ★★★★★ |
| `.env` | 配置 | API密钥配置 | ★★★★★ |
| `requirements.txt` | 依赖 | Python依赖清单 | ★★★★ |
| `package.json` | 依赖 | Node依赖清单 | ★★★★ |
| `vite.config.js` | 配置 | 前端构建配置 | ★★★ |
| `start.bat` | 脚本 | Windows启动 | ★★★ |

---

## 三、管理后台端详细结构

### 3.1 目录树

```
ruoyi\
│
├── src\                              # Vue前端源码
│   ├── api\                          # API调用封装
│   │   └── admin.js                 # 管理员API
│   │
│   ├── router\                       # 路由配置
│   │   └── index.js                  # 路由定义
│   │
│   ├── views\                        # 页面视图
│   │   ├── Dashboard.vue            # 仪表盘
│   │   │   路由：/dashboard
│   │   │   功能：系统统计
│   │   │
│   │   ├── Login.vue               # 登录页
│   │   │   路由：/login
│   │   │   凭证：admin/admin123
│   │   │
│   │   ├── InviteCodes.vue        # 邀请码管理
│   │   │   路由：/invite-codes
│   │   │   功能：CRUD邀请码
│   │   │
│   │   ├── Users.vue              # 用户管理
│   │   │   路由：/users
│   │   │   功能：用户列表、统计
│   │   │
│   │   ├── Works.vue             # 作品管理
│   │   │   路由：/works
│   │   │   功能：IP作品管理
│   │   │
│   │   └── Layout.vue             # 布局组件
│   │
│   ├── App.vue                    # Vue根组件
│   └── main.js                    # Vue入口
│
├── templates\                      # HTML模板
│   └── index.html
│
├── uploads\                        # 上传文件目录
│   └── .gitkeep
│
├── app.py                          # 【核心】Flask后端API
│   功能：管理员API、邀请码管理、作品管理
│   端口：5002
│
├── index.html                     # 入口HTML
│
├── package.json                   # npm依赖
│   依赖：vue@3.4.21, vite@5.1.6, element-plus@2.6.1
│
├── vite.config.js                 # Vite配置
│   端口：3001
│   代理：/api -> localhost:5002
│
└── Dockerfile                     # Docker配置
```

### 3.2 核心文件说明

| 文件 | 类型 | 功能 | 重要性 |
|-----|------|------|-------|
| `app.py` | Python | Flask后端API | ★★★★★ |
| `src/api/admin.js` | JavaScript | API封装 | ★★★★ |
| `src/views/*.vue` | Vue组件 | 管理页面 | ★★★ |
| `vite.config.js` | 配置 | 代理配置 | ★★★ |

---

## 四、数据库结构

### 4.1 数据库文件

- **位置**：`ciliAI/ciliAI.db`
- **类型**：SQLite 3
- **初始化**：首次启动自动创建

### 4.2 数据表清单

| 表名 | 说明 | 主键 | 记录数估算 |
|-----|------|------|-----------|
| `users` | 用户表 | id | 根据用户数 |
| `projects` | 项目表 | id | 根据项目数 |
| `generation_records` | 生成记录 | id | 较大 |
| `chat_messages` | 聊天消息 | id | 中等 |
| `compute_power_logs` | 算力日志 | id | 较大 |
| `invite_codes` | 邀请码表 | id | 较小 |
| `ip_works` | IP作品表 | id | 较小 |

### 4.3 ER关系图

```
┌──────────────┐       ┌──────────────────┐
│ invite_codes │       │      users       │
│──────────────│       │──────────────────│
│ id (PK)     │       │ id (PK)         │
│ code        │──────▶│ invite_code (UK)│
│ status      │       │ compute_power   │
│ compute_power│      │ total_power_used│
│ ...         │       │ ...             │
└──────────────┘       └────────┬─────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│    projects      │  │generation_records│  │  chat_messages  │
│──────────────────│  │──────────────────│  │──────────────────│
│ id (PK)         │  │ id (PK)         │  │ id (PK)         │
│ user_id (FK)    │  │ user_id (FK)    │  │ user_id (FK)    │
│ title           │  │ project_id (FK) │  │ project_id (FK) │
│ ...             │  │ type            │  │ chat_id         │
└──────────────────┘  │ ...             │  │ role            │
                       └──────────────────┘  │ ...             │
                                              └──────────────────┘
```

---

## 五、辅助文件和脚本

### 5.1 根目录文件

| 文件 | 说明 |
|-----|------|
| `DEPLOYMENT_GUIDE.md` | 部署指南（原始） |
| `DEPLOYMENT_GUIDE_v2.md` | 部署指南（详细版） |
| `STARTUP_GUIDE.md` | 启动说明书（新建） |
| `PROJECT_STRUCTURE.md` | 项目结构整理（新建） |
| `DIAGNOSTIC_REPORT.md` | 诊断报告 |
| `INTEGRATION_REPORT.md` | 集成报告 |

### 5.2 辅助脚本

| 文件 | 用途 |
|-----|------|
| `add_ip_works.py` | 添加IP作品 |
| `check_works.py` | 检查作品 |
| `fix_project_detail.py` | 修复项目详情 |
| `update_works_category.py` | 更新作品分类 |
| `verify_works.py` | 验证作品 |
| `test_body.json` | 测试数据 |
| `test_flask.py` | Flask测试 |
| `test_flask2.py` | Flask测试2 |

---

## 六、技术栈总结

### 6.1 后端技术栈

| 技术 | 版本 | 用途 |
|-----|------|------|
| **Python** | 3.9+ | 编程语言 |
| **Flask** | 最新 | Web框架 |
| **Flask-CORS** | 最新 | 跨域支持 |
| **python-dotenv** | 最新 | 环境变量 |
| **volcengine** | 最新 | 火山引擎SDK |
| **SQLite** | 3.x | 数据库 |

### 6.2 前端技术栈

| 技术 | 版本 | 用途 |
|-----|------|------|
| **Vue.js** | 3.5.13 | 前端框架 |
| **Vue Router** | 4.4.5 | 路由管理 |
| **Element Plus** | 2.8.4 | UI组件库 |
| **Axios** | 1.7.9 | HTTP客户端 |
| **Vite** | 6.0.5 | 构建工具 |

### 6.3 管理后台技术栈

| 技术 | 版本 | 用途 |
|-----|------|------|
| **Vue.js** | 3.4.21 | 前端框架 |
| **Pinia** | 2.1.7 | 状态管理 |
| **Element Plus** | 2.6.1 | UI组件库 |
| **Vite** | 5.1.6 | 构建工具 |

---

## 七、部署相关文件

### 7.1 Docker配置

| 文件 | 位置 | 用途 |
|-----|------|------|
| `Dockerfile` | ciliAI/ | 用户应用Docker配置 |
| `docker-compose.yml` | ciliAI/ | Docker编排配置 |

### 7.2 部署脚本

| 文件 | 位置 | 用途 |
|-----|------|------|
| `start.bat` | ciliAI/ | Windows一键启动 |
| `deploy.sh` | ciliAI/ | Linux部署脚本 |

---

## 八、环境配置

### 8.1 环境变量

**文件**：`ciliAI/.env`

```bash
# 火山引擎密钥
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey
```

### 8.2 端口配置

| 服务 | 端口 | 配置文件 |
|-----|------|---------|
| 用户应用后端 | 5001 | ciliAI/app.py |
| 管理后台后端 | 5002 | ruoyi/app.py |
| 管理后台前端 | 3001 | ruoyi/vite.config.js |

---

**文档版本**：1.0  
**最后更新**：2026-04-12


