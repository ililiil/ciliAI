import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

with app.test_client() as client:
    print("=" * 80)
    print("直接测试作品创建API")
    print("=" * 80)

    test_data = {
        'title': '直接测试作品',
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

    print(f"\n发送数据: {test_data}")

    try:
        response = client.post('/api/admin/works', json=test_data)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应数据: {response.get_json()}")

        if response.status_code == 200:
            print("\n✅ 作品创建成功!")
        else:
            print(f"\n❌ 作品创建失败: {response.get_json()}")

    except Exception as e:
        print(f"\n❌ 发生异常: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 80)
