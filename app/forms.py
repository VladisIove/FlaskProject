from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, regexp
from app.models import User 

class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Request Password Reset')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Sign In')

class CreatePost(FlaskForm):
  title = StringField('Title:', validators=[DataRequired()])
  body = StringField('Text:', validators=[DataRequired()])
  tags = StringField('Tags:')
  submit = SubmitField('Save!')

class ResetPasswordRequestForm( FlaskForm ):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Request Password Reset')

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:         
    	raise ValidationError('Please use a different username.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address.')


class CommentForm(FlaskForm):
  body = StringField('Comment', validators=[DataRequired()])
  submit = SubmitField('Comment!')

class SearchForm(FlaskForm):
  body = StringField('Search', validators=[DataRequired()])