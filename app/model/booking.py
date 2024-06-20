from database.database import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class Booking(db.Model):
    customer_id = db.Column(db.BigInteger(),primary_key=True)
    booking_number = db.Column(db.String(50),unique=True)
    event_details = db.Column(db.Text,nullable=False)
    date_booking = db.Column(db.String(60) , nullable=False)
    date_event = db.Column(db.String(60), nullable=False)
    vendor_id = db.Column(db.BigInteger(),primary_key=True)
    confirmation_vendor = db.Column(db.Boolean(),nullable=False)
    confirmation_details= db.Column(db.Text,nullable=False)
    data_cancelation = db.Column(db.Text,nullable=False)


    def __init__(self, customer_id, booking_number, event_details, date_booking, date_event, vendor_id, confirmation_vendor, confirmation_details, data_cancelation):
        self.customer_id = customer_id
        self.booking_number = booking_number
        self.event_details = event_details
        self.date_booking = date_booking
        self.date_event = date_event
        self.vendor_id = vendor_id
        self.confirmation_vendor = confirmation_vendor
        self.confirmation_details = confirmation_details
        self.data_cancelation = data_cancelation

    
    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "booking_number": self.booking_number,
            "event_details": self.event_details,
            "date_booking": self.date_booking,
            "date_event": self.date_event,
            "vendor_id": self.vendor_id,
            "confirmation_vendor": self.confirmation_vendor,
            "confirmation_details": self.confirmation_details,
            "data_cancelation": self.data_cancelation
        }
    
