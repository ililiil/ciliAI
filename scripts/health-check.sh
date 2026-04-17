#!/bin/bash

set -e

echo "=========================================="
echo "CiliAI Docker Health Check"
echo "=========================================="

ENV=${1:-prod}

if [ "$ENV" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
else
    COMPOSE_FILE="docker-compose.dev.yml"
fi

echo "Checking services for environment: $ENV"
echo ""

check_service() {
    local service=$1
    local port=$2
    local name=$3

    echo -n "Checking $name... "

    if docker ps --filter "name=${service}" --filter "status=running" | grep -q "$service"; then
        if timeout 5 bash -c "curl -f http://localhost:$port/health" 2>/dev/null; then
            echo "✓ Healthy"
            return 0
        else
            echo "⚠ Running but not responding"
            return 1
        fi
    else
        echo "✗ Not running"
        return 1
    fi
}

echo ""
echo "Container Status:"
docker-compose -f $COMPOSE_FILE ps

echo ""
echo "Service Health:"
check_service "ciliai-mysql" "3306" "MySQL"
check_service "ciliai-backend" "5001" "Backend API"
check_service "ciliai-frontend" "3003" "Frontend"
check_service "ciliai-admin" "3002" "Admin"

echo ""
echo "=========================================="
echo "Health check completed!"
echo "=========================================="
