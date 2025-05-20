from src.models import db

class Region(db.Model):
    __tablename__ = 'region'
    
    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region_name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationships
    trainers = db.relationship('Trainer', backref='region', lazy=True)
    battles = db.relationship('Battle', backref='region', lazy=True)
    
    def __repr__(self):
        return f'<Region {self.region_name}>'
