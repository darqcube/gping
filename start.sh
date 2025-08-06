#!/bin/bash

# Wait for any required services (if any)
echo "Starting Globalping Traceroute Application..."

# Check if we're in a container
if [ -f /.dockerenv ]; then
    echo "Running in Docker container"
fi

# Set Python to run in unbuffered mode
export PYTHONUNBUFFERED=1

# Start the Flask application
echo "Starting Flask application on port 5001..."
exec python -m flask run --host=0.0.0.0 --port=5001 