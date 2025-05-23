from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models import db
from src.models.pokemon import Pokemon
from src.models.trainer import Trainer
from src.models.ability import Ability

pokemon_bp = Blueprint('pokemon', __name__, url_prefix='/pokemons')

@pokemon_bp.route('/', methods=['GET'])
def get_all_pokemons():
    pokemons = Pokemon.query.all()
    return render_template('pokemons/index.html', pokemons=pokemons)

@pokemon_bp.route('/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    return render_template('pokemons/detail.html', pokemon=pokemon)

@pokemon_bp.route('/new', methods=['GET'])
def new_pokemon_form():
    trainers = Trainer.query.all()
    abilities = Ability.query.all()
    return render_template('pokemons/new.html', trainers=trainers, abilities=abilities)

@pokemon_bp.route('/', methods=['POST'])
def create_pokemon():
    name = request.form.get('name')
    hp = request.form.get('hp')
    attack = request.form.get('attack')
    defense = request.form.get('defense')
    trainer_id = request.form.get('trainer_id')
    ability_ids = request.form.getlist('ability_ids')
    
    if not name or not hp or not attack or not defense:
        flash('Name, HP, Attack, and Defense are required', 'error')
        return redirect(url_for('pokemon.new_pokemon_form'))
    
    try:
        hp = int(hp)
        attack = int(attack)
        defense = int(defense)
        
        if hp <= 0 or attack <= 0 or defense <= 0:
            flash('HP, Attack, and Defense must be positive numbers', 'error')
            return redirect(url_for('pokemon.new_pokemon_form'))
    except ValueError:
        flash('HP, Attack, and Defense must be valid numbers', 'error')
        return redirect(url_for('pokemon.new_pokemon_form'))
    
    existing_pokemon = Pokemon.query.filter_by(name=name).first()
    if existing_pokemon:
        flash('Pokemon with this name already exists', 'error')
        return redirect(url_for('pokemon.new_pokemon_form'))
    
    new_pokemon = Pokemon(
        name=name,
        hp=hp,
        attack=attack,
        defense=defense,
        trainer_id=trainer_id if trainer_id else None
    )
    
    if ability_ids:
        abilities = Ability.query.filter(Ability.ability_id.in_(ability_ids)).all()
        new_pokemon.abilities = abilities
    
    db.session.add(new_pokemon)
    
    try:
        db.session.commit()
        flash('Pokemon created successfully', 'success')
        return redirect(url_for('pokemon.get_all_pokemons'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating Pokemon: {str(e)}', 'error')
        return redirect(url_for('pokemon.new_pokemon_form'))

@pokemon_bp.route('/<int:pokemon_id>/edit', methods=['GET'])
def edit_pokemon_form(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    trainers = Trainer.query.all()
    abilities = Ability.query.all()
    return render_template('pokemons/edit.html', pokemon=pokemon, trainers=trainers, abilities=abilities)

@pokemon_bp.route('/<int:pokemon_id>', methods=['POST'])
def update_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    
    name = request.form.get('name')
    hp = request.form.get('hp')
    attack = request.form.get('attack')
    defense = request.form.get('defense')
    trainer_id = request.form.get('trainer_id')
    ability_ids = request.form.getlist('ability_ids')
    
    if not name or not hp or not attack or not defense:
        flash('Name, HP, Attack, and Defense are required', 'error')
        return redirect(url_for('pokemon.edit_pokemon_form', pokemon_id=pokemon_id))
    
    try:
        hp = int(hp)
        attack = int(attack)
        defense = int(defense)
        
        if hp <= 0 or attack <= 0 or defense <= 0:
            flash('HP, Attack, and Defense must be positive numbers', 'error')
            return redirect(url_for('pokemon.edit_pokemon_form', pokemon_id=pokemon_id))
    except ValueError:
        flash('HP, Attack, and Defense must be valid numbers', 'error')
        return redirect(url_for('pokemon.edit_pokemon_form', pokemon_id=pokemon_id))
    
    existing_pokemon = Pokemon.query.filter(Pokemon.name == name, Pokemon.id != pokemon_id).first()
    if existing_pokemon:
        flash('Pokemon with this name already exists', 'error')
        return redirect(url_for('pokemon.edit_pokemon_form', pokemon_id=pokemon_id))
    
    pokemon.name = name
    pokemon.hp = hp
    pokemon.attack = attack
    pokemon.defense = defense
    pokemon.trainer_id = trainer_id if trainer_id else None
    
    if ability_ids:
        abilities = Ability.query.filter(Ability.ability_id.in_(ability_ids)).all()
        pokemon.abilities = abilities
    else:
        pokemon.abilities = []
    
    try:
        db.session.commit()
        flash('Pokemon updated successfully', 'success')
        return redirect(url_for('pokemon.get_all_pokemons'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating Pokemon: {str(e)}', 'error')
        return redirect(url_for('pokemon.edit_pokemon_form', pokemon_id=pokemon_id))

@pokemon_bp.route('/<int:pokemon_id>/delete', methods=['POST'])
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    
    try:
        db.session.delete(pokemon)
        db.session.commit()
        flash('Pokemon deleted successfully', 'success')
        return redirect(url_for('pokemon.get_all_pokemons'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting Pokemon: {str(e)}', 'error')
        return redirect(url_for('pokemon.get_all_pokemons'))

@pokemon_bp.route('/search', methods=['GET'])
def search_pokemons():
    search_term = request.args.get('q', '')
    trainer_id = request.args.get('trainer_id')
    ability_id = request.args.get('ability_id')
    
    query = Pokemon.query
    
    if search_term:
        query = query.filter(Pokemon.name.ilike(f'%{search_term}%'))
    
    if trainer_id:
        query = query.filter(Pokemon.trainer_id == trainer_id)
    
    if ability_id:
        query = query.join(Pokemon.abilities).filter(Ability.ability_id == ability_id)
    
    pokemons = query.all()
    trainers = Trainer.query.all()
    abilities = Ability.query.all()
    
    return render_template('pokemons/index.html', pokemons=pokemons, trainers=trainers, 
                          abilities=abilities, search_term=search_term, 
                          selected_trainer=trainer_id, selected_ability=ability_id)
