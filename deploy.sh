#!/bin/bash
# 一键部署代码到 Windows 测试服务器的脚本

TARGET="Admin@172.16.109.120"
# 将下面这里的路径替换为你希望在 Windows 电脑上存放代码的实际路径
REMOTE_DIR="D:/即梦"

echo "==========================================="
echo "  🚀 即梦 AI - 一键推送代码到 Windows 服务器"
echo "==========================================="

echo "[1/3] 正在打包本地最新代码..."
# 排除虚拟环境和缓存文件夹，打个干净的包
zip -r /tmp/jimeng_deploy.zip . -x "venv/*" -x "__pycache__/*" -x ".DS_Store" -x ".git/*" > /dev/null

echo "[2/3] 正在通过网络发送到 Windows ($TARGET)..."
scp /tmp/jimeng_deploy.zip $TARGET:C:/Users/Admin/jimeng_deploy.zip

# 1. 杀旧进程，创建目录，解压代码文件，删压缩包
ssh $TARGET "mkdir \"${REMOTE_DIR}\" 2>nul & tar -xf C:/Users/Admin/jimeng_deploy.zip -C \"${REMOTE_DIR}\" & del C:\Users\Admin\jimeng_deploy.zip"

# 2. 用 PM2 热重启服务（支持安装新依赖）
ssh $TARGET "cd /d \"${REMOTE_DIR}\" & pip install -r requirements.txt >nul 2>&1 & pm2 restart jimeng"

echo ""
echo "✅ PM2 热更与推送完成！"
echo "代码已发版，PM2 已经自动帮你重启了后台 Node/Python 守护进程！"
echo "访问地址： http://172.16.109.120:5001"
