import schedule
import time
import threading
import json
import subprocess
import sys
from scripts.uptime import check_uptime
from scripts.responsetime import check_response_time

# Ensure correct arguments
if len(sys.argv) != 4:
    print("Usage: python monitor.py <mysql_user> <mysql_password> <web_portal_url>")
    sys.exit(1)

MYSQL_USER = sys.argv[1]
MYSQL_PASSWORD = sys.argv[2]
WEB_PORTAL_URL = sys.argv[3]  # Web portal URL passed as an argument

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
        result = check_uptime(WEB_PORTAL_URL)
        print(f"✅ Uptime Check ({WEB_PORTAL_URL}): {result}")
        log_to_db("uptime", result)
    except Exception as e:
        print(f"❌ Uptime Check Failed: {e}")

def run_response_time_check():
    try:
        result = check_response_time(WEB_PORTAL_URL)
        print(f"✅ Response Time Check ({WEB_PORTAL_URL}): {result}")
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
