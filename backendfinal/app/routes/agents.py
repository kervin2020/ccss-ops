from datetime import datetime, date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Agent

bp = Blueprint('agents', __name__, url_prefix='/api/agents')

def _parse_date(value, field_name):
    if not value:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:  # pragma: no cover - formatting guard
        raise ValueError(f"Invalid date format for {field_name}. Expected ISO string.") from exc


def _parse_float(value, field_name):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value for {field_name}.") from exc


@bp.route('', methods=['GET'])
@jwt_required()
def get_agents():
    status = request.args.get('status') or request.args.get('employment_status')
    query = Agent.query

    if status:
        query = query.filter_by(employment_status=status)

    is_active = request.args.get('is_active')
    if is_active is not None:
        query = query.filter_by(is_active=is_active.lower() == 'true')

    agents = query.all()
    return jsonify([agent.to_dict() for agent in agents]), 200

@bp.route('/<int:agent_id>', methods=['GET'])
@jwt_required()
def get_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    return jsonify(agent.to_dict()), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_agent():
    data = request.get_json() or {}

    employee_code = data.get('employee_code') or data.get('cin')
    first_name = data.get('first_name') or data.get('name')
    last_name = data.get('last_name') or data.get('surname')
    national_id = data.get('national_id') or data.get('cin')

    missing = [field for field, value in {
        'employee_code': employee_code,
        'first_name': first_name,
        'last_name': last_name,
        'hourly_rate': data.get('hourly_rate'),
        'phone_primary': data.get('phone_primary') or data.get('phone'),
        'date_of_birth': data.get('date_of_birth'),
        'hire_date': data.get('hire_date')
    }.items() if value in (None, '')]

    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    if Agent.query.filter_by(employee_code=employee_code).first():
        return jsonify({'error': 'Employee code already exists'}), 400

    if national_id and Agent.query.filter_by(national_id=national_id).first():
        return jsonify({'error': 'National ID already exists'}), 400

    try:
        date_of_birth = _parse_date(data.get('date_of_birth'), 'date_of_birth')
        hire_date = _parse_date(data.get('hire_date'), 'hire_date')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    try:
        hourly_rate = _parse_float(data.get('hourly_rate'), 'hourly_rate')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    agent = Agent(
        employee_code=employee_code,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=data.get('gender'),
        national_id=national_id,
        phone_primary=data.get('phone_primary') or data.get('phone'),
        phone_secondary=data.get('phone_secondary'),
        email=data.get('email'),
        address=data.get('address'),
        city=data.get('city'),
        postal_code=data.get('postal_code'),
        emergency_contact_name=data.get('emergency_contact_name'),
        emergency_contact_phone=data.get('emergency_contact_phone'),
        emergency_contact_relationship=data.get('emergency_contact_relationship'),
        hire_date=hire_date,
        contract_type=data.get('contract_type'),
        contract_end_date=_parse_date(data.get('contract_end_date'), 'contract_end_date') if data.get('contract_end_date') else None,
        employment_status=data.get('employment_status', 'active'),
        hourly_rate=hourly_rate,
        bank_name=data.get('bank_name'),
        bank_account_number=data.get('bank_account_number'),
        tax_id=data.get('tax_id'),
        uniform_size=data.get('uniform_size'),
        badge_number=data.get('badge_number'),
        security_clearance_level=data.get('security_clearance_level'),
        has_firearm_license=data.get('has_firearm_license', False),
        firearm_license_number=data.get('firearm_license_number'),
        firearm_license_expiry=_parse_date(data.get('firearm_license_expiry'), 'firearm_license_expiry') if data.get('firearm_license_expiry') else None,
        blood_type=data.get('blood_type'),
        has_drivers_license=data.get('has_drivers_license', False),
        drivers_license_number=data.get('drivers_license_number'),
        languages_spoken=data.get('languages_spoken'),
        medical_conditions=data.get('medical_conditions'),
        training_level=data.get('training_level'),
        profile_photo=data.get('profile_photo'),
        notes=data.get('notes'),
        is_active=data.get('is_active', True)
    )

    db.session.add(agent)
    db.session.commit()

    return jsonify(agent.to_dict()), 201

@bp.route('/<int:agent_id>', methods=['PUT'])
@jwt_required()
def update_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json() or {}

    new_employee_code = data.get('employee_code')
    if new_employee_code and new_employee_code != agent.employee_code:
        if Agent.query.filter_by(employee_code=new_employee_code).first():
            return jsonify({'error': 'Employee code already exists'}), 400
        agent.employee_code = new_employee_code

    new_national_id = data.get('national_id')
    if new_national_id and new_national_id != agent.national_id:
        if Agent.query.filter_by(national_id=new_national_id).first():
            return jsonify({'error': 'National ID already exists'}), 400
        agent.national_id = new_national_id

    date_fields = {
        'date_of_birth': 'date_of_birth',
        'hire_date': 'hire_date',
        'contract_end_date': 'contract_end_date',
        'termination_date': 'termination_date',
        'firearm_license_expiry': 'firearm_license_expiry'
    }

    for json_field, attr in date_fields.items():
        if json_field in data:
            try:
                setattr(agent, attr, _parse_date(data.get(json_field), json_field))
            except ValueError as exc:
                return jsonify({'error': str(exc)}), 400

    numeric_fields = ['hourly_rate', 'security_clearance_level']
    for field in numeric_fields:
        if field in data and data[field] is not None:
            try:
                setattr(agent, field, _parse_float(data[field], field))
            except ValueError as exc:
                return jsonify({'error': str(exc)}), 400

    mapped_fields = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'gender': 'gender',
        'phone_primary': 'phone_primary',
        'phone_secondary': 'phone_secondary',
        'email': 'email',
        'address': 'address',
        'city': 'city',
        'postal_code': 'postal_code',
        'emergency_contact_name': 'emergency_contact_name',
        'emergency_contact_phone': 'emergency_contact_phone',
        'emergency_contact_relationship': 'emergency_contact_relationship',
        'contract_type': 'contract_type',
        'employment_status': 'employment_status',
        'termination_reason': 'termination_reason',
        'bank_name': 'bank_name',
        'bank_account_number': 'bank_account_number',
        'tax_id': 'tax_id',
        'uniform_size': 'uniform_size',
        'badge_number': 'badge_number',
        'has_firearm_license': 'has_firearm_license',
        'blood_type': 'blood_type',
        'has_drivers_license': 'has_drivers_license',
        'drivers_license_number': 'drivers_license_number',
        'languages_spoken': 'languages_spoken',
        'medical_conditions': 'medical_conditions',
        'training_level': 'training_level',
        'profile_photo': 'profile_photo',
        'notes': 'notes',
        'is_active': 'is_active'
    }

    for json_field, attr in mapped_fields.items():
        if json_field in data:
            setattr(agent, attr, data.get(json_field))

    db.session.commit()
    return jsonify(agent.to_dict()), 200

@bp.route('/<int:agent_id>', methods=['DELETE'])
@jwt_required()
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    agent.employment_status = 'inactive'
    agent.is_active = False
    db.session.commit()
    return jsonify({'message': 'Agent deactivated'}), 200

