# CiliAI短剧平台 - 部署运维指南

## 文档信息

- **项目名称**：CiliAI短剧平台（即梦AI 4.0）
- **版本**：0.0.6
- **编写日期**：2026-04-11
- **文档用途**：运维工程师部署指南

---

## 一、项目概述

CiliAI短剧平台是一个基于AI的图像生成和短剧制作平台，提供以下核心功能：

### 1.1 功能模块

- **AI图像生成**：文生图、图生图
- **图像编辑**：局部重绘（Inpaint）、图像扩展（Extend）
- **图像增强**：智能超分（Super Resolution）
- **项目管理**：用户可创建和管理多个项目
- **算力系统**：基于邀请码的算力分配和消耗系统
- **社区功能**：作品展示和分享

### 1.2 应用组成

平台由两个独立应用组成：

| 应用 | 说明 | 端口 | 访问地址 |
|------|------|------|----------|
| **ciliAI** | 主应用（用户端） | 5001 | http://服务器IP:5001 |
| **ruoyi** | 管理后台（管理员端） | 5002 (后端) / 3001 (前端) | http://服务器IP:3001 |

### 1.3 技术架构

```
┌─────────────────────────────────────────────────────┐
│                    用户端应用                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  Vue 3 前端  │  │  Vite 构建  │  │ Element Plus│  │
│  └──────┬──────┘  └─────────────┘  └─────────────┘  │
│         │                                               │
│  ┌──────▼──────┐  ┌─────────────┐  ┌─────────────┐  │
│  │ Flask API   │──│  SQLite DB  │──│火山引擎AI服务│  │
│  │  (端口5001) │  │ ciliAI.db│  │  Visual API │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   管理后台应用                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  Vue 3 前端  │  │  Vite 构建  │  │ Element Plus│  │
│  │  (端口3001) │  │             │  │             │  │
│  └──────┬──────┘  └─────────────┘  └─────────────┘  │
│         │                                               │
│  ┌──────▼──────┐  ┌─────────────┐                     │
│  │ Flask API   │──│  SQLite DB  │                     │
│  │  (端口5002) │  │ ciliAI.db│                     │
│  └─────────────┘  └─────────────┘                     │
└─────────────────────────────────────────────────────┘
```

---

## 二、项目结构

### 2.1 完整目录结构

```
ciliAI/                          # 项目根目录
│
├── ciliAI/                      # 主应用目录（用户端）
│   ├── src/                       # Vue前端源代码
│   │   ├── components/            # 可复用组件
│   │   │   ├── CreateProjectModal.vue    # 创建项目弹窗
│   │   │   ├── LoginModal.vue            # 登录弹窗
│   │   │   ├── NovelDetailModal.vue      # 小说详情弹窗
│   │   │   └── ProjectManager.vue        # 项目管理组件
│   │   ├── views/                # 页面视图
│   │   │   ├── Home.vue         # 首页
│   │   │   ├── Order.vue        # 订单页面
│   │   │   ├── Profile.vue      # 个人中心
│   │   │   ├── ProjectDetail.vue # 项目详情
│   │   │   ├── Task.vue         # 任务页面
│   │   │   └── Works.vue        # 作品页面
│   │   ├── router/              # 路由配置
│   │   │   └── index.js
│   │   ├── styles/              # 全局样式
│   │   │   └── global.css
│   │   ├── utils/               # 工具函数
│   │   │   └── volcengine.js    # 火山引擎SDK封装
│   │   ├── routes/api/           # API路由（前端调用）
│   │   │   └── verify-invite-code.js
│   │   ├── App.vue              # 根组件
│   │   └── main.js              # 入口文件
│   ├── public/                   # 静态资源
│   │   ├── ads/                 # 广告图片
│   │   │   ├── ad1.png
│   │   │   ├── ad2.png
│   │   │   └── ad3.png
│   │   └── logo-C5RxjwAw.png    # Logo
│   ├── dist/                     # 生产构建产物（Vite打包）
│   │   ├── index.html
│   │   ├── assets/             # 打包后的CSS/JS
│   │   ├── ads/                # 广告图片
│   │   └── logo-C5RxjwAw.png
│   ├── venv/                     # Python虚拟环境（开发环境）
│   │   ├── Scripts/            # 可执行脚本
│   │   ├── Lib/                # Python库文件
│   │   └── python.exe          # Python解释器
│   ├── templates/               # Flask模板目录
│   ├── app.py                   # Flask主应用
│   ├── debug_api.py             # 调试API脚本
│   ├── debug_start.py           # 调试启动脚本
│   ├── index.html               # 入口HTML
│   ├── package.json             # npm依赖配置
│   ├── package-lock.json        # npm依赖锁定文件
│   ├── vite.config.js           # Vite构建配置
│   ├── requirements.txt         # Python依赖
│   ├── Dockerfile               # Docker构建文件
│   ├── docker-compose.yml       # Docker编排配置
│   ├── deploy.sh                # Linux部署脚本
│   ├── start.bat                # Windows启动脚本
│   ├── .env                     # 环境变量配置（包含密钥）
│   ├── .env.example             # 环境变量示例
│   ├── .gitignore               # Git忽略文件
│   └── ciliAI.db             # SQLite数据库文件
│
├── ruoyi/                       # 管理后台目录
│   ├── src/                     # Vue前端源代码
│   │   ├── api/                # API调用封装
│   │   │   └── admin.js
│   │   ├── router/             # 路由配置
│   │   │   └── index.js
│   │   ├── views/              # 页面视图
│   │   │   ├── Dashboard.vue   # 仪表盘
│   │   │   ├── InviteCodes.vue  # 邀请码管理
│   │   │   ├── Layout.vue      # 布局组件
│   │   │   ├── Login.vue       # 登录页面
│   │   │   ├── Users.vue       # 用户管理
│   │   │   └── Works.vue       # 作品管理
│   │   ├── App.vue
│   │   └── main.js
│   ├── templates/               # HTML模板
│   │   └── index.html
│   ├── app.py                   # Flask管理后台
│   ├── index.html               # 入口HTML
│   ├── package.json             # npm依赖配置
│   ├── package-lock.json
│   ├── vite.config.js           # Vite配置（代理到5002端口）
│   ├── Dockerfile               # Docker构建文件
│   ├── .gitignore
│   └── index.html
│
└── INTEGRATION_REPORT.md         # 集成报告
```

### 2.2 各目录说明

#### ciliAI/ 目录

| 目录/文件 | 说明 | 运维注意事项 |
|-----------|------|-------------|
| `src/` | Vue前端源码 | 开发时需要，部署时不需要 |
| `dist/` | 生产构建产物 | 部署时使用，由`npm run build`生成 |
| `venv/` | Python虚拟环境 | 开发时使用，生产环境应重新创建 |
| `app.py` | Flask后端主应用 | **核心启动文件** |
| `ciliAI.db` | SQLite数据库 | **重要数据文件，需要备份** |
| `.env` | 环境变量 | **包含敏感密钥，谨慎管理** |
| `start.bat` | Windows启动脚本 | 一键启动（仅Windows） |
| `Dockerfile` | Docker镜像定义 | 用于容器化部署 |
| `docker-compose.yml` | Docker编排配置 | 容器化部署使用 |

#### ruoyi/ 目录

| 目录/文件 | 说明 | 运维注意事项 |
|-----------|------|-------------|
| `src/` | Vue前端源码 | 开发时需要 |
| `app.py` | Flask管理后台API | **需要先于前端启动** |
| `package.json` | npm依赖配置 | 需要`npm install` |
| `vite.config.js` | Vite配置 | 代理到5002端口 |

---

## 三、技术栈详情

### 3.1 后端技术栈

| 技术 | 版本 | 用途 | 依赖文件 |
|------|------|------|----------|
| **Python** | 3.9+ | 编程语言 | - |
| **Flask** | 最新版 | Web框架 | requirements.txt |
| **Flask-CORS** | 最新版 | 跨域资源共享 | requirements.txt |
| **python-dotenv** | 最新版 | 环境变量管理 | requirements.txt |
| **volcengine** | 最新版 | 火山引擎SDK | requirements.txt |
| **requests** | 最新版 | HTTP客户端 | requirements.txt |
| **SQLite** | 3.x | 数据库 | Python内置 |

**requirements.txt 内容**：

```
flask
flask-cors
python-dotenv
volcengine
requests
```

### 3.2 前端技术栈

#### 主应用 (ciliAI)

| 技术 | 版本 | 用途 | 依赖文件 |
|------|------|------|----------|
| **Vue.js** | 3.5.13 | 渐进式JavaScript框架 | package.json |
| **Vue Router** | 4.4.5 | Vue路由管理 | package.json |
| **Element Plus** | 2.8.4 | UI组件库 | package.json |
| **Axios** | 1.7.9 | HTTP客户端 | package.json |
| **Vite** | 6.0.5 | 构建工具 | package.json |
| **@vitejs/plugin-vue** | 5.2.1 | Vite的Vue插件 | package.json |

#### 管理后台 (ruoyi)

| 技术 | 版本 | 用途 | 依赖文件 |
|------|------|------|----------|
| **Vue.js** | 3.4.21 | JavaScript框架 | package.json |
| **Vue Router** | 4.3.0 | 路由管理 | package.json |
| **Pinia** | 2.1.7 | 状态管理 | package.json |
| **Element Plus** | 2.6.1 | UI组件库 | package.json |
| **@element-plus/icons-vue** | 2.3.1 | 图标库 | package.json |
| **Axios** | 1.6.7 | HTTP客户端 | package.json |
| **Vite** | 5.1.6 | 构建工具 | package.json |

---

## 四、环境要求

### 4.1 服务器要求

#### 最低配置（开发/测试）

- **CPU**: 2核心
- **内存**: 4GB
- **磁盘**: 20GB
- **系统**: Windows Server 2019+ / Ubuntu 20.04+ / CentOS 8+

#### 推荐配置（生产环境）

- **CPU**: 4核心+
- **内存**: 8GB+
- **磁盘**: 50GB+ (根据数据量增长)
- **系统**: Ubuntu 20.04 LTS / CentOS 8

### 4.2 软件依赖

#### 必需软件

| 软件 | 版本要求 | 说明 | 安装命令 |
|------|----------|------|----------|
| **Python** | 3.9+ | 后端运行环境 | 见4.3节 |
| **Node.js** | 16+ | 前端构建工具 | 见4.3节 |
| **npm** | 8+ | Node包管理器 | 随Node安装 |
| **Git** | 2.0+ | 版本控制 | 可选 |

#### 可选软件（推荐）

| 软件 | 版本要求 | 用途 |
|------|----------|------|
| **Docker** | 20.10+ | 容器化部署 |
| **Docker Compose** | 2.0+ | 容器编排 |
| **PM2** | 5.0+ | 进程管理（Linux） |

### 4.3 安装步骤

#### Windows 环境

```powershell
# 1. 安装 Python 3.9+
# 访问 https://www.python.org/downloads/ 下载安装
# 安装时勾选 "Add Python to PATH"

# 验证安装
python --version

# 2. 安装 Node.js 16+
# 访问 https://nodejs.org/ 下载LTS版本

# 验证安装
node --version
npm --version
```

#### Ubuntu / Debian 环境

```bash
# 1. 安装 Python 3.9+
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip

# 2. 安装 Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs

# 3. 验证安装
python3 --version
node --version
npm --version
```

#### CentOS / RHEL 环境

```bash
# 1. 安装 Python 3.9+
sudo dnf install python3.9 python3.9-venv python3-pip

# 2. 安装 Node.js 16+
curl -fsSL https://rpm.nodesource.com/setup_16.x | sudo bash -
sudo dnf install nodejs

# 3. 验证安装
python3 --version
node --version
npm --version
```

---

## 五、配置说明

### 5.1 环境变量配置

#### 主应用配置 (ciliAI/.env)

创建配置文件：`ciliAI/.env`

```bash
# 火山引擎密钥（必需）
# 从 https://console.volcengine.com/ 获取
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey
```

#### 配置说明

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| `VOLC_AK` | 是 | 火山引擎AccessKey ID | `AKLTZTI0MGNmMTJiZTFh...` |
| `VOLC_SK` | 是 | 火山引擎SecretAccessKey | `WldVelpHSTBaalE0Tm1R...` |

**获取方式**：

1. 访问火山引擎控制台：https://console.volcengine.com/
2. 登录或注册账号
3. 进入「访问密钥」创建AccessKey
4. 复制AK和SK到.env文件

### 5.2 端口配置

#### 默认端口

| 应用 | 端口 | 用途 | 配置文件 |
|------|------|------|----------|
| **主应用后端** | 5001 | 用户端API服务 | ciliAI/app.py |
| **主应用前端** | 5001 | 通过Flask静态文件服务 | - |
| **管理后台后端** | 5002 | 管理员API服务 | ruoyi/app.py |
| **管理后台前端** | 3001 | Vite开发服务器 | ruoyi/vite.config.js |

#### 修改端口

**修改主应用端口** (ciliAI/app.py)

```python
# 第1293行
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
    # 修改 port=5001 为所需端口
```

**修改管理后台后端端口** (ruoyi/app.py)

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
    # 修改 port=5002 为所需端口
```

**修改管理后台前端端口** (ruoyi/vite.config.js)

```javascript
server: {
    port: 3001,  // 修改为所需端口
    proxy: {
      '/api': {
        target: 'http://localhost:5002',
        changeOrigin: true
      }
    }
}
```

### 5.3 数据库配置

#### 数据库文件位置

- **路径**：`ciliAI/ciliAI.db`
- **类型**：SQLite 3
- **初始化**：首次启动时自动创建表结构

#### 备份数据库

```bash
# Windows
copy ciliAI\ciliAI.db ciliAI\ciliAI_backup_20260411.db

# Linux
cp ciliAI/ciliAI.db ciliAI/ciliAI_backup_$(date +%Y%m%d).db
```

#### 恢复数据库

```bash
# 停止服务后
# Windows
copy ciliAI\ciliAI_backup_20260411.db ciliAI\ciliAI.db

# Linux
cp ciliAI/ciliAI_backup_20260411.db ciliAI/ciliAI.db
```

---

## 六、部署步骤

### 6.1 部署方式概览

| 部署方式 | 适用场景 | 难度 | 推荐度 |
|----------|----------|------|--------|
| **Windows一键启动** | 开发测试 | ⭐ | ⭐⭐⭐⭐⭐ |
| **Linux手动部署** | 生产环境 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Docker容器部署** | 生产环境 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Docker Compose** | 生产环境 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

### 6.2 Windows 部署（开发/测试环境）

#### 方式一：使用启动脚本（推荐）

```powershell
# 1. 进入主应用目录
cd d:\ciliAI\ciliAI

# 2. 运行启动脚本
start.bat
```

**启动脚本功能**：

1. 检测Python环境
2. 创建Python虚拟环境（首次）
3. 安装Python依赖
4. 启动Flask服务
5. 显示访问地址

#### 方式二：手动启动（详细步骤）

```powershell
# 1. 进入项目目录
cd d:\ciliAI\ciliAI

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
.\venv\Scripts\activate

# 4. 安装Python依赖
pip install -r requirements.txt

# 5. 配置环境变量
# 创建 .env 文件并填入 VOLC_AK 和 VOLC_SK

# 6. 启动主应用（端口5001）
python app.py

# 7. 新开终端，启动管理后台后端（端口5002）
cd d:\ciliAI\ruoyi
python app.py

# 8. 新开终端，构建并启动管理后台前端
cd d:\ciliAI\ruoyi
npm install
npm run dev
```

---

### 6.3 Linux 手动部署（生产环境）

#### 步骤1：准备环境

```bash
# 1. 创建项目目录
sudo mkdir -p /var/www/ciliAI
cd /var/www/ciliAI

# 2. 上传代码（通过Git或SCP）
# Git方式：
git clone <repository_url> .

# 3. 安装系统依赖
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip nodejs npm nginx
```

#### 步骤2：配置主应用（ciliAI）

```bash
# 1. 进入主应用目录
cd /var/www/ciliAI/ciliAI

# 2. 创建虚拟环境
python3 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate

# 4. 安装Python依赖
pip install -r requirements.txt

# 5. 配置环境变量
nano .env
# 填入 VOLC_AK 和 VOLC_SK
```

#### 步骤3：配置管理后台（ruoyi）

```bash
# 1. 进入管理后台目录
cd /var/www/ciliAI/ruoyi

# 2. 安装Node依赖
npm install

# 3. 构建生产版本
npm run build

# 4. 配置环境变量（如果需要）
```

#### 步骤4：配置Nginx反向代理

```bash
# 1. 创建Nginx配置文件
sudo nano /etc/nginx/sites-available/ciliAI
```

**配置文件内容**：

```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名或IP

    # 主应用（端口5001）
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 管理后台（端口3001）
    location /admin {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 2. 启用配置
sudo ln -s /etc/nginx/sites-available/ciliAI /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 步骤5：使用PM2管理进程

```bash
# 1. 安装PM2
npm install -g pm2

# 2. 启动主应用
cd /var/www/ciliAI/ciliAI
source venv/bin/activate
pm2 start python --name "ciliAI-main" -- app.py

# 3. 启动管理后台后端
cd /var/www/ciliAI/ruoyi
pm2 start python --name "ciliAI-admin-api" -- app.py

# 4. 配置PM2开机自启
pm2 startup
pm2 save
```

---

### 6.4 Docker 容器部署（推荐生产环境）

#### 方式一：使用Dockerfile构建（仅主应用）

```bash
# 1. 进入主应用目录
cd ciliAI/ciliAI

# 2. 创建环境变量文件
cp .env.example .env
nano .env  # 编辑填入密钥

# 3. 构建镜像
docker build -t ciliAI-app:latest .

# 4. 运行容器
docker run -d \
  --name ciliAI \
  -p 5001:5001 \
  --env-file .env \
  --restart always \
  ciliAI-app:latest
```

#### 方式二：使用Docker Compose（推荐）

```bash
# 1. 进入主应用目录
cd ciliAI/ciliAI

# 2. 创建/编辑 docker-compose.yml
# 内容见下方

# 3. 创建环境变量文件
cp .env.example .env
nano .env  # 编辑填入密钥

# 4. 启动服务
docker-compose up -d

# 5. 查看日志
docker-compose logs -f
```

**docker-compose.yml 内容**：

```yaml
version: '3'
services:
  jimeng-ai:
    build: .
    ports:
      - "5001:5001"
    env_file:
      - .env
    volumes:
      - ./ciliAI.db:/app/ciliAI.db
    restart: always
    environment:
      - TZ=Asia/Shanghai
```

---

## 七、启动说明

### 7.1 启动顺序

**重要**：必须按以下顺序启动服务

```
1. 主应用后端（端口5001）
   ↓
2. 管理后台后端（端口5002）
   ↓
3. 管理后台前端（端口3001）
```

### 7.2 详细启动步骤

#### 第一步：启动主应用（用户端）

```bash
# Windows
cd d:\ciliAI\ciliAI
python app.py

# Linux
cd /var/www/ciliAI/ciliAI
source venv/bin/activate
python app.py
```

**预期输出**：

```
INFO:werkzeug:WARNING: This is a development server...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.1.100:5001
INFO:werkzeug:Press CTRL+C to quit
```

**验证**：访问 http://localhost:5001

#### 第二步：启动管理后台后端

```bash
# Windows
cd d:\ciliAI\ruoyi
python app.py

# Linux
cd /var/www/ciliAI/ruoyi
source venv/bin/activate
python app.py
```

**预期输出**：

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5002
 * Restarting with stat
```

**验证**：访问 http://localhost:5002/api/admin/login

#### 第三步：启动管理后台前端（开发模式）

```bash
cd d:\ciliAI\ruoyi
npm install  # 首次需要
npm run dev
```

**预期输出**：

```
VITE ready in 1153 ms
  Local:   http://localhost:3001/
  Network: use --host to expose
```

**验证**：访问 http://localhost:3001

### 7.3 生产环境构建（推荐）

对于生产环境，应预先构建前端：

```bash
# 1. 构建管理后台前端
cd d:\ciliAI\ruoyi
npm install
npm run build

# 2. 构建主应用前端（如果需要）
cd d:\ciliAI\ciliAI
npm install
npm run build

# 3. 使用Gunicorn替换Flask开发服务器
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

---

## 八、服务访问

### 8.1 访问地址汇总

| 服务 | 地址 | 用途 | 登录凭证 |
|------|------|------|----------|
| **主应用** | http://服务器IP:5001 | 用户端入口 | 8位邀请码 |
| **管理后台** | http://服务器IP:3001 | 管理员入口 | admin / admin123 |

### 8.2 访问验证

#### 主应用验证

1. 打开浏览器访问：http://localhost:5001
2. 应该显示"CiliAI学堂"登录页面
3. 输入8位邀请码登录
4. 登录成功后进入主界面

#### 管理后台验证

1. 打开浏览器访问：http://localhost:3001
2. 应该显示管理后台登录页面
3. 输入用户名：`admin`
4. 输入密码：`admin123`
5. 登录成功后进入管理界面

---

## 九、数据库结构

### 9.1 数据库表清单

| 表名 | 说明 | 主键 | 关键字段 |
|------|------|------|----------|
| `users` | 用户表 | id | invite_code, compute_power |
| `projects` | 项目表 | id | user_id, title, status |
| `generation_records` | 生成记录表 | id | user_id, project_id, type |
| `chat_messages` | 聊天消息表 | id | user_id, project_id, chat_id |
| `compute_power_logs` | 算力日志表 | id | user_id, operation_type |
| `invite_codes` | 邀请码表 | id | code, status, compute_power |

### 9.2 主要表结构

#### users 表

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invite_code TEXT UNIQUE NOT NULL,
    compute_power INTEGER DEFAULT 0,
    total_power_used INTEGER DEFAULT 0,
    nickname TEXT,
    avatar TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    last_active TIMESTAMP
);
```

#### projects 表

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    cover_image TEXT,
    status TEXT DEFAULT 'active',
    image_count INTEGER DEFAULT 0,
    chat_count INTEGER DEFAULT 0,
    total_power_used INTEGER DEFAULT 0,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

#### generation_records 表

```sql
CREATE TABLE generation_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    prompt TEXT,
    negative_prompt TEXT,
    image_url TEXT,
    image_width INTEGER,
    image_height INTEGER,
    image_size INTEGER,
    model_version TEXT,
    params TEXT,
    task_id TEXT,
    status TEXT DEFAULT 'completed',
    power_cost INTEGER DEFAULT 0,
    error_msg TEXT,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

#### invite_codes 表

```sql
CREATE TABLE invite_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'active',
    compute_power INTEGER DEFAULT 1000,
    max_uses INTEGER DEFAULT 1,
    current_uses INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY (created_by) REFERENCES users (id)
);
```

### 9.3 索引信息

| 表名 | 索引字段 | 类型 |
|------|----------|------|
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

---

## 十、运维管理

### 10.1 日常维护

#### 日志查看

```bash
# 主应用日志
# Windows - 控制台输出
python app.py

# Linux - PM2日志
pm2 logs ciliAI-main

# 管理后台日志
pm2 logs ciliAI-admin-api
```

#### 服务重启

```bash
# 重启主应用
pm2 restart ciliAI-main

# 重启管理后台
pm2 restart ciliAI-admin-api

# 查看服务状态
pm2 status
```

### 10.2 备份策略

#### 自动备份脚本

创建 `backup.sh`：

```bash
#!/bin/bash
# CiliAI - 每日备份脚本

BACKUP_DIR="/var/backups/ciliAI"
DB_FILE="/var/www/ciliAI/ciliAI/ciliAI.db"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
cp $DB_FILE $BACKUP_DIR/ciliAI_$DATE.db

# 压缩备份
cd $BACKUP_DIR
tar -czf ciliAI_backup_$DATE.tar.gz ciliAI_$DATE.db

# 删除30天前的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "备份完成: ciliAI_backup_$DATE.tar.gz"
```

```bash
# 添加定时任务
crontab -e
# 添加以下行（每天凌晨3点执行）
0 3 * * * /var/www/ciliAI/backup.sh >> /var/log/ciliAI_backup.log 2>&1
```

### 10.3 监控建议

#### 基础监控

- **进程监控**：确保app.py进程运行中
- **端口监控**：检查5001、5002、3001端口占用
- **磁盘监控**：数据库文件增长监控
- **内存监控**：Python进程内存使用

#### 推荐监控工具

| 工具 | 说明 | 成本 |
|------|------|------|
| **PM2 Plus** | PM2官方监控平台 | 免费/付费 |
| **Prometheus + Grafana** | 专业监控系统 | 免费 |
| **阿里云监控** | 云服务器自带 | 免费 |
| **腾讯云监控** | 云服务器自带 | 免费 |

---

## 十一、常见问题排查

### 11.1 服务无法启动

#### 问题1：端口被占用

**错误信息**：
```
OSError: [Errno 10048] Only one usage of each socket address is normally permitted
```

**解决方案**：

```bash
# Windows - 查找占用端口的进程
netstat -ano | findstr :5001
taskkill /PID <进程ID> /F

# Linux - 查找占用端口的进程
lsof -i :5001
kill -9 <进程ID>
```

#### 问题2：Python模块缺失

**错误信息**：
```
ModuleNotFoundError: No module named 'flask'
```

**解决方案**：

```bash
pip install -r requirements.txt
```

#### 问题3：火山引擎密钥无效

**错误信息**：
```
WARNING: VOLC_AK or VOLC_SK not found in environment variables!
```

**解决方案**：

1. 检查 `.env` 文件是否存在
2. 确认 `VOLC_AK` 和 `VOLC_SK` 格式正确
3. 验证密钥是否在火山引擎控制台有效

### 11.2 前端无法访问

#### 问题1：Vite启动失败

**错误信息**：
```
npm ERR! code ENOENT
```

**解决方案**：

```bash
cd d:\ciliAI\ruoyi
rm -rf node_modules package-lock.json
npm install
npm run dev
```

#### 问题2：API代理失败

**错误信息**：
```
Failed to proxy from localhost:3001 to http://localhost:5002
```

**解决方案**：

1. 确认管理后台后端已启动（端口5002）
2. 检查 `vite.config.js` 代理配置
3. 检查防火墙是否放行5002端口

### 11.3 数据库问题

#### 问题1：数据库锁定

**错误信息**：
```
database is locked
```

**解决方案**：

1. 检查是否有其他进程访问数据库
2. 重启相关Python进程
3. 确保SQLite并发连接配置正确

#### 问题2：表不存在

**错误信息**：
```
no such table: users
```

**解决方案**：

1. 检查数据库文件是否存在
2. 删除数据库文件重新初始化
3. 重启应用自动创建表结构

### 11.4 性能问题

#### 问题1：响应缓慢

**可能原因**：

- 数据库查询性能差
- 图像生成任务阻塞
- 服务器资源不足

**解决方案**：

1. 检查服务器CPU和内存使用率
2. 优化数据库索引
3. 添加缓存层
4. 考虑升级服务器配置

---

## 十二、安全建议

### 12.1 防火墙配置

```bash
# Ubuntu/Debian - ufw
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# CentOS/RHEL - firewalld
sudo firewall-cmd --permanent --add-port=5001/tcp
sudo firewall-cmd --permanent --add-port=5002/tcp
sudo firewall-cmd --permanent --add-port=3001/tcp
sudo firewall-cmd --reload
```

### 12.2 HTTPS配置（生产环境）

```bash
# 使用Let's Encrypt免费证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

### 12.3 密钥管理

- **定期更换**火山引擎密钥
- 使用**环境变量**而非代码硬编码
- 敏感配置文件加入`.gitignore`
- 限制`.env`文件权限：`chmod 600 .env`

---

## 十三、联系支持

### 13.1 获取帮助

- **文档**：参考本部署指南
- **日志**：查看应用运行日志
- **社区**：加入CiliAI技术交流群

### 13.2 问题报告

报告问题时请提供：

1. 服务器操作系统和版本
2. 错误日志完整内容
3. 问题复现步骤
4. 已尝试的解决方案

---

## 附录

### 附录A：快速命令参考

```bash
# 启动主应用
python app.py

# 启动管理后台后端
python app.py

# 启动管理后台前端
npm run dev

# 构建前端
npm run build

# 安装Python依赖
pip install -r requirements.txt

# 安装Node依赖
npm install

# 查看端口占用
netstat -ano | findstr :5001

# 重启PM2服务
pm2 restart all

# 查看PM2日志
pm2 logs
```

### 附录B：关键文件路径

| 文件 | 路径 | 说明 |
|------|------|------|
| 主应用入口 | ciliAI/app.py | Flask主应用 |
| 管理后台入口 | ruoyi/app.py | 管理后台API |
| 数据库文件 | ciliAI/ciliAI.db | SQLite数据库 |
| 环境配置 | ciliAI/.env | 环境变量 |
| 主应用依赖 | ciliAI/requirements.txt | Python依赖 |
| 管理后台依赖 | ruoyi/package.json | Node依赖 |

### 附录C：版本信息

| 组件 | 版本 |
|------|------|
| CiliAI平台 | 0.0.6 |
| Vue.js (主应用) | 3.5.13 |
| Vue.js (管理后台) | 3.4.21 |
| Element Plus (主应用) | 2.8.4 |
| Element Plus (管理后台) | 2.6.1 |
| Flask | 最新版 |
| Vite (主应用) | 6.0.5 |
| Vite (管理后台) | 5.1.6 |

---

**文档版本**：1.0  
**最后更新**：2026-04-11  
**维护者**：CiliAI技术团队



