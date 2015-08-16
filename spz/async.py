# -*- coding: utf-8 -*-

"""Asynchronouse task queue interface.
"""

from time import sleep

from redis import Redis
from rq import Queue

from spz import app, mail


queue = Queue(
    connection=Redis(
        host=app.config.get('REDIS_HOST', 'localhost'),
        port=app.config.get('REDIS_PORT', 6379),
        db=app.config.get('REDIS_DB', 0),
        password=app.config.get('REDIS_PASSWORD', None)
    )
)

# Async tasks


def async_send(msg):
    # this may throw -- exceptions are handled by rq, stored in 'failed' queue
    with app.app_context():
        mail.send(msg)

    # XXX: hack: artificially slow down the mail queue -- search for better way
    sleep(2)


# vim: set tabstop=4 shiftwidth=4 expandtab:
