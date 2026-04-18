# Docker 部署指南

> **版本**: v0.4.5+  
> **数据库**: MySQL 8.0+  
> **更新日期**: 2026-04-15

---

## 🚀 快速开始

### 前提条件
- Docker 20.10+
- Docker Compose 2.0+
- MySQL 8.0+ 服务器

### 一行命令部署
```bash
git clone https://github.com/ililiil/ciliAI.git
cd ciliAI
cp .env.example .env
# 编辑 .env 配置文件
docker-compose up -d --build
```

---

## 📋 部署步骤

### 第一步：准备 MySQL 数据库

#### 方式 A：使用 Docker 运行 MySQL
```bash
# 创建 MySQL 容器
docker run -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=root_password \
  -e MYSQL_DATABASE=ciliai \
  -e MYSQL_USER=ciliai \
  -e MYSQL_PASSWORD=ciliai_password \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  mysql:8.0
```

#### 方式 B：使用现有 MySQL 服务器
确保 MySQL 服务器已运行，并创建数据库：
```sql
CREATE DATABASE ciliai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ciliai'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ciliai.* TO 'ciliai'@'%';
FLUSH PRIVILEGES;
```

### 第二步：配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# ============================================
# 火山引擎密钥配置（必填）
# ============================================
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey

# ============================================
# MySQL 数据库配置（必填）
# ============================================
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ciliai
DB_USER=ciliai
DB_PASSWORD=your_password

# ============================================
# Flask 配置
# ============================================
FLASK_PORT=5001
```

### 第三步：部署应用

```bash
# 构建并启动（首次部署）
docker-compose up -d --build

# 启动已构建的应用
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

---

## ⚙️ 配置说明

### 端口映射
- **5001:5001** - 应用端口（HTTP）

### 数据持久化
Docker Compose 配置中已经设置了以下卷挂载：
- `uploads/` - 上传文件目录（重要：用户上传的内容）

### 健康检查
容器配置了健康检查：
- 每 30 秒检查一次
- 超时时间 10 秒
- 连续 3 次失败后重启

### 日志配置
日志文件限制：
- 单个日志文件最大 10MB
- 最多保留 3 个日志文件

---

## 🔧 常用命令

### 查看日志
```bash
# 实时查看所有日志
docker-compose logs -f

# 查看最近 100 行日志
docker-compose logs --tail 100

# 查看特定容器日志
docker logs ciliai-backend -f
```

### 重启服务
```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart ciliai-backend
```

### 进入容器调试
```bash
docker exec -it ciliai-backend /bin/bash
```

### 更新部署
```bash
# 拉取最新代码
git pull origin master

# 停止旧容器，重新构建并启动
docker-compose down
docker-compose up -d --build
```

### 清理
```bash
# 停止并删除容器
docker-compose down

# 删除镜像
docker rmi ciliaiai-ciliai-backend

# 完全清理（包括数据卷）
docker-compose down -v
```

---

## 🌐 访问服务

部署成功后，访问：
- **本地**: http://localhost:5001
- **服务器**: http://你的服务器IP:5001

---

## ❓ 故障排除

### 1. 容器启动失败
```bash
# 查看详细错误
docker-compose logs

# 检查容器状态
docker-compose ps -a
```

### 2. 数据库连接失败
```bash
# 检查 MySQL 是否运行
docker ps | grep mysql

# 测试 MySQL 连接
docker exec -it ciliai-backend python -c "
import pymysql
conn = pymysql.connect(
    host='mysql',
    user='ciliai',
    password='ciliai_password',
    database='ciliai'
)
print('连接成功！')
"
```

### 3. 权限问题
确保 uploads 目录存在且有写入权限：
```bash
mkdir -p uploads
chmod 777 uploads
```

### 4. 端口被占用
检查 5001 端口是否被占用：
```bash
# Linux/Mac
netstat -an | grep 5001

# Windows
netstat -ano | findstr 5001
```

### 5. 容器内无法连接 MySQL
如果 MySQL 和应用不在同一台服务器，检查网络配置：
```bash
# 检查容器网络
docker network ls
docker network inspect ciliai_default
```

---

## 🔒 安全建议

### 生产环境必做

1. **修改默认密码**
   - MySQL root 密码
   - 应用数据库用户密码
   - .env 文件中的所有密钥

2. **配置防火墙**
   ```bash
   # 只开放必要端口
   ufw allow 22    # SSH
   ufw allow 80    # HTTP
   ufw allow 443   # HTTPS
   ufw deny 5001   # 阻止外部访问应用端口
   ```

3. **使用 HTTPS**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name your-domain.com;

       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;

       location / {
           proxy_pass http://localhost:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **资源限制**
   在 docker-compose.yml 中添加：
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 2G
   ```

---

## 📊 监控与日志

### 日志管理
```bash
# 查看错误日志
docker-compose logs | grep ERROR

# 导出日志
docker-compose logs > app.log

# 查看实时错误
docker-compose logs -f | grep -i error
```

### 监控建议
- 使用 Prometheus + Grafana 监控容器资源
- 配置日志收集（ELK Stack 或 Loki）
- 设置告警规则

---

## 💾 备份策略

### 数据库备份
```bash
# 备份数据库
docker exec mysql mysqldump -u ciliai -p ciliai > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker exec -i mysql mysql -u ciliai -p ciliai < backup_20260415.sql
```

### 文件备份
```bash
# 备份上传文件
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/
```

---

## 📚 相关文档

- [README.md](README.md) - 项目完整说明
- [DEPLOYMENT_CHECK.md](PRE_DEPLOYMENT_CHECK.md) - 部署前检查清单
- [.env.example](.env.example) - 环境变量示例

---

## ⚠️ 注意事项

1. **首次部署**：首次启动会比较慢，因为需要构建前端和安装 Python 依赖（约 5-10 分钟）

2. **数据备份**：
   - 定期备份 MySQL 数据库
   - 备份 uploads 目录

3. **环境变量**：敏感信息（AK/SK、数据库密码）不要提交到代码仓库

4. **防火墙**：确保服务器防火墙：
   - 开放了 22 端口（SSH）
   - 开放了 80/443 端口（HTTP/HTTPS）
   - **阻止** 5001 端口的外部访问（除非通过 Nginx）

5. **版本更新**：
   ```bash
   git pull origin master
   docker-compose down
   docker-compose up -d --build
   ```

---

## ✅ 快速检查清单

部署前确认：

- [ ] MySQL 数据库已创建
- [ ] `.env` 文件已配置
- [ ] Docker 和 Docker Compose 已安装
- [ ] 防火墙已配置
- [ ] uploads 目录已创建

部署后确认：

- [ ] `docker-compose ps` 显示运行中
- [ ] `docker-compose logs` 无错误
- [ ] 服务可访问（curl http://localhost:5001）
- [ ] 健康检查通过

---

**🎉 恭喜！部署成功！**

如有问题，请查看 [故障排除](#-故障排除) 章节或提交 Issue。
