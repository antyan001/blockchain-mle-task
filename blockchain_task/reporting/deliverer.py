from email.message import EmailMessage
import datetime
import os
import smtplib

from blockchain_task.data_models import ReportFigures
from blockchain_task.reporting.service import ReportService

TODAY = datetime.date.today()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_SERVER = os.getenv("EMAIL_SERVER")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


class ReportDeliverer:
    def __init__(self) -> None:
        self.report_service = ReportService()

    def prepare_report_text(self, report_figures: ReportFigures) -> str:
        report_text = (
            f"Hello\n\n"
            f"As of {TODAY}, we have {report_figures.users_cnt:,} users.\n"
            f"Out of those, {report_figures.us_users_cnt:,} are US users and {report_figures.non_us_users_cnt:,} are not.\n"
            f"Currently, US users constitute {report_figures.us_users_cnt/report_figures.users_cnt:.2%} of our user base.\n\n"
            f"Thank you,\n"
            f"Vlad's take-home task."
        )
        return report_text

    def send_report_email(self, report_text: str) -> None:
        msg = EmailMessage()
        msg.set_content(report_text)

        msg["Subject"] = f"User Report {TODAY}"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        s = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)

        s.send_message(msg)
        s.quit()

    def run(self) -> None:

        report_figures: ReportFigures = self.report_service.report()
        report_text: str = self.prepare_report_text(report_figures)
        self.send_report_email(report_text)


if __name__ == "__main__":
    report = ReportDeliverer()
    report.run()
