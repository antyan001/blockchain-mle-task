from typing import Dict, List, Union
import os

import psycopg2  # type: ignore
import psycopg2.extras  # type: ignore

from blockchain_task.data_models import ReportFigures, User
from blockchain_task.db_engine import DbEngine
from blockchain_task.preprocessing.address import standardise_state
from blockchain_task.reporting.deliverer import ReportDeliverer
from blockchain_task.reporting.service import ReportService


class EventProcessor:
    def __init__(self):
        self.db_engine = DbEngine()
        self.report_service = ReportService()
        self.report_deliverer = ReportDeliverer()

    def process_user_creation(self, user: User) -> None:
        """
        Currently the only event which needs to be consumed is user creation.
        This method also sends the report after each 100 users.
        """

        user_id = user.id
        city = user.address.city
        state = standardise_state(user.address.state)
        country = user.address.country
        postcode = user.address.postCode.strip()

        report_figures: ReportFigures = self.report_service.report()
        if report_figures.users_cnt and report_figures.users_cnt % 100 == 0:
            self.report_deliverer.run()

        report_figures.users_cnt += 1
        if user.address.country == "US":
            report_figures.us_users_cnt += 1
        else:
            report_figures.non_us_users_cnt += 1

        qry = f"""
        begin transaction; 

        insert into users (id, city, state, country, postcode)
        values (
            '{user_id}', 
            '{city}', 
             {"'"+state+"'" if state else 'NULL'}, 
            '{country}', 
            '{postcode}'
        );

        update report set 
            users_cnt = {report_figures.users_cnt}, 
            us_users_cnt = {report_figures.us_users_cnt}, 
            non_us_users_cnt = {report_figures.non_us_users_cnt},
            updated_date = CURRENT_TIMESTAMP;

        commit;
        """
        self.db_engine.execute(qry)
