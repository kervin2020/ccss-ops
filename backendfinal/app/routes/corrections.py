from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Correction, Attendance

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
    data = request.get_json() or {}

    required_fields = ['attendance_id', 'agent_id', 'reason']
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    attendance = Attendance.query.get_or_404(data['attendance_id'])

    correction = Correction(
        attendance_id=data['attendance_id'],
        agent_id=data['agent_id'],
        requested_by=get_jwt_identity(),
        correction_type=data.get('correction_type', 'other'),
        reason=data['reason'],
        original_clock_in=attendance.clock_in_time,
        original_clock_out=attendance.clock_out_time,
        requested_clock_in=datetime.fromisoformat(data['requested_clock_in']) if data.get('requested_clock_in') else None,
        requested_clock_out=datetime.fromisoformat(data['requested_clock_out']) if data.get('requested_clock_out') else None,
        supporting_document=data.get('supporting_document')
    )

    attendance.requires_correction = True
    attendance.correction_reason = data['reason']

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
    
    reviewer_id = get_jwt_identity()
    correction.approve(reviewer_id, data.get('review_notes'))
    db.session.commit()

    return jsonify(correction.to_dict()), 200

@bp.route('/<int:correction_id>/reject', methods=['POST'])
@jwt_required()
def reject_correction(correction_id):
    correction = Correction.query.get_or_404(correction_id)
    data = request.get_json()
    
    if correction.correction_status != 'pending':
        return jsonify({'error': 'Correction already processed'}), 400
    
    correction.reject(get_jwt_identity(), data.get('review_notes', ''))
    db.session.commit()

    return jsonify(correction.to_dict()), 200

