from flask import Flask
from models import db, User
from auth import auth
from admin import admin
from flask_cors import CORS
from user import user
from extensions import db, make_celery, mail, cache, limiter

app = Flask(__name__)

CORS(app, origins=["http://localhost:8080"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abcdefghijklmnopqrstuvwxyz"

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sanjaysakthi000@gmail.com'
app.config['MAIL_PASSWORD'] = 'wjaovhcwcyqthmfk'

mail.init_app(app)
db.init_app(app)
cache.init_app(app)
limiter.init_app(app)
celery = make_celery(app)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

@app.route('/run-daily-reminder')
def run_reminder():
    from tasks import send_daily_reminder
    send_daily_reminder.delay()
    return "Reminder Task Triggered"

@app.route('/run-monthly-report')
def run_monthly():
    from tasks import send_monthly_report
    send_monthly_report.delay()
    return "Monthly Report Task Triggered"

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

import tasks
