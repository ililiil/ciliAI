# 方塘AI短剧平台 - 项目部署说明文档

## 文档信息

- **项目名称**：方塘AI短剧平台
- **版本**：0.0.6
- **编写日期**：2026-04-12
- **文档用途**：运维团队部署指南

---

## 目录

1. [部署架构概述](#1-部署架构概述)
2. [环境要求](#2-环境要求)
3. [用户应用端部署](#3-用户应用端部署)
4. [管理后台端部署](#4-管理后台端部署)
5. [数据库部署](#5-数据库部署)
6. [后端服务部署](#6-后端服务部署)
7. [配置管理](#7-配置管理)
8. [部署验证](#8-部署验证)
9. [运维监控](#9-运维监控)
10. [故障排查](#10-故障排查)
11. [备份与恢复](#11-备份与恢复)
12. [运维对接指南](#12-运维对接指南)

---

## 1. 部署架构概述

### 1.1 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        互联网用户                                │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        负载均衡器                                 │
│                    (Nginx / 云负载均衡)                           │
└──────────┬─────────────────────────────────┬────────────────────┘
           │                                 │
           ▼                                 ▼
┌─────────────────────┐           ┌─────────────────────────┐
│   用户应用端集群      │           │    管理后台端集群          │
│  ┌───────────────┐  │           │  ┌───────────────────┐  │
│  │ 服务器1:5001   │  │           │  │  服务器1:5002/3001 │  │
│  │ 服务器2:5001   │  │           │  │  服务器2:5002/3001  │  │
│  └───────────────┘  │           │  └───────────────────┘  │
└──────────┬──────────┘           └──────────┬──────────────┘
           │                                 │
           └─────────────┬───────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        数据库服务器                               │
│                   ┌─────────────────┐                           │
│                   │  SQLite数据库    │                           │
│                   │  fangtang.db    │                           │
│                   └─────────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     外部服务依赖                                  │
│  ┌────────────────┐     ┌────────────────┐                     │
│  │  火山引擎AI服务 │     │   Dify API     │                     │
│  │  Visual API   │     │  (可选)        │                     │
│  └────────────────┘     └────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 部署模式

| 部署模式 | 适用场景 | 复杂度 | 推荐度 | 说明 |
|---------|---------|-------|-------|------|
| **单机部署** | 开发测试 | ⭐ | ⭐⭐⭐⭐⭐ | 所有组件部署在一台服务器 |
| **Docker部署** | 生产环境 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 使用Docker容器化部署 |
| **集群部署** | 大规模生产 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 多服务器负载均衡 |
| **K8s部署** | 企业级生产 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Kubernetes容器编排 |

### 1.3 组件依赖关系

```
火山引擎AI服务（外部依赖）
         │
         ▼
┌─────────────────────┐
│   用户应用后端API     │ ◀─── 依赖 ───► ┌────────────────────┐
│   (端口: 5001)       │                │   SQLite数据库      │
└──────────┬──────────┘                │   fangtang.db     │
           │                           └────────────────────┘
           │
           ▼
┌─────────────────────┐
│   管理后台后端API     │
│   (端口: 5002)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   管理后台前端Web    │
│   (端口: 3001)       │
└─────────────────────┘
```

---

## 2. 环境要求

### 2.1 服务器配置要求

#### 开发测试环境（单机）

| 资源 | 最低配置 | 推荐配置 |
|-----|---------|---------|
| **CPU** | 2核心 | 4核心 |
| **内存** | 4GB | 8GB |
| **磁盘** | 20GB | 50GB |
| **带宽** | 1Mbps | 5Mbps |

#### 生产环境（单机）

| 资源 | 最低配置 | 推荐配置 |
|-----|---------|---------|
| **CPU** | 4核心 | 8核心 |
| **内存** | 8GB | 16GB |
| **磁盘** | 50GB | 100GB SSD |
| **带宽** | 5Mbps | 10Mbps |

#### 生产环境（集群）

| 资源 | 最低配置 | 推荐配置 |
|-----|---------|---------|
| **应用服务器** | 2台 × 4核8GB | 4台 × 8核16GB |
| **数据库服务器** | 1台 × 4核16GB | 1台 × 8核32GB |
| **磁盘** | 100GB | 500GB SSD |
| **带宽** | 10Mbps | 100Mbps |

### 2.2 操作系统要求

| 操作系统 | 版本要求 | 兼容性 | 说明 |
|---------|---------|-------|------|
| **Ubuntu** | 20.04 LTS | ✅ 官方支持 | 推荐生产环境使用 |
| **CentOS** | 8.0+ | ✅ 官方支持 | 企业常用系统 |
| **Debian** | 11+ | ✅ 官方支持 | 稳定可靠 |
| **Windows Server** | 2019+ | ⚠️ 兼容 | 仅用于开发测试 |
| **macOS** | 12+ | ⚠️ 兼容 | 仅用于开发测试 |

### 2.3 软件依赖

#### 必需软件

| 软件 | 版本要求 | 用途 | 安装命令 |
|-----|---------|------|---------|
| **Python** | 3.9+ | 后端运行环境 | 见下方各系统安装命令 |
| **Node.js** | 16 LTS+ | 前端构建工具 | 见下方各系统安装命令 |
| **npm** | 8+ | 包管理器 | 随Node安装 |
| **Git** | 2.0+ | 版本控制 | 可选 |

#### 可选软件

| 软件 | 版本要求 | 用途 | 推荐度 |
|-----|---------|------|-------|
| **Docker** | 20.10+ | 容器化部署 | ⭐⭐⭐⭐⭐ |
| **Docker Compose** | 2.0+ | 容器编排 | ⭐⭐⭐⭐⭐ |
| **PM2** | 5.0+ | 进程管理 | ⭐⭐⭐⭐ |
| **Nginx** | 1.18+ | 反向代理 | ⭐⭐⭐⭐ |
| **Gunicorn** | 20.0+ | WSGI服务器 | ⭐⭐⭐ |

#### 各系统安装命令

**Ubuntu / Debian**：

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装Python
sudo apt install -y python3.9 python3.9-venv python3-pip

# 安装Node.js 16
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs

# 安装Docker
curl -fsSL https://get.docker.com | sudo -E bash -
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.0.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装PM2
sudo npm install -g pm2

# 验证安装
python3 --version  # 应该显示 Python 3.9.x
node --version     # 应该显示 v16.x.x
docker --version   # 应该显示 Docker version 20.x.x
pm2 --version      # 应该显示 5.x.x
```

**CentOS / RHEL**：

```bash
# 更新系统
sudo dnf update -y

# 安装Python
sudo dnf install -y python3.9 python3.9-venv python3-pip

# 安装Node.js 16
curl -fsSL https://rpm.nodesource.com/setup_16.x | sudo bash -
sudo dnf install -y nodejs

# 安装Docker
sudo dnf install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# 安装Docker Compose
sudo dnf install -y docker-compose

# 安装PM2
sudo npm install -g pm2

# 验证安装
python3 --version
node --version
docker --version
```

**Windows**：

```powershell
# 安装Python 3.9+
# 访问 https://www.python.org/downloads/
# 下载安装包并运行
# 勾选 "Add Python to PATH"

# 安装Node.js 16 LTS
# 访问 https://nodejs.org/
# 下载并运行安装包

# 安装Docker Desktop
# 访问 https://www.docker.com/products/docker-desktop
# 下载并运行安装包

# 验证安装
python --version
node --version
docker --version
```

### 2.4 网络要求

| 配置项 | 要求 | 说明 |
|-------|------|------|
| **公网IP** | 必须 | 用于外部访问 |
| **防火墙端口** | 开放5001, 5002, 3001 | 应用端口 |
| **防火墙端口** | 开放80, 443 | Web端口 |
| **出站规则** | 允许HTTPS | 访问火山引擎API |
| **DNS解析** | 配置 | 域名解析（可选） |

---

## 3. 用户应用端部署

### 3.1 部署架构

```
┌─────────────────────────────────────────┐
│            Nginx反向代理                 │
│         (端口: 80/443)                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Gunicorn WSGI服务器              │
│         (端口: 5001)                     │
│         worker数量: 4                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│           Flask应用                     │
│         (Python进程)                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│           SQLite数据库                   │
│         (fangtang.db)                   │
└─────────────────────────────────────────┘
```

### 3.2 部署前准备

#### 3.2.1 创建部署目录

```bash
# 创建项目目录
sudo mkdir -p /var/www/fangtang
sudo chown -R $USER:$USER /var/www/fangtang

# 进入项目目录
cd /var/www/fangtang
```

#### 3.2.2 获取代码

**方式一：Git克隆**

```bash
# 如果使用Git仓库
git clone <repository_url> /var/www/fangtang
```

**方式二：SCP上传**

```bash
# 在本地执行
scp -r ./fangtang user@server:/tmp/
ssh user@server "mv /tmp/fangtang /var/www/"
```

#### 3.2.3 配置环境变量

```bash
# 进入用户应用端目录
cd /var/www/fangtang/fangtang

# 创建环境变量文件
cp .env.example .env

# 编辑配置文件
nano .env
```

**配置文件内容**：

```bash
# 火山引擎密钥（必需）
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey

# 可选配置
FLASK_ENV=production
LOG_LEVEL=INFO
```

### 3.3 Docker部署（推荐）

#### 3.3.1 创建Dockerfile

**文件位置**：`fangtang/Dockerfile`

```dockerfile
# 前端构建阶段
FROM node:16-alpine as frontend
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 后端运行阶段
FROM python:3.9-slim
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# 复制前端构建产物
COPY --from=frontend /app/dist ./dist

# 复制后端代码
COPY app.py .
COPY requirements.txt .
COPY .env .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 5001

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "--timeout", "120", "app:app"]
```

#### 3.3.2 创建docker-compose.yml

**文件位置**：`fangtang/docker-compose.yml`

```yaml
version: '3.8'

services:
  fangtang:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fangtang-app
    ports:
      - "5001:5001"
    volumes:
      - ./data:/app/data
      - ./fangtang.db:/app/fangtang.db
      - ./logs:/app/logs
    env_file:
      - .env
    environment:
      - TZ=Asia/Shanghai
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5001/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - fangtang-network

networks:
  fangtang-network:
    driver: bridge
```

#### 3.3.3 构建和启动

```bash
# 进入用户应用端目录
cd /var/www/fangtang/fangtang

# 构建镜像
docker build -t fangtang-app:latest .

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 3.4 手动部署

#### 3.4.1 安装Python依赖

```bash
# 进入目录
cd /var/www/fangtang/fangtang

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

#### 3.4.2 构建前端（可选）

如果使用Nginx提供静态文件：

```bash
# 安装Node依赖
npm install

# 构建生产版本
npm run build

# 将构建产物移到正确位置
# dist目录应该与app.py在同一目录
```

#### 3.4.3 配置Gunicorn

创建启动脚本 `start_gunicorn.sh`：

```bash
#!/bin/bash
# Gunicorn启动脚本

NAME="fangtang-app"
DIR="/var/www/fangtang/fangtang"
USER="www-data"
GROUP="www-data"

# 激活虚拟环境
cd $DIR
source venv/bin/activate

# 启动Gunicorn
exec gunicorn \
    --name $NAME \
    --workers 4 \
    --bind 0.0.0.0:5001 \
    --timeout 120 \
    --access-logfile /var/log/fangtang/access.log \
    --error-logfile /var/log/fangtang/error.log \
    --log-level info \
    app:app
```

```bash
# 添加执行权限
chmod +x start_gunicorn.sh
```

#### 3.4.4 使用PM2管理

```bash
# 安装PM2（如果未安装）
npm install -g pm2

# 启动应用
cd /var/www/fangtang/fangtang
pm2 start start_gunicorn.sh --name fangtang-main

# 保存PM2配置
pm2 save

# 设置开机自启
pm2 startup
```

### 3.5 Nginx反向代理配置

创建Nginx配置文件 `/etc/nginx/sites-available/fangtang`：

```nginx
upstream fangtang_backend {
    server 127.0.0.1:5001;
    keepalive 32;
}

server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名或IP
    client_max_body_size 100M;

    # 访问日志
    access_log /var/log/nginx/fangtang_access.log;
    error_log /var/log/nginx/fangtang_error.log;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # 主应用
    location / {
        proxy_pass http://fangtang_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # WebSocket支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 静态文件缓存（可选）
    location /assets/ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/fangtang /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3.6 部署验证

```bash
# 检查容器/进程状态
docker-compose ps
# 或
pm2 status

# 检查端口监听
netstat -tlnp | grep 5001

# 测试API
curl -X POST http://localhost:5001/api/verify-invite-code \
  -H "Content-Type: application/json" \
  -d '{"invite_code":"111111"}'

# 访问主页
curl http://localhost:5001/ | head -20
```

---

## 4. 管理后台端部署

### 4.1 部署架构

```
┌─────────────────────────────────────────┐
│            Nginx反向代理                 │
│         (端口: 80/443)                  │
│         /admin -> 3001                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Vite开发服务器                   │
│         (端口: 3001)                     │
│         或 Nginx静态文件服务               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Flask API服务器                  │
│         (端口: 5002)                     │
│         worker数量: 2                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│           SQLite数据库                   │
│         (共享用户端数据库)                │
└─────────────────────────────────────────┘
```

### 4.2 部署前准备

```bash
# 进入管理后台目录
cd /var/www/fangtang/fadmin

# 创建上传目录
mkdir -p uploads
chmod 755 uploads
```

### 4.3 Docker部署

#### 4.3.1 创建Dockerfile

**文件位置**：`fadmin/Dockerfile`

```dockerfile
# 前端构建阶段
FROM node:16-alpine as frontend
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 后端运行阶段
FROM python:3.9-slim
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 复制前端构建产物
COPY --from=frontend /app/dist ./templates

# 复制后端代码
COPY app.py .

# 暴露端口
EXPOSE 5002

# 启动命令
CMD ["python", "app.py"]
```

#### 4.3.2 创建docker-compose.yml

**文件位置**：`fadmin/docker-compose.yml`

```yaml
version: '3.8'

services:
  fadmin-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fadmin-api
    ports:
      - "5002:5002"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - TZ=Asia/Shanghai
    restart: always
    networks:
      - fangtang-network

networks:
  fangtang-network:
    external: true
```

#### 4.3.3 构建和启动

```bash
# 进入管理后台目录
cd /var/www/fangtang/fadmin

# 构建镜像
docker build -t fadmin-api:latest .

# 启动服务
docker-compose up -d
```

### 4.4 手动部署

#### 4.4.1 安装依赖

```bash
# 进入目录
cd /var/www/fangtang/fadmin

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install flask flask-cors python-dotenv

# 安装前端依赖
npm install
```

#### 4.4.2 构建前端

```bash
# 构建生产版本
npm run build

# 构建产物在dist目录，需要复制到templates目录
cp -r dist templates
```

#### 4.4.3 启动服务

```bash
# 启动后端API
pm2 start python --name "fadmin-api" -- app.py

# 启动前端（使用Nginx或Vite）
# 方式1：Nginx（推荐生产环境）
# 配置Nginx指向templates目录

# 方式2：Vite预览（仅开发环境）
npm run preview
```

### 4.5 Nginx配置

创建Nginx配置文件 `/etc/nginx/sites-available/fadmin`：

```nginx
upstream fadmin_backend {
    server 127.0.0.1:5002;
    keepalive 16;
}

server {
    listen 80;
    server_name admin.your_domain.com;  # 替换为你的域名
    client_max_body_size 50M;

    # 管理后台API
    location /api/ {
        proxy_pass http://fadmin_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 管理后台静态文件
    location / {
        root /var/www/fangtang/fadmin/templates;
        try_files $uri $uri/ /index.html;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/fadmin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4.6 部署验证

```bash
# 检查API状态
curl http://localhost:5002/

# 测试登录接口
curl -X POST http://localhost:5002/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 访问管理后台主页
curl http://localhost:3001/
```

---

## 5. 数据库部署

### 5.1 数据库配置

#### 5.1.1 数据库文件位置

| 环境 | 文件路径 |
|-----|---------|
| **开发环境** | `d:\fangtang\fangtang\fangtang.db` |
| **生产环境** | `/var/www/fangtang/fangtang/fangtang.db` |
| **Docker环境** | `/app/fangtang.db`（容器内） |

#### 5.1.2 数据库连接配置

**用户应用端**（`fangtang/app.py` 第23行）：

```python
DATABASE = 'fangtang.db'  # 相对路径
```

**管理后台端**（`fadmin/app.py` 第18行）：

```python
DATABASE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'fangtang',
    'fangtang.db'
)
```

### 5.2 数据库初始化

#### 5.2.1 自动初始化

首次启动应用时自动创建：

```bash
# 启动应用
python app.py

# 查看日志确认初始化成功
tail -f /var/log/fangtang/app.log
```

预期输出：

```
[INFO] Starting database initialization...
[INFO] Creating table: users
[INFO] Creating table: projects
[INFO] Creating table: generation_records
[INFO] Creating table: chat_messages
[INFO] Creating table: compute_power_logs
[INFO] Creating table: invite_codes
[INFO] Creating table: ip_works
[INFO] Creating indexes...
[INFO] Inserting default invite codes...
[INFO] Database initialization completed
```

#### 5.2.2 手动初始化

如果需要重置数据库：

```bash
# 步骤1：停止应用
pm2 stop all
# 或
docker-compose down

# 步骤2：备份现有数据库
cp fangtang.db fangtang_backup_$(date +%Y%m%d).db

# 步骤3：删除数据库文件
rm fangtang.db

# 步骤4：重启应用
pm2 restart all
# 或
docker-compose up -d

# 步骤5：验证
sqlite3 fangtang.db ".tables"
```

### 5.3 数据库备份

#### 5.3.1 手动备份

```bash
# 备份命令
cp fangtang.db fangtang_backup_$(date +%Y%m%d_%H%M%S).db

# 压缩备份
tar -czf fangtang_backup_$(date +%Y%m%d).tar.gz fangtang.db
```

#### 5.3.2 自动备份脚本

创建备份脚本 `/var/scripts/backup_fangtang.sh`：

```bash
#!/bin/bash
# 方塘AI数据库备份脚本

# 配置
BACKUP_DIR="/var/backups/fangtang"
DB_FILE="/var/www/fangtang/fangtang/fangtang.db"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_DAYS=30

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行备份
echo "[$(date)] Starting backup..."
cp $DB_FILE $BACKUP_DIR/fangtang_$DATE.db

# 压缩备份
tar -czf $BACKUP_DIR/fangtang_$DATE.tar.gz -C $(dirname $DB_FILE) $(basename $DB_FILE)

# 删除原文件备份（保留压缩包）
rm $BACKUP_DIR/fangtang_$DATE.db

# 清理过期备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +$KEEP_DAYS -delete

# 上传到远程存储（可选）
# aws s3 cp $BACKUP_DIR/fangtang_$DATE.tar.gz s3://your-bucket/backups/

echo "[$(date)] Backup completed: fangtang_$DATE.tar.gz"
```

```bash
# 添加执行权限
chmod +x /var/scripts/backup_fangtang.sh
```

#### 5.3.3 设置定时任务

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天凌晨3点执行）
0 3 * * * /var/scripts/backup_fangtang.sh >> /var/log/fangtang_backup.log 2>&1

# 保存退出
```

### 5.4 数据库恢复

#### 5.4.1 从备份恢复

```bash
# 步骤1：停止应用
pm2 stop all

# 步骤2：备份当前数据库
cp fangtang.db fangtang_current.db

# 步骤3：恢复备份
tar -xzf /path/to/fangtang_backup_20260412_030000.tar.gz

# 步骤4：验证数据
sqlite3 fangtang.db "SELECT COUNT(*) FROM users;"

# 步骤5：重启应用
pm2 restart all
```

#### 5.4.2 从远程备份恢复

```bash
# 从S3下载备份
aws s3 cp s3://your-bucket/backups/fangtang_20260412.tar.gz /tmp/

# 解压
tar -xzf /tmp/fangtang_20260412.tar.gz -C /var/www/fangtang/fangtang/

# 重启
pm2 restart all
```

### 5.5 数据库性能优化

#### 5.5.1 定期 VACUUM

SQLite需要定期维护：

```bash
# 连接数据库执行VACUUM
sqlite3 fangtang.db "VACUUM;"
```

#### 5.5.2 分析查询

```bash
# 开启查询分析
sqlite3 fangtang.db "EXPLAIN QUERY PLAN SELECT * FROM users WHERE invite_code = '12345678';"
```

---

## 6. 后端服务部署

### 6.1 服务清单

| 服务名称 | 类型 | 端口 | 技术栈 | 启动方式 |
|---------|------|------|--------|---------|
| **fangtang-main** | API服务 | 5001 | Flask + Gunicorn | Docker/PM2 |
| **fadmin-api** | API服务 | 5002 | Flask | Docker/PM2 |
| **fadmin-frontend** | Web服务 | 3001 | Vite/Nginx | Nginx |

### 6.2 使用PM2管理服务

#### 6.2.1 安装PM2

```bash
# 全局安装
npm install -g pm2

# 验证
pm2 --version
```

#### 6.2.2 启动服务

**用户应用后端**：

```bash
cd /var/www/fangtang/fangtang
source venv/bin/activate

pm2 start gunicorn \
  --name fangtang-main \
  --workers 4 \
  --bind 0.0.0.0:5001 \
  --timeout 120 \
  --access-logfile /var/log/fangtang/access.log \
  --error-logfile /var/log/fangtang/error.log \
  -- app:app
```

**管理后台后端**：

```bash
cd /var/www/fangtang/fadmin
source venv/bin/activate

pm2 start python \
  --name fadmin-api \
  -- app.py
```

#### 6.2.3 PM2常用命令

```bash
# 查看服务状态
pm2 status

# 查看日志
pm2 logs fangtang-main
pm2 logs fadmin-api

# 重启服务
pm2 restart fangtang-main
pm2 restart fadmin-api

# 重启所有服务
pm2 restart all

# 停止服务
pm2 stop fangtang-main

# 删除服务
pm2 delete fangtang-main

# 保存PM2配置
pm2 save

# 设置开机自启
pm2 startup
```

#### 6.2.4 PM2配置文件

创建ecosystem配置文件 `ecosystem.config.js`：

```javascript
module.exports = {
  apps: [
    {
      name: 'fangtang-main',
      script: 'venv/bin/gunicorn',
      args: '--bind 0.0.0.0:5001 --workers 4 --timeout 120 app:app',
      cwd: '/var/www/fangtang/fangtang',
      interpreter: 'none',
      env: {
        NODE_ENV: 'production',
        PYTHONUNBUFFERED: '1'
      },
      error_file: '/var/log/fangtang/fangtang-error.log',
      out_file: '/var/log/fangtang/fangtang-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    },
    {
      name: 'fadmin-api',
      script: 'venv/bin/python',
      args: 'app.py',
      cwd: '/var/www/fangtang/fadmin',
      interpreter: 'none',
      env: {
        NODE_ENV: 'production',
        PYTHONUNBUFFERED: '1'
      },
      error_file: '/var/log/fangtang/fadmin-error.log',
      out_file: '/var/log/fangtang/fadmin-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M'
    }
  ]
};
```

```bash
# 使用配置文件启动
pm2 start ecosystem.config.js

# 保存配置
pm2 save

# 设置开机自启
pm2 startup
```

### 6.3 使用Systemd管理服务

创建systemd服务文件 `/etc/systemd/system/fangtang-main.service`：

```ini
[Unit]
Description=Fangtang AI Main Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/fangtang/fangtang
Environment="PATH=/var/www/fangtang/fangtang/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/var/www/fangtang/fangtang/venv/bin/gunicorn \
    --bind 0.0.0.0:5001 \
    --workers 4 \
    --timeout 120 \
    --access-logfile /var/log/fangtang/access.log \
    --error-logfile /var/log/fangtang/error.log \
    --daemon \
    app:app
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 重新加载systemd
sudo systemctl daemon-reload

# 启用服务
sudo systemctl enable fangtang-main

# 启动服务
sudo systemctl start fangtang-main

# 查看状态
sudo systemctl status fangtang-main

# 重启服务
sudo systemctl restart fangtang-main
```

---

## 7. 配置管理

### 7.1 环境变量配置

#### 7.1.1 用户应用端配置

**文件**：`fangtang/.env`

```bash
# 火山引擎AccessKey（必需）
VOLC_AK=你的AccessKeyID

# 火山引擎SecretKey（必需）
VOLC_SK=你的SecretAccessKey

# Flask环境（生产环境设为production）
FLASK_ENV=production

# 日志级别
LOG_LEVEL=INFO

# 数据库路径（可选）
DATABASE_PATH=fangtang.db
```

#### 7.1.2 管理后台端配置

管理后台端使用共享数据库，无需额外环境变量。

### 7.2 配置文件修改

#### 7.2.1 端口修改

**用户应用端**（`fangtang/app.py`）：

```python
# 第1353行
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
    # 修改 port=5001 为所需端口
```

**管理后台后端**（`fadmin/app.py`）：

```python
# 第398行
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
    # 修改 port=5002 为所需端口
```

**管理后台前端**（`fadmin/vite.config.js`）：

```javascript
server: {
    port: 3001,  // 修改为所需端口
    // ...
}
```

#### 7.2.2 CORS配置

如果需要允许特定域名访问：

```python
# fangtang/app.py
from flask_cors import CORS

# 允许所有域名
CORS(app)

# 或允许特定域名
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://example.com", "http://www.example.com"]
    }
})
```

### 7.3 配置验证

```bash
# 验证Python环境变量
cd /var/www/fangtang/fangtang
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'VOLC_AK: {os.getenv(\"VOLC_AK\")}')"

# 验证Flask配置
python -c "from app import app; print(f'Debug: {app.debug}')"
```

---

## 8. 部署验证

### 8.1 验证清单

| 序号 | 验证项 | 验证方法 | 预期结果 | 状态 |
|-----|-------|---------|---------|------|
| 1 | 用户应用后端运行 | `curl http://localhost:5001/` | 返回HTML页面 | ☐ |
| 2 | 用户应用API | `curl http://localhost:5001/api/stats?invite_code=test` | 返回JSON响应 | ☐ |
| 3 | 管理后台后端运行 | `curl http://localhost:5002/` | 返回HTML页面 | ☐ |
| 4 | 管理后台登录 | `curl -X POST http://localhost:5002/api/admin/login` | 返回token | ☐ |
| 5 | 管理后台前端 | `curl http://localhost:3001/` | 返回HTML页面 | ☐ |
| 6 | 数据库连接 | `sqlite3 fangtang.db "SELECT COUNT(*) FROM users;"` | 返回数字 | ☐ |
| 7 | 邀请码验证 | 使用默认邀请码登录 | 登录成功 | ☐ |
| 8 | Nginx代理 | `curl http://localhost/admin/` | 访问管理后台 | ☐ |
| 9 | 日志文件 | 检查 `/var/log/fangtang/` | 无错误日志 | ☐ |
| 10 | 防火墙 | 检查端口开放 | 5001/5002/3001开放 | ☐ |

### 8.2 验证脚本

创建验证脚本 `/var/scripts/verify_deployment.sh`：

```bash
#!/bin/bash
# 方塘AI部署验证脚本

echo "=========================================="
echo "   方塘AI短剧平台 - 部署验证脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 验证函数
check_service() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "检查 $name... "
    response=$(curl -s -o /dev/null -w "%{http_code}" $url)
    
    if [ "$response" == "$expected" ]; then
        echo -e "${GREEN}✓ 通过${NC}"
        return 0
    else
        echo -e "${RED}✗ 失败 (HTTP $response)${NC}"
        return 1
    fi
}

# 验证用户应用后端
check_service "用户应用后端" "http://localhost:5001/" "200"

# 验证管理后台后端
check_service "管理后台后端" "http://localhost:5002/" "200"

# 验证管理后台前端
check_service "管理后台前端" "http://localhost:3001/" "200"

# 验证数据库
echo -n "检查数据库... "
if sqlite3 /var/www/fangtang/fangtang/fangtang.db "SELECT COUNT(*) FROM users;" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 通过${NC}"
else
    echo -e "${RED}✗ 失败${NC}"
fi

# 验证邀请码
echo -n "检查默认邀请码... "
response=$(curl -s -X POST http://localhost:5001/api/verify-invite-code \
    -H "Content-Type: application/json" \
    -d '{"invite_code":"111111"}')
    
if echo $response | grep -q "success"; then
    echo -e "${GREEN}✓ 通过${NC}"
else
    echo -e "${RED}✗ 失败${NC}"
fi

echo ""
echo "=========================================="
echo "验证完成"
echo "=========================================="
```

```bash
chmod +x /var/scripts/verify_deployment.sh
/var/scripts/verify_deployment.sh
```

---

## 9. 运维监控

### 9.1 日志管理

#### 9.1.1 日志文件位置

| 日志类型 | 路径 | 说明 |
|---------|------|------|
| **应用日志** | `/var/log/fangtang/access.log` | 访问日志 |
| **错误日志** | `/var/log/fangtang/error.log` | 错误日志 |
| **PM2日志** | `~/.pm2/logs/` | PM2进程日志 |
| **Docker日志** | `docker logs <container>` | Docker容器日志 |

#### 9.1.2 日志配置

**Gunicorn日志配置**：

```python
# 在启动命令中添加
--access-logfile /var/log/fangtang/access.log
--error-logfile /var/log/fangtang/error.log
--log-level info
```

**Docker日志配置**（`docker-compose.yml`）：

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 9.2 监控指标

#### 9.2.1 基础监控

| 指标 | 监控方法 | 阈值 | 处理方式 |
|-----|---------|------|---------|
| **服务可用性** | HTTP健康检查 | 失败则告警 | 重启服务 |
| **CPU使用率** | 系统监控 | >80%持续5分钟 | 扩容或优化 |
| **内存使用率** | 系统监控 | >85% | 检查内存泄漏 |
| **磁盘使用率** | 系统监控 | >90% | 清理或扩容 |
| **响应时间** | API监控 | >3秒 | 优化或扩容 |

#### 9.2.2 业务监控

| 指标 | 计算方法 | 告警条件 |
|-----|---------|---------|
| **日活用户** | COUNT(DISTINCT user_id) WHERE login_date = today | 异常下降 |
| **日生成数** | COUNT(*) FROM generation_records WHERE date = today | 异常下降 |
| **算力消耗** | SUM(power_cost) WHERE date = today | 异常上升 |
| **失败率** | COUNT(status='failed') / COUNT(*) | >10% |

### 9.3 监控工具推荐

| 工具 | 类型 | 费用 | 说明 |
|-----|------|------|------|
| **PM2 Plus** | 应用监控 | 免费/付费 | PM2官方监控平台 |
| **Prometheus + Grafana** | 基础设施监控 | 免费 | 功能强大 |
| **阿里云监控** | 云监控 | 免费 | 云服务器自带 |
| **Datadog** | 应用监控 | 付费 | 企业级监控 |
| **Sentry** | 错误追踪 | 免费/付费 | 错误收集 |

### 9.4 告警配置

使用PM2 Plus告警示例：

```bash
# 安装PM2 Plus
pm2 link <key> <secret>

# 添加告警规则
pm2 alert <app-name>
```

---

## 10. 故障排查

### 10.1 常见问题

#### 问题1：服务无法启动

**症状**：运行启动命令后立即退出

**排查步骤**：

1. 检查端口占用
```bash
netstat -tlnp | grep 5001
```

2. 检查日志
```bash
pm2 logs fangtang-main
docker logs fangtang-app
```

3. 检查环境变量
```bash
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('VOLC_AK'))"
```

**解决方案**：

- 终止占用端口的进程
- 修复日志中的错误
- 配置缺失的环境变量

#### 问题2：数据库锁定

**症状**：`database is locked` 错误

**排查步骤**：

1. 检查是否有其他进程访问数据库
```bash
lsof /var/www/fangtang/fangtang/fangtang.db
```

2. 检查是否有未关闭的数据库连接

**解决方案**：

```bash
# 停止所有应用
pm2 stop all

# 重启应用
pm2 restart all
```

#### 问题3：API响应缓慢

**症状**：页面加载超过5秒

**排查步骤**：

1. 检查服务器资源
```bash
top
htop
df -h
```

2. 检查数据库性能
```bash
sqlite3 fangtang.db "PRAGMA integrity_check;"
```

3. 检查慢查询
```bash
# 在Python代码中添加日志
import time
start = time.time()
# 执行查询
print(f"Query took {time.time() - start}s")
```

**解决方案**：

- 扩容服务器资源
- 优化数据库查询
- 添加缓存层

#### 问题4：火山引擎API调用失败

**症状**：`Failed to call Visual API` 错误

**排查步骤**：

1. 检查网络连通性
```bash
curl -v https://visual.volcengine.com
```

2. 检查密钥配置
```bash
echo $VOLC_AK
echo $VOLC_SK
```

3. 检查API余额
```bash
# 登录火山引擎控制台查看
```

**解决方案**：

- 配置正确的网络代理（如果需要）
- 更新正确的密钥
- 充值API额度

#### 问题5：前端代理失败

**症状**：`Failed to proxy` 错误

**排查步骤**：

1. 确认后端服务运行
```bash
curl http://localhost:5002/
```

2. 检查防火墙
```bash
sudo ufw status
```

3. 检查Nginx配置
```bash
sudo nginx -t
```

**解决方案**：

- 开放防火墙端口
- 重启Nginx服务

### 10.2 故障排查流程

```
发现故障
    │
    ▼
检查服务状态
    │
    ├─► PM2/Docker状态
    │   └─► pm2 status / docker ps
    │
    ├─► 端口监听
    │   └─► netstat -tlnp
    │
    └─► 进程状态
        └─► ps aux | grep python
            │
            ▼
查看日志
    │
    ├─► 应用日志
    │   └─► pm2 logs / docker logs
    │
    ├─► 系统日志
    │   └─► /var/log/syslog
    │
    └─► Nginx日志
        └─► /var/log/nginx/error.log
            │
            ▼
分析问题
    │
    ├─► 配置错误
    │
    ├─► 依赖问题
    │
    ├─► 资源不足
    │
    └─► 网络问题
        │
        ▼
解决问题
    │
    ├─► 修复配置
    │
    ├─► 重启服务
    │
    ├─► 扩容资源
    │
    └─► 联系支持
```

---

## 11. 备份与恢复

### 11.1 备份策略

#### 11.1.1 备份频率

| 备份类型 | 频率 | 保留时间 | 存储位置 |
|---------|------|---------|---------|
| **每日备份** | 每天凌晨3点 | 7天 | 本地 |
| **每周备份** | 每周日凌晨3点 | 4周 | 本地+远程 |
| **每月备份** | 每月1日凌晨3点 | 12个月 | 远程存储 |

#### 11.1.2 备份内容

- 数据库文件（`fangtang.db`）
- 配置文件（`.env`）
- 上传文件（`uploads/`）
- 静态资源（`public/`）

### 11.2 备份脚本

创建完整备份脚本 `/var/scripts/full_backup.sh`：

```bash
#!/bin/bash
# 方塘AI完整备份脚本

# 配置
BACKUP_DIR="/var/backups/fangtang"
SOURCE_DIR="/var/www/fangtang"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_LOCAL_DAYS=7
KEEP_REMOTE_DAYS=30

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
echo "[$(date)] Backing up database..."
cp $SOURCE_DIR/fangtang/fangtang.db $BACKUP_DIR/fangtang.db.$DATE

# 备份上传文件
echo "[$(date)] Backing up uploads..."
tar -czf $BACKUP_DIR/uploads.$DATE.tar.gz -C $SOURCE_DIR/fadmin uploads

# 创建完整备份
echo "[$(date)] Creating full backup..."
tar -czf $BACKUP_DIR/fangtang_full.$DATE.tar.gz \
    -C $SOURCE_DIR \
    fangtang/fangtang.db \
    fangtang/.env \
    fadmin/uploads

# 清理本地旧备份
find $BACKUP_DIR -name "*.db.*" -mtime +$KEEP_LOCAL_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$KEEP_LOCAL_DAYS -delete

# 上传到远程存储（示例：S3）
# aws s3 cp $BACKUP_DIR/fangtang_full.$DATE.tar.gz s3://your-bucket/backups/

echo "[$(date)] Backup completed: fangtang_full.$DATE.tar.gz"
```

```bash
chmod +x /var/scripts/full_backup.sh
```

### 11.3 恢复流程

```bash
# 步骤1：停止服务
pm2 stop all

# 步骤2：备份当前数据
cp fangtang.db fangtang.db.emergency

# 步骤3：下载或获取备份文件
# aws s3 cp s3://your-bucket/backups/fangtang_full.20260412.tar.gz /tmp/

# 步骤4：解压备份
tar -xzf /tmp/fangtang_full.20260412.tar.gz -C /tmp/

# 步骤5：恢复文件
cp /tmp/fangtang.db /var/www/fangtang/fangtang/
cp /tmp/.env /var/www/fangtang/fangtang/

# 步骤6：验证数据
sqlite3 /var/www/fangtang/fangtang/fangtang.db "SELECT COUNT(*) FROM users;"

# 步骤7：重启服务
pm2 restart all

# 步骤8：验证服务
curl http://localhost:5001/api/stats?invite_code=test
```

---

## 12. 运维对接指南

### 12.1 运维团队交接清单

#### 12.1.1 必需资料

| 序号 | 资料名称 | 说明 | 格式 |
|-----|---------|------|------|
| 1 | 项目源码 | 完整项目代码 | ZIP/TAR.GZ |
| 2 | 数据库备份 | 最新数据库文件 | .db/.sql |
| 3 | 配置文件 | .env等敏感配置 | 加密ZIP |
| 4 | 部署文档 | 本文档 | PDF/MD |
| 5 | 架构图 | 系统架构说明 | PNG/PDF |
| 6 | API文档 | 接口说明 | SWAGGER/HTML |
| 7 | 第三方账号 | 火山引擎账号信息 | 加密文档 |

#### 12.1.2 环境信息

| 信息类型 | 内容 | 备注 |
|---------|------|------|
| **服务器信息** | IP、SSH端口、用户名 | |
| **域名配置** | 主域名、管理后台域名 | |
| **SSL证书** | 证书文件、密钥 | |
| **防火墙规则** | 开放端口列表 | |
| **DNS配置** | 域名解析记录 | |
| **监控配置** | 监控平台账号 | |

#### 12.1.3 运维脚本

| 脚本名称 | 用途 | 路径 |
|---------|------|------|
| `start_gunicorn.sh` | 启动用户应用 | `/var/scripts/` |
| `backup_fangtang.sh` | 数据库备份 | `/var/scripts/` |
| `full_backup.sh` | 完整备份 | `/var/scripts/` |
| `verify_deployment.sh` | 部署验证 | `/var/scripts/` |

#### 12.1.4 联系人信息

| 角色 | 姓名 | 电话 | 邮箱 | 备注 |
|-----|------|------|------|------|
| **项目经理** | [姓名] | [电话] | [邮箱] | 项目总负责 |
| **技术负责人** | [姓名] | [电话] | [邮箱] | 技术问题对接 |
| **开发工程师** | [姓名] | [电话] | [邮箱] | 代码问题 |
| **运维工程师** | [姓名] | [电话] | [邮箱] | 部署运维 |

### 12.2 沟通机制

#### 12.2.1 常规沟通

| 场景 | 渠道 | 响应时间 | 负责人 |
|-----|------|---------|-------|
| **日常咨询** | 企业微信群 | 4小时内 | 技术负责人 |
| **部署需求** | 邮件 | 24小时内 | 项目经理 |
| **故障报告** | 电话/企业微信 | 立即 | 技术负责人 |

#### 12.2.2 紧急联系

**故障级别定义**：

| 级别 | 定义 | 响应时间 | 解决时间 |
|-----|------|---------|---------|
| **P0** | 服务完全不可用 | 15分钟 | 1小时 |
| **P1** | 核心功能不可用 | 30分钟 | 4小时 |
| **P2** | 非核心功能异常 | 2小时 | 24小时 |
| **P3** | 轻微问题 | 24小时 | 72小时 |

**紧急联系流程**：

1. 立即电话联系技术负责人
2. 在企业微信群发送故障通知
3. 发送邮件说明详情
4. 等待技术团队响应

### 12.3 运维标准流程

#### 12.3.1 日常部署流程

```
运维工程师发起部署请求
    │
    ▼
项目经理审批
    │
    ├─► 审批通过
    │   │
    │   ▼
    │   开发团队准备部署包
    │   │
    │   ▼
    │   运维工程师执行部署
    │   │
    │   ▼
    │   验证部署结果
    │   │
    │   ▼
    │   通知相关人员
    │
    └─► 审批拒绝
        │
        ▼
    返回修改意见
```

#### 12.3.2 故障处理流程

```
发现故障
    │
    ▼
初步判断故障级别
    │
    ├─► P0/P1（紧急）
    │   │
    │   ▼
    │   立即电话通知技术负责人
    │   │
    │   ▼
    │   技术团队介入处理
    │   │
    │   ▼
    │   问题解决
    │   │
    │   ▼
    │   编写故障报告
    │
    └─► P2/P3（常规）
        │
        ▼
    在企业微信群反馈问题
        │
        ▼
    技术团队远程协助
        │
        ▼
    问题解决
```

#### 12.3.3 变更管理流程

```bash
# 常规变更
1. 提交变更申请（邮件/文档）
2. 技术负责人评审
3. 变更审批（项目经理）
4. 执行变更（运维工程师）
5. 验证变更结果
6. 更新文档
7. 关闭变更单

# 紧急变更
1. 电话通知技术负责人
2. 口头审批
3. 立即执行变更
4. 事后补办变更手续
```

### 12.4 文档更新要求

#### 12.4.1 必需维护的文档

| 文档名称 | 更新频率 | 负责人 | 存储位置 |
|---------|---------|-------|---------|
| **部署文档** | 每次部署后更新 | 运维工程师 | 共享文档 |
| **故障报告** | 每次故障后24小时内 | 技术负责人 | 共享文档 |
| **配置清单** | 每次配置变更时 | 运维工程师 | 代码仓库 |
| **联系人清单** | 人员变动时 | 项目经理 | 共享文档 |

#### 12.4.2 故障报告模板

```markdown
# 故障报告

## 基本信息
- 故障编号：INC-2026XXXX
- 故障级别：P0/P1/P2/P3
- 发现时间：YYYY-MM-DD HH:MM
- 解决时间：YYYY-MM-DD HH:MM
- 故障时长：X小时X分钟

## 故障描述
[详细描述故障现象]

## 影响范围
[影响的服务、用户数量等]

## 故障原因
[根本原因分析]

## 解决方案
[采取的措施]

## 预防措施
[防止再次发生的措施]

## 责任人
- 故障处理：
- 报告编写：
```

---

## 附录A：快速部署命令汇总

### 单机部署命令

```bash
# 1. 安装依赖
apt update && apt install -y python3.9 python3-pip nodejs npm nginx

# 2. 创建目录
mkdir -p /var/www/fangtang /var/log/fangtang /var/backups/fangtang

# 3. 上传代码
# scp -r ./fangtang user@server:/var/www/

# 4. 配置用户应用
cd /var/www/fangtang/fangtang
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
cp .env.example .env
nano .env

# 5. 配置管理后台
cd /var/www/fangtang/fadmin
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors python-dotenv
npm install
npm run build

# 6. 配置Nginx
sudo ln -s /etc/nginx/sites-available/fangtang /etc/nginx/sites-enabled/
sudo nginx -t

# 7. 启动服务
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# 8. 验证
/var/scripts/verify_deployment.sh
```

### Docker部署命令

```bash
# 1. 安装Docker
curl -fsSL https://get.docker.com | sudo -E bash -
sudo usermod -aG docker $USER

# 2. 创建网络
docker network create fangtang-network

# 3. 部署用户应用
cd /var/www/fangtang/fangtang
docker build -t fangtang-app:latest .
docker run -d \
  --name fangtang-app \
  -p 5001:5001 \
  --network fangtang-network \
  -v /var/www/fangtang/data:/app/data \
  --restart always \
  fangtang-app:latest

# 4. 部署管理后台
cd /var/www/fangtang/fadmin
docker build -t fadmin-api:latest .
docker run -d \
  --name fadmin-api \
  -p 5002:5002 \
  --network fangtang-network \
  -v /var/www/fangtang/fadmin/uploads:/app/uploads \
  --restart always \
  fadmin-api:latest

# 5. 验证
docker ps
curl http://localhost:5001/
```

---

## 附录B：服务访问地址

| 服务 | 地址 | 说明 | 默认凭证 |
|-----|------|------|---------|
| **用户应用** | http://服务器IP:5001 | 主应用入口 | 8位邀请码 |
| **管理后台** | http://服务器IP:3001 | 管理员入口 | admin / admin123 |
| **管理后台API** | http://服务器IP:5002 | API接口 | - |

---

**文档版本**：1.0  
**最后更新**：2026-04-12  
**维护者**：方塘AI技术团队  
**文档审核**：待定
