from flask import Blueprint, request, jsonify
from models import Attendance
from config import db
from datetime import datetime

attendance_bp = Blueprint('attendance_bp', __name__)


#  GET all attendance records
@attendance_bp.route('/attendance', methods=['GET'])
def get_attendance():
    records = Attendance.query.all()
    return jsonify([r.to_dict() for r in records]), 200


#  POST attendance manually (optional use)
@attendance_bp.route('/attendance', methods=['POST'])
def create_attendance():
    data = request.get_json()

    attendance = Attendance(
        member_id=data['member_id'],
        check_in_time=datetime.fromisoformat(data['check_in_time']),
        check_out_time=datetime.fromisoformat(data['check_out_time']) if data.get('check_out_time') else None
    )

    db.session.add(attendance)
    db.session.commit()

    return jsonify(attendance.to_dict()), 201


#  Check in (auto time)
@attendance_bp.route('/attendance/checkin', methods=['POST'])
def check_in():
    data = request.get_json()

    attendance = Attendance(
        member_id=data['member_id'],
        check_in_time=datetime.utcnow()
    )

    db.session.add(attendance)
    db.session.commit()

    return jsonify(attendance.to_dict()), 201


#  Check out (auto time)
@attendance_bp.route('/attendance/checkout/<int:id>', methods=['PUT'])
def check_out(id):

    attendance = Attendance.query.get_or_404(id)

    attendance.check_out_time = datetime.utcnow()
    db.session.commit()

    return jsonify(attendance.to_dict()), 200