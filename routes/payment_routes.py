from flask import Blueprint, request, jsonify
from config import db
from models import Payment
from auth_decorator import require_roles, require_permissions


payment_bp = Blueprint('payment_bp', __name__)

#Create a payment
@payment_bp.route('/payments', methods=['POST'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["create_payment"])
def create_payment():
    data = request.get_json()
    new_payment = Payment(
        member_id=data['member_id'],
        subscription_id=data['subscription_id'],
        amount=data['amount'],
        payment_method=data['payment_method'],
        payment_date=data['payment_date']
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify(new_payment.to_dict())

#Get all payments
@payment_bp.route('/payments', methods=['GET'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["view_payments"])
def get_payments():
    payments = Payment.query.all()
    return jsonify([payment.to_dict() for payment in payments]), 200

#Get a single payment
@payment_bp.route('/payments/<int:payment_id>', methods=['GET'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["view_payment"])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.to_dict())

