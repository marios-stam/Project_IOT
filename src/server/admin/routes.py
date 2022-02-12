from datetime import datetime, timedelta

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from .. import db
from ..models import User
from .forms import DriverForm

admin_blueprint = Blueprint('admin_blueprint', __name__, url_prefix='/admin')


@admin_blueprint.route('/')
@login_required
def index():
    if User.query.get(current_user.id).role != 'manager':
        abort(403)
    return render_template('admin/index.html')


@admin_blueprint.route('/citizens')
@login_required
def citizens():
    if User.query.get(current_user.id).role != 'manager':
        abort(403)
    threshold = datetime.now()-timedelta(days=30)
    active = User.query.filter_by(role='citizen').filter(
        User.created > threshold).order_by(User.created.desc()).all()
    leaderboard = User.query.filter_by(
        role='citizen').order_by(User.points.desc()).all()
    top3 = leaderboard[:3]
    rest = leaderboard[3:]
    active_num = len(active)
    return render_template('admin/citizens.html', active=active, top3=top3, rest=rest, active_num=active_num)


@admin_blueprint.route('/drivers', methods=('GET', 'POST'))
@login_required
def drivers():
    if User.query.get(current_user.id).role != 'manager':
        abort(403)
    form = DriverForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            driver = User(username=form.username.data, email=form.email.data, created=datetime.now(),
                          password=generate_password_hash(form.password.data), role='driver', admin=False)
            db.session.add(driver)
            db.session.commit()
            flash(
                [f'The driver account was successfully created.'], category='success')
            return redirect(url_for('admin_blueprint.drivers'))

        for error in form.errors.values():
            flash(error, category='danger')

    drivers = User.query.filter_by(
        role='driver').order_by(User.created.desc()).all()
    drivers_num = len(drivers)
    return render_template('admin/drivers.html', form=form, drivers=drivers, drivers_num=drivers_num)


@admin_blueprint.route('/drivers/delete/<id>')
@login_required
def delete(id):
    if User.query.get(current_user.id).role != 'manager':
        abort(403)
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash(['The driver account was successfully deleted.'], category='success')
    return redirect(url_for('admin_blueprint.drivers'))


@admin_blueprint.route('/bins')
@login_required
def bins():
    if User.query.get(current_user.id).role != 'manager':
        abort(403)
    return render_template('admin/bins.html')


@admin_blueprint.route('/reports')
@login_required
def reports():
    if User.query.get(current_user.id).role != 'manager':
        abort(403)
    return render_template('admin/reports.html')
