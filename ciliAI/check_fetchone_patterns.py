#!/usr/bin/env python3
"""
MySQL fetchone/fetchall 结果访问检查
检查所有 cursor.fetchone() 和 cursor.fetchall() 的访问模式
"""

import re

def check_fetch_patterns():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    print("=" * 70)
    print("fetchone/fetchall 结果访问模式检查")
    print("=" * 70)
    
    issues = []
    
    # 检查所有 fetchone 后使用 [数字] 访问
    print("\n📋 检查 1: fetchone()[数字] 模式")
    for i, line in enumerate(lines, 1):
        if 'fetchone()' in line and re.search(r'fetchone\(\)\[\d+\]', line):
            issues.append((i, line.strip(), 'fetchone()[数字]'))
            print(f"  ❌ 行 {i}: {line.strip()}")
    
    if not any('fetchone()[数字]' in str(i) for i in issues):
        print("  ✅ 无 fetchone()[数字] 错误模式")
    
    # 检查 fetchone 后使用 .[数字] 访问
    print("\n📋 检查 2: fetchone().[数字] 模式")
    for i, line in enumerate(lines, 1):
        if 'fetchone()' in line and re.search(r'fetchone\(\)\.\w+\(\)\[\d+\]', line):
            issues.append((i, line.strip(), 'fetchone().xxx()[数字]'))
            print(f"  ❌ 行 {i}: {line.strip()}")
    
    if not any('fetchone().xxx()[数字]' in str(i) for i in issues):
        print("  ✅ 无 fetchone().xxx()[数字] 错误模式")
    
    # 检查没有空值检查的 fetchone
    print("\n📋 检查 3: fetchone() 未检查空值")
    dangerous_lines = []
    for i, line in enumerate(lines, 1):
        if 'fetchone()' in line and '=' in line:
            # 检查前后几行是否有 None 检查
            context = '\n'.join(lines[max(0, i-3):min(len(lines), i+2)])
            if 'if' not in context and 'None' not in context and 'if not' not in context:
                # 检查是否是直接赋值
                if re.search(r'=\s*cursor\.fetchone\(\)', line):
                    print(f"  ⚠️  行 {i}: 可能缺少空值检查")
                    print(f"        {line.strip()}")
    
    # 检查 fetchall() 后使用 [数字][数字] 访问
    print("\n📋 检查 4: fetchall()[数字][数字] 模式")
    for i, line in enumerate(lines, 1):
        if 'fetchall()' in line and re.search(r'fetchall\(\)\[\d+\]\[\d+\]', line):
            issues.append((i, line.strip(), 'fetchall()[数字][数字]'))
            print(f"  ⚠️  行 {i}: {line.strip()}")
            print(f"        （如果使用 DictCursor 应改为 fetchall()[数字]['字段名']）")
    
    # 检查 SELECT COUNT(*) 查询
    print("\n📋 检查 5: SELECT COUNT(*) 查询模式")
    count_pattern = re.compile(r"SELECT COUNT\(\*\)\s+as\s+(\w+)")
    for i, line in enumerate(lines, 1):
        if 'SELECT COUNT(*)' in line.upper():
            match = count_pattern.search(line)
            if match:
                field_name = match.group(1)
                # 检查下一行是否是 result[field_name]
                if i < len(lines):
                    next_line = lines[i]
                    if f"['{field_name}']" in next_line or f'["{field_name}"]' in next_line:
                        print(f"  ✅ 行 {i}: COUNT 查询结果访问正确")
                    elif '[0]' in next_line:
                        issues.append((i+1, next_line.strip(), 'COUNT 查询使用了数字索引'))
                        print(f"  ❌ 行 {i+1}: COUNT 查询使用了数字索引")
    
    print("\n" + "=" * 70)
    print("检查结果汇总")
    print("=" * 70)
    
    if issues:
        print(f"⚠️  发现 {len(issues)} 个潜在问题:")
        for line_num, line_content, issue_type in issues:
            print(f"  - 行 {line_num}: {issue_type}")
        return False
    else:
        print("✅ 所有检查通过！")
        return True

if __name__ == '__main__':
    import sys
    success = check_fetch_patterns()
    sys.exit(0 if success else 1)
