# -*- coding: utf-8 -*-

from spz import app
from spz.decorators import templated


@app.route('/')
@templated('baselayout.html')
def index():
    return None


# vim: set tabstop=4 shiftwidth=4 expandtab:
