# 即梦 AI 4.0 文生图 Demo

这是一个简单的文生图 Web 应用，基于火山引擎即梦 AI 4.0 接口开发。

## 快速开始

### 1. 安装依赖
建议使用虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2. 配置密钥
1. 复制环境配置文件：
   ```bash
   cp .env.example .env
   ```
2. 编辑 `.env` 文件，填入你的火山引擎 `VOLC_AK` 和 `VOLC_SK`。
   > 获取地址：[火山引擎控制台 - 密钥管理](https://console.volcengine.com/iam/keymanage/)

### 3. 运行项目
```bash
python app.py
```

### 4. 访问页面
打开浏览器访问：`http://localhost:5000`

## 项目结构
- `app.py`: Flask 后端逻辑，处理 API 提交与异步结果轮询。
- `static/index.html`: 前端页面，支持提示词输入、比例选择和结果展示。
- `说明/`: 存放采集到的即梦 AI 4.0 官方文档副本。
- `requirements.txt`: 项目 Python 依赖。
- `.env.example`: 环境变量模板。

---

## 💻 Windows 局域网部署与访问指南

如果您想将本来运行在 Mac 上的本项目部署到局域网内的 **Windows 电脑** 上，并让局域网其他设备访问，请按以下步骤操作：

### 1. 准备项目文件
将 Mac 上的整个 `即梦` 文件夹（包括里面的 `.env` 密钥文件），拷贝到 Windows 电脑的任一目录。

### 2. 安装 Python 环境
前往 Python 官网 (https://www.python.org/downloads/) 下载最新的 Windows 安装包。
> **⚠️ 必须注意**：安装弹出的第一页，务必勾选最下方的 **"Add python.exe to PATH"**。

### 3. 安装依赖与启动服务
1. 在 Windows 电脑进入拷贝过来的 `即梦` 文件夹。
2. 在空白处按住 `Shift` 键 + 鼠标右键，选择 **“在此处打开 PowerShell 窗口”**。
3. 如果想保持环境干净，可以创建虚拟环境（可选）：
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. 安装项目依赖：
   ```powershell
   pip install -r requirements.txt
   ```
5. 启动程序：
   ```powershell
   python app.py
   ```
   > 服务启动后，因为代码中写的是 `host='0.0.0.0'`，这会让 Flask 监听整台电脑所有的网络接口，天然支持局域网访问。

### 4. 获取 Windows 的局域网 IP 并访问
1. 新开一个命令提示符 (CMD) 或 PowerShell，输入 `ipconfig` 回车。
2. 找到 **“IPv4 地址”** 行，记下这个 IP（例如 `192.168.31.50`）。
3. 在同一路由器下的 Mac、手机或其他设备浏览器里输入：
   `http://192.168.31.50:5001` （替换为你实际查到的 IP）。

#### 🛡️ 局域网无法打开网页的解决办法（防火墙设置）
如果 Windows 电脑上显示服务在运行，但在其他设备上打不开网页，通常是被 Windows 自带的防火墙拦截了 5001 端口：
1. 点击 Windows 徽标键，搜索并打开 **“高级安全 Windows Defender 防火墙”**。
2. 点击左侧的 **“入站规则”**，在右侧点击 **“新建规则...”**。
3. 规则类型选择 **“端口”**。
4. 协议选择 **“TCP”**，在“特定本地端口”中填入 **`5001`**。
5. 一路点击“下一步”（允许连接），最后随便起个名字（如 "Jimeng App Port"）即可。
刷新手机/Mac上的网页，即可顺利访问！
