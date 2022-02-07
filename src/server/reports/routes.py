from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Report
from datetime import datetime as dt
from flask import request, jsonify
from .db_interface import *
import json

reports_blueprint = Blueprint('reports_blueprint', __name__)


@reports_blueprint.route('/reports', methods=['POST'])  # create new Report
def create_report_route():
    return create_report()


@reports_blueprint.route('/reports', methods=['PUT'])  # Update a report
def update_report_route():
    return update_report()


# Get a Report
@reports_blueprint.route('/reports/<report_id>', methods=['GET'])
def get_report_route(report_id):
    return get_report(report_id)


# Get all Reports
@reports_blueprint.route('/reports/', methods=['GET'])
def get_al_reports_route():
    return get_all_reports()
