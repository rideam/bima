from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    """Login form"""
    passphrase = StringField(
        '25-word Passphrase',
        validators=[InputRequired()],
        render_kw={"placeholder": "Enter your 25-word Passphrase"}
    )
    submit = SubmitField('Login')
