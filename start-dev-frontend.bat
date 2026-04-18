@echo off
echo ========================================
echo 启动本地开发环境（前端开发模式）
echo ========================================

echo.
echo [1/2] 检查并安装Python依赖...
pip install -r requirements.txt

echo.
echo [2/2] 检查并安装前端依赖...
npm install

echo.
echo ========================================
echo 启动开发服务器...
echo ========================================
echo 后端服务将在 http://localhost:5001 启动
echo 前端开发服务器将在 http://localhost:5173 启动
echo 按 Ctrl+C 停止服务
echo.

start cmd /k "npm run dev"
python init_mysql_db.py
python app.py
