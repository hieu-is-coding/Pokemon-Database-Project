from src.models import db
from datetime import datetime

# Pokemon-Ability association table
pokemon_ability = db.Table('pokemon_ability',
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), primary_key=True),
    db.Column('ability_id', db.Integer, db.ForeignKey('ability.ability_id'), primary_key=True)
)

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.trainer_id'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    abilities = db.relationship('Ability', secondary=pokemon_ability, backref=db.backref('pokemons', lazy='dynamic'))
    battles_as_trainer1 = db.relationship('Battle', foreign_keys='Battle.trainer1_id', backref='trainer1_pokemon', lazy=True)
    battles_as_trainer2 = db.relationship('Battle', foreign_keys='Battle.trainer2_id', backref='trainer2_pokemon', lazy=True)
    battles_as_winner = db.relationship('Battle', foreign_keys='Battle.winner_id', backref='winner_pokemon', lazy=True)
    
    def __repr__(self):
        return f'<Pokemon {self.name}>'
