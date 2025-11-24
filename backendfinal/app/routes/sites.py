from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Site

bp = Blueprint('sites', __name__, url_prefix='/api/sites')

def _date(value, field):
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:
        raise ValueError(f"Invalid date for {field}") from exc


@bp.route('', methods=['GET'])
@jwt_required()
def get_sites():
    client_id = request.args.get('client_id')
    status = request.args.get('status')
    site_type = request.args.get('site_type')
    query = Site.query

    if client_id:
        query = query.filter_by(client_id=client_id)
    if status:
        query = query.filter_by(site_status=status)
    if site_type:
        query = query.filter_by(site_type=site_type)

    sites = query.all()
    return jsonify([site.to_dict() for site in sites]), 200

@bp.route('/<int:site_id>', methods=['GET'])
@jwt_required()
def get_site(site_id):
    site = Site.query.get_or_404(site_id)
    return jsonify(site.to_dict()), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_site():
    data = request.get_json() or {}

    required_fields = ['client_id', 'site_name', 'address', 'required_agents']
    missing = [field for field in required_fields if data.get(field) in (None, '')]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        contract_start = _date(data.get('contract_start_date'), 'contract_start_date')
        contract_end = _date(data.get('contract_end_date'), 'contract_end_date')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    site = Site(
        client_id=data['client_id'],
        site_name=data['site_name'],
        site_code=data.get('site_code'),
        site_type=data.get('site_type'),
        address=data['address'],
        city=data.get('city'),
        postal_code=data.get('postal_code'),
        gps_latitude=data.get('gps_latitude'),
        gps_longitude=data.get('gps_longitude'),
        geofence_radius_meters=data.get('geofence_radius_meters', 100),
        site_contact_name=data.get('site_contact_name'),
        site_contact_phone=data.get('site_contact_phone'),
        site_contact_email=data.get('site_contact_email'),
        required_agents=data['required_agents'],
        shift_pattern=data.get('shift_pattern'),
        access_instructions=data.get('access_instructions'),
        emergency_procedures=data.get('emergency_procedures'),
        special_equipment_required=data.get('special_equipment_required'),
        requires_armed_guard=data.get('requires_armed_guard', False),
        requires_dog_unit=data.get('requires_dog_unit', False),
        requires_vehicle=data.get('requires_vehicle', False),
        minimum_clearance_level=data.get('minimum_clearance_level', 1),
        hourly_rate_override=data.get('hourly_rate_override'),
        billing_rate=data.get('billing_rate'),
        contract_start_date=contract_start,
        contract_end_date=contract_end,
        site_status=data.get('site_status', 'active'),
        patrol_checkpoints=data.get('patrol_checkpoints'),
        restricted_areas=data.get('restricted_areas'),
        key_holder_contacts=data.get('key_holder_contacts'),
        alarm_code=data.get('alarm_code'),
        wifi_ssid=data.get('wifi_ssid'),
        wifi_password=data.get('wifi_password'),
        site_photo=data.get('site_photo'),
        site_map=data.get('site_map'),
        notes=data.get('notes')
    )

    db.session.add(site)
    db.session.commit()

    return jsonify(site.to_dict()), 201

@bp.route('/<int:site_id>', methods=['PUT'])
@jwt_required()
def update_site(site_id):
    site = Site.query.get_or_404(site_id)
    data = request.get_json() or {}

    date_fields = ['contract_start_date', 'contract_end_date']
    for field in date_fields:
        if field in data:
            try:
                setattr(site, field, _date(data[field], field))
            except ValueError as exc:
                return jsonify({'error': str(exc)}), 400

    simple_fields = [
        'site_name', 'site_code', 'site_type', 'address', 'city', 'postal_code',
        'gps_latitude', 'gps_longitude', 'geofence_radius_meters',
        'site_contact_name', 'site_contact_phone', 'site_contact_email',
        'required_agents', 'shift_pattern', 'access_instructions',
        'emergency_procedures', 'special_equipment_required',
        'requires_armed_guard', 'requires_dog_unit', 'requires_vehicle',
        'minimum_clearance_level', 'hourly_rate_override', 'billing_rate',
        'site_status', 'patrol_checkpoints', 'restricted_areas',
        'key_holder_contacts', 'alarm_code', 'wifi_ssid', 'wifi_password',
        'site_photo', 'site_map', 'notes'
    ]

    for field in simple_fields:
        if field in data:
            setattr(site, field, data[field])

    db.session.commit()
    return jsonify(site.to_dict()), 200

@bp.route('/<int:site_id>', methods=['DELETE'])
@jwt_required()
def delete_site(site_id):
    site = Site.query.get_or_404(site_id)
    site.site_status = 'inactive'
    db.session.commit()
    return jsonify({'message': 'Site deactivated'}), 200

