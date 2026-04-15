import requests
import json
import time

def test_end_to_end():
    print("=" * 80)
    print(" CiliAI 后台管理 - 端到端功能测试")
    print("=" * 80)

    results = []

    # 测试1: 创建项目
    print("\n📝 测试 1: 创建项目")
    print("-" * 80)
    try:
        response = requests.post('http://localhost:5001/api/projects', json={
            'invite_code': 'CILIAI88',
            'title': f'E2E测试项目_{int(time.time())}',
            'description': '端到端测试描述'
        }, timeout=10)
        result = response.json()
        if result.get('status') == 'success':
            project_id = result.get('project_id')
            print(f"✅ 项目创建成功 (ID: {project_id})")
            results.append(("创建项目", True))

            # 测试2: 获取项目列表
            print(f"\n📋 测试 2: 获取项目列表")
            print("-" * 80)
            response = requests.get(f'http://localhost:5001/api/projects?invite_code=CILIAI88', timeout=10)
            result = response.json()
            if result.get('status') == 'success':
                projects = result.get('projects', [])
                print(f"✅ 获取项目列表成功 (共 {len(projects)} 个项目)")
                results.append(("获取项目列表", True))
            else:
                print(f"❌ 获取项目列表失败: {result.get('message')}")
                results.append(("获取项目列表", False))
        else:
            print(f"❌ 项目创建失败: {result.get('message')}")
            results.append(("创建项目", False))
            return
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        results.append(("创建项目", False))
        return

    # 测试3: 创建订单
    print(f"\n📦 测试 3: 创建订单")
    print("-" * 80)
    try:
        response = requests.post('http://localhost:5001/api/orders', json={
            'invite_code': 'CILIAI88',
            'title': f'E2E测试订单_{int(time.time())}',
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
            'price': '¥100',
            'status': 'recruiting',
            'description': '端到端测试订单'
        }, timeout=10)
        result = response.json()
        if result.get('status') == 'success':
            order_id = result.get('order_id')
            print(f"✅ 订单创建成功 (ID: {order_id})")
            results.append(("创建订单", True))
        else:
            print(f"❌ 订单创建失败: {result.get('message')}")
            results.append(("创建订单", False))
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        results.append(("创建订单", False))

    # 测试4: 获取订单列表
    print(f"\n📋 测试 4: 获取订单列表")
    print("-" * 80)
    try:
        response = requests.get('http://localhost:5001/api/orders', timeout=10)
        result = response.json()
        if result.get('status') == 'success':
            orders = result.get('data', {}).get('list', [])
            print(f"✅ 获取订单列表成功 (共 {len(orders)} 个订单)")
            results.append(("获取订单列表", True))
        else:
            print(f"❌ 获取订单列表失败: {result.get('message')}")
            results.append(("获取订单列表", False))
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        results.append(("获取订单列表", False))

    # 测试5: 获取用户信息
    print(f"\n👤 测试 5: 获取用户信息")
    print("-" * 80)
    try:
        response = requests.get('http://localhost:5001/api/user/power?invite_code=CILIAI88', timeout=10)
        result = response.json()
        if result.get('status') == 'success':
            print(f"✅ 获取用户信息成功")
            print(f"   - 算力: {result.get('compute_power')}")
            print(f"   - 总消耗: {result.get('total_power_used', 0)}")
            results.append(("获取用户信息", True))
        else:
            print(f"❌ 获取用户信息失败: {result.get('message')}")
            results.append(("获取用户信息", False))
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        results.append(("获取用户信息", False))

    # 打印测试总结
    print("\n" + "=" * 80)
    print(" 测试总结")
    print("=" * 80)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {status} - {test_name}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常。")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查。")

    print("=" * 80)

if __name__ == '__main__':
    test_end_to_end()
