import os
import json
import sqlite3
import random
import string
from datetime import datetime
from flask import Flask, request, jsonify, g, send_from_directory, current_app
from flask_cors import CORS
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

app = Flask(__name__, static_folder='templates', static_url_path='')
CORS(app)

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ciliAI', 'fangtang.db')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_invite_code(length=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('api/'):
        return jsonify({'code': 404, 'msg': 'API not found'}), 404
    return send_from_directory('templates', 'index.html')

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
def upload_image():
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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/admin/invite-codes', methods=['GET'])
def get_invite_codes():
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
def create_invite_code():
    data = request.json
    code = data.get('code')
    compute_power = data.get('compute_power', 1000)
    
    if not code:
        code = generate_invite_code(8)
    
    if len(code) != 8:
        return jsonify({'code': 400, 'msg': '邀请码必须为8位字符'}), 400
    
    db = get_db()
    try:
        db.execute('INSERT INTO invite_codes (code, compute_power) VALUES (?, ?)', 
                   (code.upper(), compute_power))
        db.commit()
        return jsonify({'code': 200, 'msg': '创建成功', 'data': {'code': code.upper()}})
    except sqlite3.IntegrityError:
        return jsonify({'code': 400, 'msg': '邀请码已存在'}), 400

@app.route('/api/admin/invite-codes/<int:id>', methods=['PUT'])
def update_invite_code(id):
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
def delete_invite_code(id):
    db = get_db()
    
    code = db.execute('SELECT * FROM invite_codes WHERE id = ?', (id,)).fetchone()
    if not code:
        return jsonify({'code': 404, 'msg': '邀请码不存在'}), 404
    
    db.execute('DELETE FROM invite_codes WHERE id = ?', (id,))
    db.commit()
    
    return jsonify({'code': 200, 'msg': '删除成功'})

@app.route('/api/admin/invite-codes/batch', methods=['POST'])
def batch_create_invite_codes():
    data = request.json
    count = data.get('count', 10)
    compute_power = data.get('compute_power', 1000)
    
    if count > 100:
        return jsonify({'code': 400, 'msg': '单次最多创建100个邀请码'}), 400
    
    db = get_db()
    created_codes = []
    attempts = 0
    max_attempts = count * 3
    
    while len(created_codes) < count and attempts < max_attempts:
        code = generate_invite_code(8)
        try:
            db.execute('INSERT INTO invite_codes (code, compute_power) VALUES (?, ?)',
                       (code, compute_power))
            created_codes.append(code)
        except sqlite3.IntegrityError:
            pass
        attempts += 1
    
    db.commit()
    
    return jsonify({
        'code': 200,
        'msg': f'成功创建 {len(created_codes)} 个8位邀请码',
        'data': {'codes': created_codes}
    })

@app.route('/api/works', methods=['GET'])
def get_public_works():
    db = get_db()
    works = db.execute('''
        SELECT * FROM ip_works
        WHERE status = 'active'
        ORDER BY created_at DESC
    ''').fetchall()
    
    return jsonify({
        'code': 200,
        'data': {
            'list': [dict(work) for work in works],
            'total': len(works)
        }
    })

@app.route('/api/admin/works', methods=['GET'])
def get_works():
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
def create_work():
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
    
    if not title or not image:
        return jsonify({'code': 400, 'msg': '标题和图片不能为空'}), 400
    
    if category not in ['IP版权库', '社区分享']:
        category = 'IP版权库'
    
    db = get_db()
    cursor = db.execute('''
        INSERT INTO ip_works (title, student_name, image, tags, cost, duration, price, copyright, introduction, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, student_name, image, json.dumps(tags), cost, duration, price, copyright, introduction, category))
    db.commit()
    
    return jsonify({
        'code': 200,
        'msg': '创建成功',
        'data': {'id': cursor.lastrowid}
    })

@app.route('/api/admin/works/<int:id>', methods=['PUT'])
def update_work(id):
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
def delete_work(id):
    db = get_db()
    
    work = db.execute('SELECT * FROM ip_works WHERE id = ?', (id,)).fetchone()
    if not work:
        return jsonify({'code': 404, 'msg': '作品不存在'}), 404
    
    db.execute('DELETE FROM ip_works WHERE id = ?', (id,))
    db.commit()
    
    return jsonify({'code': 200, 'msg': '删除成功'})

@app.route('/api/admin/users', methods=['GET'])
def get_users():
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
def get_stats():
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

def init_db():
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
            category TEXT DEFAULT 'IP版权库',
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    try:
        cursor.execute('ALTER TABLE ip_works ADD COLUMN category TEXT DEFAULT "IP版权库"')
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)
