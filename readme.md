create a venv with name cimf (required to be named cimf)
Start with requirements.txt then run init_db.py

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

**Commands to RUN**
python init_db.py your_mysql_username your_mysql_password
python monitor.py your_mysql_username your_mysql_password

**cleanup mininet**
sudo mn -c
sudo pkill -9 -f ovs-testcontroller
sudo ovs-testcontroller ptcp:6633 &
sudo ovs-testcontroller ptcp:6633 > /dev/null 2>&1 &


