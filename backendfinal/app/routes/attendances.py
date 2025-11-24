from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Attendance, Agent, Site, Shift

bp = Blueprint('attendances', __name__, url_prefix='/api/attendances')


def _date(value, field):
    if not value:
        raise ValueError(f'{field} is required')
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:
        raise ValueError(f'Invalid date format for {field}') from exc


def _dt(value, field):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f'Invalid datetime format for {field}') from exc


@bp.route('', methods=['GET'])
@jwt_required()
def get_attendances():
    agent_id = request.args.get('agent_id')
    site_id = request.args.get('site_id')
    shift_id = request.args.get('shift_id')
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Attendance.query

    if agent_id:
        query = query.filter_by(agent_id=agent_id)
    if site_id:
        query = query.filter_by(site_id=site_id)
    if shift_id:
        query = query.filter_by(shift_id=shift_id)
    if status:
        query = query.filter_by(attendance_status=status)
    if start_date:
        query = query.filter(Attendance.attendance_date >= datetime.fromisoformat(start_date).date())
    if end_date:
        query = query.filter(Attendance.attendance_date <= datetime.fromisoformat(end_date).date())

    attendances = query.order_by(Attendance.attendance_date.desc()).all()
    return jsonify([att.to_dict() for att in attendances]), 200


@bp.route('/<int:attendance_id>', methods=['GET'])
@jwt_required()
def get_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    return jsonify(attendance.to_dict()), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_attendance():
    data = request.get_json() or {}

    required_fields = ['agent_id', 'site_id', 'attendance_date']
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    Agent.query.get_or_404(data['agent_id'])
    Site.query.get_or_404(data['site_id'])

    shift_id = data.get('shift_id')
    if shift_id:
        shift = Shift.query.get_or_404(shift_id)
    else:
        shift = None

    try:
        attendance_date = _date(data['attendance_date'], 'attendance_date')
        clock_in_time = _dt(data.get('clock_in_time'), 'clock_in_time')
        clock_out_time = _dt(data.get('clock_out_time'), 'clock_out_time')
        break_start_time = _dt(data.get('break_start_time'), 'break_start_time')
        break_end_time = _dt(data.get('break_end_time'), 'break_end_time')
        payment_date = _dt(data.get('payment_date'), 'payment_date')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    attendance = Attendance(
        shift_id=shift_id,
        agent_id=data['agent_id'],
        site_id=data['site_id'],
        attendance_date=attendance_date,
        clock_in_time=clock_in_time,
        clock_out_time=clock_out_time,
        clock_in_method=data.get('clock_in_method'),
        clock_in_gps_lat=data.get('clock_in_gps_lat'),
        clock_in_gps_lng=data.get('clock_in_gps_lng'),
        clock_in_photo=data.get('clock_in_photo'),
        clock_in_verified=data.get('clock_in_verified', False),
        clock_out_method=data.get('clock_out_method'),
        clock_out_gps_lat=data.get('clock_out_gps_lat'),
        clock_out_gps_lng=data.get('clock_out_gps_lng'),
        clock_out_photo=data.get('clock_out_photo'),
        clock_out_verified=data.get('clock_out_verified', False),
        total_break_minutes=data.get('total_break_minutes', 0),
        break_start_time=break_start_time,
        break_end_time=break_end_time,
        attendance_status=data.get('attendance_status', 'present'),
        is_late=data.get('is_late', False),
        late_minutes=data.get('late_minutes', 0),
        early_departure=data.get('early_departure', False),
        early_departure_minutes=data.get('early_departure_minutes', 0),
        incident_reported=data.get('incident_reported', False),
        incident_description=data.get('incident_description'),
        supervisor_notes=data.get('supervisor_notes'),
        requires_correction=data.get('requires_correction', False),
        correction_reason=data.get('correction_reason'),
        device_id=data.get('device_id'),
        ip_address=data.get('ip_address'),
        attendance_signature=data.get('attendance_signature'),
        weather_condition=data.get('weather_condition'),
    )

    attendance.calculate_hours()

    if shift and not attendance.shift_id:
        attendance.shift_id = shift.id

    db.session.add(attendance)
    db.session.commit()

    return jsonify(attendance.to_dict()), 201


@bp.route('/<int:attendance_id>', methods=['PUT'])
@jwt_required()
def update_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    data = request.get_json() or {}

    for field in ['agent_id', 'site_id', 'shift_id']:
        if field in data and data[field]:
            if field == 'agent_id':
                Agent.query.get_or_404(data[field])
            if field == 'site_id':
                Site.query.get_or_404(data[field])
            if field == 'shift_id':
                Shift.query.get_or_404(data[field])
            setattr(attendance, field, data[field])

    try:
        if 'attendance_date' in data:
            attendance.attendance_date = _date(data['attendance_date'], 'attendance_date')
        if 'clock_in_time' in data:
            attendance.clock_in_time = _dt(data['clock_in_time'], 'clock_in_time')
        if 'clock_out_time' in data:
            attendance.clock_out_time = _dt(data['clock_out_time'], 'clock_out_time')
        if 'break_start_time' in data:
            attendance.break_start_time = _dt(data['break_start_time'], 'break_start_time')
        if 'break_end_time' in data:
            attendance.break_end_time = _dt(data['break_end_time'], 'break_end_time')
        if 'verified_at' in data:
            attendance.verified_at = _dt(data['verified_at'], 'verified_at')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    simple_fields = [
        'clock_in_method', 'clock_in_gps_lat', 'clock_in_gps_lng', 'clock_in_photo', 'clock_in_verified',
        'clock_out_method', 'clock_out_gps_lat', 'clock_out_gps_lng', 'clock_out_photo', 'clock_out_verified',
        'total_break_minutes', 'attendance_status', 'is_late', 'late_minutes', 'early_departure',
        'early_departure_minutes', 'incident_reported', 'incident_description', 'supervisor_notes',
        'verified_by', 'requires_correction', 'correction_reason', 'device_id', 'ip_address',
        'attendance_signature', 'weather_condition', 'notes'
    ]

    for field in simple_fields:
        if field in data:
            setattr(attendance, field, data[field])

    attendance.calculate_hours()
    db.session.commit()

    return jsonify(attendance.to_dict()), 200


@bp.route('/<int:attendance_id>', methods=['DELETE'])
@jwt_required()
def delete_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    db.session.delete(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance deleted'}), 200

