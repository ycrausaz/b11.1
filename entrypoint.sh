#!/bin/bash
set -e

# Function to check if the database is ready
function check_db() {
    until pg_isready -h database_default -U postgres -d db; do
        echo "Waiting for database to be ready..."
        sleep 2
    done
}

# Wait for the database to be ready
check_db

# Regenerate version.txt at runtime
if [ ! -f /app/b11_1/version.txt ]; then
    mkdir -p /app/b11_1
    echo "v$(date +%Y%m%d)" > /app/b11_1/version.txt
    echo "Generated version file: $(cat /app/b11_1/version.txt)"
fi

# Execute the original command passed to the container
exec "$@"

