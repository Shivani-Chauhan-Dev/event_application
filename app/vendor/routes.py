from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify
import bcrypt
from . import bp


@bp.route("/vendor/registration",methods=["POST"])
def vendor_registration():
    data= request.get_json()
    if data:
        vendor_id=data.get("vendor_id")
        organization_name=data.get("organization_name")
        person_name=data.get("person_name")
        full_address=data.get("full_address")
        email_id=data.get("email_id")
        password=data.get("password")
        phone_no=data.get("phone_no")
        event=data.get("event")
        gst_no=data.get("gst_no")
        print(type(vendor_id),type(organization_name),type(person_name),type(full_address),type(email_id),type(password),type(phone_no),type(event),type(gst_no))
        # print(vendor_id,organization_name,person_name,full_address,email_id,phone_no,event,gst_no)

        if vendor_id and organization_name and person_name and full_address and email_id and password and phone_no and event and gst_no:
            existing_user= VENDOR.query.filter_by(email_id=email_id).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400
            else:
                hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt()
                )

            
                if VENDOR.create_vendor(
                        {
                        "vendor_id":vendor_id,
                        "organization_name":organization_name,
                        "person_name":person_name,
                        "full_address":full_address,
                        "email_id":email_id,
                        "password":hashed_password,
                        "phone_no":phone_no,
                        "event":event,
                        "gst_no":gst_no
                    }
                ):
                    return jsonify({"message": "User created successfully"}), 201
                else:
                    return jsonify({"message": "Failed to create user"}), 500
        else:
            return jsonify({"message": "Missing fields"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400 

@bp.route("/vendors",methods=["GET"])
def get_vendor():
    vendors=VENDOR.query.all()
    result=[]
    for vendor in vendors:
        vendor_data={
            "vendor_id":vendor.vendor_id,
            "organization_name":vendor.organization_name,
            "person_name":vendor.person_name,
            "full_address":vendor.full_address,
            "email_id":vendor.email_id,
            "phone_no":vendor.phone_no,
            "event":vendor.event,
            "gst_no":vendor.gst_no
        }

        result.append(vendor_data)
    return jsonify(result), 200

@bp.route("/vendors/<vendor_id>",methods=["GET"])
def get_vendor_by_id(vendor_id):
    vendor = VENDOR.query.filter_by(vendor_id=vendor_id).first()
    if vendor:
        vendor_data={
            "vendor_id":vendor.vendor_id,
            "organization_name":vendor.organization_name,
            "person_name":vendor.person_name,
            "full_address":vendor.full_address,
            "email_id":vendor.email_id,
            "phone_no":vendor.phone_no,
            "event":vendor.event,
            "gst_no":vendor.gst_no
        }

        return jsonify(vendor_data),200
    else:
        return jsonify({"message":"Vendor not found"}), 400

@bp.route("/vendors/<vendor_id>",methods=["PUT"])
def update_vendor(vendor_id):
    data=request.get_json()
    vendor=VENDOR.query.filter_by(vendor_id=vendor_id).first()
    if vendor:
        vendor.organization_name=data.get("organization_name",vendor.organization_name)
        vendor.person_name=data.get("person_name",vendor.person_name)
        vendor.full_address=data.get("full_address",vendor.full_address)
        vendor.email_id=data.get("email_id",vendor.email_id)
        vendor.phone_no=data.get("phone_no",vendor.phone_no)
        vendor.event=data.get("event",vendor.event)
        vendor.gst_no=data.get("gst_no",vendor.gst_no)

        try:
            db.session.commit()
            return jsonify({"message": "Vendor updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update vendor"}), 500
    else:
        return jsonify({"message": "Vendor not found"}), 404
    
@bp.route("/vendors/<vendor_id>",methods=["DELETE"])
def vender_delete(vendor_id):
    vendor=VENDOR.query.filter_by(vendor_id=vendor_id).first()
    if vendor:
        try:
            db.session.delete(vendor)
            db.session.commit()
            return jsonify({"message":"Vendor deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message":"Failed to delete vendor"}), 500
    else:
        return jsonify({"message":"Vendor not found"}), 404
