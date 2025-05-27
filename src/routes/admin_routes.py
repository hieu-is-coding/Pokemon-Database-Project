from flask import Blueprint, render_template
from src.models import db
from sqlalchemy import text

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    # Get basic statistics for the dashboard
    stats = db.session.execute(text('''
        SELECT 
            (SELECT COUNT(*) FROM Region) as region_count,
            (SELECT COUNT(*) FROM Trainer) as trainer_count,
            (SELECT COUNT(*) FROM Pokemon) as pokemon_count,
            (SELECT COUNT(*) FROM Ability) as ability_count,
            (SELECT COUNT(*) FROM Battle) as battle_count
    ''')).fetchone()
    
    # Convert to dictionary using _mapping attribute
    stats_dict = stats._mapping
    
    return render_template('admin/dashboard.html', stats=stats_dict)

@admin_bp.route('/admin/logs')
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
