from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required

from ..models import User

client_blueprint = Blueprint(
    'client_blueprint', __name__, url_prefix='/client')


@client_blueprint.route('/ctzn')
@login_required
def ctzn():
    if User.query.get(current_user.id).role != 'ctzn':
        abort(403)
    return render_template('client/ctzn.html')

@client_blueprint.route('/drvr')
@login_required
def drvr():
    if User.query.get(current_user.id).role != 'drvr':
        abort(403)
    return render_template('client/drvr.html')