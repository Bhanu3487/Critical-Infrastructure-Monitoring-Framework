Start with requirements.txt then run init_db.py

**Commands to RUN**
python init_db.py your_mysql_username your_mysql_password

python log_to_db.py your_mysql_username your_mysql_password uptime '{"status": "UP", "code": 200}'

python monitor.py your_mysql_username your_mysql_password

**MySQL setup**
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
mysql -u root -p
enter password

SHOW DATABASES;
USE monitoring_db;
SHOW TABLES;
SELECT * FROM uptime_logs;
SELECT * FROM response_time_logs;
EXIT;


- Windows CMD:
python log_to_db.py root your_password uptime "{\"status\": \"UP\", \"code\": 200}"
- PowerShell:
python log_to_db.py root your_password uptime '{\"status\": \"UP\", \"code\": 200}'
- Git Bash/Linux/macOS:
python log_to_db.py root your_password uptime '{"status": "UP"

To implement a hybrid alert system, we need to:
Write logs for real-time alerts.
Store structured data in a database for analysis & dashboard.
Check the database periodically to trigger alerts.