import sqlite3

DATABASE = 'fangtang.db'

def fix_database():
    print("=" * 60)
    print("修复数据库schema")
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

        # 检查是否缺少 deadline 列
        if 'deadline' not in column_names:
            print("\n⚠️  发现 orders 表缺少 'deadline' 列，正在添加...")
            cursor.execute("ALTER TABLE orders ADD COLUMN deadline TEXT")
            conn.commit()
            print("✅  deadline 列已添加")
        else:
            print("\n✅  orders 表已包含 deadline 列")

        # 检查是否缺少 tags 列
        if 'tags' not in column_names:
            print("\n⚠️  发现 orders 表缺少 'tags' 列，正在添加...")
            cursor.execute("ALTER TABLE orders ADD COLUMN tags TEXT")
            conn.commit()
            print("✅  tags 列已添加")
        else:
            print("\n✅  orders 表已包含 tags 列")

        # 检查是否缺少 script 列
        if 'script' not in column_names:
            print("\n⚠️  发现 orders 表缺少 'script' 列，正在添加...")
            cursor.execute("ALTER TABLE orders ADD COLUMN script TEXT")
            conn.commit()
            print("✅  script 列已添加")
        else:
            print("\n✅  orders 表已包含 script 列")

        # 再次检查表结构
        cursor.execute("PRAGMA table_info(orders)")
        columns = cursor.fetchall()

        print(f"\n修复后 orders 表的列:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        conn.close()
        print("\n✅ 数据库修复完成！")

    except Exception as e:
        print(f"\n❌ 数据库修复失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_database()
