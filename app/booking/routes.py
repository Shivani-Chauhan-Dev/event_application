from app.model.booking import Booking
from database.database import db
from flask import request,jsonify
from . import bp



@bp.route("/booking" ,methods= ["POST"])
def create_booking():
    try:
        data = request.json
        entry =Booking(**data)
        db.session.add(entry)
        db.session.commit()

        return jsonify(entry.to_dict()), 201
    
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500

@bp.route("/booking/event",methods=["GET"])
def get_booking_event():
    bookings=Booking.query.all()
    result= []
    for booking_event in bookings:
        booking_data={
            "customer_id":booking_event.customer_id,
            "booking_number":booking_event.booking_number,
            "event_details":booking_event.event_details,
            "date_booking":booking_event.date_booking,
            "date_event":booking_event.date_event,
            "vendor_id":booking_event.vendor_id,
            "confirmation_vendor":booking_event.confirmation_vendor,
            "confirmation_details":booking_event.confirmation_details,
            "data_cancelation":booking_event.data_cancelation
        }
        result.append(booking_data)
    return jsonify({"booking_events":result})
        

