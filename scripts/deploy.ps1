@echo off
REM ===========================================
REM CiliAI Docker Setup Script (Windows)
REM ===========================================

setlocal enabledelayedexpansion

set ENV=%1

if "%ENV%"=="" set ENV=prod

if "%ENV%" neq "prod" if "%ENV%" neq "dev" (
    echo Error: Environment must be 'prod' or 'dev'
    exit /b 1
)

echo ==========================================
echo CiliAI Docker Setup Script
echo ==========================================

if "%ENV%"=="prod" (
    echo Setting up production environment...

    if not exist .env (
        echo Creating .env from template...
        copy .env.prod.example .env
        echo Please edit .env file with your configuration:
        echo   - MYSQL_ROOT_PASSWORD
        echo   - MYSQL_PASSWORD
        echo   - VOLC_AK
        echo   - VOLC_SK
        echo.
        pause
    )

    echo Building Docker images...
    docker-compose -f docker-compose.prod.yml build

    echo Starting services...
    docker-compose -f docker-compose.prod.yml up -d

    echo Checking service health...
    timeout /t 10 /nobreak >nul
    docker-compose -f docker-compose.prod.yml ps

    echo.
    echo Service URLs:
    echo   - Backend API: http://localhost:5001
    echo   - Frontend: http://localhost:3003
    echo   - Admin: http://localhost:3002
)

if "%ENV%"=="dev" (
    echo Setting up development environment...

    if not exist .env.dev (
        echo Creating .env.dev from template...
        copy .env.dev.example .env.dev
        echo Please edit .env.dev file with your configuration
        echo.
        pause
    )

    echo Building Docker images...
    docker-compose -f docker-compose.dev.yml build

    echo Starting services...
    docker-compose -f docker-compose.dev.yml up -d

    echo Checking service health...
    timeout /t 10 /nobreak >nul
    docker-compose -f docker-compose.dev.yml ps

    echo.
    echo Service URLs:
    echo   - Backend API: http://localhost:5001
    echo   - Frontend: http://localhost:3003
    echo   - Admin: http://localhost:3002
)

echo.
echo ==========================================
echo Setup completed!
echo To view logs: docker-compose -f docker-compose.%ENV%.yml logs -f
echo To stop services: docker-compose -f docker-compose.%ENV%.yml down
echo ==========================================

endlocal
