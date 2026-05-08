from flask import Blueprint, request, jsonify 
from config import db
from models import ClassBooking
from auth_decorator import require_roles, require_permissions

booking_bp = Blueprint('booking_bp', __name__)

#create a new booking
@booking_bp.route('/bookings', methods=['POST'])
@require_roles(["Admin", "Trainer", "Member"])
@require_permissions(["create_booking"])
def create_booking():
    data = request.get_json()
    new_booking = ClassBooking(
        member_id=data['member_id'],
        class_id=data['class_id'],
        booking_date=data['booking_date']
    
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify(new_booking.to_dict()), 201

#Get all bookings
@booking_bp.route('/bookings', methods=['GET'])
@require_roles(["Admin", "Trainer", "Member"])
@require_permissions(["view_bookings"])
def get_bookings():
    bookings = ClassBooking.query.all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

#Get a single booking
@booking_bp.route('/bookings/<int:booking_id>', methods=['GET'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["view_booking"])
def get_booking(booking_id):
    booking = ClassBooking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict()), 200

#Update a booking
@booking_bp.route('/bookings/<int:booking_id>', methods=['PUT']) 
@require_roles(["Admin", "Trainer"])
@require_permissions(["update_booking"])  
def update_booking(booking_id):
    booking = ClassBooking.query.get_or_404(booking_id)
    data = request.get_json()
    booking.member_id = data.get('member_id', booking.member_id)
    booking.class_id = data.get('class_id', booking.class_id)
    booking.booking_date = data.get('booking_date', booking.booking_date)
    db.session.commit()
    return jsonify(booking.to_dict()), 200

#Delete a booking   
@booking_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
@require_roles(["Admin", "Trainer"])
@require_permissions(["delete_booking"])
def delete_booking(booking_id):
    booking = ClassBooking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message":"Booking deleted successfully"}), 204