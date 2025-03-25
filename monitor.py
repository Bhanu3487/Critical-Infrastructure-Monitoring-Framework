import schedule
import time
import threading
import json
import subprocess
import sys
from scripts.uptime import check_uptime
from scripts.responsetime import check_response_time

# Ensure correct arguments
if len(sys.argv) != 3:
    print("Usage: python monitor.py <mysql_user> <mysql_password>")
    sys.exit(1)

MYSQL_USER = sys.argv[1]
MYSQL_PASSWORD = sys.argv[2]
URL = "https://iitgn.ac.in/"  # This can be read from a config file

def log_to_db(check_name, result):
    """Logs monitoring results using log_to_db.py"""
    result_json = json.dumps(result)
    try:
        subprocess.run(
            ["cimf/Scripts/python", "scripts/log_to_db.py", MYSQL_USER, MYSQL_PASSWORD, check_name, result_json],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing log_to_db.py: {e}")

def run_uptime_check():
    try:
        result = check_uptime(URL)
        print(f"✅ Uptime Check: {result}")
        log_to_db("uptime", result)
    except Exception as e:
        print(f"❌ Uptime Check Failed: {e}")

def run_response_time_check():
    try:
        result = check_response_time(URL)
        print(f"✅ Response Time Check: {result}")
        log_to_db("response_time", result)
    except Exception as e:
        print(f"❌ Response Time Check Failed: {e}")

# Schedule tasks
schedule.every(1).seconds.do(run_uptime_check)
schedule.every(2).seconds.do(run_response_time_check)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    scheduler_thread.join()  # Keeps the script running indefinitely
