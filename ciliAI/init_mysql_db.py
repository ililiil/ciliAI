#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MySQL数据库初始化脚本 - 用于Docker部署
"""
import os
import sys
import time
import logging
import pymysql
from pymysql.cursors import DictCursor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_mysql(max_retries=30, retry_interval=2):
    """等待MySQL服务就绪"""
    db_host = os.getenv('DB_HOST', 'mysql')
    db_port = int(os.getenv('DB_PORT', 3306))
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')

    for i in range(max_retries):
        try:
            logger.info(f"尝试连接MySQL ({i+1}/{max_retries})...")
            conn = pymysql.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                db=os.getenv('DB_NAME', 'ciliai'),
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            conn.close()
            logger.info("MySQL连接成功！")
            return True
        except Exception as e:
            logger.warning(f"MySQL连接失败: {e}")
            if i < max_retries - 1:
                logger.info(f"等待 {retry_interval} 秒后重试...")
                time.sleep(retry_interval)
            else:
                logger.error("无法连接到MySQL数据库")
                return False

    return False

def init_mysql_database():
    """初始化MySQL数据库和表"""
    db_host = os.getenv('DB_HOST', 'mysql')
    db_port = int(os.getenv('DB_PORT', 3306))
    db_user = os.getenv('DB_USER', 'ciliai')
    db_password = os.getenv('DB_PASSWORD', 'ciliai_password')
    db_name = os.getenv('DB_NAME', 'ciliai')

    try:
        logger.info(f"连接MySQL: {db_host}:{db_port}/{db_name}")
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        cursor = conn.cursor()

        logger.info("创建数据库表...")

        tables = [
            """CREATE TABLE IF NOT EXISTS users (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS projects (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS generation_records (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS chat_messages (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS compute_power_logs (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS invite_codes (
                id INT PRIMARY KEY AUTO_INCREMENT,
                code VARCHAR(100) UNIQUE NOT NULL,
                status VARCHAR(50) DEFAULT 'active',
                compute_power INT DEFAULT 1000,
                max_uses INT DEFAULT 1,
                current_uses INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_at TIMESTAMP NULL,
                created_by INT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS ip_works (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS orders (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS advertisements (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(500) NOT NULL,
                image VARCHAR(500),
                link_url VARCHAR(500),
                status VARCHAR(50) DEFAULT 'draft',
                sort_order INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",

            """CREATE TABLE IF NOT EXISTS chat_sessions (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        ]

        for i, table_sql in enumerate(tables, 1):
            try:
                cursor.execute(table_sql)
                logger.info(f"✓ 表 {i}/{len(tables)} 创建完成")
            except Exception as e:
                logger.warning(f"表创建警告（可能已存在）: {e}")

        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        user_count = result['count'] if result else 0

        if user_count == 0:
            logger.info("创建初始数据...")
            import secrets
            from datetime import datetime

            invite_code = 'CILIAI88'
            cursor.execute('''
                INSERT INTO users (invite_code, compute_power, nickname, status)
                VALUES (%s, %s, %s, %s)
            ''', (invite_code, 10000, 'CiliAI管理员', 'active'))

            cursor.execute('SELECT LAST_INSERT_ID() as id')
            admin_id = cursor.fetchone()['id']

            for i in range(5):
                code = secrets.token_hex(4).upper()
                cursor.execute('''
                    INSERT INTO invite_codes (code, status, compute_power, max_uses, created_by)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (code, 'active', 1000, 10, admin_id))

            cursor.execute('''
                INSERT INTO advertisements (title, image, link_url, status, sort_order)
                VALUES (%s, %s, %s, %s, %s)
            ''', ('示例广告', '', '#', 'published', 1))

            conn.commit()
            logger.info("✓ 初始数据创建完成")
        else:
            logger.info("✓ 数据库已有数据，跳过初始化")

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        logger.info(f"\n✓ 数据库初始化完成！共 {len(tables)} 个表")

        for table in tables:
            table_name = list(table.values())[0]
            cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
            count = cursor.fetchone()['count']
            logger.info(f"  - {table_name}: {count} 条记录")

        conn.close()
        return True

    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    logger.info("=" * 60)
    logger.info("MySQL数据库初始化脚本")
    logger.info("=" * 60)

    if not wait_for_mysql():
        logger.error("无法连接到MySQL数据库，退出")
        sys.exit(1)

    if init_mysql_database():
        logger.info("✓ 数据库初始化成功！")
        sys.exit(0)
    else:
        logger.error("✗ 数据库初始化失败！")
        sys.exit(1)
