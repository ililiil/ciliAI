# RuoYi 快速启动指南

## 🚀 快速启动步骤

### 1. 检查环境（已完成 ✅）
```powershell
# 检查 Java
java -version
# openjdk version "24.0.1" ✅

# 检查 Maven
mvn -version
# Apache Maven 3.8.8 ✅

# 检查 MySQL
docker ps | Select-String mysql
# ciliai-mysql ✅
```

### 2. 数据库状态（已完成 ✅）
```powershell
# MySQL 信息
容器：ciliai-mysql
端口：0.0.0.0:3306->3306/tcp
数据库：ry_cloud
用户：root
密码：root_password

# 验证连接
docker exec ciliai-mysql mysql -uroot -proot_password -e "SHOW DATABASES;"
```

### 3. 编译项目
```powershell
# 进入项目目录
cd d:\fangtang\RuoYi-Vue-master

# 编译（如果还没有编译）
mvn clean package -DskipTests
```

### 4. 启动后端服务
```powershell
# 在新终端中启动后端
cd d:\fangtang\RuoYi-Vue-master
java -jar ruoyi-admin/target/ruoyi-admin.jar

# 等待启动完成，看到以下信息表示成功：
# Started RuoYiApplication in XX seconds
```

### 5. 启动前端服务
```powershell
# 在另一个终端中启动前端
cd d:\fangtang\RuoYi-Vue-master\ruoyi-ui
npm run dev

# 等待启动完成
# Local: http://localhost/
# Network: http://192.168.x.x/
```

### 6. 访问服务

| 服务 | 地址 | 说明 |
|------|------|------|
| **后端 API** | http://localhost:8080 | Spring Boot API |
| **前端管理后台** | http://localhost:80 | Vue 2 管理后台 |
| **Druid 监控** | http://localhost:8080/druid/ | 数据库连接池监控 |
| **Swagger 文档** | http://localhost:8080/swagger-ui/index.html | API 文档 |

### 7. 登录系统

```
默认管理员账号：admin
默认密码：admin123
```

---

## 🔧 配置文件位置

### 数据库配置
```
文件：ruoyi-admin/src/main/resources/application-druid.yml
```

### 日志配置
```
文件：ruoyi-admin/src/main/resources/logback.xml
路径：D:/ruoyi/logs
```

### 端口配置
```
文件：ruoyi-admin/src/main/resources/application.yml
默认端口：8080
```

---

## 📋 常用命令

### Maven 命令
```powershell
# 编译
mvn clean package

# 跳过测试编译
mvn clean package -DskipTests

# 只编译主项目
mvn clean package -pl ruoyi-admin -am
```

### Docker MySQL 命令
```powershell
# 查看状态
docker ps | Select-String mysql

# 查看日志
docker logs ciliai-mysql

# 停止
docker stop ciliai-mysql

# 启动
docker start ciliai-mysql

# 重启
docker restart ciliai-mysql
```

### Node.js 命令
```powershell
# 安装依赖
cd ruoyi-ui
npm install

# 开发模式
npm run dev

# 生产打包
npm run build:prod
```

---

## ⚠️ 常见问题

### 1. 端口被占用
```powershell
# 查找占用端口的进程
netstat -ano | Select-String :8080

# 结束进程
taskkill /PID <进程ID> /F
```

### 2. 数据库连接失败
```powershell
# 检查 MySQL 是否运行
docker ps | Select-String mysql

# 检查端口
docker port ciliai-mysql

# 测试连接
docker exec -it ciliai-mysql mysql -uroot -proot_password
```

### 3. 前端启动失败
```powershell
# 清理缓存
cd ruoyi-ui
Remove-Item -Recurse -Force node_modules, package-lock.json

# 重新安装
npm install
npm run dev
```

---

## 🎯 验证清单

启动后请验证以下功能：

### 后端验证
- [ ] 访问 http://localhost:8080 返回 JSON
- [ ] Druid 监控可访问（admin/admin123）
- [ ] Swagger 文档可访问
- [ ] 用户登录成功（admin/admin123）

### 前端验证
- [ ] 访问 http://localhost:80 显示登录页
- [ ] 登录后显示仪表盘
- [ ] 用户管理模块正常
- [ ] 角色权限模块正常

### 数据库验证
- [ ] sys_user 表有管理员用户
- [ ] sys_role 表有角色数据
- [ ] sys_menu 表有菜单数据

---

## 📞 技术支持

如果遇到问题，请检查：
1. 环境变量是否正确
2. 数据库是否运行
3. 端口是否被占用
4. 日志文件是否有权限

---

**最后更新**：2026-04-16
**适用版本**：RuoYi v3.9.2
