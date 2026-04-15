@echo off
chcp 65001 >nul
echo =============================================
echo    CiliAI短剧平台 - 启动所有服务
echo =============================================
echo.

echo [1/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python环境！
    echo 请先安装Python 3.9或更高版本
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python环境已就绪
echo.

echo [2/5] 检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Node.js环境！
    echo 请先安装Node.js 16 LTS或更高版本
    echo 下载地址：https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js环境已就绪
echo.

echo [3/5] 检查端口占用情况...
netstat -ano | findstr ":5001" >nul 2>&1
if not errorlevel 1 (
    echo [警告] 端口5001已被占用，尝试查找并终止进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5001" ^| findstr "LISTENING"') do (
        echo 终止进程ID: %%a
        taskkill /F /PID %%a >nul 2>&1
    )
)

netstat -ano | findstr ":3002" >nul 2>&1
if not errorlevel 1 (
    echo [警告] 端口3002已被占用
)

netstat -ano | findstr ":3003" >nul 2>&1
if not errorlevel 1 (
    echo [警告] 端口3003已被占用
)
echo.

echo [4/5] 启动用户端后端服务（端口5001）...
echo        - API地址: http://localhost:5001
start "CiliAI-Backend" cmd /k "cd /d %~dp0ciliAI && python app.py"
timeout /t 3 /nobreak >nul

echo [5/5] 启动前端服务...
echo        - 管理后台: http://localhost:3002
echo        - 用户端: http://localhost:3003
start "CiliAI-Admin-UI" cmd /k "cd /d %~dp0ruoyi && npm run dev"
timeout /t 2 /nobreak >nul
start "CiliAI-User-UI" cmd /k "cd /d %~dp0ciliAI && npm run dev"

echo.
echo =============================================
echo  所有服务启动中！
echo =============================================
echo.
echo 访问地址：
echo   - 用户端：http://localhost:3003
echo   - 管理后台：http://localhost:3002
echo   - 用户端API：http://localhost:5001
echo.
echo 登录凭证：
echo   - 用户端：使用8位邀请码注册
echo   - 管理后台：admin / admin123
echo.
echo 关闭服务：
echo   - 请关闭对应的命令行窗口
echo   - 或使用 stop_services.bat 快速停止
echo.
echo 详细文档：请查看 docs\STARTUP_GUIDE.md
echo =============================================
pause
