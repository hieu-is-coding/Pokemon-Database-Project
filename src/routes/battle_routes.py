from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models import db
from src.models.battle import Battle
from src.models.pokemon import Pokemon
from src.models.region import Region
from sqlalchemy import text
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
@login_required
@admin_required
def new_battle_form():
    pokemons = db.session.execute(text('SELECT * FROM Pokemon ORDER BY name')).fetchall()
    regions = db.session.execute(text('SELECT * FROM Region ORDER BY region_name')).fetchall()
    return render_template('battles/new.html', pokemons=pokemons, regions=regions)

@battle_bp.route('/', methods=['POST'])
@login_required
@admin_required
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
        db.session.execute(text(
            '''INSERT INTO Battle 
               (trainer1_id, trainer2_id, winner_id, region_id) 
               VALUES (:trainer1_id, :trainer2_id, :winner_id, :region_id)'''),
            {'trainer1_id': trainer1_id, 'trainer2_id': trainer2_id, 
             'winner_id': winner_id, 'region_id': region_id}
        )
        db.session.commit()
        flash('Battle recorded successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error recording battle: {str(e)}', 'danger')
    
    return redirect(url_for('battle.get_all_battles'))

@battle_bp.route('/<int:battle_id>/edit', methods=['GET'])
@login_required
@admin_required
def edit_battle_form(battle_id):
    battle = Battle.query.get_or_404(battle_id)
    pokemons = Pokemon.query.all()
    regions = Region.query.all()
    return render_template('battles/edit.html', battle=battle, pokemons=pokemons, regions=regions)

@battle_bp.route('/<int:battle_id>', methods=['POST'])
@login_required
@admin_required
def update_battle(battle_id):
    trainer1_id = request.form.get('trainer1_id')
    trainer2_id = request.form.get('trainer2_id')
    winner_id = request.form.get('winner_id')
    region_id = request.form.get('region_id') or None
    
    if not trainer1_id or not trainer2_id or not winner_id:
        flash('Both Pokemon and winner must be selected', 'danger')
        return redirect(url_for('battle.edit_battle_form', battle_id=battle_id))
    
    # Validate that winner is one of the participants
    if winner_id != trainer1_id and winner_id != trainer2_id:
        flash('Winner must be one of the participating Pokemon', 'danger')
        return redirect(url_for('battle.edit_battle_form', battle_id=battle_id))
    
    try:
        # Update battle using raw SQL
        db.session.execute(text(
            '''UPDATE Battle 
               SET trainer1_id = :trainer1_id, 
                   trainer2_id = :trainer2_id, 
                   winner_id = :winner_id, 
                   region_id = :region_id
               WHERE battle_id = :id'''),
            {'trainer1_id': trainer1_id, 'trainer2_id': trainer2_id, 
             'winner_id': winner_id, 'region_id': region_id, 'id': battle_id}
        )
        db.session.commit()
        flash('Battle updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating battle: {str(e)}', 'danger')
    
    return redirect(url_for('battle.get_battle', battle_id=battle_id))

@battle_bp.route('/<int:battle_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_battle(battle_id):
    try:
        # Delete battle using raw SQL
        db.session.execute(text('DELETE FROM Battle WHERE battle_id = :id'), {'id': battle_id})
        db.session.commit()
        flash('Battle deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting battle: {str(e)}', 'danger')
    
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
