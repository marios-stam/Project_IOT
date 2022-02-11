from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .. import db
from ..__config__ import BOUNTY_DEADLINE
from ..models import Bounty, User
from ..utils import diff_time
from .forms import EditForm

profile_blueprint = Blueprint(
    'profile_blueprint', __name__, url_prefix='/profile')


@profile_blueprint.route('/view')
@login_required
def view():
    return render_template('profile/view.html')


@profile_blueprint.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    form = EditForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.get(current_user.id)
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()
            flash(
                [f'Your profile was successfully updated, {user.username}.'], category='success')
            return redirect(url_for('profile_blueprint.view'))

        for error in form.errors.values():
            flash(error, category='danger')

    return render_template('profile/edit.html', form=form)


@profile_blueprint.route('/delete')
@login_required
def delete():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash(['Your profile was successfully deleted.'], category='success')
    return redirect(url_for('views.index'))


@profile_blueprint.route('/bounties')
@login_required
def bounties():
    bounties = get_uncompleted_bounties_of_user(current_user.id)
    print(bounties)
    return render_template('profile/bounties.html', bounties=bounties)


def get_uncompleted_bounties_of_user(usr_id):
    result = db.session.query(Bounty).filter(
        Bounty.assigned_usr_id == usr_id).filter(Bounty.completed == False).all()

    if(len(result) == 0):
        return []

    bounties = []
    refresh = []
    for i in range(len(result)):
        bounty = result[i].__dict__

        if bounty['assigned_usr_id'] is not None and diff_time(bounty['time_assigned'], datetime.now()) > BOUNTY_DEADLINE and not bounty['completed']:
            refresh.append(bounty['id'])
        else:
            bounty_json = {
                'id': bounty['id'],
                'timestamp': bounty['timestamp'],
                'bin_id': bounty['bin_id'],
                'message': bounty['message'],
                'points': bounty['points'],
                'type': bounty['type'],
                'assigned_usr_id': bounty['assigned_usr_id'],
                'time_assigned': bounty['time_assigned'],
                'completed': bounty['completed'],
            }

            bounties.append(bounty_json)

    for id_ in refresh:
        # print(f"Unissigning user {bounty['assigned_usr_id']} from bounty {bounty['id']}! Time limit exceeded.")
        update_bounty({
            'id': id_,
            'time_assigned': None,
            'assigned_usr_id': None
        })

    return bounties


def update_bounty(data=None):
    if data is None:
        data = request.get_json()

    id = data['id']
    result = db.session.query(Bounty).filter(Bounty.id == id).all()
    if(len(result) == 0):
        return create_bounty(data)

    print(f"Updating bounty with ID:{id} ...")
    for key, value in data.items():
        if key == 'created' or key == 'updated':
            result[0].updated = datetime.now()
            continue

        setattr(result[0], key, value)

    db.session.commit()


def create_bounty(data=None):
    if data == None:
        data = request.get_json()

    data['timestamp'] = datetime.now()  # set created date
    # data['time_assigned'] = dt.now()  # set created date

    new_bounty = Bounty(**data)

    # add to database
    db.session.add(new_bounty)
    db.session.commit()
