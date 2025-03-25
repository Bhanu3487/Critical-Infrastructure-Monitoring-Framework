import mysql.connector
import sys
import json

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
        database='monitoring_db',  # ✅ Correct database name
        auth_plugin='mysql_native_password'  # ✅ Fix authentication issue
    )
    
    cursor = conn.cursor()
    
    # Insert into correct tables
    result_data = json.loads(RESULT_JSON)

    if CHECK_NAME == "uptime":
        query = "INSERT INTO uptime_logs (timestamp, status, code) VALUES (NOW(), %s, %s)"
        cursor.execute(query, (result_data['status'], result_data['code']))

    elif CHECK_NAME == "response_time":
        query = "INSERT INTO response_time_logs (timestamp, status, response_time) VALUES (NOW(), %s, %s)"
        cursor.execute(query, (result_data['status'], result_data['response_time']))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Successfully logged {CHECK_NAME} to the database.")

except mysql.connector.Error as err:
    print(f"❌ Error logging to database: {err}")
