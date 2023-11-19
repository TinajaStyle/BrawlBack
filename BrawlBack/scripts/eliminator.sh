#!/bin/bash

app_path=""

cd "$app_path"

virtualenv_path=""

source "$virtualenv_path"

battle_eliminator="$app_path/auto/battle_eliminator.py"

mkdir -p "$app_path/logs"

log_file="$app_path/logs/eliminator.log"

original_pythonpath="$PYTHONPATH"

export PYTHONPATH="$app_path:$PYTHONPATH"

python3.11 "$battle_eliminator" 2>> "$log_file"