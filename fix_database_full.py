import sqlite3

DATABASE = 'fangtang.db'

def fix_orders_table():
    print("=" * 60)
    print("修复 orders 表的 schema")
    print("=" * 60)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 检查orders表结构
        cursor.execute("PRAGMA table_info(orders)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        print(f"\n当前 orders 表的列:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        # 需要添加的列
        columns_to_add = [
            ('deadline', 'TEXT'),
            ('tags', 'TEXT'),
            ('script', 'TEXT'),
            ('description', 'TEXT'),
            ('contact_info', 'TEXT'),
            ('min_profit', 'INTEGER DEFAULT 0'),
            ('share_ratio', 'INTEGER DEFAULT 0'),
            ('power_subsidy', 'INTEGER DEFAULT 0'),
            ('period', 'INTEGER DEFAULT 0')
        ]

        print("\n检查并修复缺失的列...")
        for col_name, col_type in columns_to_add:
            if col_name not in column_names:
                print(f"  ⚠️  添加缺失的列: {col_name} ({col_type})")
                try:
                    cursor.execute(f"ALTER TABLE orders ADD COLUMN {col_name} {col_type}")
                    conn.commit()
                    print(f"    ✅ {col_name} 列已添加")
                except Exception as e:
                    print(f"    ❌ 添加 {col_name} 列失败: {e}")
            else:
                print(f"  ✅ {col_name} 列已存在")

        # 验证修复结果
        cursor.execute("PRAGMA table_info(orders)")
        final_columns = cursor.fetchall()
        final_column_names = [col[1] for col in final_columns]

        print(f"\n修复后 orders 表的列:")
        for col in final_columns:
            print(f"  - {col[1]} ({col[2]})")

        conn.close()
        print("\n✅ orders 表修复完成！")

    except Exception as e:
        print(f"\n❌ orders 表修复失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_orders_table()
