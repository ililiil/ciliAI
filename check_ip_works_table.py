import sqlite3

DATABASE = 'fangtang.db'

def check_ip_works_table():
    print("=" * 80)
    print("检查 ip_works 表结构")
    print("=" * 80)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 获取当前表结构
        cursor.execute("PRAGMA table_info(ip_works)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        print(f"\n当前列数: {len(column_names)}")
        print(f"\n当前列:")
        for col in columns:
            print(f"  - {col[1]:20} ({col[2]})")

        # ip_works表的所有可能列
        expected_columns = [
            'id', 'title', 'student_name', 'image', 'tags', 'cost',
            'duration', 'price', 'copyright', 'introduction', 'category',
            'status', 'created_at', 'updated_at', 'is_featured', 'sort_order'
        ]

        missing = [col for col in expected_columns if col not in column_names]

        if missing:
            print(f"\n⚠️  缺失的列: {', '.join(missing)}")
            print("\n正在添加缺失的列...")

            for col in missing:
                col_type = 'TEXT'
                if col == 'id':
                    col_type = 'INTEGER PRIMARY KEY AUTOINCREMENT'
                elif col in ['status', 'is_featured', 'sort_order']:
                    col_type = 'INTEGER DEFAULT 0'
                elif col in ['created_at', 'updated_at']:
                    col_type = 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'

                try:
                    if col == 'id':
                        # 不能直接添加AUTOINCREMENT列，需要重建表
                        cursor.execute(f"ALTER TABLE ip_works ADD COLUMN {col} {col_type}")
                    else:
                        cursor.execute(f"ALTER TABLE ip_works ADD COLUMN {col} {col_type}")
                    conn.commit()
                    print(f"  ✅ {col} 列已添加")
                except Exception as e:
                    print(f"  ❌ 添加 {col} 失败: {e}")

            print("\n✅ 数据库修复完成!")
        else:
            print("\n✅ 所有列都完整!")

        # 验证最终结果
        cursor.execute("PRAGMA table_info(ip_works)")
        final_columns = cursor.fetchall()

        print(f"\n修复后列数: {len(final_columns)}")
        for col in final_columns:
            print(f"  - {col[1]:20} ({col[2]})")

        conn.close()

    except Exception as e:
        print(f"\n❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_ip_works_table()
