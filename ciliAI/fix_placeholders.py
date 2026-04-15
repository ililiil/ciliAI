#!/usr/bin/env python3
"""
MySQL 占位符全面修复脚本
将所有 SQLite 的 ? 占位符替换为 MySQL 的 %s
"""

import re

def fix_placeholders():
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 统计
    fixed_count = 0
    total_question_marks = 0
    
    new_lines = []
    for line in lines:
        # 跳过注释和字符串字面量（简化处理）
        # 查找所有 execute( 调用
        if 'execute(' in line and ('?' in line or '%s' in line):
            # 统计该行的问号数量
            question_count = line.count('?')
            total_question_marks += question_count
            
            if question_count > 0:
                # 替换所有的 ? 为 %s
                new_line = line.replace('?', '%s')
                new_lines.append(new_line)
                fixed_count += 1
                continue
        
        new_lines.append(line)
    
    # 写回文件
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ 修复完成!")
    print(f"修复行数: {fixed_count}")
    print(f"替换占位符: {total_question_marks}")

if __name__ == '__main__':
    fix_placeholders()
