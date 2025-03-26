import mysql.connector
import json
import smtplib
import time
import sys
from datetime import datetime, timedelta
import os

if len(sys.argv) != 3:
    print("Usage: python alert_manager.py <mysql_user> <mysql_password>")
    sys.exit(1)

MYSQL_USER = sys.argv[1]
MYSQL_PASSWORD = sys.argv[2]

config_path = os.path.join(os.path.dirname(__file__), "alert_config.json")
with open(config_path) as f:
    config = json.load(f)

MAX_DOWNTIME = config["max_downtime"]
MAX_RESPONSE_TIME = config["max_response_time"]
MAX_LATENCY_MS = config["max_latency_ms"]
MAX_PACKET_LOSS_PERCENT = config["max_packet_loss_percent"]
EMAIL_TO = config["alert_email"]
EMAIL_FROM = "cimf.cs331@gmail.com"
EMAIL_PASSWORD = "vnuy lqfy lpyv elor"

def send_email_alert(subject, message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            email_msg = f"Subject: {subject}\nContent-Type: text/plain; charset=utf-8\n\n{message}"
            server.sendmail(EMAIL_FROM, EMAIL_TO, email_msg.encode('utf-8'))
        print("\U0001F4E7 Email sent successfully!")
    except Exception as e:
        print(f"\u274C Email alert failed: {e}")

def check_alerts():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database="monitoring_db"
        )
        cursor = conn.cursor()

        # Get the last processed timestamp
        cursor.execute("SELECT last_checked FROM last_processed WHERE id = 1")
        last_checked = cursor.fetchone()[0]

        # Check downtime incidents
        cursor.execute("SELECT COUNT(*) FROM uptime_logs WHERE status = 'DOWN' AND timestamp > %s", (last_checked,))
        down_count = cursor.fetchone()[0]
        if down_count >= MAX_DOWNTIME:
            send_email_alert("\U0001F6A8 Alert: Service Down", f"Service has been down {down_count} times since last check.")

        # Check high response times
        cursor.execute("SELECT COUNT(*) FROM response_time_logs WHERE response_time > %s AND timestamp > %s", (MAX_RESPONSE_TIME, last_checked))
        high_response_count = cursor.fetchone()[0]
        if high_response_count > 0:
            send_email_alert("\u23F3 Alert: High Response Time", f"Service response time exceeded {MAX_RESPONSE_TIME} ms {high_response_count} times since last check.")

        # Check high latency
        cursor.execute("SELECT COUNT(*) FROM latency_logs WHERE avg_latency_ms > %s AND timestamp > %s", (MAX_LATENCY_MS, last_checked))
        high_latency_count = cursor.fetchone()[0]
        if high_latency_count > 0:
            send_email_alert("\U0001F4A1 Alert: High Latency", f"Service latency exceeded {MAX_LATENCY_MS} ms {high_latency_count} times since last check.")

        # Check packet loss
        cursor.execute("SELECT COUNT(*) FROM latency_logs WHERE packet_loss_percent > %s AND timestamp > %s", (MAX_PACKET_LOSS_PERCENT, last_checked))
        high_packet_loss_count = cursor.fetchone()[0]
        if high_packet_loss_count > 0:
            send_email_alert("\U0001F4A1 Alert: High Packet Loss", f"Service packet loss exceeded {MAX_PACKET_LOSS_PERCENT}% {high_packet_loss_count} times since last check.")

        # Check DNS resolution failure
        cursor.execute("SELECT COUNT(*) FROM dns_resolution_logs WHERE status = 'FAILURE' AND timestamp > %s", (last_checked,))
        dns_failure_count = cursor.fetchone()[0]
        if dns_failure_count > 0:
            send_email_alert("\U0001F4A1 Alert: DNS Resolution Failure", f"DNS resolution failed {dns_failure_count} times since last check.")

        # Update last processed timestamp
        cursor.execute("UPDATE last_processed SET last_checked = CURRENT_TIMESTAMP WHERE id = 1")
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"\u274C Error checking alerts: {err}")

if __name__ == "__main__":
    while True:
        check_alerts()
        time.sleep(60)  # Check every minute
