#!/bin/bash
set -e

# Regenerate version.txt at runtime
if [ ! -f /app/b11_1/version.txt ]; then
    mkdir -p /app/b11_1
    echo "v$(date +%Y%m%d)" > /app/b11_1/version.txt
    echo "Generated version file: $(cat /app/b11_1/version.txt)"
fi

# Execute the original command passed to the container
exec "$@"
