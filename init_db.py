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

    # Table for latency logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS latency_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        url VARCHAR(255),
        ip VARCHAR(45),
        avg_latency_ms FLOAT,
        packet_loss_percent INT,
        status VARCHAR(20)
    )
    """)

    # Table for DNS resolution logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dns_resolution_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        url VARCHAR(255),
        domain VARCHAR(255),
        resolved_ip VARCHAR(45),
        status VARCHAR(20)
    )
    """)

    # Table for tracking last processed timestamp
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS last_processed (
        id INT PRIMARY KEY DEFAULT 1,
        last_checked DATETIME(6) DEFAULT '1970-01-01 00:00:00.000000' ON UPDATE CURRENT_TIMESTAMP(6)
    )
    """)


    # Initialize the last processed timestamp if not exists
    cursor.execute("INSERT IGNORE INTO last_processed (id) VALUES (1)")

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
