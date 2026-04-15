# Docker 部署指南

## 准备工作

### 1. 创建 .env 文件

首先，基于 `.env.example` 创建你的 `.env` 文件：

```bash
cp .env.example .env
```

然后编辑 `.env` 文件，填入你的配置：

```env
# 火山引擎密钥（必填）
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey

# 数据库配置（默认使用SQLite）
DB_TYPE=sqlite
DB_PATH=fangtang.db

# 其他配置
FLASK_PORT=5001
```

### 2. 确保文件完整

检查关键文件是否存在：
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`
- ✅ `.dockerignore`
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `package.json`

## 部署步骤

### 方式一：使用 Docker Compose（推荐）

```bash
# 构建并启动容器
docker-compose up -d --build

# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 方式二：手动构建

```bash
# 构建镜像
docker build -t ciliai-backend .

# 运行容器
docker run -d \
  --name ciliai-backend \
  -p 5001:5001 \
  --env-file .env \
  -v $(pwd)/fangtang.db:/app/fangtang.db \
  -v $(pwd)/uploads:/app/uploads \
  --restart always \
  ciliai-backend
```

## 常用命令

### 查看日志
```bash
# 实时查看日志
docker-compose logs -f

# 查看最近 100 行日志
docker-compose logs --tail 100

# 查看特定容器的日志
docker logs ciliai-backend -f
```

### 重启服务
```bash
docker-compose restart
```

### 进入容器调试
```bash
docker exec -it ciliai-backend /bin/bash
```

### 更新部署
```bash
# 拉取最新代码后重新构建
docker-compose down
docker-compose up -d --build
```

## 配置说明

### 端口映射
- **5001:5001** - 应用端口

### 数据持久化
Docker Compose 配置中已经设置了以下卷挂载：
- `fangtang.db` - 数据库文件
- `uploads/` - 上传文件目录

### 健康检查
容器配置了健康检查，会每 30 秒检查一次服务是否可用。

### 日志配置
日志文件限制：
- 单个日志文件最大 10MB
- 最多保留 3 个日志文件

## 访问服务

部署成功后，访问：
- **http://你的服务器IP:5001**

## 故障排除

### 1. 容器启动失败
```bash
# 查看详细错误
docker-compose logs
```

### 2. 权限问题
确保 uploads 目录存在且有写入权限：
```bash
mkdir -p uploads
chmod 777 uploads
```

### 3. 端口被占用
检查 5001 端口是否被占用：
```bash
netstat -an | grep 5001
```

### 4. 数据库问题
如果数据库初始化失败，检查 .env 配置是否正确，并确保卷挂载路径存在。

## 生产环境优化（可选）

### 使用 Nginx 反向代理
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 使用 HTTPS
可以使用 Let's Encrypt 或其他证书，配合 Nginx 实现 HTTPS。

## 注意事项

1. **首次部署**：首次启动会比较慢，因为需要构建前端和安装 Python 依赖
2. **数据备份**：定期备份数据库文件 `fangtang.db`
3. **环境变量**：敏感信息（AK/SK）不要提交到代码仓库
4. **防火墙**：确保服务器防火墙开放了 5001 端口
5. **资源限制**：生产环境建议添加资源限制：
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 1G
   ```

## 快速检查清单

- [ ] 创建了 .env 文件
- [ ] 配置了正确的火山引擎密钥
- [ ] 安装了 Docker 和 Docker Compose
- [ ] 防火墙开放了 5001 端口
- [ ] 数据库和上传目录已创建
- [ ] 运行了 `docker-compose up -d`
- [ ] 服务可访问
