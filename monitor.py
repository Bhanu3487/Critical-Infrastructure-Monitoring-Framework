import schedule
import time
import threading
import json
from scripts.uptime import check_uptime
from scripts.responsetime import check_response_time

URL = "https://www.google.com/"

# Function to log results
def log_result(check_name, result):
    with open("logs/monitor.log", "a") as f:
        f.write(f"{time.ctime()} - {check_name}: {json.dumps(result)}\n")

# Scheduled tasks
def run_uptime_check():
    result = check_uptime(URL)
#    print(f"Uptime Check Result: {result}")  # Debug print
    log_result("uptime", result)

def run_response_time_check():
    result = check_response_time(URL)
    log_result("response_time", result)

# Define scheduling intervals
schedule.every(1).seconds.do(run_uptime_check)
schedule.every(2).seconds.do(run_response_time_check)

# Background thread to run scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the monitoring framework
if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Keep the main script running
    while True:
        time.sleep(10)
