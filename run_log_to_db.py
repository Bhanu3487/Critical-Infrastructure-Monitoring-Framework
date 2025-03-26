import subprocess
import json
import sys

# Ensure correct usage
if len(sys.argv) != 3:
    print("Usage: python process_logs.py <MYSQL_USER> <MYSQL_PASSWORD>")
    sys.exit(1)

MYSQL_USER = sys.argv[1]
MYSQL_PASSWORD = sys.argv[2]

LOG_FILE = 'logs/monitor.log'
LOG_TO_DB_SCRIPT = 'scripts/log_to_db.py'

# Read log file
with open(LOG_FILE, 'r') as file:
    logs = file.readlines()

# Process each log entry
for log in logs:
    try:
        log_entry = json.loads(log)
        check_name = log_entry.get('check')

        # Add timestamp to result JSON
        log_entry['result']['timestamp'] = log_entry.get('timestamp')

        # Convert result to JSON string (compact format)
        result_json = json.dumps(log_entry['result'], separators=(',', ':'))

        # Run the log_to_db.py script for each entry
        subprocess.run([
            'python', LOG_TO_DB_SCRIPT, MYSQL_USER, MYSQL_PASSWORD, check_name, result_json
        ], check=True)

    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Invalid log entry: {log.strip()} - Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to log {check_name} data to the database: {e}")

print("✅ All logs processed.")

