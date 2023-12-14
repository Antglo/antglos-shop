#main/init

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#init SQLAlchemy to use later
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #configure database sqlite
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/schema.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        from .modules.models import User
        db.create_all()
    
    #Blueprint for auth routes
    from .modules.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    #Blueprint for non-auth parts of app
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
