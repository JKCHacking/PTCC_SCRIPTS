#!/bin/bash
# shellcheck disable=SC2164
printf "Starting LDAP Exporter..."
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
python "$parent_path"/main.py