from flask import Blueprint, request, jsonify
from config import db
from models import GymClass
from auth_decorator import require_roles, require_permissions

class_bp = Blueprint('class_bp', __name__)

#ceate a new gymclass
@class_bp.route('/classes', methods=['POST'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["create_class"])
def create_class():
    data = request.get_json()
    new_class = GymClass(
        class_name=data['class_name'],
        trainer_id=data['trainer_id'],
        class_date=data['class_date'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        capacity=data['capacity']
    )
    db.session.add(new_class)
    db.session.commit()
    return jsonify(new_class.to_dict()), 201

#get all classes
@class_bp.route('/classes', methods=['GET'])
@require_roles(["Admin", "Trainer", "Member"])
@require_permissions(["view_classes"])
def get_classes():
    classes = GymClass.query.all()
    return jsonify([gym_class.to_dict() for gym_class in classes])

#get a single class
@class_bp.route('/classes/<int:class_id>', methods=['GET'])
@require_roles(["Admin", "Trainer", "Member"])
@require_permissions(["view_class"])
def get_class(class_id):
    gym_class = GymClass.query.get_or_404(class_id)
    return jsonify(gym_class.to_dict())

#delete a class
@class_bp.route('/classes/<int:class_id>', methods=['GET'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["delete_class"])
def delete_class(class_id):
    gym_class = GymClass.query.get_or_404(class_id)

    db.session.delete(gym_class)
    db.session.commit()
    return jsonify({"message":"Class Deleted Succesfully!"}), 204



    
