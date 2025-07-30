from flask import Flask, request, jsonify, current_app
from models import db, User
from auth import auth
from admin import admin
from flask_cors import CORS
from user import user
from celery import Celery
from flask_mail import Mail, Message
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)

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

mail = Mail(app)
db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
            
    
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

import tasks
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

cache = Cache(app, config={
    "CACHE_TYPE": 'RedisCache',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379"
)

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
