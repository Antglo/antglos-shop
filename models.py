from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
	#class to generate user accounts; append username and hash to schema
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	
	#set password upon registry "called in app.py"
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	#verify password during authentication
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

# class Shoes(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	price = db.Column(db.DECIMAL(10, 2), nullable=False)
# 	size = db.Column(db.Integer, nullable=False)