import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#init SQLAlchemy to use later
db = SQLAlchemy()

def create_app():
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
        from modules.models import User
        db.create_all()
    #user_loader creates/checks callbacks for user session in relation to the users ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #Blueprint for auth routes
    from modules.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    #Blueprint for non-auth parts of app
    from modules.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app