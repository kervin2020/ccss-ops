from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///security_ops.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS for frontend
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Import models
    from app import models
    
    # Create tables
    with app.app_context():
        db.create_all()
        # Create default admin user if it doesn't exist
        from app.models import User
        if not User.query.filter_by(email='admin@security.com').first():
            admin = User(
                email='admin@security.com',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    # Register blueprints (routes)
    from app.routes import auth, agents, clients, sites, attendances, corrections, payrolls
    app.register_blueprint(auth.bp)
    app.register_blueprint(agents.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(sites.bp)
    app.register_blueprint(attendances.bp)
    app.register_blueprint(corrections.bp)
    app.register_blueprint(payrolls.bp)
    
    return app

