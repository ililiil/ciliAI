Write-Host "=== 测试邀请码列表 ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5001/api/admin/invite-codes" -Method GET -TimeoutSec 10
    Write-Host "✅ 列表获取成功，总数: $($response.data.total)" -ForegroundColor Green
    
    Write-Host "`n前3条邀请码:" -ForegroundColor Cyan
    $response.data.list | Select-Object -First 3 | ForEach-Object {
        Write-Host "  邀请码: $($_.code), 配额: $($_.compute_power), 使用次数: $($_.use_count)" -ForegroundColor White
    }
} catch {
    Write-Host "❌ 列表获取失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== 测试批量创建邀请码 ===" -ForegroundColor Yellow
try {
    $body = @{
        count = 3
        compute_power = 1000
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:5001/api/admin/invite-codes/batch" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 10
    
    Write-Host "✅ 批量创建成功: $($response.msg)" -ForegroundColor Green
    Write-Host "生成的邀请码: $($response.data.codes -join ', ')" -ForegroundColor Cyan
} catch {
    Write-Host "❌ 批量创建失败: $($_.Exception.Message)" -ForegroundColor Red
}
