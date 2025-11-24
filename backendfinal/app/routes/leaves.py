from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Leave, Agent

bp = Blueprint('leaves', __name__, url_prefix='/api/leaves')


def _date(value, field):
    if not value:
        raise ValueError(f'{field} is required')
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:
        raise ValueError(f'Invalid date for {field}') from exc


@bp.route('', methods=['GET'])
@jwt_required()
def list_leaves():
    agent_id = request.args.get('agent_id')
    status = request.args.get('status')

    query = Leave.query
    if agent_id:
        query = query.filter_by(agent_id=agent_id)
    if status:
        query = query.filter_by(leave_status=status)

    leaves = query.order_by(Leave.start_date.desc()).all()
    return jsonify([leave.to_dict() for leave in leaves]), 200


@bp.route('/<int:leave_id>', methods=['GET'])
@jwt_required()
def get_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    return jsonify(leave.to_dict()), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_leave():
    data = request.get_json() or {}

    required = ['agent_id', 'leave_type', 'start_date', 'end_date']
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    Agent.query.get_or_404(data['agent_id'])

    try:
        start_date = _date(data['start_date'], 'start_date')
        end_date = _date(data['end_date'], 'end_date')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    leave = Leave(
        agent_id=data['agent_id'],
        leave_type=data['leave_type'],
        start_date=start_date,
        end_date=end_date,
        reason=data.get('reason'),
        supporting_document=data.get('supporting_document'),
        leave_status='pending'
    )

    leave.calculate_days()
    db.session.add(leave)
    db.session.commit()

    return jsonify(leave.to_dict()), 201


@bp.route('/<int:leave_id>', methods=['PUT'])
@jwt_required()
def update_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    data = request.get_json() or {}

    if leave.leave_status != 'pending' and data.get('leave_status') not in (None, 'pending'):
        return jsonify({'error': 'Leave already processed'}), 400

    if 'start_date' in data:
        try:
            leave.start_date = _date(data['start_date'], 'start_date')
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
    if 'end_date' in data:
        try:
            leave.end_date = _date(data['end_date'], 'end_date')
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400

    simple_fields = [
        'leave_type', 'reason', 'supporting_document', 'leave_status',
        'review_notes', 'is_active'
    ]
    for field in simple_fields:
        if field in data:
            setattr(leave, field, data[field])

    if leave.start_date and leave.end_date:
        leave.calculate_days()

    db.session.commit()
    return jsonify(leave.to_dict()), 200


@bp.route('/<int:leave_id>/approve', methods=['POST'])
@jwt_required()
def approve_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    if leave.leave_status != 'pending':
        return jsonify({'error': 'Leave already processed'}), 400
    payload = request.get_json(silent=True) or {}
    leave.approve(get_jwt_identity(), payload.get('notes'))
    db.session.commit()
    return jsonify(leave.to_dict()), 200


@bp.route('/<int:leave_id>/reject', methods=['POST'])
@jwt_required()
def reject_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    if leave.leave_status != 'pending':
        return jsonify({'error': 'Leave already processed'}), 400
    payload = request.get_json(silent=True) or {}
    leave.reject(get_jwt_identity(), payload.get('notes', ''))
    db.session.commit()
    return jsonify(leave.to_dict()), 200


@bp.route('/<int:leave_id>', methods=['DELETE'])
@jwt_required()
def delete_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    db.session.delete(leave)
    db.session.commit()
    return jsonify({'message': 'Leave deleted'}), 200

