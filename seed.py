from app import app
from config import db
from models import User, Role, Permission
from werkzeug.security import generate_password_hash


# =========================
# OPTIONAL: CLEAR TABLES (DEV ONLY)
# =========================
def clear_tables():
    print("⚠️ Clearing tables...")

    db.session.execute('SET FOREIGN_KEY_CHECKS = 0;')

    db.session.execute('TRUNCATE TABLE user_roles;')
    db.session.execute('TRUNCATE TABLE role_permissions;')
    db.session.execute('TRUNCATE TABLE users;')
    db.session.execute('TRUNCATE TABLE roles;')
    db.session.execute('TRUNCATE TABLE permissions;')

    db.session.execute('SET FOREIGN_KEY_CHECKS = 1;')

    db.session.commit()


# =========================
# SEED PERMISSIONS
# =========================
def seed_permissions():
    permissions_list = [
        "create_member",
        "view_member",
        "update_member",
        "delete_member",
        "manage_attendance",
        "manage_payments",
        "manage_classes",
        "manage_trainers",
        "view_own_data"
    ]

    created_permissions = []

    for perm_name in permissions_list:
        perm = Permission.query.filter_by(name=perm_name).first()

        if not perm:
            perm = Permission(name=perm_name)
            db.session.add(perm)
            print(f"✅ Created permission: {perm_name}")

        created_permissions.append(perm)

    db.session.commit()
    return created_permissions


# =========================
# SEED ROLES
# =========================
def seed_roles(permissions):
    role_map = {
        "Admin": permissions,  # all permissions

        "Trainer": [
            p for p in permissions if p.name in [
                "manage_classes",
                "manage_attendance",
                "create_member",
                "view_member",
                "manage_payments"
            ]
        ],

        "Member": [
            p for p in permissions if p.name == "view_own_data"
        ]
    }

    created_roles = {}

    for role_name, perms in role_map.items():
        role = Role.query.filter_by(name=role_name).first()

        if not role:
            role = Role(name=role_name)
            db.session.add(role)
            db.session.flush()  # ensures role.id exists
            print(f"✅ Created role: {role_name}")

        # ✅ Prevent duplicate role-permission entries
        for perm in perms:
            if perm not in role.permissions:
                role.permissions.append(perm)

        created_roles[role_name] = role

    db.session.commit()
    return created_roles


# =========================
# SEED ADMIN USER
# =========================
def seed_admin_user(roles):
    admin_email = "admin@gym.com"

    admin = User.query.filter_by(email=admin_email).first()

    if not admin:
        admin = User(
            username="admin",
            email=admin_email,
            password_hash=generate_password_hash("admin123")
        )

        db.session.add(admin)
        db.session.flush()
        print("✅ Admin user created")

    # ✅ Prevent duplicate role assignment
    admin_role = roles["Admin"]
    if admin_role not in admin.roles:
        admin.roles.append(admin_role)

    db.session.commit()


# =========================
# RUN SEED
# =========================
def run_seed():
    with app.app_context():
        print("🌱 Starting database seeding...")

        # 👉 OPTION A: Uncomment ONLY if you want fresh DB each time
        # clear_tables()

        permissions = seed_permissions()
        roles = seed_roles(permissions)
        seed_admin_user(roles)

        print("✅ Seeding complete!")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    run_seed()