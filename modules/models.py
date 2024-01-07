from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
	'''class used to create columns for users within user.table'''
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)
	is_superuser = db.Column(db.Boolean(), unique=False, default=False)

class Category(db.Model):
	'''Handle Image Unicode within DB'''
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	slug = db.Column(db.String(20), unique=True, nullable=False)
	cords = db.relationship('Cord', back_populates='category', cascade='all, delete, delete-orphan')

	def __str__(self):
		return self.name

class Cord(db.Model):
	'''Class to sell my friends'''
	id = db.Column(db.Integer, primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=True, unique=False)
	category = db.relationship('Category', back_populates='cords')
	name = db.Column(db.String(30), unique=True, nullable=False)
	slug = db.Column(db.String(300), nullable=True, unique=True)
	price = db.Column(db.DECIMAL(10, 2), nullable=False)
	desc = db.Column(db.String(500), nullable=True)
	image = db.Column(db.String(128), nullable=True, unique=True)

	def __repr__(self):
		return f'id: {self.id} - Name: {self.name} - ${self.price}'