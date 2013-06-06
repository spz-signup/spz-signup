# -*- coding: utf-8 -*-

from flask import render_template

from spz import app


# the error code has to be passed to the client explicitely
def render_error(errorcode, errormessage):
    return render_template('errorhandler.html', errorcode=errorcode, errormessage=errormessage), errorcode


@app.errorhandler(404)
def page_not_found(e):
    return render_error(404, u'Page not found')


@app.errorhandler(403)
def page_forbidden(e):
    return render_error(403, u'Access forbidden')


@app.errorhandler(410)
def page_gone(e):
    return render_error(410, u'Page gone')


@app.errorhandler(500)
def not_found(e):
    return render_error(500, u'Internal server error')


# vim: set tabstop=4 shiftwidth=4 expandtab:
