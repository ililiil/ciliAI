# CiliAI 系统

CiliAI是一个完整的短剧平台系统，包含用户端和管理后台。

## 📁 项目结构

```
fangtang/
├── ciliAI/              # 用户端 + 后端服务
│   ├── src/            # Vue前端源代码
│   ├── app.py          # Flask后端API
│   └── package.json    # 用户端依赖
│
├── ruoyi/              # 管理后台 ⚠️（容易遗漏！）
│   ├── src/            # Vue前端源代码
│   └── package.json    # 管理后台依赖
│
├── ciliAI/             # 用户端前端
│   └── (同ciliAI/)
│
└── *.bat / *.ps1       # 启动脚本
```

## ⚠️ 重要：三个服务必须全部启动

| 服务 | 位置 | 端口 | 说明 |
|------|------|------|------|
| 后端API | ciliAI/app.py | 5001 | 为所有前端提供API |
| 用户端 | ciliAI/ | 3003 | 用户使用界面 |
| 管理后台 | ruoyi/ | 3002 | 管理员界面 ⚠️ |

## 🚀 快速启动

### 方法1：双击启动（推荐）

1. 双击 `start_all.bat`
2. 或右键 → "使用PowerShell运行" `start_all.ps1`

### 方法2：手动启动

```bash
# 1. 启动后端（必须先启动）
cd ciliAI
python app.py

# 2. 启动用户端（新窗口）
cd ciliAI
npm run dev

# 3. 启动管理后台（新窗口）⚠️
cd ruoyi
npm run dev
```

## 📖 详细文档

- [完整启动指南](CILIAI_STARTUP_GUIDE.md)
- [部署指南](docs/DEPLOYMENT_GUIDE.md)
- [项目结构说明](docs/PROJECT_STRUCTURE.md)

## 🔍 检查服务状态

运行 `check_services_status.ps1` 可以快速检查所有服务是否正在运行。

## 🛠️ 故障排查

### 端口被占用
```bash
netstat -ano | findstr ":5001"
netstat -ano | findstr ":3003"
netstat -ano | findstr ":3002"
```

### 依赖缺失
```bash
cd ciliAI
pip install -r requirements.txt
npm install

cd ruoyi
npm install
```

## 📝 注意事项

1. **管理后台（ruoyi）容易被遗漏！** 每次启动时都要确认它也启动了
2. **后端服务必须先启动**，否则前端无法正常工作
3. 如果端口被占用，Vite会自动选择下一个可用端口
4. 查看终端窗口的输出可以了解服务运行状态

## 🔧 技术栈

- **后端**: Python Flask + SQLite
- **前端**: Vue 3 + Element Plus + Vite
- **管理后台**: Vue 3 + Element Plus + Pinia + Vite

## 📧 联系方式

如有问题，请检查：
1. 所有服务是否都已启动
2. 端口是否被占用
3. Python和Node.js环境是否正常
4. 依赖是否安装完整
