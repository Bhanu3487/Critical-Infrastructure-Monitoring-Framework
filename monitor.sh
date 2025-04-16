#!/bin/bash

# --- Configuration ---
MYSQL_USER="root"
MYSQL_PASSWORD="root"
MONITOR_URL="https://sports-management-portal.onrender.com"
SCRIPT_DIR="$PWD"
LOG_DIR="$SCRIPT_DIR/logs"
ALERTS_DIR="$SCRIPT_DIR/alerts"
MONITOR_LOG_FILE="$LOG_DIR/monitor.log"
PYTHON_ENV="cimf/bin/activate"
MONITOR_SCRIPT="monitor.py"
LOG_ROTATE_SIZE=5242880

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# --- Functions ---

rotate_logs() {
    if [[ -f "$MONITOR_LOG_FILE" && $(stat -c%s "$MONITOR_LOG_FILE") -gt "$LOG_ROTATE_SIZE" ]]; then
        mv "$MONITOR_LOG_FILE" "$LOG_DIR/monitor_$(date +'%Y%m%d%H%M%S').log"
        echo "$(date): Monitor log rotated" > "$MONITOR_LOG_FILE"
    fi
}

run_monitor() {
    echo "$(date): Starting/Restarting monitoring of $MONITOR_URL..."
    if [[ -f "$PYTHON_ENV" ]]; then
        source "$PYTHON_ENV"
    fi
    python3 "$SCRIPT_DIR/$MONITOR_SCRIPT" "$MONITOR_URL"
    echo "$(date): monitor.py crashed! Will be restarted by the main loop."
}

run_log_to_db() {
    echo "$(date): Running run_log_to_db.py..."
    if [[ -f "$PYTHON_ENV" ]]; then
        source "$PYTHON_ENV"
    fi
    python3 "$SCRIPT_DIR/run_log_to_db.py" "$MYSQL_USER" "$MYSQL_PASSWORD"
    echo "$(date): run_log_to_db.py finished."
}

run_alert_manager() {
    echo "$(date): Starting alert_manager.py in the background..."
    if [[ -f "$PYTHON_ENV" ]]; then
        source "$PYTHON_ENV"
    fi
    cd "$ALERTS_DIR" && python3 alert_manager.py "$MYSQL_USER" "$MYSQL_PASSWORD" >> "$LOG_DIR/alert_manager.log" 2>&1 &
    echo "$(date): alert_manager.py started in the background."
}

run_init_db() {
  echo "--- Running init_db.py ---"
  python3 "$SCRIPT_DIR/init_db.py" "$MYSQL_USER" "$MYSQL_PASSWORD"
  echo "--- init_db.py finished ---"
}

# --- Main Execution ---

echo "$(date): Starting the full monitoring automation..."

# Initialize the database (run only once or as needed)
run_init_db

# Start the alert manager in the background (run once)
run_alert_manager

# Run the monitoring and log to database in a loop
while true; do
    rotate_logs # Rotate monitor logs before each run

    # Run monitor with auto-restart on crash
    run_monitor

    echo "$(date): Waiting for monitor to run for a while..."
    sleep 30 # Wait for 1/2 minute (adjust as needed)

    run_log_to_db
    sleep 60 # Wait for 1 minute before the next log to DB run

    echo "$(date): Sleeping before the next full cycle..."
    sleep 30 # Wait for 1/2 minute before the next full cycle
done

echo "$(date): Monitoring automation stopped."