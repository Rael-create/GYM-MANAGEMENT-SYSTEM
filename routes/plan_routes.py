from flask import Blueprint, request, jsonify
from models import MembershipPlan
from config import db

plan_bp = Blueprint('plan_bp', __name__)

#Create a plan
@plan_bp.route('/plans', methods=['POST'])
def create_plan():
    data =request.get_json()

    new_plan = MembershipPlan(
        plan_name=data['plan_name'],
        duration_months=data['duration_months'],
        price=data['price'],
        description=data['description']


    )
    db.session.add(new_plan)
    db.session.commit()
    return jsonify(new_plan.to_dict()), 201

#Get all plans
@plan_bp.route('/plans', methods=['GET'])
def get_plans():
    plans = MembershipPlan.query.all()
    return jsonify([plan.to_dict() for plan in plans])

# Get a single plan
@plan_bp.route('/plans/<int:plan_id>', methods=['GET'])
def get_plan(plan_id):
    plan = MembershipPlan.query.get_or_404(plan_id)
    return jsonify(plan.to_dict()), 200


