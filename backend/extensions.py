from celery import Celery
from flask_mail import Mail, Message
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from celery.schedules import crontab

db = SQLAlchemy()
cache = Cache(config={
    "CACHE_TYPE": 'RedisCache',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)
mail = Mail()

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    celery.conf.beat_schedule = {
        'send-daily-reminder': {
            'task': 'tasks.send_daily_reminder',
            'schedule': crontab(hour=18, minute=0), 
        },
        'send-monthly-report': {
            'task': 'tasks.send_monthly_report',
            'schedule': crontab(day_of_month=1, hour=8, minute=0),
        }
    }

    celery.conf.timezone = 'Asia/Kolkata'

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


