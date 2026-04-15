#!/usr/bin/env python3
"""
MySQL 兼容性全面深度检查
"""

import re

def comprehensive_check():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    print("=" * 70)
    print("MySQL 兼容性深度检查报告")
    print("=" * 70)
    
    issues = []
    
    # 1. 检查 sqlite3 相关
    sqlite_patterns = [
        (r'import sqlite3', 'SQLite 导入'),
        (r'sqlite3\.connect', 'SQLite 连接'),
        (r'sqlite3\.IntegrityError', 'SQLite 异常'),
        (r'sqlite3\.Row', 'SQLite Row'),
    ]
    
    print("\n📋 检查 1: SQLite 残留")
    for pattern, desc in sqlite_patterns:
        matches = re.findall(pattern, content)
        if matches:
            issues.append((desc, len(matches)))
            print(f"  ❌ {desc}: 发现 {len(matches)} 处")
        else:
            print(f"  ✅ {desc}: 无")
    
    # 2. 检查 SQL 占位符
    print("\n📋 检查 2: SQL 占位符")
    
    # 查找所有 execute 调用
    execute_lines = []
    for i, line in enumerate(lines, 1):
        if 'execute(' in line:
            execute_lines.append((i, line))
    
    # 统计各种占位符
    question_mark_count = 0
    percent_s_count = 0
    
    for i, line in enumerate(lines, 1):
        # 只在 SQL 相关的行中检查
        if any(keyword in line for keyword in ['execute', 'SELECT', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'query']):
            question_mark_count += line.count('?')
            percent_s_count += line.count('%s')
    
    print(f"  - ? 占位符: {question_mark_count}")
    print(f"  - %s 占位符: {percent_s_count}")
    
    if question_mark_count > 0:
        issues.append(('SQL 占位符未完全替换', question_mark_count))
        print("  ❌ 仍有 SQLite 风格的 ? 占位符")
    else:
        print("  ✅ 所有占位符已替换为 MySQL 风格")
    
    # 3. 检查 MySQL 特有语法
    print("\n📋 检查 3: MySQL 特有语法")
    
    mysql_checks = [
        (r'AUTO_INCREMENT', 'AUTO_INCREMENT'),
        (r'INT\s+PRIMARY', 'INT PRIMARY'),
        (r'VARCHAR\(\d+\)', 'VARCHAR 类型'),
        (r'ENGINE=InnoDB', 'InnoDB 引擎'),
        (r'CHARSET=utf8mb4', 'UTF8MB4 字符集'),
    ]
    
    for pattern, desc in mysql_checks:
        if re.search(pattern, content):
            print(f"  ✅ {desc}: 存在")
        else:
            print(f"  ⚠️  {desc}: 未找到（可能不是必需的）")
    
    # 4. 检查函数定义
    print("\n📋 检查 4: 数据库函数")
    
    functions = [
        ('init_db', '数据库初始化'),
        ('get_db', '数据库连接'),
        ('close_connection', '连接关闭'),
    ]
    
    for func_name, desc in functions:
        if f'def {func_name}' in content:
            print(f"  ✅ {desc} ({func_name}): 存在")
        else:
            issues.append((f'{desc} 函数缺失', 1))
            print(f"  ❌ {desc} ({func_name}): 缺失")
    
    # 5. 检查 conn vs db 变量
    print("\n📋 检查 5: 变量命名一致性")
    
    conn_usage = len(re.findall(r'\bconn\s*=', content))
    db_usage = len(re.findall(r'\bdb\s*=', content))
    
    print(f"  - conn 变量: {conn_usage} 次")
    print(f"  - db 变量: {db_usage} 次")
    
    if conn_usage > 0:
        issues.append(('变量命名不一致', conn_usage))
        print("  ⚠️  建议统一使用 db 变量名")
    
    # 6. 检查 cursor 定义
    print("\n📋 检查 6: Cursor 定义")
    
    cursor_in_init = 'cursor = conn.cursor()' in content or 'cursor = db.cursor()' in content
    if cursor_in_init:
        print("  ✅ init_db 中包含 cursor 定义")
    else:
        print("  ❌ init_db 中未找到 cursor 定义")
    
    # 7. 检查 pymysql 导入
    print("\n📋 检查 7: pymysql 依赖")
    
    if 'import pymysql' in content:
        print("  ✅ pymysql 已导入")
    else:
        issues.append(('pymysql 未导入', 1))
        print("  ❌ pymysql 未导入")
    
    # 8. 检查 requirements.txt
    print("\n📋 检查 8: requirements.txt")
    
    try:
        with open('requirements.txt', 'r') as f:
            reqs = f.read()
        
        required = ['flask', 'pymysql', 'cryptography']
        for pkg in required:
            if pkg in reqs:
                print(f"  ✅ {pkg}")
            else:
                issues.append((f'requirements.txt 缺少 {pkg}', 1))
                print(f"  ❌ {pkg} 未找到")
    except FileNotFoundError:
        print("  ❌ requirements.txt 未找到")
    
    # 9. 检查 SQL 语句的完整性
    print("\n📋 检查 9: SQL 语句结构")
    
    sql_issues = []
    for i, line in enumerate(lines, 1):
        # 检查 execute 中的引号配对
        if 'execute(' in line:
            # 简单检查：确保没有未关闭的引号导致的问题
            single_quote = line.count("'")
            double_quote = line.count('"')
            
            # 如果有 SQL 关键字，检查括号配对
            if any(kw in line for kw in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                open_paren = line.count('(')
                close_paren = line.count(')')
                if open_paren != close_paren:
                    sql_issues.append((i, '括号不匹配'))
    
    if sql_issues:
        print(f"  ⚠️  发现 {len(sql_issues)} 个潜在问题")
        for line_num, issue in sql_issues[:5]:
            print(f"    行 {line_num}: {issue}")
    else:
        print("  ✅ SQL 语句结构正常")
    
    # 10. 输出最终结果
    print("\n" + "=" * 70)
    print("检查结果汇总")
    print("=" * 70)
    
    if issues:
        print(f"❌ 发现 {len(issues)} 个问题:")
        for issue, count in issues:
            print(f"  - {issue} ({count} 处)")
        return False
    else:
        print("✅ 所有检查通过！代码已准备好部署到 MySQL。")
        return True

if __name__ == '__main__':
    import sys
    success = comprehensive_check()
    sys.exit(0 if success else 1)
