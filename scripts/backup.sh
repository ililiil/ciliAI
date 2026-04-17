#!/bin/bash

set -e

set -e

echo "=========================================="
echo "CiliAI Database Backup Script"
echo "=========================================="

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/ciliai_backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

echo "Creating database backup..."
echo "Backup file: $BACKUP_FILE"

docker exec ciliai-mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} ciliai > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "Backup created successfully!"
    echo "File size: $(du -h $BACKUP_FILE | cut -f1)"
else
    echo "Error: Backup failed!"
    exit 1
fi

echo ""
echo "Backing up uploaded files..."
tar -czf "$BACKUP_DIR/uploads_$TIMESTAMP.tar.gz" ./ciliAI/uploads 2>/dev/null || true

echo ""
echo "Listing recent backups:"
ls -lh $BACKUP_DIR | tail -5

echo ""
echo "=========================================="
echo "Backup completed!"
echo "=========================================="
