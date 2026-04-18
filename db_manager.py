#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库管理器 - 统一管理SQLite和MySQL连接
"""
import os
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    """数据库管理器，支持SQLite和MySQL"""
    
    _instance = None
    _db_type = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()
    
    def _load_config(self):
        """加载数据库配置"""
        from dotenv import load_dotenv
        load_dotenv()
        
        self._db_type = os.getenv('DB_TYPE', 'sqlite')
        
        if self._db_type == 'mysql':
            import pymysql
            self._config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', 3306)),
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD', ''),
                'database': os.getenv('DB_NAME', 'ciliai'),
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            }
        elif self._db_type == 'postgres':
            self._config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', 5432)),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', ''),
                'database': os.getenv('DB_NAME', 'ciliai')
            }
        else:
            self._db_type = 'sqlite'
            self._config = os.getenv('DB_PATH', 'fangtang.db')
    
    @property
    def db_type(self):
        return self._db_type
    
    def get_connection(self):
        """获取数据库连接"""
        if self._db_type == 'mysql':
            import pymysql
            return pymysql.connect(**self._config)
        else:
            conn = sqlite3.connect(self._config, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            return conn
    
    def init_database(self):
        """初始化数据库和表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self._db_type == 'mysql':
            self._create_tables_mysql(cursor)
        else:
            self._create_tables_sqlite(cursor)
        
        conn.commit()
        conn.close()
    
    def _create_tables_mysql(self, cursor):
        """MySQL建表语句"""
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
        
        for table_sql in tables:
            try:
                cursor.execute(table_sql)
            except Exception as e:
                print(f"建表错误（可能已存在）: {e}")
        
        # 创建索引
        indexes = [
            'CREATE INDEX idx_projects_user_id ON projects(user_id)',
            'CREATE INDEX idx_projects_status ON projects(status)',
            'CREATE INDEX idx_generation_records_user_id ON generation_records(user_id)',
            'CREATE INDEX idx_generation_records_project_id ON generation_records(project_id)',
            'CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id)',
            'CREATE INDEX idx_chat_messages_project_id ON chat_messages(project_id)',
            'CREATE INDEX idx_chat_messages_chat_id ON chat_messages(chat_id)',
            'CREATE INDEX idx_compute_power_logs_user_id ON compute_power_logs(user_id)',
            'CREATE INDEX idx_orders_status ON orders(status)',
            'CREATE INDEX idx_advertisements_status ON advertisements(status)',
            'CREATE INDEX idx_advertisements_sort_order ON advertisements(sort_order)',
            'CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id)',
            'CREATE INDEX idx_chat_sessions_project_id ON chat_sessions(project_id)'
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except:
                pass
    
    def _create_tables_sqlite(self, cursor):
        """SQLite建表语句"""
        cursor.execute('PRAGMA foreign_keys = ON')
        
        tables = [
            """CREATE TABLE IF NOT EXISTS users (
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
            )""",
            
            """CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                cover_image TEXT,
                status TEXT DEFAULT 'active',
                image_count INTEGER DEFAULT 0,
                chat_count INTEGER DEFAULT 0,
                total_power_used INTEGER DEFAULT 0,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                update_time TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )""",
            
            """CREATE TABLE IF NOT EXISTS generation_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                prompt TEXT,
                negative_prompt TEXT,
                image_url TEXT,
                image_width INTEGER,
                image_height INTEGER,
                image_size INTEGER,
                model_version TEXT,
                params TEXT,
                task_id TEXT,
                status TEXT DEFAULT 'completed',
                power_cost INTEGER DEFAULT 0,
                error_msg TEXT,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )""",
            
            """CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                user_id INTEGER NOT NULL,
                chat_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                token_count INTEGER DEFAULT 0,
                power_cost INTEGER DEFAULT 0,
                metadata TEXT,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )""",
            
            """CREATE TABLE IF NOT EXISTS compute_power_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project_id INTEGER,
                record_id INTEGER,
                operation_type TEXT NOT NULL,
                power_change INTEGER NOT NULL,
                power_before INTEGER NOT NULL,
                power_after INTEGER NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
            )""",
            
            """CREATE TABLE IF NOT EXISTS invite_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'active',
                compute_power INTEGER DEFAULT 1000,
                max_uses INTEGER DEFAULT 1,
                current_uses INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_at TIMESTAMP,
                created_by INTEGER
            )""",
            
            """CREATE TABLE IF NOT EXISTS ip_works (
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
                category TEXT DEFAULT 'IP版权库',
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                is_featured INTEGER DEFAULT 0,
                sort_order INTEGER DEFAULT 0
            )""",
            
            """CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                image TEXT,
                qrcode TEXT,
                price TEXT,
                deadline TEXT,
                status TEXT DEFAULT 'recruiting',
                tags TEXT,
                contact_count INTEGER DEFAULT 0,
                description TEXT,
                contact_info TEXT,
                min_profit REAL DEFAULT 0,
                share_ratio REAL DEFAULT 0,
                power_subsidy REAL DEFAULT 0,
                period INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )""",
            
            """CREATE TABLE IF NOT EXISTS advertisements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                image TEXT,
                link_url TEXT,
                status TEXT DEFAULT 'draft',
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )""",
            
            """CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                user_id INTEGER NOT NULL,
                conversation_id TEXT,
                title TEXT NOT NULL DEFAULT '新对话',
                selected_people TEXT DEFAULT 'script',
                message_count INTEGER DEFAULT 0,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                update_time TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )"""
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
        
        # SQLite索引
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)',
            'CREATE INDEX IF NOT EXISTS idx_generation_records_user_id ON generation_records(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_generation_records_project_id ON generation_records(project_id)',
            'CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_chat_messages_project_id ON chat_messages(project_id)',
            'CREATE INDEX IF NOT EXISTS idx_chat_messages_chat_id ON chat_messages(chat_id)',
            'CREATE INDEX IF NOT EXISTS idx_compute_power_logs_user_id ON compute_power_logs(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)',
            'CREATE INDEX IF NOT EXISTS idx_advertisements_status ON advertisements(status)',
            'CREATE INDEX IF NOT EXISTS idx_advertisements_sort_order ON advertisements(sort_order)',
            'CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_chat_sessions_project_id ON chat_sessions(project_id)'
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except:
                pass
    
    @contextmanager
    def get_db(self):
        """上下文管理器，获取数据库连接"""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, sql, params=None, fetch_one=False, fetch_all=False):
        """执行查询的统一方法"""
        with self.get_db() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return cursor
    
    def get_count(self, sql, params=None):
        """获取数量的统一方法"""
        result = self.execute_query(sql, params, fetch_one=True)
        if result:
            if self._db_type == 'mysql':
                return list(result.values())[0] if result else 0
            else:
                return result[0]
        return 0

# 全局实例
db_manager = DatabaseManager()
