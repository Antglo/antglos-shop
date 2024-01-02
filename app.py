import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
import click

#init SQLAlchemy to use later
db = SQLAlchemy()

def create_app():
    global app
    app = Flask(__name__)
    
    #configure database sqlite
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'db/schema.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    #Create the login manager for user sessions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_page' #Tells login manager where to start session
    login_manager.init_app(app)
    

    with app.app_context():
        db.create_all()

    #user_loader creates/checks callbacks for user session in relation to the users ID
    from modules.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #create superusers from CLI
    @click.command(name="createsuperuser")
    @with_appcontext
    @click.argument("username", nargs=1)
    @click.argument("password", nargs=1)
    def create_superuser(username, password):
        '''Using click use the arguments to create a superuser'''
        user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), is_superuser=True)
        db.session.add(user)
        db.session.commit()
    app.cli.add_command(create_superuser)

    #Blueprint for admin
    from modules.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    #Blueprint for auth routes
    from modules.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    #Blueprint for non-auth parts of app
    from modules.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    #Blueprint for basket API/shopping basket
    # from modules.basket import basket as shopping_basket
    # app.register_blueprint(shopping_basket)
    
    return app