from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Document

bp = Blueprint('documents', __name__, url_prefix='/api/documents')


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
def list_documents():
    entity_type = request.args.get('entity_type')
    entity_id = request.args.get('entity_id')

    query = Document.query
    if entity_type:
        query = query.filter_by(entity_type=entity_type)
    if entity_id:
        query = query.filter_by(entity_id=entity_id)

    docs = query.order_by(Document.created_at.desc()).all()
    return jsonify([doc.to_dict() for doc in docs]), 200


@bp.route('/<int:document_id>', methods=['GET'])
@jwt_required()
def get_document(document_id):
    doc = Document.query.get_or_404(document_id)
    return jsonify(doc.to_dict()), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_document():
    data = request.get_json() or {}
    required = ['document_type', 'entity_type', 'entity_id', 'file_url']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    doc = Document(
        document_type=data['document_type'],
        entity_type=data['entity_type'],
        entity_id=data['entity_id'],
        document_name=data.get('document_name'),
        file_url=data['file_url'],
        file_size_kb=data.get('file_size_kb'),
        mime_type=data.get('mime_type'),
        issue_date=_date(data.get('issue_date'), 'issue_date'),
        expiry_date=_date(data.get('expiry_date'), 'expiry_date'),
        is_verified=data.get('is_verified', False),
        verified_by=data.get('verified_by'),
        verified_at=datetime.fromisoformat(data['verified_at']) if data.get('verified_at') else None,
        uploaded_by=data.get('uploaded_by')
    )

    db.session.add(doc)
    db.session.commit()

    return jsonify(doc.to_dict()), 201


@bp.route('/<int:document_id>', methods=['PUT'])
@jwt_required()
def update_document(document_id):
    doc = Document.query.get_or_404(document_id)
    data = request.get_json() or {}

    if 'issue_date' in data:
        doc.issue_date = _date(data['issue_date'], 'issue_date')
    if 'expiry_date' in data:
        doc.expiry_date = _date(data['expiry_date'], 'expiry_date')
    if 'verified_at' in data:
        doc.verified_at = datetime.fromisoformat(data['verified_at']) if data['verified_at'] else None

    fields = [
        'document_type', 'entity_type', 'entity_id', 'document_name', 'file_url',
        'file_size_kb', 'mime_type', 'is_verified', 'verified_by', 'uploaded_by'
    ]
    for field in fields:
        if field in data:
            setattr(doc, field, data[field])

    db.session.commit()
    return jsonify(doc.to_dict()), 200


@bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    doc = Document.query.get_or_404(document_id)
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'message': 'Document deleted'}), 200

