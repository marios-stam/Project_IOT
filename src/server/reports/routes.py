from datetime import datetime
from flask import Blueprint, flash, make_response, redirect, render_template, url_for
from flask import current_app as app
from flask_login import current_user, login_required

from .forms import ReportForm
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


@reports_blueprint.route('/rpt/create/<id>', methods=['GET', 'POST'])
@login_required
def create(id):
    form = ReportForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            report = Report(user_id=current_user.id, details=form.desc.data,
                            updated=datetime.now(), status='unconfirmed')
            db.session.add(report)
            db.session.commit()
            flash(
                [f'Your report was successfully submitted, {current_user.username}.'], category='success')
            return redirect(url_for('reports_blueprint.view'))

        for error in form.errors.values():
            flash(error, category='danger')

    return render_template('reports/create.html', bin_id=id, form=form)


@reports_blueprint.route('/rpt/view', methods=['GET', 'POST'])
@login_required
def view():
    reports = Report.query.filter_by(user_id=current_user.id).all()
    return render_template('reports/view.html', reports=reports)
