from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models import db
from src.models.ability import Ability

ability_bp = Blueprint('ability', __name__, url_prefix='/abilities')

@ability_bp.route('/', methods=['GET'])
def get_all_abilities():
    abilities = Ability.query.all()
    return render_template('abilities/index.html', abilities=abilities)

@ability_bp.route('/<int:ability_id>', methods=['GET'])
def get_ability(ability_id):
    ability = Ability.query.get_or_404(ability_id)
    return render_template('abilities/detail.html', ability=ability)

@ability_bp.route('/new', methods=['GET'])
def new_ability_form():
    return render_template('abilities/new.html')

@ability_bp.route('/', methods=['POST'])
def create_ability():
    ability_name = request.form.get('ability_name')
    description = request.form.get('description')
    
    if not ability_name:
        flash('Ability name is required', 'error')
        return redirect(url_for('ability.new_ability_form'))
    
    existing_ability = Ability.query.filter_by(ability_name=ability_name).first()
    if existing_ability:
        flash('Ability with this name already exists', 'error')
        return redirect(url_for('ability.new_ability_form'))
    
    new_ability = Ability(
        ability_name=ability_name,
        description=description
    )
    
    db.session.add(new_ability)
    
    try:
        db.session.commit()
        flash('Ability created successfully', 'success')
        return redirect(url_for('ability.get_all_abilities'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating ability: {str(e)}', 'error')
        return redirect(url_for('ability.new_ability_form'))

@ability_bp.route('/<int:ability_id>/edit', methods=['GET'])
def edit_ability_form(ability_id):
    ability = Ability.query.get_or_404(ability_id)
    return render_template('abilities/edit.html', ability=ability)

@ability_bp.route('/<int:ability_id>', methods=['POST'])
def update_ability(ability_id):
    ability = Ability.query.get_or_404(ability_id)
    
    ability_name = request.form.get('ability_name')
    description = request.form.get('description')
    
    if not ability_name:
        flash('Ability name is required', 'error')
        return redirect(url_for('ability.edit_ability_form', ability_id=ability_id))
    
    existing_ability = Ability.query.filter(Ability.ability_name == ability_name, Ability.ability_id != ability_id).first()
    if existing_ability:
        flash('Ability with this name already exists', 'error')
        return redirect(url_for('ability.edit_ability_form', ability_id=ability_id))
    
    ability.ability_name = ability_name
    ability.description = description
    
    try:
        db.session.commit()
        flash('Ability updated successfully', 'success')
        return redirect(url_for('ability.get_all_abilities'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating ability: {str(e)}', 'error')
        return redirect(url_for('ability.edit_ability_form', ability_id=ability_id))

@ability_bp.route('/<int:ability_id>/delete', methods=['POST'])
def delete_ability(ability_id):
    ability = Ability.query.get_or_404(ability_id)
    
    try:
        db.session.delete(ability)
        db.session.commit()
        flash('Ability deleted successfully', 'success')
        return redirect(url_for('ability.get_all_abilities'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting ability: {str(e)}', 'error')
        return redirect(url_for('ability.get_all_abilities'))

@ability_bp.route('/search', methods=['GET'])
def search_abilities():
    search_term = request.args.get('q', '')
    abilities = Ability.query.filter(
        Ability.ability_name.ilike(f'%{search_term}%') | 
        Ability.description.ilike(f'%{search_term}%')
    ).all()
    
    return render_template('abilities/index.html', abilities=abilities, search_term=search_term)
