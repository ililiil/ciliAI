import requests
import json

# 测试 projects API
def test_projects_api():
    print("\n" + "=" * 60)
    print("测试 projects API")
    print("=" * 60)

    url = 'http://localhost:5001/api/projects'
    test_data = {
        'invite_code': 'CILIAI88',
        'title': '测试项目',
        'description': '测试描述'
    }

    print(f"发送数据: {json.dumps(test_data, ensure_ascii=False)}")

    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                print(f"✅ 项目创建成功! project_id: {result.get('project_id')}")
                return True
            else:
                print(f"❌ 项目创建失败: {result.get('message')}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

# 测试 GET projects
def test_get_projects():
    print("\n" + "=" * 60)
    print("测试 GET /api/projects")
    print("=" * 60)

    url = 'http://localhost:5001/api/projects?invite_code=CILIAI88'
    print(f"请求URL: {url}")

    try:
        response = requests.get(url, timeout=10)
        print(f"\n响应状态码: {response.status_code}")
        result = response.json()
        print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get('status') == 'success':
            print(f"✅ 获取项目列表成功! 项目数量: {len(result.get('projects', []))}")
            return True
        else:
            print(f"❌ 获取项目列表失败: {result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

# 测试 orders API
def test_orders_api():
    print("\n" + "=" * 60)
    print("测试 orders API")
    print("=" * 60)

    url = 'http://localhost:5001/api/orders'
    test_data = {
        'invite_code': 'CILIAI88',
        'title': '测试订单-API测试',
        'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
        'price': '¥100',
        'status': 'recruiting'
    }

    print(f"发送数据: {json.dumps(test_data, ensure_ascii=False)}")

    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                print(f"✅ 订单创建成功! order_id: {result.get('order_id')}")
                return True
            else:
                print(f"❌ 订单创建失败: {result.get('message')}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

# 执行所有测试
print("=" * 60)
print("全面测试所有主要API")
print("=" * 60)

test_projects_api()
test_get_projects()
test_orders_api()

print("\n" + "=" * 60)
print("所有测试完成")
print("=" * 60)
