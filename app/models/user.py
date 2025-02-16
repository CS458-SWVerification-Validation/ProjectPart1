from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date, datetime, timedelta
from sqlalchemy.sql import func

from app.extensions import db

class User(UserMixin, db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	firstname = db.Column(db.String(128), unique=False, nullable=False)
	lastname = db.Column(db.String(128), unique=False, nullable=False)
	email = db.Column(db.String(128), unique=True, nullable=False)
	password = db.Column(db.String(256), nullable=False)
	birthdate = db.Column(db.DateTime(), nullable=False)
	phone_number = db.Column(db.String(10), unique=True, nullable=False)  # New phone column

	def __init__(self, firstname, lastname, birthdate, phone_number, email, password):
		self.lastname = lastname
		self.firstname = firstname
		self.birthdate = birthdate
		self.phone_number = phone_number
		self.email = email
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)
  
	def getUserById(id):
		return User.query.get(id)

	def getUserByEmail(email):
		return User.query.filter_by(email=email).first()

class OnlineUser(db.Model):
	__tablename__ = 'OnlineUsers'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	ipaddress = db.Column(db.String(128), unique=True, nullable=False)
	logindatetime = db.Column(db.DateTime, nullable=False)

	user = db.relationship('User', backref='online_users')

	def getUserByEmail(email):
		return OnlineUser.query.filter_by(email=email).first()

	def getUserByIpAddress(ipaddress):
		return OnlineUser.query.filter_by(ipaddress=ipaddress).first()