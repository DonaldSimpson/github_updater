import subprocess
import glob
import random
import string
import logging
import time

# Set up logging
logging.basicConfig(filename='output.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_random_text(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation + ' ', k=length))

def update_files():
    try:
        files = glob.glob('update_files/file.*')
        num_files_to_update = random.randint(1, len(files))
        files_to_update = random.sample(files, num_files_to_update)
        
        for file in files_to_update:
            random_text_length = random.randint(1, 200)
            random_text = generate_random_text(random_text_length)
            with open(file, 'a') as f:
                f.write(f'\n# {random_text}\n')
        
        logging.info(f'Updated files: {files_to_update}')
        return files_to_update
    except Exception as e:
        logging.error(f'An error occurred while updating files: {e}')
        raise

def get_random_commit_message():
    try:
        with open('commit_messages.txt', 'r') as f:
            commit_messages = f.readlines()
        commit_message = random.choice(commit_messages).strip()
        logging.info(f'Commit message: {commit_message}')
        return commit_message
    except Exception as e:
        logging.error(f'An error occurred while getting commit message: {e}')
        raise

def git_pull():
    try:
        # Stash any uncommitted changes
        stash_result = subprocess.run(['git', 'stash', 'push', '-m', 'Auto-stash before pull'], check=True, capture_output=True, text=True)
        logging.info(f"Stashed changes: {stash_result.stdout.strip()}")

        # Run the git pull command with --rebase
        result = subprocess.run(['git', 'pull', '--rebase'], check=True, capture_output=True, text=True)
        logging.info(f"Successfully pulled the latest changes with rebase: {result.stdout.strip()}")

        # Reapply the stashed changes
        pop_result = subprocess.run(['git', 'stash', 'pop'], check=True, capture_output=True, text=True)
        logging.info(f"Reapplied stashed changes: {pop_result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred during git pull or stash operations: {e}")
        logging.error(f"Command output: {e.stdout.strip()}")
        logging.error(f"Command error: {e.stderr.strip()}")
        raise

def git_pull_with_retry(retries=3, delay=5):
    for attempt in range(retries):
        try:
            git_pull()
            return  # Exit the function if git_pull succeeds
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.warning("All retry attempts failed. Continuing the process.")

def git_commit_and_push(file_paths, commit_message):
    try:
        # Add the files to the staging area
        subprocess.run(['git', 'add'] + file_paths, check=True)
        
        # Commit the files with the provided commit message
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push the changes to the remote repository
        subprocess.run(['git', 'push'], check=True)
        
        logging.info("Files committed and pushed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f'An error occurred during git operations: {e}')
        raise

def ensure_clean_working_directory():
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], check=True, capture_output=True, text=True)
        if result.stdout.strip():
            logging.error("Working directory is not clean. Please commit or stash changes before pulling.")
            raise Exception("Working directory is not clean.")
        logging.info("Working directory is clean.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while checking the working directory: {e}")
        raise

def auto_commit_changes():
    try:
        # Check for uncommitted changes
        result = subprocess.run(['git', 'status', '--porcelain'], check=True, capture_output=True, text=True)
        if result.stdout.strip():
            # Stage all changes
            subprocess.run(['git', 'add', '.'], check=True)
            # Commit the changes
            subprocess.run(['git', 'commit', '-m', 'Auto-commit before pull'], check=True)
            logging.info("Automatically committed uncommitted changes.")
        else:
            logging.info("No uncommitted changes to commit.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred during auto-commit: {e}")
        raise

def clean_untracked_files():
    try:
        subprocess.run(['git', 'clean', '-fd'], check=True)
        logging.info("Removed untracked files.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while cleaning untracked files: {e}")
        raise

try:
    # Ensure the working directory is clean or auto-commit changes
    auto_commit_changes()

    # Pull the latest changes
    git_pull_with_retry()

    # Update the files
    updated_files = update_files()

    # Get a random commit message
    commit_message = get_random_commit_message()

    # Commit and push the changes
    git_commit_and_push(updated_files, commit_message)
except Exception as e:
    logging.error(f"An error occurred in the main process: {e}")