from flask_wtf import FlaskForm
from flask_wtf.csrf import ValidationError
from sqlalchemy import select
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, length

from models import db, User

class LoginForm(FlaskForm):
  credential = StringField('credential', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired(), length(min=6)])

class RegisterForm(FlaskForm):
  username = StringField('username', validators=[DataRequired(), Length(min=4)])
  email = EmailField('email', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
  def validate_username(self, username):
    if db.session.execute(select(User).where(User.username == username.data)).scalar_one_or_none():
      raise ValidationError('User already exists')
  def validate_email(self, email):
    if db.session.execute(select(User).where(User.email == email.data)).scalar_one_or_none():
      raise ValidationError('Email already exists')