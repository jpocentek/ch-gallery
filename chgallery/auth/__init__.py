from flask import (
        Blueprint,
        g,
        redirect,
        render_template,
        session,
        url_for
)
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from chgallery.auth.decorators import login_required
from chgallery.auth.forms import LoginForm, RegisterForm
from chgallery.db import get_db_session
from chgallery.db.declarative import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
@login_required
def dashboard():
    """ TODO """
    return render_template('auth/dashboard.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db_session = get_db_session()
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
        )
        db_session.add(user)
        db_session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        db_session = get_db_session()

        try:
            user = db_session.query(User).filter(User.username == form.username.data).one()
        except NoResultFound:
            user = None

        if user is None or not check_password_hash(user.password, form.password.data):
            error = 'Invalid login credentials'
        else:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('auth.dashboard'))

    return render_template('auth/login.html', form=form, error=error)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db_session().query(User).filter(User.id == user_id).one()
