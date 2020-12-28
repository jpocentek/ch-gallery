from flask import (
        Blueprint,
        abort,
        current_app,
        g,
        redirect,
        render_template,
        session,
        url_for
)
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from chgallery.auth.decorators import login_required
from chgallery.auth.forms import LoginForm, RegisterForm
from chgallery.db import get_db_session
from chgallery.db.declarative import Image, User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
@login_required
def dashboard():
    images = (
        g.db_session.query(Image)
        .filter(Image.author == g.user)
        .order_by(Image.creation_date.desc())
    )

    return render_template('auth/dashboard.html', images=images)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_app.config.get('REGISTRATION_DISABLED'):
        abort(404)

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
    g.user = None

    if user_id is not None:
        try:
            g.user = get_db_session().query(User).filter(User.id == user_id).one()
        except NoResultFound:
            session.clear()
