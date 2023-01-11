# Blockchain MLE take-home challenge

This repository contains the solution to the take-home challenge.

Key features:
* Consuming events from Kafka stream
* Exposing reporting API using flask
* Sending user count report every 100th user
* Docker compose is used to spin up separate services for running the reporting API, the database and Kafka consumer

Set-up instructions:
* Create virtual environment: `python -m venv venv`
* Activate newly created environment: `source venv/bin/activate`
* Install dependencies: `pip install -r requirements.txt`
* Install package locally: `pip install -e .`
* Build docker image and spin up containers: `make docker-compose-up`
* Run database migrations to create all tables: `make alembic-upgrade` (database will be running on port 5435)
* Run verifications to check that everything is running fine (including unit and integration tests): `make verify`
* Replace `***` with actual credentials if using `send-report` to send the report to an email address.