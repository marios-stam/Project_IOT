from datetime import datetime, timedelta
from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required

from ..models import User

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


@admin_blueprint.route('/drivers')
@login_required
def drivers():
    if User.query.get(current_user.id).role != 'manager':
        abort(403)
    return render_template('admin/drivers.html')


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
