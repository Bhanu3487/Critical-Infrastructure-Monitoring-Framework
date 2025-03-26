import schedule
import time
import threading
import json
import subprocess
import sys
from datetime import datetime
from scripts.uptime import check_uptime
from scripts.responsetime import check_response_time
from scripts.latency_check import check_latency_packet_loss
from scripts.DNS_resolution_check import check_dns_resolution

# Ensure correct arguments
if len(sys.argv) != 2:
    print("Usage: python monitor.py <web_portal_url>")
    sys.exit(1)

WEB_PORTAL_URL = sys.argv[1]  # Web portal URL passed as an argument
LOG_FILE = "logs/monitor.log"

def log_to_file(check_name, result):
    """Logs monitoring results to a file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "check": check_name,
        "result": result
    }
    try:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"❌ Error writing to log file: {e}")

def run_uptime_check():
    try:
        result = check_uptime(WEB_PORTAL_URL)
        print(f"✅ Uptime Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("uptime", result)
    except Exception as e:
        print(f"❌ Uptime Check Failed: {e}")

def run_response_time_check():
    try:
        result = check_response_time(WEB_PORTAL_URL)
        print(f"✅ Response Time Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("response_time", result)
    except Exception as e:
        print(f"❌ Response Time Check Failed: {e}")

def run_latency_check():
    try:
        result = check_latency_packet_loss(WEB_PORTAL_URL)
        print(f"✅ Latency Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("latency", result)
    except Exception as e:
        print(f"❌ Latency Check Failed: {e}")

def run_dns_resolution():
    try:
        result = check_dns_resolution(WEB_PORTAL_URL)
        print(f"✅ DNS Resolution Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("DNS Resolution", result)
    except Exception as e:
        print(f"❌ DNS Resolution Check Failed: {e}")

# Run DNS resolution check only once before starting the scheduler
run_dns_resolution()

# Schedule tasks
schedule.every(1).seconds.do(run_uptime_check)
schedule.every(1).seconds.do(run_latency_check)
schedule.every(2).seconds.do(run_response_time_check)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    scheduler_thread.join()  # Keeps the script running indefinitely

