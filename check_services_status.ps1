# CiliAI服务状态检查脚本

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   CiliAI系统 - 服务状态检查" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$services = @(
    @{Name="后端API"; Port=5001; Description="Flask后端服务"},
    @{Name="用户端"; Port=3003; Description="CiliAI用户界面"},
    @{Name="管理后台"; Port=3002; Description="系统管理员界面"}
)

$allRunning = $true

foreach ($service in $services) {
    Write-Host "检查 $($service.Name) ($($service.Description))..." -NoNewline
    
    $result = Test-NetConnection -ComputerName "localhost" -Port $service.Port -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
    
    if ($result.TcpTestSucceeded) {
        Write-Host " ✅ 运行中 (端口 $($service.Port))" -ForegroundColor Green
    } else {
        Write-Host " ❌ 未运行" -ForegroundColor Red
        $allRunning = $false
    }
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan

if ($allRunning) {
    Write-Host "  ✅ 所有服务正在运行" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 访问地址：" -ForegroundColor Cyan
    Write-Host "   • 用户端：  http://localhost:3003" -ForegroundColor White
    Write-Host "   • 管理后台：http://localhost:3002" -ForegroundColor White
} else {
    Write-Host "  ⚠️  部分服务未运行" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请运行 start_all.bat 或 start_all.ps1 启动所有服务" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
