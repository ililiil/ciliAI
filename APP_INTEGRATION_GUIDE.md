# app.py 集成 db_manager 指南

## 概述

本文档说明如何将现有的 `app.py` 与 `db_manager` 集成。

## 当前状态

✅ `db_manager.py` 已经完成并测试通过
✅ 支持 SQLite 和 MySQL
✅ 提供统一的数据库操作接口

## 集成方式

### 方式一：保持现有代码（推荐）

现有 `app.py` 可以继续使用，无需立即修改。`db_manager` 可以作为独立工具使用：

```python
# 单独使用db_manager
from ciliAI.db_manager import db_manager

# 初始化数据库
db_manager.init_database()

# 查询数据
with db_manager.get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

# 获取数量
count = db_manager.get_count("SELECT COUNT(*) FROM users")
```

### 方式二：逐步替换

如果需要完全集成，可以按以下步骤替换：

#### 步骤1：导入db_manager

在 `app.py` 开头添加：

```python
from db_manager import db_manager
```

#### 步骤2：替换数据库初始化

找到 `init_db()` 函数，替换为：

```python
def init_db():
    db_manager.init_database()
```

#### 步骤3：替换连接函数

找到 `get_db()` 函数，替换为：

```python
def get_db():
    return db_manager.get_connection()
```

#### 步骤4：替换sqlite3.connect()

找到所有 `sqlite3.connect()` 调用，替换为：

```python
# 原来
conn = sqlite3.connect(DATABASE)

# 替换为
conn = db_manager.get_connection()
```

#### 步骤5：处理fetchone()[0]

找到所有 `cursor.fetchone()[0]` 调用，替换为：

```python
# 原来
result = cursor.fetchone()[0]

# 替换为
result = cursor.fetchone()
if db_manager.db_type == 'mysql':
    count = list(result.values())[0] if result else 0
else:
    count = result[0] if result else 0
```

或者使用统一的 `get_count()` 方法：

```python
count = db_manager.get_count("SELECT COUNT(*) FROM table_name")
```

## 批量替换工具

创建一个脚本来批量替换：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量替换工具
"""
import re

def replace_app_py():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换sqlite3.connect
    content = re.sub(
        r"conn = sqlite3\.connect\([^)]+\)",
        "conn = db_manager.get_connection()",
        content
    )
    
    # 替换fetchone()[0]
    content = re.sub(
        r"cursor\.fetchone\(\)\[0\]",
        "cursor.fetchone()[0] if db_manager.db_type != 'mysql' else list(cursor.fetchone().values())[0]",
        content
    )
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    replace_app_py()
```

## 推荐的替换顺序

1. 先替换所有 `sqlite3.connect()`
2. 再替换 `cursor.fetchone()[0]`
3. 最后替换 `init_db()`

## 测试验证

替换后，运行测试脚本验证：

```bash
python test_db_integration.py
```

## 故障排查

### 导入错误

```
ModuleNotFoundError: No module named 'db_manager'
```

解决：确保在正确的目录执行，或者将 `db_manager.py` 复制到 `app.py` 同目录。

### 连接错误

```
Connection refused
```

解决：检查MySQL配置，确保MySQL服务已启动。

### 查询错误

```
OperationalError: no such table: users
```

解决：运行 `db_manager.init_database()` 初始化表。

## 性能对比

| 操作 | 直接SQLite | 使用db_manager |
|------|-----------|----------------|
| 连接获取 | 快 | 稍慢（需要判断类型） |
| 查询性能 | 相同 | 相同 |
| 代码复杂度 | 高 | 低 |
| 可维护性 | 低 | 高 |

## 总结

- ✅ `db_manager` 已完全可用
- ✅ 可以独立使用，不影响现有代码
- ✅ 完全集成需要较大改动（约200+处修改）
- ✅ 建议：新功能使用db_manager，老代码逐步迁移

## 下一步

1. 在新功能中使用 `db_manager`
2. 逐步迁移关键代码
3. 保持向后兼容
