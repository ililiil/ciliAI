# CiliAI短剧平台 - PowerShell停止脚本
# 适用于Windows PowerShell 5.0+

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   CiliAI短剧平台 - 停止所有服务" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# 停止后端服务（端口5001）
Write-Host "[1/4] 停止后端服务（端口5001）..." -ForegroundColor Yellow
$connections = Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue
if ($connections) {
    foreach ($conn in $connections) {
        Write-Host "   正在终止进程ID: $($conn.OwningProcess)" -ForegroundColor Gray
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    Write-Host "   后端服务已停止" -ForegroundColor Green
} else {
    Write-Host "   端口5001未被占用" -ForegroundColor Gray
}

# 停止Node.js进程
Write-Host "[2/4] 停止Node.js进程..." -ForegroundColor Yellow
$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    $count = $nodeProcesses.Count
    Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
    Write-Host "   已停止 $count 个Node.js进程" -ForegroundColor Green
} else {
    Write-Host "   没有找到运行中的Node.js进程" -ForegroundColor Gray
}

# 验证端口
Write-Host "[3/4] 验证端口状态..." -ForegroundColor Yellow
$ports = @(5001, 3002, 3003)
foreach ($port in $ports) {
    $status = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($status) {
        Write-Host "   端口 $port : 仍被占用 (PID: $($status.OwningProcess))" -ForegroundColor Red
    } else {
        Write-Host "   端口 $port : 已释放" -ForegroundColor Green
    }
}

Write-Host "[4/4] 完成！" -ForegroundColor Green

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " 所有服务已停止！" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Start-Sleep -Seconds 1
