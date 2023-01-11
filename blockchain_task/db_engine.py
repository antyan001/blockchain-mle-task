from typing import Dict, List, Optional, Union
import os

import psycopg2  # type: ignore
import psycopg2.extras


class DbEngine:
    def __init__(self):
        self.db_credentials = dict(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )

    def query_one(self, query: str, params: Dict = {}) -> Optional[Dict]:

        with psycopg2.connect(**self.db_credentials) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as curs:
                curs.execute(query, params)
                result_single: psycopg2.extras.Record = curs.fetchone()
                if result_single:
                    return result_single._asdict()
                return {}

    def query_many(self, query: str, params: Dict = {}) -> Optional[List[Dict]]:

        with psycopg2.connect(**self.db_credentials) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as curs:
                curs.execute(query, params)
                result_multiple: List = curs.fetchall()
                if result_multiple:
                    return [i._asdict() for i in result_multiple]
                return []

    def execute(self, query: str, params: Dict = {}) -> None:
        with psycopg2.connect(**self.db_credentials) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as curs:
                curs.execute(query, params)
