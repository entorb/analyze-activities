#!/bin/bash

# ensure we are in the repo root dir
script_dir=$(dirname $0)
cd $script_dir/..

echo "## git_1_export_history"
src/git_1_export_history.sh

for job in cal git_2_analyze oura strava join; do
    echo "## $job"
    python3 src/$job.py
done
