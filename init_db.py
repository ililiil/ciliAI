import sqlite3
import hashlib
import secrets
from datetime import datetime

DATABASE = 'fangtang.db'

def init_database():
    print("正在初始化数据库...")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invite_code TEXT UNIQUE NOT NULL,
            compute_power INTEGER DEFAULT 0,
            total_power_used INTEGER DEFAULT 0,
            nickname TEXT,
            avatar TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            last_active TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            cover_image TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generation_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_id INTEGER,
            type TEXT NOT NULL,
            prompt TEXT,
            image_url TEXT,
            status TEXT DEFAULT 'pending',
            compute_power INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            task_id TEXT,
            power_cost INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invite_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'active',
            compute_power INTEGER DEFAULT 1000,
            max_uses INTEGER DEFAULT 1,
            current_uses INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used_at TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            image TEXT,
            qrcode TEXT,
            price TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS power_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            operation TEXT NOT NULL,
            power_change INTEGER NOT NULL,
            before_power INTEGER,
            after_power INTEGER,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            student_name TEXT,
            image TEXT,
            tags TEXT,
            cost TEXT,
            duration TEXT,
            price TEXT,
            copyright TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            introduction TEXT,
            category TEXT DEFAULT 'IP版权库',
            is_featured INTEGER DEFAULT 0,
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS advertisements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image TEXT,
            link_url TEXT,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            published_at TIMESTAMP
        )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_generation_records_user_id ON generation_records(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_generation_records_project_id ON generation_records(project_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_generation_records_type ON generation_records(type)')

    conn.commit()

    print("✓ 数据库表创建完成")

    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        print("正在创建初始数据...")
        invite_code = 'CILIAI88'
        cursor.execute('''
            INSERT INTO users (invite_code, compute_power, nickname, status)
            VALUES (?, ?, ?, ?)
        ''', (invite_code, 10000, 'CiliAI管理员', 'active'))

        cursor.execute('SELECT id FROM users WHERE invite_code = ?', (invite_code,))
        admin_id = cursor.fetchone()[0]

        for i in range(5):
            code = secrets.token_hex(4).upper()
            cursor.execute('''
                INSERT INTO invite_codes (code, status, compute_power, max_uses, created_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (code, 'active', 1000, 10, admin_id))

        cursor.execute('''
            INSERT INTO ip_works (user_id, title, student_name, image, tags, cost, duration, price, copyright, introduction, category, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (admin_id, '示例作品1', '学生A', '/uploads/sample1.jpg', '["AI创作", "示例"]', '5', '30秒', '99', '归CiliAI所有', '这是一个示例作品', 'IP版权库', 'active'))

        conn.commit()
        print("✓ 初始数据创建完成")
        print(f"  - 管理员账户邀请码: {invite_code} (算力: 10000)")
        print("  - 创建了5个测试邀请码")
        print("  - 创建了示例作品")
    else:
        print("✓ 数据库已有数据，跳过初始化")

    conn.close()
    print("\n数据库初始化完成！")

if __name__ == '__main__':
    init_database()
