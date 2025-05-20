from src.models import db

class Ability(db.Model):
    __tablename__ = 'ability'
    
    ability_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ability_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Ability {self.ability_name}>'
