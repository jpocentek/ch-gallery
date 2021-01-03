import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from chgallery.db import get_db_session
from chgallery.db.declarative import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=32)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(min=0, max=64)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=1, max=64)])
    password_repeat = PasswordField('repeat password', validators=[EqualTo('password')])

    def validate_username(self, field):
        session = get_db_session()
        if session.query(User).filter(User.username == field.data).scalar() is not None:
            raise ValidationError('User {} already exists'.format(field.data))
        if not re.match(r'^[\w\d\-_#]+$', field.data):
            raise ValidationError('Invalid username')

    def validate_email(self, field):
        session = get_db_session()
        if session.query(User).filter(User.email == field.data).scalar() is not None:
            raise ValidationError('Email already taken')
