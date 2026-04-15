# CiliAI短剧平台 - PowerShell启动脚本
# 适用于Windows PowerShell 5.0+

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   CiliAI短剧平台 - 启动所有服务" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python环境
Write-Host "[1/5] 检查Python环境..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK]" -ForegroundColor Green
        Write-Host "       $pythonVersion" -ForegroundColor Gray
    } else {
        throw "Python未安装"
    }
} catch {
    Write-Host " [错误]" -ForegroundColor Red
    Write-Host "未检测到Python环境！" -ForegroundColor Red
    Write-Host "请先安装Python 3.9或更高版本" -ForegroundColor Yellow
    Write-Host "下载地址：https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按Enter键退出"
    exit 1
}

# 检查Node.js环境
Write-Host "[2/5] 检查Node.js环境..." -NoNewline
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK]" -ForegroundColor Green
        Write-Host "       $nodeVersion" -ForegroundColor Gray
    } else {
        throw "Node.js未安装"
    }
} catch {
    Write-Host " [错误]" -ForegroundColor Red
    Write-Host "未检测到Node.js环境！" -ForegroundColor Red
    Write-Host "请先安装Node.js 16 LTS或更高版本" -ForegroundColor Yellow
    Write-Host "下载地址：https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "按Enter键退出"
    exit 1
}

# 检查端口占用情况
Write-Host "[3/5] 检查端口占用情况..."
$ports = @(5001, 3002, 3003)
foreach ($port in $ports) {
    $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connection) {
        Write-Host "       端口 $port 已被占用 (PID: $($connection.OwningProcess))" -ForegroundColor Yellow
    } else {
        Write-Host "       端口 $port 可用" -ForegroundColor Gray
    }
}

# 启动后端服务
Write-Host "[4/5] 启动用户端后端服务（端口5001）..." -ForegroundColor Cyan
Write-Host "       - API地址: http://localhost:5001" -ForegroundColor Gray
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\ciliAI && python app.py" -WindowStyle Normal -PassThru | Out-Null
Write-Host "       后端服务已启动" -ForegroundColor Green
Start-Sleep -Seconds 3

# 启动前端服务
Write-Host "[5/5] 启动前端服务..." -ForegroundColor Cyan
Write-Host "       - 管理后台: http://localhost:3002" -ForegroundColor Gray
Write-Host "       - 用户端: http://localhost:3003" -ForegroundColor Gray

Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\ruoyi && npm run dev" -WindowStyle Normal -PassThru | Out-Null
Write-Host "       管理后台已启动" -ForegroundColor Green
Start-Sleep -Seconds 2

Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\ciliAI && npm run dev" -WindowStyle Normal -PassThru | Out-Null
Write-Host "       用户端已启动" -ForegroundColor Green

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " 所有服务启动中！" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址：" -ForegroundColor White
Write-Host "  - 用户端：http://localhost:3003" -ForegroundColor Green
Write-Host "  - 管理后台：http://localhost:3002" -ForegroundColor Green
Write-Host "  - 用户端API：http://localhost:5001" -ForegroundColor Green
Write-Host ""
Write-Host "登录凭证：" -ForegroundColor White
Write-Host "  - 用户端：使用8位邀请码注册" -ForegroundColor Gray
Write-Host "  - 管理后台：admin / admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "关闭服务：" -ForegroundColor White
Write-Host "  - 请关闭对应的命令行窗口" -ForegroundColor Gray
Write-Host "  - 或使用 stop_services.bat / stop_services.ps1 快速停止" -ForegroundColor Gray
Write-Host ""
Write-Host "详细文档：请查看 docs\STARTUP_GUIDE.md" -ForegroundColor Gray
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# 等待几秒后提示用户
Start-Sleep -Seconds 2
Write-Host "提示：窗口已打开，服务正在启动中..." -ForegroundColor Yellow
