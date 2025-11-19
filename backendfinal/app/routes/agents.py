from flask import Blueprint, request, jsonify
from app import db
from app.models import Agent
from flask_jwt_extended import jwt_required

bp = Blueprint('agents', __name__, url_prefix='/api/agents')

@bp.route('', methods=['GET'])
@jwt_required()
def get_agents():
    status = request.args.get('status')
    query = Agent.query
    
    if status:
        query = query.filter_by(status=status)
    
    agents = query.all()
    return jsonify([agent.to_dict() for agent in agents]), 200

@bp.route('/<int:agent_id>', methods=['GET'])
@jwt_required()
def get_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    return jsonify(agent.to_dict()), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_agent():
    data = request.get_json()
    
    required_fields = ['name', 'surname', 'cin', 'hourly_rate']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if Agent.query.filter_by(cin=data['cin']).first():
        return jsonify({'error': 'CIN already exists'}), 400
    
    agent = Agent(
        name=data['name'],
        surname=data['surname'],
        cin=data['cin'],
        hourly_rate=data['hourly_rate'],
        phone=data.get('phone'),
        address=data.get('address'),
        photo=data.get('photo'),
        grade=data.get('grade'),
        status=data.get('status', 'actif')
    )
    
    db.session.add(agent)
    db.session.commit()
    
    return jsonify(agent.to_dict()), 201

@bp.route('/<int:agent_id>', methods=['PUT'])
@jwt_required()
def update_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json()
    
    if 'cin' in data and data['cin'] != agent.cin:
        if Agent.query.filter_by(cin=data['cin']).first():
            return jsonify({'error': 'CIN already exists'}), 400
    
    agent.name = data.get('name', agent.name)
    agent.surname = data.get('surname', agent.surname)
    agent.cin = data.get('cin', agent.cin)
    agent.hourly_rate = data.get('hourly_rate', agent.hourly_rate)
    agent.phone = data.get('phone', agent.phone)
    agent.address = data.get('address', agent.address)
    agent.photo = data.get('photo', agent.photo)
    agent.grade = data.get('grade', agent.grade)
    agent.status = data.get('status', agent.status)
    
    db.session.commit()
    return jsonify(agent.to_dict()), 200

@bp.route('/<int:agent_id>', methods=['DELETE'])
@jwt_required()
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    agent.status = 'inactif'
    db.session.commit()
    return jsonify({'message': 'Agent deactivated'}), 200

