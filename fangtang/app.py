import os
import time
import json
import logging
import sqlite3
import hashlib
import uuid
from datetime import datetime
import requests as req_lib
from flask import Flask, request, jsonify, send_from_directory, g, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
from volcengine.visual.VisualService import VisualService

load_dotenv()

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE = 'fangtang.db'

POWER_COST = {
    'generate': 10,
    'extend': 5,
    'super_resolution': 8,
    'inpaint': 6,
    'chat': 1
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, check_same_thread=False)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
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
            status TEXT DEFAULT 'active',
            image_count INTEGER DEFAULT 0,
            chat_count INTEGER DEFAULT 0,
            total_power_used INTEGER DEFAULT 0,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generation_records (
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
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
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
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compute_power_logs (
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
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL,
            FOREIGN KEY (record_id) REFERENCES generation_records (id) ON DELETE SET NULL
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
            category TEXT DEFAULT 'IP版权库',
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
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
    
    default_codes = ["111111", "222222", "333333", "444444", "555555", 
                     "666666", "777777", "888888", "999999", "000000"]
    for code in default_codes:
        try:
            cursor.execute('INSERT OR IGNORE INTO invite_codes (code, compute_power) VALUES (?, ?)', 
                          (code, 1000))
        except:
            pass
    
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
    cursor = db.execute('INSERT INTO users (invite_code, compute_power) VALUES (?, ?)', 
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, operation_type, amount, current_power, new_power, description))
    
    db.commit()
    return new_power

VOLC_AK = os.getenv('VOLC_AK')
VOLC_SK = os.getenv('VOLC_SK')

visual_service = VisualService()
visual_service.set_ak(VOLC_AK)
visual_service.set_sk(VOLC_SK)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/dify-api/chat-messages', methods=['POST'])
def dify_proxy():
    try:
        dify_url = 'https://whhongyi.com.cn/v1/chat-messages'
        headers = {
            'Authorization': request.headers.get('Authorization', ''),
            'Content-Type': 'application/json'
        }
        body = request.get_json()
        logger.info(f"Dify proxy request: query={body.get('query', '')[:50] if body else 'N/A'}")
        
        resp = req_lib.post(dify_url, json=body, headers=headers, stream=True, timeout=60)
        logger.info(f"Dify upstream status: {resp.status_code}")
        
        if resp.status_code != 200:
            error_text = resp.text[:500]
            logger.error(f"Dify upstream error: {error_text}")
            return jsonify({'status': 'error', 'message': f'Dify API error: {resp.status_code}'}), resp.status_code
        
        def generate():
            try:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk
            except Exception as e:
                logger.error(f"Stream error: {str(e)}")
                yield f"data: {{'event': 'error', 'message': '{str(e)}'}}\n\n"
        
        return Response(
            stream_with_context(generate()),
            content_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
    except Exception as e:
        logger.error(f"Dify proxy error: {str(e)}")
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
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '缺少邀请码参数'}), 400
    if not title or not title.strip():
        return jsonify({'status': 'error', 'message': '项目标题不能为空'}), 400
    
    user_id = get_or_create_user(invite_code)
    
    db = get_db()
    cursor = db.execute('''
        INSERT INTO projects (user_id, title, description)
        VALUES (?, ?, ?)
    ''', (user_id, title.strip(), description))
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
    
    if not prompt:
        return jsonify({'status': 'error', 'message': '请输入提示词'}), 400
    
    if not invite_code:
        return jsonify({'status': 'error', 'message': '请先登录'}), 401
    
    user_id = get_user_id_by_invite_code(invite_code)
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户不存在，请重新登录'}), 401
    
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
        "req_key": "jimeng_t2i_v40",
        "prompt": prompt,
        "width": data.get('width', 1024),
        "height": data.get('height', 1024),
        "model_version": "v4.0"
    }
    
    try:
        logger.info(f"Submitting task for prompt: {prompt}")
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
                "req_key": "jimeng_t2i_v40",
                "task_id": task_id
            }
            query_res = visual_service.common_json_handler("CVSync2AsyncGetResult", query_params)
            
            resp_code = query_res.get('code')
            if resp_code == 10000:
                data_res = query_res.get('data', {})
                status = data_res.get('status')
                
                if status == 'done':
                    image_urls = data_res.get('binary_data_base64', [])
                    if not image_urls:
                        image_urls = data_res.get('image_urls', [])
                    
                    db = get_db()
                    cursor = db.execute('''
                        INSERT INTO generation_records 
                        (project_id, user_id, type, prompt, image_url, image_width, image_height, model_version, params, task_id, power_cost)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

    params = {
        "req_key": "jimeng_i2i_v30",
        "binary_data_base64": [image_base64],
        "prompt": prompt or "修改图片指定区域",
        "mask": mask_base64
    }

    try:
        logger.info(f"Submitting inpaint task")
        submit_res = visual_service.common_json_handler("CVSync2AsyncSubmitTask", params)
        
        if submit_res.get('code') != 10000:
            add_compute_power(user_id, power_cost, 'refund', '改图失败退还')
            return jsonify({'status': 'error', 'message': f"提交任务失败: {submit_res.get('message')}"}), 500
        
        task_id = submit_res.get('data', {}).get('task_id')
        if not task_id:
            add_compute_power(user_id, power_cost, 'refund', '改图失败退还')
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
                    image_urls = data_res.get('binary_data_base64', [])
                    if not image_urls:
                        image_urls = data_res.get('image_urls', [])
                    
                    db = get_db()
                    cursor = db.execute('''
                        INSERT INTO generation_records 
                        (project_id, user_id, type, prompt, image_url, params, task_id, power_cost)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
        logger.error(f"Error: {str(e)}")
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
                    image_urls = data_res.get('binary_data_base64', [])
                    if not image_urls:
                        image_urls = data_res.get('image_urls', [])
                    
                    db = get_db()
                    cursor = db.execute('''
                        INSERT INTO generation_records 
                        (project_id, user_id, type, prompt, image_url, image_width, image_height, params, task_id, power_cost)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    image_urls = data_res.get('binary_data_base64', [])
                    if not image_urls:
                        image_urls = data_res.get('image_urls', [])
                    
                    db = get_db()
                    cursor = db.execute('''
                        INSERT INTO generation_records 
                        (project_id, user_id, type, image_url, params, task_id, power_cost)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
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
    
    return jsonify({
        'status': 'success',
        'records': [dict(r) for r in records],
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
    
    return jsonify({
        'status': 'success',
        'record': dict(record)
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
        VALUES (?, ?, ?, ?, ?, ?)
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
        
        result = {
            'code': 200,
            'data': {
                'list': [dict(work) for work in works],
                'total': len(works)
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

if __name__ == '__main__':
    if not VOLC_AK or not VOLC_SK:
        print("WARNING: VOLC_AK or VOLC_SK not found in environment variables!")
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
