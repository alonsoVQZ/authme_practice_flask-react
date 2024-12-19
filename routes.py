from flask import Blueprint
from flask_login import login_required, logout_user, login_user

api_bp = Blueprint('api', __name__)
auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)

api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(auth_bp, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
  return ''
@auth_bp.route('/register', methods=['POST'])
def register():
  return ''
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
  return ''

@users_bp.route('/me', methods=['GET'])
@login_required
def me():
  return ''