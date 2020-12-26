from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from chgallery.db import get_db_session
from chgallery.db.declarative import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password_repeat = PasswordField('repeat password', validators=[EqualTo('password')])

    def validate_username(self, field):
        session = get_db_session()
        if session.query(User).filter(User.username == field.data).scalar() is not None:
            raise ValidationError('User {} already exists'.format(field.data))

    def validate_email(self, field):
        session = get_db_session()
        if session.query(User).filter(User.email == field.data).scalar() is not None:
            raise ValidationError('Email already taken')
