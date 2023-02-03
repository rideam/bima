from algosdk.constants import address_len, note_max_length
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import InputRequired, Optional, Length, NumberRange


class EnrolForm(FlaskForm):
    """Policy enrollment form"""
    signature = StringField(
        'Signature',
        validators=[InputRequired(), Length(min=5)],
        render_kw={"placeholder": "Signature"}
    )
    submit = SubmitField('Join')


class PayForm(FlaskForm):
    """Payment form"""
    amount = DecimalField(
        'Amount',
        validators=[InputRequired(), NumberRange(min=0)],
        render_kw={"placeholder": "Premium Amount"}
    )
    receiver = StringField(
        'Receiver',
        validators=[InputRequired(), Length(min=address_len, max=address_len)],
        render_kw={"placeholder": "Receiver Address"}
    )
    note = StringField(
        'Note',
        validators=[Optional(), Length(max=note_max_length)],
        render_kw={"placeholder": "Note"})
    submit = SubmitField('Pay')


class LoginForm(FlaskForm):
    """Login form"""
    passphrase = StringField('25-word Passphrase',
                             validators=[InputRequired()],
                             render_kw={"placeholder": "Enter your 25-word Passphrase"}
                             )
    submit = SubmitField('Login')
