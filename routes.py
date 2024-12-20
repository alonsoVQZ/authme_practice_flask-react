from flask import Blueprint, jsonify
from flask_login import current_user, login_required, logout_user, login_user
from sqlalchemy import or_

from forms import LoginForm, RegisterForm
from models import db, User

api_bp = Blueprint('api', __name__)
auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)

api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(auth_bp, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = db.session.execute(db.select(User).where(or_(User.username == form.credential.data, User.email == form.credential.data))).scalar_one_or_none()
    if user:
      if user.check_password(form.password.data):
        login_user(user)
        return jsonify({ 'message': 'Login successful' }), 200
      else:
        return jsonify({ 'error': 'Incorrect Password' }), 400
    else:
      return jsonify({ 'error': 'Credentials not found' }), 400
  else:
    return jsonify({ 'error': form.errors }), 400
@auth_bp.route('/register', methods=['POST'])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    user = User(
      username = form.username.data,
      email = form.email.data,
      password = form.password.data
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'message': 'Registration successful' }), 200
  else:
    return jsonify({ 'error': form.errors})
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
  logout_user()
  return jsonify({ 'message': 'Logout successful'}), 200

@users_bp.route('/me', methods=['GET'])
@login_required
def me():
  user = current_user()
  return user.to_dict()