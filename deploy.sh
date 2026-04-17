#!/bin/bash

set -e

echo "=========================================="
echo "CiliAI Docker Deployment Script"
echo "=========================================="

ENV=${1:-prod}
ACTION=${2:-start}

if [ "$ENV" != "prod" ] && [ "$ENV" != "dev" ]; then
    echo "Error: Environment must be 'prod' or 'dev'"
    exit 1
fi

if [ "$ACTION" != "start" ] && [ "$ACTION" != "stop" ] && [ "$ACTION" != "restart" ] && [ "$ACTION" != "logs" ]; then
    echo "Error: Action must be 'start', 'stop', 'restart', or 'logs'"
    exit 1
fi

echo "Environment: $ENV"
echo "Action: $ACTION"

case $ACTION in
    start)
        echo "Starting CiliAI services..."
        if [ "$ENV" = "prod" ]; then
            if [ ! -f .env ]; then
                echo "Warning: .env file not found. Copying from .env.prod.example..."
                cp .env.prod.example .env
                echo "Please edit .env file with your configuration"
            fi
            docker-compose -f docker-compose.prod.yml up -d
        else
            docker-compose -f docker-compose.dev.yml up -d
        fi
        echo "Services started successfully!"
        ;;
    stop)
        echo "Stopping CiliAI services..."
        if [ "$ENV" = "prod" ]; then
            docker-compose -f docker-compose.prod.yml down
        else
            docker-compose -f docker-compose.dev.yml down
        fi
        echo "Services stopped successfully!"
        ;;
    restart)
        echo "Restarting CiliAI services..."
        if [ "$ENV" = "prod" ]; then
            docker-compose -f docker-compose.prod.yml restart
        else
            docker-compose -f docker-compose.dev.yml restart
        fi
        echo "Services restarted successfully!"
        ;;
    logs)
        echo "Showing logs..."
        if [ "$ENV" = "prod" ]; then
            docker-compose -f docker-compose.prod.yml logs -f
        else
            docker-compose -f docker-compose.dev.yml logs -f
        fi
        ;;
esac

echo "=========================================="
echo "Deployment completed!"
echo "=========================================="
