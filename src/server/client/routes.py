from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required

from ..models import User

client_blueprint = Blueprint(
    'client_blueprint', __name__, url_prefix='/client')


@client_blueprint.route('/citizen')
@login_required
def citizen():
    if User.query.get(current_user.id).role != 'citizen':
        abort(403)
    return render_template('client/citizen.html')


@client_blueprint.route('/driver')
@login_required
def driver():
    if User.query.get(current_user.id).role != 'driver':
        abort(403)
    return render_template('client/driver.html')


@client_blueprint.route('/mngr')
@login_required
def mngr():
    if User.query.get(current_user.id).role != 'mngr':
        abort(403)
    return render_template('client/mngr.html')
