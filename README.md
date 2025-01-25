# 🌟 Starships Data Pipeline Project (DBT) 🚀

![DBT](https://img.shields.io/badge/dbt-%23FF694B.svg?style=for-the-badge&logo=dbt&logoColor=white)
![Python](https://img.shields.io/badge/python-3.13-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)

A data pipeline that automates **Star Wars starships data** ingestion, transformation, and visualization using SWAPI, PostgreSQL, and DBT.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Features](#-features)
- [Setup Instructions](#-setup-instructions)
- [Directory Structure](#-directory-structure)
- [Visualization](#-visualization)
- [License](#-license)

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
