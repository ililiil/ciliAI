import os
import io
import time
import json
import logging
import hashlib
import uuid
import base64
from datetime import datetime
import requests as req_lib
from flask import Flask, request, jsonify, send_from_directory, g, Response, stream_with_context, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from volcengine.visual.VisualService import VisualService
from key_manager import key_manager

try:
    from PIL import Image
except ImportError:
    logger.error("Pillow library is required for image processing. Please install it with: pip install Pillow")
    Image = None

load_dotenv()

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pymysql
pymysql.install_as_MySQLdb()
DATABASE = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'ciliai'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

logger.info(f"数据库: {DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}")

ADMIN_BASE_URL = os.getenv('ADMIN_BASE_URL', 'http://localhost:5002')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_image_url(image_url):
    """转换图片URL，将管理后台上传的图片路径转换为完整URL"""
    if not image_url or not isinstance(image_url, str):
        return image_url

    image_url = image_url.strip()

    if not image_url:
        return image_url

    if image_url.startswith('/uploads/'):
        return f"http://localhost:5001{image_url}"

    return image_url

def convert_rgba_to_grayscale_mask(base64_image):
    """
    将RGBA格式的mask图像转换为单通道灰度图
    
    参数:
        base64_image: 原始图像的base64编码（可能是PNG或带alpha通道的格式）
    
    返回:
        转换后的单通道灰度图base64编码
    
    说明:
        - 白色区域(255) = 待重绘区域
        - 黑色区域(0) = 保持原样
    """
    if Image is None:
        raise RuntimeError("Pillow library is not installed. Cannot process images.")
    
    try:
        logger.info(f"开始转换mask，输入base64长度: {len(base64_image)}")
        
        # 移除base64前缀（如果有）
        if ',' in base64_image:
            logger.info("检测到base64带前缀，移除前缀")
            base64_image = base64_image.split(',')[1]
        
        logger.info(f"解码base64，长度: {len(base64_image)}")
        
        # 解码base64
        image_data = base64.b64decode(base64_image)
        logger.info(f"解码后数据大小: {len(image_data)} bytes")
        
        # 用PIL打开图像
        img = Image.open(io.BytesIO(image_data))
        logger.info(f"图像打开成功: 尺寸={img.size}, 模式={img.mode}, 格式={img.format}")
        
        # 转换为RGB模式（如果是RGBA或其他模式）
        original_mode = img.mode
        if img.mode != 'RGB':
            logger.info(f"转换模式从 {img.mode} 到 RGB")
            img = img.convert('RGB')
        
        logger.info(f"RGB转换完成: 尺寸={img.size}, 模式={img.mode}")
        
        # 将RGB转换为灰度图（L模式）
        # PIL的convert('L')会将图像转换为单通道灰度
        # 白色像素(255,255,255) -> 灰度值255（重绘区域）
        # 黑色像素(0,0,0) -> 灰度值0（保持区域）
        gray_img = img.convert('L')
        logger.info(f"灰度转换完成: 尺寸={gray_img.size}, 模式={gray_img.mode}")
        
        # 检查灰度图的像素值范围
        extrema = gray_img.getextrema()
        logger.info(f"灰度图像素值范围: 最小值={extrema[0]}, 最大值={extrema[1]}")
        
        # 转换回base64
        output_buffer = io.BytesIO()
        # 使用PNG格式保存（支持灰度图）
        gray_img.save(output_buffer, format='PNG')
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        logger.info(f"Mask转换成功: {original_mode} -> {gray_img.mode}, 输出base64长度: {len(output_base64)}")
        return output_base64
        
    except Exception as e:
        logger.error(f"Mask转换失败: {str(e)}")
        import traceback
        logger.error(f"详细错误: {traceback.format_exc()}")
        raise RuntimeError(f"Mask图像转换失败: {str(e)}")

def resize_image_to_fit_api_requirements(base64_image, max_size_mb=4.0, max_dimension=4096):
    """
    调整图片大小和压缩以符合API要求
    
    参数:
        base64_image: 图片的base64编码
        max_size_mb: 最大文件大小（MB），默认4.0（留点余量）
        max_dimension: 最大尺寸（宽或高），默认4096
    
    返回:
        调整后的图片base64编码
    
    说明:
        - API要求：最大4.7MB，最大分辨率4096x4096
        - 使用JPEG格式以减小文件大小
    """
    if Image is None:
        raise RuntimeError("Pillow library is not installed. Cannot process images.")
    
    try:
        logger.info(f"开始调整图片大小，输入base64长度: {len(base64_image)}")
        
        # 移除base64前缀（如果有）
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        
        # 解码base64
        image_data = base64.b64decode(base64_image)
        logger.info(f"解码后数据大小: {len(image_data)} bytes ({len(image_data)/1024/1024:.2f} MB)")
        
        # 用PIL打开图像
        img = Image.open(io.BytesIO(image_data))
        logger.info(f"原始图像: 尺寸={img.size}, 模式={img.mode}, 格式={img.format}")
        
        original_width, original_height = img.size
        
        # 调整大小
        needs_resize = False
        if original_width > max_dimension or original_height > max_dimension:
            logger.info(f"图像尺寸超过限制，需要缩放")
            needs_resize = True
            # 计算缩放比例
            ratio = min(max_dimension / original_width, max_dimension / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"图像已缩放: {original_width}x{original_height} -> {new_width}x{new_height}")
        
        # 转换为RGB（如果是RGBA或其他模式）
        if img.mode not in ('RGB', 'JPEG'):
            img = img.convert('RGB')
        
        # 压缩到目标大小
        max_size_bytes = int(max_size_mb * 1024 * 1024)
        
        # 尝试不同的质量等级找到最佳压缩率
        quality = 95
        min_quality = 60
        
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG', quality=quality, optimize=True)
        current_size = len(output_buffer.getvalue())
        logger.info(f"初始压缩(quality={quality}): {current_size} bytes ({current_size/1024/1024:.2f} MB)")
        
        # 如果还是太大，逐步降低质量
        while current_size > max_size_bytes and quality > min_quality:
            quality -= 5
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=quality, optimize=True)
            current_size = len(output_buffer.getvalue())
            logger.info(f"调整质量到 {quality}: {current_size} bytes ({current_size/1024/1024:.2f} MB)")
        
        # 如果JPEG还是太大，缩小图片尺寸
        while current_size > max_size_bytes:
            old_width, old_height = img.size
            new_width = int(old_width * 0.8)
            new_height = int(old_height * 0.8)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"缩小图像: {old_width}x{old_height} -> {new_width}x{new_height}")
            
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=quality, optimize=True)
            current_size = len(output_buffer.getvalue())
            logger.info(f"缩小后大小: {current_size} bytes ({current_size/1024/1024:.2f} MB)")
            
            # 防止无限循环
            if new_width < 256 or new_height < 256:
                break
        
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        logger.info(f"图片调整完成: 输出base64长度={len(output_base64)} ({len(output_base64)/1024/1024:.2f} MB)")
        
        return output_base64
        
    except Exception as e:
        logger.error(f"图片调整失败: {str(e)}")
        import traceback
        logger.error(f"详细错误: {traceback.format_exc()}")
        raise RuntimeError(f"图片调整失败: {str(e)}")

POWER_COST = {
    'generate': 5,
    'extend': 5,
    'super_resolution': 8,
    'inpaint': 5,
    'chat': 1
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        import pymysql
        db = g._database = pymysql.connect(**DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    import pymysql
    conn = pymysql.connect(**DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
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
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            cover_image TEXT,
            status VARCHAR(50) DEFAULT 'active',
            image_count INT DEFAULT 0,
            chat_count INT DEFAULT 0,
            total_power_used INT DEFAULT 0,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generation_records (
            id INT PRIMARY KEY AUTO_INCREMENT,
            project_id INT,
            user_id INT NOT NULL,
            type VARCHAR(50) NOT NULL,
            prompt TEXT,
            negative_prompt TEXT,
            image_url TEXT,
            image_width INT,
            image_height INT,
            image_size INT,
            model_version VARCHAR(50),
            params TEXT,
            task_id VARCHAR(255),
            status VARCHAR(50) DEFAULT 'completed',
            power_cost INT DEFAULT 0,
            error_msg TEXT,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INT PRIMARY KEY AUTO_INCREMENT,
            project_id INT,
            user_id INT NOT NULL,
            chat_id VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            token_count INT DEFAULT 0,
            power_cost INT DEFAULT 0,
            metadata TEXT,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compute_power_logs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            project_id INT,
            record_id INT,
            operation_type VARCHAR(50) NOT NULL,
            power_change INT NOT NULL,
            power_before INT NOT NULL,
            power_after INT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
            FOREIGN KEY (record_id) REFERENCES generation_records (id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invite_codes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            code VARCHAR(255) UNIQUE NOT NULL,
            status VARCHAR(50) DEFAULT 'active',
            compute_power INT DEFAULT 1000,
            max_uses INT DEFAULT 1,
            current_uses INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used_at TIMESTAMP NULL,
            created_by INT,
            FOREIGN KEY (created_by) REFERENCES users (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_works (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title TEXT NOT NULL,
            student_name TEXT,
            image TEXT,
            tags TEXT,
            cost VARCHAR(50),
            duration VARCHAR(50),
            price VARCHAR(50),
            copyright TEXT,
            introduction TEXT,
            category VARCHAR(100) DEFAULT 'IP版权库',
            status VARCHAR(50) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_generation_records_user_id ON generation_records(user_id)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_generation_records_project_id ON generation_records(project_id)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_generation_records_type ON generation_records(type)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_messages_project_id ON chat_messages(project_id)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_messages_chat_id ON chat_messages(chat_id)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_compute_power_logs_user_id ON compute_power_logs(user_id)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_compute_power_logs_created_at ON compute_power_logs(created_at)')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE projects ADD COLUMN status TEXT DEFAULT "active"')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE projects ADD COLUMN image_count INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE projects ADD COLUMN chat_count INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE projects ADD COLUMN total_power_used INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE projects ADD COLUMN update_time TIMESTAMP')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN total_power_used INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN last_active TIMESTAMP')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE generation_records ADD COLUMN power_cost INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE chat_messages ADD COLUMN power_cost INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE invite_codes ADD COLUMN current_uses INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE invite_codes ADD COLUMN max_uses INTEGER DEFAULT 1')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN status TEXT DEFAULT "active"')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN nickname TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN avatar TEXT')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE ip_works ADD COLUMN is_featured INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE ip_works ADD COLUMN sort_order INTEGER DEFAULT 0')
    except:
        pass
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title TEXT NOT NULL,
            image TEXT,
            qrcode TEXT,
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)')
    except:
        pass
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS advertisements (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title TEXT NOT NULL,
            image TEXT,
            link_url TEXT,
            status VARCHAR(50) DEFAULT 'draft',
            sort_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_advertisements_status ON advertisements(status)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_advertisements_sort_order ON advertisements(sort_order)')
    except:
        pass
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            project_id INT,
            user_id INT NOT NULL,
            conversation_id VARCHAR(255),
            title VARCHAR(255) NOT NULL DEFAULT '新对话',
            selected_people VARCHAR(50) DEFAULT 'script',
            message_count INT DEFAULT 0,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id)')
    except:
        pass
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_sessions_project_id ON chat_sessions(project_id)')
    except:
        pass
    
    cursor.execute('SELECT COUNT(*) as count FROM advertisements')
    ads_count = cursor.fetchone()[0]
    
    if ads_count == 0:
        default_ads = [
            {
                'title': '星际穿越者',
                'image': '/uploads/a0895e06216741b2a800efd7f215dad3.jpeg',
                'link_url': '',
                'status': 'published',
                'sort_order': 1
            },
            {
                'title': '古风仙侠传',
                'image': '/uploads/084d3791aad74c119e84bff831fdc820.jpeg',
                'link_url': '',
                'status': 'published',
                'sort_order': 2
            },
            {
                'title': '都市悬疑夜',
                'image': '/uploads/2267e536c2dc436aa8ae297ec1168d36.jpeg',
                'link_url': '',
                'status': 'published',
                'sort_order': 3
            }
        ]
        
        for ad in default_ads:
            try:
                cursor.execute('''
                    INSERT INTO advertisements (title, image, link_url, status, sort_order, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (ad['title'], ad['image'], ad['link_url'], ad['status'], ad['sort_order'], datetime.now(), datetime.now()))
            except Exception as e:
                logger.error(f"Error inserting default ad: {e}")
    
    default_codes = ["11111111", "22222222", "33333333", "44444444", "55555555",
                     "66666666", "77777777", "88888888", "99999999", "00000000"]
    for code in default_codes:
        try:
            cursor.execute('INSERT OR IGNORE INTO invite_codes (code, compute_power) VALUES (%s, %s, %s)', 
                          (code, 1000))
        except:
            pass
    
    cursor.execute('SELECT COUNT(*) as count FROM ip_works')
    ip_works_count = cursor.fetchone()[0]
    
    if ip_works_count == 0:
        default_ip_works = [
            {
                'title': '星际穿越者',
                'student_name': 'CiliAI官方',
                'image': 'https://picsum.photos/400/600?random=10',
                'tags': '["AI动画","现代科幻","穿越"]',
                'cost': '1000算力/分钟',
                'duration': '420分钟',
                'price': '150-300元/分钟',
                'copyright': '归CiliAI所有',
                'introduction': '一段跨越星际的冒险之旅，主角意外获得穿越时空的能力，在星际间展开一段惊心动魄的冒险故事。',
                'category': 'IP版权库'
            },
            {
                'title': '古风仙侠传',
                'student_name': 'CiliAI官方',
                'image': 'https://picsum.photos/400/600?random=11',
                'tags': '["AI动画","古风","仙侠"]',
                'cost': '1200算力/分钟',
                'duration': '600分钟',
                'price': '180-350元/分钟',
                'copyright': '归CiliAI所有',
                'introduction': '仙侠世界的史诗巨作，讲述修仙者历经磨难，最终悟道成仙的壮丽历程。画面精美，特效华丽。',
                'category': 'IP版权库'
            },
            {
                'title': '都市悬疑夜',
                'student_name': 'CiliAI官方',
                'image': 'https://picsum.photos/400/600?random=12',
                'tags': '["AI动画","都市","悬疑"]',
                'cost': '1100算力/分钟',
                'duration': '480分钟',
                'price': '160-320元/分钟',
                'copyright': '归CiliAI所有',
                'introduction': '都市背景的悬疑推理剧，层层递进的剧情，扣人心弦的谜题，让人欲罢不能。',
                'category': 'IP版权库'
            },
            {
                'title': 'AI创作者作品1',
                'student_name': 'AI爱好者小明',
                'image': 'https://picsum.photos/400/600?random=13',
                'tags': '["AI动画","创意","实验"]',
                'cost': '800算力/分钟',
                'duration': '300分钟',
                'price': '100-200元/分钟',
                'copyright': '归学员所有',
                'introduction': '学员使用AI工具创作的实验性作品，展现了AI在创意领域的无限可能。',
                'category': '社区分享'
            },
            {
                'title': 'AI创作者作品2',
                'student_name': '创意达人小红',
                'image': 'https://picsum.photos/400/600?random=14',
                'tags': '["AI动画","现代","情感"]',
                'cost': '900算力/分钟',
                'duration': '360分钟',
                'price': '120-250元/分钟',
                'copyright': '归学员所有',
                'introduction': '充满情感和创意的AI动画作品，展现了技术与人文的完美结合。',
                'category': '社区分享'
            },
            {
                'title': 'AI创作者作品3',
                'student_name': '技术宅阿杰',
                'image': 'https://picsum.photos/400/600?random=15',
                'tags': '["AI动画","科幻","未来"]',
                'cost': '950算力/分钟',
                'duration': '400分钟',
                'price': '140-280元/分钟',
                'copyright': '归学员所有',
                'introduction': '融合前沿AI技术的科幻作品，带你领略未来世界的无限魅力。',
                'category': '社区分享'
            }
        ]
        
        for idx, work in enumerate(default_ip_works):
            try:
                is_featured = 1 if idx < 3 else 0
                sort_order = idx if idx < 3 else 999
                cursor.execute('''
                    INSERT INTO ip_works (title, student_name, image, tags, cost, duration, price, copyright, introduction, category, is_featured, sort_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (work['title'], work['student_name'], work['image'], work['tags'], work['cost'], 
                     work['duration'], work['price'], work['copyright'], work['introduction'], work['category'],
                     is_featured, sort_order))
            except Exception as e:
                logger.error(f"Error inserting default ip work: {e}")
    
    conn.commit()
    conn.close()

init_db()

def get_user_by_invite_code(invite_code):
    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE invite_code = ?', (invite_code,))
    return cursor.fetchone()

def get_user_id_by_invite_code(invite_code):
    user = get_user_by_invite_code(invite_code)
    return user['id'] if user else None

def create_user(invite_code, compute_power=0):
    db = get_db()
    cursor = db.execute('INSERT INTO users (invite_code, compute_power) VALUES (%s, %s, %s)', 
                       (invite_code, compute_power))
    db.commit()
    return cursor.lastrowid

def get_or_create_user(invite_code):
    user = get_user_by_invite_code(invite_code)
    if user:
        return user['id']
    return create_user(invite_code)

def get_user_compute_power(user_id):
    db = get_db()
    user = db.execute('SELECT compute_power FROM users WHERE id = ?', (user_id,)).fetchone()
    return user['compute_power'] if user else 0

def deduct_compute_power(user_id, amount, operation_type, project_id=None, record_id=None, description=None):
    db = get_db()
    current_power = get_user_compute_power(user_id)
    
    if current_power < amount:
        return False, current_power
    
    new_power = current_power - amount
    
    db.execute('UPDATE users SET compute_power = ?, total_power_used = total_power_used + ?, last_active = ? WHERE id = ?',
               (new_power, amount, datetime.now(), user_id))
    
    db.execute('''
        INSERT INTO compute_power_logs 
        (user_id, project_id, record_id, operation_type, power_change, power_before, power_after, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (user_id, project_id, record_id, operation_type, -amount, current_power, new_power, description))
    
    if project_id:
        db.execute('UPDATE projects SET total_power_used = total_power_used + ?, update_time = ? WHERE id = ?',
                   (amount, datetime.now(), project_id))
    
    db.commit()
    return True, new_power

def add_compute_power(user_id, amount, operation_type, description=None):
    db = get_db()
    current_power = get_user_compute_power(user_id)
    new_power = current_power + amount
    
    db.execute('UPDATE users SET compute_power = ?, last_active = ? WHERE id = ?',
               (new_power, datetime.now(), user_id))
    
    db.execute('''
        INSERT INTO compute_power_logs 
        (user_id, operation_type, power_change, power_before, power_after, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (user_id, operation_type, amount, current_power, new_power, description))
    
    db.commit()
    return new_power

def get_visual_service():
    """获取配置了当前密钥的 VisualService 实例"""
    key_info = key_manager.get_next_key()
    if not key_info:
        raise ValueError("未找到有效的火山引擎密钥配置")

    service = VisualService()
    service.set_ak(key_info['ak'])
    service.set_sk(key_info['sk'])
    logger.info(f"使用密钥组 {key_info['index']} (AK: {key_info['ak'][:10]}...)")
    return service

def generate_invite_code(length=8, prefix=''):
    """生成邀请码
    
    Args:
        length: 总长度（包括前缀）
        prefix: 前缀字符串
    """
    import random
    import string
    
    chars = string.ascii_uppercase + string.digits
    chars = chars.replace('O', '').replace('0', '').replace('I', '').replace('1', '')
    
    code_length = max(length - len(prefix), 4)
    random_part = ''.join(random.choices(chars, k=code_length))
    
    full_code = f"{prefix}{random_part}" if prefix else random_part
    
    if len(full_code) < length:
        full_code = f"{prefix}{random_part}{'A' * (length - len(prefix) - code_length)}"
    
    return full_code.upper()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:fallback>')
def serve_frontend_fallback(fallback):
    """Catch-all route for SPA frontend routes"""
    if fallback.startswith('api/') or fallback.startswith('uploads/'):
        return jsonify({'error': 'Not found'}), 404
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/placeholder.png')
def serve_placeholder():
    """提供占位图片"""
    # 返回一个简单的 SVG 占位图
    svg = '''<svg width="400" height="225" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="225" fill="#cccccc"/>
        <text x="200" y="112.5" font-family="Arial" font-size="24" fill="#999999" 
              text-anchor="middle" dominant-baseline="middle">暂无图片</text>
    </svg>'''
    
    return send_file(
        io.BytesIO(svg.encode('utf-8')),
        mimetype='image/svg+xml',
        as_attachment=False,
        download_name='placeholder.svg'
    )

@app.route('/dify-api/chat-messages', methods=['POST'])
def dify_proxy():
    try:
        body = request.get_json()
        
        invite_code = body.get('invite_code')
        project_id = body.get('project_id')
        query = body.get('query', '')
        conversation_id = body.get('conversation_id', '')
        pre_deducted = body.get('pre_deducted', False)
        
        logger.info(f"========== Dify Proxy 请求开始 ==========")
        logger.info(f"邀请码: {invite_code}")
        logger.info(f"项目ID: {project_id}")
        logger.info(f"查询内容: {query[:100] if query else 'N/A'}...")
        logger.info(f"会话ID: {conversation_id if conversation_id else '(新会话)'}")
        logger.info(f"输入参数: {body.get('inputs', {})}")
        logger.info(f"算力已预扣减: {pre_deducted}")
        
        if not invite_code:
            logger.error("缺少邀请码参数")
            return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
        
        user_id = get_user_id_by_invite_code(invite_code)
        if not user_id:
            logger.error(f"用户不存在，邀请码: {invite_code}")
            return jsonify({'status': 'error', 'message': '用户不存在，请重新登录'}), 401
        
        logger.info(f"用户ID: {user_id}")
        
        power_cost = POWER_COST['chat']
        if not pre_deducted:
            success, remaining = deduct_compute_power(user_id, power_cost, 'chat', project_id, None, 
                                                       f"对话: {query[:30]}...")
            
            if not success:
                logger.warning(f"算力不足，用户ID: {user_id}, 当前算力: {remaining}，需要: {power_cost}")
                return jsonify({
                    'status': 'error',
                    'message': f'算力不足，当前算力 {remaining}，需要 {power_cost} 算力',
                    'power_required': power_cost,
                    'power_current': remaining
                }), 400
            
            logger.info(f"算力已扣除，当前剩余: {remaining}")
        else:
            remaining = get_user_compute_power(user_id)
            logger.info(f"算力已预扣减，跳过扣减步骤，当前剩余: {remaining}")
        
        dify_url = 'https://whhongyi.com.cn/v1/chat-messages'
        headers = {
            'Authorization': request.headers.get('Authorization', ''),
            'Content-Type': 'application/json'
        }
        
        dify_body = {
            'inputs': body.get('inputs', {}),
            'query': query,
            'response_mode': body.get('response_mode', 'streaming'),
            'user': body.get('user', f'user_{user_id}'),
            'files': body.get('files', [])
        }
        
        if body.get('conversation_id'):
            dify_body['conversation_id'] = body['conversation_id']
            logger.info(f"发送Dify请求，使用会话ID: {body['conversation_id']}")
        else:
            logger.info("发送Dify请求，创建新会话")
        
        logger.info(f"Dify API URL: {dify_url}")
        logger.info(f"Dify 请求体: {json.dumps(dify_body, ensure_ascii=False)[:200]}")
        
        try:
            resp = req_lib.post(dify_url, json=dify_body, headers=headers, stream=True, timeout=180)
            logger.info(f"Dify 上游响应状态: {resp.status_code}")
            logger.info(f"Dify 响应头: {dict(resp.headers)}")
        except req_lib.exceptions.Timeout:
            logger.error("❌ Dify API 请求超时（180秒）")
            add_compute_power(user_id, power_cost, 'refund', f'Dify API超时退还: {query[:30]}...')
            return jsonify({'status': 'error', 'message': 'Dify API 请求超时，请重试', 'refunded': True}), 504
        except req_lib.exceptions.ConnectionError as e:
            logger.error(f"❌ Dify API 连接错误: {str(e)}")
            add_compute_power(user_id, power_cost, 'refund', f'Dify API连接错误退还: {query[:30]}...')
            return jsonify({'status': 'error', 'message': f'Dify API 连接失败: {str(e)}', 'refunded': True}), 502
        except Exception as e:
            logger.error(f"❌ Dify API 请求失败: {str(e)}")
            add_compute_power(user_id, power_cost, 'refund', f'Dify API错误退还: {query[:30]}...')
            return jsonify({'status': 'error', 'message': f'Dify API 请求失败: {str(e)}', 'refunded': True}), 500
        
        if resp.status_code != 200:
            error_text = resp.text[:500]
            logger.error(f"❌ Dify 上游错误: {error_text}")
            add_compute_power(user_id, power_cost, 'refund', f'Dify API失败退还: {query[:30]}...')
            return jsonify({'status': 'error', 'message': f'Dify API error: {resp.status_code}', 'refunded': True}), resp.status_code
        
        logger.info(f"✅ Dify API 请求成功，开始流式响应")
        
        user_message_id = None
        conversation_id = body.get('conversation_id', '')
        
        def generate():
            nonlocal user_message_id, conversation_id
            
            db = get_db()
            db_created = True
            
            try:
                user_msg_cursor = db.execute('''
                    INSERT INTO chat_messages 
                    (project_id, user_id, chat_id, role, content, power_cost)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (project_id, user_id, conversation_id, 'user', query, power_cost))
                user_message_id = user_msg_cursor.lastrowid
                
                if project_id:
                    db.execute('UPDATE projects SET chat_count = chat_count + 1, update_time = ? WHERE id = ?',
                              (datetime.now(), project_id))
                
                db.commit()
                logger.info(f"✅ 已保存用户消息: {user_message_id}")
            except Exception as e:
                logger.error(f"❌ 保存用户消息失败: {str(e)}")
                db.rollback()
            
            ai_response_text = ''
            ai_message_id = None
            chunks_received = 0
            
            try:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        chunks_received += 1
                        yield chunk
                        
                        try:
                            chunk_str = chunk.decode('utf-8')
                            if chunk_str.startswith('data: '):
                                data_str = chunk_str[6:].strip()
                                if data_str and data_str != '[DONE]':
                                    try:
                                        data = json.loads(data_str)
                                        
                                        if data.get('event') in ['message', 'agent_message'] and data.get('answer'):
                                            ai_response_text += data['answer']
                                        
                                        if data.get('conversation_id') and not conversation_id:
                                            conversation_id = data['conversation_id']
                                            logger.info(f"✅ 收到新会话ID: {conversation_id}")
                                        
                                        if data.get('event') in ['message_end', 'done']:
                                            logger.info(f"✅ 收到消息结束事件")
                                            if not ai_message_id:
                                                try:
                                                    ai_msg_cursor = db.execute('''
                                                        INSERT INTO chat_messages 
                                                        (project_id, user_id, chat_id, role, content, power_cost)
                                                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                                                    ''', (project_id, user_id, conversation_id, 'assistant', ai_response_text, 0))
                                                    ai_message_id = ai_msg_cursor.lastrowid
                                                    db.commit()
                                                    logger.info(f"✅ 已保存AI消息: {ai_message_id}, 长度: {len(ai_response_text)}")
                                                except Exception as e:
                                                    logger.error(f"❌ 保存AI消息失败: {str(e)}")
                                                    db.rollback()
                                    except json.JSONDecodeError:
                                        continue
                        except UnicodeDecodeError:
                            continue
                
                logger.info(f"✅ 流式响应完成，共接收 {chunks_received} 个数据块")
            except Exception as e:
                logger.error(f"❌ 流式响应错误: {str(e)}")
                add_compute_power(user_id, power_cost, 'refund', f'流式响应异常退还: {query[:30]}...')
                yield f"data: {{'event': 'error', 'message': '{str(e)}'}}\n\n"
            finally:
                if not ai_message_id and ai_response_text:
                    try:
                        ai_msg_cursor = db.execute('''
                            INSERT INTO chat_messages 
                            (project_id, user_id, chat_id, role, content, power_cost)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ''', (project_id, user_id, conversation_id, 'assistant', ai_response_text, 0))
                        ai_message_id = ai_msg_cursor.lastrowid
                        db.commit()
                        logger.info(f"✅ 流结束时保存AI消息: {ai_message_id}")
                    except Exception as e:
                        logger.error(f"❌ 保存AI消息失败: {str(e)}")
                        db.rollback()
                try:
                    db.close()
                except:
                    pass
        
        logger.info(f"========== Dify Proxy 响应开始 ==========")
        
        return Response(
            stream_with_context(generate()),
            content_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'X-Power-Cost': str(power_cost),
                'X-Remaining-Power': str(remaining)
            }
        )
    except Exception as e:
        logger.error(f"❌ Dify Proxy 错误: {str(e)}")
        logger.error(f"错误堆栈: ", exc_info=True)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/verify-invite-code', methods=['POST'])
def verify_invite_code():
    data = request.json
    invite_code = data.get('invite_code', '').upper().strip()
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '请输入登录凭据'}), 400
    
    if len(invite_code) != 8:
        return jsonify({'status': 'error', 'message': '登录凭据必须为8位字符'}), 400
    
    db = get_db()
    
    existing_user = get_user_by_invite_code(invite_code)
    if existing_user:
        if existing_user['status'] == 'disabled':
            return jsonify({'status': 'error', 'message': '该账户已被禁用'}), 400
        
        db.execute('UPDATE users SET last_login = ? WHERE id = ?', (datetime.now(), existing_user['id']))
        db.commit()
        
        return jsonify({
            'status': 'success',
            'message': '登录成功',
            '算力': existing_user['compute_power'],
            'is_new_user': False
        })
    
    code_row = db.execute('SELECT * FROM invite_codes WHERE code = ?', (invite_code,)).fetchone()
    
    if not code_row:
        return jsonify({'status': 'error', 'message': '无效的邀请码，请联系管理员获取'}), 400
    
    if code_row['status'] == 'disabled':
        return jsonify({'status': 'error', 'message': '该邀请码已被禁用'}), 400
    
    compute_power = code_row['compute_power'] if code_row['compute_power'] else 1000
    
    user_id = create_user(invite_code, compute_power)
    
    db.execute('UPDATE invite_codes SET status = ?, used_at = ?, current_uses = current_uses + 1 WHERE code = ?',
               ('used', datetime.now(), invite_code))
    db.commit()
    
    add_compute_power(user_id, 0, 'init', f'用户注册，初始算力{compute_power}')
    
    return jsonify({
        'status': 'success',
        'message': '注册成功',
        '算力': compute_power,
        'is_new_user': True
    })

@app.route('/api/user/info', methods=['GET'])
def get_user_info():
    invite_code = request.args.get('invite_code')
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user = get_user_by_invite_code(invite_code)
    if not user:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 404
    
    db = get_db()
    project_count = db.execute('SELECT COUNT(*) as count FROM projects WHERE user_id = ?', (user['id'],)).fetchone()['count']
    image_count = db.execute('SELECT COUNT(*) as count FROM generation_records WHERE user_id = ?', (user['id'],)).fetchone()['count']
    
    return jsonify({
        'status': 'success',
        'data': {
            'invite_code': user['invite_code'],
            'compute_power': user['compute_power'],
            'total_power_used': user['total_power_used'],
            'project_count': project_count,
            'image_count': image_count,
            'created_at': user['created_at'],
            'last_login': user['last_login']
        }
    })

@app.route('/api/user/power', methods=['GET'])
def get_user_power():
    invite_code = request.args.get('invite_code')
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user = get_user_by_invite_code(invite_code)
    if not user:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 404
    
    return jsonify({
        'status': 'success',
        'compute_power': user['compute_power']
    })

@app.route('/api/power/deduct', methods=['POST'])
def deduct_power_only():
    """专门用于扣减算力的接口，不保存消息"""
    data = request.json
    invite_code = data.get('invite_code')
    project_id = data.get('project_id')
    message = data.get('message', '')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 401
    
    power_cost = POWER_COST['chat']
    success, remaining = deduct_compute_power(user_id, power_cost, 'chat', project_id, None, 
                                             f"对话: {message[:50]}...")
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': f'算力不足，当前算力 {remaining}，需要 {power_cost} 算力',
            'power_required': power_cost,
            'power_current': remaining
        }), 400
    
    return jsonify({
        'status': 'success',
        'power_cost': power_cost,
        'remaining_power': remaining
    })

@app.route('/api/user/power-logs', methods=['GET'])
def get_power_logs():
    invite_code = request.args.get('invite_code')
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 404
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    offset = (page - 1) * page_size
    
    db = get_db()
    logs = db.execute('''
        SELECT cpl.*, p.title as project_title
        FROM compute_power_logs cpl
        LEFT JOIN projects p ON cpl.project_id = p.id
        WHERE cpl.user_id = ?
        ORDER BY cpl.created_at DESC
        LIMIT ? OFFSET ?
    ''', (user_id, page_size, offset)).fetchall()
    
    total = db.execute('SELECT COUNT(*) as count FROM compute_power_logs WHERE user_id = ?', (user_id,)).fetchone()['count']
    
    return jsonify({
        'status': 'success',
        'data': {
            'list': [dict(log) for log in logs],
            'total': total,
            'page': page,
            'page_size': page_size
        }
    })

@app.route('/api/projects', methods=['GET'])
def get_projects():
    invite_code = request.args.get('invite_code')
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'success', 'projects': []})
    
    db = get_db()
    projects = db.execute('''
        SELECT p.*, 
               (SELECT COUNT(*) FROM generation_records WHERE project_id = p.id) as image_count,
               (SELECT COUNT(*) FROM chat_messages WHERE project_id = p.id) as chat_count
        FROM projects p
        WHERE p.user_id = ? AND p.status != 'deleted'
        ORDER BY p.update_time DESC
    ''', (user_id,)).fetchall()
    
    return jsonify({
        'status': 'success',
        'projects': [dict(p) for p in projects]
    })

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    invite_code = data.get('invite_code')
    title = data.get('title')
    description = data.get('description', '')
    cover_image = data.get('cover_image', '')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    if not title or not title.strip():
        return jsonify({'status': 'error', 'message': '项目标题不能为空'}), 400
    
    user_id = get_or_create_user(invite_code)
    
    db = get_db()
    cursor = db.execute('''
        INSERT INTO projects (user_id, title, description, cover_image)
        VALUES (%s, %s, %s, %s, %s)
    ''', (user_id, title.strip(), description, cover_image))
    db.commit()
    
    return jsonify({
        'status': 'success',
        'project_id': cursor.lastrowid,
        'message': '项目创建成功'
    })

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    invite_code = request.args.get('invite_code')
    
    db = get_db()
    project = db.execute('SELECT * FROM projects WHERE id = ? AND status != "deleted"', (project_id,)).fetchone()
    
    if not project:
        return jsonify({'status': 'error', 'message': '项目不存在'}), 404
    
    if invite_code:
        user_id = get_user_id_by_invite_code(invite_code)
        if user_id and project['user_id'] != user_id:
            return jsonify({'status': 'error', 'message': '无权访问此项目'}), 403
    
    generation_records = db.execute('''
        SELECT * FROM generation_records 
        WHERE project_id = ? 
        ORDER BY create_time DESC
        LIMIT 50
    ''', (project_id,)).fetchall()
    
    chat_messages = db.execute('''
        SELECT * FROM chat_messages 
        WHERE project_id = ? 
        ORDER BY create_time ASC
    ''', (project_id,)).fetchall()
    
    return jsonify({
        'status': 'success',
        'project': dict(project),
        'generation_records': [dict(r) for r in generation_records],
        'chat_messages': [dict(m) for m in chat_messages]
    })

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    db = get_db()
    
    project = db.execute('SELECT * FROM projects WHERE id = ? AND status != "deleted"', (project_id,)).fetchone()
    if not project:
        return jsonify({'status': 'error', 'message': '项目不存在'}), 404
    
    updates = []
    values = []
    
    if 'title' in data:
        updates.append('title = ?')
        values.append(data['title'])
    if 'description' in data:
        updates.append('description = ?')
        values.append(data['description'])
    if 'cover_image' in data:
        updates.append('cover_image = ?')
        values.append(data['cover_image'])
    
    if updates:
        updates.append('update_time = ?')
        values.append(datetime.now())
        values.append(project_id)
        
        db.execute(f'UPDATE projects SET {", ".join(updates)} WHERE id = ?', values)
        db.commit()
    
    return jsonify({'status': 'success', 'message': '项目更新成功'})

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    db = get_db()
    
    project = db.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
    if not project:
        return jsonify({'status': 'error', 'message': '项目不存在'}), 404
    
    db.execute('UPDATE projects SET status = "deleted" WHERE id = ?', (project_id,))
    db.commit()
    
    return jsonify({'status': 'success', 'message': '项目已删除'})

@app.route('/api/generate', methods=['POST'])
def generate_image():
    data = request.json
    invite_code = data.get('invite_code')
    project_id = data.get('project_id')
    prompt = data.get('prompt')

    logger.info(f"收到生图请求 - prompt: {prompt}, invite_code: {invite_code}, project_id: {project_id}")

    if not prompt:
        logger.warning("生图请求失败: 未提供提示词")
        return jsonify({'status': 'error', 'message': '请输入提示词'}), 400

    if not invite_code:
        logger.warning("生图请求失败: 未提供邀请码")
        return jsonify({'status': 'error', 'message': '请先登录'}), 401

    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        logger.warning(f"生图请求失败: 用户不存在，邀请码={invite_code}")
        return jsonify({'status': 'error', 'message': '用户不存在，请重新登录'}), 401

    logger.info(f"用户验证成功 - user_id: {user_id}")
    
    power_cost = POWER_COST['generate']
    success, remaining = deduct_compute_power(user_id, power_cost, 'generate', project_id, None, f'文生图: {prompt[:50]}...')
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': f'算力不足，当前算力 {remaining}，需要 {power_cost} 算力',
            'power_required': power_cost,
            'power_current': remaining
        }), 400
    
    params = {
        "req_key": "jimeng_seedream46_cvtob",
        "prompt": prompt,
        "width": data.get('width', 1024),
        "height": data.get('height', 1024)
    }

    try:
        logger.info(f"Submitting task for prompt: {prompt}")
        visual_service = get_visual_service()
        submit_res = visual_service.common_json_handler("CVSync2AsyncSubmitTask", params)

        if submit_res.get('code') != 10000:
            add_compute_power(user_id, power_cost, 'refund', f'生图失败退还: {prompt[:30]}...')
            return jsonify({'status': 'error', 'message': f"提交任务失败: {submit_res.get('message')}"}), 500

        task_id = submit_res.get('data', {}).get('task_id')
        if not task_id:
            add_compute_power(user_id, power_cost, 'refund', f'生图失败退还: {prompt[:30]}...')
            return jsonify({'status': 'error', 'message': "未获取到任务ID"}), 500

        logger.info(f"Polling results for task_id: {task_id}")
        max_retries = 30
        retry_interval = 2

        for i in range(max_retries):
            time.sleep(retry_interval)
            query_params = {
                "req_key": "jimeng_seedream46_cvtob",
                "task_id": task_id
            }
            query_res = visual_service.common_json_handler("CVSync2AsyncGetResult", query_params)
            
            resp_code = query_res.get('code')
            if resp_code == 10000:
                data_res = query_res.get('data', {})
                status = data_res.get('status')
                
                if status == 'done':
                    image_data = data_res.get('binary_data_base64', [])
                    if not image_data:
                        image_data = data_res.get('image_urls', [])
                    
                    image_urls = []
                    for img in image_data:
                        if isinstance(img, str) and not img.startswith('data:'):
                            img = f'data:image/png;base64,{img}'
                        image_urls.append(img)
                    
                    db = get_db()
                    cursor = db.execute('''
                        INSERT INTO generation_records 
                        (project_id, user_id, type, prompt, image_url, image_width, image_height, model_version, params, task_id, power_cost)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (project_id, user_id, 'generate', prompt, 
                          image_urls[0] if image_urls else None,
                          data.get('width', 1024), data.get('height', 1024),
                          'v4.0', json.dumps(params), task_id, power_cost))
                    record_id = cursor.lastrowid
                    
                    if project_id:
                        db.execute('UPDATE projects SET image_count = image_count + 1, update_time = ? WHERE id = ?',
                                   (datetime.now(), project_id))
                    
                    db.execute('''UPDATE compute_power_logs SET record_id = ? WHERE id = (
                        SELECT id FROM compute_power_logs WHERE user_id = ? AND operation_type = 'generate' 
                        ORDER BY created_at DESC LIMIT 1
                    )''', (record_id, user_id))
                    db.commit()
                    
                    return jsonify({
                        'status': 'success',
                        'task_id': task_id,
                        'images': image_urls,
                        'record_id': record_id,
                        'power_cost': power_cost,
                        'remaining_power': get_user_compute_power(user_id)
                    })
                elif status == 'failed':
                    add_compute_power(user_id, power_cost, 'refund', f'生图失败退还: {prompt[:30]}...')
                    return jsonify({'status': 'error', 'message': f"任务失败: {data_res.get('error_msg', '未知错误')}"}), 500
                else:
                    logger.info(f"Task {task_id} status: {status}, retrying...")
            elif resp_code == 10001:
                logger.info(f"Task {task_id} still processing...")
                continue
            else:
                add_compute_power(user_id, power_cost, 'refund', f'生图失败退还: {prompt[:30]}...')
                return jsonify({'status': 'error', 'message': f"查询失败: {query_res.get('message')}"}), 500
        
        add_compute_power(user_id, power_cost, 'refund', f'生图超时退还: {prompt[:30]}...')
        return jsonify({'status': 'error', 'message': "任务超时"}), 504

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        add_compute_power(user_id, power_cost, 'refund', f'生图异常退还: {prompt[:30]}...')
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/inpaint', methods=['POST'])
def inpaint_image():
    data = request.json
    invite_code = data.get('invite_code')
    project_id = data.get('project_id')
    image_base64 = data.get('image')
    mask_base64 = data.get('mask')
    prompt = data.get('prompt', '')
    
    if not image_base64:
        return jsonify({'status': 'error', 'message': '请上传图片'}), 400
    
    if not mask_base64:
        return jsonify({'status': 'error', 'message': '请绘制修改区域'}), 400
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '请先登录'}), 401
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在，请重新登录'}), 401
    
    power_cost = POWER_COST['inpaint']
    success, remaining = deduct_compute_power(user_id, power_cost, 'inpaint', project_id, None, f'改图: {prompt[:30] if prompt else "无提示词"}')
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': f'算力不足，当前算力 {remaining}，需要 {power_cost} 算力',
            'power_required': power_cost,
            'power_current': remaining
        }), 400

    # 转换mask为灰度图格式，并调整原图大小以符合API要求
    try:
        logger.info("="*50)
        logger.info("开始局部重绘处理")
        logger.info(f"输入图像base64长度: {len(image_base64)} ({len(image_base64)/1024/1024:.2f} MB)")
        logger.info(f"输入mask base64长度: {len(mask_base64)} ({len(mask_base64)/1024/1024:.2f} MB)")
        logger.info(f"提示词: {prompt[:50] if prompt else '无'}")
        logger.info("="*50)
        
        # 调整原图大小以符合API要求（最大4.7MB，最大4096x4096）
        logger.info("开始调整原图大小...")
        image_base64_resized = resize_image_to_fit_api_requirements(image_base64)
        logger.info(f"原图调整完成，调整后base64长度: {len(image_base64_resized)} ({len(image_base64_resized)/1024/1024:.2f} MB)")
        
        # 转换mask为灰度图格式
        logger.info("开始转换mask为灰度图...")
        mask_base64_converted = convert_rgba_to_grayscale_mask(mask_base64)
        logger.info(f"Mask转换完成，转换后base64长度: {len(mask_base64_converted)}")
    except Exception as e:
        logger.error(f"图像预处理失败: {str(e)}")
        add_compute_power(user_id, power_cost, 'refund', '图像预处理失败退还')
        return jsonify({'status': 'error', 'message': f'图像预处理失败: {str(e)}'}), 500

    params = {
        "req_key": "jimeng_image2image_dream_inpaint",
        "binary_data_base64": [image_base64_resized, mask_base64_converted],
        "prompt": prompt or "修改图片指定区域",
    }
    
    logger.info(f"准备提交API请求，二进制数据数组长度: {len(params['binary_data_base64'])}")
    logger.info(f"第一个图像base64长度: {len(params['binary_data_base64'][0])} ({len(params['binary_data_base64'][0])/1024/1024:.2f} MB)")
    logger.info(f"第二个mask base64长度: {len(params['binary_data_base64'][1])} ({len(params['binary_data_base64'][1])/1024/1024:.2f} MB)")

    try:
        logger.info(f"调用火山引擎API，提示词: {prompt[:50] if prompt else '无'}")
        visual_service = get_visual_service()
        logger.info("VisualService实例创建成功，开始提交任务...")
        submit_res = visual_service.common_json_handler("CVSync2AsyncSubmitTask", params)
        logger.info(f"API提交响应: code={submit_res.get('code')}, message={submit_res.get('message')}")
        logger.info(f"完整响应: {submit_res}")

        if submit_res.get('code') != 10000:
            add_compute_power(user_id, power_cost, 'refund', '改图失败退还')
            return jsonify({'status': 'error', 'message': f"提交任务失败: {submit_res.get('message')}"}), 500

        task_id = submit_res.get('data', {}).get('task_id')
        if not task_id:
            add_compute_power(user_id, power_cost, 'refund', '改图失败退还')
            return jsonify({'status': 'error', 'message': "未获取到任务ID"}), 500

        logger.info(f"Polling inpaint results for task_id: {task_id}")
        max_retries = 30
        retry_interval = 2

        for i in range(max_retries):
            time.sleep(retry_interval)
            query_params = {
                "req_key": "jimeng_image2image_dream_inpaint",
                "task_id": task_id
            }
            query_res = visual_service.common_json_handler("CVSync2AsyncGetResult", query_params)
            
            resp_code = query_res.get('code')
            if resp_code == 10000:
                data_res = query_res.get('data', {})
                status = data_res.get('status')
                
                if status == 'done':
                    image_data = data_res.get('binary_data_base64', [])
                    if not image_data:
                        image_data = data_res.get('image_urls', [])
                    
                    image_urls = []
                    for img in image_data:
                        if isinstance(img, str) and not img.startswith('data:'):
                            img = f'data:image/png;base64,{img}'
                        image_urls.append(img)
                    
                    db = get_db()
                    cursor = db.execute('''
                        INSERT INTO generation_records 
                        (project_id, user_id, type, prompt, image_url, params, task_id, power_cost)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (project_id, user_id, 'inpaint', prompt, 
                          image_urls[0] if image_urls else None,
                          json.dumps(params), task_id, power_cost))
                    record_id = cursor.lastrowid
                    
                    if project_id:
                        db.execute('UPDATE projects SET image_count = image_count + 1, update_time = ? WHERE id = ?',
                                   (datetime.now(), project_id))
                    db.commit()
                    
                    return jsonify({
                        'status': 'success',
                        'task_id': task_id,
                        'images': image_urls,
                        'record_id': record_id,
                        'power_cost': power_cost,
                        'remaining_power': get_user_compute_power(user_id)
                    })
                elif status == 'failed':
                    add_compute_power(user_id, power_cost, 'refund', '改图失败退还')
                    return jsonify({'status': 'error', 'message': f"任务失败: {data_res.get('error_msg', '未知错误')}"}), 500
            elif resp_code == 10001:
                continue
            else:
                add_compute_power(user_id, power_cost, 'refund', '改图失败退还')
                return jsonify({'status': 'error', 'message': f"查询失败: {query_res.get('message')}"}), 500
        
        add_compute_power(user_id, power_cost, 'refund', '改图超时退还')
        return jsonify({'status': 'error', 'message': "任务超时"}), 504

    except Exception as e:
        logger.error(f"="*50)
        logger.error(f"局部重绘API调用失败!")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"错误信息: {str(e)}")
        import traceback
        logger.error(f"详细堆栈: {traceback.format_exc()}")
        logger.error(f"="*50)
        add_compute_power(user_id, power_cost, 'refund', '改图异常退还')
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/extend', methods=['POST'])
def extend_image():
    data = request.json
    invite_code = data.get('invite_code')
    project_id = data.get('project_id')
    image_base64 = data.get('image')
    prompt = data.get('prompt', '')
    
    if not image_base64:
        return jsonify({'status': 'error', 'message': '请上传图片'}), 400
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '请先登录'}), 401
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在，请重新登录'}), 401
    
    power_cost = POWER_COST['extend']
    success, remaining = deduct_compute_power(user_id, power_cost, 'extend', project_id, None, f'扩图: {prompt[:30] if prompt else "无提示词"}')
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': f'算力不足，当前算力 {remaining}，需要 {power_cost} 算力',
            'power_required': power_cost,
            'power_current': remaining
        }), 400

    params = {
        "req_key": "jimeng_i2i_v30",
        "binary_data_base64": [image_base64],
        "prompt": prompt or "扩展图像，保持原有风格和质量",
        "width": data.get('width', 2048),
        "height": data.get('height', 2048)
    }

    try:
        logger.info(f"Submitting extend task")
        visual_service = get_visual_service()
        submit_res = visual_service.common_json_handler("CVSync2AsyncSubmitTask", params)
        
        if submit_res.get('code') != 10000:
            add_compute_power(user_id, power_cost, 'refund', '扩图失败退还')
            return jsonify({'status': 'error', 'message': f"提交任务失败: {submit_res.get('message')}"}), 500
        
        task_id = submit_res.get('data', {}).get('task_id')
        if not task_id:
            add_compute_power(user_id, power_cost, 'refund', '扩图失败退还')
            return jsonify({'status': 'error', 'message': "未获取到任务ID"}), 500

        max_retries = 30
        retry_interval = 2
        
        for i in range(max_retries):
            time.sleep(retry_interval)
            query_params = {
                "req_key": "jimeng_i2i_v30",
                "task_id": task_id
            }
            query_res = visual_service.common_json_handler("CVSync2AsyncGetResult", query_params)
            
            resp_code = query_res.get('code')
            if resp_code == 10000:
                data_res = query_res.get('data', {})
                status = data_res.get('status')
                
                if status == 'done':
                    image_data = data_res.get('binary_data_base64', [])
                    if not image_data:
                        image_data = data_res.get('image_urls', [])
                    
                    image_urls = []
                    for img in image_data:
                        if isinstance(img, str) and not img.startswith('data:'):
                            img = f'data:image/png;base64,{img}'
                        image_urls.append(img)
                    
                    db = get_db()
                    cursor = db.execute('''
                        INSERT INTO generation_records 
                        (project_id, user_id, type, prompt, image_url, image_width, image_height, params, task_id, power_cost)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (project_id, user_id, 'extend', prompt, 
                          image_urls[0] if image_urls else None,
                          data.get('width', 2048), data.get('height', 2048),
                          json.dumps(params), task_id, power_cost))
                    record_id = cursor.lastrowid
                    
                    if project_id:
                        db.execute('UPDATE projects SET image_count = image_count + 1, update_time = ? WHERE id = ?',
                                   (datetime.now(), project_id))
                    db.commit()
                    
                    return jsonify({
                        'status': 'success',
                        'task_id': task_id,
                        'images': image_urls,
                        'record_id': record_id,
                        'power_cost': power_cost,
                        'remaining_power': get_user_compute_power(user_id)
                    })
                elif status == 'failed':
                    add_compute_power(user_id, power_cost, 'refund', '扩图失败退还')
                    return jsonify({'status': 'error', 'message': f"任务失败: {data_res.get('error_msg', '未知错误')}"}), 500
            elif resp_code == 10001:
                continue
            else:
                add_compute_power(user_id, power_cost, 'refund', '扩图失败退还')
                return jsonify({'status': 'error', 'message': f"查询失败: {query_res.get('message')}"}), 500
        
        add_compute_power(user_id, power_cost, 'refund', '扩图超时退还')
        return jsonify({'status': 'error', 'message': "任务超时"}), 504

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        add_compute_power(user_id, power_cost, 'refund', '扩图异常退还')
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/super-resolution', methods=['POST'])
def super_resolution():
    data = request.json
    invite_code = data.get('invite_code')
    project_id = data.get('project_id')
    image_base64 = data.get('image')
    
    if not image_base64:
        return jsonify({'status': 'error', 'message': '请上传图片'}), 400
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '请先登录'}), 401
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在，请重新登录'}), 401
    
    power_cost = POWER_COST['super_resolution']
    success, remaining = deduct_compute_power(user_id, power_cost, 'super_resolution', project_id, None, '智能超清')
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': f'算力不足，当前算力 {remaining}，需要 {power_cost} 算力',
            'power_required': power_cost,
            'power_current': remaining
        }), 400

    params = {
        "req_key": "jimeng_i2i_seed3_tilesr_cvtob",
        "binary_data_base64": [image_base64],
        "resolution": data.get('resolution', '4k')
    }

    try:
        logger.info(f"Submitting super resolution task")
        visual_service = get_visual_service()
        submit_res = visual_service.common_json_handler("CVSync2AsyncSubmitTask", params)
        
        if submit_res.get('code') != 10000:
            add_compute_power(user_id, power_cost, 'refund', '超清失败退还')
            return jsonify({'status': 'error', 'message': f"提交任务失败: {submit_res.get('message')}"}), 500
        
        task_id = submit_res.get('data', {}).get('task_id')
        if not task_id:
            add_compute_power(user_id, power_cost, 'refund', '超清失败退还')
            return jsonify({'status': 'error', 'message': "未获取到任务ID"}), 500

        max_retries = 30
        retry_interval = 2
        
        for i in range(max_retries):
            time.sleep(retry_interval)
            query_params = {
                "req_key": "jimeng_i2i_seed3_tilesr_cvtob",
                "task_id": task_id
            }
            query_res = visual_service.common_json_handler("CVSync2AsyncGetResult", query_params)
            
            resp_code = query_res.get('code')
            if resp_code == 10000:
                data_res = query_res.get('data', {})
                status = data_res.get('status')
                
                if status == 'done':
                    image_data = data_res.get('binary_data_base64', [])
                    if not image_data:
                        image_data = data_res.get('image_urls', [])
                    
                    image_urls = []
                    for img in image_data:
                        if isinstance(img, str) and not img.startswith('data:'):
                            img = f'data:image/png;base64,{img}'
                        image_urls.append(img)
                    
                    db = get_db()
                    cursor = db.execute('''
                        INSERT INTO generation_records 
                        (project_id, user_id, type, image_url, params, task_id, power_cost)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (project_id, user_id, 'super_resolution', 
                          image_urls[0] if image_urls else None,
                          json.dumps(params), task_id, power_cost))
                    record_id = cursor.lastrowid
                    
                    if project_id:
                        db.execute('UPDATE projects SET image_count = image_count + 1, update_time = ? WHERE id = ?',
                                   (datetime.now(), project_id))
                    db.commit()
                    
                    return jsonify({
                        'status': 'success',
                        'task_id': task_id,
                        'images': image_urls,
                        'record_id': record_id,
                        'power_cost': power_cost,
                        'remaining_power': get_user_compute_power(user_id)
                    })
                elif status == 'failed':
                    add_compute_power(user_id, power_cost, 'refund', '超清失败退还')
                    return jsonify({'status': 'error', 'message': f"任务失败: {data_res.get('error_msg', '未知错误')}"}), 500
            elif resp_code == 10001:
                continue
            else:
                add_compute_power(user_id, power_cost, 'refund', '超清失败退还')
                return jsonify({'status': 'error', 'message': f"查询失败: {query_res.get('message')}"}), 500
        
        add_compute_power(user_id, power_cost, 'refund', '超清超时退还')
        return jsonify({'status': 'error', 'message': "任务超时"}), 504

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        add_compute_power(user_id, power_cost, 'refund', '超清异常退还')
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/records', methods=['GET'])
def get_records():
    invite_code = request.args.get('invite_code')
    project_id = request.args.get('project_id', type=int)
    record_type = request.args.get('type')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'success', 'records': [], 'total': 0})
    
    db = get_db()
    query = 'SELECT * FROM generation_records WHERE user_id = ?'
    params = [user_id]
    
    if project_id:
        query += ' AND project_id = ?'
        params.append(project_id)
    
    if record_type:
        query += ' AND type = ?'
        params.append(record_type)
    
    count_query = query.replace('SELECT *', 'SELECT COUNT(*) as count')
    total = db.execute(count_query, params).fetchone()['count']
    
    query += ' ORDER BY create_time DESC LIMIT ? OFFSET ?'
    params.extend([page_size, (page - 1) * page_size])
    
    records = db.execute(query, params).fetchall()
    
    records_list = []
    for r in records:
        record_dict = dict(r)
        if record_dict.get('image_url') and not record_dict['image_url'].startswith('data:'):
            record_dict['image_url'] = f"data:image/png;base64,{record_dict['image_url']}"
        records_list.append(record_dict)
    
    return jsonify({
        'status': 'success',
        'records': records_list,
        'total': total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    db = get_db()
    record = db.execute('SELECT * FROM generation_records WHERE id = ?', (record_id,)).fetchone()
    
    if not record:
        return jsonify({'status': 'error', 'message': '记录不存在'}), 404
    
    record_dict = dict(record)
    if record_dict.get('image_url') and not record_dict['image_url'].startswith('data:'):
        record_dict['image_url'] = f"data:image/png;base64,{record_dict['image_url']}"
    
    return jsonify({
        'status': 'success',
        'record': record_dict
    })

@app.route('/api/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    db = get_db()
    record = db.execute('SELECT * FROM generation_records WHERE id = ?', (record_id,)).fetchone()
    
    if not record:
        return jsonify({'status': 'error', 'message': '记录不存在'}), 404
    
    if record['project_id']:
        db.execute('UPDATE projects SET image_count = image_count - 1 WHERE id = ?', (record['project_id'],))
    
    db.execute('DELETE FROM generation_records WHERE id = ?', (record_id,))
    db.commit()
    
    return jsonify({'status': 'success', 'message': '记录已删除'})

@app.route('/api/chat/messages', methods=['GET'])
def get_chat_messages():
    project_id = request.args.get('project_id', type=int)
    chat_id = request.args.get('chat_id')
    invite_code = request.args.get('invite_code')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'success', 'messages': []})
    
    db = get_db()
    query = 'SELECT * FROM chat_messages WHERE user_id = ?'
    params = [user_id]
    
    if project_id:
        query += ' AND project_id = ?'
        params.append(project_id)
    
    if chat_id:
        query += ' AND chat_id = ?'
        params.append(chat_id)
    
    query += ' ORDER BY create_time ASC'
    
    messages = db.execute(query, params).fetchall()
    
    return jsonify({
        'status': 'success',
        'messages': [dict(msg) for msg in messages]
    })

@app.route('/api/chat/messages', methods=['POST'])
def save_chat_message():
    data = request.json
    invite_code = data.get('invite_code')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_or_create_user(invite_code)
    
    power_cost = POWER_COST['chat']
    success, remaining = deduct_compute_power(user_id, power_cost, 'chat', data.get('project_id'), None, 
                                               f"对话: {data.get('content', '')[:30]}...")
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': f'算力不足，当前算力 {remaining}，需要 {power_cost} 算力',
            'power_required': power_cost,
            'power_current': remaining
        }), 400
    
    db = get_db()
    cursor = db.execute('''
        INSERT INTO chat_messages 
        (project_id, user_id, chat_id, role, content, power_cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (data.get('project_id'), user_id, data.get('chat_id'),
          data.get('role'), data.get('content'), power_cost))
    
    if data.get('project_id'):
        db.execute('UPDATE projects SET chat_count = chat_count + 1, update_time = ? WHERE id = ?',
                   (datetime.now(), data.get('project_id')))
    
    db.commit()
    
    return jsonify({
        'status': 'success',
        'message_id': cursor.lastrowid,
        'power_cost': power_cost,
        'remaining_power': get_user_compute_power(user_id)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    invite_code = request.args.get('invite_code')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user = get_user_by_invite_code(invite_code)
    if not user:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 404
    
    db = get_db()
    
    project_count = db.execute('SELECT COUNT(*) as count FROM projects WHERE user_id = ? AND status != "deleted"', (user['id'],)).fetchone()['count']
    image_count = db.execute('SELECT COUNT(*) as count FROM generation_records WHERE user_id = ?', (user['id'],)).fetchone()['count']
    chat_count = db.execute('SELECT COUNT(*) as count FROM chat_messages WHERE user_id = ?', (user['id'],)).fetchone()['count']
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_power_used = db.execute('''
        SELECT COALESCE(SUM(ABS(power_change)), 0) as total 
        FROM compute_power_logs 
        WHERE user_id = ? AND power_change < 0 AND created_at >= ?
    ''', (user['id'], today_start)).fetchone()['total']
    
    return jsonify({
        'status': 'success',
        'data': {
            'compute_power': user['compute_power'],
            'total_power_used': user['total_power_used'],
            'project_count': project_count,
            'image_count': image_count,
            'chat_count': chat_count,
            'today_power_used': abs(today_power_used)
        }
    })

def is_valid_image_url(url):
    """检查是否为有效的图片 URL"""
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    if not url:
        return False
    
    if len(url) < 10:
        return False
    
    if url.startswith('data:image'):
        return True
    
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')
    valid_prefixes = ('http://', 'https://', '/')
    
    has_valid_prefix = any(url.lower().startswith(prefix) for prefix in valid_prefixes)
    has_valid_extension = any(url.lower().endswith(ext) for ext in valid_extensions)
    
    if url.startswith('data:'):
        return True
    
    return has_valid_prefix and (has_valid_extension or 'picsum.photos' in url or 'whhongyi' in url or 'baidu.com' in url)

DEFAULT_COVER_IMAGES = [
    'https://picsum.photos/400/600?random=1',
    'https://picsum.photos/400/600?random=2',
    'https://picsum.photos/400/600?random=3',
    'https://picsum.photos/400/600?random=4',
    'https://picsum.photos/400/600?random=5',
    'https://picsum.photos/400/600?random=6',
    'https://picsum.photos/400/600?random=7',
    'https://picsum.photos/400/600?random=8'
]

@app.route('/api/works', methods=['GET'])
def get_public_works():
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ip_works'")
        if not cursor.fetchone():
            logger.error("Table 'ip_works' does not exist in database")
            conn.close()
            return jsonify({
                'code': 404,
                'msg': 'IP works table does not exist. Please restart the application to initialize the database.',
                'data': {'list': [], 'total': 0}
            }), 404
        
        works = cursor.execute('''
            SELECT * FROM ip_works
            WHERE status = 'active'
            ORDER BY created_at DESC
        ''').fetchall()
        
        works_list = []
        for idx, work in enumerate(works):
            work_dict = dict(work)
            image_url = work_dict.get('image', '').strip() if work_dict.get('image') else ''

            if not image_url or image_url == '' or not is_valid_image_url(image_url):
                image_url = DEFAULT_COVER_IMAGES[idx % len(DEFAULT_COVER_IMAGES)]
            else:
                image_url = convert_image_url(image_url)

            work_dict['image'] = image_url
            works_list.append(work_dict)
        
        result = {
            'code': 200,
            'data': {
                'list': works_list,
                'total': len(works_list)
            }
        }
        
        conn.close()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error fetching works: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': 'Failed to fetch works',
            'error': str(e)
        }), 500

@app.route('/api/proxy-image', methods=['GET'])
def proxy_image():
    image_url = request.args.get('url')
    
    if not image_url:
        return jsonify({'status': 'error', 'message': '缺少图片URL'}), 400
    
    if not image_url.startswith('https://whhongyi.com.cn'):
        return jsonify({'status': 'error', 'message': '不支持的图片域名'}), 400
    
    try:
        logger.info(f"Proxying image request: {image_url[:80]}...")
        
        headers = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'Referer': 'https://whhongyi.com.cn/',
            'Origin': 'https://whhongyi.com.cn'
        }
        
        response = req_lib.get(image_url, headers=headers, stream=True, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"Image proxy failed: {response.status_code}")
            return jsonify({'status': 'error', 'message': f'获取图片失败: {response.status_code}'}), response.status_code
        
        content_type = response.headers.get('Content-Type', 'image/jpeg')
        
        return Response(
            response.iter_content(chunk_size=8192),
            content_type=content_type,
            headers={
                'Cache-Control': 'public, max-age=3600',
                'Content-Length': response.headers.get('Content-Length')
            }
        )
    except Exception as e:
        logger.error(f"Image proxy error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """上传图片接口，支持 Base64 编码或文件上传"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': '缺少上传数据'}), 400
        
        image_data = data.get('image')
        if not image_data:
            return jsonify({'status': 'error', 'message': '缺少图片数据'}), 400
        
        if image_data.startswith('data:image'):
            return jsonify({
                'status': 'success',
                'url': image_data,
                'message': '图片已接收（Base64格式）'
            })
        
        if image_data.startswith('http://') or image_data.startswith('https://'):
            return jsonify({
                'status': 'success',
                'url': image_data,
                'message': '图片URL已接收'
            })
        
        return jsonify({
            'status': 'success',
            'url': image_data,
            'message': '图片数据已接收'
        })
    except Exception as e:
        logger.error(f"Image upload error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/works/<int:work_id>/image', methods=['PUT'])
def update_work_image(work_id):
    """更新作品图片"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'status': 'error', 'message': '缺少图片数据'}), 400
        
        image_url = data['image']
        
        if not is_valid_image_url(image_url):
            return jsonify({'status': 'error', 'message': '无效的图片URL'}), 400
        
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM ip_works WHERE id = ?', (work_id,))
        work = cursor.fetchone()
        
        if not work:
            conn.close()
            return jsonify({'status': 'error', 'message': '作品不存在'}), 404
        
        cursor.execute('UPDATE ip_works SET image = ?, updated_at = ? WHERE id = ?', 
                      (image_url, datetime.now(), work_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '图片更新成功',
            'url': image_url
        })
    except Exception as e:
        logger.error(f"Update work image error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """获取所有订单"""
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM orders 
            ORDER BY created_at DESC
        ''')
        orders = cursor.fetchall()
        
        orders_list = []
        for order in orders:
            order_dict = dict(order)
            order_dict['id'] = order['id']
            
            image_url = order_dict.get('image', '').strip() if order_dict.get('image') else ''
            if not is_valid_image_url(image_url):
                image_url = DEFAULT_COVER_IMAGES[order['id'] % len(DEFAULT_COVER_IMAGES)]
            else:
                image_url = convert_image_url(image_url)
            order_dict['image'] = image_url
            
            if order_dict.get('contact_count') is not None:
                order_dict['contactCount'] = order_dict['contact_count']
            
            if order_dict.get('tags') and order_dict['tags']:
                try:
                    order_dict['tags'] = json.loads(order_dict['tags'])
                except:
                    order_dict['tags'] = []
            else:
                order_dict['tags'] = []
            
            orders_list.append(order_dict)
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                'list': orders_list,
                'total': len(orders_list)
            }
        })
    except Exception as e:
        logger.error(f"Get orders error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/works/featured', methods=['GET'])
def get_featured_works():
    """获取推荐作品，用于首页广告位"""
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM ip_works
            WHERE status = 'active' AND is_featured = 1
            ORDER BY sort_order ASC, created_at DESC
            LIMIT 3
        ''')
        works = cursor.fetchall()
        
        if len(works) < 3:
            cursor.execute('''
                SELECT * FROM ip_works
                WHERE status = 'active'
                ORDER BY created_at DESC
                LIMIT ?
            ''', (3 - len(works),))
            additional_works = cursor.fetchall()
            works = list(works) + list(additional_works)
        
        works_list = []
        for idx, work in enumerate(works):
            work_dict = dict(work)
            image_url = work_dict.get('image', '').strip() if work_dict.get('image') else ''

            if not image_url or not is_valid_image_url(image_url):
                image_url = DEFAULT_COVER_IMAGES[idx % len(DEFAULT_COVER_IMAGES)]
            else:
                image_url = convert_image_url(image_url)

            work_dict['image'] = image_url
            works_list.append(work_dict)
        
        conn.close()
        
        return jsonify({
            'code': 200,
            'data': {
                'list': works_list,
                'total': len(works_list)
            }
        })
    except Exception as e:
        logger.error(f"Get featured works error: {str(e)}")
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """创建新订单"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'status': 'error', 'message': '缺少订单标题'}), 400
        
        title = data['title']
        image = data.get('image', '')
        qrcode = data.get('qrcode', '')
        price = data.get('price', '')
        deadline = data.get('deadline', '')
        status = data.get('status', 'recruiting')
        tags = data.get('tags', [])
        description = data.get('description', '')
        contact_info = data.get('contact_info', '')
        min_profit = data.get('min_profit', 0)
        share_ratio = data.get('share_ratio', 0)
        power_subsidy = data.get('power_subsidy', 0)
        period = data.get('period', 0)
        
        invite_code = data.get('invite_code')
        user_id = None
        if invite_code:
            user_id = get_or_create_user(invite_code)
        
        if isinstance(tags, list):
            tags = json.dumps(tags, ensure_ascii=False)
        
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (user_id, title, image, qrcode, price, deadline, status, tags, description, contact_info, min_profit, share_ratio, power_subsidy, period)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, title, image, qrcode, price, deadline, status, tags, description, contact_info, min_profit, share_ratio, power_subsidy, period))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '订单创建成功',
            'order_id': order_id
        })
    except Exception as e:
        logger.error(f"Create order error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """更新订单"""
    try:
        data = request.get_json()
        
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return jsonify({'status': 'error', 'message': '订单不存在'}), 404
        
        title = data.get('title', order['title'])
        image = data.get('image', order['image'])
        qrcode = data.get('qrcode', order['qrcode'])
        price = data.get('price', order['price'])
        deadline = data.get('deadline', order['deadline'])
        status = data.get('status', order['status'])
        tags = data.get('tags', order['tags'])
        description = data.get('description', order['description'])
        contact_info = data.get('contact_info', order['contact_info'])
        min_profit = data.get('min_profit', order['min_profit'])
        share_ratio = data.get('share_ratio', order['share_ratio'])
        power_subsidy = data.get('power_subsidy', order['power_subsidy'])
        period = data.get('period', order['period'])
        
        if isinstance(tags, list):
            tags = json.dumps(tags, ensure_ascii=False)
        
        cursor.execute('''
            UPDATE orders SET 
                title = ?, image = ?, qrcode = ?, price = ?, deadline = ?, 
                status = ?, tags = ?, description = ?, contact_info = ?,
                min_profit = ?, share_ratio = ?, power_subsidy = ?, period = ?,
                updated_at = ?
            WHERE id = ?
        ''', (title, image, qrcode, price, deadline, status, tags, description, contact_info,
              min_profit, share_ratio, power_subsidy, period, datetime.now(), order_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '订单更新成功'
        })
    except Exception as e:
        logger.error(f"Update order error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """删除订单"""
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return jsonify({'status': 'error', 'message': '订单不存在'}), 404
        
        cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '订单删除成功'
        })
    except Exception as e:
        logger.error(f"Delete order error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/advertisements', methods=['GET'])
def get_advertisements():
    """获取所有广告位"""
    try:
        status = request.args.get('status', 'published')
        
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status == 'all':
            cursor.execute('''
                SELECT * FROM advertisements 
                ORDER BY sort_order ASC, created_at DESC
            ''')
        else:
            cursor.execute('''
                SELECT * FROM advertisements 
                WHERE status = ?
                ORDER BY sort_order ASC, created_at DESC
            ''', (status,))
        
        ads = cursor.fetchall()
        ads_list = []
        for ad in ads:
            ad_dict = dict(ad)
            if ad_dict.get('image'):
                ad_dict['image'] = convert_image_url(ad_dict['image'])
            ads_list.append(ad_dict)
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                'list': ads_list,
                'total': len(ads_list)
            }
        })
    except Exception as e:
        logger.error(f"Get advertisements error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/advertisements', methods=['POST'])
def create_advertisement():
    """创建广告位"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': '缺少广告数据'}), 400
        
        title = data.get('title', '')
        image = data.get('image', '')
        link_url = data.get('link_url', '')
        status = data.get('status', 'draft')
        sort_order = data.get('sort_order', 0)
        
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO advertisements (title, image, link_url, status, sort_order, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (title, image, link_url, status, sort_order, datetime.now(), datetime.now()))
        
        ad_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '广告位创建成功',
            'ad_id': ad_id
        })
    except Exception as e:
        logger.error(f"Create advertisement error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/advertisements/<int:ad_id>', methods=['PUT'])
def update_advertisement(ad_id):
    """更新广告位"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': '缺少广告数据'}), 400
        
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM advertisements WHERE id = ?', (ad_id,))
        ad = cursor.fetchone()
        
        if not ad:
            conn.close()
            return jsonify({'status': 'error', 'message': '广告位不存在'}), 404
        
        title = data.get('title', ad['title'])
        image = data.get('image', ad['image'])
        link_url = data.get('link_url', ad['link_url'])
        status = data.get('status', ad['status'])
        sort_order = data.get('sort_order', ad['sort_order'])
        
        cursor.execute('''
            UPDATE advertisements 
            SET title = ?, image = ?, link_url = ?, status = ?, sort_order = ?, updated_at = ?
            WHERE id = ?
        ''', (title, image, link_url, status, sort_order, datetime.now(), ad_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '广告位更新成功'
        })
    except Exception as e:
        logger.error(f"Update advertisement error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/advertisements/<int:ad_id>', methods=['DELETE'])
def delete_advertisement(ad_id):
    """删除广告位"""
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM advertisements WHERE id = ?', (ad_id,))
        ad = cursor.fetchone()
        
        if not ad:
            conn.close()
            return jsonify({'status': 'error', 'message': '广告位不存在'}), 404
        
        cursor.execute('DELETE FROM advertisements WHERE id = ?', (ad_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '广告位删除成功'
        })
    except Exception as e:
        logger.error(f"Delete advertisement error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/advertisements/<int:ad_id>/publish', methods=['POST'])
def publish_advertisement(ad_id):
    """发布广告位"""
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM advertisements WHERE id = ?', (ad_id,))
        ad = cursor.fetchone()
        
        if not ad:
            conn.close()
            return jsonify({'status': 'error', 'message': '广告位不存在'}), 404
        
        cursor.execute('''
            UPDATE advertisements 
            SET status = 'published', updated_at = ?
            WHERE id = ?
        ''', (datetime.now(), ad_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '广告位发布成功'
        })
    except Exception as e:
        logger.error(f"Publish advertisement error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/advertisements/<int:ad_id>/unpublish', methods=['POST'])
def unpublish_advertisement(ad_id):
    """下架广告位"""
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM advertisements WHERE id = ?', (ad_id,))
        ad = cursor.fetchone()
        
        if not ad:
            conn.close()
            return jsonify({'status': 'error', 'message': '广告位不存在'}), 404
        
        cursor.execute('''
            UPDATE advertisements 
            SET status = 'unpublished', updated_at = ?
            WHERE id = ?
        ''', (datetime.now(), ad_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '广告位下架成功'
        })
    except Exception as e:
        logger.error(f"Unpublish advertisement error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/advertisements/reorder', methods=['POST'])
def reorder_advertisements():
    """批量更新广告位排序"""
    try:
        data = request.get_json()
        
        if not data or 'orders' not in data:
            return jsonify({'status': 'error', 'message': '缺少排序数据'}), 400
        
        orders = data['orders']
        
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        
        for order_data in orders:
            ad_id = order_data.get('id')
            sort_order = order_data.get('sort_order')
            
            if ad_id is not None and sort_order is not None:
                cursor.execute('''
                    UPDATE advertisements 
                    SET sort_order = ?, updated_at = ?
                    WHERE id = ?
                ''', (sort_order, datetime.now(), ad_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': '排序更新成功'
        })
    except Exception as e:
        logger.error(f"Reorder advertisements error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== 管理后台 API ====================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == 'admin123':
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'token': 'admin-token-' + str(int(datetime.now().timestamp())),
                'username': 'admin'
            }
        })
    else:
        return jsonify({
            'code': 401,
            'msg': '用户名或密码错误'
        }), 401

@app.route('/api/admin/info', methods=['GET'])
def admin_info():
    return jsonify({
        'code': 200,
        'data': {
            'username': 'admin',
            'roles': ['admin']
        }
    })

@app.route('/api/admin/upload', methods=['POST'])
def admin_upload_image():
    if 'file' not in request.files:
        return jsonify({'code': 400, 'msg': '没有文件上传'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'code': 400, 'msg': '文件名为空'}), 400
    
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        image_url = f"/uploads/{filename}"
        return jsonify({
            'code': 200,
            'msg': '上传成功',
            'data': {
                'url': image_url,
                'filename': filename
            }
        })
    else:
        return jsonify({'code': 400, 'msg': '不支持的文件格式'}), 400

@app.route('/api/admin/invite-codes', methods=['GET'])
def get_admin_invite_codes():
    db = get_db()
    codes = db.execute('''
        SELECT ic.*, 
               (SELECT COUNT(*) FROM users WHERE invite_code = ic.code) as use_count
        FROM invite_codes ic
        ORDER BY ic.created_at DESC
    ''').fetchall()
    
    return jsonify({
        'code': 200,
        'data': {
            'list': [dict(code) for code in codes],
            'total': len(codes)
        }
    })

@app.route('/api/admin/invite-codes', methods=['POST'])
def create_admin_invite_code():
    data = request.json
    code = data.get('code')
    compute_power = data.get('compute_power', 1000)
    
    if not code:
        code = generate_invite_code(8)
    
    if len(code) < 4 or len(code) > 20:
        return jsonify({'code': 400, 'msg': '邀请码长度必须在4-20位之间'}), 400
    
    db = get_db()
    try:
        db.execute('INSERT INTO invite_codes (code, compute_power) VALUES (%s, %s, %s)', 
                   (code.upper(), compute_power))
        db.commit()
        return jsonify({'code': 200, 'msg': '创建成功', 'data': {'code': code.upper()}})
    except sqlite3.IntegrityError:
        return jsonify({'code': 400, 'msg': '邀请码已存在'}), 400

@app.route('/api/admin/invite-codes/<int:id>', methods=['PUT'])
def update_admin_invite_code(id):
    data = request.json
    db = get_db()
    
    code = db.execute('SELECT * FROM invite_codes WHERE id = ?', (id,)).fetchone()
    if not code:
        return jsonify({'code': 404, 'msg': '邀请码不存在'}), 404
    
    status = data.get('status', code['status'])
    compute_power = data.get('compute_power', code['compute_power'])
    
    db.execute('UPDATE invite_codes SET status = ?, compute_power = ? WHERE id = ?',
               (status, compute_power, id))
    db.commit()
    
    return jsonify({'code': 200, 'msg': '更新成功'})

@app.route('/api/admin/invite-codes/<int:id>', methods=['DELETE'])
def delete_admin_invite_code(id):
    db = get_db()
    
    code = db.execute('SELECT * FROM invite_codes WHERE id = ?', (id,)).fetchone()
    if not code:
        return jsonify({'code': 404, 'msg': '邀请码不存在'}), 404
    
    db.execute('DELETE FROM invite_codes WHERE id = ?', (id,))
    db.commit()
    
    return jsonify({'code': 200, 'msg': '删除成功'})

@app.route('/api/admin/invite-codes/batch', methods=['POST'])
def batch_create_admin_invite_codes():
    data = request.json
    count = data.get('count', 10)
    compute_power = data.get('compute_power', 1000)
    prefix = data.get('prefix', '').upper().strip()
    
    if count > 100:
        return jsonify({'code': 400, 'msg': '单次最多创建100个邀请码'}), 400
    
    db = get_db()
    created_codes = []
    attempts = 0
    max_attempts = count * 3
    
    code_length = 8 + len(prefix)
    
    while len(created_codes) < count and attempts < max_attempts:
        code = generate_invite_code(code_length, prefix)
        try:
            db.execute('INSERT INTO invite_codes (code, compute_power) VALUES (%s, %s, %s)',
                       (code, compute_power))
            created_codes.append(code)
        except sqlite3.IntegrityError:
            pass
        attempts += 1
    
    db.commit()
    
    return jsonify({
        'code': 200,
        'msg': f'成功创建 {len(created_codes)} 个邀请码' + (f'（前缀：{prefix}）' if prefix else ''),
        'data': {'codes': created_codes}
    })

@app.route('/api/admin/works', methods=['GET'])
def get_admin_works():
    db = get_db()
    works = db.execute('''
        SELECT * FROM ip_works
        ORDER BY created_at DESC
    ''').fetchall()
    
    return jsonify({
        'code': 200,
        'data': {
            'list': [dict(work) for work in works],
            'total': len(works)
        }
    })

@app.route('/api/admin/works', methods=['POST'])
def create_admin_work():
    data = request.json
    
    title = data.get('title')
    student_name = data.get('student_name')
    image = data.get('image')
    tags = data.get('tags', [])
    cost = data.get('cost', '')
    duration = data.get('duration', '')
    price = data.get('price', '')
    copyright = data.get('copyright', '归CiliAI所有')
    introduction = data.get('introduction', '')
    category = data.get('category', 'IP版权库')
    
    invite_code = data.get('invite_code')
    user_id = None
    if invite_code:
        user_id = get_or_create_user(invite_code)
    
    if not title or not image:
        return jsonify({'code': 400, 'msg': '标题和图片不能为空'}), 400
    
    if category not in ['IP版权库', '社区分享']:
        category = 'IP版权库'
    
    db = get_db()
    cursor = db.execute('''
        INSERT INTO ip_works (user_id, title, student_name, image, tags, cost, duration, price, copyright, introduction, category)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (user_id, title, student_name, image, json.dumps(tags), cost, duration, price, copyright, introduction, category))
    db.commit()
    
    return jsonify({
        'code': 200,
        'msg': '创建成功',
        'data': {'id': cursor.lastrowid}
    })

@app.route('/api/admin/works/<int:id>', methods=['PUT'])
def update_admin_work(id):
    data = request.json
    db = get_db()
    
    work = db.execute('SELECT * FROM ip_works WHERE id = ?', (id,)).fetchone()
    if not work:
        return jsonify({'code': 404, 'msg': '作品不存在'}), 404
    
    update_fields = []
    update_values = []
    
    for field in ['title', 'student_name', 'image', 'tags', 'cost', 'duration', 'price', 'copyright', 'introduction', 'category', 'status']:
        if field in data:
            if field == 'category' and data[field] not in ['IP版权库', '社区分享']:
                continue
            update_fields.append(f'{field} = ?')
            if field == 'tags':
                update_values.append(json.dumps(data[field]))
            else:
                update_values.append(data[field])
    
    if update_fields:
        update_values.append(id)
        db.execute(f'UPDATE ip_works SET {", ".join(update_fields)} WHERE id = ?', update_values)
        db.commit()
    
    return jsonify({'code': 200, 'msg': '更新成功'})

@app.route('/api/admin/works/<int:id>', methods=['DELETE'])
def delete_admin_work(id):
    db = get_db()
    
    work = db.execute('SELECT * FROM ip_works WHERE id = ?', (id,)).fetchone()
    if not work:
        return jsonify({'code': 404, 'msg': '作品不存在'}), 404
    
    db.execute('DELETE FROM ip_works WHERE id = ?', (id,))
    db.commit()
    
    return jsonify({'code': 200, 'msg': '删除成功'})

@app.route('/api/admin/orders', methods=['GET'])
def get_admin_orders():
    db = get_db()
    orders = db.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    
    orders_list = []
    for order in orders:
        order_dict = dict(order)
        order_dict['contactCount'] = order_dict.get('contact_count', 0)
        if order_dict.get('tags') and order_dict['tags']:
            try:
                order_dict['tags'] = json.loads(order_dict['tags'])
            except:
                order_dict['tags'] = []
        orders_list.append(order_dict)
    
    return jsonify({
        'code': 200,
        'data': {
            'list': orders_list,
            'total': len(orders_list)
        }
    })

@app.route('/api/admin/orders', methods=['POST'])
def create_admin_order():
    try:
        data = request.get_json(force=True)
        
        if not data or 'title' not in data:
            return jsonify({'code': 400, 'msg': '缺少订单标题'}), 400
        
        title = data.get('title')
        image = data.get('image', '')
        qrcode = data.get('qrcode', '')
        price = data.get('price', '')
        deadline = data.get('deadline', '')
        status = data.get('status', 'recruiting')
        tags = data.get('tags', [])
        contact_count = data.get('contactCount', 0)
        
        if isinstance(tags, list):
            tags = json.dumps(tags, ensure_ascii=False)
        
        db = get_db()
        cursor = db.execute('''
            INSERT INTO orders (title, image, qrcode, price, deadline, status, tags, contact_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (title, image, qrcode, price, deadline, status, tags, contact_count))
        db.commit()
        
        return jsonify({
            'code': 200,
            'msg': '订单创建成功',
            'data': {'id': cursor.lastrowid}
        })
    except Exception as e:
        logger.error(f"创建订单失败: {str(e)}")
        return jsonify({'code': 500, 'msg': f'创建订单失败: {str(e)}'}), 500

@app.route('/api/admin/orders/<int:order_id>', methods=['PUT'])
def update_admin_order(order_id):
    try:
        data = request.get_json(force=True)
        db = get_db()
        
        order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
        if not order:
            return jsonify({'code': 404, 'msg': '订单不存在'}), 404
        
        title = data.get('title', order['title'])
        image = data.get('image', order['image'])
        qrcode = data.get('qrcode', order['qrcode'])
        price = data.get('price', order['price'])
        deadline = data.get('deadline', order['deadline'])
        status = data.get('status', order['status'])
        tags = data.get('tags', order['tags'])
        contact_count = data.get('contactCount', order.get('contact_count', 0))
        
        if isinstance(tags, list):
            tags = json.dumps(tags, ensure_ascii=False)
        
        db.execute('''
            UPDATE orders SET 
                title = ?, image = ?, qrcode = ?, price = ?, deadline = ?, 
                status = ?, tags = ?, contact_count = ?
            WHERE id = ?
        ''', (title, image, qrcode, price, deadline, status, tags, contact_count, order_id))
        db.commit()
        
        return jsonify({'code': 200, 'msg': '订单更新成功'})
    except Exception as e:
        logger.error(f"更新订单失败: {str(e)}")
        return jsonify({'code': 500, 'msg': f'更新订单失败: {str(e)}'}), 500

@app.route('/api/admin/orders/<int:order_id>', methods=['DELETE'])
def delete_admin_order(order_id):
    try:
        db = get_db()
        
        order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
        if not order:
            return jsonify({'code': 404, 'msg': '订单不存在'}), 404
        
        db.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        db.commit()
        
        return jsonify({'code': 200, 'msg': '订单删除成功'})
    except Exception as e:
        logger.error(f"删除订单失败: {str(e)}")
        return jsonify({'code': 500, 'msg': f'删除订单失败: {str(e)}'}), 500

@app.route('/api/admin/users', methods=['GET'])
def get_admin_users():
    db = get_db()
    users = db.execute('''
        SELECT u.*, 
               (SELECT COUNT(*) FROM projects WHERE user_id = u.id) as project_count,
               (SELECT COUNT(*) FROM generation_records WHERE user_id = u.id) as record_count
        FROM users u
        ORDER BY u.created_at DESC
    ''').fetchall()
    
    return jsonify({
        'code': 200,
        'data': {
            'list': [dict(user) for user in users],
            'total': len(users)
        }
    })

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    db = get_db()
    
    user_count = db.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    project_count = db.execute('SELECT COUNT(*) as count FROM projects').fetchone()['count']
    code_count = db.execute('SELECT COUNT(*) as count FROM invite_codes').fetchone()['count']
    used_code_count = db.execute('SELECT COUNT(*) as count FROM invite_codes WHERE status = "used"').fetchone()['count']
    
    return jsonify({
        'code': 200,
        'data': {
            'userCount': user_count,
            'projectCount': project_count,
            'codeCount': code_count,
            'usedCodeCount': used_code_count
        }
    })

@app.route('/api/admin/power-logs', methods=['GET'])
def get_admin_power_logs():
    try:
        db = get_db()
        
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        offset = (page - 1) * page_size
        
        user_id = request.args.get('user_id', type=int)
        
        if user_id:
            logs = db.execute('''
                SELECT cpl.*, 
                       u.invite_code,
                       p.title as project_title
                FROM compute_power_logs cpl
                LEFT JOIN users u ON cpl.user_id = u.id
                LEFT JOIN projects p ON cpl.project_id = p.id
                WHERE cpl.user_id = ?
                ORDER BY cpl.created_at DESC
                LIMIT ? OFFSET ?
            ''', (user_id, page_size, offset)).fetchall()
            
            total = db.execute('SELECT COUNT(*) as count FROM compute_power_logs WHERE user_id = ?', (user_id,)).fetchone()['count']
        else:
            logs = db.execute('''
                SELECT cpl.*, 
                       u.invite_code,
                       p.title as project_title
                FROM compute_power_logs cpl
                LEFT JOIN users u ON cpl.user_id = u.id
                LEFT JOIN projects p ON cpl.project_id = p.id
                ORDER BY cpl.created_at DESC
                LIMIT ? OFFSET ?
            ''', (page_size, offset)).fetchall()
            
            total = db.execute('SELECT COUNT(*) as count FROM compute_power_logs').fetchone()['count']
        
        total_power_used = db.execute('SELECT COALESCE(SUM(ABS(power_change)), 0) as total FROM compute_power_logs WHERE power_change < 0').fetchone()['total']
        
        return jsonify({
            'code': 200,
            'data': {
                'list': [dict(log) for log in logs],
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_power_used': total_power_used
            }
        })
    except Exception as e:
        logger.error(f"获取管理后台算力日志失败: {str(e)}")
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>/power', methods=['PUT'])
def update_admin_user_power(user_id):
    try:
        data = request.json
        new_power = data.get('compute_power')
        operation = data.get('operation', 'set')
        description = data.get('description', '')
        
        if new_power is None:
            return jsonify({'code': 400, 'msg': '缺少算力值'}), 400
        
        db = get_db()
        
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if not user:
            return jsonify({'code': 404, 'msg': '用户不存在'}), 404
        
        current_power = user['compute_power']
        
        if operation == 'set':
            power_change = new_power - current_power
            db.execute('UPDATE users SET compute_power = ? WHERE id = ?', (new_power, user_id))
        elif operation == 'add':
            power_change = new_power
            new_power = current_power + new_power
            db.execute('UPDATE users SET compute_power = ? WHERE id = ?', (new_power, user_id))
        elif operation == 'deduct':
            power_change = -abs(new_power)
            new_power = max(0, current_power - abs(new_power))
            db.execute('UPDATE users SET compute_power = ? WHERE id = ?', (new_power, user_id))
        else:
            return jsonify({'code': 400, 'msg': '无效的操作类型'}), 400
        
        db.execute('''
            INSERT INTO compute_power_logs 
            (user_id, operation_type, power_change, power_before, power_after, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, f'admin_{operation}', power_change, current_power, new_power, description or f'管理员操作: {operation}'))
        
        db.commit()
        
        return jsonify({
            'code': 200,
            'msg': '算力更新成功',
            'data': {
                'old_power': current_power,
                'new_power': new_power,
                'power_change': power_change
            }
        })
    except Exception as e:
        logger.error(f"更新用户算力失败: {str(e)}")
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/admin/advertisements', methods=['GET'])
def get_admin_advertisements():
    try:
        status = request.args.get('status', 'published')
        
        db = get_db()
        
        if status == 'all':
            ads = db.execute('''
                SELECT * FROM advertisements 
                ORDER BY sort_order ASC, created_at DESC
            ''').fetchall()
        else:
            ads = db.execute('''
                SELECT * FROM advertisements 
                WHERE status = ?
                ORDER BY sort_order ASC, created_at DESC
            ''', (status,)).fetchall()
        
        ads_list = []
        for ad in ads:
            ad_dict = dict(ad)
            if ad_dict.get('image'):
                ad_dict['image'] = convert_image_url(ad_dict['image'])
            ads_list.append(ad_dict)
        
        return jsonify({
            'code': 200,
            'data': {
                'list': ads_list,
                'total': len(ads_list)
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/admin/advertisements', methods=['POST'])
def create_admin_advertisement():
    try:
        data = request.json
        
        if not data:
            return jsonify({'code': 400, 'msg': '缺少广告数据'}), 400
        
        title = data.get('title', '')
        image = data.get('image', '')
        link_url = data.get('link_url', '')
        status = data.get('status', 'draft')
        sort_order = data.get('sort_order', 0)
        
        db = get_db()
        cursor = db.execute('''
            INSERT INTO advertisements (title, image, link_url, status, sort_order, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (title, image, link_url, status, sort_order, datetime.now(), datetime.now()))
        
        db.commit()
        
        return jsonify({
            'code': 200,
            'msg': '广告位创建成功',
            'data': {'id': cursor.lastrowid}
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/admin/advertisements/<int:ad_id>', methods=['PUT'])
def update_admin_advertisement(ad_id):
    try:
        data = request.json
        
        if not data:
            return jsonify({'code': 400, 'msg': '缺少广告数据'}), 400
        
        db = get_db()
        
        ad = db.execute('SELECT * FROM advertisements WHERE id = ?', (ad_id,)).fetchone()
        if not ad:
            return jsonify({'code': 404, 'msg': '广告位不存在'}), 404
        
        title = data.get('title', ad['title'])
        image = data.get('image', ad['image'])
        link_url = data.get('link_url', ad['link_url'])
        status = data.get('status', ad['status'])
        sort_order = data.get('sort_order', ad['sort_order'])
        
        db.execute('''
            UPDATE advertisements 
            SET title = ?, image = ?, link_url = ?, status = ?, sort_order = ?, updated_at = ?
            WHERE id = ?
        ''', (title, image, link_url, status, sort_order, datetime.now(), ad_id))
        
        db.commit()
        
        return jsonify({
            'code': 200,
            'msg': '广告位更新成功'
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/admin/advertisements/<int:ad_id>', methods=['DELETE'])
def delete_admin_advertisement(ad_id):
    try:
        db = get_db()
        
        ad = db.execute('SELECT * FROM advertisements WHERE id = ?', (ad_id,)).fetchone()
        if not ad:
            return jsonify({'code': 404, 'msg': '广告位不存在'}), 404
        
        db.execute('DELETE FROM advertisements WHERE id = ?', (ad_id,))
        db.commit()
        
        return jsonify({
            'code': 200,
            'msg': '广告位删除成功'
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/admin/advertisements/<int:ad_id>/publish', methods=['POST'])
def publish_admin_advertisement(ad_id):
    try:
        db = get_db()
        
        ad = db.execute('SELECT * FROM advertisements WHERE id = ?', (ad_id,)).fetchone()
        if not ad:
            return jsonify({'code': 404, 'msg': '广告位不存在'}), 404
        
        db.execute('''
            UPDATE advertisements 
            SET status = 'published', updated_at = ?
            WHERE id = ?
        ''', (datetime.now(), ad_id))
        
        db.commit()
        
        return jsonify({
            'code': 200,
            'msg': '广告位发布成功'
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/admin/advertisements/<int:ad_id>/unpublish', methods=['POST'])
def unpublish_admin_advertisement(ad_id):
    try:
        db = get_db()
        
        ad = db.execute('SELECT * FROM advertisements WHERE id = ?', (ad_id,)).fetchone()
        if not ad:
            return jsonify({'code': 404, 'msg': '广告位不存在'}), 404
        
        db.execute('''
            UPDATE advertisements 
            SET status = 'unpublished', updated_at = ?
            WHERE id = ?
        ''', (datetime.now(), ad_id))
        
        db.commit()
        
        return jsonify({
            'code': 200,
            'msg': '广告位下架成功'
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/api/chat/sessions', methods=['GET'])
def get_chat_sessions():
    invite_code = request.args.get('invite_code')
    project_id = request.args.get('project_id', type=int)
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'success', 'sessions': [], 'total': 0})
    
    db = get_db()
    query = 'SELECT * FROM chat_sessions WHERE user_id = ?'
    params = [user_id]
    
    if project_id:
        query += ' AND project_id = ?'
        params.append(project_id)
    
    query += ' ORDER BY update_time DESC'
    
    sessions = db.execute(query, params).fetchall()
    
    return jsonify({
        'status': 'success',
        'sessions': [dict(s) for s in sessions],
        'total': len(sessions)
    })

@app.route('/api/chat/sessions', methods=['POST'])
def create_chat_session():
    data = request.json
    invite_code = data.get('invite_code')
    project_id = data.get('project_id')
    title = data.get('title', '新对话')
    selected_people = data.get('selected_people', 'script')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_or_create_user(invite_code)
    
    db = get_db()
    cursor = db.execute('''
        INSERT INTO chat_sessions (project_id, user_id, title, selected_people)
        VALUES (%s, %s, %s, %s, %s)
    ''', (project_id, user_id, title, selected_people))
    db.commit()
    
    return jsonify({
        'status': 'success',
        'session_id': cursor.lastrowid
    })

@app.route('/api/chat/sessions/<int:session_id>', methods=['PUT'])
def update_chat_session(session_id):
    data = request.json
    invite_code = data.get('invite_code')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 401
    
    db = get_db()
    session = db.execute('SELECT * FROM chat_sessions WHERE id = ? AND user_id = ?', 
                       (session_id, user_id)).fetchone()
    
    if not session:
        return jsonify({'status': 'error', 'message': '会话不存在或无权访问'}), 404
    
    updates = []
    values = []
    
    if 'title' in data:
        updates.append('title = ?')
        values.append(data['title'])
    if 'selected_people' in data:
        updates.append('selected_people = ?')
        values.append(data['selected_people'])
    if 'conversation_id' in data:
        updates.append('conversation_id = ?')
        values.append(data['conversation_id'])
    if 'message_count' in data:
        updates.append('message_count = ?')
        values.append(data['message_count'])
    
    if updates:
        updates.append('update_time = ?')
        values.append(datetime.now())
        values.append(session_id)
        
        db.execute(f'UPDATE chat_sessions SET {", ".join(updates)} WHERE id = ?', values)
        db.commit()
    
    return jsonify({'status': 'success', 'message': '会话更新成功'})

@app.route('/api/chat/sessions/<int:session_id>', methods=['DELETE'])
def delete_chat_session(session_id):
    invite_code = request.args.get('invite_code')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 401
    
    db = get_db()
    session = db.execute('SELECT * FROM chat_sessions WHERE id = ? AND user_id = ?', 
                       (session_id, user_id)).fetchone()
    
    if not session:
        return jsonify({'status': 'error', 'message': '会话不存在或无权访问'}), 404
    
    db.execute('DELETE FROM chat_sessions WHERE id = ?', (session_id,))
    db.commit()
    
    return jsonify({'status': 'success', 'message': '会话已删除'})

@app.route('/api/chat/sessions/<int:session_id>/messages', methods=['GET'])
def get_session_messages(session_id):
    invite_code = request.args.get('invite_code')
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 401
    
    db = get_db()
    session = db.execute('SELECT * FROM chat_sessions WHERE id = ? AND user_id = ?', 
                       (session_id, user_id)).fetchone()
    
    if not session:
        return jsonify({'status': 'error', 'message': '会话不存在或无权访问'}), 404
    
    messages = db.execute('''
        SELECT * FROM chat_messages 
        WHERE user_id = ? AND chat_id = ?
        ORDER BY create_time ASC
    ''', (user_id, session['conversation_id'] if session['conversation_id'] else '')).fetchall()
    
    return jsonify({
        'status': 'success',
        'messages': [dict(m) for m in messages],
        'session': dict(session)
    })

if __name__ == '__main__':
    if key_manager.get_key_count() == 0:
        print("WARNING: 未找到有效的火山引擎密钥配置！请检查 .env 文件中的 VOLC_AK_1 和 VOLC_SK_1")
    else:
        print(f"✓ 密钥管理器初始化完成，共 {key_manager.get_key_count()} 组密钥")

    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
