from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, request

from chgallery.auth.forms import RegisterForm
from chgallery.db import get_db_session
from chgallery.db.declarative import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = get_db_session()
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
        )
        session.add(user)
        session.commit()
        return 'User created successfully!'
    return render_template('auth/register.html', form=form)
