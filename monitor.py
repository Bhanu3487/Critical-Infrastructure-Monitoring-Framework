import schedule
import time
import threading
import json
import sys
from datetime import datetime
from scripts.uptime import check_uptime
from scripts.response_time import check_response_time
from scripts.latency import check_latency
from scripts.dns_check import check_dns
from scripts.performance import check_performance
from scripts.protocol import check_protocol
from scripts.ssl_check import check_ssl
from scripts.status_check import check_status_and_headers, check_errors

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
        result = check_latency(WEB_PORTAL_URL)
        print(f"✅ Latency Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("latency", result)
    except Exception as e:
        print(f"❌ Latency Check Failed: {e}")

def run_dns_resolution():
    try:
        result = check_dns(WEB_PORTAL_URL)
        print(f"✅ DNS Resolution Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("dns_resolution", result)
    except Exception as e:
        print(f"❌ DNS Resolution Check Failed: {e}")

def run_performance_check():
    try:
        result = check_performance(WEB_PORTAL_URL)
        print(f"✅ Performance Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("performance", result)
    except Exception as e:
        print(f"❌ Performance Check Failed: {e}")

def run_protocol_check():
    try:
        result = check_protocol(WEB_PORTAL_URL)
        print(f"✅ Protocol Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("protocol", result)
    except Exception as e:
        print(f"❌ Protocol Check Failed: {e}")

def run_ssl_check():
    try:
        result = check_ssl(WEB_PORTAL_URL)
        print(f"✅ SSL Check ({WEB_PORTAL_URL}): {result}")
        log_to_file("ssl", result)
    except Exception as e:
        print(f"❌ SSL Check Failed: {e}")

def run_status_check_and_errors():
    try:
        status_result = check_status_and_headers(WEB_PORTAL_URL)
        print(f"✅ Status and Headers Check ({WEB_PORTAL_URL}): {status_result}")
        log_to_file("status_headers", status_result)
        error_result = check_errors(WEB_PORTAL_URL)
        print(f"✅ Error Check ({WEB_PORTAL_URL}): {error_result}")
        log_to_file("errors", error_result)
    except Exception as e:
        print(f"❌ Status and Error Check Failed: {e}")

# Run DNS resolution check only once before starting the scheduler
run_dns_resolution()

# Schedule tasks
# schedule.every(5).seconds.do(run_uptime_check)
# schedule.every(10).seconds.do(run_response_time_check)
# schedule.every(15).seconds.do(run_latency_check)
# schedule.every(20).seconds.do(run_performance_check)
# schedule.every(30).seconds.do(run_protocol_check)
# schedule.every(60).seconds.do(run_ssl_check)
# schedule.every(30).seconds.do(run_status_check_and_errors)

schedule.every(30).seconds.do(run_uptime_check)       # Less frequent for general availability
schedule.every(15).seconds.do(run_response_time_check) # Keep an eye on performance
schedule.every(20).seconds.do(run_latency_check)       # Network performance
schedule.every(60).seconds.do(run_performance_check)   # Detailed performance less critical for every check
schedule.every(1).hour.do(run_protocol_check)         # Protocol changes are rare
schedule.every(1).hour.do(run_ssl_check)              # SSL expiry is a longer-term issue
schedule.every(30).seconds.do(run_status_check_and_errors) # Important for functional issues

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    scheduler_thread.join()  # Keeps the script running indefinitely