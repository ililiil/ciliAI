import requests
import socket
import json
from datetime import datetime

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

def check_backend():
    """检查后端服务"""
    print("=" * 80)
    print("1. 检查后端服务 (Flask)")
    print("=" * 80)

    if check_port(5001):
        print("✅ 后端服务端口 5001 正在监听")

        try:
            # 测试API端点
            response = requests.get('http://localhost:5001/api/orders', timeout=5)
            print(f"✅ API响应正常 (状态码: {response.status_code})")

            try:
                result = response.json()
                print(f"✅ JSON响应解析成功")
                print(f"   响应内容: {json.dumps(result, ensure_ascii=False)[:200]}")
                return True
            except:
                print(f"❌ JSON响应解析失败")
                print(f"   原始响应: {response.text[:200]}")
                return False
        except Exception as e:
            print(f"❌ 无法连接到后端API: {e}")
            return False
    else:
        print("❌ 后端服务端口 5001 未监听")
        print("   提示: 请运行 'python app.py' 启动后端服务")
        return False

def check_frontend():
    """检查前端服务"""
    print("\n" + "=" * 80)
    print("2. 检查前端服务 (Vite)")
    print("=" * 80)

    # 检查所有可能的端口
    frontend_ports = [3002, 3003, 3004, 3005, 5173]
    found_ports = []

    for port in frontend_ports:
        if check_port(port):
            found_ports.append(port)
            try:
                response = requests.get(f'http://localhost:{port}', timeout=3, allow_redirects=False)
                if response.status_code in [200, 304]:
                    print(f"✅ 前端服务在端口 {port} 运行中 (状态码: {response.status_code})")
                else:
                    print(f"⚠️  端口 {port} 被占用但不是前端服务 (状态码: {response.status_code})")
            except Exception as e:
                print(f"⚠️  端口 {port} 被占用但无法连接")
        else:
            print(f"❌ 端口 {port} 未监听")

    if found_ports:
        print(f"\n✅ 前端服务运行中!")
        print(f"   请访问: http://localhost:{found_ports[0]}")
        return True
    else:
        print("\n❌ 前端服务未运行")
        print("   提示: 请运行 'npm run dev' 启动前端服务")
        return False

def test_api_integration():
    """测试API集成"""
    print("\n" + "=" * 80)
    print("3. 测试API集成")
    print("=" * 80)

    # 测试订单创建
    test_order = {
        'invite_code': 'CILIAI88',
        'title': f'系统检查测试_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'image': 'https://example.com/test.jpg',
        'price': '¥100',
        'status': 'recruiting',
        'description': '系统检查测试订单'
    }

    print("\n发送测试订单...")
    print(f"数据: {json.dumps(test_order, ensure_ascii=False, indent=2)}")

    try:
        response = requests.post(
            'http://localhost:5001/api/orders',
            json=test_order,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        print(f"\n响应状态码: {response.status_code}")

        try:
            result = response.json()
            print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

            if result.get('status') == 'success':
                print(f"\n✅ API集成测试成功!")
                print(f"   订单ID: {result.get('order_id')}")
                return True
            else:
                print(f"\n❌ API测试失败!")
                print(f"   错误信息: {result.get('message')}")
                return False
        except:
            print(f"❌ JSON解析失败")
            print(f"   原始响应: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def check_database():
    """检查数据库"""
    print("\n" + "=" * 80)
    print("4. 检查数据库")
    print("=" * 80)

    import sqlite3

    DATABASE = 'fangtang.db'

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 检查orders表
        cursor.execute("PRAGMA table_info(orders)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        print(f"✅ 数据库连接成功")
        print(f"   数据库文件: {DATABASE}")

        # 检查必需列
        required_columns = [
            'deadline', 'tags', 'script', 'description',
            'contact_info', 'min_profit', 'share_ratio',
            'power_subsidy', 'period'
        ]

        missing_columns = [col for col in required_columns if col not in column_names]

        if missing_columns:
            print(f"\n❌ orders表缺少列: {', '.join(missing_columns)}")
            print("   提示: 运行 'python fix_database_full.py' 修复")
            return False
        else:
            print(f"✅ orders表结构完整")
            print(f"   总列数: {len(column_names)}")

        # 检查user_id约束
        user_id_col = [col for col in columns if col[1] == 'user_id'][0]
        if user_id_col[3] == 1:  # NOT NULL
            print(f"\n⚠️  user_id列有NOT NULL约束")
            print("   提示: 运行 'python make_user_id_nullable.py' 修复")
            return False
        else:
            print(f"✅ user_id列允许NULL值")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False

def main():
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "CiliAI 系统完整诊断检查" + " " * 20 + "  ║")
    print("╚" + "=" * 78 + "╝")
    print()

    results = {
        'backend': check_backend(),
        'frontend': check_frontend(),
        'database': check_database(),
        'api': None
    }

    # API测试依赖后端
    if results['backend']:
        results['api'] = test_api_integration()
    else:
        print("\n" + "=" * 80)
        print("⚠️  跳过API测试 (后端服务未运行)")
        print("=" * 80)

    # 总结
    print("\n" + "=" * 80)
    print("诊断总结")
    print("=" * 80)

    for check_name, status in results.items():
        if status is None:
            continue
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"{check_name.upper():20} {status_text}")

    all_passed = all(status for status in results.values() if status is not None)

    if all_passed:
        print("\n🎉 所有检查通过!")
        print("   系统运行正常，可以进行订单创建操作")
        print("\n下一步:")
        print("1. 打开浏览器访问: http://localhost:3003 (或当前运行的端口)")
        print("2. 登录系统")
        print("3. 进入接单广场")
        print("4. 点击发布商单")
        print("5. 填写表单并提交")
        print("6. 应该能看到成功提示")
    else:
        print("\n⚠️  有检查未通过!")
        print("   请根据上述提示修复问题")
        print("\n如果所有检查都显示正常但问题依然存在:")
        print("1. 清除浏览器缓存")
        print("2. 使用无痕/隐私模式打开浏览器")
        print("3. 重试订单创建操作")

    print("=" * 80)

if __name__ == '__main__':
    main()
