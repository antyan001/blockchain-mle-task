import datetime

from flask import Blueprint, abort

from blockchain_task.data_models import ReportFigures
from blockchain_task.reporting.service import ReportService

reporting_bp = Blueprint("model", __name__)


@reporting_bp.route("/", methods=["POST", "GET"])
def get_report_figures():

    service = ReportService()

    try:
        figures: ReportFigures = service.report()
    except Exception as err:
        return abort(400, str(err))

    return {"report": figures.dict()}
