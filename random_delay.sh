#!/bin/bash
sleep $((RANDOM % 3600))  # Sleep for a random time between 0 and 3600 seconds (1 hour)
/usr/bin/python3 /home/don/workspaces/github_updater/commit_file.py
