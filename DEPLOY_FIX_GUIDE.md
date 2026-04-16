# Docker 部署修复指南

## 问题原因

Docker部署后出现以下错误：

1. **MySQL连接失败**：`Can't connect to MySQL server on 'mysql'`
2. **API返回HTML而非JSON**：`SyntaxError: Unexpected token '<'`
3. **管理后台数据无法写入**：数据库配置问题

### 根本原因

1. **环境变量配置缺失**：`d:\fangtang\ciliAI\.env` 文件中缺少数据库配置
2. **数据库类型未指定**：后端不知道使用MySQL
3. **数据库表未初始化**：MySQL数据库没有创建表结构
4. **MySQL连接失败**：后端在MySQL未就绪时就尝试连接

## 修复内容

### 1. 更新 .env 文件 ✓

添加了以下配置：
```bash
# MySQL 数据库配置
DB_TYPE=mysql
DB_HOST=mysql
DB_PORT=3306
DB_NAME=ciliai
DB_USER=ciliai
DB_PASSWORD=ciliai_password

# Flask 配置
FLASK_DEBUG=False
FLASK_PORT=5001
```

### 2. 更新 docker-compose.yml ✓

- 添加了 `env_file: .env` 指令
- 添加了 `DB_TYPE: mysql` 环境变量
- 修改了 `FLASK_DEBUG: False`（生产环境应关闭调试）

### 3. 创建 MySQL 初始化脚本 ✓

创建了 `init_mysql_db.py` 脚本：
- 自动等待MySQL服务就绪
- 创建所有必要的数据库表
- 创建初始数据（管理员账户、测试邀请码等）

### 4. 更新 Dockerfile ✓

修改启动命令：
```dockerfile
CMD ["sh", "-c", "python init_mysql_db.py && python app.py"]
```

## 重新部署步骤

### 步骤 1：停止现有容器

```bash
cd d:\fangtang\ciliAI
docker-compose down
```

### 步骤 2：清理旧数据（可选）

如果你想重新初始化数据库：

```bash
docker-compose down -v  # 删除MySQL数据卷
```

**注意**：这会删除所有数据库数据！

### 步骤 3：重新构建镜像

```bash
docker-compose build --no-cache
```

### 步骤 4：启动服务

```bash
docker-compose up -d
```

### 步骤 5：查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 只查看后端日志
docker-compose logs -f backend

# 只查看MySQL日志
docker-compose logs -f mysql
```

### 步骤 6：验证服务

```bash
# 测试后端API
curl http://localhost:5001/api/health

# 测试用户端前端
curl http://localhost:3003

# 测试管理后台
curl http://localhost:3002
```

## 访问地址

- **用户端**：http://localhost:3003
- **管理后台**：http://localhost:3002
- **后端API**：http://localhost:5001

## 管理员账户

- **邀请码**：`CILIAI88`
- **初始算力**：10000

## 常见问题

### Q1: MySQL连接仍然失败

检查MySQL日志：
```bash
docker-compose logs mysql
```

确保MySQL容器正常运行：
```bash
docker ps | grep mysql
```

### Q2: 后端启动失败

查看后端日志：
```bash
docker-compose logs backend
```

检查环境变量：
```bash
docker exec ciliai-backend env | grep DB_
```

### Q3: 前端无法连接后端

检查nginx配置：
```bash
docker exec ciliai-frontend cat /etc/nginx/conf.d/default.conf
docker exec ciliai-admin cat /etc/nginx/conf.d/default.conf
```

### Q4: 端口冲突

确保以下端口未被占用：
- 3306 (MySQL)
- 5001 (Backend)
- 3003 (Frontend)
- 3002 (Admin)

```bash
netstat -ano | findstr "3306 5001 3002 3003"
```

## 数据库连接信息

- **主机**：mysql
- **端口**：3306
- **数据库名**：ciliai
- **用户名**：ciliai
- **密码**：ciliai_password

## 技术栈

- **前端**：Vue 3 + Vite + Nginx
- **后端**：Flask + Python 3.9
- **数据库**：MySQL 8.0
- **容器编排**：Docker Compose
