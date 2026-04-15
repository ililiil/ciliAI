#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def fix_file():
    filepath = r'D:\fangtang\ciliAI\src\views\ProjectDetail.vue'

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find and fix line 108 (index 107)
        for i in range(len(lines)):
            if i == 107 and '/p>' in lines[i]:
                # Replace the corrupted line
                lines[i] = '                <p class="hint">鐐瑰嚮"鏂板&#x20;寮€濮?</p>\n'
                print(f'Fixed line {i+1}')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print('File fixed successfully')
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == '__main__':
    sys.exit(0 if fix_file() else 1)
