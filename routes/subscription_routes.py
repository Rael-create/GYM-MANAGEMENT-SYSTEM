from flask import Blueprint, request, jsonify
from config import db
from models import MemberSubscription

subscription_bp = Blueprint('subcription_bp', __name__)

#create subscription
@subscription_bp.route('/subscriptions', methods=['POST'])
def create_subscription():
    data =request.get_json()

    new_subscription = MemberSubscription(
        member_id=data['member_id'],
        plan_id=data['plan_id'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        status=data['status']
    )
    db.session.add(new_subscription)
    db.session.commit()
    return jsonify(new_subscription.to_dict()), 201


#Get all subscriptions
@subscription_bp.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    subscriptions = MemberSubscription.query.all()
    return jsonify([subscription.to_dict() for subscription in subscriptions])

#Get a single subscription
@subscription_bp.route('/subscriptions/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    subscription = MemberSubscription.query.get_or_404(subscription_id)
    return jsonify(subscription.to_dict()), 200