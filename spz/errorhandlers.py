# -*- coding: utf-8 -*-

"""Custom error handlers.

   Registers error handlers for the most common errors.
"""

from flask import flash, redirect, render_template, url_for


def render_error(errorcode, errormessage):
    """Renders the error handler template and explicitely sets the HTTP status code.

       :param errorcode: The HTTP error code.
       :param errormessage: The error message to render.
    """
    return render_template('errorhandler.html', errorcode=errorcode, errormessage=errormessage), errorcode


def page_not_found(e):
    return render_error(404, u'Seite nicht gefunden')


def page_forbidden(e):
    return render_error(403, u'Keine Berechtigung')


def page_gone(e):
    return render_error(410, u'Seite wurde entfernt')


def not_found(e):
    return render_error(500, u'Interner Fehler')


def unauthorized(e):
    flash(u'Bitte einloggen!', 'warning')
    return redirect(url_for('login'))
