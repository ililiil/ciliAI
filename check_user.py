import sqlite3

conn = sqlite3.connect('fangtang.db')
cursor = conn.cursor()

print("=" * 50)
print("查询邀请码 O99RUZE1 的用户:")
print("=" * 50)

cursor.execute('SELECT * FROM users WHERE invite_code = ?', ('O99RUZE1',))
result = cursor.fetchone()

if result:
    print(f"✓ 找到用户:")
    print(f"  ID: {result[0]}")
    print(f"  邀请码: {result[1]}")
    print(f"  算力: {result[2]}")
    print(f"  总使用算力: {result[3]}")
    print(f"  状态: {result[6]}")
else:
    print("✗ 未找到该邀请码对应的用户")

print("\n" + "=" * 50)
print("所有用户列表:")
print("=" * 50)

cursor.execute('SELECT id, invite_code, compute_power, status FROM users')
for row in cursor.fetchall():
    print(f"ID: {row[0]}, 邀请码: {row[1]}, 算力: {row[2]}, 状态: {row[3]}")

conn.close()
