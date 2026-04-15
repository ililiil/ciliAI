import requests
import json

url = 'http://localhost:5001/api/orders'

# 测试创建订单
test_order = {
    'title': '测试商单',
    'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
    'qrcode': 'https://example.com/qrcode.png',
    'price': '¥100',
    'deadline': '2026-04-30',
    'status': 'recruiting',
    'tags': ['都市', '爱情'],
    'description': '测试描述',
    'contact_info': '测试联系方式',
    'min_profit': 100,
    'share_ratio': 50,
    'power_subsidy': 10,
    'period': 30
}

print("测试创建订单API...")
print(f"URL: {url}")
print(f"Data: {json.dumps(test_order, ensure_ascii=False, indent=2)}")

try:
    response = requests.post(url, json=test_order, timeout=10)
    print(f"\n响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            print(f"✅ 订单创建成功! order_id: {result.get('order_id')}")
        else:
            print(f"❌ 订单创建失败: {result.get('message')}")
    else:
        print(f"❌ HTTP请求失败: {response.status_code}")
        print(f"响应内容: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"\n❌ 请求异常: {e}")
    import traceback
    traceback.print_exc()
