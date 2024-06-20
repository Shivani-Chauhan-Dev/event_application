from flask import Flask,request,jsonify,session
from database.database import db
from app.model.customer import User
from app.model.vendor import VENDOR
import jwt
import bcrypt
import datetime
from . import bp


app = Flask(__name__)
app.config['secret_key'] = "this is secret"


def token_required(f):
    def decorated(*args, **kwargs):
        # token = request.args.get('token')
        token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)
    return decorated

@bp.route("/logging",methods=["POST"])
def logging():
    data=request.get_json()
    if data:
        email_id=data.get("email_id")
        password=data.get("password")
        # print(email_id,password)
        if email_id and password:
            # Retrieve user from the database by email
            user=User.query.filter_by(email_id=email_id).first()
            if user:
                # Check if the provided password matches the hashed password stored in the database
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                user.password = hashed_password
                if bcrypt.checkpw(password.encode("utf-8"), user.password):
                    token = jwt.encode({'user': user.email_id, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=120)}, app.config['secret_key'])
                    # return jsonify(token)
                    return jsonify({"message": "Login successful"}), 200
                else:
                    return jsonify({"message": "Invalid email or password"}), 401
            else:
                return jsonify({"message": "Missing email or password"}), 400
        else:
            return jsonify({"message": "No data provided"}), 400
        

@bp.route("/update_password",methods=["POST"])
@token_required
def update_password():
    data= request.get_json()
    if data:
        customer_id=data.get("customer_id")
        email_id=data.get("email_id")
        old_password=data.get("old_password")
        new_password=data.get("new_password")
        if customer_id and email_id and old_password and new_password:
            user=User.query.filter_by(email_id=email_id).first()
            if user:
                hashed_password = bcrypt.hashpw(old_password.encode("utf-8"), bcrypt.gensalt())
                user.password = hashed_password
                if bcrypt.checkpw(old_password.encode("utf-8"),user.password):
                    hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    user.password = hashed_new_password
                    db.session.commit()

                    return jsonify({"message": "Password updated successfully"}), 200
                else:
                    return jsonify({"message": "Invalid old password"}), 401
            else:
                return jsonify({"message": "User not found"}), 404
        else:
            return jsonify({"message": "Missing data"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400


@bp.route("/logging",methods=["POST"])
def vender_logging():
    data=request.get_json()
    if data:
        email_id=data.get("email_id")
        password=data.get("password")
        if email_id and password:
            vendor=VENDOR.query.filter_by(email_id=email_id).first()
            if vendor:
                hashed_password = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
                vendor.password = hashed_password
                if bcrypt.checkpw(password.encode("utf-8"),vendor.password):
        
                    return jsonify({"message":"Login successful"}), 200
                else:
                    return jsonify({"message":"Invalid email or password"}), 401
            else:
                return jsonify({"message":"Missing email or password"}), 400
        else:
            return jsonify({"message":"No data provided"}), 400
        
@bp.route("/vendor/update_password",methods=["POST"])
def vendor_update_password():
    data=request.get_json()
    if data:
        vendor_id=data.get("vendor_id")
        email_id=data.get("email_id")
        old_password=data.get("old_password")
        new_password=data.get("new_password")
        print(vendor_id,email_id,old_password,new_password)
        if vendor_id and email_id and old_password and new_password:
            vendor=VENDOR.query.filter_by(email_id=email_id).first()
            if vendor:
                hashed_password = bcrypt.hashpw(old_password.encode("utf-8"), bcrypt.gensalt())
                vendor.password = hashed_password
                if bcrypt.checkpw(old_password.encode("utf-8"),vendor.password):
                    hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    vendor.password = hashed_new_password
                    db.session.commit()

                    return jsonify({"message": "Password updated successfully"}), 200
                else:
                    return({"message": "Invalid old password"}), 401
            else:
                return jsonify({"message": "Vendor not found"}), 404
        else:
            return jsonify({"message": "Missing data"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400


@bp.route("/logout",methods=["POST"])
def logout():
    session.clear()
    return jsonify("you are out of the application")