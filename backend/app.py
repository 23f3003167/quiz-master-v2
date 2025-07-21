from flask import Flask, request, jsonify, current_app
from models import db, User
from functools import wraps
import jwt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abcdefghijklmnopqrstuvwxyz"

db.init_app(app)

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                 return jsonify({"message": "Token missing"}), 403
            
            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
                user = User.query.get(data['user_id'])
                if role and user.role != user.role:
                    return jsonify({"message":"Unauthorized"}), 403
            except:
                return jsonify({"message":"Token Invalid or expired"}), 403
            
            return f(user, *args, **kwargs)
        return wrapper
    return decorator

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role="admin").first():
            admin = User(username="admin@gmail.com", role="admin", full_name="Admin", qualification="Educator", dob="1999-01-01")
            admin.password = "admin@2005"
            db.session.add(admin)
            db.session.commit()
            print('Admin credentials added.')
    app.run(debug=True)