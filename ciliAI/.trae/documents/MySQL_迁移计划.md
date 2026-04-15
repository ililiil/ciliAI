# MySQL 迁移计划

## 问题清单

### 1. TEXT 类型默认值问题 (当前报错)
**文件**: app.py
**行号**: 761
**问题**: `title TEXT NOT NULL DEFAULT '新对话'` - MySQL 的 TEXT 类型不能有默认值
**修复**: 将 TEXT 改为 VARCHAR(255)

### 2. SQLite 兼容代码冗余
**文件**: app.py
**问题**: init_db() 函数中大量 `if DB_TYPE == 'mysql': ... else: ...` 代码
**修复**: 删除所有 else 分支，只保留 MySQL 语法

### 3. 需要修复的表结构
所有表中的 TEXT 类型如果使用了 DEFAULT 值需要修复：

#### chat_sessions 表
- `title TEXT NOT NULL DEFAULT '新对话'` → `title VARCHAR(255) NOT NULL DEFAULT '新对话'`
- `selected_people TEXT DEFAULT 'script'` → `selected_people VARCHAR(50) DEFAULT 'script'`

## 实施步骤

### 步骤 1: 修复 init_db() 函数
1. 读取 app.py 的 init_db() 函数
2. 删除所有 `if DB_TYPE == 'mysql': ... else: ...` 结构
3. 只保留 MySQL 语法
4. 修复所有 TEXT 类型的默认值问题

### 步骤 2: 简化代码
1. 删除 DB_TYPE 判断逻辑
2. 直接使用 pymysql 连接
3. 简化数据库初始化流程

### 步骤 3: 测试验证
1. 确保所有 SQL 语句符合 MySQL 标准
2. 验证表结构创建成功

### 步骤 4: 提交版本
1. 更新 package.json 版本到 0.4.5
2. 更新 README.md
3. 提交并推送到 GitHub

## MySQL 规范要点

1. **自增主键**: `INT PRIMARY KEY AUTO_INCREMENT`
2. **整数类型**: `INT` 而不是 `INTEGER`
3. **TEXT 不能有默认值**: 使用 `VARCHAR(n)` 替代
4. **VARCHAR 需要指定长度**: 如 `VARCHAR(255)`
5. **DECIMAL 替代 REAL**: 用于货币字段
6. **添加存储引擎**: `ENGINE=InnoDB`
7. **字符集**: `DEFAULT CHARSET=utf8mb4`
