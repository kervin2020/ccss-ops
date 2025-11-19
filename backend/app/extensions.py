""" Initialize extensions here to aboid circular imports.
Extensions are initialized without app (init_app pattern)."""

from flask_sqlalchemy import SQLALchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
ma = Marshmallow()
