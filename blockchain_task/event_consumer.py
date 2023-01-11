import json

from kafka import KafkaConsumer
from pydantic import ValidationError

from blockchain_task.data_models import User
from blockchain_task.event_processor import EventProcessor


class EventConsumer:
    """
    Kafka consumer that will connect to the "blockchain-task-topic" topic and consume the events.
    integrationtests/test_event_consumer.py contains a producer that will create messages which can be consumed.
    """

    def __init__(self) -> None:
        self.consumer = KafkaConsumer(
            "blockchain-task-topic",
            bootstrap_servers="localhost:9092",
            auto_offset_reset="latest",
        )
        self.event_processor = EventProcessor()

    def consume(self):
        for message in self.consumer:
            user_raw = json.loads(message.value)
            try:
                user = User(**user_raw)
                self.event_processor.process_user_creation(user=user)
            except ValidationError as err:
                print(f"Data validation failed with the following error:\n{str(err)}")


if __name__ == "__main__":
    consumer = EventConsumer()
    consumer.consume()
