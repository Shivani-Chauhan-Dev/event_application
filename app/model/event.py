from database.database import db
from sqlalchemy.exc import IntegrityError


class EVENT(db.Model):
    event_code= db.Column(db.String(100))
    event= db.Column(db.String(100))
    vendor_id=db.Column(db.BigInteger(),primary_key=True)
    customer_id=db.Column(db.BigInteger(),primary_key=True)
    booking_status= db.Column(db.Boolean,nullable=False)

    
    # user = db.relationship("User", back_populates="event")
    # customer_id= db.Column(db.BigInteger(), db.ForeignKey("user.customer_id"), primary_key=True)

    
    
    def to_dict(self):
        return{
            "event_code":self.event_code,
            "event":self.event,
            "customer_id":self.customer_id,
            "vendor_id":self.vendor_id,
            "booking_ststus":self.booking_status
        }
    


    # vendor_id= db.Column(db.BigInteger(),db.ForeignKey("vendor.vendor_id"),nullable=False, default=False)