import random
from datetime import datetime, timedelta
import logging
import os

# Set up logging
logging.basicConfig(filename='output.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def schedule_commit_script():
    try:
        logging.info("schedule_commit.py script started.")

        # Log the current environment variables
        logging.debug(f"Environment variables: {os.environ}")

        # Determine the number of times to run the script today (between 1 and 5)
        num_runs = random.randint(1, 5)
        logging.debug(f'Number of runs scheduled for today: {num_runs}')
        
        # Get the current time
        now = datetime.now()
        logging.debug(f'Current time: {now}')
        
        # Calculate the time intervals for running the script
        intervals = sorted([now + timedelta(seconds=random.randint(0, 86400)) for _ in range(num_runs)])
        logging.debug(f'Scheduled intervals: {intervals}')
        
        # Log the intended schedule
        for run_time in intervals:
            logging.info(f"Intended schedule: commit_file.py to run at {run_time.strftime('%H:%M:%S')}")
    except Exception as e:
        logging.error(f'An error occurred: {e}')

if __name__ == "__main__":
    schedule_commit_script()