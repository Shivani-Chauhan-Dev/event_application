from app.model.customer import User
from database.database import db
from flask import request,jsonify
import bcrypt
# from app.customer import Blueprint as bp
import datetime
from . import bp


@bp.route("/customer/registration",methods=["POST"])
def registration():
    current_date=str(datetime.datetime.now())
    data=request.get_json()
    if data:
        customer_id=data.get("customer_id")
        name=data.get("name")
        email_id=data.get("email_id")
        phone_no=data.get("phone_no")
        full_address=data.get("full_address")
        event=data.get("event")
        password=data.get("password")
        created_at=current_date
        lastupdated=current_date
        print(customer_id,name,email_id,phone_no,full_address,event,password,created_at,lastupdated)
        if customer_id and name and email_id and phone_no and full_address and event and password :
            existing_user= User.query.filter_by(email_id=email_id).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400
            else:
                hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt()
                )

                if User.create_user(
                    {
                        "customer_id":customer_id,
                        "name":name,
                        "email_id":email_id,
                        "phone_no":phone_no,
                        "full_address":full_address,
                        "event":event,
                        "password":hashed_password,
                        "created_at":created_at,
                        "lastupdated":lastupdated,
                    }
                ):

                    return jsonify({"message": "User created successfully"}), 201
                else:
                    return jsonify({"message": "Failed to create user"}), 500
        else:
            return jsonify({"message": "Missing fields"}), 400
    else:
        return jsonify({"message": "No data provided"}),

@bp.route("/users",methods=["GET"])
def get_users():
    users =User.query.all()
    result=[]
    for user in users:
        user_data={
            "customer_id":user.customer_id,
            "name":user.name,
            "email_id":user.email_id,
            "phone_no":user.phone_no,
            "full_address":user.full_address,
            "event":user.event,
            # "password":user.password,
            "created_at":user.created_at,
            "lastupdated":user.lastupdated
        }

        result.append(user_data)
    print(result)
    return jsonify(result), 200


@bp.route("/users/<customer_id>", methods=["GET"])
def get_user_by_id(customer_id):

    user= User.query.filter_by(customer_id=customer_id).first()
    if user:
        user_data={
            "customer_id": user.customer_id,
            "name": user.name,
            "email_id": user.email_id,
            "phone_no": user.phone_no,
            "full_address": user.full_address,
            "event": user.event,
            # "password":user.password,
            "created_at":user.created_at,
            "lastupdated":user.lastupdated
        }

        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404
    
@bp.route("/users/<customer_id>", methods=["PUT"])
def update_user(customer_id):
    current_date=str(datetime.datetime.now())

    data=request.get_json()
    user= User.query.filter_by(customer_id=customer_id).first()
    if user:
        user.name = data.get("name", user.name)
        user.email_id = data.get("email_id", user.email_id)
        user.phone_no = data.get("phone_no", user.phone_no)
        user.full_address = data.get("full_address", user.full_address)
        user.event = data.get("event", user.event)
        # user.password=data.get("password",user.password)
        user.lastupdated=current_date

        try:
            db.session.commit()
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update user"}), 500
    else:
        return jsonify({"message": "User not found"}), 404

@bp.route("/users/<customer_id>",methods=["DELETE"])
def user_delete(customer_id):
    user = User.query.filter_by(customer_id=customer_id).first()
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to delete user"}), 500
    else:
        return jsonify({"message": "User not found"}), 404
    