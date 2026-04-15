import requests
import json

print("=" * 80)
print("测试作品创建API")
print("=" * 80)

url = 'http://localhost:5001/api/admin/works'

# 测试数据
test_data = {
    'title': '测试作品',
    'student_name': '测试学员',
    'image': 'https://example.com/test.jpg',
    'tags': ['测试'],
    'cost': '1000算力/分钟',
    'duration': '420分钟',
    'price': '150-300元/分钟',
    'copyright': '归CiliAI所有',
    'introduction': '这是一个测试作品',
    'category': 'IP版权库'
}

print(f"\n发送数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")

try:
    response = requests.post(url, json=test_data, timeout=10)
    print(f"\n响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 200:
            print(f"\n✅ 作品创建成功! ID: {result.get('data', {}).get('id')}")
        else:
            print(f"\n❌ 作品创建失败: {result.get('msg')}")
    else:
        print(f"\n❌ HTTP请求失败: {response.status_code}")
        print(f"响应内容: {response.text}")

except Exception as e:
    print(f"\n❌ 请求异常: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)
