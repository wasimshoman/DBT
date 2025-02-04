'''
Created: 2025-01-26
this file runs the project automatically. This is an executor for the project 
parts in the intended order. First the code calls the API caller, which download 
the data from the source, clean it, save to the database.
then the project calls the dbt project to run the models. 
The models use the fact and dimension tables saved 
from the previous step to create views, which are useful for visualization.  
There is also an OBT, which I used to populate the missing data using some
mathematical operations. I also use this table to classify the starship 
models into three clusters which can be small, medium, and large ships 
using an ML algorithm.
'''
import subprocess
import sys
import os
import logging


class DataPipeline:
    #Manage the data pipeline

    def __init__(self):
        # Set the script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def run_python_script(self, script_name):
        #Python script
        logging.info(f"Running {script_name}...")
        try:
            print(f"Running {script_name} in: {self.script_dir}")
            subprocess.run([sys.executable, script_name], check=True, cwd=self.script_dir)
            logging.info(f"{script_name} executed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running {script_name}: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            sys.exit(1)

    def run_dbt_models(self):
        #Run dbt models
        logging.info("Running dbt models...")
        try:
            logging.info(f"Running dbt in: {self.script_dir}")
            subprocess.run(["dbt", "run"], check=True, cwd=self.script_dir)
            logging.info("dbt models executed successfully")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running dbt models: {e}")
            sys.exit(1)
        except NotADirectoryError:
            logging.error(f"Invalid directory: {self.script_dir}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            sys.exit(1)

    def run_pipeline(self):
        # Run the entire pipeline
        try:
            # Download and store data
            self.run_python_script("APIcaller.py")

            # Run dbt models
            self.run_dbt_models()

            # Train the classifier (K means)
            self.run_python_script("Train_Classifier.py")

        except Exception as e:
            logging.error(f"Pipeline failed: {e}")
            sys.exit(1)
            
if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()
