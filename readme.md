# Critical Infrastructure Monitoring Framework (CIMF)

A lightweight Python-based framework to monitor critical infrastructure websites for uptime, status logging, and alert management.

## 🔧 Prerequisites

- Python 3.8+
- MySQL Server installed and running  
- Ensure MySQL binaries are added to PATH or navigate to the bin directory to use the `mysql` command

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Bhanu3487/Critical-Infrastructure-Monitoring-Framework.git
cd Critical-Infrastructure-Monitoring-Framework
```

### 2. Set Up Virtual Environment

```bash
python -m venv cimf
```

Activate the virtual environment:

- **Windows**:
  ```bash
  cimf\Scripts\activate
  ```

- **WSL/Linux/macOS**:
  ```bash
  source cimf/bin/activate
  ```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ MySQL Setup

In a separate terminal:

```bash
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
mysql -u root -p
```

Inside the MySQL prompt, ensure your user has access or create a new database if needed.

---

### 4. Initialize Database

```bash
python init_db.py your_mysql_username your_mysql_password
```

---

## 🌐 Start Monitoring

```bash
python monitor.py website_url
```

Example:

```bash
python monitor.py https://ims.iitgn.ac.in
```

---

## 🗃️ Log Monitoring Results to Database

```bash
python run_log_to_db.py your_mysql_username your_mysql_password
```

---

## 🚨 Alerts Management

```bash
cd alerts
python alert_manager.py your_mysql_username your_mysql_password
```

---

## 📌 Notes

- Replace all placeholder values like `your_mysql_username` and `website_url` with your actual values.
- The system logs uptime results and manages alerts based on configured thresholds and downtimes.
