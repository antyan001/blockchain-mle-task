#!/usr/bin/env bash

# exit on failure
set -e

# apply migrations up to head
PYTHONPATH="/opt" DB_HOST=blockchain-task-db DB_PORT=5435 DB_NAME=blockchain-task \
DB_USERNAME=postgres DB_PASSWORD=password alembic upgrade head

# start Blockchain task server
python reporting_app.py
