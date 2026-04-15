# CiliAI Platform - AI创作平台

CiliAI 是一个基于火山引擎即梦AI的创作平台，支持文生图、视频生成、数字人等功能。

## 📋 项目概览

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端** | Flask + Python 3.9+ | RESTful API服务 |
| **前端** | Vue 3 + Vite + Element Plus | 用户界面 |
| **数据库** | SQLite | 数据存储（fangtang.db） |
| **AI服务** | 火山引擎即梦API | 文生图、视频生成等 |
| **容器化** | Docker + Docker Compose | 快速部署 |

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     用户浏览器                           │
└────────────────┬────────────────────────┬──────────────┘
                 │                        │
          http://localhost:3002    http://localhost:5001
                 │                        │
                 ▼                        ▼
┌─────────────────────────────────────────────────────────┐
│                   Vue 3 前端                            │
│              (npm run dev)                             │
│                                                         │
│  • 后台管理: http://localhost:3002                     │
│  • 用户端: http://localhost:3003                       │
└─────────────────────────────────────────────────────────┘
                 │                        │
                 │    /api/*            │
                 ▼                        ▼
┌─────────────────────────────────────────────────────────┐
│                 Flask 后端 API                           │
│              (python app.py)                           │
│                                                         │
│  • 用户API: /api/*                                     │
│  • 管理API: /api/admin/*                               │
│  • 静态文件: /uploads/*                                │
└─────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                 火山引擎即梦API                         │
│          (VOLC_AK / VOLC_SK)                          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 1️⃣ 环境要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16 或更高版本
- **npm**: 6 或更高版本（或使用 yarn）
- **火山引擎账号**: 需要AccessKey和SecretKey

### 2️⃣ 克隆项目

```bash
git clone https://github.com/ililiil/ciliAI.git
cd ciliAI
```

### 3️⃣ 配置火山引擎密钥

#### 方式一：环境变量文件（推荐）

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
```

编辑 `.env` 文件，配置密钥：

```env
# 方式1：单组密钥（旧版兼容）
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey

# 方式2：多组密钥（支持负载均衡和轮换）
VOLC_AK_1=你的AccessKeyID_1
VOLC_SK_1=你的SecretAccessKey_1
VOLC_AK_2=你的AccessKeyID_2
VOLC_SK_2=你的SecretAccessKey_2
# ... 可以配置多组密钥（支持100组）
```

**获取密钥地址**：[火山引擎控制台 - 密钥管理](https://console.volcengine.com/iam/keymanage/)

#### 方式二：直接设置环境变量

```bash
# Linux/Mac
export VOLC_AK_1="你的AccessKeyID"
export VOLC_SK_1="你的SecretAccessKey"

# Windows CMD
set VOLC_AK_1=你的AccessKeyID
set VOLC_SK_1=你的SecretAccessKey

# Windows PowerShell
$env:VOLC_AK_1="你的AccessKeyID"
$env:VOLC_SK_1="你的SecretAccessKey"
```

### 4️⃣ 安装依赖

#### 后端依赖

```bash
# 创建虚拟环境（推荐，隔离项目依赖）
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装后端依赖
pip install -r requirements.txt
```

#### 前端依赖

```bash
npm install
```

## 🎯 启动方式

### 方式一：完整开发环境（推荐）

需要同时运行后端API和前端开发服务器。

**终端1 - 启动后端API：**

```bash
python app.py
```

后端启动成功会显示：
```
✓ 密钥管理器初始化完成，共 X 组密钥
 * Running on http://0.0.0.0:5001
```

**终端2 - 启动前端开发服务器：**

```bash
npm run dev
```

前端启动成功会显示：
```
VITE v6.0.5  ready in XXX ms

➜  Local:   http://localhost:3002/
➜  Network: http://192.168.x.x:3002/
```

**访问地址：**

| 平台 | 地址 | 说明 |
|------|------|------|
| 后台管理 | http://localhost:3002 | 管理用户、订单、作品等 |
| 用户端 | http://localhost:3003 | AI创作功能（文生图、视频等） |
| 后端API | http://localhost:5001 | API接口（供前端调用） |

### 方式二：纯后端模式

只运行后端API，适合快速测试或API调用。

```bash
python app.py
```

访问 `http://localhost:5001` 查看API文档或测试接口。

### 方式三：Windows一键启动

双击运行 `start.bat`，脚本会自动：
1. 检测Python环境
2. 创建虚拟环境
3. 安装依赖
4. 启动服务

```batch
start.bat
```

启动后访问 `http://localhost:5001`

## 📦 项目结构详解

```
ciliAI/
│
├── 🌐 后端 (Flask)
│   ├── app.py                 # 主应用文件，包含所有API路由
│   ├── key_manager.py         # 密钥管理器，支持多密钥轮换
│   ├── requirements.txt       # Python依赖清单
│   ├── fangtang.db           # SQLite数据库文件
│   ├── uploads/              # 用户上传文件目录
│   └── check_user.py         # 用户检查工具
│
├── 🎨 前端 (Vue 3)
│   ├── src/
│   │   ├── views/           # 页面视图
│   │   │   ├── Home.vue     # 首页
│   │   │   ├── Order.vue    # 接单广场
│   │   │   ├── Profile.vue  # 个人中心
│   │   │   ├── ProjectDetail.vue  # 项目详情
│   │   │   ├── Task.vue     # 任务中心
│   │   │   └── Works.vue    # 作品展示
│   │   │
│   │   ├── components/      # 公共组件
│   │   │   ├── LoginModal.vue      # 登录弹窗
│   │   │   ├── CreateProjectModal.vue  # 创建项目
│   │   │   ├── NovelDetailModal.vue   # 小说详情
│   │   │   └── ProjectManager.vue      # 项目管理
│   │   │
│   │   ├── router/          # 路由配置
│   │   │   └── index.js     # 路由定义
│   │   │
│   │   ├── utils/           # 工具函数
│   │   │   └── volcengine.js # 火山引擎SDK封装
│   │   │
│   │   ├── styles/          # 样式文件
│   │   │   └── global.css   # 全局样式
│   │   │
│   │   ├── routes/          # API路由
│   │   │   └── api/         # API中间件
│   │   │
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 入口文件
│   │
│   ├── package.json         # Node依赖配置
│   ├── vite.config.js       # Vite构建配置
│   ├── index.html          # HTML模板
│   └── dist/               # 构建输出目录
│
├── ⚙️ 配置文件
│   ├── .env                 # 环境变量（密钥配置）
│   ├── .env.example        # 环境变量模板
│   ├── .gitignore          # Git忽略文件
│   ├── Dockerfile           # Docker镜像构建
│   ├── docker-compose.yml   # Docker Compose编排
│   └── start.bat           # Windows一键启动脚本
│
├── 📚 文档
│   ├── 说明/                # 火山引擎API文档
│   └── *.md                # 项目文档
│
└── 🧪 测试文件
    ├── test-api.html        # API测试页面
    ├── test_key_rotation.py # 密钥轮换测试
    ├── check_user.py        # 用户检查工具
    └── debug_*.py          # 调试脚本
```

## 🔌 API接口说明

### 用户端API (`/api/*`)

| 方法 | 路由 | 说明 |
|------|------|------|
| POST | /api/verify-invite-code | 验证邀请码 |
| GET | /api/user/info | 获取用户信息 |
| GET | /api/user/power | 获取算力余额 |
| POST | /api/power/deduct | 扣除算力 |
| GET | /api/projects | 获取项目列表 |
| POST | /api/projects | 创建项目 |
| POST | /api/generate | 文生图 |
| POST | /api/inpaint | 局部重绘 |
| POST | /api/extend | 图片扩展 |
| POST | /api/super-resolution | 智能超清 |
| GET | /api/records | 获取生成记录 |
| POST | /api/upload-image | 上传图片 |
| GET | /api/works | 获取作品列表 |
| POST | /api/orders | 创建订单 |

### 管理端API (`/api/admin/*`)

| 方法 | 路由 | 说明 |
|------|------|------|
| POST | /api/admin/login | 管理员登录 |
| GET | /api/admin/info | 获取管理员信息 |
| GET | /api/admin/users | 用户列表 |
| PUT | /api/admin/users/:id/power | 调整用户算力 |
| GET | /api/admin/invite-codes | 邀请码列表 |
| POST | /api/admin/invite-codes | 创建邀请码 |
| PUT | /api/admin/invite-codes/:id | 更新邀请码 |
| DELETE | /api/admin/invite-codes/:id | 删除邀请码 |
| GET | /api/admin/orders | 订单列表 |
| POST | /api/admin/orders | 创建订单 |
| PUT | /api/admin/orders/:id | 更新订单 |
| GET | /api/admin/works | 作品列表 |
| POST | /api/admin/works | 创建作品 |
| PUT | /api/admin/works/:id | 更新作品 |
| GET | /api/admin/stats | 数据统计 |
| GET | /api/admin/power-logs | 算力日志 |
| POST | /api/admin/upload | 上传管理图片 |

**管理员默认账号**：`admin` / `admin123`

## 🐳 生产环境部署

### 方式一：Docker部署（推荐）

#### 1. 构建并启动

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 2. 访问服务

- 前端：`http://你的服务器IP:5001`
- API：`http://你的服务器IP:5001/api/*`

#### 3. 停止服务

```bash
docker-compose down
```

#### 4. 重新部署

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 方式二：手动部署

#### 1. 构建前端

```bash
npm run build
```

前端构建产物在 `dist/` 目录。

#### 2. 配置环境变量

确保 `.env` 文件包含正确的密钥配置。

#### 3. 使用Gunicorn运行后端（生产环境）

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

#### 4. 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/ciliAI/dist;
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 上传文件
    location /uploads {
        alias /path/to/ciliAI/uploads;
        expires 30d;
    }
}
```

#### 5. 使用systemd管理服务

创建服务文件 `/etc/systemd/system/ciliai.service`：

```ini
[Unit]
Description=CiliAI Platform
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/ciliAI
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable ciliai
sudo systemctl start ciliai
sudo systemctl status ciliai
```

### 方式三：Linux服务器一键部署

编辑 `deploy.sh` 修改服务器信息：

```bash
TARGET="user@your-server-ip"
REMOTE_DIR="/path/to/deploy"
```

执行部署：

```bash
chmod +x deploy.sh
./deploy.sh
```

## 🌐 局域网部署

### 1. 修改后端监听地址

默认配置 `app.py` 已设置为 `host='0.0.0.0'`，支持局域网访问。

### 2. 获取服务器IP

```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

找到IPv4地址，例如：`192.168.1.100`

### 3. 访问

在同一局域网的设备浏览器中访问：

```
http://192.168.1.100:5001  # 后端API和前端
```

### 4. Windows防火墙设置

如果其他设备无法访问，需要开放端口：

1. 打开 "Windows Defender 防火墙"
2. 点击 "高级设置"
3. 选择 "入站规则" → "新建规则"
4. 规则类型：端口
5. 协议：TCP，端口：5001
6. 操作：允许连接
7. 命名规则，例如："CiliAI API Port"

## ⚙️ 配置详解

### 火山引擎密钥配置

#### 单组密钥（旧版兼容）

```env
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey
```

#### 多组密钥（推荐）

支持配置多组密钥，系统会自动轮换：

```env
VOLC_AK_1=你的AccessKeyID_1
VOLC_SK_1=你的SecretAccessKey_1
VOLC_AK_2=你的AccessKeyID_2
VOLC_SK_2=你的SecretAccessKey_2
VOLC_AK_3=你的AccessKeyID_3
VOLC_SK_3=你的SecretAccessKey_3
# ... 最多支持100组
```

**多密钥优势**：
- 负载均衡，分散API调用压力
- 自动轮换，避免单密钥频率限制
- 容灾备份，某个密钥失效不影响服务

### 算力成本配置

编辑 `app.py` 中的 `POWER_COST` 字典：

```python
POWER_COST = {
    'generate': 5,             # 文生图
    'extend': 5,               # 图片扩展
    'super_resolution': 8,      # 智能超清
    'inpaint': 5,              # 局部重绘
    'chat': 1                  # 数字人
}
```

### 数据库配置

默认使用SQLite数据库 `fangtang.db`。

如需切换到MySQL/PostgreSQL：

```python
# 安装驱动
pip install pymysql      # MySQL
pip install psycopg2     # PostgreSQL

# 修改 app.py 中的数据库连接
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/ciliai'
# 或
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/ciliai'
```

### 上传文件配置

```python
# 编辑 app.py
UPLOAD_FOLDER = 'uploads'  # 上传目录
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
```

## 🐛 常见问题

### 1. 端口被占用

**Windows：**

```bash
# 查找占用端口的进程
netstat -ano | findstr :5001

# 结束进程
taskkill /PID <进程ID> /F
```

**Linux/Mac：**

```bash
# 查找占用端口的进程
lsof -i :5001

# 结束进程
kill <进程ID>
```

### 2. 前端无法连接后端API

检查项：
1. 后端是否启动成功（查看终端日志）
2. Vite代理配置是否正确（`vite.config.js`）
3. 浏览器控制台是否有CORS错误
4. 后端是否监听在 `0.0.0.0` 而不是 `127.0.0.1`

### 3. 火山引擎API调用失败

可能原因：
- **密钥错误**：检查 `.env` 中的AK/SK是否正确
- **权限不足**：确认密钥有调用即梦API的权限
- **余额不足**：登录火山引擎控制台充值
- **频率限制**：使用多组密钥分散压力
- **网络问题**：服务器能否访问火山引擎API

查看后端日志获取详细错误信息。

### 4. 数据库锁定

SQLite并发写入可能锁定：

```python
# 在 app.py 中配置连接池
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

或切换到MySQL/PostgreSQL。

### 5. Docker部署失败

```bash
# 清理Docker缓存
docker system prune -a

# 重新构建（不缓存）
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 查看详细日志
docker-compose logs -f --tail=100
```

### 6. 虚拟环境问题

```bash
# 删除旧虚拟环境
rm -rf venv

# 重新创建
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 重新安装依赖
pip install -r requirements.txt
```

### 7. npm依赖安装失败

```bash
# 清理npm缓存
npm cache clean --force

# 删除node_modules
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

## 🔧 常用命令速查

### 后端命令

```bash
# 启动后端
python app.py

# 启动后端（生产模式）
gunicorn -w 4 -b 0.0.0.0:5001 app:app

# 检查用户
python check_user.py

# 测试密钥轮换
python test_key_rotation.py
```

### 前端命令

```bash
# 开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

### Docker命令

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重新构建
docker-compose up -d --build
```

### 数据库命令

```bash
# 查看数据库大小
ls -lh fangtang.db

# 备份数据库
cp fangtang.db fangtang.db.backup

# 恢复数据库
cp fangtang.db.backup fangtang.db
```

## 📞 技术支持

- **GitHub Issues**: https://github.com/ililiil/ciliAI/issues
- **邮箱**: 请在GitHub Issue中联系

## 📄 许可证

MIT License

## 🙏 致谢

- [火山引擎](https://www.volcengine.com/) - 提供强大的AI能力
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Flask](https://flask.palletsprojects.com/) - 轻量级WSGI Web应用框架
- [Element Plus](https://element-plus.org/) - Vue 3 UI组件库
- [Vite](https://vitejs.dev/) - 下一代前端构建工具

## 📝 更新日志

### v0.4.6 (2026-04-15)
- ✅ **Docker 部署配置优化**：移除 SQLite 数据库文件挂载
- ✅ **环境变量配置更新**：添加 MySQL 配置说明和注释模板
- ✅ **部署文档全面更新**：添加 MySQL 8.0+ 部署步骤、安全建议、备份策略
- ✅ **代码验证完成**：MySQL 兼容性 100%，无 SQLite 残留
- ✅ **功能检查完成**：管理后台、用户端、数据库、API、业务功能全部完整

### v0.4.5 (2026-04-15)
- 🔥 **移除 SQLite 支持**：简化代码，仅支持 MySQL 数据库
- 🐛 **修复 TEXT 默认值问题**：将 chat_sessions 表的 TEXT 字段改为 VARCHAR(255)
- ✅ **统一 SQL 语法**：所有 SQL 占位符从 `?` 改为 MySQL 标准 `%s`
- 📦 **代码清理**：删除所有 SQLite/PostgreSQL 兼容代码
- 🚀 **简化配置**：移除 DB_TYPE 判断，直接使用 MySQL 配置
- ⚡ **性能优化**：清理冗余导入，提高代码可维护性

### v0.4.4 (2026-04-15)
- 🐛 **修复 MySQL 兼容性问题**：所有表的创建语句现在都支持 MySQL 和 SQLite 两种数据库
- ✨ **添加 MySQL 完整支持**：为 projects、generation_records、chat_messages、compute_power_logs、invite_codes、ip_works、orders、advertisements、chat_sessions 表添加 MySQL 语法支持
- 📝 **优化字段类型**：MySQL 使用 INT 替代 INTEGER，VARCHAR 替代 TEXT，提高数据库性能

### v0.4.3 (2026-04-15)
- 🐛 **修复依赖缺失**：添加 pymysql 到 requirements.txt
- ✨ **完善部署配置**：确保所有数据库驱动可用

### v0.4.2 (2026-04-15)
- ✨ **Docker 部署优化**：升级 Node.js 版本从 16 到 20，完全兼容 Vite 6.x
- ✨ **修复静态文件路径**：修正 Dockerfile 中的 dist 目录配置
- ✨ **完善 Docker 配置**：添加健康检查、日志轮转、数据持久化
- ✨ **创建 .dockerignore**：优化镜像构建，排除不必要的文件
- ✨ **添加 SPA 路由支持**：修复前端路由 404 问题
- 📦 **新增文档**：添加 DEPLOYMENT.md 详细部署指南

### v0.3.3 (2026-04-14)
- 重构项目结构
- 添加完整的Docker支持
- 优化密钥管理系统，支持多密钥轮换
- 完善API文档和使用说明
