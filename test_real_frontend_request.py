import requests
import json

print("=" * 80)
print("模拟前端真实请求测试")
print("=" * 80)

# 模拟前端发送的完整订单数据
# 基于 Order.vue 中的 handleSubmit 函数
test_order_data = {
    'invite_code': 'CILIAI88',  # 使用测试邀请码
    'title': '测试商单_前端模拟',
    'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
    'qrcode': 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=weixin://wxid_test',
    'price': '¥100',
    'deadline': '2026-04-30',
    'status': 'recruiting',
    'tags': ['都市'],
    'description': '测试描述',
    'contact_info': '测试联系方式',
    'min_profit': 100,
    'share_ratio': 50,
    'power_subsidy': 10,
    'period': 30
}

print("\n发送的完整数据:")
print(json.dumps(test_order_data, ensure_ascii=False, indent=2))

print("\n正在测试创建订单...")
response = requests.post(
    'http://localhost:5001/api/orders',
    json=test_order_data,
    headers={'Content-Type': 'application/json'},
    timeout=10
)

print(f"\n响应状态码: {response.status_code}")
print(f"响应头: {dict(response.headers)}")

try:
    result = response.json()
    print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

    if result.get('status') == 'success':
        print("\n✅ 订单创建成功!")
        print(f"   订单ID: {result.get('order_id')}")
    else:
        print(f"\n❌ 订单创建失败!")
        print(f"   错误信息: {result.get('message')}")

except json.JSONDecodeError:
    print(f"\n❌ 响应不是有效的JSON格式")
    print(f"原始响应: {response.text}")

print("\n" + "=" * 80)

# 测试2: 测试没有invite_code的情况
print("\n测试2: 没有invite_code的情况")
print("=" * 80)

test_order_no_user = {
    'title': '测试订单_无用户',
    'image': 'https://example.com/image.jpg',
    'price': '¥100',
    'status': 'recruiting'
}

print("\n发送的数据(无invite_code):")
print(json.dumps(test_order_no_user, ensure_ascii=False, indent=2))

response2 = requests.post(
    'http://localhost:5001/api/orders',
    json=test_order_no_user,
    headers={'Content-Type': 'application/json'},
    timeout=10
)

print(f"\n响应状态码: {response2.status_code}")

try:
    result2 = response2.json()
    print(f"响应内容: {json.dumps(result2, ensure_ascii=False, indent=2)}")

    if result2.get('status') == 'success':
        print("\n✅ 订单创建成功(无用户关联)!")
        print(f"   订单ID: {result2.get('order_id')}")
    else:
        print(f"\n❌ 订单创建失败!")
        print(f"   错误信息: {result2.get('message')}")

except Exception as e:
    print(f"\n❌ 发生错误: {e}")

print("\n" + "=" * 80)
