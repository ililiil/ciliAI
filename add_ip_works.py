import sqlite3
import json
import random

DATABASE = 'fangtang/fangtang.db'

def add_ip_works():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            student_name TEXT,
            image TEXT,
            tags TEXT,
            cost TEXT,
            duration TEXT,
            price TEXT,
            copyright TEXT,
            introduction TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    ip_works = [
        {
            'title': '星际穿越者',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1001',
            'tags': ['科幻', '冒险', 'AI生成'],
            'cost': '150',
            'duration': '180',
            'price': '299',
            'copyright': '番茄小说',
            'introduction': '讲述人类在宇宙中寻找新家园的史诗故事。'
        },
        {
            'title': '时光旅行者',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1002',
            'tags': ['悬疑', '穿越', 'AI生成'],
            'cost': '140',
            'duration': '160',
            'price': '259',
            'copyright': '番茄小说',
            'introduction': '一个普通人意外获得穿越时空的能力，改变命运的故事。'
        },
        {
            'title': '都市猎人',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1003',
            'tags': ['动作', '都市', 'AI生成'],
            'cost': '135',
            'duration': '150',
            'price': '249',
            'copyright': '番茄小说',
            'introduction': '现代都市中的神秘猎人，面对黑暗势力的挑战。'
        },
        {
            'title': '修仙之路',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1004',
            'tags': ['玄幻', '修仙', 'AI生成'],
            'cost': '160',
            'duration': '200',
            'price': '399',
            'copyright': '番茄小说',
            'introduction': '一个平凡少年的修仙之旅，历经磨难终成大道。'
        },
        {
            'title': '爱情公寓',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1005',
            'tags': ['爱情', '喜剧', 'AI生成'],
            'cost': '120',
            'duration': '140',
            'price': '199',
            'copyright': '番茄小说',
            'introduction': '一群年轻人在公寓里的欢乐日常和爱情故事。'
        },
        {
            'title': '盗墓笔记',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1006',
            'tags': ['探险', '悬疑', 'AI生成'],
            'cost': '145',
            'duration': '170',
            'price': '279',
            'copyright': '番茄小说',
            'introduction': '深入古墓，探索未知世界的冒险故事。'
        },
        {
            'title': '宫廷剧',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1007',
            'tags': ['古风', '宫斗', 'AI生成'],
            'cost': '155',
            'duration': '185',
            'price': '329',
            'copyright': '番茄小说',
            'introduction': '古代宫廷中的权谋与爱情，精彩的宫斗大戏。'
        },
        {
            'title': '未来世界',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1008',
            'tags': ['科幻', '赛博朋克', 'AI生成'],
            'cost': '165',
            'duration': '195',
            'price': '359',
            'copyright': '番茄小说',
            'introduction': '2088年的未来世界，高科技与人类情感的碰撞。'
        },
        {
            'title': '武侠风云',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1009',
            'tags': ['武侠', '动作', 'AI生成'],
            'cost': '148',
            'duration': '175',
            'price': '289',
            'copyright': '番茄小说',
            'introduction': '江湖恩怨，刀光剑影，一代武侠的传奇故事。'
        },
        {
            'title': '校园青春',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1010',
            'tags': ['青春', '校园', 'AI生成'],
            'cost': '110',
            'duration': '130',
            'price': '179',
            'copyright': '番茄小说',
            'introduction': '青春洋溢的校园生活，友情与爱情的美好时光。'
        },
        {
            'title': '破案高手',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1011',
            'tags': ['刑侦', '悬疑', 'AI生成'],
            'cost': '138',
            'duration': '158',
            'price': '269',
            'copyright': '番茄小说',
            'introduction': '天才侦探破解一个又一个棘手的案件。'
        },
        {
            'title': '商战精英',
            'student_name': '方塘官方',
            'image': 'https://picsum.photos/400/600?random=1012',
            'tags': ['商战', '职场', 'AI生成'],
            'cost': '142',
            'duration': '165',
            'price': '259',
            'copyright': '番茄小说',
            'introduction': '商场如战场，精英们的智慧与胆识较量。'
        }
    ]

    for work in ip_works:
        try:
            cursor.execute('''
                INSERT INTO ip_works (title, student_name, image, tags, cost, duration, price, copyright, introduction)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                work['title'],
                work['student_name'],
                work['image'],
                json.dumps(work['tags']),
                work['cost'],
                work['duration'],
                work['price'],
                work['copyright'],
                work['introduction']
            ))
            print(f"✓ 添加作品: {work['title']}")
        except Exception as e:
            print(f"✗ 添加作品失败 {work['title']}: {e}")

    conn.commit()
    conn.close()
    print("\n成功添加 IP 版权作品！")

if __name__ == '__main__':
    add_ip_works()
