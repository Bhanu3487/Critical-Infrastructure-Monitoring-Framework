#!/bin/bash

LOG_FILE="logs/monitor.log"
PYTHON_ENV="cimf/bin/activate"  # Change this if your venv path is different
MONITOR_SCRIPT="monitor.py"

# Function to rotate logs (if log file > 5MB, archive it)
rotate_logs() {
    if [[ -f "$LOG_FILE" && $(stat -c%s "$LOG_FILE") -gt 5242880 ]]; then
        mv "$LOG_FILE" "logs/monitor_$(date +'%Y%m%d%H%M%S').log"
        echo "$(date): Log rotated" > "$LOG_FILE"
    fi
}

# Function to start monitoring
start_monitoring() {
    echo "$(date): Starting monitoring framework..." >> "$LOG_FILE"
    
    # Activate virtual environment if it exists
    if [[ -f "$PYTHON_ENV" ]]; then
        source "$PYTHON_ENV"
    fi

    # Run monitor.py in a loop (auto-restart on crash)
    while true; do
        python3 "$MONITOR_SCRIPT" >> "$LOG_FILE" 2>&1
        echo "$(date): monitor.py crashed! Restarting..." >> "$LOG_FILE"
        sleep 2  # Wait before restarting
    done
}

# Check if monitor.py is already running
if pgrep -f "$MONITOR_SCRIPT" > /dev/null; then
    echo "monitor.py is already running. Exiting..."
    exit 1
fi

# Rotate logs before starting
rotate_logs

# Start monitoring
start_monitoring
