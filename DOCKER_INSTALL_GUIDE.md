# Docker Desktop 安装指南

## 系统要求

Windows 10/11 专业版、企业版或教育版（需要WSL2支持）
或者 Windows 10/11 家庭版（可以使用WSL2）

## 安装步骤

### 1. 下载Docker Desktop

访问 Docker 官网下载：https://www.docker.com/products/docker-desktop

### 2. 启用WSL2（如果没有启用）

打开PowerShell（管理员），运行：
```powershell
wsl --install
```

### 3. 安装Docker Desktop

1. 双击下载的 `Docker Desktop Installer.exe`
2. 勾选 "Use WSL 2 instead of Hyper-V"（推荐）
3. 点击 "Install"
4. 安装完成后，Docker Desktop会自动启动

### 4. 验证安装

打开PowerShell，运行：
```powershell
docker --version
docker-compose --version
```

应该看到类似输出：
```
Docker version 24.x.x, build xxxxx
docker-compose version v2.x.x
```

## 启动Docker Desktop

1. 在Windows开始菜单中找到 "Docker Desktop"
2. 点击启动
3. 等待Docker图标变为稳定状态（不再转圈）

## 启动CiliAI项目

1. 打开PowerShell或终端
2. 进入项目目录：
   ```powershell
   cd d:\test\ciliAI
   ```

3. 配置环境变量：
   编辑 `ciliAI\.env` 文件，填入你的实际配置：
   - VOLC_AK: 火山引擎AccessKeyID
   - VOLC_SK: 火山引擎SecretAccessKey
   - DB_PASSWORD: MySQL数据库密码

4. 构建并启动所有服务：
   ```powershell
   docker-compose up -d --build
   ```

5. 查看服务状态：
   ```powershell
   docker-compose ps
   ```

6. 查看日志：
   ```powershell
   docker-compose logs -f
   ```

## 服务访问地址

- 后端API：http://localhost:5001
- 用户端：http://localhost:3003
- 管理后台：http://localhost:3002

## 停止服务

```powershell
docker-compose down
```

## 常见问题

### Docker Desktop启动失败

1. 检查BIOS中是否启用了虚拟化技术
2. 确保WSL2已正确安装
3. 重新安装Docker Desktop

### 端口被占用

如果端口5001、3002或3003被占用，可以修改docker-compose.yml中的端口映射。

### 数据库连接失败

确保MySQL服务正在运行，并且.env文件中的数据库配置正确。

## Docker命令参考

```powershell
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 进入容器内部
docker exec -it <容器名> /bin/sh

# 查看日志
docker logs <容器名>

# 重新构建并启动
docker-compose up -d --build

# 停止并删除容器
docker-compose down

# 删除所有未使用的镜像
docker image prune -a
```
