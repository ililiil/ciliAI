-- ============================================
-- CiliAI Docker Deployment Guide
-- ============================================

## 快速开始

### 1. 环境准备

确保已安装以下软件：
- Docker (版本 20.10+)
- Docker Compose (版本 2.0+)

### 2. 配置环境变量

```bash
# 复制生产环境配置模板
cp .env.prod.example .env

# 编辑配置文件
nano .env
```

必填配置项：
- `MYSQL_ROOT_PASSWORD` - MySQL root密码
- `MYSQL_PASSWORD` - 数据库用户密码
- `VOLC_AK` - 火山引擎 Access Key
- `VOLC_SK` - 火山引擎 Secret Key

### 3. 部署服务

#### Linux/macOS
```bash
# 设置脚本执行权限
chmod +x deploy.sh setup-docker.sh

# 启动生产环境
./deploy.sh prod start

# 或者使用快速设置脚本
./setup-docker.sh prod
```

#### Windows
```cmd
# 启动生产环境
deploy.bat prod start

# 或者使用快速设置脚本
scripts\deploy.ps1 prod
```

### 4. 验证部署

```bash
# 检查服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f

# 运行健康检查
./scripts/health-check.sh prod
```

### 5. 访问服务

部署成功后，可通过以下地址访问：
- 后端 API：http://localhost:5001
- 用户端前端：http://localhost:3003
- 管理后台：http://localhost:3002

## 开发环境

```bash
# 启动开发环境
./deploy.sh dev start

# 停止开发环境
./deploy.sh dev stop
```

## 数据备份

```bash
# 备份数据库
./scripts/backup.sh
```

备份文件将保存在 `backups/` 目录。

## 常见问题

### 1. 容器启动失败
检查 `.env` 文件配置是否正确，确保所有必填项已填写。

### 2. 数据库连接失败
确认 MySQL 容器已正常运行，并检查 `DB_HOST`、`DB_USER` 等配置是否正确。

### 3. 端口冲突
如果默认端口被占用，可在 `.env` 文件中修改 `*_PORT` 配置。

## 更多信息

- 项目文档：[README.md](README.md)
- 问题反馈：[GitHub Issues](https://github.com/ililiil/ciliAI/issues)
