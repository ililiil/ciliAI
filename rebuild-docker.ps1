# CiliAI Docker Rebuild Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CiliAI Docker Rebuild Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location "D:\fangtang\ciliAI"

Write-Host "[1/4] Stopping all Docker containers..." -ForegroundColor Yellow
& docker stop ciliai-backend ciliai-frontend ciliai-admin ciliai-mysql ciliai 2>$null
& docker rm ciliai-backend ciliai-frontend ciliai-admin ciliai-mysql ciliai 2>$null
Write-Host "[OK] Containers stopped" -ForegroundColor Green

Write-Host ""
Write-Host "[2/4] Removing old images..." -ForegroundColor Yellow
& docker rmi ciliai-backend:latest ciliai-frontend:latest ciliai-admin:latest ciliai:latest 2>$null
Write-Host "[OK] Old images removed" -ForegroundColor Green

Write-Host ""
Write-Host "[3/4] Rebuilding all services..." -ForegroundColor Yellow
& docker-compose build --no-cache

Write-Host ""
Write-Host "[4/4] Starting all services..." -ForegroundColor Yellow
& docker-compose up -d

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Rebuild and start completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Current running containers:" -ForegroundColor White
& docker ps --format "table {{.Names}}	{{.Status}}	{{.Ports}}"

Write-Host ""
Write-Host "View logs:" -ForegroundColor White
Write-Host "  docker-compose logs -f" -ForegroundColor Gray
Write-Host ""
