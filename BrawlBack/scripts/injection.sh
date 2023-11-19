#!/bin/bash

app_path="$(dirname "$pwd")"

db_injection="$app_path/auto/db_injection.py"

mkdir -p "$app_path/logs"

log_file="$app_path/logs/injection.log"

original_pythonpath="$PYTHONPATH"

export PYTHONPATH="$app_path:$PYTHONPATH"

python3.11 "$db_injection" 2>> $log_file &