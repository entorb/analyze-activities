#!/bin/bash

# ensure we are in the repo root dir
script_dir=$(dirname $0)
cd $script_dir/..

mkdir -p data
mkdir -p output

echo "## git_1_export_history"
src/git_1_export_history.sh

cp ../rememberthemilk/output/tasks_completed.csv data/rtm_tasks_completed.csv

for job in cal git_2_analyze oura strava rtm influx_1_download influx_2 lifelog join; do
    echo "## $job"
    python3 src/$job.py
done
