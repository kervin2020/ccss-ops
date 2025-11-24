from datetime import datetime
from decimal import Decimal

from werkzeug.security import generate_password_hash, check_password_hash

from app import db

try:
    from sqlalchemy.dialects.postgresql import JSON
except ImportError:  # pragma: no cover - fallback when dialect not available
    from sqlalchemy.types import JSON  # type: ignore


def decimal_to_float(value, allow_none=False):
    if value is None:
        return None if allow_none else 0.0
    if isinstance(value, Decimal):
        return float(value)
    return value


def to_iso(value):
    return value.isoformat() if value else None


class User(db.Model):
    """System users (admin, operators, HR, finance, etc.)."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), default='operator')  # admin, operator, manager, hr, finance, etc.
    profile_picture = db.Column(db.String(255))
    department = db.Column(db.String(100))
    permissions = db.Column(JSON)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    password_reset_token = db.Column(db.String(255))
    password_reset_expires = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'role': self.role,
            'profile_picture': self.profile_picture,
            'department': self.department,
            'permissions': self.permissions,
            'two_factor_enabled': self.two_factor_enabled,
            'is_active': self.is_active,
            'last_login': to_iso(self.last_login),
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Agent(db.Model):
    """Security agents/guards."""
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    national_id = db.Column(db.String(50), unique=True, index=True)
    phone_primary = db.Column(db.String(20), nullable=False)
    phone_secondary = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_relationship = db.Column(db.String(50))
    hire_date = db.Column(db.Date, nullable=False)
    contract_type = db.Column(db.String(20), default='permanent')
    contract_end_date = db.Column(db.Date)
    employment_status = db.Column(db.String(20), default='active', index=True)
    termination_date = db.Column(db.Date)
    termination_reason = db.Column(db.Text)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    bank_name = db.Column(db.String(100))
    bank_account_number = db.Column(db.String(50))
    tax_id = db.Column(db.String(50))
    uniform_size = db.Column(db.String(10))
    badge_number = db.Column(db.String(20), unique=True)
    security_clearance_level = db.Column(db.Integer, default=1)
    has_firearm_license = db.Column(db.Boolean, default=False)
    firearm_license_number = db.Column(db.String(50))
    firearm_license_expiry = db.Column(db.Date)
    blood_type = db.Column(db.String(5))
    has_drivers_license = db.Column(db.Boolean, default=False)
    drivers_license_number = db.Column(db.String(50))
    languages_spoken = db.Column(JSON)
    medical_conditions = db.Column(db.Text)
    training_level = db.Column(db.String(50))
    profile_photo = db.Column(db.String(255))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attendances = db.relationship('Attendance', backref='agent', lazy='dynamic')
    payrolls = db.relationship('Payroll', backref='agent', lazy='dynamic')
    shifts = db.relationship('Shift', backref='agent', lazy='dynamic')
    corrections = db.relationship('Correction', backref='agent', lazy='dynamic')
    leaves = db.relationship('Leave', backref='agent', lazy='dynamic')
    incidents = db.relationship('Incident', backref='agent', lazy='dynamic')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def to_dict(self):
        return {
            'id': self.id,
            'employee_code': self.employee_code,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'date_of_birth': to_iso(self.date_of_birth),
            'gender': self.gender,
            'national_id': self.national_id,
            'phone_primary': self.phone_primary,
            'phone_secondary': self.phone_secondary,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'emergency_contact_relationship': self.emergency_contact_relationship,
            'hire_date': to_iso(self.hire_date),
            'contract_type': self.contract_type,
            'contract_end_date': to_iso(self.contract_end_date),
            'employment_status': self.employment_status,
            'termination_date': to_iso(self.termination_date),
            'termination_reason': self.termination_reason,
            'hourly_rate': decimal_to_float(self.hourly_rate),
            'bank_name': self.bank_name,
            'bank_account_number': self.bank_account_number,
            'tax_id': self.tax_id,
            'uniform_size': self.uniform_size,
            'badge_number': self.badge_number,
            'security_clearance_level': self.security_clearance_level,
            'has_firearm_license': self.has_firearm_license,
            'firearm_license_number': self.firearm_license_number,
            'firearm_license_expiry': to_iso(self.firearm_license_expiry),
            'blood_type': self.blood_type,
            'has_drivers_license': self.has_drivers_license,
            'drivers_license_number': self.drivers_license_number,
            'languages_spoken': self.languages_spoken,
            'training_level': self.training_level,
            'profile_photo': self.profile_photo,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Client(db.Model):
    """Client companies."""
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    company_registration_number = db.Column(db.String(50), unique=True)
    tax_id = db.Column(db.String(50))
    industry_sector = db.Column(db.String(100))
    primary_contact_name = db.Column(db.String(100), nullable=False)
    primary_contact_title = db.Column(db.String(100))
    primary_contact_phone = db.Column(db.String(20), nullable=False)
    primary_contact_email = db.Column(db.String(255), nullable=False)
    billing_contact_name = db.Column(db.String(100))
    billing_contact_phone = db.Column(db.String(20))
    billing_contact_email = db.Column(db.String(255))
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10))
    country = db.Column(db.String(100), default='Haiti')
    contract_start_date = db.Column(db.Date, nullable=False)
    contract_end_date = db.Column(db.Date)
    contract_status = db.Column(db.String(20), default='active', index=True)
    payment_terms = db.Column(db.String(20), default='30_days')
    billing_frequency = db.Column(db.String(20), default='monthly')
    billing_day = db.Column(db.Integer)
    currency = db.Column(db.String(3), default='HTG')
    credit_limit = db.Column(db.Numeric(12, 2), default=0)
    current_balance = db.Column(db.Numeric(12, 2), default=0)
    total_invoiced = db.Column(db.Numeric(12, 2), default=0)
    total_paid = db.Column(db.Numeric(12, 2), default=0)
    discount_percentage = db.Column(db.Numeric(5, 2), default=0)
    service_level_agreement = db.Column(db.Text)
    special_requirements = db.Column(db.Text)
    requires_background_check = db.Column(db.Boolean, default=False)
    requires_drug_testing = db.Column(db.Boolean, default=False)
    insurance_certificate_required = db.Column(db.Boolean, default=False)
    preferred_communication_method = db.Column(db.String(20), default='email')
    logo_url = db.Column(db.String(255))
    website = db.Column(db.String(255))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sites = db.relationship('Site', backref='client', lazy='dynamic')
    invoices = db.relationship('Invoice', backref='client', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'company_registration_number': self.company_registration_number,
            'tax_id': self.tax_id,
            'industry_sector': self.industry_sector,
            'primary_contact_name': self.primary_contact_name,
            'primary_contact_title': self.primary_contact_title,
            'primary_contact_phone': self.primary_contact_phone,
            'primary_contact_email': self.primary_contact_email,
            'billing_contact_name': self.billing_contact_name,
            'billing_contact_phone': self.billing_contact_phone,
            'billing_contact_email': self.billing_contact_email,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'country': self.country,
            'contract_start_date': to_iso(self.contract_start_date),
            'contract_end_date': to_iso(self.contract_end_date),
            'contract_status': self.contract_status,
            'payment_terms': self.payment_terms,
            'billing_frequency': self.billing_frequency,
            'billing_day': self.billing_day,
            'currency': self.currency,
            'credit_limit': decimal_to_float(self.credit_limit),
            'current_balance': decimal_to_float(self.current_balance),
            'total_invoiced': decimal_to_float(self.total_invoiced),
            'total_paid': decimal_to_float(self.total_paid),
            'discount_percentage': decimal_to_float(self.discount_percentage),
            'service_level_agreement': self.service_level_agreement,
            'special_requirements': self.special_requirements,
            'requires_background_check': self.requires_background_check,
            'requires_drug_testing': self.requires_drug_testing,
            'insurance_certificate_required': self.insurance_certificate_required,
            'preferred_communication_method': self.preferred_communication_method,
            'logo_url': self.logo_url,
            'website': self.website,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Site(db.Model):
    """Work sites / locations."""
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False, index=True)
    site_name = db.Column(db.String(255), nullable=False)
    site_code = db.Column(db.String(20), unique=True, index=True)
    site_type = db.Column(db.String(50))
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    gps_latitude = db.Column(db.Numeric(10, 8))
    gps_longitude = db.Column(db.Numeric(11, 8))
    geofence_radius_meters = db.Column(db.Integer, default=100)
    site_contact_name = db.Column(db.String(100))
    site_contact_phone = db.Column(db.String(20))
    site_contact_email = db.Column(db.String(255))
    required_agents = db.Column(db.Integer, nullable=False, default=1)
    shift_pattern = db.Column(db.String(50))
    access_instructions = db.Column(db.Text)
    emergency_procedures = db.Column(db.Text)
    special_equipment_required = db.Column(db.Text)
    requires_armed_guard = db.Column(db.Boolean, default=False)
    requires_dog_unit = db.Column(db.Boolean, default=False)
    requires_vehicle = db.Column(db.Boolean, default=False)
    minimum_clearance_level = db.Column(db.Integer, default=1)
    hourly_rate_override = db.Column(db.Numeric(10, 2))
    billing_rate = db.Column(db.Numeric(10, 2))
    contract_start_date = db.Column(db.Date)
    contract_end_date = db.Column(db.Date)
    site_status = db.Column(db.String(20), default='active', index=True)
    patrol_checkpoints = db.Column(JSON)
    restricted_areas = db.Column(JSON)
    key_holder_contacts = db.Column(JSON)
    alarm_code = db.Column(db.String(50))
    wifi_ssid = db.Column(db.String(100))
    wifi_password = db.Column(db.String(100))
    site_photo = db.Column(db.String(255))
    site_map = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attendances = db.relationship('Attendance', backref='site', lazy='dynamic')
    shifts = db.relationship('Shift', backref='site', lazy='dynamic')
    incidents = db.relationship('Incident', backref='site', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'site_name': self.site_name,
            'site_code': self.site_code,
            'site_type': self.site_type,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'gps_latitude': decimal_to_float(self.gps_latitude, allow_none=True),
            'gps_longitude': decimal_to_float(self.gps_longitude, allow_none=True),
            'geofence_radius_meters': self.geofence_radius_meters,
            'site_contact_name': self.site_contact_name,
            'site_contact_phone': self.site_contact_phone,
            'site_contact_email': self.site_contact_email,
            'required_agents': self.required_agents,
            'shift_pattern': self.shift_pattern,
            'access_instructions': self.access_instructions,
            'emergency_procedures': self.emergency_procedures,
            'special_equipment_required': self.special_equipment_required,
            'requires_armed_guard': self.requires_armed_guard,
            'requires_dog_unit': self.requires_dog_unit,
            'requires_vehicle': self.requires_vehicle,
            'minimum_clearance_level': self.minimum_clearance_level,
            'hourly_rate_override': decimal_to_float(self.hourly_rate_override, allow_none=True),
            'billing_rate': decimal_to_float(self.billing_rate, allow_none=True),
            'contract_start_date': to_iso(self.contract_start_date),
            'contract_end_date': to_iso(self.contract_end_date),
            'site_status': self.site_status,
            'patrol_checkpoints': self.patrol_checkpoints,
            'restricted_areas': self.restricted_areas,
            'key_holder_contacts': self.key_holder_contacts,
            'alarm_code': self.alarm_code,
            'wifi_ssid': self.wifi_ssid,
            'wifi_password': self.wifi_password,
            'site_photo': self.site_photo,
            'site_map': self.site_map,
            'notes': self.notes,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Shift(db.Model):
    """Scheduled shifts (planning)."""
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False, index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    shift_date = db.Column(db.Date, nullable=False, index=True)
    shift_type = db.Column(db.String(20))
    scheduled_start_time = db.Column(db.Time, nullable=False)
    scheduled_end_time = db.Column(db.Time, nullable=False)
    scheduled_hours = db.Column(db.Numeric(5, 2))
    shift_status = db.Column(db.String(20), default='scheduled')
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    special_instructions = db.Column(db.Text)
    required_equipment = db.Column(db.Text)
    operator_changes = db.Column(db.Integer, default=0)
    operator_last_change_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    operator_last_change_at = db.Column(db.DateTime)
    operator_last_change_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attendance = db.relationship('Attendance', backref='shift', uselist=False, lazy=True)

    def increment_operator_change(self, user_id, reason=None):
        self.operator_changes = (self.operator_changes or 0) + 1
        self.operator_last_change_by = user_id
        self.operator_last_change_at = datetime.utcnow()
        self.operator_last_change_reason = reason

    def operator_can_modify(self):
        return (self.operator_changes or 0) < 1

    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'agent_id': self.agent_id,
            'shift_date': to_iso(self.shift_date),
            'shift_type': self.shift_type,
            'scheduled_start_time': to_iso(self.scheduled_start_time),
            'scheduled_end_time': to_iso(self.scheduled_end_time),
            'scheduled_hours': decimal_to_float(self.scheduled_hours),
            'shift_status': self.shift_status,
            'assigned_by': self.assigned_by,
            'assigned_at': to_iso(self.assigned_at),
            'special_instructions': self.special_instructions,
            'required_equipment': self.required_equipment,
            'operator_changes': self.operator_changes,
            'operator_last_change_by': self.operator_last_change_by,
            'operator_last_change_at': to_iso(self.operator_last_change_at),
            'operator_last_change_reason': self.operator_last_change_reason,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Attendance(db.Model):
    """Actual attendance records."""
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False, index=True)
    attendance_date = db.Column(db.Date, nullable=False, index=True)
    clock_in_time = db.Column(db.DateTime)
    clock_in_method = db.Column(db.String(20))
    clock_in_gps_lat = db.Column(db.Numeric(10, 8))
    clock_in_gps_lng = db.Column(db.Numeric(11, 8))
    clock_in_photo = db.Column(db.String(255))
    clock_in_verified = db.Column(db.Boolean, default=False)
    clock_out_time = db.Column(db.DateTime)
    clock_out_method = db.Column(db.String(20))
    clock_out_gps_lat = db.Column(db.Numeric(10, 8))
    clock_out_gps_lng = db.Column(db.Numeric(11, 8))
    clock_out_photo = db.Column(db.String(255))
    clock_out_verified = db.Column(db.Boolean, default=False)
    total_hours = db.Column(db.Numeric(5, 2), default=0)
    regular_hours = db.Column(db.Numeric(5, 2), default=0)
    overtime_hours = db.Column(db.Numeric(5, 2), default=0)
    night_shift_hours = db.Column(db.Numeric(5, 2), default=0)
    holiday_hours = db.Column(db.Numeric(5, 2), default=0)
    break_start_time = db.Column(db.DateTime)
    break_end_time = db.Column(db.DateTime)
    total_break_minutes = db.Column(db.Integer, default=0)
    attendance_status = db.Column(db.String(20), default='present')
    is_late = db.Column(db.Boolean, default=False)
    late_minutes = db.Column(db.Integer, default=0)
    early_departure = db.Column(db.Boolean, default=False)
    early_departure_minutes = db.Column(db.Integer, default=0)
    incident_reported = db.Column(db.Boolean, default=False)
    incident_description = db.Column(db.Text)
    supervisor_notes = db.Column(db.Text)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    requires_correction = db.Column(db.Boolean, default=False)
    correction_reason = db.Column(db.Text)
    device_id = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    attendance_signature = db.Column(db.String(255))
    weather_condition = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    corrections = db.relationship('Correction', backref='attendance', lazy='dynamic')

    def calculate_hours(self):
        if self.clock_in_time and self.clock_out_time:
            delta = self.clock_out_time - self.clock_in_time
            total_seconds = delta.total_seconds()
            if self.total_break_minutes:
                total_seconds -= (self.total_break_minutes * 60)
            self.total_hours = round(total_seconds / 3600.0, 2)
        return self.total_hours

    def to_dict(self):
        return {
            'id': self.id,
            'shift_id': self.shift_id,
            'agent_id': self.agent_id,
            'site_id': self.site_id,
            'attendance_date': to_iso(self.attendance_date),
            'clock_in_time': to_iso(self.clock_in_time),
            'clock_in_method': self.clock_in_method,
            'clock_in_gps_lat': decimal_to_float(self.clock_in_gps_lat, allow_none=True),
            'clock_in_gps_lng': decimal_to_float(self.clock_in_gps_lng, allow_none=True),
            'clock_in_photo': self.clock_in_photo,
            'clock_in_verified': self.clock_in_verified,
            'clock_out_time': to_iso(self.clock_out_time),
            'clock_out_method': self.clock_out_method,
            'clock_out_gps_lat': decimal_to_float(self.clock_out_gps_lat, allow_none=True),
            'clock_out_gps_lng': decimal_to_float(self.clock_out_gps_lng, allow_none=True),
            'clock_out_photo': self.clock_out_photo,
            'clock_out_verified': self.clock_out_verified,
            'total_hours': decimal_to_float(self.total_hours),
            'regular_hours': decimal_to_float(self.regular_hours),
            'overtime_hours': decimal_to_float(self.overtime_hours),
            'night_shift_hours': decimal_to_float(self.night_shift_hours),
            'holiday_hours': decimal_to_float(self.holiday_hours),
            'break_start_time': to_iso(self.break_start_time),
            'break_end_time': to_iso(self.break_end_time),
            'total_break_minutes': self.total_break_minutes,
            'attendance_status': self.attendance_status,
            'is_late': self.is_late,
            'late_minutes': self.late_minutes,
            'early_departure': self.early_departure,
            'early_departure_minutes': self.early_departure_minutes,
            'incident_reported': self.incident_reported,
            'incident_description': self.incident_description,
            'supervisor_notes': self.supervisor_notes,
            'verified_by': self.verified_by,
            'verified_at': to_iso(self.verified_at),
            'requires_correction': self.requires_correction,
            'correction_reason': self.correction_reason,
            'device_id': self.device_id,
            'ip_address': self.ip_address,
            'attendance_signature': self.attendance_signature,
            'weather_condition': self.weather_condition,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Correction(db.Model):
    """Attendance correction requests."""
    __tablename__ = 'corrections'

    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendances.id'), nullable=False, index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    correction_type = db.Column(db.String(50))
    reason = db.Column(db.Text, nullable=False)
    original_clock_in = db.Column(db.DateTime)
    original_clock_out = db.Column(db.DateTime)
    requested_clock_in = db.Column(db.DateTime)
    requested_clock_out = db.Column(db.DateTime)
    supporting_document = db.Column(db.String(255))
    correction_status = db.Column(db.String(20), default='pending', index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_notes = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime)
    applied_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def approve(self, reviewer_id, notes=None):
        self.correction_status = 'approved'
        self.reviewed_by = reviewer_id
        self.review_notes = notes
        self.reviewed_at = datetime.utcnow()
        self.applied_at = datetime.utcnow()
        attendance = Attendance.query.get(self.attendance_id)
        if attendance:
            if self.requested_clock_in:
                attendance.clock_in_time = self.requested_clock_in
            if self.requested_clock_out:
                attendance.clock_out_time = self.requested_clock_out
            attendance.calculate_hours()
            attendance.requires_correction = False
        return True

    def reject(self, reviewer_id, notes):
        self.correction_status = 'rejected'
        self.reviewed_by = reviewer_id
        self.review_notes = notes
        self.reviewed_at = datetime.utcnow()
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'attendance_id': self.attendance_id,
            'agent_id': self.agent_id,
            'requested_by': self.requested_by,
            'correction_type': self.correction_type,
            'reason': self.reason,
            'original_clock_in': to_iso(self.original_clock_in),
            'original_clock_out': to_iso(self.original_clock_out),
            'requested_clock_in': to_iso(self.requested_clock_in),
            'requested_clock_out': to_iso(self.requested_clock_out),
            'supporting_document': self.supporting_document,
            'correction_status': self.correction_status,
            'reviewed_by': self.reviewed_by,
            'review_notes': self.review_notes,
            'reviewed_at': to_iso(self.reviewed_at),
            'applied_at': to_iso(self.applied_at),
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Payroll(db.Model):
    """Payroll / salary records."""
    __tablename__ = 'payrolls'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    pay_period_start = db.Column(db.Date, nullable=False, index=True)
    pay_period_end = db.Column(db.Date, nullable=False, index=True)
    payment_date = db.Column(db.Date)
    total_regular_hours = db.Column(db.Numeric(7, 2), default=0)
    total_overtime_hours = db.Column(db.Numeric(7, 2), default=0)
    total_night_shift_hours = db.Column(db.Numeric(7, 2), default=0)
    total_holiday_hours = db.Column(db.Numeric(7, 2), default=0)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    overtime_rate = db.Column(db.Numeric(10, 2))
    night_shift_rate = db.Column(db.Numeric(10, 2))
    holiday_rate = db.Column(db.Numeric(10, 2))
    gross_regular_pay = db.Column(db.Numeric(12, 2), default=0)
    gross_overtime_pay = db.Column(db.Numeric(12, 2), default=0)
    gross_night_shift_pay = db.Column(db.Numeric(12, 2), default=0)
    gross_holiday_pay = db.Column(db.Numeric(12, 2), default=0)
    gross_total = db.Column(db.Numeric(12, 2), default=0)
    bonus_amount = db.Column(db.Numeric(12, 2), default=0)
    bonus_description = db.Column(db.Text)
    allowances = db.Column(db.Numeric(12, 2), default=0)
    allowances_description = db.Column(db.Text)
    deduction_tax = db.Column(db.Numeric(12, 2), default=0)
    deduction_social_security = db.Column(db.Numeric(12, 2), default=0)
    deduction_insurance = db.Column(db.Numeric(12, 2), default=0)
    deduction_uniform = db.Column(db.Numeric(12, 2), default=0)
    deduction_loan = db.Column(db.Numeric(12, 2), default=0)
    deduction_other = db.Column(db.Numeric(12, 2), default=0)
    deduction_other_description = db.Column(db.Text)
    total_deductions = db.Column(db.Numeric(12, 2), default=0)
    net_pay = db.Column(db.Numeric(12, 2), default=0)
    payment_method = db.Column(db.String(20))
    payment_reference = db.Column(db.String(100))
    payment_status = db.Column(db.String(20), default='draft', index=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    paid_at = db.Column(db.DateTime)
    payslip_generated = db.Column(db.Boolean, default=False)
    payslip_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calculate_gross_pay(self):
        self.gross_regular_pay = decimal_to_float(self.total_regular_hours) * decimal_to_float(self.hourly_rate)
        overtime_rate = decimal_to_float(self.overtime_rate) or (decimal_to_float(self.hourly_rate) * 1.5)
        night_rate = decimal_to_float(self.night_shift_rate) or decimal_to_float(self.hourly_rate)
        holiday_rate = decimal_to_float(self.holiday_rate) or (decimal_to_float(self.hourly_rate) * 2.0)
        self.gross_overtime_pay = decimal_to_float(self.total_overtime_hours) * overtime_rate
        self.gross_night_shift_pay = decimal_to_float(self.total_night_shift_hours) * night_rate
        self.gross_holiday_pay = decimal_to_float(self.total_holiday_hours) * holiday_rate
        self.gross_total = (
            self.gross_regular_pay + self.gross_overtime_pay +
            self.gross_night_shift_pay + self.gross_holiday_pay
        )
        return self.gross_total

    def calculate_total_deductions(self):
        self.total_deductions = (
            decimal_to_float(self.deduction_tax) +
            decimal_to_float(self.deduction_social_security) +
            decimal_to_float(self.deduction_insurance) +
            decimal_to_float(self.deduction_uniform) +
            decimal_to_float(self.deduction_loan) +
            decimal_to_float(self.deduction_other)
        )
        return self.total_deductions

    def calculate_net_pay(self):
        self.calculate_gross_pay()
        self.calculate_total_deductions()
        self.net_pay = (
            decimal_to_float(self.gross_total) +
            decimal_to_float(self.bonus_amount) +
            decimal_to_float(self.allowances) -
            decimal_to_float(self.total_deductions)
        )
        return self.net_pay

    def approve(self, approver_id):
        self.payment_status = 'approved'
        self.approved_by = approver_id
        self.approved_at = datetime.utcnow()
        return True

    def mark_as_paid(self, paid_by_id, payment_ref=None):
        self.payment_status = 'paid'
        self.paid_by = paid_by_id
        self.paid_at = datetime.utcnow()
        self.payment_date = datetime.utcnow().date()
        if payment_ref:
            self.payment_reference = payment_ref
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'pay_period_start': to_iso(self.pay_period_start),
            'pay_period_end': to_iso(self.pay_period_end),
            'payment_date': to_iso(self.payment_date),
            'total_regular_hours': decimal_to_float(self.total_regular_hours),
            'total_overtime_hours': decimal_to_float(self.total_overtime_hours),
            'total_night_shift_hours': decimal_to_float(self.total_night_shift_hours),
            'total_holiday_hours': decimal_to_float(self.total_holiday_hours),
            'hourly_rate': decimal_to_float(self.hourly_rate),
            'overtime_rate': decimal_to_float(self.overtime_rate),
            'night_shift_rate': decimal_to_float(self.night_shift_rate),
            'holiday_rate': decimal_to_float(self.holiday_rate),
            'gross_regular_pay': decimal_to_float(self.gross_regular_pay),
            'gross_overtime_pay': decimal_to_float(self.gross_overtime_pay),
            'gross_night_shift_pay': decimal_to_float(self.gross_night_shift_pay),
            'gross_holiday_pay': decimal_to_float(self.gross_holiday_pay),
            'gross_total': decimal_to_float(self.gross_total),
            'bonus_amount': decimal_to_float(self.bonus_amount),
            'bonus_description': self.bonus_description,
            'allowances': decimal_to_float(self.allowances),
            'allowances_description': self.allowances_description,
            'deduction_tax': decimal_to_float(self.deduction_tax),
            'deduction_social_security': decimal_to_float(self.deduction_social_security),
            'deduction_insurance': decimal_to_float(self.deduction_insurance),
            'deduction_uniform': decimal_to_float(self.deduction_uniform),
            'deduction_loan': decimal_to_float(self.deduction_loan),
            'deduction_other': decimal_to_float(self.deduction_other),
            'deduction_other_description': self.deduction_other_description,
            'total_deductions': decimal_to_float(self.total_deductions),
            'net_pay': decimal_to_float(self.net_pay),
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'payment_status': self.payment_status,
            'approved_by': self.approved_by,
            'approved_at': to_iso(self.approved_at),
            'paid_by': self.paid_by,
            'paid_at': to_iso(self.paid_at),
            'payslip_generated': self.payslip_generated,
            'payslip_url': self.payslip_url,
            'notes': self.notes,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Leave(db.Model):
    """Leave / vacation requests."""
    __tablename__ = 'leaves'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    leave_type = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer)
    reason = db.Column(db.Text)
    supporting_document = db.Column(db.String(255))
    leave_status = db.Column(db.String(20), default='pending', index=True)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)
    review_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calculate_days(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.total_days = delta.days + 1
        return self.total_days

    def approve(self, reviewer_id, notes=None):
        self.leave_status = 'approved'
        self.reviewed_by = reviewer_id
        self.reviewed_at = datetime.utcnow()
        self.review_notes = notes
        return True

    def reject(self, reviewer_id, notes):
        self.leave_status = 'rejected'
        self.reviewed_by = reviewer_id
        self.reviewed_at = datetime.utcnow()
        self.review_notes = notes
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'leave_type': self.leave_type,
            'start_date': to_iso(self.start_date),
            'end_date': to_iso(self.end_date),
            'total_days': self.total_days,
            'reason': self.reason,
            'supporting_document': self.supporting_document,
            'leave_status': self.leave_status,
            'requested_at': to_iso(self.requested_at),
            'reviewed_by': self.reviewed_by,
            'reviewed_at': to_iso(self.reviewed_at),
            'review_notes': self.review_notes,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Incident(db.Model):
    """Incident reports."""
    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False, index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendances.id'))
    incident_date = db.Column(db.DateTime, nullable=False, index=True)
    incident_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), default='medium')
    description = db.Column(db.Text, nullable=False)
    action_taken = db.Column(db.Text)
    police_notified = db.Column(db.Boolean, default=False)
    police_report_number = db.Column(db.String(50))
    client_notified = db.Column(db.Boolean, default=False)
    client_notified_at = db.Column(db.DateTime)
    witnesses = db.Column(db.Text)
    evidence_photos = db.Column(JSON)
    incident_status = db.Column(db.String(20), default='open', index=True)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def resolve(self, resolver_id, notes):
        self.incident_status = 'resolved'
        self.resolved_by = resolver_id
        self.resolved_at = datetime.utcnow()
        self.resolution_notes = notes
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'agent_id': self.agent_id,
            'attendance_id': self.attendance_id,
            'incident_date': to_iso(self.incident_date),
            'incident_type': self.incident_type,
            'severity': self.severity,
            'description': self.description,
            'action_taken': self.action_taken,
            'police_notified': self.police_notified,
            'police_report_number': self.police_report_number,
            'client_notified': self.client_notified,
            'client_notified_at': to_iso(self.client_notified_at),
            'witnesses': self.witnesses,
            'evidence_photos': self.evidence_photos,
            'incident_status': self.incident_status,
            'resolved_by': self.resolved_by,
            'resolved_at': to_iso(self.resolved_at),
            'resolution_notes': self.resolution_notes,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Invoice(db.Model):
    """Client invoices."""
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False, index=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    invoice_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    billing_period_start = db.Column(db.Date)
    billing_period_end = db.Column(db.Date)
    subtotal = db.Column(db.Numeric(12, 2), default=0)
    tax_rate = db.Column(db.Numeric(5, 2), default=0)
    tax_amount = db.Column(db.Numeric(12, 2), default=0)
    discount_percentage = db.Column(db.Numeric(5, 2), default=0)
    discount_amount = db.Column(db.Numeric(12, 2), default=0)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    invoice_status = db.Column(db.String(20), default='draft', index=True)
    amount_paid = db.Column(db.Numeric(12, 2), default=0)
    balance_due = db.Column(db.Numeric(12, 2), default=0)
    payment_terms = db.Column(db.String(50))
    notes = db.Column(db.Text)
    invoice_pdf_url = db.Column(db.String(255))
    sent_at = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    line_items = db.relationship('InvoiceLineItem', backref='invoice', lazy='dynamic', cascade='all, delete-orphan')

    def calculate_totals(self):
        self.subtotal = sum(decimal_to_float(item.line_total) for item in self.line_items)
        self.tax_amount = decimal_to_float(self.subtotal) * (decimal_to_float(self.tax_rate) / 100)
        self.discount_amount = decimal_to_float(self.subtotal) * (decimal_to_float(self.discount_percentage) / 100)
        self.total_amount = decimal_to_float(self.subtotal) + decimal_to_float(self.tax_amount) - decimal_to_float(self.discount_amount)
        self.balance_due = decimal_to_float(self.total_amount) - decimal_to_float(self.amount_paid)
        return self.total_amount

    def mark_as_sent(self):
        self.invoice_status = 'sent'
        self.sent_at = datetime.utcnow()
        return True

    def record_payment(self, amount):
        self.amount_paid = decimal_to_float(self.amount_paid) + float(amount)
        self.balance_due = decimal_to_float(self.total_amount) - decimal_to_float(self.amount_paid)
        if self.balance_due <= 0:
            self.invoice_status = 'paid'
            self.paid_at = datetime.utcnow()
        elif self.amount_paid > 0:
            self.invoice_status = 'partial'
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'invoice_number': self.invoice_number,
            'invoice_date': to_iso(self.invoice_date),
            'due_date': to_iso(self.due_date),
            'billing_period_start': to_iso(self.billing_period_start),
            'billing_period_end': to_iso(self.billing_period_end),
            'subtotal': decimal_to_float(self.subtotal),
            'tax_rate': decimal_to_float(self.tax_rate),
            'tax_amount': decimal_to_float(self.tax_amount),
            'discount_percentage': decimal_to_float(self.discount_percentage),
            'discount_amount': decimal_to_float(self.discount_amount),
            'total_amount': decimal_to_float(self.total_amount),
            'invoice_status': self.invoice_status,
            'amount_paid': decimal_to_float(self.amount_paid),
            'balance_due': decimal_to_float(self.balance_due),
            'payment_terms': self.payment_terms,
            'notes': self.notes,
            'invoice_pdf_url': self.invoice_pdf_url,
            'sent_at': to_iso(self.sent_at),
            'paid_at': to_iso(self.paid_at),
            'created_by': self.created_by,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class InvoiceLineItem(db.Model):
    """Invoice line items."""
    __tablename__ = 'invoice_line_items'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False, index=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    line_total = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'site_id': self.site_id,
            'description': self.description,
            'quantity': decimal_to_float(self.quantity),
            'unit_price': decimal_to_float(self.unit_price),
            'line_total': decimal_to_float(self.line_total),
            'created_at': to_iso(self.created_at)
        }


class Training(db.Model):
    """Training definitions."""
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True)
    training_name = db.Column(db.String(200), nullable=False)
    training_type = db.Column(db.String(20))
    duration_hours = db.Column(db.Integer)
    valid_for_months = db.Column(db.Integer)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'training_name': self.training_name,
            'training_type': self.training_type,
            'duration_hours': self.duration_hours,
            'valid_for_months': self.valid_for_months,
            'description': self.description,
            'created_at': to_iso(self.created_at)
        }


class AgentTraining(db.Model):
    """Association between agents and trainings."""
    __tablename__ = 'agent_trainings'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False, index=True)
    completion_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    score = db.Column(db.Numeric(5, 2))
    certificate_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    training = db.relationship('Training')

    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'training_id': self.training_id,
            'completion_date': to_iso(self.completion_date),
            'expiry_date': to_iso(self.expiry_date),
            'score': decimal_to_float(self.score),
            'certificate_url': self.certificate_url,
            'created_at': to_iso(self.created_at),
            'training': self.training.to_dict() if self.training else None
        }


class Equipment(db.Model):
    """Equipment inventory."""
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    equipment_type = db.Column(db.String(50), nullable=False)
    equipment_name = db.Column(db.String(200), nullable=False)
    serial_number = db.Column(db.String(100), unique=True)
    purchase_date = db.Column(db.Date)
    purchase_cost = db.Column(db.Numeric(10, 2))
    condition = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship('EquipmentAssignment', backref='equipment', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'equipment_type': self.equipment_type,
            'equipment_name': self.equipment_name,
            'serial_number': self.serial_number,
            'purchase_date': to_iso(self.purchase_date),
            'purchase_cost': decimal_to_float(self.purchase_cost),
            'condition': self.condition,
            'status': self.status,
            'notes': self.notes,
            'created_at': to_iso(self.created_at)
        }


class EquipmentAssignment(db.Model):
    """Assignments of equipment to agents."""
    __tablename__ = 'equipment_assignments'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False, index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    assigned_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    assignment_status = db.Column(db.String(20), default='active')
    return_condition = db.Column(db.Text)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    agent = db.relationship('Agent')

    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'agent_id': self.agent_id,
            'assigned_date': to_iso(self.assigned_date),
            'return_date': to_iso(self.return_date),
            'assignment_status': self.assignment_status,
            'return_condition': self.return_condition,
            'assigned_by': self.assigned_by,
            'created_at': to_iso(self.created_at),
            'equipment': self.equipment.to_dict() if self.equipment else None,
            'agent': self.agent.to_dict() if self.agent else None
        }


class Document(db.Model):
    """Documents linked to agents, clients, sites or company."""
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50), nullable=False)
    entity_type = db.Column(db.String(20), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    document_name = db.Column(db.String(255))
    file_url = db.Column(db.String(255), nullable=False)
    file_size_kb = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    issue_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'document_type': self.document_type,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'document_name': self.document_name,
            'file_url': self.file_url,
            'file_size_kb': self.file_size_kb,
            'mime_type': self.mime_type,
            'issue_date': to_iso(self.issue_date),
            'expiry_date': to_iso(self.expiry_date),
            'is_verified': self.is_verified,
            'verified_by': self.verified_by,
            'verified_at': to_iso(self.verified_at),
            'uploaded_by': self.uploaded_by,
            'created_at': to_iso(self.created_at),
            'updated_at': to_iso(self.updated_at)
        }


class Notification(db.Model):
    """System notifications."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    notification_type = db.Column(db.String(50))
    title = db.Column(db.String(255))
    message = db.Column(db.Text)
    priority = db.Column(db.String(20), default='normal')
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    action_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'agent_id': self.agent_id,
            'notification_type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'priority': self.priority,
            'is_read': self.is_read,
            'read_at': to_iso(self.read_at),
            'action_url': self.action_url,
            'created_at': to_iso(self.created_at),
            'expires_at': to_iso(self.expires_at)
        }
