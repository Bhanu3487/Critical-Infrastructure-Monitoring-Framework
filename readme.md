# Critical Infrastructure Monitoring Framework  

The **Critical Infrastructure Monitoring Framework (CIMF)** is designed to ensure the availability, reliability, and performance of essential enterprise services such as web portals, VPNs, firewalls, and service tools. It continuously monitors infrastructure health, detects failures, logs performance metrics, and triggers real-time alerts when predefined thresholds are breached.  

## 🚀 Features  
✅ **Automated Infrastructure Monitoring**: Tracks uptime, response time, network latency, DNS resolution, and packet loss.  
✅ **Real-time Alerts**: Sends notifications when critical issues are detected.  
✅ **Database Logging**: Stores monitoring results in a MySQL database for analysis.  
✅ **Scalable & Extensible**: Supports additional monitoring checks like SSL validation and service health checks.  

## 🛠️ Setup & Installation  

### 1️⃣ Create a Virtual Environment  
```bash
python -m venv cimf
```  

### 2️⃣ Activate the Virtual Environment  
#### Windows (Command Prompt):  
```bash
cimf\Scripts\activate
```  

### 3️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```  

### 4️⃣ Initialize the Database  
```bash
python init_db.py your_mysql_username your_mysql_password
```  

### 5️⃣ Verify Database & Tables  
Navigate to the MySQL binary folder:  
```bash
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
```  
Login to MySQL:  
```bash
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

### 6️⃣ Start Monitoring  
Run the monitoring script for a specific website:  
```bash
python monitor.py website_url
```  

### 7️⃣ Log Monitoring Results to Database  
```bash
python run_log_to_db.py
```  

### 8️⃣ Start Alert Manager for Real-Time Alerts  
```bash
cd alerts
python alert_manager.py your_mysql_username your_mysql_password
```  
