#!/bin/bash
# shellcheck disable=SC2164
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
python "$parent_path"/src/timesheet_calculator_ui.py