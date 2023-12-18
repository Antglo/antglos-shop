from flask import Flask, Blueprint, render_template, redirect, url_for, send_from_directory, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from .models import User
from app import db

auth = Blueprint('auth', __name__)

#route login
@auth.route('/login', methods=['GET', 'POST'])
def login_page():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		user = User.query.filter_by(username=username).first()

		if not user or not check_password_hash(user.password, password):
			flash('Login Invalid! Try again.')
			return redirect(url_for('auth.login_page'))
		else:
			login_user(user, remember=True) #creates a session for the logged in user
			return redirect(url_for('main.landing_page'))
      
	return render_template('/auth/login.html')

#registration
# @auth.route('/register')
# def register_load():
#     return render_template('register.html')
@auth.route('/register', methods=['GET', 'POST'])
def register():
	'''function for registration logic; registration success/fail'''
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		#Check if poth fields are contain text
		if not username or not password:
			flash('Both Username and password are required.', 'error')
			#Let user try again
			return redirect(url_for('auth.register'))

		#check table.user if username is taken
		user =	User.query.filter_by(username=username).first()
		if user:
			flash('The USERNAME is already taken.', 'error')
			#Redirect (reload page) to allow user to try again
			return redirect(url_for('auth.register'))


		#If user form is correct; create user row in 'schema.db'
		new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
		#new_user.set_password(password)
		db.session.add(new_user)
		db.session.commit()
		flash('Registered Account Successfully!', 'success')
		return redirect(url_for('auth.login_page'))
	else:
		return render_template('/auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))
