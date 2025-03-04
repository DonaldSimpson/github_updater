import subprocess
import glob
import random
import string
import logging

# Set up logging
logging.basicConfig(filename='output.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_random_text(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation + ' ', k=length))

def update_files():
    try:
        files = glob.glob('file.*')
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

try:
    # Update the files
    updated_files = update_files()

    # Get a random commit message
    commit_message = get_random_commit_message()

    # Commit and push the changes
    git_commit_and_push(updated_files, commit_message)
except Exception as e:
    logging.error(f'An error occurred in the main process: {e}')