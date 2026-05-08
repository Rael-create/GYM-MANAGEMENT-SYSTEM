from flask import Blueprint, request, jsonify
from models import User
from models import Role
from app import db
from werkzeug.security import generate_password_hash
from auth_decorator import require_role

users_bp = Blueprint("users", __name__)

# -------------------------------
# Get all users
# -------------------------------
@users_bp.route("/users", methods=["GET"])
@require_role("Admin")
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# -------------------------------
# Get single user
# -------------------------------
@users_bp.route("/users/<int:user_id>", methods=["GET"])
@require_role("Admin")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

# -------------------------------
# Create a new user
# -------------------------------
@users_bp.route("/users", methods=["POST"])
@require_role("Admin")
def create_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "username, email, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": f"User '{username}' created", "user_id": user.user_id}), 201

# -------------------------------
# Update user
# -------------------------------
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
@require_role("Admin")
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password_hash = generate_password_hash(password)

    db.session.commit()
    return jsonify({"message": f"User '{user.username}' updated", "user": user.to_dict()})

# -------------------------------
# Delete user
# -------------------------------
@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
@require_role("Admin")
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User '{user.username}' deleted"})