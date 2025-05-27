from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from src.models import db
from src.models.user import User
from sqlalchemy import text

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            flash('Username or email already exists.', 'danger')
        else:
            # Create new user with 'viewer' role by default
            viewer_role = db.session.execute(text("SELECT role_id FROM User_Role WHERE role_name = 'viewer'")).fetchone()
            
            if viewer_role:
                new_user = User(username=username, email=email, role_id=viewer_role[0])
                new_user.set_password(password)
                
                db.session.add(new_user)
                db.session.commit()
                
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Error creating user: Role not found.', 'danger')
    
    return render_template('auth/register.html')
