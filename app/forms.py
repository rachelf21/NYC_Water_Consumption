from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, SelectMultipleField, TextAreaField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from app.models import Users

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# %%
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    dev = IntegerField('Development ID',
                        validators=[DataRequired(),NumberRange(1,107,"Development ID must be between 1 and 107.")])
    last = StringField('Last Name',
                       validators=[DataRequired(), Length(min=2, max=25)])
    first = StringField('First Name',
                        validators=[DataRequired(), Length(min=2, max=25)])
    title_options = [('', ''), ('Miss', 'Miss'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Mr.', 'Mr.'),
                     ('Dr.', 'Dr.')]
    title = SelectField('Title', choices=title_options)

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Continue')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User already exists.')



class PayBillForm(FlaskForm):
    credit_card_number = StringField('Credit Card Number', validators=[DataRequired()])
    security_code = StringField('Security Code', validators=[DataRequired()])
    expiration = StringField('Expiration Month/Year', validators=[DataRequired()])
    amount = DecimalField('Amount', number_format="#,##0.00 USD;-# USD", validators=[DataRequired()])
    submit = SubmitField('Submit Payment')

    def validate_amount(self, amount):
        if float(amount.data) < 0:
            raise ValidationError('Amount cannot be negative')
        if not str(amount.data).isdigit():
            raise ValidationError('Can only use digits')