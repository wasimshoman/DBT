#this file runs the project automatically. First the code calls the API caller, which download the data from the source, clean it, save to the database.
# then the project calls the dbt project to run the models. The models use the fact and dimension tables saved from the previous step to create views. 
#these views are useful for visualiation 
import subprocess
import sys
import os

def run_python_script():
    #Run the Python script to download and store data.
    print("Running APIcaller.py to download and store data...")
    try:
        # change directory to the python script directory (retail_pg)
        script_dir = os.path.dirname(os.path.abspath(__file__))  
        print(f"Running APIcaller.py in: {script_dir}")
        subprocess.run([sys.executable, "APIcaller.py"], check=True, cwd=script_dir)
        print("First step is completed. Data download and storage finished.")
    except subprocess.CalledProcessError as e:
        print(f"Error running APIcaller.py: {e}")
        sys.exit(1)

def run_dbt_models():
    #Run dbt models.
    print("Running dbt models...")
    try:
        # change directory to retail_pg
        script_dir = os.path.dirname(os.path.abspath(__file__))  
        print(f"Running dbt in: {script_dir}")
        subprocess.run(["dbt", "run"], check=True, cwd=script_dir)
        print("dbt models executed successfully. Multiple views are created for visualization.")
    except subprocess.CalledProcessError as e:
        print(f"Error running dbt models: {e}")
        sys.exit(1)
    except NotADirectoryError as e:
        print(f"Invalid directory: {script_dir}")
        sys.exit(1)

def main():
    # Step 1: download and store data
    run_python_script()

    # Step 2: run dbt models
    run_dbt_models()

if __name__ == "__main__":
    main()