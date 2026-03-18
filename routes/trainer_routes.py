from flask import Blueprint, request, jsonify
from config import db
from models import Trainer
from datetime import date

trainer_bp = Blueprint('trainer_bp', __name__)

#Create a new trainer
@trainer_bp.route('/trainers', methods=['POST'])
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
def get_trainers():
    trainers = Trainer.query.all()
    return jsonify([trainer.to_dict() for trainer in trainers]), 200

#Get a single Trainer
@trainer_bp.route('/trainers/<int:trainer_id>', methods=['GET'])
def get_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    return jsonify(trainer.to_dict()), 200



