import sqlite3

DATABASE = 'fangtang.db'

def fix_ip_works_user_id():
    print("=" * 60)
    print("修复 ip_works 表的 user_id 约束")
    print("=" * 60)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 检查当前 user_id 约束
        cursor.execute("PRAGMA table_info(ip_works)")
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
                CREATE TABLE ip_works_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    student_name TEXT,
                    image TEXT NOT NULL,
                    tags TEXT,
                    cost TEXT,
                    duration TEXT,
                    price TEXT,
                    copyright TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    introduction TEXT,
                    category TEXT,
                    is_featured INTEGER DEFAULT 0,
                    sort_order INTEGER DEFAULT 0
                )
            ''')

            # 复制数据
            cursor.execute('''
                INSERT INTO ip_works_new
                SELECT id, user_id, title, student_name, image, tags, cost, duration, price, copyright, status, created_at, updated_at, introduction, category, is_featured, sort_order
                FROM ip_works
            ''')

            # 删除旧表
            cursor.execute('DROP TABLE ip_works')

            # 重命名新表
            cursor.execute('ALTER TABLE ip_works_new RENAME TO ip_works')

            conn.commit()
            print("✅ user_id 列已修改为允许NULL")
        else:
            print("\n✅ user_id 列已经是可空的")

        # 验证修复结果
        cursor.execute("PRAGMA table_info(ip_works)")
        columns = cursor.fetchall()
        user_id_col = [col for col in columns if col[1] == 'user_id'][0]

        print(f"\n修复后 user_id 列信息:")
        print(f"  列名: {user_id_col[1]}")
        print(f"  类型: {user_id_col[2]}")
        print(f"  是否NOT NULL: {user_id_col[3]}")
        print(f"  默认值: {user_id_col[4]}")

        # 测试插入
        print("\n测试插入...")
        cursor.execute('''
            INSERT INTO ip_works (title, student_name, image)
            VALUES (?, ?, ?)
        ''', ('测试', '学员', 'https://example.com/test.jpg'))
        test_id = cursor.lastrowid
        conn.commit()

        print(f"✅ 测试插入成功! ID: {test_id}")

        # 删除测试数据
        cursor.execute('DELETE FROM ip_works WHERE id = ?', (test_id,))
        conn.commit()
        print("✅ 测试数据已删除")

        conn.close()
        print("\n✅ ip_works 表修复完成！")

    except Exception as e:
        print(f"\n❌ ip_works 表修复失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_ip_works_user_id()
