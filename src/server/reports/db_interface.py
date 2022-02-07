from flask import Blueprint, make_response
from flask import current_app as app
from flask.json import _dump_arg_defaults
from ..models import db, Report
from datetime import datetime as dt
from flask import request, jsonify


def get_report(report_id=None):
    result = db.session.query(Report).filter(
        Report.report_id == report_id).all()
    if(len(result) == 0):
        return make_response(f"No report found with ID: {report_id}")
    else:
        print(f"Gettind data of report: {report_id} ...")
        data = result[0].__dict__
        data.pop('_sa_instance_state')

        data_json = jsonify(data)

        return make_response(data_json)


def update_report(report_id=None):
    data = request.get_json()
    id = data['report_id']
    result = db.session.query(Report).filter(Report.report_id == id).all()
    if(len(result) == 0):
        return create_report(data)

    print(f"Updating report with ID:{id} ...")
    for key, value in data.items():
        if key == 'created' or key == 'updated':
            result[0].updated = dt.now()
            continue

        setattr(result[0], key, value)

    db.session.commit()

    return make_response(f"Updated report with ID:{id}")


def create_report(data=None):
    if data == None:
        data = request.get_json()

    data['updated'] = dt.now()  # set created date
    new_report = Report(**data)

    # add to database
    db.session.add(new_report)
    db.session.commit()

    return make_response(f"New report created with ID:{new_report.report_id}")


def get_all_reports():
    print("Getting all Reports")

    result = db.session.query(Report).all()
    if(len(result) == 0):
        return make_response(f"No Report found!")

    reports = []
    for i in range(len(result)):
        report = result[i].__dict__
        report.pop('_sa_instance_state')

        reports.append(report)

    return jsonify(reports)
