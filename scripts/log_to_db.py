import mysql.connector
import sys
import json
from datetime import datetime

# Ensure correct arguments
if len(sys.argv) != 5:
    print("Usage: python log_to_db.py <mysql_user> <mysql_password> <check_name> <result_json>")
    sys.exit(1)

MYSQL_USER = sys.argv[1]
MYSQL_PASSWORD = sys.argv[2]
CHECK_NAME = sys.argv[3]
RESULT_JSON = sys.argv[4]

try:
    # Connect to MySQL using monitoring_db
    conn = mysql.connector.connect(
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host='localhost',
        database='monitoring_db',
        auth_plugin='mysql_native_password'
    )

    cursor = conn.cursor()

    # Extract timestamp and result data
    log_entry = json.loads(RESULT_JSON)
    timestamp = log_entry.get('timestamp')
    url = log_entry.get('url')

    # Insert into correct tables
    if CHECK_NAME == "uptime":
        query = "INSERT INTO uptime_logs (timestamp, url, status, code) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('status'), log_entry.get('status_code')))

    elif CHECK_NAME == "response_time":
        query = "INSERT INTO response_time_logs (timestamp, url, response_time, status, code) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('response_time_seconds'), log_entry.get('status'), log_entry.get('status_code')))

    elif CHECK_NAME == "dns_resolution":
        query = "INSERT INTO dns_resolution_logs (timestamp, url, domain, resolved_ip, status, connectivity) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('domain'), log_entry.get('resolved_ip'), log_entry.get('status'), log_entry.get('connectivity')))

    elif CHECK_NAME == "latency":
        query = "INSERT INTO latency_logs (timestamp, url, ip, avg_latency_ms, packet_loss_percent, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('ip'), log_entry.get('avg_latency_ms'), log_entry.get('packet_loss_percent'), log_entry.get('status')))

    elif CHECK_NAME == "performance":
        query = "INSERT INTO performance_logs (timestamp, url, total_time_seconds, ttfb_seconds, content_download_time_seconds, content_length_bytes, status_code, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('total_time_seconds'), log_entry.get('ttfb_seconds'), log_entry.get('content_download_time_seconds'), log_entry.get('content_length_bytes'), log_entry.get('status_code'), log_entry.get('status')))

    elif CHECK_NAME == "protocol":
        query = "INSERT INTO protocol_logs (timestamp, url, protocol, status_code, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('protocol'), log_entry.get('status_code'), log_entry.get('status')))

    elif CHECK_NAME == "ssl":
        query = "INSERT INTO ssl_logs (timestamp, url, ssl_valid, expiry_date, handshake_time_seconds, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('ssl_valid'), log_entry.get('expiry_date'), log_entry.get('handshake_time_seconds'), log_entry.get('status')))

    elif CHECK_NAME == "status_headers":
        query = "INSERT INTO status_headers_logs (timestamp, url, status_code, content_type, cache_control, x_request_id, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('status_code'), log_entry.get('content_type'), log_entry.get('cache_control'), log_entry.get('x_request_id'), log_entry.get('status')))

    elif CHECK_NAME == "errors":
        query = "INSERT INTO error_logs (timestamp, url, status_code, error_type, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, url, log_entry.get('status_code'), log_entry.get('error_type'), log_entry.get('status')))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Successfully logged {CHECK_NAME} to the database.")

except mysql.connector.Error as err:
    print(f"❌ Error logging to database: {err}")

except json.JSONDecodeError as e:
    print(f"❌ Error decoding JSON: {e}")
    print(f"❌ Received JSON: {RESULT_JSON}")

except KeyError as e:
    print(f"❌ Error: Missing key in JSON: {e}")
    print(f"❌ Received JSON: {RESULT_JSON}")

except Exception as e:
    print(f"❌ Error: {e}")