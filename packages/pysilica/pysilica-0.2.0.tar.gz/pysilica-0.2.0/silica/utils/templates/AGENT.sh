#!/usr/bin/env bash
# Get the directory where this script is located
TOP=$(cd $(dirname $0) && pwd)
APP_NAME=$(basename $TOP)

# NOTE: piku-specific
# source environment variables
set -a
source $HOME/.piku/envs/${APP_NAME}/ENV  # could be LIVE_ENV?

# Synchronize dependencies
cd "${TOP}"
uv sync

# Change to the code directory and start the agent
cd "${TOP}/code"
echo "Starting the agent from $(pwd) at $(date)"
uv run hdev --dwr || echo "Agent exited with status $? at $(date)"

# If the agent exits, keep the shell open for debugging in tmux
echo "Agent process has ended. Keeping tmux session alive."