from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Payroll, Agent, Attendance

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
    data = request.get_json() or {}

    required_fields = ['agent_id', 'pay_period_start', 'pay_period_end']
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    agent = Agent.query.get_or_404(data['agent_id'])

    start_date = datetime.fromisoformat(data['pay_period_start']).date()
    end_date = datetime.fromisoformat(data['pay_period_end']).date()

    attendances = Attendance.query.filter(
        Attendance.agent_id == data['agent_id'],
        Attendance.attendance_date >= start_date,
        Attendance.attendance_date <= end_date
    ).all()

    total_hours = sum((att.total_hours or 0) for att in attendances)

    payroll = Payroll(
        agent_id=data['agent_id'],
        pay_period_start=start_date,
        pay_period_end=end_date,
        total_regular_hours=total_hours,
        hourly_rate=data.get('hourly_rate', agent.hourly_rate),
        total_overtime_hours=data.get('total_overtime_hours', 0),
        total_night_shift_hours=data.get('total_night_shift_hours', 0),
        total_holiday_hours=data.get('total_holiday_hours', 0),
        overtime_rate=data.get('overtime_rate'),
        night_shift_rate=data.get('night_shift_rate'),
        holiday_rate=data.get('holiday_rate'),
        bonus_amount=data.get('bonus_amount', 0),
        bonus_description=data.get('bonus_description'),
        allowances=data.get('allowances', 0),
        allowances_description=data.get('allowances_description'),
        deduction_tax=data.get('deduction_tax', 0),
        deduction_social_security=data.get('deduction_social_security', 0),
        deduction_insurance=data.get('deduction_insurance', 0),
        deduction_uniform=data.get('deduction_uniform', 0),
        deduction_loan=data.get('deduction_loan', 0),
        deduction_other=data.get('deduction_other', data.get('deductions', 0)),
        deduction_other_description=data.get('deduction_other_description'),
        payment_status=data.get('payment_status', 'draft'),
        notes=data.get('notes')
    )

    payroll.calculate_net_pay()

    db.session.add(payroll)
    db.session.commit()

    return jsonify(payroll.to_dict()), 201

@bp.route('/<int:payroll_id>', methods=['PUT'])
@jwt_required()
def update_payroll(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    data = request.get_json() or {}

    simple_fields = [
        'hourly_rate', 'overtime_rate', 'night_shift_rate', 'holiday_rate',
        'total_regular_hours', 'total_overtime_hours', 'total_night_shift_hours',
        'total_holiday_hours', 'bonus_amount', 'bonus_description', 'allowances',
        'allowances_description', 'deduction_tax', 'deduction_social_security',
        'deduction_insurance', 'deduction_uniform', 'deduction_loan',
        'deduction_other', 'deduction_other_description', 'payment_status',
        'payment_method', 'payment_reference', 'notes'
    ]

    for field in simple_fields:
        if field in data:
            setattr(payroll, field, data[field])

    if 'payment_date' in data:
        payroll.payment_date = datetime.fromisoformat(data['payment_date']).date() if data['payment_date'] else None

    if 'bonus_amount' in data or 'allowances' in data or 'deduction_other' in data:
        payroll.calculate_net_pay()
    else:
        payroll.calculate_gross_pay()

    db.session.commit()

    return jsonify(payroll.to_dict()), 200

@bp.route('/<int:payroll_id>', methods=['DELETE'])
@jwt_required()
def delete_payroll(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    db.session.delete(payroll)
    db.session.commit()
    return jsonify({'message': 'Payroll deleted'}), 200

