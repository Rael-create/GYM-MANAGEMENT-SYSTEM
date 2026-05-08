from flask import Blueprint, request, jsonify
from models import User
from models import Role
from models import Permission
from app import db
from auth_decorator import require_permission


roles_bp = Blueprint("roles", __name__)

# -------------------------------
# Get all roles with permissions
# -------------------------------
@roles_bp.route("/roles", methods=["GET"])
@require_permission("manage_roles")
def get_roles():
    roles = Role.query.all()
    return jsonify([
        {
            "role_id": r.role_id,
            "name": r.name,
            "permissions": [p.name for p in r.permissions]
        } for r in roles
    ])

# -------------------------------
# Create a new role
# -------------------------------
@roles_bp.route("/roles", methods=["POST"])
@require_permission("manage_roles")
def create_role():
    data = request.get_json()
    role_name = data.get("name")
    if not role_name:
        return jsonify({"error": "Role name is required"}), 400

    existing = Role.query.filter_by(name=role_name).first()
    if existing:
        return jsonify({"error": "Role already exists"}), 400

    role = Role(name=role_name)
    db.session.add(role)
    db.session.commit()

    return jsonify({
        "message": f"Role '{role_name}' created",
        "role_id": role.role_id
    }), 201

# -------------------------------
# Assign role to a user
# -------------------------------
@roles_bp.route("/users/<int:user_id>/roles", methods=["POST"])
@require_permission("manage_roles")
def assign_role(user_id):
    data = request.get_json()
    role_id = data.get("role_id")
    if not role_id:
        return jsonify({"error": "role_id is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    if role in user.roles:
        return jsonify({"error": "User already has this role"}), 400

    user.roles.append(role)
    db.session.commit()

    return jsonify({"message": f"Role '{role.name}' assigned to user '{user.username}'"})

# -------------------------------
# Assign permission to a role
# -------------------------------
@roles_bp.route("/roles/<int:role_id>/permissions", methods=["POST"])
@require_permission("manage_roles")
def assign_permission_to_role(role_id):
    data = request.get_json()
    permission_id = data.get("permission_id")
    if not permission_id:
        return jsonify({"error": "permission_id is required"}), 400

    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    permission = Permission.query.get(permission_id)
    if not permission:
        return jsonify({"error": "Permission not found"}), 404

    if permission in role.permissions:
        return jsonify({"error": "Role already has this permission"}), 400

    role.permissions.append(permission)
    db.session.commit()

    return jsonify({
        "message": f"Permission '{permission.name}' assigned to role '{role.name}'"
    })

# -------------------------------
# Remove permission from a role
# -------------------------------
@roles_bp.route("/roles/<int:role_id>/permissions/<int:permission_id>", methods=["DELETE"])
@require_permission("manage_roles")
def remove_permission_from_role(role_id, permission_id):
    role = Role.query.get(role_id)
    permission = Permission.query.get(permission_id)

    if not role or not permission:
        return jsonify({"error": "Role or permission not found"}), 404

    if permission not in role.permissions:
        return jsonify({"error": "Role does not have this permission"}), 400

    role.permissions.remove(permission)
    db.session.commit()

    return jsonify({
        "message": f"Permission '{permission.name}' removed from role '{role.name}'"
    })