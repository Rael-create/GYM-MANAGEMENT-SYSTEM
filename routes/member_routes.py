from flask import Blueprint, request, jsonify 
from config import db
from models import Member
from datetime import date

members_bp = Blueprint('members_bp', __name__)

# create a new member
@members_bp.route('/members', methods=['POST'])
def create_member():
    data = request.get_json()

    # Validate required fields
    required_fields = ['full_name', 'phone_number', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    #Auto-generate join_date if not provided
    join_date = data.get('join_date', date.today().isoformat())

    new_member = Member(
        full_name=data['full_name'],
        phone_number=data['phone_number'],
        email=data['email'],
        gender=data['gender'],
        address=data['address'],
        emergency_contact=data['emergency_contact'],
        join_date=data['join_date']
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify(new_member.to_dict()), 201

#Get all members
@members_bp.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([member.to_dict() for member in members]), 200

#Get a Single Member
@members_bp.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.query.get_or_404(member_id)
    return jsonify(member.to_dict()), 200

#Update a Member
@members_bp.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    member = Member.query.get_or_404(member_id)
    data = request.get_json()

    member.full_name = data.get('full_name', member.full_name)
    member.phone_number = data.get('phone_number', member.phone_number)
    member.email = data.get('email', member.email)
    member.gender = data.get('gender', member.gender)
    member.address = data.get('address', member.address)
    member.emergency_contact = data.get('emergency_contact', member.emergency_contact)
    db.session.commit()
    return jsonify(member.to_dict()), 200

#Delete a Member
@members_bp.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message":"Member deleted successfully"}), 204