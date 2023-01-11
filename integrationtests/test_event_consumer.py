from typing import Dict
import json
import threading
import time

from kafka import KafkaProducer
import helpers
import pytest
import timeout_decorator

from blockchain_task.db_engine import DbEngine
from blockchain_task.event_consumer import EventConsumer

USER_RAW = {
    "id": "278ab326-2b6a-4b4d-aa9b-64caaf074bb3",
    "address": {
        "city": "Bloomfield",
        "state": "US-IN",
        "country": "US",
        "postCode": "47424",
    },
}

USER_INSERTED = {
    "id": "278ab326-2b6a-4b4d-aa9b-64caaf074bb3",
    "city": "Bloomfield",
    "country": "US",
    "postcode": "47424",
    "state": "Indiana",
}


def produce_test_messages():
    def value_serializer(message):
        return json.dumps(message).encode("utf-8")

    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"], value_serializer=value_serializer
    )

    time.sleep(0.3)
    for _ in range(5):
        producer.send("blockchain-task-topic", USER_RAW)
        time.sleep(0.05)


@timeout_decorator.timeout(1)
def consume_for_1_second():
    consumer = EventConsumer()
    consumer.consume()


@helpers.mockenv(
    DB_HOST="localhost",
    DB_PORT="5435",
    DB_NAME="blockchain-task",
    DB_USERNAME="postgres",
    DB_PASSWORD="password",
)
@pytest.mark.parametrize(
    "user_inserted_expected",
    [
        (USER_INSERTED),
    ],
)
def test_consumer(user_inserted_expected: Dict):

    db_engine = DbEngine()
    db_engine.execute("truncate table users")

    t = threading.Thread(target=produce_test_messages)
    t.start()

    try:
        consume_for_1_second()
    except timeout_decorator.TimeoutError:
        pass

    users_inserted_actual = db_engine.query_many(
        "select id, city, state, country, postcode from users"
    )

    assert users_inserted_actual
    assert user_inserted_expected == users_inserted_actual[0]
