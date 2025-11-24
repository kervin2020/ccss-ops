from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Training, AgentTraining, Agent

bp = Blueprint('trainings', __name__, url_prefix='/api/trainings')


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
def list_trainings():
    trainings = Training.query.order_by(Training.training_name.asc()).all()
    return jsonify([training.to_dict() for training in trainings]), 200


@bp.route('/<int:training_id>', methods=['GET'])
@jwt_required()
def get_training(training_id):
    training = Training.query.get_or_404(training_id)
    return jsonify(training.to_dict()), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_training():
    data = request.get_json() or {}
    if not data.get('training_name'):
        return jsonify({'error': 'training_name is required'}), 400

    training = Training(
        training_name=data['training_name'],
        training_type=data.get('training_type'),
        duration_hours=data.get('duration_hours'),
        valid_for_months=data.get('valid_for_months'),
        description=data.get('description')
    )

    db.session.add(training)
    db.session.commit()

    return jsonify(training.to_dict()), 201


@bp.route('/<int:training_id>', methods=['PUT'])
@jwt_required()
def update_training(training_id):
    training = Training.query.get_or_404(training_id)
    data = request.get_json() or {}

    fields = ['training_name', 'training_type', 'duration_hours', 'valid_for_months', 'description']
    for field in fields:
        if field in data:
            setattr(training, field, data[field])

    db.session.commit()
    return jsonify(training.to_dict()), 200


@bp.route('/<int:training_id>', methods=['DELETE'])
@jwt_required()
def delete_training(training_id):
    training = Training.query.get_or_404(training_id)
    db.session.delete(training)
    db.session.commit()
    return jsonify({'message': 'Training deleted'}), 200


@bp.route('/assign', methods=['POST'])
@jwt_required()
def assign_training():
    data = request.get_json() or {}
    required = ['agent_id', 'training_id']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    Agent.query.get_or_404(data['agent_id'])
    Training.query.get_or_404(data['training_id'])

    assignment = AgentTraining(
        agent_id=data['agent_id'],
        training_id=data['training_id'],
        completion_date=_date(data.get('completion_date'), 'completion_date'),
        expiry_date=_date(data.get('expiry_date'), 'expiry_date'),
        score=data.get('score'),
        certificate_url=data.get('certificate_url')
    )

    db.session.add(assignment)
    db.session.commit()

    return jsonify(assignment.to_dict()), 201


@bp.route('/assign/<int:assignment_id>', methods=['PUT'])
@jwt_required()
def update_assignment(assignment_id):
    assignment = AgentTraining.query.get_or_404(assignment_id)
    data = request.get_json() or {}

    if 'completion_date' in data:
        assignment.completion_date = _date(data['completion_date'], 'completion_date')
    if 'expiry_date' in data:
        assignment.expiry_date = _date(data['expiry_date'], 'expiry_date')

    if 'score' in data:
        assignment.score = data['score']
    if 'certificate_url' in data:
        assignment.certificate_url = data['certificate_url']

    db.session.commit()
    return jsonify(assignment.to_dict()), 200

