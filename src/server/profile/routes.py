from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..models import User
from .. import db
from .forms import EditForm, ViewForm

profile_blueprint = Blueprint('profile_blueprint', __name__, url_prefix='/me')


@profile_blueprint.route('/view')
@login_required
def view():
    form = ViewForm()
    return render_template('profile/view.html', form=form)


@profile_blueprint.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    form = EditForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.get(current_user.id)
            user.username = form.username.data
            user.email = form.email.data
            user.bio = form.bio.data
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
