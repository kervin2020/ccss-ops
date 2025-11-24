from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Incident, Site, Agent, Attendance

bp = Blueprint('incidents', __name__, url_prefix='/api/incidents')


def _dt(value, field):
    if not value:
        raise ValueError(f'{field} is required')
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f'Invalid datetime for {field}') from exc


@bp.route('', methods=['GET'])
@jwt_required()
def list_incidents():
    site_id = request.args.get('site_id')
    agent_id = request.args.get('agent_id')
    status = request.args.get('status')

    query = Incident.query
    if site_id:
        query = query.filter_by(site_id=site_id)
    if agent_id:
        query = query.filter_by(agent_id=agent_id)
    if status:
        query = query.filter_by(incident_status=status)

    incidents = query.order_by(Incident.incident_date.desc()).all()
    return jsonify([incident.to_dict() for incident in incidents]), 200


@bp.route('/<int:incident_id>', methods=['GET'])
@jwt_required()
def get_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    return jsonify(incident.to_dict()), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_incident():
    data = request.get_json() or {}

    required = ['site_id', 'agent_id', 'incident_type', 'incident_date', 'description']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    Site.query.get_or_404(data['site_id'])
    Agent.query.get_or_404(data['agent_id'])
    if data.get('attendance_id'):
        Attendance.query.get_or_404(data['attendance_id'])

    try:
        incident_date = _dt(data['incident_date'], 'incident_date')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    incident = Incident(
        site_id=data['site_id'],
        agent_id=data['agent_id'],
        attendance_id=data.get('attendance_id'),
        incident_date=incident_date,
        incident_type=data['incident_type'],
        severity=data.get('severity', 'medium'),
        description=data['description'],
        action_taken=data.get('action_taken'),
        police_notified=data.get('police_notified', False),
        police_report_number=data.get('police_report_number'),
        client_notified=data.get('client_notified', False),
        client_notified_at=_dt(data['client_notified_at'], 'client_notified_at') if data.get('client_notified_at') else None,
        witnesses=data.get('witnesses'),
        evidence_photos=data.get('evidence_photos'),
        incident_status=data.get('incident_status', 'open')
    )

    db.session.add(incident)
    db.session.commit()

    return jsonify(incident.to_dict()), 201


@bp.route('/<int:incident_id>', methods=['PUT'])
@jwt_required()
def update_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    data = request.get_json() or {}

    if 'site_id' in data and data['site_id']:
        Site.query.get_or_404(data['site_id'])
        incident.site_id = data['site_id']
    if 'agent_id' in data and data['agent_id']:
        Agent.query.get_or_404(data['agent_id'])
        incident.agent_id = data['agent_id']
    if 'attendance_id' in data:
        if data['attendance_id']:
            Attendance.query.get_or_404(data['attendance_id'])
        incident.attendance_id = data['attendance_id']
    if 'incident_date' in data and data['incident_date']:
        try:
            incident.incident_date = _dt(data['incident_date'], 'incident_date')
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400

    simple_fields = [
        'incident_type', 'severity', 'description', 'action_taken',
        'police_notified', 'police_report_number', 'client_notified',
        'witnesses', 'evidence_photos', 'incident_status', 'resolution_notes'
    ]
    for field in simple_fields:
        if field in data:
            setattr(incident, field, data[field])

    if 'client_notified_at' in data:
        incident.client_notified_at = _dt(data['client_notified_at'], 'client_notified_at') if data['client_notified_at'] else None
    if 'resolved_at' in data:
        incident.resolved_at = _dt(data['resolved_at'], 'resolved_at') if data['resolved_at'] else None
    if 'resolved_by' in data:
        incident.resolved_by = data['resolved_by']

    db.session.commit()
    return jsonify(incident.to_dict()), 200


@bp.route('/<int:incident_id>/resolve', methods=['POST'])
@jwt_required()
def resolve_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    payload = request.get_json(silent=True) or {}
    incident.resolve(payload.get('resolved_by'), payload.get('notes', 'Resolved'))
    db.session.commit()
    return jsonify(incident.to_dict()), 200


@bp.route('/<int:incident_id>', methods=['DELETE'])
@jwt_required()
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({'message': 'Incident deleted'}), 200

