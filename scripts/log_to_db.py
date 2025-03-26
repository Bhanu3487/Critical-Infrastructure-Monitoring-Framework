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
    timestamp = log_entry['timestamp']
    
    # Insert into correct tables
    if CHECK_NAME == "uptime":
        query = "INSERT INTO uptime_logs (timestamp, status, code) VALUES (%s, %s, %s)"
        cursor.execute(query, (timestamp, log_entry['status'], log_entry['code']))

    elif CHECK_NAME == "response_time":
        query = "INSERT INTO response_time_logs (timestamp, status, response_time) VALUES (%s, %s, %s)"
        cursor.execute(query, (timestamp, log_entry['status'], log_entry['response_time']))

    elif CHECK_NAME == "DNS Resolution":
        query = "INSERT INTO dns_resolution_logs (timestamp, url, domain, resolved_ip, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, log_entry['url'], log_entry['domain'], log_entry['resolved_ip'], log_entry['status']))

    elif CHECK_NAME == "latency":
        query = "INSERT INTO latency_logs (timestamp, url, ip, avg_latency_ms, packet_loss_percent, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (timestamp, log_entry['url'], log_entry['ip'], log_entry['avg_latency_ms'], log_entry['packet_loss_percent'], log_entry['status']))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Successfully logged {CHECK_NAME} to the database.")

except mysql.connector.Error as err:
    print(f"❌ Error logging to database: {err}")

except Exception as e:
    print(f"❌ Error: {e}")
