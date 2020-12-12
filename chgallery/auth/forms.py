from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    recaptcha = RecaptchaField()
