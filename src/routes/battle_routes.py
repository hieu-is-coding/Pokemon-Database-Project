from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models import db
from src.models.battle import Battle
from src.models.pokemon import Pokemon
from src.models.region import Region

battle_bp = Blueprint('battle', __name__, url_prefix='/battles')

@battle_bp.route('/', methods=['GET'])
def get_all_battles():
    battles = Battle.query.all()
    return render_template('battles/index.html', battles=battles)

@battle_bp.route('/<int:battle_id>', methods=['GET'])
def get_battle(battle_id):
    battle = Battle.query.get_or_404(battle_id)
    return render_template('battles/detail.html', battle=battle)

@battle_bp.route('/new', methods=['GET'])
def new_battle_form():
    pokemons = Pokemon.query.all()
    regions = Region.query.all()
    return render_template('battles/new.html', pokemons=pokemons, regions=regions)

@battle_bp.route('/', methods=['POST'])
def create_battle():
    trainer1_id = request.form.get('trainer1_id')
    trainer2_id = request.form.get('trainer2_id')
    winner_id = request.form.get('winner_id')
    region_id = request.form.get('region_id')
    
    if not trainer1_id or not trainer2_id or not winner_id:
        flash('Both participating Pokemon and winner must be selected', 'error')
        return redirect(url_for('battle.new_battle_form'))
    
    if trainer1_id == trainer2_id:
        flash('The two participating Pokemon must be different', 'error')
        return redirect(url_for('battle.new_battle_form'))
    
    if winner_id != trainer1_id and winner_id != trainer2_id:
        flash('The winner must be one of the participating Pokemon', 'error')
        return redirect(url_for('battle.new_battle_form'))
    
    new_battle = Battle(
        trainer1_id=trainer1_id,
        trainer2_id=trainer2_id,
        winner_id=winner_id,
        region_id=region_id if region_id else None
    )
    
    db.session.add(new_battle)
    
    try:
        db.session.commit()
        flash('Battle created successfully', 'success')
        return redirect(url_for('battle.get_all_battles'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating battle: {str(e)}', 'error')
        return redirect(url_for('battle.new_battle_form'))

@battle_bp.route('/<int:battle_id>/edit', methods=['GET'])
def edit_battle_form(battle_id):
    battle = Battle.query.get_or_404(battle_id)
    pokemons = Pokemon.query.all()
    regions = Region.query.all()
    return render_template('battles/edit.html', battle=battle, pokemons=pokemons, regions=regions)

@battle_bp.route('/<int:battle_id>', methods=['POST'])
def update_battle(battle_id):
    battle = Battle.query.get_or_404(battle_id)
    
    trainer1_id = request.form.get('trainer1_id')
    trainer2_id = request.form.get('trainer2_id')
    winner_id = request.form.get('winner_id')
    region_id = request.form.get('region_id')
    
    if not trainer1_id or not trainer2_id or not winner_id:
        flash('Both participating Pokemon and winner must be selected', 'error')
        return redirect(url_for('battle.edit_battle_form', battle_id=battle_id))
    
    if trainer1_id == trainer2_id:
        flash('The two participating Pokemon must be different', 'error')
        return redirect(url_for('battle.edit_battle_form', battle_id=battle_id))
    
    if winner_id != trainer1_id and winner_id != trainer2_id:
        flash('The winner must be one of the participating Pokemon', 'error')
        return redirect(url_for('battle.edit_battle_form', battle_id=battle_id))
    
    battle.trainer1_id = trainer1_id
    battle.trainer2_id = trainer2_id
    battle.winner_id = winner_id
    battle.region_id = region_id if region_id else None
    
    try:
        db.session.commit()
        flash('Battle updated successfully', 'success')
        return redirect(url_for('battle.get_all_battles'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating battle: {str(e)}', 'error')
        return redirect(url_for('battle.edit_battle_form', battle_id=battle_id))

@battle_bp.route('/<int:battle_id>/delete', methods=['POST'])
def delete_battle(battle_id):
    battle = Battle.query.get_or_404(battle_id)
    
    try:
        db.session.delete(battle)
        db.session.commit()
        flash('Battle deleted successfully', 'success')
        return redirect(url_for('battle.get_all_battles'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting battle: {str(e)}', 'error')
        return redirect(url_for('battle.get_all_battles'))

@battle_bp.route('/search', methods=['GET'])
def search_battles():
    region_id = request.args.get('region_id')
    pokemon_id = request.args.get('pokemon_id')
    winner_id = request.args.get('winner_id')
    
    query = Battle.query
    
    if region_id:
        query = query.filter(Battle.region_id == region_id)
    
    if pokemon_id:
        query = query.filter((Battle.trainer1_id == pokemon_id) | (Battle.trainer2_id == pokemon_id))
    
    if winner_id:
        query = query.filter(Battle.winner_id == winner_id)
    
    battles = query.all()
    pokemons = Pokemon.query.all()
    regions = Region.query.all()
    
    return render_template('battles/index.html', battles=battles, pokemons=pokemons, 
                          regions=regions, selected_region=region_id, 
                          selected_pokemon=pokemon_id, selected_winner=winner_id)
