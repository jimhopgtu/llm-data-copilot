#!/bin/bash
# Initialize database if it doesn't exist
if [ ! -f /app/data/sample.db ]; then
    echo "Database not found, initializing..."
    cd /app/data && python init_db.py
fi

# Start the server
exec uvicorn app:app --host 0.0.0.0 --port 8000
