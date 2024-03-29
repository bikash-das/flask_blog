from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed #for profile pic and fileallowed types like jpg png
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Length, Email,EqualTo,ValidationError

from flaskblog.models import User #lesson 6 username validation

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    # custom validation lesson 6 when user enters bad inputs
    def validate_username(self,username): #user already exist or not
        user = User.query.filter_by(username=username.data).first() 
        # if no user then it returns null else value
        if user:
            raise ValidationError('That username is taken. Please choose another username')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose different email')

class LoginForm(FlaskForm):
    #username = StringField('Username',validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    #confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    # custom validation lesson 6 when user enters bad inputs
    def validate_username(self,username): #user already exist or not
        if username.data != current_user.username: #while updating
            user = User.query.filter_by(username=username.data).first() 
            # if no user then it returns null else value
            if user:
                raise ValidationError('That username is taken. Please choose another username')

    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose different email')





