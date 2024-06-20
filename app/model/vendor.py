from database.database import db
from sqlalchemy.exc import IntegrityError

class VENDOR(db.Model):
    vendor_id=db.Column(db.BigInteger(),primary_key=True)
    organization_name=db.Column(db.String(50))
    person_name=db.Column(db.String(50))
    full_address=db.Column(db.String(50))
    email_id=db.Column(db.String(50),unique=True)
    password=db.Column(db.Unicode())
    phone_no=db.Column(db.BigInteger())
    event=db.Column(db.String(50))
    gst_no=db.Column(db.String(50))
    
    # event= db.relationship("EVENT",backref="vendor",lazy=True,)

    def __init__(self,vendor_id,organization_name,person_name,full_address,email_id,password,phone_no,event,gst_no):
        self.vendor_id=vendor_id,
        self.organization_name=organization_name,
        self.person_name=person_name,
        self.full_address=full_address,
        self.email_id=email_id,
        self.password=password,
        self.phone_no=phone_no,
        self.event=event,
        self.gst_no=gst_no

    @staticmethod
    def create_vendor(payload):
        vendor=VENDOR(
            vendor_id=payload["vendor_id"],
            organization_name=payload["organization_name"],
            person_name=payload["person_name"],
            full_address=payload["full_address"],
            email_id=payload["email_id"],
            password=payload["password"],
            phone_no=payload["phone_no"],
            event=payload["event"],
            gst_no=payload["gst_no"],
        )

        try:
            db.session.add(vendor)
            db.session.commit()
            return True
        except IntegrityError:
            return False

