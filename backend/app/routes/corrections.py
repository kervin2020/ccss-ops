from flask import Blueprint, request, jsonify
from app import db
from app.models import Correction, Attendance
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('corrections', __name__, url_prefix='/api/corrections')

@bp.route('', methods=['GET'])
@jwt_required()
def get_corrections():
    agent_id = request.args.get('agent_id')
    status = request.args.get('status')
    
    query = Correction.query
    
    if agent_id:
        query = query.filter_by(agent_id=agent_id)
    if status:
        query = query.filter_by(correction_status=status)
    
    corrections = query.order_by(Correction.created_at.desc()).all()
    return jsonify([corr.to_dict() for corr in corrections]), 200

@bp.route('/<int:correction_id>', methods=['GET'])
@jwt_required()
def get_correction(correction_id):
    correction = Correction.query.get_or_404(correction_id)
    return jsonify(correction.to_dict()), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_correction():
    data = request.get_json()
    
    required_fields = ['attendance_id', 'agent_id', 'reason']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    attendance = Attendance.query.get_or_404(data['attendance_id'])
    
    correction = Correction(
        attendance_id=data['attendance_id'],
        agent_id=data['agent_id'],
        correction_type=data.get('correction_type', 'other'),
        reason=data['reason'],
        requested_clock_in=datetime.fromisoformat(data['requested_clock_in']) if data.get('requested_clock_in') else None,
        requested_clock_out=datetime.fromisoformat(data['requested_clock_out']) if data.get('requested_clock_out') else None,
        correction_status='pending'
    )
    
    db.session.add(correction)
    db.session.commit()
    
    return jsonify(correction.to_dict()), 201

@bp.route('/<int:correction_id>/approve', methods=['POST'])
@jwt_required()
def approve_correction(correction_id):
    correction = Correction.query.get_or_404(correction_id)
    data = request.get_json()
    
    if correction.correction_status != 'pending':
        return jsonify({'error': 'Correction already processed'}), 400
    
    attendance = Attendance.query.get_or_404(correction.attendance_id)
    
    # Apply correction
    if correction.requested_clock_in:
        attendance.clock_in_time = correction.requested_clock_in
    if correction.requested_clock_out:
        attendance.clock_out_time = correction.requested_clock_out
    
    attendance.calculate_hours()
    
    correction.correction_status = 'approved'
    correction.reviewed_by = get_jwt_identity()
    correction.review_notes = data.get('review_notes')
    correction.reviewed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(correction.to_dict()), 200

@bp.route('/<int:correction_id>/reject', methods=['POST'])
@jwt_required()
def reject_correction(correction_id):
    correction = Correction.query.get_or_404(correction_id)
    data = request.get_json()
    
    if correction.correction_status != 'pending':
        return jsonify({'error': 'Correction already processed'}), 400
    
    correction.correction_status = 'rejected'
    correction.reviewed_by = get_jwt_identity()
    correction.review_notes = data.get('review_notes', '')
    correction.reviewed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(correction.to_dict()), 200

