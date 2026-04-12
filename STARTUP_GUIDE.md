# CiliAI短剧平台 - 项目启动说明书

## 文档信息

- **项目名称**：CiliAI短剧平台
- **版本**：0.0.6
- **编写日期**：2026-04-12
- **文档用途**：项目启动与配置指南

---

## 目录

1. [项目整体架构](#1-项目整体架构)
2. [用户应用端启动说明](#2-用户应用端启动说明)
3. [管理后台端启动说明](#3-管理后台端启动说明)
4. [数据库配置与初始化](#4-数据库配置与初始化)
5. [后端服务启动说明](#5-后端服务启动说明)
6. [启动顺序与验证方法](#6-启动顺序与验证方法)
7. [常见启动问题解决](#7-常见启动问题解决)

---

## 1. 项目整体架构

### 1.1 项目组成

CiliAI短剧平台由以下四大组件构成：

| 组件名称 | 类型 | 端口 | 功能描述 |
|---------|------|------|---------|
| **用户应用端** | 前端+后端 | 5001 | 主应用，用户进行AI图像生成和管理项目 |
| **管理后台端** | 前端+后端 | 5002(后端)/3001(前端) | 管理员管理邀请码、用户和作品 |
| **SQLite数据库** | 数据存储 | - | 存储所有业务数据 |
| **火山引擎AI服务** | 外部服务 | - | 提供AI图像生成能力 |

### 1.2 技术架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        火山引擎AI服务                         │
│                    (外部依赖 - Visual API)                   │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                      CiliAI短剧平台                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  用户应用端 (ciliAI/)               │   │
│  │  ┌──────────────┐    ┌──────────────────────────┐  │   │
│  │  │  Vue.js 3.5  │    │      Flask API          │  │   │
│  │  │  Element Plus │    │      (端口: 5001)        │  │   │
│  │  │  Vite 6.0     │    │  ┌──────────────┐       │  │   │
│  │  └──────────────┘    │  │   SQLite DB  │       │  │   │
│  │         │             │  │ ciliAI.db │       │  │   │
│  │         └────────────▶│  └──────────────┘       │  │   │
│  │                       └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                管理后台端 (ruoyi/)                  │   │
│  │  ┌──────────────┐    ┌──────────────────────────┐  │   │
│  │  │  Vue.js 3.4  │    │      Flask API          │  │   │
│  │  │  Pinia       │    │      (端口: 5002)        │  │   │
│  │  │  Vite 5.1    │    │  ┌──────────────┐       │  │   │
│  │  └──────┬───────┘    │  │   SQLite DB  │       │  │   │
│  │         │             │  │ ciliAI.db │       │  │   │
│  │         └────────────▶│  └──────────────┘       │  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 目录结构总览

```
d:\ciliAI\
│
├── ciliAI\                          # 用户应用端（主应用）
│   ├── src\                           # Vue前端源码
│   │   ├── components\                # 可复用组件
│   │   ├── views\                     # 页面视图
│   │   ├── router\                    # 路由配置
│   │   ├── styles\                    # 全局样式
│   │   ├── utils\                     # 工具函数
│   │   ├── App.vue                    # 根组件
│   │   └── main.js                    # 入口文件
│   ├── public\                        # 静态资源
│   ├── dist\                          # 生产构建产物
│   ├── app.py                         # Flask后端入口（端口5001）
│   ├── requirements.txt               # Python依赖
│   ├── package.json                   # Node依赖
│   ├── vite.config.js                 # Vite配置
│   ├── .env                          # 环境变量配置
│   └── ciliAI.db                   # SQLite数据库文件
│
├── ruoyi\                            # 管理后台端
│   ├── src\                           # Vue前端源码
│   │   ├── api\                       # API调用封装
│   │   ├── router\                    # 路由配置
│   │   ├── views\                     # 页面视图
│   │   ├── App.vue                    # 根组件
│   │   └── main.js                    # 入口文件
│   ├── templates\                     # HTML模板
│   ├── app.py                         # Flask后端入口（端口5002）
│   ├── package.json                   # Node依赖
│   ├── vite.config.js                 # Vite配置（代理5002）
│   └── uploads\                       # 上传文件目录
│
└── *.py                              # 辅助脚本
```

---

## 2. 用户应用端启动说明

### 2.1 目录结构详解

```
ciliAI\                              # 用户应用端根目录
│
├── src\                              # Vue前端源码目录
│   ├── components\                   # Vue组件目录
│   │   ├── CreateProjectModal.vue    # 创建项目弹窗组件
│   │   │   功能：创建新的AI项目
│   │   │   依赖：Element Plus对话框组件
│   │   │
│   │   ├── LoginModal.vue            # 登录弹窗组件
│   │   │   功能：8位邀请码登录验证
│   │   │   依赖：API验证接口
│   │   │
│   │   ├── NovelDetailModal.vue      # 小说详情弹窗
│   │   │   功能：展示小说/项目详情
│   │   │   依赖：项目数据
│   │   │
│   │   └── ProjectManager.vue        # 项目管理组件
│   │       功能：项目列表、删除、重命名
│   │       依赖：项目API
│   │
│   ├── views\                        # 页面视图目录
│   │   ├── Home.vue                  # 首页
│   │   │   功能：平台介绍、开始创作入口
│   │   │   路由：/
│   │   │
│   │   ├── Task.vue                  # 任务页面
│   │   │   功能：AI图像生成任务创建
│   │   │   路由：/task
│   │   │   依赖：火山引擎Visual API
│   │   │
│   │   ├── ProjectDetail.vue         # 项目详情页
│   │   │   功能：查看和管理单个项目
│   │   │   路由：/project/:id
│   │   │   显示：生成记录、聊天记录
│   │   │
│   │   ├── Works.vue                 # 作品展示页
│   │   │   功能：社区作品展示
│   │   │   路由：/works
│   │   │   数据：IP_works表
│   │   │
│   │   ├── Order.vue                 # 订单页面
│   │   │   功能：查看算力消耗记录
│   │   │   路由：/order
│   │   │
│   │   └── Profile.vue               # 个人中心
│   │       功能：用户信息、算力余额
│   │       路由：/profile
│   │
│   ├── router\                       # 路由配置目录
│   │   └── index.js                  # 路由定义文件
│   │       配置：Vue Router路由规则
│   │       守卫：登录状态验证
│   │
│   ├── styles\                       # 样式目录
│   │   └── global.css               # 全局样式文件
│   │
│   ├── utils\                        # 工具函数目录
│   │   └── volcengine.js            # 火山引擎SDK封装
│   │
│   ├── App.vue                      # Vue根组件
│   │   功能：全局布局、导航栏
│   │
│   └── main.js                      # Vue应用入口
│       功能：创建Vue应用、注册插件
│       依赖：Vue Router, Element Plus, Axios
│
├── public\                           # 静态资源目录
│   ├── ads\                          # 广告图片目录
│   │   ├── ad1.png
│   │   ├── ad2.png
│   │   └── ad3.png
│   └── logo-C5RxjwAw.png            # 平台Logo
│
├── dist\                             # 生产构建产物目录
│   ├── index.html                    # 入口HTML
│   ├── assets\                       # 打包后的CSS/JS
│   ├── ads\                          # 广告图片
│   └── logo.png
│
├── templates\                        # Flask模板目录（开发模式）
│
├── venv\                             # Python虚拟环境（开发环境）
│   ├── Scripts\                      # 可执行脚本
│   ├── Lib\                          # Python库
│   └── python.exe                    # Python解释器
│
├── app.py                            # 【核心】Flask后端主应用
│   功能：API服务、数据管理、AI调用
│   端口：5001
│   依赖：Flask, SQLite, 火山引擎SDK
│
├── debug_api.py                      # API调试脚本
│
├── debug_start.py                    # 调试启动脚本
│
├── index.html                        # 入口HTML文件
│
├── package.json                      # npm依赖配置
│   依赖：vue@3.5.13, vite@6.0.5, element-plus@2.8.4
│
├── vite.config.js                    # Vite构建配置
│   开发服务器端口：3000
│   API代理：/api -> localhost:5001
│
├── requirements.txt                  # Python依赖
│   flask, flask-cors, python-dotenv, volcengine, requests
│
├── .env                              # 【重要】环境变量配置
│   包含：VOLC_AK, VOLC_SK
│
├── .env.example                      # 环境变量示例
│
├── Dockerfile                        # Docker镜像定义
│
├── docker-compose.yml               # Docker编排配置
│
├── start.bat                        # Windows一键启动脚本
│
├── deploy.sh                        # Linux部署脚本
│
└── ciliAI.db                      # 【重要】SQLite数据库文件
    表：users, projects, generation_records, 
        chat_messages, compute_power_logs, invite_codes, ip_works
```

### 2.2 核心文件说明

| 文件路径 | 类型 | 功能说明 | 运维重要性 |
|---------|------|---------|----------|
| `app.py` | Python | Flask主应用，包含所有API接口 | ★★★★★ 核心 |
| `ciliAI.db` | SQLite | 数据库文件，存储所有业务数据 | ★★★★★ 关键 |
| `.env` | 配置文件 | 火山引擎API密钥配置 | ★★★★★ 敏感 |
| `requirements.txt` | 依赖清单 | Python依赖包列表 | ★★★★ 高 |
| `package.json` | 依赖清单 | Node.js依赖包列表 | ★★★★ 高 |
| `vite.config.js` | 配置文件 | 前端构建和代理配置 | ★★★ 中 |
| `start.bat` | 启动脚本 | Windows一键启动 | ★★★ 中 |

### 2.3 启动方法

#### 方式一：Windows一键启动（推荐用于开发测试）

```powershell
# 步骤1：打开终端，进入用户应用端目录
cd d:\ciliAI\ciliAI

# 步骤2：运行启动脚本
start.bat
```

**脚本执行流程**：

1. 检测Python环境
2. 创建Python虚拟环境（首次运行）
3. 安装Python依赖包
4. 启动Flask服务（端口5001）
5. 显示访问地址

**预期输出**：

```
==================================================
       即梦 AI 4.0 - Windows 局域网服务一键启动
==================================================

[1/4] 检测到 Python 已安装，正在准备虚拟环境...
[2/4] 激活虚拟环境...
[3/4] 检查并安装项目依赖包...
[4/4] 一切就绪！正在启动服务器...

==================================================
[成功] 服务器已启动！请不要关闭这个黑色窗口。
[访问方式] 在此电脑或局域网手机/电脑的浏览器输入：
          http://localhost:5001 (本机测)
       或 http://你的局域网IP:5001 (其他设备访问)
==================================================
```

#### 方式二：手动启动（开发调试模式）

```powershell
# 步骤1：进入用户应用端目录
cd d:\ciliAI\ciliAI

# 步骤2：创建虚拟环境（如已有则跳过）
python -m venv venv

# 步骤3：激活虚拟环境
.\venv\Scripts\activate

# 步骤4：安装Python依赖
pip install -r requirements.txt

# 步骤5：配置环境变量（创建.env文件）
# 文件路径：d:\ciliAI\ciliAI\.env
# 内容：
# VOLC_AK=你的AccessKeyID
# VOLC_SK=你的SecretAccessKey

# 步骤6：启动Flask应用
python app.py
```

**验证启动成功**：

访问 http://localhost:5001，应该显示CiliAI登录页面。

#### 方式三：Docker启动

```bash
# 步骤1：进入用户应用端目录
cd d:\ciliAI\ciliAI

# 步骤2：创建环境变量文件
cp .env.example .env
nano .env  # 编辑填入VOLC_AK和VOLC_SK

# 步骤3：构建并启动
docker-compose up -d

# 步骤4：查看日志
docker-compose logs -f
```

---

## 3. 管理后台端启动说明

### 3.1 目录结构详解

```
ruoyi\                               # 管理后台端根目录
│
├── src\                              # Vue前端源码目录
│   ├── api\                          # API调用封装目录
│   │   └── admin.js                 # 管理员API调用封装
│   │       功能：封装所有管理后台API
│   │       依赖：Axios HTTP客户端
│   │
│   ├── router\                       # 路由配置目录
│   │   └── index.js                 # 路由定义文件
│   │       配置：登录验证、权限控制
│   │
│   ├── views\                        # 页面视图目录
│   │   ├── Dashboard.vue            # 仪表盘
│   │   │   功能：系统统计概览
│   │   │   数据：用户数、项目数、邀请码统计
│   │   │   路由：/dashboard
│   │   │
│   │   ├── Login.vue                # 登录页面
│   │   │   功能：管理员身份验证
│   │   │   凭证：admin / admin123
│   │   │   路由：/login
│   │   │
│   │   ├── InviteCodes.vue          # 邀请码管理
│   │   │   功能：创建、编辑、删除邀请码
│   │   │   路由：/invite-codes
│   │   │   字段：code, compute_power, status
│   │   │
│   │   ├── Users.vue                # 用户管理
│   │   │   功能：查看用户列表、统计数据
│   │   │   路由：/users
│   │   │   数据：projects, generation_records
│   │   │
│   │   ├── Works.vue               # 作品管理
│   │   │   功能：管理IP作品、设置分类
│   │   │   路由：/works
│   │   │   分类：IP版权库、社区分享
│   │   │
│   │   └── Layout.vue              # 布局组件
│   │       功能：侧边栏、顶部导航
│   │
│   ├── App.vue                      # Vue根组件
│   │   功能：布局容器、路由视图
│   │
│   └── main.js                      # Vue应用入口
│       功能：创建Vue应用、注册插件
│       依赖：Vue Router, Pinia, Element Plus
│
├── templates\                        # HTML模板目录
│   └── index.html                   # Flask渲染的HTML
│
├── uploads\                          # 上传文件目录
│   └── .gitkeep                     # 保持目录存在
│
├── app.py                            # 【核心】Flask后端主应用
│   功能：管理后台API、邀请码管理、作品管理
│   端口：5002
│   依赖：Flask, SQLite
│
├── index.html                        # 入口HTML（Vite开发用）
│
├── package.json                      # npm依赖配置
│   依赖：vue@3.4.21, vite@5.1.6, element-plus@2.6.1, pinia@2.1.7
│
├── vite.config.js                    # Vite构建配置
│   开发服务器端口：3001
│   API代理：/api -> localhost:5002
│
└── Dockerfile                        # Docker镜像定义
```

### 3.2 核心文件说明

| 文件路径 | 类型 | 功能说明 | 运维重要性 |
|---------|------|---------|----------|
| `app.py` | Python | Flask后端API，处理邀请码和作品管理 | ★★★★★ 核心 |
| `src/api/admin.js` | JavaScript | API调用封装 | ★★★ 中 |
| `src/views/*.vue` | Vue组件 | 各个管理页面 | ★★★ 中 |
| `vite.config.js` | 配置文件 | 前端代理配置 | ★★★ 中 |

### 3.3 启动方法

#### 步骤1：启动管理后台后端（必须先启动）

```powershell
# 打开终端，进入管理后台目录
cd d:\ciliAI\ruoyi

# 激活虚拟环境（如有）
# .\venv\Scripts\activate

# 启动Flask后端
python app.py
```

**预期输出**：

```
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5002/
 * Running on http://192.168.1.100:5002/
```

**验证后端启动**：

在浏览器或终端访问：

```bash
# Windows
curl http://localhost:5002/

# 或访问登录接口
curl -X POST http://localhost:5002/api/admin/login ^
     -H "Content-Type: application/json" ^
     -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

#### 步骤2：启动管理后台前端

```powershell
# 新开终端，进入管理后台目录
cd d:\ciliAI\ruoyi

# 安装Node依赖（首次运行）
npm install

# 启动Vite开发服务器
npm run dev
```

**预期输出**：

```
VITE ready in 1153 ms

  Local:   http://localhost:3001/
  Network: use --host to expose
```

**验证前端启动**：

访问 http://localhost:3001，应该显示管理后台登录页面。

#### 步骤3：登录管理后台

1. 访问 http://localhost:3001
2. 输入用户名：`admin`
3. 输入密码：`admin123`
4. 点击登录

---

## 4. 数据库配置与初始化

### 4.1 数据库类型

| 属性 | 值 |
|-----|-----|
| **数据库类型** | SQLite 3 |
| **数据库文件** | `ciliAI/ciliAI.db` |
| **初始化方式** | 首次启动自动创建 |
| **数据文件位置** | `d:\ciliAI\ciliAI\ciliAI.db` |

### 4.2 数据库连接配置

#### 主应用数据库连接

**文件**：`ciliAI/app.py` 第23行

```python
DATABASE = 'ciliAI.db'  # 相对路径，相对于app.py所在目录
```

**连接配置**：

```python
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # 创建数据库连接
        db = g._database = sqlite3.connect(DATABASE, check_same_thread=False)
        # 设置行工厂为字典
        db.row_factory = sqlite3.Row
        # 启用外键约束
        db.execute('PRAGMA foreign_keys = ON')
    return db
```

#### 管理后台数据库连接

**文件**：`ruoyi/app.py` 第18行

```python
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ciliAI', 'ciliAI.db')
# 绝对路径：d:\ciliAI\ciliAI\ciliAI.db
```

### 4.3 数据库初始化脚本

#### 主应用初始化

**位置**：`ciliAI/app.py` 第47-286行

```python
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    
    # 创建数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (...)
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (...)
    ''')
    # ... 其他表
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id)')
    # ... 其他索引
    
    # 插入默认邀请码
    default_codes = ["111111", "222222", "333333", "444444", "555555", 
                     "666666", "777777", "888888", "999999", "000000"]
    for code in default_codes:
        try:
            cursor.execute('INSERT OR IGNORE INTO invite_codes (code, compute_power) VALUES (?, ?)', 
                          (code, 1000))
        except:
            pass
    
    conn.commit()
    conn.close()

# 应用启动时调用
init_db()
```

#### 管理后台初始化

**位置**：`ruoyi/app.py` 第367-396行

```python
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 创建ip_works表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            ...
        )
    ''')
    
    conn.commit()
    conn.close()
```

### 4.4 数据库表结构

#### users 表（用户表）

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invite_code TEXT UNIQUE NOT NULL,      -- 邀请码（唯一标识）
    compute_power INTEGER DEFAULT 0,        -- 当前算力余额
    total_power_used INTEGER DEFAULT 0,     -- 累计消耗算力
    nickname TEXT,                          -- 用户昵称
    avatar TEXT,                            -- 头像URL
    status TEXT DEFAULT 'active',           -- 状态：active/disabled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,                   -- 最后登录时间
    last_active TIMESTAMP                  -- 最后活跃时间
);
```

#### projects 表（项目表）

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,               -- 用户ID（外键）
    title TEXT NOT NULL,                    -- 项目标题
    description TEXT,                       -- 项目描述
    cover_image TEXT,                       -- 封面图片
    status TEXT DEFAULT 'active',           -- 状态：active/deleted
    image_count INTEGER DEFAULT 0,          -- 生成图片数量
    chat_count INTEGER DEFAULT 0,           -- 聊天消息数量
    total_power_used INTEGER DEFAULT 0,      -- 累计消耗算力
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

#### generation_records 表（生成记录表）

```sql
CREATE TABLE generation_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,                     -- 项目ID（可为空）
    user_id INTEGER NOT NULL,               -- 用户ID
    type TEXT NOT NULL,                     -- 类型：generate/inpaint/extend/super_resolution
    prompt TEXT,                            -- 提示词
    negative_prompt TEXT,                   -- 负面提示词
    image_url TEXT,                         -- 生成的图片URL
    image_width INTEGER,                    -- 图片宽度
    image_height INTEGER,                   -- 图片高度
    model_version TEXT,                     -- 模型版本
    params TEXT,                            -- 生成参数（JSON）
    task_id TEXT,                           -- 任务ID
    status TEXT DEFAULT 'completed',        -- 状态
    power_cost INTEGER DEFAULT 0,           -- 消耗算力
    error_msg TEXT,                         -- 错误信息
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

#### chat_messages 表（聊天消息表）

```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,                     -- 项目ID
    user_id INTEGER NOT NULL,               -- 用户ID
    chat_id TEXT NOT NULL,                  -- 聊天会话ID
    role TEXT NOT NULL,                     -- 角色：user/assistant
    content TEXT NOT NULL,                  -- 消息内容
    token_count INTEGER DEFAULT 0,          -- Token数量
    power_cost INTEGER DEFAULT 0,           -- 消耗算力
    metadata TEXT,                          -- 元数据（JSON）
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

#### compute_power_logs 表（算力日志表）

```sql
CREATE TABLE compute_power_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,               -- 用户ID
    project_id INTEGER,                     -- 项目ID
    record_id INTEGER,                      -- 生成记录ID
    operation_type TEXT NOT NULL,           -- 操作类型：generate/refund/init
    power_change INTEGER NOT NULL,          -- 算力变化（负数为消耗）
    power_before INTEGER NOT NULL,          -- 变化前算力
    power_after INTEGER NOT NULL,           -- 变化后算力
    description TEXT,                       -- 描述
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

#### invite_codes 表（邀请码表）

```sql
CREATE TABLE invite_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,              -- 邀请码（8位）
    status TEXT DEFAULT 'active',           -- 状态：active/used/disabled
    compute_power INTEGER DEFAULT 1000,     -- 分配的算力
    max_uses INTEGER DEFAULT 1,            -- 最大使用次数
    current_uses INTEGER DEFAULT 0,         -- 当前使用次数
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP,                      -- 使用时间
    created_by INTEGER,                     -- 创建者ID
    FOREIGN KEY (created_by) REFERENCES users (id)
);
```

#### ip_works 表（IP作品表）

```sql
CREATE TABLE ip_works (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,                    -- 作品标题
    student_name TEXT,                      -- 学生姓名
    image TEXT,                             -- 作品图片
    tags TEXT,                              -- 标签（JSON数组）
    cost TEXT,                              -- 成本
    duration TEXT,                           -- 时长
    price TEXT,                             -- 价格
    copyright TEXT,                          -- 版权信息
    introduction TEXT,                       -- 简介
    category TEXT DEFAULT 'IP版权库',         -- 分类：IP版权库/社区分享
    status TEXT DEFAULT 'active',           -- 状态
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4.5 数据库索引

| 表名 | 索引字段 | 类型 |
|-----|---------|------|
| projects | user_id | 普通索引 |
| projects | status | 普通索引 |
| generation_records | user_id | 普通索引 |
| generation_records | project_id | 普通索引 |
| generation_records | type | 普通索引 |
| chat_messages | user_id | 普通索引 |
| chat_messages | project_id | 普通索引 |
| chat_messages | chat_id | 普通索引 |
| compute_power_logs | user_id | 普通索引 |
| compute_power_logs | created_at | 普通索引 |

### 4.6 数据库初始化步骤

#### 首次启动（自动）

当应用首次启动时，`init_db()`函数会自动：

1. 创建数据库文件（如果不存在）
2. 创建所有数据表
3. 创建所有索引
4. 插入默认邀请码

**无需手动干预**，但需要注意：

- 确保应用有写入权限
- 确保磁盘空间充足

#### 手动初始化（如需重置）

```bash
# 步骤1：停止所有应用
# Windows: Ctrl+C 停止Flask
# Linux: pm2 stop all

# 步骤2：备份现有数据库
copy d:\ciliAI\ciliAI\ciliAI.db d:\ciliAI\ciliAI\ciliAI_backup.db

# 步骤3：删除数据库文件
del d:\ciliAI\ciliAI\ciliAI.db

# 步骤4：重启应用（会自动创建新数据库）
python app.py
```

#### 验证数据库初始化

```bash
# 使用sqlite3命令验证
sqlite3 d:\ciliAI\ciliAI\ciliAI.db ".tables"

# 预期输出：
# chat_messages    compute_power_logs    generation_records
# invite_codes     ip_works              projects
# users
```

---

## 5. 后端服务启动说明

### 5.1 服务列表

| 服务名称 | 类型 | 端口 | 技术栈 | 启动文件 |
|---------|------|------|--------|---------|
| **用户应用后端** | API服务 | 5001 | Flask + SQLite | ciliAI/app.py |
| **管理后台后端** | API服务 | 5002 | Flask + SQLite | ruoyi/app.py |
| **管理后台前端** | Web服务 | 3001 | Vite + Vue | ruoyi/ (npm) |

### 5.2 用户应用后端服务

#### 服务信息

| 属性 | 值 |
|-----|-----|
| **服务名称** | ciliAI-main |
| **监听端口** | 5001 |
| **启动命令** | `python app.py` |
| **工作目录** | `d:\ciliAI\ciliAI` |
| **配置文件** | `.env`, `app.py`, `requirements.txt` |
| **数据文件** | `ciliAI.db` |
| **依赖环境** | Python 3.9+, Flask, 火山引擎SDK |

#### 核心功能

1. **用户认证**：邀请码登录验证
2. **项目管理**：创建、查询、更新、删除项目
3. **AI图像生成**：调用火山引擎API生成图像
4. **图像编辑**：局部重绘、图像扩展、智能超分
5. **算力管理**：算力扣减、退还、日志记录
6. **数据统计**：用户、项目、生成记录统计

#### 启动步骤

**Windows环境**：

```powershell
cd d:\ciliAI\ciliAI
python app.py
```

**Linux环境**：

```bash
cd /var/www/ciliAI/ciliAI
source venv/bin/activate
python app.py
```

**Docker环境**：

```bash
cd d:\ciliAI\ciliAI
docker-compose up -d
```

#### 启动验证

访问健康检查端点：

```bash
curl http://localhost:5001/api/stats?invite_code=test
```

预期响应（未注册用户）：

```json
{"status": "error", "message": "用户不存在"}
```

### 5.3 管理后台后端服务

#### 服务信息

| 属性 | 值 |
|-----|-----|
| **服务名称** | ciliAI-admin-api |
| **监听端口** | 5002 |
| **启动命令** | `python app.py` |
| **工作目录** | `d:\ciliAI\ruoyi` |
| **配置文件** | `app.py` |
| **数据文件** | `ciliAI.db`（共享用户端数据库） |
| **依赖环境** | Python 3.9+, Flask |

#### 核心功能

1. **管理员认证**：用户名密码登录
2. **邀请码管理**：创建、编辑、删除、批量生成邀请码
3. **用户管理**：查看用户列表、统计数据
4. **作品管理**：管理IP作品、设置分类
5. **系统统计**：用户数、项目数、邀请码统计

#### 启动步骤

**Windows环境**：

```powershell
cd d:\ciliAI\ruoyi
python app.py
```

**Linux环境**：

```bash
cd /var/www/ciliAI/ruoyi
source venv/bin/activate
python app.py
```

#### 启动验证

访问健康检查端点：

```bash
curl http://localhost:5002/
```

预期响应：返回管理后台HTML页面

或访问登录接口：

```bash
curl -X POST http://localhost:5002/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

预期响应：

```json
{
  "code": 200,
  "msg": "登录成功",
  "data": {
    "token": "admin-token-1234567890",
    "username": "admin"
  }
}
```

### 5.4 管理后台前端服务

#### 服务信息

| 属性 | 值 |
|-----|-----|
| **服务名称** | ciliAI-admin-frontend |
| **监听端口** | 3001 |
| **启动命令** | `npm run dev` |
| **工作目录** | `d:\ciliAI\ruoyi` |
| **构建命令** | `npm run build` |
| **配置文件** | `vite.config.js`, `package.json` |
| **依赖环境** | Node.js 16+, npm 8+ |

#### 核心功能

1. **仪表盘**：系统统计概览
2. **邀请码管理**：可视化管理邀请码
3. **用户管理**：查看用户详情
4. **作品管理**：IP作品增删改查

#### 启动步骤

```powershell
cd d:\ciliAI\ruoyi

# 首次运行需要安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### 启动验证

访问 http://localhost:3001，应该显示管理后台登录页面。

---

## 6. 启动顺序与验证方法

### 6.1 正确启动顺序

```
重要：必须按以下顺序启动服务，否则可能导致功能异常
```

```
第一步：启动用户应用后端（端口5001）
        ↓
第二步：启动管理后台后端（端口5002）
        ↓
第三步：启动管理后台前端（端口3001）
```

### 6.2 启动顺序详解

#### 第一步：启动用户应用后端

**目的**：提供AI图像生成和用户管理API

**操作**：

```powershell
cd d:\ciliAI\ciliAI
python app.py
```

**验证方法**：

1. 检查终端输出，确认服务运行在端口5001
2. 访问 http://localhost:5001 应该显示登录页面
3. 测试API接口：

```bash
# 测试邀请码验证API
curl -X POST http://localhost:5001/api/verify-invite-code \
  -H "Content-Type: application/json" \
  -d '{"invite_code":"111111"}'
```

预期响应：

```json
{
  "status": "success",
  "message": "登录成功",
  "算力": 1000,
  "is_new_user": false
}
```

#### 第二步：启动管理后台后端

**目的**：提供管理后台API服务

**操作**：

```powershell
cd d:\ciliAI\ruoyi
python app.py
```

**验证方法**：

1. 检查终端输出，确认服务运行在端口5002
2. 测试API接口：

```bash
# 测试管理员登录
curl -X POST http://localhost:5002/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

预期响应：

```json
{
  "code": 200,
  "msg": "登录成功",
  "data": {
    "token": "admin-token-XXX",
    "username": "admin"
  }
}
```

#### 第三步：启动管理后台前端

**目的**：提供管理后台Web界面

**操作**：

```powershell
cd d:\ciliAI\ruoyi
npm run dev
```

**验证方法**：

1. 检查终端输出，确认服务运行在端口3001
2. 访问 http://localhost:3001
3. 应该显示管理后台登录页面
4. 输入admin/admin123登录
5. 验证能进入仪表盘页面

### 6.3 各组件验证清单

| 组件 | 验证方法 | 预期结果 | 验证命令 |
|-----|---------|---------|---------|
| 用户应用后端 | 访问主页 | 显示登录页面 | `curl http://localhost:5001` |
| 用户应用后端 | API调用 | 返回JSON响应 | `curl http://localhost:5001/api/stats?invite_code=test` |
| 管理后台后端 | 访问主页 | 返回HTML | `curl http://localhost:5002/` |
| 管理后台后端 | 登录API | 登录成功 | `curl -X POST http://localhost:5002/api/admin/login -d "..."` |
| 管理后台前端 | 访问主页 | 显示登录页面 | 浏览器访问 http://localhost:3001 |
| 数据库 | 查询表 | 返回表列表 | `sqlite3 ciliAI.db ".tables"` |

### 6.4 启动时间预估

| 组件 | 首次启动时间 | 后续启动时间 |
|-----|------------|-------------|
| 用户应用后端 | 30-60秒 | 5-10秒 |
| 管理后台后端 | 10-20秒 | 3-5秒 |
| 管理后台前端 | 60-120秒 | 10-20秒 |
| **总计** | **100-200秒** | **18-35秒** |

---

## 7. 常见启动问题解决

### 7.1 端口被占用

#### 问题描述

```
OSError: [Errno 10048] Only one usage of each socket address is normally permitted
```

#### 解决方案

**Windows**：

```powershell
# 查找占用端口的进程
netstat -ano | findstr :5001

# 假设输出为：
# TCP    0.0.0.0:5001    0.0.0.0:0    LISTENING    1234

# 终止进程
taskkill /PID 1234 /F
```

**Linux**：

```bash
# 查找占用端口的进程
lsof -i :5001

# 终止进程
kill -9 <进程ID>
```

### 7.2 Python模块缺失

#### 问题描述

```
ModuleNotFoundError: No module named 'flask'
```

#### 解决方案

```bash
# 进入虚拟环境
cd d:\ciliAI\ciliAI
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 7.3 火山引擎密钥未配置

#### 问题描述

```
WARNING: VOLC_AK or VOLC_SK not found in environment variables!
```

#### 解决方案

```powershell
# 创建环境变量文件
cd d:\ciliAI\ciliAI
notepad .env

# 填入以下内容：
# VOLC_AK=你的AccessKeyID
# VOLC_SK=你的SecretAccessKey

# 保存后重启应用
python app.py
```

### 7.4 数据库锁定

#### 问题描述

```
database is locked
```

#### 解决方案

1. 检查是否有其他进程访问数据库

```powershell
# Windows
tasklist | findstr python

# 终止多余的Python进程
taskkill /PID <进程ID> /F
```

2. 重启应用

```bash
python app.py
```

### 7.5 Node模块安装失败

#### 问题描述

```
npm ERR! code ENOENT
npm ERR! syscall symlink
```

#### 解决方案

```powershell
cd d:\ciliAI\ruoyi

# 删除缓存
rmdir /s /q node_modules
del package-lock.json

# 重新安装
npm install
```

### 7.6 前端代理失败

#### 问题描述

```
Failed to proxy from localhost:3001 to http://localhost:5002
```

#### 解决方案

1. 确认管理后台后端已启动（端口5002）

```bash
curl http://localhost:5002/
```

2. 检查防火墙设置

```powershell
# Windows防火墙添加规则
netsh advfirewall firewall add rule name="Flask Admin" dir=in action=allow protocol=tcp localport=5002
```

3. 检查vite.config.js代理配置

```javascript
// vite.config.js
server: {
  port: 3001,
  proxy: {
    '/api': {
      target: 'http://localhost:5002',
      changeOrigin: true
    }
  }
}
```

---

## 附录A：快速启动命令汇总

### Windows环境

```powershell
# 启动用户应用后端
cd d:\ciliAI\ciliAI
start.bat

# 启动管理后台后端（新终端）
cd d:\ciliAI\ruoyi
python app.py

# 启动管理后台前端（新终端）
cd d:\ciliAI\ruoyi
npm run dev
```

### Linux环境

```bash
# 使用PM2管理
cd /var/www/ciliAI/ciliAI
pm2 start python --name "ciliAI-main" -- app.py

cd /var/www/ciliAI/ruoyi
pm2 start python --name "ciliAI-admin" -- app.py
```

### Docker环境

```bash
cd d:\ciliAI\ciliAI
docker-compose up -d
```

---

## 附录B：访问地址汇总

| 服务 | 地址 | 说明 |
|-----|------|------|
| 用户应用 | http://localhost:5001 | 主应用入口 |
| 管理后台 | http://localhost:3001 | 管理员入口 |
| 管理后台API | http://localhost:5002 | API接口 |

---

**文档版本**：1.0  
**最后更新**：2026-04-12  
**维护者**：CiliAI技术团队



