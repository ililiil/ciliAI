# CiliAI Docker 快速启动脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CiliAI Docker 部署脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Docker是否运行
Write-Host "检查Docker Desktop状态..." -ForegroundColor Yellow
try {
    $dockerStatus = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker未运行"
    }
    Write-Host "✓ Docker正在运行" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker未运行或未安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装Docker Desktop：https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Write-Host "详细安装指南：查看 DOCKER_INSTALL_GUIDE.md" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# 检查.env文件
Write-Host "检查配置文件..." -ForegroundColor Yellow
$envFile = "ciliAI\.env"
if (-not (Test-Path $envFile)) {
    Write-Host "✗ .env文件不存在，正在创建..." -ForegroundColor Red
    Copy-Item "$envFile.example" $envFile
    Write-Host ""
    Write-Host "请编辑 $envFile 文件，填入你的实际配置：" -ForegroundColor Yellow
    Write-Host "  - VOLC_AK: 火山引擎AccessKeyID" -ForegroundColor Yellow
    Write-Host "  - VOLC_SK: 火山引擎SecretAccessKey" -ForegroundColor Yellow
    Write-Host "  - DB_PASSWORD: MySQL数据库密码" -ForegroundColor Yellow
    Write-Host ""
    exit 1
} else {
    Write-Host "✓ 配置文件存在" -ForegroundColor Green
}

Write-Host ""

# 停止旧容器（如果存在）
Write-Host "停止旧容器..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null

# 构建并启动
Write-Host ""
Write-Host "构建Docker镜像..." -ForegroundColor Yellow
docker-compose build

Write-Host ""
Write-Host "启动所有服务..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  服务已启动！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址：" -ForegroundColor White
Write-Host "  - 后端API：http://localhost:5001" -ForegroundColor Cyan
Write-Host "  - 用户端：http://localhost:3003" -ForegroundColor Cyan
Write-Host "  - 管理后台：http://localhost:3002" -ForegroundColor Cyan
Write-Host ""
Write-Host "查看日志：" -ForegroundColor White
Write-Host "  docker-compose logs -f" -ForegroundColor Gray
Write-Host ""
Write-Host "停止服务：" -ForegroundColor White
Write-Host "  docker-compose down" -ForegroundColor Gray
Write-Host ""
