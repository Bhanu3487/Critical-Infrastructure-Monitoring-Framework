import mysql.connector
import json
import smtplib
import time
import sys
import os
from datetime import datetime, timedelta

if len(sys.argv) != 3:
    print("Usage: python alert_manager.py <mysql_user> <mysql_password>")
    sys.exit(1)

MYSQL_USER = sys.argv[1]
MYSQL_PASSWORD = sys.argv[2]

config_path = os.path.join(os.path.dirname(__file__), "alert_config.json")
try:
    with open(config_path) as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"❌ Error: {config_path} not found. Exiting.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"❌ Error: Invalid JSON in {config_path}. Exiting.")
    sys.exit(1)

# Configuration with warning and critical levels
MAX_DOWNTIME_WARNING = config.get("max_downtime_warning", 5)
MAX_DOWNTIME_CRITICAL = config.get("max_downtime_critical", 10)
MAX_RESPONSE_TIME_WARNING = config.get("max_response_time_warning", 300)
MAX_RESPONSE_TIME_CRITICAL = config.get("max_response_time_critical", 500)
MAX_LATENCY_MS_WARNING = config.get("max_latency_ms_warning", 75)
MAX_LATENCY_MS_CRITICAL = config.get("max_latency_ms_critical", 150)
MAX_PACKET_LOSS_PERCENT_WARNING = config.get("max_packet_loss_percent_warning", 15)
MAX_PACKET_LOSS_PERCENT_CRITICAL = config.get("max_packet_loss_percent_critical", 30)
MAX_HANDSHAKE_TIME_WARNING = config.get("max_handshake_time_seconds_warning", 1.0)
MAX_HANDSHAKE_TIME_CRITICAL = config.get("max_handshake_time_seconds_critical", 2.5)
MIN_SSL_EXPIRY_DAYS_WARNING = config.get("min_ssl_expiry_days_warning", 60)
MIN_SSL_EXPIRY_DAYS_CRITICAL = config.get("min_ssl_expiry_days_critical", 30)
EMAIL_TO = config.get("alert_email")
EMAIL_FROM = "cimf.cs331@gmail.com"
EMAIL_PASSWORD = "vnuy lqfy lpyv elor"

def send_email_alert(subject, message):
    if not EMAIL_TO:
        print(f"⚠️ Alert: {subject} - Email recipient not configured.")
        return
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            email_msg = f"Subject: {subject}\nContent-Type: text/plain; charset=utf-8\n\n{message}"
            server.sendmail(EMAIL_FROM, EMAIL_TO, email_msg.encode('utf-8'))
        print(f"📧 Email sent successfully to {EMAIL_TO}!")
    except Exception as e:
        print(f"❌ Email alert failed: {e}")

def get_last_checked_time(cursor):
    """Retrieves the last checked timestamp from the database."""
    cursor.execute("SELECT last_checked FROM last_processed WHERE id = 1")
    result = cursor.fetchone()
    return result[0] if result else datetime(1970, 1, 1)

def update_last_checked_time(cursor, conn):
    """Updates the last checked timestamp in the database."""
    cursor.execute("UPDATE last_processed SET last_checked = CURRENT_TIMESTAMP WHERE id = 1")
    conn.commit()

def check_alerts():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database="monitoring_db"
        )
        cursor = conn.cursor()

        last_checked = get_last_checked_time(cursor)

        # Check downtime incidents per URL
        def check_downtime_alerts(cursor, url):
            cursor.execute("SELECT COUNT(*) FROM uptime_logs WHERE url = %s AND status = 'DOWN' AND timestamp > %s", (url, last_checked))
            down_count = cursor.fetchone()[0]
            if down_count >= MAX_DOWNTIME_CRITICAL:
                send_email_alert(f"🔥 Critical Alert: Service Down for {url}", f"Service at {url} has been down {down_count} times since last check (Critical).")
            elif down_count >= MAX_DOWNTIME_WARNING:
                send_email_alert(f"⚠️ Warning: Service Down for {url}", f"Service at {url} has been down {down_count} times since last check (Warning).")

        cursor.execute("SELECT DISTINCT url FROM uptime_logs WHERE timestamp > %s AND status = 'DOWN'", (last_checked,))
        down_urls = [row[0] for row in cursor.fetchall()]
        for url in set(down_urls):
            check_downtime_alerts(cursor, url)

        # Check high response times per URL
        def check_response_time_alerts(cursor, url):
            cursor.execute("SELECT MAX(response_time) FROM response_time_logs WHERE url = %s AND timestamp > %s", (url, last_checked))
            max_response = cursor.fetchone()[0]
            if max_response is not None:
                if max_response > MAX_RESPONSE_TIME_CRITICAL:
                    send_email_alert(f"🔥 Critical Alert: High Response Time for {url}", f"Service at {url} response time exceeded {MAX_RESPONSE_TIME_CRITICAL} ms (Critical: {max_response} ms).")
                elif max_response > MAX_RESPONSE_TIME_WARNING:
                    send_email_alert(f"⚠️ Warning: High Response Time for {url}", f"Service at {url} response time exceeded {MAX_RESPONSE_TIME_WARNING} ms (Warning: {max_response} ms).")

        cursor.execute("SELECT DISTINCT url FROM response_time_logs WHERE timestamp > %s AND response_time > %s", (last_checked, MAX_RESPONSE_TIME_WARNING))
        response_urls = [row[0] for row in cursor.fetchall()]
        for url in set(response_urls):
            check_response_time_alerts(cursor, url)

        # Check high latency per URL
        def check_latency_alerts(cursor, url):
            cursor.execute("SELECT MAX(avg_latency_ms) FROM latency_logs WHERE url = %s AND timestamp > %s", (url, last_checked))
            max_latency = cursor.fetchone()[0]
            if max_latency is not None:
                if max_latency > MAX_LATENCY_MS_CRITICAL:
                    send_email_alert(f"🔥 Critical Alert: High Latency for {url}", f"Service at {url} latency exceeded {MAX_LATENCY_MS_CRITICAL} ms (Critical: {max_latency} ms).")
                elif max_latency > MAX_LATENCY_MS_WARNING:
                    send_email_alert(f"⚠️ Warning: High Latency for {url}", f"Service at {url} latency exceeded {MAX_LATENCY_MS_WARNING} ms (Warning: {max_latency} ms).")

        cursor.execute("SELECT DISTINCT url FROM latency_logs WHERE timestamp > %s AND avg_latency_ms > %s", (last_checked, MAX_LATENCY_MS_WARNING))
        latency_urls = [row[0] for row in cursor.fetchall()]
        for url in set(latency_urls):
            check_latency_alerts(cursor, url)

        # Check packet loss per URL
        def check_packet_loss_alerts(cursor, url):
            cursor.execute("SELECT MAX(packet_loss_percent) FROM latency_logs WHERE url = %s AND timestamp > %s", (url, last_checked))
            max_packet_loss = cursor.fetchone()[0]
            if max_packet_loss is not None:
                if max_packet_loss > MAX_PACKET_LOSS_PERCENT_CRITICAL:
                    send_email_alert(f"🔥 Critical Alert: High Packet Loss for {url}", f"Service at {url} packet loss exceeded {MAX_PACKET_LOSS_PERCENT_CRITICAL}% (Critical: {max_packet_loss}%).")
                elif max_packet_loss > MAX_PACKET_LOSS_PERCENT_WARNING:
                    send_email_alert(f"⚠️ Warning: High Packet Loss for {url}", f"Service at {url} packet loss exceeded {MAX_PACKET_LOSS_PERCENT_WARNING}% (Warning: {max_packet_loss}%).")

        cursor.execute("SELECT DISTINCT url FROM latency_logs WHERE timestamp > %s AND packet_loss_percent > %s", (last_checked, MAX_PACKET_LOSS_PERCENT_WARNING))
        packet_loss_urls = [row[0] for row in cursor.fetchall()]
        for url in set(packet_loss_urls):
            check_packet_loss_alerts(cursor, url)

        # Check high SSL handshake time per URL
        def check_handshake_alerts(cursor, url):
            cursor.execute("SELECT MAX(handshake_time_seconds) FROM ssl_logs WHERE url = %s AND timestamp > %s", (url, last_checked))
            max_handshake = cursor.fetchone()[0]
            if max_handshake is not None:
                if max_handshake > MAX_HANDSHAKE_TIME_CRITICAL:
                    send_email_alert(f"🔥 Critical Alert: High SSL Handshake Time for {url}", f"SSL handshake time for {url} exceeded {MAX_HANDSHAKE_TIME_CRITICAL} seconds (Critical: {max_handshake}s).")
                elif max_handshake > MAX_HANDSHAKE_TIME_WARNING:
                    send_email_alert(f"⚠️ Warning: High SSL Handshake Time for {url}", f"SSL handshake time for {url} exceeded {MAX_HANDSHAKE_TIME_WARNING} seconds (Warning: {max_handshake}s).")

        cursor.execute("SELECT DISTINCT url FROM ssl_logs WHERE timestamp > %s AND handshake_time_seconds > %s", (last_checked, MAX_HANDSHAKE_TIME_WARNING))
        handshake_urls = [row[0] for row in cursor.fetchall()]
        for url in set(handshake_urls):
            check_handshake_alerts(cursor, url)

        # Check SSL certificate expiry per URL
        cursor.execute("""
            SELECT url, expiry_date
            FROM ssl_logs
            WHERE expiry_date < %s AND expiry_date >= %s AND timestamp > %s
        """, (datetime.now() + timedelta(days=MIN_SSL_EXPIRY_DAYS_CRITICAL), datetime.now(), last_checked))
        for url, expiry_date in cursor.fetchall():
            send_email_alert(f"🔥 Critical Alert: SSL Certificate Expiry for {url}", f"SSL certificate for {url} expires on {expiry_date.strftime('%Y-%m-%d')} (Critical: within {MIN_SSL_EXPIRY_DAYS_CRITICAL} days).")

        cursor.execute("""
            SELECT url, expiry_date
            FROM ssl_logs
            WHERE expiry_date < %s AND expiry_date >= %s AND timestamp > %s
        """, (datetime.now() + timedelta(days=MIN_SSL_EXPIRY_DAYS_WARNING), datetime.now() + timedelta(days=MIN_SSL_EXPIRY_DAYS_CRITICAL), last_checked))
        for url, expiry_date in cursor.fetchall():
            send_email_alert(f"⚠️ Warning: SSL Certificate Expiry for {url}", f"SSL certificate for {url} expires on {expiry_date.strftime('%Y-%m-%d')} (Warning: within {MIN_SSL_EXPIRY_DAYS_WARNING} days).")

        # Check DNS resolution failure per URL
        cursor.execute("""
            SELECT url
            FROM dns_resolution_logs
            WHERE status = 'FAILURE' AND timestamp > %s
        """, (last_checked,))
        failed_dns_urls = [row[0] for row in cursor.fetchall()]
        for url in set(failed_dns_urls):
            send_email_alert(f"⚠️ Warning: DNS Resolution Failure for {url}", f"DNS resolution failed for {url} since last check.")

        update_last_checked_time(cursor, conn)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Error checking alerts: {err}")
        
if __name__ == "__main__":
    while True:
        check_alerts()
        time.sleep(60)  # Check every minute