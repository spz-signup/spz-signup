# -*- coding: utf-8 -*-

"""Custom error handlers.

   Registers error handlers for the most common errors.
"""

from flask import render_template

from spz import app


def render_error(errorcode, errormessage):
    """Renders the error handler template and explicitely sets the HTTP status code.

       :param errorcode: The HTTP error code.
       :param errormessage: The error message to render.
    """
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
