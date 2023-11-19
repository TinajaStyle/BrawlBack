#!/bin/bash

app_path="$(dirname "$pwd")"

python_file=("$app_path/test/test_app.py" \
             "$app_path/test/test_player.py" \
             "$app_path/test/test_track.py" \
             "$app_path/test/test_ws.py")

original_pythonpath="$PYTHONPATH"

export PYTHONPATH="$app_path:$PYTHONPATH"

pytest "${python_file[@]}"   
