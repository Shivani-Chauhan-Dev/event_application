from flask import Flask
from flask import Flask, Blueprint
from database.database import db

app =  Flask(__name__)
app.secret_key = "your_secret_key"

def create_app():
    app.config["SQLALCHEMY_DATABASE_URI"]= "postgresql://postgres:shivanichauhan@localhost:5000/app"

    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()


from app.customer import bp as customer_bp
app.register_blueprint(customer_bp,url_prefix="/customer")

from app.vendor import bp as vendor_bp
app.register_blueprint(vendor_bp,url_prefix="/vendor")

from app.event import bp as event_bp
app.register_blueprint(event_bp,url_prefix="/event")

from app.booking import bp as booking_bp
app.register_blueprint(booking_bp,url_prefix="/booking")


from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)


if __name__ == '__main__':
    create_app()
    app.run(debug=True,port =5001)