from flask import Blueprint
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'login'
    
@auth.route('/register')
def register():
    return 'Register'

@auth.route('/logout')
def logout():
    return 'logout'
