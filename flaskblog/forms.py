from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User 

class SignUp(FlaskForm):
	username = StringField('Mobile No', validators = [DataRequired(), Length(min = 4, max = 15)])
	accountName = StringField('Full Name', validators = [DataRequired(), Length(min = 4, max = 15)])
	city = StringField('City', validators = [DataRequired(), Length(min = 2, max = 25)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('password', validators = [DataRequired()])
	confirm_password = PasswordField('confirm password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('sign up')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('that username is taken, please choose a diffrent one')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('that email is taken, please choose a diffrent one')

class SignIn(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('password', validators = [DataRequired()])
	remember_me = BooleanField('remember me')
	submit = SubmitField('sign in')

class UpdateProfile(FlaskForm):
	username = StringField('Mobile No', validators = [DataRequired(), Length(min = 4, max = 15)])
	accountName = StringField('Full Name', validators = [DataRequired(), Length(min = 4, max = 15)])
	city = StringField('city', validators = [DataRequired(), Length(min = 2, max = 25)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	picture = FileField('Update profile picture', validators = [FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError('that username is taken, please choose a diffrent one')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('that email is taken, please choose a diffrent one')
