from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, TextAreaField, EmailField, SelectField, TelField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fitkit.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            


class AddressForm(FlaskForm):


    select_choices = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Bihar', 'Bihar'),
        ('West Bengal', 'West Bengal'),
        ('Odisha', 'Odisha'),
        ('Delhi', 'Delhi')
    ]


    name = StringField('name', validators=[DataRequired()])
    mob  = TelField('Mobile Number', validators=[DataRequired()])
    # email = EmailField('email', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', choices=select_choices, validators=[DataRequired()])
    pincode = StringField('pincode', validators=[DataRequired()])
    submit = SubmitField('Checkout')


    def validate_mob(self, field):
        # Custom validation logic for the 'username' field
        if field.data.isalpha():
            raise ValidationError('Mobile Number digits only')
        
        if len(field.data) < 10:
            raise ValidationError('Mobile Number should be of 10 digits')

