from flask import Flask, Blueprint, render_template, redirect, url_for, send_from_directory, request, flash
from flask import Blueprint
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'login'
    
@auth.route('/register')
def register():
    return 'Register'
#registration
@auth.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		if not username or not password:
			flash('Both Username and password are required.', 'error')
		elif User.query.filter_by(username=username).first():
			flash('The USERNAME is already taken.', 'error')
		else:
			new_user = User(username=username)
			new_user.set_password(password)
			db.session.add(new_user)
			db.session.commit()
			flash('Registered Account Successfully!', 'success')
			return redirect(url_for('login_page'))
	return render_template('/auth/register.html')

@auth.route('/logout')
def logout():
    return 'logout'