#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MySQL数据库初始化脚本
使用前请确保已创建数据库: CREATE DATABASE ciliai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'ciliai',
    'charset': 'utf8mb4'
}

def create_database():
    """创建数据库（如果不存在）"""
    config = DB_CONFIG.copy()
    db_name = config.pop('database')
    
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print(f"✓ 数据库 {db_name} 已创建或已存在")
    
    conn.close()

def init_tables():
    """初始化所有表"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    tables = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            invite_code VARCHAR(255) UNIQUE NOT NULL,
            compute_power INT DEFAULT 0,
            total_power_used INT DEFAULT 0,
            nickname VARCHAR(255),
            avatar VARCHAR(500),
            status VARCHAR(50) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL,
            last_active TIMESTAMP NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            title VARCHAR(500) NOT NULL,
            description TEXT,
            cover_image VARCHAR(500),
            status VARCHAR(50) DEFAULT 'active',
            image_count INT DEFAULT 0,
            chat_count INT DEFAULT 0,
            total_power_used INT DEFAULT 0,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS generation_records (
            id INT PRIMARY KEY AUTO_INCREMENT,
            project_id INT,
            user_id INT NOT NULL,
            type VARCHAR(50) NOT NULL,
            prompt TEXT,
            negative_prompt TEXT,
            image_url VARCHAR(500),
            image_width INT,
            image_height INT,
            image_size INT,
            model_version VARCHAR(100),
            params TEXT,
            task_id VARCHAR(200),
            status VARCHAR(50) DEFAULT 'completed',
            power_cost INT DEFAULT 0,
            error_msg TEXT,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INT PRIMARY KEY AUTO_INCREMENT,
            project_id INT,
            user_id INT NOT NULL,
            chat_id VARCHAR(200) NOT NULL,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            token_count INT DEFAULT 0,
            power_cost INT DEFAULT 0,
            metadata TEXT,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS compute_power_logs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            project_id INT,
            record_id INT,
            operation_type VARCHAR(100) NOT NULL,
            power_change INT NOT NULL,
            power_before INT NOT NULL,
            power_after INT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS invite_codes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            code VARCHAR(100) UNIQUE NOT NULL,
            status VARCHAR(50) DEFAULT 'active',
            compute_power INT DEFAULT 1000,
            max_uses INT DEFAULT 1,
            current_uses INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used_at TIMESTAMP NULL,
            created_by INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS ip_works (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(500) NOT NULL,
            student_name VARCHAR(200),
            image VARCHAR(500),
            tags TEXT,
            cost VARCHAR(50),
            duration VARCHAR(50),
            price VARCHAR(50),
            copyright TEXT,
            introduction TEXT,
            category VARCHAR(100) DEFAULT 'IP版权库',
            status VARCHAR(50) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL,
            is_featured INT DEFAULT 0,
            sort_order INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(500) NOT NULL,
            image VARCHAR(500),
            qrcode VARCHAR(500),
            price VARCHAR(50),
            deadline VARCHAR(100),
            status VARCHAR(50) DEFAULT 'recruiting',
            tags TEXT,
            contact_count INT DEFAULT 0,
            description TEXT,
            contact_info TEXT,
            min_profit DECIMAL(10,2) DEFAULT 0,
            share_ratio DECIMAL(5,2) DEFAULT 0,
            power_subsidy DECIMAL(10,2) DEFAULT 0,
            period INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS advertisements (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(500) NOT NULL,
            image VARCHAR(500),
            link_url VARCHAR(500),
            status VARCHAR(50) DEFAULT 'draft',
            sort_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """,
        """
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            project_id INT,
            user_id INT NOT NULL,
            conversation_id VARCHAR(200),
            title VARCHAR(500) NOT NULL DEFAULT '新对话',
            selected_people VARCHAR(50) DEFAULT 'script',
            message_count INT DEFAULT 0,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
    ]
    
    for i, table_sql in enumerate(tables, 1):
        try:
            cursor.execute(table_sql)
            print(f"✓ 表 {i}/10 创建成功")
        except Exception as e:
            print(f"✗ 表 {i}/10 创建失败: {e}")
    
    conn.commit()
    conn.close()
    print("\n✓ 所有表创建完成！")

if __name__ == '__main__':
    print("=" * 60)
    print("MySQL数据库初始化")
    print("=" * 60)
    
    create_database()
    init_tables()
    
    print("\n📝 使用说明:")
    print("1. 修改本文件中的 DB_CONFIG 配置")
    print("2. 确保MySQL服务已启动")
    print("3. 确保用户有创建数据库的权限")
    print("4. 运行后在.env中配置:")
    print("   DB_TYPE=mysql")
    print("   DB_HOST=localhost")
    print("   DB_PORT=3306")
    print("   DB_NAME=ciliai")
    print("   DB_USER=root")
    print("   DB_PASSWORD=your_password")
