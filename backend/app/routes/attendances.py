from flask import Blueprint, request, jsonify
from app import db
from app.models import Attendance, Agent, Site
from flask_jwt_extended import jwt_required
from datetime import datetime, date

bp = Blueprint('attendances', __name__, url_prefix='/api/attendances')

@bp.route('', methods=['GET'])
@jwt_required()
def get_attendances():
    agent_id = request.args.get('agent_id')
    site_id = request.args.get('site_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Attendance.query
    
    if agent_id:
        query = query.filter_by(agent_id=agent_id)
    if site_id:
        query = query.filter_by(site_id=site_id)
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
    data = request.get_json()
    
    required_fields = ['agent_id', 'site_id', 'attendance_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if agent and site exist
    Agent.query.get_or_404(data['agent_id'])
    Site.query.get_or_404(data['site_id'])
    
    attendance = Attendance(
        agent_id=data['agent_id'],
        site_id=data['site_id'],
        attendance_date=datetime.fromisoformat(data['attendance_date']).date() if isinstance(data['attendance_date'], str) else data['attendance_date'],
        clock_in_time=datetime.fromisoformat(data['clock_in_time']) if data.get('clock_in_time') else None,
        clock_out_time=datetime.fromisoformat(data['clock_out_time']) if data.get('clock_out_time') else None,
        attendance_status=data.get('attendance_status', 'present'),
        notes=data.get('notes')
    )
    
    attendance.calculate_hours()
    
    db.session.add(attendance)
    db.session.commit()
    
    return jsonify(attendance.to_dict()), 201

@bp.route('/<int:attendance_id>', methods=['PUT'])
@jwt_required()
def update_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    data = request.get_json()
    
    if 'clock_in_time' in data:
        attendance.clock_in_time = datetime.fromisoformat(data['clock_in_time']) if data['clock_in_time'] else None
    if 'clock_out_time' in data:
        attendance.clock_out_time = datetime.fromisoformat(data['clock_out_time']) if data['clock_out_time'] else None
    
    attendance.attendance_status = data.get('attendance_status', attendance.attendance_status)
    attendance.notes = data.get('notes', attendance.notes)
    
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

