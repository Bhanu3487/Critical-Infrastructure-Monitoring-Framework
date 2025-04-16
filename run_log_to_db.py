import subprocess
import json
import sys
import mysql.connector
from datetime import datetime

# Ensure correct usage
if len(sys.argv) != 3:
    print("Usage: python run_log_to_db.py <MYSQL_USER> <MYSQL_PASSWORD>")
    sys.exit(1)

MYSQL_USER = sys.argv[1]
MYSQL_PASSWORD = sys.argv[2]

LOG_FILE = 'logs/monitor.log'
LOG_TO_DB_SCRIPT = 'scripts/log_to_db.py'

def get_last_processed_time(user, password):
    """Retrieves the last processed timestamp from the database."""
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database='monitoring_db',
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT last_checked FROM last_processed WHERE id = 1")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return datetime(1970, 1, 1)  # Default if no record
    except mysql.connector.Error as err:
        print(f"❌ Error retrieving last processed time: {err}")
        return datetime(1970, 1, 1)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def update_last_processed_time(user, password, timestamp):
    """Updates the last processed timestamp in the database."""
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database='monitoring_db',
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE last_processed SET last_checked = %s WHERE id = 1", (timestamp,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"❌ Error updating last processed time: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    last_processed = get_last_processed_time(MYSQL_USER, MYSQL_PASSWORD)
    processed_count = 0
    latest_log_time = last_processed  # Initialize with the last processed time

    try:
        with open(LOG_FILE, 'r') as file:
            for log in file:
                try:
                    log_entry = json.loads(log)
                    timestamp_str = log_entry.get('timestamp')
                    if timestamp_str:
                        log_time = datetime.fromisoformat(timestamp_str)
                        if log_time > last_processed:
                            check_name = log_entry.get('check')
                            result_json = json.dumps(log_entry['result'], separators=(',', ':'))

                            subprocess.run([
                                sys.executable, LOG_TO_DB_SCRIPT, MYSQL_USER, MYSQL_PASSWORD, check_name, result_json
                            ], check=True)
                            processed_count += 1
                            latest_log_time = max(latest_log_time, log_time)
                    else:
                        print(f"⚠️ Skipping log entry due to missing timestamp: {log.strip()}")

                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON log entry: {log.strip()} - Error: {e}")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to log data to the database: {e}")
                except Exception as e:
                    print(f"❌ An unexpected error occurred while processing log entry: {log.strip()} - Error: {e}")

    except FileNotFoundError:
        print(f"❌ Error: Log file '{LOG_FILE}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading log file '{LOG_FILE}': {e}")
        sys.exit(1)

    if processed_count > 0:
        update_last_processed_time(MYSQL_USER, MYSQL_PASSWORD, latest_log_time)
        print(f"✅ Processed {processed_count} new log entries.")
    else:
        print("✅ No new log entries to process.")