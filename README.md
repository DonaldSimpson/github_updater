# GitHub Updater

## Purpose

The GitHub Updater project is designed to automate the process of updating files in a repository, committing the changes, and pushing them to GitHub. The project includes scripts that can run a random number of times per day, making random updates to files and committing those changes with randomly selected commit messages.

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/DonaldSimpson/github_updater.git
    cd github_updater
    ```

2. **Set Up Python Environment**:
    Ensure you have Python installed. You can create a virtual environment if desired:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**:
    There are no external dependencies for this project, but ensure you have `git` and `at` installed on your system.

4. **Set Up Cron Job**:
    Open your `crontab` file:
    ```sh
    crontab -e
    ```
    Add the following line to schedule the `schedule_commit.py` script to run once a day at midnight:
    ```sh
    0 0 * * * /usr/bin/python3 /`<yourinstallpath>`/schedule_commit.py
    ```

## Features

### `commit_file.py`

- **Purpose**: This script updates a random number of files matching the pattern `file.*` by appending random text to them. It then commits and pushes these changes to the GitHub repository.
- **Functions**:
  - `generate_random_text(length)`: Generates a random string of the specified length.
  - `update_files()`: Updates a random number of `file.*` files with random text.
  - `get_random_commit_message()`: Selects a random commit message from `commit_messages.txt`.
  - `git_commit_and_push(file_paths, commit_message)`: Commits and pushes the changes to the GitHub repository.
- **Logging**: Logs activities and errors to `output.log`.

### `schedule_commit.py`

- **Purpose**: This script schedules the `commit_file.py` script to run a random number of times per day (between 1 and 5 times) at random intervals.
- **Functions**:
  - `schedule_commit_script()`: Determines the number of times to run the script and schedules it using the `at` command.
- **Logging**: Logs scheduling activities and errors to `output.log`.

### `commit_messages.txt`

- **Purpose**: Contains a list of typical commit messages. The `commit_file.py` script randomly selects a commit message from this file for each commit.
- **Content**: 20 example commit messages.

## Usage

1. Ensure the `cron` job is set up to run `schedule_commit.py` daily.
2. The `schedule_commit.py` script will schedule the `commit_file.py` script to run a random number of times each day.
3. Check `output.log` for logs of the script's activities and any errors.

## License

This project is licensed under the MIT License.