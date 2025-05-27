from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models import db
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

region_bp = Blueprint('region', __name__, url_prefix='/regions')

@region_bp.route('/', methods=['GET'])
def get_all_regions():
    regions = Region.query.all()
    return render_template('regions/index.html', regions=regions)

@region_bp.route('/<int:region_id>', methods=['GET'])
def get_region(region_id):
    region = Region.query.get_or_404(region_id)
    return render_template('regions/detail.html', region=region)

@region_bp.route('/new', methods=['GET'])
@login_required
@admin_required
def new_region_form():
    return render_template('regions/new.html')

@region_bp.route('/', methods=['POST'])
@login_required
@admin_required
def create_region():
    region_name = request.form.get('region_name')
    
    if not region_name:
        flash('Region name is required', 'error')
        return redirect(url_for('region.new_region_form'))
    
    existing_region = Region.query.filter_by(region_name=region_name).first()
    if existing_region:
        flash('Region with this name already exists', 'error')
        return redirect(url_for('region.new_region_form'))
    
    new_region = Region(region_name=region_name)
    db.session.add(new_region)
    
    try:
        db.session.commit()
        flash('Region created successfully', 'success')
        return redirect(url_for('region.get_all_regions'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating region: {str(e)}', 'error')
        return redirect(url_for('region.new_region_form'))

@region_bp.route('/<int:region_id>/edit', methods=['GET'])
@login_required
@admin_required
def edit_region_form(region_id):
    region = Region.query.get_or_404(region_id)
    return render_template('regions/edit.html', region=region)

@region_bp.route('/<int:region_id>', methods=['POST'])
def update_region(region_id):
    region = Region.query.get_or_404(region_id)
    region_name = request.form.get('region_name')
    
    if not region_name:
        flash('Region name is required', 'error')
        return redirect(url_for('region.edit_region_form', region_id=region_id))
    
    existing_region = Region.query.filter(Region.region_name == region_name, Region.region_id != region_id).first()
    if existing_region:
        flash('Region with this name already exists', 'error')
        return redirect(url_for('region.edit_region_form', region_id=region_id))
    
    region.region_name = region_name
    
    try:
        db.session.commit()
        flash('Region updated successfully', 'success')
        return redirect(url_for('region.get_all_regions'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating region: {str(e)}', 'error')
        return redirect(url_for('region.edit_region_form', region_id=region_id))

@region_bp.route('/<int:region_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_region(region_id):
    region = Region.query.get_or_404(region_id)
    
    try:
        db.session.delete(region)
        db.session.commit()
        flash('Region deleted successfully', 'success')
        return redirect(url_for('region.get_all_regions'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting region: {str(e)}', 'error')
        return redirect(url_for('region.get_all_regions'))

@region_bp.route('/search', methods=['GET'])
def search_regions():
    search_term = request.args.get('q', '')
    regions = Region.query.filter(Region.region_name.ilike(f'%{search_term}%')).all()
    return render_template('regions/index.html', regions=regions, search_term=search_term)
