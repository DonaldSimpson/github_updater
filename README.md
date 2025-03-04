# GitHub Updater

## Purpose

I heard recently that some people (recruiters, interviewers) judge developers by their github commit/activity graph. Yes; that is clearly very dumb. I migrated from GitHub to my own personal self-hosted git service when Microsoft bought GitHub (timing not a coincidence), and only use GitHub rarely - or more commonly for work - these days. But, this observation got me pondering how I could automate a busy github commit graph, just for the heck of it, and ended up here.

The GitHub Updater project automates updating files in a repository, committing the changes, and pushing them to GitHub.

The project includes scripts that will run a random number of times per day, each time making random updates to files and committing those changes with randomly selected commit messages.

This is done via cron job which runs the `schedule_commit.py` at midnight every day. This script creates a number of sceduled `at` tasks that runs the `commit_file.py` script which will make updates and commit them to github throughout the day.

Updated files & file types are in update_files - to add a new type just create a file.<ext> in there whith whatever extension you want and it will be updated (randomly).

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
    Ensure you **update the path** to the files in the `schedule_commit.py` file too.

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