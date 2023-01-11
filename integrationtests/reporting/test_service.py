import helpers

from blockchain_task.data_models import ReportFigures, User
from blockchain_task.db_engine import DbEngine
from blockchain_task.event_processor import EventProcessor
from blockchain_task.reporting.service import ReportService  # type: ignore


@helpers.mockenv(
    DB_HOST="localhost",
    DB_PORT="5435",
    DB_NAME="blockchain-task",
    DB_USERNAME="postgres",
    DB_PASSWORD="password",
)
def test_service():

    db_engine = DbEngine()
    db_engine.execute("truncate table users")
    db_engine.execute("update report set users_cnt=0, us_users_cnt=0, non_us_users_cnt=0")

    service = ReportService()
    prediction = service.report()
    assert prediction == ReportFigures(users_cnt=0, us_users_cnt=0, non_us_users_cnt=0)

    user_raw = {
        "id": "service--test-4b4d-aa9b-64caaf074bb3",
        "address": {"city": "Bloomfield", "state": "US-IN", "country": "US", "postCode": "47424"},
    }

    user = User(**user_raw)

    event_processor = EventProcessor()
    event_processor.process_user_creation(user=user)

    prediction = service.report()
    assert prediction == ReportFigures(users_cnt=1, us_users_cnt=1, non_us_users_cnt=0)
