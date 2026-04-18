# CiliAI Platform - AI创作平台

[![Version](https://img.shields.io/badge/version-1.0.1-green.svg)](https://github.com/ililiil/ciliAI)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

CiliAI 是一个基于火山引擎即梦AI的创作平台，支持文生图、视频生成、数字人等功能。

## 📋 项目概览

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端** | Flask + Python 3.9+ | RESTful API服务 |
| **前端** | Vue 3 + Vite + Element Plus | 用户界面 |
| **数据库** | MySQL 8.0 | 数据存储 |
| **AI服务** | 火山引擎即梦API | 文生图、视频生成等 |
| **容器化** | Docker + Docker Compose | 快速部署 |

### 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户浏览器                                 │
└──────────────────────┬──────────────────────┬───────────────────┘
                       │                      │
              http://localhost:3002    http://localhost:3003
                       │                      │
                       ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Docker 容器服务                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  ciliai-admin   │  │ ciliai-frontend │  │ ciliai-backend  │  │
│  │   管理后台       │  │    用户端       │  │   Flask API    │  │
│  │   Port: 3002    │  │   Port: 3003    │  │   Port: 5001    │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           └────────────────────┼────────────────────┘           │
│                                │                                │
│                                ▼                                │
│                    ┌─────────────────────┐                      │
│                    │    ciliai-mysql     │                      │
│                    │     MySQL 8.0       │                      │
│                    │    Port: 3306       │                      │
│                    └─────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   火山引擎即梦API    │
                    │  (VOLC_AK / VOLC_SK) │
                    └─────────────────────┘
```

## 🚀 快速开始

### 环境要求

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **火山引擎账号**: 需要AccessKey和SecretKey

### Docker 部署（推荐）

#### 1. 克隆项目

```bash
git clone https://github.com/ililiil/ciliAI.git
cd ciliAI
```

#### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
```

编辑 `.env` 文件，配置必要参数：

```env
# 火山引擎密钥（必填）
VOLC_AK_1=你的AccessKeyID
VOLC_SK_1=你的SecretAccessKey

# MySQL 配置
MYSQL_ROOT_PASSWORD=your_root_password
DB_NAME=ciliai
DB_USER=ciliai
DB_PASSWORD=ciliai_password

# Dify 对话配置（可选）
DIFY_API_URL=https://your-dify-api.com/v1/chat-messages
DIFY_API_KEY=你的DifyApiKey
```

**获取密钥地址**：[火山引擎控制台 - 密钥管理](https://console.volcengine.com/iam/keymanage/)

#### 3. 启动所有服务

```bash
# 启动所有服务
docker-compose -f docker-compose.optimized.yml up -d

# 查看服务状态
docker-compose -f docker-compose.optimized.yml ps

# 查看日志
docker-compose -f docker-compose.optimized.yml logs -f
```

#### 4. 访问服务

| 服务 | 地址 | 说明 |
|------|------|------|
| **用户端** | http://localhost:3003 | AI创作功能（文生图、视频等） |
| **管理后台** | http://localhost:3002 | 系统管理（用户、作品、订单） |
| **后端 API** | http://localhost:5001 | API 接口 |

**管理员默认账号**：`admin` / `admin123`

#### 5. 停止服务

```bash
docker-compose -f docker-compose.optimized.yml down
```

#### 6. 重新部署

```bash
docker-compose -f docker-compose.optimized.yml down
docker-compose -f docker-compose.optimized.yml build --no-cache
docker-compose -f docker-compose.optimized.yml up -d
```

## 📦 项目结构

```
ciliAI/
├── app.py                    # Flask 后端主程序
├── key_manager.py            # 火山引擎密钥管理器
├── db_manager.py             # 数据库管理器
├── init_mysql_db.py          # MySQL 数据库初始化脚本
├── requirements.txt          # Python 依赖
├── .env.example              # 环境变量模板
│
├── docker-compose.optimized.yml  # Docker Compose 配置
├── Dockerfile                # 后端 Docker 镜像
├── Dockerfile.frontend       # 用户端前端 Docker 镜像
│
├── ciliAI/                   # 用户端前端
│   ├── src/
│   │   ├── views/           # 页面视图
│   │   ├── components/      # 公共组件
│   │   ├── router/          # 路由配置
│   │   └── utils/           # 工具函数
│   ├── package.json
│   └── vite.config.js
│
├── backup/
│   └── flask-frontend-admin-original/
│       └── ruoyi/            # 管理后台前端
│           ├── src/
│           ├── package.json
│           └── Dockerfile
│
└── 说明/                     # 火山引擎 API 文档
```

## 🔌 API 接口

### 用户端 API (`/api/*`)

| 方法 | 路由 | 说明 |
|------|------|------|
| POST | /api/verify-invite-code | 验证邀请码 |
| GET | /api/user/info | 获取用户信息 |
| GET | /api/user/power | 获取算力余额 |
| POST | /api/power/deduct | 扣除算力 |
| GET | /api/projects | 获取项目列表 |
| POST | /api/projects | 创建项目 |
| POST | /api/generate | 文生图 |
| POST | /api/inpaint | 局部重绘 |
| POST | /api/extend | 图片扩展 |
| POST | /api/super-resolution | 智能超清 |
| GET | /api/records | 获取生成记录 |
| POST | /api/upload-image | 上传图片 |
| GET | /api/works | 获取作品列表 |
| POST | /api/orders | 创建订单 |

### 管理端 API (`/api/admin/*`)

| 方法 | 路由 | 说明 |
|------|------|------|
| POST | /api/admin/login | 管理员登录 |
| GET | /api/admin/info | 获取管理员信息 |
| GET | /api/admin/users | 用户列表 |
| PUT | /api/admin/users/:id/power | 调整用户算力 |
| GET | /api/admin/invite-codes | 邀请码列表 |
| POST | /api/admin/invite-codes | 创建邀请码 |
| PUT | /api/admin/invite-codes/:id | 更新邀请码 |
| DELETE | /api/admin/invite-codes/:id | 删除邀请码 |
| GET | /api/admin/orders | 订单列表 |
| POST | /api/admin/orders | 创建订单 |
| PUT | /api/admin/orders/:id | 更新订单 |
| GET | /api/admin/works | 作品列表 |
| POST | /api/admin/works | 创建作品 |
| PUT | /api/admin/works/:id | 更新作品 |
| DELETE | /api/admin/works/:id | 删除作品 |
| GET | /api/admin/stats | 数据统计 |
| GET | /api/admin/power-logs | 算力日志 |
| POST | /api/admin/upload | 上传管理图片 |

## ⚙️ 配置说明

### 火山引擎密钥配置

支持配置多组密钥，系统会自动轮换：

```env
VOLC_AK_1=你的AccessKeyID_1
VOLC_SK_1=你的SecretAccessKey_1
VOLC_AK_2=你的AccessKeyID_2
VOLC_SK_2=你的SecretAccessKey_2
# ... 最多支持100组
```

**多密钥优势**：
- 负载均衡，分散API调用压力
- 自动轮换，避免单密钥频率限制
- 容灾备份，某个密钥失效不影响服务

### 算力成本配置

编辑 `app.py` 中的 `POWER_COST` 字典：

```python
POWER_COST = {
    'generate': 5,             # 文生图
    'extend': 5,               # 图片扩展
    'super_resolution': 8,      # 智能超清
    'inpaint': 5,              # 局部重绘
    'chat': 1                  # 数字人
}
```

## 🐛 常见问题

### 1. Docker 部署失败

```bash
# 清理 Docker 缓存
docker system prune -a

# 重新构建（不缓存）
docker-compose -f docker-compose.optimized.yml down
docker-compose -f docker-compose.optimized.yml build --no-cache
docker-compose -f docker-compose.optimized.yml up -d

# 查看详细日志
docker-compose -f docker-compose.optimized.yml logs -f --tail=100
```

### 2. 火山引擎 API 调用失败

可能原因：
- **密钥错误**：检查 `.env` 中的 AK/SK 是否正确
- **权限不足**：确认密钥有调用即梦 API 的权限
- **余额不足**：登录火山引擎控制台充值
- **频率限制**：使用多组密钥分散压力

### 3. MySQL 连接失败

```bash
# 检查 MySQL 容器状态
docker ps | grep mysql

# 查看 MySQL 日志
docker logs ciliai-mysql

# 进入 MySQL 容器
docker exec -it ciliai-mysql mysql -uroot -p
```

### 4. 前端无法连接后端 API

检查项：
1. 后端容器是否正常运行
2. 网络配置是否正确
3. 浏览器控制台是否有 CORS 错误

## 🔧 常用命令

### Docker 命令

```bash
# 启动服务
docker-compose -f docker-compose.optimized.yml up -d

# 查看日志
docker-compose -f docker-compose.optimized.yml logs -f

# 停止服务
docker-compose -f docker-compose.optimized.yml down

# 重新构建
docker-compose -f docker-compose.optimized.yml up -d --build

# 查看容器状态
docker ps --filter "name=ciliai"
```

### 数据库命令

```bash
# 进入 MySQL 容器
docker exec -it ciliai-mysql mysql -uroot -p

# 备份数据库
docker exec ciliai-mysql mysqldump -uroot -p ciliai > backup.sql

# 恢复数据库
docker exec -i ciliai-mysql mysql -uroot -p ciliai < backup.sql
```

## 📞 技术支持

- **GitHub Issues**: https://github.com/ililiil/ciliAI/issues

## 📄 许可证

MIT License

## 🙏 致谢

- [火山引擎](https://www.volcengine.com/) - 提供强大的 AI 能力
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Flask](https://flask.palletsprojects.com/) - 轻量级 WSGI Web 应用框架
- [Element Plus](https://element-plus.org/) - Vue 3 UI 组件库
- [Vite](https://vitejs.dev/) - 下一代前端构建工具

## 📝 更新日志

### v1.0.1 (2026-04-18) - 功能完整版

- ✨ **完善管理后台功能**：使用 Flask 版本管理后台
- 🐛 **修复 MySQL 数据库问题**：添加 ip_works 表缺失字段
- 🚀 **优化 Docker 部署**：统一使用 docker-compose.optimized.yml
- 📝 **更新文档**：完善 README 和部署说明
- 🔧 **清理代码**：移除调试脚本和临时文件

### v0.4.9 (2026-04-15)

- 🐛 **修复 Dockerfile 警告**：统一 FROM 和 AS 关键字大小写
- ✅ **优化构建配置**：修复 FromAsCasing 警告，提升 Docker 构建规范

### v0.4.7 (2026-04-15)

- 🐛 **修复 KeyError: 0 错误**：修复 pymysql fetchone() 结果访问错误
- ✅ **修复问题根源**：cursor.fetchone()[0] 改为 result['count'] if result else 0

### v0.4.6 (2026-04-15)

- ✅ **Docker 部署配置优化**：移除 SQLite 数据库文件挂载
- ✅ **环境变量配置更新**：添加 MySQL 配置说明和注释模板

### v0.4.5 (2026-04-15)

- 🔥 **移除 SQLite 支持**：简化代码，仅支持 MySQL 数据库
- 🐛 **修复 TEXT 默认值问题**：将 chat_sessions 表的 TEXT 字段改为 VARCHAR(255)
- ✅ **统一 SQL 语法**：所有 SQL 占位符从 `?` 改为 MySQL 标准 `%s`
