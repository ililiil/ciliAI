import requests
import json

BASE_URL = "http://localhost:5001"


def test_key_rotation():
    print("测试密钥轮询功能...")
    print("-" * 50)

    invite_code = "11111111"

    params = {
        "prompt": "测试图片",
        "width": 1024,
        "height": 1024,
        "invite_code": invite_code,
        "project_id": 1
    }

    print("发送3次API请求，测试密钥轮询...")

    for i in range(3):
        print(f"\n请求 {i+1}:")
        try:
            response = requests.post(
                f"{BASE_URL}/api/generate",
                json=params,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    print(f"✓ 请求成功")
                    print(f"  Task ID: {data.get('task_id')}")
                    print(f"  图片数量: {len(data.get('images', []))}")
                else:
                    print(f"✗ 请求失败: {data.get('message')}")
            elif response.status_code == 401:
                print(f"✗ 用户不存在（正常，因为邀请码无效）")
                print(f"  响应: {response.text[:200]}")
            else:
                print(f"✗ HTTP错误: {response.status_code}")
                print(f"  响应: {response.text[:200]}")

        except Exception as e:
            print(f"✗ 请求异常: {str(e)}")

    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n检查应用日志，确认密钥轮询是否正常工作")
    print("你应该能看到类似这样的日志:")
    print("  INFO - 使用密钥组 1 (AK: AKLTNzVlZT...)")


def create_test_user():
    """创建测试用户"""
    print("\n创建测试用户...")
    response = requests.post(
        f"{BASE_URL}/api/verify-invite-code",
        json={"invite_code": "11111111"},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print(f"✓ 用户创建成功，初始算力: {data.get('算力')}")
            return True
        else:
            print(f"✗ 创建失败: {data.get('message')}")
            return False
    else:
        print(f"✗ HTTP错误: {response.status_code}")
        print(f"  响应: {response.text}")
        return False


if __name__ == "__main__":
    if create_test_user():
        test_key_rotation()
    else:
        print("\n无法创建测试用户，跳过密钥轮询测试")
