@echo off
chcp 65001 >nul
echo =============================================
echo    CiliAI短剧平台 - 停止所有服务
echo =============================================
echo.

echo [1/4] 停止后端服务（端口5001）...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5001" ^| findstr "LISTENING"') do (
    echo 正在终止进程ID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if errorlevel 1 (
        echo 进程已停止或不存在
    ) else (
        echo 进程已终止
    )
)

echo [2/4] 停止npm进程...
taskkill /F /IM "node.exe" >nul 2>&1
if errorlevel 1 (
    echo 没有找到运行中的Node.js进程
) else (
    echo 所有Node.js进程已终止
)

echo [3/4] 关闭启动窗口...
taskkill /F /FI "WINDOWTITLE eq CiliAI-Backend" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq CiliAI-Admin-UI" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq CiliAI-User-UI" >nul 2>&1

echo [4/4] 验证端口...
netstat -ano | findstr ":5001" >nul 2>&1
if errorlevel 1 (
    echo 端口5001已释放
) else (
    echo 警告：端口5001仍被占用
)

netstat -ano | findstr ":3002" >nul 2>&1
if errorlevel 1 (
    echo 端口3002已释放
) else (
    echo 警告：端口3002仍被占用
)

netstat -ano | findstr ":3003" >nul 2>&1
if errorlevel 1 (
    echo 端口3003已释放
) else (
    echo 警告：端口3003仍被占用
)

echo.
echo =============================================
echo  所有服务已停止！
echo =============================================
echo.
pause
