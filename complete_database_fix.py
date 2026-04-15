import sqlite3

DATABASE = 'fangtang.db'

def complete_database_repair():
    print("=" * 80)
    print("完整数据库修复 - orders表")
    print("=" * 80)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 获取当前表结构
        cursor.execute("PRAGMA table_info(orders)")
        current_columns = cursor.fetchall()
        current_column_names = [col[1] for col in current_columns]

        print(f"\n当前列数: {len(current_column_names)}")
        print(f"当前列: {', '.join(current_column_names)}")

        # orders表的所有可能列
        all_orders_columns = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'user_id': 'INTEGER',
            'title': 'TEXT NOT NULL',
            'image': 'TEXT',
            'qrcode': 'TEXT',
            'price': 'TEXT',
            'status': 'TEXT DEFAULT "pending"',
            'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'updated_at': 'TIMESTAMP',
            'deadline': 'TEXT',
            'tags': 'TEXT',
            'script': 'TEXT',
            'description': 'TEXT',
            'contact_info': 'TEXT',
            'contact_count': 'INTEGER DEFAULT 0',
            'min_profit': 'INTEGER DEFAULT 0',
            'share_ratio': 'INTEGER DEFAULT 0',
            'power_subsidy': 'INTEGER DEFAULT 0',
            'period': 'INTEGER DEFAULT 0'
        }

        # 添加缺失的列
        added_columns = []
        for col_name, col_type in all_orders_columns.items():
            if col_name not in current_column_names:
                print(f"\n⚠️  添加缺失列: {col_name} ({col_type})")
                try:
                    cursor.execute(f"ALTER TABLE orders ADD COLUMN {col_name} {col_type}")
                    conn.commit()
                    added_columns.append(col_name)
                    print(f"   ✅ {col_name} 列已添加")
                except Exception as e:
                    print(f"   ❌ 添加失败: {e}")

        # 验证最终结果
        cursor.execute("PRAGMA table_info(orders)")
        final_columns = cursor.fetchall()
        final_column_names = [col[1] for col in final_columns]

        print(f"\n" + "=" * 80)
        print("修复后列数:", len(final_column_names))
        print("=" * 80)

        for col in final_columns:
            is_new = col[1] in added_columns
            marker = " 🆕" if is_new else ""
            print(f"  - {col[1]:20} ({col[2]}){marker}")

        # 测试插入一条记录
        print("\n" + "=" * 80)
        print("测试插入记录...")
        print("=" * 80)

        try:
            cursor.execute('''
                INSERT INTO orders (title, image, price, status, description, contact_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('修复测试', 'https://example.com/test.jpg', '¥100', 'recruiting', '完整数据库修复测试', 0))

            test_id = cursor.lastrowid
            conn.commit()

            print(f"✅ 测试记录插入成功! ID: {test_id}")

            # 删除测试记录
            cursor.execute('DELETE FROM orders WHERE id = ?', (test_id,))
            conn.commit()
            print(f"✅ 测试记录已删除")

        except Exception as e:
            print(f"❌ 测试插入失败: {e}")

        conn.close()

        print("\n" + "=" * 80)
        if added_columns:
            print(f"✅ 数据库修复完成! 添加了 {len(added_columns)} 个列:")
            print("   " + ", ".join(added_columns))
        else:
            print("✅ 数据库已是最新状态，无需修复")
        print("=" * 80)

        return len(added_columns)

    except Exception as e:
        print(f"\n❌ 数据库修复失败: {e}")
        import traceback
        traceback.print_exc()
        return -1

if __name__ == '__main__':
    complete_database_repair()
