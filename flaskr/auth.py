from urllib.parse import urlparse, urljoin
from flask import (
    current_app, Blueprint, flash, redirect, render_template, request, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user
from flaskr.models import User
from flaskr import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user = User(username=username,
                        password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(
                '%s registered successfully', user.username)
            return redirect(url_for('auth.login', _external=True))

        current_app.logger.info('%s failed to log in', username)
        flash(error)

    return render_template('auth/register.html')


@bp.route('/', methods=('GET', 'POST'))
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            login_user(user)
            current_app.logger.info('%s logged in successfully', user.username)
            next = request.args.get('next')
            if not is_safe_url(next):
                abort(400)
            return redirect(next or url_for('index', _external=True))

        current_app.logger.info('%s failed to log in', username)
        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    current_app.logger.info(
        '%s logged out successfully', current_user.username)
    logout_user()
    return redirect(url_for('index', _external=True))
