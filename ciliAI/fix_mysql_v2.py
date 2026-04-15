#!/usr/bin/env python3
"""
MySQL 迁移修复脚本 v2
自动将所有 sqlite3 调用替换为 MySQL (pymysql)
"""

import re

def fix_mysql():
    # 读取文件
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 统计原始数量
    sqlite3_connect_count = content.count('sqlite3.connect')
    sqlite3_integrity_count = content.count('sqlite3.IntegrityError')
    
    # 1. 替换 sqlite3.connect(DATABASE, check_same_thread=False) 和后续的 conn.row_factory
    # 使用多行匹配
    content = re.sub(
        r'conn = sqlite3\.connect\(DATABASE, check_same_thread=False\)\s+conn\.row_factory = sqlite3\.Row\s+conn\.cursor\(\)',
        'db = get_db()',
        content
    )
    
    # 2. 替换 sqlite3.connect + row_factory + cursor() 组合（不同顺序）
    content = re.sub(
        r'conn = sqlite3\.connect\(DATABASE, check_same_thread=False\)\s+conn\.cursor\(\)',
        'db = get_db()',
        content
    )
    
    # 3. 替换单独的 sqlite3.connect
    content = re.sub(
        r'conn = sqlite3\.connect\(DATABASE, check_same_thread=False\)',
        'db = get_db()',
        content
    )
    
    # 4. 替换 conn.row_factory = sqlite3.Row
    content = re.sub(r'conn\.row_factory = sqlite3\.Row\n', '', content)
    content = re.sub(r'conn\.row_factory = sqlite3\.Row', '', content)
    
    # 5. 替换 conn.close() 为 db.close()
    content = re.sub(r'conn\.close\(\)', 'db.close()', content)
    
    # 6. 替换 conn.commit() 为 db.commit()
    content = re.sub(r'conn\.commit\(\)', 'db.commit()', content)
    
    # 7. 替换 conn.execute() 为 db.execute()
    content = re.sub(r'conn\.execute\(', 'db.execute(', content)
    
    # 8. 替换 conn.cursor() 为 cursor (已经通过 get_db 获取)
    content = re.sub(r'cursor = conn\.cursor\(\)', '', content)
    
    # 9. 替换 sqlite3.IntegrityError 为 pymysql.IntegrityError
    content = re.sub(r'sqlite3\.IntegrityError', 'pymysql.IntegrityError', content)
    
    # 10. 清理多余的空行（连续的空行）
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # 写回文件
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 统计修复后的数量
    sqlite3_connect_after = content.count('sqlite3.connect')
    sqlite3_integrity_after = content.count('sqlite3.IntegrityError')
    
    print("=" * 70)
    print("MySQL 迁移修复完成")
    print("=" * 70)
    print(f"✅ sqlite3.connect 调用:")
    print(f"   修复前: {sqlite3_connect_count}")
    print(f"   修复后: {sqlite3_connect_after}")
    print(f"✅ sqlite3.IntegrityError:")
    print(f"   修复前: {sqlite3_integrity_count}")
    print(f"   修复后: {sqlite3_integrity_after}")
    print("=" * 70)
    
    if sqlite3_connect_after == 0 and sqlite3_integrity_after == 0:
        print("🎉 所有 sqlite3 引用已清除！")
    else:
        print(f"⚠️  仍有 {sqlite3_connect_after + sqlite3_integrity_after} 处未修复")
    
    return sqlite3_connect_after == 0 and sqlite3_integrity_after == 0

if __name__ == '__main__':
    success = fix_mysql()
    exit(0 if success else 1)
