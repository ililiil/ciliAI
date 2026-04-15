import socket
import requests

def check_port(port):
    """检查端口是否被占用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

print("=" * 80)
print("CiliAI 系统状态检查")
print("=" * 80)

print("\n🔍 检查后端服务 (Flask)...")
if check_port(5001):
    print("✅ 后端服务运行中 (http://localhost:5001)")
    try:
        response = requests.get('http://localhost:5001/api/orders', timeout=3)
        print(f"   API响应: ✅ 正常")
    except:
        print(f"   API响应: ❌ 失败")
else:
    print("❌ 后端服务未运行 (http://localhost:5001)")

print("\n🔍 检查前端服务 (Vite)...")
frontend_ports = [3002, 3003, 3004, 3005]
found_port = None

for port in frontend_ports:
    if check_port(port):
        try:
            response = requests.get(f'http://localhost:{port}', timeout=3)
            if response.status_code == 200:
                print(f"✅ 前端服务运行中: http://localhost:{port}")
                found_port = port
                break
        except:
            pass

if not found_port:
    print("❌ 前端服务未运行")

print("\n" + "=" * 80)
print("📌 正确的访问地址")
print("=" * 80)

if check_port(5001):
    print(f"\n  🌐 后端API:  http://localhost:5001")

if found_port:
    print(f"\n  🌐 前端页面: http://localhost:{found_port}")
    print(f"\n  ⚠️  注意: 请使用上面的URL访问前端页面")
else:
    print("\n  ❌ 前端服务未运行")

print("\n" + "=" * 80)

if check_port(5001) and found_port:
    print("\n✅ 系统完全正常！")
    print(f"\n请在浏览器中访问: http://localhost:{found_port}")
else:
    print("\n⚠️  有服务未运行，请启动缺失的服务")

print("=" * 80)
