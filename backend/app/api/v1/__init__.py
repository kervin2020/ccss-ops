"""API v1 blueprint."""
from flask import Blueprint

api_v1_bp = Blueprint('api_v1', __name__)


@api_v1_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return {'status': 'ok', 'message': 'API v1 is running'}, 200

