from typing import Dict, List, Union
import os

import psycopg2  # type: ignore
import psycopg2.extras

from blockchain_task.data_models import ReportFigures  # type: ignore
from blockchain_task.db_engine import DbEngine


class ReportService:
    def __init__(self):
        self.db_engine = DbEngine()

    def report(self) -> ReportFigures:
        query = "select * from report"
        result = self.db_engine.query_one(query)
        return ReportFigures(**result)
