from datetime import datetime, time, date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Shift, Agent, Site, User

bp = Blueprint('shifts', __name__, url_prefix='/api/shifts')


def _parse_date(value, field):
    if not value:
        raise ValueError(f"{field} is required")
    if isinstance(value, date):
        return value
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:
        raise ValueError(f"Invalid date format for {field}") from exc


def _parse_time(value, field):
    if not value:
        raise ValueError(f"{field} is required")
    if isinstance(value, time):
        return value
    try:
        return time.fromisoformat(value)
    except ValueError:
        try:
            return datetime.strptime(value, '%H:%M').time()
        except ValueError as exc:  # pragma: no cover - guard
            raise ValueError(f"Invalid time format for {field}") from exc


def _current_user():
    user_id = get_jwt_identity()
    return User.query.get_or_404(user_id)


@bp.route('', methods=['GET'])
@jwt_required()
def list_shifts():
    site_id = request.args.get('site_id')
    agent_id = request.args.get('agent_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Shift.query
    if site_id:
        query = query.filter_by(site_id=site_id)
    if agent_id:
        query = query.filter_by(agent_id=agent_id)
    if start_date:
        query = query.filter(Shift.shift_date >= datetime.fromisoformat(start_date).date())
    if end_date:
        query = query.filter(Shift.shift_date <= datetime.fromisoformat(end_date).date())

    shifts = query.order_by(Shift.shift_date.asc()).all()
    return jsonify([shift.to_dict() for shift in shifts]), 200


@bp.route('/<int:shift_id>', methods=['GET'])
@jwt_required()
def get_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)
    return jsonify(shift.to_dict()), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_shift():
    user = _current_user()
    if user.role not in ('admin', 'manager', 'supervisor'):
        return jsonify({'error': 'Only admins/managers can create shifts'}), 403

    data = request.get_json() or {}
    required = ['site_id', 'agent_id', 'shift_date', 'scheduled_start_time', 'scheduled_end_time']
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    # ensure references exist
    Agent.query.get_or_404(data['agent_id'])
    Site.query.get_or_404(data['site_id'])

    try:
        shift_date = _parse_date(data['shift_date'], 'shift_date')
        start_time = _parse_time(data['scheduled_start_time'], 'scheduled_start_time')
        end_time = _parse_time(data['scheduled_end_time'], 'scheduled_end_time')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    shift = Shift(
        site_id=data['site_id'],
        agent_id=data['agent_id'],
        shift_date=shift_date,
        shift_type=data.get('shift_type'),
        scheduled_start_time=start_time,
        scheduled_end_time=end_time,
        scheduled_hours=data.get('scheduled_hours'),
        shift_status=data.get('shift_status', 'scheduled'),
        assigned_by=user.id,
        special_instructions=data.get('special_instructions'),
        required_equipment=data.get('required_equipment')
    )

    db.session.add(shift)
    db.session.commit()
    return jsonify(shift.to_dict()), 201


@bp.route('/<int:shift_id>', methods=['PUT'])
@jwt_required()
def update_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)
    user = _current_user()
    data = request.get_json() or {}

    is_operator = user.role == 'operator'
    if is_operator and not shift.operator_can_modify():
        return jsonify({'error': 'Operator already modified this shift. Please escalate to an admin.'}), 403

    if 'agent_id' in data and data['agent_id']:
        Agent.query.get_or_404(data['agent_id'])
        shift.agent_id = data['agent_id']
    if 'site_id' in data and data['site_id']:
        Site.query.get_or_404(data['site_id'])
        shift.site_id = data['site_id']

    if 'shift_date' in data and data['shift_date']:
        try:
            shift.shift_date = _parse_date(data['shift_date'], 'shift_date')
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400

    for field in ['shift_type', 'shift_status', 'special_instructions', 'required_equipment']:
        if field in data:
            setattr(shift, field, data[field])

    if 'scheduled_start_time' in data and data['scheduled_start_time']:
        try:
            shift.scheduled_start_time = _parse_time(data['scheduled_start_time'], 'scheduled_start_time')
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
    if 'scheduled_end_time' in data and data['scheduled_end_time']:
        try:
            shift.scheduled_end_time = _parse_time(data['scheduled_end_time'], 'scheduled_end_time')
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400

    if 'scheduled_hours' in data:
        shift.scheduled_hours = data.get('scheduled_hours')

    if is_operator:
        shift.increment_operator_change(
            user_id=user.id,
            reason=data.get('operator_reason', 'Operator adjustment')
        )
    else:
        shift.operator_changes = data.get('operator_changes', shift.operator_changes)

    db.session.commit()
    return jsonify(shift.to_dict()), 200


@bp.route('/<int:shift_id>/reset-operator-lock', methods=['POST'])
@jwt_required()
def reset_operator_lock(shift_id):
    """Allow admins to reset the operator change counter so another change can happen."""
    user = _current_user()
    if user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    shift = Shift.query.get_or_404(shift_id)
    shift.operator_changes = 0
    shift.operator_last_change_by = None
    shift.operator_last_change_at = None
    shift.operator_last_change_reason = None
    db.session.commit()
    return jsonify({'message': 'Operator change counter reset'}), 200


@bp.route('/<int:shift_id>', methods=['DELETE'])
@jwt_required()
def delete_shift(shift_id):
    user = _current_user()
    if user.role not in ('admin', 'manager'):
        return jsonify({'error': 'Only admins/managers can delete shifts'}), 403

    shift = Shift.query.get_or_404(shift_id)
    db.session.delete(shift)
    db.session.commit()
    return jsonify({'message': 'Shift deleted'}), 200

