# Complete Guide to Building Production-Ready Flask Backends

## Table of Contents
1. [Understanding Flask Architecture](#architecture)
2. [Project Structure](#structure)
3. [Step-by-Step Setup](#setup)
4. [Core Concepts](#concepts)
5. [Advanced Patterns](#patterns)

---

## 1. Understanding Flask Architecture {#architecture}

### What is Flask?
Flask is a **micro-framework** for Python web development. "Micro" means:
- **Minimal core**: Provides only essential features (routing, request/response handling)
- **Extensible**: Add features through extensions as needed
- **Unopinionated**: Doesn't force specific project structures or tools

### WSGI (Web Server Gateway Interface)
Flask is a WSGI application. Understanding this is crucial:
- **WSGI** is a specification that describes how web servers communicate with Python applications
- Your Flask app is a **WSGI callable** that receives requests and returns responses
- In production, you use a WSGI server (Gunicorn, uWSGI) instead of Flask's development server

### Request-Response Cycle
```
Client → Web Server → WSGI Server → Flask App → Your Code
                                        ↓
                                    Response
                                        ↓
Client ← Web Server ← WSGI Server ← Flask App
```

---

## 2. Production-Grade Project Structure {#structure}

```
my-flask-backend/
│
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration classes
│   ├── extensions.py            # Initialize extensions
│   │
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   │
│   ├── schemas/                 # Data validation (Marshmallow/Pydantic)
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   └── product_schema.py
│   │
│   ├── api/                     # API blueprints
│   │   ├── __init__.py
│   │   ├── v1/                  # API versioning
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── products.py
│   │   └── v2/
│   │       └── __init__.py
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── email_service.py
│   │
│   ├── middleware/              # Custom middleware
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   └── logging_middleware.py
│   │
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── validators.py
│   │   └── helpers.py
│   │
│   └── exceptions/              # Custom exceptions
│       ├── __init__.py
│       └── api_exceptions.py
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── unit/
│   │   ├── test_models.py
│   │   └── test_services.py
│   └── integration/
│       └── test_api.py
│
├── migrations/                  # Database migrations (Alembic)
│   └── versions/
│
├── scripts/                     # Utility scripts
│   ├── seed_db.py
│   └── create_admin.py
│
├── logs/                        # Application logs
│   └── app.log
│
├── .env                         # Environment variables (DO NOT COMMIT)
├── .env.example                 # Template for .env
├── .gitignore
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── pytest.ini                   # Pytest configuration
├── alembic.ini                  # Alembic configuration
├── wsgi.py                      # WSGI entry point
├── manage.py                    # CLI commands
└── README.md
```

### Why This Structure?

**Separation of Concerns**: Each directory has a specific responsibility
- `models/`: Data layer (database schemas)
- `schemas/`: Data validation and serialization
- `api/`: HTTP layer (routes and request handling)
- `services/`: Business logic (reusable across endpoints)
- `utils/`: Helper functions

**Scalability**: Easy to add new features without touching existing code

**Testability**: Clear boundaries make unit testing straightforward

---

## 3. Step-by-Step Setup {#setup}

### Step 1: Environment Setup

#### Create Project Directory
```bash
mkdir my-flask-backend
cd my-flask-backend
```

#### Virtual Environment (CRITICAL)
**Why?** Isolates project dependencies from system Python and other projects.

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Verify activation (should show path to venv)
which python  # Mac/Linux
where python  # Windows
```

**Always activate venv before working on project!**

### Step 2: Install Core Dependencies

```bash
pip install flask
pip install flask-sqlalchemy      # ORM for database
pip install flask-migrate         # Database migrations
pip install flask-jwt-extended    # JWT authentication
pip install flask-cors           # Cross-Origin Resource Sharing
pip install flask-marshmallow    # Serialization/validation
pip install python-dotenv        # Environment variables
pip install gunicorn            # Production WSGI server
pip install psycopg2-binary     # PostgreSQL adapter
```

**Development Dependencies**:
```bash
pip install pytest pytest-cov    # Testing
pip install black flake8         # Code formatting/linting
pip install ipython ipdb         # Debugging
```

**Save dependencies**:
```bash
pip freeze > requirements.txt
```

### Step 3: Configuration System

**`app/config.py`**
```python
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,  # Verify connections before using
    }
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Pagination
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_PER_PAGE = 100
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production must have these set
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.getenv('SECRET_KEY'), 'SECRET_KEY must be set in production'
        assert os.getenv('DATABASE_URL'), 'DATABASE_URL must be set'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

**Why this approach?**
- Environment-specific settings (dev/prod/test)
- Secure defaults with environment variable overrides
- Easy to test with in-memory database

### Step 4: Application Factory Pattern

**`app/__init__.py`**
```python
from flask import Flask
from app.config import config
from app.extensions import db, migrate, jwt, cors, ma

def create_app(config_name='default'):
    """
    Application factory pattern.
    
    Why? Allows creating multiple app instances with different configs.
    Essential for testing and running multiple environments.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
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
    """Register all blueprints"""
    from app.api.v1 import api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

def register_error_handlers(app):
    """Register error handlers"""
    from flask import jsonify
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
```

**`app/extensions.py`**
```python
"""
Initialize extensions here to avoid circular imports.
Extensions are initialized without app (init_app pattern).
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
ma = Marshmallow()
```

**Why Application Factory?**
- Create multiple app instances (testing, production)
- Avoid circular imports
- Initialize extensions cleanly
- Follow Flask best practices

### Step 5: Database Models

**`app/models/user.py`**
```python
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """User model with security best practices"""
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # User Info
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    orders = db.relationship('Order', back_populates='user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash password before storing"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Serialize to dictionary (excluding sensitive data)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
```

**Key Concepts**:
- **Never store plain passwords**: Use `password_hash`
- **Indexes**: Speed up queries on frequently searched columns
- **Timestamps**: Track creation and updates
- **Relationships**: Define how models connect
- **to_dict()**: Safe serialization without sensitive data

### Step 6: Data Validation with Schemas

**`app/schemas/user_schema.py`**
```python
from app.extensions import ma
from app.models.user import User
from marshmallow import fields, validates, ValidationError
import re

class UserSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serialization and validation"""
    
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)  # Never expose password hash
    
    # Custom fields
    password = fields.String(load_only=True, required=True)
    password_confirm = fields.String(load_only=True, required=True)
    
    @validates('email')
    def validate_email(self, value):
        """Validate email format"""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, value):
            raise ValidationError('Invalid email format')
    
    @validates('password')
    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain lowercase letter')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain a number')

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
```

**Why Schemas?**
- **Validation**: Ensure data meets requirements before saving
- **Serialization**: Convert models to JSON
- **Deserialization**: Convert JSON to models
- **Security**: Control which fields are exposed

### Step 7: Business Logic in Services

**`app/services/user_service.py`**
```python
from app.extensions import db
from app.models.user import User
from app.exceptions import UserNotFoundError, DuplicateUserError

class UserService:
    """
    Business logic for user operations.
    
    Why separate from routes?
    - Reusable across different endpoints
    - Easier to test
    - Cleaner code organization
    """
    
    @staticmethod
    def create_user(username, email, password, **kwargs):
        """Create a new user"""
        # Check for duplicates
        if User.query.filter_by(username=username).first():
            raise DuplicateUserError(f'Username {username} already exists')
        
        if User.query.filter_by(email=email).first():
            raise DuplicateUserError(f'Email {email} already exists')
        
        # Create user
        user = User(username=username, email=email, **kwargs)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.query.get(user_id)
        if not user:
            raise UserNotFoundError(f'User {user_id} not found')
        return user
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user"""
        user = UserService.get_user_by_id(user_id)
        
        for key, value in kwargs.items():
            if hasattr(user, key) and key != 'id':
                setattr(user, key, value)
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """Delete user (soft delete)"""
        user = UserService.get_user_by_id(user_id)
        user.is_active = False
        db.session.commit()
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user"""
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return None
        
        if not user.is_active:
            return None
        
        return user
```

### Step 8: API Routes with Blueprints

**`app/api/v1/__init__.py`**
```python
from flask import Blueprint

api_v1_bp = Blueprint('api_v1', __name__)

# Import routes to register them
from app.api.v1 import auth, users
```

**`app/api/v1/users.py`**
```python
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1_bp
from app.services.user_service import UserService
from app.schemas.user_schema import user_schema, users_schema
from marshmallow import ValidationError

@api_v1_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create new user
    
    Request Body:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "SecurePass123"
    }
    """
    try:
        # Validate input
        data = user_schema.load(request.json)
        
        # Create user
        user = UserService.create_user(**data)
        
        # Return created user
        return user_schema.jsonify(user), 201
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_v1_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID (requires authentication)"""
    try:
        user = UserService.get_user_by_id(user_id)
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@api_v1_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """
    List users with pagination
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'users': users_schema.dump(users.items),
        'total': users.total,
        'page': users.page,
        'pages': users.pages
    }), 200

@api_v1_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user (only own profile or admin)"""
    current_user_id = get_jwt_identity()
    
    # Authorization check
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        user = UserService.update_user(user_id, **request.json)
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

**Key Concepts**:
- **Blueprints**: Organize routes into modules
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found)
- **JWT Protection**: `@jwt_required()` decorator protects routes
- **Pagination**: Handle large datasets efficiently

### Step 9: Authentication

**`app/api/v1/auth.py`**
```python
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.api.v1 import api_v1_bp
from app.services.user_service import UserService

@api_v1_bp.route('/auth/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.json
    
    try:
        user = UserService.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_v1_bp.route('/auth/login', methods=['POST'])
def login():
    """Authenticate user and return tokens"""
    data = request.json
    
    user = UserService.authenticate(data['username'], data['password'])
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@api_v1_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Get new access token using refresh token"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({'access_token': access_token}), 200

@api_v1_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)
    
    return jsonify(user.to_dict()), 200
```

**JWT Authentication Flow**:
1. User logs in with credentials
2. Server validates and returns access + refresh tokens
3. Client stores tokens (localStorage/cookies)
4. Client sends access token in Authorization header: `Bearer <token>`
5. Server validates token on protected routes
6. When access token expires, use refresh token to get new one

### Step 10: Error Handling

**`app/exceptions/api_exceptions.py`**
```python
class APIException(Exception):
    """Base API exception"""
    status_code = 400
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv

class UserNotFoundError(APIException):
    status_code = 404

class DuplicateUserError(APIException):
    status_code = 409

class UnauthorizedError(APIException):
    status_code = 401
```

**Register in app factory**:
```python
def register_error_handlers(app):
    from app.exceptions import APIException
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
```

### Step 11: Database Migrations

```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

**Why migrations?**
- Track database schema changes
- Apply changes across environments
- Roll back if needed
- Collaborate with team on schema

### Step 12: Environment Variables

**`.env`**
```
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/mydb
JWT_SECRET_KEY=your-jwt-secret
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**`.env.example`** (commit this, not .env)
```
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=change-me
DATABASE_URL=postgresql://user:password@localhost/dbname
JWT_SECRET_KEY=change-me
CORS_ORIGINS=http://localhost:3000
```

**Load in app**:
```python
from dotenv import load_dotenv
load_dotenv()  # Load .env file
```

### Step 13: WSGI Entry Point

**`wsgi.py`**
```python
"""
WSGI entry point for production servers.
Usage: gunicorn wsgi:app
"""
import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app.run()
```

### Step 14: CLI Commands

**`manage.py`**
```python
import click
from app import create_app, db
from app.models.user import User

app = create_app()

@app.cli.command()
def init_db():
    """Initialize database"""
    db.create_all()
    click.echo('Database initialized')

@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    admin = User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    click.echo('Database seeded')

if __name__ == '__main__':
    app.cli()
```

---

## 4. Core Concepts {#concepts}

### Request Lifecycle

1. **Client sends request** → HTTP request to server
2. **WSGI server receives** → Converts to Python-friendly format
3. **Flask routing** → Matches URL to view function
4. **Before request hooks** → Middleware/authentication
5. **View function executes** → Your code runs
6. **Response created** → Data serialized to JSON
7. **After request hooks** → Logging/cleanup
8. **Response sent** → Back to client

### Database Transactions

```python
try:
    db.session.add(user)
    db.session.commit()  # Persist changes
except Exception as e:
    db.session.rollback()  # Undo changes
    raise e
```

**ACID Properties**:
- **Atomic**: All or nothing
- **Consistent**: Valid state always
- **Isolated**: Transactions don't interfere
- **Durable**: Changes persist after commit

### Middleware

Middleware runs before/after requests:

```python
@app.before_request
def log_request():
    """Log every request"""
    print(f'{request.method} {request.path}')

@app.after_request
def add_header(response):
    """Add custom header to all responses"""
    response.headers['X-Custom-Header'] = 'Value'
    return response
```

---

## 5. Advanced Patterns {#patterns}

### Dependency Injection
```python
class EmailService:
    def send_email(self, to, subject, body):
        pass

class UserService:
    def __init__(self, email_service=None):
        self.email_service = email_service or EmailService()
    
    def create_user(self, data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        self.email_service.send_email(
            user.email,
            'Welcome!',
            f'Hi {user.username}'
        )
```

### Repository Pattern
```python
class UserRepository:
    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()
```

### Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/users/<int:user_id>')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_user(user_id):
    return User.query.get(user_id).to_dict()
```

### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/expensive')
@limiter.limit("10 per minute")
def expensive_operation():
    pass
```

### Background Tasks (Celery)
```python
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379/0')

@celery.task
def send_email_async(to, subject, body):
    # Long-running task
    pass

# In your route
@app.route('/send-email')
def trigger_email():
    send_email_async.delay('user@example.com', 'Hello', 'Body')
    return {'message': 'Email queued'}
```

---

## Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Development
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run

# Database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Production
gunicorn -w 4 -b 0.0.0.0:8000