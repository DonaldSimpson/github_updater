import random
import subprocess
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(filename='output.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def schedule_commit_script():
    try:
        # Determine the number of times to run the script today (between 1 and 5)
        num_runs = random.randint(1, 5)
        
        # Get the current time
        now = datetime.now()
        
        # Calculate the time intervals for running the script
        intervals = sorted([now + timedelta(seconds=random.randint(0, 86400)) for _ in range(num_runs)])
        
        # Schedule the script to run at the calculated times
        for run_time in intervals:
            run_time_str = run_time.strftime('%H:%M')
            command = f'echo "/usr/bin/python3 /home/don/workspaces/github_updater/commit_file.py" | at {run_time_str}'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            logging.info(f'Scheduled commit_file.py to run at {run_time_str}')
            logging.info(f'Command output: {result.stdout}')
            logging.error(f'Command error: {result.stderr}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')

if __name__ == "__main__":
    schedule_commit_script()