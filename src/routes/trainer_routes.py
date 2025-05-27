from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models import db
from src.models.trainer import Trainer
from src.models.region import Region
from flask_login import login_required, current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.has_role('admin'):
            flash('You do not have permission to access this page.', 'danger')
            return redirect(request.referrer or url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

trainer_bp = Blueprint('trainer', __name__, url_prefix='/trainers')

@trainer_bp.route('/', methods=['GET'])
def get_all_trainers():
    trainers = Trainer.query.all()
    return render_template('trainers/index.html', trainers=trainers)

@trainer_bp.route('/<int:trainer_id>', methods=['GET'])
def get_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    return render_template('trainers/detail.html', trainer=trainer)

@trainer_bp.route('/new', methods=['GET'])
@login_required
@admin_required
def new_trainer_form():
    regions = Region.query.all()
    return render_template('trainers/new.html', regions=regions)

@trainer_bp.route('/', methods=['POST'])
@login_required
@admin_required
def create_trainer():
    trainer_name = request.form.get('trainer_name')
    trainer_level = request.form.get('trainer_level')
    region_id = request.form.get('region_id')
    
    if not trainer_name or not trainer_level:
        flash('Trainer name and level are required', 'error')
        return redirect(url_for('trainer.new_trainer_form'))
    
    try:
        trainer_level = int(trainer_level)
        if trainer_level <= 0:
            flash('Trainer level must be a positive number', 'error')
            return redirect(url_for('trainer.new_trainer_form'))
    except ValueError:
        flash('Trainer level must be a valid number', 'error')
        return redirect(url_for('trainer.new_trainer_form'))
    
    new_trainer = Trainer(
        trainer_name=trainer_name,
        trainer_level=trainer_level,
        region_id=region_id if region_id else None
    )
    
    db.session.add(new_trainer)
    
    try:
        db.session.commit()
        flash('Trainer created successfully', 'success')
        return redirect(url_for('trainer.get_all_trainers'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating trainer: {str(e)}', 'error')
        return redirect(url_for('trainer.new_trainer_form'))

@trainer_bp.route('/<int:trainer_id>/edit', methods=['GET'])
@login_required
@admin_required
def edit_trainer_form(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    regions = Region.query.all()
    return render_template('trainers/edit.html', trainer=trainer, regions=regions)

@trainer_bp.route('/<int:trainer_id>', methods=['POST'])
@login_required
@admin_required
def update_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    
    trainer_name = request.form.get('trainer_name')
    trainer_level = request.form.get('trainer_level')
    region_id = request.form.get('region_id')
    
    if not trainer_name or not trainer_level:
        flash('Trainer name and level are required', 'error')
        return redirect(url_for('trainer.edit_trainer_form', trainer_id=trainer_id))
    
    try:
        trainer_level = int(trainer_level)
        if trainer_level <= 0:
            flash('Trainer level must be a positive number', 'error')
            return redirect(url_for('trainer.edit_trainer_form', trainer_id=trainer_id))
    except ValueError:
        flash('Trainer level must be a valid number', 'error')
        return redirect(url_for('trainer.edit_trainer_form', trainer_id=trainer_id))
    
    trainer.trainer_name = trainer_name
    trainer.trainer_level = trainer_level
    trainer.region_id = region_id if region_id else None
    
    try:
        db.session.commit()
        flash('Trainer updated successfully', 'success')
        return redirect(url_for('trainer.get_all_trainers'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating trainer: {str(e)}', 'error')
        return redirect(url_for('trainer.edit_trainer_form', trainer_id=trainer_id))

@trainer_bp.route('/<int:trainer_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    
    try:
        db.session.delete(trainer)
        db.session.commit()
        flash('Trainer deleted successfully', 'success')
        return redirect(url_for('trainer.get_all_trainers'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting trainer: {str(e)}', 'error')
        return redirect(url_for('trainer.get_all_trainers'))

@trainer_bp.route('/search', methods=['GET'])
def search_trainers():
    search_term = request.args.get('q', '')
    region_id = request.args.get('region_id')
    
    query = Trainer.query
    
    if search_term:
        query = query.filter(Trainer.trainer_name.ilike(f'%{search_term}%'))
    
    if region_id:
        query = query.filter(Trainer.region_id == region_id)
    
    trainers = query.all()
    regions = Region.query.all()
    
    return render_template('trainers/index.html', trainers=trainers, regions=regions, 
                          search_term=search_term, selected_region=region_id)
