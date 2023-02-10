from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField,ValidationError
from wtforms.validators import DataRequired,Length,Email,Regexp, EqualTo
from ..models import User
class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Login')


class RegistrationForm(FlaskForm):
    username=StringField('Enter Username',validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', flags=0,message='Username '
                                                                                                                       'should contain only letters,dots and underscore and should start with letter')])
    email=StringField('Enter your email',validators=[DataRequired(),Length(1,64),Email()])
    password=PasswordField('Enter your password',validators=[DataRequired()])
    password2=PasswordField('Confirm password',validators=[DataRequired(), EqualTo('password', message='Password must match')])
    register=SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
           raise ValidationError('The email is already registered')


    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')


