# -*- coding: utf-8 -*-

from spz import app


@app.route('/')
def index():
    return u'hello'


# vim: set tabstop=4 shiftwidth=4 expandtab:
