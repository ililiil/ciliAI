# CiliAI 完整启动指南

## 📋 系统架构概览

CiliAI 系统包含 **3个核心服务**：

```
┌─────────────────────────────────────────────────┐
│                  用户端 (ciliAI)                 │
│              http://localhost:3003               │
│         功能：首页、项目管理、接单广场            │
└─────────────────────────────────────────────────┘
                        ↓
                        ↓ (共享API)
                        ↓
┌─────────────────────────────────────────────────┐
│                  后端服务 (Flask)                │
│              http://localhost:5001               │
│         提供所有REST API接口                      │
└─────────────────────────────────────────────────┘
                        ↑
                        ↑ (共享数据库)
                        ↑
┌─────────────────────────────────────────────────┐
│                管理后台 (ruoyi)                  │
│              http://localhost:3002               │
│         功能：用户、作品、订单、广告管理           │
└─────────────────────────────────────────────────┘
```

## 🚀 启动步骤

### 方法1：一键启动（推荐）

双击运行 `start_all.bat` 文件，它会自动：
1. 启动后端服务 (Flask)
2. 启动用户端 (ciliAI)
3. 启动管理后台 (ruoyi)

### 方法2：手动启动

#### 步骤1：启动后端服务
```bash
cd d:\fangtang\ciliAI
python app.py
```
- 启动后应看到：`Running on http://127.0.0.1:5001`
- 按 **Ctrl+C** 停止

#### 步骤2：启动用户端
```bash
cd d:\fangtang\ciliAI
npm run dev
```
- 启动后应看到：`Local: http://localhost:3003/`
- 端口可能自动变为 3004、3005 等

#### 步骤3：启动管理后台 ⚠️（容易遗漏）
```bash
cd d:\fangtang\ruoyi
npm run dev
```
- 启动后应看到：`Local: http://localhost:3002/`
- 端口可能自动变为其他端口

## ⚠️ 重要提醒

### 经常遗漏的点

1. **管理后台（ruoyi）经常被遗忘**
   - 位置：`d:\fangtang\ruoyi`
   - 启动命令：`cd ruoyi && npm run dev`
   - 访问地址：http://localhost:3002/

2. **后端服务（app.py）必须先启动**
   - 位置：`d:\fangtang\ciliAI\app.py`
   - 启动命令：`cd ciliAI && python app.py`
   - 端口：5001

### 端口说明

- **3001** - 预留
- **3002** - 管理后台（ruoyi）
- **3003** - 用户端（ciliAI）
- **5001** - 后端API（Flask）

> ⚠️ 如果端口被占用，Vite会自动选择下一个可用端口

## 🔍 验证启动成功

启动后，在浏览器中依次访问：

1. **后端API健康检查**
   ```
   http://localhost:5001/api/orders
   ```
   应该看到JSON数据响应

2. **用户端**
   ```
   http://localhost:3003/
   ```
   应该看到CiliAI用户界面

3. **管理后台** ⚠️
   ```
   http://localhost:3002/
   ```
   应该看到管理后台登录界面

## 📊 启动检查清单

- [ ] 后端服务运行中（5001端口）
- [ ] 用户端运行中（3003端口）
- [ ] 管理后台运行中（3002端口）

## 🛑 停止所有服务

### Windows
运行 `stop_services.bat` 或手动关闭终端

### 快捷键
- **Ctrl+C** - 停止当前服务

## 🔧 故障排查

### 问题1：端口被占用
```bash
# 查找占用端口的进程
netstat -ano | findstr ":5001"
netstat -ano | findstr ":3003"
netstat -ano | findstr ":3002"

# 结束进程（PID替换为实际数字）
taskkill /PID <PID> /F
```

### 问题2：后端启动失败
```bash
# 检查Python环境
python --version

# 检查依赖
cd ciliAI
pip install -r requirements.txt

# 重新启动
python app.py
```

### 问题3：前端启动失败
```bash
# 检查Node环境
node --version
npm --version

# 重新安装依赖
cd ciliAI
npm install

cd ruoyi
npm install

# 重新启动
npm run dev
```

## 📝 启动脚本说明

### start_all.bat
一键启动所有服务（后端、用户端、管理后台）

### stop_services.bat
停止所有服务

## 🎯 快速命令参考

```bash
# 启动后端
cd d:\fangtang\ciliAI && python app.py

# 启动用户端
cd d:\fangtang\ciliAI && npm run dev

# 启动管理后台 ⚠️
cd d:\fangtang\ruoyi && npm run dev
```

## 📞 获取帮助

如果启动遇到问题，检查：
1. Python版本（需要3.8+）
2. Node版本（需要16+）
3. 端口是否被占用
4. 依赖是否安装完整
