# CiliAI Docker部署 - 文件清单和检查清单

## ✅ 已创建的Docker配置文件

### 1. 根目录docker-compose.yml
- **路径**: `docker-compose.yml`
- **作用**: 主编排文件，定义4个服务的完整配置
- **包含**: MySQL, Backend, Frontend, Admin

### 2. ciliAI目录（用户端+后端）
- **Dockerfile**: 后端Flask应用镜像
- **Dockerfile.frontend**: 用户端Vue应用镜像
- **nginx.conf**: 用户端Nginx配置
- **.env**: 环境变量配置

### 3. ruoyi目录（管理后台）
- **Dockerfile**: 管理后台Vue应用镜像
- **nginx.conf**: 管理后台Nginx配置

### 4. 脚本和文档
- **start-docker.ps1**: PowerShell快速启动脚本
- **DOCKER_INSTALL_GUIDE.md**: Docker安装指南
- **DOCKER_DEPLOYMENT_README.md**: 详细部署说明

## 📋 部署前检查清单

### 系统要求
- [ ] Windows 10/11 专业版、企业版或教育版
- [ ] 至少8GB RAM（推荐16GB）
- [ ] 至少20GB可用磁盘空间
- [ ] 已启用WSL2（通过PowerShell: `wsl --install`）

### Docker安装
- [ ] Docker Desktop已下载
- [ ] Docker Desktop已安装
- [ ] Docker Desktop已启动并运行
- [ ] 运行 `docker --version` 验证
- [ ] 运行 `docker-compose --version` 验证

### 环境配置
- [ ] 已克隆项目：`git clone https://github.com/ililiil/ciliAI.git`
- [ ] 已进入项目目录：`cd d:\test\ciliAI`
- [ ] 已创建 `.env` 文件
- [ ] 已配置火山引擎AK/SK
- [ ] 已确认MySQL配置正确

### 端口检查
- [ ] 端口5001未被占用（后端API）
- [ ] 端口3002未被占用（管理后台）
- [ ] 端口3003未被占用（用户端）
- [ ] 端口3306未被占用（MySQL数据库）

## 🚀 部署步骤

### 步骤1：配置环境变量
```powershell
# 编辑 ciliAI\.env 文件
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey
```

### 步骤2：启动Docker服务
```powershell
# 启动所有服务（首次需要构建）
docker-compose up -d --build

# 查看构建进度
docker-compose logs -f
```

### 步骤3：验证服务状态
```powershell
# 查看运行中的容器
docker-compose ps

# 测试各服务端口
curl http://localhost:5001
curl http://localhost:3002
curl http://localhost:3003
```

## 🌐 访问地址

- **后端API**: http://localhost:5001
- **用户端**: http://localhost:3003
- **管理后台**: http://localhost:3002

## 🔧 常用命令速查

```powershell
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 进入容器
docker exec -it ciliai-backend /bin/bash
docker exec -it ciliai-mysql mysql -u ciliai -p

# 重新构建
docker-compose up -d --build

# 清理
docker-compose down -v
```

## ⚠️ 常见问题

### Q1: Docker Desktop启动失败
**解决方案**:
1. 检查BIOS中是否启用虚拟化
2. 运行 `wsl --update` 更新WSL2
3. 重新安装Docker Desktop

### Q2: 端口被占用
**解决方案**:
```powershell
netstat -ano | findstr ":5001"
# 使用任务管理器终止占用进程
```

### Q3: 数据库连接失败
**解决方案**:
1. 检查MySQL容器是否运行：`docker ps | grep mysql`
2. 查看MySQL日志：`docker logs ciliai-mysql`
3. 等待MySQL完全启动（约30秒）

### Q4: 构建失败
**解决方案**:
1. 清理Docker缓存：`docker system prune -a`
2. 重新构建：`docker-compose up -d --build`
3. 检查网络连接

## 📊 服务架构

```
                    ┌──────────────┐
                    │   MySQL      │
                    │   :3306      │
                    │  ciliai-mysql│
                    └──────┬───────┘
                           │
                           ▼
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│  Frontend   │      │   Backend    │      │    Admin     │
│   :3003     │◄────►│   :5001      │◄────►│    :3002     │
│ciliai-frontend│   │ciliai-backend│      │ ciliai-admin │
└─────────────┘      └──────────────┘      └─────────────┘
```

## 📝 注意事项

1. **首次部署**: 需要5-10分钟构建镜像
2. **数据持久化**: 
   - MySQL数据存储在Docker volume
   - 上传文件在 `./ciliAI/uploads`
3. **环境变量**: 必须配置火山引擎密钥
4. **防火墙**: 确保开放必要端口

## 🆘 获取帮助

- 项目主页：https://github.com/ililiil/ciliAI
- Docker安装：查看 `DOCKER_INSTALL_GUIDE.md`
- 详细部署：查看 `DOCKER_DEPLOYMENT_README.md`
- 官方部署文档：查看 `ciliAI/DEPLOYMENT.md`

---

**✅ 部署检查清单完成！**

按照以上步骤操作，你应该能够成功部署CiliAI项目。如有问题，请参考文档或提交Issue。
