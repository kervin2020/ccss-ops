from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Client

bp = Blueprint('clients', __name__, url_prefix='/api/clients')

def _date(value, field):
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:
        raise ValueError(f"Invalid date for {field}") from exc


@bp.route('', methods=['GET'])
@jwt_required()
def get_clients():
    status = request.args.get('status')
    query = Client.query

    if status:
        query = query.filter_by(contract_status=status)

    city = request.args.get('city')
    if city:
        query = query.filter(Client.city == city)

    is_active = request.args.get('is_active')
    if is_active is not None:
        query = query.filter_by(is_active=is_active.lower() == 'true')

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
    data = request.get_json() or {}

    required_fields = ['company_name', 'primary_contact_name', 'primary_contact_phone',
                       'primary_contact_email', 'address', 'city', 'contract_start_date']
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        contract_start = _date(data.get('contract_start_date'), 'contract_start_date')
        contract_end = _date(data.get('contract_end_date'), 'contract_end_date')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    client = Client(
        company_name=data['company_name'],
        company_registration_number=data.get('company_registration_number'),
        tax_id=data.get('tax_id'),
        industry_sector=data.get('industry_sector'),
        primary_contact_name=data['primary_contact_name'],
        primary_contact_title=data.get('primary_contact_title'),
        primary_contact_phone=data['primary_contact_phone'],
        primary_contact_email=data['primary_contact_email'],
        billing_contact_name=data.get('billing_contact_name'),
        billing_contact_phone=data.get('billing_contact_phone'),
        billing_contact_email=data.get('billing_contact_email'),
        address=data['address'],
        city=data['city'],
        postal_code=data.get('postal_code'),
        country=data.get('country', 'Haiti'),
        contract_start_date=contract_start,
        contract_end_date=contract_end,
        contract_status=data.get('contract_status', 'active'),
        payment_terms=data.get('payment_terms', '30_days'),
        billing_frequency=data.get('billing_frequency', 'monthly'),
        billing_day=data.get('billing_day'),
        currency=data.get('currency', 'HTG'),
        credit_limit=data.get('credit_limit', 0),
        current_balance=data.get('current_balance', 0),
        total_invoiced=data.get('total_invoiced', 0),
        total_paid=data.get('total_paid', 0),
        discount_percentage=data.get('discount_percentage', 0),
        service_level_agreement=data.get('service_level_agreement'),
        special_requirements=data.get('special_requirements'),
        requires_background_check=data.get('requires_background_check', False),
        requires_drug_testing=data.get('requires_drug_testing', False),
        insurance_certificate_required=data.get('insurance_certificate_required', False),
        preferred_communication_method=data.get('preferred_communication_method', 'email'),
        logo_url=data.get('logo_url'),
        website=data.get('website'),
        notes=data.get('notes'),
        is_active=data.get('is_active', True)
    )

    db.session.add(client)
    db.session.commit()

    return jsonify(client.to_dict()), 201

@bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json() or {}

    date_fields = ['contract_start_date', 'contract_end_date']
    for field in date_fields:
        if field in data:
            try:
                setattr(client, field, _date(data[field], field))
            except ValueError as exc:
                return jsonify({'error': str(exc)}), 400

    simple_fields = [
        'company_name', 'company_registration_number', 'tax_id', 'industry_sector',
        'primary_contact_name', 'primary_contact_title', 'primary_contact_phone',
        'primary_contact_email', 'billing_contact_name', 'billing_contact_phone',
        'billing_contact_email', 'address', 'city', 'postal_code', 'country',
        'contract_status', 'payment_terms', 'billing_frequency', 'billing_day', 'currency',
        'credit_limit', 'current_balance', 'total_invoiced', 'total_paid',
        'discount_percentage', 'service_level_agreement', 'special_requirements',
        'requires_background_check', 'requires_drug_testing', 'insurance_certificate_required',
        'preferred_communication_method', 'logo_url', 'website', 'notes', 'is_active'
    ]

    for field in simple_fields:
        if field in data:
            setattr(client, field, data[field])

    db.session.commit()
    return jsonify(client.to_dict()), 200

@bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    client.is_active = False
    db.session.commit()
    return jsonify({'message': 'Client deactivated'}), 200

