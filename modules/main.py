#main/init
from flask_login import current_user
from flask import Blueprint, render_template, send_from_directory

from modules.models import Cord

main = Blueprint('main', __name__)

#routes homepage
@main.route('/')
def landing_page():
	#items = Item.query.all()
	cordproduct = Cord.query.all()
	if current_user.is_authenticated:
		return render_template('landing.html', name=current_user.username, cordproduct=cordproduct)
	else:
		return render_template('landing.html', cordproduct=cordproduct)

#route look/images
@main.route('/look/<path:filename>')
def images_files(filename):
	return send_from_directory('look', filename)

#static route for login css
@main.route('/static/css/<path:filename>')
def login_css(filename):
	return send_from_directory('static/css', filename)