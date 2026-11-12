#!/usr/bin/env bash
# Run Airflow with this repository's settings (Linux, macOS or a Codespace).
#   ./orchestration/airflow.sh dags test home_value_pipeline   # run the DAG once, in the terminal
#   ./orchestration/airflow.sh standalone                      # start the web UI on port 8080
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export AIRFLOW_HOME="$ROOT/.airflow"                       # Airflow's database and logs (git-ignored)
export AIRFLOW__CORE__DAGS_FOLDER="$ROOT/orchestration/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False                  # show only our DAG
export AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=False    # ready to trigger straight away
export AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_ALL_ADMINS=True  # no login screen (local teaching setup only)
airflow db migrate > /dev/null                             # create or update Airflow's database (safe to repeat)
exec airflow "$@"
