import functools

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .forms import LoginForm, RegistrationForm
from .models import User

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')


def logout_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.is_authenticated:
            flash(
                [f'You are already logged in, {current_user.username}.'], category='warning')
            return redirect(url_for('views.index'))

        return view(**kwargs)

    return wrapped_view


@auth_blueprint.route('/register', methods=('GET', 'POST'))
@logout_required
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data,
                        password=generate_password_hash(form.password.data), admin=False)
            db.session.add(user)
            db.session.commit()
            flash(['Thanks for registering.'], category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.index'))

        for error in form.errors.values():
            flash(error, category='danger')

    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/login', methods=('GET', 'POST'))
@logout_required
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            error = None
            user = User.query.filter_by(username=form.username.data).first()

            if user is None:
                error = [f'User "{form.username.data}" does not exist.']
            elif not check_password_hash(user.password, form.password.data):
                error = ['Invalid password.']

            if error is None:
                login_user(user, remember=True)
                flash(
                    [f'You were successfully logged in, {user.username}.'], category='success')
                return redirect(url_for('views.index'))

        flash(error, category='danger')

    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash(['You were successfully logged out.'], category='success')
    return redirect(url_for('views.index'))
