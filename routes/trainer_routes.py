from flask import Blueprint, request, jsonify
from config import db
from models import Trainer
from datetime import date
from auth_decorator import require_roles, require_permissions

trainer_bp = Blueprint('trainer_bp', __name__)

#Create a new trainer
@trainer_bp.route('/trainers', methods=['POST'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["create_trainer"])
def create_trainer():
    data = request.get_json()

    new_trainer = Trainer(
        full_name=data['full_name'],
        phone_number=data['phone_number'],
        email=data['email'],
        specialization=data['specialization'],
        hire_date=data['hire_date']
    )
    db.session.add(new_trainer) 
    db.session.commit()
    return jsonify(new_trainer.to_dict()), 201

#Get all trainers
@trainer_bp.route('/trainers', methods=['GET'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["view_trainers"])
def get_trainers():
    trainers = Trainer.query.all()
    return jsonify([trainer.to_dict() for trainer in trainers]), 200

#Get a single Trainer
@trainer_bp.route('/trainers/<int:trainer_id>', methods=['GET'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["view_trainer"])
def get_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    return jsonify(trainer.to_dict()), 200

#update a trainer
@trainer_bp.route('/trainers/<int:trainer_id>', methods=['PUT'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["update_trainer"])
def update_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    data = request.get_json()
    trainer.full_name = data.get('full_name', trainer.full_name)
    trainer.phone_number = data.get('phone_number', trainer.phone_number)
    trainer.email = data.get('email', trainer.email)
    trainer.specialization = data.get('specialization', trainer.specialization)
    trainer.hire_date = data.get('hire_date', trainer.hire_date)
    db.session.commit()
    return jsonify(trainer.to_dict()), 200

#delete a trainer
@trainer_bp.route('/trainers/<int:trainer_id>', methods=['DELETE'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["delete_trainer"])
def delete_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    db.session.delete(trainer)
    db.session.commit()
    return jsonify({"message":"Trainer deleted successfully"}), 204




  



