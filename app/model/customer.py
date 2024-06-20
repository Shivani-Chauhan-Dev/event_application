from database.database import db
from sqlalchemy.exc import IntegrityError





class User(db.Model):
    customer_id= db.Column(db.BigInteger(), primary_key=True)
    name=db.Column(db.String(100))
    email_id=db.Column(db.String(100),unique=True)
    phone_no=db.Column(db.BigInteger())
    full_address=db.Column(db.String(100))
    event=db.Column(db.String(60))
    password=db.Column(db.Unicode())
    created_at=db.Column(db.String(50))
    lastupdated=db.Column(db.String(50))

    # event= db.relationship("EVENT",backref="user",lazy=True)
    def __init__(self,customer_id,name,email_id,phone_no,full_address,event,password,created_at,lastupdated):
        self.customer_id= customer_id
        self.name= name
        self.email_id= email_id
        self.phone_no= phone_no
        self.full_address= full_address
        self.event= event
        self.password= password
        self.created_at= created_at 
        self.lastupdated= lastupdated 

    @staticmethod
    def create_user(payload):
        user=User(
            customer_id= payload["customer_id"],
            name= payload["name"],
            email_id= payload["email_id"],
            phone_no= payload["phone_no"],
            full_address= payload["full_address"],
            event= payload["event"],
            password= payload["password"],
            created_at= payload["created_at"],
            lastupdated= payload["lastupdated"]
            
        )  

        try:
            db.session.add(user)
            db.session.commit() 
            return True
        except IntegrityError:
            return False
