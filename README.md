# CiliAI Platform - AI创作平台

CiliAI 是一个基于火山引擎即梦AI的创作平台，支持文生图、视频生成、数字人等功能。

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn
- 火山引擎账号及密钥

### 1. 克隆项目

```bash
git clone https://github.com/ililiil/ciliAI.git
cd ciliAI
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的火山引擎密钥
# 获取地址：https://console.volcengine.com/iam/keymanage/
```

编辑 `.env` 文件：

```env
# 火山引擎密钥（必填）
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey

# 管理后台地址（可选，默认不需要修改）
ADMIN_BASE_URL=http://localhost:5002
```

### 3. 安装后端依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 4. 安装前端依赖

```bash
npm install
```

## 🎯 用户端部署

### 开发环境

#### 方式一：前端开发服务器 + 后端API（推荐）

**终端1 - 启动后端API：**
```bash
python app.py
```
后端API将运行在 `http://localhost:5001`

**终端2 - 启动前端开发服务器：**
```bash
npm run dev
```
前端将运行在 `http://localhost:3002`

访问 `http://localhost:3002` 即可使用用户端。

#### 方式二：纯后端模式（快速测试）

如果只需要测试后端API，可以直接运行：
```bash
python app.py
```
然后访问 `http://localhost:5001`

### 生产环境部署

#### 前端构建

```bash
# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

#### 使用Docker部署（推荐）

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 手动部署

1. **构建前端：**
   ```bash
   npm run build
   ```

2. **配置Nginx：**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       # 前端静态文件
       location / {
           root /path/to/ciliAI/dist;
           try_files $uri $uri/ /index.html;
       }

       # API代理
       location /api {
           proxy_pass http://localhost:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **启动后端服务：**
   ```bash
   # 使用systemd或其他进程管理器
   nohup python app.py > app.log 2>&1 &
   ```

## 🔐 管理端部署

### 功能说明

管理端提供以下管理功能：
- 邀请码管理（创建、编辑、删除）
- 用户管理（查看用户、调整算力）
- 订单管理
- 作品管理
- 广告管理
- 数据统计

### 访问方式

管理端API已集成在后端服务中，路由前缀为 `/api/admin/`：

- 登录接口：`POST /api/admin/login`
- 用户信息：`GET /api/admin/info`
- 邀请码管理：`GET/POST/PUT/DELETE /api/admin/invite-codes`
- 用户管理：`GET /api/admin/users`
- 数据统计：`GET /api/admin/stats`

### 管理端前端（待开发）

管理端前端界面正在开发中，完成后将提供独立的部署说明。

**临时管理方式：**

可以使用Postman或其他API工具管理：

1. **登录：**
   ```bash
   curl -X POST http://localhost:5001/api/admin/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'
   ```

2. **获取邀请码：**
   ```bash
   curl http://localhost:5001/api/admin/invite-codes \
     -H "Authorization: Bearer your-token"
   ```

## 📱 局域网部署

如果需要在内网部署供多设备访问：

### 1. 修改后端监听地址

编辑 `app.py`，找到：
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

### 2. 获取服务器IP

```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

找到IPv4地址，例如：`192.168.1.100`

### 3. 访问

在同一局域网的设备浏览器中访问：
```
http://192.168.1.100:5001  # 后端API
http://192.168.1.100:3002  # 前端（如果前端也在运行）
```

### 4. 防火墙设置（Windows）

如果其他设备无法访问，需要开放端口：

1. 打开 "Windows Defender 防火墙"
2. 点击 "高级设置"
3. 选择 "入站规则" → "新建规则"
4. 规则类型：端口
5. 协议：TCP，端口：5001
6. 操作：允许连接
7. 命名规则，例如："CiliAI API Port"

## 🔧 常用命令

### 后端命令

```bash
# 启动后端（开发模式）
python app.py

# 启动后端（生产模式）
python app.py --production

# 检查用户
python check_user.py

# 密钥管理测试
python test_key_rotation.py
```

### 前端命令

```bash
# 开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

### Docker命令

```bash
# 构建镜像
docker build -t ciliai-platform .

# 运行容器
docker run -d -p 5001:5001 -p 3002:80 ciliai-platform

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 📁 项目结构

```
ciliAI/
├── app.py                    # Flask后端主文件
├── requirements.txt          # Python依赖
├── key_manager.py           # 密钥管理器
├── check_user.py            # 用户检查工具
│
├── src/                     # Vue前端源码
│   ├── views/              # 页面视图
│   │   ├── Home.vue        # 首页
│   │   ├── Order.vue       # 接单广场
│   │   ├── ProjectDetail.vue # 项目详情
│   │   └── ...
│   ├── components/         # 组件
│   │   ├── LoginModal.vue  # 登录弹窗
│   │   ├── CreateProjectModal.vue
│   │   └── ...
│   ├── router/             # 路由配置
│   └── utils/              # 工具函数
│
├── public/                  # 静态资源
│   └── ads/                # 广告图片
│
├── dist/                   # 构建输出目录
├── uploads/                # 上传文件目录
│
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker Compose配置
├── vite.config.js          # Vite配置
├── package.json            # Node依赖
└── .env.example           # 环境变量模板
```

## ⚙️ 配置说明

### 火山引擎密钥

1. 访问 [火山引擎控制台](https://console.volcengine.com/iam/keymanage/)
2. 创建 AccessKey
3. 将AK和SK填入 `.env` 文件

### 算力配置

编辑 `app.py` 中的 `POWER_COST` 字典：

```python
POWER_COST = {
    'generate': 5,           # 文生图
    'extend': 5,             # 图片扩展
    'super_resolution': 8,   # 智能超清
    'inpaint': 5,            # 局部重绘
    'chat': 1                # 数字人
}
```

### 数据库

默认使用SQLite数据库 `fangtang.db`，如需切换到MySQL/PostgreSQL：

1. 安装对应驱动：
   ```bash
   pip install pymysql  # MySQL
   # 或
   pip install psycopg2  # PostgreSQL
   ```

2. 修改 `app.py` 中的数据库连接代码

## 🐛 常见问题

### 1. 端口被占用

```bash
# Windows查找占用端口的进程
netstat -ano | findstr :5001

# 结束进程
taskkill /PID <进程ID> /F

# 或修改端口，在app.py中修改
app.run(port=5002)
```

### 2. 前端无法连接后端API

检查：
1. 后端是否启动成功
2. Vite代理配置是否正确（检查 `vite.config.js`）
3. 浏览器控制台是否有CORS错误

### 3. 火山引擎API调用失败

1. 检查AK/SK是否正确
2. 检查密钥是否有对应API的权限
3. 查看后端日志中的错误信息
4. 确认账户余额充足

### 4. Docker部署失败

```bash
# 清理Docker
docker system prune -a

# 重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📞 技术支持

- 提交Issue: https://github.com/ililiil/ciliAI/issues
- 邮箱: your-email@example.com

## 📄 许可证

MIT License

## 🙏 致谢

- [火山引擎](https://www.volcengine.com/) - 提供AI能力
- [Vue.js](https://vuejs.org/) - 前端框架
- [Flask](https://flask.palletsprojects.com/) - 后端框架
- [Element Plus](https://element-plus.org/) - UI组件库
