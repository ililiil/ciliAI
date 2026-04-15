# CiliAI Docker 本地部署说明

## 📋 部署概述

本项目已配置完整的Docker环境，包含以下4个服务：
- **MySQL** (数据库)
- **Backend** (Flask API后端)
- **Frontend** (用户端Vue应用)
- **Admin** (管理后台Vue应用)

## 🚀 快速开始

### 步骤1：安装Docker Desktop

1. 下载：https://www.docker.com/products/docker-desktop
2. 安装并启动Docker Desktop
3. 等待Docker图标变为稳定状态

### 步骤2：配置环境变量

编辑 `ciliAI\.env` 文件：

```env
# 火山引擎密钥配置（必填）
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey

# MySQL 数据库配置（已预设，无需修改）
DB_HOST=mysql
DB_PORT=3306
DB_NAME=ciliai
DB_USER=ciliai
DB_PASSWORD=ciliai_password

# Flask 配置
FLASK_DEBUG=True
FLASK_PORT=5001
```

### 步骤3：启动所有服务

在项目根目录执行：

```powershell
cd d:\test\ciliAI
docker-compose up -d --build
```

首次构建需要5-10分钟，后续启动会更快。

### 步骤4：验证服务

```powershell
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 🌐 访问地址

部署成功后，访问以下地址：

- **后端API**: http://localhost:5001
- **用户端**: http://localhost:3003
- **管理后台**: http://localhost:3002

## 📁 已创建的文件

### Docker配置文件
- `docker-compose.yml` - 主编排文件（包含所有4个服务）
- `ciliAI/Dockerfile` - 后端Docker镜像配置
- `ciliAI/Dockerfile.frontend` - 用户端Docker镜像配置
- `ciliAI/nginx.conf` - 用户端Nginx配置
- `ruoyi/Dockerfile` - 管理后台Docker镜像配置
- `ruoyi/nginx.conf` - 管理后台Nginx配置

### 脚本文件
- `start-docker.ps1` - PowerShell快速启动脚本

### 文档文件
- `DOCKER_INSTALL_GUIDE.md` - Docker安装指南
- `DOCKER_DEPLOYMENT_README.md` - 本文档

### 配置文件
- `ciliAI/.env` - 环境变量配置

## 🔧 常用Docker命令

```powershell
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启所有服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 进入后端容器
docker exec -it ciliai-backend /bin/bash

# 进入MySQL容器
docker exec -it ciliai-mysql mysql -u ciliai -p

# 重新构建并启动
docker-compose up -d --build

# 删除所有容器和镜像
docker-compose down --rmi all
```

## 🗄️ 数据库说明

MySQL服务会自动创建以下数据库：
- 数据库名：`ciliai`
- 用户名：`ciliai`
- 密码：`ciliai_password`

容器数据持久化：
- MySQL数据存储在Docker volume `mysql_data`
- 上传文件存储在 `./ciliAI/uploads` 目录

## ⚠️ 注意事项

1. **首次部署**：首次启动需要构建镜像，请耐心等待
2. **端口冲突**：确保5001、3002、3003、3306端口未被占用
3. **环境变量**：必须配置火山引擎的AK/SK才能正常使用AI功能
4. **数据备份**：定期备份MySQL数据和uploads目录

## 🔍 故障排查

### 1. 容器启动失败

```powershell
# 查看详细错误
docker-compose logs

# 查看所有容器状态
docker-compose ps -a
```

### 2. 数据库连接失败

```powershell
# 检查MySQL是否运行
docker ps | grep mysql

# 测试MySQL连接
docker exec -it ciliai-mysql mysql -u ciliai -p ciliai
```

### 3. 端口被占用

```powershell
# Windows检查端口
netstat -ano | findstr ":5001"
netstat -ano | findstr ":3002"
netstat -ano | findstr ":3003"
netstat -ano | findstr ":3306"
```

### 4. 修改MySQL配置

如果需要修改MySQL配置：

1. 停止服务：`docker-compose down`
2. 删除volume：`docker volume rm ciliai_mysql_data`
3. 修改 `docker-compose.yml` 中的MySQL配置
4. 重新启动：`docker-compose up -d --build`

## 📊 架构说明

```
                    ┌──────────────┐
                    │   MySQL      │
                    │   :3306      │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│  Frontend   │      │   Backend    │      │    Admin     │
│   :3003     │◄────►│   :5001      │◄────►│    :3002     │
└─────────────┘      └──────────────┘      └─────────────┘
```

所有服务通过 `ciliai-network` 内部网络连接。

## 🔐 安全建议

生产环境请务必：

1. 修改默认密码
2. 配置防火墙
3. 使用HTTPS
4. 定期备份数据

详细安全配置请参考 `ciliAI/DEPLOYMENT.md` 文档。

## 📞 获取帮助

- 项目主页：https://github.com/ililiil/ciliAI
- 查看详细部署文档：`ciliAI/DEPLOYMENT.md`
- Docker安装指南：`DOCKER_INSTALL_GUIDE.md`

---

**🎉 祝你部署成功！**
