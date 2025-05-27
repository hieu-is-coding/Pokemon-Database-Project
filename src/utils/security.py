from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import current_app, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Hash a password using werkzeug's security functions
    """
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    """
    Verify a password against its hash
    """
    return check_password_hash(hashed_password, password)

def generate_token(user_id, role):
    """
    Generate a JWT token for authentication
    """
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """
    Verify a JWT token
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """
    Decorator to protect routes with JWT authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            payload = verify_token(token)
            if not payload:
                return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated 