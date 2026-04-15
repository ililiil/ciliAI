import requests
import json

url = 'http://localhost:5001/api/projects'

# 测试1：正常数据
test_data_1 = {
    'invite_code': 'test_invite_code',
    'title': '测试项目1',
    'description': '测试描述1',
    'cover_image': ''
}

# 测试2：包含cover_file字段（null值）
test_data_2 = {
    'invite_code': 'test_invite_code',
    'title': '测试项目2',
    'description': '测试描述2',
    'cover_image': '',
    'cover_file': None
}

# 测试3：包含cover_file字段（带值）
test_data_3 = {
    'invite_code': 'test_invite_code',
    'title': '测试项目3',
    'description': '测试描述3',
    'cover_image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
    'cover_file': 'dummy_file'
}

def test_api(test_name, data):
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print(f"{'='*60}")
    print(f"发送数据: {json.dumps(data, ensure_ascii=False)}")

    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

        if response.status_code != 200:
            print(f"❌ 请求失败!")
        elif response.json().get('status') == 'success':
            print(f"✅ 请求成功!")
        else:
            print(f"❌ 业务逻辑失败!")
    except Exception as e:
        print(f"\n❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()

# 执行测试
test_api("正常数据（无cover_file）", test_data_1)
test_api("包含cover_file字段（null）", test_data_2)
test_api("包含cover_file字段（带值）", test_data_3)
