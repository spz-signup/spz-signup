# -*- coding: utf-8 -*-

from flask import render_template

from spz import app


@app.route('/')
def index():
    return render_template('baselayout.html')


# vim: set tabstop=4 shiftwidth=4 expandtab:
