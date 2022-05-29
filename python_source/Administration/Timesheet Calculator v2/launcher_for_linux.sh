#!/bin/bash
# shellcheck disable=SC2164
printf "Starting Timesheet Calculator..."
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
{
  python "$parent_path"/Timesheet\ Calculator\ v2/main.py
  } || {
    python3.6 "$parent_path"/Timesheet\ Calculator\ v2/main.py
}