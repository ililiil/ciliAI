# CiliAI系统 - 一键启动脚本
# 使用PowerShell编写，提供更好的界面和错误处理

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   CiliAI系统 - 一键启动所有服务" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python环境
Write-Host "[检查] Python环境..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    Write-Host " ✅ OK" -ForegroundColor Green
    Write-Host "       $pythonVersion" -ForegroundColor Gray
} catch {
    Write-Host " ❌ 失败" -ForegroundColor Red
    Write-Host "       未检测到Python环境，请先安装Python 3.9+" -ForegroundColor Yellow
    Write-Host "       下载地址：https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 检查Node环境
Write-Host "[检查] Node.js环境..." -NoNewline
try {
    $nodeVersion = node --version 2>&1
    Write-Host " ✅ OK" -ForegroundColor Green
    Write-Host "       Node $nodeVersion" -ForegroundColor Gray
} catch {
    Write-Host " ❌ 失败" -ForegroundColor Red
    Write-Host "       未检测到Node.js环境，请先安装Node.js 16+" -ForegroundColor Yellow
    Write-Host "       下载地址：https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""
Write-Host "开始启动服务..." -ForegroundColor Cyan
Write-Host ""

# 启动后端服务
Write-Host "[1/3] 启动后端服务（Flask API）..." -ForegroundColor Yellow
Write-Host "       端口: 5001" -ForegroundColor Gray
Write-Host "       说明: 为用户端和管理后台提供统一的API支持" -ForegroundColor Gray
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\ciliAI && python app.py" -WindowStyle Normal -RedirectStandardOutput "$env:TEMP\ciliai_backend.log"
Start-Sleep -Seconds 2
Write-Host "       ✅ 后端服务已在新窗口启动" -ForegroundColor Green
Write-Host ""

# 启动用户端
Write-Host "[2/3] 启动用户端（ciliAI）..." -ForegroundColor Yellow
Write-Host "       端口: 3003" -ForegroundColor Gray
Write-Host "       说明: CiliAI用户使用界面" -ForegroundColor Gray
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\ciliAI && npm run dev" -WindowStyle Normal -RedirectStandardOutput "$env:TEMP\ciliai_user.log"
Start-Sleep -Seconds 3
Write-Host "       ✅ 用户端已在新窗口启动" -ForegroundColor Green
Write-Host ""

# 启动管理后台
Write-Host "[3/3] 启动管理后台（ruoyi）... ⚠️" -ForegroundColor Yellow
Write-Host "       端口: 3002" -ForegroundColor Gray
Write-Host "       说明: 系统管理员使用界面（注意不要遗漏！）" -ForegroundColor Gray
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\ruoyi && npm run dev" -WindowStyle Normal -RedirectStandardOutput "$env:TEMP\ciliai_admin.log"
Start-Sleep -Seconds 3
Write-Host "       ✅ 管理后台已在新窗口启动" -ForegroundColor Green
Write-Host ""

# 完成
Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "  ✅ 所有服务已成功启动！" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 访问地址汇总：" -ForegroundColor Cyan
Write-Host @"

  ┌─────────────────────────────────────────┐
  │  服务名称    │   端口   │   说明        │
  ├─────────────────────────────────────────┤
  │  后端API     │   5001   │   Flask后端   │
  │  用户端      │   3003   │   用户界面    │
  │  管理后台    │   3002   │ ⚠️ 管理员界面 │
  └─────────────────────────────────────────┘
"@ -ForegroundColor White
Write-Host ""
Write-Host "🚀 请在浏览器中访问：" -ForegroundColor Cyan
Write-Host "   • 用户端：  http://localhost:3003" -ForegroundColor White
Write-Host "   • 管理后台：http://localhost:3002" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  重要提醒：" -ForegroundColor Yellow
Write-Host "   • 三个服务必须全部运行才能正常使用系统" -ForegroundColor White
Write-Host "   • 管理后台（ruoyi）容易被遗漏！" -ForegroundColor Yellow
Write-Host "   • 如果端口被占用，Vite会自动选择下一个端口" -ForegroundColor White
Write-Host ""
Write-Host "📖 详细文档：查看 CILIAI_STARTUP_GUIDE.md" -ForegroundColor Gray
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# 提示用户查看新窗口
Write-Host "提示：各服务已在独立窗口中启动，请查看新打开的终端窗口" -ForegroundColor Gray
Write-Host ""
