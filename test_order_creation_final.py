import requests
import json
from datetime import datetime

def test_order_creation():
    print("=" * 80)
    print("订单创建功能最终测试")
    print("=" * 80)

    url = 'http://localhost:5001/api/orders'

    test_cases = [
        {
            'name': '测试1: 完整数据',
            'data': {
                'invite_code': 'CILIAI88',
                'title': f'测试订单_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'image': 'https://example.com/test.jpg',
                'price': '¥100',
                'status': 'recruiting',
                'description': '测试描述',
                'contact_count': 0,
                'deadline': '2026-04-30',
                'tags': '["测试"]',
                'contact_info': '测试联系方式'
            }
        },
        {
            'name': '测试2: 最小数据',
            'data': {
                'invite_code': 'CILIAI88',
                'title': '最小数据测试',
                'image': 'https://example.com/min.jpg',
                'price': '¥50',
                'status': 'recruiting'
            }
        },
        {
            'name': '测试3: 无用户关联',
            'data': {
                'title': '无用户测试',
                'image': 'https://example.com/no_user.jpg',
                'price': '¥200',
                'status': 'pending'
            }
        }
    ]

    results = []

    for test_case in test_cases:
        print(f"\n{test_case['name']}")
        print("-" * 80)
        print(f"发送数据: {json.dumps(test_case['data'], ensure_ascii=False, indent=2)}")

        try:
            response = requests.post(
                url,
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            print(f"\n响应状态码: {response.status_code}")

            try:
                result = response.json()
                print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

                if result.get('status') == 'success':
                    print(f"\n✅ {test_case['name']} - 成功! 订单ID: {result.get('order_id')}")
                    results.append((test_case['name'], True, result.get('order_id')))
                else:
                    print(f"\n❌ {test_case['name']} - 失败: {result.get('message')}")
                    results.append((test_case['name'], False, result.get('message')))

            except json.JSONDecodeError:
                print(f"\n❌ JSON解析失败: {response.text}")
                results.append((test_case['name'], False, "JSON解析错误"))

        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            results.append((test_case['name'], False, str(e)))

    # 总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for name, success, detail in results:
        status = "✅ 成功" if success else "❌ 失败"
        detail_text = f"(ID: {detail})" if success else f"({detail})"
        print(f"{status:10} {name:30} {detail_text}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过!")
        print("\n✅ 订单创建功能完全正常!")
        print("\n现在您可以:")
        print("1. 打开浏览器访问: http://localhost:3003")
        print("2. 登录系统")
        print("3. 进入接单广场")
        print("4. 点击发布商单")
        print("5. 填写表单并提交")
        print("6. 应该能看到成功提示")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败")

    print("=" * 80)

if __name__ == '__main__':
    test_order_creation()
