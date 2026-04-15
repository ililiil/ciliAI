# MySQL迁移指南

## 概述

本项目已支持MySQL数据库，包含完整的数据库管理器（`db_manager.py`），可以轻松在SQLite和MySQL之间切换。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置MySQL

在项目根目录创建 `.env` 文件：

```env
# 数据库配置
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ciliai
DB_USER=root
DB_PASSWORD=your_mysql_password

# 火山引擎密钥
VOLC_AK=你的AccessKeyID
VOLC_SK=你的SecretAccessKey
```

### 3. 创建MySQL数据库

```sql
-- 在MySQL中执行
CREATE DATABASE ciliai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据库

运行数据库管理器来创建所有表：

```python
from db_manager import db_manager

# 初始化数据库和表
db_manager.init_database()
print(f"数据库类型: {db_manager.db_type}")
print("所有表创建完成！")
```

### 5. 启动应用

```bash
python app.py
```

## 数据库管理器使用

### 基本用法

```python
from db_manager import db_manager

# 使用上下文管理器（推荐）
with db_manager.get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

# 使用统一查询方法
count = db_manager.get_count("SELECT COUNT(*) FROM users")
results = db_manager.execute_query("SELECT * FROM works", fetch_all=True)

# 获取单条记录
user = db_manager.execute_query(
    "SELECT * FROM users WHERE invite_code = ?",
    (invite_code,),
    fetch_one=True
)
```

### 插入数据

```python
with db_manager.get_db() as conn:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (invite_code, compute_power, nickname) VALUES (?, ?, ?)",
        (invite_code, power, nickname)
    )
    conn.commit()  # 上下文管理器会自动commit
```

### 更新数据

```python
with db_manager.get_db() as conn:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET compute_power = ? WHERE id = ?",
        (new_power, user_id)
    )
```

## SQLite和MySQL对比

| 特性 | SQLite | MySQL |
|------|--------|-------|
| 适合场景 | 开发/小型项目 | 生产环境 |
| 配置复杂度 | 无需配置 | 需要配置连接 |
| 并发性能 | 一般 | 优秀 |
| 数据量限制 | < 1GB | 无限制 |
| 字符集 | UTF-8 | utf8mb4 |
| 自动递增 | AUTOINCREMENT | AUTO_INCREMENT |
| 布尔类型 | 0/1 | TINYINT(1) |

## 数据迁移（可选）

如果需要从SQLite迁移到MySQL：

### 方法1：导出导入

```bash
# 1. 导出SQLite数据
sqlite3 fangtang.db .dump > data.sql

# 2. 转换字符编码
iconv -f UTF-8 -t UTF-8//IGNORE data.sql > data_utf8.sql

# 3. 导入MySQL
mysql -u root -p ciliai < data_utf8.sql
```

### 方法2：使用Python脚本

```python
import sqlite3
import pymysql

# 读取SQLite数据
sqlite_conn = sqlite3.connect('fangtang.db')
sqlite_cursor = sqlite_conn.cursor()

# 连接MySQL
mysql_conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='ciliai'
)
mysql_cursor = mysql_conn.cursor()

# 迁移数据（示例：users表）
sqlite_cursor.execute("SELECT * FROM users")
users = sqlite_cursor.fetchall()

for user in users:
    mysql_cursor.execute("""
        INSERT INTO users (invite_code, compute_power, nickname, status)
        VALUES (%s, %s, %s, %s)
    """, (user[1], user[2], user[4], user[5]))

mysql_conn.commit()
```

## 故障排查

### 连接失败

```python
# 检查连接配置
from db_manager import db_manager

print(f"数据库类型: {db_manager.db_type}")
print(f"配置: {db_manager._config}")
```

### 表不存在

```python
# 重新初始化
from db_manager import db_manager
db_manager.init_database()
```

### 字符编码问题

确保MySQL使用utf8mb4字符集：

```sql
ALTER DATABASE ciliai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 性能优化

### MySQL

```env
DB_TYPE=mysql
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

### 连接池

MySQL支持连接池，可以提高性能：

```python
from db_manager import db_manager

# 获取连接
conn = db_manager.get_connection()

# 使用连接池（如果配置了）
pool = db_manager.get_pool()
```

## 备份和恢复

### 备份

```bash
mysqldump -u root -p ciliai > backup.sql
```

### 恢复

```bash
mysql -u root -p ciliai < backup.sql
```

## 监控

### 查看连接数

```sql
SHOW STATUS LIKE 'Threads_connected';
SHOW PROCESSLIST;
```

### 查看查询性能

```sql
EXPLAIN SELECT * FROM users WHERE invite_code = 'xxx';
```

## 技术支持

如有问题，请检查：
1. MySQL服务是否启动
2. 数据库配置是否正确
3. 用户权限是否足够
4. 防火墙是否允许连接
