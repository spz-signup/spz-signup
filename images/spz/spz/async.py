# -*- coding: utf-8 -*-

"""Asynchronouse task queue interface.
"""

from celery import Celery

from spz import app, mail


# http://flask.pocoo.org/docs/0.10/patterns/celery/
def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

cel = make_celery(app)

# Async tasks


@cel.task(bind=True, rate_limit="30/m")
def async_send(self, msg):
    try:
        mail.send(msg)
    except Exception as e:
        raise self.retry(exc=e)
