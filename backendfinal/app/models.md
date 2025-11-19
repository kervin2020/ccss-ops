from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    """System users - admin, managers, supervisors, HR, finance"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), default='manager')  # admin, manager, supervisor, hr, finance
    
    # Additional fields
    profile_picture = db.Column(db.String(255))
    department = db.Column(db.String(100))  # RH, Finance, Operations
    permissions = db.Column(JSON)  # Granular permissions
    two_factor_enabled = db.Column(db.Boolean, default=False)
    password_reset_token = db.Column(db.String(255))
    password_reset_expires = db.Column(db.DateTime)
    
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
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
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Agent(db.Model):
    """Security agents/guards"""
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # Personal Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))  # M, F, Other
    national_id = db.Column(db.String(50), unique=True, index=True)  # CIN
    
    # Contact Information
    phone_primary = db.Column(db.String(20), nullable=False)
    phone_secondary = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    
    # Emergency Contact
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_relationship = db.Column(db.String(50))
    
    # Employment Information
    hire_date = db.Column(db.Date, nullable=False)
    contract_type = db.Column(db.String(20), default='permanent')  # permanent, temporary, contract
    contract_end_date = db.Column(db.Date)
    employment_status = db.Column(db.String(20), default='active', index=True)  # active, suspended, terminated, on_leave
    termination_date = db.Column(db.Date)
    termination_reason = db.Column(db.Text)
    
    # Financial Information
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    bank_name = db.Column(db.String(100))
    bank_account_number = db.Column(db.String(50))
    tax_id = db.Column(db.String(50))
    
    # Security & Uniform
    uniform_size = db.Column(db.String(10))
    badge_number = db.Column(db.String(20), unique=True)
    security_clearance_level = db.Column(db.Integer, default=1)  # 1-5
    has_firearm_license = db.Column(db.Boolean, default=False)
    firearm_license_number = db.Column(db.String(50))
    firearm_license_expiry = db.Column(db.Date)
    
    # Additional Information
    blood_type = db.Column(db.String(5))
    has_drivers_license = db.Column(db.Boolean, default=False)
    drivers_license_number = db.Column(db.String(50))
    languages_spoken = db.Column(JSON)  # ['French', 'English', 'Creole']
    medical_conditions = db.Column(db.Text)  # Should be encrypted in production
    training_level = db.Column(db.String(50))  # Basic, Advanced, Specialized
    
    profile_photo = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    attendances = db.relationship('Attendance', backref='agent', lazy='dynamic')
    payrolls = db.relationship('Payroll', backref='agent', lazy='dynamic')
    shifts = db.relationship('Shift', backref='agent', lazy='dynamic')
    corrections = db.relationship('Correction', backref='agent', lazy='dynamic')
    leaves = db.relationship('Leave', backref='agent', lazy='dynamic')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.utcnow().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_code': self.employee_code,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
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
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'contract_type': self.contract_type,
            'contract_end_date': self.contract_end_date.isoformat() if self.contract_end_date else None,
            'employment_status': self.employment_status,
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'termination_reason': self.termination_reason,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else 0,
            'bank_name': self.bank_name,
            'bank_account_number': self.bank_account_number,
            'tax_id': self.tax_id,
            'uniform_size': self.uniform_size,
            'badge_number': self.badge_number,
            'security_clearance_level': self.security_clearance_level,
            'has_firearm_license': self.has_firearm_license,
            'firearm_license_number': self.firearm_license_number,
            'firearm_license_expiry': self.firearm_license_expiry.isoformat() if self.firearm_license_expiry else None,
            'blood_type': self.blood_type,
            'has_drivers_license': self.has_drivers_license,
            'drivers_license_number': self.drivers_license_number,
            'languages_spoken': self.languages_spoken,
            'training_level': self.training_level,
            'profile_photo': self.profile_photo,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Client(db.Model):
    """Client companies"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Company Information
    company_name = db.Column(db.String(255), nullable=False)
    company_registration_number = db.Column(db.String(50), unique=True)
    tax_id = db.Column(db.String(50))
    industry_sector = db.Column(db.String(100))
    
    # Primary Contact
    primary_contact_name = db.Column(db.String(100), nullable=False)
    primary_contact_title = db.Column(db.String(100))
    primary_contact_phone = db.Column(db.String(20), nullable=False)
    primary_contact_email = db.Column(db.String(255), nullable=False)
    
    # Billing Contact
    billing_contact_name = db.Column(db.String(100))
    billing_contact_phone = db.Column(db.String(20))
    billing_contact_email = db.Column(db.String(255))
    
    # Address
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10))
    country = db.Column(db.String(100), default='Haiti')
    
    # Contract Information
    contract_start_date = db.Column(db.Date, nullable=False)
    contract_end_date = db.Column(db.Date)
    contract_status = db.Column(db.String(20), default='active', index=True)  # active, pending, suspended, terminated
    payment_terms = db.Column(db.String(20), default='30_days')  # 15_days, 30_days, 45_days, 60_days
    billing_frequency = db.Column(db.String(20), default='monthly')  # weekly, bi-weekly, monthly
    billing_day = db.Column(db.Integer)  # Day of month (1-31)
    currency = db.Column(db.String(3), default='HTG')
    
    # Financial Information
    credit_limit = db.Column(db.Numeric(12, 2), default=0)
    current_balance = db.Column(db.Numeric(12, 2), default=0)
    total_invoiced = db.Column(db.Numeric(12, 2), default=0)
    total_paid = db.Column(db.Numeric(12, 2), default=0)
    
    # Additional Information
    discount_percentage = db.Column(db.Numeric(5, 2), default=0)
    service_level_agreement = db.Column(db.Text)
    special_requirements = db.Column(db.Text)
    requires_background_check = db.Column(db.Boolean, default=False)
    requires_drug_testing = db.Column(db.Boolean, default=False)
    insurance_certificate_required = db.Column(db.Boolean, default=False)
    preferred_communication_method = db.Column(db.String(20), default='email')  # email, phone, sms, whatsapp
    
    logo_url = db.Column(db.String(255))
    website = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
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
            'contract_start_date': self.contract_start_date.isoformat() if self.contract_start_date else None,
            'contract_end_date': self.contract_end_date.isoformat() if self.contract_end_date else None,
            'contract_status': self.contract_status,
            'payment_terms': self.payment_terms,
            'billing_frequency': self.billing_frequency,
            'billing_day': self.billing_day,
            'currency': self.currency,
            'credit_limit': float(self.credit_limit) if self.credit_limit else 0,
            'current_balance': float(self.current_balance) if self.current_balance else 0,
            'total_invoiced': float(self.total_invoiced) if self.total_invoiced else 0,
            'total_paid': float(self.total_paid) if self.total_paid else 0,
            'discount_percentage': float(self.discount_percentage) if self.discount_percentage else 0,
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
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Site(db.Model):
    """Work sites/locations"""
    __tablename__ = 'sites'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False, index=True)
    
    # Site Information
    site_name = db.Column(db.String(255), nullable=False)
    site_code = db.Column(db.String(20), unique=True, index=True)
    site_type = db.Column(db.String(50))  # office, warehouse, retail, residential, industrial, event, construction, other
    
    # Location
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    gps_latitude = db.Column(db.Numeric(10, 8))
    gps_longitude = db.Column(db.Numeric(11, 8))
    geofence_radius_meters = db.Column(db.Integer, default=100)
    
    # Site Contact
    site_contact_name = db.Column(db.String(100))
    site_contact_phone = db.Column(db.String(20))
    site_contact_email = db.Column(db.String(255))
    
    # Requirements
    required_agents = db.Column(db.Integer, nullable=False, default=1)
    shift_pattern = db.Column(db.String(50))  # 24/7, 8h-17h, rotating
    access_instructions = db.Column(db.Text)
    emergency_procedures = db.Column(db.Text)
    special_equipment_required = db.Column(db.Text)
    
    # Security Requirements
    requires_armed_guard = db.Column(db.Boolean, default=False)
    requires_dog_unit = db.Column(db.Boolean, default=False)
    requires_vehicle = db.Column(db.Boolean, default=False)
    minimum_clearance_level = db.Column(db.Integer, default=1)
    
    # Financial
    hourly_rate_override = db.Column(db.Numeric(10, 2))
    billing_rate = db.Column(db.Numeric(10, 2))
    
    # Contract
    contract_start_date = db.Column(db.Date)
    contract_end_date = db.Column(db.Date)
    site_status = db.Column(db.String(20), default='active', index=True)  # active, inactive, pending, closed
    
    # Additional Information
    patrol_checkpoints = db.Column(JSON)
    restricted_areas = db.Column(JSON)
    key_holder_contacts = db.Column(JSON)
    alarm_code = db.Column(db.String(50))  # Should be encrypted
    wifi_ssid = db.Column(db.String(100))
    wifi_password = db.Column(db.String(100))  # Should be encrypted
    
    site_photo = db.Column(db.String(255))
    site_map = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
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
            'gps_latitude': float(self.gps_latitude) if self.gps_latitude else None,
            'gps_longitude': float(self.gps_longitude) if self.gps_longitude else None,
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
            'hourly_rate_override': float(self.hourly_rate_override) if self.hourly_rate_override else None,
            'billing_rate': float(self.billing_rate) if self.billing_rate else None,
            'contract_start_date': self.contract_start_date.isoformat() if self.contract_start_date else None,
            'contract_end_date': self.contract_end_date.isoformat() if self.contract_end_date else None,
            'site_status': self.site_status,
            'patrol_checkpoints': self.patrol_checkpoints,
            'restricted_areas': self.restricted_areas,
            'key_holder_contacts': self.key_holder_contacts,
            'site_photo': self.site_photo,
            'site_map': self.site_map,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Shift(db.Model):
    """Scheduled shifts"""
    __tablename__ = 'shifts'
    
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False, index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    
    shift_date = db.Column(db.Date, nullable=False, index=True)
    shift_type = db.Column(db.String(20))  # day, night, swing, split
    scheduled_start_time = db.Column(db.Time, nullable=False)
    scheduled_end_time = db.Column(db.Time, nullable=False)
    scheduled_hours = db.Column(db.Numeric(5, 2))
    
    shift_status = db.Column(db.String(20), default='scheduled')  # scheduled, confirmed, in_progress, completed, no_show, cancelled
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_at = db.Column(db.DateTime)
    
    special_instructions = db.Column(db.Text)
    required_equipment = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance = db.relationship('Attendance', backref='shift', uselist=False, lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'agent_id': self.agent_id,
            'shift_date': self.shift_date.isoformat() if self.shift_date else None,
            'shift_type': self.shift_type,
            'scheduled_start_time': self.scheduled_start_time.isoformat() if self.scheduled_start_time else None,
            'scheduled_end_time': self.scheduled_end_time.isoformat() if self.scheduled_end_time else None,
            'scheduled_hours': float(self.scheduled_hours) if self.scheduled_hours else 0,
            'shift_status': self.shift_status,
            'assigned_by': self.assigned_by,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'special_instructions': self.special_instructions,
            'required_equipment': self.required_equipment,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Attendance(db.Model):
    """Actual attendance records"""
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False, index=True)
    attendance_date = db.Column(db.Date, nullable=False, index=True)
    
    # Clock In
    clock_in_time = db.Column(db.DateTime)
    clock_in_method = db.Column(db.String(20))  # gps, biometric, manual, qr_code, nfc
    clock_in_gps_lat = db.Column(db.Numeric(10, 8))
    clock_in_gps_lng = db.Column(db.Numeric(11, 8))
    clock_in_photo = db.Column(db.String(255))
    clock_in_verified = db.Column(db.Boolean, default=False)
    
    # Clock Out
    clock_out_time = db.Column(db.DateTime)
    clock_out_method = db.Column(db.String(20))
    clock_out_gps_lat = db.Column(db.Numeric(10, 8))
    clock_out_gps_lng = db.Column(db.Numeric(11, 8))
    clock_out_photo = db.Column(db.String(255))
    clock_out_verified = db.Column(db.Boolean, default=False)
    
    # Hours Calculation
    total_hours = db.Column(db.Numeric(5, 2), default=0)
    regular_hours = db.Column(db.Numeric(5, 2), default=0)
    overtime_hours = db.Column(db.Numeric(5, 2), default=0)
    night_shift_hours = db.Column(db.Numeric(5, 2), default=0)
    holiday_hours = db.Column(db.Numeric(5, 2), default=0)
    
    # Break
    break_start_time = db.Column(db.DateTime)
    break_end_time = db.Column(db.DateTime)
    total_break_minutes = db.Column(db.Integer, default=0)
    
    # Status
    attendance_status = db.Column(db.String(20), default='present')  # present, late, early_departure, absent, no_show, on_leave, sick
    is_late = db.Column(db.Boolean, default=False)
    late_minutes = db.Column(db.Integer, default=0)
    early_departure = db.Column(db.Boolean, default=False)
    early_departure_minutes = db.Column(db.Integer, default=0)
    
    # Incident
    incident_reported = db.Column(db.Boolean, default=False)
    incident_description = db.Column(db.Text)
    
    # Verification
    supervisor_notes = db.Column(db.Text)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    
    # Correction
    requires_correction = db.Column(db.Boolean, default=False)
    correction_reason = db.Column(db.Text)
    
    # Additional
    device_id = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    attendance_signature = db.Column(db.String(255))
    weather_condition = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    corrections = db.relationship('Correction', backref='attendance', lazy='dynamic')
    
    def calculate_hours(self):
        """Calculate total hours worked"""
        if self.clock_in_time and self.clock_out_time:
            delta = self.clock_out_time - self.clock_in_time
            total_seconds = delta.total_seconds()
            
            # Subtract break time
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
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'clock_in_time': self.clock_in_time.isoformat() if self.clock_in_time else None,
            'clock_in_method': self.clock_in_method,
            'clock_in_gps_lat': float(self.clock_in_gps_lat) if self.clock_in_gps_lat else None,
            'clock_in_gps_lng': float(self.clock_in_gps_lng) if self.clock_in_gps_lng else None,
            'clock_in_photo': self.clock_in_photo,
            'clock_in_verified': self.clock_in_verified,
            'clock_out_time': self.clock_out_time.isoformat() if self.clock_out_time else None,
            'clock_out_method': self.clock_out_method,
            'clock_out_gps_lat': float(self.clock_out_gps_lat) if self.clock_out_gps_lat else None,
            'clock_out_gps_lng': float(self.clock_out_gps_lng) if self.clock_out_gps_lng else None,
            'clock_out_photo': self.clock_out_photo,
            'clock_out_verified': self.clock_out_verified,
            'total_hours': float(self.total_hours) if self.total_hours else 0,
            'regular_hours': float(self.regular_hours) if self.regular_hours else 0,
            'overtime_hours': float(self.overtime_hours) if self.overtime_hours else 0,
            'night_shift_hours': float(self.night_shift_hours) if self.night_shift_hours else 0,
            'holiday_hours': float(self.holiday_hours) if self.holiday_hours else 0,
            'break_start_time': self.break_start_time.isoformat() if self.break_start_time else None,
            'break_end_time': self.break_end_time.isoformat() if self.break_end_time else None,
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
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'requires_correction': self.requires_correction,
            'correction_reason': self.correction_reason,
            'device_id': self.device_id,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Correction(db.Model):
    """Attendance correction requests"""
    __tablename__ = 'corrections'
    
    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendances.id'), nullable=False, index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    correction_type = db.Column(db.String(50))  # missed_clock_in, missed_clock_out, wrong_time, wrong_site, system_error, other
    reason = db.Column(db.Text, nullable=False)
    
    # Original values
    original_clock_in = db.Column(db.DateTime)
    original_clock_out = db.Column(db.DateTime)
    
    # Requested values
    requested_clock_in = db.Column(db.DateTime)
    requested_clock_out = db.Column(db.DateTime)
    
    supporting_document = db.Column(db.String(255))
    
    # Status
    correction_status = db.Column(db.String(20), default='pending', index=True)  # pending, approved, rejected, cancelled
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_notes = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime)
    applied_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def approve(self, reviewer_id, notes=None):
        """Approve correction and update attendance"""
        self.correction_status = 'approved'
        self.reviewed_by = reviewer_id
        self.review_notes = notes
        self.reviewed_at = datetime.utcnow()
        self.applied_at = datetime.utcnow()
        
        # Update attendance record
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
        """Reject correction request"""
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
            'original_clock_in': self.original_clock_in.isoformat() if self.original_clock_in else None,
            'original_clock_out': self.original_clock_out.isoformat() if self.original_clock_out else None,
            'requested_clock_in': self.requested_clock_in.isoformat() if self.requested_clock_in else None,
            'requested_clock_out': self.requested_clock_out.isoformat() if self.requested_clock_out else None,
            'supporting_document': self.supporting_document,
            'correction_status': self.correction_status,
            'reviewed_by': self.reviewed_by,
            'review_notes': self.review_notes,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Payroll(db.Model):
    """Payroll/salary records"""
    __tablename__ = 'payrolls'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    
    # Pay Period
    pay_period_start = db.Column(db.Date, nullable=False, index=True)
    pay_period_end = db.Column(db.Date, nullable=False, index=True)
    payment_date = db.Column(db.Date)
    
    # Hours
    total_regular_hours = db.Column(db.Numeric(7, 2), default=0)
    total_overtime_hours = db.Column(db.Numeric(7, 2), default=0)
    total_night_shift_hours = db.Column(db.Numeric(7, 2), default=0)
    total_holiday_hours = db.Column(db.Numeric(7, 2), default=0)
    
    # Rates
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    overtime_rate = db.Column(db.Numeric(10, 2))  # Usually 1.5x
    night_shift_rate = db.Column(db.Numeric(10, 2))
    holiday_rate = db.Column(db.Numeric(10, 2))  # Usually 2x
    
    # Gross Pay
    gross_regular_pay = db.Column(db.Numeric(12, 2), default=0)
    gross_overtime_pay = db.Column(db.Numeric(12, 2), default=0)
    gross_night_shift_pay = db.Column(db.Numeric(12, 2), default=0)
    gross_holiday_pay = db.Column(db.Numeric(12, 2), default=0)
    gross_total = db.Column(db.Numeric(12, 2), default=0)
    
    # Bonuses & Allowances
    bonus_amount = db.Column(db.Numeric(12, 2), default=0)
    bonus_description = db.Column(db.Text)
    allowances = db.Column(db.Numeric(12, 2), default=0)  # Transport, meals
    allowances_description = db.Column(db.Text)
    
    # Deductions
    deduction_tax = db.Column(db.Numeric(12, 2), default=0)
    deduction_social_security = db.Column(db.Numeric(12, 2), default=0)
    deduction_insurance = db.Column(db.Numeric(12, 2), default=0)
    deduction_uniform = db.Column(db.Numeric(12, 2), default=0)
    deduction_loan = db.Column(db.Numeric(12, 2), default=0)
    deduction_other = db.Column(db.Numeric(12, 2), default=0)
    deduction_other_description = db.Column(db.Text)
    total_deductions = db.Column(db.Numeric(12, 2), default=0)
    
    # Net Pay
    net_pay = db.Column(db.Numeric(12, 2), default=0)
    
    # Payment Info
    payment_method = db.Column(db.String(20))  # bank_transfer, cash, check, mobile_money
    payment_reference = db.Column(db.String(100))
    payment_status = db.Column(db.String(20), default='draft', index=True)  # draft, approved, paid, cancelled
    
    # Approval
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    paid_at = db.Column(db.DateTime)
    
    # Payslip
    payslip_generated = db.Column(db.Boolean, default=False)
    payslip_url = db.Column(db.String(255))
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_gross_pay(self):
        """Calculate all gross pay components"""
        self.gross_regular_pay = float(self.total_regular_hours or 0) * float(self.hourly_rate or 0)
        
        overtime_rate = float(self.overtime_rate or 0) or (float(self.hourly_rate or 0) * 1.5)
        self.gross_overtime_pay = float(self.total_overtime_hours or 0) * overtime_rate
        
        night_rate = float(self.night_shift_rate or 0) or float(self.hourly_rate or 0)
        self.gross_night_shift_pay = float(self.total_night_shift_hours or 0) * night_rate
        
        holiday_rate = float(self.holiday_rate or 0) or (float(self.hourly_rate or 0) * 2.0)
        self.gross_holiday_pay = float(self.total_holiday_hours or 0) * holiday_rate
        
        self.gross_total = (self.gross_regular_pay + self.gross_overtime_pay + 
                           self.gross_night_shift_pay + self.gross_holiday_pay)
        return self.gross_total
    
    def calculate_total_deductions(self):
        """Calculate total deductions"""
        self.total_deductions = (
            float(self.deduction_tax or 0) +
            float(self.deduction_social_security or 0) +
            float(self.deduction_insurance or 0) +
            float(self.deduction_uniform or 0) +
            float(self.deduction_loan or 0) +
            float(self.deduction_other or 0)
        )
        return self.total_deductions
    
    def calculate_net_pay(self):
        """Calculate final net pay"""
        self.calculate_gross_pay()
        self.calculate_total_deductions()
        
        self.net_pay = (
            float(self.gross_total or 0) +
            float(self.bonus_amount or 0) +
            float(self.allowances or 0) -
            float(self.total_deductions or 0)
        )
        return self.net_pay
    
    def approve(self, approver_id):
        """Approve payroll"""
        self.payment_status = 'approved'
        self.approved_by = approver_id
        self.approved_at = datetime.utcnow()
        return True
    
    def mark_as_paid(self, paid_by_id, payment_ref=None):
        """Mark payroll as paid"""
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
            'pay_period_start': self.pay_period_start.isoformat() if self.pay_period_start else None,
            'pay_period_end': self.pay_period_end.isoformat() if self.pay_period_end else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'total_regular_hours': float(self.total_regular_hours) if self.total_regular_hours else 0,
            'total_overtime_hours': float(self.total_overtime_hours) if self.total_overtime_hours else 0,
            'total_night_shift_hours': float(self.total_night_shift_hours) if self.total_night_shift_hours else 0,
            'total_holiday_hours': float(self.total_holiday_hours) if self.total_holiday_hours else 0,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else 0,
            'overtime_rate': float(self.overtime_rate) if self.overtime_rate else 0,
            'night_shift_rate': float(self.night_shift_rate) if self.night_shift_rate else 0,
            'holiday_rate': float(self.holiday_rate) if self.holiday_rate else 0,
            'gross_regular_pay': float(self.gross_regular_pay) if self.gross_regular_pay else 0,
            'gross_overtime_pay': float(self.gross_overtime_pay) if self.gross_overtime_pay else 0,
            'gross_night_shift_pay': float(self.gross_night_shift_pay) if self.gross_night_shift_pay else 0,
            'gross_holiday_pay': float(self.gross_holiday_pay) if self.gross_holiday_pay else 0,
            'gross_total': float(self.gross_total) if self.gross_total else 0,
            'bonus_amount': float(self.bonus_amount) if self.bonus_amount else 0,
            'bonus_description': self.bonus_description,
            'allowances': float(self.allowances) if self.allowances else 0,
            'allowances_description': self.allowances_description,
            'deduction_tax': float(self.deduction_tax) if self.deduction_tax else 0,
            'deduction_social_security': float(self.deduction_social_security) if self.deduction_social_security else 0,
            'deduction_insurance': float(self.deduction_insurance) if self.deduction_insurance else 0,
            'deduction_uniform': float(self.deduction_uniform) if self.deduction_uniform else 0,
            'deduction_loan': float(self.deduction_loan) if self.deduction_loan else 0,
            'deduction_other': float(self.deduction_other) if self.deduction_other else 0,
            'deduction_other_description': self.deduction_other_description,
            'total_deductions': float(self.total_deductions) if self.total_deductions else 0,
            'net_pay': float(self.net_pay) if self.net_pay else 0,
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'payment_status': self.payment_status,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'paid_by': self.paid_by,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'payslip_generated': self.payslip_generated,
            'payslip_url': self.payslip_url,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Leave(db.Model):
    """Leave/vacation requests"""
    __tablename__ = 'leaves'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    
    leave_type = db.Column(db.String(20), nullable=False)  # vacation, sick, personal, maternity, paternity, bereavement, unpaid, other
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer)
    reason = db.Column(db.Text)
    supporting_document = db.Column(db.String(255))
    
    leave_status = db.Column(db.String(20), default='pending', index=True)  # pending, approved, rejected, cancelled
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)
    review_notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_days(self):
        """Calculate total days"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.total_days = delta.days + 1
        return self.total_days
    
    def approve(self, reviewer_id, notes=None):
        """Approve leave request"""
        self.leave_status = 'approved'
        self.reviewed_by = reviewer_id
        self.reviewed_at = datetime.utcnow()
        self.review_notes = notes
        return True
    
    def reject(self, reviewer_id, notes):
        """Reject leave request"""
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
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'total_days': self.total_days,
            'reason': self.reason,
            'supporting_document': self.supporting_document,
            'leave_status': self.leave_status,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'reviewed_by': self.reviewed_by,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'review_notes': self.review_notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Incident(db.Model):
    """Incident reports"""
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False, index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False, index=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendances.id'))
    
    incident_date = db.Column(db.DateTime, nullable=False, index=True)
    incident_type = db.Column(db.String(50), nullable=False)  # theft, vandalism, trespassing, fire, medical, suspicious_activity, equipment_failure, other
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    
    description = db.Column(db.Text, nullable=False)
    action_taken = db.Column(db.Text)
    
    police_notified = db.Column(db.Boolean, default=False)
    police_report_number = db.Column(db.String(50))
    client_notified = db.Column(db.Boolean, default=False)
    client_notified_at = db.Column(db.DateTime)
    
    witnesses = db.Column(db.Text)
    evidence_photos = db.Column(JSON)  # Array of photo URLs
    
    incident_status = db.Column(db.String(20), default='open', index=True)  # open, investigating, resolved, closed
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def resolve(self, resolver_id, notes):
        """Resolve incident"""
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
            'incident_date': self.incident_date.isoformat() if self.incident_date else None,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'description': self.description,
            'action_taken': self.action_taken,
            'police_notified': self.police_notified,
            'police_report_number': self.police_report_number,
            'client_notified': self.client_notified,
            'client_notified_at': self.client_notified_at.isoformat() if self.client_notified_at else None,
            'witnesses': self.witnesses,
            'evidence_photos': self.evidence_photos,
            'incident_status': self.incident_status,
            'resolved_by': self.resolved_by,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolution_notes': self.resolution_notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Invoice(db.Model):
    """Client invoices"""
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
    
    invoice_status = db.Column(db.String(20), default='draft', index=True)  # draft, sent, paid, partial, overdue, cancelled
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
    
    # Relationships
    line_items = db.relationship('InvoiceLineItem', backref='invoice', lazy='dynamic', cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Calculate invoice totals"""
        self.subtotal = sum(float(item.line_total or 0) for item in self.line_items)
        self.tax_amount = float(self.subtotal or 0) * (float(self.tax_rate or 0) / 100)
        self.discount_amount = float(self.subtotal or 0) * (float(self.discount_percentage or 0) / 100)
        self.total_amount = float(self.subtotal or 0) + float(self.tax_amount or 0) - float(self.discount_amount or 0)
        self.balance_due = float(self.total_amount or 0) - float(self.amount_paid or 0)
        return self.total_amount
    
    def mark_as_sent(self):
        """Mark invoice as sent"""
        self.invoice_status = 'sent'
        self.sent_at = datetime.utcnow()
        return True
    
    def record_payment(self, amount):
        """Record a payment"""
        self.amount_paid = float(self.amount_paid or 0) + float(amount)
        self.balance_due = float(self.total_amount or 0) - float(self.amount_paid or 0)
        
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
            'invoice_date': self.invoice_date.isoformat() if self.invoice_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'billing_period_start': self.billing_period_start.isoformat() if self.billing_period_start else None,
            'billing_period_end': self.billing_period_end.isoformat() if self.billing_period_end else None,
            'subtotal': float(self.subtotal) if self.subtotal else 0,
            'tax_rate': float(self.tax_rate) if self.tax_rate else 0,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0,
            'discount_percentage': float(self.discount_percentage) if self.discount_percentage else 0,
            'discount_amount': float(self.discount_amount) if self.discount_amount else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'invoice_status': self.invoice_status,
            'amount_paid': float(self.amount_paid) if self.amount_paid else 0,
            'balance_due': float(self.balance_due) if self.balance_due else 0,
            'payment_terms': self.payment_terms,
            'notes': self.notes,
            'invoice_pdf_url': self.invoice_pdf_url,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class InvoiceLineItem(db.Model):
    """Invoice line items"""
    __tablename__ = 'invoice_line_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False, index=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
    
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable