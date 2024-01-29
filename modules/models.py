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
	order_items = db.relationship('OrderItem', back_populates='cordproducts', cascade='all, delete, delete-orphan')

	def __repr__(self):
		return f'id: {self.id} - Name: {self.name} - ${self.price}'
	
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False, unique=False)
    email_address = db.Column(db.String(100), nullable=False, unique=False)
    city = db.Column(db.String(50), nullable=False, unique=False)
    postal_code = db.Column(db.Integer(), nullable=False, unique=False)
    state = db.Column(db.String(50), nullable=False, unique=False)
    phone_no = db.Column(db.Integer(), nullable=False, unique=False)
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete, delete-orphan')
    total_amount = db.Column(db.Integer(), nullable=False, unique=False)

    def __repr__(self):
        return self.full_name + ' - ' + self.email_address
    


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False, unique=False)
    product_id = db.Column(db.Integer, db.ForeignKey('cord.id', ondelete='CASCADE'), nullable=False, unique=False)
    cordproducts = db.relationship('Cord', back_populates='order_items')
    quantity = db.Column(db.Integer(), nullable=False, unique=False)
    order = db.relationship('Order', back_populates='items')

    def __repr__(self):
        return f'Order id:{self.order_id} - CordProduct: {self.products.name}'