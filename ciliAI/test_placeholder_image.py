import requests

print("测试占位图...")
response = requests.get('http://localhost:5001/placeholder.png', timeout=5)

print(f"状态码: {response.status_code}")
print(f"内容类型: {response.headers.get('Content-Type')}")
print(f"内容长度: {len(response.content)} bytes")

if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
    print("\n✅ 占位图服务正常!")
else:
    print("\n❌ 占位图服务有问题")
