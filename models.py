from datetime import datetime, timezone
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class TimestampMixin():
  created: Mapped[str] = mapped_column(default=lambda: datetime.now(timezone.utc))
  updated: Mapped[str] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class User(TimestampMixin, UserMixin, db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(nullable=False, unique=True)
  email: Mapped[str] = mapped_column(nullable=False, unique=True)
  hashed_password: Mapped[str] = mapped_column(nullable=False)
  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password
  @property
  def password(self):
    return 'Password is not an readable attribute.'
  @password.setter
  def password(self, password):
    self.hashed_password = generate_password_hash(password)
  def check_password(self, password):
    return check_password_hash(self.hashed_password, password)
  def to_dict(self):
    return {
      'id': self.id,
      'username': self.username,
      'email': self.email
    }