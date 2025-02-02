from flask import Flask
import os 

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'qwertyuiopzxcvbnmlkjhgfdsa')
    DEBUG = True

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  

    from .routes import main
    app.register_blueprint(main)

    return app

