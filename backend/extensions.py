from celery import Celery
from flask_mail import Mail, Message
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

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


