#!/usr/bin/env bash
# Install Apache Airflow for the optional step (Linux, macOS or a Codespace; needs Python 3.11-3.14).
# Airflow is installed with its official constraints file, which pins compatible versions
# of its many dependencies.
set -euo pipefail
AIRFLOW_VERSION=3.3.2
PY=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
case "$PY" in
  3.11|3.12|3.13|3.14) ;;
  *) echo "Airflow $AIRFLOW_VERSION needs Python 3.11-3.14, but you have $PY. Use the Airflow Codespace instead."; exit 1 ;;
esac
pip install "apache-airflow==${AIRFLOW_VERSION}" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PY}.txt"
echo "Airflow ${AIRFLOW_VERSION} installed. Try: ./orchestration/airflow.sh dags test home_value_pipeline"
