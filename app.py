#app/init

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from moduledb import db

#configure database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/schema.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#create instance
app = Flask(__name__)

#routes homepage
@app.route('/')
def landing_page():
	items = Item.query.all()
	return render_template('landing.html')


#route login
@app.route('/login')
def login_page():
	return render_template('/auth/login.html')

#route look/images
@app.route('/look/<path:filename>')
def images_files(filename):
	return send_from_directory('look', filename)

#static route for login css
@app.route('/static/css/<path:filename>')
def login_css(filename):
	return send_from_directory('static/css', filename)

#flask reads file
with app.app_context():
	with open('db/schema.sql', 'r') as f:
		db.session.execute(f.read())
	db.session.commit()
