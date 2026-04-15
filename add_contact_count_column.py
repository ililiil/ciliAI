import sqlite3

DATABASE = 'fangtang.db'

def add_missing_columns():
    print("=" * 60)
    print("添加 orders 表缺失的 contact_count 列")
    print("=" * 60)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 检查当前orders表结构
        cursor.execute("PRAGMA table_info(orders)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        print(f"\n当前 orders 表的列 ({len(column_names)} 列):")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        # 添加 contact_count 列
        if 'contact_count' not in column_names:
            print("\n⚠️  发现 orders 表缺少 'contact_count' 列，正在添加...")
            cursor.execute("ALTER TABLE orders ADD COLUMN contact_count INTEGER DEFAULT 0")
            conn.commit()
            print("✅  contact_count 列已添加")
        else:
            print("\n✅  orders 表已包含 contact_count 列")

        # 验证修复结果
        cursor.execute("PRAGMA table_info(orders)")
        columns = cursor.fetchall()
        final_columns = [col[1] for col in columns]

        print(f"\n修复后 orders 表的列 ({len(final_columns)} 列):")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        # 检查所有可能的缺失列
        all_expected_columns = [
            'id', 'user_id', 'title', 'image', 'qrcode', 'price', 'status',
            'created_at', 'updated_at', 'deadline', 'tags', 'script',
            'description', 'contact_info', 'contact_count', 'min_profit',
            'share_ratio', 'power_subsidy', 'period'
        ]

        missing = [col for col in all_expected_columns if col not in final_columns]

        if missing:
            print(f"\n⚠️  还有缺失的列: {', '.join(missing)}")
            print("   正在添加...")
            for col in missing:
                cursor.execute(f"ALTER TABLE orders ADD COLUMN {col} TEXT")
                conn.commit()
                print(f"   ✅ {col} 列已添加")
        else:
            print("\n✅ 所有列都完整!")

        conn.close()
        print("\n✅ 数据库修复完成！")

    except Exception as e:
        print(f"\n❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_missing_columns()
