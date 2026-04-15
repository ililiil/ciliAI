import sqlite3

DATABASE = 'fangtang.db'

def check_database():
    print("=" * 60)
    print("检查数据库状态")
    print("=" * 60)

    try:
        conn = sqlite3.connect(DATABASE)
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()

        # 检查所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print(f"数据库文件: {DATABASE}")
        print(f"数据库文件中的表数量: {len(tables)}")
        print("\n表列表:")

        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} 条记录")

            # 检查表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"    列: {[col[1] for col in columns]}")

        # 检查users表
        cursor.execute("SELECT * FROM users LIMIT 1")
        user = cursor.fetchone()
        if user:
            print(f"\n示例用户: {user}")
        else:
            print("\n⚠️ users表为空")

        # 检查projects表
        cursor.execute("SELECT * FROM projects LIMIT 1")
        project = cursor.fetchone()
        if project:
            print(f"示例项目: {project}")
        else:
            print("⚠️ projects表为空")

        conn.close()
        print("\n✅ 数据库检查完成")

    except Exception as e:
        print(f"\n❌ 数据库检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_database()
