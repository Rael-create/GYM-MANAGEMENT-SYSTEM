
from datetime import datetime


from config import db

class Member(db.Model):
    __tablename__='members'
    member_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    gender=db.Column(db.Enum('Male', 'Female'), nullable=False)
    address=db.Column(db.String(200), nullable=False)
    emergency_contact=db.Column(db.String(100), nullable=False)
    join_date=db.Column(db.Date, nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    subscriptions = db.relationship('MemberSubscription', backref='member', cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='member', cascade="all, delete-orphan")
    class_bookings = db.relationship('ClassBooking', backref='member', cascade="all, delete-orphan")
    attendance_records = db.relationship('Attendance', backref='member', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "gender": self.gender,
            "address": self.address,
            "emergency_contact": self.emergency_contact,
            "join_date": str(self.join_date),
            "created_at": self.created_at.isoformat()
        }


class Trainer(db.Model):
    __tablename__='trainers'
    trainer_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.Date, nullable=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)


    # Relationships
    classes = db.relationship('GymClass', backref='trainer', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "trainer_id": self.trainer_id,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "specialization": self.specialization,
            "hire_date": str(self.hire_date),
            "created_at": self.created_at.isoformat()
        }


class MembershipPlan(db.Model):
    __tablename__='membership_plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(100), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    subscriptions = db.relationship('MemberSubscription', backref='plan', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "plan_id": self.plan_id,
            "plan_name": self.plan_name,
            "duration_months": self.duration_months,
            "price": self.price,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }


class MemberSubscription(db.Model):
    __tablename__='member_subscriptions'
    subscription_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plans.plan_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('active', 'expired', 'cancelled'), default='active', nullable=False)

    def to_dict(self):
        return {
            "subscription_id": self.subscription_id,
            "member_id": self.member_id,
            "plan_id": self.plan_id,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "status": self.status
        }

class Payment(db.Model):
    __tablename__='payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('member_subscriptions.subscription_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Enum('cash', 'mpesa', 'card'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "member_id": self.member_id,
            "subscription_id": self.subscription_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "payment_date": str(self.payment_date)
        }


class GymClass(db.Model):
    __tablename__='classes'
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'), nullable=False)
    class_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    # Relationships
    bookings = db.relationship('ClassBooking', backref='gym_class', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "trainer_id": self.trainer_id,
            "class_date": str(self.class_date),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "capacity": self.capacity
        }


class ClassBooking(db.Model):
    __tablename__='class_bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "member_id": self.member_id,
            "class_id": self.class_id,
            "booking_date": str(self.booking_date)
        }


class Attendance(db.Model):
    __tablename__='attendance'
    attendance_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    check_out_time = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "attendance_id": self.attendance_id,
            "member_id": self.member_id,
            "check_in_time": self.check_in_time.isoformat(),
            "check_out_time": self.check_out_time.isoformat() if self.check_out_time else None
        }

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    roles = db.relationship('Role', secondary='user_roles', back_populates='users')

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "roles": [role.name for role in self.roles],
            "permissions": [perm.name for perm in self.permissions]
        }
    
class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', secondary='user_roles', back_populates='roles')
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles')

class Permission(db.Model):
    __tablename__ = 'permissions'

    permission_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions')
    

class UserRole(db.Model):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), primary_key=True)

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'

    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.permission_id'), primary_key=True)


