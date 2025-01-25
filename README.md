# DBT
Starships Data Pipeline Project for Knowit

This project automates downloading data about Star Wars starships from the SWAPI API, storing it in a Postgre database, and using DBT to transform the raw data into useful visualized insights through tables, views, and models. 

It consists of:
An orchestrator script (orchestrator.py) that combines two steps:
Step 1: A script (APIcaller.py) for downloading and processing data.
Step 2: A DBT project for transforming and modeling the data into views.

 The project also includes a visualization folder (evidence_visualization) that visualizes the results. The visualization can be open from VScode. 

Setup Instructions
1. Prerequisites
Python 3.13 installed
PostgreSQL database running locally or remotely
DBT CLI installed (see DBT installation guide)
Git installed

Clone the Repository

git clone https://github.com/wasimshoman/DBT.git
cd DBT

Create a PostgreSQL database:
SQL
CREATE DATABASE test_db;
