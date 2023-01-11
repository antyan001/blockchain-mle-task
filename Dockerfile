FROM python:3.8-slim-buster as deployment

COPY blockchain_task/ /opt/blockchain_task
COPY alembic_migrations /opt/alembic_migrations/

COPY alembic.ini /opt/
COPY entrypoint.sh /opt/
COPY requirements.txt /opt/
COPY README.md /opt/
COPY setup.py /opt/

WORKDIR /opt

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt
RUN pip install --user .

USER nobody
EXPOSE 2800

ENTRYPOINT ["./entrypoint.sh"]