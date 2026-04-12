@echo off
chcp 65001 >nul
echo ===================================================
echo       即梦 AI 4.0 - Windows 局域网服务一键启动
echo ===================================================
echo.

python --version >nul 2>&1
if errorlevel 1 goto nopython
goto haspython

:nopython
echo [错误] 未检测到 Python 环境！
echo 正在为您自动打开微软商店下载 Python...
echo 请在商店中点击“获取/安装”，安装完成后重新双击本脚本！
start ms-windows-store://pdp/?productid=9NRWMJP3717K
pause
exit

:haspython
echo [1/4] 检测到 Python 已安装，正在准备虚拟环境...
if exist venv\Scripts\activate.bat goto hasvenv
echo 正在首次创建虚拟环境 (大约需要 10 秒)...
python -m venv venv

:hasvenv
echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [3/4] 检查并安装项目依赖包 (第一次可能需要下载，请稍候)...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

echo.
echo [4/4] 一切就绪！正在启动服务器...
echo.
echo ===================================================
echo [成功] 服务器已启动！请不要关闭这个黑色窗口。
echo [访问方式] 在此电脑或局域网手机/电脑的浏览器输入：
echo          http://localhost:5001 (本机测)
echo       或 http://你的局域网IP:5001 (其他设备访问)
echo ===================================================
echo.

python app.py

echo.
echo 服务器已意外停止运行（如果出错请截图发送给开发者）。
pause
