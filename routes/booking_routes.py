from flask import Blueprint, request, jsonify 
from config import db
from models import ClassBooking

booking_bp = Blueprint('booking_bp', __name__)

#create a new booking
@booking_bp.route('/bookings', methods=['POST'])
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
def get_bookings():
    bookings = ClassBooking.query.all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

#Get a single booking
@booking_bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = ClassBooking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict()), 200