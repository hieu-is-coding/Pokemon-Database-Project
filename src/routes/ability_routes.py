from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models import db
from src.models.ability import Ability
from sqlalchemy import text


ability_bp = Blueprint('ability', __name__, url_prefix='/abilities')

@ability_bp.route('/', methods=['GET'])
def get_all_abilities():
    abilities = db.session.execute(text('SELECT * FROM Ability ORDER BY ability_name')).fetchall()
    return render_template('abilities/index.html', abilities=abilities)

@ability_bp.route('/<int:ability_id>', methods=['GET'])
def get_ability(ability_id):
    ability = Ability.query.get_or_404(ability_id)
    return render_template('abilities/detail.html', ability=ability)

@ability_bp.route('/new', methods=['GET'])
def new_ability_form():
    return render_template('abilities/new.html')

@ability_bp.route('/abilities', methods=['POST'])
def create_ability():
    ability_name = request.form.get('ability_name')
    description = request.form.get('description')
    
    if not ability_name:
        flash('Ability name is required', 'danger')
        return redirect(url_for('ability.new_ability_form'))
    
    try:
        db.session.execute(text(
            'INSERT INTO Ability (ability_name, description) VALUES (:name, :description)'),
            {'name': ability_name, 'description': description}
        )
        db.session.commit()
        flash('Ability created successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating ability: {str(e)}', 'danger')
    
    return redirect(url_for('ability.get_all_abilities'))

@ability_bp.route('/<int:ability_id>/edit', methods=['GET'])
def edit_ability_form(ability_id):
    # Get ability by ID
    ability = db.session.execute(text('SELECT * FROM Ability WHERE ability_id = :id'), {'id': ability_id}).fetchone()
    
    if not ability:
        flash('Ability not found', 'danger')
        return redirect(url_for('ability.get_all_abilities'))
    
    return render_template('abilities/edit.html', ability=ability)

@ability_bp.route('/<int:ability_id>', methods=['POST'])
def update_ability(ability_id):
    ability_name = request.form.get('ability_name')
    description = request.form.get('description')
    
    if not ability_name:
        flash('Ability name is required', 'danger')
        return redirect(url_for('ability.edit_ability_form', ability_id=ability_id))
    
    try:
        # Update ability using raw SQL
        db.session.execute(text(
            'UPDATE Ability SET ability_name = :name, description = :description WHERE ability_id = :id'),
            {'name': ability_name, 'description': description, 'id': ability_id}
        )
        db.session.commit()
        flash('Ability updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating ability: {str(e)}', 'danger')
    
    return redirect(url_for('ability.get_ability', ability_id=ability_id))

@ability_bp.route('/<int:ability_id>/delete', methods=['POST'])
def delete_ability(ability_id):
    try:
        # Delete ability using raw SQL
        db.session.execute(text('DELETE FROM Ability WHERE ability_id = :id'), {'id': ability_id})
        db.session.commit()
        flash('Ability deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting ability: {str(e)}', 'danger')
    
    return redirect(url_for('ability.get_all_abilities'))

@ability_bp.route('/search', methods=['GET'])
def search_abilities():
    search_term = request.args.get('q', '')
    abilities = Ability.query.filter(
        Ability.ability_name.ilike(f'%{search_term}%') | 
        Ability.description.ilike(f'%{search_term}%')
    ).all()
    
    return render_template('abilities/index.html', abilities=abilities, search_term=search_term)
