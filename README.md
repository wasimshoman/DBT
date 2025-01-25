# 🌟 Starships Data Pipeline Project (DBT) 🚀

![DBT](https://img.shields.io/badge/dbt-%23FF694B.svg?style=for-the-badge&logo=dbt&logoColor=white)
![Python](https://img.shields.io/badge/python-3.13-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)

A data pipeline that automates **Star Wars starships data** ingestion, transformation, and visualization using SWAPI, PostgreSQL, and DBT.

---


## 🚀 Project Overview

This project automates the extraction of Star Wars starships data from the **SWAPI API**, stores it in a PostgreSQL database, and transforms it into analytical models using **DBT**. The final output includes visualized insights for stakeholders.

### Key Components:
- **Orchestrator Script**: Combines data ingestion (`APIcaller.py`) and DBT transformation.
- **DBT Models**: SQL and Jinja transformations for creating tables/views.
- **Visualization**: Interactive dashboards or charts in the `evidence_visualization` folder.

---

## 🛠️ Features
- **Automated Data Ingestion**: Fetches data from SWAPI and loads it into PostgreSQL.
- **DBT Transformations**: Modular SQL models for business-ready analytics.
- **Visual Insights**: Pre-built visualizations for quick analysis.

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.13
- PostgreSQL (local or remote)
- [DBT CLI](https://docs.getdbt.com/dbt-cli/installation)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/wasimshoman/DBT.git
cd DBT
## 🛠️ Setup Instructions

### 2. Create PostgreSQL Database 🗄️
Run this SQL command in your PostgreSQL client (e.g., `psql`, pgAdmin, or DBeaver):
```sql
CREATE DATABASE test_db;

### 3. Configure Database Credentials  🗄️
Update the connection settings in APIcaller.py to match your PostgreSQL instance:
# 📁 APIcaller.py
DB_HOST = "your_host"      # e.g., "localhost" or "127.0.0.1"
DB_NAME = "test_db"        # Database name (keep as test_db)
DB_USER = "your_user"      # e.g., "postgres"
DB_PASS = "your_password"  # Your PostgreSQL password

### 3. Install Dependencies  🗄️
Install required Python packages using:
pip install -r requirements.txt
