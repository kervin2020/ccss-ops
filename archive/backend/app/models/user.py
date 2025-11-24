from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    """User Model with Security best practices"""
    __tablename__ = 'users'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # User Info
    username = db.Column(db.String(80), unique=True,
                         nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Profile
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
