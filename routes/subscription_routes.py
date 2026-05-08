from flask import Blueprint, request, jsonify
from config import db
from models import MemberSubscription
from auth_decorator import require_roles, require_permissions


subscription_bp = Blueprint('subcription_bp', __name__)

#create subscription
@subscription_bp.route('/subscriptions', methods=['POST'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["create_subscription"])
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
@require_roles(["Admin", "Trainer"])
@require_permissions(["view_subscriptions"])
def get_subscriptions():
    subscriptions = MemberSubscription.query.all()
    return jsonify([subscription.to_dict() for subscription in subscriptions])

#Get a single subscription
@subscription_bp.route('/subscriptions/<int:subscription_id>', methods=['GET'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["view_subscription"])
def get_subscription(subscription_id):
    subscription = MemberSubscription.query.get_or_404(subscription_id)
    return jsonify(subscription.to_dict()), 200

#Update a subscription
@subscription_bp.route('/subscriptions/<int:subscription_id>', methods=['PUT']) 
@require_roles(["Admin", "Trainer"])
@require_permissions(["update_subscription"])
def update_subscription(subscription_id):
    subscription = MemberSubscription.query.get_or_404(subscription_id)
    data = request.get_json()
    subscription.member_id = data.get('member_id', subscription.member_id)
    subscription.plan_id = data.get('plan_id', subscription.plan_id)
    subscription.start_date = data.get('start_date', subscription.start_date)
    subscription.end_date = data.get('end_date', subscription.end_date)
    subscription.status = data.get('status', subscription.status)
    db.session.commit()
    return jsonify(subscription.to_dict()), 200

#Delete a subscription
@subscription_bp.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["delete_subscription"])
def delete_subscripton(subscription_id):
    subscription = MemberSubscription.query.get_or_404(subscription_id)
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({"message":"Subscription deleted successfully"}), 204

    

