# 🌟 Starships Data Pipeline Project (DBT) 🚀

![DBT](https://img.shields.io/badge/dbt-%23FF694B.svg?style=for-the-badge&logo=dbt&logoColor=white)
![Python](https://img.shields.io/badge/python-3.13-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)

A data pipeline that automates **Star Wars starships data** ingestion, transformation, and visualization using Python, SWAPI, SQL, PostgreSQL, and DBT.


## 🚀 Project Overview

This project automates the extraction of Star Wars starships data from the **SWAPI API**, stores it in a PostgreSQL database, and transforms it into analytical models using **DBT** and its SQL models. The final output includes visualized insights for stakeholders.

### Key Components:
- **Orchestrator Script**: Combines data ingestion (`APIcaller.py`), DBT transformation and Classifier.
- **DBT Models**: SQL models for creating tables/views.
- **Visualization**: Interactive dashboards or charts in the `evidence_visualization` folder.

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.13
- PostgreSQL 
- [DBT core]
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/wasimshoman/DBT.git
```

### 2. Create PostgreSQL Database 🗄️
Run this SQL command in your PostgreSQL client:
```sql
CREATE DATABASE test_db;
```

### 3. Configure Database Credentials 🔐
Update `APIcaller.py` with your PostgreSQL credentials:
```python
DB_HOST = "your_host"      # e.g., "localhost"
DB_NAME = "test_db"        # Database name
DB_USER = "your_user"      # e.g., "postgres"
DB_PASS = "your_password"  # Your PostgreSQL password
```

### 4. Install Dependencies 📦
Navigate to the DBT/retail_pg.

```bash
pip install -r requirements.txt
```
### 

Adjust project.yml file in your .dbt folder with the right information.

For better debugging, control of the DBT project, and visualization install the appropriate extensions from the VScode extension menu.


### 5. Run the Pipeline 🚀
```bash
python retail_pg/orchestrator.py
```

---

## 📂 Directory Structure
```
DBT/
├── retail_pg/
│   ├── orchestrator.py       # Pipeline orchestrator
│   ├── Train_Classifier.py       # group starship models according to k means
│   └── APIcaller.py          # SWAPI data fetcher
├   └── models/                   # DBT models (SQL + Jinja)
    ├── requirements.txt          # Python dependencies
├── evidence_visualization/   # Charts/dashboard
└── README.md
```

---

## 📊 Visualization
After running the pipeline:
1. Open the `evidence_visualization` folder in VS Code.
2. Click **Start Evidence** to explore results.


---

## 📜 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Happy Data Engineering!** 👾🚀
