import mysql.connector
import json
import smtplib
import time
import sys
from datetime import datetime, timedelta

# Ensure correct arguments
if len(sys.argv) != 3:
    print("Usage: python alert_monitor.py <mysql_user> <mysql_password>")
    sys.exit(1)

MYSQL_USER = sys.argv[1]
MYSQL_PASSWORD = sys.argv[2]

# Load alert settings
with open("alert_config.json") as f:
    config = json.load(f)

MAX_DOWNTIME = config["max_downtime"]
EMAIL_TO = config["alert_email"]
EMAIL_FROM = "yourmonitor@example.com"
EMAIL_PASSWORD = "your_email_password"

def send_email_alert(subject, message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            email_msg = f"Subject: {subject}\n\n{message}"
            server.sendmail(EMAIL_FROM, EMAIL_TO, email_msg)
    except Exception as e:
        print(f"❌ Email alert failed: {e}")

def check_alerts():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database="monitoring_db"
        )
        cursor = conn.cursor()

        # Check downtime incidents
        time_limit = datetime.now() - timedelta(minutes=MAX_DOWNTIME)
        cursor.execute("SELECT COUNT(*) FROM uptime_logs WHERE status = 'DOWN' AND timestamp > %s", (time_limit,))
        down_count = cursor.fetchone()[0]

        if down_count >= MAX_DOWNTIME:
            send_email_alert("🚨 Alert: Service Down", f"Service has been down {down_count} times in the last {MAX_DOWNTIME} minutes.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Error checking alerts: {err}")

if __name__ == "__main__":
    while True:
        check_alerts()
        time.sleep(60)  # Check every minute
