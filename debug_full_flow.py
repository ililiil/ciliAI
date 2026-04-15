import requests
import json
import sqlite3
from datetime import datetime

DATABASE = 'ciliai.db'

def check_database():
    print("=" * 60)
    print("检查数据库状态")
    print("=" * 60)

    conn = sqlite3.connect(DATABASE)
    conn.execute('PRAGMA foreign_keys = ON')

    cursor = conn.cursor()

    # 检查users表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone():
        print("✅ users 表存在")
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"   用户数量: {count}")

        if count > 0:
            cursor.execute("SELECT * FROM users LIMIT 1")
            user = cursor.fetchone()
            print(f"   示例用户: {user}")
    else:
        print("❌ users 表不存在")

    # 检查projects表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
    if cursor.fetchone():
        print("✅ projects 表存在")
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        print(f"   项目数量: {count}")

        if count > 0:
            cursor.execute("SELECT * FROM projects LIMIT 1")
            project = cursor.fetchone()
            print(f"   示例项目: {project}")
    else:
        print("❌ projects 表不存在")

    conn.close()

def test_create_user():
    print("\n" + "=" * 60)
    print("测试创建用户")
    print("=" * 60)

    url = 'http://localhost:5001/api/user/register'
    test_data = {
        'invite_code': f'test_user_{datetime.now().strftime("%Y%m%d%H%M%S")}',
        'compute_power': 100
    }

    print(f"发送数据: {json.dumps(test_data, ensure_ascii=False)}")

    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"\n响应状态码: {response.status_code}")
        result = response.json()
        print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get('status') == 'success':
            print("✅ 用户创建成功")
            return result.get('data', {}).get('invite_code')
        else:
            print(f"❌ 用户创建失败: {result.get('message')}")
            return None
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def test_create_project(invite_code):
    print("\n" + "=" * 60)
    print("测试创建项目")
    print("=" * 60)

    url = 'http://localhost:5001/api/projects'
    test_data = {
        'invite_code': invite_code,
        'title': f'测试项目_{datetime.now().strftime("%Y%m%d%H%M%S")}',
        'description': '测试描述',
        'cover_image': ''
    }

    print(f"发送数据: {json.dumps(test_data, ensure_ascii=False)}")

    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"\n响应状态码: {response.status_code}")
        result = response.json()
        print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get('status') == 'success':
            print("✅ 项目创建成功")
            return True
        else:
            print(f"❌ 项目创建失败: {result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_get_projects(invite_code):
    print("\n" + "=" * 60)
    print("测试获取项目列表")
    print("=" * 60)

    url = f'http://localhost:5001/api/projects?invite_code={invite_code}'
    print(f"请求URL: {url}")

    try:
        response = requests.get(url, timeout=10)
        print(f"\n响应状态码: {response.status_code}")
        result = response.json()
        print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get('status') == 'success':
            print(f"✅ 获取成功，项目数量: {len(result.get('projects', []))}")
            return True
        else:
            print(f"❌ 获取失败: {result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return False

# 执行测试
check_database()
invite_code = test_create_user()
if invite_code:
    test_create_project(invite_code)
    test_get_projects(invite_code)
else:
    print("\n❌ 无法继续测试，因为用户创建失败")
