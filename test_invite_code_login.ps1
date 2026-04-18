# PowerShell测试脚本 - 邀请码功能测试

Write-Host "=== 邀请码功能测试 ===" -ForegroundColor Cyan

# 测试1: 直接访问后端API
Write-Host "`n1. 直接访问后端 API:" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5001/api/admin/invite-codes" -Method GET
    Write-Host "状态: 成功" -ForegroundColor Green
    Write-Host "邀请码总数: $($response.data.total)" -ForegroundColor Green
    Write-Host "第一个邀请码: $($response.data.list[0].code)" -ForegroundColor Cyan
} catch {
    Write-Host "错误: $($_.Exception.Message)" -ForegroundColor Red
}

# 测试2: 通过nginx访问
Write-Host "`n2. 通过nginx访问 API (localhost:3003):" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:3003/api/admin/invite-codes" -Method GET -TimeoutSec 10
    Write-Host "状态: 成功" -ForegroundColor Green
    Write-Host "邀请码总数: $($response.data.total)" -ForegroundColor Green
} catch {
    Write-Host "错误: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "提示: 如果返回500错误，请尝试清除浏览器缓存或使用无痕模式" -ForegroundColor Yellow
}

# 测试3: 验证邀请码
Write-Host "`n3. 验证邀请码 (64C0412C):" -ForegroundColor Yellow
try {
    $body = @{
        invite_code = "64C0412C"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5001/api/verify-invite-code" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"

    Write-Host "状态: $($response.status)" -ForegroundColor Green
    Write-Host "消息: $($response.message)" -ForegroundColor Green
    Write-Host "算力: $($response.'算力')" -ForegroundColor Cyan
} catch {
    Write-Host "错误: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== 测试完成 ===" -ForegroundColor Cyan
Write-Host "`n如果所有测试通过，邀请码功能应该正常工作。" -ForegroundColor Green
Write-Host "请在浏览器中访问 http://localhost:3003 并尝试使用邀请码登录。" -ForegroundColor Green
