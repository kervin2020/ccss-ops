from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Notification

bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')


def _dt(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


@bp.route('', methods=['GET'])
@jwt_required()
def list_notifications():
    current_user = get_jwt_identity()
    status = request.args.get('status')

    query = Notification.query.filter(
        (Notification.user_id == current_user) | (Notification.user_id.is_(None))
    )
    if status == 'unread':
        query = query.filter_by(is_read=False)

    notifications = query.order_by(Notification.created_at.desc()).all()
    return jsonify([n.to_dict() for n in notifications]), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_notification():
    data = request.get_json() or {}
    if not data.get('title') or not data.get('message'):
        return jsonify({'error': 'title and message are required'}), 400

    notification = Notification(
        user_id=data.get('user_id'),
        agent_id=data.get('agent_id'),
        notification_type=data.get('notification_type'),
        title=data['title'],
        message=data['message'],
        priority=data.get('priority', 'normal'),
        action_url=data.get('action_url'),
        expires_at=_dt(data.get('expires_at'))
    )

    db.session.add(notification)
    db.session.commit()

    return jsonify(notification.to_dict()), 201


@bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.session.commit()
    return jsonify(notification.to_dict()), 200


@bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted'}), 200

