from flask import Flask
from app.config import config
from app.extensions import db, migrate, jwt, cors, ma


def create_app(config_name='default'):
    """Application factory pattern.
    why? Allows creating multiple app instances with different configs.
    Essential for testing and running multiple environments.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config.get('CORS_ORIGINS', '*'))
    ma.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Create database tables
    with app.app_context():
        db.create_all()
    return app


def register_blueprints(app):
    """Register all blueprints """
    from app.api.v1 import api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')


def register_error_handlers(app):
    """Register custom error handlers"""
    from flask import jsonify

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Ressource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500
