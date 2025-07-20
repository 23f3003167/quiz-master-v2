from flask import Flask
from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abcdefghijklmnopqrstuvwxyz"

db.init_app(app)

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