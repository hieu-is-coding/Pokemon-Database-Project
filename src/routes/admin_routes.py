from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from src.models import db
from sqlalchemy import text
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.has_role('admin'):
            flash('You do not have permission to access this page.', 'danger')
            return redirect(request.referrer or url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    # Get basic statistics for the dashboard
    stats = db.session.execute(text('''
        SELECT 
            (SELECT COUNT(*) FROM Region) as region_count,
            (SELECT COUNT(*) FROM Trainer) as trainer_count,
            (SELECT COUNT(*) FROM Pokemon) as pokemon_count,
            (SELECT COUNT(*) FROM Ability) as ability_count,
            (SELECT COUNT(*) FROM Battle) as battle_count,
            (SELECT COUNT(*)-1 FROM User) as user_count
    ''')).fetchone()
    
    # Convert to dictionary using _mapping attribute
    stats_dict = stats._mapping
    
    return render_template('admin/dashboard.html', stats=stats_dict)

@admin_bp.route('/admin/logs')
@login_required
@admin_required
def view_logs():
    # Get audit logs using raw SQL
    logs_rows = db.session.execute(text('''
        SELECT * FROM pokemon_audit_log
        ORDER BY change_timestamp DESC
        LIMIT 100
    ''')).fetchall()
    
    # Convert to list of dictionaries using _mapping attribute
    logs = [row._mapping for row in logs_rows]
    
    return render_template('admin/logs.html', logs=logs)
