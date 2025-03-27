import subprocess
import glob
import random
import string
import logging
import time
import os

# Set up logging
logging.basicConfig(filename='output.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
GIT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 5

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

def is_git_repository():
    try:
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], 
                      check=True, capture_output=True, timeout=GIT_TIMEOUT)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

def verify_git_config():
    try:
        # Check if user.name and user.email are configured
        subprocess.run(['git', 'config', 'user.name'], check=True, capture_output=True, timeout=GIT_TIMEOUT)
        subprocess.run(['git', 'config', 'user.email'], check=True, capture_output=True, timeout=GIT_TIMEOUT)
        return True
    except subprocess.CalledProcessError:
        logging.error("Git user.name or user.email is not configured")
        return False

def verify_remote_access():
    try:
        subprocess.run(['git', 'ls-remote', '--quiet'], check=True, capture_output=True, timeout=GIT_TIMEOUT)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to access remote repository: {e}")
        return False

def handle_merge_conflicts():
    try:
        # Check if there are merge conflicts
        status = subprocess.run(['git', 'status', '--porcelain'], 
                              check=True, capture_output=True, text=True, timeout=GIT_TIMEOUT)
        if 'UU' in status.stdout:  # UU indicates unmerged files
            logging.warning("Merge conflicts detected. Aborting rebase.")
            subprocess.run(['git', 'rebase', '--abort'], check=True, timeout=GIT_TIMEOUT)
            return False
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error handling merge conflicts: {e}")
        return False

def git_pull():
    try:
        if not is_git_repository():
            raise Exception("Not a git repository")
        
        if not verify_git_config():
            raise Exception("Git configuration is incomplete")
            
        if not verify_remote_access():
            raise Exception("Cannot access remote repository")

        # Get the current branch name
        branch_result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                    check=True, capture_output=True, text=True, timeout=GIT_TIMEOUT)
        current_branch = branch_result.stdout.strip()
        
        # Check if there are changes to stash
        status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                    check=True, capture_output=True, text=True, timeout=GIT_TIMEOUT)
        if status_result.stdout.strip():
            # Stash any uncommitted changes
            stash_result = subprocess.run(['git', 'stash', 'push', '-m', 'Auto-stash before pull'], 
                                       check=True, capture_output=True, text=True, timeout=GIT_TIMEOUT)
            logging.info(f"Stashed changes: {stash_result.stdout.strip()}")
            stash_applied = True
        else:
            logging.info("No changes to stash.")
            stash_applied = False

        # Run the git pull command with --rebase and specify the current branch
        result = subprocess.run(['git', 'pull', '--rebase', 'origin', current_branch], 
                              check=True, capture_output=True, text=True, timeout=GIT_TIMEOUT)
        logging.info(f"Successfully pulled the latest changes with rebase: {result.stdout.strip()}")

        # Check for merge conflicts after pull
        if not handle_merge_conflicts():
            raise Exception("Merge conflicts detected during pull")

        # Reapply the stashed changes if a stash was created
        if stash_applied:
            try:
                pop_result = subprocess.run(['git', 'stash', 'pop'], 
                                         check=True, capture_output=True, text=True, timeout=GIT_TIMEOUT)
                logging.info(f"Reapplied stashed changes: {pop_result.stdout.strip()}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to apply stashed changes: {e}")
                # Try to recover the stash
                subprocess.run(['git', 'stash', 'apply'], check=True, timeout=GIT_TIMEOUT)
                raise
    except subprocess.TimeoutExpired:
        logging.error("Git operation timed out")
        raise
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred during git pull or stash operations: {e}")
        logging.error(f"Command output: {e.stdout.strip()}")
        logging.error(f"Command error: {e.stderr.strip()}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during git pull: {e}")
        raise

def git_pull_with_retry(retries=MAX_RETRIES, delay=RETRY_DELAY):
    last_error = None
    for attempt in range(retries):
        try:
            git_pull()
            return  # Exit the function if git_pull succeeds
        except Exception as e:
            last_error = e
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.warning("All retry attempts failed. Continuing the process.")
    if last_error:
        raise last_error

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