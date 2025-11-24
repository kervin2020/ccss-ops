from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Equipment, EquipmentAssignment, Agent

bp = Blueprint('equipment', __name__, url_prefix='/api/equipment')


def _date(value, field):
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:
        raise ValueError(f'Invalid date for {field}') from exc


@bp.route('', methods=['GET'])
@jwt_required()
def list_equipment():
    status = request.args.get('status')
    equipment_type = request.args.get('type')

    query = Equipment.query
    if status:
        query = query.filter_by(status=status)
    if equipment_type:
        query = query.filter_by(equipment_type=equipment_type)

    items = query.order_by(Equipment.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items]), 200


@bp.route('/<int:equipment_id>', methods=['GET'])
@jwt_required()
def get_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    data = equipment.to_dict()
    data['assignments'] = [assignment.to_dict() for assignment in equipment.assignments]
    return jsonify(data), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_equipment():
    data = request.get_json() or {}

    required = ['equipment_type', 'equipment_name']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    equipment = Equipment(
        equipment_type=data['equipment_type'],
        equipment_name=data['equipment_name'],
        serial_number=data.get('serial_number'),
        purchase_date=_date(data.get('purchase_date'), 'purchase_date'),
        purchase_cost=data.get('purchase_cost'),
        condition=data.get('condition'),
        status=data.get('status', 'available'),
        notes=data.get('notes')
    )

    db.session.add(equipment)
    db.session.commit()

    return jsonify(equipment.to_dict()), 201


@bp.route('/<int:equipment_id>', methods=['PUT'])
@jwt_required()
def update_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    data = request.get_json() or {}

    if 'purchase_date' in data:
        equipment.purchase_date = _date(data['purchase_date'], 'purchase_date')

    simple_fields = [
        'equipment_type', 'equipment_name', 'serial_number', 'purchase_cost',
        'condition', 'status', 'notes'
    ]
    for field in simple_fields:
        if field in data:
            setattr(equipment, field, data[field])

    db.session.commit()
    return jsonify(equipment.to_dict()), 200


@bp.route('/<int:equipment_id>', methods=['DELETE'])
@jwt_required()
def delete_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    db.session.delete(equipment)
    db.session.commit()
    return jsonify({'message': 'Equipment deleted'}), 200


@bp.route('/assignments', methods=['POST'])
@jwt_required()
def assign_equipment():
    data = request.get_json() or {}
    required = ['equipment_id', 'agent_id', 'assigned_date']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    equipment = Equipment.query.get_or_404(data['equipment_id'])
    Agent.query.get_or_404(data['agent_id'])

    assignment = EquipmentAssignment(
        equipment_id=equipment.id,
        agent_id=data['agent_id'],
        assigned_date=_date(data['assigned_date'], 'assigned_date'),
        return_date=_date(data.get('return_date'), 'return_date'),
        assignment_status=data.get('assignment_status', 'active'),
        return_condition=data.get('return_condition'),
        assigned_by=data.get('assigned_by')
    )

    equipment.status = 'assigned'

    db.session.add(assignment)
    db.session.commit()

    return jsonify(assignment.to_dict()), 201


@bp.route('/assignments/<int:assignment_id>', methods=['PUT'])
@jwt_required()
def update_assignment(assignment_id):
    assignment = EquipmentAssignment.query.get_or_404(assignment_id)
    data = request.get_json() or {}

    if 'return_date' in data:
        assignment.return_date = _date(data['return_date'], 'return_date')
        assignment.assignment_status = 'returned'

    simple_fields = ['assignment_status', 'return_condition']
    for field in simple_fields:
        if field in data:
            setattr(assignment, field, data[field])

    db.session.commit()
    return jsonify(assignment.to_dict()), 200

