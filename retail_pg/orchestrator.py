'''
this file runs the project automatically. First the code calls the API caller, which download the data from the source, clean it, save to the database.
then the project calls the dbt project to run the models. The models use the fact and dimension tables saved from the previous step to create views. 
these views are useful for visualiation 
the file then classsify the starship models with ML
'''
import subprocess
import sys
import os
import logging

class DataPipeline:
    """manage the data pipeline"""

    def __init__(self):
        # enable logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def run_python_script(self, script_name):
        """Run a Python script"""
        logging.info(f"Running {script_name}...")
        try:
            logging.info(f"Running {script_name} in: {self.script_dir}")
            subprocess.run([sys.executable, script_name], check=True, cwd=self.script_dir)
            logging.info(f"{script_name} executed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running {script_name}: {e}")
            sys.exit(1) #
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            sys.exit(1)

    def run_dbt_models(self):
        """Run dbt models"""
        logging.info("Running dbt models...")
        try:
            logging.info(f"Running dbt in: {self.script_dir}")
            subprocess.run(["dbt", "run"], check=True, cwd=self.script_dir)
            logging.info("dbt models executed successfully. Multiple views are created for visualization.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running dbt models: {e}")
            sys.exit(1)
        except NotADirectoryError as e:
            logging.error(f"Invalid directory: {self.script_dir}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            sys.exit(1)

    def run_pipeline(self):
        """Run the entire pipeline"""
        try:
            #Download and store data
            self.run_python_script("APIcaller.py")

            #Run dbt models
            self.run_dbt_models()

            #Train the classifier
            self.run_python_script("Train_Classifier.py")

        except Exception as e:
            logging.error(f"Pipeline failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()