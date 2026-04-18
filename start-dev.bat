@echo off
echo ========================================
echo 启动本地开发环境
echo ========================================

echo.
echo [1/3] 检查并安装Python依赖...
pip install -r requirements.txt

echo.
echo [2/3] 检查并安装前端依赖...
npm install

echo.
echo [3/3] 构建前端...
npm run build

echo.
echo ========================================
echo 启动Flask后端服务...
echo ========================================
echo 后端服务将在 http://localhost:5001 启动
echo 按 Ctrl+C 停止服务
echo.

python init_mysql_db.py
python app.py
