from flask import Blueprint, render_template, redirect, url_for, request, flash, session, make_response
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Cord, Order, OrderItem
from app import db
from .cart import Cart

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
	
#route for cart
@auth.route('/cart', methods=['GET', 'POST'])
def cart_page():
	if current_user.is_authenticated:
		return render_template('/auth/cart.html')
	else:
		return redirect(url_for('auth.login_page'))

#Route to add items to the cart
@auth.route('/add/<slug>', methods=['POST', 'GET'])
def cart_add(slug):
	cordproduct = Cord.query.filter_by(slug=slug).first_or_404
	if request.method == 'POST':
		item = request.form.get('cordproduct_id', None)
		if item:
			cart = Cart(session)
			cart.add_or_update(item)
			return render_template('auth/parts/cart_menu.html')
		return render_template('auth/cart.html', cordproduct=cordproduct)

#route to update the cart
@auth.route('/cart_update/<cord_id>/<action>')
def cart_update(cord_id, action):
	cart = Cart(session)

	if action == 'increment':
		cart.add_or_update(cord_id, 1)
	elif action == 'decrement':
		cart.add_or_update(cord_id, -1)

	cordproduct = Cord.query.filter_by(id=int(cord_id)).first()
	cart_item = cart.get_item(cord_id)

	if cart_item:
		item = {
			'cord_id': cordproduct.id,
			'cordproduct': {
				'name': cordproduct.name,
				'price': cordproduct.price,
			},
			'slug': cordproduct.slug,
			'total_price': cordproduct.price * int(cart_item['quantity']),
			'quantity': cart_item['quantity'],
		}
	else:
		item = None

	response = make_response(render_template('auth/parts/cart_item.html', item=item))
	response.headers['HX-Trigger'] = 'update-cart-menu'
	return response

@auth.route('/get-cart-count')
def get_cart_count():
	return render_template('/auth/parts/cart_menu.html')

@auth.route('/get-total-amount')
def get_total_amount():
	return render_template('auth/parts/total_amount.html')

@auth.route('/checkout', methods=['GET', 'POST'])
def checkout():
	cart = Cart(session)
	if cart.__len__() == 0:
		return redirect(url_for('auth.cart_page'))
	
	if request.method == 'POST':
		full_name = request.form['full_name']
		email_address = request.form['email_address']
		city = request.form['city']
		postal_code = int(request.form['postal_code'])
		state = request.form['state']
		phone_no = int(request.form['phone_no'])

		try:
			order = Order(
				full_name=full_name,
				email_address=email_address,
				city=city,
				postal_code=postal_code,
				state=state,
				phone_no=phone_no,
				total_amount=int(cart.get_total_amount())
			)
			db.session.add(order)

			for item in cart:
				order_item = OrderItem(
					product_id = item['product_id'],
					quantity = item['quantity'],
					order_id = order.id
				)
				db.session.add(order_item)
			db.session.commit()

			cart.clear()
			return redirect(url_for('auth.success'))
		
		except:
			flash('Something went wrong dumbass. Buy my friends better...', category='error')
			return redirect(url_for('auth.checkout'))
		
	return render_template('checkout.html')

@auth.route('/success')
def success():
	return render_template('auth/parts/success.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))
