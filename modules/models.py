from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
	'''
	class used to create columns for users within user.table
	'''
	#class to generate user accounts; append username and hash to schema
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)

# class Shoes(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	price = db.Column(db.DECIMAL(10, 2), nullable=False)
# 	size = db.Column(db.Integer, nullable=False)