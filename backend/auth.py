import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from models import db, User

auth = Blueprint("auth",__name__)

@auth.route("/register", methods=['POST'])
def register():
    data = request.json
    email=data.get('password')
    password = data.get('password')
    full_name=data.get('full_name')
    qualification=data.get('qualification')
    dob=data.get('dob')

    if User.query.filter_by(username=email).first():
        return jsonify({"message":"User already exists"}), 400
    
    user = User(
        username=email,
        full_name=full_name,
        qualification=qualification,
        dob=dob,
        role='user'
    )
    user.password=password
    db.session.add(user)
    db.session.commit()

    return jsonify({"message":"User registered successfully"}), 201

@auth.route("/login", methods=['POST'])
def register():
    data = request.json
    email=data.get('email')
    password=data.get('password')
    role=data.get('role')

    user = User.query.filter_by(username=email, role=role).first()

    if user and user.check_password(password):
        token = jwt.encode({
            "user_id": user.id,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({"token": token})
    return jsonify({"message": "Invalid Credentials"}), 401

