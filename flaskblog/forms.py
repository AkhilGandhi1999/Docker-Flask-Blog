from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed 
from flask_login import current_user
from wtforms import StringField,BooleanField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Length(min = 5, max = 20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	password = PasswordField('Password',validators=[DataRequired(), Length(min=5, max=20)])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()

		if user:
			raise ValidationError("The username is already taken, please choose another one!")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()

		if user:
			raise ValidationError("The email is already taken, please choose another one!")

class LoginForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
	submit = SubmitField('Login')

	remember = BooleanField('Remember Me')


class UpdateAccountForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Length(min = 5, max = 20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed('jpg', 'png')])
	submit = SubmitField('Update')


	def validate_username(self, username):
		if current_user.username != username.data:
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError("The username is already taken, please choose another one!")

	def validate_email(self, email):
		if current_user.email != email.data:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError("The email is already taken, please choose another one!")

	
class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content',validators =[DataRequired()])
	submit = SubmitField('Post')


	
class RequestResetForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(), Email()])
	submit = SubmitField('Request Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()

		if user is None:
			raise ValidationError("No such user!, please create a new account.")

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',validators=[DataRequired(), Length(min=5, max=20)])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

	