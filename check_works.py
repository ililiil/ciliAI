import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ciliAI', 'fangtang.db')

def check_works():
    if not os.path.exists(DATABASE):
        print(f"数据库文件不存在: {DATABASE}")
        return

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, student_name, category FROM ip_works ORDER BY id')
    works = cursor.fetchall()

    print(f"\n共有 {len(works)} 个作品:")
    print("\nID | 标题 | 学员名称 | 分类")
    print("-" * 80)
    for work_id, title, student_name, category in works:
        student_display = student_name if student_name else '(空)'
        category_display = category if category else '(空)'
        print(f"{work_id:3d} | {title[:30]:30s} | {student_display:20s} | {category_display}")

    cursor.execute('SELECT category, COUNT(*) FROM ip_works GROUP BY category')
    category_stats = cursor.fetchall()

    print("\n\n分类统计:")
    for category, count in category_stats:
        print(f"  {category}: {count} 个作品")

    conn.close()

if __name__ == '__main__':
    check_works()
