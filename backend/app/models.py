class Agent(db.Model):
    """
    Agent Model - Represents a security agent

    Design Decisions:
    1. Separate name/surname for flexibility in sorting/searching
    2. CIN (ID number) is unique - prevents duplicates
    3. status field allows soft-delete (keep history)
    4. hourly_rate stored as Float for precision
    """
    __tablename__ = 'agents'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Required Fields
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    cin = db.Column(db.String(50), unique=True, nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)

    # Optional Fields
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    photo = db.Column(db.String(255))
    grade = db.Column(db.String(50))

    # Status Management
    status = db.Column(db.String(20), default='actif')

    # Timestamps (audit trail)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (SQLAlchemy handles this)
    attendances = db.relationship('Attendance', backref='agent', lazy=True)
    payrolls = db.relationship('Payroll', backref='agent', lazy=True)

    def to_dict(self):
        """
        Serialization method - converts model to dictionary
        Why: JSON responses need dictionaries, not objects
        """
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
