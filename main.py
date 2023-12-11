#main/init

from flask import Flask, Blueprint, render_template, redirect, url_for, send_from_directory, request, flash
from . import db

main = Blueprint('main', __name__)

#routes homepage
@main.route('/')
def landing_page():
	#items = Item.query.all()
	return render_template('landing.html')

#registration
# @main.route('/register', methods=['GET', 'POST'])
# def register():
# 	if request.method == 'POST':
# 		username = request.form.get('username')
# 		password = request.form.get('password')

# 		if not username or not password:
# 			flash('Both Username and password are required.', 'error')
# 		elif User.query.filter_by(username=username).first():
# 			flash('The USERNAME is already taken.', 'error')
# 		else:
# 			new_user = User(username=username)
# 			new_user.set_password(password)
# 			db.session.add(new_user)
# 			db.session.commit()
# 			flash('Registered Account Successfully!', 'success')
# 			return redirect(url_for('login_page'))
# 	return render_template('/auth/register.html')

#route login
# @main.route('/login', methods=['GET', 'POST'])
# def login_page():
	# if request.method == 'POST':
	# 	username = request.form.get('username')
	# 	password = request.form.get('password')

	# 	user = User.query.filter_by(username=username).first()

	# 	if user and user.check_password(password):
	# 		flash('Login Successful!', 'success')
	# 		return redirect(url_for('landing_page'))
	# return render_template('/auth/login.html')

#route look/images
@main.route('/look/<path:filename>')
def images_files(filename):
	return send_from_directory('look', filename)

#static route for login css
@main.route('/static/css/<path:filename>')
def login_css(filename):
	return send_from_directory('static/css', filename)