from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app import db
from app.models import Invoice, InvoiceLineItem, Client, Site

bp = Blueprint('invoices', __name__, url_prefix='/api/invoices')


def _date(value, field):
    if not value:
        raise ValueError(f'{field} is required')
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:
        raise ValueError(f'Invalid date for {field}') from exc


def _load_items(items):
    line_items = []
    for item in items or []:
        if not item.get('description') or item.get('quantity') is None or item.get('unit_price') is None:
            raise ValueError('Line items require description, quantity and unit_price')
        line_items.append(
            InvoiceLineItem(
                site_id=item.get('site_id'),
                description=item['description'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                line_total=item.get('line_total') or (float(item['quantity']) * float(item['unit_price']))
            )
        )
    return line_items


@bp.route('', methods=['GET'])
@jwt_required()
def list_invoices():
    client_id = request.args.get('client_id')
    status = request.args.get('status')

    query = Invoice.query
    if client_id:
        query = query.filter_by(client_id=client_id)
    if status:
        query = query.filter_by(invoice_status=status)

    invoices = query.order_by(Invoice.invoice_date.desc()).all()
    return jsonify([inv.to_dict() for inv in invoices]), 200


@bp.route('/<int:invoice_id>', methods=['GET'])
@jwt_required()
def get_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = invoice.to_dict()
    data['line_items'] = [item.to_dict() for item in invoice.line_items]
    return jsonify(data), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_invoice():
    data = request.get_json() or {}

    required = ['client_id', 'invoice_number', 'invoice_date', 'due_date', 'line_items']
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    Client.query.get_or_404(data['client_id'])
    for item in data['line_items']:
        if item.get('site_id'):
            Site.query.get_or_404(item['site_id'])

    try:
        invoice_date = _date(data['invoice_date'], 'invoice_date')
        due_date = _date(data['due_date'], 'due_date')
        billing_start = _date(data['billing_period_start'], 'billing_period_start') if data.get('billing_period_start') else None
        billing_end = _date(data['billing_period_end'], 'billing_period_end') if data.get('billing_period_end') else None
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    invoice = Invoice(
        client_id=data['client_id'],
        invoice_number=data['invoice_number'],
        invoice_date=invoice_date,
        due_date=due_date,
        billing_period_start=billing_start,
        billing_period_end=billing_end,
        tax_rate=data.get('tax_rate', 0),
        discount_percentage=data.get('discount_percentage', 0),
        payment_terms=data.get('payment_terms'),
        notes=data.get('notes'),
        invoice_status=data.get('invoice_status', 'draft')
    )

    line_items = _load_items(data.get('line_items'))
    invoice.line_items = line_items
    invoice.calculate_totals()

    db.session.add(invoice)
    db.session.commit()

    return jsonify(invoice.to_dict()), 201


@bp.route('/<int:invoice_id>', methods=['PUT'])
@jwt_required()
def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json() or {}

    if 'invoice_date' in data:
        try:
            invoice.invoice_date = _date(data['invoice_date'], 'invoice_date')
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
    if 'due_date' in data:
        try:
            invoice.due_date = _date(data['due_date'], 'due_date')
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
    if 'billing_period_start' in data:
        invoice.billing_period_start = _date(data['billing_period_start'], 'billing_period_start') if data['billing_period_start'] else None
    if 'billing_period_end' in data:
        invoice.billing_period_end = _date(data['billing_period_end'], 'billing_period_end') if data['billing_period_end'] else None

    simple_fields = [
        'client_id', 'tax_rate', 'discount_percentage', 'payment_terms',
        'notes', 'invoice_status', 'amount_paid', 'balance_due', 'invoice_pdf_url'
    ]
    for field in simple_fields:
        if field in data:
            setattr(invoice, field, data[field])

    if 'line_items' in data:
        invoice.line_items.delete()  # type: ignore
        new_items = _load_items(data['line_items'])
        invoice.line_items = new_items

    invoice.calculate_totals()
    db.session.commit()

    return jsonify(invoice.to_dict()), 200


@bp.route('/<int:invoice_id>/mark-sent', methods=['POST'])
@jwt_required()
def mark_invoice_sent(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.mark_as_sent()
    db.session.commit()
    return jsonify(invoice.to_dict()), 200


@bp.route('/<int:invoice_id>/record-payment', methods=['POST'])
@jwt_required()
def record_payment(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json() or {}
    amount = data.get('amount')
    if amount is None:
        return jsonify({'error': 'Payment amount required'}), 400
    invoice.record_payment(amount)
    db.session.commit()
    return jsonify(invoice.to_dict()), 200


@bp.route('/<int:invoice_id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice deleted'}), 200

