import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from models import db, User
from functools import wraps
import jwt

auth = Blueprint("auth",__name__)

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                 return jsonify({"message": "Token missing"}), 403
            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
                user = User.query.get(data['user_id'])
                if role and user.role != role:
                    return jsonify({"message":"Unauthorized"}), 403
            except:
                return jsonify({"message":"Token Invalid or expired"}), 403
            return f(user, *args, **kwargs)
        return wrapper
    return decorator

@auth.route("/register", methods=['POST'])
def register():
    data = request.json
    email=data.get('email')
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

@auth.route("/", methods=['POST'])
def login():
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

