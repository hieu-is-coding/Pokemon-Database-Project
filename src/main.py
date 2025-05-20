from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from src.models import db
from src.routes import register_blueprints

def create_app():
    app = Flask(__name__)
    
    # Configure the SQLAlchemy database
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'pokemon_db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key_for_pokemon_db')
    
    # Initialize the database
    db.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
