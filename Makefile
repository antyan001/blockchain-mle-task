verify:
	isort --check-only .
	black --check --diff .
	python -m pytest tests
	python -m pytest integrationtests

fmt:
	isort -rc .
	black .

docker-build:
	docker build --rm --force-rm --tag deployment .

docker-compose-up: docker-build
	docker-compose -f $(shell pwd)/integrationtests/docker-compose.yaml up -d

docker-compose-down: 
	docker-compose -f $(shell pwd)/integrationtests/docker-compose.yaml down

alembic-upgrade:
	DB_HOST=localhost DB_PORT=5435 DB_NAME=blockchain-task \
	DB_USERNAME=postgres DB_PASSWORD=password \
	PYTHONPATH=. alembic upgrade head

alembic-downgrade:
	DB_HOST=localhost DB_PORT=5435 DB_NAME=blockchain-task \
	DB_USERNAME=postgres DB_PASSWORD=password \
	PYTHONPATH=. alembic downgrade -1

run-consumer:
	DB_HOST=localhost DB_PORT=5435 DB_NAME=blockchain-task \
	DB_USERNAME=postgres DB_PASSWORD=password \
	python blockchain_task/consumer.py

run-reporting-app:
	DB_HOST=localhost DB_PORT=5435 DB_NAME=blockchain-task \
	DB_USERNAME=postgres DB_PASSWORD=password \
	python blockchain_task/reporting_app.py

send-report:
	DB_HOST=localhost DB_PORT=5435 DB_NAME=blockchain-task \
	DB_USERNAME=postgres DB_PASSWORD=password \
	EMAIL_FROM=*** EMAIL_TO=*** \
	EMAIL_SERVER=*** EMAIL_PORT=*** \
	EMAIL_USER=*** EMAIL_PASSWORD=*** \
	python blockchain_task/reporting/deliverer.py
