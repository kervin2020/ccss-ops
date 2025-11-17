from flask import Blueprint, request, jsonify
from app import db
from app.models import Payroll, Agent, Attendance
from flask_jwt_extended import jwt_required
from datetime import datetime, date

bp = Blueprint('payrolls', __name__, url_prefix='/api/payrolls')

@bp.route('', methods=['GET'])
@jwt_required()
def get_payrolls():
    agent_id = request.args.get('agent_id')
    status = request.args.get('status')
    
    query = Payroll.query
    
    if agent_id:
        query = query.filter_by(agent_id=agent_id)
    if status:
        query = query.filter_by(payment_status=status)
    
    payrolls = query.order_by(Payroll.pay_period_start.desc()).all()
    return jsonify([pay.to_dict() for pay in payrolls]), 200

@bp.route('/<int:payroll_id>', methods=['GET'])
@jwt_required()
def get_payroll(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    return jsonify(payroll.to_dict()), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_payroll():
    data = request.get_json()
    
    required_fields = ['agent_id', 'pay_period_start', 'pay_period_end']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    agent = Agent.query.get_or_404(data['agent_id'])
    
    # Calculate total hours from attendances
    start_date = datetime.fromisoformat(data['pay_period_start']).date() if isinstance(data['pay_period_start'], str) else data['pay_period_start']
    end_date = datetime.fromisoformat(data['pay_period_end']).date() if isinstance(data['pay_period_end'], str) else data['pay_period_end']
    
    attendances = Attendance.query.filter(
        Attendance.agent_id == data['agent_id'],
        Attendance.attendance_date >= start_date,
        Attendance.attendance_date <= end_date
    ).all()
    
    total_hours = sum(att.total_hours for att in attendances)
    
    payroll = Payroll(
        agent_id=data['agent_id'],
        pay_period_start=start_date,
        pay_period_end=end_date,
        total_hours=total_hours,
        hourly_rate=data.get('hourly_rate', agent.hourly_rate),
        deductions=data.get('deductions', 0.0),
        payment_status=data.get('payment_status', 'draft'),
        notes=data.get('notes')
    )
    
    payroll.calculate_pay()
    
    db.session.add(payroll)
    db.session.commit()
    
    return jsonify(payroll.to_dict()), 201

@bp.route('/<int:payroll_id>', methods=['PUT'])
@jwt_required()
def update_payroll(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    data = request.get_json()
    
    payroll.hourly_rate = data.get('hourly_rate', payroll.hourly_rate)
    payroll.deductions = data.get('deductions', payroll.deductions)
    payroll.payment_status = data.get('payment_status', payroll.payment_status)
    payroll.notes = data.get('notes', payroll.notes)
    
    if 'payment_date' in data:
        payroll.payment_date = datetime.fromisoformat(data['payment_date']).date() if data['payment_date'] else None
    
    payroll.calculate_pay()
    db.session.commit()
    
    return jsonify(payroll.to_dict()), 200

@bp.route('/<int:payroll_id>', methods=['DELETE'])
@jwt_required()
def delete_payroll(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    db.session.delete(payroll)
    db.session.commit()
    return jsonify({'message': 'Payroll deleted'}), 200

