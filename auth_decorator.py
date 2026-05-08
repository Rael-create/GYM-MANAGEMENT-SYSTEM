from functools import wraps
from flask import request, jsonify
from models import User


# =========================
# GET CURRENT USER
# =========================
def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        # Expecting: Bearer <token>
        token = auth_header.split(" ")[1]

        # ⚠️ TEMP LOGIC: token = user_id (for now)
        user = User.query.get(int(token))
        return user

    except Exception:
        return None


# =========================
# COMBINED DECORATOR
# =========================
def require_roles_permissions(roles=None, permissions=None):
    """
    Restrict access based on roles and/or permissions.
    Permissions are derived from roles.
    """
    roles = roles or []
    permissions = permissions or []

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_current_user()

            if not user:
                return jsonify({"error": "Unauthorized"}), 401

            # =========================
            # ROLE CHECK
            # =========================
            user_roles = [role.name for role in user.roles]

            if roles and not any(role in user_roles for role in roles):
                return jsonify({"error": "Forbidden: insufficient role"}), 403

            # =========================
            # PERMISSION CHECK
            # =========================
            user_perms = set()

            for role in user.roles:
                for perm in role.permissions:
                    user_perms.add(perm.name)

            if permissions and not any(p in user_perms for p in permissions):
                return jsonify({"error": "Forbidden: insufficient permission"}), 403

            return f(*args, **kwargs)

        return wrapper

    return decorator


# =========================
# ROLE-ONLY DECORATOR
# =========================
def require_roles(*roles):
    return require_roles_permissions(roles=list(roles))


# =========================
# PERMISSION-ONLY DECORATOR
# =========================
def require_permissions(*permissions):
    return require_roles_permissions(permissions=list(permissions))