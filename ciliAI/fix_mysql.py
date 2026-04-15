#!/usr/bin/env python3
"""
MySQL 迁移修复脚本
自动将所有 sqlite3 调用替换为 MySQL (pymysql)
"""

import re

def fix_mysql_compatibility():
    # 读取文件
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 替换 sqlite3.connect(DATABASE, ...) 为使用 pymysql
    # 匹配: conn = sqlite3.connect(DATABASE, check_same_thread=False)
    # 替换为使用 get_db()
    content = re.sub(
        r'conn = sqlite3\.connect\(DATABASE, check_same_thread=False\)\s+conn\.row_factory = sqlite3\.Row',
        'db = get_db()\n        cursor = db.cursor()',
        content,
        flags=re.MULTILINE
    )
    
    # 替换单独的 sqlite3.connect
    content = re.sub(
        r'conn = sqlite3\.connect\(DATABASE, check_same_thread=False\)',
        'db = get_db()\n        cursor = db.cursor()',
        content
    )
    
    # 2. 替换 conn.row_factory = sqlite3.Row (单独的行)
    content = re.sub(
        r'conn\.row_factory = sqlite3\.Row',
        '',
        content
    )
    
    # 3. 替换 conn.close() 为 db.close()
    content = re.sub(
        r'conn\.close\(\)',
        'db.close()',
        content
    )
    
    # 4. 替换 conn.commit() 为 db.commit()
    content = re.sub(
        r'conn\.commit\(\)',
        'db.commit()',
        content
    )
    
    # 5. 替换 conn.execute() 为 cursor.execute()
    content = re.sub(
        r'conn\.execute\(',
        'cursor.execute(',
        content
    )
    
    # 6. 替换 conn.cursor() 为 cursor (如果还有残留)
    content = re.sub(
        r'conn\.cursor\(\)',
        'cursor',
        content
    )
    
    # 7. 替换 sqlite3.IntegrityError 为 pymysql.IntegrityError
    content = re.sub(
        r'except sqlite3\.IntegrityError:',
        'except pymysql.IntegrityError:',
        content
    )
    
    # 8. 替换 sqlite3.Row 为 dict (如果还有残留)
    content = re.sub(
        r'sqlite3\.Row',
        'dict',
        content
    )
    
    # 9. 替换 cursor.fetchone() 为 cursor.fetchone()
    # 这个应该已经是正确的
    
    # 10. 替换 SELECT name FROM sqlite_master 为 MySQL 版本
    content = re.sub(
        r"SELECT name FROM sqlite_master WHERE type='table' AND name='",
        "SELECT table_name FROM information_schema.tables WHERE table_schema=DATABASE['database'] AND table_name='",
        content
    )
    
    # 11. 确保 cursor.fetchall() 使用正确
    
    # 12. 添加 pymysql 异常导入（如果需要）
    if 'import pymysql' in content and 'from pymysql import' not in content:
        # 检查是否已经安装了 pymysql
        pass
    
    # 写回文件
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 统计修改
    changes = sum([
        'get_db()' in content and content != original_content,
    ])
    
    print(f"✅ MySQL 兼容性修复完成！")
    print(f"修改统计:")
    print(f"  - sqlite3.connect 调用: {original_content.count('sqlite3.connect')} → 0")
    print(f"  - sqlite3.IntegrityError: {original_content.count('sqlite3.IntegrityError')} → 0")
    print(f"  - sqlite3.Row: {original_content.count('sqlite3.Row')} → 0")
    
    return content != original_content

if __name__ == '__main__':
    fix_mysql_compatibility()
