# Critical Infrastructure Monitoring Framework  

The **Critical Infrastructure Monitoring Framework (CIMF)** is designed to ensure the availability, reliability, and performance of essential enterprise services such as web portals, VPNs, firewalls, and service tools. It continuously monitors infrastructure health, detects failures, logs performance metrics, and triggers real-time alerts when predefined thresholds are breached.  

## 🚀 Features  
- **Automated Infrastructure Monitoring**: Tracks uptime, response time, network latency, DNS resolution, and packet loss.  
- **Real-time Alerts**: Sends notifications when critical issues are detected.  
- **Database Logging**: Stores monitoring results in a **MySQL database** for analysis.  
- **Scalable & Extensible**: Supports additional monitoring checks like SSL validation and service health checks.  

## 🛠️ Setup & Installation  

### 1️⃣ Create a Virtual Environment  
```sh
python -m venv cimf
```

### 2️⃣ Activate the Virtual Environment  
- **Windows (Command Prompt)**:  
  ```sh
  cimf\Scripts\activate
  ```

### 3️⃣ Install Dependencies  
```sh
pip install -r requirements.txt
```

### 4️⃣ Initialize the Database  
```sh
python init_db.py your_mysql_username your_mysql_password
```

### 5️⃣ Verify Database & Tables  
Navigate to MySQL binary folder:  
```sh
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
```
Login to MySQL:  
```sh
mysql -u root -p
```
Check if the database and tables were created successfully:  
```sql
SHOW DATABASES;
USE monitoring_db;
SHOW TABLES;
SELECT * FROM uptime_logs;
SELECT * FROM response_time_logs;
EXIT;
```

### 6️⃣ Start Monitoring a Website  
Run the monitoring script:  
```sh
python monitor.py website_url
```
