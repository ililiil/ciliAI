# CiliAI短剧平台 - 快速启动指南

## 📋 快速启动

### 方法一：双击启动脚本（推荐）

1. **启动所有服务**
   - 双击运行 `start_services.bat` 或 `start_services.ps1`
   - 脚本会自动检查环境并启动所有服务

2. **停止所有服务**
   - 双击运行 `stop_services.bat` 或 `stop_services.ps1`

### 方法二：手动启动

#### 1. 启动后端服务
```bash
cd d:\fangtang\ciliAI
python app.py
```
后端服务将运行在 **端口 5001**

#### 2. 启动管理后台前端
```bash
cd d:\fangtang\ruoyi
npm run dev
```
管理后台将运行在 **端口 3002**

#### 3. 启动用户端前端
```bash
cd d:\fangtang\ciliAI
npm run dev
```
用户端将运行在 **端口 3003**

## 🌐 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **用户端** | http://localhost:3003 | 用户应用界面 |
| **管理后台** | http://localhost:3002 | 管理员界面 |
| **用户端API** | http://localhost:5001 | 后端API接口 |

## 🔐 登录凭证

- **用户端**：使用8位邀请码注册
- **管理后台**：
  - 用户名：`admin`
  - 密码：`admin123`

## 🔧 环境要求

### 必需软件

1. **Python 3.9+**
   - 下载地址：https://www.python.org/downloads/
   - 安装时请勾选 "Add Python to PATH"

2. **Node.js 16 LTS+**
   - 下载地址：https://nodejs.org/
   - 推荐使用LTS版本

3. **npm** (随Node.js安装)
   - 验证安装：`npm --version`

### 验证环境

```bash
# 检查Python版本
python --version
# 应显示 Python 3.9.x 或更高版本

# 检查Node.js版本
node --version
# 应显示 v16.x.x 或更高版本

# 检查npm版本
npm --version
# 应显示 8.x.x 或更高版本
```

## 📝 端口说明

### 默认端口

| 端口 | 服务 | 说明 |
|------|------|------|
| **5001** | Flask后端 | 提供所有API接口 |
| **3002** | 管理后台前端 | Vite开发服务器 |
| **3003** | 用户端前端 | Vite开发服务器 |

### 端口占用处理

如果遇到端口被占用的情况：

1. **方案一：使用启动脚本自动处理**
   - 启动脚本会自动检测并提示端口占用情况
   - 可以手动终止占用端口的进程

2. **方案二：手动查找并终止进程**
   ```bash
   # 查找占用端口的进程
   netstat -ano | findstr ":5001"
   
   # 终止进程（将PID替换为实际进程ID）
   taskkill /F /PID <PID>
   ```

3. **方案三：修改端口配置**
   - 修改 `ciliAI/app.py` 中的端口号
   - 修改 `ruoyi/vite.config.js` 中的端口号
   - 修改 `ciliAI/vite.config.js` 中的端口号

## 🛠️ 故障排查

### 问题1：后端服务启动失败

**症状**：运行 `python app.py` 后报错

**排查步骤**：
1. 检查Python版本：`python --version`
2. 检查依赖安装：`pip list`
3. 检查数据库文件是否存在
4. 查看错误日志

**解决方案**：
```bash
# 重新安装依赖
cd d:\fangtang\ciliAI
pip install -r requirements.txt
```

### 问题2：前端服务启动失败

**症状**：运行 `npm run dev` 后报错

**排查步骤**：
1. 检查Node.js版本：`node --version`
2. 检查npm安装：`npm --version`
3. 检查node_modules是否存在

**解决方案**：
```bash
# 重新安装依赖
cd d:\fangtang\ciliAI
npm install

cd d:\fangtang\ruoyi
npm install
```

### 问题3：服务无法访问

**症状**：浏览器显示"无法连接"

**排查步骤**：
1. 确认服务窗口正在运行
2. 检查端口是否被正确监听
3. 检查防火墙设置

**解决方案**：
```bash
# 检查端口监听
netstat -ano | findstr ":5001"
netstat -ano | findstr ":3002"
netstat -ano | findstr ":3003"

# 确认返回了 LISTENING 状态
```

### 问题4：API请求失败

**症状**：前端显示API错误

**排查步骤**：
1. 确认后端服务正在运行
2. 检查浏览器控制台错误信息
3. 检查网络请求详情

**解决方案**：
```bash
# 测试API接口
curl http://localhost:5001/api/works
```

## 📊 服务架构

```
┌─────────────────────────────────────────────────────────┐
│                      浏览器                              │
│   ┌──────────────┐  ┌──────────────┐                    │
│   │ 管理后台前端  │  │ 用户端前端   │                    │
│   │ (localhost:  │  │ (localhost: │                    │
│   │   3002)     │  │   3003)     │                    │
│   └──────┬───────┘  └──────┬───────┘                    │
└──────────┼─────────────────┼──────────────────────────┘
           │                 │
           │   Vite代理      │
           └────────┬────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │   Flask后端API      │
         │  (localhost:5001)   │
         │                     │
         │ - 用户端API         │
         │ - 管理后台API       │
         │ - 火山引擎AI集成     │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │   SQLite数据库       │
         │   fangtang.db       │
         └─────────────────────┘
```

## 🔄 常用命令

### 启动服务
```bash
# 方式一：使用启动脚本
start_services.bat

# 方式二：手动启动
cd d:\fangtang\ciliAI && python app.py
cd d:\fangtang\ruoyi && npm run dev
cd d:\fangtang\ciliAI && npm run dev
```

### 停止服务
```bash
# 方式一：使用停止脚本
stop_services.bat

# 方式二：手动停止
# 关闭对应的命令行窗口即可
```

### 重启服务
1. 先停止所有服务
2. 再启动所有服务

### 查看运行日志
- **后端日志**：查看后端服务窗口的输出
- **前端日志**：查看前端服务窗口的输出
- **浏览器日志**：按F12打开开发者工具查看控制台

## 📞 获取帮助

如果遇到其他问题：
1. 查看 `docs/DEPLOYMENT_GUIDE.md` 获取详细部署文档
2. 查看 `docs/DIAGNOSTIC_REPORT.md` 获取故障诊断指南
3. 检查项目根目录下的说明文档

## ✅ 验证清单

启动完成后，确认以下内容：

- [ ] 后端服务窗口显示 "Running on http://127.0.0.1:5001"
- [ ] 管理后台可访问：http://localhost:3002
- [ ] 用户端可访问：http://localhost:3003
- [ ] 管理后台登录页面正常显示
- [ ] 管理后台登录成功：admin / admin123

## 📌 注意事项

1. **保持窗口开启**：服务窗口关闭后服务将停止
2. **端口唯一性**：确保所需端口未被其他程序占用
3. **依赖完整性**：首次运行前确保所有依赖已安装
4. **数据库权限**：确保有权限读写数据库文件
5. **网络连接**：确保可以访问外网（用于AI功能）

## 🔒 安全建议

1. **开发环境**：以上配置仅适用于开发测试
2. **生产环境**：需要配置HTTPS、反向代理等安全措施
3. **密码保护**：生产环境请修改默认密码
4. **API密钥**：妥善保管火山引擎API密钥

---

**文档版本**：1.0  
**最后更新**：2026-04-14  
**适用版本**：CiliAI短剧平台 v0.3.0+
