import requests
import json

url = 'http://localhost:5001/api/projects'

# 测试数据
test_data = {
    'invite_code': 'test_invite_code',
    'title': '测试项目',
    'description': '测试描述'
}

print("测试创建项目API...")
print(f"URL: {url}")
print(f"Data: {json.dumps(test_data, ensure_ascii=False, indent=2)}")

try:
    response = requests.post(url, json=test_data, timeout=10)
    print(f"\n响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
except requests.exceptions.RequestException as e:
    print(f"\n请求失败: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"响应状态码: {e.response.status_code}")
        print(f"响应内容: {json.dumps(e.response.json(), ensure_ascii=False, indent=2)}")
