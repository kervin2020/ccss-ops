from flask import Blueprint, request, jsonify
from app import db
from app.models import Site
from flask_jwt_extended import jwt_required

bp = Blueprint('sites', __name__, url_prefix='/api/sites')

@bp.route('', methods=['GET'])
@jwt_required()
def get_sites():
    client_id = request.args.get('client_id')
    status = request.args.get('status')
    query = Site.query
    
    if client_id:
        query = query.filter_by(client_id=client_id)
    if status:
        query = query.filter_by(site_status=status)
    
    sites = query.all()
    return jsonify([site.to_dict() for site in sites]), 200

@bp.route('/<int:site_id>', methods=['GET'])
@jwt_required()
def get_site(site_id):
    site = Site.query.get_or_404(site_id)
    return jsonify(site.to_dict()), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_site():
    data = request.get_json()
    
    required_fields = ['client_id', 'site_name', 'address', 'required_agents']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    site = Site(
        client_id=data['client_id'],
        site_name=data['site_name'],
        site_code=data.get('site_code'),
        address=data['address'],
        city=data.get('city'),
        required_agents=data['required_agents'],
        site_status=data.get('site_status', 'active')
    )
    
    db.session.add(site)
    db.session.commit()
    
    return jsonify(site.to_dict()), 201

@bp.route('/<int:site_id>', methods=['PUT'])
@jwt_required()
def update_site(site_id):
    site = Site.query.get_or_404(site_id)
    data = request.get_json()
    
    site.site_name = data.get('site_name', site.site_name)
    site.site_code = data.get('site_code', site.site_code)
    site.address = data.get('address', site.address)
    site.city = data.get('city', site.city)
    site.required_agents = data.get('required_agents', site.required_agents)
    site.site_status = data.get('site_status', site.site_status)
    
    db.session.commit()
    return jsonify(site.to_dict()), 200

@bp.route('/<int:site_id>', methods=['DELETE'])
@jwt_required()
def delete_site(site_id):
    site = Site.query.get_or_404(site_id)
    site.site_status = 'inactive'
    db.session.commit()
    return jsonify({'message': 'Site deactivated'}), 200

