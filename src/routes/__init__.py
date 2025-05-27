from flask import Blueprint

from src.routes.region_routes import region_bp
from src.routes.trainer_routes import trainer_bp
from src.routes.ability_routes import ability_bp
from src.routes.pokemon_routes import pokemon_bp
from src.routes.battle_routes import battle_bp
from src.routes.admin_routes import admin_bp

def register_blueprints(app):
    app.register_blueprint(region_bp)
    app.register_blueprint(trainer_bp)
    app.register_blueprint(ability_bp)
    app.register_blueprint(pokemon_bp)
    app.register_blueprint(battle_bp)
    app.register_blueprint(admin_bp)
