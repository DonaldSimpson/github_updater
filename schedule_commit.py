import random
import subprocess
from datetime import datetime, timedelta
import logging
import os
import sys

# Set up logging
logging.basicConfig(
    filename='output.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def schedule_commit_script():
    try:
        logging.info("schedule_commit.py script started.")

        # Log the Python executable being used
        logging.debug(f"Python executable: {sys.executable}")

        # Log the current working directory
        cwd = os.getcwd()
        logging.debug(f"Current working directory: {cwd}")

        # Set the PATH explicitly
        os.environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
        logging.debug(f"Updated PATH: {os.environ.get('PATH')}")

        # Log the current environment variables
        logging.debug(f"Environment variables: {os.environ}")

        # Determine the number of times to run the script today
        num_runs = random.randint(0, 35)
        logging.debug(f'Number of runs scheduled for today: {num_runs}')
        
        # Get the current time
        now = datetime.now()
        logging.debug(f'Current time: {now}')
        
        # Calculate the time intervals for running the script
        intervals = sorted([now + timedelta(seconds=random.randint(0, 86400)) for _ in range(num_runs)])
        logging.debug(f'Scheduled intervals: {intervals}')
        
        # Schedule the script to run at the calculated times
        for run_time in intervals:
            run_time_str = run_time.strftime('%H:%M')
            # Construct the command to schedule with `at`
            command = (
                f'echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; '
                f'/usr/bin/python3 /home/don/workspaces/github_updater/commit_file.py '
                f'>> /home/don/workspaces/github_updater/commit_output.log 2>&1" | at {run_time_str}'
            )
            logging.debug(f'Scheduling command: {command}')
            
            # Execute the command
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Log the result
            if result.returncode == 0:
                logging.info(f'Successfully scheduled commit_file.py to run at {run_time_str}')
                logging.debug(f'Command output: {result.stdout.strip()}')
            else:
                logging.error(f'Failed to schedule commit_file.py at {run_time_str}')
                logging.error(f'Command output: {result.stdout.strip()}')
                logging.error(f'Command error: {result.stderr.strip()}')
    except Exception as e:
        logging.error(f'An error occurred: {e}', exc_info=True)

if __name__ == "__main__":
    schedule_commit_script()
