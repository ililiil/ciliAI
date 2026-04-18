# 测试前端nginx代理

Write-Host "=== 测试前端nginx代理 ===" -ForegroundColor Cyan

# 测试1: 直接访问后端
Write-Host "`n1. 直接访问后端 API:" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5001/api/admin/invite-codes" -Method GET
    Write-Host "状态码: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "错误: $($_.Exception.Message)" -ForegroundColor Red
}

# 测试2: 通过前端nginx访问
Write-Host "`n2. 通过前端nginx访问 API:" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3003/api/admin/invite-codes" -Method GET
    Write-Host "状态码: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "响应长度: $($response.Content.Length)" -ForegroundColor Green
} catch {
    Write-Host "错误: $($_.Exception.Message)" -ForegroundColor Red
}

# 测试3: 检查nginx进程
Write-Host "`n3. 检查nginx进程:" -ForegroundColor Yellow
$nginxProcess = docker exec ciliai-frontend ps aux | Select-String -Pattern "nginx"
Write-Host $nginxProcess -ForegroundColor Cyan

# 测试4: 检查nginx配置
Write-Host "`n4. 检查nginx配置:" -ForegroundColor Yellow
$config = docker exec ciliai-frontend cat /etc/nginx/conf.d/default.conf
Write-Host $config -ForegroundColor Cyan

Write-Host "`n=== 测试完成 ===" -ForegroundColor Cyan
