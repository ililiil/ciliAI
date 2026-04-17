#!/bin/bash

set -e

echo "=========================================="
echo "CiliAI Docker Environment Setup"
echo "=========================================="

ENV=${1:-prod}

if [ "$ENV" = "prod" ]; then
    echo "Setting up production environment..."

    if [ ! -f .env ]; then
        echo "Creating .env from template..."
        cp .env.prod.example .env
        echo "Please edit .env file with your configuration:"
        echo "  - MYSQL_ROOT_PASSWORD"
        echo "  - MYSQL_PASSWORD"
        echo "  - VOLC_AK (Volcano Engine Access Key)"
        echo "  - VOLC_SK (Volcano Engine Secret Key)"
        echo ""
        read -p "Press Enter to continue after editing .env..."
    fi

    echo "Building Docker images..."
    docker-compose -f docker-compose.prod.yml build

    echo "Starting services..."
    docker-compose -f docker-compose.prod.yml up -d

    echo "Checking service health..."
    sleep 10
    docker-compose -f docker-compose.prod.yml ps

elif [ "$ENV" = "dev" ]; then
    echo "Setting up development environment..."

    if [ ! -f .env.dev ]; then
        echo "Creating .env.dev from template..."
        cp .env.dev.example .env.dev
        echo "Please edit .env.dev file with your configuration"
        echo ""
        read -p "Press Enter to continue after editing .env.dev..."
    fi

    echo "Building Docker images..."
    docker-compose -f docker-compose.dev.yml build

    echo "Starting services..."
    docker-compose -f docker-compose.dev.yml up -d

    echo "Checking service health..."
    sleep 10
    docker-compose -f docker-compose.dev.yml ps

else
    echo "Error: Environment must be 'prod' or 'dev'"
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup completed!"
echo ""
echo "Service URLs:"
if [ "$ENV" = "prod" ]; then
    echo "  - Backend API: http://localhost:5001"
    echo "  - Frontend: http://localhost:3003"
    echo "  - Admin: http://localhost:3002"
else
    echo "  - Backend API: http://localhost:5001"
    echo "  - Frontend: http://localhost:3003"
    echo "  - Admin: http://localhost:3002"
fi
echo ""
echo "To view logs: ./deploy.sh $ENV logs"
echo "To stop services: ./deploy.sh $ENV stop"
echo "=========================================="
