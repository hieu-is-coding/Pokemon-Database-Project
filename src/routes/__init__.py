from flask import Flask, render_template
from flask_login import LoginManager
from src.models import db
from src.models.user import User
from sqlalchemy import text
import os

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_blueprints(app):
    # Register blueprints
    from src.routes.region_routes import region_bp
    from src.routes.trainer_routes import trainer_bp
    from src.routes.ability_routes import ability_bp
    from src.routes.pokemon_routes import pokemon_bp
    from src.routes.battle_routes import battle_bp
    from src.routes.admin_routes import admin_bp
    from src.routes.auth_routes import auth_bp
    
    app.register_blueprint(region_bp)
    app.register_blueprint(trainer_bp)
    app.register_blueprint(ability_bp)
    app.register_blueprint(pokemon_bp)
    app.register_blueprint(battle_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_for_development')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'pokemon_db')}"
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app
