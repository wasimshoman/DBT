"""
created: 2025 26 01
this file runs the project automatically. First the code calls the API caller, which download the data from the source, clean it, save to the database.
then the project calls the dbt project to run the models. The models use the fact and dimension tables saved from the previous step to create views. 
these views are useful for visualiation 
the file then classsify the starship models with ML
"""
import subprocess
import sys
import os

class DataPipeline:
    #Manage the data pipeline.

    def __init__(self):
        # Set the script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def run_python_script(self, script_name):
        #Run a Python script.
        print(f"Running {script_name}...")
        try:
            print(f"Running {script_name} in: {self.script_dir}")
            subprocess.run([sys.executable, script_name], check=True, cwd=self.script_dir)
            print(f"{script_name} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

    def run_dbt_models(self):
        #Run dbt models.
        print("Running dbt models...")
        try:
            print(f"Running dbt in: {self.script_dir}")
            subprocess.run(["dbt", "run"], check=True, cwd=self.script_dir)
            print("dbt models executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running dbt models: {e}")
            sys.exit(1)
        except NotADirectoryError as e:
            print(f"Invalid directory: {self.script_dir}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

    def run_pipeline(self):
        #Run the entire pipeline.
        try:
            #Download and store data
            self.run_python_script("APIcaller.py")

            #Run dbt models
            self.run_dbt_models()

             #Train the classifier
            self.run_python_script("Train_Classifier.py")

        except Exception as e:
            print(f"Pipeline failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()