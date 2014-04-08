# -*- coding: utf-8 -*-

"""Asynchronouse task queue interface.
"""

from time import sleep

from redis import Redis
from rq import Queue

from spz import app, mail


# TODO(daniel): config: custom host, port, db, pw -- dummy queue for testing?
queue = Queue(connection=Redis())

# Async tasks


def async_send(msg):
    # this may throw -- exceptions are handled by rq, stored in 'failed' queue
    with app.app_context():
        mail.send(msg)

    # XXX: hack: artificially slow down the mail queue -- search for better way
    sleep(10)


# vim: set tabstop=4 shiftwidth=4 expandtab:
