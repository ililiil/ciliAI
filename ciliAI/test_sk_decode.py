import base64

sk = "WVdWaVkyTm1NR0psWm1RM05HRm1ZV0k0TWprMlpEbG1ORFJrTVdKa09Eaw=="

print("原始 SK (Base64):", sk)
print("长度:", len(sk))

try:
    decoded = base64.b64decode(sk)
    print("\n解码后 (UTF-8):", decoded.decode('utf-8'))
    print("解码后长度:", len(decoded))
except Exception as e:
    print(f"\n解码失败: {e}")

sk_direct = "WVdWaVkyTm1NR0ksWm1RM05HRm1ZV0k0TWprMlpEbG1ORFJrTVdKa09Eaw=="

print("\n" + "="*60)
print("检查 SK 格式:")
print("原始:", sk_direct)
print("包含填充符 (=):", '=' in sk_direct)
print("这是有效的 Base64:", len(sk_direct) % 4 == 0)
