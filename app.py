from flask import Flask
from config import Config
from models import db, bcrypt, jwt
from routes.auth_routes import auth_bp
from routes.issue_routes import issue_bp
from routes.admin_routes import admin_bp
from flask_cors import CORS

app = Flask(_name_)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(issue_bp, url_prefix="/issues")
app.register_blueprint(admin_bp, url_prefix="/admin")

with app.app_context():
    db.create_all()

if _name_ == "_main_":
    app.run(debug=True)