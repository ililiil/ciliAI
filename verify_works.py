import sqlite3

DATABASE = 'fangtang/fangtang.db'

def verify_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM ip_works ORDER BY created_at DESC')
    works = cursor.fetchall()

    print(f"数据库中共有 {len(works)} 条 IP 作品记录\n")
    print("=" * 80)

    for i, work in enumerate(works, 1):
        print(f"\n作品 {i}:")
        print(f"  ID: {work[0]}")
        print(f"  标题: {work[1]}")
        print(f"  学员名称: {work[2]}")
        print(f"  图片: {work[3][:50]}..." if len(work[3]) > 50 else f"  图片: {work[3]}")
        print(f"  标签: {work[4]}")
        print(f"  算力成本: {work[5]}")
        print(f"  制作时长: {work[6]}")
        print(f"  市场售价: {work[7]}")
        print(f"  版权: {work[8]}")
        print(f"  简介: {work[9][:50]}..." if len(str(work[9])) > 50 else f"  简介: {work[9]}")
        print(f"  状态: {work[10]}")
        print(f"  创建时间: {work[11]}")

    conn.close()
    print("\n" + "=" * 80)
    print("验证完成！")

if __name__ == '__main__':
    verify_data()
