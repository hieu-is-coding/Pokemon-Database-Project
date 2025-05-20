from src.models import db

class Trainer(db.Model):
    __tablename__ = 'trainer'
    
    trainer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_name = db.Column(db.String(100), nullable=False)
    trainer_level = db.Column(db.Integer, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'))
    
    # Relationships
    pokemons = db.relationship('Pokemon', backref='trainer', lazy=True)
    
    def __repr__(self):
        return f'<Trainer {self.trainer_name}>'
