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
        url VARCHAR(255),
        status VARCHAR(10),
        code INT
    )
    """)

    # Table for response time logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS response_time_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        url VARCHAR(255),
        response_time FLOAT,
        status VARCHAR(10),
        code INT
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
        packet_loss_percent FLOAT,
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
        status VARCHAR(20),
        connectivity VARCHAR(20)
    )
    """)

    # Table for performance logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS performance_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        url VARCHAR(255),
        total_time_seconds FLOAT,
        ttfb_seconds FLOAT,
        content_download_time_seconds FLOAT,
        content_length_bytes INT,
        status_code INT,
        status VARCHAR(10)
    )
    """)

    # Table for protocol logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS protocol_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        url VARCHAR(255),
        protocol VARCHAR(10),
        status_code INT,
        status VARCHAR(10)
    )
    """)

    # Table for SSL logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ssl_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        url VARCHAR(255),
        ssl_valid BOOLEAN,
        expiry_date DATETIME,
        handshake_time_seconds FLOAT,
        status VARCHAR(20)
    )
    """)

    # Table for status and headers logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS status_headers_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        url VARCHAR(255),
        status_code INT,
        content_type VARCHAR(255),
        cache_control VARCHAR(255),
        x_request_id VARCHAR(255),
        status VARCHAR(10)
    )
    """)

    # Table for error logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS error_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        url VARCHAR(255),
        status_code INT,
        error_type VARCHAR(20),
        status VARCHAR(10)
    )
    """)

    # Table for tracking last processed timestamp (keeping this)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS last_processed (
        id INT PRIMARY KEY DEFAULT 1,
        last_checked DATETIME(6) DEFAULT '1970-01-01 00:00:00.000000' ON UPDATE CURRENT_TIMESTAMP(6)
    )
    """)

    # Initialize the last processed timestamp if not exists (keeping this)
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