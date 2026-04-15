import sqlite3

DATABASE = 'fangtang.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("数据库表:")
for table in tables:
    print(f"  - {table[0]}")
print(f"\n总计: {len(tables)} 个表")

for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"\n{table_name} 表结构:")
    for col in columns:
        print(f"  - {col[1]}: {col[2]}")

conn.close()
