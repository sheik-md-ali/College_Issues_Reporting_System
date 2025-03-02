from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import mysql.connector
from werkzeug.security import generate_password_hash

UPLOAD_FOLDER = "static/uploads"

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize database and login manager
db = SQLAlchemy()
login_manager = LoginManager()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'qwertyuiopzxcvbnmlkjhgfdsa')
    DEBUG = True
    DB_NAME = "clgissue"
    DB_USER = "root"
    DB_PASSWORD = "6381!Root$$"
    DB_HOST = "localhost"

    # Ensure database exists
    connection = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    connection.close()

    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config) 
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)  # Initialize database
    login_manager.init_app(app)  # Initialize login manager

    login_manager.login_view = "auth.login"  # Redirect unauthorized users to login page
    login_manager.login_message_category = "danger"

    from .models import User  # Import models after db init
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    from .auth import auth  # Import auth blueprint

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    
    with app.app_context():
        db.create_all()  # Create tables if not exist

        users_data = [
            {"name": "Admin User", "email": "admin@gmail.com", "password": "admin123", "role": "admin"},
            {"name": "Student User", "email": "student@gmail.com", "password": "student123", "role": "student"},
        ]

        for user_data in users_data:
            user = User.query.filter_by(email=user_data["email"]).first()
            hashed_password = generate_password_hash(user_data["password"], method="scrypt")

            if user:
                user.password_hash = hashed_password
                user.name = user_data["name"]  # Update name if user exists
            else:
                user = User(
                    name=user_data["name"],  
                    email=user_data["email"], 
                    password_hash=hashed_password, 
                    role=user_data["role"]
                )
                db.session.add(user)

        db.session.commit()

    return app
