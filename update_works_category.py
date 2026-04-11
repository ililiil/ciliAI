import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fangtang', 'fangtang.db')

def update_all_works_category():
    if not os.path.exists(DATABASE):
        print(f"数据库文件不存在: {DATABASE}")
        return

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    print("正在重新设置所有作品的分类...")

    cursor.execute('SELECT id, student_name, category FROM ip_works ORDER BY id')
    all_works = cursor.fetchall()

    updated_count = 0
    for work_id, student_name, current_category in all_works:
        if not student_name or student_name == '方塘官方' or student_name == 'Fangtang Official':
            new_category = 'IP版权库'
        else:
            new_category = '社区分享'

        if current_category != new_category:
            cursor.execute('UPDATE ip_works SET category = ? WHERE id = ?', (new_category, work_id))
            updated_count += 1
            print(f"更新作品 {work_id}: student_name='{student_name}' -> category='{new_category}' (旧分类: '{current_category}')")

    conn.commit()

    print(f"\n当前共有 {len(all_works)} 个作品")

    cursor.execute('SELECT category, COUNT(*) FROM ip_works GROUP BY category')
    category_stats = cursor.fetchall()

    print("\n分类统计:")
    for category, count in category_stats:
        print(f"  {category}: {count} 个作品")

    print(f"\n共更新了 {updated_count} 个作品")

    conn.close()

if __name__ == '__main__':
    update_all_works_category()
