from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os






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
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql://root:6381!Root$$@localhost/clgissue')
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
        db.create_all()  
    


    
    return app
