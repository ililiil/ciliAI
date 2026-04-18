@echo off
chcp 65001 >nul
echo =============================================
echo    CiliAI - 重新构建并启动Docker容器
echo =============================================
echo.

cd /d "%~dp0"

echo [1/4] 停止所有Docker容器...
docker stop ciliai-backend ciliai-frontend ciliai-admin ciliai-mysql ciliai 2>nul
docker rm ciliai-backend ciliai-frontend ciliai-admin ciliai-mysql ciliai 2>nul
echo.

echo [2/4] 删除旧镜像...
docker rmi ciliai-backend:latest ciliai-frontend:latest ciliai-admin:latest ciliai:latest 2>nul
echo.

echo [3/4] 重新构建所有服务...
docker-compose build --no-cache
echo.

echo [4/4] 启动所有服务...
docker-compose up -d
echo.

echo =============================================
echo  ✅ 重新构建和启动完成！
echo =============================================
echo.
echo 📋 当前运行中的容器：
docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"
echo.
echo 📖 查看日志：
echo    docker-compose logs -f
echo.
pause
