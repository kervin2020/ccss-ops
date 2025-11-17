from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """System users - admin, managers, supervisors"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), default='manager')  # admin, manager, supervisor, hr, finance
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Agent(db.Model):
    """Security agents"""
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    cin = db.Column(db.String(50), unique=True, nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    photo = db.Column(db.String(255))
    grade = db.Column(db.String(50))
    status = db.Column(db.String(20), default='actif')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='agent', lazy=True)
    payrolls = db.relationship('Payroll', backref='agent', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'cin': self.cin,
            'phone': self.phone,
            'address': self.address,
            'photo': self.photo,
            'grade': self.grade,
            'hourly_rate': self.hourly_rate,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Client(db.Model):
    """Client companies"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    registration_number = db.Column(db.String(50), unique=True)
    primary_contact_name = db.Column(db.String(100), nullable=False)
    primary_contact_phone = db.Column(db.String(20), nullable=False)
    primary_contact_email = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    contract_status = db.Column(db.String(20), default='active')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sites = db.relationship('Site', backref='client', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'registration_number': self.registration_number,
            'primary_contact_name': self.primary_contact_name,
            'primary_contact_phone': self.primary_contact_phone,
            'primary_contact_email': self.primary_contact_email,
            'address': self.address,
            'city': self.city,
            'contract_status': self.contract_status,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Site(db.Model):
    """Work sites"""
    __tablename__ = 'sites'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    site_name = db.Column(db.String(255), nullable=False)
    site_code = db.Column(db.String(20), unique=True)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100))
    required_agents = db.Column(db.Integer, nullable=False, default=1)
    site_status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='site', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'site_name': self.site_name,
            'site_code': self.site_code,
            'address': self.address,
            'city': self.city,
            'required_agents': self.required_agents,
            'site_status': self.site_status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Attendance(db.Model):
    """Attendance records"""
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    clock_in_time = db.Column(db.DateTime)
    clock_out_time = db.Column(db.DateTime)
    total_hours = db.Column(db.Float, default=0.0)
    attendance_status = db.Column(db.String(20), default='present')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    corrections = db.relationship('Correction', backref='attendance', lazy=True)
    
    def calculate_hours(self):
        if self.clock_in_time and self.clock_out_time:
            delta = self.clock_out_time - self.clock_in_time
            self.total_hours = delta.total_seconds() / 3600.0
        return self.total_hours
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'site_id': self.site_id,
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'clock_in_time': self.clock_in_time.isoformat() if self.clock_in_time else None,
            'clock_out_time': self.clock_out_time.isoformat() if self.clock_out_time else None,
            'total_hours': self.total_hours,
            'attendance_status': self.attendance_status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Correction(db.Model):
    """Attendance corrections"""
    __tablename__ = 'corrections'
    
    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendances.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    correction_type = db.Column(db.String(50))
    reason = db.Column(db.Text, nullable=False)
    requested_clock_in = db.Column(db.DateTime)
    requested_clock_out = db.Column(db.DateTime)
    correction_status = db.Column(db.String(20), default='pending')
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_notes = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'attendance_id': self.attendance_id,
            'agent_id': self.agent_id,
            'correction_type': self.correction_type,
            'reason': self.reason,
            'requested_clock_in': self.requested_clock_in.isoformat() if self.requested_clock_in else None,
            'requested_clock_out': self.requested_clock_out.isoformat() if self.requested_clock_out else None,
            'correction_status': self.correction_status,
            'reviewed_by': self.reviewed_by,
            'review_notes': self.review_notes,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Payroll(db.Model):
    """Payroll records"""
    __tablename__ = 'payrolls'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    pay_period_start = db.Column(db.Date, nullable=False)
    pay_period_end = db.Column(db.Date, nullable=False)
    total_hours = db.Column(db.Float, default=0.0)
    hourly_rate = db.Column(db.Float, nullable=False)
    gross_pay = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    net_pay = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.String(20), default='draft')
    payment_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_pay(self):
        self.gross_pay = self.total_hours * self.hourly_rate
        self.net_pay = self.gross_pay - self.deductions
        return self.net_pay
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'pay_period_start': self.pay_period_start.isoformat() if self.pay_period_start else None,
            'pay_period_end': self.pay_period_end.isoformat() if self.pay_period_end else None,
            'total_hours': self.total_hours,
            'hourly_rate': self.hourly_rate,
            'gross_pay': self.gross_pay,
            'deductions': self.deductions,
            'net_pay': self.net_pay,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
