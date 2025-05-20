from src.models import db
from datetime import datetime

class Battle(db.Model):
    __tablename__ = 'battle'
    
    battle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    battle_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    trainer1_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    trainer2_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'))
    
    def __repr__(self):
        return f'<Battle {self.battle_id}>'
