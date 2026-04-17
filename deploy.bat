@echo off
REM ===========================================
REM CiliAI Docker Deployment Script (Windows)
REM ===========================================

setlocal enabledelayedexpansion

set ENV=%1
set ACTION=%2

if "%ENV%"=="" set ENV=prod
if "%ACTION%"=="" set ACTION=start

if "%ENV%" neq "prod" if "%ENV%" neq "dev" (
    echo Error: Environment must be 'prod' or 'dev'
    exit /b 1
)

if "%ACTION%" neq "start" if "%ACTION%" neq "stop" if "%ACTION%" neq "restart" if "%ACTION%" neq "logs" (
    echo Error: Action must be 'start', 'stop', 'restart', or 'logs'
    exit /b 1
)

echo ==========================================
echo CiliAI Docker Deployment Script
echo ==========================================
echo Environment: %ENV%
echo Action: %ACTION%
echo.

if "%ACTION%"=="start" (
    echo Starting CiliAI services...
    if "%ENV%"=="prod" (
        if not exist .env (
            echo Warning: .env file not found. Copying from .env.prod.example...
            copy .env.prod.example .env
            echo Please edit .env file with your configuration
        )
        docker-compose -f docker-compose.prod.yml up -d
    ) else (
        docker-compose -f docker-compose.dev.yml up -d
    )
    echo Services started successfully!
)

if "%ACTION%"=="stop" (
    echo Stopping CiliAI services...
    if "%ENV%"=="prod" (
        docker-compose -f docker-compose.prod.yml down
    ) else (
        docker-compose -f docker-compose.dev.yml down
    )
    echo Services stopped successfully!
)

if "%ACTION%"=="restart" (
    echo Restarting CiliAI services...
    if "%ENV%"=="prod" (
        docker-compose -f docker-compose.prod.yml restart
    ) else (
        docker-compose -f docker-compose.dev.yml restart
    )
    echo Services restarted successfully!
)

if "%ACTION%"=="logs" (
    echo Showing logs...
    if "%ENV%"=="prod" (
        docker-compose -f docker-compose.prod.yml logs -f
    ) else (
        docker-compose -f docker-compose.dev.yml logs -f
    )
)

echo.
echo ==========================================
echo Deployment completed!
echo ==========================================

endlocal
