from src.models import db
from src.utils.security import hash_password, verify_password
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('User_Role.role_id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationship
    role = db.relationship('UserRole', backref='users')
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password_hash = hash_password(password)
    
    def check_password(self, password):
        return verify_password(password, self.password_hash)
    
    def has_role(self, role_name):
        return self.role.role_name == role_name
    
    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role_id': self.role_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserRole(db.Model):
    __tablename__ = 'User_Role'
    
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<User_role {self.role_name}>'

