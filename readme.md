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

## ⚙️ Implementation Details

At present, our **Critical Infrastructure Monitoring Framework** operates in multiple phases, where each component runs independently in sequence. The process follows these steps:

#### Step 1: Start Monitoring  
The monitoring script is executed for a specific website, collecting key metrics such as **uptime, response time, latency, and DNS resolution**.

```bash
python monitor.py website_url
```
- This script performs periodic checks and logs the results into a file (`logs/monitor.log`).
- Log entries are stored in **JSON format**, containing timestamps, status codes, and response times.

#### Step 2: Log Monitoring Results to Database  
After monitoring, the logged data is processed and stored in the **MySQL database** using:

```bash
python run_log_to_db.py
```
- The script reads `monitor.log`, parses each entry, and calls `log_to_db.py` to insert the data into structured database tables.
- Key metrics such as **latency, uptime, and response time** are stored for analysis.

#### Step 3: Start Alert Manager for Real-Time Alerts  
To detect critical failures and notify administrators, the **Alert Manager** is executed:

```bash
cd alerts  
python alert_manager.py <mysql_user> <mysql_password>
```
- This script continuously queries the database for **abnormal conditions** (e.g., downtime, high packet loss).
- If an issue is detected, it **triggers alerts** via email.



