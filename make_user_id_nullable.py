import sqlite3

DATABASE = 'fangtang.db'

def make_user_id_nullable():
    print("=" * 60)
    print("修复 orders 表的 user_id 约束")
    print("=" * 60)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 检查当前 user_id 约束
        cursor.execute("PRAGMA table_info(orders)")
        columns = cursor.fetchall()
        user_id_col = [col for col in columns if col[1] == 'user_id'][0]

        print(f"\n当前 user_id 列信息:")
        print(f"  列名: {user_id_col[1]}")
        print(f"  类型: {user_id_col[2]}")
        print(f"  是否NOT NULL: {user_id_col[3]}")
        print(f"  默认值: {user_id_col[4]}")

        # SQLite 不支持直接修改列的NOT NULL约束，需要重建表
        if user_id_col[3] == 1:  # NOT NULL is 1
            print("\n⚠️  user_id 列有 NOT NULL 约束，正在修复...")

            # 创建新表
            cursor.execute('''
                CREATE TABLE orders_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    image TEXT,
                    qrcode TEXT,
                    price TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    deadline TEXT,
                    tags TEXT,
                    script TEXT,
                    description TEXT,
                    contact_info TEXT,
                    min_profit INTEGER DEFAULT 0,
                    share_ratio INTEGER DEFAULT 0,
                    power_subsidy INTEGER DEFAULT 0,
                    period INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # 复制数据
            cursor.execute('''
                INSERT INTO orders_new
                SELECT id, user_id, title, image, qrcode, price, status, created_at, updated_at,
                       deadline, tags, script, description, contact_info, min_profit,
                       share_ratio, power_subsidy, period
                FROM orders
            ''')

            # 删除旧表
            cursor.execute('DROP TABLE orders')

            # 重命名新表
            cursor.execute('ALTER TABLE orders_new RENAME TO orders')

            conn.commit()
            print("✅ user_id 列已修改为允许NULL")
        else:
            print("\n✅ user_id 列已经是可空的")

        # 验证修复结果
        cursor.execute("PRAGMA table_info(orders)")
        columns = cursor.fetchall()
        user_id_col = [col for col in columns if col[1] == 'user_id'][0]

        print(f"\n修复后 user_id 列信息:")
        print(f"  列名: {user_id_col[1]}")
        print(f"  类型: {user_id_col[2]}")
        print(f"  是否NOT NULL: {user_id_col[3]}")
        print(f"  默认值: {user_id_col[4]}")

        conn.close()
        print("\n✅ orders 表修复完成！")

    except Exception as e:
        print(f"\n❌ orders 表修复失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    make_user_id_nullable()
