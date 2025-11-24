from flask import Flask, jsonify, request
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
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///security_ops.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Enable CORS for frontend
    # Allow Authorization header so JWT auth works from the browser
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'], supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Friendly JSON responses for JWT errors so frontend can parse them
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        app.logger.warning('JWT unauthorized: %s - Authorization header: %s',
                           reason, request.headers.get('Authorization'))
        return jsonify({'error': reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        # invalid or malformed token -> 422
        app.logger.warning('JWT invalid token: %s - Authorization header: %s',
                           reason, request.headers.get('Authorization'))
        return jsonify({'error': reason}), 422

    @jwt.expired_token_loader
    def expired_token_callback(header, payload):
        return jsonify({'error': 'Token has expired'}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(header, payload):
        return jsonify({'error': 'Token has been revoked'}), 401

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
    from app.routes import (
        auth,
        agents,
        clients,
        sites,
        attendances,
        corrections,
        payrolls,
        shifts,
        leaves,
        incidents,
        invoices,
        equipment,
        trainings,
        documents,
        notifications,
    )
    app.register_blueprint(auth.bp)
    app.register_blueprint(agents.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(sites.bp)
    app.register_blueprint(attendances.bp)
    app.register_blueprint(corrections.bp)
    app.register_blueprint(payrolls.bp)
    app.register_blueprint(shifts.bp)
    app.register_blueprint(leaves.bp)
    app.register_blueprint(incidents.bp)
    app.register_blueprint(invoices.bp)
    app.register_blueprint(equipment.bp)
    app.register_blueprint(trainings.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(notifications.bp)

    return app
