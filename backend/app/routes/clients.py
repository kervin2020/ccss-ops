from flask import Blueprint, request, jsonify
from app import db
from app.models import Client
from flask_jwt_extended import jwt_required

bp = Blueprint('clients', __name__, url_prefix='/api/clients')

@bp.route('', methods=['GET'])
@jwt_required()
def get_clients():
    status = request.args.get('status')
    query = Client.query
    
    if status:
        query = query.filter_by(contract_status=status)
    
    clients = query.all()
    return jsonify([client.to_dict() for client in clients]), 200

@bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(client.to_dict()), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_client():
    data = request.get_json()
    
    required_fields = ['company_name', 'primary_contact_name', 'primary_contact_phone', 
                      'primary_contact_email', 'address', 'city']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    client = Client(
        company_name=data['company_name'],
        registration_number=data.get('registration_number'),
        primary_contact_name=data['primary_contact_name'],
        primary_contact_phone=data['primary_contact_phone'],
        primary_contact_email=data['primary_contact_email'],
        address=data['address'],
        city=data['city'],
        contract_status=data.get('contract_status', 'active')
    )
    
    db.session.add(client)
    db.session.commit()
    
    return jsonify(client.to_dict()), 201

@bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    
    client.company_name = data.get('company_name', client.company_name)
    client.registration_number = data.get('registration_number', client.registration_number)
    client.primary_contact_name = data.get('primary_contact_name', client.primary_contact_name)
    client.primary_contact_phone = data.get('primary_contact_phone', client.primary_contact_phone)
    client.primary_contact_email = data.get('primary_contact_email', client.primary_contact_email)
    client.address = data.get('address', client.address)
    client.city = data.get('city', client.city)
    client.contract_status = data.get('contract_status', client.contract_status)
    
    db.session.commit()
    return jsonify(client.to_dict()), 200

@bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    client.is_active = False
    db.session.commit()
    return jsonify({'message': 'Client deactivated'}), 200

