from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config
from models import db, User
from routes import api_bp

login_manager = LoginManager()
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
  return db.session.execute(db.select(User).where(User.id == user_id)).scalar_one_or_none

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  migrate.init_app(app, db)
  login_manager.init_app(app)
  app.register_blueprint(api_bp, url_prefix='/api')
  return app