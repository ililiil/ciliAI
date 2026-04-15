@echo off
chcp 65001 >nul
echo =============================================
echo    CiliAI系统 - 一键启动所有服务
echo =============================================
echo.

echo [提示] 检查Python环境...
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

echo [1/3] 启动后端服务（Flask API）...
echo        - 后端API: http://localhost:5001
echo        - 说明: 为用户端和管理后台提供API支持
start "CiliAI-Backend" cmd /k "cd /d %~dp0ciliAI && python app.py"

timeout /t 3 /nobreak >nul

echo [2/3] 启动用户端（ciliAI）...
echo        - 用户端界面: http://localhost:3003
echo        - 说明: CiliAI用户使用界面
start "CiliAI-User-Frontend" cmd /k "cd /d %~dp0ciliAI && npm run dev"

timeout /t 3 /nobreak >nul

echo [3/3] 启动管理后台（ruoyi）...  ⚠️
echo        - 管理后台: http://localhost:3002
echo        - 说明: 系统管理员使用界面（注意不要遗漏！）
start "CiliAI-Admin-Backend" cmd /k "cd /d %~dp0ruoyi && npm run dev"

echo.
echo =============================================
echo  ✅ 所有服务已启动！
echo =============================================
echo.
echo 📋 访问地址汇总：
echo   ┌─────────────────────────────────────────┐
echo   │  服务名称    │   端口   │   说明        │
echo   ├─────────────────────────────────────────┤
echo   │  后端API     │   5001   │   Flask后端   │
echo   │  用户端      │   3003   │   用户界面    │
echo   │  管理后台    │   3002   │ ⚠️ 管理员界面 │
echo   └─────────────────────────────────────────┘
echo.
echo 🚀 请在浏览器中访问：
echo   • 用户端：  http://localhost:3003
echo   • 管理后台：http://localhost:3002
echo.
echo ⚠️  重要提醒：
echo   • 三个服务必须全部运行才能正常使用系统
echo   • 管理后台（ruoyi）容易被遗漏！
echo   • 如果端口被占用，Vite会自动选择下一个端口
echo.
echo 📖 详细文档：请查看 CILIAI_STARTUP_GUIDE.md
echo =============================================
pause
