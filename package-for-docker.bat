@echo off
echo ========================================
echo 打包项目用于Docker部署
echo ========================================

set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set PACKAGE_NAME=ciliai-docker-package_%TIMESTAMP%
set PACKAGE_DIR=..\%PACKAGE_NAME%

echo.
echo [1/5] 创建打包目录...
if exist %PACKAGE_DIR% rmdir /s /q %PACKAGE_DIR%
mkdir %PACKAGE_DIR%

echo.
echo [2/5] 复制后端文件...
copy app.py %PACKAGE_DIR%\
copy key_manager.py %PACKAGE_DIR%\
copy db_manager.py %PACKAGE_DIR%\
copy init_mysql_db.py %PACKAGE_DIR%\
copy requirements.txt %PACKAGE_DIR%\
copy Dockerfile %PACKAGE_DIR%\
copy docker-compose.yml %PACKAGE_DIR%\

echo.
echo [3/5] 复制前端文件...
copy package.json %PACKAGE_DIR%\
copy package-lock.json %PACKAGE_DIR%\
xcopy /E /I /Y src %PACKAGE_DIR%\src
xcopy /E /I /Y public %PACKAGE_DIR%\public
if exist vite.config.js copy vite.config.js %PACKAGE_DIR%\
if exist vite.config.ts copy vite.config.ts %PACKAGE_DIR%\

echo.
echo [4/5] 复制配置文件...
if exist .env (
    echo 警告: 检测到.env文件，将复制.env.example作为模板
    copy .env.example %PACKAGE_DIR%\.env
) else (
    if exist .env.example copy .env.example %PACKAGE_DIR%\.env
)

echo.
echo [5/5] 创建部署说明文档...
(
echo # CiliAI Docker部署包
echo.
echo ## 部署步骤
echo.
echo 1. **配置环境变量**
echo    - 编辑 .env 文件，配置数据库连接等必要参数
echo.
echo 2. **构建并启动Docker容器**
echo    ```bash
echo    docker-compose up -d --build
echo    ```
echo.
echo 3. **查看日志**
echo    ```bash
echo    docker-compose logs -f
echo    ```
echo.
echo 4. **停止服务**
echo    ```bash
echo    docker-compose down
echo    ```
echo.
echo ## 服务访问
echo - 后端API: http://localhost:5001
echo - 前端页面: http://localhost:5001
echo.
echo ## 注意事项
echo - 确保已安装Docker和Docker Compose
echo - 确保端口5001未被占用
echo - 首次启动会自动初始化数据库
echo.
echo ## 文件说明
echo - Dockerfile: Docker镜像构建文件
echo - docker-compose.yml: Docker Compose配置文件
echo - app.py: Flask后端主程序
echo - requirements.txt: Python依赖
echo - package.json: 前端依赖配置
echo - src/: 前端源代码
echo.
echo 打包时间: %date% %time%
) > %PACKAGE_DIR%\DEPLOY.md

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo 打包目录: %PACKAGE_DIR%
echo.
echo 请将 %PACKAGE_NAME% 目录发送给运维人员
echo 运维人员可以参考 DEPLOY.md 进行部署
echo.
pause
