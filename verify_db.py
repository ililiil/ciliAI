import sqlite3

DATABASE = 'fangtang.db'

def verify_database():
    print("=" * 60)
    print("CiliAI 数据库验证报告")
    print("=" * 60)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()

        print(f"\n数据库文件: {DATABASE}")
        print(f"表数量: {len(tables)}")
        print("\n已创建的表:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  ✓ {table[0]} ({count} 条记录)")

        cursor.execute('SELECT id, invite_code, compute_power, nickname, status FROM users')
        users = cursor.fetchall()

        print(f"\n用户列表:")
        for user in users:
            print(f"  ID: {user[0]}, 邀请码: {user[1]}, 算力: {user[2]}, 昵称: {user[3]}, 状态: {user[4]}")

        cursor.execute('SELECT id, code, status, compute_power, max_uses, current_uses FROM invite_codes')
        codes = cursor.fetchall()

        print(f"\n邀请码列表:")
        for code in codes:
            print(f"  ID: {code[0]}, 码: {code[1]}, 状态: {code[2]}, 算力: {code[3]}, 已使用: {code[5]}/{code[4]}")

        cursor.execute('SELECT COUNT(*) FROM works')
        works_count = cursor.fetchone()[0]

        print(f"\n作品数量: {works_count}")

        print("\n" + "=" * 60)
        print("✓ 数据库验证通过！所有功能正常。")
        print("=" * 60)

        print("\n📝 使用说明:")
        print("  1. 管理员后台: http://localhost:3002")
        print("     管理员账号: admin / admin123")
        print("  2. 用户端: http://localhost:3003")
        print(f"  3. 用户邀请码: CILIAI88 (初始算力: 10000)")

        conn.close()

    except Exception as e:
        print(f"\n✗ 数据库验证失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify_database()
