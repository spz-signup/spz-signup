# -*- coding: utf-8 -*-

"""Celery tasks.
"""

from celery import Celery

from spz import app, mail

from spz.iliasharvester import refresh
from spz.populate import populate_global


__all__ = [
    'cel',
    'populate',
    'send_slow',
    'send_quick',
    'sync_ilias',
]


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


@cel.task(bind=True, rate_limit='20/m')
def send_slow(self, msg):
    try:
        mail.send(msg)
    except Exception as e:
        raise self.retry(exc=e)


@cel.task(bind=True, rate_limit='30/m')
def send_quick(self, msg):
    try:
        mail.send(msg)
    except Exception as e:
        raise self.retry(exc=e)


@cel.task
def populate():
    # don't catch exception because task is stateless and will be rescheduled
    populate_global()


@cel.task
def sync_ilias():
    # don't catch exception because task is stateless and will be rescheduled
    refresh()
