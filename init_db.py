import mysql.connector
import sys

def create_database(user, password):
    """Creates the database if it doesn't exist."""
    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS monitoring_db")
    conn.close()

def create_tables(user, password):
    """Creates the tables if they do not exist."""
    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="monitoring_db"
    )
    cursor = conn.cursor()

    # Table for uptime logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uptime_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(10),
        code INT
    )
    """)

    # Table for response time logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS response_time_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(10),
        response_time FLOAT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python init_db.py <mysql_user> <mysql_password>")
        sys.exit(1)

    mysql_user = sys.argv[1]
    mysql_password = sys.argv[2]

    create_database(mysql_user, mysql_password)
    create_tables(mysql_user, mysql_password)
    print("Database and tables initialized successfully.")
