#init_db.py

from app import db

#initialize the database
with app.app_context():
    db.create_all()